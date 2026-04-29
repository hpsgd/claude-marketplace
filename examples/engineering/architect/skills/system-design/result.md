# Output: system-design skill structure

**Verdict:** PARTIAL
**Score:** 17/18 criteria met (94.4%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill explicitly rejects vague non-functional requirements — the NFR table in Step 1 contrasts "Bad answer" ("Fast", "High traffic") with "Good answer" ("p95 < 200ms", "10K concurrent users"), and the Anti-Patterns section repeats the rule verbatim: "Unquantified NFRs — 'fast' and 'scalable' are not requirements. Numbers or it doesn't count."
- [x] PASS: Skill mandates a numbered assumption ledger — Step 2 is labelled "(MANDATORY)" and shows a table with columns `#`, `Assumption`, `Impact if wrong`, `Confidence`, and `Validation method`. Rows use A1/A2/A3 numbering.
- [x] PASS: Skill requires options analysis for every significant design decision — Step 7 is headed "(MANDATORY for key decisions)" and states "For every significant design decision, present at least 2 options," with a worked example table and explicit Rationale and Trade-off acknowledged fields.
- [x] PASS: Skill requires Mermaid diagrams — the Diagrams section is marked "(MANDATORY)" and lists component diagram and sequence diagram as required outputs. The section closes with "Use Mermaid syntax for all diagrams."
- [x] PASS: Skill describes all three C4 model levels (Context, Container, Component) with definitions and states: "Every system design should include at least Level 1 and Level 2 diagrams."
- [x] PASS: Skill requires a confidence assessment table per component (Step 9) with the explicit rule: "Any component with confidence below 60 must have a spike or prototype planned before implementation begins."
- [x] PASS: Skill requires change impact analysis in Step 8, covering all three required scenarios by name: "What if traffic 10x?", "What if a new client type is added?", and "What if a third-party dependency goes down?"
- [x] PASS: Skill lists all three required anti-patterns by name: "Premature microservices", "Distributed monolith", and "Shared database" — the first three entries in the Anti-Patterns section, each with an explanatory sentence.
- [~] PARTIAL: Skill references arc42 in the Output Structure section with a link to arc42.org, and references the template by path (`templates/system-design.md`). The arc42 reference is present; the template reference is a bare path with no instruction on how to locate or use it.

### Output expectations

- [x] PASS: This output is structured as a verification of the skill (PASS/FAIL per requirement), not a sample system design.
- [x] PASS: The skill rejects vague NFRs and the rule requiring numeric thresholds is quoted directly: "Unquantified NFRs — 'fast' and 'scalable' are not requirements. Numbers or it doesn't count." The NFR table illustrates p95 latency, RPS, and concurrent user formats as concrete examples.
- [x] PASS: The assumption ledger is verified as numbered (column `#`), with a `Confidence` column and a `Validation method` column — a structured table, not an unstructured list.
- [x] PASS: Options analysis is verified as mandatory per Step 7, with at least two options required and explicit Rationale and Trade-off fields in the template.
- [x] PASS: The Mermaid diagram mandate is confirmed, and the C4 model section is verified to require Level 1 (Context) and Level 2 (Container) as the explicit minimum.
- [x] PASS: The per-component confidence assessment table is confirmed, including the hard 60% threshold rule that triggers a required spike.
- [x] PASS: The change impact section is verified to cover all three required scenarios: traffic growth (10x), new client types, and dependency outages.
- [x] PASS: The anti-patterns list is verified to include premature microservices, distributed monolith, and shared database by name.
- [~] PARTIAL: Genuine gaps identified. Level 3 (Component) diagrams are "recommended for complex or high-risk containers" but no threshold or rule specifies when that recommendation becomes mandatory — the skill leaves it to judgment with no guard. There is no capacity-planning worked example. The output format includes a "Recommended ADRs" section pointing to `/architect:write-adr`, but no cross-reference convention defines which decision types always warrant an ADR or how to link the ADR back to the design document.

## Notes

Every mandatory element in the skill is explicitly labelled as such — Steps 2 and 7 use "(MANDATORY)", the Diagrams section uses "(MANDATORY)". The confidence threshold of 60 is a hard rule, not a guideline. The arc42 reference and template path are present but the template reference would benefit from an instruction telling agents where to find or load the template.

The Level 3 diagram gap is the most actionable: a simple rule like "Level 3 is required for any container with more than N components or flagged as high-risk in the confidence table" would close the judgment gap without adding complexity.
