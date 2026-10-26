# Research Bioinfo AI Repos 中文版

面向 AI agent 的科研扩展目录：文献检索、论文写作、文献管理、生物信息、生物医学与生物数据库方向的 skill、plugin 和 MCP server。

目录正文见下方；英文版见 [README.md](README.md)，独立英文页面见 [catalog.md](catalog.md)，机器可读数据见 [`catalog.json`](catalog.json)，逐周变化见 [CHANGELOG.md](CHANGELOG.md)。

## 维护方式

- `data/repos.seed.tsv` 是唯一手工维护的清单：范围、分类、受控 `type`、接口形态、宿主、领域和中英文备注。分类、类型词表和政策文本集中在 `data/catalog_config.json`。
- `scripts/update_catalog.py --refresh` 抓取 GitHub 元数据写入 `data/repos.curated.tsv`，向 `data/star_history.tsv` 追加快照，并重新生成本文件、`README.md`、`catalog.md` 中标记之间的内容以及 `catalog.json` 和 `CHANGELOG.md`。
- `scripts/discover_candidates.py` 执行 `data/discovery_queries.tsv` 中的查询，并反查目录中已收录的 awesome 列表。命中项写入 `discovery/candidates.md`，跨周跟踪记录在 `data/candidates_seen.tsv`，人工决定记录在 `data/triage.tsv`。
- `.github/workflows/update-catalog.yml` 每周一自动执行上述两个脚本，输出有变化时才提交；失败会自动开 issue。`.github/workflows/validate.yml` 校验 pull request。
- `skills/research-repo-catalog/` 和 `CLAUDE.md` 说明 coding agent（Claude Code、Codex 等）如何维护本目录。`archive/` 保存最初的草稿。

## 快速开始

```bash
python3 scripts/update_catalog.py --check          # 不联网校验数据与生成结果
python3 scripts/update_catalog.py --from-curated   # 从已缓存的元数据重新生成输出
python3 scripts/update_catalog.py --refresh        # 刷新 GitHub 元数据（需设置 GITHUB_TOKEN 或 GH_TOKEN）
python3 scripts/discover_candidates.py             # 执行候选发现；--offline 不联网重新渲染
python3 -m unittest discover -s tests              # 运行测试（仅依赖标准库）
```

## 新增仓库

1. 先查看 `discovery/candidates.md` 与 `data/triage.tsv`。
2. 在 `data/repos.seed.tsv` 增加一行：一个分类标签、一个 `type` 键、接口形态、宿主、领域，以及说明"做什么、与同类有何差异"的中英文备注。
3. 运行 `python3 scripts/update_catalog.py --from-curated`（新行在下一次刷新前显示为 `待抓取`），再运行 `--check`。
4. 如果仓库来自候选报告，在 `data/triage.tsv` 记录 `accept`。细节见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 目录

<!-- CATALOG:START -->
元数据刷新于 2026-10-26（UTC）：155 个仓库，12 个分类。stars 与最近 push 日期来自 GitHub REST API；`(已归档)` 表示仓库已归档。license、语言、topics、接口形态、宿主等完整字段见 `data/repos.curated.tsv` 与 `catalog.json`。

### 最近变化

2026-10-26 的刷新与 2026-10-19 对比。完整历史见 [CHANGELOG.md](CHANGELOG.md)。

- 新增: 无
- 移除: 无
- 已归档: `GPTomics/bioSkills`, `gyger/mcp-pyzotero`
- 已改名: 无
- GitHub 上已不存在: 无
- 本期 star 增长 Top: `K-Dense-AI/scientific-agent-skills` +1913 (52753 -> 54666), `Imbad0202/academic-research-skills` +1059 (52884 -> 53943), `wanshuiyin/Auto-claude-code-research-in-sleep` +393 (17698 -> 18091), `Imbad0202/academic-research-skills-codex` +375 (13144 -> 13519), `punkpeye/awesome-mcp-servers` +288 (96592 -> 96880)

## 综合科研 / AI4S Skill Suites

| repo | 类型 | stars | 最近 push | 方向 / 备注 |
|---|---|---:|---|---|
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | skill-suite | 54666 | 2026-10-19 | 科学研究、生物/化学/医学/药物发现，Agent Skills 标准 |
| [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | skill-suite | 53943 | 2026-10-26 | Academic research skills：research -> write -> review -> revise -> finalize |
| [wanshuiyin/Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | skill-suite | 18091 | 2026-10-24 | ARIS 自动科研循环、idea discovery、实验自动化 |
| [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) | skill-suite | 13960 | 2026-10-11 | AI research and engineering skills，Claude/Codex/Gemini 可用 |
| [Imbad0202/academic-research-skills-codex](https://github.com/Imbad0202/academic-research-skills-codex) | skill-suite | 13519 | 2026-10-26 | 面向 Codex 的学术研究工作流 skill 套件 |
| [openai/plugins](https://github.com/openai/plugins) | plugin | 7598 | 2026-10-08 | OpenAI Codex plugins，含 life-science-research |
| [zLanqing/codex-claude-academic-skills](https://github.com/zLanqing/codex-claude-academic-skills) | skill-suite | 5328 | 2026-05-14 | 中文科研阅读、写作、科学计算 |
| [brycewang-stanford/Auto-Empirical-Research-Skills](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills) | skill-suite | 4783 | 2026-10-20 | 实证社会科学研究，23,000+ agent skills |
| [google-deepmind/science-skills](https://github.com/google-deepmind/science-skills) | skill-suite | 3334 | 2026-10-23 | DeepMind 官方科学研究 agent skills |
| [Weizhena/Deep-Research-skills](https://github.com/Weizhena/Deep-Research-skills) | skill | 2422 | 2026-08-23 | Structured deep research skill，Claude/OpenCode/Codex |
| [luwill/research-skills](https://github.com/luwill/research-skills) | skill-suite | 876 | 2026-10-25 | 常用科研经验和流程封装为 Agent skills |
| [chrisblattman/claudeblattman](https://github.com/chrisblattman/claudeblattman) | skill-suite | 470 | 2026-10-24 | Claude Code for academics：skills、agents、setup guides |
| [fcakyon/phd-skills](https://github.com/fcakyon/phd-skills) | skill-suite | 434 | 2026-10-11 | PhD research：复现、实验设计、paper review、结果比较 |
| [chtc66/academic-skills](https://github.com/chtc66/academic-skills) | skill-suite | 367 | 2026-04-05 | 论文阅读、survey、实验总结、rebuttal、lab update |
| [ai4s-research/ai4s-skills](https://github.com/ai4s-research/ai4s-skills) | skill-suite | 252 | 2026-07-28 | AI for Science：topic exploration、literature survey、实验、写作、integrity audit |
| [AlterLab-IEU/AlterLab-Academic-Skills](https://github.com/AlterLab-IEU/AlterLab-Academic-Skills) | skill-suite | 78 | 2026-10-23 | 239 evaluated academic skills，含 bioinformatics/clinical |
| [s-choung/Research-Skills](https://github.com/s-choung/Research-Skills) | skill-suite | 36 | 2026-10-21 | 科研写作、图表、文档自动化、韩文学术材料 |
| [JhonHander/academic-agent-toolkit](https://github.com/JhonHander/academic-agent-toolkit) | tool | 8 | 2026-06-09 | MCP tools + AI research skills 安装工具 |

## 论文写作 / 审稿 / 投稿 Skills

| repo | 类型 | stars | 最近 push | 方向 / 备注 |
|---|---|---:|---|---|
| [Master-cai/Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills) | skill-suite | 7801 | 2026-06-23 | ML/CV/NLP 论文写作，Codex/Claude/Gemini |
| [WUBING2023/PaperSpine](https://github.com/WUBING2023/PaperSpine) | skill | 6078 | 2026-10-14 | 论文中心论证、强论文学习、manuscript rewrite、LaTeX-safe audit |
| [PaperDebugger/paperdebugger](https://github.com/PaperDebugger/paperdebugger) | plugin | 1549 | 2026-07-03 | 学术写作、审稿、编辑 |
| [fakerqwq/social-science-paper-writing-skill](https://github.com/fakerqwq/social-science-paper-writing-skill) | skill | 435 | 2026-06-02 | 社会科学论文写作、选题、文献综述、引用风险检查 |
| [SNL-UCSB/paper-writing-skill](https://github.com/SNL-UCSB/paper-writing-skill) | skill | 244 | 2026-07-31 | Brainstorm -> Draft -> Evaluate -> Write -> Compress 论文写作 |
| [SyntaxSmith/nature-writing-skill](https://github.com/SyntaxSmith/nature-writing-skill) | skill | 180 | 2026-04-27 | 面向 Nature 系列期刊的论文写作 skill |
| [cLin-c/paper-skill](https://github.com/cLin-c/paper-skill) | skill | 132 | 2026-09-26 | 论文写作、润色、审稿、翻译、投稿 |
| [fuhaoda/stats-paper-writing-agent-skills](https://github.com/fuhaoda/stats-paper-writing-agent-skills) | skill | 31 | 2026-02-13 | 统计论文写作 agent skills |
| [Zhangyanbo/vibe-paper-writing](https://github.com/Zhangyanbo/vibe-paper-writing) | skill | 25 | 2026-02-28 | 将 notes/chat/emails 整合为 LaTeX 学术论文 |
| [MetaQiu/Trivium](https://github.com/MetaQiu/Trivium) | skill | 24 | 2026-02-15 | Claude/Codex/Gemini 多 agent 论文协作写作 |
| [AGISAFETYLAB/Paper-Writing-skill](https://github.com/AGISAFETYLAB/Paper-Writing-skill) | skill | 21 | 2026-06-26 | CS、医学、金融论文规划/写作/润色/图表/引用核查 |
| [dailycafi/biomed-paper-writing-skill](https://github.com/dailycafi/biomed-paper-writing-skill) | skill | 2 | 2026-03-16 | 生物医学/药学论文写作，CONSORT/STROBE/PRISMA/ARRIVE |
| [Jason-0409-G/scriptorium](https://github.com/Jason-0409-G/scriptorium) | skill | 1 | 2026-06-25 | DOI-verified literature library、NCBI/UniProt/PDB/AlphaFold、写作与审稿 |

## 文献检索 / 学术搜索 MCP

| repo | 类型 | stars | 最近 push | 方向 / 备注 |
|---|---|---:|---|---|
| [blazickjp/arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server) | mcp-server | 3235 | 2026-10-08 | arXiv 搜索和论文分析 MCP |
| [openags/paper-search-mcp](https://github.com/openags/paper-search-mcp) | mcp-server | 2920 | 2026-10-02 | arXiv/PubMed/bioRxiv 等论文检索下载 |
| [ShZhao27208/Aut_Sci_Write](https://github.com/ShZhao27208/Aut_Sci_Write) | skill-suite | 213 | 2026-08-13 | WoS/Elsevier/Springer 检索下载、综述、Zotero、PPT/HTML |
| [Dianel555/paper-search-mcp-nodejs](https://github.com/Dianel555/paper-search-mcp-nodejs) | mcp-server | 191 | 2026-09-20 | Web of Science/arXiv 等论文检索下载 |
| [andybrandt/mcp-simple-pubmed](https://github.com/andybrandt/mcp-simple-pubmed) | mcp-server | 171 | 2026-03-19 | PubMed 医学文献搜索 MCP |
| [zongmin-yu/semantic-scholar-fastmcp-mcp-server](https://github.com/zongmin-yu/semantic-scholar-fastmcp-mcp-server) | mcp-server | 166 | 2026-03-20 | 基于 FastMCP 的 Semantic Scholar API server |
| [cyanheads/pubmed-mcp-server](https://github.com/cyanheads/pubmed-mcp-server) | mcp-server | 163 | 2026-10-26 | PubMed/Europe PMC/Unpaywall、MeSH、full text |
| [Darkroaster/pubmearch](https://github.com/Darkroaster/pubmearch) | mcp-server | 150 | 2025-05-07 | PubMed 检索与分析 MCP（Python） |
| [takashiishida/arxiv-latex-mcp](https://github.com/takashiishida/arxiv-latex-mcp) | mcp-server | 149 | 2026-10-23 | arXiv LaTeX source 解析 |
| [JackKuo666/PubMed-MCP-Server](https://github.com/JackKuo666/PubMed-MCP-Server) | mcp-server | 132 | 2025-05-08 | PubMed 文章搜索、访问、分析 |
| [grll/pubmedmcp](https://github.com/grll/pubmedmcp) | mcp-server | 123 | 2025-09-02 | PubMed 数据查询 MCP（Python） |
| [afrise/academic-search-mcp-server](https://github.com/afrise/academic-search-mcp-server) | mcp-server | 118 | 2025-02-12 | Semantic Scholar 与 Crossref 检索 MCP |
| [JackKuo666/semanticscholar-MCP-Server](https://github.com/JackKuo666/semanticscholar-MCP-Server) | mcp-server | 87 | 2025-03-25 | Semantic Scholar 论文/作者/引用/参考文献 MCP |
| [benedict2310/Scientific-Papers-MCP](https://github.com/benedict2310/Scientific-Papers-MCP) | mcp-server | 63 | 2025-08-14 | arXiv 与 OpenAlex 论文检索 MCP |
| [akapet00/semantic-scholar-mcp](https://github.com/akapet00/semantic-scholar-mcp) | mcp-server | 37 | 2026-05-07 | Semantic Scholar 论文检索与分析 MCP |
| [lstudlo/ScholarMCP](https://github.com/lstudlo/ScholarMCP) | mcp-server | 31 | 2026-09-23 | 文献搜索、PDF ingestion、引用管理 |
| [TaewoooPark/scholar-megasearch](https://github.com/TaewoooPark/scholar-megasearch) | skill | 31 | 2026-08-14 | 20+ scholarly databases 多源检索与 PDF 获取 |
| [u9401066/pubmed-search-mcp](https://github.com/u9401066/pubmed-search-mcp) | mcp-server | 28 | 2026-10-20 | PubMed/Europe PMC/CORE/OpenAlex、citation networks、PICO |
| [JackKuo666/bioRxiv-MCP-Server](https://github.com/JackKuo666/bioRxiv-MCP-Server) | mcp-server | 26 | 2025-03-18 | bioRxiv 预印本检索、元数据与下载 MCP（FastMCP） |
| [masa-med-ai/pubmed-systematic-review](https://github.com/masa-med-ai/pubmed-systematic-review) | skill | 25 | 2026-05-20 | 与 PubMed MCP 联动做简易 systematic review |
| [zongmin-yu/semantic-scholar-skills](https://github.com/zongmin-yu/semantic-scholar-skills) | skill | 22 | 2026-03-16 | 以 Semantic Scholar 为首选的文献发现 skill，附带 MCP |
| [aringadre76/mcp-for-research](https://github.com/aringadre76/mcp-for-research) | mcp-server | 16 | 2026-05-12 | PubMed、Google Scholar、arXiv、JSTOR |
| [JackKuo666/medRxiv-MCP-Server](https://github.com/JackKuo666/medRxiv-MCP-Server) | mcp-server | 9 | 2025-03-18 | medRxiv 医学健康预印本检索与元数据 MCP |

## Zotero / CNKI / Google Scholar / 文献管理

| repo | 类型 | stars | 最近 push | 方向 / 备注 |
|---|---|---:|---|---|
| [MuiseDestiny/zotero-gpt](https://github.com/MuiseDestiny/zotero-gpt) | plugin | 7495 | 2026-05-01 | Zotero GPT 插件：通过 OpenAI 兼容接口与论文和文献库对话 |
| [54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp) | mcp-server | 5573 | 2026-10-16 | Zotero library 接入 Claude/AI assistant |
| [yilewang/llm-for-zotero](https://github.com/yilewang/llm-for-zotero) | agent-app | 3413 | 2026-10-22 | 基于 Zotero library 的 research agent system |
| [papersgpt/papersgpt-for-zotero](https://github.com/papersgpt/papersgpt-for-zotero) | plugin | 2681 | 2026-10-22 | Zotero AI/MCP 插件，多模型论文问答 |
| [lifan0127/ai-research-assistant](https://github.com/lifan0127/ai-research-assistant) | plugin | 1730 | 2025-04-01 | Aria：基于 OpenAI 模型的 Zotero 内置 LLM 科研助手插件 |
| [cookjohn/zotero-mcp](https://github.com/cookjohn/zotero-mcp) | plugin | 1250 | 2026-09-09 | Zotero 与 AI assistant 深度集成 |
| [cookjohn/cnki-skills](https://github.com/cookjohn/cnki-skills) | skill-suite | 1017 | 2026-03-13 | CNKI 检索、PDF、Zotero 导出 |
| [cookjohn/gs-skills](https://github.com/cookjohn/gs-skills) | skill-suite | 535 | 2026-03-13 | Google Scholar 检索、引用追踪、Zotero 导出 |
| [introfini/ZotSeek](https://github.com/introfini/ZotSeek) | plugin | 235 | 2026-10-08 | Zotero 语义搜索，本地隐私，内置 MCP |
| [kaliaboi/mcp-zotero](https://github.com/kaliaboi/mcp-zotero) | mcp-server | 163 | 2025-02-04 | Claude Desktop 连接 Zotero Cloud |
| [kujenga/zotero-mcp](https://github.com/kujenga/zotero-mcp) | mcp-server | 162 | 2026-08-07 | Zotero Web API MCP server（Python） |
| [TonybotNi/ZotLink](https://github.com/TonybotNi/ZotLink) | mcp-server | 136 | 2025-10-12 | 保存 arXiv/CVF/bioRxiv/medRxiv 到 Zotero |
| [dralkh/seerai](https://github.com/dralkh/seerai) | plugin | 94 | 2026-10-06 | Zotero AI plugin，RAG、OCR、systematic reviews、MCP、skills |
| [gyger/mcp-pyzotero](https://github.com/gyger/mcp-pyzotero) (已归档) | mcp-server | 56 | 2025-11-20 | 本地 Zotero MCP connector |
| [Xevos117/mcp-zotero](https://github.com/Xevos117/mcp-zotero) | mcp-server | 38 | 2026-10-26 | Zotero library operations、DOI、PDF、Unpaywall、docx citation fields |
| [cookjohn/pm-skills](https://github.com/cookjohn/pm-skills) | skill-suite | 19 | 2026-03-13 | PubMed literature search、citation export、Zotero |

## 生信 / 组学 / 单细胞 Skills

| repo | 类型 | stars | 最近 push | 方向 / 备注 |
|---|---|---:|---|---|
| [GPTomics/bioSkills](https://github.com/GPTomics/bioSkills) (已归档) | skill-suite | 1225 | 2026-08-15 | RNA-seq、scRNA、variant、multi-omics |
| [ClawBio/ClawBio](https://github.com/ClawBio/ClawBio) | skill-suite | 1166 | 2026-10-26 | 生信原生 agent skill 库：95 个带示例数据的 skills、Galaxy 工具封装，支持 pip/conda 安装，并提供 Claude Code plugin 与 MCP server |
| [jaechang-hits/SciAgent-Skills](https://github.com/jaechang-hits/SciAgent-Skills) | skill-suite | 383 | 2026-10-22 | 197 个生命科学/生信 skills |
| [TianGzlab/OmicsClaw](https://github.com/TianGzlab/OmicsClaw) | agent-app | 161 | 2026-10-07 | 多组学分析到论文生成 |
| [swaruplab/operon](https://github.com/swaruplab/operon) | agent-app | 101 | 2026-10-11 | Claude Code 生信 IDE/protocols |
| [variomeanalytics/bioinformatics-agent-skills](https://github.com/variomeanalytics/bioinformatics-agent-skills) | mcp-server | 63 | 2026-04-18 | 查询 78 个 bioinformatics workflows 的知识图谱 |
| [cafferychen777/ChatSpatial](https://github.com/cafferychen777/ChatSpatial) | mcp-server | 45 | 2026-10-20 | 空间转录组自然语言分析 |
| [ma-compbio-lab/SkillFoundry](https://github.com/ma-compbio-lab/SkillFoundry) | framework | 43 | 2026-09-14 | 计算生物学 skills 发现/验证 |
| [scmcphub/scmcp](https://github.com/scmcphub/scmcp) | mcp-suite | 16 | 2025-07-10 | 自然语言驱动的 scRNA-seq 分析 MCP，同时作为 scanpy-mcp、liana-mcp、cellrank-mcp 共享 AnnData 的后端 |
| [Bioconductor/ai-agent-skills](https://github.com/Bioconductor/ai-agent-skills) | skill-suite | 10 | 2026-10-07 | R/Bioconductor 与统计生信 |
| [scmcphub/scanpy-mcp](https://github.com/scmcphub/scanpy-mcp) | mcp-server | 2 | 2025-06-27 | Scanpy MCP：覆盖读写、预处理、聚类、差异表达与绘图 |

## 蛋白设计 / 结构生物学

| repo | 类型 | stars | 最近 push | 方向 / 备注 |
|---|---|---:|---|---|
| [adaptyvbio/protein-design-skills](https://github.com/adaptyvbio/protein-design-skills) | skill-suite | 170 | 2026-06-11 | Adaptyv Bio 的蛋白设计工作流 skill 套件 |
| [001TMF/blatant-why](https://github.com/001TMF/blatant-why) | agent-app | 119 | 2026-10-16 | 多 agent 生物药设计 campaign，编排 BoltzGen、PXDesign、Protenix 与云端工具，面向抗体、纳米抗体和从头设计 binder |
| [charlesxu90/ProteinMCP](https://github.com/charlesxu90/ProteinMCP) | framework | 73 | 2026-05-01 | 自主蛋白工程 agentic framework，含 Claude Code workflow skills 和 38 个 MCP |
| [vrtejus/pymol-mcp](https://github.com/vrtejus/pymol-mcp) | mcp-server | 68 | 2025-03-18 | 从 Claude 控制 PyMOL：加载结构、切换表示、测量、比对，并在 PyMOL 内执行 Python |
| [PDBeurope/PDBe-MCP-Servers](https://github.com/PDBeurope/PDBe-MCP-Servers) | mcp-server | 43 | 2026-10-22 | PDBe/蛋白结构 |
| [Augmented-Nature/AlphaFold-MCP-Server](https://github.com/Augmented-Nature/AlphaFold-MCP-Server) | mcp-server | 36 | 2025-12-21 | 非官方 AlphaFold DB MCP：预测结构与置信度指标（Node.js） |
| [Augmented-Nature/PDB-MCP-Server](https://github.com/Augmented-Nature/PDB-MCP-Server) | mcp-server | 28 | 2025-12-21 | 非官方 RCSB PDB MCP：结构检索与元数据（Node.js） |
| [jasonkim8652/protein-design-mcp](https://github.com/jasonkim8652/protein-design-mcp) | mcp-server | 18 | 2026-10-01 | 串联 RFdiffusion、ProteinMPNN、ESMFold 与 AlphaFold2 的蛋白 binder 设计 MCP |
| [cyanheads/protein-mcp-server](https://github.com/cyanheads/protein-mcp-server) | mcp-server | 6 | 2026-10-17 | PDB + AlphaFold 蛋白结构/注释 federation |
| [PabloPauling/posebusters-mcp-server](https://github.com/PabloPauling/posebusters-mcp-server) | mcp-server | 5 | 2025-07-14 | PoseBusters 分子对接姿态验证 MCP |
| [smaniches/alphafold-sovereign-mcp](https://github.com/smaniches/alphafold-sovereign-mcp) | mcp-server | 4 | 2026-10-26 | AlphaFold DB + 8 public sources，本地知识图谱 |

## 流程 / 序列与基因组工具 MCP

| repo | 类型 | stars | 最近 push | 方向 / 备注 |
|---|---|---:|---|---|
| [bio-mcp/bio-mcp-blast](https://github.com/bio-mcp/bio-mcp-blast) | mcp-server | 11 | 2025-06-29 | 封装本地 BLAST+ 的序列比对搜索 MCP |
| [igvteam/igv-mcp](https://github.com/igvteam/igv-mcp) | mcp-server | 4 | 2025-12-07 | igvteam 官方 MCP：从 agent 控制 IGV 桌面基因组浏览器 |
| [kmaneesh/biopython-mcp](https://github.com/kmaneesh/biopython-mcp) | mcp-server | 3 | 2026-01-16 | 以 MCP 工具形式暴露 Biopython 序列处理功能 |
| [bio-mcp/bio-mcp-bwa](https://github.com/bio-mcp/bio-mcp-bwa) | mcp-server | 0 | 2025-07-10 | BWA 比对 MCP：构建索引、运行 BWA-MEM、输出 SAM |
| [wjlim/nf-core_mcp](https://github.com/wjlim/nf-core_mcp) | mcp-server | 0 | 2025-04-08 | 通过 MCP 浏览 nf-core 流程、模块、配置与工作流文件 |

## 生物医学 / 临床 / 医学研究

| repo | 类型 | stars | 最近 push | 方向 / 备注 |
|---|---|---:|---|---|
| [FreedomIntelligence/OpenClaw-Medical-Skills](https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills) | skill-suite | 3080 | 2026-07-21 | OpenClaw 医学 AI skills 大型集合 |
| [aipoch/medical-research-skills](https://github.com/aipoch/medical-research-skills) | skill-suite | 1988 | 2026-09-17 | 医学研究、protocol、数据分析、学术写作 |
| [mims-harvard/ToolUniverse](https://github.com/mims-harvard/ToolUniverse) | tool | 1759 | 2026-10-26 | 生物医学 AI scientist 工具宇宙 |
| [LeonChaoX/qinyan-academic-skills](https://github.com/LeonChaoX/qinyan-academic-skills) | skill-suite | 980 | 2026-07-20 | 177 个学术研究 skills，含生信、药物发现、临床医学 |
| [genomoncology/biomcp](https://github.com/genomoncology/biomcp) | mcp-server | 664 | 2026-10-24 | BioMCP：临床试验、基因数据、医学文献 |
| [Cicatriiz/healthcare-mcp-public](https://github.com/Cicatriiz/healthcare-mcp-public) | mcp-server | 131 | 2025-08-16 | FDA、PubMed、medRxiv、临床试验、ICD-10 等医疗数据 |
| [JamesANZ/medical-mcp](https://github.com/JamesANZ/medical-mcp) | mcp-server | 118 | 2026-10-15 | FDA、WHO、PubMed、Google Scholar、RxNorm |
| [cyanheads/clinicaltrialsgov-mcp-server](https://github.com/cyanheads/clinicaltrialsgov-mcp-server) | mcp-server | 98 | 2026-10-26 | ClinicalTrials.gov 搜索、详情、结果、患者匹配 |
| [lynnlangit/precision-medicine-mcp](https://github.com/lynnlangit/precision-medicine-mcp) | mcp-suite | 24 | 2026-08-25 | Precision medicine，多组学/基因组/空间转录组 |
| [pascalwhoop/medical-mcps](https://github.com/pascalwhoop/medical-mcps) | mcp-suite | 23 | 2026-09-01 | 主要 biomedical databases MCP 工具集合 |
| [JackKuo666/ClinicalTrials-MCP-Server](https://github.com/JackKuo666/ClinicalTrials-MCP-Server) | mcp-server | 18 | 2025-04-09 | ClinicalTrials.gov 检索与研究详情 MCP（Python） |
| [HolobiomicsLab/asb-skill-collections](https://github.com/HolobiomicsLab/asb-skill-collections) | skill-suite | 16 | 2026-09-20 | Scientific AI agents 的 evidence-grounded skill/tool collections |

## 生物数据库 / 通路 / 化学 / 药物发现 MCP

| repo | 类型 | stars | 最近 push | 方向 / 备注 |
|---|---|---:|---|---|
| [Augmented-Nature/ChEMBL-MCP-Server](https://github.com/Augmented-Nature/ChEMBL-MCP-Server) | mcp-server | 89 | 2025-12-21 | 非官方 ChEMBL MCP：化合物、靶点与生物活性查询（Node.js） |
| [longevity-genie/biothings-mcp](https://github.com/longevity-genie/biothings-mcp) | mcp-server | 37 | 2025-11-03 | Holy Bio MCP 家族的 BioThings API（MyGene、MyVariant、MyChem）MCP |
| [longevity-genie/gget-mcp](https://github.com/longevity-genie/gget-mcp) | mcp-server | 33 | 2025-10-27 | gget 生信工具封装 |
| [biocontext-ai/knowledgebase-mcp](https://github.com/biocontext-ai/knowledgebase-mcp) | mcp-server | 31 | 2026-10-12 | BioContextAI 知识库 MCP，打包常用生物医学数据库，可自托管或使用远程服务 |
| [ammawla/encode-toolkit](https://github.com/ammawla/encode-toolkit) | mcp-server | 21 | 2026-09-27 | ENCODE 基因组数据查询工具包（MCP / Claude plugin） |
| [Augmented-Nature/Augmented-Nature-UniProt-MCP-Server](https://github.com/Augmented-Nature/Augmented-Nature-UniProt-MCP-Server) | mcp-server | 21 | 2025-12-21 | 非官方 UniProt MCP：26 个蛋白查询、比较与结构工具（Node.js） |
| [longevity-genie/opengenes-mcp](https://github.com/longevity-genie/opengenes-mcp) | mcp-server | 21 | 2025-10-14 | OpenGenes 衰老基因数据库 MCP：寿命实验、衰老标志、长寿相关变异 |
| [longevity-genie/holy-bio-mcp](https://github.com/longevity-genie/holy-bio-mcp) | mcp-suite | 20 | 2025-07-14 | Holy Bio MCP 家族总入口（gget、BioThings、OpenGenes、SynergyAge、药理学），Bio x AI Hackathon 2025 获奖项目 |
| [tamerh/biobtree](https://github.com/tamerh/biobtree) | mcp-server | 20 | 2026-10-14 | BioBTree v2，70+ biomedical datasets |
| [nickzren/opentargets-mcp](https://github.com/nickzren/opentargets-mcp) | mcp-server | 19 | 2026-10-09 | Open Targets MCP：靶点-疾病关联与药物证据 |
| [Augmented-Nature/Reactome-MCP-Server](https://github.com/Augmented-Nature/Reactome-MCP-Server) | mcp-server | 12 | 2025-12-21 | 非官方 Reactome MCP，通过 Content Service 访问人工审编的通路数据 |
| [cyanheads/pubchem-mcp-server](https://github.com/cyanheads/pubchem-mcp-server) | mcp-server | 10 | 2026-10-24 | PubChem 化合物、性质、安全、生物活性 |
| [longevity-genie/synergy-age-mcp](https://github.com/longevity-genie/synergy-age-mcp) | mcp-server | 10 | 2025-08-25 | SynergyAge MCP：遗传干预及其组合对寿命影响的数据库 |
| [Augmented-Nature/SureChEMBL-MCP-Server](https://github.com/Augmented-Nature/SureChEMBL-MCP-Server) | mcp-server | 8 | 2025-12-21 | 非官方 SureChEMBL MCP：化学专利检索（Node.js） |
| [donbr/lifesciences-research](https://github.com/donbr/lifesciences-research) | mcp-suite | 8 | 2026-10-15 | Open Targets、ChEMBL、UniProt |
| [effieklimi/ensembl-mcp-server](https://github.com/effieklimi/ensembl-mcp-server) | mcp-server | 8 | 2026-02-11 | Ensembl REST MCP：基因、序列、变异与比较基因组学（TypeScript） |
| [hlydecker/ucsc-genome-mcp](https://github.com/hlydecker/ucsc-genome-mcp) | mcp-server | 6 | 2025-11-13 | UCSC Genome Browser API MCP：轨道与序列查询 |
| [longevity-genie/pharmacology-mcp](https://github.com/longevity-genie/pharmacology-mcp) | mcp-server | 6 | 2025-09-02 | Holy Bio MCP 家族的药理学数据库 MCP（靶点、配体、相互作用） |
| [EBISPOT/GrEBI](https://github.com/EBISPOT/GrEBI) | mcp-server | 5 | 2026-10-21 | biomedical data integration，API/MCP server |
| [Augmented-Nature/STRING-db-MCP-Server](https://github.com/Augmented-Nature/STRING-db-MCP-Server) | mcp-server | 4 | 2025-12-21 | 非官方 STRING MCP：蛋白相互作用网络、功能富集与同源查询 |
| [Lucas-Servi/kegg-mcp-server-python](https://github.com/Lucas-Servi/kegg-mcp-server-python) | mcp-server | 3 | 2026-10-16 | KEGG REST MCP：通路、基因与化合物（Python） |
| [smaniches/uniprot-mcp](https://github.com/smaniches/uniprot-mcp) | mcp-server | 3 | 2026-10-26 | 可审计 UniProt MCP，release pinning/offline replay |

## 科研 Agent Apps / Workspaces

| repo | 类型 | stars | 最近 push | 方向 / 备注 |
|---|---|---:|---|---|
| [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) | agent-app | 5907 | 2026-10-19 | 研究、实验、写作、投稿，支持 Claude Code/Codex CLI |
| [snap-stanford/Biomni](https://github.com/snap-stanford/Biomni) | agent-app | 4012 | 2026-10-19 | 通用生物医学 AI agent，结合检索增强规划与代码执行（Apache-2.0；会执行 LLM 生成的代码，建议沙箱运行） |
| [yb2460/harness-anything](https://github.com/yb2460/harness-anything) | framework | 2538 | 2026-10-09 | WPS/MS Office/Zotero、academic skills、文档自动化 |
| [K-Dense-AI/k-dense-byok](https://github.com/K-Dense-AI/k-dense-byok) | agent-app | 1401 | 2026-10-16 | 基于 scientific-agent-skills 的桌面 AI co-scientist |
| [beita6969/ScienceClaw](https://github.com/beita6969/ScienceClaw) | agent-app | 1019 | 2026-10-16 | 自进化科研 assistant，skills + persistent memory |
| [AgentTeam-TaichuAI/ScienceClaw](https://github.com/AgentTeam-TaichuAI/ScienceClaw) | agent-app | 674 | 2026-05-09 | LangChain DeepAgents + sandbox 的科研 assistant |
| [ymx10086/ResearchClaw](https://github.com/ymx10086/ResearchClaw) | agent-app | 315 | 2026-04-04 | 文献综述、笔记、实验跟踪、论文写作 |
| [WenyuChiou/research-hub](https://github.com/WenyuChiou/research-hub) | agent-app | 66 | 2026-10-26 | Zotero、Obsidian、NotebookLM，CLI/MCP/REST/dashboard |

## 图表 / PDF / LaTeX / 研究产物工具

| repo | 类型 | stars | 最近 push | 方向 / 备注 |
|---|---|---:|---|---|
| [PDFMathTranslate/PDFMathTranslate](https://github.com/PDFMathTranslate/PDFMathTranslate) | tool | 37880 | 2026-10-26 | 科学 PDF 翻译，保留排版，支持 MCP、Docker、Zotero |
| [llmsresearch/paperbanana](https://github.com/llmsresearch/paperbanana) | tool | 2419 | 2026-09-17 | 自动学术图、diagram、research visuals |
| [Dsadd4/AgentFigureGallery](https://github.com/Dsadd4/AgentFigureGallery) | skill | 171 | 2026-09-05 | 科学绘图 skill，Claude/Codex/Cursor |

## Awesome / Registry / 继续深挖入口

| repo | 类型 | stars | 最近 push | 方向 / 备注 |
|---|---|---:|---|---|
| [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) | directory | 96880 | 2026-10-23 | 通用 MCP 目录，含 Biology/Medicine/Bioinformatics 小节 |
| [anthropics/life-sciences](https://github.com/anthropics/life-sciences) | registry | 624 | 2026-10-23 | Claude life-sciences MCP/skills 目录 |
| [InternScience/Awesome-Scientific-Skills](https://github.com/InternScience/Awesome-Scientific-Skills) | directory | 577 | 2026-08-13 | 科学研究 agent skills 目录 |
| [WenyuChiou/ai-research-skills](https://github.com/WenyuChiou/ai-research-skills) | directory | 407 | 2026-10-26 | literature review、research design、manuscript writing |
| [BioTender-max/awesome-bio-agent-skills](https://github.com/BioTender-max/awesome-bio-agent-skills) | directory | 207 | 2026-07-01 | 生物医学 agent skills 目录，覆盖 genomics、proteomics、single-cell、clinical AI、protein design |
| [Epsilon617/Codex-Academic-Skills](https://github.com/Epsilon617/Codex-Academic-Skills) | skill-suite | 195 | 2026-06-16 | Codex research-oriented skills 目录 |
| [GoekeLab/awesome-genomic-skills](https://github.com/GoekeLab/awesome-genomic-skills) | directory | 127 | 2026-09-22 | genomics/bioinformatics agent skills、MCP、benchmarks |
| [O0000-code/awesome-academic-skills](https://github.com/O0000-code/awesome-academic-skills) | directory | 51 | 2026-10-25 | academic agent skills，按科研生命周期组织 |
| [biocontext-ai/registry](https://github.com/biocontext-ai/registry) | registry | 23 | 2026-10-20 | BioContextAI 生物医学 MCP server 注册表，同时是本目录的候选来源 |
| [JuneYaooo/awesome-medical-ai-skills](https://github.com/JuneYaooo/awesome-medical-ai-skills) | directory | 16 | 2026-10-22 | 医疗健康领域 agent skills、MCP server 与工具的人工目录 |
| [Harsh9005/awesome-scientific-ai-tools](https://github.com/Harsh9005/awesome-scientific-ai-tools) | directory | 10 | 2026-05-15 | 科学研究 AI tools、MCP、agent skills |
| [chrisliu298/awesome-research-agents](https://github.com/chrisliu298/awesome-research-agents) | directory | 4 | 2026-05-19 | research agents、skill libraries、autonomous research loops、paper-writing pipelines |
| [biocontext-ai/meta-mcp](https://github.com/biocontext-ai/meta-mcp) | mcp-server | 2 | 2026-05-18 | 以极小上下文开销访问 BioContextAI 注册表中全部 server 的 Meta MCP |

## 纳入 / 排除规则

- 纳入：明确面向科研、论文写作、文献、Zotero/PubMed/arXiv/Semantic Scholar、医学、生物信息、生命科学，并以 skill、plugin、MCP、agent workflow 或 agent-ready tool 形式服务 AI agent 的仓库。
- 保留低 star 项：如果领域直接、接口明确、方向独特，即使 stars 很低也保留。
- 排除：普通教程、书籍/藏书 app、无科研方向的通用 agent 基础设施、无新增价值的镜像或 fork、无描述且无法判断用途的空壳仓库。
- 备注必须说明仓库做什么、与同类条目有何差异；只写一个数据库名不算备注。

## 覆盖说明

GitHub Search 无法保证完整覆盖。新仓库通过每周的 `discovery/candidates.md` 候选报告、awesome 列表反查以及记录在 `data/triage.tsv` 中的人工审核进入目录。
<!-- CATALOG:END -->

## 许可

脚本采用 MIT 许可；目录数据与生成文档采用 CC BY 4.0。见 [LICENSE](LICENSE)。
