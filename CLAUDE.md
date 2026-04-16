# Claude Marketplace — Contributor Guide

## Structure

This repo is a Claude Code marketplace. Plugins are organised by function:

```
plugins/
├── leadership/          # Coordinator, CPO, CTO, GRC Lead
├── product/             # Product owner, UI designer, UX researcher, technical writer, GTM, support, customer success
├── engineering/          # Architect, developers, QA, DevOps, security, data engineering, workflow tools
├── practices/           # Coding standards, writing style, security compliance, thinking, technology stack
└── research/            # Business analyst, content analyst, open-source researcher, investigator, OSINT analyst
```

Each plugin follows this layout:

```
plugins/<category>/<name>/
├── .claude-plugin/plugin.json   # Required: plugin metadata
├── skills/                      # Optional: skills (invokable or auto-triggered)
│   └── <skill-name>/SKILL.md
├── agents/                      # Optional: subagent definitions
│   └── <agent-name>.md
├── rules/                       # Optional: installable instruction files
│   └── <topic>.md
├── hooks/                       # Optional: lifecycle hooks
│   └── hooks.json
└── templates/                   # Optional: template files
```

## Key conventions

- Never put anything except `plugin.json` (and `marketplace.json` at root) inside `.claude-plugin/`
- Skills, agents, hooks, rules, and templates go at the plugin root level
- Rules in `rules/` are instruction files installed into consuming projects via the SessionStart hook
- Skills in `skills/` are for context-specific guidance that Claude auto-invokes
- Register every new plugin in `.claude-plugin/marketplace.json`
- Use `leadership/` for coordination and C-level agents
- Use `product/` for customer-facing and product-related agents
- Use `engineering/` for technical implementation agents
- Use `practices/` for standards, conventions, and methodologies
- Use `research/` for research, analysis, and investigation agents
- Use the `scripts/install-rules.sh` helper for rule installation hooks

## Adding a new plugin

1. Create `plugins/<category>/<name>/.claude-plugin/plugin.json`
2. Add skills, agents, rules, and hooks as needed
3. Add an entry to `.claude-plugin/marketplace.json` with `source` pointing to the nested path (e.g., `engineering/architect`)
4. Update `README.md` with usage instructions
