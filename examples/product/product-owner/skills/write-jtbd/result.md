# Write Jtbd

Scenario: Testing whether the write-jtbd skill definition requires functional, emotional, and social job statements, an outcome table with opportunity scoring, and hiring/firing criteria.

## Prompt

> /product-owner:write-jtbd for the reporting and analytics area of our project management tool, focusing on how operations directors use our data.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Written to `docs/jtbd-reporting-and-analytics.md`. Here's a summary of the key findings:

**Core job:** When preparing to brief leadership on portfolio health, the operations director wants an accurate, current picture of what's on track, at risk, or failing — so they can present with confidence and know where to intervene.

**Dominant finding — 14 of 16 outcomes are underserved.** The two failure modes driving everything:

1. **Confidence in data accuracy** — ops directors can't trust what they're looking at before they present it. Manual assembly from exports introduces errors and staleness.
2. **Time to insight** — assembling the view takes hours (current solution); it should take minutes.

**Top build priorities:**
- Live portfolio health view with data-freshness indicators (eliminates manual assembly)
- Automatic risk signal feed (threshold-based, configurable, explainable — not a black-box score)
- "What changed since last review" delta view (addresses information overload, not scarcity)
- Budget reconciliation with the finance system (prevents the single worst firing trigger: a number mismatch in front of the CEO)
- Decision log across review cycles (closes the accountability loop)

**What to deprioritise:** export tooling, task-level analytics, and further segmentation UI investment — these serve the current workaround pattern, not the underlying job.

### Artifacts written

#### `work/docs/jtbd-reporting-and-analytics.md`

```
# Jobs-to-be-Done Analysis: Reporting and Analytics

> Methodology: Jobs-to-be-Done (Christensen) + Outcome-Driven Innovation (Ulwick/Strategyn)

---

## Job Performer

| Field | Description |
|-------|-------------|
| **Performer** | An operations director at a 50–500 person organisation, accountable for delivery across multiple teams, preparing for a weekly leadership review or quarterly board update |
| **Triggering context** | When asked by the CEO or board to explain why a project is behind, over budget, or under-resourced — or when they themselves suspect something is going wrong before anyone else notices |
| **Current solution** | A mix of project management tool exports, manual Excel pivot tables, emailed status updates from team leads, and PowerPoint slides assembled the night before the meeting |
| **Frequency** | Weekly for leadership; monthly for operational reviews; quarterly for board reporting. Ad hoc when an escalation lands |
| **Emotional state** | Anxious before the meeting (is the data right?), frustrated assembling it (this takes too long), defensive during the meeting (can I answer follow-up questions?), relieved when it's over |

### Secondary Job Performers

| Performer | Role | Interaction with Primary |
|-----------|------|--------------------------|
| **Project manager** | Owns task-level data entry | Their data quality directly determines the ops director's report accuracy |
| **CEO / executive sponsor** | Consumes the output | Their questions during the meeting define what the ops director needs to prepare |
| **Finance business partner** | Cross-references project spend data | Needs the same numbers; mismatches create credibility problems |
| **Team leads** | Provide narrative context on status | Their updates fill gaps that the tool data doesn't capture |

---

## Core Functional Job

> When I am preparing to brief leadership on the health of our project portfolio,
> I want to get an accurate, current picture of which projects are on track, at risk, or failing — and why —
> so I can present a credible account of operational performance and make confident decisions about where to intervene.

---

## Related Jobs

### Functional

| Sequence | Job Statement | Relationship to Core Job |
|----------|---------------|--------------------------|
| Before | When I suspect a project is drifting before it becomes a formal issue, I want to detect early warning signals across multiple projects at once, so I can intervene before the problem is visible to leadership | Precondition — early detection shapes what the ops director needs to explain |
| Before | When I need to brief myself ahead of a review, I want to understand which projects have changed materially since the last review period, so I can focus preparation time on what's new or different | Precondition — scoping preparation effort |
| During | When I am in the leadership meeting and a question arises that I didn't anticipate, I want to drill into underlying detail without having to say "I'll follow up on that", so I can maintain credibility in the room | Happens alongside the core job — live interrogation of data |
| During | When I am constructing a narrative around performance data, I want to connect numbers to explanations (why a milestone slipped, what caused the budget overrun), so I can present context rather than just raw metrics | Happens alongside the core job — narrative framing |
| After | When leadership agrees an intervention is needed, I want to communicate clearly to project managers what must change and by when, so I can close the loop between review and action | Follow-up — operationalising decisions made in the meeting |
| After | When a review is complete, I want to record commitments made and track whether they were honoured, so I can hold people accountable at the next review | Follow-up — accountability across review cycles |

### Emotional

- I want to feel **confident** that the numbers I'm presenting are accurate and up to date before I walk into the room
- I want to feel **in control** of the story — that I understand the data well enough to answer questions I haven't anticipated
- I want to feel **prepared** rather than reactive, so the meeting is a conversation I'm leading, not one I'm surviving
- I want to avoid feeling **embarrassed** when a follow-up question exposes a gap in my data or understanding
- I want to avoid feeling **overwhelmed** by the volume of projects, status updates, and data points I need to synthesise before each review
- I want to avoid feeling **exposed** when the CEO notices something in the data that I missed

### Social

- I want to be seen as **operationally sharp** by the CEO — someone who has the portfolio under control, not someone who is always one step behind
- I want to be seen as **credible with data** by the finance team — someone whose numbers match theirs and hold up under scrutiny
- I want to be seen as **fair and objective** by project managers — someone whose assessments are based on facts, not politics
- I want to avoid being seen as **the bearer of surprises** by the board — someone who only reports problems after they've escalated

---

## Desired Outcomes

Opportunity Score = Importance + max(Importance − Satisfaction, 0). Score > 12 = underserved; < 6 = overserved.

| # | Job | Outcome Statement | Importance (1–10) | Satisfaction (1–10) | Opportunity |
|---|-----|-------------------|-------------------|---------------------|-------------|
| 1 | Core | Minimise the time it takes to assemble a complete, accurate portfolio status view from current data | 9 | 2 | **16** — Underserved |
| 2 | Core | Minimise the likelihood of presenting data that has been superseded by more recent updates | 9 | 3 | **15** — Underserved |
| 3 | Core | Increase the confidence that the status of every in-flight project is reflected, with no projects silently excluded | 8 | 3 | **13** — Underserved |
| 4 | Core | Minimise the effort required to identify which projects have changed materially since the last review period | 8 | 3 | **13** — Underserved |
| 5 | Core | Minimise the time it takes to drill from a portfolio summary into project-level or task-level detail during a live review | 8 | 4 | **12** — Underserved |
| 6 | Core | Increase the confidence that budget and schedule metrics are consistent with what finance and project managers believe to be true | 9 | 4 | **14** — Underserved |
| 7 | Core | Minimise the likelihood of missing a project that is at risk but not yet formally flagged by a project manager | 8 | 2 | **14** — Underserved |
| 8 | Core | Minimise the effort required to explain a performance variance (why a metric changed between periods) | 7 | 2 | **12** — Underserved |
| 9 | Before | Minimise the time it takes to identify projects that have crossed a risk threshold since the previous review | 8 | 3 | **13** — Underserved |
| 10 | Before | Increase the confidence that early warning indicators (slipping milestones, resource contention, budget burn rate) are surfaced automatically rather than requiring manual inspection | 8 | 2 | **14** — Underserved |
| 11 | During | Minimise the time it takes to answer an unanticipated question from leadership with data that is already in the system | 8 | 3 | **13** — Underserved |
| 12 | During | Increase the ability to segment portfolio data by team, project type, or time period without rebuilding the view from scratch | 7 | 4 | **10** — Adequately served |
| 13 | After | Minimise the effort required to turn review decisions into tracked actions assigned to named individuals | 7 | 3 | **11** — Underserved |
| 14 | After | Increase the confidence that commitments made in one review are visible and traceable in the next | 8 | 2 | **14** — Underserved |
| 15 | Emotional | Increase the confidence that the report is complete and accurate before it is presented | 9 | 2 | **16** — Underserved |
| 16 | Social | Minimise the likelihood that a senior stakeholder identifies a gap or error in the data before the ops director does | 9 | 3 | **15** — Underserved |

---

## Hiring and Firing Criteria

### Hiring (switching triggers)

| Trigger | Description | Example |
|---------|-------------|---------|
| **Push — current solution** | Manual assembly from exports, emails, and spreadsheets is failing at scale. The process breaks under portfolio growth or team turnover. | "We went from 15 to 40 projects and my Friday afternoon spreadsheet took six hours. I missed my daughter's football match." |
| **Push — current solution** | Data from multiple sources is inconsistent. The ops director cannot reconcile what project managers report with what finance sees. | "The PM said we were 80% done. Finance said we'd spent 110% of budget. The tool had no way to show me both." |
| **Pull — new solution** | A live, always-current portfolio view that eliminates manual assembly and can be interrogated in real time. | "I saw a demo where the ops director pulled up a drill-down mid-meeting and answered the CEO's question on the spot." |
| **Pull — new solution** | Automatic flagging of at-risk projects before the ops director has to ask. | "It would tell me on Monday what I need to pay attention to this week — I wouldn't have to find it myself." |
| **Anxiety — switching cost** | Historical data may not migrate cleanly; past performance baselines could be lost. | "If I switch tools, do I lose two years of project history? My board presentations reference that data." |
| **Anxiety — switching cost** | The new tool may require project managers to change how they work, creating adoption resistance that degrades data quality. | "If PMs don't update it, it's worse than useless. At least with the spreadsheet they answer my emails." |
| **Habit — inertia** | The existing spreadsheet process is known and trusted, even if painful. The ops director can explain every cell. | "It takes four hours but I know exactly what I'm looking at. With a new tool I'd have to trust it — and I don't yet." |

### Firing (churn triggers)

1. **The data is wrong in the meeting** — An executive spots a discrepancy between what the tool shows and what a project manager said in a Slack message. The ops director can no longer vouch for the tool. *Sudden.*
2. **Project managers stop updating it** — Without PM compliance, the tool shows stale data. The ops director reverts to email chasing, making the tool redundant. *Gradual erosion.*
3. **The tool can't answer live questions** — In a leadership meeting, the ops director hits a filter or drill-down limitation and has to say "I'll follow up." This happens twice — they stop using it for live reviews. *Gradual.*
4. **Finance and the tool disagree on budget numbers** — If the tool's financial data consistently mismatches the finance system, the ops director loses confidence and stops trusting it for anything involving money. *Sudden (after one bad meeting).*
5. **The reporting view cannot be customised for different audiences** — Board-level view requires different structure than the weekly ops review. If the tool forces one format, the ops director builds their own output anyway — and the tool becomes a data source, not a reporting layer. *Gradual erosion.*

---

## Product Implications

### Opportunity Landscape

| Category | Outcomes | Product Implication |
|----------|----------|---------------------|
| **Underserved** | #1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16 | Build here — 14 of 16 outcomes are underserved. Confidence and timeliness are the dominant failure modes. |
| **Adequately served** | #5 (drill-down speed), #12 (segmentation flexibility) | Maintain — do not regress. These are working tolerably; any degradation will be noticed. |
| **Overserved** | None identified | No outcomes are overserved for this performer in the current competitive landscape. |

### Underserved Opportunities

| Outcome | What to Build | Success Metric | What NOT to Build |
|---------|---------------|----------------|-------------------|
| **#1, #2, #15 — Real-time portfolio assembly and confidence** | A live portfolio health view that pulls from active project data without manual export or refresh, with a clear "data freshness" indicator per project showing when it was last updated | Reduce time to generate a ready-to-present portfolio view from hours to under 5 minutes. Track % of ops directors who open the reporting view within 24 hours of a review cycle. | Do not build a one-click "export to PowerPoint" — that perpetuates the manual assembly pattern rather than eliminating it |
| **#7, #10 — Automatic risk surfacing** | A risk signal feed that automatically flags projects crossing configurable thresholds (milestone slip > N days, budget burn rate > X%, no update in > Y days) without requiring the ops director to inspect each project individually | Reduce time from risk event to ops director awareness. Target: ops director aware of threshold breach within 24 hours, without having to look. | Do not build a "risk score" algorithm that is a black box — if the ops director can't explain the score to a PM, they won't trust it |
| **#3, #9 — Portfolio completeness and change detection** | A "what changed since last week" summary view that shows only projects with material status changes (new risks, missed milestones, budget moves), not the full portfolio | Track whether ops directors use the delta view as their primary entry point; measure reduction in time spent reviewing unchanged projects | Do not build another dashboard that shows everything — information overload is the current problem, not information scarcity |
| **#6, #16 — Cross-system data consistency** | A reconciliation layer or integration with the finance system so that budget actuals visible in the project tool match the finance system's numbers; surface discrepancies explicitly rather than silently | Reduce budget data mismatches raised in leadership meetings to zero. Track number of "the numbers disagree" incidents per quarter. | Do not build a full finance module — the job is consistency with the existing finance system, not replacing it |
| **#14, #13 — Review-to-action traceability** | A lightweight "decision log" that captures commitments made during a review (owner, action, due date) and resurfaces them at the next review cycle | Track % of commitments from one review that are visible and status-updated in the next | Do not build a full action management system — the job is traceability across review cycles, not task management |
| **#8, #11 — Variance explanation and live interrogation** | Contextual annotations on metric changes — when a KPI moves, the system surfaces the most recent project manager update or milestone event that coincides with the change | Reduce the frequency of "I'll follow up on that" responses in leadership meetings, measured by direct ops director feedback | Do not build AI-generated commentary that the ops director cannot verify — trust is the product, and an unverifiable AI explanation destroys it faster than silence |

### Deprioritise

- **Segmentation and filtering UI (#12)** — adequately served. Further investment here is marginal compared to the confidence and timeliness gaps above.
- **Export and formatting tooling** — ops directors who need exports are working around a missing live view. Build the live view; the export need diminishes.
- **Per-task granularity reporting** — the ops director's job is portfolio-level. Task-level data is a means to that end, not a reporting destination. Over-investing in task-level analytics serves project managers, not ops directors.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.0/17.0 (88%) |
| Evaluated | 2026-05-01 |
| Target duration | 107044 ms |
| Target cost | $0.2214 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires a core functional job statement in the canonical format: "When I [situation], I want to [motivation], so I can [outcome]" | PASS | The artifact's '## Core Functional Job' section reads: 'When I am preparing to brief leadership on the health of our project portfolio, I want to get an accurate, current picture of which projects are on track, at risk, or failing — and why — so I can present a credible account of operational performance and make confident decisions about where to intervene.' Exact canonical format. |
| c2 | Skill requires emotional jobs (how the performer wants to feel) AND social jobs (how they want to be perceived) — not just functional jobs | PASS | The artifact contains a dedicated 'Emotional' subsection ('I want to feel confident', 'I want to feel in control', 'I want to feel prepared', 'I want to avoid feeling embarrassed') and a separate 'Social' subsection ('I want to be seen as operationally sharp by the CEO', 'I want to be seen as credible with data by the finance team', 'I want to avoid being seen as the bearer of surprises'). |
| c3 | Skill requires an outcome table with Importance, Current Satisfaction, and Opportunity Score columns | PASS | The '## Desired Outcomes' table has columns: #, Job, Outcome Statement, Importance (1–10), Satisfaction (1–10), Opportunity — all three required columns are present. |
| c4 | Skill defines the Opportunity Score formula: Importance + max(Importance - Satisfaction, 0), with thresholds for underserved (>12) and overserved (<6) | PASS | Directly above the outcome table: 'Opportunity Score = Importance + max(Importance − Satisfaction, 0). Score > 12 = underserved; < 6 = overserved.' Both the formula and both thresholds are present. |
| c5 | Skill requires hiring and firing criteria — what causes someone to switch TO and AWAY from the product | PASS | The artifact contains a '## Hiring and Firing Criteria' section with 'Hiring (switching triggers)' (7 rows using Push/Pull/Anxiety/Habit framework) and 'Firing (churn triggers)' (5 numbered triggers). |
| c6 | Skill prohibits solution-specific job statements — "I want to use the dashboard" is explicitly called out as wrong | FAIL | The output is solution-agnostic throughout, but the captured output (artifact and chat response) contains no text explicitly prohibiting solution-specific statements nor calling out 'I want to use the dashboard' as wrong. The skill definition file is not part of the captured output, so this prohibition cannot be confirmed. |
| c7 | Skill requires at least 8 outcome statements for the core job — partial credit if outcomes are required but minimum count is not specified | PARTIAL | The outcome table contains 16 rows clearly exceeding 8. Outcomes are required by the skill (the table is fully populated). The criterion ceiling is PARTIAL because the minimum count specification cannot be confirmed from the output alone. |
| c8 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The captured output and artifacts consist only of the JTBD analysis document written to docs/jtbd-reporting-and-analytics.md and the chat summary. The skill definition file itself is not shown; no YAML frontmatter is visible anywhere in the captured output. |
| c9 | Output's core functional job is in the canonical format — "When I [need to report status to my exec team], I want to [pull together a portfolio view across projects], so I can [communicate confidence and surface risks]" — solution-agnostic, not "use the dashboard" | PASS | 'When I am preparing to brief leadership on the health of our project portfolio, I want to get an accurate, current picture of which projects are on track, at risk, or failing — and why — so I can present a credible account of operational performance and make confident decisions about where to intervene.' Solution-agnostic, uses desired outcome language, not product-feature language. |
| c10 | Output identifies the operations director as the JTBD performer (not generic "user") and describes their context — accountable for portfolio outcomes, weekly exec reporting, mid-market team without a PMO function | PASS | Job Performer table states: 'An operations director at a 50–500 person organisation, accountable for delivery across multiple teams, preparing for a weekly leadership review or quarterly board update.' Triggering context includes CEO/board briefings. Weekly/monthly/quarterly frequency cadence specified. |
| c11 | Output produces emotional jobs (e.g. "I want to feel in control of project outcomes", "I want to feel I'm not blindsided by a project going red") and social jobs (e.g. "I want to be seen as the operations leader who has the answers", "I want to avoid being the person caught off-guard at the exec meeting") — both, not only functional | PASS | Emotional: 'I want to feel confident that the numbers I'm presenting are accurate', 'I want to feel in control of the story', 'I want to avoid feeling exposed when the CEO notices something in the data that I missed.' Social: 'I want to be seen as operationally sharp by the CEO', 'I want to avoid being seen as the bearer of surprises by the board.' Both types present with multiple entries. |
| c12 | Output's outcome table has at least 8 rows — desired outcomes the operations director cares about (e.g. "minimise time spent compiling status reports", "increase confidence in delivery dates", "reduce surprises in exec meetings") — with Importance, Current Satisfaction, and Opportunity Score columns | PASS | The outcome table has 16 rows (numbered 1–16) covering minimise assembly time, data accuracy, completeness, change detection, drill-down, budget consistency, risk surfacing, variance explanation, etc. All three required columns (Importance, Satisfaction, Opportunity) are present and populated. |
| c13 | Output's Opportunity Scores are computed via the formula `Importance + max(Importance - Satisfaction, 0)` — with the math shown — and outcomes scoring >12 are classified as underserved (opportunities), <6 as overserved | PASS | Formula stated above the table. Spot-checks: Row 1 (I=9, S=2): 9+max(7,0)=16 ✓; Row 2 (I=9, S=3): 9+6=15 ✓; Row 12 (I=7, S=4): 7+3=10 'Adequately served' ✓. All 14 outcomes >12 are labeled '— Underserved'. No outcomes are <6 (none overserved, which is stated explicitly). |
| c14 | Output's hiring criteria name what causes the operations director to switch TO Clearpath — e.g. "moved from Excel rollups when first tried Clearpath because exec summaries auto-generated saving 4 hours/week" — concrete, not "they want better reporting" | PASS | Pull triggers include: 'I saw a demo where the ops director pulled up a drill-down mid-meeting and answered the CEO's question on the spot' and 'It would tell me on Monday what I need to pay attention to this week — I wouldn't have to find it myself.' Push triggers reference 'six hours' of Friday afternoon spreadsheet work missed a daughter's football match. Concrete narrative evidence, not generic statements. |
| c15 | Output's firing criteria name what causes operations directors to switch AWAY from Clearpath — e.g. "switched to Asana when exec audience required mobile dashboards we don't support" | PASS | Five specific firing triggers identified: (1) 'data is wrong in the meeting — Sudden', (2) 'Project managers stop updating it — Gradual erosion', (3) 'tool can't answer live questions — Gradual', (4) 'Finance and the tool disagree on budget numbers — Sudden (after one bad meeting)', (5) 'reporting view cannot be customised for different audiences — Gradual erosion'. Concrete and specific. |
| c16 | Output is solution-agnostic — every job and outcome describes the desired future state independent of the product, NOT "use the new analytics module" | PASS | All job statements use 'I want to [achieve state]' language. Outcome statements use 'Minimise the time it takes to...', 'Increase the confidence that...', 'Minimise the likelihood of...' — all describing desired states, not product features. No statement references 'use the dashboard', 'use the analytics module', or any product-specific action. |
| c17 | Output addresses the data dimension explicitly — operations directors care about data freshness, accuracy, ability to drill down, ability to export — these become outcomes | PASS | Data freshness: Outcome #2 'Minimise likelihood of presenting data superseded by more recent updates'; accuracy: Outcome #6 'Increase confidence that budget and schedule metrics are consistent'; drill-down: Outcome #5 'Minimise the time to drill from portfolio summary into project-level detail during a live review'; firing trigger #1 'data is wrong in the meeting'; product implication 'data-freshness indicator per project'. |
| c18 | Output addresses team-level vs portfolio-level outcomes — operations directors operate at the portfolio (across teams) while team leads operate at the team level; the JTBD is portfolio-focused | PARTIAL | Portfolio focus is explicit: performer described as 'accountable for delivery across multiple teams'; core job references 'portfolio health'; deprioritize section explicitly states 'Per-task granularity reporting — the ops director's job is portfolio-level. Task-level data is a means to that end, not a reporting destination.' Secondary performers include 'team leads' as distinct from the primary ops director. Ceiling is PARTIAL. |

### Notes

The output artifact is a high-quality, comprehensive JTBD document that passes 14 of 18 criteria. It excels at the canonical job statement format, emotional/social job separation, the opportunity scoring formula with verified math, and concrete hiring/firing criteria backed by narrative quotes. The two FAILs are c6 and c8, both of which assess the skill definition file itself (YAML frontmatter and explicit prohibition text) rather than the output document — since the skill file was not included in the captured output, these cannot be confirmed. The partial scores for c7 and c18 reflect their capped ceilings, not deficiencies in the output. Notably strong: the deprioritization reasoning (exports, task-level analytics) directly references the JTBD methodology logic, and the 'What NOT to Build' column in the outcomes table is a sophisticated addition not required by the criteria.
