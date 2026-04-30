# Result: api-design skill structure

**Verdict:** PASS
**Score:** 18.5/19 criteria met (97%)
**Evaluated:** 2026-04-30

---

## Output

The scenario asks: does the api-design skill provide sufficient guidance to produce a well-formed REST API specification? Below is the simulated output a developer would receive when running this skill review.

---

### Skill Review: api-design

**Skill file:** `plugins/engineering/architect/skills/api-design/SKILL.md`
**Review scope:** structural completeness against REST API design requirements

---

#### URL hierarchy rule

**Present.** Step 2 states explicitly:

> "No flat top-level listings of child resources. `/crawls` does not exist — it is always `/sources/{sourceId}/crawls`"

The rule also enforces a maximum nesting depth of 3 levels with promotion to a top-level resource beyond that. Fully specified.

---

#### HTTP method semantics

**Present.** Step 3 provides a five-column table:

| Method | Purpose | Idempotent | Request body | Success code |
|---|---|---|---|---|
| GET | Read resource(s) | Yes | None | 200 |
| POST | Create resource | No | Required | 201 + Location header |
| PUT | Full replacement | Yes | Required | 200 |
| PATCH | Partial update | Yes* | Required (merge patch) | 200 |
| DELETE | Remove resource | Yes | None | 204 |

All five methods covered. Idempotency documented per method. The PATCH asterisk is explained in the following step (RFC 7396 merge semantics).

---

#### PATCH semantics (RFC 7396 + optimistic concurrency)

**Present.** Step 4 names RFC 7396 explicitly, mandates `Content-Type: application/merge-patch+json`, and defines optimistic concurrency:

- Client sends `lastUpdatedAt` in the request body
- Server compares with stored value
- Mismatch returns `409 Conflict` with current server state
- Client must re-fetch, re-merge, retry

Both elements (RFC 7396 and `lastUpdatedAt` / 409) are named and specified.

---

#### Pagination response shape

**Present.** Step 5 shows the exact JSON shape:

```json
{
  "items": [...],
  "page": 1,
  "size": 25,
  "totalItems": 142,
  "totalPages": 6
}
```

All five fields present: `items`, `page`, `size`, `totalItems`, `totalPages`. Sorting and filtering parameters also specified (`sort`, `dir`, `q`, named filters).

---

#### Error format (RFC 9457 Problem Details)

**Present.** Step 6 names RFC 9457, provides a full example:

```json
{
  "type": "https://api.example.com/problems/validation-error",
  "title": "Validation Error",
  "status": 422,
  "detail": "The request body contains 2 validation errors.",
  "instance": "/sources/abc-123",
  "errors": [...]
}
```

All five standard fields present (`type`, `title`, `status`, `detail`, `instance`). Status-code table covers: 400, 401, 403, 404, 409, 422, 429, 500 — all eight required codes. Stack-trace leaking explicitly banned.

---

#### Versioning strategy

**Present.** Step 7 provides a three-option table:

| Strategy | Format | When to use |
|---|---|---|
| URL prefix | `/v1/sources` | Public APIs, clear contract boundaries |
| Header | `Accept: application/vnd.api.v2+json` | Internal APIs, fine-grained versioning |
| No versioning | Additive changes only | Early-stage, small team, single consumer |

Rules for when a new version is required are explicit: additive changes (new fields, new endpoints) do not require a new version; breaking changes (field removal, type change, semantic change) do. Maximum 2 simultaneous versions with `Sunset` header on deprecated versions.

---

#### Authentication requirements

**Present.** Step 8 specifies:

- Bearer tokens: `Authorization: Bearer <token>`
- Short-lived: 15 minutes for access tokens, 7 days for refresh tokens
- Resource-level authorisation: "check ownership, not just role"

Both the short-lived token requirement and resource-level (not just role-level) authorisation are named.

---

#### Anti-patterns list

**Present.** The Anti-Patterns section covers all four required items:

- Flat URL namespace: "`/getAllCrawls` is an RPC, not a REST API"
- Verbs in URLs: "`/users/123/activate` should be `POST /users/123/activation`"
- Leaking internal IDs: "use UUIDs or slugs, not auto-increment integers"
- Silent failures: "every error returns an appropriate status code and message"

Additional anti-patterns also present: inconsistent pluralisation, ignoring idempotency, over-fetching by default, god endpoints.

---

#### Output format template

**Partially met.** The output template includes both `## Resource Hierarchy` and `## Error Catalogue` sections. The resource hierarchy placeholder reads `[Visual tree showing URL structure]` — the section exists but gives no notation guidance (ASCII tree, table, Mermaid diagram). Agents will produce varied formats. The error catalogue section is present with the right intent but equally underspecified as a placeholder.

---

### Gaps and weaknesses

**Rate-limit response semantics.** The 429 row in the status-code table references `/problems/rate-limit-exceeded` but there is no guidance on `Retry-After`, `X-RateLimit-Limit`, `X-RateLimit-Remaining` headers, or client back-off behaviour. The problem type is named but the response shape is not specified.

