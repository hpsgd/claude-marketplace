# Test: Data model for a subscription billing domain

Scenario: Developer invokes the data-model skill to design the schema for a subscription billing domain. Key entities are customers, subscriptions, plans, invoices, and payment methods.

## Prompt

Design a data model for subscription billing. Entities: customers (name, email, created date), plans (name, price, billing interval monthly/annual, feature limits), subscriptions (customer to plan, status: trial/active/past_due/cancelled, start date, trial end date), invoices (subscription, amount, due date, paid date, status), and payment methods (customer, type: card/bank, last 4 digits, expiry). A customer can have multiple subscriptions and payment methods. Subscriptions must have a payment method.

## Criteria

- [ ] PASS: Skill performs domain discovery before creating tables — identifies entities, events, actors, invariants, and cardinality for each
- [ ] PASS: All primary keys use UUIDs (`gen_random_uuid()`) — no sequential integers
- [ ] PASS: All timestamp columns use `TIMESTAMPTZ` — not timezone-naive `TIMESTAMP`
- [ ] PASS: Status fields use `CHECK` constraints with enum values — not unconstrained text columns
- [ ] PASS: Skill documents access patterns before defining indexes — lists the frequent queries with frequency and latency SLA
- [ ] PASS: Foreign keys have named constraints and appropriate `ON DELETE` strategies (e.g. `RESTRICT` not silent cascade for customer deletion)
- [ ] PASS: Privacy section identifies PII columns (email, card last 4, name) with retention and erasure strategy
- [ ] PARTIAL: Skill produces a Mermaid ER diagram in the output
- [ ] PASS: Skill identifies open questions requiring product/business input before finalising
