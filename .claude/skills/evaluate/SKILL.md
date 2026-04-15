# Evaluate a single example

Evaluate one test case against its plugin definition.

## Usage

Run against a specific example path:

```
/evaluate examples/research/analyst/skills/company-lookup
/evaluate examples/research/investigator/agents/investigator/gate-enforcement
```

## Steps

1. Parse the path to determine if this is a skill test or agent test
   - Path contains `/skills/` → skill test
   - Path contains `/agents/` → agent test

2. Read `prompt.md` and `expected.md` from the given path

3. Resolve the plugin source path:
   - Skill: replace `examples/` prefix with `plugins/`, append `/SKILL.md`
   - Agent: replace `examples/` prefix with `plugins/`, find `agents/<name>.md`

4. Dispatch to the evaluator agent with the test case details

5. The evaluator writes `output.md` to the test case directory

6. Report the verdict and score

## What gets reported

After evaluation, report:
- Verdict (PASS / PARTIAL / FAIL)
- Score (N/M, X%)
- Any notable issues from the Notes section
- Path to the output file
