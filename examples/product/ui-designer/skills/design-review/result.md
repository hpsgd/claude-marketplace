# Output: Design review

**Verdict:** PASS
**Score:** 14.5/16 criteria met (91%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill reviews across all 6 dimensions: design system consistency, component patterns, state coverage, accessibility, responsive behaviour, and code handoff quality — met; all six present as named dimensions
- [x] PASS: Skill requires checking all 8 component states — met; Dimension 3 explicitly lists Default, Hover, Focus, Active, Disabled, Loading, Error, Empty and the output format routes missing states into Blockers
- [x] PASS: Skill requires accessibility to be reviewed as a constraint — met; Dimension 4 opens with "WCAG failures are blocking issues, not suggestions" as an explicit policy statement
- [x] PASS: Skill produces findings with severity classifications — met; three-tier output: Blockers / Suggestions / Nits
- [x] PASS: Skill checks for design system consistency — met; Dimension 1 covers colour tokens, type scale, spacing scale, and border radius with grep checks flagging deviations
- [~] PARTIAL: Skill reviews responsive behaviour across breakpoints — partially met; Dimension 5 references Tailwind breakpoint prefixes (sm/md/lg/xl) and common responsive issues, but does not require specific named breakpoints to be checked — partial credit per criterion
- [x] PASS: Skill produces a prioritised list of required changes before approval — met; Blockers section is first in the output format and the Verdict is gated on blockers being resolved
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — met; all three fields present

### Output expectations

- [x] PASS: Output reviews the slide-out notification panel across all 6 dimensions explicitly — met by definition; each dimension is a mandatory review section, so a well-formed execution would produce at least one finding or "no issues" per dimension
- [x] PASS: Output verifies all 8 component states for the panel and notification items — met; Dimension 3 lists all 8 states and routes missing ones into Blockers (blocking/major equivalent)
- [x] PASS: Output reviews read/unread contrast per WCAG 1.4.1 — met; Dimension 4 Contrast section explicitly states "State differences (read/unread, selected/unselected, error/valid) are not conveyed by colour alone — combine with typography weight, icon, or text label per WCAG 1.4.1"
- [~] PARTIAL: Output reviews the filtering interaction including live regions and empty filtered states — partially met; Dimension 4 covers live regions for dynamic updates and Dimension 3 covers empty states, but filtering-specific empty state and active filter visibility are not called out explicitly — partial credit per criterion
- [x] PASS: Output findings each have a severity classification — met; output format requires every finding to appear under Blockers, Suggestions, or Nits with top tier holding WCAG failures and broken state coverage
- [x] PASS: Output flags any deviation from the design system — met; Dimension 1 explicitly checks for hardcoded colours, arbitrary spacing, and components that deviate from tokens
- [x] PASS: Output's required-changes list is prioritised — met; Blockers listed first, Suggestions next, Nits last, and approval is conditional on Blockers being addressed
- [~] PARTIAL: Output addresses code handoff quality — partially met; Dimension 6 is labelled "Code Quality" and covers TypeScript types, props API, and component structure, but does not address design handoff quality (redlines, measured vs implied spacing, implementation-ready annotations from a design file perspective)

## Notes

The skill is oriented toward reviewing code against a design system, not reviewing design files for handoff readiness. The code-handoff output criterion partially misaligns with that scope — Dimension 6 covers code implementation quality, not whether a Figma file has accurate spacing annotations. That gap accounts for the partial on the last criterion. Everything else is solid: the WCAG 1.4.1 read/unread callout is an explicit strength, the eight-state requirement is clear, and the blocking-by-default policy for accessibility is stated plainly.
