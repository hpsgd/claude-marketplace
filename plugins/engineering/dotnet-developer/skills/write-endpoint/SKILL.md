---
name: write-endpoint
description: Write a Wolverine HTTP endpoint with pre-conditions, handler, and tests.
argument-hint: "[endpoint description, e.g. 'GET /api/sources/{id}/crawls']"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
paths:
  - "**/*.cs"
---

Write a Wolverine endpoint for $ARGUMENTS.

## Process (sequential — do not skip steps)

### Step 1: Reconnaissance

Before writing the endpoint:

1. **Read existing endpoints** — find the nearest similar endpoint and match its patterns
   ```bash
   find . -name "*.cs" -path "*/Endpoints/*" | head -20
   grep -rn "WolverineGet\|WolverinePost\|WolverinePut\|WolverineDelete\|WolverinePatch" --include="*.cs" | head -20
   ```

2. **Identify the aggregate** — which Marten aggregate does this endpoint operate on?
3. **Identify the URL hierarchy** — trace the entity ownership chain to the root
4. **Check for existing commands/events** — reuse existing message types where appropriate

### Step 2: URL Design

URLs MUST mirror entity ownership. No flat top-level listings of child resources.

```
GET    /api/sources                           → List sources (paginated)
POST   /api/sources                           → Create source
GET    /api/sources/{sourceId}                → Get source
PATCH  /api/sources/{sourceId}                → Update source
DELETE /api/sources/{sourceId}                → Delete source
GET    /api/sources/{sourceId}/crawls         → List crawls for source
POST   /api/sources/{sourceId}/crawls         → Create crawl for source
GET    /api/sources/{sourceId}/crawls/{crawlId} → Get specific crawl
```

**Rules:**
- Plural nouns for collections: `/sources`, not `/source`
- IDs in path: `{sourceId}`, not `{id}` (disambiguates in nested routes)
- No verbs in URLs: `POST /sources/{id}/crawls` not `POST /sources/{id}/triggerCrawl`
- Maximum 3 levels of nesting — beyond that, promote to a top-level resource with a reference

### Step 3: Endpoint Pattern

#### Command Endpoint (POST, PATCH, DELETE)

```csharp
public static class CreateSourceEndpoint
{
    // Pre-condition: validate, load dependencies, check authorisation
    // Returns ProblemDetails to short-circuit with an error response
    // Returns null to proceed to Handle
    public static async Task<ProblemDetails?> LoadAsync(
        CreateSourceCommand command,
        IDocumentSession session,
        CancellationToken ct)
    {
        // Validate business rules that require database access
        var exists = await session.Query<Source>()
            .AnyAsync(s => s.Name == command.Name, ct);

        if (exists)
        {
            return new ProblemDetails
            {
                Title = "Source already exists",
                Detail = $"A source with name '{command.Name}' already exists.",
                Status = 409
            };
        }

        return null; // Proceed to Handle
    }

    // Handler: pure business logic, returns events as cascading messages
    [WolverinePost("/api/sources")]
    public static SourceCreated Handle(CreateSourceCommand command)
    {
        var source = new Source
        {
            Id = CombGuidIdGeneration.NewGuid(),
            Name = command.Name,
            Url = command.Url,
            CreatedAt = DateTimeOffset.UtcNow
        };

        return new SourceCreated(source.Id, source.Name);
    }
}
```

**LoadAsync rules:**
- Static method — no instance state
- Returns `Task<ProblemDetails?>` — null means "proceed", non-null means "stop with this error"
- Handles: existence checks, uniqueness validation, authorisation, loading related entities
- Does NOT handle: input format validation (that's the command record's job) or business logic (that's Handle's job)
- Inject `IDocumentSession`, `CancellationToken`, and any services needed for validation

**Handle rules:**
- Static method for stateless operations, or instance method on aggregate for state-dependent decisions
- Receives the command as a parameter
- Returns events as cascading messages (single event, tuple of events, or `object?` for polymorphic cascade)
- Contains pure business logic — no database access in Handle
- No try/catch — let Wolverine's error handling pipeline manage failures

#### Query Endpoint (GET single item)

