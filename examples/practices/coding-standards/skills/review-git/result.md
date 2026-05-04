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
> 
> Output structure (use these section names):
> 
> - **Per-pass summary table at top**:
>   ```
>   | Pass | Topic | Findings |
>   |------|-------|----------|
>   | 1 | Conventional commit format | N |
>   | 2 | Subject line under 50 chars + imperative | N |
>   | 3 | Commit body (why not what) | N |
>   | 4 | PR title + description quality | N |
>   | 5 | Branch hygiene (WIP, fixup, squash candidates) | N |
>   ```
> - **Run all 5 passes** in order with `## Pass N` headings, even when no findings emerge in a pass write `Pass N: 0 findings`.
> - **Each finding** uses structured format: `**Pass:** N | **Severity:** HIGH/MEDIUM/LOW | **Commit/PR:** <ref> | **Issue:** <description> | **Fix:** <concrete rewrite>`.
> - **Findings expected**:
>   - Pass 1, HIGH — commits 1 and 3 lack conventional commit type. Fix: rewrite as `feat(notifications): add welcome email template` and `feat(notifications): rate-limit the notification endpoint`.
>   - Pass 5, MEDIUM — `wip: still working on the push notification handler` is a hygiene finding. WIP commits are acceptable in branch history but MUST be squashed before merge. Recommend `git rebase -i HEAD~4` to fold the wip commit into the relevant feat commit.
>   - Pass 4, HIGH — PR title "User notification improvements" lacks conventional commit type. Recommend: `feat(notifications): add welcome email, dedup, rate limit, push handler`. Description "Various improvements" is too vague; needs the standard PR template with Summary, Changes, Test plan.
> 
> A few specifics for the response:
> 
> - Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
> - Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
> - For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
> - When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
> - Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

**Assumption documented:** The branch `feature/user-notifications` doesn't exist in the current repository. I'm reviewing based on the 4 commit messages you provided. If you've already created the branch locally, the findings below apply to those commits; if not, these are the issues to address before pushing.

---

| Pass | Topic | Findings |
|------|-------|----------|
| 1 | Conventional commit format | 2 (commits 1, 3) |
| 2 | Subject line under 50 chars + imperative | 1 (commit 4) |
| 3 | Commit body (why not what) | Unable to verify (no body content provided) |
| 4 | PR title + description quality | 2 |
| 5 | Branch hygiene (WIP, fixup, squash candidates) | 1 |

---

## Pass 1: Conventional commit format

**Pass 1, HIGH** | **Severity:** HIGH | **Commit:** Commit 1 (`Updated the email template for welcome messages`) | **Issue:** Missing conventional commit type prefix. Does not follow `<type>(<scope>): <description>` format. | **Fix:** `feat(notifications): update welcome email template`

**Pass 1, HIGH** | **Severity:** HIGH | **Commit:** Commit 3 (`Added rate limiting to the notification endpoint`) | **Issue:** Missing conventional commit type prefix. Does not follow `<type>(<scope>): <description>` format. | **Fix:** `feat(notifications): add rate limiting to notification endpoint`

---

## Pass 2: Subject line under 50 chars + imperative mood

**Pass 2, MEDIUM** | **Severity:** MEDIUM | **Commit:** Commit 4 (`wip: still working on the push notification handler`) | **Issue:** Uses "still working on" (passive/indicative mood) instead of imperative. Imperative form would be "implement", "add", or "work on". Also, `wip:` is not a standard conventional commit type. | **Fix:** `feat(notifications): implement push notification handler` (then squash before merge per Pass 5)

---

## Pass 3: Commit body (why not what)

Pass 3: Unable to verify — no commit bodies were provided. Assumption: commit bodies are either absent or not included in your description. Per [git-and-ci.md conventions](your CLAUDE.md), commit bodies should explain *why* the change was needed, not restate what the code does. Verify that each commit (especially the `fix:` in commit 2) includes a body explaining the root cause and rationale.

---

## Pass 4: PR title + description quality

**Pass 4, HIGH** | **Severity:** HIGH | **PR Title:** "User notification improvements" | **Issue:** Lacks conventional commit type. PR title should be a valid conventional commit that summarizes the entire PR. "Improvements" is vague and doesn't convey scope. | **Fix:** `feat(notifications): add welcome email, dedup registration, rate limit, push handler`

**Pass 4, HIGH** | **Severity:** HIGH | **PR Description:** "Various improvements to how we send notifications to users." | **Issue:** Vague and lacks structure. Per git-and-ci.md, PR descriptions should include: (1) what changed and why, (2) a test plan describing how to verify. This description does neither. | **Fix:** 
```
## Summary
- Updated welcome email template for clarity
- Fixed duplicate email bug when users register multiple times
- Added rate limiting to notification endpoint to prevent abuse
- Implemented push notification handler for real-time delivery

## Test plan
- [ ] Verify welcome email sends exactly once on user registration
- [ ] Verify re-registering same email address does not send duplicate welcome
- [ ] Verify notification endpoint rejects requests exceeding rate limit (429 response)
- [ ] Verify push notifications deliver in real-time on [platforms: web/mobile/both]
- [ ] Monitor logs for any new errors in notification pipeline
```

---

## Pass 5: Branch hygiene (WIP, fixup, squash candidates)

**Pass 5, MEDIUM** | **Severity:** MEDIUM | **Commit:** Commit 4 (`wip: still working on the push notification handler`) | **Issue:** WIP commits must not be merged to main. This indicates incomplete work and violates the no-direct-incomplete-commits policy. Must be squashed or completed before merge. | **Fix:** Use `git rebase -i HEAD~4` to fold commit 4 into the relevant feature commit (likely with commit 1 or 3, depending on scope), or complete the work and rename to `feat(notifications): implement push notification handler`. Do not merge with WIP prefix.

---

**Recommendation before raising PR:**

1. Rewrite commits 1 and 3 with conventional commit types
2. Complete or squash commit 4 — do not merge WIP
3. Rewrite PR title to conventional commit format
4. Replace vague PR description with the structured template above
5. Verify commit bodies explain *why* (especially for the duplicate email fix)

Once cleaned up, the PR will pass all reviews.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 13.5/15.5 (87%) |
| Evaluated | 2026-05-04 |
| Target duration | 25925 ms |
| Target cost | $0.0588 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill executes all five mandatory passes — does not skip any pass | PASS | Output contains ## Pass 1 through ## Pass 5 headings in order. All five passes present: Pass 1 (Conventional commit format), Pass 2 (Subject line / imperative mood), Pass 3 (Commit body), Pass 4 (PR title + description quality), Pass 5 (Branch hygiene). |
| c2 | Commits using past tense ("Updated", "Added") are flagged as Pass 1 findings with the specific commit subject line as evidence | PASS | Pass 1 flags Commit 1 with exact subject line `Updated the email template for welcome messages` and Commit 3 with exact subject line `Added rate limiting to the notification endpoint`, both as HIGH findings with verbatim quotes in backticks. |
| c3 | Commit without a type prefix ("Updated the email template...") is flagged as a missing conventional commit type | PASS | Pass 1 finding for Commit 1 states: "Missing conventional commit type prefix. Does not follow `<type>(<scope>): <description>` format." |
| c4 | WIP commit is flagged as a Pass 5 hygiene finding — acceptable in branch history but the final squash commit cannot carry this message | PASS | Pass 5 flags `wip: still working on the push notification handler` as MEDIUM severity with the recommendation to use `git rebase -i HEAD~4` to fold or complete the commit before merging to main. |
| c5 | PR title "User notification improvements" is flagged for lacking a conventional commit type prefix | PASS | Pass 4 finding for PR Title states: "Lacks conventional commit type. PR title should be a valid conventional commit that summarizes the entire PR." Fix shown as `feat(notifications): add welcome email, dedup registration, rate limit, push handler`. |
| c6 | PR description missing a test plan is flagged as a Pass 2 finding | FAIL | The PR description test plan issue is placed in Pass 4 (PR title + description quality), not Pass 2 (Subject line under 50 chars + imperative). The criterion explicitly requires it to appear as a Pass 2 finding, which it does not. |
| c7 | Output uses the defined summary template with per-pass finding counts | PASS | Summary table at top of response has all five rows with Pass, Topic, and Findings columns: "1 \| Conventional commit format \| 2 (commits 1, 3)", "2 \| Subject line under 50 chars + imperative \| 1 (commit 4)", "3 \| Commit body (why not what) \| Unable to verify", "4 \| PR title + description quality \| 2", "5 \| Branch hygiene (WIP, fixup, squash candidates) \| 1". |
| c8 | Each finding includes a concrete rewrite suggestion, not just identification of the problem | PARTIAL | Pass 1, 2, 4, and 5 all include verbatim rewrite suggestions (e.g. `feat(notifications): update welcome email template`, full PR description template). Pass 3 does not provide a concrete rewrite — it says "Unable to verify" and gives general guidance only. Ceiling is PARTIAL. |
| c9 | Output flags both past-tense commits — `Updated the email template for welcome messages` and `Added rate limiting to the notification endpoint` — by exact subject line, with the imperative-mood rewrite suggestion (`docs: update welcome email template`, `feat: add rate limiting to notification endpoint`) | PASS | Both commits flagged by exact subject line in Pass 1. Rewrites given: `feat(notifications): update welcome email template` and `feat(notifications): add rate limiting to notification endpoint` — both imperative mood. The example types in the criterion (`docs:`, `feat:`) are illustrative; the output uses `feat(notifications):` for both with imperative phrasing. |
| c10 | Output flags the missing type prefix on `Updated the email template for welcome messages` — and assigns a specific Conventional Commits type (e.g. `docs:` if this is a copy change, `feat:` if it's a behavioural change), with reasoning | PARTIAL | A specific type is assigned (`feat(notifications)`) but no reasoning is provided for the choice of `feat` over `docs` or another type. The finding says only "Missing conventional commit type prefix" and gives the fix directly, with no explanation of why `feat` was selected over alternative types. |
| c11 | Output identifies `wip: still working on the push notification handler` as a Pass 5 hygiene finding — acceptable in branch history but unacceptable as the squash commit message — with the recommendation to rewrite or squash before merge | PASS | Pass 5 flags the WIP commit as MEDIUM severity: "WIP commits must not be merged to main" with recommendation to use `git rebase -i HEAD~4` to fold or complete the commit with message `feat(notifications): implement push notification handler`. |
| c12 | Output flags the PR title `User notification improvements` for missing the conventional commit prefix and being too vague — recommending `feat: add user notification system` or `feat(notifications): add rate-limited email and push delivery` | PASS | Pass 4 flags the PR title as HIGH: "Lacks conventional commit type" and "'Improvements' is vague and doesn't convey scope." Rewrite given: `feat(notifications): add welcome email, dedup registration, rate limit, push handler`. |
| c13 | Output flags the PR description's missing test plan as a Pass 2 finding — with a concrete suggestion of what the test plan should include (manual verification steps, test cases covered, deploy notes) | FAIL | The PR description test plan deficiency is flagged in Pass 4, not Pass 2. The criterion explicitly requires it to be a Pass 2 finding. The output does not address this issue in Pass 2 at all — Pass 2 only covers the WIP commit's subject line style. |
| c14 | Output executes all five mandatory passes and reports per-pass finding counts in the summary, including passes with zero findings | PASS | All five passes appear in the summary table and as ## Pass N sections. No pass is omitted. Pass 3 is included with "Unable to verify" explanation rather than a raw zero, which still satisfies the presence requirement. |
| c15 | Output's findings each cite the exact subject line or PR text as evidence — not paraphrased — so the developer can find the offending content | PASS | Each finding quotes the exact text in backticks: Pass 1 quotes `Updated the email template for welcome messages` and `Added rate limiting to the notification endpoint`; Pass 2 and Pass 5 quote `wip: still working on the push notification handler`; Pass 4 quotes "User notification improvements" and "Various improvements to how we send notifications to users." |
| c16 | Output provides concrete rewrite suggestions per finding, not just identification — e.g. for the past-tense commits, the rewritten imperative version is shown verbatim | PASS | Verbatim rewrites provided for all findings with findings: `feat(notifications): update welcome email template`, `feat(notifications): add rate limiting to notification endpoint`, `feat(notifications): implement push notification handler`, `feat(notifications): add welcome email, dedup registration, rate limit, push handler`, plus a full PR description template with checkboxed test plan items. |
| c17 | Output's PR-description recommendation aligns with the project's PR template (Summary, Changes, Test plan) and points to the Conventional Commits + project README convention rather than a generic format | PARTIAL | The PR description template includes `## Summary` and `## Test plan` sections with concrete checklist items. However, it omits a `## Changes` section as specified in the project template. The output references git-and-ci.md conventions but does not explicitly point to the Conventional Commits spec or project README. Ceiling is PARTIAL. |

### Notes

The output is structurally strong: all five passes execute, the summary table is present with counts, exact subject lines are quoted throughout, and concrete rewrite suggestions accompany every finding. The two outright failures both stem from the same root issue — the PR description test plan deficiency is placed in Pass 4 (the semantically correct home) rather than Pass 2 as c6 and c13 require. There is also a minor gap in c10 where `feat(notifications):` is assigned to the welcome email commit without any reasoning distinguishing it from `docs:` or `chore:`. The WIP commit handling is clean and the PR title finding is well-executed. Overall the review reads as genuinely useful to a developer, with the main deficit being a mechanical placement mismatch on two related criteria.
