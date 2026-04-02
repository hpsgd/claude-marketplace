# CQRS Model — {Bounded Context Name}

> Version {0.1} | {Date} | Status: {Draft/Review/Approved}

## 1. Bounded Context

| Field | Value |
|-------|-------|
| Domain | {e.g. Order Management} |
| Owning team | {Team name} |
| Upstream contexts | {Contexts this depends on} |
| Downstream contexts | {Contexts that depend on this} |

{Brief description of responsibilities and invariants.}

## 2. Commands

| Command | Payload Fields | Validation Rules | Side Effects |
|---------|---------------|-----------------|-------------|
| `Create{Aggregate}` | `name: string`, `ownerId: UUID` | Name must be unique within scope | Emits `{Aggregate}Created` |
| `Update{Aggregate}` | `id: UUID`, `name?: string` | Aggregate must exist, caller must be owner | Emits `{Aggregate}Updated` |
| `Delete{Aggregate}` | `id: UUID` | Aggregate must exist, no active children | Emits `{Aggregate}Deleted` |

{Add rows for each command in this context.}

## 3. Command Handlers

| Handler | Command | Aggregate Root | Logic |
|---------|---------|---------------|-------|
| `Create{Aggregate}Handler` | `Create{Aggregate}` | `{Aggregate}` | Validates uniqueness, creates aggregate, appends event |
| `Update{Aggregate}Handler` | `Update{Aggregate}` | `{Aggregate}` | Loads aggregate from event stream, applies changes, appends event |
| `Delete{Aggregate}Handler` | `Delete{Aggregate}` | `{Aggregate}` | Loads aggregate, validates no children, soft-deletes, appends event |

{Each handler loads the aggregate, enforces invariants, and persists new events.}

## 4. Events

| Event | Payload Fields | Schema Version | Notes |
|-------|---------------|----------------|-------|
| `{Aggregate}Created` | `id: UUID`, `name: string`, `ownerId: UUID`, `createdAt: datetime` | 1 | Initial creation event |
| `{Aggregate}Updated` | `id: UUID`, `changes: object`, `updatedAt: datetime` | 1 | Contains only changed fields |
| `{Aggregate}Deleted` | `id: UUID`, `deletedAt: datetime` | 1 | Soft delete marker |

{All events are immutable. Schema changes require a new version with an upcaster.}

## 5. Read Models / Projections

| Projection | Source Events | Query Patterns | Staleness Tolerance |
|-----------|--------------|----------------|-------------------|
| `{Aggregate}ListProjection` | `Created`, `Updated`, `Deleted` | List with filters, search | Eventual (< 2s) |
| `{Aggregate}DetailProjection` | `Created`, `Updated` | Single item by ID | Eventual (< 2s) |
| `{Aggregate}CountProjection` | `Created`, `Deleted` | Dashboard totals | Eventual (< 30s) |

{Each projection subscribes to relevant events and maintains a denormalised read store.}

## 6. Consistency Boundaries

| Aggregate Root | Invariants | Transaction Scope |
|---------------|-----------|------------------|
| `{Aggregate}` | {e.g. Name unique per owner, status transitions follow FSM} | Single aggregate — one stream per instance |

- **Within aggregate:** Strong consistency (events applied in order).
- **Across aggregates:** Eventual consistency via sagas/process managers.
- **Saga:** {Describe multi-aggregate workflows if applicable.}

## 7. Event Store Schema

| Field | Description |
|-------|------------|
| Stream naming | `{aggregate_type}-{aggregate_id}` (e.g. `order-abc123`) |
| Event envelope | `{ streamId, eventType, data, metadata, version, timestamp }` |
| Metadata | `{ correlationId, causationId, userId, schemaVersion }` |
| Snapshots | Every {100} events; snapshot contains full aggregate state |
| Retention | Events retained indefinitely; snapshots pruned after {N+1} |

## 8. Idempotency

| Concern | Strategy |
|---------|----------|
| Duplicate commands | Commands carry a client-generated `commandId`; handler checks for existing event with same `causationId` before processing |
| Duplicate events | Projections track `lastProcessedPosition`; skip events at or below that position |
| At-least-once delivery | All consumers are idempotent; replaying events produces the same read model state |
| Ordering | Events within a stream are ordered by version; cross-stream ordering is not guaranteed |
