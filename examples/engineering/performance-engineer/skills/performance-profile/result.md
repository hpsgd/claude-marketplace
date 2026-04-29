# Output: Profile the report generation endpoint

**Verdict:** PARTIAL
**Score:** 15.5/18 criteria met (86%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill establishes a baseline with exact measurements before recommending anything — records p50, p95, p99, throughput, error rate, and the conditions (load, data volume) — met. Step 1 mandates all six metrics and explicitly requires recording exact conditions.
- [x] PASS: Skill breaks down end-to-end timing across components (server processing, database queries, external API calls, serialisation) before identifying the bottleneck — met. Step 2 provides the waterfall table with all named segments.
- [x] PASS: Skill systematically checks for N+1 queries — counts queries per request, checks for sequential DB calls in a loop — met. Step 3 explicitly requires query count per request (< 10 threshold) and provides grep commands for ORM patterns.
- [x] PASS: Skill checks whether external API calls to datasource connectors are parallel or sequential — flags sequential calls to independent services as a HIGH finding — met. Step 4's "Parallel calls?" row flags sequential calls to independent services and names the fix (`Promise.all`, `Task.WhenAll`, `asyncio.gather`).
- [x] PASS: Skill applies the one-change-at-a-time rule — does not recommend fixing N+1 queries and parallelising API calls simultaneously — met. Step 9 states "One optimisation at a time — measure after each change" and the Anti-Patterns section reinforces this.
- [x] PASS: Skill recommends a profiling tool appropriate to the server stack before proposing code changes — met. Step 5 lists tools per stack (Node.js, Python, .NET); Step 3 provides query-logging and `EXPLAIN ANALYZE` guidance.
- [x] PASS: Every recommendation specifies the expected improvement with before/after measurement using the same load — met. The output format mandates "Expected improvement: [ms saved, % reduction]" per recommendation and Step 9 requires measuring with the same metric and same load.
- [~] PARTIAL: Skill references USE Method or RED Method for systematic resource analysis — partially met per rubric type. Step 6 explicitly covers both USE and RED with descriptions and links. Substantively full coverage; scored 0.5 per PARTIAL rubric type.
- [x] PASS: Output includes baseline table, timing breakdown, bottlenecks table with impact/effort/priority, and ordered recommendations — met. The Output Format section includes all four required sections, and the bottlenecks table includes Impact, Effort, and Priority columns.

### Output expectations

- [x] PASS: Output's baseline table reproduces the prompt's exact metrics — p50=420ms, p95=3.2s, p99=8s — and records the conditions — met. The skill instructs capturing exact conditions and the baseline table format accepts these values directly from input.
- [x] PASS: Output's timing breakdown decomposes the request into named segments — server processing, database queries, external datasource API calls, calculation, serialisation — with measurement targets — met. Step 2 waterfall table covers all named segments.
- [x] PASS: Output's investigation explicitly counts queries per request to confirm or refute the N+1 hypothesis — met. Step 3 sets a < 10 threshold and instructs enabling query logging to count; applying this to 20 datasources surfaces the pattern.
- [x] PASS: Output checks whether external datasource API calls are sequential or parallel and flags sequential calls to independent services as HIGH-impact — met. Step 4 addresses this directly.
- [x] PASS: Output applies the one-change-at-a-time rule and orders recommendations sequentially — fix N+1 first, measure; then parallelise external calls, measure — never both at once — met. Step 9 and Anti-Patterns enforce this.
- [ ] FAIL: Output names a profiling tool appropriate to the inferred stack and asks for stack confirmation if not stated, rather than guessing — not met. Step 5 lists tools per stack but the skill does not instruct the agent to ask for stack confirmation when the stack is unspecified. The scenario provides no stack; the skill would enumerate all stacks without prompting.
- [x] PASS: Output ties each recommendation to a quantified expected improvement with a before/after measurement plan — met. The output format explicitly requires "Expected improvement: [ms saved, % reduction]" per recommendation and Next Steps reinforce the measure-after pattern.
- [x] PASS: Output's bottlenecks table includes impact, effort, and priority columns — met. The output format shows all three columns.
- [ ] FAIL: Output explicitly addresses the new multi-datasource feature added 3 weeks ago as the prime suspect, recommending a code/diff review of that change as part of the investigation — not met. The skill has no step instructing the agent to flag recent feature additions as prime suspects or recommend a git diff review of recent changes. It is a generic profiling skill with no scenario-sensitivity of this kind.
- [~] PARTIAL: Output references the USE method or RED method for systematic resource analysis — partially met per rubric type. Step 6 covers both methods fully. Scored 0.5 per PARTIAL rubric type.

## Notes

The skill is well-structured and handles the core profiling workflow. Two gaps against the output expectations:

1. No stack-confirmation prompt. When the stack is unknown (as in this scenario), the skill lists all profilers rather than asking which stack applies. Adding a conditional — "if the stack is not specified, ask before recommending a profiler" — would close this.

2. No recency-aware investigation step. The scenario explicitly flags a feature added 3 weeks ago as a prime suspect. The skill has no instruction to treat recent changes as an investigation starting point or to recommend reviewing the relevant diff. This is a common and high-value pattern in real performance regressions that the skill misses.

The USE/RED PARTIAL scores are per rubric type (both criteria are marked PARTIAL), though the skill's coverage of both methods is substantively complete with descriptions, links, and application guidance.
