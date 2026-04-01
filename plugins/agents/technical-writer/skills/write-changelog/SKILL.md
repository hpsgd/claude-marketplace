---
name: write-changelog
description: Generate a changelog from git history, PRs, or a list of changes. Written for the target audience (users or developers).
argument-hint: "[git range e.g. 'v1.0.0..HEAD', or 'since last release']"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Generate a changelog for $ARGUMENTS.

Run `git log --oneline` for the specified range. Group changes by type (Added, Changed, Fixed, Removed, Security). Write for the target audience — user-facing changelogs describe what changed from the user's perspective, not the code perspective. Follow Conventional Commits types to categorise.

Skip: version bumps, dependency updates (unless security-relevant), CI changes, formatting changes.
