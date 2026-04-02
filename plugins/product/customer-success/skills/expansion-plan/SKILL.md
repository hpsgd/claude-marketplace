---
name: expansion-plan
description: Plan expansion revenue for a healthy customer — identify signals, frame as enablement, and design an expansion approach.
argument-hint: "[customer name or segment to plan expansion for]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Plan expansion for $ARGUMENTS.

## Process (sequential — do not skip steps)

### Step 1: Health Prerequisite Check (MANDATORY)

**Expansion only happens with healthy customers.** Verify before proceeding:

- [ ] Composite health score >= 70 (Healthy or strong Neutral)
- [ ] No active churn signals
- [ ] Customer has achieved stated goals or is on track
- [ ] Relationship is strong — responsive, engaged, sponsor identified

If health is below threshold: **STOP.** Fix the health first. Run `/health-assessment` to diagnose. Proposing expansion to an unhealthy customer accelerates churn.

### Step 2: Identify Expansion Signals

Look for organic signals that the customer is ready for more:

| Signal | What it means | Expansion type |
|---|---|---|
| **Hitting usage limits** | They need more capacity | Upgrade — more volume, higher tier |
| **Requesting higher-tier features** | They see value in advanced capabilities | Upsell — demonstrate the specific feature |
| **Team size growing** | More users need access | Seat expansion — frame as team enablement |
| **New use cases emerging** | Product stickiness increasing | Cross-sell — adjacent products or modules |
| **Executive engagement increasing** | Strategic importance growing | Contract expansion — multi-year, broader scope |
| **Referrals or advocacy** | Customer is a promoter | Referral program + case study opportunity |

**Rules:**
- At least 2 signals should be present before initiating expansion conversation
- Signals should be organic (customer-driven), not sales-driven
- Document specific evidence for each signal (dates, usage data, quotes)

### Step 3: Quantify the Opportunity

| Metric | Value |
|---|---|
| **Current ARR** | [$] |
| **Expansion type** | [Upgrade / Upsell / Cross-sell / Seat expansion] |
| **Estimated expansion ARR** | [$] |
| **Confidence** | [High / Medium / Low — based on signal strength] |
| **Timeline** | [When to propose — aligned with customer's planning cycle] |

### Step 4: Frame as Enablement

Expansion is framed as enabling the customer's success, not as a sales transaction.

| Framing | BAD (sales) | GOOD (enablement) |
|---|---|---|
| **Upgrade** | "Would you like to upgrade to Pro?" | "You're generating 3x more reports than last quarter — let's make sure the platform keeps up with your growth" |
| **Seats** | "Can we add 10 more seats?" | "Your team has grown to 25 — right now only 15 have access. Let's get everyone onboarded" |
| **Upsell** | "Our analytics tier has great features" | "You mentioned wanting to track conversion rates — that's exactly what the Analytics module does" |
| **Cross-sell** | "We also have Product X" | "Several customers with your workflow have found Product X removes the manual step you mentioned" |

### Step 5: Timing Strategy

| Timing trigger | Why it works |
|---|---|
| **After a success milestone** | Customer has just experienced value — receptive to more |
| **During annual planning** | Budget allocation is happening — get included |
| **New team member joining** | Natural moment to discuss access and onboarding |
| **Feature request conversation** | Customer has expressed a need — connect it to the solution |
| **QBR / business review** | Structured setting to review value and discuss growth |

**Avoid:** proposing during a support escalation, mid-incident, when renewal is contentious, or when the champion is distracted by internal priorities.

### Step 6: Design the Approach

| Step | Action | Owner | Date |
|---|---|---|---|
| 1 | Prepare value summary — what the customer has achieved with current tier | CSM | [date] |
| 2 | Connect expansion to customer's stated goals | CSM | [date] |
| 3 | Propose in context (meeting, QBR, or response to signal) | CSM | [date] |
| 4 | Demo or trial of expanded capability | CSM + Product | [date] |
| 5 | Commercial proposal | CSM + Sales | [date] |

### Step 7: Post-Expansion Success Criteria

Define what a successful expansion looks like beyond the transaction:

| Criteria | Measurement | Target |
|---|---|---|
| **Adoption** | New features/seats/capacity in use within 30 days | >50% utilisation |
| **Health stability** | Health score stable or improved post-expansion | Score >= pre-expansion |
| **Value delivery** | Customer confirms expansion solved their need | Positive feedback |
| **Relationship** | Expansion felt like enablement, not a sales push | NPS maintained or improved |

## Anti-Patterns (NEVER do these)

- **Expanding unhealthy accounts** — expansion to an at-risk customer is pouring fuel on fire. Fix health first. Run `/health-assessment` before any expansion conversation
- **Sales framing** — "Would you like to upgrade?" is a sales pitch. "Your growth is outpacing your current plan — let's fix that" is enablement
- **Forcing timing** — expansion should align with the customer's planning cycle, not your quarterly targets
- **Expanding without adoption** — if the customer isn't using current features, adding more features increases complexity without value
- **Ignoring post-expansion onboarding** — new features without onboarding = shelfware. Plan adoption support
- **Single signal expansion** — one usage spike isn't a trend. Wait for sustained signals or multiple corroborating signals

## Output Format

```markdown
# Expansion Plan: [customer name]

## Health Check
- **Health score:** [0–100]
- **Status:** [Healthy / Neutral]
- **Clear to expand:** [Yes / No — if No, stop here]

## Expansion Signals
| Signal | Evidence | Strength |
|---|---|---|
| [signal] | [specific data/quote] | [Strong / Moderate] |

## Opportunity
- **Current ARR:** [$]
- **Expansion type:** [Upgrade / Upsell / Cross-sell / Seats]
- **Estimated expansion ARR:** [$]
- **Confidence:** [High / Medium / Low]
- **NRR impact:** [projected NRR after expansion]

## Approach
- **Framing:** [how to position as enablement]
- **Timing:** [when and why]
- **Trigger:** [event or conversation to use as entry point]

## Execution Plan
| Step | Action | Owner | Date |
|---|---|---|---|
| 1 | [action] | [person] | [date] |

## Success Criteria
| Criteria | Measurement | Target date |
|---|---|---|
| Adoption | [metric] | [date] |
| Health stable | [score >= current] | [date] |
| Value confirmed | [customer feedback] | [date] |
```
