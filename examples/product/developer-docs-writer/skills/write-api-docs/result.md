# Write Api Docs

Scenario: Testing whether the write-api-docs skill requires complete request/response examples, error documentation, and a quality checklist that includes running every code example.

## Prompt

> /developer-docs-writer:write-api-docs for our Projects API — endpoints for creating, reading, updating, and archiving projects, with filtering and pagination on the list endpoint.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

API reference written to `docs/api/projects.md`. It covers:

- **5 endpoints**: List (with `status`, `owner_id`, `q` filters and cursor pagination), Create, Get, Update (PATCH), Archive
- **Overview sections**: base URL, Bearer token auth with expiry/refresh, rate limiting headers, cursor-based pagination, standard error format, and full error code table
- **Every endpoint** has: auth requirement, typed parameters with all enums listed, realistic JSON examples, curl commands, per-endpoint error tables, and notes on side effects and idempotency

> **Note:** The repo contained no source code, so this document is based on the endpoint description you provided rather than derived from an implementation. You'll want to reconcile field names, ID formats, status enums, and auth details against the real codebase before publishing.

### Artifacts written

#### `work/docs/api/projects.md`

```
# Projects API

The Projects API lets you create and manage projects, list them with filtering, and archive them when they're no longer active.

## Base URL

```
Production: https://api.example.com/v1
Staging:    https://api-staging.example.com/v1
```

The API version is included in the path. All endpoints documented here are under `/v1`.

## Authentication

All endpoints require a Bearer token.

```
Authorization: Bearer YOUR_API_TOKEN
```

Obtain a token by posting credentials to `POST /v1/auth/token`. Tokens expire after 24 hours. Refresh before expiry by calling `POST /v1/auth/token/refresh` with your current token.

When authentication fails, you get:

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Token is missing or invalid"
  }
}
```

## Rate limiting

1,000 requests per hour per token. Each response includes these headers:

| Header | Value |
|---|---|
| `X-RateLimit-Limit` | Total requests allowed per window |
| `X-RateLimit-Remaining` | Requests left in the current window |
| `X-RateLimit-Reset` | Unix timestamp when the window resets |

Exceeded responses return `429 Too Many Requests`.

## Pagination

List endpoints use cursor-based pagination.

```
GET /v1/projects?limit=20&cursor=csr_abc123
```

Response:

```json
{
  "data": [...],
  "next_cursor": "csr_def456",
  "has_more": true
}
```

| Parameter | Default | Max | Notes |
|---|---|---|---|
| `limit` | 20 | 100 | Number of items per page |
| `cursor` | — | — | Omit on the first request; use `next_cursor` from the previous response |

When `has_more` is `false`, you've reached the last page. `next_cursor` is `null` on the last page.

## Error format

All errors follow this structure:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable description",
    "details": [
      {
        "field": "name",
        "message": "This field is required"
      }
    ]
  }
}
```

The `details` array is only present for validation errors. All other error types return just `code` and `message`.

### Error codes

| HTTP status | Code | When |
|---|---|---|
| 400 | `VALIDATION_ERROR` | Request body or parameters are invalid — missing required field, wrong type, value out of range |
| 401 | `UNAUTHORIZED` | Token is missing, expired, or invalid |
| 403 | `FORBIDDEN` | Token is valid but lacks permission to access this resource |
| 404 | `NOT_FOUND` | Project ID does not exist or has been deleted |
| 409 | `CONFLICT` | A project with that name already exists in this workspace |
| 422 | `UNPROCESSABLE_ENTITY` | Request is well-formed but violates a business rule — for example, archiving a project that is already archived |
| 429 | `RATE_LIMITED` | Rate limit exceeded |
| 500 | `INTERNAL_ERROR` | Server error. If this persists, contact support |

---

## List projects

Returns a paginated list of projects. Supports filtering by status and owner, and full-text search on name and description.

```
GET /v1/projects
```

### Authentication

Requires a Bearer token. Returns only projects accessible to the authenticated user.

### Query parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `status` | string | No | — | Filter by status. One of: `active`, `archived`. Omit to return both |
| `owner_id` | string (UUID) | No | — | Filter to projects owned by this user ID |
| `q` | string | No | — | Full-text search on project name and description. Minimum 2 characters |
| `limit` | integer | No | 20 | Results per page. Maximum 100 |
| `cursor` | string | No | — | Pagination cursor from a previous response. Omit for the first page |

### Response

**Success: `200 OK`**

```json
{
  "data": [
    {
      "id": "proj_a1b2c3d4e5f6",
      "name": "Website Redesign",
      "description": "Q3 refresh of the marketing site",
      "status": "active",
      "owner_id": "usr_9z8y7x6w5v4u",
      "created_at": "2026-01-10T08:00:00Z",
      "updated_at": "2026-03-15T14:22:00Z",
      "archived_at": null
    },
    {
      "id": "proj_b2c3d4e5f6a1",
      "name": "API v2 Migration",
      "description": null,
      "status": "active",
      "owner_id": "usr_9z8y7x6w5v4u",
      "created_at": "2026-02-01T10:30:00Z",
      "updated_at": "2026-02-01T10:30:00Z",
      "archived_at": null
    }
  ],
  "next_cursor": "csr_xk92mP3qR7",
  "has_more": true
}
```

**Errors:**

| Status | Code | When |
|---|---|---|
| 400 | `VALIDATION_ERROR` | `status` is not one of the allowed values, or `q` is under 2 characters |
| 401 | `UNAUTHORIZED` | Token is missing or invalid |

### Example

```bash
curl https://api.example.com/v1/projects?status=active&limit=20 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Create a project

