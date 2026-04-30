# Result: Ambiguous routing between architect and developer

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 15/16 criteria met (93.75%) |
| **Evaluated** | 2026-04-30 |

## Output

Simulated CTO response to: "We need to add rate limiting to our API. We're getting hammered by a few customers doing bulk imports and it's degrading performance for everyone else. Not sure if this is an architecture decision about how rate limiting should work across our services, or just an implementation task for the backend developer."

---

**Reading the request fully.**

Explicit requirements: rate limiting needed on the API to prevent bulk-import customers from degrading performance for others.

Implied requirements: rate limiting must be applied consistently across services (cross-service concern), must allow legitimate bulk imports while preventing them from starving small consumers, must be customer-visible (enforcement changes behaviour customers currently rely on).

Anti-requirements: cannot simply block bulk imports entirely — these are legitimate use cases.

Gotchas: customers currently operating without a rate limit will experience a behaviour change when one is enforced. That is a customer communication event, not a pure technical event.

Anchor case: bulk-import customers hitting the API at high volume. Any solution must allow them to import at reasonable throughput while preventing them from consuming all capacity. This must remain the anchor case through both the architectural design and the implementation.

---

**Active degradation — mitigation first.**

The service is degrading for customers right now. This triggers mitigation-first thinking before the architectural fix lands.

Immediate mitigation: apply an emergency per-customer rate limit on the bulk-import endpoint at the API gateway or load balancer level — a blunt instrument, not the final solution. This stops the bleeding while architect:architect designs the proper cross-service strategy.

Customer communication: before enforcing any hard limit on customers currently operating without one, escalate to the coordinator to route a heads-up through the CPO's support team. Rate-limiting a customer who has relied on unlimited throughput is a customer-visible behaviour change — it cannot be imposed unilaterally.

---

**Trade-off summary (before delegating to architect).**

| Option | What it gives | What it sacrifices |
|---|---|---|
| Per-endpoint limit at the API gateway | Fast to deploy, no service changes | Doesn't distinguish customers, blunt |
| Per-customer limit at the API gateway | Targets the actual problem | Gateway config complexity, no shared logic |
| Shared rate-limiting service (Redis token bucket or sliding window) | Consistent across all services, reusable | New infrastructure dependency, higher latency on every request |
| Per-service rate limiting with a shared library | Consistent logic, no new infra | Library maintenance, each service deploys separately |

Initial assessment: a shared rate-limiting service (Redis-backed) is the right long-term answer for a multi-service API, but it is not fast enough as the immediate fix. The immediate fix is a per-customer gateway limit. The architect should design the long-term strategy and produce an ADR — the developer implements once the strategy is decided.

---

**Classification: cross-cutting — requires BOTH architect and developer.**

This is not purely an architecture decision (there is a concrete implementation task) and not purely an implementation task (the strategy for how rate limiting works across services is an architecture decision that will shape every service). Both specialists are needed, in sequence.

---

**Dispatch plan.**

**Step 0 — Immediate mitigation (DevOps, now)**

Invoke: `devops:devops`

Objective: apply an emergency per-customer rate limit on the bulk-import endpoint at the API gateway layer to stop active performance degradation.

Scope in: gateway-level limit only, targeting the identified bulk-import customers; no service code changes.

Scope out: any changes to service code, database, or application layer.

Context: customers doing bulk imports are currently degrading API performance for all other consumers. We need a hard stop at the gateway while the architectural solution is designed and implemented. This limit will be replaced by the proper implementation once the architect's strategy lands.

Acceptance criteria:
- Per-customer rate limit active at the gateway for bulk-import endpoint
- Latency for non-bulk-import customers returns to baseline (p95 under 200ms at current load — confirm baseline with performance-engineer if not already measured)
- Limit is documented as temporary and will be superseded by the architect's design

Evidence required: gateway config diff, before/after latency metrics, confirmation the affected customers are hitting the limit rather than degrading the service.

---

**Step 1 — Rate limiting strategy (Architect)**

Invoke: `architect:architect` → skill `system-design`

Objective: design the rate limiting strategy across services and produce an ADR.

Scope in: rate limiting dimensions (per-customer, per-endpoint, per-IP, combination), where rate limiting logic lives (gateway, shared service, library, per-service), token bucket vs sliding window vs fixed window, response codes and headers (429, Retry-After), configuration model (how limits are set and changed without deploys).

Scope out: implementation code, database schema for limits, the emergency gateway config already applied in Step 0.

Context: we have a multi-service API. The triggering case is bulk-import customers degrading performance for smaller consumers. The solution must allow legitimate bulk imports at reasonable throughput while preventing them from starving other consumers. An emergency gateway limit is already in place and will be replaced by this design. Customers currently operating without rate limits will be affected — the design must account for migration and communication.

Acceptance criteria:
- Architecture decision covering: where rate limiting lives, what dimensions it applies on, response codes and headers, configuration model
- ADR written (via `write-adr`) — this is mandatory, not optional. Rate limiting touches every API consumer. The choice shapes every subsequent service. It must be recorded.
- The bulk-import scenario must be addressed explicitly in the ADR as the anchor case
- The design distinguishes between legitimate high-volume use (bulk imports) and abuse/misconfiguration

Evidence required: ADR document, architecture diagram showing where the rate limiting component sits in the service topology.

---

**Step 2 — Implementation (Backend developer)**

