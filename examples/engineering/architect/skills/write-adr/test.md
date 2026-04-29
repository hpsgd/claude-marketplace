# Test: write-adr skill structure

Scenario: Checking that the write-adr skill produces ADRs that follow the MADR format with all required sections, honest trade-offs, and measurable confirmation criteria.

## Prompt

Review the write-adr skill definition and verify it produces complete, honest ADR documents rather than decision justifications written after the fact.

## Criteria

- [ ] PASS: Skill uses the MADR format and requires all key sections: frontmatter (status, date, decision-makers), context, decision drivers, considered options, decision outcome, consequences, confirmation, and pros/cons per option
- [ ] PASS: Skill requires the ADR title to describe both the problem and the solution — not just the technology chosen
- [ ] PASS: Skill mandates at least two options including "do nothing / status quo" where applicable
- [ ] PASS: Skill requires consequences to include at least one negative — with an explicit honesty check that every decision has downsides
- [ ] PASS: Skill requires measurable or observable confirmation criteria — a review date, metric, automated test, or reconsideration trigger
- [ ] PASS: Skill provides a quality checklist before declaring the ADR complete
- [ ] PASS: Skill lists anti-patterns including retroactive ADR, no alternatives, strawman options, and orphaned ADR with no confirmation criteria
- [ ] PASS: Skill specifies file naming convention (NNNN-kebab-case-title.md) and target directory (docs/adr/ or similar)

## Output expectations

- [ ] PASS: Output is structured as a verification of the skill (verdict per requirement) rather than producing a sample ADR
- [ ] PASS: Output confirms the MADR sections are all named explicitly: status/date/decision-makers frontmatter, context, decision drivers, considered options, decision outcome, consequences, confirmation, and per-option pros/cons
- [ ] PASS: Output verifies the title rule — title must describe both problem and solution, not just the chosen technology
- [ ] PASS: Output confirms the at-least-two-options rule, including "do nothing / status quo" where applicable, and that strawman alternatives are flagged as an anti-pattern
- [ ] PASS: Output verifies the negative-consequences honesty rule — every decision must list at least one negative
- [ ] PASS: Output confirms confirmation criteria must be measurable/observable (review date, metric, automated test, or reconsideration trigger) — not aspirational text
- [ ] PASS: Output verifies the file naming convention (NNNN-kebab-case-title.md) and target directory (docs/adr/) are stated, with the four-digit prefix and kebab-case explicit
- [ ] PASS: Output verifies the anti-patterns list includes retroactive ADR, no alternatives, strawman options, and orphaned ADRs without confirmation criteria
- [ ] PARTIAL: Output identifies any gaps — e.g. no guidance on superseded ADR linkage, no template for revision notes when an ADR is updated, or no explicit author/reviewer field
