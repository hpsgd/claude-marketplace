# Test: Design review

Scenario: Testing whether the design-review skill definition covers all six review dimensions and requires severity ratings for issues found.

## Prompt


/ui-designer:design-review of the new notification centre designs — a slide-out panel showing all user notifications with read/unread states, filtering, and bulk actions.

## Criteria


- [ ] PASS: Skill reviews across all 6 dimensions: design system consistency, component patterns, state coverage, accessibility, responsive behaviour, and code handoff quality
- [ ] PASS: Skill requires checking all 8 component states are designed — missing states are a reviewable defect, not a follow-up item
- [ ] PASS: Skill requires accessibility to be reviewed as a constraint — WCAG failures are blocking issues, not suggestions
- [ ] PASS: Skill produces findings with severity classifications (e.g. Critical/Major/Minor or Blocking/Non-blocking) — not a flat list of comments
- [ ] PASS: Skill checks for design system consistency — components that deviate without justification are flagged
- [ ] PARTIAL: Skill reviews responsive behaviour across breakpoints — partial credit if responsiveness is listed as a dimension but specific breakpoints are not required to be checked
- [ ] PASS: Skill produces a prioritised list of required changes before approval, not just observations
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields
