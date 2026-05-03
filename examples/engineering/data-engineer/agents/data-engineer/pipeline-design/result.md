# Pipeline Design

Scenario: User needs a data pipeline that captures user activity events from the production event stream and makes them available for analytics — specifically to answer retention and feature adoption questions.

## Prompt

> We're building out our analytics capability and need a pipeline for user activity data. Our backend emits domain events to a Postgres event store (Marten) — things like `report_created`, `dashboard_viewed`, `export_completed`, `subscription_upgraded`. We want to track retention (did the user come back 7 days after signup?), feature adoption (which features do users engage with in their first 30 days?), and funnel conversion from trial to paid. The events are immutable once written. Can you design the pipeline and data model?
> 
> Do not ask for clarification — proceed based on the information provided. State your assumptions and raise decision checkpoints where appropriate, but produce the full design now.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll design a comprehensive event-sourced analytics pipeline that works within your Marten event store architecture. I'm building this on the assumption that:

- Events have a consistent schema with `user_id`, `timestamp`, `event_type`, and event-specific data
- You want analytics separate from the event store (operational vs. analytical concerns)
- Incremental loading is preferred over full replays
- Retention/adoption/conversion analyses need both detailed facts and rolled-up dimensions

Let me structure this across four layers: **Pipeline Architecture**, **Event Tracking Plan**, **Data Model**, and **Implementation**.

---

## 1. Pipeline Architecture

```
Marten Event Store (Postgres)
         ↓
    [Extraction]
    Daily job: Extract new events since last watermark
         ↓
    staging_events (raw, immutable append-only)
         ↓
    [Transformation via dbt]
    ├─→ dim_users (user lifecycle dimension)
    ├─→ dim_features (feature catalog)
    ├─→ fact_retention (user-day cohort analysis)
    ├─→ fact_adoption (feature-user-period interactions)
    └─→ fact_conversion_funnel (path to paid)
         ↓
    [Analytics & BI]
    Looker/Metabase queries on fact tables
```

**Key principle**: Events flow one direction only. Fact tables are **immutable inserts**, never updates. New cohorts/conversions are added, never modified. This respects the event sourcing invariant.

---

## 2. Event Tracking Plan

Your events must have these core properties for analytics:

```
All Events (required):
  - event_id: UUID (idempotency)
  - user_id: UUID (user foreign key)
  - event_type: VARCHAR (report_created, dashboard_viewed, etc.)
  - event_timestamp: TIMESTAMP (UTC, NOT event_created_at which drifts)
  - event_data: JSONB (event-specific payload)
  - marten_version: BIGINT (sequence number from Marten)

Specific events (as defined):
  
  user_signed_up (emit on first user creation)
    - plan_type: VARCHAR (trial, paid_monthly, paid_annual)
    
  report_created
    - report_id: UUID
    - report_type: VARCHAR (sales, inventory, custom)
    
  dashboard_viewed
    - dashboard_id: UUID
    - dashboard_type: VARCHAR (pre_built, custom)
    - time_on_page_seconds: INT (optional, can be calculated from session events)
    
  export_completed
    - export_id: UUID
    - export_format: VARCHAR (csv, pdf, xlsx)
    - record_count: INT
    
  subscription_upgraded
    - previous_plan: VARCHAR
    - new_plan: VARCHAR
    - effective_date: TIMESTAMP
```

**Assumption checkpoint**: Do you have a `user_signed_up` event? It's critical for retention cohort analysis. If not, we can derive signup date from the earliest event per user, but a dedicated event is cleaner.

---

## 3. Data Model

### A. Staging Table (Raw Events)

```sql
CREATE TABLE analytics.staging_events (
  event_id UUID PRIMARY KEY,
  user_id UUID NOT NULL,
  event_type VARCHAR NOT NULL,
  event_timestamp TIMESTAMP NOT NULL,
  event_data JSONB NOT NULL,
  marten_version BIGINT NOT NULL,
  loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_events_user_timestamp 
  ON analytics.staging_events(user_id, event_timestamp);
CREATE INDEX idx_events_type_timestamp 
  ON analytics.staging_events(event_type, event_timestamp);
```

**Append-only**: New events inserted daily. Never updated or deleted. Marten version ensures deduplication.

---

