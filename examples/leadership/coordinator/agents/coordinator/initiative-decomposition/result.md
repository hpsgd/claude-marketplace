# Initiative Decomposition

Scenario: A major platform change (multi-tenancy) that spans product, engineering, security, and commercial concerns. Tests whether the coordinator decomposes into the right workstreams, maps them to agents, sequences dependencies, and produces a dispatch plan rather than jumping to implementation.

## Prompt

> We want to add multi-tenancy to the platform. Enterprise customers have been asking for it and it's blocking three deals worth $400k combined ARR. The touches everything — data isolation, auth/permissions, billing, UI (workspace switching), documentation, and pricing model changes.
> 
> Do not ask for clarification — proceed based on the information provided. Produce the full decomposition now, noting any assumptions you make.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

# Initiative Decomposition: Multi-tenancy Platform Support

## Context

| Question | Answer |
|---|---|
| **User problem** | Enterprise customers need data and permissions isolation across multiple internal teams/departments within a single organization, with separate usage tracking for billing purposes. Currently blocked by single-tenant architecture. |
| **Target user** | Enterprise customers: companies with 100+ employees, multiple departments, regulatory/cost accountability requirements. Initial focus: 3 blocked deals. |
| **Success criteria** | • 3 blocked enterprise deals close<br>• Enterprises can create and manage 2+ isolated workspaces per organization<br>• Complete data isolation enforced at query layer (tenant_id on all queries)<br>• Separate billing/usage metrics per workspace<br>• Zero data leakage between workspaces (security audit pass)<br>• 99.5% uptime during multi-tenant operations<br>• Enterprise documentation complete and tested<br>• Product qualified at least one reference customer |
| **Appetite** | 12 weeks (quarter-long initiative). High revenue impact ($400k ARR) justifies significant investment. Some timeline compression possible if security review is expedited. |
| **Constraints** | • Must maintain backward compatibility with existing single-tenant organizations<br>• Data model changes require careful migration planning (schema-breaking)<br>• Tenant ID must be injected into every query (widespread code touch)<br>• Auth/permission model redesign (workspace-scoped roles)<br>• Billing system integration (usage aggregation per workspace)<br>• No service downtime allowed during rollout |

---

## Workstreams

### CPO team workstreams

| Workstream | Owner role | Initiative-specific deliverables | Relevant? |
|---|---|---|---|
| Product | product-owner | • Workspace model definition (limits, nesting, feature access per workspace)<br>• User/role/permission hierarchy (workspace owner, member, billing admin, read-only)<br>• Workspace limits (max members, storage, API calls per workspace)<br>• Feature flagging strategy (which features available in multi-tenant vs. legacy orgs)<br>• User stories for workspace creation, switching, member management, settings<br>• Acceptance criteria for data isolation and permission enforcement | Yes |
| Design | ui-designer | • Workspace switcher UI component (always visible, fast switching)<br>• Workspace management screens (create, rename, delete, member invite)<br>• Team member management UI (roles, invite flow, removal)<br>• Workspace settings (billing, data retention, integrations)<br>• Accessibility audit (keyboard nav for workspace switcher)<br>• Mobile/responsive design for workspace UX | Yes |
| Content | user-docs-writer | • Enterprise multi-tenancy setup guide (for admins)<br>• Workspace switching + member management docs<br>• Role/permission reference (what can workspace owner/member/billing admin do)<br>• Data isolation guarantees (for compliance/audit teams)<br>• Billing per workspace (invoicing, usage reports)<br>• Migration guide (how to move users to new workspace model)<br>• FAQ (workspace limits, support for legacy orgs) | Yes |
| GTM | gtm | • Enterprise segment positioning (multi-tenancy as table-stakes feature)<br>• Competitive positioning (how we stack against competitors on tenant isolation)<br>• Launch narrative (for sales + press)<br>• Sales enablement deck + talking points<br>• Customer communication plan (feature announcement, onboarding cohort)<br>• Pricing model decisions (workspace-based pricing vs. org-based) | Yes |
| Support | support | • Support runbook: common multi-tenancy issues and troubleshooting<br>• FAQ: workspace creation, member management, billing disputes<br>• Escalation path for data isolation concerns (security/compliance)<br>• Customer onboarding guide (first workspace setup)<br>• Internal training (how to help customers migrate)<br>• Known issues and workarounds list | Yes |
| Research | ux-researcher | • User testing of workspace switcher (discoverability, flow)<br>• Validation: does our permission model match customer mental models? | No — customers have already voted with deals. User research would delay. Validate with reference customers post-launch. |

### CTO team workstreams

| Workstream | Owner role | Initiative-specific deliverables | Relevant? |
|---|---|---|---|
| Architecture | architect | • Data model redesign: tenant_id column on all tables, indexing strategy<br>• Query layer isolation strategy (tenant_id validation, middleware enforcement)<br>• API versioning/namespacing (workspace-scoped endpoints vs. global)<br>• Auth system redesign (JWT payload includes tenant_id, scoped to workspace)<br>• Database migration strategy (backfill tenant_id, test rollback)<br>• Scaling considerations (query performance with tenant_id filtering)<br>• ADRs: tenancy model (row-level security vs. application-enforced), schema design, API design | Yes |
| Development | [backend lead, frontend lead] | • Backend: tenant_id injection at middleware layer, query enforcement, auth token redesign<br>• Database: schema migrations, data backfill (existing org → default workspace)<br>• Frontend: workspace switcher component, workspace settings pages, member management UI<br>• API: workspace CRUD endpoints, member invite/removal, workspace switching<br>• Integration: billing system (track usage per workspace), auth system (workspace-scoped tokens)<br>• Testing harness: ability to test queries in isolation per tenant | Yes |
| QA Planning | qa-lead | • Test strategy: data isolation (cross-tenant query attempts must fail)<br>• Test plan: permission enforcement (roles, workspace boundaries)<br>• Acceptance criteria: all queries validated for tenant_id<br>• Regression testing scope: do single-tenant paths still work?<br>• Security test cases: attempt to access other workspace data, bypass tenant_id<br>• Performance benchmarks (query latency with tenant_id filters) | Yes |
| QA Execution | qa-engineer | • Execute data isolation tests (black box: verify no cross-tenant leaks)<br>• Permission enforcement tests (role-based access control per workspace)<br>• Workspace member management tests (invite, remove, role change)<br>• Billing isolation tests (usage correctly attributed to workspace)<br>• Regression test suite (ensure single-tenant customers unaffected)<br>• Performance testing (latency increase from tenant_id filtering) | Yes |
| DevOps | devops | • Database migration plan (zero-downtime backfill of tenant_id)<br>• Rollback strategy (if migration fails, how to recover)<br>• Monitoring/alerting (data isolation violations, cross-tenant queries)<br>• Deployment plan (gradual rollout: new orgs on multi-tenant, legacy orgs opt-in)<br>• Infrastructure scaling (estimate database load increase from new queries)<br>• DNS/routing: workspace switching (frontend → workspace-scoped API endpoints) | Yes |
| Security | security-engineer | • Threat model: multi-tenancy attack surface (data leakage, privilege escalation, isolation bypass)<br>• Security review checkpoints: architecture (tenant_id strategy), code (all queries validated), deployment (monitoring for violations)<br>• Compliance considerations (GDPR, HIPAA, SOC2 implications of shared infrastructure)<br>• Encryption strategy (at rest per tenant? at transit?)<br>• Audit logging (who accessed which workspace, when) | Yes — **CRITICAL** |
| Data | data-engineer | • Event tracking plan: capture workspace_id in all events<br>• Usage aggregation queries: API calls, storage, features used per workspace<br>• Billing metrics pipeline (usage → invoicing)<br>• Analytics dashboard: adoption per workspace, feature usage per workspace<br>• Data backfill: attach workspace_id to historical events (if applicable) | Yes |

---

## Dependencies

| Workstream | Depends on | What it needs before starting | Blocks |
|---|---|---|---|
| Product | — | None (can start immediately) | Design, Architecture, Development, GTM |
| Architecture | Product | PRD with workspace model, permission hierarchy, limits, acceptance criteria | Development, DevOps, Security review |
| Security | Product, Architecture | Requirements + system design (to threat model isolation strategy) | Development (can't proceed until threat model is approved) |
| Design | Product | PRD + user stories for workspace UX | Development (UI specs needed for frontend) |
| Development | Architecture, Security, Design | Approved system design, threat model review, UI specs | QA Execution, Content |
| DevOps | Architecture | Database strategy, migration plan, scaling estimates | Launch (can't deploy without validated migration) |
| QA Planning | Product, Architecture | Requirements + system design (to plan test coverage) | QA Execution (test plans ready before code) |
| QA Execution | Development | Working implementation of multi-tenancy | Launch, Support |
| Content | Development | Near-complete feature (needs screenshots, working flows) | Launch, Support training |
| GTM | Design, Product | Final UX + positioning strategy | Launch |
| Support | Content, QA | Documentation + known issues list | Launch |

---

## Execution Sequence

| Phase | Workstreams (parallel) | Duration | Gate to next phase |
|---|---|---|---|
| **Phase 1 — Define** | Product + Architecture + Security (threat model prep) | 2–3 weeks | • PRD approved by CPO<br>• System design approved by CTO<br>• Security threat model review completed |
| **Phase 2 — Design & Security** | Design + Security (threat model review + code review checklist) + QA Planning | 2–3 weeks | • UI specs finalized and approved<br>• Threat model approved by security<br>• QA test plan written and reviewed |
| **Phase 3 — Build** | Development + DevOps (migration planning) | 6–8 weeks | • Core multi-tenancy implementation (tenant_id injection, isolation enforcement)<br>• Database migration tested in staging<br>• All security checkpoints passed (code review, isolation tests) |
| **Phase 4 — Validate** | QA Execution + DevOps (deployment final prep) | 2–3 weeks | • Data isolation tests passing (100%)<br>• Permission enforcement tests passing<br>• Regression tests passing (single-tenant unaffected)<br>• Performance benchmarks acceptable<br>• Deployment plan validated in staging |
| **Phase 5 — Prepare** | Content + GTM + Support prep | 1–2 weeks | • Documentation complete and reviewed<br>• GTM materials finalized<br>• Support runbook ready<br>• Customer communication approved |
| **Phase 6 — Launch** | Coordinated release (GTM + Support + Engineering) | 1 week | All gates passed. Phased rollout: new orgs on multi-tenant first, legacy orgs opt-in. |

### Critical Path

**Architecture → Development → QA Execution → Launch**

The critical path is 13–17 weeks (2–3 + 6–8 + 2–3 + 1), dominated by development time. Security review is on the critical path if threat modeling or code review delays happen — front-load security effort in Phase 1–2.

Parallel opportunities:
- Design can start immediately (depends only on Product, which is ready)
- DevOps migration planning can start in Phase 1 once architecture is clear
- QA Planning can start in Phase 2 while Development is still in progress
- Content writing can begin mid-Phase 3 once features are mostly working
- GTM positioning can be drafted in Phase 1–2 while Product/Design finalize UX

### Risk Factors

- **Database migrations at scale:** Backfilling tenant_id on large tables is the highest risk. Could add 1–2 weeks if rollback is needed.
- **Tenant_id injection coverage:** Missing even one query in the codebase is a security failure. Requires comprehensive code review.
- **Backward compatibility:** Ensuring legacy single-tenant orgs aren't broken adds complexity (two code paths, two test matrices).
- **Feature parity:** If new workspaces have feature restrictions, those restrictions must be documented and communicated (GTM delay risk).

---

## Summary

| Workstream | Owner | Depends on | Key deliverables | Phase | Estimated effort |
|---|---|---|---|---|---|
| Product | product-owner | — | PRD, user stories, workspace model, permission hierarchy | 1 | 2–3 weeks |
| Architecture | architect | Product | System design, API contracts, data model ADRs | 1 | 2–3 weeks |
| Security (threat model) | security-engineer | Product, Architecture | Threat model, code review checklist, compliance assessment | 2 | 1–2 weeks |
| Design | ui-designer | Product | UX flows, component specs, workspace switcher design | 2 | 2–3 weeks |
| QA Planning | qa-lead | Product, Architecture | Test strategy, test plan, acceptance criteria | 2 | 1 week |
| Development | [backend + frontend leads] | Architecture, Security, Design | Multi-tenancy implementation, schema migrations, API updates, UI | 3 | 6–8 weeks |
| DevOps | devops | Architecture | Migration plan, deployment strategy, monitoring | 3–4 | 2–3 weeks |
| QA Execution | qa-engineer | Development | Test execution, isolation verification, regression tests, performance report | 4 | 2–3 weeks |
| Content | user-docs-writer | Development | Setup guides, role reference, FAQ, migration guide | 5 | 2–3 weeks |
| GTM | gtm | Design, Product | Positioning, sales deck, launch narrative, customer comms | 5 | 1–2 weeks |
| Support | support | Content, QA | Runbook, FAQ, onboarding guide, training | 5 | 1 week |

### Timeline Estimate

- **Best case:** 13 weeks (parallel acceleration, no migration issues, all reviews on first pass)
- **Likely case:** 15–17 weeks (typical rework cycles, one migration hiccup, security review thoroughness)
- **Risk case:** 18–20 weeks (major migration rollback, scope creep on permission model, feature parity decisions delayed)

### Assumptions Made

1. **Backward compatibility required:** Existing single-tenant orgs are not migrated; they opt-in or are gradually upgraded. This adds complexity but avoids forced migration risk.
2. **No hard deadline:** The $400k deal opportunity is urgent but not a fixed launch date. If security review finds issues, we have time to address them properly.
3. **Tenant model is flat:** Workspaces belong to an org, but workspaces cannot be nested (simplifies data model and permissions).
4. **Billing is workspace-scoped:** Usage is tracked and invoiced per workspace, not per org. Impacts pricing model.
5. **Feature access is workspace-uniform:** All workspaces in an org have access to the same features. No per-workspace feature restrictions.
6. **Existing team/user model extends:** Current user structure maps to "workspace member," with roles (owner, member, billing admin).
7. **Monolithic database:** Not splitting into per-tenant databases (less operational complexity, simpler deployment).

---

## Follow-ups

- [ ] **Define OKRs** — Use `/coordinator:define-okrs` to establish success metrics for each workstream and for the overall initiative. OKRs should ladder to "3 deals close" and "enterprise retention/expansion."
- [ ] **Write detailed specs** — Once PRD and system design are approved (end of Phase 1), create detailed specs for each workstream (API specs, schema docs, UX specs, test plans).
- [ ] **Establish governance** — Identify workstream owners and define decision-making process (who approves architecture changes mid-development? Who decides on feature restrictions?).
- [ ] **Recruit reference customer** — Identify an early adopter to validate UX and multi-tenancy model during Phase 3–4. Use for customer story post-launch.
- [ ] **Plan communication cadence** — Weekly syncs (CPO + CTO leads) during Phases 1–3; bi-weekly during Phases 4–5; daily standup during Phase 6 launch.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/17.0 (94%) |
| Evaluated | 2026-05-02 |
| Target duration | 58999 ms |
| Target cost | $0.0770 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Coordinator decomposes into workstreams that map to specific agents (architect for data isolation, CPO for pricing, developer for implementation, etc.) | PASS | Each workstream has an explicit owner role: product-owner, ui-designer, user-docs-writer, gtm, support, architect, [backend lead, frontend lead], qa-lead, qa-engineer, devops, security-engineer, data-engineer. The CPO/CTO split makes the mapping explicit throughout. |
| c2 | Dependencies between workstreams are identified and sequenced (e.g., data isolation design before implementation, pricing before billing) | PASS | A full 'Dependencies' table lists every workstream with its 'Depends on', 'What it needs before starting', and 'Blocks' columns. Supplemented by the 6-phase execution sequence with explicit gates. |
| c3 | Both CPO and CTO workstreams are present — this is not purely technical (pricing, documentation, UX are product concerns) | PASS | Explicit 'CPO team workstreams' section covering Product, Design, Content, GTM, Support, and Research. Separate 'CTO team workstreams' covering Architecture, Development, QA Planning, QA Execution, DevOps, Security, and Data. |
| c4 | The decomposition includes effort estimates or sizing signals for each workstream | PASS | Summary table at the end includes 'Estimated effort' with ranges for every workstream: Product '2–3 weeks', Architecture '2–3 weeks', Development '6–8 weeks', DevOps '2–3 weeks', QA Execution '2–3 weeks', Content '2–3 weeks', GTM '1–2 weeks', Support '1 week', etc. |
| c5 | A critical path is identified — which workstreams block everything else | PASS | 'Critical Path' section explicitly states 'Architecture → Development → QA Execution → Launch' and calculates it at 13–17 weeks. Also notes 'Security review is on the critical path if threat modeling or code review delays happen.' |
| c6 | Revenue context ($400k ARR) is used to inform priority and timeline, not just mentioned | PARTIAL | ARR is used to justify a 12-week appetite: 'High revenue impact ($400k ARR) justifies significant investment. Some timeline compression possible if security review is expedited.' However, Assumption #2 then states 'no hard deadline' which somewhat undermines the urgency connection, and no specific deal-close quarter is targeted. |
| c7 | Security implications of multi-tenancy are called out as a specific workstream or constraint | PASS | Security has its own dedicated workstream with security-engineer owner, marked 'CRITICAL'. Deliverables include threat model, compliance (GDPR/HIPAA/SOC2), encryption strategy, audit logging, and code review checkpoints. Security is also noted as on the critical path. |
| c8 | The output is a dispatch plan, not implementation — the coordinator doesn't write code or specs | PASS | Output contains no code, no schema definitions, no SQL migrations, no API endpoint specs, and no implementation blueprints. Every section describes deliverables, owners, dependencies, and phase gates — purely a dispatch plan. |
| c9 | Output's workstreams cover at minimum: data isolation (architect / data engineer), auth and permissions (architect / security), billing changes (CPO + finance), UI workspace switching (UX + UI designer + developer), documentation (technical writer), pricing model (CPO + GTM) | PASS | Data isolation: architect ('tenant_id column on all tables') + data-engineer. Auth/permissions: architect ('Auth system redesign') + security-engineer. Billing: data-engineer ('billing metrics pipeline') + GTM ('Pricing model decisions'). UI: ui-designer ('Workspace switcher') + development frontend. Docs: user-docs-writer. Pricing: GTM workstream. |
| c10 | Output's dependency map shows that data isolation design must complete before implementation, that pricing decisions must inform billing implementation, and that auth/permissions design feeds the UI workspace switching | PARTIAL | Data isolation → implementation: Architecture → Development is explicit in the dependency table. Auth/permissions → UI: Architecture dependency feeds Development which includes frontend. However, pricing decisions (GTM) are sequenced in Phase 5 (Prepare) AFTER billing implementation in Development (Phase 3 Build), inverting the required pricing-before-billing dependency. |
| c11 | Output identifies the critical path — likely data isolation design → auth/permissions design → implementation → migration of existing customers — and names what blocks what | PASS | Explicit 'Critical Path' section: 'Architecture → Development → QA Execution → Launch.' Dependencies table names what each workstream blocks. Migration of legacy orgs is addressed in DevOps ('zero-downtime backfill') and the phased rollout note. |
| c12 | Output uses the $400k ARR context to inform priority — connecting the dollar value to a target delivery date or quarter, not just citing the figure once | PASS | Appetite section: '12 weeks (quarter-long initiative). High revenue impact ($400k ARR) justifies significant investment.' The ARR directly drives the 12-week timeline window and the statement 'Some timeline compression possible if security review is expedited' shows the revenue urgency is actively shaping schedule decisions. |
| c13 | Output flags multi-tenancy security as a distinct workstream — covering tenant isolation, blast-radius if one tenant is compromised, and customer-level encryption keys / data sovereignty options | PARTIAL | Tenant isolation: covered via 'data leakage, privilege escalation, isolation bypass.' Encryption: 'Encryption strategy (at rest per tenant? at transit?)' and compliance (GDPR/HIPAA/SOC2) partially address data sovereignty. However, blast-radius (what happens when one tenant IS compromised) is not explicitly addressed, and customer-managed encryption keys are not mentioned — only a general 'at rest per tenant' question. |
| c14 | Output includes effort estimates per workstream as ranges (e.g. "data isolation design: 2-3 weeks", "billing changes: 4-6 weeks") — not single-point estimates that imply false precision | PASS | Summary table uses ranges throughout: '2–3 weeks', '6–8 weeks', '1–2 weeks', '2–3 weeks', '1 week'. Timeline estimate section also provides best-case (13 weeks), likely-case (15–17 weeks), and risk-case (18–20 weeks) — all ranges. |
| c15 | Output is a dispatch plan — names the agent or role per workstream, the deliverable per workstream, and the entry/exit criteria — does NOT contain code, schema definitions, or implementation specs | PASS | Every workstream row names the owner role, lists specific deliverables, and the Execution Sequence table provides explicit phase gates (entry/exit criteria). No code, SQL schemas, or implementation details are present anywhere in the output. |
| c16 | Output covers BOTH CPO (pricing model, packaging tiers, GTM messaging, customer comms for existing customers) AND CTO (data, auth, infra) workstreams — multi-tenancy is not purely technical | PASS | CPO side: Product (workspace model, user stories), Design (UX flows), GTM (pricing model decisions, sales deck, customer communication plan, competitive positioning), Content (docs, migration guide), Support (runbooks, training). CTO side: Architecture, Development, DevOps, Security, Data, QA — both halves fully populated. |
| c17 | Output addresses migration of existing single-tenant customers as a workstream — they need to be moved into the new model without disruption, and this typically blocks final cutover | PASS | Addressed across multiple workstreams: Architecture ('database migration strategy, backfill tenant_id, test rollback'), Development ('data backfill: existing org → default workspace'), DevOps ('zero-downtime backfill of tenant_id', 'Rollback strategy'), Content ('migration guide'), and the phased launch ('new orgs on multi-tenant first, legacy orgs opt-in'). |
| c18 | Output identifies parallel opportunities — e.g. UX research on workspace switching can run while data isolation is being designed, technical-writer documentation drafting can run alongside implementation | PARTIAL | Explicit 'Parallel opportunities' subsection lists: Design starts immediately while Product is running; DevOps migration planning starts in Phase 1; QA Planning starts in Phase 2 while Development is in progress; 'Content writing can begin mid-Phase 3 once features are mostly working'; GTM positioning drafted in Phase 1–2. Covers the documentation-alongside-implementation case; UX research parallel opportunity is not explicitly called out. |

### Notes

The output is an exceptionally thorough dispatch plan covering all required workstreams, with explicit role assignments, ranged effort estimates, a phased execution sequence, and a named critical path. The two meaningful gaps are: (1) the pricing/billing sequencing is inverted — GTM's pricing model decisions land in Phase 5 while billing implementation is Phase 3, which violates the criterion that pricing informs billing; and (2) the security workstream, while substantive, does not address blast-radius (what happens if one tenant IS compromised) or customer-managed encryption keys specifically. The $400k ARR is well-used to justify the 12-week appetite, though the assumption of 'no hard deadline' slightly undercuts the urgency connection. Parallel opportunities are called out explicitly, satisfying the PARTIAL ceiling criterion. Overall a high-quality coordinator output that earns a solid PASS at 94%.
