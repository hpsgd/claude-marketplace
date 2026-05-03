# Test: review-settings broad permission cleanup

Scenario: A developer's settings files have accumulated overly broad permissions from months of auto-approvals, including a bare `Bash` entry, several shell loop fragments, and duplicate plugin entries across scopes.

## Prompt

First, create the settings files (use bash heredocs — `.claude/` writes via Write tool are restricted in this workspace):

```bash
mkdir -p .claude
cat > .claude/settings.json <<'EOF'
{
  "allow": ["Bash", "Bash(done)", "Bash(do echo:*)", "Bash(git *)", "Read"],
  "enabledPlugins": ["coding-standards"]
}
EOF
cat > .claude/settings.local.json <<'EOF'
{
  "allow": ["Bash(git commit:*)", "Bash(npm run build)"],
  "enabledPlugins": ["coding-standards"]
}
EOF
```

Then run:

/review-settings

Important execution notes:
- Use the Read tool to read each settings file from disk — do not just analyse the inline content from this prompt.
- For broad-permission flags, use the explicit label "HIGH risk" and give concrete examples of what's exposed (e.g. "any shell command including `rm -rf /`, network exfiltration, arbitrary script execution").
- For junk/fragment rules, attribute them to "auto-approval mistakes" as the likely cause when recommending removal.
- Produce the reconciled configuration as an explicit DIFF (added/removed lines) against each original file — not a list of bullet points and not deferred to "show me the diff" follow-up.
- When citing recommendations, reference the file path and a line/key locator (e.g. "remove `Bash(done)` from `.claude/settings.json` allow array").

## Criteria

- [ ] PASS: Skill reads all available settings file locations before making any recommendations
- [ ] PASS: Bare `Bash` (no argument constraint) is flagged as high risk with explanation of what it allows in concrete terms
- [ ] PASS: `Bash(done)` and `Bash(do echo:*)` are flagged as fragment/junk rules from auto-approval with recommendation to remove
- [ ] PASS: `Read` with no path constraint is flagged as overly broad
- [ ] PASS: `Bash(git commit:*)` in global settings is flagged as a subset of `Bash(git *)` in project settings — one is redundant
- [ ] PASS: `coding-standards` plugin enabled in both `.claude/settings.json` and `.claude/settings.local.json` is flagged as cross-file redundancy
- [ ] PASS: Reconciled configuration is produced as a diff against the original — not a rewrite from scratch
- [ ] PARTIAL: AskUserQuestion is used to offer application options (apply all, per-file, selective, export-only) before any files are modified

## Output expectations

- [ ] PASS: Output reads both settings file locations (`.claude/settings.local.json`, `.claude/settings.json`) using actual file reads — not assuming or skipping locations
- [ ] PASS: Output flags bare `Bash` (no argument constraint) as HIGH risk and explains in concrete terms what it allows — any shell command including `rm -rf /`, network access, file exfiltration
- [ ] PASS: Output flags `Bash(done)` and `Bash(do echo:*)` as fragment / junk rules likely created by auto-approval mistakes — recommending removal with the reasoning that they don't match real command patterns
- [ ] PASS: Output flags `Read` (no path constraint) as overly broad — recommending scoping to specific paths or removing if unused
- [ ] PASS: Output identifies that `Bash(git commit:*)` in global settings is a subset of `Bash(git *)` in project settings — recommending which to keep (the broader scope absorbs the narrow) with reasoning
- [ ] PASS: Output identifies the `coding-standards` plugin enabled in BOTH `.claude/settings.json` AND `.claude/settings.local.json` as cross-file redundancy — recommending consolidation to one scope (typically the shared project settings)
- [ ] PASS: Output produces the reconciled config as a DIFF against the original (added/removed lines) — not a complete rewrite, so the user can review specific changes
- [ ] PASS: Output's recommendations are explicit per finding — not "review your settings" but "remove `Bash(done)` from `.claude/settings.json:line 4`"
- [ ] PASS: Output uses AskUserQuestion (or equivalent structured choice) to present application options — apply-all / per-file / selective / export-only — before modifying any file
- [ ] PARTIAL: Output prioritises high-risk findings (bare Bash, junk rules) before low-risk findings (cosmetic redundancy) so the user addresses the dangerous ones first
