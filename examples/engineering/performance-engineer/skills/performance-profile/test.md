# Test: Profile the report generation endpoint

Scenario: Developer invokes the performance-profile skill against the report generation endpoint `/api/reports/generate`. P99 has climbed to 8 seconds and the endpoint is suspected to have N+1 query issues with the new multi-datasource feature added last sprint.

## Prompt

Profile `POST /api/reports/generate`. Current measurements: p50=420ms, p95=3.2s, p99=8s. This endpoint fetches data from up to 20 configured datasources, runs calculations, and builds a report. The multi-datasource feature was added 3 weeks ago. Team suspects N+1 queries — each datasource might be triggering individual DB calls. Also want to check if external API calls to datasource connectors are sequential when they could be parallel.

## Criteria

- [ ] PASS: Skill establishes a baseline with exact measurements before recommending anything — records p50, p95, p99, throughput, error rate, and the conditions (load, data volume)
- [ ] PASS: Skill breaks down end-to-end timing across components (server processing, database queries, external API calls, serialisation) before identifying the bottleneck
- [ ] PASS: Skill systematically checks for N+1 queries — counts queries per request, checks for sequential DB calls in a loop
- [ ] PASS: Skill checks whether external API calls to datasource connectors are parallel or sequential — flags sequential calls to independent services as a HIGH finding
- [ ] PASS: Skill applies the one-change-at-a-time rule — does not recommend fixing N+1 queries and parallelising API calls simultaneously
- [ ] PASS: Skill recommends a profiling tool appropriate to the server stack before proposing code changes
- [ ] PASS: Every recommendation specifies the expected improvement with before/after measurement using the same load
- [ ] PARTIAL: Skill references USE Method (Utilisation, Saturation, Errors) or RED Method for systematic resource analysis
- [ ] PASS: Output includes baseline table, timing breakdown, bottlenecks table with impact/effort/priority, and ordered recommendations

## Output expectations

- [ ] PASS: Output's baseline table reproduces the prompt's exact metrics — p50=420ms, p95=3.2s, p99=8s — and records the conditions (load, data volume, datasource count up to 20)
- [ ] PASS: Output's timing breakdown decomposes the request into named segments — server processing, database queries, external datasource API calls, calculation, serialisation — with current contributions or measurement targets per segment
- [ ] PASS: Output's investigation explicitly counts queries per request to confirm or refute the N+1 hypothesis — e.g. "20 datasources should be 1-3 queries; if N+1 is present, expect 20+ queries"
- [ ] PASS: Output checks whether external datasource API calls are sequential or parallel and flags sequential calls to independent services as a HIGH-impact finding given up to 20 datasources
- [ ] PASS: Output applies the one-change-at-a-time rule and orders recommendations sequentially — fix N+1 first, measure; then parallelise external calls, measure — never both at once
- [ ] PASS: Output names a profiling tool appropriate to the inferred stack (e.g. async-profiler, dotnet-trace, py-spy, Node clinic) and asks for stack confirmation if not stated, rather than guessing
- [ ] PASS: Output ties each recommendation to a quantified expected improvement (e.g. "fixing N+1 should reduce DB time from 3s to ~200ms based on 20x query reduction") with a before/after measurement plan
- [ ] PASS: Output's bottlenecks table includes impact, effort, and priority columns — not just a list of issues — so the team can sequence work
- [ ] PASS: Output explicitly addresses the new multi-datasource feature added 3 weeks ago as the prime suspect, recommending a code/diff review of that change as part of the investigation
- [ ] PARTIAL: Output references the USE method (Utilisation, Saturation, Errors) or RED method (Rate, Errors, Duration) for systematic resource analysis
