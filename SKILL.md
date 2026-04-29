---
name: paper-reading
description: Use this skill when the user requests deep reading, analysis, or comprehension of an academic research paper. This includes explaining methodology, breaking down formulas and mathematical notation, translating and explaining foreign-language papers into Chinese (adapts for any source language — English, Japanese, German, French, etc.), summarizing core contributions and experimental results, and generating structured Obsidian-ready reading notes with YAML frontmatter and bidirectional links. Supports two modes: paragraph-by-paragraph intensive reading with Agentic Q&A support, and structured in-depth overview with a comprehensive 20-point analysis framework backed by multi-agent parallel deep analysis. Trigger only for academic literature (arXiv preprints, conference/journal/proceedings papers). Do NOT trigger for: paper writing assistance, code review, general non-academic translation, product/technical documentation reading, textbook chapter summaries, patent analysis, or encyclopedia article reorganization.
---

# Paper Reading Assistant

Deeply analyze academic papers — their thesis, innovations, core methods, and open problems. Deconstruct content in an accessible yet rigorous way, and help users build a structured academic knowledge system.

## Core Capabilities

- **Academic Semantic Parsing**: Go beyond literal translation — identify the author's argumentation logic, experimental intent, and scholarly context.
- **Formula / Logic Decomposition**: Transform abstract formulas into physical meaning, variable relationships, and logical derivations.
- **Visual Information Extraction** (on-demand): Accurately analyze trends, comparisons, and key data in paper figures/tables (Fig/Table). Only activate when the user explicitly requests image processing.
- **Obsidian Document Engineering**: Proficient use of Markdown, YAML metadata, and bidirectional links (Wikilinks) for knowledge graph construction. All formulas use MathJax-compatible syntax.
- **Multi-Agent Parallel Analysis**: For Mode B, launch parallel subagents to simultaneously analyze different dimensions (methods, math, results, literature context, critical assessment), then synthesize into a unified reading note — inspired by nuwa-skill's agent swarm architecture.

---

## Execution Pipeline Overview

```
Phase 0: Initialization (confirm mode, extract metadata)
  ├─ Mode A → Phase A: Paragraph-by-Paragraph Deep Reading
  │             ├─ Agentic Q&A Protocol (on-demand research)
  │             └─ Offer to generate Mode B summary on completion
  └─ Mode B → Phase 0.5: Pre-Analysis Setup (output directory, agent dispatch plan)
              Phase 1: Multi-Agent Parallel Deep Analysis (6-8 agents)
              Phase 1.5: Cross-Agent Synthesis Checkpoint (user review gate)
              Phase 2: Structured 20-Point Note Generation
              Phase 2.5: Completeness & Quality Check
              Phase 3: Dual-Agent Quality Verification (math + readability)
              → Deliver final reading note
```

---

## Phase 0: Initialization

When engaging with the user, complete the following steps in order:

### Step 1: Confirm Reading Mode and Preferences

Ask concise questions to establish:

**Reading Mode**:
- **Mode A**: Full-text paragraph-by-paragraph deep reading — go through each section in order, providing original text, expert explanation, and formula/logic deconstruction. Supports Agentic Q&A (researches in real-time for questions about related work/context). After completing all paragraphs, offer to generate a comprehensive Mode B summary note.
- **Mode B**: Structured comprehensive overview using a systematic 20-point analysis framework backed by multi-agent parallel deep analysis. 6-8 subagents simultaneously analyze different dimensions — ideal for literature reviews, systematic reviews, or when preparing to deeply understand and cite a paper. No paragraph-level walkthrough.

**Image Handling**:
- Do you need analysis of figures/tables in the paper?
- If the user says no, **completely ignore all images** — do not reference, link to, or analyze any Fig/Table.

**Source Language Detection** (automatic):
- When the user provides a paper, first determine its language.
- If the paper is in **Chinese**: skip all translation steps. Provide only original text blocks and professional explanation. Do not offer or perform translation.
- If the paper is in a **foreign language** (English, Japanese, German, French, Korean, etc.): translate to Chinese alongside original text.

**Paper Type Detection** (automatic — informs Phase 1 agent dispatch):
- Identify the paper genre: theoretical (proofs/theorems), experimental/systems, survey/review, benchmark/evaluation, or position/vision paper. This determines which agents are prioritized in Phase 1.

Proceed only after confirmation.

### Step 2: Paper Metadata and Initial Overview

After receiving the paper, provide:

- **Paper Metadata**: Title, authors, year/venue, core domain/keywords.
- **Paper Type**: Identified genre (theoretical / experimental / survey / benchmark / position).
- **Three-Sentence Summary**: What pain point does it address? What is the core method? What breakthrough did it achieve?
- **Reading Recommendation**: Based on the confirmed mode, suggest next steps.
  - Mode A: Point out core chapters and recommended reading order. Mention that Agentic Q&A is available for any question during reading. After paragraph reading completes, a comprehensive 20-point summary note (Mode B format) can be generated on request.
  - Mode B: Describe the 6-8 parallel analysis dimensions that will be deployed in Phase 1, and the expected output quality.

---

## Mode A: Paragraph-by-Paragraph Deep Reading

For each user-specified paragraph/section, run through the following cycle:

### 1. Source Text and Translation
> Present the original text using Markdown blockquote format.
> **If foreign language**: provide a professional, fluent Chinese translation alongside the original.
> **If originally Chinese**: present only the original text; skip translation entirely.

### 2. Expert Explanation
- **Logical Position**: Where this paragraph sits in the paper's overall argumentation chain.
- **Concept Illumination**: Provide brief background for prerequisite knowledge mentioned (e.g., Transformer, Markov chains, gradient descent).
- **Knowledge Focus**: Focus on *what the concept is and why it matters*, not on the author's writing style.

### 3. Formula / Logic Breakdown (triggered as needed)
For formulas within the paragraph, provide:
- Symbol meaning list
- Key derivation points or logical connections
- Physical/mathematical significance
- **All formulas in MathJax syntax**: inline `$...$`, display `$$...$$`. **Never write math formulas inside code blocks.**

### 4. Figure Handling (only when user confirmed image processing)
- Extract Fig.x and provide links in `![[Fig.x description]]` format (if image resources are accessible).
- Interpret axes, curve trends, comparison items, and experimental conclusions.

After each round, provide a collapsible **Obsidian Knowledge Snippet** containing key terms as bidirectional links, critical formulas (MathJax), and bullet-point takeaways — ready for the user to save immediately.

### Agentic Q&A Protocol (Mode A)

When the user asks a question during reading that requires information beyond the current paper (e.g., "How does this compare to method X?", "What's the state of the art on this benchmark?", "Has this been refuted?"), the skill MUST research before answering, rather than relying on training data. This protocol is adapted from nuwa-skill's Agentic Protocol pattern.

#### Step 1: Question Classification

| Type | Feature | Action |
|------|---------|--------|
| **In-paper question** | Answerable from the paper text itself | Answer directly from paper content |
| **External factual question** | Involves other papers, benchmarks, methods, or current state | → Phase A-Research first |
| **Concept clarification** | Asks about background knowledge | Provide explanation; optionally search for precise definitions |
| **Critical evaluation** | Asks for judgment or comparison that requires external benchmarks | → Phase A-Research first |

**Judgment rule**: If answering without current information risks being inaccurate or outdated, must research first.

#### Step 2: Research (Phase A-Research)

**Must use tools (WebSearch etc.) to obtain factual information. Cannot skip.**

Research dimensions depend on the question type:

| Question Type | Research Focus |
|--------------|----------------|
| Comparison to other methods | Search for recent benchmarks, survey tables, method comparisons on PapersWithCode/arXiv |
| State-of-the-art | Search for leaderboard results, recent survey papers, latest arXiv publications |
| Has this been refuted? | Search for follow-up papers, critical blog posts, reproducibility issues |
| Current impact | Search citation counts, notable follow-up work, community reception |
| Code availability | Search GitHub/official repos for implementation |

**Output format**: Research results are organized internally (not shown to user). The user sees only the answer informed by fresh research.

#### Step 3: Answer

Based on research results, answer using the paper's context and domain knowledge. Clearly distinguish:
- Facts from the current paper
- Facts from external research
- Inferences and judgments

**After completing all paragraphs**: Offer to generate a comprehensive Mode B summary using the 20-point analysis framework with multi-agent parallel analysis. The user can accept or decline. If accepted, proceed to Mode B Phase 1.

---

## Mode B: Multi-Agent Systematic Analysis Pipeline

### Phase 0.5: Pre-Analysis Setup

**Before launching agents**, complete these setup steps:

#### Step 1: Create Output Directory Structure

```
paper-reading-notes/
└── [paper-short-name]/
    ├── reading-note.md                 # Final output (20-point analysis)
    ├── analysis/                       # Per-agent analysis results
    │   ├── 01-core-argument.md          # Agent 1 output
    │   ├── 02-methodology.md            # Agent 2 output
    │   ├── 03-mathematical-analysis.md  # Agent 3 output
    │   ├── 04-results-data.md           # Agent 4 output
    │   ├── 05-literature-context.md     # Agent 5 output
    │   ├── 06-critical-assessment.md    # Agent 6 output
    │   ├── 07-figure-analysis.md       # Agent 7 output (only if image mode)
    │   └── 08-code-implementation.md   # Agent 8 output (only if code available)
    └── scripts/                        # Utility scripts (copied from skill)
        ├── paper_analyze.py
        └── reading_note_quality.py
```

> **Critical rule**: All analysis files must reside within the output directory. The reading note must be self-contained — copy the entire directory to any Obsidian vault and it works without external dependencies.

#### Step 2: Determine Agent Dispatch Plan

Based on the paper type detected in Phase 0, prioritize agents:

| Paper Type | Required Agents (always) | Optional Agents (if applicable) |
|------------|--------------------------|--------------------------------|
| **Theoretical** (proofs/theorems) | 1, 3, 5, 6 | 2, 8 (if proofs are mechanized) |
| **Experimental/Systems** | 1, 2, 4, 6 | 3 (if heavy math), 7 (if user wants figures), 8 |
| **Survey/Review** | 1, 5, 6 | 4 (if meta-analysis) |
| **Benchmark/Evaluation** | 1, 2, 4, 6 | 3, 5, 7, 8 |
| **Position/Vision** | 1, 5, 6 | — |

Also factor in user's image/table preference for Agent 7, and whether code is linked in the paper for Agent 8.

#### Step 3: Confirm Plan with User

Display the agent dispatch plan briefly:

```
Paper type: Experimental
Dispatching 6 agents: 1-Core Argument, 2-Methodology, 3-Math Analysis,
4-Results, 5-Literature Context, 6-Critical Assessment
(+1 if figures requested, +1 if code available)
Estimated depth: [high/medium]
```

> No need for explicit user approval unless paper type is ambiguous. If auto-detection is confident, proceed directly.

---

### Phase 1: Multi-Agent Parallel Deep Analysis

Launch **all applicable agents in parallel** using subagent spawn. Each agent independently analyzes the paper from its specialized dimension and writes results to its designated output file. This is the core innovation — instead of one agent reading the paper once, 6-8 agents each read it through a different lens, producing much richer analysis.

#### Agent Task Definitions

| Agent | Analysis Dimension | Search/External | Output File |
|-------|-------------------|-----------------|-------------|
| **1 核心论点** | Core thesis, hypotheses, contributions, innovation claims | Verify claims against known literature | `01-core-argument.md` |
| **2 方法论** | Methods, experimental design, protocols, implementation details | Search for official code repos, implementation variants | `02-methodology.md` |
| **3 数学分析** | Formal/mathematical decomposition, proofs, derivations, notation | Search for errata, corrected proofs, known issues | `03-mathematical-analysis.md` |
| **4 结果数据** | Results, metrics, tables, statistical tests, ablation studies | Cross-check against PapersWithCode, leaderboards | `04-results-data.md` |
| **5 文献脉络** | Related work context, intellectual lineage, comparative positioning | Search citation graph, prior art, follow-up work | `05-literature-context.md` |
| **6 批判评估** | Limitations, biases, methodological flaws, overclaims | Search for published critiques, reproducibility reports | `06-critical-assessment.md` |
| **7 图表分析** | Figure/Table interpretation (only if user enabled image mode) | — | `07-figure-analysis.md` |
| **8 代码实现** | Code availability, reproducibility, implementation quality (only if code linked) | Search GitHub, replicate repos | `08-code-implementation.md` |

#### Agent Prompt Template

When spawning each agent, use this structure (example for Agent 2 - Methodology):

