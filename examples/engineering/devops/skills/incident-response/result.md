# Incident Response

Scenario: Checking that the incident-response skill enforces a sequential five-phase process with mitigation before root cause analysis, mandatory timeline, and blameless post-mortem for high-severity incidents.

## Prompt

> Review the incident-response skill definition and verify it provides a structured process that prevents common incident response failures (root-causing before mitigating, simultaneous changes, no timeline).
> 
> Read the skill at `/Users/martin/Projects/turtlestack/plugins/engineering/devops/skills/incident-response/SKILL.md` and verify each item by name. Quote skill text where present:
> 
> - **Five sequential phases (named in order)**: **Detect and Classify**, **Assess Impact**, **Mitigate**, **Root Cause Analysis**, **Prevent Recurrence**. Confirm mitigation precedes root cause and quote the cardinal rule "mitigate first, root-cause second — users should not be left suffering while investigation proceeds".
> - **Severity classification table (4 levels)**: **SEV-1**, **SEV-2**, **SEV-3**, **SEV-4** with criteria, response time, and communication cadence for each. Plus the **"classify up when in doubt"** rule.
> - **Mitigation options ranked by speed/risk** (in order of preference): (1) feature flag (seconds), (2) rollback (minutes), (3) scale, (4) redirect/route around, (5) config change, (6) hotfix (10-30 min). Plus the rule: "mitigation buys time but is not the fix".
> - **Root cause requires falsifiable hypotheses**. Bad example: "database is slow". Good example: "query X has sequential scan because index dropped in migration Z". Both examples named.
> - **Post-mortem mandatory for SEV-1 and SEV-2** with template sections: **timeline**, **impact**, **root cause**, **contributing factors**, **action items**, **lessons learned**.
> - **Prevention taxonomy**: **immediate / short-term / long-term** action items, each with a named **owner** and **deadline**.
> - **Communication protocol**: status update template, distinguishing **"mitigated"** from **"resolved"**, **"still investigating"** as a valid update.
> - **Blameless framing**: "what system allowed this?" not "who did this?".
> - **Anti-patterns named (4)**: (1) root-cause before mitigate, (2) multiple simultaneous changes, (3) blame individuals, (4) "be more careful" as prevention.
> - **Runbook template** referenced for in-incident use.
> 
> Confirm or flag each by name.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Verification Report: Incident Response Skill

✅ **All major items present.** The skill provides a structured sequential process that prevents common IR failures. Here's the verification:

### Five Sequential Phases ✅

**Named in order:** Detect and Classify → Assess Impact → Mitigate → Root Cause Analysis → Prevent Recurrence.

**Cardinal rule quoted (with slight variation):**
> "The cardinal rule: **mitigate first, root-cause second.** The goal is to stop the bleeding before you diagnose the disease. Never spend 30 minutes investigating while users are down."

Your requested phrasing ("users should not be left suffering") is captured in intent rather than exact wording, but the principle is unmistakable.

---

### Severity Classification Table (4 Levels) ✅

**All present with criteria, response time, and cadence:**

| Level | Response time | Cadence |
|---|---|---|
| SEV-1 (Critical) | Immediate | Every 15 minutes |
| SEV-2 (High) | < 30 min | Every 30 minutes |
| SEV-3 (Medium) | < 2 hours | Every 2 hours |
| SEV-4 (Low) | Next business day | Resolution only |

**"Classify up when in doubt" rule present:**
> "When in doubt, classify UP one level. Downgrade later if warranted"

---

### Mitigation Options Ranked (Speed/Risk) ✅

**In order of preference:**
1. Feature flag off (seconds, low risk)
2. Rollback deployment (1-5 min, low risk)
3. Scale up/out (1-5 min, low risk)
4. Traffic redirect (1-5 min, medium risk)
5. Configuration change (1-10 min, medium risk)
6. Hotfix deploy (10-30 min, higher risk)
7. Service isolation (1-5 min, medium risk)

**Key rule quoted:**
> "Mitigation is not the fix. It buys time. A rollback that stops the bleeding is better than a hotfix that takes 30 minutes"

**"Don't change multiple things" rule present:**
> "**Do not change multiple things at once** during mitigation. If you roll back AND change config, you don't know which helped"

---

### Root Cause Requires Falsifiable Hypotheses ✅

**Both examples present by name:**
- BAD: "The database is slow"
- GOOD: "Query X on table Y has a sequential scan because the index was dropped in migration Z"

---

### Post-Mortem Mandatory for SEV-1/SEV-2 ✅

**Template sections all present:**
- **Timeline** (with example format)
- **Impact** (users affected, duration, data/financial/SLA impact)
- **Root Cause** (with anti-pattern: "Not 'human error' — what system allowed this?")
- **Contributing Factors** (explicitly listed)
- **Action Items** (table with Type / Owner / Deadline / Status)
- **Lessons Learned** (what went well / poorly / where we got lucky)

---

### Prevention Taxonomy ✅

**Three categories named:**
> "| Prevention type | Example | Timeline |
> | **Immediate** | Add missing validation, fix the bug | This sprint |
> | **Short-term** | Add test, add monitoring alert, add circuit breaker | Next sprint |
> | **Long-term** | Architecture change, process improvement, training | Next quarter |"

**Owner and deadline rule:**
> "Every prevention action has an owner and a deadline"

---

### Communication Protocol ✅

**Status update template includes:**
- Status field with options: [Investigating / Mitigating / Monitoring / Resolved]
- Distinguishes "mitigated" vs "resolved":
  > "Distinguish between 'mitigated' (bleeding stopped) and 'resolved' (fix deployed and verified)"
- Validates "still investigating":
  > "'Still investigating' is a valid update. Silence is not"

---

### Blameless Framing ✅

> "Ask 'what system allowed this?' not 'who did this?'"

---

### Anti-Patterns Named (4 Required + extras) ✅

**Your four explicitly present:**
1. "Root-cause before mitigate — users are suffering while you investigate. Stop the bleeding first"
2. "Multiple simultaneous changes — if you change 3 things and it resolves, you don't know which fixed it"
3. "Blame individuals — post-mortems are blameless. Systems fail, not people"
4. "'Be more careful' as prevention — human vigilance fails. Automate, validate, monitor"

**Additional anti-patterns included (bonus):**
- No timeline
- Silent incidents
- Skipping the post-mortem

---

### Runbook Template Referenced ✅

> "Use the runbook template (`templates/runbook.md`) for creating runbooks referenced during incidents."

---

## Summary

The skill is **structurally sound** and includes all critical decision gates to prevent the three main IR failures:
1. ✅ Mitigation before root cause (Phase 3 precedes Phase 4)
2. ✅ Single change per test cycle (explicit rule)
3. ✅ Comprehensive timeline from minute one (mandatory in Phase 2)

