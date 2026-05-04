# Test: handoff write mid-session

Scenario: A developer is mid-investigation on a CI flake (intermittent test failure on `main`), has run several diagnostic commands, made one local commit on a debug branch, and now needs to stop for the day. They want to capture state so a future session can resume without re-running the diagnostic loop.

## Prompt

/handoff write ci-flake-investigation The intermittent failure is in `tests/integration/test_billing.py::test_refund_flow` — it passes locally and fails ~30% of the time on CI. Branch `debug/ci-flake` has one commit `abc1234` adding extra logging. Last CI run id was `7892341`. Suspect a race condition between the seed data fixture and the parallel test runner, but haven't confirmed. Need to pick this up tomorrow.

Write the handoff doc to the `handoff/` directory (workspace-local, accessible in this sandbox — `mkdir -p handoff/` first if needed). State the canonical production path as `.claude/handoff/<YYYY-MM-DD-HHMM>-ci-flake-investigation.md` in your output. Show the full file content INLINE in the chat response.

Before writing, run these git commands in parallel and report output:
```bash
git status
git log -5 --oneline
git rev-parse --abbrev-ref HEAD
```

Doc template (use exactly these section names):
```markdown
# Handoff: ci-flake-investigation

## Context
[1-3 sentences on why we're stopping]

## What changed
[branch + commit + files touched]

## State at handoff
- Branch: debug/ci-flake
- Last commit SHA: abc1234
- Dirty files: [from git status]
- In-flight work: [what's incomplete]

## Verify in new session
1. [Numbered, runnable cold — no "remember from earlier"]
2. ...

## Failure modes to watch
- [Specific things that could go wrong on resume]

## Files of interest
- [Paths to relevant files]
```

End your chat response with the "When writing" template:
```
Path: <absolute path to handoff doc>
Topic: ci-flake-investigation
Branch at handoff: debug/ci-flake
Resume with: /handoff read ci-flake-investigation
```

Do NOT ask permission. Do NOT summarise the file content (the file IS the summary). Do NOT pause for clarification.

A few specifics for the response:

- Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
- Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
- For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
- When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
- Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Criteria

- [ ] PASS: Step 1 ensures the `.claude/handoff/` directory exists via `mkdir -p` before writing — definition must include this guard explicitly, not assume the directory exists
- [ ] PASS: Step 2 gathers state via `git status`, `git log`, and `git rev-parse --abbrev-ref HEAD` — definition mandates these commands run in parallel
- [ ] PASS: Step 3 derives a kebab-case slug from the topic argument, with no timestamp in the slug — definition specifies the slug format and warns against duplicating the timestamp
- [ ] PASS: Step 4 writes the doc to `.claude/handoff/<YYYY-MM-DD-HHMM>-<slug>.md` using local 24-hour time — definition specifies this filename convention exactly
- [ ] PASS: The doc template has all six required sections — Context, What changed, State at handoff, Verify in new session, Failure modes to watch, Files of interest — definition embeds the template inline
- [ ] PASS: State at handoff is concrete (branch name, last commit SHA, dirty file list, in-flight work) rather than narrative — definition lists these as required sub-fields
- [ ] PASS: Verify steps are numbered, runnable cold, and self-contained — definition rules require "each step runnable cold by a fresh session. No 'remember from earlier.'"
- [ ] PASS: Step 5 outputs the absolute path to the new handoff doc and does not summarise its contents — definition says "Don't summarise the contents — they're in the file"
- [ ] PASS: Output follows the "When writing" template with Path, Topic, Branch at handoff, and Resume-with hint — definition's Output section embeds this exact template
- [ ] PARTIAL: Definition warns against secrets in handoff docs and treats them as ordinary repo files — rule is stated but enforcement depends on model discretion

## Output expectations

- [ ] PASS: Output creates a file at `.claude/handoff/<date>-<time>-ci-flake-investigation.md` — slug derived from the topic argument, timestamp from local time
- [ ] PASS: Output's Context section explains why the investigation exists (intermittent CI failure on `tests/integration/test_billing.py::test_refund_flow`, ~30% failure rate) — not a generic "investigating a problem" stub
- [ ] PASS: Output's What changed section lists the concrete actions taken — extra logging added on commit `abc1234`, branch `debug/ci-flake` created
- [ ] PASS: Output's State at handoff section names the branch (`debug/ci-flake`), the last commit (`abc1234`), and the in-flight CI run (`7892341`) — not vague "branch with debug logging"
- [ ] PASS: Output's Verify in new session steps are numbered, runnable cold, and include exact commands — e.g. `gh run view 7892341`, `git log --oneline debug/ci-flake -3`, `pytest tests/integration/test_billing.py::test_refund_flow --count=10`
- [ ] PASS: Output's Failure modes to watch section names what could go wrong — CI run expired/garbage-collected, race-condition hypothesis was wrong, fixture seed changed under us — not just "things might fail"
- [ ] PASS: Output's Files of interest list includes `tests/integration/test_billing.py`, the fixture file, and the parallel runner config — relevant paths only, no kitchen-sink dump
- [ ] PASS: Output's hypothesis (race condition between seed fixture and parallel runner) is preserved in the doc as an unconfirmed suspicion, not stated as fact — handoff captures the actual epistemic state
- [ ] PASS: Final output reports the absolute path to the new file and the resume command (`/handoff resume`) — does not paste the doc body back into the chat
- [ ] PASS: Output does NOT include actual secrets, tokens, or credentials from the developer's environment — even though the prompt mentions a CI run id, the output treats it as an opaque identifier, not a sensitive token
