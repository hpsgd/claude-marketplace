# Result: Write API docs

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15/16 criteria met (93.75%) |
| Evaluated | 2026-04-29 |

## Results — Criteria

- [x] PASS: Skill requires success AND error responses per endpoint — Step 4 template includes a mandatory Errors table. Step 6 requires a worked example for every documented error. The Rules block states "Document every error code, its cause, and how to fix it — not just the happy path."
- [x] PASS: Skill requires runnable examples — Step 4: "Every endpoint must have a curl example. Developers will copy this. Make it work." Step 6 checks "Every curl example was actually run" and requires the response body recorded next to the example.
- [x] PASS: Skill requires a discovery step — Step 1 mandates scanning with `Grep` and `Glob` to build "a complete endpoint inventory before writing anything."
- [x] PASS: Skill organises by resource with consistent per-endpoint structure — Step 2 groups endpoints by resource noun; Step 4 provides a mandatory template applied identically to every endpoint.
- [x] PASS: Skill requires an overview section before endpoint reference — Step 3 mandates Base URL, Authentication, Rate limiting, Pagination, Error format, and Error code reference sections before any endpoint documentation.
- [x] PASS: Skill includes a quality checklist covering examples and error responses — Step 6 is a dedicated checklist requiring that every curl example was run with response body recorded, and that every documented error has a worked request/response example.
- [~] PARTIAL: Pagination documentation requirements — Step 3 has a dedicated Pagination section requiring default page size, maximum page size, how to detect the last page, and whether total count is available. Step 6 verifies pagination is documented for every list endpoint. Full coverage of the core requirements; full 0.5 awarded.
- [x] PASS: Valid YAML frontmatter — `name: write-api-docs`, `description`, and `argument-hint` fields present in valid YAML frontmatter.

**Criteria subtotal: 7.5/8**

## Results — Output expectations

- [x] PASS: Output covers all four operations — Step 1 discovers all endpoints in the codebase; Step 4 applies the template to each. A skill-compliant output for the Projects API would produce documented sections for create, read, update, and archive.
- [x] PASS: List endpoint documents pagination and filter/sort parameters — Step 3 requires the pagination pattern (with default and max page size), and Step 4's query parameters table requires type, required flag, default, and description for every parameter. Filter and sort parameters present in the implementation would be fully documented.
- [x] PASS: Both success AND error responses per endpoint including 401, 403, 404, 422 — Step 4 requires an Errors table per endpoint. Step 3's error code reference table explicitly covers 401, 403, 404, 409, and 422. Step 6 requires a worked example for each error.
- [x] PASS: Runnable code examples — Step 4 requires full curl examples with method, headers, body, and realistic response data. Step 6 requires each example to have been actually run with the response body recorded.
- [x] PASS: Resource-organised under a Projects heading with consistent structure — Step 2 produces resource grouping; Step 4's template enforces Description, Authentication, Parameters, Request body, Response, Errors, Example per endpoint.
- [x] PASS: Overview and authentication section before endpoint reference — Step 3 mandates Base URL, Authentication (with exact error responses for auth failures), Rate limiting, Pagination, Error format, and Error code reference.
- [x] PASS: Quality checklist verifies each example was run and every error has a worked example — Step 6 explicitly requires "Record the response body next to the example. Untested examples do not pass this check." and "Show the request that triggers each error and paste the actual error body returned."
- [~] PARTIAL: Pagination edge cases — Step 3 covers default page size, maximum page size, and last-page detection. Out-of-range page number behaviour and empty result set behaviour are not explicitly required. Partial credit for max page size cap and last-page detection.

**Output expectations subtotal: 7.5/8**

## Notes

The skill is thorough for general-purpose API documentation. The Step 6 quality checklist is stronger than most: it requires actual execution evidence (response body recorded) rather than a self-reported assertion. The main gap is pagination edge cases — the skill does not require documenting what happens when a page number exceeds the total, or what the empty result set response looks like. These are common developer pain points worth encoding explicitly.

The error format in Step 3 uses a custom envelope (`{"error": {"code": ..., "message": ..., "details": [...]}}`) rather than RFC 9457 Problem Details. Teams with a specific error envelope standard would need to override this section.
