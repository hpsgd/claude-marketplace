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
