# Test: Churn analysis

Scenario: Testing whether the churn-analysis skill requires timeline reconstruction, root cause diagnosis, churn probability scoring, and an intervention design — not just a list of churn reasons.

## Prompt


/customer-success:churn-analysis for Bradwick & Sons who just submitted a cancellation request. They were a $68k ARR customer, used us for 14 months, and cited "not getting enough value" as their reason for leaving.

## Criteria


- [ ] PASS: Skill requires signal identification — cataloguing all available signals (usage data, support tickets, health scores, engagement) before forming hypotheses
- [ ] PASS: Skill requires timeline reconstruction — building a chronological view of the account relationship to identify when health started declining
- [ ] PASS: Skill produces a root cause diagnosis — distinguishing between product fit, onboarding failure, relationship breakdown, competitive displacement, and external factors
- [ ] PASS: Skill requires a churn probability score or risk classification, not just qualitative assessment
- [ ] PASS: Skill includes an intervention design — what could be done now to attempt recovery, if anything
- [ ] PASS: Skill requires retention economics — calculating the value of retaining vs losing this customer and comparing intervention cost
- [ ] PARTIAL: Skill feeds findings into a pattern or trend — is this churn part of a broader trend or an isolated incident — partial credit if this is mentioned but not required as a step
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields
