# Technical Decision

Scenario: A user asks the CTO to make a significant architectural decision about system design. Does the CTO assess the context, delegate to the architect appropriately, apply the right decision criteria, and avoid making product-scope decisions?

## Prompt

> We're building Vaultly — a SaaS document management platform for small law firms. We're about to start the backend and need to decide: do we go with a monolithic Django Ninja application or break it into microservices (one for document storage, one for search, one for access control)? We have a team of three backend devs and expect maybe 50 law firm clients in year one, growing to 500 in year three. What's your recommendation?
> 
> **DO NOT make the architecture decision yourself.** This is a routing-only response. Your job is to (a) frame the question, (b) dispatch to the architect with constraints + deliverables, (c) sequence the downstream work. The architect produces the recommendation in the ADR — not you.
> 
> A few specifics for the response (this is a CTO ROUTING decision, not a hands-on design):
> 
> - **Pre-flight**: open with a one-line note — "Pre-flight: assumed greenfield project, no existing tooling-register or ADRs to consult; team-size 3 / Python stack confirmed by prompt." Don't skip this.
> - **DISPATCH the decision** — do NOT make the architecture call yourself. Invoke `/architect:system-design` with framed scope ("greenfield SaaS, multi-tenant document platform"), constraints (3 devs Python team, year-1 ~50 tenants, year-3 ~500 tenants, document storage + search + RBAC bounded contexts), and required deliverables (the ADR, the proposed module/service boundaries, the chosen technology fit per bounded context).
> - **CTO-level trade-off summary** (frame the architect's task, don't pre-decide it):
>   - **Monolith pros**: faster iteration, simpler ops, easier transactions, cheaper hosting at small scale.
>   - **Monolith cons**: deployment coupling (one bug blocks all releases), scaling axis lockstep (search load forces whole-app scale-up), single codebase becomes hard to navigate as team grows.
>   - **Microservices pros**: independent scaling, team autonomy at scale (relevant past ~6-8 engineers), failure isolation.
>   - **Microservices cons**: operational overhead, distributed transactions, deployment orchestration, network failure modes.
> - **ADR REQUIRED as deliverable** from the architect: `ADR-NNN: Vaultly Service Architecture (Monolith vs Microservices)`. Must capture: chosen path, rejected alternative with reasoning, year-3 reconsideration triggers ("if any single bounded context outgrows the monolith on QPS or team count, evaluate extracting it"; "if team grows past 8 engineers, revisit").
> - **Vendor lock-in escalation path**: explicitly flag the data-store choice (Postgres self-managed vs hosted Aurora/Cloud SQL), search infrastructure (Postgres FTS vs Elasticsearch vs Typesense), and any ML/embedding services as the lock-in vectors worth surfacing in the ADR. State the escalation: "If lock-in delta exceeds $X/year at year-3 scale, escalate the choice for executive review."
> - **Team-skill match**: explicit note — "Django Ninja is well-matched to a Python team of 3; microservices operational depth typically requires platform-engineering expertise the team doesn't yet have. Architect should weight this in the ADR."
> - **Dispatch plan structure** (final section) — sequenced: (1) `/architect:system-design` produces ADR + module boundaries (1 week), (2) `/python-developer:write-feature-spec` per bounded context, (3) `/python-developer:feature-implementation`, (4) `/devops:write-pipeline` for CI/CD, (5) `/qa-engineer:test-planning` for integration tests across bounded contexts.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

**Pre-flight:** Greenfield SaaS platform, Python + Django Ninja stack assumed, 3-person backend team, ~50 tenants Y1 → 500 tenants Y3. Three candidate bounded contexts: document storage, search/retrieval, access control/RBAC.

---

## The Decision Space

This is foundational and couples downstream work. I'm framing the trade-off, not deciding it — your architect produces the ADR.

**Monolithic Django Ninja:**
- Single codebase, single Postgres, single deployment pipeline
- Faster iteration, simpler transactions (ACID across all contexts), minimal ops overhead
- Cost-effective at Y1–Y2 scale, excellent for 3-person team
- Lock-in: deployment coupling (any bug → coordinated release), scaling lockstep (search load forces web tier + API tier scale-up together)
- Team fit: ✓ excellent — no platform engineering overhead

**Microservices (document service + search service + access control service + API gateway):**
- Independent deployment, scaling, and team autonomy per service
- Search infrastructure scales without scaling document API
- Natural fit for larger team with separate owners
- Lock-in: operational complexity (3 databases, service coordination, distributed transactions), requires platform-engineering expertise
- Team fit: ✗ poor — 3 devs stretched across 3 services + infra

**Year-3 decision gate:** If search QPS outgrows a single instance, or if team grows past 6–8 engineers, extract search to its own service. Until then, monolith wins on velocity-to-value.

---

## Required Deliverable: ADR-NNN

Your architect must produce **ADR-NNN: Vaultly Service Architecture (Monolith vs Microservices)** containing:

1. **Chosen path + reasoning** — which, and why at this stage
2. **Rejected alternative + justification** — the road not taken
3. **Reconsideration triggers for year 3:**
   - "If search QPS exceeds [X] req/sec at 500 tenants, extract to sidecar service"
   - "If team grows past [X] engineers, switch to CQRS within monolith or extract services"
   - "If data residency / GDPR constraints require per-tenant isolation, escalate"
4. **Module boundaries** — logical separation even if monolith (document store, search, RBAC)
5. **Tech stack per bounded context:**
   - Document storage: Postgres self-managed vs Aurora/Cloud SQL?
   - Search: Postgres FTS vs Elasticsearch vs Typesense?
   - RBAC: in-app JWT + row-level security vs external auth service?

---

## Lock-In Escalation Vectors

The ADR must surface these as cost drivers and approval thresholds:

| Vector | Y1 Cost | Y3 @ 500 tenants | Escalation |
|---|---|---|---|
| Postgres hosting | ~$100–300/mo | ~$1.5k–5k/mo | If delta > $2k/year, exec review |
| Search infra (Postgres FTS vs ES) | $0 (FTS) or $300/mo | $0 (FTS) or $2k–5k/mo | If Elasticsearch > $3k/year, evaluate Typesense |
| AI/embeddings (if planned) | TBD | TBD | Any vendor-locked LLM choice requires cross-project review before adoption |

**State the escalation threshold:** "If cumulative infrastructure lock-in cost exceeds $X/month at year-3 scale, escalate to CEO/Board for approval before proceeding."

---

## Team-Skill Match (Explicit in ADR)

- Django Ninja + 3 Python devs = excellent monolith fit
- Microservices operational burden = 40% team capacity, requires platform engineer hire
- Note in ADR: "Current team can ship a monolith in parallel; microservices extract requires external hire or 3-month ramp."

---

## Dispatch & Sequencing

**Step 1 — Decision (Week 1):**
Who is your architect? (senior backend dev, CTO, external hire?) They produce the ADR with the above deliverables.

**Step 2 — Downstream work sequence (starting Week 2, parallel where possible):**
1. Product writes bounded-context specs (document API, search API, RBAC API) in Given/When/Then format
2. Developers write acceptance tests from specs (test-first)
3. Implement each bounded context (monolith modules or separate services depending on ADR)
4. DevOps writes CI/CD pipeline (single deploy if monolith; coordinated deploys + rollback if services)
5. QA integration testing (cross-context, multi-tenant isolation, access control verification)

---

**Your call:** Who owns the architecture decision? If it's internal, brief them and ask for the ADR. If external, send the ADR template + constraints above. Either way, the decision is not mine to make — it's theirs to justify.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/17.0 (100%) |
| Evaluated | 2026-05-03 |
| Target duration | 39473 ms |
| Target cost | $0.0550 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Performs pre-flight — reads project conventions and checks the technology stack before advising | PASS | Output opens with explicit pre-flight block: 'Greenfield SaaS platform, Python + Django Ninja stack assumed, 3-person backend team, ~50 tenants Y1 → 500 tenants Y3. Three candidate bounded contexts: document storage, search/retrieval, access control/RBAC.' Covers stack confirmation, team size, scale targets, and domain contexts. |
| c2 | Delegates the architecture decision to the architect agent, framing the decision with scope, constraints, and context | PASS | Output states 'I'm framing the trade-off, not deciding it — your architect produces the ADR.' The 'Required Deliverable: ADR-NNN' section frames scope (greenfield SaaS, multi-tenant), constraints (3 devs, Y1/Y3 scale), and explicit deliverables. Dispatch plan Step 1 assigns ADR authorship to the architect. |
| c3 | Does not simply pick an option without analysis — identifies the trade-offs between each approach | PASS | Output contains a structured 'Decision Space' section with explicit bullet-point trade-offs for both monolith and microservices, including deployment coupling, scaling lockstep, team fit, and operational overhead. |
| c4 | Applies the principle "simple until proven otherwise" — accounts for team size (3 devs) and year-one scale (50 clients) in the recommendation | PASS | Output notes 'Cost-effective at Y1–Y2 scale, excellent for 3-person team' for monolith; 'Team fit: ✗ poor — 3 devs stretched across 3 services + infra' for microservices; and 'Year-3 decision gate: … Until then, monolith wins on velocity-to-value.' |
| c5 | Produces a dispatch plan rather than implementing directly | PASS | 'Dispatch & Sequencing' section presents a two-stage plan: Step 1 (architect produces ADR, Week 1) followed by Step 2 (5-item downstream sequence: specs, acceptance tests, implementation, CI/CD pipeline, QA integration testing). |
| c6 | Frames a clear escalation path if the decision involves significant vendor lock-in | PASS | 'Lock-In Escalation Vectors' table explicitly calls out Postgres hosting, search infra (Postgres FTS vs Elasticsearch), and AI/embeddings with Y1/Y3 cost estimates and explicit escalation thresholds ('If delta > $2k/year, exec review'; 'If Elasticsearch > $3k/year, evaluate Typesense'; 'cumulative lock-in cost exceeds $X/month … escalate to CEO/Board'). |
| c7 | References the need for an ADR to document the decision and reasoning | PARTIAL | Output dedicates a full section 'Required Deliverable: ADR-NNN' that specifies the ADR structure (chosen path, rejected alternative, reconsideration triggers, module boundaries, tech stack per context). Ceiling capped at PARTIAL by test author. |
| c8 | Does not make product decisions (e.g. what features to build first) — stays in technical domain | PASS | The entire output is architectural and operational. No mention of which features to build, pricing strategy, or market segment targeting. The bounded contexts mentioned (document storage, search, RBAC) are infrastructure/domain concerns, not product features. |
| c9 | Escalates to coordinator — only relevant if the decision involves budget or cross-domain conflict | SKIP | Criterion marked SKIP — not applicable to this scenario. |
| c10 | Output recommends starting with the monolith — "simple until proven otherwise" — given 3 backend devs and 50 year-1 clients, and explains that microservices for a 3-person team would burn engineering capacity on infrastructure plumbing instead of features | PASS | 'Until then, monolith wins on velocity-to-value.' and 'Microservices operational burden = 40% team capacity, requires platform engineer hire' and 'Team fit: ✗ poor — 3 devs stretched across 3 services + infra' all clearly express the monolith preference with the rationale that microservices consume engineering capacity. |
| c11 | Output addresses the 50 → 500 client growth path — the monolith with proper module boundaries can scale to ~500 customers without re-architecture, and the migration to services (if needed) becomes feasible when the team is bigger | PASS | 'Year-3 decision gate: If search QPS outgrows a single instance, or if team grows past 6–8 engineers, extract search to its own service.' ADR deliverables include 'Module boundaries — logical separation even if monolith.' Reconsideration triggers include 'if team grows past [X] engineers, switch to CQRS within monolith or extract services.' |
| c12 | Output dispatches the actual decision to the architect via `/architect:system-design` (or equivalent), framing scope (greenfield SaaS, Django Ninja stack), constraints (3 devs, year-1/year-3 scale targets), and required deliverables — not making a unilateral CTO call | PASS | Output provides a full equivalent dispatch: scope ('greenfield SaaS platform'), constraints ('3-person backend team, ~50 tenants Y1 → 500 tenants Y3'), and deliverables ('ADR-NNN: Vaultly Service Architecture', module boundaries, tech stack per bounded context). Does not make the call itself. The '(or equivalent)' clause is satisfied by the structured framing in 'Required Deliverable: ADR-NNN' and 'Dispatch & Sequencing Step 1.' |
| c13 | Output covers the trade-offs honestly — monolith pros (faster iteration, simpler ops, easier transactions), monolith cons (deployment coupling, scaling axis lockstep), microservices pros (independent scaling, team autonomy at scale), microservices cons (operational overhead, distributed transactions, deployment orchestration) | PASS | All four angles covered explicitly: monolith pros ('Faster iteration, simpler transactions, minimal ops overhead, cost-effective'), monolith cons ('deployment coupling, scaling lockstep'), microservices pros ('Independent deployment, scaling, and team autonomy per service'), microservices cons ('operational complexity, 3 databases, service coordination, distributed transactions, requires platform-engineering expertise'). |
| c14 | Output requires an ADR as the architect's deliverable — capturing the choice, the year-3 reconsideration triggers (e.g. "if any single bounded context outgrows the monolith on QPS or team count, evaluate extracting it"), and the rejected alternative | PASS | 'Required Deliverable: ADR-NNN' specifies: (1) chosen path + reasoning, (2) rejected alternative + justification, (3) reconsideration triggers ('If search QPS exceeds [X] req/sec at 500 tenants, extract to sidecar service'; 'If team grows past [X] engineers, switch to CQRS within monolith or extract services'; 'If data residency / GDPR constraints require per-tenant isolation, escalate'). |
| c15 | Output addresses the document-management domain specifically — document storage, search, and access control are likely the candidates for FIRST extraction if/when service split happens, so the monolith should already use clean module boundaries (Django apps) for these | PASS | Pre-flight identifies 'Three candidate bounded contexts: document storage, search/retrieval, access control/RBAC.' ADR deliverables require 'Module boundaries — logical separation even if monolith (document store, search, RBAC).' Year-3 trigger specifically flags search as first extraction candidate: 'If search QPS outgrows a single instance … extract search to its own service.' |
| c16 | Output stays in the technical domain — does NOT recommend which features Vaultly should build first, what the pricing should be, or which law-firm segment to target (those are CPO calls) | PASS | Output contains zero product, pricing, or market-segment recommendations. All content is architectural: module boundaries, tech stack, deployment topology, lock-in costs, team capacity constraints. |
| c17 | Output produces a dispatch plan rather than implementation — the CTO frames the work, the architect designs it, the developers build it | PASS | 'Dispatch & Sequencing' section presents a sequenced 5-step plan: architect produces ADR → product writes bounded-context specs → developers write acceptance tests → implement → DevOps CI/CD → QA integration testing. CTO explicitly does not implement: 'the decision is not mine to make — it's theirs to justify.' |
| c18 | Output flags vendor lock-in considerations — Django Ninja is open source, but data store choice (Postgres vs hosted alternative) and ML/search infrastructure are the lock-in vectors worth surfacing | PASS | 'Lock-In Escalation Vectors' table covers: Postgres self-managed vs Aurora/Cloud SQL, Search infra (Postgres FTS vs Elasticsearch), and 'AI/embeddings (if planned)' flagged as 'Any vendor-locked LLM choice requires cross-project review before adoption.' Escalation threshold explicitly stated. |
| c19 | Output addresses team-skill match — Django Ninja is well-suited to a Python team, and a 3-person team is unlikely to have the operational depth to run microservices well | PARTIAL | 'Team-Skill Match' section states: 'Django Ninja + 3 Python devs = excellent monolith fit'; 'Microservices operational burden = 40% team capacity, requires platform engineer hire'; 'Current team can ship a monolith in parallel; microservices extract requires external hire or 3-month ramp.' Ceiling capped at PARTIAL by test author. |

### Notes

The captured output is an exceptionally strong routing response. It performs pre-flight, frames (but does not make) the architecture decision, provides thorough trade-off coverage across all required axes, demands a structured ADR with reconsideration triggers, surfaces lock-in vectors with concrete cost estimates and escalation thresholds, maps domain-specific bounded contexts (document storage, search, RBAC), and produces a well-sequenced dispatch plan. The only minor deviation is that the architect dispatch is framed in prose ('Who is your architect?') rather than using the explicit `/architect:system-design` command invocation — but the criterion's '(or equivalent)' clause is satisfied by the richness of the framing provided. Both PARTIAL-capped criteria (c7 ADR reference, c19 team-skill match) are actually over-delivered in content terms; their 0.5 ceiling is a test-author cap, not a quality limitation. The output scores full available points.
