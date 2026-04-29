# Output: Write KB article (support)

**Verdict:** PASS
**Score:** 18/18 criteria met (100%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill requires the article title to be a question the user would search — Title section explicitly requires question format with good/bad examples using user vocabulary
- [x] PASS: Skill requires a short answer at the top that resolves the issue without requiring the user to read the full article — Short answer section mandates 1-2 self-contained sentences
- [x] PASS: Skill produces step-by-step instructions where applicable — Step-by-step section requires numbered format with action verb, exact UI element names, and expected result per step
- [x] PASS: Skill requires a troubleshooting section covering variations of the problem — Troubleshooting section is mandatory with Problem/Cause/Solution format including error messages, user mistakes, and environment differences
- [x] PASS: Skill is written to deflect repeat support tickets — quality rules checklist (scannable, testable), workaround section pointing to real paths, and maintenance rule tracking ticket volume vs article views
- [x] PASS: Skill requires the article to be tested against the original ticket language — Title section explicitly says "If you have access to source tickets, validate the title and short answer against the actual phrasing customers use" with specific instructions to pull two ticket subject lines
- [x] PASS: Skill requires related articles or next steps at the end — Related articles section requires 3-5 articles grouped by next steps, related topics, and background
- [x] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields — present in SKILL.md header

### Output expectations

- [x] PASS: Output's title is phrased as a user-search question — skill enforces this explicitly; given the prompt the output would yield something like "Why do my exports fail for large datasets?"
- [x] PASS: Output's first paragraph tells the user the fix in 1-3 sentences — skill mandates short answer with core fix, self-contained
- [x] PASS: Output's step-by-step instructions are numbered with concrete actions — skill enforces exact format: action verb, UI element names, expected result per step
- [x] PASS: Output's troubleshooting section covers variations — skill requires common error message, common user mistake, and environment-difference cases; covers "still fails after filtering" scenarios
- [x] PASS: Output is written to deflect support contact — workaround section, quality rules, and maintenance tracking together ensure the article addresses the problem fully and calls out upgrade paths
- [x] PASS: Output uses ticket language for the title and summary — skill explicitly requires validating against ticket phrasing before finalising
- [x] PASS: Output addresses the WHY briefly after the WHAT — skill mandates: "Immediately after the short answer, add one sentence explaining WHY the constraint exists"
- [x] PASS: Output's related articles cover adjacent topics — skill requires 3-5 articles grouped by next steps, related topics, background; "[To be created]" placeholders allowed
- [x] PASS: Output addresses the at-scale customer — "When the answer is a workaround" section explicitly covers power users who hit the same wall repeatedly, pointing to API access or Enterprise plan
- [x] PASS: Output uses screenshots or visual references where applicable — skill requires screenshot placeholders ("![Screenshot: ...](TODO)") and states "Don't ship the article without flagging where visuals are needed"

## Notes

The SKILL.md is unusually thorough. Every output expectation in the test maps directly to an explicit requirement in the skill — not just implied behaviour. The workaround section ("When the answer is a workaround") is particularly strong: it addresses the at-scale customer case that many KB skills miss entirely. The PARTIAL criterion on ticket-language matching is fully met because the skill goes beyond "plain language" to require explicit validation against source ticket phrasing with a specific two-ticket-subject-line check. Maintenance rules including helpfulness tracking (views vs continued ticket volume) tie the article back to its deflection goal.
