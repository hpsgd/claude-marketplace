# Council

Scenario: A team needs to choose between PostgreSQL and MongoDB for a new event-driven analytics platform. The council skill is invoked to debate the options with multiple competing perspectives.

## Prompt

> /council Should we use PostgreSQL or MongoDB for the new analytics platform? We're storing user behaviour events (high write volume, ~50k events/min at peak), and the data analysts need ad-hoc SQL queries. The engineering team is more comfortable with Postgres but the product manager thinks MongoDB's flexible schema will speed up iteration.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Council: PostgreSQL vs MongoDB for analytics platform (50k events/min, ad-hoc SQL)

---

### Perspectives

---

**The Data Analyst** — PostgreSQL is the only viable choice when ad-hoc SQL is a core requirement.

**Core argument:** Ad-hoc SQL isn't a nice-to-have — it's the entire analytical workflow. Analysts use JOINs, window functions, CTEs, and aggregations that MongoDB's query language can't replicate without a translation layer. Every hour spent working around that limitation is wasted.

**Primary concern:** Analysts blocked waiting for engineers to write aggregation pipelines for every new query pattern.

**What they would sacrifice:** Some schema rigidity on ingest — they'll handle messy event payloads if the query layer is SQL.

---

**The Product Manager (Pragmatist)** — MongoDB's flexible schema cuts time-to-market for new event types.

**Core argument:** Event schemas evolve constantly — new product features add new fields. With Postgres, every new event type means a migration, a PR, review, deploy. With MongoDB, the app just writes the new shape and the schema catches up later. This removes a bottleneck in the product feedback loop.

**Primary concern:** Schema migrations slowing down the product team's ability to instrument new features quickly.

**What they would sacrifice:** The convenience of native SQL — analysts can use a BI tool with a MongoDB connector or an abstraction layer.

---

**The Infrastructure Engineer** — At 50k events/min, the write architecture matters more than schema flexibility.

**Core argument:** 50k events/min is 833 writes/second sustained, with peak spikes likely 2-5x that. Neither Postgres nor MongoDB out-of-the-box handles this without architectural decisions: connection pooling, write buffering, partitioning strategy, index design. The database choice is secondary to the ingestion pipeline design.

**Primary concern:** Picking a database based on schema philosophy, then hitting a wall at peak load because the write path wasn't designed for it.

**What they would sacrifice:** Developer convenience in both directions — they'd rather have a Kafka/buffer layer in front of either database than optimise the wrong thing.

---

**The Skeptic** — Both options are wrong for analytics at this scale; the real answer is a purpose-built analytics store.

**Core argument:** Operational databases — both Postgres and MongoDB — are optimised for transactional workloads. At 50k events/min, analytical queries on an OLTP database will either kill query performance or require read replicas, materialized views, and partitioning that make the schema flexibility argument moot. ClickHouse, BigQuery, or Redshift exist precisely because this problem is solved.

**Primary concern:** Six months from now, analysts complain about slow queries, engineers spend a sprint on read replicas and partitioning, and the team revisits this decision under pressure.

**What they would sacrifice:** Simplicity now, to avoid a painful migration later.

---

### Debate

---

**The Data Analyst responds**

**Agrees with The Skeptic on:** purpose-built analytics stores being superior for query performance — ClickHouse's columnar storage would make aggregations dramatically faster.

**Disagrees with The Product Manager on:** the migration burden claim — Postgres JSONB columns handle semi-structured event payloads without schema migrations. You get flexible ingest *and* SQL. This directly undercuts the PM's core argument.

**What The Product Manager is missing:** Most BI tools that "support MongoDB" do so via an SQL translation layer (e.g., MongoDB Atlas SQL Interface) that is slower, less capable, and harder to debug than native SQL. Analysts will feel that gap.

**Strongest concession:** The Skeptic is right that this may be the wrong layer entirely. If the analytics volume warrants a purpose-built store, I'd rather have ClickHouse with native SQL than Postgres under strain.

---

**The Product Manager responds**

**Agrees with The Infrastructure Engineer on:** the write pipeline mattering more than the database brand — a Kafka buffer in front of either database solves the ingest problem cleanly.

**Disagrees with The Data Analyst on:** JSONB as a solution to schema flexibility — JSONB queries are slower, indexes on nested fields are complex, and schema discovery in JSONB columns is painful for analysts who need to understand what fields exist. It's a workaround, not a solution.

**What The Infrastructure Engineer is missing:** The engineering team's familiarity with Postgres is an operational asset. Introducing ClickHouse or a new OLAP store adds operational burden — backup, monitoring, replication, ops expertise. That cost is real.

**Strongest concession:** The Skeptic's point lands. If this platform is genuinely analytics-first (not a dual OLTP/analytics workload), then optimising on Postgres vs MongoDB schema flexibility is debating deck chairs. The right tool is probably neither.

---

**The Infrastructure Engineer responds**

**Agrees with The Skeptic on:** the fundamental mismatch between OLTP databases and analytical query patterns — window functions over 500M event rows on Postgres will require careful partitioning that adds engineering cost either way.

**Disagrees with The Skeptic on:** immediate adoption of a purpose-built OLAP store — ClickHouse, BigQuery, and Redshift introduce operational complexity, cost, and team learning curves. For an analytics platform that's *just starting*, Postgres is a reasonable foundation if the team commits to TimescaleDB or PG partitioning from day one.

**What The Data Analyst is missing:** JSONB with GIN indexes is workable at low-medium scale, but GIN indexes bloat and slow writes at high insert rates. At 50k events/min, index maintenance overhead becomes visible.

**Strongest concession:** The PM's point about team familiarity is underweighted in my analysis. Operational familiarity with Postgres reduces incident response time and on-call burden — that's real value.

---

**The Skeptic responds**

**Agrees with The Infrastructure Engineer on:** Kafka/buffer layer being the right architectural move regardless of database — this decouples the ingest rate from the database write performance and is the correct pattern for event pipelines.

**Disagrees with The Product Manager on:** MongoDB's schema flexibility advantage at the *analytics* layer — flexible schema helps at ingest time, not at query time. Analysts still need to know what fields exist to query them. The schema problem doesn't disappear; it moves from the write path to the read path where it's harder to manage.

**What The Data Analyst is missing:** Even with Postgres and SQL, at 50k events/min the query performance story degrades without partitioning. The SQL advantage over MongoDB shrinks if analysts are waiting 30 seconds for queries on unpartitioned tables.

**Strongest concession:** The PM is right that introducing ClickHouse now adds operational burden the team may not be ready for. A Postgres foundation with TimescaleDB is a legitimate "start here, migrate later" path — as long as the team doesn't pretend the migration won't eventually be necessary.

---

### Position Shifts

---

**The Data Analyst — revised position**

**Original stance:** PostgreSQL is the only viable choice.

**Shifted to:** PostgreSQL with a clear partitioning/TimescaleDB strategy from day one, with an explicit plan to evaluate ClickHouse if query performance degrades within 6 months.

**Key insight from debate:** JSONB at write volume is more expensive than I acknowledged. The SQL requirement stands, but the *database* behind SQL may need to change.

**Remaining non-negotiable:** Native SQL for analysts. Any solution that requires a translation layer or MongoDB's aggregation pipeline is a regression.

---

**The Product Manager — revised position**

**Original stance:** MongoDB's flexible schema speeds iteration.

**Shifted to:** The schema flexibility argument is weaker than I thought; JSONB in Postgres covers the ingest flexibility need while preserving SQL.

**Key insight from debate:** The analysts' SQL requirement is load-bearing — it's not just preference, it's how the team actually works. Routing around it adds friction that compounds.

**Remaining non-negotiable:** No manual schema migrations required to add a new event type. Whether that's MongoDB, JSONB, or a schemaless ingest layer, the product team can't be blocked by database PRs.

---

**The Infrastructure Engineer — revised position**

**Original stance:** Write architecture matters more than schema choice.

**Shifted to:** Agreed, but Postgres with TimescaleDB + Kafka ingest buffer is a coherent starting architecture — not a compromise, a deliberate foundation.

**Key insight from debate:** The team's operational familiarity with Postgres is undersold. Incident response on a known system beats theoretical performance on an unfamiliar one.

**Remaining non-negotiable:** A write buffer (Kafka or equivalent) in front of the database. Direct application writes at 50k events/min to any OLTP database is a design risk.

---

**The Skeptic — revised position**

**Original stance:** Neither Postgres nor MongoDB; use a purpose-built OLAP store.

