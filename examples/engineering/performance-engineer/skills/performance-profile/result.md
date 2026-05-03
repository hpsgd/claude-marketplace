# Performance Profile

Scenario: Developer invokes the performance-profile skill against the report generation endpoint `/api/reports/generate`. P99 has climbed to 8 seconds and the endpoint is suspected to have N+1 query issues with the new multi-datasource feature added last sprint.

## Prompt

> Profile `POST /api/reports/generate`. Current measurements: p50=420ms, p95=3.2s, p99=8s. This endpoint fetches data from up to 20 configured datasources, runs calculations, and builds a report. The multi-datasource feature was added 3 weeks ago. Team suspects N+1 queries — each datasource might be triggering individual DB calls. Also want to check if external API calls to datasource connectors are sequential when they could be parallel.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

The work directory appears to be a fresh repo. Since you have specific measurements and suspects for this endpoint, I'll create a systematic profile document with investigation steps. Can you share the code for the `POST /api/reports/generate` endpoint so I can:

1. **Confirm the suspected N+1 queries** — count database queries when fetching 20 datasources
2. **Identify sequential vs parallel API calls** — trace external connector calls
3. **Pinpoint exact bottlenecks** — measure component breakdown

In the meantime, here's the profiling plan:

## Performance Profile: POST /api/reports/generate

**Baseline (your measurements)**
| Metric | Value | Target | Status |
|---|---|---|---|
| p50 response | 420ms | < 300ms | ❌ FAIL |
| p95 response | 3.2s | < 500ms | ❌ FAIL |
| p99 response | 8s | < 1s | ❌ FAIL |

**Tail latency concern:** p99 is 19× worse than p50 — classic symptom of sequential blocking or connection pool exhaustion under concurrent load.

## Likely Bottlenecks (based on your suspects)

| # | Problem | Hypothesis | Impact | Priority |
|---|---|---|---|---|
| 1 | N+1 queries | Each of 20 datasources triggers separate DB query for config + data | ~200-400ms (can be 4-8× improvement) | **HIGH** |
| 2 | Sequential API calls | Datasource connectors fetched one-at-a-time instead of parallel | ~100-200ms per datasource (can be 15-20× improvement with 20 sources) | **HIGH** |
| 3 | Missing connection pool | External API calls use fresh connections instead of pooled | Cascading latency under concurrent requests | **MEDIUM** |

