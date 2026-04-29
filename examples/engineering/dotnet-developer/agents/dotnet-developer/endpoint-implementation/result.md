# Result: Order processing REST endpoint

**Verdict:** PARTIAL
**Score:** 14.5 / 19 criteria met (76%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Agent reads CLAUDE.md and checks `.claude/rules/` including `dotnet-stack--jasperfx.md` — Pre-Flight Step 1 is marked MANDATORY with explicit `Read(file_path="CLAUDE.md")` and `Read(file_path=".claude/CLAUDE.md")` calls, plus a directive to check `.claude/rules/` listing `dotnet-stack--jasperfx.md` as a key rule.

- [x] PASS: Agent uses hierarchical URL `/api/customers/{customerId}/orders` — API Design section: "Hierarchical URLs mirroring entity ownership" and "No flat top-level listings — every entity accessed through its parent chain." Principles section repeats: "Hierarchical URLs mirror ownership."

- [x] PASS: Agent separates LoadAsync from Handle — Wolverine Endpoints section provides this pattern explicitly with a code example: `LoadAsync` returns `ProblemDetails?` to short-circuit, `Handle` contains business logic and returns cascading events.

- [x] PASS: Agent uses `IDocumentSession` injected by Wolverine — Managed Sessions Only section: "Use Wolverine's `IDocumentSession` — never create `store.LightweightSession()` independently." Principles section repeats: "Managed sessions only. Never create your own `IDocumentSession`."

- [x] PASS: Agent returns `OrderPlaced` as cascading message from Handle — Wolverine Endpoints code example: "Return events as cascading messages." Cascading Handler Chains: "Return the next command — don't call the next handler directly." One Message One Unit of Work forbids inline processing.

- [x] PASS: Agent produces both unit and integration tests — Testing section "The Rule" is MANDATORY: unit test with NSubstitute + Shouldly, integration test via Alba + Testcontainers PostgreSQL. BDD naming `WhenDoingSomething` matches the expected class name `WhenCreatingAnOrder`.

- [x] PASS: Agent raises decision checkpoint before creating Order aggregate — Decision Checkpoints table (MANDATORY): "Creating a new aggregate | Domain modelling decision" is an explicit stop-and-ask trigger.

- [ ] FAIL: Commands and events are C# `record` types with immutable properties — the word "record" does not appear anywhere in the agent definition. Code examples use `static class` for endpoints and handlers. "Events are immutable history" appears in the Principles section but does not mandate C# `record` as the required construct for commands or events.

- [~] PARTIAL: Agent includes response DTO separate from aggregate — no mention of response DTOs, HTTP response shape, or DTO mapping in the definition. The endpoint example shows `Handle` returning an event without addressing the HTTP response body. Partially met: 0.5.

### Output expectations

- [x] PASS: Endpoint route is exactly `POST /api/customers/{customerId}/orders` mounted via Wolverine HTTP attributes — the Wolverine Endpoints pattern `[WolverineGet("/api/parents/{parentId}/children/{id}")]` with customerId bound from the route is directly demonstrated; API Design mandates hierarchical URLs. A well-formed agent response would produce `[WolverinePost("/api/customers/{customerId}/orders")]`.

- [ ] FAIL: Command record is a C# `record` with `init`-only or positional-immutable properties — the definition never uses the word "record." No constraint on whether commands should be `record` vs `class`. The agent could produce either without violating any stated rule.

- [~] PARTIAL: Output enforces both business rules — the active-order count check is directly covered by the `LoadAsync` ProblemDetails pattern. Quantity range validation ([1,100]) is not addressed: FluentValidation is listed only as an analyser package, not as a request-validation mechanism. A well-formed response would enforce the count rule but may omit or inconsistently handle quantity validation. Partially met: 0.5.

- [x] PASS: LoadAsync loads customer/counts active orders and returns ProblemDetails / 4xx — Wolverine Endpoints section explicitly shows `LoadAsync` returning `ProblemDetails?` to short-circuit on pre-condition failures, not throwing exceptions.

- [x] PASS: Handle returns domain events plus HTTP response, no inline side effects — One Message One Unit of Work is marked CRITICAL. Cascading returns are prescribed. Inline processing is an explicit anti-pattern.

- [x] PASS: IDocumentSession injected by Wolverine, never from IDocumentStore, no manual SaveChangesAsync — Managed Sessions Only section is explicit on all three points.

- [ ] FAIL: 201 Created with Location header pointing to `/api/customers/{customerId}/orders/{orderId}` and a response DTO — the definition gives no guidance on the HTTP status code for POST creation responses, Location headers, or the shape of the response body. A well-formed response could return any status code and any body without violating a stated rule.

- [x] PASS: Unit test class in `When...` style with Shouldly, plus Alba + Testcontainers integration test — Testing section mandates BDD naming (`WhenDoingSomething`), Shouldly assertions, and Alba + Testcontainers for integration tests. All three are explicit.

- [~] PARTIAL: Tests cover happy path plus both rule violations with explicit arrange/act/assert — Testing section mandates dual-layer tests but does not specify coverage of individual rule violations or require a Given/When/Then or arrange/act/assert structure beyond BDD class naming. The definition would produce tests, but whether they cover the 51st-order and quantity-out-of-range cases is not enforced. Partially met: 0.5.

- [x] PASS: Output flags architecture decision (introducing the Order aggregate) for stakeholder review before implementing — Decision Checkpoints (MANDATORY) lists "Creating a new aggregate | Domain modelling decision" as an explicit stop-and-ask trigger.

## Notes

Three gaps combine to drop this from PASS to PARTIAL.

The `record` gap appears in both sections (Criteria C8 and OE2). The definition covers immutability at the principle level ("Events are immutable history") but never at the language construct level. A developer following this definition alone could produce classes with mutable setters and not know they'd done something wrong. One line — "Commands and events are C# `record` types" — in the Architecture Rules section would close both criteria.

The response shape gap (OE7) is the most significant. The definition precisely covers what `Handle` returns internally (cascading events) but says nothing about the outbound HTTP contract: no mention of 201 Created, no Location header, no DTO vs aggregate distinction at the HTTP layer. For a POST endpoint that must return 201 with a new resource URL, this leaves the agent without any convention to follow. A sentence in the API Design or Wolverine Endpoints section — "POST endpoints return 201 Created with a Location header and a dedicated response record" — would close this.

The validation gap (OE3) is narrower: the active-order count check is well-covered by the `LoadAsync` pattern, but input validation (quantity range) has no prescribed mechanism. Adding FluentValidation usage guidance alongside the Wolverine Endpoints example would close it.

The test coverage gap (OE9) is minor: the dual-test mandate is strong, but the definition doesn't direct the agent to cover specific business rule violations. A note in the Testing section ("unit tests must cover at least the happy path and each distinct business rule violation") would make this deterministic.
