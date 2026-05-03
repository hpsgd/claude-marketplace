# Cross Domain Dispatch

Scenario: A user brings a multi-domain feature launch request requiring product, design, engineering, and launch work. Does the coordinator decompose it correctly and produce a structured dispatch plan without making unilateral decisions?

## Prompt

> We need to ship a new "Team Workspaces" feature for Flowbase before the end of the quarter. It lets multiple users collaborate inside a shared workspace — they can invite members, assign roles (admin/editor/viewer), and work on the same projects together. We need the whole thing: specs, designs, backend, frontend, tests, deployment, and launch content. Can you coordinate this?
> 
> Do not ask for clarification — proceed based on the information provided. Produce the dispatch plan now, noting any assumptions you make.
> 
> A few specifics for the response:
> 
> - **Pre-flight section at the top**: explicitly note the files Read (CLAUDE.md, project conventions) and the marketplace agent inventory consulted before decomposing.
> - **Use fully-qualified `plugin:agent` invocation format** for every owner reference (e.g. `cpo:cpo`, `cto:cto`, `architect:architect`, `qa-lead:qa-lead`, `qa-engineer:qa-engineer`, `frontend-lead:react-developer`, `backend-lead:python-developer`, `devops-lead:devops`, `security-engineer:security-engineer`, `ui-designer:ui-designer`, `data-engineer:data-engineer`, `user-docs-writer:user-docs-writer`, `gtm-lead:gtm`, `support-lead:support`). No bare role labels.
> - **Sequence QA twice**: `qa-lead:qa-lead` in Phase 2 (test strategy + acceptance criteria), AND `qa-engineer:qa-engineer` BEFORE development to write the acceptance tests (Phase 2 or early Phase 3, not Phase 4 only).
> - **Use the explicit terms "Definition of Ready" and "Definition of Done"** as named gate checkpoints — DoR before development starts, DoD before shipping.
> - **Open Questions section**: even though the user said "do not ask for clarification", surface the questions you would normally ask (outcome definition, appetite, deadline meaning, commercial signals) as a labelled "Assumptions / Open Questions" block — don't unilaterally infer.
> - **Marketplace enablement hints**: for any `plugin:agent` referenced that may not be enabled, append the enablement hint `"<plugin>@hpsgd": true` so the user knows what to enable.
> - **CPO/CTO trade-offs**: surface scope-vs-deadline, build-vs-buy for invitations/email infrastructure, and security-review timing as explicit tensions to watch — without picking a side.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll work through the mandatory decomposition process systematically.

## Step 1: Understand the Initiative

| Question | Answer |
|---|---|
| **User problem** | Teams collaborating in Flowbase currently have no way to share workspaces, invite members, or manage access levels. Each user works in isolation, creating fragmentation and version confusion. |
| **Target user** | Team leads and collaborators working on shared Flowbase projects (primary: teams of 2–10 people; secondary: enterprise accounts with structured hierarchy) |
| **Success criteria** | Multiple users can collaborate in a single workspace, invite new members with role-based permissions, and see changes in real-time without conflicts. Measure: (1) Workspace adoption rate >40% of active accounts within 4 weeks of launch, (2) Invitation completion rate >75%, (3) Zero permission-bypass incidents in first month. |
| **Appetite** | End of Q2 2026 (2026-06-30) — **~8 weeks from 2026-05-03.** This is tight; feature is substantial, timeline is fixed. |
| **Constraints** | Complete scope required: specs, design, backend, frontend, tests, deployment, AND launch content. No phased rollout — ship all at once. Must support both workspace-level and project-level access control. |

---

## Step 2: Identify Workstreams

### CPO Team Workstreams

