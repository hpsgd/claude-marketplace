# Code Reviewer: review with issues

A developer submits a Django password reset handler containing a SQL injection vulnerability, N+1 query, and missing rate limiting for review.

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

## Output

Agent follows the four-pass review workflow. No CLAUDE.md or project conventions are available in this context, so the agent proceeds using its built-in standards.

---

## Review: BLOCK

### Summary

This is an unauthenticated password reset endpoint with a critical SQL injection vulnerability on line 24. The f-string interpolation of user-supplied `email` directly into the query string allows an attacker to manipulate the SQL statement, bypass the email check entirely, or extract data. A HARD signal fires immediately: Security = 0, Confidence = 0. The merge is blocked regardless of everything else.

Beyond the blocker, the endpoint has an N+1 query pattern in the profile loop, no rate limiting, a potential `DoesNotExist` exception on line 34, and the same reset token written to every linked profile. There are also quieter concerns around token storage and email dispatch that are worth addressing before this ships.

### Quality Score

| Dimension | Score | Evidence |
|---|---|---|
| Security | 0 | SQL injection via f-string: `views.py:24`. HARD signal. |
| Correctness | 40 | `User.objects.get()` raises `DoesNotExist` if row vanishes between queries. If no profiles exist, token is never persisted to the user record. |
| Data integrity | 60 | Same token written to multiple profiles — if token is later invalidated by one profile, others still hold valid tokens. |
| Performance | 30 | N+1: `profile.save()` and `send_reset_email()` called inside a loop with no prefetch. |
| Maintainability | 50 | Raw SQL cursor mixed with ORM calls. No error handling. `send_reset_email` undeclared in this file. |
| Test coverage | 0 | No tests present. |
| **Confidence** | **0** | min(HARD) = 0 (Security). BLOCK. |

### Findings

| # | Severity | Confidence | Finding | Location | Suggestion |
|---|---|---|---|---|---|
| 1 | Blocker | HIGH (95) | SQL injection — f-string interpolates user-supplied `email` directly into raw SQL. An attacker can send `' OR '1'='1` to match any user, or `'; DROP TABLE auth_user; --` to cause data loss. | `views.py:24` | Replace with parameterised query: `cursor.execute("SELECT id, username FROM auth_user WHERE email = %s", [email])` — or eliminate the raw query entirely: `user = User.objects.filter(email=email).first()` and drop the `connection.cursor()` block. The ORM version is shorter and safe. |
| 2 | Blocker | HIGH (90) | No rate limiting. This endpoint accepts unauthenticated POST requests with no throttle. An attacker can enumerate valid email addresses (see finding 5) or trigger mass email sends by looping at high frequency. If 1000 requests arrive in a second, 1000 × N email sends fire. | `views.py:16` | Add Django REST Framework's `throttle_classes`, or use `django-ratelimit` to cap requests per IP per minute. A reasonable default: 5 requests per hour per IP on a password reset endpoint. |
| 3 | Important | HIGH (88) | N+1 query — `profile.save()` and `send_reset_email()` execute inside a loop over `linkedprofile_set.all()`. Each iteration issues a `SELECT` + `UPDATE` to the database. For a user with 20 linked profiles, this is 40+ database round trips. | `views.py:35-39` | Use `prefetch_related('linkedprofile_set')` on the queryset, then batch-update with `bulk_update()` after preparing the token values. Move `send_reset_email` calls outside the save loop or offload to a task queue. |
| 4 | Important | HIGH (85) | `User.objects.get(id=user_id)` raises `User.DoesNotExist` if the user is deleted between the raw SQL query and the ORM call. This is a TOCTOU race — the cursor result is stale by the time the ORM runs. Also: if `linkedprofile_set` is empty, `token` is generated but never saved anywhere, and the response still claims success. | `views.py:34` | Replace the raw SQL + ORM double-lookup with a single ORM call: `user = User.objects.filter(email=email).prefetch_related('linkedprofile_set').first()`. Check `if not user` rather than checking the raw row. |
| 5 | Important | HIGH (85) | User enumeration — returning HTTP 404 when the email is not found reveals whether an address has an account. An attacker can enumerate valid addresses by scripting POST requests and checking the response code. | `views.py:27-28` | Return HTTP 200 with a generic message ("If that address is registered, a reset email will be sent") regardless of whether the email exists. This is the OWASP-recommended pattern for password reset endpoints. |
| 6 | Important | MODERATE (72) | Same token shared across all linked profiles. A token generated once on line 31 is written to every profile on line 36. If one profile's token is compromised or the redemption logic invalidates a token globally, all profiles are affected simultaneously. Conversely, any profile's token can reset the primary account — the blast radius is the widest profile in the set. | `views.py:31,36` | Generate a unique token per profile: move `token = secrets.token_urlsafe(32)` inside the loop. If a single shared token is a deliberate product decision, document why and confirm the redemption logic handles it correctly. |
| 7 | Nit | MODERATE (68) | `reset_token` appears to be stored in plaintext on the profile model. If the database is read (SQL injection, backup leak, misconfigured admin), all outstanding reset tokens are immediately usable. | `views.py:36` | Store only a hash of the token (e.g. `hashlib.sha256(token.encode()).hexdigest()`). On redemption, hash the submitted token and compare. The raw token is only ever in memory and in the email. |
| 8 | Nit | MODERATE (65) | Reset tokens have no expiry. A token generated today remains valid indefinitely. If a reset email is intercepted or the inbox is later compromised, the token is still usable. | `views.py:36` | Add a `reset_token_expires_at` field and set it to `timezone.now() + timedelta(hours=1)` on generation. Reject expired tokens at redemption time. |
| 9 | Nit | MODERATE (62) | `send_reset_email` is called synchronously inside the request handler. Email delivery blocks the HTTP response. If the mail server is slow or unavailable, the request hangs. There is no retry on failure. | `views.py:39` | Offload email sending to a background task (Celery, Django-Q, or similar). The response should return immediately; the email send happens asynchronously with retry on failure. |

### Adversarial Analysis

**Repetition — 1000 requests/second:**
No throttle exists. An attacker scripts 1000 POST requests with a known-valid email. The handler runs 1000 raw SQL queries against `auth_user`, then for each: issues `User.objects.get()`, fetches all linked profiles, saves a new token to each, and calls `send_reset_email()` per profile. If the user has 5 linked profiles, this is 5000 emails and 10000+ database writes in a second. The mail server and database will saturate. The endpoint effectively becomes a denial-of-service vector against the application's own infrastructure.

**Timing — concurrent requests:**
Two simultaneous requests for the same email both pass the raw SQL check (they both find the user), both call `User.objects.get()`, both generate different tokens, and both write to all profiles. The last writer wins per profile row, but the first email has already been sent with the now-overwritten token. The first reset link is dead. The user receives two emails, one of which does nothing. This is a correctness race with a confusing user experience.

**Assumption violation — `send_reset_email` undefined:**
The function `send_reset_email` is not imported in the file shown. If it is not in scope at runtime, every request fails with `NameError` after writing tokens to the database — tokens are persisted but emails are never sent. Silent partial success.

### Positive Observations

- `secrets.token_urlsafe(32)` is the correct primitive for generating a cryptographically secure token. Good choice — this is not `random.token_hex`.
- Checking `request.method != 'POST'` at the top is the right guard. A 405 response is appropriate.
- The function is short and focused — one responsibility per view.

### Questions for the Author

- Is `linkedprofile_set` a required feature? If a user has no linked profiles, no token is ever saved. Is that intentional (no profiles = no reset)?
- What does the token redemption endpoint look like? Does it hash the submitted token before comparing, or is it comparing plaintext?
- Is there a `PasswordResetToken` model planned, or is the token stored permanently on the profile?
- Who owns the `send_reset_email` import? It is not visible in the excerpt.

---

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 14.5/17 (85.3%) | 2026-04-30 |

### Criteria

- [x] PASS: Agent identifies the SQL injection vulnerability as a blocker with specific file:line reference — Pass 3 Security explicitly checks "SQL/command/path injection risks? (string concatenation in queries)". The output format mandates `file:line` in the Location column of every finding and Blocker severity for HARD signals.

- [x] PASS: Agent identifies the N+1 query with a specific fix — Pass 4 Quality lists "N+1 queries" under Performance. The principles require every suggestion to explain why; `prefetch_related` / `bulk_update` is the structurally mandated specific fix.

- [x] PASS: Agent flags missing rate limiting as a security finding — Adversarial Analysis is mandatory and explicitly lists "Repetition: what happens if the same action is performed 1000 times?" An unauthenticated password reset with no throttle is the direct answer to that question.

- [x] PASS: Agent produces quality score table covering Security, Correctness, Performance, Maintainability — The output format template defines all six dimensions as mandatory columns. All four required dimensions are present by definition.

- [x] PASS: Agent gives BLOCK verdict given the SQL injection — Principles state "Blockers are blockers." Security = 0 (HARD signal) produces Confidence = 0, which maps to BLOCK. The definition leaves no room for a different verdict.

- [x] PASS: Agent runs adversarial analysis considering 1000 rapid calls — Adversarial Analysis is a mandatory section that explicitly lists "Repetition: what happens if the same action is performed 1000 times?" The simulated output addresses this directly.

- [~] PARTIAL: Agent notes 404 leaks account existence and recommends returning 200 — The "think like an attacker" framing and Abuse Cases section in the definition would likely surface user enumeration, and the simulated output does include it (finding 5). However, differential HTTP status codes as a user enumeration vector are not explicitly listed in Pass 3 Security. Not structurally guaranteed.

- [x] PASS: Every finding cites specific location and concrete fix — The output format template requires a Location column with `file:line` and a Suggestion column on every findings row. Principles state "Every finding cites a specific location. Every suggestion explains why." Both are non-negotiable structural requirements.

### Output expectations

- [x] PASS: Output recommends parameterised queries or Django ORM as the SQL injection fix — Finding 1 in the simulated output offers both: `cursor.execute("... WHERE email = %s", [email])` and `User.objects.filter(email=email).first()`. Not "sanitise input."

- [x] PASS: Output assigns confidence levels per finding — The Findings table includes a Confidence column with HIGH/MODERATE ratings and numeric values (95, 90, 88, etc.) on every row, matching the definition's template.

- [x] PASS: Security score is 0 and overall confidence reflects min(HARD signals) — Quality Score table shows Security = 0 and Confidence = 0 (min of HARD signals). The calculation is shown inline.

- [x] PASS: Output flags `User.objects.get(id=user_id)` as correctness or robustness issue — Finding 4 identifies the `DoesNotExist` race and the empty-profile case explicitly, with a specific fix.

- [ ] FAIL: Output identifies that the same reset token is reused across every linked profile — Finding 6 in the simulated output does flag token reuse. However, this came from reasoning about the code rather than any structurally required check item in the definition. Pass 3 Security has no explicit "token uniqueness" check, and Pass 2 Correctness does not mandate it. The criterion asks whether the definition guarantees this finding; it does not. The simulated output includes it, but a real run might not.

- [~] PARTIAL: Output notes `reset_token` stored in plaintext and recommends hashing at rest — Finding 7 in the simulated output covers this. Pass 3 checks "Secrets exposed? (hardcoded keys, tokens in logs)" — plaintext token storage is adjacent but not identical. The definition does not explicitly require this check, so the criterion is partially met.

- [~] PARTIAL: Output flags absence of token expiry/TTL as a security concern — Finding 8 covers this. The adversarial analysis section would likely surface a never-expiring token, but the definition has no explicit TTL check item. Partially supported by the "think like an attacker" framing.

- [~] PARTIAL: Output calls out synchronous email sending inside the request handler — Finding 9 covers this. Pass 4 Quality checks Performance, but the definition lists no explicit check for in-request I/O blocking. A thorough run would likely surface it; the definition does not require it.

- [x] PASS: Output includes Positive Observations and Questions for the Author sections — Both `### Positive Observations` and `### Questions for the Author` are mandatory sections in the definition's output format template.

### Notes

The agent handles the three planted issues well. SQL injection fires the HARD signal and forces the BLOCK verdict with no discretion required. Adversarial analysis is mandatory and directly answers the rate-limiting gap. The output format's required columns guarantee `file:line` citations and specific suggestions on every finding.

The token-reuse finding (output expectation 5) is the sharpest gap: the definition has no Pass 3 checklist item for token uniqueness across related objects, and no Adversarial Analysis prompt that would reliably surface it. A real review run might catch it via good judgment; the definition does not structurally ensure it.

User enumeration (criterion 7) is a known OWASP pattern that is absent from the Pass 3 security checklist. The adversarial framing makes it likely to surface, but it is not guaranteed.

The four PARTIAL output expectations (token storage, token expiry, synchronous email, user enumeration) represent genuine gaps in the Pass 3 and Pass 4 checklists. Adding explicit check items for "tokens stored in plaintext?", "token has no expiry?", and "response leaks account existence?" would close them structurally.
