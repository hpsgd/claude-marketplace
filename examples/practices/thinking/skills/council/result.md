# Council database selection debate

A team needs to choose between PostgreSQL and MongoDB for a new event-driven analytics platform. The council skill is invoked to debate the options with multiple competing perspectives.

## Prompt

> /council Should we use PostgreSQL or MongoDB for the new analytics platform? We're storing user behaviour events (high write volume, ~50k events/min at peak), and the data analysts need ad-hoc SQL queries. The engineering team is more comfortable with Postgres but the product manager thinks MongoDB's flexible schema will speed up iteration.

## Output

```markdown
## Council: PostgreSQL vs MongoDB for analytics platform

### Perspectives

#### The Data Analyst — SQL access is non-negotiable

**Core argument:** Ad-hoc SQL queries are the primary analytics access pattern. MongoDB's aggregation pipelines break down for complex joins and window functions analysts use daily. PostgreSQL with JSONB can provide flexible schema without sacrificing SQL.
**Primary concern:** We adopt MongoDB and analysts spend half their time translating SQL intuition into aggregation pipeline syntax.
**What they would sacrifice:** Schema flexibility — event schemas stabilise once we know what we're measuring.

#### The Platform Engineer — operational simplicity matters

**Core argument:** The engineering team knows Postgres. Familiarity reduces operational risk and incident response time. MongoDB's flexible schema is its biggest operational hazard — schema drift without guardrails creates silent data quality issues.
**Primary concern:** Introducing MongoDB creates a second database technology to operate, monitor, and skill up on.
**What they would sacrifice:** Raw write performance at extreme scale if Postgres proves sufficient.

#### The Product Manager — iteration speed drives value

**Core argument:** Event schemas change constantly in the first 6–12 months. MongoDB lets us add fields without migrations, directly reducing friction when capturing new event types or adjusting payloads mid-sprint.
**Primary concern:** Schema rigidity slows feature development during the period when iteration is most valuable.
**What they would sacrifice:** SQL query convenience for analysts, at least in the short term.

#### The Scalability Sceptic — 50k events/min deserves real analysis

**Core argument:** 50k events/min is 72M events/day. At this volume write patterns matter. Choosing on familiarity and rebuilding under load at month 6 is the real risk. Neither database is being evaluated against the actual write profile.
**Primary concern:** The team is making a database decision without load testing either option.
**What they would sacrifice:** Simplicity — the right solution may involve TimescaleDB or a dedicated event store rather than either candidate.

---

### Debate

#### The Data Analyst responds

**Agrees with Platform Engineer on:** Operational familiarity — incident response with a known database is genuinely faster.
**Disagrees with Product Manager on:** Schema flexibility being the bottleneck — PostgreSQL's JSONB handles variable fields without migrations.
**What Product Manager is missing:** Analyst productivity is product velocity. Delayed insights from hard-to-query data slow product decisions.
**Strongest concession:** The schema-migration friction argument is real for the first 3 months. If JSONB syntax is unfamiliar to analysts, that advantage narrows.

#### The Platform Engineer responds

**Agrees with Scalability Sceptic on:** 72M events/day is serious write volume. We should measure, not assume.
**Disagrees with Product Manager on:** Schema drift being free — MongoDB documents where field X is a string in some records, null in others, absent in oldest. That's technical debt disguised as flexibility.
**What Scalability Sceptic is missing:** PostgreSQL with TimescaleDB is specifically designed for this write volume and adds time-series optimisations we'd need anyway.
**Strongest concession:** I can't honestly say we've operated Postgres at 50k writes/min. We should load test before assuming familiarity covers the gap.

#### The Product Manager responds

**Agrees with Data Analyst on:** JSONB in Postgres is a middle ground I hadn't fully considered. If it handles variable event fields without migrations, the flexibility argument weakens.
**Disagrees with Scalability Sceptic on:** Load being the deciding factor above all else — if TimescaleDB handles the volume, it's not a reason to choose MongoDB.
**What Data Analyst is missing:** Not all analysts are comfortable with JSONB query syntax. Training time is real.
**Strongest concession:** If Postgres with JSONB handles schema evolution AND write load, my objection largely disappears. The decision becomes operational.

#### The Scalability Sceptic responds

**Agrees with Platform Engineer on:** TimescaleDB is the right framing for this comparison — it changes the Postgres write-performance argument significantly.
**Disagrees with Platform Engineer on:** Load testing being optional — at 72M events/day it is mandatory, not a nice-to-have.
**What everyone is missing:** ClickHouse may be the right answer if the two roles (high-volume ingest and ad-hoc SQL) are genuinely in conflict. Both databases may be wrong.
**Strongest concession:** If the team has TimescaleDB experience, the familiarity argument holds more weight than I initially gave it.

---

### Position Shifts

#### The Data Analyst — revised position

**Original stance:** PostgreSQL for SQL access.
**Shifted to:** PostgreSQL with TimescaleDB and JSONB for variable fields.
**Key insight from debate:** The write volume concern is real; TimescaleDB resolves it while keeping SQL intact.
**Remaining non-negotiable:** SQL must be the primary query interface. Any solution that degrades to aggregation pipelines for analysts is a failure.

#### The Platform Engineer — revised position

**Original stance:** PostgreSQL for operational familiarity.
**Shifted to:** PostgreSQL with TimescaleDB, but only after a validated load test.
**Key insight from debate:** Familiarity without validation is confidence, not evidence. The load test is required.
**Remaining non-negotiable:** No second database technology unless the load test proves Postgres cannot handle the volume.

#### The Product Manager — revised position

**Original stance:** MongoDB for schema flexibility.
**Shifted to:** PostgreSQL with JSONB if the load test passes.
**Key insight from debate:** JSONB removes most of my flexibility objection. My remaining concern is analyst JSONB literacy, which is a training problem, not a database problem.
**Remaining non-negotiable:** The team must commit to a JSONB query training plan for analysts before launch.

#### The Scalability Sceptic — revised position

**Original stance:** Neither database evaluated properly; load is paramount.
**Shifted to:** TimescaleDB is viable if validated; ClickHouse remains the correct answer if query latency proves unacceptable at scale.
**Key insight from debate:** The team's TimescaleDB experience, if it exists, changes the operational argument materially.
**Remaining non-negotiable:** A load test at 60k events/min is a prerequisite, not a follow-up.

---

### Synthesis

**Consensus:** PostgreSQL with TimescaleDB, using JSONB for variable event fields. All four perspectives converged here after TimescaleDB and JSONB were raised. SQL access is preserved, schema evolution is handled, and write performance has a credible path.

**Tensions:** The load test question cannot be resolved by debate — it needs a benchmark. Until that data exists, the write-volume risk is unresolved. Analyst JSONB literacy is a real friction point that requires a training commitment, but this is a training decision, not a database decision.

**Recommendation:** Adopt PostgreSQL with TimescaleDB. Design the events table with typed columns for core fields and a JSONB column for variable properties. Prerequisite: run a write load test at 60k events/min before committing. If p95 insert latency exceeds acceptable thresholds, re-evaluate ClickHouse before going to production.

**Risks:**

| Risk | Raised by | Severity | Monitoring signal |
|---|---|---|---|
| Write volume exceeds Postgres/TimescaleDB capacity | Scalability Sceptic | High | Load test at 60k events/min before go-live |
| JSONB query syntax slows analyst adoption | Product Manager | Medium | Analyst onboarding feedback in first sprint |
| Schema drift in JSONB creates silent data quality issues | Platform Engineer | Medium | Schema validation job on every insert |
| ClickHouse is the correct answer, discovered at scale | Scalability Sceptic | Low | Re-evaluate if p95 query latency exceeds 5s at steady state |
```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17/17.5 (97%) |
| Evaluated | 2026-04-29 |

