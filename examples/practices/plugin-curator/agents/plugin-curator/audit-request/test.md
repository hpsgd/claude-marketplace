# Test: plugin-curator audit request

Scenario: User asks the plugin-curator agent to audit an existing agent definition for structural consistency, expecting a structured report against the template criteria.

## Prompt

Can you audit the `qa` agent for me? I want to know if it's structurally consistent with the template — whether it's got all the required sections, the right model, no private references, that kind of thing. Just give me the full breakdown.

## Criteria

- [ ] PASS: Agent reads CLAUDE.md and marketplace.json as part of its mandatory pre-flight before beginning the audit
- [ ] PASS: Agent reads the agent template file before evaluating the qa agent definition
- [ ] PASS: Audit output includes a criteria table covering all 15 quality criteria from the template
- [ ] PASS: Each criterion is scored as met, partially met, or missing — not left blank or assumed
- [ ] PASS: Non-passing criteria include specific evidence (file reference, line number, or exact quote) rather than vague descriptions
- [ ] PASS: Audit output includes a quality score (X/15 format) and line count
- [ ] PASS: Audit includes recommended actions prioritised by impact
- [ ] PARTIAL: Boundary check — agent does not audit itself (plugin-curator is explicitly excluded from "all" audits per the skill's anti-patterns)

## Output expectations

- [ ] PASS: Output's audit table covers all 15 quality criteria from the agent template — not a subset, not a generic checklist
- [ ] PASS: Output scores each criterion as MET / PARTIALLY MET / MISSING (or equivalent ternary) — never blank, never "assumed met"
- [ ] PASS: Output's non-passing criteria each include specific evidence — file reference, line number, or exact quote from the qa agent definition — not vague descriptions like "frontmatter could be better"
- [ ] PASS: Output reports the quality score as `X/15` and the line count of the audited agent — both numeric, not approximate
- [ ] PASS: Output checks model correctness — qa is a specialist agent that should use `sonnet`, not `opus` — and flags as a finding if mismatched
- [ ] PASS: Output's recommended actions are prioritised — structural gaps (missing required sections) before content gaps (sparse rules) before style issues (line length, banned words) — with severity per action
- [ ] PASS: Output reads CLAUDE.md, marketplace.json, and the agent template before evaluating the qa agent — pre-flight is shown explicitly as a step or evidence in the output
- [ ] PASS: Output checks for private references / company names that shouldn't appear in a public marketplace plugin definition
- [ ] PASS: Output checks tool-link conventions — third-party tools mentioned in prose have markdown hyperlinks on first mention
- [ ] PARTIAL: Output's recommendations are concrete — each action specifies what to add or change, not "improve this section"
