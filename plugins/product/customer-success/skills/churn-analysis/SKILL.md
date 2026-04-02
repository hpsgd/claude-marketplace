---
name: churn-analysis
description: Analyse churn risk for a customer or segment — diagnose root cause, design intervention, and define success criteria for retention.
argument-hint: "[customer name, segment, or churn pattern to analyse]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Analyse churn risk for $ARGUMENTS.

## Process (sequential — do not skip steps)

### Step 1: Signal Identification

What triggered this analysis? Identify all active churn signals:

| Signal category | Indicators to check |
|---|---|
| **Usage decline** | DAU/MAU trending down, key features unused, session duration decreasing |
| **Engagement drop** | Fewer logins, stopped attending meetings, unresponsive to outreach |
| **Relationship deterioration** | NPS dropped, champion left, new decision-maker unfamiliar with product |
| **Value gap** | Stated goals not met, ROI not demonstrated, competitor evaluation underway |
| **Commercial friction** | Payment failures, pricing complaints, downgrade requests, contract negotiation stalling |
| **Support escalation** | Increasing ticket volume, repeated unresolved issues, frustrated tone in tickets |

Document every active signal with specific evidence (dates, metrics, quotes).

### Step 2: Timeline Reconstruction

Build a timeline of the customer's trajectory:

| Date | Event | Signal |
|---|---|---|
| [date] | [what happened] | [what it indicates] |

Look for:
- **Inflection point** — when did things start changing? What preceded the change?
- **Accelerating decline** — is the situation getting worse faster?
- **Correlated events** — did something specific trigger the decline? (product change, champion departure, competitor launch, internal reorg)

### Step 3: Root Cause Diagnosis

Churn signals are symptoms. Diagnose the underlying cause:

| Root cause category | Questions to answer | Common indicators |
|---|---|---|
| **Product-market fit** | Does the product actually solve their problem? | Never adopted core features, using workarounds, feature requests for basic functionality |
| **Onboarding failure** | Did they reach Time to First Value? | Low adoption after 30+ days, never completed setup, no established workflow |
| **Value delivery gap** | Are they achieving their stated goals? | Goals not met, ROI not demonstrated, success metrics not defined |
| **Relationship failure** | Has the relationship degraded? | Champion left, no executive sponsor, ignored outreach |
| **Product quality** | Is the product failing them? | Recurring bugs, performance issues, data loss, broken integrations |
| **Competitive pressure** | Is a competitor winning? | Feature comparisons, pricing benchmarks, evaluation signals |
| **Internal change** | Did something change on their side? | Reorg, budget cuts, strategy shift, new leadership |

**Rules:**
- Identify the PRIMARY root cause, not just a list of everything wrong
- Distinguish between causes you can address and causes you cannot
- If the root cause is unclear, say so — don't guess

### Step 4: Churn Probability Scoring

| Factor | Low risk (1) | Medium risk (2) | High risk (3) | Score |
|---|---|---|---|---|
| **Usage trend** | Stable or growing | Declining < 4 weeks | Declining > 4 weeks | [1–3] |
| **Engagement** | Responsive, attending | Delayed responses | Unresponsive | [1–3] |
| **Sponsor status** | Active champion | Champion passive | No champion | [1–3] |
| **Value realisation** | Goals being met | Partially met | Not met | [1–3] |
| **Contract timeline** | >6 months to renewal | 3–6 months | <3 months | [1–3] |
| **Competitive activity** | No signals | Casual mentions | Active evaluation | [1–3] |

**Churn probability:**
- 6–9: Low risk — monitor
- 10–13: Medium risk — proactive intervention
- 14–18: High risk — urgent intervention required

### Step 5: Intervention Design

Design a specific intervention based on the root cause:

| Root cause | Intervention approach | Timeline |
|---|---|---|
| **Onboarding failure** | Restart onboarding — dedicated session, fast-track to value | 2 weeks |
| **Value gap** | Success planning — define metrics, demonstrate ROI, remove blockers | 4 weeks |
| **Relationship failure** | Executive engagement — new sponsor identification, business review | 2 weeks |
| **Product quality** | Engineering escalation — prioritise fixes, dedicated support | Depends on fix |
| **Competitive pressure** | Value reinforcement — feature comparison, switching costs, executive meeting | 1 week |
| **Internal change** | Stakeholder mapping — identify new decision-makers, rebuild business case | 3 weeks |

Each intervention must have:
- **Owner** — single person accountable
- **First action** — what happens within 48 hours
- **Success criteria** — measurable definition of "saved"
- **Checkpoint** — when to assess whether the intervention is working
- **Escalation path** — what happens if the intervention fails

### Step 6: Retention Economics

Quantify the business impact to frame urgency:

| Metric | Value |
|---|---|
| **ARR at risk** | [annual revenue from this customer] |
| **Replacement cost** | [cost to acquire equivalent — typically 5–7x retention cost] |
| **Lifetime value remaining** | [expected remaining contract value] |
| **Intervention cost** | [effort and resources required] |
| **ROI of retention** | [value saved vs intervention cost] |

## Anti-Patterns (NEVER do these)

- **Discounting as first response** — discounts treat the symptom (price), not the cause (value). If the product doesn't deliver value, a discount just delays churn
- **Intervention without root cause** — "schedule an executive meeting" without knowing what problem to solve wastes the executive's time and the customer's patience
- **Ignoring the timeline** — a customer declining for 6 months needs a different intervention than one who dropped suddenly last week
- **Assuming you can save everyone** — some churn is natural (company closed, product-market misfit, budget eliminated). Focus where intervention can make a difference
- **Expansion during churn risk** — never upsell an at-risk customer. Fix the health first
- **Waiting for the customer to complain** — by the time they announce they're leaving, they've already decided. Detect early

## Output Format

```markdown
# Churn Analysis: [customer/segment]

## Risk Summary
- **Churn probability:** [Low / Medium / High]
- **Risk score:** [6–18]
- **ARR at risk:** [$]
- **Time to action:** [Urgent / This week / This month]

## Active Signals
| Signal | Severity | Evidence | Duration |
|---|---|---|---|
| [signal] | [level] | [specific data] | [how long] |

## Timeline
| Date | Event | Significance |
|---|---|---|
| [date] | [event] | [what it indicates] |

## Root Cause
- **Primary:** [root cause with evidence]
- **Contributing:** [secondary factors]
- **Addressable:** [Yes / Partially / No]

## Risk Scoring
| Factor | Score (1–3) | Evidence |
|---|---|---|
| Usage trend | [n] | [detail] |
| Engagement | [n] | [detail] |
| Sponsor status | [n] | [detail] |
| Value realisation | [n] | [detail] |
| Contract timeline | [n] | [detail] |
| Competitive activity | [n] | [detail] |
| **Total** | [6–18] | |

## Intervention Plan
| Action | Owner | Timeline | Success criteria |
|---|---|---|---|
| [first action — within 48h] | [person] | [date] | [measurable outcome] |
| [follow-up actions] | [person] | [date] | [measurable outcome] |

## Retention Economics
| Metric | Value |
|---|---|
| ARR at risk | [$] |
| Replacement cost | [$] |
| Intervention ROI | [ratio] |

## Checkpoint
- **Review date:** [when to assess intervention effectiveness]
- **Success indicators:** [what improvement looks like]
- **Escalation trigger:** [when to escalate if intervention isn't working]
```

## Related Skills

- `/customer-success:health-assessment` — run a health assessment first to identify at-risk accounts, then do churn analysis on the flagged ones.
