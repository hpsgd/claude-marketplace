# Write Query

Scenario: Developer invokes the write-query skill to answer: "What percentage of trial users convert to a paid subscription within 14 days, broken down by the acquisition channel they signed up through?"

## Prompt

> Write a query to answer: What percentage of users who started a trial in Q1 2024 converted to a paid subscription within 14 days, broken down by acquisition channel (organic, paid_search, referral, direct)? Exclude internal test accounts and users from the 'acme-corp' domain. Data is in: `users` (user_id, created_at, acquisition_channel, email, is_test_account), `subscriptions` (subscription_id, user_id, status, started_at, plan_type where 'trial' or 'paid').

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

# SQL Query: Q1 2024 Trial-to-Paid Conversion by Acquisition Channel

## Step 1: Question Decomposition

| Element | Definition |
|---|---|
| **Metric** | Conversion rate: % of Q1 2024 trial users who subscribed to a paid plan within 14 days |
| **Time range** | Trial start: 2024-01-01 to 2024-03-31 (Q1); Conversion window: 14 days after trial start |
| **Granularity** | Per acquisition_channel (organic, paid_search, referral, direct) |
| **Filters** | Exclude is_test_account=true; Exclude email domain '@acme-corp.com' |
| **Comparison** | Baseline within each channel (no control group) |

## Step 2: Metric Definitions (MANDATORY)

```
METRIC: Conversion Rate
├─ Numerator: Users with ≥1 'paid' subscription started within 14 days of trial start
├─ Denominator: Users with ≥1 'trial' subscription in Q1 2024
├─ Exclusions: is_test_account=true, email LIKE '%@acme-corp.com'
├─ Time window: Q1 2024 = 2024-01-01 00:00 to 2024-03-31 23:59
└─ 14-day conversion window: trial_start + 0 to 14 days
```

## Step 3: Data Source Documentation

```
TABLE: users
├─ Grain: one row per user
├─ Key: user_id (unique)
├─ Relevant columns: is_test_account, email, acquisition_channel
├─ Data quality: email may be null for some users

TABLE: subscriptions
├─ Grain: one row per subscription
├─ Key: subscription_id (unique)
├─ Foreign key: user_id
├─ Relevant columns: plan_type (values: 'trial', 'paid'), started_at
├─ Data quality: users may have multiple subscriptions
```

## Query

```sql
-- ============================================================
-- BUSINESS QUESTION:
-- What percentage of users who started a trial in Q1 2024 
-- converted to a paid subscription within 14 days, 
-- broken down by acquisition channel?
-- ============================================================
--
-- METRIC DEFINITIONS:
-- Trial User: A user with a subscription where plan_type='trial' 
--             and started_at between 2024-01-01 and 2024-03-31
-- Conversion: A trial user with a paid subscription started 
--             within 14 days of their trial start date
-- Excludes: is_test_account=true, email domain '@acme-corp.com'
--
-- ASSUMPTIONS:
-- 1. Multiple trials per user are counted once (using MIN(started_at))
-- 2. Multiple paid subscriptions per user count as 1 conversion
-- 3. A user who had 2 trials in Q1 is counted once per channel
--
-- KNOWN LIMITATIONS:
-- - Does not account for paid subscriptions that may have been cancelled
-- - Does not distinguish between subscription types (monthly vs annual)
-- - Assumes started_at is reliable (no backdated subscriptions)
-- ============================================================

WITH trial_cohort AS (
    -- Unique trial users in Q1 2024, per acquisition channel
    -- (taking the first trial date per user to establish conversion window)
    SELECT
        u.user_id,
        u.acquisition_channel,
        MIN(s.started_at) AS trial_date
    FROM users u
    INNER JOIN subscriptions s ON u.user_id = s.user_id
    WHERE s.plan_type = 'trial'
      AND s.started_at >= '2024-01-01'
      AND s.started_at < '2024-04-01'  -- Q1 2024
      AND u.is_test_account = FALSE
      AND u.email NOT LIKE '%@acme-corp.com'
    GROUP BY u.user_id, u.acquisition_channel
),

conversions AS (
    -- Trial users who had a paid subscription within 14 days of trial start
    SELECT DISTINCT
        t.user_id
    FROM trial_cohort t
    INNER JOIN subscriptions s ON t.user_id = s.user_id
    WHERE s.plan_type = 'paid'
      AND s.started_at >= t.trial_date
      AND s.started_at <= t.trial_date + INTERVAL '14 days'
)

SELECT
    t.acquisition_channel,
    COUNT(DISTINCT t.user_id) AS trial_users,
    COUNT(DISTINCT c.user_id) AS converted_users,
    ROUND(
        COUNT(DISTINCT c.user_id)::DECIMAL / COUNT(DISTINCT t.user_id) * 100,
        2
    ) AS conversion_rate_pct
FROM trial_cohort t
LEFT JOIN conversions c ON t.user_id = c.user_id
GROUP BY t.acquisition_channel
ORDER BY trial_users DESC;
```

---

## Sanity Checks

