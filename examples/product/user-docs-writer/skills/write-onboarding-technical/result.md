# Output: write-onboarding — technical product with configuration

| | |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 15/17 criteria met (88%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Each step has an expected result that confirms success before moving to the next step — met: Step 3 template mandates a "### You should see" section; quality checklist explicitly requires "Expected results present"
- [x] PASS: Progress indicators are present — met: output format uses "## Step N of [N]:" headings throughout, matching the criterion's example format exactly
- [x] PASS: The 10-minute time target is acknowledged and the flow is scoped to fit it — met: value path table includes "Time target" row; output format header includes "**Time to complete:** [N] minutes"; quality checklist includes a time test; rules cap each step at under 2 minutes
- [x] PASS: Error recovery is provided for the most likely failure at each step — met: Step 3 template includes a mandatory "### If something's not right" section; quality checklist requires "Escape hatches" at every step
- [x] PASS: The "first scan" is positioned as the activation moment with a clear payoff — met: Step 1 requires identifying a specific aha moment (not a configured state); Step 4 confirms that moment with named concrete outcomes
- [~] PARTIAL: Alternative paths are noted where applicable (yarn vs npm, GitHub vs GitLab, CI vs local) — partially met: the skill has no instruction to surface alternative tooling paths; the Rules section actively steers toward a single opinionated path ("ask for the minimum to start," "never front-load configuration"), which discourages noting exceptions
- [~] PARTIAL: Copy is written for developers (concise, code-first, no hand-holding on terminal basics) — partially met: Step 1 identifies target user and what they already know, which accommodates a developer audience; step template uses exact UI element names and example inputs suited to CLI docs; however no explicit developer-specific writing guidance exists and nothing instructs the writer to favour code blocks over prose or skip terminal basics
- [x] PASS: The onboarding flow ends with a clear "what's next" that points to deeper usage — met: Step 4 mandates a "### What to explore next" table with links; rules state "Link to deeper content, don't summarise it here"

### Output expectations

- [x] PASS: Output's value path covers exactly the 4 steps from the prompt fitting under the 10-minute target — met: Step 1 maps minimum steps to aha moment with a time target field; the skill would produce a value path table identifying install, API key config, GitHub connection, and first scan
- [~] PARTIAL: Output's first-scan step is positioned as the activation moment with visible payoff — partially met: Step 4 confirms the aha moment with "What you just did" outcomes; quality check asks "does the flow end with the user seeing real value, not just a configured state?" — this implies scan results must be visible, but the template does not mandate describing the specific CLI output (vulnerabilities found, dependency tree) that constitutes the payoff
- [x] PASS: Output's step expected results are concrete with verification commands — met: "You should see" is mandatory per the step template; rules require exact element names and example inputs, steering toward verification steps like `mycli --version` or `mycli auth status`
- [x] PASS: Output's progress indicator is shown in the docs — met: output format uses "Step N of [N]:" heading pattern throughout
- [x] PASS: Output's error recovery covers the most likely failure per step — met: "If something's not right" sub-section is mandatory for every step; quality checklist validates escape hatches are present at each step
- [x] PASS: Output's tone is developer-appropriate — met: rules are concise and action-first; "Use exact UI element names" and "Use the product to teach the product" steer toward code-first writing; step template uses command syntax and bold element names naturally suited to CLI docs
- [x] PASS: Output's "what's next" section points to deeper usage paths with linked docs — met: Step 4 mandates a table of next goals with links; "Link to deeper content, don't summarise it here" is an explicit rule; 3-option cap keeps it actionable
- [x] PASS: Output covers common alternative paths as sidebar callouts without inflating the linear flow — met: progressive disclosure rules ("no more than 3 steps visible," "reveal only when needed") and the step template leave structural room for callout blocks without derailing the linear flow
- [~] PARTIAL: Output addresses CI integration as a natural next step — partially met: Step 4's "What to explore next" table could include a CI integration link, and the skill's rules require linking to deeper content; however the skill does not explicitly prompt the writer to include CI integration as one of the three next-step options for a CLI tool

## Notes

The skill covers the structural requirements well. Value path table, per-step template, and quality checklist work together cleanly, and most criteria map to explicit mechanisms in the definition.

Two recurring gaps: the skill is audience-neutral (no developer-specific writing guidance beyond implicit structure), and it has no mechanism for surfacing alternative tooling paths. The Rules section actively discourages branching, which cuts against the alternative-paths criterion. CI integration as an explicit next-step prompt is missing from the aha moment template, leaving it to the writer's judgment whether to include it.
