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

## Output expectations

- [ ] PASS: Output's schema includes all five entities from the prompt — customers, plans, subscriptions, invoices, payment_methods — with the columns and types specified in the prompt
- [ ] PASS: Output's `subscriptions` table has a `status` column with a CHECK constraint listing the four exact values from the prompt (`trial`, `active`, `past_due`, `cancelled`) — not a free-text string
- [ ] PASS: Output's `payment_methods` table stores only the last 4 digits and expiry — never full card number, CVV, or PAN — and the type column has a CHECK on (`card`, `bank`)
- [ ] PASS: Output's `subscriptions` table enforces the "must have a payment method" requirement via a NOT NULL foreign key to `payment_methods`, addressing the chicken-and-egg ordering issue (e.g. payment method created before subscription)
- [ ] PASS: Output uses `gen_random_uuid()` for every primary key and `TIMESTAMPTZ` for every datetime column (created_at, started_at, due_date, paid_date, trial_end_date)
- [ ] PASS: Output specifies ON DELETE strategies for each foreign key — customer deletion is RESTRICT (or soft-delete pattern), not silent CASCADE that would erase invoices and audit history
- [ ] PASS: Output's privacy section flags email, name, and card last-4 as PII with an erasure strategy that respects financial-record retention requirements (typically 7+ years for invoices)
- [ ] PASS: Output includes a Mermaid ER diagram showing the cardinality (customer 1:N subscriptions, customer 1:N payment_methods, subscription 1:N invoices, subscription N:1 plan)
- [ ] PASS: Output lists open questions for product — e.g. proration on plan change, partial refund handling, multi-currency support, tax columns — rather than silently making assumptions
- [ ] PARTIAL: Output addresses currency and money representation — money stored as integer cents (or numeric with explicit precision) and a currency column, not floating-point
