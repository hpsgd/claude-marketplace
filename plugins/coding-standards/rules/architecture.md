---
description: General architecture principles — applies across all languages and frameworks
---

# Architecture Conventions

## General principles
- Keep files focused — one module, one responsibility
- Group related files by feature or domain, not by type
- Keep the dependency graph shallow — avoid deep import chains

## Documentation
- Each workspace or service should have its own CLAUDE.md with project-specific guidance
- Services in separate languages/runtimes get their own CLAUDE.md (not just the monorepo root)
- Shared configuration packages (eslint-config, prettier-config) should document their presets and usage

## Shared configuration
- Shared presets for linting and formatting in dedicated packages
- Each project's config is a one-liner re-export of the shared preset
- Shared component libraries consumed as source (no build step)

## Content management
- Use typed content collections for structured content (markdown + frontmatter)
- Content accessed via typed helpers, not raw file reads
- Prose content in content files, structured data can remain as const arrays in code
- Shared content packages (e.g., legal pages, policies) with per-app override by slug
