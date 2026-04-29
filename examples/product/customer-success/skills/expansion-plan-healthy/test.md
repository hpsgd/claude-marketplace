# Test: expansion plan for a healthy account

Scenario: A customer success manager requests an expansion plan for a high-performing account. The account has strong utilisation, positive QBR history, and the customer has proactively asked about a higher tier. The skill should pass the health gate and produce a real expansion plan.

## Prompt

/customer-success:expansion-plan Meridian Legal is at $180k ARR, 92% seat utilisation (115/125 seats), health score 85, just completed their third QBR showing 40% time savings. They've been asking about our API integration tier.

## Criteria

- [ ] PASS: Health prerequisite check passes and expansion planning proceeds
- [ ] PASS: Expansion is framed as customer enablement, not a sales motion
- [ ] PASS: The specific signal (customer asking about API tier) is used as the expansion anchor
- [ ] PASS: Revenue impact is estimated with assumptions stated
- [ ] PASS: A timeline with milestones is produced, not just "upsell them"
- [ ] PARTIAL: Risk factors for the expansion are identified (e.g., adoption risk on a new tier)
- [ ] PASS: The plan references the customer's demonstrated value (40% time savings) as proof of readiness

## Output expectations

- [ ] PASS: Output's health prerequisite check passes explicitly — citing the four positive signals (92% utilisation, health score 85, 3 successful QBRs, customer-initiated tier inquiry) — and proceeds to plan
- [ ] PASS: Output uses the customer's specific request (asking about API integration tier) as the expansion anchor — meeting them where they are, NOT pivoting to a different tier or bundle
- [ ] PASS: Output's revenue impact estimate is shown with assumptions — e.g. "API tier adds $X/seat or $Y flat; 115 active seats currently; potential ARR uplift $Z assuming 100% adoption, $Z/2 assuming 50%" — with the math and the assumption stated
- [ ] PASS: Output's enablement-not-sales framing is visible — the recommendation discusses what API integration would unlock for Meridian Legal (e.g. integrating with their case management system, automating client intake), NOT "let's grow account revenue"
- [ ] PASS: Output's timeline has milestones — Week 1: discovery call to understand the integration use case; Week 2-3: technical scoping with their IT; Week 4: API tier trial with their stack; Month 2: production rollout; Month 3: review uplift in time savings
- [ ] PASS: Output references the demonstrated 40% time-savings as the "we're ready for more" signal — connecting the QBR-proven value to the expansion ask rather than treating expansion as new
- [ ] PASS: Output identifies adoption risks — API tier requires technical resourcing on their side; if they don't have engineering capacity, the tier is bought but underused; recommends gating the upsell on confirming their technical readiness
- [ ] PASS: Output addresses the renewal context indirectly — Meridian is at $180k ARR with 3 successful QBRs; expansion ahead of renewal sets up a strong renewal conversation 6-9 months out
- [ ] PASS: Output names the AE / CSM owner of the conversation explicitly — not "the team" but the named CSM responsible for following up on the customer's inquiry
- [ ] PARTIAL: Output addresses cross-sell beyond the API tier — if the API integration drives further utilisation and demand for analytics or compliance modules, the expansion plan flags those as future opportunities (gated on this expansion succeeding first)
