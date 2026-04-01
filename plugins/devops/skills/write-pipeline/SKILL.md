---
name: write-pipeline
description: Write a CI/CD pipeline configuration — build, test, lint, deploy stages.
argument-hint: "[service or project to create pipeline for, and platform e.g. 'GitHub Actions']"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Write a CI/CD pipeline for $ARGUMENTS.

## Standard stages

1. **Lint & format check** — run before tests (fast failure)
2. **Build** — compile, bundle, or containerise
3. **Unit tests** — run first (fastest feedback)
4. **Integration tests** — run after unit tests pass
5. **Security scan** — dependency audit, SAST
6. **Deploy** — only on main branch, after all checks pass

## Rules

- Pipeline should fail fast — cheapest checks first
- Cache dependencies between runs (node_modules, .nuget, pip cache)
- Use matrix strategy for auto-discovery where possible (e.g., `infrastructure/*/Pulumi.yaml`)
- Pin action/tool versions for reproducibility
- Secrets via environment variables, never hardcoded
