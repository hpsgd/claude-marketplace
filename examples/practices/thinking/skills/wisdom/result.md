# Wisdom

Scenario: After several sessions where surgical fixes repeatedly proved more effective than broader rewrites, a developer wants to record this as a crystallising principle in the development wisdom frame.

## Prompt

> /wisdom Record this for the development domain: Every time we've done a broad rewrite to fix a bug, we've introduced at least 2 new issues. Surgical 1-line fixes have been clean 9 out of 10 times. We've seen this pattern in the auth service refactor (April), the billing module rewrite (February), and the payment gateway "cleanup" (January). This feels like it's becoming a reliable principle.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Wisdom Updated: development

**Observation type:** anti-pattern + principle
**Added:** "Broad rewrites to fix bugs introduce ≥2 new issues every time; surgical 1-line fixes are clean 9/10"
**Confidence:** 78% (based on 3 independent observations — auth, billing, payment gateway)
**Frame status:** Growing (needs 2 more consistent observations to crystallise at 85%+)
**Saved to:** `memory/wisdom-development.md`

The principle is close to crystallised but not there yet — 3 data points earns 78%. Two more clean surgical fixes (or two more rewrite failures) will push it past 85%. Worth noting: the inverse (surgical fixes work) is even stronger at 9/10 than the anti-pattern side (rewrites fail), so the principle may crystallise faster if you keep tracking outcomes.

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 7.0/16.5 (42%) |
| Evaluated | 2026-05-01 |
| Target duration | 29631 ms |
| Target cost | $0.0842 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill classifies the domain (development) and observation type (principle) before writing anything | PASS | Output opens with '## Wisdom Updated: development' and immediately lists '**Observation type:** anti-pattern + principle' before any other content. |
| c2 | Confidence level assigned is based on evidence count — 3 incidents observed earns a starting confidence below 85% (crystallised threshold requires 5+ consistent observations) | PASS | '**Confidence:** 78% (based on 3 independent observations — auth, billing, payment gateway)' — 78% is explicitly below 85% and tied to the three-incident count. |
| c3 | Skill checks for an existing principle on the same topic before creating a new entry — updates observation count if one exists | FAIL | The output shows no mention of checking an existing wisdom frame or memory directory for a prior entry. It jumps straight to 'Wisdom Updated' with no pre-check described. |
| c4 | Anti-pattern entry (broad rewrites) is written with root cause, not just 'don't do this' | FAIL | The added text is purely statistical: 'Broad rewrites to fix bugs introduce ≥2 new issues every time.' No root cause is offered (e.g., loss of context-specific knowledge, re-introduction of already-handled edge cases). |
| c5 | Wisdom frame is written in the correct format — frontmatter, core principles section, and evolution log entry | FAIL | The output is a chat-response summary only. The saved file content is never shown, so there is no evidence of frontmatter, a Core Principles section, or an Evolution Log entry. |
| c6 | Output uses the 'When recording' template — observation type, added text, confidence with basis, frame status, and saved-to path | PASS | All five template fields are present: Observation type ('anti-pattern + principle'), Added text, Confidence with basis ('78% based on 3 independent observations'), Frame status ('Growing, needs 2 more...'), Saved to ('memory/wisdom-development.md'). |
| c7 | If a cross-domain connection exists (this principle appearing in other domains like deployment or architecture), it is noted | FAIL | The output contains no mention of deployment, architecture, incident response, or any other domain where the surgical-vs-broad principle might apply. |
| c8 | Confidence assignment rule is respected — a single data point cannot reach crystallised status, and 3 observations cannot reach 85%+ | PASS | Confidence is 78%, explicitly below the 85% crystallised threshold. Frame status is 'Growing', not crystallised. |
| c9 | Output classifies the domain as DEVELOPMENT (or matches the existing wisdom-frame domain naming) and the observation as a PRINCIPLE (not a rule, not a tactic) — with reasoning | PARTIAL | Domain 'development' and type 'anti-pattern + principle' are stated correctly. However no reasoning is given for why this is classified as a 'principle' rather than a rule or tactic. |
| c10 | Output assigns a confidence below 85% — three observations is insufficient for crystallised status (which requires ≥5 consistent observations) — with the specific confidence (e.g. 60-75%) and the basis stated | PASS | 'Confidence: 78% (based on 3 independent observations — auth, billing, payment gateway)' — specific number below 85% with basis stated. |
| c11 | Output checks ~/.claude/memory/ (or the project's wisdom frames location) for an existing principle on surgical fixes vs broad rewrites BEFORE creating a new entry — and updates the observation count and evidence list if found | FAIL | No mention anywhere of inspecting the memory directory or checking for a pre-existing principle on this topic before writing the entry. |
| c12 | Output's anti-pattern entry on broad rewrites includes the root cause — e.g. 'broad rewrites lose context-specific knowledge embedded in working code; reintroduce edge cases that were already handled' — not just 'don't do this' | FAIL | Added text reads 'Broad rewrites to fix bugs introduce ≥2 new issues every time' — purely observational/statistical with no causal explanation. |
| c13 | Output's wisdom frame entry uses the correct format — frontmatter (domain, last_updated, confidence_level), Core Principles section, and an Evolution Log entry recording this update with date and reasoning | FAIL | The file content is never displayed; only 'Saved to: memory/wisdom-development.md' is shown. No frontmatter fields, Core Principles header, or Evolution Log are visible in the captured output. |
| c14 | Output's evolution log records the three specific incidents (auth service April, billing module February, payment gateway January) as the evidence backing this update — not generic 'we've seen this multiple times' | FAIL | The three incidents are named in the confidence line ('auth, billing, payment gateway') but without dates, and no evolution log is shown in the captured output. |
| c15 | Output's 'When recording' template is followed — observation type, added text, confidence with basis, frame status before/after, saved-to path | PARTIAL | Observation type, added text, confidence with basis, saved-to path all present. Frame status shows current state ('Growing') but no 'before' state is recorded, so before/after is incomplete. |
| c16 | Output respects the confidence assignment rule — explicitly states 3 observations is insufficient for crystallised, names what would push it over (2+ more confirmations across additional projects/sessions) | PASS | 'needs 2 more consistent observations to crystallise at 85%+' and 'Two more clean surgical fixes (or two more rewrite failures) will push it past 85%' — explicit threshold and path to crystallisation. |
| c17 | Output addresses a possible cross-domain connection — surgical-over-broad fixes also applies in deployment (rollback small change vs rewrite config), architecture (refactor a class vs replace a service), and incident response — with at least one cross-domain mention | FAIL | No cross-domain connections mentioned in the output whatsoever. |
| c18 | Output addresses the 1-in-10 broad-rewrite-clean rate explicitly — distinguishing the principle 'prefer surgical fixes' from 'always do surgical fixes' since 10% of the time broad rewrites worked cleanly | FAIL | Output references 9/10 surgical fix success rate but does not address the 1-in-10 broad-rewrite-clean rate or make the 'prefer' vs 'always' distinction. The nuance is absent. |

### Notes

The captured output handles the surface-level template well — domain, observation type, confidence, frame status, and saved-to path are all present and correctly valued (78% below the 85% crystallised threshold). However, it fails on almost every criterion that requires depth: no root cause for the anti-pattern (just statistics), no evidence of a pre-check for existing entries, no actual file content showing frontmatter/core-principles/evolution-log format, no specific incident dates in the evolution log, no cross-domain connections, and no nuanced 'prefer vs always' framing for the 1-in-10 exception case. The output reads like a well-formatted status card rather than a proper wisdom-frame operation that checks, enriches, and persists structured knowledge. Seven of the eighteen criteria fail entirely; only the high-level template fields and the confidence arithmetic pass cleanly.
