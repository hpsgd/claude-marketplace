# Test: Write battle card

Scenario: Testing whether the write-battle-card skill produces at least 4 objection/response pairs, includes landmine questions, and fits on a single page for sales use.

## Prompt


/gtm:write-battle-card for competing against Monday.com — our sales team keeps losing deals when Monday comes up late in the evaluation and we don't have a consistent response.

## Criteria


- [ ] PASS: Skill requires a competitor research step before writing — not synthesising from assumptions about Monday.com
- [ ] PASS: Skill requires win/loss analysis — understanding why deals were won or lost against this competitor specifically
- [ ] PASS: Skill produces at least 4 objection/response pairs — covering the most common objections sales encounters
- [ ] PASS: Skill includes landmine questions — questions reps can ask to surface issues where Clearpath wins and Monday loses
- [ ] PASS: Skill produces output that fits on a single page — the battle card must be scannable in under 60 seconds
- [ ] PASS: All messaging is labelled DRAFT and flagged for human review before sales use
- [ ] PARTIAL: Skill differentiates between objection responses for different buyer types or stages — partial credit if responses are provided but not segmented by buyer persona or deal stage
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields
