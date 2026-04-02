---
description: Git workflow, branching, CI/CD, and commit conventions
---

# Git & CI/CD Conventions

## Commit message format

Commits must follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Common types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`, `perf`, `build`.

## Branch model

```
feature/my-thing ──squash──> main
```

- Feature branches from `main`
- Squash merges only into main (linear history)
- PR titles must be conventional commits
- No direct commits to main

## Pull requests
- Keep PRs focused — one feature or fix per PR
- Include a description of what changed and why
- Add a test plan describing how to verify the changes
- Request review from at least one team member

## Pre-commit checks
- Lint, format-check, and typecheck staged files before commit
- Fix issues before committing — don't bypass hooks

## Pre-push verification (monorepos)
- Run full CI across ALL projects, not just the one you changed
- In [Moon](https://moonrepo.dev) monorepos: `moon ci` checks web apps, packages, AND services
- Known gotchas: [Storybook](https://storybook.js.org) artifacts may need cleaning, CSharpier formatting, `package-lock.json` changes, .NET integration tests

## Force pushing
- Avoid force-pushing to update stale PRs
- Prefer `git rebase` (resolving conflicts) or merging main into the branch
- Discuss approach before force-pushing if conflicts are messy
- Check `git remote -v` to verify the correct repo before any push

## Content dates
- Preserve publication dates on articles and content — don't update to today's date
- Authors set intentional publish dates; changing them disrupts publishing schedules
