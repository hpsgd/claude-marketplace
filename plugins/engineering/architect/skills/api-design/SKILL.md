---
name: api-design
description: Design an API — resource hierarchy, endpoints, request/response shapes, error handling, and pagination.
argument-hint: "[API or resource to design]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Design an API for $ARGUMENTS.

## Process (sequential — do not skip steps)

### Step 1: Resource Identification

Before designing endpoints, identify the domain resources:

1. List every noun in the domain (users, orders, products, invoices)
2. Identify ownership relationships — which resources belong to which?
3. Determine resource lifecycle — how is each created, read, updated, deleted?
4. Identify cross-cutting resources (audit logs, notifications) that are read-only

### Step 2: URL Hierarchy Design

URLs MUST mirror entity ownership. Every resource is accessed through its parent chain.

**Rules:**
- Hierarchical: `/sources/{sourceId}/crawls/{crawlId}/pages/{pageId}`
- No flat top-level listings of child resources. `/crawls` does not exist — it is always `/sources/{sourceId}/crawls`
- Collection nouns are plural: `/users`, not `/user`
- Resource identifiers use `{camelCaseId}` in the path
- Maximum nesting depth: 3 levels. Beyond that, promote to a top-level resource with a reference
- No verbs in URLs. Use HTTP methods for actions: `POST /orders/{id}/cancellation`, not `POST /orders/{id}/cancel`

**URL anatomy:**
```
/{resource}                    → collection
/{resource}/{id}               → single item
/{resource}/{id}/{sub}         → sub-collection
/{resource}/{id}/{sub}/{subId} → single sub-item
```

### Step 3: HTTP Method Semantics

| Method | Purpose | Idempotent | Request body | Success code |
|---|---|---|---|---|
| GET | Read resource(s) | Yes | None | 200 |
| POST | Create resource | No | Required | 201 + Location header |
| PUT | Full replacement | Yes | Required | 200 |
| PATCH | Partial update | Yes* | Required (merge patch) | 200 |
| DELETE | Remove resource | Yes | None | 204 |

*PATCH is idempotent when using RFC 7396 merge semantics (the default for this API style).

### Step 4: PATCH Semantics (RFC 7396 Merge Patch)

All PATCH operations use JSON Merge Patch (`Content-Type: application/merge-patch+json`):

- **Set a field:** include the field with new value: `{"name": "New Name"}`
- **Remove a field:** set it to null: `{"description": null}`
- **Leave a field unchanged:** omit it from the payload
- **Arrays are replaced wholesale** — no partial array updates via merge patch

Optimistic concurrency is MANDATORY for all PATCH and PUT operations:
- Client sends `lastUpdatedAt` in the request body
- Server compares with stored value
- If mismatch: return `409 Conflict` with the current server state
- Client must re-fetch, re-merge, and retry

### Step 5: Pagination, Sorting, and Filtering

Every list endpoint MUST support:

**Pagination:**
```
GET /sources?page=1&size=25
```
- `page` — 1-indexed page number (default: 1)
- `size` — items per page (default: 25, max: 100)
- Response includes pagination metadata (see response format below)

**Sorting:**
```
GET /sources?sort=createdAt&dir=desc
```
- `sort` — field name to sort by (must be from an allowlist)
- `dir` — `asc` or `desc` (default: sensible for the resource, usually `desc` for time-based, `asc` for alphabetical)
- Every list endpoint has a sensible default sort (document it)

**Filtering:**
```
GET /sources?q=search+term&status=active&createdAfter=2024-01-01
```
- `q` — general text search (searches across predefined fields)
- Named filters for common filter dimensions (status, type, date ranges)
- Date filters use ISO 8601 format
- Multiple values for the same filter: `?status=active&status=pending` (OR semantics)

**Paginated response format:**
```json
{
  "items": [...],
  "page": 1,
  "size": 25,
  "totalItems": 142,
  "totalPages": 6
}
```

### Step 6: Error Format (Problem Details — RFC 9457)

All errors use the Problem Details format:

```json
{
  "type": "https://api.example.com/problems/validation-error",
  "title": "Validation Error",
  "status": 422,
  "detail": "The request body contains 2 validation errors.",
  "instance": "/sources/abc-123",
  "errors": [
    {
      "field": "name",
      "message": "Name must be between 1 and 255 characters.",
      "code": "STRING_LENGTH"
    },
    {
      "field": "url",
      "message": "URL must be a valid HTTP or HTTPS URL.",
      "code": "INVALID_FORMAT"
    }
  ]
}
```

**Standard error codes:**

| Status | When | Type suffix |
|---|---|---|
| 400 | Malformed request (bad JSON, wrong type) | `/problems/bad-request` |
| 401 | Missing or invalid authentication | `/problems/unauthorized` |
| 403 | Authenticated but not authorised | `/problems/forbidden` |
| 404 | Resource not found | `/problems/not-found` |
| 409 | Optimistic concurrency conflict | `/problems/conflict` |
| 422 | Valid JSON but fails business validation | `/problems/validation-error` |
| 429 | Rate limit exceeded | `/problems/rate-limit-exceeded` |
| 500 | Server error (never leak internals) | `/problems/internal-error` |

**Rules:**
- Never expose stack traces, internal paths, or database details in error responses
- 4xx errors include enough detail for the client to fix the request
- 5xx errors are generic — log the detail server-side, return a correlation ID to the client
- Validation errors list ALL failing fields, not just the first one

### Step 7: Versioning Strategy

Choose one and apply consistently:

| Strategy | Format | When to use |
|---|---|---|
| URL prefix | `/v1/sources` | Public APIs, clear contract boundaries |
| Header | `Accept: application/vnd.api.v2+json` | Internal APIs, fine-grained versioning |
| No versioning | Additive changes only | Early-stage, small team, single consumer |

**Rules:**
- Additive changes (new fields, new endpoints) do NOT require a new version
- Breaking changes (field removal, type change, semantic change) require a new version
- Support at most 2 versions simultaneously. Deprecate with a timeline
- Sunset header on deprecated versions: `Sunset: Sat, 01 Mar 2025 00:00:00 GMT`

### Step 8: Authentication and Authorisation

**Authentication:**
- Bearer tokens in the `Authorization` header: `Authorization: Bearer <token>`
- Tokens are short-lived (15 minutes for access, 7 days for refresh)
- Token refresh via `POST /auth/token/refresh`
- API keys for service-to-service communication (long-lived, scoped)

**Authorisation:**
- Every endpoint documents required permissions
- Resource-level authorisation — check ownership, not just role
- Admin endpoints under a separate path prefix or require explicit scope
- Never rely solely on client-side authorisation checks

### Step 9: Request/Response Design Rules

**Naming:**
- Field names use `camelCase` in JSON
- Consistent naming across all resources (`createdAt`, not sometimes `created_at`)
- Boolean fields use `is`/`has`/`can` prefix: `isActive`, `hasChildren`
- Date fields use ISO 8601 with timezone: `2024-03-15T14:30:00Z`

**Response shape:**
- Single resource: return the resource object directly (not wrapped)
- Collection: return `{ items: [...], page, size, totalItems, totalPages }`
- Create: return the created resource + `Location` header
- Update: return the updated resource
- Delete: return `204 No Content` (no body)

**Envelope avoidance:**
- Do NOT wrap responses in `{ data: ..., success: true }` envelopes
- Use HTTP status codes for success/failure signalling
- Use headers for metadata (pagination links, rate limit info)

## Anti-Patterns (NEVER do these)

- **Flat URL namespace** — `/getAllCrawls` is an RPC, not a REST API. Use hierarchical resources
- **Verbs in URLs** — `/users/123/activate` should be `POST /users/123/activation`
- **Inconsistent pluralisation** — pick plural for collections and stick with it
- **Ignoring idempotency** — PUT and DELETE must be safe to retry
- **Leaking internal IDs** — use UUIDs or slugs, not auto-increment integers
- **Over-fetching by default** — return a reasonable default set of fields; use sparse fieldsets or separate endpoints for detailed views
- **God endpoints** — one endpoint that accepts a `type` parameter and does 10 different things
- **Silent failures** — every error returns an appropriate status code and message

## Output Format

```markdown
# API Design: [name]

## Resource Hierarchy
[Visual tree showing URL structure]

## Authentication
[Scheme and token lifecycle]

## Endpoints

### [Resource Name]

| Method | Path | Description | Auth |
|---|---|---|---|
| GET | /resources | List resources (paginated) | Bearer |
| POST | /resources | Create resource | Bearer |
| GET | /resources/{id} | Get resource | Bearer |
| PATCH | /resources/{id} | Update resource | Bearer |
| DELETE | /resources/{id} | Delete resource | Bearer + Owner |

#### GET /resources
**Parameters:**
[Table: name, location (query/path/header), type, required, description]

**Response 200:**
```json
[example with realistic data]
```

**Errors:** [table of possible error codes with examples]

[Repeat for each endpoint]

## Error Catalogue
[All custom error types with examples]

## Versioning
[Strategy and migration plan]
```
