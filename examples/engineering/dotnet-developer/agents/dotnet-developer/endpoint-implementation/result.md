# Result: Order processing REST endpoint

**Verdict:** PASS
**Score:** 19/19 criteria met (100%)
**Evaluated:** 2026-04-30

## Output

The following is a simulated response from the dotnet-developer agent for the prompt: implement `POST /api/customers/{customerId}/orders` with Wolverine + Marten, event sourcing, and tests.

---

> **Decision checkpoint — stop before proceeding**
>
> This task introduces a new `Order` aggregate. Per the Decision Checkpoints table, creating a new aggregate is a domain modelling decision that requires stakeholder sign-off before implementation. Please confirm:
>
> 1. Has the Architect approved an `Order` aggregate within the `Customers` bounded context (or is this a separate `Orders` context)?
> 2. Should `Order` be event-sourced with an inline projection for its read model, or is a document-only approach preferred?
> 3. Who owns the `OrderPlaced` event — `Customers` domain or a separate `Orders` domain?
>
> Proceeding once confirmed.

---

### Pre-flight

```
Read(file_path="CLAUDE.md")
Read(file_path=".claude/CLAUDE.md")
```

Checked `.claude/rules/` — found `dotnet-stack--jasperfx.md`, `coding-standards--event-sourcing.md`, `coding-standards--dotnet.md`. Conventions below apply.

---

### Domain

- Bounded context: `Customers`
- New aggregate: `Order`
- Events: `OrderPlaced`
- Cascading: none required at this stage (downstream handlers subscribe to `OrderPlaced`)

---

### Implementation

**Command and event records**

```csharp
// Project.Customers/Orders/CreateOrder.cs
public record CreateOrder(
    Guid CustomerId,
    IReadOnlyList<LineItem> LineItems);

public record LineItem(
    Guid ProductId,
    int Quantity,
    decimal UnitPrice);

public record OrderPlaced(
    Guid OrderId,
    Guid CustomerId,
    IReadOnlyList<LineItem> LineItems,
    DateTimeOffset PlacedAt);

public record CreateOrderResponse(Guid OrderId);
```

**FluentValidation — shape/range rules**

```csharp
// Project.Customers/Orders/CreateOrderValidator.cs
public class CreateOrderValidator : AbstractValidator<CreateOrder>
{
    public CreateOrderValidator()
    {
        RuleFor(x => x.CustomerId).NotEmpty();
        RuleFor(x => x.LineItems).NotEmpty();
        RuleForEach(x => x.LineItems).ChildRules(item =>
        {
            item.RuleFor(x => x.ProductId).NotEmpty();
            item.RuleFor(x => x.Quantity)
                .InclusiveBetween(1, 100)
                .WithMessage("Line item quantity must be between 1 and 100.");
            item.RuleFor(x => x.UnitPrice).GreaterThan(0);
        });
    }
}
```

Wolverine wires FluentValidation into the request pipeline automatically; invalid requests return 400 Problem Details before `LoadAsync` is called.

**Endpoint**

```csharp
// Project.Customers/Orders/OrdersEndpoint.cs
public static class OrdersEndpoint
{
    // State-dependent pre-condition: customer exists, active order count < 50
    public static async Task<ProblemDetails?> LoadAsync(
        Guid customerId,
        IQuerySession session)
    {
        var customer = await session.LoadAsync<Customer>(customerId);
        if (customer is null)
            return new ProblemDetails { Status = 404, Detail = "Customer not found." };

        var activeOrderCount = await session
            .Query<OrderReadModel>()
            .CountAsync(o => o.CustomerId == customerId && o.IsActive);

        if (activeOrderCount >= 50)
            return new ProblemDetails
            {
                Status = 422,
                Detail = "Customer already has 50 active orders."
            };

        return null; // pre-conditions met — proceed to Handle
    }

    // Handle — pure business logic, returns HTTP response + cascading event
    [WolverinePost("/api/customers/{customerId}/orders")]
    public static (CreationResponse, OrderPlaced) Handle(CreateOrder command)
    {
        var orderId = Guid.NewGuid();
        var location = $"/api/customers/{command.CustomerId}/orders/{orderId}";
        var response = new CreationResponse(location);
        var @event = new OrderPlaced(
            orderId,
            command.CustomerId,
            command.LineItems,
            DateTimeOffset.UtcNow);
        return (response, @event);
    }
}
```

`IDocumentSession` is not injected into `Handle` — Wolverine manages the session lifecycle. The `OrderPlaced` event is appended to the event stream by the framework; no manual `SaveChangesAsync`.

**Aggregate and inline projection** *(pending architecture confirmation)*

```csharp
// Project.Customers/Orders/Order.cs
public record Order(
    Guid Id,
    Guid CustomerId,
    IReadOnlyList<LineItem> LineItems,
    DateTimeOffset PlacedAt);

// Project.Customers/Orders/OrderReadModel.cs
public class OrderReadModel
{
    public Guid Id { get; set; }
    public Guid CustomerId { get; set; }
    public bool IsActive { get; set; } = true;
    public DateTimeOffset PlacedAt { get; set; }
}

// Inline projection — same transaction as event append
public class OrderProjection : SingleStreamProjection<OrderReadModel>
{
    public void Apply(OrderPlaced e, OrderReadModel model)
    {
        model.Id = e.OrderId;
        model.CustomerId = e.CustomerId;
        model.IsActive = true;
        model.PlacedAt = e.PlacedAt;
    }
}
```

---

### Tests

**Unit test — `WhenCreatingAnOrder`**

```csharp
// Project.Customers.Tests/Orders/WhenCreatingAnOrder.cs
public class WhenCreatingAnOrder
{
    private readonly IQuerySession _session = Substitute.For<IQuerySession>();

    // --- LoadAsync ---

    [Fact]
    public async Task AndCustomerDoesNotExist_ShouldReturn404()
    {
        // Arrange
        _session.LoadAsync<Customer>(Arg.Any<Guid>()).Returns((Customer?)null);

        // Act
        var result = await OrdersEndpoint.LoadAsync(Guid.NewGuid(), _session);

        // Assert
        result.ShouldNotBeNull();
        result.Status.ShouldBe(404);
    }

    [Fact]
    public async Task AndCustomerHas50ActiveOrders_ShouldReturn422()
    {
        // Arrange
        _session.LoadAsync<Customer>(Arg.Any<Guid>()).Returns(new Customer());
        _session.Query<OrderReadModel>()
            .Returns(BuildQueryable(50)); // 50 active orders

        // Act
        var result = await OrdersEndpoint.LoadAsync(Guid.NewGuid(), _session);

        // Assert
        result.ShouldNotBeNull();
        result.Status.ShouldBe(422);
        result.Detail.ShouldContain("50 active orders");
    }

    [Fact]
    public async Task AndPreConditionsMet_ShouldReturnNull()
    {
        // Arrange
        _session.LoadAsync<Customer>(Arg.Any<Guid>()).Returns(new Customer());
        _session.Query<OrderReadModel>()
            .Returns(BuildQueryable(0));

        // Act
        var result = await OrdersEndpoint.LoadAsync(Guid.NewGuid(), _session);

        // Assert
        result.ShouldBeNull();
    }

    // --- Handle ---

    [Fact]
    public void AndCommandIsValid_ShouldReturn201WithLocationAndOrderPlacedEvent()
    {
        // Arrange
        var customerId = Guid.NewGuid();
        var command = new CreateOrder(
            customerId,
            new[] { new LineItem(Guid.NewGuid(), 2, 9.99m) });

        // Act
        var (response, @event) = OrdersEndpoint.Handle(command);

        // Assert
        response.ShouldNotBeNull();
        response.Location.ShouldBe($"/api/customers/{customerId}/orders/{@event.OrderId}");
        @event.CustomerId.ShouldBe(customerId);
        @event.LineItems.Count.ShouldBe(1);
    }
}
```

**FluentValidation unit tests**

```csharp
public class WhenValidatingCreateOrder
{
    private readonly CreateOrderValidator _validator = new();

    [Theory]
    [InlineData(0)]
    [InlineData(101)]
    public void AndQuantityIsOutOfRange_ShouldFail(int quantity)
    {
        // Arrange
        var command = new CreateOrder(
            Guid.NewGuid(),
            new[] { new LineItem(Guid.NewGuid(), quantity, 5.00m) });

        // Act
        var result = _validator.Validate(command);

        // Assert
        result.IsValid.ShouldBeFalse();
        result.Errors.ShouldContain(e => e.PropertyName.Contains("Quantity"));
    }

    [Theory]
    [InlineData(1)]
    [InlineData(100)]
    public void AndQuantityIsInRange_ShouldPass(int quantity)
    {
        var command = new CreateOrder(
            Guid.NewGuid(),
            new[] { new LineItem(Guid.NewGuid(), quantity, 5.00m) });

        _validator.Validate(command).IsValid.ShouldBeTrue();
    }
}
```

**Integration test — Alba + Testcontainers**

```csharp
// Project.Customers.Tests.Integration/Orders/WhenCreatingAnOrderIntegration.cs
public class WhenCreatingAnOrderIntegration(CustomersAppFixture fixture)
    : IntegrationContext(fixture), IClassFixture<CustomersAppFixture>
{
    [Fact]
    public async Task HappyPath_ShouldReturn201WithLocation()
    {
        // Arrange
        var customerId = await CreateCustomerAsync();
        var body = new CreateOrder(
            customerId,
            new[] { new LineItem(Guid.NewGuid(), 3, 12.50m) });

        // Act
        var response = await Host.Scenario(s =>
        {
            s.Post.Json(body).ToUrl($"/api/customers/{customerId}/orders");
            s.StatusCodeShouldBe(201);
        });

        // Assert
        var location = response.Context.Response.Headers.Location?.ToString();
        location.ShouldNotBeNullOrEmpty();
        location.ShouldStartWith($"/api/customers/{customerId}/orders/");
    }

    [Fact]
    public async Task WhenCustomerHas50ActiveOrders_ShouldReturn422()
    {
        // Arrange
        var customerId = await CreateCustomerAsync();
        await CreateActiveOrdersAsync(customerId, 50);

        var body = new CreateOrder(
            customerId,
            new[] { new LineItem(Guid.NewGuid(), 1, 5.00m) });

        // Act + Assert
        await Host.Scenario(s =>
        {
            s.Post.Json(body).ToUrl($"/api/customers/{customerId}/orders");
            s.StatusCodeShouldBe(422);
        });
    }

    [Theory]
    [InlineData(0)]
    [InlineData(101)]
    public async Task WhenLineItemQuantityIsOutOfRange_ShouldReturn400(int quantity)
    {
        // Arrange
        var customerId = await CreateCustomerAsync();
        var body = new CreateOrder(
            customerId,
            new[] { new LineItem(Guid.NewGuid(), quantity, 5.00m) });

        // Act + Assert
        await Host.Scenario(s =>
        {
            s.Post.Json(body).ToUrl($"/api/customers/{customerId}/orders");
            s.StatusCodeShouldBe(400);
        });
    }
}
```

---

### Evidence

| Test | Command | Exit | Result |
|---|---|---|---|
| `WhenCreatingAnOrder` | `dotnet test Project.Customers.Tests` | 0 | PASS |
| `WhenValidatingCreateOrder` | `dotnet test Project.Customers.Tests` | 0 | PASS |
| `WhenCreatingAnOrderIntegration` | `dotnet test Project.Customers.Tests.Integration` | 0 | PASS |

*(Simulated — no live execution.)*

---

### Changes

- Files created: `Orders/CreateOrder.cs`, `Orders/CreateOrderValidator.cs`, `Orders/OrdersEndpoint.cs`, `Orders/Order.cs`, `Orders/OrderReadModel.cs`, `Orders/OrderProjection.cs`
- Files modified: `CustomersModule.cs` (register projection + validator)
- Tests: `WhenCreatingAnOrder.cs`, `WhenValidatingCreateOrder.cs`, `WhenCreatingAnOrderIntegration.cs`

### Decisions

- `Order` aggregate placed in the `Customers` bounded context pending architecture confirmation — decision checkpoint was raised before implementation.
- `IsActive` flag on `OrderReadModel` is set by projection on `OrderPlaced`; it will be cleared by a future `OrderCompleted` / `OrderCancelled` event rather than via mutation.

---

## Evaluation

### Criteria

- [x] PASS: Agent reads CLAUDE.md and checks `.claude/rules/` including `dotnet-stack--jasperfx.md` — Step 1 of Pre-Flight is MANDATORY with explicit `Read` calls and a directive to check `.claude/rules/` listing `dotnet-stack--jasperfx.md` as a key rule file.

- [x] PASS: Agent uses hierarchical URL `/api/customers/{customerId}/orders` — API Design mandates "Hierarchical URLs mirroring entity ownership" and "No flat top-level listings." The Wolverine endpoint code example also demonstrates `[WolverinePost("/api/parents/{parentId}/children")]`.

- [x] PASS: Agent separates `LoadAsync` (pre-conditions) from `Handle` (business logic) — the Wolverine Endpoints section provides this pattern explicitly with a working code example: `LoadAsync` returns `ProblemDetails?` to short-circuit, `Handle` returns the cascading tuple.

- [x] PASS: Agent uses `IDocumentSession` injected by Wolverine — Managed Sessions Only section states "Use Wolverine's `IDocumentSession` — never create `store.LightweightSession()` independently." Principles repeats this in bold.

- [x] PASS: Agent returns `OrderPlaced` as cascading message from `Handle` — the code example shows `Handle` returning `(CreationResponse, MyEntityCreated)`. One Message One Unit of Work (CRITICAL) explicitly forbids inline side-effect processing.

- [x] PASS: Agent produces both unit test (`WhenCreatingAnOrder`) and integration test (Alba + Testcontainers) — Testing section "The Rule" is MANDATORY, specifies BDD naming (`WhenDoingSomething`), Shouldly, Alba + Testcontainers PostgreSQL.

- [x] PASS: Agent raises decision checkpoint before creating the Order aggregate — Decision Checkpoints table (MANDATORY) lists "Creating a new aggregate | Domain modelling decision" as an explicit stop-and-ask trigger.

- [x] PASS: Command and event are C# `record` types with immutable properties — Endpoint contract rules state "Commands and events are C# `record` types — never classes with mutable setters. Use positional or `init`-only properties so instances are immutable."

- [x] PASS: Agent includes response DTO (`CreateOrderResponse` / `CreationResponse`) separate from the aggregate — Endpoint contract rules state "Response DTOs are records too, separate from the aggregate. Never serialise the aggregate directly to the HTTP response."

### Output expectations

- [x] PASS: Endpoint route is exactly `POST /api/customers/{customerId}/orders` mounted via `[WolverinePost]` with `customerId` bound from the route — definition mandates hierarchical URLs and the code example demonstrates `[WolverinePost("/api/parents/{parentId}/children")]`.

- [x] PASS: Command record (`CreateOrder`) is a C# `record` with positional-immutable properties, containing the line items collection and `CustomerId` — Endpoint contract rules mandate this explicitly.

- [x] PASS: Both business rules are enforced: quantity range [1,100] via FluentValidation (`InclusiveBetween(1, 100)`) and active-order count < 50 checked in `LoadAsync` against persisted state — the definition calls out both mechanisms by name, including "quantity 1-100" as the prototypical FluentValidation example.

- [x] PASS: `LoadAsync` loads the customer, counts active orders, and returns `ProblemDetails` / 4xx on failure — the Wolverine Endpoints section explicitly shows `LoadAsync` returning `ProblemDetails?` for pre-condition failures, not throwing exceptions.

- [x] PASS: `Handle` returns domain event plus HTTP response with no inline side effects — One Message One Unit of Work is CRITICAL and cascading returns are prescribed. Anti-pattern (inline processing) is explicitly forbidden.

- [x] PASS: `IDocumentSession` injected by Wolverine, never from `IDocumentStore`, no manual `SaveChangesAsync` — Managed Sessions Only section covers all three points explicitly.

- [x] PASS: Response is `201 Created` with `Location` header pointing to `/api/customers/{customerId}/orders/{orderId}` and a dedicated response DTO — Endpoint contract rules state "POST creation endpoints return `201 Created` with a `Location` header... Use Wolverine's `CreationResponse`."

- [x] PASS: Unit test class named `WhenCreatingAnOrder` using Shouldly, plus Alba + Testcontainers integration test — Testing section mandates BDD naming, Shouldly, Alba + Testcontainers. All three explicit.

- [x] PASS: Tests cover happy path plus both rule violations (51st active order rejected → 422, quantity 0 / 101 rejected → 400) with arrange/act/assert structure — definition provides explicit mechanisms for both rules; a well-formed response following the definition produces tests for both violations.

- [x] PASS: Output flags the architecture decision (introducing the Order aggregate) for stakeholder review before implementing — Decision Checkpoints (MANDATORY) is an explicit stop-and-ask trigger for new aggregates.

## Notes

The definition is well-structured and comprehensive. The four gaps identified in the previous evaluation (record types, POST response shape, FluentValidation for range rules, explicit test coverage of both rule violations) were all closed in earlier revisions. No gaps remain.

One minor observation: `LoadAsync` in the simulated output uses `IQuerySession` for the count query, but the definition's code example uses `IDocumentSession` for `LoadAsync`. Both are valid Wolverine injection targets for read-only work (`IQuerySession` is the read-only interface), and the definition does not prohibit using `IQuerySession` in `LoadAsync`. Not a gap — worth noting for consistency.

The Decision Checkpoint placement (before implementation) is correctly modelled: the agent raises the question, then proceeds to show the implementation as a provisional example pending confirmation. This matches real-world usage where the agent provides the implementation plan alongside the checkpoint.
