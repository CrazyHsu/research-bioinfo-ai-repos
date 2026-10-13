#!/usr/bin/env python3
"""Update, render, and validate the curated research/bioinfo AI repo catalog.

Data flow
---------
  data/repos.seed.tsv  (human-maintained scope, category, type, notes)
        |  --refresh  (GitHub REST API)
        v
  data/repos.curated.tsv  (seed fields + GitHub metadata, sorted by repo name)
  data/star_history.tsv   (append-only weekly snapshot: date, repo, stars, forks, pushed_at)
  data/last_refresh.json  (when the metadata was last fetched)
  data/refresh_report.md  (what failed or changed during the last refresh)
        |  render
        v
  README.md / README-zh.md / catalog.md  (tables injected between CATALOG markers)
  catalog.json / CHANGELOG.md

Modes
-----
  --refresh        fetch GitHub metadata for every active seed repo, then render and check
  --from-curated   merge seed fields into cached metadata and render without network
  --check          validate data files and rendered outputs without network
  --summary        print a one-line summary of the last refresh (used for commit messages)

Prose outside the ``<!-- CATALOG:START -->`` / ``<!-- CATALOG:END -->`` markers in the three
Markdown files is never touched, so it can be edited by hand.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CONFIG_PATH = DATA / "catalog_config.json"
SEED_PATH = DATA / "repos.seed.tsv"
CURATED_PATH = DATA / "repos.curated.tsv"
HISTORY_PATH = DATA / "star_history.tsv"
LAST_REFRESH_PATH = DATA / "last_refresh.json"
REPORT_PATH = DATA / "refresh_report.md"
AWESOME_REFS_PATH = DATA / "awesome_refs.tsv"
POLICY_DOC_PATH = ROOT / "skills" / "research-repo-catalog" / "references" / "catalog-policy.md"
README_PATH = ROOT / "README.md"
README_ZH_PATH = ROOT / "README-zh.md"
CATALOG_PATH = ROOT / "catalog.md"
JSON_PATH = ROOT / "catalog.json"
CHANGELOG_PATH = ROOT / "CHANGELOG.md"

MARK_START = "<!-- CATALOG:START -->"
MARK_END = "<!-- CATALOG:END -->"
OLD_TABLE_HEADERS = (
    "| repo | type | stars | updated | focus / notes |",
    "| repo | type | stars | last update | focus / notes |",
    "| repo | 类型 | stars | last update | 方向 / 备注 |",
)

SEED_FIELDS = [
    "repo", "category", "type", "type_detail", "interfaces", "hosts", "domain",
    "pinned", "notes", "notes_zh", "include",
]
SEED_TO_CURATED = [
    "category", "type", "type_detail", "interfaces", "hosts", "domain", "pinned", "notes", "notes_zh",
]
CURATED_FIELDS = [
    "repo", "url", "category", "type", "type_detail", "interfaces", "hosts", "domain", "pinned",
    "stars", "forks", "open_issues", "created_at", "pushed_at", "updated_at", "archived",
    "license", "language", "topics", "homepage", "description", "notes", "notes_zh",
    "listed_in", "status", "missing_since", "renamed_to", "fetched_at",
]
HISTORY_FIELDS = ["date", "repo", "stars", "forks", "pushed_at"]
STATUS_VALUES = {"ok", "cached", "missing", "pending"}
MISSING_GRACE_DAYS = 8
CHANGELOG_ENTRIES = 16
CJK_RE = re.compile(r"[㐀-鿿]")
USER_AGENT = "research-bioinfo-ai-repos-catalog"

LOCALES = {
    "en": {
        "table_header": "| repo | type | stars | last push | focus / notes |",
        "table_divider": "|---|---|---:|---|---|",
        "archived": "(archived)",
        "pending": "pending",
        "refreshed": (
            "Metadata refreshed on {date} (UTC): {count} repositories in {ncat} categories. "
            "Stars and last-push dates come from the GitHub REST API; `(archived)` marks archived repositories. "
            "All fields, including license, language, topics, interfaces, and hosts, are in "
            "`data/repos.curated.tsv` and `catalog.json`."
        ),
        "pending_note": "{count} newly seeded repositories are marked `pending`: their metadata is filled in by the next scheduled refresh.",
        "recent": "### Recent changes",
        "recent_intro": "Refresh of {date} compared with {prev}. Full history: [CHANGELOG.md](CHANGELOG.md).",
        "recent_first": "First recorded snapshot on {date}; no earlier data to compare.",
        "added": "Added",
        "removed": "Removed",
        "archived_label": "Archived",
        "renamed": "Renamed",
        "missing": "Missing on GitHub",
        "gainers": "Top star gains",
        "none": "none",
    },
    "zh": {
        "table_header": "| repo | 类型 | stars | 最近 push | 方向 / 备注 |",
        "table_divider": "|---|---|---:|---|---|",
        "archived": "(已归档)",
        "pending": "待抓取",
        "refreshed": (
            "元数据刷新于 {date}（UTC）：{count} 个仓库，{ncat} 个分类。"
            "stars 与最近 push 日期来自 GitHub REST API；`(已归档)` 表示仓库已归档。"
            "license、语言、topics、接口形态、宿主等完整字段见 `data/repos.curated.tsv` 与 `catalog.json`。"
        ),
        "pending_note": "{count} 个新加入的仓库标记为 `待抓取`：其元数据将在下一次定时刷新时补全。",
        "recent": "### 最近变化",
        "recent_intro": "{date} 的刷新与 {prev} 对比。完整历史见 [CHANGELOG.md](CHANGELOG.md)。",
        "recent_first": "{date} 是首个记录快照，没有更早数据可对比。",
        "added": "新增",
        "removed": "移除",
        "archived_label": "已归档",
        "renamed": "已改名",
        "missing": "GitHub 上已不存在",
        "gainers": "本期 star 增长 Top",
        "none": "无",
    },
}


# --------------------------------------------------------------------------- helpers

def today_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")


def now_utc_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def clean_cell(value: object) -> str:
    return str(value or "").replace("\t", " ").replace("\r", " ").replace("\n", " ").replace("|", "/").strip()


def star_int(row: dict[str, str]) -> int:
    value = str(row.get("stars", "0")).strip()
    return int(value) if value.isdigit() else 0


def split_list(value: str) -> list[str]:
    return [item.strip() for item in str(value or "").split(",") if item.strip()]


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"Missing required file: {path}")
    with path.open("r", encoding="utf-8", newline="") as fh:
        return [dict(row) for row in csv.DictReader(fh, delimiter="\t")]


def write_tsv(path: Path, fields: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: clean_cell(row.get(field, "")) for field in fields})


def load_config(path: Path | None = None) -> dict:
    path = path or CONFIG_PATH
    with path.open("r", encoding="utf-8") as fh:
        cfg = json.load(fh)
    cfg["category_order"] = [item["en"] for item in cfg["categories"]]
    cfg["category_zh"] = {item["en"]: item["zh"] for item in cfg["categories"]}
    cfg["type_keys"] = [item["key"] for item in cfg["types"]]
    return cfg


def read_seed(path: Path | None = None) -> list[dict[str, str]]:
    rows = read_tsv(path or SEED_PATH)
    for row in rows:
        for field in SEED_FIELDS:
            row[field] = clean_cell(row.get(field, ""))
        row["include"] = row["include"] or "yes"
    return rows


def active_seed(rows: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in rows:
        key = row["repo"].lower()
        if not key or key in seen or row["include"].lower() in {"no", "false", "0"}:
            continue
        seen.add(key)
        out.append(row)
    return out


def sort_by_repo(rows: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    return sorted(rows, key=lambda row: row.get("repo", "").lower())


def merge_seed(row: dict[str, str], seed: dict[str, str]) -> dict[str, str]:
    for field in SEED_TO_CURATED:
        row[field] = seed.get(field, "")
    row["repo"] = row.get("repo") or seed["repo"]
    row["url"] = row.get("url") or f"https://github.com/{seed['repo']}"
    return row


def load_awesome_refs(path: Path | None = None) -> dict[str, str]:
    path = path or AWESOME_REFS_PATH
    if not path.exists():
        return {}
    return {row["repo"].lower(): row.get("listed_in", "") for row in read_tsv(path) if row.get("repo")}


# --------------------------------------------------------------------------- GitHub

def github_headers(token: str | None) -> dict[str, str]:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": USER_AGENT}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def fetch_repo(repo: str, token: str | None) -> dict[str, object]:
    req = Request(f"https://api.github.com/repos/{repo}", headers=github_headers(token))
    with urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def blank_row(seed: dict[str, str]) -> dict[str, str]:
    row = {field: "" for field in CURATED_FIELDS}
    return merge_seed(row, seed)


def row_from_meta(seed: dict[str, str], meta: dict[str, object], fetched: str) -> dict[str, str]:
    license_info = meta.get("license") or {}
    spdx = ""
    if isinstance(license_info, dict):
        spdx = str(license_info.get("spdx_id") or "")
        if spdx == "NOASSERTION":
            spdx = "other"
    topics = meta.get("topics") or []
    row = blank_row(seed)
    row.update({
        "repo": str(meta.get("full_name") or seed["repo"]),
        "url": str(meta.get("html_url") or f"https://github.com/{seed['repo']}"),
        "stars": str(meta.get("stargazers_count") or 0),
        "forks": str(meta.get("forks_count") or 0),
        "open_issues": str(meta.get("open_issues_count") or 0),
        "created_at": str(meta.get("created_at") or "")[:10],
        "pushed_at": str(meta.get("pushed_at") or "")[:10],
        "updated_at": str(meta.get("updated_at") or "")[:10],
        "archived": "yes" if meta.get("archived") else "no",
        "license": spdx,
        "language": str(meta.get("language") or ""),
        "topics": ",".join(str(t) for t in topics) if isinstance(topics, list) else "",
        "homepage": str(meta.get("homepage") or ""),
        "description": clean_cell(meta.get("description")),
        "status": "ok",
        "missing_since": "",
        "renamed_to": "",
        "fetched_at": fetched,
    })
    if row["repo"].lower() != seed["repo"].lower():
        row["renamed_to"] = row["repo"]
        row["repo"] = seed["repo"]
    return row


def refresh_from_github(
    seed_rows: list[dict[str, str]],
    existing: dict[str, dict[str, str]],
    token: str | None,
    delay: float = 0.0,
    only: set[str] | None = None,
    fetcher=fetch_repo,
) -> tuple[list[dict[str, str]], dict[str, object]]:
    """Return refreshed curated rows plus a report dict. Never raises for a single repo."""
    today = today_utc()
    output: list[dict[str, str]] = []
    report: dict[str, object] = {
        "refreshed_at": now_utc_iso(), "date": today, "fetched": 0, "cached": 0, "missing": 0,
        "renamed": [], "archived": [], "missing_repos": [], "rate_limited": False, "warnings": [],
    }
    rate_limited = False
    for seed in seed_rows:
        repo = seed["repo"]
        old = existing.get(repo.lower())
        if (only is not None and repo.lower() not in only) or rate_limited:
            row = merge_seed(dict(old), seed) if old else blank_row(seed)
            if not old:
                row["status"] = "pending"
                report["warnings"].append(f"{repo}: not fetched yet (pending first refresh)")
            elif rate_limited:
                row["status"] = "cached"
            output.append(row)
            continue
        try:
            meta = fetcher(repo, token)
            row = row_from_meta(seed, meta, today)
            report["fetched"] = int(report["fetched"]) + 1
            if row["renamed_to"]:
                report["renamed"].append(f"{repo} -> {row['renamed_to']}")
            if row["archived"] == "yes":
                report["archived"].append(repo)
        except HTTPError as exc:
            if exc.code == 404:
                row = merge_seed(dict(old), seed) if old else blank_row(seed)
                row["status"] = "missing"
                row["missing_since"] = (old or {}).get("missing_since") or today
                report["missing"] = int(report["missing"]) + 1
                report["missing_repos"].append(repo)
                report["warnings"].append(f"{repo}: HTTP 404 (deleted, private, or renamed)")
            else:
                remaining = exc.headers.get("x-ratelimit-remaining") if exc.headers else None
                if exc.code in (403, 429) and remaining == "0":
                    rate_limited = True
                    report["rate_limited"] = True
                    report["warnings"].append(f"{repo}: GitHub rate limit exhausted; remaining repos use cached metadata")
                else:
                    report["warnings"].append(f"{repo}: HTTP {exc.code}; using cached metadata")
                row = merge_seed(dict(old), seed) if old else blank_row(seed)
                row["status"] = "cached" if old else "pending"
                report["cached"] = int(report["cached"]) + 1
        except (URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
            row = merge_seed(dict(old), seed) if old else blank_row(seed)
            row["status"] = "cached" if old else "pending"
            report["cached"] = int(report["cached"]) + 1
            report["warnings"].append(f"{repo}: {exc}; using cached metadata")
        output.append(row)
        if delay:
            time.sleep(delay)
    return sort_by_repo(output), report


# --------------------------------------------------------------------------- history / changes

def load_history(path: Path | None = None) -> dict[str, dict[str, dict[str, str]]]:
    path = path or HISTORY_PATH
    history: dict[str, dict[str, dict[str, str]]] = {}
    if not path.exists():
        return history
    for row in read_tsv(path):
        history.setdefault(row["date"], {})[row["repo"]] = row
    return history


def write_history(history: dict[str, dict[str, dict[str, str]]], path: Path | None = None) -> None:
    path = path or HISTORY_PATH
    rows = [history[date][repo] for date in sorted(history) for repo in sorted(history[date], key=str.lower)]
    write_tsv(path, HISTORY_FIELDS, rows)


def append_history(history: dict[str, dict[str, dict[str, str]]], rows: list[dict[str, str]], date: str) -> None:
    snapshot = history.setdefault(date, {})
    for row in rows:
        if row.get("status") != "ok":
            continue
        snapshot[row["repo"]] = {
            "date": date, "repo": row["repo"], "stars": row.get("stars", ""),
            "forks": row.get("forks", ""), "pushed_at": row.get("pushed_at", ""),
        }


def compute_changes(history: dict[str, dict[str, dict[str, str]]], curated: list[dict[str, str]], limit: int | None = None) -> list[dict[str, object]]:
    dates = sorted(history)
    entries: list[dict[str, object]] = []
    for index in range(len(dates) - 1, -1, -1):
        date = dates[index]
        prev = dates[index - 1] if index > 0 else None
        current = history[date]
        previous = history[prev] if prev else {}
        entry: dict[str, object] = {"date": date, "prev": prev, "added": [], "removed": [], "gains": []}
        if prev:
            entry["added"] = sorted(set(current) - set(previous), key=str.lower)
            entry["removed"] = sorted(set(previous) - set(current), key=str.lower)
            gains = []
            for repo, row in current.items():
                old = previous.get(repo)
                if old and row["stars"].isdigit() and old["stars"].isdigit():
                    gains.append((int(row["stars"]) - int(old["stars"]), repo, int(old["stars"]), int(row["stars"])))
            gains.sort(key=lambda item: (-item[0], item[1].lower()))
            entry["gains"] = [item for item in gains[:10] if item[0] > 0]
        entries.append(entry)
        if limit and len(entries) >= limit:
            break
    if entries:
        latest = entries[0]
        latest["archived"] = sorted((r["repo"] for r in curated if r.get("archived") == "yes"), key=str.lower)
        latest["renamed"] = sorted((f"{r['repo']} -> {r['renamed_to']}" for r in curated if r.get("renamed_to")), key=str.lower)
        latest["missing"] = sorted((r["repo"] for r in curated if r.get("status") == "missing"), key=str.lower)
    return entries


def fmt_repo_list(items: list[str], none_label: str) -> str:
    return ", ".join(f"`{item}`" for item in items) if items else none_label


def render_recent_changes(entries: list[dict[str, object]], locale: str) -> list[str]:
    L = LOCALES[locale]
    if not entries:
        return []
    entry = entries[0]
    lines = [L["recent"], ""]
    if not entry.get("prev"):
        lines.append(L["recent_first"].format(date=entry["date"]))
        lines.append("")
        return lines
    lines.append(L["recent_intro"].format(date=entry["date"], prev=entry["prev"]))
    lines.append("")
    lines.append(f"- {L['added']}: {fmt_repo_list(entry['added'], L['none'])}")
    lines.append(f"- {L['removed']}: {fmt_repo_list(entry['removed'], L['none'])}")
    lines.append(f"- {L['archived_label']}: {fmt_repo_list(entry.get('archived', []), L['none'])}")
    lines.append(f"- {L['renamed']}: {fmt_repo_list(entry.get('renamed', []), L['none'])}")
    lines.append(f"- {L['missing']}: {fmt_repo_list(entry.get('missing', []), L['none'])}")
    gains = entry.get("gains", [])[:5]
    if gains:
        gain_text = ", ".join(f"`{repo}` +{gain} ({old} -> {new})" for gain, repo, old, new in gains)
    else:
        gain_text = L["none"]
    lines.append(f"- {L['gainers']}: {gain_text}")
    lines.append("")
    return lines


def render_changelog(entries: list[dict[str, object]]) -> str:
    lines = [
        "# Changelog",
        "",
        "Generated by `scripts/update_catalog.py` from `data/star_history.tsv` and `data/repos.curated.tsv`. "
        "Each entry compares one refresh with the previous recorded snapshot.",
        "",
    ]
    for entry in entries:
        date = entry["date"]
        prev = entry.get("prev")
        lines.append(f"## {date}" + (f" (vs {prev})" if prev else " (initial snapshot)"))
        lines.append("")
        if not prev:
            lines.append("- First recorded snapshot.")
            lines.append("")
            continue
        lines.append(f"- Added: {fmt_repo_list(entry['added'], 'none')}")
        lines.append(f"- Removed: {fmt_repo_list(entry['removed'], 'none')}")
        if "archived" in entry:
            lines.append(f"- Archived: {fmt_repo_list(entry['archived'], 'none')}")
            lines.append(f"- Renamed: {fmt_repo_list(entry['renamed'], 'none')}")
            lines.append(f"- Missing on GitHub: {fmt_repo_list(entry['missing'], 'none')}")
        gains = entry.get("gains", [])
        if gains:
            lines.append("- Top star gains:")
            for gain, repo, old, new in gains:
                lines.append(f"  - `{repo}` +{gain} ({old} -> {new})")
        else:
            lines.append("- Top star gains: none")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


# --------------------------------------------------------------------------- rendering

def notes_for(row: dict[str, str], locale: str) -> str:
    if locale == "zh":
        text = row.get("notes_zh") or row.get("notes") or row.get("description")
    else:
        text = row.get("notes") or row.get("description")
    return clean_cell(text)


def render_table(rows: list[dict[str, str]], locale: str) -> list[str]:
    L = LOCALES[locale]
    lines = [L["table_header"], L["table_divider"]]
    for row in sorted(rows, key=lambda item: (-star_int(item), item.get("repo", "").lower())):
        repo = row.get("repo", "").strip()
        url = row.get("url", "").strip() or f"https://github.com/{repo}"
        name = f"[{repo}]({url})"
        if row.get("archived") == "yes":
            name += f" {L['archived']}"
        pushed = row.get("pushed_at", "").strip() or row.get("updated_at", "").strip()
        stars = L["pending"] if row.get("status") == "pending" else str(star_int(row))
        lines.append(f"| {name} | {row.get('type', '').strip()} | {stars} | {pushed} | {notes_for(row, locale)} |")
    return lines


def render_sections(rows: list[dict[str, str]], cfg: dict, locale: str) -> list[str]:
    lines: list[str] = []
    for category in cfg["category_order"]:
        group = [row for row in rows if row.get("category") == category]
        if not group:
            continue
        heading = category if locale == "en" else cfg["category_zh"][category]
        lines.extend([f"## {heading}", ""])
        lines.extend(render_table(group, locale))
        lines.append("")
    return lines


def render_policy(cfg: dict, locale: str) -> list[str]:
    policy = cfg["policy"]
    lines = [policy["include"]["heading"][locale], ""]
    lines.extend(f"- {item}" for item in policy["include"][locale])
    lines.append("")
    lines.extend([policy["stopping"]["heading"][locale], "", policy["stopping"][locale], ""])
    return lines


def load_last_refresh(path: Path | None = None) -> dict[str, object]:
    path = path or LAST_REFRESH_PATH
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def render_body(rows: list[dict[str, str]], cfg: dict, locale: str, refresh_info: dict[str, object], entries: list[dict[str, object]]) -> str:
    L = LOCALES[locale]
    categories = {row.get("category") for row in rows}
    lines = [
        L["refreshed"].format(date=refresh_info.get("date", "unknown"), count=len(rows), ncat=len(categories)),
        "",
    ]
    pending = sum(1 for row in rows if row.get("status") == "pending")
    if pending:
        lines.insert(1, "")
        lines.insert(1, L["pending_note"].format(count=pending))
    lines.extend(render_recent_changes(entries, locale))
    lines.extend(render_sections(rows, cfg, locale))
    lines.extend(render_policy(cfg, locale))
    return "\n".join(lines).rstrip()


def extract_body(text: str, path: Path) -> tuple[str, str, str]:
    if MARK_START not in text or MARK_END not in text:
        raise SystemExit(f"{path} is missing the {MARK_START} / {MARK_END} markers")
    start = text.index(MARK_START) + len(MARK_START)
    end = text.index(MARK_END)
    return text[:start], text[start:end].strip(), text[end:]


def inject(path: Path, body: str) -> None:
    text = path.read_text(encoding="utf-8")
    head, _, tail = extract_body(text, path)
    path.write_text(f"{head}\n{body}\n{tail}", encoding="utf-8")


def export_json(rows: list[dict[str, str]], cfg: dict, refresh_info: dict[str, object], path: Path | None = None) -> None:
    path = path or JSON_PATH
    def convert(row: dict[str, str]) -> dict[str, object]:
        item: dict[str, object] = dict(row)
        for key in ("stars", "forks", "open_issues"):
            item[key] = int(row[key]) if str(row.get(key, "")).isdigit() else None
        for key in ("interfaces", "hosts", "topics"):
            item[key] = split_list(row.get(key, ""))
        item["archived"] = row.get("archived") == "yes"
        item["pinned"] = row.get("pinned") == "yes"
        item["listed_in"] = int(row["listed_in"]) if str(row.get("listed_in", "")).isdigit() else 0
        return item

    payload = {
        "schema_version": cfg.get("schema_version", 2),
        "refreshed_at": refresh_info.get("refreshed_at"),
        "categories": cfg["categories"],
        "types": cfg["types"],
        "repos": [convert(row) for row in rows],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def render_outputs(rows: list[dict[str, str]], cfg: dict) -> None:
    refresh_info = load_last_refresh()
    history = load_history()
    entries = compute_changes(history, rows, limit=CHANGELOG_ENTRIES)
    inject(README_PATH, render_body(rows, cfg, "en", refresh_info, entries))
    inject(README_ZH_PATH, render_body(rows, cfg, "zh", refresh_info, entries))
    inject(CATALOG_PATH, render_body(rows, cfg, "en", refresh_info, entries))
    CHANGELOG_PATH.write_text(render_changelog(entries), encoding="utf-8")
    export_json(rows, cfg, refresh_info)


def render_report(report: dict[str, object]) -> str:
    lines = [
        "# Refresh report",
        "",
        f"- Refreshed at: {report.get('refreshed_at')}",
        f"- Fetched: {report.get('fetched')}, cached: {report.get('cached')}, missing: {report.get('missing')}",
        f"- Renamed: {', '.join(report.get('renamed', [])) or 'none'}",
        f"- Archived: {', '.join(report.get('archived', [])) or 'none'}",
        f"- Rate limited: {'yes' if report.get('rate_limited') else 'no'}",
        "",
        "## Warnings",
        "",
    ]
    warnings = report.get("warnings", [])
    lines.extend(f"- {warning}" for warning in warnings) if warnings else lines.append("- none")
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- validation

def is_untranslated(row: dict[str, str]) -> bool:
    notes_zh = row.get("notes_zh", "").strip()
    return bool(notes_zh) and notes_zh == row.get("notes", "").strip() and not CJK_RE.search(notes_zh)


def check_catalog(seed_rows: list[dict[str, str]], curated: list[dict[str, str]], cfg: dict, strict: bool = False) -> int:
    errors: list[str] = []
    warnings: list[str] = []
    today = dt.date.fromisoformat(today_utc())

    # seed
    seen: set[str] = set()
    pinned: list[str] = []
    for row in seed_rows:
        repo = row["repo"]
        if not repo:
            errors.append("seed: blank repo field")
            continue
        if repo.lower() in seen:
            errors.append(f"seed: duplicate repo {repo}")
        seen.add(repo.lower())
        if row["category"] not in cfg["category_order"]:
            errors.append(f"seed: unknown category for {repo}: {row['category']}")
        if row["type"] not in cfg["type_keys"]:
            errors.append(f"seed: unknown type for {repo}: {row['type']!r} (allowed: {', '.join(cfg['type_keys'])})")
        for field, allowed in (("interfaces", cfg["interfaces"]), ("hosts", cfg["hosts"])):
            bad = [item for item in split_list(row[field]) if item not in allowed]
            if bad:
                errors.append(f"seed: unknown {field} for {repo}: {bad}")
        if row["domain"] and row["domain"] not in cfg["domains"]:
            errors.append(f"seed: unknown domain for {repo}: {row['domain']}")
        if row["pinned"] not in {"", "yes", "no"}:
            errors.append(f"seed: pinned must be yes/no for {repo}")
        if row["include"].lower() not in {"yes", "no"}:
            errors.append(f"seed: include must be yes/no for {repo}")
        if row["include"].lower() == "yes":
            if not row["notes"]:
                errors.append(f"seed: missing English notes for {repo}")
            if not row["notes_zh"]:
                errors.append(f"seed: missing Chinese notes for {repo}")
            if row["pinned"] == "yes":
                pinned.append(repo)

    # curated vs seed
    untranslated: list[str] = []
    active = {row["repo"].lower(): row for row in active_seed(seed_rows)}
    curated_by_repo: dict[str, dict[str, str]] = {}
    for row in curated:
        key = row.get("repo", "").lower()
        if key in curated_by_repo:
            errors.append(f"curated: duplicate repo {row['repo']}")
        curated_by_repo[key] = row
        if key not in active:
            errors.append(f"curated: {row['repo']} is not an active seed repo (run --from-curated)")
            continue
        seed = active[key]
        for field in SEED_TO_CURATED:
            if clean_cell(row.get(field, "")) != clean_cell(seed.get(field, "")):
                errors.append(f"curated: {row['repo']} field {field} differs from seed (run --from-curated)")
                break
        if not row.get("url", "").startswith("https://github.com/"):
            errors.append(f"curated: bad GitHub URL for {row['repo']}: {row.get('url', '')}")
        status = row.get("status", "")
        if status not in STATUS_VALUES:
            errors.append(f"curated: bad status for {row['repo']}: {status!r}")
        if status == "pending":
            warnings.append(f"curated: {row['repo']} is pending its first GitHub refresh")
        if status == "missing":
            since = row.get("missing_since", "")
            if not row.get("fetched_at"):
                errors.append(f"curated: {row['repo']} has never been fetched from GitHub (typo in seed?)")
            else:
                try:
                    age = (today - dt.date.fromisoformat(since)).days
                except ValueError:
                    age = MISSING_GRACE_DAYS + 1
                if age > MISSING_GRACE_DAYS:
                    errors.append(f"curated: {row['repo']} missing on GitHub since {since}; remove it or fix the seed")
                else:
                    warnings.append(f"curated: {row['repo']} missing on GitHub since {since}")
        if row.get("renamed_to"):
            warnings.append(f"curated: {row['repo']} was renamed to {row['renamed_to']}; update the seed")
        if is_untranslated(row):
            untranslated.append(row["repo"])
    for key, seed in active.items():
        if key not in curated_by_repo:
            errors.append(f"curated: {seed['repo']} missing (run --refresh --repos {seed['repo']})")
    for repo in cfg.get("pinned_repos", []):
        seed = active.get(repo.lower())
        if not seed:
            errors.append(f"pinned repo missing from seed: {repo} (listed in catalog_config.json pinned_repos)")
        elif seed.get("pinned") != "yes":
            errors.append(f"pinned repo {repo} must have pinned=yes in the seed")
        elif repo not in pinned:
            pinned.append(repo)
    for repo in pinned:
        if repo.lower() not in curated_by_repo:
            errors.append(f"pinned repo missing from curated: {repo}")
    if untranslated:
        shown = ", ".join(untranslated[:8]) + (f", ... (+{len(untranslated) - 8} more)" if len(untranslated) > 8 else "")
        warnings.append(f"curated: notes_zh identical to the English notes for {len(untranslated)} repos: {shown}")

    # policy document mentions every category
    if POLICY_DOC_PATH.exists():
        policy_text = POLICY_DOC_PATH.read_text(encoding="utf-8")
        for category in cfg["category_order"]:
            if f"`{category}`" not in policy_text:
                errors.append(f"policy doc missing category label: {category}")
    else:
        errors.append(f"missing policy document: {POLICY_DOC_PATH}")

    # rendered outputs
    refresh_info = load_last_refresh()
    entries = compute_changes(load_history(), curated, limit=CHANGELOG_ENTRIES)
    for path, label, locale in ((README_PATH, "README", "en"), (README_ZH_PATH, "README-zh", "zh"), (CATALOG_PATH, "catalog", "en")):
        if not path.exists():
            errors.append(f"missing {label}: {path}")
            continue
        text = path.read_text(encoding="utf-8")
        if MARK_START not in text or MARK_END not in text:
            errors.append(f"{label} missing {MARK_START}/{MARK_END} markers")
            continue
        _, body, _ = extract_body(text, path)
        expected = render_body(curated, cfg, locale, refresh_info, entries)
        if body != expected:
            errors.append(f"{label} is stale: run --from-curated (or --refresh) to regenerate")
        for old in OLD_TABLE_HEADERS:
            if old in text:
                errors.append(f"{label} still contains an old table header: {old}")
        for repo in pinned:
            if repo not in text:
                errors.append(f"{label} missing pinned repo {repo}")
    for path in (JSON_PATH, CHANGELOG_PATH):
        if not path.exists():
            errors.append(f"missing generated file: {path} (run --from-curated)")

    if strict:
        errors.extend(f"strict: {warning}" for warning in warnings)
        warnings = []
    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    categories = {row.get("category") for row in curated}
    print(f"ok: {len(curated)} repos across {len(categories)} categories; {len(warnings)} warnings")
    return 0


def summary_line(info: dict[str, object]) -> str:
    if not info:
        return "Weekly refresh: no refresh recorded"
    return (
        f"Weekly refresh {info.get('date')}: {info.get('repos')} repos "
        f"(+{info.get('added', 0)}/-{info.get('removed', 0)}), {info.get('renamed', 0)} renamed, "
        f"{info.get('archived', 0)} archived, {info.get('missing', 0)} missing, {info.get('cached', 0)} cached"
    )


# --------------------------------------------------------------------------- main

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Update, render, and validate the catalog.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--refresh", action="store_true", help="Fetch GitHub metadata, append history, render, check")
    mode.add_argument("--from-curated", action="store_true", help="Merge seed into cached metadata and render without network")
    mode.add_argument("--check", action="store_true", help="Validate data and rendered outputs without network")
    mode.add_argument("--summary", action="store_true", help="Print a one-line summary of the last refresh")
    parser.add_argument("--repos", default="", help="With --refresh: comma-separated subset of repos to fetch")
    parser.add_argument("--delay", type=float, default=0.0, help="Delay between GitHub API calls during --refresh")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors during --check")
    args = parser.parse_args(argv)

    if args.summary:
        print(summary_line(load_last_refresh()))
        return 0

    cfg = load_config()
    seed_rows = read_seed()
    active = active_seed(seed_rows)
    awesome_refs = load_awesome_refs()

    if args.refresh:
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        existing = {row["repo"].lower(): row for row in read_tsv(CURATED_PATH)} if CURATED_PATH.exists() else {}
        only = {item.strip().lower() for item in args.repos.split(",") if item.strip()} or None
        rows, report = refresh_from_github(active, existing, token, args.delay, only)
        for row in rows:
            row["listed_in"] = awesome_refs.get(row["repo"].lower(), row.get("listed_in", ""))
        history = load_history()
        previous_dates = sorted(history)
        previous = history[previous_dates[-1]] if previous_dates else {}
        append_history(history, rows, report["date"])
        write_history(history)
        current = history[report["date"]]
        info = {
            "refreshed_at": report["refreshed_at"], "date": report["date"], "repos": len(rows),
            "fetched": report["fetched"], "cached": report["cached"], "missing": report["missing"],
            "renamed": len(report["renamed"]), "archived": len(report["archived"]),
            "added": len(set(current) - set(previous)) if previous else 0,
            "removed": len(set(previous) - set(current)) if previous else 0,
            "rate_limited": report["rate_limited"],
        }
        LAST_REFRESH_PATH.write_text(json.dumps(info, indent=2) + "\n", encoding="utf-8")
        REPORT_PATH.write_text(render_report(report), encoding="utf-8")
        write_tsv(CURATED_PATH, CURATED_FIELDS, rows)
        for warning in report["warnings"]:
            print(f"warning: {warning}", file=sys.stderr)
        render_outputs(rows, cfg)
        return check_catalog(seed_rows, rows, cfg, args.strict)

    curated = read_tsv(CURATED_PATH)
    if args.from_curated:
        by_repo = {row["repo"].lower(): row for row in curated}
        rows = []
        for seed in active:
            old = by_repo.get(seed["repo"].lower())
            if old:
                row = {field: old.get(field, "") for field in CURATED_FIELDS}
                merge_seed(row, seed)
            else:
                row = blank_row(seed)
                row["status"] = "pending"
                print(f"warning: {seed['repo']} has no cached metadata yet (pending first --refresh)", file=sys.stderr)
            row["listed_in"] = awesome_refs.get(seed["repo"].lower(), row.get("listed_in", ""))
            rows.append(row)
        rows = sort_by_repo(rows)
        write_tsv(CURATED_PATH, CURATED_FIELDS, rows)
        render_outputs(rows, cfg)
        return check_catalog(seed_rows, rows, cfg, args.strict)

    return check_catalog(seed_rows, sort_by_repo(curated), cfg, args.strict)


if __name__ == "__main__":
    raise SystemExit(main())
