---
name: research-repo-catalog
description: Maintain and update a curated GitHub catalog of AI-agent-related research, academic writing, literature search, Zotero, PubMed, arXiv, Semantic Scholar, bioinformatics, biomedical, life-science, scientific database skill/plugin/MCP repositories. Use when Codex needs to add repos, refresh metadata, recategorize entries, validate sorting/deduplication, or regenerate this project README/catalog.
---

# Research Repo Catalog

## Workflow

1. Read `references/catalog-policy.md` for inclusion rules, category labels, and update constraints.
2. Inspect `data/repos.seed.tsv`, `data/repos.curated.tsv`, `README.md`, and `catalog.md`.
3. Add or edit repos in `data/repos.seed.tsv`; maintain both `notes` and `notes_zh`; do not hand-edit generated table sections in `README.md`, `README-zh.md`, or `catalog.md`.
4. Refresh metadata with `python3 scripts/update_catalog.py --refresh` when network is available.
5. If network is unavailable, regenerate English and Chinese outputs from cached metadata with `python3 scripts/update_catalog.py --from-curated` and report that stars were not refreshed.
6. Validate with `python3 scripts/update_catalog.py --check`.
7. Review `git diff` before summarizing results.

## Guardrails

- Do not push or create a GitHub remote unless the user explicitly asks.
- Keep categories exactly aligned with the labels in `references/catalog-policy.md`.
- Preserve user-requested entries such as `WUBING2023/PaperSpine` unless the user asks to remove them.
- Prefer primary GitHub metadata from the GitHub REST API for stars, updated date, URL, language, and description.
- Treat GitHub Search results as incomplete; record search directions in the final summary when doing broad updates.
