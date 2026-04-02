Audit all skill definitions in this marketplace against the standard template.

Read the skill template at ${CLAUDE_PLUGIN_ROOT}/templates/skill-template.md to understand the quality criteria.

Find every skill file:
```bash
find plugins -name 'SKILL.md' | sort
```

For each skill, check these criteria:
1. 100-500 lines
2. Description specific enough for auto-invocation matching
3. Self-contained (works without reading parent agent)
4. Sequential mandatory steps
5. Each step produces a verifiable output
6. Rules section with imperatives and anti-patterns
7. Structured output format
8. References related skills where appropriate
9. Generic examples only (no private references)
10. External tools linked on first mention
11. argument-hint present
12. Frontmatter description precise enough for auto-invocation

Produce a summary table:

| Agent | Skill | Lines | Score | Top issue |
|---|---|---|---|---|
| {parent} | {name} | {N} | {X}/12 | {issue} |

Sort by agent name, then skill name within each agent.

Flag empty skill directories (placeholder dirs without SKILL.md content).
