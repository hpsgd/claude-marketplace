# Test: product prioritisation

Scenario: Competing stakeholder requests land on the CPO's desk simultaneously — a sales-driven feature request, a retention problem flagged by support, and a technical dependency from engineering. Does the CPO apply evidence-based prioritisation, challenge unvalidated requests, and route correctly?

## Prompt

We have three things all asking for attention on Helipad (our logistics SaaS) right now:

1. The sales team says we're losing deals because we don't have a mobile app. Two enterprise prospects specifically asked for it last month.
2. Support has flagged that 30% of new users never complete their first shipment booking — they drop off at the address validation step. We've had 47 tickets about it in the last 6 weeks.
3. The CTO says we need to upgrade our PostgreSQL version before Q3 or it goes end-of-life. It'll take 2 weeks of engineering time.

How do you prioritise these?

## Criteria

- [ ] PASS: Challenges the mobile app request as a solution rather than a validated problem — asks for evidence beyond two anecdotal prospects
- [ ] PASS: Identifies the address validation dropout as the highest-priority item due to quantified frequency (47 tickets, 30% dropoff) and direct impact on activation
- [ ] PASS: Applies problem frequency and severity weighting — does not treat all three requests as equal
- [ ] PASS: Escalates the PostgreSQL upgrade to the CTO rather than making a technical timeline decision
- [ ] PASS: Does not approve the mobile app without evidence of user need at scale — cites the 94% low-engagement principle or equivalent
- [ ] PASS: Produces a clear prioritisation with reasoning, not just a ranked list
- [ ] PARTIAL: References the need for a success metric on the address validation fix (e.g. target dropout rate)
- [ ] PASS: Does not make the business priority call unilaterally on scope conflicts — presents trade-offs clearly

## Output expectations

- [ ] PASS: Output explicitly challenges the mobile app request as a solution-not-problem — asks for evidence that mobile (vs responsive web) is the actual blocker, not assumes the two anecdotal prospects represent the wider market
- [ ] PASS: Output prioritises the address-validation drop-off as #1 due to quantified impact — 30% of new users dropping off plus 47 tickets in 6 weeks = direct, measurable activation problem with revenue and churn impact
- [ ] PASS: Output applies frequency × severity reasoning — does NOT treat the three requests as equal weight, and shows the math (rough) that retention/activation problems compound into ARR loss faster than missing a feature for two prospects
- [ ] PASS: Output escalates the PostgreSQL upgrade to the CTO — recognising it's a technical timeline call, not a product priority call — and proposes coordinating to fit it into the schedule alongside the activation fix
- [ ] PASS: Output does NOT approve the mobile app build without further evidence — references something like "94% of feature requests are low-engagement" or "we need quantified user research before building a major platform" before committing
- [ ] PASS: Output's prioritisation is presented with reasoning per item — not a bare ranked list — covering the user-pain rationale and the evidence weight per request
- [ ] PASS: Output recommends a specific success metric on the address-validation fix — e.g. "reduce address-step dropoff from 30% to under 15%" — so the team knows when the fix is good enough to declare done
- [ ] PASS: Output proposes a cheap discovery action on the mobile request — e.g. interview the two prospects, look at usage analytics from existing customers (mobile vs desktop), survey customers — before committing engineering time
- [ ] PASS: Output presents the trade-off honestly to stakeholders — naming who is unhappy with the recommended sequence (sales team) and how to mitigate (customer-relations action while the dropoff fix ships)
- [ ] PARTIAL: Output addresses what happens if the PostgreSQL upgrade and the address-validation fix conflict for engineering time — proposing a sequencing or parallelisation plan rather than leaving the conflict unresolved
