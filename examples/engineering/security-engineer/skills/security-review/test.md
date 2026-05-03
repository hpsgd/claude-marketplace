# Test: security-review skill applied to an authentication endpoint

Scenario: A backend developer asks for a security review of a new login endpoint in a Node/Express application. The handler queries Postgres directly with string concatenation, returns user records on successful authentication, logs the failed-attempt details, and uses a hard-coded secret for JWT signing. The reviewer needs to apply the six-scan security-review methodology.

## Prompt

Run a security review on this login endpoint before we ship it.

```typescript
// src/routes/auth.ts
import { Router } from 'express'
import { Pool } from 'pg'
import jwt from 'jsonwebtoken'
import bcrypt from 'bcrypt'

const pool = new Pool({ connectionString: process.env.DATABASE_URL })
const router = Router()

const JWT_SECRET = 'turtle-jwt-secret-2026'

router.post('/login', async (req, res) => {
  const { email, password } = req.body

  const result = await pool.query(
    `SELECT id, email, password_hash, role, mfa_secret, last_login
     FROM users WHERE email = '${email}'`
  )

  if (result.rows.length === 0) {
    console.log(`Login failed: no user for ${email}`)
    return res.status(404).json({ error: 'user not found' })
  }

  const user = result.rows[0]
  const ok = await bcrypt.compare(password, user.password_hash)

  if (!ok) {
    console.log(`Login failed: bad password for ${email}, hash=${user.password_hash}`)
    return res.status(401).json({ error: 'wrong password' })
  }

  const token = jwt.sign({ sub: user.id, role: user.role }, JWT_SECRET)

  return res.json({
    token,
    user: {
      id: user.id,
      email: user.email,
      role: user.role,
      mfa_secret: user.mfa_secret,
      last_login: user.last_login,
    },
  })
})

export default router
```

Stack: Node 20, Express 4, Postgres 15. This will be deployed behind Cloudflare on api.example.com.

A few specifics for the response:

- Each finding row MUST include a CVSS v3.1 score (e.g. `9.8`) AND its vector string (e.g. `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`) alongside Severity.
- Briefly cover configuration security: name CORS, Content-Security-Policy, Strict-Transport-Security (HSTS), and the cookie flags `Secure` / `HttpOnly` / `SameSite`. Flag the token-in-response-body design as a cookie-design concern (tokens in body bypass HttpOnly).

## Criteria

- [ ] PASS: Skill defines six mandatory scans in order — Input Validation, Injection, Auth/Authz, Secrets/Data Exposure, Dependencies, OWASP Top 10 — and states all are mandatory regardless of perceived applicability
- [ ] PASS: Skill provides grep patterns for each scan with specific patterns for the target languages (TypeScript, Python, C#)
- [ ] PASS: Skill includes a checklist per scan with pass criteria and the specific finding severity if the criterion is missing
- [ ] PASS: Skill's confidence calibration suppresses findings below 60% confidence — prohibits reporting speculative findings
- [ ] PASS: Skill requires an OWASP Top 10 compliance sweep as the final scan with PASS/FAIL per category and evidence
- [ ] PASS: Skill prohibits zero-finding rubber stamps — requires naming a specific positive assertion with file:line to prove review depth
- [ ] PASS: Skill output format includes Executive Summary (overall risk, finding counts, ship/fix/block recommendation), findings table, and scan evidence table
- [ ] PARTIAL: Skill addresses configuration security — mentions CORS, CSP, HSTS, and cookie flags as security controls to review

## Output expectations

- [ ] PASS: Output identifies the SQL injection in the email parameter (template-string concatenation into the query) as a Critical / CVSS 9.0+ finding with parameterised-query fix
- [ ] PASS: Output identifies the hard-coded `JWT_SECRET` as Critical — secret in source control, predictable across deployments, fix is environment variable + rotation procedure
- [ ] PASS: Output identifies user enumeration through the 404 vs 401 response distinction (and matching log messages) as a finding with the standard fix — return identical 401 for both unknown user and wrong password
- [ ] PASS: Output flags the response shape leaking the `mfa_secret` field as Critical / sensitive data exposure — MFA secret should never leave the server, fix is to omit from the response DTO
- [ ] PASS: Output flags `console.log` of `email` and `password_hash` as a logging-PII / credential-exposure finding (hash leaks let offline attacks proceed if logs are breached)
- [ ] PASS: Output flags the missing JWT expiry — `jwt.sign` without `expiresIn` produces a non-expiring token that becomes a long-lived credential
- [ ] PASS: Output flags the missing rate-limit / brute-force protection on the login endpoint
- [ ] PASS: Output runs the six scans in order (Input Validation, Injection, Auth/Authz, Secrets/Data Exposure, Dependencies, OWASP Top 10) with grep evidence for each — not just the headline findings
- [ ] PASS: Output produces an Executive Summary with overall risk (HIGH or CRITICAL), per-severity counts, and a ship / fix / block recommendation that is BLOCK or FIX-BEFORE-SHIP given the SQL injection alone
- [ ] PASS: Each finding has a CVSS score, location (file:line), evidence (the offending line quoted), and a concrete fix
- [ ] PARTIAL: Output flags configuration concerns — no `Secure`/`HttpOnly`/`SameSite` cookie flags (token returned in body is a cookie design issue), no CSP header, no rate limit infrastructure considered for Cloudflare
