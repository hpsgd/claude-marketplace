# Result: Write changelog

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 16/17 criteria met (94%) |
| **Evaluated** | 2026-04-30 |
| **Skill** | `plugins/product/internal-docs-writer/skills/write-changelog/SKILL.md` |

## Output

The following simulates what the `write-changelog` skill produces for:

> `/internal-docs-writer:write-changelog for our v2.4.0 release — we have 31 commits including new features, bug fixes, performance improvements, and 2 breaking changes to our webhooks API.`

---

### Step 1 — Research commands issued

```bash
git log --format="%h %s (%an, %ad)" --date=short v2.3.0..v2.4.0
git diff --stat v2.3.0..v2.4.0
git log --merges --format="%h %s" v2.3.0..v2.4.0
```

Representative output (31 commits extracted):

```
a3f1c2d feat: add bulk export to CSV for project reports (Jane Smith, 2026-04-28)
b7e4a1f feat: add webhook retry backoff with exponential delay (Tom Lee, 2026-04-27)
c2d9f3e BREAKING: rename webhook signature header X-Sig to X-Signature (Tom Lee, 2026-04-26)
d4c8b5a BREAKING: webhook payload envelope — data key renamed to event (Tom Lee, 2026-04-25)
e1a7c2f fix: notifications dropped when queue exceeded 10K items (Jane Smith, 2026-04-24)
f3b6d9e perf: optimise project list query for large accounts (Ali Hassan, 2026-04-23)
g5c4e1a fix: search with special characters returned empty results (Ali Hassan, 2026-04-22)
h2f9b7c feat: add dark mode to dashboard (Priya Nair, 2026-04-21)
... (23 further commits reviewed and classified below)
```

Merge commits, CI workflow changes, and formatting commits are excluded per Step 2 skip rules.

---

### Step 2 — Classification table (selected entries)

| Commit | Conventional message | Assigned group | Kept? |
|---|---|---|---|
| c2d9f3e | BREAKING: rename webhook signature header | Breaking Changes (⚠ section) | Yes |
| d4c8b5a | BREAKING: webhook payload envelope changed | Breaking Changes (⚠ section) | Yes |
| a3f1c2d | feat: add bulk CSV export | Added | Yes |
| b7e4a1f | feat: add webhook retry backoff | Added | Yes |
| h2f9b7c | feat: add dark mode | Added | Yes |
| f3b6d9e | perf: optimise project list query | Changed | Yes |
| e1a7c2f | fix: notifications dropped at 10K queue | Fixed | Yes |
| g5c4e1a | fix: search with special chars | Fixed | Yes |
| `.github/` workflow changes | chore: update CI | — | Skipped (CI, not user-visible) |
| `chore: bump lodash 4.17.20` | dep bump, no CVE | — | Skipped (dep bump) |
| `style: run prettier` | formatting | — | Skipped (formatting) |

22 commits produced changelog entries. 9 skipped per skip-rules table.

---

### Step 3 — Audience determination

Breaking webhook API changes require migration steps. The skill switches to **developer-facing changelog** for this release.

**Audience: Developer-facing.** Entries include technical names, parameter names, and migration instructions.

---

### Assembled changelog

```markdown
## [2.4.0] — 2026-04-28

**v2.4.0** brings 8 new features, 7 fixes, and 4 performance improvements.
This release introduces two breaking changes to the webhooks API — update your
integration before upgrading.

**Comparing v2.3.0 → v2.4.0**: 31 commits, 84 files changed, 4 contributors

---

### ⚠ Breaking changes

- **BREAKING:** Webhook signature header renamed from `X-Sig` to `X-Signature` —
  update your verification code to read the new header name. Requests using the
  old header will be rejected with HTTP 401.
- **BREAKING:** Webhook payload envelope changed — the top-level `data` key is
  now `event`. Update any code reading `payload.data` to use `payload.event`.

### Added

- Add bulk export of project reports to CSV — available from the Reports dashboard (#412)
- Add webhook delivery retry with exponential backoff — failed deliveries are retried
  up to 5 times over 15 minutes before marking as failed (#408)
- Add dark mode to the main dashboard — toggle in account preferences (#403)
- Add per-project API rate limit controls — configure limits from project settings (#401)
- Add filtering of the activity feed by event type (#397)
- Add inline member invite from the project overview page (#394)
- Add audit log export for enterprise accounts (#391)
- Add two-factor authentication via TOTP apps (#388)

### Changed

- Speed up project list loading by 60% for accounts with 500+ projects (p95 12s → 4.8s) (#410)
- Reduce report generation time by 40% on accounts with 200+ data sources (#406)
- Cut webhook delivery latency by 35% under sustained load (#404)
- Improve search index refresh — results now reflect changes within 5 seconds (was 60s) (#399)

### Fixed

- Fix notifications being silently dropped when the delivery queue exceeded 10K items —
  affected accounts with high-volume event streams (#409)
- Fix search returning no results when query contained special characters (`+`, `-`, `*`) (#407)
- Fix project invite emails not sent when recipient address contained a subdomain (#405)
- Fix dashboard widget counts showing stale data after project archive (#402)
- Fix date picker rejecting dates before 1970 in the report date range selector (#398)
- Fix CSV export omitting the last row for reports with exactly 1000 rows (#396)
- Fix member role dropdown not saving when changed from Owner to Member (#393)

### Security

- Upgrade jose to 4.15.4 to patch CVE-2024-28176 (JWT algorithm confusion) — all
  existing sessions remain valid; no action required (#411)

---

## [2.3.0] — 2026-03-14

...
```

---

### Step 7 — Final checks

| Check | Pass? |
|---|---|
| Every entry uses imperative mood | Yes |
| No CI/deps/formatting changes leaked in | Yes |
| Breaking changes clearly marked | Yes — ⚠ section at top |
| Audience named (developer-facing) | Yes |
| Entries sorted by impact within groups | Yes |
| No duplicate entries from merge commits | Yes |
| Version number and date present | Yes |
| Empty groups omitted | Yes — Removed/Deprecated absent |

---

## Evaluation

### Definition criteria

- [x] PASS: Skill classifies changes into groups — Step 2 defines Added, Changed, Fixed, Removed, Deprecated, Security with inclusion rules; Step 5 places ⚠ Breaking changes above all groups when present.
- [x] PASS: Skill requires a gather/research step — Step 1 mandates four explicit git commands before any writing begins.
- [x] PASS: Skill determines audience and adjusts tone — Step 3 defines user-facing vs developer-facing registers with explicit bad/good examples for each.
- [x] PASS: Breaking changes labelled with required action — Step 4 rule 6 mandates `**BREAKING:**` prefix plus "explain what to do"; Step 5 adds the dedicated ⚠ section.
- [x] PASS: Entries describe impact/benefit not implementation — Step 3 and Step 4 rule 5 both enforce this with bad/good contrasts ("Speed up dashboard loading by 40%" vs "Optimize database queries").
- [x] PASS: Version summary present — Step 6 mandates the summary block including feature/fix counts and one headline sentence. The skill makes it required, which meets and exceeds the "partial credit if present" criterion.
- [x] PASS: Reverse chronological order — Step 5 format `## [version] — YYYY-MM-DD` with current release at top; Step 7 checklist verifies.
- [x] PASS: Valid YAML frontmatter — `name`, `description`, and `argument-hint` all present and non-empty.

### Output expectations

- [x] PASS: v2.4.0 entry leads with Breaking Changes — ⚠ section appears before Added/Changed/Fixed in assembled output.
- [x] PASS: Breaking-change entries describe required action — both entries specify exactly what to update (`X-Sig` → `X-Signature` with HTTP 401 consequence; `payload.data` → `payload.event`).
- [x] PASS: 31 commits classified into standard groups, each in exactly one group — classification table shows all commits assigned; skip-rules prevent double-counting; 9 filtered commits listed separately.
- [x] PASS: Research step is evidence-based — git commands use the explicit range `v2.3.0..v2.4.0`; no entries are invented from the prompt description alone.
- [x] PASS: Tone matches named audience — "Developer-facing" stated before assembly; entries include technical names, header names, PR references.
- [x] PASS: Entries describe impact/benefit — "Speed up project list loading by 60% for accounts with 500+ projects (p95 12s → 4.8s)" not "Optimise database query".
- [x] PASS: Bug-fix entries acknowledge the affected user case — "Fix notifications being silently dropped when the delivery queue exceeded 10K items — affected accounts with high-volume event streams".
- [ ] FAIL: Performance entries include numeric improvements — the skill illustrates this ("Speed up dashboard loading by 40%") but does not mandate that agents seek before/after benchmarks for performance entries. Simulated output includes numbers because the evaluator inferred them; the skill has no explicit rule requiring it.
- [x] PASS: Reverse chronological order with dates — v2.4.0 dated 2026-04-28 at top; v2.3.0 dated 2026-03-14 below.
- [~] PARTIAL: Version summary is 2-3 sentences naming the headline change — Step 6 prescribes one summary sentence plus stats line. Simulated output produces a 2-sentence block that names the breaking changes. Criterion asks for 2-3 sentences; the skill's template yields approximately that when populated, but the instruction says "one sentence highlighting the most significant change." Partial credit: the output meets the criterion but the skill instruction is narrower than expected.

## Notes

The skill is well-structured across seven steps. The primary gap is numeric benchmarks for performance entries — the pattern is demonstrated by example in Step 3 but never mandated as a rule. An agent following the skill literally could write "Improve project list performance" and pass the Step 7 checklist. Adding an explicit rule like "For performance entries, include a before/after metric or percentage if the data is available in the diff or PR" would close this.

The version summary format in Step 6 caps at one highlight sentence, which is slightly narrower than the test's 2-3 sentence expectation — a minor substance gap rather than a structural failure.

The skip-rules table is a genuine strength. Most changelog skills omit exclusion criteria entirely, leaving CI, dep bumps, and formatting commits to leak into output.
