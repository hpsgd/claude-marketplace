---
name: pr-create
description: Create a pull request following team conventions
argument-hint: "[base branch, defaults to 'main']"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

Create a pull request that follows team conventions. This skill analyses ALL commits on the branch (not just the latest), drafts a conventional commit title, writes a structured description, pushes, and creates the PR.

## Mandatory Process

Execute every step in order. Do not skip.

### Step 1: Determine Base Branch

Use `$ARGUMENTS` if provided. Otherwise default to `main`.

```bash
BASE_BRANCH="${ARGUMENTS:-main}"
```

Verify the base branch exists:
```bash
git rev-parse --verify $BASE_BRANCH
```

### Step 2: Verify Branch State

1. **Check for uncommitted changes**:
   ```bash
   git status --short
   ```
   If there are uncommitted changes, stop and ask the user whether to commit them first or proceed without them. Do not silently ignore uncommitted work.

2. **Check current branch**:
   ```bash
   git branch --show-current
   ```
   If on `main` (or the base branch), stop. PRs come from feature branches.

3. **Check remote tracking**:
   ```bash
   git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null
   ```
   Note whether the branch tracks a remote. If not, you will need to push with `-u`.

### Step 3: Analyse ALL Commits

This is the most important step. The PR description must reflect the full scope of changes, not just the last commit.

1. **Get the full commit log**:
   ```bash
   git log --oneline $BASE_BRANCH..HEAD
   ```

2. **Get the full diff**:
   ```bash
   git diff $BASE_BRANCH...HEAD --stat
   ```
   And for the detailed diff:
   ```bash
   git diff $BASE_BRANCH...HEAD
   ```

3. **Read every changed file** in the diff to understand the full picture. Do not skim. If there are 20 changed files, read all 20.

4. **Categorise the changes**:
   - What is the primary type? (`feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `ci`, `perf`, `build`)
   - Is there a secondary type? (e.g., a `feat` that also includes `test` changes)
   - What is the scope? (which module, component, or area)
   - Is there a breaking change?

### Step 4: Draft the PR Title

The PR title becomes the squash commit message. It must follow Conventional Commits:

```
<type>[optional scope]: <description>
```

Rules:
- Under 70 characters total
- Imperative mood: "Add", "Fix", "Refactor" — not "Added", "Fixes", "Refactoring"
- No period at the end
- Lowercase after the colon (unless a proper noun)
- If breaking: `feat!: remove legacy API` or note in the footer
- The description captures the WHAT at a high level — details go in the body

Examples of good titles:
- `feat(auth): add SSO login with SAML provider`
- `fix: prevent duplicate webhook delivery on retry`
- `refactor(api): extract validation middleware from controllers`
- `docs: add deployment runbook for production`

Examples of bad titles:
- `Update code` (no type, vague)
- `feat: Added new feature for user authentication and also fixed some bugs` (too long, past tense, multiple concerns)
- `fix: Fix bug` (redundant, no context)

### Step 5: Draft the PR Description

Use this template. Fill every section.

```markdown
## Summary
- [1-3 bullet points: WHAT changed and WHY]
- [Focus on the motivation and outcome, not the implementation details]
- [If fixing a bug, describe the bug and its impact]

## Changes
- [Grouped by area: API, UI, database, tests, config, etc.]
- [Each bullet: specific file or module and what changed]
- [Include new dependencies, migrations, config changes]

## Test plan
- [How to verify the changes work]
- [Specific commands to run, or manual steps to follow]
- [What to check in CI]
- [Edge cases to test manually]
```

Additional sections to include when relevant:

```markdown
## Breaking changes
- [What breaks, who is affected, migration steps]

## Screenshots
[For UI changes — before and after]

## Related issues
Closes #[issue number]
```

Rules for the description:
- Write in active voice, direct tone
- No filler phrases ("This PR...", "In this change we...")
- Lead each bullet with the action or outcome
- Be specific: "Add retry logic with exponential backoff (max 3 attempts)" not "Improve error handling"
- The test plan must be actionable — someone unfamiliar with the code should be able to follow it

### Step 6: Push and Create

1. **Push the branch**:
   ```bash
   git push -u origin $(git branch --show-current)
   ```

2. **Create the PR**:
   ```bash
   gh pr create --title "<title>" --body "$(cat <<'EOF'
   <body content>
   EOF
   )"
   ```

3. **Verify creation**:
   ```bash
   gh pr view --json url,title,state
   ```

### Step 7: Report

Share the PR URL and a brief summary:
```
PR created: <URL>
Title: <title>
Base: <base branch>
Commits: N
Files changed: N
```

## Common Mistakes to Avoid

1. **Describing only the last commit** — the PR covers all commits since diverging from base. Read every commit.
2. **Vague test plan** — "run the tests" is not a test plan. Specify which tests, what commands, what to check.
3. **Missing context** — the reviewer was not in your head when you wrote the code. Explain the WHY.
4. **Too much implementation detail in the title** — the title is a summary. Details go in the body.
5. **Not checking for uncommitted changes** — pushing a branch with local changes not included leads to confusion.
6. **Creating from main** — always create from a feature branch.

## Edge Cases

- **Single commit branch**: The PR title should match the commit message (it already follows conventional commits if the commit does).
- **Many small commits**: Summarise the overall change. The individual commit messages inform the description but the PR title captures the whole.
- **Draft PRs**: If the user says "draft" or "WIP", add `--draft` to the `gh pr create` command.
- **Cross-repo PRs**: If the base is on a different fork, use `--repo` and `--head` flags appropriately.

## Related Skills

- `/code-reviewer:code-review` — run a code review before creating the PR to catch issues early.
