# Evaluate all examples

Run all test cases in the `examples/` directory and produce a summary report.

## Usage

```
/evaluate-all
/evaluate-all examples/research
```

With no argument, runs every example in the repo. With a path argument, scopes to that subtree.

## Steps

1. Glob for all `expected.md` files under `examples/` (or the given subtree)

2. For each test case directory found:
   - Determine test type (skill or agent) from the path
   - Run evaluation via the evaluator agent
   - Collect the verdict and score

3. Write a summary to `examples/REPORT.md`:

```markdown
# Evaluation report

**Run date:** <date>
**Total:** N tests
**Passed:** N | **Partial:** N | **Failed:** N

## Results

| Test | Type | Verdict | Score |
|---|---|---|---|
| research/analyst/skills/company-lookup | skill | PASS | 8/8 (100%) |
| research/investigator/agents/investigator/gate-enforcement | agent | PARTIAL | 6/7 (86%) |
```

4. Print the summary table and flag any failures for follow-up

## Notes

- Skip any directory that has `prompt.md` and `expected.md` but no corresponding plugin source — report these as missing definitions
- Re-running will overwrite existing `output.md` files
- The report overwrites `examples/REPORT.md` each run
