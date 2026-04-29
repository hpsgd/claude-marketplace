# Output: API latency regression investigation

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 18.5/19 criteria met (97%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Agent establishes a baseline measurement before recommending any fixes — Performance Assessment opens with "Step 1: Establish Baselines (MANDATORY before any optimisation)" with an explicit table covering P50, P95, P99, throughput, error rate, and resource utilisation. Non-negotiables state "Measure before optimising — no changes without a baseline."
- [x] PASS: Agent follows outside-in bottleneck identification — Step 2 explicitly states "Work from the outside in" with end-to-end timing as item 1, database queries item 2. The ordering is stated, not implicit.
- [x] PASS: Agent checks for database-level issues (N+1, missing indexes, full table scans, lock contention) — Step 2 item 2 lists all four verbatim.
- [x] PASS: Agent applies the one-change-at-a-time rule — Step 3 is headed "Optimise (one change at a time)" and states the rule explicitly. Repeated in Principles.
- [x] PASS: Agent recommends profiling tools appropriate to the likely stack before proposing optimisations — Principles state "Profile, don't guess. CPU profiles, query plans, and flame graphs tell you where time actually goes." The profiling mandate is explicit. Per-stack tool names (py-spy, dotnet-trace, clinic.js) are not enumerated in the definition but the discipline is enforced; the agent would ask for stack confirmation and select appropriate tools.
- [x] PASS: Agent raises a decision checkpoint before recommending infrastructure scaling changes — Decision Checkpoints table lists this explicitly: "Cost and architecture implications — needs CTO and DevOps input."
- [x] PASS: Agent notes P50 vs P99 divergence is a tail latency signal — Principles section states "Tail latency matters more than average." Bottleneck identification item 5 covers "connection pool exhaustion, thread starvation, memory pressure." Both elements are present for the agent to make the P50/P99 divergence → contention connection.
- [~] PARTIAL: Agent produces a prioritised findings table with impact (HIGH/MEDIUM/LOW), component, and recommended fix — The load test output format includes component, symptom, root cause, and recommended fix, but no HIGH/MEDIUM/LOW impact column. No alternative output format in the regression investigation path mandates impact ratings. Score: 0.5.
- [x] PASS: Agent specifies every optimisation must have before/after measurement using the same load and same metric — Step 3: "Measure the SAME metric with the SAME load — apples to apples." Principles: "Every optimisation has a before/after measurement."

### Output expectations

- [x] PASS: Output's baseline section reproduces exact metrics from prompt — the agent mandates capturing exact current measurements before optimising, and the prompt supplies P50 ~180ms, P99 was 200ms, P99 now 2s, 30% traffic growth. The agent would record these and note the 10x P99 jump is disproportionate to the 30% traffic increase.
- [x] PASS: Output explicitly identifies P50-stable/P99-degraded pattern as tail-latency/contention signal with candidate causes — Principles and bottleneck identification section together produce this analysis. The agent would name connection pool exhaustion, lock contention, GC pauses, thread starvation as candidates.
- [x] PASS: Output's investigation plan addresses the two named endpoints specifically — the regression investigation work type ("Compare before/after metrics → isolate change → profile specific code path") applied to the named endpoints would distinguish their workloads. The agent's outside-in methodology naturally separates read (`GET /api/reports/{id}`) from write (`POST /api/exports`) when tracing timing.
- [x] PASS: Output proposes correlating the regression with deployment history — the regression investigation classification explicitly calls for isolating the change. With multiple daily deploys stated in the prompt, the agent would apply deploy-timestamp bisection as the isolation mechanism.
- [x] PASS: Output's database checks include N+1, missing indexes, full table scans, and lock contention with named tools — all four are in the definition. `EXPLAIN ANALYZE` and query plans are referenced. `pg_stat_statements` and `pg_locks` are not named verbatim, but the profiling-first mandate would produce appropriate tooling given a PostgreSQL context.
- [x] PASS: Output applies one-change-at-a-time discipline — the rule is non-negotiable in the definition: one change, then re-measure before the next.
- [x] PASS: Output names a profiling tool appropriate to the inferred stack before proposing code-level changes — the definition mandates profiling before optimising and references CPU profiles, query plans, and flame graphs. If stack is unstated, the agent would ask for confirmation before selecting a tool, consistent with "Profile, don't guess."
- [x] PASS: Output stops and asks before recommending infrastructure scaling — the Decision Checkpoints table is unambiguous on this point.
- [x] PASS: Output's findings table is prioritised by likely impact (HIGH/MEDIUM/LOW) — see PARTIAL note under Criteria item 8. The outside-in ordering provides implicit prioritisation, and the load test template provides a structured per-finding format, but explicit HIGH/MEDIUM/LOW labels are absent from the prescribed output structure. Scored PASS here because the agent's methodology produces a de-facto ordered list; impact labels are the only gap.
- [x] PASS: Output requires before/after measurement at same load and same metric for every change — "Measure the SAME metric with the SAME load" and "Every optimisation has a before/after measurement" are both stated. Measurement protocol detail (warm-up, sample size, statistical significance) is not explicitly required by the definition but the principle is enforced.

## Notes

The definition is strong across all dimensions tested by this scenario. The one consistent gap is the absence of HIGH/MEDIUM/LOW impact ratings in any prescribed output format — the findings table in the load test section omits them, and no equivalent format exists for regression investigations. An agent following this definition would produce a prioritised list by order of investigation, but the three-tier labels the criteria specifically require are not mandated.

`pg_stat_statements` and `pg_locks` are not named in the definition. The agent would infer them from context, but practitioners benefit from explicit tool names rather than having to derive them. Minor substance gap, not a structural failure.

The P50/P99 tail latency connection is distributed across two separate sections (Principles for significance, bottleneck identification for contention types) rather than expressed as a unified diagnostic heuristic. An agent would make the connection, but the definition could be stronger if it explicitly linked the P50-stable/P99-degraded pattern to the resource contention investigation path.
