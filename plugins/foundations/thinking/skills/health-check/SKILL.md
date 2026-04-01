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

Scan `.claude/rules/` for installed marketplace rules:

```bash
ls -la .claude/rules/
```

For each rule file:
- Which plugin installed it (from the namespace prefix)
- When it was last updated (file modification time)
- Whether the source rule is newer than the installed copy

Report: total count, breakdown by plugin, any stale copies.

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
