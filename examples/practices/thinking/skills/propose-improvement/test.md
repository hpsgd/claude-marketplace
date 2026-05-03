# Test: propose-improvement upstream a learned rule

Scenario: A developer has a local learned rule that has proven effective across 5 sessions and wants to upstream it to the marketplace via a PR. The propose-improvement skill handles the full workflow.

## Prompt

First, set up the workspace with a git repo and marketplace structure (use bash heredocs — `.claude/` writes via the Write tool are restricted in this workspace):

```bash
git init
git checkout -b main
git commit --allow-empty -m "chore: init"
git remote add origin https://github.com/hpsgd/turtlestack.git
mkdir -p .claude/rules .claude-plugin plugins/practices/coding-standards/rules

cat > .claude-plugin/marketplace.json <<'EOF'
{
  "name": "turtlestack",
  "version": "1.0.0",
  "plugins": []
}
EOF

cat > .claude/settings.json <<'EOF'
{
  "enabledPlugins": {"thinking@turtlestack": true}
}
EOF

cat > .claude/rules/learned--verify-before-declaring-complete.md <<'EOF'
---
name: verify-before-declaring-complete
type: feedback
trigger_count: 5
status: pending_review
sessions:
  - a1b2c3d4: "Declared migration complete before checking row count — was wrong"
  - e5f6g7h8: "Said deploy succeeded without checking health endpoint"
  - i9j0k1l2: "Marked tests passing without running the full suite"
  - m3n4o5p6: "Confirmed file was correct without re-reading after edit"
  - q7r8s9t0: "Announced feature done before verifying in browser"
---

Always run verification steps before declaring work complete. The verification method depends on the task: read the file after editing, check the health endpoint after deploying, run the full test suite before marking tests green, verify row counts after migrations.

**Why:** In 5 sessions, claimed completion without verifying — every time the verification step would have caught an error.

**How to apply:** Before saying "done", ask: what tool would prove this is correct? Use it. Then say done.
EOF
```

Then run:

/propose-improvement The pattern `learned--verify-before-declaring-complete` has been triggered in 5 sessions now. I think it's ready to share upstream. It's about always running verification steps before saying something is done.

Note: this is a sandboxed test environment. `git fetch origin` and `git push` will fail because there is no real remote. When git network operations fail, note the error and continue using local git state. Proceed autonomously through all steps: auto-confirm the target marketplace (turtlestack), create the branch from local HEAD, apply the change to `plugins/practices/coding-standards/rules/`, show the full diff, prepare the commit with evidence, and update the pattern file status to `pr_submitted`. Do not stop to ask for confirmation — treat the investigation and diff review as auto-approved for this test run.

Additional execution requirements — to ensure all work is captured for review, write a full execution log to `handoff/propose-improvement-execution.md` as you go, with one section per skill step. Each section must contain the verbatim outputs (not summaries):

- **Step 1 — Marketplace discovery:** Read `.claude/settings.json` and `.claude-plugin/marketplace.json`. Quote both file contents verbatim in this section.
- **Step 2 — Pattern read:** Quote the rule file's frontmatter verbatim (showing the `trigger_count: 5` field and all 5 session IDs).
- **Step 3 — Mapping decision:** Explain WHY this maps to a rule (not skill/agent/script) — based on `type: feedback` and cross-cutting nature.
- **Step 4 — Branch creation:** Show the actual `git checkout -b learning/...` output.
- **Step 5 — Diff:** Run `git diff` (NOT `--stat`) and paste the FULL unified diff output (with `+++`, `---`, `@@` headers and `+`/`-` lines) into a fenced code block.
- **Step 6 — Commit:** Show the commit command with the full message body. The commit message body MUST include all 5 session IDs verbatim (a1b2c3d4, e5f6g7h8, i9j0k1l2, m3n4o5p6, q7r8s9t0) with their correction summaries — not a paraphrase. After committing, run `git log -1 --format=fuller` and paste the full output verbatim.
- **Step 7 — Push attempt + PR description:** Note that push fails in sandbox. Then write a complete PR description body — title, summary, evidence table with all 5 sessions, proposed rule wording, and an explicit "Please review" request.
- **Step 8 — Pattern file update:** Use the Edit tool to update `.claude/rules/learned--verify-before-declaring-complete.md` — change `status: pending_review` to `status: pr_submitted` and add a `pr_url:` field (use a placeholder if push failed). Show the file contents after the edit.
- **Step 9 — Return to main:** Run `git checkout main` and confirm the working state.

## Criteria

- [ ] PASS: Step 1 locates the marketplace repo by reading settings files — does not assume a hardcoded path
- [ ] PASS: Step 2 reads the pattern file and confirms it meets the minimum threshold (count >= 3) before proceeding
- [ ] PASS: Step 3 maps the learning to the correct target file in the marketplace (rule, skill, agent, or script depending on type)
- [ ] PASS: Step 4 creates a branch from main and applies the minimal required change (uses local git state if fetch fails)
- [ ] PASS: Step 5 (diff review) is never skipped — the diff is shown and the workflow proceeds only after showing it
- [ ] PASS: Step 6 commit message includes the session IDs and correction summaries as evidence — not just the rule text
- [ ] PASS: Step 7 updates the pattern file status to `pr_submitted` and attempts to record the PR URL (or notes push failure)
- [ ] PARTIAL: Skill returns to `main` after completing the workflow — never leaves the marketplace repo on a feature branch

## Output expectations

- [ ] PASS: Output locates the marketplace repo path by reading project settings or config — not assuming a hardcoded path like `~/code/turtlestack`
- [ ] PASS: Output reads the rule file `.claude/rules/learned--verify-before-declaring-complete.md` and confirms the trigger count is at or above the minimum threshold (>=3) — citing the actual count (5) from the file's metadata
- [ ] PASS: Output maps the learning to a specific target file in the marketplace — likely a rule file (e.g. under `plugins/practices/coding-standards/rules/` or thinking/rules) — and explains the mapping decision (rule vs skill vs agent vs script)
- [ ] PASS: Output creates a branch from local main (`git checkout -b learnings/verify-before-declaring-complete`) — notes if fetch fails but proceeds with local state
- [ ] PASS: Output shows the diff explicitly (`git diff`) before proceeding to the commit step — approval is acknowledged before push is attempted
- [ ] PASS: Output's commit message includes evidence — the 5 session IDs where the pattern was triggered, with brief correction summaries — not just the rule text
- [ ] PASS: Output uses Conventional Commits for the commit message (e.g. `feat(rules): add verify-before-declaring-complete rule`) per project convention
- [ ] PASS: Output updates the pattern file's status to `pr_submitted` and records the PR URL (or notes push failure) — so future invocations of the skill can detect the already-proposed learning
- [ ] PASS: Output's PR description includes the evidence (sessions, count, why it should be marketplace-wide), the proposed rule wording, and a request for review
- [ ] PARTIAL: Output returns to the `main` branch in the marketplace repo at the end of the workflow — leaving on the feature branch is flagged as cleanup pending
