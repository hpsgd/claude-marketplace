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
