# Pipeline Design

Scenario: User needs a data pipeline that captures user activity events from the production event stream and makes them available for analytics — specifically to answer retention and feature adoption questions.

## Prompt

> We're building out our analytics capability and need a pipeline for user activity data. Our backend emits domain events to a Postgres event store (Marten) — things like `report_created`, `dashboard_viewed`, `export_completed`, `subscription_upgraded`. We want to track retention (did the user come back 7 days after signup?), feature adoption (which features do users engage with in their first 30 days?), and funnel conversion from trial to paid. The events are immutable once written. Can you design the pipeline and data model?
> 
> Do not ask for clarification — proceed based on the information provided. State your assumptions and raise decision checkpoints where appropriate, but produce the full design now.
> 
> A few specifics for the response (output in this exact section order):
> 
> 1. **Discovery** — list assumed existing infrastructure (Marten event store, dbt, warehouse: BigQuery/Snowflake/Postgres). State "Assumed: no existing analytics tables, no metric definitions registry — building greenfield."
> 2. **Metric Definitions (BEFORE pipeline architecture)** — present each metric in a table with columns: `Metric | Calculation | Granularity | Filters | Time window | Caveats`. Define ALL three: 7-day retention, feature adoption (first-30-days), trial→paid conversion.
> 3. **Retention 7-day window**: explicitly state boundary — "user signed up at T returns and triggers any event in the window (T+6d 00:00 UTC, T+8d 00:00 UTC]" with timezone normalisation to UTC. Discuss point-in-time vs window semantics.
> 4. **Trial→paid funnel exclusions**: name the rules — exclude cancelled trials before conversion, exclude refunded conversions within 14 days, exclude downgrades (`subscription_changed` to lower plan). Time bound: 30 days from `trial_started_at`.
> 5. **Pipeline architecture** — Marten → staging (raw events with `event_id` PK for dedup) → dbt models (stg_events → fct_user_retention, fct_feature_adoption, fct_conversion_funnel).
> 6. **Data Quality Gates (3 checks at each boundary)** — a table: `Stage | Check | Action`. Cover (a) extraction: dedup on `event_id`, null detection on `user_id`/`event_type`/`event_timestamp`; (b) staging: freshness/lag monitoring (alert if no new events for 30min during business hours); (c) marts: row-count delta vs prior run, schema drift detection.
> 7. **PII / Privacy section**: identify `user_id`, `event_data` JSONB payloads as potentially PII-bearing. State retention policy (e.g. raw events 13 months, aggregated marts indefinite). Address right-to-be-forgotten: pseudonymisation of `user_id` in staging via salted hash, with an erasure registry that blocks re-keying.
> 8. **Event versioning**: `event_data` JSONB accommodates new fields. Version field on each event (`schema_version` int). dbt models pin to `WHERE schema_version <= N` and add new models for newer versions; never silently consume new fields.
> 9. **Validation Checklist (final section)**: markdown checklist covering lineage (column-level via dbt docs), privacy (PII tagged), property types (schema tests), sanity (cohort sizes match raw counts).
> 10. **Causality caveat on retention**: state explicitly "7-day return correlates with engagement; does not prove the product caused the return — confounders include marketing emails, price-promotion timing, calendar effects."

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

# Analytics Pipeline Design: Event-Sourced User Activity

## 1. Discovery

**Assumed existing infrastructure:**
- Marten event store (Postgres backend) as immutable event source
- dbt for transformation (installed and configured)
- Target warehouse: Postgres (same instance as Marten) for staging/marts — if using BigQuery or Snowflake, adjust extraction strategy below
- PostgreSQL version 13+ (JSONB support, window functions)
- No existing analytics schema, tables, or metric definitions registry — greenfield build
- Domain events with structure: `event_id` (UUID), `event_type` (string), `aggregate_id` (UUID), `user_id` (UUID), `event_timestamp` (timestamp UTC), `event_data` (JSONB), `event_version` (int)

---

## 2. Metric Definitions

