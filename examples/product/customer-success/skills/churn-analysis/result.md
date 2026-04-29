# Output: Churn analysis

**Verdict:** PARTIAL
**Score:** 12.5/14 criteria met (89%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill requires signal identification — Step 1 catalogs six signal categories (usage decline, engagement drop, relationship deterioration, value gap, commercial friction, support escalation) with specific indicators and requires evidence with dates, metrics, and quotes
- [x] PASS: Skill requires timeline reconstruction — Step 2 mandates a chronological Date/Event/Signal table and requires identifying inflection point, accelerating decline, and correlated trigger events; it is a discrete required step
- [x] PASS: Skill produces a root cause diagnosis — Step 3 provides a 7-category taxonomy with questions and indicators per category; rules require naming a single primary root cause and distinguishing addressable from non-addressable causes
- [x] PASS: Skill requires a churn probability score or risk classification — Step 4 defines a 6-factor scoring rubric (1–3 per factor, total 6–18) with explicit Low/Medium/High thresholds and a numeric score in the output template
- [x] PASS: Skill includes an intervention design — Step 5 maps each root cause to a specific intervention approach with owner, first action within 48h, success criteria, checkpoint, and escalation path
- [x] PASS: Skill requires retention economics — Step 6 explicitly requires ARR at risk, replacement cost (with 5–7x benchmark stated), lifetime value remaining, intervention cost, and ROI ratio; output template mirrors all five metrics
- [~] PARTIAL: Skill feeds findings into a pattern or trend — no step, instruction, or output section asks whether this churn is part of a broader pattern or cohort trend; the argument-hint includes "churn pattern" but the process never prompts for it once inside an individual analysis
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — all three present and correctly formed

### Output expectations

- [x] PASS: Signal inventory enumerates available data and flags missing data — Step 1's structure surfaces gaps where evidence is absent per category; requiring "specific evidence (dates, metrics, quotes)" forces the agent to note what is unavailable as well as what exists
- [x] PASS: Timeline reconstruction is chronological from contract start to cancellation — the Date/Event/Signal table format with inflection point and correlated events drives month-by-month thinking; a 14-month account would naturally surface inflection points like "month 8 MAU drop"
- [x] PASS: Root cause diagnosis distinguishes categories and picks the most-evidence-backed cause — Step 3 covers all required categories and rules mandate a single PRIMARY root cause with evidence
- [x] PASS: Output produces a churn probability score classifying preventability — the 6-factor scoring framework applied retrospectively on a cancellation produces a classification with reasoning; the output template includes Risk Score and Time to Action
- [x] PASS: Intervention design names specific actions or states intervention will not change outcome — Step 5 maps root causes to interventions with a 48h first action; anti-patterns explicitly include "Assuming you can save everyone," which supports an explicit "won't change outcome" pathway
- [x] PASS: Retention economics calculates $68k ARR vs intervention cost with a recommendation — Step 6 table would be populated with the $68k figure; ROI ratio field produces a math-backed recommendation
- [x] PASS: "Not getting enough value" surface reason is interrogated deeper — Step 3's value delivery gap category asks "Are they achieving their stated goals?" and "ROI not demonstrated, success metrics not defined" — the skill pushes past the surface answer
- [ ] FAIL: Output flags whether churn fits a broader pattern — no step, prompt, or anti-pattern directs the agent to check whether this is the third 14-month customer citing value in the past quarter; entirely absent
- [~] PARTIAL: Output proposes specific learnings to feed back into onboarding, QBR cadence, or product positioning — anti-patterns section warns against common mistakes but no process step requires the agent to produce retrospective learnings for future accounts
- [ ] FAIL: Output addresses post-cancellation handling — exit interview, references/referrals if the relationship was healthy, and win-back triggers are entirely absent from the skill definition

## Notes

The skill is well-constructed for individual account diagnosis. The sequential six-step process is logical, the anti-patterns section is specific, and the numeric scoring rubric makes risk classification reproducible across CSMs. The two hard fails are both in the "after the save attempt" space: the skill treats every churn as an isolated event (no pattern detection) and stops at the intervention decision (no post-cancellation workflow). A single prompt — "Is this cancellation appearing across similar accounts?" — would close the pattern gap. Exit interview and win-back handling would require a new section, but it is a natural extension of retention economics.
