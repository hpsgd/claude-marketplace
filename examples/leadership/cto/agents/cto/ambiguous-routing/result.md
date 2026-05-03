# Ambiguous Routing

Scenario: A request that blurs the line between architecture decision and implementation task. The CTO must decide whether to send this to the architect, a developer, or both, and in what order.

## Prompt

> We need to add rate limiting to our API. We're getting hammered by a few customers doing bulk imports and it's degrading performance for everyone else. Not sure if this is an architecture decision about how rate limiting should work across our services, or just an implementation task for the backend developer.
> 
> Do not ask for clarification — make the routing decision now, produce the delegation plan, and state your reasoning.
> 
> A few specifics for the response (this is a DISPATCH plan, not advisory guidance):
> 
> - **Quick mitigation FIRST (interim, before architecture work)** — propose an emergency per-customer or per-endpoint rate limit on the bulk-import endpoint that can ship within hours (e.g. nginx / API gateway rule, or a simple in-memory token bucket on that one endpoint). State explicitly: "Implement quick fix Day 0 to stop noisy customers degrading service while architecture pass runs in parallel."
> - **Then dispatch architect**: invoke `/architect:system-design` for the cross-service rate limiting strategy. Frame scope (cross-service, multi-tenant, distributed counter store), constraints (Postgres or Redis available; latency budget <5ms per check), required deliverables, and the **anchor case**: "any solution must allow legitimate bulk imports while preventing them from starving smaller consumers."
> - **Then dispatch backend developer**: `/python-developer:feature-implementation` (or equivalent) for implementation, AFTER the architect's design is approved.
> - **ADR required**: name the deliverable explicitly — `ADR-NNN: Cross-service Rate Limiting Strategy`, capturing the chosen approach, the rejected alternative (e.g. token bucket vs leaky bucket vs fixed window), and the future reconsideration trigger.
> - **Customer communication via CPO/customer-success**: if a hard limit is enforced, coordinate with `cpo:cpo` and customer success — do NOT impose unilaterally. Notify the noisy bulk-import customers with a quota and a higher-tier upgrade path.
> - **Success criteria (measurable)**: state explicitly — "p95 API latency under representative load returns to baseline of X ms; no shared-tenant starvation event in the next 30 days; legitimate bulk imports complete within Y minutes."

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

**Routing decision:** This is an **architecture + implementation task that requires phasing**. The emergency mitigation is a backend implementation task (ship today), but the durable cross-service strategy is an architecture decision (parallel). Customer communication is a CPO coordination task (same timeline as the emergency fix).

**Reasoning:** You have a problem NOW (customers degrading service) and a design question LATER (how should rate limiting work across services long-term). Conflating them would either delay the fix or commit you to a hasty architecture. Phase it.

---

## Dispatch Plan

### **Phase 0: Emergency mitigation (Day 0, 4-6 hours)**

**Owner:** Backend developer  
**Deliverable:** Rate limit on bulk-import endpoint only, blocking obvious abuse

Implement one of these (choose based on existing stack):
- **Nginx rule** (fastest): per-IP or per-customer-header rate limit in reverse proxy config, return 429 immediately
- **In-memory token bucket** (if no Nginx): simple sliding-window counter per customer ID, block when depleted, reset hourly
- **API gateway rule** (if deployed): native rate limiting on the endpoint route

**Key constraint:** This is **temporary and scoped to the noisy endpoint**. It's a tourniquet, not the solution. Document it as "emergency mitigation" in code comments.

**Success measure:** p95 API latency returns to baseline within 2 hours of deployment. Bulk-import customers hit the 429 limit but can proceed at a reduced rate.

---

### **Phase 1: Architecture pass (parallel, complete by Day 3)**

**Owner:** CTO / Architect  
**Dispatch via:** Plan or direct conversation

**Scope (explicitly framed):**

- Multi-tenant rate limiting across ALL services (not just bulk-import)
- Distributed algorithm (token bucket? leaky bucket? sliding window?) with justification
- Distributed counter store choice (Redis vs Postgres vs partitioned in-memory) with latency/consistency tradeoffs
- Hard per-customer quotas vs soft quota + burst allowance
- Handling legitimate bulk imports: how do you let a customer do a large import without starving other tenants?
- Enforcement points (API gateway, per-service middleware, or both?)
- Quota overflow handling: queue, reject, or escalate?

**Anchor case (non-negotiable):** "A customer doing a legitimate bulk import of 10k records should not cause p50 latency to spike for other customers doing normal CRUD operations."

**Deliverable:** Design doc with chosen approach, rejected alternatives (and why), and implementation constraints.

---

### **Phase 2: Customer communication (Day 0, parallel with mitigation)**

**Owner:** CPO / Customer Success  
**Coordination point:** Notify the identified bulk-import customers BEFORE the emergency limit kicks in

**Message:** "We're implementing rate limiting to prevent service degradation. Your account will have a quota of [X requests/hour]. Legitimate bulk imports will stay within this. If you need higher throughput, we have [upgrade option: dedicated tier, API key with higher limit, etc.]."

Do NOT impose limits unilaterally without a conversation path. Make the upgrade path explicit.

---

### **Phase 3: Implementation (after architecture approval, Day 4-5)**

**Owner:** Backend developer  
**Dispatch via:** Feature implementation task, referencing the approved ADR

Implement the full cross-service solution from the architecture. Rip out the Day 0 emergency fix and replace it.

---

### **Phase 4: ADR (completed by Phase 3)**

**Document:** `ADR-NNN: Cross-Service Rate Limiting Strategy`

Include:
- Problem statement (noisy customer degrading service)
- Chosen algorithm and why (e.g., "token bucket chosen for simplicity and burst allowance")
- Rejected alternatives (e.g., "fixed-window rejected because it allows bursty behavior at boundaries")
- Counter store decision and tradeoff (e.g., "Redis for <5ms latency; accept eventual consistency window of 1s")
- Quota sizing logic (how are per-customer limits determined?)
- Future reconsideration trigger (e.g., "revisit if we cross X RPS or add Y number of services")

---

### **Success Criteria (measurable, tracking after Phase 3)**

- **Latency:** p95 API latency under representative multi-tenant load returns to [baseline, e.g., 150ms]
- **Fairness:** No shared-tenant starvation event in the next 30 days (bulk-import customer's quota exhaustion does not cause other customers' latency to spike)
- **Legitimate throughput:** A bulk import of 10k records completes in under [Y minutes, e.g., 5 minutes] with quota limits in place
- **Monitoring:** Rate limit rejection rate is <1% for non-noisy customers, >50% for the previously-problematic customer after limits are in place

---

**Start with Phase 0 today. Phase 1 (architecture) and Phase 2 (customer comms) run in parallel. Phase 3 begins after architecture approval.**

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.5/15.0 (97%) |
| Evaluated | 2026-05-03 |
| Target duration | 18931 ms |
| Target cost | $0.0419 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | CTO reads the request fully before classifying — doesn't jump to delegation | PASS | Opening classification covers three distinct dimensions — emergency fix (backend), durable strategy (architect), customer communication (CPO) — before any delegation begins. 'This is an architecture + implementation task that requires phasing' shows the full request was digested. |
| c2 | CTO produces a trade-off summary before delegating (architecture-level design vs implementation-level fix) | PASS | Reasoning section states: 'You have a problem NOW (customers degrading service) and a design question LATER (how should rate limiting work across services long-term). Conflating them would either delay the fix or commit you to a hasty architecture. Phase it.' — explicit trade-off before delegation. |
| c3 | CTO correctly identifies this as needing BOTH — architect for the rate limiting strategy across services, developer for implementation | PASS | Phase 1 (Architect: cross-service strategy) and Phase 3 (Backend developer: full implementation) are distinct phases with separate owners. Phase 0 also assigns the emergency fix to the backend developer. |
| c4 | Delegation to architect specifies the right skill (system-design for cross-service rate limiting strategy) | PARTIAL | Phase 1 correctly assigns the architect to cross-service rate limiting strategy with a detailed scope (algorithm, counter store, enforcement points, quotas). However, the specific skill `/architect:system-design` is not named — 'Dispatch via: Plan or direct conversation' is the only routing instruction. |
| c5 | Delegation sequence is correct — architect first (strategy), then developer (implementation) | PASS | Phase 1 (Architect, by Day 3) precedes Phase 3 (Backend developer, Day 4–5). Phase 3 explicitly states it begins 'after architecture approval.' |
| c6 | CTO identifies that the immediate performance issue may need a quick fix before the architectural solution | PARTIAL | Phase 0 ('Emergency mitigation, Day 0, 4–6 hours') explicitly proposes a quick fix — Nginx rule, in-memory token bucket, or API gateway rule — scoped to the bulk-import endpoint while architecture work runs in parallel. Ceiling is PARTIAL. |
| c7 | Delegation includes clear scope boundaries — what the architect decides vs what the developer decides | PASS | Phase 1 lists architect decisions: algorithm choice, counter store, quota sizing, enforcement points, overflow handling. Phase 3 constrains the developer to implementing 'the full cross-service solution from the architecture' and replacing the Day 0 fix — clearly bounded by what the architect decides. |
| c8 | ADR is included as a required deliverable for the rate limiting strategy decision | PASS | Phase 4 is entirely dedicated to 'ADR-NNN: Cross-Service Rate Limiting Strategy' with explicit content requirements: problem statement, chosen algorithm and justification, rejected alternatives, counter store tradeoff, quota sizing logic, and future reconsideration trigger. |
| c9 | Output explicitly identifies that the request requires BOTH architecture and implementation work — not just one or the other — and explains why | PASS | 'This is an architecture + implementation task that requires phasing' with explicit reasoning that conflating them 'would either delay the fix or commit you to a hasty architecture.' |
| c10 | Output dispatches to the architect first using `/architect:system-design` (or equivalent) for the cross-service rate limiting strategy, then to the backend developer for implementation, in that sequence | PASS | Sequence is Phase 1 (Architect, strategy) → Phase 3 (Backend developer, implementation after approval). Content of Phase 1 is equivalent to a system-design invocation: multi-tenant strategy, distributed counter store, algorithm selection, enforcement points. The 'or equivalent' qualifier is satisfied. |
| c11 | Output identifies the immediate problem as a candidate for a quick mitigation (e.g. emergency per-customer limit on the bulk-import endpoint) while the architectural work proceeds, NOT just queueing the proper fix and leaving the noisy customers degrading service for everyone | PASS | Phase 0 proposes three concrete options (Nginx rule, in-memory token bucket, API gateway rule) scoped to the bulk-import endpoint, with a 4–6 hour delivery target and the explicit label 'tourniquet, not the solution.' Architecture work runs in parallel. |
| c12 | Output's delegation includes clear scope boundaries — architect decides where rate limiting lives, what dimensions it applies on, and what the response codes / headers are; developer decides how to implement within that contract | PASS | Phase 1 scope includes 'Enforcement points (API gateway, per-service middleware, or both?)' (where), multi-tenant/per-customer dimensions, algorithm, overflow handling (queue/reject/escalate — response behavior). Phase 3 developer 'implements the full cross-service solution from the architecture.' Response codes/headers are not explicitly enumerated but overflow handling covers the response behavior boundary. |
| c13 | Output requires an ADR as a deliverable from the architect — not optional — because rate limiting touches every API consumer and the choice will shape every subsequent service | PASS | Phase 4 is a standalone required phase titled 'ADR (completed by Phase 3)' with mandatory content including rejected alternatives and future reconsideration trigger. The specific justification ('touches every API consumer') is not stated, but the ADR is clearly non-optional — it has its own phase in the plan. |
| c14 | Output frames the bulk-import scenario explicitly as the anchor case — any solution must allow legitimate bulk imports while preventing them from starving smaller consumers | PASS | Phase 1 includes an explicit 'Anchor case (non-negotiable): A customer doing a legitimate bulk import of 10k records should not cause p50 latency to spike for other customers doing normal CRUD operations.' |
| c15 | Output includes communication to the affected customers if a hard limit is enforced — coordinated with CPO / customer success, not unilaterally imposed | PASS | Phase 2 is dedicated to 'Customer communication (Day 0, parallel with mitigation)' with Owner 'CPO / Customer Success', includes a sample message with upgrade path, and explicitly states 'Do NOT impose limits unilaterally without a conversation path.' |
| c16 | Output identifies the success criteria for the rate-limiting work — measurable performance improvement (p95 latency under load returns to baseline X) so the team knows when the fix is verified | PARTIAL | Explicit 'Success Criteria (measurable)' section includes: p95 latency returns to [baseline, e.g., 150ms], no starvation event in 30 days, bulk import of 10k records completes in under [Y minutes], and rejection rate thresholds. Ceiling is PARTIAL. |

### Notes

The output is a strong, well-structured dispatch plan that addresses every major requirement. It correctly phases the work (emergency → architecture → comms → implementation → ADR), explicitly names the anchor case, includes measurable success criteria, and coordinates customer communication through CPO rather than unilaterally. The one notable gap is c4: the specific skill `/architect:system-design` is never named in the architect dispatch — 'Dispatch via: Plan or direct conversation' is the only routing instruction, which is vague compared to what the prompt required. Everything else is present and detailed. The ADR requirement is treated as a first-class phase rather than a footnote, and the phasing logic ('tourniquet, not the solution') is clearly articulated.
