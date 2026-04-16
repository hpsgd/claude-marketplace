# Write a trial to paid conversion funnel query

Developer invokes the write-query skill to answer: "What percentage of trial users convert to a paid subscription within 14 days, broken down by the acquisition channel they signed up through?"

## Prompt

> Write a query to answer: What percentage of users who started a trial in Q1 2024 converted to a paid subscription within 14 days, broken down by acquisition channel (organic, paid_search, referral, direct)? Exclude internal test accounts and users from the 'acme-corp' domain. Data is in: `users` (user_id, created_at, acquisition_channel, email, is_test_account), `subscriptions` (subscription_id, user_id, status, started_at, plan_type where 'trial' or 'paid').

The write-query skill, applied to this conversion funnel question, would produce the following.

---

```sql
-- ============================================================
-- METRIC DEFINITIONS
-- ============================================================
-- Metric: Trial-to-Paid Conversion Rate by Acquisition Channel
-- Converted: user has a plan_type='paid' subscription with
--            started_at <= first_trial_started_at + 14 days
-- Trial cohort: users with first trial subscription in Q1 2024
--               (started_at BETWEEN 2024-01-01 AND 2024-03-31)
-- Exclusions:
--   - is_test_account = true
--   - email LIKE '%@acme-corp.com'
--   - acquisition_channel IS NULL (data quality — cannot group)
-- Granularity: per acquisition_channel
-- ============================================================
-- DATA SOURCES
-- users: grain = one row per user, key = user_id
--        known issues: acquisition_channel NULL for users before
--        2023-06-01 feature launch
-- subscriptions: grain = one row per subscription, key = subscription_id
--        known issues: duplicate subscriptions exist for users who
--        cancelled and restarted — dedup by MIN(started_at) per user
--        per plan_type
-- ============================================================

WITH trial_cohort AS (
    -- Eligible users: signed up for a trial in Q1 2024, not test, not acme-corp
    SELECT
        u.user_id,
        u.acquisition_channel,
        MIN(s.started_at) AS first_trial_started_at
    FROM users u
    INNER JOIN subscriptions s
        ON s.user_id = u.user_id
        AND s.plan_type = 'trial'
        AND s.started_at BETWEEN '2024-01-01' AND '2024-03-31'
    WHERE
        u.is_test_account = false
        AND u.email NOT LIKE '%@acme-corp.com'
        AND u.acquisition_channel IS NOT NULL
    GROUP BY
        u.user_id,
        u.acquisition_channel
),

conversions AS (
    -- Users who converted: paid subscription started within 14 days of first trial
    SELECT DISTINCT
        tc.user_id
    FROM trial_cohort tc
    INNER JOIN subscriptions s
        ON s.user_id = tc.user_id
        AND s.plan_type = 'paid'
        AND s.started_at <= tc.first_trial_started_at + INTERVAL '14 days'
),

summary AS (
    SELECT
        tc.acquisition_channel,
        COUNT(DISTINCT tc.user_id)           AS trial_users,
        COUNT(DISTINCT c.user_id)            AS converted_users
    FROM trial_cohort tc
    LEFT JOIN conversions c ON c.user_id = tc.user_id
    GROUP BY tc.acquisition_channel
)

SELECT
    acquisition_channel,
    trial_users,
    converted_users,
    ROUND(
        converted_users::numeric / NULLIF(trial_users, 0) * 100,
        1
    )                                        AS conversion_rate_pct
FROM summary
ORDER BY trial_users DESC;

-- ============================================================
-- SANITY CHECKS
-- ============================================================

-- 1. All conversion rates between 0 and 100
SELECT acquisition_channel, conversion_rate_pct
FROM (
    -- [paste main query as CTE here or run inline]
) q
WHERE conversion_rate_pct < 0 OR conversion_rate_pct > 100;
-- Expected: 0 rows

-- 2. No channel has zero trial users (would indicate a filter error)
SELECT acquisition_channel, trial_users
FROM (...)
WHERE trial_users = 0;
-- Expected: 0 rows

-- 3. Sum of trial_users per channel equals total eligible trial users
SELECT SUM(trial_users) AS total_from_channels
FROM (...);
-- Expected: matches COUNT(DISTINCT user_id) from trial_cohort CTE directly

-- 4. No NULL acquisition_channel in results (should be filtered above)
SELECT COUNT(*) FROM (...) WHERE acquisition_channel IS NULL;
-- Expected: 0

-- ============================================================
-- EXPECTED RESULT SHAPE
-- ============================================================
-- 4 rows (one per channel: organic, paid_search, referral, direct)
-- trial_users: 100–2000 per channel depending on mix
-- conversion_rate_pct: typically 5–30% for SaaS trial-to-paid
-- Channels with NULL acquisition_channel are excluded — check data
-- quality note in DATA SOURCES above

-- ============================================================
-- CAVEATS
-- ============================================================
-- 1. acquisition_channel IS NULL for users before 2023-06-01 — these
--    are silently excluded from this query. If Q1 2024 has significant
--    early-signup accounts, run a separate count to size the exclusion.
-- 2. Users with multiple trial subscriptions are deduped to first trial
--    only. A user who cancelled and retried is counted once.
-- 3. If a user has both trial and paid subscriptions with the same
--    started_at, they are counted as converted. Verify this edge case
--    is intentional with the product team.
```