**Check 1: Verify sum of trial users matches total trial cohort**
```sql
-- Expected: One row with total matching SUM in main query
SELECT COUNT(DISTINCT user_id) AS total_trial_users
FROM (
    SELECT u.user_id
    FROM users u
    INNER JOIN subscriptions s ON u.user_id = s.user_id
    WHERE s.plan_type = 'trial'
      AND s.started_at >= '2024-01-01'
      AND s.started_at < '2024-04-01'
      AND u.is_test_account = FALSE
      AND u.email NOT LIKE '%@acme-corp.com'
);
```

**Check 2: Verify conversion rate is between 0-100%**
```sql
-- Expected: No rows (all rates should be 0-100)
SELECT acquisition_channel, conversion_rate_pct
FROM [main query above]
WHERE conversion_rate_pct > 100 OR conversion_rate_pct < 0;
```

**Check 3: Verify converted_users ≤ trial_users for each channel**
```sql
-- Expected: No rows (conversion count should never exceed trial count)
SELECT acquisition_channel, trial_users, converted_users
FROM [main query above]
WHERE converted_users > trial_users;
```

**Check 4: Verify all expected acquisition channels are present**
```sql
-- Expected: exactly 4 rows (organic, paid_search, referral, direct)
-- or fewer if some channels have no Q1 trial starts
SELECT acquisition_channel
FROM [main query above];
```

---

## Expected Result Shape

| Column | Type | Example Value |
|---|---|---|
| acquisition_channel | VARCHAR | 'organic', 'paid_search', 'referral', 'direct' |
| trial_users | INTEGER | 245 |
| converted_users | INTEGER | 78 |
| conversion_rate_pct | DECIMAL | 31.84 |

**Expected row count:** 4 (one per acquisition channel, or fewer if some channels have no trials)

**Expected data pattern:** 
- Trial users likely highest for 'organic' or 'paid_search'
- Conversion rates likely 15-40% range (typical SaaS)
- All percentages between 0-100

---

## Caveats & Limitations

1. **Subscription status ignored** — Query counts any 'paid' plan_type regardless of status. If you need only active subscriptions, add `AND status = 'active'` to conversions CTE.

2. **Multiple trial subscriptions** — If a user starts multiple trials in Q1, the query uses their earliest trial date as the conversion window. If you want to count each trial independently, remove the `GROUP BY` and `MIN()` aggregation.

3. **Paid subscription timing** — Query assumes a paid subscription represents true conversion. If some paid subscriptions are test/fraudulent, add additional filters.

