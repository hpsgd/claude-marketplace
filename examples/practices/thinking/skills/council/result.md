# Council database selection debate

A team needs to choose between PostgreSQL and MongoDB for a new event-driven analytics platform. The council skill is invoked to debate the options with multiple competing perspectives.

## Prompt

> /council Should we use PostgreSQL or MongoDB for the new analytics platform? We're storing user behaviour events (high write volume, ~50k events/min at peak), and the data analysts need ad-hoc SQL queries. The engineering team is more comfortable with Postgres but the product manager thinks MongoDB's flexible schema will speed up iteration.

```markdown

## Output

### Council: PostgreSQL vs MongoDB for analytics platform

#### Perspectives

##### The Data Analyst — SQL access is non-negotiable

| Field | Value |
|---|---|
| Core argument | Ad-hoc SQL queries are the primary access pattern for analytics. MongoDB's aggregation pipelines fall apart for complex joins and window functions that analysts use daily. |
| Primary concern | We end up with MongoDB and analysts spend half their time translating SQL intuition. |
| What they would sacrifice | Schema flexibility. The event schema will stabilise once we know what we're measuring. |


##### The Platform Engineer — operational simplicity matters

| Field | Value |
|---|---|
| Core argument | The engineering team knows Postgres. Familiarity reduces operational risk and incident response time. MongoDB's flexible schema is also its biggest operational hazard — schema drift without guardrails. |
| Primary concern | Introducing MongoDB creates a second database technology to operate and skill up on. |
| What they would sacrifice | Raw write performance at extreme scale if Postgres proves sufficient. |


##### The Product Manager — iteration speed drives value

| Field | Value |
|---|---|
| Core argument | Event schemas change constantly in the first 6–12 months. MongoDB lets us add fields without migrations, directly reducing the friction to iterate. |
| Primary concern | Schema rigidity slows feature development when we need to capture new event types. |
| What they would sacrifice | SQL query convenience for analysts, at least initially. |


##### The Scalability Sceptic — 50k events/min is not trivial

| Field | Value |
|---|---|
| Core argument | 50k events/min = 72M events/day. At this volume, write patterns matter. Choosing on familiarity and then rebuilding under load at month 6 is the real risk. |
| Primary concern | Neither database is being evaluated properly against the actual write profile. |
| What they would sacrifice | Simplicity — the right solution probably involves TimescaleDB or a dedicated event store. |


---

#### Debate

##### The Data Analyst responds

| Field | Value |
|---|---|
| Agrees with Platform Engineer on | Operational familiarity reduces incident risk. |
| Disagrees with Product Manager on | Schema flexibility being the bottleneck — JSONB in Postgres handles variable fields without migrations. |
| What Product Manager is missing | Analyst productivity is product velocity. If analysts can't query the data cleanly, insights are delayed. |
| Strongest concession | The schema-migration friction argument is real for the first 3 months. |


##### The Platform Engineer responds

| Field | Value |
|---|---|
| Agrees with Scalability Sceptic on | 72M events/day is serious write volume; we need to measure, not assume. |
| Disagrees with Product Manager on | Schema drift being free — MongoDB documents where field X is a string in some, null in others, missing in oldest. That's technical debt, not flexibility. |
| What Scalability Sceptic is missing | Postgres with TimescaleDB is specifically designed for this volume. |
| Strongest concession | I can't honestly say we've operated Postgres at 50k writes/min. We should load test first. |


##### The Product Manager responds

| Field | Value |
|---|---|
| Agrees with Data Analyst on | JSONB in Postgres is a legitimate middle ground I hadn't fully considered. |
| Disagrees with Scalability Sceptic on | Load being the deciding factor — if TimescaleDB handles it, use Postgres. |
| What Data Analyst is missing | Not all analysts know JSONB query syntax well. |
| Strongest concession | If Postgres with a JSONB events column handles schema evolution AND write load, my objection largely disappears. |


##### The Scalability Sceptic responds

| Field | Value |
|---|---|
| Agrees with Platform Engineer on | TimescaleDB is the right framing for this comparison. |
| Disagrees with Platform Engineer on | Load testing being optional — at this volume it's mandatory before deciding. |
| What everyone is missing | ClickHouse may be the right answer — both databases are being asked to serve two conflicting roles. |
| Strongest concession | If the team has TimescaleDB experience, familiarity changes the operational argument. |


---

#### Position Shifts


| Field | Value |
|---|---|
| The Data Analyst | Postgres → Postgres with TimescaleDB + JSONB for variable fields. Schema concern solvable. |
| The Platform Engineer | Postgres for familiarity → Postgres with TimescaleDB, but only after a load test. |
| The Product Manager | MongoDB for flexibility → Postgres with JSONB if load test passes. |
| The Scalability Sceptic | Load paramount → TimescaleDB viable if validated; raise ClickHouse as alternative. |


---

#### Synthesis

**Consensus:** PostgreSQL with TimescaleDB, JSONB for variable event fields. All four perspectives converged here after TimescaleDB and JSONB were raised.

**Tensions:** The load test question cannot be resolved by debate — it requires data. This must be answered with a benchmark before finalising.

**Recommendation:** Adopt PostgreSQL with TimescaleDB. Design the events table with typed columns for core fields and JSONB for variable properties. Prerequisite: run a write load test at 60k events/min before committing.

**Risks:**

| Risk | Raised by | Severity | Monitoring signal |
|---|---|---|---|
| Write volume exceeds Postgres capacity | Scalability Sceptic | High | Load test at 60k events/min |
| JSONB query syntax slows analyst adoption | Product Manager | Medium | Analyst onboarding feedback |
| Schema drift in JSONB creates data quality issues | Platform Engineer | Medium | Schema validation job on insert |
| ClickHouse is correct answer discovered at scale | Scalability Sceptic | Low | Re-evaluate if p95 query latency exceeds 5s |
```

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7/8 (88%) |
| Evaluated | 2026-04-16 |


