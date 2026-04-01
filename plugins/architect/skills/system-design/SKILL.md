---
name: system-design
description: Design a system — service boundaries, data flow, API contracts, and non-functional requirements.
argument-hint: "[system or feature to design]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Design a system for $ARGUMENTS.

## Process

1. **Requirements** — functional (what it does) and non-functional (scale, latency, availability, security)
2. **Boundaries** — what's in scope, what's external (existing services, third-party APIs)
3. **Components** — services, databases, queues, caches. Each component has one responsibility
4. **Data flow** — how data moves through the system. Sequence diagram for key flows
5. **API contracts** — interfaces between components. Enough detail to implement against
6. **Storage** — what's stored where, schema design, access patterns
7. **Trade-offs** — what was chosen and what was sacrificed. No design is optimal on all dimensions

## Output

Present as a design document with diagrams (Mermaid) and a trade-off analysis. Suggest an ADR for the key decisions via `/hpsgd:write-adr`.
