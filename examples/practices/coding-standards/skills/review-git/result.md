# Review Git

Scenario: A developer asks for a git review of their feature branch before raising a PR. Several commits use past tense, one has no type prefix, and the PR description is missing a test plan.

## Prompt

> Can you review my branch `feature/user-notifications` before I raise a PR? The last 4 commits are:
> - `Updated the email template for welcome messages`
> - `fix: sending duplicate emails when user registers twice`
> - `Added rate limiting to the notification endpoint`  
> - `wip: still working on the push notification handler`
> 
> The PR title is "User notification improvements" and the description just says "Various improvements to how we send notifications to users."

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Git Review

### Summary
- Commits reviewed: 4
- Commit format: 5 findings
- PR standards: 3 findings
- Branch model: 0 findings
- Content dates: N/A
- Commit hygiene: 1 finding

---

### Findings

#### CRITICAL — Commit Hygiene: WIP commit must not reach main

**Commit:** `wip: still working on the push notification handler`
**Evidence:** Subject begins with `wip:`, description says "still working on"
**Convention:** WIP commits signal incomplete work. This must be finished and rewritten before the PR is raised — or dropped entirely if the feature isn't ready.
**Fix:** Either finish the work and rewrite as `feat: add push notification handler`, or remove the commit from this branch and raise it separately when done.

---

#### IMPORTANT — Pass 1: Three commits missing conventional commit type

**Commit 1:** `Updated the email template for welcome messages`
**Fix:** `feat: update welcome email template` — or `style:` if only visual/copy changes

**Commit 3:** `Added rate limiting to the notification endpoint`
**Fix:** `feat: add rate limiting to notification endpoint`

**Commit 4:** `wip:` is not a valid type.
**Convention:** Valid types are `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`, `perf`, `build`, `revert`.

---

#### IMPORTANT — Pass 1: Past tense / gerund in subject lines

**Commits:** 1 (`Updated`), 3 (`Added`), 4 (`still working on`)
**Commit 2:** `fix: sending duplicate emails...` — "sending" is a gerund, not imperative.
**Convention:** Subject lines use imperative mood: "Add", "Fix", "Update" — not "Added", "Adds", "Adding".
**Fix for commit 2:** `fix: prevent duplicate emails on repeated user registration`

---

#### IMPORTANT — Pass 2: PR title doesn't follow Conventional Commits

**PR field:** title — `"User notification improvements"`
**Convention:** The PR title becomes the squash commit message. It must match `<type>: <description>` in imperative mood.
**Fix:** `feat: improve user notification delivery` — or be more specific about the primary change.

---

#### IMPORTANT — Pass 2: PR description is incomplete

**PR field:** description — `"Various improvements to how we send notifications to users."`
**Missing:**
- **What changed** — which specific changes are included
- **Why** — the motivation (duplicate emails, rate limit abuse, etc.)
- **Test plan** — how to verify the changes

**Fix:** Expand with all three sections. Example structure:
```
## What changed
- Fixed duplicate email sends on repeated registration
- Added rate limiting to the notification endpoint
- Updated welcome email template

## Why
[Describe the bug/need driving each change]

## Test plan
- [ ] Register the same email twice, confirm single email received
- [ ] Hammer the notification endpoint, confirm 429 responses after threshold
- CI passes
```

---

### Clean Areas

- Branch name `feature/user-notifications` follows the `feature/<description>` convention.
- Commit 2 (`fix:`) correctly uses the `fix` type — the only one that does.

---

**Before raising this PR:** finish or remove the WIP commit, rewrite all four subjects in conventional format with imperative mood, and expand the PR description. The WIP commit alone is a blocker — it signals the branch isn't ready to merge.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.5/15.0 (97%) |
| Evaluated | 2026-05-01 |
| Target duration | 55952 ms |
| Target cost | $0.0987 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill executes all five mandatory passes — does not skip any pass | PASS | Summary explicitly lists all five pass categories: Commit format, PR standards, Branch model (0 findings), Content dates (N/A), Commit hygiene (1 finding). Findings sections reference 'Pass 1' and 'Pass 2' explicitly. |
| c2 | Commits using past tense ("Updated", "Added") are flagged as Pass 1 findings with the specific commit subject line as evidence | PASS | Section 'IMPORTANT — Pass 1: Past tense / gerund in subject lines' lists 'Commits: 1 (`Updated`), 3 (`Added`)' with exact subject line references. |
| c3 | Commit without a type prefix ("Updated the email template...") is flagged as a missing conventional commit type | PASS | Section 'IMPORTANT — Pass 1: Three commits missing conventional commit type' lists 'Commit 1: `Updated the email template for welcome messages`' explicitly. |
| c4 | WIP commit is flagged as a Pass 5 hygiene finding — acceptable in branch history but the final squash commit cannot carry this message | PARTIAL | WIP is flagged under 'CRITICAL — Commit Hygiene' and in the summary ('Commit hygiene: 1 finding'). However, the output does NOT make the distinction that a WIP is acceptable in branch history — it treats it as a complete blocker: 'This must be finished and rewritten before the PR is raised — or dropped entirely.' The squash-commit-specific nuance is absent. |
| c5 | PR title "User notification improvements" is flagged for lacking a conventional commit type prefix | PASS | Section 'IMPORTANT — Pass 2: PR title doesn't follow Conventional Commits' cites exact PR field: title — `"User notification improvements"` and states 'It must match `<type>: <description>`'. |
| c6 | PR description missing a test plan is flagged as a Pass 2 finding | PASS | Section 'IMPORTANT — Pass 2: PR description is incomplete' lists 'Test plan — how to verify the changes' under Missing items. |
| c7 | Output uses the defined summary template with per-pass finding counts | PASS | Summary block lists: 'Commit format: 5 findings / PR standards: 3 findings / Branch model: 0 findings / Content dates: N/A / Commit hygiene: 1 finding' — per-pass counts including zero-finding passes. |
| c8 | Each finding includes a concrete rewrite suggestion, not just identification of the problem | PARTIAL | Each finding includes a concrete Fix line: `feat: update welcome email template`, `feat: add rate limiting to notification endpoint`, `fix: prevent duplicate emails on repeated user registration`, `feat: improve user notification delivery`, and an expanded PR description example with checkboxes. |
| c9 | Output flags both past-tense commits — `Updated the email template for welcome messages` and `Added rate limiting to the notification endpoint` — by exact subject line, with the imperative-mood rewrite suggestion (`docs: update welcome email template`, `feat: add rate limiting to notification endpoint`) | PASS | Both commits cited by exact subject in 'Pass 1: Past tense / gerund'. Imperative rewrites given: `feat: update welcome email template` (or `style:`) and `feat: add rate limiting to notification endpoint`. Type differs slightly from criterion's `docs:` example but imperative form and exact subject lines are present. |
| c10 | Output flags the missing type prefix on `Updated the email template for welcome messages` — and assigns a specific Conventional Commits type (e.g. `docs:` if this is a copy change, `feat:` if it's a behavioural change), with reasoning | PASS | 'Fix: `feat: update welcome email template` — or `style:` if only visual/copy changes' — assigns type with conditional reasoning distinguishing behavioral vs copy change. |
| c11 | Output identifies `wip: still working on the push notification handler` as a Pass 5 hygiene finding — acceptable in branch history but unacceptable as the squash commit message — with the recommendation to rewrite or squash before merge | PARTIAL | Exact subject line is cited. Rewrite recommendation is given: 'rewrite as `feat: add push notification handler`'. However, the output omits the 'acceptable in branch history / unacceptable as squash commit' distinction entirely — treating it as an outright blocker rather than a squash-specific concern. |
| c12 | Output flags the PR title `User notification improvements` for missing the conventional commit prefix and being too vague — recommending `feat: add user notification system` or `feat(notifications): add rate-limited email and push delivery` | PARTIAL | Missing prefix is explicitly flagged. The 'too vague' aspect is only lightly touched: 'or be more specific about the primary change' — not called out explicitly. Suggested fix `feat: improve user notification delivery` differs from the criterion's expected specifics and doesn't match the recommended alternatives in specificity. |
| c13 | Output flags the PR description's missing test plan as a Pass 2 finding — with a concrete suggestion of what the test plan should include (manual verification steps, test cases covered, deploy notes) | PASS | Pass 2 finding lists missing test plan. Example provided includes manual steps: '- [ ] Register the same email twice, confirm single email received / - [ ] Hammer the notification endpoint, confirm 429 responses after threshold / - CI passes'. Deploy notes absent but manual verification and test cases are concrete. |
| c14 | Output executes all five mandatory passes and reports per-pass finding counts in the summary, including passes with zero findings | PASS | Summary explicitly includes 'Branch model: 0 findings' (zero-finding pass) and 'Content dates: N/A' alongside the passes with findings. |
| c15 | Output's findings each cite the exact subject line or PR text as evidence — not paraphrased — so the developer can find the offending content | PASS | WIP commit: backtick-quoted verbatim. PR title: `"User notification improvements"` in quotes. PR description: `"Various improvements to how we send notifications to users."` in quotes. Commit subjects quoted throughout findings sections. |
| c16 | Output provides concrete rewrite suggestions per finding, not just identification — e.g. for the past-tense commits, the rewritten imperative version is shown verbatim | PASS | Verbatim rewrites given for every finding: `feat: update welcome email template`, `feat: add rate limiting to notification endpoint`, `fix: prevent duplicate emails on repeated user registration`, `feat: improve user notification delivery`, and full PR description block example. |
| c17 | Output's PR-description recommendation aligns with the project's PR template (Summary, Changes, Test plan) and points to the Conventional Commits + project README convention rather than a generic format | PARTIAL | Output provides a structured template ('What changed / Why / Test plan') that approximates the Summary+Changes+Test plan structure but uses non-standard section names and does not reference the project README or Conventional Commits spec explicitly. |

### Notes

The output is thorough and well-structured, covering all five passes with per-pass counts, exact evidence citations, and concrete rewrites for every finding. The main gaps are: (1) the WIP commit nuance — the output treats it as a complete blocker rather than flagging that WIP is acceptable in branch history but must not appear in the squash commit message (affects c4 and c11); (2) the PR title's 'too vague' aspect is only lightly addressed rather than explicitly called out (c12). Everything else — imperative mood, type prefixes with reasoning, test plan example, zero-finding pass reporting — is handled well.
