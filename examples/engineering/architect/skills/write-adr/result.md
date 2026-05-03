# Write Adr

Scenario: Checking that the write-adr skill produces ADRs that follow the MADR format with all required sections, honest trade-offs, and measurable confirmation criteria.

## Prompt

> Review the write-adr skill definition and verify it produces complete, honest ADR documents rather than decision justifications written after the fact.
> 
> Read the skill at `/Users/martin/Projects/turtlestack/plugins/engineering/architect/skills/write-adr/SKILL.md` and verify each item by name. Quote skill text where present:
> 
> - **MADR format with all key sections (8)**: frontmatter (`status`, `date`, `decision-makers`), `Context`, `Decision Drivers`, `Considered Options`, `Decision Outcome`, `Consequences`, `Confirmation`, and per-option `Pros and Cons`. Enumerate all eight by name.
> - **Title rule**: ADR title must describe both the **problem** and the **solution** (e.g. "0007-payment-rate-limiting-via-redis-token-bucket" not "0007-redis"). Not just naming the technology.
> - **At-least-two-options rule** including **"do nothing / status quo"** where applicable. Strawman alternatives are an anti-pattern.
> - **Confirmation criteria must be measurable/observable** — a metric, an automated test, a reconsideration trigger, or a review date with associated condition. Not aspirational text or a bare review date.
> - **File naming convention**: `NNNN-kebab-case-title.md` (4-digit prefix), target directory `docs/adr/` (or equivalent stated path).
> - **Anti-patterns named (4)**: (1) **Retroactive ADR** (writing after decision already implemented), (2) **No alternatives** (single-option ADR), (3) **Strawman options** (intentionally weak alternatives), (4) **Orphaned ADR** with no confirmation criteria.
> - **Identified gaps**: any of — no guidance on superseded ADR linkage, no template for revision notes when an ADR is updated, no explicit author/reviewer field.
> 
> Confirm or flag each by name.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Verification Results

**Summary: 5 of 6 verified items ✓, 1 critical gap ✗**

### ✓ Verified Items

**1. MADR Format with All 8 Key Sections**

All eight sections present and named:
1. Frontmatter (status, date, decision-makers, consulted, informed) — lines 47–55
2. Context and Problem Statement — lines 64–69
3. Decision Drivers — lines 72–73
4. Considered Options — lines 75–76
5. Decision Outcome — lines 78–81
6. Consequences — lines 83–87
7. Confirmation — lines 89–94
8. Pros and Cons of Options — lines 96–100

**2. Title Rule (Problem + Solution)**

Explicitly stated in lines 57–62:
> `# ADR-NNNN: {Short title — describes the problem AND solution}`
> 
> Good: "ADR-0005: Use PostgreSQL BYTEA for binary content storage"
> Bad: "ADR-0005: Database decision" (too vague)
> Bad: "ADR-0005: We should use PostgreSQL" (no problem stated)

Quality checklist reinforces (line 106): "Title describes both the problem and the solution"

**3. At-Least-Two-Options Rule + "Do Nothing"**

Lines 75–76:
> "At least 2 options. Always include "do nothing / status quo" if applicable."

Quality checklist (line 108): "At least 2 options considered (including status quo if applicable)"

**4. Confirmation Criteria Must Be Measurable/Observable**

Lines 90–94 specify four concrete forms:
> - A review date
> - A metric to watch
> - An automated test or CI check
> - Conditions that would trigger revisiting

Quality checklist (line 112): "Confirmation criteria are measurable or observable"

Anti-pattern "Orphaned ADR" (line 126–127) reinforces this by flagging ADRs with no confirmation criteria.

**5. File Naming Convention**

Line 132:
> File naming: `NNNN-kebab-case-title.md` (e.g., `0005-use-postgresql-bytea-for-content.md`)

Directory guidance (line 130): check for existing location (`docs/adr/`, `docs/architecture-decisions/`, or `docs/decisions/`); create `docs/adr/` if none exists.

**6. Four Anti-Patterns Named**

