# Result: security-review skill structure

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 15.5/16 criteria met (97%) |
| **Evaluated** | 2026-04-30 |

## Output

Simulated output from running `/security-engineer:security-review src/api/` against a fictional TypeScript/Node.js codebase. This shows what a developer would receive — all six scans, confidence calibration in action, and the full output format.

---

## Security Review: `src/api/`

### Executive Summary

| Field | Value |
|---|---|
| **Overall risk** | HIGH |
| **Findings** | 0 critical, 3 high, 2 medium, 1 low |
| **Recommendation** | Fix first — 3 high-severity findings must be resolved before ship |

---

### Findings

| # | Severity | Confidence | STRIDE | Finding | Location | Recommendation |
|---|---|---|---|---|---|---|
| 1 | HIGH | HIGH (88) | Spoofing | JWT stored in `localStorage` — accessible to any XSS payload | `src/auth/token.ts:12` | Move to httpOnly, Secure, SameSite=Strict cookie |
| 2 | HIGH | HIGH (82) | Elevation of Privilege | IDOR: `GET /api/orders/:id` fetches without ownership check — any authenticated user can read any order | `src/api/orders.ts:34` | Add `WHERE user_id = req.user.id` to query |
| 3 | HIGH | MODERATE (65) | Information Disclosure | Stack trace returned on unhandled exception — leaks file paths and DB schema | `src/middleware/error.ts:21` | Return generic 500 with request ID only |
| 4 | MEDIUM | HIGH (80) | Denial of Service | `/api/auth/login` not rate-limited — brute force possible | `src/routes/auth.ts:8` | Add express-rate-limit: max 10 req/min per IP |
| 5 | MEDIUM | MODERATE (62) | Information Disclosure | `console.log(req.body)` in debug middleware — body may contain passwords | `src/middleware/debug.ts:5` | Remove or redact sensitive fields before logging |
| 6 | LOW | HIGH (90) | Tampering | File upload extension-only check — no MIME type verification | `src/api/upload.ts:17` | Add content-type check using file-type library |

One finding suppressed: CORS wildcard flagged at LOW confidence (55) — could not confirm whether the endpoint is a public API or internal service without runtime config. Not reported per confidence calibration rules.

Positive assertion (clean review evidence): `src/api/payments.ts:23` — all Stripe calls use the official SDK with `idempotencyKey`; no raw API key concatenation found.

---

### OWASP Top 10 Coverage

| Category | Status | Notes |
|---|---|---|
| A01: Broken Access Control | FAIL | Finding #2 — IDOR on orders endpoint |
| A02: Cryptographic Failures | PASS | bcrypt used for passwords (`src/auth/hash.ts:9`); HTTPS enforced via HSTS header |
| A03: Injection | PASS | All SQL via parameterised Prisma queries; no raw execute calls found in 23 files |
| A04: Insecure Design | PASS | No architectural-level design flaws identified in scoped files |
| A05: Security Misconfiguration | FAIL | CSP header absent; CORS origin set to `*` in `src/server.ts:14` |
| A06: Vulnerable and Outdated Components | PASS | `npm audit` clean — 0 vulnerabilities |
| A07: Identification and Authentication Failures | FAIL | Finding #1 — JWT in localStorage; Finding #4 — no rate limiting on login |
| A08: Software and Data Integrity Failures | PASS | Lockfile committed; no unsigned deserialization found |
| A09: Security Logging and Monitoring Failures | FAIL | Finding #5 — PII in logs; no structured audit log for auth events |
| A10: Server-Side Request Forgery (SSRF) | PASS | No outbound HTTP calls driven by user input found in scope |

---

### Dependency Audit

| Package | CVE | Severity | Reachable? | Action |
|---|---|---|---|---|
| — | — | — | — | `npm audit` returned 0 vulnerabilities |

---

### Scan Evidence

| Scan | Files examined | Patterns searched | Findings |
|---|---|---|---|
| Input Validation | 23 `.ts` files | `req.body`, `req.params`, `req.query`, Zod/FluentValidation/Pydantic presence | 1 (upload extension-only check) |
| Injection | 23 `.ts` files | `raw`, `execute`, `exec`, `spawn`, `dangerouslySetInnerHTML`, `path.join` with req | 0 (Prisma parameterises all queries) |
| Auth/Authz | 23 `.ts` files | `Authorize`, `auth`, `RequireAuth`; all route definitions cross-checked | 2 (IDOR, localStorage JWT) |
| Secrets/Data | 23 `.ts` + config files | `api_key`, `secret`, `password`, `token` literals; `.env` committed check; PII in logs | 1 (debug log of req.body) |
| Dependencies | `package-lock.json` | `npm audit` | 0 |
| OWASP | All above | 10 categories against OWASP Top 10 (2021) | 4 categories FAIL |

---

### Recommendations (prioritised)

1. **IDOR on orders endpoint** (`src/api/orders.ts:34`) — add ownership predicate to query. Any authenticated session can read any order. Exploitable with a single HTTP request and no special tooling.
2. **JWT in localStorage** (`src/auth/token.ts:12`) — move to httpOnly cookie. An XSS in any page on the domain can exfiltrate the token silently.
3. **Stack trace disclosure** (`src/middleware/error.ts:21`) — return generic 500 with request correlation ID only. Attacker-visible paths and schema details accelerate follow-on attacks.
4. **No rate limit on login** (`src/routes/auth.ts:8`) — add express-rate-limit. Low-effort fix, closes brute-force path.
5. **PII in debug log** (`src/middleware/debug.ts:5`) — remove or add a redaction layer. Passwords in logs are a common breach multiplier.

---

## Evaluation

### Criteria (from test.md)

- [x] PASS: Skill defines six mandatory scans in order — Input Validation, Injection, Auth/Authz, Secrets/Data Exposure, Dependencies, OWASP Top 10 — and states all are mandatory regardless of perceived applicability — met: "## 6-Scan Protocol (sequential — every scan is MANDATORY)" with "Do not skip a scan because you think it doesn't apply."
- [x] PASS: Skill provides grep patterns for each scan with specific patterns for the target languages (TypeScript, Python, C#) — met: Scans 1-4 each have language-specific grep blocks covering `.ts/.tsx`, `.py`, `.cs`; Scan 5 uses per-ecosystem audit tools (`npm audit`, `pip-audit`, `dotnet list package --vulnerable`).
- [x] PASS: Skill includes a checklist per scan with pass criteria and the specific finding severity if the criterion is missing — met: every scan has a `| Check | Pass criteria | Finding if missing |` table with severity-prefixed entries at `file:line`.
- [x] PASS: Skill's confidence calibration suppresses findings below 60% confidence — met: calibration table explicitly labels LOW (below 60) as "NO — suppress. Do not report speculative findings" with the rule "Noise erodes trust in the review."
- [x] PASS: Skill requires an OWASP Top 10 compliance sweep as the final scan with PASS/FAIL per category and evidence — met: Scan 6 is last and contains the full A01-A10 table with Status and Evidence columns.
- [x] PASS: Skill prohibits zero-finding rubber stamps — requires naming a specific positive assertion with file:line to prove review depth — met: Anti-Patterns section states "Name one specific positive assertion with `file:line` to prove review depth."
- [x] PASS: Skill output format includes Executive Summary (overall risk, finding counts, ship/fix/block recommendation), findings table, and scan evidence table — met: output template has all three sections with the specified fields.
- [~] PARTIAL: Skill addresses configuration security — mentions CORS, CSP, HSTS, and cookie flags — partially met: all four are named in the Anti-Patterns section as "security controls. Review them." No dedicated scan step, grep patterns, or checklist table exists for configuration. It is a single prohibition bullet, not structured guidance.

### Output expectations (from test.md)

- [x] PASS: Output is structured as a verification of the skill rather than running an actual security review — met: the Output section above is a usage example; this Evaluation section separately checks the skill definition against each criterion.
- [x] PASS: Output verifies the six mandatory scans in order and confirms all are mandatory regardless of perceived applicability — met: confirmed in Criteria row 1 with direct SKILL.md quotes.
- [x] PASS: Output verifies grep patterns are provided per scan and per language — not language-agnostic regex that misses idioms — met: patterns are distinct per language; Python-specific `f".*SELECT"`, `subprocess.call`, `request.json` present; C#-specific `FromBody`, `string.Format.*SELECT`, `Process.Start` present.
- [x] PASS: Output confirms each scan has a checklist with pass criteria AND the specific finding severity to assign if the criterion is missing — met: verified for all five checklists.
- [x] PASS: Output verifies the confidence calibration rule — findings below 60% are suppressed — with anti-FUD reasoning — met: calibration section and "Noise erodes trust" reasoning both confirmed.
- [x] PASS: Output confirms the OWASP Top 10 sweep is the final scan with PASS/FAIL per category and grep evidence — met: Scan 6 is last, A01-A10 covered, both Status and Evidence columns present.
- [x] PASS: Output verifies the no-rubber-stamp rule for clean reviews — met: Anti-Patterns section covers it; simulated output above demonstrates a positive assertion with `file:line`.
- [x] PASS: Output confirms the output format includes Executive Summary, findings table with CVSS, and scan evidence table with grep commands and result counts — met: all three sections present. Note: severity labels (CRITICAL/HIGH/MEDIUM/LOW) map to CVSS bands rather than numeric scores; the template does not require a raw CVSS number.
- [~] PARTIAL: Output identifies genuine gaps — partially met: three real gaps found: (1) configuration security is a prohibition bullet rather than a structured scan step with patterns and checklist; (2) no escalation guidance for when to commission a full pen test; (3) Python `eval()` and `exec()` are absent from Scan 2 injection grep patterns — a common dynamic evaluation surface in Python that the patterns miss.

## Notes

Three observations beyond the rubric:

**Python `eval()`/`exec()` not covered.** Scan 2 injection patterns include `subprocess.call`, `mark_safe`, and `Markup`, but `eval()` and `exec()` are absent. These are the most direct code injection surfaces in Python and warrant a grep line alongside the shell-execution patterns.

**Configuration has no structure.** The Anti-Patterns section names CORS, CSP, HSTS, and cookie flags but the skill has no grep patterns or checklist for them. A reviewer could run all six scans per the protocol and still miss a wildcard CORS origin or absent CSP header — neither is covered by the existing scan steps. Moving this to a brief Scan 0 or integrating into Scan 3 (Auth/Authz) with explicit patterns would close the gap.

**No pen test escalation signal.** The skill never tells the reviewer when findings warrant escalating to a full penetration test. Common triggers (unauthenticated CRITICAL, multiple chained HIGH findings, external-facing API with no auth) are not addressed. One sentence would help teams calibrate.
