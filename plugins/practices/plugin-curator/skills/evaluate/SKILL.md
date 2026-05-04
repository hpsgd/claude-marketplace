---
name: evaluate
description: "Run rubric-style tests against skill and agent plugins by invoking them headlessly, capturing real output and artifacts, and judging against test criteria. Replaces the prior simulation-based evaluator. Use to verify a single test, a directory of tests, or every test in the marketplace."
argument-hint: "[test path or directory; default: all of examples/]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Evaluate

Run rubric tests against plugin definitions. Each run invokes the skill or agent in a real headless `claude -p` session, captures the chat response and any files written, then asks a judge model to score against the test's criteria.

This skill **does not simulate**. Earlier versions wrote `result.md` files containing imagined output. That was unreliable — fixes against simulated weaknesses didn't always change real-run behaviour. The runner now executes targets for real.

## Modes

`$ARGUMENTS` selects the scope:

| Mode | Trigger | Action |
|---|---|---|
| Empty / `all` | `/evaluate` | Run every `test.md` under `examples/` |
| Directory | `/evaluate examples/research` | Run every `test.md` under that subtree |
| Single test | `/evaluate examples/practices/thinking/skills/handoff` | Run only that one test |

## Step 1: Resolve runner

The runner script lives at:

```bash
RUNNER="${CLAUDE_PLUGIN_ROOT}/scripts/run-test.py"
```

If the script doesn't exist, stop and tell the user to install or update the `plugin-curator` plugin.

## Step 2: Discover tests

Find every `test.md` under the requested scope:

```bash
SCOPE="${ARGUMENTS:-examples}"
find "$SCOPE" -type f -name 'test.md' 2>/dev/null | sort
```

If `$SCOPE` is itself a test directory (contains `test.md`), use that single test.

If no `test.md` files exist, report that plainly and stop.

## Step 3: Resolve plugin source per test

For each `test.md`, derive the plugin under test:

- **Skill test:** path matches `examples/<category>/<plugin>/skills/<name>/test.md` → plugin source is `plugins/<category>/<plugin>` (the directory containing `.claude-plugin/plugin.json`)
- **Agent test:** path matches `examples/<category>/<plugin>/agents/<role>/<scenario>/test.md` → plugin source is `plugins/<category>/<plugin>`

Verify the plugin source has `.claude-plugin/plugin.json` before invoking the runner. If missing, skip the test and record `missing-plugin` in the report.

## Step 4: Invoke the runner

For each (test, plugin) pair, run:

```bash
"$RUNNER" \
  --test-dir "<test_dir>" \
  --plugin-dir "<plugin_dir>" \
  --target-model claude-haiku-4-5-20251001 \
  --judge-model claude-sonnet-4-6
```

The runner emits a JSON summary on stdout. Capture that. The runner also writes `result.md` to `<test_dir>` for inspection.

Exit code reflects the verdict:

- `0` PASS (≥ 80%)
- `1` PARTIAL (≥ 60%)
- `2` FAIL (< 60%)
- `3+` infrastructure error (workspace setup, claude invocation, judge response unparseable)

Treat exit codes ≥ 3 as failures of the harness, not the skill — record them as `infra-error` in the report and continue.

For long batches, run sequentially. Parallel runs are safe in principle (each gets its own tmp workspace) but cost-of-debugging outweighs the speed-up for now.

## Step 5: Aggregate results

For directory or all-tests mode, collect every JSON summary into a single report at `examples/REPORT.md`:

```markdown
# Evaluation report

| Field | Value |
|---|---|
| Run date | <YYYY-MM-DD> |
| Total | N tests |
| Passed | N |
| Partial | N |
| Failed | N |
| Infra errors | N |
| Score range | X%–Y% |
| Average | Z% |
| Median | M% |
| Total cost | $X.XX |
| Total duration | XmYs |

## Results

| Test | Type | Verdict | Score | Cost | Duration |
|---|---|---|---|---|---|
| <relative-path> | skill\|agent | PASS\|PARTIAL\|FAIL | X/Y (Z%) | $0.XX | XX s |
```

Sort the table by score ascending so the lowest-scoring tests surface first. Verdicts under PASS deserve attention before the high scorers.

For single-test mode, skip the report file and just print the runner's JSON output along with the `result.md` path.

## Step 6: Report back

Print a summary table and flag anything that needs attention:

- Tests with `FAIL` verdict
- Tests with `infra-error`
- Tests with `PARTIAL` that previously passed (regression)
- Tests where target cost or duration is significantly above the median (suggests the skill is wandering)

Don't suggest fixes here — that's a separate workflow. Just surface the data.

## Argument matrix

| Argument | Behaviour |
|---|---|
| (empty) | Run all of `examples/`, write `REPORT.md` |
| `examples/research` | Run all tests under that subtree, write `REPORT.md` |
| `examples/practices/thinking/skills/handoff` | Run that single test, no report |
| `path/that/doesnt/exist` | Report missing path, stop |
| Anything else | Treat as a path, glob for `test.md` underneath |

## Rules

- **Real execution only.** Never write a `result.md` containing simulated output. If the runner can't fire (e.g. `claude` not in PATH, no auth), report the infrastructure failure — don't fabricate a score.
- **One test, one workspace.** The runner creates a fresh tmp workspace per test. Never reuse workspaces across tests — cross-contamination invalidates results.
- **Sort by score ascending.** The bottom of the table is what matters. Don't bury low scorers.
- **Don't tune until you've measured.** If a test scores below 80%, surface it. Don't immediately edit the skill — first confirm the gap is real (re-run if judge variance is plausible), then fix.
- **Treat infra errors as bugs in the harness, not the skill.** Don't downgrade a skill verdict because the runner couldn't authenticate or the workspace got wedged. Fix the harness first.

## Output format

### Single-test mode

```markdown
## Evaluated: <test path>

**Verdict:** <PASS|PARTIAL|FAIL>
**Score:** X/Y (Z%)
**Target cost:** $0.XX
**Target duration:** XX s
**Result file:** `<test_dir>/result.md`

<one paragraph summary of any criteria that didn't pass, or notes from the judge>
```

### Multi-test mode

Print the full `REPORT.md` table to the chat, then point at the file:

```markdown
Wrote evaluation report to `examples/REPORT.md` — N tests, X passed, Y partial, Z failed.
Total cost $X.XX, total duration XmYs.

<sub-90% tests listed inline so they're impossible to miss>
```

## Related skills

- `/plugin-curator:create-skill` — scaffolds new skills with a `test.md` ready to evaluate
- `/plugin-curator:audit-skill` — structural audit (separate from rubric evaluation)
- `/plugin-curator:audit-agent` — same, for agents

## Downstream usage

The runner is portable and has no marketplace-specific assumptions. To use the same harness in a downstream repo, copy `scripts/run-test.py` and `scripts/judge-prompt.md` into the target project. See `${CLAUDE_PLUGIN_ROOT}/scripts/README.md` for full vendoring instructions.
