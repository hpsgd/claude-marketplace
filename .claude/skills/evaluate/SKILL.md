# Evaluate

Run test cases against their plugin definitions. Works at three levels:

- `/evaluate` — run all tests in `examples/`
- `/evaluate examples/research` — run all tests under a directory
- `/evaluate examples/research/analyst/skills/company-lookup.md` — run a single test

## Steps

1. **Discover test files.** Based on the argument:
   - No argument: glob for all `.md` files under `examples/` that contain a `## Criteria` section
   - Directory path: glob within that directory
   - File path: use that single file
   - Skip `REPORT.md` when globbing

2. **For each test file:**

   a. Parse the path to determine test type: `/skills/` → skill test, `/agents/` → agent test

   b. Read the test file. It contains Prompt and Criteria above the `<!-- EVALUATION BELOW -->` marker, and (optionally) previous Output and Evaluation below it.

   c. Resolve the plugin source path:
      - Skill: replace `examples/` prefix with `plugins/`, replace the filename with the stem + `/SKILL.md` (e.g. `company-lookup.md` → `company-lookup/SKILL.md`)
      - Agent: replace `examples/` prefix with `plugins/`, find `agents/<name>.md` by walking up from the test file
      - Skip any test file with no corresponding plugin source. Report as missing definition.

   d. Dispatch to the evaluator agent with the test case details

   e. The evaluator generates the simulated output and evaluation, then rewrites everything below the `<!-- EVALUATION BELOW -->` marker. Content above the marker is preserved. The structure below the marker MUST be:

      ```
      ## Output

      [Full simulated output demonstrating what the skill/agent would
       actually produce for this prompt. This is the most valuable part
       of the test — it shows what quality output looks like. Must be
       realistic and substantial, not a summary or stub.]

      ## Evaluation

      **Verdict:** PASS/PARTIAL/FAIL
      **Score:** X/Y (Z%)
      **Evaluated:** [date]

      [Per-criterion results with evidence]

      ### Notes
      [Notable findings]
      ```

      The `## Output` section is MANDATORY. An evaluation without a simulated output is incomplete. The output should be long enough to demonstrate the skill's actual deliverable — a PRD should look like a PRD, a threat model should look like a threat model, a code review should look like a code review.

   f. Collect the verdict and score

3. **Write summary report** to `examples/REPORT.md` (overwrites previous):

   ```markdown
   # Evaluation report

   **Run date:** <date>
   **Total:** N tests
   **Passed:** N | **Partial:** N | **Failed:** N

   ## Results

   | Test | Type | Description | Verdict | Score |
   |---|---|---|---|---|
   | research/analyst/skills/company-lookup | skill | Research a company's structure, financials, and market position | PASS | 7/7 (100%) |
   ```

4. Print the summary table and flag any failures for follow-up. For single-file runs, skip the report file and just print the result inline.

## What gets reported

After evaluation, report:

- Verdict (PASS / PARTIAL / FAIL)
- Score (N/M, X%)
- Any notable issues from the Notes section
- Path to the test file

## Scoring rules

- PASS criterion = 1 point, PARTIAL = 0.5, FAIL = 0, SKIP = excluded from denominator
- Verdict: PASS if score >= 80%, PARTIAL if >= 60%, FAIL if < 60%

## Criterion prefix rules

The prefix on each criterion (`PASS:`, `PARTIAL:`, `SKIP:`) sets the **ceiling**, not the expected result:

- `PASS:` — can score PASS, PARTIAL, or FAIL based on evidence
- `PARTIAL:` — **maximum score is 0.5 points.** Even if the definition fully satisfies it, score it as PARTIAL. The test author set this ceiling deliberately. Never upgrade a PARTIAL-prefixed criterion to PASS.
- `SKIP:` — excluded from scoring entirely

## Evaluator calibration

These rules govern how the evaluator assesses criteria against plugin definitions:

**Evaluate the definition, not your own output.** The simulated output exists to demonstrate what the definition would produce. The evaluation must assess whether the plugin definition (SKILL.md or agent.md) explicitly requires, enforces, or guides each criterion. "The output I generated matches" is not evidence. "The definition's Step 3 requires X with template Y" is evidence.

**PASS requires explicit support.** The definition must contain a specific instruction, template field, required step, or enforcement mechanism for the criterion. "The definition doesn't contradict this" is not a PASS. "The definition is consistent with this" is not a PASS. The criterion must be traceable to a specific part of the definition.

**PARTIAL is for partial coverage.** Give PARTIAL when the definition addresses the criterion but incompletely: mentioned but not required, suggested but not enforced, covered by implication but not by explicit instruction.

**FAIL is a valid outcome.** If the definition contains no instruction, template, or mechanism that addresses a criterion, score it FAIL. Zero failures across a full test suite is a signal that the evaluator is too lenient, not that every definition is perfect.

**Simulated outputs should be realistic, not perfect.** When generating the simulated output, reflect the definition's actual coverage. If the definition has a gap that would affect a criterion, the output should show that gap. Do not generate output that compensates for missing definition guidance.

**Independence between criteria.** Evaluate each criterion independently. Do not let a strong result on one criterion influence your assessment of another.

**Source citation quality in simulated outputs.** For research-related tests (anything under `examples/research/`), simulated output source citations must use specific deep links, not generic homepages. `linkedin.com/company/safetyculture` not `linkedin.com`. `crt.sh/?q=example.com` not `crt.sh`. When a registry doesn't support deep linking, state the exact search path used. Every source gets an access date. If the plugin definition has a `rules/source-citations.md` rule installed, the simulated output must follow it.
