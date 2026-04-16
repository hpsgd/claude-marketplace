# Write GET endpoint for listing crawls under a source

Developer invokes the write-endpoint skill for a `GET /api/sources/{sourceId}/crawls` endpoint that returns a paginated, sortable, filterable list of crawls belonging to a source.

## Prompt

> Write a GET endpoint for `GET /api/sources/{sourceId}/crawls`. It should return a paginated list of crawls for a given source. Support: `page` (default 1), `size` (default 25, max 100), `sort` (name or createdAt, default createdAt), `dir` (asc or desc, default desc), and `q` for text search on crawl name. Return 404 if the source doesn't exist.

Given the skill definition, a well-formed invocation of `write-endpoint` for this prompt would proceed as follows.

Step 1 (Reconnaissance) runs `find . -name "*.cs" -path "*/Endpoints/*"` and greps for Wolverine HTTP attributes to read existing endpoints, identify the `PagedResult<T>` return type, and match the `ListSourceCrawlsEndpoint` naming convention.

Step 2 (URL Design) confirms `/api/sources/{sourceId}/crawls` is correct — hierarchical, plural noun, ID in path.

Step 3 (Endpoint Pattern) routes to the List Endpoint sub-pattern. The skill's own `ListSourceCrawlsEndpoint` example (lines 141-187 of SKILL.md) matches this scenario almost exactly. The skill would also add a `LoadAsync` for the source existence check (404), using the pattern from the Command Endpoint section. `IQuerySession` is used throughout the list endpoint example.

The skill's list endpoint example shows sorting via a `switch` expression against named fields (`"name"`, fallback to `createdAt`), which is the allowlist pattern. The size cap is stated as a rule ("Size has a maximum (100) — enforce server-side") though the list endpoint example in the skill does not inline `Math.Min` — it states the default as `Size = 25` without showing the cap enforcement in the example code. The rule is explicit; the example is silent on the cap.

Step 4 produces `CrawlResponse` as a record separate from `Crawl`.

Step 6 produces both a unit test (`WhenListingSourceCrawls`, Shouldly) and an integration test (Alba `Host.Scenario`), with Evidence table.

The Anti-Patterns section explicitly lists "In-memory pagination," "Flat URL structure," and "Exposing aggregates as responses."

## Output



## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 8.5/9 criteria met (94%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Skill performs reconnaissance — Step 1 is an explicit reconnaissance step with bash commands to read existing endpoints before writing anything. Step 1 items 2-5 identify the aggregate, URL hierarchy, and existing message types.
- [x] PASS: Endpoint uses `IQuerySession` for GET — Query Endpoint section: "Use `IQuerySession` (read-only) not `IDocumentSession` (read-write) for queries." The `GetSourceEndpoint` and `ListSourceCrawlsEndpoint` examples both use `IQuerySession`. List endpoint rules state this explicitly.
- [x] PASS: Pagination/sorting/filtering in database — List endpoint rules: "Pagination, sorting, and filtering happen in the database (not in memory)" and "Never fetch full result set to filter in memory." The `ListSourceCrawlsEndpoint` example shows `.Where()`, `.OrderBy()`, `.Skip().Take()`, and `.CountAsync()` chained on the queryable.
- [x] PASS: Sort field validated against allowlist — List endpoint rules: "Sort field must be from an allowlist — do not accept arbitrary field names (SQL injection vector)." The `ListSourceCrawlsEndpoint` example uses a `switch` expression matching `"name"` and falling through to `createdAt` — no arbitrary field pass-through.
- [x] PASS: `size` capped at 100 server-side — List endpoint rules: "Size has a maximum (100) — enforce server-side." The rule is explicit. The example code does not show `Math.Min` inline but the rule text is unambiguous.
- [x] PASS: Source existence check in LoadAsync returning ProblemDetails 404 — LoadAsync rules: "Returns `Task<ProblemDetails?>` — null means 'proceed', non-null means 'stop with this error'." "Handles: existence checks, uniqueness validation, authorisation." The `CreateSourceEndpoint.LoadAsync` example demonstrates the pattern; the list endpoint example omits `LoadAsync` (since it checks for source), but the rule and pattern are clearly stated and applicable.
- [x] PASS: Skill produces unit and integration tests with evidence — Step 6 is marked "(MANDATORY — both unit and integration)" with explicit unit and integration test examples. Output section item 5 states "Evidence that tests pass (command + exit code)."
- [~] PARTIAL: Response DTO separate from aggregate — Step 4 rules: "Response DTOs are separate from aggregates — never expose internal state directly." Step 3 Query Endpoint rules: "Map to a response DTO — never expose the aggregate directly." The `ListSourceCrawlsEndpoint` example calls `.ToResponse()` on each item. The criterion is prefixed PARTIAL, so maximum score is 0.5.
- [x] PASS: Anti-patterns section confirms specified items — Anti-Patterns section explicitly lists: "In-memory pagination — query.ToList().Skip().Take() loads everything," "Flat URL structure — `/crawls/{id}` without the parent `/sources/{sourceId}/crawls/{id}`," and "Exposing aggregates as responses — always map to a response DTO."

## Notes

The skill's `ListSourceCrawlsEndpoint` example (Step 3) maps almost directly to this test scenario, which means there is very little ambiguity about what the skill would produce. The example covers hierarchical URL, `IQuerySession`, database-side filtering and pagination, and the `switch`-based sort allowlist.

The LoadAsync criterion for the 404 check is worth flagging: the list endpoint example in Step 3 does not include `LoadAsync` (it jumps straight to `Handle`). The source existence check would need to be inferred from the Command Endpoint `LoadAsync` pattern. The rule text is clear enough for a pass, but adding a list endpoint example with a parent-resource existence check would close the gap.

The `size` cap rule is stated explicitly but not shown in the example code. The list endpoint example uses `request.Size` directly without a `Math.Min` call. A developer following only the example (not the rules) might miss the cap. The rule text saves this criterion, but the example should match the rule.
