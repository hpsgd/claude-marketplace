# Test: Design review

Scenario: Testing whether the design-review skill definition covers all six review dimensions and requires severity ratings for issues found.

## Prompt


/ui-designer:design-review of the new notification centre designs — a slide-out panel showing all user notifications with read/unread states, filtering, and bulk actions.

## Criteria


- [ ] PASS: Skill reviews across all 6 dimensions: design system consistency, component patterns, state coverage, accessibility, responsive behaviour, and code handoff quality
- [ ] PASS: Skill requires checking all 8 component states are designed — missing states are a reviewable defect, not a follow-up item
- [ ] PASS: Skill requires accessibility to be reviewed as a constraint — WCAG failures are blocking issues, not suggestions
- [ ] PASS: Skill produces findings with severity classifications (e.g. Critical/Major/Minor, Blocking/Non-blocking, or Blockers/Suggestions/Nits) — not a flat list of comments
- [ ] PASS: Skill checks for design system consistency — components that deviate without justification are flagged
- [ ] PARTIAL: Skill reviews responsive behaviour across breakpoints — partial credit if responsiveness is listed as a dimension but specific breakpoints are not required to be checked
- [ ] PASS: Skill produces a prioritised list of required changes before approval, not just observations
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output reviews the slide-out notification panel across all 6 dimensions explicitly — design system consistency, component patterns, state coverage, accessibility, responsive behaviour, code handoff quality — with at least one finding or "no issues" per dimension
- [ ] PASS: Output verifies all 8 component states are designed for the panel and notification items — Default, Hover (on a notification row), Focus (keyboard focus), Active (clicking), Disabled, Loading (notifications fetching), Error (fetch failed), Empty (no notifications) — flagging any missing state as a blocking/major finding
- [ ] PASS: Output reviews the read/unread state contrast — unread notifications must be distinguishable from read ones with sufficient contrast (not just colour, also typography weight or icon), per WCAG 1.4.1 (not relying on colour alone)
- [ ] PARTIAL: Output reviews the filtering interaction — partial credit if live regions or screen reader announcement mechanisms are covered generally; full credit if the active filter visibility and empty filtered states are addressed specifically
- [ ] PASS: Output's findings each have a severity classification (Critical / Major / Minor, Blocking / Non-blocking, or Blockers / Suggestions / Nits) — top tier includes WCAG failures and broken state coverage; bottom tier includes spacing or visual nits
- [ ] PASS: Output flags any deviation from the design system — components that look custom but aren't documented as new primitives, colour values not in the token system, spacing not on the grid
- [ ] PASS: Output's required-changes list is prioritised — Critical findings (WCAG or broken state) listed first as blockers, Major (UX issue or system inconsistency) next, Minor (polish) last — and approval is conditional on Critical+Major being addressed
- [ ] PARTIAL: Output addresses code handoff quality — does the design include redlines / specs that engineers can implement without ambiguity, or are spacing values implied rather than measured
