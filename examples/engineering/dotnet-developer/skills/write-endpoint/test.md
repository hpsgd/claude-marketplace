# Test: Write GET endpoint for listing crawls under a source

Scenario: Developer invokes the write-endpoint skill for a `GET /api/sources/{sourceId}/crawls` endpoint that returns a paginated, sortable, filterable list of crawls belonging to a source.

## Prompt

Write a GET endpoint for `GET /api/sources/{sourceId}/crawls`. It should return a paginated list of crawls for a given source. Support: `page` (default 1), `size` (default 25, max 100), `sort` (name or createdAt, default createdAt), `dir` (asc or desc, default desc), and `q` for text search on crawl name. Return 404 if the source doesn't exist.

**Important:** The source existence check must go in `LoadAsync` (returns `ProblemDetails` 404), not in `Handle`. `Handle` is for pure business logic — no database access. See the LoadAsync pattern in the context below.

`dotnet` is available. Create the project structure, write the endpoint and tests, then run `dotnet test` and show the output. Set up the project as follows:

```bash
# Create solution
dotnet new sln -n TurtleStack
mkdir -p src tests

# Class library for endpoint code
dotnet new classlib -n TurtleStack.Endpoints -o src/TurtleStack.Endpoints
dotnet sln add src/TurtleStack.Endpoints/TurtleStack.Endpoints.csproj

# Test project
dotnet new xunit -n TurtleStack.Endpoints.Tests -o tests/TurtleStack.Endpoints.Tests
dotnet add tests/TurtleStack.Endpoints.Tests/TurtleStack.Endpoints.Tests.csproj package Shouldly
dotnet add tests/TurtleStack.Endpoints.Tests/TurtleStack.Endpoints.Tests.csproj reference src/TurtleStack.Endpoints/TurtleStack.Endpoints.csproj
dotnet sln add tests/TurtleStack.Endpoints.Tests/TurtleStack.Endpoints.Tests.csproj
```

Write these stub types into `src/TurtleStack.Endpoints/Stubs.cs` — they replace Wolverine.HTTP and Marten so the project compiles without those NuGet packages:

```csharp
// src/TurtleStack.Endpoints/Stubs.cs
namespace Wolverine.Http;

[AttributeUsage(AttributeTargets.Method)]
public sealed class WolverineGetAttribute(string route) : Attribute { }

[AttributeUsage(AttributeTargets.Parameter)]
public sealed class AsParametersAttribute : Attribute { }

namespace Microsoft.AspNetCore.Http;

public class ProblemDetails
{
    public int? Status { get; set; }
    public string? Title { get; set; }
    public string? Detail { get; set; }
    public string? Instance { get; set; }
}

public class HttpContext
{
    public HttpRequest Request { get; } = new();
}

public class HttpRequest
{
    public string Path { get; set; } = string.Empty;
}

namespace TurtleStack.Endpoints;

public interface IQuerySession
{
    IQueryable<T> Query<T>();
}

public static class QueryableExtensions
{
    public static Task<bool> AnyAsync<T>(this IQueryable<T> q,
        System.Linq.Expressions.Expression<Func<T, bool>> pred,
        CancellationToken ct = default)
        => Task.FromResult(q.Any(pred.Compile()));

    public static Task<int> CountAsync<T>(this IQueryable<T> q, CancellationToken ct = default)
        => Task.FromResult(q.Count());

    public static Task<List<T>> ToListAsync<T>(this IQueryable<T> q, CancellationToken ct = default)
        => Task.FromResult(q.ToList());
}

public static class StringQueryExtensions
{
    // Stub for Marten's MatchesSql — in tests becomes case-insensitive Contains
    public static bool MatchesSql(this string value, string pattern, string term)
        => value.Contains(term, StringComparison.OrdinalIgnoreCase);
}
```

The codebase has the following existing code for context:

```csharp
// Aggregates/Source.cs
public class Source
{
    public Guid Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Url { get; set; } = string.Empty;
    public DateTimeOffset CreatedAt { get; set; }
    public DateTimeOffset? LastUpdatedAt { get; set; }
}

// Aggregates/Crawl.cs
public class Crawl
{
    public Guid Id { get; set; }
    public Guid SourceId { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Status { get; set; } = "pending";
    public DateTimeOffset CreatedAt { get; set; }
    public DateTimeOffset? LastUpdatedAt { get; set; }

    public CrawlResponse ToResponse() =>
        new(Id, SourceId, Name, Status, CreatedAt, LastUpdatedAt);
}

// Endpoints/Sources/ListSourcesEndpoint.cs
public static class ListSourcesEndpoint
{
    private const int MaxPageSize = 100;
    private static readonly HashSet<string> AllowedSortFields =
        new(StringComparer.OrdinalIgnoreCase) { "name", "createdAt" };
    private static readonly HashSet<string> AllowedDirections =
        new(StringComparer.OrdinalIgnoreCase) { "asc", "desc" };

    public record ListSourcesRequest(
        int Page = 1,
        int Size = 25,
        string? Sort = "createdAt",
        string? Dir = "desc",
        string? Q = null);

    public static ProblemDetails? LoadAsync(
        [AsParameters] ListSourcesRequest request,
        HttpContext http)
    {
        if (request.Sort is not null && !AllowedSortFields.Contains(request.Sort))
            return new ProblemDetails
            {
                Status = 400,
                Title = "Invalid sort field",
                Detail = $"sort must be one of: {string.Join(", ", AllowedSortFields)}.",
                Instance = http.Request.Path
            };

        if (request.Dir is not null && !AllowedDirections.Contains(request.Dir))
            return new ProblemDetails
            {
                Status = 400,
                Title = "Invalid sort direction",
                Detail = "dir must be 'asc' or 'desc'.",
                Instance = http.Request.Path
            };

        return null;
    }

    [WolverineGet("/api/sources")]
    public static async Task<PagedResult<SourceResponse>> Handle(
        [AsParameters] ListSourcesRequest request,
        IQuerySession session,
        CancellationToken ct)
    {
        var size = Math.Min(request.Size, MaxPageSize);
        var query = session.Query<Source>();

        if (!string.IsNullOrWhiteSpace(request.Q))
            query = query.Where(s => s.Name.MatchesSql("%?%", request.Q));

        query = request.Sort?.ToLowerInvariant() switch
        {
            "name" => request.Dir == "asc"
                ? query.OrderBy(s => s.Name)
                : query.OrderByDescending(s => s.Name),
            _ => request.Dir == "asc"
                ? query.OrderBy(s => s.CreatedAt)
                : query.OrderByDescending(s => s.CreatedAt)
        };

        var totalItems = await query.CountAsync(ct);
        var items = await query
            .Skip((request.Page - 1) * size)
            .Take(size)
            .ToListAsync(ct);

        return new PagedResult<SourceResponse>(
            items.Select(s => s.ToResponse()).ToList(),
            request.Page, size, totalItems);
    }
}

// Common/PagedResult.cs
public record PagedResult<T>(
    IReadOnlyList<T> Items,
    int Page,
    int Size,
    int TotalItems)
{
    public int TotalPages => (int)Math.Ceiling((double)TotalItems / Size);
}
```

## Criteria

- [ ] PASS: Skill performs reconnaissance — reads existing endpoints and identifies the URL pattern, naming conventions, and `PagedResult<T>` return type in use
- [ ] PASS: Endpoint uses `IQuerySession` (read-only) — not `IDocumentSession` (read-write) for a GET query
- [ ] PASS: Pagination, sorting, and filtering are performed in the database query — not by loading all records and filtering in memory
- [ ] PASS: Sort field is validated against an allowlist (name, createdAt) — not passed directly to the ORM (SQL injection vector)
- [ ] PASS: `size` parameter is capped at 100 server-side — not trusted from the client
- [ ] PASS: Source existence check is in LoadAsync returning ProblemDetails 404 — not in Handle
- [ ] PASS: Skill produces a unit test and an integration test — both with evidence (command + exit code)
- [ ] PARTIAL: Response DTO is separate from the aggregate — `CrawlResponse` not a direct `Crawl` return
- [ ] PASS: Anti-patterns section confirms no in-memory pagination, no flat URL, no direct aggregate exposure

## Output expectations

- [ ] PASS: Output's route is exactly `GET /api/sources/{sourceId}/crawls`, hierarchical, not a flat top-level `/api/crawls?sourceId=...`
- [ ] PASS: Output binds query parameters with their stated defaults — `page=1`, `size=25`, `sort=createdAt`, `dir=desc` — and rejects `size > 100` server-side rather than trusting the client
- [ ] PASS: Output validates `sort` against an explicit allowlist of `["name", "createdAt"]` and `dir` against `["asc", "desc"]`, returning a 400 Problem Details on invalid values rather than passing through to the ORM
- [ ] PASS: Output uses `IQuerySession` (read-only) — not `IDocumentSession` — for this GET, given the read-only semantics
- [ ] PASS: Output applies pagination, sorting, and filtering at the database query level (via `IQueryable` with `Skip`/`Take` or Marten's paging), not by materialising all crawls in memory and filtering client-side
- [ ] PASS: Output's source-existence check happens in `LoadAsync` and returns ProblemDetails 404 with `instance` set to the request path — not by throwing in `Handle`
- [ ] PASS: Output's response uses a `PagedResult<T>` (or equivalent) shape with `items`, `page`, `size`, `totalItems`, `totalPages` — not a bare array
- [ ] PASS: Output's response items are a `CrawlResponse` DTO (or similar) — not the raw `Crawl` aggregate, preventing internal field exposure
- [ ] PASS: Output includes both a unit test (with `When...` naming + Shouldly) and an integration test (Alba + Testcontainers), each with command and exit code shown as evidence of passing
- [ ] PARTIAL: Output's `q` text-search filter is implemented case-insensitively and against a documented set of fields (likely `name`), with the search semantics explicit (substring vs full-text)
