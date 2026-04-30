# Result: incident-response skill structure

**Verdict:** PASS
**Score:** 19.5/20 criteria met (97.5%)
**Evaluated:** 2026-04-30

---

## Output

The following is a simulated evaluation response the skill would produce when invoked against the prompt: "Review the incident-response skill definition and verify it provides a structured process that prevents common incident response failures (root-causing before mitigating, simultaneous changes, no timeline)."

---

### Skill Evaluation: incident-response

**Skill:** `plugins/engineering/devops/skills/incident-response/SKILL.md`
**Test focus:** Structural verification — does the definition prevent three named failure modes?

---

#### Phase structure

The skill defines five sequential phases, explicitly labelled and ordered:

| # | Phase | Key constraint |
|---|---|---|
| 1 | Detect and Classify | Classify severity; when in doubt, classify up |
| 2 | Assess Impact | Build mandatory timeline before taking action |
| 3 | Mitigate | STOP THE BLEEDING — speed over elegance |
| 4 | Root Cause Analysis | Only after mitigation is confirmed effective |
| 5 | Prevent Recurrence | Concrete actions with owner and deadline |

The cardinal rule is stated at the top of the process section: "mitigate first, root-cause second. Never spend 30 minutes investigating while users are down." Phase 4 opens with "Only after mitigation is confirmed effective" — making the sequencing a hard gate, not a suggestion.

---

#### Severity classification table

| Severity | Criteria | Response time | Communication cadence |
|---|---|---|---|
| SEV-1 (Critical) | Service down, data loss, security breach, revenue impact | Immediate | Every 15 minutes |
| SEV-2 (High) | Major feature degraded, affecting many users, no workaround | < 30 min | Every 30 minutes |
| SEV-3 (Medium) | Feature degraded, workaround exists, limited user impact | < 2 hours | Every 2 hours |
| SEV-4 (Low) | Minor issue, cosmetic, single user affected | Next business day | Resolution only |

The skill includes a "classify up" rule: when in doubt, elevate one level and downgrade later if warranted. Classification decisions must be logged with reasoning — silent reclassification is prohibited.

---

#### Timeline requirement

The skill marks the timeline **MANDATORY** in Phase 2, before any mitigation action is taken. The format is prescriptive:

```
HH:MM UTC — [Event] — [Source of information]
14:23 UTC — Error rate spike to 15% (normal: <1%) — Datadog alert
14:25 UTC — Deployment abc123 completed — GitHub Actions
14:27 UTC — First customer report via support — Zendesk ticket #4521
```

The skill states: "The timeline is the single most important artifact. Update it continuously." Every mitigation action must also be documented in the timeline.

---

#### Mitigation options (ranked)

| Option | Speed | Risk | When to use |
|---|---|---|---|
| Feature flag off | Seconds | Low | Feature is behind a flag |
| Rollback deployment | 1-5 min | Low | Recent deployment is the likely cause |
| Scale up/out | 1-5 min | Low | Load-related, capacity issue |
| Traffic redirect | 1-5 min | Medium | Regional issue, failover available |
| Configuration change | 1-10 min | Medium | Bad config deployed |
| Hotfix deploy | 10-30 min | Higher | Root cause identified and fix is small |
| Service isolation | 1-5 min | Medium | Cascade prevention, circuit breaker |

Feature flag is fastest (seconds, low risk); hotfix is slowest (10-30 min, higher risk). The skill includes the rule: "Mitigation is not the fix. It buys time." A rollback that stops the bleeding is explicitly preferred over a hotfix that takes 30 minutes.

---

#### Root cause analysis — hypothesis discipline

The skill requires a specific, falsifiable hypothesis before testing. The contrasting examples are verbatim in the definition:

- BAD: "The database is slow"
- GOOD: "Query X on table Y has a sequential scan because the index was dropped in migration Z"

The process requires: form the hypothesis, test with one change, confirm or refute before moving to the next. This prevents scatter-shot debugging during an active incident.

---

#### Post-mortem

Marked **MANDATORY for SEV-1 and SEV-2**. The template includes six required sections:

1. Timeline
2. Impact (users, duration, data, financial, SLA)
3. Root Cause
4. Contributing Factors
5. Action Items (with owner, deadline, and type: Prevent / Detect / Mitigate)
6. Lessons Learned (what went well, what went poorly, where we got lucky)

The Root Cause field is explicitly framed as blameless: "Not 'human error' — what system allowed this to happen?" This framing appears in the template itself, not just in the Anti-Patterns section, which means it's present at the point of use.

---

#### Prevention taxonomy

Phase 5 uses a three-tier taxonomy with required owner and deadline for every action:

| Prevention type | Example | Timeline |
|---|---|---|
| Immediate | Add missing validation, fix the bug | This sprint |
| Short-term | Add test, add monitoring alert, add circuit breaker | Next sprint |
| Long-term | Architecture change, process improvement, training | Next quarter |

"Be more careful" is explicitly rejected as a prevention measure in both Phase 5 and the Anti-Patterns section.

---

#### Anti-patterns

The skill names seven anti-patterns. The four required by the test criteria are all present:

- Root-cause before mitigate: "users are suffering while you investigate. Stop the bleeding first"
- Multiple simultaneous changes: "if you change 3 things and it resolves, you don't know which fixed it"
- Blame individuals: "post-mortems are blameless. Ask 'what system allowed this?' not 'who did this?'"
- "Be more careful" as prevention: "human vigilance fails. Automate, validate, monitor"

Additional anti-patterns: no timeline, silent incidents, skipping the post-mortem.

---

#### Communication protocol

Status update template (used during the incident):

```
**Incident: [title]**
**Severity:** SEV-[1/2/3/4]
**Status:** [Investigating / Mitigating / Monitoring / Resolved]
**Impact:** [who is affected and how]
**Current action:** [what is being done right now]
**Next update:** [time]
```

Key rules: updates at the cadence defined by severity; "still investigating" is a valid update — silence is not; "mitigated" (bleeding stopped) is distinguished from "resolved" (fix deployed and verified); no speculation on root cause in customer-facing communications.

---

#### Failure mode assessment

| Failure mode | Addressed? | Where |
|---|---|---|
| Root-causing before mitigating | Yes — hard gate | Cardinal rule on line 13; Phase 4 gated by "only after mitigation confirmed"; Anti-Patterns |
| Simultaneous changes | Yes — explicit prohibition | Phase 3 rule: "Do not change multiple things at once during mitigation"; Anti-Patterns |
| No timeline | Yes — mandatory artifact | Phase 2: MANDATORY timeline, HH:MM UTC format; "single most important artifact"; Anti-Patterns |

All three failure modes named in the prompt are addressed with specific, verifiable content in the skill definition.

---

#### Runbook reference

The final line of the skill references `templates/runbook.md` for creating runbooks during incidents. This is a brief closing note rather than an integrated instruction — whether the template exists is not verifiable from this skill file alone.

---

## Criteria

### Definition criteria

- [x] PASS: Skill defines five sequential phases — Detect, Assess Impact, Mitigate, Root Cause, Prevent Recurrence — and states that mitigation must precede root cause analysis — met: phases are labelled and ordered; "mitigate first, root-cause second" is declared the cardinal rule; Phase 4 opens with "Only after mitigation is confirmed effective"
- [x] PASS: Skill provides a severity classification table (SEV-1 through SEV-4) with criteria, response time, and communication cadence for each level — met: table present with all four levels and all three columns
- [x] PASS: Skill requires building a mandatory timeline with timestamps and sources — and states the timeline is the single most important artifact — met: marked MANDATORY, HH:MM UTC format shown with Event and Source columns, stated "the single most important artifact"
- [x] PASS: Skill's mitigation phase lists options in order of preference (feature flag, rollback, scale, redirect, config change, hotfix) with risk assessment for each — met: table lists all six options (plus service isolation) with Speed and Risk columns in that order
- [x] PASS: Skill prohibits changing multiple things simultaneously during mitigation — met: "Do not change multiple things at once during mitigation. If you roll back AND change config, you don't know which helped."
- [x] PASS: Skill's root cause section requires forming a specific, falsifiable hypothesis before testing — met: verbatim bad/good examples present ("database is slow" vs "query X sequential scan because index dropped in migration Z")
- [x] PASS: Skill mandates a post-mortem for SEV-1 and SEV-2 incidents using the provided template — met: header reads "MANDATORY for SEV-1 and SEV-2" with full template included
- [x] PASS: Skill lists anti-patterns including root-cause before mitigate, multiple simultaneous changes, blame individuals, and "be more careful" as prevention — met: all four appear in the Anti-Patterns section

### Output expectations

- [x] PASS: Output confirms the skill enforces "mitigate before root-cause" as a cardinal rule, citing the specific guidance that users should not be left suffering — met: cardinal rule stated with direct quote, Phase 4 gate noted
- [x] PASS: Output names all five phases in order and confirms they are sequential — met: table enumerates all five phases with constraints
- [x] PASS: Output verifies the severity table includes all four levels with response times and communication cadences, and notes the "classify up when in doubt" rule — met: full table reproduced, classify-up rule noted
- [x] PASS: Output confirms the timeline requirement uses HH:MM UTC format with event and source columns, and is described as the single most important artifact — met: format shown, "single most important artifact" quoted
- [x] PASS: Output verifies mitigation options are ranked by speed/risk (feature flag fastest at seconds, hotfix slowest at 10-30 min) and includes the rule that mitigation buys time but is not the fix — met: table reproduced with speed values, "buys time" rule quoted
- [x] PASS: Output confirms the root cause section requires falsifiable hypotheses with the contrasting bad/good examples — met: both examples quoted verbatim
- [x] PASS: Output confirms post-mortem is mandatory for SEV-1 and SEV-2 and references the template's required sections — met: all six sections enumerated
- [x] PASS: Output identifies the prevention taxonomy (immediate / short-term / long-term) with required owner and deadline — met: table reproduced with all three tiers
- [x] PASS: Output assesses whether the skill prevents the three failure modes — met: failure mode table maps each to specific content
- [x] PASS: Output mentions the communication protocol (status update template, "mitigated" vs "resolved", "still investigating" valid) — met: all three sub-points covered
- [x] PASS: Output notes the blameless framing of post-mortems — met: Root Cause field quote included; Anti-Patterns reference
- [~] PARTIAL: Output flags the runbook template reference for in-incident use — partially met: mentioned as a closing note but not integrated as an actionable instruction; whether `templates/runbook.md` exists cannot be confirmed from the skill alone

## Notes

The skill is well-constructed. All eight structural criteria are met cleanly. The three failure modes named in the prompt (root-cause before mitigate, simultaneous changes, missing timeline) are each addressed with specific language — not just in the Anti-Patterns section but within the phases themselves, which is better design.

One observation: the mitigation table lists seven options (including service isolation), while the criterion names six. Service isolation is a genuine addition for cascade-prevention scenarios — not a gap, and not counted against the criterion.

The blameless framing appears in two places: the Anti-Patterns section and the Root Cause field of the post-mortem template itself. Embedding it at the point of use (the template) is better than relying on general guidance alone.

The runbook reference at line 229 is a closing sentence rather than an integrated instruction. Whether `templates/runbook.md` exists in the plugin is an external dependency not verifiable from this skill file.
