# Cross Domain Dispatch

Scenario: A user brings a multi-domain feature launch request requiring product, design, engineering, and launch work. Does the coordinator decompose it correctly and produce a structured dispatch plan without making unilateral decisions?

## Prompt

> We need to ship a new "Team Workspaces" feature for Flowbase before the end of the quarter. It lets multiple users collaborate inside a shared workspace — they can invite members, assign roles (admin/editor/viewer), and work on the same projects together. We need the whole thing: specs, designs, backend, frontend, tests, deployment, and launch content. Can you coordinate this?
> 
> Do not ask for clarification — proceed based on the information provided. Produce the dispatch plan now, noting any assumptions you make.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll work through the mandatory decomposition process systematically.

---

# Initiative Decomposition: Team Workspaces for Flowbase

## Step 1: Initiative Context

| Question | Answer |
|---|---|
| **User problem** | Flowbase teams (2–10 person groups) need to collaborate on shared projects but lack workspace-level organization, member management, and role-based access control. Currently, projects are owned by individuals with no built-in sharing or permission delegation. |
| **Target user** | Mid-size teams (3–8 members) working on shared projects in Flowbase who need to invite collaborators and control permissions without sharing account credentials. |
| **Success criteria** | • 30% of monthly active users create a team workspace within 60 days of launch<br>• Average team workspace has 3+ members<br>• 70% of team workspaces show collaborative activity (2+ members editing weekly)<br>• Feature launches with sub-100ms latency on member list / role update operations<br>• Zero security regressions (no unintended permission leaks)<br>• 95% of support tickets are FAQ-addressable (permissioning questions) |
| **Appetite** | **Hard deadline: June 30, 2026 (end of Q2)**<br>Calendar: 29 days remaining. Working time: ~20 days at 5-day weeks. Requires heavy parallelization to compress 6–8 weeks of work into this window. |
| **Constraints** | • Hard launch deadline (quarter-end)<br>• Must preserve backward compatibility (existing individual project ownership)<br>• Requires core schema changes (workspaces, members, role assignments)<br>• Must support zero-downtime migration of existing projects<br>• RBAC enforcement must be pervasive (every API endpoint checks permissions)<br>• No scope creep into "teams" beyond workspaces (sub-teams, hierarchies out of scope) |

---

## Step 2: Identify Workstreams

### CPO Team Workstreams

| Workstream | Owner role | Initiative-specific deliverables | Relevant? | Why |
|---|---|---|---|---|
| **Product** | product-owner | PRD: workspace creation UX, member invite flow, role permission matrix (admin/editor/viewer), acceptance criteria for each role, project ownership transfer rules, backward-compat strategy | **YES** | Core blocker for all other teams. Must define permission semantics upfront. |
| **Design** | ui-designer | UX flows: workspace setup wizard, member management UI (invite/remove/role change), project sharing dialog, permission error states; accessibility audit; component specs for role selector | **YES** | Development and GTM both need finalized designs; directly impacts frontend velocity. |
| **Content** | user-docs-writer | Docs: workspace onboarding guide, permission model explanation, inviting members, role responsibilities, troubleshooting permission denials, FAQ on shared project behavior | **YES** | Launch blocker. Customers need clear docs on unfamiliar permission model. Support will reference extensively. |
| **GTM** | gtm-lead | Positioning: "Collaborate with your team" messaging, launch announcement (email, product blog, in-app banner), pricing implications if any (free tier workspace limits?), launch timeline communication | **YES** | Launch coordination. Must be ready to announce on June 30. |
| **Support** | support-lead | FAQ preparation, support runbook for permission troubleshooting, known issues list, training on new workspace features, escalation paths for permission disputes | **YES** | Post-launch operational readiness. Team must handle surge of permission-related tickets. |
| **Research** | ux-researcher | Quick validation: usability testing on permission model (do customers understand admin/editor/viewer?), validation of role semantics with target users | **NO** | Time-constrained. Assume roles are correct based on product team expertise; post-launch feedback will validate. Research can iterate post-launch. |

### CTO Team Workstreams

