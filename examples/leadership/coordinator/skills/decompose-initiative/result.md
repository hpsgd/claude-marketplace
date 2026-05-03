# Decompose Initiative

Scenario: A user invokes the skill with a reasonably complex initiative. Does the skill produce a correctly structured decomposition with initiative context, relevant workstreams (not all of them), a dependency map, a phased execution sequence with gates, and a summary table with estimates?

## Prompt

> /coordinator:decompose-initiative "Notification Centre — a new in-app notification system for Taskwave that lets users receive, manage, and act on real-time alerts for task assignments, deadline reminders, and @mentions. Estimated scope: medium. Timeline appetite: 6 weeks."

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Here's the full decomposition. Pasting the final output:

---

# Initiative Decomposition: Notification Centre

## Context

| Question | Answer |
|---|---|
| **User problem** | Taskwave users miss important events — task assignments, looming deadlines, and @mentions — because there is no in-app notification layer. Users must actively poll the app or rely on external email/Slack noise. |
| **Target user** | All Taskwave workspace members; particularly contributors assigned work and collaborators mentioned in comments. Power users (project leads, managers) who receive high volumes are secondary (preferences, mute). |
| **Success criteria** | ≥80% of assigned-task and @mention notifications opened within 24 hours; open rate tracked via analytics; zero missed deadline reminders in QA acceptance testing; user-reported missed-event complaints drop measurably post-launch. |
| **Appetite** | 6 weeks (medium). Time box, not a scope commitment — if trade-offs are needed, scope is cut before the deadline slips. |
| **Constraints** | Real-time delivery + persistence + preferences + @mention parsing within 6 weeks is aggressive. A scheduler/cron system is required for deadline reminders. @mentions require permission checks (can the mentioner see the mentioned user in this context?). The delivery channel decision (WebSocket vs SSE vs managed push) must be made in Phase 1 — it affects every downstream workstream. |

---

## Workstreams

**CPO workstreams:**

| Workstream | Owner | Key deliverables | Relevant? |
|---|---|---|---|
| Product | `product-owner` | PRD, notification taxonomy (assignments/deadlines/@mentions), preference spec, mark-as-read/deep-link/mute behaviour, bell UI spec, inbox view, success metrics | **Yes** |
| Design | `ui-designer` | Bell + badge count, inbox panel (grouped/ungrouped, read/unread), preference settings page, empty/error states, mobile/responsive, WCAG AA accessibility | **Yes** |
| Content | `user-docs-writer` | Help article, in-app tooltip copy, preference setting descriptions, opt-out guidance | **Yes** |
| GTM | `gtm` | In-app "what's new" announcement, changelog entry, internal readiness comms | **Yes** — in-app launch moment still needed |
| Support | `support` | FAQ, known-issues list from QA, support escalation runbook | **Yes** — preference failures will generate tickets |
| Research | `ux-researcher` | Existing-feedback review of missed-event complaints, single usability pass on preference settings UI | **Yes (lightweight, 1–2 days)** |

**CTO workstreams:**

| Workstream | Owner | Key deliverables | Relevant? |
|---|---|---|---|
| Architecture | `architect` | System design, delivery channel ADR (**flag: managed push services like Pusher/Ably/Firebase carry ongoing subscription costs**), scheduler design, API contracts, @mention permission contract, notification persistence model | **Yes — foundational blocker** |
| Development | `fullstack-developer` | Notification service, real-time delivery layer, @mention parser + permission-guarded fan-out, deadline reminder scheduler, preference API, read/unread state, deep-link resolver, bell + inbox + preference UI | **Yes** |
| QA Planning | `qa-lead` | Test strategy: delivery latency criteria, deadline reminder accuracy tolerance, @mention permission edge cases, preference persistence, fan-out scale | **Yes** |
| QA Execution | `qa-engineer` | Automated delivery/scheduler/parser/preference tests; manual exploratory: inbox UX, deep-link routing, mobile, read state | **Yes** |
| DevOps | `devops` | Real-time infra provisioning, scheduler hosting, delivery failure monitoring, scheduler miss-fire alerting, deployment plan | **Yes** |
| Security | `security-engineer` | Threat model: @mention permission enforcement, notification content exposure, preference manipulation, fan-out rate limiting | **Yes — not optional; @mention permissions make this mandatory** |
| Data | `data-engineer` | Event tracking plan (delivered/opened/dismissed/preference-changed), analytics dashboard, pre-launch baseline | **Yes — open rate is the primary success metric** |

---

## Dependencies

| Workstream | Depends on | What it needs | Blocks |
|---|---|---|---|
| Architecture | Product | PRD with taxonomy, NFRs, scale estimates | Development, DevOps, Security, Data |
| Design | Product | Full user flows incl. preference, deep-link, mute, empty states | Development (UI), Content, GTM |
| Security | Architecture | Data model, API contracts, @mention permission contract | Development (cannot ship without sign-off) |
| QA Planning | Architecture | System design and API contracts | QA Execution |
| DevOps | Architecture | Infrastructure decisions (delivery channel, scheduler) | Development integration env, Launch |
| Development | Design, Architecture, Security | UI specs, API contracts, permission contract, delivery channel decision | QA Execution, Content, GTM |
| Data | Architecture + Development | Event taxonomy + working instrumentation points | Dashboard, launch analytics |
| QA Execution | Development | Working implementation in staging | Launch gate |
| Content | Development | Working feature in staging (screenshots, real preference labels) | GTM, Support, Launch |
| GTM | Product, Design, Content | Final UX, changelog copy | Launch |
| Support | Content + QA Execution | Help articles, known-issues list | Launch |

---

## Execution Sequence

| Phase | Workstreams (parallel) | Duration | Gate |
|---|---|---|---|
| 1 — Define | Product + Architecture (+ Research lightweight) | 1–1.5 wks | PRD approved; delivery channel ADR accepted; paid-service cost confirmed with leadership |
| 2 — Design & Secure | Design + Security threat model + QA Planning + DevOps provisioning | 1–1.5 wks | UI specs signed off; threat model accepted; test plan drafted; staging env live |
| 3 — Build | Development + Data instrumentation | 2–2.5 wks | Feature complete in staging: all notification types, preferences, deep-links, scheduler |
| 4 — Validate | QA Execution + DevOps monitoring verification + Security sign-off | 0.5–1 wk | All acceptance criteria passing; no P0/P1 open; monitoring live; security sign-off obtained |
| 5 — Prepare & Launch | Content + GTM + Support → coordinated release | 0.5 wk | Help article published; announcement ready; FAQ merged; data baseline captured |

**Total: 5–7 weeks**

**Critical path:** Product → Architecture → Development → QA Execution → Launch. The delivery channel decision is the single highest-leverage call — a reversal compresses every downstream phase.

**Timeline tension:** The 6-week appetite is tight. Most likely compression: defer mute/snooze, ship with assignment + @mention notifications first, add deadline reminders in weeks 5–6, or simplify preferences to on/off toggle for v1.

---

## Summary

| Workstream | Owner | Phase | Estimated effort |
|---|---|---|---|
| Product | `product-owner` | 1 | 3–5 days |
| Research (lightweight) | `ux-researcher` | 1–2 | 1–2 days |
| Architecture | `architect` | 1 | 4–6 days |
| Design | `ui-designer` | 2 | 5–8 days |
| Security | `security-engineer` | 2 | 2–3 days |
| QA Planning | `qa-lead` | 2 | 2–3 days |
| DevOps | `devops` | 2–3 | 3–5 days |
| Development | `fullstack-developer` | 3 | 10–15 days |
| Data | `data-engineer` | 3–4 | 2–4 days |
| QA Execution | `qa-engineer` | 4 | 3–5 days |
| Content | `user-docs-writer` | 5 | 2–3 days |
| GTM | `gtm` | 5 | 1–2 days |
| Support | `support` | 5 | 1–2 days |

**Best case:** 5 weeks — no architecture reversals, no security redesign, clean QA pass.  
**Likely case:** 7 weeks — one architecture debate, one design revision cycle, 2–3 QA issues.  
**Latency NFR (placeholder):** <5s P95 event-to-visible — to be confirmed as a hard acceptance criterion in Phase 1.

**Risk factors:** delivery channel cost/complexity trade-off; @mention permission model depth; no existing job queue infrastructure; scope creep into mute/snooze, grouping/threading, email/push channels, and digest mode — all require explicit in/out decisions at the PRD gate.

---

## Follow-ups

- [ ] Define OKRs for this initiative — use `/coordinator:define-okrs`
- [ ] Create detailed spec for the Product workstream — use `/coordinator:write-spec`
- [ ] Confirm delivery channel decision (self-hosted vs managed push) with leadership before Architecture begins — flag subscription cost if managed service is selected
- [ ] Identify whether Taskwave has existing job/queue infrastructure before scoping the scheduler workstream
- [ ] Agree v1 scope boundary (mute/snooze, notification grouping/threading, email/push channels, digest mode — in or out?) at the PRD gate

---

The full document is saved at `initiative-decomposition-notification-centre.md`. The key flags to act on before Phase 1 starts: confirm the delivery channel cost implications with leadership, and check whether a job queue already exists in Taskwave — both decisions will materially shape Architecture effort.

### Artifacts written

#### `work/initiative-decomposition-notification-centre.md`

```
# Initiative Decomposition: Notification Centre

## Context

### Initiative context

| Question | Answer |
|---|---|
| **User problem** | Taskwave users miss important events — task assignments, looming deadlines, and @mentions — because there is no in-app notification layer. Users must actively poll the app or rely on external email/Slack noise. |
| **Target user** | All Taskwave workspace members; particularly contributors who are assigned work and collaborators who are mentioned in comments. Power users (project leads, managers) who receive high notification volumes are the secondary concern (preferences, mute). |
| **Success criteria** | ≥80% of assigned-task and @mention notifications opened within 24 hours; notification open rate tracked via analytics; zero missed deadline reminders in QA acceptance testing; user-reported "I missed something important" complaints drop measurably post-launch. |
| **Appetite** | 6 weeks (medium scope). This is a time box, not a commitment to full scope — if trade-offs are needed, scope is cut before the deadline slips. |
| **Constraints** | "Real-time" delivery + persistence + preferences + @mention parsing within 6 weeks is aggressive. A scheduler/cron system is required for deadline reminders (not a simple event trigger). @mentions require permission checks (can the mentioner see the mentioned user in this context?). Any real-time delivery infrastructure choice (WebSockets, SSE, third-party push) must be made in Phase 1 — it affects every other workstream. |

---

## Workstreams

### CPO team workstreams

| Workstream | Owner role | Key deliverables | Relevant? |
|---|---|---|---|
| Product | `product-owner` | PRD covering notification taxonomy (assignments, deadline reminders, @mentions), notification preferences spec, mark-as-read / mark-all-read behaviour, deep-link routing to source object, mute/snooze rules, notification bell UI spec, inbox view requirements, success metrics | **Yes** — this is the definition layer for everything downstream |
| Design | `ui-designer` | Notification bell component + badge count spec, notification inbox panel (grouped/ungrouped, read/unread states), notification preference settings page, empty states and error states, mobile/responsive behaviour, accessibility (WCAG AA — keyboard navigation, screen reader labels) | **Yes** — UX complexity is high; mark-as-read, grouping, and preference flows all need explicit specs |
| Content | `user-docs-writer` | In-app onboarding tooltip copy, help article ("Managing your notifications"), notification preference descriptions, email/push opt-out guidance | **Yes** — preference settings need clear copy; help content is needed for launch |
| GTM | `gtm` | In-app announcement (what's new modal or banner), internal comms to support/success, changelog entry | **Yes** — in-app feature still needs a launch moment; no external marketing required but an in-app announcement and internal readiness note are needed |
| Support | `support` | FAQ entries ("Why am I not receiving notifications?", "How do I turn off deadline reminders?"), known-issue list from QA, support runbook for common escalations | **Yes** — notification preferences and delivery failures will generate support tickets |
| Research | `ux-researcher` | Notification fatigue risk assessment, review of existing user feedback on missed-event complaints, usability review of preference settings flows | **Yes (lightweight)** — no new primary research needed within appetite, but a targeted review of existing feedback and a single usability pass on the preference UI is worth the 1–2 day investment |

### CTO team workstreams

| Workstream | Owner role | Key deliverables | Relevant? |
|---|---|---|---|
| Architecture | `architect` | System design document: real-time delivery channel decision (WebSocket vs SSE vs managed push — **note:** managed services like Pusher/Ably/Firebase carry ongoing subscription costs and must be flagged to leadership before selection), notification persistence model (event-sourced append-only log vs relational store), scheduler design for deadline reminders (cron job, queue-based delayed delivery), @mention parser interface and permission check contract, API contracts (REST + WebSocket/SSE endpoints), notification preference data model, ADR for delivery channel choice | **Yes** — foundational; every other CTO workstream is blocked on architecture decisions |
| Development | `fullstack-developer` | Notification service (event ingestion, fan-out, persistence), real-time delivery layer, @mention extraction and permission-guarded fan-out, deadline reminder scheduler, notification preference CRUD API, read/unread state management, deep-link resolver, notification bell + inbox UI components, preference settings UI, integration with existing task/comment/assignment event sources | **Yes** — the core build |
| QA Planning | `qa-lead` | Test strategy: real-time delivery latency acceptance criteria, deadline reminder accuracy window (± tolerance), @mention permission edge cases, notification preference persistence and override behaviour, cross-browser notification rendering, performance under fan-out at expected user scale | **Yes** |
| QA Execution | `qa-engineer` | Automated tests: notification delivery (unit + integration), scheduler accuracy tests, @mention parser tests, preference API contract tests; manual exploratory: inbox UX, read/unread state, deep-link routing, mobile responsiveness | **Yes** |
| DevOps | `devops` | Infrastructure for real-time channel (if self-hosted: WebSocket server scaling, sticky sessions or pub/sub broker); scheduler job hosting; monitoring and alerting (notification delivery failure rate, scheduler missed-fire alerts, queue depth); deployment plan for phased rollout | **Yes** — real-time infrastructure is not trivial to operate |
| Security | `security-engineer` | Threat model: @mention permission enforcement (user A cannot mention user B in a context where B is not a member), notification content exposure (does the notification payload leak data the recipient shouldn't see?), preference manipulation (can a user suppress notifications for another user?), rate limiting fan-out to prevent abuse | **Yes — not optional.** @mentions with permission implications and notification content exposure make this mandatory |
| Data | `data-engineer` | Event tracking plan: notification delivered, notification opened, notification dismissed, preference changed; analytics dashboard: open rate by notification type, time-to-open distribution, opt-out rate by type; baseline measurement pre-launch | **Yes** — open/click rate is the primary success metric; without instrumentation the initiative cannot be declared successful |

---

## Dependencies

### Dependency map

| Workstream | Depends on | What it needs before starting | Blocks |
|---|---|---|---|
| Architecture | Product | PRD with notification taxonomy, NFRs (latency targets, scale estimates, retention policy), and preference model requirements | Development, DevOps, Security, Data |
| Design | Product | PRD with full user flows: bell, inbox, preferences, mute/snooze, deep-link behaviour, empty/error states | Development (UI layer), Content, GTM |
| Security | Architecture | Threat surface definition: data model, API contracts, @mention permission contract, fan-out design | Development (cannot ship without sign-off) |
| Development | Design, Architecture, Security | Finalised UI specs, API contracts, permission contract, delivery channel decision | QA Execution, Content (needs working feature for screenshots), GTM |
| QA Planning | Architecture | System design and API contracts to derive test cases and latency acceptance criteria | QA Execution |
| QA Execution | Development | Working implementation in staging | Launch gate |
| DevOps | Architecture | Infrastructure decisions (delivery channel, scheduler hosting) | Development (environment needed for integration testing), Launch |
| Data | Architecture | Event taxonomy agreed; Development | Dashboard and launch analytics |
| Content | Development | Working feature in staging (screenshots, actual preference labels) | GTM, Support, Launch |
| GTM | Product, Design, Content | Final UX, changelog copy, in-app announcement copy | Launch |
| Support | Content, QA Execution | Help articles finalised, known-issues list from QA | Launch |
| Research | Product | Draft PRD available for review; Design | Preference UI usability input feeds back into Design before final spec |

---

## Execution Sequence

### Phased plan

| Phase | Workstreams (parallel) | Duration | Gate to next phase |
|---|---|---|---|
| 1 — Define | Product + Architecture (+ Research lightweight review) | 1–1.5 weeks | PRD approved by stakeholders; system design reviewed and ADR for delivery channel accepted; any paid-service decisions confirmed with leadership |
| 2 — Design & Secure | Design + Security threat model + QA Planning + DevOps infrastructure provisioning | 1–1.5 weeks | UI specs signed off (bell, inbox, preferences, all states); threat model reviewed and accepted; test plan drafted; staging environment with real-time infrastructure live |
| 3 — Build | Development (all layers: service + API + UI) + Data instrumentation implementation | 2–2.5 weeks | Feature complete in staging: all notification types delivered, preferences persist, deep-links route correctly, scheduler fires in test environment |
| 4 — Validate | QA Execution + DevOps monitoring verification + Security sign-off | 0.5–1 week | All acceptance criteria passing; no open P0/P1 bugs; delivery failure monitoring and scheduler miss-fire alerting live; security sign-off obtained |
| 5 — Prepare & Launch | Content + GTM + Support prep → coordinated release | 0.5 week | Help article published; in-app announcement ready; support FAQ merged; changelog live; data dashboard baseline captured; rollout confirmed |

**Total: 5–7 weeks**

### Critical path

Product → Architecture → Development → QA Execution → Launch.

The delivery channel decision inside Architecture is the single highest-leverage decision: it determines DevOps infrastructure, Development implementation approach, and QA latency acceptance criteria simultaneously. A delayed or reversed architecture decision compresses every downstream phase.

### Parallel opportunities

- Design and Security threat model run in parallel during Phase 2 — neither blocks the other.
- QA Planning starts as soon as Architecture is complete (Phase 2), well before Development finishes (Phase 3).
- Data instrumentation can be built as a parallel track within Phase 3 alongside feature development — it shares the same codebase touchpoints but has independent deliverables.
- Content, GTM, and Support preparation all run in parallel during Phase 5.

### Timeline tension

**The 6-week appetite is tight for this scope.** Real-time delivery infrastructure, a deadline reminder scheduler, @mention permission enforcement, notification preferences, and a full inbox UI collectively represent 4–5 distinct technical surfaces. The most likely compression strategy: defer mute/snooze to a fast-follow, ship with basic notification types (assignment + @mention) first and add deadline reminders in week 5–6, or time-box the preference UI to a simple on/off toggle initially.

---

## Summary

### Workstream summary

| Workstream | Owner | Depends on | Key deliverables | Phase | Estimated effort |
|---|---|---|---|---|---|
| Product | `product-owner` | — | PRD, notification taxonomy, preference spec, success metrics | 1 | 3–5 days |
| Research (lightweight) | `ux-researcher` | Product (draft PRD) | Existing-feedback review, preference UX usability input | 1–2 | 1–2 days |
| Architecture | `architect` | Product | System design, delivery channel ADR, scheduler design, API contracts, permission contract | 1 | 4–6 days |
| Design | `ui-designer` | Product | Bell + inbox specs, preference settings, all states, accessibility requirements | 2 | 5–8 days |
| Security | `security-engineer` | Architecture | Threat model: @mention permissions, content exposure, rate limiting | 2 | 2–3 days |
| QA Planning | `qa-lead` | Architecture | Test strategy, latency criteria, permission edge-case test cases, fan-out scale test plan | 2 | 2–3 days |
| DevOps | `devops` | Architecture | Staging environment, real-time infra provisioning, monitoring and alerting setup | 2–3 | 3–5 days |
| Development | `fullstack-developer` | Design, Architecture, Security | Notification service, scheduler, @mention parser, delivery layer, bell + inbox + preference UI | 3 | 10–15 days |
| Data | `data-engineer` | Architecture, Development | Event tracking plan, instrumentation, analytics dashboard | 3–4 | 2–4 days |
| QA Execution | `qa-engineer` | Development | Automated tests, exploratory testing, bug reports | 4 | 3–5 days |
| Content | `user-docs-writer` | Development | Help article, preference copy, onboarding tooltips | 5 | 2–3 days |
| GTM | `gtm` | Product, Design, Content | In-app announcement, changelog entry, internal comms | 5 | 1–2 days |
| Support | `support` | Content, QA Execution | FAQ, known-issues list, support runbook | 5 | 1–2 days |

### Timeline estimate

- **Best case:** 5 weeks — no major architecture reversals, no security findings requiring redesign, QA finds no P0 bugs in the first pass.
- **Likely case:** 7 weeks — one architecture trade-off debate (self-hosted vs managed push), at least one design revision after usability review, QA finds 2–3 issues requiring a fix cycle.
- **Latency target (NFR placeholder):** real-time delivery target <5s P95 from event to notification visible in UI — to be confirmed as a hard acceptance criterion in Phase 1 during Architecture.
- **Risk factors:**
  - **Delivery channel selection** — choosing a managed push service (Pusher, Ably, Firebase Cloud Messaging) resolves infrastructure complexity quickly but introduces ongoing subscription cost; choosing self-hosted WebSocket/SSE is cheaper but adds DevOps complexity and may hit sticky-session scaling issues.
  - **@mention permission scope** — if the permission model is complex (cross-workspace, guest users, private channels), the security review and development effort can expand significantly.
  - **Deadline reminder scheduler** — if no existing job/queue infrastructure exists in Taskwave, building it from scratch adds 3–5 days to Architecture and Development.
  - **Scope creep** — "manage and act on" can expand to include email/push notification channels, snooze, notification grouping/threading, and digest mode. Each is a separate surface. The PRD gate must explicitly mark what is in/out for v1.

---

## Follow-ups

- [ ] Define OKRs for this initiative — use `/coordinator:define-okrs`
- [ ] Create detailed spec for the Product workstream — use `/coordinator:write-spec`
- [ ] Confirm delivery channel decision (self-hosted vs managed) with leadership before Architecture begins — flag subscription cost implications if managed service is selected
- [ ] Identify whether Taskwave has existing job/queue infrastructure before scoping the scheduler workstream
- [ ] Agree v1 scope boundary (mute/snooze, notification grouping/threading, email/push channels, digest mode — in or out?) at PRD gate

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.0/17.0 (88%) |
| Evaluated | 2026-05-01 |
| Target duration | 252020 ms |
| Target cost | $0.7620 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Completes Step 1 (initiative context table) — including user problem, target user, success criteria, appetite, and constraints | PASS | Context table in artifact has all five rows: User problem ('Taskwave users miss important events'), Target user ('All Taskwave workspace members; particularly contributors...'), Success criteria ('≥80% of assigned-task and @mention notifications opened within 24 hours...'), Appetite ('6 weeks (medium scope)'), and Constraints (real-time delivery, scheduler requirement, @mention permission checks, delivery channel decision). |
| c2 | Assesses workstream relevance for both CPO and CTO teams — does not include all workstreams blindly, excludes irrelevant ones with reasoning | PARTIAL | Both CPO and CTO workstream tables include a 'Relevant?' column with explicit reasoning for each workstream (e.g., Research: 'Yes (lightweight, 1–2 days)'; GTM: 'Yes — in-app feature still needs a launch moment'). However, no workstream is marked as irrelevant or excluded — every workstream is included with justification, which does not satisfy 'excludes irrelevant ones.' |
| c3 | Includes a dependency map showing what blocks what — specifically that design and architecture depend on product requirements | PASS | Dependency map table explicitly shows: Architecture 'Depends on: Product' and Design 'Depends on: Product'. Architecture blocks Development, DevOps, Security, Data. Design blocks Development (UI layer), Content, GTM. |
| c4 | Produces a phased execution sequence with named gates between phases (not just 'move on when ready') | PASS | Phased plan table has a 'Gate to next phase' column with specific named criteria: Phase 1 gate is 'PRD approved by stakeholders; system design reviewed and ADR for delivery channel accepted'; Phase 2 gate is 'UI specs signed off (bell, inbox, preferences, all states); threat model reviewed and accepted; test plan drafted; staging environment with real-time infrastructure live'; and so on through Phase 5. |
| c5 | Identifies the critical path and parallel opportunities explicitly | PASS | A 'Critical path' subsection states 'Product → Architecture → Development → QA Execution → Launch' and singles out 'The delivery channel decision inside Architecture is the single highest-leverage decision.' A 'Parallel opportunities' subsection explicitly lists four parallel tracks: Design + Security in Phase 2, QA Planning starting in Phase 2 parallel to Phase 3 development, Data instrumentation as a parallel Phase 3 track, and Content + GTM + Support in parallel in Phase 5. |
| c6 | Produces a summary table with owner roles, dependencies, key deliverables, phase, and effort estimates as ranges | PASS | Workstream summary table has all required columns: Workstream, Owner (role tags like `product-owner`, `architect`), Depends on, Key deliverables, Phase, and Estimated effort — with all effort values as ranges (e.g., '3–5 days', '10–15 days'). |
| c7 | Effort estimates are ranges, not point estimates (e.g. '1–2 weeks' not '1 week') | PASS | Every effort estimate in the summary table is a range: Product '3–5 days', Architecture '4–6 days', Design '5–8 days', Development '10–15 days', QA Execution '3–5 days', etc. No single-point estimates appear. |
| c8 | Includes follow-up actions pointing to related skills (define-okrs, write-spec) | PARTIAL | Follow-ups section contains: '[ ] Define OKRs for this initiative — use `/coordinator:define-okrs`' and '[ ] Create detailed spec for the Product workstream — use `/coordinator:write-spec`', along with three other actionable follow-ups. |
| c9 | Does not include GTM, support prep, or formal UX research if the scenario doesn't warrant it — avoids padding the decomposition | FAIL | The output includes GTM ('in-app announcement, changelog entry, internal comms'), Support ('FAQ entries, known-issue list, support runbook'), and Research ('ux-researcher: Existing-feedback review, preference UX usability input') as full workstreams. All three are present in the CPO workstream table and in the summary table with effort estimates. |
| c10 | Output's initiative context table reproduces the prompt facts — Notification Centre, Taskwave, in-app notifications for task assignments / deadlines / @mentions, medium scope, 6-week appetite — not abstracted into generic placeholders | PASS | Context table names 'Taskwave' explicitly, specifies 'task assignments, looming deadlines, and @mentions' as the exact event types from the prompt, states '6 weeks (medium scope)' matching the appetite, and the document title is 'Initiative Decomposition: Notification Centre'. No generic placeholders used. |
| c11 | Output's workstreams include the relevant ones — UX (notification surface design), architect (real-time delivery mechanism), backend developer (event sources for assignments, deadlines, mentions), frontend developer (notification centre UI), QA — and EXCLUDE GTM, support training, formal UX research as out-of-scope for an internal feature this size | PARTIAL | All relevant workstreams are present: `ui-designer` (notification surface design), `architect` (real-time delivery channel ADR), `fullstack-developer` (notification service + UI), `qa-lead` and `qa-engineer` (QA). However, the criterion explicitly requires EXCLUDING GTM (`gtm`), support training (`support`), and formal UX research (`ux-researcher`) — all three are included in the output's workstream tables and summary. |
| c12 | Output's dependency map shows architect and UX work feeds developer implementation, and that backend event-source work for each notification type must be in place before the frontend can subscribe to them | PARTIAL | Dependency map clearly shows Development depends on 'Design, Architecture, Security' — confirming architect and UX (Design) feed developer implementation. However, the output uses a single `fullstack-developer` role covering both backend and frontend; there is no explicit statement that backend event-source work per notification type must precede frontend subscription — this backend→frontend sequencing is not surfaced. |
| c13 | Output's phased execution sequence has named gates between phases — e.g. 'Discovery complete → Design gate', 'Design complete → Implementation gate', 'Implementation complete → QA gate' — not just sequential phases without checkpoints | PASS | Each phase row in the phased plan table has a 'Gate to next phase' column with specific named conditions (e.g., Phase 1: 'PRD approved by stakeholders; system design reviewed and ADR for delivery channel accepted'; Phase 3: 'Feature complete in staging: all notification types delivered, preferences persist, deep-links route correctly, scheduler fires in test environment'). These are concrete checkpoints, not generic transitions. |
| c14 | Output identifies the critical path explicitly — likely real-time delivery mechanism design (e.g. WebSockets vs polling) blocking everything that depends on it — and names parallel opportunities (e.g. UI mockups can proceed while delivery mechanism is being chosen) | PASS | Critical path section identifies 'The delivery channel decision inside Architecture is the single highest-leverage decision: it determines DevOps infrastructure, Development implementation approach, and QA latency acceptance criteria simultaneously.' Parallel opportunities section explicitly names: 'Design and Security threat model run in parallel during Phase 2 — neither blocks the other' and 'Data instrumentation can be built as a parallel track within Phase 3.' |
| c15 | Output's summary table has columns for owner role, dependencies, key deliverables, phase, AND effort estimate — and the effort estimates are ranges (e.g. '1-2 weeks') not single points | PASS | Workstream summary table contains all five required columns (Owner, Depends on, Key deliverables, Phase, Estimated effort). Effort estimates are all ranges: '3–5 days', '1–2 days', '4–6 days', '5–8 days', '10–15 days', etc. |
| c16 | Output's effort estimates fit within the 6-week appetite — total time on the critical path should be ≤6 weeks, with the timeline reasoning shown | PASS | Critical path sum: Phase 1 (1–1.5 wks) + Phase 2 (1–1.5 wks) + Phase 3 (2–2.5 wks) + Phase 4 (0.5–1 wk) + Phase 5 (0.5 wk) = 5–7 weeks. Timeline reasoning is explicit: 'Best case: 5 weeks', 'Likely case: 7 weeks', with a 'Timeline tension' paragraph explaining the 6-week appetite is tight and proposing compression strategies (defer mute/snooze, simplify preferences to on/off toggle for v1). |
| c17 | Output includes follow-up actions pointing to related skills — at minimum `/coordinator:write-spec` to spec the work and `/coordinator:define-okrs` if there's an outcome metric to track (e.g. notification engagement rate) | PASS | Follow-ups section contains '[ ] Define OKRs for this initiative — use `/coordinator:define-okrs`' and '[ ] Create detailed spec for the Product workstream — use `/coordinator:write-spec`' as the first two items. |
| c18 | Output addresses the user-actionable nature of the notifications — task assignments and deadline reminders can drive workflow actions, so the design must cover both passive (read) and active (act) interactions | PARTIAL | The output references 'mark-as-read / mark-all-read behaviour, deep-link routing to source object, mute/snooze rules' in the Product workstream and 'deep-link resolver' as a Development deliverable. The prompt's phrase 'receive, manage, and act on real-time alerts' is echoed in context. However, the output does not explicitly frame the design requirement as covering both passive (read) and active (act) interaction modes as a distinct design consideration. |

### Notes

The decomposition is comprehensive and well-structured, earning PASS on the majority of criteria. The initiative context table is thorough, the dependency map is explicit, named gates are present at every phase transition, the critical path (delivery channel decision) is correctly identified, and the summary table has all required columns with range estimates. The main deductions come from: (1) including GTM, Support, and UX Research workstreams that criteria c9 and c11 expected to be excluded for a feature of this scope and size — the output justifies their inclusion but the test rubric treats them as padding; (2) no explicit separation of backend event-source dependencies from frontend subscription in the dependency map, since a single fullstack-developer role was used; and (3) partial credit on c2 for assessing relevance with reasoning but not actually excluding any workstream. The timeline reasoning and risk analysis are notably strong, particularly the delivery channel cost flag and scope-creep risk enumeration.
