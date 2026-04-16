# Test: system design request

Scenario: A developer asks the architect agent to design a real-time notification system for a logistics SaaS platform. The system needs to push shipment status updates to both a web dashboard and mobile apps.

## Prompt

We're building a logistics platform called FreightFlow. We need a real-time notification system so that customers and drivers can see shipment status updates (picked up, in transit, out for delivery, delivered) pushed to the web dashboard and the mobile apps without polling. We're currently running a Django REST API on PostgreSQL. Expecting roughly 50,000 active shipments per day, with peak bursts around 9am and 2pm when most deliveries kick off. Need to know what you'd recommend for the architecture.

## Criteria

- [ ] PASS: Agent performs a pre-flight step — checks for project conventions (CLAUDE.md, installed rules) and existing ADRs before proposing anything
- [ ] PASS: Agent classifies the work type and scopes what is and is not covered by the design
- [ ] PASS: Agent produces a mandatory assumption ledger with each assumption classified as proven_by_code, inferred, or needs_user_confirmation
- [ ] PASS: Agent quantifies non-functional requirements rather than accepting vague terms — scale (50k shipments/day), latency targets, and availability
- [ ] PASS: Agent presents at least two architectural options (e.g. WebSockets vs SSE vs polling) with a scored trade-off table
- [ ] PASS: Agent includes Mermaid diagrams — at minimum a component diagram showing trust boundaries
- [ ] PASS: Agent identifies decisions that require an ADR (e.g. choice of message broker or real-time transport)
- [ ] PASS: Agent includes a confidence score (HIGH/MEDIUM/LOW with numeric) and states which assumptions drive uncertainty
- [ ] PARTIAL: Agent maps change impact — what existing FreightFlow components are directly or indirectly affected, and explicitly lists what is unaffected
