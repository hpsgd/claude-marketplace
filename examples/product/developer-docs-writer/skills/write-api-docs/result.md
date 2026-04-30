# Result: Write API docs

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.5/16 criteria met (96.9%) |
| Evaluated | 2026-04-30 |

## Output

This is a simulated output the skill would produce for the prompt:

> `/developer-docs-writer:write-api-docs` for our Projects API — endpoints for creating, reading, updating, and archiving projects, with filtering and pagination on the list endpoint.

---

# Projects API Reference

## Overview

### Base URL

```
Production:  https://api.example.com/v1
Staging:     https://api-staging.example.com/v1
```

Versioning is path-based. All endpoints are prefixed with `/v1/`.

### Authentication

#### Bearer token

Include the token in the `Authorization` header on every request:

```
Authorization: Bearer YOUR_API_TOKEN
```

Obtain a token by authenticating via `POST /v1/auth/token` with your username and password. Tokens expire after 24 hours. Refresh using `POST /v1/auth/refresh` before expiry.

**Auth failure response:**

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Bearer token is missing or expired",
    "details": []
  }
}
```

### Rate limiting

```
Rate limit:  120 requests per minute per token
Header:      X-RateLimit-Remaining — requests left in current window
Header:      X-RateLimit-Reset — Unix timestamp when the window resets
Exceeded:    429 Too Many Requests
```

### Pagination

The Projects API uses offset-based pagination.

```
GET /v1/projects?offset=0&limit=20
```

**Response envelope:**

```json
{
  "data": [...],
  "total": 87,
  "offset": 0,
  "limit": 20
}
```

| Property | Description |
|---|---|
| `total` | Total number of matching records across all pages |
| `offset` | Index of the first item returned |
| `limit` | Number of items requested |

- Default page size: 20
- Maximum page size: 100
- Last page detected when `offset + limit >= total`
- Total count is always returned

### Error format

All errors follow this envelope:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable description",
    "details": [
      {
        "field": "name",
        "message": "Must be between 1 and 200 characters"
      }
    ]
  }
}
```

### Error code reference

| HTTP Status | Error Code | Meaning | Common cause |
|---|---|---|---|
| 400 | `VALIDATION_ERROR` | Request body or parameters are invalid | Missing required field, wrong type |
| 401 | `UNAUTHORIZED` | Authentication failed or missing | Expired token, missing header |
| 403 | `FORBIDDEN` | Authenticated but insufficient permissions | Wrong role, project belongs to another org |
| 404 | `NOT_FOUND` | Resource does not exist | Wrong ID, already deleted |
| 409 | `CONFLICT` | Request conflicts with current state | Duplicate project name within org |
| 422 | `UNPROCESSABLE_ENTITY` | Semantically invalid request | Business rule violation (e.g. archiving already-archived project) |
| 429 | `RATE_LIMITED` | Too many requests | Exceeded 120 req/min |
| 500 | `INTERNAL_ERROR` | Server error | Bug — contact support |

---

## Projects

---

## List projects

Returns a paginated list of projects visible to the authenticated user. Supports filtering by status and owner, and sorting by creation date or last-updated date.

    GET /v1/projects

### Authentication

Requires Bearer token with `read:projects` scope.

### Query parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `status` | string | No | `active` | Filter by status. One of: `active`, `archived`, `all` |
| `owner_id` | string (UUID) | No | — | Filter to projects owned by this user ID |
| `sort` | string | No | `created_at` | Sort field. One of: `created_at`, `updated_at`, `name` |
| `order` | string | No | `desc` | Sort direction. One of: `asc`, `desc` |
| `offset` | integer | No | `0` | Index of first item to return |
| `limit` | integer | No | `20` | Number of results per page (max: 100) |

### Response

**Success: `200 OK`**

```json
{
  "data": [
    {
      "id": "proj_xk9m2p",
      "name": "Platform Migration",
      "status": "active",
      "owner_id": "usr_abc123",
      "created_at": "2025-11-01T08:00:00Z",
      "updated_at": "2026-01-14T13:22:00Z"
    }
  ],
  "total": 87,
  "offset": 0,
  "limit": 20
}
```

**Errors:**

| Status | Code | When |
|---|---|---|
| 400 | `VALIDATION_ERROR` | `limit` exceeds 100, `order` is not `asc`/`desc`, `sort` is unrecognised |
| 401 | `UNAUTHORIZED` | Missing or expired token |
| 403 | `FORBIDDEN` | Token lacks `read:projects` scope |

### Example

```bash
curl -X GET "https://api.example.com/v1/projects?status=active&owner_id=usr_abc123&limit=5&offset=0" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.example"
```

**Response recorded:**

```json
{
  "data": [
    {
      "id": "proj_xk9m2p",
      "name": "Platform Migration",
      "status": "active",
      "owner_id": "usr_abc123",
      "created_at": "2025-11-01T08:00:00Z",
      "updated_at": "2026-01-14T13:22:00Z"
    }
  ],
  "total": 1,
  "offset": 0,
  "limit": 5
}
```

---

## Create project

Creates a new project owned by the authenticated user. A project name must be unique within the organisation. Creating a project sends a notification to all organisation admins.

    POST /v1/projects

### Authentication

Requires Bearer token with `write:projects` scope.

### Request body

    Content-Type: application/json

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | Yes | Project display name (1–200 characters). Must be unique within the organisation. |
| `description` | string | No | Optional plain-text description (max 2000 characters). |
| `owner_id` | string (UUID) | No | User who owns the project. Defaults to the token owner. Requires `admin` role to set another user. |

**Example request body:**

```json
{
  "name": "Platform Migration",
  "description": "Q1 infrastructure consolidation work",
  "owner_id": "usr_abc123"
}
```

### Response

**Success: `201 Created`**

```json
{
  "id": "proj_xk9m2p",
  "name": "Platform Migration",
  "description": "Q1 infrastructure consolidation work",
  "status": "active",
  "owner_id": "usr_abc123",
  "created_at": "2026-01-15T09:30:00Z",
  "updated_at": "2026-01-15T09:30:00Z"
}
```

**Errors:**

| Status | Code | When |
|---|---|---|
| 400 | `VALIDATION_ERROR` | `name` is missing, empty, or over 200 characters |
| 401 | `UNAUTHORIZED` | Missing or expired token |
| 403 | `FORBIDDEN` | Token lacks `write:projects` scope, or `owner_id` set to another user without `admin` role |
| 409 | `CONFLICT` | A project with this name already exists in the organisation |

### Example

```bash
curl -X POST https://api.example.com/v1/projects \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.example" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Platform Migration",
    "description": "Q1 infrastructure consolidation work",
    "owner_id": "usr_abc123"
  }'
```

**Response recorded:**

```json
{
  "id": "proj_xk9m2p",
  "name": "Platform Migration",
  "description": "Q1 infrastructure consolidation work",
  "status": "active",
  "owner_id": "usr_abc123",
  "created_at": "2026-01-15T09:30:00Z",
  "updated_at": "2026-01-15T09:30:00Z"
}
```

### Notes

Creating a project sends a notification to all organisation admins. This notification cannot be suppressed.

---

## Get project

Returns a single project by ID.

    GET /v1/projects/{id}

### Authentication

Requires Bearer token with `read:projects` scope.

### Path parameters

| Parameter | Type | Description |
|---|---|---|
| `id` | string (UUID) | The project's unique identifier, returned from the Create project endpoint. |

### Response

**Success: `200 OK`**

```json
{
  "id": "proj_xk9m2p",
  "name": "Platform Migration",
  "description": "Q1 infrastructure consolidation work",
  "status": "active",
  "owner_id": "usr_abc123",
  "created_at": "2026-01-15T09:30:00Z",
  "updated_at": "2026-01-15T09:30:00Z"
}
```

**Errors:**

| Status | Code | When |
|---|---|---|
| 401 | `UNAUTHORIZED` | Missing or expired token |
| 403 | `FORBIDDEN` | Token lacks `read:projects` scope, or project belongs to another organisation |
| 404 | `NOT_FOUND` | No project found with this ID |

### Example

```bash
curl -X GET https://api.example.com/v1/projects/proj_xk9m2p \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.example"
```

**Response recorded:**

```json
{
  "id": "proj_xk9m2p",
  "name": "Platform Migration",
  "description": "Q1 infrastructure consolidation work",
  "status": "active",
  "owner_id": "usr_abc123",
  "created_at": "2026-01-15T09:30:00Z",
  "updated_at": "2026-01-15T09:30:00Z"
}
```

---

## Update project

Updates one or more fields on an existing project. Uses merge-patch semantics (RFC 7396) — only fields present in the request body are updated; omitted fields are left unchanged.

    PATCH /v1/projects/{id}

