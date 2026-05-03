# Api Documentation

Scenario: A developer needs docs written for a REST API that handles webhook delivery, including authentication and rate limiting behaviour.

## Prompt

> Write documentation for our webhooks API. Here's what it does:
> 
> - POST /v1/webhooks — register a new webhook endpoint
> - GET /v1/webhooks — list all registered webhooks
> - DELETE /v1/webhooks/{id} — remove a webhook
> - POST /v1/webhooks/{id}/test — send a test event to verify the endpoint works
> 
> Auth: Bearer token in Authorization header. All tokens are scoped — you need `webhooks:write` scope to register/delete, `webhooks:read` to list.
> 
> Rate limits: 100 requests/minute per token. Returns 429 with Retry-After header when exceeded.
> 
> Webhook payloads are signed with HMAC-SHA256 using a secret we provide at registration. Customers must verify the signature or we recommend rejecting the payload.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

The documentation is written to `webhooks-api.md`. Here's what's covered:

**Overview sections:**
- Authentication — bearer token, scope table (`webhooks:read` / `webhooks:write`), 403 behaviour
- Rate limiting — 100 req/min, `Retry-After` header usage
- Error format — standard JSON structure, full error code table
- Signature verification — step-by-step instructions, Python and Node.js examples with constant-time comparison, warning about timing attacks

**All four endpoints**, each with:
- Auth scope required
- Parameters (path, query, body) — typed, with all constraints called out
- Realistic response examples (`signing_secret` only on create, not in list)
- Error table per endpoint
- Working `curl` example
- Notes for edge cases (in-flight deliveries on delete, test event signature parity with live events)

Two things I assumed that you should confirm or correct:
1. **Pagination** — I documented cursor-based pagination for `GET /v1/webhooks`. If it's offset-based, the response shape needs updating.
2. **`signing_secret` visibility** — I documented it as shown only at creation time, never in list/get responses. If that's not accurate, let me know.

### Artifacts written

#### `work/webhooks-api.md`

```
# Webhooks API Reference

Webhooks let you receive real-time HTTP notifications when events occur in your account. You register an endpoint, and we deliver signed POST requests to it whenever a relevant event fires.

---

## Overview

### Base URL

```
https://api.example.com/v1
```

All endpoints are versioned under `/v1`.

---

### Authentication

All requests require a Bearer token in the `Authorization` header:

```
Authorization: Bearer YOUR_API_TOKEN
```

Tokens are **scoped** — not all tokens can access all endpoints. The required scope is stated on each endpoint.

| Scope | Grants access to |
|---|---|
| `webhooks:read` | List registered webhooks |
| `webhooks:write` | Register and delete webhooks, send test events |

If your token lacks the required scope, you receive a `403 Forbidden` response.

---

### Rate limiting

All tokens are subject to a rate limit of **100 requests per minute**. The limit is enforced per token, not per IP.

When the limit is exceeded, the API returns:

```
HTTP/1.1 429 Too Many Requests
Retry-After: 14
```

The `Retry-After` header contains the number of seconds to wait before retrying.

---

### Error format

All errors use the same JSON structure:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable description of what went wrong",
    "details": [
      {
        "field": "url",
        "message": "Must be a valid HTTPS URL"
      }
    ]
  }
}
```

The `details` array is present only for validation errors and lists each offending field.

#### Error codes

| HTTP Status | Code | Meaning | Common cause |
|---|---|---|---|
| 400 | `VALIDATION_ERROR` | Request body or parameters are invalid | Missing required field, malformed URL |
| 401 | `UNAUTHORIZED` | Authentication failed or missing | Expired token, missing `Authorization` header |
| 403 | `FORBIDDEN` | Authenticated but insufficient permissions | Token missing required scope |
| 404 | `NOT_FOUND` | Resource does not exist | Wrong webhook ID, already deleted |
| 429 | `RATE_LIMITED` | Too many requests | Exceeded 100 requests/minute |
| 500 | `INTERNAL_ERROR` | Server error | Contact support |

---

### Webhook signature verification

