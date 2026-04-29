# Test: Expansion plan

Scenario: Testing whether the expansion-plan skill enforces a health prerequisite check and refuses to plan expansion for unhealthy accounts.

## Prompt


/customer-success:expansion-plan for Fenwick Capital — they're at $95k ARR and we think there's an opportunity to upsell them to our enterprise tier. They have 45 licensed seats but our data shows only 12 active users in the last 30 days.

## Criteria


- [ ] PASS: Skill performs a health prerequisite check as the FIRST step — before any expansion planning begins
- [ ] PASS: Skill flags that 12/45 active users (27% adoption) indicates an unhealthy account and recommends against expansion
- [ ] PASS: Skill refuses to produce an expansion plan for an unhealthy account — or explicitly labels any output as conditional on health improvement first
- [ ] PASS: Skill recommends a health recovery path before expansion can be attempted — what needs to improve and by how much
- [ ] PASS: Skill frames expansion as customer enablement rather than a sales motion — the reason to expand should be that the customer needs more to get more value
- [ ] PARTIAL: Skill identifies what specific signals would indicate the account is ready for expansion — partial credit if health criteria for expansion readiness are mentioned but not quantified
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output's FIRST action is a health prerequisite check — not "let's plan the expansion" first then add caveats; the gate runs before any plan is written
- [ ] PASS: Output computes the adoption rate explicitly — 12 active users / 45 licensed seats = 27% — and flags this as below the healthy threshold (typically 60-70%+ for enterprise expansion readiness)
- [ ] PASS: Output explicitly REFUSES to produce a normal expansion plan — either declines and recommends a recovery plan first, or labels the expansion plan as conditional ("only valid after adoption returns to >60%")
- [ ] PASS: Output's recovery path lists what needs to improve and quantified targets — e.g. "active user count needs to reach 27 (60% of 45) over a 60-day window before expansion is safe to discuss"
- [ ] PASS: Output frames expansion as customer enablement — the right reason to expand is "the customer needs more capacity / features to extract more value" — NOT "we have a quota gap" or "they have budget"
- [ ] PASS: Output addresses the wasted-spend risk — Fenwick is paying for 33 unused seats; reducing seat count back to 12-15 may be the right call before any expansion conversation
- [ ] PASS: Output names the expansion-readiness signals quantitatively — adoption rate >=60%, active engagement on multiple features, positive health score on relationship and value dimensions, executive buy-in confirmed — not generic "they should be doing well"
- [ ] PASS: Output proposes a sequence — first restore adoption (90 days), then assess expansion fit (review post-recovery), then build a plan if signals align — rather than collapsing all three into a single recommendation
- [ ] PASS: Output's recommended communication to the AE / sales team explains why expansion is on hold — protecting the customer relationship rather than blocking revenue arbitrarily
- [ ] PARTIAL: Output flags the underlying issue — Fenwick was sold 45 seats but only used 12 — as a symptom of a sales/CS handoff or scoping problem worth feeding back upstream
