# Result: Write GET endpoint for listing crawls under a source

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17.5 / 19 criteria met (92%) |
| **Evaluated** | 2026-04-29 |
| **Skill source** | `plugins/engineering/dotnet-developer/skills/write-endpoint/SKILL.md` |

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

- [x] PASS: Output's route is exactly `GET /api/sources/{sourceId}/crawls` — `[WolverineGet("/api/sources/{sourceId}/crawls")]` is shown in the example — met
- [x] PASS: Output binds query parameters with stated defaults and rejects `size > 100` server-side — defaults (`Page = 1`, `Size = 25`, `Sort = "createdAt"`, `Dir = "desc"`) are present in the record; `Math.Min(request.Size, MaxPageSize)` enforces the cap — met
- [x] PASS: Output validates `sort` against an allowlist and `dir` against `["asc", "desc"]`, returning 400 on invalid values — `LoadAsync` checks both fields against `AllowedSortFields` and `AllowedDirections` HashSets and returns 400 ProblemDetails with `Instance` on violation — met
- [x] PASS: Output uses `IQuerySession` — injected in both `LoadAsync` and `Handle` signatures — met
- [x] PASS: Output applies pagination, sorting, and filtering at the database query level — `Skip`/`Take` on `IQueryable` before materialisation — met
- [x] PASS: Output's source-existence check is in `LoadAsync` with ProblemDetails 404 and `instance` set to the request path — present in `LoadAsync`, using `http.Request.Path` for `Instance` — met
- [~] PARTIAL: Output's response uses a `PagedResult<T>` shape with `items`, `page`, `size`, `totalItems`, `totalPages` — the constructor call shows four positional arguments (`items`, `page`, `size`, `totalItems`); `totalPages` is stated in a comment as computed by the constructor but is not shown in the constructor signature or the returned value — partially met
- [x] PASS: Output's response items are a `CrawlResponse` DTO — `c.ToResponse()` returning `CrawlResponse` — met
- [~] PARTIAL: Output includes a unit test (When... naming + Shouldly) and an integration test (Alba + Testcontainers) with command and exit code — both test styles are shown with Shouldly and Alba; Testcontainers is referenced in the description ("Testcontainers-managed Postgres") but no Testcontainers setup code is shown; the evidence block shows a dotnet test command with exit code — mostly met
- [x] PASS: Output's `q` text-search filter is case-insensitive and against documented fields — `MatchesSql("%?%", request.Q)` is used with an explicit comment "Case-insensitive substring search on the crawl Name field (Marten ILIKE)"; both the mechanism and the target field are documented — met

## Notes

The skill was edited since the previous evaluation and the three major gaps have been closed.

`LoadAsync` now covers the list endpoint with parent-resource existence (404) and sort/dir validation (400 ProblemDetails), both with `Instance` set to the request path. The size cap is enforced with `Math.Min` in Handle. The `q` filter uses `MatchesSql` with an explanatory comment instead of `string.Contains`.

Two minor gaps remain. The `PagedResult` constructor call only shows four arguments; `totalPages` is mentioned in a comment but its presence in the type is not demonstrated. A developer reading this in isolation could implement a `PagedResult<T>` without `totalPages`. The Testcontainers reference in the testing rules is descriptive but the `IntegrationContext` setup code is not shown — a developer new to the project would need to look it up elsewhere.

Neither gap is significant enough to affect the verdict. Both are documentation completeness issues, not correctness issues.
