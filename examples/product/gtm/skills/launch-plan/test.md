# Test: Launch plan

Scenario: Testing whether the launch-plan skill determines a launch tier, produces a structured rollout strategy, and requires a post-launch review plan with success metrics.

## Prompt


/gtm:launch-plan for our mobile app — we're releasing native iOS and Android apps after 3 years of web-only. This is a significant milestone for us and for our customers who've been requesting it.

## Criteria


- [ ] PASS: Skill determines a launch tier before planning — a 3-year milestone mobile launch is not a silent rollout, and the tier determines resource allocation and communication scope
- [ ] PASS: Skill produces a pre-launch checklist — internal readiness, support preparation, documentation — not just external marketing
- [ ] PASS: Skill produces a rollout strategy — phased or full launch, criteria for advancing phases
- [ ] PASS: Skill requires a post-launch review plan with defined success metrics and a review date
- [ ] PASS: Skill includes a communication plan — who is told what, when, and through which channel
- [ ] PASS: All marketing copy and messaging is labelled DRAFT and flagged for human review
- [ ] PARTIAL: Skill includes a launch day checklist — specific actions on the day of release — partial credit if launch day is covered in the rollout strategy but not as a separate checklist
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields
