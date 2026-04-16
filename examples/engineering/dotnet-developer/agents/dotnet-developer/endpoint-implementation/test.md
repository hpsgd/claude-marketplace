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
