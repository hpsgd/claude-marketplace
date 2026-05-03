# Test: Feedback synthesis

Scenario: Testing whether the feedback-synthesis skill uses user language for themes, applies the Impact scoring formula, and produces prioritised recommendations rather than a raw catalogue.

## Prompt

First, create the feedback data files:

```bash
mkdir -p feedback
```

Write to `feedback/support-tickets.csv`:

```csv
id,date,segment,category,raw_quote
T001,2024-10-03,enterprise,usability,"The dashboard takes forever to load. We have 800 projects and it just spins."
T002,2024-10-04,free,feature_request,"Can you add a bulk edit option? Updating projects one by one is painful."
T003,2024-10-05,pro,bug,"Export button doesn't work on Chrome. I get a blank page."
T004,2024-10-06,enterprise,usability,"I can't find the reports section. Took me 20 minutes to figure out it was under Analytics."
T005,2024-10-07,pro,bug,"Export button is broken again. This is the third time this month."
T006,2024-10-08,enterprise,complaint,"Performance is getting worse every month. Our team is considering switching."
T007,2024-10-09,free,feature_request,"I wish I could share a project as a read-only link without giving someone an account."
T008,2024-10-10,enterprise,usability,"Dashboard load is painfully slow for us. We have 1200 projects. Takes 8 seconds."
T009,2024-10-11,pro,bug,"Export fails silently. No error, no file. Just nothing happens."
T010,2024-10-14,enterprise,feature_request,"We need an executive summary view. Our CEO wants to see all project statuses in one place."
T011,2024-10-15,free,question,"How do I archive a project? I've looked everywhere."
T012,2024-10-16,pro,usability,"The search is almost useless. Searching for a project by name gives me 50 results I don't want."
T013,2024-10-17,enterprise,complaint,"Why did the dashboard suddenly get slower? It used to be fine."
T014,2024-10-18,pro,bug,"Export creates a corrupted CSV when project names have commas in them."
T015,2024-10-19,enterprise,feature_request,"We desperately need multi-user workspaces. Our team of 30 can't work on the same project."
T016,2024-10-21,free,praise,"Love the new task view! Makes it so much easier to see what's due."
T017,2024-10-22,enterprise,usability,"Every time I switch between projects I lose my scroll position. So annoying."
T018,2024-10-23,pro,feature_request,"Please add keyboard shortcuts. Power users like me need to move fast."
T019,2024-10-24,enterprise,complaint,"The dashboard performance problem is making our weekly team meetings painful. We spend 5 minutes waiting for it to load."
T020,2024-10-25,free,question,"Is there a way to connect this to Zapier? I want to trigger actions from other tools."
T021,2024-10-28,pro,bug,"Export button worked once then stopped. Cleared cache, still broken."
T022,2024-10-29,enterprise,feature_request,"We need workspace-level roles. Right now everyone can see everything."
T023,2024-10-30,pro,usability,"Search doesn't filter by status. I only want to see active projects."
T024,2024-11-01,enterprise,complaint,"I am seriously considering leaving. The slow dashboard makes the product unusable for us."
T025,2024-11-04,free,feature_request,"Dark mode please!"
T026,2024-11-05,pro,bug,"Export button is completely broken for me. Has been for 2 weeks."
T027,2024-11-06,enterprise,usability,"Reports section is buried. We check it daily but have to click through 3 menus."
T028,2024-11-07,free,praise,"Best project tool I've used. The interface is clean and fast."
T029,2024-11-08,enterprise,feature_request,"Need API webhooks so we can sync project status to Salesforce."
T030,2024-11-11,pro,bug,"Export fails with an error for projects with more than 500 tasks."
T031,2024-11-12,enterprise,usability,"Can't load dashboard at all today. 30+ second timeout."
T032,2024-11-13,pro,feature_request,"Would love a Gantt view for timeline planning."
T033,2024-11-14,enterprise,complaint,"Performance has been unacceptable this month. 3 of my team are using a competitor to avoid waiting."
T034,2024-11-15,free,question,"How do I export my data? Can't find the button."
T035,2024-11-18,pro,bug,"Export button missing entirely on mobile view."
T036,2024-11-19,enterprise,feature_request,"Team workspaces are our #1 ask. We're evaluating alternatives."
T037,2024-11-20,pro,usability,"The search returns results in a random order. Alphabetical or recency would be better."
T038,2024-11-21,enterprise,praise,"The executive summary widget we built with the API is great. But wish it was built-in."
T039,2024-11-22,free,feature_request,"Guest access with limited permissions — we want clients to view projects without full access."
T040,2024-11-25,enterprise,complaint,"We had an internal review about the dashboard slowness. It's become a recurring theme."
```

Write to `feedback/nps-responses.csv`:

```csv
id,date,segment,score,comment
N001,2024-10-05,enterprise,4,"Good product but dashboard speed is a real problem for us. Would score higher if that was fixed."
N002,2024-10-07,pro,9,"Really enjoy using it. Export occasionally has issues but generally solid."
N003,2024-10-10,free,7,"It works well. Would love dark mode and keyboard shortcuts."
N004,2024-10-12,enterprise,3,"Performance has degraded noticeably. This is affecting our team's productivity."
N005,2024-10-15,enterprise,5,"Core features are there but team collaboration is missing. We need workspaces."
N006,2024-10-18,pro,8,"Clean UI, good feature set. Search could be better."
N007,2024-10-20,free,10,"Love it! Best project tool I've used for solo work."
N008,2024-10-23,enterprise,2,"Dashboard is too slow for our account size. Considering alternatives."
N009,2024-10-25,pro,7,"Mostly happy. Export has been flaky lately though."
N010,2024-10-28,enterprise,4,"Would be a 9 if the dashboard loaded faster and we had workspace roles."
N011,2024-10-30,free,9,"Super easy to use. Wish there was a mobile app."
N012,2024-11-02,pro,6,"Decent product. The export bug has been there for weeks, needs fixing."
N013,2024-11-05,enterprise,3,"We're actively evaluating alternatives due to performance issues."
N014,2024-11-08,free,8,"Great for personal use. Would recommend."
N015,2024-11-10,enterprise,5,"Team collaboration features are our biggest gap. Also slow dashboard."
N016,2024-11-13,pro,7,"Good tool. Would love Zapier integration and better search."
N017,2024-11-15,enterprise,2,"Performance has gotten progressively worse. Hard to justify the cost."
N018,2024-11-18,free,9,"Very happy with the product. Does everything I need."
N019,2024-11-20,pro,8,"Really good. Export works now which was my main complaint."
N020,2024-11-22,enterprise,4,"Core features solid but enterprise needs (workspaces, SSO, speed) lagging."
```

Then run:

/support:feedback-synthesis from feedback/

## Criteria


- [ ] PASS: Skill themes feedback using user language — themes are named after what users say, not internal product terminology
- [ ] PASS: Skill applies a quantified impact scoring formula — Impact = Severity × Frequency × SegmentWeight — not qualitative judgement alone
- [ ] PASS: Skill tracks trends — whether issues are increasing, stable, or decreasing — not just current volume
- [ ] PASS: Skill produces prioritised recommendations linked to themes, not just a ranked list of complaints
- [ ] PASS: Skill requires an ingest step — reading all feedback before categorising — to enable cross-source pattern detection
- [ ] PASS: Skill distinguishes between different customer segments when quantifying impact — an issue affecting enterprise customers is weighted differently from one affecting free tier users
- [ ] PARTIAL: Skill identifies feedback that indicates churn risk — partial credit if negative sentiment is tracked but churn signal is not explicitly flagged
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output processes both data sources — 340 support tickets AND 89 NPS responses — with cross-source pattern detection (a theme appearing in both is stronger signal than one in isolation)
- [ ] PASS: Output's themes are named in user language — e.g. "I can't find what I'm looking for in the dashboard" — not internal terminology like "navigation IA issues"
- [ ] PASS: Output's impact scoring formula is shown explicitly per theme — `Impact = Severity (1-3) × Frequency (count) × SegmentWeight (1-3)` — with the resulting numeric Impact score, not just "High / Medium / Low"
- [ ] PASS: Output identifies trends per theme — increasing / stable / decreasing — by comparing this quarter's volume vs previous quarter, with the math (e.g. "checkout failures: 23 last quarter, 87 this quarter — 3.8x increase")
- [ ] PASS: Output segments the impact — same volume of tickets from enterprise customers (small N, high ARR) vs free-tier customers (large N, low ARR) yields different priorities; the segment weight is named per theme
- [ ] PASS: Output's recommendations are linked to themes — each top-priority theme has an "if we did X, we'd address this signal" recommendation, not just a list of complaints reformatted as suggestions
- [ ] PASS: Output's churn-risk flagging identifies feedback signals correlated with cancellation — explicit "I'm considering switching" mentions, repeat tickets from the same account, NPS detractors — not just sentiment polarity
- [ ] PASS: Output's prioritisation recommends 3-5 specific actions for the next quarter — not "improve the product" but "fix the top-2 themes (X and Y) which together represent 35% of ticket volume"
- [ ] PASS: Output addresses theme novelty — themes that are new this quarter (didn't appear last quarter) get a "new signal" flag for early attention, even if their volume is currently lower than long-running themes
- [ ] PARTIAL: Output identifies positive feedback themes (what customers love) — synthesis isn't only about pain; positive themes inform what to protect and what to amplify in marketing
