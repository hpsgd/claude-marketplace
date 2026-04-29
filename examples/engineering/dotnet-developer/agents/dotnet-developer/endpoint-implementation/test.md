# Test: Order processing REST endpoint

Scenario: User asks the .NET developer to implement a REST endpoint for creating and processing orders in a .NET 8 API that uses Wolverine and Marten with event sourcing.

## Prompt

We need a `POST /api/customers/{customerId}/orders` endpoint to create a new order. The request body contains line items (product ID, quantity, unit price). Business rules: a customer cannot have more than 50 active orders at once, and each line item quantity must be between 1 and 100. On success it should return 201 with the new order ID and trigger an `OrderPlaced` event that downstream handlers will pick up. We're using Wolverine for HTTP and Marten for persistence. Can you implement this including tests?

## Criteria

- [ ] PASS: Agent reads CLAUDE.md and checks `.claude/rules/` including `dotnet-stack--jasperfx.md` before writing code
- [ ] PASS: Agent uses hierarchical URL `/api/customers/{customerId}/orders` — does not propose a flat `/api/orders`
- [ ] PASS: Agent separates LoadAsync (pre-condition: customer exists, active order count < 50) from Handle (pure business logic returning OrderPlaced event)
- [ ] PASS: Agent uses `IDocumentSession` injected by Wolverine — does not create sessions from `IDocumentStore` directly
- [ ] PASS: Agent returns `OrderPlaced` event as a cascading message from Handle, not inline side-effect processing
- [ ] PASS: Agent produces both a unit test (WhenCreatingAnOrder class, Shouldly assertions) and an integration test (Alba + Testcontainers)
- [ ] PASS: Agent raises a decision checkpoint before creating the Order aggregate (architecture decision)
- [ ] PASS: Command and event are C# records (not classes), with immutable properties
- [ ] PARTIAL: Agent includes a response DTO separate from the aggregate — does not expose aggregate internals directly

## Output expectations

- [ ] PASS: Output's endpoint route is exactly `POST /api/customers/{customerId}/orders`, mounted via Wolverine HTTP attributes/conventions, with the customerId bound from the route
- [ ] PASS: Output's command record (e.g. `CreateOrder`) is a C# `record` with `init`-only or positional-immutable properties — not a class with mutable setters — and contains the line items collection and customerId
- [ ] PASS: Output enforces both business rules in code: line item quantity range [1,100] (validated via FluentValidation or in LoadAsync) and the customer's active-order count below 50 checked against persisted state
- [ ] PASS: Output's `LoadAsync` (or equivalent pre-condition step) loads the customer / counts active orders and returns a Problem Details / 4xx response when pre-conditions fail — not throwing exceptions for business validation
- [ ] PASS: Output's `Handle` returns the new domain event(s) (`OrderPlaced` and any cascading messages) plus the HTTP response — it does NOT execute side effects inline
- [ ] PASS: Output uses an `IDocumentSession` parameter injected by Wolverine and never instantiates a session from `IDocumentStore` directly, and never calls `SaveChangesAsync` manually
- [ ] PASS: Output's response is 201 Created with a Location header pointing to `/api/customers/{customerId}/orders/{orderId}` and a response DTO that does NOT directly serialise the aggregate
- [ ] PASS: Output includes both a unit test class named in the `When...` style (e.g. `WhenCreatingAnOrder`) using Shouldly assertions, and an integration test using Alba + Testcontainers for Postgres
- [ ] PASS: Output's tests cover the happy path plus both rule violations (51st active order rejected, quantity 0 / 101 rejected) with explicit Given/When/Then or arrange/act/assert structure
- [ ] PARTIAL: Output flags the architecture decision (introducing the Order aggregate) for stakeholder review before implementing rather than just creating it
