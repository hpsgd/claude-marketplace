---
name: review-settings
description: "Audit Claude Code settings.json files for overly broad permissions, overlapping rules, and cross-file redundancy. Produces a reconciled config."
argument-hint: "[optional: path to project, or 'global' to review only ~/.claude]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Edit, AskUserQuestion
---

Audit Claude Code settings files and produce a reconciled configuration. If $ARGUMENTS specifies a path, use that as the project root; otherwise use the current working directory.

## Step 1: Discover all settings files

Find every settings file that applies to the current context. Check these locations in order (highest to lowest priority):

| Scope | Path | Shared? |
|---|---|---|
| Local project | `.claude/settings.local.json` | No (gitignored) |
| Shared project | `.claude/settings.json` | Yes (committed) |
| User global | `~/.claude/settings.json` | No |

```bash
# Check each location exists and is valid JSON
for f in .claude/settings.local.json .claude/settings.json ~/.claude/settings.json; do
  if [ -f "$f" ]; then
    echo "FOUND: $f ($(wc -l < "$f") lines)"
  fi
done
```

Read each file that exists. If a file has invalid JSON, report the parse error and skip it.

## Step 2: Extract and classify permissions

From each file, extract the `permissions.allow`, `permissions.deny`, and `permissions.ask` arrays. For each rule, classify it:

**Tool type** (parse from the rule prefix):
- `Bash(...)` — shell command permissions
- `Read(...)` / `Edit(...)` / `Write(...)` — file access permissions
- `WebFetch(...)` / `WebSearch` — network permissions
- `Skill(...)` — skill invocation permissions
- `mcp__*` — MCP server permissions
- `Agent(...)` — subagent permissions

**Specificity level** (from most to least specific):
- **Exact command** — matches one literal command, e.g. `Bash(npm run build)`
- **Prefix wildcard** — matches commands starting with a prefix, e.g. `Bash(git commit:*)`
- **Broad wildcard** — matches a wide class of commands, e.g. `Bash(curl *)`, `Bash(grep:*)`
- **Unrestricted** — matches anything for that tool, e.g. `Bash`, `WebSearch`

## Step 3: Flag overly broad permissions

A permission is "overly broad" when it grants ability to execute arbitrary code or access arbitrary resources without meaningful constraint. Flag any rule matching these patterns:

**Always flag (high risk):**
- `Bash` with no arguments (allows any shell command)
- `Bash(python*)`, `Bash(node*)`, `Bash(ruby*)` — arbitrary script execution
- `Bash(curl *)`, `Bash(wget *)` — arbitrary network requests from shell
- `Bash(rm *)`, `Bash(sudo *)` — destructive operations
- `Read` or `Edit` with no path constraint
- `WebFetch` with no domain constraint

**Flag as suspicious (medium risk):**
- `Bash(grep:*)`, `Bash(find *)` — broad filesystem inspection (usually fine, but worth noting if more specific rules exist)
- `Bash(cd:*)` — directory traversal (rarely useful as a permission)
- `Bash(ls:*)` — broad directory listing
- Path permissions covering home directory recursively, e.g. `Read(~/*)` or `Read(//Users/**)`

**Flag as fragments (likely junk):**
- `Bash(done)`, `Bash(do)`, `Bash(do echo:*)` — shell loop fragments that got approved individually
- `Bash(echo *)` — echo statements approved during debugging
- Permissions containing shell constructs like `while read`, `for f`, `xargs`
- Rules with escaped quotes and complex inline scripts — these are one-off commands that got auto-approved

For each flagged rule, report:
- The rule text
- Which file it appears in
- Risk level (high / medium / junk)
- Why it's flagged
- Suggested action (remove, replace with narrower rule, or keep with justification)

## Step 4: Find overlapping and redundant permissions

Compare all rules pairwise within and across files. Identify:

**Subsets (one rule covers the other):**
- `Bash(git commit *)` is a subset of `Bash(git *)`
- `Bash(npm run build)` is a subset of `Bash(npm run *)`  which is a subset of `Bash(npm *)`
- `Read(/src/**/*.ts)` is a subset of `Read(/src/**)`
- `WebFetch(domain:api.github.com)` is a subset of `WebFetch(domain:github.com)` (subdomain matching)

When one rule is a strict subset of another, recommend keeping only the broader rule — unless the broader rule was flagged as overly broad in Step 3, in which case keep the narrower rules and remove the broad one.

**Duplicates across files:**
- Same rule in both `.claude/settings.json` and `.claude/settings.local.json`
- Same plugin enabled in both global and project settings
- Same `extraKnownMarketplaces` entry in multiple files

For duplicates, recommend keeping the rule at the appropriate scope:
- Rules specific to this project → `.claude/settings.json` (shared) or `.claude/settings.local.json` (personal)
- Rules that apply everywhere → `~/.claude/settings.json`

**Conflicting rules:**
- A rule in `allow` at one scope and `deny` at another
- A rule in both `allow` and `ask` at the same scope

Report conflicts with which scope wins (deny always wins; for allow vs ask, the more restrictive scope wins).

## Step 5: Check non-permission settings

Review other settings for redundancy:

**enabledPlugins:**
- Same plugin enabled at both global and project scope — redundant (project inherits global)
- Plugins enabled but not installed or not found in any known marketplace

**extraKnownMarketplaces:**
- Duplicated across scopes
- Marketplaces referenced but no plugins enabled from them

**env:**
- Same env var set at multiple scopes (which wins?)
- Experimental flags that may no longer be needed

## Step 6: Present findings and proposed reconciliation

Present the audit as a structured report, then offer a reconciled configuration.

### Report format

```markdown
## Settings Audit Report

### Files discovered
- [list each file with line count]

### Overly broad permissions (Step 3)
| Rule | File | Risk | Recommendation |
|---|---|---|---|
| ... | ... | ... | ... |

### Overlapping rules (Step 4)
| Broader rule | Narrower rule(s) | Recommendation |
|---|---|---|
| ... | ... | ... |

### Cross-file redundancy (Step 4-5)
| Setting | Found in | Recommendation |
|---|---|---|
| ... | ... | ... |

### Fragments and junk rules
[list with recommendation to remove all]

### Summary
- X rules reviewed
- Y flagged as overly broad
- Z overlapping pairs found
- W redundant across files
- N fragments/junk rules
```

### Reconciled configuration

After presenting the report, produce a clean version of each settings file with:
- All junk/fragment rules removed
- Overlapping rules collapsed to the broader (safe) rule
- Overly broad rules removed or replaced with safer alternatives
- Cross-file duplicates removed (kept at the right scope)
- Rules sorted by tool type, then alphabetically

Present the reconciled files as diffs against the current files so the user can see what changed.

## Step 7: Apply changes (with user approval)

Use AskUserQuestion to present the reconciled configuration and ask the user which changes to apply. Offer these options:

1. **Apply all** — write all reconciled files
2. **Apply per-file** — show each file's changes and ask individually
3. **Apply selectively** — let the user pick which individual changes to keep
4. **Export only** — write the reconciled config to a temp file for manual review

Only write to settings files after explicit approval. Never modify settings files without asking.

## Rules

- **Read before recommending.** Every recommendation must be based on an actual rule read from an actual file. Never assume what a settings file contains.
- **Explain the risk.** When flagging a rule, say what it allows in concrete terms. "`Bash(python3 *)` allows execution of any Python script" is useful. "This is too broad" is not.
- **Respect intentional breadth.** Some broad rules are deliberate. `Bash(git *)` in a developer's global settings is probably intentional. Flag it, but don't treat it as equivalent to `Bash(rm *)`.
- **Don't invent rules.** The reconciled config should only contain rules from the original files (narrowed, deduplicated, or removed). Never add permissions the user didn't already have.
- **Preserve deny rules.** Never recommend removing a deny rule unless the user explicitly asks. Deny rules are safety constraints.
- **Local stays local.** Rules in `settings.local.json` were put there for a reason (personal, not shared). Don't move them to `settings.json` without asking.
- **Junk detection is pattern-based.** Shell fragments (`done`, `do`, `do echo:*`) and one-off inline scripts with heavy escaping are almost always auto-approved accidents, not intentional permissions. Flag them confidently.

## Anti-patterns

- **Rewriting from scratch** — the goal is to clean up existing settings, not design an ideal permission set. Work with what's there.
- **Adding permissions** — this is a review skill, not a setup skill. Reduce, don't expand.
- **Silently modifying files** — every change must be shown to the user first with a clear diff.
- **Treating all broad rules equally** — `Bash(git *)` and `Bash(python3 *)` are different risk levels. Git commands are version control operations. Python is arbitrary code execution.

## Related skills

- `/thinking:health-check` — broader project setup audit (rules, plugins, memory, docs). Use when you want a full picture beyond just settings.
- `/update-config` — built-in skill for adding new configuration. Use that for setup, use this skill for cleanup.
