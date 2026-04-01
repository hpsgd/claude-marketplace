# Claude Marketplace

A centralized marketplace for sharing Claude Code plugins, instructions, and configurations across your team.

## Quick start

### 1. Add the marketplace

```
/plugin marketplace add hpsgd/claude-marketplace
```

### 2. Install plugins

Pick what you need, or copy a block to install a whole category.

**Core (rules + thinking skills):**
```
/plugin install coding-standards@hpsgd
/plugin install writing-style@hpsgd
/plugin install security-compliance@hpsgd
/plugin install thinking@hpsgd
/plugin install workflow-tools@hpsgd
/plugin install technology-stack@hpsgd
```

**Product team agents:**
```
/plugin install cpo@hpsgd
/plugin install product-owner@hpsgd
/plugin install designer@hpsgd
/plugin install technical-writer@hpsgd
/plugin install gtm@hpsgd
/plugin install support@hpsgd
```

**Engineering team agents:**
```
/plugin install cto@hpsgd
/plugin install architect@hpsgd
/plugin install react-developer@hpsgd
/plugin install dotnet-developer@hpsgd
/plugin install python-developer@hpsgd
/plugin install qa-engineer@hpsgd
/plugin install devops@hpsgd
/plugin install security-engineer@hpsgd
/plugin install data-engineer@hpsgd
```

**Everything at once:**
```
/plugin install coding-standards@hpsgd
/plugin install writing-style@hpsgd
/plugin install security-compliance@hpsgd
/plugin install thinking@hpsgd
/plugin install workflow-tools@hpsgd
/plugin install technology-stack@hpsgd
/plugin install cpo@hpsgd
/plugin install product-owner@hpsgd
/plugin install designer@hpsgd
/plugin install technical-writer@hpsgd
/plugin install gtm@hpsgd
/plugin install support@hpsgd
/plugin install cto@hpsgd
/plugin install architect@hpsgd
/plugin install react-developer@hpsgd
/plugin install dotnet-developer@hpsgd
/plugin install python-developer@hpsgd
/plugin install qa-engineer@hpsgd
/plugin install devops@hpsgd
/plugin install security-engineer@hpsgd
/plugin install data-engineer@hpsgd
```

Then reload:

```
/reload-plugins
```

### Alternative: JSON configuration

Copy into your project's `.claude/settings.json` (or `settings.local.json` for personal use):

<details>
<summary>Core plugins only</summary>

```json
{
  "enabledPlugins": {
    "coding-standards@hpsgd": true,
    "writing-style@hpsgd": true,
    "security-compliance@hpsgd": true,
    "thinking@hpsgd": true,
    "workflow-tools@hpsgd": true,
    "technology-stack@hpsgd": true
  }
}
```
</details>

<details>
<summary>Everything</summary>

```json
{
  "enabledPlugins": {
    "coding-standards@hpsgd": true,
    "writing-style@hpsgd": true,
    "security-compliance@hpsgd": true,
    "thinking@hpsgd": true,
    "workflow-tools@hpsgd": true,
    "technology-stack@hpsgd": true,
    "cpo@hpsgd": true,
    "product-owner@hpsgd": true,
    "designer@hpsgd": true,
    "technical-writer@hpsgd": true,
    "gtm@hpsgd": true,
    "support@hpsgd": true,
    "cto@hpsgd": true,
    "architect@hpsgd": true,
    "react-developer@hpsgd": true,
    "dotnet-developer@hpsgd": true,
    "python-developer@hpsgd": true,
    "qa-engineer@hpsgd": true,
    "devops@hpsgd": true,
    "security-engineer@hpsgd": true,
    "data-engineer@hpsgd": true
  }
}
```
</details>

### 3. Start using them

Plugins activate automatically. Skills are available as slash commands (e.g., `/hpsgd:code-review`) or are auto-invoked by Claude when relevant.

## Available plugins

### Core plugins

| Plugin | Type | Description |
|---|---|---|
| `coding-standards` | Rules + Skills | TypeScript, .NET, Python conventions, git workflow, testing, architecture, AI steering. 7 rules, 5 review skills |
| `writing-style` | Rules + Skills | AI tell avoidance, banned vocabulary, sentence structure, 15-point editing checklist |
| `security-compliance` | Rules + Skills | Security baseline rules and deep security audit skill |
| `thinking` | Skills | 11 skills: ISC, algorithm, first-principles, council, red-team, creative, iterative-depth, scientific-method, learning, wisdom, health-check |
| `workflow-tools` | Skills + Agent | Code review, PR creation skills, and reviewer agent |
| `technology-stack` | Rules | JasperFx, Next.js, Pulumi, Moon, SonarCloud, event sourcing conventions |

### Product team agents

Each agent is a separate plugin — install only the ones you need.

| Plugin | Agent | Skills |
|---|---|---|
| `cpo` | Chief Product Officer — coordinates product team, escalates to CTO for technical concerns | `decompose-initiative` |
| `product-owner` | Requirements, user stories, acceptance criteria, backlog prioritisation | `write-prd`, `groom-backlog`, `write-user-story`, `define-okrs` |
| `designer` | UI/UX design, design system, accessibility, component specs | `component-spec`, `accessibility-audit`, `design-review` |
| `technical-writer` | API docs, user guides, changelogs, knowledge base, runbooks | `write-api-docs`, `write-changelog`, `write-runbook` |
| `gtm` | Positioning, launch strategy, content marketing, competitive analysis | `positioning`, `launch-plan`, `competitive-analysis` |
| `support` | Ticket triage, feedback synthesis, knowledge base, bug escalation | `write-kb-article`, `feedback-synthesis`, `triage-tickets` |

