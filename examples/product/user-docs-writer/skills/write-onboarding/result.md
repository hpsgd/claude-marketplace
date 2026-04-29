# Output: Write onboarding

**Verdict:** PARTIAL
**Score:** 12.5/18 criteria met (69%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill requires defining the value path first — Step 1 mandates mapping the journey before writing any content, producing a completed value path table as its required output — met
- [x] PASS: Skill requires an "aha moment" step — Step 4 is a dedicated required step for the aha moment confirmation, distinct from "completed setup"; rules require naming what was accomplished, not features used — met
- [x] PASS: Skill requires a welcome step that contextualises what the user will achieve — Step 2 rules require "In the next [N] minutes, you'll [specific outcome]" and leading with the user's goal, not a greeting — met
- [x] PASS: Each onboarding step includes the benefit — Step 3 template mandates "One sentence: why this step matters to THEM" and rules frame actions as benefits, not tasks — met
- [x] PASS: Skill requires progress indicators — Output Format uses "Step N of [N]:" headers throughout, making position-within-flow a structural requirement — met
- [~] PARTIAL: Skill addresses skip/abandon — Step 1 requires identifying drop-off risks and Step 3 mandates per-step escape hatches; abandonment recovery (re-engagement or resume paths) is not required — partially met
- [x] PASS: Skill uses plain language only — "No jargon" appears in welcome rules, Step 5 quality checks, and the Rules section; enforced at multiple points — met
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — all three present — met

### Output expectations

- [x] PASS: Output defines the value path explicitly — Step 1 produces a mandatory value path table before any UI copy, naming minimum steps and why they lead to value — met
- [ ] FAIL: Output's aha moment step is concrete and specific to Clearpath — the skill produces a template structure requiring specificity; the criterion requires Clearpath-specific copy ("user sees their first project milestone marked Complete with a status update visible to their team") that the skill's design supports but cannot guarantee without execution — not met by definition alone
- [x] PASS: Output's welcome step contextualises what the user will achieve — Step 2 template explicitly requires "In the next [N] minutes, you'll [specific outcome]" framing — met
- [x] PASS: Output's per-step copy includes the benefit — Step 3 template requires a benefit sentence per step; the template cannot be followed without it — met
- [x] PASS: Output's progress indicator is named and specified — Output Format uses "Step 1 of [N]" labelling on every step header — met
- [ ] FAIL: Output addresses skip/abandon paths — skill identifies drop-off risks in Step 1 but has no required output section, template, or rule for re-engagement nudges or resume mechanics after abandonment — not met
- [x] PASS: Output uses plain language only — no-jargon quality check and welcome rules enforce this; jargon introduced in context rule is present — met
- [x] PASS: Output's onboarding length is appropriate — Rules require ≤5 steps to aha moment with explicit reasoning ("If you can't get to the aha moment in 5 steps, you're onboarding to too much") — met
- [ ] FAIL: Output addresses success measurement — no mention of completion rate, time-to-aha-moment, or 30-day retention metrics anywhere in the skill; omission is direct — not met
- [~] PARTIAL: Output addresses celebration/reinforcement at the aha moment — Step 4 requires a celebration sentence and "What you just did" summary; no explicit animation, share-with-team prompt, or visibility mechanics beyond text — partially met

## Notes

Three genuine gaps in the skill definition:

1. Skip/abandon recovery: the skill diagnoses drop-off risk but never closes the loop. There is no required design element for what the product does when a user returns after abandoning mid-flow. The test criterion is looking for re-engagement nudges and resume paths — neither is required.

2. Success metrics: the skill's stated goal is "optimised for time-to-first-value" but it never asks the writer to define what success looks like in measurable terms. Completion rate, time-to-aha-moment, and 30-day retention are absent.

3. The Clearpath-specific aha moment criterion (Output expectation 2) is structurally unassessable from the skill definition alone — the template supports specificity but cannot produce Clearpath-specific copy without live execution. Scored as FAIL per the rubric's intent for behavioural criteria.

The prior evaluation (2026-04-16) scored 7.5/8 (PASS) against the Criteria section only. Adding the Output expectations section reveals three new failures and drops the overall score to PARTIAL.
