# Test: Write PRD

Scenario: Testing whether the write-prd skill definition includes all required sections, RICE scoring, success metrics framework, and pre-mortem analysis.

## Prompt


/product-owner:write-prd for a bulk user import feature that lets admins upload a CSV to add multiple team members at once.

## Criteria


- [ ] PASS: Skill requires a problem statement section that is separate from the solution description
- [ ] PASS: Skill requires RICE scoring to justify prioritisation of the feature
- [ ] PASS: Skill requires three types of success metrics: leading indicators, lagging indicators, and guardrail metrics
- [ ] PASS: Skill requires a pre-mortem or risk analysis section — what could go wrong with this feature
- [ ] PASS: Skill requires explicit out-of-scope statements — not just what's included but what's excluded
- [ ] PASS: Skill produces a structured document with named sections that a team can review, not a prose narrative
- [ ] PARTIAL: Skill requires a rollout or release strategy section — partial credit if phasing is mentioned but not required as a structured section
- [ ] PASS: Skill requires success criteria to be measurable — "users can import" is not acceptable, "95% of CSV imports complete without error" is
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields
