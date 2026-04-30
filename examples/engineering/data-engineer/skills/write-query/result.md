# Result: Write a trial-to-paid conversion funnel query

**Verdict:** PASS
**Score:** 17/19 criteria met (89%)
**Evaluated:** 2026-04-30

## Output

The following is the simulated output the `write-query` skill would produce for the given prompt.

---

### Question Decomposition

Before writing SQL, the skill requires decomposing the question into precise definitions:

| Dimension | Definition |
|---|---|
| What is being measured? | Percentage of trial users who converted to paid within 14 days of their trial start |
| Time range (cohort window) | Trial started between 2024-01-01 and 2024-03-31 (Q1 2024) |
| Time range (conversion window) | Up to 14 calendar days after the user's trial `started_at` |
| Granularity | Per acquisition channel (organic, paid_search, referral, direct) |
| Inclusion | Users with a `subscriptions` row where `plan_type = 'trial'` in the cohort window |
| Exclusions | `is_test_account = true`, email domain `@acme-corp.com` |
| Comparison | No period-over-period comparison — single Q1 2024 cohort |

**Converted** = the same user has a subsequent `subscriptions` row where `plan_type = 'paid'` and `paid.started_at - trial.started_at <= 14 days`.

**Multiple trials per user**: deduplicate to the earliest trial in Q1 2024 per user before joining.

---

### Data Sources

| Table | Grain | Key | Known issues |
|---|---|---|---|
| `users` | One row per user | `user_id` (unique) | `email` may be null for SSO users — acme-corp filter applies only where email is non-null |
| `subscriptions` | One row per subscription | `subscription_id` (unique) | Multiple rows per user expected — must deduplicate trials to one per user before aggregating |

Dependency: accuracy of conversion rate depends entirely on `subscriptions.started_at` being recorded at the moment of plan activation, not billing date.

---

### Main Query

```sql
-- ============================================================
-- BUSINESS QUESTION: What percentage of users who started a trial
--   in Q1 2024 converted to a paid subscription within 14 days,
--   broken down by acquisition channel?
-- AUTHOR: data-engineer
-- DATE: 2026-04-30
-- ============================================================
--
-- METRIC DEFINITIONS:
-- Trial User:   A user with a row in `subscriptions` where plan_type = 'trial'
--               and started_at >= '2024-01-01' AND started_at < '2024-04-01'
--               Excludes: is_test_account = true, email LIKE '%@acme-corp.com'
--               When a user has multiple Q1 trial rows, use the earliest (MIN started_at)
--
-- Converted:    The same user also has a row in `subscriptions` where plan_type = 'paid'
--               and paid.started_at - trial.started_at <= INTERVAL '14 days'
--               (measured from the user's earliest Q1 trial start)
--
-- Conversion Rate: converted_users / trial_users * 100, rounded to 1 decimal
--
-- ASSUMPTIONS:
-- 1. started_at is recorded at activation time — billing delays would undercount conversions
-- 2. SSO users with NULL email are included unless is_test_account is set
-- 3. Users who paid before officially trialling are excluded (paid.started_at < trial.started_at)
-- 4. acquisition_channel NULLs would appear as NULL in output — see sanity check 2
--
-- DATA SOURCES:
-- users:         one row per user; email may be NULL for SSO users
-- subscriptions: one row per subscription; multiple plan_type rows per user expected
--
-- KNOWN LIMITATIONS:
-- - Does not account for users who churned and re-subscribed (only first paid after trial counted)
-- - Users who converted to paid before any formal trial row are excluded by the join condition
-- - Acquisition channel is captured at signup, not at trial start — channel changes are ignored
-- ============================================================

WITH

-- Step 1: Define the trial cohort (Q1 2024, one row per user — earliest trial)
trial_cohort AS (
    SELECT
        u.user_id,
        u.acquisition_channel,
        MIN(s.started_at) AS trial_started_at
    FROM users u
    INNER JOIN subscriptions s
        ON u.user_id = s.user_id
        AND s.plan_type = 'trial'
    WHERE s.started_at >= '2024-01-01'
      AND s.started_at < '2024-04-01'
      AND u.is_test_account = FALSE
      AND (u.email NOT LIKE '%@acme-corp.com' OR u.email IS NULL)
    GROUP BY
        u.user_id,
        u.acquisition_channel
),

-- Step 2: Find users who converted to paid within 14 days of their trial start
converted_users AS (
    SELECT DISTINCT
        tc.user_id
    FROM trial_cohort tc
    INNER JOIN subscriptions s
        ON tc.user_id = s.user_id
        AND s.plan_type = 'paid'
        AND s.started_at > tc.trial_started_at
        AND s.started_at <= tc.trial_started_at + INTERVAL '14 days'
),

-- Step 3: Aggregate by acquisition channel
channel_metrics AS (
    SELECT
        tc.acquisition_channel,
        COUNT(DISTINCT tc.user_id)                              AS trial_users,
        COUNT(DISTINCT cu.user_id)                             AS converted_within_14d
    FROM trial_cohort tc
    LEFT JOIN converted_users cu ON tc.user_id = cu.user_id
    GROUP BY
        tc.acquisition_channel
)

-- Step 4: Final output with conversion rate
SELECT
    acquisition_channel,
    trial_users,
    converted_within_14d,
    ROUND(
        converted_within_14d::DECIMAL / NULLIF(trial_users, 0) * 100,
        1
    ) AS conversion_rate_pct
FROM channel_metrics
ORDER BY conversion_rate_pct DESC NULLS LAST;
```

