<div align="center">

# Paper Reading Skill

> *"Not just reading papers. Deconstructing them through 6 parallel analytical lenses."*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

**Other Languages:**
[中文](README.md) · English

<br>

**Two modes, 6-8 parallel agents, 20+ dimensions of analysis — deconstructing papers through cognitive architecture, not linear reading.**

</div>

---

## Examples

### Mode A: Paragraph-by-Paragraph Deep Reading + Agentic Q&A

```
User      ❯ Read Section 3.2 of Attention Is All You Need for me

PaperReader ❯ ## Section 3.2: Multi-Head Attention
              > Instead of performing a single attention function, we found
              > it beneficial to linearly project the queries, keys and
              > values h times with different, learned linear projections...
              
              **Position**: This is the paper's core innovation —
              decomposing a single attention into multiple parallel "heads",
              each attending to different representation subspaces.
              
              **Why not just increase d_model?** Multi-head achieves richer
              representations with less computation. Head dimension
              d_k = d_model/h, with O(n²·d_model) not O(n²·d_model²).
              
              **Formula Breakdown**:
              $$\text{MultiHead}(Q,K,V) = \text{Concat}(\text{head}_1,...,\text{head}_h)W^O$$
              $$\text{head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)$$
              - $W_i^Q \in \mathbb{R}^{d_{model} \times d_k}$: query projection for head i
```

```
User      ❯ What are the most important improvements to Multi-Head Attention?

PaperReader ❯ [Agentic Q&A — searching latest literature]
              
              Based on recent research, three key directions:
              
              1. **MLA (Multi-head Latent Attention)** — DeepSeek-V2 (2024)
                  Compresses KV into a low-dim latent space, reducing
                  KV cache by 90%+ at inference. [[MLA]] [[DeepSeek-V2]]
              
              2. **GQA (Grouped-Query Attention)** — Ainslie et al. (2023)
                  Multiple query heads share the same KV heads.
                  Llama 2/3 both use this, achieving 30%+ inference speedup.
                  [[GQA]] [[Llama 3]]
              
              3. **MQA (Multi-Query Attention)** — Shazeer (2019)
                  All heads share a single KV — extreme inference speedup.
                  [[MQA]]
```

### Mode B: 20-Point Systematic Analysis + Multi-Agent Parallel

```
User      ❯ Use Mode B to deep-read the DeepSeek-V3 Technical Report

PaperReader ❯ [Phase 0] Type: Tech Report / Systems | Language: English
             [Phase 0.5] Dispatching 6 parallel agents...
             
             ● Agent 1 Core Argument ─ Done (MoE + Multi-Token Prediction)
             ● Agent 2 Methodology   ─ Done (FP8 training, Aux-loss-free MoE)
             ● Agent 3 Math Analysis ─ Done (Load Balancing formalization)
             ● Agent 4 Results       ─ Done (comparison tables, ablation)
             ● Agent 5 Literature    ─ Done (MoE evolution: GShard→GLaM→DeepSeek)
             ● Agent 6 Critique      ─ Done (FP8 precision loss, OSS limits)
             
             [Phase 1.5] ⚠ Agent 4 & 6 disagree: claims SOTA but missing
             latest GPT-4o comparison | Agent 6 flags data contamination risk
             
             [Phase 2] Generated complete 20-point note → reading-note.md
             [Phase 3] Dual-Agent QA → PASS
             
             ✅ Output: paper-reading-notes/deepseek-v3/reading-note.md
             📂 Includes: 6 agent analysis files + math QA + readability QA
```

Sample output (Obsidian-ready):

```markdown
---
title: "DeepSeek-V3 Technical Report"
authors: "DeepSeek-AI"
year: 2024
tags: [MoE, LLM, FP8-Training, paper-notes]
source_language: english
status: reading
---
## Core Scientific Problem
How can Mixture-of-Experts be scaled to extreme sizes while maintaining
training efficiency? Previous MoE approaches suffer from load balancing
instability and communication bottlenecks...
## Methods & Techniques
- **Auxiliary-Loss-Free Load Balancing**: [[MoE]] [[Load Balancing]]
- **Multi-Token Prediction (MTP)**: predicts D future tokens per position
- **FP8 Mixed Precision Training**: block-wise quantization
## Key Results
| Benchmark | DeepSeek-V3 | Qwen2.5-72B | Llama-3.1-405B |
|-----------|-------------|-------------|-----------------|
| MMLU      | 88.5        | 86.1        | 88.6            |
## Concept Map
[[Mixture of Experts]] → core architecture
[[Load Balancing]] → Aux-loss-free innovation
[[FP8 Training]] → key to training efficiency
```

---

## What It Does

