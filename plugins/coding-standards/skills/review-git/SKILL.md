---
name: review-git
description: Review git conventions — commit messages, PR titles, branch model. Auto-invoked during PR and commit workflows.
allowed-tools: Read, Grep, Glob, Bash
---

When reviewing commits or PRs, check against these standards:

## Commit messages
- Conventional Commits format: `<type>[optional scope]: <description>`
- Common types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`, `perf`, `build`
- Imperative mood: "Add feature" not "Added feature"
- First line under 70 characters
- Detail in the body, not the title

## PR conventions
- PR title matches conventional commit format
- One feature or fix per PR
- Description includes what changed and why
- Test plan describing how to verify

## Branch model
- Feature branches from `main`
- Squash merges only (linear history)
- No force pushing to update stale PRs — prefer rebase

## Content dates
- Preserve publication dates on articles — don't update to today's date

For each violation found, report:
1. What was found
2. Which convention is violated
3. A concrete suggestion for fixing it