All four present (skill lists 7 total):
1. **Retroactive ADR** (line 120): "Written after the decision to justify it"
2. **No alternatives** (line 121): "Only the chosen option described"
3. **Strawman options** (line 122): "Alternatives are obviously bad"
4. **Orphaned ADR** (line 126–127): "No confirmation criteria"

---

### ✗ Critical Gap

**Missing Template File**

Line 42 references a required template:
> "The template is at `${CLAUDE_PLUGIN_ROOT}/templates/adr-template.md` — read it for the full structure."

**Status:** Template file does not exist in the repository. The skill is incomplete — it delegates "the full structure" to an external template that isn't present. When a user invokes the skill, it will fail at Step 3 when asked to read the template.

**Fix:** Either (a) embed the template in the SKILL.md directly as a code block, or (b) create `/Users/martin/Projects/turtlestack/plugins/engineering/architect/skills/write-adr/templates/adr-template.md` with a complete MADR example.

---

### Identified Gaps (Non-Critical)

1. **Superseded ADR Linkage** — Quality checklist (line 114) mentions "Related ADRs are linked (supersedes, builds on, relates to)" but doesn't specify the frontmatter syntax or body format for these relationships.

2. **Template for Revision Notes** — No guidance on how to document when an ADR is updated or superseded. Should an old ADR be left with a "Superseded by ADR-NNNN" note, or deleted? How is the history tracked?

