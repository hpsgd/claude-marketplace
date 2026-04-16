# Test: first-principles API versioning assumptions

Scenario: An architect is questioning whether the team's assumption that REST API versioning via URL path (/v1/, /v2/) is the right approach. The first-principles skill is used to pressure-test the constraints.

## Prompt

/first-principles We've always versioned our APIs with URL path prefixes (/api/v1/users, /api/v2/users). The team assumes this is required because "that's how APIs work" and "clients will break otherwise". I want to challenge whether this is actually necessary or if it's just habit. We have 3 internal services and 2 external partners as consumers.

## Criteria

- [ ] PASS: Step 1 produces a complete component inventory classifying every constraint as hard constraint, soft constraint, or assumption with evidence for each
- [ ] PASS: "That's how APIs work" and similar inherited conventions are correctly classified as assumptions, not hard constraints
- [ ] PASS: Step 2 challenge ledger addresses every soft constraint and assumption from Step 1 with a verdict (keep/remove/test) and impact-if-removed analysis
- [ ] PASS: Step 3 reconstruction starts only from verified truths and hard constraints — ignores current URL path versioning form and asks what function requires
- [ ] PASS: Step 4 delta analysis compares reconstructed approach against current state with a table showing which assumption removal enabled each difference
- [ ] PASS: Output uses the defined first-principles template with all four sections
- [ ] PARTIAL: Migration assessment distinguishes quick wins from changes requiring stakeholder authority
- [ ] PASS: Reconstruction does not conclude "change nothing" — if it does, the skill's own rules require returning to Step 2 to challenge more assumptions
