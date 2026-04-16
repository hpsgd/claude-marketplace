# Test: Write runbook

Scenario: Testing whether the write-runbook skill requires copy-pasteable commands, rollback steps for every destructive action, and an escalation table with specific contacts.

## Prompt


/internal-docs-writer:write-runbook for our database failover procedure — promoting the read replica to primary when the primary instance becomes unavailable.

## Criteria


- [ ] PASS: Skill is explicitly written for a first-timer at 2am — no assumed knowledge, all commands copy-pasteable with expected output shown
- [ ] PASS: Every command includes the expected output so the engineer knows whether it worked
- [ ] PASS: Skill requires a rollback step for every destructive or hard-to-reverse action
- [ ] PASS: Skill requires an escalation table with named roles, contact methods, and when to escalate — not "escalate if needed"
- [ ] PASS: Skill requires a verification step at the end — how to confirm the runbook succeeded and the system is healthy
- [ ] PASS: Skill requires a research step — reading existing code, configs, or infrastructure before writing the runbook
- [ ] PARTIAL: Skill requires severity classification or impact context at the top — partial credit if business impact is mentioned but not required as a runbook header field
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields
