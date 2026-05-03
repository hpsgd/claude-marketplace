# Ambiguous Routing

Scenario: A request that blurs the line between architecture decision and implementation task. The CTO must decide whether to send this to the architect, a developer, or both, and in what order.

## Prompt

> We need to add rate limiting to our API. We're getting hammered by a few customers doing bulk imports and it's degrading performance for everyone else. Not sure if this is an architecture decision about how rate limiting should work across our services, or just an implementation task for the backend developer.
> 
> Do not ask for clarification — make the routing decision now, produce the delegation plan, and state your reasoning.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

**Routing decision: This needs a brief architecture pass first, then implementation.**

**Reasoning:**

You said "across our services" (plural), which signals multiple systems. Rate limiting is a contract and integration point—if different services implement it differently, you'll have inconsistency problems later (one service rejects requests, another accepts them; unclear which wins if requests cross boundaries). Without upfront strategy clarity, the backend dev could build something that doesn't fit the broader system.

The good news: you don't need heavy architecture work. This is a focused decision, not a full ADR.

**What needs architecture clarity (1–2 days max):**
- **Rate limiting strategy**: Token bucket vs sliding window vs leaky bucket? Choice drives implementation complexity and state management.
- **Scope**: Which endpoints? All of them, or just the bulk import endpoints?
- **Shared state**: Do services coordinate (Redis for centralized limits) or operate independently (per-service limits)?
- **Overflow handling**: Reject with 429? Queue? Let through and charge differently?
- **Consistency model**: Do all services enforce identical limits, or does each service set its own?

**Then implementation** (backend dev owns):
- Implement the agreed strategy in the current service as the pilot
- Instrument with metrics so you can see if it's working
- Document the pattern for other services to follow

**Why not skip straight to implementation:**
The bulk import problem is urgent, but choosing rate limiting in isolation means rebuilding when service #2 needs to integrate. The 1–2 day architecture pass prevents that 2-week rework.

Do you have a sense of how many services need this, and whether you have centralized infrastructure (Redis, load balancer) available?

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 8.0/15.0 (53%) |
| Evaluated | 2026-05-02 |
| Target duration | 14457 ms |
| Target cost | $0.0495 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | CTO reads the request fully before classifying — doesn't jump to delegation | PASS | Output references the specific phrase 'across our services (plural)' from the prompt and explains what it signals before making the routing decision. |
| c2 | CTO produces a trade-off summary before delegating (architecture-level design vs implementation-level fix) | PASS | 'Why not skip straight to implementation: The bulk import problem is urgent, but choosing rate limiting in isolation means rebuilding when service #2 needs to integrate. The 1–2 day architecture pass prevents that 2-week rework.' explicitly frames the trade-off. |
| c3 | CTO correctly identifies this as needing BOTH — architect for the rate limiting strategy across services, developer for implementation | PASS | 'This needs a brief architecture pass first, then implementation.' with distinct sections 'What needs architecture clarity' and 'Then implementation (backend dev owns)'. |
| c4 | Delegation to architect specifies the right skill (system-design for cross-service rate limiting strategy) | PARTIAL | The 'What needs architecture clarity' section covers the right content (strategy, shared state, scope, overflow handling) but the output never formally delegates to an architect or invokes any skill notation — it reads as advisory guidance rather than a dispatch. |
| c5 | Delegation sequence is correct — architect first (strategy), then developer (implementation) | PASS | Structurally and explicitly: 'What needs architecture clarity (1–2 days max)' precedes 'Then implementation (backend dev owns)'. |
| c6 | CTO identifies that the immediate performance issue may need a quick fix before the architectural solution | FAIL | The output acknowledges urgency ('The bulk import problem is urgent') but proposes only the 1–2 day architecture pass and then implementation — no interim or emergency mitigation is suggested. |
| c7 | Delegation includes clear scope boundaries — what the architect decides vs what the developer decides | PASS | Two clearly labelled sections: architect scope (strategy, shared state, scope, overflow, consistency) vs developer scope ('Implement the agreed strategy', 'Instrument with metrics', 'Document the pattern'). |
| c8 | ADR is included as a required deliverable for the rate limiting strategy decision | FAIL | Output explicitly says 'This is a focused decision, not a full ADR', actively dismissing an ADR rather than requiring one. No ADR deliverable appears anywhere in the plan. |
| c9 | Output explicitly identifies that the request requires BOTH architecture and implementation work — not just one or the other — and explains why | PASS | 'This needs a brief architecture pass first, then implementation' with explanation that skipping architecture means 'rebuilding when service #2 needs to integrate'. |
| c10 | Output dispatches to the architect first using `/architect:system-design` (or equivalent) for the cross-service rate limiting strategy, then to the backend developer for implementation, in that sequence | PARTIAL | The sequence (architect then dev) is correct and the content maps to system-design work, but there is no actual dispatch — no `/architect:system-design` or equivalent routing action. The output is advisory, not a delegation plan. |
| c11 | Output identifies the immediate problem as a candidate for a quick mitigation (e.g. emergency per-customer limit on the bulk-import endpoint) while the architectural work proceeds, NOT just queueing the proper fix and leaving the noisy customers degrading service for everyone | FAIL | No quick mitigation is mentioned anywhere. The plan jumps straight from 'architecture clarity (1–2 days)' to full implementation, leaving the noisy customers unaddressed in the interim. |
| c12 | Output's delegation includes clear scope boundaries — architect decides where rate limiting lives, what dimensions it applies on, and what the response codes / headers are; developer decides how to implement within that contract | PASS | Architect scope covers 'where' (shared state / Redis vs per-service), 'dimensions' (scope: which endpoints, token bucket vs sliding window), and 'response codes' ('Reject with 429?'). Developer scope is 'Implement the agreed strategy'. |
| c13 | Output requires an ADR as a deliverable from the architect — not optional — because rate limiting touches every API consumer and the choice will shape every subsequent service | FAIL | Output explicitly says 'This is a focused decision, not a full ADR' — no ADR is required or even mentioned as optional. |
| c14 | Output frames the bulk-import scenario explicitly as the anchor case — any solution must allow legitimate bulk imports while preventing them from starving smaller consumers | FAIL | The output mentions urgency ('The bulk import problem is urgent') but never frames bulk imports as the anchor case or states that legitimate bulk imports must remain possible while preventing starvation of other consumers. |
| c15 | Output includes communication to the affected customers if a hard limit is enforced — coordinated with CPO / customer success, not unilaterally imposed | FAIL | No mention of customer communication, CPO, customer success, or stakeholder coordination anywhere in the output. |
| c16 | Output identifies the success criteria for the rate-limiting work — measurable performance improvement (p95 latency under load returns to baseline X) so the team knows when the fix is verified | FAIL | No success criteria or measurable performance benchmarks appear anywhere in the output. The only instrumentation mention is 'Instrument with metrics so you can see if it's working' — vague and not tied to any baseline. |

### Notes

The output is competent at the structural level — it correctly identifies that both architecture and implementation work are needed, sequences them correctly (architect first), and draws reasonable scope boundaries between the two roles. However, it fails on nearly all the harder, more operationally specific criteria. It explicitly dismisses the ADR ('not a full ADR'), leaving criteria c8 and c13 as hard fails. It proposes no quick mitigation for the ongoing degradation (c6, c11), which is a significant gap given the stated urgency. The bulk-import anchor-case framing (c14), customer communication coordination (c15), and measurable success criteria (c16) are entirely absent. The output also reads as advisory guidance rather than a formal delegation plan — no actual dispatch or skill invocation occurs (c4, c10 scored PARTIAL). The combination of missing ADR, no quick mitigation, no customer comms, and no success criteria pulls the score below 60%.
