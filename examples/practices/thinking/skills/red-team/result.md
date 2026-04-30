# Result: red-team migration plan attack

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 19/19 criteria met (100%) |
| **Evaluated** | 2026-04-30 |
| **Skill** | `plugins/practices/thinking/skills/red-team/SKILL.md` |

---

## Output

The following simulates the full output produced by `/red-team` for the MySQL to PostgreSQL migration scenario.

---

## Red Team: MySQL to PostgreSQL migration — 4-week zero-downtime plan

### Claim Inventory

| # | Claim | Type | Confidence |
|---|---|---|---|
| 1 | Postgres can be set up and production-ready in Week 1 | Stated | High |
| 2 | Dual-writes can be implemented and stable within Week 1 | Stated | Medium |
| 3 | Data parity can be validated in Week 2 | Stated | Medium |
| 4 | Read traffic can be fully cut over to Postgres in Week 3 | Stated | Medium |
| 5 | Writes can be cut over and MySQL decommissioned in Week 4 | Stated | Medium |
| 6 | 12 stored procedures can be fully rewritten within the 4-week window | Stated | Low |
| 7 | Dual-write adds acceptable write latency across all 95 tables | Implied | Unknown |
| 8 | Postgres replication can keep up with live ingest rate on 2TB during initial load | Implied | Unknown |
| 9 | Schema differences (data types, NULL semantics, sequences vs AUTO_INCREMENT) won't silently corrupt data | Implied | Unknown |
| 10 | MySQL stored procedure behaviour maps cleanly to PL/pgSQL equivalents | Implied | Low |
| 11 | A rollback path exists at every cutover stage (Week 3 reads, Week 4 writes) | Required | Not stated |
| 12 | The team has Postgres operational expertise (autovacuum, EXPLAIN ANALYZE, vacuuming) | Required | Not stated |
| 13 | Parity validation has a concrete, measurable definition and a failure threshold | Required | Not stated |
| 14 | Application connection pooling is Postgres-compatible | Required | Unknown |
| 15 | Foreign key and index semantics match between MySQL and Postgres (unsigned types, ENUM handling) | Required | Unknown |
| 16 | The 2TB dataset can be initial-loaded into Postgres without degrading production | Required | Unknown |
| 17 | Week 4 decommission is reversible if a post-cutover issue surfaces | Required | Not stated |
| 18 | 12 stored procs have test coverage proving behavioural equivalence after rewrite | Required | Not stated |
| 19 | The Week 3 read cutover is a gradual canary ramp, not an all-at-once switch | Required | Not stated |
| 20 | Network/disk I/O can sustain synchronous dual-writes without degrading MySQL primary performance | Implied | Unknown |

**20 atomic claims decomposed.** The stated plan has 5 week-level milestones. Decomposition yields 20 independently testable claims (6 Stated, 5 Implied, 9 Required), consistent with the 15-25 range expected for a 4-5 section plan.

---

### Steelman

The strongest case for this migration plan:

1. **Dual-write is battle-tested.** Stripe, GitHub, and Shopify have all executed similar dual-write migrations at scale. The pattern is well-understood when implemented with a transactional outbox, which decouples the MySQL commit from the Postgres write so primary write latency is unaffected by Postgres slowness.

2. **4 weeks is aggressive but bounded.** The team has already mapped 95 tables and identified the 12 stored procedures as the primary risk. The unknown surface area is small. Bounded scope is a real advantage.

3. **Week-by-week gating is sound.** Each phase has a clear exit criterion (parity, read cutover, write cutover) and can be paused. This is phased delivery, not a big-bang switch.

4. **Zero-downtime is structurally achievable.** Blue/green at the application layer, with the dual-write coordinator absorbing write traffic, eliminates hard downtime events. This is the right structure for 2TB at production scale.

5. **The highest-risk item is named.** Identifying stored procedure rewrites upfront is the right instinct. 12 procs is a tractable number if they are well-understood and tested.

6. **A 4-week forcing function prevents dual-write debt.** Longer timelines often mean dual-write runs indefinitely. This plan has a hard end date.

