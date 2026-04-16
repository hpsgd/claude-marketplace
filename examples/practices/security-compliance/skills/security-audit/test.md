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
