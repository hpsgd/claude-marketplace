# Output: Design review

**Verdict:** FAIL
**Score:** 12/18 criteria met (67%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill reviews across all 6 dimensions: design system consistency, component patterns, state coverage, accessibility, responsive behaviour, and code handoff quality — all six present as named sections
- [x] PASS: Skill requires checking all 8 component states — Default, Hover, Focus, Active, Disabled, Loading, Error, Empty are all listed explicitly in Dimension 3
- [~] PARTIAL: Skill requires accessibility to be reviewed as a constraint — the output format places accessibility failures in "Blockers (must fix before merge)" which functionally treats them as blocking, but no explicit policy statement says "WCAG failures are blocking issues, not suggestions"
- [x] PASS: Skill produces findings with severity classifications — three levels: Blockers, Suggestions, Nits
- [x] PASS: Skill checks for design system consistency — Dimension 1 covers colour, typography, spacing, border radius with grep checks
- [~] PARTIAL: Skill reviews responsive behaviour across breakpoints — Dimension 5 lists Tailwind breakpoint prefixes (sm/md/lg/xl) and common responsive issues, but does not require specific named pixel breakpoints to be checked
- [x] PASS: Skill produces a prioritised list of required changes before approval — output format has Blockers first, then Suggestions, then Nits, with a Verdict field
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — all three present

### Output expectations

- [x] PASS: Output reviews the notification panel across all 6 dimensions — skill structure drives this; each dimension is a required section
- [~] PARTIAL: Output verifies all 8 component states for the panel and notification items — Dimension 3 lists all 8 states, but the criterion requires flagging missing states as "Major" and the skill uses "Blockers" — severity naming mismatch
- [~] PARTIAL: Output reviews read/unread contrast per WCAG 1.4.1 — Dimension 4 covers contrast ratios (4.5:1 for normal text) but does not reference WCAG 1.4.1 (use of colour) or require distinguishing states by more than colour alone
- [~] PARTIAL: Output reviews filtering interaction for screen reader announcements — Dimension 4 mentions live regions for dynamic updates, which covers the mechanism, but filtering-specific announcement requirements are not called out
- [ ] FAIL: Output reviews bulk actions — select all, per-item selection, bulk-action toolbar, bulk dismiss with undo affordance — the skill has no coverage of bulk action patterns or irreversible action affordances anywhere
- [~] PARTIAL: Output findings have severity classification Critical/Major/Minor or Blocking/Non-blocking — the skill uses Blockers/Suggestions/Nits, which covers the same tiers but does not match the named levels the criterion specifies
- [x] PASS: Output flags design system deviations — Dimension 1 explicitly checks for custom components, hardcoded colour values, and spacing off the token system
- [~] PARTIAL: Output reviews responsive behaviour at named breakpoints with mobile full-screen overlay pattern — Dimension 5 covers responsive issues generically but does not require specific pixel breakpoints (1440/1024/375) or address slide-out-to-full-screen-overlay transitions
- [x] PASS: Output's required-changes list is prioritised with blockers first — Blockers section is first in the output format, Verdict is conditional on addressing them
- [~] PARTIAL: Output addresses code handoff quality — Dimension 6 covers code structure and performance, but the criterion asks about design spec quality (redlines, measured spacing, implementation-ready annotations) which the skill does not address

## Notes

The skill is designed for reviewing implementation code against a design system, not for reviewing design files. The output expectations section asks for behaviours suited to a design-file review — redlines, whether spacing values are measured, Figma spec quality. That mismatch accounts for most of the output expectation failures. The bulk action criterion is a genuine gap in the skill regardless: complex interactive patterns with irreversible actions and undo affordances are not covered anywhere. The skill's three-tier severity model (Blockers/Suggestions/Nits) maps conceptually to Critical/Major/Minor but the naming difference causes partial-credit failures across multiple criteria.
