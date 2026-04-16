# Test: Write onboarding

Scenario: Testing whether the write-onboarding skill defines a value path before writing content, includes an "aha moment" confirmation step, and measures progress toward first value.

## Prompt


/user-docs-writer:write-onboarding for new Clearpath users — the in-product onboarding experience that takes someone from account creation to completing their first project milestone.

## Criteria


- [ ] PASS: Skill requires defining the value path first — the minimum steps to reach first value — before writing any content
- [ ] PASS: Skill requires an "aha moment" step that explicitly confirms the user has reached first value — not just "completed setup"
- [ ] PASS: Skill requires a welcome step that contextualises what the user will achieve, not just a greeting
- [ ] PASS: Each onboarding step includes the benefit to the user, not just the instruction — why this step matters
- [ ] PASS: Skill requires progress indicators so users know how far they are through onboarding
- [ ] PARTIAL: Skill addresses what happens if a user skips or abandons onboarding mid-flow — partial credit if this is mentioned but not required as a design consideration
- [ ] PASS: Skill uses plain language only — no technical terms or internal product jargon
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields
