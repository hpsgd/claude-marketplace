# Test: Write changelog

Scenario: Testing whether the write-changelog skill classifies changes by type, adapts tone for the audience, and produces entries that describe impact rather than implementation details.

## Prompt

First, set up a git repository with commit history for the v2.4.0 release:

```bash
git init
git commit --allow-empty -m "chore: init repo"
git tag v2.3.0

git commit --allow-empty -m "feat: add bulk project archive — users can now archive multiple projects at once from the projects list"
git commit --allow-empty -m "feat: add project templates — 8 built-in templates for common project types"
git commit --allow-empty -m "feat: add X-RateLimit-* headers to all API responses"
git commit --allow-empty -m "feat: add audit log for admin actions (project deletion, member removal, billing changes)"
git commit --allow-empty -m "feat: add dark mode support — follows system preference, manual toggle in settings"
git commit --allow-empty -m "feat: add webhook retry with exponential backoff on delivery failure"
git commit --allow-empty -m "perf: reduce dashboard load time for accounts with 1000+ projects (p95 6.2s → 820ms)"
git commit --allow-empty -m "perf: reduce report generation time by 40% on large datasets via query optimisation"
git commit --allow-empty -m "perf: lazy-load chart components — initial page load reduced by 35%"
git commit --allow-empty -m "fix: export no longer fails for accounts with >10,000 rows"
git commit --allow-empty -m "fix: resolve dashboard freeze on Safari 16 caused by SVG rendering in chart library"
git commit --allow-empty -m "fix: prevent duplicate email notifications on project creation (race condition)"
git commit --allow-empty -m "fix: CSV import now correctly handles Unicode characters in all columns"
git commit --allow-empty -m "fix: search results update immediately after project rename (cache invalidation)"
git commit --allow-empty -m "fix: pagination no longer breaks on page >100 with active filters"
git commit --allow-empty -m "fix: project archive no longer removes shared team member access"
git commit --allow-empty -m "fix: billing page correctly shows proration for mid-cycle plan changes"
git commit --allow-empty -m "fix: API token expiry now shown in UTC not local time"
git commit --allow-empty -m "fix: project sort order preserved after browser refresh"
git commit --allow-empty -m "fix: notification badge count resets correctly after marking all read"
git commit --allow-empty -m "fix: member invitation email no longer sent when invite is cancelled"
git commit --allow-empty -m "breaking: webhook signature header renamed from X-Signature-V1 to X-Signature — update your verification code to read the new header name"
git commit --allow-empty -m "breaking: webhook payload envelope changed — event data now nested under 'payload' key instead of being at the top level — update consumer code to access event.payload.* instead of event.*"
git commit --allow-empty -m "docs: update webhook integration guide with new signature header and payload format"
git commit --allow-empty -m "docs: add rate limiting guide to API reference"
git commit --allow-empty -m "chore: upgrade dependencies — axios 1.6, zod 3.22, date-fns 3.0"
git commit --allow-empty -m "chore: remove deprecated v1 dashboard feature flag scaffolding"
git commit --allow-empty -m "chore: upgrade Node.js 16 → 20 LTS"
git commit --allow-empty -m "refactor: extract notification service into standalone module"
git commit --allow-empty -m "test: add integration tests for bulk archive and project templates"
git commit --allow-empty -m "ci: add webhook payload schema validation to CI pipeline"

git tag v2.4.0
```

Then run:

/internal-docs-writer:write-changelog for our v2.4.0 release — we have 31 commits including new features, bug fixes, performance improvements, and 2 breaking changes to our webhooks API.

Output requirements:

- **Produce TWO changelogs**: a **developer-facing** version (technical detail, commit refs, code changes) AND a **customer-facing** version (plain language, benefit-led, no commit hashes). Label each section explicitly.
- **Version summary** at the top of each: 2-3 sentence overview of what this release delivers and why it matters.
- **Sections in Keep-a-Changelog format**: `### Breaking Changes` (FIRST, with migration path), `### Added` (new features), `### Changed` (improvements), `### Fixed` (bug fixes), `### Performance` (perf improvements), `### Security` (security fixes), `### Deprecated` (sunset notices).
- **Breaking changes**: each has a `**Before:**` / `**After:**` code block AND a numbered migration step list AND a deprecation timeline.
- **Show file content inline** in chat AND write to disk at `CHANGELOG.md` (developer) and `RELEASE_NOTES.md` (customer) — do NOT just summarise.

A few specifics for the response:

- Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
- Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
- For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
- When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
- Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

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
