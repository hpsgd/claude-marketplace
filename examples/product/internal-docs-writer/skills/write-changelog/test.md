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

## Output expectations

- [ ] PASS: Output's v2.4.0 entry leads with the Breaking Changes section — both webhooks API breaking changes are listed FIRST under their own heading, before features or fixes
- [ ] PASS: Output's breaking-changes entries each describe what action consumers must take — e.g. "Webhook signature header renamed from `X-Sig` to `X-Signature` — update your verification code to read the new header" — not just "renamed header"
- [ ] PASS: Output classifies the 31 commits into the standard groups — Breaking Changes, Features, Bug Fixes, Performance, with Documentation/Internal possibly pulled out separately — and every commit ends up in exactly one group
- [ ] PASS: Output's research step is evidence-based — uses `git log --oneline v2.3.0..v2.4.0`, the merged PRs, and linked tickets to source the entries, not invented from a description
- [ ] PASS: Output's tone matches the named audience (developer-facing changelog vs customer-facing release notes) — not ambiguous; the audience is named at the top
- [ ] PASS: Output's entries describe IMPACT or BENEFIT to the user — e.g. "Fixed slow dashboard load for accounts with 1000+ projects (p95 6s → 800ms)" — NOT implementation details like "Optimised SQL query in ProjectRepository.list_projects"
- [ ] PASS: Output's bug-fix entries acknowledge the affected user case — e.g. "Fixed: notifications were dropped when the queue was longer than 10K items" — so users with that problem recognise the fix
- [ ] PASS: Output's performance entries include numeric improvements where possible — e.g. "Reduced report generation time by 40% on accounts with 500+ projects" — not "improved performance"
- [ ] PASS: Output is in reverse chronological order with v2.4.0 at the top, prior releases below — and each release has its date
- [ ] PARTIAL: Output's version summary at the top of the v2.4.0 section is 2-3 sentences naming the headline change (e.g. "v2.4.0 introduces breaking webhook auth changes alongside performance improvements for large accounts")
