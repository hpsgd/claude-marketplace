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
