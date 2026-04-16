# Test: learning capture after a mistake

Scenario: A developer just force-pushed to the wrong branch and wants to capture the incident as a learning immediately after it happened.

## Prompt

/learning Capture this: I just ran `git push --force origin main` from the wrong directory — I was in the `payments-service` repo but thought I was in `my-feature-branch` project. Pushed over 3 commits on `origin/main` in the payments-service repo. Had to ask the platform team to restore from their backup. This wasted about 2 hours and caused a 20-minute deploy freeze.

## Criteria

- [ ] PASS: Step 1 assigns a category (SYSTEM, METHOD, DOMAIN, or FEEDBACK) with reasoning
- [ ] PASS: Step 2 writes the learning in the exact format — frontmatter with name/description/type, plus What happened, Learning (imperative), Why, How to apply, Severity, and Category
- [ ] PASS: The learning is stated as an imperative rule ("Always X" or "Never Y"), not as a narrative
- [ ] PASS: The "Why" field explains the consequence of ignoring the rule — not just a restatement
- [ ] PASS: Step 3 assigns Critical severity given the data loss and rework described — downgrading to Important would violate the skill's own severity rules
- [ ] PASS: Step 4 failure capture is triggered (something went notably wrong) and produces a failure analysis with root cause, what was tried, what worked, and a prevention rule
- [ ] PASS: Output follows the "When capturing" format template with name, category, severity, rule, and saved-to path
- [ ] PARTIAL: Skill checks for an existing learning on the same topic before creating a new file, to avoid duplicates
