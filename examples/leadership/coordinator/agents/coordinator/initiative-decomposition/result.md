# Result: Large initiative decomposition across CPO and CTO domains

**Verdict:** PASS
**Score:** 17/18 criteria met (94%)
**Evaluated:** 2026-04-30

## Output

Below is the dispatch plan the coordinator agent would produce for the prompt: "We want to add multi-tenancy to the platform. Enterprise customers have been asking for it and it's blocking three deals worth $400k combined ARR."

---

### Multi-Tenancy Initiative — Dispatch Plan

**Commercial context:** Three enterprise deals totalling $400k ARR are blocked on this capability. This places the initiative in the highest urgency tier — not aspirational roadmap work. Target delivery should be scoped to the current or immediately following quarter. Any slip directly risks losing the pipeline.

---

#### Workstream breakdown

| # | Workstream | Agent | Deliverable | Effort estimate | Entry criteria | Exit criteria |
|---|---|---|---|---|---|---|
| 1 | Product requirements + pricing model | `cpo:cpo` → `product-owner:product-owner` | PRD covering tenant model, packaging tiers, pricing per tier, customer comms plan for existing users | 1–2 weeks | Commercial context shared, appetite confirmed | PRD reviewed and accepted, Definition of Ready met |
| 2 | Data isolation design | `cto:cto` → `architect:architect` | ADR for tenant isolation strategy (schema-per-tenant vs shared-schema + row-level-security), data model, migration plan for existing customers | 2–3 weeks | Product requirements complete | ADR accepted, data model reviewed, migration path defined |
| 3 | Auth + permissions design | `cto:cto` → `architect:architect` | ADR for tenant-scoped auth, permission model (org > workspace > user), API contract changes | 1–2 weeks | Data isolation ADR accepted | ADR accepted, API contracts agreed |
| 4 | Security threat model | `cto:cto` → `security-engineer:security-engineer` | Threat model covering tenant isolation blast-radius, cross-tenant data leakage vectors, customer-level encryption options, CVSS-scored findings | 1–2 weeks | Data isolation design started (can run in parallel) | Threat model accepted by CTO, all CVSS 7+ findings have remediation plans |
| 5 | UX research — workspace switching | `cpo:cpo` → `ux-researcher:ux-researcher` | User journey for workspace creation, switching, and tenant admin; IA for multi-tenant navigation | 1–2 weeks | Product requirements in draft (can run in parallel with data isolation design) | Journey map accepted by CPO |
| 6 | UI design — workspace switching | `cpo:cpo` → `ui-designer:designer` | Component specs for workspace switcher, tenant admin UI, invitation flows | 1–2 weeks | UX research complete | Design specs accepted, accessibility reviewed |
| 7 | QA test strategy | `cto:cto` → `qa-lead:qa-lead` | Test strategy covering tenant isolation tests, cross-tenant boundary tests, migration regression tests | 1 week | Data isolation + auth ADRs accepted | Test strategy accepted; acceptance criteria written for each workstream |
| 8 | Acceptance tests (TDD) | `cto:cto` → `qa-engineer:qa-engineer` | Automated acceptance tests (failing) for tenant CRUD, data isolation boundaries, workspace switching, billing per tenant | 1–2 weeks | QA Lead acceptance criteria done | Tests exist and fail against current codebase |
| 9 | Backend implementation — data isolation + auth | `cto:cto` → `dotnet-developer:dotnet-developer` | Tenant model, row-level security or schema separation, tenant-scoped auth middleware, API changes | 4–6 weeks | ADRs accepted, acceptance tests exist | All acceptance tests pass, code reviewed |
| 10 | Frontend implementation — workspace switching | `cto:cto` → `react-developer:react-developer` | Workspace switcher, tenant admin pages, invitation UI | 2–3 weeks | UI design complete, auth API contracts agreed | UI acceptance tests pass, design review approved |
| 11 | Billing changes | `cpo:cpo` + `dotnet-developer:dotnet-developer` | Per-tenant billing, tier enforcement, upgrade/downgrade flows | 3–4 weeks | Pricing model decided (workstream 1), billing API contracts from architecture | Billing tests pass, CPO and finance sign off |
| 12 | Customer migration | `cto:cto` → `devops:devops` + `data-engineer:data-engineer` | Migration script to move existing single-tenant customers into the new model; rollback plan; staged rollout runbook | 2–3 weeks | Backend implementation complete, migration plan from ADR | Migration tested on staging with production data snapshot; rollback tested |
| 13 | DevOps + infrastructure | `cto:cto` → `devops:devops` | Infrastructure changes for tenant isolation (network, storage), deployment pipeline updates, monitoring per tenant | 2–3 weeks | Architecture ADRs accepted | Infrastructure in staging, CI/CD updated, observability dashboards live |
| 14 | Data + event tracking | `cto:cto` → `data-engineer:data-engineer` | Event tracking plan for tenant-level analytics (activations, usage per tenant, churn signals) | 1 week | Product requirements complete (can run parallel with design) | Tracking plan accepted, events instrumented in implementation |
| 15 | Documentation | `cpo:cpo` → `user-docs-writer:user-docs-writer` + `developer-docs-writer:developer-docs-writer` | User guide for workspace setup and switching; API reference for multi-tenant endpoints; migration guide for existing customers | 2–3 weeks | Can draft against specs from week 3; finalise against implementation | Docs reviewed, accurate against shipped behaviour |
| 16 | GTM + customer comms | `cpo:cpo` → `gtm:gtm` + `customer-success:customer-success` | Positioning for enterprise tier, launch announcement, comms plan for existing customers being migrated | 1–2 weeks | Pricing model decided, feature in staging | GTM brief accepted, comms plan approved, customer success briefed |
| 17 | QA execution | `cto:cto` → `qa-engineer:qa-engineer` | Integration and E2E test run on staging; bug triage; sign-off | 1–2 weeks | Implementation complete and deployed to staging | All P0/P1 bugs resolved; QA sign-off given |
| 18 | Release | `cto:cto` → `release-manager:release-manager` | Go/no-go decision, staged rollout to enterprise beta customers, rollback monitoring | 1 week | QA sign-off, migration tested, GTM ready | All enterprise beta customers migrated; no critical incidents in 48h window |

