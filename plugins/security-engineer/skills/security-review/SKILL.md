---
name: security-review
description: Review code or configuration for security vulnerabilities — OWASP Top 10, secrets, auth, injection.
argument-hint: "[file, directory, or git diff range to review]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Security review $ARGUMENTS.

## Checks

- **Injection** — SQL, NoSQL, command, LDAP. Parameterised queries? No string concatenation?
- **Authentication** — secure session handling, password hashing (bcrypt/argon2), rate limiting
- **Authorisation** — checked on every request, not just UI level. No IDOR vulnerabilities
- **Data exposure** — no secrets in code, no PII in logs, encryption at rest and in transit
- **XSS** — output escaped, CSP headers, no `dangerouslySetInnerHTML` without sanitisation
- **CSRF** — anti-CSRF tokens on state-changing requests
- **Dependencies** — known CVEs in dependencies? Is the vulnerable code path reachable?
- **Configuration** — debug mode off, default credentials removed, CORS properly scoped
- **Secrets** — grep for API keys, tokens, passwords in code. Check `.env` files aren't committed

## Output

| Severity | Finding | Location | Recommendation |
|---|---|---|---|
| Critical/High/Medium/Low | Description | file:line | Fix |
