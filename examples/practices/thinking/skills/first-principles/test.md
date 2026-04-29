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

## Output expectations

- [ ] PASS: Output classifies "that's how APIs work" and "clients will break otherwise" explicitly as ASSUMPTIONS, not hard constraints — naming them as inherited convention, not a function-imposed requirement
- [ ] PASS: Output's hard constraints are limited to truths grounded in function — e.g. "consumers must be able to upgrade independently", "old clients must keep working during transition windows", "the same identifier must reach the same code path" — not URL-shape conventions
- [ ] PASS: Output's challenge ledger gives every soft constraint and assumption a verdict (KEEP / REMOVE / TEST) with the impact-if-removed analysis — e.g. "if we remove URL-path versioning, what breaks for the 2 external partners?"
- [ ] PASS: Output's reconstruction starts from versioning's actual function — versioning exists to allow simultaneous old + new behaviour for different consumers — and considers all viable forms (URL path, header, query param, content-type, no version with additive-only changes)
- [ ] PASS: Output addresses the small consumer set (3 internal + 2 external) as a relevant fact — internal services can typically migrate together, external partners need a longer window, which influences the chosen versioning mechanism
- [ ] PASS: Output's delta analysis compares the reconstructed approach to the current `/v1/`, `/v2/` form with a table showing "this changed because we removed assumption X" — not just a "before/after" comparison without traceability
- [ ] PASS: Output's reconstruction does NOT conclude "no change" — it either identifies a meaningful shift (e.g. "internal APIs can use header-based versioning to keep the URL stable; external partners keep URL versioning") or returns to Step 2 to challenge more assumptions
- [ ] PASS: Output's migration assessment distinguishes quick wins (e.g. add a deprecation header to v1 starting now) from changes requiring stakeholder authority (e.g. asking external partners to switch to header-based versioning needs lead time and contractual coordination)
- [ ] PASS: Output addresses the API evolution mechanism alongside versioning — additive changes (new optional fields) don't need a new version, breaking changes do; this is more important than the version-shape choice
- [ ] PARTIAL: Output references real-world examples of non-URL-path versioning (Stripe's date-based header versioning, GitHub's media-type versioning) as evidence the assumption is challengeable
