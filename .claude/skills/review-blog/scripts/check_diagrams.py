#!/usr/bin/env python3
"""Check text diagram alignment in MDX blog posts.

Finds all ```text code blocks, measures the display width of each line
using Unicode east_asian_width, and reports any lines that don't match
the expected width (derived from the first line of each diagram).

Usage:
    python check_diagrams.py <path-to-mdx-file>
"""

import sys
import unicodedata


def display_width(s: str) -> int:
    """Calculate the display width of a string in a monospace font."""
    width = 0
    for ch in s:
        if unicodedata.east_asian_width(ch) in ("W", "F"):
            width += 2
        else:
            width += 1
    return width


def find_diagrams(lines: list[str]) -> list[tuple[int, int]]:
    """Find all ```text diagram blocks. Returns list of (start, end) line numbers (1-indexed)."""
    diagrams = []
    i = 0
    while i < len(lines):
        stripped = lines[i].rstrip()
        if stripped == "```text":
            start = i + 2  # line after ```text (1-indexed)
            j = i + 1
            while j < len(lines) and lines[j].rstrip() != "```":
                j += 1
            end = j  # line before closing ``` (1-indexed)
            if j > i + 1:
                # Only include bordered diagrams (starting with ┌ or +)
                first_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
                if first_line.startswith("┌") or first_line.startswith("+"):
                    diagrams.append((start, end))
            i = j + 1
        else:
            i += 1
    return diagrams


def check_diagram(lines: list[str], start: int, end: int) -> list[str]:
    """Check a single diagram for alignment issues. Returns list of issue descriptions."""
    issues = []
    diagram_lines = []

    for line_num in range(start, end + 1):
        idx = line_num - 1
        if idx < len(lines):
            content = lines[idx].rstrip("\n")
            w = display_width(content)
            diagram_lines.append((line_num, content, w))

    if not diagram_lines:
        return issues

    # Use the first line's width as the expected width
    expected_width = diagram_lines[0][2]

    for line_num, content, w in diagram_lines:
        if w != expected_width:
            diff = w - expected_width
            direction = "wider" if diff > 0 else "narrower"
            issues.append(
                f"Line {line_num}: display width is {w} ({abs(diff)} {direction} "
                f"than expected {expected_width})"
            )

    # Check for Vietnamese diacritical characters inside diagrams
    vietnamese_chars = set("àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ"
                          "ÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴĐ")
    for line_num, content, w in diagram_lines:
        found = [ch for ch in content if ch in vietnamese_chars]
        if found:
            issues.append(
                f"Line {line_num}: contains Vietnamese characters: {''.join(set(found))} "
                f"— use English inside diagrams"
            )

    # Check for wide Unicode arrows
    wide_arrows = {"▶": ">", "▼": "v", "→": "->", "◀": "<", "▲": "^", "←": "<-"}
    for line_num, content, w in diagram_lines:
        for arrow, replacement in wide_arrows.items():
            if arrow in content:
                issues.append(
                    f"Line {line_num}: contains wide Unicode arrow '{arrow}' "
                    f"(2 columns wide) — replace with '{replacement}'"
                )

    return issues


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path-to-mdx-file>")
        sys.exit(1)

    filepath = sys.argv[1]
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    diagrams = find_diagrams(lines)

    if not diagrams:
        print("No ```text diagrams found.")
        sys.exit(0)

    all_ok = True
    for i, (start, end) in enumerate(diagrams, 1):
        issues = check_diagram(lines, start, end)
        if issues:
            all_ok = False
            print(f"Diagram {i} (lines {start}-{end}):")
            for issue in issues:
                print(f"  - {issue}")
            print()
        else:
            print(f"Diagram {i} (lines {start}-{end}): OK")

    if all_ok:
        print("\nAll diagrams passed alignment check.")
    else:
        print("\nSome diagrams have alignment issues.")
        sys.exit(1)


if __name__ == "__main__":
    main()