- [x] PASS: Exactly 4 perspectives with at least 2 in direct tension — Step 1 states "Define 4 perspectives" with "at least 2 must be in direct tension (e.g., speed vs quality, user value vs technical debt)." The constraint is explicit in the definition.
- [x] PASS: Each perspective states core argument, primary concern, and trade-off — Step 1 template requires all three fields: "Core argument," "Primary concern," "What they would sacrifice." All three are mandatory template fields.
- [x] PASS: Each perspective engages with specific claims in Step 2 — Step 2 rules state "Every response must engage with a specific claim, not a general position." The response template requires naming which perspective and which specific point with "because [reasoning]."
- [x] PASS: Every perspective makes at least one concession — Step 2 rules state "Every perspective must make at least one concession." The Rules section reinforces: "Concessions are mandatory. A debate with no concessions is propaganda." The "Strongest concession" field is in the per-perspective response template.
- [x] PASS: Step 3 shows revised positions with explicit shifts — Step 3 template requires "Original stance," "Shifted to," "Key insight from debate," and "Remaining non-negotiable." These are mandatory template fields that require stating what changed.
- [x] PASS: Step 4 produces a concrete recommendation — the Rules section states "No false balance. If the evidence overwhelmingly supports one perspective, say so in the synthesis." Step 4 mandates "Recommended decision" with a risk register. The Output Format section explicitly requires "Recommendation: [decision with reasoning]."
- [~] PARTIAL: Risk register includes at least one risk per perspective — Step 4 defines a risk register table with a "Raised by" column. The definition requires the table exist with the column structure. However the skill does not require one risk per perspective — it requires "Concerns raised during debate that should be monitored regardless of decision." Coverage per perspective is not mandated. PARTIAL scored as 0.5.
- [~] PARTIAL: Synthesis distinguishes consensus from remaining tensions — Step 4 has separate "Points of consensus" and "Remaining tensions" sections. Tensions are defined as "Genuine disagreements that debate alone cannot resolve — these need data, experiments, or authority to decide." This is explicit in the definition. PARTIAL ceiling applies per criterion prefix.

### Notes

The council skill is well-designed. The mandatory concession requirement is the key mechanism that prevents performative debate. The Step 3 position shift template with explicit "what changed" and "remaining non-negotiable" fields forces genuine evolution rather than restating the opening. One gap on criterion 7: the skill mandates a risk register but not one risk per perspective. In a well-run council debate perspectives naturally surface risks, but the definition doesn't enforce this coverage. The four-step output format (Perspectives, Debate, Position Shifts, Synthesis) is well-structured and clearly defined.
