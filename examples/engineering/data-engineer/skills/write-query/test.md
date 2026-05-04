# Test: Write a trial-to-paid conversion funnel query

Scenario: Developer invokes the write-query skill to answer: "What percentage of trial users convert to a paid subscription within 14 days, broken down by the acquisition channel they signed up through?"

## Prompt

Write a query to answer: What percentage of users who started a trial in Q1 2024 converted to a paid subscription within 14 days, broken down by acquisition channel (organic, paid_search, referral, direct)? Exclude internal test accounts and users from the 'acme-corp' domain. Data is in: `users` (user_id, created_at, acquisition_channel, email, is_test_account), `subscriptions` (subscription_id, user_id, status, started_at, plan_type where 'trial' or 'paid').

A few specifics for the response:

- Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
- Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
- For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
- When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
- Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Criteria

- [ ] PASS: Skill decomposes the question into precise definitions before writing SQL — states what "converted" means, the time window, filters, and granularity
- [ ] PASS: Metric definitions are written as SQL comments at the top of the query — including inclusion and exclusion criteria
- [ ] PASS: Query uses CTEs over subqueries — no nested subqueries
- [ ] PASS: Query filters out test accounts (`is_test_account = false`) and acme-corp domain explicitly
- [ ] PASS: Skill includes at least 2 sanity check queries — checking percentages are 0-100, row counts are reasonable, and no NULL acquisition channels in output
- [ ] PASS: Final SELECT column names are descriptive — not aliased as `a`, `b`, `c`
- [ ] PASS: Data sources section documents the grain of each table used and any known data quality issues
- [ ] PARTIAL: Query handles the case where a user has multiple trial subscriptions (deduplication logic)
- [ ] PASS: Output includes the query with full documentation header, sanity checks, expected result shape, and any caveats

## Output expectations

- [ ] PASS: Output's documentation header (SQL comments) defines "trial user" (any user with a row in `subscriptions` where `plan_type = 'trial'`), "converted" (subsequent row with `plan_type = 'paid'`), and the 14-day window (paid.started_at - trial.started_at <= 14 days)
- [ ] PASS: Output explicitly filters Q1 2024 by trial start (`started_at >= '2024-01-01' AND started_at < '2024-04-01'`) — not by paid conversion date — so Q1 cohorts are measured properly
- [ ] PASS: Output excludes test accounts via `is_test_account = false` and the acme-corp domain via `email NOT LIKE '%@acme-corp.com'` (or domain-extracted equivalent), with both filters visible at the cohort-defining stage
- [ ] PASS: Output uses CTEs (WITH clauses) named for what they compute — e.g. `trial_cohort`, `converted_users`, `final_metrics` — not nested subqueries or one giant SELECT
- [ ] PASS: Output's final SELECT groups by `acquisition_channel` and reports both the converted count and the conversion rate (percentage), with descriptive column names like `trial_users`, `converted_within_14d`, `conversion_rate_pct`
- [ ] PASS: Output handles users with multiple trial subscriptions by deduplicating to one trial row per user (e.g. earliest trial in Q1) before joining — the `users.user_id` should appear at most once in the cohort
- [ ] PASS: Output includes at least 2 sanity check queries: one verifying `conversion_rate_pct` falls in [0, 100], and one verifying every output row has a non-NULL `acquisition_channel` from the four expected values
- [ ] PASS: Output documents the grain of `users` (one row per user) and `subscriptions` (one row per subscription, multiple per user possible) and notes the dependency on `started_at` accuracy
- [ ] PARTIAL: Output addresses edge cases — users who churned then re-subscribed, users who paid before officially trialling, users with overlapping trial windows — even just to state how each is handled
- [ ] PARTIAL: Output includes an expected result shape (e.g. 4 rows, one per acquisition_channel, with conversion rates between 0% and ~25%) so the reader can sanity-check actual results against expectations
