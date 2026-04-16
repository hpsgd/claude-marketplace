# Test: technical decision

Scenario: A user asks the CTO to make a significant architectural decision about system design. Does the CTO assess the context, delegate to the architect appropriately, apply the right decision criteria, and avoid making product-scope decisions?

## Prompt

We're building Vaultly — a SaaS document management platform for small law firms. We're about to start the backend and need to decide: do we go with a monolithic Django Ninja application or break it into microservices (one for document storage, one for search, one for access control)? We have a team of three backend devs and expect maybe 50 law firm clients in year one, growing to 500 in year three. What's your recommendation?

## Criteria

- [ ] PASS: Performs pre-flight — reads project conventions and checks the technology stack before advising
- [ ] PASS: Delegates the architecture decision to the architect agent, framing the decision with scope, constraints, and context
- [ ] PASS: Does not simply pick an option without analysis — identifies the trade-offs between each approach
- [ ] PASS: Applies the principle "simple until proven otherwise" — accounts for team size (3 devs) and year-one scale (50 clients) in the recommendation
- [ ] PASS: Produces a dispatch plan rather than implementing directly
- [ ] PASS: Frames a clear escalation path if the decision involves significant vendor lock-in
- [ ] PARTIAL: References the need for an ADR to document the decision and reasoning
- [ ] PASS: Does not make product decisions (e.g. what features to build first) — stays in technical domain
- [ ] SKIP: Escalates to coordinator — only relevant if the decision involves budget or cross-domain conflict
