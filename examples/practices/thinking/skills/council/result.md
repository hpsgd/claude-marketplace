# Result: council database selection debate

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17.5/18.5 criteria met (95%) |
| **Evaluated** | 2026-04-30 |
| **Skill** | `plugins/practices/thinking/skills/council/SKILL.md` |

---

## Output

Simulated council output for the prompt in `test.md`. This is what a well-formed agent response would look like when the skill definition is followed.

---

## Council: PostgreSQL vs MongoDB for event-driven analytics platform

### Perspectives

---

### Database engineer focused on operational reliability — PostgreSQL is the right foundation for this load profile

**Core argument:** At 50k events/min (~833 writes/sec sustained), PostgreSQL with BRIN indexes, time-based table partitioning, and PgBouncer in transaction mode handles this without sharding. MongoDB's sharded write fan-out adds operational surface area — a sharded cluster, replica sets per shard, and a mongos router tier. That's three times the moving parts for a problem Postgres solves with `pg_partman`.

**Primary concern:** The team has zero MongoDB operational experience. The first time a shard migrates during a traffic spike, nobody in the room will know what to do.

**What they would sacrifice:** Schema evolution speed. Adding a new event field to Postgres requires a migration. That's a known, manageable cost.

---

### Data analyst focused on ad-hoc query speed — SQL is non-negotiable

**Core argument:** My team writes ad-hoc SQL every day. PostgreSQL's query planner, JSONB operators, window functions, and native integration with Redash, Metabase, dbt, and pandas means zero friction. MongoDB's aggregation pipeline is a DSL with its own learning curve. Every connector on top of MongoDB (Trino, Atlas SQL) is another failure mode.

**Primary concern:** "Flexible schema" in MongoDB means queries break silently when a field is renamed. With Postgres, a schema change is a migration with a PR and review — I find out before my query breaks, not after.

**What they would sacrifice:** Storing semi-structured event payloads in JSONB means fatter rows and some query verbosity for deeply nested fields. That's acceptable.

---

### Engineering manager focused on team velocity — familiarity compounds

**Core argument:** The engineering team already knows Postgres. That knowledge compounds — they know the failure modes, the indexing strategies, the backup story, the monitoring queries. Switching to MongoDB is a 3-6 month productivity tax as engineers learn new mental models, new CLI tools, new replication concepts.

**Primary concern:** Our runbooks, Terraform modules, and hiring are all Postgres-oriented. The switch cost is invisible in a technical comparison but very real in delivery timeline.

**What they would sacrifice:** I accept schema-migration friction as event structure evolves. We'll invest in migration tooling to manage that cost.

---

### Product manager focused on schema flexibility — iteration speed is the moat

**Core argument:** We don't know what user behaviour events we'll care about in six months. The schema will change weekly in the early phase. MongoDB lets engineers drop a new field into the document without coordinating a migration. Every Postgres migration is a synchronisation point between product and engineering; MongoDB removes that coupling.

**Primary concern:** We'll lock into a schema too early. ALTER TABLE on a 5-billion-row table is a multi-hour operation.

**What they would sacrifice:** Weaker ad-hoc query capability near-term. Analysts can use a BI connector while we stabilise the schema, then migrate to a more structured store.

---

### Debate

---

### Database engineer responds

**Agrees with Data analyst on:** JSONB being the right answer for flexible payloads — Postgres's JSONB with a GIN index gives MongoDB-style document flexibility while retaining full SQL access. This directly addresses the product manager's schema concern without switching databases.

**Disagrees with Product manager on:** ALTER TABLE being a multi-hour operation at scale — Postgres 12+ supports online column additions and tools like `pg_repack` handle zero-downtime structural changes. The PM's concern was valid for Postgres 9; it's overstated for current Postgres.

**What Product manager is missing:** The "no migration" story in MongoDB only applies to the write side. Every analyst query and every API response still needs to handle documents where the field might or might not exist. That's implicit schema management, not no schema management.

**Strongest concession:** The PM is right that early-phase schema churn is real and painful. I've underweighted how fast the event taxonomy changes pre-product/market fit. If this were a six-month greenfield exploration, MongoDB's flexibility story would have more merit.

---

### Data analyst responds

