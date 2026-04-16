# Technical decision

**Scenario:** A user asks the CTO to make a significant architectural decision about system design. Does the CTO assess the context, delegate to the architect appropriately, apply the right decision criteria, and avoid making product-scope decisions?

> We're building Vaultly — a SaaS document management platform for small law firms. We're about to start the backend and need to decide: do we go with a monolithic Django Ninja application or break it into microservices (one for document storage, one for search, one for access control)? We have a team of three backend devs and expect maybe 50 law firm clients in year one, growing to 500 in year three. What's your recommendation?

Routed to the CTO, which must perform pre-flight, produce a trade-off summary, delegate to the architect with clear scope, and identify the vendor lock-in escalation gate.

## Output

**Pre-flight:** Reading CLAUDE.md and .claude/CLAUDE.md... Reading installed rules in `.claude/rules/`... Reading `.claude-plugin/marketplace.json` — architect agent available. Technology stack: Python/Django Ninja confirmed. No existing ADRs found (greenfield). No active incidents or flagged technical debt.

This is an architecture decision. Before delegating to the architect, here is my trade-off summary.

**Trade-off summary**

Monolith (Django Ninja, single deployable):
- Simple to operate — one process, one database, one deployment pipeline
- Natural fit for a 3-person team: no inter-service networking, no distributed tracing, no independent release cycles to manage
- Year-one scale (50 clients, document SaaS) is well within single-server capacity
- Reversibility: module boundaries can be established now; splitting later is painful but possible
- Risk: over time, without enforced seams, code can become entangled

Microservices (separate storage, search, access control services):
- Independent deployability and scaling per domain
- Operational overhead is real and immediate: service discovery, network latency, distributed tracing, multiple deployment pipelines
- 3-person team will spend significant time on plumbing rather than product
- Premature for year-one scale — adds complexity before there is evidence it is needed
- Risk: distributed systems failure modes (partial outages, data consistency) require more defensive engineering

My initial assessment: the monolith is the right choice for this context. Team size and year-one scale do not justify the operational overhead of microservices. Module seams inside the monolith (storage, search, access control as separate Django apps) protect reversibility without the cost. This aligns with "simple until proven otherwise."

**Work classification:** Architecture decision → delegate to architect via `system-design` skill.

**Dispatch plan**

Step 1 — Architect (system-design): evaluate monolith vs. microservices for Vaultly backend (Python, Django Ninja), with context: 3 backend devs, year-one 50 clients, year-three 500 clients, functional domains are document storage, full-text/metadata search, and access control. Apply "simple until proven otherwise." Acceptance criteria: explicit trade-offs for this context, a recommendation, and module seam documentation if monolith is recommended. Required deliverable: ADR using `write-adr` — this is mandatory.

Step 2 — Escalation gate for vendor lock-in: if the architect's recommendation involves significant infrastructure lock-in (e.g. a managed search service that makes provider switching expensive), stop and escalate to the coordinator before committing. Lock-in decisions on core infrastructure are in the Decision Checkpoints table.

Step 3 — ADR review: once the architect produces the ADR, review it before approving. The recommendation must account for team size and year-one scale — not just architectural preference.

What this is not: I am not deciding which features to build, in what order, or what a law firm client's usage profile looks like in detail. Those are product questions. Once architecture is confirmed, infrastructure decisions go to DevOps.

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 8/8 (100%) | 2026-04-16 |

- [x] PASS: Performs pre-flight — the Pre-Flight (MANDATORY) section requires reading CLAUDE.md, `.claude/CLAUDE.md`, and `.claude/rules/`; then reading marketplace.json, reviewing the technology stack, checking for existing ADRs, and identifying active technical debt; all four checks are required by name
- [x] PASS: Delegates to architect with scope, constraints, and context — the definition classifies "System structure, bounded contexts, integration patterns → `system-design`" under architect delegation; the Delegation Protocol mandates five elements (objective, scope, context, acceptance criteria, evidence requirements); the dispatch framing covers all five
- [x] PASS: Does not simply pick an option without analysis — the definition's architecture decision path explicitly requires "produce a trade-off summary in your output: what options exist, what each sacrifices, and your initial assessment" before delegating; this is a mandatory step
- [x] PASS: Applies "simple until proven otherwise" — the Principles section explicitly states "Simple until proven otherwise. Add complexity only when you have evidence it's needed"; team size (3 devs) and year-one scale (50 clients) are directly cited as the basis for the assessment
- [x] PASS: Produces a dispatch plan rather than implementing directly — the Capability Constraint section explicitly states the CTO "produce[s] a dispatch plan listing which engineering agents to invoke, in what order, with what context"; "What You Don't Do" prohibits direct implementation
- [x] PASS: Escalation path for vendor lock-in — the Decision Checkpoints table lists "Choosing a technology that creates significant vendor lock-in → escalate to coordinator" as a STOP trigger; named and enforced in the definition
- [~] PARTIAL: References need for an ADR — the definition states "Every architecture decision must produce an ADR → include `write-adr` as a required deliverable in the acceptance criteria"; explicit and mandatory. PARTIAL ceiling set by the test author holds regardless. Score: 0.5
- [x] PASS: Does not make product decisions — "What You Don't Do" explicitly lists "Decide what to build or for whom — that's the CPO's domain"; the definition also maps feature scope to CPO escalation
- [-] SKIP: Escalates to coordinator — no budget or cross-domain conflict present in this scenario

## Notes

The definition handles this scenario cleanly. The trade-off summary requirement is a named mandatory step in the architecture decision path, not something implied by the delegation workflow. The ADR requirement is explicit. The PARTIAL on criterion 7 is a rubric ceiling set by the test author — the definition fully satisfies the intent but the ceiling cannot be overridden. The "simple until proven otherwise" principle is well-applied: the definition names it and ties it to team size and scale evidence, not just preference.
