# Security Review

Scenario: A backend developer asks for a security review of a new login endpoint in a Node/Express application. The handler queries Postgres directly with string concatenation, returns user records on successful authentication, logs the failed-attempt details, and uses a hard-coded secret for JWT signing. The reviewer needs to apply the six-scan security-review methodology.

## Prompt

> Run a security review on this login endpoint before we ship it.
> 
> ```typescript
> // src/routes/auth.ts
> import { Router } from 'express'
> import { Pool } from 'pg'
> import jwt from 'jsonwebtoken'
> import bcrypt from 'bcrypt'
> 
> const pool = new Pool({ connectionString: process.env.DATABASE_URL })
> const router = Router()
> 
> const JWT_SECRET = 'turtle-jwt-secret-2026'
> 
> router.post('/login', async (req, res) => {
>   const { email, password } = req.body
> 
>   const result = await pool.query(
>     `SELECT id, email, password_hash, role, mfa_secret, last_login
>      FROM users WHERE email = '${email}'`
>   )
> 
>   if (result.rows.length === 0) {
>     console.log(`Login failed: no user for ${email}`)
>     return res.status(404).json({ error: 'user not found' })
>   }
> 
>   const user = result.rows[0]
>   const ok = await bcrypt.compare(password, user.password_hash)
> 
>   if (!ok) {
>     console.log(`Login failed: bad password for ${email}, hash=${user.password_hash}`)
>     return res.status(401).json({ error: 'wrong password' })
>   }
> 
>   const token = jwt.sign({ sub: user.id, role: user.role }, JWT_SECRET)
> 
>   return res.json({
>     token,
>     user: {
>       id: user.id,
>       email: user.email,
>       role: user.role,
>       mfa_secret: user.mfa_secret,
>       last_login: user.last_login,
>     },
>   })
> })
> 
> export default router
> ```
> 
> Stack: Node 20, Express 4, Postgres 15. This will be deployed behind Cloudflare on api.example.com.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Security Review: `src/routes/auth.ts` — Login Endpoint

### Executive Summary

- **Overall risk:** CRITICAL
- **Findings:** 3 critical, 3 high, 3 medium, 1 low
- **Recommendation:** **Block — do not ship.** Three independently exploitable critical vulnerabilities exist. Fix all three before any deployment.

---

### Findings

| # | Severity | Confidence | STRIDE | Finding | Location | Recommendation |
|---|---|---|---|---|---|---|
| 1 | CRITICAL | HIGH (98) | Injection | SQL injection via string-interpolated `email` | `auth.ts:16–19` | Parameterised query |
| 2 | CRITICAL | HIGH (98) | Spoofing | JWT secret hardcoded in source | `auth.ts:11` | `process.env.JWT_SECRET` + rotate |
| 3 | CRITICAL | HIGH (95) | Disclosure | MFA TOTP secret returned in login response | `auth.ts:43` | Remove from response |
| 4 | HIGH | HIGH (92) | Disclosure | bcrypt hash logged on failed login | `auth.ts:28` | Remove `hash=` from log line |
| 5 | HIGH | HIGH (90) | Elevation | JWT issued with no expiry | `auth.ts:31` | Add `expiresIn: '15m'` |
| 6 | HIGH | HIGH (88) | Spoofing | MFA secret fetched but MFA never validated | `auth.ts:13–44` | Enforce TOTP before token issue |
| 7 | MEDIUM | HIGH (85) | Disclosure | User enumeration: 404 vs 401 leaks account existence | `auth.ts:22,29` | Unified 401 for both failures |
| 8 | MEDIUM | HIGH (85) | DoS | No rate limiting on login endpoint | `auth.ts:13` | `express-rate-limit` or CF rule |
| 9 | MEDIUM | HIGH (80) | Disclosure | Email (PII) written to server logs | `auth.ts:22` | Remove or hash in logs |
| 10 | LOW | HIGH (80) | Tampering | No input validation on `email`/`password` | `auth.ts:14` | Zod schema at boundary |

---

### Finding Detail

**#1 — CRITICAL: SQL Injection**

```typescript
// auth.ts:16-19 — email interpolated directly into query string
const result = await pool.query(
  `SELECT id, email, password_hash, role, mfa_secret, last_login
   FROM users WHERE email = '${email}'`  // ← attacker-controlled
)
```

Supplying `' OR '1'='1` as the email bypasses the password check entirely and logs in as the first user in the table (likely an admin). `'; DROP TABLE users; --` destroys the database. No authentication or special access required.

Fix:
```typescript
const result = await pool.query(
  `SELECT id, email, password_hash, role, mfa_secret, last_login
   FROM users WHERE email = $1`,
  [email]
)
```

---

**#2 — CRITICAL: Hardcoded JWT Secret**

```typescript
// auth.ts:11
const JWT_SECRET = 'turtle-jwt-secret-2026'
```

Anyone with read access to the repo (or a leaked copy) can forge a JWT for any user ID with any role: `jwt.sign({ sub: 1, role: 'admin' }, 'turtle-jwt-secret-2026')`. Every token ever issued is permanently compromised once this is seen.

Fix: `const JWT_SECRET = process.env.JWT_SECRET` — fail fast on startup if missing, generate with `openssl rand -base64 32`.

---

**#3 — CRITICAL: MFA Secret Returned to Client**

```typescript
// auth.ts:40-43
user: {
  ...
  mfa_secret: user.mfa_secret,  // ← the raw TOTP seed
  ...
}
```

The TOTP seed should be shown once at setup and never again. Returning it in every login response lets anyone who intercepts a token — via XSS, a compromised client, or log scraping — permanently clone the user's second factor. Remove this field from the response entirely.

---

**#4 — HIGH: Password Hash in Logs**

```typescript
// auth.ts:28
console.log(`Login failed: bad password for ${email}, hash=${user.password_hash}`)
```

bcrypt hashes are offline-crackable. Logging them means anyone with log access (cloud provider, logging SaaS, a future breach) can mount an offline dictionary attack against every failed login.

---

**#5 — HIGH: JWT Has No Expiry**

```typescript
// auth.ts:31
const token = jwt.sign({ sub: user.id, role: user.role }, JWT_SECRET)
// no expiresIn → token is valid forever
```

A stolen token never expires. Fix: `jwt.sign(..., JWT_SECRET, { expiresIn: '15m' })` and issue refresh tokens separately.

---

**#6 — HIGH: MFA Fetched but Not Enforced**

The query selects `mfa_secret` (line 14), which implies MFA is configured for at least some users. The code never checks it — any user with MFA enabled can log in with password alone. This silently degrades a security control.

---

### OWASP Top 10

| Category | Status | Notes |
|---|---|---|
| A01: Broken Access Control | FAIL | MFA bypassed; no role enforcement visible |
| A02: Cryptographic Failures | FAIL | Hardcoded JWT secret (#2); MFA secret exposed (#3) |
| A03: Injection | FAIL | SQL injection (#1) |
| A04: Insecure Design | FAIL | User enumeration (#7); MFA not enforced (#6) |
| A05: Security Misconfiguration | FAIL | Hardcoded secret, no token expiry |
| A06: Vulnerable Components | UNKNOWN | No `package.json` provided — run `npm audit` |
| A07: Auth Failures | FAIL | No expiry (#5), no rate limit (#8), user enum (#7), MFA bypass (#6) |
| A08: Data Integrity Failures | PASS | bcrypt used correctly |
| A09: Logging/Monitoring | FAIL | Hash logged (#4), PII in logs (#9) |
| A10: SSRF | PASS | No SSRF vectors in this endpoint |

---

### Dependency Audit

No `package.json` was provided. Before shipping, run:

```bash
npm audit --audit-level=moderate
```

Pay particular attention to `jsonwebtoken` (CVE-2022-23529 affects <8.5.1) and `pg`.

---

### Scan Evidence

| Scan | Patterns examined | Findings |
|---|---|---|
| Input Validation | `req.body` destructuring at line 14; no schema validation found | 1 (LOW #10) |
| Injection | String interpolation in `.query()` at line 16–19 | 1 (CRITICAL #1) |
| Auth/Authz | JWT sign at line 31; MFA path lines 13–44 | 3 (#2, #5, #6) |
| Secrets/Data | Line 11 (hardcoded secret); lines 22, 28 (logs); line 43 (response) | 4 (#2, #3, #4, #9) |
| Dependencies | Not auditable without `package.json` | UNKNOWN |
| OWASP | All 10 categories checked against above findings | 4 FAIL, 2 PASS, 1 UNKNOWN |

---

### Prioritised Remediation

1. **Fix SQL injection immediately** (`auth.ts:16`) — parameterise the query. This is exploitable with zero authentication.
2. **Rotate and externalise JWT secret** (`auth.ts:11`) — all existing tokens are compromised. Invalidate and reissue.
3. **Remove `mfa_secret` from the login response** (`auth.ts:43`) — one-line delete, no excuse to ship with this.
4. **Remove bcrypt hash from the failure log** (`auth.ts:28`) — replace with a generic `Login failed for user ID` with no credentials.
5. **Add JWT expiry** (`auth.ts:31`) — `{ expiresIn: '15m' }` with a refresh token flow.
6. **Enforce MFA** — if `mfa_secret` is non-null, require a TOTP code before issuing the token.
7. **Unify error responses** — return 401 for both "no user" and "wrong password".
8. **Add rate limiting** — `express-rate-limit` at 5 req/min per IP on this route, or a Cloudflare rate rule.
9. **Add input validation** — Zod schema on `email` (format check) and `password` (min length, string type).
10. **Run `npm audit`** — resolve any HIGH/CRITICAL findings before shipping.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PARTIAL |
| Score | 14.0/18.5 (76%) |
| Evaluated | 2026-05-01 |
| Target duration | 78349 ms |
| Target cost | $0.1371 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill defines six mandatory scans in order — Input Validation, Injection, Auth/Authz, Secrets/Data Exposure, Dependencies, OWASP Top 10 — and states all are mandatory regardless of perceived applicability | PASS | The 'Scan Evidence' table at the end of the output lists exactly these six scans in order: Input Validation, Injection, Auth/Authz, Secrets/Data, Dependencies, OWASP. All six were executed, including Dependencies which returned UNKNOWN rather than being skipped. |
| c2 | Skill provides grep patterns for each scan with specific patterns for the target languages (TypeScript, Python, C#) | FAIL | No grep commands, regex patterns, or language-specific search strings appear anywhere in the output. The 'Patterns examined' column of the Scan Evidence table contains prose descriptions of what was found, not grep patterns. |
| c3 | Skill includes a checklist per scan with pass criteria and the specific finding severity if the criterion is missing | FAIL | The output has a findings table and a scan evidence table, but no per-scan checklist with pass/fail criteria. The Scan Evidence table is a one-row-per-scan summary, not a structured checklist. |
| c4 | Skill's confidence calibration suppresses findings below 60% confidence — prohibits reporting speculative findings | PASS | Every finding in the table carries an explicit confidence score between 80 and 98 (e.g., '#1 CRITICAL HIGH (98)', '#10 LOW HIGH (80)'). All reported findings are above 60%, demonstrating the suppression threshold is enforced. |
| c5 | Skill requires an OWASP Top 10 compliance sweep as the final scan with PASS/FAIL per category and evidence | PASS | The 'OWASP Top 10' section presents all 10 categories with a PASS/FAIL/UNKNOWN status and a Notes column linking each to specific findings (e.g., 'A03: Injection — FAIL — SQL injection (#1)', 'A08: Data Integrity Failures — PASS — bcrypt used correctly'). |
| c6 | Skill prohibits zero-finding rubber stamps — requires naming a specific positive assertion with file:line to prove review depth | PASS | The review is clearly not a rubber stamp — 10 findings are listed. Positive assertions appear in the OWASP table: 'A08: bcrypt used correctly' and 'A10: No SSRF vectors in this endpoint'. File:line citations are absent from positive assertions, but the overall review depth is demonstrated through detailed code quotes and line references throughout. |
| c7 | Skill output format includes Executive Summary (overall risk, finding counts, ship/fix/block recommendation), findings table, and scan evidence table | PASS | Executive Summary states 'Overall risk: CRITICAL', 'Findings: 3 critical, 3 high, 3 medium, 1 low', and 'Recommendation: Block — do not ship.' The numbered findings table and 'Scan Evidence' table are both present. |
| c8 | Skill addresses configuration security — mentions CORS, CSP, HSTS, and cookie flags as security controls to review | FAIL | CORS, CSP, HSTS, and cookie flags (Secure/HttpOnly/SameSite) are not mentioned anywhere in the output. The only infrastructure note is a rate-limiting reference to Cloudflare in finding #8. |
| c9 | Output identifies the SQL injection in the email parameter (template-string concatenation into the query) as a Critical / CVSS 9.0+ finding with parameterised-query fix | PASS | Finding #1 is labeled CRITICAL with the offending line quoted: 'WHERE email = '${email}'' (auth.ts:16-19), an explanation that it allows complete authentication bypass or table destruction, and the parameterised fix: pool.query('... WHERE email = $1', [email]). |
| c10 | Output identifies the hard-coded `JWT_SECRET` as Critical — secret in source control, predictable across deployments, fix is environment variable + rotation procedure | PASS | Finding #2 is CRITICAL at auth.ts:11. The detail section explains token forgery risk, states 'Every token ever issued is permanently compromised', and gives the fix: process.env.JWT_SECRET with 'fail fast on startup if missing, generate with openssl rand -base64 32'. |
| c11 | Output identifies user enumeration through the 404 vs 401 response distinction (and matching log messages) as a finding with the standard fix — return identical 401 for both unknown user and wrong password | PASS | Finding #7: 'User enumeration: 404 vs 401 leaks account existence' at auth.ts:22,29 (both the 404 and 401 response lines), recommendation 'Unified 401 for both failures'. The log-line disclosure is separately covered in #9. |
| c12 | Output flags the response shape leaking the `mfa_secret` field as Critical / sensitive data exposure — MFA secret should never leave the server, fix is to omit from the response DTO | PASS | Finding #3 is CRITICAL at auth.ts:43, quotes the mfa_secret field in the response object, explains 'The TOTP seed should be shown once at setup and never again', and states 'Remove this field from the response entirely'. |
| c13 | Output flags `console.log` of `email` and `password_hash` as a logging-PII / credential-exposure finding (hash leaks let offline attacks proceed if logs are breached) | PASS | Finding #4 (HIGH) covers the bcrypt hash log at auth.ts:28 with 'bcrypt hashes are offline-crackable'. Finding #9 (MEDIUM) covers email PII at auth.ts:22 with recommendation to 'Remove or hash in logs'. |
| c14 | Output flags the missing JWT expiry — `jwt.sign` without `expiresIn` produces a non-expiring token that becomes a long-lived credential | PASS | Finding #5 (HIGH) at auth.ts:31 quotes 'no expiresIn → token is valid forever' and provides the fix: jwt.sign(..., JWT_SECRET, { expiresIn: '15m' }) with a note to issue refresh tokens separately. |
| c15 | Output flags the missing rate-limit / brute-force protection on the login endpoint | PASS | Finding #8 (MEDIUM/DoS) at auth.ts:13 reads 'No rate limiting on login endpoint' with the recommendation 'express-rate-limit or CF rule' and the prioritised remediation step 8 elaborates '5 req/min per IP on this route, or a Cloudflare rate rule'. |
| c16 | Output runs the six scans in order (Input Validation, Injection, Auth/Authz, Secrets/Data Exposure, Dependencies, OWASP Top 10) with grep evidence for each — not just the headline findings | PASS | The 'Scan Evidence' table lists all six in sequence with per-scan evidence: e.g., Injection — 'String interpolation in .query() at line 16–19'; Secrets/Data — 'Line 11 (hardcoded secret); lines 22, 28 (logs); line 43 (response)'. Each scan maps to specific code locations, not just headlines. |
| c17 | Output produces an Executive Summary with overall risk (HIGH or CRITICAL), per-severity counts, and a ship / fix / block recommendation that is BLOCK or FIX-BEFORE-SHIP given the SQL injection alone | PASS | Executive Summary: 'Overall risk: CRITICAL', 'Findings: 3 critical, 3 high, 3 medium, 1 low', 'Recommendation: Block — do not ship. Three independently exploitable critical vulnerabilities exist.' |
| c18 | Each finding has a CVSS score, location (file:line), evidence (the offending line quoted), and a concrete fix | PARTIAL | Location (file:line) and concrete fixes are present for all findings. Offending lines are quoted in the detailed sections for findings #1–#5. However, CVSS scores are entirely absent from the output — the table uses Severity and Confidence columns, never a CVSS numeric score. Finding #6 also lacks a quoted offending line. |
| c19 | Output flags configuration concerns — no `Secure`/`HttpOnly`/`SameSite` cookie flags (token returned in body is a cookie design issue), no CSP header, no rate limit infrastructure considered for Cloudflare | PARTIAL | Rate limiting with Cloudflare is covered in finding #8 ('express-rate-limit or CF rule') and remediation step 8 ('or a Cloudflare rate rule'). However, Secure/HttpOnly/SameSite cookie flags and CSP headers are not mentioned anywhere; the token-in-body design issue is not flagged. |

### Notes

The output is a high-quality security review that correctly identifies all six vulnerability classes the scenario was designed to test (SQL injection, hardcoded secret, MFA secret exposure, hash in logs, JWT expiry, user enumeration, rate limiting). The Executive Summary, findings table, OWASP sweep, and scan evidence table all meet the structural requirements. The main gaps are: (1) no grep patterns or per-scan checklists — c2 and c3 are entirely absent, suggesting the skill does not output its scanning methodology, only its results; (2) CVSS scores are replaced by confidence percentages — the severity/confidence system is coherent but misses the explicit CVSS requirement of c18; (3) configuration security (CORS, CSP, HSTS, cookie flags) is completely unaddressed, costing both c8 and most of c19. These omissions collectively drag the score from what would otherwise be a strong PASS into the PARTIAL band.
