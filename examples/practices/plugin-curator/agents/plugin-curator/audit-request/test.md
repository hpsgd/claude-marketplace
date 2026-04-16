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
