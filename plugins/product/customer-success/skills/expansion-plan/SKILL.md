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

**Expansion only happens with healthy customers.** Compute and report the basics from the inputs given (don't wait for a separate health report):

- [ ] **Seat / licence utilisation** — active users ÷ licensed seats, as a percentage. Flag below 60% as unhealthy for expansion purposes
- [ ] Composite health score >= 70 (Healthy or strong Neutral)
- [ ] No active churn signals
- [ ] Customer has achieved stated goals or is on track
- [ ] Relationship is strong — responsive, engaged, sponsor identified

If health is below threshold: **STOP.** Do not produce a normal expansion plan. Switch to the unhealthy-path response below.

**Unhealthy-path response (when the gate fires):**

1. **Quantified recovery targets** — state what needs to improve and by how much, with a window. Example: "active users need to reach 27 (60% of 45 seats) sustained over a 60-day window before expansion can be reconsidered." Run `/health-assessment` to diagnose root cause.
1. **Sequence: recover → reassess → plan** — first restore adoption (typical 60–90 days), then reassess expansion fit against the readiness signals in Step 2, then plan only if signals align. Do not collapse these into one recommendation.
1. **Right-size before expand** — if the customer is paying for substantially more capacity than they use (e.g. 33 of 45 seats unused), consider whether reducing seat count is the correct next step before any expansion conversation. Protecting the relationship beats protecting ARR.
1. **Internal communication to AE / sales** — draft a short note explaining why expansion is on hold and what would unblock it. Frame as protecting the customer relationship, not blocking revenue. Include the recovery targets and the reassessment date.
1. **Upstream feedback** — if the gap looks like a sales/CS handoff or scoping problem (sold 45, only ever used 12), flag it for the AE and CS lead so it's not repeated.

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

**Quantified readiness thresholds.** Signal presence is necessary but not sufficient. Before advancing an expansion conversation, the account should also clear: seat / licence utilisation >= 60% sustained over the last 30–60 days, composite health score >= 70, active engagement on more than one core feature, positive relationship and value scores, and an executive sponsor confirmed. State the actual numbers for this customer — don't say "they're doing well."

### Step 3: Quantify the Opportunity

| Metric | Value |
|---|---|
| **Current ARR** | [$] |
| **Expansion type** | [Upgrade / Upsell / Cross-sell / Seat expansion] |
| **Estimated expansion ARR** | [$] |
| **Confidence** | [High / Medium / Low — based on signal strength] |
| **Timeline** | [When to propose — aligned with customer's planning cycle] |

**Show the math.** Don't just give a single ARR figure. Document the pricing assumption (per-seat, flat, tier delta), the relevant volume (seats in scope, modules in scope), and at least two adoption scenarios (e.g. 100% adoption vs 50% adoption). State each assumption explicitly so the customer-facing recommendation can be defended.

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
| 1 | Prepare value summary — what the customer has achieved with current tier. Connect demonstrated outcomes to the readiness narrative explicitly: "they've already proven X with the current tier, which is why they're ready for Y." | CSM | [date] |
| 2 | Connect expansion to customer's stated goals | CSM | [date] |
| 3 | Propose in context (meeting, QBR, or response to signal) | CSM | [date] |
| 4 | Demo or trial of expanded capability | CSM + Product | [date] |
| 5 | Commercial proposal | CSM + Sales | [date] |

**Phase the milestones.** For non-trivial expansions (new tier, new module, integration work), the execution plan should walk through phases the customer can recognise: discovery, scoping, trial, rollout, and post-rollout review. Express milestones at the granularity the customer plans in (weeks for technical work, months for org-wide rollout) — not just "step 1 / step 2."

### Step 7: Identify Expansion Risks

Surface risks specific to this expansion as a named deliverable — don't bury them in the success criteria. For each risk, state what it is, why it applies to this customer/tier, and the gating action that mitigates it.

Tailor risks to the expansion type. Examples:

- **New tier with technical dependencies (API, integrations)** — does the customer have engineering capacity to consume it? If not, the tier becomes shelfware. Gate the upsell on confirming technical readiness.
- **Seat expansion** — onboarding capacity, training, change-management load. Gate on a rollout plan.
- **Cross-sell into a new module** — does the customer have the workflow context for it? Gate on a use-case validation.
- **Multi-year contract** — exposure to changing requirements. Gate on contract terms that allow scope adjustment.

### Step 8: Post-Expansion Success Criteria

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
- **Seat utilisation:** [active / licensed = %]
- **Health score:** [0–100]
- **Status:** [Healthy / Neutral / Unhealthy]
- **Clear to expand:** [Yes / No — if No, complete the Unhealthy-Path Response below and stop]

## Unhealthy-Path Response (only if Clear to expand = No)
- **Recovery targets:** [quantified — e.g. active users to N (X% of seats) sustained over Y days]
- **Sequence:** recover ([window]) → reassess on [date] → plan only if signals align
- **Right-sizing consideration:** [if substantially over-licensed, recommend seat reduction before expansion]
- **AE / sales communication:** [short note explaining the hold, the unblock criteria, and the reassessment date]
- **Upstream feedback:** [if oversell / handoff issue, flag for AE and CS lead]

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

## Risks
| Risk | Why it applies | Gating action |
|---|---|---|
| [risk specific to this tier/expansion] | [reason it applies to this customer] | [what must be true before proceeding] |

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