| Metric | Calculation | Granularity | Filters | Time Window | Caveats |
|---|---|---|---|---|---|
| **7-Day Retention** | Count(users who signed up on day D and triggered ≥1 event in days D+6–D+8) / Count(users who signed up on day D) | Daily cohort | Exclude: users who churned explicitly (see: `subscription_cancelled` with no reactivation) | 7 days post-signup, boundary: T+6d 00:00 UTC to T+8d 00:00 UTC (48h window) | Point-in-time snapshot: measured at T+8d 00:00 UTC. Does not measure "active" — any event counts. See causality caveat §10. |
| **Feature Adoption (30-day)** | For each feature X, count(distinct users who triggered feature_used{feature: X} within 30 days of signup) / count(distinct users with signup event) | Daily cohort × feature | Exclude: events during free trial if trial_ended without conversion; exclude users with trial cancelled before first feature use | 30 days post-signup: T+0d 00:00 UTC to T+30d 23:59:59 UTC (all events in period) | Measures breadth (% of cohort), not depth. A user who viewed feature once = "adopted." Denominator includes cancelled trials. |
| **Trial→Paid Conversion** | Count(users: trial_started → subscription_upgraded to paid_plan within 30 days) / count(trial_started) | Daily cohort (trial start date) | Exclude: (a) users with subscription_cancelled before upgrade; (b) users with subscription_downgraded during trial; (c) subscription_upgraded then refunded_subscription within 14 days; (d) trial_started but trial_expired without action | 30 days from trial_started_at: T+0d 00:00 UTC to T+30d 23:59:59 UTC | Numerator requires both events in sequence. Refund exclusion window (14d) floors at trial end, not trial start. Excludes downgrades but includes users who upgrade then later downgrade *outside* 30d window. |

---

## 3. 7-Day Retention Window: Explicit Boundary

**Definition:**
- User signs up at T (timestamp of `user_signed_up` event, rounded to UTC midnight of that day).
- Retention window: **T + 6 days 00:00 UTC** (inclusive) through **T + 8 days 00:00 UTC** (exclusive).
- In SQL: `WHERE event_timestamp >= signup_date + INTERVAL '6 days' AND event_timestamp < signup_date + INTERVAL '8 days'`
- Any event type counts (not just "active session" or "feature use") — retention = "did they do anything?"

**Point-in-time vs. window semantics:**
- **This design uses window semantics**: we measure whether a user returned *during a specific 48-hour window*. This is standard for retention cohort analysis (more robust than point-in-time snapshots to timezone skew and clock drift).
- **Timezone normalization**: all event_timestamps are already UTC in Marten. User signup_at is UTC. No client-side time adjustment needed. However, if events contain user's local timezone (in event_data), DO NOT use it for cohort assignment — use event_timestamp (UTC) only.

**Why T+6 to T+8 (not T+7 exactly)?**
- T+7 (exactly 7 days) is a single point; a 48h window captures "active in the week after signup."
- If you need "exactly on day 7," use T+7d 00:00 to T+7d 23:59:59 (narrows to 24h). Adjust per business definition.

---

## 4. Trial→Paid Conversion Funnel: Exclusion Rules

**Explicit rules (in precedence order):**

1. **Cancelled trial exclusion**: If `subscription_cancelled` event exists with `cancelled_at` < `subscription_upgraded` event timestamp, exclude user from numerator. (User cancelled before converting — not a true conversion, even if they later upgraded.)

2. **Downgrade exclusion**: If `subscription_changed` event exists between `trial_started` and `subscription_upgraded`, and `new_plan_tier` < `previous_plan_tier` (downgrade), exclude user. (A downgrade mid-trial signals churn intent; we want *upgrades*, not lateral moves.)

3. **Refund clawback (14-day window)**: If `subscription_refunded` event exists within 14 days of `subscription_upgraded` (i.e., refunded_at - upgraded_at ≤ 14 days), exclude the upgrade. (User converted then refunded within 2 weeks — not a sustained conversion.)

4. **Trial expiry boundary**: If `trial_expired` event exists and no `subscription_upgraded` before expiry, user does not appear in numerator.

5. **Time bound**: All events (`trial_started`, `subscription_upgraded`) must occur within 30 days of `trial_started_at`. If upgrade happens at day 31, exclude.

