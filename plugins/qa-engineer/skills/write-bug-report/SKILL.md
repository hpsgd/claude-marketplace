---
name: write-bug-report
description: Write a structured bug report with reproduction steps, expected vs actual behaviour, and severity assessment.
argument-hint: "[bug description or failing test output]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Write a bug report for $ARGUMENTS.

## Structure

1. **Title** — concise description of the defect
2. **Severity** — critical (data loss, security), high (major feature broken), medium (degraded), low (cosmetic)
3. **Environment** — OS, browser, version, configuration
4. **Steps to reproduce** — numbered, each step is one action. Include exact inputs
5. **Expected behaviour** — what should happen
6. **Actual behaviour** — what actually happens (include error messages, screenshots, logs)
7. **Workaround** — if known
8. **Regression** — did this work before? If so, when did it break? (check git log)

## Rules

- Reproduction steps must be specific enough for someone unfamiliar with the code to follow
- Include the exact error message, not a paraphrase
- If intermittent, note the frequency and any conditions that seem to affect it
- Check if a test should have caught this — if so, note the coverage gap
