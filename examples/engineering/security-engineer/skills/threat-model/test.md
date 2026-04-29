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

## Output expectations

- [ ] PASS: Output is structured as a verification of the skill (verdict per requirement) rather than running an actual threat model
- [ ] PASS: Output verifies the scope-first rule — system name, included components, excluded components, and a threat actor table with motivation and capability per actor type
- [ ] PASS: Output confirms data flow diagrams are mandatory and rendered in Mermaid with trust boundaries marked, BEFORE any STRIDE analysis
- [ ] PASS: Output verifies the data flow inventory annotates each flow with protocol, authentication mechanism, encryption status, and data classification
- [ ] PASS: Output confirms STRIDE analysis is applied per component AND per data flow with specific evidence-based questions for each of the six STRIDE categories (Spoofing, Tampering, Repudiation, Information disclosure, DoS, Elevation of privilege)
- [ ] PASS: Output verifies every threat is scored using a likelihood × impact risk matrix (e.g. 5×5 grid) — not just a verbal high/medium/low
- [ ] PASS: Output confirms the mitigations table requires control type per mitigation (preventive / detective / corrective) and implementation status (planned / in-progress / done)
- [ ] PASS: Output verifies every threat must have at least one preventive control — detective and corrective controls are additions, not substitutes
- [ ] PASS: Output confirms residual risk after mitigations is documented, with accepted risks requiring a named owner and a review date
- [ ] PARTIAL: Output identifies any genuine gaps — e.g. no rule on threat-model versioning (when does the model need to be re-run after architectural change?), no link between threats and detection / monitoring requirements