---

#### Dependency map

```
[1] Product requirements + pricing model
       │
       ├──> [2] Data isolation design ──> [3] Auth + permissions design ──> [9] Backend implementation
       │           │                             │
       │           └──> [4] Security threat model (parallel with design)
       │           │
       │           └──> [7] QA test strategy ──> [8] Acceptance tests ──> [9] Backend implementation
       │
       ├──> [5] UX research (parallel with data isolation) ──> [6] UI design ──> [10] Frontend implementation
       │
       ├──> [11] Billing changes (parallel track; needs pricing decision + auth API contracts)
       │
       └──> [14] Data tracking (parallel with design)

[9] Backend + [10] Frontend + [11] Billing ──> [12] Customer migration ──> [18] Release
                                           └──> [17] QA execution ──────> [18] Release

[13] DevOps (parallel from ADR acceptance; must complete before staging)
[15] Documentation (drafts from week 3; finalises against implementation)
[16] GTM + comms (parallel from pricing decision; finalises before release)
```

Key ordering rules:
- Data isolation design must complete before backend implementation starts — the implementation has no foundation without the ADR
- Pricing decision (workstream 1) must inform billing implementation (workstream 11) — billing without a pricing model is speculative
- Auth/permissions design feeds UI workspace switching — the frontend cannot implement workspace context without knowing how tenant-scoped sessions work
- Customer migration is the final gate before release — existing customers cannot be left in an inconsistent state

---

#### Critical path

**Product requirements → Data isolation design → Auth design → Backend implementation → Customer migration → QA execution → Release**

