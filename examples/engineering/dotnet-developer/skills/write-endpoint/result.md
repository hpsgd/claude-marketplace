# Result: Write GET endpoint for listing crawls under a source

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 14.5 / 19 criteria met (76%) |
| **Evaluated** | 2026-04-29 |
| **Skill source** | `plugins/engineering/dotnet-developer/skills/write-endpoint/SKILL.md` |

## Criteria

- [x] PASS: Skill performs reconnaissance — Step 1 is a named reconnaissance step with explicit bash commands (`find`, `grep` for Wolverine attributes), plus direction to identify the aggregate, URL hierarchy, and existing message types before writing anything — met
- [x] PASS: Endpoint uses `IQuerySession` (read-only) not `IDocumentSession` — the rule is explicit and both the `GetSourceEndpoint` and `ListSourceCrawlsEndpoint` examples inject `IQuerySession` — met
- [x] PASS: Pagination, sorting, and filtering in the database — the list endpoint chains `.Where()`, `.OrderBy()`, `.Skip()`, `.Take()`, and `.CountAsync()` on the queryable before materialising; anti-patterns section flags in-memory pagination explicitly — met
- [x] PASS: Sort field validated against an allowlist — a `switch` expression limits applied ordering to `"name"` and `"createdAt"` only; the field string is never forwarded directly to the ORM — met
- [~] PARTIAL: `size` capped at 100 server-side — the rule states "Size has a maximum (100) — enforce server-side" but the code example uses `request.Size` directly with no `Math.Min`, guard clause, or validation attribute; stated but not demonstrated — partially met
- [ ] FAIL: Source existence check is in `LoadAsync` returning ProblemDetails 404 — the list endpoint example has no `LoadAsync`; source existence is not checked at all for this query endpoint; the pattern appears only in command and update examples — not found
- [x] PASS: Skill produces a unit test and an integration test with evidence — Step 6 is labelled MANDATORY with working code examples for both; the Output section requires command + exit code — met
- [x] PASS: Response DTO is separate from the aggregate — `c.ToResponse()` maps to `CrawlResponse`; the rule "never expose internal state directly" is explicit — met (full credit; PARTIAL label on this criterion does not reduce score given the DTO separation is fully demonstrated)
- [x] PASS: Anti-patterns section confirms no in-memory pagination, no flat URL, no direct aggregate exposure — all three are called out verbatim — met

## Output expectations

- [x] PASS: Output's route is exactly `GET /api/sources/{sourceId}/crawls` — `[WolverineGet("/api/sources/{sourceId}/crawls")]` is shown in the example — met
- [~] PARTIAL: Output binds query parameters with stated defaults and rejects `size > 100` server-side — defaults (`Page = 1`, `Size = 25`, `Sort = "createdAt"`, `Dir = "desc"`) are present in the record; size cap enforcement code is absent — partially met
- [ ] FAIL: Output validates `sort` against an allowlist and `dir` against `["asc", "desc"]`, returning 400 on invalid values — the switch silently falls through to the default for invalid sort values; `dir` is not validated at all; no 400 ProblemDetails is returned — not found
- [x] PASS: Output uses `IQuerySession` — injected in the Handle signature — met
- [x] PASS: Output applies pagination, sorting, and filtering at the database query level — `Skip`/`Take` on `IQueryable` before materialisation — met
- [ ] FAIL: Output's source-existence check is in `LoadAsync` with ProblemDetails 404 and `instance` set to the request path — the list endpoint has no `LoadAsync`; no source existence check is shown for this endpoint — not found
- [~] PARTIAL: Output's response uses a `PagedResult<T>` shape with `items`, `page`, `size`, `totalItems`, `totalPages` — the constructor call shows four positional arguments (`items`, `page`, `size`, `totalItems`); `totalPages` is not present in the example and is not confirmed to be computed in the constructor — partially met
- [x] PASS: Output's response items are a `CrawlResponse` DTO — `c.ToResponse()` returning `CrawlResponse` — met
- [~] PARTIAL: Output includes a unit test (When... naming + Shouldly) and an integration test (Alba + Testcontainers) with command and exit code — both test styles are shown with Shouldly and Alba; Testcontainers is referenced in the description but not demonstrated in any code example; no "command + exit code" evidence block appears anywhere in the skill — partially met
- [~] PARTIAL: Output's `q` text-search filter is case-insensitive and against documented fields — `.Contains(request.Q)` is shown with no case-insensitivity modifier; no documentation of which fields are searched — partially met

## Notes

Two gaps appear in both sections and account for most of the lost score.

**Missing LoadAsync for the list endpoint.** Every command and mutation pattern in the skill demonstrates a `LoadAsync` for existence and authorisation checks, but the list endpoint example goes straight to Handle. A caller requesting crawls for a non-existent source would receive an empty list rather than a 404. Adding a list variant with a parent-resource existence `LoadAsync` would close this — the pattern is present elsewhere in the skill and just needs to be applied here.

**No 400 rejection for invalid sort or dir values.** The switch expression prevents injection but silently applies a default when the caller passes `sort=foobar` or `dir=sideways`. The output expectations require an explicit 400 ProblemDetails response. This is a real API contract issue, not a style gap — callers have no way to detect that their parameter was ignored.

The size cap is stated in rules but absent from example code. The rule saves the criterion score in the Criteria section; the Output expectations section docks it because a developer following the example literally would not enforce it.

The `q` filter using `.Contains()` will be case-sensitive in PostgreSQL via Marten unless `ILike` or full-text search is used. The skill does not address this.

The overall structure and pattern coverage is solid. The gaps are specific and fixable, not architectural.