3. **Author/Reviewer Fields** — Frontmatter includes decision-makers, consulted, informed (lines 51–53), but no explicit author or reviewer field. This can make it unclear who actually wrote the ADR or who should approve it.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.5/16.5 (88%) |
| Evaluated | 2026-05-03 |
| Target duration | 35602 ms |
| Target cost | $0.0763 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill uses the MADR format and requires all key sections: frontmatter (status, date, decision-makers), context, decision drivers, considered options, decision outcome, consequences, confirmation, and pros/cons per option | PASS | Section 1 of the output explicitly enumerates all eight sections with line numbers: Frontmatter (lines 47–55), Context and Problem Statement, Decision Drivers, Considered Options, Decision Outcome, Consequences (lines 83–87), Confirmation (lines 89–94), Pros and Cons of Options (lines 96–100). |
| c2 | Skill requires the ADR title to describe both the problem and the solution — not just the technology chosen | PASS | Section 2 quotes lines 57–62 directly: 'ADR-NNNN: {Short title — describes the problem AND solution}' with Good/Bad examples, and notes the quality checklist at line 106 reinforces 'Title describes both the problem and the solution'. |
| c3 | Skill mandates at least two options including "do nothing / status quo" where applicable | PASS | Section 3 quotes lines 75–76: 'At least 2 options. Always include "do nothing / status quo" if applicable.' Quality checklist at line 108 is also cited: 'At least 2 options considered (including status quo if applicable)'. |
| c4 | Skill requires consequences to include at least one negative — with an explicit honesty check that every decision has downsides | FAIL | The output lists 'Consequences — lines 83–87' as a present section but provides no quote from those lines and makes no mention of a requirement for at least one negative consequence or an explicit honesty check. The negative-consequences rule is entirely absent from the verification output. |
| c5 | Skill requires measurable or observable confirmation criteria — a review date, metric, automated test, or reconsideration trigger | PASS | Section 4 quotes lines 90–94 listing four concrete forms: 'A review date', 'A metric to watch', 'An automated test or CI check', and 'Conditions that would trigger revisiting'. Quality checklist line 112 is also cited. |
| c6 | Skill provides a quality checklist before declaring the ADR complete | PASS | The output references a quality checklist at four separate points (lines 106, 108, 112, 114) with specific checklist items quoted, confirming the skill contains one. |
| c7 | Skill lists anti-patterns including retroactive ADR, no alternatives, strawman options, and orphaned ADR with no confirmation criteria | PASS | Section 6 explicitly names all four: Retroactive ADR (line 120), No alternatives (line 121), Strawman options (line 122), Orphaned ADR (lines 126–127), noting the skill lists 7 anti-patterns total. |
| c8 | Skill specifies file naming convention (NNNN-kebab-case-title.md) and target directory (docs/adr/ or similar) | PASS | Section 5 quotes line 132: 'File naming: NNNN-kebab-case-title.md (e.g., 0005-use-postgresql-bytea-for-content.md)' and line 130 confirms directory guidance: check for docs/adr/, docs/architecture-decisions/, or docs/decisions/; create docs/adr/ if none exists. |
| c9 | Output is structured as a verification of the skill (verdict per requirement) rather than producing a sample ADR | PASS | The entire output is a verification report with a summary ('5 of 6 verified items'), numbered verified items with line citations, a critical gap section, and a non-critical gaps section. No sample ADR is produced. |
| c10 | Output confirms the MADR sections are all named explicitly: status/date/decision-makers frontmatter, context, decision drivers, considered options, decision outcome, consequences, confirmation, and per-option pros/cons | PASS | Section 1 enumerates all eight sections with line-number citations and confirms frontmatter includes 'status, date, decision-makers, consulted, informed'. |
| c11 | Output verifies the title rule — title must describe both problem and solution, not just the chosen technology | PASS | Section 2 directly quotes the skill's title rule with examples of both good and bad titles, confirming the problem-plus-solution requirement. |
| c12 | Output confirms the at-least-two-options rule, including "do nothing / status quo" where applicable, and that strawman alternatives are flagged as an anti-pattern | PASS | Section 3 confirms the two-options and status-quo requirement with direct quotes. Section 6 separately names 'Strawman options' as one of the four anti-patterns at line 122. |
| c13 | Output verifies the negative-consequences honesty rule — every decision must list at least one negative | FAIL | The output never mentions requiring at least one negative consequence or any honesty check for downsides. Consequences are noted as a section (lines 83–87) but no verification of the negative-consequences rule appears anywhere in the output. |
| c14 | Output confirms confirmation criteria must be measurable/observable (review date, metric, automated test, or reconsideration trigger) — not aspirational text | PASS | Section 4 quotes the four concrete forms from lines 90–94 and notes the quality checklist at line 112 requires 'Confirmation criteria are measurable or observable'. The Orphaned ADR anti-pattern at lines 126–127 reinforces the requirement. |
| c15 | Output verifies the file naming convention (NNNN-kebab-case-title.md) and target directory (docs/adr/) are stated, with the four-digit prefix and kebab-case explicit | PASS | Section 5 quotes 'NNNN-kebab-case-title.md' with a concrete example ('0005-use-postgresql-bytea-for-content.md') making the four-digit prefix and kebab-case explicit, and references docs/adr/ as the target directory. |
| c16 | Output verifies the anti-patterns list includes retroactive ADR, no alternatives, strawman options, and orphaned ADRs without confirmation criteria | PASS | Section 6 explicitly lists all four anti-patterns with line numbers: Retroactive ADR (line 120), No alternatives (line 121), Strawman options (line 122), Orphaned ADR (lines 126–127). |
| c17 | Output identifies any gaps — e.g. no guidance on superseded ADR linkage, no template for revision notes when an ADR is updated, or no explicit author/reviewer field | PARTIAL | The 'Identified Gaps (Non-Critical)' section names all three gaps verbatim: (1) Superseded ADR Linkage — notes the quality checklist mentions linking but lacks frontmatter syntax, (2) Template for Revision Notes — no guidance on superseding/updating ADRs, (3) Author/Reviewer Fields — frontmatter has decision-makers but no explicit author or reviewer. |

### Notes

The output is a thorough, well-structured verification that correctly confirms seven of the eight criteria it could confirm (c1–c3, c5–c8 on the skill side; c9–c12, c14–c16 on the output side). The single consistent blind spot is the negative-consequences honesty rule: criterion c4 asks whether the skill requires at least one negative consequence with an explicit honesty check, and c13 asks whether the output verifies that rule. Neither is addressed anywhere in the captured output — the Consequences section is listed as present at lines 83–87 but never quoted, and no mention of a mandatory negative or honesty check appears. Everything else — MADR sections, title rule, two-options mandate, measurable confirmation criteria, quality checklist, anti-patterns, and file naming — is verified with direct line citations and quotes. The three identified gaps in the non-critical section are all correctly flagged and named, earning the PARTIAL ceiling for c17.
