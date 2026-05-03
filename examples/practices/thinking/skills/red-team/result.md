# Red Team

Scenario: An engineering team has decided to migrate their MySQL database to PostgreSQL over a 4-week window with zero downtime. They want the plan stress-tested before they start.

## Prompt

> /red-team Our plan: migrate from MySQL to PostgreSQL in 4 weeks with zero downtime. Week 1 — set up Postgres and run dual-writes. Week 2 — validate data parity. Week 3 — cut reads over to Postgres. Week 4 — cut writes and decommission MySQL. We have 2TB of data, 95 tables, 12 stored procedures. Main risk we've identified is the stored procedure rewrite.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Red Team: MySQL → PostgreSQL Migration (4 weeks, zero downtime)

---

### Claim Inventory

| # | Claim | Type | Confidence |
|---|---|---|---|
| 1 | Zero downtime is achievable | Stated | High |
| 2 | 4 weeks is sufficient for this migration | Stated | High |
| 3 | Dual-writes can be implemented in Week 1 | Stated | Medium |
| 4 | Dual-writes will not degrade production performance | Implied | High |
| 5 | Data parity validation is completable in one week | Stated | Medium |
| 6 | Parity validation will catch all inconsistencies | Implied | Medium |
| 7 | Reads can be safely cut over in Week 3 | Stated | Medium |
| 8 | Reads and writes can be split independently | Required | Unstated |
| 9 | The application layer can be made database-agnostic enough to route reads/writes separately | Required | Unstated |
| 10 | Stored procedures are the main migration risk | Stated | Medium |
| 11 | The 12 stored procedures can be rewritten in time | Implied | Medium |
| 12 | MySQL and PostgreSQL semantic equivalence is achievable | Required | Unstated |
| 13 | 2TB can be replicated without impacting production | Implied | Medium |
| 14 | Rollback is possible at each stage | Implied | High |
| 15 | Week 4 decommission of MySQL is safe after one week of Postgres-only writes | Implied | Medium |
| 16 | The team has sufficient PostgreSQL expertise to execute this | Required | Unstated |
| 17 | Schema differences between MySQL and PostgreSQL are handled | Required | Unstated |
| 18 | All 95 tables have been audited for compatibility issues | Required | Unstated |
| 19 | Transaction semantics are equivalent between both systems | Required | Unstated |
| 20 | Application connection pool and ORM configuration works correctly on both | Required | Unstated |
| 21 | External integrations (reporting, ETL, analytics) can tolerate the migration | Required | Unstated |
| 22 | The dual-write mechanism handles failures atomically | Required | Unstated |

---

### Steelman

The strongest case for this plan:

1. **Dual-write is industry-proven.** Companies including GitHub, Stripe, and Shopify have used dual-write + read cutover patterns successfully. The staged approach is correct in principle.
2. **4 weeks is aggressive but not absurd** for a team with tooling (AWS DMS, pgloader, or similar) already in use. 95 tables and 12 procs isn't enormous.
3. **Separating read and write cutover reduces blast radius.** If Postgres reads fail, you haven't lost write continuity. The sequencing is logical.
4. **Stored procedure risk is correctly identified early.** Naming it upfront means it gets resourcing. It's better to surface it now than discover it in Week 3.
5. **2TB is large but not unusually large** — with logical replication or DMS, initial load + CDC is standard. AWS DMS handles this at scale routinely.
6. **Decommissioning MySQL in Week 4 preserves motivation** to complete the migration rather than letting dual-write drag on indefinitely.
7. **Read-only Postgres validation in Week 3** before any write cutover limits write-path risk exposure.
8. **Zero-downtime is structurally possible** — no hard technical barrier prevents it if dual-write and replication are correctly implemented.

**Best available evidence:** Netflix, GitHub, and dozens of documented migrations confirm this pattern works. The risk is execution quality, not architectural validity.

---

### Attack Findings

**Critical weaknesses** (would cause failure):

