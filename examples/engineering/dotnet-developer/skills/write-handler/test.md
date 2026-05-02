# Test: Write handler for processing crawl completion

Scenario: Developer invokes the write-handler skill for a `CompleteCrawl` command handler. When a crawl completes, it should update the crawl status, record the completion time, and fan out to trigger extraction of each crawled page independently.

## Prompt

Write a handler for `CompleteCrawl`. The crawl has a list of pages (each with an ID and URL). When completed: mark the crawl status as Completed, set CompletedAt to now, then trigger extraction for each page as an independent unit of work. Each page extraction is a separate `ExtractPage` message. Use AggregateHandler pattern with `IDocumentSession` injected.

`dotnet` is available. Create the project structure, write the handler and tests, then run `dotnet test` and paste the exact output including the exit code.

**Unit test class must be named `WhenCompletingACrawl`** with test methods following the `it_verb_noun` naming pattern. Use Shouldly for assertions.

**Include an error handling section** in your response that explains: (1) which exceptions should propagate (fatal — let Wolverine retry), and (2) which should be caught and logged (non-fatal — return null to skip cascade).

**Also write an integration test class** named `CompleteCrawlIntegrationTests` that extends `IntegrationContext` and uses `Host.TrackActivity().IncludeExternalTransports().InvokeMessageAndWaitAsync(new CompleteCrawl(...))` to verify the crawl status and cascaded messages. The stubs provided compile without Wolverine NuGet packages.

Set up the project as follows:

```bash
# Create solution
dotnet new sln -n TurtleStack
mkdir -p src tests

# Class library for handler code
dotnet new classlib -n TurtleStack.Handlers -o src/TurtleStack.Handlers
dotnet sln add src/TurtleStack.Handlers/TurtleStack.Handlers.csproj

# Test project
dotnet new xunit -n TurtleStack.Handlers.Tests -o tests/TurtleStack.Handlers.Tests
dotnet add tests/TurtleStack.Handlers.Tests/TurtleStack.Handlers.Tests.csproj package Shouldly
dotnet add tests/TurtleStack.Handlers.Tests/TurtleStack.Handlers.Tests.csproj reference src/TurtleStack.Handlers/TurtleStack.Handlers.csproj
dotnet sln add tests/TurtleStack.Handlers.Tests/TurtleStack.Handlers.Tests.csproj
```

Write these stub types into `src/TurtleStack.Handlers/Stubs.cs` — they replace Wolverine and Marten so the project compiles without those NuGet packages:

```csharp
// src/TurtleStack.Handlers/Stubs.cs
namespace Wolverine;

[AttributeUsage(AttributeTargets.Class | AttributeTargets.Method)]
public sealed class AggregateHandlerAttribute : Attribute { }

public interface IDocumentSession
{
    T? Load<T>(Guid id) where T : class;
    void Store<T>(T entity) where T : class;
    Task SaveChangesAsync(CancellationToken ct = default);
    EventOperations Events { get; }
}

public class EventOperations
{
    public void Append(Guid streamId, params object[] events) { }
    public Task<T?> AggregateStreamAsync<T>(Guid streamId, CancellationToken ct = default)
        where T : class => Task.FromResult<T?>(null);
}

public interface IQuerySession
{
    IQueryable<T> Query<T>();
}

namespace Wolverine.Tracking;

public class TrackedSession
{
    public SentMessages Sent { get; } = new();
}

public class SentMessages
{
    private readonly List<object> _messages = new();
    public void Add<T>(T msg) where T : notnull => _messages.Add(msg);
    public IEnumerable<T> MessagesOf<T>() => _messages.OfType<T>();
}

public class TrackedActivityOptions
{
    public TrackedActivityOptions IncludeExternalTransports() => this;
    public Task<TrackedSession> InvokeMessageAndWaitAsync<T>(T message)
        => Task.FromResult(new TrackedSession());
}

namespace Microsoft.Extensions.Hosting;

public interface IHost { }

public static class HostTrackingExtensions
{
    public static Wolverine.Tracking.TrackedActivityOptions TrackActivity(this IHost host)
        => new();
}

namespace TurtleStack.Handlers.Tests;

public abstract class IntegrationContext
{
    protected IHost Host => null!;
    protected IDocumentSession Session => null!;
}
```

The codebase has the following existing code for context:

```csharp
// Domain/Crawl.cs
public class Crawl
{
    public Guid Id { get; set; }
    public Guid SourceId { get; set; }
    public string Status { get; set; } = "Running";
    public DateTimeOffset CreatedAt { get; set; }
    public DateTimeOffset? CompletedAt { get; set; }
    public List<CrawlPage> Pages { get; set; } = new();

    public void Apply(CrawlCompleted e)
    {
        Status = "Completed";
        CompletedAt = e.CompletedAt;
    }
}

// Domain/CrawlPage.cs
public record CrawlPage(Guid Id, string Url);

// Handlers/StartCrawlHandler.cs — existing handler to match conventions
// NOTE: fan-out handlers return a TUPLE (event, IEnumerable<CascadeMessage>) — never a wrapper record
[AggregateHandler]
public static class StartCrawlHandler
{
    public static (CrawlStarted, IEnumerable<QueuePageIndex>) Handle(
        StartCrawl command,
        Crawl? crawl,
        IDocumentSession session)
    {
        var started = new CrawlStarted(command.CrawlId, command.SourceId, command.Pages);
        var indexJobs = command.Pages.Select(p => new QueuePageIndex(command.CrawlId, p.Id));
        return (started, indexJobs);
    }
}

public record StartCrawl(Guid CrawlId, Guid SourceId, List<CrawlPage> Pages);
public record CrawlStarted(Guid CrawlId, Guid SourceId, List<CrawlPage> Pages);
public record QueuePageIndex(Guid CrawlId, Guid PageId);

// Tests/WhenStartingACrawl.cs — existing tests to match naming convention
public class WhenStartingACrawl
{
    [Fact]
    public void it_emits_crawl_started_and_one_index_job_per_page()
    {
        var pages = new List<CrawlPage> { new(Guid.NewGuid(), "https://example.com") };
        var command = new StartCrawl(Guid.NewGuid(), Guid.NewGuid(), pages);

        // Destructure the tuple return — never wrap in a result record
        var (started, indexJobs) = StartCrawlHandler.Handle(command, null, null!);

        started.CrawlId.ShouldBe(command.CrawlId);
        indexJobs.Count().ShouldBe(1);
    }
}
```

## Criteria

- [ ] PASS: Skill performs reconnaissance — reads existing handlers and matches `[AggregateHandler]` usage, return type conventions, and test naming patterns
- [ ] PASS: Handler fans out with `IEnumerable<ExtractPage>` return — does not loop through pages inline in a single handler
- [ ] PASS: Handler uses managed `IDocumentSession` injected as a method parameter — does not create sessions from `IDocumentStore`
- [ ] PASS: Skill does not call `SaveChangesAsync` manually — notes Wolverine manages the session lifecycle
- [ ] PASS: `CompleteCrawl` command record has an `Id` property (or `CrawlId`) to enable automatic aggregate loading
- [ ] PASS: Unit test class is named `WhenCompletingACrawl` and uses Shouldly assertions
- [ ] PASS: Integration test uses `Host.InvokeMessageAndWaitAsync` and verifies the crawl status after processing
- [ ] PARTIAL: Skill includes error handling guidance — distinguishes fatal errors (let propagate for Wolverine retry) from non-fatal errors (catch, log, return null)
- [ ] PASS: Output delivers handler class, command/event records, unit test, integration test, and evidence of tests passing

## Output expectations

- [ ] PASS: Output's handler is decorated with `[AggregateHandler]` (or matches the established convention) and operates on the Crawl aggregate, with the `CompleteCrawl` command and `Crawl` aggregate both as parameters
- [ ] PASS: Output's `CompleteCrawl` command record has an `Id` (or `CrawlId`) property — without it, automatic aggregate loading by ID won't work
- [ ] PASS: Output's command and emitted events (`CrawlCompleted`, `ExtractPage`) are C# `record` types with immutable properties, not classes
- [ ] PASS: Output emits a `CrawlCompleted` event recording the new status and `CompletedAt` timestamp via the aggregate (event sourcing) — not by mutating fields directly
- [ ] PASS: Output's handler returns `IEnumerable<ExtractPage>` (or yields one per page) so each page extraction is a separate Wolverine message processed in its own transaction — NOT looped inline
- [ ] PASS: Output's handler accepts `IDocumentSession` as a method parameter where persistence is needed and never instantiates a session from `IDocumentStore`, and never calls `SaveChangesAsync` manually
- [ ] PASS: Output's unit test class is named `WhenCompletingACrawl` and uses Shouldly assertions, asserting on the resulting events (not on persisted state in unit tests)
- [ ] PASS: Output's integration test uses `Host.InvokeMessageAndWaitAsync(new CompleteCrawl(...))` and verifies, after waiting, that the crawl status is `Completed` and that one `ExtractPage` message per page was published
- [ ] PASS: Output includes evidence of the tests running and passing (command + exit code or test output snippet)
- [ ] PARTIAL: Output's error handling guidance distinguishes fatal errors (let propagate so Wolverine retries) from non-fatal/expected errors (catch and short-circuit) — explicit policy, not silent try/catch
