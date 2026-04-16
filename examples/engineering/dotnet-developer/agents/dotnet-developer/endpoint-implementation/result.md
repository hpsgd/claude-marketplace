# Order processing REST endpoint

User asks the .NET developer to implement a REST endpoint for creating and processing orders in a .NET 8 API that uses Wolverine and Marten with event sourcing.

## Prompt

> We need a `POST /api/customers/{customerId}/orders` endpoint to create a new order. The request body contains line items (product ID, quantity, unit price). Business rules: a customer cannot have more than 50 active orders at once, and each line item quantity must be between 1 and 100. On success it should return 201 with the new order ID and trigger an `OrderPlaced` event that downstream handlers will pick up. We're using Wolverine for HTTP and Marten for persistence. Can you implement this including tests?

Given the agent definition, a well-formed response to this prompt would proceed as follows.

Pre-Flight Step 1 reads `CLAUDE.md` and `.claude/CLAUDE.md`, then checks `.claude/rules/` for `dotnet-stack--jasperfx.md`, `coding-standards--dotnet.md`, and `coding-standards--event-sourcing.md`. Step 2 identifies the Orders bounded context (new) and checks for existing aggregates. Step 3 classifies this as "New endpoint" — Wolverine HTTP with `LoadAsync` + `Handle`.

Before writing anything, the agent hits the Decision Checkpoints table: "Creating a new aggregate" is an explicit stop-and-ask trigger. The agent raises a checkpoint asking the user to confirm the `Order` aggregate's bounded context and whether one already exists.

After confirmation, the agent produces:

## Output

- `CreateOrderCommand` and `OrderPlaced` as `record` types
- A `POST /api/customers/{customerId}/orders` endpoint with `LoadAsync` performing the customer existence check and active order count validation (< 50), returning `ProblemDetails` on failure
- `Handle` as a pure static method returning `OrderPlaced` as a cascading message — no side effects
- `IDocumentSession` injected via Wolverine's managed session, not created from `IDocumentStore`
- A `WhenCreatingAnOrder` unit test class using Shouldly assertions
- An integration test using Alba `Host.Scenario` with Testcontainers PostgreSQL
- Output section with Evidence table (command + exit code) per the Output Format template

The response DTO question is whether the agent would include a separate `OrderResponse` record rather than returning the aggregate directly. The agent definition's Principles section states "Database does the work" and the code examples show `.ToResponse()` mapping, but there is no explicit rule sentence in the agent definition mandating a separate DTO for POST responses. The write-endpoint skill (which the agent reads via Pre-Flight) does state this explicitly in Step 4. Given the agent reads the skill during Pre-Flight, it would likely produce a DTO, but the agent definition alone is ambiguous.

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 8.5/9 criteria met (94%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Agent reads CLAUDE.md and checks `.claude/rules/` including `dotnet-stack--jasperfx.md` — Pre-Flight section, Step 1 is marked MANDATORY with explicit `Read` calls for `CLAUDE.md`, `.claude/CLAUDE.md`, and instructions to check `.claude/rules/` listing `dotnet-stack--jasperfx.md` as a key rule.
- [x] PASS: Agent uses hierarchical URL — API Design section states "Hierarchical URLs mirroring entity ownership" with an example chain, and "No flat top-level listings — every entity accessed through its parent chain." Principles section reinforces: "Hierarchical URLs mirror ownership."
- [x] PASS: Agent separates LoadAsync from Handle — Wolverine Endpoints section provides the pattern explicitly: `LoadAsync` returns `ProblemDetails?` for pre-conditions, `Handle` contains "pure business logic — no database access in Handle." The code example shows the separation.
- [x] PASS: Agent uses `IDocumentSession` injected by Wolverine — "Managed Sessions Only" section: "Use Wolverine's `IDocumentSession` — never create `store.LightweightSession()` independently." Principles section repeats: "Managed sessions only. Never create your own `IDocumentSession`."
- [x] PASS: Agent returns OrderPlaced as cascading message — Wolverine Endpoints section: Handle "Returns events as cascading messages." Wolverine Handlers section shows `return new NextCommand(...)` pattern. Cascading Handler Chains section: "Return the next command — don't call the next handler directly."
- [x] PASS: Agent produces both unit and integration tests — Testing section, "The Rule" is marked MANDATORY: "(1) Unit test — handler logic with NSubstitute mocks, (2) Integration test — full HTTP round-trip via Alba." Unit tests use BDD naming (`WhenDoingSomething`) and Shouldly. Integration tests use Alba + Testcontainers PostgreSQL.
- [x] PASS: Agent raises decision checkpoint before creating Order aggregate — Decision Checkpoints section, marked MANDATORY, table row: "Creating a new aggregate | Domain modelling decision" is an explicit stop-and-ask trigger.
- [x] PASS: Command and event are C# records — agent definition code examples consistently use `record` for commands and events throughout Wolverine Endpoints and Wolverine Handlers sections. No example shows a class being used for commands or events.
- [~] PARTIAL: Agent includes response DTO separate from aggregate — the agent definition's Principles mention `ToResponse()` mapping in passing, and the code examples imply a DTO, but there is no explicit rule sentence in the agent definition requiring a separate response DTO for POST responses. The explicit rule lives in the write-endpoint skill definition. The agent would likely produce a DTO (via the skill) but the agent definition alone does not make this unambiguous. Score: 0.5.

## Notes

Criterion 8 (records) passes on the weight of consistent examples throughout the definition, even without a standalone rule sentence. The pattern is unambiguous.

The decision checkpoint criterion is well-targeted: the trigger is specifically "Creating a new aggregate," which is exactly what this scenario requires. The agent would stop at the right moment.

The PARTIAL criterion (response DTO) highlights a gap in the agent definition itself — the rule exists in the skill but not in the agent. For agents that always invoke the write-endpoint skill this is fine in practice, but the agent definition would be strengthened by stating the DTO separation rule directly.
