#!/usr/bin/env python3
"""Discover candidate GitHub repositories that are not yet in the seed catalog.

Sources
-------
1. GitHub Search queries listed in ``data/discovery_queries.tsv`` (query, target_category, sort).
2. Cross-references from the directories already in the catalog: README links of seed rows whose
   ``type`` is ``directory`` or ``registry``.

State files
-----------
``data/candidates_seen.tsv``  every candidate ever reported, with first_seen / last_seen / times_seen.
``data/triage.tsv``           human decisions (accept / reject / defer) with a reason; rejected and
                              accepted repos are suppressed from future reports.
``data/awesome_refs.tsv``     for seeded repos, how many catalog directories reference them.

Output
------
``discovery/candidates.md``   "new this run" and "seen before" tables for manual review.

``--offline`` re-renders the report from the state files without touching the network.
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
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SEED_PATH = DATA / "repos.seed.tsv"
QUERIES_PATH = DATA / "discovery_queries.tsv"
SEEN_PATH = DATA / "candidates_seen.tsv"
TRIAGE_PATH = DATA / "triage.tsv"
AWESOME_REFS_PATH = DATA / "awesome_refs.tsv"
AWESOME_CACHE_PATH = DATA / "awesome_refs_cache.tsv"
DEFAULT_OUTPUT = ROOT / "discovery" / "candidates.md"
USER_AGENT = "research-bioinfo-ai-repos-discovery"

SEEN_FIELDS = [
    "repo", "url", "first_seen", "last_seen", "times_seen", "max_stars", "last_stars", "pushed_at",
    "language", "suggested_category", "suggested_type", "sources", "description",
]
TRIAGE_FIELDS = ["repo", "decision", "reason", "date"]
AWESOME_FIELDS = ["repo", "listed_in", "lists"]
AWESOME_CACHE_FIELDS = ["repo", "checked_on", "relevant", "stars", "pushed_at", "language", "description"]
AWESOME_CACHE_DAYS = 90
TRIAGE_DECISIONS = {"accept", "reject", "defer"}
MAX_SEEN_ROWS = 250

TABLE_HEADER = "| repo | suggested category | suggested type | stars | last push | first seen | seen | sources | description |"
TABLE_DIVIDER = "|---|---|---|---:|---|---|---:|---|---|"

DOMAIN_TERMS = [
    # life sciences
    "protein", "proteomics", "alphafold", "boltz", "macromnex", "pdb", "pdbe", "uniprot", "biomolecular",
    "biologics", "antibody", "nanobody", "binder", "drug discovery", "cheminformatics", "bioinformatics",
    "bioinformatic", "genomics", "genomic", "genome", "single-cell", "single cell", "scrna", "omics",
    "transcriptom", "spatial", "biomedical", "medical", "medicine", "clinical", "life-science", "life science",
    "biology", "biological", "bio ", "bio-", "-bio", "/bio", "bioskill", "biopython", "ensembl", "chembl", "pubchem", "kegg", "reactome",
    "string-db", "opentargets", "open targets", "clinvar", "gnomad", "gwas", "ncbi", "nextflow", "nf-core",
    "galaxy", "snakemake", "samtools", "bcftools", "blast", "bwa", "igv", "jbrowse", "pymol", "chimerax",
    "molecular", "pharmacolog", "fda", "trials", "crispr", "sequencing",
    # research and literature
    "research", "academic", "scientific", "science", "scholar", "paper", "literature", "citation", "arxiv",
    "pubmed", "biorxiv", "medrxiv", "zotero", "mendeley", "endnote", "cnki", "openalex", "crossref",
    "europe pmc", "manuscript", "latex", "thesis", "journal", "peer review", "phd",
]
INTERFACE_TERMS = ["mcp", "skill", "plugin", "agent", "claude", "codex", "cursor", "gemini", "llm", "copilot", "workflow", "server", "tool", "assistant", "openclaw"]
DISCOVERY_TERMS = ["awesome", "directory", "catalog", "registry", "benchmark", "curated"]
NON_REPO_OWNERS = {
    "about", "apps", "blog", "collections", "contact", "customer-stories", "enterprise", "events", "explore",
    "features", "github", "issues", "login", "marketplace", "new", "notifications", "orgs", "pricing", "pulls",
    "readme", "search", "security", "settings", "site", "sponsors", "team", "topics", "trending", "users",
    "settings", "join", "signup", "sessions", "watching", "stars", "dashboard", "codespaces", "pages",
}
GITHUB_LINK_RE = re.compile(r"github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)")


# --------------------------------------------------------------------------- io helpers

def today_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")


def clean_cell(value: object) -> str:
    return str(value or "").replace("\t", " ").replace("\r", " ").replace("\n", " ").replace("|", "/").strip()


def as_int(value: object) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as fh:
        return [dict(row) for row in csv.DictReader(fh, delimiter="\t")]


def write_tsv(path: Path, fields: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: clean_cell(row.get(field, "")) for field in fields})


def read_seed_rows(path: Path = SEED_PATH) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"Missing seed file: {path}")
    return [row for row in read_tsv(path) if row.get("repo", "").strip()]


def seed_keys(rows: Iterable[dict[str, str]]) -> set[str]:
    return {row["repo"].strip().lower() for row in rows}


def read_queries(path: Path = QUERIES_PATH) -> list[dict[str, str]]:
    rows = [row for row in read_tsv(path) if row.get("query", "").strip()]
    for row in rows:
        row["sort"] = (row.get("sort") or "stars").strip()
    return rows


def read_triage(path: Path = TRIAGE_PATH) -> dict[str, dict[str, str]]:
    return {row["repo"].strip().lower(): row for row in read_tsv(path) if row.get("repo", "").strip()}


def read_seen(path: Path = SEEN_PATH) -> dict[str, dict[str, str]]:
    return {row["repo"].strip().lower(): row for row in read_tsv(path) if row.get("repo", "").strip()}


# --------------------------------------------------------------------------- GitHub

def github_headers(token: str | None, accept: str = "application/vnd.github+json") -> dict[str, str]:
    headers = {"Accept": accept, "User-Agent": USER_AGENT}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def github_json(url: str, token: str | None) -> dict[str, object]:
    req = Request(url, headers=github_headers(token))
    with urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def search_repositories(query: str, limit: int, sort: str, token: str | None) -> list[dict[str, object]]:
    params = urlencode({"q": query, "sort": sort, "order": "desc", "per_page": str(limit)})
    data = github_json(f"https://api.github.com/search/repositories?{params}", token)
    items = data.get("items", [])
    return items if isinstance(items, list) else []


def fetch_repo_meta(repo: str, token: str | None) -> dict[str, object]:
    return github_json(f"https://api.github.com/repos/{repo}", token)


def fetch_readme(repo: str, token: str | None) -> str:
    req = Request(f"https://api.github.com/repos/{repo}/readme", headers=github_headers(token, "application/vnd.github.raw+json"))
    with urlopen(req, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


# --------------------------------------------------------------------------- classification

def has_any(text: str, terms: list[str]) -> bool:
    return any(term in text for term in terms)


def is_relevant_candidate(repo: str, description: str) -> bool:
    lowered = f"{repo} {description}".lower()
    if "proteinmcp" in lowered:
        return True
    if not has_any(lowered, DOMAIN_TERMS):
        return False
    return has_any(lowered, INTERFACE_TERMS) or has_any(lowered, DISCOVERY_TERMS)


def suggest_category(repo: str, text: str, fallback: str = "General Research / AI4S Skill Suites") -> str:
    lowered = f"{repo} {text}".lower()
    rules = [
        (["zotero", "mendeley", "endnote", "cnki", "reference manag"], "Zotero / CNKI / Google Scholar / Reference Management"),
        (["pubmed", "arxiv", "semantic scholar", "openalex", "crossref", "biorxiv", "medrxiv", "europe pmc", "scholar", "literature search", "paper search"], "Literature Search / Scholarly Search MCP"),
        (["paper writing", "academic writing", "peer review", "manuscript", "latex"], "Paper Writing / Peer Review / Submission Skills"),
        (["protein", "pdb", "pdbe", "alphafold", "boltz", "folding", "rfdiffusion", "proteinmpnn", "pymol", "chimerax", "macromnex", "binder", "antibody", "nanobody"], "Protein Design / Structural Biology"),
        (["nextflow", "nf-core", "galaxy", "snakemake", "samtools", "bcftools", "blast", "bwa", "biopython", "igv", "jbrowse", "pipeline"], "Pipelines / Sequence & Genome Tool MCP"),
        (["uniprot", "chembl", "pubchem", "opentargets", "open targets", "kegg", "reactome", "string", "ensembl", "clinvar", "gnomad", "gwas", "ncbi", "database"], "Biological Databases / Pathways / Chemistry / Drug Discovery MCP"),
        (["clinical", "medical", "medicine", "fda", "trial", "healthcare", "patient", "drug"], "Biomedical / Clinical / Medical Research"),
        (["proteomics", "genom", "omics", "single-cell", "single cell", "scrna", "bioinformatic", "sequenc", "spatial"], "Bioinformatics / Omics / Single-Cell Skills"),
        (["awesome", "catalog", "registry", "directory", "curated list"], "Awesome Lists / Registries / Further Discovery"),
        (["figure", "plot", "diagram", "pdf", "translate"], "Figures / PDF / LaTeX / Research Artifact Tools"),
        (["scientist", "co-scientist", "research assistant", "workspace", "autonomous research"], "Research Agent Apps / Workspaces"),
    ]
    for terms, category in rules:
        if any(term in lowered for term in terms):
            return category
    return fallback


def suggest_type(repo: str, text: str) -> str:
    lowered = f"{repo} {text}".lower()
    if "awesome" in lowered or "curated list" in lowered:
        return "directory"
    if "registry" in lowered or "marketplace" in lowered:
        return "registry"
    if "mcp" in lowered:
        return "mcp-server"
    if "skills" in lowered:
        return "skill-suite"
    if "skill" in lowered:
        return "skill"
    if "plugin" in lowered:
        return "plugin"
    if any(term in lowered for term in ["agent", "assistant", "workflow", "scientist"]):
        return "agent-app"
    return "tool"


def extract_github_repos(text: str) -> set[str]:
    repos: set[str] = set()
    for owner, name in GITHUB_LINK_RE.findall(text):
        if owner.lower() in NON_REPO_OWNERS:
            continue
        name = re.sub(r"\.git$", "", name).rstrip(".,;:)")
        if not name or name.lower() in {"blob", "tree", "issues", "pull", "wiki", "releases", "actions"}:
            continue
        repos.add(f"{owner}/{name}")
    return repos


# --------------------------------------------------------------------------- discovery

def run_searches(queries: list[dict[str, str]], limit: int, min_stars: int, include_forks: bool,
                 include_broad: bool, delay: float, token: str | None, searcher=search_repositories,
                 max_queries: int | None = None) -> tuple[dict[str, dict[str, object]], list[str], int]:
    seen_queries: set[tuple[str, str]] = set()
    found: dict[str, dict[str, object]] = {}
    warnings: list[str] = []
    hits = 0
    for index, item in enumerate(queries):
        if max_queries is not None and index >= max_queries:
            break
        key = (item["query"], item["sort"])
        if key in seen_queries:
            continue
        seen_queries.add(key)
        try:
            results = searcher(item["query"], limit, item["sort"], token)
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
            warnings.append(f"{item['query']} [{item['sort']}]: {exc}")
            if isinstance(exc, HTTPError) and exc.code in (403, 429):
                time.sleep(max(delay, 5.0))
            continue
        for result in results:
            repo = clean_cell(result.get("full_name"))
            if not repo or result.get("archived") or result.get("disabled"):
                continue
            if result.get("fork") and not include_forks:
                continue
            stars = as_int(result.get("stargazers_count"))
            if stars < min_stars:
                continue
            description = clean_cell(result.get("description"))
            if not include_broad and not is_relevant_candidate(repo, description):
                continue
            hits += 1
            source = f"search:{item['query']}"
            record = found.get(repo.lower())
            if record:
                sources = record["sources"]
                if isinstance(sources, list) and source not in sources:
                    sources.append(source)
                continue
            found[repo.lower()] = {
                "repo": repo,
                "url": clean_cell(result.get("html_url")) or f"https://github.com/{repo}",
                "stars": stars,
                "pushed_at": clean_cell(result.get("pushed_at"))[:10],
                "language": clean_cell(result.get("language")),
                "suggested_category": item.get("target_category") or suggest_category(repo, description),
                "suggested_type": suggest_type(repo, description),
                "sources": [source],
                "description": description,
            }
        if delay:
            time.sleep(delay)
    return found, warnings, hits


def run_awesome_crossref(seed_rows: list[dict[str, str]], token: str | None, delay: float,
                         reader=fetch_readme) -> tuple[dict[str, set[str]], list[str]]:
    """Return {referenced_repo_lower: {list_repo, ...}} for every directory/registry in the seed."""
    refs: dict[str, set[str]] = {}
    warnings: list[str] = []
    directories = [
        row["repo"] for row in seed_rows
        if row.get("type", "").strip() in {"directory", "registry"} and (row.get("include") or "yes").lower() == "yes"
    ]
    for list_repo in directories:
        try:
            text = reader(list_repo, token)
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            warnings.append(f"awesome:{list_repo}: {exc}")
            continue
        for repo in extract_github_repos(text):
            if repo.lower() == list_repo.lower():
                continue
            refs.setdefault(repo.lower(), set()).add(list_repo)
        if delay:
            time.sleep(delay)
    return refs, warnings


def read_awesome_cache(path: Path = AWESOME_CACHE_PATH) -> dict[str, dict[str, str]]:
    return {row["repo"].strip().lower(): row for row in read_tsv(path) if row.get("repo", "").strip()}


def write_awesome_cache(cache: dict[str, dict[str, str]], path: Path = AWESOME_CACHE_PATH) -> None:
    write_tsv(path, AWESOME_CACHE_FIELDS, sorted(cache.values(), key=lambda row: row.get("repo", "").lower()))


def cache_is_fresh(row: dict[str, str] | None, today: str) -> bool:
    if not row or not row.get("checked_on"):
        return False
    try:
        age = (dt.date.fromisoformat(today) - dt.date.fromisoformat(row["checked_on"])).days
    except ValueError:
        return False
    return 0 <= age <= AWESOME_CACHE_DAYS


def enrich_awesome_refs(refs: dict[str, set[str]], skip: set[str], cache: dict[str, dict[str, str]], today: str,
                        token: str | None, fetch_limit: int, delay: float = 0.0, fetcher=fetch_repo_meta,
                        min_lists: int = 2) -> dict[str, dict[str, object]]:
    """Turn awesome-list references into candidate records.

    References are checked against GitHub (budgeted by ``fetch_limit``) so relevance can use the real
    description instead of the repo name alone; results are cached for ``AWESOME_CACHE_DAYS`` days.
    Without budget or cache, a reference is kept only when its name looks relevant or it appears in at
    least ``min_lists`` directories.
    """
    found: dict[str, dict[str, object]] = {}
    pending = [key for key in refs if key not in skip]
    # check multi-listed and name-relevant references first
    pending.sort(key=lambda key: (-len(refs[key]), not is_relevant_candidate(key, ""), key))
    budget = fetch_limit
    for key in pending:
        lists = refs[key]
        row = cache.get(key)
        if not cache_is_fresh(row, today) and budget > 0:
            budget -= 1
            try:
                meta = fetcher(key, token)
                archived = bool(meta.get("archived") or meta.get("disabled"))
                description = clean_cell(meta.get("description"))
                relevant = (not archived) and (is_relevant_candidate(key, description) or len(lists) >= min_lists)
                row = {
                    "repo": clean_cell(meta.get("full_name")) or key,
                    "checked_on": today,
                    "relevant": "yes" if relevant else "no",
                    "stars": str(as_int(meta.get("stargazers_count"))),
                    "pushed_at": clean_cell(meta.get("pushed_at"))[:10],
                    "language": clean_cell(meta.get("language")),
                    "description": description,
                }
            except HTTPError as exc:
                row = {"repo": key, "checked_on": today, "relevant": "no", "stars": "", "pushed_at": "", "language": "",
                       "description": f"HTTP {exc.code}"}
            except (URLError, TimeoutError, json.JSONDecodeError, OSError):
                row = None
            if row:
                cache[key] = row
            if delay:
                time.sleep(delay)
        if row and row.get("checked_on"):
            if row.get("relevant") != "yes":
                continue
            stars: object = row.get("stars", "")
            pushed_at = row.get("pushed_at", "")
            language = row.get("language", "")
            description = row.get("description", "")
            repo_name = row.get("repo") or key
        else:
            if not (len(lists) >= min_lists or is_relevant_candidate(key, "")):
                continue
            stars, pushed_at, language, description, repo_name = "", "", "", "", key
        found[key] = {
            "repo": repo_name,
            "url": f"https://github.com/{repo_name}",
            "stars": stars,
            "pushed_at": pushed_at,
            "language": language,
            "suggested_category": suggest_category(repo_name, description),
            "suggested_type": suggest_type(repo_name, description),
            "sources": [f"awesome:{name}" for name in sorted(lists, key=str.lower)],
            "description": description,
        }
    return found


def merge_candidates(found: dict[str, dict[str, object]], extra: dict[str, dict[str, object]]) -> None:
    for key, record in extra.items():
        existing = found.get(key)
        if not existing:
            found[key] = record
            continue
        sources = existing["sources"]
        if isinstance(sources, list):
            sources.extend(source for source in record["sources"] if source not in sources)
        for field in ("stars", "pushed_at", "language", "description"):
            if not existing.get(field) and record.get(field):
                existing[field] = record[field]


def update_seen(seen: dict[str, dict[str, str]], found: dict[str, dict[str, object]], today: str) -> None:
    """Merge this run's candidates into the seen table; times_seen grows at most once per run date."""
    for key, record in found.items():
        stars = record.get("stars")
        stars_text = str(stars) if stars not in ("", None) else ""
        sources = record.get("sources", [])
        source_list = list(sources) if isinstance(sources, list) else [s for s in str(sources).split("; ") if s]
        row = seen.get(key)
        if row is None:
            seen[key] = {
                "repo": str(record["repo"]),
                "url": str(record["url"]),
                "first_seen": today,
                "last_seen": today,
                "times_seen": "1",
                "max_stars": stars_text,
                "last_stars": stars_text,
                "pushed_at": str(record.get("pushed_at", "")),
                "language": str(record.get("language", "")),
                "suggested_category": str(record.get("suggested_category", "")),
                "suggested_type": str(record.get("suggested_type", "")),
                "sources": "; ".join(source_list),
                "description": str(record.get("description", "")),
            }
            continue
        if row.get("last_seen") != today:
            row["times_seen"] = str(as_int(row.get("times_seen")) + 1)
        row["last_seen"] = today
        if stars_text:
            row["last_stars"] = stars_text
            row["max_stars"] = str(max(as_int(row.get("max_stars")), as_int(stars_text)))
        for field in ("pushed_at", "language", "description"):
            if record.get(field):
                row[field] = str(record[field])
        for field in ("suggested_category", "suggested_type"):
            if not row.get(field):
                row[field] = str(record.get(field, ""))
        merged = [item for item in row.get("sources", "").split("; ") if item]
        merged.extend(item for item in source_list if item not in merged)
        row["sources"] = "; ".join(merged)


def write_seen(seen: dict[str, dict[str, str]], path: Path = SEEN_PATH) -> None:
    rows = sorted(seen.values(), key=lambda row: (row.get("first_seen", ""), row.get("repo", "").lower()))
    write_tsv(path, SEEN_FIELDS, rows)


def write_awesome_refs(refs: dict[str, set[str]], seed_rows: list[dict[str, str]], path: Path = AWESOME_REFS_PATH) -> None:
    rows = []
    for row in seed_rows:
        key = row["repo"].strip().lower()
        lists = sorted(refs.get(key, set()), key=str.lower)
        rows.append({"repo": row["repo"].strip(), "listed_in": str(len(lists)), "lists": "; ".join(lists)})
    write_tsv(path, AWESOME_FIELDS, rows)


# --------------------------------------------------------------------------- rendering

def compact_sources(text: str, limit: int = 3) -> str:
    items = [item for item in text.split("; ") if item]
    shown = items[:limit]
    extra = len(items) - len(shown)
    rendered = "; ".join(shown)
    return f"{rendered} (+{extra} more)" if extra > 0 else rendered


def safe_description(text: str) -> str:
    """Keep descriptions from being mistaken for repo cells: drop markdown link syntax."""
    text = re.sub(r"\[([^\]]*)\]\(([^)]*)\)", r"\1 (\2)", text)
    return text


def render_row(row: dict[str, str]) -> str:
    repo = clean_cell(row.get("repo"))
    url = clean_cell(row.get("url")) or f"https://github.com/{repo}"
    stars = clean_cell(row.get("last_stars")) or "?"
    return "| " + " | ".join([
        f"[{repo}]({url})",
        clean_cell(row.get("suggested_category")),
        clean_cell(row.get("suggested_type")),
        stars,
        clean_cell(row.get("pushed_at")),
        clean_cell(row.get("first_seen")),
        clean_cell(row.get("times_seen")) or "1",
        compact_sources(clean_cell(row.get("sources"))),
        safe_description(clean_cell(row.get("description"))),
    ]) + " |"


def sort_key(row: dict[str, str]) -> tuple:
    return (row.get("last_seen", ""), as_int(row.get("last_stars")), row.get("repo", "").lower())


def render_candidates(seen: dict[str, dict[str, str]], triage: dict[str, dict[str, str]], seeded: set[str],
                      queries: list[dict[str, str]], warnings: list[str], today: str, stats: dict[str, object],
                      output_path: Path) -> None:
    untriaged = [row for key, row in seen.items() if key not in seeded and key not in triage]
    deferred = [row for key, row in seen.items() if key not in seeded and triage.get(key, {}).get("decision") == "defer"]
    new_rows = sorted((row for row in untriaged if row.get("first_seen") == today), key=sort_key, reverse=True)
    old_rows = sorted((row for row in untriaged if row.get("first_seen") != today), key=sort_key, reverse=True)
    decisions = {"accept": 0, "reject": 0, "defer": 0}
    for row in triage.values():
        decision = row.get("decision", "").strip().lower()
        if decision in decisions:
            decisions[decision] += 1

    lines = [
        "# Discovery Candidates",
        "",
        f"Generated on: {today} (UTC)",
        "",
        "GitHub Search hits and awesome-list cross-references that are not yet in `data/repos.seed.tsv`. "
        "They are candidates only: review README evidence, scope, overlap, license, maintenance, and safety before adding "
        "an entry to the seed file. Record every decision in `data/triage.tsv` (`accept`, `reject`, or `defer` with a reason) "
        "so the repo stops reappearing here. Candidates are tracked across runs in `data/candidates_seen.tsv`.",
        "",
        f"- Queries run: {stats.get('queries', 0)} (see `data/discovery_queries.tsv`)",
        f"- Search hits after filtering: {stats.get('hits', 0)}",
        f"- Awesome-list references scanned: {stats.get('awesome_refs', 0)} from {stats.get('awesome_lists', 0)} directories",
        f"- Candidates tracked: {len(seen)} ({len(untriaged)} untriaged, {decisions['defer']} deferred, {decisions['reject']} rejected, {decisions['accept']} accepted)",
        "",
    ]
    if stats.get("offline"):
        lines.extend(["Rendered offline from the state files; no searches were run.", ""])
    if warnings:
        lines.extend(["## Search Warnings", ""])
        lines.extend(f"- `{clean_cell(warning)}`" for warning in warnings)
        lines.append("")

    def table(rows: list[dict[str, str]], empty: str) -> list[str]:
        out = [TABLE_HEADER, TABLE_DIVIDER]
        if rows:
            out.extend(render_row(row) for row in rows)
        else:
            out.append(f"| {empty} | | | | | | | | |")
        out.append("")
        return out

    lines.extend([f"## New this run ({len(new_rows)})", ""])
    lines.extend(table(new_rows, "No new candidates this run."))
    shown_old = old_rows[:MAX_SEEN_ROWS]
    suffix = f", showing {len(shown_old)}" if len(old_rows) > len(shown_old) else ""
    lines.extend([f"## Seen before, not yet triaged ({len(old_rows)}{suffix})", ""])
    lines.extend(table(shown_old, "No untriaged candidates."))
    lines.extend([f"## Deferred ({len(deferred)})", ""])
    lines.extend(table(sorted(deferred, key=sort_key, reverse=True), "No deferred candidates."))
    lines.extend(["## Queries", ""])
    lines.extend(f"- `{item['query']}` ({item['sort']}) -> {item.get('target_category', '')}" for item in queries)
    lines.append("")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")


# --------------------------------------------------------------------------- validation

def check_candidates(output_path: Path, seed_rows: list[dict[str, str]], triage: dict[str, dict[str, str]]) -> int:
    errors: list[str] = []
    if not output_path.exists():
        print(f"ERROR: missing candidate report: {output_path}", file=sys.stderr)
        return 1
    text = output_path.read_text(encoding="utf-8")
    if "# Discovery Candidates" not in text:
        errors.append("candidate report missing title")
    if "last push" not in text:
        errors.append("candidate report missing last push column")
    seeded = seed_keys(seed_rows)
    seen_in_report: set[str] = set()
    for match in re.finditer(r"^\|\s*\[([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)\]\(", text, flags=re.MULTILINE):
        key = match.group(1).lower()
        if key in seeded:
            errors.append(f"candidate report includes already seeded repo: {match.group(1)}")
        decision = triage.get(key, {}).get("decision", "").lower()
        if decision in {"reject", "accept"}:
            errors.append(f"candidate report includes {decision}ed repo: {match.group(1)}")
        if key in seen_in_report:
            errors.append(f"duplicate candidate repo: {match.group(1)}")
        seen_in_report.add(key)
    for key, row in triage.items():
        decision = row.get("decision", "").strip().lower()
        if decision not in TRIAGE_DECISIONS:
            errors.append(f"triage: bad decision for {row.get('repo')}: {decision!r}")
        if not row.get("reason", "").strip():
            errors.append(f"triage: missing reason for {row.get('repo')}")
        if decision == "accept" and key not in seeded:
            errors.append(f"triage: {row.get('repo')} is accepted but not in the seed file")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"ok: candidate report lists {len(seen_in_report)} unseeded repos; {len(triage)} triage decisions")
    return 0


