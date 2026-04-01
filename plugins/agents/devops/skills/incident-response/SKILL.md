---
name: incident-response
description: Guide incident response — detect, assess, mitigate, root cause, prevent recurrence.
argument-hint: "[incident description, error logs, or alert details]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Respond to $ARGUMENTS.

## Incident Response Process (5 phases — sequential, do not skip)

The cardinal rule: **mitigate first, root-cause second.** The goal is to stop the bleeding before you diagnose the disease. Never spend 30 minutes investigating while users are down.

### Phase 1: Detect and Classify

**Gather the symptoms (2 minutes max):**

1. What is the symptom? (error spike, latency increase, service down, data corruption, security alert)
2. What alert fired? What is the threshold and current value?
3. When did it start? (check monitoring dashboards for the exact time)
4. Is it ongoing or has it resolved?

**Classify severity:**

| Severity | Criteria | Response time | Communication cadence |
|---|---|---|---|
| **SEV-1 (Critical)** | Service down, data loss, security breach, revenue impact | Immediate | Every 15 minutes |
| **SEV-2 (High)** | Major feature degraded, affecting many users, no workaround | < 30 min | Every 30 minutes |
| **SEV-3 (Medium)** | Feature degraded, workaround exists, limited user impact | < 2 hours | Every 2 hours |
| **SEV-4 (Low)** | Minor issue, cosmetic, single user affected | Next business day | Resolution only |

**Rules:**
- When in doubt, classify UP one level. Downgrade later if warranted
- SEV-1 and SEV-2 override all other work in progress
- Log the classification decision and reasoning — do not silently reclassify later

### Phase 2: Assess Impact

Answer these questions before taking action:

1. **Who is affected?** All users? A segment? One customer? Internal only?
2. **How many?** Percentage of traffic, number of users, number of requests failing
3. **What is the user experience?** Complete failure? Degraded? Wrong data? Slow?
4. **Is data at risk?** Is data being lost, corrupted, or exposed?
5. **Is there financial impact?** Transactions failing? SLA breach? Billing errors?
6. **What is the blast radius?** Is this isolated to one service or cascading?

**Build a timeline (MANDATORY):**
```
HH:MM UTC — [Event] — [Source of information]
14:23 UTC — Error rate spike to 15% (normal: <1%) — Datadog alert
14:25 UTC — Deployment abc123 completed — GitHub Actions
14:27 UTC — First customer report via support — Zendesk ticket #4521
```

The timeline is the single most important artifact. Update it continuously.

### Phase 3: Mitigate (STOP THE BLEEDING)

Choose the fastest path to reduce user impact. Speed over elegance.

**Mitigation options (in order of preference):**

| Option | Speed | Risk | When to use |
|---|---|---|---|
| **Feature flag off** | Seconds | Low | Feature is behind a flag |
| **Rollback deployment** | 1-5 min | Low | Recent deployment is the likely cause |
| **Scale up/out** | 1-5 min | Low | Load-related, capacity issue |
| **Traffic redirect** | 1-5 min | Medium | Regional issue, failover available |
| **Configuration change** | 1-10 min | Medium | Bad config deployed |
| **Hotfix deploy** | 10-30 min | Higher | Root cause identified and fix is small |
| **Service isolation** | 1-5 min | Medium | Cascade prevention, circuit breaker |

**Rules:**
- Mitigation is not the fix. It buys time. A rollback that stops the bleeding is better than a hotfix that takes 30 minutes
- **Do not change multiple things at once** during mitigation. If you roll back AND change config, you don't know which helped
- Document every mitigation action in the timeline
- Verify mitigation worked — check error rates, latency, user reports. If not resolved, escalate
- If mitigation is not possible within 15 minutes for SEV-1, escalate immediately

### Phase 4: Root Cause Analysis

Only after mitigation is confirmed effective:

1. **Check the change log** — recent deployments, config changes, dependency updates, infrastructure changes
   ```bash
   git log --oneline --since="2 hours ago"
   ```

2. **Correlate with the timeline** — what changed within 30 minutes before the incident started?

3. **Trace the failure path:**
   - Start at the symptom (error message, failed request)
   - Trace backwards through the system
   - At each boundary: what went in? What came out? Where did it diverge?

4. **Form a hypothesis** — specific and falsifiable:
   - BAD: "The database is slow"
   - GOOD: "Query X on table Y has a sequential scan because the index was dropped in migration Z"

5. **Test the hypothesis with one change** — confirm or refute before moving to the next

6. **Identify contributing factors** beyond the root cause:
   - Missing monitoring that delayed detection
   - Missing test that would have caught it pre-deploy
   - Missing circuit breaker that allowed cascade
   - Process gap that allowed the bad change

### Phase 5: Prevent Recurrence

For every root cause, define concrete prevention measures:

| Prevention type | Example | Timeline |
|---|---|---|
| **Immediate** | Add missing validation, fix the bug | This sprint |
| **Short-term** | Add test, add monitoring alert, add circuit breaker | Next sprint |
| **Long-term** | Architecture change, process improvement, training | Next quarter |

**Rules:**
- Every prevention action has an owner and a deadline
- "Be more careful" is not a prevention measure. Systemic fixes, not human vigilance
- If the same class of incident has occurred before, the previous prevention measures failed. Escalate

## Communication Protocol

### During the Incident

**Who to notify (by severity):**

| Severity | Notify | Channel |
|---|---|---|
| SEV-1 | Engineering lead, product lead, support lead, affected customers | Incident Slack channel + status page |
| SEV-2 | Engineering lead, product lead | Incident Slack channel |
| SEV-3 | Team lead | Team Slack channel |
| SEV-4 | Log for next standup | None |

**Status update template:**
```
**Incident: [title]**
**Severity:** SEV-[1/2/3/4]
**Status:** [Investigating / Mitigating / Monitoring / Resolved]
**Impact:** [who is affected and how]
**Current action:** [what is being done right now]
**Next update:** [time]
```

**Rules:**
- Status updates at the cadence defined by severity — even if the update is "still investigating"
- "Still investigating" is a valid update. Silence is not
- Never speculate on root cause in customer-facing communications
- Distinguish between "mitigated" (bleeding stopped) and "resolved" (fix deployed and verified)

## Post-Mortem Template (MANDATORY for SEV-1 and SEV-2)

```markdown
# Post-Mortem: [Incident Title]

**Date:** [date]
**Duration:** [start time] — [end time] ([total duration])
**Severity:** SEV-[level]
**Author:** [name]
**Reviewers:** [names]

## Summary
[2-3 sentences: what happened, who was affected, what was the impact]

## Timeline
| Time (UTC) | Event | Source |
|---|---|---|
| [HH:MM] | [what happened] | [how we know] |

## Impact
- **Users affected:** [number or percentage]
- **Duration of impact:** [time]
- **Data impact:** [none / lost / corrupted / exposed]
- **Financial impact:** [if any]
- **SLA impact:** [if any]

## Root Cause
[Detailed technical explanation. Not "human error" — what system allowed this to happen?]

## Contributing Factors
- [Factor 1 — why it made the incident worse or harder to detect]
- [Factor 2]

## Resolution
[What was done to resolve the incident — both mitigation and permanent fix]

## Detection
- **How was it detected?** [alert / customer report / internal discovery]
- **Time to detect:** [minutes from start to detection]
- **Could we have detected it sooner?** [yes/no — how?]

## Action Items

| # | Action | Type | Owner | Deadline | Status |
|---|---|---|---|---|---|
| 1 | [action] | Prevent / Detect / Mitigate | [name] | [date] | TODO |
| 2 | [action] | Prevent / Detect / Mitigate | [name] | [date] | TODO |

## Lessons Learned
- **What went well:** [things that helped during the response]
- **What went poorly:** [things that hindered the response]
- **Where we got lucky:** [things that could have made it worse]
```

## Anti-Patterns (NEVER do these)

- **Root-cause before mitigate** — users are suffering while you investigate. Stop the bleeding first
- **Multiple simultaneous changes** — if you change 3 things and it resolves, you don't know which fixed it
- **Blame individuals** — post-mortems are blameless. Systems fail, not people. Ask "what system allowed this?" not "who did this?"
- **No timeline** — without a timeline, the post-mortem is a guess. Log everything as it happens
- **"Be more careful" as prevention** — human vigilance fails. Automate, validate, monitor
- **Silent incidents** — if users were affected, communicate. Silence erodes trust faster than outages
- **Skipping the post-mortem** — if it was worth responding to, it's worth learning from

## Output

Deliver:
1. Severity classification with justification
2. Impact assessment
3. Timeline of events
4. Mitigation actions taken (or recommended)
5. Root cause analysis (or investigation plan if ongoing)
6. Post-mortem document (for SEV-1/SEV-2)
7. Prioritised action items with owners and deadlines
