---
name: health-assessment
description: Assess customer health across product adoption, engagement, relationship, value realisation, and commercial dimensions. Identify at-risk accounts and recommend interventions.
argument-hint: "[customer name, segment, or 'portfolio' for all accounts]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Assess customer health for $ARGUMENTS.

## Process (sequential — do not skip steps)

### Step 1: Identify Data Sources

Before scoring, establish where health signals come from:

| Signal type | Where to find it |
|---|---|
| **Product usage** | Analytics dashboard, event tracking, DAU/MAU metrics |
| **Engagement** | Login frequency, feature usage trends, session duration |
| **Relationship** | NPS/CSAT scores, meeting attendance, executive sponsor status |
| **Value realisation** | Customer-stated goals, ROI metrics, outcome tracking |
| **Commercial** | Billing status, contract terms, renewal date, pricing tier |

If data sources are unavailable, note the gap — a health score with missing dimensions is less reliable but still useful.

### Step 2: Score Each Dimension (0–100)

Score every dimension. Do not skip a dimension because data is sparse — estimate with documented reasoning.

| Dimension | Weight | Scoring criteria |
|---|---|---|
| **Product adoption** | 30% | Feature usage breadth, DAU/MAU ratio, time in app. 80+: using core + advanced features. 60–79: using core features. 40–59: sporadic use. <40: minimal or declining |
| **Engagement** | 25% | Login frequency trend, support interactions, content consumption. 80+: increasing or stable high usage. 60–79: stable. 40–59: declining. <40: disengaged |
| **Relationship** | 20% | NPS/CSAT score, executive sponsor engagement, meeting attendance. 80+: promoter, active sponsor. 60–79: passive, sponsor identified. 40–59: detractor or no sponsor. <40: unresponsive |
| **Value realisation** | 15% | Achieving stated goals, ROI metrics, expansion signals. 80+: exceeding goals. 60–79: on track. 40–59: behind on goals. <40: no measurable value |
| **Commercial** | 10% | Payment status, contract term remaining, pricing sensitivity. 80+: paid on time, long-term contract. 60–79: current, standard terms. 40–59: payment issues or pricing complaints. <40: at risk of non-renewal |

### Step 3: Calculate Composite Score

```
Composite = (Adoption × 0.30) + (Engagement × 0.25) + (Relationship × 0.20)
           + (Value × 0.15) + (Commercial × 0.10)
```

### Step 4: Classify Health Status

| Health | Score | Meaning | Response |
|---|---|---|---|
| **Healthy** | 80–100 | Customer is succeeding and engaged | Nurture. Identify expansion opportunities. Ask for referrals |
| **Neutral** | 60–79 | No immediate risk, but not thriving | Monitor. Quarterly check-in. Look for engagement opportunities |
| **At Risk** | 40–59 | Multiple warning signals present | Intervene within 1 week. Proactive outreach. Root cause analysis |
| **Critical** | 0–39 | Active churn risk | Escalate immediately. Intervention plan within 48 hours |

### Step 5: Identify Active Risk Signals

Check for churn risk indicators regardless of composite score — a single critical signal can override the composite:

| Signal | Risk level | Response |
|---|---|---|
| Usage declining over 2+ weeks | Medium | Proactive check-in — "noticed you haven't used X recently" |
| Key feature not adopted after 30 days | High | Onboarding follow-up — offer training, remove friction |
| Support tickets increasing | Medium | Pattern analysis — is the product failing them? |
| Champion/sponsor left the company | High | Identify new sponsor immediately |
| NPS < 7 or CSAT declining | High | Personal outreach — understand the root cause |
| Payment issues (failed charge, downgrade inquiry) | Critical | Retention outreach same day |
| Competitor evaluation signals | Critical | Executive engagement + value reinforcement |

**Rule:** A Healthy composite with a Critical signal = At Risk. The signal overrides the score.

### Step 6: Recommend Interventions

For every account classified At Risk or Critical, define a specific intervention:

| Intervention type | When to use | Actions |
|---|---|---|
| **Engagement rescue** | Usage declining, features unadopted | Training session, workflow review, success plan |
| **Relationship repair** | NPS low, sponsor gone, unresponsive | Executive outreach, new sponsor identification, business review |
| **Value acceleration** | Not achieving goals, no measurable ROI | Goal review, success metrics definition, use case workshop |
| **Commercial save** | Payment issues, downgrade inquiry, competitor evaluation | Pricing review, value demonstration, executive engagement |

Each intervention has:
- **Owner** — who leads the intervention
- **Timeline** — when to start, when to review progress
- **Success criteria** — what does "saved" look like?
- **Escalation** — what happens if the intervention doesn't work?

### Step 7: Portfolio Summary (if assessing multiple accounts)

Aggregate across accounts for portfolio-level insights.

## Anti-Patterns (NEVER do these)

- **Scoring without data** — estimate with documented reasoning, don't fabricate precision. "Adoption: 65 (estimated — no analytics dashboard available)" is honest
- **Composite score only** — always break down by dimension. A composite of 60 could be five dimensions at 60 or one at 100 and one at 0 — very different situations
- **Ignoring single critical signals** — a customer with a composite of 85 whose champion just left is At Risk, not Healthy
- **Intervention without root cause** — "schedule a call" is not an intervention plan. Why is the customer at risk? What specific problem will the intervention solve?
- **One-time assessment** — health monitoring is continuous. Define the re-assessment cadence (monthly for At Risk, quarterly for Neutral, semi-annually for Healthy)
- **Expanding unhealthy accounts** — expansion conversations with At Risk customers accelerate churn. Fix the health first

## Output Format

```markdown
# Customer Health Assessment: [account/segment/portfolio]

## Summary
- **Overall health:** [Healthy / Neutral / At Risk / Critical]
- **Composite score:** [0–100]
- **Assessment date:** [date]
- **Data confidence:** [High / Medium / Low — based on data availability]

## Dimension Scores

| Dimension | Weight | Score | Trend | Key signals |
|---|---|---|---|---|
| Product adoption | 30% | [0–100] | [↑ / → / ↓] | [specific evidence] |
| Engagement | 25% | [0–100] | [↑ / → / ↓] | [specific evidence] |
| Relationship | 20% | [0–100] | [↑ / → / ↓] | [specific evidence] |
| Value realisation | 15% | [0–100] | [↑ / → / ↓] | [specific evidence] |
| Commercial | 10% | [0–100] | [↑ / → / ↓] | [specific evidence] |

## Active Risk Signals
| Signal | Risk level | Detail |
|---|---|---|
| [signal] | [level] | [specific observation] |

## Recommended Interventions
| Intervention | Owner | Timeline | Success criteria |
|---|---|---|---|
| [action] | [person] | [start–review] | [what success looks like] |

## Next Assessment
- **Date:** [when]
- **Trigger for earlier review:** [what would warrant reassessing sooner]
```

## Related Skills

- `/customer-success:churn-analysis` — when health assessment flags an account as at-risk, run a churn analysis to identify specific intervention opportunities.
- `/customer-success:expansion-plan` — when health assessment shows a healthy, engaged account, explore expansion opportunities.
