---
name: security-audit
description: "Perform a deep security audit of code changes or a specific area of the codebase. OWASP Top 10 coverage, grep-based vulnerability detection, confidence-calibrated findings."
argument-hint: "[file path, directory, or git diff range]"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

# Security Audit

Perform a focused security audit on $ARGUMENTS. If no argument is provided, audit staged changes (`git diff --staged`).

**Mindset:** Paranoid. Assume worst-case scenario. Edge cases and unexpected inputs are always tested. "It probably won't happen" is not a security posture.

## Step 1: Scope Identification (MANDATORY)

Before scanning:

1. **Identify files in scope:**
   ```bash
   # If directory or file path
   find $ARGUMENTS -type f \( -name "*.ts" -o -name "*.cs" -o -name "*.py" -o -name "*.js" \)

   # If git diff range
   git diff --name-only $ARGUMENTS
   ```

2. **Map data flows:**
   - Where does user input enter the system? (API endpoints, form handlers, CLI args, file uploads)
   - Where does it leave? (responses, logs, database, external APIs, emails)
   - Where does it transform? (parsing, serialisation, concatenation)

3. **Identify trust boundaries:**
   - Client ↔ server
   - Server ↔ database
   - Service ↔ external API
   - Authenticated ↔ unauthenticated

## Step 2: Six-Scan Protocol (sequential)

### Scan 1: Input Validation

```bash
# Find all request input points
grep -rn "req\.body\|req\.params\|req\.query\|Request\.\|formData\|searchParams\|getServerSideProps\|getStaticProps" --include="*.ts" --include="*.tsx" --include="*.js"

# Find all form submissions
grep -rn "action=\|onSubmit\|handleSubmit\|useActionState\|server action" --include="*.ts" --include="*.tsx"
```

Check:
- [ ] Every external input validated at the boundary (Zod, joi, or manual validation)
- [ ] Allowlists used over denylists
- [ ] Output sanitised based on context (HTML, SQL, shell, URL)
- [ ] File upload validation (type, size, content sniffing)

### Scan 2: Injection

```bash
# SQL injection — raw queries
grep -rn "raw\|execute\|query\(" --include="*.ts" --include="*.cs" --include="*.py" | grep -v "parameterized\|@\|\$\|CreateCommand\|AddParameter"

# Command injection
grep -rn "exec\|eval\|spawn\|child_process\|subprocess\|os\.system\|Runtime\.exec" --include="*.ts" --include="*.cs" --include="*.py"

# Path traversal
grep -rn "path\.join\|path\.resolve\|readFile\|writeFile" --include="*.ts" --include="*.js" | grep -v "__dirname\|__filename"
```

Check:
- [ ] SQL: parameterised queries only, no string concatenation
- [ ] Command: no `exec`/`eval` with user input, safe APIs used
- [ ] XSS: output escaped, CSP headers set, no `dangerouslySetInnerHTML` without sanitisation
- [ ] Path traversal: file paths validated, no direct join with user input

### Scan 3: Authentication & Authorisation

```bash
# Find auth-related code
grep -rn "auth\|token\|session\|cookie\|jwt\|bearer\|password\|credential" --include="*.ts" --include="*.cs" --include="*.py" -i

# Find routes without auth middleware
grep -rn "router\.\|app\.\(get\|post\|put\|patch\|delete\)" --include="*.ts" --include="*.js"
```

Check:
- [ ] Auth checked on EVERY request, not just at the UI level
- [ ] No IDOR vulnerabilities (can user A access user B's data by changing an ID?)
- [ ] Session management: httpOnly cookies, secure flag, short-lived tokens
- [ ] Password hashing: bcrypt/argon2 (not MD5/SHA1/plaintext)
- [ ] Rate limiting on auth endpoints
- [ ] MFA support (blocks 99.9% of automated attacks)

### Scan 4: Secrets & Data Exposure

```bash
# Hardcoded secrets
grep -rn "api[_-]key\|apiKey\|secret\|password\|token\|bearer\|private[_-]key" --include="*.ts" --include="*.cs" --include="*.py" --include="*.json" --include="*.yaml" --include="*.yml" --include="*.env" | grep -v "test\|mock\|stub\|example\|template\|schema\|type\|interface"

# Logging sensitive data
grep -rn "console\.log\|logger\.\|Log\.\|logging\." --include="*.ts" --include="*.cs" --include="*.py" | grep -i "password\|token\|secret\|credit\|ssn\|email"
```

Check:
- [ ] No secrets in code, config files, or version control
- [ ] `.env` files in `.gitignore`
- [ ] Encryption at rest for sensitive data
- [ ] Logs don't contain passwords, tokens, PII, credit card numbers
- [ ] Error messages don't leak internal details to users
- [ ] HTTPS enforced (no HTTP fallback)

### Scan 5: Dependencies

```bash
# Run appropriate audit tool
npm audit 2>/dev/null || pip-audit 2>/dev/null || dotnet list package --vulnerable 2>/dev/null
```

Check:
- [ ] Known CVEs in dependencies? Is the vulnerable code path reachable?
- [ ] Dependencies pinned for production?
- [ ] Last dependency update date?
- [ ] Deprecated packages needing replacement?

### Scan 6: OWASP Top 10 Compliance Sweep

Final sweep against current OWASP Top 10 categories:

| Category | Status | Notes |
|---|---|---|
| A01: Broken Access Control | PASS / FAIL | |
| A02: Cryptographic Failures | PASS / FAIL | |
| A03: Injection | PASS / FAIL | |
| A04: Insecure Design | PASS / FAIL | |
| A05: Security Misconfiguration | PASS / FAIL | |
| A06: Vulnerable Components | PASS / FAIL | |
| A07: Auth Failures | PASS / FAIL | |
| A08: Data Integrity Failures | PASS / FAIL | |
| A09: Logging Failures | PASS / FAIL | |
| A10: SSRF | PASS / FAIL | |

## Step 3: Confidence Calibration

Every finding has a confidence level:

- **HIGH (80+):** Complete attack path traceable — specific input, code path, and outcome. Reproducible
- **MODERATE (60-79):** Pattern present but confirming requires runtime testing or specific conditions
- **LOW (below 60):** Requires unlikely conditions or speculative chaining. **Suppress these** — don't waste time on theoretical vulnerabilities

**Only report findings at confidence 60+.**

## Step 4: Severity Assessment

| Severity | Criteria | Examples |
|---|---|---|
| **Critical** | Exploitable remotely, no auth required, data breach or RCE | SQL injection in public endpoint, hardcoded admin credentials |
| **High** | Exploitable with low-privilege access, significant impact | IDOR allowing access to other users' data, XSS in auth flow |
| **Medium** | Requires specific conditions, moderate impact | Missing rate limiting, CSRF on non-critical endpoints |
| **Low** | Theoretical or minor impact | Information disclosure via verbose errors, missing security headers |

## Output Format

```markdown
## Security Audit: [scope]

### Executive Summary
- **Overall risk:** CRITICAL / HIGH / MEDIUM / LOW
- **Findings:** X critical, Y high, Z medium, W low
- **Recommendation:** Ship / Fix first / Block

### Data Flow Map
[Where user input enters, transforms, and exits]

### Findings

| # | Severity | Confidence | Category | Finding | Location | Recommendation |
|---|---|---|---|---|---|---|
| 1 | CRITICAL | HIGH (95) | Injection | SQL string concatenation in user search | `api/search.ts:42` | Use parameterised query |
| 2 | HIGH | HIGH (85) | Access Control | No auth check on `/api/admin/users` | `routes/admin.ts:15` | Add auth middleware |

### OWASP Coverage
[Category status table from Scan 6]

### Dependency Audit
| Package | CVE | Severity | Reachable? | Action |
|---|---|---|---|---|

### Recommendations (prioritised)
1. [Most critical — what, where, exact fix]
2. [Second priority]
3. [Third priority]

### Positive Findings
[What's done well — acknowledge good security practices]
```

## Rules

- **Paranoid by default.** Assume attackers are creative, persistent, and patient
- **Evidence over speculation.** Every finding needs a specific code location and attack scenario
- **Suppress low-confidence findings.** Speculative findings waste developer time and erode trust in audits
- **Acknowledge good practices.** If auth is solid, say so. Security audits that only report negatives are demoralising
- **60% of breaches exploit unpatched vulnerabilities.** Dependency scanning is not optional
- **Baseline controls catch most attacks.** MFA, patching, input validation, and encryption prevent more breaches than sophisticated controls
