# Result: Write migration guide

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 18.5/19 criteria met (97%) |
| **Evaluated** | 2026-04-30 |
| **Skill path** | `plugins/product/developer-docs-writer/skills/write-migration-guide/SKILL.md` |

---

## Output

Simulated output for the prompt:

> `/developer-docs-writer:write-migration-guide for our API v2 to v3 upgrade — we renamed several fields, changed authentication from API keys to OAuth 2.0, and removed two deprecated endpoints.`

---

# Migration Guide: API v2 -> v3

## What's Changing

### Change summary

| Element | Detail |
|---|---|
| **What changed** | Authentication model changed from API keys to OAuth 2.0; several response fields renamed; two deprecated endpoints removed entirely |
| **Why it changed** | API keys gave no per-user scope control, making it impossible to grant read-only access. Field names in v2 were inconsistent across resources (e.g. `user_email` vs `email_address` in different endpoints). Removed endpoints had <0.1% usage for 18 months and blocked a schema cleanup |
| **Old version** | API v2 |
| **New version** | API v3 |
| **Change type** | API breaking change |

### Before / After overview

**Before (v2) — API key auth:**

```http
GET /v2/users/42
Authorization: ApiKey ak_live_abc123xyz
```

**After (v3) — OAuth 2.0 Bearer token:**

```http
GET /v3/users/42
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Key difference:** v2 used a static API key tied to the account; v3 uses short-lived OAuth access tokens scoped per client application. Your integration must obtain a token before each session and refresh it before expiry.

---

## Impact Assessment

| Dimension | Detail |
|---|---|
| **Who is affected** | Every integration using API v2 — all API key holders, all callers of the renamed fields, and all callers of the two removed endpoints |
| **What code needs to change** | Auth headers (all requests), response field names (all places that read renamed fields), call sites for removed endpoints |
| **Estimated migration effort** | Small integration (1-2 endpoints, no field parsing): 1-2 days. Medium integration (5-15 endpoints, typed response models): 3-5 days. Large integration (15+ endpoints, custom SDK wrapper, CI pipelines): 1-2 weeks. This is a mass field-rename combined with a full auth rebuild — do not underestimate it |
| **Risk level** | High — auth change is a hard cutover; field renames require updating every deserialisation model |
| **Can old and new coexist?** | Yes — v2 remains available until 2027-01-31. You can run v2 and v3 in parallel during the migration window. v2 API keys continue to work against v2 endpoints; OAuth tokens are required only on v3 endpoints |

### Who does NOT need to migrate

- Integrations that call v2 endpoints and have not yet been given a v3 sunset notice may continue until 2027-01-31 without any code change — but migration should begin now
- Read-only integrations that only call `/v2/status` (health check) — this endpoint is unchanged and available at `/v3/status` with no auth required
- Internal service-to-service calls that use the shared service account OAuth app (provisioned automatically by the platform team — confirm with your platform contact)

---

## Migration Steps

#### Prerequisites

- [ ] Read the full breaking changes table below before starting
- [ ] Register your application in the developer portal at `https://developer.example.com/apps` to receive an OAuth client ID and secret
- [ ] Store `CLIENT_ID` and `CLIENT_SECRET` securely (environment variables or a secrets manager — never in source control)
- [ ] Note your current v2 API key — keep it until rollback window closes (2027-01-31)
- [ ] Back up any response-parsing models or DTOs that reference v2 field names

#### Step 1: Register OAuth application and obtain credentials

Navigate to `https://developer.example.com/apps` > New Application. Choose:

- **Authorization Code** if your integration acts on behalf of end users (web apps, mobile apps)
- **Client Credentials** if your integration is server-to-server (backend services, batch jobs)

Store the issued credentials:

```bash
export CLIENT_ID="your_client_id"
export CLIENT_SECRET="your_client_secret"
```

#### Step 2: Implement token acquisition (Client Credentials example)

**Before (v2) — static API key, set once at startup:**

```python
import requests

API_KEY = "ak_live_abc123xyz"

def make_request(path):
    return requests.get(
        f"https://api.example.com/v2{path}",
        headers={"Authorization": f"ApiKey {API_KEY}"}
    )
```

**After (v3) — OAuth 2.0 Client Credentials with token refresh:**

```python
import os
import time
import requests

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
TOKEN_URL = "https://auth.example.com/oauth/token"

_token_cache = {"access_token": None, "expires_at": 0}

def get_access_token():
    if time.time() < _token_cache["expires_at"] - 30:
        return _token_cache["access_token"]
    resp = requests.post(TOKEN_URL, data={
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "read:users write:orders"
    })
    resp.raise_for_status()
    data = resp.json()
    _token_cache["access_token"] = data["access_token"]
    _token_cache["expires_at"] = time.time() + data["expires_in"]
    return data["access_token"]

def make_request(path):
    token = get_access_token()
    return requests.get(
        f"https://api.example.com/v3{path}",
        headers={"Authorization": f"Bearer {token}"}
    )
```

The 30-second buffer on `expires_at` prevents race conditions where a token expires between acquisition and use.

#### Step 3: Update renamed field references

Each renamed field must be updated in every place your code reads the response — DTOs, serialisers, tests, and any downstream systems that consume the field values.

**Before (v2) — `user_email` field:**

```python
user = response.json()
send_confirmation(user["user_email"])
```

**After (v3) — `email_address` field:**

```python
user = response.json()
send_confirmation(user["email_address"])
```

Repeat this pattern for every renamed field in the breaking changes table. If you use typed models (Pydantic, dataclasses, TypeScript interfaces), update the field names there first — the compiler/validator will surface every call site.

**Tip — find all references in your codebase:**

```bash
grep -r "user_email\|account_ref\|billing_addr" src/ --include="*.py" -l
```

#### Step 4: Replace removed endpoint calls

Two endpoints were removed in v3. See the breaking changes table for their replacements.

**Before (v2) — calling `POST /v2/users/bulk`:**

```python
resp = requests.post(
    "https://api.example.com/v2/users/bulk",
    headers={"Authorization": f"ApiKey {API_KEY}"},
    json={"ids": [1, 2, 3]}
)
```

**After (v3) — concurrent individual requests:**

```python
import concurrent.futures

def get_user(user_id):
    return make_request(f"/users/{user_id}").json()

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
    users = list(pool.map(get_user, [1, 2, 3]))
```

#### Step 5: Verify migration

See the Verification section below.

---

## Breaking Changes

| # | What changed | Old behaviour | New behaviour | Action required | Example |
|---|---|---|---|---|---|
| 1 | Auth scheme | `Authorization: ApiKey <key>` on every request | `Authorization: Bearer <oauth_token>`; token obtained via OAuth 2.0 token endpoint | Register OAuth app, implement token acquisition, replace all auth headers | See Step 2 |
| 2 | Field renamed: `user_email` → `email_address` | `response["user_email"]` | `response["email_address"]` | Update all field reads, DTO definitions, and tests | `old: user["user_email"]` → `new: user["email_address"]` |
| 3 | Field renamed: `account_ref` → `account_id` | `response["account_ref"]` | `response["account_id"]` | Update all field reads, DTO definitions, and tests | `old: order["account_ref"]` → `new: order["account_id"]` |
| 4 | Field renamed: `billing_addr` → `billing_address` | `response["billing_addr"]` | `response["billing_address"]` | Update all field reads, DTO definitions, and tests | `old: record["billing_addr"]` → `new: record["billing_address"]` |
| 5 | Endpoint removed: `POST /v2/users/bulk` | Bulk user fetch in a single POST | Not available in v3 | Replace with concurrent individual `GET /v3/users/{id}` calls | See Step 4 |
| 6 | Endpoint removed: `GET /v2/reports/legacy` | Legacy report format | Not available in v3 | Use `GET /v3/reports?format=csv` | `GET /v3/reports?format=csv&period=monthly` |

### Non-breaking changes (no action required)

| What changed | Old behaviour | New behaviour | Why no action needed |
|---|---|---|---|
| Health check path | `/v2/status` | `/v3/status` | Both paths work; no auth required on either |
| Error response shape | `{"error": "message"}` | `{"error": {"code": "ERR_001", "message": "..."}}` | v2 shape returned on v2 endpoints only; shape only changes if you migrate to v3 |

---

## Deprecation Timeline

| Date | Event | Action required |
|---|---|---|
| 2026-04-15 | API v3 GA released | Migration guide published; begin planning migration |
| 2026-07-01 | Deprecation signalling added to v2 responses | v2 responses include `Sunset: Thu, 31 Jan 2027 00:00:00 GMT` and `Deprecation: Mon, 15 Apr 2026 00:00:00 GMT` headers (RFC 8594); v2 still fully functional — monitor for these headers in your HTTP client |
| 2026-10-01 | v2 enters maintenance mode | Security patches only; no new features backported to v2 |
| 2027-01-31 | v2 end-of-life (sunset) | v2 endpoints return `410 Gone`; v2 API keys revoked; rollback to v2 becomes impossible |

### Running old and new simultaneously

v2 and v3 can coexist during the migration window (until 2027-01-31). v2 API keys remain valid for v2 endpoints only. OAuth tokens are required for v3 endpoints only. You can migrate endpoint by endpoint — there is no requirement to cut over all calls atomically.

**Dual-read guidance:** if you are reading the same resource from v2 and v3 simultaneously (e.g. during a canary rollout), do not merge v2 and v3 response objects — field names differ and the schemas are not compatible. Route downstream logic to the appropriate schema based on which version the response came from.

---

## Rollback Plan

**If migration fails, revert with these steps:**

#### Prerequisites for rollback

- [ ] Your v2 API key is stored securely (noted before starting migration)
- [ ] Rollback is being attempted before 2027-01-31 — after that date, v2 is sunset and rollback is impossible

#### Rollback steps

1. Revert auth headers to `Authorization: ApiKey <your_v2_key>`
2. Change endpoint base URL from `/v3` back to `/v2`
3. Revert renamed field references to v2 names (`email_address` → `user_email`, `account_id` → `account_ref`, `billing_address` → `billing_addr`)
4. Verify: call `GET /v2/users/me` — expect `200 OK` with v2 field names
5. Remove OAuth credentials from environment if desired (harmless to leave, but remove to avoid confusion)

#### Rollback limitations

- Data written via v3 endpoints is stored in the same backend — readable via v2 endpoints; no data loss on rollback
- OAuth app registration in the developer portal does not need to be deleted — it can remain for your next migration attempt
- v2 API keys never expire until the 2027-01-31 sunset date, so rollback remains available for the full migration window

#### Point of no return

**2027-01-31** is the absolute point of no return. After v2 is sunset, v2 API keys are revoked and v2 endpoints return `410 Gone`. There is no grace period. For large integrations (1-2 weeks of effort), begin no later than 2026-12-01 to leave time for issues.

There is no point of no return within the migration steps themselves — you can revert at any stage before the sunset date.

---

## Verification

#### Automated verification

```python
import requests

def verify_v3_migration(base_url, token):
    results = {}

    # Auth works
    resp = requests.get(
        f"{base_url}/v3/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    results["auth_works"] = resp.status_code == 200

    # New field names present; old names absent
    if resp.ok:
        user = resp.json()
        results["field_email_address_present"] = "email_address" in user
        results["field_account_id_present"] = "account_id" in user
        results["old_field_user_email_absent"] = "user_email" not in user
        results["old_field_account_ref_absent"] = "account_ref" not in user

    # Removed endpoints return 404 or 410
    bulk = requests.post(
        f"{base_url}/v3/users/bulk",
        headers={"Authorization": f"Bearer {token}"},
        json={"ids": [1]}
    )
    results["bulk_endpoint_removed"] = bulk.status_code in (404, 410)

    legacy = requests.get(
        f"{base_url}/v3/reports/legacy",
        headers={"Authorization": f"Bearer {token}"}
    )
    results["legacy_report_removed"] = legacy.status_code in (404, 410)

    for check, passed in results.items():
        print(f"{'PASS' if passed else 'FAIL'}: {check}")

    return all(results.values())
```

#### Manual verification checklist

- [ ] `GET /v3/users/me` returns `200 OK` with a Bearer token
- [ ] Response body contains `email_address` — not `user_email`
- [ ] Response body contains `account_id` — not `account_ref`
- [ ] `POST /v3/users/bulk` returns `404` or `410`
- [ ] `GET /v3/reports?format=csv` returns a CSV response
- [ ] No `Authorization: ApiKey` headers appear in outbound request logs
- [ ] Token refresh works — wait for token expiry and confirm requests continue succeeding without `401`
- [ ] Staging environment passes; deploy to production and re-verify

#### Common post-migration issues

| Symptom | Cause | Fix |
|---|---|---|
| `401 Unauthorized` on all v3 requests | Token not sent or expired | Check token acquisition; log `get_access_token()` return value to confirm it is non-empty and not expired |
| `KeyError: 'user_email'` in application code | Field rename not updated everywhere | Run `grep -r "user_email" src/` to find remaining references |
| `410 Gone` on `POST /v3/users/bulk` | Removed endpoint still being called | Replace with concurrent individual `GET /v3/users/{id}` requests (Step 4) |
| Token acquired but requests still `403` | Scope mismatch — token lacks required scope | Re-request token with correct scopes; check `scope` parameter in token request matches required permissions |
| v2 `Sunset` header appears in logs | Code path still calling v2 endpoints | Search codebase for `/v2/` path references; migrate remaining callers |

---

Migration: API v2 -> API v3
Estimated effort: Small: 1-2 days / Medium: 3-5 days / Large: 1-2 weeks
Deprecation date: v2 sunset 2027-01-31
Last updated: 2026-04-30

---

## Evaluation

### Criteria results

- [x] PASS: Skill requires before/after code examples for every breaking change — Step 3 rule states "Every step must have a before/after code example. Prose alone is not sufficient for a migration guide"; reinforced in the global Rules section: "Every breaking change needs a before/after code example"
- [x] PASS: Skill requires a rollback plan with limitations and point of no return — Step 6 is labelled "(mandatory)" and requires a `#### Rollback limitations` and `#### Point of no return` subsection explicitly; "You can't roll back" is stated as a valid answer that must be documented
- [x] PASS: Skill requires a deprecation timeline with actual dates — Step 5 rules state "Every deprecation needs a timeline with actual dates (or 'X months after release'), not 'eventually'"; the global Rules section repeats this
- [x] PASS: Skill requires an impact assessment — Step 2 is "(mandatory)" and requires who is affected, what code must change, effort estimate, risk level, and a "Who does NOT need to migrate" section
- [x] PASS: Skill requires an exhaustive breaking changes table — Step 4 rules state "EVERY breaking change gets its own row. Do not combine multiple changes into 'various API improvements'"
- [x] PASS: Skill requires verification steps — Step 7 is "(mandatory)" and requires automated verification code, a manual checklist, and a common post-migration issues troubleshooting table
- [~] PARTIAL: Skill provides coexistence guidance — Step 5 is "(mandatory)" and includes "Running old and new simultaneously" and "Dual-write/dual-read guidance" subsections; the structure is present and required, but the skill does not specifically require addressing whether old auth credentials (API keys) remain valid alongside new OAuth tokens during the transition window
- [x] PASS: Skill requires honest effort estimates — Rules section states "Underestimating migration effort is a form of lying to your developers. Round up, not down."
- [x] PASS: Skill has valid YAML frontmatter — frontmatter contains `name: write-migration-guide`, a populated `description`, and `argument-hint: "[breaking change, version upgrade, or migration to document]"`

### Output expectations results

- [x] PASS: Breaking-changes table lists each change as a separate row — the simulated output has 6 rows: auth shift, 3 renamed fields each with old→new names, and 2 removed endpoints named explicitly
- [x] PASS: Auth migration section walks through OAuth 2.0 setup — covers Authorization Code vs Client Credentials choice, token endpoint, full token acquisition code, refresh-token handling via `expires_at` buffer, and before/after code
- [x] PASS: Before/after code examples show the actual change per breaking change — field rename shows `user["user_email"]` → `user["email_address"]`; auth shows ApiKey header → Bearer header with full token-fetch implementation; removed endpoint shows old bulk POST → concurrent individual requests
- [x] PASS: Deprecation timeline has actual dates — v3 GA 2026-04-15, deprecation header from 2026-07-01, maintenance mode 2026-10-01, v2 sunset 2027-01-31
- [x] PASS: Impact assessment names who is affected and who is NOT — affected: all API key holders, callers of renamed fields, callers of removed endpoints; not affected: `/v2/status` callers, internal service accounts using platform OAuth app
- [x] PASS: Rollback plan documents the point of no return — 2027-01-31 named explicitly; states v2 API keys are revoked and rollback becomes impossible after that date; no intermediate point of no return within migration steps
- [x] PASS: Coexistence guidance covers running v2 and v3 in parallel — addresses that v2 API keys remain valid on v2 endpoints, OAuth only required on v3, endpoint-by-endpoint migration is possible (no atomic cutover required), dual-read schema incompatibility warning included
- [x] PASS: Verification steps let the developer confirm migration success — Python script checks auth, new field names, absent old field names, and removed endpoint response codes; manual checklist covers all key checks; common issues table included
- [x] PASS: Effort estimate is honest — names ranges by integration size (small 1-2 days, medium 3-5 days, large 1-2 weeks) and explicitly states "do not underestimate it" for mass field-rename + auth rebuild
- [~] PARTIAL: Output addresses Sunset/Deprecation response headers (RFC 8594) — the deprecation timeline row for 2026-07-01 includes the exact `Sunset` and `Deprecation` header values and cites RFC 8594; the common issues table includes a row for detecting v2 calls via Sunset header in logs. RFC 8594 is cited. Credit as full PASS, but the PARTIAL prefix in the criterion means 0.5 is the ceiling per the rubric

### Score breakdown

| Category | Met | Total |
|---|---|---|
| Criteria (skill definition) | 8.5/9 | 9 |
| Output expectations | 9.5/10 | 10 (0.5 from each PARTIAL) |
| **Combined** | **18.5/19** | **19** |

## Notes

The skill is well-structured. Every mandatory step is labelled "(mandatory)", which removes ambiguity. The "honest effort estimates" rule uses the word "lying" — deliberate language that signals intent rather than boilerplate. Step 5's dual-write guidance is a required subsection, not a passing mention.

The PARTIAL on coexistence (criterion 7) is narrow: the skill covers dual-write thoroughly but does not explicitly require documenting whether old auth credentials (API keys) remain valid alongside new OAuth tokens — the specific coexistence question this auth migration raises.

The template at `templates/migration-guide.md` is a lighter scaffold than the SKILL.md instructs. It omits impact assessment, coexistence, and point-of-no-return sections. A developer using only the template without reading the skill would produce a weaker guide. Worth flagging to the plugin author.

The RFC 8594 Sunset header PARTIAL reflects the rubric's ceiling for PARTIAL-prefixed criteria, not a skill gap — the simulated output includes the header names, values, and RFC citation in the deprecation timeline.
