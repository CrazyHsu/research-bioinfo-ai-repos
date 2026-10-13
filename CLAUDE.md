# CLAUDE.md

This repository is a curated, bilingual catalog of AI-agent extensions (skills, plugins, MCP servers) for research, paper writing, literature search, bioinformatics, and biomedical work. The full maintainer workflow is in `skills/research-repo-catalog/SKILL.md`; the rules below are the short version.

## Commands

```bash
python3 -m unittest discover -s tests                # tests (stdlib only, no dependencies)
python3 scripts/update_catalog.py --check            # validate seed, curated data, and rendered outputs (no network)
python3 scripts/update_catalog.py --from-curated     # regenerate outputs from cached metadata (no network)
python3 scripts/update_catalog.py --refresh          # fetch GitHub metadata; needs GITHUB_TOKEN or GH_TOKEN
python3 scripts/discover_candidates.py               # run discovery queries + awesome-list cross-references
python3 scripts/discover_candidates.py --offline     # re-render discovery/candidates.md from state files
```

## Rules

- `data/repos.seed.tsv` is the only hand-edited list. Never edit the text between `<!-- CATALOG:START -->` and `<!-- CATALOG:END -->` in `README.md`, `README-zh.md`, or `catalog.md`; regenerate it.
- Categories, the `type` vocabulary, interfaces, hosts, domains, and policy text live in `data/catalog_config.json`. Keep `skills/research-repo-catalog/references/catalog-policy.md` in sync (`--check` verifies every category label appears there).
- Every seed row needs English `notes` and Chinese `notes_zh` that say what the repo does and how it differs from its neighbours. `notes_zh` must be a translation, not a copy.
- New seed rows render as `pending` until the next `--refresh`; that is expected when working offline.
- Candidates come from `discovery/candidates.md`. Record every decision in `data/triage.tsv` (`accept`, `reject`, `defer` + reason) so the repo stops reappearing.
- After editing the seed: run `--from-curated`, then `--check`, then the tests. Review `git diff` before committing.
- Do not push or open pull requests unless the user asks.