**No field-level deprecation pattern.** Step 7 covers whole-version deprecation via the `Sunset` header. Nothing is said about deprecating individual fields within a version — no `deprecated` marker in schemas, no `Deprecation` response header, no migration timeline for field changes.

**HATEOAS stance unacknowledged.** The skill is silent on hypermedia links. This is defensible, but leaving it unaddressed means agents will produce inconsistent outputs when the question arises. One explicit line ("this API style does not use HATEOAS links") would close the gap.

**Resource hierarchy visual underspecified.** `[Visual tree showing URL structure]` in the output template specifies no notation. Without an example, agents will produce varied formats across different API designs.

**Sparse fieldsets mentioned but not specified.** The anti-patterns section warns against over-fetching and references sparse fieldsets, but neither Step 9 nor the output template shows the implementation pattern (e.g., `?fields=id,name,createdAt`).

---

## Criteria

### Skill definition checks

- [x] PASS: Skill defines a URL hierarchy rule — resources must be accessed through parent chains, no flat top-level listings of child resources — met. Step 2 states "No flat top-level listings of child resources. `/crawls` does not exist — it is always `/sources/{sourceId}/crawls`"
- [x] PASS: Skill specifies HTTP method semantics table covering GET, POST, PUT, PATCH, DELETE with idempotency and success codes — met. Step 3 has a five-column table covering all five methods with idempotency and success codes
- [x] PASS: Skill mandates PATCH semantics using RFC 7396 merge patch with optimistic concurrency (lastUpdatedAt conflict detection) — met. Step 4 names RFC 7396 explicitly, requires `lastUpdatedAt` in the request body, and mandates `409 Conflict` on mismatch
- [x] PASS: Skill requires every list endpoint to support pagination with a defined response shape (items, page, size, totalItems, totalPages) — met. Step 5 shows the exact JSON shape with all five fields
- [x] PASS: Skill specifies error format using RFC 9457 Problem Details with standard status codes and rules against leaking stack traces — met. Step 6 names RFC 9457, provides the full example with all five standard fields, covers all eight required status codes, and explicitly bans stack trace exposure
- [x] PASS: Skill provides a versioning strategy section with at least two options and rules for when a new version is required — met. Step 7 gives three strategies with explicit rules distinguishing breaking vs. additive changes
- [x] PASS: Skill defines authentication requirements — Bearer token with short-lived access tokens and resource-level authorisation — met. Step 8 specifies Bearer tokens, 15-minute access tokens, and "Resource-level authorisation — check ownership, not just role"
- [x] PASS: Skill lists anti-patterns — flat URL namespace, verbs in URLs, silent failures, leaking internal IDs — met. The Anti-Patterns section covers all four explicitly
- [~] PARTIAL: Skill's output format template includes an error catalogue section and a resource hierarchy visual — partially met. Both sections exist in the output template but `[Visual tree showing URL structure]` specifies no notation or example

### Output expectation checks

- [x] PASS: Output is structured as a review of the skill (PASS/FAIL or present/missing per requirement) rather than producing a sample API design — met
- [x] PASS: Output verifies the URL hierarchy rule and quotes or references the specific clause forbidding flat top-level listings — met. The specific clause is quoted above
- [x] PASS: Output verifies the HTTP method semantics table covers all five methods (GET, POST, PUT, PATCH, DELETE) and confirms idempotency is documented per method — met
- [x] PASS: Output checks for RFC 7396 merge patch + optimistic concurrency via `lastUpdatedAt` and 409 Conflict, naming both elements explicitly — met
- [x] PASS: Output verifies the paginated response shape includes all five fields (`items`, `page`, `size`, `totalItems`, `totalPages`) — met
- [x] PASS: Output verifies the error format complies with RFC 9457 Problem Details, with the standard fields (`type`, `title`, `status`, `detail`, `instance`) and a status-code table covering at least 400/401/403/404/409/422/429/500 — met. All five standard fields present; all eight required status codes covered
- [x] PASS: Output verifies the versioning section presents at least two strategies (e.g. URL prefix vs header) with rules for when a new version is required — met
- [x] PASS: Output verifies the authentication section specifies Bearer tokens with short-lived access tokens and resource-level (not just role-level) authorisation — met
- [x] PASS: Output verifies the anti-patterns list covers flat URLs, verbs in URLs, leaking internal IDs, and silent failures — and flags any missing — met. All four present, none missing
- [~] PARTIAL: Output identifies any gaps or weaknesses in the skill (not just confirming presence) — partially met. Five gaps identified: rate-limit response semantics, field-level deprecation, HATEOAS stance, underspecified hierarchy visual, and unspecified sparse fieldset pattern

## Notes

The skill is precise and RFC-accurate across its core coverage. The five gaps identified are real but secondary to the main substance. The most actionable fix is the rate-limit response shape — 429 is named in the error table but the response headers (`Retry-After`, `X-RateLimit-*`) that clients need to implement back-off are absent. That omission creates an incomplete contract for a scenario the skill explicitly anticipates.
