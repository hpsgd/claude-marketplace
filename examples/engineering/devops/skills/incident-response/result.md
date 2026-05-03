# Incident Response

Scenario: Checking that the incident-response skill enforces a sequential five-phase process with mitigation before root cause analysis, mandatory timeline, and blameless post-mortem for high-severity incidents.

## Prompt

> Review the incident-response skill definition and verify it provides a structured process that prevents common incident response failures (root-causing before mitigating, simultaneous changes, no timeline).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

The skill directly addresses all three failure modes. Here's the verdict:

**Root-causing before mitigating** — Explicitly prevented. The cardinal rule is declared at the top ("mitigate first, root-cause second"), Phase 4 is gated with "Only after mitigation is confirmed effective", and it's called out in the Anti-Patterns section. No ambiguity.

**Simultaneous changes** — Covered in two places: Phase 3 rules ("Do not change multiple things at once... you don't know which helped") and Phase 4 step 5 ("Test the hypothesis with one change"). Anti-Patterns reinforces it. Solid.

**No timeline** — Mandatory from Phase 2 onward. Concrete format provided (`HH:MM UTC — [Event] — [Source]`), described as "the single most important artifact", Phase 3 requires logging every mitigation action to it, and the Anti-Patterns section calls out its absence explicitly.

**Minor gaps worth noting:**

- No incident commander / roles assignment — for SEV-1, who owns the timeline vs. who executes mitigations isn't defined. Parallel work during an incident needs coordination.
- The "Output" section references `templates/runbook.md` (line 229) — if that file doesn't exist, the reference is dead weight.
- No shift-change protocol for long-running SEV-1s (handoff procedure).

The core structure is sound and the three failure modes you called out are all explicitly guarded against. The gaps are real but secondary — they matter at scale/team size, not for the skill's primary purpose.

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 6.0/18.5 (32%) |
| Evaluated | 2026-04-30 |
| Target duration | 46717 ms |
| Target cost | $0.1329 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill defines five sequential phases — Detect, Assess Impact, Mitigate, Root Cause, Prevent Recurrence — and states that mitigation must precede root cause analysis | PARTIAL | Output confirms mitigation precedes root cause ('mitigate first, root-cause second' as cardinal rule, Phase 4 gated with 'Only after mitigation is confirmed effective') but never enumerates all five phases by name. |
| c2 | Skill provides a severity classification table (SEV-1 through SEV-4) with criteria, response time, and communication cadence for each level | FAIL | Output only mentions 'SEV-1' once (in the context of shift-change handoff). No severity table, no SEV-2 through SEV-4, no response times, no communication cadences described. |
| c3 | Skill requires building a mandatory timeline with timestamps and sources — and states the timeline is the single most important artifact | PASS | Output states the timeline is 'described as the single most important artifact', 'Concrete format provided (HH:MM UTC — [Event] — [Source])', and 'Phase 3 requires logging every mitigation action to it'. |
| c4 | Skill's mitigation phase lists options in order of preference (feature flag, rollback, scale, redirect, config change, hotfix) with risk assessment for each | FAIL | Output makes no mention of ordered mitigation options, feature flags, rollbacks, or risk assessments for each option. |
| c5 | Skill prohibits changing multiple things simultaneously during mitigation — one change at a time to know what worked | PASS | Output quotes Phase 3 rule: 'Do not change multiple things at once... you don't know which helped' and Phase 4 step 5: 'Test the hypothesis with one change'. |
| c6 | Skill's root cause section requires forming a specific, falsifiable hypothesis before testing — distinguishes bad ("database is slow") from good ("query X has sequential scan because index dropped in migration Z") | FAIL | Output does not mention falsifiable hypotheses or the contrasting bad/good examples anywhere. |
| c7 | Skill mandates a post-mortem for SEV-1 and SEV-2 incidents using the provided template | FAIL | Output mentions 'post-mortem' only in the minor gaps section (no shift-change protocol for 'long-running SEV-1s'). Never confirms post-mortem is mandatory for SEV-1 and SEV-2, and does not reference any template. |
| c8 | Skill lists anti-patterns including root-cause before mitigate, multiple simultaneous changes, blame individuals, and "be more careful" as prevention | PARTIAL | Output confirms an 'Anti-Patterns section' exists and references it reinforcing the no-simultaneous-changes and root-cause-before-mitigate rules. However, it never enumerates 'blame individuals' or 'be more careful' as specific anti-patterns. |
| c9 | Output confirms the skill enforces "mitigate before root-cause" as a cardinal rule, citing the specific guidance that users should not be left suffering while investigation proceeds | PARTIAL | Output confirms 'cardinal rule is declared at the top (mitigate first, root-cause second)' but does not cite any 'users should not be left suffering while investigation proceeds' guidance. |
| c10 | Output names all five phases in order (Detect and Classify, Assess Impact, Mitigate, Root Cause Analysis, Prevent Recurrence) and confirms they are sequential | FAIL | Output refers to 'Phase 3' and 'Phase 4' by number but never names all five phases in order. The phase names Detect and Classify, Assess Impact, and Prevent Recurrence do not appear. |
| c11 | Output verifies the severity table includes all four levels (SEV-1 through SEV-4) with response times and communication cadences, and notes the "classify up when in doubt" rule | FAIL | Output never mentions a severity table, does not reference SEV-2, SEV-3, or SEV-4, and does not mention 'classify up when in doubt'. |
| c12 | Output confirms the timeline requirement uses HH:MM UTC format with event and source columns, and is described as the single most important artifact | PASS | Output explicitly states: 'Concrete format provided (HH:MM UTC — [Event] — [Source])' and 'described as the single most important artifact'. |
| c13 | Output verifies mitigation options are ranked by speed/risk (feature flag fastest at seconds, hotfix slowest at 10-30 min) and includes the rule that mitigation buys time but is not the fix | FAIL | Output does not mention feature flags, hotfixes, speed rankings, or the rule that mitigation buys time but is not the fix. |
| c14 | Output confirms the root cause section requires falsifiable hypotheses with the contrasting bad/good examples (vague "database is slow" vs specific "query X sequential scan because index dropped in migration Z") | FAIL | Output does not mention falsifiable hypotheses or any contrasting examples. |
| c15 | Output confirms post-mortem is mandatory for SEV-1 and SEV-2 and references the template's required sections (timeline, impact, root cause, contributing factors, action items, lessons learned) | FAIL | Output does not confirm a post-mortem mandate for any severity level and does not reference any template sections. |
| c16 | Output identifies the prevention taxonomy (immediate / short-term / long-term) with required owner and deadline for each action item | FAIL | Output makes no mention of a prevention taxonomy, immediate/short-term/long-term categories, or owner and deadline requirements. |
| c17 | Output assesses whether the skill prevents the three failure modes named in the prompt — root-causing before mitigating, simultaneous changes, and missing timeline — and points to the specific skill content addressing each | PASS | Output has a dedicated section for each of the three failure modes with specific skill content cited: cardinal rule + Phase 4 gate for root-cause-before-mitigate; Phase 3 and Phase 4 rules for simultaneous changes; mandatory format and Phase 2 onward for timeline. |
| c18 | Output mentions the communication protocol (status update template, distinguishing "mitigated" from "resolved", "still investigating" being a valid update) | FAIL | Output does not mention communication protocols, status update templates, or the distinction between 'mitigated' and 'resolved'. |
| c19 | Output notes the blameless framing of post-mortems ("what system allowed this?" not "who did this?") | FAIL | Output does not mention blameless framing, 'what system allowed this?', or any related post-mortem philosophy. |
| c20 | Output flags the runbook template reference for in-incident use | PARTIAL | Output explicitly flags: 'The Output section references templates/runbook.md (line 229) — if that file doesn't exist, the reference is dead weight.' This addresses the runbook reference, though framed as a gap rather than confirming its in-incident use. |

### Notes

The captured output is tightly focused on the three failure modes explicitly named in the prompt (root-cause before mitigate, simultaneous changes, no timeline) and performs well on those (c3, c5, c12, c17). However, it entirely skips large portions of the skill's content: no severity classification table (c2, c11), no ordered mitigation options with risk assessment (c4, c13), no falsifiable hypothesis requirement with examples (c6, c14), no post-mortem mandate or template sections (c7, c15), no prevention taxonomy (c16), no communication protocol (c18), and no blameless framing (c19). The response answers the prompt's narrow question competently but fails to verify the breadth of structured process that the criteria require.
