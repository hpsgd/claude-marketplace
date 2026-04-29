# Test: Feedback synthesis

Scenario: Testing whether the feedback-synthesis skill uses user language for themes, applies the Impact scoring formula, and produces prioritised recommendations rather than a raw catalogue.

## Prompt


/support:feedback-synthesis from 340 support tickets and 89 NPS survey responses collected over the last quarter — we want to understand what's driving friction and what product changes would have the most impact.

## Criteria


- [ ] PASS: Skill themes feedback using user language — themes are named after what users say, not internal product terminology
- [ ] PASS: Skill applies a quantified impact scoring formula — Impact = Severity × Frequency × SegmentWeight — not qualitative judgement alone
- [ ] PASS: Skill tracks trends — whether issues are increasing, stable, or decreasing — not just current volume
- [ ] PASS: Skill produces prioritised recommendations linked to themes, not just a ranked list of complaints
- [ ] PASS: Skill requires an ingest step — reading all feedback before categorising — to enable cross-source pattern detection
- [ ] PASS: Skill distinguishes between different customer segments when quantifying impact — an issue affecting enterprise customers is weighted differently from one affecting free tier users
- [ ] PARTIAL: Skill identifies feedback that indicates churn risk — partial credit if negative sentiment is tracked but churn signal is not explicitly flagged
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output processes both data sources — 340 support tickets AND 89 NPS responses — with cross-source pattern detection (a theme appearing in both is stronger signal than one in isolation)
- [ ] PASS: Output's themes are named in user language — e.g. "I can't find what I'm looking for in the dashboard" — not internal terminology like "navigation IA issues"
- [ ] PASS: Output's impact scoring formula is shown explicitly per theme — `Impact = Severity (1-3) × Frequency (count) × SegmentWeight (1-3)` — with the resulting numeric Impact score, not just "High / Medium / Low"
- [ ] PASS: Output identifies trends per theme — increasing / stable / decreasing — by comparing this quarter's volume vs previous quarter, with the math (e.g. "checkout failures: 23 last quarter, 87 this quarter — 3.8x increase")
- [ ] PASS: Output segments the impact — same volume of tickets from enterprise customers (small N, high ARR) vs free-tier customers (large N, low ARR) yields different priorities; the segment weight is named per theme
- [ ] PASS: Output's recommendations are linked to themes — each top-priority theme has an "if we did X, we'd address this signal" recommendation, not just a list of complaints reformatted as suggestions
- [ ] PASS: Output's churn-risk flagging identifies feedback signals correlated with cancellation — explicit "I'm considering switching" mentions, repeat tickets from the same account, NPS detractors — not just sentiment polarity
- [ ] PASS: Output's prioritisation recommends 3-5 specific actions for the next quarter — not "improve the product" but "fix the top-2 themes (X and Y) which together represent 35% of ticket volume"
- [ ] PASS: Output addresses theme novelty — themes that are new this quarter (didn't appear last quarter) get a "new signal" flag for early attention, even if their volume is currently lower than long-running themes
- [ ] PARTIAL: Output identifies positive feedback themes (what customers love) — synthesis isn't only about pain; positive themes inform what to protect and what to amplify in marketing
