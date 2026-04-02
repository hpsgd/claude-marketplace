---
name: audit-skill
description: "Audit a skill definition against the standard template. Reports structural gaps and recommended fixes."
argument-hint: "[skill name, parent agent, or 'all' to audit every skill]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Audit $ARGUMENTS against the skill template quality criteria.

## Process

### Step 1: Read the template

```
Read(file_path="plugins/practices/plugin-curator/templates/skill-template.md")
```

### Step 2: Read the skill(s) to audit

If `$ARGUMENTS` is "all", find every skill:
```bash
find plugins -name 'SKILL.md' | sort
```

### Step 3: Check each quality criterion

For each skill, check all 11 criteria from the template. Score as ✅ (met), ⚠️ (partially met), or ❌ (missing).

Also check:
- Is the skill self-contained? (works without reading parent agent)
- Does it reference related skills where appropriate?
- Are there empty SKILL.md placeholder directories? (flag for creation)

### Step 4: Report

When auditing "all", produce a summary table:

```markdown
| Skill | Agent | Lines | Score | Top issue |
|---|---|---|---|---|
| {name} | {parent} | {N} | {X}/11 | {issue} |
```

Flag empty skill directories separately:

```markdown
### Empty Skill Directories (need SKILL.md written)
- {agent}/{skill-name}
```
