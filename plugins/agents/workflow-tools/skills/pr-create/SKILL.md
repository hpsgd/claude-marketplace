---
name: pr-create
description: Create a pull request following team conventions
argument-hint: "[base branch, defaults to 'main']"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

Create a pull request following team conventions:

## Process

1. **Determine the base branch**: Use `$ARGUMENTS` if provided, otherwise default to `main`

2. **Analyze changes**: Run `git log` and `git diff` against the base branch to understand all commits being included

3. **Draft the PR**:
   - **Title**: Under 70 characters, describes the change concisely. Use conventional format:
     - `feat: ...` for new features
     - `fix: ...` for bug fixes
     - `refactor: ...` for refactoring
     - `docs: ...` for documentation
     - `test: ...` for test changes
     - `chore: ...` for maintenance
   - **Body**: Use this template:

```
## Summary
<1-3 bullet points describing what changed and why>

## Changes
<Bulleted list of specific changes, grouped by area>

## Test plan
<How to verify the changes work — manual steps or test commands>
```

4. **Push and create**: Push the branch and create the PR using `gh pr create`

5. **Report**: Share the PR URL when done