```csharp
public static class GetSourceEndpoint
{
    [WolverineGet("/api/sources/{sourceId}")]
    public static async Task<IResult> Handle(
        Guid sourceId,
        IQuerySession session,
        CancellationToken ct)
    {
        var source = await session.LoadAsync<Source>(sourceId, ct);

        return source is not null
            ? Results.Ok(source.ToResponse())
            : Results.NotFound();
    }
}
```

**Rules:**
- Use `IQuerySession` (read-only) not `IDocumentSession` (read-write) for queries
- Return `IResult` to control HTTP status codes
- Map to a response DTO — never expose the aggregate directly

#### List Endpoint (GET collection — paginated)

```csharp
public static class ListSourceCrawlsEndpoint
{
    private const int MaxPageSize = 100;
    private static readonly HashSet<string> AllowedSortFields = new(StringComparer.OrdinalIgnoreCase)
        { "name", "createdAt" };
    private static readonly HashSet<string> AllowedDirections = new(StringComparer.OrdinalIgnoreCase)
        { "asc", "desc" };

    public record ListCrawlsRequest(
        Guid SourceId,
        int Page = 1,
        int Size = 25,
        string? Sort = "createdAt",
        string? Dir = "desc",
        string? Q = null);

    // Pre-condition: validate sort/dir against allowlist, check parent source exists.
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

        return null; // Proceed to Handle
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
            // Case-insensitive substring search on the crawl Name field (Marten ILIKE).
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

        // PagedResult constructor computes totalPages = ceil(totalItems / size).
        return new PagedResult<CrawlResponse>(
            items.Select(c => c.ToResponse()).ToList(),
            request.Page,
            size,
            totalItems);
    }
}
```

**List endpoint rules:**
- Every list endpoint supports: `page`, `size`, `sort`, `dir`, `q` (text search)
- Return `PagedResult<T>` with `items`, `page`, `size`, `totalItems`, `totalPages` (derived from `totalItems / size`)
- Pagination, sorting, and filtering happen in the database (not in memory)
- Default sort order is sensible (usually `createdAt desc` for time-based, `name asc` for alphabetical)
- Sort field and direction validated in `LoadAsync` against an allowlist — return 400 ProblemDetails on invalid values, never forward arbitrary strings to the ORM
- Size capped at 100 server-side via `Math.Min(request.Size, MaxPageSize)` — never trust the client value
- Parent-resource existence checked in `LoadAsync` returning 404 ProblemDetails with `Instance` set to the request path — a list query for a non-existent parent is a 404, not an empty array
- Text search (`q`) uses case-insensitive substring matching against documented fields (e.g. `Name`) via Marten `ILIKE` / `MatchesSql`, not the default case-sensitive `string.Contains`

### Step 4: Command and Event Records

```csharp
// Command — what the caller wants to happen
public record CreateSourceCommand(
    string Name,
    string Url);

// Event — what happened (past tense, immutable)
public record SourceCreated(
    Guid SourceId,
    string Name);

// Response DTO — what the caller sees
public record SourceResponse(
    Guid Id,
    string Name,
    string Url,
    DateTimeOffset CreatedAt,
    DateTimeOffset? LastUpdatedAt);
```

**Rules:**
- Commands are imperative (`CreateSource`, `UpdateCrawlSettings`)
- Events are past tense (`SourceCreated`, `CrawlSettingsUpdated`)
- Response DTOs are separate from aggregates — never expose internal state directly
- Records (not classes) for commands, events, and responses — immutability by default
- Include `LastUpdatedAt` on every response for optimistic concurrency

### Step 5: Optimistic Concurrency (MANDATORY for PATCH/PUT)

```csharp
public static class UpdateSourceEndpoint
{
    public static async Task<ProblemDetails?> LoadAsync(
        UpdateSourceCommand command,
        IDocumentSession session,
        CancellationToken ct)
    {
        var source = await session.LoadAsync<Source>(command.SourceId, ct);

        if (source is null)
            return new ProblemDetails { Status = 404, Title = "Source not found" };

        if (source.LastUpdatedAt != command.LastUpdatedAt)
            return new ProblemDetails
            {
                Status = 409,
                Title = "Conflict",
                Detail = "The resource was modified by another request. Please re-fetch and retry."
            };

        return null;
    }

    [WolverinePatch("/api/sources/{sourceId}")]
    public static SourceUpdated Handle(UpdateSourceCommand command, Source source)
    {
        // Apply changes using RFC 7396 merge semantics
        if (command.Name is not null) source.Name = command.Name;
        if (command.Url is not null) source.Url = command.Url;
        source.LastUpdatedAt = DateTimeOffset.UtcNow;

        return new SourceUpdated(source.Id);
    }
}
```

