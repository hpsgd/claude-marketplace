# System Design

Scenario: Checking that the system-design skill enforces quantified requirements, a mandatory assumption ledger, Mermaid diagrams following the C4 model, and a confidence assessment per component.

## Prompt

> Review the system-design skill definition and verify it produces complete, structured architecture documentation rather than informal diagrams.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I can't find the skill definition file in the local repository—the `architect:system-design` skill is from the marketplace/turtlestack bundles. However, based on the skill description ("Design a system — service boundaries, data flow, API contracts, and non-functional requirements"), I can outline what "complete, structured documentation" should include and flag gaps:

## What structured system design documentation should produce:

**Required outputs:**
1. **Architecture Decision Record (ADR)** — formal decision with context, options, consequences
2. **Service boundary document** — bounded contexts, responsibilities, ownership
3. **API contracts** — OpenAPI/GraphQL schemas for each service boundary
4. **Data model** — entity definitions, relationships, constraints (not just ER diagram)
5. **Non-functional requirements** — latency, throughput, availability, scalability targets with justification
6. **Deployment topology** — how services map to infrastructure

**What I'd need to verify:**
- Does the skill output Markdown/YAML/structured text, or does it default to Mermaid diagrams?
- Are API contracts machine-readable (OpenAPI/GraphQL schema)?
- Are non-functional requirements quantified with trade-off analysis, not vague?
- Is the output suitable for inclusion in `docs/architecture/` and git versioning?

**Known risks from your rules:**
- Your rule on "Extract callables from day one" suggests architecture should define clear service interfaces upfront
- Your spec-driven rules require "API contract (OpenAPI)" before implementation
- Your event-sourcing rules require documenting context flow and lifecycle events

**Question for you:** Has the system-design skill been used recently, and did it produce something you'd consider complete/incomplete? That would help me evaluate whether it needs refinement or if it's already aligned with your architecture standards.

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 0.0/17.0 (0%) |
| Evaluated | 2026-05-04 |
| Target duration | 16677 ms |
| Target cost | $0.0900 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill explicitly rejects vague non-functional requirements — requires numbers (e.g. "p95 < 200ms", "10K concurrent users") not adjectives ("fast", "scalable") | FAIL | The output mentions NFRs with 'latency, throughput, availability, scalability targets with justification' as a desired output, but never verifies the skill explicitly rejects vague adjectives or mandates numeric thresholds. |
| c2 | Skill mandates a numbered assumption ledger with confidence rating and validation method for each assumption | FAIL | No mention of an assumption ledger, confidence ratings, or validation methods anywhere in the captured output. |
| c3 | Skill requires an options analysis for every significant design decision, with at least two options and a rationale for the chosen one | FAIL | Options analysis for design decisions is not mentioned anywhere in the captured output. |
| c4 | Skill requires Mermaid diagrams — specifically component and sequence diagrams — as mandatory output elements | FAIL | The output asks 'Does the skill output Markdown/YAML/structured text, or does it default to Mermaid diagrams?' as an open question — it does not verify Mermaid diagrams are mandatory. Sequence and component diagram requirements are not mentioned. |
| c5 | Skill describes the C4 model levels (Context, Container, Component) and requires at minimum Level 1 and Level 2 diagrams | FAIL | The C4 model is never referenced in the captured output. |
| c6 | Skill requires a confidence assessment table per component with a rule that components below 60% confidence must have a spike planned | FAIL | No mention of confidence assessment tables, per-component ratings, or spike planning rules in the output. |
| c7 | Skill requires a change impact analysis (what-if scenarios) covering traffic growth, new client types, and dependency outages | FAIL | Change impact analysis and what-if scenarios are not mentioned anywhere in the captured output. |
| c8 | Skill lists anti-patterns including premature microservices, distributed monolith, and shared database | FAIL | No anti-patterns list is referenced in the captured output. 'Premature microservices', 'distributed monolith', and 'shared database' are not named. |
| c9 | Skill references arc42 as the output structure standard and links to the system-design template | FAIL | arc42 is not mentioned anywhere in the captured output. |
| c10 | Output is structured as a verification of the skill (PASS/FAIL per requirement) rather than producing a sample design | FAIL | The output is structured as a bulleted outline of 'what should be included' and 'what I'd need to verify', ending with a question to the user. There is no PASS/FAIL verification structure per requirement. |
| c11 | Output verifies the skill rejects vague NFRs and quotes the rule that requires numeric thresholds (e.g. p95, RPS, concurrent users) instead of adjectives like "fast" or "scalable" | FAIL | The output asks as an open question 'Are non-functional requirements quantified with trade-off analysis, not vague?' but does not verify this against the skill definition or quote any rule. No numeric threshold examples are cited. |
| c12 | Output verifies the assumption ledger is numbered, with a confidence rating and validation method per assumption — not just an unstructured list | FAIL | Assumption ledger is not mentioned anywhere in the captured output. |
| c13 | Output verifies that every significant design decision requires options analysis with at least two options and a chosen-option rationale | FAIL | Options analysis verification is absent from the captured output. |
| c14 | Output confirms the skill mandates Mermaid diagrams (component and sequence) and references the C4 model with Level 1 (Context) and Level 2 (Container) as minimum | FAIL | The output raises Mermaid as a question, not a confirmed mandate. C4 model, Level 1, and Level 2 are not mentioned. |
| c15 | Output confirms the per-component confidence assessment table exists, including the rule that components below 60% confidence trigger a planned spike | FAIL | Per-component confidence assessment and the 60% spike trigger are not mentioned in the captured output. |
| c16 | Output verifies the change impact / what-if section covers traffic growth, new client types, and dependency outages — not just the happy path | FAIL | No verification of a what-if or change impact section appears in the captured output. |
| c17 | Output verifies the anti-patterns list includes premature microservices, distributed monolith, and shared database by name | FAIL | No anti-patterns are named or verified in the captured output. |
| c18 | Output identifies any genuine gaps — e.g. no explicit rule on when to upgrade C4 Level 3 (Component) diagrams, missing capacity-planning worked example, or no ADR cross-reference convention | FAIL | The output poses questions ('Does the skill output...?', 'Are API contracts machine-readable?') framed as things it would need to verify, but explicitly admits it cannot locate the skill definition. These are speculative guesses about potential gaps rather than genuine gaps identified from reviewing the skill. None of the example gaps named in the criterion (C4 Level 3 upgrade rule, capacity-planning example, ADR cross-reference) are mentioned. |

### Notes

The captured output completely fails all criteria. The root cause is that the model admitted it could not locate the skill definition file and then produced a generic outline of what good architecture documentation should look like, framed as questions and 'what I'd need to verify' items. This is the opposite of what was required: a structured PASS/FAIL verification of the actual skill definition against specific requirements. None of the 18 criteria are addressed — not the C4 model, assumption ledger, confidence assessment table, anti-patterns list, arc42 reference, numeric NFR enforcement, options analysis mandate, or change impact analysis. The output ends by asking the user a question rather than delivering a verdict, which violates the task's intent entirely.
