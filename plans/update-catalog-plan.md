# Update Catalog Plan

## Summary

Refresh the curated GitHub README/catalog for research, paper writing, literature search, bioinformatics, biomedical, life-science skill/plugin/MCP repositories. Keep `data/repos.seed.tsv` as the human-maintained source and regenerate `README.md`, `README-zh.md`, and `catalog.md` through `scripts/update_catalog.py`.

## Steps

1. Inspect current state:
   - Run `python3 scripts/update_catalog.py --check`.
   - Read `README.md`, `catalog.md`, and `data/repos.seed.tsv` to understand current categories and scope.

2. Search for candidate repos:
   - Use GitHub search/API queries around: `academic research skills`, `paper writing skill`, `arxiv MCP`, `Semantic Scholar MCP`, `Zotero MCP`, `PubMed MCP`, `bioinformatics skills`, `genomics MCP`, `AlphaFold MCP`, `PDB MCP`, `ChEMBL MCP`, `ClinicalTrials MCP`, `AI for Science skills`.
   - Include user-specified missing repos first.

3. Apply inclusion policy:
   - Include repos that explicitly serve AI agents as skill/plugin/MCP/agent-ready workflows for research, paper writing, literature search, life sciences, bioinformatics, biomedical, or scientific databases.
   - Exclude unrelated generic agent infrastructure, empty forks, mirror-only repos, ordinary tutorials, and unclear repos without useful descriptions.

4. Edit `data/repos.seed.tsv`:
   - Add `repo`, `category`, `type`, `notes`, `notes_zh`, `include`.
   - Choose one of the existing category labels exactly.
   - Keep both English `notes` and Chinese `notes_zh` short and useful for catalog readers.

5. Refresh and render:
   - Run `python3 scripts/update_catalog.py --refresh` when network is available.
   - If network is unavailable, update `data/repos.curated.tsv` manually or defer metadata refresh, then run `python3 scripts/update_catalog.py --from-curated` to regenerate README/catalog.

6. Validate:
   - Run `python3 scripts/update_catalog.py --check`.
   - Confirm user-requested repos are present.
   - Confirm each category remains sorted by stars descending.
   - Review `git diff` for accidental removals or category drift.

7. Commit locally:
   - Commit when the update is coherent.
   - Do not create a remote or push unless explicitly requested.

## Acceptance Criteria

- `README.md`, `README-zh.md`, and `catalog.md` are generated and readable by category.
- `data/repos.seed.tsv` has no duplicate repo rows.
- `scripts/update_catalog.py --check` exits successfully.
- New and changed repos have short notes and appropriate categories.

## Automation

GitHub Actions can refresh metadata automatically through `.github/workflows/update-catalog.yml`, which runs weekly and can also be triggered manually. The workflow commits only when generated files change.
