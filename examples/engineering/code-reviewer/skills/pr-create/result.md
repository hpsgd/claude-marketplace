# Pr Create

Scenario: Checking that the pr-create skill analyses ALL commits on a branch (not just the latest), produces a conventional commit title, and writes a structured description with a usable test plan.

## Prompt

> Review the pr-create skill definition and verify it produces well-formed pull requests that give reviewers sufficient context.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Here's my review of the `pr-create` skill (both versions are identical at 1.7.6):

---

## Findings

### Blocking

**1. `$ARGUMENTS` is not a shell variable (line 20)**
```bash
BASE_BRANCH="${ARGUMENTS:-main}"
```
`$ARGUMENTS` is a template placeholder the skill runtime substitutes, but the `git rev-parse` command on line 23 is real shell. The skill conflates pseudo-code with executable commands without labelling the distinction. If an agent runs these literally, `$ARGUMENTS` expands to empty and the verify command fails silently.

**2. No `git fetch origin` before diffing (Step 3)**
If the local base branch is behind remote (common in active repos), the diff against a stale `$BASE_BRANCH` silently omits commits added to base since the last fetch. The "read ALL commits" instruction becomes unreliable without this.

---

### Should-fix

**3. Imperative-mood examples contradict the casing rule (lines 84–94)**
Line 84 says: *"Imperative mood: 'Add', 'Fix', 'Refactor'"* (capitalised). Line 86 says: *"Lowercase after the colon."* The examples then show `add`, `prevent`, `extract` (lowercase). The rule conflicts with the mnemonic.

Suggested fix: Change line 84 to `"add", "fix", "refactor"` — the conventional commits standard is lowercase.

**4. No confirm-before-push step (Step 6)**
The skill drafts title and body then immediately pushes and creates the PR. The user's feedback rule (`learned--confirm-before-launching-agents`) flags premature consequential actions. A pause between Step 5 and Step 6 — showing the draft and asking "ready to push?" — is consistent with that preference and gives the author a final review.

**5. Draft PR handling buried in Edge Cases, not in Step 6 (line 187)**
An agent following steps linearly will push as non-draft and then need to convert. Move draft detection into Step 6's logic: *"If the user requested a draft, add `--draft`."*

**6. "Fill every section" conflicts with trivial changes (line 103)**
The Edge Cases section handles draft and cross-repo PRs but not "no meaningful test plan" (e.g., docs-only changes). Forcing a Test plan section for a typo fix produces filler. Add a note: *"For documentation-only or non-functional changes, the test plan may be 'N/A — no runtime behaviour changed'."*

---

### Nit

**7. No guidance for large diffs (line 66)**
*"If there are 20 changed files, read all 20"* — no guidance for 100+ file PRs, generated files, or lockfiles. A note like *"Skip generated files and lockfiles; focus on hand-written code"* would prevent wasted context.

**8. `🤖 Generated with [Claude Code]` footer absent**
The system-level PR template includes this footer. The skill omits it. Likely intentional (the skill owns the format), but worth confirming whether you want the footer on skill-created PRs for consistency.

---

**Bottom line:** The skill produces structurally sound PRs with good reviewer context — the description template, title rules, and "read everything" instruction are all solid. The two blocking issues (shell variable ambiguity, stale base branch) can produce silently wrong output. The confirm-before-push gap is the most practically impactful should-fix given your stated preferences.

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 9.0/15.5 (58%) |
| Evaluated | 2026-04-30 |
| Target duration | 94907 ms |
| Target cost | $0.3869 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill explicitly requires reading every changed file in the diff — "if there are 20 changed files, read all 20" — not just the diffstat | PASS | Nit #7 directly quotes the skill: "'If there are 20 changed files, read all 20' — no guidance for 100+ file PRs" confirming the rule exists. |
| c2 | Skill mandates getting the full commit log (git log --oneline BASE..HEAD) before drafting the title | PARTIAL | Blocking issue #2 references "The 'read ALL commits' instruction becomes unreliable without this [git fetch]" — confirms an all-commits instruction exists but never quotes the specific git log command or confirms it runs before title drafting. |
| c3 | Skill requires the PR title to follow Conventional Commits format with type, optional scope, imperative mood description under 70 characters | PASS | Should-fix #3 describes lines 84–94 in detail: "Imperative mood: 'Add', 'Fix', 'Refactor'", "Lowercase after the colon", and references "the conventional commits standard" — confirming CC format is required by the skill. |
| c4 | Skill's description template includes Summary, Changes (grouped by area), and Test plan sections — all required | PARTIAL | Should-fix #6 explicitly names "Test plan section". The bottom line calls "the description template… solid" but neither Summary nor Changes (grouped by area) are named as sections. |
| c5 | Skill stops if the current branch is main — PRs must come from feature branches | FAIL | No mention anywhere in the captured output of a main-branch guard or any safety check that prevents PRs from the default branch. |
| c6 | Skill checks for uncommitted changes and asks the user whether to commit them first rather than silently ignoring them | FAIL | No mention of uncommitted-changes detection or any prompt to the user about staging/committing before creating the PR. |
| c7 | Skill uses gh pr create and verifies creation via gh pr view after pushing | PARTIAL | Should-fix #4 says "The skill drafts title and body then immediately pushes and creates the PR" — implying gh pr create is used. No mention of gh pr view or gh pr list post-creation verification. |
| c8 | Skill handles edge cases including draft PRs (--draft flag), single-commit branches, and branches with many small commits | PARTIAL | Should-fix #5 confirms draft PR handling exists in Edge Cases (line 187). Single-commit branches and branches with many small commits are not mentioned anywhere in the output. |
| c9 | Output is structured as a verification of the skill (verdict per requirement) rather than producing a sample PR | PASS | The output is structured as a code-review-style analysis with Blocking / Should-fix / Nit categories and a Bottom line verdict — clearly a verification, not a sample PR. |
| c10 | Output confirms the read-every-changed-file rule explicitly, quoting or paraphrasing "if there are 20 changed files, read all 20" | PASS | Nit #7 directly quotes: "'If there are 20 changed files, read all 20'" and discusses the gap for 100+ file PRs. |
| c11 | Output verifies the requirement to run `git log --oneline BASE..HEAD` (or equivalent full-commit-history fetch) before drafting the title — and that the title reflects all commits, not just HEAD | PARTIAL | Blocking issue #2 references the "read ALL commits" instruction and a stale base risk, implying all-commit history is required. Neither the specific git log command nor the link between full history and title drafting is confirmed. |
| c12 | Output confirms the Conventional Commits format requirement with type, optional scope, imperative mood, under 70 characters | PARTIAL | Should-fix #3 confirms imperative mood and CC lowercase standard. Optional scope and the 70-character limit are not mentioned anywhere in the output. |
| c13 | Output verifies the description template includes Summary, Changes (grouped by area), and Test plan — all named as required sections | PARTIAL | Should-fix #6 explicitly names "Test plan section". The bottom line calls the description template "solid" but does not name Summary or Changes (grouped by area) as distinct required sections. |
| c14 | Output confirms the safety checks: stop if on `main`, ask the user about uncommitted changes rather than silently ignoring them | FAIL | Neither the main-branch guard nor the uncommitted-changes prompt appears anywhere in the output's findings or confirmations. |
| c15 | Output verifies the workflow uses `gh pr create` and confirms creation via `gh pr view` (or `gh pr list`) — not just declaring success | PARTIAL | Should-fix #4 implies gh pr create is used ("pushes and creates the PR"). No mention of a post-creation verification step via gh pr view or gh pr list. |
| c16 | Output confirms edge-case coverage: draft PRs (--draft), single-commit branches, branches with many small commits | PARTIAL | Should-fix #5 confirms draft PR edge case exists at line 187. Single-commit branches and branches with many small commits are not addressed anywhere in the output. |
| c17 | Output identifies any gaps — e.g. no rule on linking issues with `Closes #N`, no guidance on assigning reviewers, no behaviour defined for branches diverged behind base | PARTIAL | Blocking issue #2 identifies the stale-base-branch gap (branches diverged behind base). Should-fix #4 identifies no confirm-before-push. Should-fix #6 identifies no guidance for trivial-change test plans. None of the criterion's specific examples (Closes #N, reviewer assignment) are raised. |

### Notes

The captured output is a technically competent review that identifies real issues (stale base branch, shell variable ambiguity, draft PR placement). However, it largely fails to confirm the specific safety checks the criteria care about most: the main-branch guard (c5), uncommitted-changes prompt (c6), and post-creation gh pr view verification (c15) are entirely absent. The reviewer confirms the all-commits instruction exists (c2, c11) only indirectly, and confirms the description template (c4, c13) only partially — naming Test plan but not Summary or Changes. The score lands at 58% (9.0/15.5), narrowly below the 60% PARTIAL threshold, primarily because c5, c6, and c14 score zero and most partial confirmations are incomplete.
