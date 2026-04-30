#!/usr/bin/env python3
"""
PostToolUse check on result.md edits — verify the verdict label matches the score.

Rules:
  score >= 80%  → PASS
  score >= 60%  → PARTIAL
  score < 60%   → FAIL

Silent on pass, blocks on mismatch.
"""
import json
import re
import sys


def main() -> int:
    payload = json.load(sys.stdin)
    tool_input = payload.get("tool_input", {}) or {}
    path = tool_input.get("file_path", "")

    if "/result.md" not in path or "/examples/" not in path:
        return 0

    try:
        text = open(path).read()
    except FileNotFoundError:
        return 0

    verdict = re.search(
        r"(?:\*\*)?Verdict(?:\*\*)?[\s|:]+\*?\*?\s*(PASS|PARTIAL|FAIL)",
        text,
        re.IGNORECASE,
    )
    if not verdict:
        verdict = re.search(
            r"\|\s*Verdict\s*\|\s*Score\s*\|[^\n]*\n\|[^\n]*\n\|\s*(PASS|PARTIAL|FAIL)\s*\|",
            text,
            re.IGNORECASE,
        )

    score = re.search(
        r"(?:\*\*)?Score(?:\*\*)?[\s|:]+\*?\*?\s*[\d.]+\s*/\s*[\d.]+[^()]*\(([\d.]+)\s*%?\)",
        text,
    )
    if not score:
        score = re.search(
            r"\|\s*(?:PASS|PARTIAL|FAIL)\s*\|\s*[\d.]+\s*/\s*[\d.]+[^()]*\(([\d.]+)\s*%?\)",
            text,
        )

    if not (verdict and score):
        return 0

    pct = float(score.group(1))
    actual = verdict.group(1).upper()
    expected = "PASS" if pct >= 80 else ("PARTIAL" if pct >= 60 else "FAIL")

    if actual == expected:
        return 0

    print(
        f"Verdict mismatch in {path}\n"
        f"  Score: {pct}%\n"
        f"  Verdict label: {actual}\n"
        f"  Expected (rule: PASS >= 80%, PARTIAL >= 60%, FAIL < 60%): {expected}\n"
        f"  Update the Verdict cell to {expected}.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
