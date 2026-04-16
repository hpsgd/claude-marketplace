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
