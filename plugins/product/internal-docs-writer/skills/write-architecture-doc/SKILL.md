---
name: write-architecture-doc
description: "Write or update architecture documentation — system overview, component diagrams, data flows, bounded contexts, and key decisions. Produces a living document that explains boundaries and why, not implementation details."
argument-hint: "[system, service, or area to document]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Write architecture documentation for $ARGUMENTS using the mandatory process and structure below.

**Core principle: Architecture docs explain boundaries, relationships, and decisions — not implementation details.** Document WHAT the system is, WHERE data flows, and WHY decisions were made. Leave HOW to the code.

## Step 1 — Research the system

Before writing, build a complete picture:

1. Search the codebase for service definitions, entry points, and deployment configs using `Grep` and `Glob`
2. Identify all components: services, databases, queues, caches, external APIs, CDNs
3. Find infrastructure definitions (Terraform, CloudFormation, Kubernetes manifests, docker-compose)
4. Check for existing ADRs, design docs, or README files
5. Trace the key data flows: what triggers what, what reads from where, what writes to where
6. Identify bounded contexts — which component owns which data?

**Output:** A component inventory with ownership, dependencies, and data stores.

## Step 2 — Write the context section

Every architecture doc starts by answering "what problem does this system solve and for whom?"

```markdown
# Architecture: [System Name]

## Context

### What this system does
[2–3 sentences: the problem it solves and the value it provides. Written for someone who has never seen this system.]

### Who uses it
| Actor | How they interact | What they care about |
|---|---|---|
| [End users] | [Web app, mobile app, API] | [Speed, reliability] |
| [Internal teams] | [Admin dashboard, CLI] | [Observability, control] |
| [External systems] | [Webhooks, API integration] | [Consistency, uptime] |

### System boundary
[One sentence: what is inside this system vs. what is outside (consumed as external dependencies)]
```

**Output:** Context section with actors and system boundary.

## Step 3 — Write the component overview

Document each component with just enough detail to understand its role and boundaries:

```markdown
## Components

### Component diagram

\`\`\`mermaid
graph TD
    Client[Web Client] --> Gateway[API Gateway]
    Gateway --> AuthSvc[Auth Service]
    Gateway --> OrderSvc[Order Service]
    OrderSvc --> OrderDB[(Order DB)]
    OrderSvc --> Queue[Event Queue]
    Queue --> NotifySvc[Notification Service]
    NotifySvc --> Email[Email Provider]
    OrderSvc --> InventorySvc[Inventory Service]
    InventorySvc --> InventoryDB[(Inventory DB)]
\`\`\`

### [Component name]

| Property | Value |
|---|---|
| **Purpose** | [One sentence — if you need two, it's two components] |
| **Owns** | [Data this component is the source of truth for] |
| **Consumes** | [Other components or external services it depends on] |
| **Exposes** | [API, events, or UI it provides to others] |
| **Scales by** | [Horizontal / vertical / managed — and the key metric] |
| **Fails by** | [What happens when this component is down — who is affected?] |
```

**Rules for components:**
- One table per component — no exceptions
- Every component must state what it OWNS (data ownership is singular — two components cannot own the same data)
- Every component must state its failure mode — "the system is resilient" is not a failure mode
- Include external dependencies as components (marked as external) — they fail too

**Output:** Mermaid component diagram and per-component specification tables.

## Step 4 — Write the data flow section

For the 2–3 most critical workflows, trace the full data path:

```markdown
## Data flows

### [Workflow name, e.g., "Place an order"]

\`\`\`mermaid
sequenceDiagram
    participant Client
    participant Gateway as API Gateway
    participant OrderSvc as Order Service
    participant DB as Order DB
    participant Queue as Event Queue
    participant NotifySvc as Notification Service

    Client->>Gateway: POST /orders
    Gateway->>OrderSvc: Create order
    OrderSvc->>DB: Write order (ACID)
    OrderSvc-->>Queue: Publish OrderCreated
    OrderSvc->>Gateway: 201 Created
    Gateway->>Client: Order confirmation
    Queue-->>NotifySvc: Process event
    NotifySvc-->>Client: Email confirmation
\`\`\`

| Step | Consistency | Failure handling | Latency budget |
|---|---|---|---|
| Write order | Strong (ACID) | Reject request, return 500 | 50ms |
| Publish event | At-least-once | Retry with backoff, dead-letter after 5 failures | 10ms |
| Send email | Best-effort | Log failure, retry in 1 hour | N/A (async) |
```

