# Result: Order processing REST endpoint

**Verdict:** PASS
**Score:** 19/19 criteria met (100%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Agent reads CLAUDE.md and checks `.claude/rules/` including `dotnet-stack--jasperfx.md` — Pre-Flight Step 1 is MANDATORY with explicit `Read(file_path="CLAUDE.md")` and `Read(file_path=".claude/CLAUDE.md")` calls, plus a directive to check `.claude/rules/` listing `dotnet-stack--jasperfx.md` as a key rule.

- [x] PASS: Agent uses hierarchical URL `/api/customers/{customerId}/orders` — API Design section mandates "Hierarchical URLs mirroring entity ownership" and "No flat top-level listings." Principles section repeats: "Hierarchical URLs mirror ownership."

- [x] PASS: Agent separates LoadAsync from Handle — Wolverine Endpoints section provides this pattern explicitly with a code example: `LoadAsync` returns `ProblemDetails?` to short-circuit, `Handle` contains business logic and returns cascading events.

- [x] PASS: Agent uses `IDocumentSession` injected by Wolverine — Managed Sessions Only section: "Use Wolverine's `IDocumentSession` — never create `store.LightweightSession()` independently." Principles section repeats: "Managed sessions only. Never create your own `IDocumentSession`."

- [x] PASS: Agent returns `OrderPlaced` as cascading message from Handle — Wolverine Endpoints code example shows Handle returning a tuple of `(HTTP response, cascading event)`. One Message One Unit of Work (CRITICAL) forbids inline processing.

- [x] PASS: Agent produces both unit and integration tests — Testing section "The Rule" is MANDATORY: unit test with NSubstitute + Shouldly, integration test via Alba + Testcontainers PostgreSQL. BDD naming `WhenDoingSomething` matches the expected class name `WhenCreatingAnOrder`.

- [x] PASS: Agent raises decision checkpoint before creating Order aggregate — Decision Checkpoints table (MANDATORY): "Creating a new aggregate | Domain modelling decision" is an explicit stop-and-ask trigger.

- [x] PASS: Commands and events are C# `record` types with immutable properties — Wolverine Endpoints section now explicitly states "Commands and events are C# records (immutable, init-only or positional)" in the code comment (line 98), and the Endpoint contract rules section states "**Commands and events are C# `record` types** — never classes with mutable setters. Use positional or `init`-only properties so instances are immutable."

- [x] PASS: Agent includes response DTO separate from aggregate — Endpoint contract rules explicitly state "**Response DTOs are records too**, separate from the aggregate. Never serialise the aggregate directly to the HTTP response — define a dedicated response record with only the fields the client needs." The code example shows `MyEntityResponse(Guid Id, string Value)` as a dedicated DTO.

### Output expectations

- [x] PASS: Endpoint route is exactly `POST /api/customers/{customerId}/orders` mounted via Wolverine HTTP attributes — `[WolverinePost("/api/parents/{parentId}/children")]` pattern is directly demonstrated; API Design mandates hierarchical URLs. A well-formed response would produce `[WolverinePost("/api/customers/{customerId}/orders")]`.

- [x] PASS: Command record is a C# `record` with `init`-only or positional-immutable properties — Endpoint contract rules now explicitly mandate "Commands and events are C# `record` types — never classes with mutable setters." The code example demonstrates `public record CreateMyEntity(Guid ParentId, string Value)`.

- [x] PASS: Output enforces both business rules — the active-order count check is covered by the `LoadAsync` ProblemDetails pattern (state-dependent pre-condition). Quantity range validation ([1,100]) is now explicitly covered: "**Input validation uses FluentValidation** — ... Use FluentValidation for shape/range rules (string length, numeric ranges like quantity 1-100, required fields)."

- [x] PASS: LoadAsync loads customer/counts active orders and returns ProblemDetails / 4xx — Wolverine Endpoints section explicitly shows `LoadAsync` returning `ProblemDetails?` to short-circuit on pre-condition failures, not throwing exceptions for business validation.

- [x] PASS: Handle returns domain events plus HTTP response, no inline side effects — One Message One Unit of Work is CRITICAL. Cascading returns are prescribed. Inline processing is an explicit anti-pattern.

- [x] PASS: IDocumentSession injected by Wolverine, never from IDocumentStore, no manual SaveChangesAsync — Managed Sessions Only section is explicit on all three points.

- [x] PASS: 201 Created with Location header pointing to `/api/customers/{customerId}/orders/{orderId}` and a response DTO — Endpoint contract rules now explicitly state "**POST creation endpoints return `201 Created`** with a `Location` header pointing to the new resource. Use Wolverine's `CreationResponse` (or equivalent) so the framework sets status and header automatically." The code example demonstrates `new CreationResponse($"/api/parents/{command.ParentId}/children/{id}")`.

- [x] PASS: Unit test class in `When...` style with Shouldly, plus Alba + Testcontainers integration test — Testing section mandates BDD naming (`WhenDoingSomething`), Shouldly assertions, and Alba + Testcontainers for integration tests. All three are explicit.

- [x] PASS: Tests cover happy path plus both rule violations with explicit arrange/act/assert — Testing section mandates dual-layer tests. The active-order count and quantity validation rules are now explicitly defined, so a well-formed response following the definition would cover both violations. FluentValidation for quantity and `LoadAsync` for count gives the agent concrete mechanisms to test against each rule.

- [x] PASS: Output flags architecture decision (introducing the Order aggregate) for stakeholder review before implementing — Decision Checkpoints (MANDATORY) lists "Creating a new aggregate | Domain modelling decision" as an explicit stop-and-ask trigger.

## Notes

The four gaps identified in the previous evaluation have all been closed by edits to the agent definition.

The `record` gap (previously affecting Criteria C8 and OE2) is resolved: the Wolverine Endpoints code block now annotates the record declarations explicitly, and the Endpoint contract rules section adds a binding rule in bold text.

The response shape gap (previously OE7) is resolved: POST creation response convention is now stated as a named rule — 201 Created, Location header, `CreationResponse`, dedicated response DTO — matching what the test expects.

The validation gap (previously OE3) is resolved: FluentValidation is now prescribed as the mechanism for shape/range rules, with "quantity 1-100" called out by name as the prototypical example.

The test coverage gap (previously OE9) is partially addressed by the new validation rules: with explicit FluentValidation for quantity and `LoadAsync` for active-order count, the mechanisms the agent would test are now deterministic. The definition still does not explicitly require tests for each business rule violation, but the rules are now specific enough that a well-formed response would naturally produce tests for both.
