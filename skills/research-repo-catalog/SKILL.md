---
name: research-repo-catalog
description: Maintain and update a curated GitHub catalog of AI-agent-related research, academic writing, literature search, Zotero, PubMed, arXiv, Semantic Scholar, bioinformatics, biomedical, life-science, scientific database skill/plugin/MCP repositories. Use when a coding agent (Claude Code, Codex, or similar) needs to add repos, triage discovery candidates, refresh metadata, recategorize entries, validate the data, or regenerate the README/catalog outputs.
---

# Research Repo Catalog

## Layout

- `data/catalog_config.json` - categories (English and Chinese), `type` vocabulary, interfaces, hosts, domains, policy text. Single source of truth.
- `data/repos.seed.tsv` - the hand-maintained list: `repo, category, type, type_detail, interfaces, hosts, domain, pinned, notes, notes_zh, include`.
- `data/repos.curated.tsv` - seed fields plus GitHub metadata (stars, forks, pushed_at, archived, license, topics, status). Generated; sorted by repo name.
- `data/star_history.tsv` - one row per repo per refresh date. Feeds `CHANGELOG.md` and the "Recent changes" block.
- `data/last_refresh.json`, `data/refresh_report.md` - when metadata was last fetched and what went wrong.
- `data/discovery_queries.tsv`, `data/candidates_seen.tsv`, `data/triage.tsv`, `data/awesome_refs.tsv` - discovery inputs, state, and human decisions.
- `README.md`, `README-zh.md`, `catalog.md` - prose plus a generated block between `<!-- CATALOG:START -->` and `<!-- CATALOG:END -->`.
- `catalog.json`, `CHANGELOG.md` - generated machine-readable export and history.

## Workflow

1. Read `references/catalog-policy.md` for inclusion rules, category labels, the type vocabulary, and field definitions.
2. Run `python3 scripts/update_catalog.py --check` to confirm the starting state is clean.
3. To add or change repos, edit `data/repos.seed.tsv` only. Use one category label and one `type` key exactly as listed in `data/catalog_config.json`. Fill `interfaces`, `hosts`, and `domain`; write short English `notes` and a real Chinese translation in `notes_zh`.
4. If the repo came from `discovery/candidates.md`, add a row to `data/triage.tsv` (`accept`, `reject`, or `defer`, with a reason and date). Rejected repos stop appearing in reports.
5. Regenerate: `python3 scripts/update_catalog.py --refresh` when the network and a GitHub token are available, otherwise `--from-curated` (new rows render as `pending` until the next refresh).
6. Discovery: `python3 scripts/discover_candidates.py` (network) or `--offline` to re-render the report from state files.
7. Validate: `python3 scripts/update_catalog.py --check`, `python3 scripts/discover_candidates.py --check --output discovery/candidates.md`, and `python3 -m unittest discover -s tests`.
8. Review `git diff` before summarizing results.

## Guardrails

- Do not push or create a GitHub remote unless the user explicitly asks.
- Keep category labels and `type` keys exactly aligned with `data/catalog_config.json`; add new ones there first, then in `references/catalog-policy.md`.
- Preserve rows marked `pinned=yes` unless the user asks to remove them.
- Prefer primary GitHub REST metadata for stars, dates, URL, language, license, and description; never type numbers by hand.
- Treat GitHub Search and awesome-list cross-references as incomplete leads; `discovery/candidates.md` is a triage queue, not catalog membership.
- Never hand-edit generated blocks or generated files; fix the seed, config, or script instead.
