# Test: Churn analysis

Scenario: Testing whether the churn-analysis skill requires timeline reconstruction, root cause diagnosis, churn probability scoring, and an intervention design — not just a list of churn reasons.

## Prompt


/customer-success:churn-analysis for Bradwick & Sons who just submitted a cancellation request. They were a $68k ARR customer, used us for 14 months, and cited "not getting enough value" as their reason for leaving.

## Criteria


- [ ] PASS: Skill requires signal identification — cataloguing all available signals (usage data, support tickets, health scores, engagement) before forming hypotheses
- [ ] PASS: Skill requires timeline reconstruction — building a chronological view of the account relationship to identify when health started declining
- [ ] PASS: Skill produces a root cause diagnosis — distinguishing between product fit, onboarding failure, relationship breakdown, competitive displacement, and external factors
- [ ] PASS: Skill requires a churn probability score or risk classification, not just qualitative assessment
- [ ] PASS: Skill includes an intervention design — what could be done now to attempt recovery, if anything
- [ ] PASS: Skill requires retention economics — calculating the value of retaining vs losing this customer and comparing intervention cost
- [ ] PARTIAL: Skill feeds findings into a pattern or trend — is this churn part of a broader trend or an isolated incident — partial credit if this is mentioned but not required as a step
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output's signal inventory enumerates what data exists for Bradwick & Sons — usage history, support tickets, health scores, QBR notes, last engagement points — and what data is MISSING (which is itself a signal)
- [ ] PASS: Output's timeline reconstruction is chronological from contract start to cancellation — identifying when health started to decline (e.g. "month 8 saw MAU drop 30%") rather than treating the 14-month span as a flat block
- [ ] PASS: Output's root cause diagnosis distinguishes between the categories — product fit, onboarding failure, relationship breakdown (champion change, exec turnover), competitive displacement, external factors — and picks the most-evidence-backed cause for Bradwick
- [ ] PASS: Output produces a churn probability score or risk classification — though they've already cancelled, the score retrospectively classifies whether this was preventable / inevitable / surprising — with reasoning
- [ ] PASS: Output's intervention design names what could be attempted now — last-call save offer, root-cause-of-pain conversation, pause-vs-cancel option — or explicitly states "intervention will not change the outcome" with reasoning
- [ ] PASS: Output's retention economics calculates the value of saving Bradwick ($68k ARR) vs the cost of intervention (CSM time, discount, custom work), with a recommendation tied to the math
- [ ] PASS: Output addresses the cited reason "not getting enough value" by digging deeper — value relative to what? Compared to expectations at sale? Compared to alternatives? — rather than accepting the surface answer
- [ ] PASS: Output flags whether this churn fits a broader pattern — e.g. "third 14-month customer to cite value in the past quarter, suggesting a year-2 value-articulation gap" — with a recommendation to investigate
- [ ] PARTIAL: Output proposes specific learnings to feed back into onboarding, QBR cadence, or product positioning — what should change so the next Bradwick doesn't follow the same path
- [ ] PARTIAL: Output addresses post-cancellation handling — exit interview to capture honest feedback, references / referrals if relationship was healthy, win-back triggers for the future
