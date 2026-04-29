# Output: Write integration guide

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 11.5 / 18 criteria met (64%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Skill requires numbered steps — met. Step 3 mandates `## Step N:` format and a "One concept per step" rule. Bullet points are not an option.
- [x] PASS: Each step includes expected output — met. Step 3's template includes a mandatory `**Expected result:**` block, and the rules state "Every step needs expected output."
- [x] PASS: Skill requires a complete runnable end-to-end example — met. Step 4 is dedicated to this and states "This is mandatory" and "The complete example is non-negotiable."
- [x] PASS: Skill requires a troubleshooting section covering common failure modes with specific fixes — met. Step 5 defines Cause/Fix structure and mandates at minimum auth error, config mistake, and external-service unavailability entries.
- [x] PASS: Skill requires a prerequisites section before the integration steps begin — met. Step 2 defines the Prerequisites checklist template with rules requiring every credential to say where to find it.
- [x] PASS: Skill requires a research step — met. Step 1 is a mandatory research phase covering codebase search, auth method, config/env vars, existing docs, and minimum viable integration scope.
- [~] PARTIAL: Skill covers how to verify the integration is working correctly — partially met. No dedicated verification section exists; verification is embedded in each step's `**Expected result:**` block and the complete example's expected result. Score: 0.5.
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — met. All three fields present in lines 1-7.

### Output expectations

- [x] PASS: Output's prerequisites section names what the developer needs before starting with explicit credentials and permissions — met. Skill rules require "every credential must say where to find it" and every tool must include its install command.
- [x] PASS: Output's steps are numbered (1, 2, 3...) — met. Mandated by Step 3 format.
- [x] PASS: Output's steps each include expected output/visible result — met. `**Expected result:**` block is required in every step template.
- [ ] FAIL: Output's mapping step covers field-level mapping (Salesforce Opportunity stage → Clearpath project status, 3+ stages) — not found. The skill is generic and does not direct the agent to produce an explicit field mapping table. A mapping may or may not appear depending on what the agent infers from the argument.
- [x] PASS: Output's complete runnable example covers an end-to-end deal-status sync — met. Step 4 mandates a single complete runnable example covering the full integration flow.
- [~] PARTIAL: Output's troubleshooting section covers at least 4 common failure modes (auth token expired, field mapping mismatch, rate-limit hit, webhook delivery failure) — partially met. Skill requires only 3+ entries covering auth, config mistake, and external-service unavailability. A fourth mode (rate-limit or webhook delivery failure) is not guaranteed by the skill definition. Score: 0.5.
- [ ] FAIL: Output addresses sync direction explicitly (one-way vs bidirectional, conflict resolution) — not found. Not mentioned anywhere in the skill.
- [~] PARTIAL: Output's verification section explains how the developer confirms the integration is working — partially met. Embedded per-step via expected results but no dedicated verification section is mandated. Score: 0.5.
- [ ] FAIL: Output addresses the initial historical sync vs ongoing sync — not found. Not mentioned in the skill.
- [ ] FAIL: Output addresses how to disable/pause the integration safely — not found. Not mentioned in the skill.

## Notes

The skill handles universal integration-guide requirements well: numbered steps, expected outputs per step, mandatory complete example, troubleshooting with cause/fix structure. The structural criteria (8/8) are all met or partially met.

The output expectation failures are all integration-specific concerns the skill never prompts for:

- **Sync direction and conflict resolution** — critical for any sync integration; should be a standard research question in Step 1 or a dedicated section in the output format.
- **Historical backfill vs ongoing sync** — a common source of confusion; worth a research prompt.
- **Disable/pause instructions** — incident response standard; could be a mandatory Next Steps entry.
- **Field-level mapping table** — the research step could direct the agent to enumerate mappings explicitly when the integration is data-sync oriented.

The skill is a solid generic integration guide template. It would produce a well-structured guide but would miss several integration-specific concerns that an experienced integrations writer would cover as standard practice.

One minor structural tension noted previously: the Output Format section presents a structure (Quick Start before Step-by-Step Walkthrough) that differs from the mandatory process in Steps 1-5, which places the complete example after the numbered steps. The process steps should be treated as authoritative.
