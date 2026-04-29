# Output: write-adr skill structure

**Verdict:** PASS
**Score:** 16.5/17 criteria met (97%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill uses the MADR format and requires all key sections: frontmatter (status, date, decision-makers), context, decision drivers, considered options, decision outcome, consequences, confirmation, and pros/cons per option — all sections named explicitly under Step 3, labelled "(none optional)"
- [x] PASS: Skill requires the ADR title to describe both the problem and the solution — stated directly ("describes the problem AND solution") with three concrete examples: one good, two bad
- [x] PASS: Skill mandates at least two options including "do nothing / status quo" where applicable — "At least 2 options. Always include 'do nothing / status quo' if applicable"
- [x] PASS: Skill requires consequences to include at least one negative with an explicit honesty check — "What gets worse (every decision has downsides — if you can't name one, you haven't thought hard enough)" reinforced in the quality checklist
- [x] PASS: Skill requires measurable or observable confirmation criteria — four concrete forms: review date, metric to watch, automated test or CI check, conditions that trigger revisiting
- [x] PASS: Skill provides a quality checklist before declaring the ADR complete — nine-item checklist covering title, context, options, decision drivers, consequences, risks, confirmation, rejected option fairness, and related ADR linkage
- [x] PASS: Skill lists anti-patterns including retroactive ADR, no alternatives, strawman options, and orphaned ADR with no confirmation criteria — all four present in the anti-patterns table with problem and fix columns
- [x] PASS: Skill specifies file naming convention (NNNN-kebab-case-title.md) and target directory (docs/adr/) — four-digit prefix, kebab-case, `.md` extension, and `docs/adr/` as primary target with fallback detection and creation instructions

### Output expectations

- [x] PASS: Output is structured as a verification of the skill (verdict per requirement) rather than producing a sample ADR
- [x] PASS: Output confirms the MADR sections are all named explicitly — status/date/decision-makers frontmatter (skill also includes consulted and informed), context and problem statement, decision drivers, considered options, decision outcome, consequences with three sub-categories (positive/negative/risks), confirmation, and per-option pros/cons using Good/Bad/Neutral structure
- [x] PASS: Output verifies the title rule — skill states the title must describe both problem and solution, with explicit good/bad examples showing vague-title and solution-only-title as failures
- [x] PASS: Output confirms the at-least-two-options rule including "do nothing / status quo" where applicable, and that strawman alternatives are flagged as an anti-pattern in the skill's anti-patterns table
- [x] PASS: Output verifies the negative-consequences honesty rule — skill's "every decision has downsides" phrasing is specific and appears in two places: the Consequences section and the quality checklist
- [x] PASS: Output confirms confirmation criteria must be measurable/observable — skill lists four concrete mechanism types rather than aspirational language, and the quality checklist item explicitly uses the words "measurable or observable"
- [x] PASS: Output verifies file naming convention (NNNN-kebab-case-title.md) and target directory (docs/adr/) with four-digit prefix and kebab-case explicit — confirmed in the Output section with a concrete filename example
- [x] PASS: Output verifies anti-patterns list includes all four: retroactive ADR, no alternatives, strawman options, and orphaned ADRs without confirmation criteria — all present in the anti-patterns table
- [~] PARTIAL: Output identifies gaps — the skill references "Related ADRs are linked (supersedes, builds on, relates to)" in the quality checklist but gives no convention for updating a superseded ADR's own status field (e.g., setting it to "superseded by ADR-NNNN"). There is no guidance on revision notes if an ADR's status changes after acceptance. The frontmatter includes `decision-makers`, `consulted`, and `informed` but no separate `author` field — relevant when the author differs from the decision-makers. These are genuine gaps, though the quality checklist reference to related ADR linkage partially addresses the supersession concern.

## Notes

The skill is well-structured. The honesty-forcing mechanisms — mandatory negative consequences with the "if you can't name one, you haven't thought hard enough" phrase, the anti-strawman rule, and the orphaned ADR anti-pattern — are specific enough to catch the most common ADR failure modes in practice.

The template reference (`${CLAUDE_PLUGIN_ROOT}/templates/adr-template.md`) delegates some structure to an external file not evaluated here. The inline section instructions in SKILL.md are detailed enough to stand alone if that template is absent.

The quality checklist item "Rejected options have fair representation (not strawmen)" overlaps with but extends the anti-patterns table — it catches cases where options were described accurately but were never genuinely considered, which the anti-pattern label alone doesn't cover. That's a useful distinction.
