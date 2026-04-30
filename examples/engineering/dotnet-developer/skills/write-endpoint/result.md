# Result: Write GET endpoint for listing crawls under a source

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 18.5 / 19 criteria met (97%) |
| **Evaluated** | 2026-04-30 |
| **Skill source** | `plugins/engineering/dotnet-developer/skills/write-endpoint/SKILL.md` |

## Output

Simulated output the skill produces for: _Write a GET endpoint for `GET /api/sources/{sourceId}/crawls`._

---

### Reconnaissance findings

```
$ find . -name "*.cs" -path "*/Endpoints/*" | head -20
./src/Sources/Endpoints/ListSourcesEndpoint.cs
./src/Sources/Endpoints/GetSourceEndpoint.cs
./src/Sources/Endpoints/CreateSourceEndpoint.cs
./src/Crawls/Endpoints/GetCrawlEndpoint.cs

$ grep -rn "WolverineGet\|WolverinePost" --include="*.cs" | head -10
ListSourcesEndpoint.cs:  [WolverineGet("/api/sources")]
GetSourceEndpoint.cs:    [WolverineGet("/api/sources/{sourceId}")]
CreateSourceEndpoint.cs: [WolverinePost("/api/sources")]
GetCrawlEndpoint.cs:     [WolverineGet("/api/sources/{sourceId}/crawls/{crawlId}")]
```

- Parent route pattern confirmed: `/api/sources/{sourceId}/crawls` (follows existing hierarchy)
- `PagedResult<T>` already used by `ListSourcesEndpoint` — will reuse
- `IQuerySession` used consistently in GET endpoints; `IDocumentSession` only in POST/PATCH
- `CrawlResponse` record exists in `./src/Crawls/Crawl.cs` via `ToResponse()` extension
- Naming convention: `WhenListing...` for unit tests, `List...IntegrationTest` for integration

---

### Task definition

| Property | Value |
|---|---|
| Route | `GET /api/sources/{sourceId}/crawls` |
| Query params | `page` (int, default 1), `size` (int, default 25, max 100), `sort` (string, default `createdAt`), `dir` (string, default `desc`), `q` (string?, optional) |
| Sort allowlist | `name`, `createdAt` |
| Dir allowlist | `asc`, `desc` |
| Response shape | `PagedResult<CrawlResponse>` |
| Source missing | 404 ProblemDetails |
| Invalid sort/dir | 400 ProblemDetails |

---

### `ListSourceCrawlsEndpoint.cs`

```csharp
using JasperFx.Core.Id;
using Marten;
using Microsoft.AspNetCore.Mvc;
using Wolverine.Http;

namespace Crawls.Endpoints;

public static class ListSourceCrawlsEndpoint
{
    private const int MaxPageSize = 100;

    private static readonly HashSet<string> AllowedSortFields =
        new(StringComparer.OrdinalIgnoreCase) { "name", "createdAt" };

    private static readonly HashSet<string> AllowedDirections =
        new(StringComparer.OrdinalIgnoreCase) { "asc", "desc" };

    public record ListCrawlsRequest(
        Guid SourceId,
        int Page = 1,
        int Size = 25,
        string? Sort = "createdAt",
        string? Dir = "desc",
        string? Q = null);

    // Pre-condition: validate sort/dir against allowlists, confirm parent source exists.
    // Returns ProblemDetails to short-circuit; null proceeds to Handle.
    public static async Task<ProblemDetails?> LoadAsync(
        [AsParameters] ListCrawlsRequest request,
        HttpContext http,
        IQuerySession session,
        CancellationToken ct)
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

        var sourceExists = await session.Query<Source>()
            .AnyAsync(s => s.Id == request.SourceId, ct);

        if (!sourceExists)
            return new ProblemDetails
            {
                Status = 404,
                Title = "Source not found",
                Detail = $"No source with id '{request.SourceId}'.",
                Instance = http.Request.Path
            };

        return null;
    }

    [WolverineGet("/api/sources/{sourceId}/crawls")]
    public static async Task<PagedResult<CrawlResponse>> Handle(
        [AsParameters] ListCrawlsRequest request,
        IQuerySession session,
        CancellationToken ct)
    {
        var size = Math.Min(request.Size, MaxPageSize); // server-side cap

        var query = session.Query<Crawl>()
            .Where(c => c.SourceId == request.SourceId);

        if (!string.IsNullOrWhiteSpace(request.Q))
        {
            // Case-insensitive substring search on Name (Marten ILIKE via MatchesSql).
            query = query.Where(c => c.Name.MatchesSql("%?%", request.Q));
        }

        query = request.Sort?.ToLowerInvariant() switch
        {
            "name" => request.Dir == "asc"
                ? query.OrderBy(c => c.Name)
                : query.OrderByDescending(c => c.Name),
            _ => request.Dir == "asc"
                ? query.OrderBy(c => c.CreatedAt)
                : query.OrderByDescending(c => c.CreatedAt)
        };

        var totalItems = await query.CountAsync(ct);
        var items = await query
            .Skip((request.Page - 1) * size)
            .Take(size)
            .ToListAsync(ct);

        return new PagedResult<CrawlResponse>(
            items.Select(c => c.ToResponse()).ToList(),
            request.Page,
            size,
            totalItems);
    }
}
```

---

### Supporting records

```csharp
// Response DTO — never expose the Crawl aggregate directly
public record CrawlResponse(
    Guid Id,
    Guid SourceId,
    string Name,
    string Status,
    DateTimeOffset CreatedAt,
    DateTimeOffset? LastUpdatedAt);

public static class CrawlExtensions
{
    public static CrawlResponse ToResponse(this Crawl c) =>
        new(c.Id, c.SourceId, c.Name, c.Status, c.CreatedAt, c.LastUpdatedAt);
}

// Shared paged result wrapper — totalPages derived from totalItems / size
public record PagedResult<T>(
    IReadOnlyList<T> Items,
    int Page,
    int Size,
    int TotalItems)
{
    public int TotalPages => Size > 0 ? (int)Math.Ceiling((double)TotalItems / Size) : 0;
}
```

---

### Unit test — `WhenListingCrawlsForASource.cs`

```csharp
using Shouldly;

namespace Crawls.Tests.Unit;

public class WhenListingCrawlsForASource
{
    private readonly IQuerySession _session = Substitute.For<IQuerySession>();
    private readonly HttpContext _http = new DefaultHttpContext();

    [Fact]
    public async Task it_returns_paged_results_in_default_createdAt_desc_order()
    {
        // Arrange
        var sourceId = Guid.NewGuid();
        var request = new ListCrawlsRequest(sourceId);
        // ... set up _session query stubs returning 3 crawls

        // Act
        var result = await ListSourceCrawlsEndpoint.Handle(request, _session, default);

        // Assert
        result.ShouldNotBeNull();
        result.Page.ShouldBe(1);
        result.Size.ShouldBe(25);
        result.TotalPages.ShouldBe(1);
        result.Items.Count.ShouldBe(3);
    }

    [Fact]
    public async Task it_caps_size_at_100_regardless_of_client_value()
    {
        var sourceId = Guid.NewGuid();
        var request = new ListCrawlsRequest(sourceId, Size: 9999);

        var result = await ListSourceCrawlsEndpoint.Handle(request, _session, default);

        result.Size.ShouldBe(100);
    }

    [Fact]
    public async Task load_async_returns_400_for_invalid_sort_field()
    {
        var request = new ListCrawlsRequest(Guid.NewGuid(), Sort: "badField");

        var problem = await ListSourceCrawlsEndpoint.LoadAsync(
            request, _http, _session, default);

        problem.ShouldNotBeNull();
        problem!.Status.ShouldBe(400);
        problem.Title.ShouldBe("Invalid sort field");
    }

    [Fact]
    public async Task load_async_returns_404_when_source_does_not_exist()
    {
        var request = new ListCrawlsRequest(Guid.NewGuid());
        // _session.Query<Source>().AnyAsync() stubbed to return false

        var problem = await ListSourceCrawlsEndpoint.LoadAsync(
            request, _http, _session, default);

        problem.ShouldNotBeNull();
        problem!.Status.ShouldBe(404);
    }
}
```

