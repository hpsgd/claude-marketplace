# Output: write-onboarding — technical product with configuration

| | |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 14/18 criteria met (78%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Each step has an expected result that confirms success before moving to the next step — met: Step 3 template mandates a "### You should see" section describing the expected state after each action; quality checklist explicitly requires "Expected results present"
- [x] PASS: Progress indicators are present — the user knows where they are in the flow — met: Output Format template uses `## Step 1 of [N]`, `## Step 2 of [N]` headings throughout, matching the example format from the criterion exactly
- [x] PASS: The 10-minute time target is acknowledged and the flow is scoped to fit it — met: value path table (Step 1) includes a "Time target" row; Output Format header includes "**Time to complete:** [N] minutes"; quality checklist includes a time test; rules cap each step at under 2 minutes
- [x] PASS: Error recovery is provided for the most likely failure at each step — met: Step 3 template includes a mandatory "### If something's not right" section with a one-line fix for each problem; quality checklist requires "Escape hatches" at every step
- [x] PASS: The "first scan" is positioned as the activation moment with a clear payoff — met: Step 1 requires identifying a specific "aha moment" (not just a configured state); Step 4 is dedicated to confirming that moment with named concrete outcomes
- [~] PARTIAL: Alternative paths are noted where applicable (yarn vs npm, GitHub vs GitLab, CI vs local) — partially met: the skill has no instruction to surface alternative tooling paths; the Rules section actively discourages branching ("ask for the minimum to start," "never front-load configuration"), steering toward a single opinionated path without noting exceptions
- [~] PARTIAL: Copy is written for developers (concise, code-first, no hand-holding on terminal basics) — partially met: Step 1 requires identifying the target user and what they already know, which accommodates a developer audience, and the step template uses exact syntax and bold element names that suit CLI docs; however the skill has no explicit developer-specific writing guidance and does not instruct the writer to skip terminal basics or favour code blocks over prose
- [x] PASS: The onboarding flow ends with a clear "what's next" that points to deeper usage — met: Step 4 requires a "### What to explore next" table with links; rules state "Link to deeper content, don't summarise it here"; limit of 3 options prevents decision paralysis

### Output expectations

- [x] PASS: Output's value path covers exactly the 4 steps from the prompt — met: Step 1 maps minimum steps to aha moment; the skill would produce a value path table identifying install, API key, GitHub connection, and first scan as the four steps
- [~] PARTIAL: Output's first-scan step is positioned as the activation moment with visible payoff — partially met: Step 4 confirms the aha moment with "What you just did" outcomes; the quality check asks "does the flow end with the user seeing real value, not just a configured state?" — this implies scan results must be visible, but the template does not mandate describing the specific CLI output (vulnerabilities found, dependency tree, etc.) that constitutes the payoff
- [x] PASS: Output's step expected results are concrete with verification commands — met: "You should see" is mandatory per the step template; rules require exact element names and example inputs, which together guide the writer toward verification steps like `mycli --version` or `mycli auth status`
- [x] PASS: Output's progress indicator is shown in the docs — met: output format uses "Step N of [N]:" heading pattern throughout
- [x] PASS: Output's error recovery covers the most likely failure per step — met: "If something's not right" sub-section is mandatory for every step; quality checklist validates escape hatches are present at each step
- [x] PASS: Output's tone is developer-appropriate — met: the skill's rules are concise and action-first; "Use exact UI element names" and "Use the product to teach the product" steer toward code-first writing; the step template uses command syntax and bold element names naturally suited to CLI docs
- [x] PASS: Output's "what's next" section points to deeper usage paths with linked docs — met: Step 4 mandates a table of next goals with links; "Link to deeper content, don't summarise it here" is an explicit rule; the 3-option cap keeps it actionable
- [ ] FAIL: Output addresses authentication choices — not met: the skill has no instruction to surface auth method choices (API key vs SSO/OAuth), identify a recommended path for first-time users, or note the alternative; entirely absent from the definition
- [x] PASS: Output covers common alternative paths as sidebar callouts without inflating the linear flow — met: the step template and output format leave structural room for callout blocks; progressive disclosure rules ("no more than 3 steps visible," "reveal only when needed") support sidebars rather than detours; the skill does not break the linear flow
- [~] PARTIAL: Output addresses CI integration as a natural next step — partially met: Step 4's "What to explore next" table could include a CI integration link; the skill's rules require linking to deeper content rather than summarising, which is compatible with a CI path; however the skill does not explicitly prompt the writer to include CI integration as one of the three next-step options for a CLI tool

## Notes

The skill is well-structured for generic onboarding and covers most of what a developer-focused CLI scenario needs. The value path table, per-step template, and quality checklist work together cleanly, and most criteria map to explicit mechanisms in the definition.

Three gaps point in the same direction: the skill is deliberately audience-neutral. Authentication alternatives are entirely absent — the skill has no concept of recommending a first-time auth path. The alternative-path gap is compounded by the Rules section actively discouraging branching. CI integration as a next-step prompt is missing from the aha moment template.

The developer register point is borderline. The step template suits CLI documentation naturally, but nothing in the definition distinguishes developer-appropriate writing from consumer-appropriate writing. A less technical writer following the same template for a consumer product would produce similar structure.