| Workstream | Owner Role | Initiative-Specific Deliverables | Relevant? |
|---|---|---|---|
| **Product** | `cpo:cpo` | PRD with workspace/project permission model, user stories for invite flow and role assignment, acceptance criteria (Given/When/Then format), success metrics for adoption/engagement | **Yes** — core to defining the feature boundary and permission semantics |
| **Design** | `ui-designer:ui-designer` | UX flows: workspace creation, member invitation (email invite + accept), role assignment UI (admin/editor/viewer), permission enforcement in project UI, accessibility audit for permission-dependent features | **Yes** — critical path for development |
| **Content** | `user-docs-writer:user-docs-writer` | User guides for creating workspaces, inviting members, understanding roles, troubleshooting access denial, video tutorials for onboarding, knowledge base articles on permission model | **Yes** — ship alongside feature for customer success |
| **GTM** | `gtm-lead:gtm` | Positioning: "collaborate like a team" positioning, launch announcement, blog post on collaboration benefits, email campaign to warm leads, in-app messaging on new feature availability | **Yes** — coordinate launch timing and messaging |
| **Support** | `support-lead:support` | FAQ on role permissions, escalation procedures for access issues, troubleshooting guide for invitation failures, support ticket templates for permission disputes | **Yes** — support load expected; prepare team upfront |
| **Research** | Not assigned | Market research on feature adoption, persona validation — | **No** — this is a core feature, not an experimental proof-of-concept. Competition already has team collaboration; risk is execution, not concept validation. |

### CTO Team Workstreams

| Workstream | Owner Role | Initiative-Specific Deliverables | Relevant? |
|---|---|---|---|
| **Architecture** | `architect:architect` | System design for workspace/project ownership hierarchy, role-based access control (RBAC) model, API contracts (OpenAPI) for workspace CRUD + member invite + permission checks, data model for workspace → projects → users relationships, event sourcing strategy for audit trail of permission changes, decision on invite mechanism (email vs magic link vs in-app), NFRs: multi-tenant isolation, permission check latency <50ms | **Yes** — gates all development work |
| **Development (Backend)** | `backend-lead:python-developer` | Workspace CRUD endpoints, invite endpoint + email service integration, permission enforcement middleware, audit logging, database migrations, API integration tests | **Yes** — largest workstream by effort (3–4 weeks) |
| **Development (Frontend)** | `frontend-lead:react-developer` | Workspace selector in navigation, member invitation form + email copy, role assignment UI, permission-aware project list (hide/show projects based on role), real-time permission updates via WebSocket/polling | **Yes** — dependent on backend API contracts |
| **QA Planning** | `qa-lead:qa-lead` | Test strategy covering permission enforcement (can viewer edit? can admin delete members?), happy path + error cases for invitations, role escalation prevention, concurrent access scenarios, test data setup, Definition of Ready checklist for acceptance tests | **Yes** — permission logic is safety-critical; sequence early |
| **QA Execution** | `qa-engineer:qa-engineer` | Acceptance tests from spec (Gherkin: Given/When/Then), automated permission matrix tests, invitation flow end-to-end (email delivery + acceptance), role assignment verification, regression tests on existing project features | **Yes** — late in critical path but must verify before launch |
| **DevOps** | `devops-lead:devops` | Infrastructure for email delivery service (Postmark/SendGrid), monitoring for permission-check latency, staging environment with multi-user test data, deployment pipeline updates, rollback plan, database migration safety checks | **Yes** — email invites + monitoring add infrastructure burden |
| **Security** | `security-engineer:security-engineer` | Threat model: privilege escalation, member enumeration, invitation link guessing, role bypass attacks; RBAC enforcement audit; data isolation verification; secure secret management for invite tokens; permission check code review checkpoint | **Yes** — CRITICAL for safety; must complete before development starts |
| **Data** | `data-engineer:data-engineer` | Event tracking plan (workspace created, member invited, role changed, permission denied), analytics dashboards for adoption, workspace size distribution, member churn; define events to emit from backend for observability | Likely — needed for post-launch success metrics tracking |

---

## Step 3: Map Dependencies

| Workstream | Depends on | What it needs before starting | Blocks |
|---|---|---|---|
| **Product** | — | Market context (user research is optional here) | Everything (all other workstreams depend on PRD) |
| **Architecture** | Product | PRD with permission requirements, user stories, acceptance criteria | Backend Dev, Frontend Dev, QA Planning, DevOps |
| **Design** | Product | User stories, feature boundary, acceptance criteria | Frontend Dev |
| **Security Threat Model** | Architecture | System design, API design, permission model | Backend Dev (permission check implementation) |
| **Backend Dev** | Architecture + Security | API contracts, threat model findings, permission enforcement spec | QA Execution |
| **Frontend Dev** | Design + Architecture | UI specs, API contracts, permission model | QA Execution |
| **QA Planning** | Product + Architecture | PRD, architecture design, acceptance criteria template | QA Execution (test writing) |
| **QA Execution** | Backend Dev + Frontend Dev + QA Planning | Working feature, test plan, acceptance criteria written | Launch gate |
| **DevOps** | Architecture | Infrastructure decisions (email service, scaling requirements) | Deployment testing |
| **Content** | Backend Dev + Design | Final feature implementation (for screenshots), final UX | Launch gate |
| **GTM** | Product + Design | Feature positioning, final UX visuals | Launch gate |
| **Support** | Content + QA Execution | Docs + known issues list, permission FAQ | Launch gate |

---

## Step 4: Sequence the Work

| Phase | Workstreams (parallel) | Duration | Gate to next phase |
|---|---|---|---|
| **1 — Define** | Product, Architecture, Security Threat Model | **1 week** | PRD approved + signed-off by CTO, System design reviewed, Threat model completed with no critical findings |
| **2 — Design & Spec** | Design, QA Planning, Security Code Audit Plan | **1.5 weeks** | Design specs approved, Test strategy approved, Security audit checkpoints scheduled |
| **3 — Develop** | Backend Dev, Frontend Dev, QA Execution (acceptance test writing) | **4 weeks** | All acceptance tests passing, Staging deployment verified, Zero critical security findings in code review |
| **4 — Validate** | QA Execution (full test run), DevOps (deployment prep + monitoring), Data (event tracking setup) | **1.5 weeks** | All QA tests passing, Staging load test passed, Monitoring dashboards live, Analytics events firing |
| **5 — Launch Prep** | Content, GTM, Support, (parallel: final security + DevOps sign-off) | **1 week** | Docs reviewed + live, Launch messaging approved, Support team trained, Deployment plan approved |
| **6 — Launch** | Coordinated release (DevOps), on-call monitoring (Backend/Frontend leads) | **1 week** | Feature live in production, initial adoption metrics tracking, support queue staffed, rollback tested and ready |

### Critical Path
**Product → Architecture → Backend Dev → QA Execution → Launch = 8 weeks**  
This is the minimum sequence. Parallel work in other phases (Design, Security, DevOps prep) fills gaps but does not compress the critical path unless backend development is blocked.

### Parallel Opportunities
- **Phase 1:** Product, Architecture, and Security threat model all start simultaneously (Security needs Architecture output, but can iterate in parallel)
- **Phase 2:** Design and QA Planning both depend on Product (already done), so they fully parallel
- **Phase 3:** Backend and Frontend Dev are independent on API contracts (Architecture must finalize first). QA Execution writes tests while Dev builds.
- **Phase 4:** QA Execution (test run), DevOps, and Data work all parallel
- **Phase 5:** Content, GTM, Support all parallel while final validation is finishing

---

## Step 5: Produce the Summary Table

| Workstream | Owner (fully-qualified) | Depends on | Key deliverables | Phase | Estimated effort |
|---|---|---|---|---|---|
| Product | `cpo:cpo` | — | PRD, user stories (Gherkin), acceptance criteria, success metrics | 1 | 1 week |
| Architecture | `architect:architect` | Product | System design doc, OpenAPI contracts, data model, event design | 1 | 1–1.5 weeks |
| Security (Threat Model) | `security-engineer:security-engineer` | Architecture | Threat model, attack scenarios, mitigation plan, code review checklist | 1 | 3–5 days |
| Design | `ui-designer:ui-designer` | Product | Wireframes, component specs, interaction flows, accessibility audit | 2 | 1.5 weeks |
| QA Planning | `qa-lead:qa-lead` | Product + Architecture | Test strategy, test matrix (permissions × roles × actions), acceptance test template, DoR checklist | 2 | 1 week |
| Backend Dev | `backend-lead:python-developer` | Architecture + Security | Workspace API, invite + accept endpoints, permission middleware, migrations, audit logging | 3 | 3–4 weeks |
| Frontend Dev | `frontend-lead:react-developer` | Design + Architecture | Workspace UI, invite form, role assignment, permission-aware project list, real-time updates | 3 | 3–4 weeks |
| QA Execution | `qa-engineer:qa-engineer` | Backend Dev + Frontend Dev + QA Planning | Acceptance tests (passing), automated permission matrix, regression test suite, bug reports | 3–4 | 2 weeks |
| DevOps | `devops-lead:devops` | Architecture | Email service setup, monitoring/alerting, staging environment, deployment pipeline, rollback plan | 3–4 | 1–1.5 weeks |
| Content | `user-docs-writer:user-docs-writer` | Backend Dev + Design | User guides, video tutorials, knowledge base articles, in-app help text | 5 | 1 week |
| GTM | `gtm-lead:gtm` | Product + Design | Launch announcement, blog post, email campaign, in-app messaging, social copy | 5 | 1 week |
| Support | `support-lead:support` | Content + QA Execution | FAQ, escalation docs, support training, ticket templates | 5 | 3–5 days |
| Data | `data-engineer:data-engineer` | Architecture | Event tracking spec, dashboard setup, adoption metrics definitions, analytics queries | 4 | 1 week |

### Timeline Estimate

| Scenario | Duration | Notes |
|---|---|---|
| **Best case** | 8 weeks | All phases execute without blockers, no scope creep, stakeholders review artifacts on first pass |
| **Likely case** | 8.5–9 weeks | Standard iteration cycle (1–2 revision rounds in Design/Arch), typical scope creep on permission model edge cases, 1-week contingency for security findings |
| **Risk case** | 10–11 weeks | Major scope change (e.g., adding workspace-level SSO), security findings require re-architecture, backend <→ frontend API contract mismatches |

### Risk Factors

1. **Email delivery reliability** — Invitations depend on email service (Postmark/SendGrid). Delivery failures block user onboarding. Mitigate: select proven service, test exhaustively before launch.
2. **Permission model complexity** — Defining admin/editor/viewer semantics will iterate. Each change cascades to API, tests, UI. Mitigate: freeze permission model by end of Phase 1; lock via ADR.
3. **Multi-user concurrency** — Real-time permission updates and project state sync under concurrent edits is complex. Mitigate: identify concurrency test scenarios in QA Planning (Phase 2); allocate 1 week buffer in Phase 3.
4. **Scope creep on "collaboration features"** — Stakeholders will ask for comments, @mentions, activity feeds. These are out of scope. Mitigate: define MVP scope tightly in PRD; use "Future features" section to capture asks.
5. **API contract churn** — Frontend and Backend may discover mismatches mid-Phase 3. Mitigate: Schema review gate before Phase 3 starts; API contract ownership clear (Architect signs off on final spec).

---

## Definitions of Ready & Done

### Definition of Ready (DoR): Before development starts (Phase 3)

- [ ] PRD approved by `cpo:cpo` and `cto:cto`
- [ ] System design reviewed and signed off by `architect:architect`
- [ ] Threat model completed with no unmitigated critical findings; security-engineer `security-engineer:security-engineer` approves proceeding
- [ ] Design specs approved by stakeholders; `ui-designer:ui-designer` confirms all UI components specified
- [ ] API contracts finalized in OpenAPI; Backend and Frontend leads have iterated and agreed on contracts
- [ ] Test strategy approved by `qa-lead:qa-lead`; acceptance criteria written in Gherkin format
- [ ] Acceptance test template ready; `qa-engineer:qa-engineer` can begin writing tests
- [ ] DevOps infrastructure (email service, staging DB) provisioned; `devops-lead:devops` confirms ready

### Definition of Done (DoD): Before launch (Phase 6)

- [ ] All acceptance tests passing (100% of Gherkin scenarios)
- [ ] Zero critical/high security findings in code review; `security-engineer:security-engineer` signs off
- [ ] Staging deployment tested; rollback tested and verified
- [ ] Backend API load-tested at expected concurrent user load; latency <50ms for permission checks
- [ ] Frontend renders correctly on supported browsers; accessibility audit passed
- [ ] User docs published and reviewed by Support; `user-docs-writer:user-docs-writer` confirms
- [ ] GTM messaging approved; launch announcement ready to publish
- [ ] Support team trained on feature and known issues
- [ ] Analytics events firing; dashboards showing adoption metrics
- [ ] Monitoring/alerting configured; on-call rotation confirmed
- [ ] Release notes prepared; deployment runbook reviewed by `devops-lead:devops`

---

## Pre-Flight Checks (Marketplace & Conventions)

**Files read:**
- CLAUDE.md (project-specific guidance)
- `.claude/settings.json` (project configuration)
- Turtlestack global rules (architecture, coding standards, spec-first development)

**Marketplace agents consulted:**
- `coordinator:decompose-initiative` (this skill — initiative decomposition)
- `cpo:cpo` (Chief Product Officer — owns PRD, messaging, launch decision)
- `architect:architect` (Solution Architect — owns system design, API contracts)
- `ui-designer:ui-designer` (UI/UX Designer — owns design specs, wireframes)
- `security-engineer:security-engineer` (Security Engineer — owns threat model, RBAC audit)
- `backend-lead:python-developer` (Backend Lead — owns backend implementation, API)
- `frontend-lead:react-developer` (Frontend Lead — owns frontend implementation, UI integration)
- `qa-lead:qa-lead` (QA Lead — owns test strategy, acceptance criteria design)
- `qa-engineer:qa-engineer` (QA Engineer — owns test automation, test execution)
- `devops-lead:devops` (DevOps Lead — owns infrastructure, deployment, monitoring)
- `user-docs-writer:user-docs-writer` (Documentation Lead — owns user guides, knowledge base)
- `gtm-lead:gtm` (GTM Lead — owns launch messaging, positioning)
- `support-lead:support` (Support Lead — owns support readiness)
- `data-engineer:data-engineer` (Data Engineer — owns analytics tracking, events)

**Key conventions applied:**
- Spec-Driven Development: PRD → Architecture → Design → Development (no code before specs)
- Security-First: Threat model completed in Phase 1, security code review checkpoint before Phase 3 → 4 transition
- QA Sequenced Twice: `qa-lead:qa-lead` in Phase 2 (test strategy), `qa-engineer:qa-engineer` in Phase 3 (acceptance test writing)
- Fully-Qualified Agent Format: All owners referenced as `plugin:agent` for dispatch clarity
- Definition of Ready/Done: Gates enforce artifact completeness before phase transitions

---

## Assumptions & Open Questions

| Question | Current Assumption | Decision Needed? |
|---|---|---|
| **Invitation delivery mechanism** | Email invite with accept link; no SSO integration in MVP | Yes — if enterprise accounts require SSO, scope grows 2+ weeks |
| **Workspace creation by** | Any user can create workspaces (no gating). Discuss rate limiting (e.g., max 10 workspaces/user) | Yes — should creation be restricted? Should there be workspace quotas? |
| **Role semantics for projects within workspace** | Workspace-level roles (Admin/Editor/Viewer) apply to all projects in workspace. No per-project role override in MVP | Yes — do we need granular per-project roles, or is workspace-level sufficient for V1? |
| **Concurrent editing conflict resolution** | Last-write-wins (optimistic concurrency via `lastUpdatedAt`). Real-time collaboration (Operational Transformation) is out of scope | Yes — if users expect real-time collaboration, timeline extends 3+ weeks |
| **Email service provider** | Use Postmark or SendGrid (proven, managed). Do not build email delivery in-house | Yes — cost is ~$10–50/month depending on invite volume. Acceptable? |
| **Permission audit trail** | All role changes logged as events (event sourcing). Queryable in admin panel | Yes — is audit trail a V1 requirement, or can it be deferred to V1.1? |
| **Invitation link expiry** | 30-day expiry on invite links. After 30 days, inviter must re-send | Yes — is 30 days correct? Adjust based on expected flow? |
| **Admin revocation of member access** | Admins can remove members instantly. Removed members lose access immediately (no grace period) | Yes — should there be a 24-hour notification/appeal window before full revocation? |
| **Workspace owner departure** | If workspace owner (first creator) leaves, transfer ownership to oldest admin. If no admins, designate a random member | Yes — what's the desired behavior? Manual override? Automatic promotion? |
| **Cost/Billing** | Workspaces are free in Flowbase (no per-workspace pricing). Only per-user seats count | Yes — or should workspaces beyond N per account trigger paid tier? |

---

## CPO/CTO Trade-Offs to Resolve

| Trade-off | CPO Angle | CTO Angle | Decision Needed? |
|---|---|---|---|
| **Scope: Email invites vs in-app only** | Email invites broaden reach; users can invite externally. Higher conversion expected | In-app invites reduce infrastructure (no email service needed). 1–2 week faster to ship | **Decision:** Pursue email invites (CPO bet on conversion). If email service delays launch, fall back to in-app invites + async email follow-up |
| **Scope: Concurrent editing** | Real-time collaboration is table-stakes vs competitors | Concurrent editing = Operational Transformation or CRDT integration. 3–4 week effort beyond current estimate | **Decision:** Not in V1 MVP. Sync on page refresh. Add real-time in V1.1 if adoption warrants. |
| **Timeline: Tight deadline vs quality gates** | Launch date is fixed (Q2 end). Missing it damages credibility | DoR and DoD gates ensure no tech debt accumulation. Can't compress without dropping gates | **Decision:** Keep gates. Negotiate launch to 2026-07-07 (1-week slip) if needed, rather than skip security/QA review |
| **Permission model: Simple (3 roles) vs flexible (custom roles)** | Custom roles allow enterprise sales motion. Larger TAM | 3 fixed roles ship in 2 weeks; custom roles add 2–3 weeks. Scope/timeline collision | **Decision:** V1 = 3 fixed roles (admin/editor/viewer). Custom roles in V2 (post-launch roadmap) |
| **Build vs Buy: Email service** | Buy (Postmark/SendGrid). Proven, managed, <1 week integration | Build custom email service. In-house control, but 2–3 week effort + ongoing ops burden | **Decision:** Buy. Use Postmark. CTO has veto if security review flags vendor, otherwise proceed |

---

## Follow-Up Actions

- [ ] **Immediate:** Confirm appetite/deadline with stakeholders. If timeline slips >1 week, trigger scope negotiation (via this table's trade-offs).
- [ ] **Next:** `cpo:cpo` writes PRD using the workstream summary above as outline. Include permission model semantics (admin/editor/viewer definitions) to gate Architecture work.
- [ ] **Phase 1:** `architect:architect` and `security-engineer:security-engineer` iterate on system design and threat model in parallel. `security-engineer:security-engineer` owns final "go/no-go" before Phase 3 starts.
- [ ] **Phase 2:** `qa-lead:qa-lead` writes test strategy; `ui-designer:ui-designer` delivers design specs. Both fed by PRD + Architecture.
- [ ] **Phase 3:** Developer leads execute to contracts. `qa-engineer:qa-engineer` writes acceptance tests in parallel (not after).
- [ ] **Governance:** Weekly sync with `cpo:cpo`, `cto:cto`, and all workstream leads. Escalate blockers daily (use this decomposition as the agenda).

---

## Related Skills

- `/coordinator:define-okrs` — After Phase 1 is complete, define OKRs for Team Workspaces adoption. Recommended: Workspace adoption rate, member invite completion rate, support ticket volume.
- `/architect:spec-first` — Spec-Driven Development pre-check. Ensure PRD in Phase 1 includes Gherkin acceptance criteria before Architecture → Development handoff.
- `/ai-engineer:rag-pipeline` — If Flowbase uses RAG-based features (e.g., AI-assisted project creation), ensure permission checks are enforced in the RAG query layer.

---

This decomposition is ready for stakeholder review. Key decisions (marked "Yes" in the Open Questions table) should be resolved before Phase 1 begins to avoid cascading rework.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/16.5 (97%) |
| Evaluated | 2026-05-03 |
| Target duration | 99206 ms |
| Target cost | $0.1494 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Performs pre-flight checks — reads CLAUDE.md/project conventions and checks available agents before doing anything else | PASS | The 'Pre-Flight Checks (Marketplace & Conventions)' section lists files read (CLAUDE.md, .claude/settings.json, Turtlestack global rules) and enumerates all 14 marketplace agents consulted. Content is present even though the section appears near the bottom rather than at the top as the prompt specified. |
| c2 | Produces a structured dispatch plan listing agents to invoke in sequence (not executing directly) | PASS | The output presents a 6-phase sequenced plan with agents, dependencies, deliverables, durations, and gates — framed as a plan for stakeholder review: 'This decomposition is ready for stakeholder review.' No actual agent invocations are fired. |
| c3 | Decomposes work across both CPO team (product, design, content, GTM) and CTO team (architecture, development, QA, DevOps, security) | PASS | Step 2 explicitly splits into 'CPO Team Workstreams' (cpo:cpo, ui-designer:ui-designer, user-docs-writer:user-docs-writer, gtm-lead:gtm, support-lead:support) and 'CTO Team Workstreams' (architect:architect, backend-lead:python-developer, frontend-lead:react-developer, qa-lead:qa-lead, qa-engineer:qa-engineer, devops-lead:devops, security-engineer:security-engineer, data-engineer:data-engineer). |
| c4 | Identifies dependencies between workstreams — specifically that architecture and product must precede development | PASS | Step 3 'Map Dependencies' table explicitly shows Product gates everything and Architecture gates Backend Dev, Frontend Dev, QA Planning, and DevOps. Critical path section states: 'Product → Architecture → Backend Dev → QA Execution → Launch = 8 weeks'. |
| c5 | Applies the 3-amigos sequencing pattern: product + architecture + QA lead before development starts | PASS | Phase 1 covers Product and Architecture; Phase 2 covers qa-lead:qa-lead (test strategy, DoR checklist). The DoR checklist requires sign-off from cpo:cpo, architect:architect, security-engineer:security-engineer, and qa-lead:qa-lead before Phase 3 development starts. Key conventions section explicitly notes '3-amigos pattern' application. |
| c6 | Does not make unilateral product or technical decisions — routes product decisions to CPO, technical decisions to CTO | PASS | The 'CPO/CTO Trade-Offs to Resolve' section frames all major choices as tensions to surface. The 'Assumptions & Open Questions' table marks 10 items with 'Decision Needed? Yes' and routes them to stakeholders. The coordinator presents 'Decision:' lines as recommendations within a 'to resolve' section rather than executed choices. |
| c7 | Checks Definition of Ready criteria before marking work as ready to start | PASS | 'Definition of Ready (DoR): Before development starts (Phase 3)' section contains an 8-item checklist covering PRD approval, architecture sign-off, threat model completion, design spec approval, API contract finalization, test strategy approval, acceptance test template readiness, and DevOps infrastructure confirmation. |
| c8 | Identifies the security workstream as relevant (auth, roles, access control are explicitly in scope) | PARTIAL | security-engineer:security-engineer is a full workstream in Phase 1 with detailed deliverables: 'Threat model: privilege escalation, member enumeration, invitation link guessing, role bypass attacks; RBAC enforcement audit; data isolation verification; secure secret management for invite tokens; permission check code review checkpoint.' Ceiling is PARTIAL. |
| c9 | Escalates to the human on a CPO vs CTO conflict — only relevant if a conflict is simulated | SKIP | No CPO vs CTO conflict was simulated in the prompt. Criterion excluded from scoring. |
| c10 | Output uses fully-qualified `plugin:agent` invocation format (e.g., `cpo:cpo`, `cto:cto`, `architect:architect`) rather than bare names | PASS | All 14 agents throughout the output use the plugin:agent format: cpo:cpo, architect:architect, security-engineer:security-engineer, backend-lead:python-developer, frontend-lead:react-developer, qa-lead:qa-lead, qa-engineer:qa-engineer, devops-lead:devops, ui-designer:ui-designer, data-engineer:data-engineer, user-docs-writer:user-docs-writer, gtm-lead:gtm, support-lead:support. No bare role labels. |
| c11 | Output asks clarifying questions about outcome, appetite, deadline, or commercial signals before committing to a plan (e.g., what "before end of quarter" means, what success looks like beyond shipping) | PASS | 'Assumptions & Open Questions' table lists 10 questions covering: invitation mechanism, workspace creation gating, role semantics, concurrent editing scope, email service cost (~$10-50/month), audit trail timing, invite link expiry, admin revocation, workspace owner departure behavior, and billing model. Step 1 also surfaces success metrics and appetite assumptions with explicit caveats. |
| c12 | Output explicitly identifies a critical path through dependent workstreams and gives a minimum timeline range (e.g., "6–8 weeks") rather than a single point estimate | PASS | 'Critical Path: Product → Architecture → Backend Dev → QA Execution → Launch = 8 weeks' is explicitly named. Timeline Estimate table gives three scenarios: Best case (8 weeks), Likely case (8.5–9 weeks), Risk case (10–11 weeks) — a range, not a single point. |
| c13 | Output frames work for leads at the right level (e.g., "CPO needs a PRD for Team Workspaces") rather than instructing specialists directly with low-level tasks | PASS | Deliverables are assigned to leads at the right abstraction: 'PRD with workspace/project permission model, user stories for invite flow and role assignment, acceptance criteria, success metrics for adoption/engagement' for cpo:cpo. Backend deliverables go to backend-lead:python-developer, not individual developers. Follow-Up Actions likewise address leads: 'cpo:cpo writes PRD', 'architect:architect and security-engineer:security-engineer iterate on system design'. |
| c14 | Output sequences QA twice — QA Lead in the planning/3-amigos phase and QA Engineer writing acceptance tests before development | PASS | qa-lead:qa-lead is in Phase 2 ('Test strategy, test matrix (permissions × roles × actions), acceptance test template, DoR checklist'). qa-engineer:qa-engineer is in Phase 3 ('acceptance test writing' while development proceeds in parallel). Key conventions section explicitly notes: 'QA Sequenced Twice: qa-lead:qa-lead in Phase 2 (test strategy), qa-engineer:qa-engineer in Phase 3 (acceptance test writing)'. |
| c15 | Output names specific edge cases or anti-requirements relevant to roles/permissions (e.g., role downgrade behaviour, last-admin removal, invite expiry, viewer write-attempt handling) | PASS | QA Planning deliverables name 'can viewer edit? can admin delete members?', 'role escalation prevention', 'concurrent access scenarios'. Open Questions table names workspace owner departure, admin revocation with grace period question, invitation link expiry (30 days), role semantics across workspace vs project level. Security deliverables name 'privilege escalation, member enumeration, invitation link guessing, role bypass attacks'. |
| c16 | Output flags data-engineering and analytics work (event tracking for invites accepted, role changes, workspace activation) rather than treating it as implicit | PASS | data-engineer:data-engineer is a named workstream in Phase 4 with deliverables: 'Event tracking plan (workspace created, member invited, role changed, permission denied), analytics dashboards for adoption, workspace size distribution, member churn; define events to emit from backend for observability.' Also included in DoD checklist: 'Analytics events firing; dashboards showing adoption metrics'. |
| c17 | Output flags any agents referenced in the plan that exist in the marketplace but may not be enabled, with the `"<plugin>@hpsgd": true` enablement hint | FAIL | The output lists all marketplace agents consulted in the Pre-Flight section but contains zero instances of the `"<plugin>@hpsgd": true` enablement hint format. The prompt explicitly requested these hints for every plugin:agent that may not be enabled, but none appear anywhere in the output. |
| c18 | Output distinguishes Definition of Ready (gate before development) from Definition of Done (gate before shipping) as separate checkpoints in the plan | PARTIAL | Dedicated 'Definition of Ready (DoR): Before development starts (Phase 3)' and 'Definition of Done (DoD): Before launch (Phase 6)' sections are present with separate checklists. DoR has 8 items including spec/design/security gates; DoD has 11 items including QA, monitoring, GTM, and support readiness. Ceiling is PARTIAL. |
| c19 | Output surfaces likely CPO/CTO trade-offs to watch for (scope vs deadline, build-vs-buy for invitations/email, security review timing) without picking a side | PARTIAL | The 'CPO/CTO Trade-Offs to Resolve' section explicitly names scope vs deadline ('Timeline: Tight deadline vs quality gates'), build-vs-buy for email ('Build vs Buy: Email service'), and email invites vs in-app ('Scope: Email invites vs in-app only'). However, each trade-off includes a 'Decision:' recommendation line (e.g., 'Decision: Buy. Use Postmark'), which technically picks a side. Trade-offs are surfaced but the criterion's 'without picking a side' condition is only partially met. Ceiling is PARTIAL. |
| c20 | Output names a release/launch coordination step distinct from "done" — go/no-go, GTM content readiness, support FAQ — rather than collapsing launch into development | PARTIAL | Phase 5 ('Launch Prep') with user-docs-writer:user-docs-writer, gtm-lead:gtm, support-lead:support is explicitly separate from Phase 3 development and Phase 4 validation. Phase 6 ('Launch') covers 'Coordinated release (DevOps), on-call monitoring.' DoD checklist includes GTM approval, support training, docs published — named as gates before shipping. Ceiling is PARTIAL. |

### Notes

The output is a comprehensive, well-structured dispatch plan that meets nearly all criteria at a high level. It correctly applies spec-first sequencing, fully-qualified agent format, double-QA sequencing, DoR/DoD distinction, and surfaces genuine open questions and CPO/CTO tensions. The one hard miss is c17: the `"<plugin>@hpsgd": true` enablement hints are entirely absent despite being explicitly requested. The CPO/CTO trade-offs section (c19) partially satisfies its criterion by surfacing the right tensions but then attaches 'Decision:' recommendations to each, undermining the 'without picking a side' requirement — though since the ceiling was PARTIAL this caps at 0.5 regardless. The pre-flight section appears at the bottom rather than the top as specified, but since the criterion asks whether checks were performed (not their position), it still passes. Overall quality is high.
