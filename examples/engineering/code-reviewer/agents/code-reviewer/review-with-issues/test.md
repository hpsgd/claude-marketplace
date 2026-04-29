# Test: review with issues

Scenario: A developer asks the code reviewer agent to review a Python Django view that handles user password reset. The code contains a SQL injection risk, an N+1 query, and missing rate limiting on the endpoint.

## Prompt

Can you review this code? It's the password reset handler in our Django app.

```python
# views.py
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db import connection
import secrets

def request_password_reset(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    email = request.POST.get('email', '')

    # Find user by email
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT id, username FROM auth_user WHERE email = '{email}'")
        row = cursor.fetchone()

    if not row:
        return JsonResponse({'error': 'Email not found'}, status=404)

    user_id, username = row
    token = secrets.token_urlsafe(32)

    # Save token and send to all user's linked accounts
    user = User.objects.get(id=user_id)
    for profile in user.linkedprofile_set.all():
        profile.reset_token = token
        profile.save()
        # Send email for each linked account
        send_reset_email(profile.email, token)

    return JsonResponse({'message': 'Reset email sent'})
```

## Criteria

- [ ] PASS: Agent identifies the SQL injection vulnerability (f-string interpolation into the raw SQL query) as a blocker with specific file:line reference
- [ ] PASS: Agent identifies the N+1 query in the loop over linkedprofile_set as a performance finding, with a specific fix (select_related or prefetch_related)
- [ ] PASS: Agent flags the missing rate limiting on the password reset endpoint as a security finding
- [ ] PASS: Agent produces a quality score table covering at least Security, Correctness, Performance, and Maintainability dimensions
- [ ] PASS: Agent gives a verdict of REQUEST CHANGES or BLOCK (not APPROVE) given the SQL injection blocker
- [ ] PASS: Agent runs adversarial analysis — considers what happens if the endpoint is called 1000 times in rapid succession
- [ ] PARTIAL: Agent notes that the 404 response on unknown email leaks account existence information (user enumeration) and recommends returning 200 regardless
- [ ] PASS: Every finding cites a specific location in the code and includes a concrete suggested fix

## Output expectations

- [ ] PASS: Output recommends parameterised queries (e.g. `cursor.execute("SELECT ... WHERE email = %s", [email])`) or the Django ORM (`User.objects.filter(email=email).first()`) as the fix for the SQL injection, not just "sanitise input"
- [ ] PASS: Output assigns confidence levels (HIGH / MODERATE / LOW or numeric 0-100) to individual findings, not only an overall confidence
- [ ] PASS: Output's Security score is 0 (or otherwise reflects that a HARD signal hit zero) given the SQL injection, and the overall confidence reflects `min(HARD signals)` rather than averaging the issue away
- [ ] PASS: Output flags the unconditional `User.objects.get(id=user_id)` as a correctness or robustness issue (raises `DoesNotExist` if the row vanishes between the raw query and the ORM lookup, or if `linkedprofile_set` is empty no token is ever persisted to the user)
- [ ] PASS: Output identifies that the same reset token is reused across every linked profile and recommends per-profile token generation (or explains why a single token is acceptable) — a token-handling concern beyond the SQL/N+1/rate-limit trio
- [ ] PARTIAL: Output notes that `reset_token` appears to be stored in plaintext on the profile and recommends hashing the token at rest (storing only a hash, comparing on redemption)
- [ ] PARTIAL: Output flags the absence of a token expiry / time-to-live on the reset token as a security concern
- [ ] PARTIAL: Output calls out that emails are sent synchronously inside the request handler (blocking the response, no retry) and suggests offloading to a background task or queue
- [ ] PARTIAL: Output includes a "Positive Observations" or "Questions for the Author" section consistent with the agent's defined output format, not only findings
