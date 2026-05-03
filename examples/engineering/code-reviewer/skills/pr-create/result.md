# Pr Create

Scenario: Checking that the pr-create skill analyses ALL commits on a branch (not just the latest), produces a conventional commit title, and writes a structured description with a usable test plan.

## Prompt

> Review the pr-create skill definition and verify it produces well-formed pull requests that give reviewers sufficient context.
> 
> In your verification report, confirm or flag each of the following items by name. Quote skill text where present:
> 
> - **Full commit history**: `git log --oneline BASE..HEAD` mandated before drafting the title; title must reflect ALL commits, not just HEAD.
> - **Conventional Commits format**: type, optional scope, imperative mood, **under 70 characters** — all four named.
> - **Description template sections**: **Summary**, **Changes (grouped by area)**, **Test plan** — all three named as required.
> - **Safety checks (2)**: (1) **stop if current branch is `main`**, (2) **detect uncommitted changes and ask the user** before proceeding.
> - **Workflow verification**: uses `gh pr create` AND verifies creation via `gh pr view` (or `gh pr list`) post-push.
> - **Edge cases (3)**: (1) **draft PRs** (`--draft` flag), (2) **single-commit branches**, (3) **branches with many small commits**.
> - **Identified gaps**: explicitly call out any of: no rule on linking issues with `Closes #N`, no guidance on assigning reviewers, no defined behaviour for branches diverged behind base.
> 
> Confirm or flag each by name — do not paraphrase.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I've reviewed the pr-create skill definition. Here's my verification report:

## Confirmed ✓

**Full commit history**: 
- ✓ Line 54: `git log --oneline $BASE_BRANCH..HEAD` mandated in Step 3
- ✓ Line 9: "analyses ALL commits on the branch (not just the latest)"
- ✓ Line 176: Common mistake explicitly lists "Describing only the last commit"

**Conventional Commits format**: 
- ✓ Line 76-80: Format defined as `<type>[optional scope]: <description>`
- ✓ Line 84: "Under 70 characters total"
- ✓ Line 84: Imperative mood rule named with examples
- ✓ All four elements explicitly named

**Description template sections**: 
- ✓ Line 106: `## Summary`
- ✓ Line 111: `## Changes` with "Grouped by area"
- ✓ Line 116: `## Test plan`
- ✓ All three named as required

**Safety checks (2)**: 
- ✓ Line 36-40: "If on `main` (or the base branch), stop"
- ✓ Line 30-34: "If there are uncommitted changes, stop and ask the user"

**Workflow verification**: 
- ✓ Line 151: `gh pr create` used
- ✓ Line 160: `gh pr view --json url,title,state` verifies post-creation

**Edge cases (3)**: 
- ✓ Line 187: Draft PRs (`--draft` flag)
- ✓ Line 185: Single-commit branches
- ✓ Line 186: Many small commits ("Summarise the overall change")

## Flagged Gaps

**Gap 1: No mandate that PR title must reflect ALL commits** — Step 4 doesn't explicitly state the title must synthesise all commits into one coherent statement. The template shows analysis of all commits, but the title drafting guidance doesn't enforce this constraint. Line 176 warns against *describing only the last commit*, but doesn't mandate the title itself summarize the full scope.

**Gap 2: No guidance on assigning reviewers** — The skill contains no mention of reviewer selection, assignment strategy, or how to populate the `--reviewer` flag in `gh pr create`.

**Gap 3: No rule linking issues with `Closes #N`** — Line 133 shows the template section `Closes #[issue number]`, but there's no explicit rule requiring issue linkage or auto-detection of issue numbers from commits. It appears as optional boilerplate, not a mandatory convention.

**Gap 4: No guidance on branches diverged behind base** — If the feature branch is behind the base branch (requires rebase), there's no defined behaviour. Step 2 checks tracking but doesn't address divergence or stale branches.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.0/16.0 (88%) |
| Evaluated | 2026-05-03 |
| Target duration | 33609 ms |
| Target cost | $0.1169 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill explicitly requires reading every changed file in the diff — "if there are 20 changed files, read all 20" — not just the diffstat | FAIL | The captured output contains no mention of reading every changed file in the diff, nor any paraphrase of 'if there are 20 changed files, read all 20'. The report covers commit history, conventional commits, template sections, safety checks, workflow, edge cases, and gaps — but the diff-reading rule is entirely absent. |
| c2 | Skill mandates getting the full commit log (git log --oneline BASE..HEAD) before drafting the title | PASS | Output confirms: '✓ Line 54: `git log --oneline $BASE_BRANCH..HEAD` mandated in Step 3' and '✓ Line 9: "analyses ALL commits on the branch (not just the latest)"'. |
| c3 | Skill requires the PR title to follow Conventional Commits format with type, optional scope, imperative mood description under 70 characters | PASS | Output confirms all four elements: '✓ Line 76-80: Format defined as `<type>[optional scope]: <description>`', '✓ Line 84: "Under 70 characters total"', '✓ Line 84: Imperative mood rule named with examples', '✓ All four elements explicitly named'. |
| c4 | Skill's description template includes Summary, Changes (grouped by area), and Test plan sections — all required | PASS | Output confirms: '✓ Line 106: `## Summary`', '✓ Line 111: `## Changes` with "Grouped by area"', '✓ Line 116: `## Test plan`', '✓ All three named as required'. |
| c5 | Skill stops if the current branch is main — PRs must come from feature branches | PASS | Output confirms: '✓ Line 36-40: "If on `main` (or the base branch), stop"'. |
| c6 | Skill checks for uncommitted changes and asks the user whether to commit them first rather than silently ignoring them | PASS | Output confirms: '✓ Line 30-34: "If there are uncommitted changes, stop and ask the user"'. |
| c7 | Skill uses gh pr create and verifies creation via gh pr view after pushing | PASS | Output confirms: '✓ Line 151: `gh pr create` used' and '✓ Line 160: `gh pr view --json url,title,state` verifies post-creation'. |
| c8 | Skill handles edge cases including draft PRs (--draft flag), single-commit branches, and branches with many small commits | PARTIAL | Output confirms all three: '✓ Line 187: Draft PRs (`--draft` flag)', '✓ Line 185: Single-commit branches', '✓ Line 186: Many small commits ("Summarise the overall change")'. Ceiling is PARTIAL so maximum is 0.5. |
| c9 | Output is structured as a verification of the skill (verdict per requirement) rather than producing a sample PR | PASS | The captured output is explicitly a verification report structured with '## Confirmed ✓' and '## Flagged Gaps' sections, each item keyed to a named requirement from the prompt — no sample PR is produced. |
| c10 | Output confirms the read-every-changed-file rule explicitly, quoting or paraphrasing "if there are 20 changed files, read all 20" | FAIL | The captured output contains no mention of a rule requiring every changed file to be read, nor any paraphrase of the '20 changed files' formulation. This dimension is entirely missing from the verification report. |
| c11 | Output verifies the requirement to run `git log --oneline BASE..HEAD` (or equivalent full-commit-history fetch) before drafting the title — and that the title reflects all commits, not just HEAD | PASS | Output confirms '✓ Line 54: `git log --oneline $BASE_BRANCH..HEAD` mandated in Step 3' and '✓ Line 9: "analyses ALL commits on the branch (not just the latest)"'. Gap 1 also explicitly flags that 'Step 4 doesn't explicitly state the title must synthesise all commits into one coherent statement', addressing both dimensions of the criterion. |
| c12 | Output confirms the Conventional Commits format requirement with type, optional scope, imperative mood, under 70 characters | PASS | Output confirms all four named elements: format pattern at lines 76-80, '"Under 70 characters total"' at line 84, imperative mood at line 84, and states '✓ All four elements explicitly named'. |
| c13 | Output verifies the description template includes Summary, Changes (grouped by area), and Test plan — all named as required sections | PASS | Output confirms '✓ Line 106: `## Summary`', '✓ Line 111: `## Changes` with "Grouped by area"', '✓ Line 116: `## Test plan`', and '✓ All three named as required'. |
| c14 | Output confirms the safety checks: stop if on `main`, ask the user about uncommitted changes rather than silently ignoring them | PASS | Output confirms both safety checks: '✓ Line 36-40: "If on `main` (or the base branch), stop"' and '✓ Line 30-34: "If there are uncommitted changes, stop and ask the user"'. |
| c15 | Output verifies the workflow uses `gh pr create` and confirms creation via `gh pr view` (or `gh pr list`) — not just declaring success | PASS | Output confirms '✓ Line 151: `gh pr create` used' and '✓ Line 160: `gh pr view --json url,title,state` verifies post-creation'. |
| c16 | Output confirms edge-case coverage: draft PRs (--draft), single-commit branches, branches with many small commits | PASS | Output confirms all three edge cases by line number: '✓ Line 187: Draft PRs (`--draft` flag)', '✓ Line 185: Single-commit branches', '✓ Line 186: Many small commits ("Summarise the overall change")'. |
| c17 | Output identifies any gaps — e.g. no rule on linking issues with `Closes #N`, no guidance on assigning reviewers, no behaviour defined for branches diverged behind base | PARTIAL | Output identifies four gaps under '## Flagged Gaps': Gap 3 ('No rule linking issues with `Closes #N`'), Gap 2 ('No guidance on assigning reviewers'), and Gap 4 ('No guidance on branches diverged behind base') — all three example gaps named in the criterion are present. Ceiling is PARTIAL so maximum is 0.5. |

### Notes

The output is a well-structured verification report that correctly confirms or flags nearly every named requirement. Two criteria fail: c1 and c10, both concerning the 'read every changed file in the diff' rule (the "if there are 20 changed files, read all 20" formulation). This rule is completely absent from the captured output — neither confirmed, flagged as a gap, nor mentioned in passing. All other requirements are addressed with line-number evidence. The gap identification (c17) is notably thorough, surfacing all three example gaps plus a fourth (title-synthesis ambiguity in Gap 1), which shows the model went beyond the minimum. The overall score is 87.5%, a clear PASS.
