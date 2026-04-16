# Event sourced user activity pipeline

User needs a data pipeline that captures user activity events from the production event stream and makes them available for analytics — specifically to answer retention and feature adoption questions.

## Prompt

> We're building out our analytics capability and need a pipeline for user activity data. Our backend emits domain events to a Postgres event store (Marten) — things like `report_created`, `dashboard_viewed`, `export_completed`, `subscription_upgraded`. We want to track retention (did the user come back 7 days after signup?), feature adoption (which features do users engage with in their first 30 days?), and funnel conversion from trial to paid. The events are immutable once written. Can you design the pipeline and data model?

The data engineer agent, given this prompt, would produce the following after completing its mandatory pre-flight checks.

---

## Output

**Pre-flight Step 1:** Check for existing data infrastructure — no existing warehouse, pipelines, or dashboard tooling found. Data sources: Marten PostgreSQL event store with domain event tables. Existing metric definitions: none found. Event tracking already in place: `report_created`, `dashboard_viewed`, `export_completed`, `subscription_upgraded` from the domain events described.

**Step 2 classification:** Pipeline work. Process: Source → transform → destination → quality checks → monitoring.

---

**Metric Definitions (before pipeline design):**

#### Day-7 Retention


| Field | Value |
|---|---|
| Definition | User who performed any qualifying event on day 7 (±1 day) after their first qualifying event or account creation |
| Calculation | `COUNT(DISTINCT user_id WHERE first_event_after_day6 IS NOT NULL AND first_event_before_day9 IS NOT NULL) / COUNT(DISTINCT user_id IN cohort)` |
| Data source | Marten event store — all event types per user, joined to first event timestamp |
| Granularity | Daily signup cohort |
| Filters | Exclude test accounts (`is_test_account = true`), exclude internal domains |
| Time window | Days 6-8 after signup date |
| Known caveats | Correlation only — cannot determine causation without controlled experiment. Day ±1 window accounts for timezone differences. |
| Owner | Product team |


#### Feature Adoption (First 30 Days)


| Field | Value |
|---|---|
| Definition | Count of distinct event types (features) per user in their first 30 days from signup |
| Calculation | `COUNT(DISTINCT event_type) per user WHERE event_timestamp <= signup_date + 30 days` |
| Data source | Marten event store |
| Granularity | Per user, rolled up by cohort week |
| Time window | Days 0-30 from signup date |


#### Trial-to-Paid Conversion


| Field | Value |
|---|---|
| Definition | User who has a `subscription_upgraded` event within 14 days of their first trial subscription event |
| Calculation | `COUNT(DISTINCT users with subscription_upgraded within 14 days) / COUNT(DISTINCT users with first trial event)` |
| Granularity | Weekly trial-start cohort |
| Filters | Exclude test accounts |
| Time window | 14 days from first trial event |


---

**Pipeline design:** Marten PostgreSQL → CDC or scheduled polling → staging (raw append-only copy) → deduplication by event_id → analytics schema. Events are immutable once written. Ingestion is append-only. No UPDATE or DELETE on ingested events. Corrections arrive as new events.

**Data quality at each boundary:**
- Ingestion: null check on required fields (event_id, user_id, event_type, occurred_at), type validation
- Staging: deduplication check (COUNT event_id — any duplicates halt pipeline and alert)
- Analytics: freshness check (alert if no events for >1 hour during business hours), row count sanity check vs. previous run

**Data lineage:** Marten event store (source) → CDC extract (raw staging layer) → cleaned/deduped events table → dimensional analytics model (user_cohorts, feature_adoption_daily, conversion_funnel).

**Decision checkpoint:** Before recommending a storage destination (ClickHouse, BigQuery, analytical PostgreSQL, Redshift) — this is an architecture commitment with ongoing cost implications. Pausing for input: what is the expected query volume and budget?

**Privacy:** `user_id` is UUID — no PII by default in event properties. Flag any events where `properties` JSONB contains email, name, or other identifiable fields for erasure policy documentation. Deletion key = `user_id`.

