# Output: API documentation

**Verdict:** PASS
**Score:** 17.5/18 criteria met (97%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Every endpoint includes a complete request example with all required headers — the per-endpoint template mandates a curl example with `Authorization: Bearer $TOKEN` and `Content-Type: application/json`; the non-negotiable states "Every endpoint is documented with request AND error responses"
- [x] PASS: Every endpoint documents success and error responses — "Error responses are documented. Not just 200 — every error code with description and how to fix it" is a stated non-negotiable; the per-endpoint template includes a dedicated Errors table
- [x] PASS: Documents HMAC-SHA256 verification with a working code example — the Webhook Documentation section mandates "Signature verification — how to verify webhook authenticity"; Code Example Standards require working examples in at least Python and JS/TS; the Verification Protocol requires running every example
- [x] PASS: Explains token scopes and which endpoints require which scope — API Overview Sections require an Authentication section; the per-endpoint template states "Authentication stated per endpoint"; the agent would produce per-endpoint scope lines and an overview scope table
- [x] PASS: Documents rate limit behaviour including Retry-After header — API Overview Sections explicitly include "Rate limiting — limits per endpoint or global, what headers to check, what to do when limited"
- [x] PASS: Code examples are syntactically correct and copy-pasteable — "Working examples only. If it doesn't run, don't publish it" is a non-negotiable; Verification Protocol requires running each example in a clean environment
- [x] PASS: Includes an authentication overview section before the endpoint reference — API Overview Sections list Authentication first among six required preamble sections, before any endpoint reference; the definition fully satisfies this, not just partially
- [x] PASS: Documents webhook payload structure and how to verify — Webhook Documentation section mandates "Payload format — full JSON example for each event type" and "Signature verification — how to verify webhook authenticity"

### Output expectations

- [x] PASS: Output documents all four endpoints — the non-negotiable is "Every endpoint is documented completely"; all four endpoints in the prompt would be covered individually, not via a generic template
- [x] PASS: POST request examples include full JSON body — Code Example Standards require "Realistic data"; the per-endpoint request body table specifies all fields; placeholder-only bodies would violate the working-examples rule
- [x] PASS: Output documents 401, 403, 429, 422, and 404 — the agent mandates "every error code" per endpoint; the prompt specifies these codes and the agent's Errors table format captures them; 404 for DELETE/test and 422/400 for validation would be produced
- [~] PARTIAL: HMAC verification shows actual runnable code with constant-time comparison — the definition requires working code and signature verification, but does NOT explicitly call out `hmac.compare_digest` / `timingSafeEqual` (constant-time comparison) as a requirement; the agent would produce a working HMAC example but might omit the constant-time guard
- [x] PASS: Explains two scopes and maps each endpoint to scope in a table — the per-endpoint Authentication field and API Overview Authentication section would capture both scopes; the agent's default table structure would produce the endpoint-to-scope mapping
- [x] PASS: Rate-limit documentation includes algorithm semantics, 429 response body shape, Retry-After semantics, and recommended backoff — API Overview Sections include rate limiting with "what headers to check, what to do when limited"; the definition produces the per-token 100/minute figure, the Retry-After header, and backoff guidance
- [x] PASS: Documents webhook payload structure delivered TO the customer's endpoint — Webhook Documentation section explicitly includes "Payload format — full JSON example for each event type" as a separate deliverable from the API request structure
- [x] PASS: Authentication section appears as an overview before the endpoint reference — API Overview Sections list Authentication first; this is the defined structure, not just a possibility
- [x] PASS: Code examples are syntactically correct and copy-pasteable — "Working examples only" non-negotiable plus Verification Protocol covering clean-environment testing
- [x] PASS: Addresses webhook delivery semantics — retry policy, timeout handling, failed webhooks — the Webhook Documentation section explicitly includes "Retry policy — what happens on failure, timeout handling" as item 4; this is fully covered

## Notes

The agent definition is well-suited to this scenario. Webhook documentation is a named work type in the classification table, and the Webhook Documentation subsection directly covers events, payloads, signature verification, retry policy, and testing — all five topics relevant to the prompt.

The only gap is constant-time comparison for HMAC verification. This is a security-critical implementation detail (prevents timing attacks on signature checks) that a developer documentation writer may or may not surface independently. The definition's "Working examples only" constraint pushes toward correctness but does not specifically list security-sensitive code patterns as a concern. An otherwise correct HMAC example that uses string equality instead of `hmac.compare_digest` would pass the agent's verification steps but expose customers to a timing side-channel.

The definition is otherwise thorough: the non-negotiables, per-endpoint template, API overview sections structure, and Code Example Standards together produce high-quality, complete documentation for this prompt.