---

### Sanity Check Queries

```sql
-- SANITY CHECK 1: Conversion rates must be in [0, 100]
-- Expected: 0 rows returned
SELECT
    acquisition_channel,
    conversion_rate_pct
FROM channel_metrics
WHERE conversion_rate_pct > 100
   OR conversion_rate_pct < 0;

-- SANITY CHECK 2: All output rows must have a non-NULL acquisition_channel
--   from the four expected values (organic, paid_search, referral, direct)
-- Expected: 0 rows returned
SELECT
    acquisition_channel,
    trial_users
FROM channel_metrics
WHERE acquisition_channel IS NULL
   OR acquisition_channel NOT IN ('organic', 'paid_search', 'referral', 'direct');

-- SANITY CHECK 3: Converted users cannot exceed trial users in any channel
-- Expected: 0 rows returned
SELECT
    acquisition_channel,
    trial_users,
    converted_within_14d
FROM channel_metrics
WHERE converted_within_14d > trial_users;

-- SANITY CHECK 4: Row count — expect exactly 4 rows (one per acquisition channel)
-- Expected: 4
SELECT COUNT(*) AS row_count FROM channel_metrics;
```

---

### Expected Result Shape

4 rows, one per acquisition channel. Approximate expected values (industry benchmarks for SaaS trial-to-paid, adjust based on your product):

| acquisition_channel | trial_users | converted_within_14d | conversion_rate_pct |
|---|---|---|---|
| referral | ~800 | ~160 | ~20.0 |
| organic | ~2,400 | ~360 | ~15.0 |
| paid_search | ~1,600 | ~200 | ~12.5 |
| direct | ~600 | ~60 | ~10.0 |

Actual numbers depend on your user base. If conversion rates are 0% across channels, suspect the join condition on `started_at`. If a channel is missing, suspect NULL acquisition_channel values in `users`.

---

### Caveats

1. **SSO users with NULL email** are included in the cohort. If acme-corp users can sign up via SSO, they may slip through the email filter. Add an `organisation_domain` column to `users` if available.
2. **Users who trialled multiple times in Q1** are reduced to their earliest trial. Users with a second trial close to March 31 and a conversion in April within 14 days are correctly included.
3. **Users who paid before trialling** are excluded by `paid.started_at > trial_started_at`. If your product allows that workflow, this query undercounts conversions.
4. **14-day window is inclusive** — day 14 is included (`<= 14 days`). Confirm this matches the business definition.

---

## Criteria

- [x] PASS: Skill decomposes the question into precise definitions before writing SQL — Step 1 is explicitly mandatory ("MANDATORY before writing any SQL"), requiring metric, window, granularity, filters, and comparison baseline to be stated before any SQL is written. Met.
- [x] PASS: Metric definitions are written as SQL comments at the top of the query — Step 2 requires metric definitions as SQL comments at the top, including inclusion and exclusion criteria and time window. The format is shown with a concrete example. Met.
- [x] PASS: Query uses CTEs over subqueries — Step 4 is titled "Query Architecture (CTEs over subqueries)"; the CTE rules section states "CTEs over subqueries, always. Subqueries make debugging impossible." The anti-patterns list also prohibits nested subqueries. Met.
- [x] PASS: Query filters out test accounts and acme-corp domain explicitly — the skill prescribes the technique: Step 2 requires "Specify inclusion AND exclusion criteria"; Step 3 examples show `is_bot = FALSE` and `email NOT LIKE '%@example.com'`; Step 1 requires decomposing all filters. The pattern is taught; the scenario-specific field names arrive via arguments. Met.
- [x] PASS: Skill includes at least 2 sanity check queries — Step 5 mandates "Every query has at least 2 sanity checks" and the template examples cover percentage-bounds checks, NULL key checks, and row count checks. Met.
- [x] PASS: Final SELECT column names are descriptive — the anti-patterns list warns against single-letter aliases; every query example throughout the skill uses descriptive names. Step 4 CTE rules state "Final SELECT is clean — no complex logic." Met.
- [x] PASS: Data sources section documents grain of each table and known quality issues — Step 3 explicitly requires "Document the grain (what does one row represent?) for every table used" and "Note any known data quality issues." Met.
- [~] PARTIAL: Query handles multiple trial subscriptions (deduplication logic) — the anti-patterns section covers "Missing deduplication" with `DISTINCT or dedup CTE`, but this addresses event-level duplicates. The specific problem of reducing multiple subscription rows per user to one canonical row via `MIN(started_at)` or `ROW_NUMBER()` is not taught. The skill gestures at dedup without providing the entity-level pattern. Partially met: 0.5.
- [x] PASS: Output includes full documentation header, sanity checks, expected result shape, and caveats — the Output section lists all four explicitly. Met.

