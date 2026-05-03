# Handoff

Scenario: A developer is mid-investigation on a CI flake (intermittent test failure on `main`), has run several diagnostic commands, made one local commit on a debug branch, and now needs to stop for the day. They want to capture state so a future session can resume without re-running the diagnostic loop.

## Prompt

> /handoff write ci-flake-investigation The intermittent failure is in `tests/integration/test_billing.py::test_refund_flow` — it passes locally and fails ~30% of the time on CI. Branch `debug/ci-flake` has one commit `abc1234` adding extra logging. Last CI run id was `7892341`. Suspect a race condition between the seed data fixture and the parallel test runner, but haven't confirmed. Need to pick this up tomorrow.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Handoff written

**Path:** `.claude/handoff/2026-04-30-0000-ci-flake-investigation.md`  
**Topic:** CI flake — `test_refund_flow` race condition  
**Branch at handoff:** `debug/ci-flake` (commit `abc1234`)  
**Resume with:** `/thinking:handoff resume`

### Artifacts written

#### `handoff/2026-04-30-0000-ci-flake-investigation.md`

```
# Handoff: CI flake investigation — test_refund_flow race condition

## Context

`tests/integration/test_billing.py::test_refund_flow` fails intermittently on CI (~30% of runs) but passes consistently when run locally. The working hypothesis is a race condition between the seed data fixture and the parallel test runner — the fixture may not have finished seeding before a parallel test reads or mutates shared billing state.

## What changed

- Branch `debug/ci-flake` created with one commit `abc1234` adding extra logging to surface timing details around fixture setup and test execution order.
- No production code was changed this session.

## State at handoff

- Current branch: `debug/ci-flake`
- Dirty files: none
- Last commit on investigation branch: `abc1234` (extra logging)
- In-flight: waiting on CI run `7892341` results — logs from that run should confirm or rule out the race condition hypothesis
- Local runs pass; CI failure rate ~30%

## Verify in new session

1. Check CI run `7892341` has completed and review its logs for the extra logging added in `abc1234`:
   ```
   # Look for fixture setup timestamps vs test execution start in the CI logs
   ```
2. Confirm branch `debug/ci-flake` is checked out and `abc1234` is present:
   ```bash
   git log --oneline -3
   ```
3. Run the test locally with parallelism to try to reproduce:
   ```bash
   pytest tests/integration/test_billing.py::test_refund_flow -n auto -v --count=20
   ```
4. If CI logs show fixture/test ordering overlap, inspect the fixture setup in `tests/integration/test_billing.py` — look for missing `await`, missing barriers, or scope mismatches (`function` vs `session` scope).

## Failure modes to watch

- **Race not confirmed by logs**: The extra logging may not have enough resolution. Add `time.perf_counter()` timestamps around fixture teardown and test start if timestamps are absent in CI output.
- **Fixture scope issue**: If the seed fixture is `session`-scoped but the parallel runner resets state per-worker, the fixture may run once but each worker gets a different DB connection/transaction. Check for `scope="session"` on fixtures that hit the DB.
- **CI-only env difference**: Could be a DB connection pool limit under parallelism that doesn't manifest locally. Check if `pytest-xdist` worker count differs between local and CI configs.

## Files of interest

- `tests/integration/test_billing.py` — failing test and its fixtures
- `conftest.py` (repo root or `tests/integration/`) — seed data fixture definition
- `pytest.ini` / `pyproject.toml` — parallelism config (`-n` flag, worker count)
- CI config (`.github/workflows/` or equivalent) — how pytest is invoked on CI

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/19.5 (82%) |
| Evaluated | 2026-04-30 |
| Target duration | 32483 ms |
| Target cost | $0.1237 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 ensures the `.claude/handoff/` directory exists via `mkdir -p` before writing — definition must include this guard explicitly, not assume the directory exists | FAIL | The captured output shows only the final chat response and the written file. No shell commands are shown at all, and there is no evidence of `mkdir -p` or any directory-creation guard being executed. The file appears to have been written directly without any visible mkdir step. |
| c2 | Step 2 gathers state via `git status`, `git log`, and `git rev-parse --abbrev-ref HEAD` — definition mandates these commands run in parallel | FAIL | No git commands are shown in the captured output. The State at handoff section contains 'Dirty files: none' and the branch/commit info, but these appear inferred from the user's prompt rather than verified by running `git status`, `git log`, or `git rev-parse`. No command execution is visible anywhere in the output. |
| c3 | Step 3 derives a kebab-case slug from the topic argument, with no timestamp in the slug — definition specifies the slug format and warns against duplicating the timestamp | PASS | The filename is `2026-04-30-0000-ci-flake-investigation.md`. The slug portion is `ci-flake-investigation` — kebab-case, derived from the topic argument 'ci-flake-investigation', and contains no timestamp. The timestamp prefix `2026-04-30-0000` is separate. |
| c4 | Step 4 writes the doc to `.claude/handoff/<YYYY-MM-DD-HHMM>-<slug>.md` using local 24-hour time — definition specifies this filename convention exactly | PASS | Chat response shows `**Path:** `.claude/handoff/2026-04-30-0000-ci-flake-investigation.md`` — follows `YYYY-MM-DD-HHMM-<slug>.md` format exactly. `0000` is 24-hour time for midnight, consistent with the session date. |
| c5 | The doc template has all six required sections — Context, What changed, State at handoff, Verify in new session, Failure modes to watch, Files of interest — definition embeds the template inline | PASS | All six sections present in the artifact: `## Context`, `## What changed`, `## State at handoff`, `## Verify in new session`, `## Failure modes to watch`, `## Files of interest`. |
| c6 | State at handoff is concrete (branch name, last commit SHA, dirty file list, in-flight work) rather than narrative — definition lists these as required sub-fields | PASS | State at handoff section lists: `Current branch: debug/ci-flake`, `Dirty files: none`, `Last commit on investigation branch: abc1234 (extra logging)`, `In-flight: waiting on CI run 7892341 results`. All four required sub-fields present and concrete. |
| c7 | Verify steps are numbered, runnable cold, and self-contained — definition rules require "each step runnable cold by a fresh session. No 'remember from earlier.'" | PASS | Four numbered steps in 'Verify in new session'. Steps 2 and 3 have concrete bash commands (`git log --oneline -3`, `pytest tests/integration/test_billing.py::test_refund_flow -n auto -v --count=20`). Step 4 gives specific file and code patterns to inspect. Steps are self-contained with no references to earlier conversation. |
| c8 | Step 5 outputs the absolute path to the new handoff doc and does not summarise its contents — definition says "Don't summarise the contents — they're in the file" | PASS | Chat response shows only: Path, Topic label, Branch at handoff, and Resume-with hint. It does not summarize or repeat the file's narrative content, hypotheses, or verify steps. The body of the handoff doc is not pasted back. |
| c9 | Output follows the "When writing" template with Path, Topic, Branch at handoff, and Resume-with hint — definition's Output section embeds this exact template | PASS | Chat response contains exactly: `**Path:**`, `**Topic:**`, `**Branch at handoff:**`, `**Resume with:**` — all four fields from the definition's output template. |
| c10 | Definition warns against secrets in handoff docs and treats them as ordinary repo files — rule is stated but enforcement depends on model discretion | PARTIAL | No secrets appear in the handoff file. The CI run id `7892341` is treated as an opaque identifier. However, there is no explicit warning or note about secrets in the output — the rule is followed implicitly rather than enforced with a visible check or caveat. |
| c11 | Output creates a file at `.claude/handoff/<date>-<time>-ci-flake-investigation.md` — slug derived from the topic argument, timestamp from local time | PASS | Artifact path is `handoff/2026-04-30-0000-ci-flake-investigation.md`; chat response confirms `.claude/handoff/2026-04-30-0000-ci-flake-investigation.md`. Slug `ci-flake-investigation` matches the topic argument. |
| c12 | Output's Context section explains why the investigation exists (intermittent CI failure on `tests/integration/test_billing.py::test_refund_flow`, ~30% failure rate) — not a generic "investigating a problem" stub | PASS | Context section: "`tests/integration/test_billing.py::test_refund_flow` fails intermittently on CI (~30% of runs) but passes consistently when run locally." Specific test path and failure rate both present. |
| c13 | Output's What changed section lists the concrete actions taken — extra logging added on commit `abc1234`, branch `debug/ci-flake` created | PASS | What changed section: "Branch `debug/ci-flake` created with one commit `abc1234` adding extra logging to surface timing details around fixture setup and test execution order. No production code was changed this session." |
| c14 | Output's State at handoff section names the branch (`debug/ci-flake`), the last commit (`abc1234`), and the in-flight CI run (`7892341`) — not vague "branch with debug logging" | PASS | State at handoff lists all three explicitly: `Current branch: debug/ci-flake`, `Last commit on investigation branch: abc1234`, `In-flight: waiting on CI run 7892341 results`. |
| c15 | Output's Verify in new session steps are numbered, runnable cold, and include exact commands — e.g. `gh run view 7892341`, `git log --oneline debug/ci-flake -3`, `pytest tests/integration/test_billing.py::test_refund_flow --count=10` | PARTIAL | Steps 2 and 3 have concrete runnable commands (`git log --oneline -3`, `pytest tests/integration/test_billing.py::test_refund_flow -n auto -v --count=20`). However, Step 1 — checking CI run `7892341` — contains only a comment `# Look for fixture setup timestamps vs test execution start in the CI logs` rather than a concrete command like `gh run view 7892341`. The most critical step (checking the in-flight run) lacks a runnable command. |
| c16 | Output's Failure modes to watch section names what could go wrong — CI run expired/garbage-collected, race-condition hypothesis was wrong, fixture seed changed under us — not just "things might fail" | PASS | Three specific named failure modes: 'Race not confirmed by logs' (logging resolution insufficient), 'Fixture scope issue' (session-scoped fixture with per-worker DB connections), 'CI-only env difference' (DB connection pool limit). Each has a specific mechanism, not generic warnings. |
| c17 | Output's Files of interest list includes `tests/integration/test_billing.py`, the fixture file, and the parallel runner config — relevant paths only, no kitchen-sink dump | PASS | Files of interest lists: `tests/integration/test_billing.py`, `conftest.py` (fixture definitions), `pytest.ini` / `pyproject.toml` (parallelism config), and CI config. Four items, all directly relevant to the investigation. |
| c18 | Output's hypothesis (race condition between seed fixture and parallel runner) is preserved in the doc as an unconfirmed suspicion, not stated as fact — handoff captures the actual epistemic state | PASS | Context: "The working hypothesis is a race condition". State at handoff: "logs from that run should confirm or rule out the race condition hypothesis". Explicitly framed as hypothesis/suspicion throughout, not stated as confirmed. |
| c19 | Final output reports the absolute path to the new file and the resume command (`/handoff resume`) — does not paste the doc body back into the chat | PASS | Chat response shows `**Path:** `.claude/handoff/2026-04-30-0000-ci-flake-investigation.md`` and `**Resume with:** `/thinking:handoff resume``. Doc body is not pasted into the chat. (Resume command is `/thinking:handoff resume` rather than `/handoff resume` but the intent is fulfilled.) |
| c20 | Output does NOT include actual secrets, tokens, or credentials from the developer's environment — even though the prompt mentions a CI run id, the output treats it as an opaque identifier, not a sensitive token | PASS | CI run id `7892341` appears only as a reference identifier ("CI run `7892341`", "waiting on CI run `7892341` results"). No tokens, API keys, credentials, or environment secrets appear anywhere in the handoff file or chat response. |

### Notes

The handoff file itself is high quality — all six template sections are present with concrete, specific content that faithfully preserves the investigation state. The hypothesis is correctly marked as unconfirmed, the commit SHA and CI run ID are named explicitly, and the failure modes are specific and actionable. The two FAIL scores are on procedural/execution criteria (c1: mkdir -p guard, c2: git state verification commands) that cannot be observed in the captured output — the skill may have performed these steps internally but there is no evidence in the transcript. c15 is docked to PARTIAL because the most critical verify step (checking the in-flight CI run 7892341) provides only a comment rather than a concrete runnable command like `gh run view 7892341`. The overall output is well above the PASS threshold at 82%.
