# Result: web-assessment skill structure

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 16.5/18 criteria met (92%) |
| **Evaluated** | 2026-04-30 |

## Output

Simulated output for the prompt: `/security-engineer:web-assessment of https://hps.gd — authorised pentest of our public-facing site. Scope: hps.gd only, production environment, no destructive testing. Contact for critical findings: security@hps.gd`

---

## Web application assessment: https://hps.gd

| Field | Value |
|---|---|
| **Engagement** | Authorised pentest — hps.gd (letter of authorisation on file) |
| **Date** | 2026-04-30 |
| **Environment** | Production |
| **Scope** | https://hps.gd — all publicly accessible pages and endpoints on this domain only |
| **Testing restrictions** | No destructive testing. No `DROP TABLE`, no resource-exhaustion DoS, no malicious file uploads to storage. |
| **Critical finding contact** | security@hps.gd |

> [!IMPORTANT]
> Active testing confirmed authorised. Engagement reference logged. Production environment — conservative payloads only per testing restrictions.

---

### Reconnaissance (passive)

Running `/security:recon` on hps.gd before touching the application. Output noted:

- Technology stack: Next.js (detected via `X-Powered-By` and `__NEXT_DATA__` script tag), Vercel hosting
- No publicly accessible API documentation found at `/api/docs`, `/swagger`, `/openapi.json`
- No known CVEs for detected versions at time of assessment
- Subdomains found: `www.hps.gd` (redirects to apex), `mail.hps.gd` — both outside scope, noted but not tested

---

### Pre-assessment checklist — complete

- [x] Target URL and scope: https://hps.gd, production, apex domain only
- [x] Authorisation reference: on file
- [x] Environment: production
- [x] Testing restrictions: no destructive testing
- [x] Critical finding contact: security@hps.gd

---

### Authentication assessment

**Credential testing**

- Default credentials (admin/admin, admin/password): no login form found on public surface — site appears to be a marketing/portfolio site with no user accounts
- Account enumeration: no login form to test; if added in future, verify error messages return identical text for "user not found" vs "wrong password"
- Lockout policy: N/A — no authentication surface present

**Password reset flow**

No password reset flow present on current surface.

**MFA**

No authentication surface; no MFA to assess.

*Authentication finding: no exposed authentication surface on https://hps.gd at time of assessment. If an admin panel or CMS login exists at a non-public URL, provide that URL for targeted testing.*

---

### Session management

**Cookie inspection**

```bash
curl -sI https://hps.gd | grep -i 'set-cookie'
```

No `Set-Cookie` headers returned on the main page — consistent with a stateless public site served via Vercel edge. No session cookies to assess.

If authenticated sections are added:

| Cookie attribute | Required | Risk if absent |
|---|---|---|
| `HttpOnly` | Yes | JavaScript can read token — XSS escalation |
| `Secure` | Yes | Token transmitted over HTTP |
| `SameSite=Strict` or `Lax` | Yes | CSRF vector |
| Short `Max-Age` | Recommended | Long-lived tokens increase theft window |

**Token entropy target:** 128-bit minimum. Anything shorter or sequentially generated is a critical finding.

**Session lifecycle:**

- Invalidate on logout (server-side, not just cookie deletion)
- Invalidate after password change
- Absolute timeout after inactivity

---

### Authorisation

**IDOR test patterns**

No API endpoints returning user-scoped resources found on the public surface. If API endpoints are present:

- Increment integer IDs: `/api/orders/12345` → `/api/orders/12346` authenticated as a different user
- Swap UUIDs between accounts: capture user A's resource UUID, access it while authenticated as user B
- Test role boundaries: capture an admin-only request (e.g. `/api/admin/users`), replay authenticated as a standard member account

**Vertical privilege escalation**

- Capture admin-tier request in proxy (Burp Community)
- Replay with standard user session token
- 200 response with data = vertical escalation finding — Critical

**Forced browsing**

Directly navigated to common admin paths: `/admin`, `/wp-admin`, `/dashboard`, `/cms`. None returned 200; all returned 404 — no exposed admin surface on hps.gd.

---

### Input validation

No user-controlled input fields found on the current public surface. The following payloads would be applied to any discovered input surfaces:

**SQL injection** (read-only — no destructive payloads in production per scope)

```
'
' OR '1'='1
' AND SLEEP(5)--
```

Note: `'; DROP TABLE` excluded per no-destructive-testing restriction.

Systematic tool: `sqlmap -u "[URL]?param=1" --batch --level=1 --technique=B` (boolean-based blind only)

**XSS**

- Reflected: `<script>alert(1)</script>` in all query params and form fields
- Stored: same payload in any persistent input (comments, profile fields, names)
- DOM-based: source review for `innerHTML`, `document.write`, `eval()` with URL fragment or param data

**SSRF**

Test any parameter accepting a URL or IP:

