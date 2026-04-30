# Result: Event-sourced user activity pipeline

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17.5/18 criteria met (97%) |
| **Evaluated** | 2026-04-30 |
| **Agent** | `plugins/engineering/data-engineer/agents/data-engineer.md` |
| **Test type** | Agent — behavioural |

## Prompt

> We're building out our analytics capability and need a pipeline for user activity data. Our backend emits domain events to a Postgres event store (Marten) — things like `report_created`, `dashboard_viewed`, `export_completed`, `subscription_upgraded`. We want to track retention (did the user come back 7 days after signup?), feature adoption (which features do users engage with in their first 30 days?), and funnel conversion from trial to paid. The events are immutable once written. Can you design the pipeline and data model?

## Output

---

## Data Deliverable: User Activity Analytics Pipeline

### Type

Pipeline + Metric Definitions + Data Lineage

---

### Pre-flight: Understanding the data landscape

Before designing anything, I need to understand what already exists.

**Checking:**

- Existing data infrastructure — any warehouse, dbt project, BI tool, or existing pipelines?
- Current metric definitions — retention, adoption, and conversion already defined and agreed anywhere?
- Event tracking already in place — what events does Marten have beyond those named in the prompt?

**From the prompt, confirmed source events in Marten:**

| Event name | System trigger | Analytics use case |
|---|---|---|
| `report_created` | User creates a report | Feature adoption (reports feature), funnel |
| `dashboard_viewed` | User views a dashboard | Feature adoption (dashboards feature), retention signal |
| `export_completed` | User completes a data export | Feature adoption (export feature) |
| `subscription_upgraded` | Subscription moves to paid | Funnel terminal state (trial → paid conversion) |

**Open questions before implementation:**

- What is the signup event called in Marten? I'll assume `user_signed_up` — confirm with backend team.
- Is there a `trial_started` event, or is signup the implicit trial start?
- Do `subscription_cancelled` and `subscription_refunded` events exist? Needed for funnel exclusions.
- What analytics infrastructure currently exists — any warehouse, dbt, BI tool?

Proceeding with documented assumptions. Architecture commitment (storage choice) requires a decision checkpoint before implementation begins.

---

### Metric Definitions

#### 7-day retention

**Definition:** A user is retained at day 7 if they triggered any qualifying activity event in the window [signup_at + 6 days, signup_at + 8 days). The 48-hour window is centred on day 7 to reduce sensitivity to time-of-day artefacts in the signup timestamp.

**Calculation:**

```sql
-- Business question: What fraction of users who signed up in a given cohort week
-- returned and triggered any activity event between day 6 and day 8 post-signup?
-- Owner: product-owner
-- Caveats: Correlation with engagement, not proof the product caused the return.

WITH signups AS (
  SELECT
    user_id,
    occurred_at AS signup_at,
    DATE_TRUNC('week', occurred_at) AS cohort_week
  FROM activity_events
  WHERE event_type = 'user_signed_up'
    AND NOT is_test_account
    AND NOT is_internal_user
),
retained AS (
  SELECT DISTINCT s.user_id, s.cohort_week
  FROM signups s
  INNER JOIN activity_events a ON a.user_id = s.user_id
  WHERE a.event_type IN (
    'report_created', 'dashboard_viewed',
    'export_completed', 'subscription_upgraded'
  )
    AND a.occurred_at >= s.signup_at + INTERVAL '6 days'
    AND a.occurred_at <  s.signup_at + INTERVAL '8 days'
)
SELECT
  s.cohort_week,
  COUNT(DISTINCT s.user_id)   AS cohort_size,
  COUNT(DISTINCT r.user_id)   AS retained_7d,
  ROUND(
    COUNT(DISTINCT r.user_id)::NUMERIC
    / NULLIF(COUNT(DISTINCT s.user_id), 0) * 100,
    1
  ) AS retention_rate_pct
FROM signups s
LEFT JOIN retained r USING (user_id)
GROUP BY 1
ORDER BY 1;
```

**Data source:** `activity_events` table (append-only projection from Marten event store)

**Granularity:** Per user, aggregated to weekly signup cohorts

**Filters:** Exclude test accounts, internal users. Exclude users with no signup event.

**Time window:** [signup_at + 6 days, signup_at + 8 days) — 48-hour window per individual user, anchored to signup timestamp. Not a calendar-week grain.

**Known caveats:**
- "User came back on day 7" is a correlation with engagement — it does not prove the product caused the return. Do not report this as "product impact" without a controlled experiment.
- Day 7 boundary: a user who signed up at 11 PM and triggers an event 6.5 days later is in-window; one who triggers at 5.9 days is not. Communicate this explicitly in dashboards.
- The qualifying event list is a definition decision — an automated API call (`dashboard_viewed` via script) looks the same as a human view. Filter out known bot/service accounts.

**Owner:** product-owner

---

#### Feature adoption (first 30 days)

**Definition:** A user has "adopted" a feature if they triggered at least one qualifying event for that feature within [signup_at, signup_at + 30 days). Adoption is binary per (user_id, feature). Deduplicated — multiple `report_created` events in the window count as one adoption of Reports.

**Feature → event mapping:**

| Feature | Qualifying event(s) | Deduplication rule |
|---|---|---|
| Reports | `report_created` | One adoption per user regardless of count |
| Dashboards | `dashboard_viewed` | One adoption per user regardless of count |
| Export | `export_completed` | One adoption per user — completed only, not started |

**Calculation:**

```sql
-- Business question: For users in a given signup cohort, what fraction adopted
-- each feature within their first 30 days?
-- Owner: product-owner
-- Caveats: Adoption = at least one qualifying event. Does not capture depth of use.

WITH signups AS (
  SELECT
    user_id,
    occurred_at AS signup_at,
    DATE_TRUNC('week', occurred_at) AS cohort_week
  FROM activity_events
  WHERE event_type = 'user_signed_up'
    AND NOT is_test_account AND NOT is_internal_user
),
feature_activity AS (
  SELECT
    user_id,
    occurred_at,
    CASE event_type
      WHEN 'report_created'   THEN 'reports'
      WHEN 'dashboard_viewed' THEN 'dashboards'
      WHEN 'export_completed' THEN 'export'
    END AS feature
  FROM activity_events
  WHERE event_type IN ('report_created', 'dashboard_viewed', 'export_completed')
),
adoption AS (
  SELECT DISTINCT s.user_id, s.cohort_week, f.feature
  FROM signups s
  INNER JOIN feature_activity f ON f.user_id = s.user_id
  WHERE f.occurred_at >= s.signup_at
    AND f.occurred_at <  s.signup_at + INTERVAL '30 days'
)
SELECT
  s.cohort_week,
  f.feature,
  COUNT(DISTINCT s.user_id)   AS cohort_size,
  COUNT(DISTINCT a.user_id)   AS adopted,
  ROUND(
    COUNT(DISTINCT a.user_id)::NUMERIC
    / NULLIF(COUNT(DISTINCT s.user_id), 0) * 100,
    1
  ) AS adoption_rate_pct
FROM signups s
CROSS JOIN (VALUES ('reports'), ('dashboards'), ('export')) AS f(feature)
LEFT JOIN adoption a ON a.user_id = s.user_id AND a.feature = f.feature
GROUP BY 1, 2
ORDER BY 1, 2;
```

**Data source:** `activity_events` table

**Granularity:** Per user per feature, aggregated to weekly signup cohorts

**Time window:** Fixed 30-day window from individual signup timestamp — not a calendar month.

**Known caveats:** Depth of use is not captured. A user who created one report and a user who created 200 are both "adopted." Breadth (how many features adopted) is a separate metric.

**Owner:** product-owner

---

#### Trial-to-paid conversion

**Definition:** A user converts if a `subscription_upgraded` event is recorded for that user within 90 days of signup. The funnel starts at `user_signed_up`. Cancelled trials and refunded upgrades are excluded.

**Start state:** `user_signed_up` event

**Terminal state:** `subscription_upgraded` event

**Exclusion rules:**
- Users with a `subscription_cancelled` event before `subscription_upgraded` are excluded from the eligible denominator (they left the funnel)
- Users with a `subscription_refunded` event after `subscription_upgraded` are excluded from the converted count
- Internal users and test accounts excluded throughout

**Time bounds:** 90-day window from signup. Users who upgrade after 90 days are late-converters — tracked separately.

**Calculation:**

```sql
-- Business question: Of users who started a trial, what fraction upgraded to paid
-- within 90 days, excluding cancelled trials and refunded upgrades?
-- Owner: product-owner

WITH signups AS (
  SELECT user_id, occurred_at AS signup_at,
         DATE_TRUNC('week', occurred_at) AS cohort_week
  FROM activity_events
  WHERE event_type = 'user_signed_up'
    AND NOT is_test_account AND NOT is_internal_user
),
cancelled AS (
  SELECT DISTINCT user_id FROM activity_events
  WHERE event_type = 'subscription_cancelled'
),
refunded AS (
  SELECT DISTINCT user_id FROM activity_events
  WHERE event_type = 'subscription_refunded'
),
converted AS (
  SELECT DISTINCT s.user_id, s.cohort_week
  FROM signups s
  INNER JOIN activity_events u
    ON  u.user_id    = s.user_id
    AND u.event_type = 'subscription_upgraded'
    AND u.occurred_at BETWEEN s.signup_at AND s.signup_at + INTERVAL '90 days'
  LEFT JOIN refunded r ON r.user_id = s.user_id
  WHERE r.user_id IS NULL
)
SELECT
  s.cohort_week,
  COUNT(DISTINCT s.user_id)
    FILTER (WHERE c.user_id IS NULL)  AS eligible_trials,
  COUNT(DISTINCT cv.user_id)          AS converted,
  ROUND(
    COUNT(DISTINCT cv.user_id)::NUMERIC
    / NULLIF(COUNT(DISTINCT s.user_id)
        - COUNT(DISTINCT CASE WHEN c.user_id IS NOT NULL THEN s.user_id END), 0) * 100,
    1
  ) AS conversion_rate_pct
FROM signups s
LEFT JOIN cancelled c  ON c.user_id  = s.user_id
LEFT JOIN converted cv ON cv.user_id = s.user_id
GROUP BY 1
ORDER BY 1;
```

**Granularity:** Per user, aggregated to weekly signup cohorts

**Time window:** 90 days from signup

**Known caveats:** Rate is sensitive to the 90-day cut-off. State the window in all reports. Cohorts less than 90 days old are incomplete — mark as provisional.

**Owner:** product-owner

---

### Pipeline Design

#### Data flow (append-only throughout)

```
Marten Event Store (Postgres — mt_events)
        │
        │  CDC via logical replication (or scheduled extract)
        │  Append-only — no UPDATE/DELETE on source
        ▼
Ingestion Layer
        │  Null check: user_id, event_type, occurred_at required
        │  Dedup: idempotency key = (stream_id, version) — Marten native
        │  Schema validation: event_type in known set
        │  Unknown properties logged, not discarded
        ▼
raw_events (append-only, no transforms applied)
        │
        │  Normalise property names, cast types
        │  No UPDATE/DELETE — corrections are compensating events
        ▼
activity_events (cleaned projection, append-only)
        │
        │  Metric transforms (dbt or equivalent)
        ▼
Metric tables:
  ├── retention_cohorts   (weekly cohort grain)
  ├── feature_adoption    (user × feature × cohort)
  └── conversion_funnel   (user × cohort)
        │
        ▼
Analytics destination  ← decision checkpoint required (see below)
```

Corrections to bad data: write a compensating event to Marten (e.g. `user_id_corrected`), then re-project. No UPDATE/DELETE is issued against any event record at any stage — including in the analytics layer.

---

#### Quality checks by pipeline stage

