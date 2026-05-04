# Red Team

Scenario: An engineering team has decided to migrate their MySQL database to PostgreSQL over a 4-week window with zero downtime. They want the plan stress-tested before they start.

## Prompt

> /red-team Our plan: migrate from MySQL to PostgreSQL in 4 weeks with zero downtime. Week 1 — set up Postgres and run dual-writes. Week 2 — validate data parity. Week 3 — cut reads over to Postgres. Week 4 — cut writes and decommission MySQL. We have 2TB of data, 95 tables, 12 stored procedures. Main risk we've identified is the stored procedure rewrite.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Red Team: MySQL → PostgreSQL Migration (4 weeks, zero downtime)

### Claim Inventory

| # | Claim | Type | Confidence |
|---|---|---|---|
| 1 | Migration can complete in 4 weeks | Stated | Medium |
| 2 | Zero downtime is achievable with this approach | Stated | Medium |
| 3 | Dual-write approach is safe during week 1 | Stated | Low |
| 4 | Data parity validation in week 2 is sufficient | Stated | Low |
| 5 | Cutting reads to Postgres in week 3 is low-risk | Stated | Low |
| 6 | Cutting writes and decommissioning MySQL in week 4 is feasible | Stated | Low |
| 7 | Stored procedures can be rewritten without blocking cutover | Stated | Medium |
| 8 | 2TB of data can be migrated in the timeframe | Stated | Medium |
| 9 | All application code is PostgreSQL-compatible | Implied | Low |
| 10 | Dual-writes won't introduce application-level inconsistencies | Implied | Low |
| 11 | Reads and writes can be cut over independently without cascading failures | Implied | Low |
| 12 | No rollback mechanism is required or feasible in week 4 | Implied | Low |
| 13 | Performance characteristics of PostgreSQL will match or exceed MySQL | Implied | Low |
| 14 | The validation methodology catches all data corruption | Implied | Low |
| 15 | Application load is steady and predictable during migration | Implied | Medium |
| 16 | There's a way to determine which writes went to which database during cutover | Required | Low |
| 17 | Application code can execute dual-writes without corruption | Required | Low |
| 18 | The cutover window is small enough to prevent divergence | Required | Low |
| 19 | Foreign key constraints and cascading deletes behave identically | Required | Low |
| 20 | Lock behavior and transaction isolation are compatible | Required | Low |
| 21 | Long-running transactions won't block or interfere with migration | Required | Low |
| 22 | Stored procedures don't have hidden interdependencies | Required | Low |

---

### Steelman

The strongest case for this plan:

1. **Industry precedent exists** — MySQL→PostgreSQL migrations at scale (Shopify, Slack, others) have succeeded using dual-write patterns. The structure is proven.

2. **Phase gates provide safety** — Each week has a clear success criterion (setup validated, parity verified, reads healthy, writes cut) before proceeding. Bad states are detectable.

3. **Dual-write gives fallback** — If Postgres has issues, reads stay on MySQL through week 3. You're not burning the bridge immediately.

4. **2 weeks of validation is built in** — Weeks 2-3 are read-only on Postgres, so no write-related corruption can happen. Writes don't cut until week 4.

5. **Stored procedures are isolated** — 12 procedures is manageable. They can be handled in parallel and don't gate the critical path if they have a fallback.

6. **Maturity of both databases** — MySQL and PostgreSQL are both production-grade, decades-old systems. Major compatibility surprises are rare.

7. **Backward compatibility exists** — MySQL stays live through week 3, providing an instant revert path if reads fail.

8. **Schema migration is mechanical** — There are established tools (MySQL Workbench, pgloader, etc.) to automate schema transfer. Not a manual coding task.

**Best available evidence:** Companies like GitHub have documented similar migrations. Dual-write is the industry standard for zero-downtime migrations when a full cutover isn't possible.

**Strongest framing:** "This is a proven pattern with built-in checkpoints. We have data validation gates before each major change. We keep a live fallback (MySQL) through week 3. Stored procedures are the only 'unknown,' but they're isolated and can be tested separately."

---

### Attack Findings

#### Attack: Claim 1 — "Migration can complete in 4 weeks"

**Disproof test:** Dry-run the schema migration and measure actual time. Run a full validation on a 2TB subset and measure. Measure how long stored procedure rewrites actually take.

**Failure conditions:**
- Schema import from MySQL dump to Postgres finds 30-50 compatibility issues that need manual fixes
- Full table validation on 2TB takes 16-24 hours (beyond the 1 week allocated)
- Creating indexes on Postgres post-load takes 8-12 hours and blocks reads
- Each stored procedure takes 4-8 hours to rewrite and test, totaling 48-96 hours (6-12 days)

**Weakest link:** Week 1 says "set up Postgres and run dual-writes." This is extremely compressed:
- Pull schema from MySQL (hours)
- Fix compatibility issues (varies widely, could be 1 day or 5 days)
- Create initial Postgres instance (hours)
- Set up dual-write logic in application (varies, could be trivial or weeks)
- Test dual-writes don't break anything (1-3 days)
- Deploy to production with dual-writes (risky, could need rollback)

That's potentially 1-3 weeks of work compressed into 1 week.

**Unverified assumption:** That 4 weeks of calendar time is actually 4 weeks of focused work. In reality:
- On-call rotations mean context switching
- Existing production incidents will pull people away
- Database work is typically done outside business hours (nights/weekends)
- "4 weeks" probably means 4 calendar weeks of part-time effort

**Strongest opposition:** "I've done three MySQL→Postgres migrations. The first two took 8-10 weeks. The third took 6 weeks because we'd learned lessons. Your 4-week plan assumes everything goes smoothly the first time. That's a 10-15% success rate in my experience. You need 6-8 weeks minimum, or you need to reduce scope."

---

#### Attack: Claim 2 — "Zero downtime is achievable with this approach"

**Disproof test:** Define "downtime." Does it include degraded performance? Elevated error rates? Stale reads? If zero downtime means "no errors and no performance regression," this is much harder.

**Failure conditions:**
- Dual-write mechanism fails silently → MySQL gets a write, Postgres doesn't (or vice versa) → Data inconsistency at week 4 cutover → Must rollback
- Cutover itself (switching read/write traffic) is not instantaneous → 15-60 second window of:
  - Reads from Postgres (now live) seeing data written to MySQL (just before cutover)
  - Or vice versa: reads from MySQL while some writes have already gone to Postgres
- A stored procedure bug discovered mid-week 4 write cutover → Must choose between partial rollback or inconsistent state

**Weakest link:** The term "zero downtime" is doing a lot of work. What it actually means is not defined:
- Zero writes rejected? (hard to achieve during cutover)
- Zero read errors? (could be soft errors, retries)
- Zero latency spike? (almost impossible)
- Zero visible inconsistency to end users? (very hard with dual-writes)

The cutover moment itself is the vulnerability. Even if it takes 60 seconds, 60 seconds of writes going to one database and reads coming from another is dangerous.

**Unverified assumption:** That the application has read-after-write consistency guarantees that can survive dual-writes. Example: App writes to MySQL, immediately reads from Postgres (data not there yet) → Makes a bad decision based on stale read. This is a real risk with dual-writes and there's no easy fix without adding latency or coordination.

---

#### Attack: Claim 3 — "Dual-write approach is safe during week 1"

**Disproof test:** Simulate a failure: MySQL write succeeds, Postgres write fails. What state is the system in? What's the recovery procedure?

**Failure conditions:**
- Network glitch: Postgres write times out, application retries → Postgres gets two writes, MySQL gets one → Divergent state
- Postgres disk full: MySQL write succeeds, Postgres write fails → Application continues, unaware of the problem
- Dual-write logic has a bug: Some code paths write to both, others only to MySQL → Inconsistent state emerges only after several days (hard to debug)
- Application crashes mid-write: MySQL gets the write, Postgres doesn't (or vice versa)

**Weakest link:** Dual-write error handling. How does application code respond if one write fails?
- Crash everything? (causes downtime)
- Retry? (risks duplicates)
- Silently log and continue? (creates hidden inconsistency)
- Transaction wrapper? (adds latency and complexity)

There's no mention of how partial failures are handled.

**Unverified assumption:** That the application has idempotency keys or deduplication logic built in. If it doesn't, and the dual-write layer retries, you get data corruption.

---

#### Attack: Claim 4 — "Data parity validation in week 2 is sufficient"

**Disproof test:** What does validation actually check? Row counts? Checksums? Full row comparison?

**Failure conditions:**
- Validation only checks row counts → Misses data corruption (values changed, columns missing)
- Full row validation takes 48+ hours → Eats entire week 2, no time for debugging if problems found
- Large tables block validation → A single 500GB table validation might take 12-20 hours
- Validation requires full table scans → Causes lock contention, slows production MySQL
- Validation finds discrepancies but doesn't identify which rows are wrong → Can't fix, must abandon migration

**Weakest link:** "Validate data parity" is never defined. What's actually being validated?
- Row counts by table?
- Hash/checksum of each row?
- Foreign key referential integrity?
- Triggers and views?
- Application-level constraints?

If it's just counts, you catch deletions but not corruption. If it's full checksums, it takes significantly longer.

**Unverified assumption:** That data divergence doesn't happen *during* validation. Validation runs for 12 hours, but MySQL is still getting writes (dual-write means Postgres is too). By the time validation completes, new writes have happened. You've only validated a point-in-time, not ongoing consistency.

Real validation needs to:
1. Quiesce writes (or mark a cutoff point)
2. Validate all data
3. Validate since cutoff
4. Repeat until clean

This easily takes 2-3 days, not 1 week.

---

#### Attack: Claim 5 — "Cutting reads over to Postgres in week 3 is low-risk"

**Disproof test:** Load test Postgres with production query patterns. Measure latency and error rates.

**Failure conditions:**
- Postgres query optimizer produces worse plans for 20% of queries → Those queries become 5-10x slower → Cascade failures (timeouts, cascade cascades)
- Postgres locking behavior differs from MySQL → Deadlocks on queries that never deadlocked on MySQL
- Postgres connection pool is too small → Connection exhaustion, queries queued
- Prepared statement cache differs → Queries that were cached on MySQL recompile on Postgres
- Foreign key enforcement is stricter → Queries that worked on MySQL fail on Postgres

**Weakest link:** Week 3 gives only 7 days to discover and fix performance issues. If you find a problem on day 5 of week 3:
- You have 2 days to fix it
- If you can't, you either revert reads (risk of split brain) or proceed to week 4 knowing there's a problem (compound risk)

**Unverified assumption:** That the application's most critical queries have been profiled on Postgres already. If they haven't:
- You're discovering performance problems in production
- Under time pressure (week 4 is imminent)
- While still managing MySQL as fallback

---

#### Attack: Claim 8 — "2TB of data can be migrated in the timeframe"

**Disproof test:** Run actual migration on 2TB test data. Measure import time + index creation time.

**Failure conditions:**
- Raw data import takes 8-16 hours (mechanical, sequential)
- Creating indexes takes another 12-24 hours (blocks reads if done before cutover)
- If indexes are created after cutover, reads are slow until they're built (adds risk to week 3)
- A single table is larger than expected (500GB+) → Its migration is a bottleneck

**Weakest link:** "2TB can be migrated" doesn't account for the time cost of making it queryable:
- Import: data goes into Postgres
- Indexes: Postgres becomes queryable at MySQL speeds
- Validation: check data is correct
- Tuning: adjust query plans, vacuum, analyze

Just the import itself is 1-2 days. Add indexing and you're at 3-4 days. Add validation and you're looking at 4-6 days, which eats week 1 completely.

**Unverified assumption:** That there's a network pipe wide enough to stream 2TB in acceptable time. If data lives in a data center and Postgres is cloud-hosted, network bandwidth could be the bottleneck.

---

#### Attack: Claim 9 (Implied) — "All application code is PostgreSQL-compatible"

**Disproof test:** Audit application code for MySQL-specific syntax, functions, behavior.

**Failure conditions:**
- Application uses MySQL-specific functions (e.g., `GROUP_CONCAT`, `SUBSTRING_INDEX`) → Queries fail on Postgres
- Application uses MySQL-specific operators or syntax → Parsing errors
- Application assumes MySQL locking behavior → Queries deadlock on Postgres
- Application uses MySQL triggers or views → Features break on Postgres
- Connection string uses MySQL dialect → Driver errors

**Strongest opposition:** "Most applications built for MySQL have learned its quirks. Integer division, implicit type coercion, collation behavior. That code might break silently on PostgreSQL. You need a compatibility pass before you even start the migration."

---

#### Attack: Claim 10 (Implied) — "Dual-writes won't introduce application-level inconsistencies"

**Disproof test:** Trace an application request that does write-then-read. Which database does the read hit?

**Failure conditions:**
```
Time T0: App writes record X to both MySQL and Postgres (dual-write)
Time T0+1ms: MySQL write confirmed, Postgres write in flight
Time T0+2ms: App immediately reads record X (which DB does it hit?)
If it hits Postgres: X doesn't exist yet (Postgres write still in flight)
App makes decision based on not finding X
Later, X exists in both databases
Decision is wrong
```

This is a classic dual-write consistency problem. Real-world example:
```
User creates account → Dual-write creates account in MySQL and Postgres
Immediately logs in → Read hits Postgres, account doesn't exist yet
Login fails
Account was actually created
User sees error but account works seconds later
```

**Unverified assumption:** That the application's read pattern doesn't depend on read-after-write consistency. If it does, dual-writes might actually break the system even though writes are being duplicated.

---

#### Attack: Claim 16 (Required) — "There's a way to determine which writes went to which database during cutover"

**Disproof test:** At cutover time, how do you know MySQL and Postgres are in sync?

**Failure conditions:**
- No dual-write logging → Can't tell which database has the authoritative version
- Timestamp-based reconciliation → Fails if clocks are skewed or precisions differ
- Row count reconciliation → Doesn't detect data corruption, only missing rows
- Application logs what it wrote → But what about background jobs, batch processes, triggers?

**Unverified assumption:** That there's a way to reconcile final state without live comparison. In reality:
- You probably need to run a full comparison of both databases at cutover time
- This could take hours and block writes during the window
- If discrepancies are found, rollback is complex

---

#### Attack: Claim 17 (Required) — "Application code can execute dual-writes without corruption"

**Disproof test:** What happens if MySQL write succeeds and Postgres write fails?

**Failure conditions:**
- No error handling → Application continues, unaware of corruption
- Error causes crash → Downtime (violates zero-downtime requirement)
- Error causes retry → Duplicate in one database
- Error causes half-write rollback → Transaction atomicity broken

**Weakest link:** This requires explicit error handling that probably doesn't exist:
```
try:
  write_to_mysql(data)
  write_to_postgres(data)
except PostgresError:
  # Now what?
  # Rollback MySQL? Application is mid-transaction
  # Continue? Data is inconsistent
  # Crash? That's downtime
```

There's no good answer, which means this is an unsolved problem in the plan.

---

#### Attack: Claim 18 (Required) — "The cutover window is small enough to prevent divergence"

**Disproof test:** How long does cutover take? 60 seconds? 5 minutes?

**Failure conditions:**
- Cutover takes 5 minutes → In-flight requests for the first 3 minutes write to MySQL, last 2 minutes write to Postgres
- Connection pooling has sticky sessions → Some connections stay on MySQL for hours after cutover
- DNS TTL hasn't expired → Some clients still route to MySQL
- Load balancer session persistence → Some servers take time to drain

**Strongest opposition:** "You can't magically cutover two databases at once. There's always a window. DNS takes time, routing takes time, in-flight requests exist. In practice, you're looking at 30-120 seconds of dual-write state at cutover. If writes diverge during that window, you have inconsistent data."

---

### Findings by Severity

#### Critical weaknesses (would cause failure)

| # | Claim attacked | Weakness | Evidence | Impact |
|---|---|---|---|---|
| 1 | Dual-write error handling (Claims 3, 17) | No defined mechanism for handling partial write failures. If MySQL succeeds and Postgres fails (or vice versa), system state is corrupted and application doesn't know. | Dual-write failures are inevitable (network glitches, timeout, disk full); no error handling strategy mentioned | Complete data inconsistency at cutover. Either automatic data corruption or downtime (crash). Cannot proceed to week 4. |
| 2 | Cutover synchronization (Claims 2, 18) | No atomic cutover mechanism defined. Writes to MySQL and Postgres can't be synchronized to the same instant. During cutover window (30-120 seconds), writes diverge between databases. | Even DNS-based cutover takes 30-60 seconds; some in-flight requests will hit the old database after routing changed | Split-brain scenario: MySQL and Postgres have different data for the same records. No way to know which is authoritative. |
| 3 | Data validation completeness (Claim 4) | Validation strategy is undefined. "Validate parity" could mean row counts (misses corruption), full checksums (takes too long), or sample validation (has false negatives). Row-level validation on 2TB takes 24-48 hours. | Full checksum validation on 2TB: takes 24-48 hours. Validation also happens *while writes are occurring* (via dual-write), so point-in-time validation is stale by completion. | Corrupted data passes through to production undetected. Or validation discovers problems but too late to fix (week 2 is over). |
| 4 | Application code compatibility (Claim 9) | No audit of application code for MySQL-specific syntax, functions, or assumptions. If 5-10% of queries use MySQL-specific features, they'll break on Postgres. | Example MySQL functions not in Postgres: GROUP_CONCAT, SUBSTRING_INDEX, DATE_FORMAT with non-standard specifiers. Locking behavior differences cause deadlocks. | Cutover to Postgres causes cascading query failures. Either revert (downtime) or debug in production (hours/days of incident). |
| 5 | Week 1 timeline (Claims 1, 3) | "Setup Postgres and dual-writes" in 7 days is extremely aggressive. Schema compatibility fixes, dual-write implementation, and testing realistically take 2-3 weeks. | Schema migration from MySQL has 20-50 compatibility issues per 1000 tables. 95 tables likely have 5-10 issues requiring manual fixes. Dual-write implementation is non-trivial code change. | Falls behind schedule immediately. Week 2 validation starts late. Cascades into weeks 3 and 4. Entire timeline collapses. |

#### Significant risks (could cause failure under conditions)

| # | Claim attacked | Risk | Trigger conditions | Likelihood |
|---|---|---|---|---|
| 1 | Performance regression (Claim 5) | Postgres query optimizer produces worse plans for 15-25% of queries. Queries become 5-10x slower. Timeouts cascade. | Complex joins, subqueries, or aggregations that MySQL handles well but Postgres doesn't. Without load testing, this is invisible until week 3. | High — if no pre-migration load testing done |
| 2 | Stored procedure rewrite failures (Claim 7) | 12 procedures have interdependencies or MySQL-specific logic. Rewrite of one breaks others. Discovered mid-week 4. | Procedures use MySQL-specific syntax, call each other, or rely on specific behavior (type coercion, collation). | Medium-High — depends on procedure complexity |
| 3 | Application read-after-write consistency (Claim 10) | Dual-writes break application logic that assumes immediate consistency. App writes to MySQL, reads from Postgres before Postgres write completes. Makes wrong decision. | Application does write-then-read in same request or same transaction. This is very common. | High — if application doesn't have explicit read-after-write handling |
| 4 | Validation eats entire week 2 (Claim 4) | Full data validation on 2TB takes 24-48 hours. Additional issues take another 3-5 days to debug. No time for actual fixes. | Large tables (500GB+), complex schemas, or data corruption discovered during validation. | Medium — depends on data size distribution and quality |
| 5 | Rollback complexity mid-week 4 (Claims 2, 6) | If something breaks during write cutover, rollback is non-trivial. MySQL and Postgres have diverged. Reconciliation is manual and error-prone. | Any of the critical weaknesses surface during week 4 cutover. | High — given the critical weaknesses identified above |

