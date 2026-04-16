# Test: Event-sourced user activity pipeline

Scenario: User needs a data pipeline that captures user activity events from the production event stream and makes them available for analytics — specifically to answer retention and feature adoption questions.

## Prompt

We're building out our analytics capability and need a pipeline for user activity data. Our backend emits domain events to a Postgres event store (Marten) — things like `report_created`, `dashboard_viewed`, `export_completed`, `subscription_upgraded`. We want to track retention (did the user come back 7 days after signup?), feature adoption (which features do users engage with in their first 30 days?), and funnel conversion from trial to paid. The events are immutable once written. Can you design the pipeline and data model?

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
