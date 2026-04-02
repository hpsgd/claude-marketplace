# API Design Document — {API Name}

> Version {1.0} | {Date} | Status: {Draft/Review/Approved}

## 1. Overview

| Field | Value |
|-------|-------|
| Purpose | {What this API enables} |
| Base URL | `https://api.example.com/v1` |
| Authentication | {e.g. OAuth 2.0 Bearer Token / API Key} |
| Transport | HTTPS (TLS 1.2+) |
| Content Type | `application/json` |

## 2. Resource Hierarchy

```
/{top-level-resource}
  /{id}/{sub-resource}/{id}
```

{Describe parent-child ownership rules and lifecycle dependencies.}

## 3. Endpoints

| Method | Path | Description | Auth | Idempotent |
|--------|------|-------------|------|-----------|
| GET | `/{resource}` | List resources (paginated) | Required | Yes |
| POST | `/{resource}` | Create a resource | Required | No |
| GET | `/{resource}/{id}` | Retrieve a resource | Required | Yes |
| PUT | `/{resource}/{id}` | Replace a resource | Required | Yes |
| PATCH | `/{resource}/{id}` | Partial update | Required | Yes |
| DELETE | `/{resource}/{id}` | Delete a resource | Required | Yes |

## 4. Request/Response Schemas

### POST `/{resource}` — Create

**Request:**
```json
{ "name": "string (required)", "description": "string (optional)", "metadata": {} }
```

**Response (201 Created):**
```json
{ "id": "res_abc123", "name": "string", "createdAt": "2026-01-15T10:30:00Z" }
```

{Repeat for each endpoint with distinct schemas.}

## 5. Error Catalogue

| Code | HTTP Status | Message | Resolution |
|------|------------|---------|-----------|
| `invalid_request` | 400 | Malformed input | {Fix guidance} |
| `unauthorized` | 401 | Authentication required | Provide valid Bearer token |
| `forbidden` | 403 | Insufficient permissions | Request elevated role |
| `not_found` | 404 | Resource not found | Verify resource ID |
| `conflict` | 409 | Resource already exists | Use PUT to update |
| `rate_limited` | 429 | Too many requests | Retry after `Retry-After` header |
| `internal_error` | 500 | Unexpected server error | Contact support with request ID |

Error shape: `{ "error": { "code": "string", "message": "string", "target": "field", "requestId": "string" } }`

## 6. Pagination & Filtering

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | integer | 20 | Items per page (max 100) |
| `cursor` | string | — | Opaque cursor from previous response |
| `filter[{field}]` | string | — | Filter by field value |
| `sort` | string | `-createdAt` | Sort field (`-` prefix = desc) |

Response envelope: `{ "data": [], "pagination": { "nextCursor": "string", "hasMore": true } }`

## 7. Versioning Strategy

| Aspect | Approach |
|--------|----------|
| Mechanism | URL path prefix (`/v1/`, `/v2/`) |
| Deprecation notice | `Sunset` header + 6-month window |
| Breaking change policy | New major version; old version maintained for deprecation period |

## 8. Rate Limiting

| Tier | Requests/min | Burst | Notes |
|------|-------------|-------|-------|
| Free | 60 | 10 | Per API key |
| Pro | 600 | 50 | Per API key |
| Enterprise | Custom | Custom | Negotiated |

Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, `Retry-After` (on 429).

## 9. Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | {Date} | Initial release |
