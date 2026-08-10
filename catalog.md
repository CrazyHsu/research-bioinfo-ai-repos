# GitHub Research, Paper Writing, Bioinformatics AI Skill/Plugin Repos

Search date: 2026-08-10

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
| [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | Skill suite | 41525 | 2026-08-10 | Academic research skills: research -> write -> review -> revise -> finalize |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | Skill suite | 33078 | 2026-08-10 | Agent Skills standard for scientific research, biology, chemistry, medicine, and drug discovery |
| [wanshuiyin/Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | Skill suite | 14448 | 2026-08-10 | ARIS automated research loop, idea discovery, and experiment automation |
| [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) | Skill suite | 11557 | 2026-08-10 | AI research and engineering skills for Claude, Codex, and Gemini |
| [Imbad0202/academic-research-skills-codex](https://github.com/Imbad0202/academic-research-skills-codex) | Skill suite | 8177 | 2026-08-10 | Codex-native academic research workflow |
| [openai/plugins](https://github.com/openai/plugins) | Plugin/skills | 5015 | 2026-08-10 | OpenAI Codex plugins, including life-science-research |
| [brycewang-stanford/Auto-Empirical-Research-Skills](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills) | Skill library | 3342 | 2026-08-10 | Empirical social science research with 23,000+ agent skills |
| [zLanqing/codex-claude-academic-skills](https://github.com/zLanqing/codex-claude-academic-skills) | Skills | 2721 | 2026-08-10 | Chinese-language research reading, writing, and scientific computing |
| [google-deepmind/science-skills](https://github.com/google-deepmind/science-skills) | Skill suite | 2664 | 2026-08-10 | DeepMind science agent skills |
| [Weizhena/Deep-Research-skills](https://github.com/Weizhena/Deep-Research-skills) | Skill | 1916 | 2026-08-10 | Structured deep research skill, Claude/OpenCode/Codex |
| [luwill/research-skills](https://github.com/luwill/research-skills) | Skills | 800 | 2026-08-10 | Common research practices and workflows packaged as agent skills |
| [chrisblattman/claudeblattman](https://github.com/chrisblattman/claudeblattman) | Academic setup | 437 | 2026-08-09 | Claude Code for academics: skills, agents, setup guides |
| [fcakyon/phd-skills](https://github.com/fcakyon/phd-skills) | Skills | 361 | 2026-08-08 | PhD research: reproduction, experimental design, paper review, and result comparison |
| [chtc66/academic-skills](https://github.com/chtc66/academic-skills) | Skills | 331 | 2026-08-10 | Paper reading, surveys, experiment summaries, rebuttals, and lab updates |
| [ai4s-research/ai4s-skills](https://github.com/ai4s-research/ai4s-skills) | Skill suite | 165 | 2026-08-09 | AI for Science: topic exploration, literature survey, experiments, writing, and integrity audit |
| [AlterLab-IEU/AlterLab-Academic-Skills](https://github.com/AlterLab-IEU/AlterLab-Academic-Skills) | Skill library | 58 | 2026-08-06 | 239 evaluated academic skills, including bioinformatics and clinical research |
| [s-choung/Research-Skills](https://github.com/s-choung/Research-Skills) | Skills/agents | 30 | 2026-07-23 | Research writing, figures, document automation, and Korean academic materials |
| [JhonHander/academic-agent-toolkit](https://github.com/JhonHander/academic-agent-toolkit) | Toolkit | 7 | 2026-06-28 | Installer for MCP tools and AI research skills |

## Paper Writing / Peer Review / Submission Skills

| repo | type | stars | last update | focus / notes |
|---|---:|---:|---|---|
| [Master-cai/Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills) | Skills | 5915 | 2026-08-10 | ML/CV/NLP paper writing for Codex, Claude, and Gemini |
| [WUBING2023/PaperSpine](https://github.com/WUBING2023/PaperSpine) | Skill | 4722 | 2026-08-10 | Central paper argumentation, strong-paper learning, manuscript rewriting, and LaTeX-safe audits |
| [PaperDebugger/paperdebugger](https://github.com/PaperDebugger/paperdebugger) | Plugin/agent | 1522 | 2026-08-04 | Academic writing, peer review, and editing |
| [fakerqwq/social-science-paper-writing-skill](https://github.com/fakerqwq/social-science-paper-writing-skill) | Skill | 204 | 2026-08-09 | Social science paper writing, topic selection, literature reviews, and citation risk checks |
| [SNL-UCSB/paper-writing-skill](https://github.com/SNL-UCSB/paper-writing-skill) | Skill | 160 | 2026-08-08 | Brainstorm -> Draft -> Evaluate -> Write -> Compress paper writing |
| [SyntaxSmith/nature-writing-skill](https://github.com/SyntaxSmith/nature-writing-skill) | Skill | 88 | 2026-08-10 | Nature-family paper writing |
| [cLin-c/paper-skill](https://github.com/cLin-c/paper-skill) | Skill | 77 | 2026-08-09 | Paper writing, polishing, peer review, translation, and submission |
| [fuhaoda/stats-paper-writing-agent-skills](https://github.com/fuhaoda/stats-paper-writing-agent-skills) | Skill | 28 | 2026-07-03 | Agent skills for statistics paper writing |
| [Zhangyanbo/vibe-paper-writing](https://github.com/Zhangyanbo/vibe-paper-writing) | Skill | 25 | 2026-08-09 | Convert notes, chats, and emails into LaTeX academic papers |
| [MetaQiu/Trivium](https://github.com/MetaQiu/Trivium) | Skill/workflow | 24 | 2026-06-08 | Multi-agent collaborative paper writing for Claude, Codex, and Gemini |
| [AGISAFETYLAB/Paper-Writing-skill](https://github.com/AGISAFETYLAB/Paper-Writing-skill) | Skill | 16 | 2026-07-29 | Planning, writing, polishing, figures, and citation checks for CS, medical, and finance papers |
| [dailycafi/biomed-paper-writing-skill](https://github.com/dailycafi/biomed-paper-writing-skill) | Skill | 2 | 2026-04-02 | Biomedical and pharmaceutical paper writing with CONSORT, STROBE, PRISMA, and ARRIVE |
| [Jason-0409-G/scriptorium](https://github.com/Jason-0409-G/scriptorium) | Skill | 1 | 2026-06-25 | DOI-verified literature library, NCBI/UniProt/PDB/AlphaFold integration, writing, and review |

## Literature Search / Scholarly Search MCP

| repo | type | stars | last update | focus / notes |
|---|---:|---:|---|---|
| [blazickjp/arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server) | MCP | 3034 | 2026-08-10 | arXiv search and paper analysis MCP |
| [openags/paper-search-mcp](https://github.com/openags/paper-search-mcp) | MCP/CLI/skills | 2390 | 2026-08-10 | Paper search and download for arXiv, PubMed, bioRxiv, and related sources |
| [Agents365-ai/asta-skill](https://github.com/Agents365-ai/asta-skill) | Skill | 179 | 2026-08-08 | Asta/Semantic Scholar MCP routing |
| [Dianel555/paper-search-mcp-nodejs](https://github.com/Dianel555/paper-search-mcp-nodejs) | MCP | 179 | 2026-08-06 | Paper search and download for Web of Science, arXiv, and related sources |
| [ShZhao27208/Aut_Sci_Write](https://github.com/ShZhao27208/Aut_Sci_Write) | Skill suite | 177 | 2026-08-09 | WoS, Elsevier, and Springer search/download, reviews, Zotero, PPT, and HTML |
| [andybrandt/mcp-simple-pubmed](https://github.com/andybrandt/mcp-simple-pubmed) | MCP | 170 | 2026-07-20 | PubMed medical literature search MCP |
| [zongmin-yu/semantic-scholar-fastmcp-mcp-server](https://github.com/zongmin-yu/semantic-scholar-fastmcp-mcp-server) | MCP | 164 | 2026-08-07 | Semantic Scholar API FastMCP server |
| [Darkroaster/pubmearch](https://github.com/Darkroaster/pubmearch) | MCP | 149 | 2026-08-03 | PubMed MCP server |
| [takashiishida/arxiv-latex-mcp](https://github.com/takashiishida/arxiv-latex-mcp) | MCP | 142 | 2026-07-30 | arXiv LaTeX source parsing |
| [cyanheads/pubmed-mcp-server](https://github.com/cyanheads/pubmed-mcp-server) | MCP | 133 | 2026-08-10 | PubMed/Europe PMC/Unpaywall, MeSH, full text |
| [JackKuo666/PubMed-MCP-Server](https://github.com/JackKuo666/PubMed-MCP-Server) | MCP | 124 | 2026-08-03 | PubMed article search, access, and analysis |
| [grll/pubmedmcp](https://github.com/grll/pubmedmcp) | MCP | 121 | 2026-08-06 | PubMed data MCP |
| [afrise/academic-search-mcp-server](https://github.com/afrise/academic-search-mcp-server) | MCP | 119 | 2026-08-02 | Semantic Scholar + Crossref |
| [JackKuo666/semanticscholar-MCP-Server](https://github.com/JackKuo666/semanticscholar-MCP-Server) | MCP | 78 | 2026-08-09 | Semantic Scholar paper/author/citation/reference |
| [benedict2310/Scientific-Papers-MCP](https://github.com/benedict2310/Scientific-Papers-MCP) | MCP | 55 | 2026-08-07 | arXiv + OpenAlex scientific papers |
| [connerlambden/bgpt-mcp](https://github.com/connerlambden/bgpt-mcp) | MCP/REST | 42 | 2026-07-20 | Scientific paper evidence search |
| [akapet00/semantic-scholar-mcp](https://github.com/akapet00/semantic-scholar-mcp) | MCP | 31 | 2026-08-09 | Semantic Scholar paper search and analysis |
| [masa-med-ai/pubmed-systematic-review](https://github.com/masa-med-ai/pubmed-systematic-review) | Skill | 25 | 2026-06-26 | Lightweight systematic reviews integrated with a PubMed MCP |
| [u9401066/pubmed-search-mcp](https://github.com/u9401066/pubmed-search-mcp) | MCP | 24 | 2026-08-09 | PubMed/Europe PMC/CORE/OpenAlex, citation networks, PICO |
| [lstudlo/ScholarMCP](https://github.com/lstudlo/ScholarMCP) | MCP | 23 | 2026-07-23 | Literature search, PDF ingestion, and reference management |
| [TaewoooPark/scholar-megasearch](https://github.com/TaewoooPark/scholar-megasearch) | Skill | 23 | 2026-08-03 | 20+ scholarly databases with multi-source search and PDF retrieval |
| [zongmin-yu/semantic-scholar-skills](https://github.com/zongmin-yu/semantic-scholar-skills) | Skill/MCP | 20 | 2026-08-07 | S2-first discovery engine |
| [aringadre76/mcp-for-research](https://github.com/aringadre76/mcp-for-research) | MCP | 14 | 2026-07-13 | PubMed, Google Scholar, arXiv, JSTOR |

## Zotero / CNKI / Google Scholar / Reference Management

| repo | type | stars | last update | focus / notes |
|---|---:|---:|---|---|
| [54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp) | MCP | 4593 | 2026-08-10 | Connect Zotero libraries to Claude and AI assistants |
| [yilewang/llm-for-zotero](https://github.com/yilewang/llm-for-zotero) | Zotero agent | 2588 | 2026-08-10 | Research agent system based on a Zotero library |
| [papersgpt/papersgpt-for-zotero](https://github.com/papersgpt/papersgpt-for-zotero) | Zotero plugin/MCP | 2586 | 2026-08-08 | Zotero AI/MCP plugin with multi-model paper Q&A |
| [cookjohn/zotero-mcp](https://github.com/cookjohn/zotero-mcp) | Zotero plugin/MCP | 1066 | 2026-08-09 | Deep integration between Zotero and AI assistants |
| [cookjohn/cnki-skills](https://github.com/cookjohn/cnki-skills) | Skills | 826 | 2026-08-10 | CNKI search, PDFs, and Zotero export |
| [cookjohn/gs-skills](https://github.com/cookjohn/gs-skills) | Skills | 474 | 2026-08-09 | Google Scholar search, citation tracking, and Zotero export |
| [introfini/ZotSeek](https://github.com/introfini/ZotSeek) | Zotero plugin/MCP | 180 | 2026-08-07 | Zotero semantic search with local privacy and built-in MCP |
| [kaliaboi/mcp-zotero](https://github.com/kaliaboi/mcp-zotero) | MCP | 165 | 2026-07-25 | Connect Claude Desktop to Zotero Cloud |
| [kujenga/zotero-mcp](https://github.com/kujenga/zotero-mcp) | MCP | 160 | 2026-08-09 | Zotero API MCP server |
| [TonybotNi/ZotLink](https://github.com/TonybotNi/ZotLink) | MCP | 137 | 2026-08-02 | Save arXiv, CVF, bioRxiv, and medRxiv papers to Zotero |
| [dralkh/seerai](https://github.com/dralkh/seerai) | Zotero plugin/MCP | 74 | 2026-08-03 | Zotero AI plugin, RAG, OCR, systematic reviews, MCP, skills |
| [gyger/mcp-pyzotero](https://github.com/gyger/mcp-pyzotero) | MCP | 56 | 2026-07-18 | Local Zotero MCP connector |
| [Xevos117/mcp-zotero](https://github.com/Xevos117/mcp-zotero) | MCP | 33 | 2026-07-27 | Zotero library operations, DOI, PDF, Unpaywall, docx citation fields |
| [cookjohn/pm-skills](https://github.com/cookjohn/pm-skills) | Skills | 19 | 2026-08-09 | PubMed literature search, citation export, Zotero |

## Bioinformatics / Omics / Single-Cell Skills

| repo | type | stars | last update | focus / notes |
|---|---:|---:|---|---|
| [GPTomics/bioSkills](https://github.com/GPTomics/bioSkills) | Skill suite | 1143 | 2026-08-09 | RNA-seq, scRNA, variant, multi-omics |
| [jaechang-hits/SciAgent-Skills](https://github.com/jaechang-hits/SciAgent-Skills) | Skill library | 298 | 2026-08-08 | 197 life-science and bioinformatics skills |
| [TianGzlab/OmicsClaw](https://github.com/TianGzlab/OmicsClaw) | Agent app | 155 | 2026-08-02 | Multi-omics analysis through manuscript generation |
| [adaptyvbio/protein-design-skills](https://github.com/adaptyvbio/protein-design-skills) | Skill suite | 151 | 2026-08-03 | Protein design |
| [swaruplab/operon](https://github.com/swaruplab/operon) | Bioinformatics IDE | 94 | 2026-08-01 | Claude Code bioinformatics IDE and protocols |
| [charlesxu90/ProteinMCP](https://github.com/charlesxu90/ProteinMCP) | Agentic framework/MCP suite | 64 | 2026-08-06 | Agentic framework for autonomous protein engineering with Claude Code workflow skills and 38 supported MCPs |
| [variomeanalytics/bioinformatics-agent-skills](https://github.com/variomeanalytics/bioinformatics-agent-skills) | MCP/skills | 60 | 2026-08-06 | Knowledge graph over 78 bioinformatics workflows |
| [cafferychen777/ChatSpatial](https://github.com/cafferychen777/ChatSpatial) | MCP | 43 | 2026-08-09 | Natural-language analysis for spatial transcriptomics |
| [ma-compbio-lab/SkillFoundry](https://github.com/ma-compbio-lab/SkillFoundry) | Skill framework | 36 | 2026-06-24 | Computational biology skill discovery and validation |
| [Bioconductor/ai-agent-skills](https://github.com/Bioconductor/ai-agent-skills) | Skill suite | 4 | 2026-08-03 | R/Bioconductor and statistical bioinformatics |
| [Agents365-ai/seurat-skill](https://github.com/Agents365-ai/seurat-skill) | Skill | 3 | 2026-05-14 | Seurat v5 single-cell analysis |
| [igvteam/igv-mcp](https://github.com/igvteam/igv-mcp) | MCP | 3 | 2026-07-23 | IGV genome viewer control |

## Biomedical / Clinical / Medical Research

| repo | type | stars | last update | focus / notes |
|---|---:|---:|---|---|
| [FreedomIntelligence/OpenClaw-Medical-Skills](https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills) | Skill library | 2921 | 2026-08-10 | Large OpenClaw medical AI skills collection |
| [aipoch/medical-research-skills](https://github.com/aipoch/medical-research-skills) | Skill suite | 1670 | 2026-08-09 | Medical research, protocols, data analysis, and academic writing |
| [mims-harvard/ToolUniverse](https://github.com/mims-harvard/ToolUniverse) | Tool/skills | 1619 | 2026-08-09 | Tool universe for biomedical AI scientists |
| [LeonChaoX/qinyan-academic-skills](https://github.com/LeonChaoX/qinyan-academic-skills) | Skill library | 785 | 2026-08-10 | 177 academic research skills, including bioinformatics, drug discovery, and clinical medicine |
| [genomoncology/biomcp](https://github.com/genomoncology/biomcp) | MCP | 584 | 2026-08-10 | BioMCP for clinical trials, genomic data, and medical literature |
| [anthropics/life-sciences](https://github.com/anthropics/life-sciences) | Marketplace | 569 | 2026-08-10 | Claude life-sciences MCP and skills directory |
| [Cicatriiz/healthcare-mcp-public](https://github.com/Cicatriiz/healthcare-mcp-public) | MCP | 125 | 2026-07-27 | Medical data from FDA, PubMed, medRxiv, clinical trials, ICD-10, and related sources |
| [JamesANZ/medical-mcp](https://github.com/JamesANZ/medical-mcp) | MCP | 108 | 2026-08-05 | FDA, WHO, PubMed, Google Scholar, RxNorm |
| [cyanheads/clinicaltrialsgov-mcp-server](https://github.com/cyanheads/clinicaltrialsgov-mcp-server) | MCP | 87 | 2026-08-09 | ClinicalTrials.gov search, details, results, and patient matching |
| [pascalwhoop/medical-mcps](https://github.com/pascalwhoop/medical-mcps) | MCP collection | 23 | 2026-08-05 | MCP tool collection for major biomedical databases |
| [lynnlangit/precision-medicine-mcp](https://github.com/lynnlangit/precision-medicine-mcp) | MCP platform | 22 | 2026-08-09 | Precision medicine across multi-omics, genomics, and spatial transcriptomics |
| [JackKuo666/ClinicalTrials-MCP-Server](https://github.com/JackKuo666/ClinicalTrials-MCP-Server) | MCP | 16 | 2026-04-23 | ClinicalTrials.gov |
| [HolobiomicsLab/asb-skill-collections](https://github.com/HolobiomicsLab/asb-skill-collections) | Skill collection | 15 | 2026-07-31 | Evidence-grounded skill and tool collections for scientific AI agents |

## Biological Databases / Structural Biology / Chemistry / Drug Discovery MCP

| repo | type | stars | last update | focus / notes |
|---|---:|---:|---|---|
| [Augmented-Nature/ChEMBL-MCP-Server](https://github.com/Augmented-Nature/ChEMBL-MCP-Server) | MCP | 89 | 2026-08-04 | ChEMBL |
| [PDBeurope/PDBe-MCP-Servers](https://github.com/PDBeurope/PDBe-MCP-Servers) | MCP | 37 | 2026-08-02 | PDBe and protein structures |
| [Augmented-Nature/AlphaFold-MCP-Server](https://github.com/Augmented-Nature/AlphaFold-MCP-Server) | MCP | 35 | 2026-06-12 | AlphaFold Protein Structure Database |
| [longevity-genie/biothings-mcp](https://github.com/longevity-genie/biothings-mcp) | MCP | 33 | 2026-07-05 | BioThings MCP |
| [longevity-genie/gget-mcp](https://github.com/longevity-genie/gget-mcp) | MCP | 30 | 2026-07-05 | MCP wrapper for gget bioinformatics tools |
| [ammawla/encode-toolkit](https://github.com/ammawla/encode-toolkit) | MCP/Claude plugin | 26 | 2026-08-05 | ENCODE genomic data toolkit |
| [Augmented-Nature/PDB-MCP-Server](https://github.com/Augmented-Nature/PDB-MCP-Server) | MCP | 25 | 2026-06-12 | Protein Data Bank |
| [nickzren/opentargets-mcp](https://github.com/nickzren/opentargets-mcp) | MCP | 20 | 2026-08-04 | Open Targets |
| [Augmented-Nature/Augmented-Nature-UniProt-MCP-Server](https://github.com/Augmented-Nature/Augmented-Nature-UniProt-MCP-Server) | MCP | 19 | 2026-03-29 | UniProt protein database |
| [tamerh/biobtree](https://github.com/tamerh/biobtree) | MCP/graph DB | 19 | 2026-08-03 | BioBTree v2, 70+ biomedical datasets |
| [cyanheads/pubchem-mcp-server](https://github.com/cyanheads/pubchem-mcp-server) | MCP | 9 | 2026-07-30 | PubChem compounds, properties, safety, and bioactivity |
| [effieklimi/ensembl-mcp-server](https://github.com/effieklimi/ensembl-mcp-server) | MCP | 8 | 2026-05-28 | Ensembl REST API |
| [Augmented-Nature/SureChEMBL-MCP-Server](https://github.com/Augmented-Nature/SureChEMBL-MCP-Server) | MCP | 7 | 2026-01-28 | SureChEMBL chemical patent database |
| [donbr/lifesciences-research](https://github.com/donbr/lifesciences-research) | MCP wrappers | 7 | 2026-06-27 | Open Targets, ChEMBL, UniProt |
| [hlydecker/ucsc-genome-mcp](https://github.com/hlydecker/ucsc-genome-mcp) | MCP | 6 | 2026-07-05 | UCSC Genome Browser API |
| [cyanheads/protein-mcp-server](https://github.com/cyanheads/protein-mcp-server) | MCP | 5 | 2026-07-30 | PDB and AlphaFold protein structure and annotation federation |
| [PabloPauling/posebusters-mcp-server](https://github.com/PabloPauling/posebusters-mcp-server) | MCP | 5 | 2026-03-30 | PoseBusters molecular pose validation |
| [EBISPOT/GrEBI](https://github.com/EBISPOT/GrEBI) | API/MCP | 4 | 2026-07-10 | biomedical data integration, API/MCP server |
| [smaniches/alphafold-sovereign-mcp](https://github.com/smaniches/alphafold-sovereign-mcp) | MCP | 4 | 2026-08-09 | AlphaFold DB plus eight public sources with a local knowledge graph |
| [Lucas-Servi/kegg-mcp-server-python](https://github.com/Lucas-Servi/kegg-mcp-server-python) | MCP | 3 | 2026-08-06 | KEGG REST API |
| [smaniches/uniprot-mcp](https://github.com/smaniches/uniprot-mcp) | MCP | 3 | 2026-08-04 | Auditable UniProt MCP with release pinning and offline replay |

## Research Agent Apps / Workspaces

| repo | type | stars | last update | focus / notes |
|---|---:|---:|---|---|
| [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) | Research assistant | 5055 | 2026-08-10 | Research, experiments, writing, and submission support for Claude Code and Codex CLI |
| [yb2460/harness-anything](https://github.com/yb2460/harness-anything) | Agent harness | 1414 | 2026-08-09 | WPS, MS Office, Zotero, academic skills, and document automation |
| [K-Dense-AI/k-dense-byok](https://github.com/K-Dense-AI/k-dense-byok) | Agent app | 984 | 2026-08-09 | Desktop AI co-scientist based on scientific-agent-skills |
| [beita6969/ScienceClaw](https://github.com/beita6969/ScienceClaw) | Agent app | 875 | 2026-08-10 | Self-evolving research assistant with skills and persistent memory |
| [AgentTeam-TaichuAI/ScienceClaw](https://github.com/AgentTeam-TaichuAI/ScienceClaw) | Agent app | 635 | 2026-08-09 | Research assistant built with LangChain DeepAgents and sandboxing |
| [ymx10086/ResearchClaw](https://github.com/ymx10086/ResearchClaw) | Research assistant | 312 | 2026-08-10 | Literature reviews, notes, experiment tracking, and paper writing |
| [WenyuChiou/research-hub](https://github.com/WenyuChiou/research-hub) | Research workspace | 45 | 2026-08-09 | Zotero, Obsidian, NotebookLM, CLI/MCP/REST/dashboard |

## Figures / PDF / LaTeX / Research Artifact Tools

| repo | type | stars | last update | focus / notes |
|---|---:|---:|---|---|
| [PDFMathTranslate/PDFMathTranslate](https://github.com/PDFMathTranslate/PDFMathTranslate) | Tool/MCP/Zotero | 36052 | 2026-08-10 | Scientific PDF translation that preserves layout, with MCP, Docker, and Zotero support |
| [llmsresearch/paperbanana](https://github.com/llmsresearch/paperbanana) | Research visual tool | 2227 | 2026-08-10 | Automated academic figures, diagrams, and research visuals |
| [Dsadd4/AgentFigureGallery](https://github.com/Dsadd4/AgentFigureGallery) | Skill | 133 | 2026-08-08 | Scientific plotting skill for Claude, Codex, and Cursor |

## Awesome Lists / Registries / Further Discovery

| repo | type | stars | last update | focus / notes |
|---|---:|---:|---|---|
| [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) | Directory | 92021 | 2026-08-10 | General MCP directory with Biology, Medicine, and Bioinformatics sections |
| [InternScience/Awesome-Scientific-Skills](https://github.com/InternScience/Awesome-Scientific-Skills) | Directory | 503 | 2026-08-10 | Scientific research agent skills directory |
| [WenyuChiou/ai-research-skills](https://github.com/WenyuChiou/ai-research-skills) | Skill catalog | 201 | 2026-08-10 | literature review, research design, manuscript writing |
| [Epsilon617/Codex-Academic-Skills](https://github.com/Epsilon617/Codex-Academic-Skills) | Skills | 169 | 2026-08-09 | Codex research-oriented skills directory |
| [BioTender-max/awesome-bio-agent-skills](https://github.com/BioTender-max/awesome-bio-agent-skills) | Directory | 140 | 2026-08-07 | Biomedical agent skills directory covering genomics, proteomics, single-cell analysis, clinical AI, and protein design |
| [GoekeLab/awesome-genomic-skills](https://github.com/GoekeLab/awesome-genomic-skills) | Directory | 90 | 2026-08-07 | genomics/bioinformatics agent skills, MCP, benchmarks |
| [O0000-code/awesome-academic-skills](https://github.com/O0000-code/awesome-academic-skills) | Directory | 15 | 2026-08-10 | Academic agent skills organized by the research lifecycle |
| [Harsh9005/awesome-scientific-ai-tools](https://github.com/Harsh9005/awesome-scientific-ai-tools) | Directory | 7 | 2026-07-02 | AI tools, MCP servers, and agent skills for scientific research |
| [chrisliu298/awesome-research-agents](https://github.com/chrisliu298/awesome-research-agents) | Directory | 3 | 2026-06-29 | research agents, skill libraries, autonomous research loops, paper-writing pipelines |
| [Agents365-ai/awesome-ai-for-science-skills](https://github.com/Agents365-ai/awesome-ai-for-science-skills) | Directory | 1 | 2026-05-11 | AI for Science skills, MCP, and Agent SDK directory |

## Inclusion / Exclusion Rules

- Include repositories that clearly target research, paper writing, literature, Zotero/PubMed/arXiv/Semantic Scholar, medicine, bioinformatics, or life sciences, and expose that capability as a skill, plugin, MCP server, agent workflow, or agent-ready tool.
- Keep low-star repositories when they are direct, domain-specific, and interface-ready.
- Exclude ordinary tutorials, book inventory apps, generic agent infrastructure without a research angle, mirror-only forks without meaningful additions, and empty shells with no useful description.

## Stopping Criteria

Expansion stopped after the last passes produced mostly duplicate PubMed/arXiv/Zotero implementations, same-name forks, mirrors, and broad AI skill directories rather than new high-confidence core repositories.