The blameless/systemic framing is present throughout. The only minor gap: the exact phrasing of the cardinal rule differs slightly from your specification, but the safety principle is unambiguous.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/18.5 (92%) |
| Evaluated | 2026-05-03 |
| Target duration | 25884 ms |
| Target cost | $0.0585 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill defines five sequential phases — Detect, Assess Impact, Mitigate, Root Cause, Prevent Recurrence — and states that mitigation must precede root cause analysis | PASS | Output explicitly lists: 'Named in order: Detect and Classify → Assess Impact → Mitigate → Root Cause Analysis → Prevent Recurrence' and quotes the cardinal rule: 'mitigate first, root-cause second. The goal is to stop the bleeding before you diagnose the disease. Never spend 30 minutes investigating while users are down.' |
| c2 | Skill provides a severity classification table (SEV-1 through SEV-4) with criteria, response time, and communication cadence for each level | PASS | Output asserts 'All present with criteria, response time, and cadence' and presents a table covering SEV-1 through SEV-4 with response times (Immediate / <30 min / <2 hours / Next business day) and cadences (every 15 min / every 30 min / every 2 hours / resolution only). |
| c3 | Skill requires building a mandatory timeline with timestamps and sources — and states the timeline is the single most important artifact | PARTIAL | Output confirms a timeline requirement ('Comprehensive timeline from minute one (mandatory in Phase 2)' and 'Timeline (with example format)' in the post-mortem template) but never confirms the specific HH:MM UTC format with event/source columns, and never quotes or confirms the skill describes the timeline as 'the single most important artifact'. |
| c4 | Skill's mitigation phase lists options in order of preference (feature flag, rollback, scale, redirect, config change, hotfix) with risk assessment for each | PASS | Output enumerates all six required options (plus service isolation) in ranked order, each with timing and risk level (e.g., 'Feature flag off (seconds, low risk)' through 'Hotfix deploy (10-30 min, higher risk)'). |
| c5 | Skill prohibits changing multiple things simultaneously during mitigation — one change at a time to know what worked | PASS | Output quotes: 'Do not change multiple things at once during mitigation. If you roll back AND change config, you don't know which helped.' |
| c6 | Skill's root cause section requires forming a specific, falsifiable hypothesis before testing — distinguishes bad ("database is slow") from good ("query X has sequential scan because index dropped in migration Z") | PASS | Output confirms both named examples: 'BAD: The database is slow' and 'GOOD: Query X on table Y has a sequential scan because the index was dropped in migration Z'. |
| c7 | Skill mandates a post-mortem for SEV-1 and SEV-2 incidents using the provided template | PASS | Output section header 'Post-Mortem Mandatory for SEV-1/SEV-2 ✅' and lists all template sections (Timeline, Impact, Root Cause, Contributing Factors, Action Items, Lessons Learned). |
| c8 | Skill lists anti-patterns including root-cause before mitigate, multiple simultaneous changes, blame individuals, and "be more careful" as prevention | PASS | Output explicitly lists all four under 'Anti-Patterns Named': (1) Root-cause before mitigate, (2) Multiple simultaneous changes, (3) Blame individuals, (4) 'Be more careful' as prevention — plus three bonus anti-patterns. |
| c9 | Output confirms the skill enforces "mitigate before root-cause" as a cardinal rule, citing the specific guidance that users should not be left suffering while investigation proceeds | PARTIAL | Output confirms the cardinal rule and quotes 'Never spend 30 minutes investigating while users are down,' but explicitly notes the requested phrasing 'users should not be left suffering' is 'captured in intent rather than exact wording' — meaning the specific language cited in the criterion is acknowledged as absent from the skill. |
| c10 | Output names all five phases in order (Detect and Classify, Assess Impact, Mitigate, Root Cause Analysis, Prevent Recurrence) and confirms they are sequential | PASS | Output states: 'Named in order: Detect and Classify → Assess Impact → Mitigate → Root Cause Analysis → Prevent Recurrence' with arrow notation confirming sequential ordering. |
| c11 | Output verifies the severity table includes all four levels (SEV-1 through SEV-4) with response times and communication cadences, and notes the "classify up when in doubt" rule | PASS | Output provides the full four-row table with response times and cadences, and quotes: 'When in doubt, classify UP one level. Downgrade later if warranted.' |
| c12 | Output confirms the timeline requirement uses HH:MM UTC format with event and source columns, and is described as the single most important artifact | FAIL | Output mentions 'Timeline (with example format)' in the post-mortem template and 'Comprehensive timeline from minute one (mandatory in Phase 2)' in the summary, but never references HH:MM UTC format, event/source column structure, or describes the timeline as 'the single most important artifact'. |
| c13 | Output verifies mitigation options are ranked by speed/risk (feature flag fastest at seconds, hotfix slowest at 10-30 min) and includes the rule that mitigation buys time but is not the fix | PASS | Output lists feature flag first at 'seconds, low risk' and hotfix at '10-30 min, higher risk', and quotes: 'Mitigation is not the fix. It buys time. A rollback that stops the bleeding is better than a hotfix that takes 30 minutes.' |
| c14 | Output confirms the root cause section requires falsifiable hypotheses with the contrasting bad/good examples (vague "database is slow" vs specific "query X sequential scan because index dropped in migration Z") | PASS | Output section 'Root Cause Requires Falsifiable Hypotheses ✅' explicitly presents both contrasting examples by name. |
| c15 | Output confirms post-mortem is mandatory for SEV-1 and SEV-2 and references the template's required sections (timeline, impact, root cause, contributing factors, action items, lessons learned) | PASS | Output lists all six required template sections: Timeline, Impact, Root Cause, Contributing Factors, Action Items, Lessons Learned — all present and named. |
| c16 | Output identifies the prevention taxonomy (immediate / short-term / long-term) with required owner and deadline for each action item | PASS | Output quotes the three-row taxonomy table (Immediate / Short-term / Long-term with examples and timelines) and confirms: 'Every prevention action has an owner and a deadline.' |
| c17 | Output assesses whether the skill prevents the three failure modes named in the prompt — root-causing before mitigating, simultaneous changes, and missing timeline — and points to the specific skill content addressing each | PASS | Summary section explicitly addresses all three: '1. ✅ Mitigation before root cause (Phase 3 precedes Phase 4), 2. ✅ Single change per test cycle (explicit rule), 3. ✅ Comprehensive timeline from minute one (mandatory in Phase 2)' — each pointing to specific skill content. |
| c18 | Output mentions the communication protocol (status update template, distinguishing "mitigated" from "resolved", "still investigating" being a valid update) | PARTIAL | Output confirms all three elements: status update template with options listed, quotes 'Distinguish between mitigated (bleeding stopped) and resolved (fix deployed and verified)', and quotes 'Still investigating is a valid update. Silence is not.' |
| c19 | Output notes the blameless framing of post-mortems ("what system allowed this?" not "who did this?") | PARTIAL | Output quotes verbatim: 'Ask what system allowed this? not who did this?' under the 'Blameless Framing ✅' section. |
| c20 | Output flags the runbook template reference for in-incident use | PARTIAL | Output quotes: 'Use the runbook template (templates/runbook.md) for creating runbooks referenced during incidents.' |

### Notes

The output is thorough and well-structured, correctly confirming 17 of 20 criteria. The two main gaps are c3/c12 (timeline specifics): the output confirms the timeline requirement exists but never surfaces the 'single most important artifact' designation, HH:MM UTC format, or event/source column structure — both c3 and c12 check different facets of this same gap, resulting in PARTIAL and FAIL respectively. The other deduction is c9: the output explicitly acknowledges the exact cardinal-rule phrasing ('users should not be left suffering') is not present verbatim in the skill, earning only PARTIAL. All PARTIAL-ceiling criteria (c18–c20) are fully satisfied within their ceilings. The output's summary section directly addressing the three named failure modes is a strong positive, and the inclusion of additional anti-patterns beyond the required four shows thorough skill analysis.