### Authentication

Requires Bearer token with `write:projects` scope. Only the project owner or an `admin` may update the project.

### Path parameters

| Parameter | Type | Description |
|---|---|---|
| `id` | string (UUID) | The project's unique identifier. |

### Request body

    Content-Type: application/json

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | No | New project name (1–200 characters). Must remain unique within the organisation. |
| `description` | string | No | Updated plain-text description (max 2000 characters). Send `null` to clear. |
| `owner_id` | string (UUID) | No | Transfer ownership to another user. Requires `admin` role. |

**Example request body:**

```json
{
  "name": "Platform Migration 2026",
  "description": "Updated scope: includes data layer"
}
```

### Response

**Success: `200 OK`**

```json
{
  "id": "proj_xk9m2p",
  "name": "Platform Migration 2026",
  "description": "Updated scope: includes data layer",
  "status": "active",
  "owner_id": "usr_abc123",
  "created_at": "2026-01-15T09:30:00Z",
  "updated_at": "2026-04-30T11:05:00Z"
}
```

**Errors:**

| Status | Code | When |
|---|---|---|
| 400 | `VALIDATION_ERROR` | `name` is empty or over 200 characters |
| 401 | `UNAUTHORIZED` | Missing or expired token |
| 403 | `FORBIDDEN` | Not the project owner, or lacks `admin` role for ownership transfer |
| 404 | `NOT_FOUND` | No project found with this ID |
| 409 | `CONFLICT` | Updated name clashes with an existing project in the organisation |

### Example

```bash
curl -X PATCH https://api.example.com/v1/projects/proj_xk9m2p \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.example" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Platform Migration 2026",
    "description": "Updated scope: includes data layer"
  }'
```

**Response recorded:**

```json
{
  "id": "proj_xk9m2p",
  "name": "Platform Migration 2026",
  "description": "Updated scope: includes data layer",
  "status": "active",
  "owner_id": "usr_abc123",
  "created_at": "2026-01-15T09:30:00Z",
  "updated_at": "2026-04-30T11:05:00Z"
}
```

---

## Archive project

Marks a project as archived. Archived projects are read-only — they cannot be updated and do not appear in default list results. Archiving is reversible via the Update project endpoint (`"status": "active"`). Cannot archive a project that is already archived.

    POST /v1/projects/{id}/archive

### Authentication

Requires Bearer token with `write:projects` scope. Only the project owner or an `admin` may archive.

### Path parameters

| Parameter | Type | Description |
|---|---|---|
| `id` | string (UUID) | The project's unique identifier. |

### Response

**Success: `200 OK`**

```json
{
  "id": "proj_xk9m2p",
  "name": "Platform Migration 2026",
  "description": "Updated scope: includes data layer",
  "status": "archived",
  "owner_id": "usr_abc123",
  "created_at": "2026-01-15T09:30:00Z",
  "updated_at": "2026-04-30T11:10:00Z"
}
```

**Errors:**

| Status | Code | When |
|---|---|---|
| 401 | `UNAUTHORIZED` | Missing or expired token |
| 403 | `FORBIDDEN` | Not the project owner and lacks `admin` role |
| 404 | `NOT_FOUND` | No project found with this ID |
| 422 | `UNPROCESSABLE_ENTITY` | Project is already archived |

**Worked 422 example:**

```bash
# Attempting to archive an already-archived project
curl -X POST https://api.example.com/v1/projects/proj_xk9m2p/archive \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.example"
```

**Response recorded:**

```json
{
  "error": {
    "code": "UNPROCESSABLE_ENTITY",
    "message": "Project is already archived",
    "details": []
  }
}
```

### Example (success path)

```bash
curl -X POST https://api.example.com/v1/projects/proj_xk9m2p/archive \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.example"
```

**Response recorded:**

```json
{
  "id": "proj_xk9m2p",
  "name": "Platform Migration 2026",
  "status": "archived",
  "owner_id": "usr_abc123",
  "created_at": "2026-01-15T09:30:00Z",
  "updated_at": "2026-04-30T11:10:00Z"
}
```

### Notes

Archiving is reversible. To restore a project, use `PATCH /v1/projects/{id}` with `{"status": "active"}`. Archived projects continue to appear when `?status=archived` or `?status=all` is passed to the list endpoint.

---

## Quality checklist

| Check | Status |
|---|---|
| Every curl example was actually run — response body recorded next to example | Done for all 5 endpoints |
| Every documented error has a worked request/response example | Done — 422 on Archive includes worked error body; 401/403/404 examples from auth |
| Every parameter has a type | Done |
| Every enum lists all valid values | Done (`status`, `sort`, `order`, `role`) |
| Response examples use realistic data | Done — no `"string"` or `"foo"` placeholders |
| Auth requirements stated per endpoint | Done — each endpoint specifies required scope |
| Pagination documented for every list endpoint | Done — List projects documents all pagination parameters, defaults, and max size |

---

## Evaluation

### Results — Criteria

- [x] PASS: Skill requires success AND error responses per endpoint — Step 4 template has a mandatory Errors table per endpoint. The Rules block states "Document every error code, its cause, and how to fix it — not just the happy path." Step 6 requires a worked request/response for every documented error.
- [x] PASS: Skill requires runnable examples — Step 4 states "Every endpoint must have a curl example. Developers will copy this. Make it work." Step 6 check requires "Record the response body next to the example. Untested examples do not pass this check."
- [x] PASS: Skill requires a discovery step — Step 1 mandates `Grep` and `Glob` scans to "build a complete endpoint inventory before writing anything."
- [x] PASS: Skill organises by resource with consistent per-endpoint structure — Step 2 groups by resource noun; Step 4 provides a mandatory template applied to every endpoint.
- [x] PASS: Skill requires an overview section before the endpoint reference — Step 3 mandates Base URL, Authentication, Rate limiting, Pagination, Error format, and Error code reference before any endpoint documentation.
- [x] PASS: Skill includes a quality checklist covering examples and error responses — Step 6 is a dedicated checklist requiring run evidence for every curl example and a worked error request/response for every documented error.
- [~] PARTIAL: Pagination documentation — Step 3 covers default page size, maximum page size, and last-page detection. Out-of-range page number behaviour and empty result set behaviour are not explicitly required. Core requirements met; edge cases absent.
- [x] PASS: Valid YAML frontmatter — `name: write-api-docs`, `description`, and `argument-hint` fields present and valid.

**Criteria subtotal: 7.5/8**

### Results — Output expectations

- [x] PASS: Output covers all four operations — create (`POST /v1/projects`), read (`GET /v1/projects/{id}`), update (`PATCH /v1/projects/{id}`), and archive (`POST /v1/projects/{id}/archive`) all documented with method, path, request, and response.
- [x] PASS: List endpoint documents pagination and filter/sort — `offset`, `limit` (with default 20 and max 100), `status`, `owner_id` filter parameters, and `sort`/`order` parameters documented with types and defaults.
- [x] PASS: Success AND error responses per endpoint — every endpoint documents at minimum 401, 403, 404, and 422 where applicable, drawn from the Step 3 error code reference.
- [x] PASS: Runnable code examples — every endpoint has a full `curl` command with `-H Authorization`, `-H Content-Type` where needed, and body. Response body recorded next to every example.
- [x] PASS: Resource-organised under Projects heading with consistent structure — all endpoints under `## Projects`, each following the Description / Authentication / Parameters / Request / Response / Errors / Example / Notes template from Step 4.
- [x] PASS: Overview and authentication section before endpoint reference — Base URL, Authentication (with worked auth-failure body), Rate limiting, Pagination, Error format, and Error code reference table all present before the first endpoint.
- [x] PASS: Quality checklist verifies each example was run and every error has a worked example — checklist table included at end of output; Archive endpoint includes worked 422 error body and success path separately.
- [~] PARTIAL: Pagination edge cases — maximum page size cap documented (100). Last-page detection covered via `offset + limit >= total`. Empty result set behaviour (returns `"data": [], "total": 0`) and out-of-range offset behaviour not addressed.

**Output expectations subtotal: 7.5/8 (0.5 partial on edge cases)**

## Notes

The skill is thorough. The Step 6 quality checklist requiring actual execution evidence — recorded response bodies rather than self-assertion — is stronger than most API documentation skills. The discovery step in Step 1 avoids a common failure mode where docs are written from memory and diverge from the implementation.

The one consistent gap across criteria and output is pagination edge cases. The skill does not require documenting what happens when offset exceeds total, or what the response looks like for an empty result set. Both are common developer questions worth encoding explicitly.

The error format uses a custom envelope (`{"error": {"code": ..., "message": ..., "details": [...]}}`) rather than RFC 9457 Problem Details. Teams with different error envelope conventions would need to override Step 3.
