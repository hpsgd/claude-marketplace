# Decompose initiative

**Scenario:** A user invokes the skill with a reasonably complex initiative. Does it produce a correctly structured decomposition with initiative context, relevant workstreams (not all of them), a dependency map, a phased execution sequence with gates, and a summary table with estimates?

> /coordinator:decompose-initiative "Notification Centre — a new in-app notification system for Taskwave that lets users receive, manage, and act on real-time alerts for task assignments, deadline reminders, and @mentions. Estimated scope: medium. Timeline appetite: 6 weeks."

Invoked as a skill via `/coordinator:decompose-initiative`, producing a structured multi-section document written to disk.

## Output

#### Initiative context

| Question | Answer |
|---|---|
| **User problem** | Users miss task assignments, deadline reminders, and @mentions because there is no in-app notification system — they rely on email or manual checking |
| **Target user** | Task managers and contributors using Taskwave for collaborative project work |
| **Success criteria** | Notifications delivered within 5s of triggering event; >70% of users open at least one notification in week 1; inbox zero achievable within 3 interactions |
| **Appetite** | 6 weeks |
| **Constraints** | Must not break existing real-time features; notification persistence requires a new data store or extension of existing DB |

#### Workstream relevance assessment

CPO team: Product (Yes — requirements and acceptance criteria for notification types, read/unread state, actions), Design (Yes — inbox UI, notification component, empty state, badge), Content (No — no user-facing docs needed for MVP), GTM (No — internal feature, no external launch), Support (No — FAQ not required for MVP), Research (No — scope is clear, no persona research needed for this initiative).

CTO team: Architecture (Yes — notification delivery pipeline, storage, real-time transport), Development (Yes — react-developer for inbox UI, dotnet-developer for backend), QA Planning (Yes — test strategy for real-time behaviour), QA Execution (Yes — automated tests for delivery and state), DevOps (Yes — infrastructure for notification service), Security (No — no new auth surface), Data (Yes — event tracking for notification engagement metrics).

#### Dependency map

| Workstream | Depends on | What it needs before starting | Blocks |
|---|---|---|---|
| Design | Product | Notification types, read/unread state, action model | Development (frontend) |
| Architecture | Product | NFRs, delivery latency, persistence requirements | Development (backend), DevOps |
| Development (frontend) | Design, Architecture | Component specs, API contracts | QA Execution |
| Development (backend) | Architecture | System design, data model | QA Execution |
| QA Planning | Product, Architecture | Acceptance criteria, system design | Development |
| QA Execution | Development | Working implementation | Launch |
| DevOps | Architecture | Infrastructure decisions | Launch |
| Data | Product | Event tracking plan | Launch |

#### Execution sequence

| Phase | Workstreams (parallel) | Duration | Gate to next phase |
|---|---|---|---|
| 1 — Define | Product + Architecture | 1 week | PRD approved, system design reviewed |
| 2 — Design | Design + QA Planning | 1 week | Specs complete, test strategy reviewed |
| 3 — Build | Development (frontend + backend) | 2–3 weeks | Feature complete per acceptance criteria |
| 4 — Validate | QA Execution + DevOps deployment prep | 1 week | Tests passing, deployed to staging |
| 5 — Launch | Coordinated release + Data tracking live | 1 day | All gates passed |

**Critical path:** Product requirements → Architecture → Development (backend) → QA Execution → Release. Minimum 5–6 weeks.

**Parallel opportunities:** Design runs parallel to Architecture (Phase 2); frontend development runs parallel to backend development (Phase 3).

#### Workstream summary

| Workstream | Owner | Depends on | Key deliverables | Phase | Estimated effort |
|---|---|---|---|---|---|
| Product | product-owner | — | PRD, notification types, acceptance criteria | 1 | 3–5 days |
| Architecture | architect | Product | System design, data model, API contracts, ADR | 1 | 3–5 days |
| Design | ui-designer | Product | Inbox UI, notification component, badge | 2 | 3–4 days |
| QA Planning | qa-lead | Product, Architecture | Test strategy, edge cases | 2 | 2–3 days |
| Development (frontend) | react-developer | Design, Architecture | Notification inbox, real-time updates | 3 | 1–2 weeks |
| Development (backend) | dotnet-developer | Architecture | Notification service, delivery pipeline | 3 | 1–2 weeks |
| QA Execution | qa-engineer | Development | Automated tests, bug reports | 4 | 3–5 days |
| DevOps | devops | Architecture | Deployment pipeline, monitoring | 4 | 2–3 days |
| Data | data-engineer | Product | Event tracking plan, dashboard | 4–5 | 2–3 days |

#### Follow-ups
- [ ] Define OKRs for this initiative — use `/coordinator:define-okrs`
- [ ] Create detailed specs for each workstream

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 8.5/9 (94%) | 2026-04-16 |

- [x] PASS: Completes Step 1 initiative context table — the skill mandates a five-field context table (User problem, Target user, Success criteria, Appetite, Constraints); all five are required outputs; "Output: Completed initiative context table" is explicit
- [x] PASS: Assesses workstream relevance for both CPO and CTO teams — Step 2 requires a Relevant? column (Yes/No — why) for every row in both CPO and CTO tables; the rule states "Not every workstream applies to every initiative — include only what's relevant" and requires reasoning for exclusions
- [x] PASS: Dependency map showing what blocks what — Step 3 mandates a four-column table (Workstream, Depends on, What it needs, Blocks); the template explicitly shows Design and Architecture depending on Product requirements; both must be adapted to the specific initiative
- [x] PASS: Phased execution sequence with named gates — Step 4 requires a phase table with a "Gate to next phase" column; the Rules section states "'Move on when ready' is not a gate"; six phases with example gates are in the template
- [x] PASS: Critical path and parallel opportunities identified explicitly — Step 4's output template includes both "Critical path" and "Parallel opportunities" subsections as required outputs
- [x] PASS: Summary table with owner roles, dependencies, key deliverables, phase, and effort estimates — Step 5 mandates a six-column summary table (Workstream, Owner, Depends on, Key deliverables, Phase, Estimated effort); all six columns are required
- [x] PASS: Effort estimates are ranges not point estimates — the Rules section states "'2 weeks' is a guess. '1–3 weeks, depending on API complexity' is an estimate"; this is a named rule, not just a template convention
- [~] PARTIAL: Follow-up actions pointing to related skills — the Output Format template includes `/coordinator:define-okrs` as an explicit follow-up with a skill reference; "Create detailed specs for each workstream" is present but does not reference `/coordinator:write-spec`. The criterion asks for both skills to be referenced; define-okrs is explicit, write-spec is not. Score: 0.5
- [x] PASS: Does not pad with irrelevant workstreams — the rule "Not every workstream applies to every initiative" combined with the required Yes/No reasoning column enforces selective inclusion; the skill names GTM, Support, and Research as options and requires justification for inclusion or exclusion

## Notes

The skill is tightly structured with every criterion mapped to a mandatory step or named rule. The one genuine gap: the Related Skills section and Output Format template reference `/coordinator:define-okrs` but not `/coordinator:write-spec`. The write-spec follow-up is present as an unrouted action item. Adding `/coordinator:write-spec` to both the Related Skills section and the Output Format template would close this without changing any other behaviour.
