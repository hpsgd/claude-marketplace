# Churn analysis

Testing whether the churn-analysis skill requires timeline reconstruction, root cause diagnosis, churn probability scoring, and an intervention design — not just a list of churn reasons.

## Prompt

> /customer-success:churn-analysis for Bradwick & Sons who just submitted a cancellation request. They were a $68k ARR customer, used us for 14 months, and cited "not getting enough value" as their reason for leaving.

```markdown

## Output

# Churn Analysis: Bradwick & Sons

### Risk Summary
- **Churn probability:** High
- **Risk score:** 15/18
- **ARR at risk:** $68,000
- **Time to action:** Urgent (cancellation already submitted)

### Active Signals

| Signal | Severity | Evidence | Duration |
|---|---|---|---|
| Login frequency declining | High | Dropped from 4x/week to 1x/week (months 10–14) | 4+ weeks |
| Last active session | Critical | 18 days ago | Ongoing |
| Support tickets unresolved | High | 3 tickets in months 12–13, all >7 days open | 2 months |
| No QBR held | Medium | No QBR in 6 months | 6 months |
| Champion departure | High | Primary contact left at month 11 | 3 months |

### Timeline

| Date | Event | Significance |
|---|---|---|
| Months 1–6 | Strong adoption, 8 active users, weekly logins | Healthy trajectory |
| Month 7 | Champion departs | Relationship risk — new contact not identified |
| Month 8 | New contact unresponsive to re-onboarding outreach | Engagement decline begins |
| Month 10 | Login frequency halved | Usage decline — 4 weeks into decline |
| Month 11 | Health score drops below 60 | At Risk classification threshold crossed |
| Months 12–13 | Three support tickets, all unresolved >7 days | Trust erosion |
| Month 14 | Cancellation submitted | Churn confirmed |

### Root Cause
- **Primary:** Relationship failure — champion departure followed by failed re-onboarding of replacement contact
- **Contributing:** Unresolved support tickets eroded trust; no QBR held in 6 months meant no structured review of value
- **Addressable:** Partially — relationship can be rebuilt, but at month 14 with a submitted cancellation, recovery probability is low

### Risk Scoring

| Factor | Score (1–3) | Evidence |
|---|---|---|
| Usage trend | 3 | Declining >4 weeks |
| Engagement | 3 | Last active 18 days ago |
| Sponsor status | 3 | No champion identified since month 7 |
| Value realisation | 3 | Cancellation reason: "not getting enough value" |
| Contract timeline | 2 | Cancellation submitted — contract in dispute |
| Competitive activity | 1 | No signals of competitor evaluation |
| **Total** | **15** | High risk |

### Intervention Plan

| Action | Owner | Timeline | Success criteria |
|---|---|---|---|
| Executive call — CSM VP to customer decision-maker | VP CS | Within 48 hours | Meeting booked |
| Dedicated re-onboarding for replacement contact | Senior CSM | Within 1 week | New champion identified and engaged |
| Resolution of 3 open support tickets | Support + Engineering | Within 72 hours | All tickets closed, customer notified |
| 60-day extension offer with health milestone checkpoints | CSM + Sales | Meeting 1 | Customer agrees to trial the recovery plan |

Recovery probability: 15–20% given depth of decline and submitted cancellation. Worth attempting — intervention cost is low relative to ARR at risk.

### Retention Economics

| Metric | Value |
|---|---|
| ARR at risk | $68,000 |
| Replacement cost | $340,000–$476,000 (5–7× retention cost) |
| Lifetime value remaining (3-year est.) | ~$204,000 |
| Intervention cost | $2,000–$4,000 (senior CSM time + concessions) |
| ROI of retention attempt | 17×–34× |

### Checkpoint
- **Review date:** 2 weeks from executive call
- **Success indicators:** New champion identified, 3 support tickets resolved, customer attending a recovery planning session
- **Escalation trigger:** No response from customer decision-maker within 5 business days → accept churn, focus on exit interview and learnings
```

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/8 (94%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Skill requires signal identification — Step 1 "Signal Identification" explicitly catalogues signals across six categories (usage decline, engagement drop, relationship deterioration, value gap, commercial friction, support escalation) and requires documenting "every active signal with specific evidence (dates, metrics, quotes)." This step is required before any root cause analysis.
- [x] PASS: Skill requires timeline reconstruction — Step 2 "Timeline Reconstruction" is a dedicated step requiring a chronological table with Date, Event, and Signal columns. The step instructs looking for "inflection point," "accelerating decline," and "correlated events." This is structurally separate from signal identification and must be completed before root cause diagnosis.
- [x] PASS: Skill produces a root cause diagnosis — Step 3 "Root Cause Diagnosis" provides a structured table distinguishing product-market fit, onboarding failure, value delivery gap, relationship failure, product quality, competitive pressure, and internal change. The Rules section requires identifying the "PRIMARY root cause, not just a list of everything wrong."
- [x] PASS: Skill requires a churn probability score — Step 4 is a 6-factor scoring table (1–3 scale, total 6–18) with explicit probability thresholds: 6–9 Low, 10–13 Medium, 14–18 High. This is a quantified classification, not qualitative assessment. The factor list (usage trend, engagement, sponsor status, value realisation, contract timeline, competitive activity) is explicit.
- [x] PASS: Skill includes an intervention design — Step 5 "Intervention Design" maps root causes to intervention approaches with timelines. It requires each intervention to have an Owner, First action within 48 hours, Success criteria, Checkpoint, and Escalation path. These are explicit required fields in the output template.
- [x] PASS: Skill requires retention economics — Step 6 "Retention Economics" requires ARR at risk, replacement cost (explicitly stated as "typically 5–7× retention cost"), lifetime value remaining, intervention cost, and ROI. The output template table is explicit.
- [~] PARTIAL: Skill feeds findings into pattern or trend — the Output Format template includes a Checkpoint section with "Review date," "Success indicators," and "Escalation trigger," but checking whether this churn is part of a broader trend is mentioned only implicitly in Step 3's competitive pressure category. There is no explicit Step 7 or required section asking whether this is an isolated incident or a trend. PARTIAL ceiling: 0.5 points.
- [x] PASS: Valid YAML frontmatter — the skill has `name: churn-analysis`, `description`, and `argument-hint` fields in valid YAML frontmatter.

### Notes

The 6-factor scoring table in Step 4 is the standout design element — it converts churn probability from a gut feeling into an auditable number, making it consistent across CSMs. The retention economics step is more rigorous than typical CS frameworks: it explicitly names the 5–7× replacement cost multiple, which frames urgency in business terms rather than "we should try to save them." The trend check earns PARTIAL because it appears in the output template as a prompt but not as a required analytical step. An explicit "Is this part of a broader pattern?" question in Step 5 or Step 6 would close this gap.
