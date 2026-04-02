---
name: write-onboarding-playbook
description: "Create a customer onboarding playbook with milestones, success criteria, and escalation triggers. Produces a structured playbook for a customer segment. Use when formalising onboarding for a new segment or improving time-to-value."
argument-hint: "[customer segment or product tier to create onboarding playbook for]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Write Onboarding Playbook

Create a customer onboarding playbook for $ARGUMENTS. Time-to-first-value is the north star metric — every milestone, action, and escalation exists to shorten it.

## Step 1: Define the segment (mandatory)

```markdown
### Segment definition

| Element | Detail |
|---|---|
| **Segment** | [e.g. Enterprise, Mid-Market, Self-Serve, specific vertical] |
| **Typical company size** | [employee count, ARR range] |
| **Technical sophistication** | [High — dedicated engineering team / Medium — IT generalist / Low — non-technical] |
| **Typical goals** | [top 3 outcomes they want from the product] |
| **Decision-maker** | [who bought it and why] |
| **Day-to-day users** | [who will actually use it] |
| **Common integrations** | [systems they need to connect] |
| **Contract type** | [annual, monthly, usage-based — affects urgency] |
```

**Rules for scope:**
- Enterprise onboarding is NOT self-serve onboarding with more meetings. They are fundamentally different playbooks
- If the segment has sub-segments with different needs, create separate playbooks
- Identify the gap between who bought (decision-maker) and who uses (end user) — this gap kills onboarding

**Output:** Segment definition table.

## Step 2: Define time-to-first-value (mandatory)

```markdown
### Time-to-first-value (TTFV)

| Element | Detail |
|---|---|
| **"First value" definition** | [specific outcome — not "completed setup" but "sent first campaign" or "processed first payment"] |
| **Target TTFV** | [days from contract signed to first value achieved] |
| **Measurement** | [how you know first value was achieved — product event, metric threshold, customer confirmation] |
| **Current TTFV** | [what it is today, if known] |
| **Benchmark** | [industry or competitor benchmark, if available] |
```

**Rules for TTFV:**
- "First value" must be something the CUSTOMER considers valuable, not something you consider complete. "Completed onboarding call" is not first value — "generated first report with their own data" is
- Target TTFV should be aggressive but achievable. If current is 45 days, don't target 5 days — target 25, then iterate
- If you cannot measure TTFV automatically, it is not a real metric. Build the instrumentation first

**Output:** TTFV definition with target and measurement.

## Step 3: Design milestones (mandatory)

Design the milestone sequence from contract signature to onboarding complete:

```markdown
### Onboarding milestones

| # | Milestone | Target day | Success criteria | Owner | Verification method | Escalation trigger |
|---|---|---|---|---|---|---|
| 1 | Kickoff complete | Day 1–3 | Goals aligned, stakeholders identified, access provisioned | CS | Kickoff notes signed off | No kickoff within 5 business days of contract |
| 2 | Technical setup | Day 3–7 | [integration connected, data imported, environment configured] | CS + Customer IT | [automated health check / manual verification] | Setup not started by Day 5 |
| 3 | First use | Day 7–14 | [first real task completed with own data — not a demo] | CS | [product event triggered] | No login by Day 10 |
| 4 | First value | Day 14–21 | [TTFV achieved — per Step 2 definition] | CS | [metric threshold met] | No value by Day 25 |
| 5 | Team rollout | Day 21–30 | [target adoption % across team — not just champion] | CS + Champion | [usage analytics] | Only 1 user active by Day 25 |
| 6 | Handoff to BAU | Day 30–45 | [success criteria met, QBR scheduled, health score green] | CS | [handoff checklist complete] | Health score not green by Day 40 |
```

**Rules for milestones:**
- Every milestone has measurable success criteria — "complete onboarding call" is not measurable
- Every milestone has an escalation trigger with a specific day threshold — no open-ended milestones
- Milestones are sequential. Milestone 3 cannot start until Milestone 2 success criteria are met
- Adjust day targets per segment — enterprise may need 2x the timeline of self-serve

**Output:** Complete milestone table with all columns filled.

## Step 4: Write the kickoff agenda (mandatory)

```markdown
### Kickoff meeting agenda

**Duration:** [60 min for enterprise, 30 min for mid-market, async for self-serve]
**Attendees:** [CS lead, champion, technical lead, executive sponsor — specify required vs optional]

| Time | Topic | Owner | Output |
|---|---|---|---|
| 0–10 min | Introductions and role mapping | CS | Know who does what on both sides |
| 10–20 min | Goals alignment | CS + Champion | Documented success criteria (customer's words, not yours) |
| 20–30 min | Technical requirements | CS + Tech lead | Integration plan, data migration scope, access requirements |
| 30–45 min | Milestone walkthrough | CS | Shared timeline with dates (not "week 2" — actual dates) |
| 45–55 min | Access provisioning | CS | All accounts created, invites sent, SSO configured |
| 55–60 min | Next steps | CS | First 3 actions with owners and deadlines |

### Kickoff anti-patterns
- Demoing the product during kickoff (they already bought it — focus on THEIR goals, not your features)
- Skipping the executive sponsor (if they don't attend kickoff, they won't attend the QBR either)
- Agreeing to vague goals ("improve efficiency" — push for "reduce report generation from 4 hours to 30 minutes")
```

**Output:** Kickoff agenda with timing, owners, and outputs per topic.

## Step 5: Map common blockers (mandatory)

```markdown
### Common blockers

| Blocker | Early warning sign | Resolution | Escalation path |
|---|---|---|---|
| **Champion unavailable** | Missed first 2 meetings, delayed responses >3 days | Identify backup contact, shift to async, propose condensed schedule | CS Manager → Account Executive |
| **Technical integration delayed** | No API key generated by Day 5, IT team unresponsive | Provide step-by-step guide, offer technical call, involve solutions engineer | Solutions Engineering → Engineering |
| **Data quality issues** | Import fails, mapping errors, incomplete data | Provide data template, offer data audit, manual assist first import | CS → Data team |
| **Stakeholder misalignment** | Different goals mentioned by different people, scope creep | Facilitate alignment meeting, document agreed scope, get sign-off | CS Manager → Executive Sponsor |
| **Security/compliance review** | InfoSec blocks integration, SSO requirements not met | Provide security documentation, schedule InfoSec call, fast-track compliance cert | CS → Security team |
| **Low user adoption** | Only champion logging in, team not invited, no training completed | Champion-led training, team onboarding session, quick-start guides | CS Manager → Champion + Exec Sponsor |
```

**Rules for blockers:**
- Every blocker needs an early warning sign — by the time the customer tells you, you've already lost days
- Resolution should be a specific action, not "follow up" or "check in"
- Escalation path should name roles, not "escalate as needed"

**Output:** Blocker table with early warning signs, resolutions, and escalation paths.

## Step 6: Define handoff criteria (mandatory)

```markdown
### Handoff: Onboarding → BAU Customer Success

**Handoff is complete when ALL of the following are true:**

| Criterion | Measurement | Status |
|---|---|---|
| TTFV achieved | [product event / metric — from Step 2] | [ ] |
| Target user adoption reached | [X% of licensed users active in last 7 days] | [ ] |
| Champion identified and engaged | [Named champion, responding within 24h] | [ ] |
| Executive sponsor confirmed | [Named sponsor, attended at least 1 meeting] | [ ] |
| Success criteria documented | [Written, agreed, measurable — from kickoff] | [ ] |
| Health score green | [Composite health score above threshold] | [ ] |
| First QBR scheduled | [Date set, attendees confirmed] | [ ] |

**Handoff process:**
1. Onboarding CS completes handoff document with milestone history
2. BAU CS reviews document and account before introduction
3. Warm introduction — onboarding CS introduces BAU CS to champion
4. BAU CS conducts relationship-building call (NOT a repeat of kickoff)
5. First QBR scheduled within 30 days of handoff

**If handoff criteria not met by Day [X]:**
- Extend onboarding with CS Manager approval
- Root cause analysis — why did onboarding stall?
- Feed findings back to improve this playbook
```

**Output:** Handoff checklist and process.

## Rules

- **Time-to-first-value is THE metric.** Every milestone, meeting, and action exists to shorten TTFV. If an activity doesn't contribute to TTFV, remove it from the playbook.
- **Milestones must have measurable success criteria.** "Complete onboarding call" is not a success criterion. "Customer has processed first transaction with own data" is.
- **Every milestone needs an escalation trigger.** If the customer stalls at a milestone, the playbook must define what happens automatically — not wait for someone to notice.
- **Segment-specific, not generic.** An enterprise playbook with white-glove service is not a self-serve playbook with extra steps. Design for the segment.
- **Never assume the champion is the user.** The person who bought the product often isn't the person who uses it daily. Onboard both.
- **Measure, don't assume.** If you can't measure whether a milestone was achieved, the milestone is useless.

## Output Format

```markdown
# Onboarding Playbook: [segment/tier]

## Segment Definition
[From Step 1]

## Time-to-First-Value
[From Step 2]

## Milestones
[Full milestone table from Step 3]

## Kickoff Agenda
[From Step 4]

## Common Blockers
[Blocker table from Step 5]

## Handoff Criteria
[Checklist and process from Step 6]

---
Segment: [segment name]
Target TTFV: [X days]
Milestone count: [N]
Last updated: [date]
```

## Related Skills

- `/customer-success:health-assessment` — health score tracks onboarding progress. A red health score during onboarding triggers escalation per the milestone table.
- `/customer-success:churn-analysis` — onboarding failure is a top churn cause. Failed onboarding playbooks feed directly into churn root cause analysis.

Use the onboarding playbook template (`templates/onboarding-playbook.md`) for output structure.
