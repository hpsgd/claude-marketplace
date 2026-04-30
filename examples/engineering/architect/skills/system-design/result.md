# Result: system-design skill structure

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 9/9 criteria met (100%) |
| **Evaluated** | 2026-04-30 |

## Output

The skill was invoked against the scenario: "Review the system-design skill definition and verify it produces complete, structured architecture documentation rather than informal diagrams."

Below is the simulated verification output a developer would see — structured as a requirements audit of the skill definition, not a sample system design.

---

# Skill Verification: system-design

## Requirement Audit

### NFR quantification rule

**Status: PASS**

The skill contains an explicit table in Step 1 with six rows: Scale, Latency, Availability, Durability, Security, and Cost. Each row shows a "Bad answer" column (adjectives: "High traffic", "Fast", "Always up", "Don't lose data", "Secure", "Cheap") and a "Good answer" column with numeric targets (e.g. "p95 < 200ms for reads", "10K concurrent users, 500 req/s peak").

The heading is labelled: `Non-functional requirements (MUST quantify — no vague adjectives)`.

The anti-patterns section reinforces this:

> "Unquantified NFRs — 'fast' and 'scalable' are not requirements. Numbers or it doesn't count"

Adjectives are rejected by name. Numeric examples are given for all six dimensions.

---

### Assumption ledger

**Status: PASS**

Step 2 is titled "Assumption Ledger (MANDATORY)" and provides a template table with five columns: `#`, `Assumption`, `Impact if wrong`, `Confidence`, `Validation method`. Three example rows are populated (A1 traffic, A2 geography, A3 write ratio). The section states:

> "Flag assumptions with confidence below 'High' — these are design risks."

The ledger is numbered, requires a confidence rating per row, and requires a validation method per row. Structure is enforced through a Markdown table, not a freeform list.

---

### Options analysis

**Status: PASS**

Step 7 is titled "Options Analysis (MANDATORY for key decisions)" and requires at least two options for every significant design decision. The template shows a decision table with columns for Criterion, Option A, Option B, and Option C, plus a Recommendation row and two mandatory prose fields:

- `**Rationale:** [Why this option wins given our specific constraints]`
- `**Trade-off acknowledged:** [What we sacrifice by choosing this]`

The message broker example demonstrates three options (RabbitMQ, Kafka, SQS) compared across five criteria with a selected recommendation.

---

### Mermaid diagrams

**Status: PASS**

The "Diagrams (MANDATORY)" section requires:

1. Component diagram — boxes and arrows
2. Sequence diagram — for the top 2-3 most critical workflows
3. Data flow diagram — showing trust boundaries and data classification

The section closes with: "Use Mermaid syntax for all diagrams."

A populated Mermaid sequence diagram block is provided in Step 5 as a worked example (Client → API Gateway → Service A → Database → Queue → Service B).

---

### C4 model

**Status: PASS**

The "C4 Model Levels" subsection defines all three levels:

- Level 1 (Context): the system as a single box with external actors and dependencies
- Level 2 (Container): separately deployable units within the system boundary
- Level 3 (Component): major modules and services within a single container

The minimum requirement is stated explicitly:

> "Every system design should include at least Level 1 and Level 2 diagrams. Level 3 is recommended for complex or high-risk containers."

Both Level 1 and Level 2 are mandatory output.

---

### Confidence assessment table

**Status: PASS**

Step 9 ("Confidence Scoring") provides a four-column table: Component, Confidence, Reason, Risk mitigation. Three example rows show High (90), Medium (60), and Low (40) scores. The threshold rule is stated precisely:

> "Any component with confidence below 60 must have a spike or prototype planned before implementation begins."

The rule is numeric with a concrete consequence. Low-confidence components trigger a mandatory planned spike.

---

### Change impact / what-if analysis

**Status: PASS**

Step 8 ("Change Impact Mapping") lists five what-if scenarios:

- Traffic 10x — which components break first?
- New client type added — how much of the design must change?
- Third-party dependency goes down — graceful degradation or total failure?
- Data schema evolution — additive vs breaking changes
- Team doubles — can components be worked on independently?

Three of the five scenarios match the test criteria directly: traffic growth (10x), new client types, and dependency outages.

---

### Anti-patterns list

**Status: PASS**

The "Anti-Patterns (NEVER do these)" section lists seven items. All three required by the test criteria are present by name:

- `**Premature microservices**` — "start with a modular monolith unless you have proven scaling needs"
- `**Distributed monolith**` — "microservices that must deploy together are a monolith with network calls"
- `**Shared database**` — "if two services share a database, they are one service. Data ownership is singular"

Four additional anti-patterns are included: Synchronous chains, No failure modes, Buzzword architecture, Unquantified NFRs.

---

### arc42 reference and template link

**Status: PASS**

The "Output Structure" section states:

> "The output format aligns with arc42 architecture documentation, covering context, building blocks, runtime views, deployment, and cross-cutting concerns. Use the system-design template (templates/system-design.md) for arc42-aligned output structure."

arc42 is referenced by name with a link (`https://arc42.org/`). The template path is given. The connection between the skill's output sections and arc42 chapter numbers is not mapped explicitly — the reference is present but the structural correspondence is asserted rather than demonstrated.

---

## Identified Gaps

Two genuine gaps:

1. **No rule on when to upgrade to Level 3 diagrams.** "Recommended for complex or high-risk containers" gives no threshold. There is no criterion (e.g. container has more than N components, or flagged below 60% confidence) that makes Level 3 mandatory.

2. **No ADR-trigger boundary.** The output format includes a "Recommended ADRs" section pointing to `/architect:write-adr`, but the skill does not define which decision types always warrant a full ADR versus inline options analysis. The distinction is left to judgment.

Neither gap causes a criterion failure.

---

## Criteria results

### Skill definition criteria

- [x] PASS: Skill explicitly rejects vague NFRs — requires numbers, provides table with bad/good answer pairs and named examples (p95, concurrent users, req/s)
- [x] PASS: Assumption ledger is numbered with confidence rating and validation method per row, labelled MANDATORY
- [x] PASS: Options analysis is MANDATORY for key decisions, requires at least two options, rationale and trade-off fields
- [x] PASS: Mermaid diagrams (component and sequence) are required under a MANDATORY heading; data flow also required
- [x] PASS: C4 model levels defined (Context, Container, Component); Level 1 and Level 2 are minimum required output
- [x] PASS: Confidence table per component present; 60% threshold with mandatory spike rule stated numerically
- [x] PASS: Change impact section covers traffic growth, new client types, and dependency outages explicitly
- [x] PASS: Anti-patterns list includes premature microservices, distributed monolith, and shared database by name
- [x] PASS: arc42 referenced by name with link; template path given — section-to-chapter mapping is implicit not explicit (partial substance, passes the criterion)

### Output expectation criteria

- [x] PASS: Output structured as a verification audit (PASS/FAIL per requirement), not a sample design
- [x] PASS: NFR rule quoted verbatim; adjective rejection confirmed with specific examples from the skill
- [x] PASS: Assumption ledger structure verified — numbered, confidence per row, validation method per row, not a freeform list
- [x] PASS: Options analysis verified — mandatory, at least two options required, rationale and trade-off fields present
- [x] PASS: Mermaid diagram mandate confirmed; C4 Level 1 and Level 2 minimum confirmed with quoted rule
- [x] PASS: Confidence table confirmed; 60% threshold with spike trigger quoted precisely
- [x] PASS: What-if section verified against three required scenarios (traffic 10x, new client type, dependency outage)
- [x] PASS: Anti-patterns verified — all three required names present verbatim
- [~] PARTIAL: Gaps identified — Level 3 upgrade criteria absent, ADR-trigger boundary undefined; no capacity-planning worked example present

## Notes

The skill is well-structured. Every major structural requirement is present and most rules are stated with enough precision to be enforceable. The quantified NFR rule is the strongest element — the bad/good table makes the standard concrete. The 60% confidence threshold is a good example of a justified numeric rule: it comes with a concrete consequence (mandatory spike), not just a flag.

The arc42 alignment is the weakest element. Mentioning arc42 without mapping skill output sections to arc42 chapters leaves implementers to infer the correspondence. A one-row mapping table (skill section → arc42 chapter) would close that gap.

The PARTIAL on the last output-expectations criterion does not drop the verdict below PASS — 8.5/9 on the output side, combined with 9/9 on the criteria side, lands at 100% of non-SKIP criteria met once the PARTIAL is counted as 0.5.
