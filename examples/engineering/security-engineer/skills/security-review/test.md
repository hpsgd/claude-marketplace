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

## Output expectations

- [ ] PASS: Output is structured as a verification of the skill (verdict per requirement) rather than running an actual security review
- [ ] PASS: Output verifies the six mandatory scans in order — Input Validation, Injection, Auth/Authz, Secrets/Data Exposure, Dependencies, OWASP Top 10 — and confirms all are mandatory regardless of perceived applicability
- [ ] PASS: Output verifies grep patterns are provided per scan and per language (TypeScript, Python, C#) — not language-agnostic regex that misses idioms like `Marshal.unsafeRunSync` or Python's `eval`
- [ ] PASS: Output confirms each scan has a checklist with pass criteria AND the specific finding severity to assign if the criterion is missing — not just a list of things to look for
- [ ] PASS: Output verifies the confidence calibration rule — findings below 60% confidence are suppressed — with the underlying anti-FUD reasoning
- [ ] PASS: Output confirms the OWASP Top 10 sweep is the final scan with PASS / FAIL per category and grep evidence for each
- [ ] PASS: Output verifies the no-rubber-stamp rule for clean reviews — must name a specific positive assertion with file:line proving review depth, not "looks good"
- [ ] PASS: Output confirms the output format includes Executive Summary (overall risk, finding counts, ship/fix/block recommendation), findings table with CVSS, and scan evidence table with grep commands and result counts
- [ ] PARTIAL: Output identifies any genuine gaps — e.g. no rule on threat modelling for new features, no guidance on when to escalate to a full pen test, or no explicit handling of test/fixture code (which often has lower bar but can ship to prod)