| Workstream | Owner role | Initiative-specific deliverables | Relevant? | Why |
|---|---|---|---|---|
| **Architecture** | architect | System design doc: workspace and member entities, RBAC enforcement patterns, API contracts (CreateWorkspace, InviteMember, UpdateRole, ListMembers), data model + migrations, permission check placement (middleware vs. per-endpoint) | **YES** | Blocks development and DevOps. Must define schema and API boundaries upfront. |
| **Development (Backend)** | backend-lead | Workspace CRUD APIs, member management (invite/remove/role change), RBAC checks on all project/resource endpoints, permission enforcement, audit logging for permission changes | **YES** | Core feature. 40–50% of effort. |
| **Development (Frontend)** | frontend-lead | Workspace selector UI, settings page (manage members, roles, workspace name), invite link handling, permission error UX, updated project sharing dialogs, role badges | **YES** | User-facing feature. 30–40% of effort. Must be intuitive. |
| **QA Planning** | qa-lead | Test strategy: RBAC edge cases (admin creates resource, editor deletes own, viewer tries to edit), permission inheritance rules, role boundary violations, concurrent member changes, backward-compat scenarios (old projects with no workspace) | **YES** | RBAC is high-risk; must have comprehensive test coverage. |
| **QA Execution** | qa-engineer | Automated tests: permission enforcement (unit + integration), role isolation, API boundary tests, backward-compat smoke tests, performance tests on member list / role update | **YES** | Launch blocker. Can't ship with permission bypass bugs. |
| **DevOps** | devops-lead | Database migration strategy (zero-downtime), deployment plan (feature flag for new endpoints, gradual rollout?), monitoring for permission denials, rollback plan if issues surface, performance baselines | **YES** | Deployment blocker. Schema migration on live database is risky. |
| **Security** | security-engineer | Threat model: workspace isolation (can user A see user B's workspace?), permission bypass risks, audit trail for access changes, data exfiltration via roles, RBAC collision edge cases (same email invited twice?) | **YES** | High-risk feature. Permission bugs are security bugs. Must review before launch. |
| **Data** | data-engineer | Workspace adoption tracking, member invite success rate, role distribution (how many admins vs. editors vs. viewers), feature usage dashboards, analytics events for key user flows | **YES** | Post-launch metrics needed for success evaluation. Instrumentation must ship with feature. |

---

## Step 3: Dependency Map

| Workstream | Depends on | What it needs before starting | Blocks |
|---|---|---|---|
| **Product** | — | — | Architecture, Design, Development, GTM, Content |
| **Architecture** | Product | PRD with acceptance criteria, role semantics, API requirements | Backend dev, Frontend dev, DevOps, Security |
| **Design** | Product | Requirements and user flows from PRD | Frontend dev, GTM, Content |
| **Security threat model** | Architecture | Schema and API design | Architecture sign-off, permission enforcement implementation |
| **Backend dev** | Architecture + Security threat model review | API contracts, schema, threat model addressing | QA execution, DevOps validation |
| **Frontend dev** | Design + Backend (for API availability) | Wireframes and component specs, backend endpoints ready | QA, GTM final messaging |
| **QA Planning** | Product + Architecture | Acceptance criteria, API design | QA execution |
| **QA Execution** | Backend + Frontend + QA test plan | Working implementation in staging | Launch decision |
| **DevOps** | Architecture + Backend | Migration scripts, deployment endpoints | Launch decision |
| **Content** | Frontend + QA | Working feature for screenshots, finalized docs | Launch |
| **GTM** | Design + Frontend (final UX) | Positioning, finalized feature visuals | Launch coordination |
| **Support** | Content + QA + Backend | Docs and known issues, permission model clarity | Launch readiness |
| **Data** | Backend + Frontend | Analytics events instrumented in code | Launch readiness |

---

## Step 4: Execution Sequence

| Phase | Workstreams (parallel) | Duration | Gate to next phase |
|---|---|---|---|
| **1 — Define** | Product, Architecture, Security threat model | 1 week (May 6–10) | PRD approved with role matrix; schema design + API contracts reviewed; threat model reviewed; architecture signed off |
| **2 — Prep** | Design, QA Planning, DevOps (migration plan), Data (analytics plan) | 0.5 weeks (May 9–13, overlapping) | Design specs finalized; test strategy approved; migration strategy approved; analytics events defined |
| **3 — Build** | Backend dev, Frontend dev, Security review of impl | 2.5 weeks (May 13–27) | Core features implemented in staging; RBAC enforcement complete; security review passed; tests written and passing |
| **4 — Validate** | QA execution, DevOps validation, Content, GTM, Support prep | 1 week (May 27–June 3) | Tests passing; deployment validated in staging; docs written; launch plan finalized; support trained |
| **5 — Launch** | Coordinated release + monitoring | 3 days (June 3–6) | Feature live; monitoring confirms no permission errors; adoption metrics baseline |
| **6 — Buffer** | Post-launch support, issue response | 24 days (June 6–30) | Roll up for end-of-quarter, prepare for next iteration or rollback if critical issues |

### Critical Path
**Product → Architecture → Backend dev → QA Execution → Launch**
- Minimum serial duration: 1 + 0.5 + 2.5 + 1 = 5 weeks = 25 working days
- Calendar: May 6 → June 3 ✓ (fits in 29-day window with buffer)

### Parallel Opportunities
- **Design, QA Planning, DevOps, Data** all start as soon as Architecture baseline is approved (overlap with backend work).
- **Frontend dev** runs parallel to Backend (API-first contracts enable this).
- **Security threat model** runs early (Phase 1) and final review in Phase 3 (doesn't block implementation start).
- **Content, GTM, Support** run late-phase in parallel (all depend on completed feature, not implementation details).

### Why This Works
- **Parallel reduces delay**: Design + Backend + Frontend can run in tandem (2.5 weeks instead of 5).
- **Gates prevent rework**: Each phase gate ensures downstream teams have what they need; no mid-cycle spec changes.
- **Security is integrated, not a bottleneck**: Threat modeling starts early, final review is lightweight.

---

## Step 5: Summary

### Workstream Summary

| Workstream | Owner | Depends on | Key deliverables | Phase | Estimated effort |
|---|---|---|---|---|---|
| **Product** | product-owner | — | PRD with role matrix, acceptance criteria, user flows, backward-compat plan | 1 | 3–4 days |
| **Architecture** | architect | Product | System design, schema, API contracts, RBAC enforcement pattern, security checklist | 1 | 3–4 days |
| **Security (Threat Model)** | security-engineer | Architecture | Threat model, permission isolation checklist, audit logging requirements | 1 | 2–3 days |
| **Design** | ui-designer | Product | Wireframes, component specs, accessibility review, error state designs | 2 | 3–4 days |
| **QA Planning** | qa-lead | Product + Architecture | Test strategy, edge case matrix, acceptance criteria mapping | 2 | 2–3 days |
| **DevOps** | devops-lead | Architecture | Migration scripts, deployment plan, feature flag strategy, monitoring setup | 2 | 2–3 days |
| **Data** | data-engineer | Backend sketch | Analytics event definitions, dashboard mockups | 2 | 1–2 days |
| **Backend Development** | backend-lead | Architecture + Security | CRUD APIs, RBAC enforcement, audit logging, staging-ready code | 3 | 8–10 days |
| **Frontend Development** | frontend-lead | Design + Backend APIs | UI implementation, permission error handling, role-based UX, staging-ready | 3 | 6–8 days |
| **Security (Implementation Review)** | security-engineer | Backend + Frontend code | Permission bypass audit, data isolation verification, sign-off | 3 | 1–2 days |
| **QA Execution** | qa-engineer | Backend + Frontend + QA plan | Automated tests, manual testing, known issues list, final regression | 4 | 4–5 days |
| **DevOps Validation** | devops-lead | Backend + Frontend | Staging deployment, migration dry-run, rollback test, perf validation | 4 | 2–3 days |
| **Content** | user-docs-writer | Frontend + QA | Onboarding guide, permission model docs, troubleshooting FAQ, help articles | 4 | 2–3 days |
| **GTM** | gtm-lead | Design + Frontend final UX | Positioning copy, launch announcement, in-app messaging, email template | 4 | 1–2 days |
| **Support** | support-lead | Content + QA + Backend | Support runbook, FAQ, training session notes, escalation matrix | 4 | 1–2 days |

### Timeline Estimate

| Scenario | Duration | Calendar dates |
|---|---|---|
| **Best case** (no blockers, clean execution) | 25 working days | May 6 → June 3 ✓ |
| **Likely case** (1 phase slips 3–5 days) | 28–30 working days | May 6 → June 6–10 (may extend past ideated launch) |
| **Risk case** (schema issues, security findings) | 35+ working days | Deadline at risk |

### Risk Factors & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Schema migration on live DB fails or is slow | Deployment blocked; potential data loss | Early dry-run (DevOps Week 2), small batch rollout (feature flag), rollback plan tested |
| Permission bypass found late in QA | Must rework backend; launch delay | Security involved early (Phase 1), threat model informs design, implementation review in Phase 3 |
| Product spec changes mid-cycle | Rework cascades to design, backend | Lock PRD in Phase 1 gate; treat scope changes as post-launch features |
| Frontend complexity underestimated | Frontend dev extends; blocks QA | Prototype invite flow early (Week 2), reduce scope if needed (admin-only invite in v1, public in v2) |
| Database performance issues under load | QA uncovers slowness; migration needed | Load test member list / role update endpoints in Phase 3; index strategy defined in Architecture |
| Support team unprepared | Launch-day chaos | Training scheduled for Week 4; runbook finalized by Phase 4 gate |

---

## Dispatch Plan Summary

### Team Assignments (Assumed)
- **Product Lead**: Define workspace semantics, role matrix, UX requirements
- **Architect**: Schema, API design, RBAC pattern, data model decisions
- **Backend Lead**: Implement CRUD, permission enforcement, audit logging
- **Frontend Lead**: Workspace selector, settings UI, member management UX
- **QA Lead + QA Engineer**: Test plan, automated testing, staging validation
- **DevOps Lead**: Migration, deployment, monitoring
- **UI Designer**: Wireframes, components, accessibility
- **Security Engineer**: Threat model, implementation review
- **Data Engineer**: Analytics instrumentation
- **Content Writer**: Docs, help center, onboarding
- **GTM Lead**: Launch messaging, announcement
- **Support Lead**: FAQ, runbook, training

### Immediate Actions (This Week)
1. **Assign owners** to each workstream (from above table)
2. **Kick off Product + Architecture sync** on May 6 to lock PRD and schema by end of week
3. **Schedule Phase 1 gate review** for May 10 (PRD, schema, threat model checkpoints)
4. **Communicate timeline internally**: June 3 soft launch target, June 30 hard deadline, heavy parallelization, no scope changes mid-cycle
5. **Create CLAUDE.md for Team Workspaces project** (shared context document for all teams)

### Follow-ups (After This Decomposition)
- [ ] Define OKRs for workspace adoption, collaboration depth, permission model accuracy — use `/coordinator:define-okrs`
- [ ] Create detailed PRD with user stories and acceptance criteria (Product owner, Week 1)
- [ ] Write architecture ADR (schema, RBAC pattern, migration strategy) — Architect, Week 1
- [ ] Schedule weekly sync (Tuesday 10am?) for phase gate reviews and blocker resolution

---

**Assumptions in this plan:**
1. All workstream owners are available full-time for their assigned phase duration
2. "Existing projects with no workspace" can be auto-assigned to a personal workspace (backward-compat without manual migration)
3. Roles are admin/editor/viewer (no future extensibility assumed)
4. Public shared links (workspace-level sharing) are post-launch
5. Audit logging is informational only (no compliance requirement for retention)
6. Single workspace per user (no multi-workspace support in v1)

## Evaluation

| Field | Value |
|---|---|
| Verdict | PARTIAL |
| Score | 12.5/16.5 (76%) |
| Evaluated | 2026-05-02 |
| Target duration | 70604 ms |
| Target cost | $0.0820 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Performs pre-flight checks — reads CLAUDE.md/project conventions and checks available agents before doing anything else | FAIL | The output opens with 'I'll work through the mandatory decomposition process systematically' and immediately enters the decomposition tables. No mention of reading CLAUDE.md, checking project conventions, or inventorying available agents anywhere in the output. |
| c2 | Produces a structured dispatch plan listing agents to invoke in sequence (not executing directly) | PASS | The 'Execution Sequence' table (Step 4) lists phases with parallel workstreams, gate conditions, and calendar dates. The 'Immediate Actions' section further structures who does what first. The plan describes what to dispatch in what order without executing any of it. (Format issue with invocation syntax is assessed separately under c10.) |
| c3 | Decomposes work across both CPO team (product, design, content, GTM) and CTO team (architecture, development, QA, DevOps, security) | PASS | Step 2 explicitly splits into 'CPO Team Workstreams' (Product, Design, Content/user-docs-writer, GTM, Support, Research) and 'CTO Team Workstreams' (Architecture, Backend dev, Frontend dev, QA Planning, QA Execution, DevOps, Security, Data). All named domains are covered. |
| c4 | Identifies dependencies between workstreams — specifically that architecture and product must precede development | PASS | Step 3 'Dependency Map' shows Architecture depends on Product ('PRD with acceptance criteria, role semantics, API requirements') and Backend dev depends on 'Architecture + Security threat model.' The Execution Sequence confirms Phase 1 (Product + Architecture) gates Phase 3 (Build). |
| c5 | Applies the 3-amigos sequencing pattern: product + architecture + QA lead before development starts | PASS | Phase 1 covers Product + Architecture + Security (threat model). Phase 2 adds QA Planning (qa-lead: 'Test strategy, edge case matrix, acceptance criteria mapping'). Development (backend + frontend) is Phase 3. All three roles appear in phases before development begins. |
| c6 | Does not make unilateral product or technical decisions — routes product decisions to CPO, technical decisions to CTO | PASS | Deliverables are consistently routed to named role owners (product-owner, architect, security-engineer, etc.). Items that could be unilateral decisions are isolated in an 'Assumptions in this plan' section at the end (e.g., 'Single workspace per user (no multi-workspace support in v1)'), framing them as assumptions to be validated rather than final decisions. |
| c7 | Checks Definition of Ready criteria before marking work as ready to start | PASS | Each phase in the Execution Sequence has an explicit 'Gate to next phase' column. Phase 1 gate lists 'PRD approved with role matrix; schema design + API contracts reviewed; threat model reviewed; architecture signed off' — a multi-item readiness checklist before development is permitted to start. |
| c8 | Identifies the security workstream as relevant (auth, roles, access control are explicitly in scope) | PARTIAL | Security appears as two distinct workstreams: 'Security (Threat Model)' in Phase 1 with threat model covering 'workspace isolation, permission bypass risks, audit trail for access changes, data exfiltration via roles, RBAC collision edge cases,' and 'Security (Implementation Review)' in Phase 3 for 'permission bypass audit, data isolation verification, sign-off.' |
| c9 | Escalates to the human on a CPO vs CTO conflict — only relevant if a conflict is simulated | SKIP | No CPO vs CTO conflict was simulated in the scenario. |
| c10 | Output uses fully-qualified `plugin:agent` invocation format (e.g., `cpo:cpo`, `cto:cto`, `architect:architect`) rather than bare names | FAIL | All owner references throughout the output use bare hyphenated role labels: 'product-owner', 'architect', 'backend-lead', 'frontend-lead', 'qa-lead', 'qa-engineer', 'devops-lead', 'ui-designer', 'security-engineer', 'data-engineer', 'user-docs-writer', 'gtm-lead', 'support-lead'. No plugin:agent format (e.g., cpo:cpo, architect:architect) appears anywhere. |
| c11 | Output asks clarifying questions about outcome, appetite, deadline, or commercial signals before committing to a plan (e.g., what "before end of quarter" means, what success looks like beyond shipping) | FAIL | The output asks no clarifying questions whatsoever. It proceeds directly to decomposition per the user's instruction 'Do not ask for clarification.' It does not even note what questions would normally be asked. The success metrics, appetite, and deadline are inferred and asserted unilaterally without surfacing them as open questions. |
| c12 | Output explicitly identifies a critical path through dependent workstreams and gives a minimum timeline range (e.g., "6–8 weeks") rather than a single point estimate | PASS | The 'Critical Path' section states 'Product → Architecture → Backend dev → QA Execution → Launch' with 'Minimum serial duration: 1 + 0.5 + 2.5 + 1 = 5 weeks = 25 working days.' The Timeline Estimate table gives three scenarios: Best case 25 days, Likely case 28–30 days, Risk case 35+ days — a range rather than a single estimate. |
| c13 | Output frames work for leads at the right level (e.g., "CPO needs a PRD for Team Workspaces") rather than instructing specialists directly with low-level tasks | PASS | Workstream assignments target leads: 'product-owner' gets 'PRD with role matrix, acceptance criteria, user flows, backward-compat plan'; 'architect' gets 'System design, schema, API contracts, RBAC enforcement pattern.' Immediate Actions says 'Kick off Product + Architecture sync on May 6 to lock PRD and schema by end of week' — lead-level coordination, not low-level task assignment. |
| c14 | Output sequences QA twice — QA Lead in the planning/3-amigos phase and QA Engineer writing acceptance tests before development | PARTIAL | QA is sequenced twice: qa-lead in Phase 2 ('Test strategy, edge case matrix, acceptance criteria mapping') and qa-engineer in Phase 4 ('Automated tests, manual testing, known issues list, final regression'). However, the criterion requires the QA Engineer to write acceptance tests *before* development, while the output places qa-engineer only in Phase 4, after Phase 3 development. Phase 2 acceptance criteria writing is assigned to qa-lead, not qa-engineer. |
| c15 | Output names specific edge cases or anti-requirements relevant to roles/permissions (e.g., role downgrade behaviour, last-admin removal, invite expiry, viewer write-attempt handling) | PASS | QA Planning deliverables include 'RBAC edge cases (admin creates resource, editor deletes own, viewer tries to edit), permission inheritance rules, role boundary violations, concurrent member changes, backward-compat scenarios (old projects with no workspace).' Security threat model lists 'RBAC collision edge cases (same email invited twice?).' These cover viewer write-attempt, role boundary violations, and collision scenarios. |
| c16 | Output flags data-engineering and analytics work (event tracking for invites accepted, role changes, workspace activation) rather than treating it as implicit | PASS | Data is a named workstream (data-engineer, Phase 2–3) with explicit deliverables: 'Workspace adoption tracking, member invite success rate, role distribution (how many admins vs. editors vs. viewers), feature usage dashboards, analytics events for key user flows.' The success criteria also define adoption metrics requiring instrumentation. |
| c17 | Output flags any agents referenced in the plan that exist in the marketplace but may not be enabled, with the `"<plugin>@hpsgd": true` enablement hint | FAIL | No enablement hints, marketplace references, or `"<plugin>@hpsgd": true` syntax appear anywhere in the output. The output does not mention agent availability, plugin enablement, or how to activate any referenced capabilities. |
| c18 | Output distinguishes Definition of Ready (gate before development) from Definition of Done (gate before shipping) as separate checkpoints in the plan | PARTIAL | Phase gates functionally separate these: Phase 1 gate ('PRD approved, schema reviewed, threat model reviewed, architecture signed off') acts as a DoR for development. Phase 4 gate ('Tests passing; deployment validated in staging; docs written; launch plan finalized; support trained') acts as a DoD for shipping. However, the terms 'Definition of Ready' and 'Definition of Done' are never used explicitly, and the distinction is implied through phase structure rather than named as a pattern. |
| c19 | Output surfaces likely CPO/CTO trade-offs to watch for (scope vs deadline, build-vs-buy for invitations/email, security review timing) without picking a side | PARTIAL | The Risk Factors table surfaces 'Product spec changes mid-cycle → scope changes as post-launch features' (scope vs. deadline) and 'Frontend complexity underestimated → reduce scope if needed (admin-only invite in v1, public in v2).' GTM notes 'pricing implications if any (free tier workspace limits?).' However, build-vs-buy for invitation/email infrastructure is not mentioned, and the trade-offs are not framed explicitly as CPO/CTO tensions. |
| c20 | Output names a release/launch coordination step distinct from "done" — go/no-go, GTM content readiness, support FAQ — rather than collapsing launch into development | PARTIAL | Phase 5 is labelled 'Launch — Coordinated release + monitoring' as a distinct phase separate from Phase 4 'Validate.' GTM is a named workstream (Phase 4) producing 'Positioning copy, launch announcement, in-app messaging, email template.' Support is a separate workstream producing 'Support runbook, FAQ, training session notes.' These are distinct from development completion in Phase 3. |

### Notes

The output demonstrates strong domain competency — the decomposition is thorough, the dependency map is well-reasoned, the critical path is identified, and both CPO and CTO domains are covered with appropriate granularity. However, three significant gaps drag the score down: (1) no pre-flight checks whatsoever (c1); (2) complete absence of plugin:agent invocation format, using bare role labels throughout (c10); and (3) no clarifying questions or even acknowledgment of what would normally be asked before proceeding (c11). The output also misses the pattern of placing QA Engineer before development for acceptance-test writing (c14) and has no marketplace/enablement hints (c17). Strengths include the explicit phase gates as readiness criteria, the distinct launch coordination phase, data/analytics as a named workstream, and meaningful permission edge cases in the QA plan.
