---
name: write-api-docs
description: Generate API reference documentation from code, OpenAPI specs, or endpoint implementations.
argument-hint: "[API file, directory, or OpenAPI spec path]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Generate API documentation for $ARGUMENTS using the mandatory process and structure below.

## Step 1 — Discover all endpoints

Scan the codebase to find every API endpoint:

1. Use `Grep` to find route definitions (e.g., `router.get`, `@app.route`, `@GetMapping`, endpoint annotations)
2. Use `Glob` to find controller files, route files, or OpenAPI specs
3. Read each file to extract: HTTP method, path, handler function, middleware (auth, validation)
4. If an OpenAPI/Swagger spec exists, use it as the source of truth but cross-reference with the implementation for accuracy

Build a complete endpoint inventory before writing anything.

## Step 2 — Identify resources and organise

Group endpoints by **resource** (the noun), not by HTTP method. This is how developers think about APIs.

- Good: All `/users` endpoints together (GET list, GET by ID, POST create, PUT update, DELETE)
- Bad: All GET endpoints together, then all POST endpoints

Determine the resource hierarchy:
```
/users
/users/{id}
/users/{id}/projects
/users/{id}/projects/{projectId}
```

This hierarchy becomes the documentation structure.

## Step 3 — Write the API overview

Every API document starts with these sections:

### Base URL

```
Production: https://api.example.com/v1
Staging: https://api-staging.example.com/v1
```

State the versioning strategy (path-based `/v1/`, header-based, query parameter).

### Authentication

Document every authentication method the API supports:

```
#### Bearer token

Include the token in the Authorization header:

    Authorization: Bearer YOUR_API_TOKEN

Obtain a token by: [exact steps or link]
Token expiration: [duration]
Token refresh: [procedure]

#### API key

Include the key as a header:

    X-API-Key: YOUR_API_KEY

Obtain a key from: [exact location in dashboard]
Key permissions: [what different key types can access]
```

For each auth method, specify:
- How to obtain credentials
- Where to include them (header, query, cookie)
- Expiration and refresh behaviour
- What error you get when auth fails (include the exact error response body)

### Rate limiting

```
Rate limit: [N] requests per [period]
Header: X-RateLimit-Remaining (requests left in current window)
Header: X-RateLimit-Reset (Unix timestamp when window resets)
Exceeded response: 429 Too Many Requests
```

If rate limits differ by plan or endpoint, document the tiers.

### Pagination

Document the pagination pattern used. Pick the one that matches:

**Offset-based:**
```
GET /resources?offset=20&limit=10

Response:
{
  "data": [...],
  "total": 153,
  "offset": 20,
  "limit": 10
}
```

**Cursor-based:**
```
GET /resources?cursor=abc123&limit=10

Response:
{
  "data": [...],
  "next_cursor": "def456",
  "has_more": true
}
```

State:
- Default page size
- Maximum page size
- How to detect the last page
- Whether total count is available

### Error format

