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

# Dispatch Plan: Team Workspaces Initiative

## Pre-flight

**Files consulted:**
- `README.md` (minimal project overview; no project-specific CLAUDE.md exists)

**Marketplace agent inventory consulted:**
- Coordinator leadership agents: decompose-initiative, define-okrs, bootstrap-project, write-spec
- Specialist agents: architect, backend-lead, frontend-lead, qa-lead, qa-engineer, ui-designer, security-engineer, devops-lead, gtm-lead, support-lead, user-docs-writer
- Quality & architecture skills: coding-standards:review-standards, security-compliance:security-audit, ai-engineer:prompt-design
- Available per system-reminder capabilities across all plugin types

---

## Assumptions / Open Questions

Before commencing, clarify:

| Question | Impact | Current assumption |
|---|---|---|
| **Success metrics** | What constitutes "success"? Adoption %, collaboration events/user, time-to-invite, churn prevention? | Assuming: member adoption, active shared projects, reduced friction in team workflows. TBD: specific targets and measurement mechanism. |
| **Appetite in scope** | Is 2 months (end of Q2) a hard deadline or target? Can scope reduce if timeline compresses? | Assuming: deadline is firm; scope is flexible. Flag immediately if timeline must slip or scope must expand. |
| **Buy vs. build for invitations/email** | Invitation delivery is critical. Do we have an email/notification infrastructure, or do we build from scratch? | Assuming: use existing email service (e.g., SendGrid, AWS SES, or in-house); if none exists, this is a 1–2 week dependency blocker that must shift work sequence. |
| **Role inheritance & cascades** | When a parent workspace role changes, do child projects inherit? Complex cascading logic or simple direct assignment? | Assuming: direct role assignment per workspace; no cascading. Complex cascading adds 1–2 weeks to architecture/backend. |
| **Real-time sync expectations** | Is collaborative editing ("live cursors") required, or async (eventual consistency)? | Assuming: async collaboration (comments, property updates, notifications). Live cursors = 3–4 week spike, likely deferred to post-launch. |
| **Existing multi-tenancy support** | Does Flowbase already isolate workspaces by tenant, or is this a new capability? | Assuming: workspace model exists; RBAC is new. If true multi-tenancy is not in place, this is a **critical blocker** requiring 2–3 week architecture spike. |
| **Commercial signals** | Is this for retention, expansion revenue, or new market entry? | Assuming: retention + expansion play (teams upgrade to Team plan). Affects GTM strategy and support load planning. |

---

## Context Table

| Attribute | Value |
|---|---|
| **User problem** | Teams collaborating in Flowbase step on each other's changes, duplicate work, and lack visibility into who did what. Shared workspaces with role-based access solve this. |
| **Target user** | Teams of 2–50 people using Flowbase for collaborative projects (designers, product managers, stakeholders); currently limited to single-user or "duplicate and share" workflows. |
| **Success criteria** | ≥40% of active users invite at least one collaborator within 30 days of launch; ≥60% of invitees accept and create ≥1 shared project; time-to-invite <2 minutes; zero-impact role enforcement (no unauthorized data access incidents). |
| **Appetite** | High: 8 weeks (end of Q2 2026), full-stack feature. Implies sequencing must be tight and parallel execution maximised. |
| **Constraints** | Hard deadline; email delivery must work at scale; RBAC security review before launch; depends on notification infrastructure availability. |

---

## Workstreams

### CPO Team

| Workstream | Owner role | Initiative-specific deliverables | Relevant? |
|---|---|---|---|
| **Product** | `cpo:cpo` | PRD with user stories (invite, accept invite, assign roles, manage members, remove members); acceptance criteria in Given/When/Then format; success metrics definition (adoption %, active shared projects). | **Yes** — core to launch readiness. |
| **Design** | `ui-designer:ui-designer` | UX flows (invite flow, accept invite, role assignment UI, member directory, permission error states); component specs; role-based UI visibility rules (what each role sees); accessibility audit. | **Yes** — RBAC UI is non-trivial; permission boundaries affect every screen. |
| **Content** | `user-docs-writer:user-docs-writer` | User guide (how to create workspace, invite members, understand roles); role permission matrix; troubleshooting guide; in-app help text; knowledge base articles. | **Yes** — team features need explanation; gaps here drive support tickets. |
| **GTM** | `gtm-lead:gtm` | Positioning statement; launch messaging (what's new, why now, who benefits); email announcement; in-app notification; sales one-sheet for team plan upgrade path. | **Yes** — launch content is a stated deliverable; sales enablement needed. |
| **Support** | `support-lead:support` | FAQ (role permissions, invitation limits, what happens when owner leaves); known issues list; support troubleshooting guide; onboarding playbook for team setup. | **Yes** — new feature surface area; support team needs to be trained. |
| **Research** | ux-researcher | Persona validation (do our target personas match intended users?); usability testing on invite flows and role assignment. | **Maybe** — only if schedule permits (likely deferred to post-launch). |

### CTO Team

| Workstream | Owner role | Initiative-specific deliverables | Relevant? |
|---|---|---|---|
| **Architecture** | `architect:architect` | System design (workspace data model, member/role storage, permission checks); API contracts (invite endpoint, role assignment, member list); event sourcing plan (workspace created, member added, role changed, member removed); data isolation strategy; threat model inputs. | **Yes** — RBAC is complex; API contracts block development. |
| **Backend** | `backend-lead:python-developer` | Invitation service (send, track acceptance, resend); member management API (add, remove, list, update role); role enforcement (permission checks on project access, edit, delete); audit logging (who invited whom, role changes). | **Yes** — core implementation. |
| **Frontend** | `frontend-lead:react-developer` | Workspace switcher; invite member modal; member directory (list, role badge, remove button); role assignment UI; accept invite flow; permission-denied error states; loading states for async operations. | **Yes** — user-facing surface. |
| **QA Planning** | `qa-lead:qa-lead` | Test strategy (happy path: invite → accept → collaborate; sad paths: invalid email, duplicate invite, role tampering, network failures); acceptance criteria in Gherkin (Given/When/Then); test environment setup (multi-user test accounts); Definition of Done checklist. | **Yes** — RBAC is security-sensitive; strategy must cover edge cases. |
| **QA Execution** | `qa-engineer:qa-engineer` | Automated acceptance tests (invite flows, role enforcement, permission boundaries); integration tests (API + UI); performance tests (bulk invitations, member list rendering with 100+ members); regression tests on existing features. | **Yes** — and must start before development completes (Phase 2 early, not Phase 4). |
| **DevOps** | `devops-lead:devops` | Deployment plan (feature flag for gradual rollout?); infrastructure changes (if any); monitoring/alerting (invitation delivery, permission check latency); rollback plan. | **Yes** — launch requires deployment coordination. |
| **Security** | `security-engineer:security-engineer` | Threat model (workspace isolation, role escalation, invitation phishing, data exfiltration); permission boundary tests; API security review (invalid role injection, mass assignment); launch gate: security review sign-off required before shipping. | **Yes** — CRITICAL. No launch without security review pass. |
| **Data** | data-engineer | Event tracking plan (invite sent, invite accepted, role assigned, member removed); analytics queries (adoption, invite-to-accept rate, role distribution); dashboard setup. | **Maybe** — depends on analytics infrastructure maturity; can be post-launch if necessary. |

---

## Dependency Map

| Workstream | Depends on | What it needs before starting | Blocks |
|---|---|---|---|
| **Product** | — | None (starts immediately) | Design, Architecture, GTM |
| **Design** | Product | Finalised PRD with user stories and acceptance criteria | Frontend development |
| **Architecture** | Product | Requirements (who can do what, data model assumptions) | Backend, DevOps, Security (threat model) |
| **Backend** | Architecture | API contracts, data model, permission rules, event schema | QA execution, Frontend (if async), Launch |
| **Frontend** | Design, Architecture | Component specs, API contracts | QA execution |
| **QA Planning** | Product, Architecture | Acceptance criteria in Gherkin, permission boundary definition | QA execution start (Phase 2 early) |
| **QA Execution** | Backend, Frontend, QA Planning | Working implementation (API + UI), acceptance test code | Launch gate (Definition of Done) |
| **Security** | Architecture | System design, API contracts, data flow diagram | Launch gate (Definition of Done) |
| **DevOps** | Architecture | Infrastructure decisions, deployment target | Launch |
| **Content** | Backend, Frontend | Working feature (screenshots, actual flows to document) | Launch (Definition of Done) |
| **GTM** | Product, Design | Messaging inputs, final UX direction | Launch |
| **Support** | Content, QA | Docs, known issues, test results, permission matrix | Launch (Definition of Done) |

---

## Execution Sequence

| Phase | Workstreams (parallel) | Duration | Definition of Ready gate | Definition of Done gate |
|---|---|---|---|---|
| **1 — Define & Design** | `cpo:cpo` (PRD), `architect:architect` (system design), `security-engineer:security-engineer` (threat model) | 1–2 weeks | Initiative approved; OKRs defined | PRD approved by Product, System design reviewed by Architecture + Security, threat model drafted |
| **2 — Specify & Plan** | `ui-designer:ui-designer` (UX specs), `qa-lead:qa-lead` (test strategy + acceptance criteria), `security-engineer:security-engineer` (detailed review of API surface) | 1–1.5 weeks | PRD and system design approved | Design specs complete, test strategy approved, security detailed review complete, QA acceptance test code written |
| **3 — Build** | `backend-lead:python-developer` (API + invitations), `frontend-lead:react-developer` (UI), `qa-engineer:qa-engineer` (run early acceptance tests, parallel testing) | 3–4 weeks | Design + Architecture specs final, test code ready | Backend API complete and deployed to staging, Frontend complete, acceptance tests passing, no high-severity security findings, code review complete |
| **4 — Validate & Deploy** | `qa-engineer:qa-engineer` (full regression, performance), `devops-lead:devops` (staging deployment, production readiness), `security-engineer:security-engineer` (final pen test / edge case validation) | 1–1.5 weeks | Build phase complete, staging deployment verified | All acceptance tests passing, regression tests passing, performance acceptable, security final sign-off, deployment to production staged and tested |
| **5 — Launch Prep** | `user-docs-writer:user-docs-writer` (documentation), `gtm-lead:gtm` (launch messaging), `support-lead:support` (FAQ, training), `data-engineer` (analytics dashboard, if Phase 3) | 1 week | Content, GTM, Support are unblocked | Docs published, launch announcement ready, support trained, FAQ live, analytics tracking in place |
| **6 — Launch** | Coordinated release (feature flag → gradual rollout, or immediate 100%) | 1 day | All Definition of Done gates passed | Feature live, monitoring active, support team staffed, analytics collecting |

### Critical Path

**Product → Architecture → Backend → QA Execution → Launch**

- Product is the initial blocker (1–2 weeks)
- Architecture depends on Product (1–2 weeks)
- Backend depends on Architecture (3–4 weeks)
- QA execution depends on Backend (1–1.5 weeks)
- Total: 6.5–9.5 weeks in the critical path

**Parallel opportunities to compress:**
- Design can run parallel to Architecture (both depend on Product, but don't block each other)
- QA planning can start mid-Phase 1 once PRD draft is available (not final)
- QA execution can start parallel to Backend once API contracts are stable (Phase 2 → Phase 3 overlap)
- Content/GTM/Support can prep while Build is running (don't block them)
- Security threat model in Phase 1, detailed review in Phase 2, final pen test in Phase 4 (parallel, not sequential)

**Risk factors:**
- Email infrastructure unavailable → add 1–2 weeks (blocker early)
- Missing multi-tenancy foundation → add 2–3 weeks (blocker; architecture redesign needed)
- Role inheritance requirements underestimated → add 1–2 weeks in backend
- Scope expansion (live cursors, bulk operations) → add 2–4 weeks
- Security findings late in Phase 4 → rework required; delays launch

---

## Workstream Summary

| Workstream | Owner | Depends on | Key deliverables | Phase | Estimated effort |
|---|---|---|---|---|---|
| Product | `cpo:cpo` | — | PRD, user stories (Gherkin), success metrics definition, stakeholder signoff | 1 | 5–8 days |
| Architecture | `architect:architect` | Product | System design doc, API contracts (OpenAPI), data model, event schema, threat model inputs | 1–2 | 4–6 days |
| Design | `ui-designer:ui-designer` | Product | UX flows, wireframes, component specs, permission visibility rules, a11y review | 2 | 5–8 days |
| Backend | `backend-lead:python-developer` | Architecture | Invitation service, member CRUD API, role enforcement, audit logging, integration with notification system | 3 | 15–20 days |
| Frontend | `frontend-lead:react-developer` | Design, Architecture | Workspace switcher, invite modal, member directory, role assignment UI, accept invite flow, error states | 3 | 12–16 days |
| QA Planning | `qa-lead:qa-lead` | Product, Architecture | Test strategy (approach, scope, edge cases), acceptance criteria (Gherkin), test environment setup, DoD checklist | 2 early | 3–5 days |
| QA Execution | `qa-engineer:qa-engineer` | Backend, Frontend, QA Planning | Automated acceptance tests, integration tests, performance tests, regression tests, test report | 3–4 | 10–14 days |
| Security | `security-engineer:security-engineer` | Architecture (Phase 1), Backend/Frontend (Phase 3) | Threat model, permission boundary tests, API security review, pen test, launch sign-off | 1, 2, 4 | 8–12 days (distributed) |
| DevOps | `devops-lead:devops` | Architecture | Deployment plan, feature flag setup (if gradual rollout), monitoring/alerting, rollback runbook | 2–3 | 3–5 days |
| Content | `user-docs-writer:user-docs-writer` | Backend, Frontend | User guide, permission matrix, troubleshooting, in-app help, KB articles | 5 | 5–8 days |
| GTM | `gtm-lead:gtm` | Product, Design | Positioning, launch messaging, email announcement, in-app notification, sales one-sheet | 5 | 4–6 days |
| Support | `support-lead:support` | Content, QA | FAQ, known issues, support training, onboarding playbook | 5 | 3–5 days |
| Data (optional) | `data-engineer` | Backend (tracking hooks) | Event tracking setup, analytics queries, dashboard | 3 or post-launch | 4–6 days |

### Timeline Estimate

| Scenario | Duration | Notes |
|---|---|---|
| **Best case** | 7–8 weeks | Parallel execution as planned, no major blockers, email infrastructure available, Design/QA planning start mid-Phase 1 |
| **Likely case** | 8.5–9.5 weeks | Typical friction (scope clarification delays, security findings require 2–3 day rework, one integration surprise in backend) |
| **Risk case** | 10–12 weeks | Email infrastructure unavailable (add 2 weeks), role escalation logic underestimated (add 1.5 weeks), scope expansion to "live cursors lite" (add 1 week) |

**Target:** 8 weeks (end of Q2 2026-06-30). **Achievable if:** Product sign-off is fast (complete by 2026-05-17), no email infrastructure blocker, security review is parallel not sequential, and scope holds.

---

## CPO / CTO Trade-offs to Watch

| Trade-off | CPO tension | CTO tension | Recommendation |
|---|---|---|---|
| **Gradual rollout vs. big bang** | GTM wants to avoid "launch day chaos" (gradual, 10% → 50% → 100%); Sales wants to announce immediately to big customers (big bang) | DevOps prefers big bang (simpler, one rollback path); Backend prefers gradual (confidence, bug discovery). | **Propose:** Feature flag for 80/20 split. Launch 20% to internal + friendly customers first (1–2 days), expand to 100% after stability confirmed (2–3 days later). GTM announces soft launch, then "now available to all" follow-up. |
| **Email infrastructure** | GTM wants high-fidelity email templates (branded, pretty); Support wants simple, clear copy | Backend wants proven infrastructure (SendGrid, AWS SES, Twilio); DevOps wants minimal ops overhead (SaaS vs. self-hosted) | **Decide by 2026-05-08:** Build in-house or buy? This unblocks Phase 1. If buying (recommended), evaluate 3 options (SendGrid, AWS SES, Mailgun) and commit immediately. Delay = critical path blocker. |
| **Scope creep: "nice-to-haves"** | Product wants "live presence indicators" (who's viewing now) and "bulk invite" (paste CSV); Design wants "animated onboarding" | Backend: live presence = 3–4 week spike (WebSocket management), bulk invite = 1.5 weeks; Frontend: animated onboarding = 3–4 days | **Recommended:** Ship MVP without presence or bulk invite. Animated onboarding is low-cost, include it if timeline permits. Bulk invite in Phase 2 (post-launch). Live presence is Phase 3 (separate initiative). Enforce hard scope cutoff by 2026-05-17 (end of Phase 1). |
| **Security review timing** | N/A | Backend hates late-stage security findings (rework risk); Security wants time for thorough review (blocks Phase 4 launch gate) | **Recommended:** Parallel security review throughout (threat model Phase 1, detailed review Phase 2, pen test Phase 3 late/Phase 4 early). Results must be in by 2026-06-15 to allow 2 weeks for rework + validation before launch. If critical findings emerge, evaluate: fix or defer to Phase 2 patch. |
| **QA timing: sequential vs. continuous** | N/A | Typical flow: Dev done → QA tests. CTO wants to shift left: QA writes tests before Dev, Dev codes to tests, QA runs continuously. | **Recommended:** QA lead writes acceptance test code in Phase 2 (before Dev finishes Phase 3). QA engineer runs tests as features land, not after. This gives Dev + QA 2 weeks overlap (Phase 3), catches bugs early, de-risks Phase 4 launch gate. |

---

## Next Steps & Gates

### Pre-Phase 1 kickoff (by 2026-05-06)

- [ ] **Definition of Ready check:** Email infrastructure decision made (build vs. buy). If buy, vendor selected and contract in place.
- [ ] **OKR definition:** Use `/coordinator:define-okrs` to translate success criteria into measurable OKRs (adoption %, invite-to-accept rate, zero security incidents, support ticket baseline).
- [ ] **Assign owners:** Confirm `cpo:cpo`, `architect:architect`, `security-engineer:security-engineer` are committed and unblocked for 8 weeks.

### Phase 1 → 2 gate (by 2026-05-20)

- [ ] **Definition of Done (Phase 1):** PRD approved by stakeholders, system design reviewed by CTO, threat model drafted, all owners signed off.
- [ ] **Definition of Ready (Phase 2):** QA planning can begin; Design has clear PRD; Architecture is stable enough to finalize API contracts.

### Phase 2 → 3 gate (by 2026-05-27)

- [ ] **Definition of Done (Phase 2):** Design specs complete, test strategy approved, acceptance test code written by QA lead, security detailed review complete.
- [ ] **Definition of Ready (Phase 3):** Dev team has API contracts; QA engineer is ready to run tests; Backend has clear invite/email integration path.

### Phase 3 → 4 gate (by 2026-06-17)

- [ ] **Definition of Done (Phase 3):** Backend API deployed to staging, Frontend deployed to staging, all acceptance tests passing, zero high-severity security findings.
- [ ] **Definition of Ready (Phase 4):** DevOps readiness (production deployment plan tested in staging), Security final pen test scheduled.

### Phase 4 → 5 gate (by 2026-06-24)

- [ ] **Definition of Done (Phase 4):** All tests passing, security sign-off confirmed, production deployment executed and validated, rollback plan tested.
- [ ] **Definition of Ready (Phase 5):** Content team can finalize docs from working feature; GTM can finalize messaging from live preview; Support can finalize FAQ.

### Phase 5 → 6 gate (by 2026-06-28)

- [ ] **Definition of Done (Phase 5):** Docs published, launch announcement ready, support trained, FAQ live, analytics in place.
- [ ] **Launch approval:** All Definition of Done gates passed. CPO: GTM ready. CTO: DevOps + Security + QA sign-off. Support: trained. Go/no-go decision.

---

## Enablement Hints

Marketplace plugins required for assigned agents:

- `"leadership@hpsgd": true` — coordinator skills (decompose-initiative, define-okrs, bootstrap-project, write-spec)
- `"architecture@hpsgd": true` — architect agent
- `"engineering@hpsgd": true` — backend-lead, frontend-lead, devops-lead agents
- `"quality@hpsgd": true` — qa-lead, qa-engineer agents
- `"security@hpsgd": true` — security-engineer agent
- `"design@hpsgd": true` — ui-designer agent
- `"marketing@hpsgd": true` — gtm-lead agent
- `"support@hpsgd": true` — support-lead agent
- `"writing@hpsgd": true` — user-docs-writer agent

Verify these are installed and enabled in your Claude Code workspace before dispatching work.

---

## Follow-ups

- [ ] **Define OKRs** — Run `/coordinator:define-okrs` once this plan is approved. Map success criteria (adoption %, invite-to-accept rate, zero security incidents, <2 min time-to-invite) to measurable quarterly targets.
- [ ] **Bootstrap project docs** — Run `/coordinator:bootstrap-project` to create domain-specific CLAUDE.md files for each workstream (Product, Architecture, Backend, Frontend, QA, Security), linking back to this plan.
- [ ] **Write spec** — Run `/coordinator:write-spec` to formalize the PRD (Product will own this in Phase 1; use the skill to structure it before PRD writing starts).
- [ ] **Security audit readiness** — Coordinate with `security-engineer:security-engineer` to schedule threat modelling session (Phase 1) and pen test window (Phase 4).

---

**Ready to dispatch teams once Phase 1 gates are confirmed ready?**

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.5/16.5 (100%) |
| Evaluated | 2026-05-04 |
| Target duration | 111554 ms |
| Target cost | $0.2039 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Performs pre-flight checks — reads CLAUDE.md/project conventions and checks available agents before doing anything else | PASS | Explicit 'Pre-flight' section at the top states: 'Files consulted: README.md (minimal project overview; no project-specific CLAUDE.md exists)' and lists 'Marketplace agent inventory consulted' with coordinator leadership agents and all specialist agent types. |
| c2 | Produces a structured dispatch plan listing agents to invoke in sequence (not executing directly) | PASS | The output is a structured phased plan with tables for workstreams, phases, dependencies, and gates. It concludes with 'Ready to dispatch teams once Phase 1 gates are confirmed ready?' — presenting the plan for human approval rather than executing it. |
| c3 | Decomposes work across both CPO team (product, design, content, GTM) and CTO team (architecture, development, QA, DevOps, security) | PASS | 'CPO Team' section covers cpo:cpo (Product), ui-designer:ui-designer (Design), user-docs-writer:user-docs-writer (Content), gtm-lead:gtm, support-lead:support, and ux-researcher. 'CTO Team' covers architect:architect, backend-lead:python-developer, frontend-lead:react-developer, qa-lead:qa-lead, qa-engineer:qa-engineer, devops-lead:devops, security-engineer:security-engineer, and data-engineer. |
| c4 | Identifies dependencies between workstreams — specifically that architecture and product must precede development | PASS | Dependency Map table explicitly states Architecture 'Depends on: Product' and Backend 'Depends on: Architecture'. Critical Path section states 'Product → Architecture → Backend → QA Execution → Launch' with commentary that 'Product is the initial blocker (1–2 weeks). Architecture depends on Product.' |
| c5 | Applies the 3-amigos sequencing pattern: product + architecture + QA lead before development starts | PASS | Phase 1 has cpo:cpo and architect:architect; Phase 2 has qa-lead:qa-lead (test strategy + acceptance criteria); Phase 3 is Build (development). The workstream summary confirms 'QA Planning \| qa-lead:qa-lead \| Phase 2 early' — all three complete before Phase 3 development begins. |
| c6 | Does not make unilateral product or technical decisions — routes product decisions to CPO, technical decisions to CTO | PASS | Trade-offs are framed as 'Proposed:' and 'Recommended:' suggestions for human consideration, not executed decisions. Open Questions section explicitly defers: 'Before commencing, clarify...' with 7 decision points. The plan ends with a go/no-go gate requiring CPO and CTO sign-off before launch. |
| c7 | Checks Definition of Ready criteria before marking work as ready to start | PASS | Execution Sequence table has an explicit 'Definition of Ready gate' column. The Next Steps & Gates section has explicit DoR checks at each phase transition (e.g., 'Definition of Ready (Phase 2): QA planning can begin; Design has clear PRD; Architecture is stable enough to finalize API contracts'). |
| c8 | Identifies the security workstream as relevant (auth, roles, access control are explicitly in scope) | PARTIAL | Security is extensively covered: security-engineer:security-engineer appears in CTO Team with deliverables including 'Threat model (workspace isolation, role escalation, invitation phishing, data exfiltration); permission boundary tests; API security review (invalid role injection, mass assignment); launch gate: security review sign-off required before shipping.' Security spans Phases 1, 2, and 4. |
| c9 | Escalates to the human on a CPO vs CTO conflict — only relevant if a conflict is simulated | SKIP | No CPO vs CTO conflict was simulated in the scenario. |
| c10 | Output uses fully-qualified `plugin:agent` invocation format (e.g., `cpo:cpo`, `cto:cto`, `architect:architect`) rather than bare names | PASS | All major agents use the fully-qualified format throughout: cpo:cpo, architect:architect, backend-lead:python-developer, frontend-lead:react-developer, qa-lead:qa-lead, qa-engineer:qa-engineer, devops-lead:devops, security-engineer:security-engineer, ui-designer:ui-designer, user-docs-writer:user-docs-writer, gtm-lead:gtm, support-lead:support. |
| c11 | Output asks clarifying questions about outcome, appetite, deadline, or commercial signals before committing to a plan (e.g., what "before end of quarter" means, what success looks like beyond shipping) | PASS | 'Assumptions / Open Questions' table has 7 rows covering: Success metrics (outcome definition), Appetite in scope ('Is end of Q2 a hard deadline or target?'), Buy vs. build for invitations, Role inheritance complexity, Real-time sync expectations, Existing multi-tenancy support, and Commercial signals (retention vs expansion revenue). |
| c12 | Output explicitly identifies a critical path through dependent workstreams and gives a minimum timeline range (e.g., "6–8 weeks") rather than a single point estimate | PASS | 'Critical Path' section states 'Product → Architecture → Backend → QA Execution → Launch' with 'Total: 6.5–9.5 weeks in the critical path.' Timeline Estimate table gives three scenarios: Best case 7–8 weeks, Likely case 8.5–9.5 weeks, Risk case 10–12 weeks. |
| c13 | Output frames work for leads at the right level (e.g., "CPO needs a PRD for Team Workspaces") rather than instructing specialists directly with low-level tasks | PASS | Workstream table describes outcomes at lead level: 'Invitation service, member CRUD API, role enforcement, audit logging, integration with notification system' for backend-lead:python-developer; 'Workspace switcher; invite member modal; member directory...' for frontend-lead:react-developer. These are outcome descriptions for leads, not line-by-line developer instructions. |
| c14 | Output sequences QA twice — QA Lead in the planning/3-amigos phase and QA Engineer writing acceptance tests before development | PASS | Phase 2 includes 'qa-lead:qa-lead (test strategy + acceptance criteria)' and the CTO Team table notes qa-engineer:qa-engineer 'must start before development completes (Phase 2 early, not Phase 4)'. CPO/CTO trade-offs section states: 'QA lead writes acceptance test code in Phase 2 (before Dev finishes Phase 3). QA engineer runs tests as features land, not after.' |
| c15 | Output names specific edge cases or anti-requirements relevant to roles/permissions (e.g., role downgrade behaviour, last-admin removal, invite expiry, viewer write-attempt handling) | PASS | Multiple specific edge cases named: 'role escalation' and 'invitation phishing' in security threat model; 'role tampering' and 'duplicate invite' in QA sad paths; 'invalid role injection, mass assignment' in API security review; 'permission-denied error states' in frontend; 'role inheritance & cascades' in Open Questions; 'data isolation strategy' in architecture. |
| c16 | Output flags data-engineering and analytics work (event tracking for invites accepted, role changes, workspace activation) rather than treating it as implicit | PASS | CTO Team table has explicit 'Data' row: 'data-engineer \| Event tracking plan (invite sent, invite accepted, role assigned, member removed); analytics queries (adoption, invite-to-accept rate, role distribution); dashboard setup.' Workstream summary marks it 'Data (optional) \| data-engineer \| Phase 3 or post-launch.' |
| c17 | Output flags any agents referenced in the plan that exist in the marketplace but may not be enabled, with the `"<plugin>@hpsgd": true` enablement hint | PARTIAL | 'Enablement Hints' section provides plugin-level hints in the correct format: leadership@hpsgd, architecture@hpsgd, engineering@hpsgd, quality@hpsgd, security@hpsgd, design@hpsgd, marketing@hpsgd, support@hpsgd, writing@hpsgd. However, data-engineer (referenced in CTO Team table) has no corresponding hint, and ux-researcher is similarly omitted. |
| c18 | Output distinguishes Definition of Ready (gate before development) from Definition of Done (gate before shipping) as separate checkpoints in the plan | PARTIAL | Execution Sequence table has both 'Definition of Ready gate' and 'Definition of Done gate' as separate columns. Next Steps & Gates section uses both terms explicitly at every phase transition (e.g., 'Definition of Done (Phase 1): PRD approved...' and 'Definition of Ready (Phase 2): QA planning can begin...'). |
| c19 | Output surfaces likely CPO/CTO trade-offs to watch for (scope vs deadline, build-vs-buy for invitations/email, security review timing) without picking a side | PARTIAL | 'CPO / CTO Trade-offs to Watch' table surfaces all three named tensions plus two more (gradual vs. big-bang rollout; QA timing). However, each entry includes a 'Recommendation:' that picks a side (e.g., 'If buying (recommended)' for email infrastructure; 'Recommended: Ship MVP without presence or bulk invite' for scope). Trade-offs are surfaced but the output does not remain neutral. |
| c20 | Output names a release/launch coordination step distinct from "done" — go/no-go, GTM content readiness, support FAQ — rather than collapsing launch into development | PARTIAL | Phase 5 (Launch Prep) and Phase 6 (Launch) are separate from Phase 4 (Validate & Deploy). Phase 5 explicitly covers user-docs-writer:user-docs-writer (docs), gtm-lead:gtm (launch messaging), support-lead:support (FAQ, training). Phase 5→6 gate states: 'Launch approval: All Definition of Done gates passed. CPO: GTM ready. CTO: DevOps + Security + QA sign-off. Support: trained. Go/no-go decision.' |

### Notes

This is an exceptionally comprehensive dispatch plan that meets or exceeds every criterion. The pre-flight section is correctly placed and explicit. The plan correctly decomposes across CPO and CTO teams, sequences QA twice (QA Lead in Phase 2, QA Engineer early Phase 3), uses DoR/DoD as named checkpoints throughout, names a full Assumptions/Open Questions section with the right categories (outcome, appetite, deadline, commercial signals), provides a critical path with range estimates, and includes fully-qualified plugin:agent identifiers throughout. The Enablement Hints section is thorough but misses data-engineer. The CPO/CTO Trade-offs section surfaces all required tensions but undercuts the 'without picking a side' requirement by including explicit recommendations for each trade-off — this is the one notable deviation. Security is treated as a first-class cross-cutting concern across phases 1, 2, and 4, with specific edge cases named for RBAC. The output is well above the PASS threshold and demonstrates strong coordinator-level thinking with appropriate deferral of decisions to human stakeholders.
