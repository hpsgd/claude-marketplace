# Test: Write onboarding playbook

Scenario: Testing whether the write-onboarding-playbook skill defines TTFV as a measurable customer outcome, requires escalation triggers on every milestone, and includes handoff criteria.

## Prompt


/customer-success:write-onboarding-playbook for our enterprise segment — customers with 200+ seats, dedicated IT teams, and annual contracts over $100k.

## Criteria


- [ ] PASS: Skill defines time-to-first-value (TTFV) as a customer-perceived outcome — not "completed onboarding call" but a specific product event or metric threshold
- [ ] PASS: Skill requires TTFV to be measurable automatically — if it can't be measured, the skill requires building the instrumentation first
- [ ] PASS: Every milestone has an escalation trigger with a specific day threshold — not "follow up if no response"
- [ ] PASS: Skill requires a segment definition before designing milestones — enterprise playbooks must be distinct from self-serve playbooks
- [ ] PASS: Skill includes a kickoff meeting agenda with timing, owners, and outputs per topic
- [ ] PASS: Skill defines handoff criteria as a checklist — onboarding is not complete until all criteria are met
- [ ] PARTIAL: Skill maps common blockers with early warning signs — partial credit if blockers are listed but early warning signs are not required per blocker
- [ ] PASS: Skill requires measurable success criteria for every milestone — "complete onboarding call" is explicitly rejected
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields
