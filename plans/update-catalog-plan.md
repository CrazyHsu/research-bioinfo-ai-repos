# Update Catalog Plan

## Summary

Keep `data/repos.seed.tsv` as the human-maintained source and regenerate `README.md`, `README-zh.md`, `catalog.md`, `catalog.json`, and `CHANGELOG.md` through `scripts/update_catalog.py`. New repositories enter through `discovery/candidates.md` and decisions are recorded in `data/triage.tsv`.

## Steps

1. Inspect the current state:
   - `python3 scripts/update_catalog.py --check`
   - Read `discovery/candidates.md` (new this run, seen before, deferred) and `data/refresh_report.md`.

2. Triage candidates:
   - For each candidate, check README evidence, scope, overlap with existing entries, license, and maintenance.
   - Add a row to `data/triage.tsv` with `accept`, `reject`, or `defer` and a reason.
   - Accepted repos go into `data/repos.seed.tsv` with a category, a `type` key, interfaces, hosts, domain, and bilingual notes.

3. Regenerate and validate:
   - `python3 scripts/update_catalog.py --refresh` (network) or `--from-curated` (offline; new rows render as `pending`).
   - `python3 scripts/discover_candidates.py` (network) or `--offline`.
   - `python3 scripts/update_catalog.py --check`, `python3 scripts/discover_candidates.py --check --output discovery/candidates.md`, `python3 -m unittest discover -s tests`.

4. Review `git diff` for accidental removals or category drift, then commit locally. Do not push unless asked.

## Acceptance Criteria

- `--check` and the tests pass.
- Every candidate reviewed has a triage row; every accepted candidate is in the seed.
- New and changed rows have short, differentiating notes in both languages.

## Automation

`.github/workflows/update-catalog.yml` runs every Monday (and on demand): tests, metadata refresh, discovery, validation, and a commit whose message summarizes the refresh. A failed run opens or updates an issue labelled `catalog-failure`. `.github/workflows/validate.yml` runs the tests and `--check` on pull requests.
