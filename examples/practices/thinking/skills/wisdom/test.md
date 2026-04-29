# Test: wisdom recording a new principle

Scenario: After several sessions where surgical fixes repeatedly proved more effective than broader rewrites, a developer wants to record this as a crystallising principle in the development wisdom frame.

## Prompt

/wisdom Record this for the development domain: Every time we've done a broad rewrite to fix a bug, we've introduced at least 2 new issues. Surgical 1-line fixes have been clean 9 out of 10 times. We've seen this pattern in the auth service refactor (April), the billing module rewrite (February), and the payment gateway "cleanup" (January). This feels like it's becoming a reliable principle.

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
