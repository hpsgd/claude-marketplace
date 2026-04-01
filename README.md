# Claude Marketplace

A centralized marketplace for sharing Claude Code plugins, instructions, and configurations across your team.

## Quick start

### 1. Add the marketplace to your project

Add this to your project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "hpsgd": {
      "source": {
        "source": "github",
        "repo": "hpsgd/claude-marketplace"
      }
    }
  }
}
```

### 2. Enable plugins

Add the plugins you want to `.claude/settings.json`:

```json
{
  "enabledPlugins": {
    "coding-standards@hpsgd": true,
    "workflow-tools@hpsgd": true,
    "security-compliance@hpsgd": true,
    "writing-style@hpsgd": true,
    "technology-stack@hpsgd": true,
    "thinking@hpsgd": true
  }
}
```

### 3. Start using them

Plugins activate automatically. Skills are available as slash commands (e.g., `/hpsgd:code-review`) or are auto-invoked by Claude when relevant.

## Available plugins

### coding-standards
Language-generic conventions for TypeScript, .NET, Python, plus git workflow and AI behavioral rules.

| Component | Type | Description |
|-----------|------|-------------|
| `typescript.md` | Rule (installed) | TypeScript conventions: strict mode, ESM, Prettier, naming, imports |
| `dotnet.md` | Rule (installed) | .NET/C# conventions: project structure, package management, API design, dependency abstraction |
| `python.md` | Rule (installed) | Python 3.14+: Ruff, mypy strict, frozen dataclasses, BDD testing hierarchy |
| `testing.md` | Rule (installed) | General testing principles: AAA pattern, assertions, test data, external dependency abstraction |
| `git-and-ci.md` | Rule (installed) | Conventional Commits, squash merges, branch model, pre-push verification, no force pushing |
| `architecture.md` | Rule (installed) | General architecture: file focus, feature-slicing, shared configuration |
| `ai-steering.md` | Rule (installed) | Behavioral rules: surgical fixes, verify before asserting, minimal scope, no lint suppression |
| `review-standards` | Skill | Auto-invoked during code review — general quality and writing style |
| `review-typescript` | Skill | Auto-invoked for `.ts`/`.tsx` files — TypeScript and Next.js conventions |
| `review-dotnet` | Skill | Auto-invoked for `.cs` files — .NET/C# conventions |
| `review-python` | Skill | Auto-invoked for `.py` files — Python conventions |
| `review-git` | Skill | Auto-invoked during PR/commit workflows — git conventions |

### workflow-tools
Skills and agents for common development workflows.

| Component | Type | Description |
|-----------|------|-------------|
| `code-review` | Skill | Structured code review process (`/hpsgd:code-review`) |
| `pr-create` | Skill | Create PRs following team conventions (`/hpsgd:pr-create`) |
| `reviewer` | Agent | Dedicated code review subagent |

### security-compliance
Security baseline rules and audit capabilities.

| Component | Type | Description |
|-----------|------|-------------|
| `security-baseline.md` | Rule (installed) | Input validation, auth, secrets, bot protection, container security, dependency abstraction |
| `security-audit` | Skill | Deep security audit (`/hpsgd:security-audit`) |

### writing-style
Tone, voice, and communication guidelines.

| Component | Type | Description |
|-----------|------|-------------|
| `tone-and-voice.md` | Rule (installed) | Comprehensive AI tell avoidance: banned vocabulary (73+ words, 40+ phrases), sentence structure, punctuation rules, document structure, 15-point editing checklist |
| `style-guide` | Skill | Auto-invoked when writing documentation or copy |

### thinking
Structured thinking and reasoning skills.

| Component | Type | Description |
|-----------|------|-------------|
| `first-principles` | Skill | Deconstruct to fundamental truths and rebuild (`/hpsgd:first-principles`) |
| `iterative-depth` | Skill | Multi-lens analysis — 3-5 structured passes through a problem (`/hpsgd:iterative-depth`) |
| `creative` | Skill | Divergent ideation with forced diversity techniques (`/hpsgd:creative`) |
| `council` | Skill | Structured debate between 4 expert perspectives (`/hpsgd:council`) |
| `red-team` | Skill | Adversarial stress-testing — decompose, steelman, then attack (`/hpsgd:red-team`) |
| `scientific-method` | Skill | Goal → observe → hypothesise → experiment → measure → iterate (`/hpsgd:scientific-method`) |
| `isc` | Skill | Decompose requests into Identifiable, Specific, Verifiable Criteria with effort tiers and splitting tests (`/hpsgd:isc`) |
| `algorithm` | Skill | Seven-phase execution: observe → think → plan → build → execute → verify → learn (`/hpsgd:algorithm`) |
| `learning` | Skill | Capture, categorise, and recall learnings — failures, corrections, patterns (`/hpsgd:learning`) |
| `wisdom` | Skill | Build domain-specific wisdom frames with confidence levels and cross-domain synthesis (`/hpsgd:wisdom`) |
| `health-check` | Skill | Project health report — installed rules, memory state, wisdom frame health (`/hpsgd:health-check`) |

### technology-stack
Framework-specific conventions — enable the ones relevant to your project.

| Component | Type | Description |
|-----------|------|-------------|
| `jasperfx.md` | Rule (installed) | Wolverine endpoints/handlers/cascading chains, Marten event sourcing/projections, Alba integration tests |
| `nextjs.md` | Rule (installed) | Next.js App Router, atomic design, content-collections, Storybook, Tailwind, server/client patterns |
| `pulumi.md` | Rule (installed) | Pulumi IaC: encrypted config, cross-stack secrets, key rotation, auto-discovery, deployment pipeline |
| `moonrepo.md` | Rule (installed) | Moon task orchestration, tag-based tasks, generators, git hooks, MCP integration |
| `event-sourcing.md` | Rule (installed) | Cross-language CQRS/ES: lifecycle events, aggregates, cascading handlers, projections, context flow |
| `sonarcloud.md` | Rule (installed) | SonarCloud quality gate: PR enforcement, lcov coverage integration, configuration |

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
     "source": "./plugins/my-plugin",
     "description": "What it does",
     "version": "1.0.0"
   }
   ```

4. Update this README with usage instructions.

## Customization

### Per-project overrides
Projects can override marketplace rules by creating their own `.claude/rules/` files. Project-level rules take precedence.

### Disabling entire plugins
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
