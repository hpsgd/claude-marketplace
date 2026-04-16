# Test: API documentation

Scenario: A developer needs docs written for a REST API that handles webhook delivery, including authentication and rate limiting behaviour.

## Prompt


Write documentation for our webhooks API. Here's what it does:

- POST /v1/webhooks — register a new webhook endpoint
- GET /v1/webhooks — list all registered webhooks
- DELETE /v1/webhooks/{id} — remove a webhook
- POST /v1/webhooks/{id}/test — send a test event to verify the endpoint works

Auth: Bearer token in Authorization header. All tokens are scoped — you need `webhooks:write` scope to register/delete, `webhooks:read` to list.

Rate limits: 100 requests/minute per token. Returns 429 with Retry-After header when exceeded.

Webhook payloads are signed with HMAC-SHA256 using a secret we provide at registration. Customers must verify the signature or we recommend rejecting the payload.

## Criteria


- [ ] PASS: Every endpoint includes a complete request example with all required headers (Authorization, Content-Type) and a realistic request body
- [ ] PASS: Every endpoint documents both success responses and error responses — at minimum: 401 Unauthorized, 403 Forbidden (wrong scope), 429 Too Many Requests, and relevant 4xx for invalid input
- [ ] PASS: Documents the HMAC-SHA256 signature verification process with a working code example in at least one language
- [ ] PASS: Explains token scopes (webhooks:read vs webhooks:write) and which endpoints require which scope
- [ ] PASS: Documents rate limit behaviour including the Retry-After header and how clients should handle 429 responses
- [ ] PASS: Code examples are syntactically correct and copy-pasteable — not pseudocode or placeholder-heavy
- [ ] PARTIAL: Includes a quick-start or authentication section before the endpoint reference — partial credit if auth is documented inline per endpoint but not as a standalone overview
- [ ] PASS: Documents what a webhook payload looks like and how to verify the signature, not just that verification should happen