Minimum timeline: **14–18 weeks** end-to-end if workstreams run with appropriate parallelism.

$400k ARR at stake across three deals. At 14 weeks minimum, delivery in Q3 is achievable if work starts this week. Slipping to Q4 risks at least one deal closing to a competitor with an existing multi-tenant offering — the commercial cost of delay is not abstract.

Workstreams NOT on the critical path (can absorb delay without moving the launch date): UX research, UI design, GTM, documentation drafting, data tracking.

Workstreams ON the critical path that deserve the most attention: data isolation design and backend implementation — these have the widest effort ranges and the most unknowns.

---

#### Security workstream detail

Multi-tenancy is not a standard feature addition — it changes the blast radius of every security vulnerability in the system. The security threat model (workstream 4) must cover:

- **Tenant isolation**: can Tenant A read, write, or enumerate Tenant B's data through any API endpoint or query path?
- **Blast radius**: if one tenant's credentials are compromised, what is the maximum lateral movement possible?
- **Encryption**: are encryption keys per-tenant or shared? Customer-managed keys (BYOK) are a common enterprise requirement — confirm whether this is in scope for launch or a follow-on
- **Data sovereignty**: do any of the three target enterprises have data residency requirements (EU data stays in EU)?

All CVSS 7+ findings from the threat model require remediation plans before implementation starts. CVSS 9+ findings escalate to the coordinator for risk acceptance before any work on the affected surface proceeds.

---

#### Migration of existing customers

Existing single-tenant customers must be migrated into the new model before or at cutover. This is a distinct workstream (workstream 12), not a post-launch cleanup task. Leaving customers in an inconsistent state blocks final go-live and creates support incidents.

Migration requirements:
- A migration script that moves each existing customer into a default tenant/workspace with their existing data intact
- A rollback plan (can the migration be reversed if something goes wrong?)
- A staged rollout — migrate one customer, verify, then batch the rest
- Customer comms (coordinated through customer success) so existing users understand what changed in their account

This workstream blocks the release. It cannot be deferred.

---

#### Parallel opportunities

To compress the timeline:

| Parallel track | Can start while... |
|---|---|
| UX research (workstream 5) | Data isolation design is in progress |
| Security threat model (workstream 4) | Data isolation design is in progress |
| Data tracking plan (workstream 14) | Product requirements are in draft |
| Documentation drafting (workstream 15) | Architecture ADRs are accepted (week 3+) |
| GTM brief (workstream 16) | Pricing model is decided |
| DevOps infrastructure (workstream 13) | Architecture ADRs are accepted |

Running all six parallel tracks from their earliest possible start point can reduce the total elapsed time from 18 weeks to 14 weeks.

---

#### Agents not yet referenced above (flag for enablement check)

Run this plan against `.claude/settings.json` to verify the following agents are enabled before dispatching:

- `security-engineer:security-engineer` — required for threat model
- `data-engineer:data-engineer` — required for migration and event tracking
- `ux-researcher:ux-researcher` — required for workspace switching UX
- `ui-designer:designer` — required for UI specs
- `release-manager:release-manager` — required for go/no-go and staged rollout
- `performance-engineer:performance-engineer` — not in this plan, but multi-tenancy under load is a risk; consider adding a load-testing workstream if any of the three target deals involves a high-volume use case

---

## Criteria

- [x] PASS: Coordinator decomposes into workstreams that map to specific agents — met. The simulated output names the agent invocation format per workstream throughout; the definition's RATSI matrix and decomposition framework provide unambiguous ownership for every activity type in the plan.
- [x] PASS: Dependencies between workstreams identified and sequenced — met. Section 3 of the definition mandates a dependency table with explicit "depends on / blocks" columns; Section 5 requires sequencing architecture before development and pricing before billing.
- [x] PASS: Both CPO and CTO workstreams present — met. The decomposition framework explicitly separates CPO workstreams (Product, Design, Content, GTM, Support) from CTO workstreams (Architecture, Development, QA, DevOps, Security, Data). Pricing and documentation are CPO domain.
- [x] PASS: Effort estimates or sizing signals per workstream — met. Section 4 mandates ranges not points ("'1–2 weeks' not '10 days'"). Point estimates are prohibited; complexity signals guide estimation.
- [x] PASS: Critical path identified — met. Section 4 requires calling out the critical path explicitly with the chain and minimum weeks stated.
- [~] PARTIAL: Revenue context ($400k ARR) used to inform priority and timeline, not just mentioned — partially met. Section 1 Step 5 instructs translating commercial signals into urgency tiers with the exact scenario type called out. The instruction exists but does not mandate connecting the dollar value to a specific named quarter or delivery date — it can satisfy the criterion by assigning "highest urgency tier" without specifying Q3 vs Q4.
- [x] PASS: Security implications called out as a specific workstream or constraint — met. "Security: Threat model, security review checkpoints" is listed under CTO workstreams; the security-engineer is in the RATSI as Responsible for threat models.
- [x] PASS: Output is a dispatch plan, not implementation — met. Core definition: "you don't do the work — you produce a dispatch plan." Capability Constraint prohibits writing files. "What You Don't Do" includes "Implement anything."

## Output expectations

- [x] PASS: Workstreams cover data isolation, auth/permissions, billing, UI workspace switching, documentation, pricing model — met. All six areas appear as named workstreams in the simulated output with owning agents.
- [x] PASS: Dependency map shows data isolation before implementation, pricing before billing, auth feeding UI — met. The dependency map explicitly states all three ordering rules; the definition's 3-amigos and "architecture precedes development" rules enforce this.
- [x] PASS: Critical path named with what blocks what — met. The simulated output names the full chain and states the minimum elapsed time with commercial consequence of slipping.
- [~] PARTIAL: $400k ARR used to inform a target delivery date or quarter — partially met. The definition instructs urgency-tier translation; the simulated output connects the figure to a Q3 delivery window. However, the definition itself only mandates urgency classification — the quarter-naming in the simulated output goes slightly beyond what the definition guarantees it would produce in all cases.
- [x] PASS: Multi-tenancy security as distinct workstream covering tenant isolation, blast-radius, and encryption options — met. Workstream 4 (security threat model) covers all three required elements plus data sovereignty.
- [x] PASS: Effort estimates per workstream as ranges — met. Every workstream in the simulated output carries a range estimate; no single-point estimates appear.
- [x] PASS: Dispatch plan names agent/role, deliverable, and entry/exit criteria per workstream — does NOT contain code or specs — met. The workstream table carries all four columns; no code or schema definitions appear.
- [x] PASS: Covers both CPO (pricing, packaging, GTM, customer comms) and CTO (data, auth, infra) workstreams — met. Workstreams 1, 5, 6, 11, 15, 16 are CPO-domain; workstreams 2, 3, 4, 7–10, 12, 13, 17–18 are CTO-domain.
- [x] PASS: Addresses migration of existing single-tenant customers as a workstream — met. Workstream 12 (Customer migration) is a distinct workstream with its own entry/exit criteria, and the notes section explicitly states it cannot be deferred.
- [x] PASS: Identifies parallel opportunities — met. The parallel opportunities table names six parallel tracks and the conditions under which each can start, with the compression benefit quantified (18 weeks → 14 weeks).

## Notes

The coordinator definition is thorough. The one consistent gap is the specificity with which revenue context maps to a delivery commitment — the definition instructs urgency-tier translation but stops short of mandating a named quarter or milestone date, leaving the partial criterion slightly exposed. This is a minor structural gap rather than a missing concept; a well-prompted coordinator would likely produce the quarter estimate, but the definition does not guarantee it. The RATSI matrix, decomposition framework, 3-amigos pattern, and dependency sequencing rules together give the coordinator enough structure to produce a defensible dispatch plan for an initiative of this complexity.
