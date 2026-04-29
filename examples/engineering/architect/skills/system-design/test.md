# Test: system-design skill structure

Scenario: Checking that the system-design skill enforces quantified requirements, a mandatory assumption ledger, Mermaid diagrams following the C4 model, and a confidence assessment per component.

## Prompt

Review the system-design skill definition and verify it produces complete, structured architecture documentation rather than informal diagrams.

## Criteria

- [ ] PASS: Skill explicitly rejects vague non-functional requirements — requires numbers (e.g. "p95 < 200ms", "10K concurrent users") not adjectives ("fast", "scalable")
- [ ] PASS: Skill mandates a numbered assumption ledger with confidence rating and validation method for each assumption
- [ ] PASS: Skill requires an options analysis for every significant design decision, with at least two options and a rationale for the chosen one
- [ ] PASS: Skill requires Mermaid diagrams — specifically component and sequence diagrams — as mandatory output elements
- [ ] PASS: Skill describes the C4 model levels (Context, Container, Component) and requires at minimum Level 1 and Level 2 diagrams
- [ ] PASS: Skill requires a confidence assessment table per component with a rule that components below 60% confidence must have a spike planned
- [ ] PASS: Skill requires a change impact analysis (what-if scenarios) covering traffic growth, new client types, and dependency outages
- [ ] PASS: Skill lists anti-patterns including premature microservices, distributed monolith, and shared database
- [ ] PARTIAL: Skill references arc42 as the output structure standard and links to the system-design template

## Output expectations

- [ ] PASS: Output is structured as a verification of the skill (PASS/FAIL per requirement) rather than producing a sample design
- [ ] PASS: Output verifies the skill rejects vague NFRs and quotes the rule that requires numeric thresholds (e.g. p95, RPS, concurrent users) instead of adjectives like "fast" or "scalable"
- [ ] PASS: Output verifies the assumption ledger is numbered, with a confidence rating and validation method per assumption — not just an unstructured list
- [ ] PASS: Output verifies that every significant design decision requires options analysis with at least two options and a chosen-option rationale
- [ ] PASS: Output confirms the skill mandates Mermaid diagrams (component and sequence) and references the C4 model with Level 1 (Context) and Level 2 (Container) as minimum
- [ ] PASS: Output confirms the per-component confidence assessment table exists, including the rule that components below 60% confidence trigger a planned spike
- [ ] PASS: Output verifies the change impact / what-if section covers traffic growth, new client types, and dependency outages — not just the happy path
- [ ] PASS: Output verifies the anti-patterns list includes premature microservices, distributed monolith, and shared database by name
- [ ] PARTIAL: Output identifies any genuine gaps — e.g. no explicit rule on when to upgrade C4 Level 3 (Component) diagrams, missing capacity-planning worked example, or no ADR cross-reference convention
