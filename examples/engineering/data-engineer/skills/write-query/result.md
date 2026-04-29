# Result: Write a trial-to-paid conversion funnel query

**Verdict:** PARTIAL
**Score:** 17/19 criteria met (89%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill decomposes the question into precise definitions before writing SQL — Step 1 is explicitly mandatory ("MANDATORY before writing any SQL"), requiring metric, window, granularity, filters, and comparison baseline to be stated before any SQL is written. Met.
- [x] PASS: Metric definitions are written as SQL comments at the top of the query — Step 2 requires metric definitions as SQL comments at the top, including inclusion and exclusion criteria and time window. The format is shown with a concrete example. Met.
- [x] PASS: Query uses CTEs over subqueries — Step 4 is titled "Query Architecture (CTEs over subqueries)"; the CTE rules section states "CTEs over subqueries, always. Subqueries make debugging impossible." The anti-patterns list also prohibits nested subqueries. Met.
- [x] PASS: Query filters out test accounts and acme-corp domain explicitly — the skill prescribes the technique: Step 2 requires "Specify inclusion AND exclusion criteria"; Step 3 examples show `is_bot = FALSE` and `email NOT LIKE '%@example.com'`; Step 1 requires decomposing all filters. The pattern is taught; the scenario-specific field names arrive via arguments. Met.
- [x] PASS: Skill includes at least 2 sanity check queries — Step 5 mandates "Every query has at least 2 sanity checks" and the template examples cover percentage-bounds checks, NULL key checks, and row count checks. Met.
- [x] PASS: Final SELECT column names are descriptive — the anti-patterns list warns against "Over-precision" in reporting and every query example throughout the skill uses descriptive names. Step 4 CTE rules state "Final SELECT is clean — no complex logic." The skill establishes the pattern consistently by demonstration. Met.
- [x] PASS: Data sources section documents grain of each table and known quality issues — Step 3 explicitly requires "Document the grain (what does one row represent?) for every table used" and "Note any known data quality issues (duplicates, nulls, late-arriving data)." Met.
- [~] PARTIAL: Query handles multiple trial subscriptions (deduplication logic) — the anti-patterns section covers "Missing deduplication" with `DISTINCT or dedup CTE`, but this addresses event-level duplicates. The specific problem of reducing multiple rows per user (e.g. multiple trial subscriptions for the same user) to one row using `MIN(started_at)` or `ROW_NUMBER()` is not taught. Partially met: 0.5.
- [x] PASS: Output includes full documentation header, sanity checks, expected result shape, and caveats — the Output section lists all four explicitly: "The SQL query with full documentation", "Sanity check queries (at least 2)", "Expected result shape", "Any caveats or limitations." Met.

### Output expectations

- [x] PASS: Documentation header defines "trial user", "converted", and the 14-day window — Step 2 and Step 7 both require metric definitions as SQL comments covering inclusion/exclusion criteria and time windows. The skill would produce these definitions. Met.
- [~] PARTIAL: Output filters Q1 by trial start, not by paid conversion date — the funnel pattern in Step 6 implicitly shows this (step1 defines the cohort window, steps 2/3 extend it to later windows), but the skill never states the rule explicitly: cohort membership is defined by the entry event's date, not the outcome event's date. A reader following the skill could filter Q1 on `paid.started_at` and silently exclude valid conversions. Partially met: 0.5.
- [x] PASS: Both filters visible at the cohort-defining stage — Step 2 requires exclusion criteria in the metric definitions block; Step 3 requires data quality notes. The skill prescribes documenting and applying exclusions at the data-sourcing stage, not buried in a later CTE. Met.
- [x] PASS: CTEs named for what they compute — Step 4 states "CTE names describe what the data IS, not what it does: `active_users` not `get_active_users`." Multiple named examples reinforce this. Met.
- [x] PASS: Final SELECT groups by acquisition_channel, reports count and rate with descriptive column names — Step 4 requires a clean final SELECT; anti-patterns prohibit single-letter aliases; the skill's examples consistently use names like `retention_rate_pct`, `cohort_size`. Met.
- [~] PARTIAL: Deduplicates to one trial per user (earliest in Q1) before joining — anti-patterns section covers generic dedup (`DISTINCT or dedup CTE`), but the specific pattern of reducing a one-to-many user-subscription relationship to one row per user via `MIN(started_at)` or `ROW_NUMBER()` is not described. This is a different problem from event-level dedup and is not taught by the skill. Partially met: 0.5.
- [x] PASS: At least 2 sanity checks including rate in [0,100] and non-NULL acquisition_channel — Step 5 templates include both a percentage-bounds check (`WHERE retention_rate_pct > 100 OR retention_rate_pct < 0`) and a NULL keys check (`WHERE cohort_week IS NULL`). These map directly to the required checks. Met.
- [x] PASS: Documents grain of users (one per user) and subscriptions (multiple per user possible) — Step 3 requires grain documentation for every table used; the subscriptions table's one-to-many nature would be captured there. Met.
- [~] PARTIAL: Addresses edge cases — churn/re-subscribe, paid-before-trial, overlapping windows — Step 7 includes a "KNOWN LIMITATIONS" section in the documentation template, but the skill does not enumerate these specific edge cases or prompt the analyst to consider them. The template slot exists; the content is not prescribed. Partially met: 0.5.
- [x] PASS: Includes expected result shape with approximate row count and conversion rate range — the Output section step 3 requires "Expected result shape (columns, approximate row count, sample values)." This directly covers the criterion. Met.

## Notes

The skill is strong and well-structured. The two recurring gaps both come from the same underlying issue: the skill teaches deduplication generically (event-level `DISTINCT`) but does not address entity-level deduplication — reducing a one-to-many join to one canonical row per user. The `subscriptions` table has exactly this shape (multiple plan rows per user), and the skill does not teach the `MIN()`/`ROW_NUMBER()` over partition pattern that handles it. Adding this as a named pattern in Step 4 or Step 6 would close both the Criteria and Output expectations gaps.

The cohort-filtering gap (Output expectation #2) is the subtler risk. The skill teaches funnel analysis but never states the principle that separates correct cohort analysis from common errors: filter cohort membership on the cohort-entry event's date, not the outcome event's date. A single rule added to Step 1 ("for time-bounded cohorts, filter on the event that defines membership — not the event you're measuring") would make this explicit.

Everything else is well-covered. The mandatory decomposition step, metric definitions as comments, CTE architecture, sanity check templates, and documentation structure are all prescribed clearly and would reliably produce correct output.