| # | Claim attacked | Weakness | Evidence | Impact |
|---|---|---|---|---|
| 1 | #22 — dual-write handles failures atomically | Dual-write across two separate databases cannot be atomic without distributed transactions. A write succeeds in MySQL and fails in Postgres (or vice versa) on every network hiccup, lock timeout, or constraint violation — silently diverging the two. | Two-phase commit across MySQL + Postgres requires XA transactions, which most ORMs don't support and adds latency spikes. Without it, divergence is guaranteed under load. | Data corruption in Postgres that isn't caught until Week 2 — at which point the parity gap may be too large to reconcile in one week. |
| 2 | #12 — MySQL and PostgreSQL semantic equivalence | MySQL and Postgres differ on: `NULL` handling in `GROUP BY`, `ONLY_FULL_GROUP_BY`, case sensitivity in string comparisons (MySQL case-insensitive by default), `AUTO_INCREMENT` vs sequences, `TINYINT(1)` as boolean, `DATETIME` vs `TIMESTAMP` timezone behaviour, `0000-00-00` dates that are illegal in Postgres, `ENUM` types, and implicit type coercions. With 95 tables, hitting at least one production-breaking semantic difference is near-certain. | MySQL's default `utf8` charset is actually `utf8mb3` (3-byte), causing failures on 4-byte emoji/Unicode in Postgres's true `utf8mb4`. | Silent wrong-answer queries in Postgres that pass parity checks because the test data doesn't cover the edge case. Application bugs surface after Week 4 decommission when rollback is no longer available. |
| 3 | #8/#9 — reads and writes can be split independently | If the application uses a single ORM connection string, a single connection pool, or has any implicit "read your own writes" pattern (writing then immediately reading in the same request), splitting reads to Postgres while writes go to MySQL will break consistency. Reads on Postgres may return stale data from before replication lag catches up. | Replication lag on a 2TB dataset under write load is not negligible — even 100ms of lag breaks "read your own writes" for any user-facing feature. | User-visible data loss (writes appear to vanish) and race conditions that only manifest under load in Week 3, which is the worst possible time. |
| 4 | #15 — one week of Postgres-only writes is sufficient before decommission | One week of production write load does not surface slow-burning issues: end-of-month batch jobs, quarterly reports, weekly aggregations, or infrequent code paths. Decommissioning MySQL in Week 4 eliminates rollback permanently. | Many production incidents only emerge after 30–60 days when infrequent jobs run. One week of "clean" operation is insufficient evidence of correctness. | Catastrophic, unrecoverable data loss after MySQL is gone and a previously-untested code path hits Postgres. |

**Significant risks** (could cause failure under conditions):

| # | Claim attacked | Risk | Trigger conditions | Likelihood |
|---|---|---|---|---|
| 1 | #4 — dual-writes don't degrade production | Dual-write doubles write latency in the synchronous path. 2x write latency at p99 may breach SLAs or cause timeouts cascading upstream. | Any write-heavy traffic spike during Week 1, especially if Postgres is slower than MySQL on initial cold data (no warm buffer pool). | High — almost certain to show up in monitoring; question is whether it's tolerable. |
| 2 | #13 — 2TB initial replication doesn't impact production | Initial bulk load of 2TB reads from MySQL at high I/O. Depending on instance type, this competes with production read queries. | MySQL running on storage-bounded instances (RDS with provisioned IOPS), or initial load scheduled during a traffic peak. | Medium — often underestimated. mysqldump/pgloader on 2TB can run 12–24 hours and saturate I/O. |
| 3 | #5/#6 — parity validation is complete in one week | Parity validation of 2TB across 95 tables is not a one-week project if done rigorously. Naive row-count checks will miss: column-level corruption, NULL vs empty-string coercion differences, timezone-shifted timestamps, and floating-point rounding differences. | Any semantic difference from Claim #12 that isn't explicitly tested. | High — a thorough parity check on 2TB takes weeks, not days, unless the tooling is already built. |
| 4 | #11 — 12 stored procedures rewritten in Week 1 | Stored procedures often embed MySQL-specific syntax: `DELIMITER`, `IFNULL`, `GROUP_CONCAT`, `INSERT IGNORE`, `ON DUPLICATE KEY UPDATE`, `LIMIT` in subqueries, and transaction semantics that differ. If any proc is central to a high-traffic path, a subtle rewrite bug is a production incident. | Any proc that uses MySQL-specific aggregate functions or conditional logic (`IF()` vs `CASE`). | High — 12 procs with MySQL-specific idioms is the expected case, not the exception. |
| 5 | #21 — external integrations can tolerate migration | BI tools, ETL pipelines, analytics databases, data warehouses, and monitoring agents that connect directly to MySQL (not through the app) are not addressed in the plan at all. These may use MySQL-specific SQL dialect, rely on binlog for CDC, or have hardcoded connection strings. | Any external system that reads directly from MySQL's binlog (Debezium, Canal, Maxwell) — the replication stream changes completely in Postgres (logical replication / pgoutput). | Medium-High — 2TB and 95 tables implies a mature system that almost certainly has downstream consumers. |

**Unverified assumptions** (unknown whether true):

| # | Claim attacked | Assumption | How to verify | Cost of being wrong |
|---|---|---|---|---|
| 1 | #16 — team has PostgreSQL expertise | Does the team know Postgres's MVCC behaviour, `VACUUM`, index types (GIN vs GiST vs BRIN), connection pooler requirements (PgBouncer), and operational differences from MySQL? | Ask directly: who has run Postgres in production before? | High — operational surprises (table bloat, transaction ID wraparound, autovacuum blocking) hit production weeks after migration, not during it. |
| 2 | #14 — rollback is possible at each stage | Is there a documented, tested rollback plan for each week? "MySQL still running" is not a rollback plan — it requires tested failback procedures, connection string switches, and data reconciliation for any writes that landed in Postgres during Week 3–4. | Write and dry-run the rollback procedure before starting Week 1. | High — without a tested rollback, "zero downtime" becomes "no planned downtime but potentially very long unplanned downtime." |
| 3 | #17/#18 — schema differences audited | Has the schema been run through a compatibility checker (pgloader dry-run, AWS SCT report, or manual audit)? Foreign keys with `ON DELETE SET DEFAULT` (not supported in Postgres pre-14), check constraints, expression defaults, and virtual columns all differ. | Run `pgloader` or AWS SCT in dry-run mode against a schema dump. | Medium-High — schema incompatibilities block the initial load, compressing the already-tight Week 1 timeline. |
| 4 | #19 — transaction semantics are equivalent | MySQL's default isolation level is `REPEATABLE READ`; PostgreSQL's is also `REPEATABLE READ` but the implementation differs (Postgres uses MVCC, MySQL uses locking). Queries that rely on MySQL's locking behaviour (e.g., `SELECT ... FOR UPDATE` interactions with phantom reads) may behave differently. | Review all transactions that use explicit locking or isolation levels. | Medium — affects correctness of financial or inventory-type operations. |

---

### Verdict

**Overall robustness: Fragile**

**Confidence in verdict: High** — because three of the four critical weaknesses are structural (not execution quality issues) and at least two of them — dual-write non-atomicity and MySQL/Postgres semantic divergence — are near-certain to manifest on a 2TB, 95-table production system. The plan's timeline compresses the points where these failures surface (parity validation, read cutover) into windows too short to catch and fix them before the next stage begins.

The plan is *architecturally correct in skeleton* but *dangerously under-specified in the areas that actually fail migrations*. The identified risk (stored procedure rewrite) is real but is the third or fourth most dangerous item on this list, not the first.

---

### Recommendations

**Must address before proceeding:**

1. **Dual-write divergence handling** — define the consistency model explicitly: will dual-writes be fire-and-forget to Postgres (async, with reconciliation) or synchronous? If synchronous, what's the failure mode when Postgres rejects a write MySQL accepted? Build a divergence detector that runs continuously in Week 1–3 and alerts on row-level mismatches in near-real-time, not just end-of-week batch checks.

2. **MySQL→Postgres semantic audit** — run AWS Schema Conversion Tool or pgloader in dry-run mode across all 95 tables *before* Week 1 starts. Produce a compatibility report. Any table with `0000-00-00` dates, `TINYINT(1)` booleans used ambiguously, case-sensitive string comparisons, or `ENUM` columns needs a migration strategy defined upfront, not discovered during parity validation.

