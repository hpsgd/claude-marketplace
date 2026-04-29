# Output: Write integration guide

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 14 / 14 criteria met (100%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Skill requires numbered steps — met. Step 3 mandates `## Step N:` format; bullets are not an option.
- [x] PASS: Each step includes expected output — met. Step 3's template has a mandatory `**Expected result:**` block with the rule "Every step needs expected output."
- [x] PASS: Skill requires a complete runnable end-to-end example — met. Step 4 is dedicated to this and states "This is mandatory" and "The complete example is non-negotiable."
- [x] PASS: Skill requires a troubleshooting section covering common failure modes with specific fixes — met. Step 6 now requires 4+ entries (auth error, config mistake, external service unavailable, rate-limit/transient failure) with Cause/Fix structure.
- [x] PASS: Skill requires a prerequisites section before integration steps begin — met. Step 2 defines the Prerequisites checklist template with rules requiring every credential to say where to find it.
- [x] PASS: Skill requires a research step — met. Step 1 is a mandatory research phase covering codebase search, auth method, config/env vars, existing docs, and minimum viable integration scope.
- [x] PASS: Skill covers how to verify the integration is working correctly — met. Step 5 is now a dedicated verification section requiring concrete test data, expected behaviour, and inspection steps, in addition to per-step expected results.
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — met. All three fields present in lines 1-7.

### Output expectations

- [x] PASS: Output's prerequisites section names what the developer needs before starting with explicit credentials and permissions — met. Skill rules require "every credential must say where to find it" and every tool must include its install command.
- [x] PASS: Output's steps are numbered (1, 2, 3...) — met. Mandated by Step 3 format.
- [x] PASS: Output's steps each include expected output/visible result — met. `**Expected result:**` block is required in every step template.
- [x] PASS: Output's complete runnable example covers an end-to-end deal-status sync — met. Step 4 mandates a single complete runnable example covering the full integration flow with run command and expected result.
- [x] PASS: Output's troubleshooting section covers at least 4 common failure modes each with symptom, cause, and specific fix — met. Step 6 explicitly enumerates all four required entry types.
- [x] PASS: Output's verification section explains how the developer confirms the integration is working — met. Step 5 is now a dedicated verification section (not just embedded per-step checks) requiring specific test actions, expected behaviour, and log inspection guidance.

## Notes

The SKILL.md has been significantly improved since the previous evaluation. Two key changes lifted the score:

1. The verification criterion moved from PARTIAL to PASS. Step 5 is now a standalone "Write a verification section" step with a mandatory template, distinct from the per-step expected results in Step 3. The skill explicitly states "Per-step checks confirm each piece works in isolation; the verification section confirms the whole flow works together."

2. The troubleshooting criterion moved from PARTIAL to PASS. Step 6 now requires 4+ entries and enumerates them explicitly: auth error, config mistake, external service unavailable, and rate-limit/transient failure.

The skill is now a well-structured, complete integration guide template. All structural and output criteria are satisfied for the Clearpath/Salesforce scenario described in the prompt.
