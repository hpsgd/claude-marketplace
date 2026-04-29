# Output: pr-create skill structure

**Verdict:** PASS
**Score:** 16.5/17 criteria met (97%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill explicitly requires reading every changed file — met. Step 3.3 reads: "Do not skim. If there are 20 changed files, read all 20."
- [x] PASS: Skill mandates `git log --oneline BASE..HEAD` before drafting the title — met. Step 3.1 runs `git log --oneline $BASE_BRANCH..HEAD`; Step 4 (title drafting) is sequenced after.
- [x] PASS: Skill requires PR title to follow Conventional Commits with type, optional scope, imperative mood, under 70 characters — met. Step 4 rules state all four constraints explicitly, with positive and negative examples.
- [x] PASS: Skill's description template includes Summary, Changes (grouped by area), and Test plan — met. Step 5 template has all three named sections; "Fill every section" makes them mandatory. Changes annotated "Grouped by area: API, UI, database, tests, config, etc."
- [x] PASS: Skill stops if current branch is main — met. Step 2.2: "If on `main` (or the base branch), stop. PRs come from feature branches."
- [x] PASS: Skill checks for uncommitted changes and asks the user rather than silently ignoring them — met. Step 2.1 runs `git status --short` and instructs: "stop and ask the user whether to commit them first or proceed without them. Do not silently ignore uncommitted work."
- [x] PASS: Skill uses `gh pr create` and verifies creation via `gh pr view` after pushing — met. Step 6 runs `gh pr create` then `gh pr view --json url,title,state` in sequence.
- [~] PARTIAL: Skill handles edge cases including draft PRs (`--draft` flag), single-commit branches, and branches with many small commits — partially met. All three cases are addressed in the Edge Cases section with explicit guidance. Scored 0.5 per PARTIAL rules.

### Output expectations

- [x] PASS: Output is structured as a verification of the skill (verdict per requirement) rather than producing a sample PR — met. This result lists verdicts per criterion against the skill definition.
- [x] PASS: Output confirms the read-every-changed-file rule, quoting or paraphrasing "if there are 20 changed files, read all 20" — met. Criterion 1 above quotes the exact line.
- [x] PASS: Output verifies the requirement to run `git log --oneline BASE..HEAD` before drafting the title, and that the title reflects all commits not just HEAD — met. Criterion 2 confirms the command and its sequencing before Step 4.
- [x] PASS: Output confirms the Conventional Commits format requirement with type, optional scope, imperative mood, under 70 characters — met. Criterion 3 confirms all four constraints.
- [x] PASS: Output verifies the description template includes Summary, Changes (grouped by area), and Test plan — all named as required sections — met. Criterion 4 confirms all three with the "grouped by area" annotation.
- [x] PASS: Output confirms the safety checks: stop if on `main`, ask the user about uncommitted changes rather than silently ignoring them — met. Criteria 5 and 6 confirm both.
- [x] PASS: Output verifies the workflow uses `gh pr create` and confirms creation via `gh pr view` — not just declaring success — met. Criterion 7 confirms both commands and the json flag.
- [x] PASS: Output confirms edge-case coverage: draft PRs (`--draft`), single-commit branches, branches with many small commits — met. Criterion 8 confirms all three.
- [~] PARTIAL: Output identifies any gaps — e.g. no rule on linking issues with `Closes #N`, no guidance on assigning reviewers, no behaviour defined for branches diverged behind base — partially met. Gaps identified below in Notes.

## Notes

The skill is well-constructed across every binary criterion. The mandatory-process framing, the explicit "do not silently ignore" instruction for uncommitted changes, and the read-all-files rule are notably strong.

Gaps identified (for the PARTIAL output criterion):

- **Issue linking.** `Closes #[issue number]` appears only in an optional "Related issues" template block. There is no instruction to check whether a related issue exists and add the closing reference. A practitioner creating a PR for a tracked issue would miss this without prompting.
- **Reviewer assignment.** The skill has no mention of `--reviewer` or any guidance on who should review the PR. In team contexts this is a routine part of PR creation.
- **Diverged branch.** If the feature branch has diverged behind the base (i.e., base has moved forward), `git push` will succeed but the PR may need a rebase before it can merge. The skill does not check for this condition or instruct the user to rebase first.

The PARTIAL score on criterion 8 (edge cases) reflects the scoring rule, not missing substance — all three listed cases are covered in the skill.
