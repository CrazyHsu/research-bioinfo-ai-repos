# Research Bioinfo AI Repos 中文版

这是一个面向 AI agent 的科研、论文写作、文献检索、生物信息、生物医学和生命科学 skill/plugin/MCP GitHub 仓库目录。英文主页见 [README.md](README.md)，独立英文目录见 [catalog.md](catalog.md)。

## 内容

- `README.md` - 英文主页目录。
- `README-zh.md` - 中文主页目录，由同一份数据生成。
- `catalog.md` - 独立英文分类目录，每个分类内按 stars 降序排序。
- `data/repos.seed.tsv` - 人工维护的 repo 范围、分类、类型、英文备注和中文备注。
- `data/repos.curated.tsv` - 生成的 metadata 表，包含 GitHub URL、stars、last update、language、description 和备注。
- `scripts/update_catalog.py` - 刷新、重生成和校验 README/catalog 输出。
- `.github/workflows/update-catalog.yml` - 每周自动刷新目录的 GitHub Actions workflow。
- `plans/update-catalog-plan.md` - 可重复执行的更新流程。
- `skills/research-repo-catalog/` - 维护这个目录的 Codex skill。

## 快速开始

不联网校验当前目录：

```bash
python3 scripts/update_catalog.py --check
```

从已有 metadata 重生成 README、`README-zh.md` 和 `catalog.md`：

```bash
python3 scripts/update_catalog.py --from-curated
```

刷新 GitHub metadata 并重生成目录输出：

```bash
python3 scripts/update_catalog.py --refresh
```

如果需要更高 GitHub API 限额，运行 `--refresh` 前设置 `GITHUB_TOKEN` 或 `GH_TOKEN`。

## 更新策略

新增或修改 repo 时编辑 `data/repos.seed.tsv`，不要直接编辑生成表格。英文备注维护在 `notes`，中文备注维护在 `notes_zh`。每个分类在重生成时按 stars 降序排序。

GitHub Actions 每周自动刷新 metadata；只有生成内容发生变化时才会提交。

## 目录

生成日期：2026-07-10

## 更新方式

- 本地校验：`python3 scripts/update_catalog.py --check`
- 从已有 metadata 重生成：`python3 scripts/update_catalog.py --from-curated`
- 刷新 GitHub metadata：`python3 scripts/update_catalog.py --refresh`
- GitHub Actions 会在每周一 03:17 UTC 定时更新，也支持手动触发。
- 扩展清单时先编辑 `data/repos.seed.tsv`，同时维护 `notes` 和 `notes_zh`。

## 综合科研 / AI4S Skill Suites

