# GitHub Research, Paper Writing, Bioinformatics AI Skill/Plugin Repos

Search date: 2026-07-13

Scope: AI-agent-related skills, plugins, MCP servers, and agent-ready workflows, with emphasis on research, paper writing, literature search, Zotero/arXiv/PubMed/Semantic Scholar, life sciences, bioinformatics, and medical research. This catalog does not attempt to enumerate traditional scientific software plugin ecosystems or generic agent infrastructure with no clear research relevance.

Notes: GitHub Search cannot mathematically guarantee complete coverage. `data/repos.seed.tsv` is the manually maintained source for scope and categories, and `scripts/update_catalog.py` fetches or reuses GitHub metadata to generate the Markdown outputs. Star counts are GitHub metadata, not a quality judgment. Some 2026 repositories have unusually high star counts; review source code, license, dependencies, network behavior, and file permissions before use.

## Update Instructions

- Local validation: `python3 scripts/update_catalog.py --check`
- Regenerate from cached metadata: `python3 scripts/update_catalog.py --from-curated`
- Refresh GitHub metadata: `python3 scripts/update_catalog.py --refresh`
- Discover candidate repos for manual review: `python3 scripts/discover_candidates.py --limit-per-query 20 --min-stars 5 --output discovery/candidates.md`
- Scheduled updates run through `.github/workflows/update-catalog.yml` every Monday at 03:17 UTC.
- To extend the list, edit `data/repos.seed.tsv` first, then run a refresh or regeneration command.

## General Research / AI4S Skill Suites

