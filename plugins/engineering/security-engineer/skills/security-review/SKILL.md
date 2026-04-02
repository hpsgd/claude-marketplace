---
name: security-review
description: Review code or configuration for security vulnerabilities — OWASP Top 10, secrets, auth, injection.
argument-hint: "[file, directory, or git diff range to review]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Security review $ARGUMENTS.

## 6-Scan Protocol (sequential — every scan is MANDATORY)

Execute all six scans in order. Do not skip a scan because you think it doesn't apply. Evidence of execution is required for each scan. Use [OWASP ASVS 4.0](https://owasp.org/www-project-application-security-verification-standard/) as the comprehensive security verification standard (286 requirements across 14 categories, 3 verification levels).

### Scan 1: Input Validation

**Goal:** Every external input is validated at the boundary before it reaches business logic.

**Grep patterns:**
```bash
# Find all request input points
grep -rn "req\.body\|req\.params\|req\.query\|Request\.\|formData\|searchParams" --include="*.ts" --include="*.tsx"
grep -rn "FromBody\|FromQuery\|FromRoute\|FromForm\|BindProperty" --include="*.cs"
grep -rn "request\.json\|request\.form\|request\.args\|request\.data" --include="*.py"
```

**Checklist:**

| Check | Pass criteria | Finding if missing |
|---|---|---|
| All inputs validated | Zod schema, FluentValidation, Pydantic, or manual validation at entry point | MEDIUM: Unvalidated input at `file:line` |
| Allowlists over denylists | Validation defines what IS valid, not what IS NOT | HIGH: Denylist-based validation at `file:line` |
| Type coercion explicit | No implicit string-to-number, no truthy/falsy validation | LOW: Implicit coercion at `file:line` |
| File uploads validated | File type, size limit, content-type verification (not just extension) | HIGH: Unvalidated file upload at `file:line` |
| Output encoding | Context-appropriate encoding (HTML, URL, JS, SQL) | HIGH: Missing output encoding at `file:line` |

### Scan 2: Injection

**Goal:** No user input reaches interpreters (SQL, shell, HTML, template) without parameterisation or encoding.

**Grep patterns:**
```bash
# SQL injection — raw queries or string concatenation
grep -rn "raw\|execute\|\.query(" --include="*.ts" --include="*.py" --include="*.cs"
grep -rn "string\.Format.*SELECT\|string\.Format.*INSERT\|\$\".*SELECT\|\$\".*INSERT" --include="*.cs"
grep -rn "f\".*SELECT\|f\".*INSERT\|%.*SELECT\|\.format.*SELECT" --include="*.py"

# Command injection
grep -rn "exec\|spawn\|system\|popen\|subprocess\.call\|Process\.Start" --include="*.ts" --include="*.py" --include="*.cs"

# XSS — unescaped output
grep -rn "dangerouslySetInnerHTML\|innerHTML\|document\.write\|v-html\|\|safe\|mark_safe\|Markup\|HtmlString" --include="*.tsx" --include="*.vue" --include="*.py" --include="*.cs"

# Path traversal
grep -rn "path\.join\|path\.resolve\|os\.path\.join\|Path\.Combine" --include="*.ts" --include="*.py" --include="*.cs" | grep -i "req\|request\|param\|user"
```

**Checklist:**

| Check | Pass criteria | Finding if missing |
|---|---|---|
| SQL parameterised | All queries use parameterised queries or ORM | CRITICAL: SQL injection at `file:line` |
| No shell commands with user input | User input never passed to exec/system/popen | CRITICAL: Command injection at `file:line` |
| No XSS vectors | All user content HTML-encoded, CSP headers set | HIGH: XSS vector at `file:line` |
| No path traversal | File paths validated against a root, no `../` allowed | HIGH: Path traversal at `file:line` |
| No template injection | User input never used as template source | CRITICAL: Template injection at `file:line` |

### Scan 3: Authentication and Authorisation

**Goal:** Identity is verified on every request, and permissions are enforced server-side.

**Grep patterns:**
```bash
# Auth middleware/decorators — verify coverage
grep -rn "Authorize\|auth\|protected\|RequireAuth\|login_required\|permission_required" --include="*.ts" --include="*.cs" --include="*.py"

# Endpoints without auth — find all route definitions and check each
grep -rn "app\.get\|app\.post\|app\.put\|app\.delete\|router\.\|MapGet\|MapPost\|@app\.route\|@router\." --include="*.ts" --include="*.cs" --include="*.py"
```

**Checklist:**

| Check | Pass criteria | Finding if missing |
|---|---|---|
| Auth on every endpoint | All non-public endpoints have auth middleware/attribute | CRITICAL: Unauthenticated endpoint at `file:line` |
| No IDOR | Resource access checks ownership (user A can't access user B's data by changing ID) | CRITICAL: IDOR at `file:line` |
| Password hashing | bcrypt or argon2 (NOT MD5, SHA1, SHA256, or plaintext) | CRITICAL: Weak password hashing at `file:line` |
| Session management | httpOnly cookies, Secure flag, SameSite attribute, short-lived tokens | HIGH: Insecure session management at `file:line` |
| Rate limiting | Auth endpoints rate-limited (login, password reset, token refresh) | MEDIUM: No rate limiting on `file:line` |
| CSRF protection | Anti-CSRF tokens on state-changing requests (POST, PUT, DELETE) | HIGH: No CSRF protection at `file:line` |

### Scan 4: Secrets and Data Exposure

**Goal:** No secrets in code, no PII in logs, encryption where required.

**Grep patterns:**
```bash
# Hardcoded secrets
grep -rn "api[_-]key\|apiKey\|secret\|password\|token\|bearer\|credential\|private[_-]key" --include="*.ts" --include="*.cs" --include="*.py" --include="*.json" --include="*.yaml" --include="*.yml" | grep -v "node_modules\|test\|mock\|stub\|example\|schema\|type\|interface\|\.d\.ts"

# .env files committed
find . -name ".env" -not -path "*/node_modules/*" -not -path "*/.git/*" -not -name ".env.example"

# Logging sensitive data
grep -rn "console\.log\|logger\.\|log\.\|Logger\." --include="*.ts" --include="*.cs" --include="*.py" | grep -i "password\|token\|secret\|credit\|ssn\|email"
```

**Checklist:**

| Check | Pass criteria | Finding if missing |
|---|---|---|
| No hardcoded secrets | All secrets from environment variables or secret manager | CRITICAL: Hardcoded secret at `file:line` |
| `.env` in `.gitignore` | `.env` files never committed (`.env.example` without values OK) | CRITICAL: Secrets committed at `file:line` |
| No PII in logs | Logs do not contain passwords, tokens, emails, SSNs, credit cards | HIGH: PII in logs at `file:line` |
| Encryption at rest | Sensitive data encrypted in database (PII fields, financial data) | HIGH: Unencrypted sensitive data at `file:line` |
| Error messages safe | 4xx/5xx responses don't leak stack traces, file paths, or DB schema | MEDIUM: Information disclosure at `file:line` |

### Scan 5: Dependencies

**Goal:** No known vulnerabilities in dependencies, especially in reachable code paths.

```bash
# Run the appropriate audit tool
npm audit 2>/dev/null || true
pip-audit 2>/dev/null || true
dotnet list package --vulnerable 2>/dev/null || true
```

**For each vulnerability found:**

1. Is the vulnerable code path actually reachable in this project?
2. Is a patched version available?
3. What is the CVSS score and attack vector?

**Triage categories:**
- **Fix now:** Reachable, HIGH/CRITICAL severity, fix available
- **Fix soon:** Reachable, MEDIUM severity, or fix requires coordination
- **Monitor:** Not reachable, or LOW severity with no current fix

### Scan 6: OWASP Top 10 Compliance Sweep

Final pass against each OWASP Top 10 (2021) category:

| # | Category | Status | Evidence |
|---|---|---|---|
| A01 | Broken Access Control | PASS/FAIL | [specific finding or "checked, no issues"] |
| A02 | Cryptographic Failures | PASS/FAIL | [evidence] |
| A03 | Injection | PASS/FAIL | [evidence] |
| A04 | Insecure Design | PASS/FAIL | [evidence] |
| A05 | Security Misconfiguration | PASS/FAIL | [evidence] |
| A06 | Vulnerable and Outdated Components | PASS/FAIL | [evidence] |
| A07 | Identification and Authentication Failures | PASS/FAIL | [evidence] |
| A08 | Software and Data Integrity Failures | PASS/FAIL | [evidence] |
| A09 | Security Logging and Monitoring Failures | PASS/FAIL | [evidence] |
| A10 | Server-Side Request Forgery (SSRF) | PASS/FAIL | [evidence] |

For each FAIL: reference the specific finding from Scans 1-5.

## Confidence Calibration (MANDATORY)

Every finding has a confidence level. This prevents false positives from polluting the report.

| Confidence | Criteria | Report? |
|---|---|---|
| **HIGH (80+)** | Complete attack path traceable — specific input, specific code path, specific exploit outcome. Reproducible | YES — include in findings |
| **MODERATE (60-79)** | Pattern present but confirming requires runtime info or specific conditions | YES — include with caveat |
| **LOW (below 60)** | Requires unlikely conditions, speculative chaining, or unverified assumptions | NO — suppress. Do not report speculative findings |

**Rules:**
- Never report a finding below confidence 60. Noise erodes trust in the review
- If unsure, investigate further before reporting. Read more code, trace more paths
- A finding with HIGH confidence and LOW severity is still worth reporting
- A finding with LOW confidence and HIGH severity should be investigated further (not reported as-is)

## Anti-Patterns (NEVER do these)

- **Skipping scans** — all 6 scans are mandatory. "I don't think injection applies" is not valid
- **Reporting without evidence** — every finding has a `file:line` reference and a specific description
- **Paraphrasing grep results** — show the exact code, not a summary
- **Severity inflation** — CRITICAL means "exploitable, high impact, no auth required." Not "I don't like this pattern"
- **Zero-finding rubber stamp** — if you find nothing, verify you actually read the code. Name one specific positive assertion with `file:line` to prove review depth
- **Ignoring configuration** — CORS, CSP, HSTS, cookie flags are security controls. Review them

## Output Format

```markdown
## Security Review: [scope]

### Executive Summary
- **Overall risk:** [CRITICAL / HIGH / MEDIUM / LOW]
- **Findings:** [X critical, Y high, Z medium, W low]
- **Recommendation:** [ship / fix first / block]

### Findings

| # | Severity | Confidence | STRIDE | Finding | Location | Recommendation |
|---|---|---|---|---|---|---|
| 1 | CRITICAL | HIGH (95) | Injection | SQL injection via unsanitised user input | `src/api/users.ts:47` | Use parameterised query |
| 2 | HIGH | HIGH (85) | Spoofing | JWT stored in localStorage | `src/auth/token.ts:12` | Move to httpOnly cookie |

### OWASP Top 10 Coverage
| Category | Status | Notes |
|---|---|---|
| A01: Broken Access Control | PASS/FAIL | [detail] |
| ... | ... | ... |

### Dependency Audit
| Package | CVE | Severity | Reachable? | Action |
|---|---|---|---|---|

### Scan Evidence
| Scan | Files examined | Patterns searched | Findings |
|---|---|---|---|
| Input Validation | [count] | [patterns] | [count] |
| Injection | [count] | [patterns] | [count] |
| Auth/Authz | [count] | [patterns] | [count] |
| Secrets/Data | [count] | [patterns] | [count] |
| Dependencies | [manifest] | [tool used] | [count] |
| OWASP | [all above] | [10 categories] | [count] |

### Recommendations (prioritised)
1. [Most critical — what, where, how to fix]
2. [Second priority]
3. [Third priority]
```

## Related Skills

- `/security-engineer:threat-model` — review findings inform the threat model. Update threat mitigations based on review results.
- `/security-engineer:dependency-audit` — run alongside the security review to catch vulnerable dependencies.

Use the security review template (`templates/security-review.md`) for consistent output structure.