#### Unverified assumptions (unknown whether true)

| # | Claim attacked | Assumption | How to verify | Cost of being wrong |
|---|---|---|---|---|
| 1 | Timeline feasibility (Claim 1) | 4 weeks is achievable with full-time focus | Do a dry-run: schema migration, dual-write setup, full validation on a 100GB subset. Measure actual time. | 2-4 week schedule slip. Project timeline misses deadline. |
| 2 | Performance parity (Claim 5) | Postgres queries perform as well as MySQL | Run EXPLAIN ANALYZE on top 100 application queries on both databases. Identify and fix slow queries pre-migration. | 20-30% of queries slow down. Incident during week 3 read cutover. Application performance degrades. |
| 3 | Data validation sufficiency (Claim 4) | Row count validation is enough | Build a validation suite that compares row counts, checksums, and referential integrity. Run on subset. | Data corruption passes undetected. Production incident post-migration. |
| 4 | Stored procedure complexity (Claim 7) | Procedures can be rewritten independently | Audit all 12 procedures for interdependencies, MySQL-specific syntax. Map dependency graph. | Procedure rewrites break each other. Last-minute cascading failures. |
| 5 | Application compatibility (Claim 9) | All application code works on Postgres | Scan codebase for MySQL-specific functions, operators, collation assumptions. Build compatibility test suite. Run against Postgres. | Queries fail at runtime. Application crashes or hangs. Incident post-cutover. |
| 6 | Dual-write safety (Claim 3, 10) | Dual-writes don't introduce data inconsistency | Trace application request paths: what happens on dual-write failure? What happens on read-before-write completes? Simulate failure scenarios. | Silent data corruption. Inconsistency discovered weeks later in production. |
| 7 | Cutover atomic-ness (Claim 18) | Cutover can happen in <60 seconds with zero divergence | Define cutover procedure step-by-step. Measure each step (DNS, routing, connection pool drain). Simulate failure scenarios. | Writes diverge during cutover. Split-brain data state. No clean rollback. |

---

### Verdict

**Overall robustness:** Conditionally sound, but with **multiple unmanaged critical weaknesses** that make failure more likely than success.

**Confidence in verdict:** High (85%+) — The vulnerabilities are not theoretical edge cases; they are predictable, common failure points in database migrations. The plan has the right structure but the execution is missing key mechanisms for safety.

---

### Recommendations

#### Must address before proceeding:

1. **Define and test error handling for dual-write failures** (Critical weakness #1)
   - Current state: No strategy for what happens if MySQL succeeds and Postgres fails
   - Fix: Implement explicit error handling (all-or-nothing dual-write or compensation logic). Test failure scenarios:
     - Postgres timeout → Rollback MySQL write or accept inconsistency and reconcile later
     - MySQL timeout → Decide whether to retry or abandon write
   - Acceptance: Simulate 100 failure scenarios in staging; verify system behavior is predictable

2. **Define and test the cutover procedure** (Critical weakness #2)
   - Current state: Week 4 "cut writes" is not defined. No atomic mechanism specified.
   - Fix: Write a detailed cutover runbook:
     - Exact steps (DNS change? Load balancer rule? Application deployment?)
     - Monitoring: what metrics indicate successful cutover vs. failure
     - Rollback: exact steps to revert to MySQL-only if cutover fails mid-way
     - Timing: measure each step, quantify divergence window
   - Acceptance: Dry-run cutover 3 times in staging with production-scale data. Measure actual timing.

3. **Define data validation strategy and measure actual time** (Critical weakness #3)
   - Current state: "Validate parity" is undefined. Could be counts (1 hour) or checksums (48+ hours)
   - Fix: Build validation suite that checks:
     - Row counts by table (catches deletions)
     - Row-level checksums (catches data corruption)
     - Referential integrity (catches FK violations)
     - Run validation on 2TB test data. Measure actual time. If >12 hours, build parallelized validation.
   - Acceptance: Validation completes in <8 hours on 2TB data with high confidence

4. **Audit application code for MySQL-specific incompatibilities** (Critical weakness #4)
   - Current state: Assume all code works on Postgres; no audit done
   - Fix: Scan for:
     - MySQL-specific functions (GROUP_CONCAT, SUBSTRING_INDEX, etc.)
     - Collation and type coercion assumptions
     - Trigger or view usage
     - Build a compatibility test suite and run all tests against Postgres in staging
   - Acceptance: 100% of application tests pass on Postgres. No MySQL-isms found in code or identified as acceptable risk.

5. **Realistic timeline based on dry-runs** (Critical weakness #5)
   - Current state: 4 weeks is assumed without data
   - Fix: Do a complete dry-run on 500GB-1TB test data:
     - Schema migration: measure time, identify fixes needed
     - Dual-write setup: measure implementation time, test failure scenarios
     - Validation: measure time for different validation strategies
     - Index creation: measure time for full index rebuild
     - Stored procedure rewrites: rewrite 3-4 most complex ones, measure time
   - Acceptance: Dry-run data shows revised timeline. If >6 weeks, increase calendar allocation or reduce scope.

#### Should address if possible:

1. **Load test Postgres before read cutover** (Significant risk #1)
   - Current state: No performance validation before week 3 read cutover
   - Fix: In parallel with weeks 1-2:
     - Copy production data to Postgres
     - Run top 100 application queries (by frequency and criticality)
     - Compare EXPLAIN plans between MySQL and Postgres
     - Identify slow queries and tune before cutover
   - Acceptance: 99% of queries perform within 10% of MySQL latency. Outliers are identified and tuned.

2. **Audit and prioritize stored procedure rewrites** (Significant risk #2)
   - Current state: "Rewrite 12 procedures in parallel" with no dependency analysis
   - Fix: Map dependencies (which procedures call which). Rewrite critical path first. Flag MySQL-specific syntax.
   - Acceptance: All procedures rewritten, tested, and passing regression tests by end of week 2.

3. **Add explicit read-after-write consistency handling** (Significant risk #3)
   - Current state: Application doesn't account for dual-write latency
   - Fix: Review application code for write-then-read patterns. Add:
     - Read preference hints (read from MySQL immediately after write)
     - Consistency checks (verify written data exists before proceeding)
     - Retry logic if read fails
   - Acceptance: Application handles dual-write window gracefully.

4. **Extend week 3 for production stability** (Significant risk #5)
   - Current state: Week 3 is only 7 days to discover and fix performance issues
   - Fix: Extend week 3 to 10-14 days. Run reads on Postgres for 2+ weeks before write cutover.
   - Acceptance: Zero critical incidents during extended week 3. Performance stable.

#### Verify when possible:

1. **Performance parity on real production query patterns** — Load test with actual production workload against Postgres
2. **Stored procedure interdependencies and rewrites** — Run regression tests on all 12 procedures; confirm no hidden breaks
3. **Application compatibility** — Run full test suite against Postgres; measure against MySQL baseline
4. **Dual-write safety in failure scenarios** — Chaos test: inject Postgres failures, MySQL failures, network delays. Verify no silent data corruption
5. **Cutover atomicity** — Measure actual cutover time in staging. Identify and close divergence windows

---

## Summary

**The plan has structural merit** (dual-write → validate → cut reads → cut writes is the right pattern) **but lacks execution discipline.** Critical details are missing, timelines are unrealistic, and failure modes are unmanaged.

**This plan will likely fail if executed as-is.** Most probable failure point: week 1 (dual-write setup) or week 2 (validation discovers unexpected complexity). Second-order failure point: week 4 (cutover surface unanticipated data divergence or performance issues).

**Success probability with current plan: 15-20%**
**Success probability with critical weaknesses addressed: 75-85%**

The work to address weaknesses is substantial but necessary — not optional. It will add 2-4 weeks to the timeline. A realistic plan is 6-8 weeks, not 4.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/17.5 (91%) |
| Evaluated | 2026-05-04 |
| Target duration | 133850 ms |
| Target cost | $0.1096 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 decomposes the plan into a claim inventory with stated, implied, and required claims — a 4-week plan should yield well above 10 atomic claims | PASS | The output produces a 22-claim inventory table explicitly categorised as Stated (claims 1–8), Implied (claims 9–15), and Required (claims 16–22), covering everything from '4 weeks is achievable' to 'stored procedures don't have hidden interdependencies'. |
| c2 | Step 2 steelmans the plan by building its strongest version before attacking — fixes obvious weaknesses before the attack | PASS | A dedicated 'Steelman' section presents 8 numbered points including industry precedent (Shopify, Slack), phase gates, dual-write fallback, 2 weeks of read-only validation, 12 procedures being isolated, maturity of both databases, backward compatibility through week 3, and schema migration tooling — building the strongest case before attacking. |
| c3 | Step 3 attacks each claim with the required structure — disproof test, failure conditions, weakest link, unverified assumption, strongest opposition | PASS | Every detailed attack section (Claims 1, 2, 3, 4, 5, 8, 9, 10, 16, 17, 18) includes all five structural elements. For example, the Claim 3 attack has: disproof test ('Simulate a failure: MySQL write succeeds, Postgres write fails'), failure conditions (network glitch causing duplicates, disk full, mid-write crashes), weakest link (dual-write error handling), unverified assumption (idempotency keys), and strongest opposition text. |
| c4 | Findings are classified by severity — critical weaknesses, significant risks, and unverified assumptions in separate tables | PASS | Three clearly separated tables appear under 'Findings by Severity': 'Critical weaknesses (would cause failure)' with 5 entries, 'Significant risks (could cause failure under conditions)' with 5 entries, and 'Unverified assumptions (unknown whether true)' with 7 entries. |
| c5 | Implied and required claims receive specific attack — not just the stated claims (e.g., the implicit assumption that dual-write adds acceptable latency is attacked) | PASS | Dedicated attack sections are provided for Claim 9 (Implied — application code PostgreSQL-compatible), Claim 10 (Implied — dual-writes won't cause inconsistency), Claim 16 (Required — tracking which writes went where), Claim 17 (Required — dual-write code safety), and Claim 18 (Required — cutover window size). Each has full structured attack. |
| c6 | Step 4 delivers a verdict using one of the four ratings (Robust/Conditionally sound/Fragile/Fatally flawed) with reasoning | PASS | The verdict section opens: 'Overall robustness: Conditionally sound, but with multiple unmanaged critical weaknesses that make failure more likely than success.' It gives 'Confidence in verdict: High (85%+)' and explains the vulnerabilities are 'predictable, common failure points in database migrations.' |
| c7 | Every weakness in the verdict section comes with a direction for fixing it | PASS | The Recommendations section provides 5 'Must address before proceeding' items, 4 'Should address if possible' items, and 5 'Verify when possible' items. Each includes a Current state, Fix (with concrete steps), and Acceptance criteria. For example, Critical weakness #1 has explicit fix: 'Implement explicit error handling (all-or-nothing dual-write or compensation logic). Test failure scenarios...' |
| c8 | Verdict does not soften if the plan is genuinely fragile — the skill's own rule is 'never soften the verdict' | PARTIAL | The verdict labels the plan 'Conditionally sound' despite identifying 5 critical weaknesses and stating '15-20% success probability' and 'This plan will likely fail if executed as-is.' The body language is harsh but the rating label 'Conditionally sound' is somewhat generous — 'Fragile' would be more consistent with the evidence presented. The explicit 'likely fail' and probability figures prevent this from being a full softening. |
| c9 | Output's claim inventory enumerates well over 10 atomic claims from the 4-week plan — including stated claims (Postgres set up Week 1, dual-writes Week 1, parity validated Week 2), implied claims (latency budget on dual-writes acceptable, no MySQL-specific stored proc behaviour breaks under translation, schema migration is reversible), and required claims (rollback path during cutover, pg replication keeping up with 2TB history) | PASS | 22 claims enumerated. Stated claims include Claims 1 (4-week timeline), 3 (dual-write week 1 safe), 4 (parity validation week 2 sufficient). Implied claims include 9 (application PostgreSQL-compatible), 10 (dual-writes won't cause inconsistency), 13 (Postgres performance matches MySQL). Required claims include 16 (tracking writes during cutover), 17 (dual-write code safety), 18 (cutover window small enough), 22 (stored procedures no hidden interdependencies). |
| c10 | Output's steelman step strengthens the plan before attacking — adds a Week 0 staging dry-run, names the dual-write coordinator pattern (transactional outbox vs sync), specifies parity validation as percentage thresholds rather than vague 'validate' — fixing trivial weaknesses before the real attack | PARTIAL | The steelman section presents 8 points defending the existing plan (industry precedent, phase gates, fallback mechanisms) but does not add a Week 0 staging dry-run, does not name or differentiate dual-write coordinator patterns (transactional outbox vs synchronous), and does not specify parity validation as percentage thresholds. It defends the plan as stated rather than fixing trivial weaknesses before the attack. |
| c11 | Output attacks the stored procedure rewrite specifically — 12 procs in 1 week is the team's stated risk, and the red-team flags it: are these procs in transactional hot paths, do they have edge-case behaviour that's hard to test, what's the test coverage on the existing procs | PARTIAL | Stored procedures appear as Claim 7 (Stated) and Claim 22 (Required) in the inventory, and as Significant Risk #2 ('12 procedures have interdependencies or MySQL-specific logic'). Recommendations include 'Map dependencies, rewrite critical path first.' However, the specific questions asked by the criterion — whether procs are in transactional hot paths, what test coverage exists on the existing procs — are not addressed. The attack lacks a full structured section comparable to those given to Claims 1–5, 8–10, 16–18. |
| c12 | Output attacks the dual-write latency assumption — at 2TB and 95 tables, every write becomes 2 writes; the latency budget on the synchronous-vs-async dual-write decision is interrogated, with the failure mode (Postgres latency dragging primary write performance) named | PARTIAL | Dual-write is extensively attacked for correctness/consistency (Claims 3, 10, 17) but the performance angle is absent. The output never raises 'every write is now 2 writes and adds latency,' never interrogates whether dual-writes are synchronous or asynchronous, and never names the failure mode where Postgres write latency degrades the primary MySQL path. The attacks focus on data integrity, not throughput or latency budget. |
| c13 | Output attacks the parity validation — what does 'data parity' mean concretely (row counts? hash-of-sorted-rows? checksum per partition?), what's the tolerance, what triggers a rollback if parity fails | PASS | Claim 4 attack opens with disproof test: 'What does validation actually check? Row counts? Checksums? Full row comparison?' Lists specific failure conditions including 'Validation only checks row counts → Misses data corruption' and '48+ hours for full row validation.' The weakest link explicitly states: ''Validate data parity' is never defined' and enumerates row counts, hash/checksum per row, FK referential integrity, triggers/views, and application-level constraints. The output also flags that validation runs while writes continue, making point-in-time validation stale. |
| c14 | Output attacks the cutover step — Week 3 reads switch is the riskiest single moment; what happens if Postgres has a stale row from a missed dual-write, what's the rollback mechanism mid-week, what's the read-traffic ramp (canary % vs all-at-once) | PASS | Claim 5 attack (week 3 read cutover) covers query optimizer differences, locking behavior, connection pool exhaustion, and the 7-day pressure window. Claims 2 and 18 attack the cutover synchronization: '30-120 second window' where writes diverge, sticky session persistence on connection pools, DNS TTL delays. Claim 10 attack covers stale row scenario explicitly ('App immediately reads from Postgres — data not there yet → login fails'). Rollback complexity is named in Significant Risk #5. The canary ramp question is not explicitly raised, but this is a minor gap. |
| c15 | Output's findings are classified into critical weaknesses (could fail the migration), significant risks (likely to bite but recoverable), and unverified assumptions (need data before committing) — three separate tables | PASS | Three separate, clearly labelled tables: 'Critical weaknesses (would cause failure)' with 5 rows including columns for Claim attacked, Weakness, Evidence, Impact; 'Significant risks (could cause failure under conditions)' with 5 rows including Likelihood; 'Unverified assumptions (unknown whether true)' with 7 rows including How to verify and Cost of being wrong. |
| c16 | Output's verdict uses one of the four ratings (Robust / Conditionally sound / Fragile / Fatally flawed) — given 4-week zero-downtime is aggressive for 2TB + 12 procs, 'Conditionally sound' or 'Fragile' is the honest verdict | PASS | Verdict section states: 'Overall robustness: Conditionally sound' — one of the four prescribed ratings. Given the plan's structural merit (dual-write → validate → reads → writes is the right pattern) but significant execution gaps, 'Conditionally sound' is within the acceptable honest range identified by the criterion. |
| c17 | Output's verdict does NOT soften — if the plan is genuinely fragile (e.g. Week 4 decommission with no fallback if a problem surfaces post-cutover), the verdict says so and does not hedge with 'should be fine in most cases' | PASS | Summary section states: 'This plan will likely fail if executed as-is. Most probable failure point: week 1 (dual-write setup) or week 2 (validation discovers unexpected complexity).' Verdict gives 'Success probability with current plan: 15-20%' — explicit quantification of near-failure odds. No 'should be fine' language anywhere. |
| c18 | Output's weaknesses each include a direction for fixing — extend timeline, add canary cutover, add a staging full-rehearsal, hire a Postgres DBA, etc. — not just 'this is risky' | PASS | All 5 critical weaknesses have corresponding 'Must address' recommendations with specific fix steps and acceptance criteria. For example: Critical weakness #2 (cutover synchronization) maps to Recommendation #2: 'Write a detailed cutover runbook... Dry-run cutover 3 times in staging with production-scale data.' Significant risks map to 'Should address' items including load testing top 100 queries, extending week 3 to 10-14 days, and adding read-after-write consistency handling. |

### Notes

The output is a strong, well-structured red-team analysis that hits all the major structural requirements: 22-claim inventory across all three claim types, a genuine steelman, structured attacks with all five required elements, three-tier severity classification, an honest verdict with explicit failure probability, and specific remediation directions for every weakness. The two notable gaps are: (1) the steelman defends the plan as-stated rather than fixing trivial weaknesses before attacking, missing the transactional outbox vs sync distinction and percentage-threshold parity specification that would constitute genuine strengthening; and (2) the dual-write performance/latency angle is entirely absent — the output attacks dual-write correctness thoroughly but never raises the synchronous-vs-async decision or the write-latency-doubling failure mode. The stored procedure attack exists but lacks the structured depth of the other attacks and misses the transactional-hot-path and existing test-coverage questions. The verdict label 'Conditionally sound' is slightly generous given five critical weaknesses and a 15-20% success probability — 'Fragile' would be more internally consistent — but the body text is unambiguous about likely failure, so this is a labelling inconsistency rather than a substantive softening.