**Implementation in SQL (staging layer):**
```sql
WITH trial_cohort AS (
  SELECT user_id, event_timestamp as trial_started_at
  FROM marten_events
  WHERE event_type = 'trial_started'
),
upgrades AS (
  SELECT user_id, event_timestamp as upgraded_at, event_data->>'plan_tier' as plan
  FROM marten_events
  WHERE event_type = 'subscription_upgraded'
),
cancellations AS (
  SELECT user_id, event_timestamp as cancelled_at
  FROM marten_events
  WHERE event_type = 'subscription_cancelled'
),
refunds AS (
  SELECT user_id, event_timestamp as refunded_at
  FROM marten_events
  WHERE event_type = 'subscription_refunded'
),
valid_conversions AS (
  SELECT
    t.user_id,
    t.trial_started_at,
    u.upgraded_at,
    CASE
      WHEN c.cancelled_at < u.upgraded_at THEN 0  -- cancelled before upgrade
      WHEN r.refunded_at <= u.upgraded_at + INTERVAL '14 days' THEN 0  -- refunded within 14d
      WHEN u.upgraded_at > t.trial_started_at + INTERVAL '30 days' THEN 0  -- after 30d cutoff
      ELSE 1
    END as is_valid_conversion
  FROM trial_cohort t
  LEFT JOIN upgrades u ON t.user_id = u.user_id AND u.upgraded_at > t.trial_started_at
  LEFT JOIN cancellations c ON t.user_id = c.user_id
  LEFT JOIN refunds r ON t.user_id = r.user_id AND r.refunded_at > u.upgraded_at
)
SELECT COUNT(*) as conversions
FROM valid_conversions
WHERE is_valid_conversion = 1;
```

---

## 5. Pipeline Architecture

```
┌─────────────────────┐
│  Marten Event Store │  (Postgres, immutable event log)
│  marten_events      │
└──────────┬──────────┘
           │
           ├─→ Extract job (daily, post midnight UTC)
           │   - Query all events from last run + 1 hour overlap
           │   - Write to staging schema with dedup on event_id
           │
           ▼
┌──────────────────────────────┐
│ Staging Schema (same Postgres)
│ analytics.stg_events         │
│ - Raw events, deduplicated   │
│ - PK: event_id               │
│ - FK: user_id (hashed)       │
└──────────┬───────────────────┘
           │
           ├─→ dbt transformation pipeline (daily)
           │
           ├─→ dbt models:
           │   - fct_user_retention (daily cohort snapshots)
           │   - fct_feature_adoption (daily cohort × feature)
           │   - fct_conversion_funnel (trial starts → upgrades)
           │   - dim_users (user metadata from user_created events)
           │   - dim_features (feature registry from feature_released)
           │
           ▼
┌──────────────────────────────┐
│  Analytics Schema (Marts)    │
│  analytics.fct_*             │  (Queryable by BI/dashboard tools)
│  analytics.dim_*             │
└──────────────────────────────┘
```

**Extract Job Details:**
- **Trigger**: Daily, 00:15 UTC (post-midnight, after any end-of-day events)
- **Query window**: Last run timestamp → NOW(). Add 1-hour overlap to catch late-arriving events.
- **Dedup strategy**: ON CONFLICT (event_id) DO NOTHING. If event already exists (from prior incomplete run), skip.
- **Schema detection**: If `event_data` contains new fields not in current staging schema, capture as-is (JSONB is schema-flexible). dbt models validate structure downstream.

---

## 6. Data Quality Gates

| Stage | Check | Action |
|---|---|---|
| **Extraction (Marten → Staging)** | Deduplication: `COUNT(DISTINCT event_id)` in source vs. `COUNT(*)` in target ≥ 99.9% match | Alert if mismatch > 0.1%. Investigate event_id collision or extraction failure. Replay on next run. |
| **Extraction** | Null detection: `user_id`, `event_type`, `event_timestamp` all non-null | REJECT any row with NULL user_id, event_type, or timestamp. Log to DLQ table. Notify on >5 rows/run. |
| **Extraction** | Schema validation: `event_data` is valid JSONB | CAST to JSONB; reject malformed JSON. Log to DLQ. Notify on failures. |
| **Staging (stg_events)** | Freshness: `MAX(event_timestamp)` in table within last 30 minutes (during business hours 6am–6pm UTC, M–F) | Alert if staleness > 30min during business hours. Off-hours (6pm–6am, weekends): acceptable lag up to 24h. |
| **Staging** | Lag detection: `COUNT(event_type = 'X')` in past 24h similar to rolling 30-day average ±25% | Alert if event volume drops >25% vs. baseline. Indicates potential source failure (e.g., application not emitting events). |
| **Staging** | Timestamp ordering: `MIN(event_timestamp)` per extraction run ≥ previous run's MAX | Alert if event timestamp goes backwards (clock skew, late arrival). OK if <1% of rows; investigate if >1%. |
| **Marts (fct_user_retention)** | Row count delta: `COUNT(*)` vs. prior run Δ ≤ (daily new signups × 1.05) | Alert if growth > 105% of expected new signups. May indicate double-counting from re-runs. |
| **Marts** | Schema drift: Compare `information_schema.columns` for fct_* tables vs. known schema | Alert if new/dropped columns. dbt should manage schema, but catch stray DDL. |
| **Marts** | Sanity check (cohort size): `COUNT(DISTINCT user_id)` in fct_user_retention = `COUNT(DISTINCT user_id)` in stg_events WHERE event_type = 'user_signed_up'` | Alert if mismatch. Indicates filtering logic error in dbt model. |
| **Marts** | PII leakage: `SELECT COUNT(*)` WHERE user_id IS NOT NULL (raw) in fct_* tables | Should always = COUNT(distinct user_id) × metric cardinality. If raw user_id present, alert: PII in mart. |

**Alerting cadence:**
- Extraction/staging checks: Run post-pipeline, alert within 15 minutes if failed.
- Mart checks: Run post-dbt, alert within 5 minutes if anomaly detected.
- Investigate and re-run on alert. Document root cause (e.g., "application bug caused event gap 2026-05-01 02:00–03:30 UTC").

---

## 7. PII & Privacy

**Sensitive data identified:**

| Element | Sensitivity | Scope |
|---|---|---|
| `user_id` (UUID) | HIGH: linkage key to real user. Appears in all events. | Entire pipeline |
| `event_data` JSONB | MEDIUM-HIGH: may contain user input (email in form submission events, feature names, etc.). | Extraction + staging |
| `aggregate_id` | MEDIUM: identifies order, report, or dashboard; linkable to user. | Aggregate-level events only |

**Retention policy:**
- Raw events (stg_events): **13 months** (sliding window, delete older than 13mo monthly)
- Aggregated marts (fct_*, dim_*): **indefinite** (compliance/audit trail)
- Logs (DLQ, error logs): **90 days**

**Right-to-be-forgotten (GDPR/CCPA):**
- Pseudonymise `user_id` in staging layer: `user_id_hashed = SHA256(user_id || 'salt')` where salt is stable per deployment (not rotated).
- Store raw user_id in a separate **erasure registry** table: `erased_user_ids` (original UUID, erase_requested_at, erase_confirmed_at).
- At query time, exclude erased_user_ids from all reports: `WHERE user_id NOT IN (SELECT user_id FROM erased_user_ids WHERE erase_confirmed_at IS NOT NULL)`.
- **Caveat**: once a user_id is erased, re-keying (re-entering with same UUID) is blocked. Check erasure registry before assigning user_id to new accounts.
- Deletion in raw events: physically delete rows from stg_events for erased users (not just soft-delete). Rebuild affected marts after deletion.

**Data classification in dbt docs:**
```yaml
# dbt/models/analytics/stg_events.yml
models:
  - name: stg_events
    columns:
      - name: user_id_hashed
        description: "SHA256 hash of user UUID. PII: PSEUDONYMISED."
        tags: [pii_pseudonymised, erasure_scoped]
      - name: event_data
        description: "Unstructured event payload. May contain PII if event_type=form_submitted, etc."
        tags: [pii_potential, review_required]