**Shifted to:** Postgres + TimescaleDB as a pragmatic starting point, with explicit architectural markers for when to migrate to ClickHouse.

**Key insight from debate:** Introducing ClickHouse now is the right long-term answer but the wrong immediate answer if the team lacks operational experience with it. The migration path matters.

**Remaining non-negotiable:** The team must not pretend Postgres is the permanent answer. Define the migration trigger upfront (e.g., "if P90 query time exceeds 10s on 90-day lookback, we evaluate ClickHouse").

---

### Synthesis

**Points of consensus**

- A write buffer (Kafka or equivalent) is required regardless of database choice. Direct application writes at peak load is a design smell.
- MongoDB's schema flexibility argument does not survive scrutiny at the analytics query layer — the problem moves from write time to read time.
- The ad-hoc SQL requirement is non-negotiable. Any solution that routes around native SQL fails the analysts.
- Postgres is not the permanent answer at analytics scale, but it may be the correct starting point given team familiarity.
- JSONB columns in Postgres address the PM's schema flexibility concern without abandoning SQL.

**Remaining tensions**

- **Immediate OLAP vs "start Postgres, migrate later"**: The Skeptic and Analyst converged on "migrate later," but this requires genuine organisational commitment to the trigger conditions — which often doesn't happen.
- **JSONB query performance under write load**: Real uncertainty around GIN index maintenance at 50k events/min. Needs a proof-of-concept load test, not debate.

**Recommendation**

**PostgreSQL with TimescaleDB, JSONB for event payloads, and Kafka ingest buffer — with a pre-agreed migration trigger to ClickHouse.**

Reasoning:
1. The SQL requirement eliminates MongoDB without further debate. The ad-hoc analytical workflow the team depends on cannot be replicated adequately through a translation layer.
2. JSONB satisfies the PM's schema flexibility concern on ingest. New event types require no migrations — just write the new shape.
3. TimescaleDB gives time-series partitioning and compression that makes Postgres viable at this write volume, extending the runway before a migration is necessary.
4. Kafka decouples ingest rate from database write performance — this is the correct architecture regardless of which database sits behind it.
5. The team's Postgres familiarity is an operational asset that reduces incident risk in a new platform's early life.
6. **The migration trigger must be documented now:** if P90 analytical query time on a 90-day lookback exceeds an agreed threshold (e.g., 15 seconds), evaluate ClickHouse. This prevents "Postgres is temporary" from becoming "Postgres forever."

**Risks**

