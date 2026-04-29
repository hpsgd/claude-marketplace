# Output: security-review skill structure

**Verdict:** PASS
**Score:** 15.5/16 criteria met (97%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill defines six mandatory scans in order — Input Validation, Injection, Auth/Authz, Secrets/Data Exposure, Dependencies, OWASP Top 10 — and states all are mandatory regardless of perceived applicability — met: "## 6-Scan Protocol (sequential — every scan is MANDATORY)" with "Do not skip a scan because you think it doesn't apply"
- [x] PASS: Skill provides grep patterns for each scan with specific patterns for the target languages (TypeScript, Python, C#) — met: Scans 1-4 each have language-specific grep blocks covering .ts/.tsx, .py, .cs; Scan 5 uses per-ecosystem audit tool invocations
- [x] PASS: Skill includes a checklist per scan with pass criteria and the specific finding severity if the criterion is missing — met: each scan has a table with columns "Check", "Pass criteria", "Finding if missing" with explicit severity labels
- [x] PASS: Skill's confidence calibration suppresses findings below 60% confidence — prohibits reporting speculative findings — met: calibration table states LOW (below 60) = "NO — suppress. Do not report speculative findings", reinforced by explicit rule
- [x] PASS: Skill requires an OWASP Top 10 compliance sweep as the final scan with PASS/FAIL per category and evidence — met: Scan 6 is positioned last with a full A01-A10 table including Status and Evidence columns
- [x] PASS: Skill prohibits zero-finding rubber stamps — requires naming a specific positive assertion with file:line to prove review depth — met: Anti-Patterns section states this explicitly
- [x] PASS: Skill output format includes Executive Summary (overall risk, finding counts, ship/fix/block recommendation), findings table, and scan evidence table — met: output template defines all three; Executive Summary has all three fields; findings table includes Severity, Confidence, STRIDE, Location; Scan Evidence table covers all six scans
- [~] PARTIAL: Skill addresses configuration security — mentions CORS, CSP, HSTS, and cookie flags as security controls to review — partially met: all four are named in the Anti-Patterns section ("CORS, CSP, HSTS, cookie flags are security controls. Review them") but there is no dedicated scan step, grep patterns, or checklist table for configuration; it is a single prohibition bullet, not structured guidance

### Output expectations

- [x] PASS: Output is structured as a verification of the skill (verdict per requirement) rather than running an actual security review — met: this result evaluates the skill definition against the rubric
- [x] PASS: Output verifies the six mandatory scans in order and confirms all are mandatory regardless of perceived applicability — met: confirmed in Criteria row 1 above with direct SKILL.md references
- [x] PASS: Output verifies grep patterns are provided per scan and per language — not language-agnostic regex that misses idioms — met: patterns are language-specific across TypeScript, Python, C#; noted that Python `eval()` is absent from injection patterns (see Notes)
- [x] PASS: Output confirms each scan has a checklist with pass criteria AND the specific finding severity to assign if the criterion is missing — met: every scan checklist table has a "Finding if missing" column with severity labels and file:line placeholders
- [x] PASS: Output verifies the confidence calibration rule — findings below 60% confidence are suppressed — with anti-FUD reasoning — met: calibration table and rules section both cover suppression; "Noise erodes trust in the review" is the stated rationale
- [x] PASS: Output confirms the OWASP Top 10 sweep is the final scan with PASS / FAIL per category and grep evidence for each — met: Scan 6 is last, has PASS/FAIL and Evidence columns for all 10 categories
- [x] PASS: Output verifies the no-rubber-stamp rule for clean reviews — must name a specific positive assertion with file:line proving review depth — met: Anti-Patterns section covers this directly
- [x] PASS: Output confirms the output format includes Executive Summary, findings table with CVSS, and scan evidence table with grep commands and result counts — met: Executive Summary and findings table confirmed; Scan Evidence table has patterns searched and finding counts; note the template column shows "Patterns searched" as a description, not the literal grep commands
- [~] PARTIAL: Output identifies any genuine gaps — met: three real gaps are identified: (1) no escalation guidance for when to commission a pen test, (2) no explicit policy on test/fixture code (Scan 4 silently excludes `test` paths from secret detection without flagging the risk that test fixtures can ship to prod), (3) Python `eval()`/`exec()` not covered by injection grep patterns

## Notes

The skill is well-structured and substantive. Three gaps worth flagging:

Scan 4 grep for hardcoded secrets excludes `test` paths with `grep -v "... test ..."`, which reduces noise but creates a blind spot: test fixtures containing real-looking secrets or actual credentials sometimes ship to production. The exclusion needs a companion note, not silent omission.

Python `eval()` and `exec()` are absent from the Scan 2 injection grep patterns. The patterns cover SQL, shell (`subprocess.call`), XSS (`mark_safe`, `Markup`), and path traversal, but dynamic evaluation is a common Python injection surface and is not addressed.

The Scan Evidence table in the output template uses a "Patterns searched" column that an agent could interpret loosely as a description rather than the literal grep commands. This undercuts the evidence-first intent of the scan protocol.
