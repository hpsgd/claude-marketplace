# Output: Data model for a subscription billing domain

**Verdict:** PASS
**Score:** 18.5/19 criteria met (97%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill performs domain discovery before creating tables — Step 1 explicitly covers entities, events, actors, invariants, and a per-entity property table (identity, lifecycle, ownership, cardinality, mutability, temporal). All five discovery elements required before any table creation — met.
- [x] PASS: All primary keys use UUIDs (`gen_random_uuid()`) — Step 3 schema rules state `UUID PRIMARY KEY DEFAULT gen_random_uuid()` with explicit rationale against sequential integers; anti-patterns section reinforces it — met.
- [x] PASS: All timestamp columns use `TIMESTAMPTZ` — Step 3 schema rules state "Timestamps with timezone — `TIMESTAMPTZ` not `TIMESTAMP` — always store UTC"; anti-patterns section adds a second explicit prohibition — met.
- [x] PASS: Status fields use `CHECK` constraints with enum values — Step 3 example shows `CHECK (status IN ('active', 'paused', 'archived'))` and the schema rules table lists CHECK constraints for enums as mandatory — met.
- [x] PASS: Skill documents access patterns before defining indexes — Step 4 is labelled MANDATORY and requires frequency and latency SLA columns; the index strategy table follows within the same step — met.
- [x] PASS: Foreign keys have named constraints and appropriate ON DELETE strategies — Step 3 example shows `CONSTRAINT uq_sources_name_per_owner`; Step 5 provides an ON DELETE strategy table with RESTRICT rationale for important records — met.
- [x] PASS: Privacy section identifies PII columns with retention and erasure strategy — Step 8 explicitly covers PII identification, retention policy, right to erasure, and anonymisation; SQL comment example tags `email` and `name` with retention and erasure notes; "payment info" is listed as PII — met.
- [x] PASS: Skill produces a Mermaid ER diagram in the output — Output Format section lists `[Mermaid ER diagram]` as the first deliverable under `## Entity-Relationship Diagram` — met.
- [x] PASS: Skill identifies open questions requiring product/business input — Output Format includes `## Open Questions` described as "Decisions that need product/business input before finalising" — met.

### Output expectations

- [x] PASS: Output's schema includes all five entities — the skill instructs "Design a data model for $ARGUMENTS" and Step 3 requires full schema for each entity identified in domain discovery; all five named entities in the prompt would be covered — met.
- [x] PASS: Output's `subscriptions` status column uses a CHECK with the four exact values from the prompt — Step 3 mandates CHECK constraints for enums and makes the pattern explicit; the four values come directly from $ARGUMENTS — met.
- [x] PASS: Output's `payment_methods` table stores only last-4/expiry with a CHECK on type — Step 8 data minimisation supports not storing full card numbers; the type CHECK follows from the general enum rule — met.
- [x] PASS: Output's `subscriptions` enforces NOT NULL FK to `payment_methods` — Step 2 asks whether FKs are mandatory (NOT NULL) and Step 5 covers referential integrity; the NOT NULL FK follows from the mandatory relationship — met.
- [x] PASS: Output uses `gen_random_uuid()` for every primary key and `TIMESTAMPTZ` for every datetime column — both rules are stated unconditionally in Step 3 and apply across all entities — met.
- [x] PASS: Output specifies ON DELETE strategies with RESTRICT for customer deletion — Step 5 shows RESTRICT rationale ("Don't delete users with sources — orphaned data") that maps directly to invoice audit history in the billing domain — met.
- [x] PASS: Output's privacy section flags email, name, and card last-4 as PII with an erasure strategy — Step 8 covers PII identification, retention, and erasure; email, name, and payment info are all explicitly listed — met.
- [x] PASS: Output includes a Mermaid ER diagram showing cardinality — Output Format mandates the diagram as the first section; cardinality relationships are established in Step 1 domain discovery — met.
- [x] PASS: Output lists open questions for product — Step 1 domain discovery surfaces invariants and edge cases; the Open Questions section in the Output Format captures them; proration, refunds, multi-currency, and tax are natural outputs of billing domain discovery — met.
- [~] PARTIAL: Output addresses currency and money representation — the skill has no explicit guidance on money representation. The schema rules, anti-patterns, and privacy sections make no mention of floating-point money, integer cents, or currency columns. An agent following this skill could produce a `FLOAT` or bare `NUMERIC` column without correction. The skill's general strictness principles lean toward explicit types, but the specific money representation rule is absent — partially met.

## Notes

The skill is structurally strong. The eight-step sequential process, the MANDATORY label on Step 4, and the explicit anti-patterns section would produce a correct and defensible schema for most billing use cases.

The one gap worth noting: money representation is absent from schema rules and anti-patterns. For a billing domain, storing amounts as `NUMERIC(19,4)` or integer cents is a critical correctness rule — floating-point money is a well-known production bug. One anti-pattern bullet would close this without restructuring anything else.
