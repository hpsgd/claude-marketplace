# Test: Journey map

Scenario: Testing whether the journey-map skill requires evidence sources, maps all journey dimensions (actions/thinking/feeling/pain), and identifies critical moments.

## Prompt


/ux-researcher:journey-map for the customer journey from first hearing about Clearpath through to becoming an active daily user — specifically for mid-market operations directors.

## Criteria


- [ ] PASS: Skill requires defining a scope with a concrete start trigger and end outcome before mapping begins
- [ ] PASS: Skill requires identifying evidence sources (interviews, analytics, support data) before mapping — not mapping from assumptions
- [ ] PASS: Skill maps all four customer dimensions per stage: actions, thinking, feeling, and pain points
- [ ] PASS: Skill requires touchpoints and channels to be specified for each stage — not just abstract stages
- [ ] PASS: Skill identifies critical moments — stages with the highest emotional intensity or biggest impact on outcome
- [ ] PASS: Skill produces improvement recommendations linked to specific stages or pain points — not generic UX advice
- [ ] PARTIAL: Skill includes wait times and gaps as explicit journey stages — partial credit if pain points capture this but wait times are not explicitly required as steps
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields
