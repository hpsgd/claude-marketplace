# Test: Write migration guide

Scenario: Testing whether the write-migration-guide skill requires before/after code examples for every breaking change, a rollback plan, and a deprecation timeline with actual dates.

## Prompt


/developer-docs-writer:write-migration-guide for our API v2 to v3 upgrade — we renamed several fields, changed authentication from API keys to OAuth 2.0, and removed two deprecated endpoints.

## Criteria


- [ ] PASS: Skill requires before/after code examples for every breaking change — prose description alone is not sufficient
- [ ] PASS: Skill requires a rollback plan — including limitations and the point of no return after which rollback is impossible
- [ ] PASS: Skill requires a deprecation timeline with actual dates or relative timeframes — "eventually deprecated" is explicitly rejected
- [ ] PASS: Skill requires an impact assessment — who is affected, what code must change, estimated effort, and who is NOT affected
- [ ] PASS: Skill requires an exhaustive breaking changes table — each change gets its own row, not combined into "various improvements"
- [ ] PASS: Skill requires verification steps so developers can confirm the migration succeeded
- [ ] PARTIAL: Skill provides guidance on coexistence — whether old and new can run simultaneously during migration — partial credit if this is mentioned but no specific dual-write guidance is given
- [ ] PASS: Skill requires honest effort estimates — the rule that underestimating effort is a form of dishonesty is present
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields
