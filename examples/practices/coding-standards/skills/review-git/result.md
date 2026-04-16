# Review git non conventional commits

A developer asks for a git review of their feature branch before raising a PR. Several commits use past tense, one has no type prefix, and the PR description is missing a test plan.

## Prompt

> Can you review my branch `feature/user-notifications` before I raise a PR? The last 4 commits are:
> - `Updated the email template for welcome messages`
> - `fix: sending duplicate emails when user registers twice`
> - `Added rate limiting to the notification endpoint`  
> - `wip: still working on the push notification handler`
>
> The PR title is "User notification improvements" and the description just says "Various improvements to how we send notifications to users."

```markdown

## Output

### Git Review

#### Summary
- Commits reviewed: 4
- Commit format: 3 findings
- PR standards: 2 findings
- Branch model: 0 findings
- Content dates: N/A
- Commit hygiene: 1 finding

#### Findings

##### IMPORTANT [Pass 1]: Missing conventional commit type prefix


| Field | Value |
|---|---|
| Commit | `Updated the email template for welcome messages` |
| Evidence | No `type:` prefix. Does not match `<type>[optional scope]: <description>` |
| Convention | Every commit must start with a valid type (feat, fix, docs, style, refactor, test, chore, ci, perf, build, revert) |
| Fix | `docs: update email template for welcome messages` or `feat: update welcome email template` |


---

##### IMPORTANT [Pass 1]: Past tense subject line — "Updated..."


| Field | Value |
|---|---|
| Commit | `Updated the email template for welcome messages` |
| Evidence | "Updated" — past tense |
| Convention | Imperative mood required. "Add feature" not "Added feature" |
| Fix | `docs: update email template for welcome messages` |


---

##### IMPORTANT [Pass 1]: Past tense subject line and missing type — "Added..."


| Field | Value |
|---|---|
| Commit | `Added rate limiting to the notification endpoint` |
| Evidence | "Added" — past tense; no type prefix |
| Convention | Imperative mood + conventional commit type required |
| Fix | `feat: add rate limiting to notification endpoint` |


---

##### IMPORTANT [Pass 2]: PR title missing conventional commit type prefix


| Field | Value |
|---|---|
| PR field | title — "User notification improvements" |
| Evidence | No type prefix. The PR title becomes the squash commit message. |
| Convention | PR title must match conventional commit format |
| Fix | `feat: improve user notification delivery` |


---

##### IMPORTANT [Pass 2]: PR description missing test plan


| Field | Value |
|---|---|
| PR field | description — "Various improvements to how we send notifications to users." |
| Evidence | No test plan section. Missing what changed, why, and how to verify. |
| Convention | Description must include: what changed, why, and a test plan |
| Fix | Add sections — What changed: ..., Why: ..., Test plan: run `npm test notifications`, verify welcome email sends once on new registration |


---

##### SUGGESTION [Pass 5]: WIP commit in branch history


| Field | Value |
|---|---|
| Commit | `wip: still working on the push notification handler` |
| Evidence | "wip" is not in the valid type list; subject signals incomplete work |
| Convention | WIP commits are acceptable in branch history in a squash-merge workflow. The final squash commit message must not be "wip:..." |
| Fix | Confirm the squash commit message will be something like `feat: add push notification handler` before raising the PR. |


#### Clean Areas

`fix: sending duplicate emails...` uses the correct type prefix. Branch name `feature/user-notifications` follows the `feature/description` convention.
```

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/7.5 (100%) |
| Evaluated | 2026-04-16 |


- [x] PASS: All five mandatory passes executed — the definition states "Execute all five passes. Every finding requires the specific commit hash or PR field that violates the convention." All five passes have explicit bash commands; none are optional
- [x] PASS: Past tense commits flagged with specific subject lines — Pass 1 step 3 lists "Fixed", "Updated", "Changed", "Removed" as past tense violations and requires the commit subject line as evidence; "Updated" and "Added" match directly
- [x] PASS: Missing type prefix flagged — Pass 1 step 2 defines the full list of valid types and states "Anything else (update, change, wip, misc, stuff) is a finding"; a bare description with no type prefix is a clear finding under this rule
- [x] PASS: WIP commit flagged as Pass 5 hygiene finding — Pass 5 step 1 explicitly lists "wip" in the grep target and states "acceptable in the branch history but must not survive as the final squash commit message" — exact match to the criterion language
- [x] PASS: PR title flagged for missing type — Pass 2 step 1 states "Apply the same type, imperative mood, and length rules from Pass 1" to PR titles; the title "User notification improvements" has no type prefix
- [x] PASS: Missing test plan flagged as Pass 2 finding — Pass 2 step 3 lists three required sections (what changed, why, test plan) and states "Missing any of these three sections is a finding"
- [x] PASS: Output uses the defined summary template — the Output Template section defines exactly the per-pass summary counts structure that the simulated output follows
- [~] PARTIAL: Concrete rewrites included — the Evidence Format defines a "Fix" field described as "concrete rewording or action." The field is part of the mandatory evidence structure, so fixes are required. The criterion is PARTIAL-prefixed regardless; credit for the Fix field being mandated in the format

### Notes

The definition is strong. Pass 1 enumerates every common past-tense violation form. Pass 2 names the three required PR description sections explicitly. The WIP-in-squash nuance in Pass 5 is precise — it correctly distinguishes between branch history (acceptable) and the final squash commit (not acceptable). The `fix: sending duplicate emails` commit is a subtle case: it has the right type prefix but the description describes the bug rather than the fix. The definition's imperative mood check in Pass 1 would catch "sending" as a gerund, so the skill would surface this too — good depth.
