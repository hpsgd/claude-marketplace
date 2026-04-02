# Security Review Report

| Field | Value |
|---|---|
| **Scope** | [Files, directories, or components reviewed] |
| **Date** | [YYYY-MM-DD] |
| **Reviewer** | [Name] |
| **Methodology** | 6-Scan Protocol + [OWASP ASVS 4.0](https://owasp.org/www-project-application-security-verification-standard/) Level [1/2/3] |
| **Status** | Draft / In Review / Final |

## Executive Summary

- **Overall risk level:** [Critical / High / Medium / Low]
- **Findings:** [X] Critical, [X] High, [X] Medium, [X] Low, [X] Informational
- **Top recommendation:** [Single most impactful action to reduce risk]

## Scope & Methodology

### Files Reviewed

- [List files, directories, or git diff range reviewed]
- [Total lines of code reviewed]
- [Language(s) and framework(s)]

### Scans Executed

| Scan | Description | Status |
|---|---|---|
| 1 — Input Validation | All external inputs validated at boundary | [Completed / Partial / Skipped + reason] |
| 2 — Injection | No user input reaches interpreters without parameterisation | [Completed / Partial / Skipped + reason] |
| 3 — Authentication & Session | Auth mechanisms verified, session management reviewed | [Completed / Partial / Skipped + reason] |
| 4 — Access Control | Authorisation enforced at every endpoint | [Completed / Partial / Skipped + reason] |
| 5 — Cryptography & Secrets | No hardcoded secrets, appropriate algorithms | [Completed / Partial / Skipped + reason] |
| 6 — Configuration & Dependencies | Secure defaults, no known vulnerable dependencies | [Completed / Partial / Skipped + reason] |

### Tools Used

- [e.g. Static analysis tool and version]
- [e.g. Dependency scanner and version]
- [e.g. Manual code review]

### ASVS Coverage

- **Target level:** [1 — Opportunistic / 2 — Standard / 3 — Advanced]
- **Categories assessed:** [e.g. V2 Authentication, V5 Validation, V8 Data Protection]
- **Requirements checked:** [e.g. 45 of 286 total ASVS requirements]

## Findings

| ID | Severity | Confidence | STRIDE | CWE | Description | Location | Recommendation |
|---|---|---|---|---|---|---|---|
| SEC-001 | [Critical/High/Medium/Low/Info] | [High/Medium/Low] | [S/T/R/I/D/E] | [CWE-XXX](https://cwe.mitre.org/data/definitions/XXX.html) | [What the vulnerability is and why it matters] | `file:line` | [Specific fix or remediation step] |

## OWASP Top 10 Coverage

| Category | Checked | Findings |
|---|---|---|
| A01:2021 — Broken Access Control | [Yes/No] | [Finding IDs or "None"] |
| A02:2021 — Cryptographic Failures | [Yes/No] | [Finding IDs or "None"] |
| A03:2021 — Injection | [Yes/No] | [Finding IDs or "None"] |
| A04:2021 — Insecure Design | [Yes/No] | [Finding IDs or "None"] |
| A05:2021 — Security Misconfiguration | [Yes/No] | [Finding IDs or "None"] |
| A06:2021 — Vulnerable Components | [Yes/No] | [Finding IDs or "None"] |
| A07:2021 — Auth Failures | [Yes/No] | [Finding IDs or "None"] |
| A08:2021 — Software & Data Integrity | [Yes/No] | [Finding IDs or "None"] |
| A09:2021 — Logging & Monitoring | [Yes/No] | [Finding IDs or "None"] |
| A10:2021 — SSRF | [Yes/No] | [Finding IDs or "None"] |

## Dependency Audit Summary

[Link to dependency audit report if run alongside, or "Not performed — run `/dependency-audit` separately"]

## Positive Observations

- [Security practice the codebase does well — e.g. consistent use of parameterised queries]
- [Good pattern worth preserving — e.g. centralised auth middleware]

## Prioritised Recommendations

| Priority | Recommendation | Findings Addressed | Effort | Risk Reduction |
|---|---|---|---|---|
| P1 | [Highest-impact remediation] | [SEC-XXX, SEC-XXX] | [Low/Medium/High] | [Critical/High/Medium] |
| P2 | [Next priority] | [SEC-XXX] | [Low/Medium/High] | [High/Medium/Low] |

## ASVS Compliance Summary (Optional)

| ASVS Category | Level Achieved | Gaps |
|---|---|---|
| [V2 — Authentication] | [1/2/3/None] | [Specific requirements not met] |
| [V5 — Validation] | [1/2/3/None] | [Specific requirements not met] |