```
Your task: Analyze the "[Paper Title]" paper through the lens of METHODOLOGY & EXPERIMENTAL DESIGN.

Paper content is provided below. Read it thoroughly with a focus on:

REQUIRED ANALYSIS:
1. List all methods/techniques/algorithms used, with their roles
2. Describe the experimental setup: datasets, baselines, hyperparameters, hardware, evaluation protocol
3. Identify the evaluation metrics and justify their appropriateness for the task
4. Note any methodological innovations (what's new vs. adapted from prior work)
5. Flag any missing experimental details that would hamper reproducibility

EXTERNAL RESEARCH:
- Search for official code repositories, re-implementations, or reproducibility reports
- Check if the method has been adopted/compared in later work
- Note any known implementation issues or corrections

OUTPUT:
- Write to: [output-dir]/analysis/02-methodology.md
- Format: Clear headings, bullet points for key items, tables for comparisons
- Mark source of each claim: [paper] / [external search] / [inference]
- Flag uncertainties with [UNCERTAIN: reason]
- If the paper has insufficient detail on any point, mark as [GAP: description]

DO NOT summarize the entire paper. Stay focused on methodology only.
```

Other agents follow the same structure, adjusted for their dimension. The key principle: **each agent goes deep on its dimension, not wide across the whole paper**.

#### Hard Requirements for All Agents
- Results MUST be written to the designated analysis file. Analysis not saved = analysis not done.
- Mark the source of each claim: `[paper]` / `[external]` / `[inferred]`
- When finding contradictions between agents' domains, note them (they'll be synthesized in Phase 1.5)
- Flag uncertainties and information gaps explicitly: `[UNCERTAIN: reason]` or `[GAP: description]`

#### Agent Timeout & Failure Handling

| Situation | Handling |
|-----------|----------|
| Agent times out (no useful results in 5 min) | Mark that dimension as `[INSUFFICIENT DATA]`, do not block other agents |
| Agent finds very little to analyze (e.g., paper has minimal math → Agent 3) | Short output noting `[DIMENSION NOT APPLICABLE]` is acceptable |
| Agent results conflict with another agent | Preserve conflict — it's valuable signal. Tag with `[CONTRADICTS Agent N]` |
| External search returns nothing | Note `[NO EXTERNAL DATA FOUND]`, base analysis on paper content only |

**Key principle**: Better to deliver a note honestly marking gaps than to fabricate analysis for missing dimensions.

---

### Phase 1.5: Cross-Agent Synthesis Checkpoint

**After all agents complete, pause and present a synthesis summary.** This is a critical quality gate — garbage in, garbage out. Catching gaps here is far cheaper than fixing a flawed reading note later.

Use the `scripts/paper_analyze.py` tool to automatically scan all agent outputs and generate a summary table:

```bash
python paper_analyze.py [output-dir]
```

The tool outputs:

```
┌──────────────────────┬─────────────────────────────────────┬────────────┐
│ Agent                │ Key Findings                        │ Confidence │
├──────────────────────┼─────────────────────────────────────┼────────────┤
│ 1 核心论点           │ Novel attention variant for...     │ HIGH       │
│ 2 方法论             │ Trained on 8×A100, 300 epochs...   │ HIGH       │
│ 3 数学分析           │ Theorem 1 proof assumes...         │ MEDIUM     │
│ 4 结果数据           │ +2.3% on GLUE, +1.7% on SuperGLUE │ HIGH       │
│ 5 文献脉络           │ Builds on Vaswani 2017, differs..  │ HIGH       │
│ 6 批判评估           │ Ablation missing for key component │ MEDIUM     │
├──────────────────────┼─────────────────────────────────────┼────────────┤
│ 跨Agent矛盾          │ 2处                                 │            │
│ 信息缺口              │ 1处 (code not released)            │            │
└──────────────────────┴─────────────────────────────────────┴────────────┘

⚠ Agent 3 flagged potential error in proof (see analysis/03-mathematical-analysis.md)
⚠ Agent 2 and 4 disagree on whether baseline is fairly tuned (see details)
```

**User action required**:
- Review the summary and flag any dimension that needs deeper analysis
- Confirm whether to proceed to Phase 2, or re-run specific agents with additional focus
- If gaps are acceptable (e.g., code not released is a known fact), proceed