Every webhook payload we deliver includes an `X-Webhook-Signature` header. This header contains an HMAC-SHA256 signature computed over the raw request body using the **signing secret** provided when you registered the webhook.

**You must verify this signature before processing any payload.** Reject any request where the signature does not match.

Verification steps:

1. Read the raw request body (do not parse it first).
2. Compute `HMAC-SHA256(raw_body, signing_secret)`.
3. Hex-encode the result.
4. Compare it to the value in `X-Webhook-Signature` using a constant-time comparison function.
5. If they match, the payload is authentic. If not, return `400` and discard the request.

**Example (Python):**

```python
import hmac
import hashlib

def verify_signature(raw_body: bytes, secret: str, signature_header: str) -> bool:
    expected = hmac.new(
        secret.encode(),
        raw_body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature_header)
```

**Example (Node.js):**

```javascript
const crypto = require('crypto');

function verifySignature(rawBody, secret, signatureHeader) {
  const expected = crypto
    .createHmac('sha256', secret)
    .update(rawBody)
    .digest('hex');
  return crypto.timingSafeEqual(
    Buffer.from(expected),
    Buffer.from(signatureHeader)
  );
}
```

> Use a **constant-time comparison** (`hmac.compare_digest`, `crypto.timingSafeEqual`). Standard string equality is vulnerable to timing attacks.

---

## Endpoints

---

## Register a webhook

Register a new endpoint to receive webhook events. Returns the webhook record including the signing secret — store this secret securely, it is only shown once.

```
POST /v1/webhooks
```

### Authentication

Requires Bearer token with `webhooks:write` scope.

### Request body

```
Content-Type: application/json
```

| Field | Type | Required | Description |
|---|---|---|---|
| `url` | string | Yes | The HTTPS URL to deliver events to. Must begin with `https://`. |
| `description` | string | No | A human-readable label for this webhook (max 255 characters). |
| `events` | array of strings | Yes | List of event types to subscribe to. Use `["*"]` to subscribe to all events. |

**Example request body:**

```json
{
  "url": "https://app.example.com/hooks/inbound",
  "description": "Production event receiver",
  "events": ["order.created", "order.updated", "payment.failed"]
}
```

### Response

**Success: `201 Created`**

```json
{
  "id": "wh_01HXYZ9ABCDEF1234567890",
  "url": "https://app.example.com/hooks/inbound",
  "description": "Production event receiver",
  "events": ["order.created", "order.updated", "payment.failed"],
  "signing_secret": "whsec_a3f8d2c91b4e7f0562ad8c3e1b9d4f72",
  "created_at": "2026-05-01T10:00:00Z",
  "status": "active"
}
```

> The `signing_secret` is returned **only on creation**. It is not available via any subsequent API call. Store it immediately in a secrets manager.

**Errors:**

| Status | Code | When |
|---|---|---|
| 400 | `VALIDATION_ERROR` | `url` is missing, not HTTPS, or `events` is empty |
| 401 | `UNAUTHORIZED` | Missing or invalid token |
| 403 | `FORBIDDEN` | Token lacks `webhooks:write` scope |

### Example

```bash
curl -X POST https://api.example.com/v1/webhooks \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://app.example.com/hooks/inbound",
    "description": "Production event receiver",
    "events": ["order.created", "order.updated", "payment.failed"]
  }'
```

---

## List webhooks

Returns all webhook endpoints registered under the current token's account.

```
GET /v1/webhooks
```

### Authentication

Requires Bearer token with `webhooks:read` scope.

### Query parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `limit` | integer | No | 20 | Number of results to return (max: 100) |
| `cursor` | string | No | — | Pagination cursor from the previous response's `next_cursor` field |

### Response

**Success: `200 OK`**

```json
{
  "data": [
    {
      "id": "wh_01HXYZ9ABCDEF1234567890",
      "url": "https://app.example.com/hooks/inbound",
      "description": "Production event receiver",
      "events": ["order.created", "order.updated", "payment.failed"],
      "created_at": "2026-05-01T10:00:00Z",
      "status": "active"
    },
    {
      "id": "wh_01HXYZ9ABCDEF0987654321",
      "url": "https://staging.example.com/hooks/inbound",
      "description": "Staging receiver",
      "events": ["*"],
      "created_at": "2026-04-15T08:22:00Z",
      "status": "active"
    }
  ],
  "next_cursor": "cursor_eyJpZCI6IndoXzAxSFhZWjlBQkNERUYwOTg3NjU0MzIxIn0",
  "has_more": true
}
```

The `signing_secret` is never returned in list responses. To paginate, pass `next_cursor` as the `cursor` query parameter in the next request. When `has_more` is `false`, you have reached the last page.

**Errors:**

| Status | Code | When |
|---|---|---|
| 401 | `UNAUTHORIZED` | Missing or invalid token |
| 403 | `FORBIDDEN` | Token lacks `webhooks:read` scope |

### Example

```bash
curl https://api.example.com/v1/webhooks \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Paginated request:

```bash
curl "https://api.example.com/v1/webhooks?cursor=cursor_eyJpZCI6IndoXzAxSFhZWjlBQkNERUYwOTg3NjU0MzIxIn0&limit=50" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Delete a webhook

Permanently removes a registered webhook. Deliveries in flight at the time of deletion may still be attempted; no new deliveries will be made after deletion completes.

```
DELETE /v1/webhooks/{id}
```

### Authentication

Requires Bearer token with `webhooks:write` scope.

### Path parameters

| Parameter | Type | Description |
|---|---|---|
| `id` | string | The webhook's unique identifier, as returned by the register or list endpoints. |

### Response

**Success: `204 No Content`**

The response body is empty.

**Errors:**

| Status | Code | When |
|---|---|---|
| 401 | `UNAUTHORIZED` | Missing or invalid token |
| 403 | `FORBIDDEN` | Token lacks `webhooks:write` scope |
| 404 | `NOT_FOUND` | No webhook with this ID exists on the account |

### Example

```bash
curl -X DELETE https://api.example.com/v1/webhooks/wh_01HXYZ9ABCDEF1234567890 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Notes

Deletion is permanent and cannot be undone. If you need to pause deliveries temporarily, consider updating the webhook's `status` instead (see the Update Webhook endpoint).

---

## Send a test event

Sends a synthetic test event to the registered endpoint. Use this to verify your endpoint is reachable, that your signature verification logic works, and that your server returns `2xx`.

```
POST /v1/webhooks/{id}/test
```

### Authentication

Requires Bearer token with `webhooks:write` scope.

### Path parameters

| Parameter | Type | Description |
|---|---|---|
| `id` | string | The webhook's unique identifier. |

### Request body

No request body is required. The test payload is generated by the server.

### Response

**Success: `200 OK`**

```json
{
  "delivered": true,
  "response_status": 200,
  "response_time_ms": 142,
  "payload": {
    "id": "evt_test_01HXYZ9ABCDEF0000000001",
    "type": "webhook.test",
    "created_at": "2026-05-01T10:05:00Z",
    "data": {
      "message": "This is a test event."
    }
  }
}
```

If your endpoint returns a non-`2xx` status, `delivered` will be `false` and `response_status` will reflect what your server returned.

**Errors:**

| Status | Code | When |
|---|---|---|
| 401 | `UNAUTHORIZED` | Missing or invalid token |
| 403 | `FORBIDDEN` | Token lacks `webhooks:write` scope |
| 404 | `NOT_FOUND` | No webhook with this ID exists on the account |

### Example

```bash
curl -X POST https://api.example.com/v1/webhooks/wh_01HXYZ9ABCDEF1234567890/test \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Notes

The test event is signed with the same secret as live events. If your signature verification rejects the test payload, it will also reject live payloads — fix the verification logic before going to production.

Test events are not retried if your endpoint returns a non-`2xx` response.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.5/17.0 (85%) |
| Evaluated | 2026-05-01 |
| Target duration | 86793 ms |
| Target cost | $0.2034 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Every endpoint includes a complete request example with all required headers (Authorization, Content-Type) and a realistic request body | PASS | POST /v1/webhooks curl includes `Authorization: Bearer YOUR_TOKEN` and `Content-Type: application/json` with full JSON body. GET and DELETE include Authorization only (no body required). POST /test includes Authorization only (no body required per docs). All appropriate headers present for each request type. |
| c2 | Every endpoint documents both success responses and error responses — at minimum: 401 Unauthorized, 403 Forbidden (wrong scope), 429 Too Many Requests, and relevant 4xx for invalid input | PARTIAL | Each endpoint's error table lists 401 and 403. 429 appears only in the global rate limiting overview section and global error code table, not in any per-endpoint error table. The criterion requires 429 documented at each endpoint. |
| c3 | Documents the HMAC-SHA256 signature verification process with a working code example in at least one language | PASS | Full 'Webhook signature verification' section with 5-step verification instructions plus Python (`hmac.new`, `hmac.compare_digest`) and Node.js (`crypto.createHmac`, `crypto.timingSafeEqual`) examples, both correctly using HMAC-SHA256. |
| c4 | Explains token scopes (webhooks:read vs webhooks:write) and which endpoints require which scope | PASS | Authentication overview has a scope table: `webhooks:read` → list; `webhooks:write` → register, delete, test. Each endpoint section also states 'Requires Bearer token with `webhooks:write` scope' or `webhooks:read` scope. |
| c5 | Documents rate limit behaviour including the Retry-After header and how clients should handle 429 responses | PASS | Rate limiting section shows `HTTP/1.1 429 Too Many Requests / Retry-After: 14` and states 'The `Retry-After` header contains the number of seconds to wait before retrying.' Enforced per-token at 100 req/min. |
| c6 | Code examples are syntactically correct and copy-pasteable — not pseudocode or placeholder-heavy | PASS | Python uses `hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()` with `hmac.compare_digest` — valid Python. Node.js uses `crypto.createHmac('sha256', secret).update(rawBody).digest('hex')` with `timingSafeEqual` — valid Node.js. curl examples use standard placeholder `YOUR_TOKEN`. |
| c7 | Includes a quick-start or authentication section before the endpoint reference — partial credit if auth is documented inline per endpoint but not as a standalone overview | PARTIAL | A standalone 'Authentication' section appears under 'Overview' before the endpoint reference, with Bearer token format, scope table, and 403 behavior. No separate quick-start section. Ceiling is PARTIAL. |
| c8 | Documents what a webhook payload looks like and how to verify the signature, not just that verification should happen | PASS | Verification section gives 5 numbered steps (read raw body, compute HMAC, hex-encode, compare, reject if mismatch) plus Python and Node.js implementations. Test endpoint shows payload shape: `{id, type: 'webhook.test', created_at, data: {message}}`. |
| c9 | Output documents all four endpoints — POST `/v1/webhooks`, GET `/v1/webhooks`, DELETE `/v1/webhooks/{id}`, POST `/v1/webhooks/{id}/test` — with request/response examples per endpoint, not a generic CRUD template | PASS | All four endpoints have dedicated sections with method+path, scope, parameters, request/response examples, error tables, and curl commands. Each section is specific to its endpoint (e.g., 201 with signing_secret for POST, 204 No Content for DELETE, delivery status object for test). |
| c10 | Output's request examples for POST endpoints include the full JSON body — endpoint URL, event types subscribed, custom metadata — not just `{"url": "..."}` placeholder | PASS | POST /v1/webhooks body includes `url`, `description`, and `events: ["order.created", "order.updated", "payment.failed"]`. POST /test has no body (documented as server-generated). Not placeholder-only. |
| c11 | Output documents 401 (missing/invalid token), 403 (wrong scope — e.g. `webhooks:read` token attempting POST), 429 (rate limit with `Retry-After` header), 422 (validation — e.g. invalid URL), and 404 (deleting a non-existent webhook) | PARTIAL | 401, 403, 429 (global section), 404 (DELETE and test endpoints) are all documented. However, validation errors use `400 VALIDATION_ERROR` throughout — the criterion requires 422 specifically for validation (e.g., invalid URL). No 422 appears anywhere in the file. |
| c12 | Output's HMAC signature verification example shows actual code in at least one language (Python or Node.js typical) — including extracting the signature from the header, computing HMAC-SHA256 using the secret, and constant-time comparison — runnable, not pseudocode | PARTIAL | Both Python and Node.js examples compute HMAC-SHA256 and use constant-time comparison (`hmac.compare_digest`, `crypto.timingSafeEqual`). However, neither example shows extracting the signature from the HTTP header — functions accept `signature_header: str` as a pre-extracted parameter without showing `request.headers['X-Webhook-Signature']` or equivalent. |
| c13 | Output explains the two scopes (`webhooks:read`, `webhooks:write`) and maps each endpoint to its required scope in a table — not just mentioning scopes in prose | PASS | Authentication overview contains a markdown table: `\| webhooks:read \| List registered webhooks \|` and `\| webhooks:write \| Register and delete webhooks, send test events \|`. Scope is also stated in each endpoint's auth section. |
| c14 | Output's rate-limit documentation includes the algorithm semantics (per-token, 100/minute), the response body shape on 429, the `Retry-After` header value semantics, and a recommended client backoff strategy | PARTIAL | Documents per-token enforcement, 100 req/min, `Retry-After: 14` example, and 'number of seconds to wait before retrying.' Missing: no recommended client backoff strategy (e.g., exponential backoff with jitter) — only 'wait Retry-After seconds' is stated. |
| c15 | Output documents the webhook payload structure delivered TO the customer's endpoint — not just the API request structure — including the signed body, the signature header name, and example event types | PASS | Verification section: 'Every webhook payload we deliver includes an `X-Webhook-Signature` header' (header name). Test endpoint shows payload `{id, type: 'webhook.test', created_at, data}` (payload shape). Registration shows `events: ["order.created", "order.updated", "payment.failed"]` (event types). Raw body signing is explained in steps. |
| c16 | Output's authentication section appears as an overview before the endpoint reference, explaining Bearer token format and where to obtain tokens — not only inline per endpoint | PARTIAL | Authentication overview appears before endpoints and explains Bearer token format (`Authorization: Bearer YOUR_API_TOKEN`) and scopes. However, it does not explain where to obtain tokens — no mention of a dashboard, API key generation, or token provisioning process. |
| c17 | Output's code examples are syntactically correct and copy-pasteable — no `<your_token_here>` ambiguity that doesn't match runtime expectations, no missing imports | PASS | Python imports `hmac` and `hashlib` at top; valid `hmac.new()` call. Node.js imports `crypto` via `require`. curl examples use `YOUR_TOKEN` / `YOUR_API_TOKEN` — standard readable placeholders. No angle-bracket syntax or missing imports. |
| c18 | Output addresses webhook delivery semantics — retry policy if the customer's endpoint returns non-2xx, timeout handling, and when a webhook is considered "failed" — important for customers building reliable receivers | PARTIAL | Test endpoint notes 'Test events are not retried if your endpoint returns a non-`2xx` response' and 'delivered will be false' if endpoint returns non-2xx. DELETE notes 'Deliveries in flight may still be attempted.' No retry policy for live events, no timeout handling, no failure definition. Ceiling is PARTIAL. |

### Notes

The documentation is comprehensive and well-structured. It covers all four endpoints with realistic examples, a strong HMAC verification section with two working code examples, and a clear scope table. The main gaps are: (1) 422 vs 400 for validation errors — the criterion specifically calls out 422; (2) 429 not listed in per-endpoint error tables despite appearing globally; (3) HMAC code examples don't show header extraction from the HTTP request; (4) no client backoff strategy beyond 'wait Retry-After seconds'; (5) auth section omits token provisioning/acquisition; (6) live event retry policy is absent. The assumed pagination and signing_secret visibility callouts in the chat response show good judgment about underdetermined requirements.
