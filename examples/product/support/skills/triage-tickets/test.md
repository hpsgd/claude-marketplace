# Test: Triage tickets

Scenario: Testing whether the triage-tickets skill classifies tickets across all required dimensions, includes pattern detection, and produces a structured triage table.

## Prompt


/support:triage-tickets for this batch of 18 new support tickets received overnight, ranging from billing questions to feature requests to what appear to be related login errors from multiple customers.

## Criteria


- [ ] PASS: Skill classifies each ticket across multiple dimensions — category (bug/question/feature/billing), severity, and routing destination
- [ ] PASS: Skill includes pattern detection — when 3 or more tickets match the same root issue, they should be grouped and escalated
- [ ] PASS: Skill generates a bug report or incident escalation for patterns that suggest a systemic issue — not just individual ticket responses
- [ ] PASS: Skill produces a structured triage table as output — not a prose summary of the ticket queue
- [ ] PASS: Skill requires an ingest step — reading all tickets before classifying any — to enable pattern detection across the full batch
- [ ] PARTIAL: Skill assigns a response SLA or priority to each ticket — partial credit if severity classification does this work implicitly
- [ ] PASS: Skill routes tickets to appropriate teams or owners, not just classifies them
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output's ingest step reads ALL 18 tickets BEFORE classifying any — pattern detection requires the full batch, not sequential processing
- [ ] PASS: Output's triage table classifies each ticket across the dimensions — category (bug / question / feature / billing), severity (critical / high / medium / low), and routing destination (engineering / billing / product / answered-in-place)
- [ ] PASS: Output detects the login-error pattern — multiple tickets sharing the same root cause are GROUPED into a single incident or bug report, not 3 separate engineering tickets
- [ ] PASS: Output generates an incident escalation for the login pattern — naming the affected user count, time window, and the recommended on-call escalation (engineering rather than support resolves it individually)
- [ ] PASS: Output's structured triage table has columns — Ticket ID, Customer, Category, Severity, Routing, Priority, Pattern Group (if applicable), Suggested Owner — not a prose summary
- [ ] PASS: Output assigns a response SLA per ticket based on severity — e.g. critical: respond in 30 min; high: 2h; medium: 24h; low: 3 business days — making expectations clear
- [ ] PASS: Output routes billing tickets to the billing/finance owner, feature requests to product, bugs to engineering, and questions to support agents — not just "engineering" for everything
- [ ] PASS: Output identifies tickets that can be answered from KB articles or self-serve — the support agent doesn't escalate questions that have public docs, recommending a deflection link instead
- [ ] PASS: Output's pattern detection rule is explicit — 3 or more tickets matching the same root cause within a defined window (e.g. 24 hours) trigger an incident escalation
- [ ] PARTIAL: Output addresses tickets that need follow-up classification — e.g. "needs more info from customer" tickets get a separate state, not classified as resolved or stuck
