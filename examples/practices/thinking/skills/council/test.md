# Test: council database selection debate

Scenario: A team needs to choose between PostgreSQL and MongoDB for a new event-driven analytics platform. The council skill is invoked to debate the options with multiple competing perspectives.

## Prompt

/council Should we use PostgreSQL or MongoDB for the new analytics platform? We're storing user behaviour events (high write volume, ~50k events/min at peak), and the data analysts need ad-hoc SQL queries. The engineering team is more comfortable with Postgres but the product manager thinks MongoDB's flexible schema will speed up iteration.

## Criteria

- [ ] PASS: Skill selects exactly 4 perspectives with genuinely different stances — at least 2 in direct tension with each other
- [ ] PASS: Each perspective states a core argument, primary concern, and explicit trade-off they accept in Step 1
- [ ] PASS: Each perspective in Step 2 engages with a specific claim from at least one other perspective — not just restates their own position
- [ ] PASS: Every perspective makes at least one concession in the debate — a debate with zero concessions is flagged as performative by the skill's own rules
- [ ] PASS: Step 3 shows revised positions with explicit description of what shifted from the opening stance
- [ ] PASS: Step 4 synthesis produces a concrete recommendation with reasoning, not just "it depends"
- [ ] PASS: Risk register in the synthesis includes at least one risk per perspective raised during debate
- [ ] PARTIAL: Synthesis correctly distinguishes between points of genuine consensus vs remaining tensions that need data or authority to resolve

## Output expectations

- [ ] PASS: Output's four perspectives are named with distinct, role-grounded identities (e.g. "Database engineer focused on operational reliability", "Data analyst focused on ad-hoc query speed", "Engineering manager focused on team velocity", "Product manager focused on schema flexibility") — not labelled "Perspective 1, 2, 3, 4"
- [ ] PASS: Output's perspectives include genuine tension — at least one strongly pro-Postgres voice and at least one strongly pro-MongoDB voice — not four variants of the same lukewarm stance
- [ ] PASS: Output addresses the 50k events/min peak write requirement explicitly — analysing whether each option handles that throughput, with reasoning grounded in the technology (Postgres with appropriate write paths, partitioning, BRIN indexes vs MongoDB sharded write fan-out)
- [ ] PASS: Output addresses the ad-hoc SQL requirement — pointing out that MongoDB's ad-hoc query story is weaker for analysts who expect SQL, and that Postgres's `JSONB` columns can give "schema flexibility" without giving up SQL
- [ ] PASS: Output's engagement step shows perspectives quoting or referencing each other's specific claims — e.g. "the data analyst's point about ad-hoc SQL undermines my flexibility argument because..."
- [ ] PASS: Output shows at least one concession per perspective — a moment where the speaker admits an opposing point has merit and adjusts their position, not pure restatement
- [ ] PASS: Output's revised positions are explicit about what shifted — "I started favouring MongoDB on flexibility, but I've come around on Postgres `JSONB` for that" — not implicit
- [ ] PASS: Output's synthesis recommends ONE option (likely Postgres given the constraints) with concrete reasoning tied to the specific load and analyst-tooling requirements — not "it depends on your priorities"
- [ ] PASS: Output's risk register lists at least one risk per perspective raised during the debate — capturing what the rejected perspectives warned about that could still bite
- [ ] PARTIAL: Output's synthesis distinguishes consensus (e.g. "all perspectives agree the team's Postgres familiarity is real value") from remaining tensions (e.g. "schema flexibility is a real cost — needs migration tooling investment regardless of choice")
