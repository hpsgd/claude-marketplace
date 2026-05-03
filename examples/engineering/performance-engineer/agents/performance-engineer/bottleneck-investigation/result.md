# Bottleneck Investigation

Scenario: User reports that API response times have degraded significantly under load, with P99 climbing from 200ms to 2s, and asks the performance engineer to investigate.

## Prompt

> Our API is getting slow under load. Two weeks ago P99 was around 200ms. Now it's hitting 2 seconds. P50 is still okay at about 180ms — it's the tail latency that's the problem. We're seeing this mostly on `GET /api/reports/{id}` and `POST /api/exports`. Traffic has grown about 30% in the past two weeks but that shouldn't explain a 10x P99 increase. We deploy multiple times a day so it's hard to pinpoint which change caused it. Can you investigate?
> 
> Do not ask for clarification — proceed using the information provided. State your assumptions where relevant.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll create a targeted investigation plan for your specific performance issue. Based on the pattern (10x P99 increase, stable P50, 30% traffic growth, specific endpoints affected), here's where to focus:

## Diagnostic Checklist for Your Issue

**Assumptions:**
- You have APM/monitoring in place (Datadog, New Relic, etc.) or can access application/database logs
- Deployments include both application code and database schema changes
- `GET /api/reports/{id}` and `POST /api/exports` likely involve database queries or external API calls

### Priority 1: Query Performance (Most Likely)
The fact that **only two endpoints** are affected and **P50 is stable** while **P99 spikes** suggests a query that performs differently under load or with larger datasets:

```bash
# Check your slow query logs (adjust for your database)
# MySQL/PostgreSQL
tail -f /var/log/mysql/slow.log  # MySQL
grep "duration:" /var/log/postgresql/postgresql.log | grep "duration: [0-9]{4,}"  # PostgreSQL

# Look for:
# - Queries on /api/reports/{id} or exports that take > 500ms
# - Query count > 10 per request (N+1 indicator)
# - Increasing execution time over the past 2 weeks
```

**Check for these specific problems:**

1. **Missing indexes** — this is the #1 cause of tail latency spikes at scale
   ```bash
   # Run EXPLAIN ANALYZE on slow queries
   EXPLAIN ANALYZE SELECT * FROM reports WHERE id = ?;
   EXPLAIN ANALYZE SELECT * FROM exports WHERE ...;
   
   # Look for "Seq Scan" on tables > 10K rows — that's your problem
   # Add indexes on frequently filtered columns
   ```

2. **N+1 query patterns** — especially in reports endpoint
   ```bash
   # Count queries per request in your application logs
   # Typical: < 10 queries per request
   # If /api/reports/{id} does 50+ queries, you have an N+1 problem
   
   # Look for loops like:
   # for report in reports:
   #     details = db.query(f"SELECT * FROM details WHERE report_id = {report.id}")
   ```

3. **Data volume increase** — queries that were fast with 10K rows are slow with 1M rows
   ```bash
   # Check table row counts over time
   SELECT table_name, row_count FROM information_schema.tables 
   WHERE table_schema = 'your_db';
   
   # If key tables grew 30%+ in the past 2 weeks, query plans may have changed
   ```

### Priority 2: Resource Saturation

**Database connection pool exhaustion** — typical symptom: p99 fine on low load, p99 spikes under concurrent load
```bash
# Check connection pool usage (depends on your framework/DB driver)
# For connection pooling, look for:
# - Max pool size vs concurrent requests
# - Wait time for available connection
# - Queue depth increasing under load

# Example: if max_connections = 100 and you have 150 concurrent requests,
# 50 requests queue up and hit timeout
```

**Lock contention** — if POST /api/exports writes to shared tables
```bash
# PostgreSQL
SELECT * FROM pg_locks WHERE NOT granted;  # Waiting locks

# MySQL
SHOW PROCESSLIST;  # Look for "Locked" state
SHOW ENGINE INNODB STATUS;  # Lock wait info
```

### Priority 3: Recent Deploys

Since you deploy multiple times daily, check recent changes:

```bash
# Git log for the past 2 weeks on affected files
git log --since="2 weeks ago" --oneline -- "reports/*" "exports/*" "api/*"

# Look for:
# - New queries or query changes
# - Removed indexes
# - Changed WHERE clauses or JOINs
# - New async operations (if causing queue buildup)

# Run git diff on each commit to review changes:
git show <commit-hash> -- database/migrations/
```

### Priority 4: Load Test the Affected Endpoints

To isolate the problem, **reproduce it under load**:

```bash
# Apache Bench / wrk to simulate the 30% traffic increase
# Current: measure baseline
ab -n 1000 -c 50 "https://your-api.com/api/reports/123"
ab -n 100 -c 10 -p exports.json -T application/json "https://your-api.com/api/exports"

# Then test with 30% higher concurrency (c flag)
ab -n 1000 -c 65 "https://your-api.com/api/reports/123"
ab -n 100 -c 13 -p exports.json -T application/json "https://your-api.com/api/exports"

# Compare response time distribution — does p99 spike?
```

## Root Cause Hypotheses (Ranked by Likelihood)

| Hypothesis | Confidence | Time to Check | Next Step |
|---|---|---|---|
| **Missing index added in recent deploy** | Very High | 5 min | Check slow query logs for `Seq Scan` on large tables |
| **N+1 query in reports endpoint** | High | 10 min | Count queries per request; check ORM for eager loading |
| **Connection pool saturation** | High | 5 min | Check pool metrics in APM; compare max pool size to concurrent requests |
| **Query plan change with data growth** | High | 15 min | Compare query plan from 2 weeks ago vs now with EXPLAIN ANALYZE |
| **Garbage collection pauses** (if JVM/Go) | Medium | 10 min | Enable GC logging; check heap usage during load test |
| **Slow external API added** | Medium | 5 min | Check for new API calls in /api/exports; measure their latency |
| **Dataset explosion in related table** | Medium | 5 min | Count rows in tables joined by reports/{id} query |

## Immediate Actions (Next 30 Minutes)

1. **Pull the slow query log** for the past 2 weeks, filter for queries > 500ms on reports/exports tables
2. **Run EXPLAIN ANALYZE** on the top 3 slowest queries — look for Seq Scan on large tables
3. **Count queries per request** in application logs — if > 20, you have an N+1 problem
4. **Check the last 5 deployments** for schema changes, new queries, or removed indexes
5. **Load test locally** with 30% higher concurrency — does p99 spike?

If steps 1–5 don't surface the issue, I can help with:
- Detailed query plan analysis
- Load test design to isolate the bottleneck
- Code review of the affected endpoints

**What data can you share?** (This will accelerate the diagnosis):
- Slow query logs from the past 2 weeks
- Recent deployment commits touching `/reports` or `/exports` endpoints
- Current query plans (EXPLAIN ANALYZE output) for those endpoints
- APM metrics showing resource utilization over the past 2 weeks

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 7.0/18.5 (38%) |
| Evaluated | 2026-05-02 |
| Target duration | 48123 ms |
| Target cost | $0.0839 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent establishes a baseline measurement before recommending any fixes — records the exact current metrics (P50, P95, P99, throughput, error rate) | FAIL | The output jumps immediately into a 'Diagnostic Checklist' and 'Priority 1: Query Performance' without establishing a baseline measurement step. The load test section includes 'measure baseline' as a sub-step, but this is not a pre-fix baseline capture — it is part of a load test exercise described under Priority 4. |
| c2 | Agent follows the outside-in bottleneck identification: end-to-end timing breakdown before diving into database or code | FAIL | The output's first priority is 'Query Performance (Most Likely)' — diving directly into database-level checks (slow query logs, EXPLAIN ANALYZE, N+1 patterns). There is no prior step that breaks down latency across the stack (network, load balancer, application layer, database, external calls) to locate where time is being spent before narrowing to the database. |
| c3 | Agent checks for database-level issues: N+1 queries, missing indexes, full table scans, and lock contention | PASS | All four are explicitly covered: 'N+1 query patterns' with example code; 'Missing indexes — this is the #1 cause'; full table scans via 'Look for Seq Scan on tables > 10K rows'; and 'Lock contention — if POST /api/exports writes to shared tables' with pg_locks query. |
| c4 | Agent applies the one-change-at-a-time rule — does not recommend changing multiple things simultaneously | FAIL | 'Immediate Actions (Next 30 Minutes)' lists five parallel actions (pull slow query log, run EXPLAIN ANALYZE, count queries per request, check last 5 deployments, load test locally) with no sequencing or measurement gate between them. The output does not apply a one-change-at-a-time discipline. |
| c5 | Agent recommends profiling tools appropriate to the likely stack before proposing optimisations | PARTIAL | The output recommends APM tools (Datadog, New Relic in assumptions), EXPLAIN ANALYZE, pg_locks, and ab/wrk for load testing. These are general database/load tools. No application-level profilers (py-spy, async-profiler, dotnet-trace, Node clinic) are mentioned, and the stack is never asked about. Some tool recommendations exist but not stack-appropriate profiling tools before code-level investigation. |
| c6 | Agent raises a decision checkpoint before recommending infrastructure scaling changes (cost and architecture implications) | FAIL | The output mentions connection pool size as something to check but makes no explicit infrastructure scaling recommendations and raises no decision checkpoint framing cost or architecture implications before any such recommendation. The criterion expects an explicit pause/ask, which is absent. |
| c7 | Agent notes that P50 vs P99 divergence is a tail latency signal — suggests investigating resource contention and connection pool exhaustion under concurrency rather than average-case code paths | PASS | 'P50 is stable while P99 spikes suggests a query that performs differently under load.' 'Database connection pool exhaustion — typical symptom: p99 fine on low load, p99 spikes under concurrent load' is explicitly listed as Priority 2, along with lock contention and GC pauses in the hypothesis table. |
| c8 | Agent produces a prioritised findings table with impact (HIGH/MEDIUM/LOW), component, and recommended fix | PARTIAL | The 'Root Cause Hypotheses' table is present and prioritized, with columns Hypothesis, Confidence (Very High/High/Medium), Time to Check, and Next Step. However it uses 'Confidence' instead of 'Impact (HIGH/MEDIUM/LOW)' and lacks a 'Component' column. Partially satisfies the criterion. |
| c9 | Agent specifies that every optimisation must have a before/after measurement using the same load and same metric | FAIL | No such requirement is stated anywhere in the output. The 'Immediate Actions' section lists changes to make without mandating before/after measurement for each. The load test section measures a baseline once but does not apply the discipline to every subsequent optimisation. |
| c10 | Output's baseline section reproduces the exact metrics from the prompt — P50 ~180ms (still healthy), P99 was 200ms two weeks ago, P99 now 2s, 30% traffic growth — and notes the 10x P99 jump is disproportionate to traffic | PARTIAL | The opening sentence captures '10x P99 increase, stable P50, 30% traffic growth' but there is no dedicated baseline section. The exact values (P50 ~180ms, P99 200ms historically, P99 2s now) are not explicitly listed in one place; P50's numeric value and the historical P99 figure are only implicit. The disproportionality to traffic is noted ('that shouldn't explain a 10x P99 increase'). |
| c11 | Output explicitly identifies the P50-stable / P99-degraded pattern as a tail-latency / contention signal rather than an across-the-board slowdown, and lists candidate causes (connection pool exhaustion, lock contention, GC pauses, cold cache, queueing under load) | PASS | 'P50 is stable while P99 spikes' is called out as the key pattern. The hypothesis table lists connection pool exhaustion (High), lock contention (High), and GC pauses (Medium). Queueing under load is implicit in connection pool exhaustion description. Cold cache is the only candidate cause not mentioned. |
| c12 | Output's investigation plan addresses the two named endpoints (`GET /api/reports/{id}` and `POST /api/exports`) specifically — looking at their distinct workloads (read vs write, sync vs async) | PARTIAL | Both endpoints are named and addressed: reports for N+1 and slow queries, exports for lock contention ('if POST /api/exports writes to shared tables'). The load test section tests both separately. However, the read-vs-write and sync-vs-async distinction is not analyzed; async processing implications for exports (queue buildup, background jobs) are not investigated. |
| c13 | Output proposes correlating the regression with the deployment history — using deploy timestamps to bisect the change set, since 'we deploy multiple times a day' makes single-commit blame infeasible | PARTIAL | 'Priority 3: Recent Deploys' includes `git log --since="2 weeks ago"` and 'check the last 5 deployments for schema changes.' The output acknowledges deploy history investigation but does not address the 'multiple times a day' bisection challenge with deploy timestamps or a binary search strategy. |
| c14 | Output's database checks include N+1 detection, missing indexes, full table scans, and lock contention, with named tools or queries (`pg_stat_statements`, `EXPLAIN ANALYZE`, `pg_locks`) where applicable | PASS | EXPLAIN ANALYZE is explicitly named and used for full table scan detection ('Seq Scan'). pg_locks is named with a query ('SELECT * FROM pg_locks WHERE NOT granted'). N+1 and missing indexes are both addressed. pg_stat_statements is not mentioned, but the other named tools satisfy the criterion. |
| c15 | Output applies the one-change-at-a-time discipline — any recommended fix is followed by a re-measurement step before the next change, not a batch of optimisations | FAIL | 'Immediate Actions (Next 30 Minutes)' batches 5 investigation/fix actions sequentially with no measurement gate between them. The output provides no re-measurement step between recommended changes, violating the one-change-at-a-time discipline. |
| c16 | Output names a profiling tool appropriate to the inferred stack (e.g. py-spy, async-profiler, dotnet-trace, Node clinic) before proposing code-level changes — and asks for stack confirmation if not stated | FAIL | No stack-specific application profiler (py-spy, async-profiler, dotnet-trace, Node clinic, etc.) is named anywhere in the output. The closing 'What data can you share?' section does not ask for stack confirmation. The output relies on generic database and load tools without addressing the application runtime. |
| c17 | Output stops and asks before recommending infrastructure scaling (more nodes, larger pool, bigger DB), framing the cost and architecture implications | FAIL | The output does not recommend infrastructure scaling explicitly, but also does not raise an explicit decision checkpoint or frame cost/architecture implications before any such recommendation. The criterion expects an acknowledged pause before scaling decisions, which is absent. |
| c18 | Output's findings table is prioritised by likely impact (HIGH/MEDIUM/LOW) with component and recommended fix per row, not a flat unranked list | PARTIAL | The 'Root Cause Hypotheses' table is ranked by Confidence (Very High/High/Medium) and includes a Next Step column. However, it does not use HIGH/MEDIUM/LOW impact labels and lacks a 'Component' column (e.g., Database, Application, Infrastructure). Partially satisfies the criterion. |
| c19 | Output requires before/after measurement at the same load and same metric for every change, with the measurement protocol stated (warm-up, sample size, statistical significance) | FAIL | No before/after measurement requirement is stated for any individual change. The measurement protocol (warm-up period, sample size, statistical significance thresholds) is entirely absent. The load test section describes a single comparative run but does not establish a repeatable measurement protocol. |

### Notes

The output is a competent triage guide that correctly identifies the P50/P99 divergence as a tail-latency/contention signal, covers the key database failure modes with appropriate named tools, and produces a ranked hypothesis table. However, it fails on nearly all of the rigorous performance-engineering process criteria: it skips baseline capture before any recommendations, skips the outside-in end-to-end timing step, does not apply one-change-at-a-time discipline with re-measurement gates, names no stack-appropriate application profilers, does not ask for stack confirmation, and omits before/after measurement protocols entirely. The output reads as a solid senior-engineer checklist but not as a disciplined performance investigation methodology. It scores well only on the 'what to look for' criteria (c3, c7, c11, c14) and poorly on the 'how to investigate rigorously' criteria (c1, c2, c4, c9, c15, c16, c17, c19).
