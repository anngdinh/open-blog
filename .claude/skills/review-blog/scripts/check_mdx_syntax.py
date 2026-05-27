#!/usr/bin/env python3
"""Check MDX files for syntax patterns that break the parser.

MDX treats `<` as the start of a JSX tag whenever it appears in prose.
Common patterns that look fine when writing but explode at build time:

  - `<50ms`           (less-than + digit in measurements/comparisons)
  - `<N is small`     (less-than + single letter used as a variable)

This script scans MDX files outside of code blocks (``` fenced and `inline`)
and flags occurrences. It does not run an MDX parser — it's a fast, regex-based
linter that catches the patterns we've actually been bitten by.

Usage:
    python3 check_mdx_syntax.py <path-to-mdx-file> [<more-files>...]

Exit code 1 if any issues found, 0 if clean.
"""

import re
import sys


# `<` followed by a digit. JSX tag names must start with a letter, $, or _ —
# so `<5` is always a hard parse error. This is the high-confidence catch.
LT_DIGIT = re.compile(r"<(\d)")

# `<` followed by a single letter then whitespace or punctuation. Looks like
# `<N seconds`, `<x is the count`. JSX would try to parse `<N` as a tag with
# attributes and usually fails. Lower confidence (a real JSX tag like `<a href="...">`
# also matches), so we treat these as warnings, not errors.
LT_LETTER_WORD = re.compile(r"<([a-zA-Z])(\s|[,.;:!?])")


def strip_code_regions(text: str) -> str:
    """Replace fenced code blocks and inline code with spaces of the same length.

    Preserving length keeps line numbers and column offsets accurate so we can
    point at the original location of any issue we find.
    """
    out = list(text)

    # Fenced code blocks: ```lang ... ```
    for m in re.finditer(r"```.*?```", text, re.DOTALL):
        start, end = m.span()
        for i in range(start, end):
            if out[i] != "\n":
                out[i] = " "

    # Inline code: `...` (single-backtick spans on one line)
    for m in re.finditer(r"`[^`\n]+`", "".join(out)):
        start, end = m.span()
        for i in range(start, end):
            if out[i] != "\n":
                out[i] = " "

    # Quoted strings inside MDX prose. Important for JSX attribute values like
    # `alt="something with <20 in it"` — the `<` inside quotes is harmless to MDX
    # but our naive `<digit` regex would flag it. Strip them so we don't false-positive.
    # We do this BEFORE the JSX tag pass so multi-line attribute values are neutralized.
    for m in re.finditer(r'"[^"\n]*"|\'[^\'\n]*\'', "".join(out)):
        start, end = m.span()
        for i in range(start, end):
            if out[i] != "\n":
                out[i] = " "

    # JSX-style HTML inside MDX: <img ... />, <div>...</div>, etc.
    # We strip well-formed JSX tags so we don't false-positive on them.
    # The `re.DOTALL` flag lets the regex span newlines for multi-line tags.
    for m in re.finditer(r"<[A-Za-z][A-Za-z0-9]*(\s[^<>]*)?/?>", "".join(out), re.DOTALL):
        start, end = m.span()
        for i in range(start, end):
            if out[i] != "\n":
                out[i] = " "

    return "".join(out)


def find_issues(text: str) -> list[tuple[int, int, str, str]]:
    """Return (line, col, severity, message) for each issue found."""
    cleaned = strip_code_regions(text)
    issues = []

    # Build a line/col index from offset
    line_starts = [0]
    for i, ch in enumerate(cleaned):
        if ch == "\n":
            line_starts.append(i + 1)

    def loc(offset: int) -> tuple[int, int]:
        # Binary search would be nicer, but linear is fine for blog-sized files.
        line = 0
        for i, start in enumerate(line_starts):
            if start > offset:
                break
            line = i
        col = offset - line_starts[line] + 1
        return (line + 1, col)

    for m in LT_DIGIT.finditer(cleaned):
        line, col = loc(m.start())
        issues.append((line, col, "ERROR",
                       f"`<{m.group(1)}` will break MDX parsing (JSX tag names cannot start with a digit). "
                       f"Wrap in backticks (`<{m.group(1)}...`) or use `&lt;`."))

    for m in LT_LETTER_WORD.finditer(cleaned):
        line, col = loc(m.start())
        snippet = m.group(0)
        issues.append((line, col, "WARN",
                       f"`{snippet}` looks like prose but MDX may try to parse `<{m.group(1)}` as a JSX tag. "
                       f"Wrap in backticks or rephrase if this isn't an HTML element."))

    return issues


def check_file(path: str) -> int:
    with open(path, encoding="utf-8") as f:
        text = f.read()

    issues = find_issues(text)
    if not issues:
        return 0

    print(f"=== {path} ===")
    for line, col, severity, msg in issues:
        print(f"  {path}:{line}:{col}: [{severity}] {msg}")
    return 1


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2

    failures = 0
    for path in sys.argv[1:]:
        failures += check_file(path)

    if failures:
        print(f"\n{failures} file(s) have potential MDX syntax issues.")
        return 1

    print("All files clean of known MDX syntax pitfalls.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
