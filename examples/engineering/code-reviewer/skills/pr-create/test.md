# Test: pr-create skill structure

Scenario: Checking that the pr-create skill analyses ALL commits on a branch (not just the latest), produces a conventional commit title, and writes a structured description with a usable test plan.

## Prompt

Review the pr-create skill definition and verify it produces well-formed pull requests that give reviewers sufficient context.

In your verification report, confirm or flag each of the following items by name. Quote skill text where present:

- **Full commit history**: `git log --oneline BASE..HEAD` mandated before drafting the title; title must reflect ALL commits, not just HEAD.
- **Conventional Commits format**: type, optional scope, imperative mood, **under 70 characters** — all four named.
- **Description template sections**: **Summary**, **Changes (grouped by area)**, **Test plan** — all three named as required.
- **Safety checks (2)**: (1) **stop if current branch is `main`**, (2) **detect uncommitted changes and ask the user** before proceeding.
- **Workflow verification**: uses `gh pr create` AND verifies creation via `gh pr view` (or `gh pr list`) post-push.
- **Edge cases (3)**: (1) **draft PRs** (`--draft` flag), (2) **single-commit branches**, (3) **branches with many small commits**.
- **Identified gaps**: explicitly call out any of: no rule on linking issues with `Closes #N`, no guidance on assigning reviewers, no defined behaviour for branches diverged behind base.

Confirm or flag each by name — do not paraphrase.

## Criteria

- [ ] PASS: Skill explicitly requires reading every changed file in the diff — "if there are 20 changed files, read all 20" — not just the diffstat
- [ ] PASS: Skill mandates getting the full commit log (git log --oneline BASE..HEAD) before drafting the title
- [ ] PASS: Skill requires the PR title to follow Conventional Commits format with type, optional scope, imperative mood description under 70 characters
- [ ] PASS: Skill's description template includes Summary, Changes (grouped by area), and Test plan sections — all required
- [ ] PASS: Skill stops if the current branch is main — PRs must come from feature branches
- [ ] PASS: Skill checks for uncommitted changes and asks the user whether to commit them first rather than silently ignoring them
- [ ] PASS: Skill uses gh pr create and verifies creation via gh pr view after pushing
- [ ] PARTIAL: Skill handles edge cases including draft PRs (--draft flag), single-commit branches, and branches with many small commits

## Output expectations

- [ ] PASS: Output is structured as a verification of the skill (verdict per requirement) rather than producing a sample PR
- [ ] PASS: Output confirms the read-every-changed-file rule explicitly, quoting or paraphrasing "if there are 20 changed files, read all 20"
- [ ] PASS: Output verifies the requirement to run `git log --oneline BASE..HEAD` (or equivalent full-commit-history fetch) before drafting the title — and that the title reflects all commits, not just HEAD
- [ ] PASS: Output confirms the Conventional Commits format requirement with type, optional scope, imperative mood, under 70 characters
- [ ] PASS: Output verifies the description template includes Summary, Changes (grouped by area), and Test plan — all named as required sections
- [ ] PASS: Output confirms the safety checks: stop if on `main`, ask the user about uncommitted changes rather than silently ignoring them
- [ ] PASS: Output verifies the workflow uses `gh pr create` and confirms creation via `gh pr view` (or `gh pr list`) — not just declaring success
- [ ] PASS: Output confirms edge-case coverage: draft PRs (--draft), single-commit branches, branches with many small commits
- [ ] PARTIAL: Output identifies any gaps — e.g. no rule on linking issues with `Closes #N`, no guidance on assigning reviewers, no behaviour defined for branches diverged behind base
