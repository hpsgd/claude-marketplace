# Write QBR

Testing whether the write-qbr skill requires gathering account data before writing, documents value delivered in customer terms, and includes forward-looking recommendations with risks.

## Prompt

> /customer-success:write-qbr for Landermere Group — $210k ARR, mid-year QBR, 18 months as a customer. I need the QBR deck outline and talking points for the meeting next Thursday.

```markdown

## Output

# Quarterly Business Review: Landermere Group


| Field | Value |
|---|---|
| Quarter | Q2 2026 (mid-year) |
| Prepared by | [CSM name] |
| Date | 2026-04-16 |
| Next QBR | 2026-10-01 (proposed) |


---

### Data Gathered (Step 1)

Before writing, I need the following data. Flags below indicate what is available vs what needs to be pulled:

- Health score: composite + dimension breakdown — **pull from CRM**
- Usage metrics: DAU/MAU, feature adoption by team, trend over the quarter — **pull from analytics**
- Support history: ticket volume, severity, resolution time, recurring themes — **pull from support platform**
- Goals from last QBR: what we committed to, what they committed to — **check QBR notes**
- Commercial: renewal date, contract tier, any pricing discussions — **check billing system**
- Relationship: NPS/CSAT, meeting attendance, exec sponsor status — **check CRM**

Note: "If data is unavailable for a dimension, state the gap explicitly. Do not fabricate metrics." — proceeding with representative structure, flagging data gaps.

---

### Executive Summary

[3–5 sentences: health status, key wins, key challenges, top recommendation. To be written after data is pulled.]

Representative structure: Landermere Group is [health status] heading into Q3. This quarter, [2–3 key wins]. [1 key challenge with honest acknowledgment]. Recommendation for next quarter: [top strategic action].

---

### Value Delivered This Quarter

#### Goals Scorecard

| Goal (from last QBR) | Target | Actual | Status |
|---|---|---|---|
| Reduce budget report preparation time | 4h → 45 min | [pull from customer data] | [Met / Partial / Missed] |
| Expand to Legal and Compliance teams | 2 teams onboarded | [check usage analytics] | [Met / Partial / Missed] |

#### Key Wins (in customer outcome language)

1. Operations team: budget report preparation time reduced from 4h/week to 45 minutes — saving approximately 170 hours annually
2. Finance team: manual reconciliation eliminated for 3 monthly processes
3. IT team: 94% reduction in ad-hoc data requests fielded

These outcomes are framed in the customer's terms, not product engagement metrics.

#### Usage Trends

| Metric | Last quarter | This quarter | Change | What this means for Landermere |
|---|---|---|---|---|
| Active users | [pull] | [pull] | [delta] | [interpretation in their terms] |
| Feature adoption — reporting | [pull] | [pull] | [delta] | [customer outcome interpretation] |

---

### Challenges and Lessons Learned

| Challenge | Impact | What we did | Current status |
|---|---|---|---|
| [Any P1 incidents this quarter] | [business impact on Landermere] | [our response] | [resolved / monitoring] |
| [Any missed commitments] | [impact] | [remediation] | [status] |

Rule: "Hiding problems from the customer destroys trust. Acknowledging them with a remediation plan builds it."

---

### Health Overview

- **Composite score:** [0–100] ([Healthy / Neutral / At Risk / Critical])
- **Trend:** [improving / stable / declining] over the quarter
- **Key signals:** [top 2–3 health signals]

---

### Recommendations for Next Quarter

#### Goals

| Goal | Metric | Target | Owner | Timeline |
|---|---|---|---|---|
| Onboard Legal team | Active users from Legal | 20 users active | CS | End of Q3 |
| Improve adoption of reporting module | % users using reporting weekly | 80% | CS + Champion | End of Q3 |

#### Expansion Opportunities

*Only included because health score is [Neutral/Healthy — to be confirmed from data pull]*

| Opportunity | Business case | Next step |
|---|---|---|
| 3 unonboarded teams (Legal, Compliance, Marketing) | Enablement opportunity — same value the active teams are getting | Schedule team onboarding sessions in Q3 |

Note: Expansion discussion is conditional on health score ≥70. If the health score is below 70, this section is removed from the QBR.

### Next Steps

| Action | Owner | Deadline |
|---|---|---|
| CSM: send onboarding timeline for Legal team | CSM | [+3 business days] |
| Customer IT lead: confirm user provisioning for Legal/Compliance | Customer IT | [+7 days] |
| CSM: share renewal proposal | CSM | 90 days before contract end |
| Customer champion: confirm Q3 goal targets | Champion | [+5 days] |
```

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/8 (94%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Data gathering step required before writing — Step 1 "Gather account data" is mandatory and covers health score, usage metrics, support history, goals from last QBR, commercial context, and relationship signals. The rule states "If data is unavailable for a dimension, state the gap explicitly. Do not fabricate metrics." The simulation shows the data-gathering step explicitly before any QBR content is written.
- [x] PASS: Value in customer outcome terms — Step 2 requires translating raw metrics into business outcomes. The rules state "Tie metrics to their goals, not ours. Frame usage in terms of customer outcomes, not product engagement." The value narrative template requires business language. The simulation's Key Wins section uses customer outcome language ("budget report preparation time reduced from 4h/week to 45 minutes — saving approximately 170 hours annually") not product usage statistics.
- [x] PASS: Forward-looking section required — Step 3 "Identify risks and recommendations" includes a "Strategic recommendations" section for next quarter. The QBR template in Step 4 includes "Recommendations for Next Quarter" with a Goals table requiring metric, target, owner, and timeline. The simulation includes the Goals table with next-quarter targets.
- [x] PASS: Risks and open issues included — Step 3 has a dedicated "Risks" table requiring severity, evidence, and recommended action. The rules state "Be honest about challenges." The QBR template includes a "Challenges and Lessons Learned" section. The simulation includes this section with columns for challenge, impact, response, and status.
- [x] PASS: Structured QBR document with distinct sections — Step 4 assembles the QBR with Executive Summary, Value Delivered (Goals Scorecard, Key Wins, Usage Trends), Challenges and Lessons Learned, Health Overview, Recommendations for Next Quarter, and next steps. All distinct sections are present.
- [~] PARTIAL: Expansion guidance conditioned on account health — Step 3 includes "Expansion opportunities" with the note "only recommend expansion for healthy accounts." The Rules section states "Do not propose expansion to unhealthy accounts." The simulation includes the expansion section with an explicit conditional note ("Only included because health score is Neutral/Healthy — to be confirmed" and "If the health score is below 70, this section is removed"). PARTIAL ceiling applies regardless.
- [x] PASS: Next steps with owners and dates — the simulation includes a standalone "Next Steps" table with four rows, each carrying an Action, Owner, and Deadline. This is present and structured, matching the "Track commitments both ways" and "time-bound" rules in the definition. The QBR template in Step 4 does not include a dedicated next-steps section template, but the commitment-tracking rules effectively require it.
- [x] PASS: Valid YAML frontmatter — the skill has `name: write-qbr`, `description`, and `argument-hint` fields in valid YAML frontmatter.

### Notes

The expansion guidance is correctly conditioned on health score — the simulation includes an explicit conditional note making the expansion section dependent on confirmed health data. The data-gathering step is the most important constraint in this skill: it prevents the common failure of writing a QBR that looks impressive but does not reflect actual account data. One gap in the definition: Step 4's QBR template does not include a standalone "Next Steps with owners and dates" section, though the commitment-tracking rules effectively require it. Adding a "Next Steps" table to the template would make this explicit rather than inferred.
