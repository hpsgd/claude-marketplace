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

## Output expectations

- [ ] PASS: Output classifies the performance-profile skill as a STUB (not "Complete" or "Needs expansion") given 34 lines, missing rules section, missing output format, and a single vague step
- [ ] PASS: Output's overall action recommendation is "Full rewrite needed" — not "fill in the missing sections" — given how little content is present
- [ ] PASS: Output evaluates all 12 template criteria — even ones that score MISSING, none skipped
- [ ] PASS: Output scores each criterion as MET / PARTIALLY MET / MISSING with specific evidence — e.g. "no `## Output Format` heading found in the file" not "output format is missing"
- [ ] PASS: Output's missing-output-format finding cites the exact symptom — "skill ends after the single step with no markdown template / no Output section heading" — not just "no output format"
- [ ] PASS: Output's self-containment evaluation flags "look for bottlenecks" / "preferred tool" as failing — explaining that another agent invoking this skill cannot proceed without external knowledge of what tools and what bottleneck patterns to look for
- [ ] PASS: Output's missing-rules-section finding distinguishes "soft guidance phrasing in prose" from a Rules section with anti-patterns — the casual mention of preferred tools is NOT a rules section
- [ ] PASS: Output reports the line count (34) and the target band (50-300 lines for a complete skill) explicitly, classifying 34 as below the stub threshold
- [ ] PASS: Output's rewrite recommendation includes specific guidance — what the rewritten skill must contain (multi-step process, named tools per stack, output format template with sections, anti-patterns list, rules) — not just "expand it"
- [ ] PARTIAL: Output references the related performance-engineer agent for context — the skill is owned by performance-engineer, so the rewrite should align with the parent agent's methodology and not duplicate it
