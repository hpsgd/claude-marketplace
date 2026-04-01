---
name: review-standards
description: Review code changes against general quality and writing style standards. Auto-invoked during code review for cross-cutting concerns.
allowed-tools: Read, Grep, Glob, Bash
---

When reviewing code, check against these general standards:

## Code quality
- Functions focused on a single responsibility
- Error handling uses typed errors, not thrown strings
- No dead code or commented-out code
- No lint suppressions without explicit discussion

## Writing style (if docs/comments/copy changed)
- No banned AI words: delve, tapestry, landscape, nuanced, robust, crucial, etc.
- No banned phrases: "it's important to note", "in today's world", "at its core", etc.
- Active voice, direct tone, vary sentence length
- Avoid participial phrases (-ing constructions)
- Em dashes: 1-2 per document max

For each violation found, report:
1. The file and line
2. Which standard is violated
3. A concrete suggestion for fixing it

Summarize findings grouped by severity: critical, important, suggestion.