3. **Read-your-own-writes analysis** — map every request flow that writes then reads in the same transaction or request. These flows break when reads go to Postgres before replication lag is zero. Either keep these flows on MySQL through Week 3 or implement synchronous replication with lag monitoring before cutting over reads.

4. **Tested rollback procedures** — write and execute a rollback drill for each week before the migration begins. The Week 4 rollback (after MySQL decommission) should be treated as "there is no rollback" — which means the MySQL decommission gate should require at least 30 days of clean Postgres operation, not 7.

**Should address if possible:**

1. **External integration audit** — catalogue every system connecting directly to MySQL (BI tools, ETL, CDC pipelines, monitoring). Each needs its own cutover plan. Binlog-based CDC consumers (Debezium etc.) need to switch to Postgres logical replication — that's a separate project.

2. **Postgres operational readiness** — ensure the team has run autovacuum tuning, connection pooling (PgBouncer), and bloat monitoring before go-live. PostgreSQL operational failure modes are different from MySQL's and surprise teams that migrate without operational prep.

3. **Extend the timeline** — 4 weeks for 2TB / 95 tables / zero downtime is achievable but leaves no margin. One unexpected semantic incompatibility in Week 2 consumes the entire buffer. 6–8 weeks with the same structure dramatically improves the probability of success without changing the architecture.

**Verify when possible:**

1. **Parity validation tooling** — confirm the team has (or will build) column-level comparison, not just row counts. Tools like `data-diff` (open source) handle this at scale. Validate the tooling itself on a representative sample before Week 2.

2. **Write latency under dual-write** — load-test dual-write on a staging environment before enabling in production. Measure p95 and p99 write latency. If it exceeds current SLAs, the Week 1 plan needs to change (async dual-write with lag tolerance instead of synchronous).

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.5/17.5 (89%) |
| Evaluated | 2026-05-01 |
| Target duration | 89368 ms |
| Target cost | $0.0992 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 decomposes the plan into a claim inventory with stated, implied, and required claims — a 4-week plan should yield well above 10 atomic claims | PASS | The output presents a 22-row claim inventory table with columns for Type (Stated/Implied/Required) and Confidence. Examples: claim #1 'Zero downtime is achievable' (Stated), #4 'Dual-writes will not degrade production performance' (Implied), #8 'Reads and writes can be split independently' (Required). |
| c2 | Step 2 steelmans the plan by building its strongest version before attacking — fixes obvious weaknesses before the attack | PASS | A dedicated 'Steelman' section with 8 numbered arguments appears before the Attack Findings. It argues the pattern is industry-proven (GitHub, Stripe, Shopify), that 4 weeks is 'aggressive but not absurd,' and that 2TB 'is large but not unusually large.' Culminates with 'Zero-downtime is structurally possible — no hard technical barrier prevents it.' |
| c3 | Step 3 attacks each claim with the required structure — disproof test, failure conditions, weakest link, unverified assumption, strongest opposition | PARTIAL | Attack findings are rigorous and adversarial but use a different per-entry structure than the five named elements (disproof test, failure conditions, weakest link, unverified assumption, strongest opposition). Critical weaknesses use: Claim attacked / Weakness / Evidence / Impact. Significant risks use: Risk / Trigger conditions / Likelihood. Unverified assumptions use: Assumption / How to verify / Cost of being wrong. The content is adversarial but the named five-element per-claim structure is not followed. |
| c4 | Findings are classified by severity — critical weaknesses, significant risks, and unverified assumptions in separate tables | PASS | Three distinct tables are present: 'Critical weaknesses (would cause failure)' with 4 entries, 'Significant risks (could cause failure under conditions)' with 5 entries, and 'Unverified assumptions (unknown whether true)' with 4 entries. |
| c5 | Implied and required claims receive specific attack — not just the stated claims (e.g., the implicit assumption that dual-write adds acceptable latency is attacked) | PASS | Implied claim #4 ('dual-writes will not degrade production') is attacked in Significant risks row 1: 'Dual-write doubles write latency in the synchronous path. 2x write latency at p99 may breach SLAs.' Required claims #8/#9 (read/write splitting) and #22 (atomic dual-write) are attacked in Critical weaknesses. |
| c6 | Step 4 delivers a verdict using one of the four ratings (Robust/Conditionally sound/Fragile/Fatally flawed) with reasoning | PASS | Verdict section states 'Overall robustness: Fragile' — one of the four required ratings. Reasoning follows: 'three of the four critical weaknesses are structural (not execution quality issues)' and 'dual-write non-atomicity and MySQL/Postgres semantic divergence — are near-certain to manifest on a 2TB, 95-table production system.' |
| c7 | Every weakness in the verdict section comes with a direction for fixing it | PASS | Recommendations section has 'Must address before proceeding' (4 items with specific fixes), 'Should address if possible' (3 items), and 'Verify when possible' (2 items). Examples: 'Run AWS Schema Conversion Tool or pgloader in dry-run mode across all 95 tables before Week 1 starts,' 'write and execute a rollback drill for each week before the migration begins.' |
| c8 | Verdict does not soften if the plan is genuinely fragile — the skill's own rule is "never soften the verdict" | PARTIAL | The verdict says 'Fragile' with 'Confidence in verdict: High' and explicitly states the plan is 'dangerously under-specified.' The verdict does not hedge with phrases like 'should be fine in most cases.' Earns the PARTIAL ceiling. |
| c9 | Output's claim inventory enumerates well over 10 atomic claims from the 4-week plan — including stated claims (Postgres set up Week 1, dual-writes Week 1, parity validated Week 2), implied claims (latency budget on dual-writes acceptable, no MySQL-specific stored proc behaviour breaks under translation, schema migration is reversible), and required claims (rollback path during cutover, pg replication keeping up with 2TB history) | PASS | 22 claims enumerated covering all three types. Stated: #1 'Zero downtime is achievable,' #3 'Dual-writes can be implemented in Week 1,' #5 'Data parity validation is completable in one week.' Implied: #4 latency, #13 '2TB can be replicated without impacting production.' Required: #8 reads/writes can be split, #14 'Rollback is possible at each stage,' #22 'The dual-write mechanism handles failures atomically.' |
| c10 | Output's steelman step strengthens the plan before attacking — adds a Week 0 staging dry-run, names the dual-write coordinator pattern (transactional outbox vs sync), specifies parity validation as percentage thresholds rather than vague "validate" — fixing trivial weaknesses before the real attack | FAIL | The steelman section contains 8 purely defensive arguments ('Dual-write is industry-proven,' '4 weeks is aggressive but not absurd,' etc.) but does NOT add a Week 0 staging dry-run, does NOT name the dual-write coordinator pattern (transactional outbox vs sync), and does NOT specify parity validation as percentage thresholds. The steelman defends the plan as stated rather than strengthening/patching it before attacking. |
| c11 | Output attacks the stored procedure rewrite specifically — 12 procs in 1 week is the team's stated risk, and the red-team flags it: are these procs in transactional hot paths, do they have edge-case behaviour that's hard to test, what's the test coverage on the existing procs | PASS | Significant risks table row 4 attacks claim #11: lists MySQL-specific syntax differences (DELIMITER, IFNULL, GROUP_CONCAT, INSERT IGNORE, ON DUPLICATE KEY UPDATE, LIMIT in subqueries) and states 'If any proc is central to a high-traffic path, a subtle rewrite bug is a production incident.' Likelihood rated 'High.' |
| c12 | Output attacks the dual-write latency assumption — at 2TB and 95 tables, every write becomes 2 writes; the latency budget on the synchronous-vs-async dual-write decision is interrogated, with the failure mode (Postgres latency dragging primary write performance) named | PASS | Significant risks row 1 attacks claim #4: 'Dual-write doubles write latency in the synchronous path. 2x write latency at p99 may breach SLAs or cause timeouts cascading upstream.' Recommendations item 2 further says 'load-test dual-write on a staging environment... If it exceeds current SLAs, the Week 1 plan needs to change (async dual-write with lag tolerance instead of synchronous).' |
| c13 | Output attacks the parity validation — what does "data parity" mean concretely (row counts? hash-of-sorted-rows? checksum per partition?), what's the tolerance, what triggers a rollback if parity fails | PASS | Significant risks row 3 attacks claims #5/#6: 'Naive row-count checks will miss: column-level corruption, NULL vs empty-string coercion differences, timezone-shifted timestamps, and floating-point rounding differences.' Recommendations item under 'Verify' says 'confirm the team has column-level comparison, not just row counts. Tools like data-diff.' Tolerance and rollback trigger not explicitly addressed. |
| c14 | Output attacks the cutover step — Week 3 reads switch is the riskiest single moment; what happens if Postgres has a stale row from a missed dual-write, what's the rollback mechanism mid-week, what's the read-traffic ramp (canary % vs all-at-once) | PARTIAL | Critical weaknesses row 3 attacks claims #8/#9: addresses stale data from replication lag ('Reads on Postgres may return stale data from before replication lag catches up') and read-your-own-writes breakage. However, the output does not address the rollback mechanism mid-week during Week 3, nor the read-traffic ramp strategy (canary percentage vs all-at-once). These specific elements are absent. |
| c15 | Output's findings are classified into critical weaknesses (could fail the migration), significant risks (likely to bite but recoverable), and unverified assumptions (need data before committing) — three separate tables | PASS | Three explicitly labeled separate tables: 'Critical weaknesses (would cause failure)' with 4 rows, 'Significant risks (could cause failure under conditions)' with 5 rows, 'Unverified assumptions (unknown whether true)' with 4 rows. |
| c16 | Output's verdict uses one of the four ratings (Robust / Conditionally sound / Fragile / Fatally flawed) — given 4-week zero-downtime is aggressive for 2TB + 12 procs, "Conditionally sound" or "Fragile" is the honest verdict | PASS | Verdict section opens with 'Overall robustness: Fragile' — one of the four required ratings, and an honest one given the identified structural weaknesses. |
| c17 | Output's verdict does NOT soften — if the plan is genuinely fragile (e.g. Week 4 decommission with no fallback if a problem surfaces post-cutover), the verdict says so and does not hedge with "should be fine in most cases" | PASS | Verdict states 'Confidence in verdict: High' and 'The plan is architecturally correct in skeleton but dangerously under-specified.' Recommendation 4 explicitly says 'the MySQL decommission gate should require at least 30 days of clean Postgres operation, not 7' — treating Week 4 decommission as having no practical rollback. |
| c18 | Output's weaknesses each include a direction for fixing — extend timeline, add canary cutover, add a staging full-rehearsal, hire a Postgres DBA, etc. — not just "this is risky" | PASS | All four 'Must address' items include specific fixes: 'define the consistency model explicitly... build a divergence detector,' 'run AWS Schema Conversion Tool or pgloader in dry-run mode across all 95 tables,' 'map every request flow that writes then reads,' 'write and execute a rollback drill.' 'Should address' and 'Verify' sections similarly prescriptive. |

### Notes

The output is a strong red-team analysis that clearly passes on most criteria. The claim inventory (22 claims) and severity-classified attack tables are well-executed. The verdict is unambiguous and unsoftened. The main gaps are: (1) the steelman section is purely defensive rather than constructively patching obvious weaknesses — it argues the plan is sound rather than adding a Week 0 dry-run, naming dual-write coordinator patterns, or specifying parity thresholds as the criterion expected; (2) the attack structure per claim uses a custom three-table format rather than the named five-element structure (disproof test, failure conditions, weakest link, unverified assumption, strongest opposition); (3) the Week 3 read cutover attack misses the canary ramp strategy and mid-week rollback mechanism. These are genuine gaps but do not undermine the overall quality of the analysis, which correctly identifies dual-write non-atomicity and MySQL/Postgres semantic divergence as the most dangerous risks above the team's stated stored-procedure concern.
