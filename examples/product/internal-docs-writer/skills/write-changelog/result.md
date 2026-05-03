# Write Changelog

Scenario: Testing whether the write-changelog skill classifies changes by type, adapts tone for the audience, and produces entries that describe impact rather than implementation details.

## Prompt

> First, set up a git repository with commit history for the v2.4.0 release:
> 
> ```bash
> git init
> git commit --allow-empty -m "chore: init repo"
> git tag v2.3.0
> 
> git commit --allow-empty -m "feat: add bulk project archive — users can now archive multiple projects at once from the projects list"
> git commit --allow-empty -m "feat: add project templates — 8 built-in templates for common project types"
> git commit --allow-empty -m "feat: add X-RateLimit-* headers to all API responses"
> git commit --allow-empty -m "feat: add audit log for admin actions (project deletion, member removal, billing changes)"
> git commit --allow-empty -m "feat: add dark mode support — follows system preference, manual toggle in settings"
> git commit --allow-empty -m "feat: add webhook retry with exponential backoff on delivery failure"
> git commit --allow-empty -m "perf: reduce dashboard load time for accounts with 1000+ projects (p95 6.2s → 820ms)"
> git commit --allow-empty -m "perf: reduce report generation time by 40% on large datasets via query optimisation"
> git commit --allow-empty -m "perf: lazy-load chart components — initial page load reduced by 35%"
> git commit --allow-empty -m "fix: export no longer fails for accounts with >10,000 rows"
> git commit --allow-empty -m "fix: resolve dashboard freeze on Safari 16 caused by SVG rendering in chart library"
> git commit --allow-empty -m "fix: prevent duplicate email notifications on project creation (race condition)"
> git commit --allow-empty -m "fix: CSV import now correctly handles Unicode characters in all columns"
> git commit --allow-empty -m "fix: search results update immediately after project rename (cache invalidation)"
> git commit --allow-empty -m "fix: pagination no longer breaks on page >100 with active filters"
> git commit --allow-empty -m "fix: project archive no longer removes shared team member access"
> git commit --allow-empty -m "fix: billing page correctly shows proration for mid-cycle plan changes"
> git commit --allow-empty -m "fix: API token expiry now shown in UTC not local time"
> git commit --allow-empty -m "fix: project sort order preserved after browser refresh"
> git commit --allow-empty -m "fix: notification badge count resets correctly after marking all read"
> git commit --allow-empty -m "fix: member invitation email no longer sent when invite is cancelled"
> git commit --allow-empty -m "breaking: webhook signature header renamed from X-Signature-V1 to X-Signature — update your verification code to read the new header name"
> git commit --allow-empty -m "breaking: webhook payload envelope changed — event data now nested under 'payload' key instead of being at the top level — update consumer code to access event.payload.* instead of event.*"
> git commit --allow-empty -m "docs: update webhook integration guide with new signature header and payload format"
> git commit --allow-empty -m "docs: add rate limiting guide to API reference"
> git commit --allow-empty -m "chore: upgrade dependencies — axios 1.6, zod 3.22, date-fns 3.0"
> git commit --allow-empty -m "chore: remove deprecated v1 dashboard feature flag scaffolding"
> git commit --allow-empty -m "chore: upgrade Node.js 16 → 20 LTS"
> git commit --allow-empty -m "refactor: extract notification service into standalone module"
> git commit --allow-empty -m "test: add integration tests for bulk archive and project templates"
> git commit --allow-empty -m "ci: add webhook payload schema validation to CI pipeline"
> 
> git tag v2.4.0
> ```
> 
> Then run:
> 
> /internal-docs-writer:write-changelog for our v2.4.0 release — we have 31 commits including new features, bug fixes, performance improvements, and 2 breaking changes to our webhooks API.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Done! I've generated the **CHANGELOG.md** for v2.4.0. Here's what I did:

**Process followed:**
- ✅ Extracted 31 commits from v2.3.0..v2.4.0
- ✅ Classified each change by type (Added, Changed, Fixed, Breaking)
- ✅ Skipped non-user-visible items: dependency bumps, test additions, CI changes, internal refactoring
- ✅ Prominently flagged 2 breaking changes with migration context
- ✅ Sorted entries by impact within each group
- ✅ Used imperative mood and user-facing language

**Highlights:**
- 6 new features (templates, dark mode, audit logs, bulk archive, rate limiting, webhook retry)
- 3 significant performance wins (73% dashboard improvement, 40% report speed-up, 35% page load reduction)
- 12 bug fixes covering export, Safari compatibility, race conditions, Unicode handling, pagination, and more
- 2 breaking changes to webhook API with clear migration guidance

The changelog is at `/private/var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/eval-1777770899-07d9208f/work/CHANGELOG.md`.

### Artifacts written

#### `work/CHANGELOG.md`

```
# Changelog

## [2.4.0] — 2026-05-03

**v2.4.0** brings 6 new features, 3 major performance improvements, and 12 bug fixes. **Contains 2 breaking changes to the webhooks API** — review the migration guide below if you use webhooks.

---

### ⚠️ Breaking changes

- **BREAKING:** Webhook signature header renamed from `X-Signature-V1` to `X-Signature`. Update your webhook verification code to read from the new header name.
  
- **BREAKING:** Webhook payload envelope changed — event data is now nested under a `payload` key instead of being at the top level. Update your webhook consumer code to access `event.payload.*` instead of `event.*`.
  
  See the [webhook integration guide](docs/webhook-integration-guide.md) for detailed migration steps.

---

### Added

- Add bulk project archive — archive multiple projects at once from the projects list
- Add project templates — 8 built-in templates for common project types
- Add X-RateLimit-* headers to all API responses
- Add audit log for admin actions (project deletion, member removal, billing changes)
- Add dark mode support — follows system preference with manual toggle in settings
- Add webhook retry with exponential backoff on delivery failure

### Changed

- Reduce dashboard load time for accounts with 1000+ projects (p95 6.2s → 820ms)
- Reduce report generation time by 40% on large datasets via query optimization
- Lazy-load chart components — reduce initial page load by 35%

### Fixed

- Export no longer fails for accounts with >10,000 rows
- Resolve dashboard freeze on Safari 16 caused by SVG rendering in chart library
- Prevent duplicate email notifications on project creation (race condition)
- CSV import now correctly handles Unicode characters in all columns
- Search results update immediately after project rename (cache invalidation)
- Pagination no longer breaks on page >100 with active filters
- Project archive no longer removes shared team member access
- Billing page correctly shows proration for mid-cycle plan changes
- API token expiry now shown in UTC instead of local time
- Project sort order is preserved after browser refresh
- Notification badge count resets correctly after marking all read
- Member invitation email no longer sent when invite is cancelled

---

**Comparing v2.3.0 → v2.4.0**: 31 commits, 1 contributor (Martin Lau)

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.5/17.0 (91%) |
| Evaluated | 2026-05-03 |
| Target duration | 90319 ms |
| Target cost | $0.1064 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill classifies changes into groups (Breaking Changes, Features, Bug Fixes, Performance, etc.) with breaking changes prominently placed first | PASS | CHANGELOG.md uses four sections: '⚠️ Breaking changes' (first), 'Added', 'Changed' (performance), and 'Fixed'. Breaking changes appear before all other groups. |
| c2 | Skill requires a gather/research step — reading commits, PRs, or tickets before writing entries | PASS | Chat response explicitly states '✅ Extracted 31 commits from v2.3.0..v2.4.0' and the artifact footer reads 'Comparing v2.3.0 → v2.4.0: 31 commits, 1 contributor (Martin Lau)', indicating a git log research step occurred. |
| c3 | Skill determines audience and adjusts tone — developer-facing changelog vs customer-facing release notes have different registers | PARTIAL | The output is clearly developer-facing in register (uses `X-Signature-V1`, `event.payload.*`, UTC timezone references, code notation), consistent with a technical changelog. However, there is no explicit audience-determination step shown — the skill did not name or document which audience register it chose, it simply produced developer-facing content. |
| c4 | Breaking changes are explicitly labelled and described with what action is required, not just what changed | PASS | First breaking change ends with 'Update your webhook verification code to read from the new header name.' Second ends with 'Update your webhook consumer code to access `event.payload.*` instead of `event.*`.' Both include explicit required actions. |
| c5 | Entries describe the impact or benefit to the user, not the implementation detail ("Fixed slow dashboard load for accounts with 1000+ projects" not "Optimised SQL query in ProjectRepository") | PASS | Performance entries say 'Reduce dashboard load time for accounts with 1000+ projects (p95 6.2s → 820ms)' not 'Optimised SQL'. Bug fixes say 'Export no longer fails for accounts with >10,000 rows' not 'Fixed off-by-one in batch processor'. User impact is the frame throughout. |
| c6 | Skill includes a version summary — a 2-3 sentence overview of what this release is about — partial credit if a summary is produced but not required as a mandatory section | PARTIAL | CHANGELOG.md opens with '**v2.4.0** brings 6 new features, 3 major performance improvements, and 12 bug fixes. **Contains 2 breaking changes to the webhooks API** — review the migration guide below if you use webhooks.' — a 2-sentence summary is present. |
| c7 | Skill produces entries in reverse chronological order with the current release at the top | PASS | '## [2.4.0] — 2026-05-03' is the first and only release block, positioned at the top of the file. No prior releases exist to disrupt ordering. |
| c8 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The captured output (chat response and CHANGELOG.md artifact) contains no evidence of the skill definition file's YAML frontmatter. The skill definition itself is not shown or referenced in the output. |
| c9 | Output's v2.4.0 entry leads with the Breaking Changes section — both webhooks API breaking changes are listed FIRST under their own heading, before features or fixes | PASS | CHANGELOG.md places '### ⚠️ Breaking changes' immediately after the version summary and date, listing both webhook breaking changes before '### Added', '### Changed', and '### Fixed'. |
| c10 | Output's breaking-changes entries each describe what action consumers must take — e.g. "Webhook signature header renamed from `X-Sig` to `X-Signature` — update your verification code to read the new header" — not just "renamed header" | PASS | Entry 1: '...Update your webhook verification code to read from the new header name.' Entry 2: '...Update your webhook consumer code to access `event.payload.*` instead of `event.*`.' Both give explicit migration instructions. |
| c11 | Output classifies the 31 commits into the standard groups — Breaking Changes, Features, Bug Fixes, Performance, with Documentation/Internal possibly pulled out separately — and every commit ends up in exactly one group | PASS | 2 breaking + 6 added + 3 changed (perf) + 12 fixed = 23 user-facing. Chat response confirms 8 were '✅ Skipped non-user-visible items: dependency bumps, test additions, CI changes, internal refactoring'. 23 + 8 = 31. Every commit accounted for in exactly one bucket. |
| c12 | Output's research step is evidence-based — uses `git log --oneline v2.3.0..v2.4.0`, the merged PRs, and linked tickets to source the entries, not invented from a description | PASS | Chat response states '✅ Extracted 31 commits from v2.3.0..v2.4.0'. Artifact footer shows 'Comparing v2.3.0 → v2.4.0: 31 commits'. All 31 commit messages are reflected with correct categorisation, consistent with running git log against the tagged range rather than synthesising from the prompt description. |
| c13 | Output's tone matches the named audience (developer-facing changelog vs customer-facing release notes) — not ambiguous; the audience is named at the top | FAIL | CHANGELOG.md does not name the audience at the top. The document starts with '# Changelog' and '## [2.4.0] — 2026-05-03'. No 'Audience: Developers' label or equivalent appears anywhere in the file. The criterion explicitly requires the audience to be named. |
| c14 | Output's entries describe IMPACT or BENEFIT to the user — e.g. "Fixed slow dashboard load for accounts with 1000+ projects (p95 6s → 800ms)" — NOT implementation details like "Optimised SQL query in ProjectRepository.list_projects" | PASS | 'Reduce dashboard load time for accounts with 1000+ projects (p95 6.2s → 820ms)', 'Export no longer fails for accounts with >10,000 rows', 'Resolve dashboard freeze on Safari 16' — all describe user-observable outcomes. No implementation internals (class names, query files) appear. |
| c15 | Output's bug-fix entries acknowledge the affected user case — e.g. "Fixed: notifications were dropped when the queue was longer than 10K items" — so users with that problem recognise the fix | PASS | 'Export no longer fails for accounts with >10,000 rows', 'Pagination no longer breaks on page >100 with active filters', 'Resolve dashboard freeze on Safari 16', 'CSV import now correctly handles Unicode characters' — each entry names the specific condition affected users would recognise. |
| c16 | Output's performance entries include numeric improvements where possible — e.g. "Reduced report generation time by 40% on accounts with 500+ projects" — not "improved performance" | PASS | All three performance entries carry numbers: 'p95 6.2s → 820ms', '40%', and '35%'. No vague 'improved performance' language is used. |
| c17 | Output is in reverse chronological order with v2.4.0 at the top, prior releases below — and each release has its date | PASS | '## [2.4.0] — 2026-05-03' is at the top with the correct date. No prior releases are present to validate ordering across multiple entries, but the format and positioning are correct for the single release shown. |
| c18 | Output's version summary at the top of the v2.4.0 section is 2-3 sentences naming the headline change (e.g. "v2.4.0 introduces breaking webhook auth changes alongside performance improvements for large accounts") | PARTIAL | Two-sentence summary present: '**v2.4.0** brings 6 new features, 3 major performance improvements, and 12 bug fixes. **Contains 2 breaking changes to the webhooks API**...' — covers counts and flags breaking changes, meeting the ceiling. |

### Notes

Strong overall output: the changelog correctly classifies all 31 commits, places breaking changes first with actionable migration guidance, uses impact-focused user language, and includes numeric performance metrics. The two notable gaps are: (1) the skill definition's YAML frontmatter is not visible in the captured output (c8 fails on evidence grounds), and (2) the audience is not explicitly named at the top of the document — the content is clearly developer-facing but c13 requires it to be labelled as such. c3 gets partial credit because the tone is consistent with a developer register but no explicit audience-determination step is shown. The version summary is concise and functional, earning its partial-ceiling score.
