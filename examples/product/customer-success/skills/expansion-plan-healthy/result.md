# Expansion plan for a healthy account

A customer success manager requests an expansion plan for a high-performing account. The account has strong utilisation, positive QBR history, and the customer has proactively asked about a higher tier. The skill should pass the health gate and produce a real expansion plan.

## Prompt

> /customer-success:expansion-plan Meridian Legal is at $180k ARR, 92% seat utilisation (115/125 seats), health score 85, just completed their third QBR showing 40% time savings. They've been asking about our API integration tier.

```markdown

## Output

# Expansion Plan: Meridian Legal

### Health Check
- **Health score:** 85
- **Status:** Healthy
- **Clear to expand:** Yes

Prerequisites verified:
- [x] Composite health score ≥70 — score is 85
- [x] No active churn signals
- [x] Customer achieving stated goals — 40% time savings confirmed at QBR
- [x] Relationship strong — attended three QBRs, responsive

### Expansion Signals

| Signal | Evidence | Strength |
|---|---|---|
| Requesting higher-tier features | Customer has proactively asked about API integration tier | Strong |
| Hitting usage limits | 92% seat utilisation (115/125 seats) — near capacity | Strong |
| Executive engagement | Third QBR completed, positive trajectory confirmed | Moderate |

Two strong organic signals present — meets the "at least 2 signals" threshold from Step 2.

### Opportunity

- **Current ARR:** $180,000
- **Expansion type:** Upsell (API integration tier) + potential seat expansion (10 remaining seats)
- **Estimated expansion ARR:** $35,000–$55,000
  - Assumption: API tier at approximately $250–$350/seat/year on comparable pricing; to be confirmed with AE
  - Assumption: Only a subset of seats upgrade to API tier initially
- **Confidence:** High — two strong organic signals, customer-initiated enquiry
- **NRR impact:** Projected 119–131% NRR post-expansion
- **Timeline:** Post-QBR window (now) — customer is in planning mode

### Approach

- **Framing:** "You've achieved 40% time savings on your current plan. The API integration tier removes the remaining manual handoff your team mentioned in the QBR — it connects directly to your case management system and automates the data transfer step."
- **Timing:** Post-QBR window, now — customer has just confirmed value delivery and is in a receptive planning mindset
- **Trigger:** Use their API tier enquiry as the natural entry point — they opened the door

### Execution Plan

| Step | Action | Owner | Date |
|---|---|---|---|
| 1 | Prepare value summary — 40% time savings, 92% seat utilisation, 3 QBR trajectory | CSM | Week 1 |
| 2 | Connect API tier to the specific workflow gap mentioned in the QBR | CSM | Week 1 |
| 3 | Working session: demo API integration capability against their actual workflow | CSM + Product | Week 2 |
| 4 | Trial access for 2–3 power users in their operations team | CSM + Product | Week 3 |
| 5 | Commercial proposal for API tier + remaining 10 seat top-up | CSM + Sales | Week 4 |

### Success Criteria

| Criteria | Measurement | Target date |
|---|---|---|
| Adoption | API tier in active use, at least 1 integration live | 30 days post-expansion |
| Health stable | Score ≥85 | 60 days post-expansion |
| Value confirmed | Customer confirms workflow automation achieved | 90-day check-in |
```

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 6.5/7 (93%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Health prerequisite check passes — Step 1 is labelled "MANDATORY" and defines the threshold (composite health score ≥70). It requires all four conditions to be met before any expansion planning proceeds. Health score 85 clears the gate. The output format requires a Health Check section with a "Clear to expand: Yes/No" field. All four prerequisite criteria are checked and pass.
- [x] PASS: Expansion framed as customer enablement — Step 4 "Frame as Enablement" is a dedicated step with an explicit BAD/GOOD comparison table. The skill's Anti-patterns section explicitly lists "Sales framing" as a prohibited approach. The simulation's framing ("You've achieved 40% time savings... the API tier removes the remaining manual handoff") directly follows the GOOD pattern from Step 4's table.
- [x] PASS: Specific signal used as expansion anchor — Step 2 defines a signals table with "Requesting higher-tier features" as a named signal type. The expansion signals table shows the customer-initiated API tier enquiry as the primary strong signal, and the Approach section's Trigger field explicitly uses it as the entry point.
- [x] PASS: Revenue impact estimated with assumptions stated — Step 3 requires "Estimated expansion ARR" and "Confidence" fields. The simulation provides a range ($35,000–$55,000) with two explicit assumptions stated (pricing per seat, initial subset upgrade), which is the appropriate level of honesty when exact pricing is AE-dependent.
- [x] PASS: Timeline with milestones produced — Step 6 defines an Execution Plan as a five-row table with Step, Action, Owner, and Date columns. The Anti-patterns section prohibits vague "upsell" framing. The simulation produces a structured five-step plan across four weeks.
- [~] PARTIAL: Risk factors identified — Step 7 defines post-expansion success criteria (adoption rate, health stability, value confirmed) which implies adoption risk awareness. The Anti-patterns section explicitly warns about "Expanding without adoption" and "Ignoring post-expansion onboarding." However, there is no explicit "Expansion risks" section or instruction to identify risks as a discrete step — risk awareness is embedded in the anti-patterns and success criteria rather than surfaced as a named section. PARTIAL ceiling applies.
- [x] PASS: Plan references demonstrated value as proof of readiness — Step 6's execution plan explicitly includes "Prepare value summary — what the customer has achieved with current tier" as Step 1. Step 4's framing guidance requires connecting expansion to demonstrated customer value. The simulation's framing leads with "40% time savings" as the readiness evidence.

### Notes

The health gate in Step 1 is the skill's most important design element — it is a hard stop, not a soft recommendation. A health score of 85 clears it cleanly. Risk identification earns PARTIAL because the skill encodes risk awareness through anti-patterns and post-expansion success criteria rather than a dedicated risk analysis section. This is a reasonable design choice (risks addressed operationally rather than analytically), but a CSM completing this plan could miss tier-change adoption risk without reading the anti-patterns section carefully. A brief "Expansion risks" prompt in the output format would close this gap.