4. **Email domain comparison** — Uses `LIKE '%@acme-corp.com'`. Adjust if acme-corp uses subdomains (e.g., `LIKE '%@%.acme-corp.com'` or email LIKE '%@acme-corp%').

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.5/17.5 (100%) |
| Evaluated | 2026-04-30 |
| Target duration | 44711 ms |
| Target cost | $0.0526 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill decomposes the question into precise definitions before writing SQL — states what "converted" means, the time window, filters, and granularity | PASS | Step 1 (Question Decomposition) table and Step 2 (Metric Definitions) explicitly define Metric, Time range, Granularity, Filters, and the 14-day conversion window before any SQL appears. |
| c2 | Metric definitions are written as SQL comments at the top of the query — including inclusion and exclusion criteria | PASS | The SQL block opens with a multi-line comment block defining 'Trial User', 'Conversion', 'Excludes', Assumptions, and Known Limitations before the first CTE. |
| c3 | Query uses CTEs over subqueries — no nested subqueries | PASS | Query uses `WITH trial_cohort AS (...)` and `conversions AS (...)` — no nested subqueries anywhere in the SQL. |
| c4 | Query filters out test accounts (`is_test_account = false`) and acme-corp domain explicitly | PASS | `AND u.is_test_account = FALSE` and `AND u.email NOT LIKE '%@acme-corp.com'` appear in the trial_cohort CTE WHERE clause. |
| c5 | Skill includes at least 2 sanity check queries — checking percentages are 0-100, row counts are reasonable, and no NULL acquisition channels in output | PASS | 4 sanity checks provided: Check 2 verifies `conversion_rate_pct > 100 OR conversion_rate_pct < 0` (0–100 range), Check 1 verifies total trial user count, Check 3 verifies converted_users ≤ trial_users, Check 4 verifies the 4 expected acquisition channels are present. |
| c6 | Final SELECT column names are descriptive — not aliased as `a`, `b`, `c` | PASS | Final SELECT outputs `acquisition_channel`, `trial_users`, `converted_users`, `conversion_rate_pct` — all fully descriptive. |
| c7 | Data sources section documents the grain of each table used and any known data quality issues | PASS | Step 3 documents: users grain = 'one row per user', subscriptions grain = 'one row per subscription'. Data quality notes: 'email may be null for some users' and 'users may have multiple subscriptions'. |
| c8 | Query handles the case where a user has multiple trial subscriptions (deduplication logic) | PARTIAL | trial_cohort CTE uses `MIN(s.started_at) AS trial_date` with `GROUP BY u.user_id, u.acquisition_channel` to take the earliest trial per user. However, grouping by both user_id AND acquisition_channel means a user who tried two channels would appear twice — not a fully general deduplication. Ceiling is PARTIAL. |
| c9 | Output includes the query with full documentation header, sanity checks, expected result shape, and any caveats | PASS | All four components present: SQL block with comment header, four numbered sanity check queries, 'Expected Result Shape' table with example values, and 'Caveats & Limitations' section with 4 items. |
| c10 | Output's documentation header (SQL comments) defines "trial user" (any user with a row in `subscriptions` where `plan_type = 'trial'`), "converted" (subsequent row with `plan_type = 'paid'`), and the 14-day window (paid.started_at - trial.started_at <= 14 days) | PASS | SQL comment defines: 'Trial User: A user with a subscription where plan_type=\'trial\' and started_at between 2024-01-01 and 2024-03-31', 'Conversion: A trial user with a paid subscription started within 14 days of their trial start date', and the window is enforced in code via `s.started_at <= t.trial_date + INTERVAL '14 days'`. |
| c11 | Output explicitly filters Q1 2024 by trial start (`started_at >= '2024-01-01' AND started_at < '2024-04-01'`) — not by paid conversion date — so Q1 cohorts are measured properly | PASS | trial_cohort CTE WHERE clause: `AND s.started_at >= '2024-01-01'` and `AND s.started_at < '2024-04-01'` applied on `plan_type = 'trial'` rows. The conversions CTE has no date range filter, correctly allowing conversions beyond Q1. |
| c12 | Output excludes test accounts via `is_test_account = false` and the acme-corp domain via `email NOT LIKE '%@acme-corp.com'` (or domain-extracted equivalent), with both filters visible at the cohort-defining stage | PASS | Both filters appear in the trial_cohort CTE (the cohort-defining stage): `AND u.is_test_account = FALSE` and `AND u.email NOT LIKE '%@acme-corp.com'`. |
| c13 | Output uses CTEs (WITH clauses) named for what they compute — e.g. `trial_cohort`, `converted_users`, `final_metrics` — not nested subqueries or one giant SELECT | PASS | CTEs are named `trial_cohort` and `conversions` — both names clearly describe their computational purpose. |
| c14 | Output's final SELECT groups by `acquisition_channel` and reports both the converted count and the conversion rate (percentage), with descriptive column names like `trial_users`, `converted_within_14d`, `conversion_rate_pct` | PASS | Final SELECT: `GROUP BY t.acquisition_channel`, outputs `trial_users`, `converted_users`, `conversion_rate_pct` — all descriptive. Uses `converted_users` instead of `converted_within_14d` but is equally descriptive. |
| c15 | Output handles users with multiple trial subscriptions by deduplicating to one trial row per user (e.g. earliest trial in Q1) before joining — the `users.user_id` should appear at most once in the cohort | PASS | `MIN(s.started_at) AS trial_date` with `GROUP BY u.user_id, u.acquisition_channel` ensures each user appears once per channel with their earliest trial date before the conversions join. |
| c16 | Output includes at least 2 sanity check queries: one verifying `conversion_rate_pct` falls in [0, 100], and one verifying every output row has a non-NULL `acquisition_channel` from the four expected values | PASS | Check 2 explicitly tests `WHERE conversion_rate_pct > 100 OR conversion_rate_pct < 0`. Check 4 selects all acquisition_channel values from the output and comments 'Expected: exactly 4 rows (organic, paid_search, referral, direct)' — surfacing any NULL or unexpected channels. |
| c17 | Output documents the grain of `users` (one row per user) and `subscriptions` (one row per subscription, multiple per user possible) and notes the dependency on `started_at` accuracy | PASS | Step 3: users grain = 'one row per user', subscriptions grain = 'one row per subscription'. Data quality: 'users may have multiple subscriptions'. Assumptions: 'Assumes started_at is reliable (no backdated subscriptions)'. |
| c18 | Output addresses edge cases — users who churned then re-subscribed, users who paid before officially trialling, users with overlapping trial windows — even just to state how each is handled | PARTIAL | Caveats mention 'Subscription status ignored' (touches on churn/re-subscribe: status='active' filter suggestion) and 'Multiple trial subscriptions' (overlapping windows partially addressed). Users who paid before trialling and overlapping trial windows are not explicitly addressed. |
| c19 | Output includes an expected result shape (e.g. 4 rows, one per acquisition_channel, with conversion rates between 0% and ~25%) so the reader can sanity-check actual results against expectations | PARTIAL | 'Expected Result Shape' section shows 4 rows with example values and states 'Conversion rates likely 15-40% range (typical SaaS)'. Row count expectation ('4 rows, one per acquisition channel') is explicit. Ceiling is PARTIAL. |

### Notes

The output is comprehensive and well-structured, meeting every criterion fully or at its ceiling. Decomposition, metric definitions, CTE structure, filters, sanity checks, and documentation are all exemplary. The main minor gap is in c8/c15: grouping by both user_id AND acquisition_channel means a user who appeared in two channels would be counted twice — not a true cross-channel deduplication. Edge-case coverage (c18) mentions status/multi-trial but omits pre-trial paid users and overlapping windows. All PARTIAL-capped criteria were met at their ceiling, yielding a perfect score within the scoring constraints.
