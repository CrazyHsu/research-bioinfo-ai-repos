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
README_ZH_PATH = ROOT / "README-zh.md"
DISCOVERY_PATH = ROOT / "discovery" / "candidates.md"
TABLE_HEADER = "| repo | type | stars | last update | focus / notes |"
OLD_TABLE_HEADER = "| repo | type | stars | updated | focus / notes |"
ZH_TABLE_HEADER = "| repo | 类型 | stars | last update | 方向 / 备注 |"

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

CATEGORY_ZH = {
    "General Research / AI4S Skill Suites": "综合科研 / AI4S Skill Suites",
    "Paper Writing / Peer Review / Submission Skills": "论文写作 / 审稿 / 投稿 Skills",
    "Literature Search / Scholarly Search MCP": "文献检索 / 学术搜索 MCP",
    "Zotero / CNKI / Google Scholar / Reference Management": "Zotero / CNKI / Google Scholar / 文献管理",
    "Bioinformatics / Omics / Single-Cell Skills": "生信 / 组学 / 单细胞 Skills",
    "Biomedical / Clinical / Medical Research": "生物医学 / 临床 / 医学研究",
    "Biological Databases / Structural Biology / Chemistry / Drug Discovery MCP": "生物数据库 / 结构生物学 / 化学 / 药物发现 MCP",
    "Research Agent Apps / Workspaces": "科研 Agent Apps / Workspaces",
    "Figures / PDF / LaTeX / Research Artifact Tools": "图表 / PDF / LaTeX / 研究产物工具",
    "Awesome Lists / Registries / Further Discovery": "Awesome / Registry / 继续深挖入口",
}

SEED_FIELDS = ["repo", "category", "type", "notes", "notes_zh", "include"]
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
    "notes_zh",
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
            seed_notes_zh = seed.get("notes_zh", "").strip()
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
                "notes_zh": seed_notes_zh or seed_notes,
            }
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            old = existing.get(repo)
            if not old:
                raise SystemExit(f"Could not fetch {repo}: {exc}") from exc
            row = dict(old)
            row["category"] = seed.get("category", row.get("category", "")).strip()
            row["type"] = seed.get("type", row.get("type", "")).strip()
            row["notes"] = seed.get("notes", row.get("notes", "")).strip()
            row["notes_zh"] = seed.get("notes_zh", row.get("notes_zh", row.get("notes", ""))).strip()
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


def render_repo_sections_zh(rows: list[dict[str, str]]) -> list[str]:
    lines: list[str] = []
    for category in CATEGORY_ORDER:
        group = [row for row in rows if row.get("category") == category]
        if not group:
            continue
        lines.extend([
            f"## {CATEGORY_ZH[category]}",
            "",
            ZH_TABLE_HEADER,
            "|---|---:|---:|---|---|",
        ])
        for row in sorted(group, key=lambda item: (-star_int(item), item.get("repo", "").lower())):
            repo = row.get("repo", "").strip()
            url = row.get("url", "").strip() or f"https://github.com/{repo}"
            notes = row.get("notes_zh", "").strip() or row.get("notes", "").strip() or row.get("description", "").strip()
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
        "- Discover candidate repos for manual review: `python3 scripts/discover_candidates.py --limit-per-query 20 --min-stars 5 --output discovery/candidates.md`",
        "- Scheduled updates run through `.github/workflows/update-catalog.yml` every Monday at 03:17 UTC.",
        "- To extend the list, edit `data/repos.seed.tsv` first, then run a refresh or regeneration command.",
        "",
    ]


def render_update_instructions_zh() -> list[str]:
    return [
        "## 更新方式",
        "",
        "- 本地校验：`python3 scripts/update_catalog.py --check`",
        "- 从已有 metadata 重生成：`python3 scripts/update_catalog.py --from-curated`",
        "- 刷新 GitHub metadata：`python3 scripts/update_catalog.py --refresh`",
        "- 发现待审候选 repo：`python3 scripts/discover_candidates.py --limit-per-query 20 --min-stars 5 --output discovery/candidates.md`",
        "- GitHub Actions 会在每周一 03:17 UTC 定时更新，也支持手动触发。",
        "- 扩展清单时先编辑 `data/repos.seed.tsv`，同时维护 `notes` 和 `notes_zh`。",
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


def render_policy_sections_zh() -> list[str]:
    return [
        "## 纳入 / 排除规则",
        "",
        "- 纳入：明确面向科研、论文写作、文献、Zotero/PubMed/arXiv/Semantic Scholar、医学、生物信息、生命科学，并以 skill、plugin、MCP、agent workflow 或 agent-ready tool 形式服务 AI agent 的仓库。",
        "- 保留低 star 项：如果领域直接、接口明确、方向独特，即使 stars 很低也保留。",
        "- 排除：普通教程、书籍/藏书 app、无科研方向的通用 agent 基础设施、无新增价值的镜像或 fork、无描述且无法判断用途的空壳仓库。",
        "",
        "## 停止条件",
        "",
        "最后几轮新增主要是重复 PubMed/arXiv/Zotero 实现、同名 fork、镜像和泛化 AI skill 目录，没有继续出现新的高可信核心 repo，因此停止扩展。",
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
        "This README embeds the full generated catalog so visitors can browse the repo list directly from the project homepage. A Chinese version is available at [README-zh.md](README-zh.md), and the standalone generated catalog is available at [catalog.md](catalog.md).",
        "",
        "## Contents",
        "",
        "- `README-zh.md` - Chinese generated catalog kept in sync with this README.",
        "- `catalog.md` - standalone categorized catalog, sorted by stars within each category.",
        "- `data/repos.seed.tsv` - manually curated source of repo scope, category, type, English notes, and Chinese notes.",
        "- `data/repos.curated.tsv` - generated metadata table with GitHub URL, stars, last update date, language, description, and notes.",
        "- `discovery/candidates.md` - generated candidate report from focused GitHub Search queries; review before adding repos to the seed file.",
        "- `scripts/update_catalog.py` - refresh, regenerate, and validate README/catalog outputs.",
        "- `scripts/discover_candidates.py` - run focused GitHub Search passes and write the candidate report.",
        "- `.github/workflows/update-catalog.yml` - scheduled GitHub Actions workflow for weekly catalog refreshes.",
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
        "Regenerate README, `README-zh.md`, and `catalog.md` from existing metadata:",
        "",
        "```bash",
        "python3 scripts/update_catalog.py --from-curated",
        "```",
        "",
        "Refresh GitHub metadata and regenerate README/catalog outputs:",
        "",
        "```bash",
        "python3 scripts/update_catalog.py --refresh",
        "```",
        "",
        "For higher GitHub API limits, set `GITHUB_TOKEN` or `GH_TOKEN` before running `--refresh`.",
        "",
        "## Update Policy",
        "",
        "Add or change repos in `data/repos.seed.tsv`, not directly in generated Markdown tables. Keep both `notes` and `notes_zh` short and useful. Each category is sorted by stars descending when regenerated.",
        "",
        "Use `discovery/candidates.md` as a triage queue for broad GitHub Search hits. Candidate entries are not part of the catalog until they are manually reviewed and added to `data/repos.seed.tsv`.",
        "",
        "The GitHub Actions workflow refreshes metadata weekly and commits changes only when generated outputs differ.",
        "",
        "## Catalog",
        "",
        f"Generated on {today}.",
        "",
    ]
    lines.extend(render_repo_sections(rows))
    lines.extend(render_policy_sections())
    output_path.write_text("\n".join(lines), encoding="utf-8")


def render_readme_zh(rows: list[dict[str, str]], output_path: Path) -> None:
    today = dt.date.today().isoformat()
    lines: list[str] = [
        "# Research Bioinfo AI Repos 中文版",
        "",
        "这是一个面向 AI agent 的科研、论文写作、文献检索、生物信息、生物医学和生命科学 skill/plugin/MCP GitHub 仓库目录。英文主页见 [README.md](README.md)，独立英文目录见 [catalog.md](catalog.md)。",
        "",
        "## 内容",
        "",
        "- `README.md` - 英文主页目录。",
        "- `README-zh.md` - 中文主页目录，由同一份数据生成。",
        "- `catalog.md` - 独立英文分类目录，每个分类内按 stars 降序排序。",
        "- `data/repos.seed.tsv` - 人工维护的 repo 范围、分类、类型、英文备注和中文备注。",
        "- `data/repos.curated.tsv` - 生成的 metadata 表，包含 GitHub URL、stars、last update、language、description 和备注。",
        "- `discovery/candidates.md` - 由 GitHub Search 生成的待审候选报告；确认范围后再加入 seed。",
        "- `scripts/update_catalog.py` - 刷新、重生成和校验 README/catalog 输出。",
        "- `scripts/discover_candidates.py` - 执行聚焦 GitHub Search 并写入候选报告。",
        "- `.github/workflows/update-catalog.yml` - 每周自动刷新目录的 GitHub Actions workflow。",
        "- `plans/update-catalog-plan.md` - 可重复执行的更新流程。",
        "- `skills/research-repo-catalog/` - 维护这个目录的 Codex skill。",
        "",
        "## 快速开始",
        "",
        "不联网校验当前目录：",
        "",
        "```bash",
        "python3 scripts/update_catalog.py --check",
        "```",
        "",
        "从已有 metadata 重生成 README、`README-zh.md` 和 `catalog.md`：",
        "",
        "```bash",
        "python3 scripts/update_catalog.py --from-curated",
        "```",
        "",
        "刷新 GitHub metadata 并重生成目录输出：",
        "",
        "```bash",
        "python3 scripts/update_catalog.py --refresh",
        "```",
        "",
        "如果需要更高 GitHub API 限额，运行 `--refresh` 前设置 `GITHUB_TOKEN` 或 `GH_TOKEN`。",
        "",
        "## 更新策略",
        "",
        "新增或修改 repo 时编辑 `data/repos.seed.tsv`，不要直接编辑生成表格。英文备注维护在 `notes`，中文备注维护在 `notes_zh`。每个分类在重生成时按 stars 降序排序。",
        "",
        "`discovery/candidates.md` 只作为 broad search 的待审队列。候选项只有经过人工判断并加入 `data/repos.seed.tsv` 后，才会进入正式目录。",
        "",
        "GitHub Actions 每周自动刷新 metadata；只有生成内容发生变化时才会提交。",
        "",
        "## 目录",
        "",
        f"生成日期：{today}",
        "",
    ]
    lines.extend(render_update_instructions_zh())
    lines.extend(render_repo_sections_zh(rows))
    lines.extend(render_policy_sections_zh())
    output_path.write_text("\n".join(lines), encoding="utf-8")


def render_outputs(rows: list[dict[str, str]]) -> None:
    render_catalog(rows, CATALOG_PATH)
    render_readme(rows, README_PATH)
    render_readme_zh(rows, README_ZH_PATH)


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
        if not row.get("notes", "").strip():
            errors.append(f"missing English notes for {repo}")
        if not row.get("notes_zh", "").strip():
            errors.append(f"missing Chinese notes for {repo}")

    if "WUBING2023/PaperSpine" not in seen:
        errors.append("missing WUBING2023/PaperSpine")
    if "charlesxu90/ProteinMCP" not in seen:
        errors.append("missing charlesxu90/ProteinMCP")

    for category in CATEGORY_ORDER:
        group = [row for row in rows if row.get("category") == category]
        stars = [star_int(row) for row in group]
        if stars != sorted(stars, reverse=True):
            errors.append(f"category not sorted by stars: {category}")

    for path, label, header, categories in [
        (CATALOG_PATH, "catalog", TABLE_HEADER, CATEGORY_ORDER),
        (README_PATH, "README", TABLE_HEADER, CATEGORY_ORDER),
        (README_ZH_PATH, "README-zh", ZH_TABLE_HEADER, [CATEGORY_ZH[category] for category in CATEGORY_ORDER]),
    ]:
        if not path.exists():
            errors.append(f"missing {label}: {path}")
            continue
        text = path.read_text(encoding="utf-8")
        if header not in text:
            errors.append(f"{label} missing last update table header")
        if OLD_TABLE_HEADER in text:
            errors.append(f"{label} still contains old updated table header")
        if "WUBING2023/PaperSpine" not in text:
            errors.append(f"{label} missing WUBING2023/PaperSpine")
        if "charlesxu90/ProteinMCP" not in text:
            errors.append(f"{label} missing charlesxu90/ProteinMCP")
        for category in categories:
            if f"## {category}" not in text:
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
