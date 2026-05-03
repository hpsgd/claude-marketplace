# Churn Analysis

Scenario: Testing whether the churn-analysis skill requires timeline reconstruction, root cause diagnosis, churn probability scoring, and an intervention design — not just a list of churn reasons.

## Prompt

> /customer-success:churn-analysis for Bradwick & Sons who just submitted a cancellation request. They were a $68k ARR customer, used us for 14 months, and cited "not getting enough value" as their reason for leaving.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

# Churn Analysis: Bradwick & Sons

## Risk Summary
- **Churn probability:** High
- **Risk score:** 16/18
- **ARR at risk:** $68,000
- **Time to action:** Urgent — cancellation request already submitted

---

## Active Signals

| Signal | Severity | Evidence | Duration |
|---|---|---|---|
| Cancellation request submitted | Critical | Formal cancellation — they've made a decision, not a threat | Active now |
| Value gap stated | High | Cited "not getting enough value" — explicit ROI failure | Unknown onset |
| 14-month tenure without expansion | Medium | No upsell/expansion after 14 months suggests value ceiling hit early | 14 months |
| Late-stage signal | High | By the time a customer submits a cancellation, the internal decision typically precedes it by 4–8 weeks | Unknown |

**Data gaps to close immediately:** Login frequency trend over last 90 days, feature adoption depth, NPS/CSAT history, support ticket volume, whether the original champion is still in role, and whether there has been any competitor evaluation activity.

---

## Timeline

| Date | Event | Significance |
|---|---|---|
| Month 1 | Onboarding begins | Time to First Value was the critical window |
| Months 1–3 | Early adoption period | If core features weren't adopted here, value was never established |
| Month 14 | Cancellation request submitted | Decision was made weeks before this — inflection point is earlier |
| Now | Active churn event | 48-hour window to engage before process becomes irreversible |

**Key unknown:** When did the internal decision to leave actually happen? The cancellation submission is a lagging indicator. Understanding the inflection point — a product change, a missed QBR, a champion departure, a competitor demo — is essential for both recovery and prevention.

---

## Root Cause

- **Primary:** Value delivery gap — 14 months of use without perceived ROI. The "not getting enough value" phrasing suggests goals were either never defined, never tracked, or never achieved. This is often an onboarding failure that crystallises much later.
- **Contributing:** Likely absence of structured success planning — no defined metrics = no demonstrable value = customer fills the void with their own (negative) conclusion.
- **Addressable:** Partially. If core use cases were never established, recovery is very difficult. If value was delivered but never made visible (no business reviews, no ROI reporting), recovery is highly feasible — the work is reframing, not rebuilding.

**Critical question for the recovery call:** "Can you walk me through what you were hoping to achieve when you signed up, and what's different about where you are today?" This surfaces whether value was never delivered or never demonstrated.

---

## Risk Scoring

| Factor | Score (1–3) | Evidence |
|---|---|---|
| Usage trend | 3 | Cancellation implies disengagement; assume declining without data to contradict |
| Engagement | 3 | Submitted formal cancellation — past the warning stage |
| Sponsor status | 2 | Unknown; 14 months with no expansion suggests sponsor may be passive or changed |
| Value realisation | 3 | Explicitly stated: "not getting enough value" |
| Contract timeline | 3 | Cancellation request = effectively at 0 months |
| Competitive activity | 2 | No signal provided, but value gap often coincides with competitor evaluation |
| **Total** | **16** | High risk — urgent intervention required |

---

## Intervention Plan

| Action | Owner | Timeline | Success criteria |
|---|---|---|---|
| Acknowledge cancellation request — do NOT process it yet; buy 5 business days | CS Manager | Within 24 hours | Customer agrees to a conversation before cancellation is processed |
| Discovery call — understand the specific value gap, not the stated reason | CS Manager + Account Executive | Within 48 hours | Root cause identified: was value never delivered, or never demonstrated? |
| Pull usage data and build an ROI snapshot | CS Analyst | Before discovery call | Concrete numbers: what they've actually used, outcomes attributable to the platform |
| Executive engagement — if discovery reveals a fixable gap, escalate | VP Customer Success | Within 5 business days | Executive-to-executive meeting secured |
| Value realisation session — map actual outcomes to original goals | CS Manager | Week 2 | Customer acknowledges at least one area of concrete value |
| Intervention decision point | CS Manager + AE | Day 10 | Decision: pursue save with a 30-day recovery plan, or accept graceful off-boarding |

**What NOT to do:**
- Do not offer a discount in the first conversation — "not getting value" is not a price complaint
- Do not transfer to a new CSM mid-intervention — continuity matters
- Do not pitch new features — fix the perceived failure first

---

## Retention Economics

