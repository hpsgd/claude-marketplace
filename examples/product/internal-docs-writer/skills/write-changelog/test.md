# Test: Write changelog

Scenario: Testing whether the write-changelog skill classifies changes by type, adapts tone for the audience, and produces entries that describe impact rather than implementation details.

## Prompt


/internal-docs-writer:write-changelog for our v2.4.0 release — we have 31 commits including new features, bug fixes, performance improvements, and 2 breaking changes to our webhooks API.

## Criteria


- [ ] PASS: Skill classifies changes into groups (Breaking Changes, Features, Bug Fixes, Performance, etc.) with breaking changes prominently placed first
- [ ] PASS: Skill requires a gather/research step — reading commits, PRs, or tickets before writing entries
- [ ] PASS: Skill determines audience and adjusts tone — developer-facing changelog vs customer-facing release notes have different registers
- [ ] PASS: Breaking changes are explicitly labelled and described with what action is required, not just what changed
- [ ] PASS: Entries describe the impact or benefit to the user, not the implementation detail ("Fixed slow dashboard load for accounts with 1000+ projects" not "Optimised SQL query in ProjectRepository")
- [ ] PARTIAL: Skill includes a version summary — a 2-3 sentence overview of what this release is about — partial credit if a summary is produced but not required as a mandatory section
- [ ] PASS: Skill produces entries in reverse chronological order with the current release at the top
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields
