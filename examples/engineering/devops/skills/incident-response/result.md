# Incident response skill structure

Checking that the incident-response skill enforces a sequential five-phase process with mitigation before root cause analysis, mandatory timeline, and blameless post-mortem for high-severity incidents.

## Prompt

> Review the incident-response skill definition and verify it provides a structured process that prevents common incident response failures (root-causing before mitigating, simultaneous changes, no timeline).

Given an alert — "Error rate on /api/v1/shipments spiked to 28% (normal < 0.5%). Alert fired at 14:23 UTC. A deployment completed at 14:20 UTC." — the skill would drive this response:

Phase 1 classifies severity (SEV-2: major feature degraded, no workaround confirmed) and starts the timeline. Phase 2 assesses blast radius and impact count. Phase 3 selects rollback as the fastest mitigation option, explicitly noting no other changes should occur simultaneously. Only after rollback is confirmed does Phase 4 begin — forming a specific hypothesis about the deployment diff before testing it. Phase 5 produces concrete prevention actions, explicitly excluding "be more careful." A post-mortem is mandatory because this is SEV-2.

## Output



## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 8/8 criteria met (100%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Skill defines five sequential phases with mitigation before root cause — the skill opens with "The cardinal rule: mitigate first, root-cause second" and defines Phase 1 (Detect and Classify) → Phase 2 (Assess Impact) → Phase 3 (Mitigate) → Phase 4 (Root Cause Analysis) → Phase 5 (Prevent Recurrence) in explicit sequence. Phase 4 starts with "Only after mitigation is confirmed effective."

- [x] PASS: Skill provides SEV-1 through SEV-4 table with criteria, response time, and communication cadence — Phase 1 contains a four-row table: SEV-1 (Critical / Immediate / every 15 min), SEV-2 (High / <30 min / every 30 min), SEV-3 (Medium / <2 hours / every 2 hours), SEV-4 (Low / next business day / resolution only). All three columns are present for all four rows.

- [x] PASS: Skill requires mandatory timeline with timestamps and sources, named the single most important artifact — Phase 2: "Build a timeline (MANDATORY)" with format `HH:MM UTC — [Event] — [Source of information]` and the explicit statement: "The timeline is the single most important artifact. Update it continuously."

- [x] PASS: Skill lists mitigation options in the specified order with risk assessment — Phase 3 table lists in order: Feature flag off → Rollback deployment → Scale up/out → Traffic redirect → Configuration change → Hotfix deploy → Service isolation. Each row has Speed, Risk, and "When to use" columns.

- [x] PASS: Skill prohibits simultaneous changes — Phase 3 rules: "Do not change multiple things at once during mitigation. If you roll back AND change config, you don't know which helped."

- [x] PASS: Skill requires specific falsifiable hypothesis — Phase 4 item 4: "BAD: 'The database is slow'" / "GOOD: 'Query X on table Y has a sequential scan because the index was dropped in migration Z'" — the exact examples from the criterion are present verbatim.

- [x] PASS: Skill mandates post-mortem for SEV-1 and SEV-2 with template — heading reads "Post-Mortem Template (MANDATORY for SEV-1 and SEV-2)" followed by a complete markdown template covering summary, timeline, impact, root cause, contributing factors, resolution, detection, action items, and lessons learned.

- [x] PASS: Skill lists all four required anti-patterns — Anti-Patterns section lists: "Root-cause before mitigate", "Multiple simultaneous changes", "Blame individuals", and "'Be more careful' as prevention" — all four present by name.

## Notes

The skill is complete against all eight criteria. The anti-patterns section includes three additional items beyond the four specified in the rubric: "No timeline", "Silent incidents", and "Skipping the post-mortem" — each a genuine failure mode. The hypothesis quality bar is high: the bad/good examples in the criterion text appear verbatim in the definition, suggesting the rubric was written against this skill.