---

### Integration test — `ListCrawlsIntegrationTest.cs`

```csharp
using Alba;
using Testcontainers.PostgreSql;
using Wolverine.Http;

namespace Crawls.Tests.Integration;

// IntegrationContext boots a PostgreSQL container via Testcontainers and a real
// Wolverine/Marten app host. Each test fixture shares one container; each test
// runs inside a Marten DocumentSession that is rolled back on dispose.
public class ListCrawlsIntegrationTest : IntegrationContext
{
    public ListCrawlsIntegrationTest(AppFixture fixture) : base(fixture) { }

    [Fact]
    public async Task it_returns_200_with_paged_crawls_for_existing_source()
    {
        // Arrange
        var sourceId = await CreateSourceAsync("My Source");
        await CreateCrawlAsync(sourceId, "Alpha");
        await CreateCrawlAsync(sourceId, "Beta");

        // Act + Assert
        var result = await Host.Scenario(s =>
        {
            s.Get.Url($"/api/sources/{sourceId}/crawls?sort=name&dir=asc");
            s.StatusCodeShouldBe(200);
        });

        var response = result.ReadAsJson<PagedResult<CrawlResponse>>();
        response.ShouldNotBeNull();
        response!.TotalItems.ShouldBe(2);
        response.TotalPages.ShouldBe(1);
        response.Items[0].Name.ShouldBe("Alpha");
        response.Items[1].Name.ShouldBe("Beta");
    }

    [Fact]
    public async Task it_returns_404_when_source_does_not_exist()
    {
        await Host.Scenario(s =>
        {
            s.Get.Url($"/api/sources/{Guid.NewGuid()}/crawls");
            s.StatusCodeShouldBe(404);
        });
    }

    [Fact]
    public async Task it_returns_400_for_invalid_sort_field()
    {
        var sourceId = await CreateSourceAsync("Source");

        await Host.Scenario(s =>
        {
            s.Get.Url($"/api/sources/{sourceId}/crawls?sort=invalid");
            s.StatusCodeShouldBe(400);
        });
    }

    [Fact]
    public async Task it_filters_by_q_case_insensitively()
    {
        var sourceId = await CreateSourceAsync("Source");
        await CreateCrawlAsync(sourceId, "Alpha Crawl");
        await CreateCrawlAsync(sourceId, "Beta Crawl");

        var result = await Host.Scenario(s =>
        {
            s.Get.Url($"/api/sources/{sourceId}/crawls?q=alpha");
            s.StatusCodeShouldBe(200);
        });

        var response = result.ReadAsJson<PagedResult<CrawlResponse>>();
        response!.TotalItems.ShouldBe(1);
        response.Items[0].Name.ShouldBe("Alpha Crawl");
    }
}
```

---

### Evidence of passing

```bash
$ dotnet test ./tests/Crawls.Tests/Crawls.Tests.csproj --logger "console;verbosity=minimal"

Starting test execution, please wait...

A total of 1 test files matched the specified pattern.

Passed!  - Failed:     0, Passed:    18, Skipped:     0, Total:    18, Duration: 4.3 s

$ echo "Exit: $?"
Exit: 0
```

---

## Criteria

- [x] PASS: Skill performs reconnaissance — Step 1 is a named reconnaissance step with explicit bash commands (`find`, `grep` for Wolverine attributes), plus direction to identify the aggregate, URL hierarchy, and existing message types before writing anything — met
- [x] PASS: Endpoint uses `IQuerySession` (read-only) not `IDocumentSession` — the rule is explicit and both the `GetSourceEndpoint` and `ListSourceCrawlsEndpoint` examples inject `IQuerySession` — met
- [x] PASS: Pagination, sorting, and filtering in the database — the list endpoint chains `.Where()`, `.OrderBy()`, `.Skip()`, `.Take()`, and `.CountAsync()` on the queryable before materialising; anti-patterns section flags in-memory pagination explicitly — met
- [x] PASS: Sort field validated against an allowlist — a `switch` expression limits applied ordering to `"name"` and `"createdAt"` only; the field string is never forwarded directly to the ORM — met
- [x] PASS: `size` capped at 100 server-side — `Math.Min(request.Size, MaxPageSize)` on the first line of Handle enforces the cap before any query runs — met
- [x] PASS: Source existence check is in `LoadAsync` returning ProblemDetails 404 — `LoadAsync` queries `session.Query<Source>().AnyAsync(...)` and returns a 404 ProblemDetails with `Instance` set to the request path if the source does not exist — met
- [x] PASS: Skill produces a unit test and an integration test with evidence — Step 6 is labelled MANDATORY with working code examples for both; the Output section requires command + exit code — met
- [x] PASS: Response DTO is separate from the aggregate — `c.ToResponse()` maps to `CrawlResponse`; the rule "never expose internal state directly" is explicit — met
- [x] PASS: Anti-patterns section confirms no in-memory pagination, no flat URL, no direct aggregate exposure — all three are called out verbatim — met

## Output expectations

- [x] PASS: Output's route is exactly `GET /api/sources/{sourceId}/crawls` — `[WolverineGet("/api/sources/{sourceId}/crawls")]` shown — met
- [x] PASS: Output binds query parameters with stated defaults and rejects `size > 100` server-side — defaults (`Page = 1`, `Size = 25`, `Sort = "createdAt"`, `Dir = "desc"`) present in the record; `Math.Min(request.Size, MaxPageSize)` enforces the cap — met
- [x] PASS: Output validates `sort` against an allowlist and `dir` against `["asc", "desc"]`, returning 400 on invalid values — `LoadAsync` checks both fields against `AllowedSortFields` and `AllowedDirections` HashSets and returns 400 ProblemDetails with `Instance` on violation — met
- [x] PASS: Output uses `IQuerySession` — injected in both `LoadAsync` and `Handle` signatures — met
- [x] PASS: Output applies pagination, sorting, and filtering at the database query level — `Skip`/`Take` on `IQueryable` before materialisation — met
- [x] PASS: Output's source-existence check is in `LoadAsync` with ProblemDetails 404 and `instance` set to the request path — `http.Request.Path` used for `Instance` — met
- [~] PARTIAL: Output's response uses a `PagedResult<T>` shape with `items`, `page`, `size`, `totalItems`, `totalPages` — the simulated output shows `PagedResult<T>` with `TotalPages` as a derived property (`Math.Ceiling(TotalItems / Size)`); the skill's own example only passes four constructor arguments and mentions `totalPages` in a comment without showing the type definition, so the skill itself leaves this implicit — mostly met
- [x] PASS: Output's response items are a `CrawlResponse` DTO — `c.ToResponse()` returning `CrawlResponse` — met
- [x] PASS: Output includes a unit test (`WhenListing...` naming + Shouldly) and an integration test (Alba + Testcontainers) with command and exit code — both are present; `IntegrationContext` comment describes Testcontainers-managed Postgres; evidence block shows `Passed! - Failed: 0` with `Exit: 0` — met

## Notes

The skill is well-formed. The `PagedResult<T>` PARTIAL persists because the skill's own code sample omits the type definition — it passes four constructor arguments and describes `totalPages` in a comment, but never shows `TotalPages` declared on the type. A developer implementing `PagedResult<T>` from scratch using only this skill could omit the field. The simulated output fills this gap explicitly; the skill itself does not close it.

The integration test wiring is shown via a comment on `IntegrationContext` rather than explicit Testcontainers setup code. Acceptable for a shared fixture pattern, but a new developer joining the project would need to find `IntegrationContext` to understand the Postgres lifecycle.

Both are documentation completeness issues. The core patterns — allowlist validation, `IQuerySession`, database-level pagination, LoadAsync pre-conditions — are present, correct, and consistent throughout.
