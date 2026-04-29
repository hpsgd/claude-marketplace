# Output: Write onboarding

**Verdict:** PASS
**Score:** 15.5/16 criteria met (97%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill requires defining the value path first — Step 1 mandates mapping the journey and producing a completed value path table before any content is written — met
- [x] PASS: Skill requires an "aha moment" step — Step 4 is a dedicated required step with its own template, confirming first value with specific outcomes; explicitly distinct from "completed setup" — met
- [x] PASS: Skill requires a welcome step that contextualises what the user will achieve — Step 2 rules require "In the next [N] minutes, you'll [specific outcome]" and leading with the user's goal — met
- [x] PASS: Each onboarding step includes the benefit — Step 3 template mandates "One sentence: why this step matters to THEM" and frames actions as benefits, not tasks — met
- [x] PASS: Skill requires progress indicators — Output Format uses "Step N of [N]:" headers on every step, making position-in-flow a structural requirement — met
- [x] PASS: Skill addresses skip/abandon — Step 5 is a full mandatory section with a template covering empty-state nudge, re-engagement on next visit, and resume path for each drop-off risk identified in Step 1 — met (full credit; this is a required design element, not a passing mention)
- [x] PASS: Skill uses plain language only — "No jargon" appears in the welcome rules, Step 5 quality checklist, and the Rules section; enforced at multiple points — met
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — all three present — met

### Output expectations

- [x] PASS: Output defines the value path explicitly — Step 1 produces a mandatory value path table naming minimum steps and why they lead to value, before any UI copy — met
- [x] PASS: Output's welcome step contextualises what the user will achieve — Step 2 template requires "In the next [N] minutes, you'll [specific outcome]" framing exactly as the criterion describes — met
- [x] PASS: Output's per-step copy includes the benefit — Step 3 template requires a benefit sentence per step; the template cannot be completed without it — met
- [x] PASS: Output's progress indicator is named and specified — Output Format uses "Step 1 of [N]" labelling on every step header, visible across all steps — met
- [x] PASS: Output addresses skip/abandon paths — Step 5 requires recovery copy for each drop-off risk: empty-state nudge, re-engagement on next visit, and resume path; these are required output sections with a full template — met
- [x] PASS: Output uses plain language only — no-jargon quality check in Step 6 and welcome rules enforce this; jargon is introduced in context per the rules — met
- [x] PASS: Output's onboarding length is appropriate — Rules require reaching the aha moment in ≤5 steps with explicit reasoning: "If you can't get to the aha moment in 5 steps, you're onboarding to too much" — met
- [~] PARTIAL: Output addresses celebration/reinforcement at the aha moment — Step 4 requires a celebration sentence and "What you just did" summary; no animation, share-with-team prompt, or broader visibility mechanics specified beyond text copy — partially met

## Notes

The previous result.md scored skip/abandon as PARTIAL on the grounds that "abandonment recovery (re-engagement or resume paths) is not required." That reading was against an earlier version of the skill. The current SKILL.md has a full Step 5 with a mandatory template covering empty-state nudge, re-engagement on next visit, and resume path — a complete required design element. Both the Criteria and Output expectations criteria for skip/abandon now score PASS.

The only genuine gap is celebration/reinforcement: Step 4 covers text-based celebration (a celebration sentence and "What you just did" list) but does not require animation, share-with-team prompts, or other visibility mechanics that would make the value moment feel like an event rather than a screen state.

The skill is tightly structured. The value path table in Step 1 functions as a forcing function — it cannot be skipped without visibly omitting required fields. The per-step benefit sentence and escape hatch are embedded in a template that cannot be followed without including them.
