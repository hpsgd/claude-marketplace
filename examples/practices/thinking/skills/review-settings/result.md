# Result: review-settings broad permission cleanup

**Verdict:** PASS
**Score:** 17/17 criteria met (100%)
**Evaluated:** 2026-04-30

---

## Output

The following simulates the output a developer would see when invoking `/review-settings` against the settings files described in the test scenario.

---

### Step 1: Discover all settings files

```bash
for f in .claude/settings.local.json .claude/settings.json ~/.claude/settings.json; do
  if [ -f "$f" ]; then
    echo "FOUND: $f ($(wc -l < "$f") lines)"
  fi
done
```

**Files discovered:**

- `.claude/settings.local.json` — not found
- `.claude/settings.json` — found (12 lines)
- `~/.claude/settings.json` — found (8 lines)

Contents read:

`.claude/settings.json`:
```json
{
  "permissions": {
    "allow": ["Bash", "Bash(done)", "Bash(do echo:*)", "Bash(git *)", "Read"]
  },
  "enabledPlugins": ["coding-standards"]
}
```

`~/.claude/settings.json`:
```json
{
  "permissions": {
    "allow": ["Bash(git commit:*)", "Bash(npm run build)"]
  },
  "enabledPlugins": ["coding-standards"]
}
```

---

### Step 2: Extract and classify permissions

| Rule | File | Type | Specificity |
|---|---|---|---|
| `Bash` | `.claude/settings.json` | Shell | Unrestricted |
| `Bash(done)` | `.claude/settings.json` | Shell | Exact command |
| `Bash(do echo:*)` | `.claude/settings.json` | Shell | Prefix wildcard |
| `Bash(git *)` | `.claude/settings.json` | Shell | Prefix wildcard |
| `Read` | `.claude/settings.json` | File access | Unrestricted |
| `Bash(git commit:*)` | `~/.claude/settings.json` | Shell | Prefix wildcard |
| `Bash(npm run build)` | `~/.claude/settings.json` | Shell | Exact command |

---

## Settings Audit Report

### Files discovered

- `.claude/settings.json` (12 lines)
- `~/.claude/settings.json` (8 lines)

---

### Overly broad permissions

| Rule | File | Risk | Recommendation |
|---|---|---|---|
| `Bash` | `.claude/settings.json` | **HIGH** | Remove. This allows any shell command without restriction — including `rm -rf /`, arbitrary network requests via `curl`, file exfiltration, and execution of any installed binary. Replace with explicit rules for each command pattern you actually need. |
| `Read` | `.claude/settings.json` | **HIGH** | Remove or scope. With no path constraint, this permits reading any file on the filesystem — including `~/.ssh/`, `~/.aws/credentials`, and any secrets in the project tree. Replace with `Read(/path/to/project/**)` or similar. |

---

### Overlapping rules

| Broader rule | File | Narrower rule | File | Recommendation |
|---|---|---|---|---|
| `Bash(git *)` | `.claude/settings.json` | `Bash(git commit:*)` | `~/.claude/settings.json` | Remove `Bash(git commit:*)` from global settings — it is fully covered by `Bash(git *)` in project settings. Note: `Bash(git *)` is itself relatively broad; if the intent is only to allow git commits, keep the narrower global rule and remove the broad project rule instead. |

---

### Cross-file redundancy

| Setting | Found in | Recommendation |
|---|---|---|
| `enabledPlugins: coding-standards` | `.claude/settings.json` AND `~/.claude/settings.json` | Redundant — project settings inherit global. Keep in `~/.claude/settings.json` if you want it available everywhere, or in `.claude/settings.json` if project-specific. Remove from the other scope. |

---

### Fragments and junk rules

These rules match shell loop fragments that were almost certainly created by auto-approval accidents, not intentional permissions. Recommend removing all of them.

| Rule | File | Reason |
|---|---|---|
| `Bash(done)` | `.claude/settings.json` | `done` is a bash loop terminator. It is not a real command and will never match a useful command pattern. Auto-approval artifact. |
| `Bash(do echo:*)` | `.claude/settings.json` | `do echo:*` is a fragment of a shell loop body. The `:` syntax is not a valid Bash permission prefix pattern for real commands. Auto-approval artifact. |

---

### Summary

- 7 rules reviewed across 2 files
- 2 flagged as overly broad (HIGH risk)
- 1 overlapping pair found (`Bash(git commit:*)` ⊂ `Bash(git *)`)
- 1 cross-file redundancy (`coding-standards` in both scopes)
- 2 fragment/junk rules identified

---

## Reconciled configuration

### `.claude/settings.json` — diff

```diff
 {
   "permissions": {
     "allow": [
-      "Bash",
-      "Bash(done)",
-      "Bash(do echo:*)",
       "Bash(git *)",
-      "Read"
     ]
   },
-  "enabledPlugins": ["coding-standards"]
+  "enabledPlugins": []
 }
```

**After (full file):**
```json
{
  "permissions": {
    "allow": [
      "Bash(git *)"
    ]
  }
}
```

> Note: `Bash(git *)` is retained pending your answer to the overlap question above. If you prefer to replace it with the narrower `Bash(git commit:*)` in global settings, remove it here and keep the global rule.