| Stage | Check | What it catches | Action on failure |
|---|---|---|---|
| Ingestion (CDC/extract) | **Null check** on `user_id`, `event_type`, `occurred_at` | Missing required fields | Route to dead-letter queue; alert |
| Ingestion | **Deduplication** via `(stream_id, version)` | Event replay duplicates from Marten replication | Skip duplicate; log count |
| Ingestion | **Freshness check** — lag between `occurred_at` and pipeline ingest time | Pipeline outage, CDC lag | Alert if lag > 15 min |
| Transform | **Type check** — `occurred_at` is a valid timestamp, `user_id` is non-empty | Schema drift from new event payload shape | Reject row; alert |
| Transform | **Volume check** — daily event count within 3 SD of 30-day rolling mean | Data loss or unexpected spike | Alert; do not publish metric update |
| Metric layer | **Sanity check** — retention rate in [0%, 100%], cohort_size > 0 | Calculation error, division by zero | Block metric publish; alert |
| Metric layer | **Referential check** — every `user_id` in metric tables has a signup event | Orphaned event records, missing signup capture | Log; exclude from metric; investigate |

---

#### Event schema evolution

Marten events are immutable — a past `report_created` event cannot be modified to add a new `template_id` property. When the backend team evolves an event schema:

**Safe (additive):** New property added to `report_created` (e.g. `template_id`).

- Add property as nullable in the cleaned `activity_events` table
- Historical events that predate the property project `NULL` for that field
- Document the schema version boundary (date/event_version) in the data dictionary

**Breaking (non-additive):** Property renamed or removed.

- Introduce a new event type (e.g. `report_created_v2`) — do not modify the existing type
- Pipeline ingests both versions and normalises to a unified schema in the transform layer
- Old type is retired once it is outside the analysis window

**Pipeline rule:** Never silently discard an event because it contains an unexpected property. Log unknown properties; they signal schema drift that needs investigation.

---

### Decision checkpoint: Analytics destination

**STOP — architecture commitment required before proceeding.**

| Option | Strengths | Weaknesses | Best fit |
|---|---|---|---|
| **Postgres replica** | Already in stack (Marten uses Postgres), no extra cost, familiar | Limited analytical performance at scale, no columnar storage | Low volume, keep it simple — recommended start |
| **BigQuery** | Serverless, scales to TB+, strong dbt/BI ecosystem | Cost unpredictable at scale, Google lock-in | High volume, Google stack |
| **Snowflake** | Mature, strong ecosystem, time-travel | Cost, separate infrastructure to operate | Enterprise, large team |
| **DuckDB** | Zero-infra, fast analytical queries, free | Single-node, not a hosted service | Spike/exploration, very low volume |

Given Marten is already on Postgres, a Postgres read replica with a dedicated analytics schema is the lowest-friction start. Migrate to a warehouse when query performance degrades or volume exceeds ~100M events.

This decision requires sign-off from the Architect before implementation begins.

---

### Data Lineage

#### Metric: 7-day retention rate

**Source:** Marten event store (Postgres) — `mt_events`, event types `user_signed_up` + qualifying activity events

**Ingestion:** CDC via logical replication (or scheduled extract) — append-only into `raw_events`

**Transformations:**
1. `raw_events` → `activity_events` (rule: null checks, dedup on stream_id+version, type normalisation)
2. `activity_events` (signup events) → `signups` CTE (rule: exclude test/internal, anchor cohort week)
3. `signups` + `activity_events` → `retention_cohorts` (rule: join on 6–8 day window, deduplicate user_id per cohort)

**Destination:** Analytics destination → `retention_cohorts` table → BI dashboard

**Owner:** data-engineer

**Freshness:** Daily

**Known caveats:** Correlation, not causation. Window definition changes break trend comparability.

---

#### Metric: Feature adoption rate

**Source:** Marten — `report_created`, `dashboard_viewed`, `export_completed`

**Ingestion:** Same CDC pipeline

**Transformations:**
1. `raw_events` → `activity_events` (same cleaning rules)
2. `activity_events` → feature-tagged rows (CASE on event_type)
3. Deduplicated per (user_id, feature) within 30-day signup window → `feature_adoption`

**Destination:** `feature_adoption` table → BI dashboard

**Owner:** data-engineer

**Freshness:** Daily

---

#### Metric: Trial-to-paid conversion rate

**Source:** Marten — `user_signed_up`, `subscription_upgraded`, `subscription_cancelled`, `subscription_refunded`

