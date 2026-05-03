# Api Design

Scenario: Checking that the api-design skill contains the required elements for designing a REST API — resource hierarchy, HTTP semantics, pagination, error format, and versioning guidance.

## Prompt

> Review the api-design skill definition and verify it provides sufficient guidance to produce a well-formed REST API specification.
> 
> In your verification report, confirm or flag each of the following items by name. Quote skill text where present:
> 
> - **URL hierarchy rule** with the specific clause forbidding flat top-level listings of child resources.
> - **HTTP method semantics table** covering ALL FIVE methods (GET, POST, PUT, PATCH, DELETE) with idempotency confirmed per method.
> - **Paginated response shape** with all FIVE fields named: `items`, `page`, `size`, `totalItems`, `totalPages`.
> - **Error format** complies with **RFC 9457 Problem Details** with all five fields (`type`, `title`, `status`, `detail`, `instance`) AND a status-code table covering at minimum: 400, 401, 403, 404, 409, 422, 429, 500.
> - **Versioning strategy** with at least TWO options (e.g. URL prefix `/v2/` vs header `Accept-Version`) and explicit rules for when a new version is required (breaking change vs additive).
> - **Authentication**: Bearer tokens with **short-lived access tokens** AND **resource-level authorisation** (not just role-level RBAC).
> - **Anti-patterns list (4)**: (1) flat URL namespace, (2) verbs in URLs, (3) silent failures, (4) leaking internal IDs.
> - **Output template includes**: an **error catalogue** section AND a **resource hierarchy visual** (tree diagram or similar).
> - **Identified gaps**: any of: missing rate-limit response semantics (`Retry-After` header, 429 body shape), ambiguous HATEOAS guidance, no field-level deprecation pattern.
> 
> Confirm or flag each by name — do not paraphrase.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## API-Design Skill Verification Report

I've reviewed the skill definition at `/Users/martin/.claude/plugins/marketplaces/hpsgd/plugins/engineering/architect/skills/api-design/SKILL.md`. Below is my confirmation or flag for each required item:

---

### ✅ **URL hierarchy rule**
**CONFIRMED** — Step 2, line 28:
> "No flat top-level listings of child resources. `/crawls` does not exist — it is always `/sources/{sourceId}/crawls`"

---

### ✅ **HTTP method semantics table**
**CONFIRMED** — Step 3, lines 44–50. Table covers all five methods with idempotency column:

| Method | Idempotent |
|---|---|
| GET | Yes |
| POST | No |
| PUT | Yes |
| PATCH | Yes* (with RFC 7396 merge semantics) |
| DELETE | Yes |

---

### ✅ **Paginated response shape**
**CONFIRMED** — Step 5, lines 98–107. All five fields present:
```json
{
  "items": [...],
  "page": 1,
  "size": 25,
  "totalItems": 142,
  "totalPages": 6
}
```

---

### ✅ **Error format (RFC 9457 Problem Details)**
**CONFIRMED** — Step 6, lines 113–146.

Five fields all present (lines 114–119):
```json
{
  "type": "...",
  "title": "...",
  "status": 422,
  "detail": "...",
  "instance": "..."
}
```

Status code table covers required codes:

| Status | Codes present |
|---|---|
| 400 ✅ | Bad request |
| 401 ✅ | Unauthorized |
| 403 ✅ | Forbidden |
| 404 ✅ | Not found |
| 409 ✅ | Conflict |
| 422 ✅ | Validation error |
| 429 ✅ | Rate limit exceeded |
| 500 ✅ | Internal error |

---

### ✅ **Versioning strategy**
**CONFIRMED** — Step 7, lines 154–170. Table presents three options:

1. **URL prefix** — `/v1/sources`
2. **Header** — `Accept: application/vnd.api.v2+json`
3. **No versioning** — Additive changes only

Explicit rules for new version (lines 166–169):
> "Additive changes (new fields, new endpoints) do NOT require a new version. Breaking changes (field removal, type change, semantic change) require a new version."

---

### ✅ **Authentication**
**CONFIRMED** — Step 8, lines 172–184:

- **Short-lived access tokens** (line 176): "Tokens are short-lived (15 minutes for access, 7 days for refresh)"
- **Bearer tokens** (line 175): "`Authorization: Bearer <token>`"
- **Resource-level authorisation** (line 182): "Resource-level authorisation — check ownership, not just role"

---

### ✅ **Anti-patterns (4 required)**
**CONFIRMED** — Anti-Patterns section, lines 206–215. All four present with direct language:

1. **Flat URL namespace** (line 208): "`/getAllCrawls` is an RPC, not a REST API"
2. **Verbs in URLs** (line 209): "`/users/123/activate` should be `POST /users/123/activation`"
3. **Silent failures** (line 215): "every error returns an appropriate status code and message"
4. **Leaking internal IDs** (line 212): "use UUIDs or slugs, not auto-increment integers"

---

### ✅ **Output template**
**CONFIRMED** — Output Format section, lines 217–258:

- **Resource Hierarchy visual** (line 222): "`## Resource Hierarchy [Visual tree showing URL structure]`"
- **Error Catalogue** (line 253): "`## Error Catalogue [All custom error types with examples]`"

---

### ❌ **GAPS IDENTIFIED (3)**

1. **Rate-limit response semantics** — The 429 status code is listed (line 145), but the skill provides:
   - ✅ Generic Problem Details structure
   - ❌ **No `Retry-After` header guidance** (format, semantics)
   - ❌ **No rate-limit specific response body fields** (e.g., `retryAfter`, `remainingRequests`, `resetAt`)
   - Recommendation: Add to Step 6 or a new "Rate Limiting" section with 429 response shape

2. **HATEOAS guidance** — Completely absent. No mention of:
   - Hypermedia links in responses (`_links`, `Link` header)
   - State machine guidance (when to include state-transition actions)
   - Recommendation: Either add as optional section ("HATEOAS is not used in this API") OR add guidance if REST maturity is expected

3. **Field-level deprecation pattern** — Missing. Step 7 covers API versioning but not:
   - How to deprecate individual fields (e.g., `Deprecated: 2025-06-01` header)
   - How to signal deprecated fields in responses
   - Sunset timeline per field
   - Recommendation: Add to Step 7 or request/response design rules (Step 9)

---

### Summary

The skill provides **solid, actionable guidance** for designing a well-formed REST API. It covers the core deliverables (hierarchy, methods, pagination, errors, versioning, auth) with clear rules and examples. The output template is structured and reusable.

**The three gaps are not critical blockers** for initial API design, but they become important when:
- APIs require rate limiting (consumer-facing APIs almost always do)
- APIs evolve and need graceful field deprecation (any API > 1 year old)
- Design includes hypermedia links (less common but valuable for discoverability)

