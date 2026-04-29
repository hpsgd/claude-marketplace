# Output: Write PRD

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 17/19 criteria met (89%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Skill requires a problem statement section that is separate from the solution description — Step 2 explicitly says "State the problem in one sentence. Not the solution, not the feature — the problem." Anti-patterns list "Solution-first PRDs."
- [x] PASS: Skill requires RICE scoring to justify prioritisation — Step 4 is a full RICE prioritisation section with formula and scoring guidance.
- [x] PASS: Skill requires three types of success metrics: leading indicators, lagging indicators, and guardrail metrics — Step 5 defines all three explicitly with examples.
- [x] PASS: Skill requires a pre-mortem or risk analysis section — Step 8 is titled "Risks and Pre-Mortem" and explicitly references the pre-mortem technique.
- [x] PASS: Skill requires explicit out-of-scope statements — Step 7 requires both "Out of scope" with reasoning per item and "Anti-requirements."
- [x] PASS: Skill produces a structured document with named sections — Output Format specifies writing to `docs/prd-[feature-name].md` with the section structure above; mandatory steps map directly to named document sections.
- [x] PASS: Skill requires a rollout or release strategy section — Step 9 "Launch Plan" is a mandatory structured section with rollout strategy, rollback criteria, monitoring, communication, and documentation sub-fields. This fully satisfies the criterion as a required structured section, not just a mention. (PARTIAL prefix limits ceiling to 0.5 by rubric rules — scored 0.5.)
- [x] PASS: Skill requires success criteria to be measurable — Step 5 failure definition requires specific thresholds like "Less than 10% adoption after 4 weeks"; Quality Checklist enforces measurability.
- [x] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields — frontmatter present with all three required fields.

### Output expectations

- [x] PASS: Output's problem statement is separate from the solution — Step 2 requires problem stated "Not the solution, not the feature — the problem" before solution description; anti-patterns reinforce this.
- [x] PASS: Output's RICE score shown numerically per cell — Step 4 table requires Reach as "N users/quarter," Impact as numbered scale, Confidence as %, Effort as person-weeks, with formula.
- [x] PASS: Output's leading-indicator metrics are pre-launch/early signal — Step 5 specifies "measurable within the first week" for leading indicators with adoption rate, activation rate, error rate examples.
- [x] PASS: Output's lagging-indicator metrics measure actual outcome — Step 5 specifies "measurable after 4-8 weeks" with retention, task completion, revenue impact examples.
- [x] PASS: Output's guardrail metrics name what must NOT regress — Step 5 defines guardrail metrics explicitly as "must NOT get worse," covering existing feature usage, performance, support volume.
- [ ] FAIL: Output's pre-mortem identifies at least 3-5 specific risks with mitigation per risk — Step 8 provides four categorical risk types (value, usability, feasibility, viability) as question-answer table rows, not a list of named specific risks with individual mitigations. The skill doesn't require enumerating concrete risks like "permission escalation via CSV row" or "duplicate-email handling" — it assesses risk categories, not specific risks.
- [x] PASS: Output's out-of-scope section is explicit — Step 7 requires listing excluded items with reasoning per item and "Anti-requirements" that make exclusions visible to reviewers.
- [x] PASS: Output's success criteria are measurable — Step 5 failure definition requires specific thresholds; Quality Checklist enforces measurability.
- [x] PASS: Output addresses rollout strategy — Step 9 requires rollout strategy (big bang / percentage rollout / beta → GA / feature flag), rollback criteria, and monitoring before launch.
- [ ] FAIL: Output references the related coordinator skill (`/coordinator:write-spec`) — Related Skills section links to `/product-owner:write-user-story` and `/product-owner:groom-backlog` only. No reference to a coordinator skill or engineering-facing technical spec handoff.

## Notes

Two gaps pull output expectations below a clean pass:

1. **Pre-mortem specificity**: The four-category risk table (value/usability/feasibility/viability) is a solid framework but produces categorical assessments, not a list of named risks with per-risk mitigations. For a bulk CSV import feature, the obvious specific risks (permission escalation, duplicate email handling, performance at 1,000 rows) would need to be named individually to satisfy the test expectation. The skill doesn't require that granularity.

2. **No cross-skill handoff reference**: The test expects a pointer from the PRD skill to `/coordinator:write-spec` as the downstream engineering-facing artefact. The skill's Related Skills section correctly references downstream product-owner skills but doesn't name the handoff to engineering.

The rollout section is a full structured requirement (Step 9) — it exceeds the PARTIAL threshold but rubric rules cap the criterion at 0.5 regardless.

The skill definition itself is strong and thorough. The sizing table, ISC Splitting Test, and quantified kill condition are above-average elements. The "Do not skip sections" instruction in the preamble conflicts with the sizing table for small-effort tickets (one is permissive, one is absolute) — a quality observation not captured in the rubric.