**If user is unsatisfied** with a dimension: re-launch that specific agent with refined instructions, then return to Phase 1.5.

---

### Phase 2: Structured 20-Point Note Generation

Based on the multi-agent analysis files (all in `analysis/`), generate the complete 20-point reading note. This phase synthesizes the parallel analyses into a unified, coherent document.

**Write to**: `[output-dir]/reading-note.md`

ALWAYS follow this exact structure:

#### 1. Note YAML Metadata
At the very top of the file, include YAML front matter:
```yaml
---
title: "Paper Title"
authors: "[Authors]"
year: 2026
journal: "Journal Name, Volume(Issue), Pages"
doi: "DOI number"
tags: [keyword1, keyword2, paper-notes]
source_language: english
status: reading
created: 2026-04-28
analysis_agents: [agent1, agent2, ...]  # Which agents contributed
---
```

#### 2. 论文基本信息 (Bibliographic Information)
- 作者 (Authors)、发表年份 (Year)、论文标题 (Title)
- 期刊/会议名称 (Journal/Conference)、卷号 (Volume)、期号 (Issue)、起止页码 (Pages)
- DOI号
- 通讯作者及所属机构
- **来源**: Agent 1 (core metadata) + Phase 0 extraction

#### 3. 核心科学问题 (Core Scientific Problem)
清晰阐述本研究旨在解决的核心科学问题或技术瓶颈。说明该问题为何重要、现有方法为何不足。
- **来源**: Agent 1 (core argument)

#### 4. 研究假设 (Research Hypothesis)
明确列出作者提出的核心研究假设或理论构想。
- **来源**: Agent 1 (hypothesis extraction)

#### 5. 研究设计 (Research Design)
概述整体研究思路：理论推导、仿真模拟、实验验证、临床试验、病例对照研究、队列研究、荟萃分析、案例研究等。说明研究类型和整体架构。
- **来源**: Agent 1 (overall design) + Agent 2 (experimental structure)

#### 6. 数据/样本来源 (Data/Sample Sources)
说明数据获取方式（公共数据库、自有采集、文献数据提取等）、样本规模、纳入/排除标准、样本基本特征。对于临床研究，注明伦理审批信息。
- **来源**: Agent 2 (datasets, sources)

#### 7. 方法与技术 (Methods & Techniques)
详述所使用的关键技术、算法、模型架构、实验平台、试剂材料、仪器设备或软件工具。对于计算方法，说明编程语言和关键参数；对于实验方法，说明实验条件和操作步骤。
- **来源**: Agent 2 (methods detail) + Agent 3 (formal methods) + Agent 8 (code, if available)

#### 8. 分析流程 (Analysis Workflow)
分步说明实验步骤、仿真流程或理论推导的关键环节。使用有序列表清晰呈现，让读者能够复现研究过程。
- **来源**: Agent 2 (workflow decomposition)

#### 9. 数据分析 (Data Analysis)
说明所采用的统计方法（如t检验、方差分析、生存分析、回归模型等）、多重比较校正方法、有效性验证手段、性能评价指标（如AUC、敏感度、特异度、F1-score、p值阈值等）。
- **来源**: Agent 4 (metrics, statistical methods)

#### 10. 核心发现 (Core Findings)
提炼研究中最重要、最创新的科学发现或观测现象。这是论文的核心贡献所在。
- **来源**: Agent 1 (contributions) + Agent 4 (key results)

#### 11. 实验结果 (Experimental Results)
总结关键的定量结果（性能指标、效应量、统计显著性p值、置信区间等）和定性结论。用表格呈现关键对比数据以便快速查阅。
- **来源**: Agent 4 (results with tables)

#### 12. 辅助结果 (Secondary Results)
简述其他支持性、补充性的次要结果（如亚组分析、敏感性分析、补充实验、消融实验等）。
- **来源**: Agent 4 (ablation, secondary)

#### 13. 作者结论 (Author Conclusions)
归纳作者基于证据得出的最终结论。区分哪些结论有充分数据支持，哪些属于推断或推测。
- **来源**: Agent 1 (author claims) + Agent 6 (overclaim detection)

#### 14. 研究贡献 (Contributions)
评价本研究在理论创新、技术突破、方法改进或应用拓展方面对相关领域的具体贡献。
- **来源**: Agent 1 (claimed contributions) + Agent 5 (positioning in field)

#### 15. 与我的研究关联 (Relevance to My Research)
分析该工作与读者研究方向的核心关联点（方法可迁移性、数据集可利用性、结论可引用性等）。
- **来源**: Agent 5 (connection points) + user's research context

#### 16. 综述讨论要点 (Key Discussion Points for Review)
指出值得在综述中重点讨论的亮点：开创性贡献、与其他工作的争议点、方法学局限性、对未来研究的启示。
- **来源**: Agent 5 (literature positioning) + Agent 6 (critical discussion points)

#### 17. 图表索引 (Figures & Tables Index)
列出文中所有Figure和Table的编号、标题及其所展示的核心内容概述：
```
**Table 1**: [标题] — [核心内容概述]
**Figure 1**: [标题] — [核心内容概述]
...
```
- **来源**: Agent 7 (if image mode enabled), otherwise extracted from paper text
> If image processing was confirmed, embed figure links `![[Fig.x description]]` with interpretation alongside the index entries. Otherwise, omit image analysis.

#### 18. 个人评价 (Personal Evaluation)
对该研究的方法严谨性、逻辑完备性和结论可靠性的个人评价。指出方法学上的优势和不足。
- **来源**: Agent 6 (critical assessment synthesis)

#### 19. 疑问与不足 (Questions & Limitations)
阅读中产生的疑问，或认为该研究存在的不足之处（样本量限制、方法学缺陷、结论过度推广、潜在偏倚等）。
- **来源**: Agent 6 (limitations) + cross-agent contradictions from Phase 1.5

#### 20. 启发与展望 (Inspirations & Future Directions)
该研究带来的新思路、新想法或未来可探索的方向。可从方法改进、应用拓展、跨领域迁移等角度思考。
- **来源**: Agent 6 (future directions) + synthesis of agent insights

#### 21. 关键参考文献 (Key References)
列出文中引用的2-3篇最具代表性的参考文献，格式：作者，年份，标题，期刊，卷(期)，页码。方便追溯重要学术渊源。
- **来源**: Agent 5 (citation analysis)

#### 22. 概念关系图谱 (Concept Map)
列出论文中的关键学术概念作为 Obsidian 双向链接，例如 `[[Tumor Microenvironment]]`、`[[Immune Checkpoint]]`、`[[Survival Analysis]]`，并附简短说明其在本研究中的角色。
- **来源**: All agents (concept extraction)

---

### Phase 2.5: Completeness & Quality Check

Before entering final verification, verify the generated note covers all 22 sections. Run:

```bash
python reading_note_quality.py [output-dir]/reading-note.md
```

The tool checks:
- [ ] All 22 sections present and non-empty
- [ ] All formulas in MathJax syntax (not code blocks)
- [ ] YAML frontmatter valid
- [ ] Figure links only present if image mode was enabled
- [ ] Source language handling correct (translation present if foreign; absent if Chinese)
- [ ] Bidirectional links (Wikilinks) format correct

Fix any flagged issues before proceeding to Phase 3.

---

### Phase 3: Dual-Agent Quality Verification

**Launch two quality-assurance agents in parallel** to independently review the reading note. This pattern is directly adapted from nuwa-skill's Phase 5 dual-agent refinement.

#### Agent A: Mathematical & Logical Correctness

Spawn a subagent to verify:
- All formulas correctly transcribed from the paper
- Derivations are logically sound (no missing steps)
- Symbol definitions are consistent throughout the note
- Statistical claims are correctly interpreted (p-values, confidence intervals, effect sizes)
- No hallucinated formulas or results
- Flag any `[INFERRED]` claims that should be downgraded to `[UNCERTAIN]`

**Output**: List of issues found, each with a suggested fix. Write to `[output-dir]/analysis/qa-math.md`.

#### Agent B: Completeness & Readability

Spawn a subagent to verify:
- All 22 sections have substantive content (not just placeholders)
- The note tells a coherent story — a reader unfamiliar with the paper should understand it
- Cross-references between sections are consistent (e.g., Section 10's findings match Section 11's results)
- Contradictions identified in Phase 1.5 are properly addressed in Sections 18-19
- Chinese translation quality (if applicable) — no awkward machine-translation artifacts
- No information from Agent 7 (figures) appears if user declined image mode
- Reading flow: can a domain researcher skim this in 5 minutes and grasp the paper?

