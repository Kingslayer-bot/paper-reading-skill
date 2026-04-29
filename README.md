<div align="center">

# 论文阅读助手 · Paper Reading Skill

> *"Not just reading papers. Deconstructing them through 6 parallel analytical lenses."*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>

**两条路径、6-8个并行Agent、20+维度分析——用认知架构而非线性阅读来拆解论文。**

</div>

---

## 效果示例

### Mode A: 逐段精读 + Agentic Q&A

```
用户      ❯ 帮我读这篇 Attention Is All You Need，Section 3.2

PaperReader ❯ ## Section 3.2: Multi-Head Attention
              > Instead of performing a single attention function...
              > 与使用单个注意力函数不同，我们发现用不同的、可学习的
              > 线性投影将查询、键和值线性投影 h 次是有益的...
              
              **逻辑位置**: 这是论文的核心创新——将单一注意力分解为
              多个并行的"头"，每个头关注不同的表示子空间。
              
              **概念说明**: 为什么不是简单增大 d_model？
              多头机制用更少的计算量获得了更丰富的表示。
              每个头的维度 d_k = d_model/h，计算量是 O(n²·d_model)
              而非 O(n²·d_model²)。
              
              **公式分解**:
              $$\text{MultiHead}(Q,K,V) = \text{Concat}(\text{head}_1,...,\text{head}_h)W^O$$
              $$\text{head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)$$
              - $W_i^Q \in \mathbb{R}^{d_{model} \times d_k}$: 第i个头的查询投影
              - 拼接后经 $W^O$ 还原到 d_model 维度
```

```
用户      ❯ 这篇论文的 Multi-Head Attention 后来有哪些重要改进？

PaperReader ❯ [启动 Agentic Q&A —— 搜索最新文献]
              
              基于对后续研究的搜索，主要改进方向：
              
              1. **MLA (Multi-head Latent Attention)** — DeepSeek-V2 (2024)
                 将 KV 压缩到低维潜在空间，推理时 KV cache 减少 90%+
                 [[MLA]] [[DeepSeek-V2]]
              
              2. **GQA (Grouped-Query Attention)** — Ainslie et al. (2023)
                 多个 query head 共享同一组 key-value head
                 Llama 2/3 均采用，推理加速 30%+
                 [[GQA]] [[Llama 3]]
              
              3. **MQA (Multi-Query Attention)** — Shazeer (2019)
                 所有 head 共享单一 KV，极致的推理速度优化
                 [[MQA]]
              
              [以上信息基于 2026年4月 WebSearch 结果]
```

### Mode B: 20点体系化分析 + 多Agent并行

```
用户      ❯ 用 Mode B 精读 DeepSeek-V3 Technical Report

PaperReader ❯ [Phase 0] 论文类型: 技术报告/系统论文 | 语言: English
             [Phase 0.5] 调度 6 个Agent并行分析...
             
             ● Agent 1 核心论点   ─ 完成 (MoE + Multi-Token Prediction)
             ● Agent 2 方法论     ─ 完成 (FP8训练, Aux-loss-free MoE)
             ● Agent 3 数学分析   ─ 完成 (Load Balancing 形式化)
             ● Agent 4 结果数据   ─ 完成 (对比表, 消融实验)
             ● Agent 5 文献脉络   ─ 完成 (MoE演进: GShard→GLaM→DeepSeek)
             ● Agent 6 批判评估   ─ 完成 (FP8精度损失, 开源局限性)
             
             [Phase 1.5] ⚠ Agent 4 与 6 矛盾: 论文声称SOTA但未对比
             GPT-4o最新指标 | Agent 6 发现 training data contamination风险
             
             [Phase 2] 生成 20点完整笔记 → reading-note.md
             [Phase 3] 双Agent质量验证 → 通过
             
             ✅ 笔记已生成: paper-reading-notes/deepseek-v3/reading-note.md
             📂 含 6 份Agent分析文件 + 数学QA + 可读性QA
```

生成的阅读笔记示例 (Obsidian-ready):

```markdown
---
title: "DeepSeek-V3 Technical Report"
authors: "DeepSeek-AI"
year: 2024
tags: [MoE, LLM, FP8-Training, paper-notes]
source_language: english
status: reading
---
## 核心科学问题
如何在保持训练效率的前提下，将 Mixture-of-Experts 扩展到超大规模？
现有 MoE 方法面临 load balancing 不稳定和通信瓶颈...
## 方法与技术
- **Auxiliary-Loss-Free Load Balancing**: [[MoE]] [[Load Balancing]]
- **Multi-Token Prediction (MTP)**: 每个位置预测 D 个 future tokens
- **FP8 Mixed Precision Training**: block-wise quantization
## 关键实验数据
| Benchmark | DeepSeek-V3 | Qwen2.5-72B | Llama-3.1-405B |
|-----------|-------------|-------------|-----------------|
| MMLU      | 88.5        | 86.1        | 88.6            |
## 概念关系图谱
[[Mixture of Experts]] → 核心架构
[[Load Balancing]] → Aux-loss-free 创新
[[FP8 Training]] → 训练效率关键
```