### B. Dimension: User Lifecycle

```sql
-- Type 2 SCD (tracks plan changes over time)
CREATE TABLE analytics.dim_users (
  user_id UUID NOT NULL,
  signup_date DATE NOT NULL,
  signup_plan VARCHAR NOT NULL,
  
  -- Slowly-changing attributes
  current_plan VARCHAR,
  plan_changed_at TIMESTAMP,
  
  -- Event-derived flags
  has_created_report BOOLEAN,
  has_viewed_dashboard BOOLEAN,
  has_exported BOOLEAN,
  
  -- Validity windows (for time-travel queries)
  valid_from TIMESTAMP NOT NULL,
  valid_to TIMESTAMP,
  is_current BOOLEAN DEFAULT TRUE,
  
  dbt_scd_id VARCHAR,
  dbt_updated_at TIMESTAMP
);

CREATE UNIQUE INDEX idx_users_scd 
  ON analytics.dim_users(user_id, valid_to DESC) 
  WHERE is_current = TRUE;
```

**ES mindset**: This uses dbt's Type 2 SCD (Slowly Changing Dimension) pattern. When a `subscription_upgraded` event arrives, a new row is inserted with `valid_from` = upgrade timestamp and the old row's `valid_to` is updated. This preserves history without ever mutating user facts.

---

### C. Dimension: Features

```sql
CREATE TABLE analytics.dim_features (
  feature_id VARCHAR PRIMARY KEY,
  feature_name VARCHAR NOT NULL,
  feature_category VARCHAR,
  event_types VARCHAR[], -- e.g., ['report_created', 'export_completed']
  first_released DATE
);

-- Populate once, rarely changes
INSERT INTO analytics.dim_features VALUES
  ('reporting', 'Reports', 'Core', ARRAY['report_created']::VARCHAR[], '2024-01-01'),
  ('dashboards', 'Dashboards', 'Core', ARRAY['dashboard_viewed']::VARCHAR[], '2024-02-01'),
  ('export', 'Export', 'Analytics', ARRAY['export_completed']::VARCHAR[], '2024-03-01');
```

**Static**: This is a lookup table. Features don't emit events; events map to features. Maps event types to feature definitions for adoption analysis.

---

### D. Fact: User Retention Cohorts

```sql
CREATE TABLE analytics.fact_user_retention (
  user_id UUID NOT NULL,
  signup_date DATE NOT NULL,
  signup_cohort_week DATE NOT NULL, -- Monday of signup week
  
  day_offset INT NOT NULL, -- 0, 1, 7, 30, ...
  cohort_date DATE NOT NULL, -- signup_date + day_offset
  
  returned BOOLEAN NOT NULL, -- Did user have ANY event on cohort_date?
  event_count INT, -- Number of events on cohort_date
  
  UNIQUE(user_id, day_offset),
  FOREIGN KEY (user_id) REFERENCES dim_users(user_id)
);

CREATE INDEX idx_retention_cohort 
  ON analytics.fact_user_retention(signup_cohort_week, day_offset, returned);
```

**Immutable facts**: One row per user per day-offset. Once a user is marked `returned=TRUE` on day 7, that fact never changes. If new events arrive, we insert new rows for new day-offsets, never update old ones.

**Query example** (7-day retention rate by cohort):
```sql
SELECT 
  signup_cohort_week,
  COUNT(DISTINCT CASE WHEN day_offset = 0 THEN user_id END) as users_acquired,
  COUNT(DISTINCT CASE WHEN day_offset = 7 AND returned THEN user_id END) as users_retained_d7,
  ROUND(100.0 * COUNT(DISTINCT CASE WHEN day_offset = 7 AND returned THEN user_id END) 
        / COUNT(DISTINCT CASE WHEN day_offset = 0 THEN user_id END), 1) as retention_pct
FROM analytics.fact_user_retention
GROUP BY signup_cohort_week
ORDER BY signup_cohort_week DESC;
```

---

### E. Fact: Feature Adoption (First 30 Days)

```sql
CREATE TABLE analytics.fact_feature_adoption (
  user_id UUID NOT NULL,
  feature_id VARCHAR NOT NULL,
  signup_date DATE NOT NULL,
  
  days_to_first_interaction INT, -- How many days until first use?
  first_interaction_date DATE,
  interaction_count INT, -- Total interactions in first 30 days
  
  adopted BOOLEAN, -- Rule: at least 1 interaction
  UNIQUE(user_id, feature_id),
  FOREIGN KEY (user_id) REFERENCES dim_users(user_id),
  FOREIGN KEY (feature_id) REFERENCES dim_features(feature_id)
);

CREATE INDEX idx_adoption_feature 
  ON analytics.fact_feature_adoption(feature_id, adopted);
```

**Adoption rule checkpoint**: How do you define "adopted"? 
- Option A: ≥1 interaction (my default above)
- Option B: ≥3 interactions
- Option C: Feature-specific thresholds (reports: 2+ created, dashboards: 1+ viewed)

This shapes the fact table definition.

**Query example** (feature adoption rates by cohort):
```sql
SELECT 
  f.feature_name,
  ROUND(100.0 * SUM(CASE WHEN fa.adopted THEN 1 ELSE 0 END) 
        / COUNT(*), 1) as adoption_pct,
  COUNT(*) as users_in_period
FROM analytics.fact_feature_adoption fa
JOIN analytics.dim_features f ON fa.feature_id = f.feature_id
WHERE DATE(fa.signup_date) >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY f.feature_name
ORDER BY adoption_pct DESC;
```

---

### F. Fact: Conversion Funnel (Trial → Paid)

```sql
CREATE TABLE analytics.fact_conversion_funnel (
  user_id UUID NOT NULL,
  signup_date DATE NOT NULL,
  signup_plan VARCHAR NOT NULL,
  
  -- Trial events
  trial_started_at TIMESTAMP,
  
  -- Engagement proxy
  first_core_action_at TIMESTAMP, -- First report/dashboard event
  first_core_action_type VARCHAR,
  
  -- Conversion
  converted_to_paid_at TIMESTAMP,
  conversion_plan VARCHAR,
  days_to_conversion INT,
  
  UNIQUE(user_id),
  FOREIGN KEY (user_id) REFERENCES dim_users(user_id)
);

CREATE INDEX idx_funnel_conversion 
  ON analytics.fact_conversion_funnel(
    CASE WHEN converted_to_paid_at IS NOT NULL THEN 1 ELSE 0 END,
    days_to_conversion
  );
```

**Immutable**: One row per user. `converted_to_paid_at` is NULL until they upgrade, then it's set once and frozen.

**Query example** (conversion funnel):
```sql
SELECT 
  COUNT(*) as total_trials,
  COUNT(CASE WHEN first_core_action_at IS NOT NULL THEN 1 END) as users_engaged,
  COUNT(CASE WHEN converted_to_paid_at IS NOT NULL THEN 1 END) as users_converted,
  ROUND(100.0 * COUNT(CASE WHEN converted_to_paid_at IS NOT NULL THEN 1 END) 
        / COUNT(*), 1) as conversion_rate_pct,
  ROUND(AVG(CASE WHEN converted_to_paid_at IS NOT NULL THEN days_to_conversion END), 0) 
    as avg_days_to_conversion
FROM analytics.fact_conversion_funnel
WHERE signup_date >= CURRENT_DATE - INTERVAL '90 days';
```

---

## 4. Implementation Approach

### A. Extract (Daily Job)

```sql
-- Find watermark (last event loaded)
SELECT MAX(marten_version) AS last_version 
FROM analytics.staging_events;

-- Load new events from Marten
INSERT INTO analytics.staging_events (
  event_id, user_id, event_type, event_timestamp, 
  event_data, marten_version
)
SELECT 
  id,
  data->>'user_id'::UUID,
  type,
  timestamp,
  data,
  version
FROM marten.mt_events
WHERE version > :last_version
  AND version <= :last_version + 10000 -- Batch size
ORDER BY version ASC;
```

**Idempotency**: `event_id` primary key prevents duplicate loads. `marten_version` is the source-of-truth sequence.

---

### B. Transform (dbt models)

Create a `dbt/models/analytics/` folder:

```
dbt/models/analytics/
├── staging/
│   └── stg_events.sql          (clean event schema)
├── dimensions/
│   ├── dim_users.sql           (SCD Type 2)
│   └── dim_features.sql
└── facts/
    ├── fact_retention.sql
    ├── fact_adoption.sql
    └── fact_conversion_funnel.sql
```

