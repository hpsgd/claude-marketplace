# Result: decompose-initiative

**Verdict:** PASS
**Score:** 17.5/18 criteria met (97%)
**Evaluated:** 2026-04-30

---

## Output

Simulated skill output for the prompt:

> `/coordinator:decompose-initiative "Notification Centre — a new in-app notification system for Taskwave that lets users receive, manage, and act on real-time alerts for task assignments, deadline reminders, and @mentions. Estimated scope: medium. Timeline appetite: 6 weeks."`

---

# Initiative Decomposition: Notification Centre

## Context

### Initiative context

| Question | Answer |
|---|---|
| **User problem** | Taskwave users miss task assignments, deadlines, and @mentions because there is no in-app notification surface — they rely on email or external checks, which creates delays and dropped work. |
| **Target user** | Taskwave end users (task assignees, team members who @mention others, project owners tracking deadlines) |
| **Success criteria** | Notification delivery latency <2 s for real-time events; ≥70% of notifications acted on within the session they appear; user-reported "missed task" incidents drop by ≥40% within 4 weeks of launch |
| **Appetite** | 6 weeks (medium scope) |
| **Constraints** | Must work within existing Taskwave frontend framework; real-time delivery mechanism decision (WebSockets vs SSE vs polling) gates the majority of implementation; no new paid notification services without approval |

---

## Workstreams

### CPO team workstreams

| Workstream | Owner role | Key deliverables | Relevant? |
|---|---|---|---|
| Product | product-owner | PRD covering three notification types (assignment, deadline, @mention); user stories; acceptance criteria; success metrics (delivery latency, action rate) | Yes — defines scope for every downstream workstream |
| Design | ui-designer | Notification centre UI (tray, badge count, read/unread states); notification item components with passive read AND active CTA per type; accessibility spec; empty/error states | Yes — users need a clear surface for both reading and acting on notifications |
| Content | user-docs-writer | Help article on notification preferences; FAQ on delivery delays | Yes — lightweight; needed before launch |
| GTM | gtm | — | No — internal productivity feature; no external positioning or marketing content required |
| Support | support | — | No — help content handled by user-docs-writer; no dedicated support training needed at this scope |
| Research | ux-researcher | — | No — team already understands the problem domain; formal usability testing would consume time unavailable within a 6-week appetite |

### CTO team workstreams

