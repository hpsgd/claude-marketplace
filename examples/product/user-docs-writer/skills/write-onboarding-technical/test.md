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

## Output expectations

- [ ] PASS: Output's value path covers exactly the 4 steps from the prompt — npm install, API key configuration, GitHub connection, run first scan — fitting under the 10-minute time-to-first-value target
- [ ] PASS: Output's first-scan step is positioned as the activation moment — with the visible payoff being scan results displayed (vulnerabilities found, dependency tree, or whatever the CLI outputs) — NOT just "scan complete"
- [ ] PASS: Output's step expected results are concrete — Step 1: "after `npm install`, run `mycli --version` and you should see `v1.2.3`"; Step 2: "after setting API key, run `mycli auth status` and you should see `Authenticated as <your email>`" — every step has a verification command
- [ ] PASS: Output's progress indicator is shown in the docs — "Step 2 of 4: Configure your API key" or visual progress dots — so the user knows how far along they are
- [ ] PASS: Output's error recovery covers the most likely failure per step — npm install fails (Node version mismatch, npm registry, permissions), API key invalid (typo, expired key, wrong env var), GitHub auth fails (PAT scope insufficient, network), first scan errors (no repos found, ratelimited)
- [ ] PASS: Output's tone is developer-appropriate — concise, code-first, assumes terminal fluency; e.g. "run `mycli init` in your repo root" not "open your terminal application then type the following command"
- [ ] PASS: Output's "what's next" section points to deeper usage paths — "Set up scheduled scans in CI", "Configure custom rules", "Integrate with your CI/CD pipeline" — with linked docs, not just "explore the docs"
- [ ] PASS: Output addresses authentication choices — if the CLI supports both API key and SSO / OAuth, the recommended path for first-time users is named (likely API key for speed) with the alternative noted
- [ ] PASS: Output covers common alternative paths — yarn vs npm, GitHub vs GitLab if supported, CI usage vs local — without inflating the linear flow; alternatives are sidebar callouts, not detours
- [ ] PARTIAL: Output addresses CI integration as a natural next step — many developers will want to move from local CLI to CI scan after the first manual run; the "what's next" should preview the CI integration path
