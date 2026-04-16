# Pr create skill structure

Checking that the pr-create skill analyses ALL commits on a branch (not just the latest), produces a conventional commit title, and writes a structured description with a usable test plan.

## Prompt

> Review the pr-create skill definition and verify it produces well-formed pull requests that give reviewers sufficient context.

Structural assessment of `plugins/engineering/code-reviewer/skills/pr-create/SKILL.md`.

The SKILL.md defines a mandatory 7-step process. Step 3 explicitly states "Do not skim. If there are 20 changed files, read all 20." Step 3 also runs `git log --oneline $BASE_BRANCH..HEAD` as its first sub-step. Step 4 specifies Conventional Commits format with type, optional scope, imperative mood, and <70 character limit. Step 5 description template has Summary, Changes, and Test plan sections with "Fill every section" making them all required. Step 2 checks for uncommitted changes and stops if on main. Step 6 runs `gh pr create` then `gh pr view`. An Edge Cases section covers draft PRs (`--draft`), single-commit branches, and branches with many small commits.

## Output



## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/8 criteria met (94%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Skill explicitly requires reading every changed file — Step 3 states verbatim: "Do not skim. If there are 20 changed files, read all 20." This is a hard instruction, not a suggestion.

- [x] PASS: Skill mandates full commit log before drafting title — Step 3 sub-step 1 runs `git log --oneline $BASE_BRANCH..HEAD` before Step 4 (drafting the title). The sequence enforces commit log review before title writing.

- [x] PASS: Skill requires Conventional Commits format with all constraints — Step 4 specifies: type (required), optional scope in parentheses, imperative mood, lowercase after the colon, and <70 characters total. All four constraints in the criterion are explicitly stated.

- [x] PASS: Skill's description template includes all three required sections — Step 5 template shows Summary, Changes (grouped by area), and Test plan as named sections. The instruction "Fill every section" makes all three required, not optional.

- [x] PASS: Skill stops if on main — Step 2, sub-step 2: "If on `main` (or the base branch), stop. PRs come from feature branches." The stop instruction is explicit.

- [x] PASS: Skill checks for uncommitted changes and asks user — Step 2, sub-step 1: "If there are uncommitted changes, stop and ask the user whether to commit them first or proceed without them. Do not silently ignore uncommitted work." Both the check and the ask are required.

- [x] PASS: Skill uses gh pr create and verifies with gh pr view — Step 6 sub-steps show both commands with their exact flags. The definition requires verification after creation, not just creation.

- [~] PARTIAL: Skill handles draft PRs, single-commit, and many small commits — Edge Cases section covers all three: draft PRs (`--draft` flag when user says "draft" or "WIP"), single-commit branches (use the commit message directly), and many small commits (summarise the overall change rather than listing commits). Coverage is present but in prose notes rather than structured decision rules; the draft PR handling is the most actionable, the others are guidance-level only.

## Notes

The "Fill every section" instruction in Step 5 is the right mechanism to make template sections mandatory without labelling each one explicitly. The edge cases section reads as informational rather than enforced — a developer following the skill could miss the single-commit or many-commits guidance without consequence, since neither is tied to a decision rule or stop condition. Adding a conditional step ("if only one commit on the branch...") would tighten this. The Step 3 read-all-files instruction is notably strong — most PR creation processes skip file reading entirely.
