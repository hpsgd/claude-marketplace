# Test: Write QBR

Scenario: Testing whether the write-qbr skill requires gathering account data before writing, documents value delivered in customer terms, and includes forward-looking recommendations with risks.

## Prompt


/customer-success:write-qbr for Landermere Group — $210k ARR, mid-year QBR, 18 months as a customer. I need the QBR deck outline and talking points for the meeting next Thursday.

## Criteria


- [ ] PASS: Skill requires a data gathering step before writing — usage metrics, support history, health scores, business outcomes
- [ ] PASS: Skill documents value delivered in customer outcome terms — not product usage statistics alone (e.g. "reduced report time from 4h to 20min" not "used the reports feature 340 times")
- [ ] PASS: Skill includes a forward-looking section — goals for the next quarter, not just a retrospective
- [ ] PASS: Skill identifies risks and open issues — the QBR is not only a celebration of success
- [ ] PASS: Skill produces a structured QBR document with distinct sections: value delivered, health summary, risks/recommendations, next steps
- [ ] PARTIAL: Skill includes expansion or growth conversation guidance — partial credit if upsell is mentioned but not conditioned on account health
- [ ] PASS: Skill requires next steps with owners and dates — not a general "we'll follow up"
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields
