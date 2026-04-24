# Turtlestack — Contributor Guide

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
├── rules/                       # Optional: instruction files (installed by thinking plugin hook)
│   └── <topic>.md
├── hooks/                       # Optional: lifecycle hooks
│   └── hooks.json
└── templates/                   # Optional: template files
```

## Key conventions

- Never put anything except `plugin.json` (and `marketplace.json` at root) inside `.claude-plugin/`
- Skills, agents, hooks, rules, and templates go at the plugin root level
- Rules in `rules/` are instruction files installed into `.claude/rules/` by the thinking plugin's SessionStart hook
- Skills in `skills/` are for context-specific guidance that Claude auto-invokes
- Register every new plugin in `.claude-plugin/marketplace.json`
- Use `leadership/` for coordination and C-level agents
- Use `product/` for customer-facing and product-related agents
- Use `engineering/` for technical implementation agents
- Use `practices/` for standards, conventions, and methodologies
- Use `research/` for research, analysis, and investigation agents
- The `thinking` plugin's SessionStart hook installs rules from all enabled plugins into `.claude/rules/` as `<marketplace>--<plugin>--<version>--<filename>.md`
- **`thinking` must be enabled** for any plugin's rules to be installed — it is the rule delivery mechanism for the marketplace

## Adding a new plugin

1. Create `plugins/<category>/<name>/.claude-plugin/plugin.json`
2. Add skills, agents, rules, and hooks as needed
3. Add an entry to `.claude-plugin/marketplace.json` with `source` pointing to the nested path (e.g., `./plugins/engineering/architect`)
4. Update `README.md` with usage instructions
