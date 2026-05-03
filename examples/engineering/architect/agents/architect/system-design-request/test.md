# Test: system design request

Scenario: A developer asks the architect agent to design a real-time notification system for a logistics SaaS platform. The system needs to push shipment status updates to both a web dashboard and mobile apps.

## Prompt

We're building a logistics platform called FreightFlow. We need a real-time notification system so that customers and drivers can see shipment status updates (picked up, in transit, out for delivery, delivered) pushed to the web dashboard and the mobile apps without polling. We're currently running a Django REST API on PostgreSQL. Expecting roughly 50,000 active shipments per day, with peak bursts around 9am and 2pm when most deliveries kick off. Need to know what you'd recommend for the architecture.

Do not ask for clarification — produce the full design now. State your assumptions in an assumption ledger and mark each as proven_by_code, inferred, or needs_user_confirmation.

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

## Output expectations

- [ ] PASS: Output's transport recommendation explicitly compares WebSockets vs SSE vs long-polling for the push-to-browser-and-mobile use case, with reasoning that addresses bidirectional vs server-initiated traffic and mobile network behaviour (background sockets, reconnection)
- [ ] PASS: Output addresses the existing Django + PostgreSQL stack — either uses Django Channels / a Django-compatible push solution, or names a separate service with clear integration points to the existing API
- [ ] PASS: Output sizes the system from the 50,000 shipments/day plus 9am/2pm peak — converting daily volume into a peak-second concurrent connection or message rate (e.g. burst factor of 5-10x average) and validating the chosen transport handles it
- [ ] PASS: Output includes at least one Mermaid component diagram showing the path from shipment status change → message broker → push fan-out → web/mobile clients, with trust boundaries marked
- [ ] PASS: Output's assumption ledger lists the unstated facts (mobile platforms iOS/Android both, push notification vs in-app socket for backgrounded apps, customer authentication model) classified as `inferred` or `needs_user_confirmation`
- [ ] PASS: Output identifies at least 2 ADR-worthy decisions (e.g. message broker selection, push transport, fan-out service vs in-Django) and lists them in a "Decisions Requiring ADR" section
- [ ] PASS: Output's change impact section explicitly addresses the Django REST API (extended with status-change events) and PostgreSQL (transactional outbox or change capture) and lists at least one component that is unaffected
- [ ] PASS: Output includes a confidence score with HIGH/MEDIUM/LOW label plus a numeric value out of 100, and lists the assumptions or unknowns driving any confidence reduction
- [ ] PARTIAL: Output addresses backgrounded mobile app delivery — recommending APNs/FCM for true push when the app isn't foregrounded, distinct from in-app socket for live dashboards
- [ ] PARTIAL: Output addresses authentication on the persistent connection (token-scoped channels per customer/driver, not broadcast) so customers can't see other customers' shipments
