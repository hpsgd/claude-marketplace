# Claude Marketplace — Contributor Guide

## Structure

This repo is a Claude Code marketplace. Plugins are organised into two categories:

```
plugins/
├── foundations/         # Rules, standards, and methodology
│   ├── coding-standards/
│   ├── writing-style/
│   ├── security-compliance/
│   ├── thinking/
│   └── technology-stack/
└── agents/             # Role-based agents with skills
    ├── cpo/
    ├── product-owner/
    ├── designer/
    ├── architect/
    ├── react-developer/
    └── ...
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
- Use `foundations/` for plugins that provide rules, standards, or thinking methodology
- Use `agents/` for plugins that provide role-based agents with domain-specific skills
- Use the `scripts/install-rules.sh` helper for rule installation hooks

## Adding a new plugin

1. Create `plugins/<category>/<name>/.claude-plugin/plugin.json`
2. Add skills, agents, rules, and hooks as needed
3. Add an entry to `.claude-plugin/marketplace.json` with `source` pointing to the nested path (e.g., `agents/architect`)
4. Update `README.md` with usage instructions
