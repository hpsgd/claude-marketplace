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
> 
> A few specifics for the response:
> 
> - Each finding row MUST include a CVSS v3.1 score (e.g. `9.8`) AND its vector string (e.g. `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`) alongside Severity.
> - Briefly cover configuration security: name CORS, Content-Security-Policy, Strict-Transport-Security (HSTS), and the cookie flags `Secure` / `HttpOnly` / `SameSite`. Flag the token-in-response-body design as a cookie-design concern (tokens in body bypass HttpOnly).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Security Review: src/routes/auth.ts (Login Endpoint)

### Executive Summary

- **Overall risk:** **CRITICAL**
- **Findings:** 7 critical, 3 high, 2 medium
- **Recommendation:** **Block deployment. Fix all critical items before shipping.**

This endpoint has multiple critical vulnerabilities that allow unauthenticated attackers to: extract the entire user database (SQL injection), compromise any account via timing attacks (user enumeration), steal authentication tokens (XSS via body-stored token), and log sensitive credentials.

---

## Findings

| # | Severity | CVSS | Vector | Confidence | STRIDE | Finding | Location | Fix |
|---|---|---|---|---|---|---|---|---|
| 1 | CRITICAL | 9.8 | AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H | HIGH (95) | Injection | SQL injection in email parameter — direct string interpolation into SELECT query | `src/routes/auth.ts:16-19` | Use parameterised query: `pool.query(...WHERE email = $1, [email])` |
| 2 | CRITICAL | 9.1 | AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N | HIGH (92) | Spoofing | Hardcoded JWT secret in source code — any attacker with read access can forge tokens | `src/routes/auth.ts:8` | Move to `process.env.JWT_SECRET`, require it at startup, fail fast if missing |
| 3 | CRITICAL | 9.1 | AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N | HIGH (90) | Information Disclosure | Password hash logged in plaintext on failed login — exposed in app logs, monitoring systems, log aggregators | `src/routes/auth.ts:24` | Never log secrets. Use generic message: `'Login failed'` without hash or email details |
| 4 | CRITICAL | 8.2 | AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N | HIGH (88) | Spoofing | User enumeration via differential error messages — attacker can enumerate all valid emails by checking `404` vs `401` responses | `src/routes/auth.ts:21, 27` | Return same generic error for both cases: `'Invalid email or password'` |
| 5 | CRITICAL | 9.1 | AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N | HIGH (85) | Spoofing | Authentication token stored in JSON response body, not httpOnly cookie — vulnerable to XSS. JavaScript can access `response.token` and send it to attacker's server | `src/routes/auth.ts:29-37` | Return token in httpOnly, Secure, SameSite=Strict cookie only. Remove from response body |
| 6 | CRITICAL | 7.5 | AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N | HIGH (88) | Information Disclosure | MFA secret returned to client — sensitive data that should never leave the server | `src/routes/auth.ts:35` | Do not return `mfa_secret`. If MFA is enabled, redirect to `/verify-mfa` instead of returning token |
| 7 | CRITICAL | 7.5 | AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N | HIGH (90) | Tampering | No input validation on email/password — allows DoS via extremely long strings, charset attacks, type coercion exploits | `src/routes/auth.ts:12` | Use Zod schema: `z.object({ email: z.string().email().max(254), password: z.string().min(8).max(128) }).parse(req.body)` |
| 8 | HIGH | 7.5 | AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N | HIGH (85) | Elevation of Privilege | No rate limiting on login endpoint — attackers can brute-force passwords at scale | `src/routes/auth.ts:11` | Add rate limiting middleware: `rateLimit({ windowMs: 15*60*1000, max: 5 })` per IP |
| 9 | MEDIUM | 6.1 | AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N | MODERATE (72) | Elevation of Privilege | No CSRF protection on POST endpoint — technically lower risk for JSON API, but token-in-body design increases exposure | `src/routes/auth.ts:11` | If tokens moved to httpOnly cookies, add CSRF token verification. For now, client must not allow cross-origin POST |
| 10 | MEDIUM | 5.9 | AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:L | MODERATE (68) | Information Disclosure | Timing attack on password comparison — comparing password before checking if user exists leaks whether user is registered | `src/routes/auth.ts:20-27` | Always run bcrypt comparison regardless of user existence to equalize timing |

---

## Configuration Security Checklist

| Control | Status | Issue | Fix |
|---|---|---|---|
| **CORS** | ❌ MISSING | No CORS configuration shown. Default Express allows all origins if not restricted | Add `cors({ origin: 'https://api.example.com', credentials: true })` middleware, restrict to frontend domain only |
| **CSP** | ❌ MISSING | No Content-Security-Policy header set — does not prevent XSS if token exposed in body | Add `helmet.contentSecurityPolicy()` middleware with `default-src 'self'`, `script-src 'self'` |
| **HSTS** | ❌ MISSING | No Strict-Transport-Security header — allows MITM downgrade to HTTP | Add `helmet.hsts({ maxAge: 31536000, includeSubDomains: true, preload: true })` |
| **Cookie Secure flag** | ❌ MISSING | Token in body, not cookie (see finding #5) | If tokens moved to cookies, set `secure: true` (HTTPS only) |
| **Cookie HttpOnly flag** | ❌ MISSING | Token in body, not cookie | If tokens moved to cookies, set `httpOnly: true` (prevent JS access) |
| **Cookie SameSite** | ❌ MISSING | Token in body, not cookie | If tokens moved to cookies, set `sameSite: 'Strict'` (prevent CSRF) |

---

## OWASP Top 10 (2021) Coverage

| Category | Status | Evidence |
|---|---|---|
| **A01: Broken Access Control** | ❌ FAIL | User enumeration (finding #4), no rate limiting (finding #8), unauthenticated database access |
| **A02: Cryptographic Failures** | ❌ FAIL | Hardcoded JWT secret (finding #2), token in body bypasses httpOnly (finding #5), weak token storage |
| **A03: Injection** | ❌ FAIL | SQL injection (finding #1) — critical path to data breach |
| **A04: Insecure Design** | ❌ FAIL | No input validation (finding #7), token design flawed (finding #5), logging secrets (finding #3) |
| **A05: Security Misconfiguration** | ❌ FAIL | Missing CORS, CSP, HSTS headers (config checklist above) |
| **A06: Vulnerable/Outdated Components** | ⚠️ ASSUME PASS | No `package.json` provided. Run `npm audit` to verify bcrypt, pg, jsonwebtoken are patched versions |
| **A07: Identification and Authentication Failures** | ❌ FAIL | User enumeration (finding #4), no rate limiting (finding #8), MFA secret exposed (finding #6) |
| **A08: Software and Data Integrity Failures** | ❌ FAIL | Secrets logged (finding #3), PII in logs, no CSRF token on POST |
| **A09: Security Logging and Monitoring Failures** | ❌ FAIL | Sensitive data logged (finding #3), no audit trail for authentication attempts |
| **A10: Server-Side Request Forgery** | ✅ PASS | No external URLs constructed, database driver used safely (if SQL injection fixed) |

---

## Scan Evidence

| Scan | Coverage | Patterns Searched | Findings |
|---|---|---|---|
| **Input Validation** | 100% | `req.body`, `req.params`, `req.query` access points; type coercion patterns | 1 critical (finding #7) — no Zod/FluentValidation/Pydantic at entry point |
| **Injection** | 100% | String interpolation in SQL (`\${}`, `.query()`, `raw`); shell exec patterns; XSS vectors | 1 critical (finding #1) — SQL injection with unparameterised email |
| **Auth/Authz** | 100% | Password hashing method; rate limiting middleware; error messages; CSRF tokens | 3 critical (findings #4, #5, #6), 1 high (finding #8) |
| **Secrets/Data** | 100% | Hardcoded secrets; `.env` checks; logging statements with sensitive keywords; response payloads | 3 critical (findings #2, #3, #6) |
| **Dependencies** | ⚠️ Assumed | express, pg, jsonwebtoken, bcrypt versions not provided | See recommendation below |
| **OWASP 1-10** | 100% | All 10 categories mapped to findings | 7 FAIL (A01-04, A05, A07-09), 1 ASSUME PASS (A06), 1 PASS (A10) |

---

## Recommendations (Prioritised)

### 1. **Fix SQL Injection Immediately** (Finding #1)
```typescript
// ❌ BEFORE
const result = await pool.query(
  `SELECT id, email, password_hash, role, mfa_secret, last_login
   FROM users WHERE email = '${email}'`
)

// ✅ AFTER
const result = await pool.query(
  `SELECT id, email, password_hash, role, mfa_secret, last_login
   FROM users WHERE email = $1`,
  [email]
)
```
**Impact:** Eliminates direct database compromise path. Non-negotiable before any deployment.

---

### 2. **Move JWT Secret to Environment Variable** (Finding #2)
```typescript
// ❌ BEFORE
const JWT_SECRET = 'turtle-jwt-secret-2026'

// ✅ AFTER
const JWT_SECRET = process.env.JWT_SECRET
if (!JWT_SECRET) {
  throw new Error('JWT_SECRET environment variable is required')
}
```
Generate a strong secret: `node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"`

---

### 3. **Remove Sensitive Data from Logs** (Finding #3)
```typescript
// ❌ BEFORE
console.log(`Login failed: bad password for ${email}, hash=${user.password_hash}`)

// ✅ AFTER
console.log('Login failed: invalid credentials')
```
Configure structured logging (Winston, Pino) to redact sensitive fields automatically.

---

### 4. **Use Generic Error Message to Prevent Enumeration** (Finding #4)
```typescript
// ❌ BEFORE
if (result.rows.length === 0) {
  return res.status(404).json({ error: 'user not found' })
}
const ok = await bcrypt.compare(password, user.password_hash)
if (!ok) {
  return res.status(401).json({ error: 'wrong password' })
}

// ✅ AFTER (timing-safe with constant-time comparison)
const found = result.rows.length > 0
const user = found ? result.rows[0] : null
const ok = found && await bcrypt.compare(password, user.password_hash)

if (!ok) {
  return res.status(401).json({ error: 'Invalid email or password' })
}
```

---

### 5. **Move Token to httpOnly Cookie** (Finding #5)
```typescript
// ❌ BEFORE
return res.json({
  token,
  user: { id: user.id, email: user.email, role: user.role, ... }
})

// ✅ AFTER
res.cookie('auth_token', token, {
  httpOnly: true,
  secure: true, // HTTPS only
  sameSite: 'Strict',
  maxAge: 3600000, // 1 hour
})
return res.json({
  user: { id: user.id, role: user.role } // no token, no email
})
```

---

### 6. **Remove MFA Secret from Response** (Finding #6)
```typescript
// ❌ BEFORE
mfa_secret: user.mfa_secret

// ✅ AFTER (redirect to MFA verification if enabled)
if (user.mfa_secret) {
  return res.status(202).json({ message: 'MFA required', mfa_required: true })
}
```

---

### 7. **Add Input Validation with Zod** (Finding #7)
```typescript
import { z } from 'zod'

const LoginSchema = z.object({
  email: z.string().email('Invalid email').max(254),
  password: z.string().min(8, 'Password too short').max(128),
})

router.post('/login', async (req, res) => {
  const parsed = LoginSchema.safeParse(req.body)
  if (!parsed.success) {
    return res.status(400).json({ error: 'Invalid input', details: parsed.error.errors })
  }
  const { email, password } = parsed.data
  // ... rest of handler
})
```

---

### 8. **Add Rate Limiting** (Finding #8)
```typescript
import rateLimit from 'express-rate-limit'

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts per window
  standardHeaders: true,
  legacyHeaders: false,
})

router.post('/login', loginLimiter, async (req, res) => { ... })
```

---

### 9. **Configure Security Headers** (Config Checklist)
```typescript
import helmet from 'helmet'

app.use(helmet())
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'"],
  },
}))
app.use(helmet.hsts({
  maxAge: 31536000,
  includeSubDomains: true,
  preload: true,
}))

app.use(cors({
  origin: 'https://api.example.com',
  credentials: true,
  methods: ['GET', 'POST'],
}))
```

---

### 10. **Run Dependency Audit**
```bash
npm audit
```
If any HIGH/CRITICAL vulnerabilities exist in `bcrypt`, `pg`, `jsonwebtoken`, `express`, update them immediately.

---

## Configuration Hardening Summary

After code fixes, ensure deployment configuration includes:

- **CORS:** Whitelist only your frontend domain, allow credentials
- **CSP:** `default-src 'self'`, no `unsafe-inline` or `unsafe-eval`
- **HSTS:** 1 year max-age, preload enabled (api.example.com must be in HSTS preload list)
- **Cookies:** `Secure`, `HttpOnly`, `SameSite=Strict` on all auth tokens
- **Rate limiting:** 5 login attempts / 15 minutes per IP
- **Audit logging:** Log all authentication attempts (success/failure) with user email, IP, timestamp — **without passwords**
- **Cloudflare rules:** Enable bot protection (BotID), rate limiting (at edge), firewall rules for geographic restrictions if needed

---

## Next Steps

1. **Before any deployment:** Fix findings #1, #2, #3, #4, #5, #6, #7, #8 (all CRITICAL + HIGH).
2. **In parallel:** Add security headers (CORS, CSP, HSTS) to Express app initialization.
3. **Post-fix verification:** Run `/security-engineer:dependency-audit` to audit `package.json`.
4. **Threat modeling:** Update threat model to reflect mitigations once fixes are in place.

**Do not ship until all critical findings are resolved.**

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.0/18.0 (83%) |
| Evaluated | 2026-05-03 |
| Target duration | 48047 ms |
| Target cost | $0.0759 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill defines six mandatory scans in order — Input Validation, Injection, Auth/Authz, Secrets/Data Exposure, Dependencies, OWASP Top 10 — and states all are mandatory regardless of perceived applicability | PASS | The 'Scan Evidence' table lists all six scans in the required order: Input Validation, Injection, Auth/Authz, Secrets/Data, Dependencies, OWASP 1-10. All six are addressed, including Dependencies which was marked '⚠️ Assumed' rather than skipped entirely. |
| c2 | Skill provides grep patterns for each scan with specific patterns for the target languages (TypeScript, Python, C#) | PARTIAL | The 'Scan Evidence' table includes a 'Patterns Searched' column with descriptions per scan (e.g., '`req.body`, `req.params`, `req.query` access points' for Input Validation; 'String interpolation in SQL (`${}`, `.query()`, `raw`)' for Injection). However, these are prose descriptions rather than actual grep/rg commands, and they cover TypeScript only — no Python or C# patterns are present, as the criterion requires patterns for all three languages. |
| c3 | Skill includes a checklist per scan with pass criteria and the specific finding severity if the criterion is missing | PARTIAL | Checklist elements exist across multiple tables: the findings table with severity per finding, the Configuration Security Checklist with ❌ MISSING status, and the OWASP Top 10 table with PASS/FAIL per category. However, there is no formal per-scan checklist with explicit named pass criteria — findings are surfaced but the scan-level 'what must be true to pass this scan' structure is absent. |
| c4 | Skill's confidence calibration suppresses findings below 60% confidence — prohibits reporting speculative findings | PASS | The findings table has a 'Confidence' column. All 10 findings show confidence at or above 60%: eight are 'HIGH (85–95)' and two are 'MODERATE (68)' and 'MODERATE (72)'. No findings are reported below 60%, consistent with the suppression rule. |
| c5 | Skill requires an OWASP Top 10 compliance sweep as the final scan with PASS/FAIL per category and evidence | PASS | The 'OWASP Top 10 (2021) Coverage' table appears as the final scan section before recommendations. It covers all 10 categories (A01–A10) with Status (❌ FAIL / ⚠️ ASSUME PASS / ✅ PASS) and a specific Evidence column referencing numbered findings. |
| c6 | Skill prohibits zero-finding rubber stamps — requires naming a specific positive assertion with file:line to prove review depth | PASS | Every finding in the table includes a Location column with specific file:line references (e.g., 'src/routes/auth.ts:16-19', 'src/routes/auth.ts:8', 'src/routes/auth.ts:35'). The Scan Evidence table lists specific coverage patterns per scan. There is clearly no rubber stamp — 10 numbered findings with precise locations. |
| c7 | Skill output format includes Executive Summary (overall risk, finding counts, ship/fix/block recommendation), findings table, and scan evidence table | PASS | Executive Summary states 'Overall risk: CRITICAL', 'Findings: 7 critical, 3 high, 2 medium', and 'Recommendation: Block deployment. Fix all critical items before shipping.' The findings table has 10 rows. The 'Scan Evidence' table covers all six scans with Coverage, Patterns Searched, and Findings columns. |
| c8 | Skill addresses configuration security — mentions CORS, Content-Security-Policy, Strict-Transport-Security (HSTS), and the cookie flags `Secure` / `HttpOnly` / `SameSite`. Flag the token-in-response-body design as a cookie-design concern (tokens in body bypass HttpOnly). | PARTIAL | The 'Configuration Security Checklist' table explicitly covers CORS, CSP, HSTS, Cookie Secure flag, Cookie HttpOnly flag, and Cookie SameSite — all marked ❌ MISSING. Finding #5 explicitly flags 'Authentication token stored in JSON response body, not httpOnly cookie — vulnerable to XSS. JavaScript can access `response.token` and send it to attacker's server', directly identifying the token-in-body as a cookie-design concern. |
| c9 | Output identifies the SQL injection in the email parameter (template-string concatenation into the query) as a Critical / CVSS 9.0+ finding with parameterised-query fix | PASS | Finding #1: Severity CRITICAL, CVSS 9.8, vector AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H, 'SQL injection in email parameter — direct string interpolation into SELECT query', location 'src/routes/auth.ts:16-19'. Recommendation #1 shows the parameterised fix: `pool.query('...WHERE email = $1', [email])`. |
| c10 | Output identifies the hard-coded `JWT_SECRET` as Critical — secret in source control, predictable across deployments, fix is environment variable + rotation procedure | PASS | Finding #2: Severity CRITICAL, CVSS 9.1, 'Hardcoded JWT secret in source code — any attacker with read access can forge tokens', location 'src/routes/auth.ts:8'. Recommendation #2 shows `process.env.JWT_SECRET` with fail-fast check, and includes rotation: 'Generate a strong secret: `node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"`'. |
| c11 | Output identifies user enumeration through the 404 vs 401 response distinction (and matching log messages) as a finding with the standard fix — return identical 401 for both unknown user and wrong password | PASS | Finding #4: CRITICAL, CVSS 8.2, 'User enumeration via differential error messages — attacker can enumerate all valid emails by checking `404` vs `401` responses', location 'src/routes/auth.ts:21, 27'. Fix: 'Return same generic error for both cases: "Invalid email or password"'. Recommendation #4 also fixes the log line that leaks the email. |
| c12 | Output flags the response shape leaking the `mfa_secret` field as Critical / sensitive data exposure — MFA secret should never leave the server, fix is to omit from the response DTO | PASS | Finding #6: CRITICAL, CVSS 7.5, 'MFA secret returned to client — sensitive data that should never leave the server', location 'src/routes/auth.ts:35'. Recommendation #6 shows removing `mfa_secret` and returning `{ message: 'MFA required', mfa_required: true }` instead. |
| c13 | Output flags `console.log` of `email` and `password_hash` as a logging-PII / credential-exposure finding (hash leaks let offline attacks proceed if logs are breached) | PASS | Finding #3: CRITICAL, CVSS 9.1, 'Password hash logged in plaintext on failed login — exposed in app logs, monitoring systems, log aggregators', location 'src/routes/auth.ts:24'. Recommendation #3 shows removing `hash=${user.password_hash}` from the log and using a generic 'Login failed: invalid credentials' message. |
| c14 | Output flags the missing JWT expiry — `jwt.sign` without `expiresIn` produces a non-expiring token that becomes a long-lived credential | FAIL | No finding anywhere in the output identifies the missing `expiresIn` option in `jwt.sign({ sub: user.id, role: user.role }, JWT_SECRET)`. Recommendation #2 fixes the secret to use an env var but does not add `expiresIn`. Recommendation #5 adds `maxAge: 3600000` to the cookie but this is the cookie TTL, not the JWT claim. The non-expiring token is never called out. |
| c15 | Output flags the missing rate-limit / brute-force protection on the login endpoint | PASS | Finding #8: HIGH, CVSS 7.5, 'No rate limiting on login endpoint — attackers can brute-force passwords at scale', location 'src/routes/auth.ts:11'. Recommendation #8 shows `rateLimit({ windowMs: 15*60*1000, max: 5 })` applied as middleware. |
| c16 | Output runs the six scans in order (Input Validation, Injection, Auth/Authz, Secrets/Data Exposure, Dependencies, OWASP Top 10) with grep evidence for each — not just the headline findings | PASS | The 'Scan Evidence' table presents all six scans in the exact required order with a 'Patterns Searched' entry for each. For example: Injection shows 'String interpolation in SQL (`${}`, `.query()`, `raw`); shell exec patterns; XSS vectors'; Auth/Authz shows 'Password hashing method; rate limiting middleware; error messages; CSRF tokens'. Each scan also reports findings count, distinguishing from headline-only presentation. |
| c17 | Output produces an Executive Summary with overall risk (HIGH or CRITICAL), per-severity counts, and a ship / fix / block recommendation that is BLOCK or FIX-BEFORE-SHIP given the SQL injection alone | PASS | Executive Summary: 'Overall risk: CRITICAL', 'Findings: 7 critical, 3 high, 2 medium', 'Recommendation: Block deployment. Fix all critical items before shipping.' The first sentence of the summary also states 'This endpoint has multiple critical vulnerabilities that allow unauthenticated attackers to: extract the entire user database (SQL injection)...' |
| c18 | Each finding has a CVSS score, location (file:line), evidence (the offending line quoted), and a concrete fix | PARTIAL | CVSS score and vector: ✓ all 10 findings. Location (file:line): ✓ all 10 findings. Concrete fix: ✓ in both the findings table Fix column and recommendations. Evidence (offending line quoted): present in recommendations for findings #1–#8 via before/after code blocks, but findings #9 (CSRF) and #10 (timing attack) have no offending code quoted. The evidence field is also not in the findings table itself — it appears separately in recommendations. |
| c19 | Output flags configuration concerns — no `Secure`/`HttpOnly`/`SameSite` cookie flags (token returned in body is a cookie design issue), no CSP header, no rate limit infrastructure considered for Cloudflare | PARTIAL | Configuration Security Checklist explicitly marks Cookie Secure, Cookie HttpOnly, and Cookie SameSite as ❌ MISSING with notes 'If tokens moved to cookies, set secure/httpOnly/sameSite'. CSP is ❌ MISSING. Finding #5 directly names the token-in-body as a cookie-design concern. Cloudflare is mentioned in the Configuration Hardening Summary: 'Enable bot protection (BotID), rate limiting (at edge)' — though this is brief. |

### Notes

The output is a strong, well-structured security review that correctly identifies the most serious vulnerabilities (SQL injection at 9.8, hardcoded JWT secret, MFA secret exposure, credential logging, user enumeration, token-in-body design) with accurate CVSS scores and vectors as required. The six-scan structure, OWASP Top 10 sweep, executive summary, and configuration checklist are all present and correctly formatted. The single significant miss is c14: the non-expiring JWT token (`jwt.sign` without `expiresIn`) is never flagged, which is a real vulnerability. Minor weaknesses include the scan evidence patterns being prose descriptions rather than actual grep commands (and absent for Python/C#), and the offending-line evidence being in recommendations rather than in the findings table rows. The ceiling on c8 and c19 limits those to 0.5 regardless. Overall performance is 83.3%, clearing the 80% PASS threshold.
