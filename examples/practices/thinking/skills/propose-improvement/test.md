# Test: propose-improvement upstream a learned rule

Scenario: A developer has a local learned rule that has proven effective across 5 sessions and wants to upstream it to the marketplace via a PR. The propose-improvement skill handles the full workflow.

## Prompt

/propose-improvement The pattern `learned--verify-before-declaring-complete` has been triggered in 5 sessions now. I think it's ready to share upstream. It's about always running verification steps before saying something is done.

## Criteria

- [ ] PASS: Step 1 locates the marketplace repo by reading settings files — does not assume a hardcoded path
- [ ] PASS: Step 2 reads the pattern file and confirms it meets the minimum threshold (count >= 3) before proceeding
- [ ] PASS: Step 3 maps the learning to the correct target file in the marketplace (rule, skill, agent, or script depending on type)
- [ ] PASS: Step 4 creates a branch from a fresh main (not from the current branch) and applies the minimal required change
- [ ] PASS: Step 5 (diff review) is never skipped — the diff is shown to the user and approval is required before any push occurs
- [ ] PASS: Step 6 commit message includes the session IDs and correction summaries as evidence — not just the rule text
- [ ] PASS: Step 7 updates the pattern file status to `pr_submitted` and records the PR URL
- [ ] PARTIAL: Skill returns to `main` after completing the workflow — never leaves the marketplace repo on a feature branch
