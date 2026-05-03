# Write Adr

Scenario: Checking that the write-adr skill produces ADRs that follow the MADR format with all required sections, honest trade-offs, and measurable confirmation criteria.

## Prompt

> Review the write-adr skill definition and verify it produces complete, honest ADR documents rather than decision justifications written after the fact.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Here's the full assessment:

## Verdict: Aspires to honesty but under-enforces it

The skill has the right instincts — the anti-pattern list names "Retroactive ADR", the quality checklist has an honesty check, and the template is genuinely well-structured. But there are gaps between intention and enforcement.

### Critical gap: SKILL.md and template are mismatched

The template has two sections specifically designed to catch retroactive justification that **never appear** in SKILL.md's "Key sections (none optional)" list or the Quality Checklist:

- **Assumptions table** (`proven_by_code` / `inferred` / `needs_confirmation`) — this is the single best honesty mechanism in the whole document
- **Change Impact table** (Direct / Indirect / Unaffected) — forces the author to think through consequences honestly

An agent running this skill will likely skip both because they're not enforced.

### Other gaps relevant to "honest vs retroactive"

| Gap | Why it matters |
|---|---|
| "Retroactive ADR" anti-pattern has no operational defence | Says "write during the process" but gives no way to verify that happened — no required trigger artifact (incident, meeting, issue link) |
| Decision drivers can be reverse-engineered | No requirement to link drivers to evidence (existing ADRs, stakeholder constraints, NFRs) |
| Confirmation can degrade to a calendar date | "A review date" (line 92) is the weakest possible form — should require a metric or observable condition |
| Status starts "proposed" but nothing gates "accepted" | No consulted/informed sign-off check before the decision is closed |

### What's working well

The anti-pattern table and "at least one negative consequence" honesty check are genuinely strong. The `evaluate-technology` cross-reference is the right call — evaluate first, then record.

---

**Recommendation:** The Assumptions table in the template is the most valuable honesty mechanism and should be promoted to a required section in SKILL.md. Do you want me to propose specific edits to the skill, or is this review the deliverable?

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 7.0/16.5 (42%) |
| Evaluated | 2026-04-30 |
| Target duration | 75147 ms |
| Target cost | $0.3719 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill uses the MADR format and requires all key sections: frontmatter (status, date, decision-makers), context, decision drivers, considered options, decision outcome, consequences, confirmation, and pros/cons per option | PARTIAL | Output references 'Key sections (none optional)' list in SKILL.md and calls the template 'genuinely well-structured', but never enumerates all required sections by name. Mentions assumptions table and change impact table as gaps but does not confirm the full MADR section list (frontmatter fields, decision drivers, considered options, etc.). |
| c2 | Skill requires the ADR title to describe both the problem and the solution — not just the technology chosen | FAIL | The title rule is not mentioned anywhere in the captured output. |
| c3 | Skill mandates at least two options including 'do nothing / status quo' where applicable | FAIL | The at-least-two-options rule and 'do nothing/status quo' requirement are not mentioned in the captured output. |
| c4 | Skill requires consequences to include at least one negative — with an explicit honesty check that every decision has downsides | PASS | Output explicitly states: 'The anti-pattern table and "at least one negative consequence" honesty check are genuinely strong.' This directly confirms the rule and the honesty check exist. |
| c5 | Skill requires measurable or observable confirmation criteria — a review date, metric, automated test, or reconsideration trigger | PARTIAL | Output references 'A review date (line 92)' showing confirmation criteria exist, but frames it as a gap: 'is the weakest possible form — should require a metric or observable condition.' Confirms existence but flags that measurability is under-enforced. |
| c6 | Skill provides a quality checklist before declaring the ADR complete | PASS | Output states 'the Quality Checklist has an honesty check', confirming a quality checklist exists in the skill. |
| c7 | Skill lists anti-patterns including retroactive ADR, no alternatives, strawman options, and orphaned ADR with no confirmation criteria | PARTIAL | Output explicitly names 'Retroactive ADR' as present in the anti-pattern list. Strawman options are referenced indirectly. 'No alternatives' and 'orphaned ADR without confirmation criteria' are not confirmed as being in the anti-pattern list. |
| c8 | Skill specifies file naming convention (NNNN-kebab-case-title.md) and target directory (docs/adr/ or similar) | FAIL | No mention of file naming convention, four-digit prefix, kebab-case format, or target directory anywhere in the captured output. |
| c9 | Output is structured as a verification of the skill (verdict per requirement) rather than producing a sample ADR | PASS | Output opens with '## Verdict: Aspires to honesty but under-enforces it' and proceeds to assess the skill definition through structured analysis. It explicitly reviews the skill rather than producing a sample ADR. |
| c10 | Output confirms the MADR sections are all named explicitly: status/date/decision-makers frontmatter, context, decision drivers, considered options, decision outcome, consequences, confirmation, and per-option pros/cons | FAIL | Output does not enumerate or confirm all MADR sections by name. It references 'Key sections (none optional)' list generally and mentions assumptions/change-impact tables as gaps, but never lists status/date/decision-makers frontmatter, context, decision drivers, considered options, decision outcome, etc. |
| c11 | Output verifies the title rule — title must describe both problem and solution, not just the chosen technology | FAIL | The title rule is not mentioned or verified in the captured output. |
| c12 | Output confirms the at-least-two-options rule, including 'do nothing / status quo' where applicable, and that strawman alternatives are flagged as an anti-pattern | FAIL | The at-least-two-options rule and 'do nothing/status quo' are not confirmed. Strawman options appear in a gap table row but the output does not confirm they are explicitly flagged as an anti-pattern in the skill. |
| c13 | Output verifies the negative-consequences honesty rule — every decision must list at least one negative | PASS | Output explicitly states: 'The anti-pattern table and "at least one negative consequence" honesty check are genuinely strong.' This directly verifies the rule exists in the skill. |
| c14 | Output confirms confirmation criteria must be measurable/observable (review date, metric, automated test, or reconsideration trigger) — not aspirational text | PARTIAL | Output identifies this as a gap: '"A review date" (line 92) is the weakest possible form — should require a metric or observable condition.' This confirms the skill has confirmation criteria but flags that the skill allows non-measurable forms, meaning the requirement is not fully enforced. |
| c15 | Output verifies the file naming convention (NNNN-kebab-case-title.md) and target directory (docs/adr/) are stated, with the four-digit prefix and kebab-case explicit | FAIL | File naming convention and target directory are not mentioned anywhere in the captured output. |
| c16 | Output verifies the anti-patterns list includes retroactive ADR, no alternatives, strawman options, and orphaned ADRs without confirmation criteria | PARTIAL | Output explicitly names 'Retroactive ADR' as being in the anti-pattern list. 'No alternatives', 'strawman options', and 'orphaned ADRs without confirmation criteria' are not confirmed as being present in the skill's anti-pattern list. |
| c17 | Output identifies any gaps — e.g. no guidance on superseded ADR linkage, no template for revision notes when an ADR is updated, or no explicit author/reviewer field | PARTIAL | Output identifies several gaps: assumptions table not in enforced key sections list, change impact table not enforced, 'Retroactive ADR anti-pattern has no operational defence', confirmation can degrade to a calendar date, no sign-off check before status moves to accepted. These are substantive gaps beyond the examples listed in the criterion. |

### Notes

The captured output is a genuine critique of the write-adr skill's honesty enforcement, but it operates at too high a level of abstraction to satisfy most verification criteria. It confirms the quality checklist exists, the negative-consequences honesty check is present, and the anti-pattern table includes Retroactive ADR. However, it completely omits verification of: the title rule (problem+solution framing), the at-least-two-options rule including do-nothing, and the file naming/directory convention. It also fails to enumerate all MADR sections by name. The output is strongest where it identifies enforcement gaps (assumptions table, confirmation strength, sign-off gates) but weakest as a systematic checklist-style verification — it reads more as an expert critique than a structured pass/fail review against the skill's stated requirements.
