---
description: Moon monorepo manager conventions — task orchestration, tags, generators, hooks
paths:
  - "**/.moon/**"
  - "**/moon.yml"
---

# Moon Monorepo Conventions

## Task orchestration
- Always use `moon run` instead of running tools directly (not `npx`, not `dotnet`, not `npm run`)
- Projects are referenced by their `id` field in `moon.yml`, not their directory name

```sh
moon run '@org/web/app:check'  # Run checks for a specific project
moon run '@org/ui:check'          # Run checks for shared UI
moon check                            # Run all checks across all projects
moon query tasks                      # List all available tasks
```

## Two-layer task system

1. **Global tasks** (`.moon/tasks.yml`) — abstract lifecycle commands (`init`, `build`, `dev`, `check`, `format`, `start`) that delegate to optional sub-tasks via `deps`
2. **Tag-based tasks** (`.moon/tasks/tag-*.yml`) — tool-specific implementations. A project opts in by adding tags to its `moon.yml` (e.g., `tags: [eslint, nextjs, prettier, storybook, vitest]`)

| Task     | What it does                                                   |
| -------- | -------------------------------------------------------------- |
| `init`   | Installs dependencies (`npm install`)                          |
| `build`  | Builds the project (Next.js + Storybook if tagged)             |
| `dev`    | Runs the dev server                                            |
| `check`  | Runs all checks: `check/prettier`, `check/eslint`, `check/tsc` |
| `format` | Auto-fixes: `format/prettier`, `format/eslint`                 |
| `start`  | Runs production server                                         |

## Git hooks via Moon

Moon manages git hooks via `.moon/workspace.yml`:
- **pre-commit**: `moon run :check --affected --status=staged` (lint, format-check, typecheck staged files)
- **commit-msg**: commitlint enforces Conventional Commits format

After cloning or pulling changes to hook config:
```sh
moon sync hooks
```

## Generators

Moon generators produce device-specific configuration files (e.g., `.mcp.json` with full project paths):
```sh
moon templates         # List available generators
moon generate <name>   # Run a generator
```

## MCP integration
Moon MCP server configured in `.mcp.json` for Claude Code integration (generated via `moon generate mcp.json`).