### Step 6: Testing (MANDATORY — both unit and integration)

#### Unit Test (Handler logic)

```csharp
public class WhenCreatingASource
{
    [Fact]
    public void it_returns_a_source_created_event()
    {
        // Arrange
        var command = new CreateSourceCommand("Test Source", "https://example.com");

        // Act
        var result = CreateSourceEndpoint.Handle(command);

        // Assert
        result.ShouldNotBeNull();
        result.Name.ShouldBe("Test Source");
    }
}
```

#### Integration Test (Full HTTP round-trip via Alba)

```csharp
public class CreateSourceIntegrationTest : IntegrationContext
{
    [Fact]
    public async Task it_creates_a_source_and_returns_201()
    {
        // Arrange
        var command = new CreateSourceCommand("Test Source", "https://example.com");

        // Act
        var result = await Host.Scenario(s =>
        {
            s.Post.Json(command).ToUrl("/api/sources");
            s.StatusCodeShouldBe(201);
        });

        // Assert
        var response = result.ReadAsJson<SourceResponse>();
        response.ShouldNotBeNull();
        response.Name.ShouldBe("Test Source");
    }

    [Fact]
    public async Task it_returns_409_when_source_name_already_exists()
    {
        // Arrange — create existing source
        await Host.Scenario(s =>
        {
            s.Post.Json(new CreateSourceCommand("Duplicate", "https://a.com")).ToUrl("/api/sources");
            s.StatusCodeShouldBe(201);
        });

        // Act — try to create another with same name
        await Host.Scenario(s =>
        {
            s.Post.Json(new CreateSourceCommand("Duplicate", "https://b.com")).ToUrl("/api/sources");
            s.StatusCodeShouldBe(409);
        });
    }
}
```

**Testing rules:**
- BDD class naming: `WhenCreatingASource`, `GivenAnExistingSource`
- NSubstitute for mocks: `Substitute.For<T>()`
- Shouldly for assertions: `ShouldBe`, `ShouldNotBeNull`, `ShouldThrow`
- Alba for HTTP integration with Testcontainers-managed Postgres (`IntegrationContext` boots a real database container per test fixture — no shared dev DB, no in-memory provider)
- Test happy path, conflict (409), not found (404), validation (422), and authorisation (403)
- Factory helpers for test data — no inline magic strings

**Evidence of passing — paste actual command and exit code into the PR description:**

```bash
$ dotnet test ./tests/Sources.Tests/Sources.Tests.csproj
Passed!  - Failed:     0, Passed:    14, Skipped:     0, Total:    14
$ echo "Exit: $?"
Exit: 0
```

## Anti-Patterns (NEVER do these)

- **Database access in Handle** — Handle is for pure business logic. Database goes in LoadAsync or side-effect handlers
- **Exposing aggregates as responses** — always map to a response DTO
- **Flat URL structure** — `/crawls/{id}` without the parent `/sources/{sourceId}/crawls/{id}`
- **In-memory pagination** — query.ToList().Skip().Take() loads everything. Paginate in the database
- **Missing optimistic concurrency** — PATCH/PUT without `lastUpdatedAt` allows silent overwrites
- **Catching exceptions in handlers** — let Wolverine's error pipeline handle failures
- **Sequential IDs in URLs** — use GUIDs or CombGuid. Sequential IDs enable enumeration

## Output

Deliver:
1. Endpoint class with LoadAsync (if applicable) and Handle
2. Command, event, and response records
3. Unit test for handler logic
4. Integration test for HTTP round-trip
5. Evidence that tests pass (command + exit code)

## Related Skills

- `/dotnet-developer:write-handler` — endpoints delegate to handlers. Write the endpoint first (HTTP contract), then the handler (business logic).
