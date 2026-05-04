# Write Query

Scenario: Developer invokes the write-query skill to answer: "What percentage of trial users convert to a paid subscription within 14 days, broken down by the acquisition channel they signed up through?"

## Prompt

> Write a query to answer: What percentage of users who started a trial in Q1 2024 converted to a paid subscription within 14 days, broken down by acquisition channel (organic, paid_search, referral, direct)? Exclude internal test accounts and users from the 'acme-corp' domain. Data is in: `users` (user_id, created_at, acquisition_channel, email, is_test_account), `subscriptions` (subscription_id, user_id, status, started_at, plan_type where 'trial' or 'paid').
> 
> A few specifics for the response:
> 
> - Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
> - Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
> - For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
> - When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
> - Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

# Query: Trial-to-Paid Conversion Rate by Channel (Q1 2024)

## Step 1: Question Decomposition

**Precise question components:**

| Component | Definition |
|---|---|
| **What is measured** | Conversion rate (%) = users with paid subscription within 14 days ÷ total trial starters × 100 |
| **Time range** | Trial started: Q1 2024 (Jan 1 — Mar 31, 2024); Conversion window: +14 days from trial start |
| **Granularity** | Per acquisition channel (organic, paid_search, referral, direct) |
| **Filters (inclusion)** | Users with `is_test_account = FALSE` AND email NOT LIKE `'%@acme-corp%'` |
| **Baseline** | All trial-starting users in Q1 2024 (post-filters) |

---

## Step 2: Metric Definitions

```sql
-- Trial Starter: A user with a subscription record where:
--   - plan_type = 'trial'
--   - started_at between 2024-01-01 and 2024-03-31
--   - User: is_test_account = FALSE
--   - User: email does NOT match '%@acme-corp%'
--   - Deduplicated per user (first trial in period if multiple)
--
-- Converted to Paid: Same user has a subscription where:
--   - plan_type = 'paid'
--   - started_at >= trial_started_at AND 
--     started_at <= trial_started_at + 14 days (inclusive)
--
-- Conversion Rate: 
--   (count distinct users with paid conversion) / 
--   (count distinct trial starter users) × 100
--   grouped by acquisition_channel
```

---

## Step 3: Data Source Identification

| Table | Grain | Key | Freshness | Known Issues |
|---|---|---|---|---|
| `users` | One row per user | `user_id` (unique) | Current | Email may be NULL for SSO users |
| `subscriptions` | One row per subscription | `subscription_id` (unique) | Current | Users can have multiple subscriptions; plan_type is 'trial' or 'paid' |

---

## Step 4: Query

```sql
-- ============================================================
-- BUSINESS QUESTION: What percentage of users who started a 
-- trial in Q1 2024 converted to a paid subscription within 
-- 14 days, broken down by acquisition channel? Exclude internal 
-- test accounts and users from the 'acme-corp' domain.
--
-- AUTHOR: Claude Code
-- DATE: 2026-05-04
-- DATABASE: PostgreSQL (note: adjust interval/date syntax for other DBs)
-- ============================================================
--
-- METRIC DEFINITIONS:
-- Trial Starter: User with subscription.plan_type='trial' 
--   where started_at in [2024-01-01, 2024-03-31),
--   is_test_account=FALSE, email NOT LIKE '%@acme-corp%'
--
-- Converted to Paid: Same user has subscription.plan_type='paid'
--   with started_at within 14 days of first trial start
--
-- Conversion Rate: (converted users / trial starters) × 100
--   grouped by acquisition_channel
--
-- ASSUMPTIONS:
-- 1. acquisition_channel is immutable per user (set at account creation)
-- 2. Multiple trials/subscriptions per user are possible;
--    conversion measured against first trial in Q1
-- 3. "Within 14 days" is inclusive: trial_date + 14 days
-- 4. A paid subscription = conversion, regardless of status
--    or duration (not checking if subscription is still active)
-- 5. Test accounts and acme-corp are known internal exclusions
--
-- KNOWN LIMITATIONS:
-- - Does not measure actual usage or engagement during trial
-- - "Converted" = started paid subscription, not completed payment
-- - Paid subscription may be cancelled; no filtering for active status
-- - Does not distinguish trial plan types if multiple exist
-- ============================================================

WITH trial_starters_first AS (
    -- Identify unique trial-starting users in Q1 2024
    -- One row per user, earliest trial date in period
    SELECT
        u.user_id,
        u.acquisition_channel,
        MIN(s.started_at) AS first_trial_start
    FROM users u
    INNER JOIN subscriptions s ON u.user_id = s.user_id
    WHERE u.is_test_account = FALSE
      AND u.email NOT LIKE '%@acme-corp%'
      AND s.plan_type = 'trial'
      AND s.started_at >= '2024-01-01'
      AND s.started_at < '2024-04-01'
    GROUP BY u.user_id, u.acquisition_channel
),

conversion_check AS (
    -- For each trial starter, check if any paid subscription 
    -- exists within 14 days of their first trial
    SELECT
        tf.user_id,
        tf.acquisition_channel,
        MAX(CASE 
            WHEN s.subscription_id IS NOT NULL THEN 1
            ELSE 0
        END) AS converted_to_paid
    FROM trial_starters_first tf
    LEFT JOIN subscriptions s 
      ON tf.user_id = s.user_id
      AND s.plan_type = 'paid'
      AND s.started_at >= tf.first_trial_start
      AND s.started_at <= tf.first_trial_start + INTERVAL '14 days'
    GROUP BY tf.user_id, tf.acquisition_channel
)

-- Final output: conversion rates by channel
SELECT
    COALESCE(acquisition_channel, 'Unknown') AS acquisition_channel,
    COUNT(*) AS total_trial_starters,
    SUM(converted_to_paid) AS converted_users,
    COUNT(*) - SUM(converted_to_paid) AS not_converted_users,
    ROUND(
        SUM(converted_to_paid)::DECIMAL / NULLIF(COUNT(*), 0) * 100, 
        2
    ) AS conversion_rate_pct
FROM conversion_check
GROUP BY acquisition_channel
ORDER BY conversion_rate_pct DESC NULLS LAST, total_trial_starters DESC;
```

---

## Step 5: Sanity Checks

```sql
-- SANITY CHECK 1: Total row count
-- Expected: 4-5 rows (4 channels + possibly 1 NULL row)
SELECT COUNT(*) AS channel_count
FROM (
    SELECT DISTINCT acquisition_channel FROM trial_starters_first
) AS channels;

-- SANITY CHECK 2: Conversion rates within 0-100%
-- Expected: 0 rows (flag if any exist)
WITH rates AS (
    SELECT
        acquisition_channel,
        SUM(converted_to_paid)::DECIMAL / NULLIF(COUNT(*), 0) * 100 AS conv_pct
    FROM conversion_check
    GROUP BY acquisition_channel
)
SELECT * FROM rates 
WHERE conv_pct < 0 OR conv_pct > 100;

-- SANITY CHECK 3: Converted users ≤ total users per channel
-- Expected: 0 rows (flag if any exist — indicates JOIN logic error)
WITH summary AS (
    SELECT
        acquisition_channel,
        COUNT(*) AS total,
        SUM(converted_to_paid) AS converted
    FROM conversion_check
    GROUP BY acquisition_channel
)
SELECT * FROM summary
WHERE converted > total;

-- SANITY CHECK 4: No unexpected NULLs in keys
-- Expected: count matches total unique users
SELECT 
    COUNT(DISTINCT user_id) AS total_users,
    COUNT(DISTINCT acquisition_channel) AS channels_represented,
    COUNT(*) FILTER (WHERE acquisition_channel IS NULL) AS null_channels
FROM trial_starters_first;

-- SANITY CHECK 5: Verify trial dates are in Q1 2024
-- Expected: MIN >= 2024-01-01, MAX < 2024-04-01
SELECT
    MIN(first_trial_start) AS earliest_trial,
    MAX(first_trial_start) AS latest_trial,
    CASE 
        WHEN MIN(first_trial_start) < '2024-01-01' THEN 'ERROR: Before Q1'
        WHEN MAX(first_trial_start) >= '2024-04-01' THEN 'ERROR: After Q1'
        ELSE 'OK'
    END AS date_validation
FROM trial_starters_first;
```

---

## Expected Result Shape

| Column | Type | Example | Notes |
|---|---|---|---|
| `acquisition_channel` | string | `'organic'` | One of: organic, paid_search, referral, direct, Unknown |
| `total_trial_starters` | integer | `1,247` | Count of unique users per channel |
| `converted_users` | integer | `312` | Users with paid subscription in 14-day window |
| `not_converted_users` | integer | `935` | Total starters minus converted |
| `conversion_rate_pct` | decimal | `25.02` | Conversion % (0-100, 2 decimal places) |

**Approximate row count:** 4–5 rows (one per channel, possibly one for NULL)

**Sample output:**
```
acquisition_channel  | total_trial_starters | converted_users | conversion_rate_pct
---------------------|----------------------|-----------------|--------------------
paid_search          | 1,247                | 312             | 25.02
organic              | 856                  | 178             | 20.79
direct               | 543                  | 97              | 17.86
referral             | 421                  | 61              | 14.49
```

---

## Caveats and Limitations

1. **Subscription status not checked** — includes paid subscriptions regardless of whether they remain active. If you need "still paid as of today," add a `WHERE status = 'active'` or similar filter to the LEFT JOIN.

2. **Multiple trials per user** — conversion is measured from the *first* trial in Q1. If a user starts a second trial on March 30 and converts on April 5, they won't count as converted (April 5 is outside 14 days of first trial). Clarify if you want "any trial in Q1" instead.

3. **No payment validation** — a paid subscription row exists, but it doesn't confirm payment completed or card was charged.

4. **Acquisition channel immutability** — assumes channel doesn't change per user. If users can re-sign up or have their channel updated, results may be misleading.

5. **Database syntax** — Query uses PostgreSQL (`INTERVAL '14 days'`, `NULLIF`, `COALESCE`). Adjust for BigQuery, Snowflake, etc.:
   - BigQuery: `DATE_ADD(first_trial_start, INTERVAL 14 DAY)`
   - Snowflake: `DATEADD(day, 14, first_trial_start)`

---

## Next Steps

Run the main query first. Then run sanity checks 1–5 in order to verify:
- Row counts are reasonable
- Rates are 0-100%
- No logic errors in the JOIN
- Date ranges are correct

If sanity checks fail, the issue is likely in the LEFT JOIN logic — verify the `subscription` table has expected plan_type values and started_at dates.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/17.5 (97%) |
| Evaluated | 2026-05-04 |
| Target duration | 65857 ms |
| Target cost | $0.1342 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill decomposes the question into precise definitions before writing SQL — states what "converted" means, the time window, filters, and granularity | PASS | Step 1 (Question Decomposition) explicitly defines: 'Conversion rate (%) = users with paid subscription within 14 days ÷ total trial starters × 100', time range 'Q1 2024 (Jan 1 — Mar 31, 2024); Conversion window: +14 days from trial start', granularity 'Per acquisition channel', and filters 'is_test_account = FALSE AND email NOT LIKE \'%@acme-corp%\''. |
| c2 | Metric definitions are written as SQL comments at the top of the query — including inclusion and exclusion criteria | PASS | The query header block contains '-- METRIC DEFINITIONS:' with explicit definitions for Trial Starter (plan_type='trial', date range, is_test_account=FALSE, email filter), Converted to Paid (plan_type='paid' within 14 days), and Conversion Rate formula — all as SQL block comments. |
| c3 | Query uses CTEs over subqueries — no nested subqueries | PASS | The query uses two named CTEs: `trial_starters_first` and `conversion_check`, with no nested subqueries present anywhere in the SQL. |
| c4 | Query filters out test accounts (`is_test_account = false`) and acme-corp domain explicitly | PASS | In `trial_starters_first`: 'WHERE u.is_test_account = FALSE AND u.email NOT LIKE \'%@acme-corp%\''. Both filters appear at the cohort-defining stage. |
| c5 | Skill includes at least 2 sanity check queries — checking percentages are 0-100, row counts are reasonable, and no NULL acquisition channels in output | PASS | Step 5 contains 5 sanity check queries: SANITY CHECK 1 (total row count), SANITY CHECK 2 (rates within 0-100%), SANITY CHECK 3 (converted ≤ total per channel), SANITY CHECK 4 (NULL checks including acquisition_channel IS NULL count), SANITY CHECK 5 (date range validation). |
| c6 | Final SELECT column names are descriptive — not aliased as `a`, `b`, `c` | PASS | Final SELECT uses: `acquisition_channel`, `total_trial_starters`, `converted_users`, `not_converted_users`, `conversion_rate_pct` — all fully descriptive. |
| c7 | Data sources section documents the grain of each table used and any known data quality issues | PASS | Step 3 table documents `users` grain as 'One row per user' with known issue 'Email may be NULL for SSO users', and `subscriptions` grain as 'One row per subscription' with known issue 'Users can have multiple subscriptions; plan_type is \'trial\' or \'paid\''. |
| c8 | Query handles the case where a user has multiple trial subscriptions (deduplication logic) | PARTIAL | CTE `trial_starters_first` uses `MIN(s.started_at) AS first_trial_start` grouped by `u.user_id, u.acquisition_channel`, ensuring each user appears exactly once with their earliest Q1 trial. Ceiling is PARTIAL per rubric. |
| c9 | Output includes the query with full documentation header, sanity checks, expected result shape, and any caveats | PASS | All four components present: documentation header (BUSINESS QUESTION, AUTHOR, DATE, DATABASE, METRIC DEFINITIONS, ASSUMPTIONS, KNOWN LIMITATIONS), Step 5 sanity checks (5 queries), 'Expected Result Shape' section with table and sample output, and 'Caveats and Limitations' section with 5 items. |
| c10 | Output's documentation header (SQL comments) defines "trial user" (any user with a row in `subscriptions` where `plan_type = 'trial'`), "converted" (subsequent row with `plan_type = 'paid'`), and the 14-day window (paid.started_at - trial.started_at <= 14 days) | PASS | Header comments define: Trial Starter as 'User with subscription.plan_type=\'trial\'...', Converted to Paid as 'Same user has subscription.plan_type=\'paid\' with started_at within 14 days of first trial start'. All three definitional elements are present. |
| c11 | Output explicitly filters Q1 2024 by trial start (`started_at >= '2024-01-01' AND started_at < '2024-04-01'`) — not by paid conversion date — so Q1 cohorts are measured properly | PASS | In `trial_starters_first` WHERE clause: `AND s.plan_type = 'trial' AND s.started_at >= '2024-01-01' AND s.started_at < '2024-04-01'`. Filter applies to the trial subscription rows only, not the paid conversion date. |
| c12 | Output excludes test accounts via `is_test_account = false` and the acme-corp domain via `email NOT LIKE '%@acme-corp.com'` (or domain-extracted equivalent), with both filters visible at the cohort-defining stage | PASS | Both filters appear in the cohort-defining CTE `trial_starters_first`: `u.is_test_account = FALSE` and `u.email NOT LIKE '%@acme-corp%'`. The pattern `%@acme-corp%` is a domain-extracted equivalent that correctly targets the domain. |
| c13 | Output uses CTEs (WITH clauses) named for what they compute — e.g. `trial_cohort`, `converted_users`, `final_metrics` — not nested subqueries or one giant SELECT | PASS | Two CTEs with descriptive names: `trial_starters_first` (identifies trial-starting users and their first trial date) and `conversion_check` (checks for paid conversion per user). No nested subqueries. |
| c14 | Output's final SELECT groups by `acquisition_channel` and reports both the converted count and the conversion rate (percentage), with descriptive column names like `trial_users`, `converted_within_14d`, `conversion_rate_pct` | PASS | Final SELECT: `GROUP BY acquisition_channel` with columns `total_trial_starters`, `converted_users`, `not_converted_users`, `conversion_rate_pct`. Both converted count and rate are present with descriptive names. |
| c15 | Output handles users with multiple trial subscriptions by deduplicating to one trial row per user (e.g. earliest trial in Q1) before joining — the `users.user_id` should appear at most once in the cohort | PASS | `trial_starters_first` uses `MIN(s.started_at) AS first_trial_start` with `GROUP BY u.user_id, u.acquisition_channel`, guaranteeing each `user_id` appears at most once. The comment explicitly notes 'One row per user, earliest trial date in period'. |
| c16 | Output includes at least 2 sanity check queries: one verifying `conversion_rate_pct` falls in [0, 100], and one verifying every output row has a non-NULL `acquisition_channel` from the four expected values | PASS | SANITY CHECK 2 verifies rates are within 0-100% ('WHERE conv_pct < 0 OR conv_pct > 100'). SANITY CHECK 4 includes 'COUNT(*) FILTER (WHERE acquisition_channel IS NULL) AS null_channels' to check for NULL channels. |
| c17 | Output documents the grain of `users` (one row per user) and `subscriptions` (one row per subscription, multiple per user possible) and notes the dependency on `started_at` accuracy | PARTIAL | Step 3 documents grain for both tables correctly ('One row per user' and 'One row per subscription'). However, the dependency on `started_at` accuracy is not explicitly noted — neither the data sources table nor the caveats section calls out that incorrect `started_at` values would silently corrupt cohort membership or conversion windows. |
| c18 | Output addresses edge cases — users who churned then re-subscribed, users who paid before officially trialling, users with overlapping trial windows — even just to state how each is handled | PARTIAL | The Caveats section addresses overlapping trial windows ('Multiple trials per user — conversion is measured from the first trial') and subscription status ('Subscription status not checked'). However, 'users who paid before officially trialling' (paid subscription predating trial) is not addressed, and the churn/re-subscribe scenario is not explicitly called out. Ceiling is PARTIAL per rubric. |
| c19 | Output includes an expected result shape (e.g. 4 rows, one per acquisition_channel, with conversion rates between 0% and ~25%) so the reader can sanity-check actual results against expectations | PARTIAL | 'Expected Result Shape' section states 'Approximate row count: 4–5 rows (one per channel, possibly one for NULL)' and includes a sample output table with 4 channels showing conversion rates ranging from 14.49% to 25.02%. Ceiling is PARTIAL per rubric. |

### Notes

This is a high-quality output that covers nearly every criterion. The query is well-structured with two clearly named CTEs, a comprehensive SQL header block, five sanity checks, and a detailed caveats section. The main gaps are minor: c17 misses an explicit note about `started_at` accuracy as a data dependency risk (the grain documentation is complete but the accuracy caveat is absent); c18 doesn't address users who paid before trialling; and c19 is capped at PARTIAL by the rubric ceiling. The acme-corp filter uses `'%@acme-corp%'` rather than the stricter `'%@acme-corp.com'` — functionally more permissive but defensively correct. The deduplication logic in `trial_starters_first` using `MIN(started_at)` is clean and correct. Overall, this output would be production-ready with only minor documentation additions needed.
