# Technical Decision

Scenario: A user asks the CTO to make a significant architectural decision about system design. Does the CTO assess the context, delegate to the architect appropriately, apply the right decision criteria, and avoid making product-scope decisions?

## Prompt

> We're building Vaultly — a SaaS document management platform for small law firms. We're about to start the backend and need to decide: do we go with a monolithic Django Ninja application or break it into microservices (one for document storage, one for search, one for access control)? We have a team of three backend devs and expect maybe 50 law firm clients in year one, growing to 500 in year three. What's your recommendation?

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

**Recommendation: Django Ninja monolith, structured for future extraction.**

At 3 devs and 500 clients by year 3, microservices would burn your team on operational overhead (service discovery, distributed tracing, cross-service transactions) rather than product. "Upload a document" touches storage, search indexing, and access control atomically — in microservices that becomes a distributed transaction problem on day one.

The core tradeoff: microservices give independent scaling and deployment isolation, but you pay that cost upfront with a small team. A monolith defers that cost until you actually hit the constraint — which at 500 law firm clients you likely won't.

**What I'd do instead:**
- Enforce internal module boundaries from the start: `documents/`, `search/`, `access/` as Django apps with explicit APIs between them (no cross-app model imports)
- Use Django Ninja routers to keep the HTTP surface clean per domain
- Put search behind an interface so you can swap in Elasticsearch/OpenSearch later without touching the rest of the app
- Run it on a single host initially; add a read replica when needed

This gives you the extraction path when you need it, without paying microservices tax when you don't. The moment you hire a 6th dev or hit genuine scaling pain in one domain, you have clean seams to cut on.

The one counter-argument worth considering: if your team already has strong microservices experience and wants to avoid the rewrite risk, the operational cost is more predictable. But for a greenfield Django team of 3, I'd bet on the monolith.

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 8.5/17.0 (50%) |
| Evaluated | 2026-05-01 |
| Target duration | 17965 ms |
| Target cost | $0.0472 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Performs pre-flight — reads project conventions and checks the technology stack before advising | FAIL | The output jumps immediately to a recommendation with no mention of reading project conventions, CLAUDE.md, or checking existing tech stack decisions. No pre-flight step is described or referenced. |
| c2 | Delegates the architecture decision to the architect agent, framing the decision with scope, constraints, and context | FAIL | The output makes the decision itself — 'Recommendation: Django Ninja monolith, structured for future extraction.' No architect agent is mentioned or invoked. The CTO acts as the decision-maker rather than a delegator. |
| c3 | Does not simply pick an option without analysis — identifies the trade-offs between each approach | PASS | 'microservices give independent scaling and deployment isolation, but you pay that cost upfront with a small team... A monolith defers that cost until you actually hit the constraint.' Trade-offs are identified before the recommendation is given. |
| c4 | Applies the principle 'simple until proven otherwise' — accounts for team size (3 devs) and year-one scale (50 clients) in the recommendation | PASS | 'At 3 devs and 500 clients by year 3, microservices would burn your team on operational overhead... rather than product.' Team size (3 devs) is explicitly referenced; the monolith recommendation defers complexity until constraints are actually hit. |
| c5 | Produces a dispatch plan rather than implementing directly | FAIL | The output is a direct recommendation with implementation guidance ('Enforce internal module boundaries from the start… Use Django Ninja routers…'). No dispatch plan or delegation to other roles/agents is present. |
| c6 | Frames a clear escalation path if the decision involves significant vendor lock-in | FAIL | There is no explicit escalation path for vendor lock-in scenarios. The search interface note ('swap in Elasticsearch/OpenSearch later') is a design tip, not a framed escalation path for a lock-in decision. |
| c7 | References the need for an ADR to document the decision and reasoning | FAIL | ADRs are not mentioned anywhere in the output. No reference to documenting the decision, capturing rejected alternatives, or setting future reconsideration triggers. |
| c8 | Does not make product decisions (e.g. what features to build first) — stays in technical domain | PASS | The entire output is technical: module boundaries, Django apps, router structure, search interfaces. No feature prioritisation, pricing, or market segment guidance is offered. |
| c9 | Escalates to coordinator — only relevant if the decision involves budget or cross-domain conflict | SKIP | Criterion marked SKIP — not applicable to this scenario. |
| c10 | Output recommends starting with the monolith — 'simple until proven otherwise' — given 3 backend devs and 50 year-1 clients, and explains that microservices for a 3-person team would burn engineering capacity on infrastructure plumbing instead of features | PASS | 'Recommendation: Django Ninja monolith… microservices would burn your team on operational overhead (service discovery, distributed tracing, cross-service transactions) rather than product.' Exactly matches the required reasoning. |
| c11 | Output addresses the 50 → 500 client growth path — the monolith with proper module boundaries can scale to ~500 customers without re-architecture, and the migration to services (if needed) becomes feasible when the team is bigger | PASS | 'The moment you hire a 6th dev or hit genuine scaling pain in one domain, you have clean seams to cut on.' Module boundaries explicitly positioned as the extraction path, addresssing growth to the point microservices become viable. |
| c12 | Output dispatches the actual decision to the architect via `/architect:system-design` (or equivalent), framing scope (greenfield SaaS, Django Ninja stack), constraints (3 devs, year-1/year-3 scale targets), and required deliverables — not making a unilateral CTO call | FAIL | No dispatch to any architect agent or skill. The output is a unilateral recommendation delivered directly by the CTO persona, with no framing of deliverables for another agent. |
| c13 | Output covers the trade-offs honestly — monolith pros (faster iteration, simpler ops, easier transactions), monolith cons (deployment coupling, scaling axis lockstep), microservices pros (independent scaling, team autonomy at scale), microservices cons (operational overhead, distributed transactions, deployment orchestration) | PARTIAL | Microservices pros ('independent scaling and deployment isolation') and cons ('operational overhead… cross-service transactions… distributed transaction problem') are covered. Monolith pros are implied. Monolith cons (deployment coupling, scaling axis lockstep) are not explicitly stated — a meaningful gap. |
| c14 | Output requires an ADR as the architect's deliverable — capturing the choice, the year-3 reconsideration triggers (e.g. 'if any single bounded context outgrows the monolith on QPS or team count, evaluate extracting it'), and the rejected alternative | FAIL | No ADR is required, mentioned, or referenced. Year-3 reconsideration triggers are touched on informally ('The moment you hire a 6th dev…') but not framed as ADR content or a formal deliverable. |
| c15 | Output addresses the document-management domain specifically — document storage, search, and access control are likely the candidates for FIRST extraction if/when service split happens, so the monolith should already use clean module boundaries (Django apps) for these | PASS | 'Enforce internal module boundaries from the start: `documents/`, `search/`, `access/` as Django apps with explicit APIs between them' directly maps to the three candidate extraction domains. |
| c16 | Output stays in the technical domain — does NOT recommend which features Vaultly should build first, what the pricing should be, or which law-firm segment to target (those are CPO calls) | PASS | No product decisions are made. The output is entirely about module structure, tech choices (Django Ninja, Elasticsearch/OpenSearch), and operational deployment strategy. |
| c17 | Output produces a dispatch plan rather than implementation — the CTO frames the work, the architect designs it, the developers build it | FAIL | The output is implementation-level guidance: 'Enforce internal module boundaries… Use Django Ninja routers… Put search behind an interface…' The CTO both frames and designs the solution, bypassing any architect or dispatch structure. |
| c18 | Output flags vendor lock-in considerations — Django Ninja is open source, but data store choice (Postgres vs hosted alternative) and ML/search infrastructure are the lock-in vectors worth surfacing | PARTIAL | 'Put search behind an interface so you can swap in Elasticsearch/OpenSearch later without touching the rest of the app' addresses search lock-in implicitly. Data store choice and ML infrastructure lock-in vectors are not surfaced. Partial coverage only. |
| c19 | Output addresses team-skill match — Django Ninja is well-suited to a Python team, and a 3-person team is unlikely to have the operational depth to run microservices well | PARTIAL | 'for a greenfield Django team of 3, I'd bet on the monolith' and 'if your team already has strong microservices experience… the operational cost is more predictable' both reference team skill match, though briefly and without explicitly noting Django Ninja's fit for Python teams. |

### Notes

The captured output is a high-quality, well-reasoned technical recommendation that correctly identifies the monolith-first path, applies team-size and scale constraints, names the right domain boundaries (documents/search/access), and stays cleanly in the technical domain. However, it fails the majority of the process-oriented criteria that define the CTO skill's expected behaviour: no pre-flight check, no delegation to an architect agent, no dispatch plan, no ADR requirement, and no formal escalation path for lock-in. The output reads as a direct technical advisor response rather than a CTO operating within an agent hierarchy. Criteria c3, c4, c8, c10, c11, c15, c16 are satisfied; the structural/process criteria (c1, c2, c5, c6, c7, c12, c14, c17) are all failed, which represents the bulk of the scoring weight.