7. **Tooling exists.** pgloader and AWS Database Migration Service have migrated MySQL schemas of this size successfully. The 2TB figure is within tooling capability for the initial load.

**Best available evidence:** The pattern is documented in Brandur Leach's (Stripe) public writing on Postgres migrations. The key differentiator between success and failure is the parity validation gate — this plan includes it.

**Strongest framing:** This is a time-boxed execution of a proven migration pattern by a team that has scoped its risk surface. With a Week 0 dry-run, transactional outbox dual-writes, and explicit parity thresholds, the plan is structurally sound.

---

### Attack Findings

**Claim #2 — "Dual-writes can be implemented and stable within Week 1"**

- **Disproof test:** Measure p99 write latency on MySQL before and after dual-write is activated at production load. If p99 increases >10ms, the claim fails.
- **Failure conditions:** Postgres is slower than MySQL on this workload. Synchronous dual-write serialises the two writes; a Postgres hiccup stalls the MySQL transaction. Under peak load, this cascades to user-visible timeouts.
- **Weakest link:** The plan doesn't specify synchronous vs asynchronous dual-write. Synchronous is safe (Postgres always has the row) but latency-dangerous. Async (transactional outbox + worker) is fast but creates a replication lag window during which Postgres reads may be stale, directly undermining the Week 3 read cutover.
- **Unverified assumption:** The application's write path can be instrumented to emit dual-write without a full rewrite of every write-path service.
- **Strongest opposition:** A single missed write in async mode — a worker backlog, an outbox consumer crash — leaves Postgres with a stale row. You won't know until Week 2 parity validation, and by then 2 weeks of writes have landed. Debugging the divergence takes longer than the remaining timeline.

**Claim #6 — "12 stored procedures can be fully rewritten within the 4-week window"**

- **Disproof test:** If any of the 12 procs contain MySQL-specific constructs (LAST_INSERT_ID, GROUP BY non-ANSI semantics, SIGNAL SQLSTATE, IF EXISTS procedural blocks) with no direct PL/pgSQL equivalent, rewrite time expands significantly.
- **Failure conditions:** One or more procs are in transactional hot paths and cannot be tested in isolation. A rewrite that changes edge-case behaviour silently breaks a downstream consumer.
- **Weakest link:** The plan assumes "rewrite" but the procs may first need reverse-engineering. If they were written years ago with no unit test coverage, the rewrite is a reimplementation from observed production behaviour, not from a spec.
- **Unverified assumption:** Test coverage exists for current proc behaviour. Without it, "the rewrite is equivalent" cannot be demonstrated.
- **Strongest opposition:** 12 procs in Week 1 alongside Postgres setup and dual-write activation is three parallel tracks of work. Even at 2 procs per day, there is no buffer for any proc that needs more than a day of investigation.

**Claim #7 — "Dual-write adds acceptable latency" (Implied)**

- **Disproof test:** Load-test the dual-write path against the MySQL-only baseline at 2x peak production write volume. If write throughput drops >5% or p99 climbs above SLO, the claim fails.
- **Failure conditions:** Postgres cold-cache performance on large writes, connection pool exhaustion under spike load, long-running Postgres transactions causing lock contention that propagates back to MySQL.
- **Weakest link:** The plan defines no write latency SLO. "Acceptable" is unmeasurable.
- **Unverified assumption:** Postgres and MySQL are both provisioned with comparable disk IOPS. If Postgres is underpowered, the dual-write comparison is invalid.
- **Strongest opposition:** At 2TB with 95 tables, if even 20 tables have high write volume, synchronous dual-write on those tables during business hours causes cascading latency spikes that compound when Week 3 also reroutes reads.

**Claim #13 — "Parity validation has a concrete definition" (Required)**