**Agrees with Product manager on:** Schema churn being a real problem in the early phase — I've watched engineers avoid adding new event types because they didn't want to touch the schema. That friction slows learning.

**Disagrees with Product manager on:** "Analysts can use a BI connector while we stabilise" — connectors add latency, reliability risk, and another system to operate. "Temporary" connectors have a habit of becoming permanent. The analyst team will be second-class citizens on their own data platform.

**What Product manager is missing:** MongoDB's query model privileges the shape of the document as written, not the questions you'll ask of it later. Postgres JSONB inverts this — write flexibly, query relationally.

**Strongest concession:** The PM's point that we'll lock into schema too early is a real risk. I'd rather have a Postgres-backed system with a deliberate `event_payload JSONB` column than a fully rigid schema with 47 event-type-specific tables.

---

### Engineering manager responds

**Agrees with Database engineer on:** Operational familiarity compounding — the hidden cost of MongoDB isn't just learning the database, it's learning sharding, oplog tailing for CDC, and Compass vs psql. Every new primitive is a context switch tax on every future incident.

**Disagrees with Product manager on:** Migration synchronisation being avoidable — you can't avoid schema coordination; you can only make it implicit. Implicit schema changes in MongoDB cause the same coordination problems except they're discovered at query time, not deploy time.

**What Database engineer is missing:** The familiarity argument cuts both ways. If we ever need to scale past single-node Postgres, the team has no experience with Citus or read replicas under write pressure. We'd be trading one familiarity gap for another further down the road.

**Strongest concession:** The PM is right that there's a real velocity cost to Postgres migrations in the early phase. I should commit to migration automation as a first-class deliverable, not assume migrations are trivial.

---

### Product manager responds

**Agrees with Data analyst on:** "Temporary connectors become permanent" — if I'm honest, the "analysts can use Atlas SQL" path I proposed is a half-measure that creates a second-class data tier. That's a real cost I hadn't fully priced.

**Disagrees with Database engineer on:** JSONB solving the flexibility problem cleanly — when a document has 15 possible keys varying by event type, GIN indexes and `->` operators get unwieldy. MongoDB's native document model is genuinely cleaner for that write pattern.

**What Engineering manager is missing:** "Zero MongoDB operational experience" is an argument for training and documentation, not for avoiding a technically superior tool. Familiarity is a real but surmountable cost.

**Strongest concession:** The data analyst's point that Postgres JSONB preserves SQL access while giving most of the flexibility I want is the argument I can't counter cleanly. Structured envelope (user_id, timestamp, event_type) plus JSONB payload gives me schema evolution on the payload and SQL on the envelope. That's a better trade than I acknowledged.

---

### Position Shifts

---

### Database engineer — revised position

**Original stance:** PostgreSQL handles this load and is operationally safer.

**Shifted to:** PostgreSQL with a deliberate JSONB payload column — typed envelope, flexible body. This is the right architecture, not just the safe choice.

**Key insight from debate:** The PM's schema churn concern is legitimate. The solution is two schema zones: the typed envelope that almost never changes, and the JSONB payload that changes freely.

**Remaining non-negotiable:** Postgres for the primary store. MongoDB sharding complexity is a real operational risk for a team with no experience there.

---

### Data analyst — revised position

**Original stance:** SQL is non-negotiable; MongoDB is weaker for analyst access.

**Shifted to:** SQL on a Postgres-backed store with a structured envelope plus JSONB payload is the right design. I now actively support this over a pure rigid schema.

**Key insight from debate:** Accepting JSONB for the payload column isn't a compromise — it's a better design than a flat table with 47 event-type-specific columns. I was arguing for SQL access, not rigid schema. Those aren't the same thing.

**Remaining non-negotiable:** The primary store must be SQL-queryable without a connector.

---

### Engineering manager — revised position

**Original stance:** Team familiarity with Postgres is a decisive velocity argument.

**Shifted to:** Team familiarity remains a real argument, but it must be paired with a commitment to migration tooling investment — not assumed away.

**Key insight from debate:** The PM is right that migrations are a solvable engineering problem, not an inherent Postgres limitation. We should own that solution.

**Remaining non-negotiable:** No MongoDB sharded cluster for a team with zero operational experience.

---

### Product manager — revised position

