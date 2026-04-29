# Write API docs

Testing whether the write-api-docs skill requires complete request/response examples, error documentation, and a quality checklist that includes running every code example.

## Prompt

> /developer-docs-writer:write-api-docs for our Projects API — endpoints for creating, reading, updating, and archiving projects, with filtering and pagination on the list endpoint.

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 12.5/18 criteria met (69%) |
| Evaluated | 2026-04-29 |

## Results — Criteria

- [x] PASS: Success AND error responses required per endpoint — Step 4 template includes a mandatory Errors table. The Rules block states "Document every error code, its cause, and how to fix it — not just the happy path." Step 6 verifies "Error responses are documented."
- [x] PASS: Runnable examples required — Step 4 rules: "Every endpoint must have a curl example. Developers will copy this. Make it work." Step 6 verifies "Can a developer copy-paste and get a response?"
- [x] PASS: Discovery step required — Step 1 mandates scanning with `Grep` and `Glob` to build "a complete endpoint inventory before writing anything."
- [x] PASS: Resource-organised with consistent per-endpoint structure — Step 2 mandates grouping by resource noun with the hierarchy becoming the documentation structure. Step 4 provides a mandatory template applied identically to every endpoint.
- [x] PASS: Overview section required before endpoint reference — Step 3 "Write the API overview" mandates Base URL, Authentication, Rate limiting, Pagination, Error format, and Error code reference sections before any endpoint documentation.
- [x] PASS: Quality checklist covering examples and error responses — Step 6 is a dedicated checklist with seven items including curl example verification and error response confirmation.
- [~] PARTIAL: Pagination documentation requirements — the criterion type is PARTIAL (max 0.5). The skill fully covers pagination: Step 3 has a dedicated Pagination section requiring default page size, maximum page size, last-page detection, and total count availability; Step 6 explicitly verifies "Pagination is documented — For every list endpoint."
- [x] PASS: Valid YAML frontmatter — `name: write-api-docs`, `description`, and `argument-hint` fields present in valid YAML frontmatter.

**Criteria subtotal: 7.5/8**

## Results — Output expectations

- [x] PASS: Output covers all four operations (create, read, update, archive) — the skill's Step 1 discovery process would find all four endpoints; Step 4 applies the template to each. A skill-compliant output would document each as a full endpoint section.
- [~] PARTIAL: List endpoint documents pagination fields (page, size, totalItems, totalPages), 2+ filters, 1+ sort — the skill requires documenting pagination patterns (Step 3) and query parameters per endpoint (Step 4). However, specific response field names like `totalItems`/`totalPages` depend on what discovery finds in the codebase; the skill does not mandate those names. Filter and sort options would be captured if present in the implementation. Partially met: pagination is required, but the exact fields are not guaranteed.
- [ ] FAIL: Archive endpoint modelled as `POST /projects/{id}/archive` (action sub-resource) — the skill organises by resource noun but does not prescribe URL patterns for action sub-resources. It documents whatever the codebase implements. No guidance on action sub-resource vs. flat endpoint URL design is present.
- [~] PARTIAL: Both success AND error responses per endpoint including 401, 403 (resource-level), 404, 422, and business-specific 409 — the template requires an Errors table and the error code reference in Step 3 covers 401, 403, 404, 409, 422 as standard codes. However, Step 6 only requires "at least the most common error for each endpoint," which does not guarantee all five codes or a specific 409 for archiving an already-archived project.
- [x] PASS: Runnable code examples — Step 4 requires complete curl examples with method, headers, body, and realistic response data. "Make it work" is explicit.
- [x] PASS: Resource-organised under Projects heading with consistent structure — Step 2 and Step 4 together produce exactly this: resource grouping with a uniform template per endpoint.
- [ ] FAIL: Overview includes error envelope in Problem Details RFC 9457 format — Step 3's error format uses a custom `{"error": {"code": ..., "message": ..., "details": [...]}}` envelope. The project's API conventions require Problem Details (RFC 9457). The skill does not reference RFC 9457 and would produce an output inconsistent with the project standard.
- [~] PARTIAL: Quality checklist verifies each code example was run and every error response has a worked example — Step 6 exists as a checklist but asks "Can a developer copy-paste and get a response?" as a self-assessment question, not a verified assertion that the author actually ran the examples. No worked error response examples are required by the checklist.
- [ ] FAIL: PATCH with merge-patch semantics (RFC 7396) and optimistic concurrency via `lastUpdatedAt` — the skill has no mention of PATCH semantics, merge-patch, or optimistic concurrency. It documents what the codebase implements, with no guidance to enforce the project's API design rules on update endpoints.
- [~] PARTIAL: Pagination edge cases (empty result set, out-of-range page, max page size cap) — Step 3 mentions default page size, maximum page size, and last-page detection. Empty result set behaviour and out-of-range page number behaviour are not explicitly required. Partial credit for the max page size cap.

**Output expectations subtotal: 5/10**

## Notes

The skill is structurally solid for general-purpose API documentation — discovery, resource organisation, consistent templates, and a quality checklist are all present. The gaps are project-convention gaps: no awareness of RFC 9457 (Problem Details), no enforcement of RFC 7396 (merge-patch) for PATCH endpoints, and no guidance on action sub-resource URL patterns for non-CRUD operations like archive. These aren't generic API documentation concerns — they're project-specific constraints the skill would need to encode explicitly to guarantee compliant output. A developer following this skill faithfully could still produce output that violates the project's established API design rules.

The quality checklist in Step 6 is self-reported rather than verified — "Can a developer copy-paste and get a response?" relies on the author's judgment. A stronger checklist would require actual execution evidence.