| repo | type | stars | last update | focus / notes |
|---|---:|---:|---|---|
| [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | Skill suite | 37560 | 2026-07-13 | Academic research skills: research -> write -> review -> revise -> finalize |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | Skill suite | 30780 | 2026-07-13 | Agent Skills standard for scientific research, biology, chemistry, medicine, and drug discovery |
| [wanshuiyin/Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | Skill suite | 13323 | 2026-07-13 | ARIS automated research loop, idea discovery, and experiment automation |
| [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) | Skill suite | 10651 | 2026-07-13 | AI research and engineering skills for Claude, Codex, and Gemini |
| [Imbad0202/academic-research-skills-codex](https://github.com/Imbad0202/academic-research-skills-codex) | Skill suite | 6095 | 2026-07-13 | Codex-native academic research workflow |
| [openai/plugins](https://github.com/openai/plugins) | Plugin/skills | 4517 | 2026-07-13 | OpenAI Codex plugins, including life-science-research |
| [brycewang-stanford/Auto-Empirical-Research-Skills](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills) | Skill library | 2822 | 2026-07-13 | Empirical social science research with 23,000+ agent skills |
| [google-deepmind/science-skills](https://github.com/google-deepmind/science-skills) | Skill suite | 2347 | 2026-07-13 | DeepMind science agent skills |
| [zLanqing/codex-claude-academic-skills](https://github.com/zLanqing/codex-claude-academic-skills) | Skills | 1810 | 2026-07-13 | Chinese-language research reading, writing, and scientific computing |
| [Weizhena/Deep-Research-skills](https://github.com/Weizhena/Deep-Research-skills) | Skill | 1623 | 2026-07-13 | Structured deep research skill, Claude/OpenCode/Codex |
| [luwill/research-skills](https://github.com/luwill/research-skills) | Skills | 716 | 2026-07-12 | Common research practices and workflows packaged as agent skills |
| [chrisblattman/claudeblattman](https://github.com/chrisblattman/claudeblattman) | Academic setup | 424 | 2026-07-13 | Claude Code for academics: skills, agents, setup guides |
| [fcakyon/phd-skills](https://github.com/fcakyon/phd-skills) | Skills | 326 | 2026-07-13 | PhD research: reproduction, experimental design, paper review, and result comparison |
| [chtc66/academic-skills](https://github.com/chtc66/academic-skills) | Skills | 310 | 2026-07-13 | Paper reading, surveys, experiment summaries, rebuttals, and lab updates |
| [ai4s-research/ai4s-skills](https://github.com/ai4s-research/ai4s-skills) | Skill suite | 144 | 2026-07-12 | AI for Science: topic exploration, literature survey, experiments, writing, and integrity audit |
| [AlterLab-IEU/AlterLab-Academic-Skills](https://github.com/AlterLab-IEU/AlterLab-Academic-Skills) | Skill library | 40 | 2026-07-11 | 239 evaluated academic skills, including bioinformatics and clinical research |
| [s-choung/Research-Skills](https://github.com/s-choung/Research-Skills) | Skills/agents | 28 | 2026-07-06 | Research writing, figures, document automation, and Korean academic materials |
| [JhonHander/academic-agent-toolkit](https://github.com/JhonHander/academic-agent-toolkit) | Toolkit | 7 | 2026-06-28 | Installer for MCP tools and AI research skills |

## Paper Writing / Peer Review / Submission Skills

| repo | type | stars | last update | focus / notes |
|---|---:|---:|---|---|
| [Master-cai/Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills) | Skills | 5049 | 2026-07-13 | ML/CV/NLP paper writing for Codex, Claude, and Gemini |
| [WUBING2023/PaperSpine](https://github.com/WUBING2023/PaperSpine) | Skill | 3970 | 2026-07-13 | Central paper argumentation, strong-paper learning, manuscript rewriting, and LaTeX-safe audits |
| [PaperDebugger/paperdebugger](https://github.com/PaperDebugger/paperdebugger) | Plugin/agent | 1508 | 2026-07-11 | Academic writing, peer review, and editing |
| [fakerqwq/social-science-paper-writing-skill](https://github.com/fakerqwq/social-science-paper-writing-skill) | Skill | 153 | 2026-07-13 | Social science paper writing, topic selection, literature reviews, and citation risk checks |
| [SNL-UCSB/paper-writing-skill](https://github.com/SNL-UCSB/paper-writing-skill) | Skill | 107 | 2026-07-11 | Brainstorm -> Draft -> Evaluate -> Write -> Compress paper writing |
| [SyntaxSmith/nature-writing-skill](https://github.com/SyntaxSmith/nature-writing-skill) | Skill | 63 | 2026-07-12 | Nature-family paper writing |
| [cLin-c/paper-skill](https://github.com/cLin-c/paper-skill) | Skill | 50 | 2026-07-13 | Paper writing, polishing, peer review, translation, and submission |
| [fuhaoda/stats-paper-writing-agent-skills](https://github.com/fuhaoda/stats-paper-writing-agent-skills) | Skill | 28 | 2026-07-03 | Agent skills for statistics paper writing |
| [MetaQiu/Trivium](https://github.com/MetaQiu/Trivium) | Skill/workflow | 24 | 2026-06-08 | Multi-agent collaborative paper writing for Claude, Codex, and Gemini |
| [Zhangyanbo/vibe-paper-writing](https://github.com/Zhangyanbo/vibe-paper-writing) | Skill | 22 | 2026-07-07 | Convert notes, chats, and emails into LaTeX academic papers |
| [AGISAFETYLAB/Paper-Writing-skill](https://github.com/AGISAFETYLAB/Paper-Writing-skill) | Skill | 13 | 2026-07-09 | Planning, writing, polishing, figures, and citation checks for CS, medical, and finance papers |
| [dailycafi/biomed-paper-writing-skill](https://github.com/dailycafi/biomed-paper-writing-skill) | Skill | 2 | 2026-04-02 | Biomedical and pharmaceutical paper writing with CONSORT, STROBE, PRISMA, and ARRIVE |
| [Jason-0409-G/scriptorium](https://github.com/Jason-0409-G/scriptorium) | Skill | 1 | 2026-06-25 | DOI-verified literature library, NCBI/UniProt/PDB/AlphaFold integration, writing, and review |

## Literature Search / Scholarly Search MCP

| repo | type | stars | last update | focus / notes |
|---|---:|---:|---|---|
| [blazickjp/arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server) | MCP | 2953 | 2026-07-12 | arXiv search and paper analysis MCP |
| [openags/paper-search-mcp](https://github.com/openags/paper-search-mcp) | MCP/CLI/skills | 2118 | 2026-07-13 | Paper search and download for arXiv, PubMed, bioRxiv, and related sources |
| [Dianel555/paper-search-mcp-nodejs](https://github.com/Dianel555/paper-search-mcp-nodejs) | MCP | 175 | 2026-07-13 | Paper search and download for Web of Science, arXiv, and related sources |
| [andybrandt/mcp-simple-pubmed](https://github.com/andybrandt/mcp-simple-pubmed) | MCP | 169 | 2026-07-08 | PubMed medical literature search MCP |
| [Agents365-ai/asta-skill](https://github.com/Agents365-ai/asta-skill) | Skill | 164 | 2026-07-12 | Asta/Semantic Scholar MCP routing |
| [ShZhao27208/Aut_Sci_Write](https://github.com/ShZhao27208/Aut_Sci_Write) | Skill suite | 162 | 2026-07-11 | WoS, Elsevier, and Springer search/download, reviews, Zotero, PPT, and HTML |
| [zongmin-yu/semantic-scholar-fastmcp-mcp-server](https://github.com/zongmin-yu/semantic-scholar-fastmcp-mcp-server) | MCP | 160 | 2026-07-08 | Semantic Scholar API FastMCP server |
| [Darkroaster/pubmearch](https://github.com/Darkroaster/pubmearch) | MCP | 150 | 2026-06-04 | PubMed MCP server |
| [takashiishida/arxiv-latex-mcp](https://github.com/takashiishida/arxiv-latex-mcp) | MCP | 140 | 2026-07-05 | arXiv LaTeX source parsing |
| [cyanheads/pubmed-mcp-server](https://github.com/cyanheads/pubmed-mcp-server) | MCP | 121 | 2026-07-05 | PubMed/Europe PMC/Unpaywall, MeSH, full text |
| [JackKuo666/PubMed-MCP-Server](https://github.com/JackKuo666/PubMed-MCP-Server) | MCP | 121 | 2026-07-09 | PubMed article search, access, and analysis |
| [afrise/academic-search-mcp-server](https://github.com/afrise/academic-search-mcp-server) | MCP | 118 | 2026-07-09 | Semantic Scholar + Crossref |
| [grll/pubmedmcp](https://github.com/grll/pubmedmcp) | MCP | 118 | 2026-06-27 | PubMed data MCP |
| [JackKuo666/semanticscholar-MCP-Server](https://github.com/JackKuo666/semanticscholar-MCP-Server) | MCP | 77 | 2026-07-10 | Semantic Scholar paper/author/citation/reference |
| [benedict2310/Scientific-Papers-MCP](https://github.com/benedict2310/Scientific-Papers-MCP) | MCP | 54 | 2026-06-25 | arXiv + OpenAlex scientific papers |
| [connerlambden/bgpt-mcp](https://github.com/connerlambden/bgpt-mcp) | MCP/REST | 37 | 2026-07-10 | Scientific paper evidence search |
| [akapet00/semantic-scholar-mcp](https://github.com/akapet00/semantic-scholar-mcp) | MCP | 28 | 2026-07-09 | Semantic Scholar paper search and analysis |
| [masa-med-ai/pubmed-systematic-review](https://github.com/masa-med-ai/pubmed-systematic-review) | Skill | 25 | 2026-06-26 | Lightweight systematic reviews integrated with a PubMed MCP |
| [lstudlo/ScholarMCP](https://github.com/lstudlo/ScholarMCP) | MCP | 23 | 2026-07-13 | Literature search, PDF ingestion, and reference management |
| [TaewoooPark/scholar-megasearch](https://github.com/TaewoooPark/scholar-megasearch) | Skill | 20 | 2026-07-12 | 20+ scholarly databases with multi-source search and PDF retrieval |
| [u9401066/pubmed-search-mcp](https://github.com/u9401066/pubmed-search-mcp) | MCP | 20 | 2026-06-24 | PubMed/Europe PMC/CORE/OpenAlex, citation networks, PICO |
| [zongmin-yu/semantic-scholar-skills](https://github.com/zongmin-yu/semantic-scholar-skills) | Skill/MCP | 19 | 2026-07-10 | S2-first discovery engine |
| [aringadre76/mcp-for-research](https://github.com/aringadre76/mcp-for-research) | MCP | 13 | 2026-05-12 | PubMed, Google Scholar, arXiv, JSTOR |

## Zotero / CNKI / Google Scholar / Reference Management

| repo | type | stars | last update | focus / notes |
|---|---:|---:|---|---|
| [54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp) | MCP | 4245 | 2026-07-13 | Connect Zotero libraries to Claude and AI assistants |
| [papersgpt/papersgpt-for-zotero](https://github.com/papersgpt/papersgpt-for-zotero) | Zotero plugin/MCP | 2507 | 2026-07-12 | Zotero AI/MCP plugin with multi-model paper Q&A |
| [yilewang/llm-for-zotero](https://github.com/yilewang/llm-for-zotero) | Zotero agent | 2262 | 2026-07-13 | Research agent system based on a Zotero library |
| [cookjohn/zotero-mcp](https://github.com/cookjohn/zotero-mcp) | Zotero plugin/MCP | 995 | 2026-07-13 | Deep integration between Zotero and AI assistants |
| [cookjohn/cnki-skills](https://github.com/cookjohn/cnki-skills) | Skills | 750 | 2026-07-13 | CNKI search, PDFs, and Zotero export |
| [cookjohn/gs-skills](https://github.com/cookjohn/gs-skills) | Skills | 449 | 2026-07-13 | Google Scholar search, citation tracking, and Zotero export |
| [kaliaboi/mcp-zotero](https://github.com/kaliaboi/mcp-zotero) | MCP | 164 | 2026-07-10 | Connect Claude Desktop to Zotero Cloud |
| [kujenga/zotero-mcp](https://github.com/kujenga/zotero-mcp) | MCP | 158 | 2026-07-09 | Zotero API MCP server |
| [introfini/ZotSeek](https://github.com/introfini/ZotSeek) | Zotero plugin/MCP | 149 | 2026-07-12 | Zotero semantic search with local privacy and built-in MCP |
| [TonybotNi/ZotLink](https://github.com/TonybotNi/ZotLink) | MCP | 138 | 2026-06-05 | Save arXiv, CVF, bioRxiv, and medRxiv papers to Zotero |
| [dralkh/seerai](https://github.com/dralkh/seerai) | Zotero plugin/MCP | 64 | 2026-07-10 | Zotero AI plugin, RAG, OCR, systematic reviews, MCP, skills |
| [gyger/mcp-pyzotero](https://github.com/gyger/mcp-pyzotero) | MCP | 55 | 2026-03-29 | Local Zotero MCP connector |
| [Xevos117/mcp-zotero](https://github.com/Xevos117/mcp-zotero) | MCP | 29 | 2026-06-21 | Zotero library operations, DOI, PDF, Unpaywall, docx citation fields |
| [cookjohn/pm-skills](https://github.com/cookjohn/pm-skills) | Skills | 17 | 2026-06-14 | PubMed literature search, citation export, Zotero |

## Bioinformatics / Omics / Single-Cell Skills

| repo | type | stars | last update | focus / notes |
|---|---:|---:|---|---|
| [GPTomics/bioSkills](https://github.com/GPTomics/bioSkills) | Skill suite | 1014 | 2026-07-13 | RNA-seq, scRNA, variant, multi-omics |
| [jaechang-hits/SciAgent-Skills](https://github.com/jaechang-hits/SciAgent-Skills) | Skill library | 233 | 2026-07-12 | 197 life-science and bioinformatics skills |
| [TianGzlab/OmicsClaw](https://github.com/TianGzlab/OmicsClaw) | Agent app | 149 | 2026-07-12 | Multi-omics analysis through manuscript generation |
| [adaptyvbio/protein-design-skills](https://github.com/adaptyvbio/protein-design-skills) | Skill suite | 148 | 2026-07-12 | Protein design |
| [swaruplab/operon](https://github.com/swaruplab/operon) | Bioinformatics IDE | 90 | 2026-07-10 | Claude Code bioinformatics IDE and protocols |
| [charlesxu90/ProteinMCP](https://github.com/charlesxu90/ProteinMCP) | Agentic framework/MCP suite | 61 | 2026-07-12 | Agentic framework for autonomous protein engineering with Claude Code workflow skills and 38 supported MCPs |
| [variomeanalytics/bioinformatics-agent-skills](https://github.com/variomeanalytics/bioinformatics-agent-skills) | MCP/skills | 58 | 2026-06-30 | Knowledge graph over 78 bioinformatics workflows |
| [cafferychen777/ChatSpatial](https://github.com/cafferychen777/ChatSpatial) | MCP | 40 | 2026-07-05 | Natural-language analysis for spatial transcriptomics |
| [ma-compbio-lab/SkillFoundry](https://github.com/ma-compbio-lab/SkillFoundry) | Skill framework | 36 | 2026-06-24 | Computational biology skill discovery and validation |
| [Agents365-ai/seurat-skill](https://github.com/Agents365-ai/seurat-skill) | Skill | 3 | 2026-05-14 | Seurat v5 single-cell analysis |
| [igvteam/igv-mcp](https://github.com/igvteam/igv-mcp) | MCP | 2 | 2026-03-10 | IGV genome viewer control |
| [Bioconductor/ai-agent-skills](https://github.com/Bioconductor/ai-agent-skills) | Skill suite | 0 | 2026-07-08 | R/Bioconductor and statistical bioinformatics |

## Biomedical / Clinical / Medical Research

| repo | type | stars | last update | focus / notes |
|---|---:|---:|---|---|
| [FreedomIntelligence/OpenClaw-Medical-Skills](https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills) | Skill library | 2832 | 2026-07-13 | Large OpenClaw medical AI skills collection |
| [mims-harvard/ToolUniverse](https://github.com/mims-harvard/ToolUniverse) | Tool/skills | 1564 | 2026-07-13 | Tool universe for biomedical AI scientists |
| [aipoch/medical-research-skills](https://github.com/aipoch/medical-research-skills) | Skill suite | 1412 | 2026-07-13 | Medical research, protocols, data analysis, and academic writing |
| [LeonChaoX/qinyan-academic-skills](https://github.com/LeonChaoX/qinyan-academic-skills) | Skill library | 591 | 2026-07-13 | 177 academic research skills, including bioinformatics, drug discovery, and clinical medicine |
| [genomoncology/biomcp](https://github.com/genomoncology/biomcp) | MCP | 547 | 2026-07-12 | BioMCP for clinical trials, genomic data, and medical literature |
| [anthropics/life-sciences](https://github.com/anthropics/life-sciences) | Marketplace | 523 | 2026-07-11 | Claude life-sciences MCP and skills directory |
| [Cicatriiz/healthcare-mcp-public](https://github.com/Cicatriiz/healthcare-mcp-public) | MCP | 121 | 2026-07-10 | Medical data from FDA, PubMed, medRxiv, clinical trials, ICD-10, and related sources |
| [JamesANZ/medical-mcp](https://github.com/JamesANZ/medical-mcp) | MCP | 103 | 2026-07-08 | FDA, WHO, PubMed, Google Scholar, RxNorm |
| [cyanheads/clinicaltrialsgov-mcp-server](https://github.com/cyanheads/clinicaltrialsgov-mcp-server) | MCP | 81 | 2026-07-09 | ClinicalTrials.gov search, details, results, and patient matching |
| [pascalwhoop/medical-mcps](https://github.com/pascalwhoop/medical-mcps) | MCP collection | 22 | 2026-07-02 | MCP tool collection for major biomedical databases |
| [lynnlangit/precision-medicine-mcp](https://github.com/lynnlangit/precision-medicine-mcp) | MCP platform | 21 | 2026-07-13 | Precision medicine across multi-omics, genomics, and spatial transcriptomics |
| [JackKuo666/ClinicalTrials-MCP-Server](https://github.com/JackKuo666/ClinicalTrials-MCP-Server) | MCP | 16 | 2026-04-23 | ClinicalTrials.gov |
| [HolobiomicsLab/asb-skill-collections](https://github.com/HolobiomicsLab/asb-skill-collections) | Skill collection | 13 | 2026-07-11 | Evidence-grounded skill and tool collections for scientific AI agents |

## Biological Databases / Structural Biology / Chemistry / Drug Discovery MCP

| repo | type | stars | last update | focus / notes |
|---|---:|---:|---|---|
| [Augmented-Nature/ChEMBL-MCP-Server](https://github.com/Augmented-Nature/ChEMBL-MCP-Server) | MCP | 88 | 2026-06-12 | ChEMBL |
| [ammawla/encode-toolkit](https://github.com/ammawla/encode-toolkit) | MCP/Claude plugin | 37 | 2026-07-08 | ENCODE genomic data toolkit |
| [PDBeurope/PDBe-MCP-Servers](https://github.com/PDBeurope/PDBe-MCP-Servers) | MCP | 36 | 2026-06-25 | PDBe and protein structures |
| [Augmented-Nature/AlphaFold-MCP-Server](https://github.com/Augmented-Nature/AlphaFold-MCP-Server) | MCP | 35 | 2026-06-12 | AlphaFold Protein Structure Database |
| [longevity-genie/biothings-mcp](https://github.com/longevity-genie/biothings-mcp) | MCP | 33 | 2026-07-05 | BioThings MCP |
| [longevity-genie/gget-mcp](https://github.com/longevity-genie/gget-mcp) | MCP | 30 | 2026-07-05 | MCP wrapper for gget bioinformatics tools |
| [Augmented-Nature/PDB-MCP-Server](https://github.com/Augmented-Nature/PDB-MCP-Server) | MCP | 25 | 2026-06-12 | Protein Data Bank |
| [Augmented-Nature/Augmented-Nature-UniProt-MCP-Server](https://github.com/Augmented-Nature/Augmented-Nature-UniProt-MCP-Server) | MCP | 19 | 2026-03-29 | UniProt protein database |
| [nickzren/opentargets-mcp](https://github.com/nickzren/opentargets-mcp) | MCP | 19 | 2026-06-27 | Open Targets |
| [tamerh/biobtree](https://github.com/tamerh/biobtree) | MCP/graph DB | 19 | 2026-07-07 | BioBTree v2, 70+ biomedical datasets |
| [cyanheads/pubchem-mcp-server](https://github.com/cyanheads/pubchem-mcp-server) | MCP | 9 | 2026-07-03 | PubChem compounds, properties, safety, and bioactivity |
| [effieklimi/ensembl-mcp-server](https://github.com/effieklimi/ensembl-mcp-server) | MCP | 8 | 2026-05-28 | Ensembl REST API |
| [Augmented-Nature/SureChEMBL-MCP-Server](https://github.com/Augmented-Nature/SureChEMBL-MCP-Server) | MCP | 7 | 2026-01-28 | SureChEMBL chemical patent database |
| [donbr/lifesciences-research](https://github.com/donbr/lifesciences-research) | MCP wrappers | 7 | 2026-06-27 | Open Targets, ChEMBL, UniProt |
| [hlydecker/ucsc-genome-mcp](https://github.com/hlydecker/ucsc-genome-mcp) | MCP | 6 | 2026-07-05 | UCSC Genome Browser API |
| [cyanheads/protein-mcp-server](https://github.com/cyanheads/protein-mcp-server) | MCP | 5 | 2026-07-03 | PDB and AlphaFold protein structure and annotation federation |
| [PabloPauling/posebusters-mcp-server](https://github.com/PabloPauling/posebusters-mcp-server) | MCP | 5 | 2026-03-30 | PoseBusters molecular pose validation |
| [EBISPOT/GrEBI](https://github.com/EBISPOT/GrEBI) | API/MCP | 4 | 2026-07-10 | biomedical data integration, API/MCP server |
| [Lucas-Servi/kegg-mcp-server-python](https://github.com/Lucas-Servi/kegg-mcp-server-python) | MCP | 3 | 2026-06-29 | KEGG REST API |
| [smaniches/alphafold-sovereign-mcp](https://github.com/smaniches/alphafold-sovereign-mcp) | MCP | 3 | 2026-07-12 | AlphaFold DB plus eight public sources with a local knowledge graph |
| [smaniches/uniprot-mcp](https://github.com/smaniches/uniprot-mcp) | MCP | 3 | 2026-07-13 | Auditable UniProt MCP with release pinning and offline replay |

## Research Agent Apps / Workspaces

| repo | type | stars | last update | focus / notes |
|---|---:|---:|---|---|
| [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) | Research assistant | 4600 | 2026-07-13 | Research, experiments, writing, and submission support for Claude Code and Codex CLI |
| [yb2460/harness-anything](https://github.com/yb2460/harness-anything) | Agent harness | 931 | 2026-07-13 | WPS, MS Office, Zotero, academic skills, and document automation |
| [K-Dense-AI/k-dense-byok](https://github.com/K-Dense-AI/k-dense-byok) | Agent app | 910 | 2026-07-13 | Desktop AI co-scientist based on scientific-agent-skills |
| [beita6969/ScienceClaw](https://github.com/beita6969/ScienceClaw) | Agent app | 864 | 2026-07-10 | Self-evolving research assistant with skills and persistent memory |
| [AgentTeam-TaichuAI/ScienceClaw](https://github.com/AgentTeam-TaichuAI/ScienceClaw) | Agent app | 552 | 2026-07-12 | Research assistant built with LangChain DeepAgents and sandboxing |
| [ymx10086/ResearchClaw](https://github.com/ymx10086/ResearchClaw) | Research assistant | 308 | 2026-07-08 | Literature reviews, notes, experiment tracking, and paper writing |
| [WenyuChiou/research-hub](https://github.com/WenyuChiou/research-hub) | Research workspace | 35 | 2026-07-10 | Zotero, Obsidian, NotebookLM, CLI/MCP/REST/dashboard |

## Figures / PDF / LaTeX / Research Artifact Tools

| repo | type | stars | last update | focus / notes |
|---|---:|---:|---|---|
| [PDFMathTranslate/PDFMathTranslate](https://github.com/PDFMathTranslate/PDFMathTranslate) | Tool/MCP/Zotero | 35538 | 2026-07-13 | Scientific PDF translation that preserves layout, with MCP, Docker, and Zotero support |
| [llmsresearch/paperbanana](https://github.com/llmsresearch/paperbanana) | Research visual tool | 2104 | 2026-07-12 | Automated academic figures, diagrams, and research visuals |
| [Dsadd4/AgentFigureGallery](https://github.com/Dsadd4/AgentFigureGallery) | Skill | 132 | 2026-07-08 | Scientific plotting skill for Claude, Codex, and Cursor |

## Awesome Lists / Registries / Further Discovery

| repo | type | stars | last update | focus / notes |
|---|---:|---:|---|---|
| [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) | Directory | 90665 | 2026-07-13 | General MCP directory with Biology, Medicine, and Bioinformatics sections |
| [InternScience/Awesome-Scientific-Skills](https://github.com/InternScience/Awesome-Scientific-Skills) | Directory | 475 | 2026-07-13 | Scientific research agent skills directory |
| [WenyuChiou/ai-research-skills](https://github.com/WenyuChiou/ai-research-skills) | Skill catalog | 149 | 2026-07-13 | literature review, research design, manuscript writing |
| [Epsilon617/Codex-Academic-Skills](https://github.com/Epsilon617/Codex-Academic-Skills) | Skills | 148 | 2026-07-12 | Codex research-oriented skills directory |
| [BioTender-max/awesome-bio-agent-skills](https://github.com/BioTender-max/awesome-bio-agent-skills) | Directory | 96 | 2026-07-13 | Biomedical agent skills directory covering genomics, proteomics, single-cell analysis, clinical AI, and protein design |
| [GoekeLab/awesome-genomic-skills](https://github.com/GoekeLab/awesome-genomic-skills) | Directory | 68 | 2026-07-11 | genomics/bioinformatics agent skills, MCP, benchmarks |
| [O0000-code/awesome-academic-skills](https://github.com/O0000-code/awesome-academic-skills) | Directory | 11 | 2026-07-12 | Academic agent skills organized by the research lifecycle |
| [Harsh9005/awesome-scientific-ai-tools](https://github.com/Harsh9005/awesome-scientific-ai-tools) | Directory | 7 | 2026-07-02 | AI tools, MCP servers, and agent skills for scientific research |
| [chrisliu298/awesome-research-agents](https://github.com/chrisliu298/awesome-research-agents) | Directory | 3 | 2026-06-29 | research agents, skill libraries, autonomous research loops, paper-writing pipelines |
| [Agents365-ai/awesome-ai-for-science-skills](https://github.com/Agents365-ai/awesome-ai-for-science-skills) | Directory | 1 | 2026-05-11 | AI for Science skills, MCP, and Agent SDK directory |

## Inclusion / Exclusion Rules

- Include repositories that clearly target research, paper writing, literature, Zotero/PubMed/arXiv/Semantic Scholar, medicine, bioinformatics, or life sciences, and expose that capability as a skill, plugin, MCP server, agent workflow, or agent-ready tool.
- Keep low-star repositories when they are direct, domain-specific, and interface-ready.
- Exclude ordinary tutorials, book inventory apps, generic agent infrastructure without a research angle, mirror-only forks without meaningful additions, and empty shells with no useful description.

## Stopping Criteria

Expansion stopped after the last passes produced mostly duplicate PubMed/arXiv/Zotero implementations, same-name forks, mirrors, and broad AI skill directories rather than new high-confidence core repositories.
