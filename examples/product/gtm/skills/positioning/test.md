# Test: Positioning

Scenario: Testing whether the positioning skill applies the April Dunford framework, leads with competitive alternatives, and produces a complete positioning canvas before any messaging.

## Prompt


/gtm:positioning for Clearpath Analytics — our new reporting add-on competing against native reporting in Asana and Monday.com, targeting operations directors at 50-500 person companies.

## Criteria


- [ ] PASS: Skill follows the April Dunford positioning framework — competitive alternatives first, then unique attributes, value, target customer, market category
- [ ] PASS: Skill begins with competitive alternatives as the anchor — not with product features or benefits
- [ ] PASS: Skill identifies unique attributes that only this product has relative to competitive alternatives — not general strengths
- [ ] PASS: Skill maps unique attributes to specific value for the target customer — not generic claims like "saves time"
- [ ] PASS: Skill produces a complete positioning canvas before any messaging or taglines are written
- [ ] PASS: Skill includes validation questions — criteria to test whether the positioning will hold up with real customers
- [ ] PARTIAL: Skill produces a sales narrative based on the positioning — partial credit if a narrative is mentioned as an output but not structured as a required section
- [ ] PASS: All marketing copy output is labelled DRAFT and flagged for human review
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output's competitive alternatives are listed FIRST — not features, not benefits — naming Asana native reporting, Monday.com dashboards, and the do-nothing alternative (Excel + Slack + manual rollups)
- [ ] PASS: Output's unique attributes are differentiating relative to those alternatives — not "we have dashboards" (Asana has dashboards) but "executive summary auto-generation that other reporting tools don't do natively" — concrete and verifiable
- [ ] PASS: Output maps each unique attribute to specific customer value — e.g. "auto-generated weekly exec summaries → operations director saves 4-6 hours/week + delivers consistent exec reporting" — not "saves time"
- [ ] PASS: Output's target customer is precise — "operations directors at 50-500 person companies who own portfolio-level project visibility and report up to a CEO/COO" — not "businesses that want better reporting"
- [ ] PASS: Output's market category is named explicitly — "executive project portfolio reporting" or "operations intelligence for project-led teams" — not "project management software"
- [ ] PASS: Output's positioning canvas covers all five Dunford elements — competitive alternatives, unique attributes, value, target customer, market category — in a structured layout, not prose
- [ ] PASS: Output's validation questions test whether real customers will recognise the positioning — e.g. "do operations directors describe their alternative as Asana reporting, or as Excel rollups?" — concrete questions that can be answered by 5-10 customer conversations
- [ ] PASS: Output's sales narrative (if produced) follows the canvas — opens with the competitive alternative pain, transitions to the unique attributes, lands on customer value, names the category — not a generic problem-solution-product structure
- [ ] PASS: Output labels every customer-facing tagline / message draft — DRAFT, requires human review — not approved finals
- [ ] PARTIAL: Output addresses where the canvas may shift on pricing — analytics add-on at $15/seat positions Clearpath as a premium overlay (suggesting the buyer values exec visibility highly) which informs the pricing message and channel
