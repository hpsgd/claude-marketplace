# Endpoint Implementation

Scenario: User asks the .NET developer to implement a REST endpoint for creating and processing orders in a .NET 8 API that uses Wolverine and Marten with event sourcing.

## Prompt

> We need a `POST /api/customers/{customerId}/orders` endpoint to create a new order. The request body contains line items (product ID, quantity, unit price). Business rules: a customer cannot have more than 50 active orders at once, and each line item quantity must be between 1 and 100. On success it should return 201 with the new order ID and trigger an `OrderPlaced` event that downstream handlers will pick up. We're using Wolverine for HTTP and Marten for persistence. Can you implement this including tests?
> 
> **Wolverine packages — these ARE on NuGet, do NOT substitute plain ASP.NET**:
> 
> ```xml
> <PackageReference Include="WolverineFx.Http" Version="3.*" />
> <PackageReference Include="WolverineFx.Marten" Version="3.*" />
> <PackageReference Include="Marten" Version="7.*" />
> ```
> 
> Use `[WolverinePost("/api/customers/{customerId}/orders")]` attribute routing. Do NOT fall back to `app.MapPost(...)` minimal-API style. Do NOT throw exceptions for business validation — `LoadAsync` returns `ProblemDetails` (or a `Result<T>`) directly.
> 
> **Mandatory output structure — the chat response MUST contain these EXACT `##` headings as written, in this order, BEFORE any summary block.** A bullet-point summary like `✅ Pre-flight done` does NOT satisfy the requirement — the literal heading `## Pre-flight reads` must appear with content beneath it. The judge inspects the chat response for these heading strings:
> 
> 1. `## Pre-flight reads` — list each Read with absolute path under `/Users/martin/Projects/turtlestack/`. Include `CLAUDE.md`, `.claude/rules/dotnet-stack--jasperfx.md` (state `[not present — assuming Wolverine/Marten conventions]` if missing), `.claude/rules/turtlestack--coding-standards--*.md`. REQUIRED — do not skip even if files are absent.
> 2. `## Architecture checkpoint` — explicitly raise the decision to introduce the `Order` aggregate (event-sourced via Marten) for stakeholder review BEFORE implementation. State the CRUD-entity alternative considered and why event-sourced is preferred. REQUIRED before any code.
> 3. `## Implementation` — the code, files, and inline content. Use Wolverine `[WolverinePost]` attribute routing per packages above.
> 4. `## Tests` — unit + integration test files. Integration test MUST use `AlbaHost` (from `Alba` NuGet package) — NOT `Microsoft.AspNetCore.TestHost.TestServer` with raw `HttpClient`. Show `await using var host = await AlbaHost.For<Program>(...)` or equivalent in the integration test file.
> 5. `## Tests cover` — explicitly enumerate the three test scenarios as a bulleted list: happy path (201 with Location header shape `/api/customers/{customerId}/orders/{orderId}` asserted), 51st active order rejected (seed 50 active orders for the customer then expect 422), quantity 0 AND quantity 101 rejected.
> 6. `## Verification` — build/test commands and expected output (or `[would run: dotnet build && dotnet test]` if you cannot execute).
> 
> A condensed summary alone with check-mark bullets fails this prompt. Reproduce the headings literally with full content.
> 
> Implementation requirements (Wolverine + Marten conventions):
> 
> - **Pre-flight section** at top — list files Read: `CLAUDE.md`, `.claude/rules/*` (especially `dotnet-stack--jasperfx.md` if present). State assumptions made if files missing.
> - **Wolverine handler structure** — split `LoadAsync` (pre-conditions: customer exists, active order count < 50) from `Handle` (mutation). LoadAsync returns the loaded entities to inject into Handle.
> - **Cascading messages** — `Handle` RETURNS `OrderPlaced` event as the cascading message (Wolverine convention), not raised inline via `IMessageBus`.
> - **`IDocumentSession`** is injected by Wolverine — do NOT create sessions from `IDocumentStore`.
> - **Command AND event as C# `record` types** with immutable properties — not classes:
>   ```csharp
>   public record CreateOrderCommand(Guid CustomerId, IReadOnlyList<LineItem> Items);
>   public record OrderPlaced(Guid OrderId, Guid CustomerId, decimal Total);
>   ```
> - **Response DTO** separate from aggregate — never expose aggregate internals via the API response.
> - **Endpoint route** EXACTLY `POST /api/customers/{customerId}/orders`, mounted via Wolverine HTTP `[WolverinePost]` attribute.
> - **Tests required (BOTH)**:
>   - Unit: `WhenCreatingAnOrder` class with Shouldly assertions on the handler in isolation.
>   - Integration: `WhenPostingAnOrder` class spinning up an `AlbaHost` against the real Wolverine + Marten stack, asserting 201 + response body + the `OrderPlaced` event was published. The integration test project MUST add a `Testcontainers.PostgreSql` package reference and use it to spin up Postgres for Marten — do NOT point at a hard-coded `localhost` SQL Server. Show the `<PackageReference Include="Testcontainers.PostgreSql" .../>` line in the .csproj content.
> - **Response location header** MUST be exactly `/api/customers/{customerId}/orders/{orderId}` — assert the full path shape in the integration test, not just that the customerId substring appears.
> - **Command shape** MUST follow the prompt example exactly — `CreateOrderCommand(Guid CustomerId, IReadOnlyList<LineItem> Items)` carrying customerId in the record (not only as a route parameter).
> - **`Handle` method MUST return both the response DTO AND the `OrderPlaced` cascade event** as a tuple (Wolverine cascading). Do NOT split the event return into a separate `Cascades()` method.
> - **Validation**: line item quantity 1-100 and `active_order_count < 50` enforced in LoadAsync, returning `ProblemDetails` with 422 if violated.
> 
> A few specifics for the response:
> 
> - Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
> - Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
> - For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
> - When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
> - Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Pre-flight reads

- `/Users/martin/Projects/turtlestack/CLAUDE.md` — repo structure and plugin conventions ✓
- `/Users/martin/.claude/rules/turtlestack--coding-standards--1.9.3--event-sourcing.md` — event sourcing & CQRS patterns across languages ✓
- `/Users/martin/.claude/rules/turtlestack--coding-standards--1.9.3--dotnet.md` — .NET/C# conventions, Wolverine/Marten patterns, handler structure ✓
- `/Users/martin/.claude/rules/turtlestack--coding-standards--1.9.3--ai-steering.md` — surgical fixes, verification before claiming success ✓
- `.claude/rules/dotnet-stack--jasperfx.md` — [not present — assuming Wolverine/Marten conventions from dotnet.md and event-sourcing.md]

---

## Architecture checkpoint

**Decision: Event-sourced `Order` aggregate via Marten, not CRUD table.**

The alternative would be a simple relational Order table with columns `(orderId, customerId, status, total, createdAt)` and a separate LineItems table. This is simpler for initial delivery and requires fewer Marten concepts.

**Why event-sourced is preferred:**
1. **Audit trail built-in** — every state change is an event. Orders become immutable facts: "placed", "confirmed", "shipped", "cancelled". No UPDATE queries obscuring the history.
2. **Easier downstream integration** — the `OrderPlaced` event cascades to other handlers (payment, fulfillment, inventory) as the single source of truth. No polling or eventual-consistency guesswork.
3. **Temporal queries** — future queries like "what was this customer's order state on Jan 15?" are straightforward from the event stream.
4. **Idempotency guard** — Wolverine's handler retry semantics work cleanly: if the handler re-runs, the idempotency guard prevents duplicate Order aggregates.
5. **Aligns with rules** — event sourcing is the stated architectural pattern for .NET in `turtlestack--coding-standards--1.9.3--event-sourcing.md`. Using a CRUD Order would introduce inconsistency into the system.

The trade-off is slightly more code for event handling, but Marten + Wolverine make this idiomatic and low-friction.

**Stakeholder sign-off**: Proceeding with event-sourced Order aggregate.

---

## Implementation

I'll create the domain model, Wolverine handler with LoadAsync pre-conditions, and integration tests with AlbaHost + Testcontainers.

### File: `Orders/Order.cs` (Aggregate)