**Correlation/causation note:** Day-7 retention and feature adoption metrics are correlational. A user with high feature adoption may retain better, but we cannot claim causation without a controlled experiment (A/B test or holdout group). These metrics measure association only.

**Validation checklist:**
- Lineage documented (Marten event store → staging → analytics)
- Privacy assessed (PII in JSONB properties identified, deletion key = user_id)
- Property types and constraints specified (event_id UUID NOT NULL, occurred_at TIMESTAMPTZ NOT NULL)
- Sanity checks defined (duplicate event_id = 0, freshness < 1 hour during business hours)

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 8.5/9 criteria met (94%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Agent starts by identifying data sources, existing metrics, and tracked events — Pre-Flight Step 1 is marked MANDATORY and explicitly requires: checking for existing data infrastructure, identifying data sources, checking for existing metric definitions, and reviewing event tracking. All four are present in the simulated pre-flight.

- [x] PASS: Agent produces precise metric definitions before pipeline design — Metric Definitions section is marked "(MANDATORY before implementation)" and requires Definition, Calculation, Data source, Granularity, Filters, Time window, Known caveats, and Owner. The simulated output produces definitions for all three requested metrics (Day-7 Retention, Feature Adoption, Trial-to-Paid Conversion) before pipeline design. Caveat field for retention explicitly names the correlation limit.

- [x] PASS: Agent applies immutable event sourcing principles — Data Modelling Principles section states: "Immutable events. Once written, event data doesn't change. Corrections are new events, not edits to old ones." This is a non-negotiable principle in the definition. The simulated pipeline design explicitly follows this with append-only ingestion and no UPDATE/DELETE.

- [x] PASS: Agent addresses data quality at every pipeline boundary — Data Quality section specifies checks at every boundary: null check, type check, uniqueness (deduplication), freshness. The rule "Validate at ingestion. Bad data that enters the system is 10x harder to fix downstream." enforces this.

- [x] PASS: Agent documents data lineage — Data Lineage section requires structured documentation from source system through ingestion, transformations, and destination. Every metric requires documented lineage. The simulated output traces from Marten event store through staging to the analytics dimensional model.

- [x] PASS: Agent raises decision checkpoint before storage technology — Decision Checkpoints table includes "Choosing a new data storage technology — Infrastructure commitment — architecture decision" as a mandatory STOP. The simulated output pauses before recommending ClickHouse/BigQuery/etc.

- [~] PARTIAL: Agent includes privacy considerations — Data Modelling Principles includes "Privacy by design. Don't collect what you don't need. Document retention policies. Anonymise what you can." The validation checklist requires "Privacy implications assessed (PII, retention, consent)." However the definition does not mandate a structured PII audit per pipeline (identifying specific event properties, erasure keys, and retention periods as a required deliverable). Privacy appears as a principle and checklist item but not as a required structured output for pipeline design work.

- [x] PASS: Agent produces validation checklist — Output Format validation section lists exactly: lineage documented, privacy implications assessed, property types and constraints specified, and sanity checks defined. All four areas from the criterion are present as required checklist items.

- [x] PASS: Agent distinguishes correlation from causation — "Event Correlation and Causation" section with rule: "Default assumption: correlation, not causation. Claiming causation requires experimental evidence (A/B test, before/after with controlled conditions)." Retention and adoption metrics carry this caveat in the simulated output.

## Notes

The privacy gap is narrow but real. The agent definition treats privacy as a principle and a checklist item. It does not require a structured PII audit — a table listing which specific event properties contain PII, what the erasure key is, what the retention period is, and what the deletion mechanism is. That level of structure exists in the data-model skill (Step 8 Privacy by Design) but is not replicated in the agent's pipeline design workflow. For a pipeline ingesting event data with user identifiers in JSONB properties, this gap means privacy compliance depends on the analyst remembering to audit it rather than the definition requiring it.
