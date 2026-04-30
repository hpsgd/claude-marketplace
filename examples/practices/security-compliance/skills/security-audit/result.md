# Result: security-audit injection and access control findings

**Verdict:** PASS
**Score:** 16.5/18 criteria met (92%)
**Evaluated:** 2026-04-30

---

## Output

Simulated output from `/security-audit src/api/reports/` against the two-file scenario.

---

### Scope summary

```
Files analysed: 2
Risk classification: 2 Critical, 0 High, 0 Medium, 0 Low
Data flow entry points: 2
```

**File classification:**

| File | Classification | Risk level | Reason |
|---|---|---|---|
| `query-builder.py` | Data access | Critical | Constructs and executes SQL queries; direct database interaction path |
| `report-routes.py` | Auth / Identity | Critical | Resource access endpoint; handles ownership and identity decisions |

---

### Data flow map

```
### Data flow map

1. User input entry points:
   - query-builder.py:? — `request.args.get('filter')` — URL query parameter, HTTP GET request

2. Processing / transformation:
   - query-builder.py:? — filter value interpolated directly into SQL f-string; no validation, no sanitisation, no parameterisation

3. Storage / persistence:
   - query-builder.py:? — constructed SQL string passed to database cursor or ORM raw execute

4. Output / rendering:
   - report-routes.py:? — query results returned in API response body

5. External system calls:
   - None identified in scope
```

Trust boundary violations identified:
- **Client to server to database:** `request.args.get('filter')` (untrusted, client-controlled) crosses directly into SQL execution (trusted database operation) with no boundary enforcement.
- **Authenticated user to owned resource:** `GET /api/reports/{report_id}` crosses from the URL (client-controlled) to database retrieval with no authenticated-user ownership check.

---

### Findings table

| # | Severity | Confidence | Category | Finding | Location | Data flow | Recommendation |
|---|---|---|---|---|---|---|---|
| 1 | Critical | HIGH | A03: Injection | SQL query built with f-string using `request.args.get('filter')` directly — attacker controls query structure | `query-builder.py` | `request.args.get('filter')` → f-string SQL construction → database execute | Replace f-string with parameterised query (`?` placeholder or named bind); string concatenation is never safe regardless of escaping |
| 2 | Critical | HIGH | A01: Broken Access Control | `GET /api/reports/{report_id}` fetches by ID without verifying `request.user.id == report.owner_id` — IDOR vulnerability | `report-routes.py` | URL `{report_id}` → database lookup → response with no ownership gate | Add server-side ownership check: verify `authenticated_user.id == report.owner_id` before returning data; alternatively filter query as `WHERE id = ? AND owner_id = ?` using the authenticated user's ID from the session, not the URL |

---

### Data flow diagrams

**Finding 1 — SQL Injection (A03):**

```
User input: request.args.get('filter')   [UNTRUSTED — client-controlled]
  -> query-builder.py (f-string: f"SELECT * FROM reports WHERE {filter}")
  -> No validation checkpoint
  -> No parameterisation
  -> Database cursor.execute(sql_string)   [TRUSTED operation breached]

VULNERABILITY: Attacker supplies filter=1 OR 1=1-- to dump all records,
or filter=1; DROP TABLE reports-- for destructive injection.
CWE-89: Improper Neutralisation of Special Elements in SQL Command.

Fix:
  cursor.execute("SELECT * FROM reports WHERE filter_col = ?", (filter_value,))
```

**Finding 2 — IDOR (A01):**

```
URL parameter: /api/reports/{report_id}   [UNTRUSTED — attacker can enumerate]
  -> report-routes.py: db.get_report(report_id)
  -> No check: request.user.id == report.owner_id
  -> Response returned to any authenticated user   [OWNERSHIP BOUNDARY ABSENT]

VULNERABILITY: Any authenticated user can enumerate report IDs and read
reports belonging to other users. No ownership gate at any point in the path.
CWE-639: Authorisation Bypass Through User-Controlled Key.

Fix:
  report = db.get_report(report_id)
  if report.owner_id != request.user.id:
      abort(403)
  return report
```

---

### OWASP coverage

| Category | Status | Notes |
|---|---|---|
| A01: Broken Access Control | FAIL | IDOR on `GET /api/reports/{report_id}` — no ownership check (HIGH confidence) |
| A02: Cryptographic Failures | N/A | No crypto operations, credential storage, or HTTP config in scope |
| A03: Injection | FAIL | SQL f-string injection in `query-builder.py` (HIGH confidence) |
| A04: Insecure Design | N/A | No login, rate-limiting, or account lockout logic in scope |
| A05: Security Misconfiguration | N/A | No config files, debug flags, or security headers in scope |
| A06: Vulnerable Components | N/A | No dependency manifests in scope; out-of-band dependency audit required |
| A07: Auth Failures | PASS | No password handling, session config, or JWT logic found in scope |
| A08: Data Integrity Failures | N/A | No deserialization or integrity-check logic in scope |
| A09: Logging Failures | N/A | No logging calls identified in the two files; absence noted |
| A10: SSRF | N/A | No server-side URL fetching in scope |

---

### Summary and priorities

