# Test: security-review skill structure

Scenario: Checking that the security-review skill enforces all six mandatory scans in sequence, requires grep evidence for each scan, suppresses low-confidence findings, and produces CVSS-scored output.

## Prompt

Review the security-review skill definition and verify it produces systematic security assessments with evidence rather than intuition-based findings.

## Criteria

- [ ] PASS: Skill defines six mandatory scans in order — Input Validation, Injection, Auth/Authz, Secrets/Data Exposure, Dependencies, OWASP Top 10 — and states all are mandatory regardless of perceived applicability
- [ ] PASS: Skill provides grep patterns for each scan with specific patterns for the target languages (TypeScript, Python, C#)
- [ ] PASS: Skill includes a checklist per scan with pass criteria and the specific finding severity if the criterion is missing
- [ ] PASS: Skill's confidence calibration suppresses findings below 60% confidence — prohibits reporting speculative findings
- [ ] PASS: Skill requires an OWASP Top 10 compliance sweep as the final scan with PASS/FAIL per category and evidence
- [ ] PASS: Skill prohibits zero-finding rubber stamps — requires naming a specific positive assertion with file:line to prove review depth
- [ ] PASS: Skill output format includes Executive Summary (overall risk, finding counts, ship/fix/block recommendation), findings table, and scan evidence table
- [ ] PARTIAL: Skill addresses configuration security — mentions CORS, CSP, HSTS, and cookie flags as security controls to review
