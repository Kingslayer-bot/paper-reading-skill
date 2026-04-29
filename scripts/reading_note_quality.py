#!/usr/bin/env python3
"""
Phase 2.5: Completeness & Quality Check for generated reading notes.
Validates that the 20-point analysis framework is fully populated,
formulas use correct MathJax syntax, and formatting rules are followed.

Usage:
    python reading_note_quality.py <path/to/reading-note.md>

Example:
    python reading_note_quality.py paper-reading-notes/my-paper/reading-note.md

Exit codes:
    0 — All checks passed
    1 — Warnings found (non-blocking)
    2 — Errors found (must fix before proceeding)
"""

import sys
import re
from pathlib import Path

# The 22 required sections (by section number and expected heading keywords)
REQUIRED_SECTIONS = [
    (1, "YAML", [r"^---\n", r"^title:"]),
    (2, "论文基本信息 / Bibliographic", [r"论文基本信息|Bibliographic"]),
    (3, "核心科学问题 / Core Scientific Problem", [r"核心科学问题|Core Scientific"]),
    (4, "研究假设 / Research Hypothesis", [r"研究假设|Research Hypothesis"]),
    (5, "研究设计 / Research Design", [r"研究设计|Research Design"]),
    (6, "数据/样本来源 / Data Sources", [r"数据.*来源|样本来源|Data.*Source"]),
    (7, "方法与技术 / Methods", [r"方法与技术|Methods.*Techniques"]),
    (8, "分析流程 / Analysis Workflow", [r"分析流程|Analysis Workflow"]),
    (9, "数据分析 / Data Analysis", [r"数据分析|Data Analysis"]),
    (10, "核心发现 / Core Findings", [r"核心发现|Core Findings"]),
    (11, "实验结果 / Experimental Results", [r"实验结果|Experimental Results"]),
    (12, "辅助结果 / Secondary Results", [r"辅助结果|Secondary Results"]),
    (13, "作者结论 / Author Conclusions", [r"作者结论|Author Conclusions"]),
    (14, "研究贡献 / Contributions", [r"研究贡献|Contributions"]),
    (15, "与我的研究关联 / Relevance", [r"研究关联|Relevance"]),
    (16, "综述讨论要点 / Key Discussion", [r"综述讨论|Discussion Points"]),
    (17, "图表索引 / Figures & Tables", [r"图表索引|Figures.*Tables|Table.*Index"]),
    (18, "个人评价 / Personal Evaluation", [r"个人评价|Personal Evaluation"]),
    (19, "疑问与不足 / Questions & Limitations", [r"疑问与不足|Questions.*Limitations"]),
    (20, "启发与展望 / Inspirations", [r"启发与展望|Inspirations.*Future"]),
    (21, "关键参考文献 / Key References", [r"关键参考|Key Reference"]),
    (22, "概念关系图谱 / Concept Map", [r"概念关系|Concept Map"]),
]


def check_yaml_frontmatter(content: str) -> list[str]:
    """Check YAML frontmatter exists and is valid."""
    issues = []
    if not content.startswith("---"):
        issues.append("Missing YAML frontmatter (should start with ---)")
        return issues

    # Find end of YAML
    end = content.find("\n---", 3)
    if end == -1:
        issues.append("YAML frontmatter not closed (missing closing ---)")
        return issues

    yaml_block = content[3:end].strip()
    required_fields = ["title", "authors", "year", "journal", "tags"]
    for field in required_fields:
        if f"{field}:" not in yaml_block:
            issues.append(f"YAML missing field: {field}")

    return issues


def check_section_coverage(content: str) -> list[str]:
    """Check all 22 sections are present with content."""
    issues = []

    for num, name, patterns in REQUIRED_SECTIONS:
        found = False
        for pattern in patterns:
            if re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                found = True
                break
        if not found:
            issues.append(f"Section {num} ({name}) NOT FOUND")

    return issues


def check_mathjax_syntax(content: str) -> list[str]:
    """Verify all formulas use MathJax ($...$ or $$...$$) not code blocks."""
    issues = []

    # Find code blocks containing math symbols
    code_blocks = re.findall(r"```.*?```", content, re.DOTALL)
    for i, block in enumerate(code_blocks):
        # Check for math indicators in code blocks
        math_indicators = [
            r"\\frac", r"\\sum", r"\\int", r"\\alpha", r"\\beta",
            r"\\theta", r"\\lambda", r"\\partial", r"\\nabla",
            r"\\mathbb", r"\\mathcal", r"\\mathbf",
        ]
        for indicator in math_indicators:
            if indicator in block:
                issues.append(
                    f"Math formula found inside code block #{i+1}: "
                    f"contains '{indicator}'. Use $...$ or $$...$$ instead."
                )
                break

    return issues


def check_figure_links(content: str) -> list[str]:
    """Check figure references are in Wikilink format."""
    issues = []

    # Find figure references that are NOT in ![[...]] format
    # Acceptable: ![[Fig.x description]]
    # Unacceptable: bare "Fig.x" in narrative text (unless in a clear text reference)

    # Check for HTML img tags (should use Obsidian embed syntax)
    html_imgs = re.findall(r'<img\s', content)
    for _ in html_imgs:
        issues.append("HTML <img> tag found. Use Obsidian embed syntax: ![[Fig.x desc]]")

    return issues


