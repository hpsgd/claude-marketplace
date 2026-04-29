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

## Output expectations

- [ ] PASS: Output evaluates all 15 template criteria for the devops agent — none skipped, none assumed
- [ ] PASS: Output scores each criterion as MET / PARTIALLY MET / MISSING with a specific evidence reference (file path, line number, or quoted text) for non-MET findings
- [ ] PASS: Output reports the quality score as `X/15` and the actual line count of the devops agent file, with the 150-300 line target band stated
- [ ] PASS: Output verifies the model is `sonnet` (specialist agent) — flags as MISSING / wrong if it's `opus` or absent from the frontmatter
- [ ] PASS: Output's tool-links criterion checks the agent body for third-party tool mentions (e.g. Terraform, Docker, GitHub Actions) and confirms each has a markdown hyperlink on first mention
- [ ] PASS: Output's frontmatter description check verifies the description includes the role, domain summary, and trigger conditions — quoting the actual description and flagging missing elements
- [ ] PASS: Output's recommended actions are prioritised — structural gaps (missing Pre-Flight, missing Failure Caps, missing Decision Checkpoints) before content gaps (sparse domain methodology) before style (line-count outside band, banned words)
- [ ] PASS: Output checks for private references / company names that shouldn't appear in a marketplace plugin
- [ ] PASS: Output verifies all mandatory sections per template are present — Core, Non-negotiable, Pre-Flight, Output Format, Failure Caps, Decision Checkpoints, Collaboration, Principles, What You Don't Do
- [ ] PARTIAL: Output identifies any genuine gaps relative to peer specialist agents (e.g. compares devops sections against architect or ai-engineer for parity in depth)
