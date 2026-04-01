---
name: security-audit
description: Perform a security-focused audit of code changes or a specific area of the codebase
argument-hint: "[file path, directory, or git diff range]"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

Perform a focused security audit on the specified code. If no argument is provided, audit staged changes (`git diff --staged`).

## Audit process

### 1. Scope identification
- Identify all files in scope based on the argument
- Map data flows: where does user input enter? Where does it leave the system?

### 2. Vulnerability scan
Check for each OWASP Top 10 category:

- **Injection** (SQL, NoSQL, OS command, LDAP): Search for string concatenation in queries, `exec`/`eval` usage, unparameterized queries
- **Broken authentication**: Weak password policies, missing rate limiting, insecure session handling
- **Sensitive data exposure**: Plaintext secrets, missing encryption, excessive logging of PII
- **XXE**: XML parsing without disabling external entities
- **Broken access control**: Missing authorization checks, IDOR vulnerabilities, privilege escalation paths
- **Security misconfiguration**: Debug mode enabled, default credentials, overly permissive CORS
- **XSS**: Unescaped output, `dangerouslySetInnerHTML`, missing CSP headers
- **Insecure deserialization**: Untrusted data deserialized without validation
- **Using components with known vulnerabilities**: Outdated dependencies with CVEs
- **Insufficient logging**: Security events not logged, logs containing sensitive data

### 3. Additional checks
- Hardcoded secrets or API keys (grep for common patterns)
- Insecure randomness (Math.random for security purposes)
- Race conditions in authentication or authorization flows
- Missing input validation at API boundaries

## Output format

Report findings as:

| Severity | Finding | Location | Recommendation |
|----------|---------|----------|----------------|
| Critical/High/Medium/Low | Description | file:line | How to fix |

End with a summary of the overall security posture and top priorities.