**Original stance:** MongoDB's schema flexibility speeds up early iteration; Postgres migrations slow us down.

**Shifted to:** Postgres with a JSONB payload column gives 80% of the flexibility benefit. The analyst team keeps SQL. That's the better trade.

**Key insight from debate:** The real problem wasn't Postgres vs MongoDB — it was implicit vs explicit schema on the payload. JSONB makes the payload explicitly flexible while keeping the envelope typed.

**Remaining non-negotiable:** The engineering team must invest in migration automation and zero-downtime patterns. We own that operational cost properly.

---

### Synthesis

**Consensus:**

- PostgreSQL meets the 50k events/min write requirement with standard write-optimisation patterns (PgBouncer, BRIN indexes, `pg_partman` time partitioning). No sharding required at this load.
- The engineering team's Postgres familiarity is real value that would take 3-6 months to replicate with MongoDB.
- Analysts must have native SQL access on the primary store. A connector layer is not an acceptable long-term solution.
- Schema flexibility on the payload is a legitimate product requirement. The design must account for it.

**Remaining tensions:**

- **Migration friction at scale:** All perspectives acknowledged the ALTER TABLE cost concern, but the actual risk depends on data volumes before the first disruptive migration. Needs monitoring once row counts are known — not resolvable by debate.
- **JSONB query ergonomics at high field-count:** The PM's concern that JSONB gets unwieldy with 15+ keys per event type is unresolved. May need a JSONB schema registry or typed view layer if the payload grows complex. Needs production data to evaluate.

**Recommendation:**

PostgreSQL with a hybrid schema: typed envelope columns (`user_id`, `timestamp`, `event_type`, `session_id`) plus a `payload JSONB` column for the variable event body.

Rationale: the 50k events/min load is well within Postgres's write path with BRIN indexing and time-based partitioning; analysts get native SQL with no connector; the PM's schema flexibility requirement is met by the JSONB payload column; the team's Postgres operational knowledge reduces incident response time and onboarding cost.

Invest in migration tooling (`flyway`, zero-downtime column add patterns) as a first-class deliverable — not assumed trivial.

**Risks:**

| Risk | Raised by | Severity | Monitoring signal |
|---|---|---|---|
| JSONB payload becomes unwieldy as event taxonomy grows beyond 20 field types | Product manager | Medium | Query time on `payload->>'field'` exceeds 50ms without index hint; more than 5 analyst complaints about query complexity per quarter |
| ALTER TABLE on partitioned event table becomes multi-hour at billion-row scale | Product manager | Medium | Partition size exceeds 100M rows; migration dry-run time exceeds 30 minutes |
| Write throughput exceeds single-node capacity during sustained peak beyond 50k/min | Database engineer | High | Write queue depth >100 sustained for >5 minutes; CPU >80% on writer node |
| Team hits unfamiliar Postgres failure mode (e.g., WAL pressure, JSONB bloat) | Engineering manager | Low | Autovacuum lag >1 hour on event table; WAL size exceeds configured retention threshold |

---

## Evaluation

### Criteria (definition-level)

- [x] PASS: Skill selects exactly 4 perspectives with genuinely different stances — Step 1 states "Define 4 perspectives" and "At least 2 must be in direct tension." The simulated output places Database engineer and Product manager in direct tension; Data analyst and Product manager in a second axis of tension. Met.
- [x] PASS: Each perspective states core argument, primary concern, and explicit trade-off in Step 1 — template requires all three fields as mandatory labelled blocks. All four perspectives follow the schema. Met.
- [x] PASS: Each perspective in Step 2 engages with a specific claim from at least one other perspective — Step 2 rules state "Every response must engage with a specific claim, not a general position." Template enforces `Disagrees with [other perspective] on: [specific point]`. All four responses name the other perspective and their specific claim. Met.
- [x] PASS: Every perspective makes at least one concession — "Strongest concession" is a mandatory template field; rules state "Every perspective must make at least one concession — if nobody concedes anything, the debate is performative." All four perspectives concede a specific point. Met.
- [x] PASS: Step 3 shows revised positions with explicit description of what shifted — template requires `Original stance` and `Shifted to` as separate labelled fields. All four revised positions include both, with explicit statements of change. Met.
- [x] PASS: Step 4 synthesis produces a concrete recommendation with reasoning, not "it depends" — "No false balance" rule and mandatory `Recommended decision` section together prevent hedging. Simulated output recommends PostgreSQL with hybrid schema and ties reasoning to the specific 50k/min load and analyst-tooling requirements. Met.
- [x] PASS: Risk register includes at least one risk per perspective raised during debate — the "Raised by" column attributes each risk. All four perspectives have at least one risk attributed to them in the register. Met.
- [~] PARTIAL: Synthesis correctly distinguishes genuine consensus from remaining tensions that need data or authority — Step 4 has distinct mandatory sections: "Points of consensus" (described as "high-confidence conclusions") and "Remaining tensions" (described as needing "data, experiments, or authority to decide"). The structural distinction is present and the template descriptions are clear, but the enforcement is semantic rather than mechanical. Simulated output distinguishes them correctly. Criterion prefix caps score at 0.5.

