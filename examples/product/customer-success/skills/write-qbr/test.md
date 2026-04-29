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

## Output expectations

- [ ] PASS: Output's data gathering step lists the specific data sources needed for Landermere — usage metrics over the last 6 months, support ticket history, health scores, executive contacts attended/missed in prior QBRs, contract details ($210k ARR, 18-month tenure)
- [ ] PASS: Output's value-delivered section uses customer-outcome language — e.g. "saved 12 FTE hours per week on report generation", "reduced order-processing errors by 22%" — NOT "logged in 3,400 times" or "used the dashboard 47 times"
- [ ] PASS: Output's value section quantifies outcomes with before/after metrics — not "improved efficiency", but "reduced report compilation from 4 hours to 20 minutes per report"
- [ ] PASS: Output's forward-looking section sets goals for the next quarter — at least 2-3 specific, measurable customer outcomes Landermere wants to achieve, not "continue using the platform"
- [ ] PASS: Output's risks/issues section is honest — flags any deteriorating signals (declining MAU, missed deadlines, executive sponsor changes) and presents them, not just successes
- [ ] PASS: Output's structure follows the named sections — Value Delivered, Health Summary, Risks/Recommendations, Next Steps — visible in the deck outline, not buried
- [ ] PASS: Output's expansion / growth conversation guidance is conditional on health — if Landermere is healthy, opportunities are surfaced; if not, expansion is held back with reasoning
- [ ] PASS: Output's next steps each have an owner (named person, not "the team") and a date — at minimum 3 actionable next steps, not "we'll follow up next quarter"
- [ ] PASS: Output's deck outline is structured for a meeting (10-15 slides typical) with talking points per slide, not a Word document
- [ ] PARTIAL: Output addresses 18-month tenure context — Landermere is past first-year wow factor, so the QBR should focus on year-2 value-articulation and not just feature adoption
