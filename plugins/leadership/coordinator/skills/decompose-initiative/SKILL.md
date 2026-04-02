---
name: decompose-initiative
description: "Break a product initiative into workstreams across CPO and CTO teams. Produces a dependency-sequenced workstream table with owners, deliverables, and effort estimates. Use at the start of any significant product effort to plan who does what."
argument-hint: "[initiative or feature to decompose]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Decompose $ARGUMENTS into workstreams across the CPO and CTO teams using the mandatory process below.

## Step 1: Understand the initiative (mandatory)

Before decomposing, establish the context:

```markdown
### Initiative context

| Question | Answer |
|---|---|
| **User problem** | [What problem is being solved, for whom?] |
| **Target user** | [Specific user type — not "everyone"] |
| **Success criteria** | [How will we know this initiative succeeded? Include metrics] |
| **Appetite** | [Time/effort budget — 2 weeks? 6 weeks? Quarter?] |
| **Constraints** | [Fixed deadlines, dependencies on other teams, technical limitations] |
```

**Output:** Completed initiative context table.

## Step 2: Identify workstreams (mandatory)

Map the initiative across both teams. Not every workstream applies to every initiative — include only what's relevant.

```markdown
### CPO team workstreams

| Workstream | Owner role | Key deliverables | Relevant? |
|---|---|---|---|
| Product | product-owner | PRD, user stories, acceptance criteria, success metrics | [Yes/No — why] |
| Design | ui-designer | UX flows, component specs, accessibility requirements | [Yes/No] |
| Content | user-docs-writer | Documentation, help content, knowledge base updates | [Yes/No] |
| GTM | gtm | Positioning, launch plan, marketing content | [Yes/No] |
| Support | support | FAQ preparation, known issues, support training | [Yes/No] |
| Research | ux-researcher | Persona validation, usability testing, journey mapping | [Yes/No] |

### CTO team workstreams

| Workstream | Owner role | Key deliverables | Relevant? |
|---|---|---|---|
| Architecture | architect | System design, API contracts, data model, ADRs | [Yes/No] |
| Development | [developer role] | Implementation, code review, technical spikes | [Yes/No] |
| QA | qa-engineer | Test strategy, test plan, quality gates | [Yes/No] |
| DevOps | devops | Infrastructure changes, deployment plan, monitoring | [Yes/No] |
| Security | security-engineer | Threat model, security review checkpoints | [Yes/No] |
| Data | data-engineer | Event tracking plan, analytics, dashboard updates | [Yes/No] |
```

For each relevant workstream, expand the deliverables to be specific to this initiative — not generic lists.

**Output:** Workstream tables with relevance assessment and initiative-specific deliverables.

## Step 3: Map dependencies (mandatory)

Identify which workstreams block others:

```markdown
### Dependency map

| Workstream | Depends on | What it needs before starting | Blocks |
|---|---|---|---|
| Design | Product | Requirements and acceptance criteria | Development |
| Architecture | Product | Requirements and NFRs | Development, DevOps |
| Development | Design, Architecture | Specs and API contracts | QA |
| QA | Development | Working implementation | Launch |
| DevOps | Architecture | Infrastructure decisions | Launch |
| Content | Development | Working feature for screenshots/docs | Launch |
| GTM | Product, Design | Positioning inputs, final UX | Launch |
| Support | Content, QA | Docs and known issues list | Launch |
```

Adapt this map to the specific initiative — remove irrelevant rows, add dependencies specific to this effort.

**Output:** Dependency table showing what blocks what.

## Step 4: Sequence the work (mandatory)

Propose a phased order that minimises blocking:

```markdown
### Execution sequence

| Phase | Workstreams (parallel) | Duration | Gate to next phase |
|---|---|---|---|
| 1 — Define | Product + Architecture | [estimate] | PRD approved, system design reviewed |
| 2 — Design | Design + Security threat model | [estimate] | Specs complete, threat model reviewed |
| 3 — Build | Development + QA test planning | [estimate] | Feature complete, test plan ready |
| 4 — Validate | QA execution + DevOps deployment prep | [estimate] | Tests passing, deployment verified in staging |
| 5 — Prepare | Content + GTM + Support prep | [estimate] | Docs written, launch plan approved |
| 6 — Launch | Coordinated release | [estimate] | All gates passed |

### Critical path
[Which workstream sequence determines the minimum total duration?]

### Parallel opportunities
[Which workstreams can run simultaneously to compress the timeline?]
```

**Output:** Phased execution sequence with gates and critical path.

## Step 5: Produce the summary table (mandatory)

```markdown
### Workstream summary

| Workstream | Owner | Depends on | Key deliverables | Phase | Estimated effort |
|---|---|---|---|---|---|
| Product | product-owner | — | PRD, user stories | 1 | [estimate] |
| Architecture | architect | Product | System design, API contracts | 1 | [estimate] |
| Design | ui-designer | Product | UX flows, component specs | 2 | [estimate] |
| ... | ... | ... | ... | ... | ... |

### Timeline estimate
- **Best case:** [duration assuming no blockers]
- **Likely case:** [duration with typical friction]
- **Risk factors:** [what could extend the timeline]
```

**Output:** Complete summary table with estimates and timeline.

## Rules

- **Every workstream needs an owner role.** "Someone should handle security" is not a plan. "security-engineer owns the threat model, due in Phase 2" is a plan.
- **Dependencies must be specific.** "Design depends on Product" is vague. "Design needs the PRD with user flows and acceptance criteria before starting wireframes" is specific.
- **Not every workstream is relevant.** A small bug fix doesn't need GTM, support preparation, or a formal QA strategy. Include only what the initiative actually requires — and state WHY you excluded the rest.
- **Parallel work is the default.** If two workstreams don't depend on each other, they run in parallel. Sequential work by default wastes time.
- **Gates prevent cascading rework.** Each phase ends with a gate — a specific artifact that must be reviewed before the next phase starts. "Move on when ready" is not a gate.
- **Estimates are ranges, not points.** "2 weeks" is a guess. "1–3 weeks, depending on API complexity" is an estimate.

## Output Format

```markdown
# Initiative Decomposition: [name]

## Context
[From Step 1]

## Workstreams
[From Step 2 — relevant workstreams only]

## Dependencies
[From Step 3]

## Execution Sequence
[From Step 4 — phased plan with gates]

## Summary
[From Step 5 — table with estimates]

## Follow-ups
- [ ] Define OKRs for this initiative — use `/coordinator:define-okrs`
- [ ] Create detailed specs for each workstream
```

## Related Skills

- `/coordinator:define-okrs` — define success metrics and OKRs after decomposition. Decompose first (what), then define OKRs (how we'll measure success).
