Audit all agent definitions in this marketplace against the standard template.

Read the agent template at ${CLAUDE_PLUGIN_ROOT}/templates/agent-template.md to understand the 15 quality criteria.

Find every agent file:
```bash
find plugins -path '*/agents/*.md' -not -path '*/plugin-curator/*' | sort
```

For each agent, check these criteria:
1. 150-300 lines
2. Core statement (one paragraph explaining ownership)
3. Non-negotiable rules (specific, not vague)
4. Pre-Flight (reads CLAUDE.md and .claude/CLAUDE.md)
5. Domain methodology with mandatory steps
6. Structured output format (EXEMPT for leadership agents: coordinator, cpo, cto, grc-lead; and doc-writer agents whose methodology IS their output)
7. Failure caps (3-strike escalation)
8. Decision checkpoints (domain-specific triggers)
9. Collaboration table
10. Principles (5-10, opinionated)
11. "What You Don't Do" (names who DOES own it)
12. No private references
13. External tools linked on first mention (N/A if agent doesn't mention specific tools in prose)
14. Correct model (sonnet for specialists, opus for leadership)
15. Frontmatter description precise enough for auto-invocation

**Evidence requirement:** Every non-passing criterion MUST include specific evidence:
- What was looked for
- What was found or not found
- Where (line number if applicable)

For the links criterion: list each unlinked tool mention with its line number, e.g., "Line 199: 'dbt' mentioned without hyperlink". Do NOT just say "links" — always cite the specific tool and location.

Produce a summary table:

| Agent | Lines | Score | Status |
|---|---|---|---|
| {name} | {N} | {X}/15 | ✅ or {specific finding with evidence} |

Then detailed findings for any agent not at 15/15.
