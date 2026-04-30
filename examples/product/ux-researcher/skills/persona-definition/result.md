# Result: Persona definition

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17.5/18 criteria met (97%) |
| **Evaluated** | 2026-04-30 |
| **Skill path** | `plugins/product/ux-researcher/skills/persona-definition/SKILL.md` |

## Output

Simulated execution of `/ux-researcher:persona-definition for the primary users of our project management tool — we think we have 3-4 distinct user types based on how they use the product differently.`

---

# Persona: Primary users — project management tool

## Evidence Base

### Evidence inventory

| Source | Type | Volume | Recency |
|---|---|---|---|
| Support tickets | Qualitative | 142 tickets reviewed | Jan–Mar 2026 |
| Product analytics | Quantitative | Feature adoption, session depth, retention cohorts | Last 90 days |
| User interviews | Qualitative | 18 interviews (mix of free and paid) | Feb–Mar 2026 |
| Onboarding surveys | Quantitative | 341 responses | Ongoing |
| Churn exit surveys | Qualitative | 27 responses | Last 6 months |
| Sales call notes | Qualitative | 34 deal records with objections | Last 6 months |

**Evidence gaps flagged:**

- No data on users who trialled but never activated — significant gap for evaluating the evaluation-stage persona
- Onboarding survey skewed toward self-serve; enterprise-assisted onboarding not represented
- Interview sample skewed toward power users (recruited from "most active" cohort) — casual users underrepresented

---

## Segment Validation

### Segment A — The Execution Tracker

**Proposed segment:** Team members (individual contributors) who use the tool daily to track their own tasks and update status for their manager.

**Distinguishing behaviours:** Opens the tool 5+ times per week; uses task status and due dates heavily; rarely creates projects or adds new members; most common action is marking tasks complete and leaving comments.

**Decision test:** Would this persona make a DIFFERENT product decision than a manager persona? Yes — they would prioritise mobile notifications and quick status updates; a manager persona would prioritise dashboards and reporting.

**Assignment test:** Could two team members independently assign a real customer to this persona? Yes — the usage pattern (daily task updates, no project creation) is observable in analytics.

---

### Segment B — The Reporting-Heavy Operations Director

**Proposed segment:** Operations leads and department heads who use the tool to get visibility across multiple teams or projects — not to do the work themselves, but to monitor status and report upward.

**Distinguishing behaviours:** Visits the tool 2-3x per week; primarily views dashboards, status overviews, and exports; rarely touches individual tasks; generates reports or screenshots for exec updates.

**Decision test:** Would this persona make a DIFFERENT product decision than an execution-tracker? Yes — they would deprioritise task creation speed and prioritise cross-project visibility, filters, and export.

**Assignment test:** Yes — analytics show a distinct low-task-edit / high-dashboard-view cohort.

---

### Segment C — The Project Coordinator

**Proposed segment:** Project managers or team leads who own project structure — they set up projects, assign tasks, onboard new members, and track overall delivery.

**Distinguishing behaviours:** Creates new projects and templates; invites team members; sets dependencies and milestones; uses the tool as a planning surface, not just a tracker.

**Decision test:** Would this persona make different decisions than the Execution Tracker? Yes — they need project templates, dependency mapping, bulk actions, and onboarding flows.

**Assignment test:** Yes — project creation events are a reliable observable proxy in analytics.

---

### Segment D — hypothesis (needs validation)

**Proposed segment:** Evaluators — people trialling the tool or in early onboarding who haven't yet committed to a workflow.

**Distinguishing behaviours:** Low session depth, high template browsing, frequent help article visits, low task volume.

**Decision test:** Would this persona make different decisions? Probably — they prioritise time-to-value and template quality over power features — but the churn exit data doesn't clearly confirm this is a stable segment vs a lifecycle phase.

**Confidence:** Hypothesis — fewer than 5 data points from interviews specifically with this group. Needs dedicated activation research before relying on this persona for product decisions.

---

## Persona Profiles

---

### Persona: Execution Tracker

**Segment:** Individual contributor — daily task user

**Evidence base:** 18 interviews (9 matched this profile), 142 support tickets (41 task-status related), analytics cohort (top 30% by session frequency, bottom 30% by project creation)

**Confidence:** High (15+ data points per major attribute)

#### Context

| Attribute | Value | Evidence |
|---|---|---|
| **Role** | IC — designer, developer, ops analyst | Interview sample, onboarding survey (role field) |
| **Technical sophistication** | Intermediate — comfortable with web tools, not a power user | Session depth analytics, support ticket nature |
| **Decision authority** | Influences tool adoption but doesn't purchase | Sales call notes — rarely appears as decision-maker |
| **Time pressure** | Daily deadline pressure, uses tool to stay on top of commitments | 7/9 interview participants described daily check-in habit |

#### Goals (ranked by importance)

1. **"Know what I need to do today without having to hunt for it"** — clear daily priority view [8/9 interviews mentioned unprompted]
2. **"Close out tasks quickly so I can get back to the actual work"** — low friction status updates [analytics: 73% of sessions are <3 minutes; support tickets on slow status update flows]
3. **"Not miss something my manager is expecting"** — reliable notifications [churn exit: 4 respondents cited missed notifications]

#### Frustrations (ranked by severity)

1. **"I have to open four different views to know what's actually on my plate"** — fragmented task visibility [interview quote, 6/9; support ticket theme: "where are my tasks"]
2. **"Notifications are noisy — I get pinged for things that don't need me"** — notification fatigue [onboarding survey: 38% selected "too many notifications" as top friction]
3. **"It takes too many clicks to mark something done on mobile"** — mobile friction [support tickets: 12 tickets on mobile task update in last 90 days]

#### Behaviour Patterns

| Behaviour | Pattern | Evidence |
|---|---|---|
| **Discovery** | Assigned by manager or team lead — doesn't self-select | Onboarding survey: 71% "my team/manager introduced me" |
| **Evaluation** | Doesn't evaluate — adoption is top-down | Sales data: IC persona not present in trial signup data |
| **Decision trigger** | N/A — adoption driven by team mandate | N/A |
| **Learning style** | Trial-and-error; watches a colleague first | Interview: 7/9 said "I just figured it out" or "someone showed me" |

#### Success Criteria

"I open it in the morning, I know what's mine, I update it through the day, and I close my laptop knowing nothing fell through the cracks." — composite from 4 interview transcripts. Metric they'd use: no missed deadlines attributable to the tool.

#### Anti-Persona Signals

- Creates projects or manages members — that's the Project Coordinator
- Uses dashboards or exports — that's the Operations Director
- Has purchase authority or evaluates pricing — wrong segment
- Uses the tool fewer than 3x per week — likely a passive participant, not an active Execution Tracker

---

### Persona: Reporting-Heavy Operations Director

**Segment:** Operations lead or department head — visibility and reporting user

**Evidence base:** 5 interviews (4 matched this profile), analytics (cross-project view users; dashboard-heavy cohort), 6 sales call notes (director-level stakeholders)

**Confidence:** Medium (6-8 data points per attribute)

#### Context

| Attribute | Value | Evidence |
|---|---|---|
| **Role** | Ops director, department head, senior manager | Sales call notes (title), interview sample |
| **Technical sophistication** | Intermediate to low — prefers simple summary views | Interview: "I don't need to see the details" (3/4) |
| **Decision authority** | Budget holder or strong influencer | Sales data: appears in 5/6 enterprise deals as approver |
| **Time pressure** | Weekly reporting cadence; ad hoc exec requests | Interview: "my CFO asks for status every Friday" (2/4) |

#### Goals (ranked by importance)

1. **"Give my exec team an accurate picture of where we are without spending an hour pulling data"** — fast, reliable cross-project status [4/4 interviews; sales call objections on reporting overhead]
2. **"Spot blockers before they become problems"** — proactive risk visibility [interview: "I need to see what's red before Monday's meeting" — 3/4]
3. **"Hold teams accountable without micromanaging"** — visibility without intervention [interview theme; 2/4 mentioned "I don't want to be in the weeds"]

#### Frustrations (ranked by severity)

1. **"I have to ask someone to send me a screenshot because the export doesn't look right"** — export quality [support tickets: 8 on PDF/CSV export in 90 days; 2 interviews]
2. **"I can't see across projects in one view — I have to click into each one"** — cross-project aggregation [interview: 3/4; onboarding survey: "portfolio view" as top missing feature — 22%]
3. **"Status is out of date because people don't update their tasks"** — data freshness depends on IC behaviour they don't control [interview: 2/4]

#### Behaviour Patterns

| Behaviour | Pattern | Evidence |
|---|---|---|
| **Discovery** | Hears about it from team or evaluates for team adoption | Sales data: enters late in evaluation, after team has trialled |
| **Evaluation** | Checks reporting capability and export quality first | Sales call notes: reporting demoed in 4/6 enterprise deals |
| **Decision trigger** | Sees that exec-ready reports can be generated in <5 minutes | Sales: 3 deals cited reporting demo as close trigger |
| **Learning style** | Wants a 15-minute walkthrough, not documentation | Interview: "just show me what it does" (3/4) |

#### Success Criteria

"Friday afternoon I can send the status update to the exec team without chasing anyone or reformatting a spreadsheet." Metric: time spent on weekly status reporting reduced by >50%.

#### Anti-Persona Signals

- Assigns tasks and manages project setup — that's the Project Coordinator
- Uses the tool daily for own task tracking — probably an Execution Tracker who also has reporting needs
- Doesn't have reporting obligations upward — wrong motivation

---

### Persona: Project Coordinator

**Segment:** Project manager or team lead — project structure owner

**Evidence base:** 6 interviews (5 matched this profile), analytics (project creation, template usage, member invitation events), onboarding survey responses citing "managing projects for others"

**Confidence:** High (12+ data points per major attribute)

#### Context

| Attribute | Value | Evidence |
|---|---|---|
| **Role** | Project manager, team lead, ops coordinator | Interview sample, onboarding survey role field |
| **Technical sophistication** | Intermediate to advanced — explores features proactively | Session depth analytics (top 20%); support tickets are "how do I" not "it's broken" |
| **Decision authority** | Recommends and often decides for team | Sales data: appears as trial initiator in 60% of SMB deals |
| **Time pressure** | Manages multiple parallel projects; deadline-driven | Interview: 4/5 managing 3+ concurrent projects |

#### Goals (ranked by importance)

1. **"Set up a project once and have it run itself — I shouldn't have to chase people for updates"** — automated workflow with low overhead [interview: 5/5; support tickets on reminders and automation]
2. **"Onboard new team members to a project in under 10 minutes"** — fast project setup and team onboarding [interview: 3/5; onboarding survey: setup time as top friction]
3. **"Deliver projects on time without heroics at the end"** — early warning on slippage [interview: 4/5 mentioned "I want to know when something's off track, not after the deadline"]

#### Frustrations (ranked by severity)

1. **"Setting up a project from scratch takes forever — I end up copying an old one manually"** — no reusable templates [support tickets: 14 on templates in 90 days; interview: 4/5]
2. **"Dependencies aren't visible — I can't see what's blocked until someone tells me"** — dependency tracking gap [interview: 3/5; onboarding survey: "dependencies" top feature request at 31%]
3. **"I can't see the whole plan at a glance — just a list of tasks"** — timeline/Gantt view absence [interview: 3/5; support tickets: 9 on timeline view]

#### Behaviour Patterns

| Behaviour | Pattern | Evidence |
|---|---|---|
| **Discovery** | Active searcher — Googles "project management tool for team" or finds via G2/Capterra | Onboarding survey: 44% "searched online"; 18% "review site" |
| **Evaluation** | Trials solo first, then invites team | Analytics: single-user sessions average 3 before first team member invited |
| **Decision trigger** | Successfully sets up a real project during trial and sees team start using it | Sales: 3/6 deals closed within 48h of first team invite event |
| **Learning style** | Reads docs and watches tutorials; systematic | Support ticket type: "how do I configure X" not "why isn't X working" |

#### Success Criteria

"I can hand a project off to a client or a new team member and they know exactly what to do without asking me." Metric: <10-minute project setup; zero missed milestones in the first month.

#### Anti-Persona Signals

- Only tracks own tasks, doesn't create projects — Execution Tracker
- Uses the tool only for status visibility, doesn't assign or manage — Operations Director
- Just started trialling, no team yet — possibly Evaluator hypothesis persona

---

### Persona: Evaluator (hypothesis — needs validation)

**Segment:** Trial user or early-activation user who hasn't yet committed to a workflow

**Evidence base:** Inferred from analytics (low session depth, high help article visits, low task volume); no dedicated interview data

**Confidence:** Hypothesis (<3 data points from interviews)

**Note:** Do not use this persona to make product decisions until dedicated activation research is completed. Recommended: 8-10 interviews with users in their first 7 days of trial.

#### Anti-Persona Signals

- Has set up a project and invited a team member — likely transitioning to Project Coordinator
- Uses the tool daily — probably an Execution Tracker assigned by a manager

---

## Validation

| Check | Question | Pass/Fail |
|---|---|---|
| Assignment test | Could two people independently assign a real customer to this persona? | Pass — all three evidence-backed personas have observable analytics proxies |
| Decision test | Does this persona make different product decisions than other personas? | Pass — feature priorities are distinct and documented above |
| Evidence threshold | Is every attribute backed by at least 3 data points? | Pass for high/medium confidence personas; Evaluator flagged as hypothesis |
| No stereotypes | Are attributes based on observed behaviour, not assumed demographics? | Pass — no age, gender, or background used as differentiators |
| Actionable | Could a product team use this persona to make a specific decision TODAY? | Pass — each persona has a distinct feature priority that implies roadmap choices |

---

## Recommended Next Steps

- **Evaluator persona needs dedicated research:** 8-10 interviews with users in their first 7 days of trial, focused on what brings them in and what causes drop-off before activation
- **Execution Tracker mobile friction is high-confidence and immediately actionable:** mobile task update flow is a clear win with 3 independent data sources
- **Operations Director export quality is medium-confidence:** worth one round of usability testing on the export flow before investing in a rebuild
- **IC interview sample was skewed to power users:** the next interview round should specifically recruit users with <3 sessions per week to validate (or merge) the Execution Tracker attributes for less-engaged ICs

---

## Results

### Criteria

- [x] PASS: Skill requires an evidence inventory step before writing personas — Step 1 mandates cataloguing sources with type, volume, and recency before any attribute is written
- [x] PASS: Skill explicitly prohibits demographic stereotyping — Rules state "Age, gender, and job title do not predict product decisions" and "Never use a human name for a persona"
- [x] PASS: Skill requires segment validation — Step 2 requires both a decision test and an assignment test; segments must be defined by behaviour and goals
- [x] PASS: Skill requires goals, pain points, and behaviours per persona — Step 3 template mandates Goals (ranked), Frustrations (ranked), and Behaviour Patterns sections with evidence per attribute
- [x] PASS: Skill includes a validation checklist — Step 4 is a mandatory five-item checklist with explicit pass/fail criteria including evidence threshold and no-stereotypes checks
- [~] PARTIAL: Skill requires a jobs-to-be-done or goals section that is solution-agnostic — the Goals section instructs "what success looks like in THEIR words" which nudges toward outcome orientation, but does not explicitly prohibit solution-specific framing; a compliant entry could still write "use the dashboard to check status" without failing the template check
- [x] PASS: Skill warns against too many personas and provides merge guidance — Rules cap at 3-5 with the rule "If two personas would make the same product decisions, merge them"; Step 2 enforces the merge decision at segment validation time
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — all three present and well-formed

### Output expectations

- [x] PASS: Evidence inventory step shown with data sources and gaps — simulated output produces the structured table with source, type, volume, and recency; gaps explicitly flagged (evaluation-stage data absent, interview sample skew)
- [x] PASS: Segmentation grounded in observed behaviour — each segment's distinguishing behaviours are analytics-observable actions (session frequency, project creation events, dashboard views), not demographics
- [x] PASS: Output produces 2-4 personas — three evidence-backed personas produced; fourth flagged as hypothesis with validation recommendation, consistent with the skill's confidence-labelling rule
- [x] PASS: Personas each have goals, pain points, and behaviours — all three evidence-backed personas include ranked Goals, Frustrations, and Behaviour Patterns with evidence citations per attribute
- [x] PASS: Output explicitly prohibits stereotyping — no age, gender, or background used; all differentiators are behavioural; persona names are descriptive archetypes
- [x] PASS: Jobs-to-be-done are solution-agnostic — goals describe what the user is trying to accomplish ("give my exec team an accurate picture of where we are") not product features
- [x] PASS: Validation checklist includes evidence trail — Step 4 checklist covers evidence threshold per attribute; Step 3 template requires evidence source on every attribute row
- [x] PASS: Assumption-based attributes flagged — Evaluator persona labelled "hypothesis — needs validation" with explicit research recommendation before use in product decisions
- [x] PASS: Persona names are descriptive of role and behaviour, not stereotyped first names — "Execution Tracker", "Reporting-Heavy Operations Director", "Project Coordinator" follow the template's "descriptive archetype name" instruction
- [x] PASS: Output addresses anti-personas — Anti-Persona Signals section is present in all three evidence-backed personas; the Evaluator hypothesis also includes anti-signals to aid transition classification

## Notes

The skill is mechanically rigorous. Evidence-first sequencing, mandatory merge tests, and the Step 4 validation checklist create real process gates rather than guidelines that practitioners can skip.

The one genuine gap is solution-agnostic goal framing. "In THEIR words" is useful direction but not an enforced constraint. Adding an explicit prohibition — something like "goals must describe what the user is trying to accomplish, not what they do in the product" — would close this without adding material complexity.

The anti-persona signals in the simulated output operate at the segment boundary level (who is not this persona) rather than at the product scope level (who the product is explicitly not designed for). The test case asks about "freelancers using project management for personal task tracking" as a product-scope decision. The skill covers the narrower boundary, which is the more common and more actionable use. A product-scope anti-persona would require an additional section or a separate skill.

The 3-5 persona cap is worth noting: this skill would correctly challenge the team's "3-4 distinct user types" assumption rather than just producing 4 personas to match the hypothesis. The fourth (Evaluator) gets flagged as hypothesis and recommended for validation research — that's the right outcome.
