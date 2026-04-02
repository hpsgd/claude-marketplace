---
name: bootstrap-project
description: "Bootstrap or update a project with domain-specific documentation, CLAUDE.md files, and governance artifacts. Delegates to each installed agent's bootstrap skill. Idempotent — safe to re-run after adding new plugins. Use at project kickoff or when adding new agents to an existing project."
argument-hint: "[project name, or 'update' to re-run for newly installed plugins]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Bootstrap Project

Orchestrate the bootstrapping (or updating) of project documentation and governance for $ARGUMENTS. This skill does not generate domain files itself — it delegates to each installed agent's `bootstrap` skill, coordinates execution order, and produces shared artifacts. It is idempotent: re-running after installing new plugins bootstraps only what is new or updated.

## Step 1: Discover Installed Plugins

Read the project's plugin configuration to determine which agent plugins are installed. The coordinator does not decide what is relevant — **if a plugin is installed, it participates**.

1. Read `.claude/settings.json`, `.claude/settings.local.json`, and any workspace `settings.json` to find installed plugin paths.
2. For each installed plugin, read its `.claude-plugin/plugin.json` to extract `name` and `version`.
3. Check for the existence of a `bootstrap` skill directory under each plugin (`skills/bootstrap/SKILL.md`). Only plugins with a bootstrap skill participate in delegation.
4. Build the **installed agents list** — a list of `{ name, version, hasBootstrap }` entries.

**Output:** Table of installed plugins, their versions, and whether they have a bootstrap skill.

## Step 2: Read or Initialise Manifest

The manifest tracks which agents have been bootstrapped, enabling idempotent re-runs.

1. Attempt to read `.claude/bootstrap-manifest.json`.
2. If it does not exist, initialise an empty manifest structure:

```json
{
  "schemaVersion": 1,
  "projectName": "[project name]",
  "lastRun": null,
  "agents": {}
}
```

Each entry in `agents` looks like:

```json
{
  "coding-standards": {
    "version": "1.2.0",
    "bootstrappedAt": "2026-04-02T10:30:00Z",
    "files": ["docs/coding-standards/CLAUDE.md", "docs/coding-standards/linting.md"]
  }
}
```

**Output:** Manifest state — new or loaded with N existing agent entries.

## Step 3: Determine Work Plan

Compare the installed agents list (Step 1) against the manifest (Step 2) to classify each agent:

| Classification | Condition | Action |
|---|---|---|
| **New** | Agent has a bootstrap skill but is not in the manifest | Run bootstrap skill |
| **Updated** | Agent is in the manifest but installed version > manifest version | Run bootstrap skill in **merge mode** |
| **Current** | Agent is in the manifest at the same version | **Skip** (unless user passed `--force`) |
| **No bootstrap** | Agent has no bootstrap skill | Skip — note in summary |

If `$ARGUMENTS` contains `--force`, treat all agents with bootstrap skills as **New**.

Present the work plan to the user before proceeding:

```markdown
### Bootstrap Work Plan

| Agent | Status | Action |
|---|---|---|
| coding-standards | New | Bootstrap |
| architect | v1.0 → v1.2 | Merge update |
| qa-lead | v2.0 (current) | Skip |
| ... | ... | ... |

Proceed? (Y/n)
```

**Output:** Classified work plan table. Wait for user confirmation.

## Step 4: Delegate to Agent Bootstraps

Invoke each agent's `bootstrap` skill in dependency order. Groups execute sequentially; agents within a group may execute in any order.

### Dependency Order

| Group | Agents | Rationale |
|---|---|---|
| **1 — Foundations** | coding-standards, architect | Standards and architecture inform everything else |
| **2 — Engineering domains** | qa-lead, security-engineer, devops, release-manager, performance-engineer | Core engineering practices depend on foundations |
| **3 — Stack-specific** | python-developer, dotnet-developer, react-developer, data-engineer, ai-engineer | Stack implementations depend on standards and practices |
| **4 — Product domains** | product-owner, ui-designer, ux-researcher | Product work builds on the engineering foundation |
| **5 — Content** | developer-docs-writer, user-docs-writer, internal-docs-writer | Documentation follows product and engineering decisions |
| **6 — Market & customer** | gtm, support, customer-success | Go-to-market and support build on product definition |
| **7 — Governance** | grc-lead | Governance wraps around everything else |

For each agent that needs bootstrapping:

1. **Skip** agents classified as "Current" or "No bootstrap".
2. **New agents:** Invoke the agent's `bootstrap` skill. The agent creates its domain directory under `docs/` and writes its own `CLAUDE.md` and domain-specific files.
3. **Updated agents (merge mode):** Invoke the agent's `bootstrap` skill with a merge instruction. The agent must:
   - Read existing files in its domain directory.
   - Compare with its current template.
   - Add missing sections or files.
   - **Never overwrite or delete** existing content — only append or create new files.
4. After each agent completes, record the files it created or modified (use `Glob` to diff before/after if needed).

**Output:** Per-group progress log showing which agents ran and what files they produced.

## Step 5: Generate Shared Artifacts

After all agent bootstraps complete, the coordinator generates cross-cutting artifacts that no single agent owns.

### 5a. `docs/CLAUDE.md` — Domain Index

Auto-generate an index of all active domain directories. Scan `docs/*/CLAUDE.md` with `Glob` and build:

```markdown
<!-- Generated by bootstrap-project. Auto-regenerated on each run. -->
# Project Documentation Index

This file is auto-generated by `/coordinator:bootstrap-project`. It lists all active domain documentation directories. Each domain has its own `CLAUDE.md` with domain-specific instructions.

| Domain | Path | Description |
|---|---|---|
| Architecture | `docs/architecture/CLAUDE.md` | System design, ADRs, technology choices |
| Coding Standards | `docs/coding-standards/CLAUDE.md` | Linting, formatting, review conventions |
| ... | ... | ... |

> Re-run `/coordinator:bootstrap-project update` after adding or removing plugins to refresh this index.
```

### 5b. Root `CLAUDE.md` Integration

Read the project root `CLAUDE.md`. If it exists, ensure it contains a section pointing to `docs/CLAUDE.md`. If the section is missing, append it. If `CLAUDE.md` does not exist, create it with a minimal project header and the pointer section.

The section to add or verify:

```markdown
## Documentation Index

This project uses domain-specific documentation managed by agent plugins.
See [docs/CLAUDE.md](docs/CLAUDE.md) for the full index of all domain documentation.
```

Use `Edit` to merge — never overwrite the root `CLAUDE.md`.

### 5c. `docs/tooling-register.md`

If the file does not exist, create it from the coding-standards tooling register template:

```markdown
<!-- Generated by bootstrap-project. Review and customize. -->
# Tooling Register

| Function | Tool | Version | Notes |
|---|---|---|---|
| Language | [e.g. Python 3.12] | | |
| Framework | [e.g. FastAPI] | | |
| Package manager | [e.g. uv] | | |
| Linter | [e.g. ruff] | | |
| Formatter | [e.g. ruff format] | | |
| Type checker | [e.g. mypy] | | |
| Test runner | [e.g. pytest] | | |
| CI/CD | [e.g. GitHub Actions] | | |
| Container runtime | [e.g. Docker] | | |
| Orchestration | [e.g. Kubernetes] | | |
| Monitoring | [e.g. Datadog] | | |
| Error tracking | [e.g. Sentry] | | |

> Populate this register with your actual tool choices. Keep it updated as the stack evolves.
```

If the file already exists, skip.

### 5d. `docs/okrs/period-1-okrs.md`

If the file does not exist, create the placeholder:

```markdown
<!-- Generated by bootstrap-project. Review and customize. -->
# OKRs — [Project Name] — Period 1

## Objective 1: Establish project foundations

| Key Result | Target | Current | Status |
|---|---|---|---|
| KR1: CI/CD pipeline deployed and green | 100% | 0% | Not started |
| KR2: Core domain model defined and reviewed | Complete | — | Not started |
| KR3: First feature spec written and approved | Complete | — | Not started |

## Objective 2: Deliver initial value

| Key Result | Target | Current | Status |
|---|---|---|---|
| KR1: [placeholder] | [target] | — | Not started |
| KR2: [placeholder] | [target] | — | Not started |

> Customize these OKRs with the team. Use `/coordinator:define-okrs` for detailed OKR facilitation.
```

If the file exists, skip.

### 5e. `SECURITY.md`

If the file does not exist at the project root, create it following [GitHub security policy conventions](https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository):

```markdown
<!-- Generated by bootstrap-project. Review and customize. -->
# Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| latest | Yes |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **Do not** open a public issue.
2. Email [security contact] with a description of the vulnerability.
3. Include steps to reproduce, impact assessment, and any suggested fix.
4. You will receive an acknowledgement within **48 hours**.
5. We aim to provide a fix or mitigation within **7 days** for critical issues.

## Security Practices

- Dependencies are monitored for known vulnerabilities.
- Security-sensitive changes require review by the security engineer.
- See `docs/security/CLAUDE.md` for detailed security engineering practices (if available).
```

If the file exists, skip.

### 5f. `CHANGELOG.md`

If the file does not exist at the project root, create it in [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
<!-- Generated by bootstrap-project. Review and customize. -->
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project bootstrap with documentation structure.
```

If the file exists, skip.

## Step 6: Update Manifest

After all work is complete, update `.claude/bootstrap-manifest.json`:

1. For each agent that ran, record or update its entry with the current version, timestamp, and list of files created/modified.
2. Set `lastRun` to the current ISO 8601 timestamp.
3. Write the manifest using `Write`.

Ensure the `.claude/` directory exists before writing (create with `mkdir -p` if needed).

## Step 7: Output Summary

Present the final summary:

```markdown
## Bootstrap Summary — [Project Name]

### Agent Execution

| Agent | Group | Action | Files Created | Files Merged |
|---|---|---|---|---|
| coding-standards | 1 — Foundations | Bootstrapped | 3 | 0 |
| architect | 1 — Foundations | Merge update | 0 | 2 |
| qa-lead | 2 — Engineering | Skipped (current) | — | — |
| security-engineer | 2 — Engineering | Bootstrapped | 4 | 0 |
| ... | ... | ... | ... | ... |

### Shared Artifacts

| File | Action |
|---|---|
| `docs/CLAUDE.md` | Created / Updated |
| `docs/tooling-register.md` | Created / Skipped (exists) |
| `docs/okrs/period-1-okrs.md` | Created / Skipped (exists) |
| `SECURITY.md` | Created / Skipped (exists) |
| `CHANGELOG.md` | Created / Skipped (exists) |
| `.claude/bootstrap-manifest.json` | Updated |

### Next Steps

1. Review every generated document — they are starting points, not final artifacts.
2. Populate `docs/tooling-register.md` with your actual tool choices.
3. Customise `docs/okrs/period-1-okrs.md` with the team — or run `/coordinator:define-okrs`.
4. Run `/coordinator:decompose-initiative` to break down the first initiative.
5. Update `SECURITY.md` with your actual security contact and supported versions.
6. Add newly installed plugins and re-run `/coordinator:bootstrap-project update` to bootstrap them.
```

**Output:** Summary table with next steps.

## Rules

- **Delegate, don't generate.** The coordinator never creates domain-specific files itself. Each agent's `bootstrap` skill is responsible for its own domain directory and `CLAUDE.md`. The coordinator only produces shared cross-cutting artifacts (listed in Step 5).
- **Plugin installation determines participation.** Do not detect or guess the tech stack. If a plugin is installed, it participates. If it is not installed, it does not. The user controls relevance by installing and uninstalling plugins.
- **Idempotent by default.** The manifest tracks what has been done. Re-runs only process new or updated agents. Use `--force` to re-run everything. Never duplicate work.
- **Safe merge, never overwrite.** When updating existing files, review existing content and merge in missing sections. Never clobber existing files. Existing content represents decisions already made.
- **Every coordinator-generated file gets the marker comment.** `<!-- Generated by bootstrap-project. Review and customize. -->` at the top. Agent-generated files follow their own conventions.
- **Respect dependency order.** Foundations before engineering domains. Engineering domains before stack-specific. Stack-specific before product. Content after product. Governance last. This ensures later agents can reference artifacts from earlier ones.
- **CHANGELOG.md uses [Keep a Changelog](https://keepachangelog.com/) format.** Sections: Added, Changed, Deprecated, Removed, Fixed, Security. Start with `## [Unreleased]`.
- **SECURITY.md follows [GitHub conventions](https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository).** Include supported versions, reporting process, and expected response time.
- **Always confirm the work plan.** Present the classified agent table and wait for user confirmation before executing. This prevents unexpected changes.
- **This is a starting point.** Say it in the summary. Say it in the marker comments. Every generated doc needs team review before it becomes authoritative.

## Output Format

1. Installed plugins table (Step 1).
2. Work plan table with classifications — wait for user confirmation (Step 3).
3. Per-group execution log (Step 4).
4. Summary table of all files created/merged, agent execution results, and numbered next steps (Step 7).

## Related Skills

- `/coordinator:decompose-initiative` — after bootstrap, decompose the first initiative into workstreams.
- `/coordinator:define-okrs` — customise the generated OKR template with the team.
- `/qa-lead:test-strategy` — expand the generated test strategy with detailed test plans.
- `/architect:write-adr` — record architecture decisions as the project progresses.
- `/security-engineer:threat-model` — develop threat models referenced by the security bootstrap.
