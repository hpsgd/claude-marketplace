---
description: General architecture principles — applies across all languages and frameworks
---

# Architecture Conventions

## General principles
- Keep files focused — one module, one responsibility
- Group related files by feature or domain, not by type
- Keep the dependency graph shallow — avoid deep import chains

## Naming consistency across contexts

When the same semantic operation exists in multiple modules or bounded contexts, use the same method name everywhere. Don't mix `fail()` in one context with `record_failed()` in another for the same operation. Pick one and apply it consistently.

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

## Trace the cascade before changing pipelines

Before finalising a change to any pipeline stage, trace every downstream consumer. Ask: "if this stage's output changes after the next stage already consumed it, what breaks?" A "complete" plan that doesn't trace downstream will miss consumers you forgot about (weekly summaries, backfill paths, notification hooks, projections).

This applies to event handlers, build pipelines, data flows, and any system where stages consume each other's output. Map the full graph before changing a node.

## Extract callables from day one

When logic will be called from more than one context (a CLI command, a handler, an agent prompt, a hook), extract it into a standalone callable with explicit arguments from the start. Don't embed it in the first caller and refactor later. The refactor never happens cleanly because each caller has already adapted to the embedded version's quirks.

A callable means: a script with CLI args, a function with typed parameters, or a module with a clear entry point. Not a prompt template. Not inline logic wrapped in a conditional.