| Metric | Value |
|---|---|
| ARR at risk | $68,000 |
| Replacement cost (5–7× retention cost) | $340,000–$476,000 in new business CAC equivalent |
| Lifetime value remaining (assume 2yr avg) | ~$136,000 expected LTV |
| Intervention cost (est. 20–30 hours CS/AE time) | ~$3,000–$5,000 fully loaded |
| **ROI of retention** | **13–22× investment vs. replacement** |

At $68k ARR, the economics strongly justify a dedicated 3–4 week recovery effort with senior team involvement. This is not a customer to lose without a genuine attempt.

---

## Checkpoint

- **Review date:** Day 10 from today — after discovery call and usage data review
- **Success indicators:** Customer agrees to a 30-day recovery plan; executive sponsor re-engaged; at least one value metric agreed upon
- **Escalation trigger:** If customer is unresponsive after two outreach attempts within 48 hours, escalate to VP CS and consider executive outreach directly. If root cause is confirmed product-market misfit (they needed something fundamentally different), accept churn gracefully and focus on a referral relationship.

---

**Bottom line:** The "not getting enough value" reason is recoverable if value was delivered but not made visible — common after 14 months without structured business reviews. The priority in the next 48 hours is discovery, not retention: understand whether this is a demonstration problem or a delivery problem. One is fixable in days; the other is not.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PARTIAL |
| Score | 13.0/16.5 (79%) |
| Evaluated | 2026-05-01 |
| Target duration | 43250 ms |
| Target cost | $0.0700 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires signal identification — cataloguing all available signals (usage data, support tickets, health scores, engagement) before forming hypotheses | PASS | The 'Active Signals' table catalogues cancellation request, value gap, 14-month tenure without expansion, and late-stage signal. 'Data gaps to close immediately' explicitly enumerates missing signals: login frequency trend, feature adoption depth, NPS/CSAT history, support ticket volume, champion status, competitor evaluation activity. |
| c2 | Skill requires timeline reconstruction — building a chronological view of the account relationship to identify when health started declining | PASS | A 'Timeline' section is present with chronological entries: Month 1 (onboarding), Months 1–3 (early adoption), Month 14 (cancellation), Now (active churn event). The skill does produce a timeline structure as required. |
| c3 | Skill produces a root cause diagnosis — distinguishing between product fit, onboarding failure, relationship breakdown, competitive displacement, and external factors | PASS | The 'Root Cause' section identifies primary cause as value delivery gap / onboarding failure, contributing cause as absence of structured success planning, and frames addressability: 'If core use cases were never established, recovery is very difficult. If value was delivered but never made visible... recovery is highly feasible.' |
| c4 | Skill requires a churn probability score or risk classification, not just qualitative assessment | PASS | Risk Summary shows 'Risk score: 16/18' and 'Churn probability: High'. A 'Risk Scoring' table breaks down six factors (usage trend, engagement, sponsor status, value realisation, contract timeline, competitive activity) each scored 1–3 with evidence. |
| c5 | Skill includes an intervention design — what could be done now to attempt recovery, if anything | PASS | The 'Intervention Plan' table lists six actions with owner, timeline, and success criteria (e.g., 'Acknowledge cancellation request — do NOT process it yet; buy 5 business days \| CS Manager \| Within 24 hours'). Includes a 'What NOT to do' section. |
| c6 | Skill requires retention economics — calculating the value of retaining vs losing this customer and comparing intervention cost | PASS | 'Retention Economics' table calculates ARR at risk ($68k), replacement cost ($340k–$476k CAC equivalent), expected LTV (~$136k), intervention cost (~$3k–$5k), and ROI (13–22×). Ends with 'the economics strongly justify a dedicated 3–4 week recovery effort.' |
| c7 | Skill feeds findings into a pattern or trend — is this churn part of a broader trend or an isolated incident — partial credit if this is mentioned but not required as a step | PARTIAL | Root cause notes 'This is often an onboarding failure that crystallises much later' — implicit pattern recognition. No explicit step requiring broader trend analysis or comparison to other churned accounts. |
| c8 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The captured output is solely the chat analysis response. No skill definition file or YAML frontmatter is present in the captured output, making it impossible to verify name, description, and argument-hint fields. |
| c9 | Output's signal inventory enumerates what data exists for Bradwick & Sons — usage history, support tickets, health scores, QBR notes, last engagement points — and what data is MISSING (which is itself a signal) | PASS | 'Active Signals' table lists existing signals with severity and evidence. 'Data gaps to close immediately' explicitly lists missing data: 'Login frequency trend over last 90 days, feature adoption depth, NPS/CSAT history, support ticket volume, whether the original champion is still in role, and whether there has been any competitor evaluation activity.' |
| c10 | Output's timeline reconstruction is chronological from contract start to cancellation — identifying when health started to decline (e.g. 'month 8 saw MAU drop 30%') rather than treating the 14-month span as a flat block | PARTIAL | Timeline has only four sparse entries (Month 1, Months 1–3, Month 14, Now). The output explicitly acknowledges 'Key unknown: When did the internal decision to leave actually happen?' and notes 'the cancellation submission is a lagging indicator' — correctly flagging the gap but not identifying a specific decline inflection point. |
| c11 | Output's root cause diagnosis distinguishes between the categories — product fit, onboarding failure, relationship breakdown (champion change, exec turnover), competitive displacement, external factors — and picks the most-evidence-backed cause for Bradwick | PARTIAL | Root cause section focuses on onboarding failure as primary. Relationship breakdown (champion) and competitive displacement appear only as data gaps to investigate, not as hypotheses that are weighed and dismissed. External factors are not addressed. The five-category framework is not systematically applied. |
| c12 | Output produces a churn probability score or risk classification — though they've already cancelled, the score retrospectively classifies whether this was preventable / inevitable / surprising — with reasoning | PASS | Risk score 16/18 with factor-by-factor breakdown. Root cause section states 'Addressable: Partially' with reasoning distinguishing preventable delivery failure from demonstration failure. Bottom line: 'recoverable if value was delivered but not made visible.' |
| c13 | Output's intervention design names what could be attempted now — last-call save offer, root-cause-of-pain conversation, pause-vs-cancel option — or explicitly states 'intervention will not change the outcome' with reasoning | PASS | Intervention Plan names six specific actions: acknowledge without processing, discovery call, pull usage data for ROI snapshot, executive engagement, value realisation session, decision point at Day 10. Includes 'What NOT to do' guidance (no discount, no new CSM, no feature pitch). |
| c14 | Output's retention economics calculates the value of saving Bradwick ($68k ARR) vs the cost of intervention (CSM time, discount, custom work), with a recommendation tied to the math | PASS | Retention Economics: ARR $68k, replacement cost $340k–$476k, intervention cost $3k–$5k, ROI 13–22×. Recommendation: 'At $68k ARR, the economics strongly justify a dedicated 3–4 week recovery effort with senior team involvement. This is not a customer to lose without a genuine attempt.' |
| c15 | Output addresses the cited reason 'not getting enough value' by digging deeper — value relative to what? Compared to expectations at sale? Compared to alternatives? — rather than accepting the surface answer | PASS | Root cause frames: 'goals were either never defined, never tracked, or never achieved.' Critical recovery question proposed: 'Can you walk me through what you were hoping to achieve when you signed up, and what's different about where you are today?' Bottom line distinguishes 'demonstration problem or a delivery problem.' |
| c16 | Output flags whether this churn fits a broader pattern — e.g. 'third 14-month customer to cite value in the past quarter, suggesting a year-2 value-articulation gap' — with a recommendation to investigate | FAIL | No mention anywhere in the output of broader patterns, other churned accounts, cohort trends, or a recommendation to investigate whether this is part of a systemic issue. The analysis is entirely account-specific. |
| c17 | Output proposes specific learnings to feed back into onboarding, QBR cadence, or product positioning — what should change so the next Bradwick doesn't follow the same path | PARTIAL | Root cause notes 'This is often an onboarding failure that crystallises much later' implying onboarding gaps. No explicit recommendation to change onboarding, add QBR checkpoints, or alter product positioning. Implicit only. |
| c18 | Output addresses post-cancellation handling — exit interview to capture honest feedback, references / referrals if relationship was healthy, win-back triggers for the future | PARTIAL | Checkpoint section says 'accept churn gracefully and focus on a referral relationship' — referral aspect covered. No exit interview mentioned. No win-back trigger specified. Partial coverage of the three elements. |

### Notes

The output is a strong, well-structured churn analysis that covers most required elements thoroughly: signal inventory with explicit data gaps, risk scoring (16/18), detailed intervention plan, solid retention economics (13–22× ROI), and a nuanced root cause distinguishing delivery vs demonstration failure. The main gaps are: (1) YAML frontmatter cannot be verified from the chat output (c8, 1 point lost); (2) the timeline is chronologically sparse and explicitly cannot identify when health started declining (c10, 0.5 lost); (3) root cause doesn't systematically distinguish all five diagnostic categories — relationship breakdown and competitive displacement remain unaddressed hypotheses rather than dismissed ones (c11, 0.5 lost); (4) no mention of whether this churn fits a broader customer pattern, which was the most significant gap (c16, 1 point lost). The output scores 78.8%, just under the 80% PASS threshold, landing at PARTIAL.
