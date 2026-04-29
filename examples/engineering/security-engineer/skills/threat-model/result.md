# Output: threat-model skill structure

**Verdict:** PARTIAL
**Score:** 15.5/18 criteria met (86%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill requires scope definition first — system name, included components, excluded components, and a threat actor table with motivation and capability for each actor type — Step 1 covers all four elements with a populated actor table including motivation, capability, and examples columns
- [x] PASS: Skill mandates data flow mapping using a Mermaid diagram with trust boundaries before any STRIDE analysis begins — Step 2 is explicitly labelled MANDATORY and precedes Step 3 (STRIDE), with a full Mermaid diagram using subgraph trust boundaries
- [x] PASS: Skill requires a data flow inventory table annotating each flow with protocol, authentication, encryption, and data classification — the table immediately follows the Mermaid diagram with all four columns present
- [x] PASS: Skill applies STRIDE analysis per component and data flow with specific evidence-based questions for each of the six categories — Step 3 applies all six STRIDE categories with "Evidence to check" question tables for each
- [x] PASS: Skill requires every identified threat to be scored using a likelihood x impact risk matrix — Step 4 is labelled MANDATORY and provides a 3x4 likelihood/impact matrix with defined criteria for each level
- [x] PASS: Skill requires mitigations table with control type (preventive/detective/corrective) and implementation status for each threat — Step 5 table has STRIDE, Threat, Risk, Mitigation, Control type, and Status columns
- [x] PASS: Skill requires at least one preventive control per threat — Step 5 states explicitly: "Each threat must have at least one preventive control. Detective and corrective controls are layered on top"
- [~] PARTIAL: Skill addresses residual risk assessment after mitigations — Step 6 covers residual risk and accepted risks. The output template includes an Accepted Risks table with Owner and Review date columns, and Step 6 prose says "Document them explicitly with an owner and review date." The requirement is present but framed as guidance rather than a hard rule (no MANDATORY label, no anti-pattern calling out missing owners)

### Output expectations

- [x] PASS: Output is structured as a verification of the skill (verdict per requirement) rather than running an actual threat model — this result follows that format
- [x] PASS: Output verifies the scope-first rule — system name, included components, excluded components, and a threat actor table with motivation and capability per actor type — confirmed: all four elements present in Step 1
- [x] PASS: Output confirms data flow diagrams are mandatory and rendered in Mermaid with trust boundaries marked, BEFORE any STRIDE analysis — confirmed: Step 2 labelled MANDATORY, Mermaid subgraph trust boundaries used, Step 2 precedes Step 3
- [x] PASS: Output verifies the data flow inventory annotates each flow with protocol, authentication mechanism, encryption status, and data classification — confirmed: table has all four columns with example rows
- [x] PASS: Output confirms STRIDE analysis is applied per component AND per data flow with specific evidence-based questions for each of the six STRIDE categories — confirmed: all six categories present with evidence-based question tables
- [x] PASS: Output verifies every threat is scored using a likelihood x impact risk matrix — the matrix is 3x4 (Low/Medium/High likelihood × Low/Medium/High/Critical impact) with explicit outcome cells per combination, not just verbal labels
- [x] PASS: Output confirms the mitigations table requires control type per mitigation (preventive / detective / corrective) and implementation status — confirmed; Status column present with examples showing Implemented and TODO
- [x] PASS: Output verifies every threat must have at least one preventive control — confirmed with explicit statement in Step 5
- [x] PASS: Output confirms residual risk after mitigations is documented, with accepted risks requiring a named owner and a review date — confirmed via Step 6 prose and Accepted Risks table in the output template
- [~] PARTIAL: Output identifies any genuine gaps — two gaps worth noting: (1) no concrete re-run trigger criteria — the Anti-Patterns section says the model must be updated "when the system changes" and the output template has a Review Schedule section, but neither mandates specific triggers (e.g., "re-run when any trust boundary changes, when a new data store is added"); (2) no explicit link between individual threats and monitoring or detection requirements — detective controls are acknowledged in the control type taxonomy but there is no requirement to map each threat to a SIEM rule, alert, or observability instrument

## Notes

The skill is well-constructed and enforces the core STRIDE methodology with more rigour than most definitions of this type. The Anti-Patterns section acts as a second enforcement layer — each major failure mode (no data flows, no risk scoring, missing status) is called out by name, which helps an agent resist shortcuts even under long-context pressure.

The 3x4 matrix (three likelihood levels, four impact levels) is deliberately simpler than a 5x5 grid. This is a reasonable design choice that trades granularity for clarity, but it means the output expectation criterion noting "e.g. 5x5 grid" is met in spirit rather than precisely.

The templates/threat-model.md cross-reference at the end of the skill is worth verifying — if that file does not exist, the reference is a dead end.
