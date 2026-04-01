---
name: decompose-initiative
description: Break a product initiative into workstreams across CPO and CTO teams. Use at the start of any significant product effort to plan who does what.
argument-hint: "[initiative or feature to decompose]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Decompose $ARGUMENTS into workstreams across the CPO and CTO teams.

## Process

### 1. Understand the initiative
- What's the user problem being solved?
- Who's the target user?
- What does success look like?
- What's the appetite (time/effort budget)?

### 2. Identify workstreams

Map the initiative across both teams:

**CPO team:**
- Product: Requirements, acceptance criteria, success metrics
- Design: UX flows, component specs, accessibility requirements
- Content: Documentation, help content, knowledge base updates
- GTM: Positioning, launch plan, marketing content
- Support: FAQ preparation, known issues, support training

**CTO team:**
- Architecture: System design, API contracts, data model, ADRs
- Development: Implementation plan, technical spikes needed
- QA: Test strategy, test plan, quality gates
- DevOps: Infrastructure changes, deployment plan, monitoring
- Security: Threat model, security review checkpoints
- Data: Event tracking plan, analytics requirements, dashboard updates

### 3. Identify dependencies

Map which workstreams depend on others:
- Design needs requirements from Product before starting
- Development needs API contracts from Architecture and specs from Design
- QA needs implementation from Development before test execution
- DevOps needs architecture decisions before infrastructure work
- GTM needs the feature working before launch content

### 4. Sequence the work

Propose an order that minimises blocking:
1. Product + Architecture (parallel — define what and how)
2. Design + Security threat model (parallel — needs requirements)
3. Development + QA test planning (parallel — QA plans while dev builds)
4. QA execution + DevOps deployment prep
5. Content + GTM + Support preparation
6. Launch

### Output

Present as a table:

| Workstream | Owner | Depends on | Key deliverables | Estimated effort |
|---|---|---|---|---|
| Requirements | product-owner | — | PRD, user stories | ... |
| Architecture | architect | Requirements | ADR, API contracts | ... |
| ... | ... | ... | ... | ... |
