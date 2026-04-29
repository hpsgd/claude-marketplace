# Output: security-audit injection and access control findings

**Verdict:** PASS
**Score:** 16.5/17 criteria met (97%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Step 1 classifies both files by risk level — query-builder.py as Critical (data access), report-routes.py as Critical (auth/identity) — met. The classification table in Step 1 maps "Data access" and "Auth / Identity" both to Critical.
- [x] PASS: Step 2 produces a data flow map tracing user input from entry point through processing to storage/output — met. Step 2 mandates the five-section template (entry points, processing, storage, output, external calls) and requires trust boundary identification.
- [x] PASS: SQL f-string with user input is flagged as an A03 (Injection) finding with HIGH confidence after tracing the data flow — met. Step 3 A03 patterns target `f".*SELECT` etc. in Python files; Step 5 calibration confirms HIGH when string concat + user input + no parameterisation are all confirmed in the data flow.
- [x] PASS: Missing ownership check on the report endpoint is flagged as an A01 (Broken Access Control) finding — IDOR — met. Step 3 A01 explicitly checks for "Direct object references without ownership check" and mandates verifying authenticated user ownership for every resource-by-ID endpoint.
- [x] PASS: Confidence calibration is applied correctly — HIGH requires confirming the dangerous pattern AND that no mitigating control exists in the data flow — met. Step 5 defines the exact rule and states "Never rate something HIGH based on grep alone — you must trace the data flow."
- [x] PASS: OWASP coverage table with all 10 categories showing pass/fail/N/A — met. Step 6 mandates the complete A01–A10 table as required output.
- [x] PASS: "What was NOT checked" section is present — met. The Rules section marks it mandatory and Step 6 output template includes it as a required subsection.
- [~] PARTIAL: Any positive security practices found are acknowledged alongside findings — partially met. The skill mandates a "Positive findings" subsection in Step 6 and the Rules state "Acknowledge good practices." The structural mechanism is present. With only two vulnerable files in scope and no positive practices described in the scenario, the section would exist but may contain nothing substantive. Mechanism present; substance scenario-dependent. Score: 0.5.

### Output expectations

- [x] PASS: Output classifies `query-builder.py` as Critical (data access / SQL execution path) and `report-routes.py` as Critical (auth / identity / IDOR potential) — explicitly, with reasoning — met. The Step 1 classification table drives this deterministically for these file types.
- [x] PASS: Output's data flow map traces `request.args.get('filter')` from the HTTP request through `query-builder.py` to SQL execution — met. Step 2's template requires entry points → processing → storage, and the A03 search patterns would surface this exact path.
- [x] PASS: Output flags SQL injection as A03:2021 with HIGH confidence, citing f-string interpolation, with the fix being parameterised queries — met. Step 3 A03 grep patterns target the f-string SQL pattern; Step 5 confirms HIGH; Step 6 finding table example cites "string concatenation + parameterised queries" as the fix.
- [x] PASS: Output flags the IDOR as A01:2021 — citing the missing `request.user.id == report.owner_id` check — with the fix showing explicit ownership comparison — met. Step 3 A01 explicitly requires the ownership check verification and the finding table requires a Recommendation column.
- [x] PASS: Output's confidence calibration is HIGH for both findings only after confirming no upstream validation or middleware mitigates — met. Step 5 requires tracing the full data flow as a precondition for HIGH; "Never rate something HIGH based on grep alone."
- [x] PASS: Output's OWASP Top 10 coverage table lists all 10 categories with PASS/FAIL/N/A and evidence per — met. Step 6 mandates the table; Step 3 per-category search patterns provide the evidence basis for each entry.
- [x] PASS: Output includes a "What was NOT checked" section — met. Mandatory per Rules and prescribed in the Step 6 output template.
- [~] PARTIAL: Output's findings include severity, CWE reference (CWE-89 for SQLi, CWE-639 for IDOR), location, evidence snippet, and concrete code fix — partially met. The findings table in Step 6 prescribes Severity, Confidence, Category, Finding, Location, Data flow, and Recommendation — but CWE numbers are not a named column in the schema. Severity, location, evidence, and fix are fully prescribed. CWE references would need to be inferred or added ad hoc; they are not structurally required. Score: 0.5.
- [x] PASS: Output's recommended fix for the IDOR uses an authorisation check (server-side ownership verification from the authenticated user, not just a where-clause) — met. Step 3 A01 states "verify that the code checks whether the authenticated user owns or has access to that resource" — this is server-side ownership verification from the authenticated context, not a URL-trusting where-clause.
- [~] PARTIAL: Output acknowledges positive security practices — partially met. Same as Criteria item 8: the structural requirement (mandatory "Positive findings" section, Rules directive) is present; substance depends on what the scenario's files actually contain. Score: 0.5.

## Notes

The skill is methodologically strong. Confidence calibration in Step 5 is the standout — worked examples and the "never HIGH from grep alone" rule prevent the most common audit failure mode. The mandatory data flow map before vulnerability scanning is the right ordering and it is structurally enforced, not just advised.

The one material gap is CWE references. The test's Output expectations criterion 8 asks for CWE-89 and CWE-639 explicitly, but the Step 6 findings table schema does not include a CWE column. A well-formed output would likely mention CWEs in the Finding or Category text given the OWASP-to-CWE mapping, but it is not structurally required by the skill. Adding a CWE column to the findings table would close this gap cleanly.

The related skills references (`/security-engineer:threat-model`, `/security-engineer:dependency-audit`) assume those plugins are installed — worth flagging as soft dependencies for marketplace consumers.
