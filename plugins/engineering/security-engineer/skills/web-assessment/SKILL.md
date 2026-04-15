---
name: web-assessment
description: "Structured web application security assessment following OWASP methodology. Covers authentication, authorisation, input validation, session management, API security, and security headers. Use during penetration testing or security reviews of web applications."
argument-hint: "[target application URL] for [engagement name or authorisation reference]"
user-invocable: true
allowed-tools: Bash, WebFetch
---

Conduct a structured web application security assessment of $ARGUMENTS.

> [!IMPORTANT]
> This skill requires explicit written authorisation for the target application. Active testing sends requests to the target — this is not passive. Confirm the Rules of Engagement before running any active checks. Never test production systems without written authorisation that explicitly includes production.

## Pre-assessment checklist

Log before starting:

- **Target URL and scope:** which URLs, endpoints, and functionality are in scope
- **Authorisation reference:** engagement name, SOW reference, or letter of authorisation
- **Environment:** production / staging / dedicated test environment
- **Testing restrictions:** any specific tests or hours excluded
- **Contact:** who to notify if a critical finding is discovered mid-assessment

## Step 1: Reconnaissance (passive)

Before active testing, run `/security:recon` for passive domain and technology intelligence. This establishes what you're dealing with before touching the application.

From the recon output, note:
- Framework and CMS (shapes which tests are highest priority)
- Known CVEs for detected technology versions
- API documentation if publicly available

## Step 2: Authentication assessment

Test the authentication implementation:

**Credential testing:**
- Default credentials for the identified platform
- Account enumeration via login error messages (do they differ for "user doesn't exist" vs "wrong password"?)
- Lockout policy: how many attempts before lockout, and is it bypassable?

**Password policy:**
- Minimum length and complexity requirements
- Is the policy enforced server-side?
- Are weak passwords accepted?

**MFA:**
- Is MFA available? Is it enforced for privileged accounts?
- Is the MFA implementation bypassable (TOTP without replay protection, SMS-based with SIM swap exposure)?

**Password reset flow:**
- Is the reset token sufficiently random and short-lived?
- Is the token single-use?
- Are there predictable reset questions?

## Step 3: Session management

**Session token quality:**
- Token length (should be 128+ bits of entropy)
- Token randomness — predictable tokens indicate a systemic vulnerability
- Token location: cookie vs URL parameter (URL tokens appear in logs and referrer headers)

**Cookie attributes:**
- `HttpOnly` — prevents JavaScript access
- `Secure` — HTTPS only
- `SameSite` — CSRF mitigation
- Appropriate expiry

**Session lifecycle:**
- Is the session invalidated on logout?
- Is the session invalidated after password change?
- Is there an absolute timeout?

## Step 4: Authorisation

**Horizontal privilege escalation:**
Test whether user A can access user B's resources by modifying object IDs (IDOR — Insecure Direct Object Reference).

Common pattern: change `/api/orders/12345` to `/api/orders/12346` while authenticated as a different user. Access to another user's data = IDOR.

**Vertical privilege escalation:**
Test whether a low-privilege user can access admin or elevated functions.

Common pattern: capture an admin request in proxy, replay it authenticated as a standard user.

**Forced browsing:**
Directly access URLs that are not linked from the authenticated UI. Are they protected by authentication checks or only hidden by obscurity?

## Step 5: Input validation

Focus on the OWASP Top 10 injection categories:

**SQL injection:**
- Test user-controlled input that reaches database queries
- Payloads: single quote `'`, `' OR '1'='1`, `'; DROP TABLE` (in non-production only)
- Use `sqlmap` in safe mode for systematic testing: `sqlmap -u "[URL]" --forms --batch --level=1`

**XSS (Cross-Site Scripting):**
- Reflected: does user input appear in the response unescaped?
- Stored: does user input persist and render in other users' sessions?
- Basic payload: `<script>alert(1)</script>` — if this executes, it's XSS
- DOM-based: look for `innerHTML`, `document.write`, `eval()` with user-controlled data

**SSRF (Server-Side Request Forgery):**
- Look for parameters that take URLs or IP addresses as input
- Test: `http://169.254.169.254/latest/meta-data/` (AWS metadata), `http://localhost/`, internal hostnames
- SSRF in cloud environments can lead to credential exfiltration from metadata services

**XXE (XML External Entity):**
- Applies wherever the application processes XML
- Test payload in XML body: `<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>`

**Command injection:**
- Parameters that might reach OS commands: filenames, IP addresses, hostnames
- Payloads: `; id`, `| id`, `&& id`

## Step 6: Security headers

Check HTTP response headers on the application's main page and authenticated sections:

```bash
curl -I -s "[URL]" | grep -i -E "strict-transport|content-security|x-frame|x-content-type|referrer-policy|permissions-policy"
```

| Header | Expected value | Risk if absent |
|---|---|---|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` | Downgrade attack |
| `Content-Security-Policy` | Restrictive policy | XSS escalation |
| `X-Frame-Options` | `DENY` or `SAMEORIGIN` | Clickjacking |
| `X-Content-Type-Options` | `nosniff` | MIME sniffing |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Data leakage in referrer |

## Step 7: API security

If the application has an API:

- Is API documentation publicly exposed? (`/api/docs`, `/swagger`, `/openapi.json`)
- Are API endpoints subject to the same authentication and authorisation controls as the web UI?
- Mass assignment: does the API accept and process unexpected fields in JSON payloads?
- Rate limiting: are API endpoints rate-limited against brute force and enumeration?
- Are verbose error messages returned that reveal stack traces, internal paths, or database schema?

## Rules

- Written authorisation before any active testing. No exceptions.
- Test destructive payloads (DROP TABLE, format strings) only in non-production environments.
- Report critical findings immediately — don't wait for the full assessment to complete.
- Scope discipline: if you find a vulnerability that leads outside the agreed scope, note it and ask before following up.
- Tooling: use standard tools (sqlmap, Burp Community) with conservative settings. Don't write custom exploits for this skill's scope.

## Output format

```markdown
## Web application assessment: [Target]

**Engagement:** [authorisation reference]
**Date:** [today]
**Environment:** [production / staging / test]
**Scope:** [URLs and functionality in scope]

### Executive summary

[2-3 sentences: overall risk posture and the 1-2 most significant findings]

### Findings

#### [Finding title] — [Critical / High / Medium / Low / Informational]

**CVSS score (if applicable):** —
**Affected component:** —
**Description:** [what the vulnerability is]
**Evidence:** [specific request/response or screenshot reference]
**Impact:** [what an attacker could do]
**Remediation:** [specific fix recommendation]

### Security headers

| Header | Present | Value | Assessment |
|---|---|---|---|

### Summary table

| Finding | Severity | Status |
|---|---|---|
| [Finding] | Critical / High / Medium / Low | Open |

### Out-of-scope observations

[Potential issues noticed outside the agreed scope — noted for client awareness, not tested]
```