def check_wikilinks(content: str) -> list[str]:
    """Verify bidirectional links (Wikilinks) are properly formatted."""
    issues = []

    # Find [[links]]
    wikilinks = re.findall(r"\[\[([^\]]+)\]\]", content)
    if not wikilinks:
        issues.append("No Wikilinks (bidirectional links) found. Add at least in Section 22 (Concept Map).")

    # Check for broken-looking links
    for link in wikilinks:
        if "|" in link:
            # [[target|display]] — OK
            continue
        if len(link) < 2:
            issues.append(f"Potentially empty Wikilink: [[{link}]]")

    return issues


def check_language_handling(content: str) -> list[str]:
    """Check source language handling consistency."""
    issues = []

    # Check for source_language in YAML
    lang_match = re.search(r"source_language:\s*(\w+)", content)
    if not lang_match:
        issues.append("No source_language field in YAML frontmatter")
        return issues

    source_lang = lang_match.group(1).lower()

    # Check blockquote patterns
    blockquotes = re.findall(r"^> .+$", content, re.MULTILINE)

    if source_lang in ("english", "japanese", "german", "french", "korean"):
        # Foreign language: should have translation alongside original
        if len(blockquotes) == 0:
            issues.append("Foreign language paper but no > blockquotes found (expected original+translation)")
        # Count Chinese characters as evidence of translation
        chinese_chars = len(re.findall(r"[\u4e00-\u9fff]", content))
        if chinese_chars < 100:
            issues.append(f"Very few Chinese characters ({chinese_chars}). Expected translation to Chinese.")

    elif source_lang in ("chinese", "zh"):
        # Chinese paper: should NOT have translation
        if len(blockquotes) > 0:
            # Check if blockquotes contain both CN and foreign text (suspicious)
            has_english_translation = False
            for bq in blockquotes:
                eng_words = len(re.findall(r"\b[a-zA-Z]{3,}\b", bq))
                cn_words = len(re.findall(r"[\u4e00-\u9fff]", bq))
                if eng_words > 10 and cn_words > 10:
                    has_english_translation = True
                    break
            if has_english_translation:
                issues.append("Chinese paper with apparent English translation in blockquotes. Chinese papers should NOT be translated.")

    return issues


def check_section_content_depth(content: str) -> list[str]:
    """Check sections have substantial content (not just a single line)."""
    issues = []
    warnings = []

    # Find all ## sections
    sections = re.split(r"\n(?=## )", content)
    empty_sections = []
    single_line_sections = []

    for section in sections:
        header_match = re.match(r"^##\s+(.+)", section)
        if not header_match:
            continue

        section_name = header_match.group(1).strip()
        # Get content after the heading
        body_lines = section.split("\n")[1:]  # Skip the heading
        body_lines = [l for l in body_lines if l.strip() and not l.strip().startswith("#")]

        if len(body_lines) == 0:
            empty_sections.append(section_name)
        elif len(body_lines) < 3:
            single_line_sections.append(section_name)

    for s in empty_sections:
        issues.append(f"Empty section: {s}")
    for s in single_line_sections:
        warnings.append(f"Very short section (consider expanding): {s}")

    return issues + [f"WARNING: {w}" for w in warnings]


def main():
    if len(sys.argv) < 2:
        print("Usage: python reading_note_quality.py <path/to/reading-note.md>")
        sys.exit(1)

    note_path = Path(sys.argv[1])
    if not note_path.exists():
        print(f"Error: File not found: {note_path}")
        sys.exit(2)

    content = note_path.read_text(encoding="utf-8")

    all_issues = []
    errors = 0
    warnings = 0

    checks = [
        ("YAML Frontmatter", check_yaml_frontmatter, True),
        ("Section Coverage", check_section_coverage, True),
        ("MathJax Syntax", check_mathjax_syntax, False),
        ("Figure Links Format", check_figure_links, False),
        ("Wikilinks (Bidirectional)", check_wikilinks, False),
        ("Language Handling", check_language_handling, True),
        ("Section Content Depth", check_section_content_depth, False),
    ]

    print(f"\n=== Phase 2.5: Reading Note Quality Check ===")
    print(f"File: {note_path}")
    print()

    for check_name, check_fn, is_critical in checks:
        issues = check_fn(content)
        if not issues:
            print(f"  ✓ {check_name} — PASS")
            continue

        for issue in issues:
            if issue.startswith("WARNING:"):
                prefix = "  ⚠"
                warnings += 1
            else:
                prefix = "  ✗"
                if is_critical:
                    errors += 1
                else:
                    warnings += 1
            print(f"{prefix} {check_name}: {issue.replace('WARNING: ', '')}")

    print(f"\n{'='*60}")
    print(f"Results: {errors} errors, {warnings} warnings")

    if errors > 0:
        print("❌ FAIL — Must fix errors before proceeding to Phase 3 (Dual-Agent QA).")
        sys.exit(2)
    elif warnings > 0:
        print("⚠ WARN — Consider addressing warnings before Phase 3.")
        sys.exit(1)
    else:
        print("✓ PASS — Ready for Phase 3 (Dual-Agent QA).")
        sys.exit(0)


if __name__ == "__main__":
    main()
