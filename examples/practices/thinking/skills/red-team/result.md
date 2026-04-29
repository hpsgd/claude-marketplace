# Red team migration plan attack

An engineering team has decided to migrate their MySQL database to PostgreSQL over a 4-week window with zero downtime. They want the plan stress-tested before they start.

## Prompt

> /red-team Our plan: migrate from MySQL to PostgreSQL in 4 weeks with zero downtime. Week 1 — set up Postgres and run dual-writes. Week 2 — validate data parity. Week 3 — cut reads over to Postgres. Week 4 — cut writes and decommission MySQL. We have 2TB of data, 95 tables, 12 stored procedures. Main risk we've identified is the stored procedure rewrite.

## Output

### Red Team: MySQL → PostgreSQL 4-week zero-downtime migration

#### Claim Inventory

| # | Claim | Type | Confidence |
|---|---|---|---|
| 1 | Migration can be completed in 4 weeks | Stated | Asserted |
| 2 | Zero downtime is achievable | Stated | Asserted |
| 3 | Week 1 dual-writes will capture all data changes | Stated | Unknown |
| 4 | Data parity validation is completable in one week | Stated | Unknown |
| 5 | Week 3 read cutover is safe after parity validation | Stated | Medium |
| 6 | Week 4 write cutover and decommission can happen together | Stated | Low |
| 7 | 12 stored procedures can be rewritten alongside migration | Implied | Unknown |
| 8 | Dual-write adds acceptable latency overhead | Implied | Unknown |
| 9 | All 95 tables have equivalent PostgreSQL column types | Implied | Unknown |
| 10 | Application can connect to two databases simultaneously | Required | Unknown |
| 11 | 2TB can be replicated without degrading production | Required | Unknown |
| 12 | MySQL-specific types (ENUM, TINYINT, JSON) map cleanly | Required | Unknown |
| 13 | Team has sufficient PostgreSQL operational expertise | Required | Low |
| 14 | Rollback is possible at each phase boundary | Required | Unknown |
| 15 | Parity validation catches semantic differences, not just row counts | Required | Unknown |
| 16 | No competing incidents in the 4-week window | Required | Unknown |

16 claims — well above the 10-claim floor.

---

#### Steelman

The strongest case for this plan:

1. The phased approach (dual-write → parity → read cutover → write cutover) is textbook zero-downtime migration practice used successfully at Stripe and GitHub.
2. Separating read and write cutover reduces blast radius — problems on the read path don't affect write durability.
3. Week 2 parity validation creates an explicit go/no-go gate. Most migration failures happen when this step is skipped.
4. Starting dual-write in Week 1 means PostgreSQL accumulates real production data before any traffic routes to it.
5. Identifying stored procedures upfront shows awareness of where complexity lives — this is the hardest part and is scoped at 12 procedures.
6. A 4-week window is aggressive but not unreasonable for a team that has done this kind of work before.

Best available evidence: This migration pattern is documented in Brandur Leach's (Stripe) public writing on Postgres migrations. The key differentiator between success and failure is the parity validation gate.

Strongest framing: The plan has the right architecture. The risks are execution-level detail within each phase, not the overall structure.

---

#### Attack Findings

**Attack: Claim #8 — "Dual-write adds acceptable latency overhead"**

- Disproof test: Measure p99 write latency under peak load with dual-write active. If p99 increases >20%, this claim fails.
- Failure conditions: Synchronous dual-write doubles write latency on every write path. Checkout, payment, and inventory writes will feel this first.
- Weakest link: No mention of whether dual-writes are synchronous or async. Synchronous adds latency; async risks divergence.
- Unverified assumption: Application write latency SLAs absorb the dual-write overhead.
- Strongest opposition: A synchronous dual-write at peak traffic produces user-visible timeouts even if average latency is fine. P99 can be 3-5x worse than mean.

**Attack: Claim #11 — "2TB can be replicated without degrading production"**

- Disproof test: Monitor MySQL CPU and IOPS during initial bulk sync. If production p95 increases >15%, this fails.
- Failure conditions: 2TB initial sync on the same host competes with production reads. Sync IO is unbounded unless throttled.
- Weakest link: No mention of when the initial sync happens or whether it is throttled.
- Unverified assumption: MySQL host has spare IO capacity for a full logical replication stream during business hours.
- Strongest opposition: 2TB at typical replication speeds takes 6–20 hours. A business-hours sync will visibly degrade production.

**Attack: Claim #15 — "Parity validation catches semantic differences"**

- Disproof test: Run column-level checksum comparison, not just row count. If only row counts are checked, this claim fails.
- Failure conditions: MySQL and PostgreSQL differ on NULL comparisons, timezone storage, float arithmetic, and case sensitivity in string comparisons. Row count parity does not equal semantic equivalence.
- Weakest link: "Validate data parity" is unspecified — the validation method is unknown.
- Unverified assumption: The team's validation scope covers semantic drift, not just structural drift.
- Strongest opposition: Migrations have passed row-count validation and then surfaced incorrect financial aggregates post-cutover due to float handling differences between engines.

