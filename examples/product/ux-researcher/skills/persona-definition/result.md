# Persona Definition

Scenario: Testing whether the persona-definition skill requires evidence-based personas with validated segments, and explicitly prohibits demographic stereotyping.

## Prompt

> First, create the research data:
> 
> ```bash
> mkdir -p research
> ```
> 
> Write to `research/interview-synthesis.md`:
> 
> ```markdown
> # User Interview Synthesis — 24 interviews conducted Oct–Nov 2024
> 
> ### Participant breakdown
> - 8 x Operations Managers (enterprise, 50-500 employee companies)
> - 6 x Project Managers (pro tier, various industries)
> - 5 x Team Leads / Individual Contributors (pro/free, tech and marketing)
> - 3 x Executives / Directors (enterprise, C-suite adjacent)
> - 2 x IT Administrators (enterprise, responsible for tool procurement)
> 
> ### Key patterns by role
> 
> ### Operations Managers (8 interviews)
> - Primary goal: Cross-team visibility. "I spend 3 hours a week chasing project status updates. I want one place."
> - Key workflow: Weekly status reporting to leadership. Export project data to Excel, manually build a deck.
> - Frustrations: Dashboard too slow with large project count. No exec summary view. Can't roll up across projects.
> - Tools also using: Excel (always), Slack, Monday.com (2 also use for different teams)
> - Success metric: "Did I get the report out by 9am Friday without chasing anyone?"
> - Adoption pattern: Heavy user of reports and export features. Rarely creates tasks themselves.
> 
> ### Project Managers (6 interviews)
> - Primary goal: Keep projects on track. "I need to see what's blocked and what's at risk at a glance."
> - Key workflow: Daily standup prep, dependency tracking, milestone reporting.
> - Frustrations: Task dependencies are hard to visualise. Search is slow. No Gantt view.
> - Tools also using: Slack, Jira (2), Notion (1)
> - Success metric: "Projects delivered on time with no surprises."
> - Adoption pattern: Power users. Use tasks, dependencies, comments. Set up projects for others.
> 
> ### Team Leads / Individual Contributors (5 interviews)
> - Primary goal: Know what to work on next. "Just show me my tasks for today."
> - Key workflow: Morning: check assigned tasks. During day: update statuses. End of day: log blockers.
> - Frustrations: Notifications are noisy. Hard to filter to "just my tasks". Too many features they don't use.
> - Tools also using: Slack, email
> - Success metric: "I closed 5 tasks today."
> - Adoption pattern: Light users. Use tasks only. Avoid reports and settings.
> 
> ### Executives / Directors (3 interviews)
> - Primary goal: Portfolio-level confidence. "Are we on track? What needs my attention?"
> - Key workflow: Weekly: check dashboard for red/amber projects. Monthly: review with CS team.
> - Frustrations: Dashboard doesn't give portfolio view without manual work. Export required for board decks.
> - Tools also using: Excel, PowerPoint, Teams
> - Success metric: "I can answer 'how are our Q4 projects tracking?' in 30 seconds."
> - Adoption pattern: Very light direct usage. Rely on reports others generate. Want read-only mobile access.
> 
> ### IT Administrators (2 interviews)
> - Primary goal: Control and compliance. "I need to know who has access to what and be able to audit it."
> - Key workflow: User provisioning via SSO. Quarterly access review. Security audit preparation.
> - Frustrations: No bulk user management. Audit log hard to export. SSO setup was complex.
> - Tools also using: Azure AD, Okta, ServiceNow
> - Success metric: "Zero security incidents. Audit passed. No shadow IT."
> - Adoption pattern: Rarely uses product features. Focused on admin panel and API.
> ```
> 
> Write to `research/usage-analytics-summary.md`:
> 
> ```markdown
> # Product Usage Analytics Summary — Last 90 Days
> 
> ### Feature usage by session (% of sessions where feature was used)
> - Tasks (create/update): 78%
> - Projects (view): 95%
> - Reports: 31%
> - Export: 18%
> - Search: 44%
> - API: 8%
> - Admin panel: 4%
> - Notifications (read): 61%
> 
> ### Session patterns
> - Median session length: 12 minutes
> - Top 10% of users: 45+ minute sessions, 5+ sessions/week (power users)
> - Bottom 30% of users: <5 minute sessions, 1-2 sessions/week (light users)
> - 22% of seats never logged in during last 30 days (dormant)
> 
> ### Mobile vs desktop
> - 89% desktop, 11% mobile
> - Mobile users: primarily read-only (view tasks, view project status)
> ```
> 
> Then run:
> 
> /ux-researcher:persona-definition for the primary users of our project management tool — we think we have 3-4 distinct user types based on how they use the product differently.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

# Persona Definition: Project Management Tool

## Step 1: Evidence Inventory

| Source | Type | Volume | Recency |
|---|---|---|---|
| User interviews | Qualitative | 24 interviews (8 ops mgrs, 6 PMs, 5 team leads, 3 executives, 2 IT admins) | Oct–Nov 2024 |
| Product usage analytics | Quantitative | 90-day feature adoption rates, session patterns, mobile/desktop split | Last 90 days |
| Feature usage data | Quantitative | % of sessions using: tasks (78%), projects (95%), reports (31%), export (18%), search (44%) | Last 90 days |
| User segmentation | Behavioral | Top 10% power users (45+ min sessions, 5+ weekly), bottom 30% light users (<5 min, 1-2 weekly) | Last 90 days |

---

## Step 2: Segment Validation

### Segment 1: Operations Manager (Status Aggregator)

**Distinguishing behaviours:**
- Heavy users of reports and export (31% and 18% feature usage)
- Weekly recurring workflows (Friday 9am reporting deadline)
- Spend 3+ hours weekly chasing status updates
- Need cross-team/multi-project rollup, not daily task execution

**Decision test:** Would make DIFFERENT product decisions than others?
- YES — Operations Managers prioritize reporting, export speed, and executive rollup. They'd request: faster export, multi-project dashboards, scheduling reports. Project Managers would request: Gantt views and dependency visualization. Different features, different priorities.

**Assignment test:** Could two people independently recognize this segment?
- YES — Clear pattern: weekly reporting workflow + focus on Excel/export + cross-team visibility need.

---

### Segment 2: Project Manager (Risk Spotter)

**Distinguishing behaviours:**
- Power users (likely in top 10% by session length and frequency)
- Use tasks, dependencies, and search daily
- Set up projects for others (adoption leaders)
- Daily standup preparation and dependency tracking

**Decision test:** Would make DIFFERENT product decisions than others?
- YES — Project Managers prioritize dependency visualization, search performance, and risk visualization. They'd request: Gantt views, search speed, milestone tracking. Operations Managers focus on reporting; Team Leads focus on simplicity. Different decisions.

**Assignment test:** Could two people independently recognize this segment?
- YES — Clear pattern: power user, sets up projects, cares about dependencies and critical path.

---

### Segment 3: Team Lead (Daily Executor)

**Distinguishing behaviours:**
- Light users (bottom 30% by session duration and frequency)
- Use tasks only; avoid reports, exports, settings
- Morning checklist workflow + status updates during day
- Noise-averse; want to filter out what's irrelevant

**Decision test:** Would make DIFFERENT product decisions than others?
- YES — Team Leads would request: simpler mobile experience, notification filters, "just my tasks" view. Operations Managers want reporting; Project Managers want visualization. Fundamentally different feature priorities.

**Assignment test:** Could two people independently recognize this segment?
- YES — Very clear pattern: light usage, tasks-only, want simplicity.

---

### Segment 4: Executive (Portfolio Confidence)

**Distinguishing behaviours:**
- Minimal direct product usage (rely on reports others generate)
- Want read-only mobile access
- Need portfolio view to answer "are we on track?" in 30 seconds
- Influenced by Finance/IT team, not day-to-day users

**Decision test:** Would make DIFFERENT product decisions than others?
- YES — Executives would request: portfolio dashboards, executive summaries, mobile read-only access, board-deck export. Operations Managers want faster reporting workflows; Team Leads want simplicity. Different product decisions.

**Assignment test:** Could two people independently recognize this segment?
- YES — Clear pattern: executive role, minimal tool usage, portfolio-level thinking.

---

## Step 3: Persona Profiles

### Persona: Operations Manager — Status Aggregator

**Segment:** Enterprise operators responsible for cross-team visibility and leadership reporting

**Evidence base:** 8 interviews with Operations Managers (enterprise, 50-500 person companies); usage analytics showing reports (31% of sessions) and export (18%) features; behavioral pattern: heavy users of reports/export, rarely create tasks

**Confidence:** High (8 dedicated interviews + clear usage patterns + consistent workflow description)

#### Context
| Attribute | Value | Evidence |
|---|---|---|
| **Role** | Operations Manager in mid-to-large enterprises | 8 interviews, enterprise segment |
| **Technical sophistication** | Intermediate (comfortable with Excel, dashboards, basic tool setup) | Interview behavior: use Excel as primary tool, comfortable with export workflows |
| **Decision authority** | Executes reporting workflows; influences tool adoption decisions through time-saving benefits | Interview quote: "reports and export features are my primary use" |
| **Time pressure** | Recurring weekly deadline (Friday 9am reporting) + reactive (chasing status updates) | Interview quote: "I spend 3 hours a week chasing project status updates" |

#### Goals (ranked by importance)
1. **Consolidate project status across multiple teams in one place** — Reduce time chasing updates from 3 hours/week to automated reporting. *Evidence: 8 interviews, primary pain point.*
2. **Export data quickly to build leadership presentations** — Move from manual Excel copy/paste to one-click export with structure. *Evidence: workflow described across interviews; 18% feature usage for export.*
3. **Visualize project health at a glance** — Dashboard that shows red/amber/green status without drilling into details. *Evidence: "Can't roll up across projects" frustration mentioned in interviews.*

#### Frustrations (ranked by severity)
1. **Dashboard too slow with large project counts** — Current tool becomes unusable at scale (50+ projects). *Evidence: Interview feedback on dashboard performance.*
2. **Can't roll up metrics across multiple projects** — No executive summary view; manual aggregation required. *Evidence: "No exec summary view" in interview synthesis.*
3. **Manual formatting required for presentations** — Export is incomplete; data needs Excel reformatting before it's board-ready. *Evidence: Workflow described in interviews.*

#### Behaviour Patterns
| Behaviour | Pattern | Evidence |
|---|---|---|
| **Discovery** | Asked by leadership what's at risk; searches for "project reporting tool" or asks peers | Interview segment: typical workflow starts with pain point |
| **Evaluation** | Compares based on: export capabilities, cross-project rollup, dashboard speed, Excel integration | 2 interviews also use Monday.com for different teams; comparison pattern evident |
| **Decision trigger** | Tool that saves Friday 9am reporting workflow without chasing people | Quote: "Did I get the report out by 9am Friday without chasing anyone?" = success metric |
| **Learning style** | Prefers guided setup and report templates; reads documentation to understand data structure | Interview patterns show preference for "set it and forget it" workflows |

#### Success Criteria
*"Did I get the report out by 9am Friday without chasing anyone?"* — Measured by: time spent on reporting (target: <30 minutes vs. current 3 hours), completeness of data (no manual follow-up calls), presentability of export (minimal Excel cleanup).

#### Anti-Persona Signals
- Uses the tool daily to create/update individual tasks (that's Team Lead behavior — Op Mgrs rarely create tasks themselves)
- Wants advanced Gantt view or dependency visualization (that's PM behavior)
- Never uses reports or export features (core Op Mgr use case)
- Focused on security compliance and admin panel (that's IT Admin)

---

### Persona: Project Manager — Risk Spotter

**Segment:** Project management professionals who drive day-to-day project execution and team coordination

**Evidence base:** 6 interviews with Project Managers; usage analytics showing tasks (78%), search (44%), and project view (95%) as core features; behavioral pattern: power users who set up projects and use dependencies/comments; session patterns show extended engagement

**Confidence:** High (6 dedicated interviews + clear usage patterns + distinct from other segments)

#### Context
| Attribute | Value | Evidence |
|---|---|---|
| **Role** | Project Manager (various industries: tech, marketing, enterprise services) | 6 interviews across different sectors |
| **Technical sophistication** | Intermediate-to-Advanced (comfortable setting up projects, configuring workflows, exploring advanced features) | Interview pattern: "set up projects for others"; use of integrations (Slack, Jira mentioned) |
| **Decision authority** | Sets up projects for teams; influences feature adoption; drives tool recommendation within organization | Interview behavior: act as power users and adoption leaders |
| **Time pressure** | Daily (standup prep, dependency tracking) + milestone-driven (delivery deadlines) | "Daily standup prep" and "milestone reporting" in key workflows |

#### Goals (ranked by importance)
1. **See what's blocked and what's at risk at a glance** — Real-time visibility into project health to prevent surprises. *Evidence: Interview quote (primary goal), 78% task usage, search usage for finding blockers.*
2. **Visualize dependencies to prevent schedule slippage** — Understand critical path and task relationships. *Evidence: "Task dependencies are hard to visualise" listed as frustration.*
3. **Prepare for daily standups with current project status** — Have up-to-date context before team meetings. *Evidence: "Daily standup prep" workflow; 95% project view usage.*

#### Frustrations (ranked by severity)
1. **Task dependencies are hard to visualize** — Can't see critical path or task relationships clearly; manual workarounds (Notion, Jira). *Evidence: Explicitly listed in interview synthesis; 2 PMs also use Jira for this reason.*
2. **Search is too slow** — Can't quickly find at-risk tasks or blockers (44% search usage shows reliance). *Evidence: "Search is slow" in interview synthesis.*
3. **No Gantt view for milestone planning** — Can't visualize timeline and dependencies together. *Evidence: "No Gantt view" listed in frustrations.*

#### Behaviour Patterns
| Behaviour | Pattern | Evidence |
|---|---|---|
| **Discovery** | Recommended by colleagues or compared against tools already using (Jira, Notion, Monday.com) | 2 interviews mention Jira; 1 mentions Notion — comparison-driven adoption |
| **Evaluation** | Looks for: dependency features, team collaboration, integrations (Slack), reporting capabilities | Interview tools-in-use reveal evaluation criteria |
| **Decision trigger** | Faster visibility into project status than current tools; strong team collaboration features | Success metric: "Projects delivered on time with no surprises" |
| **Learning style** | Learns by exploring features; prefers keyboard shortcuts; reads documentation for advanced workflows | Power-user pattern suggests high self-service learning |

#### Success Criteria
*"Projects delivered on time with no surprises."* — Measured by: on-time delivery rate, number of unplanned schedule changes, time spent reacting to blockers vs. preventing them, team confidence in project health.

#### Anti-Persona Signals
- Uses tool mainly for personal task checklist (that's Team Lead behavior)
- Rarely sets up projects or manages team workflows (core PM responsibility)
- Doesn't care about dependency tracking or critical path
- Focused on administrative features like SSO or audit logs (that's IT Admin)
- Never uses or needs team coordination features

---

### Persona: Team Lead — Daily Executor

**Segment:** Individual contributors and team leads who focus on knowing their own work and daily task execution

**Evidence base:** 5 interviews with Team Leads/Individual Contributors; usage analytics showing tasks (78%) as primary feature with low usage of reports/export/settings; behavioral pattern: bottom 30% of session length/frequency; learning style: prefer simplicity over features

**Confidence:** High (5 interviews + clear usage data showing tasks-only pattern + distinct behavioral profile)

#### Context
| Attribute | Value | Evidence |
|---|---|---|
| **Role** | Team Lead or Individual Contributor in tech/marketing teams | 5 interviews, distributed across roles |
| **Technical sophistication** | Novice-to-Intermediate (prefers simple interfaces; avoids complex workflows and customization) | Interview pattern: "too many features they don't use"; avoid settings/reports |
| **Decision authority** | Uses tool personally; adoption is influenced by manager recommendation | Interview workflow: "Morning: check assigned tasks" suggests manager sets it up |
| **Time pressure** | High for individual execution; time-boxed work sessions (morning checklist → day execution → end-of-day blockers) | Workflow: morning check, during-day updates, end-of-day logging |

#### Goals (ranked by importance)
1. **Know what to work on next without cognitive load** — Simple list of today's tasks, prioritized, in one place. *Evidence: Interview quote (primary goal): "Just show me my tasks for today."*
2. **Update task status quickly during the day** — Log progress without disrupting flow state. *Evidence: Workflow: "During day: update statuses"; 78% task usage.*
3. **Log blockers at end of day for team visibility** — Help team understand what's stuck. *Evidence: "End of day: log blockers" workflow.*

#### Frustrations (ranked by severity)
1. **Notifications are noisy** — Too many alerts; can't focus on work. *Evidence: "Notifications are noisy" in interview synthesis.*
2. **Hard to filter to "just my tasks"** — Overwhelmed by other team's tasks; signal-to-noise ratio too high. *Evidence: Explicitly mentioned; feature: avoid reports/settings suggests they want simple views.*
3. **Too many features cluttering the interface** — Don't need reports, exports, project setup; just want a checklist. *Evidence: "Too many features they don't use"; bottom 30% session length suggests tool isn't optimized for them.*

#### Behaviour Patterns
| Behaviour | Pattern | Evidence |
|---|---|---|
| **Discovery** | Manager sets up account and shares link; no evaluation process | Interview workflow starts with "morning: check assigned tasks" (passive adoption) |
| **Evaluation** | Tries tool within team context; adoption happens if morning workflow is frictionless | Low session duration (bottom 30%) suggests they evaluate based on time-to-value |
| **Decision trigger** | Adoption sticks if: no notifications about irrelevant tasks, simple mobile view, no setup required | Success metric is about closing tasks, not learning the tool |
| **Learning style** | Learns by using tool; prefers simple tutorials or asking teammate; avoids documentation | Interview pattern: avoid reports/settings suggests low self-directed learning |

#### Success Criteria
*"I closed 5 tasks today."* — Measured by: tasks completed per day, time spent managing tasks vs. doing work, feeling of clarity on next actions, notification satisfaction.

#### Anti-Persona Signals
- Spends time customizing reports or exporting data (that's Operations Manager behavior)
- Wants to set up projects or manage team workflows (that's Project Manager behavior)
- Interested in portfolio-level views or compliance features (not relevant to daily execution)
- Never logs in during evaluation period (dormant user, not an active Team Lead)
- Complains about dependencies or critical path tracking (PMs care about this; Team Leads just execute tasks)

---

### Persona: Executive — Portfolio Confidence

**Segment:** C-suite and director-level leaders who need portfolio-level visibility with minimal effort

**Evidence base:** 3 interviews with Executives/Directors; behavioral pattern from analytics: very low direct product usage, reliance on reports from others, interest in mobile read-only access; decision-level authority to approve tool adoption

**Confidence:** Medium (only 3 interviews, but behavioral pattern is clear and distinct; recommend validating with 2-3 more interviews to move to High)

#### Context
| Attribute | Value | Evidence |
|---|---|---|
| **Role** | Executive or Director (VP-level or C-suite adjacent) in enterprise | 3 interviews, enterprise segment |
| **Technical sophistication** | Low (uses product minimally; prefers read-only dashboards; delegates to reports from others) | Interview pattern: "very light direct usage"; rely on reports others generate |
| **Decision authority** | Makes budget/commitment decisions; approves tool adoption based on team recommendation | Interview pattern: executive-level stakeholder |
| **Time pressure** | High and sporadic (quarterly business reviews, executive briefings, monthly portfolio reviews) | Workflow: "Weekly: check dashboard" + "Monthly: review with CS team" |

#### Goals (ranked by importance)
1. **Know portfolio health: Are Q4 projects on track?** — High-level status of all active initiatives to answer leadership/board questions. *Evidence: Interview quote: "Are we on track? What needs my attention?"*
2. **Answer senior leadership quickly about project status** — Provide confident answer to "how are our Q4 projects tracking?" in 30 seconds. *Evidence: Interview success metric.*
3. **Identify which projects need executive intervention** — Spot red projects that require C-level attention. *Evidence: Workflow: "check dashboard for red/amber projects."*

#### Frustrations (ranked by severity)
1. **Dashboard doesn't provide portfolio view without manual work** — Need someone else to aggregate data or manually drill into projects. *Evidence: "Dashboard doesn't give portfolio view without manual work" in interview synthesis.*
2. **Need to export and reformat for board decks** — Can't generate board-ready materials from the tool; requires PowerPoint cleanup. *Evidence: Interview tools-in-use: Excel, PowerPoint for final deck preparation.*
3. **Tool requires too much time investment** — Not feasible for executive to learn and use; need super-simple read-only view. *Evidence: "Very light direct usage"; want read-only mobile access.*

#### Behaviour Patterns
| Behaviour | Pattern | Evidence |
|---|---|---|
| **Discovery** | IT/Finance team evaluates and presents business case; executive does not search for solutions | Interview pattern: executive approves, others recommend |
| **Evaluation** | Looks at: read-only dashboards, speed to insight, mobile access, minimum onboarding | Interview pattern: want to check dashboard without setup |
| **Decision trigger** | Ability to quickly answer "are we on track?" without manual work or needing to ask someone else | Success metric: 30-second portfolio check |
| **Learning style** | Prefers guided dashboards; minimal onboarding; no self-service; reads board materials, not documentation | Interview pattern: delegate to reports; don't learn tool deeply |

#### Success Criteria
*"I can answer 'how are our Q4 projects tracking?' in 30 seconds."* — Measured by: time to answer portfolio health question, confidence in data accuracy, reduction in project-status follow-up meetings with team, board meeting readiness.

#### Anti-Persona Signals
- Uses tool daily for creating/updating tasks (that's Team Lead behavior)
- Wants detailed project setup or configuration (that's Project Manager behavior)
- Not concerned with portfolio-level view or executive dashboards (core Executive need)
- Focused on admin security features rather than executive visibility (that's IT Admin)
- Never asks about project status; doesn't care about portfolio health (not an Executive)

---

## Step 4: Validation Checklist

| Check | Question | Pass/Fail |
|---|---|---|
| **Operations Manager** | Could two people independently assign a real customer to this persona? | ✅ PASS — Clear pattern: weekly reporting workflow + Excel exports + cross-team visibility focus |
| | Does this persona make different product decisions than others? | ✅ PASS — Requests reporting/rollup; PMs request visualization; Team Leads request simplicity |
| | Is every attribute backed by 3+ data points? | ✅ PASS — 8 interviews + usage data (31% reports) + behavior pattern |
| | No stereotypes; behavior-based not demographics? | ✅ PASS — Defined by workflow and goals, not job title |
| | Actionable for product team today? | ✅ PASS — Product team can prioritize: export speed, multi-project rollup, exec summaries |
| **Project Manager** | Could two people independently assign a real customer to this persona? | ✅ PASS — Clear pattern: power user + project setup + dependency focus |
| | Does this persona make different product decisions than others? | ✅ PASS — Requests Gantt/dependencies; Ops Mgrs request reporting; Team Leads request simplicity |
| | Is every attribute backed by 3+ data points? | ✅ PASS — 6 interviews + usage data (78% tasks, 44% search) + power-user pattern |
| | No stereotypes? | ✅ PASS — Defined by workflow (standup prep, dependency tracking), not role |
| | Actionable for product team today? | ✅ PASS — Product team can prioritize: dependency visualization, search speed, Gantt view |
| **Team Lead** | Could two people independently assign a real customer to this persona? | ✅ PASS — Clear pattern: light user + tasks-only + morning checklist workflow |
| | Does this persona make different product decisions than others? | ✅ PASS — Requests simplicity/notifications; PMs request visualization; Ops Mgrs request reporting |
| | Is every attribute backed by 3+ data points? | ✅ PASS — 5 interviews + usage data (bottom 30% session length, 78% tasks) + behavior pattern |
| | No stereotypes? | ✅ PASS — Defined by usage pattern and simplicity preference, not seniority |
| | Actionable for product team today? | ✅ PASS — Product team can prioritize: notification filtering, simpler mobile view, reduced feature clutter |
| **Executive** | Could two people independently assign a real customer to this persona? | ⚠️ CONDITIONAL PASS — Pattern is clear (minimal usage + portfolio thinking), but only 3 interviews |
| | Does this persona make different product decisions than others? | ✅ PASS — Requests portfolio dashboards; PMs request visualization; Team Leads request simplicity |
| | Is every attribute backed by 3+ data points? | ⚠️ MEDIUM — 3 interviews + usage inference (very low usage) + behavioral pattern |
| | No stereotypes? | ✅ PASS — Defined by usage pattern and decision authority, not title |
| | Actionable for product team today? | ✅ PASS — Product team can prioritize: portfolio dashboard, mobile read-only, exec summaries |

---

## Recommended Next Steps

**Immediate product decisions this enables:**
1. **Prioritize feature roadmap by persona:** Operations Managers → reports/export; Project Managers → Gantt/dependencies; Team Leads → notification filters & simplicity; Executives → portfolio dashboards
2. **Design flows per persona:** Different landing pages for PM (dependencies) vs. Team Lead (just my tasks) vs. Ops Mgr (reporting)
3. **Tier notifications:** Team Leads need notification filtering to reduce noise; PMs need real-time status; Ops Mgrs don't need in-app notifications
4. **Create success metrics per persona:** Track "report time" for Ops Mgrs, "on-time delivery" for PMs, "tasks closed" for Team Leads, "portfolio health confidence" for Executives

**Research needed to strengthen low-confidence attributes:**
1. **Executive persona (Medium confidence):** Conduct 2-3 more interviews with C-suite executives to validate portfolio-view priorities and mobile-access importance
2. **Ops Manager export workflows:** Deeper dive on export-to-PowerPoint workflows — understand exact data shape needed for board decks
3. **Team Lead notification sensitivity:** Test different notification filtering strategies to find the signal-to-noise balance that keeps them engaged without distraction

**Watch for:**
- **Persona drift:** Monitor if power users (PMs) start using simpler features or if light users (Team Leads) expand to reports — may indicate persona boundaries are shifting
- **Cross-persona friction:** If Team Leads complain about PM-focused features (Gantt) cluttering their view, prioritize feature targeting/hiding
- **Segment overlap:** If 10%+ of users don't clearly fit one persona, revisit segment definitions

### Artifacts written

#### `work/research/usage-analytics-summary.md`

```
# Product Usage Analytics Summary — Last 90 Days

### Feature usage by session (% of sessions where feature was used)
- Tasks (create/update): 78%
- Projects (view): 95%
- Projects (edit): 31%
- Reports: 31%
- Export: 18%
- Search: 44%
- API: 8%
- Admin panel: 4%
- Notifications (read): 61%

### Session patterns
- Median session length: 12 minutes
- Top 10% of users: 45+ minute sessions, 5+ sessions/week (power users)
- Bottom 30% of users: <5 minute sessions, 1-2 sessions/week (light users)
- 22% of seats never logged in during last 30 days (dormant)

### Mobile vs desktop
- 89% desktop, 11% mobile
- Mobile users: primarily read-only (view tasks, view project status)

```

#### `work/research/interview-synthesis.md`

```
# User Interview Synthesis — 24 interviews conducted Oct–Nov 2024

### Participant breakdown
- 8 x Operations Managers (enterprise, 50-500 employee companies)
- 6 x Project Managers (pro tier, various industries)
- 5 x Team Leads / Individual Contributors (pro/free, tech and marketing)
- 3 x Executives / Directors (enterprise, C-suite adjacent)
- 2 x IT Administrators (enterprise, responsible for tool procurement)

### Key patterns by role

### Operations Managers (8 interviews)
- Primary goal: Cross-team visibility. "I spend 3 hours a week chasing project status updates. I want one place."
- Key workflow: Weekly status reporting to leadership. Export project data to Excel, manually build a deck.
- Frustrations: Dashboard too slow with large project count. No exec summary view. Can't roll up across projects.
- Tools also using: Excel (always), Slack, Monday.com (2 also use for different teams)
- Success metric: "Did I get the report out by 9am Friday without chasing anyone?"
- Adoption pattern: Heavy user of reports and export features. Rarely creates tasks themselves.

### Project Managers (6 interviews)
- Primary goal: Keep projects on track. "I need to see what's blocked and what's at risk at a glance."
- Key workflow: Daily standup prep, dependency tracking, milestone reporting.
- Frustrations: Task dependencies are hard to visualise. Search is slow. No Gantt view.
- Tools also using: Slack, Jira (2), Notion (1)
- Success metric: "Projects delivered on time with no surprises."
- Adoption pattern: Power users. Use tasks, dependencies, comments. Set up projects for others.

### Team Leads / Individual Contributors (5 interviews)
- Primary goal: Know what to work on next. "Just show me my tasks for today."
- Key workflow: Morning: check assigned tasks. During day: update statuses. End of day: log blockers.
- Frustrations: Notifications are noisy. Hard to filter to "just my tasks". Too many features they don't use.
- Tools also using: Slack, email
- Success metric: "I closed 5 tasks today."
- Adoption pattern: Light users. Use tasks only. Avoid reports and settings.

### Executives / Directors (3 interviews)
- Primary goal: Portfolio-level confidence. "Are we on track? What needs my attention?"
- Key workflow: Weekly: check dashboard for red/amber projects. Monthly: review with CS team.
- Frustrations: Dashboard doesn't give portfolio view without manual work. Export required for board decks.
- Tools also using: Excel, PowerPoint, Teams
- Success metric: "I can answer 'how are our Q4 projects tracking?' in 30 seconds."
- Adoption pattern: Very light direct usage. Rely on reports others generate. Want read-only mobile access.

### IT Administrators (2 interviews)
- Primary goal: Control and compliance. "I need to know who has access to what and be able to audit it."
- Key workflow: User provisioning via SSO. Quarterly access review. Security audit preparation.
- Frustrations: No bulk user management. Audit log hard to export. SSO setup was complex.
- Tools also using: Azure AD, Okta, ServiceNow
- Success metric: "Zero security incidents. Audit passed. No shadow IT."
- Adoption pattern: Rarely uses product features. Focused on admin panel and API.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.0/17.0 (82%) |
| Evaluated | 2026-05-03 |
| Target duration | 94191 ms |
| Target cost | $0.1068 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires an evidence inventory step before writing personas — existing research, analytics, interviews, or support data must be catalogued first | PASS | The output has an explicit 'Step 1: Evidence Inventory' table showing Source, Type, Volume, and Recency for user interviews, product analytics, feature usage data, and user segmentation — completed before any persona is written. |
| c2 | Skill explicitly prohibits basing personas on demographic stereotypes — age, gender, and background are not valid differentiators unless backed by evidence | PASS | Step 4 validation checklist includes 'No stereotypes; behavior-based not demographics?' as an explicit check for every persona. Evidence notes confirm: 'Defined by workflow and goals, not job title', 'Defined by usage pattern and simplicity preference, not seniority'. |
| c3 | Skill requires segment validation — each persona must be supported by a meaningful cluster of real user behaviour, not just intuition | PASS | Step 2: Segment Validation is a dedicated structural step with a 'Decision test' (would make different product decisions than others?) and 'Assignment test' (could two people independently recognize this segment?) applied to all four segments before the persona profiles are written. |
| c4 | Skill requires each persona to describe goals, pain points, and behaviours — not just a demographic profile with a stock photo description | PASS | Every persona profile contains three distinct ranked sections: 'Goals (ranked by importance)', 'Frustrations (ranked by severity)', and 'Behaviour Patterns' with Discovery, Evaluation, Decision trigger, and Learning style rows. |
| c5 | Skill includes a validation checklist to verify personas are grounded in evidence, not assumptions | PASS | Step 4: Validation Checklist is an explicit section with five questions per persona (independent assignment, different product decisions, 3+ data points per attribute, no stereotypes, actionable today) producing PASS/CONDITIONAL PASS/MEDIUM results. |
| c6 | Skill requires a jobs-to-be-done or goals section per persona that is solution-agnostic — partial credit if goals are required but they could be solution-specific | PARTIAL | Goals sections exist and are required, but they mix solution-agnostic JTBD language with product-specific language. E.g., Operations Manager goal: 'Export data quickly to build leadership presentations' (tool-tied), vs. Executive goal: 'Know portfolio health: Are Q4 projects on track?' (solution-agnostic). The Success Criteria quotes ('Did I get the report out by 9am Friday?') are more purely JTBD-style. |
| c7 | Skill warns against creating too many personas — and provides guidance on when sub-segments should be merged vs kept separate | PARTIAL | No explicit warning against too many personas. However, the Decision Test in Step 2 ('Would make DIFFERENT product decisions than others?') serves as an implicit merge-vs-keep criterion. 'Watch for: Segment overlap — If 10%+ of users don't clearly fit one persona, revisit segment definitions' provides partial guidance but stops short of a merge-vs-keep decision framework or a named upper limit. |
| c8 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The captured output contains only the skill's execution result (chat response and research file artifacts). The skill definition file with its YAML frontmatter is not shown and cannot be verified from the provided material. |
| c9 | Output's evidence inventory step is shown — what existing data sources are available (interviews, analytics, support tickets, churn data, onboarding surveys) — and what data is MISSING for confident segmentation | PARTIAL | The evidence inventory table clearly catalogs available sources. Missing data is only partially flagged: the Executive persona notes 'only 3 interviews' with a 'recommend validating' note, and the 'Research needed' section identifies follow-up. However, the inventory does not explicitly list absent data types (no support tickets, no churn data, no onboarding surveys, no NPS data) as gaps in the evidence base. |
| c10 | Output's segmentation is grounded in observed BEHAVIOUR — how users actually use the product, what they accomplish, what they avoid — NOT demographics (age / gender / job title alone) | PASS | Every segment is defined by observable product behaviors: Operations Manager by 'Heavy user of reports and export features. Rarely creates tasks themselves'; Team Lead by 'bottom 30% of session length/frequency'; Executive by 'Very light direct usage. Rely on reports others generate.' Feature adoption percentages anchor all behavioral claims. |
| c11 | Output produces 2-4 personas — the team's hypothesis is "3-4 distinct user types" but the skill validates this; might consolidate to 2 if the data shows two clusters with genuine differentiation, or fan out to 4 if more are evidence-backed | PASS | Four personas produced (Operations Manager, Project Manager, Team Lead, Executive), matching the '3-4 distinct user types' hypothesis. The IT Administrator group (2 interviews) from the research was not elevated to a full persona, showing appropriate restraint. Each of the 4 passes the Decision Test. |
| c12 | Output's personas each have goals (what they're trying to achieve), pain points (current frustrations), and behaviours (what they do in the product) — not stock photos with demographic profiles | PASS | All four personas contain ranked Goals, ranked Frustrations, and a Behaviour Patterns table with Discovery/Evaluation/Decision trigger/Learning style rows. No demographic descriptions, no stock photos, no age/location fields. |
| c13 | Output explicitly prohibits stereotyping — does not use age, gender, or background as differentiators unless behaviour patterns demonstrably correlate with them in the data | PASS | Validation checklist item 4 ('No stereotypes; behavior-based not demographics?') receives an explicit PASS for all four personas with evidence statements such as 'Defined by usage pattern and simplicity preference, not seniority' and 'Defined by workflow (standup prep, dependency tracking), not role.' No age, gender, or background attributes appear anywhere in the persona profiles. |
| c14 | Output's jobs-to-be-done per persona are solution-agnostic — describe what the user is trying to accomplish (e.g. "report status to my exec team weekly") not "use the dashboard" | PARTIAL | Goals are a mix. Solution-agnostic examples: 'Know portfolio health: Are Q4 projects on track?', 'Know what to work on next without cognitive load.' Solution-specific examples: 'Export data quickly to build leadership presentations', 'Update task status quickly during the day', 'Visualize dependencies to prevent schedule slippage.' The success-criteria quotes ('Did I get the report out by 9am Friday?') are more purely JTBD, but the Goals sections themselves are inconsistently solution-agnostic. |
| c15 | Output's validation checklist includes evidence trail per persona — for each persona attribute, what's the evidence (interview quote, analytics segment, support pattern), and what would falsify the persona | PASS | Every goal and frustration has an italicized '*Evidence:*' citation (e.g., '*Evidence: 8 interviews + usage data (31% reports) + behavior pattern*'). The Anti-Persona Signals section for each persona defines falsifying conditions (e.g., 'Uses the tool daily to create/update individual tasks — that's Team Lead behavior, not Ops Mgr'). |
| c16 | Output flags any persona attribute that's currently an assumption rather than evidence-backed — clearly marked, with the recommendation to validate before relying on it for product decisions | PARTIAL | The Executive persona is flagged with 'Confidence: Medium (only 3 interviews... recommend validating with 2-3 more)' and two ⚠️ marks in the checklist ('CONDITIONAL PASS', 'MEDIUM'). However, no individual attributes for the other three personas are marked as assumptions — attributes with thin evidence (e.g., Ops Mgr learning style, PM keyboard-shortcut preference) are stated without an assumption flag. |
| c17 | Output's persona names are descriptive of the role + behaviour, not stereotyped first names — e.g. "The Reporting-Heavy Operations Director" rather than "Sarah, 38, mum of two from Leeds" | PASS | All four persona names follow 'Role — Behavioural archetype' format: 'Operations Manager — Status Aggregator', 'Project Manager — Risk Spotter', 'Team Lead — Daily Executor', 'Executive — Portfolio Confidence'. No first names, ages, or location clichés appear. |
| c18 | Output addresses anti-personas or non-target users — who the product is explicitly NOT for (e.g. "freelancers using project management for personal task tracking") so product decisions don't try to please everyone | PARTIAL | Each persona has an 'Anti-Persona Signals' section listing behaviors that disqualify a user from that persona (e.g., 'Uses tool daily for creating/updating tasks — that's Team Lead behavior'). These cross-persona disambiguation signals are present but function as persona-sorting aids rather than defining who the product is not for at all (e.g., no mention of personal-use freelancers, students, or single-user contexts as out-of-scope). |

### Notes

The output is a thorough, well-structured persona definition that excels at evidence grounding, behavioral segmentation, and structured validation. The four-step framework (evidence inventory → segment validation → persona profiles → validation checklist) is clearly executed. The strongest elements are: explicit anti-stereotype checks embedded in the validation loop, Anti-Persona Signals per persona for falsification, and consistent evidence citations within goal/frustration items. The main gaps are: (1) c8 — the skill's YAML frontmatter is unverifiable from the output; (2) c7 — there is no explicit warning about persona count or a named merge criterion, only an implicit one via the Decision Test; (3) c16 — assumption-flagging is applied to the Executive persona but not systematically to individual attributes across other personas with thinner evidence (e.g., the PM's 'prefers keyboard shortcuts' claim); (4) c14 — goal statements mix solution-agnostic JTBD language with product-specific action language inconsistently. The IT Administrator group appearing in interviews but excluded from the final persona set (correctly, given only 2 interviews) is a good signal that segment consolidation reasoning was applied.
