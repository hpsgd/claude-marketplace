#!/usr/bin/env python3
"""Strip hook-managed artifact blocks from existing test result.md files.

Older result.md files were generated before run-test.py learned to filter
hook-installed paths (rules/, learnings/signals/, learnings/sessions/, and
their global counterparts) from the artifact snapshot. They contain ~1500
lines of noise per file — rule files installed by the SessionStart hook
and signal entries from the message classifier hook.

This script post-processes result.md files in place: parses the
`### Artifacts written` section, drops `#### `<hook-path>`` blocks, keeps
everything else. Verdict, criteria, chat response, and skill-written
artifacts are untouched.

Usage:
  python3 clean-result-artifacts.py                       # walk examples/ from cwd
  python3 clean-result-artifacts.py path/to/result.md     # one file
  python3 clean-result-artifacts.py path/to/dir           # walk dir for result.md
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_HOOK_PATH_PATTERNS = [
    re.compile(r"^rules(/|$)"),
    re.compile(r"^global-rules(/|$)"),
    re.compile(r"^learnings/signals(/|$)"),
    re.compile(r"^learnings/sessions(/|$)"),
    re.compile(r"^global-learnings/signals(/|$)"),
    re.compile(r"^global-learnings/sessions(/|$)"),
]


def is_hook_path(path: str) -> bool:
    return any(p.match(path) for p in _HOOK_PATH_PATTERNS)


def clean_result(text: str) -> tuple[str, int]:
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    i = 0
    in_artifacts = False
    dropped = 0
    artifact_header = re.compile(r"^### Artifacts written\s*$")
    section_break = re.compile(r"^##\s")
    artifact_block_header = re.compile(r"^#### `([^`]+)`\s*$")

    while i < len(lines):
        line = lines[i]
        if artifact_header.match(line):
            in_artifacts = True
            out.append(line)
            i += 1
            continue
        if in_artifacts and section_break.match(line):
            in_artifacts = False
        if in_artifacts:
            m = artifact_block_header.match(line)
            if m and is_hook_path(m.group(1)):
                # Skip the entire block: header + content + trailing blank lines
                # until the next #### header or ## section break.
                i += 1
                while i < len(lines):
                    nxt = lines[i]
                    if nxt.startswith("#### ") or section_break.match(nxt):
                        break
                    i += 1
                dropped += 1
                continue
        out.append(line)
        i += 1
    return "".join(out), dropped


def find_targets(arg: Path) -> list[Path]:
    if arg.is_file():
        return [arg]
    if arg.is_dir():
        return sorted(arg.rglob("result.md"))
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", default="examples",
                        help="Path to a result.md, or a directory to walk (default: examples)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print what would change without modifying files")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    files = find_targets(target)
    if not files:
        print(f"No result.md files found at {target}", file=sys.stderr)
        return 1

    total_before = 0
    total_after = 0
    files_changed = 0
    total_blocks_dropped = 0

    for path in files:
        original = path.read_text()
        before_lines = original.count("\n")
        cleaned, dropped = clean_result(original)
        after_lines = cleaned.count("\n")

        total_before += before_lines
        total_after += after_lines

        if dropped == 0:
            continue

        files_changed += 1
        total_blocks_dropped += dropped
        rel = path.relative_to(Path.cwd()) if str(path).startswith(str(Path.cwd())) else path
        print(f"{rel}: dropped {dropped} hook block(s), {before_lines} -> {after_lines} lines")

        if not args.dry_run:
            path.write_text(cleaned)

    print()
    print(f"{files_changed}/{len(files)} files changed; {total_blocks_dropped} hook blocks dropped; "
          f"{total_before} -> {total_after} total lines "
          f"({100 * (total_before - total_after) / max(total_before, 1):.0f}% reduction)")
    if args.dry_run:
        print("(dry run — no files modified)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
