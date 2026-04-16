# Test: audit-agent single agent full evaluation

Scenario: A contributor asks for a full audit of the `devops` agent to check structural consistency before proposing it for the marketplace.

## Prompt

/audit-agent devops

## Criteria

- [ ] PASS: Step 1 reads the agent template file before evaluating the devops agent — uses the template criteria as the audit checklist
- [ ] PASS: All 15 criteria are evaluated and scored (met, partially met, or missing) — none left blank
- [ ] PASS: Every non-passing criterion includes specific evidence: what was looked for, what was found or not found, and where (file location or line number)
- [ ] PASS: Output includes quality score in X/15 format and line count with the 150-300 line target
- [ ] PASS: Model correctness is checked — devops is a specialist agent and should use sonnet, not opus
- [ ] PASS: Tool links criterion checks that external tools mentioned in prose have markdown hyperlinks on first mention
- [ ] PASS: Recommended actions are prioritised — structural gaps listed before content gaps before style issues
- [ ] PARTIAL: Frontmatter description precision criterion checks that the description includes role, domain summary, and trigger conditions in the required format
