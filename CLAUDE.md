# Claude Marketplace — Contributor Guide

## Structure

This repo is a Claude Code marketplace. Each plugin lives in `plugins/<name>/` and follows this layout:

```
plugins/<name>/
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

- Never put anything except `plugin.json` inside `.claude-plugin/`
- Skills, agents, hooks, and rules go at the plugin root level
- Rules in `rules/` are instruction files installed into consuming projects via the SessionStart hook
- Skills in `skills/` are for context-specific guidance that Claude auto-invokes
- Register every new plugin in the root `.claude-plugin/marketplace.json`
- Use the `scripts/install-rules.sh` helper for rule installation hooks

## Adding a new plugin

1. Create `plugins/<name>/.claude-plugin/plugin.json`
2. Add skills, agents, rules, and hooks as needed
3. Add an entry to `.claude-plugin/marketplace.json`
4. Update `README.md` with usage instructions