**Share the endpoint code and I'll:**
- Count actual queries (enable SQL logging)
- Trace API call timing (add instrumentation)
- Measure each component's contribution to the 8s p99
- Recommend specific fixes with expected improvements

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 6.0/17.0 (35%) |
| Evaluated | 2026-04-30 |
| Target duration | 27040 ms |
| Target cost | $0.0417 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill establishes a baseline with exact measurements before recommending anything — records p50, p95, p99, throughput, error rate, and the conditions (load, data volume) | PARTIAL | Baseline table records p50=420ms, p95=3.2s, p99=8s with Target and Status columns. However, throughput, error rate, and conditions (load level, data volume, datasource count) are absent from the table. |
| c2 | Skill breaks down end-to-end timing across components (server processing, database queries, external API calls, serialisation) before identifying the bottleneck | FAIL | No component-level timing breakdown exists in the output. The output jumps directly from the baseline table to a 'Likely Bottlenecks' table without any decomposition of where time is currently spent per segment. |
| c3 | Skill systematically checks for N+1 queries — counts queries per request, checks for sequential DB calls in a loop | PARTIAL | Output states it will 'Count actual queries (enable SQL logging)' and hypothesises 'Each of 20 datasources triggers separate DB query for config + data', but no actual systematic check or query count is performed — it asks for code first. |
| c4 | Skill checks whether external API calls to datasource connectors are parallel or sequential — flags sequential calls to independent services as a HIGH finding | PASS | Bottlenecks table item #2: 'Sequential API calls — Datasource connectors fetched one-at-a-time instead of parallel' with Priority column value '**HIGH**'. |
| c5 | Skill applies the one-change-at-a-time rule — does not recommend fixing N+1 queries and parallelising API calls simultaneously | FAIL | Both N+1 queries and sequential API calls are listed side-by-side in the bottlenecks table with no sequencing instruction, no 'fix one then measure' rule, and no explicit statement that they should not be addressed simultaneously. |
| c6 | Skill recommends a profiling tool appropriate to the server stack before proposing code changes | FAIL | No profiling tool is named anywhere in the output. The output asks for code but does not mention async-profiler, py-spy, dotnet-trace, Node clinic, or any stack-appropriate tool. |
| c7 | Every recommendation specifies the expected improvement with before/after measurement using the same load | PARTIAL | Impact column includes rough estimates: '~200-400ms (can be 4-8× improvement)' and '~100-200ms per datasource (can be 15-20× improvement with 20 sources)'. However, no before/after measurement plan using the same load conditions is specified. |
| c8 | Skill references USE Method (Utilisation, Saturation, Errors) or RED Method for systematic resource analysis | FAIL | Neither USE Method nor RED Method is mentioned anywhere in the output. |
| c9 | Output includes baseline table, timing breakdown, bottlenecks table with impact/effort/priority, and ordered recommendations | PARTIAL | Baseline table present ✓. Bottlenecks table present ✓ (has Impact and Priority but lacks an Effort column). Timing breakdown absent ✗. Ordered recommendations with measure-between-steps absent ✗. |
| c10 | Output's baseline table reproduces the prompt's exact metrics — p50=420ms, p95=3.2s, p99=8s — and records the conditions (load, data volume, datasource count up to 20) | PARTIAL | Baseline table rows show p50=420ms, p95=3.2s, p99=8s matching the prompt exactly. Conditions (load level, data volume, datasource count) are not recorded in the table. |
| c11 | Output's timing breakdown decomposes the request into named segments — server processing, database queries, external datasource API calls, calculation, serialisation — with current contributions or measurement targets per segment | FAIL | No such timing breakdown exists. The output contains a baseline table and a bottlenecks table, but no per-segment decomposition with current or target timing contributions. |
| c12 | Output's investigation explicitly counts queries per request to confirm or refute the N+1 hypothesis — e.g. '20 datasources should be 1-3 queries; if N+1 is present, expect 20+ queries' | PARTIAL | Output says 'Each of 20 datasources triggers separate DB query for config + data' (implying 40+ queries) and plans to 'Count actual queries (enable SQL logging)', but never states the expected baseline (e.g., '1-3 queries') or the N+1 threshold explicitly. |
| c13 | Output checks whether external datasource API calls are sequential or parallel and flags sequential calls to independent services as a HIGH-impact finding given up to 20 datasources | PASS | Bottlenecks table item #2: 'Sequential API calls — Datasource connectors fetched one-at-a-time instead of parallel — ~100-200ms per datasource (can be 15-20× improvement with 20 sources)' with Priority: **HIGH**. |
| c14 | Output applies the one-change-at-a-time rule and orders recommendations sequentially — fix N+1 first, measure; then parallelise external calls, measure — never both at once | FAIL | Both fixes appear side-by-side in the bottlenecks table with no explicit sequencing, no 'fix N+1 first, measure' instruction, and no prohibition on addressing both simultaneously. |
| c15 | Output names a profiling tool appropriate to the inferred stack (e.g. async-profiler, dotnet-trace, py-spy, Node clinic) and asks for stack confirmation if not stated, rather than guessing | FAIL | No profiling tool is named. The output asks for code to be shared but does not ask for stack confirmation or suggest any profiler. |
| c16 | Output ties each recommendation to a quantified expected improvement (e.g. 'fixing N+1 should reduce DB time from 3s to ~200ms based on 20x query reduction') with a before/after measurement plan | PARTIAL | Impact estimates given ('4-8× improvement', '15-20× improvement with 20 sources') but not tied to specific before/after timings (e.g., 'from 3s to ~200ms') and no measurement plan with matching load conditions is provided. |
| c17 | Output's bottlenecks table includes impact, effort, and priority columns — not just a list of issues — so the team can sequence work | PARTIAL | Bottlenecks table columns are: #, Problem, Hypothesis, Impact, Priority. An Effort column is absent, so the team cannot assess sequencing by effort. |
| c18 | Output explicitly addresses the new multi-datasource feature added 3 weeks ago as the prime suspect, recommending a code/diff review of that change as part of the investigation | FAIL | The output never mentions the 3-week-old feature addition as the prime suspect and does not recommend reviewing the diff or commit history from that change. The 20-datasource context is referenced but not tied back to the specific recent feature. |
| c19 | Output references the USE method (Utilisation, Saturation, Errors) or RED method (Rate, Errors, Duration) for systematic resource analysis | FAIL | Neither USE nor RED method is mentioned anywhere in the output. |

### Notes

The captured output is a lightweight, conversational profiling plan that correctly identifies the two main suspects (N+1 queries and sequential API calls) and flags them as HIGH priority, and reproduces the exact p50/p95/p99 numbers. However it fails most structural criteria: there is no component timing breakdown, no profiling tool recommendation, no one-change-at-a-time ordering, no mention of the 3-week-old feature as prime suspect requiring a diff review, no USE/RED method reference, and the bottlenecks table is missing an Effort column. The output is essentially a skeleton that asks for source code before proceeding rather than producing the full structured profile document the skill was expected to deliver. The two PASS results (c4, c13) are for correctly flagging sequential API calls as HIGH — the strongest part of the response.
