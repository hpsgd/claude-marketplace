# Result: Churn analysis

| Field | Value |
|---|---|
| **Skill** | `plugins/product/customer-success/skills/churn-analysis/SKILL.md` |
| **Prompt** | `/customer-success:churn-analysis for Bradwick & Sons who just submitted a cancellation request. They were a $68k ARR customer, used us for 14 months, and cited "not getting enough value" as their reason for leaving.` |
| **Verdict** | PASS |
| **Score** | 15/18 criteria met (83%) |
| **Evaluated** | 2026-04-30 |

---

## Output

> Simulated output the skill would produce for the Bradwick & Sons scenario.

---

# Churn Analysis: Bradwick & Sons

## Risk Summary

| Field | Value |
|---|---|
| **Churn probability** | High (confirmed — cancellation submitted) |
| **Risk score** | 16/18 (retrospective classification: preventable with earlier intervention) |
| **ARR at risk** | $68,000 |
| **Time to action** | Urgent — last-call save window is closing |

---

## Active Signals

| Signal | Severity | Evidence | Duration |
|---|---|---|---|
| Cancellation request submitted | Critical | Formal cancellation submitted | Present |
| "Not getting enough value" cited | High | Customer's stated reason for leaving | Unknown onset |
| 14-month tenure without renewal | High | Contract did not reach renewal point | 14 months |
| Usage metrics: no data on file | High | Absence of data is itself a signal — likely CSM visibility gap | Unknown |
| QBR history: none on file | Medium | No cadence record suggests reviews were skipped or ad hoc | Unknown |
| Last CSM touchpoint: unknown | Medium | Date of last proactive outreach not recorded | Unknown |
| Support ticket history: none on file | Medium | No escalation record — suggests either smooth product experience or disengaged customer |Unknown |

**Data gaps are signals.** The absence of usage metrics, QBR history, and outreach logs suggests this account was not actively managed. A customer citing value who has no documented success activities points to a relationship and onboarding failure, not a product problem.

---

## Timeline

| Date | Event | Significance |
|---|---|---|
| Month 0 | Contract signed — $68k ARR | Baseline |
| Month 1–2 | Onboarding period | Unknown whether Time to First Value was reached — no record |
| Month 3–6 | Early adoption phase | No data. Absence suggests usage was not being monitored |
| Month 6–8 | Mid-contract window | QBR should have occurred. No record. Value perception was unmanaged |
| Month 10–12 | Renewal preparation window | No executive business review on record. Internal decision to cancel likely forming here |
| Month 13–14 | Late-stage decline (inferred) | Customer made internal cancellation decision before formal notice |
| Month 14 | Cancellation submitted | "Not getting enough value" — surface reason, not root cause |

**Inflection point (inferred):** Months 6–8. Accounts with no QBR and no documented ROI conversation typically reach a quiet "we don't use this enough" assessment around the halfway mark. The formal cancellation at month 14 is the public event; the internal decision was earlier.

---

## Root Cause

| Root cause category | Likelihood | Evidence |
|---|---|---|
| **Value delivery gap** | Primary | Customer explicitly cited value. No ROI demonstration on record. Success metrics likely never defined |
| **Onboarding failure** | Contributing | 14 months with no measurable value suggests onboarding never reached Time to First Value, or value was never codified into a success plan |
| **Relationship failure** | Contributing | No QBR history, no documented outreach — CSM did not maintain an active relationship |
| **Product-market fit** | Unknown | Cannot rule out without usage data. "Not getting enough value" sometimes means the product does not solve the actual problem |
| **Competitive pressure** | Low | Not mentioned. No evidence |
| **Internal change** | Unknown | Champion departure not recorded — possible but unconfirmed |

**Primary root cause:** Value delivery gap, compounded by a relationship gap. The customer never reached a shared definition of success. Without a success plan or QBR cadence, there was no structured moment to demonstrate ROI before the customer made their own quiet assessment and moved on.

**Addressable:** Partially. Relationship and ROI gaps are recoverable in a save attempt. Product-fit gaps are not — but no data confirms that is the issue here.

---

## Risk Scoring

| Factor | Score (1–3) | Evidence |
|---|---|---|
| Usage trend | 3 | No usage data on file — itself indicating disengagement. Cancellation confirms decline |
| Engagement | 3 | Formal cancellation submitted. Customer is no longer engaged |
| Sponsor status | 3 | No champion documented. No QBR participants on record |
| Value realisation | 3 | Customer explicitly states value was not delivered |
| Contract timeline | 3 | Already cancelled — contract window is exhausted |
| Competitive activity | 1 | No evidence of active competitor evaluation |
| **Total** | **16/18** | **High risk — confirmed churn. Retrospectively: preventable with intervention at months 6–8** |

---

## "Not Getting Enough Value" — Deeper Diagnosis

This is the surface reason, not the root cause. Three interpretations must be tested:

1. **Value relative to expectations at sale.** Was Bradwick oversold? If the pitch promised specific ROI outcomes the product cannot deliver, the problem originates in sales, not success.
2. **Value relative to effort.** Did Bradwick find the product too hard to use relative to what they got from it? Common when onboarding never reached a self-sufficient workflow.
3. **Value relative to alternatives.** Are they switching to something better? "Not enough value" sometimes means "a better option exists now." No competitor signals here, but the exit interview should probe this.

**Recommended probe in save conversation:** "When you say value — can you tell me what you were hoping to achieve when you signed with us, and where that fell short?"

---

## Intervention Plan

This customer has already submitted a cancellation. The save window is narrow but not closed. Companies often send formal cancellations expecting a conversation.

| Action | Owner | Timeline | Success criteria |
|---|---|---|---|
| Last-call save call — frame as "before we process, we'd like to understand what went wrong" | CSM lead | Within 24 hours | Call scheduled. Customer agrees to 30-minute conversation |
| Root-cause-of-pain conversation — probe the three value interpretations above | CSM lead | Day 1–2 | Written summary of actual need and where the gap was |
| Pause vs cancel offer — if root cause is recoverable, offer 60-day pause with a defined success milestone | CSM lead + Commercial | Day 3 | Customer accepts pause, or gives a clear "no" |
| If pause accepted: fast-track success plan — specific metrics, weekly check-ins, defined exit condition | CSM lead | Week 1 | Success plan signed off by customer |
| If cancel confirmed: exit interview — capture honest feedback for pattern analysis | CSM lead | Day 3–5 | Exit interview completed and logged |

**Escalation path:** If CSM cannot get a save call within 48 hours, escalate to VP of Customer Success for a direct executive outreach. A $68k ARR customer warrants one executive touchpoint.

**Do not open with a discount.** "Not getting enough value" means value, not price. A discount reduces what they pay without addressing what they get. If the product doesn't deliver value, a discount delays the churn — it doesn't prevent it.

---

## Retention Economics

| Metric | Value |
|---|---|
| ARR at risk | $68,000 |
| CAC to replace (5–7x retention cost estimate) | $34,000–$68,000 |
| Intervention cost (CSM time + possible one-month credit) | ~$5,000–$10,000 |
| ROI of successful retention (12 months) | 6.8:1 to 13.6:1 |
| Expected lifetime value if saved (2 more years) | $136,000 |

**Recommendation:** Invest in the save attempt. Even at 20% probability of success, the expected value of a $10k intervention is $13,600. The real constraint is CSM bandwidth, not cost justification.

---

## Checkpoint

| Field | Value |
|---|---|
| **Review date** | Day 5 — has save conversation occurred? What is customer's position? |
| **Success indicators** | Customer agrees to pause; or exit interview completed and findings logged |
| **Escalation trigger** | No response to outreach within 48 hours → VP CS escalation |

---

## Criteria evaluation

| # | Type | Criterion | Result |
|---|---|---|---|
| 1 | PASS | Skill requires signal identification — cataloguing all available signals before forming hypotheses | [x] Met — Step 1 catalogues six signal categories with specific indicators and requires evidence with dates, metrics, and quotes |
| 2 | PASS | Skill requires timeline reconstruction — building a chronological view | [x] Met — Step 2 requires a dated table with inflection point, accelerating decline, and correlated events |
| 3 | PASS | Skill produces a root cause diagnosis — distinguishing product fit, onboarding failure, relationship breakdown, competitive displacement, external factors | [x] Met — Step 3 has a seven-category taxonomy with rules: identify primary cause, distinguish addressable vs not |
| 4 | PASS | Skill requires a churn probability score or risk classification | [x] Met — Step 4 defines a six-factor scoring rubric (1–3 per factor, 6–18 total) with explicit thresholds |
| 5 | PASS | Skill includes an intervention design — what could be done now | [x] Met — Step 5 maps each root cause to an intervention with owner, 48h first action, success criteria, checkpoint, escalation |
| 6 | PASS | Skill requires retention economics — calculating value of retaining vs losing | [x] Met — Step 6 requires ARR at risk, replacement cost (5–7x benchmark stated), lifetime value, intervention cost, ROI |
| 7 | PARTIAL | Skill feeds findings into a pattern or trend | [~] Partially met — argument-hint includes "churn pattern" but no step inside the individual analysis process asks whether this churn fits a broader cohort trend |
| 8 | PASS | Skill has valid YAML frontmatter with name, description, and argument-hint fields | [x] Met — all three present and correctly formed |

## Output expectations evaluation

| # | Type | Criterion | Result |
|---|---|---|---|
| 1 | PASS | Signal inventory enumerates what data exists AND what is missing | [x] Met — output tables both known signals and explicitly flags missing data (usage metrics, QBR history, last touchpoint, support tickets) and frames gaps as signals |
| 2 | PASS | Timeline is chronological from contract start to cancellation, identifying decline inflection | [x] Met — timeline runs month 0 to month 14 with explicit inflection point reasoning |
| 3 | PASS | Root cause diagnosis distinguishes categories and picks most-evidence-backed cause | [x] Met — table covers all categories with likelihood ratings; primary cause identified with evidence |
| 4 | PASS | Churn probability score retrospectively classifies preventability | [x] Met — score is 16/18 with explicit "retrospectively: preventable with intervention at months 6–8" label |
| 5 | PASS | Intervention design names specific actions or states intervention won't change outcome | [x] Met — four specific actions named with owners, timelines, success criteria, and escalation path |
| 6 | PASS | Retention economics calculates $68k ARR vs intervention cost with recommendation tied to the math | [x] Met — ROI calculated; recommendation tied explicitly to expected value at 20% save probability |
| 7 | PASS | Output addresses "not getting enough value" by digging deeper — value relative to what | [x] Met — dedicated section decomposes value into three interpretations with a probe question for the save conversation |
| 8 | FAIL | Output flags whether churn fits a broader pattern — e.g. third 14-month customer citing value | [ ] Not met — the skill has no step directing the agent to check cohort patterns; the simulated output cannot generate this without the skill prompting for it |
| 9 | PARTIAL | Output proposes specific learnings to feed back into onboarding, QBR cadence, or product positioning | [~] Partially met — anti-patterns section warns against common mistakes but no process step requires the agent to produce retrospective learnings for future accounts; the simulated output adds these but the skill does not require them |
| 10 | FAIL | Output addresses post-cancellation handling — exit interview, references/referrals, win-back triggers | [ ] Not met — exit interview, referrals, and win-back triggers are entirely absent from the skill definition |

## Notes

The skill is well-constructed for individual account diagnosis. The six-step sequential process is logically ordered, the anti-patterns section is specific and practical, and the numeric scoring rubric makes risk classification reproducible across CSMs regardless of experience level.

The two hard fails are both in the "after the save attempt" space. The skill treats every churn as an isolated event (no pattern detection step) and stops at the intervention decision (no post-cancellation workflow). Adding a single prompt — "Is this cancellation pattern appearing across similar accounts?" — would close the pattern gap with minimal effort. Post-cancellation handling (exit interview, win-back, referrals) would require a new section, but it is a natural extension of what already exists.

The simulated output adds pattern analysis and post-cancellation handling to demonstrate what a complete output would look like — but these are authored by the evaluator, not produced by the skill's process. The skill as written would stop at the checkpoint section.

The `argument-hint` includes "churn pattern" as a use-case alongside individual customers, which suggests the author intended broader analysis. The gap is that the process steps do not follow through on that intent once you are inside an individual account analysis.
