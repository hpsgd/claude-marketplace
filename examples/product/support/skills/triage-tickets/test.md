# Test: Triage tickets

Scenario: Testing whether the triage-tickets skill classifies tickets across all required dimensions, includes pattern detection, and produces a structured triage table.

## Prompt


/support:triage-tickets for this batch of 18 new support tickets received overnight, ranging from billing questions to feature requests to what appear to be related login errors from multiple customers.

## Criteria


- [ ] PASS: Skill classifies each ticket across multiple dimensions — category (bug/question/feature/billing), severity, and routing destination
- [ ] PASS: Skill includes pattern detection — when 3 or more tickets match the same root issue, they should be grouped and escalated
- [ ] PASS: Skill generates a bug report or incident escalation for patterns that suggest a systemic issue — not just individual ticket responses
- [ ] PASS: Skill produces a structured triage table as output — not a prose summary of the ticket queue
- [ ] PASS: Skill requires an ingest step — reading all tickets before classifying any — to enable pattern detection across the full batch
- [ ] PARTIAL: Skill assigns a response SLA or priority to each ticket — partial credit if severity classification does this work implicitly
- [ ] PASS: Skill routes tickets to appropriate teams or owners, not just classifies them
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields
