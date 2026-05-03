# Test: write-adr skill structure

Scenario: Checking that the write-adr skill produces ADRs that follow the MADR format with all required sections, honest trade-offs, and measurable confirmation criteria.

## Prompt

Review the write-adr skill definition and verify it produces complete, honest ADR documents rather than decision justifications written after the fact.

Read the skill at `/Users/martin/Projects/turtlestack/plugins/engineering/architect/skills/write-adr/SKILL.md` and verify each item by name. Quote skill text where present:

- **MADR format with all key sections (8)**: frontmatter (`status`, `date`, `decision-makers`), `Context`, `Decision Drivers`, `Considered Options`, `Decision Outcome`, `Consequences`, `Confirmation`, and per-option `Pros and Cons`. Enumerate all eight by name.
- **Title rule**: ADR title must describe both the **problem** and the **solution** (e.g. "0007-payment-rate-limiting-via-redis-token-bucket" not "0007-redis"). Not just naming the technology.
- **At-least-two-options rule** including **"do nothing / status quo"** where applicable. Strawman alternatives are an anti-pattern.
- **Confirmation criteria must be measurable/observable** — a metric, an automated test, a reconsideration trigger, or a review date with associated condition. Not aspirational text or a bare review date.
- **File naming convention**: `NNNN-kebab-case-title.md` (4-digit prefix), target directory `docs/adr/` (or equivalent stated path).
- **Anti-patterns named (4)**: (1) **Retroactive ADR** (writing after decision already implemented), (2) **No alternatives** (single-option ADR), (3) **Strawman options** (intentionally weak alternatives), (4) **Orphaned ADR** with no confirmation criteria.
- **Identified gaps**: any of — no guidance on superseded ADR linkage, no template for revision notes when an ADR is updated, no explicit author/reviewer field.

Confirm or flag each by name.

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
