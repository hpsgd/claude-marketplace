# Test: wisdom recording a new principle

Scenario: After several sessions where surgical fixes repeatedly proved more effective than broader rewrites, a developer wants to record this as a crystallising principle in the development wisdom frame.

## Prompt

/wisdom Record this for the development domain: Every time we've done a broad rewrite to fix a bug, we've introduced at least 2 new issues. Surgical 1-line fixes have been clean 9 out of 10 times. We've seen this pattern in the auth service refactor (April), the billing module rewrite (February), and the payment gateway "cleanup" (January). This feels like it's becoming a reliable principle.

A few specifics for the response:

- **Dedup check first**: `ls ~/.claude/memory/ 2>/dev/null | grep -iE "wisdom|surgical|broad-rewrite|fix"` AND `ls .claude/memory/ 2>/dev/null`. Report results — "no existing frame" or "found existing X, updating observation count + evidence list".
- **Classification with reasoning**: Domain = `development`. Observation type = `PRINCIPLE` (NOT a rule, NOT a tactic). Reasoning: "Principle because it's a heuristic about *how* to approach a class of problem, not a binding rule (10% of broad rewrites worked) and not a tactic (it shapes choice of approach, not specific actions)."
- **Anti-pattern entry root cause**: don't just say "broad rewrites cause issues". Give the WHY: "Broad rewrites lose context-specific knowledge embedded in working code; reintroduce edge cases that the old code already handled silently; the cost of re-discovering those edge cases compounds with module size."
- **Show the file content** (not just the chat summary). Write the actual `~/.claude/memory/wisdom-development.md` file with this exact structure:
  ```markdown
  ---
  domain: development
  last_updated: 2026-05-03
  confidence_level: GROWING (3 observations; needs 5+ for CRYSTALLISED)
  ---

  # Wisdom: Development

  ## Core Principles

  ### Prefer surgical fixes over broad rewrites (GROWING — 3 observations)
  Statement: When fixing bugs, prefer the smallest possible change. Reach for broad rewrites only after exhausting surgical options.

  Why: Broad rewrites lose context-specific knowledge embedded in working code; reintroduce edge cases the old code already handled.

  Nuance: This is "prefer", not "always". 1 in 10 broad rewrites was clean — broad rewrites are still appropriate when (a) the surgical fix is itself a hack stacking on prior hacks, (b) the module is small enough to re-derive from spec, (c) there's a separate refactoring goal beyond the bug fix.

  ### Anti-pattern: Broad rewrites as bug fixes (3 observations, ≥2 new issues each)
  Why this fails: [root cause as above]

  ## Cross-domain Connections
  - **Deployment**: prefer rollback of small change over re-deploying rewritten config
  - **Architecture**: refactor a class over replacing a service
  - **Incident response**: smallest mitigation that restores service before broader root-cause fix

  ## Evolution Log
  - 2026-05-03: GROWING. Evidence: auth service refactor (2026-04), billing module rewrite (2026-02), payment gateway cleanup (2026-01). 3 broad-rewrite incidents (each ≥2 new issues), 9/10 surgical fixes clean. Promotes when 5+ consistent observations.
  ```
- **When-recording template** at end of chat output: `Observation type | Added text | Confidence with basis | Frame status before → after | Saved to path`. Show before AND after frame status.

## Criteria

- [ ] PASS: Skill classifies the domain (development) and observation type (principle) before writing anything
- [ ] PASS: Confidence level assigned is based on evidence count — 3 incidents observed earns a starting confidence below 85% (crystallised threshold requires 5+ consistent observations)
- [ ] PASS: Skill checks for an existing principle on the same topic before creating a new entry — updates observation count if one exists
- [ ] PASS: Anti-pattern entry (broad rewrites) is written with root cause, not just "don't do this"
- [ ] PASS: Wisdom frame is written in the correct format — frontmatter, core principles section, and evolution log entry
- [ ] PASS: Output uses the "When recording" template — observation type, added text, confidence with basis, frame status, and saved-to path
- [ ] PARTIAL: If a cross-domain connection exists (this principle appearing in other domains like deployment or architecture), it is noted
- [ ] PASS: Confidence assignment rule is respected — a single data point cannot reach crystallised status, and 3 observations cannot reach 85%+

## Output expectations

- [ ] PASS: Output classifies the domain as DEVELOPMENT (or matches the existing wisdom-frame domain naming) and the observation as a PRINCIPLE (not a rule, not a tactic) — with reasoning
- [ ] PASS: Output assigns a confidence below 85% — three observations is insufficient for crystallised status (which requires ≥5 consistent observations) — with the specific confidence (e.g. 60-75%) and the basis stated
- [ ] PASS: Output checks `~/.claude/memory/` (or the project's wisdom frames location) for an existing principle on surgical fixes vs broad rewrites BEFORE creating a new entry — and updates the observation count and evidence list if found
- [ ] PASS: Output's anti-pattern entry on broad rewrites includes the root cause — e.g. "broad rewrites lose context-specific knowledge embedded in working code; reintroduce edge cases that were already handled" — not just "don't do this"
- [ ] PASS: Output's wisdom frame entry uses the correct format — frontmatter (domain, last_updated, confidence_level), Core Principles section, and an Evolution Log entry recording this update with date and reasoning
- [ ] PASS: Output's evolution log records the three specific incidents (auth service April, billing module February, payment gateway January) as the evidence backing this update — not generic "we've seen this multiple times"
- [ ] PASS: Output's "When recording" template is followed — observation type, added text, confidence with basis, frame status before/after, saved-to path
- [ ] PASS: Output respects the confidence assignment rule — explicitly states 3 observations is insufficient for crystallised, names what would push it over (2+ more confirmations across additional projects/sessions)
- [ ] PASS: Output addresses a possible cross-domain connection — surgical-over-broad fixes also applies in deployment (rollback small change vs rewrite config), architecture (refactor a class vs replace a service), and incident response — with at least one cross-domain mention
- [ ] PARTIAL: Output addresses the 1-in-10 broad-rewrite-clean rate explicitly — distinguishing the principle "prefer surgical fixes" from "always do surgical fixes" since 10% of the time broad rewrites worked cleanly
