# Output: api-design skill structure

**Verdict:** PASS
**Score:** 18.5/19 criteria met (97%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill defines a URL hierarchy rule — resources must be accessed through parent chains, no flat top-level listings of child resources — met. Step 2 states "No flat top-level listings of child resources. `/crawls` does not exist — it is always `/sources/{sourceId}/crawls`"
- [x] PASS: Skill specifies HTTP method semantics table covering GET, POST, PUT, PATCH, DELETE with idempotency and success codes — met. Step 3 has a five-column table covering all five methods with idempotency and success codes
- [x] PASS: Skill mandates PATCH semantics using RFC 7396 merge patch with optimistic concurrency (lastUpdatedAt conflict detection) — met. Step 4 names RFC 7396 explicitly, requires `lastUpdatedAt` in the request body, and mandates `409 Conflict` on mismatch
- [x] PASS: Skill requires every list endpoint to support pagination with a defined response shape (items, page, size, totalItems, totalPages) — met. Step 5 shows the exact JSON shape with all five fields
- [x] PASS: Skill specifies error format using RFC 9457 Problem Details with standard status codes and rules against leaking stack traces — met. Step 6 names RFC 9457, provides a full example with the standard fields (`type`, `title`, `status`, `detail`, `instance`), a status-code table covering 400/401/403/404/409/422/429/500, and explicitly bans stack trace exposure
- [x] PASS: Skill provides a versioning strategy section with at least two options and rules for when a new version is required — met. Step 7 gives three strategies (URL prefix, header, no versioning) with a rules block defining breaking vs. additive changes
- [x] PASS: Skill defines authentication requirements — Bearer token with short-lived access tokens and resource-level authorisation — met. Step 8 specifies Bearer tokens, 15-minute access tokens, and "Resource-level authorisation — check ownership, not just role"
- [x] PASS: Skill lists anti-patterns — flat URL namespace, verbs in URLs, silent failures, leaking internal IDs — met. The Anti-Patterns section covers all four explicitly
- [~] PARTIAL: Skill's output format template includes an error catalogue section and a resource hierarchy visual — partially met. Both sections exist in the output template (`## Resource Hierarchy` and `## Error Catalogue`), but `[Visual tree showing URL structure]` specifies no notation or example, leaving agents to invent the format inconsistently

### Output expectations

- [x] PASS: Output is structured as a review of the skill (PASS/FAIL or present/missing per requirement) rather than producing a sample API design — met
- [x] PASS: Output verifies the URL hierarchy rule and quotes or references the specific clause forbidding flat top-level listings — met. The specific clause is quoted above
- [x] PASS: Output verifies the HTTP method semantics table covers all five methods (GET, POST, PUT, PATCH, DELETE) and confirms idempotency is documented per method — met
- [x] PASS: Output checks for RFC 7396 merge patch + optimistic concurrency via `lastUpdatedAt` and 409 Conflict, naming both elements explicitly — met
- [x] PASS: Output verifies the paginated response shape includes all five fields (`items`, `page`, `size`, `totalItems`, `totalPages`) — met
- [x] PASS: Output verifies the error format complies with RFC 9457 Problem Details, with the standard fields (`type`, `title`, `status`, `detail`, `instance`) and a status-code table covering at least 400/401/403/404/409/422/429/500 — met. All five standard fields present in the skill's example; all eight required status codes covered
- [x] PASS: Output verifies the versioning section presents at least two strategies (e.g. URL prefix vs header) with rules for when a new version is required — met
- [x] PASS: Output verifies the authentication section specifies Bearer tokens with short-lived access tokens and resource-level (not just role-level) authorisation — met
- [x] PASS: Output verifies the anti-patterns list covers flat URLs, verbs in URLs, leaking internal IDs, and silent failures — and flags any missing — met. All four present; none missing
- [~] PARTIAL: Output identifies any gaps or weaknesses in the skill (not just confirming presence) — partially met. Gaps identified below

## Notes

Genuine gaps in the skill worth flagging:

**Rate-limit response semantics are missing.** The status-code table includes 429 with the problem type `/problems/rate-limit-exceeded`, but there is no guidance on `Retry-After`, `X-RateLimit-*` headers, or client back-off behaviour. The skill names the problem without specifying the response shape.

**No field-level deprecation pattern.** Step 7 covers whole-version deprecation via the `Sunset` header but says nothing about deprecating individual fields within a version — no `deprecated` marker in schemas, no `Deprecation` response header, no migration timeline for field changes.

**HATEOAS stance is unacknowledged.** The skill is entirely silent on hypermedia links. This is a defensible choice, but leaving it unaddressed means agents will produce inconsistent outputs when the question comes up. One explicit line would close the gap.

**Resource hierarchy visual is underspecified.** `[Visual tree showing URL structure]` in the output template gives no guidance on notation (ASCII tree, table, Mermaid diagram). Agents will produce varied formats across designs.

**Sparse fieldsets are mentioned but not specified.** The anti-patterns section warns against over-fetching and references sparse fieldsets, but neither Step 9 nor the output template shows how to implement them (e.g., `?fields=id,name,createdAt`).

Overall the skill is precise and RFC-accurate. The gaps are real but minor relative to the core coverage.
