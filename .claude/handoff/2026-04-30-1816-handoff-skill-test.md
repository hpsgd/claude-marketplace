# Handoff: handoff skill — manual test in progress

## Context

Building `/handoff` skill in `plugins/practices/thinking/skills/handoff/SKILL.md`
to standardise session-to-session handoffs. Optional skill, not a hook. Three
modes: `write`, `resume`, `list`.

User asked to test before adding to evaluator harness. This handoff doc itself
is the test artefact for `/handoff write` mode.

## What changed

- Wrote `plugins/practices/thinking/skills/handoff/SKILL.md`
- Registered in root `README.md` under thinking plugin's skill table
- No commits yet — skill source is local, not in plugin cache

## State at handoff

| Field | Value |
|---|---|
| Branch | `main` |
| Last commit | `fc47c42 fix(thinking): pick highest plugin version and prune stale cache dirs` |
| Dirty files | `.claude/learnings/manifest.json`, `.claude/settings.json`, `README.md` |
| Untracked | `.claude/handoff-rule-install-fix.md`, `plugins/practices/thinking/skills/handoff/`, `.claude/handoff/` |
| In-flight | manual test of skill modes; harness `test.md` not written yet |

Bug found during list-mode test: zsh glob errors when `.claude/handoff/*.md`
matches nothing. SKILL.md uses bare `ls -1t` which fails. Needs `find`-based
command instead.

## Verify in new session

1. `cat plugins/practices/thinking/skills/handoff/SKILL.md` — confirm skill
   exists with three modes
2. `grep -n handoff README.md` — confirm registry entry on the thinking
   skill table
3. `ls .claude/handoff/` — should show this file
4. Confirm bug fix landed: SKILL.md uses `find` (or `[ -d ... ]` guard) before
   listing handoff files, not bare zsh glob
5. Confirm `examples/practices/thinking/skills/handoff/test.md` exists with
   write/resume/list scenarios
6. Run `/evaluate examples/practices/thinking/skills/handoff` if results
   needed

## Failure modes to watch

- **Skill not invocable via Skill tool:** plugin cache hasn't refreshed.
  Either commit + release + reload, or copy `SKILL.md` into
  `~/.claude/plugins/cache/turtlestack/thinking/<version>/skills/handoff/`
  for local testing
- **List mode still errors on missing dir:** the fix didn't land in SKILL.md
- **README registry entry missing:** the README edit was reverted

## Files of interest

- `plugins/practices/thinking/skills/handoff/SKILL.md` — skill definition
- `plugins/practices/thinking/skills/learning/SKILL.md` — pattern reference
- `plugins/practices/plugin-curator/skills/evaluate/SKILL.md` — harness contract
- `examples/practices/thinking/skills/learning/test.md` — test.md template
- `README.md` line 325 — skill table entry
