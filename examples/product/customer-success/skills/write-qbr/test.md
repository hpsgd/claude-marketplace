# Test: Write QBR

Scenario: Testing whether the write-qbr skill requires gathering account data before writing, documents value delivered in customer terms, and includes forward-looking recommendations with risks.

## Prompt


/customer-success:write-qbr for Landermere Group — $210k ARR, mid-year QBR, 18 months as a customer. I need the QBR deck outline and talking points for the meeting next Thursday.

Pre-fill the data placeholders with the following Landermere data so the QBR is account-specific (don't leave [DATA NEEDED] gaps):

- **Usage**: H2 2025 MAU averaged 142, H1 2026 MAU averaged 168 (+18%). Seat utilisation 78% (28 of 36 licensed seats active in last 30 days).
- **Support**: 14 tickets in H1 2026, 2 P2 incidents (both resolved within SLA), zero P1.
- **Health score**: 7.2/10 — Yellow. Slight decline from 7.8 last QBR.
- **Executive sponsor**: Champion Priya Sharma (VP Operations); exec sponsor Michael Chen (COO) attended last QBR but missed the previous one.
- **Goals from last QBR**: (1) integrate with their Snowflake instance, (2) onboard the procurement team (12 seats).

A few specifics for the response:

- **Format as a deck outline**: numbered slides 1-12 with `Slide N: <Title>` followed by 3-4 bullet talking points per slide. Not a narrative reference document.
- **Goals for next quarter** — at least 3 Landermere-specific, measurable goals (using the data above), each with named owner (use `Champion: Priya Sharma`, `Us: <named CSM>`, or `Shared`) and a date.
- **Year-2 framing**: explicitly pivot the QBR away from year-1 feature-adoption framing to year-2 strategic-value-articulation. Title at least one section "Year-2 Value Realisation" or equivalent.
- **Risks/issues**: name the actual deteriorating signals (health score drop 7.8 → 7.2, exec sponsor attendance gap last QBR) — don't leave placeholder.
- **Pre-meeting checklist** with named owner (e.g. "CSM: Pull usage metrics") and Thursday deadline.

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
