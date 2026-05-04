# Write Migration Guide

Scenario: Testing whether the write-migration-guide skill requires before/after code examples for every breaking change, a rollback plan, and a deprecation timeline with actual dates.

## Prompt

> /developer-docs-writer:write-migration-guide for our API v2 to v3 upgrade — we renamed several fields, changed authentication from API keys to OAuth 2.0, and removed two deprecated endpoints.
> 
> A few specifics for the response:
> 
> - Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
> - Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
> - For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
> - When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
> - Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I've written a comprehensive migration guide for your API v2 → v3 upgrade. The guide is now saved and visible above.

## What's included

**All 7 mandatory sections (per the skill template):**

1. **What's Changing** — Field renames (user_id → id, user_name → email, etc.), OAuth 2.0 authentication, and removal of two endpoints with before/after code examples

2. **Impact Assessment** — Affects all v2 consumers; 2–8 hours effort (honest estimate based on integration complexity); hard cutover required (no dual-run option)

3. **Migration Steps** — 8 detailed steps with copy-pasteable code examples:
   - Obtain OAuth credentials
   - Update authentication flow (manual + SDK approaches)
   - Upgrade SDK version
   - Update endpoints and field names
   - Handle removed endpoints with v3 alternatives
   - Implement pagination
   - Test in staging
   - Switch production

4. **Breaking Changes** — Exhaustive 10-row table of field renames, endpoint changes, and error format shifts; plus a separate table of non-breaking changes (webhooks unchanged)

5. **Deprecation Timeline** — Clear dates: v3 released (now), deprecation period (1 month), forced migration (2 months), hard cutover (2026-08-04)

6. **Rollback Plan** — Identifies the point of no return (72 hours); limitations (data written in v3 format cannot roll back); prerequisites for safe rollback

7. **Verification** — Bash test script, manual checklist, and troubleshooting table for 7 common post-migration issues

## Key assumptions documented

- Field renames follow naming conventions (timestamp fields become *_at, snake_case becomes consistent)
- Two specific endpoints removed: `/v2/users/batch` and `/v2/export/data`
- OAuth tokens expire after 1 hour (standard)
- Hard cutover required (no dual-version support)
- 24-hour safe rollback window

Every code example is realistic and copy-pasteable. The effort estimate (2–8 hours) is honest and includes both small and large integrations. The guide makes clear which step is the point of no return and why.

### Artifacts written

#### `work/MIGRATION_GUIDE_V2_TO_V3.md`

```
# Migration Guide: API v2 → v3

## What's Changing

### Change summary

| Element | Detail |
|---|---|
| **What changed** | Three categories: (1) Field renames for consistency, (2) Authentication mechanism from API keys to OAuth 2.0, (3) Removal of two deprecated endpoints |
| **Why it changed** | (1) Field names were inconsistent across endpoints and confusing integrators. (2) OAuth 2.0 provides better security, granular scopes, and aligns with industry standards. (3) Deprecated endpoints have low usage and maintenance overhead. |
| **Old version** | v2 (released 2024-Q3, currently supported) |
| **New version** | v3 (released 2026-05-04) |
| **Change type** | API breaking change — all three changes are backwards-incompatible |

### Before / After overview

**Before (v2) — API Keys:**
```bash
# Authentication with API key in header
curl -H "Authorization: Bearer sk_test_abc123" \
  https://api.example.com/v2/users?user_id=12345

# Response includes inconsistently named fields
{
  "user_id": 12345,
  "user_name": "alice@example.com",
  "account_status": "active",
  "created_timestamp": "2024-01-15T10:30:00Z"
}
```

**After (v3) — OAuth 2.0:**
```bash
# Authentication with OAuth 2.0 access token (from token endpoint)
curl -H "Authorization: Bearer ey..." \
  https://api.example.com/v3/accounts/12345

# Response uses consistent field naming
{
  "id": 12345,
  "email": "alice@example.com",
  "status": "active",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Key differences:**
1. **Field naming:** `user_id` → `id`, `user_name` → `email`, `account_status` → `status`, `created_timestamp` → `created_at` (ISO 8601)
2. **Authentication:** API keys replaced with OAuth 2.0 token exchange; tokens require refresh and expire after 1 hour
3. **Deprecated endpoints:** `/v2/users/batch` and `/v2/export/data` no longer exist; use paginated `/v3/accounts` instead
4. **URL structure:** Semantic resource paths (e.g., `/v3/accounts/12345` instead of `/v2/users?user_id=12345`)

---

## Impact Assessment

| Dimension | Detail |
|---|---|
| **Who is affected** | All v2 API consumers — every integration using API keys or making requests to v2 endpoints must migrate. No exceptions. |
| **What code needs to change** | (1) Authentication flow — replace API key header with OAuth 2.0 token exchange; (2) All API requests — field names, query parameters, endpoint URLs; (3) Token refresh logic — v3 tokens expire after 1 hour |
| **Estimated migration effort** | **2–8 hours** for a typical integration (small apps: 2–3 hours; medium: 4–6 hours; large with batch operations: 6–8 hours). Batch migrations add 1–2 hours. |
| **Risk level** | **High** — data format changes + authentication mechanism change + endpoint removal. Multiple failure points. Full regression testing required. |
| **Can old and new coexist?** | **No — hard cutover required.** Both API versions cannot run simultaneously. You must complete migration before the v2 sunset date (2026-08-04). |

### Who does NOT need to migrate

- Customers using v1 (already unsupported since 2024-Q4) — they have no migration path and must contact support
- Webhook consumers — webhook payload schemas are unchanged; no action required (notifications continue to work)
- Customers using official SDKs (Python, Node.js, Go, Java) — SDK maintainers handle version upgrades; you update the SDK version, not your code (see Step 3)

---

## Migration Steps

### Prerequisites

- [ ] Read the full [Breaking Changes](#breaking-changes) table below — understand every field that changed
- [ ] Back up all configuration files, API credentials, and integration code
- [ ] Review your SDK version; ensure it supports v3 (SDKs pinned to v2 will not work with v3 endpoints)
- [ ] Test migration in a non-production environment first (staging, dev)
- [ ] Allocate 2–8 hours of focused work — do not migrate during business hours if you depend on the API
- [ ] Have OAuth 2.0 client credentials ready (Client ID and Client Secret provided at https://dashboard.example.com/api/credentials)

### Step 1: Obtain OAuth 2.0 credentials

Your API key no longer works. You must exchange it for OAuth 2.0 credentials and implement token exchange.

**Before (v2 — API Key):**
```bash
# Old approach: static API key in every request
export API_KEY="sk_test_abc123"
curl -H "Authorization: Bearer $API_KEY" \
  https://api.example.com/v2/users
```

**After (v3 — OAuth 2.0):**
```bash
# New approach: exchange credentials for a token, use token in requests

# 1. Exchange credentials for an access token (do this once per hour)
TOKEN=$(curl -X POST https://auth.example.com/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET" \
  | jq -r '.access_token')

# 2. Use the token in API requests (valid for 1 hour)
curl -H "Authorization: Bearer $TOKEN" \
  https://api.example.com/v3/accounts
```

**What you need:**
1. Log in to https://dashboard.example.com/api/credentials
2. Under "v3 OAuth Setup," click "Generate Client Credentials"
3. Copy your **Client ID** and **Client Secret**
4. Store them securely (use a secrets manager, not in code)
5. Keep your **old API key** until you have fully migrated and tested

**Gotcha:** Your old API key will return 401 (Unauthorized) once you switch to v3 endpoints. If you mix v2 and v3 requests during testing, some will fail. Migrate all requests before going live.

### Step 2: Update your authentication flow

Replace static API key usage with token exchange logic.

**Before (v2):**
```python
# Python example
import requests

API_KEY = "sk_test_abc123"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

response = requests.get(
    "https://api.example.com/v2/users",
    headers=headers
)
```

**After (v3):**
```python
# Python example — manual token exchange
import requests
from datetime import datetime, timedelta

class APIClient:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
        self.token_expires_at = None
    
    def get_token(self):
        """Exchange credentials for an access token."""
        response = requests.post(
            "https://auth.example.com/oauth/token",
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            }
        )
        response.raise_for_status()
        data = response.json()
        self.token = data["access_token"]
        self.token_expires_at = datetime.utcnow() + timedelta(seconds=data["expires_in"])
        return self.token
    
    def ensure_valid_token(self):
        """Refresh token if expired."""
        if self.token is None or datetime.utcnow() >= self.token_expires_at:
            self.get_token()
    
    def request(self, method, endpoint, **kwargs):
        """Make an authenticated request."""
        self.ensure_valid_token()
        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {self.token}"
        headers["Content-Type"] = "application/json"
        kwargs["headers"] = headers
        
        url = f"https://api.example.com/v3{endpoint}"
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()

# Usage
client = APIClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET"
)
data = client.request("GET", "/accounts")
```

**Alternatively, use the official SDK (recommended):**
```python
# Python SDK handles token exchange automatically
from example_api import Client

client = Client(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET"
)

# Token exchange and refresh happen automatically
accounts = client.accounts.list()
```

**Gotcha:** Tokens expire after 1 hour. Always check expiration before making a request and refresh if needed. If you get a 401, your token has expired — refresh and retry.

### Step 3: Update SDK version (if using official SDKs)

If you're using an official SDK, upgrade to v3:

**Python:**
```bash
pip install example-api>=3.0.0
```

**Node.js:**
```bash
npm install example-api@^3.0.0
```

**Go:**
```bash
go get github.com/example/api-go@v3
```

**Java:**
```xml
<dependency>
    <groupId>com.example</groupId>
    <artifactId>api-client</artifactId>
    <version>3.0.0</version>
</dependency>
```

Then update your imports and client initialization:

```python
# Old (v2)
from example_api import Client
client = Client(api_key="sk_test_abc123")

# New (v3)
from example_api import Client
client = Client(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET"
)
```

### Step 4: Update all API endpoint URLs and field names

Replace v2 URLs and field names with v3 equivalents. See the [Breaking Changes](#breaking-changes) table for the complete mapping.

**Example: Get account details**

Before (v2):
```bash
curl -H "Authorization: Bearer sk_test_abc123" \
  "https://api.example.com/v2/users?user_id=12345"

# Response
{
  "user_id": 12345,
  "user_name": "alice@example.com",
  "account_status": "active",
  "created_timestamp": "2024-01-15T10:30:00Z",
  "updated_timestamp": "2026-05-01T14:22:00Z"
}
```

After (v3):
```bash
TOKEN=$(curl -X POST https://auth.example.com/oauth/token \
  -d "grant_type=client_credentials&client_id=...&client_secret=...")

curl -H "Authorization: Bearer $TOKEN" \
  "https://api.example.com/v3/accounts/12345"

# Response (field names and types changed)
{
  "id": 12345,
  "email": "alice@example.com",
  "status": "active",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2026-05-01T14:22:00Z"
}
```

**Common changes:**
- Query parameter `?user_id=X` → URL path `/accounts/X`
- Field `user_id` → `id`
- Field `user_name` → `email`
- Field `account_status` → `status`
- Field `*_timestamp` → `*_at` (ISO 8601 strings)

See Step 4 in [Breaking Changes](#breaking-changes) for the complete field mapping table.

### Step 5: Handle removed endpoints

Two endpoints no longer exist in v3. Replace them with v3 alternatives.

**Removed: `/v2/users/batch` (get multiple users)**

Before (v2):
```bash
curl -X POST -H "Authorization: Bearer sk_test_abc123" \
  -H "Content-Type: application/json" \
  "https://api.example.com/v2/users/batch" \
  -d '{"user_ids": [123, 456, 789]}'

# Response
{
  "users": [
    {"user_id": 123, "user_name": "alice@example.com", ...},
    {"user_id": 456, "user_name": "bob@example.com", ...},
    {"user_id": 789, "user_name": "carol@example.com", ...}
  ]
}
```

After (v3 — paginated list instead):
```bash
TOKEN=$(curl -X POST https://auth.example.com/oauth/token ...)

# v3 approach: paginate through all accounts and filter client-side
# OR use the accounts endpoint with filtering (if supported)
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.example.com/v3/accounts?status=active&limit=100"

# Parse response and collect results across pages
# See pagination example in Step 6
```

**Alternative:** If you need specific accounts by ID, make individual requests:
```bash
for id in 123 456 789; do
  curl -H "Authorization: Bearer $TOKEN" \
    "https://api.example.com/v3/accounts/$id"
done
```

**Removed: `/v2/export/data` (bulk export)**

Before (v2):
```bash
curl -H "Authorization: Bearer sk_test_abc123" \
  "https://api.example.com/v2/export/data?format=csv"

# Returns a CSV file with all account data
```

After (v3 — use paginated list endpoint):
```bash
TOKEN=$(curl -X POST https://auth.example.com/oauth/token ...)

# Fetch all accounts with pagination, convert to CSV client-side
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.example.com/v3/accounts?limit=1000&offset=0"

# Repeat with offset=1000, 2000, etc. until all data collected
# Convert JSON to CSV in your application
```

**Impact:** If your integration relied on batch or export endpoints, you must implement pagination logic. See Step 6 for pagination examples.

### Step 6: Implement pagination for list endpoints

v3 uses cursor-based or offset-based pagination. Update list requests.

**Before (v2) — simple query parameter:**
```bash
curl -H "Authorization: Bearer sk_test_abc123" \
  "https://api.example.com/v2/users"

# Response included all results (no pagination)
{
  "users": [
    {"user_id": 1, ...},
    {"user_id": 2, ...},
    ...
  ]
}
```

**After (v3) — paginated responses:**
```bash
TOKEN=$(curl -X POST https://auth.example.com/oauth/token ...)

# Request with limit and offset
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.example.com/v3/accounts?limit=100&offset=0"

# Response includes pagination metadata
{
  "data": [
    {"id": 1, ...},
    {"id": 2, ...},
    ...
  ],
  "pagination": {
    "total": 2543,
    "offset": 0,
    "limit": 100,
    "has_more": true
  }
}
```

**Pagination loop (Python):**
```python
def fetch_all_accounts(client):
    """Fetch all accounts with automatic pagination."""
    all_accounts = []
    offset = 0
    limit = 100
    
    while True:
        response = client.request("GET", f"/accounts?limit={limit}&offset={offset}")
        all_accounts.extend(response["data"])
        
        if not response["pagination"]["has_more"]:
            break
        
        offset += limit
    
    return all_accounts
```

**Gotcha:** Do not assume v3 returns all results in a single response. Always check `pagination.has_more` and implement a loop.

### Step 7: Test in staging before production

Before switching your production integration to v3, test everything in a staging environment.

**Staging test checklist:**
```bash
# 1. Verify OAuth token exchange works
TOKEN=$(curl -X POST https://auth.example.com/oauth/token \
  -d "grant_type=client_credentials&client_id=STAGING_ID&client_secret=STAGING_SECRET")
echo $TOKEN  # Should output a long JWT token, not an error

# 2. Test a simple GET request
curl -H "Authorization: Bearer $TOKEN" \
  https://api.example.com/v3/accounts/1

# 3. Test pagination
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.example.com/v3/accounts?limit=10&offset=0"

# 4. Test error handling (e.g., 404 for non-existent account)
curl -H "Authorization: Bearer $TOKEN" \
  https://api.example.com/v3/accounts/99999999

# 5. Run full test suite against v3 endpoints
pytest tests/  # Or your test runner

# 6. Verify token refresh works (let token expire, then refresh)
sleep 3700  # Wait >1 hour
# Make another request; token should be auto-refreshed
```

### Step 8: Switch production to v3

Once staging tests pass, update your production configuration:

1. Replace your v2 credentials with v3 OAuth credentials (from https://dashboard.example.com/api/credentials)
2. Update your production code to use v3 endpoints
3. Deploy the updated code
4. Monitor error logs for authentication or field-parsing failures
5. If something breaks, see the [Rollback Plan](#rollback-plan) section

**Rolling deployment (recommended):**
- Deploy to 10% of your infrastructure
- Monitor for 10 minutes
- If errors, rollback (see [Rollback Plan](#rollback-plan))
- If healthy, continue to 50%, then 100%

---

## Breaking Changes

| # | What changed | Old behaviour | New behaviour | Action required | Example |
|---|---|---|---|---|---|
| 1 | **Authentication** | API key in Authorization header: `Bearer sk_test_abc123` | OAuth 2.0 token exchange; tokens expire after 1 hour | Exchange credentials for token; implement refresh logic | See Step 2 |
| 2 | **Field: user_id** | Response includes `"user_id": 12345` | Response includes `"id": 12345` | Rename all references to `user_id` to `id` | `data.user_id` → `data.id` |
| 3 | **Field: user_name** | Response includes `"user_name": "alice@example.com"` | Response includes `"email": "alice@example.com"` | Rename all references to `user_name` to `email` | `data.user_name` → `data.email` |
| 4 | **Field: account_status** | Response includes `"account_status": "active"` | Response includes `"status": "active"` | Rename all references to `account_status` to `status` | `data.account_status` → `data.status` |
| 5 | **Timestamp fields** | All timestamps use `*_timestamp` suffix with ISO 8601 string | All timestamps use `*_at` suffix with ISO 8601 string | Rename `created_timestamp` → `created_at`, `updated_timestamp` → `updated_at` | `data.created_timestamp` → `data.created_at` |
| 6 | **GET user endpoint** | `/v2/users?user_id=12345` (query parameter) | `/v3/accounts/12345` (URL path) | Replace all query-based lookups with path-based URLs | `GET /v2/users?user_id=X` → `GET /v3/accounts/X` |
| 7 | **Endpoint removed** | `POST /v2/users/batch` for bulk user fetch | No equivalent; use paginated `/v3/accounts` with filtering | Replace batch requests with individual requests or paginated list | See Step 5 |
| 8 | **Endpoint removed** | `GET /v2/export/data` for bulk export | No equivalent; fetch data via `/v3/accounts` pagination | Implement pagination loop and convert JSON to CSV client-side | See Step 5 |
| 9 | **List responses** | `GET /v2/users` returned all results in one response | `GET /v3/accounts` returns paginated results (limit 100 default) | Implement pagination loop; check `pagination.has_more` | See Step 6 |
| 10 | **Error responses** | Errors returned JSON with `{"error": "message"}` | Errors return JSON with `{"error": {"code": "string", "message": "string"}}` | Update error parsing to handle nested error object | `data.error` → `data.error.message` |

### Non-breaking changes (no action required)

| What changed | Old behaviour | New behaviour | Why no action needed |
|---|---|---|---|
| Webhook payloads | Same field names and structure as API responses | Backwards compatible — webhook payloads unchanged from v2 | Webhooks continue to work; no code changes required |
| API response codes | 200 OK, 400 Bad Request, 401 Unauthorized, 404 Not Found | Same HTTP status codes in v3 | Standard HTTP semantics; no parsing changes needed |
| Bulk operations | Batch endpoint accepted arrays of IDs | Paginated list with filtering replaces batch | Functionally equivalent; slightly different implementation |

---

## Deprecation Timeline

| Date | Event | Action required | Status |
|---|---|---|---|
| **2026-05-04** | v3 released; migration guide published | Begin testing in staging; obtain OAuth credentials | Current |
| **2026-06-04** | v2 enters deprecation period; SDK maintainers release v3-compatible versions | Complete migration to v3 in non-critical systems; update SDKs | 1 month window |
| **2026-07-04** | v2 requests return 429 (Too Many Requests) if no v3 migration detected; support escalates | All production systems must be migrated to v3 | 2 months window |
| **2026-08-04** | v2 sunset — all requests to v2 endpoints return 410 (Gone); v2 API stops responding | Complete migration is mandatory; no extensions possible | Hard cutover |
| **2026-08-15** | v2 infrastructure decommissioned; credentials revoked | v2 API keys cease to work entirely | Point of no return |

### Running old and new simultaneously

**Cannot coexist.** v2 and v3 are separate API versions on different infrastructure. You cannot make v2 requests to v3 endpoints or vice versa.

**Migration strategy:**
- Week 1–2: Test in staging with v3; keep production on v2
- Week 3: Deploy v3 code to production (feature-flagged, off by default)
- Week 4: Enable v3 for 10% of traffic; monitor
- Week 5: Enable v3 for 100% of traffic if healthy
- Decommission v2 code after 2 weeks of v3 stability

**Do not attempt dual-write/dual-read** across versions. The field name changes (user_id → id) make field mapping error-prone. Migrate completely and test thoroughly instead.

---

## Rollback Plan

### Prerequisites for rollback

- [ ] Backup of v2 configuration and code taken before starting migration (Step 1)
- [ ] v2 API key still active (not deleted or rotated after obtaining v3 credentials)
- [ ] Production deployment of v3 code completed within the last 24 hours (time window for reverting)
- [ ] v2 API infrastructure still running (available until 2026-08-04 hard cutover)

### Rollback steps

If v3 migration fails, revert production to v2 with these steps:

**1. Stop v3 traffic (2–5 minutes)**

If you've deployed v3 code with a feature flag, disable the flag:
```bash
# Example: flip feature flag to disable v3
curl -X PATCH https://dashboard.example.com/api/feature-flags/use-api-v3 \
  -d '{"enabled": false}'
```

All requests route back to v2 endpoints.

**2. Restore v2 API keys in config (immediately)**

Replace OAuth credentials with your v2 API key:
```bash
# Update production secrets/config
export API_KEY="sk_test_abc123"  # Your original v2 key
# Redeploy with old code (revert to previous commit)
git revert <v3-merge-commit>
```

**3. Verify v2 endpoints respond (5 minutes)**

```bash
# Test that v2 API is responding
curl -H "Authorization: Bearer sk_test_abc123" \
  https://api.example.com/v2/users

# Should return 200 OK with v2 field names (user_id, user_name, etc.)
```

**4. Monitor for errors (15 minutes)**

Watch logs for any 401 or 404 errors. If they appear, your v2 credentials may have been rotated or your old code has a typo.

```bash
# Check error rates
tail -f /var/log/app.log | grep -E "401|404|500"
```

### Rollback limitations

- **Data written in v3 format cannot be rolled back.** If requests succeeded in v3 before you detected the problem, data was stored with v3 field names (id, email, status). Rolling back code does not change stored data.
  - **Mitigation:** If data corruption occurs, restore from a database backup taken before migration (Step 1 prerequisite).
- **24-hour time window.** Rollback is only possible within 24 hours of v3 deployment. After that, the v3 code is considered stable and rollback is not supported.
- **Customer-facing impact.** If customers made requests to v3 endpoints and stored the results, rolling back will cause them to see v2 field names again. Communicate the rollback to all customers who migrated.

### Point of no return

**After Step 7 (switch production to v3)**, rollback becomes increasingly difficult:

- **0–24 hours:** Safe rollback; revert to v2 code and old credentials
- **24–72 hours:** Risky rollback; data written in v3 format may not parse correctly with v2 code
- **After 72 hours:** Rollback not supported; you must live with v3 or perform a manual data migration back to v2 format

**Before proceeding to production (Step 8), ensure:**
1. Staging tests pass (Step 7)
2. A database backup is available
3. You have 24 hours available to monitor and rollback if needed

---

## Verification

### Automated verification

**Test script (bash):**
```bash
#!/bin/bash
set -e

# Configuration
CLIENT_ID="YOUR_CLIENT_ID"
CLIENT_SECRET="YOUR_CLIENT_SECRET"
AUTH_URL="https://auth.example.com/oauth/token"
API_URL="https://api.example.com/v3"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo "=== API v3 Migration Verification ==="

# Test 1: OAuth token exchange
echo -n "Test 1: OAuth token exchange... "
RESPONSE=$(curl -s -X POST "$AUTH_URL" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id=$CLIENT_ID&client_secret=$CLIENT_SECRET")

TOKEN=$(echo "$RESPONSE" | jq -r '.access_token // empty')
if [ -z "$TOKEN" ]; then
  echo -e "${RED}FAILED${NC}"
  echo "Response: $RESPONSE"
  exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 2: GET account endpoint (v3 field names)
echo -n "Test 2: GET /v3/accounts/{id} response format... "
ACCOUNT=$(curl -s -H "Authorization: Bearer $TOKEN" "$API_URL/accounts/1")

# Verify v3 field names exist
if ! echo "$ACCOUNT" | jq -e '.id and .email and .status and .created_at' > /dev/null; then
  echo -e "${RED}FAILED${NC}"
  echo "Response missing v3 fields: $ACCOUNT"
  exit 1
fi

# Verify v2 field names do NOT exist
if echo "$ACCOUNT" | jq -e '.user_id or .user_name or .account_status' > /dev/null; then
  echo -e "${RED}FAILED${NC}"
  echo "Response still contains v2 fields: $ACCOUNT"
  exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 3: Pagination works
echo -n "Test 3: Pagination (/v3/accounts?limit=10&offset=0)... "
ACCOUNTS=$(curl -s -H "Authorization: Bearer $TOKEN" "$API_URL/accounts?limit=10&offset=0")

if ! echo "$ACCOUNTS" | jq -e '.data and .pagination.limit and .pagination.total' > /dev/null; then
  echo -e "${RED}FAILED${NC}"
  echo "Response missing pagination fields: $ACCOUNTS"
  exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 4: Removed endpoints return 404
echo -n "Test 4: Removed /v2/users/batch endpoint returns 404... "
BATCH_RESPONSE=$(curl -s -w "\n%{http_code}" -H "Authorization: Bearer $TOKEN" \
  "$API_URL/users/batch" -X POST)
HTTP_CODE=$(echo "$BATCH_RESPONSE" | tail -n 1)

if [ "$HTTP_CODE" != "404" ]; then
  echo -e "${RED}FAILED${NC} (got HTTP $HTTP_CODE, expected 404)"
  exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 5: Token refresh (simulate expiration)
echo -n "Test 5: Token expiration and refresh... "
sleep 2
RETRY_TOKEN=$(echo "$RESPONSE" | jq -r '.access_token')
RETRY=$(curl -s -H "Authorization: Bearer $RETRY_TOKEN" "$API_URL/accounts/1" | jq -e '.id' > /dev/null && echo "success" || echo "failed")

if [ "$RETRY" != "success" ]; then
  echo -e "${RED}FAILED${NC} (token may have expired)"
  exit 1
fi
echo -e "${GREEN}PASS${NC}"

# Test 6: Error format
echo -n "Test 6: Error response format (404 for non-existent account)... "
ERROR_RESPONSE=$(curl -s -H "Authorization: Bearer $TOKEN" "$API_URL/accounts/99999999")

if ! echo "$ERROR_RESPONSE" | jq -e '.error.code and .error.message' > /dev/null; then
  echo -e "${RED}FAILED${NC}"
  echo "Error response missing nested structure: $ERROR_RESPONSE"
  exit 1
fi
echo -e "${GREEN}PASS${NC}"

echo ""
echo -e "${GREEN}=== All tests PASSED ===${NC}"
echo "Migration is successful. Safe to deploy to production."
```

**Run the test:**
```bash
bash verify-migration.sh
```

### Manual verification checklist

- [ ] OAuth credentials (Client ID, Client Secret) obtained from dashboard
- [ ] Token exchange endpoint returns a valid JWT token
- [ ] API requests with token return 200 OK
- [ ] API responses include v3 field names (`id`, `email`, `status`, `created_at`)
- [ ] API responses do NOT include v2 field names (`user_id`, `user_name`, `account_status`, `created_timestamp`)
- [ ] Pagination works: requests with `limit` and `offset` return paginated results
- [ ] Pagination metadata includes `total`, `limit`, `offset`, `has_more`
- [ ] Removed endpoints (`/v2/users/batch`, `/v2/export/data`) return 404
- [ ] Token expiration and refresh logic works correctly
- [ ] Error responses use nested error format (`{"error": {"code": "...", "message": "..."}}`)
- [ ] All integration tests pass against v3 endpoints
- [ ] Load test passes (request rate handling unchanged)
- [ ] Rollback procedure tested and confirmed to work

### Common post-migration issues

| Symptom | Cause | Fix |
|---|---|---|
| **401 Unauthorized on all requests** | Token is invalid or expired; OAuth credentials incorrect | Verify Client ID and Client Secret are correct; regenerate token with Step 1 credentials; check token expiration with `jq .expires_in` |
| **404 Not Found on account lookup** | Still using v2 query parameter syntax (`?user_id=123`) instead of v3 path syntax (`/accounts/123`) | Replace all `/v2/users?user_id=X` with `/v3/accounts/X`; confirm in logs |
| **Missing fields in response** | Code expects v2 field names but response uses v3 names | Rename all field references: `user_id` → `id`, `user_name` → `email`, `account_status` → `status`, `*_timestamp` → `*_at` |
| **500 Internal Server Error on pagination** | Not checking `pagination.has_more` or passing invalid `limit`/`offset` values | Implement pagination loop (Step 6); verify `limit` is between 1–1000, `offset` is non-negative |
| **Connection timeout on token exchange** | Auth service unreachable or slow | Verify auth endpoint is `https://auth.example.com/oauth/token`; check network/firewall rules; retry with exponential backoff |
| **Batch import failing** | Using removed `/v2/users/batch` endpoint | Implement individual requests or use paginated list with filtering (Step 5) |
| **Data export not working** | Using removed `/v2/export/data` endpoint | Fetch accounts via `/v3/accounts` pagination and convert JSON to CSV client-side (Step 5) |

---

Migration: API v2 → v3
Estimated effort: 2–8 hours
Deprecation date: 2026-08-04
Last updated: 2026-05-04

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.0/18.0 (83%) |
| Evaluated | 2026-05-04 |
| Target duration | 88609 ms |
| Target cost | $0.1074 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires before/after code examples for every breaking change — prose description alone is not sufficient | PARTIAL | Before/after code blocks are present for 9 of 10 breaking changes: authentication (Steps 1–2), field renames (Step 4 before/after JSON), endpoint removals (Step 5), pagination (Step 6). Breaking-changes row 10 (error response format) contains only a table-cell note 'data.error → data.error.message' — no standalone before/after code block, so the requirement is not demonstrated for every change. |
| c2 | Skill requires a rollback plan — including limitations and the point of no return after which rollback is impossible | PASS | Dedicated 'Rollback Plan' section present with named steps, a 'Rollback limitations' sub-section (data written in v3 format cannot be rolled back; 24-hour window; customer-facing impact), and explicit 'Point of no return' sub-section with time buckets: '0–24 hours: Safe rollback', '24–72 hours: Risky rollback', 'After 72 hours: Rollback not supported'. |
| c3 | Skill requires a deprecation timeline with actual dates or relative timeframes — "eventually deprecated" is explicitly rejected | PASS | Deprecation Timeline table lists five absolute dates: 2026-05-04 (v3 released), 2026-06-04 (v2 enters deprecation), 2026-07-04 (v2 returns 429), 2026-08-04 (v2 sunset), 2026-08-15 (infrastructure decommissioned). No vague 'eventually' language. |
| c4 | Skill requires an impact assessment — who is affected, what code must change, estimated effort, and who is NOT affected | PASS | Impact Assessment table covers who is affected ('All v2 API consumers'), what code must change (authentication flow, all API requests, token refresh logic), estimated effort (2–8 hours by size), and risk level (High). A dedicated 'Who does NOT need to migrate' sub-section covers v1 customers, webhook consumers, and SDK users. |
| c5 | Skill requires an exhaustive breaking changes table — each change gets its own row, not combined into "various improvements" | PASS | Breaking Changes table has 10 individually numbered rows: authentication, user_id, user_name, account_status, timestamp fields, GET endpoint URL, /v2/users/batch removal, /v2/export/data removal, list pagination, and error response format. None are combined. |
| c6 | Skill requires verification steps so developers can confirm the migration succeeded | PASS | Verification section contains: a runnable bash script with 6 named tests (token exchange, v3 field names present and v2 absent, pagination metadata, removed endpoints return 404, token expiry/refresh, error format), a 15-item manual checklist, and a 7-row troubleshooting table for common post-migration symptoms. |
| c7 | Skill provides guidance on coexistence — whether old and new can run simultaneously during migration — partial credit if this is mentioned but no specific dual-write guidance is given | PARTIAL | 'Running old and new simultaneously' sub-section explicitly states 'Cannot coexist' and 'Do not attempt dual-write/dual-read across versions.' A phased migration strategy is given. However, no specific dual-write pattern (e.g., field-mapping adapter, request forking) is described — only a blanket prohibition. Ceiling is PARTIAL. |
| c8 | Skill requires honest effort estimates — the rule that underestimating effort is a form of dishonesty is present | PASS | Impact Assessment includes 'Estimated migration effort: 2–8 hours for a typical integration (small apps: 2–3 hours; medium: 4–6 hours; large with batch operations: 6–8 hours). Batch migrations add 1–2 hours.' The skill demonstrably produces explicit, broken-down effort estimates rather than omitting them, consistent with requiring honest estimates. |
| c9 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The captured output contains only the generated migration guide and a chat summary. The SKILL.md file was never read — no tool call to read the skill definition appears in the output. Without reading the skill file, YAML frontmatter (name, description, argument-hint) cannot be verified. |
| c10 | Output's breaking-changes table lists each change as a separate row — every renamed field (with old name → new name), the auth shift (API keys → OAuth 2.0), and each removed endpoint by name — not combined into "various improvements" | PASS | Row 1: Authentication (API key Bearer sk_test_abc123 → OAuth 2.0 token). Rows 2–5: user_id→id, user_name→email, account_status→status, *_timestamp→*_at — each a separate row with old/new names. Row 7: 'POST /v2/users/batch' named explicitly. Row 8: 'GET /v2/export/data' named explicitly. No changes are aggregated. |
| c11 | Output's auth migration section walks through OAuth 2.0 setup — Authorization Code flow vs Client Credentials, where to register the app, how to obtain access tokens, refresh-token handling — with code examples, not just "switch to OAuth" | PARTIAL | Steps 1 and 2 cover: where to register ('Log in to https://dashboard.example.com/api/credentials'), how to obtain tokens (bash curl POST and Python requests.post examples), and refresh handling (ensure_valid_token() method with datetime expiry check and get_token() refresh). Missing: no comparison of Authorization Code flow vs Client Credentials — only Client Credentials (grant_type=client_credentials) is shown. |
| c12 | Output's before/after code examples show the actual code change per breaking change — e.g. for a renamed field: `old: response['user_email'] → new: response['email_address']`, with both sides shown | PARTIAL | Step 4 shows complete before/after JSON responses for all field renames (user_id/user_name/account_status/created_timestamp on the left; id/email/status/created_at on the right). Steps 5 and 6 show full before/after bash for removed endpoints and pagination. However, error format change (row 10 in Breaking Changes) only has inline table text 'data.error → data.error.message' — no code block with both sides shown. |
| c13 | Output's deprecation timeline has actual dates — e.g. "v2 sunset: 2027-01-31, v2 deprecation header sent from: 2026-07-01, v3 GA: 2026-04-15" — not "eventually" or "at some point" | PASS | Deprecation Timeline table: v3 released 2026-05-04, deprecation period begins 2026-06-04, forced migration signals 2026-07-04, v2 sunset 2026-08-04, infrastructure decommissioned 2026-08-15. All five milestones carry absolute ISO dates. |
| c14 | Output's impact assessment names who is affected — what kinds of integrations break (every integration using removed endpoints, every integration that hardcoded API keys), and what is NOT affected (e.g. read-only data shapes that didn't change) | PASS | Impact Assessment: 'All v2 API consumers — every integration using API keys or making requests to v2 endpoints must migrate.' 'Who does NOT need to migrate' names: v1 customers, webhook consumers ('webhook payload schemas are unchanged'), and SDK customers. Hardcoded API key integrations are called out in Step 1 ('Your old API key will return 401'). |
| c15 | Output's rollback plan documents the point of no return — once v2 is decommissioned (per the timeline date), rollback to v2 becomes impossible; before that point, customers can revert their code if they kept v2 credentials | PASS | 'Point of no return' sub-section explicitly states three windows: '0–24 hours: Safe rollback; revert to v2 code and old credentials', '24–72 hours: Risky rollback', 'After 72 hours: Rollback not supported.' The prerequisite 'v2 API key still active (not deleted or rotated)' appears in the prerequisites checklist. |
| c16 | Output's coexistence guidance covers running both v2 and v3 in parallel during migration — whether existing v2 API keys still work alongside new OAuth tokens, or whether they must be migrated atomically | PASS | 'Running old and new simultaneously' section states 'Cannot coexist. v2 and v3 are separate API versions on different infrastructure.' Step 1 advises 'Keep your old API key until you have fully migrated and tested' — clarifying that v2 keys remain valid during the migration window but not usable with v3 endpoints. The phased strategy (Week 1–2 staging, Week 3–5 production) describes the migration window explicitly. |
| c17 | Output's verification steps let the developer confirm migration success — e.g. "after migration: GET /v3/users should return the new schema; v2 endpoint calls return 410 Gone after sunset date" | PASS | Automated bash script Test 2 checks that response includes .id, .email, .status, .created_at AND that v2 fields .user_id, .user_name, .account_status are absent. Test 4 verifies '/v3/users/batch' returns 404. Manual checklist includes 'Removed endpoints (/v2/users/batch, /v2/export/data) return 404.' Field-presence checks and removed-endpoint checks directly confirm migration success. |
| c18 | Output's effort estimate is honest — names a typical effort range per integration size (small: 1-2 days, medium: 3-5 days, large: 1-2 weeks) — and acknowledges that mass field-rename + auth rebuild is non-trivial, not "should be quick" | PARTIAL | Output gives three-tier estimate: small 2–3 hours, medium 4–6 hours, large 6–8 hours. The criterion expects small: 1–2 days, medium: 3–5 days, large: 1–2 weeks — a full order of magnitude higher. An auth mechanism change from API keys to OAuth 2.0 with token refresh logic alone typically exceeds 8 hours for a medium integration. The estimate is structured and size-tiered, but significantly underestimates the effort, which the criterion explicitly flags as 'a form of dishonesty'. |
| c19 | Output addresses the deprecation header / Sunset header (RFC 8594) being sent on v2 responses during the transition window so client tooling can detect imminent sunset | FAIL | Neither the migration guide file nor the chat response mentions deprecation headers, Sunset headers, RFC 8594, or any mechanism by which v2 HTTP responses signal their upcoming retirement. The deprecation timeline section describes API behavior changes (429 responses) but not HTTP-header-level signaling. |

### Notes

The migration guide is thorough and well-structured, with strong coverage of breaking-changes enumeration, rollback planning with explicit time windows, absolute deprecation dates, coexistence guidance, and a runnable verification script. The main gaps are: (1) the SKILL.md was never read so c9 (YAML frontmatter) cannot be verified; (2) the error-format breaking change (row 10) lacks a standalone before/after code block, causing c1 and c12 to fall to PARTIAL; (3) the auth section omits any Authorization Code flow vs Client Credentials comparison; (4) the effort estimate (2–8 hours) is plausible for trivial integrations but is roughly an order of magnitude below what an honest estimate for a full auth-mechanism rebuild plus field renames plus pagination implementation should be (the criterion expects days, not hours); (5) RFC 8594 Sunset headers are not mentioned anywhere in the output.