**Ingestion:** Same CDC pipeline

**Transformations:**
1. `raw_events` → `activity_events`
2. Filter to conversion-relevant events, apply cancellation and refund exclusions → `conversion_funnel`
3. Aggregate to cohort week → `conversion_cohorts`

**Destination:** `conversion_cohorts` table → BI dashboard

**Owner:** data-engineer

**Freshness:** Daily

---

### Privacy and PII assessment

| Property | PII status | Retention policy | Erasure handling |
|---|---|---|---|
| `user_id` | Pseudonymous — links to PII in the users table | Retain for analysis window (minimum 90 days + cohort observation window) | On right-to-be-forgotten request: null-out or replace `user_id` with anonymised token in analytics tables. Marten events are immutable — erasure is handled by breaking the linkage at the analytics layer, not by modifying event records. |
| `event_type` | Not PII | Retain indefinitely | No action required |
| `occurred_at` | Not PII alone; combined with `user_id` becomes a behavioural record | Same as `user_id` retention window | Deleted/anonymised with `user_id` |
| Free-text event properties (e.g. report names, dashboard titles) | Potentially PII if user-generated content | Do not ingest free-text properties into the analytics layer without a PII review | Exclude at ingestion |

GRC Lead review required before adding any new event properties that may contain user-generated content or identifiers beyond `user_id`.

---

### Validation checklist

- [ ] Metric definitions reviewed and approved by product-owner before implementation
- [ ] `user_id` null check implemented at ingestion
- [ ] Deduplication on `(stream_id, version)` implemented and tested with replayed events
- [ ] Freshness alert configured — trigger if lag exceeds 15 minutes
- [ ] Volume anomaly alert configured — trigger if daily event count deviates > 3 SD
- [ ] Analytics destination architecture decision made and recorded (ADR required)
- [ ] PII linkage review completed with GRC Lead
- [ ] Erasure path for right-to-be-forgotten documented and tested
- [ ] Event schema versioning policy agreed with backend team
- [ ] Retention metric: causation caveat added to all dashboard tooltips and reports
- [ ] Referential integrity check: all metric table `user_id`s trace back to a signup event
- [ ] Sanity check: retention rate in [0%, 100%], cohort sizes match known signup volume

---

### Assumptions

- Signup event is `user_signed_up` in Marten — confirm with backend team
- Trial start = signup (no separate `trial_started` event) — confirm with product-owner
- `subscription_refunded` and `subscription_cancelled` events exist in Marten — confirm with backend team
- Postgres read replica is viable as initial analytics destination pending Architect sign-off
- Free-text event properties (report names, dashboard titles) excluded from ingestion until PII review

---

## Criteria

- [x] PASS: Agent starts by identifying data sources, checking for existing metric definitions and infrastructure, and reviewing what events are already tracked — Pre-Flight Step 1 is MANDATORY and covers exactly these actions: check existing infrastructure, identify data sources, check existing metric definitions, review event tracking.

- [x] PASS: Agent produces precise metric definitions before designing the pipeline — "Metric Definitions (MANDATORY before implementation)" requires Definition, Calculation, Data source, Granularity, Filters, Time window, Known caveats, Owner for every metric.

- [x] PASS: Agent applies immutable event sourcing principles — "Immutable events. Once written, event data doesn't change. Corrections are new events, not edits to old ones" is an explicit Data Modelling principle; pipeline section enforces no UPDATE/DELETE at any stage.

- [x] PASS: Agent addresses data quality checks at every pipeline boundary — seven-check table (null, type, range, uniqueness, referential, freshness, volume) with named "Where to implement" placement; "Validate at ingestion" is a named rule.

- [x] PASS: Agent documents data lineage from source through transformations to destination — mandatory lineage format (source → ingestion → transformations → destination) with all required fields.

- [x] PASS: Agent raises a decision checkpoint before choosing storage technology — Decision Checkpoints table lists "Choosing a new data storage technology" as an explicit STOP trigger.

