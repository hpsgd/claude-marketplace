---
description: JasperFx ecosystem conventions — Wolverine command bus and Marten event store
paths:
  - "**/*.cs"
---

# JasperFx — Wolverine & Marten

## Wolverine Endpoints

Endpoints use Wolverine HTTP conventions:
- Static `LoadAsync` for pre-conditions (returns `ProblemDetails` to short-circuit)
- Instance `Handle` method on the aggregate for decisions
- Return events as cascading messages

## Wolverine Handlers

- `[AggregateHandler]` for automatic aggregate loading from Marten event streams
- Cascading return values publish follow-on commands/events
- Polymorphic cascade: return `object?` to support branching logic (e.g., companions exist → `ExtractCompanionDocuments`, no companions → `CoalesceExtractedEntries`)

## One Message, One Unit of Work

Every Wolverine handler must be a self-contained unit of work with its own transaction. NEVER loop through N items doing heavy work inline — publish N independent messages instead. A single failure must not break the other N-1 items.

Canonical pattern: orchestration handler creates the parent entity, then publishes one independent message per child item.

## Cascading Handler Chains

Handlers form event-driven pipelines where each handler does one thing and returns the next command:

```
Started → Handler1 → Command2
  → Handler2 → Command3
    → Handler3 → FinaliseCommand
      → FinaliseHandler (terminal — cleanup, notify parent)
```

- Non-fatal failures are caught and logged — pipeline continues with whatever completed
- Intermediate state stored as Marten documents, cleaned up by the finalise handler
- Managed sessions only — use Wolverine's `IDocumentSession`, not independent `store.LightweightSession()`

## Marten Event Sourcing

- Event-sourced aggregates for all domain entities
- Inline projections (synchronous, same transaction as event append) for read models
- Inline snapshotting for aggregates with many events
- Database schema: use a dedicated schema (not `public`)
- Weasel `ExtendedSchemaObjects` for custom tables (auto-migrated alongside Marten tables)

## Marten Document Storage

- Use Marten documents for intermediate state between pipeline stages
- Clean up temporary documents in the finalise handler
- Binary content (HTML snapshots, images, PDFs) goes in a dedicated PostgreSQL BYTEA table, not JSONB or Marten documents
- Metadata (fingerprint, content type, timestamps) lives in Marten documents referencing a `ContentBlobId`
- Write via `IContentStore.QueueStore(session, contentType, data)` — enqueued within the Marten session transaction
- Read via `IContentStore.LoadAsync(session, id)` — raw SQL on the session connection
- Schema management via Weasel `ExtendedSchemaObjects` (auto-migrated alongside Marten tables)

## Integration Testing with Alba

- Full HTTP request/response cycle via Alba + Testcontainers PostgreSQL
- Each domain has its own `AppFixture` subclass for domain-specific service replacements
- Base class: `IntegrationContext` provides fixture, `IDocumentSession`, `IMessageBus`
- Register stub external dependencies (e.g., `StubContentFetcher`, stub `IChatClient`) in the fixture
- Remove background services (e.g., `TickService`) in test fixtures for determinism

## Health and Scheduling

- `/health` endpoint with pluggable `IHealthContributor` interface — each domain registers its own contributors
- Generic tick system: `Tick(Type, IssuedAt)` message with type-based routing to domain handlers for scheduled work

## Module Registration

Each domain exposes an `AddXxx(IServiceCollection, IConfiguration)` extension method. The host calls these in `Program.cs`. Modules register their own:
- Marten projections and document types
- Schema extensions
- HTTP clients and health contributors
- Background services