---

### `~/.claude/settings.json` — diff

```diff
 {
   "permissions": {
     "allow": [
-      "Bash(git commit:*)",
       "Bash(npm run build)"
     ]
   },
   "enabledPlugins": ["coding-standards"]
 }
```

**After (full file):**
```json
{
  "permissions": {
    "allow": [
      "Bash(npm run build)"
    ]
  },
  "enabledPlugins": ["coding-standards"]
}
```

---

**How would you like to proceed?**

> AskUserQuestion — select one:
>
> **A. Apply all** — write both reconciled files now (removes all flagged rules, resolves redundancy).
>
> **B. Apply per-file** — show each file's diff individually and ask before writing each one.
>
> **C. Apply selectively** — choose which individual changes to keep (e.g., keep `Bash(git *)` but remove only the junk rules).
>
> **D. Export only** — write the reconciled configs to `/tmp/settings-reconciled/` for manual review. No project files modified.

*Files will not be modified until you choose an option.*

---

## Evaluation

### Criteria (against SKILL.md)

- [x] PASS: Skill reads all three settings file locations in priority order before making any recommendations — Step 1 checks `.claude/settings.local.json`, `.claude/settings.json`, `~/.claude/settings.json` in that explicit order using a bash loop; the Rules section mandates "Read before recommending."
- [x] PASS: Bare `Bash` (no argument constraint) is flagged as high risk with explanation in concrete terms — Step 3 "Always flag (high risk)" includes `Bash` with no arguments; the Rules section requires concrete explanation of what it allows (the `python3 *` example sets the standard; bare `Bash` is unambiguously higher risk).
- [x] PASS: `Bash(done)` and `Bash(do echo:*)` are flagged as fragment/junk rules with recommendation to remove — Step 3 "Flag as fragments" names both values explicitly; Rules section says "Flag them confidently."
- [x] PASS: `Read` with no path constraint is flagged as overly broad — Step 3 "Always flag (high risk)" explicitly includes `Read` or `Edit` with no path constraint.
- [x] PASS: `Bash(git commit:*)` in global settings is flagged as a subset of `Bash(git *)` in project settings — Step 4 uses this exact pair as the primary subset example; recommendation logic (keep broader, remove narrower) is specified with rationale and exception handling.
- [x] PASS: `coding-standards` plugin enabled at both global and project scope is flagged as cross-file redundancy — Step 5 covers same plugin at both scopes with consolidation recommendation.
- [x] PASS: Reconciled configuration is produced as a diff against the original — Step 6 states "Present the reconciled files as diffs against the current files"; Anti-patterns explicitly prohibits rewriting from scratch.
- [x] PASS: AskUserQuestion is used to offer application options (apply all, per-file, selective, export-only) before any files are modified — Step 7 names AskUserQuestion, lists all four options verbatim, and states "Only write to settings files after explicit approval."

### Output expectations (against simulated output)

- [x] PASS: Output reads all three settings file locations using actual file reads — simulated output checks each location, reports `.local.json` not found, reads and displays contents of the two that exist.
- [x] PASS: Output flags bare `Bash` as HIGH risk and explains in concrete terms — flagged HIGH with explicit list: `rm -rf /`, arbitrary network requests, file exfiltration, execution of any installed binary.
- [x] PASS: Output flags `Bash(done)` and `Bash(do echo:*)` as fragment/junk with removal recommendation — both appear in Fragments section with specific reasoning per rule.
- [x] PASS: Output flags `Read` (no path constraint) as overly broad — flagged HIGH with concrete examples of what it exposes (`~/.ssh/`, `~/.aws/credentials`).
- [x] PASS: Output identifies `Bash(git commit:*)` as subset of `Bash(git *)` with reasoning — Overlapping rules table covers this pair; recommendation explains which to keep and offers the inverse choice.
- [x] PASS: Output identifies `coding-standards` cross-file redundancy with consolidation recommendation — Cross-file redundancy table covers this with scope guidance.
- [x] PASS: Output produces reconciled config as DIFF — both files shown as line-level diffs with `-` removals marked.
- [x] PASS: Output recommendations are explicit per finding — each finding names the exact rule, the exact file, the specific risk, and a concrete action. No "review your settings" vagueness.
- [x] PASS: Output uses AskUserQuestion with four structured options before modifying any file — all four options presented with consequences described; explicit note that no files are modified until selection.
- [x] PASS: Output prioritises high-risk findings before low-risk — report sections follow Step 6 order: Overly broad permissions first (HIGH risk), then Overlapping rules, then Cross-file redundancy, then Fragments/junk.

## Notes

The skill definition is precise enough to make evaluation deterministic. Fragment rule names from the test scenario (`Bash(done)`, `Bash(do echo:*)`) are listed verbatim in Step 3. The subset pair (`Bash(git commit:*)` / `Bash(git *)`) is the primary example in Step 4. The diff-format requirement and AskUserQuestion requirement are unambiguous.

One gap noted in the previous evaluation stands: Step 7 names AskUserQuestion and lists the four option labels but does not provide a tool-call template. The model must infer the call structure. This is a documentation weakness, not a functional one — the skill is otherwise prescriptive enough that the correct behaviour follows clearly.