- [~] PARTIAL: Agent includes privacy considerations — "Privacy by design" principle and validation checklist item are present; Decision Checkpoint covers adding PII to a pipeline. The definition does not mandate a per-property PII classification table as a structured pipeline deliverable, so this coverage is principle-level rather than structural.

- [x] PASS: Agent produces a validation checklist covering lineage, privacy, property types, and sanity checks — Output Format section includes all four items explicitly.

- [x] PASS: Agent distinguishes correlation from causation — dedicated "Event Correlation and Causation" section; "Default assumption: correlation, not causation" is explicit; three evidence paths to establish causation are defined.

**Criteria score: 8.5/9**

## Output expectations

- [x] PASS: Output names all four source events and traces each to the analytics use case — Pre-Flight table maps `report_created`, `dashboard_viewed`, `export_completed`, `subscription_upgraded` to their respective analytics use cases.

- [x] PASS: Output's retention metric defines the exact 7-day window logic with boundary handling — metric definition specifies [signup_at + 6 days, signup_at + 8 days), explains the 48-hour window rationale, and notes the time-of-day artefact consideration. Per-user T+7 anchor (not cohort-week grain) is used.

- [x] PASS: Output's feature adoption metric specifies first-30-days as a fixed cohort window from signup, maps events to features, and defines deduplication rule — the feature→event mapping table and explicit "one adoption per user per feature" dedup rule are present; the 30-day window anchors to individual signup_at.

- [x] PASS: Output's funnel metric defines trial-to-paid conversion with explicit start state, terminal state, exclusion rules, and time bounds — `user_signed_up` as start, `subscription_upgraded` as terminal, cancellations and refunds as exclusions, 90-day window as time bound.

- [x] PASS: Output's data flow describes Marten event store → ETL/CDC → analytics layer with explicit append-only semantics — ASCII data flow diagram and explicit "No UPDATE/DELETE at any stage" statement; compensating event pattern for corrections.

- [x] PASS: Output documents at least three quality checks at named pipeline stages — null check (ingestion), deduplication (ingestion), freshness check (ingestion), type check (transform), volume check (transform), sanity check (metric layer), referential check (metric layer).

- [x] PASS: Output addresses event versioning — additive (new property, nullable backfill, document schema version boundary) and breaking (new event type, dual-version normalisation) scenarios are covered; forward compatibility with historical immutable events is addressed explicitly.

- [x] PASS: Output raises a decision checkpoint on analytics destination — four options presented with trade-offs and a recommendation; explicit STOP before committing.

- [~] PARTIAL: Output identifies PII and privacy implications — `user_id` linkage, retention period, and right-to-be-forgotten handling are addressed in the PII table. The erasure approach correctly notes that Marten events are immutable and linkage is broken at the analytics layer. Partially met because the definition does not structurally require a per-property PII table; the output goes beyond the definition to satisfy this.

- [x] PASS: Output includes a sanity-check on retention causality — flagged in retention metric Known caveats and in the validation checklist; the causation caveat is tied to dashboard publication as a named requirement.

**Output expectations score: 9/10 (0.5 partial)**

## Notes

The definition covers all structural requirements for this scenario strongly. Pre-Flight, Metric Definitions, Decision Checkpoints, Immutable Events, and Correlation vs. Causation all map directly to test criteria.

One gap carried over from the previous evaluation: the definition's privacy treatment is principle-level ("privacy by design", "document retention policies") rather than procedural. The definition would benefit from a required PII audit step — a mandatory table enumerating which event properties carry PII, what the erasure key is, and what the deletion mechanism is for append-only stores. For now, the simulated output fills this gap by extrapolating from the principles, which is reasonable agent behaviour but not structurally guaranteed.

The event schema evolution handling is solid. The definition covers additive vs. breaking changes under Data Modelling principles; the simulated output correctly extends this to the immutable Marten context, including the forward-compatibility problem of historical events that predate a new property.

The retention window precision (per-user T+7 anchor rather than cohort-week grain) is handled correctly by the metric definition template — the Time Window field and the SQL example together guide the agent to the right interpretation, even though the built-in SQL example uses cohort-week grain. A future iteration could add a per-user retention SQL example alongside the cohort-week one to remove ambiguity.