**Attack: Claim #2 — "Zero downtime is achievable"**

- Disproof test: If the application requires a restart to change DATABASE_URL, there is a downtime window.
- Failure conditions: Most applications require a process restart to change connection configuration.
- Weakest link: No mention of how the application handles connection switching at write cutover.
- Unverified assumption: The application can switch databases without a deployment restart.
- Strongest opposition: True zero downtime requires application-level zero-downtime deployment capability — a separate engineering requirement the plan does not address.

**Attack: Claim #7 — "12 stored procedures can be rewritten alongside migration"**

- Disproof test: If any stored procedure uses MySQL-only syntax (SIGNAL, GROUP_CONCAT without separator), it cannot translate directly.
- Failure conditions: Procedures developed over years against MySQL-specific behaviour will need behaviour-equivalent rewrites, not mechanical translation.
- Weakest link: No mention of test coverage for stored procedure output equivalence.
- Unverified assumption: The team will have time to test all 12 procedures while also running the migration itself.
- Strongest opposition: Stored procedure rewrites typically take 2–3x longer than estimated due to edge cases only discovered during testing.

---

#### Findings by Severity

**Critical weaknesses** (would cause failure):

| # | Claim attacked | Weakness | Evidence | Impact |
|---|---|---|---|---|
| 1 | #15: Parity validation | Row count only — semantic drift undetected | MySQL/PostgreSQL differ on NULL, timezone, float | Silent data corruption post-cutover |
| 2 | #7: Stored procedure translation | No test coverage specified for any of the 12 procedures | Untested rewrites under time pressure | Silent incorrect results after cutover |
| 3 | #2: Zero downtime | Application restart may be required for DB URL change | Most apps require restart for connection config change | Unplanned downtime at write cutover |

**Significant risks** (could cause failure under conditions):

| # | Claim attacked | Risk | Trigger conditions | Likelihood |
|---|---|---|---|---|
| 1 | #8: Dual-write latency | Synchronous dual-writes double write latency | Peak traffic on latency-sensitive write paths | Medium |
| 2 | #11: Initial 2TB sync | Replication competes with production IO | Business-hours sync, no throttling | High |
| 3 | #13: PostgreSQL expertise | Production incident exposes knowledge gaps | Any incident in Weeks 3–4 when MySQL is degraded | Medium |

**Unverified assumptions**:

| # | Claim attacked | Assumption | How to verify | Cost of being wrong |
|---|---|---|---|---|
| 1 | #9: Type equivalence | All 95 MySQL column types map cleanly | pgloader dry-run against a dump | Data truncation or silent type coercion |
| 2 | #14: Rollback | Rollback is possible at each phase boundary | Write rollback procedures before starting | Irreversible partial migration |
| 3 | #16: Clean window | No competing incidents in 4 weeks | Check release calendar and incident history | Forced pause mid-migration in a split-brain state |

---

#### Verdict

**Overall robustness:** Fragile

**Confidence in verdict:** High — the plan has the right architecture but three critical weaknesses, each capable of independently causing failure without any of the others.

#### Recommendations

**Must address before proceeding:**

1. Parity validation scope — suggested fix: define a validation script that checks row counts AND column-level checksums AND output of key aggregate queries run against both databases simultaneously with identical inputs.
2. Stored procedure test coverage — suggested fix: write input/output test cases for all 12 procedures before translation begins. Run both the MySQL and PostgreSQL versions against identical inputs and compare outputs. Do not cut over until all 12 match.
3. Application restart requirement — suggested fix: verify now whether the application can switch database connections without a restart. If not, plan a brief maintenance window or implement a connection proxy such as PgBouncer.

**Should address if possible:**

1. Dual-write latency — benchmark dual-write overhead in staging under production-equivalent load before Week 1. If synchronous is too slow, implement async with divergence reconciliation.
2. Initial sync scheduling — run the 2TB sync against a replica or during low-traffic hours with IO throttling set.

**Verify when possible:**

