---
name: create-agent
description: "Create a new agent plugin following the standard template. Handles directory structure, plugin.json, agent definition, marketplace.json, README, and RATSI updates."
argument-hint: "[agent name and brief description of its role]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Create a new agent plugin for $ARGUMENTS.

## Process

### Step 1: Read the templates

```
Read(file_path="${CLAUDE_PLUGIN_ROOT}/templates/agent-template.md")
```

### Step 2: Determine category and create structure

Classify: `leadership/` (coordinates others), `product/` (customer-facing), `engineering/` (builds things), `practices/` (standards/methodology).

Create: `.claude-plugin/plugin.json`, `agents/{name}.md`, `skills/` (empty dirs for known skills), `templates/` (if applicable).

### Step 3: Write the agent following the template

Every section from the agent template is mandatory. Be opinionated — make decisions about the right way to work in this domain. 150-300 lines.

### Step 4: Update the registry chain

1. `marketplace.json` — add plugin entry
2. `README.md` — install commands (category block + everything block + JSON config), agent table
3. Coordinator RATSI — add to relevant activity rows
4. Lead agent (CTO/CPO) team listing — add to the appropriate lead's table

### Step 5: Verify

All JSON valid, no broken references, install commands match marketplace, plugin count matches registry.

## Output

The new agent plugin directory with all files, plus all registry updates.
