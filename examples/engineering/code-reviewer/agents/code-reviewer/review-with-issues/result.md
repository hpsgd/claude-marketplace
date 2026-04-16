# Review with issues

A developer asks the code reviewer agent to review a Python Django view that handles user password reset. The code contains a SQL injection risk, an N+1 query, and missing rate limiting on the endpoint.

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

The code reviewer agent, given this prompt, would produce the following response.

---

## Output

**Pre-flight:** reads `CLAUDE.md` and installed rules. Checks for existing auth patterns and security-sensitive files.

**Pass 1 (Context):** Single view function — password reset handler. Auth-critical code path. Reads full `views.py`. No accompanying tests found. No rate limiting middleware visible in settings.

**Pass 2 (Correctness):**
- Token has no expiry — `reset_token` is stored but no timestamp or TTL field exists. A token issued months ago would still be valid.
- `User.objects.get(id=user_id)` at line 34 will raise `User.DoesNotExist` if the raw SQL query and ORM operate on different user tables (unlikely but possible in multi-tenant setups). No exception handling around this call.

**Pass 3 (Security):**
- **BLOCKER — SQL injection** `views.py:24`: f-string interpolates `email` directly into raw SQL. Any value like `' OR '1'='1` passes through unescaped. **Fix:** `cursor.execute("SELECT id, username FROM auth_user WHERE email = %s", [email])`
- **HIGH — No rate limiting** on this endpoint. **Adversarial analysis:** 1000 POST requests would enumerate valid emails from 404 vs 200 responses, exhaust `secrets.token_urlsafe()` overhead, and flood linked-account email addresses with reset emails. `django-ratelimit` or a reverse-proxy rate limit (e.g. nginx `limit_req`) is required before this ships.
- **MEDIUM — User enumeration** `views.py:27-28`: `JsonResponse({'error': 'Email not found'}, status=404)` reveals whether an email address is registered. **Fix:** Return `JsonResponse({'message': 'If that address is registered, you will receive an email.'}, status=200)` regardless of whether the user exists.

**Pass 4 (Quality):**
- **N+1 query** `views.py:35-38`: `linkedprofile_set.all()` inside a loop fires one SELECT per profile's `.save()` call. For a user with 10 linked profiles this makes 10 update queries sequentially. **Fix:** `user = User.objects.prefetch_related('linkedprofile_set').get(id=user_id)` before the loop, then batch token updates.
- No test coverage.

**Quality score table:**

| Dimension | Score | Evidence |
|---|---|---|
| Security | 0 | SQL injection blocker at `views.py:24` |
| Correctness | 45 | Token has no expiry; `DoesNotExist` not caught at line 34 |
| Data integrity | 65 | Token overwrites all profiles atomically but no transaction wrapper |
| Performance | 40 | N+1 at `views.py:35-38` |
| Maintainability | 40 | Raw SQL mixed with ORM; no tests |
| Test coverage | 0 | No tests found |
| **Confidence** | **0** | min(HARD) = 0 — Security blocker |

**Verdict: BLOCK** — SQL injection in an authentication endpoint is a critical vulnerability. Cannot merge.

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/8 criteria met (94%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Agent identifies SQL injection as blocker with file:line — the agent definition mandates Pass 3 (Security) covering injection; the output format requires `file:line` on every finding; HARD signal rule means any security = 0 blocks approval. The definition is explicit: "Injection — is any user input concatenated into SQL queries, shell commands, file paths?" under Pass 3. Reference traces to `views.py:24`.

- [x] PASS: Agent identifies N+1 with specific fix (prefetch_related) — Pass 4 Quality explicitly covers "N+1 queries (database call inside a loop)" under Performance. The calibration rule "A finding without a fix suggestion is incomplete" enforces a concrete fix. `select_related` / `prefetch_related` is the standard Django pattern.

- [x] PASS: Agent flags missing rate limiting as security finding — the Adversarial Analysis section is mandatory for every review: "Repetition: what happens if the same action is performed 1000 times?" This steer surfaces rate limiting on a public auth endpoint as a required finding, not an optional one.

- [x] PASS: Agent produces quality score table covering ≥4 dimensions — the agent definition's output format template defines Security, Correctness, Data integrity, Performance, Maintainability, Test coverage as required dimensions. All four specified dimensions are present.

- [x] PASS: Agent gives BLOCK verdict — HARD signal rule is explicit: "any zero blocks approval." SQL injection → Security = 0 → overall confidence = min(HARD scores) = 0. The agent definition does not permit APPROVE or REQUEST_CHANGES when a HARD signal is zero.

- [x] PASS: Agent runs adversarial analysis — Adversarial Analysis is a mandatory review section per the agent definition. The "Repetition: 1000 times" heuristic is listed explicitly. The definition enforces this for every review regardless of the reviewer's judgment about relevance.

- [~] PARTIAL: Agent notes 404 leaks account existence (user enumeration) — Pass 3 covers "data exposure: Are error messages safe for external users?" which partially covers existence disclosure. However the agent definition focuses on stack traces, internal paths, and secret leakage rather than boolean account existence via status codes. The definition partially supports this finding but would not reliably require it as a distinct item. The simulated output produces it; a different agent implementation might subsume it under the rate-limiting finding.

- [x] PASS: Every finding cites specific location with concrete fix — calibration rules state: "A finding without evidence is not a finding. Show the code." and "A finding without a fix suggestion is incomplete. Propose the change." Both are explicit prohibitions enforced across all findings.

## Notes

The agent definition is strong on the HARD signal path — SQL injection in an auth handler will always surface as a BLOCK given the security pass + adversarial analysis combination. The user enumeration gap is a real limitation in the definition: the data exposure check focuses on secrets and stack traces rather than boolean existence leakage via HTTP status codes. Adding "does any response reveal account existence?" to Pass 3's data exposure checklist would close this. The quality score table including Data integrity and Test coverage beyond the minimum four required dimensions is a strength.
