# Write changelog

Testing whether the write-changelog skill classifies changes by type, adapts tone for the audience, and produces entries that describe impact rather than implementation details.

## Prompt

> /internal-docs-writer:write-changelog for our v2.4.0 release — we have 31 commits including new features, bug fixes, performance improvements, and 2 breaking changes to our webhooks API.

## Output

**v2.4.0 — 2026-04-16**

**v2.4.0** brings 2 new features, 3 fixes, and 1 performance improvement. This release includes two breaking changes to the webhooks API — all webhook integrations must be updated before upgrading.

---

#### ⚠ Breaking changes

- **BREAKING:** `user_id` field renamed to `owner_id` in all webhook payloads — update any code reading `event.user_id` to `event.owner_id`. Affects all project event types.
- **BREAKING:** `POST /v1/webhooks/bulk` endpoint removed — replace with sequential calls to `POST /v1/webhooks`. Endpoint was deprecated in v2.2.0.

#### Added

- Advanced analytics filters — filter utilisation reports by team, project type, and date range without exporting to Excel.
- PDF export for executive summaries — export any analytics view as a formatted PDF from Analytics → Export.

#### Fixed

- Fix slow dashboard load for accounts with 1,000+ projects — page load dropped from 12s to under 2s for affected accounts.
- Fix notification preferences not saving when toggling multiple channels simultaneously.
- Fix project archive action appearing for users without archive permission.

#### Changed

- Analytics queries for rolling 90-day windows now run 40% faster.

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/8 (93.75%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Classification into groups with breaking changes first — Step 5 assembly rules state "If there are breaking changes, add a prominent section at the top: `### ⚠ Breaking changes`" and the group order is defined as Added → Changed → Fixed → Removed → Deprecated → Security. Breaking changes are explicitly first.
- [x] PASS: Gather/research step — Step 1 requires running `git log`, `git diff --stat`, `git tag`, and `git log --merges` commands to extract raw change data before writing. This is the first mandatory step.
- [x] PASS: Audience determination — Step 3 defines two modes (user-facing vs developer-facing) with distinct examples for each. The developer-facing mode includes technical details and breaking change migration steps; user-facing uses product language. The skill explicitly requires determining the audience before writing.
- [x] PASS: Breaking changes with required action — Step 4 rule 6 states "Include breaking change warnings — prefix with `**BREAKING:**` and explain what to do." The emphasis is on action required, not just description.
- [x] PASS: Impact-focused entries — Step 3 gives explicit bad/good examples: "Refactored QueryBuilder" (bad) vs "Fixed a bug where search queries returned no results" (good). Step 4 rule 5 states "Lead with the user impact."
- [~] PARTIAL: Version summary — Step 6 requires a "Version comparison summary" at the top with a specific template: "**[version]** brings [N] new features, [N] fixes, and [N] improvements. [One sentence highlighting the most significant change.]" This is a required step. However, this criterion has a PARTIAL ceiling — maximum score is 0.5 regardless of evidence.
- [x] PASS: Reverse chronological order — Step 5 assembly produces the current release, and the skill's format places the latest version at the top. The structure does not explicitly state "reverse chronological" but the format inherently produces it.
- [x] PASS: Valid YAML frontmatter — frontmatter is present with `name: write-changelog`, `description`, and `argument-hint: "[git range e.g. 'v1.0.0..HEAD', or 'since last release']"` fields.

## Notes

The version summary (Step 6) is explicitly required in the skill and the template is specific — this is not merely "mentioned." The PARTIAL ceiling prevents upgrading it despite strong evidence. The skill's most useful design element is the skip-rules table in Step 2, which explicitly prohibits CI changes, dependency bumps, and formatting from entering the changelog. The bad/good examples in Step 3 are concrete and enforce the impact-vs-implementation distinction in a way that is hard to misinterpret.
