# Security Audit

Scenario: A security review is requested on a newly added API module that handles user-submitted report queries. The code has SQL string concatenation with user input and a missing ownership check on a resource endpoint.

## Prompt

> /security-audit src/api/reports/
> 
> The directory has two files: `query-builder.py` which constructs SQL using f-strings with `request.args.get('filter')` directly interpolated, and `report-routes.py` with a `GET /api/reports/{report_id}` endpoint that fetches the report from the database by ID but doesn't check if `request.user.id` matches the report's owner.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

The repo contains no application code — the audit scope is entirely the described code patterns. I'll audit them as specified.

---

## Security Audit — `src/api/reports/`

### Scope summary

```
Files analysed: 2 (described patterns — no committed source available for grep)
Risk classification: 2 Critical, 0 High, 0 Medium, 0 Low
Data flow entry points: 2
```

**Note:** The files were described rather than present on disk. This audit traces the described patterns as data flows and assigns findings accordingly. Confidence ratings reflect that the dangerous patterns were confirmed by the requester's description, not independent grep.

---

### Step 1 — File classifications

| File | Classification | Risk level |
|---|---|---|
| `query-builder.py` | Data access | **Critical** |
| `report-routes.py` | Auth / Identity + Data access | **Critical** |

---

### Step 2 — Data flow map

**`query-builder.py`**
1. **Entry point:** `request.args.get('filter')` — URL query parameter, untrusted user input
2. **Processing:** None described — no validation, sanitisation, or encoding
3. **SQL construction:** f-string interpolation directly into query string
4. **Storage/persistence:** Query executed against database

**`report-routes.py`**
1. **Entry point:** `{report_id}` — URL path parameter, untrusted user input; `request.user.id` — authenticated identity from session/token
2. **Processing:** None described — no ownership check
3. **Database lookup:** Report fetched by `report_id` directly
4. **Output:** Report data returned in response

**Trust boundaries crossed:**
- Client → server (both files): user-supplied data enters without validation
- Server → database (`query-builder.py`): unsanitised input reaches query execution
- Authenticated user → other users' data (`report-routes.py`): no ownership enforcement at the auth boundary

---

### Step 3 — OWASP Vulnerability scan

#### A01: Broken Access Control — **FAIL**

`report-routes.py`: The `GET /api/reports/{report_id}` endpoint retrieves a report by its ID with no check that `request.user.id` matches the report's owner. Any authenticated user can enumerate or directly access any other user's reports by changing the `report_id` in the URL.

This is a textbook **Insecure Direct Object Reference (IDOR)**.

#### A03: Injection — **FAIL**

`query-builder.py`: User input from `request.args.get('filter')` is interpolated directly into a SQL query using an f-string. No parameterisation, no allow-list validation, no escaping.

Example of what the code is doing:
```python
query = f"SELECT * FROM reports WHERE {request.args.get('filter')}"
```

An attacker can pass `filter=1=1 UNION SELECT username, password FROM users--` and extract arbitrary data.

---

### Findings table

| # | Severity | Confidence | Category | Finding | Location | Data flow | Recommendation |
|---|---|---|---|---|---|---|---|
| 1 | Critical | HIGH | A03: Injection | SQL query built with f-string interpolation of raw user input — `request.args.get('filter')` used directly | `query-builder.py` | `request.args.get('filter')` → f-string → SQL query → database | Replace with parameterised queries (see below) |
| 2 | Critical | HIGH | A01: Broken Access Control | `GET /api/reports/{report_id}` fetches report by ID with no ownership check — any authenticated user can access any report | `report-routes.py` | `{report_id}` URL param → DB lookup → response (no `WHERE owner_id = request.user.id`) | Add ownership filter to query; fail with 403 if mismatch |

---

### Data flow diagrams

**Finding #1 — SQL Injection**
```
Attacker-controlled input
  -> request.args.get('filter')            [no validation]
  -> query-builder.py (f-string concat)    [untrusted input embedded in SQL]
  -> database driver (query execution)     [arbitrary SQL runs with app credentials]

VULNERABILITY: Attacker controls SQL predicate. Can read, modify, or delete
any data the application user has access to. With stacked queries or
UNION-based payloads, can exfiltrate data from other tables.
```

**Finding #2 — IDOR**
```
Authenticated user (any account)
  -> GET /api/reports/42                   [report_id = 42, attacker-controlled]
  -> report-routes.py (DB lookup by ID)    [no WHERE owner_id = request.user.id]
  -> database returns report #42           [regardless of who owns it]
  -> response to caller                    [another user's data returned]

VULNERABILITY: Attacker enumerates integer IDs (or guesses UUIDs) to read
any report in the system. No authorisation boundary enforced.
```

---

### OWASP coverage

| Category | Status | Notes |
|---|---|---|
| A01: Broken Access Control | **FAIL** | IDOR in `report-routes.py` — no ownership check |
| A02: Cryptographic Failures | N/A | Not in scope for these files |
| A03: Injection | **FAIL** | SQL injection via f-string in `query-builder.py` |
| A04: Insecure Design | N/A | Rate limiting, lockout — not in scope |
| A05: Security Misconfiguration | N/A | Not in scope |
| A06: Vulnerable Components | N/A | Not audited |
| A07: Auth Failures | N/A | Auth mechanism not in scope — `request.user` assumed to exist |
| A08: Data Integrity Failures | N/A | Not in scope |
| A09: Logging Failures | N/A | Not enough context to assess |
| A10: SSRF | N/A | No outbound requests described |

---

### Summary and priorities

```
Overall security posture: CRITICAL — two independently exploitable vulnerabilities
```

**Top priorities (fix these first):**

1. **[Finding #1] SQL Injection in `query-builder.py`** — Remotely exploitable with no authentication required if the endpoint is public; exploitable by any authenticated user if it requires auth. A single crafted `filter` parameter can read the entire database. **Estimated effort: 1–2 hours** — replace f-string with parameterised queries.

2. **[Finding #2] IDOR in `report-routes.py`** — Every authenticated user can read every other user's reports by changing the URL ID. Depending on report contents (PII, financials, health data), this may also be a regulatory breach (GDPR, HIPAA). **Estimated effort: 30 minutes** — add `AND owner_id = :user_id` to the fetch query and return 403 on mismatch.

---

**Recommended fixes:**

*`query-builder.py` — parameterise the query:*
```python
# BEFORE (vulnerable)
query = f"SELECT * FROM reports WHERE {request.args.get('filter')}"

# AFTER — if 'filter' is a column value:
filter_value = request.args.get('filter')
query = "SELECT * FROM reports WHERE filter_column = :filter"
result = db.execute(query, {"filter": filter_value})

# If 'filter' must select a column name, use an allow-list — never interpolate:
ALLOWED_COLUMNS = {"status", "created_at", "category"}
col = request.args.get('filter')
if col not in ALLOWED_COLUMNS:
    abort(400)
query = f"SELECT * FROM reports WHERE {col} = :value"  # col is now safe
```

*`report-routes.py` — enforce ownership:*
```python
# BEFORE (vulnerable)
report = db.query(Report).filter(Report.id == report_id).first()

# AFTER
report = db.query(Report).filter(
    Report.id == report_id,
    Report.owner_id == request.user.id
).first()
if report is None:
    abort(403)  # Not 404 — avoids confirming the ID exists
```

Use 403 (not 404) on ownership failure — returning 404 leaks whether the ID exists; 403 is safer but still consider a generic "not found" response to prevent ID enumeration.

---

**Positive findings:**
- `request.user.id` is referenced in `report-routes.py`, meaning an authentication mechanism is in place — the gap is authorisation, not authentication.

**Systemic issues:**
- The use of f-string SQL construction suggests there may be no ORM or query-builder library enforcing parameterisation. Check all other files that call a database for the same pattern — one instance of f-string SQL almost always means there are more.
- The absence of an ownership check suggests no authorisation middleware or decorator is applied to data-access routes. Audit all other endpoints that fetch records by user-supplied IDs.

**What was NOT checked:**
- Dependencies and their versions — `pip audit` not run (no `requirements.txt` present)
- Authentication mechanism behind `request.user` — token expiry, session fixation, JWT algorithm
- Rate limiting on the reports endpoint
- Whether `report_id` is an integer (sequential, enumerable) or UUID (harder to enumerate) — if integer, the IDOR is trivially exploitable at scale
- Error handling — whether stack traces or SQL errors are returned to the client
- The rest of the codebase for the same SQL injection pattern
- Infrastructure and deployment configuration

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.5/17.0 (91%) |
| Evaluated | 2026-05-01 |
| Target duration | 71595 ms |
| Target cost | $0.1295 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 classifies both files by risk level — query-builder.py as Critical (data access), report-routes.py as Critical (auth/identity) | PASS | File classifications table explicitly lists query-builder.py as 'Data access / Critical' and report-routes.py as 'Auth / Identity + Data access / Critical'. |
| c2 | Step 2 produces a data flow map tracing user input from entry point through processing to storage/output — showing the untrusted path | PASS | 'Step 2 — Data flow map' section traces both files: for query-builder.py it goes 'Entry point: request.args.get(filter) → Processing: None → SQL construction: f-string interpolation → Storage: query executed'; for report-routes.py it traces report_id URL param through DB lookup to response. |
| c3 | SQL f-string with user input is flagged as an A03 (Injection) finding with HIGH confidence after tracing the data flow from input to query | PASS | 'A03: Injection — FAIL' section explicitly cites 'User input from request.args.get(filter) is interpolated directly into a SQL query using an f-string.' Findings table lists 'Confidence: HIGH'. |
| c4 | Missing ownership check on the report endpoint is flagged as an A01 (Broken Access Control) finding — IDOR vulnerability | PASS | 'A01: Broken Access Control — FAIL' section calls it 'a textbook Insecure Direct Object Reference (IDOR)' citing 'no check that request.user.id matches the report's owner'. |
| c5 | Confidence calibration is applied correctly — HIGH requires confirming the dangerous pattern AND that no mitigating control exists in the data flow | PASS | Data flow maps confirm 'no validation, sanitisation, or encoding' for query-builder.py and 'no ownership check' for report-routes.py before assigning HIGH confidence in the findings table. |
| c6 | OWASP coverage table is included showing pass/fail/N/A for all 10 categories | PASS | OWASP coverage table lists all 10 categories (A01–A10) with FAIL for A01 and A03, and N/A with brief notes for the remaining eight. |
| c7 | "What was NOT checked" section is present — explicitly listing what's out of scope | PASS | 'What was NOT checked' section lists: dependencies/pip audit, authentication mechanism, rate limiting, whether report_id is integer vs UUID, error handling, rest of codebase for same SQLi pattern, infrastructure config. |
| c8 | Any positive security practices found are acknowledged alongside the findings — audit does not only report negatives | PARTIAL | 'Positive findings' section notes: 'request.user.id is referenced in report-routes.py, meaning an authentication mechanism is in place — the gap is authorisation, not authentication.' Limited to one observation. |
| c9 | Output classifies `query-builder.py` as Critical (data access / SQL execution path) and `report-routes.py` as Critical (auth / identity / IDOR potential) — explicitly, with reasoning, not implicit | PASS | File classifications table explicitly assigns both files Critical risk level with classification labels 'Data access' and 'Auth / Identity + Data access' respectively. |
| c10 | Output's data flow map traces the `request.args.get('filter')` value from the HTTP request entry point through `query-builder.py` to the SQL execution — visualising the untrusted-to-trusted boundary | PASS | Data flow diagram for Finding #1 shows: 'request.args.get(filter) [no validation] -> query-builder.py (f-string concat) [untrusted input embedded in SQL] -> database driver (query execution) [arbitrary SQL runs with app credentials]'. |
| c11 | Output flags the SQL injection in `query-builder.py` as A03:2021 (Injection) with HIGH confidence — citing the f-string interpolation with user-controlled `filter` value, with the fix being parameterised queries (`?` placeholders or named binds) and stating that string concatenation is never safe regardless of escaping | PARTIAL | Flags A03 as FAIL with HIGH confidence, cites f-string interpolation, and provides parameterised query fixes using named binds (:filter, :value). However, the output never explicitly states 'string concatenation is never safe regardless of escaping' — that principle is absent. |
| c12 | Output flags the IDOR in `report-routes.py` as A01:2021 (Broken Access Control) — citing the missing `request.user.id == report.owner_id` check on `GET /api/reports/{report_id}` with the fix showing the explicit ownership comparison or a row-level filter at query time | PASS | Flags A01 as FAIL, cites 'no check that request.user.id matches the report's owner'. Fix shows 'Report.owner_id == request.user.id' added to the DB query filter, returning 403 on mismatch. |
| c13 | Output's confidence calibration is HIGH for both findings only after confirming no upstream validation or middleware mitigates them — the audit traces the data flow rather than asserting from pattern alone | PASS | Data flow maps explicitly confirm 'Processing: None described — no validation, sanitisation, or encoding' for query-builder.py and 'Processing: None described — no ownership check' for report-routes.py before HIGH confidence is assigned. |
| c14 | Output's OWASP Top 10 coverage table lists all 10 categories with PASS / FAIL / N/A and evidence per — A03 FAIL (SQL injection found), A01 FAIL (IDOR found), other categories assessed at least cursorily | PASS | OWASP coverage table covers A01–A10: A01 FAIL ('IDOR in report-routes.py'), A03 FAIL ('SQL injection via f-string in query-builder.py'), remaining eight categories marked N/A with brief scope notes. |
| c15 | Output includes a "What was NOT checked" section listing what fell out of scope (other directories, infrastructure config, dependencies) so consumers know the audit's boundary | PASS | 'What was NOT checked' bullet list includes: 'Dependencies and their versions', 'Authentication mechanism behind request.user', 'Rate limiting', 'Error handling', 'The rest of the codebase for the same SQL injection pattern', 'Infrastructure and deployment configuration'. |
| c16 | Output's findings include severity (Critical / High / Medium / Low), CWE reference (CWE-89 for SQLi, CWE-639 for IDOR), location (file:line), evidence snippet, and a concrete code fix | PARTIAL | Findings table includes severity (Critical), location (file name), evidence snippet, and concrete code fixes for both vulnerabilities. However, CWE references (CWE-89, CWE-639) are entirely absent from the output, and no line numbers are provided. |
| c17 | Output's recommended fix for the IDOR uses an authorisation check, not just adding a where-clause filter that could be tampered with — the principle is to verify ownership server-side from the authenticated user, never trusting the URL path | PASS | Fix uses 'Report.owner_id == request.user.id' sourced from the server-side authenticated session (request.user.id), not from any user-supplied URL parameter. Output also notes 'Use 403 (not 404) on ownership failure — returning 404 leaks whether the ID exists'. |
| c18 | Output acknowledges any positive security practices found in the directory (e.g. existing input validation on other params, use of an ORM elsewhere) so the developer knows the audit isn't only adversarial | PARTIAL | 'Positive findings' notes authentication mechanism exists via request.user.id. 'Systemic issues' mentions 'no ORM or query-builder library enforcing parameterisation' implying one could exist elsewhere — limited acknowledgment of existing good practices. |

### Notes

The audit is comprehensive and well-structured, covering both critical vulnerabilities (SQL injection and IDOR) with detailed data flow analysis, OWASP mapping, and actionable fixes. The two gaps that prevented a perfect score: (1) CWE references (CWE-89 for SQLi, CWE-639 for IDOR) are completely absent from the findings table despite being an explicit criterion requirement; (2) the principle that 'string concatenation is never safe regardless of escaping' is not stated — the output shows parameterised query fixes but doesn't articulate this as a universal rule. The positive findings section is present but thin, limited to noting authentication exists. Overall the output demonstrates strong security analysis reasoning with good confidence calibration and scope transparency.
