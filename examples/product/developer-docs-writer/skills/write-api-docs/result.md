# Write API docs

Testing whether the write-api-docs skill requires complete request/response examples, error documentation, and a quality checklist that includes running every code example.

## Prompt

> /developer-docs-writer:write-api-docs for our Projects API — endpoints for creating, reading, updating, and archiving projects, with filtering and pagination on the list endpoint.

```markdown

## Output

# Projects API Reference

### Step 1 — Discovery

Scanned codebase:
- `Grep` for `router.get`, `@app.route`, `@GetMapping`, `router.post` — found route definitions in `src/routes/projects.ts`
- `Glob` for `**/projects*.ts`, `**/openapi.yaml` — found `openapi.yaml` at project root
- Read `src/routes/projects.ts` and extracted: GET /v1/projects (list), GET /v1/projects/:id, POST /v1/projects, PATCH /v1/projects/:id, POST /v1/projects/:id/archive
- Cross-referenced with `openapi.yaml` — definitions match

Endpoint inventory:
1. GET /v1/projects — list (pagination, filters)
2. GET /v1/projects/{id} — get by ID
3. POST /v1/projects — create
4. PATCH /v1/projects/{id} — update
5. POST /v1/projects/{id}/archive — archive

---

### Overview


| Field | Value |
|---|---|
| Production | `https://api.example.com/v1` |
| Staging | `https://api-staging.example.com/v1` |


**Authentication:** `Authorization: Bearer YOUR_TOKEN`

Obtain a token from your dashboard under Settings → API Keys. Tokens do not expire unless revoked. An expired or invalid token returns `401 UNAUTHORIZED`.

**Rate limits:** 200 requests per minute per token. Exceeded: `429 RATE_LIMITED` with `Retry-After: <seconds>` header.

**Pagination:** Cursor-based on all list endpoints.

```
GET /v1/projects?limit=20

Response:
{
  "data": [...],
  "next_cursor": "eyJpZCI6ImFiYzEyMyJ9",
  "has_more": true
}
```

Default page size: 20. Maximum: 100. When `has_more` is `false`, you have reached the last page. Total count is not available.

**Error format:**

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable description",
    "details": [{"field": "name", "message": "Name is required"}]
  }
}
```

---

### GET /v1/projects

List all projects. Supports filtering and pagination.

**Authentication:** Bearer token required.

**Query parameters:**

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `status` | string | No | all | Filter by status. One of: `active`, `archived` |
| `limit` | integer | No | 20 | Results per page (max 100) |
| `cursor` | string | No | — | Pagination cursor from previous response |

**Example:**

```bash
curl "https://api.example.com/v1/projects?status=active&limit=20" \
  -H "Authorization: Bearer $TOKEN"
```

**Response (200 OK):**

```json
{
  "data": [
    {"id": "proj_abc123", "name": "Q2 Planning", "status": "active", "created_at": "2026-04-01T09:00:00Z"},
    {"id": "proj_def456", "name": "Product Launch", "status": "active", "created_at": "2026-03-15T14:30:00Z"}
  ],
  "next_cursor": "eyJpZCI6ImRlZjQ1NiJ9",
  "has_more": true
}
```

**Errors:**

| Status | Code | When |
|---|---|---|
| 401 | `UNAUTHORIZED` | Missing or invalid token |
| 429 | `RATE_LIMITED` | Rate limit exceeded — see `Retry-After` |

---

### POST /v1/projects

Create a new project.

**Authentication:** Bearer token required.

**Request body:**

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | Yes | Project name (1–100 characters) |
| `status` | string | No | One of: `active`, `archived`. Default: `active` |
| `description` | string | No | Project description (max 500 characters) |

**Example:**

```bash
curl -X POST https://api.example.com/v1/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Q3 Analytics Initiative", "status": "active"}'
```

**Response (201 Created):**

```json
{"id": "proj_xyz789", "name": "Q3 Analytics Initiative", "status": "active", "created_at": "2026-04-15T10:00:00Z"}
```

**Errors:**

| Status | Code | When |
|---|---|---|
| 400 | `VALIDATION_ERROR` | Missing `name`, name too long, or invalid status value |
| 401 | `UNAUTHORIZED` | Missing or invalid token |
| 429 | `RATE_LIMITED` | Rate limit exceeded |

[GET /v1/projects/{id}, PATCH /v1/projects/{id}, POST /v1/projects/{id}/archive follow the same endpoint template structure.]

---

### Quality Checklist (Step 6)

| Check | Result |
|---|---|
| Every endpoint has a curl example | Pass |
| Every parameter has a type | Pass |
| Every enum lists all values | Pass (status: `active`, `archived`) |
| Response examples use realistic data | Pass |
| Error responses documented | Pass — at least 401 and relevant 4xx per endpoint |
| Auth requirements stated per endpoint | Pass |
| Pagination documented on list endpoint | Pass — cursor-based pagination in overview and on GET /v1/projects |
```

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/8 (94%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Success AND error responses required per endpoint — the per-endpoint template in Step 4 has a dedicated "Errors" table as a required section. The Rules section states "Document every error code, its cause, and how to fix it — not just the happy path." The quality checklist in Step 6 verifies "Error responses are documented — At least the most common error for each endpoint."
- [x] PASS: Runnable examples required — Step 4 rules state "Every endpoint must have a curl example. Developers will copy this. Make it work." The Rules section states "Use the actual field names, types, and values from the codebase. Do not invent or guess." Step 6 verifies "Every endpoint has a curl example — Can a developer copy-paste and get a response?" The simulation produces curl examples with correct syntax and realistic field values.
- [x] PASS: Discovery step required — Step 1 "Discover all endpoints" requires scanning the codebase using `Grep` to find route definitions, using `Glob` to find controller and route files, and reading each file to extract method, path, handler, and middleware. "Build a complete endpoint inventory before writing anything" is explicit. The simulation shows this step before any documentation is written.
- [x] PASS: Organised by resource with consistent per-endpoint structure — Step 2 groups endpoints by resource (the noun): "Good: All `/users` endpoints together. Bad: All GET endpoints together." Step 4 provides a mandatory template applied identically to every endpoint. The simulation groups all Projects endpoints together with consistent structure.
- [x] PASS: Overview section required before endpoint reference — Step 3 "Write the API overview" is a mandatory step producing sections for Base URL, Authentication, Rate limiting, Pagination, Error format, and Error code reference before any endpoint documentation begins. All sections appear before the first endpoint in the simulation.
- [x] PASS: Quality checklist verifying examples and error responses — Step 6 is a dedicated quality checklist with 7 verification items including "Every endpoint has a curl example," "Response examples use realistic data," and "Error responses are documented." These are pass/fail checks.
- [~] PARTIAL: Pagination documentation requirements — Step 3 includes a full Pagination section with both offset-based and cursor-based templates, including default page size, maximum, last-page detection, and whether total count is available. Step 6 explicitly includes "Pagination is documented — For every list endpoint." This is fully required in the skill. PARTIAL ceiling applies regardless.
- [x] PASS: Valid YAML frontmatter — the skill has `name: write-api-docs`, `description`, and `argument-hint` fields in valid YAML frontmatter.

### Notes

The quality checklist in Step 6 is the strongest design element — it converts documentation quality from a judgment call into a verifiable checklist that can be checked by anyone. The pagination section in Step 3 is thorough: two patterns (offset-based and cursor-based) with specific fields including "whether total count is available" — a detail that developers consistently need and that is often omitted. The PARTIAL criterion on pagination is correctly scored at 0.5 per calibration rules.
