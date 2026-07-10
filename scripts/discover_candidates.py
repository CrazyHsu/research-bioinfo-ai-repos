#!/usr/bin/env python3
"""Discover candidate GitHub repos that are not yet in the seed catalog."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
from pathlib import Path
import re
import sys
import time
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SEED_PATH = ROOT / "data" / "repos.seed.tsv"
DEFAULT_OUTPUT = ROOT / "discovery" / "candidates.md"

QUERIES = [
    "ProteinMCP in:name,description,readme",
    '"protein MCP" in:name,description,readme',
    '"autonomous protein design" in:name,description,readme',
    '"protein engineering" "MCP" in:name,description,readme',
    '"Claude Code" "protein" in:name,description,readme',
    "MacromNex MCP in:name,description,readme",
    "Boltz MCP in:name,description,readme",
    "AlphaFold MCP in:name,description,readme",
    "protein agent skills in:name,description,readme",
]

TABLE_HEADER = "| repo | suggested category | suggested type | stars | last update | language | query source | reason |"
TABLE_DIVIDER = "|---|---|---|---:|---|---|---|---|"

DOMAIN_TERMS = [
    "protein",
    "proteomics",
    "alphafold",
    "boltz",
    "macromnex",
    "pdb",
    "pdbe",
    "uniprot",
    "biomolecular",
    "biologics",
    "antibody",
    "nanobody",
    "binder",
    "drug discovery",
    "cheminformatics",
    "bioinformatics",
    "genomics",
    "single-cell",
    "omics",
    "biomedical",
    "medical",
    "clinical",
    "life-science",
    "life science",
]

INTERFACE_TERMS = [
    "mcp",
    "skill",
    "plugin",
    "agent",
    "claude",
    "codex",
    "llm",
    "ai-ready",
    "workflow",
    "server",
    "tool",
]

DISCOVERY_TERMS = [
    "awesome",
    "list",
    "directory",
    "catalog",
    "registry",
    "benchmark",
    "bench",
    "papers",
]


def read_seed_repos(path: Path) -> set[str]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return {
            row["repo"].strip().lower()
            for row in csv.DictReader(fh, delimiter="\t")
            if row.get("repo", "").strip()
        }


def github_json(url: str, token: str | None) -> dict[str, object]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "research-bioinfo-ai-repos-discovery",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = Request(url, headers=headers)
    with urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def search_repositories(query: str, limit: int, token: str | None) -> list[dict[str, object]]:
    params = urlencode(
        {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": str(limit),
        }
    )
    data = github_json(f"https://api.github.com/search/repositories?{params}", token)
    items = data.get("items", [])
    return items if isinstance(items, list) else []


def as_int(value: object) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def clean_cell(value: object) -> str:
    return str(value or "").replace("|", "/").replace("\n", " ").strip()


def has_any(text: str, terms: list[str]) -> bool:
    return any(term in text for term in terms)


def is_relevant_candidate(repo: str, description: str) -> bool:
    lowered = f"{repo} {description}".lower()
    if "proteinmcp" in lowered:
        return True
    has_domain = has_any(lowered, DOMAIN_TERMS)
    if not has_domain:
        return False
    return has_any(lowered, INTERFACE_TERMS) or has_any(lowered, DISCOVERY_TERMS)


def suggest_category(repo: str, text: str) -> str:
    lowered = f"{repo} {text}".lower()
    if any(term in lowered for term in ["pdb", "pdbe", "uniprot", "chembl", "pubchem", "opentargets", "macromnex"]):
        return "Biological Databases / Structural Biology / Chemistry / Drug Discovery MCP"
    if any(term in lowered for term in ["protein", "alphafold", "boltz", "folding", "proteomics"]):
        return "Bioinformatics / Omics / Single-Cell Skills"
    if any(term in lowered for term in ["pubmed", "arxiv", "semantic scholar", "openalex", "crossref"]):
        return "Literature Search / Scholarly Search MCP"
    if any(term in lowered for term in ["awesome", "catalog", "registry", "directory"]):
        return "Awesome Lists / Registries / Further Discovery"
    return "General Research / AI4S Skill Suites"


def suggest_type(repo: str, text: str) -> str:
    lowered = f"{repo} {text}".lower()
    if "mcp" in lowered:
        return "MCP candidate"
    if "skill" in lowered:
        return "Skill candidate"
    if any(term in lowered for term in ["agent", "workflow"]):
        return "Agent workflow candidate"
    return "Candidate"


def discover_candidates(limit: int, min_stars: int, include_forks: bool, include_broad_matches: bool, delay: float) -> tuple[list[dict[str, object]], list[str]]:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    seeded = read_seed_repos(SEED_PATH)
    by_repo: dict[str, dict[str, object]] = {}
    warnings: list[str] = []

    for query in QUERIES:
        try:
            items = search_repositories(query, limit, token)
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            warnings.append(f"{query}: {exc}")
            continue

        for item in items:
            repo = clean_cell(item.get("full_name"))
            if not repo:
                continue
            repo_key = repo.lower()
            if repo_key in seeded:
                continue
            if item.get("archived") or item.get("disabled"):
                continue
            if item.get("fork") and not include_forks:
                continue
            stars = as_int(item.get("stargazers_count"))
            if stars < min_stars:
                continue

            description = clean_cell(item.get("description"))
            if not include_broad_matches and not is_relevant_candidate(repo, description):
                continue
            updated = clean_cell(item.get("updated_at"))[:10]
            existing = by_repo.get(repo_key)
            if existing:
                existing_queries = existing.setdefault("queries", [])
                if isinstance(existing_queries, list) and query not in existing_queries:
                    existing_queries.append(query)
                continue

            by_repo[repo_key] = {
                "repo": repo,
                "url": clean_cell(item.get("html_url")) or f"https://github.com/{repo}",
                "suggested_category": suggest_category(repo, description),
                "suggested_type": suggest_type(repo, description),
                "stars": stars,
                "updated": updated,
                "language": clean_cell(item.get("language")),
                "queries": [query],
                "reason": description or "Matched focused GitHub Search query",
            }

        if delay:
            time.sleep(delay)

    rows = sorted(
        by_repo.values(),
        key=lambda row: (-as_int(row.get("stars")), clean_cell(row.get("repo")).lower()),
    )
    return rows, warnings


def render_candidates(rows: Iterable[dict[str, object]], warnings: list[str], output_path: Path) -> None:
    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines: list[str] = [
        "# Discovery Candidates",
        "",
        f"Generated on: {today}",
        "",
        "These are GitHub Search hits that are not yet present in `data/repos.seed.tsv`. They are candidates only; review README evidence, scope, overlap, license, maintenance, and safety before adding any entry to the seed catalog.",
        "",
        "Default discovery filters out broad README-only matches unless the repository name or description also signals a bio/protein domain plus an MCP/skill/agent/tool or registry/list pattern.",
        "",
        "## Queries",
        "",
    ]
    lines.extend(f"- `{query}`" for query in QUERIES)
    lines.append("")

    if warnings:
        lines.extend(["## Search Warnings", ""])
        lines.extend(f"- `{warning}`" for warning in warnings)
        lines.append("")

    rows = list(rows)
    lines.extend(["## Candidates", "", TABLE_HEADER, TABLE_DIVIDER])
    if rows:
        for row in rows:
            repo = clean_cell(row.get("repo"))
            url = clean_cell(row.get("url")) or f"https://github.com/{repo}"
            queries = row.get("queries", [])
            query_source = "; ".join(clean_cell(query) for query in queries) if isinstance(queries, list) else clean_cell(queries)
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"[{repo}]({url})",
                        clean_cell(row.get("suggested_category")),
                        clean_cell(row.get("suggested_type")),
                        str(as_int(row.get("stars"))),
                        clean_cell(row.get("updated")),
                        clean_cell(row.get("language")),
                        query_source,
                        clean_cell(row.get("reason")),
                    ]
                )
                + " |"
            )
    else:
        lines.append("| No unseeded candidates matched the current query set and filters. | | |  | | | | |")
    lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")


def check_candidates(output_path: Path) -> int:
    errors: list[str] = []
    if not output_path.exists():
        print(f"ERROR: missing candidate report: {output_path}", file=sys.stderr)
        return 1

    text = output_path.read_text(encoding="utf-8")
    if "# Discovery Candidates" not in text:
        errors.append("candidate report missing title")
    if "last update" not in text:
        errors.append("candidate report missing last update column")

    seeded = read_seed_repos(SEED_PATH)
    seen: set[str] = set()
    for match in re.finditer(r"\|\s*\[([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)\]\(", text):
        repo = match.group(1)
        key = repo.lower()
        if key in seeded:
            errors.append(f"candidate report includes already seeded repo: {repo}")
        if key in seen:
            errors.append(f"duplicate candidate repo: {repo}")
        seen.add(key)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"ok: candidate report contains {len(seen)} unseeded repos")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit-per-query", type=int, default=20, help="Maximum GitHub Search results to inspect per query")
    parser.add_argument("--min-stars", type=int, default=5, help="Minimum stars required for candidate output")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Candidate Markdown report path")
    parser.add_argument("--include-forks", action="store_true", help="Include fork repositories in the candidate report")
    parser.add_argument("--include-broad-matches", action="store_true", help="Keep broad README-only matches that fail the default relevance filter")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between GitHub Search API calls")
    parser.add_argument("--check", action="store_true", help="Validate an existing candidate report without network")
    args = parser.parse_args()

    output_path = args.output if args.output.is_absolute() else ROOT / args.output
    if args.check:
        return check_candidates(output_path)

    rows, warnings = discover_candidates(args.limit_per_query, args.min_stars, args.include_forks, args.include_broad_matches, args.delay)
    render_candidates(rows, warnings, output_path)
    return check_candidates(output_path)


if __name__ == "__main__":
    raise SystemExit(main())