Creates a new project. Project names must be unique within your workspace.

```
POST /v1/projects
```

### Authentication

Requires a Bearer token.

### Request body

```
Content-Type: application/json
```

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | Yes | Project name. Between 1 and 200 characters. Must be unique within the workspace |
| `description` | string | No | Optional description. Maximum 2,000 characters |
| `owner_id` | string (UUID) | No | User ID to assign as project owner. Defaults to the authenticated user |

**Example request body:**

```json
{
  "name": "Website Redesign",
  "description": "Q3 refresh of the marketing site",
  "owner_id": "usr_9z8y7x6w5v4u"
}
```

### Response

**Success: `201 Created`**

```json
{
  "id": "proj_a1b2c3d4e5f6",
  "name": "Website Redesign",
  "description": "Q3 refresh of the marketing site",
  "status": "active",
  "owner_id": "usr_9z8y7x6w5v4u",
  "created_at": "2026-01-10T08:00:00Z",
  "updated_at": "2026-01-10T08:00:00Z",
  "archived_at": null
}
```

**Errors:**

| Status | Code | When |
|---|---|---|
| 400 | `VALIDATION_ERROR` | `name` is missing, empty, or over 200 characters |
| 401 | `UNAUTHORIZED` | Token is missing or invalid |
| 409 | `CONFLICT` | A project with this name already exists in the workspace |

### Example

```bash
curl -X POST https://api.example.com/v1/projects \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Website Redesign",
    "description": "Q3 refresh of the marketing site"
  }'
```

### Notes

Creating a project is idempotent by name within a workspace: if you try to create a project with the same name twice, the second call returns `409 CONFLICT` rather than creating a duplicate. The ID of the existing project is included in the `409` response body under `existing_id`.

---

## Get a project

Returns a single project by ID.

```
GET /v1/projects/{id}
```

### Authentication

Requires a Bearer token. Returns `403 FORBIDDEN` if the project exists but the user does not have access.

### Path parameters

| Parameter | Type | Description |
|---|---|---|
| `id` | string | The project's unique identifier, as returned by Create or List |

### Response

**Success: `200 OK`**

```json
{
  "id": "proj_a1b2c3d4e5f6",
  "name": "Website Redesign",
  "description": "Q3 refresh of the marketing site",
  "status": "active",
  "owner_id": "usr_9z8y7x6w5v4u",
  "created_at": "2026-01-10T08:00:00Z",
  "updated_at": "2026-03-15T14:22:00Z",
  "archived_at": null
}
```

**Errors:**

| Status | Code | When |
|---|---|---|
| 401 | `UNAUTHORIZED` | Token is missing or invalid |
| 403 | `FORBIDDEN` | User does not have access to this project |
| 404 | `NOT_FOUND` | No project with this ID exists |

### Example

