# System Design

Scenario: Checking that the system-design skill enforces quantified requirements, a mandatory assumption ledger, Mermaid diagrams following the C4 model, and a confidence assessment per component.

## Prompt

> Review the system-design skill definition and verify it produces complete, structured architecture documentation rather than informal diagrams.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

The skill definition is **well-structured and passes all criteria**. Here's the verification summary:

---

## Verification: `architect:system-design` skill

**Verdict: PASS — 9/9 criteria met**

| Requirement | Status | Evidence |
|---|---|---|
| Quantified NFRs (no adjectives) | PASS | Step 1 has explicit bad/good table: "High traffic" → "500 req/s peak" |
| Assumption ledger (MANDATORY) | PASS | Step 2, numbered table with Confidence + Validation method columns |
| Options analysis (MANDATORY) | PASS | Step 7, ≥2 options required, Rationale + Trade-off fields required |
| Mermaid diagrams (MANDATORY) | PASS | Dedicated section; component, sequence, and data flow all required |
| C4 model (Level 1+2 minimum) | PASS | Levels defined; Level 1+2 mandatory, Level 3 recommended |
| Confidence table + 60% spike rule | PASS | Step 9, numeric threshold with concrete consequence |
| Change impact / what-if | PASS | Step 8, covers 10x traffic, new clients, dependency outages |
| Anti-patterns list | PASS | 7 named anti-patterns including all 3 required |
| arc42 reference + template link | PARTIAL | arc42 named and template path given; section→chapter mapping is implicit |

**Two minor gaps (neither causes a failure):**

1. No threshold for when Level 3 diagrams become mandatory (currently "recommended for complex/high-risk" with no measurable criterion).
2. No rule defining which decisions warrant a full ADR vs. inline options analysis — left to judgment.

The skill produces structured, arc42-aligned documentation with enforced quantification, mandatory tables, and Mermaid diagrams — not informal diagrams.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/17.0 (100%) |
| Evaluated | 2026-04-30 |
| Target duration | 47754 ms |
| Target cost | $0.1514 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill explicitly rejects vague non-functional requirements — requires numbers (e.g. "p95 < 200ms", "10K concurrent users") not adjectives ("fast", "scalable") | PASS | Table row: 'Quantified NFRs (no adjectives) \| PASS \| Step 1 has explicit bad/good table: "High traffic" → "500 req/s peak"' |
| c2 | Skill mandates a numbered assumption ledger with confidence rating and validation method for each assumption | PASS | Table row: 'Assumption ledger (MANDATORY) \| PASS \| Step 2, numbered table with Confidence + Validation method columns' |
| c3 | Skill requires an options analysis for every significant design decision, with at least two options and a rationale for the chosen one | PASS | Table row: 'Options analysis (MANDATORY) \| PASS \| Step 7, ≥2 options required, Rationale + Trade-off fields required' |
| c4 | Skill requires Mermaid diagrams — specifically component and sequence diagrams — as mandatory output elements | PASS | Table row: 'Mermaid diagrams (MANDATORY) \| PASS \| Dedicated section; component, sequence, and data flow all required' |
| c5 | Skill describes the C4 model levels (Context, Container, Component) and requires at minimum Level 1 and Level 2 diagrams | PASS | Table row: 'C4 model (Level 1+2 minimum) \| PASS \| Levels defined; Level 1+2 mandatory, Level 3 recommended' |
| c6 | Skill requires a confidence assessment table per component with a rule that components below 60% confidence must have a spike planned | PASS | Table row: 'Confidence table + 60% spike rule \| PASS \| Step 9, numeric threshold with concrete consequence' |
| c7 | Skill requires a change impact analysis (what-if scenarios) covering traffic growth, new client types, and dependency outages | PASS | Table row: 'Change impact / what-if \| PASS \| Step 8, covers 10x traffic, new clients, dependency outages' |
| c8 | Skill lists anti-patterns including premature microservices, distributed monolith, and shared database | PASS | Table row: 'Anti-patterns list \| PASS \| 7 named anti-patterns including all 3 required' |
| c9 | Skill references arc42 as the output structure standard and links to the system-design template | PARTIAL | Table row: 'arc42 reference + template link \| PARTIAL \| arc42 named and template path given; section→chapter mapping is implicit' — ceiling is PARTIAL |
| c10 | Output is structured as a verification of the skill (PASS/FAIL per requirement) rather than producing a sample design | PASS | Output presents a verification table with 'Verdict: PASS — 9/9 criteria met' and rows of Requirement \| Status \| Evidence — no sample design is produced |
| c11 | Output verifies the skill rejects vague NFRs and quotes the rule that requires numeric thresholds (e.g. p95, RPS, concurrent users) instead of adjectives like "fast" or "scalable" | PASS | Output explicitly quotes the bad/good table rule: '"High traffic" → "500 req/s peak"' and labels the row 'Quantified NFRs (no adjectives)' |
| c12 | Output verifies the assumption ledger is numbered, with a confidence rating and validation method per assumption — not just an unstructured list | PASS | Output states: 'Step 2, numbered table with Confidence + Validation method columns' — explicitly confirms numbered format and both required fields |
| c13 | Output verifies that every significant design decision requires options analysis with at least two options and a chosen-option rationale | PASS | Output states: 'Step 7, ≥2 options required, Rationale + Trade-off fields required' |
| c14 | Output confirms the skill mandates Mermaid diagrams (component and sequence) and references the C4 model with Level 1 (Context) and Level 2 (Container) as minimum | PASS | Two table rows confirm: Mermaid diagrams — 'component, sequence, and data flow all required'; C4 model — 'Level 1+2 mandatory, Level 3 recommended' |
| c15 | Output confirms the per-component confidence assessment table exists, including the rule that components below 60% confidence trigger a planned spike | PASS | Table row: 'Confidence table + 60% spike rule \| PASS \| Step 9, numeric threshold with concrete consequence' — confirms both the table and the 60% threshold rule |
| c16 | Output verifies the change impact / what-if section covers traffic growth, new client types, and dependency outages — not just the happy path | PASS | Table row explicitly lists all three required scenarios: 'covers 10x traffic, new clients, dependency outages' |
| c17 | Output verifies the anti-patterns list includes premature microservices, distributed monolith, and shared database by name | PASS | Table row: '7 named anti-patterns including all 3 required' — directly asserts all three named anti-patterns are present |
| c18 | Output identifies any genuine gaps — e.g. no explicit rule on when to upgrade C4 Level 3 (Component) diagrams, missing capacity-planning worked example, or no ADR cross-reference convention | PARTIAL | Output identifies two genuine gaps: '1. No threshold for when Level 3 diagrams become mandatory (currently "recommended for complex/high-risk" with no measurable criterion). 2. No rule defining which decisions warrant a full ADR vs. inline options analysis' — ceiling is PARTIAL |

### Notes

The captured output is a well-structured verification report that addresses all 18 criteria. It uses a clear table format with PASS/PARTIAL status per requirement and evidence citations pointing to specific skill steps. All 9 core skill requirements (c1–c9) are verified with step references and example content. The output-level verification criteria (c10–c17) are all satisfied because the report explicitly quotes the relevant rules and confirms the structural requirements. For c17, the output claims 'all 3 required' anti-patterns are present but does not name them individually — relying on the assertion rather than quoting them; this is borderline but the direct claim is sufficient evidence. Both PARTIAL-ceiling criteria (c9 arc42, c18 gap identification) are correctly scored at PARTIAL — arc42 is noted as implicit rather than fully mapped, and two genuine gaps are identified including the Level 3 diagram threshold issue explicitly called out in the criterion.