Current AI paper reading is linear, one-pass comprehension — read and forget, no structured knowledge accumulation.

Paper Reading Skill borrows [Nuwa·Skill Creator](https://github.com/alchaincyf/nuwa-skill)'s Phase pipeline and Agent Swarm architecture, transforming paper reading into a **multi-dimensional, verifiable, self-correcting cognitive process**:

| Layer | Description |
|-------|-------------|
| **Mode A: Deep Reading** | Paragraph-by-paragraph: original text + translation + expert explanation + formula decomposition, with Agentic Q&A for real-time literature search |
| **Mode B: Systematic Analysis** | 6-8 agents analyze the paper in parallel from different dimensions, generating a complete 20-point structured note |
| **Agentic Q&A** | When you ask a question, it searches latest literature rather than relying on stale training data |
| **Quality Verification** | Two independent agents verify mathematical correctness and readability |
| **Knowledge Accumulation** | Obsidian YAML + bidirectional links + MathJax — your paper reading feeds directly into your knowledge graph |

### Core Innovation

**Multi-Agent Parallel Deep Analysis** — not one AI reading the paper, but 6 AI agents each owning a dimension:
- Agent 1: Argumentation logic and contributions
- Agent 2: Methodology and experimental design
- Agent 3: Mathematical decomposition
- Agent 4: Results data and statistical validation
- Agent 5: Literature context and scholarly positioning
- Agent 6: Critical assessment of limitations and biases
- Agent 7 (optional): Figure and table interpretation
- Agent 8 (optional): Code implementation quality

Multiple perspectives generate **cognitive tension** — when Agent 4 says "significant improvement" and Agent 6 says "ablation missing key comparison," that contradiction itself is the most valuable insight.

---

## Installation

```bash
npx skills add Kingslayer-bot/paper-reading-skill
```

Then in Claude Code:

```
> Read this paper paragraph-by-paragraph in Mode A
> Generate a complete reading note in Mode B
> How does this method compare to XX?
```

---

## How It Works

<img src="https://mermaid.ink/img/pako:eNqNVE1v2zgQ_SsDn5IAdj-G8SHZBmivPQQoUMRGsQiBQaPWRCI0pVJUXCfwf-9QkmXb6TaLBBbJmTdv3jzObK5sZ6RkhhW3yFtBHXgNPpdCcOuaoouKc1N0ojsoK2vRF0Lgt-Gck-7IOvqEXoKChV4hxOssf1He67I78hJPgcOtkbV8k-Xtv1lWIqOPSKij0ktW2L6p8IXnRXkbcZ7Lh1aGFH8PLU5XNe81aKugOdfSpZDP1sRQP9tXnJfb2u6dO1iD3YhDge4nDIMRerMC1TeeMkuq5guSuyY4YEvv1L3L2GYnWk-yAniLsJPP3vDDjH-B4e3IgUuBtGyBSRLaNHLmNPOd3thuUJDDtB9YQXUl3x7Q1qB2eOjRA9bTb5uHbDsSic5Od6B2TsEP_s6a7mSikJBEk0BpqSOtwQ5XgRVuXWP0oKiiY9EQjB5Yc94jfPRjHnT66slqqCRVikHQI4C2OmigA6NHpCA__XU5d0dBNyR-WIu1L3u-B8h5Jm3b3NBSoQvKBTJA_IfyRZvLZBmxW9BstfCHPnCU15s87snHLK8Uyq7Aj0i0gpJXUo8wZvOWwDF6cVES98tSjKaUv2WKjjMjhFPsBlQkpnQB2P3a4GkpJBrJSIQhiuy3aXmbDUTjUqFJ9vtjJ_7osAJFn24HUXi56-J11vSc26CCT3rDHOF4HL1cyEub3MhGBeK6BwXh-MOztP1Htr4Is2pIKbP1IqBdlc79fX9x_wvh7YmOjz7gKBMydA6jEDiqpFlPYkESWCQoUC5NP8x0mL7wA0fcse03yBjUa35RaoKc9NLSK6KMQ-WW4Q6jthq9DWTEkV7IruOvc7DFuhTb--I7tH0sntnRllfTPDl-jbykL2TMPKd4OvQVU1oJJ4UetWBBMZ_yLRWm6IkX3b3g2og4cnLrQ0R84nmf59NDaFq3EDmfUn92sXvjksFYm3DcnjPrFQ-BwVK3zBfBsfHfH4mIUnG2L6a0FSSPWtW6Qy3nNqS2s1R48LM_7z7DJ2LX34CRPT6BFiSgR3EbzrIdFtk97mOdHU4ibxkpuIA4O8ViSR1VcE4t6zKPOcESoKX5_DS0jU_3mpRjtjkPMNvUBI4czJjQq2qKGU8Lj66ZxPOQMglOLiPda8K5oPk4tt7NT6DF6RTDNCWTKnK+q3qevn3R8IvUn8X56eH5eZ2-IlmbzR-D3mFMWU8WefqGYrG8D8oUFq1nNHUUKYtHox_o2EjO7dFQ2sJYpjiRNHUX5uRiZ8RhUsbLeD-Jc9fO0X5xjnY3nUF3YHtNz5n3PP5m9OLaoy7uNjwW2D1vFgfhFRmSSy4DZoTlKNCmpNNgPAv_W7oRFjO-PHKFMCV6jOl7S07Jx-3ID2_Qh_X3W21nId-KG21Kwi0E7Y4KBmvJX0RPlLp6U74PmaFjQpN4OfQ7bC7VafRBx6QZzft5n5xf9MNsNOlP-wGjR3H8Cb7mTAA?type=png" alt="Pipeline Diagram" width="100%">

---

## Repository Structure

```
paper-reading-skill/
├── SKILL.md                          # Core skill (Phase 0→3 full pipeline)
├── README.md                         # Chinese README
├── README_EN.md                      # English README (this file)
├── .gitignore
├── scripts/
│   ├── paper_analyze.py              # Phase 1.5: cross-agent synthesis summary
│   └── reading_note_quality.py       # Phase 2.5: note completeness validator
└── evals/                            # Quality evaluation cases
    ├── eval_set.json
    └── eval_review.html
```

---

## Phase Pipeline Overview

| Phase | Name | Action | Gate |
|-------|------|--------|------|
| **0** | Initialize | Confirm Mode A/B, detect language, extract metadata | User confirm |
| **0.5** | Dispatch | Detect paper type, plan agent dispatch, create output dir | — |
| **1** | Multi-Agent Analysis | 6-8 agents analyze paper in parallel from different dimensions | Agent archives |
| **1.5** | Cross-Validation | Detect cross-agent contradictions, gaps, confidence | `paper_analyze.py` + user review |
| **2** | Note Generation | Synthesize 20-point structured reading note | — |
| **2.5** | Completeness Check | Verify 22 sections covered, MathJax syntax, wikilinks | `reading_note_quality.py` |
| **3** | Quality Verification | Agent A (math) + Agent B (readability) parallel audit | Fix → Deliver |

### Why Checkpoints?

| Skipping | Consequence | Cost |
|----------|-------------|------|
| Phase 0.5 (Dispatch) | Wrong paper type → wrong agents | Shallow analysis |
| Phase 1.5 (Cross-Validate) | Contradictions buried → errors in note | Faulty foundation |
| Phase 2.5 (Completeness) | Missing sections, format errors | Unusable note |
| Phase 3 (Quality) | Math errors, narrative gaps | Loss of credibility |

Each checkpoint costs 1 minute and saves 5× rework.

---

## vs. Plain AI Paper Reading

| | Plain AI Chat | Paper Reading Skill |
|---|---|---|
| **Depth** | Single-pass linear read | 6-8 agents parallel multi-dimension analysis |
| **Verification** | Trusts paper claims | Agent 6 independent critique + Agent 3 math check |
| **Timeliness** | Training data dependent | Agentic Q&A real-time literature search |
| **Knowledge** | Lost with conversation | Obsidian YAML + wikilinks + concept map |
| **Quality** | No verification | 4 checkpoints + dual-agent audit |
| **Formulas** | Mixed | MathJax enforced, code blocks banned |

---

## Background

Reading papers is one of the most critical skills in the AI era — but current tools stop at "have AI read it aloud for you." AI reads and forgets. You get zero structured knowledge accumulation.

[Nuwa·Skill Creator](https://github.com/alchaincyf/nuwa-skill) proved that Phase Pipeline + Multi-Agent Swarm is a powerful cognitive enhancement architecture. Apply the same philosophy to paper reading —

**Not one AI reading a paper for you, but 6 AIs simultaneously decomposing the same paper from different dimensions, cross-validating each other, and condensing it into a structured note you can directly feed into your knowledge management system.**

The 20-point analysis framework originates from biomedical systematic review methodology. The 6-Agent parallel architecture borrows from Nuwa's information collection system. Dual-Agent quality verification comes from Darwin Skill's evolutionary evaluation system.

---

## License

MIT 

---

<div align="center">

**Plain Chat** = 1 AI linear read ↔ **Paper Reading Skill** = 6 AI multi-dimension decomposition + 4 quality gates<br>
*You don't just read the paper. You build a reusable knowledge node.*

<br>

MIT License

</div>