**Output**: List of issues with suggested fixes. Write to `[output-dir]/analysis/qa-readability.md`.

#### Apply Fixes

The main agent reads both QA reports, applies all non-conflicting fixes to `reading-note.md`, and presents a change summary:

```
QA Results:
- Agent A (Math): 2 issues fixed (typo in Eq.3, missing normalization constant)
- Agent B (Readability): 3 issues fixed (added transition in §7, expanded §15,
  removed orphaned figure reference)
- 0 unresolved conflicts
```

If the two QA agents disagree on a point, present both views and let the user decide.

---

## Constraints

- **Language**: Default all output to Chinese. Do not interleave unnecessary English words in explanations.
- **Academic Rigor**: Zero hallucinations. All interpretations must be grounded in the paper text. When supplementing background knowledge, clearly state the source or nature of the supplement.
- **Format Rules**:
  - Source text and translations MUST use `>` blockquote format.
  - Formulas strictly in MathJax syntax: inline `$...$`, display `$$...$$`. **Never write math formulas inside code blocks.**
  - Figure links only in `![[Fig.x name]]` format, and only when the user has authorized image processing.
- **Focus**: Concentrate on the technical details described in the paper (What & Why), not on the author's writing manner.
- **Translation Scope**: Translation is a tool for comprehension, not the primary deliverable. The core value is expert explanation and knowledge deconstruction. Skip translation entirely when the source is already in Chinese.
- **Parallelism**: In Mode B Phase 1, agents MUST be launched in parallel (not sequentially). Sequential agent execution defeats the purpose of deepening analysis — the value comes from independent perspectives synthesized together.
- **Contradictions are features, not bugs**: When two agents disagree, preserve the tension. It often reveals the most interesting aspects of a paper (e.g., strong claims with weak evidence, methods that don't match the problem).

---

## Scripts

The following Python tools assist automation. Copy them from the skill directory into the output directory when setting up Phase 0.5.

### `paper_analyze.py`
Scans all agent analysis files and generates the Phase 1.5 checkpoint summary table. Automatically detects contradictions, information gaps, and confidence levels across agents.

Usage: `python paper_analyze.py [output-dir]`

### `reading_note_quality.py`
Validates the generated reading note against completeness and format rules for Phase 2.5.

Usage: `python reading_note_quality.py [path/to/reading-note.md]`

---

## Quality Gates Summary

| Gate | Phase | What It Prevents | Cost of Skipping |
|------|-------|-----------------|------------------|
| Mode/Preferences Confirmation | 0 | Wrong mode, wrong language handling | Wasted entire session |
| Agent Dispatch Plan | 0.5 | Wrong agents for paper type | Thin analysis on key dimensions |
| Cross-Agent Synthesis | 1.5 | Contradictions buried, gaps unnoticed | Flawed foundation for entire note |
| Completeness Check | 2.5 | Missing sections, malformed output | Unusable reading note |
| Dual-Agent QA | 3 | Math errors, incoherent narrative | Embarrassing errors in deliverable |

**Investment principle**: Each hour spent on quality gates saves 5+ hours of rework or correction later. Never skip a gate without explicit user instruction.

---

## Taste Principles (Quick Reference)

| Principle | Meaning |
|-----------|---------|
| Depth > Width | 6 focused analyses beat 1 shallow summary |
| Contradictions > Consensus | Where agents disagree is where the paper is most interesting |
| Gap honesty > Fabricated completeness | Marking `[INSUFFICIENT DATA]` is better than inventing analysis |
| Fresh research > Stale training data | Agentic Q&A with WebSearch beats trusting cutoff knowledge |
| Structure > Prose | Obsidian-ready formatting with YAML, Wikilinks, and MathJax enables knowledge accumulation |

### NEVER
- Skip an agent just because its dimension seems thin — thin output is itself informative
- Harmonize away cross-agent contradictions — they are the most valuable content
- Generate analysis without reading the paper — every claim must be traceable to the text
- Write math formulas inside code blocks
- Reference figures without user permission
- Deliver a reading note without running Phase 2.5 quality check