## Output expectations

- [x] PASS: Documentation header defines "trial user", "converted", and the 14-day window — Step 2 and Step 7 both require metric definitions as SQL comments covering inclusion/exclusion criteria and time windows. The simulated output produces these definitions in the header block. Met.
- [~] PARTIAL: Output filters Q1 by trial start, not by paid conversion date — the funnel pattern in Step 6 implicitly shows this (the cohort step defines the entry window, later steps extend it), but the skill never states the rule explicitly. A reader could filter Q1 on `paid.started_at` and silently exclude valid conversions. The simulated output applies the correct filter (`trial.started_at` in the cohort CTE) but the skill does not prescribe this explicitly enough to guarantee it. Partially met: 0.5.
- [x] PASS: Both filters (`is_test_account` and acme-corp domain) visible at the cohort-defining stage — Step 2 requires exclusion criteria in the metric definitions block; Step 3 requires data quality notes. Both filters appear in `trial_cohort`, the first CTE. Met.
- [x] PASS: CTEs named for what they compute — Step 4 states "CTE names describe what the data IS, not what it does." The simulated output uses `trial_cohort`, `converted_users`, `channel_metrics`. Met.
- [x] PASS: Final SELECT groups by acquisition_channel, reports count and rate with descriptive column names — the simulated output produces `trial_users`, `converted_within_14d`, `conversion_rate_pct`. Met.
- [~] PARTIAL: Deduplicates to one trial per user (earliest in Q1) before joining — anti-patterns section covers generic dedup but not the entity-level `GROUP BY user_id` with `MIN(started_at)` pattern specifically. The simulated output applies it correctly using `MIN(s.started_at)` with `GROUP BY user_id`, but the skill does not prescribe this pattern; it must be inferred. Partially met: 0.5.
- [x] PASS: At least 2 sanity checks including rate in [0,100] and non-NULL acquisition_channel — Step 5 templates include both a percentage-bounds check and a NULL keys check. The simulated output includes four sanity checks covering all required cases. Met.
- [x] PASS: Documents grain of `users` (one per user) and `subscriptions` (multiple per user possible) — Step 3 requires grain documentation for every table; the simulated output documents both tables in the data sources table. Met.
- [~] PARTIAL: Addresses edge cases — churn/re-subscribe, paid-before-trial, overlapping windows — Step 7 includes a "KNOWN LIMITATIONS" section in the documentation template, but the skill does not enumerate these specific edge cases. The simulated output addresses paid-before-trial and multiple-trial scenarios in caveats, but the skill only provides the slot, not the content prompts. Partially met: 0.5.
- [x] PASS: Includes expected result shape with approximate row count and conversion rate range — the Output section requires "Expected result shape (columns, approximate row count, sample values)." The simulated output includes a table with 4 rows and approximate percentages. Met.

## Notes

The skill is well-structured and would reliably produce correct output for most queries. The two recurring gaps stem from the same underlying issue: entity-level deduplication (reducing a one-to-many join to one canonical row per user) is not a taught pattern. The skill covers event-level `DISTINCT` in the anti-patterns section, but the `GROUP BY user_id` with `MIN(started_at)` or `ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY started_at)` pattern — needed whenever a dimension table has a one-to-many relationship with a fact table — is absent. Adding this as a named pattern in Step 6 ("Entity Deduplication") would close both the Criteria and Output expectations gaps.

The cohort-filter gap is the subtler risk. The skill teaches funnel analysis correctly in its examples but never states the principle explicitly: for cohort analysis, filter membership on the entry event's date, not the outcome event's date. One rule added to Step 1 ("for time-bounded cohorts, define membership by the event that establishes inclusion — not the event you are measuring") would make this unambiguous and prevent a common analytical error.

Everything else is well-covered. The mandatory decomposition step, metric definitions as comments, CTE architecture, sanity check templates, and documentation structure are all prescribed clearly and would reliably produce correct, well-documented output.