Document the standard error response structure:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable description",
    "details": [
      {
        "field": "email",
        "message": "Must be a valid email address"
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
| 403 | `FORBIDDEN` | Authenticated but insufficient permissions | Wrong role, resource belongs to another user |
| 404 | `NOT_FOUND` | Resource does not exist | Wrong ID, deleted resource |
| 409 | `CONFLICT` | Request conflicts with current state | Duplicate email, concurrent edit |
| 422 | `UNPROCESSABLE_ENTITY` | Request is well-formed but semantically invalid | Business rule violation |
| 429 | `RATE_LIMITED` | Too many requests | Exceeded rate limit |
| 500 | `INTERNAL_ERROR` | Server error | Bug — contact support |

Populate this table with the actual error codes from the codebase.

## Step 4 — Document each endpoint

Use this exact template for every endpoint:

```markdown
---

## [Action description]

[One sentence describing what this endpoint does and when to use it.]

    [METHOD] [path]

### Authentication

[Required auth level — e.g., "Requires Bearer token with `read:users` scope"]

### Path parameters

| Parameter | Type | Description |
|---|---|---|
| `id` | string (UUID) | The user's unique identifier |

### Query parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `status` | string | No | `active` | Filter by status. One of: `active`, `inactive`, `suspended` |
| `limit` | integer | No | 20 | Number of results per page (max: 100) |

### Request body

    Content-Type: application/json

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | Yes | User's display name (1-100 characters) |
| `email` | string | Yes | Valid email address. Must be unique. |
| `role` | string | No | One of: `admin`, `member`, `viewer`. Default: `member` |

**Example request body:**
\`\`\`json
{
  "name": "Jane Smith",
  "email": "jane@example.com",
  "role": "member"
}
\`\`\`

### Response

**Success: `201 Created`**

\`\`\`json
{
  "id": "usr_abc123",
  "name": "Jane Smith",
  "email": "jane@example.com",
  "role": "member",
  "created_at": "2025-01-15T09:30:00Z"
}
\`\`\`

**Errors:**

| Status | Code | When |
|---|---|---|
| 400 | `VALIDATION_ERROR` | Missing required field or invalid format |
| 409 | `CONFLICT` | Email already in use |

### Example

\`\`\`bash
curl -X POST https://api.example.com/v1/users \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "email": "jane@example.com",
    "role": "member"
  }'
\`\`\`

### Notes

[Any caveats, side effects, or important behaviour — e.g., "Creating a user sends a welcome email" or "Deleted users are soft-deleted and can be restored within 30 days"]

---
```

Rules for endpoint documentation:
- **Every parameter must have a type and description.** "id — the ID" is not a description. "id — string (UUID) — The unique identifier for the user, returned from the Create User endpoint" is.
- **Every enum must list all valid values.** Do not write "a valid status" — write "One of: `active`, `inactive`, `suspended`."
- **Every response must show a realistic example.** Use plausible data, not `"string"` or `"foo"`.
- **Every endpoint must have a curl example.** Developers will copy this. Make it work.
- **Document side effects.** If creating a resource triggers an email, webhook, or event, say so.
- **Document idempotency.** Is it safe to retry this request? What happens if you call it twice with the same data?

## Step 5 — Handle special cases

### Nested resources

Document the relationship: "A Project belongs to a User. You must provide the user ID in the path."

### Bulk operations

If the API supports bulk create/update/delete, document:
- Maximum batch size
- Partial failure behaviour (does the whole batch fail or do individual items fail?)
- Response format for mixed success/failure

### Webhooks / Events

If the API sends webhooks, document:
- Available events
- Payload format for each event
- Retry behaviour
- How to verify webhook signatures

### File uploads

If any endpoint accepts file uploads, document:
- Accepted file types and size limits
- Whether to use `multipart/form-data` or binary body
- Example with curl

## Step 6 — Quality checks

| Check | Requirement |
|---|---|
| Every endpoint has a curl example | Can a developer copy-paste and get a response? |
| Every parameter has a type | No untyped parameters |
| Every enum lists all values | No "valid value" without the list |
| Response examples use realistic data | No `"string"` or `"test"` placeholder values |
| Error responses are documented | At least the most common error for each endpoint |
| Auth requirements are stated per endpoint | Not just in the overview |
| Pagination is documented | For every list endpoint |

## Rules

- Organise by resource, never by HTTP method. Developers look up "how to work with users," not "what can I GET."
- Use the actual field names, types, and values from the codebase. Do not invent or guess.
- If the implementation disagrees with an OpenAPI spec, document the implementation and flag the discrepancy.
- If an endpoint has undocumented behaviour (e.g., it returns different fields based on permissions), document it — these are the things developers waste hours discovering.
- Write for the developer who has never seen this API before. They should be able to make their first successful request within 5 minutes of reading.

## Output Format

The output is one instance of the endpoint template from Step 4 per endpoint, wrapped by the overview sections from Step 3. See Step 3 and Step 4 above for the exact structure.

## Related Skills

- `/developer-docs-writer:write-sdk-guide` — for SDK-level documentation that wraps the API. Write the API reference first, then the SDK guide.
- `/developer-docs-writer:write-integration-guide` — for step-by-step integration tutorials that use the API.