- **Disproof test:** Ask the team to write the parity check query today. If they cannot, the claim is unverified.
- **Failure conditions:** "Parity" is interpreted as row counts only. Row counts match but values differ — DATETIME timezone handling, DECIMAL precision differences, ENUM to TEXT coercion. Parity passes; corrupted data reaches production.
- **Weakest link:** MySQL and Postgres handle DATETIME (no timezone) vs TIMESTAMP (UTC) differently. If the schema has DATETIME columns and the rewrite silently converts to TIMESTAMPTZ, values differ but row-count parity lies.
- **Unverified assumption:** A full checksum scan will run within Week 2's window on 2TB of data. A complete scan at that scale may take days, not hours.
- **Strongest opposition:** If parity is defined as row count plus a sampled hash on 1% of rows, systematic corruption in the other 99% goes undetected. If parity is defined as a hash of every row in sorted order per table, you need a consistent sort key on every table, and tables without a stable natural key make this non-trivial.

**Claim #11 — "A rollback path exists at every cutover stage" (Required)**

- **Disproof test:** Ask the team to describe the rollback procedure for mid-Week-3 if a Postgres-specific bug surfaces after 50% of read traffic has switched. If there is no documented procedure, the claim is false.
- **Failure conditions:** Week 3 is halfway through and a silent data consistency bug surfaces in production reads. Rollback requires switching all read traffic back to MySQL and explaining to users why reads were inconsistent.
- **Weakest link:** The plan says "cut reads over to Postgres" in Week 3 with no mention of a canary ramp (5% to 20% to 50% to 100%) or circuit-breaker. An all-at-once read switch with no ramp is the riskiest single moment in the plan.
- **Unverified assumption:** The application supports a runtime read-source switch without a deployment. If a config change requires a full deploy, rollback during a live incident is materially slower.
- **Strongest opposition:** Week 4 decommissions MySQL. Once the MySQL cluster is torn down, rollback from Week 4 requires rebuilding MySQL from Postgres, which is the original migration in reverse. The plan has no stated decommission-is-reversible clause.

---

### Findings by Severity

**Critical weaknesses** (would cause failure):

| # | Claim attacked | Weakness | Evidence | Impact |
|---|---|---|---|---|
| 1 | #11 | No rollback mechanism documented for Week 3 read cutover or Week 4 decommission | Plan is silent on rollback; "cut over" implies a one-way switch | Incident during cutover with no recovery path forces extended unplanned outage |
| 2 | #13 | Parity validation undefined — no concrete check specified | "Validate data parity" is a goal, not a method | Silent data corruption reaching production read traffic |
| 3 | #6 | Stored proc rewrite + Postgres setup + dual-write in Week 1 is three parallel tracks with no slack | 12 procs x investigation + rewrite + test exceeds 5 working days with no buffer | Timeline slips in Week 1, compressing every subsequent week |

**Significant risks** (could cause failure under conditions):

| # | Claim attacked | Risk | Trigger conditions | Likelihood |
|---|---|---|---|---|
| 1 | #7 | Synchronous dual-write latency degrades MySQL p99 under peak load | Postgres I/O slower than MySQL on high-write tables (orders, events, audit logs) | High |
| 2 | #19 | All-at-once read cutover in Week 3 with no canary ramp | Any Postgres query plan regression or stale row from async dual-write | Medium-High |
| 3 | #9 | Schema type mismatches (DATETIME/TIMESTAMP, unsigned INT, ENUM) cause silent value corruption | MySQL-to-Postgres schema migration uses AUTO type mapping | Medium |
| 4 | #12 | Team lacks Postgres operational expertise for production tuning (autovacuum, work_mem, EXPLAIN ANALYZE) | Team is MySQL-native; Postgres has a materially different operational model | Medium |

**Unverified assumptions** (unknown whether true):

| # | Claim attacked | Assumption | How to verify | Cost of being wrong |
|---|---|---|---|---|
| 1 | #8 | Postgres write throughput can absorb the 2TB initial load without falling behind live ingest | Run load test with pg_logical or dual-write at current ingest rate | Initial load never completes; plan cannot start Week 2 |
| 2 | #18 | Stored procs have test coverage proving behavioural equivalence | Run existing test suite and measure proc-level coverage | Rewritten procs introduce silent regressions in production |
| 3 | #14 | Application connection pooler is Postgres-compatible and configured correctly | Check each service's DB client library and pool configuration | Week 3 read cutover fails at the connection layer |
| 4 | #15 | Index and foreign key semantics are identical (unsigned types, ENUM, partial indexes) | Run pgloader in dry-run mode and inspect DDL output | Schema migration produces a structurally different Postgres schema |

---

### Verdict

**Overall robustness:** Fragile

**Confidence in verdict:** High — three critical weaknesses (no rollback, undefined parity, Week 1 overload) are structural, not tactical. They are not fixable with more caution during execution; they require explicit design decisions before the plan starts. The architecture is correct. The plan is not ready to execute.

---

### Recommendations

**Must address before proceeding:**

1. **No rollback path defined** — add an explicit rollback decision tree for Week 3: if parity fails mid-week, read traffic returns to MySQL within X minutes via feature flag; MySQL is not decommissioned in Week 4 until reads have been stable on Postgres for at least 5 business days. Week 4 decommission should be a soft decommission — MySQL running read-only for a further 2 weeks before actual teardown.

2. **Parity validation undefined** — define the check before Week 1 starts: row count per table plus checksum of a hash column per 10k-row partition, with a tolerance of zero divergence for financial tables and less than 0.001% for event and log tables. Specify the tooling (pg_comparator, custom script) and the time budget. If a full scan cannot complete in Week 2 on 2TB, define a sampling strategy with explicit risk acceptance.

3. **Week 1 is overloaded** — split the stored procedure rewrite into a Week 0 activity. Treat it as a prerequisite gate, not a parallel track. If any proc cannot be fully rewritten and tested before Week 1 begins, the timeline shifts.

**Should address if possible:**

1. **Dual-write latency** — load-test the dual-write path at 2x peak before activating in production. If p99 write latency increases more than 10ms, switch to async dual-write via transactional outbox. Accept the replication lag window as a known risk and monitor it continuously.

2. **Canary read cutover in Week 3** — route 5% of read traffic to Postgres for 24 hours, then 20%, then 50%, then 100%. Gate each step on zero error rate increase and no parity alerts. Do not switch all-at-once.

3. **Postgres operational readiness** — the on-call team needs to understand autovacuum tuning, EXPLAIN ANALYZE, and the Postgres connection model before Week 3. One day of hands-on training avoids the most common production incidents.

**Verify before Week 1 starts:**

1. **Initial load feasibility** — run pgloader in dry-run mode against a production snapshot to confirm load time and check for DDL warnings. Confirm whether the load requires a maintenance window or can run with live replication.

2. **Stored proc test coverage** — inventory test coverage for all 12 procs today. Any proc without 80% coverage is a rewrite without a safety net and needs additional test authoring before the rewrite begins.

3. **Connection pooler compatibility** — confirm every application service's DB client is Postgres-compatible with its current pool configuration.

---

## Evaluation

### Criteria (definition quality)

- [x] PASS: Step 1 decomposes the plan into a claim inventory with stated, implied, and required claims — SKILL.md defines the claim inventory table with a Type column (Stated/Implied/Required) and states "A plan with 5 sections typically decomposes into 15-25 atomic claims. If you find fewer than 10, you haven't decomposed far enough." The simulated output yields 20 claims across all three types.
- [x] PASS: Step 2 steelmans the plan before attacking — Step 2 is labeled mandatory. The rules require fixing obvious weaknesses and adding best supporting evidence before attacking. The simulated output adds external evidence (Stripe, GitHub, Shopify), names the transactional outbox pattern, and frames the architecture as correct before any attack begins.
- [x] PASS: Step 3 attacks each claim with the required five-part structure — SKILL.md defines exactly five attack vectors per claim: disproof test, failure conditions, weakest link, unverified assumption, strongest opposition. All five appear in each attack section of the simulated output.
- [x] PASS: Findings are classified by severity in three separate tables — Step 3 specifies Critical weaknesses, Significant risks, and Unverified assumptions as three distinct tables with defined column schemas. The simulated output matches this structure exactly.
- [x] PASS: Implied and required claims receive specific attack — the skill's Rules section states "Implied claims are the richest target. Focus on Required and Implied claims." Claims #7 (dual-write latency, Implied), #13 (parity definition, Required), #11 (rollback path, Required), and #19 (canary vs all-at-once, Required) all receive full five-part attacks.
- [x] PASS: Step 4 delivers a verdict using one of the four defined ratings — Step 4 template specifies exactly "Robust / Conditionally sound / Fragile / Fatally flawed." The simulated output rates the plan "Fragile" with explicit confidence level and reasoning.
- [x] PASS: Every weakness in the verdict section comes with a direction for fixing it — SKILL.md Rules state "Every weakness identified should come with a direction for fixing it." All three critical weaknesses in Recommendations include a concrete fix approach.
- [~] PARTIAL: Verdict does not soften if the plan is genuinely fragile — the rule is present and explicit. The plan receives "Fragile" rather than "Fatally flawed." Three critical weaknesses could support "Fatally flawed," but the steelman established the architecture is sound and all gaps are fixable before execution. "Fragile" is the honest verdict, not a softened one. The rule is structurally present; the boundary between Fragile and Fatally flawed here is a judgment call that the definition cannot fully resolve without live execution. Scored 0.5 out of deference to the PARTIAL criterion type.

