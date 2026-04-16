---
name: review-dotnet
description: "Review .NET / C# code against team conventions — messaging architecture, API design, testing, dependency management, and analyser compliance. Auto-invoked when reviewing .cs files."
argument-hint: "[files, PR, or git range to review]"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
paths:
  - "**/*.cs"
---

Review .NET and C# code against team architectural patterns and conventions. This methodology covers messaging architecture, API design, testing, dependency management, and analyser compliance.

## Mandatory Process

Execute all seven passes. Every finding requires file, line, and evidence.

### Pass 1: Message Architecture — One Message, One Unit of Work

The foundational rule: every message handler performs exactly one unit of work. No loops with heavy inline logic. No handlers that orchestrate multiple unrelated operations.

1. **Handler scan** — find all message handlers in changed files:
   ```bash
   grep -rn 'IHandleMessages\|ICommandHandler\|IEventHandler\|Handle\s*(' --include='*.cs' [changed files]
   ```

2. **Loop detection in handlers** — grep for `foreach`, `for (`, `while (`, `Parallel.For`, `.Select(` inside handler methods. Each loop that performs I/O, database access, or publishes messages is a finding:
   - **Wrong**: `foreach (var item in items) { await _repository.Save(item); }`
   - **Right**: Batch the operation or publish individual messages for each item

3. **Handler responsibility** — read each handler. It should:
   - Validate preconditions
   - Perform one operation
   - Return or publish one result
   If a handler does validate + fetch + transform + save + notify, it has multiple units of work. Split into separate messages.

4. **Side effects in handlers** — handlers should not send emails, call external APIs, or write to multiple aggregates. Those belong in separate handlers triggered by domain events.

### Pass 2: AggregateHandler and Cascading Returns

1. **`[AggregateHandler]` usage** — aggregates that handle commands must use the `[AggregateHandler]` attribute with cascading returns, not manual event publishing:
   ```bash
   grep -rn 'AggregateHandler\|\.Publish\|\.Send\(' --include='*.cs' [changed files]
   ```
   If a handler inside an aggregate calls `_bus.Publish()` or `_mediator.Send()` manually, that is a finding. Use cascading return types instead — the infrastructure handles event dispatch.

2. **Return types** — aggregate handlers return domain events as their result. The framework publishes them. Verify handlers return the event, not `void` or `Task`.

3. **Idempotency guards on creation handlers** — handlers that create aggregates from coordination events (e.g., `WorkItemTriggered` → create `WorkItem`) must check whether the aggregate already exists before calling create. Event replay after a partial write will re-run the handler, and a second create for the same ID produces a duplicate-version conflict in the event store:
   - **Wrong**: `var item = new WorkItem(command.Id); await repository.Save(item);`
   - **Right**: Try to load the aggregate first. If it exists, return early. If `AggregateNotFound`, proceed with creation.

4. **Event immutability** — domain events must be immutable records or classes with `init`-only properties. Grep for `set;` in event classes:
   ```bash
   grep -rn 'set;' --include='*.cs' [event file paths]
   ```

### Pass 3: API Design — Hierarchical and Complete

1. **URL structure** — API endpoints must reflect entity ownership hierarchically:
   - **Right**: `/api/organisations/{orgId}/projects/{projectId}/tasks/{taskId}`
   - **Wrong**: `/api/tasks/{taskId}` (loses the ownership chain)
   Read controller route attributes and verify the hierarchy matches the domain model.

2. **Static `LoadAsync` for preconditions** — endpoints that need to validate entity existence or permissions before executing should use the static `LoadAsync` pattern:
   ```csharp
   public static async Task<IResult> LoadAsync(Guid id, IRepository repo)
   ```
   This separates precondition loading from business logic. If a controller action starts with 5 lines of "fetch and check if null" logic, that belongs in `LoadAsync`.

3. **List endpoints — pagination, sort, filter** — every list endpoint must support:
   - Pagination (skip/take or cursor-based)
   - At least one sort parameter
   - Text filter/search
   - All filtering and sorting happens in the database query, not in memory

   Grep for list endpoints (methods returning collections) and verify these parameters exist:
   ```bash
   grep -rn 'IEnumerable\|IList\|List<\|IQueryable\|Task<.*\[\]>' --include='*.cs' [changed files]
   ```
   If a list endpoint loads all records and filters in memory (`.ToList()` followed by `.Where()`), that is a critical finding.

4. **Consistent response shapes** — all endpoints should return consistent wrapper types. No raw primitives as responses.

### Pass 4: Dependency Management

1. **Constructor injection only** — dependencies come through the constructor, never through property injection, service locator, or static helpers:
   ```bash
   grep -rn 'ServiceLocator\|GetService\|Resolve<\|\.GetRequiredService' --include='*.cs' [changed files]
   ```
   Every hit is a finding. Use constructor injection with interfaces.

2. **External dependencies behind interfaces** — every external system (database, HTTP client, file system, clock, message bus) must be accessed through an interface. Direct usage of `HttpClient`, `DateTime.Now`, `File.ReadAllText` is a finding:
   ```bash
   grep -rn 'DateTime\.Now\|DateTime\.UtcNow\|File\.\|Directory\.' --include='*.cs' [changed files]
   ```
   Use `IDateTimeProvider`, `IFileSystem`, etc. This enables testing.

3. **Central package management** — verify the solution uses `Directory.Packages.props` for NuGet versions. Individual `.csproj` files should not specify package versions:
   ```bash
   grep -rn 'Version=' --include='*.csproj' [changed files]
   ```
   Package versions in `.csproj` files are a finding (they should use `VersionOverride` only in exceptional cases).

### Pass 5: Managed Sessions

1. **Session lifecycle** — database sessions / units of work must be managed by infrastructure, not by handlers. Handlers should not call `SaveChanges()`, `Commit()`, or `Dispose()` on sessions directly. The pipeline handles that.

2. **Transaction boundaries** — if a handler needs a transaction broader than the default, it must be explicit and documented. Grep for `BeginTransaction`, `TransactionScope`:
   ```bash
   grep -rn 'BeginTransaction\|TransactionScope' --include='*.cs' [changed files]
   ```
   Each hit requires a comment explaining why the default session management is insufficient.

### Pass 6: Analyser Compliance

1. **Warnings-as-errors** — verify the project treats analyser warnings as errors. Check `.csproj` or `Directory.Build.props`:
   ```bash
   grep -rn 'TreatWarningsAsErrors\|WarningsAsErrors' --include='*.csproj' --include='*.props'
   ```
   If `TreatWarningsAsErrors` is not `true`, that is a finding.

2. **Suppression audit** — grep for all analyser suppressions:
   ```bash
   grep -rn '#pragma warning disable\|SuppressMessage\|GlobalSuppressions' --include='*.cs' [changed files]
   ```
   Every suppression must have:
   - The specific warning code (not a blanket suppression)
   - An inline justification comment
   - A linked issue number if the suppression is temporary

3. **Nullable reference types** — verify `<Nullable>enable</Nullable>` is set. Grep for `null!` (null-forgiving operator):
   ```bash
   grep -rn 'null!' --include='*.cs' [changed files]
   ```
   Each `null!` is a finding unless it is in a test fixture or deserialization constructor with a comment.

### Pass 7: Testing Standards

1. **BDD naming** — test methods must use BDD-style names describing the scenario:
   - **Right**: `WhenCreatingUserWithDuplicateEmail_ShouldReturnConflict`
   - **Wrong**: `TestCreateUser`, `CreateUser_Test`, `Test1`

   ```bash
   grep -rn '\[Fact\]\|\[Theory\]\|\[Test\]' --include='*.cs' -A1 [changed files]
   ```
   Read the method name on the line after each attribute.

2. **Test structure** — each test follows Arrange/Act/Assert (or Given/When/Then). Tests with multiple Act steps test too much — split them.

3. **No test logic** — tests should not contain `if`, `switch`, `try/catch`, or loops. A test that branches is testing multiple things.

4. **Integration over mocking** — prefer integration tests with real dependencies (in-memory database, test bus) over unit tests that mock everything. Tests that mock the thing being tested are always wrong.

## Evidence Format

```
### [SEVERITY] [Pass]: [Short description]

**File:** `path/to/File.cs:42`
**Evidence:** [code or grep output]
**Standard:** [which rule is violated]
**Fix:** [concrete code change or architectural suggestion]
```

## Output Template

```
## .NET Review

### Summary
- Files reviewed: N
- Message architecture: X findings
- Aggregate patterns: X findings
- API design: X findings
- Dependencies: X findings
- Sessions: X findings
- Analysers: X findings
- Testing: X findings

### Findings
[grouped by severity: critical, important, suggestion]

### Clean Areas
[what was done well]
```

## Zero-Finding Gate

If all checks pass: "No findings. .NET review complete — all changed files comply with team conventions." Do not fabricate issues.

## Related Skills

- `/coding-standards:review-standards` — cross-cutting quality and writing style checks that apply to all languages. Run alongside this review.
- `/coding-standards:review-git` — commit message and PR conventions. Run when reviewing a PR.
