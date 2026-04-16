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
