# Initiative Decomposition

Scenario: A major platform change (multi-tenancy) that spans product, engineering, security, and commercial concerns. Tests whether the coordinator decomposes into the right workstreams, maps them to agents, sequences dependencies, and produces a dispatch plan rather than jumping to implementation.

## Prompt

> We want to add multi-tenancy to the platform. Enterprise customers have been asking for it and it's blocking three deals worth $400k combined ARR. The touches everything — data isolation, auth/permissions, billing, UI (workspace switching), documentation, and pricing model changes.
> 
> Do not ask for clarification — proceed based on the information provided. Produce the full decomposition now, noting any assumptions you make.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

# Initiative Decomposition: Enterprise Multi-Tenancy Platform

## Context

| Question | Answer |
|---|---|
| **User problem** | Enterprise customers require data isolation, role-based workspaces, and per-tenant billing to meet procurement/compliance standards. Without multi-tenancy, these customers cannot adopt the platform. |
| **Target user** | Mid-market and enterprise customers with 10–1000+ seats, who require GDPR/SOC 2 compliance, role-based access controls, and usage-based billing. |
| **Success criteria** | Close 3 blocked enterprise deals ($400k combined ARR); support unlimited concurrent tenants on single deployment; <100ms workspace-switch latency; 100% audit logging for tenant operations; zero unintended cross-tenant data access; sales can demonstrate multi-tenant features in proof-of-concept. |
| **Appetite** | 10–12 weeks. This is deal-blocking and revenue-critical. High priority for CTO and CPO teams. |
| **Constraints** | Must preserve backward compatibility for existing single-tenant customers; auth/permissions is the critical path (data isolation, UI, and billing all depend on it); billing system integration cannot be deferred (pricing changes are go-to-market requirement); security review is mandatory before any launch. |

## Workstreams

### CPO Team

| Workstream | Owner role | Initiative-specific deliverables | Relevant? |
|---|---|---|---|
| **Product** | product-owner | PRD defining: tenant model (account → workspace hierarchy), seat/user allocation model, permission matrix (owner/admin/member/viewer roles), workspace switching behavior, per-tenant feature flags, bulk user provisioning via SCIM, audit logging requirements | ✅ Yes — core to deal closure |
| **Design** | ui-designer | Workspace switcher (account context + quick-switch dropdown), tenant admin dashboard (users, roles, billing, audit log viewer), workspace settings (name, capacity, feature toggles), invite/onboarding flows, role assignment UI, mobile-responsive tenant navigation | ✅ Yes — enterprise customers evaluate UX before purchasing |
| **Content** | user-docs-writer | Tenant admin guide, workspace management documentation, role/permission reference, audit log interpretation guide, SCIM provisioning guide, SOC 2 compliance attestation, multi-tenant FAQ, migration guide for existing customers upgrading to multi-tenant | ✅ Yes — mandatory for enterprise sales process |
| **GTM** | gtm | Positioning multi-tenancy as enterprise feature, case studies from early adopters, comparison against competitors (single-tenant limitations), sales collateral for account structure/seat model, ROI calculator for per-seat pricing model | ✅ Yes — $400k deal closure depends on positioning |
| **Support** | support | Tenant admin troubleshooting FAQ, workspace permission debugging guide, escalation procedures for cross-tenant data concerns, common onboarding issues, bulk user provisioning troubleshooting | ✅ Yes — early adopters will need hand-holding |
| **Research** | ux-researcher | Usability testing of workspace switcher with enterprise users, permission matrix validation (is the role model intuitive?), onboarding flow testing, early adopter feedback on feature gaps | ✅ Yes — enterprise UX must reduce cognitive load |

### CTO Team

| Workstream | Owner role | Initiative-specific deliverables | Relevant? |
|---|---|---|---|
| **Architecture** | architect | System design: tenant isolation strategy (row-level security vs. schema-based vs. isolated databases — with trade-off analysis), updated data model (tenant_id foreign key propagation, soft multi-tenancy vs. hard), authentication model (tenant-aware JWT, workspace claims), API contract (tenant routing, workspace context in headers), policy enforcement layer (middleware for tenant isolation checks), ADR documenting isolation approach | ✅ Yes — all downstream work depends on this |
| **Development** | senior-backend-engineer, senior-frontend-engineer | Core implementation: (1) auth layer — tenant context injection into all requests, workspace-aware JWTs, session management; (2) data layer — tenant routing, query filters, update guards ensuring no cross-tenant leaks; (3) API endpoints — tenant CRUD, workspace management, user/role assignment; (4) frontend — workspace context management, switcher component, tenant-aware feature flags; (5) billing integration — per-tenant usage tracking, seat-based charges, invoice generation per workspace | ✅ Yes — 6–8 weeks of effort, critical path |
| **QA Planning** | qa-lead | Test strategy: isolation breach scenarios (can user A access user B's data via direct ID manipulation?), permission enforcement matrix (each role-feature-action combination tested), workspace context leakage (are workspace claims enforced in all API paths?), compliance edge cases (audit log completeness, data retention per tenant), performance under multi-tenant load, data migration integrity | ✅ Yes — compliance-critical; test plan must be exhaustive |
| **QA Execution** | qa-engineer | Automated test suite: isolation tests (parameterized across all API endpoints), permission matrix tests (role-based access control verification), data leak detection (negative tests), audit log audits (all mutations logged), batch user provisioning validation, workspace switching reliability, compliance verification against SOC 2 requirements | ✅ Yes — multi-week effort; enterprise deals depend on test coverage |
| **DevOps** | devops | Infrastructure: tenant provisioning automation (account creation → workspace setup → initial user provisioning), backup/restore per-tenant (with audit trail), tenant-aware monitoring (alert on isolation breaches, per-tenant latency, resource contention), graceful degradation for tenant isolation failures, audit log persistence (immutable, compliant with long-term retention), secrets per-tenant (API keys, webhook tokens) | ✅ Yes — ops must support multi-tenant reliability |
| **Security** | security-engineer | Threat model: cross-tenant data access scenarios (direct ID manipulation, query injection, insecure deserialization), permission bypass vectors (role escalation, workspace context spoofing), audit logging integrity, secrets leakage, compliance requirements (GDPR data deletion per tenant, right to audit), isolation breach detection and remediation, penetration test for multi-tenant scenarios, security architecture review | ✅ Yes — mandatory; enterprise customers will audit us |
| **Data** | data-engineer | Event tracking: workspace creation/deletion, user-role assignments, permission changes, audit log events (all mutations), usage metrics per tenant (API calls, storage, seats), billing event pipeline (seat activations, usage charges), dashboard for tenant usage analytics, compliance reporting (audit trails exportable per tenant) | ✅ Yes — billing and compliance depend on clean event tracking |

## Dependencies

| Workstream | Depends on | What it needs before starting | Blocks |
|---|---|---|---|
| **Product** | — | — | Design, Architecture, Content, GTM, Development |
| **Architecture** | Product | PRD with tenant model, permission matrix, audit requirements, NFRs (isolation latency, scale targets) | Development, Security, DevOps, QA Planning |
| **Security** | Product + Architecture | Tenant isolation approach, permission model, audit logging plan | Development (for audit implementation), QA Planning (for test scenarios) |
| **Design** | Product | Tenant model, workspace structure, role definitions from PRD | Development (frontend), Research (usability testing) |
| **Research** | Design | Workspace switcher mockups, tenant admin dashboard wireframes | GTM (early adopter feedback → positioning), Design refinement |
| **Development** | Architecture + Security | Data model, API contracts, isolation enforcement approach, audit logging spec | QA Execution, DevOps, Content |
| **QA Planning** | Architecture + Product + Security | Isolation strategy, permission matrix, audit requirements, acceptance criteria | QA Execution (test cases) |
| **QA Execution** | Development + QA Planning | Working implementation, test plan | Launch gate |
| **DevOps** | Architecture | Tenant provisioning logic, backup strategy, monitoring requirements | Launch gate |
| **Content** | Development + QA | Working features to screenshot, documented behaviors, known issues | GTM, Support, Launch gate |
| **GTM** | Product + Design + Research | Tenant model positioning, UX validation, early adopter feedback | Launch preparation, Sales materials |
| **Support** | Content + QA | Documented features, known issues, troubleshooting guides | Launch gate |

## Execution Sequence

| Phase | Workstreams (parallel) | Duration | Gate to next phase |
|---|---|---|---|
| **1 — Define & Design Systems** | Product, Architecture, Security | 2 weeks | PRD approved by CPO; architecture reviewed and signed off by CTO; threat model reviewed; no major isolation unknowns remaining |
| **2 — Design UX & Validate** | Design, Research, (Product refinement as needed) | 1–2 weeks | Workspace switcher and tenant admin UX flows signed off; early adopter feedback integrated; no usability blockers identified |
| **3 — Build Core Auth & Data Layer** | Development (backend), QA Planning, DevOps design | 2–3 weeks | Tenant-aware auth system complete and isolated; core data layer routing working; isolation tests passing for existing endpoints; provisioning automation designed |
| **4 — Build Feature Complete** | Development (backend + frontend), QA Execution, DevOps setup, Data pipeline | 3–4 weeks | All acceptance tests passing; UI complete and integrated; audit logging working; billing integration tested; DevOps monitoring in place |
| **5 — Prepare Launch & Compliance** | Content, GTM, Support training, QA final sweep, Security audit | 1–2 weeks | Docs complete and reviewed; support trained and confident; GTM ready; all compliance requirements verified; security audit complete with no blockers; known issues list finalized |
| **6 — Launch to Early Adopters** | Coordinated release, Sales handoff, Support on-call | 1–2 weeks | Deployed to staging with full tenant isolation verified; early adopter accounts created; sales begins proof-of-concept conversations; post-launch monitoring active |

### Critical Path

**Product → Architecture → Development (backend) → QA Execution → Launch**

This is the bottleneck. Decisions in Product cascade through Architecture, which blocks Development. QA cannot start until Development is substantial. Total: ~10–12 weeks.

### Parallel Opportunities

- **Design & Research** run in parallel with Architecture/Security (no dependencies between them)
- **Security & Architecture** design concurrently (share design but independent efforts)
- **DevOps design** starts in Phase 1 with Architecture; implementation happens in Phase 4
- **GTM & Content** can start early drafts once Design is complete; final versions wait for Development
- **QA Planning** happens in Phase 1 with Architecture; execution doesn't start until Development is substantial

## Summary

| Workstream | Owner | Depends on | Key deliverables | Phase | Estimated effort |
|---|---|---|---|---|---|
| **Product** | product-owner | — | PRD, user stories, permission matrix, acceptance criteria | 1 | 1–2 weeks |
| **Architecture** | architect | Product | System design doc, data model, API contracts, isolation strategy ADR, policy enforcement spec | 1 | 2–3 weeks |
| **Security** | security-engineer | Product, Architecture | Threat model, isolation breach scenarios, audit logging design, compliance checklist | 1 | 1–2 weeks |
| **Design** | ui-designer | Product | Workspace switcher comps, tenant admin dashboard, role assignment flows, mobile responsive designs | 2 | 2–3 weeks |
| **Research** | ux-researcher | Design | Usability test report, early adopter feedback, UX refinement recommendations | 2 | 1 week |
| **Development** | senior-backend + senior-frontend | Architecture, Security | Tenant auth system, data isolation layer, API endpoints, frontend components, billing integration | 3–4 | 6–8 weeks |
| **QA Planning** | qa-lead | Architecture, Product, Security | Test strategy, isolation test cases, permission matrix tests, compliance scenarios | 1–2 | 1 week |
| **QA Execution** | qa-engineer | Development, QA Planning | Automated test suite, isolation breach reports, permission audit, compliance verification | 4–5 | 2–3 weeks |
| **DevOps** | devops | Architecture | Tenant provisioning automation, backup/restore strategy, monitoring design, audit log infrastructure, production readiness | 1–4 | 2–3 weeks |
| **Content** | user-docs-writer | Development, QA | Admin guide, audit logging docs, SCIM provisioning guide, compliance attestation, FAQ, migration guide | 5 | 2–3 weeks |
| **GTM** | gtm | Product, Design, Research | Positioning doc, case studies, sales collateral, ROI calculator, competitive comparison | 2–5 | 2 weeks |
| **Support** | support | Content, QA | Admin troubleshooting guide, escalation procedures, training materials | 5 | 1 week |

### Timeline Estimate

- **Best case** (no blockers, parallel execution, early decisions): **9–10 weeks**
- **Likely case** (one architecture pivot, design feedback loop, compliance delays): **11–13 weeks**
- **Risk factors**:
  - Isolation strategy complexity (if row-level security proves insufficient, must pivot to schema/database isolation) — adds 1–2 weeks
  - Billing integration scope creep (per-tenant feature flags, tiered pricing) — adds 1 week
  - Compliance requirements change during QA — adds 1 week
  - Security audit finds isolation breach — adds 1–2 weeks rework
  - Early adopter migration complexity — does not block launch but may delay deals

## Follow-ups

- [ ] Schedule 3 amigos kickoff with Product Owner (CPO), Architect (CTO), and QA Lead to align on Phase 1 gate criteria
- [ ] Define OKRs for this initiative using `/coordinator:define-okrs` — success metrics beyond deal closure (NPS from early adopters, time-to-value for tenant admins, zero isolation breaches in first 6 months)
- [ ] Create detailed specs for each Phase workstream (Product first; Architecture second) — use `/coordinator:write-spec` for at least the tenant isolation strategy
- [ ] Identify and reserve the 6–8 week Development capacity now; this is the critical path blocker
- [ ] Schedule Security threat modeling workshop (Architecture + Security) before Phase 2 to catch isolation risks early
- [ ] Begin early adopter recruitment in parallel with Phase 1 (will need them in Phase 2 for Research)

---

**Assumptions made:**

1. Existing auth system exists; we're adding tenant-awareness, not building from scratch
2. Database is relational (SQL); isolation handled via row-level security, schema-based, or database-per-tenant (trade-offs to be analyzed)
3. Billing system exists and can be extended for per-tenant usage tracking
4. Single deployment model (all tenants on shared infrastructure, not isolated environments)
5. Early adopters are committed and available for feedback throughout phases 2–6
6. No real-time collaboration features complicating multi-tenant isolation
7. Existing single-tenant customers can be migrated or run as a "default tenant" with backward compatibility
8. Security audit and compliance verification (SOC 2, GDPR) can happen in parallel with development

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/17.0 (94%) |
| Evaluated | 2026-05-04 |
| Target duration | 85751 ms |
| Target cost | $0.1262 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Coordinator decomposes into workstreams that map to specific agents (architect for data isolation, CPO for pricing, developer for implementation, etc.) | PASS | The output explicitly maps every workstream to a named role: product-owner, ui-designer, user-docs-writer, gtm, support, ux-researcher, architect, senior-backend-engineer, senior-frontend-engineer, qa-lead, qa-engineer, devops, security-engineer, data-engineer. The Summary table repeats the Owner column for each row. |
| c2 | Dependencies between workstreams are identified and sequenced (e.g., data isolation design before implementation, pricing before billing) | PASS | A dedicated "Dependencies" table lists each workstream alongside "Depends on" and "Blocks" columns. For example: Architecture depends on Product and blocks Development, Security, DevOps, QA Planning; Development depends on Architecture + Security and blocks QA Execution, DevOps, Content. |
| c3 | Both CPO and CTO workstreams are present — this is not purely technical (pricing, documentation, UX are product concerns) | PASS | Output is explicitly split into a "CPO Team" section (Product, Design, Content, GTM, Support, Research) and a "CTO Team" section (Architecture, Development, QA Planning, QA Execution, DevOps, Security, Data). Pricing model and documentation are assigned to Product and Content under CPO. |
| c4 | The decomposition includes effort estimates or sizing signals for each workstream | PASS | The Summary table contains an "Estimated effort" column with ranges for every workstream: Product (1–2 weeks), Architecture (2–3 weeks), Security (1–2 weeks), Design (2–3 weeks), Research (1 week), Development (6–8 weeks), QA Planning (1 week), QA Execution (2–3 weeks), DevOps (2–3 weeks), Content (2–3 weeks), GTM (2 weeks), Support (1 week). |
| c5 | A critical path is identified — which workstreams block everything else | PASS | Under "Critical Path": "Product → Architecture → Development (backend) → QA Execution → Launch" with the explanation "Decisions in Product cascade through Architecture, which blocks Development. QA cannot start until Development is substantial. Total: ~10–12 weeks." |
| c6 | Revenue context ($400k ARR) is used to inform priority and timeline, not just mentioned | PARTIAL | The $400k ARR is cited in the context table and used to label the work "deal-blocking and revenue-critical" with a 10–12 week appetite and "High priority for CTO and CPO teams." This goes beyond a single mention, but the ceiling is PARTIAL and the connection to a specific calendar quarter or deadline date is absent. |
| c7 | Security implications of multi-tenancy are called out as a specific workstream or constraint | PASS | Security is a named workstream in the CTO Team table with owner security-engineer. Its deliverables include: threat model, cross-tenant data access scenarios, permission bypass vectors, audit logging integrity, secrets leakage, GDPR compliance, isolation breach detection and remediation, and penetration testing. |
| c8 | The output is a dispatch plan, not implementation — the coordinator doesn't write code or specs | PASS | The output contains workstream tables, dependency maps, phase gates, effort estimates, and follow-up actions. There is no code, no schema definitions, no SQL, and no implementation specifications anywhere in the response. |
| c9 | Output's workstreams cover at minimum: data isolation (architect / data engineer), auth and permissions (architect / security), billing changes (CPO + finance), UI workspace switching (UX + UI designer + developer), documentation (technical writer), pricing model (CPO + GTM) | PASS | Data isolation: Architecture workstream (isolation strategy ADR). Auth/permissions: Architecture + Security workstreams. Billing: Development (billing integration) + Product (seat/billing model) + GTM. UI workspace switching: Design (workspace switcher comps) + Development (frontend). Documentation: Content workstream (user-docs-writer). Pricing model: Product workstream (seat/user allocation model) + GTM (ROI calculator, positioning). |
| c10 | Output's dependency map shows that data isolation design must complete before implementation, that pricing decisions must inform billing implementation, and that auth/permissions design feeds the UI workspace switching | PASS | Dependencies table: Development depends on Architecture + Security (data isolation and auth/permissions design before implementation). Design depends on Product (pricing/workspace model informs UI). Development's billing integration listed under deliverables only after Architecture + Security sign-off. Auth/permissions design via Architecture is listed as prerequisite to Development, which includes the frontend workspace switcher. |
| c11 | Output identifies the critical path — likely data isolation design → auth/permissions design → implementation → migration of existing customers — and names what blocks what | PASS | Critical path explicitly stated: "Product → Architecture → Development (backend) → QA Execution → Launch" with blocking relationships described. Note: migration is not placed on the critical path explicitly (it appears in Assumptions and risk factors instead), but the blocking chain is clearly named. |
| c12 | Output uses the $400k ARR context to inform priority — connecting the dollar value to a target delivery date or quarter, not just citing the figure once | PARTIAL | The output uses the $400k ARR to justify a 10–12 week appetite and describe the initiative as "deal-blocking and revenue-critical" with "High priority." However, it does not connect the dollar value to a specific calendar date or quarter (e.g. "must ship by Q3 2026 to close these deals"). The ARR informs urgency but stops short of a time-bound commitment tied to the revenue figure. |
| c13 | Output flags multi-tenancy security as a distinct workstream — covering tenant isolation, blast-radius if one tenant is compromised, and customer-level encryption keys / data sovereignty options | PASS | Security is a named CTO workstream. It covers tenant isolation (cross-tenant data access scenarios), isolation breach detection and remediation (blast-radius equivalent), GDPR data deletion per tenant and compliance (data sovereignty), and secrets per-tenant in DevOps (API keys, webhook tokens). Customer-level encryption keys are not named explicitly but secrets-per-tenant and compliance requirements cover the intent. |
| c14 | Output includes effort estimates per workstream as ranges (e.g. "data isolation design: 2-3 weeks", "billing changes: 4-6 weeks") — not single-point estimates that imply false precision | PASS | Every row in the Summary table has a range in the "Estimated effort" column: e.g. Architecture (2–3 weeks), Development (6–8 weeks), QA Execution (2–3 weeks), DevOps (2–3 weeks). No single-point estimates are used. |
| c15 | Output is a dispatch plan — names the agent or role per workstream, the deliverable per workstream, and the entry/exit criteria — does NOT contain code, schema definitions, or implementation specs | PASS | Each workstream has a named owner role, specific deliverables, and the Execution Sequence table includes a "Gate to next phase" column (entry/exit criteria per phase). No code, schema, SQL, or implementation specs appear anywhere in the output. |
| c16 | Output covers BOTH CPO (pricing model, packaging tiers, GTM messaging, customer comms for existing customers) AND CTO (data, auth, infra) workstreams — multi-tenancy is not purely technical | PASS | CPO section includes: Product (seat/pricing model, permission matrix), Design (UX), GTM (positioning, ROI calculator, competitive comparison), Content (migration guide, compliance attestation, customer comms), Support, Research. CTO section includes: Architecture, Development, QA Planning, QA Execution, DevOps, Security, Data. Both dimensions are substantively represented. |
| c17 | Output addresses migration of existing single-tenant customers as a workstream — they need to be moved into the new model without disruption, and this typically blocks final cutover | PARTIAL | Migration is acknowledged in Assumption 7 ("migrated or run as a 'default tenant'"), as a Content deliverable ("migration guide for existing customers"), as a Constraint ("backward compatibility"), and as a risk factor ("Early adopter migration complexity — does not block launch but may delay deals"). However, migration is not a distinct workstream with its own owner, dependencies, phase assignment, or entry/exit gate. The criterion specifically asks for it as a workstream that blocks final cutover. |
| c18 | Output identifies parallel opportunities — e.g. UX research on workspace switching can run while data isolation is being designed, technical-writer documentation drafting can run alongside implementation | PARTIAL | A dedicated "Parallel Opportunities" section lists: Design & Research run in parallel with Architecture/Security; Security & Architecture design concurrently; DevOps design starts in Phase 1; GTM & Content can start early drafts once Design is complete; QA Planning happens in Phase 1 alongside Architecture. Both specific examples the criterion names (UX research while isolation is designed; docs alongside implementation) are covered. |

### Notes

The output is an exceptionally thorough dispatch plan that covers all major workstream categories, maps every workstream to a named role, provides ranged effort estimates, identifies the critical path, and explicitly calls out parallel opportunities. The two main gaps are: (1) c12 — the $400k ARR is used to justify urgency and a 10–12 week appetite but is never connected to a specific calendar delivery target (quarter or date), and (2) c17 — migration of existing single-tenant customers is acknowledged in assumptions, constraints, content deliverables, and risk factors, but never elevated to a standalone workstream with its own owner and gate criteria. The output avoids all implementation detail (no code, no schema) and stays firmly in dispatch-plan territory. The security workstream is detailed and substantive. The CPO/CTO split is clean and explicit. The dependency table is the strongest element, clearly showing what blocks what across all 12 workstreams.
