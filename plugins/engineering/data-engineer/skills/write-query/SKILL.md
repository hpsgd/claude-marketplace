---
name: write-query
description: Write a SQL query, dbt model, or analytics query to answer a business question.
argument-hint: "[business question to answer, or data to extract]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Write a query to answer: $ARGUMENTS

## Process (sequential — do not skip steps)

### Step 1: Question Decomposition (MANDATORY before writing any SQL)

Before writing SQL, decompose the business question into precise, unambiguous definitions:

1. **What is being measured?** — the metric
2. **Over what time range?** — the window
3. **With what granularity?** — daily, weekly, monthly, per-user, per-cohort
4. **With what filters?** — exclusions, segments, conditions
5. **Compared to what?** — baseline, previous period, control group

**Examples of vague vs precise:**

| Vague question | Precise question |
|---|---|
| "How many active users?" | "How many users performed at least 1 qualifying action in the last 7 days, excluding bots and internal accounts?" |
| "What's our conversion rate?" | "What percentage of users who viewed the pricing page in Q1 2024 started a trial within 7 days?" |
| "Which features are popular?" | "Which features were used by >10% of monthly active users in March 2024, ranked by usage frequency?" |

**Rule:** If the question is ambiguous, STOP and clarify. A precise question answered correctly is infinitely more valuable than a vague question answered quickly.

### Step 2: Metric Definitions

Every metric in the query MUST be defined before it is computed:

```sql
-- METRIC DEFINITIONS:
-- Active User: A user who performed at least 1 of [page_view, report_created, export_completed]
--              in the measurement window, excluding:
--              - Users with is_bot = true
--              - Users with email domain in ('example.com', 'test.com')
--              - Users created < 24 hours ago (exclude same-day signups)
--
-- Measurement Window: 7 calendar days ending at midnight UTC of the report date
--
-- Conversion: A user who completed 'subscription_started' within 14 days of their first 'pricing_page_viewed'
```

**Rules:**
- Define the metric BEFORE writing the query — not after
- Include the metric definition as a SQL comment at the top of the query
- Specify inclusion AND exclusion criteria
- Specify the time window and timezone
- Specify what "unique" means (per user? per session? per device?)

### Step 3: Data Source Identification

Before joining tables, understand the data:

```sql
-- DATA SOURCES:
-- events: Raw event stream, one row per event occurrence
--   - Grain: one row per event
--   - Key: event_id (unique)
--   - Partitioned by: event_date
--   - Known issues: duplicate events possible (dedup by event_id)
--
-- users: User dimension table, one row per user
--   - Grain: one row per user
--   - Key: user_id (unique)
--   - Updated: daily snapshot
--   - Known issues: email may be null for SSO users
```

**Rules:**
- Document the grain (what does one row represent?) for every table used
- Note any known data quality issues (duplicates, nulls, late-arriving data)
- Check for partitioning — always filter on the partition key first (cost and performance)
- Check for data freshness — when was the table last updated?

### Step 4: Query Architecture (CTEs over subqueries)

Structure every query using CTEs for readability:

```sql
-- Business question: What is the 7-day retention rate by signup cohort (weekly)?
-- Metric: Retention = user performed at least 1 qualifying action in days 7-13 after signup

WITH
-- Step 1: Define the user cohort
cohort AS (
    SELECT
        user_id,
        DATE_TRUNC('week', created_at) AS cohort_week,
        created_at AS signup_date
    FROM users
    WHERE created_at >= '2024-01-01'
      AND is_bot = FALSE
      AND email NOT LIKE '%@example.com'
),

-- Step 2: Find qualifying actions in the retention window
retention_actions AS (
    SELECT DISTINCT
        e.user_id,
        c.cohort_week
    FROM events e
    INNER JOIN cohort c ON e.user_id = c.user_id
    WHERE e.event_name IN ('page_view', 'report_created', 'export_completed')
      AND e.timestamp >= c.signup_date + INTERVAL '7 days'
      AND e.timestamp < c.signup_date + INTERVAL '14 days'
),

-- Step 3: Calculate retention per cohort
cohort_sizes AS (
    SELECT
        cohort_week,
        COUNT(DISTINCT user_id) AS cohort_size
    FROM cohort
    GROUP BY cohort_week
),

retained AS (
    SELECT
        cohort_week,
        COUNT(DISTINCT user_id) AS retained_users
    FROM retention_actions
    GROUP BY cohort_week
)

-- Step 4: Final output
SELECT
    cs.cohort_week,
    cs.cohort_size,
    COALESCE(r.retained_users, 0) AS retained_users,
    ROUND(COALESCE(r.retained_users, 0)::DECIMAL / cs.cohort_size * 100, 1) AS retention_rate_pct
FROM cohort_sizes cs
LEFT JOIN retained r ON cs.cohort_week = r.cohort_week
ORDER BY cs.cohort_week;
```

**CTE rules:**
- Each CTE does ONE thing — filter, transform, or aggregate
- CTE names describe what the data IS, not what it does: `active_users` not `get_active_users`
- Comment each CTE with its purpose
- Final SELECT is clean — no complex logic, just assembling the result
- CTEs over subqueries, always. Subqueries make debugging impossible

### Step 5: Sanity Checks (MANDATORY)

Every query result must be sanity-checked. Include these checks in your output:

```sql
-- SANITY CHECK 1: Total should roughly equal sum of parts
-- Expected: SUM(retained_users) across all cohorts ≈ total retained users
SELECT SUM(retained_users) FROM retention_results;

-- SANITY CHECK 2: Percentages should be 0-100
-- Flag any retention_rate_pct > 100 or < 0
SELECT * FROM retention_results WHERE retention_rate_pct > 100 OR retention_rate_pct < 0;

-- SANITY CHECK 3: No future cohorts
SELECT * FROM retention_results WHERE cohort_week > CURRENT_DATE;

-- SANITY CHECK 4: Row count is reasonable
-- Expected: ~52 rows (one per week for 1 year)
SELECT COUNT(*) FROM retention_results;

-- SANITY CHECK 5: No NULL keys
SELECT COUNT(*) FROM retention_results WHERE cohort_week IS NULL;
```

**Rules:**
- Every query has at least 2 sanity checks
- Totals equal sum of parts (within rounding tolerance)
- Percentages are between 0 and 100
- Row counts are in expected range
- No unexpected NULLs in key columns
- Date ranges are within expected bounds
- Results match known benchmarks (if available)

### Step 6: Common Analysis Patterns

#### Cohort Analysis

```sql
-- Cohort = group of users who share a characteristic (signup week, first action, geography)
-- Measure behaviour of each cohort over time relative to their cohort date
WITH cohort AS (
    SELECT user_id, DATE_TRUNC('week', MIN(event_date)) AS cohort_week
    FROM events
    WHERE event_name = 'signup'
    GROUP BY user_id
),
activity AS (
    SELECT
        c.cohort_week,
        DATEDIFF('week', c.cohort_week, e.event_date) AS weeks_since_signup,
        COUNT(DISTINCT e.user_id) AS active_users
    FROM events e
    JOIN cohort c ON e.user_id = c.user_id
    GROUP BY 1, 2
)
SELECT * FROM activity ORDER BY cohort_week, weeks_since_signup;
```

#### Funnel Analysis

```sql
-- Each step filters from the previous step's users
-- ORDER matters: step 1 -> step 2 -> step 3
WITH step1 AS (
    SELECT DISTINCT user_id
    FROM events WHERE event_name = 'pricing_page_viewed'
      AND event_date BETWEEN '2024-01-01' AND '2024-03-31'
),
step2 AS (
    SELECT DISTINCT e.user_id
    FROM events e JOIN step1 s ON e.user_id = s.user_id
    WHERE e.event_name = 'trial_started'
      AND e.event_date BETWEEN '2024-01-01' AND '2024-04-14'  -- 14-day window
),
step3 AS (
    SELECT DISTINCT e.user_id
    FROM events e JOIN step2 s ON e.user_id = s.user_id
    WHERE e.event_name = 'subscription_started'
      AND e.event_date BETWEEN '2024-01-01' AND '2024-04-28'  -- 28-day window
)
SELECT
    'Viewed Pricing' AS step, COUNT(*) AS users FROM step1
UNION ALL
SELECT 'Started Trial', COUNT(*) FROM step2
UNION ALL
SELECT 'Subscribed', COUNT(*) FROM step3;
```

#### Period-over-Period Comparison

```sql
WITH current_period AS (
    SELECT COUNT(DISTINCT user_id) AS current_users
    FROM events
    WHERE event_date BETWEEN CURRENT_DATE - INTERVAL '7 days' AND CURRENT_DATE
),
previous_period AS (
    SELECT COUNT(DISTINCT user_id) AS previous_users
    FROM events
    WHERE event_date BETWEEN CURRENT_DATE - INTERVAL '14 days' AND CURRENT_DATE - INTERVAL '7 days'
)
SELECT
    c.current_users,
    p.previous_users,
    ROUND((c.current_users - p.previous_users)::DECIMAL / p.previous_users * 100, 1) AS change_pct
FROM current_period c, previous_period p;
```

#### Window Functions for Rankings and Running Totals

```sql
SELECT
    user_id,
    event_date,
    event_count,
    SUM(event_count) OVER (PARTITION BY user_id ORDER BY event_date) AS cumulative_events,
    RANK() OVER (ORDER BY event_count DESC) AS rank_by_activity,
    LAG(event_count) OVER (PARTITION BY user_id ORDER BY event_date) AS prev_day_count
FROM daily_user_events;
```

### Step 7: Query Documentation

Every query includes these comments:

```sql
-- ============================================================
-- BUSINESS QUESTION: [The original question, verbatim]
-- AUTHOR: [name]
-- DATE: [date]
-- ============================================================
--
-- METRIC DEFINITIONS:
-- [Precise definitions of every metric computed]
--
-- ASSUMPTIONS:
-- 1. [Assumption and impact if wrong]
-- 2. [Assumption and impact if wrong]
--
-- DATA SOURCES:
-- [Table name, grain, freshness, known issues]
--
-- KNOWN LIMITATIONS:
-- [What this query does NOT account for]
-- ============================================================
```

## Anti-Patterns (NEVER do these)

- **Undefined metrics** — "active users" without specifying qualifying actions, time window, and exclusions
- **Subqueries instead of CTEs** — deeply nested subqueries are unreadable and undebuggable
- **SELECT \*** — list columns explicitly. Schema changes silently break `SELECT *`
- **Missing NULL handling** — `COUNT(*)` vs `COUNT(column)` behave differently with NULLs. Be explicit
- **No partition filter** — querying a partitioned table without filtering on the partition key = full table scan
- **Implicit type coercion** — string/integer comparison, implicit date parsing. Cast explicitly
- **No sanity checks** — a query that returns results is not necessarily correct. Verify the results make sense
- **Over-precision** — reporting `12.3456789% conversion rate`. Round to meaningful precision (1 decimal for percentages)
- **Missing deduplication** — events table often has duplicates. `DISTINCT` or dedup CTE before aggregating
- **Commenting the obvious** — `-- Select the user_id` adds nothing. Comment the WHY, not the WHAT

## Output

Deliver:
1. The SQL query with full documentation (metric definitions, assumptions, data sources)
2. Sanity check queries (at least 2)
3. Expected result shape (columns, approximate row count, sample values)
4. Any caveats or limitations of the analysis
