# Ambiguous routing between architect and developer

**Scenario:** A request that blurs the line between architecture decision and implementation task. The CTO must decide whether to send this to the architect, a developer, or both, and in what order.

> We need to add rate limiting to our API. We're getting hammered by a few customers doing bulk imports and it's degrading performance for everyone else. Not sure if this is an architecture decision about how rate limiting should work across our services, or just an implementation task for the backend developer.

Routed to the CTO, which classifies work before delegating and must produce a trade-off summary before routing to the architect.

## Output

**CTO assessment — rate limiting request**

Reading the full request: bulk import customers are degrading API performance for all other customers. The question is whether this is an architecture decision (how rate limiting works across services) or an implementation task. Answer: both, in sequence.

**Trade-off summary**

Option A — Quick implementation fix (developer first): apply a basic per-customer rate limit at the API gateway or middleware level for the dotnet backend. Fast to ship. Risk: if rate limiting logic needs to work across multiple services, a per-service implementation creates inconsistency and we'll need to redo this.

Option B — Architecture-first: design a consistent rate limiting strategy across services before touching code. Slower to start. Benefit: we ship the right thing once. Given the request mentions "across our services," this is the correct framing.

Assessment: this is cross-cutting (multiple services), so it's an architecture decision first, then implementation. The architect defines the strategy; the dotnet-developer implements it.

**Dispatch plan**

Step 1 — Architect (system-design):
- Objective: design a rate limiting strategy for the API layer that works consistently across services
- Scope IN: rate limiting approach (token bucket / sliding window / fixed window), where enforcement sits (gateway vs middleware vs service-level), how limits are configured per customer tier
- Scope OUT: implementation code, the specific dotnet middleware — that's the developer's job
- Required deliverable: ADR documenting the decision, rationale, and discarded options
- Acceptance criteria: strategy covers multi-service consistency, handles bulk import use case explicitly, includes configuration model

Step 2 — Dotnet-developer (after architect delivers ADR):
- Objective: implement the rate limiting strategy defined in the ADR
- Scope IN: implementing the chosen approach in the .NET backend, tests, Wolverine handler changes if needed
- Scope OUT: strategy decisions — follow the ADR
- Dependencies: ADR from architect must be complete before implementation starts

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 7.5/8 (94%) | 2026-04-16 |

- [x] PASS: CTO reads the request fully before classifying — the "Assess Before Acting" section mandates "Read the request fully. Extract explicit requirements, implied requirements, anti-requirements, and gotchas" as Step 1 before any classification
- [x] PASS: CTO produces a trade-off summary before delegating — the definition explicitly states "before delegating to the architect, produce a trade-off summary in your output: what options exist, what each sacrifices, and your initial assessment"
- [x] PASS: CTO correctly identifies this as needing BOTH — the "Cross-cutting" classification in Step 2 says "decompose into specialist tasks, coordinate"; rate limiting across services fits this category; the team table maps architect to system design and dotnet-developer to backend implementation
- [x] PASS: Delegation to architect specifies the right skill — the definition's team table maps "System structure, bounded contexts, integration patterns → `system-design`" to the architect, which is the correct skill for cross-service rate limiting strategy
- [x] PASS: Delegation sequence is correct — architecture before implementation is explicit in the classification workflow; the dependency between architect ADR and developer implementation is required in the dispatch plan
- [~] PARTIAL: CTO identifies that the immediate performance issue may need a quick fix before the architectural solution — the "Surgical fixes" principle and the incident response "mitigate before investigate" guidance support this recognition, but the workflow for non-incident performance degradation does not explicitly require a quick-fix consideration before routing to the architect. The framework supports it; the definition doesn't require it for this routing path. Score: 0.5
- [x] PASS: Delegation includes clear scope boundaries — the Delegation Protocol explicitly requires "Define the scope — what's in, what's explicitly out" for every delegation
- [x] PASS: ADR is a required deliverable — the definition states "Every architecture decision must produce an ADR → include `write-adr` as a required deliverable in the acceptance criteria"

## Notes

The definition is strong on the architecture-first classification path and the ADR requirement. The one genuine gap is that performance degradation that isn't formally declared an incident doesn't have an explicit "consider a quick fix first" prompt outside the incident response section. In practice, "getting hammered" implies some service impact happening now — the CTO definition would benefit from a note in the classification flow about whether immediate mitigation is warranted before dispatching for architectural resolution.