1. Type mapping — run a pgloader dry-run from a MySQL dump before committing to dual-write. Check warnings for type coercions.
2. Rollback procedures — document the rollback steps for each phase boundary now, before starting.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.5/18 (97%) |
| Evaluated | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Step 1 decomposes the plan into a claim inventory with stated, implied, and required claims above 10 — the skill's Step 1 defines a claim inventory table with a Type column (Stated/Implied/Required) and states "A plan with 5 sections typically decomposes into 15–25 atomic claims. If you find fewer than 10, you haven't decomposed far enough." The simulated output yields 16 claims across all three types, well above the floor.
- [x] PASS: Step 2 steelmans the plan before attacking — Step 2 is labeled mandatory. The rules require fixing obvious weaknesses and adding best supporting evidence before attacking. The simulated output adds external evidence (Brandur Leach/Stripe), adds the parity gate as an explicit strength, and completes before any attack begins.
- [x] PASS: Step 3 attacks each claim with the required five-part structure — the skill defines exactly five attack vectors per claim: disproof test, failure conditions, weakest link, unverified assumption, strongest opposition. All five appear in each attack section of the simulated output.
- [x] PASS: Findings are classified by severity in three separate tables — Step 3 specifies "Critical weaknesses", "Significant risks", and "Unverified assumptions" as three distinct tables with defined column schemas. The simulated output matches this structure.
- [x] PASS: Implied and required claims receive specific attack — the skill's Rules section states "Implied claims are the richest target. Focus on Required and Implied claims." Claim #8 (dual-write latency — Implied) and claim #7 (stored procedures — Implied) are unstated in the prompt; claims #11 and #15 (Required) are also attacked with full five-part structure.
- [x] PASS: Step 4 delivers a verdict using one of the four defined ratings — the Step 4 template specifies exactly "Robust / Conditionally sound / Fragile / Fatally flawed." The simulated output rates the plan "Fragile" with explicit confidence level and reasoning.
- [x] PASS: Every weakness in the verdict section comes with a direction for fixing it — the skill's Rules section states "Every weakness identified should come with a direction for fixing it." All three critical weaknesses in Recommendations include a "suggested fix" with concrete approach.
- [~] PARTIAL: Verdict does not soften if the plan is genuinely fragile — the rule "Never soften the verdict. If the argument is fatally flawed, say so" is present and explicit in the skill. The plan receives "Fragile" rather than "Fatally flawed." Three critical weaknesses could support "Fatally flawed." However, the steelman established the architecture is sound and gaps are fixable, which arguably makes "Fragile" the honest verdict rather than a softer one. Structural rule is present; runtime compliance cannot be verified without live execution, and the boundary between "Fragile" and "Fatally flawed" here is a judgment call. Scored 0.5.

### Output expectations

- [x] PASS: Output's claim inventory enumerates well over 10 atomic claims — 16 claims produced, covering stated (1–6), implied (7–9), and required (10–16). The skill mandates all three types and flags fewer than 10 as insufficient.
- [x] PASS: Output's steelman strengthens the plan before attacking — adds external evidence (Stripe/Brandur Leach), names the parity gate as the critical success differentiator, and frames the plan's architecture as sound before any attack begins. Fixes the "what parity validation means" ambiguity by naming the gate explicitly.
- [x] PASS: Output attacks the stored procedure rewrite specifically — claim #7 receives a full five-part attack. Flags absence of test coverage, MySQL-specific syntax risk (SIGNAL, GROUP_CONCAT), and the 2–3x underestimation pattern for proc rewrites.
- [x] PASS: Output attacks the dual-write latency assumption — claim #8 is the first dedicated attack. Names synchronous vs async as the key decision, identifies p99 degradation as the failure mode, and flags that the plan does not specify which approach is used.
- [x] PASS: Output attacks the parity validation — claim #15 attacks the unspecified validation method, identifies MySQL/PostgreSQL semantic differences (NULL, timezone, float), and names the failure mode (silent data corruption from row-count-only validation).
- [x] PASS: Output attacks the cutover step — claim #2 attacks the zero-downtime assumption at write cutover. Identifies application restart risk, and the findings table classifies it as a critical weakness capable of independently causing failure.
- [x] PASS: Output's findings use three separate tables — Critical weaknesses (3 entries), Significant risks (3 entries), and Unverified assumptions (3 entries) with all required columns populated.
- [x] PASS: Output's verdict uses one of the four defined ratings — "Fragile" is one of the four valid options and is appropriate given three critical weaknesses on a 4-week zero-downtime migration of 2TB + 12 procs.
- [x] PASS: Output's verdict does not soften — "Fragile" with "High" confidence and explicit statement that "three critical weaknesses, each capable of independently causing failure" is not a hedge. The verdict does not say the plan will probably be fine.
- [x] PASS: Output's weaknesses each include a direction for fixing — all three critical weaknesses in Recommendations name a concrete fix (validation script with checksums, input/output test cases for all 12 procs before translation, connection proxy or maintenance window).

## Notes

The skill's claim taxonomy (Stated/Implied/Required) is its strongest structural element. Directing attack at Required and Implied claims — rather than just what the plan says — is what surfaces the latency budget, the semantic parity gap, and the rollback absence, none of which the team mentioned.

One structural ambiguity worth flagging: Step 3 says "For each claim from Step 1" which implies 16 five-part attacks for this prompt. In practice only the critical claims get full five-part treatment; others surface only in the severity tables. The definition does not explicitly permit selective depth, which creates tension between thoroughness and usability. The authors may want to add language like "prioritise low-confidence, Implied, and Required claims for full five-part treatment" to make selective depth explicit rather than implied.
