# Output: web-assessment skill structure

**Verdict:** PARTIAL
**Score:** 16.5/18 criteria met (92%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill requires logging authorisation reference, target URL/scope, environment (prod/staging/test), testing restrictions, and a contact for critical findings before any active testing begins — pre-assessment checklist covers all five elements before Step 1
- [x] PASS: Skill covers authentication assessment — credential testing, account enumeration via error messages, lockout policy, MFA bypass, and password reset flow token quality — all present in Step 2
- [x] PASS: Skill covers session management — token entropy (128+ bits), cookie attributes (HttpOnly, Secure, SameSite), and session invalidation on logout and password change — all present in Step 3
- [x] PASS: Skill covers authorisation — horizontal IDOR with concrete ID-swap example (`/api/orders/12345` → `12346`) and vertical escalation via admin-request-replay pattern
- [x] PASS: Skill covers input validation for SQL injection, XSS (reflected, stored, DOM-based), SSRF, XXE, and command injection with specific test payloads
- [x] PASS: Skill covers security headers with a bash command (`curl -I -s "[URL]" | grep -i -E ...`) and a five-row table of expected values and risk if absent
- [x] PASS: Skill requires immediate reporting of critical findings — Rules section states "Report critical findings immediately — don't wait for the full assessment to complete"
- [~] PARTIAL: Skill addresses API security — exposed documentation (/api/docs, /swagger, /openapi.json), mass assignment, rate limiting, and verbose error messages all named, but no concrete test payloads or commands provided (unlike Steps 5 and 6)

### Output expectations

- [x] PASS: Output logs the authorisation reference, exact target (https://hps.gd), environment (production), testing restriction (no destructive testing), and critical-finding contact (security@hps.gd) before active checks — the output format template places all engagement metadata at the top, and the pre-assessment checklist is the first action item
- [x] PASS: Output's authentication assessment runs concrete checks — credential brute force boundary, account enumeration via login error variation, lockout threshold, MFA bypass attempts, password reset token entropy and reuse — all covered with specific test descriptions
- [x] PASS: Output's session management assessment inspects cookie flags (HttpOnly, Secure, SameSite), token entropy, and session invalidation on logout AND password change — all explicitly listed in Step 3
- [x] PASS: Output's authorisation assessment includes IDOR test patterns — incrementing IDs, swap while authenticated as a different user, and admin-request-replay for vertical escalation — all present
- [x] PASS: Output's input validation tests cover SQL injection (`'`, `' OR '1'='1`, DROP TABLE), reflected/stored/DOM XSS (payload + source audit), SSRF (169.254.169.254, localhost), XXE (DOCTYPE/ENTITY payload), and command injection (`; id`, `| id`, `&& id`) — each with a representative payload
- [x] PASS: Output's security headers check uses a concrete bash command and an expected-values table — both present and well-formed
- [x] PASS: Output flags critical findings immediately — Rules section is explicit; the output format template could include a dedicated critical-findings callout section but the instruction is unambiguous
- [ ] FAIL: Output adheres to the no-destructive-testing scope — the skill lists `'; DROP TABLE` as a SQL injection payload with only a parenthetical "(in non-production only)" qualifier; no mechanism exists to suppress or gate this payload when the skill is invoked against a production target with explicit no-destructive-testing scope
- [x] PASS: Output's API security section covers exposed Swagger/OpenAPI documentation, mass assignment via extra JSON fields, rate limit observability, and verbose error messages leaking stack traces
- [x] PASS: Output stays within agreed scope — output format template includes "Out-of-scope observations" section; Rules section states "if you find a vulnerability that leads outside the agreed scope, note it and ask before following up"

## Notes

The skill is well-structured and covers all major OWASP assessment areas with good specificity. The single clear gap is destructive payload handling: `'; DROP TABLE` appears in the SQL injection section with a parenthetical "(in non-production only)" qualifier, but the skill has no conditional logic or warning mechanism to suppress or flag this payload when the environment is production and the scope explicitly excludes destructive testing. A production + no-destructive-testing invocation should either omit those payloads or display a visible warning at the point they are listed.

The API security section (Step 7) is functionally correct but thinner than the other assessment steps — it names the right concerns without providing equivalent concrete commands or payloads. A mass assignment example (`"role": "admin"` added to a registration body) and a command to probe for exposed OpenAPI endpoints would bring it in line with Steps 5 and 6.
