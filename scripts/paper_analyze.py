#!/usr/bin/env python3
"""
Phase 1.5: Cross-Agent Synthesis Checkpoint tool.
Scans all agent analysis files in output-dir/analysis/ and generates
a summary table with key findings, confidence levels, contradictions,
and information gaps.

Usage:
    python paper_analyze.py <output-dir>

Example:
    python paper_analyze.py paper-reading-notes/attention-is-all-you-need

Output: Prints markdown-formatted summary table to stdout.
"""

import sys
import re
import json
from pathlib import Path
from datetime import datetime

AGENT_FILES = {
    "01-core-argument.md": "1 核心论点",
    "02-methodology.md": "2 方法论",
    "03-mathematical-analysis.md": "3 数学分析",
    "04-results-data.md": "4 结果数据",
    "05-literature-context.md": "5 文献脉络",
    "06-critical-assessment.md": "6 批判评估",
    "07-figure-analysis.md": "7 图表分析",
    "08-code-implementation.md": "8 代码实现",
}

# Keywords that indicate confidence levels
HIGH_CONFIDENCE = [
    "clearly", "demonstrates", "confirmed by", "explicitly stated",
    "明确", "证实", "验证", "正如", "原文指出"
]
LOW_CONFIDENCE = [
    "unclear", "ambiguous", "not specified", "vague", "UNCERTAIN",
    "possibly", "seems to", "不明确", "不清晰", "可能", "似乎",
    "INFERRED", "推断", "推测"
]
CONTRADICTION_MARKERS = [
    "CONTRADICTS", "contradicts", "inconsistent", "disagrees",
    "矛盾", "不一致", "相反", "不符合"
]
GAP_MARKERS = [
    "GAP:", "INSUFFICIENT DATA", "NOT APPLICABLE", "MISSING",
    "缺口", "缺失", "不足", "不适用"
]


def analyze_file(filepath: Path) -> dict:
    """Analyze a single agent output file."""
    if not filepath.exists():
        return {"status": "missing", "label": AGENT_FILES.get(filepath.name, filepath.stem)}

    content = filepath.read_text(encoding="utf-8")
    lines = content.split("\n")

    # Extract headings as key findings
    headings = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## ") or stripped.startswith("### "):
            heading = stripped.lstrip("# ").strip()
            if len(heading) < 80:
                headings.append(heading)

    # Determine confidence
    high_count = sum(1 for kw in HIGH_CONFIDENCE if kw.lower() in content.lower())
    low_count = sum(1 for kw in LOW_CONFIDENCE if kw.lower() in content.lower())
    gap_count = sum(1 for kw in GAP_MARKERS if kw in content)
    total_lines = len([l for l in lines if l.strip()])

    if total_lines < 5:
        confidence = "N/A"
    elif gap_count > 3 or low_count > high_count * 2:
        confidence = "LOW"
    elif low_count > high_count:
        confidence = "MEDIUM"
    else:
        confidence = "HIGH"

    # Key findings: top 2 headings, or first substantive lines
    key_findings = []
    for h in headings[:2]:
        short = h[:50] + "..." if len(h) > 50 else h
        key_findings.append(short)

    if not key_findings:
        # Fallback: first bullet points
        bullets = re.findall(r"^[-*]\s+(.+)$", content, re.MULTILINE)
        for b in bullets[:2]:
            key_findings.append(b[:50] + "..." if len(b) > 50 else b)

    if not key_findings:
        key_findings = ["(内容待解析)"]

    return {
        "status": "ok",
        "label": AGENT_FILES.get(filepath.name, filepath.stem),
        "confidence": confidence,
        "key_findings": key_findings,
        "total_lines": total_lines,
        "headings": headings,
        "gap_count": gap_count,
    }


def detect_contradictions(results: dict) -> list[str]:
    """Detect cross-agent contradictions."""
    contradictions = []
    for filename, result in results.items():
        if result["status"] != "ok":
            continue
        content = Path(filename).read_text(encoding="utf-8")
        for marker in CONTRADICTION_MARKERS:
            if marker in content:
                match = re.search(
                    rf".{{0,60}}{re.escape(marker)}.{{0,60}}",
                    content
                )
                if match:
                    contradictions.append(
                        f"{result['label']}: ...{match.group().strip()[:80]}..."
                    )
    return contradictions[:5]