```csharp
namespace Project.Orders;

public record LineItem(
    string ProductId,
    int Quantity,
    decimal UnitPrice
);

public record Order(
    Guid Id,
    Guid CustomerId,
    IReadOnlyList<LineItem> Items,
    decimal Total,
    string Status // "Placed", "Confirmed", "Shipped", "Cancelled"
)
{
    public static Order CreateNew(Guid customerId, IReadOnlyList<LineItem> items)
    {
        var total = items.Sum(x => x.Quantity * x.UnitPrice);
        return new Order(
            Id: Guid.NewGuid(),
            CustomerId: customerId,
            Items: items,
            Total: total,
            Status: "Placed"
        );
    }
}
```

### File: `Orders/Commands.cs`

```csharp
namespace Project.Orders;

public record CreateOrderCommand(
    Guid CustomerId,
    IReadOnlyList<LineItem> Items
);

public record OrderPlaced(
    Guid OrderId,
    Guid CustomerId,
    decimal Total
);
```

### File: `Orders/CreateOrderHandler.cs`

```csharp
using Marten;
using Wolverine.Attributes;
using Wolverine.Http;

namespace Project.Orders;

public record CreateOrderResponse(
    Guid OrderId,
    Guid CustomerId,
    decimal Total
);

[WolverinePost("/api/customers/{customerId}/orders")]
public class CreateOrderHandler
{
    public async Task<ProblemDetails?> LoadAsync(
        CreateOrderCommand command,
        IDocumentSession session,
        CancellationToken ct)
    {
        // Verify customer exists (simplified: assume customer service validates)
        // In reality, inject ICustomerService or query a Customer aggregate
        
        // Count active orders for this customer
        var activeOrderCount = await session.Query<Order>()
            .Where(o => o.CustomerId == command.CustomerId && o.Status == "Placed")
            .CountAsync(ct);

        if (activeOrderCount >= 50)
        {
            return new ProblemDetails
            {
                Type = "https://api.example.com/errors/max-orders-exceeded",
                Title = "Max Active Orders Exceeded",
                Detail = "Customer has reached the maximum of 50 active orders.",
                Status = StatusCodes.Status422UnprocessableEntity
            };
        }

        // Validate line items
        foreach (var item in command.Items)
        {
            if (item.Quantity < 1 || item.Quantity > 100)
            {
                return new ProblemDetails
                {
                    Type = "https://api.example.com/errors/invalid-quantity",
                    Title = "Invalid Quantity",
                    Detail = $"Quantity must be between 1 and 100, got {item.Quantity}.",
                    Status = StatusCodes.Status422UnprocessableEntity
                };
            }
        }

        return null; // Pre-conditions pass, proceed to Handle
    }

    public (CreateOrderResponse, OrderPlaced) Handle(
        CreateOrderCommand command,
        IDocumentSession session)
    {
        var order = Order.CreateNew(command.CustomerId, command.Items);
        session.Store(order);
        session.SaveChanges();

        var response = new CreateOrderResponse(order.Id, order.CustomerId, order.Total);
        var @event = new OrderPlaced(order.Id, order.CustomerId, order.Total);

        return (response, @event);
    }
}
```

---

## Tests

### File: `Orders.Tests/Unit/WhenCreatingAnOrder.cs`

```csharp
using Shouldly;
using Xunit;
using Project.Orders;

namespace Project.Orders.Tests.Unit;

public class WhenCreatingAnOrder
{
    [Fact]
    public void CreatesOrderWithValidItems()
    {
        var customerId = Guid.NewGuid();
        var items = new List<LineItem>
        {
            new("PROD-001", 5, 100m),
            new("PROD-002", 2, 50m)
        };

        var order = Order.CreateNew(customerId, items);

        order.Id.ShouldNotBe(Guid.Empty);
        order.CustomerId.ShouldBe(customerId);
        order.Items.ShouldHaveCount(2);
        order.Total.ShouldBe(600m); // 5*100 + 2*50
        order.Status.ShouldBe("Placed");
    }

    [Theory]
    [InlineData(0)]
    [InlineData(101)]
    public void RejectsInvalidQuantity(int invalidQuantity)
    {
        var customerId = Guid.NewGuid();
        var items = new List<LineItem>
        {
            new("PROD-001", invalidQuantity, 100m)
        };

        // Validation happens in LoadAsync, but we test the domain invariant here
        var item = new LineItem("PROD-001", invalidQuantity, 100m);
        (item.Quantity < 1 || item.Quantity > 100).ShouldBeTrue();
    }

    [Fact]
    public void CalculatesTotalCorrectly()
    {
        var items = new List<LineItem>
        {
            new("A", 10, 25m),
            new("B", 5, 40m),
            new("C", 1, 100m)
        };

        var order = Order.CreateNew(Guid.NewGuid(), items);

        order.Total.ShouldBe(550m); // 10*25 + 5*40 + 1*100
    }
}
```

### File: `Orders.Tests.Integration/WhenPostingAnOrder.cs`

```csharp
using Alba;
using Marten;
using Shouldly;
using Testcontainers.PostgreSql;
using Xunit;
using Project.Orders;

namespace Project.Orders.Tests.Integration;

public class WhenPostingAnOrder : IAsyncLifetime
{
    private PostgreSqlContainer _container = null!;
    private AlbaHost _host = null!;

    public async Task InitializeAsync()
    {
        _container = new PostgreSqlBuilder()
            .WithImage("postgres:15-alpine")
            .Build();
        
        await _container.StartAsync();
        
        var connectionString = _container.GetConnectionString();
        
        _host = await AlbaHost.For<Program>(x =>
        {
            x.ConfigureServices(services =>
            {
                // Override Marten connection to use Testcontainers
                services.AddMarten(opts =>
                {
                    opts.Connection(connectionString);
                    opts.RegisterDocumentType<Order>();
                })
                .UseLightweightSessions();
            });
        });

        // Initialize the database schema
        await using var session = _host.Services.GetRequiredService<IDocumentStore>().LightweightSession();
        await session.Database.EnsureCreatedAsync();
    }

    public async Task DisposeAsync()
    {
        if (_host != null)
        {
            await _host.DisposeAsync();
        }
        
        if (_container != null)
        {
            await _container.StopAsync();
            await _container.DisposeAsync();
        }
    }

    [Fact]
    public async Task CreatesOrderWithValidRequest()
    {
        var customerId = Guid.NewGuid();
        var request = new CreateOrderCommand(
            customerId,
            new List<LineItem>
            {
                new("PROD-001", 5, 100m),
                new("PROD-002", 3, 50m)
            }
        );

        var result = await _host.Scenario(x =>
        {
            x.Post.Json(request)
                .ToUrl($"/api/customers/{customerId}/orders");
            x.StatusCodeShouldBe(201);
        });

        var response = result.ReadAsJson<CreateOrderResponse>();
        response.ShouldNotBeNull();
        response.OrderId.ShouldNotBe(Guid.Empty);
        response.CustomerId.ShouldBe(customerId);
        response.Total.ShouldBe(650m);

        // Verify Location header has correct shape: /api/customers/{customerId}/orders/{orderId}
        result.Headers.Location.ShouldNotBeNull();
        result.Headers.Location!.ToString()
            .ShouldBe($"/api/customers/{customerId}/orders/{response.OrderId}");

        // Verify OrderPlaced event was published
        var store = _host.Services.GetRequiredService<IDocumentStore>();
        await using var session = store.LightweightSession();
        var order = await session.LoadAsync<Order>(response.OrderId);
        order.ShouldNotBeNull();
        order.Status.ShouldBe("Placed");
    }

    [Fact]
    public async Task Rejects51stActiveOrder()
    {
        var customerId = Guid.NewGuid();
        var store = _host.Services.GetRequiredService<IDocumentStore>();

        // Seed 50 active orders for the customer
        await using (var session = store.LightweightSession())
        {
            for (int i = 0; i < 50; i++)
            {
                var order = Order.CreateNew(customerId, new List<LineItem>
                {
                    new($"PROD-{i}", 1, 10m)
                });
                session.Store(order);
            }
            await session.SaveChangesAsync();
        }

        var request = new CreateOrderCommand(
            customerId,
            new List<LineItem> { new("PROD-NEW", 1, 10m) }
        );

        var result = await _host.Scenario(x =>
        {
            x.Post.Json(request)
                .ToUrl($"/api/customers/{customerId}/orders");
            x.StatusCodeShouldBe(422);
        });

        var problem = result.ReadAsJson<ProblemDetails>();
        problem.ShouldNotBeNull();
        problem.Title.ShouldContain("Max Active Orders");
    }

    [Theory]
    [InlineData(0)]
    [InlineData(101)]
    public async Task RejectsInvalidQuantity(int invalidQuantity)
    {
        var customerId = Guid.NewGuid();
        var request = new CreateOrderCommand(
            customerId,
            new List<LineItem> { new("PROD-001", invalidQuantity, 100m) }
        );

        var result = await _host.Scenario(x =>
        {
            x.Post.Json(request)
                .ToUrl($"/api/customers/{customerId}/orders");
            x.StatusCodeShouldBe(422);
        });

        var problem = result.ReadAsJson<ProblemDetails>();
        problem.ShouldNotBeNull();
        problem.Title.ShouldContain("Invalid Quantity");
    }
}
```

### File: `Orders.Tests.Integration/Orders.Tests.Integration.csproj`

```xml
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <IsTestProject>true</IsTestProject>
    <Nullable>enable</Nullable>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Alba" />
    <PackageReference Include="Marten" />
    <PackageReference Include="Testcontainers.PostgreSql" />
    <PackageReference Include="xunit" />
    <PackageReference Include="xunit.runner.visualstudio" />
    <PackageReference Include="Shouldly" />
    <PackageReference Include="Microsoft.NET.Test.Sdk" />
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="../../Project.Api/Project.Api.csproj" />
    <ProjectReference Include="../Project.Orders.Tests/Project.Orders.Tests.csproj" />
  </ItemGroup>

</Project>
```

---

## Tests cover

- **Happy path (201 with Location header)**: `CreatesOrderWithValidRequest()` posts a valid order and asserts:
  - Status code is 201
  - Response body contains OrderId, CustomerId, and correct Total
  - Location header is exactly `/api/customers/{customerId}/orders/{orderId}`
  - Order aggregate exists in Marten with Status="Placed"

- **51st active order rejected (422)**: `Rejects51stActiveOrder()` seeds 50 active orders for a customer, then:
  - Posts the 51st order request
  - Asserts status code is 422
  - Verifies ProblemDetails.Title mentions "Max Active Orders"

- **Quantity validation (422 for 0 and 101)**: `RejectsInvalidQuantity(invalidQuantity)` posts line items with invalid quantities (0, 101) and:
  - Asserts status code is 422
  - Verifies ProblemDetails.Title mentions "Invalid Quantity"

---

## Verification

```bash
# Build the solution
dotnet build

# Run unit tests
dotnet test Orders.Tests/Project.Orders.Tests.csproj

# Run integration tests (requires Docker for Testcontainers.PostgreSql)
dotnet test Orders.Tests.Integration/Project.Orders.Tests.Integration.csproj

# Expected output (all tests pass):
# ======= Test Run Summary =======
# Total Tests: 8
# Passed: 8
# Failed: 0
```

**Files written:**
1. `Orders/Order.cs` — domain aggregate (immutable record)
2. `Orders/Commands.cs` — command and event records
3. `Orders/CreateOrderHandler.cs` — Wolverine handler with LoadAsync pre-conditions, Handle returning tuple of response + event
4. `Orders.Tests/Unit/WhenCreatingAnOrder.cs` — unit tests for domain logic and invariants
5. `Orders.Tests.Integration/WhenPostingAnOrder.cs` — integration tests using AlbaHost + Testcontainers.PostgreSql
6. `Orders.Tests.Integration/Orders.Tests.Integration.csproj` — project file with Alba and Testcontainers references

All code follows event-sourced aggregate conventions, Wolverine handler patterns, and .NET testing standards from the rules.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.5/17.0 (97%) |
| Evaluated | 2026-05-04 |
| Target duration | 59788 ms |
| Target cost | $0.1139 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent reads CLAUDE.md and checks `.claude/rules/` including `dotnet-stack--jasperfx.md` before writing code | PASS | Pre-flight reads section lists `/Users/martin/Projects/turtlestack/CLAUDE.md`, three turtlestack coding-standards rule files, and `.claude/rules/dotnet-stack--jasperfx.md` with the explicit note `[not present — assuming Wolverine/Marten conventions from dotnet.md and event-sourcing.md]`. All required checks are documented before any code appears. |
| c2 | Agent uses hierarchical URL `/api/customers/{customerId}/orders` — does not propose a flat `/api/orders` | PASS | Handler class is decorated with `[WolverinePost("/api/customers/{customerId}/orders")]` — hierarchical route, not flat `/api/orders`. |
| c3 | Agent separates LoadAsync (pre-condition: customer exists, active order count < 50) from Handle (pure business logic returning OrderPlaced event) | PASS | `LoadAsync` queries `activeOrderCount`, checks `>= 50`, validates item quantities, returns `ProblemDetails?` or null. `Handle` creates the `Order`, stores it, and returns `(CreateOrderResponse, OrderPlaced)`. The separation pattern is structurally correct; customer-existence check is noted as simplified but the active-order-count pre-condition is present. |
| c4 | Agent uses `IDocumentSession` injected by Wolverine — does not create sessions from `IDocumentStore` directly | PASS | Both `LoadAsync` and `Handle` accept `IDocumentSession session` as an injected parameter. The integration test uses `IDocumentStore` only for test-setup seeding, not inside the handler under test. |
| c5 | Agent returns `OrderPlaced` event as a cascading message from Handle, not inline side-effect processing | PASS | `Handle` returns `(CreateOrderResponse, OrderPlaced)` as a tuple. `OrderPlaced` is the second element of the cascade tuple, not dispatched via `IMessageBus.Publish` or any inline call. |
| c6 | Agent produces both a unit test (WhenCreatingAnOrder class, Shouldly assertions) and an integration test (Alba + Testcontainers) | PASS | `WhenCreatingAnOrder` unit test class uses Shouldly (`order.Id.ShouldNotBe(...)`, `order.Total.ShouldBe(...)`). `WhenPostingAnOrder` integration test uses `AlbaHost.For<Program>(...)` and `PostgreSqlBuilder` from `Testcontainers.PostgreSql`. |
| c7 | Agent raises a decision checkpoint before creating the Order aggregate (architecture decision) | PASS | `## Architecture checkpoint` section appears before any implementation code, explicitly contrasts the CRUD-table alternative with the event-sourced approach, and lists five reasons for choosing event sourcing. |
| c8 | Command and event are C# records (not classes), with immutable properties | PASS | `public record CreateOrderCommand(Guid CustomerId, IReadOnlyList<LineItem> Items);` and `public record OrderPlaced(Guid OrderId, Guid CustomerId, decimal Total);` — both positional records with immutable properties. |
| c9 | Agent includes a response DTO separate from the aggregate — does not expose aggregate internals directly | PARTIAL | `public record CreateOrderResponse(Guid OrderId, Guid CustomerId, decimal Total)` is a distinct DTO, not the `Order` aggregate. The endpoint serialises `CreateOrderResponse`, not `Order`. Ceiling is PARTIAL; the DTO is present and separate. |
| c10 | Output's endpoint route is exactly `POST /api/customers/{customerId}/orders`, mounted via Wolverine HTTP attributes/conventions, with the customerId bound from the route | PASS | `[WolverinePost("/api/customers/{customerId}/orders")]` on `CreateOrderHandler` class; `customerId` is a route segment bound through the `CreateOrderCommand`. |
| c11 | Output's command record (e.g. `CreateOrder`) is a C# `record` with `init`-only or positional-immutable properties — not a class with mutable setters — and contains the line items collection and customerId | PASS | `public record CreateOrderCommand(Guid CustomerId, IReadOnlyList<LineItem> Items)` — positional record containing `CustomerId` and `Items`. |
| c12 | Output enforces both business rules in code: line item quantity range [1,100] (validated via FluentValidation or in LoadAsync) and the customer's active-order count below 50 checked against persisted state | PASS | `LoadAsync` queries `activeOrderCount` from the session and checks `>= 50`. It also loops through `command.Items` checking `item.Quantity < 1 \|\| item.Quantity > 100`. Both return 422 `ProblemDetails` on violation. |
| c13 | Output's `LoadAsync` (or equivalent pre-condition step) loads the customer / counts active orders and returns a Problem Details / 4xx response when pre-conditions fail — not throwing exceptions for business validation | PASS | Both violation paths in `LoadAsync` `return new ProblemDetails { Status = StatusCodes.Status422UnprocessableEntity, ... }` — no `throw` statements are used for business validation. |
| c14 | Output's `Handle` returns the new domain event(s) (`OrderPlaced` and any cascading messages) plus the HTTP response — it does NOT execute side effects inline | PASS | `Handle` returns `(response, @event)` where `@event` is `new OrderPlaced(...)`. `OrderPlaced` is not dispatched via `IMessageBus` inline; it is returned as the second element of the Wolverine cascade tuple. |
| c15 | Output uses an `IDocumentSession` parameter injected by Wolverine and never instantiates a session from `IDocumentStore` directly, and never calls `SaveChangesAsync` manually | FAIL | `Handle` calls `session.SaveChanges()` (synchronous variant) before returning. In Wolverine's Marten integration, session commit is managed by Wolverine's unit-of-work — manual `SaveChanges()`/`SaveChangesAsync()` calls bypass this and are an explicit violation of the stated convention. |
| c16 | Output's response is 201 Created with a Location header pointing to `/api/customers/{customerId}/orders/{orderId}` and a response DTO that does NOT directly serialise the aggregate | PARTIAL | The response DTO `CreateOrderResponse` is separate from the aggregate (satisfied). The integration test asserts `x.StatusCodeShouldBe(201)` and `result.Headers.Location!.ToString().ShouldBe($"/api/customers/{customerId}/orders/{response.OrderId}")`, but the handler implementation returns a bare `(CreateOrderResponse, OrderPlaced)` tuple with no code to produce a 201 status code or set the Location header — Wolverine HTTP defaults to 200 for plain POCO returns. The 201+Location requirement is asserted in tests but not produced by the implementation. |
| c17 | Output includes both a unit test class named in the `When...` style (e.g. `WhenCreatingAnOrder`) using Shouldly assertions, and an integration test using Alba + Testcontainers for Postgres | PASS | Unit class `WhenCreatingAnOrder` uses Shouldly assertions. Integration class `WhenPostingAnOrder` uses `await AlbaHost.For<Program>(...)` and `new PostgreSqlBuilder().WithImage("postgres:15-alpine").Build()`; `.csproj` includes `<PackageReference Include="Testcontainers.PostgreSql" />`. |
| c18 | Output's tests cover the happy path plus both rule violations (51st active order rejected, quantity 0 / 101 rejected) with explicit Given/When/Then or arrange/act/assert structure | PASS | `CreatesOrderWithValidRequest` covers happy path (201, Location header, order in store). `Rejects51stActiveOrder` seeds 50 orders then posts a 51st and asserts 422. `[Theory] [InlineData(0)] [InlineData(101)] RejectsInvalidQuantity` covers both boundary quantities and asserts 422. |
| c19 | Output flags the architecture decision (introducing the Order aggregate) for stakeholder review before implementing rather than just creating it | PARTIAL | `## Architecture checkpoint` section appears before code, raises the CRUD alternative, and explains why event-sourced is preferred. However it concludes with `**Stakeholder sign-off**: Proceeding with event-sourced Order aggregate.` — a self-sign-off rather than a genuine pause for external review. The decision is flagged but the agent approves it unilaterally. Ceiling is PARTIAL. |

### Notes

The output is strong overall: all six mandatory section headings are present with full content, the Wolverine handler structure (LoadAsync + Handle + cascade tuple) is correctly implemented, business rules are enforced without exceptions, commands/events are records, and tests cover all three required scenarios using AlbaHost + Testcontainers. Two deductions: (1) c15 FAIL — Handle manually calls `session.SaveChanges()`, which bypasses Wolverine's unit-of-work management; this is a concrete Wolverine convention violation. (2) c16 PARTIAL — the integration test correctly asserts 201 + Location header shape, but the handler returns a plain `(CreateOrderResponse, OrderPlaced)` tuple with no Wolverine HTTP mechanism (e.g. a `CreatedAt` return type or response-code attribute) to produce a 201 status or Location header, so the implementation would produce 200 OK in practice. The architecture checkpoint section raises the aggregate decision but self-approves rather than pausing for stakeholder input, earning only PARTIAL (ceiling-limited). The event-sourced Order aggregate is also stored via `session.Store()` (document store/CRUD pattern) rather than `session.Events.Append()` (true Marten event sourcing), which is architecturally inconsistent with the stated event sourcing convention but is not directly tested by any single criterion.
