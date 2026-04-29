# Output: incident-response skill structure

**Verdict:** PASS
**Score:** 19.5/20 criteria met (97.5%)
**Evaluated:** 2026-04-29

## Results

### Criteria (skill definition)

- [x] PASS: Skill defines five sequential phases — Detect, Assess Impact, Mitigate, Root Cause, Prevent Recurrence — and states that mitigation must precede root cause analysis — met: phases are labelled and ordered; "mitigate first, root-cause second" is declared the cardinal rule on line 13
- [x] PASS: Skill provides a severity classification table (SEV-1 through SEV-4) with criteria, response time, and communication cadence for each level — met: table includes all four levels with all three columns
- [x] PASS: Skill requires building a mandatory timeline with timestamps and sources — and states the timeline is the single most important artifact — met: marked MANDATORY, HH:MM UTC format shown with Event and Source columns, "single most important artifact" stated explicitly
- [x] PASS: Skill's mitigation phase lists options in order of preference (feature flag, rollback, scale, redirect, config change, hotfix) with risk assessment for each — met: table lists all six options (plus service isolation) with Speed and Risk columns in that order
- [x] PASS: Skill prohibits changing multiple things simultaneously during mitigation — one change at a time to know what worked — met: "Do not change multiple things at once during mitigation. If you roll back AND change config, you don't know which helped."
- [x] PASS: Skill's root cause section requires forming a specific, falsifiable hypothesis before testing — distinguishes bad ("database is slow") from good ("query X has sequential scan because index dropped in migration Z") — met: verbatim examples present
- [x] PASS: Skill mandates a post-mortem for SEV-1 and SEV-2 incidents using the provided template — met: header reads "MANDATORY for SEV-1 and SEV-2" with full template included
- [x] PASS: Skill lists anti-patterns including root-cause before mitigate, multiple simultaneous changes, blame individuals, and "be more careful" as prevention — met: all four named items appear in the Anti-Patterns section

### Output expectations (simulated response)

- [x] PASS: Output confirms the skill enforces "mitigate before root-cause" as a cardinal rule, citing the specific guidance that users should not be left suffering while investigation proceeds — met: cardinal rule language and "users are down" framing are prominent enough that any thorough evaluation surfaces them
- [x] PASS: Output names all five phases in order (Detect and Classify, Assess Impact, Mitigate, Root Cause Analysis, Prevent Recurrence) and confirms they are sequential — met: phases are clearly labelled in the skill; a structural evaluation would enumerate them
- [x] PASS: Output verifies the severity table includes all four levels (SEV-1 through SEV-4) with response times and communication cadences, and notes the "classify up when in doubt" rule — met: table and rule are both present and easily verifiable
- [x] PASS: Output confirms the timeline requirement uses HH:MM UTC format with event and source columns, and is described as the single most important artifact — met: format and description are explicit in the skill
- [x] PASS: Output verifies mitigation options are ranked by speed/risk (feature flag fastest at seconds, hotfix slowest at 10-30 min) and includes the rule that mitigation buys time but is not the fix — met: table values and the "buys time" rule are both present
- [x] PASS: Output confirms the root cause section requires falsifiable hypotheses with the contrasting bad/good examples (vague "database is slow" vs specific "query X sequential scan because index dropped in migration Z") — met: verbatim in the skill; a response would quote or paraphrase both examples
- [x] PASS: Output confirms post-mortem is mandatory for SEV-1 and SEV-2 and references the template's required sections (timeline, impact, root cause, contributing factors, action items, lessons learned) — met: all six sections appear in the template
- [x] PASS: Output identifies the prevention taxonomy (immediate / short-term / long-term) with required owner and deadline for each action item — met: table and rules are explicit
- [x] PASS: Output assesses whether the skill prevents the three failure modes named in the prompt — root-causing before mitigating, simultaneous changes, and missing timeline — and points to the specific skill content addressing each — met: all three are addressed in both phase guidance and the Anti-Patterns section, giving a response clear content to cite
- [x] PASS: Output mentions the communication protocol (status update template, distinguishing "mitigated" from "resolved", "still investigating" being a valid update) — met: all three sub-points are present in the Communication Protocol section and prominent enough to surface
- [x] PASS: Output notes the blameless framing of post-mortems ("what system allowed this?" not "who did this?") — met: phrasing appears verbatim in both the Anti-Patterns section and the post-mortem template's Root Cause field
- [~] PARTIAL: Output flags the runbook template reference for in-incident use — partially met: the reference exists as the final line of the skill but is brief and easy to omit when the prompt focuses on failure-mode prevention; a response may surface the substantive content without reaching this closing line

## Notes

The skill is well-constructed. All eight structural criteria are met cleanly. The phase sequencing, severity table, and anti-patterns directly address the three failure modes the prompt names.

One observation: the mitigation table lists seven options (including service isolation), while the criterion names six. Service isolation is a genuine addition for cascade-prevention scenarios — not a gap, and not counted against the criterion.

The post-mortem template embeds blameless framing directly into the Root Cause field ("Not 'human error' — what system allowed this to happen?") rather than relying solely on the Anti-Patterns section to enforce it. That's good design.

The runbook reference at line 229 is a closing sentence rather than an integrated instruction. Whether `templates/runbook.md` exists in the plugin is a dependency not evaluated here.
