---
name: write-handler
description: Write a Wolverine command handler with aggregate loading and cascading messages.
argument-hint: "[handler description, e.g. 'TriggerCrawlExtraction']"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
paths:
  - "**/*.cs"
---

Write a Wolverine handler for $ARGUMENTS.

## Process (sequential — do not skip steps)

### Step 1: Reconnaissance

Before writing the handler:

1. **Read existing handlers** — match the project's patterns:
   ```bash
   grep -rn "AggregateHandler\|public static.*Handle(" --include="*.cs" | head -20
   ```

2. **Identify the aggregate** — which Marten aggregate does this handler operate on?
3. **Identify the message** — what command triggers this handler?
4. **Identify the side effects** — what downstream messages should cascade?
5. **Check for existing messages** — reuse existing command/event types where appropriate

### Step 2: Handler Architecture Decision

Choose the correct handler pattern based on what the handler does:

| Pattern | When to use | Aggregate loading |
|---|---|---|
| `[AggregateHandler]` with aggregate parameter | Handler operates on a Marten event-sourced aggregate | Automatic — Wolverine loads by convention |
| Static handler with `IDocumentSession` | Handler operates on document store data | Manual — load in handler |
| Static handler with external service | Handler calls external APIs or infrastructure | No aggregate — orchestration only |
| Handler returning cascading messages | Handler triggers downstream work | Any of the above + return type |

### Step 3: AggregateHandler Pattern (Primary)

Event-sourced aggregates evolve their state by **emitting events, not mutating fields**. Return the event(s) from `Handle` — Marten appends them to the aggregate stream and `Apply` methods on the aggregate fold them into state.

```csharp
[AggregateHandler]
public static class CompleteCrawlHandler
{
    public static (CrawlCompleted, IEnumerable<ExtractPage>) Handle(
        CompleteCrawl command,
        Crawl crawl)
    {
        // Emit the domain event — Marten appends it to the stream.
        // Do NOT mutate crawl.Status / crawl.CompletedAt directly.
        var completed = new CrawlCompleted(crawl.Id, DateTimeOffset.UtcNow);

        // Fan out — one ExtractPage per page, each its own unit of work
        var extractions = crawl.Pages.Select(p => new ExtractPage(crawl.Id, p.Id, p.Url));

        return (completed, extractions);
    }
}
```

**Event-sourced state changes:**
- Return the event from `Handle` — Wolverine + Marten append it to the stream automatically. The aggregate's `Apply(CrawlCompleted)` method updates state on rehydration
- Never mutate aggregate fields directly (`crawl.Status = ...`) — the change won't be persisted as an event and is invisible on replay
- For non-event-sourced document aggregates, use `session.Store(crawl)` after explicit field changes — but this is the document path, not the event-sourced path
- If you need to append events from inside a non-aggregate handler, use `session.Events.Append(streamId, @event)` and let `IDocumentSession` flush

**`[AggregateHandler]` rules:**
- Wolverine automatically loads the aggregate from Marten using the command's `Id` property (or `{AggregateName}Id`)
- The aggregate is injected as a method parameter — you don't load it yourself
- The command MUST have an `Id` property (or a property named `{AggregateName}Id`) that maps to the aggregate identity
- If the aggregate doesn't exist, Wolverine returns a 404 (for HTTP) or skips (for messages)
- **Commands and events are C# `record` types** with immutable properties — never classes with setters

### Step 4: Cascading Returns

Cascading returns are how handlers trigger downstream work. The return value of `Handle` is automatically published as a message.

```csharp
// Single cascade — return one event (Marten appends it to the stream)
public static CrawlCompleted Handle(CompleteCrawl command, Crawl crawl)
{
    return new CrawlCompleted(crawl.Id, DateTimeOffset.UtcNow);
}

// Multiple cascades — return a tuple of event + message
public static (CrawlCompleted, NotifySourceOwner) Handle(CompleteCrawl command, Crawl crawl)
{
    return (
        new CrawlCompleted(crawl.Id, DateTimeOffset.UtcNow),
        new NotifySourceOwner(crawl.SourceId, $"Crawl {crawl.Id} completed")
    );
}

// Polymorphic cascade — return object? for branching
public static object? Handle(ProcessCrawlResult command, Crawl crawl)
{
    return command.Success
        ? new CrawlCompleted(crawl.Id)
        : new CrawlFailed(crawl.Id, command.Error);
}

// No cascade — return void or null
public static void Handle(LogCrawlMetrics command, ILogger logger)
{
    logger.LogInformation("Crawl {CrawlId} processed {Pages} pages", command.CrawlId, command.PageCount);
    // No return — fire and forget
}

// Fan-out — return IEnumerable for N cascading messages
public static IEnumerable<ExtractPage> Handle(
    ExtractCrawlPages command,
    Crawl crawl)
{
    // ONE message per page — not one handler processing N pages inline
    return command.PageIds.Select(pageId => new ExtractPage(crawl.Id, pageId));
}
```

**Cascading rules:**
- Return type determines cascade: single message, tuple, `object?`, `IEnumerable<T>`, or `void`
- **One message, one unit of work** — never loop through N items inline. Fan out with `IEnumerable<T>` and let each item process independently
- Cascading messages are published to the same bus — they can be handled by any subscriber
- Return `null` (with `object?` return type) to skip cascade — no downstream work needed
- Cascading is transactional — if the handler fails, the cascade is not published

### Step 5: One Message, One Unit of Work (IRON LAW)

This is the most important rule in Wolverine handler design.

```csharp
// WRONG — processing N items inline
public static async Task Handle(ProcessAllPages command, IDocumentSession session)
{
    var pages = await session.Query<Page>()
        .Where(p => p.CrawlId == command.CrawlId)
        .ToListAsync();

    foreach (var page in pages)  // BAD: if page 47 fails, pages 1-46 are lost
    {
        await ExtractContent(page);
        session.Store(page);
    }
}

// CORRECT — fan out to individual handlers
public static IEnumerable<ExtractPage> Handle(
    ExtractCrawlPages command,
    Crawl crawl)
{
    return crawl.Pages.Select(p => new ExtractPage(crawl.Id, p.Id));
}

// Each page is an independent unit of work
[AggregateHandler]
public static class ExtractPageHandler
{
    public static PageExtracted Handle(ExtractPage command, Page page)
    {
        page.Content = ExtractContent(page.Html);
        return new PageExtracted(page.Id);
    }
}
```

**Why:**
- Individual failures don't block the batch — page 47 failing doesn't affect pages 1-46
- Wolverine handles retries per message — each unit of work can be retried independently
- Parallelism — Wolverine can process fan-out messages concurrently
- Observability — each message has its own trace, timing, and error reporting

### Step 6: Session Management

```csharp
// CORRECT — managed session via dependency injection
public static async Task Handle(
    MyCommand command,
    IDocumentSession session,  // Wolverine manages the session lifecycle
    CancellationToken ct)
{
    var entity = await session.LoadAsync<MyEntity>(command.Id, ct);
    entity.Update(command);
    session.Store(entity);
    // Wolverine calls SaveChangesAsync automatically
}

// WRONG — creating your own session
public static async Task Handle(
    MyCommand command,
    IDocumentStore store)  // BAD: manual session management
{
    await using var session = store.LightweightSession();  // NOT managed by Wolverine
    // ...
    await session.SaveChangesAsync();  // Manual save — bypasses Wolverine's unit of work
}
```

**Session rules:**
- Always inject `IDocumentSession` — never create sessions from `IDocumentStore`
- Wolverine manages the session lifecycle and calls `SaveChangesAsync` after Handle succeeds
- Use `IQuerySession` (read-only) if the handler only reads data
- Do not call `SaveChangesAsync` manually — Wolverine does it. Calling it yourself causes double-save
- The session is scoped to the message — one message, one session, one transaction

### Step 7: Error Handling

```csharp
// Non-fatal errors: catch, log, continue pipeline
public static object? Handle(
    ProcessExternalData command,
    ILogger logger)
{
    try
    {
        var result = ParseExternalPayload(command.Payload);
        return new DataProcessed(result);
    }
    catch (FormatException ex)
    {
        // Non-fatal: log and skip. Don't crash the pipeline
        logger.LogWarning(ex, "Failed to parse payload for {CommandId}", command.Id);
        return null; // No cascade — this item is skipped
    }
}

// Fatal errors: let them propagate — Wolverine handles retry/dead-letter
public static CrawlCompleted Handle(CompleteCrawl command, Crawl crawl)
{
    // No try/catch — if this throws, Wolverine retries per policy
    crawl.Complete();
    return new CrawlCompleted(crawl.Id);
}
```

**Error handling rules:**
- **Fatal errors** (database unavailable, aggregate missing): let the exception propagate. Wolverine retries according to the configured retry policy and eventually dead-letters
- **Non-fatal errors** (bad external data, expected validation failures): catch, log, return null (skip cascade)
- **Never swallow exceptions silently** — always log with context (command ID, aggregate ID)
- Configure retry policies per message type, not per handler
- Dead letter queue for messages that fail all retries — monitor and investigate

### Step 8: Dependency Injection

```csharp
// External dependencies: constructor injection on the handler class
public class NotifyExternalServiceHandler
{
    private readonly IHttpClientFactory _httpClientFactory;
    private readonly ILogger<NotifyExternalServiceHandler> _logger;

    public NotifyExternalServiceHandler(
        IHttpClientFactory httpClientFactory,
        ILogger<NotifyExternalServiceHandler> logger)
    {
        _httpClientFactory = httpClientFactory;
        _logger = logger;
    }

    public async Task<object?> Handle(
        NotifyExternalService command,
        CancellationToken ct)
    {
        var client = _httpClientFactory.CreateClient("external");
        var response = await client.PostAsJsonAsync("/webhook", command, ct);

        return response.IsSuccessStatusCode
            ? new ExternalServiceNotified(command.Id)
            : null; // Will be retried by Wolverine
    }
}
```

**Rules:**
- Use constructor injection for external services (HTTP clients, loggers, configuration)
- Static handlers cannot use constructor injection — they receive dependencies as method parameters
- `[AggregateHandler]` handlers are typically static — inject `IDocumentSession` as a method parameter
- Use `IHttpClientFactory` for HTTP clients — never `new HttpClient()`

### Step 9: Testing (MANDATORY)

#### Unit Test

For event-sourced handlers, assert on the **events returned** by `Handle` (the cascade) — not on persisted state. Persistence is Marten's job and belongs in integration tests.

```csharp
public class WhenCompletingACrawl
{
    [Fact]
    public void it_emits_crawl_completed_and_one_extract_per_page()
    {
        // Arrange
        var crawl = CrawlFactory.Create(pageCount: 3);
        var command = new CompleteCrawl(crawl.Id);

        // Act
        var (completed, extractions) = CompleteCrawlHandler.Handle(command, crawl);

        // Assert — on the events, not on mutated state
        completed.ShouldBeOfType<CrawlCompleted>();
        completed.CrawlId.ShouldBe(crawl.Id);
        completed.CompletedAt.ShouldBeGreaterThan(DateTimeOffset.MinValue);

        var pages = extractions.ToList();
        pages.Count.ShouldBe(3);
        pages.ShouldAllBe(p => p.CrawlId == crawl.Id);
    }
}
```

#### Integration Test

Verify both the resulting aggregate state **and** the cascading messages published to the bus. Use Wolverine's `TrackedSession` (via `Host.TrackActivity().InvokeMessageAndWaitAsync(...)`) to capture published messages.

```csharp
public class CompleteCrawlIntegrationTest : IntegrationContext
{
    [Fact]
    public async Task it_completes_the_crawl_and_publishes_one_extract_per_page()
    {
        // Arrange — seed the aggregate via its event stream
        var crawlId = Guid.NewGuid();
        await using var session = Store.LightweightSession();
        session.Events.StartStream<Crawl>(crawlId, new CrawlStarted(crawlId, pages: 3));
        await session.SaveChangesAsync();

        // Act — track the session so we can assert on cascading messages
        var tracked = await Host
            .TrackActivity()
            .IncludeExternalTransports()
            .InvokeMessageAndWaitAsync(new CompleteCrawl(crawlId));

        // Assert — aggregate state
        var crawl = await session.Events.AggregateStreamAsync<Crawl>(crawlId);
        crawl!.Status.ShouldBe(CrawlStatus.Completed);
        crawl.CompletedAt.ShouldNotBeNull();

        // Assert — one ExtractPage per page was published
        var extracts = tracked.Sent.MessagesOf<ExtractPage>().ToList();
        extracts.Count.ShouldBe(3);
        extracts.ShouldAllBe(e => e.CrawlId == crawlId);
    }
}
```

## Anti-Patterns (NEVER do these)

- **Inline loops** — processing N items in one handler. Fan out with `IEnumerable<T>` instead
- **Manual sessions** — `store.LightweightSession()` bypasses Wolverine's unit of work
- **Manual SaveChangesAsync** — Wolverine calls it. Calling it yourself causes double-save
- **Catching fatal errors** — let Wolverine retry. Catching `DbException` and logging it defeats the retry pipeline
- **Missing aggregate ID on command** — `[AggregateHandler]` can't load without an `Id` property matching the aggregate
- **Business logic in LoadAsync** — LoadAsync is for pre-conditions. Business decisions go in Handle
- **God handlers** — one handler doing 5 things. Each handler does one thing and cascades the next
- **Mutating event-sourced aggregates directly** — `crawl.Status = ...` on an event-sourced aggregate is silently lost. Return events from `Handle` and let `Apply` methods fold state
- **Classes for commands/events** — commands and events are immutable `record` types, not classes with setters

## Output

Deliver:
1. Handler class with appropriate pattern (AggregateHandler, static, or instance)
2. Command and event records
3. Unit test with NSubstitute mocks
4. Integration test via Alba or message invocation
5. Evidence that tests pass (command + exit code)

## Related Skills

- `/dotnet-developer:write-endpoint` — handlers are invoked by endpoints. If the handler needs a new HTTP entry point, create the endpoint first.