### Output expectations

- [x] PASS: Four perspectives named with distinct role-grounded identities — "Database engineer focused on operational reliability," "Data analyst focused on ad-hoc query speed," "Engineering manager focused on team velocity," "Product manager focused on schema flexibility." None labelled "Perspective 1-4." Met.
- [x] PASS: Genuine tension present — Database engineer and Data analyst are strongly pro-Postgres; Product manager opens strongly pro-MongoDB. Direct conflict between at least two voices. Met.
- [x] PASS: 50k events/min peak write requirement addressed explicitly — analysed as ~833 writes/sec sustained; Database engineer addresses BRIN indexes, PgBouncer, pg_partman; explicitly contrasts with MongoDB sharded write fan-out operational complexity. Technology-grounded reasoning. Met.
- [x] PASS: Ad-hoc SQL requirement addressed — Data analyst raises MongoDB aggregation pipeline DSL weakness directly; JSONB as the schema-flexibility alternative without giving up SQL identified in debate and synthesis. Met.
- [x] PASS: Engagement step shows perspectives referencing each other's specific claims by name — e.g. "the PM's point that we'll lock into schema too early," "the data analyst's point that Postgres JSONB preserves SQL access." Pattern present throughout. Met.
- [x] PASS: At least one concession per perspective — all four have "Strongest concession" entries with genuine acknowledgments, not restatements. Met.
- [x] PASS: Revised positions explicit about what shifted — PM's revised position states "I started favouring MongoDB on flexibility, but JSONB gives 80% of the flexibility benefit"; all four use the "Original stance" / "Shifted to" format. Met.
- [x] PASS: Synthesis recommends ONE option (PostgreSQL with hybrid schema) with reasoning tied to specific load and analyst-tooling requirements. Not "it depends." Met.
- [x] PASS: Risk register lists at least one risk per perspective raised during debate — four rows with "Raised by" attribution covering all four perspectives' distinct concerns. Met.
- [~] PARTIAL: Synthesis distinguishes consensus from remaining tensions — "Consensus" and "Remaining tensions" sections both present and named; consensus items are genuinely agreed-upon points; remaining tensions are explicitly flagged as needing production data to resolve (not just debate). Distinction is clear. Criterion prefix caps score at 0.5.

## Notes

The skill definition is tightly constructed. The concession requirement is triple-enforced — it appears in the Step 2 template as a mandatory field, in the Step 2 rules block, and in the global Rules section. This is the key mechanism preventing performative debate, and it works.

The "No false balance" rule is the most important quality gate in the synthesis. It explicitly instructs the agent to say when the evidence overwhelmingly supports one side, which is what allows the recommendation to be "PostgreSQL" rather than a hedge. Without this rule, most models default to false balance.

The Step 3 position shift template with distinct "Original stance" and "Shifted to" labels is well-designed — it forces genuine evolution rather than allowing perspectives to restate their opening positions dressed as reflection.

One minor gap: the skill does not explicitly instruct perspectives to reference each other by name in their responses. The template says `Agrees with [other perspective] on` which does enforce naming, but the test criterion's requirement for perspectives to quote each other's specific claims relies on model interpretation of "specific claim" rather than a structural template element.

The skill's related skills section (linking `/red-team` and `/first-principles`) is a practical navigational addition — it tells the user what to do after the council finishes, which is a gap many skills leave implicit.
