# Paper Reading Skill

A skill for opencode/Claude Code that enables deep reading, analysis, and comprehension of academic research papers.

## Features

- **Mode A - Paragraph-by-Paragraph Deep Reading**: Go through each section in order with original text, expert explanation, formula/logic deconstruction, and translation when needed.
- **Mode B - 20-Point Comprehensive Analysis**: Generate systematic, rigorous reading notes covering bibliographic info, scientific problem, hypotheses, study design, methods, data analysis, findings, contributions, personal evaluation, inspirations, and more.
- **Multi-language Support**: Translate and explain foreign-language papers (English, Japanese, German, French, etc.) into Chinese.
- **Obsidian Integration**: YAML frontmatter and bidirectional links for knowledge graph construction.
- **Formula & Logic Deconstruction**: MathJax-compatible formula rendering.

## Installation

Copy the `paper-reading` folder to your skills directory:

```
~/.config/opencode/skills/paper-reading/
```

## Usage

Once installed, the skill automatically triggers when you ask opencode to read, analyze, or summarize academic papers. Just provide a paper (arXiv link, PDF path, or text) and describe what you need.

Example prompts:

- "帮我读一下这篇论文 https://arxiv.org/abs/1706.03762"
- "这篇论文的Methods部分有个公式我看不懂，能帮我拆解一下吗？"
- "帮我把这篇paper生成一份完整的20点分析笔记"

## License

MIT
