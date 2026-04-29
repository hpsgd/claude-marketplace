# Output: Write changelog

**Verdict:** PARTIAL
**Score:** 14.5/17 criteria met (85%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill classifies changes into groups (Breaking Changes, Features, Bug Fixes, Performance, etc.) with breaking changes prominently placed first — Step 2 defines six named groups; Step 5 mandates a prominent `### ⚠ Breaking changes` section above all other groups when breaking changes exist.

- [x] PASS: Skill requires a gather/research step — Step 1 mandates four explicit `git` commands (`git log`, `git diff --stat`, `git tag`, `git log --merges`) before any writing begins.

- [x] PASS: Skill determines audience and adjusts tone — Step 3 explicitly separates "User-facing changelog (default)" from "Developer-facing changelog" with concrete bad/good examples for each register.

- [x] PASS: Breaking changes are explicitly labelled and described with what action is required — Step 4 rule 6 requires `**BREAKING:**` prefix plus "explain what to do"; Step 7 checklist includes "Breaking changes are clearly marked."

- [x] PASS: Entries describe impact or benefit to the user, not implementation detail — Step 3 and Step 4 rule 5 ("Lead with the user impact") both enforce this with bad/good contrasts.

- [~] PARTIAL: Skill includes a version summary — Step 6 mandates a summary block with feature/fix/improvement counts and one headline sentence, but the format prescribes only one sentence rather than a richer 2-3 sentence overview — partially met: 0.5

- [x] PASS: Skill produces entries in reverse chronological order with the current release at the top — Step 5 uses `## [version] — YYYY-MM-DD` format; the structure implies current release first.

- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — all three fields present and non-empty.

### Output expectations

- [x] PASS: Output's v2.4.0 entry leads with the Breaking Changes section — Step 5 explicitly places `### ⚠ Breaking changes` at the top before all other groups.

- [~] PARTIAL: Output's breaking-changes entries each describe what action consumers must take — Step 4 requires migration steps generally via `**BREAKING:**` but gives no webhook-specific illustration; the pattern is covered but not exemplified at API-header level — partially met: 0.5

- [x] PASS: Output classifies the 31 commits into standard groups with every commit in exactly one group — Step 2 classification table covers all types; Step 2 skip rules prevent double-counting; Step 4 "one change per line" rule enforces single membership.

- [x] PASS: Output's research step is evidence-based — Step 1 mandates `git log --format` with the user-supplied range, `git diff --stat`, and PR merge commits; instructs substituting the exact range from the user prompt.

- [x] PASS: Output's tone matches the named audience — Step 3 requires explicit audience choice; Step 7 checklist verifies "Audience is appropriate."

- [x] PASS: Output's entries describe IMPACT or BENEFIT — Step 3 and Step 4 both mandate this with explicit bad/good examples.

- [x] PASS: Output's bug-fix entries acknowledge the affected user case — Step 3 user-facing example ("Fixed a bug where search queries with special characters returned no results") directly models the pattern.

- [ ] FAIL: Output's performance entries include numeric improvements where possible — Step 4 illustrates "Speed up dashboard loading by 40%" as a good example, but no rule mandates numeric benchmarks for performance entries; the requirement is illustrated but not enforced — not found: no explicit rule requiring before/after metrics.

- [~] PARTIAL: Output's version summary at the top of the v2.4.0 section is 2-3 sentences naming the headline change — Step 6 produces a summary but prescribes only one sentence for the highlight, not 2-3 — partially met: 0.5

- [x] PASS: Output is in reverse chronological order with v2.4.0 at the top and each release has its date — Step 5 format uses `## [version] — YYYY-MM-DD`; standard CHANGELOG convention implied throughout.

## Notes

The skill is well-structured across seven clear steps. The main gap is that numeric performance benchmarks are illustrated by example but never mandated — the criterion requires them "where possible," but the skill doesn't instruct the agent to seek them out. The version summary covers the intent but caps at one sentence rather than the 2-3 expected. Breaking-change migration steps are required generally but not illustrated for API-level patterns (e.g. header renames), which is a substance gap rather than a structural failure. Reverse chronological ordering is implicit in the format rather than stated as an explicit instruction for appending to an existing changelog.
