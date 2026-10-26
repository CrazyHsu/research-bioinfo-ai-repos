# Research Bioinfo AI Repos

Curated GitHub catalog of AI-agent extensions for research work: skills, plugins, and MCP servers for literature search, paper writing, reference management, bioinformatics, biomedical research, and biological databases.

Browse the catalog below, in Chinese at [README-zh.md](README-zh.md), as a standalone page in [catalog.md](catalog.md), or as data in [`catalog.json`](catalog.json). Week-by-week changes are in [CHANGELOG.md](CHANGELOG.md).

## How the catalog is maintained

- `data/repos.seed.tsv` is the only hand-edited list: scope, category, a controlled `type`, interfaces, hosts, domain, and bilingual notes. Categories, the type vocabulary, and policy text live in `data/catalog_config.json`.
- `scripts/update_catalog.py --refresh` fetches GitHub metadata into `data/repos.curated.tsv`, appends a snapshot to `data/star_history.tsv`, and regenerates everything between the catalog markers in this file, `README-zh.md`, and `catalog.md`, plus `catalog.json` and `CHANGELOG.md`.
- `scripts/discover_candidates.py` runs the queries in `data/discovery_queries.tsv` and cross-references the awesome lists already in the catalog. Hits land in `discovery/candidates.md`, are tracked across runs in `data/candidates_seen.tsv`, and decisions are recorded in `data/triage.tsv`.
- `.github/workflows/update-catalog.yml` runs both scripts every Monday and commits when outputs change; a failed run opens an issue. `.github/workflows/validate.yml` checks pull requests.
- `skills/research-repo-catalog/` and `CLAUDE.md` tell a coding agent (Claude Code, Codex, or similar) how to maintain the catalog. `archive/` keeps the original draft.

## Quick start

```bash
python3 scripts/update_catalog.py --check          # validate data and rendered outputs, no network
python3 scripts/update_catalog.py --from-curated   # regenerate outputs from cached metadata, no network
python3 scripts/update_catalog.py --refresh        # fetch GitHub metadata (set GITHUB_TOKEN or GH_TOKEN)
python3 scripts/discover_candidates.py             # run discovery; --offline re-renders without network
python3 -m unittest discover -s tests              # run the test suite (standard library only)
```

## Adding a repository

1. Check `discovery/candidates.md` and `data/triage.tsv` first.
2. Add a row to `data/repos.seed.tsv` with one category label, one `type` key, interfaces, hosts, domain, and short English and Chinese notes that say what the repo does and how it differs from its neighbours.
3. Run `python3 scripts/update_catalog.py --from-curated` (the new row renders as `pending` until the next refresh) and then `--check`.
4. If the repo came from the candidate report, add an `accept` row to `data/triage.tsv`. Details in [CONTRIBUTING.md](CONTRIBUTING.md).

## Catalog

<!-- CATALOG:START -->
Metadata refreshed on 2026-10-26 (UTC): 155 repositories in 12 categories. Stars and last-push dates come from the GitHub REST API; `(archived)` marks archived repositories. All fields, including license, language, topics, interfaces, and hosts, are in `data/repos.curated.tsv` and `catalog.json`.

### Recent changes

Refresh of 2026-10-26 compared with 2026-10-19. Full history: [CHANGELOG.md](CHANGELOG.md).

- Added: none
- Removed: none
- Archived: `GPTomics/bioSkills`, `gyger/mcp-pyzotero`
- Renamed: none
- Missing on GitHub: none
- Top star gains: `K-Dense-AI/scientific-agent-skills` +1913 (52753 -> 54666), `Imbad0202/academic-research-skills` +1059 (52884 -> 53943), `wanshuiyin/Auto-claude-code-research-in-sleep` +393 (17698 -> 18091), `Imbad0202/academic-research-skills-codex` +375 (13144 -> 13519), `punkpeye/awesome-mcp-servers` +288 (96592 -> 96880)

## General Research / AI4S Skill Suites

| repo | type | stars | last push | focus / notes |
|---|---|---:|---|---|
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | skill-suite | 54666 | 2026-10-19 | Agent Skills standard for scientific research, biology, chemistry, medicine, and drug discovery |
| [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | skill-suite | 53943 | 2026-10-26 | Academic research skills: research -> write -> review -> revise -> finalize |
| [wanshuiyin/Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | skill-suite | 18091 | 2026-10-24 | ARIS automated research loop, idea discovery, and experiment automation |
| [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) | skill-suite | 13960 | 2026-10-11 | AI research and engineering skills for Claude, Codex, and Gemini |
| [Imbad0202/academic-research-skills-codex](https://github.com/Imbad0202/academic-research-skills-codex) | skill-suite | 13519 | 2026-10-26 | Codex-native academic research workflow |
| [openai/plugins](https://github.com/openai/plugins) | plugin | 7598 | 2026-10-08 | OpenAI Codex plugins, including life-science-research |
| [zLanqing/codex-claude-academic-skills](https://github.com/zLanqing/codex-claude-academic-skills) | skill-suite | 5328 | 2026-05-14 | Chinese-language research reading, writing, and scientific computing |
| [brycewang-stanford/Auto-Empirical-Research-Skills](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills) | skill-suite | 4783 | 2026-10-20 | Empirical social science research with 23,000+ agent skills |
| [google-deepmind/science-skills](https://github.com/google-deepmind/science-skills) | skill-suite | 3334 | 2026-10-23 | DeepMind science agent skills |
| [Weizhena/Deep-Research-skills](https://github.com/Weizhena/Deep-Research-skills) | skill | 2422 | 2026-08-23 | Structured deep research skill, Claude/OpenCode/Codex |
| [luwill/research-skills](https://github.com/luwill/research-skills) | skill-suite | 876 | 2026-10-25 | Common research practices and workflows packaged as agent skills |
| [chrisblattman/claudeblattman](https://github.com/chrisblattman/claudeblattman) | skill-suite | 470 | 2026-10-24 | Claude Code for academics: skills, agents, setup guides |
| [fcakyon/phd-skills](https://github.com/fcakyon/phd-skills) | skill-suite | 434 | 2026-10-11 | PhD research: reproduction, experimental design, paper review, and result comparison |
| [chtc66/academic-skills](https://github.com/chtc66/academic-skills) | skill-suite | 367 | 2026-04-05 | Paper reading, surveys, experiment summaries, rebuttals, and lab updates |
| [ai4s-research/ai4s-skills](https://github.com/ai4s-research/ai4s-skills) | skill-suite | 252 | 2026-07-28 | AI for Science: topic exploration, literature survey, experiments, writing, and integrity audit |
| [AlterLab-IEU/AlterLab-Academic-Skills](https://github.com/AlterLab-IEU/AlterLab-Academic-Skills) | skill-suite | 78 | 2026-10-23 | 239 evaluated academic skills, including bioinformatics and clinical research |
| [s-choung/Research-Skills](https://github.com/s-choung/Research-Skills) | skill-suite | 36 | 2026-10-21 | Research writing, figures, document automation, and Korean academic materials |
| [JhonHander/academic-agent-toolkit](https://github.com/JhonHander/academic-agent-toolkit) | tool | 8 | 2026-06-09 | Installer for MCP tools and AI research skills |

## Paper Writing / Peer Review / Submission Skills

| repo | type | stars | last push | focus / notes |
|---|---|---:|---|---|
| [Master-cai/Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills) | skill-suite | 7801 | 2026-06-23 | ML/CV/NLP paper writing for Codex, Claude, and Gemini |
| [WUBING2023/PaperSpine](https://github.com/WUBING2023/PaperSpine) | skill | 6078 | 2026-10-14 | Central paper argumentation, strong-paper learning, manuscript rewriting, and LaTeX-safe audits |
| [PaperDebugger/paperdebugger](https://github.com/PaperDebugger/paperdebugger) | plugin | 1549 | 2026-07-03 | Academic writing, peer review, and editing |
| [fakerqwq/social-science-paper-writing-skill](https://github.com/fakerqwq/social-science-paper-writing-skill) | skill | 435 | 2026-06-02 | Social science paper writing, topic selection, literature reviews, and citation risk checks |
| [SNL-UCSB/paper-writing-skill](https://github.com/SNL-UCSB/paper-writing-skill) | skill | 244 | 2026-07-31 | Brainstorm -> Draft -> Evaluate -> Write -> Compress paper writing |
| [SyntaxSmith/nature-writing-skill](https://github.com/SyntaxSmith/nature-writing-skill) | skill | 180 | 2026-04-27 | Nature-family paper writing |
| [cLin-c/paper-skill](https://github.com/cLin-c/paper-skill) | skill | 132 | 2026-09-26 | Paper writing, polishing, peer review, translation, and submission |
| [fuhaoda/stats-paper-writing-agent-skills](https://github.com/fuhaoda/stats-paper-writing-agent-skills) | skill | 31 | 2026-02-13 | Agent skills for statistics paper writing |
| [Zhangyanbo/vibe-paper-writing](https://github.com/Zhangyanbo/vibe-paper-writing) | skill | 25 | 2026-02-28 | Convert notes, chats, and emails into LaTeX academic papers |
| [MetaQiu/Trivium](https://github.com/MetaQiu/Trivium) | skill | 24 | 2026-02-15 | Multi-agent collaborative paper writing for Claude, Codex, and Gemini |
| [AGISAFETYLAB/Paper-Writing-skill](https://github.com/AGISAFETYLAB/Paper-Writing-skill) | skill | 21 | 2026-06-26 | Planning, writing, polishing, figures, and citation checks for CS, medical, and finance papers |
| [dailycafi/biomed-paper-writing-skill](https://github.com/dailycafi/biomed-paper-writing-skill) | skill | 2 | 2026-03-16 | Biomedical and pharmaceutical paper writing with CONSORT, STROBE, PRISMA, and ARRIVE |
| [Jason-0409-G/scriptorium](https://github.com/Jason-0409-G/scriptorium) | skill | 1 | 2026-06-25 | DOI-verified literature library, NCBI/UniProt/PDB/AlphaFold integration, writing, and review |

## Literature Search / Scholarly Search MCP

| repo | type | stars | last push | focus / notes |
|---|---|---:|---|---|
| [blazickjp/arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server) | mcp-server | 3235 | 2026-10-08 | arXiv search and paper analysis MCP |
| [openags/paper-search-mcp](https://github.com/openags/paper-search-mcp) | mcp-server | 2920 | 2026-10-02 | Paper search and download for arXiv, PubMed, bioRxiv, and related sources |
| [ShZhao27208/Aut_Sci_Write](https://github.com/ShZhao27208/Aut_Sci_Write) | skill-suite | 213 | 2026-08-13 | WoS, Elsevier, and Springer search/download, reviews, Zotero, PPT, and HTML |
| [Dianel555/paper-search-mcp-nodejs](https://github.com/Dianel555/paper-search-mcp-nodejs) | mcp-server | 191 | 2026-09-20 | Paper search and download for Web of Science, arXiv, and related sources |
| [andybrandt/mcp-simple-pubmed](https://github.com/andybrandt/mcp-simple-pubmed) | mcp-server | 171 | 2026-03-19 | PubMed medical literature search MCP |
| [zongmin-yu/semantic-scholar-fastmcp-mcp-server](https://github.com/zongmin-yu/semantic-scholar-fastmcp-mcp-server) | mcp-server | 166 | 2026-03-20 | Semantic Scholar API FastMCP server |
| [cyanheads/pubmed-mcp-server](https://github.com/cyanheads/pubmed-mcp-server) | mcp-server | 163 | 2026-10-26 | PubMed/Europe PMC/Unpaywall, MeSH, full text |
| [Darkroaster/pubmearch](https://github.com/Darkroaster/pubmearch) | mcp-server | 150 | 2025-05-07 | PubMed search and analysis MCP (Python) |
| [takashiishida/arxiv-latex-mcp](https://github.com/takashiishida/arxiv-latex-mcp) | mcp-server | 149 | 2026-10-23 | arXiv LaTeX source parsing |
| [JackKuo666/PubMed-MCP-Server](https://github.com/JackKuo666/PubMed-MCP-Server) | mcp-server | 132 | 2025-05-08 | PubMed article search, access, and analysis |
| [grll/pubmedmcp](https://github.com/grll/pubmedmcp) | mcp-server | 123 | 2025-09-02 | PubMed data MCP (Python) |
| [afrise/academic-search-mcp-server](https://github.com/afrise/academic-search-mcp-server) | mcp-server | 118 | 2025-02-12 | Semantic Scholar and Crossref search MCP |
| [JackKuo666/semanticscholar-MCP-Server](https://github.com/JackKuo666/semanticscholar-MCP-Server) | mcp-server | 87 | 2025-03-25 | Semantic Scholar paper/author/citation/reference |
| [benedict2310/Scientific-Papers-MCP](https://github.com/benedict2310/Scientific-Papers-MCP) | mcp-server | 63 | 2025-08-14 | arXiv + OpenAlex scientific papers |
| [akapet00/semantic-scholar-mcp](https://github.com/akapet00/semantic-scholar-mcp) | mcp-server | 37 | 2026-05-07 | Semantic Scholar paper search and analysis |
| [lstudlo/ScholarMCP](https://github.com/lstudlo/ScholarMCP) | mcp-server | 31 | 2026-09-23 | Literature search, PDF ingestion, and reference management |
| [TaewoooPark/scholar-megasearch](https://github.com/TaewoooPark/scholar-megasearch) | skill | 31 | 2026-08-14 | 20+ scholarly databases with multi-source search and PDF retrieval |
| [u9401066/pubmed-search-mcp](https://github.com/u9401066/pubmed-search-mcp) | mcp-server | 28 | 2026-10-20 | PubMed/Europe PMC/CORE/OpenAlex, citation networks, PICO |
| [JackKuo666/bioRxiv-MCP-Server](https://github.com/JackKuo666/bioRxiv-MCP-Server) | mcp-server | 26 | 2025-03-18 | bioRxiv preprint search, metadata, and download MCP (FastMCP) |
| [masa-med-ai/pubmed-systematic-review](https://github.com/masa-med-ai/pubmed-systematic-review) | skill | 25 | 2026-05-20 | Lightweight systematic reviews integrated with a PubMed MCP |
| [zongmin-yu/semantic-scholar-skills](https://github.com/zongmin-yu/semantic-scholar-skills) | skill | 22 | 2026-03-16 | Semantic Scholar first literature discovery skill with an MCP companion |
| [aringadre76/mcp-for-research](https://github.com/aringadre76/mcp-for-research) | mcp-server | 16 | 2026-05-12 | PubMed, Google Scholar, arXiv, JSTOR |
| [JackKuo666/medRxiv-MCP-Server](https://github.com/JackKuo666/medRxiv-MCP-Server) | mcp-server | 9 | 2025-03-18 | medRxiv health-science preprint search and metadata MCP |

## Zotero / CNKI / Google Scholar / Reference Management

| repo | type | stars | last push | focus / notes |
|---|---|---:|---|---|
| [MuiseDestiny/zotero-gpt](https://github.com/MuiseDestiny/zotero-gpt) | plugin | 7495 | 2026-05-01 | Zotero GPT plugin: chat with papers and your library through OpenAI-compatible APIs |
| [54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp) | mcp-server | 5573 | 2026-10-16 | Connect Zotero libraries to Claude and AI assistants |
| [yilewang/llm-for-zotero](https://github.com/yilewang/llm-for-zotero) | agent-app | 3413 | 2026-10-22 | Research agent system based on a Zotero library |
| [papersgpt/papersgpt-for-zotero](https://github.com/papersgpt/papersgpt-for-zotero) | plugin | 2681 | 2026-10-22 | Zotero AI/MCP plugin with multi-model paper Q&A |
| [lifan0127/ai-research-assistant](https://github.com/lifan0127/ai-research-assistant) | plugin | 1730 | 2025-04-01 | Aria: LLM-powered research assistant plugin for Zotero (OpenAI models) |
| [cookjohn/zotero-mcp](https://github.com/cookjohn/zotero-mcp) | plugin | 1250 | 2026-09-09 | Deep integration between Zotero and AI assistants |
| [cookjohn/cnki-skills](https://github.com/cookjohn/cnki-skills) | skill-suite | 1017 | 2026-03-13 | CNKI search, PDFs, and Zotero export |
| [cookjohn/gs-skills](https://github.com/cookjohn/gs-skills) | skill-suite | 535 | 2026-03-13 | Google Scholar search, citation tracking, and Zotero export |
| [introfini/ZotSeek](https://github.com/introfini/ZotSeek) | plugin | 235 | 2026-10-08 | Zotero semantic search with local privacy and built-in MCP |
| [kaliaboi/mcp-zotero](https://github.com/kaliaboi/mcp-zotero) | mcp-server | 163 | 2025-02-04 | Connect Claude Desktop to Zotero Cloud |
| [kujenga/zotero-mcp](https://github.com/kujenga/zotero-mcp) | mcp-server | 162 | 2026-08-07 | Zotero Web API MCP server (Python) |
| [TonybotNi/ZotLink](https://github.com/TonybotNi/ZotLink) | mcp-server | 136 | 2025-10-12 | Save arXiv, CVF, bioRxiv, and medRxiv papers to Zotero |
| [dralkh/seerai](https://github.com/dralkh/seerai) | plugin | 94 | 2026-10-06 | Zotero AI plugin, RAG, OCR, systematic reviews, MCP, skills |
| [gyger/mcp-pyzotero](https://github.com/gyger/mcp-pyzotero) (archived) | mcp-server | 56 | 2025-11-20 | Local Zotero MCP connector |
| [Xevos117/mcp-zotero](https://github.com/Xevos117/mcp-zotero) | mcp-server | 38 | 2026-10-26 | Zotero library operations, DOI, PDF, Unpaywall, docx citation fields |
| [cookjohn/pm-skills](https://github.com/cookjohn/pm-skills) | skill-suite | 19 | 2026-03-13 | PubMed literature search, citation export, Zotero |

## Bioinformatics / Omics / Single-Cell Skills

| repo | type | stars | last push | focus / notes |
|---|---|---:|---|---|
| [GPTomics/bioSkills](https://github.com/GPTomics/bioSkills) (archived) | skill-suite | 1225 | 2026-08-15 | RNA-seq, scRNA, variant, multi-omics |
| [ClawBio/ClawBio](https://github.com/ClawBio/ClawBio) | skill-suite | 1166 | 2026-10-26 | Bioinformatics-native agent skill library: 95 skills with demo data, Galaxy tool wrappers, pip/conda install, Claude Code plugin and MCP server |
| [jaechang-hits/SciAgent-Skills](https://github.com/jaechang-hits/SciAgent-Skills) | skill-suite | 383 | 2026-10-22 | 197 life-science and bioinformatics skills |
| [TianGzlab/OmicsClaw](https://github.com/TianGzlab/OmicsClaw) | agent-app | 161 | 2026-10-07 | Multi-omics analysis through manuscript generation |
| [swaruplab/operon](https://github.com/swaruplab/operon) | agent-app | 101 | 2026-10-11 | Claude Code bioinformatics IDE and protocols |
| [variomeanalytics/bioinformatics-agent-skills](https://github.com/variomeanalytics/bioinformatics-agent-skills) | mcp-server | 63 | 2026-04-18 | Knowledge graph over 78 bioinformatics workflows |
| [cafferychen777/ChatSpatial](https://github.com/cafferychen777/ChatSpatial) | mcp-server | 45 | 2026-10-20 | Natural-language analysis for spatial transcriptomics |
| [ma-compbio-lab/SkillFoundry](https://github.com/ma-compbio-lab/SkillFoundry) | framework | 43 | 2026-09-14 | Computational biology skill discovery and validation |
| [scmcphub/scmcp](https://github.com/scmcphub/scmcp) | mcp-suite | 16 | 2025-07-10 | Natural-language scRNA-seq analysis MCP; also the shared AnnData backend for scanpy-mcp, liana-mcp, and cellrank-mcp |
| [Bioconductor/ai-agent-skills](https://github.com/Bioconductor/ai-agent-skills) | skill-suite | 10 | 2026-10-07 | R/Bioconductor and statistical bioinformatics |
| [scmcphub/scanpy-mcp](https://github.com/scmcphub/scanpy-mcp) | mcp-server | 2 | 2025-06-27 | Scanpy MCP covering IO, preprocessing, clustering, differential expression, and plotting |

## Protein Design / Structural Biology

| repo | type | stars | last push | focus / notes |
|---|---|---:|---|---|
| [adaptyvbio/protein-design-skills](https://github.com/adaptyvbio/protein-design-skills) | skill-suite | 170 | 2026-06-11 | Adaptyv Bio skill suite for protein design workflows |
| [001TMF/blatant-why](https://github.com/001TMF/blatant-why) | agent-app | 119 | 2026-10-16 | Multi-agent biologics design campaigns orchestrating BoltzGen, PXDesign, Protenix, and cloud tools for antibodies, nanobodies, and de novo binders |
| [charlesxu90/ProteinMCP](https://github.com/charlesxu90/ProteinMCP) | framework | 73 | 2026-05-01 | Agentic framework for autonomous protein engineering with Claude Code workflow skills and 38 supported MCPs |
| [vrtejus/pymol-mcp](https://github.com/vrtejus/pymol-mcp) | mcp-server | 68 | 2025-03-18 | Drive PyMOL from Claude: load structures, change representations, measure, align, and run Python inside PyMOL |
| [PDBeurope/PDBe-MCP-Servers](https://github.com/PDBeurope/PDBe-MCP-Servers) | mcp-server | 43 | 2026-10-22 | PDBe and protein structures |
| [Augmented-Nature/AlphaFold-MCP-Server](https://github.com/Augmented-Nature/AlphaFold-MCP-Server) | mcp-server | 36 | 2025-12-21 | Unofficial AlphaFold DB MCP for predicted structures and confidence metrics (Node.js) |
| [Augmented-Nature/PDB-MCP-Server](https://github.com/Augmented-Nature/PDB-MCP-Server) | mcp-server | 28 | 2025-12-21 | Unofficial RCSB PDB MCP for structure search and metadata (Node.js) |
| [jasonkim8652/protein-design-mcp](https://github.com/jasonkim8652/protein-design-mcp) | mcp-server | 18 | 2026-10-01 | Protein binder design MCP chaining RFdiffusion, ProteinMPNN, ESMFold, and AlphaFold2 |
| [cyanheads/protein-mcp-server](https://github.com/cyanheads/protein-mcp-server) | mcp-server | 6 | 2026-10-17 | PDB and AlphaFold protein structure and annotation federation |
| [PabloPauling/posebusters-mcp-server](https://github.com/PabloPauling/posebusters-mcp-server) | mcp-server | 5 | 2025-07-14 | PoseBusters molecular pose validation |
| [smaniches/alphafold-sovereign-mcp](https://github.com/smaniches/alphafold-sovereign-mcp) | mcp-server | 4 | 2026-10-26 | AlphaFold DB plus eight public sources with a local knowledge graph |

## Pipelines / Sequence & Genome Tool MCP

| repo | type | stars | last push | focus / notes |
|---|---|---:|---|---|
| [bio-mcp/bio-mcp-blast](https://github.com/bio-mcp/bio-mcp-blast) | mcp-server | 11 | 2025-06-29 | BLAST sequence search MCP that wraps a local BLAST+ install |
| [igvteam/igv-mcp](https://github.com/igvteam/igv-mcp) | mcp-server | 4 | 2025-12-07 | Official igvteam MCP to control the IGV desktop genome viewer from an agent |
| [kmaneesh/biopython-mcp](https://github.com/kmaneesh/biopython-mcp) | mcp-server | 3 | 2026-01-16 | Biopython sequence utilities exposed as MCP tools |
| [bio-mcp/bio-mcp-bwa](https://github.com/bio-mcp/bio-mcp-bwa) | mcp-server | 0 | 2025-07-10 | BWA alignment MCP: index references, run BWA-MEM, and emit SAM |
| [wjlim/nf-core_mcp](https://github.com/wjlim/nf-core_mcp) | mcp-server | 0 | 2025-04-08 | Browse nf-core pipelines, modules, configs, and workflow files through MCP |

## Biomedical / Clinical / Medical Research

| repo | type | stars | last push | focus / notes |
|---|---|---:|---|---|
| [FreedomIntelligence/OpenClaw-Medical-Skills](https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills) | skill-suite | 3080 | 2026-07-21 | Large OpenClaw medical AI skills collection |
| [aipoch/medical-research-skills](https://github.com/aipoch/medical-research-skills) | skill-suite | 1988 | 2026-09-17 | Medical research, protocols, data analysis, and academic writing |
| [mims-harvard/ToolUniverse](https://github.com/mims-harvard/ToolUniverse) | tool | 1759 | 2026-10-26 | Tool universe for biomedical AI scientists |
| [LeonChaoX/qinyan-academic-skills](https://github.com/LeonChaoX/qinyan-academic-skills) | skill-suite | 980 | 2026-07-20 | 177 academic research skills, including bioinformatics, drug discovery, and clinical medicine |
| [genomoncology/biomcp](https://github.com/genomoncology/biomcp) | mcp-server | 664 | 2026-10-24 | BioMCP for clinical trials, genomic data, and medical literature |
| [Cicatriiz/healthcare-mcp-public](https://github.com/Cicatriiz/healthcare-mcp-public) | mcp-server | 131 | 2025-08-16 | Medical data from FDA, PubMed, medRxiv, clinical trials, ICD-10, and related sources |
| [JamesANZ/medical-mcp](https://github.com/JamesANZ/medical-mcp) | mcp-server | 118 | 2026-10-15 | FDA, WHO, PubMed, Google Scholar, RxNorm |
| [cyanheads/clinicaltrialsgov-mcp-server](https://github.com/cyanheads/clinicaltrialsgov-mcp-server) | mcp-server | 98 | 2026-10-26 | ClinicalTrials.gov search, details, results, and patient matching |
| [lynnlangit/precision-medicine-mcp](https://github.com/lynnlangit/precision-medicine-mcp) | mcp-suite | 24 | 2026-08-25 | Precision medicine across multi-omics, genomics, and spatial transcriptomics |
| [pascalwhoop/medical-mcps](https://github.com/pascalwhoop/medical-mcps) | mcp-suite | 23 | 2026-09-01 | MCP tool collection for major biomedical databases |
| [JackKuo666/ClinicalTrials-MCP-Server](https://github.com/JackKuo666/ClinicalTrials-MCP-Server) | mcp-server | 18 | 2025-04-09 | ClinicalTrials.gov search and study detail MCP (Python) |
| [HolobiomicsLab/asb-skill-collections](https://github.com/HolobiomicsLab/asb-skill-collections) | skill-suite | 16 | 2026-09-20 | Evidence-grounded skill and tool collections for scientific AI agents |

## Biological Databases / Pathways / Chemistry / Drug Discovery MCP

| repo | type | stars | last push | focus / notes |
|---|---|---:|---|---|
| [Augmented-Nature/ChEMBL-MCP-Server](https://github.com/Augmented-Nature/ChEMBL-MCP-Server) | mcp-server | 89 | 2025-12-21 | Unofficial ChEMBL MCP for compound, target, and bioactivity lookups (Node.js) |
| [longevity-genie/biothings-mcp](https://github.com/longevity-genie/biothings-mcp) | mcp-server | 37 | 2025-11-03 | BioThings APIs (MyGene, MyVariant, MyChem) MCP from the Holy Bio MCP family |
| [longevity-genie/gget-mcp](https://github.com/longevity-genie/gget-mcp) | mcp-server | 33 | 2025-10-27 | MCP wrapper for gget bioinformatics tools |
| [biocontext-ai/knowledgebase-mcp](https://github.com/biocontext-ai/knowledgebase-mcp) | mcp-server | 31 | 2026-10-12 | BioContextAI knowledgebase MCP bundling common biomedical databases; self-hosted or remote |
| [ammawla/encode-toolkit](https://github.com/ammawla/encode-toolkit) | mcp-server | 21 | 2026-09-27 | ENCODE genomic data toolkit |
| [Augmented-Nature/Augmented-Nature-UniProt-MCP-Server](https://github.com/Augmented-Nature/Augmented-Nature-UniProt-MCP-Server) | mcp-server | 21 | 2025-12-21 | Unofficial UniProt MCP with 26 protein lookup, comparative, and structural tools (Node.js) |
| [longevity-genie/opengenes-mcp](https://github.com/longevity-genie/opengenes-mcp) | mcp-server | 21 | 2025-10-14 | OpenGenes aging-gene database MCP: lifespan experiments, hallmarks of aging, longevity variants |
| [longevity-genie/holy-bio-mcp](https://github.com/longevity-genie/holy-bio-mcp) | mcp-suite | 20 | 2025-07-14 | Umbrella for the Holy Bio MCP family (gget, BioThings, OpenGenes, SynergyAge, pharmacology); Bio x AI Hackathon 2025 winner |
| [tamerh/biobtree](https://github.com/tamerh/biobtree) | mcp-server | 20 | 2026-10-14 | BioBTree v2, 70+ biomedical datasets |
| [nickzren/opentargets-mcp](https://github.com/nickzren/opentargets-mcp) | mcp-server | 19 | 2026-10-09 | Open Targets MCP for target-disease associations and drug evidence |
| [Augmented-Nature/Reactome-MCP-Server](https://github.com/Augmented-Nature/Reactome-MCP-Server) | mcp-server | 12 | 2025-12-21 | Unofficial Reactome MCP over the Content Service for curated pathway data |
| [cyanheads/pubchem-mcp-server](https://github.com/cyanheads/pubchem-mcp-server) | mcp-server | 10 | 2026-10-24 | PubChem compounds, properties, safety, and bioactivity |
| [longevity-genie/synergy-age-mcp](https://github.com/longevity-genie/synergy-age-mcp) | mcp-server | 10 | 2025-08-25 | SynergyAge MCP for genetic interventions and their combined effects on lifespan |
| [Augmented-Nature/SureChEMBL-MCP-Server](https://github.com/Augmented-Nature/SureChEMBL-MCP-Server) | mcp-server | 8 | 2025-12-21 | Unofficial SureChEMBL MCP for chemical patent search (Node.js) |
| [donbr/lifesciences-research](https://github.com/donbr/lifesciences-research) | mcp-suite | 8 | 2026-10-15 | Open Targets, ChEMBL, UniProt |
| [effieklimi/ensembl-mcp-server](https://github.com/effieklimi/ensembl-mcp-server) | mcp-server | 8 | 2026-02-11 | Ensembl REST MCP for genes, sequences, variants, and comparative genomics (TypeScript) |
| [hlydecker/ucsc-genome-mcp](https://github.com/hlydecker/ucsc-genome-mcp) | mcp-server | 6 | 2025-11-13 | UCSC Genome Browser API MCP for tracks and sequence lookups |
| [longevity-genie/pharmacology-mcp](https://github.com/longevity-genie/pharmacology-mcp) | mcp-server | 6 | 2025-09-02 | Pharmacology database MCP from the Holy Bio MCP family (targets, ligands, interactions) |
| [EBISPOT/GrEBI](https://github.com/EBISPOT/GrEBI) | mcp-server | 5 | 2026-10-21 | biomedical data integration, API/MCP server |
| [Augmented-Nature/STRING-db-MCP-Server](https://github.com/Augmented-Nature/STRING-db-MCP-Server) | mcp-server | 4 | 2025-12-21 | Unofficial STRING MCP: protein interaction networks, functional enrichment, and homolog lookup |
| [Lucas-Servi/kegg-mcp-server-python](https://github.com/Lucas-Servi/kegg-mcp-server-python) | mcp-server | 3 | 2026-10-16 | KEGG REST MCP for pathways, genes, and compounds (Python) |
| [smaniches/uniprot-mcp](https://github.com/smaniches/uniprot-mcp) | mcp-server | 3 | 2026-10-26 | Auditable UniProt MCP with release pinning and offline replay |

## Research Agent Apps / Workspaces

| repo | type | stars | last push | focus / notes |
|---|---|---:|---|---|
| [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) | agent-app | 5907 | 2026-10-19 | Research, experiments, writing, and submission support for Claude Code and Codex CLI |
| [snap-stanford/Biomni](https://github.com/snap-stanford/Biomni) | agent-app | 4012 | 2026-10-19 | General-purpose biomedical AI agent with retrieval-augmented planning and code execution (Apache-2.0; executes LLM-written code, sandbox recommended) |
| [yb2460/harness-anything](https://github.com/yb2460/harness-anything) | framework | 2538 | 2026-10-09 | WPS, MS Office, Zotero, academic skills, and document automation |
| [K-Dense-AI/k-dense-byok](https://github.com/K-Dense-AI/k-dense-byok) | agent-app | 1401 | 2026-10-16 | Desktop AI co-scientist based on scientific-agent-skills |
| [beita6969/ScienceClaw](https://github.com/beita6969/ScienceClaw) | agent-app | 1019 | 2026-10-16 | Self-evolving research assistant with skills and persistent memory |
| [AgentTeam-TaichuAI/ScienceClaw](https://github.com/AgentTeam-TaichuAI/ScienceClaw) | agent-app | 674 | 2026-05-09 | Research assistant built with LangChain DeepAgents and sandboxing |
| [ymx10086/ResearchClaw](https://github.com/ymx10086/ResearchClaw) | agent-app | 315 | 2026-04-04 | Literature reviews, notes, experiment tracking, and paper writing |
| [WenyuChiou/research-hub](https://github.com/WenyuChiou/research-hub) | agent-app | 66 | 2026-10-26 | Zotero, Obsidian, NotebookLM, CLI/MCP/REST/dashboard |

## Figures / PDF / LaTeX / Research Artifact Tools

| repo | type | stars | last push | focus / notes |
|---|---|---:|---|---|
| [PDFMathTranslate/PDFMathTranslate](https://github.com/PDFMathTranslate/PDFMathTranslate) | tool | 37880 | 2026-10-26 | Scientific PDF translation that preserves layout, with MCP, Docker, and Zotero support |
| [llmsresearch/paperbanana](https://github.com/llmsresearch/paperbanana) | tool | 2419 | 2026-09-17 | Automated academic figures, diagrams, and research visuals |
| [Dsadd4/AgentFigureGallery](https://github.com/Dsadd4/AgentFigureGallery) | skill | 171 | 2026-09-05 | Scientific plotting skill for Claude, Codex, and Cursor |

## Awesome Lists / Registries / Further Discovery

| repo | type | stars | last push | focus / notes |
|---|---|---:|---|---|
| [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) | directory | 96880 | 2026-10-23 | General MCP directory with Biology, Medicine, and Bioinformatics sections |
| [anthropics/life-sciences](https://github.com/anthropics/life-sciences) | registry | 624 | 2026-10-23 | Claude life-sciences MCP and skills directory |
| [InternScience/Awesome-Scientific-Skills](https://github.com/InternScience/Awesome-Scientific-Skills) | directory | 577 | 2026-08-13 | Scientific research agent skills directory |
| [WenyuChiou/ai-research-skills](https://github.com/WenyuChiou/ai-research-skills) | directory | 407 | 2026-10-26 | literature review, research design, manuscript writing |
| [BioTender-max/awesome-bio-agent-skills](https://github.com/BioTender-max/awesome-bio-agent-skills) | directory | 207 | 2026-07-01 | Biomedical agent skills directory covering genomics, proteomics, single-cell analysis, clinical AI, and protein design |
| [Epsilon617/Codex-Academic-Skills](https://github.com/Epsilon617/Codex-Academic-Skills) | skill-suite | 195 | 2026-06-16 | Codex research-oriented skills directory |
| [GoekeLab/awesome-genomic-skills](https://github.com/GoekeLab/awesome-genomic-skills) | directory | 127 | 2026-09-22 | genomics/bioinformatics agent skills, MCP, benchmarks |
| [O0000-code/awesome-academic-skills](https://github.com/O0000-code/awesome-academic-skills) | directory | 51 | 2026-10-25 | Academic agent skills organized by the research lifecycle |
| [biocontext-ai/registry](https://github.com/biocontext-ai/registry) | registry | 23 | 2026-10-20 | BioContextAI registry of biomedical MCP servers; also a discovery source for this catalog |
| [JuneYaooo/awesome-medical-ai-skills](https://github.com/JuneYaooo/awesome-medical-ai-skills) | directory | 16 | 2026-10-22 | Curated medical and healthcare agent skills, MCP servers, and tools |
| [Harsh9005/awesome-scientific-ai-tools](https://github.com/Harsh9005/awesome-scientific-ai-tools) | directory | 10 | 2026-05-15 | AI tools, MCP servers, and agent skills for scientific research |
| [chrisliu298/awesome-research-agents](https://github.com/chrisliu298/awesome-research-agents) | directory | 4 | 2026-05-19 | research agents, skill libraries, autonomous research loops, paper-writing pipelines |
| [biocontext-ai/meta-mcp](https://github.com/biocontext-ai/meta-mcp) | mcp-server | 2 | 2026-05-18 | Meta MCP that exposes every server in the BioContextAI registry with minimal context |

## Inclusion / Exclusion Rules

- Include repositories that clearly target research, paper writing, literature, Zotero/PubMed/arXiv/Semantic Scholar, medicine, bioinformatics, or life sciences, and expose that capability as a skill, plugin, MCP server, agent workflow, or agent-ready tool.
- Keep low-star repositories when they are direct, domain-specific, and interface-ready.
- Exclude ordinary tutorials, book inventory apps, generic agent infrastructure without a research angle, mirror-only forks without meaningful additions, and empty shells with no useful description.
- Notes must say what the repo does and how it differs from neighbours in the same category; a bare database name is not a note.

## Coverage Notes

GitHub Search cannot guarantee complete coverage. New repositories enter through the weekly discovery report in `discovery/candidates.md`, awesome-list cross-references, and manual triage recorded in `data/triage.tsv`.
<!-- CATALOG:END -->

## License

Scripts are MIT licensed. Catalog data and generated documents are CC BY 4.0. See [LICENSE](LICENSE).
