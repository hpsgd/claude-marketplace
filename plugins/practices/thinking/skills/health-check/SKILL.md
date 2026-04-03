---
name: health-check
description: Generate a health report of the current project's Claude Code setup — installed rules, enabled plugins, memory state, wisdom frame health, and learning coverage.
argument-hint: "[optional: specific area to check, e.g. 'rules', 'memory', 'wisdom']"
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

Generate a health report for the current project's Claude Code setup. If $ARGUMENTS specifies an area, focus on that; otherwise report on everything.

## What to Check

### 1. Installed Rules

Scan **both** global and project-level rules:

```bash
# Global rules (apply to all projects)
ls -la ~/.claude/rules/ 2>/dev/null

# Project-level rules (this project only)
ls -la .claude/rules/ 2>/dev/null
```

Check global (`~/.claude/rules/`) **first** — plugins installed globally write rules there. Then check project-level (`.claude/rules/`). For each rule file:
- Which plugin installed it (from the namespace prefix, e.g., `coding-standards--`)
- Whether it's a learned rule (`learned--` prefix)
- When it was last updated (file modification time)
- Whether the source rule in the plugin is newer than the installed copy

Report: total count, breakdown by source (marketplace vs learned), global vs project-level, any stale copies.

### 2. Project Configuration

Check `.claude/settings.json` and `.claude/settings.local.json`:
- Which plugins are enabled
- Any custom permissions
- Any hooks configured
- MCP servers

Report: enabled plugins, custom configuration.

### 3. CLAUDE.md Coverage

Check for project documentation:
- Root `CLAUDE.md` or `.claude/CLAUDE.md` — does it exist? How comprehensive?
- `.claude/rules/` — any project-specific (non-marketplace) rules?
- Sub-project CLAUDE.md files — are workspaces documented?

Report: documentation coverage, gaps.

### 4. Memory Health

If the project has a memory directory, check:
- Total memory files
- Memory types (user, feedback, project, reference)
- Most recent memory (is the system actively learning?)
- Any stale memories (referenced files that no longer exist)

Report: memory count by type, freshness.

### 5. Wisdom Frame Health

If wisdom frames exist in memory:
- List all frames with observation counts
- Classify health: growing (updated ≤7 days, 10+ observations), stable (≤30 days), stale (>30 days)
- Count crystallised principles (85%+ confidence)
- Identify cross-domain principles

Report: frame inventory, health status, crystallisation rate.

### 6. Learning Coverage

If learning/feedback memories exist:
- Count by severity (critical, important, minor)
- Check for unresolved critical learnings
- Look for patterns (5+ learnings in same category)
- Identify domains with no learnings (blind spots)

Report: learning density, unresolved issues, pattern candidates.

## Output Format

```
## Project Health Report

### Summary
- Rules: X installed (Y from marketplace, Z project-specific)
- Plugins: X enabled
- Documentation: [good/gaps identified]
- Memory: X files (Y feedback, Z project decisions)
- Wisdom: X frames (Y growing, Z stable, W stale)
- Learnings: X captured (Y critical, Z important)

### Details
[per-section details as above]

### Recommendations
[specific actions to improve coverage]
```

## Anti-Patterns

See Rules below — health-check is diagnostic, not procedural, so anti-patterns are expressed as rules rather than a separate list.

## Rules

- **Check, don't assume.** Every health-check item must be verified with a tool call (ls, grep, read). Do not report based on memory of what was installed.
- **Report what IS, not what SHOULD BE.** A health check describes current state. Recommendations go in a separate section, not mixed with findings.
- **Never fabricate coverage.** If a section has no data (e.g., no wisdom frames exist), report "none found" — do not skip the section.
- **Staleness is a finding.** A rule installed 6 months ago with no updates is worth flagging. A memory referencing a deleted file is worth flagging.
- **Quantify everything.** "Some rules installed" is not a finding. "7 rules installed (5 from marketplace, 2 project-specific, 1 stale)" is.
- **Privacy-aware.** Memory files may contain user preferences or feedback. Report counts and types, not contents, unless the user asks for detail.

## Related Skills

- `/learning` — the learning system this health check audits. Use to capture new learnings.
- `/wisdom` — the wisdom frame system this health check audits. Use to record or query wisdom.
