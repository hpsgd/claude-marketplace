---
name: audit-agent
description: "Audit an agent definition against the standard template. Reports structural gaps with specific evidence for each finding."
argument-hint: "[agent name, or 'all' to audit every agent]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Audit $ARGUMENTS against the agent template quality criteria.

## Process

### Step 1: Read the template

```
Read(file_path="${CLAUDE_PLUGIN_ROOT}/templates/agent-template.md")
```

### Step 2: Read the agent(s) to audit

If `$ARGUMENTS` is "all", find every agent:
```bash
find plugins -path '*/agents/*.md' -not -path '*/plugin-curator/*' | sort
```

### Step 3: Check each quality criterion

For each agent, check all 15 criteria from the template. Score as ✅ (met), ⚠️ (partially met — with reason), or ❌ (missing).

**Exemptions:**
- Output format: N/A for leadership agents (coordinator, cpo, cto, grc-lead) and doc-writer agents — they coordinate or their methodology IS the output
- Tool links: N/A if the agent doesn't mention specific external tools in prose. If marked down, cite the SPECIFIC unlinked tool reference (line number and tool name)

**Evidence requirement:** Every non-passing criterion MUST include:
- What was looked for (the criterion)
- What was found or not found (the specific evidence)
- Where it was found or expected (file location, line number if applicable)

For the links criterion specifically: list each unlinked tool mention with its line number, e.g., "Line 199: 'dbt' mentioned without hyperlink"

### Step 4: Report

When auditing "all", produce a summary table first:

```markdown
| Agent | Lines | Score | Status |
|---|---|---|---|
| {name} | {N} | {X}/15 | ✅ or {specific issue with evidence} |
```

Then for any agent not at 15/15, provide detail:

```markdown
### {agent-name} — {X}/15

| Criterion | Status | Evidence |
|---|---|---|
| {criterion} | ❌ | {what was expected, what was found, where} |
```

Do NOT report vague issues like "links" — always include the specific tool name and line number that triggered the finding.
