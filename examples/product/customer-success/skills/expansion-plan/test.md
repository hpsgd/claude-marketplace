# Test: Expansion plan

Scenario: Testing whether the expansion-plan skill enforces a health prerequisite check and refuses to plan expansion for unhealthy accounts.

## Prompt


/customer-success:expansion-plan for Fenwick Capital — they're at $95k ARR and we think there's an opportunity to upsell them to our enterprise tier. They have 45 licensed seats but our data shows only 12 active users in the last 30 days.

## Criteria


- [ ] PASS: Skill performs a health prerequisite check as the FIRST step — before any expansion planning begins
- [ ] PASS: Skill flags that 12/45 active users (27% adoption) indicates an unhealthy account and recommends against expansion
- [ ] PASS: Skill refuses to produce an expansion plan for an unhealthy account — or explicitly labels any output as conditional on health improvement first
- [ ] PASS: Skill recommends a health recovery path before expansion can be attempted — what needs to improve and by how much
- [ ] PASS: Skill frames expansion as customer enablement rather than a sales motion — the reason to expand should be that the customer needs more to get more value
- [ ] PARTIAL: Skill identifies what specific signals would indicate the account is ready for expansion — partial credit if health criteria for expansion readiness are mentioned but not quantified
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields
