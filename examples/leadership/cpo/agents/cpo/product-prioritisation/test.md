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
