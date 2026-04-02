---
name: create-skill
description: "Create a new skill following the standard template. Handles SKILL.md creation, README update, and parent agent cross-reference."
argument-hint: "[skill name, parent agent, and brief description]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Create a new skill for $ARGUMENTS.

## Process

### Step 1: Read the template

```
Read(file_path="${CLAUDE_PLUGIN_ROOT}/templates/skill-template.md")
```

### Step 2: Create the skill directory and SKILL.md

`plugins/{category}/{agent}/skills/{skill-name}/SKILL.md`

Follow the skill template: frontmatter, purpose, sequential mandatory steps, rules, output format. 100-300 lines. Self-contained — works without reading the parent agent.

### Step 3: Update README

Add skill to the parent agent's row in the agent table.

### Step 4: Verify

Skill is self-contained, references related skills where appropriate, uses generic examples.