**Example dbt model** (`dim_users.sql` with dbt-utils SCD):

```sql
{{ config(
  materialized='table',
  unique_key='dbt_scd_id'
) }}

WITH events AS (
  SELECT * FROM {{ ref('stg_events') }}
),

signup_events AS (
  SELECT 
    user_id,
    event_timestamp AS signup_date,
    (event_data->>'plan_type')::VARCHAR AS signup_plan
  FROM events
  WHERE event_type = 'user_signed_up'
),

feature_flags AS (
  SELECT 
    user_id,
    MAX(CASE WHEN event_type IN ('report_created') THEN 1 ELSE 0 END) as has_created_report,
    MAX(CASE WHEN event_type IN ('dashboard_viewed') THEN 1 ELSE 0 END) as has_viewed_dashboard,
    MAX(CASE WHEN event_type IN ('export_completed') THEN 1 ELSE 0 END) as has_exported
  FROM events
  GROUP BY user_id
),

upgrades AS (
  SELECT DISTINCT ON (user_id)
    user_id,
    event_timestamp AS plan_changed_at,
    (event_data->>'new_plan')::VARCHAR AS current_plan
  FROM events
  WHERE event_type = 'subscription_upgraded'
  ORDER BY user_id, event_timestamp DESC
)

SELECT 
  su.user_id,
  DATE(su.signup_date) AS signup_date,
  su.signup_plan,
  COALESCE(u.current_plan, su.signup_plan) AS current_plan,
  u.plan_changed_at,
  ff.has_created_report,
  ff.has_viewed_dashboard,
  ff.has_exported,
  COALESCE(u.plan_changed_at, su.signup_date) AS valid_from,
  NULL::TIMESTAMP AS valid_to,
  TRUE AS is_current,
  {{ dbt_utils.generate_surrogate_key(['su.user_id', 'su.signup_date']) }} AS dbt_scd_id,
  CURRENT_TIMESTAMP AS dbt_updated_at
FROM signup_events su
LEFT JOIN feature_flags ff ON su.user_id = ff.user_id
LEFT JOIN upgrades u ON su.user_id = u.user_id
```

**Incremental loading** (for retention/adoption facts):
```sql
{{ config(
  materialized='incremental',
  unique_key=['user_id', 'day_offset']
) }}

WITH events AS (
  SELECT * FROM {{ ref('stg_events') }}
),

users AS (
  SELECT user_id, DATE(signup_date) AS signup_date 
  FROM {{ ref('dim_users') }}
),

user_days AS (
  SELECT 
    u.user_id,
    u.signup_date,
    DATEPART('week', u.signup_date) AS signup_cohort_week,
    (CURRENT_DATE - u.signup_date) AS day_offset
  FROM users u
  CROSS JOIN LATERAL GENERATE_SERIES(0, 30, 1) AS offsets(day_offset)
  WHERE u.signup_date >= CURRENT_DATE - INTERVAL '90 days'
),

activity AS (
  SELECT 
    user_id,
    DATE(event_timestamp) AS event_date,
    COUNT(*) AS event_count
  FROM events
  WHERE event_timestamp >= CURRENT_DATE - INTERVAL '90 days'
  GROUP BY user_id, DATE(event_timestamp)
)

SELECT 
  ud.user_id,
  ud.signup_date,
  ud.signup_cohort_week,
  ud.day_offset,
  ud.signup_date + ud.day_offset AS cohort_date,
  COALESCE(a.event_count > 0, FALSE) AS returned,
  COALESCE(a.event_count, 0) AS event_count
FROM user_days ud
LEFT JOIN activity a 
  ON ud.user_id = a.user_id 
  AND ud.signup_date + ud.day_offset = a.event_date

{% if execute %}
  WHERE ud.day_offset >= (
    SELECT COALESCE(MAX(day_offset), -1) + 1 
    FROM {{ this }}
    WHERE user_id = ud.user_id
  )
{% endif %}
```

---

## 5. Decision Checkpoints

**1. Adoption Definition**: What counts as "adopted"?
   - At least 1 interaction (simplest)
   - At least 3 interactions (committed use)
   - Feature-specific rules (recommended: export = 1+, reports = 2+)