```
### Overall security posture: Critical

**Top priorities (fix these first):**
1. [Finding #1] SQL injection in query-builder.py — remotely exploitable with no
   authentication barrier; full database read (and potentially write) access.
   Estimated effort: 30 minutes (swap f-string for parameterised query).
2. [Finding #2] IDOR on report endpoint — any authenticated user can read any
   other user's report by guessing the ID. Exploitable immediately with a
   logged-in session.
   Estimated effort: 1 hour (add ownership check + regression test).

**Positive findings:**
- No hardcoded credentials or API keys found in either file.
- No weak crypto or insecure randomness identified in scope.
- Authentication layer exists (request.user.id is populated, indicating a
  session/auth middleware is in use upstream) — the gap is authorisation,
  not authentication.

**Systemic issues:**
- No parameterised query discipline in the data access layer. Where one
  f-string SQL pattern exists, others are likely. Run this audit across all
  files matching `*query*`, `*db*`, `*repository*`.
- No ownership-check pattern visible in route handlers. If this endpoint lacks
  the check, audit all other resource-by-ID endpoints for the same omission.

**What was NOT checked:**
- Other directories outside src/api/reports/ — additional endpoints may share
  the same patterns.
- Infrastructure config, environment variables, and secrets management.
- Third-party dependency versions (npm/pip audit not run — run
  /security-engineer:dependency-audit separately).
- Authentication middleware implementation — assumed present and functional
  based on request.user.id being available, but not verified.
- Test files — not in scope for this audit pass.
```

---

## Criteria results

### Criteria (skill definition)

- [x] PASS: Step 1 classifies both files by risk level — `query-builder.py` as Critical (data access), `report-routes.py` as Critical (auth/identity) — met. The classification table in Step 1 maps "Data access" and "Auth / Identity" both to Critical, and those are the two matching categories.
- [x] PASS: Step 2 produces a data flow map tracing user input from entry point through processing to storage/output — met. Step 2 mandates the five-section template and requires trust boundary identification before proceeding to vulnerability scanning.
- [x] PASS: SQL f-string with user input is flagged as A03 (Injection) with HIGH confidence after tracing the data flow — met. Step 3 A03 patterns explicitly target `f".*SELECT` in Python; Step 5 calibration confirms HIGH when string concat + user input + no parameterisation are all confirmed.
- [x] PASS: Missing ownership check flagged as A01 (Broken Access Control) IDOR — met. Step 3 A01 explicitly checks "Direct object references without ownership check" and mandates verifying authenticated user ownership for every resource-by-ID endpoint.
- [x] PASS: Confidence calibration applied correctly — HIGH requires confirming dangerous pattern AND no mitigating control in the data flow — met. Step 5 states "Never rate something HIGH based on grep alone — you must trace the data flow."
- [x] PASS: OWASP coverage table with all 10 categories — met. Step 6 mandates the complete A01–A10 table.
- [x] PASS: "What was NOT checked" section present — met. Rules mark it mandatory; Step 6 output template includes it as a required subsection.
- [~] PARTIAL: Positive security practices acknowledged alongside findings — partially met. Step 6 mandates a "Positive findings" subsection and Rules state "Acknowledge good practices." The mechanism is structurally enforced. In the simulated output the positive findings section surfaces the authentication middleware inference — present and non-trivial. Score: 0.5.

### Output expectations (simulated output)

- [x] PASS: Output classifies `query-builder.py` as Critical (data access / SQL execution path) and `report-routes.py` as Critical (auth / identity / IDOR potential) — explicitly, with reasoning — met. Classification table in the Output section shows both as Critical with stated reasons.
- [x] PASS: Output data flow map traces `request.args.get('filter')` from HTTP entry point through `query-builder.py` to SQL execution — met. Data flow map section and Finding 1 diagram both trace this path explicitly.
- [x] PASS: Output flags SQL injection as A03:2021 with HIGH confidence, citing f-string interpolation, fix being parameterised queries, stating string concatenation is never safe — met. Finding #1 covers all three: f-string citation, HIGH confidence, fix shown with `?` placeholder, explicit note that string concatenation is never safe.
- [x] PASS: Output flags IDOR as A01:2021, citing missing `request.user.id == report.owner_id` check, fix showing explicit ownership comparison — met. Finding #2 names the check and shows the fix with explicit `report.owner_id != request.user.id` comparison.
- [x] PASS: Confidence calibration is HIGH for both findings only after confirming no upstream validation or middleware mitigates — met. The data flow diagrams trace the full path and confirm no validation checkpoint before HIGH is assigned.
- [x] PASS: OWASP Top 10 coverage table lists all 10 categories with PASS/FAIL/N/A and evidence per — met. Coverage table in Output has all 10 rows with notes.
- [x] PASS: "What was NOT checked" section lists other directories, infrastructure config, dependencies — met. Summary section lists exactly these items.
- [~] PARTIAL: Findings include severity, CWE reference (CWE-89 for SQLi, CWE-639 for IDOR), location, evidence snippet, and concrete code fix — partially met. Severity, location, evidence, and code fix are all present. CWE references (CWE-89, CWE-639) appear in the data flow diagrams but are not a named column in the findings table schema — the skill does not require a CWE column. Score: 0.5.
- [x] PASS: Recommended fix for IDOR uses server-side ownership verification from the authenticated user, not a URL-trusting where-clause — met. Fix explicitly checks `report.owner_id != request.user.id` from the session, and the note clarifies the principle of filtering via authenticated user's ID.
- [~] PARTIAL: Output acknowledges positive security practices — partially met. "Positive findings" section in the summary surfaces the authentication middleware inference (request.user.id being populated). Present and substantive for this scenario. Score: 0.5.

## Notes

The skill is methodologically strong. The confidence calibration rule in Step 5 ("never HIGH from grep alone") is the standout design choice — it prevents the most common audit failure mode of asserting vulnerabilities without tracing the data flow.

The one gap against test expectations: CWE references (CWE-89, CWE-639) are not a required column in the Step 6 findings table schema. The simulated output surfaces them in the data flow diagrams, but the skill would need an explicit CWE column in the findings table to guarantee they always appear in machine-readable form. Closing this would be a one-line schema addition.

The related skills references (`/security-engineer:threat-model`, `/security-engineer:dependency-audit`) assume those plugins are installed — a soft dependency worth documenting in the plugin manifest for marketplace consumers.
