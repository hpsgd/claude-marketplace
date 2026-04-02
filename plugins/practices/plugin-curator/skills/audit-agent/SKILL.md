---
name: audit-agent
description: "Audit an agent definition against the standard template. Reports structural gaps, inconsistencies, and recommended fixes."
argument-hint: "[agent name, or 'all' to audit every agent]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Audit $ARGUMENTS against the agent template quality criteria.

## Process

### Step 1: Read the template

```
Read(file_path="plugins/practices/plugin-curator/templates/agent-template.md")
```

### Step 2: Read the agent(s) to audit

If `$ARGUMENTS` is "all", find every agent:
```bash
find plugins -path '*/agents/*.md' -not -path '*/plugin-curator/*' | sort
```

### Step 3: Check each quality criterion

For each agent, check all 14 criteria from the template. Score as ✅ (met), ⚠️ (partially met), or ❌ (missing).

### Step 4: Report

Use the audit output format from the plugin-curator agent. Prioritise fixes: structural gaps > content gaps > style issues.

When auditing "all", produce a summary table first:

```markdown
| Agent | Lines | Score | Top issue |
|---|---|---|---|
| {name} | {N} | {X}/14 | {most important fix} |
```

Then detailed findings for agents scoring below 12/14.
