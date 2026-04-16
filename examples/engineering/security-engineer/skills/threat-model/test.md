# Test: threat-model skill structure

Scenario: Checking that the threat-model skill mandates data flow mapping before STRIDE analysis, requires risk scoring (likelihood x impact) for every threat, and produces an actionable risk register rather than a generic threat catalogue.

## Prompt

Review the threat-model skill definition and verify it produces a system-specific threat model rather than a generic security checklist.

## Criteria

- [ ] PASS: Skill requires scope definition first — system name, included components, excluded components, and a threat actor table with motivation and capability for each actor type
- [ ] PASS: Skill mandates data flow mapping using a Mermaid diagram with trust boundaries before any STRIDE analysis begins
- [ ] PASS: Skill requires a data flow inventory table annotating each flow with protocol, authentication, encryption, and data classification
- [ ] PASS: Skill applies STRIDE analysis per component and data flow with specific evidence-based questions for each of the six categories
- [ ] PASS: Skill requires every identified threat to be scored using a likelihood x impact risk matrix — not just labelled as high/medium/low without justification
- [ ] PASS: Skill requires mitigations table with control type (preventive/detective/corrective) and implementation status for each threat
- [ ] PASS: Skill requires at least one preventive control per threat — detective/corrective controls are additions, not substitutes
- [ ] PARTIAL: Skill addresses residual risk assessment after mitigations — accepted risks must have an owner and review date
