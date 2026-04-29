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

## Output expectations

- [ ] PASS: Output's breaking-changes table lists each change as a separate row — every renamed field (with old name → new name), the auth shift (API keys → OAuth 2.0), and each removed endpoint by name — not combined into "various improvements"
- [ ] PASS: Output's auth migration section walks through OAuth 2.0 setup — Authorization Code flow vs Client Credentials, where to register the app, how to obtain access tokens, refresh-token handling — with code examples, not just "switch to OAuth"
- [ ] PASS: Output's before/after code examples show the actual code change per breaking change — e.g. for a renamed field: `old: response['user_email'] → new: response['email_address']`, with both sides shown
- [ ] PASS: Output's deprecation timeline has actual dates — e.g. "v2 sunset: 2027-01-31, v2 deprecation header sent from: 2026-07-01, v3 GA: 2026-04-15" — not "eventually" or "at some point"
- [ ] PASS: Output's impact assessment names who is affected — what kinds of integrations break (every integration using removed endpoints, every integration that hardcoded API keys), and what is NOT affected (e.g. read-only data shapes that didn't change)
- [ ] PASS: Output's rollback plan documents the point of no return — once v2 is decommissioned (per the timeline date), rollback to v2 becomes impossible; before that point, customers can revert their code if they kept v2 credentials
- [ ] PASS: Output's coexistence guidance covers running both v2 and v3 in parallel during migration — whether existing v2 API keys still work alongside new OAuth tokens, or whether they must be migrated atomically
- [ ] PASS: Output's verification steps let the developer confirm migration success — e.g. "after migration: GET /v3/users should return the new schema; v2 endpoint calls return 410 Gone after sunset date"
- [ ] PASS: Output's effort estimate is honest — names a typical effort range per integration size (small: 1-2 days, medium: 3-5 days, large: 1-2 weeks) — and acknowledges that mass field-rename + auth rebuild is non-trivial, not "should be quick"
- [ ] PARTIAL: Output addresses the deprecation header / Sunset header (RFC 8594) being sent on v2 responses during the transition window so client tooling can detect imminent sunset
