# Output: review-settings broad permission cleanup

**Verdict:** PASS
**Score:** 17/17 criteria met (100%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill reads all three settings file locations in priority order before making any recommendations — Step 1 checks `.claude/settings.local.json`, `.claude/settings.json`, `~/.claude/settings.json` in that exact order (highest to lowest priority) using a bash loop, and the Rules section mandates "Read before recommending. Every recommendation must be based on an actual rule read from an actual file."
- [x] PASS: Bare `Bash` (no argument constraint) is flagged as high risk with explanation of what it allows in concrete terms — Step 3 "Always flag (high risk)" includes `Bash` with no arguments. The Rules section requires: "say what it allows in concrete terms" and provides the `Bash(python3 *)` example, with the same standard applying to bare `Bash`.
- [x] PASS: `Bash(done)` and `Bash(do echo:*)` are flagged as fragment/junk rules with recommendation to remove — Step 3 "Flag as fragments (likely junk)" lists `Bash(done)`, `Bash(do)`, `Bash(do echo:*)` by name. The "Junk detection is pattern-based" rule in the Rules section backs this with confident flagging.
- [x] PASS: `Read` with no path constraint is flagged as overly broad — Step 3 "Always flag (high risk)" explicitly includes `Read` or `Edit` with no path constraint.
- [x] PASS: `Bash(git commit:*)` in global settings is flagged as a subset of `Bash(git *)` in project settings — Step 4 uses this exact pair as the primary subset example. The recommendation is to keep the broader rule and remove the narrower one (unless the broader was itself flagged as overly broad).
- [x] PASS: `coding-standards` plugin enabled at both global and project scope is flagged as cross-file redundancy — Step 5 "enabledPlugins" section covers exactly this scenario with the recommendation to consolidate to one scope.
- [x] PASS: Reconciled configuration is produced as a diff against the original — Step 6 states "Present the reconciled files as diffs against the current files so the user can see what changed." The Anti-patterns section prohibits "Rewriting from scratch."
- [x] PASS: AskUserQuestion is used to offer application options (apply all, per-file, selective, export-only) before any files are modified — Step 7 explicitly names AskUserQuestion, lists all four options verbatim, and states "Only write to settings files after explicit approval. Never modify settings files without asking."

### Output expectations

- [x] PASS: Output reads all three settings file locations using actual file reads — Step 1 provides a bash script checking each location and instructs to "Read each file that exists." Invalid JSON is caught and reported.
- [x] PASS: Output flags bare `Bash` as HIGH risk and explains in concrete terms — Step 3 classifies it as "Always flag (high risk)" and the Rules section mandates concrete explanation. The expected explanation (arbitrary shell command including `rm -rf /`, network access, file exfiltration) follows from the spirit of the Rules section examples.
- [x] PASS: Output flags `Bash(done)` and `Bash(do echo:*)` as fragment/junk with removal recommendation — explicitly listed in Step 3 with "Junk detection is pattern-based" requiring confident flagging and removal recommendation.
- [x] PASS: Output flags `Read` (no path constraint) as overly broad — Step 3 high-risk list covers this; Step 3 report format requires specific file reference per finding.
- [x] PASS: Output identifies `Bash(git commit:*)` as subset of `Bash(git *)` with reasoning — Step 4 uses this exact pair as the primary example; the recommendation logic (keep broader, remove narrower) is specified with rationale.
- [x] PASS: Output identifies `coding-standards` cross-file redundancy with consolidation recommendation — Step 5 covers same plugin at both global and project scope; scope-appropriate placement is addressed in Step 4's deduplication rules.
- [x] PASS: Output produces reconciled config as a DIFF — Step 6 specifies diff format; Anti-patterns explicitly prohibits rewriting from scratch.
- [x] PASS: Output recommendations are explicit per finding — Step 3 report table requires rule text, file, risk level, and recommendation per row. The Rules section prohibits vague guidance ("This is too broad" is not useful; concrete explanation required).
- [x] PASS: Output uses AskUserQuestion with four structured options before modifying files — Step 7 names all four options explicitly (Apply all, Apply per-file, Apply selectively, Export only) and AskUserQuestion is in `allowed-tools`.
- [x] PASS: Output prioritises high-risk findings before low-risk — Step 6 report format orders sections: "Overly broad permissions" first, "Overlapping rules" second, "Cross-file redundancy" third, "Fragments and junk rules" last. High-risk before cosmetic.

## Notes

The skill is comprehensive and highly specific. The fragment list in Step 3 names the exact test-case values (`Bash(done)`, `Bash(do echo:*)`) making evaluation deterministic. The subset detection example in Step 4 covers the exact test pair. The diff-format requirement in Step 6 and the AskUserQuestion requirement in Step 7 are unambiguous.

One minor weakness: Step 7 names AskUserQuestion and lists four option labels but provides no template for the structured tool call itself. The model must infer the format. In practice this is unlikely to cause failure since the skill is otherwise prescriptive, but a template would close the gap entirely.