**Rules for data flows:**
- Use Mermaid sequence diagrams — they are versionable and diffable
- Annotate every step with consistency model, failure handling, and latency
- Show both synchronous (solid arrows) and asynchronous (dashed arrows) paths
- Include the unhappy path for critical workflows (what happens when step N fails?)

**Output:** Sequence diagrams with annotated flow tables for key workflows.

## Step 5 — Write bounded contexts and key decisions

```markdown
## Bounded contexts

| Context | Owns | Communicates via | Boundary type |
|---|---|---|---|
| Orders | Order lifecycle, line items | REST API + events | Service boundary |
| Inventory | Stock levels, reservations | Events (async) | Service boundary |
| Identity | Users, roles, sessions | REST API (sync) | Shared library |

## Key decisions

| Decision | Choice | Rationale | ADR |
|---|---|---|---|
| [What was decided] | [What was chosen] | [One sentence: why] | [Link to ADR or "undocumented — write one"] |
| Message broker | Kafka | Ordering guarantees needed for event sourcing | [ADR-007](./adrs/007-kafka.md) |
| Auth approach | OAuth2 + JWKS | Federation with existing IdP, no session state | [ADR-003](./adrs/003-auth.md) |
```

**Rules for decisions:**
- Every significant decision must link to an ADR. If no ADR exists, flag it as "undocumented" and suggest writing one via `/architect:write-adr`.
- Document the rationale, not just the choice. "We chose Kafka" is useless without "because we need ordering guarantees."
- Include decisions that were considered and rejected — these prevent future teams from re-evaluating.

**Output:** Bounded context table and key decisions table with ADR links.

## Step 6 — Write non-functional requirements and known limitations

```markdown
## Non-functional requirements

| Dimension | Target | Current | Measured by |
|---|---|---|---|
| Availability | 99.9% | [current or unknown] | [monitoring tool/dashboard] |
| Latency (p95) | < 200ms reads | [current or unknown] | [APM tool] |
| Throughput | 500 req/s peak | [current or unknown] | [load test results] |
| Recovery | RPO: 1h, RTO: 4h | [current or unknown] | [last DR test date] |

## Known limitations

- [Limitation 1 — what it means for users and what would need to change to fix it]
- [Limitation 2]
```

**Output:** NFR table with targets and measurement methods, plus known limitations.

## Step 7 — Quality checks

| Check | Requirement |
|---|---|
| Diagrams present | At least one component diagram and one sequence diagram |
| Boundaries clear | Can a reader tell what this system owns vs. what it consumes? |
| Decisions linked | Does every key decision reference an ADR? |
| Failure modes stated | Does every component state what happens when it fails? |
| No implementation details | Does the doc describe boundaries and flows, not code structure? |
| Freshness marker | Is the "last updated" date present? |

## Rules

- Document BOUNDARIES, not internals. "The Order Service exposes a REST API and publishes events to Kafka" belongs. "The Order Service uses a repository pattern with dependency injection" does not.
- Diagrams are mandatory. An architecture doc without diagrams is a wall of text. Use Mermaid for all diagrams so they live in version control.
- Link to ADRs for every significant decision. If the ADR doesn't exist, write one. Cross-reference `/architect:write-adr`.
- Every architecture doc has a shelf life. Include a `Last updated: [date]` marker and a `Review trigger: [what change should prompt a rewrite]` note.
- Do not describe aspirational architecture. Document what IS deployed, not what you wish it was. Use a separate "Future state" section if needed, clearly marked.
- Cross-reference `/internal-docs-writer:write-runbook` for operational procedures and `/internal-docs-writer:write-changelog` for change history.

## Output Format

```markdown
# Architecture: [System Name]

**Last updated:** [date]
**Review trigger:** [what change should prompt an update]

## Context
[What, who, boundary]

## Components
[Mermaid diagram + per-component tables]

## Data Flows
[Sequence diagrams + annotated flow tables]

## Bounded Contexts
[Ownership table]

## Key Decisions
[Decision table with ADR links]

## Non-Functional Requirements
[Target vs current table]

## Known Limitations
[Bulleted list with impact]

## Related Documentation
- [Runbooks](./runbooks/)
- [ADRs](./adrs/)
- [Changelog](./CHANGELOG.md)
```
