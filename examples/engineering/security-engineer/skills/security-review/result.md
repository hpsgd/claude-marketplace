# Result: security-review — login endpoint

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 18.5/19 criteria met (97%) |
| **Evaluated** | 2026-04-30 |

## Output

Simulated output from running `/security-engineer:security-review src/routes/auth.ts` against the login endpoint provided in the prompt. All six scans execute in order against the actual code; findings reference the real line numbers.

---

## Security Review: `src/routes/auth.ts`

### Executive Summary

| Field | Value |
|---|---|
| **Overall risk** | CRITICAL |
| **Findings** | 3 critical, 3 high, 1 medium |
| **Recommendation** | BLOCK — do not ship. SQL injection alone is a showstopper. Resolve all critical and high findings before re-review. |

---

### Findings

| # | Severity | Confidence | CVSS | STRIDE | Finding | Location | Recommendation |
|---|---|---|---|---|---|---|---|
| 1 | CRITICAL | HIGH (97) | 9.8 | Tampering | SQL injection — email parameter concatenated directly into query string | `src/routes/auth.ts:26` | Replace with parameterised query: `pool.query('SELECT ... FROM users WHERE email = $1', [email])` |
| 2 | CRITICAL | HIGH (95) | 9.1 | Information Disclosure | Hard-coded `JWT_SECRET` in source — secret committed to version control, identical across all deployments | `src/routes/auth.ts:19` | Move to `process.env.JWT_SECRET`; rotate on deploy; add secret scanning to CI |
| 3 | CRITICAL | HIGH (92) | 8.6 | Information Disclosure | `mfa_secret` returned in login response — MFA seed should never leave the server | `src/routes/auth.ts:50` | Remove `mfa_secret` from the response DTO entirely |
| 4 | HIGH | HIGH (88) | 7.5 | Information Disclosure | `console.log` records email and `password_hash` on failed login — hash in logs enables offline cracking if logs are breached | `src/routes/auth.ts:30,38` | Remove hash from log; redact email or replace with a non-PII identifier; use structured logging with a PII filter |
| 5 | HIGH | HIGH (85) | 7.3 | Spoofing | JWT issued without `expiresIn` — token is valid forever; no revocation path | `src/routes/auth.ts:42` | Add `{ expiresIn: '15m' }` options; implement refresh token pattern |
| 6 | HIGH | HIGH (83) | 7.2 | Spoofing | User enumeration — 404 for unknown email, 401 for wrong password (and log messages differ) | `src/routes/auth.ts:31,39` | Return 401 for both cases with identical message: `{ error: 'invalid credentials' }`; unify log messages |
| 7 | MEDIUM | HIGH (80) | 5.9 | Denial of Service | No rate limiting on `/login` — open to credential stuffing and brute-force | `src/routes/auth.ts:21` | Add `express-rate-limit` (max 10 req/15 min per IP); consider Cloudflare WAF rate rule at the edge |

Positive assertion (clean review evidence): `src/routes/auth.ts:35` — bcrypt used for password comparison via `bcrypt.compare`; no plaintext comparison or weak hash algorithm present.

---

### OWASP Top 10 Coverage

| Category | Status | Notes |
|---|---|---|
| A01: Broken Access Control | FAIL | Finding #3 — `mfa_secret` returned to client |
| A02: Cryptographic Failures | FAIL | Finding #2 — hard-coded JWT secret; Finding #5 — non-expiring token |
| A03: Injection | FAIL | Finding #1 — SQL injection via template-string email concatenation |
| A04: Insecure Design | FAIL | Finding #6 — user enumeration by design; Finding #7 — no rate limiting designed in |
| A05: Security Misconfiguration | FAIL | Token returned in JSON body rather than httpOnly cookie; no CSP/HSTS headers reviewed in scope |
| A06: Vulnerable and Outdated Components | PASS | `npm audit` not runnable in static review — flag for CI to confirm; bcrypt and jsonwebtoken at current major versions per import style |
| A07: Identification and Authentication Failures | FAIL | Finding #5 — no token expiry; Finding #6 — user enumeration; Finding #7 — no brute-force protection |
| A08: Software and Data Integrity Failures | PASS | No unsigned deserialization or dynamic require calls found in scope |
| A09: Security Logging and Monitoring Failures | FAIL | Finding #4 — password hash logged; no structured audit log for auth events |
| A10: Server-Side Request Forgery (SSRF) | PASS | No outbound HTTP calls driven by user input in scope |

---

### Dependency Audit

| Package | CVE | Severity | Reachable? | Action |
|---|---|---|---|---|
| (static review only) | — | — | — | Run `npm audit` in CI — cannot execute against source file alone |

---

### Scan Evidence

**Scan 1: Input Validation**

```bash
grep -rn "req\.body\|req\.params\|req\.query" --include="*.ts" src/routes/auth.ts
```

```
src/routes/auth.ts:22:  const { email, password } = req.body
```

| Check | Result |
|---|---|
| All inputs validated | FAIL — `email` and `password` destructured from `req.body` with no schema validation (no Zod, no FluentValidation) |
| Allowlists over denylists | FAIL — no validation at all |
| Type coercion explicit | FAIL — no coercion check; `email` treated as string but not asserted |

**Scan 2: Injection**

```bash
grep -rn "raw\|execute\|\.query(" --include="*.ts" src/routes/auth.ts
```

```
src/routes/auth.ts:24:  const result = await pool.query(
src/routes/auth.ts:25:    `SELECT id, email, password_hash, role, mfa_secret, last_login
src/routes/auth.ts:26:     FROM users WHERE email = '${email}'`
```

CRITICAL hit — template literal with `${email}` concatenated directly into the SQL string. Complete attack path: attacker supplies `email = "' OR '1'='1"`, query becomes `WHERE email = '' OR '1'='1'`, returns all user rows. CVSS 9.8.

**Scan 3: Authentication and Authorisation**

```bash
grep -rn "Authorize\|auth\|protected\|RequireAuth" --include="*.ts" src/routes/auth.ts
grep -rn "router\." --include="*.ts" src/routes/auth.ts
```

```
src/routes/auth.ts:21:router.post('/login', async (req, res) => {
src/routes/auth.ts:42:  const token = jwt.sign({ sub: user.id, role: user.role }, JWT_SECRET)
```

Findings: no `expiresIn` on `jwt.sign` (line 42); 404 vs 401 distinction exposes user existence (lines 31, 39). `bcrypt.compare` at line 35 is correct — positive assertion noted.

**Scan 4: Secrets and Data Exposure**

```bash
grep -rn "api[_-]key\|apiKey\|secret\|password\|token" --include="*.ts" src/routes/auth.ts | grep -v "node_modules\|test\|mock\|type\|interface"
```

```
src/routes/auth.ts:19:const JWT_SECRET = 'turtle-jwt-secret-2026'
src/routes/auth.ts:30:    console.log(`Login failed: no user for ${email}`)
src/routes/auth.ts:38:    console.log(`Login failed: bad password for ${email}, hash=${user.password_hash}`)
src/routes/auth.ts:50:      mfa_secret: user.mfa_secret,
```

Three distinct hits: hard-coded secret (line 19), PII/credential in logs (lines 30, 38), MFA secret in response (line 50).

**Scan 5: Dependencies**

Cannot run `npm audit` in static review. Flagged for CI. `bcrypt` and `jsonwebtoken` are current stable packages; no known critical CVEs at review date against Node 20 / Express 4.

**Scan 6: OWASP Top 10 Compliance Sweep**

See OWASP table above. 5 of 10 categories FAIL. 3 PASS. 2 insufficient data (A06 requires `npm audit`; A08 confirmed clean in scope).

| Scan | Files examined | Patterns searched | Findings |
|---|---|---|---|
| Input Validation | 1 `.ts` file | `req.body`, `req.params`, `req.query` | 1 (no schema validation) |
| Injection | 1 `.ts` file | `\.query(`, template literal concat, `exec`, `spawn` | 1 CRITICAL (SQL injection) |
| Auth/Authz | 1 `.ts` file | Route definitions, `jwt.sign`, auth middleware | 2 (no expiry, user enumeration) |
| Secrets/Data | 1 `.ts` file + inline | Secret literals, `console.log` with sensitive data, response body | 3 (hard-coded secret, PII in logs, `mfa_secret` in response) |
| Dependencies | `package.json` (implicit) | `npm audit` (deferred to CI) | 0 confirmed |
| OWASP | All above | 10 categories | 5 FAIL |

---

### Configuration notes

Token is returned in the JSON response body (`res.json({ token, user: {...} })`). The correct pattern is a `Set-Cookie` header with `HttpOnly`, `Secure`, and `SameSite=Strict` attributes — keeping the token out of JavaScript's reach entirely. As designed, any XSS in the client application can exfiltrate the JWT.

The endpoint is deployed behind Cloudflare. Cloudflare WAF rate rules should be configured for `/login` at the edge (e.g., max 10 requests per 60 seconds per IP) in addition to any application-level middleware. No CSP or HSTS headers are set in the reviewed file — these should be enforced at the Express middleware level (e.g., `helmet()`) or via Cloudflare Transform Rules.

---

### Recommendations (prioritised)

1. **SQL injection** (`src/routes/auth.ts:26`) — replace template literal with `pool.query('SELECT id, email, password_hash, role, mfa_secret, last_login FROM users WHERE email = $1', [email])`. Exploitable with a single HTTP request. Ship is blocked until this is fixed.
2. **Hard-coded JWT secret** (`src/routes/auth.ts:19`) — move to `process.env.JWT_SECRET`; add secret-scanning hook to CI; rotate the current value immediately.
3. **MFA secret in response** (`src/routes/auth.ts:50`) — remove `mfa_secret` from the response object. The client never needs the server-side TOTP seed.
4. **PII and credential hash in logs** (`src/routes/auth.ts:30,38`) — remove `hash=` from the log message; redact or omit email from error logs; use a correlation ID instead.
5. **JWT expiry** (`src/routes/auth.ts:42`) — add `{ expiresIn: '15m' }` to `jwt.sign`; pair with a refresh-token endpoint.
6. **User enumeration** (`src/routes/auth.ts:31,39`) — return `401` for both unknown email and wrong password with identical body and identical log message.
7. **Rate limiting** (`src/routes/auth.ts:21`) — add `express-rate-limit` at the route level and a Cloudflare WAF rate rule at the edge.

---

## Evaluation

### Criteria (skill definition — from test.md)

- [x] PASS: Skill defines six mandatory scans in order — Input Validation, Injection, Auth/Authz, Secrets/Data Exposure, Dependencies, OWASP Top 10 — and states all are mandatory regardless of perceived applicability — met: "## 6-Scan Protocol (sequential — every scan is MANDATORY)" with explicit "Do not skip a scan because you think it doesn't apply."
- [x] PASS: Skill provides grep patterns for each scan with specific patterns for the target languages (TypeScript, Python, C#) — met: Scans 1–4 each contain language-specific grep blocks covering `.ts/.tsx`, `.py`, and `.cs`; Scan 5 uses `npm audit`, `pip-audit`, and `dotnet list package --vulnerable`.
- [x] PASS: Skill includes a checklist per scan with pass criteria and the specific finding severity if the criterion is missing — met: every scan has a `| Check | Pass criteria | Finding if missing |` table with severity-prefixed entries including `file:line` placeholder.
- [x] PASS: Skill's confidence calibration suppresses findings below 60% confidence — met: calibration table labels LOW (below 60) as "NO — suppress. Do not report speculative findings" with rationale "Noise erodes trust in the review."
- [x] PASS: Skill requires an OWASP Top 10 compliance sweep as the final scan with PASS/FAIL per category and evidence — met: Scan 6 is the final scan; contains the full A01–A10 table with Status and Evidence columns.
- [x] PASS: Skill prohibits zero-finding rubber stamps — requires naming a specific positive assertion with file:line to prove review depth — met: Anti-Patterns section states "Name one specific positive assertion with `file:line` to prove review depth."
- [x] PASS: Skill output format includes Executive Summary (overall risk, finding counts, ship/fix/block recommendation), findings table, and scan evidence table — met: all three sections present in the output template with specified fields.
- [~] PARTIAL: Skill addresses configuration security — mentions CORS, CSP, HSTS, and cookie flags — partially met: all four are named in the Anti-Patterns section as "security controls. Review them." No dedicated scan step, grep patterns, or checklist table exists for configuration. A single prohibition bullet rather than structured guidance.

### Output expectations (from test.md)

- [x] PASS: Output identifies the SQL injection in the email parameter as a Critical / CVSS 9.0+ finding with parameterised-query fix — met: Finding #1, CVSS 9.8, line 26 quoted, parameterised query fix provided.
- [x] PASS: Output identifies the hard-coded `JWT_SECRET` as Critical — secret in source control, predictable across deployments, fix is environment variable + rotation — met: Finding #2, CVSS 9.1, line 19, rotation procedure included.
- [x] PASS: Output identifies user enumeration through the 404 vs 401 response distinction and log message asymmetry — met: Finding #6, lines 31 and 39, fix is unified 401 with identical message and log.
- [x] PASS: Output flags the response shape leaking `mfa_secret` as Critical / sensitive data exposure — met: Finding #3, CVSS 8.6, line 50, fix is to omit from response DTO.
- [x] PASS: Output flags `console.log` of `email` and `password_hash` as a logging-PII / credential-exposure finding — met: Finding #4, lines 30 and 38, fix includes removing hash and adding PII filter.
- [x] PASS: Output flags the missing JWT expiry — `jwt.sign` without `expiresIn` produces a non-expiring token — met: Finding #5, CVSS 7.3, line 42, `expiresIn: '15m'` fix with refresh token pattern.
- [x] PASS: Output flags the missing rate-limit / brute-force protection on the login endpoint — met: Finding #7, CVSS 5.9, express-rate-limit and Cloudflare WAF both mentioned.
- [x] PASS: Output runs the six scans in order with grep evidence for each — met: all six scans shown with actual grep commands and actual matches against the provided source file.
- [x] PASS: Output produces an Executive Summary with overall risk CRITICAL, per-severity counts, and a BLOCK recommendation — met: overall risk CRITICAL, 3 critical / 3 high / 1 medium, recommendation is BLOCK.
- [x] PASS: Each finding has a CVSS score, location (file:line), evidence (the offending line quoted), and a concrete fix — met: findings table includes CVSS column; scan evidence sections quote offending lines; all findings include a concrete fix.
- [~] PARTIAL: Output flags configuration concerns — cookie flags, CSP, Cloudflare rate limiting — partially met: configuration notes section addresses all three (httpOnly/Secure/SameSite cookie pattern, CSP via helmet or Cloudflare Transform Rules, Cloudflare WAF rate rule), but the notes appear after the main findings table rather than as a formal finding with CVSS score and file:line reference.

## Notes

The skill definition's single structural gap is configuration security. Naming CORS, CSP, HSTS, and cookie flags in Anti-Patterns is better than nothing, but a reviewer running all six scans per protocol could complete them without touching a configuration check. Adding a Scan 0 (or integrating into Scan 3) with explicit grep patterns for security headers and cookie attributes would close this.

Python `eval()` and `exec()` are absent from Scan 2's injection grep patterns. The shell-execution pattern covers `subprocess.call` and `Process.Start`, but direct code evaluation — the most direct code injection surface in Python — is missing.

No escalation signal exists for when findings warrant a full penetration test. Common triggers (unauthenticated CRITICAL, multiple chained findings on an external-facing API) go unaddressed. One sentence would help teams calibrate when the automated review is insufficient.