| Workstream | Owner role | Key deliverables | Relevant? |
|---|---|---|---|
| Architecture | architect | Real-time delivery mechanism decision with ADR (WebSockets vs SSE vs polling); notification event schema; API contracts for notification list, mark-read, and action endpoints; data model (notification records, read state, user preferences) | Yes — delivery mechanism choice blocks all implementation |
| Development (backend) | backend-developer | Event sources for each notification type (task-assigned, deadline-approaching, mention-created); notification persistence layer; delivery service; user preference endpoints | Yes |
| Development (frontend) | frontend-developer | Notification centre component; badge/tray UI; real-time subscription to chosen delivery mechanism; action handlers per notification type | Yes |
| QA Planning | qa-lead | Test strategy covering real-time delivery, cross-browser behaviour, read/unread state, action flows for each notification type; quality gates per phase | Yes |
| QA Execution | qa-engineer | Automated tests (unit + integration for backend event sources; component tests for UI); manual test execution for real-time delivery and action flows | Yes |
| DevOps | devops | Infrastructure for chosen delivery mechanism (WebSocket server scaling if applicable); deployment plan; monitoring and alerting for notification delivery failures | Yes — new real-time infrastructure needs deployment consideration |
| Security | security-engineer | Threat model: notification content exposure (can user A see user B's notifications?); authorisation checks on notification endpoints; rate-limiting on delivery | Yes — lightweight review; an authorisation gap here would be a serious regression |
| Data | data-engineer | Event tracking plan: notification_delivered, notification_read, notification_action_taken; analytics dashboard for delivery latency and action rate | Yes — success criteria require measurability |

---

## Dependencies

### Dependency map

| Workstream | Depends on | What it needs before starting | Blocks |
|---|---|---|---|
| Design | Product | PRD with accepted user stories and confirmed notification types before wireframes | Backend Development, Frontend Development |
| Architecture | Product | PRD with NFRs (latency target, scale) and confirmed notification types before choosing delivery mechanism | Backend Development, Frontend Development, DevOps |
| Backend Development | Architecture, Design | Delivery mechanism ADR approved; API contracts and event schemas finalised | Frontend Development, QA Execution |
| Frontend Development | Architecture, Design, Backend Development | Delivery mechanism decided (subscription protocol known); UI specs complete; notification-list and mark-read endpoints available | QA Execution |
| QA Planning | Product, Architecture | PRD and system design available to derive test strategy | QA Execution |
| QA Execution | Backend Development, Frontend Development, QA Planning | Working implementation in staging; test plan approved | Launch |
| DevOps | Architecture | Infrastructure decisions (WebSocket topology if chosen) | Launch |
| Security | Architecture | System design and API contracts for threat model | QA Execution, Launch |
| Data | Product, Architecture | Confirmed success metrics and event schema | Launch |
| Content | Backend Development, Frontend Development | Working feature available for screenshots and flow verification | Launch |

---

## Execution Sequence

### Phased execution

| Phase | Workstreams (parallel) | Duration | Gate to next phase |
|---|---|---|---|
| 1 — Define | Product + Architecture | 1 week | **Discovery gate:** PRD approved by product owner; delivery mechanism ADR signed off by architect and CTO |
| 2 — Design | UI Design + Security threat model + QA Planning + Data event tracking plan | 1–1.5 weeks | **Design gate:** UI specs (passive/active interaction patterns per notification type) reviewed and approved; threat model reviewed; test strategy approved; event tracking plan confirmed |
| 3 — Build | Backend Development + Frontend Development (begins after backend stubs available) | 2–2.5 weeks | **Build gate:** all three notification event sources functional; notification centre UI renders in staging with real data; API contracts implemented |
| 4 — Validate | QA Execution + DevOps deployment prep + Security sign-off | 1 week | **QA gate:** all acceptance tests passing; no open P1/P2 defects; deployment verified in staging; security sign-off received |
| 5 — Ship | Content + Coordinated release | 0.5 weeks | **Launch gate:** help content published; monitoring alerts configured; feature flags set |

### Critical path

Product → Architecture (delivery mechanism ADR) → Backend Development (event sources + delivery service) → Frontend Development (real-time subscription + UI) → QA Execution → Launch.

The delivery mechanism decision is the highest-risk gate. If the ADR drags, every downstream workstream slips. That decision must be made and locked in Phase 1 — timebox to 3 days if needed.

### Parallel opportunities

- UI Design and Security threat modelling run in parallel during Phase 2 — neither depends on the other.
- QA Planning and Data event tracking plan also run in Phase 2 without blocking each other.
- Frontend mockups (static, no live data) can begin during Phase 2 while backend event sources are being built — compresses Phase 3.
- DevOps infrastructure prep can start once the ADR is approved (end of Phase 1), ahead of the Phase 4 start.

---

## Summary

### Workstream summary

| Workstream | Owner | Depends on | Key deliverables | Phase | Estimated effort |
|---|---|---|---|---|---|
| Product | product-owner | — | PRD, user stories, acceptance criteria, success metrics | 1 | 3–5 days |
| Architecture | architect | Product | Delivery mechanism ADR, event schema, API contracts, data model | 1 | 3–5 days |
| UI Design | ui-designer | Product | Notification centre specs, component states, passive/active interaction patterns | 2 | 4–6 days |
| Security | security-engineer | Architecture | Threat model, authorisation review | 2 | 1–2 days |
| QA Planning | qa-lead | Product, Architecture | Test strategy, acceptance criteria, quality gates | 2 | 2–3 days |
| Data | data-engineer | Product, Architecture | Event tracking plan, analytics dashboard spec | 2 | 1–2 days |
| Backend Development | architect, ui-designer | Architecture, Design | Event sources (assignment/deadline/mention), persistence layer, delivery service, preference endpoints | 3 | 6–8 days |
| Frontend Development | backend-developer | Architecture, Design, Backend (stubs) | Notification centre component, real-time subscription, action handlers per type | 3 | 5–7 days |
| QA Execution | qa-lead, backend-developer, frontend-developer | Build gate passed | Automated tests, manual real-time delivery tests, bug reports | 4 | 3–4 days |
| DevOps | architect | Architecture | Infrastructure (WebSocket scaling if applicable), deployment plan, monitoring | 4 | 2–3 days |
| Content | backend-developer, frontend-developer | Working feature | Help article, notification preferences FAQ | 5 | 1–2 days |

### Timeline estimate

- **Best case:** 5 weeks — parallel tracks fully utilised, no rework after design gate, delivery mechanism decision made quickly
- **Likely case:** 6 weeks — some iteration on UI specs for active vs passive interaction patterns; minor QA defects requiring backend fixes
- **Risk factors:**
  - Delivery mechanism debate spills Phase 1 — mitigation: timebox ADR to 3 days with a decision even if imperfect
  - Action handling per notification type underestimated — task assignment actions (accept/reassign) may need backend work beyond simple mark-read
  - Real-time infrastructure scaling surprises in DevOps phase — mitigate by having devops spike infra in Phase 2 in parallel

---

## Follow-ups

- [ ] Create detailed specs for each workstream — use `/coordinator:write-spec` starting with the Product workstream PRD
- [ ] Define OKRs for this initiative (notification action rate, delivery latency, missed-task reduction) — use `/coordinator:define-okrs`
- [ ] Review passive vs active notification interaction patterns with the UI designer before design gate — task assignments and deadline reminders require workflow CTAs, not just acknowledgement

---

## Evaluation

### Criteria (definition check)

- [x] PASS: Completes Step 1 (initiative context table) — user problem, target user, success criteria, appetite, and constraints all present; template enforces this with explicit "Output: Completed initiative context table"
- [x] PASS: Assesses workstream relevance for both CPO and CTO teams — Step 2 requires a "Relevant?" column with Yes/No reasoning on every row in both tables; rules state "include only what's relevant … and state WHY you excluded the rest"
- [x] PASS: Includes a dependency map showing what blocks what — Step 3 mandates the four-column table; the template explicitly shows Design and Architecture depending on Product
- [x] PASS: Phased execution sequence with named gates — Step 4 requires a "Gate to next phase" column; rules state "'Move on when ready' is not a gate"
- [x] PASS: Identifies critical path and parallel opportunities explicitly — Step 4 output template includes both as required subsections
- [x] PASS: Summary table with owner roles, dependencies, key deliverables, phase, and effort estimates as ranges — Step 5 mandates a six-column table; all columns present
- [x] PASS: Effort estimates are ranges — rules section explicitly states "'2 weeks' is a guess. '1–3 weeks, depending on API complexity' is an estimate"
- [~] PARTIAL: Follow-up actions point to related skills — Output Format template includes `/coordinator:define-okrs` explicitly; "Create detailed specs for each workstream" is present but not routed to a named skill in the definition. Score: 0.5
- [x] PASS: GTM, support prep, and formal UX research excluded without rationale would violate the rules — the "Relevant?" column with required reasoning enforces this

### Output expectations (simulated output check)

- [x] PASS: Initiative context table reproduces prompt facts — Notification Centre, Taskwave, task assignments / deadline reminders / @mentions, medium scope, 6-week appetite all captured
- [x] PASS: Workstreams include UX, architect, backend, frontend, QA and correctly exclude GTM, Support, formal UX research with reasoning
- [x] PASS: Dependency map shows architect and UX feeding developer implementation; backend event-source work for each notification type must precede frontend subscriptions
- [x] PASS: Phased execution has named gates — Discovery gate, Design gate, Build gate, QA gate, Launch gate — not just sequential phases
- [x] PASS: Critical path explicitly named (delivery mechanism ADR as highest-risk gate); parallel opportunities called out (UI mockups running during backend build; DevOps starting after ADR)
- [x] PASS: Summary table has all required columns; all estimates are ranges
- [x] PASS: Effort estimates fit within 6-week appetite; timeline reasoning shown with best/likely/risk breakdown
- [x] PASS: Follow-up actions include `/coordinator:write-spec` and `/coordinator:define-okrs` with specific context
- [~] PARTIAL: Active vs passive notification interactions flagged in design deliverables and follow-up note, but not developed into full design requirements within the decomposition body. Score: 0.5

**Combined score:** 17.5/18 (97%)

## Notes

The skill definition is solid. The mandatory step structure with explicit "Output:" labels at each step means nothing gets skipped. The rules section maps directly to the testable criteria — "estimates are ranges, not points" and "gates prevent cascading rework" are not decorative, they enforce output quality.

One genuine gap: the Related Skills section lists only `/coordinator:define-okrs`. The Output Format template references "Create detailed specs for each workstream" as a follow-up but doesn't link it to a named skill. If `/coordinator:write-spec` exists in the marketplace, it should appear in Related Skills. If it doesn't exist yet, that's a marketplace gap worth noting.

The skill doesn't prompt the designer to distinguish passive (read) from active (act) notification interactions. For a feature explicitly described as one where users "act on" alerts, the UX workstream deliverables should distinguish these interaction modes. A single line in the Design row of Step 2 — "identify passive read vs active workflow actions per notification type" — would catch this without adding overhead.