| repo | 类型 | stars | last update | 方向 / 备注 |
|---|---:|---:|---|---|
| [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | Skill suite | 37088 | 2026-07-09 | Academic research skills：research -> write -> review -> revise -> finalize |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | Skill suite | 30568 | 2026-07-09 | 科学研究、生物/化学/医学/药物发现，Agent Skills 标准 |
| [wanshuiyin/Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | Skill suite | 13192 | 2026-07-09 | ARIS 自动科研循环、idea discovery、实验自动化 |
| [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) | Skill suite | 10549 | 2026-07-09 | AI research and engineering skills，Claude/Codex/Gemini 可用 |
| [Imbad0202/academic-research-skills-codex](https://github.com/Imbad0202/academic-research-skills-codex) | Skill suite | 5864 | 2026-07-09 | Codex-native academic research workflow |
| [openai/plugins](https://github.com/openai/plugins) | Plugin/skills | 4166 | 2026-07-09 | OpenAI Codex plugins，含 life-science-research |
| [brycewang-stanford/Auto-Empirical-Research-Skills](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills) | Skill library | 2757 | 2026-07-09 | 实证社会科学研究，23,000+ agent skills |
| [google-deepmind/science-skills](https://github.com/google-deepmind/science-skills) | Skill suite | 2303 | 2026-07-09 | DeepMind science agent skills |
| [zLanqing/codex-claude-academic-skills](https://github.com/zLanqing/codex-claude-academic-skills) | Skills | 1680 | 2026-07-09 | 中文科研阅读、写作、科学计算 |
| [Weizhena/Deep-Research-skills](https://github.com/Weizhena/Deep-Research-skills) | Skill | 1576 | 2026-07-09 | Structured deep research skill，Claude/OpenCode/Codex |
| [luwill/research-skills](https://github.com/luwill/research-skills) | Skills | 714 | 2026-07-09 | 常用科研经验和流程封装为 Agent skills |
| [chrisblattman/claudeblattman](https://github.com/chrisblattman/claudeblattman) | Academic setup | 421 | 2026-07-07 | Claude Code for academics：skills、agents、setup guides |
| [fcakyon/phd-skills](https://github.com/fcakyon/phd-skills) | Skills | 316 | 2026-07-09 | PhD research：复现、实验设计、paper review、结果比较 |
| [chtc66/academic-skills](https://github.com/chtc66/academic-skills) | Skills | 307 | 2026-07-08 | 论文阅读、survey、实验总结、rebuttal、lab update |
| [ai4s-research/ai4s-skills](https://github.com/ai4s-research/ai4s-skills) | Skill suite | 124 | 2026-07-09 | AI for Science：topic exploration、literature survey、实验、写作、integrity audit |
| [AlterLab-IEU/AlterLab-Academic-Skills](https://github.com/AlterLab-IEU/AlterLab-Academic-Skills) | Skill library | 38 | 2026-07-07 | 239 evaluated academic skills，含 bioinformatics/clinical |
| [s-choung/Research-Skills](https://github.com/s-choung/Research-Skills) | Skills/agents | 28 | 2026-07-06 | 科研写作、图表、文档自动化、韩文学术材料 |
| [JhonHander/academic-agent-toolkit](https://github.com/JhonHander/academic-agent-toolkit) | Toolkit | 7 | 2026-06-28 | MCP tools + AI research skills 安装工具 |

## 论文写作 / 审稿 / 投稿 Skills

| repo | 类型 | stars | last update | 方向 / 备注 |
|---|---:|---:|---|---|
| [Master-cai/Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills) | Skills | 4926 | 2026-07-09 | ML/CV/NLP 论文写作，Codex/Claude/Gemini |
| [WUBING2023/PaperSpine](https://github.com/WUBING2023/PaperSpine) | Skill | 3896 | 2026-07-09 | 论文中心论证、强论文学习、manuscript rewrite、LaTeX-safe audit |
| [PaperDebugger/paperdebugger](https://github.com/PaperDebugger/paperdebugger) | Plugin/agent | 1508 | 2026-07-09 | 学术写作、审稿、编辑 |
| [fakerqwq/social-science-paper-writing-skill](https://github.com/fakerqwq/social-science-paper-writing-skill) | Skill | 151 | 2026-07-09 | 社会科学论文写作、选题、文献综述、引用风险检查 |
| [SNL-UCSB/paper-writing-skill](https://github.com/SNL-UCSB/paper-writing-skill) | Skill | 99 | 2026-07-09 | Brainstorm -> Draft -> Evaluate -> Write -> Compress 论文写作 |
| [SyntaxSmith/nature-writing-skill](https://github.com/SyntaxSmith/nature-writing-skill) | Skill | 60 | 2026-07-09 | Nature-family paper writing |
| [cLin-c/paper-skill](https://github.com/cLin-c/paper-skill) | Skill | 44 | 2026-07-09 | 论文写作、润色、审稿、翻译、投稿 |
| [fuhaoda/stats-paper-writing-agent-skills](https://github.com/fuhaoda/stats-paper-writing-agent-skills) | Skill | 28 | 2026-07-03 | 统计论文写作 agent skills |
| [MetaQiu/Trivium](https://github.com/MetaQiu/Trivium) | Skill/workflow | 24 | 2026-06-08 | Claude/Codex/Gemini 多 agent 论文协作写作 |
| [Zhangyanbo/vibe-paper-writing](https://github.com/Zhangyanbo/vibe-paper-writing) | Skill | 22 | 2026-07-07 | 将 notes/chat/emails 整合为 LaTeX 学术论文 |
| [AGISAFETYLAB/Paper-Writing-skill](https://github.com/AGISAFETYLAB/Paper-Writing-skill) | Skill | 13 | 2026-07-09 | CS、医学、金融论文规划/写作/润色/图表/引用核查 |
| [dailycafi/biomed-paper-writing-skill](https://github.com/dailycafi/biomed-paper-writing-skill) | Skill | 2 | 2026-04-02 | 生物医学/药学论文写作，CONSORT/STROBE/PRISMA/ARRIVE |
| [Jason-0409-G/scriptorium](https://github.com/Jason-0409-G/scriptorium) | Skill | 1 | 2026-06-25 | DOI-verified literature library、NCBI/UniProt/PDB/AlphaFold、写作与审稿 |

## 文献检索 / 学术搜索 MCP

| repo | 类型 | stars | last update | 方向 / 备注 |
|---|---:|---:|---|---|
| [blazickjp/arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server) | MCP | 2944 | 2026-07-09 | arXiv 搜索和论文分析 MCP |
| [openags/paper-search-mcp](https://github.com/openags/paper-search-mcp) | MCP/CLI/skills | 2093 | 2026-07-09 | arXiv/PubMed/bioRxiv 等论文检索下载 |
| [Dianel555/paper-search-mcp-nodejs](https://github.com/Dianel555/paper-search-mcp-nodejs) | MCP | 173 | 2026-07-09 | Web of Science/arXiv 等论文检索下载 |
| [andybrandt/mcp-simple-pubmed](https://github.com/andybrandt/mcp-simple-pubmed) | MCP | 169 | 2026-07-08 | PubMed 医学文献搜索 MCP |
| [Agents365-ai/asta-skill](https://github.com/Agents365-ai/asta-skill) | Skill | 161 | 2026-07-09 | Asta/Semantic Scholar MCP routing |
| [ShZhao27208/Aut_Sci_Write](https://github.com/ShZhao27208/Aut_Sci_Write) | Skill suite | 160 | 2026-07-09 | WoS/Elsevier/Springer 检索下载、综述、Zotero、PPT/HTML |
| [zongmin-yu/semantic-scholar-fastmcp-mcp-server](https://github.com/zongmin-yu/semantic-scholar-fastmcp-mcp-server) | MCP | 160 | 2026-07-08 | Semantic Scholar API FastMCP server |
| [Darkroaster/pubmearch](https://github.com/Darkroaster/pubmearch) | MCP | 150 | 2026-06-04 | PubMed MCP server |
| [takashiishida/arxiv-latex-mcp](https://github.com/takashiishida/arxiv-latex-mcp) | MCP | 140 | 2026-07-05 | arXiv LaTeX source 解析 |
| [cyanheads/pubmed-mcp-server](https://github.com/cyanheads/pubmed-mcp-server) | MCP | 121 | 2026-07-05 | PubMed/Europe PMC/Unpaywall、MeSH、full text |
| [JackKuo666/PubMed-MCP-Server](https://github.com/JackKuo666/PubMed-MCP-Server) | MCP | 121 | 2026-07-09 | PubMed 文章搜索、访问、分析 |
| [grll/pubmedmcp](https://github.com/grll/pubmedmcp) | MCP | 118 | 2026-06-27 | PubMed data MCP |
| [afrise/academic-search-mcp-server](https://github.com/afrise/academic-search-mcp-server) | MCP | 117 | 2026-06-16 | Semantic Scholar + Crossref |
| [JackKuo666/semanticscholar-MCP-Server](https://github.com/JackKuo666/semanticscholar-MCP-Server) | MCP | 75 | 2026-07-07 | Semantic Scholar paper/author/citation/reference |
| [benedict2310/Scientific-Papers-MCP](https://github.com/benedict2310/Scientific-Papers-MCP) | MCP | 54 | 2026-06-25 | arXiv + OpenAlex scientific papers |
| [connerlambden/bgpt-mcp](https://github.com/connerlambden/bgpt-mcp) | MCP/REST | 36 | 2026-07-06 | Scientific paper evidence search |
| [akapet00/semantic-scholar-mcp](https://github.com/akapet00/semantic-scholar-mcp) | MCP | 27 | 2026-07-05 | Semantic Scholar paper search and analysis |
| [masa-med-ai/pubmed-systematic-review](https://github.com/masa-med-ai/pubmed-systematic-review) | Skill | 25 | 2026-06-26 | 与 PubMed MCP 联动做简易 systematic review |
| [lstudlo/ScholarMCP](https://github.com/lstudlo/ScholarMCP) | MCP | 22 | 2026-07-08 | 文献搜索、PDF ingestion、引用管理 |
| [u9401066/pubmed-search-mcp](https://github.com/u9401066/pubmed-search-mcp) | MCP | 20 | 2026-06-24 | PubMed/Europe PMC/CORE/OpenAlex、citation networks、PICO |
| [TaewoooPark/scholar-megasearch](https://github.com/TaewoooPark/scholar-megasearch) | Skill | 19 | 2026-07-08 | 20+ scholarly databases 多源检索与 PDF 获取 |
| [zongmin-yu/semantic-scholar-skills](https://github.com/zongmin-yu/semantic-scholar-skills) | Skill/MCP | 18 | 2026-06-30 | S2-first discovery engine |
| [aringadre76/mcp-for-research](https://github.com/aringadre76/mcp-for-research) | MCP | 13 | 2026-05-12 | PubMed、Google Scholar、arXiv、JSTOR |

## Zotero / CNKI / Google Scholar / 文献管理

| repo | 类型 | stars | last update | 方向 / 备注 |
|---|---:|---:|---|---|
| [54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp) | MCP | 4195 | 2026-07-09 | Zotero library 接入 Claude/AI assistant |
| [papersgpt/papersgpt-for-zotero](https://github.com/papersgpt/papersgpt-for-zotero) | Zotero plugin/MCP | 2503 | 2026-07-09 | Zotero AI/MCP 插件，多模型论文问答 |
| [yilewang/llm-for-zotero](https://github.com/yilewang/llm-for-zotero) | Zotero agent | 2212 | 2026-07-09 | 基于 Zotero library 的 research agent system |
| [cookjohn/zotero-mcp](https://github.com/cookjohn/zotero-mcp) | Zotero plugin/MCP | 988 | 2026-07-09 | Zotero 与 AI assistant 深度集成 |
| [cookjohn/cnki-skills](https://github.com/cookjohn/cnki-skills) | Skills | 740 | 2026-07-09 | CNKI 检索、PDF、Zotero 导出 |
| [cookjohn/gs-skills](https://github.com/cookjohn/gs-skills) | Skills | 447 | 2026-07-09 | Google Scholar 检索、引用追踪、Zotero 导出 |
| [kaliaboi/mcp-zotero](https://github.com/kaliaboi/mcp-zotero) | MCP | 163 | 2026-07-05 | Claude Desktop 连接 Zotero Cloud |
| [kujenga/zotero-mcp](https://github.com/kujenga/zotero-mcp) | MCP | 158 | 2026-07-09 | Zotero API MCP server |
| [introfini/ZotSeek](https://github.com/introfini/ZotSeek) | Zotero plugin/MCP | 146 | 2026-07-08 | Zotero 语义搜索，本地隐私，内置 MCP |
| [TonybotNi/ZotLink](https://github.com/TonybotNi/ZotLink) | MCP | 138 | 2026-06-05 | 保存 arXiv/CVF/bioRxiv/medRxiv 到 Zotero |
| [dralkh/seerai](https://github.com/dralkh/seerai) | Zotero plugin/MCP | 64 | 2026-07-09 | Zotero AI plugin，RAG、OCR、systematic reviews、MCP、skills |
| [gyger/mcp-pyzotero](https://github.com/gyger/mcp-pyzotero) | MCP | 55 | 2026-03-29 | 本地 Zotero MCP connector |
| [Xevos117/mcp-zotero](https://github.com/Xevos117/mcp-zotero) | MCP | 29 | 2026-06-21 | Zotero library operations、DOI、PDF、Unpaywall、docx citation fields |
| [cookjohn/pm-skills](https://github.com/cookjohn/pm-skills) | Skills | 17 | 2026-06-14 | PubMed literature search、citation export、Zotero |

## 生信 / 组学 / 单细胞 Skills

| repo | 类型 | stars | last update | 方向 / 备注 |
|---|---:|---:|---|---|
| [GPTomics/bioSkills](https://github.com/GPTomics/bioSkills) | Skill suite | 1001 | 2026-07-09 | RNA-seq、scRNA、variant、multi-omics |
| [jaechang-hits/SciAgent-Skills](https://github.com/jaechang-hits/SciAgent-Skills) | Skill library | 228 | 2026-07-09 | 197 个生命科学/生信 skills |
| [adaptyvbio/protein-design-skills](https://github.com/adaptyvbio/protein-design-skills) | Skill suite | 147 | 2026-07-09 | 蛋白设计 |
| [TianGzlab/OmicsClaw](https://github.com/TianGzlab/OmicsClaw) | Agent app | 147 | 2026-07-09 | 多组学分析到论文生成 |
| [swaruplab/operon](https://github.com/swaruplab/operon) | Bioinformatics IDE | 90 | 2026-07-09 | Claude Code 生信 IDE/protocols |
| [variomeanalytics/bioinformatics-agent-skills](https://github.com/variomeanalytics/bioinformatics-agent-skills) | MCP/skills | 58 | 2026-06-30 | 查询 78 个 bioinformatics workflows 的知识图谱 |
| [cafferychen777/ChatSpatial](https://github.com/cafferychen777/ChatSpatial) | MCP | 40 | 2026-07-05 | 空间转录组自然语言分析 |
| [ma-compbio-lab/SkillFoundry](https://github.com/ma-compbio-lab/SkillFoundry) | Skill framework | 36 | 2026-07-09 | 计算生物学 skills 发现/验证 |
| [Agents365-ai/seurat-skill](https://github.com/Agents365-ai/seurat-skill) | Skill | 3 | 2026-05-14 | Seurat v5 single-cell analysis |
| [igvteam/igv-mcp](https://github.com/igvteam/igv-mcp) | MCP | 2 | 2026-07-09 | IGV genome viewer 控制 |
| [Bioconductor/ai-agent-skills](https://github.com/Bioconductor/ai-agent-skills) | Skill suite | 0 | 2026-07-09 | R/Bioconductor 与统计生信 |

## 生物医学 / 临床 / 医学研究

| repo | 类型 | stars | last update | 方向 / 备注 |
|---|---:|---:|---|---|
| [FreedomIntelligence/OpenClaw-Medical-Skills](https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills) | Skill library | 2821 | 2026-07-09 | OpenClaw 医学 AI skills 大型集合 |
| [mims-harvard/ToolUniverse](https://github.com/mims-harvard/ToolUniverse) | Tool/skills | 1551 | 2026-07-09 | 生物医学 AI scientist 工具宇宙 |
| [aipoch/medical-research-skills](https://github.com/aipoch/medical-research-skills) | Skill suite | 1333 | 2026-07-09 | 医学研究、protocol、数据分析、学术写作 |
| [genomoncology/biomcp](https://github.com/genomoncology/biomcp) | MCP | 547 | 2026-07-09 | BioMCP：临床试验、基因数据、医学文献 |
| [LeonChaoX/qinyan-academic-skills](https://github.com/LeonChaoX/qinyan-academic-skills) | Skill library | 539 | 2026-07-09 | 177 个学术研究 skills，含生信、药物发现、临床医学 |
| [anthropics/life-sciences](https://github.com/anthropics/life-sciences) | Marketplace | 521 | 2026-07-09 | Claude life-sciences MCP/skills 目录 |
| [Cicatriiz/healthcare-mcp-public](https://github.com/Cicatriiz/healthcare-mcp-public) | MCP | 119 | 2026-07-08 | FDA、PubMed、medRxiv、临床试验、ICD-10 等医疗数据 |
| [JamesANZ/medical-mcp](https://github.com/JamesANZ/medical-mcp) | MCP | 103 | 2026-07-08 | FDA、WHO、PubMed、Google Scholar、RxNorm |
| [cyanheads/clinicaltrialsgov-mcp-server](https://github.com/cyanheads/clinicaltrialsgov-mcp-server) | MCP | 81 | 2026-07-09 | ClinicalTrials.gov 搜索、详情、结果、患者匹配 |
| [pascalwhoop/medical-mcps](https://github.com/pascalwhoop/medical-mcps) | MCP collection | 22 | 2026-07-02 | 主要 biomedical databases MCP 工具集合 |
| [lynnlangit/precision-medicine-mcp](https://github.com/lynnlangit/precision-medicine-mcp) | MCP platform | 21 | 2026-07-08 | Precision medicine，多组学/基因组/空间转录组 |
| [JackKuo666/ClinicalTrials-MCP-Server](https://github.com/JackKuo666/ClinicalTrials-MCP-Server) | MCP | 16 | 2026-04-23 | ClinicalTrials.gov |
| [HolobiomicsLab/asb-skill-collections](https://github.com/HolobiomicsLab/asb-skill-collections) | Skill collection | 12 | 2026-07-06 | Scientific AI agents 的 evidence-grounded skill/tool collections |

## 生物数据库 / 结构生物学 / 化学 / 药物发现 MCP

| repo | 类型 | stars | last update | 方向 / 备注 |
|---|---:|---:|---|---|
| [Augmented-Nature/ChEMBL-MCP-Server](https://github.com/Augmented-Nature/ChEMBL-MCP-Server) | MCP | 88 | 2026-07-09 | ChEMBL |
| [ammawla/encode-toolkit](https://github.com/ammawla/encode-toolkit) | MCP/Claude plugin | 37 | 2026-07-08 | ENCODE genomic data toolkit |
| [PDBeurope/PDBe-MCP-Servers](https://github.com/PDBeurope/PDBe-MCP-Servers) | MCP | 36 | 2026-06-25 | PDBe/蛋白结构 |
| [Augmented-Nature/AlphaFold-MCP-Server](https://github.com/Augmented-Nature/AlphaFold-MCP-Server) | MCP | 35 | 2026-06-12 | AlphaFold Protein Structure Database |
| [longevity-genie/biothings-mcp](https://github.com/longevity-genie/biothings-mcp) | MCP | 33 | 2026-07-05 | BioThings MCP |
| [longevity-genie/gget-mcp](https://github.com/longevity-genie/gget-mcp) | MCP | 30 | 2026-07-05 | gget 生信工具封装 |
| [Augmented-Nature/PDB-MCP-Server](https://github.com/Augmented-Nature/PDB-MCP-Server) | MCP | 25 | 2026-06-12 | Protein Data Bank |
| [Augmented-Nature/Augmented-Nature-UniProt-MCP-Server](https://github.com/Augmented-Nature/Augmented-Nature-UniProt-MCP-Server) | MCP | 19 | 2026-03-29 | UniProt protein database |
| [nickzren/opentargets-mcp](https://github.com/nickzren/opentargets-mcp) | MCP | 19 | 2026-06-27 | Open Targets |
| [tamerh/biobtree](https://github.com/tamerh/biobtree) | MCP/graph DB | 19 | 2026-07-07 | BioBTree v2，70+ biomedical datasets |
| [cyanheads/pubchem-mcp-server](https://github.com/cyanheads/pubchem-mcp-server) | MCP | 9 | 2026-07-03 | PubChem 化合物、性质、安全、生物活性 |
| [effieklimi/ensembl-mcp-server](https://github.com/effieklimi/ensembl-mcp-server) | MCP | 8 | 2026-05-28 | Ensembl REST API |
| [Augmented-Nature/SureChEMBL-MCP-Server](https://github.com/Augmented-Nature/SureChEMBL-MCP-Server) | MCP | 7 | 2026-01-28 | SureChEMBL chemical patent database |
| [donbr/lifesciences-research](https://github.com/donbr/lifesciences-research) | MCP wrappers | 7 | 2026-06-27 | Open Targets、ChEMBL、UniProt |
| [hlydecker/ucsc-genome-mcp](https://github.com/hlydecker/ucsc-genome-mcp) | MCP | 6 | 2026-07-05 | UCSC Genome Browser API |
| [cyanheads/protein-mcp-server](https://github.com/cyanheads/protein-mcp-server) | MCP | 5 | 2026-07-03 | PDB + AlphaFold 蛋白结构/注释 federation |
| [PabloPauling/posebusters-mcp-server](https://github.com/PabloPauling/posebusters-mcp-server) | MCP | 5 | 2026-03-30 | PoseBusters molecular pose validation |
| [EBISPOT/GrEBI](https://github.com/EBISPOT/GrEBI) | API/MCP | 4 | 2026-07-08 | biomedical data integration，API/MCP server |
| [Lucas-Servi/kegg-mcp-server-python](https://github.com/Lucas-Servi/kegg-mcp-server-python) | MCP | 3 | 2026-06-29 | KEGG REST API |
| [smaniches/alphafold-sovereign-mcp](https://github.com/smaniches/alphafold-sovereign-mcp) | MCP | 3 | 2026-07-06 | AlphaFold DB + 8 public sources，本地知识图谱 |
| [smaniches/uniprot-mcp](https://github.com/smaniches/uniprot-mcp) | MCP | 3 | 2026-07-06 | 可审计 UniProt MCP，release pinning/offline replay |

## 科研 Agent Apps / Workspaces

| repo | 类型 | stars | last update | 方向 / 备注 |
|---|---:|---:|---|---|
| [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) | Research assistant | 4558 | 2026-07-09 | 研究、实验、写作、投稿，支持 Claude Code/Codex CLI |
| [yb2460/harness-anything](https://github.com/yb2460/harness-anything) | Agent harness | 917 | 2026-07-09 | WPS/MS Office/Zotero、academic skills、文档自动化 |
| [K-Dense-AI/k-dense-byok](https://github.com/K-Dense-AI/k-dense-byok) | Agent app | 906 | 2026-07-09 | 基于 scientific-agent-skills 的桌面 AI co-scientist |
| [beita6969/ScienceClaw](https://github.com/beita6969/ScienceClaw) | Agent app | 863 | 2026-07-09 | 自进化科研 assistant，skills + persistent memory |
| [AgentTeam-TaichuAI/ScienceClaw](https://github.com/AgentTeam-TaichuAI/ScienceClaw) | Agent app | 551 | 2026-07-07 | LangChain DeepAgents + sandbox 的科研 assistant |
| [ymx10086/ResearchClaw](https://github.com/ymx10086/ResearchClaw) | Research assistant | 308 | 2026-07-08 | 文献综述、笔记、实验跟踪、论文写作 |
| [WenyuChiou/research-hub](https://github.com/WenyuChiou/research-hub) | Research workspace | 34 | 2026-07-09 | Zotero、Obsidian、NotebookLM，CLI/MCP/REST/dashboard |

## 图表 / PDF / LaTeX / 研究产物工具

| repo | 类型 | stars | last update | 方向 / 备注 |
|---|---:|---:|---|---|
| [PDFMathTranslate/PDFMathTranslate](https://github.com/PDFMathTranslate/PDFMathTranslate) | Tool/MCP/Zotero | 35498 | 2026-07-09 | 科学 PDF 翻译，保留排版，支持 MCP、Docker、Zotero |
| [llmsresearch/paperbanana](https://github.com/llmsresearch/paperbanana) | Research visual tool | 2084 | 2026-07-09 | 自动学术图、diagram、research visuals |
| [Dsadd4/AgentFigureGallery](https://github.com/Dsadd4/AgentFigureGallery) | Skill | 132 | 2026-07-08 | 科学绘图 skill，Claude/Codex/Cursor |

## Awesome / Registry / 继续深挖入口

| repo | 类型 | stars | last update | 方向 / 备注 |
|---|---:|---:|---|---|
| [Epsilon617/Codex-Academic-Skills](https://github.com/Epsilon617/Codex-Academic-Skills) | Skills | 143 | 2026-07-08 | Codex research-oriented skills 目录 |
| [WenyuChiou/ai-research-skills](https://github.com/WenyuChiou/ai-research-skills) | Skill catalog | 142 | 2026-07-09 | literature review、research design、manuscript writing |
| [BioTender-max/awesome-bio-agent-skills](https://github.com/BioTender-max/awesome-bio-agent-skills) | Directory | 93 |  | 生物医学 agent skills 目录，覆盖 genomics、proteomics、single-cell、clinical AI、protein design |
| [GoekeLab/awesome-genomic-skills](https://github.com/GoekeLab/awesome-genomic-skills) | Directory | 64 |  | genomics/bioinformatics agent skills、MCP、benchmarks |
| [O0000-code/awesome-academic-skills](https://github.com/O0000-code/awesome-academic-skills) | Directory | 11 |  | academic agent skills，按科研生命周期组织 |
| [Harsh9005/awesome-scientific-ai-tools](https://github.com/Harsh9005/awesome-scientific-ai-tools) | Directory | 7 |  | 科学研究 AI tools、MCP、agent skills |
| [chrisliu298/awesome-research-agents](https://github.com/chrisliu298/awesome-research-agents) | Directory | 3 |  | research agents、skill libraries、autonomous research loops、paper-writing pipelines |
| [Agents365-ai/awesome-ai-for-science-skills](https://github.com/Agents365-ai/awesome-ai-for-science-skills) | Directory | 1 |  | AI for Science skills/MCP/Agent SDK 目录 |
| [InternScience/Awesome-Scientific-Skills](https://github.com/InternScience/Awesome-Scientific-Skills) | Directory | 0 |  | 科学研究 agent skills 目录 |
| [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) | Directory | 0 |  | 通用 MCP 目录，含 Biology/Medicine/Bioinformatics 小节 |

## 纳入 / 排除规则

- 纳入：明确面向科研、论文写作、文献、Zotero/PubMed/arXiv/Semantic Scholar、医学、生物信息、生命科学，并以 skill、plugin、MCP、agent workflow 或 agent-ready tool 形式服务 AI agent 的仓库。
- 保留低 star 项：如果领域直接、接口明确、方向独特，即使 stars 很低也保留。
- 排除：普通教程、书籍/藏书 app、无科研方向的通用 agent 基础设施、无新增价值的镜像或 fork、无描述且无法判断用途的空壳仓库。

## 停止条件

最后几轮新增主要是重复 PubMed/arXiv/Zotero 实现、同名 fork、镜像和泛化 AI skill 目录，没有继续出现新的高可信核心 repo，因此停止扩展。
