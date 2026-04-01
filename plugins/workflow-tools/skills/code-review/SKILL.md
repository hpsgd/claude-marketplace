---
name: code-review
description: Perform a structured code review of staged or recent changes
argument-hint: "[branch or commit range, e.g. 'main..HEAD']"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

Perform a thorough code review using this structured process:

## 1. Understand the scope
- Run `git diff $ARGUMENTS` (or `git diff --staged` if no argument provided) to see what changed
- Read the full context of each modified file to understand the surrounding code

## 2. Review checklist
For each changed file, evaluate:

**Correctness**
- Does the logic do what it intends?
- Are edge cases handled?
- Are there off-by-one errors, null/undefined risks, or race conditions?

**Security**
- Any user input used without validation?
- SQL injection, XSS, command injection risks?
- Secrets or credentials exposed?

**Performance**
- Unnecessary re-renders, redundant queries, or O(n^2) algorithms?
- Missing indexes for new database queries?

**Maintainability**
- Is the code readable without comments?
- Are names descriptive and consistent?
- Is there duplication that should be extracted?

**Tests**
- Are new code paths tested?
- Do tests cover the happy path and key error cases?

## 3. Output format
Organize findings by severity:
- **Blockers**: Must fix before merge
- **Suggestions**: Would improve the code but not blocking
- **Nits**: Style/preference items

For each finding, include the file, line range, and a concrete fix suggestion.