**Recommendation**: Expand Step 6 or add two new sections:
1. "Rate Limiting" with 429 response shape and `Retry-After` semantics
2. "Field Deprecation" with timeline and signalling patterns

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/17.0 (94%) |
| Evaluated | 2026-05-03 |
| Target duration | 41128 ms |
| Target cost | $0.1249 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill defines a URL hierarchy rule — resources must be accessed through parent chains, no flat top-level listings of child resources | PASS | Output quotes skill Step 2, line 28: 'No flat top-level listings of child resources. `/crawls` does not exist — it is always `/sources/{sourceId}/crawls`' |
| c2 | Skill specifies HTTP method semantics table covering GET, POST, PUT, PATCH, DELETE with idempotency and success codes | PARTIAL | Output confirms table with all five methods and an idempotency column (Step 3, lines 44–50). No mention of success codes column — the quoted table only shows Method and Idempotent columns, so success codes are not explicitly confirmed in the captured output. |
| c3 | Skill mandates PATCH semantics using RFC 7396 merge patch with optimistic concurrency (lastUpdatedAt conflict detection) | PARTIAL | Output confirms RFC 7396 merge semantics for PATCH via the idempotency table note 'Yes* (with RFC 7396 merge semantics)'. However, `lastUpdatedAt` and optimistic concurrency conflict detection are not quoted or referenced anywhere in the PATCH verification section. |
| c4 | Skill requires every list endpoint to support pagination with a defined response shape (items, page, size, totalItems, totalPages) | PASS | Output confirms Step 5, lines 98–107 with a JSON example showing all five fields: `items`, `page`, `size`, `totalItems`, `totalPages`. |
| c5 | Skill specifies error format using RFC 9457 Problem Details with standard status codes and rules against leaking stack traces | PARTIAL | Output confirms RFC 9457 Problem Details with all five fields and a full status-code table (Step 6, lines 113–146). No mention of stack trace prohibition rules anywhere in the error format section — neither confirmed as present nor flagged as missing. |
| c6 | Skill provides a versioning strategy section with at least two options and rules for when a new version is required | PASS | Output confirms Step 7, lines 154–170 with three versioning options (URL prefix, Accept header, no-versioning additive) and quotes explicit breaking-change rules: 'Additive changes … do NOT require a new version. Breaking changes … require a new version.' |
| c7 | Skill defines authentication requirements — Bearer token with short-lived access tokens and resource-level authorisation | PASS | Output confirms Step 8, lines 172–184: Bearer token (`Authorization: Bearer <token>`), short-lived access tokens (15 minutes), and resource-level authorisation ('check ownership, not just role'). |
| c8 | Skill lists anti-patterns — flat URL namespace, verbs in URLs, silent failures, leaking internal IDs | PASS | Output confirms Anti-Patterns section, lines 206–215, quoting all four: flat URL namespace ('`/getAllCrawls` is an RPC'), verbs in URLs ('`/users/123/activate` should be `POST /users/123/activation`'), silent failures ('every error returns an appropriate status code'), leaking internal IDs ('use UUIDs or slugs, not auto-increment integers'). |
| c9 | Skill's output format template includes an error catalogue section and a resource hierarchy visual | PARTIAL | Output confirms Output Format section, lines 217–258, naming both '`## Resource Hierarchy [Visual tree showing URL structure]`' (line 222) and '`## Error Catalogue [All custom error types with examples]`' (line 253). |
| c10 | Output is structured as a review of the skill (PASS/FAIL or present/missing per requirement) rather than producing a sample API design | PASS | The entire captured output is structured as a verification report with named sections per requirement, each marked CONFIRMED (✅) or flagged (❌), with quoted skill text. No sample API design is produced. |
| c11 | Output verifies the URL hierarchy rule and quotes or references the specific clause forbidding flat top-level listings | PASS | Output quotes verbatim from Step 2, line 28: 'No flat top-level listings of child resources. `/crawls` does not exist — it is always `/sources/{sourceId}/crawls`' |
| c12 | Output verifies the HTTP method semantics table covers all five methods (GET, POST, PUT, PATCH, DELETE) and confirms idempotency is documented per method | PASS | Output shows a reproduced table confirming all five methods (GET, POST, PUT, PATCH, DELETE) each with an explicit Idempotent value, including PATCH noted as 'Yes* (with RFC 7396 merge semantics)'. |
| c13 | Output checks for RFC 7396 merge patch + optimistic concurrency via `lastUpdatedAt` and 409 Conflict, naming both elements explicitly | PARTIAL | Output names RFC 7396 merge patch in the PATCH table row. The string `lastUpdatedAt` does not appear anywhere in the captured output, and the 409 Conflict entry in the error table is not connected to optimistic concurrency — the pairing of lastUpdatedAt + 409 Conflict is not named explicitly as required. |
| c14 | Output verifies the paginated response shape includes all five fields (`items`, `page`, `size`, `totalItems`, `totalPages`) | PASS | Output shows a JSON block from Step 5 with all five fields explicitly named: `items`, `page`, `size`, `totalItems`, `totalPages`. |
| c15 | Output verifies the error format complies with RFC 9457 Problem Details, with the standard fields (`type`, `title`, `status`, `detail`, `instance`) and a status-code table covering at least 400/401/403/404/409/422/429/500 | PASS | Output shows a JSON block with all five RFC 9457 fields and a status-code table explicitly listing 400, 401, 403, 404, 409, 422, 429, and 500 — each with a checkmark. |
| c16 | Output verifies the versioning section presents at least two strategies (e.g. URL prefix vs header) with rules for when a new version is required | PASS | Output confirms three versioning options (URL prefix `/v1/sources`, header `Accept: application/vnd.api.v2+json`, additive-only no-versioning) and quotes the breaking-change vs additive-change rule from lines 166–169. |
| c17 | Output verifies the authentication section specifies Bearer tokens with short-lived access tokens and resource-level (not just role-level) authorisation | PASS | Output quotes three distinct elements: `Authorization: Bearer <token>` (line 175), '15 minutes for access, 7 days for refresh' (line 176), and 'Resource-level authorisation — check ownership, not just role' (line 182) — explicitly contrasting resource-level with role-level. |
| c18 | Output verifies the anti-patterns list covers flat URLs, verbs in URLs, leaking internal IDs, and silent failures — and flags any missing | PASS | Output confirms all four anti-patterns with direct quotes from lines 208–215 and marks none as missing (section is ✅ CONFIRMED). |
| c19 | Output identifies any gaps or weaknesses in the skill (not just confirming presence) — e.g. missing rate-limit response semantics, ambiguous HATEOAS guidance, or no field-level deprecation pattern | PARTIAL | Output identifies exactly three gaps matching the criterion's examples: (1) missing Retry-After header and 429-specific response body fields, (2) HATEOAS guidance 'completely absent', (3) field-level deprecation pattern missing (sunset timelines, Deprecated header). Each gap includes a recommendation. |

### Notes

The captured output is a high-quality verification report that correctly confirms all major skill elements with quoted text and line references. It earns full marks on the presence checks for pagination, error format (RFC 9457 fields + status codes), versioning, authentication, anti-patterns, and output template. It loses half-marks on c2 (success codes column not confirmed in the method table), c3 and c13 (RFC 7396 is named but lastUpdatedAt/optimistic concurrency connection is absent), and c5 (stack trace prohibition not confirmed). The gaps section is excellent — it independently identifies the three weaknesses the test specifically named (rate-limit semantics, HATEOAS, field deprecation), satisfying c19 at its PARTIAL ceiling. The overall review methodology (PASS/FAIL per named requirement, quoted evidence, gap recommendations) is exactly what c10 asks for.
