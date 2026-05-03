# Test: Event-sourced user activity pipeline

Scenario: User needs a data pipeline that captures user activity events from the production event stream and makes them available for analytics — specifically to answer retention and feature adoption questions.

## Prompt

We're building out our analytics capability and need a pipeline for user activity data. Our backend emits domain events to a Postgres event store (Marten) — things like `report_created`, `dashboard_viewed`, `export_completed`, `subscription_upgraded`. We want to track retention (did the user come back 7 days after signup?), feature adoption (which features do users engage with in their first 30 days?), and funnel conversion from trial to paid. The events are immutable once written. Can you design the pipeline and data model?

Do not ask for clarification — proceed based on the information provided. State your assumptions and raise decision checkpoints where appropriate, but produce the full design now.

## Criteria

- [ ] PASS: Agent starts by identifying data sources, checking for existing metric definitions and infrastructure, and reviewing what events are already tracked
- [ ] PASS: Agent produces precise metric definitions (with calculation, granularity, filters, time window, and caveats) for retention, feature adoption, and trial conversion before designing the pipeline
- [ ] PASS: Agent applies immutable event sourcing principles — never proposes UPDATE/DELETE patterns on event data, only append-only ingestion
- [ ] PASS: Agent addresses data quality checks at every pipeline boundary (null checks, deduplication, freshness monitoring)
- [ ] PASS: Agent documents data lineage from source (Marten event store) through transformations to the destination (analytics layer)
- [ ] PASS: Agent raises a decision checkpoint before choosing storage technology (architecture commitment)
- [ ] PARTIAL: Agent includes privacy considerations — identifying which properties contain PII and specifying retention/erasure policy
- [ ] PASS: Agent produces a validation checklist covering lineage, privacy, property types, and sanity checks
- [ ] PASS: Agent distinguishes correlation from causation when discussing retention metrics

## Output expectations

- [ ] PASS: Output names the four source events from the prompt (`report_created`, `dashboard_viewed`, `export_completed`, `subscription_upgraded`) and traces each to the analytics use case it supports
- [ ] PASS: Output's retention metric defines the exact 7-day window logic — e.g. "user signed up at T returns and triggers any event in (T+6d, T+8d]" — including boundary handling, not just "did they come back after 7 days"
- [ ] PASS: Output's feature adoption metric specifies first-30-days as a fixed cohort window from signup, lists which events count as "engagement" with which features, and defines the de-duplication rule (one count per user-feature)
- [ ] PASS: Output's funnel metric defines trial-to-paid conversion with explicit start state, terminal state (`subscription_upgraded` event), exclusion rules (cancelled trials, refunds), and time bounds
- [ ] PASS: Output's data flow describes Marten event store → ETL/CDC → analytics layer with explicit append-only semantics — no UPDATE/DELETE patterns on the activity events themselves, even in transformations
- [ ] PASS: Output documents at least three quality checks (null detection on user_id, deduplication of replayed events, freshness/lag monitoring) at named pipeline stages
- [ ] PASS: Output addresses event versioning — what happens if an event schema evolves (new property added to `report_created`) given the events are immutable in Marten
- [ ] PASS: Output raises a decision checkpoint on the analytics destination (warehouse choice — Snowflake / BigQuery / DuckDB / Postgres replica) before committing rather than picking unilaterally
- [ ] PARTIAL: Output identifies the PII and privacy implications — `user_id` linkage, retention period for raw activity, and erasure/right-to-be-forgotten handling for the immutable event store
- [ ] PARTIAL: Output includes a sanity-check on retention causality — flags that "user came back" correlates with engagement but doesn't prove the product caused the return
