# Test: Write architecture doc

Scenario: Testing whether the write-architecture-doc skill requires Mermaid diagrams, bounded context documentation, key decisions with rationale, and NFRs.

## Prompt


/internal-docs-writer:write-architecture-doc for our notification system — it handles in-app, email, and push notifications, with a queue-based delivery system and user preference management.

## Criteria


- [ ] PASS: Skill requires Mermaid diagrams for component architecture — not text descriptions of boxes and arrows
- [ ] PASS: Skill requires sequence diagrams for data flows — showing the temporal order of interactions, not just the components involved
- [ ] PASS: Skill documents key architectural decisions with rationale — why this approach was chosen, not just what was built
- [ ] PASS: Skill documents non-functional requirements (NFRs) — latency, throughput, availability — with specific targets
- [ ] PASS: Skill requires a research step before writing — reading existing code, configs, or ADRs
- [ ] PASS: Skill documents bounded contexts or system boundaries — what this system owns vs what it depends on externally
- [ ] PARTIAL: Skill documents known limitations or technical debt — partial credit if this section is mentioned but not required as mandatory
- [ ] PASS: Skill includes a quality checklist that verifies diagrams render and decisions are traceable
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields
