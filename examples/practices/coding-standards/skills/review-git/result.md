# Result: review-git non-conventional commits

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 16/16.5 criteria met (97%) |
| **Evaluated** | 2026-04-30 |

## Output

Simulated output from invoking `/coding-standards:review-git` on branch `feature/user-notifications` with the four commits described in the prompt.

---

## Git Review

### Summary

| Pass | Area | Findings |
|---|---|---|
| Pass 1 | Commit format | 3 findings |
| Pass 2 | PR standards | 2 findings |
| Pass 3 | Branch model | 0 findings |
| Pass 4 | Content dates | N/A |
| Pass 5 | Commit hygiene | 1 finding |
| **Total** | | **6 findings** |

- Commits reviewed: 4
- Branch: `feature/user-notifications`

---

### Findings

#### [IMPORTANT] Pass 1: Missing conventional commit type prefix

**Commit:** `Updated the email template for welcome messages`
**Evidence:** `Updated the email template for welcome messages`
**Convention:** Every commit message must match `<type>[optional scope]: <description>`. This commit has no type prefix.
**Fix:** Determine whether this is a content/copy change or a behavioural change:

- If copy-only (text wording, formatting): `docs: update welcome email template`
- If it changes rendering or sending behaviour: `feat: update welcome email template`

Use `docs:` for template wording changes; `feat:` if this alters what the email does or when it fires.

---

#### [IMPORTANT] Pass 1: Past tense — imperative mood required

**Commit:** `Updated the email template for welcome messages`
**Evidence:** Subject begins with `Updated` (past tense).
**Convention:** Imperative mood required — "Update", not "Updated". See also: missing type prefix finding above.
**Fix:** `docs: update welcome email template` or `feat: update welcome email template`

---

#### [IMPORTANT] Pass 1: Past tense — imperative mood required

**Commit:** `Added rate limiting to the notification endpoint`
**Evidence:** Subject begins with `Added` (past tense). Also missing a type prefix.
**Convention:** Imperative mood required — "Add", not "Added". Type prefix required.
**Fix:** `feat: add rate limiting to notification endpoint`

---

#### [IMPORTANT] Pass 2: PR title missing conventional commit type prefix

**PR field:** title
**Evidence:** `User notification improvements`
**Convention:** The PR title becomes the squash commit message — it must be a valid conventional commit. This title has no type prefix and uses a vague noun phrase rather than imperative mood.
**Fix:** `feat: add user notification system` or more precisely: `feat(notifications): add rate-limited email and push delivery`

The current title would produce a squash commit that violates the entire commit log convention.

---

#### [IMPORTANT] Pass 2: PR description missing test plan

**PR field:** description
**Evidence:** `Various improvements to how we send notifications to users.`
**Convention:** PR description must include three sections: (1) what changed, (2) why, (3) test plan. All three are absent here.
**Fix:** Expand the description:

```markdown
## Summary
Add rate limiting to the notification endpoint to prevent duplicate sends on double-registration.
Update welcome email template copy.

## Why
Users were receiving duplicate welcome emails when registering twice in quick succession.
Rate limiting at the endpoint prevents this. Email template was outdated.

## Test plan
- [ ] Register a new user twice rapidly — confirm only one welcome email is sent
- [ ] Trigger welcome email manually — confirm updated template renders correctly
- [ ] Run `npm test src/notifications` — all notification unit tests pass
- [ ] Manual: confirm no duplicate entries appear in the user notification feed
```

---

#### [SUGGESTION] Pass 5: WIP commit in branch history

**Commit:** `wip: still working on the push notification handler`
**Evidence:** Subject contains `wip`
**Convention:** WIP commits are acceptable in a feature branch in a squash-merge workflow. They must NOT survive as the final squash commit message.
**Fix:** Before raising the PR, confirm the squash commit message is rewritten to something like `feat(notifications): add rate-limited email and push delivery`. If the push notification handler is incomplete, consider whether this PR should be split before merge.

---

### Clean Areas

- `fix: sending duplicate emails when user registers twice` — type prefix present, description is a finding-free imperative phrase, under 70 characters, no trailing period.
- Branch name `feature/user-notifications` — follows the `feature/description` convention.
- No merge commits detected in branch history (Pass 3 clean).
- No content files modified; content date preservation check not applicable (Pass 4).
- No empty commits, large binary files, or sensitive data patterns found (Pass 5).

---

## Criteria

### Criteria checks (against skill definition)

- [x] PASS: Skill executes all five mandatory passes — the SKILL.md states "Execute all five passes" as a mandatory process; each pass has explicit commands. All five appear in the output including N/A for Pass 4.
- [x] PASS: Past-tense commits flagged as Pass 1 findings with specific commit subject lines as evidence — `Updated` and `Added` are both flagged verbatim; Evidence Format requires `**Evidence:** [the actual message]`.
- [x] PASS: Missing type prefix on `Updated the email template...` flagged — Pass 1 step 1 requires `<type>[optional scope]: <description>`; a bare description violates the format. Type assigned with reasoning.
- [x] PASS: WIP commit flagged as Pass 5 hygiene finding — Pass 5 step 1 explicitly targets `wip` in the grep pattern and states the squash-merge nuance: acceptable in history, not acceptable as final squash message.
- [x] PASS: PR title `User notification improvements` flagged for lacking conventional commit type — Pass 2 step 1 applies the same type and imperative rules from Pass 1 to PR titles.
- [x] PASS: PR description missing test plan flagged as Pass 2 finding — Pass 2 step 3 lists "Test plan" as one of three required sections; missing it is an explicit finding.
- [x] PASS: Output uses the defined summary template with per-pass finding counts — Output Template in SKILL.md defines per-pass counts; simulated output includes all five passes with counts and N/A notation.
- [~] PARTIAL: Each finding includes a concrete rewrite suggestion, not just identification — the Evidence Format mandates a `**Fix:** [concrete rewording or action]` field; all findings carry rewrites. The WIP fix recommends a squash message rather than a per-commit rewrite, which is the correct approach but is a process instruction rather than a verbatim replacement of the offending message.

### Output expectation checks (against simulated output)

- [x] PASS: Both past-tense commits flagged by exact subject line with imperative-mood rewrite suggestions — `Updated the email template for welcome messages` and `Added rate limiting to the notification endpoint` both appear verbatim with `docs: update...` and `feat: add...` rewrites.
- [x] PASS: Missing type prefix on `Updated...` flagged with specific type assigned and reasoning — `docs:` vs `feat:` reasoning provided based on whether the change is copy or behavioural.
- [x] PASS: WIP commit identified as Pass 5 finding, acceptable in history but not as squash commit message — exact framing from SKILL.md reproduced; recommendation to rewrite or split included.
- [x] PASS: PR title flagged for missing conventional prefix and being too vague — two verbatim rewrite options provided, explaining that the current title would pollute the commit log.
- [x] PASS: PR description missing test plan flagged with concrete suggestion of what the test plan should include — manual verification steps, specific test commands, and deploy-adjacent checks all present.
- [x] PASS: All five mandatory passes executed, per-pass counts in summary including zero-finding passes — Pass 3 shows 0 findings, Pass 4 shows N/A; table covers all five.
- [x] PASS: Each finding cites exact subject line or PR text as evidence — every `**Evidence:**` block quotes verbatim content, not paraphrase.
- [x] PASS: Concrete rewrite suggestions per finding — every finding ends with a `**Fix:**` block showing the rewritten version verbatim.
- [~] PARTIAL: Output's PR-description recommendation aligns with the project's PR template and points to Conventional Commits + project README convention — the suggested template uses Summary, Why, and Test plan sections which aligns with the project convention. It does not explicitly reference the Conventional Commits spec by URL or the project README by name. Partially met.

## Notes

The skill definition handles this scenario well. Pass 1 enumerates the common past-tense forms explicitly (`Fixed`, `Updated`, `Changed`, `Removed`) so `Updated` and `Added` are unambiguously in scope. The WIP nuance in Pass 5 — acceptable in branch history under squash-merge workflow, not acceptable as the final message — is precise and practically useful.

One thing the test scenario misses: `fix: sending duplicate emails when user registers twice` uses "sending" as a gerund in the description, which Pass 1 step 3 calls out as a violation. A thorough review would flag it. The scenario treats it as a clean commit; the skill is more thorough than the test credits, which is a quality signal in the skill's favour.

The `fix:` commit on its own passes the type and prefix checks but the gerund violation means a real run would produce one more Pass 1 finding than the test expects. This does not affect scoring — it reflects the skill being stricter than the rubric, not looser.
