# Test: pr-create skill structure

Scenario: Checking that the pr-create skill analyses ALL commits on a branch (not just the latest), produces a conventional commit title, and writes a structured description with a usable test plan.

## Prompt

Review the pr-create skill definition and verify it produces well-formed pull requests that give reviewers sufficient context.

## Criteria

- [ ] PASS: Skill explicitly requires reading every changed file in the diff — "if there are 20 changed files, read all 20" — not just the diffstat
- [ ] PASS: Skill mandates getting the full commit log (git log --oneline BASE..HEAD) before drafting the title
- [ ] PASS: Skill requires the PR title to follow Conventional Commits format with type, optional scope, imperative mood description under 70 characters
- [ ] PASS: Skill's description template includes Summary, Changes (grouped by area), and Test plan sections — all required
- [ ] PASS: Skill stops if the current branch is main — PRs must come from feature branches
- [ ] PASS: Skill checks for uncommitted changes and asks the user whether to commit them first rather than silently ignoring them
- [ ] PASS: Skill uses gh pr create and verifies creation via gh pr view after pushing
- [ ] PARTIAL: Skill handles edge cases including draft PRs (--draft flag), single-commit branches, and branches with many small commits