**2. Retention Windows**: Which day-offsets matter?
   - Standard: D0, D1, D7, D14, D30
   - Could add: D3, D14, D60 for retention curves

**3. Conversion Rules**: What triggers a conversion fact?
   - Any `subscription_upgraded` event (my default)
   - Or only upgrades from trial → paid (exclude plan downgrades)?

**4. Analytics Storage**: Keep in same Postgres or separate DW?
   - **Same Postgres**: Simpler ops, lower cost, works if event volume <1M/day
   - **Separate warehouse (Snowflake/BigQuery)**: Better scaling, SQL optimized for analytics, CDC pipeline adds complexity
   - **Recommendation**: Start in same Postgres with this schema, migrate if query latency becomes an issue

**5. Pipeline Cadence**: Daily, hourly, or real-time?
   - Daily (my assumed default): Sufficient for retention/adoption/conversion, clean daily cohorts
   - Hourly: If you need faster dashboards
   - Real-time (streaming): Overkill unless you're doing live monitoring

**6. Event Timestamp Semantics**: 
   - **event_timestamp** (when event occurred in user's timezone) ✓
   - **server_received_at** (when Marten ingested it) — use this as tiebreaker
   - Do NOT use `created_at` from Marten's internal metadata, it drifts

---

## Summary

This design:
- ✅ **Respects event sourcing**: Immutable append-only facts, no UPDATE statements
- ✅ **Answers your three questions**: Retention (cohort analysis), adoption (feature flags), conversion (funnel facts)
- ✅ **Handles duplicates**: `event_id` PK + `marten_version` deduplication
- ✅ **Scales incrementally**: dbt incremental models, daily loads instead of full replays
- ✅ **Time-travel capable**: SCD Type 2 for user dimensions, event replay possible

**Next steps**: 
1. Confirm the **adoption definition** and **retention windows** to finalize fact table schemas
2. Implement the `staging_events` load job (daily, after event ingestion stabilizes)
3. Build dbt models, starting with `stg_events`, then dimensions, then facts
4. Add BI layer (Looker/Metabase) with pre-built dashboards for retention, adoption, funnel

Does this align with your event structure, or do you need to adjust event properties or add new ones?

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 10.0/17.5 (57%) |
| Evaluated | 2026-05-02 |
| Target duration | 59568 ms |
| Target cost | $0.0797 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent starts by identifying data sources, checking for existing metric definitions and infrastructure, and reviewing what events are already tracked | PARTIAL | Output identifies Marten Event Store as the data source and lists all four events in the Event Tracking Plan. One assumption checkpoint asks 'Do you have a user_signed_up event?' — a form of checking existing events. However, there is no discovery phase for existing metric definitions or existing analytics infrastructure; the agent proceeds directly into design based only on stated assumptions. |
| c2 | Agent produces precise metric definitions (with calculation, granularity, filters, time window, and caveats) for retention, feature adoption, and trial conversion before designing the pipeline | PARTIAL | Metric definitions exist but are embedded inside the data model section (Section 3), after the pipeline architecture (Section 1) is already described. They are not produced 'before designing the pipeline.' The definitions are partially precise — retention uses 'any event on cohort_date', adoption uses 'at least 1 interaction in 30 days', conversion uses 'subscription_upgraded' — but filters and caveats are absent or minimal, and they are spread across table DDL and SQL examples rather than presented as discrete metric definitions. |
| c3 | Agent applies immutable event sourcing principles — never proposes UPDATE/DELETE patterns on event data, only append-only ingestion | PASS | Output explicitly states 'Events flow one direction only. Fact tables are immutable inserts, never updates' and 'Append-only: New events inserted daily. Never updated or deleted.' The staging_events DDL is insert-only. The summary confirms '✅ Respects event sourcing: Immutable append-only facts, no UPDATE statements.' The SCD Type 2 updates on dim_users are on a derived dimension, not on event data itself. |
| c4 | Agent addresses data quality checks at every pipeline boundary (null checks, deduplication, freshness monitoring) | PARTIAL | Deduplication is explicitly addressed at the extraction boundary: 'event_id primary key prevents duplicate loads.' Null detection is implicit in the staging_events DDL via NOT NULL constraints on user_id, event_type, event_timestamp. However, freshness/lag monitoring is entirely absent, and no quality checks are defined at the dbt transformation boundaries (stg_events → facts/dims). Coverage is partial and limited to one pipeline stage. |
| c5 | Agent documents data lineage from source (Marten event store) through transformations to the destination (analytics layer) | PASS | The pipeline architecture diagram shows the full lineage: 'Marten Event Store (Postgres) → [Extraction] → staging_events → [Transformation via dbt] → dim_users / dim_features / fact_retention / fact_adoption / fact_conversion_funnel → [Analytics & BI].' The dbt models section shows ref() chains (stg_events → dims → facts), and the extraction SQL shows how data moves from marten.mt_events to analytics.staging_events. |
| c6 | Agent raises a decision checkpoint before choosing storage technology (architecture commitment) | PASS | Decision Checkpoint #4 explicitly states: 'Analytics Storage: Keep in same Postgres or separate DW?' with options 'Same Postgres: Simpler ops, lower cost, works if event volume <1M/day' and 'Separate warehouse (Snowflake/BigQuery): Better scaling, SQL optimized for analytics, CDC pipeline adds complexity.' The checkpoint is raised before fully committing, with a conditional recommendation ('Start in same Postgres, migrate if query latency becomes an issue'). |
| c7 | Agent includes privacy considerations — identifying which properties contain PII and specifying retention/erasure policy | FAIL | No privacy considerations appear anywhere in the output. PII-bearing fields (user_id, event_data JSONB payloads) are not identified as PII. No data retention period is specified. No erasure or right-to-be-forgotten handling is mentioned, despite the fact that this is a significant concern for an immutable event store. |
| c8 | Agent produces a validation checklist covering lineage, privacy, property types, and sanity checks | FAIL | No validation checklist is produced. The 'Summary' section contains five ✅ bullet points about design properties (event sourcing, three analytic questions, duplicate handling, incremental loading, time-travel) but these are feature claims, not a validation checklist. Lineage validation, privacy checks, property type verification, and sanity checks are all absent. |
| c9 | Agent distinguishes correlation from causation when discussing retention metrics | FAIL | There is no mention of correlation, causation, or interpretive caveats anywhere in the output. The retention metric is presented straightforwardly as 'did user have ANY event on cohort_date?' without any note that return visits correlate with but do not prove the product caused the return. |
| c10 | Output names the four source events from the prompt (`report_created`, `dashboard_viewed`, `export_completed`, `subscription_upgraded`) and traces each to the analytics use case it supports | PASS | All four events are named and traced: report_created → dim_features (reporting) + fact_feature_adoption; dashboard_viewed → dim_features (dashboards) + fact_feature_adoption; export_completed → dim_features (export) + fact_feature_adoption; subscription_upgraded → dim_users (plan change tracking) + fact_conversion_funnel. The dim_features table maps event_types arrays to each feature explicitly. |
| c11 | Output's retention metric defines the exact 7-day window logic — e.g. "user signed up at T returns and triggers any event in (T+6d, T+8d]" — including boundary handling, not just "did they come back after 7 days" | PARTIAL | The output defines retention as 'Did user have ANY event on cohort_date?' where cohort_date = signup_date + day_offset, and the query uses 'day_offset = 7.' This is more specific than 'after 7 days' — it is day-exact (the calendar day of signup_date + 7). However, there is no discussion of boundary handling: no mention of whether it means 7 complete 24-hour periods vs. 7 calendar days, no consideration of timezone effects, and no discussion of a window (e.g., T+6d to T+8d) vs. point-in-time semantics. |
| c12 | Output's feature adoption metric specifies first-30-days as a fixed cohort window from signup, lists which events count as "engagement" with which features, and defines the de-duplication rule (one count per user-feature) | PASS | fact_feature_adoption has 'interaction_count INT, -- Total interactions in first 30 days.' The dim_features table maps event_types to features (e.g., ARRAY['report_created'] for reporting, ARRAY['dashboard_viewed'] for dashboards, ARRAY['export_completed'] for export). The UNIQUE(user_id, feature_id) constraint implements the one-row-per-user-feature de-duplication rule. |
| c13 | Output's funnel metric defines trial-to-paid conversion with explicit start state, terminal state (`subscription_upgraded` event), exclusion rules (cancelled trials, refunds), and time bounds | PARTIAL | fact_conversion_funnel has trial_started_at (start state), converted_to_paid_at derived from subscription_upgraded (terminal state), and days_to_conversion (time bounds). Decision Checkpoint #3 asks about excluding plan downgrades. However, no exclusion rules for cancelled trials or refunds are mentioned anywhere. The start state 'trial' is implicit in signup_plan='trial' but not explicitly defined as a predicate. |
| c14 | Output's data flow describes Marten event store → ETL/CDC → analytics layer with explicit append-only semantics — no UPDATE/DELETE patterns on the activity events themselves, even in transformations | PASS | Architecture diagram shows Marten → Extraction → staging_events → dbt → facts. The extraction SQL uses INSERT INTO ... SELECT with marten_version watermark. dbt incremental model uses insert-only logic (WHERE day_offset >= max from this table). staging_events is declared append-only. The output states 'Append-only: New events inserted daily. Never updated or deleted.' No UPDATE/DELETE is proposed on staging_events or fact tables. |
| c15 | Output documents at least three quality checks (null detection on user_id, deduplication of replayed events, freshness/lag monitoring) at named pipeline stages | PARTIAL | Two of the three named checks are present: (1) deduplication — 'event_id primary key prevents duplicate loads' and 'marten_version ensures deduplication' at the staging_events loading stage; (2) null detection — 'user_id UUID NOT NULL' in the staging_events DDL. Freshness/lag monitoring is entirely absent. The checks are only at one named stage (staging_events) and are not framed as a formal quality gate. |
| c16 | Output addresses event versioning — what happens if an event schema evolves (new property added to `report_created`) given the events are immutable in Marten | FAIL | Event schema evolution is never discussed. The staging_events table uses event_data JSONB which implicitly accommodates new properties, but this is not called out as an intentional design choice for versioning. There is no discussion of what happens when a new field appears in report_created, how stg_events.sql should handle new columns, or how dbt models should be updated. |
| c17 | Output raises a decision checkpoint on the analytics destination (warehouse choice — Snowflake / BigQuery / DuckDB / Postgres replica) before committing rather than picking unilaterally | PASS | Decision Checkpoint #4 explicitly presents 'Same Postgres' vs. 'Separate warehouse (Snowflake/BigQuery)' with tradeoffs for each and a conditional recommendation ('Start in same Postgres with this schema, migrate if query latency becomes an issue') rather than picking unilaterally. |
| c18 | Output identifies the PII and privacy implications — `user_id` linkage, retention period for raw activity, and erasure/right-to-be-forgotten handling for the immutable event store | FAIL | No PII identification, no retention period for raw activity, and no erasure/RTBF discussion anywhere in the output. The user_id field is treated purely as a technical key with no acknowledgement of its privacy implications or of the tension between immutable event sourcing and data erasure requirements. |
| c19 | Output includes a sanity-check on retention causality — flags that "user came back" correlates with engagement but doesn't prove the product caused the return | FAIL | No causality discussion anywhere. The retention metric is presented at face value without any caution about causal interpretation. The output does not distinguish between 'user returned' as a measurement and any causal attribution to the product. |

### Notes

The output is a technically solid engineering design that correctly applies event sourcing principles, documents lineage, and raises the right storage architecture checkpoint. It scores well on the structural/implementation criteria (c3, c5, c6, c10, c12, c14, c17). However, it fails comprehensively on the analytics engineering rigor criteria: no privacy/PII analysis (c7, c18), no validation checklist (c8), no causality caveats for retention metrics (c9, c19), no event schema versioning discussion (c16), and insufficient data quality checks beyond deduplication (c4, c15). The metric definitions — while present — are embedded in DDL and SQL rather than stated as upfront precise definitions with all required elements (c2). The retention boundary logic defines day-exact matching but lacks the window/boundary discussion the criterion requires (c11). The funnel metric is missing exclusion rules for cancellations and refunds (c13). The output reads as a strong data engineering response that would satisfy a backend engineer, but falls short of the full analytics engineering standard the rubric expects — particularly around governance, privacy, causal reasoning, and explicit quality gates at every pipeline stage.
