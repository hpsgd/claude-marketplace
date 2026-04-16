# Test: write-onboarding — technical product with configuration

Scenario: Testing the write-onboarding skill for a developer CLI tool where activation requires installation, API key configuration, GitHub connection, and running a first scan within a 10-minute time-to-first-value target.

## Prompt

/user-docs-writer:write-onboarding for our CLI tool that developers install via npm, configure with an API key, connect to their GitHub repo, and run their first scan. Time-to-first-value target: under 10 minutes.

## Criteria

- [ ] PASS: Each step has an expected result that confirms success before moving to the next step
- [ ] PASS: Progress indicators are present — the user knows where they are in the flow (e.g., "Step 2 of 4")
- [ ] PASS: The 10-minute time target is acknowledged and the flow is scoped to fit it
- [ ] PASS: Error recovery is provided for the most likely failure at each step (npm install fails, API key invalid, GitHub auth fails)
- [ ] PASS: The "first scan" is positioned as the activation moment with a clear payoff
- [ ] PARTIAL: Alternative paths are noted where applicable (yarn vs npm, GitHub vs GitLab, CI vs local)
- [ ] PASS: Copy is written for developers (concise, code-first, no hand-holding on terminal basics)
- [ ] PASS: The onboarding flow ends with a clear "what's next" that points to deeper usage, not just "you're done"
