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

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Three categories of issues here: a critical security vulnerability, a moderate security issue, and a design problem.

---

**Critical: SQL Injection**

```python
cursor.execute(f"SELECT id, username FROM auth_user WHERE email = '{email}'")
```

This is directly interpolating user input into SQL. An attacker can supply `' OR '1'='1` or worse. There's no reason to use raw SQL here at all — use the ORM:

```python
try:
    user = User.objects.get(email=email)
except User.DoesNotExist:
    user = None
```

If you must use raw SQL, use parameterized queries: `cursor.execute("SELECT id FROM auth_user WHERE email = %s", [email])`.

---

**Moderate: User enumeration**

```python
if not row:
    return JsonResponse({'error': 'Email not found'}, status=404)
```

Returning a distinct 404 tells attackers which email addresses are registered. Return 200 with a generic message regardless of whether the email exists — "If that address is registered, you'll receive a reset email."

---

**Design: Token shared across all linked profiles, no expiry**

The same token is fanned out to every linked profile. If any profile's token is compromised, all accounts are exposed. Each profile (or better: the user) should get one token, stored once, with an expiry timestamp. Consider using Django's built-in `PasswordResetTokenGenerator` which handles expiry and invalidation on use.

---

Also worth noting: no `@csrf_protect` decorator on this POST endpoint. Django's middleware may cover it depending on your config, but it's worth verifying.

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 4.0/13.0 (31%) |
| Evaluated | 2026-04-30 |
| Target duration | 15143 ms |
| Target cost | $0.0899 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent identifies the SQL injection vulnerability (f-string interpolation into the raw SQL query) as a blocker with specific file:line reference | PARTIAL | Output labels it 'Critical: SQL Injection' and quotes the offending f-string, but gives no file:line reference (e.g. 'views.py:14'). The criterion requires a specific file:line citation. |
| c2 | Agent identifies the N+1 query in the loop over linkedprofile_set as a performance finding, with a specific fix (select_related or prefetch_related) | FAIL | The loop is mentioned only in the context of token-sharing design, not as an N+1 query. Neither select_related nor prefetch_related is suggested anywhere in the output. |
| c3 | Agent flags the missing rate limiting on the password reset endpoint as a security finding | FAIL | Rate limiting is not mentioned at all in the output. The four issues raised are SQL injection, user enumeration, token sharing, and missing CSRF decorator. |
| c4 | Agent produces a quality score table covering at least Security, Correctness, Performance, and Maintainability dimensions | FAIL | No score table of any kind appears in the output. |
| c5 | Agent gives a verdict of REQUEST CHANGES or BLOCK (not APPROVE) given the SQL injection blocker | FAIL | No explicit verdict (APPROVE / REQUEST CHANGES / BLOCK) is issued. The output uses the label 'Critical' but never renders a formal review decision. |
| c6 | Agent runs adversarial analysis — considers what happens if the endpoint is called 1000 times in rapid succession | FAIL | No adversarial analysis is present. The high-volume abuse scenario is not considered anywhere in the output. |
| c7 | Agent notes that the 404 response on unknown email leaks account existence information (user enumeration) and recommends returning 200 regardless | PASS | Output has a dedicated 'Moderate: User enumeration' section: 'Returning a distinct 404 tells attackers which email addresses are registered. Return 200 with a generic message regardless of whether the email exists.' Ceiling is PARTIAL so maximum is 0.5. |
| c8 | Every finding cites a specific location in the code and includes a concrete suggested fix | PARTIAL | SQL injection and user enumeration findings quote the exact offending lines and provide concrete fixes. The token-sharing finding references the loop but offers only a design direction ('each profile should get one token, stored once, with an expiry timestamp') without a code example. No file:line numbers are used. Coverage is partial. |
| c9 | Output recommends parameterised queries (e.g. `cursor.execute("SELECT ... WHERE email = %s", [email])`) or the Django ORM (`User.objects.filter(email=email).first()`) as the fix for the SQL injection, not just 'sanitise input' | PASS | Output gives both fixes explicitly: ORM via `User.objects.get(email=email)` and parameterized raw SQL via `cursor.execute("SELECT id FROM auth_user WHERE email = %s", [email])`. |
| c10 | Output assigns confidence levels (HIGH / MODERATE / LOW or numeric 0-100) to individual findings, not only an overall confidence | FAIL | No confidence levels are assigned to any individual finding. The section headers use 'Critical' and 'Moderate' as severity labels, not confidence indicators. |
| c11 | Output's Security score is 0 (or otherwise reflects that a HARD signal hit zero) given the SQL injection, and the overall confidence reflects `min(HARD signals)` rather than averaging the issue away | FAIL | No score table exists, so there is no Security score and no min(HARD signals) calculation. |
| c12 | Output flags the unconditional `User.objects.get(id=user_id)` as a correctness or robustness issue (raises `DoesNotExist` if the row vanishes between the raw query and the ORM lookup, or if `linkedprofile_set` is empty no token is ever persisted to the user) | FAIL | The `User.objects.get(id=user_id)` call is not mentioned at all. The race condition and empty-linkedprofile edge cases are not discussed. |
| c13 | Output identifies that the same reset token is reused across every linked profile and recommends per-profile token generation (or explains why a single token is acceptable) — a token-handling concern beyond the SQL/N+1/rate-limit trio | PASS | 'The same token is fanned out to every linked profile. If any profile's token is compromised, all accounts are exposed. Each profile (or better: the user) should get one token, stored once, with an expiry timestamp.' |
| c14 | Output notes that `reset_token` appears to be stored in plaintext on the profile and recommends hashing the token at rest (storing only a hash, comparing on redemption) | FAIL | Plaintext token storage is not mentioned. No recommendation to hash the token at rest appears anywhere in the output. |
| c15 | Output flags the absence of a token expiry / time-to-live on the reset token as a security concern | PARTIAL | The token-sharing section mentions 'with an expiry timestamp' and suggests 'Django's built-in PasswordResetTokenGenerator which handles expiry and invalidation on use.' Expiry is raised but not as a named standalone finding — it's embedded in the design note. |
| c16 | Output calls out that emails are sent synchronously inside the request handler (blocking the response, no retry) and suggests offloading to a background task or queue | FAIL | Synchronous email sending is not flagged as an issue. The loop over `send_reset_email` is mentioned only in the context of token reuse, not blocking or retry concerns. |
| c17 | Output includes a 'Positive Observations' or 'Questions for the Author' section consistent with the agent's defined output format, not only findings | FAIL | No 'Positive Observations' or 'Questions for the Author' section appears. The output is purely a list of findings. |

### Notes

The captured output is a competent ad-hoc code review that catches the SQL injection (with good remediation advice), user enumeration, and token-sharing concerns. However it falls well short of the structured review format the rubric expects: no score table, no formal verdict, no confidence levels, no adversarial analysis, no positive observations section. Two of the three primary issues in the scenario (N+1 query, rate limiting) are completely missed. Several secondary security concerns — plaintext token storage, synchronous email, unconditional ORM lookup, token expiry as a standalone finding — are either absent or only glancingly touched. The output reads like a helpful developer comment rather than a formal security-aware code review.
