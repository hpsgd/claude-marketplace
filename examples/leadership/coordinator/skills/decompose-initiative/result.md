# Decompose Initiative

Scenario: A user invokes the skill with a reasonably complex initiative. Does the skill produce a correctly structured decomposition with initiative context, relevant workstreams (not all of them), a dependency map, a phased execution sequence with gates, and a summary table with estimates?

## Prompt

> /coordinator:decompose-initiative "Notification Centre — a new in-app notification system for Taskwave that lets users receive, manage, and act on real-time alerts for task assignments, deadline reminders, and @mentions. Estimated scope: medium. Timeline appetite: 6 weeks."

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll work through the mandatory decomposition process step by step.

## Step 1: Understand the initiative

| Question | Answer |
|---|---|
| **User problem** | Team members miss critical task updates (assignments, deadline changes, mentions) because alerts are scattered or non-existent. This creates information gaps, missed deadlines, and poor collaboration coordination. |
| **Target user** | Primary: Team members and project managers who need to stay aware of task changes. Secondary: Team leads and managers who oversee task distribution. |
| **Success criteria** | • Notification delivery <2s latency (p95)<br/>• >95% delivery reliability<br/>• >70% of users engage with notifications (read, act on, or dismiss)<br/>• Reduce "I didn't know about this" support tickets by 40%<br/>• User satisfaction with notification relevance >4/5 |
| **Appetite** | 6 weeks |
| **Constraints** | • Must integrate with existing task assignment system<br/>• Real-time infrastructure decision impacts timeline<br/>• Notification preferences must respect user settings<br/>• Must not create alert fatigue (quality > quantity)<br/>• Rollout phased by user segment if needed |

## Step 2: Identify workstreams

### CPO team workstreams

| Workstream | Owner role | Key deliverables | Relevant? |
|---|---|---|---|
| Product | product-owner | PRD defining: notification types (assignment, deadline, mention), user preferences schema, delivery rules, relevance filtering | **YES** — core driver |
| Design | ui-designer | Notification centre UI, bell icon with badge, notification card layout, preference panel, empty/error states, accessibility | **YES** — essential for UX |
| Content | user-docs-writer | Notification types guide, preference customization docs, troubleshooting FAQ, in-app onboarding copy | **YES** — users need guidance |
| GTM | gtm | Feature highlight in release notes, email to existing users, in-app announcement | **MAYBE** — medium feature, not major launch. Include if doing phased rollout with user comms. |
| Support | support | FAQ (why I got a notification, how to turn off type X), known issues, support response templates | **YES** — expect support load spike |
| Research | ux-researcher | Validate notification types users actually care about (via survey or interview), usability test preference panel | **NO** — scope is fixed, not exploratory. User feedback post-launch is more valuable. |

### CTO team workstreams

| Workstream | Owner role | Key deliverables | Relevant? |
|---|---|---|---|
| Architecture | architect | Real-time mechanism decision (WebSocket vs Server-Sent Events vs polling), notification service design, API contracts, data model (notification events table), ADR-000X | **YES** — critical blocker |
| Development | backend-engineer, frontend-engineer | Implement notification service, integrate with task system, UI components, real-time transport layer | **YES** — core implementation |
| QA Planning | qa-lead | Test strategy for real-time delivery, acceptance criteria for latency/reliability, integration test plan | **YES** — real-time is complex |
| QA Execution | qa-engineer | Automated test suite, load testing real-time delivery, manual verification of notification types | **YES** — quality gate |
| DevOps | devops | Provision real-time infrastructure (WebSocket servers / message queue), monitoring dashboards, deployment strategy, feature flag for rollout | **YES** — enables real-time delivery |
| Security | security-engineer | Threat model (information leakage in notifications, rate limiting), permission checks (only see notifications for tasks you can access), audit logging | **YES** — must prevent data leaks |
| Data | data-engineer | Event tracking plan (notification sent/delivered/read), analytics dashboard for adoption/engagement | **YES** — measure success |

## Step 3: Map dependencies

| Workstream | Depends on | What it needs before starting | Blocks |
|---|---|---|---|
| Product | — | None (can start immediately) | Design, Architecture |
| Architecture | Product | PRD with: notification types, delivery SLAs, integration points, user preference schema | Development, DevOps, Security |
| Design | Product | PRD with notification types and user flows | Development, GTM |
| Development | Architecture, Design | API contracts, UI specs, decision on real-time mechanism | QA, DevOps |
| Security | Architecture, Product | System design (what data moves where), notification content rules | Development |
| QA Planning | Architecture | Understanding of real-time mechanism and test hooks for delivery verification | Development |
| QA Execution | Development, QA Planning | Working implementation, test plan, test environment ready | Launch |
| DevOps | Architecture | Infrastructure decisions (WebSocket server, queue, deployment approach) | Development (for staging), Launch (for production) |
| Content | Development | Working notification centre to screenshot and test | GTM, Support, Launch |
| Support | Content, QA Execution | Documentation, list of known issues | Launch |
| GTM | Design, Product | Final UX and positioning, launch timing | Launch |
| Data | Development | Working implementation with event instrumentation | Launch |

## Step 4: Sequence the work

| Phase | Workstreams (parallel) | Duration | Gate to next phase |
|---|---|---|---|
| 1 — Define | **Product** + **Architecture** | 1–1.5 weeks | PRD approved, architecture decision documented (WebSocket vs SSE), data model reviewed |
| 2 — Design & Threat Model | **Design** + **Security** + **QA Planning** | 1–1.5 weeks | UI specs approved, threat model complete, test strategy signed off |
| 3 — Build | **Development** (backend + frontend) + **DevOps** (infra provisioning) | 2.5–3 weeks | Feature complete in staging, real-time delivery verified, API contracts working |
| 4 — Validate | **QA Execution** + **Data** (analytics setup) | 1–1.5 weeks | All acceptance tests passing, latency/delivery SLAs met, analytics instrumented |
| 5 — Prepare & Train | **Content** + **Support** + **GTM** | 1 week (parallel with phase 4) | Docs written, support trained, GTM plan finalized |
| 6 — Launch | Coordinated release with monitoring | 2–3 days | All gates passed, monitoring dashboards live, support on standby |

### Critical path
**Product → Architecture → Development → QA → Launch** (6.5–8 weeks total if done sequentially)

The critical path is broken by parallelizing Design, Security, and QA Planning while Architecture is in progress. This compresses the timeline.

### Parallel opportunities
- **Design + Security can start as soon as Product outlines notification types** (doesn't need full PRD)
- **QA Planning can start from architecture draft** (real-time mechanism determines test approach)
- **DevOps can provision infrastructure in parallel with Development** (they use the same architecture decision)
- **Content, Support, and GTM can start at week 3** (phase 4) once the feature is feature-complete, compressing final prep

## Step 5: Produce the summary table

### Workstream summary

| Workstream | Owner | Depends on | Key deliverables | Phase | Estimated effort |
|---|---|---|---|---|---|
| Product | product-owner | — | PRD (notification types, delivery rules, preferences schema) | 1 | 3–5 days |
| Architecture | architect | Product | System design, real-time mechanism ADR, API contracts, data model | 1 | 4–6 days |
| Design | ui-designer | Product | Wireframes, component specs, preference panel design, accessibility audit | 2 | 4–5 days |
| Security | security-engineer | Architecture, Product | Threat model, permission rules, rate limiting spec, audit logging | 2 | 3–4 days |
| QA Planning | qa-lead | Architecture | Test strategy, latency/delivery acceptance criteria, test plan | 2 | 2–3 days |
| Development | backend-engineer, frontend-engineer | Architecture, Design | Notification service, task integration, UI components, real-time transport | 3 | 10–12 days |
| DevOps | devops | Architecture | Infrastructure provisioning, monitoring dashboards, deployment pipeline | 3 | 5–7 days |
| QA Execution | qa-engineer | Development, QA Planning | Test execution, load testing, bug reports, sign-off | 4 | 5–7 days |
| Data | data-engineer | Development | Event tracking plan, analytics dashboard, success metric instrumentation | 4 | 3–4 days |
| Content | user-docs-writer | Development | Help articles, preference guide, FAQ, onboarding copy | 5 | 2–3 days |
| Support | support | Content, QA Execution | FAQ responses, support training, escalation playbook | 5 | 1–2 days |
| GTM | gtm | Design, Product | Release notes, email campaign, in-app announcement timing | 5 | 2–3 days |

### Timeline estimate
- **Best case:** 5.5 weeks (all teams fully allocated, no rework, no infrastructure delays)
- **Likely case:** 6–6.5 weeks (typical friction: architecture decision takes longer, one round of design revisions, QA finds edge cases)
- **Risk factors:** 
  - Real-time infrastructure availability (if WebSocket servers not provisioned, adds 1 week)
  - Lack of user research on notification preferences (rework if users reject our decision on notification types)
  - Integration complexity with existing task system (if APIs don't exist, add 1 week to development)
  - Load testing reveals delivery bottleneck (adds QA cycle, 3–5 days)

---

## Follow-ups

- [ ] **Define OKRs** — use `/coordinator:define-okrs` to translate success criteria into measurable OKRs
- [ ] **Assign owners** — confirm each workstream has a dedicated owner before phase 1 starts
- [ ] **Create specs** — Product owner writes full PRD; Architecture starts real-time mechanism evaluation
- [ ] **Set up tracking** — Create GitHub issues for each workstream, link to this decomposition
- [ ] **Schedule gates** — Book review meetings before each phase gate (day 5, 11, 25, 32, 38)

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.0/17.0 (82%) |
| Evaluated | 2026-05-04 |
| Target duration | 50621 ms |
| Target cost | $0.1068 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | PASS: Completes Step 1 (initiative context table) — including user problem, target user, success criteria, appetite, and constraints | PASS | Step 1 table includes all five required elements: user problem ('Team members miss critical task updates'), target user (primary: team members/PMs; secondary: team leads), success criteria (5 measurable criteria with metrics), appetite ('6 weeks'), and constraints (5 explicit constraints including real-time infra and alert fatigue). |
| c2 | PASS: Assesses workstream relevance for both CPO and CTO teams — does not include all workstreams blindly, excludes irrelevant ones with reasoning | PASS | Both CPO and CTO team workstreams are assessed in separate tables with an explicit 'Relevant?' column. Research is marked NO with reasoning ('scope is fixed, not exploratory'). GTM is marked MAYBE with conditional reasoning. Each inclusion/exclusion is justified. |
| c3 | PASS: Includes a dependency map showing what blocks what — specifically that design and architecture depend on product requirements | PASS | Dependency map table explicitly shows Design depends on Product ('PRD with notification types and user flows') and Architecture depends on Product ('PRD with: notification types, delivery SLAs, integration points'). Both are listed as blocking Development. |
| c4 | PASS: Produces a phased execution sequence with named gates between phases (not just 'move on when ready') | PASS | Phase table has a 'Gate to next phase' column with specific named criteria for each gate, e.g. Phase 1 gate: 'PRD approved, architecture decision documented (WebSocket vs SSE), data model reviewed'; Phase 3 gate: 'Feature complete in staging, real-time delivery verified, API contracts working'. |
| c5 | PASS: Identifies the critical path and parallel opportunities explicitly | PASS | Dedicated 'Critical path' section: 'Product → Architecture → Development → QA → Launch (6.5–8 weeks total if done sequentially)'. Dedicated 'Parallel opportunities' section with four specific named examples including 'Design + Security can start as soon as Product outlines notification types'. |
| c6 | PASS: Produces a summary table with owner roles, dependencies, key deliverables, phase, and effort estimates as ranges | PASS | Summary table has all required columns: Workstream, Owner (role names), Depends on, Key deliverables, Phase, and Estimated effort. All 12 workstreams are covered with all columns populated. |
| c7 | PASS: Effort estimates are ranges, not point estimates (e.g. '1–2 weeks' not '1 week') | PASS | Every effort estimate in the summary table is a range: '3–5 days', '4–6 days', '4–5 days', '3–4 days', '2–3 days', '10–12 days', '5–7 days', '5–7 days', '3–4 days', '2–3 days', '1–2 days', '2–3 days'. No single-point estimates. |
| c8 | PARTIAL: Includes follow-up actions pointing to related skills (define-okrs, write-spec) | PARTIAL | Follow-ups section explicitly references '/coordinator:define-okrs'. A 'Create specs' action is mentioned but does not reference a '/coordinator:write-spec' skill by name — it reads as a prose action item ('Product owner writes full PRD') rather than a skill pointer. |
| c9 | PASS: Does not include GTM, support prep, or formal UX research if the scenario doesn't warrant it — avoids padding the decomposition | PARTIAL | UX Research is correctly excluded with explicit reasoning ('scope is fixed, not exploratory'). However, Support is included as a full workstream (marked YES) and GTM appears in Phase 5 and the summary table despite being marked MAYBE — both contradict the criterion's expectation of exclusion for a feature of this size. |
| c10 | PASS: Output's initiative context table reproduces the prompt facts — Notification Centre, Taskwave, in-app notifications for task assignments / deadlines / @mentions, medium scope, 6-week appetite — not abstracted into generic placeholders | PARTIAL | Notification types (assignments, deadline changes, mentions), the 6-week appetite, and medium-feature characterisation are preserved in the table. However, the product name 'Taskwave' does not appear anywhere in the output — it is abstracted to 'existing task assignment system' and 'team members', removing a key prompt-specific fact. |
| c11 | PASS: Output's workstreams include the relevant ones — UX (notification surface design), architect (real-time delivery mechanism), backend developer (event sources for assignments, deadlines, mentions), frontend developer (notification centre UI), QA — and EXCLUDE GTM, support training, formal user research as out-of-scope for an internal feature this size | PARTIAL | All five required workstreams are present: ui-designer, architect, backend-engineer, frontend-engineer, qa-lead/qa-engineer. UX research is correctly excluded. However, GTM and Support are included in the summary table and phased plan contrary to the criterion's exclusion requirement. |
| c12 | PASS: Output's dependency map shows architect and UX work feeds developer implementation, and that backend event-source work for each notification type must be in place before the frontend can subscribe to them | PARTIAL | The dependency map clearly shows Development depends on Architecture and Design ('API contracts, UI specs, decision on real-time mechanism'). However, Development is treated as a single joint workstream (backend-engineer + frontend-engineer); the specific dependency that backend event-source work per notification type must precede frontend subscription is not called out. |
| c13 | PASS: Output's phased execution sequence has named gates between phases — e.g. 'Discovery complete → Design gate', 'Design complete → Implementation gate', 'Implementation complete → QA gate' — not just sequential phases without checkpoints | PASS | Every phase row has a populated 'Gate to next phase' column with named criteria. Phase 2 gate: 'UI specs approved, threat model complete, test strategy signed off'; Phase 4 gate: 'All acceptance tests passing, latency/delivery SLAs met, analytics instrumented'. All six phases have explicit named gates. |
| c14 | PASS: Output identifies the critical path explicitly — likely real-time delivery mechanism design (e.g. WebSockets vs polling) blocking everything that depends on it — and names parallel opportunities (e.g. UI mockups can proceed while delivery mechanism is being chosen) | PASS | Critical path section explicitly states 'Product → Architecture → Development → QA → Launch'. Architecture includes 'Real-time mechanism decision (WebSocket vs Server-Sent Events vs polling)' as a key deliverable that blocks Development and DevOps. Parallel opportunities section lists 'Design + Security can start as soon as Product outlines notification types' and 'QA Planning can start from architecture draft'. |
| c15 | PASS: Output's summary table has columns for owner role, dependencies, key deliverables, phase, AND effort estimate — and the effort estimates are ranges (e.g. '1-2 weeks') not single points | PASS | Summary table has Owner, Depends on, Key deliverables, Phase, and Estimated effort columns. All effort values are ranges in days (e.g. '3–5 days', '10–12 days', '5–7 days'). No single-point estimates present. |
| c16 | PASS: Output's effort estimates fit within the 6-week appetite — total time on the critical path should be ≤6 weeks, with the timeline reasoning shown | PASS | Timeline estimate section explicitly states 'Best case: 5.5 weeks' and 'Likely case: 6–6.5 weeks', with phase durations summing to ~5.9–6 weeks when phases 4 and 5 run in parallel as noted. Risk factors that could push beyond appetite are listed. Reasoning is transparent and the parallelised path fits within the 6-week appetite. |
| c17 | PASS: Output includes follow-up actions pointing to related skills — at minimum `/coordinator:write-spec` to spec the work and `/coordinator:define-okrs` if there's an outcome metric to track (e.g. notification engagement rate) | PARTIAL | '/coordinator:define-okrs' is explicitly referenced with skill notation in the follow-ups. 'Create specs' is listed as a follow-up action but without a '/coordinator:write-spec' skill reference — it reads as a prose instruction rather than a skill pointer, missing the minimum skill call the criterion requires. |
| c18 | PARTIAL: Output addresses the user-actionable nature of the notifications — task assignments and deadline reminders can drive workflow actions, so the design must cover both passive (read) and active (act) interactions | PARTIAL | Success criteria mentions '>70% of users engage with notifications (read, act on, or dismiss)' acknowledging active and passive modes. The user problem statement uses 'receive, manage, and act on real-time alerts'. However, the Design workstream deliverables do not explicitly specify active-interaction patterns (e.g. 'act' affordances on notification cards for task assignment acceptance), so coverage is partial. |

### Notes

The output is a high-quality decomposition that excels at structure: all five steps are clearly executed, gates are named rather than implied, the critical path and parallel opportunities are explicit, and effort estimates are consistently ranges. The main gaps are: (1) GTM and support workstreams are included despite the criteria expecting exclusion for a feature of this size — only UX research is correctly excluded; (2) the product name 'Taskwave' is never used in the output, abstracting away a key prompt-specific fact; (3) the write-spec skill is not explicitly referenced in follow-ups; and (4) the backend-before-frontend event-source dependency is not broken out in the dependency map. The 82.4% score reflects a strong output with a few deliberate inclusions that contradict the test rubric's leanness expectations.