# --------------------------------------------------------------------------- main

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--limit-per-query", type=int, default=30, help="GitHub Search results inspected per query")
    parser.add_argument("--min-stars", type=int, default=1, help="Minimum stars for search hits (awesome references are exempt)")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Candidate Markdown report path")
    parser.add_argument("--include-forks", action="store_true", help="Include fork repositories")
    parser.add_argument("--include-broad-matches", action="store_true", help="Keep hits that fail the relevance filter")
    parser.add_argument("--skip-awesome", action="store_true", help="Skip awesome-list cross-referencing")
    parser.add_argument("--awesome-fetch-limit", type=int, default=200, help="Max GitHub metadata lookups for awesome-list references per run")
    parser.add_argument("--max-queries", type=int, default=None, help="Only run the first N queries (debugging)")
    parser.add_argument("--delay", type=float, default=2.1, help="Delay between GitHub API calls (search allows 30/min)")
    parser.add_argument("--offline", action="store_true", help="Re-render the report from state files without network")
    parser.add_argument("--check", action="store_true", help="Validate an existing candidate report without network")
    args = parser.parse_args(argv)

    output_path = args.output if args.output.is_absolute() else ROOT / args.output
    seed_rows = read_seed_rows()
    seeded = seed_keys(seed_rows)
    triage = read_triage()
    queries = read_queries()
    if args.check:
        return check_candidates(output_path, seed_rows, triage)

    today = today_utc()
    seen = read_seen()
    warnings: list[str] = []
    stats: dict[str, object] = {"queries": len(queries), "hits": 0, "awesome_refs": 0, "awesome_lists": 0, "offline": args.offline}
    if not args.offline:
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        found, search_warnings, hits = run_searches(
            queries, args.limit_per_query, args.min_stars, args.include_forks, args.include_broad_matches,
            args.delay, token, max_queries=args.max_queries,
        )
        warnings.extend(search_warnings)
        stats["hits"] = hits
        found = {key: record for key, record in found.items() if key not in seeded}
        if not args.skip_awesome:
            refs, awesome_warnings = run_awesome_crossref(seed_rows, token, min(args.delay, 1.0))
            warnings.extend(awesome_warnings)
            stats["awesome_refs"] = len(refs)
            stats["awesome_lists"] = len({name for lists in refs.values() for name in lists})
            cache = read_awesome_cache()
            skip = seeded | {key for key, row in triage.items() if row.get("decision", "").lower() in {"reject", "accept"}}
            extra = enrich_awesome_refs(refs, skip, cache, today, token, args.awesome_fetch_limit, min(args.delay, 0.5))
            write_awesome_cache(cache)
            merge_candidates(found, extra)
            write_awesome_refs(refs, seed_rows)
        update_seen(seen, found, today)
        write_seen(seen)
    render_candidates(seen, triage, seeded, queries, warnings, today, stats, output_path)
    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    return check_candidates(output_path, seed_rows, triage)


if __name__ == "__main__":
    raise SystemExit(main())
