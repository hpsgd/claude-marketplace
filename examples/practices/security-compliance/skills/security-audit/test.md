# Test: security-audit injection and access control findings

Scenario: A security review is requested on a newly added API module that handles user-submitted report queries. The code has SQL string concatenation with user input and a missing ownership check on a resource endpoint.

## Prompt

/security-audit src/api/reports/

The directory has two files: `query-builder.py` which constructs SQL using f-strings with `request.args.get('filter')` directly interpolated, and `report-routes.py` with a `GET /api/reports/{report_id}` endpoint that fetches the report from the database by ID but doesn't check if `request.user.id` matches the report's owner.

## Criteria

- [ ] PASS: Step 1 classifies both files by risk level — query-builder.py as Critical (data access), report-routes.py as Critical (auth/identity)
- [ ] PASS: Step 2 produces a data flow map tracing user input from entry point through processing to storage/output — showing the untrusted path
- [ ] PASS: SQL f-string with user input is flagged as an A03 (Injection) finding with HIGH confidence after tracing the data flow from input to query
- [ ] PASS: Missing ownership check on the report endpoint is flagged as an A01 (Broken Access Control) finding — IDOR vulnerability
- [ ] PASS: Confidence calibration is applied correctly — HIGH requires confirming the dangerous pattern AND that no mitigating control exists in the data flow
- [ ] PASS: OWASP coverage table is included showing pass/fail/N/A for all 10 categories
- [ ] PASS: "What was NOT checked" section is present — explicitly listing what's out of scope
- [ ] PARTIAL: Any positive security practices found are acknowledged alongside the findings — audit does not only report negatives

## Output expectations

- [ ] PASS: Output classifies `query-builder.py` as Critical (data access / SQL execution path) and `report-routes.py` as Critical (auth / identity / IDOR potential) — explicitly, with reasoning, not implicit
- [ ] PASS: Output's data flow map traces the `request.args.get('filter')` value from the HTTP request entry point through `query-builder.py` to the SQL execution — visualising the untrusted-to-trusted boundary
- [ ] PASS: Output flags the SQL injection in `query-builder.py` as A03:2021 (Injection) with HIGH confidence — citing the f-string interpolation with user-controlled `filter` value, with the fix being parameterised queries (`?` placeholders or named binds) and stating that string concatenation is never safe regardless of escaping
- [ ] PASS: Output flags the IDOR in `report-routes.py` as A01:2021 (Broken Access Control) — citing the missing `request.user.id == report.owner_id` check on `GET /api/reports/{report_id}` with the fix showing the explicit ownership comparison or a row-level filter at query time
- [ ] PASS: Output's confidence calibration is HIGH for both findings only after confirming no upstream validation or middleware mitigates them — the audit traces the data flow rather than asserting from pattern alone
- [ ] PASS: Output's OWASP Top 10 coverage table lists all 10 categories with PASS / FAIL / N/A and evidence per — A03 FAIL (SQL injection found), A01 FAIL (IDOR found), other categories assessed at least cursorily
- [ ] PASS: Output includes a "What was NOT checked" section listing what fell out of scope (other directories, infrastructure config, dependencies) so consumers know the audit's boundary
- [ ] PASS: Output's findings include severity (Critical / High / Medium / Low), CWE reference (CWE-89 for SQLi, CWE-639 for IDOR), location (file:line), evidence snippet, and a concrete code fix
- [ ] PASS: Output's recommended fix for the IDOR uses an authorisation check, not just adding a where-clause filter that could be tampered with — the principle is to verify ownership server-side from the authenticated user, never trusting the URL path
- [ ] PARTIAL: Output acknowledges any positive security practices found in the directory (e.g. existing input validation on other params, use of an ORM elsewhere) so the developer knows the audit isn't only adversarial