| Risk | Raised by | Severity | Monitoring signal |
|---|---|---|---|
| GIN index bloat degrades write performance at peak load | Infrastructure Engineer | High | Monitor index size and write latency weekly in first 30 days; alert if insert P99 exceeds 50ms |
| "Migrate later" commitment erodes; Postgres becomes permanent by default | Skeptic | High | Review the migration trigger at each quarterly planning cycle; treat it as a first-class architectural decision |
| JSONB field discovery is painful for analysts at scale | Data Analyst | Medium | Track analyst time spent on schema discovery; if >2hrs/week, invest in a schema registry or event catalogue |
| Kafka buffer adds operational complexity the team underestimates | PM | Medium | Ensure at least one engineer has production Kafka experience before go-live; include in on-call runbook |
| Peak spikes (2–5x sustained) exceed TimescaleDB chunk limits | Infrastructure Engineer | Medium | Load test at 250k events/min before launch; validate chunk sizes and compression settings |

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/17.0 (100%) |
| Evaluated | 2026-05-01 |
| Target duration | 73272 ms |
| Target cost | $0.0898 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill selects exactly 4 perspectives with genuinely different stances — at least 2 in direct tension with each other | PASS | Exactly 4 perspectives: The Data Analyst (strongly pro-Postgres), The Product Manager (pro-MongoDB flexibility), The Infrastructure Engineer (write architecture focus), The Skeptic (neither — use OLAP). Data Analyst and PM are in direct tension from the first line. |
| c2 | Each perspective states a core argument, primary concern, and explicit trade-off they accept in Step 1 | PASS | Every perspective block has 'Core argument', 'Primary concern', and 'What they would sacrifice'. E.g. Data Analyst: core=ad-hoc SQL is non-negotiable; concern=analysts blocked; sacrifice='Some schema rigidity on ingest'. PM: core=schema evolution velocity; concern=migration bottlenecks; sacrifice='The convenience of native SQL'. |
| c3 | Each perspective in Step 2 engages with a specific claim from at least one other perspective — not just restates their own position | PASS | Each debate block names other perspectives directly: Data Analyst 'Disagrees with The Product Manager on: the migration burden claim'; PM 'Disagrees with The Data Analyst on: JSONB as a solution'; Infrastructure Engineer 'Disagrees with The Skeptic on: immediate adoption of a purpose-built OLAP store'; Skeptic 'Disagrees with The Product Manager on: MongoDB's schema flexibility advantage at the analytics layer'. |
| c4 | Every perspective makes at least one concession in the debate — a debate with zero concessions is flagged as performative by the skill's own rules | PASS | Each debate block ends with a 'Strongest concession' line. E.g. Skeptic: 'The PM is right that introducing ClickHouse now adds operational burden the team may not be ready for'; Infrastructure Engineer: 'The PM's point about team familiarity is underweighted in my analysis'; Data Analyst: 'The Skeptic is right that this may be the wrong layer entirely.' |
| c5 | Step 3 shows revised positions with explicit description of what shifted from the opening stance | PASS | 'Position Shifts' section has 'Original stance:' and 'Shifted to:' fields for every perspective. PM: 'Original stance: MongoDB's flexible schema speeds iteration. Shifted to: The schema flexibility argument is weaker than I thought; JSONB in Postgres covers the ingest flexibility need while preserving SQL.' Each also names 'Key insight from debate' and 'Remaining non-negotiable'. |
| c6 | Step 4 synthesis produces a concrete recommendation with reasoning, not just 'it depends' | PASS | Synthesis recommends: 'PostgreSQL with TimescaleDB, JSONB for event payloads, and Kafka ingest buffer — with a pre-agreed migration trigger to ClickHouse.' Followed by 6 numbered reasoning points tied to the specific load and analyst requirements, plus a 5-row risk table. |
| c7 | Risk register in the synthesis includes at least one risk per perspective raised during debate | PASS | Risk table attributes risks to each perspective: 'GIN index bloat' and 'Peak spikes' — Infrastructure Engineer; 'Migrate later commitment erodes' — Skeptic; 'JSONB field discovery painful for analysts' — Data Analyst; 'Kafka buffer adds operational complexity the team underestimates' — PM. |
| c8 | Synthesis correctly distinguishes between points of genuine consensus vs remaining tensions that need data or authority to resolve | PARTIAL | Synthesis has explicit 'Points of consensus' (5 items, e.g. 'A write buffer is required regardless') and 'Remaining tensions' (2 items, including 'Needs a proof-of-concept load test, not debate' for JSONB performance). The distinction is structurally present and well-reasoned. |
| c9 | Output's four perspectives are named with distinct, role-grounded identities (e.g. 'Database engineer focused on operational reliability') — not labelled 'Perspective 1, 2, 3, 4' | PASS | Perspectives are titled 'The Data Analyst', 'The Product Manager (Pragmatist)', 'The Infrastructure Engineer', and 'The Skeptic' — all role-grounded, none generic. |
| c10 | Output's perspectives include genuine tension — at least one strongly pro-Postgres voice and at least one strongly pro-MongoDB voice — not four variants of the same lukewarm stance | PASS | Data Analyst opens with 'PostgreSQL is the only viable choice' (strongly pro-Postgres). Product Manager opens with 'MongoDB's flexible schema cuts time-to-market for new event types' (pro-MongoDB). These are opposing poles, and the other two perspectives are genuinely distinct (write architecture, OLAP advocacy). |
| c11 | Output addresses the 50k events/min peak write requirement explicitly — analysing whether each option handles that throughput, with reasoning grounded in the technology | PASS | Infrastructure Engineer explicitly calculates: '50k events/min is 833 writes/second sustained, with peak spikes likely 2-5x that.' Debate discusses connection pooling, write buffering, partitioning, GIN index maintenance overhead at high insert rates, and the risk table flags 'Peak spikes (2–5x sustained) exceed TimescaleDB chunk limits' as High severity. |
| c12 | Output addresses the ad-hoc SQL requirement — pointing out that MongoDB's ad-hoc query story is weaker for analysts who expect SQL, and that Postgres's JSONB columns can give 'schema flexibility' without giving up SQL | PASS | Data Analyst: 'MongoDB's query language can't replicate [JOINs, window functions, CTEs] without a translation layer.' Also: 'Postgres JSONB columns handle semi-structured event payloads without schema migrations. You get flexible ingest *and* SQL.' PM's revised position confirms: 'JSONB in Postgres covers the ingest flexibility need while preserving SQL.' |
| c13 | Output's engagement step shows perspectives quoting or referencing each other's specific claims — e.g. 'the data analyst's point about ad-hoc SQL undermines my flexibility argument because...' | PASS | Each debate section uses 'Agrees with [Name] on:', 'Disagrees with [Name] on:', and 'What [Name] is missing:' headers referencing named perspectives' specific claims. E.g. PM: 'Disagrees with The Data Analyst on: JSONB as a solution to schema flexibility — JSONB queries are slower, indexes on nested fields are complex...' |
| c14 | Output shows at least one concession per perspective — a moment where the speaker admits an opposing point has merit and adjusts their position, not pure restatement | PASS | Explicit 'Strongest concession' block in each debate section. Infrastructure Engineer: 'The PM's point about team familiarity is underweighted in my analysis. Operational familiarity with Postgres reduces incident response time and on-call burden — that's real value.' These are genuine admissions of opposing merit. |
| c15 | Output's revised positions are explicit about what shifted — 'I started favouring MongoDB on flexibility, but I've come around on Postgres JSONB for that' — not implicit | PASS | PM revised position: 'Original stance: MongoDB's flexible schema speeds iteration. Shifted to: The schema flexibility argument is weaker than I thought; JSONB in Postgres covers the ingest flexibility need while preserving SQL.' Skeptic: 'Original stance: Neither Postgres nor MongoDB; use a purpose-built OLAP store. Shifted to: Postgres + TimescaleDB as a pragmatic starting point.' All explicit. |
| c16 | Output's synthesis recommends ONE option (likely Postgres given the constraints) with concrete reasoning tied to the specific load and analyst-tooling requirements — not 'it depends on your priorities' | PASS | Single concrete recommendation: 'PostgreSQL with TimescaleDB, JSONB for event payloads, and Kafka ingest buffer.' Point 1 explicitly eliminates MongoDB: 'The SQL requirement eliminates MongoDB without further debate.' Reasoning is tied to 50k events/min (TimescaleDB partitioning, Kafka buffer) and analyst tooling (native SQL, no translation layer). |
| c17 | Output's risk register lists at least one risk per perspective raised during the debate — capturing what the rejected perspectives warned about that could still bite | PASS | Risk table column 'Raised by' attributes each risk: Infrastructure Engineer gets rows 1 and 5; Skeptic gets row 2; Data Analyst gets row 3; PM gets row 4. All four perspectives have at least one risk attributed to them in the register. |
| c18 | Output's synthesis distinguishes consensus (e.g. 'all perspectives agree the team's Postgres familiarity is real value') from remaining tensions (e.g. 'schema flexibility is a real cost — needs migration tooling investment regardless of choice') | PARTIAL | 'Points of consensus' lists 5 explicitly agreed items (e.g. 'A write buffer is required regardless of database choice'). 'Remaining tensions' section names 2 unresolved items: the 'start Postgres, migrate later' commitment risk and 'JSONB query performance under write load — Real uncertainty... Needs a proof-of-concept load test, not debate.' Clear structural separation. |

### Notes

The captured output is a near-perfect execution of the council skill. All 18 criteria are met at or above the required level. The four perspectives are sharply differentiated with genuine opposing poles (Data Analyst vs PM), the debate structure rigorously engages across perspectives using named references and explicit concessions, and the position-shift section is transparently explicit about what each speaker changed their mind on. The synthesis is notably strong: it picks one concrete option (PostgreSQL+TimescaleDB+Kafka+JSONB), eliminates MongoDB with a crisp single sentence, and adds a migration trigger condition to prevent the 'temporary becomes permanent' failure mode — a detail drawn directly from the Skeptic's position. The risk table covers all four perspectives. The only ceiling-capped criteria (c8, c18) are both satisfied at the maximum allowed level. No gaps or omissions were identified.
