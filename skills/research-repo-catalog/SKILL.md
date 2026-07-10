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
5. Run focused discovery with `python3 scripts/discover_candidates.py --limit-per-query 20 --min-stars 5 --output discovery/candidates.md`; review candidates before adding any to the seed file.
6. If network is unavailable, regenerate English and Chinese outputs from cached metadata with `python3 scripts/update_catalog.py --from-curated` and report that stars/candidates were not refreshed.
7. Validate with `python3 scripts/update_catalog.py --check` and, when generated, `python3 scripts/discover_candidates.py --check --output discovery/candidates.md`.
8. Review `git diff` before summarizing results.

## Guardrails

- Do not push or create a GitHub remote unless the user explicitly asks.
- Keep categories exactly aligned with the labels in `references/catalog-policy.md`.
- Preserve user-requested entries such as `WUBING2023/PaperSpine` unless the user asks to remove them.
- Preserve user-requested entries such as `charlesxu90/ProteinMCP` unless the user asks to remove them.
- Prefer primary GitHub metadata from the GitHub REST API for stars, updated date, URL, language, and description.
- Treat GitHub Search results as incomplete; use `discovery/candidates.md` as a triage queue, not as automatic catalog membership.