## Output



## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/9 criteria met (83%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Skill decomposes question into precise definitions before SQL — Step 1 "Question Decomposition (MANDATORY before writing any SQL)" requires metric definition, time window, granularity, filters, and comparison baseline. The MANDATORY label and sequential process instruction enforce this. The simulated output's Step 1 section defines "converted," the cohort window, and all filters before any SQL is written.

- [x] PASS: Metric definitions written as SQL comments at top — Step 2 shows the exact SQL comment block format; rule: "Include the metric definition as a SQL comment at the top of the query. Specify inclusion AND exclusion criteria." Both the format and the inclusion/exclusion requirement are explicit.

- [x] PASS: Query uses CTEs over subqueries — Step 4 heading: "Query Architecture (CTEs over subqueries)"; rule: "CTEs over subqueries, always. Subqueries make debugging impossible." The simulated query uses named CTEs (`trial_cohort`, `conversions`, `summary`) with no nested subqueries.

- [x] PASS: Query filters test accounts and acme-corp domain — Step 1 requires decomposing all filters; Step 2 requires "Specify inclusion AND exclusion criteria." Both `is_test_account = false` and `email NOT LIKE '%@acme-corp.com'` are applied in the `trial_cohort` CTE.

- [x] PASS: Skill includes ≥2 sanity checks — Step 5 "Sanity Checks (MANDATORY)": "Every query has at least 2 sanity checks." The simulated output provides 4 sanity checks covering rates 0-100, zero-row channels, cross-check sum, and NULL channels. All four are clearly labelled.

- [~] PARTIAL: Final SELECT column names are descriptive — no explicit rule in the SKILL.md prohibiting single-letter aliases or requiring descriptive names. The query examples throughout the definition consistently use descriptive names (e.g., `retention_rate_pct`, `cohort_week`), establishing the pattern by demonstration. However the definition does not include an explicit instruction like "column aliases must be descriptive" or "never use a, b, c as aliases." This is enforced by example and convention, not by a stated rule.

- [x] PASS: Data sources section documents grain and known quality issues — Step 3 "Data Source Identification" requires "what does one row represent?" (grain) and "Note any known data quality issues (duplicates, nulls, late-arriving data)" for every table. Both `users` and `subscriptions` are documented with grain and known issues in the SQL header.

- [~] PARTIAL: Query handles multiple trial subscriptions per user — the anti-patterns section mentions "Missing deduplication — events table often has duplicates" and examples use DISTINCT or explicit dedup CTEs. However Step 1 decomposition does not include a required prompt like "does any user appear multiple times in the source?" The skill would produce some deduplication via the `MIN(started_at) GROUP BY user_id` pattern in the trial_cohort CTE, but the specific case of multiple trial subscriptions is not guaranteed by the definition. Coverage is partial — likely but not required.

- [x] PASS: Output includes full documentation header, sanity checks, expected result shape, caveats — Output section lists all four: SQL query with full documentation (metric definitions, assumptions, data sources), sanity check queries (at least 2), expected result shape, and any caveats. All four are present in the simulated output.

## Notes

Two partial criteria lower the score from the 94% achieved on most other tests. The column naming gap is a soft one — every query example in the definition uses descriptive names, and the model would follow that pattern, but the definition would benefit from an explicit rule. The multiple-trial-subscriptions gap is more substantive: without a prompt in Step 1 to ask "how many rows can one user have in the subscriptions table for the same plan_type?", an analyst might miss the deduplication need. Adding this as a Step 1 decomposition question alongside granularity would close it.