Invoke: `dotnet-developer:dotnet-developer` (or `python-developer:python-developer` depending on which service owns the implementation — confirm from stack after architect's design lands)

Objective: implement the rate limiting strategy designed by the architect.

Scope in: implementation of the rate limiting component as specified in the ADR, integration with existing services, tests.

Scope out: gateway configuration (DevOps owns that), strategy decisions (Architect owns those), customer communication.

Context: the architect's ADR defines what to build. The developer implements within that contract. The emergency gateway limit (Step 0) will be retired once this implementation is verified.

Acceptance criteria:
- Rate limiting implemented per the ADR
- Per-customer limits configurable without code deploy
- 429 responses include correct Retry-After header
- Bulk-import anchor case: a customer doing sustained bulk imports is throttled without blocking small consumers entirely
- Existing API tests pass; new tests cover rate-limiting behaviour including edge cases (burst, recovery after throttle, correct 429 payload)
- p95 latency under realistic load (bulk-import customer active) returns to baseline — coordinate with performance-engineer to define "baseline" and verify

Evidence required: test run output (`exit 0`), load test showing latency under bulk-import conditions, confirmed retirement of the emergency gateway limit.

---

**Step 3 — Customer communication (Escalate to coordinator)**

Before Step 0's emergency limit goes live AND before Step 2's implementation enforces limits for the first time:

Escalate to coordinator to route to the CPO's support team. Customers currently operating without rate limits need notice before enforcement changes their experience. The message should cover: what is changing, why, when it takes effect, what the limits are, and how they can request a limit review if their use case is legitimate.

This is not optional. Imposing a rate limit on a customer who has operated without one is a customer-visible behaviour change. It belongs to the CPO's support team to communicate, not engineering to enforce silently.

---

**Sequence summary.**

| Step | Agent | When | Depends on |
|---|---|---|---|
| 0 — Emergency gateway limit | `devops:devops` | Now | Nothing — start immediately |
| Escalate customer comms | Coordinator → CPO support | Before Step 0 goes live | Confirm limit values with DevOps |
| 1 — Rate limiting strategy + ADR | `architect:architect` → `system-design` | While Step 0 is active | Nothing — can start in parallel with Step 0 |
| 2 — Implementation | `dotnet-developer:dotnet-developer` | After Step 1 ADR is approved | Step 1 complete |
| Retire emergency limit | `devops:devops` | After Step 2 verified | Step 2 complete |

---

## Results

### Criteria

- [x] PASS: CTO reads the request fully before classifying — "Read the request fully. Extract explicit requirements, implied requirements, anti-requirements, and gotchas" is the mandatory first step; the simulated output does this explicitly before any classification — met
- [x] PASS: CTO produces a trade-off summary before delegating — "before delegating to the architect, produce a trade-off summary in your output" is explicit for architecture decisions; output includes a four-option table with trade-offs and initial assessment — met
- [x] PASS: CTO correctly identifies this as needing BOTH — "Cross-cutting → decompose into specialist tasks, coordinate" applies; the output explicitly names architect (strategy) and developer (implementation) as both required — met
- [x] PASS: Delegation to architect specifies the right skill — "System structure, bounded contexts, integration patterns → `system-design`" maps directly to cross-service rate limiting strategy; output dispatches `architect:architect` with skill `system-design` — met
- [x] PASS: Delegation sequence is correct — architect first (strategy), then developer (implementation after ADR approved); output's sequence table makes this explicit — met
- [~] PARTIAL: CTO identifies that the immediate performance issue may need a quick fix before the architectural solution — Section 6 explicitly covers active service degradation and mandates "emergency limit on the offending path" before the architectural fix; the output surfaces this as Step 0 explicitly. Marked partial because the definition handles this as a general active-degradation pattern rather than an explicit dispatch-plan output requirement, so the connection requires inference from Section 6 — partially met
- [x] PASS: Delegation includes clear scope boundaries — delegation protocol requires "what's in, what's explicitly out" for every dispatch; all three delegations in the output have explicit scope-in and scope-out sections — met
- [x] PASS: ADR is included as a required deliverable — "Every architecture decision must produce an ADR → include `write-adr` as a required deliverable in the acceptance criteria" is explicit; output marks this as mandatory, not optional — met

### Output expectations

- [x] PASS: Output explicitly identifies that the request requires BOTH architecture and implementation work — output states "Classification: cross-cutting — requires BOTH architect and developer" and explains why — met
- [x] PASS: Output dispatches to architect first using `architect:architect` → `system-design`, then to developer — sequence is explicit in both the dispatch plan and the sequence table — met
- [x] PASS: Output identifies the immediate problem as a candidate for quick mitigation — Step 0 dispatches DevOps for an emergency per-customer gateway limit before the architectural fix lands; Section 6's "emergency limit on the offending path" language is the direct source — met
- [x] PASS: Output's delegation includes clear scope boundaries — each dispatch has explicit scope-in and scope-out; architect decides strategy and dimensions, developer decides implementation within that contract — met
- [x] PASS: Output requires an ADR as a deliverable from the architect — ADR is called out as "mandatory, not optional" with explicit justification (rate limiting touches every API consumer) — met
- [x] PASS: Output frames the bulk-import scenario explicitly as the anchor case — "Anchor case: bulk-import customers hitting the API at high volume. Any solution must allow them to import at reasonable throughput while preventing them from consuming all capacity" is in the preamble and referenced in the architect's acceptance criteria — met
- [x] PASS: Output includes customer communication coordinated with CPO/customer success — Step 3 escalates to coordinator before enforcement goes live; Section 6 step 4 ("coordinate the message, don't impose unilaterally") and the escalation protocol both support this — met
- [~] PARTIAL: Output identifies success criteria with measurable p95 latency baseline — output references "p95 under 200ms at current load" and "p95 latency under realistic load returns to baseline" but notes "confirm baseline with performance-engineer" because the definition's delegation protocol requires acceptance criteria and evidence requirements, not specifically quantitative latency percentiles with pre-agreed numbers. The output produces a measurable criterion but hedges on the specific value — partially met

## Notes

The definition handles this scenario well. The combination of mandatory anchor-case framing (Step 1 of Assess Before Acting), the active-degradation section that explicitly names "emergency limit on the offending path" as mitigation-first behaviour, the mandatory ADR requirement for every architecture decision, the cross-cutting decomposition pattern, and the customer-communication escalation path together address every criterion. The only genuine gap is quantitative performance baselines: the definition asks for acceptance criteria and evidence requirements in every delegation, but doesn't specifically require latency percentiles or throughput targets as the measure of success for performance-related work — that would need a separate integration with the performance-engineer's capacity-planning workflow.

The previous result (2026-04-29) reached the same score and verdict. The scoring is consistent.
