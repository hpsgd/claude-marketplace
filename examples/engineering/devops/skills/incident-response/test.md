# Test: incident-response skill structure

Scenario: Checking that the incident-response skill enforces a sequential five-phase process with mitigation before root cause analysis, mandatory timeline, and blameless post-mortem for high-severity incidents.

## Prompt

Review the incident-response skill definition and verify it provides a structured process that prevents common incident response failures (root-causing before mitigating, simultaneous changes, no timeline).

## Criteria

- [ ] PASS: Skill defines five sequential phases — Detect, Assess Impact, Mitigate, Root Cause, Prevent Recurrence — and states that mitigation must precede root cause analysis
- [ ] PASS: Skill provides a severity classification table (SEV-1 through SEV-4) with criteria, response time, and communication cadence for each level
- [ ] PASS: Skill requires building a mandatory timeline with timestamps and sources — and states the timeline is the single most important artifact
- [ ] PASS: Skill's mitigation phase lists options in order of preference (feature flag, rollback, scale, redirect, config change, hotfix) with risk assessment for each
- [ ] PASS: Skill prohibits changing multiple things simultaneously during mitigation — one change at a time to know what worked
- [ ] PASS: Skill's root cause section requires forming a specific, falsifiable hypothesis before testing — distinguishes bad ("database is slow") from good ("query X has sequential scan because index dropped in migration Z")
- [ ] PASS: Skill mandates a post-mortem for SEV-1 and SEV-2 incidents using the provided template
- [ ] PASS: Skill lists anti-patterns including root-cause before mitigate, multiple simultaneous changes, blame individuals, and "be more careful" as prevention

## Output expectations

- [ ] PASS: Output confirms the skill enforces "mitigate before root-cause" as a cardinal rule, citing the specific guidance that users should not be left suffering while investigation proceeds
- [ ] PASS: Output names all five phases in order (Detect and Classify, Assess Impact, Mitigate, Root Cause Analysis, Prevent Recurrence) and confirms they are sequential
- [ ] PASS: Output verifies the severity table includes all four levels (SEV-1 through SEV-4) with response times and communication cadences, and notes the "classify up when in doubt" rule
- [ ] PASS: Output confirms the timeline requirement uses HH:MM UTC format with event and source columns, and is described as the single most important artifact
- [ ] PASS: Output verifies mitigation options are ranked by speed/risk (feature flag fastest at seconds, hotfix slowest at 10-30 min) and includes the rule that mitigation buys time but is not the fix
- [ ] PASS: Output confirms the root cause section requires falsifiable hypotheses with the contrasting bad/good examples (vague "database is slow" vs specific "query X sequential scan because index dropped in migration Z")
- [ ] PASS: Output confirms post-mortem is mandatory for SEV-1 and SEV-2 and references the template's required sections (timeline, impact, root cause, contributing factors, action items, lessons learned)
- [ ] PASS: Output identifies the prevention taxonomy (immediate / short-term / long-term) with required owner and deadline for each action item
- [ ] PASS: Output assesses whether the skill prevents the three failure modes named in the prompt — root-causing before mitigating, simultaneous changes, and missing timeline — and points to the specific skill content addressing each
- [ ] PARTIAL: Output mentions the communication protocol (status update template, distinguishing "mitigated" from "resolved", "still investigating" being a valid update)
- [ ] PARTIAL: Output notes the blameless framing of post-mortems ("what system allowed this?" not "who did this?")
- [ ] PARTIAL: Output flags the runbook template reference for in-incident use
