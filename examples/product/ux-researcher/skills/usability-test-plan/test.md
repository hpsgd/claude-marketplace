# Test: Usability test plan

Scenario: Testing whether the usability-test-plan skill requires defined research questions, participant criteria, task scenarios, and success metrics — not just a list of questions to ask.

## Prompt


/ux-researcher:usability-test-plan for testing our new onboarding flow before we ship it — we want to know if new users can get to their first project within 10 minutes without help.

## Criteria


- [ ] PASS: Skill requires specific research questions (what will we learn?) before methodology selection — not "we'll run usability tests and see what happens"
- [ ] PASS: Skill requires participant screener criteria — who qualifies to participate, who should be excluded
- [ ] PASS: Skill requires task scenarios written from the user's perspective, not the product's perspective (e.g. "You've just joined a new company..." not "Navigate to onboarding")
- [ ] PASS: Skill requires success metrics defined per task — completion rate, time-on-task, or error rate — not just "did they complete it"
- [ ] PASS: Skill includes a moderator guide with specific prompts and a policy on when to intervene
- [ ] PASS: Skill specifies the number of participants with a rationale — not an arbitrary number
- [ ] PARTIAL: Skill covers logistics — session duration, recording consent, tools — partial credit if logistics are mentioned but not all required elements are present
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields
