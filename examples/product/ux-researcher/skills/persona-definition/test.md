# Test: Persona definition

Scenario: Testing whether the persona-definition skill requires evidence-based personas with validated segments, and explicitly prohibits demographic stereotyping.

## Prompt

First, create the research data:

```bash
mkdir -p research
```

Write to `research/interview-synthesis.md`:

```markdown
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

Write to `research/usage-analytics-summary.md`:

```markdown
# Product Usage Analytics Summary — Last 90 Days

### Feature usage by session (% of sessions where feature was used)
- Tasks (create/update): 78%
- Projects (view): 95%
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

Then run:

/ux-researcher:persona-definition for the primary users of our project management tool — we think we have 3-4 distinct user types based on how they use the product differently.

## Criteria


- [ ] PASS: Skill requires an evidence inventory step before writing personas — existing research, analytics, interviews, or support data must be catalogued first
- [ ] PASS: Skill explicitly prohibits basing personas on demographic stereotypes — age, gender, and background are not valid differentiators unless backed by evidence
- [ ] PASS: Skill requires segment validation — each persona must be supported by a meaningful cluster of real user behaviour, not just intuition
- [ ] PASS: Skill requires each persona to describe goals, pain points, and behaviours — not just a demographic profile with a stock photo description
- [ ] PASS: Skill includes a validation checklist to verify personas are grounded in evidence, not assumptions
- [ ] PARTIAL: Skill requires a jobs-to-be-done or goals section per persona that is solution-agnostic — partial credit if goals are required but they could be solution-specific
- [ ] PASS: Skill warns against creating too many personas — and provides guidance on when sub-segments should be merged vs kept separate
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output's evidence inventory step is shown — what existing data sources are available (interviews, analytics, support tickets, churn data, onboarding surveys) — and what data is MISSING for confident segmentation
- [ ] PASS: Output's segmentation is grounded in observed BEHAVIOUR — how users actually use the product, what they accomplish, what they avoid — NOT demographics (age / gender / job title alone)
- [ ] PASS: Output produces 2-4 personas — the team's hypothesis is "3-4 distinct user types" but the skill validates this; might consolidate to 2 if the data shows two clusters with genuine differentiation, or fan out to 4 if more are evidence-backed
- [ ] PASS: Output's personas each have goals (what they're trying to achieve), pain points (current frustrations), and behaviours (what they do in the product) — not stock photos with demographic profiles
- [ ] PASS: Output explicitly prohibits stereotyping — does not use age, gender, or background as differentiators unless behaviour patterns demonstrably correlate with them in the data
- [ ] PASS: Output's jobs-to-be-done per persona are solution-agnostic — describe what the user is trying to accomplish (e.g. "report status to my exec team weekly") not "use the dashboard"
- [ ] PASS: Output's validation checklist includes evidence trail per persona — for each persona attribute, what's the evidence (interview quote, analytics segment, support pattern), and what would falsify the persona
- [ ] PASS: Output flags any persona attribute that's currently an assumption rather than evidence-backed — clearly marked, with the recommendation to validate before relying on it for product decisions
- [ ] PASS: Output's persona names are descriptive of the role + behaviour, not stereotyped first names — e.g. "The Reporting-Heavy Operations Director" rather than "Sarah, 38, mum of two from Leeds"
- [ ] PARTIAL: Output addresses anti-personas or non-target users — who the product is explicitly NOT for (e.g. "freelancers using project management for personal task tracking") so product decisions don't try to please everyone
