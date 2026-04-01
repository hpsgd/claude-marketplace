---
name: review-python
description: Review Python code against team conventions. Auto-invoked when reviewing .py files.
allowed-tools: Read, Grep, Glob, Bash
paths:
  - "**/*.py"
---

When reviewing Python code, check against these standards:

- mypy strict, no `Any` without justification
- Frozen dataclasses for domain models
- Kebab-case for config file names
- Explicit `{path: ...}` form for all references
- Testing hierarchy: BDD > Property-based > Unit
- Coverage target: 98%+, 80%+ mutation kill rate
- Ruff clean — no lint suppressions without discussion

For each violation found, report:
1. The file and line
2. Which standard is violated
3. A concrete suggestion for fixing it

Summarize findings grouped by severity: critical, important, suggestion.
