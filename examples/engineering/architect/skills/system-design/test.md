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
