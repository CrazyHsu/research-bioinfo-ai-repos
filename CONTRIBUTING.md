# Contributing

## Suggest a repository

Open an issue with the "Suggest a repository" template, or send a pull request that edits `data/repos.seed.tsv`.

## Pull request checklist

1. Add one row to `data/repos.seed.tsv`:
   - `category`: one label from `data/catalog_config.json`.
   - `type`: one key from the vocabulary (`skill`, `skill-suite`, `mcp-server`, `mcp-suite`, `plugin`, `agent-app`, `framework`, `tool`, `directory`, `registry`).
   - `interfaces`, `hosts`, `domain`: see `skills/research-repo-catalog/references/catalog-policy.md`.
   - `notes` (English) and `notes_zh` (Chinese): one sentence each saying what the repo does and how it differs from its neighbours.
2. If the repo appears in `discovery/candidates.md`, add an `accept` row to `data/triage.tsv`.
3. Run `python3 scripts/update_catalog.py --from-curated` and `python3 scripts/update_catalog.py --check`. New rows render as `pending`; the weekly workflow fills in GitHub metadata.
4. Run `python3 -m unittest discover -s tests`.
5. Do not hand-edit the generated blocks in `README.md`, `README-zh.md`, `catalog.md`, or the generated files `catalog.json` and `CHANGELOG.md`.

## Rejecting or removing

Set `include` to `no` instead of deleting a seed row when the repo should stop being suggested by discovery, and add a `reject` row with the reason to `data/triage.tsv`.
