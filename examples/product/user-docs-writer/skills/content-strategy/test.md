# Test: Content strategy

Scenario: Testing whether the content-strategy skill uses the Diataxis framework, requires a content inventory, and produces a prioritised content roadmap.

## Prompt

First, create the help centre content inventory:

```bash
mkdir -p help-centre/analytics
```

Write to `help-centre/inventory.csv`:

```csv
id,title,category,last_updated,views_last_90d,support_tickets_referencing,outdated_flag
1,Getting started with Clearpath,Onboarding,2021-03-10,4200,0,yes
2,Creating your first project,Onboarding,2021-03-10,3800,2,yes
3,Inviting team members,Onboarding,2021-04-05,2100,18,yes
4,Understanding project statuses,Projects,2022-01-20,1800,4,no
5,How to archive a project,Projects,2021-06-15,890,31,yes
6,Bulk project actions,Projects,2023-08-01,450,0,no
7,Creating tasks and subtasks,Tasks,2021-05-01,3100,1,no
8,Assigning tasks to team members,Tasks,2022-02-14,2200,3,no
9,Setting due dates and reminders,Tasks,2021-05-01,1900,2,no
10,Using task dependencies,Tasks,2023-01-10,780,0,no
11,Understanding the dashboard,Dashboard,2020-11-01,5100,44,yes
12,Customising dashboard widgets,Dashboard,2021-09-22,1200,12,yes
13,Dashboard performance troubleshooting,Dashboard,2022-06-01,340,67,yes
14,Using the reports section,Reports,2020-11-01,2800,38,yes
15,Exporting a report to CSV,Reports,2021-02-10,1600,29,yes
16,Scheduling automated reports,Reports,2023-03-15,440,0,no
17,How to export project data,Export,2020-12-01,2900,51,yes
18,Export file formats explained,Export,2021-01-20,800,8,yes
19,Troubleshooting export errors,Export,2022-04-05,1100,72,yes
20,Using the search function,Search,2020-12-01,1700,22,yes
21,Advanced search filters,Search,2023-07-01,380,0,no
22,Setting up your account,Account,2021-01-15,2100,5,no
23,Managing billing and plans,Billing,2021-03-01,1400,9,yes
24,API authentication guide,API,2022-05-01,980,3,no
25,API rate limits,API,2022-05-01,560,1,no
26,Webhook setup guide,Integrations,2023-11-01,420,0,no
27,Zapier integration,Integrations,2021-08-10,310,14,yes
28,Salesforce integration,Integrations,2024-01-15,290,2,no
29,Two-factor authentication setup,Security,2023-04-01,680,0,no
30,Managing user permissions,Security,2021-07-01,1200,16,yes
31,Understanding notification settings,Notifications,2021-02-20,900,21,yes
32,Email notification troubleshooting,Notifications,2021-02-20,650,18,yes
33,Mobile app getting started,Mobile,2022-09-01,720,8,yes
34,Keyboard shortcuts reference,Productivity,2023-05-01,540,0,no
35,Project templates guide,Templates,2023-10-01,310,0,no
36,Importing projects from spreadsheet,Import,2022-01-01,880,33,yes
37,CSV import format requirements,Import,2022-01-01,640,27,yes
38,Troubleshooting CSV import errors,Import,2022-06-01,420,41,yes
39,Dark mode setup,Accessibility,2024-02-01,210,0,no
40,Accessibility features overview,Accessibility,2023-01-01,180,0,no
```

Write to `help-centre/analytics/top-search-queries.csv`:

```csv
query,searches_last_90d,results_found,tickets_created_after_search
how to export,1840,yes,203
dashboard slow,1620,no,891
archive project,1180,yes,312
find reports,980,no,441
bulk edit,870,no,290
invite user,760,yes,45
export not working,680,no,512
change project status,640,yes,22
delete project,590,yes,18
api token,480,yes,12
```

Then run:

/user-docs-writer:content-strategy for our help centre — we have 140 articles written over 3 years, significant product changes since most were written, and support tickets suggesting users can't find answers to common questions.

## Criteria


- [ ] PASS: Skill uses the Diataxis framework — classifying content as Tutorial, How-to, Reference, or Explanation — not an ad-hoc taxonomy
- [ ] PASS: Skill requires a content inventory step before any recommendations — auditing what exists before deciding what to create
- [ ] PASS: Skill produces a gap analysis — identifying what content types are missing or underrepresented for each product area
- [ ] PASS: Skill produces a prioritised content roadmap — what to create first, with rationale based on user impact
- [ ] PASS: Skill defines content standards — what good looks like for each content type in this context
- [ ] PASS: Skill requires a coverage matrix — mapping content to user tasks to identify blind spots
- [ ] PARTIAL: Skill addresses content maintenance — how to keep existing content current as the product evolves — partial credit if this is mentioned but not required as a strategy component
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output's content inventory step processes the 140 existing articles — at minimum classifying each into one of the four Diataxis types and flagging stale articles (last reviewed > 6 months without product change) — not a sample
- [ ] PASS: Output uses the Diataxis taxonomy explicitly — Tutorial (learning-oriented), How-to (task-oriented), Reference (information-oriented), Explanation (understanding-oriented) — with the framework named, not invented categories
- [ ] PASS: Output's gap analysis identifies what's missing per product area — e.g. "Reporting has 8 How-tos but 0 Tutorials, suggesting new users have nowhere to start" — concrete, not generic "we need more content"
- [ ] PASS: Output's coverage matrix maps content to user tasks — rows are user tasks ("export a report", "invite a teammate"), columns are Diataxis types — with cells showing the article(s) that cover each, blanks revealing gaps
- [ ] PASS: Output addresses the support-ticket signal — common questions where users couldn't find answers should be cross-referenced with the inventory to identify content that exists but isn't findable, vs content that's genuinely missing
- [ ] PASS: Output's roadmap is prioritised — with the top items being either (a) high-frequency support deflection wins or (b) gaps blocking key user tasks — not arbitrary "let's update the docs"
- [ ] PASS: Output's content standards define what GOOD looks like per Diataxis type — e.g. "How-tos must have numbered steps with expected results", "Reference must be exhaustive and machine-scannable" — actionable for writers
- [ ] PASS: Output's recommendations distinguish between rewrite (article exists but is stale or wrong type), retire (no longer relevant), and create (genuine gap) — and the inventory feeds these decisions
- [ ] PASS: Output addresses content maintenance as a strategic component — review cadence (e.g. every 6 months), trigger-based update (after a product release in the same area), and content owner per article
- [ ] PARTIAL: Output addresses the IA / findability dimension — even good content fails if users can't find it; recommendations on search, navigation hierarchy, and tagging belong in the strategy
