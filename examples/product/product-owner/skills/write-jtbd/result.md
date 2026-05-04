# Write Jtbd

Scenario: Testing whether the write-jtbd skill definition requires functional, emotional, and social job statements, an outcome table with opportunity scoring, and hiring/firing criteria.

## Prompt

> /product-owner:write-jtbd for the reporting and analytics area of our project management tool, focusing on how operations directors use our data.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I've created a comprehensive Jobs-to-be-Done analysis focused on operations directors preparing for leadership check-ins. The analysis identifies:

**Core job:** Quickly verify portfolio health (budget, timeline, resources, risks) across 20+ projects and surface what's changed, so they can present with confidence and answer questions without delays.

**Key underserved outcomes (opportunities to build):**
- **Reporting time** — currently 4+ hours, could drop to <30 min with auto-generated portfolio snapshot
- **Data freshness** — currently stale/manual, needs real-time or <30 min lag
- **Change detection** — currently manual scan of all projects, could auto-flag critical changes daily
- **Fast project lookup** — currently requires leaving the meeting, needs <5 min drill-down with history

**Key insights from hiring/firing criteria:**
- They'll switch TO a solution that drops prep time and removes manual consolidation
- They'll switch AWAY if data becomes stale, the tool breaks during a reporting window, or a spreadsheet workaround becomes faster
- The emotional/social jobs are load-bearing: they need to feel confident and be seen as prepared

The analysis is saved to `docs/jtbd-reporting-analytics.md` and includes product recommendations (what to build, what not to build) and success metrics.

**What to do next:**
- Validate the job performer context — is the bi-weekly pre-meeting scenario accurate for your users, or does the pattern differ?
- Adjust frequency/pain points if your operations directors face a different workflow
- Prioritise which underserved outcomes to tackle first (the portfolio snapshot and change alerts would move the needle fastest)

Do you want me to adjust any of the assumptions, or dive deeper into a specific outcome area?

### Artifacts written

#### `work/docs/jtbd-reporting-analytics.md`

```
# Jobs-to-be-Done Analysis: Reporting and Analytics

## Job Performer

| Field | Description |
|-------|-------------|
| **Performer** | An operations director during their bi-weekly leadership check-in, when they need to report on portfolio health to the executive team |
| **Triggering context** | 2 hours before a leadership meeting where they must present current project status, budget burn, resource utilisation, and risk exposure across 20+ concurrent projects |
| **Current solution** | Spreadsheets exported from the PM tool, manually consolidated with notes, combined with Slack conversations and email threads to piece together the narrative |
| **Frequency** | Twice weekly (formal check-ins), plus ad-hoc requests from finance/exec every 2-3 days |
| **Emotional state** | Anxious that they'll miss something critical; under time pressure; frustrated by manual work |

---

## Core Functional Job

> When I have a leadership meeting in 2 hours and need to report on 20+ concurrent projects, I want to quickly verify the current state (budget, timeline, resource allocation, risks) and surface what's changed since the last check-in, so I can present with confidence and answer unexpected questions about specific projects without digging through email chains.

---

## Related Jobs

### Functional

| Sequence | Job Statement | Relationship |
|----------|---------------|--------------|
| Before | When I start my day, I want to know which projects have critical status changes or blockers since yesterday, so I can prioritise my day and catch issues early | Early warning; prevents escalation |
| Before | When finance asks "what's our budget position for Q2?", I want to pull the number directly from the source without manual calculation, so I can answer confidently and quickly | Precondition: accurate, current data |
| During | When I'm in the meeting and exec asks "what happened with Project X's timeline?", I want to see the history of why it slipped (is it resource, scope, or risk-related?), so I can explain root cause without guessing | Accountability; ability to defend decisions |
| After | When the meeting ends with new direction or priorities, I want to update status/timeline assumptions in the system so the whole team sees the new reality, so decisions cascade downward | Follow-up action; alignment |
| After | When I need to brief a project manager on a risky project, I want to show them the data I just presented to exec so we're all looking at the same picture, so we can have a focused conversation about mitigation | Alignment with team |

### Emotional

- I want to **feel confident** that the data I'm presenting is current and hasn't changed since I pulled it
- I want to **feel in control** — like I know what's happening across the portfolio, not surprised by exec questions
- I want to **avoid feeling embarrassed** by not being able to answer a direct question about a specific project
- I want to **avoid feeling like a data janitor** — manually copying and pasting when I should be thinking strategically
- I want to **feel like an operations leader**, not an analyst. I want to spend my time on decisions, not data wrangling

### Social

- I want to **be seen as organised and prepared** by my executive team — someone who has their finger on the pulse
- I want to **be seen as trustworthy** — when I say "project X is on track," they believe it without needing to verify it elsewhere
- I want to **be seen as responsive** — able to answer questions quickly without saying "let me check and get back to you"

---

## Desired Outcomes

| # | Job | Outcome Statement | Importance | Satisfaction | Opportunity |
|---|-----|-------------------|-----------|--------------|-------------|
| 1 | Core | Minimise the time it takes to gather all project data and compile it into a report format | 9 | 2 | **Underserved (17)** |
| 2 | Core | Minimise the likelihood that the data in my report is stale (>4 hours old) when I present | 9 | 3 | **Underserved (15)** |
| 3 | Core | Minimise the effort required to identify which projects have changed status since the last check-in | 8 | 2 | **Underserved (14)** |
| 4 | Core | Increase the confidence that budget numbers are accurate before I present them | 9 | 4 | **Underserved (14)** |
| 5 | Core | Minimise the number of ad-hoc data requests I receive from finance or exec during the week | 7 | 1 | **Underserved (13)** |
| 6 | Core | Increase the ability to answer a specific question about project X (timeline, budget, blocker) in <5 minutes without leaving the reporting tool | 8 | 2 | **Underserved (14)** |
| 7 | Core | Minimise the effort to show root cause of a timeline slip (resource, scope, risk, dependency) | 7 | 1 | **Underserved (13)** |
| 8 | Core | Increase the consistency of terminology and definitions across all project reports (so exec isn't confused by different definitions of "at risk") | 6 | 2 | **Underserved (10)** |
| 9 | Related (before) | Minimise the time to identify critical issues (budget overrun, timeline slip, key person gone) that need escalation | 8 | 2 | **Underserved (14)** |
| 10 | Related (after) | Minimise the effort to cascade updated priorities/timelines back to project managers so they see the exec decision | 6 | 3 | Adequately served |
| 11 | Emotional | Increase confidence that I'm not missing a critical project status change between formal check-ins | 7 | 2 | **Underserved (12)** |
| 12 | Emotional | Minimise the feeling of being caught off-guard by an exec question I should have anticipated | 7 | 2 | **Underserved (12)** |
| 13 | Social | Increase the likelihood that exec sees me as "someone who has the full picture" vs "someone who doesn't know what's happening" | 8 | 3 | **Underserved (13)** |

---

## Hiring / Firing Criteria

### Hiring (What causes them to switch TO a reporting/analytics solution)

| Push (current frustration) | Pull (new solution appeal) | Anxiety (switching fear) | Habit (sticking with current) |
|------|------|---------|-------|
| Reporting takes 4+ hours per check-in; manual consolidation is error-prone | "I saw a demo where the report auto-generated in 2 minutes" | "Will I lose my historical data? Can we recreate Q1 reports?" | "My team already knows how to use spreadsheets; retraining is time I don't have" |
| Exec asks a specific question and I can't answer without leaving the meeting | "I could search for any project and see its full history in one place" | "What if the new tool doesn't have all the fields we track in the spreadsheet?" | "The spreadsheet is 'good enough' even though it's slow" |
| Finance asks "what's our burn?" and I have to manually recalculate from three different sources | "Budget is always current; I just pull the number" | "Will the data sync correctly? What if it breaks mid-report?" | "I'm used to doing it this way; change is risky" |
| Can't explain *why* a project status changed; I'm guessing at root cause | "The tool shows me the change history and what triggered it" | "What if I find out the historical data was wrong the whole time?" | "I've survived this long without root cause analysis" |

### Firing (What causes them to switch AWAY from this solution)

**Sudden firings:**
1. Data corruption or loss — the report showed one number yesterday and a different number today with no explanation
2. Tool goes down during a reporting window — can't generate report 30 minutes before the meeting
3. A critical field is missing — exec asks about "resource utilisation" and the tool doesn't track it
4. Manual workaround is faster than the tool — the built-in report is slower than exporting to Excel

**Gradual erosion:**
1. Reports drift out of sync with reality — they start requesting data "the old way" because they don't trust the new reports
2. The tool becomes hard to navigate — simple questions require 10 clicks instead of one
3. Data is always 2+ hours stale — exec asks about today's status and the report shows yesterday
4. New projects or workflows aren't reflected in the reporting tool — staff are doing workarounds
5. The tool adds process overhead — now operations director spends time maintaining the reporting tool instead of reducing time

---

## Product Implications

### Opportunity Landscape

**Underserved (build here):**
- Minimise time to gather and compile report (outcome #1) — currently 4+ hours, opportunity to get to <30 min
- Guarantee data freshness (outcome #2) — real-time or <30 min lag
- Identify changes since last check-in automatically (outcome #3) — highlight what's new
- Verify budget accuracy without manual recalculation (outcome #4) — single source of truth
- Reduce ad-hoc data requests (outcome #5) — self-serve answers for common questions
- Fast lookup of project details (outcome #6) — search + drill-down, <5 min answer
- Show root cause of status changes (outcome #7) — linked history, not just snapshots
- Minimise being caught off-guard (outcome #11) — alerts or daily digest of critical changes

**Adequately served (maintain parity):**
- Cascading updates to project managers (outcome #10) — it works; don't regress

**Overserved (simplify/deprioritise):**
- None identified in this analysis. All outcomes reflect real operational needs.

### Recommendations

#### 1. Build: Auto-generated Portfolio Report (Addresses outcomes #1, #2, #4)

**What to build:**
- A "Portfolio Snapshot" report that aggregates all 20+ projects in one view: project name, status (on track / at risk / delayed), budget (total / spent / % variance), timeline (original / current / days slip), and key resource allocation
- Report pulls from live project data (not a cache/export)
- Timestamp shows "data as of [time]" so reader knows freshness
- One click to generate; <1 minute to export/present

**How to measure success:**
- Reporting time drops from 4 hours to <30 minutes
- Zero manual data compilation steps in the preparation flow
- Report generated within 15 minutes of meeting start time

**What NOT to build:**
- Don't build a custom reporting UI that requires configuration for each check-in — it should be one-click standard
- Don't require project managers to fill out a "status form" before reporting appears — pull from existing project data

---

#### 2. Build: Change Detection & Alerts (Addresses outcomes #3, #11, #9)

**What to build:**
- Daily digest or real-time alerts flagging which projects have status changes since yesterday: timeline slip >X days, budget variance >X%, key resource unallocated, blocker added
- Alert shows the change (what was it, what is it now) and the trigger (exec added a new constraint, PM marked a dependency as blocked, etc.)
- Operations director gets a morning digest (5 min read) instead of manually checking all 20 projects

**How to measure success:**
- Operations director identifies critical issues before the leadership meeting
- Number of "I didn't see that coming" questions in meetings drops by 80%
- Time to identify at-risk projects drops from 30 minutes to 5 minutes

**What NOT to build:**
- Don't send alerts for every tiny change (every status update, every comment) — alert fatigue kills adoption
- Don't require custom thresholds per project; use sensible defaults (e.g., 5+ day timeline slip, 10%+ budget variance)

---

#### 3. Build: Project Drill-Down with History (Addresses outcomes #6, #7)

**What to build:**
- From the portfolio report, click any project to see: current status, budget detail (by category if relevant), timeline (original plan vs. current), resources assigned, blockers/risks, and a timeline view showing when status changed and why
- The "why" is populated from project notes, blocker records, or scope change events — not free text, structured data
- Exec can ask "what happened with Project X?" and operations director can answer in <5 min by showing this drill-down view

**How to measure success:**
- Average time to answer a specific project question drops from 15 min to <5 min
- Operations director can explain root cause of status changes without leaving the reporting tool
- Exec confidence in the answer increases (less "I think it's because..." and more "Here's why...")

**What NOT to build:**
- Don't require a narrative text field — structure the data (scope change, resource change, external blocker, dependency issue) instead
- Don't mix project notes with status history; separate the streams so exec can see the history without wading through comments

---

#### 4. Build: Self-Service Data Access for Finance (Addresses outcome #5)

**What to build:**
- A simple "Finance Dashboard" that shows: total portfolio budget, spend to date, burn rate, projected overrun, and budget by project/category
- Finance can answer "what's our Q2 budget position?" without asking operations director
- One-page view; auto-updating from project actuals

**How to measure success:**
- Ad-hoc budget questions from finance drop by 70%
- Operations director is no longer the gatekeeper for basic portfolio metrics
- Finance reports are always based on the same data ops uses (single source of truth)

**What NOT to build:**
- Don't build a full custom reporting UI for finance; one simple dashboard solves 90% of questions
- Don't require finance to understand PM terminology; label things clearly for non-PM audience

---

### Deprioritise / Remove

- Custom report builder with 50 different visualization options — creates decision paralysis and maintenance burden
- Ability to manually override project data in the report — creates inconsistency and conflicts with source truth
- Export to 10 different formats — solve for PDF and Excel; that covers 95% of use cases

---

## Anti-Patterns to Avoid

**Don't ship a "custom report builder."** The jobs-to-be-done research shows operations director wants *less* configuration burden, not more. A pre-built portfolio report that solves the core job in one click beats a flexible builder that requires 30 minutes of setup.

**Don't treat reporting as a "nice-to-have" feature bolted on the side.** The emotional and social jobs reveal that how operations director *feels* (confident, prepared, in control) and how they're *perceived* (organised, trustworthy) are as important as the functional metric. A report that's accurate but slow will lose to a faster competitor.

**Don't ignore the "stale data" job.** Outcome #2 (data freshness) is highly underserved (satisfaction 3/10). If the report data is 2+ hours old, operations director won't trust it and will still use spreadsheets as the "real" source. Real-time or <30min freshness is table stakes.

**Don't require manual action from project managers to make reporting work.** If the report only appears after PMs fill out a form, you've made reporting a bottleneck instead of a solution.

---

## Success Metrics (How to know this area is working)

- **Adoption:** >80% of operations directors use the report for their formal check-ins within 60 days of launch
- **Time savings:** Average reporting prep time drops from 4 hours to <30 minutes (verified via time tracking or session logs)
- **Trust:** Operations director stops using spreadsheets as the "real source" and relies on the tool for all check-ins
- **Response time:** Ability to answer a specific project question in <5 minutes (measured via support requests or observation)
- **Leadership perception:** Exec feedback shifts from "ops seems reactive" to "ops always has the full picture"

---

## Next Steps

**For Product Owner:**
1. Validate job performer context — is the triggering moment really a 2-hour pre-meeting rush? Interview 3-5 operations directors to confirm.
2. Prioritise outcomes — which 2-3 underserved outcomes would create the most value?
3. Define success criteria for each outcome — what does "good enough" look like?

**For Design:**
1. Prototype the Portfolio Snapshot report — one-click, <1 minute to generate, clear and scannable
2. Test the project drill-down — can an exec understand root cause without talking to ops?
3. Design the change alerts — what's the right frequency and detail level to avoid alert fatigue?

**For Engineering:**
1. Audit data freshness — what's the current lag between a project change and when it appears in reports?
2. Identify data gaps — what fields/dimensions are operations directors currently tracking in spreadsheets that don't exist in the PM tool?
3. Design the reporting data model — separate from transactional schema if needed to support fast queries

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.5/17.0 (85%) |
| Evaluated | 2026-05-04 |
| Target duration | 70929 ms |
| Target cost | $0.0946 |
| Permission denials | 1 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires a core functional job statement in the canonical format: "When I [situation], I want to [motivation], so I can [outcome]" | PASS | The artifact's 'Core Functional Job' section reads: "When I have a leadership meeting in 2 hours and need to report on 20+ concurrent projects, I want to quickly verify the current state (budget, timeline, resource allocation, risks) and surface what's changed since the last check-in, so I can present with confidence and answer unexpected questions about specific projects without digging through email chains." Exact canonical format. |
| c2 | Skill requires emotional jobs (how the performer wants to feel) AND social jobs (how they want to be perceived) — not just functional jobs | PASS | The artifact has a dedicated 'Emotional' subsection ('I want to feel confident', 'I want to feel in control', 'I want to avoid feeling embarrassed', 'I want to avoid feeling like a data janitor', 'I want to feel like an operations leader') and a separate 'Social' subsection ('I want to be seen as organised and prepared', 'I want to be seen as trustworthy', 'I want to be seen as responsive'). Both categories are present and distinct. |
| c3 | Skill requires an outcome table with Importance, Current Satisfaction, and Opportunity Score columns | PASS | The 'Desired Outcomes' table explicitly includes columns labelled Importance, Satisfaction, and Opportunity, with 13 populated rows. All three required columns are present. |
| c4 | Skill defines the Opportunity Score formula: Importance + max(Importance - Satisfaction, 0), with thresholds for underserved (>12) and overserved (<6) | PARTIAL | Opportunity scores are computed in the table and outcomes scoring >12 are labelled 'Underserved'. However, the formula is never explicitly written out in the output, the math is not shown, row 1 contains a calculation error (I=9, S=2 → formula gives 16 but output shows 17), and the overserved threshold (<6) is not demonstrated (the analysis states 'None identified' for overserved outcomes, so it cannot be verified). |
| c5 | Skill requires hiring and firing criteria — what causes someone to switch TO and AWAY from the product | PASS | The artifact contains a full 'Hiring / Firing Criteria' section. The hiring table has four columns (Push, Pull, Anxiety, Habit) with concrete rows. The firing section divides into 'Sudden firings' (4 items) and 'Gradual erosion' (5 items). Both switch-TO and switch-AWAY directions are covered. |
| c6 | Skill prohibits solution-specific job statements — "I want to use the dashboard" is explicitly called out as wrong | PARTIAL | All JTBD statements in the output are solution-agnostic (no 'I want to use the dashboard' pattern), demonstrating the skill steers away from solution-specific language. However, no explicit prohibition or anti-example naming 'I want to use the dashboard' appears anywhere in the captured output or artifact. The 'Anti-Patterns to Avoid' section addresses product decisions, not JTBD statement construction conventions. |
| c7 | Skill requires at least 8 outcome statements for the core job — partial credit if outcomes are required but minimum count is not specified | PARTIAL | The outcome table contains exactly 8 rows labelled 'Core' (outcomes #1–#8), meeting the minimum count. An additional 5 rows cover related, emotional, and social jobs. Ceiling is PARTIAL. |
| c8 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The captured output consists of a chat response and an artifact file (docs/jtbd-reporting-analytics.md). Neither contains or references a skill definition file with YAML frontmatter. The artifact starts directly with '# Jobs-to-be-Done Analysis' — no frontmatter. There is no evidence in the captured output about the skill's own file structure. |
| c9 | Output's core functional job is in the canonical format — "When I [need to report status to my exec team], I want to [pull together a portfolio view across projects], so I can [communicate confidence and surface risks]" — solution-agnostic, not "use the dashboard" | PASS | Core Functional Job: "When I have a leadership meeting in 2 hours... I want to quickly verify the current state... so I can present with confidence and answer unexpected questions..." — canonical format, solution-agnostic. No reference to using a specific product or feature. |
| c10 | Output identifies the operations director as the JTBD performer (not generic "user") and describes their context — accountable for portfolio outcomes, weekly exec reporting, mid-market team without a PMO function | PASS | The Job Performer table identifies the performer as 'An operations director during their bi-weekly leadership check-in', describes the triggering context (2 hours before leadership meeting, 20+ concurrent projects, exec reporting), current solution (spreadsheets + Slack + email), frequency (twice weekly formal + ad-hoc every 2-3 days), and emotional state. Rich context well beyond a generic 'user'. |
| c11 | Output produces emotional jobs (e.g. "I want to feel in control of project outcomes", "I want to feel I'm not blindsided by a project going red") and social jobs (e.g. "I want to be seen as the operations leader who has the answers", "I want to avoid being the person caught off-guard at the exec meeting") — both, not only functional | PASS | Emotional jobs include: 'feel confident that the data I'm presenting is current', 'feel in control', 'avoid feeling embarrassed by not being able to answer a direct question', 'avoid feeling like a data janitor', 'feel like an operations leader'. Social jobs include: 'be seen as organised and prepared', 'be seen as trustworthy', 'be seen as responsive'. Both categories fully populated. |
| c12 | Output's outcome table has at least 8 rows — desired outcomes the operations director cares about (e.g. "minimise time spent compiling status reports", "increase confidence in delivery dates", "reduce surprises in exec meetings") — with Importance, Current Satisfaction, and Opportunity Score columns | PASS | The Desired Outcomes table contains 13 rows, each with Importance, Satisfaction, and Opportunity columns populated. Rows include outcomes like 'Minimise the time it takes to gather all project data' (I=9, S=2), 'Minimise the likelihood that the data in my report is stale' (I=9, S=3), 'Increase confidence that budget numbers are accurate' (I=9, S=4), and 'Minimise the feeling of being caught off-guard' (I=7, S=2). |
| c13 | Output's Opportunity Scores are computed via the formula `Importance + max(Importance - Satisfaction, 0)` — with the math shown — and outcomes scoring >12 are classified as underserved (opportunities), <6 as overserved | PARTIAL | Opportunity scores are present in the table and outcomes >12 are labelled 'Underserved'. However, the formula is not written out anywhere; no derivation or calculation steps are shown. Row 1 (I=9, S=2) shows 17 but the formula yields 16. The overserved threshold (<6) cannot be verified since the output reports 'None identified' for overserved outcomes. Partial credit: scores present and underserved threshold applied, but math not shown and formula not stated. |
| c14 | Output's hiring criteria name what causes the operations director to switch TO Clearpath — e.g. "moved from Excel rollups when first tried Clearpath because exec summaries auto-generated saving 4 hours/week" — concrete, not "they want better reporting" | PASS | The Push column cites 'Reporting takes 4+ hours per check-in; manual consolidation is error-prone' and 'Finance asks what's our burn? and I have to manually recalculate from three different sources'. The Pull column cites 'I saw a demo where the report auto-generated in 2 minutes' and 'Budget is always current; I just pull the number'. Concrete, quantified motivations rather than generic 'wants better reporting'. |
| c15 | Output's firing criteria name what causes operations directors to switch AWAY from Clearpath — e.g. "switched to Asana when exec audience required mobile dashboards we don't support" | PASS | Sudden firings include: 'Data corruption or loss — the report showed one number yesterday and a different number today with no explanation', 'Tool goes down during a reporting window — can't generate report 30 minutes before the meeting', 'Manual workaround is faster than the tool'. Gradual erosion includes 'Data is always 2+ hours stale' and 'New projects or workflows aren't reflected in the reporting tool'. Specific and concrete. |
| c16 | Output is solution-agnostic — every job and outcome describes the desired future state independent of the product, NOT "use the new analytics module" | PASS | All job statements (core functional, related, emotional, social) and all 13 outcome statements describe desired states ('minimise time', 'increase confidence', 'minimise likelihood of stale data') with no references to using any specific product feature or module. Product implications are in a separate recommendations section, correctly separated from the JTBD layer. |
| c17 | Output addresses the data dimension explicitly — operations directors care about data freshness, accuracy, ability to drill down, ability to export — these become outcomes | PASS | Outcome #2: 'Minimise the likelihood that the data in my report is stale (>4 hours old)' (freshness). Outcome #4: 'Increase the confidence that budget numbers are accurate before I present them' (accuracy). Outcome #6: 'Increase the ability to answer a specific question about project X in <5 minutes without leaving the reporting tool' (drill-down). The anti-patterns section explicitly states 'Don't ignore the stale data job.' The firing criteria include 'Data is always 2+ hours stale'. |
| c18 | Output addresses team-level vs portfolio-level outcomes — operations directors operate at the portfolio (across teams) while team leads operate at the team level; the JTBD is portfolio-focused | PARTIAL | The entire analysis is framed at the portfolio level: '20+ concurrent projects', 'portfolio health', 'Portfolio Snapshot report'. The job performer is explicitly an operations director (not a team lead or PM). However, the output never explicitly contrasts portfolio-level vs team-level outcomes or mentions team leads as a separate performer with different jobs. The portfolio framing is consistent throughout but the distinction is implicit, not called out. Ceiling is PARTIAL. |

### Notes

The output is a strong, well-structured JTBD analysis that correctly implements most of the required elements: canonical job statement format, both emotional and social job dimensions, a 13-row outcome table with all required columns, concrete hiring/firing criteria presented in a four-forces framework, and consistently solution-agnostic language throughout. The main gaps are: (1) the Opportunity Score formula is never explicitly written out and one row contains a calculation error (row 1 shows 17, formula yields 16); (2) the skill's own YAML frontmatter cannot be verified from the output; (3) there is no explicit prohibition of solution-specific job statement patterns cited in the output; and (4) the team-level vs portfolio-level distinction is implicit rather than explicitly articulated. The product implications section and anti-patterns section add genuine value beyond the JTBD framework itself, demonstrating that the skill prompted actionable translation of the analysis.
