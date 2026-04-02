---
name: write-pipeline
description: Write a CI/CD pipeline configuration — build, test, lint, deploy stages.
argument-hint: "[service or project to create pipeline for, and platform e.g. 'GitHub Actions']"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Write a CI/CD pipeline for $ARGUMENTS.

## Process (sequential — do not skip steps)

### Step 1: Reconnaissance

Before writing any pipeline configuration:

1. **Identify the stack** — language, framework, package manager, test runner, linter
2. **Check existing pipelines** — look for `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `azure-pipelines.yml`
3. **Check existing scripts** — `package.json` scripts, `Makefile`, `Taskfile`, `scripts/` directory
4. **Identify deployment targets** — cloud provider, container registry, CDN, serverless
5. **Check for monorepo structure** — multiple projects/services in one repo?

### Step 2: Pipeline Architecture

Every pipeline follows this ordering principle: **fail fast — cheapest checks first.**

```
Lint/Format → Build → Unit Tests → Integration Tests → Security Scan → Deploy
```

If any stage fails, subsequent stages do not run. Total pipeline time budget: under 10 minutes for the fast path (lint + build + unit tests).

### Step 3: Stage Design

#### Stage 1: Lint and Format Check (fastest — run first)

```yaml
# Purpose: catch style and type errors in <30 seconds
- name: Lint
  run: |
    npm run lint
    npm run typecheck
    npm run format:check  # --check flag, never auto-fix in CI
```

Rules:
- Format check, not format fix — CI detects, developers fix locally
- Type checking is a lint stage, not a build stage
- If lint takes >60 seconds, something is wrong

#### Stage 2: Build

```yaml
# Purpose: compile/bundle and verify the artifact is producible
- name: Build
  run: npm run build
```

Rules:
- Build output is cached or uploaded as an artifact for later stages
- Build once, deploy the same artifact everywhere (dev, staging, prod)
- Never rebuild for each environment — use environment variables at runtime

#### Stage 3: Unit Tests (fast feedback)

```yaml
- name: Unit Tests
  run: CI=true npm test -- --coverage
```

Rules:
- Run in run mode, never watch mode (`CI=true` or explicit `--run` flag)
- Coverage report uploaded as artifact
- Fail if coverage drops below threshold (configure per-project)
- Timeout: 5 minutes max. If unit tests take longer, they aren't unit tests

#### Stage 4: Integration Tests

```yaml
- name: Integration Tests
  run: CI=true npm run test:integration
  services:
    postgres:
      image: postgres:16-alpine
      env:
        POSTGRES_PASSWORD: test
```

Rules:
- Run after unit tests pass (don't waste time on integration if units fail)
- Use service containers for databases, message brokers, etc.
- Timeout: 10 minutes max
- Separate from unit tests — different command, different config

#### Stage 5: Security Scan

```yaml
- name: Security Scan
  run: |
    npm audit --audit-level=high
    # or: trivy fs . --severity HIGH,CRITICAL
```

Rules:
- Fail on HIGH and CRITICAL vulnerabilities
- Allow suppression file for acknowledged false positives (with expiry dates)
- Run SAST (static analysis) in addition to dependency audit
- Container image scanning if building Docker images

#### Stage 6: Deploy

```yaml
- name: Deploy
  if: github.ref == 'refs/heads/main' && success()
  run: ./scripts/deploy.sh
```

Rules:
- Deploy only on main branch, only after ALL checks pass
- Use environment protection rules (manual approval for production)
- Deploy the artifact built in Stage 2 — never rebuild
- Include a smoke test after deployment
- Rollback plan documented or automated

## Caching Strategy

Cache aggressively to reduce pipeline time:

```yaml
# Node.js
- uses: actions/cache@v4
  with:
    path: node_modules
    key: node-${{ hashFiles('package-lock.json') }}

# .NET
- uses: actions/cache@v4
  with:
    path: ~/.nuget/packages
    key: nuget-${{ hashFiles('**/*.csproj') }}

# Python
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: pip-${{ hashFiles('requirements*.txt') }}

# Docker layers
- uses: docker/build-push-action@v5
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

Rules:
- Cache key MUST include a hash of the lockfile/dependency manifest
- Restore keys for partial cache hits (same prefix, different hash)
- Cache the dependency directory, not the build output (build output changes more frequently)
- Monitor cache hit rates — below 80% means the key strategy is wrong

## Matrix Strategy

Use matrix builds for multi-version or multi-project testing:

```yaml
# Multi-version testing
strategy:
  matrix:
    node-version: [20, 22]
  fail-fast: true  # Stop all jobs if one fails

# Monorepo auto-discovery
strategy:
  matrix:
    project: ${{ fromJson(needs.detect-changes.outputs.projects) }}
```

Rules:
- `fail-fast: true` — no point running other versions if one fails
- For monorepos, detect changed projects first and only build/test affected ones
- Matrix dimension should be small (2-3 values). Combinatorial explosion wastes CI minutes

## Monorepo CI (if applicable)

For monorepo projects:

1. **Change detection** — determine which projects changed using path filters or `git diff`
2. **Selective execution** — only build/test projects that changed or depend on changed code
3. **Dependency graph** — if project A depends on project B and B changed, test A too
4. **Shared workflows** — extract common steps into reusable workflows/templates

```yaml
# GitHub Actions path filter
on:
  push:
    paths:
      - 'services/api/**'
      - 'packages/shared/**'  # shared dependency
```

## Secrets Management

- **Never hardcode secrets** — use repository/environment secrets
- **Minimal scope** — each secret available only to the jobs that need it
- **Rotation** — document which secrets exist and when they were last rotated
- **Masking** — pipeline platform should auto-mask secrets in logs. Verify this
- **Environment-specific** — production secrets only available in production deployment jobs
- **No secrets in build args** — use multi-stage builds or runtime injection

## Version Pinning

```yaml
# Pin action versions to full SHA (not tags)
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4.1.1

# Pin tool versions
- uses: actions/setup-node@v4
  with:
    node-version-file: '.nvmrc'  # or package.json engines
```

Rules:
- Pin GitHub Actions to commit SHA, not tag (tags can be moved)
- Pin language/tool versions to the project's version file (`.nvmrc`, `global.json`, `.python-version`)
- Pin Docker base images to digest, not just tag
- Dependabot or Renovate for automated version updates

## Anti-Patterns (NEVER do these)

- **Watch mode in CI** — tests never exit. Always use `CI=true` or `--run`
- **Rebuilding for each environment** — build once, configure at runtime
- **No caching** — every run downloads the internet. Cache dependencies
- **Deploy from feature branches** — only main/release branches deploy
- **Secrets in pipeline files** — use secret management, never inline
- **No timeout** — set job-level and step-level timeouts. Runaway processes cost money
- **Success-only notifications** — alert on failure, not on success. Nobody reads 200 green emails
- **Manual artifact passing** — use pipeline artifacts or cache, not manual copy between stages

## Output

Pipeline design affects all four [DORA metrics](https://dora.dev/): deployment frequency (how often the pipeline runs), lead time for changes (pipeline duration), change failure rate (test/gate effectiveness), and time to restore service (rollback speed).

Deliver:
1. Complete pipeline configuration file (`.github/workflows/*.yml` or equivalent)
2. Any supporting scripts referenced by the pipeline
3. `.dockerignore` or equivalent if building containers
4. Brief explanation of stage ordering and caching decisions

## Related Skills

- `/devops:write-dockerfile` — pipelines that build containers need a Dockerfile. Ensure the pipeline's build stage matches the Dockerfile's target.