def detect_gaps(results: dict) -> list[str]:
    """Collect all information gaps across agents."""
    gaps = []
    for filename, result in results.items():
        if result["status"] != "ok":
            continue
        content = Path(filename).read_text(encoding="utf-8")
        for marker in GAP_MARKERS:
            pattern = rf"{re.escape(marker)}(.{{0,120}})"
            for m in re.finditer(pattern, content):
                gaps.append(f"{result['label']}: {m.group().strip()[:100]}")
    return gaps[:8]


def main():
    if len(sys.argv) < 2:
        print("Usage: python paper_analyze.py <output-dir>")
        print("Example: python paper_analyze.py paper-reading-notes/my-paper")
        sys.exit(1)

    output_dir = Path(sys.argv[1])
    analysis_dir = output_dir / "analysis"

    if not analysis_dir.exists():
        print(f"Error: analysis directory not found: {analysis_dir}")
        print("Make sure Phase 1 agents have completed and written their outputs.")
        sys.exit(1)

    # Analyze each agent file
    results = {}
    for filename, label in AGENT_FILES.items():
        filepath = analysis_dir / filename
        r = analyze_file(filepath)
        results[filepath] = r

    # Count present/missing agents
    present = sum(1 for r in results.values() if r["status"] == "ok")
    missing_agents = [r["label"] for r in results.values() if r["status"] == "missing"]

    # Detect contradictions and gaps
    contradictions = detect_contradictions(results)
    gaps = detect_gaps(results)

    # Build output
    print(f"\n=== Phase 1.5: Cross-Agent Synthesis Checkpoint ===")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Source: {output_dir}")
    print(f"Active agents: {present}/{len(AGENT_FILES)}")
    print()

    # Summary table
    header = (
        f"{'Agent':<20} {'Key Findings':<48} {'Confidence':<12}"
    )
    separator = f"{'─'*20} {'─'*48} {'─'*12}"
    print(header)
    print(separator)

    for filepath, r in results.items():
        label = r["label"]
        if r["status"] == "missing":
            print(f"{label:<20} {'(缺失 — 该Agent未运行)':<48} {'—':<12}")
            continue

        findings = r["key_findings"][0] if r["key_findings"] else "(无)"
        confidence = r["confidence"]
        conf_icon = {"HIGH": "● HIGH", "MEDIUM": "◐ MEDIUM", "LOW": "○ LOW", "N/A": "—"}.get(confidence, confidence)
        print(f"{label:<20} {findings:<48} {conf_icon:<12}")

    print(separator)

    # Cross-agent contradictions
    if contradictions:
        print(f"\n{'='*60}")
        print(f"⚠ Cross-Agent Contradictions ({len(contradictions)} found):")
        for c in contradictions:
            print(f"  • {c}")
    else:
        print(f"\n{'='*60}")
        print("✓ No cross-agent contradictions detected.")

    # Information gaps
    if gaps:
        print(f"\n{'='*60}")
        print(f"⚠ Information Gaps ({len(gaps)} found):")
        for g in gaps:
            print(f"  • {g}")

    # Missing agents
    if missing_agents:
        print(f"\n{'='*60}")
        print(f"⚠ Missing Agents: {', '.join(missing_agents)}")
        print("  These dimensions were not analyzed. Consider re-running if critical.")

    # Overall quality assessment
    print(f"\n{'='*60}")
    total_confidence = sum(
        1 for r in results.values()
        if r["status"] == "ok" and r["confidence"] in ("HIGH", "MEDIUM")
    )
    if present == 0:
        print("❌ CRITICAL: No agent outputs found. Cannot proceed.")
    elif total_confidence < max(present - 1, 1):
        print("⚠ CAUTION: Multiple agents have LOW confidence. Consider deeper analysis.")
    elif len(contradictions) > 2:
        print("⚠ CAUTION: Multiple cross-agent contradictions. Review before Phase 2.")
    else:
        print("✓ Ready to proceed to Phase 2 (20-Point Note Generation).")

    print()

    # Write a machine-readable summary JSON to analysis/ dir
    summary = {
        "timestamp": datetime.now().isoformat(),
        "output_dir": str(output_dir),
        "present_agents": present,
        "total_agents": len(AGENT_FILES),
        "missing_agents": missing_agents,
        "agent_details": {
            r["label"]: {
                "status": r["status"],
                "confidence": r["confidence"] if r["status"] == "ok" else "N/A",
                "gap_count": r.get("gap_count", 0),
            }
            for r in results.values()
        },
        "contradictions_count": len(contradictions),
        "gaps_count": len(gaps),
    }
    summary_path = analysis_dir / "_phase15_summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Summary written to: {summary_path}")


if __name__ == "__main__":
    main()
