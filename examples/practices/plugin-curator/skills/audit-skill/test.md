# Test: audit-skill stub detection

Scenario: A contributor asks for an audit of a specific skill that turns out to be a near-stub — correct frontmatter but minimal body content with no structured output format or rules section.

## Prompt

/audit-skill performance-profile (performance-engineer)

(The skill has valid frontmatter with a good description and argument-hint, an opening paragraph, and a single vague step saying "Profile the endpoint using your preferred tool and look for bottlenecks." No rules section, no output format template, no anti-patterns. 34 lines total.)

## Criteria

- [ ] PASS: Step 1 reads the skill template before evaluating — uses template criteria as the audit checklist
- [ ] PASS: All 12 criteria are evaluated and scored — none skipped or assumed
- [ ] PASS: Line count of 34 is correctly classified as a Stub (below 50 lines) — not scored as "Needs expansion"
- [ ] PASS: Missing structured output format is flagged with evidence: "skill ends after the single step with no markdown template"
- [ ] PASS: Missing rules/anti-patterns section is flagged as absent — a note about "preferred tool" is not a rule
- [ ] PASS: Self-containment is evaluated — "look for bottlenecks" without specifying how fails the self-contained criterion
- [ ] PASS: Overall state is classified as Stub (not Complete or Needs expansion) with the correct action: "Full rewrite needed"
- [ ] PARTIAL: Recommended actions include specific guidance on what the rewrite must include — not just "write more content"
