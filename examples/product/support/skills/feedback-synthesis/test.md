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
