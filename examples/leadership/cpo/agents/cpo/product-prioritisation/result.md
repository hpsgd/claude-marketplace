# Product Prioritisation

Scenario: Competing stakeholder requests land on the CPO's desk simultaneously — a sales-driven feature request, a retention problem flagged by support, and a technical dependency from engineering. Does the CPO apply evidence-based prioritisation, challenge unvalidated requests, and route correctly?

## Prompt

> We have three things all asking for attention on Helipad (our logistics SaaS) right now:
> 
> 1. The sales team says we're losing deals because we don't have a mobile app. Two enterprise prospects specifically asked for it last month.
> 2. Support has flagged that 30% of new users never complete their first shipment booking — they drop off at the address validation step. We've had 47 tickets about it in the last 6 weeks.
> 3. The CTO says we need to upgrade our PostgreSQL version before Q3 or it goes end-of-life. It'll take 2 weeks of engineering time.
> 
> How do you prioritise these?

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

**Address validation fix first, PostgreSQL second, mobile app third** — here's the reasoning:

**1. Address validation drop-off (immediate)**
A 30% activation failure at a known, specific step is the highest-leverage thing on this list. Every user you acquire hits this wall. Fixing it compounds: it improves revenue from your *existing* acquisition spend, reduces the 47-ticket support load, and the scope is bounded (one step, reproducible failure). Build a mobile app onto a broken funnel and you've just spent months bringing more people to the same cliff edge.

**2. PostgreSQL upgrade (schedule now, execute before Q3)**
This is a deadline-driven risk item, not an urgency-today item. Two weeks of known scope with a hard external deadline — put it on the calendar now so it doesn't get squeezed out, but it doesn't need to block the activation fix.

**3. Mobile app (discovery, not commitment)**
Two prospects asking is signal worth investigating, not a build order. Before committing 3-6+ months of engineering, I'd want to know: how many *other* prospects raised it, was it a blocker or a nice-to-have, and what do your existing users actually do (are they already on mobile web?). A cross-platform framework (React Native/Flutter) changes the cost calculus significantly versus native. Run discovery in parallel while #1 and #2 are in flight.

The counter-argument worth raising with the CTO and sales team: if you close those two enterprise deals, do they have enough ARR to justify fast-tracking mobile? That's the only scenario where I'd revisit the order.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PARTIAL |
| Score | 11.0/17.0 (65%) |
| Evaluated | 2026-05-01 |
| Target duration | 23441 ms |
| Target cost | $0.0929 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Challenges the mobile app request as a solution rather than a validated problem — asks for evidence beyond two anecdotal prospects | PASS | "Two prospects asking is signal worth investigating, not a build order. Before committing 3-6+ months of engineering, I'd want to know: how many *other* prospects raised it, was it a blocker or a nice-to-have..." |
| c2 | Identifies the address validation dropout as the highest-priority item due to quantified frequency (47 tickets, 30% dropoff) and direct impact on activation | PASS | "A 30% activation failure at a known, specific step is the highest-leverage thing on this list" and explicitly references 47-ticket support load and activation impact. |
| c3 | Applies problem frequency and severity weighting — does not treat all three requests as equal | PASS | Three clearly differentiated dispositions: address validation = "immediate"; PostgreSQL = "schedule now, not urgency-today"; mobile = "discovery, not commitment". |
| c4 | Escalates the PostgreSQL upgrade to the CTO rather than making a technical timeline decision | FAIL | The output makes the scheduling decision itself: "put it on the calendar now so it doesn't get squeezed out." The CTO is mentioned only in the closing counter-argument about mobile ARR, not in the PostgreSQL section. |
| c5 | Does not approve the mobile app without evidence of user need at scale — cites the 94% low-engagement principle or equivalent | PARTIAL | Output does not approve the mobile build and challenges the two-prospect sample, but cites no named principle or statistic equivalent to "94% of feature requests are low-engagement" — the reasoning is qualitative only. |
| c6 | Produces a clear prioritisation with reasoning, not just a ranked list | PASS | Each of the three items has a dedicated section with substantive rationale (activation funnel logic, deadline-driven risk framing, discovery vs. commitment framing). |
| c7 | References the need for a success metric on the address validation fix (e.g. target dropout rate) | FAIL | No success metric is mentioned for the address-validation fix. The output does not suggest a target dropout rate or any quantified done-condition. |
| c8 | Does not make the business priority call unilaterally on scope conflicts — presents trade-offs clearly | PASS | "The counter-argument worth raising with the CTO and sales team: if you close those two enterprise deals, do they have enough ARR to justify fast-tracking mobile? That's the only scenario where I'd revisit the order." |
| c9 | Output explicitly challenges the mobile app request as a solution-not-problem — asks for evidence that mobile (vs responsive web) is the actual blocker, not assumes the two anecdotal prospects represent the wider market | PASS | "what do your existing users actually do (are they already on mobile web?)" directly challenges the mobile-vs-web assumption; "Two prospects asking is signal worth investigating, not a build order" challenges the sample size. |
| c10 | Output prioritises the address-validation drop-off as #1 due to quantified impact — 30% of new users dropping off plus 47 tickets in 6 weeks = direct, measurable activation problem with revenue and churn impact | PASS | "A 30% activation failure... is the highest-leverage thing on this list" and "reduces the 47-ticket support load" and "improves revenue from your *existing* acquisition spend". |
| c11 | Output applies frequency × severity reasoning — does NOT treat the three requests as equal weight, and shows the math (rough) that retention/activation problems compound into ARR loss faster than missing a feature for two prospects | PARTIAL | Output makes the compounding argument qualitatively ("Fixing it compounds", "brings more people to the same cliff edge") but shows no rough arithmetic linking 30% dropout to ARR loss vs. two-prospect deal risk. |
| c12 | Output escalates the PostgreSQL upgrade to the CTO — recognising it's a technical timeline call, not a product priority call — and proposes coordinating to fit it into the schedule alongside the activation fix | FAIL | The output schedules PostgreSQL itself ("put it on the calendar now") without framing it as a CTO-owned technical call. No explicit escalation or coordination proposal with engineering leadership. |
| c13 | Output does NOT approve the mobile app build without further evidence — references something like "94% of feature requests are low-engagement" or "we need quantified user research before building a major platform" before committing | PARTIAL | Output withholds approval and calls for discovery, but cites no named principle, statistic, or framework (e.g., "94% of feature requests") to back the caution — reasoning remains anecdotal-counter rather than principled. |
| c14 | Output's prioritisation is presented with reasoning per item — not a bare ranked list — covering the user-pain rationale and the evidence weight per request | PASS | Each ranked item has its own headed section with user-pain rationale and evidence weight explicitly discussed (activation spend, deadline-driven risk, anecdotal vs. quantified evidence). |
| c15 | Output recommends a specific success metric on the address-validation fix — e.g. "reduce address-step dropoff from 30% to under 15%" — so the team knows when the fix is good enough to declare done | FAIL | No specific success metric or target is provided for the address-validation fix anywhere in the output. |
| c16 | Output proposes a cheap discovery action on the mobile request — e.g. interview the two prospects, look at usage analytics from existing customers (mobile vs desktop), survey customers — before committing engineering time | PARTIAL | "Run discovery in parallel while #1 and #2 are in flight" is proposed, and discovery questions are listed (how many other prospects, blocker or nice-to-have, mobile web usage), but no specific low-cost action (interview, analytics pull, survey) is named. |
| c17 | Output presents the trade-off honestly to stakeholders — naming who is unhappy with the recommended sequence (sales team) and how to mitigate (customer-relations action while the dropoff fix ships) | PARTIAL | Sales team is named in the counter-argument section, but no mitigation action is proposed (e.g., communicating to the two prospects that mobile is on the roadmap, or a customer-success touchpoint). |
| c18 | Output addresses what happens if the PostgreSQL upgrade and the address-validation fix conflict for engineering time — proposing a sequencing or parallelisation plan rather than leaving the conflict unresolved | PARTIAL | "it doesn't need to block the activation fix" implicitly resolves the conflict by allowing parallelism, but no concrete sequencing or resource plan is offered. |

### Notes

The output is strong on prioritisation rationale, funnel logic, and challenging the mobile app anecdote — c1, c2, c3, c6, c8, c9, c10, c14 all pass cleanly. The main gaps are: (1) the PostgreSQL upgrade is treated as a product scheduling call rather than escalated to the CTO (c4, c12 both fail); (2) no success metric is set for the address-validation fix (c15 fails, c7 fails); (3) the output invokes no named principle (94% low-engagement or equivalent) to back its mobile app caution (c5, c13 both partial); and (4) the discovery plan for mobile is directional but not actionable (c16 partial). The trade-off section names the sales team as a stakeholder but proposes no mitigation action (c17 partial). Overall the response is competent CPO reasoning but stops short of the operational specificity the rubric rewards.
