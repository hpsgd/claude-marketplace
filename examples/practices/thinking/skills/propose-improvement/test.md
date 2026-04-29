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

## Output expectations

- [ ] PASS: Output locates the marketplace repo path by reading project settings or config — not assuming a hardcoded path like `~/code/turtlestack`
- [ ] PASS: Output reads the pattern file `learned--verify-before-declaring-complete.md` and confirms the trigger count is at or above the minimum threshold (>=3) — citing the actual count (5) from the file's metadata
- [ ] PASS: Output maps the learning to a specific target file in the marketplace — likely a rule file (e.g. under `plugins/practices/coding-standards/rules/` or thinking/rules) — and explains the mapping decision (rule vs skill vs agent vs script)
- [ ] PASS: Output creates the branch from a freshly-pulled main — `git fetch origin && git checkout main && git pull && git checkout -b learnings/verify-before-declaring-complete` — not from whatever branch was current
- [ ] PASS: Output's diff is shown to the user explicitly before any push — the workflow stops at "review this diff and approve" — and proceeds only after user confirmation
- [ ] PASS: Output's commit message includes evidence — the 5 session IDs where the pattern was triggered, with brief correction summaries — not just the rule text
- [ ] PASS: Output uses Conventional Commits for the commit message (e.g. `feat(rules): add verify-before-declaring-complete rule`) per project convention
- [ ] PASS: Output updates the pattern file's status to `pr_submitted` and records the PR URL in the file — so future invocations of the skill don't re-propose the same learning
- [ ] PASS: Output's PR description includes the evidence (sessions, count, why it should be marketplace-wide), the proposed rule wording, and a request for review
- [ ] PARTIAL: Output returns to the `main` branch in the marketplace repo at the end of the workflow — leaving on the feature branch is flagged as cleanup pending
