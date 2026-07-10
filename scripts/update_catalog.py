#!/usr/bin/env python3
"""Update and validate the curated research/bioinfo AI repo catalog."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
from pathlib import Path
import sys
import time
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SEED_PATH = ROOT / "data" / "repos.seed.tsv"
CURATED_PATH = ROOT / "data" / "repos.curated.tsv"
CATALOG_PATH = ROOT / "catalog.md"
README_PATH = ROOT / "README.md"
TABLE_HEADER = "| repo | type | stars | last update | focus / notes |"
OLD_TABLE_HEADER = "| repo | type | stars | updated | focus / notes |"

CATEGORY_ORDER = [
    "General Research / AI4S Skill Suites",
    "Paper Writing / Peer Review / Submission Skills",
    "Literature Search / Scholarly Search MCP",
    "Zotero / CNKI / Google Scholar / Reference Management",
    "Bioinformatics / Omics / Single-Cell Skills",
    "Biomedical / Clinical / Medical Research",
    "Biological Databases / Structural Biology / Chemistry / Drug Discovery MCP",
    "Research Agent Apps / Workspaces",
    "Figures / PDF / LaTeX / Research Artifact Tools",
    "Awesome Lists / Registries / Further Discovery",
]

SEED_FIELDS = ["repo", "category", "type", "notes", "include"]
CURATED_FIELDS = [
    "repo",
    "url",
    "category",
    "type",
    "stars",
    "updated",
    "language",
    "description",
    "notes",
]


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"Missing required file: {path}")
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def write_tsv(path: Path, fields: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: str(row.get(field, "")) for field in fields})


def category_rank(category: str) -> int:
    try:
        return CATEGORY_ORDER.index(category)
    except ValueError:
        return len(CATEGORY_ORDER)


def star_int(row: dict[str, str]) -> int:
    value = row.get("stars", "0").strip()
    return int(value) if value.isdigit() else 0


def sort_rows(rows: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    return sorted(
        rows,
        key=lambda row: (category_rank(row.get("category", "")), -star_int(row), row.get("repo", "").lower()),
    )


def fetch_repo(repo: str, token: str | None) -> dict[str, object]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "research-bioinfo-ai-repos-catalog",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = Request(f"https://api.github.com/repos/{repo}", headers=headers)
    with urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def refresh_from_github(seed_path: Path, curated_path: Path, delay: float) -> list[dict[str, str]]:
    seed_rows = read_tsv(seed_path)
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    existing = {row["repo"]: row for row in read_tsv(curated_path)} if curated_path.exists() else {}
    output: list[dict[str, str]] = []
    seen: set[str] = set()

    for seed in seed_rows:
        repo = seed.get("repo", "").strip()
        if not repo or repo in seen or seed.get("include", "yes").lower() in {"no", "false", "0"}:
            continue
        seen.add(repo)
        try:
            meta = fetch_repo(repo, token)
            seed_notes = seed.get("notes", "").strip()
            row = {
                "repo": meta.get("full_name") or repo,
                "url": meta.get("html_url") or f"https://github.com/{repo}",
                "category": seed.get("category", "").strip(),
                "type": seed.get("type", "").strip(),
                "stars": meta.get("stargazers_count", 0),
                "updated": str(meta.get("updated_at", ""))[:10],
                "language": meta.get("language") or "",
                "description": seed_notes or meta.get("description") or "",
                "notes": seed_notes,
            }
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            old = existing.get(repo)
            if not old:
                raise SystemExit(f"Could not fetch {repo}: {exc}") from exc
            row = dict(old)
            row["category"] = seed.get("category", row.get("category", "")).strip()
            row["type"] = seed.get("type", row.get("type", "")).strip()
            row["notes"] = seed.get("notes", row.get("notes", "")).strip()
            print(f"warning: using cached metadata for {repo}: {exc}", file=sys.stderr)
        output.append({key: str(value) for key, value in row.items()})
        if delay:
            time.sleep(delay)

    output = sort_rows(output)
    write_tsv(curated_path, CURATED_FIELDS, output)
    return output


def render_repo_sections(rows: list[dict[str, str]]) -> list[str]:
    lines: list[str] = []
    for category in CATEGORY_ORDER:
        group = [row for row in rows if row.get("category") == category]
        if not group:
            continue
        lines.extend([
            f"## {category}",
            "",
            TABLE_HEADER,
            "|---|---:|---:|---|---|",
        ])
        for row in sorted(group, key=lambda item: (-star_int(item), item.get("repo", "").lower())):
            repo = row.get("repo", "").strip()
            url = row.get("url", "").strip() or f"https://github.com/{repo}"
            notes = row.get("notes", "").strip() or row.get("description", "").strip()
            notes = notes.replace("|", "/")
            lines.append(
                f"| [{repo}]({url}) | {row.get('type', '').strip()} | {star_int(row)} | {row.get('updated', '').strip()} | {notes} |"
            )
        lines.append("")
    return lines


def render_update_instructions() -> list[str]:
    return [
        "## Update Instructions",
        "",
        "- Local validation: `python3 scripts/update_catalog.py --check`",
        "- Regenerate from cached metadata: `python3 scripts/update_catalog.py --from-curated`",
        "- Refresh GitHub metadata: `python3 scripts/update_catalog.py --refresh`",
        "- To extend the list, edit `data/repos.seed.tsv` first, then run a refresh or regeneration command.",
        "",
    ]


def render_policy_sections() -> list[str]:
    return [
        "## Inclusion / Exclusion Rules",
        "",
        "- Include repositories that clearly target research, paper writing, literature, Zotero/PubMed/arXiv/Semantic Scholar, medicine, bioinformatics, or life sciences, and expose that capability as a skill, plugin, MCP server, agent workflow, or agent-ready tool.",
        "- Keep low-star repositories when they are direct, domain-specific, and interface-ready.",
        "- Exclude ordinary tutorials, book inventory apps, generic agent infrastructure without a research angle, mirror-only forks without meaningful additions, and empty shells with no useful description.",
        "",
        "## Stopping Criteria",
        "",
        "Expansion stopped after the last passes produced mostly duplicate PubMed/arXiv/Zotero implementations, same-name forks, mirrors, and broad AI skill directories rather than new high-confidence core repositories.",
        "",
    ]


def render_catalog(rows: list[dict[str, str]], output_path: Path) -> None:
    today = dt.date.today().isoformat()
    lines: list[str] = [
        "# GitHub Research, Paper Writing, Bioinformatics AI Skill/Plugin Repos",
        "",
        f"Search date: {today}",
        "",
        "Scope: AI-agent-related skills, plugins, MCP servers, and agent-ready workflows, with emphasis on research, paper writing, literature search, Zotero/arXiv/PubMed/Semantic Scholar, life sciences, bioinformatics, and medical research. This catalog does not attempt to enumerate traditional scientific software plugin ecosystems or generic agent infrastructure with no clear research relevance.",
        "",
        "Notes: GitHub Search cannot mathematically guarantee complete coverage. `data/repos.seed.tsv` is the manually maintained source for scope and categories, and `scripts/update_catalog.py` fetches or reuses GitHub metadata to generate the Markdown outputs. Star counts are GitHub metadata, not a quality judgment. Some 2026 repositories have unusually high star counts; review source code, license, dependencies, network behavior, and file permissions before use.",
        "",
    ]
    lines.extend(render_update_instructions())
    lines.extend(render_repo_sections(rows))
    lines.extend(render_policy_sections())
    output_path.write_text("\n".join(lines), encoding="utf-8")


def render_readme(rows: list[dict[str, str]], output_path: Path) -> None:
    today = dt.date.today().isoformat()
    lines: list[str] = [
        "# Research Bioinfo AI Repos",
        "",
        "Curated GitHub catalog for AI-agent-related research, academic writing, literature search, bioinformatics, biomedical, and life-science skill/plugin/MCP repositories.",
        "",
        "This README embeds the full generated catalog so visitors can browse the repo list directly from the project homepage. The standalone generated catalog is also available at [catalog.md](catalog.md).",
        "",
        "## Contents",
        "",
        "- `catalog.md` - standalone categorized catalog, sorted by stars within each category.",
        "- `data/repos.seed.tsv` - manually curated source of repo scope, category, type, and notes.",
        "- `data/repos.curated.tsv` - generated metadata table with GitHub URL, stars, last update date, language, description, and notes.",
        "- `scripts/update_catalog.py` - refresh, regenerate, and validate README/catalog outputs.",
        "- `plans/update-catalog-plan.md` - repeatable update workflow for humans or agents.",
        "- `skills/research-repo-catalog/` - Codex skill that explains how to maintain this catalog.",
        "- `archive/` - prior generated versions kept for traceability.",
        "",
        "## Quick Start",
        "",
        "Validate the current catalog without network:",
        "",
        "```bash",
        "python3 scripts/update_catalog.py --check",
        "```",
        "",
        "Regenerate README and `catalog.md` from existing metadata:",
        "",
        "```bash",
        "python3 scripts/update_catalog.py --from-curated",
        "```",
        "",
        "Refresh GitHub metadata and regenerate README/catalog:",
        "",
        "```bash",
        "python3 scripts/update_catalog.py --refresh",
        "```",
        "",
        "For higher GitHub API limits, set `GITHUB_TOKEN` or `GH_TOKEN` before running `--refresh`.",
        "",
        "## Update Policy",
        "",
        "Add or change repos in `data/repos.seed.tsv`, not directly in generated Markdown tables. Keep categories specific enough that the catalog remains readable. Each category is sorted by stars descending when regenerated.",
        "",
        "Do not push this repository unless a remote is intentionally configured later.",
        "",
        "## Catalog",
        "",
        f"Generated on {today}.",
        "",
    ]
    lines.extend(render_repo_sections(rows))
    lines.extend(render_policy_sections())
    output_path.write_text("\n".join(lines), encoding="utf-8")


def render_outputs(rows: list[dict[str, str]]) -> None:
    render_catalog(rows, CATALOG_PATH)
    render_readme(rows, README_PATH)


def check_catalog(rows: list[dict[str, str]]) -> int:
    errors: list[str] = []
    seen: set[str] = set()
    for row in rows:
        repo = row.get("repo", "").strip()
        if not repo:
            errors.append("blank repo field")
            continue
        if repo in seen:
            errors.append(f"duplicate repo: {repo}")
        seen.add(repo)
        if row.get("category", "") not in CATEGORY_ORDER:
            errors.append(f"unknown category for {repo}: {row.get('category', '')}")
        if not row.get("url", "").startswith("https://github.com/"):
            errors.append(f"bad GitHub URL for {repo}: {row.get('url', '')}")

    if "WUBING2023/PaperSpine" not in seen:
        errors.append("missing WUBING2023/PaperSpine")

    for category in CATEGORY_ORDER:
        group = [row for row in rows if row.get("category") == category]
        stars = [star_int(row) for row in group]
        if stars != sorted(stars, reverse=True):
            errors.append(f"category not sorted by stars: {category}")

    for path, label in [(CATALOG_PATH, "catalog"), (README_PATH, "README")]:
        if not path.exists():
            errors.append(f"missing {label}: {path}")
            continue
        text = path.read_text(encoding="utf-8")
        if TABLE_HEADER not in text:
            errors.append(f"{label} missing last update table header")
        if OLD_TABLE_HEADER in text:
            errors.append(f"{label} still contains old updated table header")
        if "WUBING2023/PaperSpine" not in text:
            errors.append(f"{label} missing WUBING2023/PaperSpine")
        for category in CATEGORY_ORDER:
            if any(row.get("category") == category for row in rows) and f"## {category}" not in text:
                errors.append(f"{label} missing category heading: {category}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"ok: {len(rows)} repos across {len({row['category'] for row in rows})} categories")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--refresh", action="store_true", help="Fetch current GitHub metadata and regenerate README/catalog")
    mode.add_argument("--from-curated", action="store_true", help="Regenerate README/catalog from data/repos.curated.tsv without network")
    mode.add_argument("--check", action="store_true", help="Validate data and generated Markdown without network")
    parser.add_argument("--delay", type=float, default=0.0, help="Delay between GitHub API calls during --refresh")
    args = parser.parse_args()

    if args.refresh:
        rows = refresh_from_github(SEED_PATH, CURATED_PATH, args.delay)
        render_outputs(rows)
        return check_catalog(rows)

    rows = sort_rows(read_tsv(CURATED_PATH))
    if args.from_curated:
        render_outputs(rows)
        write_tsv(CURATED_PATH, CURATED_FIELDS, rows)
        return check_catalog(rows)
    if args.check:
        return check_catalog(rows)

    render_outputs(rows)
    return check_catalog(rows)


if __name__ == "__main__":
    raise SystemExit(main())
