# Test: Usability review

Scenario: Testing whether the usability-review skill requires Nielsen's heuristics with severity ratings, and produces a prioritised synthesis rather than a flat list of observations.

## Prompt


/ux-researcher:usability-review of our account settings area — users frequently contact support saying they can't find how to manage team members, billing, or their API keys.

## Criteria


- [ ] PASS: Skill evaluates against Nielsen's 10 usability heuristics — not a generic UX checklist
- [ ] PASS: Skill assigns severity ratings to each finding (e.g. Critical/Major/Minor/Enhancement or a numeric scale) — not a flat unrated list
- [ ] PASS: Skill requires a structured walkthrough of the interface before evaluation — scope is defined, paths are traced
- [ ] PASS: Skill produces a prioritised synthesis with the top issues identified — not just a complete catalogue of all findings
- [ ] PASS: Each finding is tied to a specific heuristic violation — not a general observation
- [ ] PARTIAL: Skill distinguishes between issues that affect task completion (blocking) and issues that affect experience quality (non-blocking) — partial credit if severity does this work implicitly
- [ ] PASS: Skill includes recommendations for each finding, not just problem statements
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields
