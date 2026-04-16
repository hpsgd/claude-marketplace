# Test: Write a trial-to-paid conversion funnel query

Scenario: Developer invokes the write-query skill to answer: "What percentage of trial users convert to a paid subscription within 14 days, broken down by the acquisition channel they signed up through?"

## Prompt

Write a query to answer: What percentage of users who started a trial in Q1 2024 converted to a paid subscription within 14 days, broken down by acquisition channel (organic, paid_search, referral, direct)? Exclude internal test accounts and users from the 'acme-corp' domain. Data is in: `users` (user_id, created_at, acquisition_channel, email, is_test_account), `subscriptions` (subscription_id, user_id, status, started_at, plan_type where 'trial' or 'paid').

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