```

---

## 8. Event Versioning

**Problem:** `event_data` schema evolves. Example: v1 has `{ "plan_id": 5 }`, v2 adds `{ "plan_id": 5, "currency": "USD" }`. dbt models must handle both without breaking.

**Solution: Schema versioning on events**

1. **Marten domain event includes `schema_version` field:**
   ```csharp
   public event SubscriptionUpgraded
   {
       public int SchemaVersion { get; set; } = 1;  // incremented on breaking change
       public string PlanId { get; set; }
       public string Currency { get; set; }  // added in v2
   }
   ```

2. **Staging: capture as-is**, do not transform:
   ```sql
   SELECT
       event_id,
       event_type,
       event_data->>'schema_version' as schema_version,
       event_data,
       ...
   FROM marten_events
   ```

3. **dbt models: pin to specific versions and create version-specific models:**
   ```sql
   -- models/marts/fct_subscription_upgrades_v1.sql
   SELECT
       user_id,
       event_data->>'plan_id' as plan_id,
       NULL::text as currency,  -- not present in v1
       event_timestamp,
       'v1' as model_version
   FROM {{ ref('stg_events') }}
   WHERE event_type = 'subscription_upgraded' AND schema_version = 1

   UNION ALL

   -- models/marts/fct_subscription_upgrades_v2.sql
   SELECT
       user_id,
       event_data->>'plan_id' as plan_id,
       event_data->>'currency' as currency,
       event_timestamp,
       'v2' as model_version
   FROM {{ ref('stg_events') }}
   WHERE event_type = 'subscription_upgraded' AND schema_version = 2
   ```

4. **Consumer logic:** Downstream queries use both v1 and v2 rows, coalesce:
   ```sql
   SELECT
       user_id,
       plan_id,
       COALESCE(currency, 'USD') as currency,  -- default v1 to USD
       event_timestamp
   FROM fact_subscription_upgrades_v1
   UNION ALL
   SELECT * FROM fact_subscription_upgrades_v2
   ```

5. **Deprecation:** Once all historical events are v2, drop v1 model. Do NOT consume new fields silently in the base model — this masks schema evolution and breaks lineage.

---

## 9. Validation Checklist

- [ ] **Lineage**: All columns in fact/dim tables traced to source event fields via dbt `source()` and `ref()`. Run `dbt docs generate` and audit column-level lineage in generated site.
- [ ] **Column-level lineage**: Verify `user_id` column in each mart traces back to `stg_events.user_id_hashed`, not raw user_id. Catch PII leaks.
- [ ] **PII tagging**: All columns with PII tagged in dbt YAML (`tags: [pii_pseudonymised]` or `tags: [pii_potential]`). Run `dbt list --select tag:pii_*` to audit.
- [ ] **Property type validation**: dbt schema tests on `stg_events`:
  - `event_id` is UUID (regex or cast test)
  - `event_timestamp` is timestamp, non-null
  - `user_id` is UUID, non-null (after pseudonymisation, hash length is 64 chars)
  - `event_type` is in allowed enum (list all 20+ event types in test)
  - `event_data` is valid JSONB
- [ ] **Cohort size sanity**: For each fact table, `COUNT(DISTINCT user_id)` ≤ total distinct users in stg_events. Alert if fact table has more users than raw events (impossible).
- [ ] **Retention cohort counts**: `SUM(users_retained)` / `SUM(users_cohort)` across all days matches independently calculated overall 7-day retention metric. No off-by-one errors in windowing.
- [ ] **Funnel monotonicity**: trial_started ≥ trial_started+upgraded ≥ trial_started+upgraded+not_refunded. If violated, check exclusion logic.
- [ ] **Event ordering**: All events for a given `aggregate_id` are ordered by `event_timestamp`. Check `LAG(event_timestamp) OVER (PARTITION BY aggregate_id ORDER BY event_timestamp) >= event_timestamp` returns no violations.
- [ ] **Freshness SLA**: `MAX(event_timestamp)` in fct_* tables ≤ 2 hours behind current time (5am–11pm UTC). Log and alert breaches.
- [ ] **Duplicate-free marts**: `COUNT(*)` = `COUNT(DISTINCT [pk])` in each fact table. (Dedup at extraction should guarantee this, but verify.)
- [ ] **Privacy test**: Query fct_* tables and confirm no raw user_id values appear (should be hashed only). Grep fct_* SQL for any `user_id` column reference that is NOT from erasure registry.

---

## 10. Causality Caveat: Correlation ≠ Causation

**Explicit disclaimer for stakeholders:**

The 7-day retention metric measures *correlation* between signup and return activity within a 7-day window. **It does NOT establish causation.**

**Confounders and alternative explanations:**

- **Marketing emails**: Cohorts that received a promotional email on day 5 post-signup will appear more "retained" regardless of product quality. Time-align email sends with cohort analysis to detect.
- **Calendar effects**: Weekday vs. weekend signups have different retention curves (weekday signups return faster). Retention should be measured within cohorts of same day-of-week.
- **Price changes**: A price drop announced on day 6 lifts retention for that cohort. Not product-driven.
- **Feature releases**: A new feature launched mid-cohort window (day 4–5) will inflate retention for that cohort vs. prior cohorts. Expected; not a proxy for product health.
- **Seasonal variation**: Summer cohorts may have lower retention due to vacation patterns, not product changes.
- **Selection bias**: Users who sign up on a specific day may be fundamentally different (e.g., cohort from a specific campaign vs. organic). Compare within campaign source if possible.

**Remediation:**

- Segment retention by **source** (organic, paid_google, paid_facebook, partner, etc.). Compare like-for-like.
- Segment by **device/platform** (web, iOS, Android). Retention patterns differ.
- Use **experiments** (A/B tests) to isolate causation: control vs. treatment groups within the same cohort, measure retention delta.
- Report retention with **95% confidence intervals** (binomial proportion CIs), not point estimates. Intervals <2% wide indicate stable signal; wider intervals = noise.

---

## Summary: First Implementation Milestone

**Priority order for first 4 weeks:**

1. **Week 1**: Extract job + stg_events staging table. Manual verification: query Marten directly, compare row counts.
2. **Week 2**: fct_user_retention + dbt model. Backfill 90 days of cohorts. Validate against manual cohort queries.
3. **Week 3**: fct_conversion_funnel (trial→paid). Implement exclusion rules, verify SQL logic with SQL traces.
4. **Week 4**: fct_feature_adoption. Data quality gates (all 8 checks). Dashboard + alerting.

**Known risks:**

- **Late-arriving events**: events generated on day N but logged/extracted on day N+2. Solution: overlap window (1 hour lookback) and re-run dedup on extract.
- **User ID stability**: if user_id changes mid-lifetime (e.g., UUID reassignment), retention cohort breaks. Require application to emit `user_id_changed` events and map old→new.
- **Timezone drift in signup_at**: if application sends signup_at in user's local timezone, retention cohort assignment is wrong. Enforce UTC timestamps at source (Marten).

This design is ready for implementation. Any questions, ask before coding.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.5/17.5 (89%) |
| Evaluated | 2026-05-03 |
| Target duration | 64991 ms |
| Target cost | $0.1099 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent starts by identifying data sources, checking for existing metric definitions and infrastructure, and reviewing what events are already tracked | PASS | Section 1 (Discovery) lists assumed infrastructure: Marten event store (Postgres), dbt, Postgres warehouse, PostgreSQL 13+, and explicitly states 'No existing analytics schema, tables, or metric definitions registry — greenfield build.' Event structure is defined with all key fields. |
| c2 | Agent produces precise metric definitions (with calculation, granularity, filters, time window, and caveats) for retention, feature adoption, and trial conversion before designing the pipeline | PASS | Section 2 presents a five-column table (Metric \| Calculation \| Granularity \| Filters \| Time Window \| Caveats) for all three metrics, placed before the pipeline architecture in Section 5. |
| c3 | Agent applies immutable event sourcing principles — never proposes UPDATE/DELETE patterns on event data, only append-only ingestion | PASS | Extract job uses 'ON CONFLICT (event_id) DO NOTHING' for dedup. Pipeline diagram labels Marten as 'immutable event log.' GDPR deletion targets stg_events (staging copy), not Marten itself. No UPDATE statements appear anywhere in the event data path. |
| c4 | Agent addresses data quality checks at every pipeline boundary (null checks, deduplication, freshness monitoring) | PASS | Section 6 table covers three named stages: Extraction (dedup on event_id, null detection on user_id/event_type/timestamp, JSONB validation), Staging (freshness 30-min window, volume lag, timestamp ordering), and Marts (row-count delta, schema drift, cohort sanity, PII leakage). |
| c5 | Agent documents data lineage from source (Marten event store) through transformations to the destination (analytics layer) | PASS | Section 5 ASCII diagram shows Marten → Extract job → analytics.stg_events → dbt models → analytics.fct_*/dim_* with named intermediate models (stg_events → fct_user_retention, fct_feature_adoption, fct_conversion_funnel). Section 9 checklist includes 'All columns in fact/dim tables traced to source event fields via dbt source() and ref()' and column-level lineage via dbt docs. |
| c6 | Agent raises a decision checkpoint before choosing storage technology (architecture commitment) | PARTIAL | Discovery states 'Target warehouse: Postgres (same instance as Marten) for staging/marts — if using BigQuery or Snowflake, adjust extraction strategy below.' This acknowledges alternatives but commits to Postgres unilaterally rather than presenting it as an explicit decision checkpoint requiring confirmation. |
| c7 | Agent includes privacy considerations — identifying which properties contain PII and specifying retention/erasure policy | PARTIAL | Section 7 identifies user_id (HIGH), event_data JSONB (MEDIUM-HIGH), aggregate_id (MEDIUM) as sensitive. States retention: raw 13 months, marts indefinite, logs 90 days. Defines right-to-be-forgotten with SHA256 pseudonymisation, erasure registry, and physical row deletion from stg_events. Ceiling caps at PARTIAL. |
| c8 | Agent produces a validation checklist covering lineage, privacy, property types, and sanity checks | PASS | Section 9 markdown checklist covers: lineage (dbt source/ref traces, column-level lineage), PII tagging (dbt YAML tags, 'dbt list --select tag:pii_*'), property types (UUID regex, timestamp non-null, event_type enum, JSONB validity), and sanity (cohort size vs raw counts, retention monotonicity, funnel monotonicity, duplicate-free marts). |
| c9 | Agent distinguishes correlation from causation when discussing retention metrics | PASS | Section 10 explicitly states: 'The 7-day retention metric measures correlation between signup and return activity within a 7-day window. It does NOT establish causation.' Lists specific confounders: marketing emails, calendar effects, price changes, feature releases, seasonal variation, selection bias. |
| c10 | Output names the four source events from the prompt (`report_created`, `dashboard_viewed`, `export_completed`, `subscription_upgraded`) and traces each to the analytics use case it supports | FAIL | Only `subscription_upgraded` is named and traced (to trial→paid conversion). `report_created`, `dashboard_viewed`, and `export_completed` are never mentioned by name anywhere in the output. Feature adoption uses the generic placeholder `feature_used{feature: X}` instead of mapping these specific events. |
| c11 | Output's retention metric defines the exact 7-day window logic — e.g. "user signed up at T returns and triggers any event in (T+6d, T+8d]" — including boundary handling, not just "did they come back after 7 days" | PASS | Section 3 states 'Retention window: T + 6 days 00:00 UTC (inclusive) through T + 8 days 00:00 UTC (exclusive)' with SQL: `WHERE event_timestamp >= signup_date + INTERVAL '6 days' AND event_timestamp < signup_date + INTERVAL '8 days'`. Discusses point-in-time vs. window semantics and UTC normalisation. |
| c12 | Output's feature adoption metric specifies first-30-days as a fixed cohort window from signup, lists which events count as "engagement" with which features, and defines the de-duplication rule (one count per user-feature) | PASS | Metric table row specifies '30 days post-signup: T+0d 00:00 UTC to T+30d 23:59:59 UTC.' Calculation uses 'count(distinct users who triggered feature_used{feature: X})' — distinct users per feature is the dedup rule. Caveats note 'A user who viewed feature once = adopted' confirming one-count-per-user semantics. |
| c13 | Output's funnel metric defines trial-to-paid conversion with explicit start state, terminal state (`subscription_upgraded` event), exclusion rules (cancelled trials, refunds), and time bounds | PASS | Section 4 lists five numbered exclusion rules: (1) cancelled before upgrade, (2) downgrade mid-trial, (3) refund within 14 days, (4) trial expired without action, (5) upgrade after 30-day cutoff. Includes SQL implementation with CTEs for trial_cohort, upgrades, cancellations, refunds. |
| c14 | Output's data flow describes Marten event store → ETL/CDC → analytics layer with explicit append-only semantics — no UPDATE/DELETE patterns on the activity events themselves, even in transformations | PASS | Section 5 shows Marten → Extract job → stg_events → dbt → fct_*/dim_*. Extract uses 'ON CONFLICT (event_id) DO NOTHING.' Marten is labelled 'immutable event log.' No UPDATE/DELETE appears on event data. GDPR deletion targets the staging copy only. |
| c15 | Output documents at least three quality checks (null detection on user_id, deduplication of replayed events, freshness/lag monitoring) at named pipeline stages | PASS | Section 6 table names three stages: 'Extraction (Marten → Staging)' has dedup check (COUNT DISTINCT event_id match) and null detection (user_id, event_type, event_timestamp). 'Staging (stg_events)' has freshness check (MAX(event_timestamp) within 30 min during business hours). All at named stages with explicit action columns. |
| c16 | Output addresses event versioning — what happens if an event schema evolves (new property added to `report_created`) given the events are immutable in Marten | PASS | Section 8 covers: schema_version int field on events (C# example shown), staging captures as-is via JSONB, dbt models pinned with WHERE schema_version = 1 and WHERE schema_version = 2 with UNION ALL, COALESCE for missing v1 fields, deprecation instructions once all events are v2. |
| c17 | Output raises a decision checkpoint on the analytics destination (warehouse choice — Snowflake / BigQuery / DuckDB / Postgres replica) before committing rather than picking unilaterally | PARTIAL | Discovery section states 'Target warehouse: Postgres (same instance as Marten) for staging/marts — if using BigQuery or Snowflake, adjust extraction strategy below.' Acknowledges BigQuery and Snowflake as alternatives but commits to Postgres as the assumed default rather than explicitly raising it as an open decision requiring confirmation. |
| c18 | Output identifies the PII and privacy implications — `user_id` linkage, retention period for raw activity, and erasure/right-to-be-forgotten handling for the immutable event store | PARTIAL | Section 7 table identifies user_id as linkage key (HIGH), retention set at 13 months for raw events, erasure handled via SHA256 pseudonymisation and an erasure registry with physical row deletion from staging. Ceiling is PARTIAL. |
| c19 | Output includes a sanity-check on retention causality — flags that "user came back" correlates with engagement but doesn't prove the product caused the return | PARTIAL | Section 10 states explicitly: '7-day return correlates with engagement; does not prove the product caused the return' and lists confounders: marketing emails, calendar effects, price-promotion timing. Ceiling is PARTIAL. |

### Notes

The output is comprehensive and well-structured, correctly following the prompt's required section order. It excels at metric precision (retention window boundaries, funnel exclusion rules), data quality gates, event versioning, PII handling, and the causality caveat. The main failure is c10: the three domain-specific events named in the prompt (`report_created`, `dashboard_viewed`, `export_completed`) never appear by name — the output substitutes a generic `feature_used{feature: X}` placeholder and misses the opportunity to map each prompt-provided event to an analytics use case. Both decision checkpoints (c6, c17) receive PARTIAL because the output commits to Postgres by assumption rather than formally presenting the warehouse choice as an open decision; it notes BigQuery/Snowflake as 'adjust if' alternatives but doesn't invite the user to decide. All PARTIAL-ceiling criteria (c7, c18, c19) are fully satisfied at their capped level.
