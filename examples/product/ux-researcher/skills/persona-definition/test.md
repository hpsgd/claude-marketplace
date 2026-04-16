# Test: Persona definition

Scenario: Testing whether the persona-definition skill requires evidence-based personas with validated segments, and explicitly prohibits demographic stereotyping.

## Prompt


/ux-researcher:persona-definition for the primary users of our project management tool — we think we have 3-4 distinct user types based on how they use the product differently.

## Criteria


- [ ] PASS: Skill requires an evidence inventory step before writing personas — existing research, analytics, interviews, or support data must be catalogued first
- [ ] PASS: Skill explicitly prohibits basing personas on demographic stereotypes — age, gender, and background are not valid differentiators unless backed by evidence
- [ ] PASS: Skill requires segment validation — each persona must be supported by a meaningful cluster of real user behaviour, not just intuition
- [ ] PASS: Skill requires each persona to describe goals, pain points, and behaviours — not just a demographic profile with a stock photo description
- [ ] PASS: Skill includes a validation checklist to verify personas are grounded in evidence, not assumptions
- [ ] PARTIAL: Skill requires a jobs-to-be-done or goals section per persona that is solution-agnostic — partial credit if goals are required but they could be solution-specific
- [ ] PASS: Skill warns against creating too many personas — and provides guidance on when sub-segments should be merged vs kept separate
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields
