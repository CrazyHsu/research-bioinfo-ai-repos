# Catalog Policy

The machine-readable copy of the categories, type vocabulary, and policy text is `data/catalog_config.json`; `scripts/update_catalog.py --check` verifies that every category label below also exists there.

## Categories

Use exactly one of these category labels per repo:

- `General Research / AI4S Skill Suites`
- `Paper Writing / Peer Review / Submission Skills`
- `Literature Search / Scholarly Search MCP`
- `Zotero / CNKI / Google Scholar / Reference Management`
- `Bioinformatics / Omics / Single-Cell Skills`
- `Protein Design / Structural Biology`
- `Pipelines / Sequence & Genome Tool MCP`
- `Biomedical / Clinical / Medical Research`
- `Biological Databases / Pathways / Chemistry / Drug Discovery MCP`
- `Research Agent Apps / Workspaces`
- `Figures / PDF / LaTeX / Research Artifact Tools`
- `Awesome Lists / Registries / Further Discovery`

## Type vocabulary

Use exactly one `type` key per repo; keep the original free-text description in `type_detail` if it adds information.

| key | meaning |
|---|---|
| `skill` | a single agent skill (one SKILL.md or one focused workflow) |
| `skill-suite` | a library or suite of multiple skills |
| `mcp-server` | one MCP server |
| `mcp-suite` | a collection or platform of several MCP servers |
| `plugin` | a host-specific plugin (Zotero, Claude Code, Codex, VS Code, ...) |
| `agent-app` | a standalone research agent application or workspace |
| `framework` | a framework or harness for building agents or skills |
| `tool` | an agent-ready tool or toolkit that is not primarily a skill or MCP server |
| `directory` | an awesome list or curated directory |
| `registry` | a machine-readable registry or marketplace |

## Seed fields

- `interfaces` - comma-separated subset of `skill, mcp, plugin, app, tool, framework, directory, registry`: every interface the repo exposes.
- `hosts` - comma-separated subset of `claude-code, claude-desktop, codex, cursor, gemini-cli, opencode, openclaw, copilot, vscode`: hosts the README explicitly supports. Leave empty when unknown; MCP servers work with any MCP client and need no host entry.
- `domain` - `bio` (life sciences, biomedical), `research` (research workflow without a bio focus), or `general` (kept only as a discovery entry point).
- `pinned` - `yes` for entries that must never be dropped without an explicit request.
- `notes` / `notes_zh` - one short sentence each. Say what the repo does and how it differs from neighbours in the same category. `notes_zh` must be Chinese, not a copy of `notes`.
- `include` - `no` keeps a row in the file (so discovery stops reporting it) without rendering it.

## Include

Include a repository when it clearly targets AI-agent use and at least one of these areas:

- scientific or academic research workflows
- paper writing, review, rebuttal, revision, or submission
- literature search, citation, article retrieval, PDF reading, or reference management
- Zotero, CNKI, Google Scholar, arXiv, PubMed, bioRxiv, medRxiv, Semantic Scholar, OpenAlex, Crossref
- bioinformatics, genomics, transcriptomics, proteomics, single-cell, spatial omics, multi-omics
- protein engineering, protein design, folding, structural biology, and agentic protein workflows
- biomedical, clinical, medical research, clinical trials, drug discovery
- scientific databases and model/tool interfaces such as AlphaFold, Boltz, MacromNex, PDB/PDBe, UniProt, Ensembl, ChEMBL, PubChem, KEGG, Reactome, STRING, Open Targets
- pipeline engines and sequence tools exposed to agents (Nextflow/nf-core, Galaxy, Snakemake, BLAST, samtools)
- agent-ready tools that generate research artifacts such as figures, LaTeX, PDF translations, or diagrams

## Exclude

Exclude repositories that are primarily:

- generic agent infrastructure without a research/science/literature/bio angle
- ordinary tutorials, paper lists, or reading lists without reusable agent skill/plugin/MCP content
- book inventory, note apps, or document tools without research-agent specificity
- mirror-only forks or empty wrappers without meaningful additions
- unclear repos with no useful description or README evidence

## Triage

- Every repo in `discovery/candidates.md` gets a row in `data/triage.tsv` once reviewed: `accept` (then add it to the seed), `reject` (with the rule it fails), or `defer` (with what is missing).
- Low-star repos may stay if they are direct, unique, and useful; discovery reports everything with at least one star.
- If two repos duplicate the same implementation, prefer the original or more maintained repo and record the other as `reject` with that reason.
- Stars are metadata, not a quality score. `pushed_at`, `archived`, and `license` are the maintenance signals; a repo missing on GitHub for more than a week fails validation and must be removed or fixed.