### Engineering team agents

Each agent is a separate plugin — install only the ones you need.

| Plugin | Agent | Skills |
|---|---|---|
| `cto` | Chief Technology Officer — coordinates engineering team, escalates to CPO for product concerns | — |
| `architect` | System design, ADRs, technology evaluation, API strategy | `write-adr`, `evaluate-technology`, `system-design`, `api-design` |
| `react-developer` | React/Next.js: TypeScript, Tailwind, content-collections, Vitest | `component-from-spec`, `performance-audit` |
| `dotnet-developer` | .NET/C#: Wolverine, Marten, event sourcing, CQRS, Alba testing | `write-endpoint`, `write-handler` |
| `python-developer` | Python: Ruff, mypy, BDD (pytest-bdd), Hypothesis, DDD | `write-feature-spec`, `write-schema` |
| `qa-engineer` | Test strategy, test automation, quality gates, coverage | `test-strategy`, `generate-tests`, `write-bug-report` |
| `devops` | IaC, CI/CD, deployment, monitoring, incident response | `write-pipeline`, `write-dockerfile`, `incident-response` |
| `security-engineer` | Threat modelling, security audits, compliance, vulnerability management | `threat-model`, `security-review`, `dependency-audit` |
| `data-engineer` | Data pipelines, analytics, event tracking, metrics | `event-tracking-plan`, `write-query`, `data-model` |

## How it works

### Two approaches to sharing instructions

Claude Code plugins natively support **tools, agents, skills, and output styles**. But team **instructions** (coding standards, security rules, writing guidelines) need a different mechanism. This marketplace uses two complementary approaches:

#### 1. Rules (installed via hook)
For instructions that should **always be active** — coding conventions, security baselines, writing style. These are `.md` files in each plugin's `rules/` directory. A `SessionStart` hook automatically copies them into your project's `.claude/rules/` directory with a namespace prefix (e.g., `coding-standards--typescript.md`).

**Best for:** org-wide standards, conventions, compliance rules

#### 2. Skills (auto-invoked by context)
For instructions that apply **in specific contexts** — code review checklists, security audit procedures, PR templates. These are skills that Claude auto-invokes when the context matches.

**Best for:** workflow-specific guidance, path-specific rules, on-demand tools

| Scenario | Approach |
|----------|----------|
| "Always follow these TypeScript conventions" | Rule (installed) |
| "When reviewing code, check for X" | Skill (auto-invoked) |
| "Use this tone in all communications" | Rule (installed) |
| "When working on API files, follow these patterns" | Skill with `paths:` filter |
| "Security checklist for all PRs" | Skill (invoked during review) |

### Agent coordination model

Agents are organised as two teams reporting to the human:

```
Human (CEO/Founder)
├── CPO
│   ├── product-owner
│   ├── designer
│   ├── technical-writer
│   ├── gtm
│   └── support
└── CTO
    ├── architect
    ├── react-developer
    ├── dotnet-developer
    ├── python-developer
    ├── qa-engineer
    ├── devops
    ├── security-engineer
    └── data-engineer
```

Leads coordinate their teams and escalate cross-domain issues to the human. When the CPO hits a technical question, they say "this needs the CTO's input." When leads conflict, both present their case and the human decides.

## Creating a new plugin

1. Create the plugin directory:
   ```
   plugins/my-plugin/
   ├── .claude-plugin/plugin.json   # Required
   ├── skills/                      # Optional
   │   └── my-skill/SKILL.md
   ├── agents/                      # Optional
   │   └── my-agent.md
   ├── rules/                       # Optional: installed into projects
   │   └── my-rules.md
   └── hooks/                       # Optional: if you have rules to install
       └── hooks.json
   ```

2. If your plugin has rules, add the install hook in `hooks/hooks.json`:
   ```json
   {
     "hooks": {
       "SessionStart": [
         {
           "matcher": "startup",
           "hooks": [
             {
               "type": "command",
               "command": "${CLAUDE_PLUGIN_ROOT}/../../scripts/install-rules.sh \"${CLAUDE_PLUGIN_ROOT}\" \"$CLAUDE_PROJECT_DIR\""
             }
           ]
         }
       ]
     }
   }
   ```

   `${CLAUDE_PLUGIN_ROOT}` is automatically set by Claude Code to the plugin's installation directory. `$CLAUDE_PROJECT_DIR` points to the consuming project's root.

3. Register the plugin in `.claude-plugin/marketplace.json`:
   ```json
   {
     "name": "my-plugin",
     "source": "my-plugin",
     "description": "What it does",
     "version": "1.0.0"
   }
   ```

4. Update this README with usage instructions.

## Customization

### Per-project overrides
Projects can override marketplace rules by creating their own `.claude/rules/` files. Project-level rules take precedence.

### Disabling specific plugins
Remove or set to `false` in your project's `.claude/settings.json`:
```json
{
  "enabledPlugins": {
    "writing-style@hpsgd": false
  }
}
```

### Local overrides (not committed)
Use `.claude/settings.local.json` for personal preferences that shouldn't affect the team:
```json
{
  "enabledPlugins": {
    "coding-standards@hpsgd": false
  }
}
```

## Acknowledgements

The thinking plugin — particularly the ISC methodology, algorithm phases, first principles, council, red team, and creative skills — draws on concepts and methodologies from [PAI (Personal AI Infrastructure)](https://github.com/danielmiessler/Personal_AI_Infrastructure) by Daniel Miessler. The AI steering rules and writing style rules were also informed by patterns developed within the PAI framework.
