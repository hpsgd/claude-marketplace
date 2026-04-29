# Output: propose-improvement upstream a learned rule

**Verdict:** PASS
**Score:** 16.5/17 criteria met (97%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Step 1 locates the marketplace repo by reading settings files — the skill's Step 1 runs a Python script that reads `~/.claude/settings.json`, `.claude/settings.json`, and `.claude/settings.local.json` for `extraKnownMarketplaces`. No hardcoded path exists; the script builds the map dynamically.
- [x] PASS: Step 2 reads the pattern file and confirms count >= 3 — Step 3 explicitly reads from `.claude/learnings/patterns/{pattern-id}.json` and checks `count >= 3` and `status` not already submitted before proceeding.
- [x] PASS: Step 3 maps the learning to the correct target file — Step 4 defines a mapping table covering new rules, skill updates, agent updates, regex patterns, templates, and cross-cutting rules, each with a specific target path.
- [x] PASS: Step 4 creates a branch from a fresh main — Step 5 specifies the exact git sequence: `git fetch origin`, `git checkout main`, `git pull --ff-only`, then `git checkout -b`. Rules section reinforces this with "Always branch from a fresh `main`."
- [x] PASS: Step 5 diff review is never skipped — Step 6 is labelled "(mandatory — never skip)" in the section header. Rules section states "Never push without user approval. Step 6 (diff review) is mandatory." Y/n/edit paths are all defined.
- [x] PASS: Step 6 commit message includes session IDs and correction summaries — Step 7 defines a commit template with an Evidence section using `- {session1}: {summary}` per-session lines. Rules state "Evidence is mandatory. Every PR must include the session IDs and correction summaries."
- [x] PASS: Step 7 updates pattern file status to `pr_submitted` with PR URL — Step 8 defines updating the pattern JSON with `"status": "pr_submitted"` and `"pr_url"`, adding a note to the local rule, and logging a proposal record to `.claude/learnings/proposals/`.
- [~] PARTIAL: Skill returns to main after completing — Rules state "Return to main. Always `git checkout main` at the end, regardless of outcome" and the command appears at the end of the Step 7 bash block. However it is embedded mid-step, not isolated as a guaranteed post-workflow cleanup; an error partway through Step 7 after pushing would leave the repo on the feature branch.

### Output expectations

- [x] PASS: Output locates the marketplace repo path by reading project settings or config — Step 1 Python script reads the three settings files for `extraKnownMarketplaces`; no hardcoded path.
- [x] PASS: Output reads the pattern file and confirms trigger count at or above threshold — Step 3 reads the pattern file, checks `count >= 3`, and the Evidence block in Step 6's diff template would display the actual count from the file's metadata.
- [x] PASS: Output maps the learning to a specific target file and explains the mapping decision — Step 4's mapping table distinguishes rule vs skill vs agent vs script vs template, and instructs reading the current target file before applying changes.
- [x] PASS: Output creates the branch from a freshly-pulled main — Step 5 defines exactly `git fetch origin && git checkout main && git pull --ff-only && git checkout -b learning/{topic}`.
- [x] PASS: Output's diff is shown before any push and workflow stops for user confirmation — Step 6 presents the full diff with context, requires Y/n/edit, and the Rules section repeats "never push without user approval."
- [x] PASS: Output's commit message includes evidence with session IDs and correction summaries — Step 7's commit template has an Evidence section with per-session `- {session}: {summary}` lines and the Rules section makes evidence mandatory.
- [x] PASS: Output uses Conventional Commits for the commit message — the Step 7 commit template uses `feat: learned rule — {topic}` which follows Conventional Commits format.
- [x] PASS: Output updates the pattern file status to `pr_submitted` with PR URL — Step 8 defines this update explicitly, including `"pr_url"` and `"pr_submitted_at"` fields.
- [x] PASS: Output's PR description includes evidence, proposed rule wording, and request for review — the Step 7 `gh pr create` body template includes Evidence table with sessions, the change description, and the source pattern metadata.
- [~] PARTIAL: Output returns to main at the end — `git checkout main` is present at the end of Step 7's bash block and stated in Rules, but not guaranteed against mid-step failures.

## Notes

The skill is one of the most operationally complete in the set. The org-comparison check in Step 2 (same org = owned upstream, different org = third-party) cleanly handles the third-party case without needing config flags. The two mandatory gates (Step 2 confirmation, Step 6 diff review) give the user clear checkpoints before any remote action.

One gap in Step 4's mapping table: cross-cutting rules default to `plugins/practices/coding-standards/rules/`, but a rule like "verify before declaring complete" could equally belong in `plugins/practices/thinking/rules/`. No tiebreaker is given when a rule spans multiple plugin domains.

The skill's Step 3 reads a pattern file by ID, but the scenario presents the argument as a learned rule name (`learned--verify-before-declaring-complete`) rather than a pattern JSON file. The skill handles both cases (pattern ID and learned rule), so this resolves cleanly — the "From a learned rule" branch in Step 3 covers it.