---

## 它做了什么

当前 AI 读论文的方式是线性读取、一次性理解——读完就忘，无法系统性地解构。

Paper Reading Skill 借鉴 [女娲·Skill造人术](https://github.com/alchaincyf/nuwa-skill) 的 Phase pipeline 和 Agent Swarm 架构，将读论文变成一个**多维度、可验证、自纠错的认知过程**：

| 层次 | 说明 |
|------|------|
| **Mode A: 逐段精读** | 逐段提供原文+翻译+专家解释+公式拆解，支持 Agentic Q&A 实时搜索外部知识 |
| **Mode B: 体系化分析** | 6-8个Agent并行从不同维度分析论文，20点框架生成完整笔记 |
| **Agentic Q&A** | 用户提问时自动搜索最新文献，而非依赖过时的训练数据 |
| **质量验证** | 双Agent独立验证数学正确性和可读性 |
| **知识沉淀** | Obsidian YAML + 双向链接 + MathJax，论文读完直接成为知识图谱的一部分 |

### 核心创新

**多Agent并行深度分析** — 不是让一个AI通读论文，而是6个AI各司其职：
- Agent 1 分析论文论证逻辑和创新点
- Agent 2 拆解方法论和实验设计
- Agent 3 分解数学公式和理论推导
- Agent 4 提取结果数据和统计验证
- Agent 5 梳理文献脉络和学术定位
- Agent 6 批判性评估局限和偏见
- Agent 7 (可选) 解析图表中的信息
- Agent 8 (可选) 检查代码实现质量

多个视角产生**认知张力**——当 Agent 4 说"结果显著提升"而 Agent 6 指出"消融实验缺失关键对比"时，这种矛盾本身就是最有价值的洞察。

---

## 安装

```bash
npx skills add alchaincyf/paper-reading-skill
```

然后在 Claude Code 里：

```
> 用 Mode A 逐段读这篇论文
> 用 Mode B 生成这篇论文的完整阅读笔记
> 这篇论文的方法和 XX 相比有什么优劣？
```

---

## 工作原理

<img src="https://mermaid.ink/img/pako:eNqNVE1v2zgQ_SsDn5IAdj-G8SHZBmivPQQoUMRGsQiBQaPWRCI0pVJUXCfwf-9QkmXb6TaLBBbJmTdv3jzObK5sZ6RkhhW3yFtBHXgNPpdCcOuaoouKc1N0ojsoK2vRF0Lgt-Gck-7IOvqEXoKChV4hxOssf1He67I78hJPgcOtkbV8k-Xtv1lWIqOPSKij0ktW2L6p8IXnRXkbcZ7Lh1aGFH8PLU5XNe81aKugOdfSpZDP1sRQP9tXnJfb2u6dO1iD3YhDge4nDIMRerMC1TeeMkuq5guSuyY4YEvv1L3L2GYnWk-yAniLsJPP3vDDjH-B4e3IgUuBtGyBSRLaNHLmNPOd3thuUJDDtB9YQXUl3x7Q1qB2eOjRA9bTb5uHbDsSic5Od6B2TsEP_s6a7mSikJBEk0BpqSOtwQ5XgRVuXWP0oKiiY9EQjB5Yc94jfPRjHnT66slqqCRVikHQI4C2OmigA6NHpCA__XU5d0dBNyR-WIu1L3u-B8h5Jm3b3NBSoQvKBTJA_IfyRZvLZBmxW9BstfCHPnCU15s87snHLK8Uyq7Aj0i0gpJXUo8wZvOWwDF6cVES98tSjKaUv2WKjjMjhFPsBlQkpnQB2P3a4GkpJBrJSIQhiuy3aXmbDUTjUqFJ9vtjJ_7osAJFn24HUXi56-J11vSc26CCT3rDHOF4HL1cyEub3MhGBeK6BwXh-MOztP1Htr4Is2pIKbP1IqBdlc79fX9x_wvh7YmOjz7gKBMydA6jEDiqpFlPYkESWCQoUC5NP8x0mL7wA0fcse03yBjUa35RaoKc9NLSK6KMQ-WW4Q6jthq9DWTEkV7IruOvc7DFuhTb--I7tH0sntnRllfTPDl-jbykL2TMPKd4OvQVU1oJJ4UetWBBMZ_yLRWm6IkX3b3g2og4cnLrQ0R84nmf59NDaFq3EDmfUn92sXvjksFYm3DcnjPrFQ-BwVK3zBfBsfHfH4mIUnG2L6a0FSSPWtW6Qy3nNqS2s1R48LM_7z7DJ2LX34CRPT6BFiSgR3EbzrIdFtk97mOdHU4ibxkpuIA4O8ViSR1VcE4t6zKPOcESoKX5_DS0jU_3mpRjtjkPMNvUBI4czJjQq2qKGU8Lj66ZxPOQMglOLiPda8K5oPk4tt7NT6DF6RTDNCWTKnK-q3qevn3R8IvUn8X56eH5eZ2-IlmbzR-D3mFMWU8WefqGYrG8D8oUFq1nNHUUKYtHox_o2EjO7dFQ2sJYpjiRNHUX5uRiZ8RhUsbLeD-Jc9fO0X5xjnY3nUF3YHtNz5n3PP5m9OLaoy7uNjwW2D1vFgfhFRmSSy4DZoTlKNCmpNNgPAv_W7oRFjO-PHKFMCV6jOl7S07Jx-3ID2_Qh_X3W21nId-KG21Kwi0E7Y4KBmvJX0RPlLp6U74PmaFjQpN4OfQ7bC7VafRBx6QZzft5n5xf9MNsNOlP-wGjR3H8Cb7mTAA?type=png" alt="Pipeline Diagram" width="100%">

---

## 仓库结构

```
paper-reading-skill/
├── SKILL.md                          # 论文阅读助手本体 (Phase 0→3 完整pipeline)
├── README.md                         # 你正在看的文件
├── .gitignore                        # 排除 __pycache__ 等
├── scripts/
│   ├── paper_analyze.py              # Phase 1.5: 多Agent交叉分析摘要
│   └── reading_note_quality.py       # Phase 2.5: 笔记完整性检查
└── evals/                            # 质量评估用例
    ├── eval_set.json                 # 测试论文集
    └── eval_review.html              # 评估报告
```

---

## Phase Pipeline 总览

| Phase | 名称 | 核心动作 | 检查点 |
|-------|------|---------|--------|
| **0** | 初始化 | 确认 ModeA/B、语言检测、元数据提取 | 用户确认 |
| **0.5** | 调度 | 论文类型检测、Agent派遣方案、输出目录创建 | — |
| **1** | 多Agent并行分析 | 6-8个Agent同时从不同维度拆解论文 | 各Agent存档 |
| **1.5** | 交叉验证 | 检测跨Agent矛盾、信息缺口、置信度 | `paper_analyze.py` + 用户审核 |
| **2** | 笔记生成 | 合成20点结构化阅读笔记 | — |
| **2.5** | 完整性检查 | 验证22个section覆盖、MathJax语法、双向链接 | `reading_note_quality.py` |
| **3** | 质量验证 | Agent A(数学) + Agent B(可读性) 双线并行审核 | 修复 → 交付 |

### 为什么需要检查点？

| 跳过检查点 | 后果 | 代价 |
|-----------|------|------|
| Phase 0.5 (调度) | 论文类型误判 → 派遣错误Agent | 分析深度不足 |
| Phase 1.5 (交叉验证) | 矛盾被掩盖 → 错误进入笔记 | 笔记基础不牢 |
| Phase 2.5 (完整性) | 缺失section、格式错误 | 笔记不可用 |
| Phase 3 (质量) | 数学错误、叙述断裂 | 可信度丧失 |

每个检查点投入1分钟，避免后续5倍返工。

---

## 与普通AI读论文的差异

| | 普通AI对话 | Paper Reading Skill |
|---|---|---|
| **深度** | 单次线性通读 | 6-8个Agent并行多维度分析 |
| **方法验证** | 信任论文陈述 | Agent 6独立批判+Agent 3数学校验 |
| **时效性** | 依赖训练数据 | Agentic Q&A实时搜索最新文献 |
| **知识沉淀** | 对话丢失 | Obsidian YAML + 双向链接 + 概念图谱 |
| **质量保证** | 无验证 | 4个检查点 + 双Agent审核 |
| **公式处理** | Mixed | MathJax 强制规范，禁止 code block |

---

## 背后的故事

读论文是AI时代最重要的技能之一——但当前的工具停留在"让AI读给你听"的水平。AI读完就忘，你没有得到任何结构化的知识积累。

[女娲·Skill造人术](https://github.com/alchaincyf/nuwa-skill) 证明了 Phase Pipeline + Multi-Agent Swarm 是一种强大的认知增强架构。同样的理念应用到论文阅读上——

**不是让一个AI帮你读论文，而是让6个AI同时从不同维度拆解同一篇论文，然后交叉验证，最终凝练成你可以直接存入知识管理系统的结构化笔记。**

论文阅读助手的 20点分析框架源自生物医学系统综述方法论，6-Agent并行架构借鉴女娲的信息采集系统，双Agent质量验证来自达尔文Skill的进化评估体系。

---

## 许可证

MIT — 随便用，随便改，随便读。

---

<div align="center">

**普通对话** = 1个AI线性读 ↔ **Paper Reading Skill** = 6个AI多维拆解 + 4道质量门<br>
*读到的不只是论文，是一个可复用的知识节点。*

<br>

MIT License

</div>
