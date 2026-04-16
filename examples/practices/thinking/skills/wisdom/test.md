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
