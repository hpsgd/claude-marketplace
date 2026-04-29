# Test: Write architecture doc

Scenario: Testing whether the write-architecture-doc skill requires Mermaid diagrams, bounded context documentation, key decisions with rationale, and NFRs.

## Prompt


/internal-docs-writer:write-architecture-doc for our notification system — it handles in-app, email, and push notifications, with a queue-based delivery system and user preference management.

## Criteria


- [ ] PASS: Skill requires Mermaid diagrams for component architecture — not text descriptions of boxes and arrows
- [ ] PASS: Skill requires sequence diagrams for data flows — showing the temporal order of interactions, not just the components involved
- [ ] PASS: Skill documents key architectural decisions with rationale — why this approach was chosen, not just what was built
- [ ] PASS: Skill documents non-functional requirements (NFRs) — latency, throughput, availability — with specific targets
- [ ] PASS: Skill requires a research step before writing — reading existing code, configs, or ADRs
- [ ] PASS: Skill documents bounded contexts or system boundaries — what this system owns vs what it depends on externally
- [ ] PARTIAL: Skill documents known limitations or technical debt — partial credit if this section is mentioned but not required as mandatory
- [ ] PASS: Skill includes a quality checklist that verifies diagrams render and decisions are traceable
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output's component architecture is rendered as a Mermaid graph — showing the in-app channel, email sender, push sender, queue, preferences service, and external providers (Sendgrid / FCM / APNs) — with arrows for control flow
- [ ] PASS: Output includes a Mermaid sequence diagram for the notification dispatch flow — caller → API → preferences check → queue → channel-specific worker → external provider → callback — showing temporal ordering, not just topology
- [ ] PASS: Output documents the bounded context — what the notification system OWNS (delivery decisions, channel routing, retry logic, audit) and what it DEPENDS ON (preferences service, user identity, message templates) — so consumers know the contract surface
- [ ] PASS: Output's NFR section has specific numeric targets — latency (p95 < 5s for in-app, < 60s for email/push), throughput (50K notifications/day at launch, 500K target), availability (99.9% uptime SLO) — not "fast" or "scalable"
- [ ] PASS: Output documents at least 3 key architectural decisions with rationale — e.g. "queue-based delivery: chosen over synchronous because external providers fail unpredictably; allows retries without affecting the caller", with the alternative considered and why it was rejected
- [ ] PASS: Output's known-limitations section is mandatory — naming current debt (e.g. "no retry policy on Sendgrid 5xx; deliveries are dropped after 1 attempt", "preferences cache is not invalidated on update") with a link to backlog items
- [ ] PASS: Output's research step shows evidence — read existing code, ADRs, configs — with citations (file paths) so the reader can verify the documentation matches reality
- [ ] PASS: Output's quality checklist verifies Mermaid diagrams render without syntax errors AND that every architectural decision has a referenced ADR (or "to be written" with a date)
- [ ] PASS: Output addresses preferences as a first-class concern — channel × event-type matrix, opt-out enforcement at delivery time, and what happens when a preference change races with a notification mid-flight
- [ ] PARTIAL: Output addresses observability — what metrics are emitted (delivery rate, queue depth, provider error rate), which dashboards exist, and which alerts fire
