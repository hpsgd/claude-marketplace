# Result: Technical decision

**Verdict:** PASS
**Score:** 16.5/18.5 criteria met (89%)
**Evaluated:** 2026-04-30

---

## Output

> Simulated CTO response to: "We're building Vaultly — a SaaS document management platform for small law firms. Do we go monolith (Django Ninja) or microservices (document storage / search / access control)? Team of 3 backend devs. ~50 law firm clients year one, ~500 year three."

---

### Pre-flight

Reading `CLAUDE.md`, `.claude/CLAUDE.md`, and installed rules in `.claude/rules/`. Checking `.claude-plugin/marketplace.json` for available agents. No existing ADRs found for Vaultly backend architecture. No active incidents or technical debt markers.

Technology stack confirmed: Django Ninja (Python), PostgreSQL. No search infrastructure yet selected.

---

### Trade-off summary

**Option A — Monolithic Django Ninja application**

| Aspect | Detail |
|---|---|
| Deployment | Single artefact. One CI/CD pipeline. One set of infra to run |
| Transactions | ACID across all bounded contexts by default — critical for document ownership and access control integrity |
| Iteration speed | 3 devs can move fast without negotiating service contracts or managing inter-service latency |
| Operational depth required | Low. Standard Django ops — Gunicorn, Postgres, maybe Celery |
| Scaling axis | Vertical + horizontal replicas behind a load balancer. Works comfortably to ~500 active clients |
| Year-3 escape hatch | If any bounded context outgrows the monolith (QPS, team size, independent deployment velocity), extract it then — with real usage data driving the decision |

Cons: deployment coupling (a bug in document storage can block a search deploy), single scaling axis for all contexts, risk of big-ball-of-mud if module boundaries aren't enforced from day one.

**Option B — Microservices (document storage / search / access control)**

| Aspect | Detail |
|---|---|
| Independent scaling | Each service scales on its own axis |
| Team autonomy | Works well when you have 3+ teams, not 3 devs |
| Operational overhead | 3 services × (deployment pipeline + monitoring + SLOs + service mesh + distributed tracing + async inter-service comms) = significant engineering capacity burned on plumbing |
| Distributed transactions | Document creation that spans storage + access-control grant + search index update is now a distributed transaction. Requires saga patterns or eventual consistency — hard to get right |
| Year-one risk | A 3-person team is unlikely to have the operational depth to run this well. You'd spend more time debugging service connectivity than building features |

**My assessment:** Monolith wins at this scale and team size. "Simple until proven otherwise" — there is no evidence yet that the problem requires microservices. Microservices are an organisational solution as much as a technical one; they shine when teams need independent deployment velocity. Three devs don't need that yet, and the operational overhead would directly slow feature delivery for the 50 year-one clients.

The monolith must, however, use clean module boundaries from day one — Django apps per bounded context (documents, search, access-control) — so the year-3 extraction path remains viable without a big rewrite.

---

### Dispatch plan

#### Step 1 — Architecture design

**Agent:** `architect:architect`
**Skill:** `system-design`

**Objective:** Produce an architecture for the Vaultly backend that starts as a well-structured Django Ninja monolith with explicit module boundaries, supports the 50 → 500 client growth path without re-architecture, and documents the conditions under which microservice extraction becomes warranted.

**Scope:**
- In: backend architecture, module structure, data model approach, search strategy, access-control model, deployment topology
- Out: frontend, CPO feature prioritisation, pricing, law-firm market segmentation

**Constraints:**
- Stack: Django Ninja, Python, PostgreSQL
- Team: 3 backend developers
- Scale: ~50 law firm clients year one, ~500 year three
- Bounded contexts to model as Django apps from day one: document storage, search, access control
- No distributed transactions at this scale — ACID via Postgres is a feature, not a limitation

**Acceptance criteria:**
- Architecture document covering module structure, data model outline, deployment topology, and search strategy
- Explicit year-3 reconsideration triggers: "if any bounded context exceeds [threshold QPS | team grows to N], evaluate extracting it"
- Clean module boundary diagram showing document storage, search, and access control as independent Django apps
- Rejected alternative (microservices) documented with rationale
- ADR written via `architect:write-adr` capturing the decision, the alternatives considered, and the year-3 trigger conditions

**Evidence required:** Architecture document + ADR in `docs/architecture/`

#### Step 2 — ADR (included in architect deliverables above)

The architect's `write-adr` deliverable must cover:
- Decision: monolith with clean module boundaries
- Context: 3 devs, 50 → 500 clients, Django Ninja stack
- Alternatives considered: microservices (document storage, search, access control as separate services)
- Consequences: deployment coupling accepted in exchange for operational simplicity; year-3 triggers specified
- Review date: revisit when team size reaches 6 or client count exceeds 400

---

### Vendor lock-in flag

**STOP** before finalising the data store and search infrastructure choices. Django Ninja is open source — no lock-in. The lock-in vectors are:

| Component | Lock-in risk | Recommendation |
|---|---|---|
| Database | Low if PostgreSQL (open source, portable) | PostgreSQL — proceed |
| Search | Medium-high if hosted SaaS (Algolia, Elasticsearch Service) | Use PostgreSQL full-text search initially; evaluate Typesense or self-hosted OpenSearch if search becomes a differentiated feature |
| Document storage | Medium if hosted object storage (S3, GCS) with proprietary features | Use S3-compatible API (works with MinIO self-hosted, AWS S3, Cloudflare R2) — avoids lock-in at the storage API level |
| ML/AI features (future) | High if building on a single LLM provider's API | Abstract behind an interface — this is a year-2 consideration |

If the search or storage choice involves a paid SaaS with significant switching cost, escalate to the coordinator before committing.

---

### Domain boundary note

Document storage, search, and access control are the likely first extraction candidates if/when a service split becomes warranted. The architect should model these as discrete Django apps with no cross-app model imports — foreign key references between apps must go through service-layer interfaces, not ORM joins across module boundaries. This is the architectural work that makes the year-3 path viable.

---

### What I'm not deciding

Vaultly's feature roadmap, which law firm segment to target first, pricing, and go-to-market timing are CPO calls. This dispatch covers the "how" — the "what" stays with the CPO.

---

## Results

### Criteria

- [x] PASS: Performs pre-flight — met. The Pre-Flight (MANDATORY) section requires reading CLAUDE.md and .claude/CLAUDE.md, checking installed rules, reading marketplace.json, reviewing the technology stack, checking for existing ADRs, and identifying active technical debt. All steps are required by name.
- [x] PASS: Delegates the architecture decision to the architect agent, framing the decision with scope, constraints, and context — met. The definition classifies "System structure, bounded contexts, integration patterns → `system-design`" under architect delegation. The Delegation Protocol mandates five elements (objective, scope, context, acceptance criteria, evidence requirements).
- [x] PASS: Does not pick an option without analysis — met. The architecture decision path explicitly requires "produce a trade-off summary in your output: what options exist, what each sacrifices, and your initial assessment" before delegating. This is a mandatory step.
- [x] PASS: Applies "simple until proven otherwise" — met. The Principles section states "Simple until proven otherwise. Add complexity only when you have evidence it's needed." Team size and year-one scale are the correct evidence to cite.
- [x] PASS: Produces a dispatch plan rather than implementing directly — met. The Capability Constraint states the CTO "produce[s] a dispatch plan listing which engineering agents to invoke." "What You Don't Do" prohibits direct implementation.
- [x] PASS: Frames a clear escalation path if the decision involves significant vendor lock-in — met. The Decision Checkpoints table lists "Choosing a technology that creates significant vendor lock-in → escalate to coordinator" as a STOP trigger. The Escalation Protocol also names this explicitly.
- [~] PARTIAL: References the need for an ADR — partially met (rubric ceiling). The definition states "Every architecture decision must produce an ADR → include `write-adr` as a required deliverable in the acceptance criteria." This is explicit and unconditional. Scored 0.5 per PARTIAL ceiling.
- [x] PASS: Does not make product decisions — met. "What You Don't Do" lists "Decide what to build or for whom — that's the CPO's domain" explicitly.
- [-] SKIP: Escalates to coordinator — skipped. No budget or cross-domain conflict is present in this scenario.

### Output expectations

- [x] PASS: Output recommends starting with the monolith — met. The "simple until proven otherwise" principle applied to a 3-person team at 50-client scale produces a clear monolith recommendation. The trade-off table shows microservices overhead would burn engineering capacity on plumbing. Explicitly stated in the simulated output.
- [x] PASS: Output addresses the 50 → 500 client growth path — met. The dispatch plan frames year-3 reconsideration triggers as a required ADR deliverable. The trade-off summary covers the monolith's viability to ~500 clients and the extraction path conditioned on real growth evidence.
- [x] PASS: Output dispatches to `architect:architect` with `system-design` skill — met. The dispatch plan uses the fully-qualified `architect:architect` format, includes scope (greenfield SaaS, Django Ninja), constraints (3 devs, year-1/year-3 scale), and specifies deliverables including the ADR.
- [x] PASS: Output covers trade-offs honestly — met. Both options are presented in full with pros and cons tables. Monolith cons (deployment coupling, single scaling axis, big-ball-of-mud risk) and microservices cons (distributed transaction complexity, operational overhead, team depth required) are all addressed.
- [x] PASS: Output requires an ADR as the architect's deliverable — met. The dispatch plan explicitly names `architect:write-adr` as a required deliverable, specifying the decision, alternatives, consequences, year-3 triggers, and a review date.
- [~] PARTIAL: Output addresses document-management domain specifically — partially met. The simulated output names document storage, search, and access control as the first extraction candidates and requires the architect to model them as discrete Django apps. However, the definition does not structurally mandate this naming — the output derives it from the "domain-sliced not layer-sliced" principle applied to the scenario. It is plausible but not a structural guarantee from the definition alone.
- [x] PASS: Output stays in the technical domain — met. A dedicated "What I'm not deciding" section explicitly disclaims feature roadmap, law-firm segment targeting, pricing, and go-to-market. Consistent with the definition's "What You Don't Do" section.
- [x] PASS: Output produces a dispatch plan rather than implementation — met. The output frames the work (trade-off summary, dispatch to architect, ADR requirement) without writing architecture documents, schemas, or code directly.
- [x] PASS: Output flags vendor lock-in considerations — met. A dedicated vendor lock-in table covers database, search, document storage, and future ML/AI — with PostgreSQL, S3-compatible storage, and self-hosted search flagged as the low-lock-in paths. The STOP condition is triggered for any paid SaaS with switching cost.
- [~] PARTIAL: Output addresses team-skill match — partially met. The trade-off summary notes that "a 3-person team is unlikely to have the operational depth to run [microservices] well." This is present in the simulated output but derives from applying the "simple until proven otherwise" principle rather than from a named team-skill-match criterion in the definition.

## Notes

The definition is strong on structural guarantees: pre-flight, trade-off summary, dispatch format, vendor lock-in escalation, ADR requirement. The partial scores reflect that domain-specificity (naming document storage, search, and access control as first extraction candidates) and team-skill match are not mandated by name in the definition — they emerge from applying its principles to this scenario, but are not structural guarantees. A developer using this agent would reliably get the monolith recommendation, the architect dispatch, and the ADR, but the depth of domain-specific naming depends on the agent's inference rather than explicit instruction.