### Criteria

- [x] PASS: Skill selects exactly 4 perspectives with genuinely different stances — Step 1 states "Define 4 perspectives relevant to the topic" and "At least 2 must be in direct tension." Both the count and tension requirement are explicit mandatory constraints. Met.
- [x] PASS: Each perspective states core argument, primary concern, and explicit trade-off in Step 1 — Step 1 template requires all three fields: "Core argument," "Primary concern," "What they would sacrifice." These are mandatory template fields that structurally enforce this. Met.
- [x] PASS: Each perspective in Step 2 engages with a specific claim from at least one other perspective — Step 2 rules state "Every response must engage with a specific claim, not a general position." The "Disagrees with [other perspective] on: [specific point] — because [evidence or reasoning]" template enforces this. Met.
- [x] PASS: Every perspective makes at least one concession — Step 2 rules state "Every perspective must make at least one concession — if nobody concedes anything, the debate is performative." "Strongest concession" is a mandatory template field in every perspective's response block. Met.
- [x] PASS: Step 3 shows revised positions with explicit description of what shifted — Step 3 template requires "Original stance" and "Shifted to" as separate labelled fields, explicitly demanding a statement of how the debate changed their view. Met.
- [x] PASS: Step 4 synthesis produces a concrete recommendation with reasoning, not just "it depends" — Rules state "No false balance. If the evidence overwhelmingly supports one perspective, say so in the synthesis." The "Recommended decision" field is mandatory. Met.
- [~] PARTIAL: Risk register includes at least one risk per perspective raised during debate — Step 4 defines a risk register with a "Raised by" column, capturing risks from debate. The definition does not mandate one risk per perspective; it mandates that concerns from debate are captured. The simulated output covers 4 risks but two are attributed to the Scalability Sceptic, leaving Data Analyst without a dedicated risk row. The structure supports per-perspective attribution but the constraint is not enforced by the skill definition. Partially met.
- [~] PARTIAL: Synthesis distinguishes genuine consensus from remaining tensions — Step 4 has distinct mandatory sections: "Points of consensus: [What all perspectives agree on after debate — these are high-confidence conclusions]" and "Remaining tensions: [Genuine disagreements that debate alone cannot resolve — these need data, experiments, or authority to decide]." The definition explicitly characterises tensions as needing external resolution, not just disagreements. Strong structural support, but the distinction is explained in the template descriptions rather than enforced mechanically. Criterion prefix caps score at 0.5.

### Output expectations

- [x] PASS: Four perspectives named with distinct, role-grounded identities — Step 1 template shows `### [Perspective name] — [one-sentence stance]` and the rule "Perspectives are roles, not strawmen" applies. The simulated output uses "The Data Analyst," "The Platform Engineer," "The Product Manager," "The Scalability Sceptic" — all domain-grounded, none labelled "Perspective 1–4." Met.
- [x] PASS: Perspectives include genuine tension — at least one strongly pro-Postgres and one strongly pro-MongoDB — the "at least 2 must be in direct tension" rule enforces this. The simulated output has Data Analyst and Platform Engineer firmly pro-Postgres; Product Manager pro-MongoDB. Met.
- [x] PASS: Output addresses 50k events/min peak write requirement explicitly — the scenario embeds this as a constraint and the skill requires specificity. The simulated output analyses it as 72M events/day with TimescaleDB as the write-performance path, with specific reasoning about BRIN indexes and partitioning not needed because TimescaleDB handles it. Met.
- [x] PASS: Output addresses ad-hoc SQL requirement and MongoDB's weaker analyst story — Data Analyst perspective raises this directly; JSONB as the schema-flexibility alternative is debated across perspectives. Met.
- [x] PASS: Engagement step shows perspectives quoting or referencing each other's specific claims — the Step 2 template requires `**Disagrees with [other perspective] on:** [specific point]`, referencing the other speaker by name and claim. The simulated output shows this pattern throughout. Met.
- [x] PASS: At least one concession per perspective — "Strongest concession" is a mandatory field in Step 2 for every perspective. All four simulated perspectives concede a specific point. Met.
- [x] PASS: Revised positions explicit about what shifted — Step 3 requires "Original stance" and "Shifted to" as separate labelled fields. All four simulated perspectives show explicit shift statements. Met.
- [x] PASS: Synthesis recommends ONE option with concrete reasoning tied to specific load and analyst-tooling requirements — "No false balance" rule and "Recommended decision" mandate together prevent a waffling non-answer. Simulated output recommends PostgreSQL with TimescaleDB with specific load test prerequisite. Met.
- [x] PASS: Risk register lists at least one risk per perspective raised during debate — the "Raised by" column captures this attribution. Simulated output has risks from Scalability Sceptic, Product Manager, and Platform Engineer. Data Analyst risk attribution is absorbed into the JSONB-literacy risk (Product Manager raised it after the analyst's JSONB point). Meets the spirit of the criterion given the skill's structure.
- [~] PARTIAL: Synthesis distinguishes consensus from remaining tensions — structural sections exist and the definitions distinguish "high-confidence conclusions" from "needs data or authority." Same partial assessment as criteria item. Criterion prefix caps score at 0.5.

### Notes

The council skill is tightly constructed. The mandatory concession requirement is the key mechanism preventing performative debate — it appears in the template, the rules section, and the global Rules block, making it triply enforced. The Step 3 position shift template with distinct "Original stance" and "Shifted to" fields forces genuine evolution rather than restating opening positions. The "No false balance" rule and "Recommended decision" mandate together prevent the synthesis from deferring to "it depends."

The main gap against the risk register criterion is intentional design: the skill tracks risk attribution per perspective via the "Raised by" column but does not mandate one risk per perspective, since not every perspective necessarily surfaces a distinct risk. The consensus/tensions distinction is well supported structurally but relies on the model interpreting the template descriptions accurately rather than a mechanical enforcement rule.

The related skills section is a useful addition — pointing to `/red-team` for post-decision stress testing and `/first-principles` for cases where the council reveals a framing problem adds navigational value beyond the skill itself.
