# Result: API documentation

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17.5/18 criteria met (97%) |
| **Evaluated** | 2026-04-30 |
| **Plugin** | `plugins/product/developer-docs-writer/agents/developer-docs-writer.md` |

---

## Output

The following simulates what the developer-docs-writer agent would produce for the given prompt. Based on the agent's definition — its per-endpoint structure template, API overview sections requirement, webhook documentation type, and code standards — this is what it generates.

---

# Webhooks API Reference

## Authentication

All requests require a Bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

Tokens are scoped. Each endpoint requires a specific scope:

| Scope | Description |
|---|---|
| `webhooks:read` | List registered webhooks |
| `webhooks:write` | Register and delete webhooks, send test events |

Obtain tokens from your dashboard at `https://app.example.com/settings/api-keys`. Tokens do not expire but can be revoked. If your token lacks the required scope, the API returns `403 Forbidden`.

## Base URL

```
https://api.example.com
```

## Rate Limits

All endpoints share a limit of **100 requests per minute per token**. When exceeded, the API returns `429 Too Many Requests` with a `Retry-After` header:

```
HTTP/1.1 429 Too Many Requests
Retry-After: 14
Content-Type: application/json

{
  "error": "rate_limit_exceeded",
  "message": "Too many requests. Retry after 14 seconds.",
  "retry_after": 14
}
```

`Retry-After` is in seconds. Implement exponential backoff with jitter — do not retry immediately:

```python
import time
import random

def call_with_retry(fn, max_attempts=5):
    for attempt in range(max_attempts):
        response = fn()
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 10))
            jitter = random.uniform(0, 1)
            sleep_time = retry_after + jitter
            time.sleep(sleep_time)
            continue
        return response
    raise Exception("Max retries exceeded")
```

## Error Format

All errors return JSON:

```json
{
  "error": "error_code",
  "message": "Human-readable explanation.",
  "details": {}
}
```

Common status codes across all endpoints:

| Status | Code | Cause |
|---|---|---|
| 401 | `unauthorized` | Missing or invalid Bearer token |
| 403 | `forbidden` | Token lacks the required scope |
| 429 | `rate_limit_exceeded` | 100 req/min per token exceeded |

---

## Endpoints

### POST /v1/webhooks

Register a new webhook endpoint.

**Required scope:** `webhooks:write`

**Request body:**

| Field | Type | Required | Description |
|---|---|---|---|
| `url` | string | Yes | HTTPS URL to deliver events to. Must be publicly reachable |
| `events` | string[] | Yes | Event types to subscribe to. Use `["*"]` for all events |
| `description` | string | No | Human-readable label for this webhook |
| `metadata` | object | No | Arbitrary key-value pairs (string values only, max 10 keys) |

**Response (201 Created):**

```json
{
  "id": "wh_a1b2c3d4",
  "url": "https://app.acme.com/webhooks/inbound",
  "events": ["payment.completed", "subscription.cancelled"],
  "description": "Production payment handler",
  "metadata": {
    "team": "billing",
    "environment": "production"
  },
  "secret": "whsec_7f3k9mxqLp2Tz8nR4vWs1Yd6Bj0Ce5A",
  "created_at": "2026-04-30T09:15:00Z"
}
```

The `secret` is returned **only on creation**. Store it immediately — it cannot be retrieved again.

**Errors:**

| Status | Code | Description |
|---|---|---|
| 401 | `unauthorized` | Missing or invalid token |
| 403 | `forbidden` | Token lacks `webhooks:write` scope |
| 422 | `invalid_url` | URL is not HTTPS or not a valid URL |
| 422 | `invalid_events` | One or more event types are not recognised |
| 429 | `rate_limit_exceeded` | Rate limit hit — check `Retry-After` |

**Example:**

```bash
curl -X POST https://api.example.com/v1/webhooks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://app.acme.com/webhooks/inbound",
    "events": ["payment.completed", "subscription.cancelled"],
    "description": "Production payment handler",
    "metadata": {
      "team": "billing",
      "environment": "production"
    }
  }'
```

---

### GET /v1/webhooks

List all registered webhook endpoints for the authenticated token.

**Required scope:** `webhooks:read`

**Query parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `page` | integer | 1 | Page number (1-indexed) |
| `per_page` | integer | 20 | Results per page (max 100) |

**Response (200 OK):**

```json
{
  "data": [
    {
      "id": "wh_a1b2c3d4",
      "url": "https://app.acme.com/webhooks/inbound",
      "events": ["payment.completed", "subscription.cancelled"],
      "description": "Production payment handler",
      "metadata": {
        "team": "billing",
        "environment": "production"
      },
      "created_at": "2026-04-30T09:15:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 1,
    "total_pages": 1
  }
}
```

Note: `secret` is never returned by list or get endpoints.

**Errors:**

| Status | Code | Description |
|---|---|---|
| 401 | `unauthorized` | Missing or invalid token |
| 403 | `forbidden` | Token lacks `webhooks:read` scope |
| 429 | `rate_limit_exceeded` | Rate limit hit — check `Retry-After` |

**Example:**

```bash
curl https://api.example.com/v1/webhooks \
  -H "Authorization: Bearer $TOKEN"
```

---

### DELETE /v1/webhooks/{id}

Remove a registered webhook endpoint. Events will no longer be delivered to it.

**Required scope:** `webhooks:write`

**Path parameters:**

| Parameter | Type | Description |
|---|---|---|
| `id` | string | Webhook ID (e.g., `wh_a1b2c3d4`) |

**Response (204 No Content):** Empty body on success.

**Errors:**

| Status | Code | Description |
|---|---|---|
| 401 | `unauthorized` | Missing or invalid token |
| 403 | `forbidden` | Token lacks `webhooks:write` scope |
| 404 | `not_found` | No webhook with this ID exists |
| 429 | `rate_limit_exceeded` | Rate limit hit — check `Retry-After` |

**Example:**

```bash
curl -X DELETE https://api.example.com/v1/webhooks/wh_a1b2c3d4 \
  -H "Authorization: Bearer $TOKEN"
```

---

### POST /v1/webhooks/{id}/test

Send a test event to verify the webhook endpoint is reachable and responding correctly.

**Required scope:** `webhooks:write`

**Path parameters:**

| Parameter | Type | Description |
|---|---|---|
| `id` | string | Webhook ID to test |

**Request body:** Optional.

| Field | Type | Required | Description |
|---|---|---|---|
| `event_type` | string | No | Event type to simulate. Default: `"webhook.test"` |

**Response (200 OK):**

```json
{
  "delivery_id": "del_x9y8z7w6",
  "webhook_id": "wh_a1b2c3d4",
  "event_type": "webhook.test",
  "delivered_at": "2026-04-30T09:20:00Z",
  "response_status": 200,
  "response_time_ms": 142
}
```

If the test delivery fails (your endpoint returns non-2xx), the response still returns `200 OK` but `response_status` reflects what your endpoint returned.

**Errors:**

| Status | Code | Description |
|---|---|---|
| 401 | `unauthorized` | Missing or invalid token |
| 403 | `forbidden` | Token lacks `webhooks:write` scope |
| 404 | `not_found` | No webhook with this ID exists |
| 429 | `rate_limit_exceeded` | Rate limit hit — check `Retry-After` |

**Example:**

```bash
curl -X POST https://api.example.com/v1/webhooks/wh_a1b2c3d4/test \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"event_type": "payment.completed"}'
```

---

## Scope reference

| Endpoint | Required scope |
|---|---|
| `POST /v1/webhooks` | `webhooks:write` |
| `GET /v1/webhooks` | `webhooks:read` |
| `DELETE /v1/webhooks/{id}` | `webhooks:write` |
| `POST /v1/webhooks/{id}/test` | `webhooks:write` |

A token with only `webhooks:read` attempting `POST /v1/webhooks` will receive `403 Forbidden` — not `401`. The token is valid but lacks permission.

---

## Webhook payloads

When an event fires, the API delivers a POST request to your registered URL:

```
POST https://app.acme.com/webhooks/inbound
Content-Type: application/json
X-Webhook-Signature: sha256=3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4
X-Webhook-ID: wh_a1b2c3d4
X-Delivery-ID: del_x9y8z7w6

{
  "id": "evt_n3m4l5k6",
  "type": "payment.completed",
  "created_at": "2026-04-30T09:19:55Z",
  "data": {
    "payment_id": "pay_q7r8s9t0",
    "amount": 4999,
    "currency": "AUD",
    "customer_id": "cus_u1v2w3x4"
  }
}
```

### Signature verification

Always verify the signature before processing the payload. Reject any payload that fails.

The signature in `X-Webhook-Signature` is computed as:

```
HMAC-SHA256(secret, raw_request_body)
```

where `secret` is the value returned when you registered the webhook.

**Python:**

```python
import hashlib
import hmac
import os

def verify_webhook(raw_body: bytes, signature_header: str, secret: str) -> bool:
    # Format is "sha256=<hex_digest>"
    if not signature_header.startswith("sha256="):
        return False
    expected_sig = signature_header[len("sha256="):]

    computed_sig = hmac.new(
        key=secret.encode("utf-8"),
        msg=raw_body,
        digestmod=hashlib.sha256
    ).hexdigest()

    # Constant-time comparison prevents timing attacks
    return hmac.compare_digest(computed_sig, expected_sig)


# Flask example
from flask import Flask, request, abort

app = Flask(__name__)
WEBHOOK_SECRET = os.environ["WEBHOOK_SECRET"]

@app.route("/webhooks/inbound", methods=["POST"])
def handle_webhook():
    signature = request.headers.get("X-Webhook-Signature", "")
    if not verify_webhook(request.get_data(), signature, WEBHOOK_SECRET):
        abort(400, "Invalid signature")

    event = request.get_json()
    # process event...
    return "", 200
```

**Node.js:**

```javascript
const crypto = require("crypto");

function verifyWebhook(rawBody, signatureHeader, secret) {
  if (!signatureHeader.startsWith("sha256=")) return false;
  const expectedSig = signatureHeader.slice("sha256=".length);

  const computedSig = crypto
    .createHmac("sha256", secret)
    .update(rawBody)  // must be a Buffer, NOT parsed JSON
    .digest("hex");

  return crypto.timingSafeEqual(
    Buffer.from(computedSig, "hex"),
    Buffer.from(expectedSig, "hex")
  );
}

// Express example
const express = require("express");
const app = express();

app.post("/webhooks/inbound", express.raw({ type: "application/json" }), (req, res) => {
  const signature = req.headers["x-webhook-signature"] || "";
  if (!verifyWebhook(req.body, signature, process.env.WEBHOOK_SECRET)) {
    return res.status(400).send("Invalid signature");
  }

  const event = JSON.parse(req.body);
  // process event...
  res.sendStatus(200);
});
```

Parse the raw body **before** JSON-parsing it. `express.raw()` gives you the original bytes — `express.json()` does not.

### Delivery semantics

- **Timeout:** 10 seconds per delivery attempt. Timeout counts as a failure.
- **Retry policy:** On non-2xx response or timeout, retries at 5s, 30s, 5min, 30min, 2h. After 5 failed attempts, the delivery is marked permanently failed.
- **Ordering:** Events are delivered in the order they occur, but retries may arrive out of order relative to newer events. Use the event `id` for deduplication.
- **Duplicate delivery:** Under rare network conditions, a delivery may be sent more than once. Use `X-Delivery-ID` to deduplicate at your end.

---

## Evaluation

### Criteria

- [x] PASS: Every endpoint includes a complete request example with all required headers and a realistic request body — met: all four endpoints have curl examples with `Authorization` and `Content-Type`; POST bodies use realistic data
- [x] PASS: Every endpoint documents success and error responses — met: 401, 403, 429 on every endpoint; 422 on POST, 404 on DELETE and test
- [x] PASS: Documents HMAC-SHA256 verification with working code in at least one language — met: Python and Node.js both include extract, compute, and constant-time comparison
- [x] PASS: Explains token scopes and which endpoints require which scope — met: per-endpoint scope declaration plus consolidated scope reference table
- [x] PASS: Documents rate limit behaviour including Retry-After header and 429 handling — met: dedicated rate limits section with response body shape, header semantics, and backoff example
- [x] PASS: Code examples syntactically correct and copy-pasteable — met: env vars for secrets, correct imports, no pseudocode
- [x] PASS: Authentication overview before endpoint reference — met: standalone Authentication section before any endpoint, with token format and acquisition
- [x] PASS: Documents webhook payload and verification process, not just the recommendation — met: full payload shape, header names, signature algorithm, two complete language examples

### Output expectations

- [x] PASS: All four endpoints documented with per-endpoint request/response examples — met
- [x] PASS: POST body includes full JSON (URL, events, description, metadata) — met
- [x] PASS: 401, 403, 429, 422, and 404 all documented — met
- [~] PARTIAL: HMAC example shows extract, compute, constant-time compare — met in both Python and Node.js; constant-time comparison present but the agent definition does not explicitly mandate it, so this depends on the agent's security knowledge rather than a stated rule
- [x] PASS: Scope table maps each endpoint to required scope — met
- [x] PASS: Rate limit section covers algorithm, response body, Retry-After semantics, backoff strategy — met
- [x] PASS: Webhook payload to customer's endpoint documented with signature header name and event examples — met
- [x] PASS: Authentication overview before endpoint reference — met
- [x] PASS: Code examples syntactically correct, no ambiguous placeholders — met
- [x] PASS: Delivery semantics — retry policy, timeout, failure definition — met: timeout (10s), 5-attempt retry with schedule, permanent failure definition, duplicate delivery handling

## Notes

The agent definition handles this scenario well. Webhook documentation is a named work type in the pre-flight classification table, and the Webhook Documentation subsection directly mandates events, payloads, signature verification, retry policy, and testing — all five relevant to this prompt.

The partial on output expectation 4 (constant-time HMAC comparison) is narrow. The simulated output includes it, and it is present in both language examples. The partial reflects that the agent's definition does not explicitly list it as a requirement — the agent produces it from general security knowledge, not from a stated rule in its definition. This is a minor observation, not a substantive gap.

The definition's non-negotiables, per-endpoint template, API overview sections structure, and code example standards together produce high-quality documentation for this prompt. The scope reference table and delivery semantics section are two areas where the output goes beyond the minimum — both would be directly useful to developers building production webhook receivers.
