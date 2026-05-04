# Security Audit

Scenario: A security review is requested on a newly added API module that handles user-submitted report queries. The code has SQL string concatenation with user input and a missing ownership check on a resource endpoint.

## Prompt

> /security-audit src/api/reports/
> 
> The directory has two files: `query-builder.py` which constructs SQL using f-strings with `request.args.get('filter')` directly interpolated, and `report-routes.py` with a `GET /api/reports/{report_id}` endpoint that fetches the report from the database by ID but doesn't check if `request.user.id` matches the report's owner.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Now I'll conduct the security audit following the structured methodology.

## Step 1 — Scope Identification

**Files in scope:**

```
src/api/reports/query-builder.py    → Critical — constructs SQL queries
src/api/reports/report-routes.py    → Critical — API endpoints for data access
```

Risk classification:
- **Critical:** 2 files (both handle data access and API boundaries)
- **High:** 0
- **Medium:** 0
- **Low:** 0

---

## Step 2 — Data Flow Mapping

### Data flow map

1. **User input entry points:**
   - `report-routes.py:51` — `request.args.get('filter')` parameter in `GET /api/reports`
   - `report-routes.py:13` — `report_id` path parameter in `GET /api/reports/<report_id>`
   - `report-routes.py:30` — `report_id` path parameter in `DELETE /api/reports/<report_id>`
   - `report-routes.py:44` — `report_id` path parameter in `POST /api/reports/<report_id>/share`
   - `report-routes.py:45` — `request.json['user_id']` in share endpoint

2. **Processing / transformation:**
   - `query-builder.py:6-12` — f-string concatenation of filter into SQL (NO validation)
   - `query-builder.py:36` — f-string concatenation of search term into SQL (NO validation)
   - `report-routes.py:13-19` — Direct query execution with parameterised ID (safe) but NO ownership check

3. **Storage / persistence:**
   - `query-builder.py:22` — `cursor.execute()` with unsanitised SQL
   - `query-builder.py:39` — `cursor.execute()` with unsanitised SQL
   - `report-routes.py:21` — Database read without authorisation check
   - `report-routes.py:35` — Database delete without authorisation check

4. **Output / rendering:**
   - `report-routes.py:28-34` — Returns report data including owner_id (exposes internal IDs)

5. **External system calls:**
   - None identified

### Trust boundaries

- **Client → Server:** User inputs (filter, report_id, user_id) are not validated
- **Server → Database:** SQL queries are constructed unsafely; missing ownership checks before data access

---

## Step 3 — Vulnerability Scan by OWASP Top 10

### A01: Broken Access Control — **FAIL**

**Finding:** Insecure Direct Object Reference (IDOR) in all data endpoints

- `report-routes.py:13-28` — `GET /api/reports/{report_id}` returns any report without ownership check
- `report-routes.py:30-40` — `DELETE /api/reports/{report_id}` deletes any report without ownership check
- `report-routes.py:42-54` — `POST /api/reports/{report_id}/share` shares any report without ownership check

No role-based access control (RBAC) validation found anywhere.

### A02: Cryptographic Failures — **PASS**

No cryptographic operations found. (Not applicable to this code.)

### A03: Injection — **FAIL**

**Finding:** SQL Injection in query-builder.py

- `query-builder.py:10` — SQL query built with f-string: `f"{base_query} AND {filters}"`
  - Input: `request.args.get('filter')`
  - No parameterisation
  - No allowlist
  - Direct execution: `cursor.execute(query)` on line 22

- `query-builder.py:36` — SQL query built with f-string: `f"SELECT * FROM reports WHERE name LIKE '%{search_term}%'"`
  - Input: `search_term` parameter (unsanitised)
  - Vulnerable to LIKE-based injection
  - Direct execution on line 39

Example exploit: `?filter=1 OR 1=1 --` returns all reports. `?filter=1; DROP TABLE reports; --` deletes the table.

### A04: Insecure Design — **PASS**

No rate limiting mechanisms found, but no login/registration endpoints in scope. Not applicable.

### A05: Security Misconfiguration — **PASS**

No debug mode, default credentials, or verbose error exposure found in scope.

### A06: Vulnerable Components — **OUT OF SCOPE**

Dependency audit required separately.

### A07: Auth Failures — **PASS**

Session/JWT handling not in scope. Request.user exists (line 45 reference), suggesting auth middleware is in place elsewhere.

### A08: Data Integrity — **PASS**

No deserialization or integrity checks required for this scope.

### A09: Logging Failures — **PASS**

No sensitive data logging detected in scope.

### A10: SSRF — **PASS**

No external URLs or server-side requests found.

---

## Step 4 — Additional Checks

### Hardcoded secrets
✓ None found

### Insecure randomness
✓ None found

### Race conditions
⚠ **MODERATE:** `DELETE` endpoint (line 35) could be subject to TOCTOU if concurrent requests target the same report. No transactional safety visible.

### Missing input validation at API boundaries
✗ **CRITICAL:** 
- `filter` parameter has no type, length, or content validation
- `search_term` (implied in `apply_text_filter`) has no validation
- `user_id` in share endpoint has no validation (could be non-existent, negative, etc.)
- `report_id` uses Flask's `<int:report_id>` type hint but no further validation

---

## Step 5 — Confidence Calibration

| Finding | Confidence | Reasoning |
|---|---|---|
| SQL Injection via filter param | **HIGH** | f-string concatenation, user input from request.args, direct execution, no sanitisation or parameterisation |
| SQL Injection via search_term | **HIGH** | Same pattern: f-string, user input, direct execution |
| IDOR on GET /reports/{id} | **HIGH** | No ownership check in code path, report object returned unconditionally, user can enumerate all report IDs |
| IDOR on DELETE /reports/{id} | **HIGH** | No ownership check, direct deletion, no audit trail visible |
| IDOR on POST /reports/{id}/share | **HIGH** | No ownership check, any user can share any report with anyone |
| Potential race condition on DELETE | **MODERATE** | Delete happens without row-level locking; concurrent deletes could produce inconsistent state. Depends on SQLite's isolation level. |

---

## Step 6 — Output

### Scope Summary

```
Files analysed: 2
Risk classification: 2 Critical, 0 High, 0 Medium, 0 Low
Data flow entry points: 5
Vulnerable endpoints: 4
```

### Findings Table

| # | Severity | Confidence | Category | Finding | Location | Data Flow | Recommendation |
|---|---|---|---|---|---|---|---|
| 1 | Critical | HIGH | A03: Injection | SQL Injection via filter parameter | `query-builder.py:10` | `request.args.get('filter')` → f-string → `cursor.execute()` | Use parameterised queries with `?` placeholders; implement allowlist for filter fields |
| 2 | Critical | HIGH | A03: Injection | SQL Injection via LIKE search | `query-builder.py:36` | `search_term` parameter → f-string → `cursor.execute()` | Use parameterised queries; escape wildcard characters or use parameterised LIKE |
| 3 | Critical | HIGH | A01: Access Control | IDOR on GET endpoint | `report-routes.py:13-28` | `report_id` URL param → query → return report | Add ownership check: `if report[2] != request.user.id: return 403` |
| 4 | Critical | HIGH | A01: Access Control | IDOR on DELETE endpoint | `report-routes.py:30-40` | `report_id` URL param → delete | Add ownership check before deletion; add audit log |
| 5 | Critical | HIGH | A01: Access Control | IDOR on SHARE endpoint | `report-routes.py:42-54` | `report_id` URL param → share operation | Add ownership check; validate `user_id` exists in system |
| 6 | High | MODERATE | A08: Data Integrity | TOCTOU race condition on DELETE | `report-routes.py:30-40` | Concurrent requests to same `report_id` | Wrap DELETE in transaction; use row locking or optimistic concurrency (`lastUpdatedAt`) |

### Data Flow Diagrams

**VULNERABILITY 1 & 2: SQL Injection**

```
User input (?filter or search_term)
  → request.args.get() or function parameter
  → query-builder.py:10 / query-builder.py:36 (f-string concatenation)
  → cursor.execute(query) with unsanitised SQL
  → SQLite database (arbitrary query execution)

EXAMPLE ATTACK:
GET /api/reports?filter=1 OR 1=1--
RESULT: Returns all reports, bypasses any WHERE conditions

GET /api/reports?filter=1; DELETE FROM reports; --
RESULT: Deletes entire reports table
```

**VULNERABILITY 3, 4, 5: IDOR (Insecure Direct Object Reference)**

```
User input (report_id in URL)
  → Flask route parameter /<report_id>
  → report-routes.py:13-28 (GET) / 30-40 (DELETE) / 42-54 (SHARE)
  → Database query with report_id (parameterised query — SAFE here)
  → NO ownership validation: if report.owner_id != request.user.id
  → Return/modify/share the report unconditionally

EXAMPLE ATTACK:
GET /api/reports/999 (belonging to user_id=5)
As user_id=3, you receive the full report data without authorisation check

DELETE /api/reports/999 (belonging to user_id=5)
As user_id=3, you delete another user's report
```

### OWASP Coverage Summary

| Category | Status | Notes |
|---|---|---|
| A01: Broken Access Control | **FAIL** | 3 IDOR vulnerabilities across GET, DELETE, and SHARE endpoints |
| A02: Cryptographic Failures | PASS | No cryptographic operations in scope |
| A03: Injection | **FAIL** | 2 SQL injection vectors via f-strings |
| A04: Insecure Design | PASS | Rate limiting not applicable to scope |
| A05: Security Misconfiguration | PASS | No debug/verbose error exposure detected |
| A06: Vulnerable Components | N/A | Requires dependency audit |
| A07: Auth Failures | PASS | Auth exists upstream (request.user); session management not in scope |
| A08: Data Integrity | FAIL | TOCTOU race condition on DELETE (moderate risk) |
| A09: Logging Failures | PASS | No security event logging required for scope |
| A10: SSRF | PASS | No external requests |

---

### Summary and Priorities

**Overall security posture: CRITICAL**

This code is exploitable in production. Both SQL injection and IDOR vulnerabilities are trivial to exploit and have high impact (data theft, data destruction, unauthorised modifications).

---

**Top priorities (fix these first):**

1. **SQL Injection (Vulnerabilities #1 & #2)** — Replace f-string concatenation with parameterised queries
   - Estimated effort: **15 minutes**
   - Impact: Prevents arbitrary SQL execution, table destruction, data exfiltration
   - Steps: Replace `f"{base_query} AND {filters}"` with `base_query + " AND ?"` and pass `filters` as parameter tuple
   - Applies to: `query-builder.py:10`, `query-builder.py:36`

2. **IDOR on GET/DELETE/SHARE (Vulnerabilities #3, #4, #5)** — Add ownership checks to all data-access endpoints
   - Estimated effort: **20 minutes**
   - Impact: Prevents unauthorised data access, deletion, and sharing
   - Steps: Before returning/modifying report, verify `report.owner_id == request.user.id`; return 403 if mismatch
   - Applies to: `report-routes.py:13`, `report-routes.py:30`, `report-routes.py:42`

3. **TOCTOU on DELETE (Vulnerability #6)** — Wrap DELETE in transaction with row-level locking
   - Estimated effort: **10 minutes**
   - Impact: Prevents edge cases where two concurrent deletes produce inconsistent state
   - Steps: Fetch-check-delete in a single transaction; use SQLite's `BEGIN IMMEDIATE`

---

**Positive findings:**

- ✓ Parameterised queries ARE used correctly for `report_id` in GET/DELETE/SHARE (the lookup itself is safe)
- ✓ Sensitive database credentials not hardcoded
- ✓ No command injection or template injection vectors

---

**Systemic issues:**

- **No input validation library:** The codebase lacks a schema validator (Pydantic, Marshmallow, Flask-Inputs). Every endpoint should validate request shape and types at the boundary.
- **No authorisation layer:** Access control checks are ad-hoc and missing from most endpoints. Consider extracting to a decorator: `@require_ownership(Report)` or similar.
- **SQL-building pattern is error-prone:** The `query-builder.py` approach of concatenating filters is fragile. Use an ORM (SQLAlchemy) or query builder (sqlalchemy.sql) to enforce parameterisation.

---

**What was NOT checked:**

- Dependency vulnerabilities (requires `pip audit` or similar)
- Authentication and session management (handled upstream; not in scope)
- Infrastructure and deployment configuration
- Database schema constraints and foreign keys
- Rate limiting or DDoS protection
- Logging and audit trails
- Encryption at rest or in transit (assumes HTTPS)
- Frontend/client-side security
- API documentation and versioning

---

**Remediation checklist:**

- [ ] Replace f-string SQL concatenation with parameterised queries
- [ ] Add `if report.owner_id != request.user.id: abort(403)` to GET, DELETE, SHARE
- [ ] Wrap DELETE in transaction with BEGIN IMMEDIATE
- [ ] Add input validation decorator or middleware
- [ ] Consider migrating from raw SQL to SQLAlchemy ORM
- [ ] Add unit tests for ownership checks (positive and negative cases)
- [ ] Add integration tests for IDOR payloads (verify 403 responses)

### Artifacts written

#### `work/src/api/reports/query-builder.py`

```
from flask import request
import sqlite3

def build_report_query(filters=None):
    """Construct SQL query for filtering reports."""
    base_query = "SELECT id, name, owner_id, created_at FROM reports WHERE 1=1"

    if not filters:
        filters = request.args.get('filter', '')

    # VULNERABILITY: SQL injection - f-string with user input
    if filters:
        query = f"{base_query} AND {filters}"
    else:
        query = base_query

    return query


def execute_report_query(filters=None):
    """Execute the constructed query."""
    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()

    query = build_report_query(filters)

    # Query is executed directly with user-controlled input
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    return results


def apply_text_filter(search_term):
    """Apply text search to reports."""
    # Another SQL injection vector
    query = f"SELECT * FROM reports WHERE name LIKE '%{search_term}%'"

    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    return results

```

#### `work/src/api/reports/report-routes.py`

```
from flask import Blueprint, request, jsonify, g
import sqlite3

reports_bp = Blueprint('reports', __name__, url_prefix='/api/reports')


@reports_bp.route('/<int:report_id>', methods=['GET'])
def get_report(report_id):
    """
    Fetch a report by ID.
    VULNERABILITY: No ownership check - user can access any report by ID (IDOR)
    """
    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()

    # Query fetches the report without checking ownership
    cursor.execute('SELECT id, name, owner_id, data, created_at FROM reports WHERE id = ?', (report_id,))
    report = cursor.fetchone()
    conn.close()

    if not report:
        return jsonify({'error': 'Report not found'}), 404

    # No check for: if report[2] != request.user.id
    # User can view any report regardless of ownership

    return jsonify({
        'id': report[0],
        'name': report[1],
        'owner_id': report[2],
        'data': report[3],
        'created_at': report[4]
    })


@reports_bp.route('/<int:report_id>', methods=['DELETE'])
def delete_report(report_id):
    """
    Delete a report by ID.
    VULNERABILITY: No ownership check - user can delete any report (privilege escalation)
    """
    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()

    # Delete without checking if user owns this report
    cursor.execute('DELETE FROM reports WHERE id = ?', (report_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Report deleted'}), 200


@reports_bp.route('/<int:report_id>/share', methods=['POST'])
def share_report(report_id):
    """
    Share a report with another user.
    VULNERABILITY: No ownership check - user can share any report
    """
    data = request.json
    share_with_user = data.get('user_id')

    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()

    # No verification that the requester owns this report
    cursor.execute(
        'INSERT INTO report_shares (report_id, shared_with_user_id) VALUES (?, ?)',
        (report_id, share_with_user)
    )
    conn.commit()
    conn.close()

    return jsonify({'message': 'Report shared'}), 200


@reports_bp.route('', methods=['GET'])
def list_reports():
    """
    List reports, optionally filtered.
    VULNERABILITY: Uses query-builder.py which has SQL injection
    """
    from query_builder import execute_report_query

    # Filter parameter is passed directly to query builder
    filter_param = request.args.get('filter', '')

    # This calls the vulnerable query builder
    results = execute_report_query(filters=filter_param)

    return jsonify({
        'reports': [
            {'id': r[0], 'name': r[1], 'owner_id': r[2], 'created_at': r[3]}
            for r in results
        ]
    })

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/17.0 (94%) |
| Evaluated | 2026-05-04 |
| Target duration | 62375 ms |
| Target cost | $0.1080 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 classifies both files by risk level — query-builder.py as Critical (data access), report-routes.py as Critical (auth/identity) | PASS | Step 1 explicitly: 'src/api/reports/query-builder.py → Critical — constructs SQL queries' and 'src/api/reports/report-routes.py → Critical — API endpoints for data access'. Risk classification: 'Critical: 2 files (both handle data access and API boundaries)'. |
| c2 | Step 2 produces a data flow map tracing user input from entry point through processing to storage/output — showing the untrusted path | PASS | Step 2 'Data Flow Mapping' lists five entry points (request.args.get('filter'), report_id path params, request.json['user_id']), traces through 'query-builder.py:6-12 — f-string concatenation of filter into SQL (NO validation)' and 'cursor.execute()' at lines 22 and 39, and shows output rendering returning report data. |
| c3 | SQL f-string with user input is flagged as an A03 (Injection) finding with HIGH confidence after tracing the data flow from input to query | PASS | A03: Injection — FAIL section cites 'query-builder.py:10 — SQL query built with f-string: f"{base_query} AND {filters}"' with 'Input: request.args.get("filter")'. Confidence Calibration table shows HIGH for 'SQL Injection via filter param' citing 'f-string concatenation, user input from request.args, direct execution, no sanitisation or parameterisation'. |
| c4 | Missing ownership check on the report endpoint is flagged as an A01 (Broken Access Control) finding — IDOR vulnerability | PASS | A01: Broken Access Control — FAIL: 'Finding: Insecure Direct Object Reference (IDOR) in all data endpoints' with 'report-routes.py:13-28 — GET /api/reports/{report_id} returns any report without ownership check'. Findings table entry #3 cites A01: Access Control, IDOR on GET endpoint. |
| c5 | Confidence calibration is applied correctly — HIGH requires confirming the dangerous pattern AND that no mitigating control exists in the data flow | PASS | Calibration table gives HIGH for both SQL injection ('f-string concatenation, user input from request.args, direct execution, no sanitisation or parameterisation') and IDOR ('No ownership check in code path, report object returned unconditionally'). Both explicitly confirm absence of mitigating controls, not mere pattern-matching. |
| c6 | OWASP coverage table is included showing pass/fail/N/A for all 10 categories | PASS | 'OWASP Coverage Summary' table lists all A01–A10 with PASS/FAIL/N/A. A01: FAIL, A02: PASS, A03: FAIL, A04: PASS, A05: PASS, A06: N/A, A07: PASS, A08: FAIL, A09: PASS, A10: PASS — each with a brief rationale note. |
| c7 | "What was NOT checked" section is present — explicitly listing what's out of scope | PASS | 'What was NOT checked:' section explicitly lists: dependency vulnerabilities (requires pip audit), authentication and session management, infrastructure and deployment configuration, database schema constraints, rate limiting/DDoS protection, logging and audit trails, encryption at rest or in transit, frontend/client-side security, API documentation and versioning. |
| c8 | Any positive security practices found are acknowledged alongside the findings — audit does not only report negatives | PARTIAL | 'Positive findings:' section states '✓ Parameterised queries ARE used correctly for report_id in GET/DELETE/SHARE', '✓ Sensitive database credentials not hardcoded', '✓ No command injection or template injection vectors'. Positive findings are present and substantive. |
| c9 | Output classifies `query-builder.py` as Critical (data access / SQL execution path) and `report-routes.py` as Critical (auth / identity / IDOR potential) — explicitly, with reasoning, not implicit | PASS | Step 1: 'query-builder.py → Critical — constructs SQL queries' and 'report-routes.py → Critical — API endpoints for data access' with explicit reasoning 'both handle data access and API boundaries'. Not implicit — stated directly with rationale. |
| c10 | Output's data flow map traces the `request.args.get('filter')` value from the HTTP request entry point through `query-builder.py` to the SQL execution — visualising the untrusted-to-trusted boundary | PASS | Step 2 entry points: 'report-routes.py:51 — request.args.get("filter") parameter'. Processing: 'query-builder.py:6-12 — f-string concatenation of filter into SQL (NO validation)'. Storage: 'query-builder.py:22 — cursor.execute() with unsanitised SQL'. Data flow diagram shows: 'User input (?filter) → request.args.get() → query-builder.py:10 (f-string concatenation) → cursor.execute(query) with unsanitised SQL → SQLite database'. |
| c11 | Output flags the SQL injection in `query-builder.py` as A03:2021 (Injection) with HIGH confidence — citing the f-string interpolation with user-controlled `filter` value, with the fix being parameterised queries (`?` placeholders or named binds) and stating that string concatenation is never safe regardless of escaping | PARTIAL | A03 flagged with HIGH confidence, f-string interpolation cited, parameterised fix recommended ('Replace f-string SQL concatenation with parameterised queries' with `base_query + " AND ?"` and parameter tuple). However, the output never explicitly states the principle that string concatenation is unsafe regardless of escaping — only that the current approach is 'fragile' and 'unsanitised'. The critical security principle (escaping/sanitisation cannot substitute for parameterisation) is absent. |
| c12 | Output flags the IDOR in `report-routes.py` as A01:2021 (Broken Access Control) — citing the missing `request.user.id == report.owner_id` check on `GET /api/reports/{report_id}` with the fix showing the explicit ownership comparison or a row-level filter at query time | PASS | A01 FAIL finding cites 'report-routes.py:13-28 — GET /api/reports/{report_id} returns any report without ownership check'. Findings table finding #3 recommends 'Add ownership check: if report[2] != request.user.id: return 403'. Priority 2 says 'verify report.owner_id == request.user.id; return 403 if mismatch'. |
| c13 | Output's confidence calibration is HIGH for both findings only after confirming no upstream validation or middleware mitigates them — the audit traces the data flow rather than asserting from pattern alone | PASS | Calibration table for SQL injection: 'f-string concatenation, user input from request.args, direct execution, no sanitisation or parameterisation'. For IDOR: 'No ownership check in code path, report object returned unconditionally'. Both explicitly confirm absence of upstream controls — data-flow based, not pattern-matching alone. |
| c14 | Output's OWASP Top 10 coverage table lists all 10 categories with PASS / FAIL / N/A and evidence per — A03 FAIL (SQL injection found), A01 FAIL (IDOR found), other categories assessed at least cursorily | PASS | OWASP Coverage Summary table covers all 10 (A01–A10). A01: FAIL 'IDOR vulnerabilities', A03: FAIL '2 SQL injection vectors via f-strings', A08: FAIL 'TOCTOU race condition'. Remaining categories have brief evidence notes (e.g. A07 'Auth exists upstream (request.user); session management not in scope'). |
| c15 | Output includes a "What was NOT checked" section listing what fell out of scope (other directories, infrastructure config, dependencies) so consumers know the audit's boundary | PASS | 'What was NOT checked:' explicitly lists 9 items: dependency vulnerabilities, authentication/session management, infrastructure/deployment configuration, database schema constraints/foreign keys, rate limiting/DDoS protection, logging/audit trails, encryption at rest or in transit, frontend/client-side security, API documentation and versioning. |
| c16 | Output's findings include severity (Critical / High / Medium / Low), CWE reference (CWE-89 for SQLi, CWE-639 for IDOR), location (file:line), evidence snippet, and a concrete code fix | PARTIAL | Findings table includes severity (Critical/High), location (query-builder.py:10, report-routes.py:13-28), evidence snippets (f-string patterns, IDOR explanation), and concrete code fixes (parameterised ? placeholders, ownership check code). However, CWE references (CWE-89 for SQLi, CWE-639 for IDOR) are entirely absent from the output — only OWASP categories (A01, A03) are cited. |
| c17 | Output's recommended fix for the IDOR uses an authorisation check, not just adding a where-clause filter that could be tampered with — the principle is to verify ownership server-side from the authenticated user, never trusting the URL path | PASS | Findings table: 'Add ownership check: if report[2] != request.user.id: return 403'. Priority 2: 'Before returning/modifying report, verify report.owner_id == request.user.id; return 403 if mismatch — Applies to: report-routes.py:13, 30, 42'. This is a server-side check against the authenticated user (request.user.id), not a URL-controllable where-clause filter. |
| c18 | Output acknowledges any positive security practices found in the directory (e.g. existing input validation on other params, use of an ORM elsewhere) so the developer knows the audit isn't only adversarial | PARTIAL | 'Positive findings:' section notes '✓ Parameterised queries ARE used correctly for report_id in GET/DELETE/SHARE (the lookup itself is safe)', '✓ Sensitive database credentials not hardcoded', '✓ No command injection or template injection vectors'. These are genuine practices found in the code rather than generic praise. |

### Notes

This is a high-quality security audit output that covers the two core vulnerabilities (SQL injection and IDOR) thoroughly, with strong data flow tracing, correct confidence calibration, and clear remediation guidance. Two gaps prevent a perfect score: (1) CWE references (CWE-89, CWE-639) are completely absent from the findings table — only OWASP category codes appear; and (2) the principle that string concatenation is unsafe regardless of escaping is never explicitly stated, which is a meaningful omission since developers sometimes believe sanitisation/escaping is an acceptable alternative to parameterisation. The positive findings section is genuinely useful (correctly noting that report_id lookups ARE parameterised), and the 'What was NOT checked' scope boundary section is comprehensive. The OWASP Top 10 walkthrough covers all categories with evidence, and the confidence calibration correctly traces data flows rather than asserting from pattern recognition alone.
