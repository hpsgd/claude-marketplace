# Review With Issues

Scenario: A developer asks the code reviewer agent to review a Python Django view that handles user password reset. The code contains a SQL injection risk, an N+1 query, and missing rate limiting on the endpoint.

## Prompt

> Can you review this code? It's the password reset handler in our Django app.
> 
> ```python
> # views.py
> from django.http import JsonResponse
> from django.contrib.auth.models import User
> from django.db import connection
> import secrets
> 
> def request_password_reset(request):
>     if request.method != 'POST':
>         return JsonResponse({'error': 'Method not allowed'}, status=405)
> 
>     email = request.POST.get('email', '')
> 
>     # Find user by email
>     with connection.cursor() as cursor:
>         cursor.execute(f"SELECT id, username FROM auth_user WHERE email = '{email}'")
>         row = cursor.fetchone()
> 
>     if not row:
>         return JsonResponse({'error': 'Email not found'}, status=404)
> 
>     user_id, username = row
>     token = secrets.token_urlsafe(32)
> 
>     # Save token and send to all user's linked accounts
>     user = User.objects.get(id=user_id)
>     for profile in user.linkedprofile_set.all():
>         profile.reset_token = token
>         profile.save()
>         # Send email for each linked account
>         send_reset_email(profile.email, token)
> 
>     return JsonResponse({'message': 'Reset email sent'})
> ```
> 
> A few specifics for the response (the file is `views.py`; cite `views.py:line` on every finding):
> 
> - **Findings list (8 minimum)** — each with `**Severity**: BLOCKER/CRITICAL/HIGH/MEDIUM/LOW | **Confidence**: HIGH/MEDIUM/LOW | **File:Line**: views.py:N | **Evidence**: \`code snippet\` | **Fix**: [concrete code]`:
>   1. **BLOCKER, HIGH confidence** — SQL injection at `views.py:14` via f-string interpolation `f"SELECT id, email FROM auth_user WHERE email = '{email}'"`. Fix: parameterised query `cursor.execute("SELECT id, email FROM auth_user WHERE email = %s", [email])` OR Django ORM `User.objects.get(email=email)`.
>   2. **CRITICAL** — N+1 query in the `for profile in user.linkedprofile_set.all()` loop at `views.py:~34`. Each iteration triggers a save. Fix: `select_related('user')` on the queryset and bulk update with `LinkedProfile.objects.filter(user=user).update(reset_token=token)`.
>   3. **CRITICAL** — Missing rate limiting on the password-reset endpoint. Fix: add `django-ratelimit` decorator `@ratelimit(key='ip', rate='5/h', block=True)` or equivalent middleware. WHY: unbounded password-reset attempts allow account-enumeration probing and email flooding.
>   4. **HIGH** — User enumeration via 404 on unknown email at `views.py:~22`. Returning a different status for unknown vs known emails leaks account existence. Fix: return 200 with a generic message ("If an account exists for this email, a reset link has been sent") regardless.
>   5. **HIGH** — Reset token stored in plaintext on `profile.reset_token`. Fix: store `hashlib.sha256(token.encode()).hexdigest()` at rest; compare hashed value on redemption. Plaintext tokens in the DB = full account takeover if DB leaks.
>   6. **HIGH** — No token expiry / TTL on the reset token. Fix: add `reset_token_expires_at = models.DateTimeField()` with a 1-hour TTL; reject expired tokens at redemption. Use Django's built-in `PasswordResetTokenGenerator` which handles expiry and single-use invalidation.
>   7. **MEDIUM** — Missing CSRF protection (no `@csrf_protect` or DRF auth/permission decorator) on the view.
>   8. **MEDIUM** — Synchronous `send_reset_email()` inside the request handler blocks the response and provides no retry. Fix: offload to a Celery / RQ background task.
>   9. **MEDIUM** — Race condition between raw SQL `SELECT` and `User.objects.get(id=user_id)` ORM call — if the user row is deleted between these two queries, `DoesNotExist` raises an unhandled 500. Use a single ORM call.
> - **Quality Score Table** with at least four dimensions: `| Dimension | Score (0-10) | Rationale |` — Security (0/10 — SQL injection blocker), Correctness, Performance, Maintainability. Overall confidence = `min(HARD signals)` so Security=0 means overall confidence floor is 0.
> - **Verdict**: explicit `Verdict: REQUEST_CHANGES` (or `BLOCK` given the SQL injection blocker). Not approve.
> - **Adversarial analysis section**: explicitly consider "what happens if this endpoint is called 1000×/sec from one IP?" and "what if the email is `' OR 1=1 --`?" and "what if `linkedprofile_set` is empty?". Each as a separate sub-finding.
> - **Confidence levels per finding** (HIGH/MEDIUM/LOW) — not just severity. SQL injection = HIGH confidence; race condition = MEDIUM (requires concurrent delete).
> - **"Positive Observations" or "Questions for the Author" section at end** (per the agent's defined output format), not only findings.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Security Audit Report: Django Password Reset Handler

### Scope Summary

**Files analysed:** 1 file (`views.py`)  
**Risk classification:** Critical (1), High (5), Medium (2), Low (1)  
**Data flow entry points:** 1 — user email via POST parameter  
**Code classification:** Auth/Identity (Critical risk level)

---

## Findings (Ordered by Severity + Confidence)

| # | Severity | Confidence | Category | Finding | Location | Recommendation |
|---|---|---|---|---|---|---|
| 1 | **CRITICAL** | HIGH | A03: Injection | SQL injection via f-string interpolation | `views.py:14` | Use parameterised queries (`cursor.execute("SELECT id, username FROM auth_user WHERE email = %s", [email])`) or Django ORM (`User.objects.get(email=email)`) |
| 2 | **HIGH** | HIGH | A07: Auth Failures | User enumeration — different response status for known vs unknown email | `views.py:22` | Return HTTP 200 with generic message ("If an account exists for this email, a reset link has been sent") regardless of whether email is found |
| 3 | **HIGH** | HIGH | A02: Cryptographic Failures | Reset token stored in plaintext in database | `views.py:26` | Hash token before storage: `hashlib.sha256(token.encode()).hexdigest()`. Compare hashed value on token redemption. Full account takeover if DB leaks. |
| 4 | **HIGH** | HIGH | A07: Auth Failures | No token expiration / TTL on reset token | `views.py:26` | Add `reset_token_expires_at = models.DateTimeField()` field with 1-hour TTL. Reject expired tokens at redemption. Use Django's built-in `PasswordResetTokenGenerator` which handles expiry automatically. |
| 5 | **HIGH** | HIGH | A04: Insecure Design | No rate limiting on password reset endpoint | `views.py:9` | Add rate limiting: `@ratelimit(key='ip', rate='5/h', block=True)` from `django-ratelimit`. Prevents account enumeration probing, email flooding, and token generation abuse. |
| 6 | **HIGH** | MODERATE | A01: Broken Access Control | Race condition between raw SQL SELECT and ORM User.objects.get() | `views.py:14, 24` | If user is deleted between queries, `DoesNotExist` raises unhandled 500. Use single ORM call: `user = User.objects.get(email=email)` — eliminates both the SQL injection and the race condition. |
| 7 | **MEDIUM** | HIGH | A05: Security Misconfiguration | Missing CSRF protection on POST endpoint | `views.py:9` | Add `@csrf_protect` decorator OR use Django REST Framework with CSRF middleware. Without it, cross-site requests can trigger password resets. |
| 8 | **MEDIUM** | HIGH | A08: Data Integrity Failures | N+1 query pattern in profile update loop | `views.py:25–28` | Replace loop with bulk update: `LinkedProfile.objects.filter(user=user).update(reset_token=hashed_token)` — eliminates N separate UPDATE queries and the plaintext token issue. |
| 9 | **MEDIUM** | MODERATE | A04: Insecure Design | Synchronous email sending blocks response | `views.py:28` | Offload to async task (Celery/RQ): emit a `PasswordResetRequested` event and handle email dispatch in a background job. If SMTP is slow, user gets slow 200. If email fails, user thinks reset succeeded. |
| 10 | **LOW** | MODERATE | A07: Auth Failures | No email format validation | `views.py:10` | Validate email format with regex or `django.core.validators.validate_email()`. Prevents malformed input from reaching the query. |

---

## Data Flow Diagram (Critical Finding)

```
POST request with user input (email)
  ↓
views.py:10  →  email = request.POST.get('email', '')  [NO VALIDATION]
  ↓
views.py:14  →  cursor.execute(f"SELECT ... WHERE email = '{email}'")  [VULNERABLE]
  ↓
Database SQL parser interprets email value as SQL code
  ↓
VULNERABILITY: Malicious email like ' OR 1=1 -- bypasses WHERE clause

EXAMPLE ATTACK:
  email = "' OR 1=1 --"
  Query becomes: SELECT id, username FROM auth_user WHERE email = '' OR 1=1 --'
  Result: Returns ALL users (not just the target)
```

---

## Adversarial Analysis

### Attack Scenario 1: SQL Injection
**Question:** What happens if email is `' OR 1=1 --`?  
**Answer:** The query becomes `SELECT id, username FROM auth_user WHERE email = '' OR 1=1 --'`. The `OR 1=1` is always true, so the database returns the first user row (often the admin or lowest ID). The `--` comments out the trailing quote. The attacker now has an arbitrary user ID and can generate a reset token for any account.

**Finding #1 elaborated:**
```python
# DANGEROUS (current code)
cursor.execute(f"SELECT id, username FROM auth_user WHERE email = '{email}'")

# If email = "admin@example.com' OR '1'='1"
# Query sent to DB: SELECT id, username FROM auth_user WHERE email = 'admin@example.com' OR '1'='1'
# OR '1'='1' is ALWAYS TRUE → returns first user
```

**Evidence:** `views.py:14` — f-string directly interpolates unsanitized `email` variable.  
**Severity:** CRITICAL (full authentication bypass)  
**Confidence:** HIGH (SQL injection is trivial to exploit)

---

### Attack Scenario 2: User Enumeration via Status Code
**Question:** What if I submit 1000 emails and track which ones return 404 vs 200?  
**Answer:** I can build a complete list of all registered user emails. This enables:
- Targeted phishing ("we found your account")
- Credential stuffing (test if this email/password combo works elsewhere)
- OSINT on which team members have accounts

**Finding #2 elaborated:**
```python
# Current code leaks existence
if not row:
    return JsonResponse({'error': 'Email not found'}, status=404)  ← Different response
```

**Fix:**
```python
# Generic response regardless
return JsonResponse({'message': 'If an account exists for this email, a reset link has been sent.'}, status=200)
```

**Evidence:** `views.py:22` — returns 404 only when email is not found.  
**Severity:** HIGH (account enumeration)  
**Confidence:** HIGH (this pattern is well-known)

---

### Attack Scenario 3: Token Plaintext + No Expiry
**Question:** What if the database is breached?  
**Answer:** Every password reset token ever issued is now readable. If a token was generated 6 months ago and never used, it's still valid (no expiry check). An attacker can take any leaked token and reset anyone's password.

**Finding #3 & #4 elaborated:**
```python
# Current code
profile.reset_token = token  # Stored in plaintext
profile.save()              # No expiry field

# Attack: DB breach → attacker has plaintext tokens → account takeover
```

**Evidence:** `views.py:26` — token stored without hashing; no expiry field defined.  
**Severity:** HIGH (full account compromise if DB leaks)  
**Confidence:** HIGH (plaintext storage in DB is always a vulnerability)

---

### Attack Scenario 4: Rate Limiting Absence + Email Flooding
**Question:** What if I call this endpoint 1000 times/sec from one IP with different emails?  
**Answer:**
1. **DOS on email system:** The app sends 1000 reset emails instantly. If the SMTP server rate-limits per domain, legitimate users can't get password resets for hours.
2. **User enumeration at scale:** I can enumerate all users by hitting the endpoint with a email list and measuring response times or email delivery patterns.
3. **Account lockout abuse:** Some systems auto-lock after N failed attempts. If I trigger N resets for a target, I could lock them out.

**Finding #5 elaborated:**  
**Evidence:** `views.py:9` — no rate limit decorator or middleware  
**Severity:** HIGH (DOS, enumeration, account abuse)  
**Confidence:** HIGH (completely unprotected endpoint)

---

### Attack Scenario 5: Race Condition Between SELECT and ORM
**Question:** What if the user is deleted between the raw SQL query and the ORM call?  
**Answer:**
```python
cursor.execute(f"SELECT id, username FROM auth_user WHERE email = '{email}'")
row = cursor.fetchone()
# [WINDOW: User could be deleted here]
user = User.objects.get(id=user_id)  # DoesNotExist exception, unhandled 500
```

**Finding #6 elaborated:**  
**Evidence:** `views.py:14, 24` — gap between raw SQL SELECT and ORM query  
**Severity:** HIGH (unhandled exception = 500 error + information leak)  
**Confidence:** MODERATE (requires concurrent user deletion, but is exploitable)

---

### Attack Scenario 6: Synchronous Email Blocking
**Question:** What if `send_reset_email()` takes 30 seconds?  
**Answer:** The user's request hangs for 30 seconds. If there's a Celery/RQ failure and email never sends, the user thinks the reset succeeded and checks their email for 24 hours. When they finally try to reset again, the first token is still valid (no expiry), so an attacker can intercept it.

**Finding #9 elaborated:**  
**Evidence:** `views.py:28` — synchronous call inside request handler  
**Severity:** MEDIUM (blocks responses, creates false success perception)  
**Confidence:** HIGH (observable in slow email environments)

---

## Quality Score Table

| Dimension | Score (0–10) | Rationale |
|---|---|---|
| **Security** | **1/10** | SQL injection blocker (CRITICAL), user enumeration, plaintext tokens, no rate limiting, no expiry. Multiple vectors for account takeover and DOS. |
| **Correctness** | **3/10** | Race condition between SELECT and ORM. N+1 queries. Unhandled exception on user deletion. Email validation missing. |
| **Performance** | **4/10** | Synchronous email sending blocks requests. N+1 queries multiply database load. Missing index hint (email field should be indexed). |
| **Maintainability** | **5/10** | Uses raw SQL instead of ORM (harder to reason about). Mixes low-level cursor work with high-level ORM. No logging. Email sending is tightly coupled to the request. |
| **Overall Confidence** | **1/10** | Security floor (1) = overall confidence floor. The SQL injection alone disqualifies this code from production. |

---

## Verdict

**`REQUEST_CHANGES` — DO NOT MERGE**

This code is **not production-ready**. The SQL injection at line 14 is a blocker that grants attackers full authentication bypass. Combined with plaintext tokens, no rate limiting, and user enumeration, this endpoint is a critical attack surface.

**Before merging, fix (in order):**
1. **SQL Injection** — replace raw SQL with `User.objects.get(email=email)` (fixes race condition too)
2. **Plaintext tokens** — hash tokens before storage
3. **Token expiry** — add TTL; use Django's `PasswordResetTokenGenerator`
4. **Rate limiting** — add `@ratelimit(key='ip', rate='5/h')`
5. **User enumeration** — return 200 with generic message for all cases
6. **CSRF protection** — add `@csrf_protect`
7. **N+1 queries** — use `bulk_update` or single query
8. **Async email** — dispatch to Celery task

Estimated effort: **4–6 hours** (use Django's built-in `PasswordResetTokenGenerator` to accelerate).

---

## OWASP Coverage

| Category | Status | Notes |
|---|---|---|
| A01: Broken Access Control | **FAIL** | No rate limiting, user enumeration via status codes, race condition in concurrent deletion |
| A02: Cryptographic Failures | **FAIL** | Plaintext token storage, no expiry, no hashing |
| A03: Injection | **FAIL** | SQL injection via f-string interpolation — CRITICAL |
| A04: Insecure Design | **FAIL** | No rate limiting, no abort on repeated failures, synchronous email sending creates false success |
| A05: Security Misconfiguration | **FAIL** | Raw SQL instead of ORM, missing CSRF decorator |
| A06: Vulnerable Components | **N/A** | Not checked (dependencies not in scope) |
| A07: Auth Failures | **FAIL** | No token expiry, plaintext tokens, missing CSRF, no strong password policy enforcement downstream |
| A08: Data Integrity | **FAIL** | Race condition, N+1 query pattern, no bulk operations |
| A09: Logging Failures | **FAIL** | No audit log of reset attempts, no alerting on suspicious patterns |
| A10: SSRF | **N/A** | Not applicable to this endpoint |

---

## Positive Observations

- ✅ **Token generation is secure:** Using `secrets.token_urlsafe(32)` is correct; the issue is storage, not generation.
- ✅ **Linked account model exists:** The code thoughtfully handles multiple linked profiles per user, which is a good design pattern.
- ✅ **HTTP method gating:** Correctly rejects non-POST requests.

---

## What Was NOT Checked

- **Dependencies & versions:** No audit of Django version, Celery, or email backend. Assumes Django 3.0+.
- **Downstream token redemption:** This audit only reviews the reset *request*. The token *verification* endpoint (not shown) may have additional vulnerabilities.
- **Email template injection:** The `send_reset_email()` function is not shown. If the email body contains user input, there's a secondary injection risk.
- **Infrastructure & deployment:** No audit of HTTPS enforcement, database encryption, or secrets management.
- **Session management:** No review of whether authenticated users are properly invalidated after a reset.
- **Logging and monitoring:** No check for audit trails, alerting, or incident response procedures.
- **Test coverage:** No review of unit/integration tests for this endpoint.

---

## Top Priorities (Fix First)

1. **SQL Injection (Finding #1)** — Use ORM. Takes 2 minutes. Blocks everything else.
2. **User Enumeration (Finding #2)** — Return 200 always. Takes 1 minute.
3. **Plaintext Tokens + Expiry (Findings #3, #4)** — Use `PasswordResetTokenGenerator`. Takes 30 minutes, prevents token replay.
4. **Rate Limiting (Finding #5)** — Add decorator. Takes 5 minutes, prevents DOS and enumeration at scale.

Once these four are fixed, the remaining findings (CSRF, N+1, async email) are moderate-priority refactoring.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 12.0/14.0 (86%) |
| Evaluated | 2026-05-03 |
| Target duration | 52971 ms |
| Target cost | $0.1178 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent identifies the SQL injection vulnerability (f-string interpolation into the raw SQL query) as a blocker with specific file:line reference | PASS | Finding #1 in the table: 'SQL injection via f-string interpolation \| views.py:14' rated CRITICAL/HIGH. The verdict section repeats: 'The SQL injection at line 14 is a blocker'. Attack Scenario 1 details the f-string exploit with concrete example. |
| c2 | Agent identifies the N+1 query in the loop over linkedprofile_set as a performance finding, with a specific fix (select_related or prefetch_related) | PARTIAL | Finding #8 identifies 'N+1 query pattern in profile update loop' at views.py:25–28 and provides a concrete fix: 'LinkedProfile.objects.filter(user=user).update(reset_token=hashed_token)'. However, the fix is a bulk update rather than the criterion-specified select_related or prefetch_related approaches. |
| c3 | Agent flags the missing rate limiting on the password reset endpoint as a security finding | PASS | Finding #5: 'No rate limiting on password reset endpoint' at views.py:9, HIGH/HIGH, with fix '@ratelimit(key="ip", rate="5/h", block=True)'. Also covered in detail in Attack Scenario 4. |
| c4 | Agent produces a quality score table covering at least Security, Correctness, Performance, and Maintainability dimensions | PASS | Quality Score Table contains exactly these four dimensions: Security (1/10), Correctness (3/10), Performance (4/10), Maintainability (5/10), each with explicit rationale. |
| c5 | Agent gives a verdict of REQUEST CHANGES or BLOCK (not APPROVE) given the SQL injection blocker | PASS | Verdict section reads: '`REQUEST_CHANGES` — DO NOT MERGE'. This is unambiguous and non-approving. |
| c6 | Agent runs adversarial analysis — considers what happens if the endpoint is called 1000 times in rapid succession | PASS | Attack Scenario 4 is titled 'Rate Limiting Absence + Email Flooding' and opens with 'What if I call this endpoint 1000 times/sec from one IP with different emails?' — addressing DOS on email system, enumeration at scale, and account lockout abuse. |
| c7 | Agent notes that the 404 response on unknown email leaks account existence information (user enumeration) and recommends returning 200 regardless | PARTIAL | Finding #2 explicitly identifies 'User enumeration — different response status for known vs unknown email' at views.py:22. Fix provided: 'Return HTTP 200 with generic message'. Attack Scenario 2 elaborates. Ceiling capped at PARTIAL. |
| c8 | Every finding cites a specific location in the code and includes a concrete suggested fix | PASS | All 10 findings in the table include a views.py:N location and a concrete code-level recommendation (e.g., cursor.execute with %s parameterisation, bulk_update call, @ratelimit decorator, hashlib.sha256 hashing, @csrf_protect, PasswordResetTokenGenerator). |
| c9 | Output recommends parameterised queries (e.g. `cursor.execute("SELECT ... WHERE email = %s", [email])`) or the Django ORM (`User.objects.filter(email=email).first()`) as the fix for the SQL injection, not just 'sanitise input' | PASS | Finding #1 fix: 'Use parameterised queries (cursor.execute("SELECT id, username FROM auth_user WHERE email = %s", [email])) or Django ORM (User.objects.get(email=email))'. Both specific alternatives are named. |
| c10 | Output assigns confidence levels (HIGH / MODERATE / LOW or numeric 0-100) to individual findings, not only an overall confidence | PASS | The findings table has a dedicated 'Confidence' column with per-finding values: HIGH for findings 1–5, 7–8; MODERATE for findings 6, 9–10. |
| c11 | Output's Security score is 0 (or otherwise reflects that a HARD signal hit zero) given the SQL injection, and the overall confidence reflects `min(HARD signals)` rather than averaging the issue away | PARTIAL | Security score is 1/10, not 0/10 as specified. The criterion requires 0 or a score that 'reflects a HARD signal hit zero'. Overall Confidence is 1/10 with rationale 'Security floor (1) = overall confidence floor', which does implement the min() pattern. The security score deviates from the expected 0. |
| c12 | Output flags the unconditional `User.objects.get(id=user_id)` as a correctness or robustness issue (raises `DoesNotExist` if the row vanishes between the raw query and the ORM lookup, or if `linkedprofile_set` is empty no token is ever persisted to the user) | PASS | Finding #6: 'Race condition between raw SQL SELECT and ORM User.objects.get()' at views.py:14, 24. 'If user is deleted between queries, DoesNotExist raises unhandled 500.' Attack Scenario 5 elaborates with code showing the deletion window. |
| c13 | Output identifies that the same reset token is reused across every linked profile and recommends per-profile token generation (or explains why a single token is acceptable) — a token-handling concern beyond the SQL/N+1/rate-limit trio | FAIL | No finding in the output addresses the single shared token being used across all linked profiles. The positive observation section even commends the linked account model without noting the shared-token risk. The bulk update fix in Finding #8 perpetuates the single token approach without comment. |
| c14 | Output notes that `reset_token` appears to be stored in plaintext on the profile and recommends hashing the token at rest (storing only a hash, comparing on redemption) | PARTIAL | Finding #3: 'Reset token stored in plaintext in database' at views.py:26. Fix: 'Hash token before storage: hashlib.sha256(token.encode()).hexdigest(). Compare hashed value on token redemption.' Attack Scenario 3 elaborates. Ceiling capped at PARTIAL. |
| c15 | Output flags the absence of a token expiry / time-to-live on the reset token as a security concern | PARTIAL | Finding #4: 'No token expiration / TTL on reset token' at views.py:26. Fix includes reset_token_expires_at with 1-hour TTL and PasswordResetTokenGenerator. Attack Scenario 3 also notes 'a token generated 6 months ago... is still valid'. Ceiling capped at PARTIAL. |
| c16 | Output calls out that emails are sent synchronously inside the request handler (blocking the response, no retry) and suggests offloading to a background task or queue | PARTIAL | Finding #9: 'Synchronous email sending blocks response' at views.py:28. Fix: 'Offload to async task (Celery/RQ): emit a PasswordResetRequested event and handle email dispatch in a background job.' Attack Scenario 6 describes the 30-second hang scenario. Ceiling capped at PARTIAL. |
| c17 | Output includes a 'Positive Observations' or 'Questions for the Author' section consistent with the agent's defined output format, not only findings | PARTIAL | A 'Positive Observations' section is present at the end with three items: secure token generation via secrets.token_urlsafe(32), the linked account model as good design, and HTTP method gating. Ceiling capped at PARTIAL. |

### Notes

The output is a thorough, well-structured security review that handles the three headline issues (SQL injection, N+1, rate limiting) plus seven additional findings with correct OWASP categorisation and concrete fixes. The adversarial analysis section is strong, covering all four scenarios including 1000 req/sec. The main gap is c13 — the shared reset token across all linked profiles is not identified as a concern, despite being a meaningful security issue. The quality table deviates slightly from the expected zero-floor Security score (gives 1/10 instead of 0/10), earning partial credit. The N+1 fix is correct and more accurate than the criterion's suggested fix (bulk_update vs select_related for write N+1), but since the criterion explicitly names select_related/prefetch_related, only partial credit is awarded. Positive Observations and per-finding confidence levels are both present.
