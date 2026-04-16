# Test: Service blueprint

Scenario: Testing whether the service-blueprint skill requires both frontstage and backstage lanes, a line of visibility, failure point analysis, and improvement recommendations.

## Prompt


/ux-researcher:service-blueprint for our enterprise customer onboarding process — from contract signed to customer achieving first value, including everything our CS, solutions engineering, and support teams do behind the scenes.

## Criteria


- [ ] PASS: Skill requires a scope definition with a concrete start event and end outcome before mapping begins
- [ ] PASS: Skill maps all four required lanes: customer actions, frontstage employee actions, backstage employee actions, and support processes
- [ ] PASS: Skill explicitly draws the line of visibility separating what customers see from what they don't
- [ ] PASS: Skill includes a visibility audit — identifying what backstage work becomes visible to customers and whether that's intentional
- [ ] PASS: Skill requires failure point analysis with location, failure mode, customer impact, frequency, and root cause
- [ ] PASS: Skill requires each backstage action to have a trigger — no orphaned process steps
- [ ] PARTIAL: Skill requires duration estimates for backstage actions — partial credit if duration is mentioned as important but not required per step
- [ ] PASS: Skill produces prioritised improvement recommendations linked to specific failure points
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields
