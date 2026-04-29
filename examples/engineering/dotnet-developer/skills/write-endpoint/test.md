# Test: Write GET endpoint for listing crawls under a source

Scenario: Developer invokes the write-endpoint skill for a `GET /api/sources/{sourceId}/crawls` endpoint that returns a paginated, sortable, filterable list of crawls belonging to a source.

## Prompt

Write a GET endpoint for `GET /api/sources/{sourceId}/crawls`. It should return a paginated list of crawls for a given source. Support: `page` (default 1), `size` (default 25, max 100), `sort` (name or createdAt, default createdAt), `dir` (asc or desc, default desc), and `q` for text search on crawl name. Return 404 if the source doesn't exist.

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
