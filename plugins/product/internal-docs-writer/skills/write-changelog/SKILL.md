---
name: write-changelog
description: Generate a changelog from git history, PRs, or a list of changes. Written for the target audience (users or developers).
argument-hint: "[git range e.g. 'v1.0.0..HEAD', or 'since last release']"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Generate a changelog for $ARGUMENTS using the mandatory process below.

## Step 1 — Gather the raw changes

Run these commands to extract the change data:

```bash
# Get the commit log with author and date
git log --format="%h %s (%an, %ad)" --date=short $RANGE

# Get the full diff stat for scope assessment
git diff --stat $RANGE

# Get any tags in range for version markers
git tag --merged HEAD --no-merged $BASE_REF --sort=-version:refname

# Get PR merge commits if using PR-based workflow
git log --merges --format="%h %s" $RANGE
```

Replace `$RANGE` with the user's specified range (e.g., `v1.0.0..HEAD`). If the user says "since last release," first find the latest tag:

```bash
git describe --tags --abbrev=0
```

If no tags exist, ask the user for a commit range or use the last 50 commits.

## Step 2 — Classify each change

For every commit/PR, assign it to exactly one group:

| Group | Include when | Conventional Commits prefixes |
|---|---|---|
| **Added** | New feature, new endpoint, new capability that didn't exist before | `feat:` |
| **Changed** | Modification to existing behaviour, UI changes, API changes | `refactor:`, `style:`, `perf:` |
| **Fixed** | Bug fix — something was broken and is now correct | `fix:` |
| **Removed** | Feature, endpoint, or option that has been removed | `feat!:`, BREAKING CHANGE |
| **Deprecated** | Feature marked for future removal | `deprecate:` |
| **Security** | Vulnerability fix, dependency update for CVE, auth change | `security:`, `fix:` with security context |

### Skip rules — do NOT include these in the changelog

| Skip if | Reason |
|---|---|
| CI/CD pipeline changes (`.github/`, `Jenkinsfile`, `.circleci/`) | Not user-visible |
| Dependency version bumps (`chore(deps):`, `bump`) | Noise — unless it fixes a CVE, then put in Security |
| Code formatting, linting fixes (`style:`, `chore: format`) | Not user-visible |
| Internal refactoring with no behaviour change | Not user-visible |
| Merge commits that duplicate PR content | Avoid double-counting |
| Test additions/changes (`test:`) | Not user-visible |
| Version bump commits (`chore: release`, `bump version`) | Meta, not a change |

When uncertain whether to include a change: if a user would notice the difference, include it. If they wouldn't, skip it.

## Step 3 — Determine the audience and write accordingly

### User-facing changelog (default)

Write from the user's perspective. Describe what changed for them, not what changed in the code.

- Bad: "Refactored the QueryBuilder class to use prepared statements"
- Good: "Fixed a bug where search queries with special characters returned no results"
- Bad: "Added `maxRetries` parameter to `HttpClient`"
- Good: "API requests now automatically retry on temporary failures (up to 3 attempts)"

### Developer-facing changelog

Write from the developer's perspective. Include technical details, breaking changes, migration steps.

- Good: "Added `maxRetries` parameter to `HttpClient` constructor (default: 3). Set to 0 to disable."
- Good: "BREAKING: `User.getProfile()` now returns a `Promise<Profile>` instead of `Profile`. Update all call sites to use `await`."

## Step 4 — Write each entry

Every changelog entry MUST follow these rules:

1. **Imperative mood** — "Add export feature" not "Added export feature" or "Adds export feature"
2. **Start with a verb** — "Fix," "Add," "Remove," "Change," "Improve," "Update"
3. **One change per line** — if a PR contains multiple changes, split them into separate entries
4. **No ticket/PR numbers in the text** — put references in parentheses at the end if needed: `(#123)`
5. **Lead with the user impact** — "Speed up dashboard loading by 40%" not "Optimize database queries"
6. **Include breaking change warnings** — prefix with `**BREAKING:**` and explain what to do

## Step 5 — Assemble the changelog

Use this format:

```markdown
## [version] — YYYY-MM-DD

### Added
- [entry]
- [entry]

### Changed
- [entry]

### Fixed
- [entry]

### Removed
- [entry]

### Security
- [entry]
```

Rules for assembly:
- Omit empty groups — if there are no Security changes, don't include the Security header
- Order groups: Added → Changed → Fixed → Removed → Deprecated → Security
- Within each group, order by impact (most significant first)
- If there are breaking changes, add a prominent section at the top:

```markdown
### ⚠ Breaking changes
- **BREAKING:** [description and migration steps]
```

## Step 6 — Version comparison summary

At the top of the changelog, include a brief summary:

```markdown
**[version]** brings [N] new features, [N] fixes, and [N] improvements.
[One sentence highlighting the most significant change.]
```

If comparing two versions, include the diff stats:

```markdown
**Comparing [old] → [new]**: [N] commits, [N] files changed, [N] contributors
```

## Step 7 — Final checks

Before delivering, verify:

| Check | Pass? |
|---|---|
| Every entry uses imperative mood | |
| No CI/deps/formatting changes leaked in | |
| Breaking changes are clearly marked | |
| Audience is appropriate (user vs developer language) | |
| Entries are sorted by impact within groups | |
| No duplicate entries (from merge commits) | |
| Version number and date are present | |
| Empty groups are omitted | |

## Rules

- When a single commit touches both user-visible and internal changes, only document the user-visible part.
- If the commit history is messy (no conventional commits, vague messages like "fix stuff"), read the actual diffs to understand what changed and write proper entries.
- If a bugfix and a feature are closely related (e.g., "add retry logic" could be a fix or a feature), classify based on whether the previous behaviour was a bug (→ Fixed) or just missing (→ Added).
- Security fixes should be described clearly enough for users to assess impact, but should not include exploitation details.
- For large changelogs (50+ entries), add a "Highlights" section at the top with the 3-5 most important changes.