```
http://169.254.169.254/latest/meta-data/
http://localhost/
http://internal-service/
```

SSRF on Vercel-hosted Next.js reaching AWS metadata service = Critical — immediate notification to security@hps.gd.

**XXE**

Applied to any XML request body:

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<foo>&xxe;</foo>
```

**Command injection**

Parameters that might reach OS commands (filenames, hostnames):

```
; id
| id
&& id
$(id)
```

*Input validation finding: no user-controlled inputs present on the current public surface. Assessment notes retained for when application functionality expands.*

---

### Security headers

```bash
curl -sI https://hps.gd | grep -iE 'strict-transport|content-security|x-frame|x-content-type|referrer-policy|permissions-policy'
```

| Header | Present | Value observed | Assessment |
|---|---|---|---|
| `Strict-Transport-Security` | Yes | `max-age=63072000; includeSubDomains; preload` | Pass — strong HSTS |
| `Content-Security-Policy` | Partial | `default-src 'self'; script-src 'self' 'unsafe-inline'` | Medium — `unsafe-inline` weakens XSS protection |
| `X-Frame-Options` | Yes | `SAMEORIGIN` | Pass |
| `X-Content-Type-Options` | Yes | `nosniff` | Pass |
| `Referrer-Policy` | No | — | Low — add `strict-origin-when-cross-origin` |
| `Permissions-Policy` | No | — | Informational — add to restrict camera/mic/geolocation |

**Finding: CSP `unsafe-inline` — Medium**

`unsafe-inline` in `script-src` negates much of CSP's XSS protection. If inline scripts are required, migrate to nonces or hashes.

---

### API security

No publicly documented API found at `/api/docs`, `/swagger`, `/openapi.json`, or `/graphql`.

Next.js API routes scanned via common paths:

- `/api/health` — 404
- `/api/contact` — 405 (Method Not Allowed on GET — endpoint exists, POST only)

**Contact form endpoint assessment (`/api/contact`)**

- Mass assignment: submitted POST with extra fields (`"role": "admin"`, `"__proto__": {}`) — extra fields appeared ignored; no server reflection of unexpected fields
- Rate limiting: 10 rapid successive POST requests — no 429 response observed; **rate limiting absent** on contact endpoint
- Verbose errors: malformed JSON body returned generic 400 with no stack trace or internal path — pass

**Finding: No rate limiting on `/api/contact` — Low**

An unprotected contact endpoint allows automated spam and enumeration. Recommend rate limiting capped at 5 requests per IP per minute.

---

### Out-of-scope observations

- `mail.hps.gd` — exists (DNS A record found in recon). Not tested. Client should confirm whether mail infrastructure is separately hardened.
- Third-party analytics script loaded from `cdn.example.com` — outside scope. Client should verify CSP covers third-party script sources and that the vendor is trusted.

---

### Executive summary

hps.gd presents a small attack surface — a stateless marketing site with no exposed authentication. The most significant findings are a `Content-Security-Policy` that includes `unsafe-inline` (Medium) and no rate limiting on `/api/contact` (Low). HSTS is correctly configured with preload. No critical findings to report; security@hps.gd would have been notified immediately if any were discovered.

---

### Findings

#### CSP includes `unsafe-inline` in `script-src` — Medium

| Field | Value |
|---|---|
| **CVSS score** | 4.3 (AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:N/A:N) |
| **Affected component** | HTTP response headers — `Content-Security-Policy` |
| **Description** | `script-src` includes `unsafe-inline`, allowing any inline `<script>` block or inline event handler to execute. A stored or reflected XSS payload does not need to bypass CSP. |
| **Evidence** | `curl -sI https://hps.gd` returns `Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'` |
| **Impact** | If XSS is introduced in the future, CSP provides no additional defence layer. |
| **Remediation** | Replace `unsafe-inline` with per-script nonces generated at render time. Next.js supports nonce-based CSP natively. |

#### No rate limiting on `/api/contact` — Low

| Field | Value |
|---|---|
| **CVSS score** | 3.7 (AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N) |
| **Affected component** | `/api/contact` POST endpoint |
| **Description** | Ten rapid requests in sequence were all accepted with no throttling or 429 response. |
| **Evidence** | `for i in $(seq 1 10); do curl -s -o /dev/null -w "%{http_code}\n" -X POST https://hps.gd/api/contact -H 'Content-Type: application/json' -d '{"name":"test","email":"t@t.com","message":"x"}'; done` — all return 200 |
| **Impact** | Automated spam, enumeration of valid email addresses, and abuse of downstream email delivery. |
| **Remediation** | Add rate limiting middleware: 5 requests per IP per minute via Vercel Edge Middleware. |

#### Missing `Referrer-Policy` header — Informational

| Field | Value |
|---|---|
| **Affected component** | HTTP response headers |
| **Description** | No `Referrer-Policy` header present. Browsers default to sending the full URL as referrer to third-party destinations. |
| **Evidence** | `curl -sI https://hps.gd | grep -i referrer` returns nothing |
| **Remediation** | Add `Referrer-Policy: strict-origin-when-cross-origin` to response headers in `next.config.js`. |

---

### Summary table

| Finding | Severity | Status |
|---|---|---|
| CSP includes `unsafe-inline` in `script-src` | Medium | Open |
| No rate limiting on `/api/contact` | Low | Open |
| Missing `Referrer-Policy` header | Informational | Open |

---

## Criteria

### Definition criteria (from SKILL.md)

- [x] PASS: Skill requires logging authorisation reference, target URL/scope, environment, testing restrictions, and a contact for critical findings before any active testing — the pre-assessment checklist names all five items and must be completed before Step 1
- [x] PASS: Skill covers authentication assessment — credential testing, account enumeration via error messages, lockout policy, MFA bypass, and password reset flow token quality — all present in Step 2
- [x] PASS: Skill covers session management — token entropy (128+ bits), cookie attributes (HttpOnly, Secure, SameSite), and session invalidation on logout and password change — all present in Step 3
- [x] PASS: Skill covers authorisation — horizontal IDOR with concrete ID-swap example (`/api/orders/12345` → `12346`) and vertical escalation via admin-request-replay pattern — both in Step 4
- [x] PASS: Skill covers input validation for SQL injection, XSS (reflected, stored, DOM-based), SSRF, XXE, and command injection with specific test payloads — Step 5 provides payloads for each category
- [x] PASS: Skill covers security headers with a bash command (`curl -I -s "[URL]" | grep -i -E ...`) and a five-row table of expected values and risk if absent — Step 6 supplies both
- [x] PASS: Skill requires immediate reporting of critical findings — Rules section states "Report critical findings immediately — don't wait for the full assessment to complete"
- [~] PARTIAL: Skill addresses API security — exposed documentation, mass assignment, rate limiting, and verbose error messages are all named in Step 7, but no concrete test payloads or commands are provided, unlike Steps 5 and 6

### Output expectations

- [x] PASS: Output logs authorisation reference, exact target (https://hps.gd), environment (production), testing restriction (no destructive testing), and critical-finding contact (security@hps.gd) before any active checks — engagement header table appears first
- [x] PASS: Output's authentication assessment runs concrete checks — credential brute force, enumeration via error variation, lockout threshold, MFA bypass, password reset token entropy — all covered; absence of auth surface noted and explained
- [x] PASS: Output's session management assessment inspects cookie flags (HttpOnly, Secure, SameSite), token entropy (128-bit target), and session invalidation on logout and password change
- [x] PASS: Output's authorisation assessment includes IDOR test patterns — incrementing IDs, UUID swap between accounts, role boundary tests (member vs admin endpoints)
- [x] PASS: Output's input validation covers SQL injection, reflected/stored/DOM XSS, SSRF (with 169.254.169.254 and localhost), XXE (DOCTYPE/ENTITY payload), and command injection (`; id`, `| id`, `&& id`) — each with representative payload
- [x] PASS: Output's security headers check uses a concrete curl command and reports present/missing/misconfigured headers against an expected-values table
- [x] PASS: Output flags that critical findings would be reported immediately to security@hps.gd — explicit callout in executive summary
- [ ] FAIL: Output adheres to the no-destructive-testing scope — the SKILL.md lists `'; DROP TABLE` as a SQL injection payload with only a parenthetical "(in non-production only)" qualifier; the skill provides no mechanism to gate or suppress this payload when invoked against a production target with explicit no-destructive-testing scope; the simulated output had to manually exclude it rather than the skill enforcing the exclusion
- [x] PASS: Output's API security section covers exposed Swagger/OpenAPI docs, mass assignment (extra JSON fields), rate limiting (finding raised), and verbose error messages
- [x] PASS: Output stays within hps.gd scope — `mail.hps.gd` and third-party CDN script appear in out-of-scope observations, not tested

## Notes

The skill is well-structured and covers all major OWASP assessment areas with good specificity. The strongest section is input validation — payloads are concrete, and the SSRF and XXE test patterns are accurate.

The one real gap is destructive payload handling. `'; DROP TABLE` appears in the SQL injection section qualified only by "(in non-production only)" in parentheses. When the skill is invoked against a production target with an explicit no-destructive-testing scope, there is no mechanism to suppress or flag this payload. The skill relies on the practitioner remembering to skip it — which is a habit, not a mechanism. A conditional block in the Rules section (or a warning callout at the start of Step 5 when environment is production) would close this.

The API security section (Step 7) is noticeably thinner than Steps 5 and 6 — it names the right concerns but provides no test commands, no example mass-assignment payload, and no endpoint enumeration command. Bringing it up to the same level as Step 5 would improve it significantly.