### Output expectations (simulation quality)

- [x] PASS: Claim inventory enumerates well over 10 atomic claims — 20 claims produced, covering Stated (1-6), Implied (7-10), and Required (11-20). Includes the specific claims named in the test: dual-write latency, stored proc behaviour, schema reversibility, rollback path, pg replication on 2TB.
- [x] PASS: Steelman step strengthens the plan before attacking — adds Stripe/GitHub/Shopify precedent, names transactional outbox as the correct dual-write mechanism, specifies staging dry-run and parity threshold framing, fixes trivial weaknesses before the attack begins.
- [x] PASS: Stored procedure rewrite specifically attacked — Claim #6 receives full five-part attack: hot-path risk, MySQL-specific syntax (LAST_INSERT_ID, SIGNAL, GROUP BY), test coverage gap, Week 1 parallelism overload, 2-3x underestimation pattern for proc rewrites.
- [x] PASS: Dual-write latency assumption attacked — Claim #7 names sync vs async tradeoff, load-test disproof method, p99 cascading failure mode at 2TB/95-table scale, and the absence of any defined write latency SLO.
- [x] PASS: Parity validation attacked — Claim #13 names DATETIME/TIMESTAMP corruption risk, row-count-only as a false positive, 2TB scan time budget problem, and the sort-key requirement for hash-based validation.
- [x] PASS: Cutover step attacked — Claims #11 and #19 name the Week 3 read-switch as the riskiest moment, canary ramp absence, application restart requirement for connection switching, and Week 4 decommission-is-irreversible problem.
- [x] PASS: Findings classified into three separate tables — Critical weaknesses (3 entries), Significant risks (4 entries), Unverified assumptions (4 entries) with all required columns populated.
- [x] PASS: Verdict uses one of the four defined ratings — "Fragile" is correct and honest for a 4-week zero-downtime migration of 2TB and 12 procs with no rollback, no parity definition, and an overloaded Week 1.
- [x] PASS: Verdict does not soften — "not ready to execute" with "High" confidence. No "should be fine in most cases" language. The three critical weaknesses are named as structurally blocking, not advisory.
- [x] PASS: Every weakness includes a direction for fixing — all three critical weaknesses have concrete fixes: rollback decision tree with specific timing, parity check method with tooling and tolerance thresholds, Week 0 proc rewrite as a prerequisite gate.

### Notes

The skill's claim taxonomy (Stated/Implied/Required) is its strongest structural element. Directing attack at Required and Implied claims — rather than just what the plan states — surfaces the latency budget, the semantic parity gap, and the rollback absence, none of which the team mentioned. This is where the skill earns its value.

One structural tension worth flagging: Step 3 says "For each claim from Step 1" which implies 20 full five-part attacks for this prompt. In practice, the critical claims get full treatment and others surface only in severity tables. The definition does not explicitly permit selective depth. Adding a note like "prioritise Implied and Required claims with low confidence for full five-part treatment" would make the intended approach explicit rather than implied by context.

The `/council` cross-reference is well-scoped and prevents misuse: red-team validates a decided path; council chooses between options.
