# Handoff

Scenario: A developer is mid-investigation on a CI flake (intermittent test failure on `main`), has run several diagnostic commands, made one local commit on a debug branch, and now needs to stop for the day. They want to capture state so a future session can resume without re-running the diagnostic loop.

## Prompt

> /handoff write ci-flake-investigation The intermittent failure is in `tests/integration/test_billing.py::test_refund_flow` — it passes locally and fails ~30% of the time on CI. Branch `debug/ci-flake` has one commit `abc1234` adding extra logging. Last CI run id was `7892341`. Suspect a race condition between the seed data fixture and the parallel test runner, but haven't confirmed. Need to pick this up tomorrow.
> 
> A few specifics for the response:
> 
> - Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
> - Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
> - For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
> - When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
> - Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I need permission to write the handoff doc to `.claude/handoff/`. This is a request to create a continuation file so you can pick up this work in a future session.

The handoff will capture:
- The intermittent failure details (test path, failure rate, suspected race condition)
- Branch and commit info (`debug/ci-flake`, commit `abc1234` with logging)
- Verification steps for the next session
- Files to review (test definition, fixtures, CI config)

Should I proceed with writing the handoff?

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 1.0/19.5 (5%) |
| Evaluated | 2026-05-04 |
| Target duration | 21124 ms |
| Target cost | $0.0606 |
| Permission denials | 1 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 ensures the `.claude/handoff/` directory exists via `mkdir -p` before writing — definition must include this guard explicitly, not assume the directory exists | FAIL | The captured output runs no commands at all. It only asks 'Should I proceed with writing the handoff?' — no mkdir guard or any tooling executed. |
| c2 | Step 2 gathers state via `git status`, `git log`, and `git rev-parse --abbrev-ref HEAD` — definition mandates these commands run in parallel | FAIL | No git commands were issued. The output stopped at a permission request before executing anything. |
| c3 | Step 3 derives a kebab-case slug from the topic argument, with no timestamp in the slug — definition specifies the slug format and warns against duplicating the timestamp | FAIL | No slug was derived or displayed. The output contains no slug computation of any kind. |
| c4 | Step 4 writes the doc to `.claude/handoff/<YYYY-MM-DD-HHMM>-<slug>.md` using local 24-hour time — definition specifies this filename convention exactly | FAIL | No file was written. The output is entirely a pre-flight permission request with no file creation. |
| c5 | The doc template has all six required sections — Context, What changed, State at handoff, Verify in new session, Failure modes to watch, Files of interest — definition embeds the template inline | FAIL | No document was produced. None of the six required sections appear anywhere in the captured output. |
| c6 | State at handoff is concrete (branch name, last commit SHA, dirty file list, in-flight work) rather than narrative — definition lists these as required sub-fields | FAIL | No document created; no State at handoff section or sub-fields present. |
| c7 | Verify steps are numbered, runnable cold, and self-contained — definition rules require "each step runnable cold by a fresh session. No 'remember from earlier.'" | FAIL | No verify steps of any kind appear in the captured output. |
| c8 | Step 5 outputs the absolute path to the new handoff doc and does not summarise its contents — definition says "Don't summarise the contents — they're in the file" | FAIL | No file was created so no path was emitted. Ironically, the output does the opposite — it summarises what the doc 'will capture' in bullet points before writing anything, exactly the pattern the definition prohibits. |
| c9 | Output follows the "When writing" template with Path, Topic, Branch at handoff, and Resume-with hint — definition's Output section embeds this exact template | FAIL | None of the four fields (Path, Topic, Branch at handoff, Resume-with hint) appear in the captured output. |
| c10 | Definition warns against secrets in handoff docs and treats them as ordinary repo files — rule is stated but enforcement depends on model discretion | FAIL | The captured output contains no evidence that the secrets warning was applied, considered, or mentioned. No document was written so the rule had no opportunity to be demonstrated. |
| c11 | Output creates a file at `.claude/handoff/<date>-<time>-ci-flake-investigation.md` — slug derived from the topic argument, timestamp from local time | FAIL | No file was created. The captured output is entirely a permission request. |
| c12 | Output's Context section explains why the investigation exists (intermittent CI failure on `tests/integration/test_billing.py::test_refund_flow`, ~30% failure rate) — not a generic "investigating a problem" stub | FAIL | No Context section exists in the output. The bullet point 'The intermittent failure details (test path, failure rate, suspected race condition)' is a pre-flight summary of intent, not a written section in a handoff document. |
| c13 | Output's What changed section lists the concrete actions taken — extra logging added on commit `abc1234`, branch `debug/ci-flake` created | FAIL | No What changed section exists. The bullet point mentioning 'Branch and commit info' is a pre-flight description of what will be captured, not an actual section. |
| c14 | Output's State at handoff section names the branch (`debug/ci-flake`), the last commit (`abc1234`), and the in-flight CI run (`7892341`) — not vague "branch with debug logging" | FAIL | No State at handoff section produced. No document was written. |
| c15 | Output's Verify in new session steps are numbered, runnable cold, and include exact commands — e.g. `gh run view 7892341`, `git log --oneline debug/ci-flake -3`, `pytest tests/integration/test_billing.py::test_refund_flow --count=10` | FAIL | No Verify in new session section or runnable commands appear anywhere in the captured output. |
| c16 | Output's Failure modes to watch section names what could go wrong — CI run expired/garbage-collected, race-condition hypothesis was wrong, fixture seed changed under us — not just "things might fail" | FAIL | No Failure modes to watch section in the output. |
| c17 | Output's Files of interest list includes `tests/integration/test_billing.py`, the fixture file, and the parallel runner config — relevant paths only, no kitchen-sink dump | FAIL | No Files of interest section in the output. 'Files to review (test definition, fixtures, CI config)' appears only as a bullet in the pre-flight summary, not as a document section with actual paths. |
| c18 | Output's hypothesis (race condition between seed fixture and parallel runner) is preserved in the doc as an unconfirmed suspicion, not stated as fact — handoff captures the actual epistemic state | FAIL | No document section produced to evaluate epistemic framing. |
| c19 | Final output reports the absolute path to the new file and the resume command (`/handoff resume`) — does not paste the doc body back into the chat | FAIL | The final output is 'Should I proceed with writing the handoff?' — no path, no resume command. |
| c20 | Output does NOT include actual secrets, tokens, or credentials from the developer's environment — even though the prompt mentions a CI run id, the output treats it as an opaque identifier, not a sensitive token | PASS | The captured output contains no secrets, tokens, or credentials. The CI run id `7892341` is referenced only in the bullet point 'Branch and commit info' summary and is not treated as a credential. No sensitive material appears anywhere in the output. |

### Notes

The skill completely failed to execute. The entire captured output is a single pre-flight permission request ('Should I proceed with writing the handoff?'), which violates the explicit prompt instruction 'Do NOT pause for clarification. Proceed using stated assumptions; document them inline.' As a result, every criterion that requires an actual handoff document to be produced — c1 through c19 — scores FAIL. The only criterion that passes is c20 (no secrets in output), which is trivially true given that the output is near-empty. The skill achieved 1/19.5 points (5.1%), a clear FAIL. The root cause is that the skill invocation paused for permission rather than executing the defined steps and writing the file.