```bash
curl https://api.example.com/v1/projects/proj_a1b2c3d4e5f6 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Update a project

Updates one or more fields on an existing project. Only the fields you include in the request body are changed — omitted fields keep their current values.

```
PATCH /v1/projects/{id}
```

### Authentication

Requires a Bearer token. Only the project owner or a workspace admin can update a project.

### Path parameters

| Parameter | Type | Description |
|---|---|---|
| `id` | string | The project's unique identifier |

### Request body

```
Content-Type: application/json
```

All fields are optional. Include only the fields you want to change.

| Field | Type | Description |
|---|---|---|
| `name` | string | New project name. Between 1 and 200 characters. Must be unique within the workspace |
| `description` | string | New description. Maximum 2,000 characters. Pass `null` to clear the description |
| `owner_id` | string (UUID) | Transfer ownership to this user ID. The target user must be a member of the workspace |

**Example request body:**

```json
{
  "name": "Website Redesign 2026",
  "description": "Updated scope to include mobile"
}
```

### Response

**Success: `200 OK`**

Returns the full updated project object.

```json
{
  "id": "proj_a1b2c3d4e5f6",
  "name": "Website Redesign 2026",
  "description": "Updated scope to include mobile",
  "status": "active",
  "owner_id": "usr_9z8y7x6w5v4u",
  "created_at": "2026-01-10T08:00:00Z",
  "updated_at": "2026-04-02T09:15:00Z",
  "archived_at": null
}
```

**Errors:**

| Status | Code | When |
|---|---|---|
| 400 | `VALIDATION_ERROR` | `name` is empty or over 200 characters |
| 401 | `UNAUTHORIZED` | Token is missing or invalid |
| 403 | `FORBIDDEN` | User is not the project owner or a workspace admin |
| 404 | `NOT_FOUND` | No project with this ID exists |
| 409 | `CONFLICT` | The new name is already taken by another project in the workspace |
| 422 | `UNPROCESSABLE_ENTITY` | `owner_id` refers to a user who is not a member of the workspace |

### Example

```bash
curl -X PATCH https://api.example.com/v1/projects/proj_a1b2c3d4e5f6 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Website Redesign 2026"}'
```

### Notes

You cannot update `status` directly via this endpoint. To archive a project, use the [Archive a project](#archive-a-project) endpoint. To restore an archived project, that operation is not supported via the API; contact support.

---

## Archive a project

Archives a project. Archived projects remain readable but cannot be modified. They appear in list results when you filter by `status=archived`.

```
POST /v1/projects/{id}/archive
```

### Authentication

Requires a Bearer token. Only the project owner or a workspace admin can archive a project.

### Path parameters

| Parameter | Type | Description |
|---|---|---|
| `id` | string | The project's unique identifier |

### Request body

No request body required.

### Response

**Success: `200 OK`**

```json
{
  "id": "proj_a1b2c3d4e5f6",
  "name": "Website Redesign 2026",
  "description": "Updated scope to include mobile",
  "status": "archived",
  "owner_id": "usr_9z8y7x6w5v4u",
  "created_at": "2026-01-10T08:00:00Z",
  "updated_at": "2026-04-30T17:00:00Z",
  "archived_at": "2026-04-30T17:00:00Z"
}
```

**Errors:**

| Status | Code | When |
|---|---|---|
| 401 | `UNAUTHORIZED` | Token is missing or invalid |
| 403 | `FORBIDDEN` | User is not the project owner or a workspace admin |
| 404 | `NOT_FOUND` | No project with this ID exists |
| 422 | `UNPROCESSABLE_ENTITY` | Project is already archived |

### Example

```bash
curl -X POST https://api.example.com/v1/projects/proj_a1b2c3d4e5f6/archive \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Notes

Archiving is idempotent in the sense that calling it on an already-archived project returns `422 UNPROCESSABLE_ENTITY` with code `CONFLICT_ALREADY_ARCHIVED` rather than silently succeeding. This is intentional: a silent success would mask bugs where your code archives the wrong project or calls archive twice on the same ID.

Archiving does not delete the project. All project data is preserved and remains accessible via `GET /v1/projects/{id}` and in list results with `status=archived`.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PARTIAL |
| Score | 11.0/15.0 (73%) |
| Evaluated | 2026-05-01 |
| Target duration | 193115 ms |
| Target cost | $0.5954 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires every endpoint to document both success responses AND error responses — not just the happy path | PASS | Every endpoint section in the artifact contains a 'Response' subsection with a success code (200/201) and an 'Errors' table. All five endpoints (List, Create, Get, Update, Archive) follow this pattern consistently. |
| c2 | Skill requires every code example to be syntactically correct and runnable — not pseudocode | PASS | All five curl examples use complete flags (-X, -H, -d), full URLs, and valid JSON bodies. E.g. the Update example: 'curl -X PATCH https://api.example.com/v1/projects/proj_a1b2c3d4e5f6 -H "Authorization: Bearer YOUR_TOKEN" -H "Content-Type: application/json" -d {"name": "Website Redesign 2026"}'. |
| c3 | Skill requires a discovery or research step — reading existing code or specs before writing docs | PASS | Chat response explicitly states: 'The repo contained no source code, so this document is based on the endpoint description you provided rather than derived from an implementation.' This demonstrates the skill attempted a source-code lookup before writing. |
| c4 | Skill organises endpoints by resource (Projects) with a consistent structure per endpoint — not a flat alphabetical list | PASS | All endpoints are grouped under '# Projects API' and follow logical CRUD order (List → Create → Get → Update → Archive), not alphabetical. Each endpoint section contains: Authentication, Parameters, Response, Errors, Example in the same order. |
| c5 | Skill requires an overview section before the endpoint reference — authentication, base URL, common patterns | PASS | Artifact opens with 'Base URL', 'Authentication', 'Rate limiting', 'Pagination', and 'Error format' sections — all before the first endpoint definition ('## List projects'). |
| c6 | Skill includes a quality checklist that verifies every code example runs and every error response is documented | FAIL | No quality checklist appears anywhere in the artifact or the chat response. There is no section, appendix, or mention of checking that examples were executed or error responses verified. |
| c7 | Skill covers pagination documentation requirements specifically — partial credit if special cases like pagination are mentioned but not required to be documented | PARTIAL | A dedicated '## Pagination' overview section exists describing cursor mechanics, the `limit`/`cursor` parameters, `has_more`, `next_cursor` semantics, and last-page behaviour. Pagination is also reflected in the List endpoint's query parameters table. |
| c8 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The captured output and artifact contain no skill file content or frontmatter. The skill was invoked successfully but the three specific required frontmatter fields (name, description, argument-hint) cannot be verified from the output alone. |
| c9 | Output covers all four prompt-named operations on Projects — create, read, update, archive — each as a documented endpoint with method, path, request, response | PASS | Artifact has '## Create a project' (POST /v1/projects), '## Get a project' (GET /v1/projects/{id}), '## Update a project' (PATCH /v1/projects/{id}), '## Archive a project' (POST /v1/projects/{id}/archive). Each includes method, path, request params/body, and response JSON. |
| c10 | Output's list endpoint documents pagination, at least 2 filter parameters (e.g. status, owner), and at least 1 sort option — not just GET / response | PARTIAL | List endpoint documents pagination (`limit`, `cursor`) and three filters (`status`, `owner_id`, `q`), satisfying two of three requirements. No sort parameter (e.g. `sort_by`, `order`) is documented anywhere in the list endpoint parameters table. |
| c11 | Output documents both success AND error responses per endpoint — at minimum 401, 403, 404, and 422 | PARTIAL | Update and Archive endpoints have all four codes (401, 403, 404, 422). Get has 401, 403, 404 but no 422. List has only 400 and 401 — missing 403, 404, 422. Create has 400, 401, 409 — missing 403, 404, 422. Only 2 of 5 endpoints satisfy the full minimum requirement. |
| c12 | Output's code examples are runnable — full HTTP request with method, headers, body, and a parseable response example — no pseudocode, no placeholder gaps | PASS | All curl commands include method (-X POST/PATCH), auth header (-H 'Authorization: Bearer YOUR_TOKEN'), content-type header where applicable, and -d body for writes. Response JSON objects are complete and parseable with realistic IDs like 'proj_a1b2c3d4e5f6'. |
| c13 | Output organises endpoints under a Projects resource heading with consistent structure per endpoint (Description, Request, Response, Errors, Example) — not flat alphabetical | PASS | All five endpoints sit under '# Projects API' and each uses the sub-section pattern: description text → Authentication → Parameters → Response (with JSON) → Errors table → Example (curl). Structure is uniform across all five endpoints. |
| c14 | Output includes an overview / authentication section before the endpoint reference — base URL, auth scheme, common request/response headers, and a common error envelope | PASS | '## Base URL' shows production/staging URLs; '## Authentication' shows Bearer scheme and token lifecycle; '## Rate limiting' documents X-RateLimit-* headers; '## Error format' shows the full common error envelope JSON with code/message/details structure. |
| c15 | Output's quality checklist verifies each code example was run and that every documented error response has a worked example | FAIL | The artifact contains no quality checklist section. The chat response also makes no mention of running examples or verifying error coverage. No evidence of a verification pass appears anywhere in the captured output. |
| c16 | Output addresses pagination behaviour edge cases — what happens for an empty result set, an out-of-range page number, and the maximum page size cap | PARTIAL | Pagination section states max limit is 100, and 'When has_more is false, you've reached the last page. next_cursor is null on the last page.' Empty result set behaviour is not addressed. Out-of-range cursor is not addressed (cursor-based pagination makes page numbers moot, but empty-set is still a gap). |

### Notes

The artifact is high quality for a generated API reference — consistent structure, realistic examples, a solid overview section, and all four CRUD operations covered. The main weaknesses are: (1) no quality checklist appears anywhere in the output (c6, c15), which are outright failures; (2) the skill's own YAML frontmatter cannot be verified from the output (c8); (3) the list endpoint omits sort parameters (c10); and (4) simpler endpoints (List, Create) fall short of the 401/403/404/422 minimum error coverage (c11). These five gaps bring the score to 73%, earning a PARTIAL verdict. The pagination and authentication sections are notably strong.
