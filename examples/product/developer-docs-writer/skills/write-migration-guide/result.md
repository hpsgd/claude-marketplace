# Write Migration Guide

Scenario: Testing whether the write-migration-guide skill requires before/after code examples for every breaking change, a rollback plan, and a deprecation timeline with actual dates.

## Prompt

> /developer-docs-writer:write-migration-guide for our API v2 to v3 upgrade — we renamed several fields, changed authentication from API keys to OAuth 2.0, and removed two deprecated endpoints.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Migration guide written to `docs/api/migration-v2-to-v3.md`. All 7 required sections are in place:

- **What's changing** with before/after curl examples
- **Impact** table with honest effort estimate (2-4 hours) and who can skip
- **4 numbered migration steps** with copy-paste code for auth, URL updates, field renames, and endpoint replacements
- **Breaking changes table** with 8 rows (every change, including the `usr_`→`acc_` ID prefix)
- **Deprecation timeline** with absolute dates: GA 2026-05-01, warnings 2026-08-01, sunset 2027-02-01
- **Rollback plan** with point of no return (when you store `acc_`-prefixed IDs without retaining the originals)
- **Verification** with a curl-based check script and troubleshooting table

Before publishing, replace the placeholder URLs (`api.example.com`, `auth.example.com`), field names, and endpoint paths with your real ones.

### Artifacts written

#### `work/docs/api/migration-v2-to-v3.md`

```
# Migration guide: API v2 to v3

## What's changing

### Change summary

| Element | Detail |
|---|---|
| **What changed** | Authentication changed from static API keys to OAuth 2.0 client credentials. Four response fields renamed. Two deprecated endpoints removed with no fallback. |
| **Why it changed** | API keys have no expiry, no per-scope control, and can only be revoked by rotating the key. OAuth 2.0 client credentials solves all three. The field renames align the schema with the account model introduced in v2.6 — `user_id` was never accurate once an account could have multiple users. The two removed endpoints have had documented replacements since v2.4. |
| **Old version** | v2 |
| **New version** | v3 |
| **Change type** | API breaking change |

### Before / after overview

**Before (v2) — API key auth:**

```bash
curl https://api.example.com/v2/accounts \
  -H "Authorization: Bearer sk_live_abc123xyz"
```

**After (v3) — OAuth 2.0 access token:**

```bash
# Step 1: exchange client credentials for an access token
curl https://auth.example.com/oauth/token \
  -d "grant_type=client_credentials" \
  -d "client_id=your_client_id" \
  -d "client_secret=your_client_secret" \
  -d "scope=accounts:read"

# Step 2: use the access token
curl https://api.example.com/v3/accounts \
  -H "Authorization: Bearer eyJhbGc..."
```

The core difference: access tokens expire (default 1 hour) and carry scopes. Your application must handle token refresh. A static API key never had to.

---

## Impact assessment

### Impact

| Dimension | Detail |
|---|---|
| **Who is affected** | All integrations calling the v2 API. No exceptions — the auth change alone requires updates to every request. |
| **What code needs to change** | Auth logic (token acquisition and refresh), any code that constructs or reads `user_id`, `created`, `username`, or `is_active` fields, and any calls to `GET /v2/users/me` or `POST /v2/messages/send`. |
| **Estimated migration effort** | 2–4 hours for a typical integration. Add a day if your app has no existing OAuth 2.0 client or if field names are spread across many models. |
| **Risk level** | Medium. The auth change is significant but mechanical. No data migration required. |
| **Can old and new coexist?** | Yes, until 2027-02-01. Both versions run in parallel. You can migrate incrementally. |

### Who does not need to migrate

If you are on a managed integration (Zapier, Make, HubSpot native connector), your connector vendor handles the migration. Check with them before touching anything.

---

## Migration steps

### Prerequisites

- [ ] Read the full breaking changes table below before starting
- [ ] Register an OAuth 2.0 client application in the developer portal and note your `client_id` and `client_secret`
- [ ] Identify which scopes your integration needs (see [scope reference](../api-reference.md#scopes))
- [ ] If you store API responses in a database, note which tables hold `user_id`, `created`, `username`, or `is_active` from our API

### Step 1: Add an OAuth 2.0 token client

Your integration needs to acquire and cache access tokens. Tokens expire after 3,600 seconds. You must refresh before expiry, not after getting a 401.

**Before (v2) — one static key, set once:**

```bash
export API_KEY=sk_live_abc123xyz
```

**After (v3) — token acquisition function:**

```python
import time
import requests

TOKEN_URL = "https://auth.example.com/oauth/token"
_token_cache = {"token": None, "expires_at": 0}

def get_access_token(client_id: str, client_secret: str, scope: str) -> str:
    now = time.time()
    if _token_cache["token"] and now < _token_cache["expires_at"] - 60:
        return _token_cache["token"]

    resp = requests.post(TOKEN_URL, data={
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": scope,
    })
    resp.raise_for_status()
    data = resp.json()

    _token_cache["token"] = data["access_token"]
    _token_cache["expires_at"] = now + data["expires_in"]
    return _token_cache["token"]
```

The 60-second buffer on the expiry check prevents clock-skew rejections. Do not request a new token on every API call — the token endpoint is rate-limited at 10 requests/minute per client.

### Step 2: Update all API base URLs from v2 to v3

Find every hardcoded or configured URL pointing at `/v2/` and change it to `/v3/`.

**Before:**

```bash
BASE_URL=https://api.example.com/v2
```

**After:**

```bash
BASE_URL=https://api.example.com/v3
```

If you have a config file or environment variable, this is a one-line change. If URLs are spread through the codebase, grep first:

```bash
grep -r "api.example.com/v2" --include="*.py" --include="*.ts" --include="*.js" .
```

### Step 3: Replace the four renamed fields

These fields were renamed in the API response. Update any code that reads, stores, or forwards these field names.

**`user_id` → `account_id`:**

```python
# Before
owner = response["user_id"]

# After
owner = response["account_id"]
```

**`created` → `created_at`:**

```python
# Before
timestamp = record["created"]

# After
timestamp = record["created_at"]
```

**`username` → `display_name`:**

```python
# Before
label = user["username"]

# After
label = user["display_name"]
```

**`is_active` → `status`:**

This one requires more than a rename. `is_active` was a boolean. `status` is a string enum with values `"active"`, `"inactive"`, and `"suspended"`. If your code did `if user["is_active"]:`, that still works for active/inactive. But suspended accounts will now read as `"suspended"` (truthy) rather than `False`. Audit any boolean checks.

```python
# Before
if user["is_active"]:
    allow_access()

# After — handle all three states explicitly
if user["status"] == "active":
    allow_access()
elif user["status"] == "suspended":
    show_suspended_message()
else:
    deny_access()
```

### Step 4: Replace the two removed endpoints

These endpoints return `410 Gone` in v3. They have no soft deprecation period in v3 — calling them fails immediately.

**`GET /v2/users/me` → `GET /v3/accounts/current`:**

```bash
# Before
curl https://api.example.com/v2/users/me \
  -H "Authorization: Bearer sk_live_abc123xyz"

# After
curl https://api.example.com/v3/accounts/current \
  -H "Authorization: Bearer eyJhbGc..."
```

The response schema is the same except for the renamed fields from Step 3.

**`POST /v2/messages/send` → `POST /v3/messages`:**

```bash
# Before
curl -X POST https://api.example.com/v2/messages/send \
  -H "Authorization: Bearer sk_live_abc123xyz" \
  -H "Content-Type: application/json" \
  -d '{"recipient_id": "usr_123", "body": "Hello"}'

# After
curl -X POST https://api.example.com/v3/messages \
  -H "Authorization: Bearer eyJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{"recipient_id": "acc_123", "body": "Hello"}'
```

Note: `recipient_id` still takes an ID, but the ID format changed from `usr_` prefix to `acc_` prefix to reflect the account model. You will need to look up the new `account_id` values for any IDs you have stored.

### Step 5: Verify migration

See the [Verification section](#verification) below.

---

## Breaking changes

### Breaking changes table

| # | What changed | Old behaviour | New behaviour | Action required | Example |
|---|---|---|---|---|---|
| 1 | Authentication mechanism | Static API key in `Authorization: Bearer` header | OAuth 2.0 access token (client credentials grant) | Implement token acquisition and refresh | Step 1 above |
| 2 | Field: `user_id` | Present in account/user responses | Removed; replaced by `account_id` | Rename all reads and writes | `response["account_id"]` |
| 3 | Field: `created` | ISO 8601 timestamp string | Removed; replaced by `created_at` | Rename all reads and writes | `record["created_at"]` |
| 4 | Field: `username` | Display string | Removed; replaced by `display_name` | Rename all reads and writes | `user["display_name"]` |
| 5 | Field: `is_active` | Boolean (`true`/`false`) | Removed; replaced by `status` (enum: `"active"`, `"inactive"`, `"suspended"`) | Rename and expand boolean checks to handle three states | Step 3 above |
| 6 | Endpoint: `GET /v2/users/me` | Returns current user profile | Returns `410 Gone` | Change to `GET /v3/accounts/current` | Step 4 above |
| 7 | Endpoint: `POST /v2/messages/send` | Sends a message | Returns `410 Gone` | Change to `POST /v3/messages` | Step 4 above |
| 8 | ID prefix for accounts | `usr_` prefix (e.g. `usr_abc123`) | `acc_` prefix (e.g. `acc_abc123`) | Update any stored IDs or hardcoded ID references | `recipient_id: "acc_123"` |

### Non-breaking changes (no action required)

| What changed | Old behaviour | New behaviour | Why no action needed |
|---|---|---|---|
| Pagination default page size | 20 results per page | 20 results per page (unchanged) | Included for clarity — this did not change |
| Rate limit headers | `X-RateLimit-*` headers | `X-RateLimit-*` headers (unchanged) | No change |
| Webhook payload format | Same format | Same format | Webhooks are not versioned — v3 does not affect them |
| Error response schema | `{"error": "...", "code": "..."}` | Same shape | Codes may be new but the structure is backwards compatible |

---

## Deprecation timeline

| Date | Event | Action required |
|---|---|---|
| 2026-05-01 | v3 GA | Migration guide available. Start migrating. |
| 2026-08-01 | v2 deprecation warning added | v2 responses include a `Deprecation: true` header and a `Sunset: Sat, 01 Nov 2026` header. v2 still works. |
| 2026-11-01 | v2 enters maintenance mode | Security fixes only. No new features will be added to v2. |
| 2027-02-01 | v2 end-of-life | v2 returns `410 Gone` for all endpoints. Integrations not yet migrated will stop working. |

Nine months is the migration window. That's deliberate — the auth change is the hard part, and some teams will need procurement or security review for OAuth 2.0 credentials. If your deadline is tighter, email api-support@example.com and we can discuss.

### Running v2 and v3 simultaneously

Both versions are live and independent during the transition. You can migrate endpoint by endpoint rather than doing a big-bang cutover. The only dependency: once you switch to OAuth 2.0 tokens, those tokens work on both v2 and v3. You do not need to keep the API key alive once you've switched auth.

---

## Rollback plan

If the migration breaks something and you need to revert, the path back is straightforward — as long as you haven't cancelled your API key yet.

**Do not cancel your v2 API key until you are fully on v3 and have run in production for at least a week.**

### Prerequisites for rollback

- [ ] Your v2 API key must still be active (not revoked or expired)
- [ ] You must not have deleted any `user_id`, `created`, `username`, or `is_active` data that you translated during the migration

### Rollback steps

1. Revert your application to use the v2 base URL (`https://api.example.com/v2`)
2. Revert the `Authorization` header to use your static API key
3. Revert field name reads back to `user_id`, `created`, `username`, and `is_active`
4. Revert any calls to `GET /v3/accounts/current` back to `GET /v2/users/me`
5. Revert any calls to `POST /v3/messages` back to `POST /v2/messages/send`
6. Deploy and verify the rollback worked (run the manual checklist below)

### Rollback limitations

- If you have stored `acc_` prefixed IDs in your database after migration, those IDs will not work against v2. You will need to convert them back to `usr_` prefix or re-fetch them from v2.
- The OAuth 2.0 client registration cannot be rolled back, but it also causes no harm to leave in place.
- Rollback is possible at any point before 2027-02-01. After that date, v2 is gone and rollback is not possible.

### Point of no return

The point of no return is when you store `acc_`-prefixed account IDs from v3 responses into a database without retaining the original `usr_`-prefixed IDs. At that point, rolling back requires a data migration. Keep both IDs during the transition period if your application stores them.

---

## Verification

### Automated verification

Run these checks after migration to confirm everything is wired correctly:

```bash
# 1. Confirm token acquisition works
TOKEN=$(curl -s https://auth.example.com/oauth/token \
  -d "grant_type=client_credentials" \
  -d "client_id=$CLIENT_ID" \
  -d "client_secret=$CLIENT_SECRET" \
  -d "scope=accounts:read messages:write" \
  | jq -r '.access_token')

echo "Token acquired: ${TOKEN:0:20}..."

# 2. Confirm v3 account endpoint responds
curl -s https://api.example.com/v3/accounts/current \
  -H "Authorization: Bearer $TOKEN" \
  | jq '{account_id, display_name, status, created_at}'

# 3. Confirm old endpoint returns 410
STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
  https://api.example.com/v3/users/me \
  -H "Authorization: Bearer $TOKEN")
echo "Old endpoint status: $STATUS (expected 410)"

# 4. Confirm v2 still works with API key (during transition only)
curl -s https://api.example.com/v2/users/me \
  -H "Authorization: Bearer $API_KEY" \
  | jq '{user_id, username, is_active}'
```

### Manual verification checklist

- [ ] Token acquisition returns an `access_token` and `expires_in` field
- [ ] Token expires after approximately 3,600 seconds
- [ ] `GET /v3/accounts/current` returns `account_id` (not `user_id`)
- [ ] `GET /v3/accounts/current` returns `status: "active"` (not `is_active: true`)
- [ ] `GET /v3/accounts/current` returns `display_name` (not `username`)
- [ ] `GET /v3/accounts/current` returns `created_at` (not `created`)
- [ ] `POST /v3/messages` returns 201 with a message ID
- [ ] `GET /v2/users/me` still works with API key (confirms v2 is untouched)
- [ ] No 401 errors appearing in logs after deploy

### Common post-migration issues

| Symptom | Cause | Fix |
|---|---|---|
| `401 Unauthorized` on first request | Token not acquired before the first API call | Check token acquisition runs at startup or is lazy-loaded before the first request |
| `401 Unauthorized` after ~1 hour | Token expired; no refresh logic | Add the 60-second pre-expiry buffer check from Step 1 |
| `400 Bad Request` from token endpoint | Wrong scope name | Check scope values against the [scope reference](../api-reference.md#scopes) — scopes are case-sensitive |
| `404 Not Found` on `/v3/accounts/current` | Still calling `/v3/users/me` (old path with new version prefix) | The endpoint path changed too, not just the version prefix |
| `422 Unprocessable Entity` on `POST /v3/messages` | Sending `usr_` prefixed ID in `recipient_id` | Look up the `account_id` for the recipient and use the `acc_` prefix |
| `KeyError: 'user_id'` in your application | Field renamed but code not updated | Search for remaining v2 field names: `grep -r "user_id\|\"created\"\|is_active\|username" src/` |

---

*Migration: v2 to v3*
*Estimated effort: 2–4 hours (add 1 day if no existing OAuth client)*
*Deprecation date: 2026-08-01*
*v2 end-of-life: 2027-02-01*
*Last updated: 2026-05-01*

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.5/18.0 (86%) |
| Evaluated | 2026-05-01 |
| Target duration | 423794 ms |
| Target cost | $1.4764 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires before/after code examples for every breaking change — prose description alone is not sufficient | PASS | Every breaking change in Steps 1-4 has explicit before/after code: auth (curl + Python), URL change (bash), all four field renames (Python), both removed endpoints (curl). Breaking changes table also includes an 'Example' column. |
| c2 | Skill requires a rollback plan — including limitations and the point of no return after which rollback is impossible | PASS | Dedicated 'Rollback plan' section with prerequisites, numbered rollback steps, 'Rollback limitations' subsection, and explicit 'Point of no return' subsection: 'The point of no return is when you store acc_-prefixed account IDs from v3 responses into a database without retaining the original usr_-prefixed IDs.' |
| c3 | Skill requires a deprecation timeline with actual dates or relative timeframes — "eventually deprecated" is explicitly rejected | PASS | Deprecation timeline table lists four absolute dates: 2026-05-01 (v3 GA), 2026-08-01 (deprecation warning), 2026-11-01 (maintenance mode), 2027-02-01 (end-of-life). No vague language. |
| c4 | Skill requires an impact assessment — who is affected, what code must change, estimated effort, and who is NOT affected | PASS | Impact section covers: affected party ('All integrations calling the v2 API. No exceptions'), what code changes (auth logic, field names, endpoint URLs), effort estimate (2–4 hours), and explicitly who is NOT affected ('managed integrations (Zapier, Make, HubSpot native connector)'). |
| c5 | Skill requires an exhaustive breaking changes table — each change gets its own row, not combined into "various improvements" | PASS | Breaking changes table has 8 separate rows: authentication mechanism, user_id, created, username, is_active, GET /v2/users/me endpoint, POST /v2/messages/send endpoint, and ID prefix change (usr_ → acc_). |
| c6 | Skill requires verification steps so developers can confirm the migration succeeded | PASS | Verification section includes: automated bash/curl script checking token acquisition, v3 endpoint response, 410 from old endpoint, and v2 still working; a manual checklist with 9 items; and a troubleshooting table for common post-migration issues. |
| c7 | Skill provides guidance on coexistence — whether old and new can run simultaneously during migration — partial credit if this is mentioned but no specific dual-write guidance is given | PARTIAL | Section 'Running v2 and v3 simultaneously' states: 'Both versions are live and independent during the transition. You can migrate endpoint by endpoint.' Mentions OAuth tokens work on both v2 and v3. However no specific dual-write pattern or data synchronization strategy is provided. |
| c8 | Skill requires honest effort estimates — the rule that underestimating effort is a form of dishonesty is present | PASS | The guide includes an effort estimate with qualifier: '2–4 hours for a typical integration. Add a day if your app has no existing OAuth 2.0 client or if field names are spread across many models.' The footer also explicitly restates the estimate. |
| c9 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The captured output contains only a chat response and the migration guide markdown file. No skill definition file with YAML frontmatter is shown anywhere in the artifacts. Cannot verify name, description, or argument-hint fields. |
| c10 | Output's breaking-changes table lists each change as a separate row — every renamed field (with old name → new name), the auth shift (API keys → OAuth 2.0), and each removed endpoint by name — not combined into "various improvements" | PASS | 8-row table with separate entries for auth (row 1), user_id→account_id (row 2), created→created_at (row 3), username→display_name (row 4), is_active→status (row 5), GET /v2/users/me (row 6), POST /v2/messages/send (row 7), usr_→acc_ prefix (row 8). |
| c11 | Output's auth migration section walks through OAuth 2.0 setup — Authorization Code flow vs Client Credentials, where to register the app, how to obtain access tokens, refresh-token handling — with code examples, not just "switch to OAuth" | PARTIAL | Step 1 provides detailed Python token acquisition code, covers client credentials grant, mentions developer portal registration, and handles refresh with 60-second buffer. However, there is no comparison of Authorization Code flow vs Client Credentials — only client credentials is discussed, with no explanation of why or when the other flow applies. |
| c12 | Output's before/after code examples show the actual code change per breaking change — e.g. for a renamed field: `old: response['user_email'] → new: response['email_address']`, with both sides shown | PASS | Each renamed field in Step 3 has explicit before/after Python code (e.g., `owner = response["user_id"]` → `owner = response["account_id"]`). Step 4 has before/after curl for both removed endpoints. Auth has before/after curl and Python. |
| c13 | Output's deprecation timeline has actual dates — e.g. "v2 sunset: 2027-01-31, v2 deprecation header sent from: 2026-07-01, v3 GA: 2026-04-15" — not "eventually" or "at some point" | PASS | Four absolute ISO dates: 2026-05-01, 2026-08-01, 2026-11-01, 2027-02-01. Footer also repeats 'Deprecation date: 2026-08-01' and 'v2 end-of-life: 2027-02-01'. |
| c14 | Output's impact assessment names who is affected — what kinds of integrations break (every integration using removed endpoints, every integration that hardcoded API keys), and what is NOT affected (e.g. read-only data shapes that didn't change) | PASS | 'Who is affected: All integrations calling the v2 API. No exceptions — the auth change alone requires updates to every request.' Who is NOT affected: 'If you are on a managed integration (Zapier, Make, HubSpot native connector), your connector vendor handles the migration.' |
| c15 | Output's rollback plan documents the point of no return — once v2 is decommissioned (per the timeline date), rollback to v2 becomes impossible; before that point, customers can revert their code if they kept v2 credentials | PASS | Explicit 'Point of no return' section and: 'Rollback is possible at any point before 2027-02-01. After that date, v2 is gone and rollback is not possible.' Also notes keeping v2 API key as prerequisite and warns 'Do not cancel your v2 API key until you are fully on v3.' |
| c16 | Output's coexistence guidance covers running both v2 and v3 in parallel during migration — whether existing v2 API keys still work alongside new OAuth tokens, or whether they must be migrated atomically | PASS | 'Running v2 and v3 simultaneously' section explicitly states: 'once you switch to OAuth 2.0 tokens, those tokens work on both v2 and v3. You do not need to keep the API key alive once you've switched auth.' Confirms both run independently during transition. |
| c17 | Output's verification steps let the developer confirm migration success — e.g. "after migration: GET /v3/users should return the new schema; v2 endpoint calls return 410 Gone after sunset date" | PASS | Automated script checks token acquisition, v3 `/accounts/current` response, 410 from old `/users/me`, and v2 still responding with old schema. Manual checklist verifies account_id, status, display_name, created_at fields. Also confirms '410 Gone' expectation via `STATUS=$(curl ... -w "%{http_code}")`. |
| c18 | Output's effort estimate is honest — names a typical effort range per integration size (small: 1-2 days, medium: 3-5 days, large: 1-2 weeks) — and acknowledges that mass field-rename + auth rebuild is non-trivial, not "should be quick" | PARTIAL | Estimate is '2–4 hours for a typical integration. Add a day if no existing OAuth client.' The criterion expects ranges by integration size (small/medium/large up to 1-2 weeks) and explicit acknowledgment of non-triviality. The 2-4 hour estimate lacks size tiers and may understate effort for large codebases with widespread field usage. |
| c19 | Output addresses the deprecation header / Sunset header (RFC 8594) being sent on v2 responses during the transition window so client tooling can detect imminent sunset | PARTIAL | In the deprecation timeline table, the 2026-08-01 row states: 'v2 responses include a `Deprecation: true` header and a `Sunset: Sat, 01 Nov 2026` header.' Headers are named but no guidance on how client tooling should detect or act on them, and RFC 8594 is not referenced. |

### Notes

The output is a high-quality migration guide that covers all major structural requirements: exhaustive breaking changes table, before/after code per change, concrete dates in the timeline, rollback plan with point-of-return, and solid verification steps. The two main weaknesses are: (1) c9 — no skill YAML frontmatter is visible in the captured artifacts, so it cannot be scored; (2) c11 — the auth section only covers client credentials without discussing Authorization Code flow, which the criterion explicitly required; (3) c18 — the 2-4 hour estimate is plausibly low and lacks the per-size breakdown (small/medium/large) the criterion called for. The Deprecation/Sunset header mention satisfies the PARTIAL ceiling for c19. Overall the guide is well-structured and actionable, scoring 86% against the rubric.
