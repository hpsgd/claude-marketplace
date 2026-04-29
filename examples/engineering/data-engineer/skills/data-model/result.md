# Output: Data model for a subscription billing domain

**Verdict:** PARTIAL
**Score:** 14.5/19 criteria met (76%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill performs domain discovery before creating tables — Step 1 explicitly covers entities, events, actors, invariants, and a per-entity property table (identity, lifecycle, ownership, cardinality, mutability, temporal). All five discovery elements are required before any table creation — met
- [x] PASS: All primary keys use UUIDs (`gen_random_uuid()`) — Step 3 schema rules state `UUID PRIMARY KEY DEFAULT gen_random_uuid()` with explicit rationale against sequential integers; anti-patterns section reinforces it — met
- [x] PASS: All timestamp columns use `TIMESTAMPTZ` — Step 3 schema rules state "Timestamps with timezone — `TIMESTAMPTZ` not `TIMESTAMP` — always store UTC"; anti-patterns section adds a second explicit prohibition — met
- [x] PASS: Status fields use `CHECK` constraints with enum values — Step 3 example shows `CHECK (status IN ('active', 'paused', 'archived'))` and the schema rules table lists CHECK constraints for enums as mandatory — met
- [x] PASS: Skill documents access patterns before defining indexes — Step 4 is labelled MANDATORY and requires frequency and latency SLA columns; the index strategy table follows within the same step — met
- [x] PASS: Foreign keys have named constraints and appropriate `ON DELETE` strategies — Step 3 example shows `CONSTRAINT uq_sources_name_per_owner`; Step 5 provides an ON DELETE strategy table with RESTRICT rationale for important records — met
- [x] PASS: Privacy section identifies PII columns with retention and erasure strategy — Step 8 explicitly covers PII identification, retention policy, right to erasure, and anonymisation; the SQL comment example tags `email` and `name` with retention and erasure notes; "payment info" is listed as PII — met
- [x] PASS: Skill produces a Mermaid ER diagram in the output — Output Format section lists `[Mermaid ER diagram]` as the first deliverable under `## Entity-Relationship Diagram` — met
- [x] PASS: Skill identifies open questions requiring product/business input — Output Format includes `## Open Questions` described as "Decisions that need product/business input before finalising" — met

### Output expectations

- [x] PASS: Output's schema includes all five entities — the skill instructs "Design a data model for $ARGUMENTS" and Step 3 requires full schema for each entity identified in domain discovery; a well-formed execution over the prompt's five named entities covers all five — met
- [x] PASS: Output's `subscriptions` status column uses a CHECK with the four exact values from the prompt — Step 3 mandates CHECK constraints for enums and the schema template makes the pattern explicit; the four values come directly from the $ARGUMENTS — met
- [~] PARTIAL: Output's `payment_methods` table stores only last-4/expiry with a CHECK on type — Step 8 data minimisation and the anti-patterns section ("Don't collect what you don't need") support not storing full card numbers, and the type CHECK follows from the general enum rule. However, the skill has no PCI-DSS-specific rule explicitly prohibiting PAN, CVV, or full card storage. The type CHECK would be produced; the PAN/CVV prohibition is implied but not instructed — partially met
- [~] PARTIAL: Output's `subscriptions` enforces NOT NULL FK to `payment_methods` addressing chicken-and-egg ordering — Step 2 asks whether FKs are mandatory (NOT NULL) and Step 5 covers referential integrity, so the NOT NULL FK would follow. The skill gives no guidance on the chicken-and-egg creation-order problem (payment method must exist before subscription can be created), so the constraint would likely appear but the ordering issue would not be called out — partially met
- [x] PASS: Output uses `gen_random_uuid()` for every primary key and `TIMESTAMPTZ` for every datetime column — both rules are stated unconditionally in Step 3 schema rules and apply across all entities — met
- [x] PASS: Output specifies ON DELETE strategies with RESTRICT for customer deletion — Step 5 shows RESTRICT rationale ("Don't delete users with sources — orphaned data") that maps directly to invoice audit history in the billing domain — met
- [~] PARTIAL: Output's privacy section flags email, name, and card last-4 as PII with an erasure strategy respecting financial-record retention — Step 8 covers PII and retention policy but gives no guidance on financial record retention periods (7+ years for invoices). The skill would flag the PII columns and document erasure, but may not distinguish between customer PII erasure and invoice record retention requirements — partially met
- [x] PASS: Output includes a Mermaid ER diagram showing cardinality — Output Format mandates the diagram as the first section; cardinality relationships are established in Step 1 domain discovery — met
- [x] PASS: Output lists open questions for product (proration, refunds, multi-currency, tax) — Step 1 domain discovery surfaces invariants and edge cases; the Open Questions section in the Output Format captures them; these specific questions are natural outputs of billing domain discovery — met
- [~] PARTIAL: Output addresses currency and money representation — the skill has no explicit guidance on money representation. The schema rules, anti-patterns, and privacy sections make no mention of floating-point money, integer cents, or currency columns. An agent following this skill could produce a `FLOAT` or bare `NUMERIC` column without correction. The skill's general strictness principles push toward explicit types, but the specific money representation rule is absent — partially met

## Notes

The skill is structurally strong. The eight-step sequential process, the MANDATORY label on Step 4, and the explicit anti-patterns section would produce a correct and defensible schema for most billing use cases.

Three targeted gaps stand out for a payment domain:

1. **Money representation.** No rule against floating-point for currency. The schema example shows no money column, so the agent has no model to follow. One anti-pattern bullet ("Never use FLOAT or DOUBLE for monetary amounts — use INTEGER cents or NUMERIC with explicit precision and a separate currency column") would close this.

2. **PCI-DSS data minimisation.** Step 8 covers PII generally but doesn't explicitly prohibit storing full card numbers or CVV. The implication is there via data minimisation, but a billing domain warrants an explicit rule.

3. **FK creation ordering.** The skill covers whether FKs are mandatory but not what to do when two entities have a mandatory circular dependency at creation time (subscription requires payment method; payment method may need subscription context). A note in Step 2 about creation ordering patterns would help.

The Mermaid ER diagram gap from the previous evaluation (diagram only in output format, not in a process step) remains, but counts as met here because the output format is an explicit instruction to produce it.
