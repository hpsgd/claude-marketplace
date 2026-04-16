---
description: Event Sourcing, CQRS, and DDD patterns — cross-language architectural conventions
---

# Event Sourcing & CQRS Patterns

These patterns apply across language boundaries (.NET with Marten, Python with pyeventsourcing, etc.).

## Domain-sliced architecture
- Each bounded context is a separate assembly/package/module
- Domain modules don't reference each other — communicate via events
- Only host/composition root projects compose domain modules

## Event-sourced aggregates
- All domain entities modelled as event-sourced aggregates
- State reconstructed from event history, not mutable records
- Use immutable/frozen models for domain state (frozen dataclasses in Python, records in C#)
- Each aggregate has its own event stream

## Lifecycle events
All entities and long-running processes should have lightweight lifecycle events for history/audit:

```
ProcessStarted → Checkpoint, Checkpoint, ... → ProcessCompleted
```

- The outer process emits "started" and "completed" events
- Each meaningful milestone emits its own event in between
- This provides granular visibility into what happened and when
- Event semantics: Invoked = outgoing request (prompt, input); Replied = incoming response (output, tokens, cost)

## One message, one unit of work
Orchestration handlers MUST NOT loop through items doing heavy work inline. Instead, publish one independent message per item and let the message bus handle each in its own transaction. A failure in one item must not affect others.

## Cascading handler chains
Each handler does one thing (one API call, one persistence operation) and returns the next command. This creates event-driven pipelines that are:
- Individually retriable
- Non-blocking (one failure doesn't break the chain)
- Observable (each step emits events)

## Projections / read models
- Inline projections (synchronous, same transaction as event append) for consistency-critical read models
- Async projections for eventually-consistent views
- Read models are disposable — can be rebuilt from events at any time

## Snapshotting
- Inline snapshotting for aggregates with many events
- Snapshot frequency balanced against rebuild cost

## API design for event-sourced systems
- Hierarchical URLs mirroring semantic entity ownership
- No flat top-level listings — every entity accessed through its parent chain
- All list endpoints: pagination + sort + text filter, always in the database
- Optimistic concurrency via `lastUpdatedAt` (409 Conflict on mismatch)
- PATCH updates use RFC 7396 merge patch semantics

## Context flow
- Layered property bags (`ContextLayer`) flow through every invocation
- Each invocation pushes a new layer; reads fall through to parents, writes are local
- Layer discarded when invocation completes (parent can't see child's writes)
- Well-known properties as typed constants: `BUDGET_CENTS`, `ACCUMULATED_COST_CENTS`, `SENSITIVITY`, `TASK_DESCRIPTION`
- Context passed to enforcement checks (immune system, policy containers) as part of the payload
- CLI flags (e.g., `--budget 500`) set initial context properties

## Event semantics
- **Invoked** = outgoing request (prompt, input, parameters)
- **Replied** = incoming response (output, tokens, cost)
- Use consistent naming: `ProcessStarted`, `PageVisited`, `ProcessCompleted`
- Enforcement checks (code-backed containers) emit proper Invoked/Replied events for trace visibility
