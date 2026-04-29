# Test: review-git non-conventional commits

Scenario: A developer asks for a git review of their feature branch before raising a PR. Several commits use past tense, one has no type prefix, and the PR description is missing a test plan.

## Prompt

Can you review my branch `feature/user-notifications` before I raise a PR? The last 4 commits are:
- `Updated the email template for welcome messages`
- `fix: sending duplicate emails when user registers twice`
- `Added rate limiting to the notification endpoint`  
- `wip: still working on the push notification handler`

The PR title is "User notification improvements" and the description just says "Various improvements to how we send notifications to users."

## Criteria

- [ ] PASS: Skill executes all five mandatory passes — does not skip any pass
- [ ] PASS: Commits using past tense ("Updated", "Added") are flagged as Pass 1 findings with the specific commit subject line as evidence
- [ ] PASS: Commit without a type prefix ("Updated the email template...") is flagged as a missing conventional commit type
- [ ] PASS: WIP commit is flagged as a Pass 5 hygiene finding — acceptable in branch history but the final squash commit cannot carry this message
- [ ] PASS: PR title "User notification improvements" is flagged for lacking a conventional commit type prefix
- [ ] PASS: PR description missing a test plan is flagged as a Pass 2 finding
- [ ] PASS: Output uses the defined summary template with per-pass finding counts
- [ ] PARTIAL: Each finding includes a concrete rewrite suggestion, not just identification of the problem

## Output expectations

- [ ] PASS: Output flags both past-tense commits — `Updated the email template for welcome messages` and `Added rate limiting to the notification endpoint` — by exact subject line, with the imperative-mood rewrite suggestion (`docs: update welcome email template`, `feat: add rate limiting to notification endpoint`)
- [ ] PASS: Output flags the missing type prefix on `Updated the email template for welcome messages` — and assigns a specific Conventional Commits type (e.g. `docs:` if this is a copy change, `feat:` if it's a behavioural change), with reasoning
- [ ] PASS: Output identifies `wip: still working on the push notification handler` as a Pass 5 hygiene finding — acceptable in branch history but unacceptable as the squash commit message — with the recommendation to rewrite or squash before merge
- [ ] PASS: Output flags the PR title `User notification improvements` for missing the conventional commit prefix and being too vague — recommending `feat: add user notification system` or `feat(notifications): add rate-limited email and push delivery`
- [ ] PASS: Output flags the PR description's missing test plan as a Pass 2 finding — with a concrete suggestion of what the test plan should include (manual verification steps, test cases covered, deploy notes)
- [ ] PASS: Output executes all five mandatory passes and reports per-pass finding counts in the summary, including passes with zero findings
- [ ] PASS: Output's findings each cite the exact subject line or PR text as evidence — not paraphrased — so the developer can find the offending content
- [ ] PASS: Output provides concrete rewrite suggestions per finding, not just identification — e.g. for the past-tense commits, the rewritten imperative version is shown verbatim
- [ ] PARTIAL: Output's PR-description recommendation aligns with the project's PR template (Summary, Changes, Test plan) and points to the Conventional Commits + project README convention rather than a generic format
