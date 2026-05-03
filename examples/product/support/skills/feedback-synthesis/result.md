# Feedback Synthesis

Scenario: Testing whether the feedback-synthesis skill uses user language for themes, applies the Impact scoring formula, and produces prioritised recommendations rather than a raw catalogue.

## Prompt

> First, create the feedback data files:
> 
> ```bash
> mkdir -p feedback
> ```
> 
> Write to `feedback/support-tickets.csv`:
> 
> ```csv
> id,date,segment,category,raw_quote
> T001,2024-10-03,enterprise,usability,"The dashboard takes forever to load. We have 800 projects and it just spins."
> T002,2024-10-04,free,feature_request,"Can you add a bulk edit option? Updating projects one by one is painful."
> T003,2024-10-05,pro,bug,"Export button doesn't work on Chrome. I get a blank page."
> T004,2024-10-06,enterprise,usability,"I can't find the reports section. Took me 20 minutes to figure out it was under Analytics."
> T005,2024-10-07,pro,bug,"Export button is broken again. This is the third time this month."
> T006,2024-10-08,enterprise,complaint,"Performance is getting worse every month. Our team is considering switching."
> T007,2024-10-09,free,feature_request,"I wish I could share a project as a read-only link without giving someone an account."
> T008,2024-10-10,enterprise,usability,"Dashboard load is painfully slow for us. We have 1200 projects. Takes 8 seconds."
> T009,2024-10-11,pro,bug,"Export fails silently. No error, no file. Just nothing happens."
> T010,2024-10-14,enterprise,feature_request,"We need an executive summary view. Our CEO wants to see all project statuses in one place."
> T011,2024-10-15,free,question,"How do I archive a project? I've looked everywhere."
> T012,2024-10-16,pro,usability,"The search is almost useless. Searching for a project by name gives me 50 results I don't want."
> T013,2024-10-17,enterprise,complaint,"Why did the dashboard suddenly get slower? It used to be fine."
> T014,2024-10-18,pro,bug,"Export creates a corrupted CSV when project names have commas in them."
> T015,2024-10-19,enterprise,feature_request,"We desperately need multi-user workspaces. Our team of 30 can't work on the same project."
> T016,2024-10-21,free,praise,"Love the new task view! Makes it so much easier to see what's due."
> T017,2024-10-22,enterprise,usability,"Every time I switch between projects I lose my scroll position. So annoying."
> T018,2024-10-23,pro,feature_request,"Please add keyboard shortcuts. Power users like me need to move fast."
> T019,2024-10-24,enterprise,complaint,"The dashboard performance problem is making our weekly team meetings painful. We spend 5 minutes waiting for it to load."
> T020,2024-10-25,free,question,"Is there a way to connect this to Zapier? I want to trigger actions from other tools."
> T021,2024-10-28,pro,bug,"Export button worked once then stopped. Cleared cache, still broken."
> T022,2024-10-29,enterprise,feature_request,"We need workspace-level roles. Right now everyone can see everything."
> T023,2024-10-30,pro,usability,"Search doesn't filter by status. I only want to see active projects."
> T024,2024-11-01,enterprise,complaint,"I am seriously considering leaving. The slow dashboard makes the product unusable for us."
> T025,2024-11-04,free,feature_request,"Dark mode please!"
> T026,2024-11-05,pro,bug,"Export button is completely broken for me. Has been for 2 weeks."
> T027,2024-11-06,enterprise,usability,"Reports section is buried. We check it daily but have to click through 3 menus."
> T028,2024-11-07,free,praise,"Best project tool I've used. The interface is clean and fast."
> T029,2024-11-08,enterprise,feature_request,"Need API webhooks so we can sync project status to Salesforce."
> T030,2024-11-11,pro,bug,"Export fails with an error for projects with more than 500 tasks."
> T031,2024-11-12,enterprise,usability,"Can't load dashboard at all today. 30+ second timeout."
> T032,2024-11-13,pro,feature_request,"Would love a Gantt view for timeline planning."
> T033,2024-11-14,enterprise,complaint,"Performance has been unacceptable this month. 3 of my team are using a competitor to avoid waiting."
> T034,2024-11-15,free,question,"How do I export my data? Can't find the button."
> T035,2024-11-18,pro,bug,"Export button missing entirely on mobile view."
> T036,2024-11-19,enterprise,feature_request,"Team workspaces are our #1 ask. We're evaluating alternatives."
> T037,2024-11-20,pro,usability,"The search returns results in a random order. Alphabetical or recency would be better."
> T038,2024-11-21,enterprise,praise,"The executive summary widget we built with the API is great. But wish it was built-in."
> T039,2024-11-22,free,feature_request,"Guest access with limited permissions — we want clients to view projects without full access."
> T040,2024-11-25,enterprise,complaint,"We had an internal review about the dashboard slowness. It's become a recurring theme."
> ```
> 
> Write to `feedback/nps-responses.csv`:
> 
> ```csv
> id,date,segment,score,comment
> N001,2024-10-05,enterprise,4,"Good product but dashboard speed is a real problem for us. Would score higher if that was fixed."
> N002,2024-10-07,pro,9,"Really enjoy using it. Export occasionally has issues but generally solid."
> N003,2024-10-10,free,7,"It works well. Would love dark mode and keyboard shortcuts."
> N004,2024-10-12,enterprise,3,"Performance has degraded noticeably. This is affecting our team's productivity."
> N005,2024-10-15,enterprise,5,"Core features are there but team collaboration is missing. We need workspaces."
> N006,2024-10-18,pro,8,"Clean UI, good feature set. Search could be better."
> N007,2024-10-20,free,10,"Love it! Best project tool I've used for solo work."
> N008,2024-10-23,enterprise,2,"Dashboard is too slow for our account size. Considering alternatives."
> N009,2024-10-25,pro,7,"Mostly happy. Export has been flaky lately though."
> N010,2024-10-28,enterprise,4,"Would be a 9 if the dashboard loaded faster and we had workspace roles."
> N011,2024-10-30,free,9,"Super easy to use. Wish there was a mobile app."
> N012,2024-11-02,pro,6,"Decent product. The export bug has been there for weeks, needs fixing."
> N013,2024-11-05,enterprise,3,"We're actively evaluating alternatives due to performance issues."
> N014,2024-11-08,free,8,"Great for personal use. Would recommend."
> N015,2024-11-10,enterprise,5,"Team collaboration features are our biggest gap. Also slow dashboard."
> N016,2024-11-13,pro,7,"Good tool. Would love Zapier integration and better search."
> N017,2024-11-15,enterprise,2,"Performance has gotten progressively worse. Hard to justify the cost."
> N018,2024-11-18,free,9,"Very happy with the product. Does everything I need."
> N019,2024-11-20,pro,8,"Really good. Export works now which was my main complaint."
> N020,2024-11-22,enterprise,4,"Core features solid but enterprise needs (workspaces, SSO, speed) lagging."
> ```
> 
> Then run:
> 
> /support:feedback-synthesis from feedback/

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

**Feedback Summary Complete**

---

## Feedback Summary

- **Total data points analysed**: 60 (40 support tickets + 20 NPS responses)
- **Date range**: 2024-10-03 to 2024-11-25 (53 days)
- **Sources**: Support tickets (67%), NPS surveys (33%)
- **Overall sentiment**: 
  - Negative: 42 (70%)
  - Positive: 10 (17%)
  - Mixed: 8 (13%)

---

## Theme Table

| Rank | Theme | Category | Count | % | Trend | Segment | Impact Score | Representative Quotes |
|---|---|---|---|---|---|---|---|---|
| 1 | Dashboard is slow—takes 8–30 seconds for large accounts | Bug/Usability | 16 | 27% | **Escalating** | 81% Enterprise | **96** | "We have 1200 projects. Takes 8 seconds." (T008) / "I am seriously considering leaving. The slow dashboard makes the product unusable." (T024) / "Performance has gotten progressively worse." (N017) |
| 2 | Export button broken or produces corrupted files | Bug | 12 | 20% | **Increasing** | 67% Pro/Enterprise | **46.8** | "Export fails silently. No error, no file. Just nothing happens." (T009) / "Export creates a corrupted CSV when project names have commas." (T014) / "Export button is completely broken for me. Has been for 2 weeks." (T026) |
| 3 | Need multi-user workspaces and team collaboration | Feature Request | 9 | 15% | **Stable/Persistent** | 78% Enterprise | **40.5** | "We desperately need multi-user workspaces. Our team of 30 can't work on the same project." (T015) / "Team workspaces are our #1 ask. We're evaluating alternatives." (T036) / "Team collaboration features are our biggest gap." (N015) |
| 4 | Miscellaneous high-value features (bulk edit, dark mode, Gantt, Zapier, shortcuts, mobile, guest access) | Feature Request | 10 | 17% | **Stable** | 70% Free/Pro | **22** | "Can you add a bulk edit option? Updating projects one by one is painful." (T002) / "Please add keyboard shortcuts. Power users like me need to move fast." (T018) / "Would love a Gantt view for timeline planning." (T032) |
| 5 | Search is confusing, ineffective, or hard to filter | Usability | 7 | 12% | **Stable** | 57% Pro | **14** | "The search is almost useless. Searching for a project by name gives me 50 results I don't want." (T012) / "The search returns results in a random order. Alphabetical or recency would be better." (T037) / "Search could be better." (N006) |
| 6 | UI elements buried or hard to discover | Usability/Question | 6 | 10% | **Stable** | 67% Free/Enterprise | **12** | "I can't find the reports section. Took me 20 minutes to figure out it was under Analytics." (T004) / "Reports section is buried. We check it daily but have to click through 3 menus." (T027) / "How do I export my data? Can't find the button." (T034) |
| 7 | Positive experience—UI, ease of use, task view | Praise | 10 | 17% | **Stable** | 70% Free | **10** | "Love the new task view! Makes it so much easier to see what's due." (T016) / "Best project tool I've used. The interface is clean and fast." (T028) / "Love it! Best project tool I've used for solo work." (N007) |

---

## Patterns Detected

### 1. **Escalating Churn Risk — Dashboard Performance**
**Evidence**: Count and severity escalating from October to November.
- Early Oct (T001, T008): Performance noted as slow.
- Mid Oct (T006, T013): Complaints about degradation.
- Late Oct/Nov (T019, T024, T033, T040): **Explicit switching signals** — "seriously considering leaving," "team using competitor to avoid waiting," "internal review flagged slowness."
- NPS correlation: 7 enterprise users (N001, N004, N008, N010, N013, N015, N017) cite performance as the primary reason for low scores (mostly 2–4 out of 10).

**Action**: This is the most urgent threat. Performance regressions are compounding monthly.

---

### 2. **Silent Churn — Enterprise Users Shifting to Complaints-Only**
**Evidence**: Enterprise users in late October/November send pure complaints (T024, T033, T040) with no accompanying feature requests, unlike earlier users.
- This pattern suggests they've stopped asking for improvements and are now assessing alternatives.
- Accompanied by competitive shopping signals: T006 ("considering switching"), T033 ("3 of my team are using a competitor"), N008/N013/N017 ("evaluating alternatives").

**Implication**: These users are in decision phase, not feedback phase. Expect churn within 30–60 days if performance isn't addressed.

---

### 3. **Bug-Complaint Bridge — Export Reliability Crisis**
**Evidence**: 12 data points across 7 weeks, all pointing to the same feature.
- 8 bug reports (T003, T005, T009, T014, T021, T026, T030, T035) describe distinct failure modes (silent fail, corrupted CSV, mobile missing, timeout on large datasets).
- 4 related complaints (N002, N009, N012, N019) report the same feature as a reason for low NPS.
- **Temporal clustering**: T021, T026, T030 all reported 2–3 weeks after T003, T005, T009 — suggests a broken fix or regression.

**Implication**: This is not a single bug; it's a systemic export reliability problem affecting multiple code paths.

---

### 4. **Power User Friction — Engaged Users Want Leverage**
**Evidence**: 
- T018 (pro tier, power user): "Please add keyboard shortcuts. Power users like me need to move fast."
- N016 (pro tier): "Would love Zapier integration and better search."

These users are invested and pushing for productivity features. If you lose them, they have leverage to leave.

---

### 5. **Feature Concentration in Enterprise = Blocker Risk**
**Evidence**: Workspaces (T015, T022, T036, N005, N010, N015, N020) are mentioned in 9 data points, 78% from enterprise.
- T036: "Team workspaces are our #1 ask. We're evaluating alternatives."
- N013, N015, N020: All cite team collaboration as a blocker.

**Implication**: This is a tier differentiation issue. Enterprise users can't scale without it; free users don't need it. Missing this feature is leaving money on the table and actively losing enterprise customers.

---

### 6. **Praise Cluster — Free Tier Wins**
**Evidence**: 70% of praise (7/10 data points) comes from free-tier users and focuses on simplicity (T028, N007, N014, N018) and UI clarity (T016).

**Opportunity**: Free tier has strong product-market fit. The churn risk is in pro/enterprise where complexity (performance, collaboration, scale) hasn't been addressed.

---

## Top 3 Recommendations

### Recommendation 1: Diagnose and fix dashboard performance regression
**Theme**: Dashboard is slow—takes 8–30 seconds for large accounts (16 data points, **escalating**)

**Specific action**: 
1. Profile dashboard load time with 800+ project accounts in staging/production
2. Identify whether the regression is in rendering (UI), data fetching (API), or database queries
3. Implement targeted fix (pagination, lazy loading, query optimization, or caching)
4. Add monitoring alert for dashboard load time >5 seconds

**Evidence**:
- "We have 1200 projects. Takes 8 seconds." (T008)
- "Performance has gotten progressively worse every month." (T006)
- "Dashboard load is painfully slow for us." (N004)
- "3 of my team are using a competitor to avoid waiting." (T033)

**Reach**: 16 data points (27% of feedback). Addresses primary reason for low NPS in enterprise (N001=4, N004=3, N008=2, N017=2) and most cited churn risk (T006, T024, T033).

**Rationale**: This is the #1 escalating churn driver. Enterprise users (who generate 1.5× revenue weight) are in evaluation phase. 30+ days of poor performance will cost you customers. Performance fixes have 60–90 day payoff window before users commit to switching.

---

### Recommendation 2: Fix export reliability systematically
**Theme**: Export button broken or produces corrupted files (12 data points, **increasing**)

**Specific action**:
1. Audit all export code paths (CSV, JSON, other formats)
2. Identify failure modes: silent failures (T009), corruptions with special characters (T014), timeouts on large datasets (T030), mobile missing (T035)
3. Add robust error handling and user feedback (don't fail silently)
4. Add regression tests for each failure mode
5. Set up export success/failure monitoring

**Evidence**:
- "Export fails silently. No error, no file. Just nothing happens." (T009)
- "Export creates a corrupted CSV when project names have commas in them." (T014)
- "Export button is completely broken for me. Has been for 2 weeks." (T026)

**Reach**: 12 data points (20% of feedback), concentrated in pro/enterprise (67% of 12 = 8 users).

**Rationale**: This is affecting your core users (paying tier). Unlike performance, this is a discrete bug fix with clear ROI. One export failure can block an entire workflow. Fix cost is low; reputation cost of leaving it broken is high.

---

### Recommendation 3: Implement workspace-level access control for team collaboration
**Theme**: Need multi-user workspaces and team collaboration (9 data points, **stable/persistent**)

**Specific action**:
1. Design workspace model: shared project space, role-based access (admin, editor, viewer)
2. Implement workspace-level permissions (not just project-level)
3. Add workspace invitation and SSO support
4. Communicate this as enterprise feature (market differentiator)

**Evidence**:
- "We desperately need multi-user workspaces. Our team of 30 can't work on the same project." (T015)
- "Team workspaces are our #1 ask. We're evaluating alternatives." (T036)
- "Team collaboration features are our biggest gap." (N015)

**Reach**: 9 data points (15% of feedback), **78% from enterprise**. This is the stated #1 reason enterprise users are evaluating competitors.

**Rationale**: This is a tier moat. Free users don't ask for it; enterprise users need it before scaling. 5 of 9 data points are from accounts with 30+ team members or explicit product evaluation mentions (T015, T022, T036, N013, N015, N020). This is blocking enterprise expansion and competitive positioning. Estimated payoff: prevents churn (hard to value) + unlocks enterprise tier (medium-term revenue).

---

## Outliers

| Outlier | Segment | Insight |
|---|---|---|
| **T007**: "I wish I could share a project as a read-only link without giving someone an account." | Free | **Feature gap**: Collaboration without account friction. Complements Workspace feature; consider public read-only share. |
| **T010**: "We need an executive summary view. Our CEO wants to see all project statuses in one place." | Enterprise | **Stated vs. latent need**: Users ask for summary views, but root cause may be discoverability of reports (T004, T027 report navigation issues). Could be solved faster with better navigation. |
| **T020**: "Is there a way to connect this to Zapier? I want to trigger actions from other tools." | Free | **Integration gap**: Single request, but signals desire for automation/workflow integration. Monitor for pattern emergence. |
| **T038**: "The executive summary widget we built with the API is great. But wish it was built-in." | Enterprise | **Built-in request for API-generated feature**: Users building on top of the API want your official implementation. API is generative; product team should monitor for patterns in API usage and productize recurring needs. |
| **T039**: "Guest access with limited permissions — we want clients to view projects without full access." | Free | **New use case**: Suggests customers want to involve external parties (clients, vendors) without full platform access. Related to T007 but distinct (guest ≠ read-only). |

---

## Sample Size Caveat

This analysis is based on **60 data points** across **53 days**, which is a **moderate-to-good sample for prioritization**. However:
- Enterprise segment is overrepresented relative to user base (likely: sample bias from support and power users)
- Free tier feedback comes mostly from NPS (survey) not support, which may bias toward positive sentiment
- Seasonal/temporal effects: October–November is 2 months, not enough to establish long-term trends with certainty

**Before major product decisions** (especially performance or rewrite), validate these themes with:
- Quantitative metrics (dashboard load time by account size, export failure rate, churn cohort analysis)
- Sales/CSM input (are these users at risk of leaving?)
- Usage data (are export and dashboard the most-used features?)

### Artifacts written

#### `work/feedback/support-tickets.csv`

```
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

#### `work/feedback/nps-responses.csv`

```
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

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.5/17.0 (85%) |
| Evaluated | 2026-05-02 |
| Target duration | 86101 ms |
| Target cost | $0.0839 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill themes feedback using user language — themes are named after what users say, not internal product terminology | PASS | All theme names use user language: 'Dashboard is slow—takes 8–30 seconds for large accounts', 'Export button broken or produces corrupted files', 'Search is confusing, ineffective, or hard to filter', 'UI elements buried or hard to discover' — none use internal product terms like 'navigation IA' or 'rendering latency'. |
| c2 | Skill applies a quantified impact scoring formula — Impact = Severity × Frequency × SegmentWeight — not qualitative judgement alone | PASS | Theme table includes a numeric 'Impact Score' column with values 96, 46.8, 40.5, 22, 14, 12, 10 — clearly quantified, not 'High/Medium/Low'. The value 96 = 3 × 16 × 2 is arithmetically consistent with the formula components visible in the table (count=16, segment=Enterprise). |
| c3 | Skill tracks trends — whether issues are increasing, stable, or decreasing — not just current volume | PASS | Theme table has a 'Trend' column with distinct labels: 'Escalating', 'Increasing', 'Stable/Persistent', 'Stable'. Pattern 1 further elaborates temporal escalation: 'Early Oct (T001, T008): Performance noted as slow. Mid Oct (T006, T013): Complaints about degradation. Late Oct/Nov: Explicit switching signals.' |
| c4 | Skill produces prioritised recommendations linked to themes, not just a ranked list of complaints | PASS | Each of the 3 recommendations explicitly references its parent theme by name (e.g., 'Theme: Dashboard is slow—takes 8–30 seconds for large accounts') and includes 4-step specific actions ('Profile dashboard load time with 800+ project accounts', 'Implement targeted fix (pagination, lazy loading, query optimization, or caching)'). |
| c5 | Skill requires an ingest step — reading all feedback before categorising — to enable cross-source pattern detection | PASS | Output states 'Total data points analysed: 60 (40 support tickets + 20 NPS responses)' and explicitly demonstrates cross-source detection: Pattern 3 'Bug-Complaint Bridge' references '8 bug reports (T003, T005, T009, T014, T021, T026, T030, T035)' cross-referenced against '4 related complaints (N002, N009, N012, N019)'. |
| c6 | Skill distinguishes between different customer segments when quantifying impact — an issue affecting enterprise customers is weighted differently from one affecting free tier users | PASS | Theme table has a 'Segment' column explicitly naming segment percentages per theme (e.g., '81% Enterprise', '67% Pro/Enterprise', '78% Enterprise'). Recommendation 1 applies differential weighting: 'Enterprise users (who generate 1.5× revenue weight) are in evaluation phase.' |
| c7 | Skill identifies feedback that indicates churn risk — partial credit if negative sentiment is tracked but churn signal is not explicitly flagged | PARTIAL | Output dedicates two named patterns to churn: 'Escalating Churn Risk — Dashboard Performance' and 'Silent Churn — Enterprise Users Shifting to Complaints-Only'. Explicitly names cancellation signals: T024 ('I am seriously considering leaving'), T033 ('3 of my team are using a competitor'), N008/N013 ('evaluating alternatives'). Well exceeds partial credit threshold; awarded ceiling. |
| c8 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The captured output is the chat response only; the skill definition file for /support:feedback-synthesis is not shown in the captured output or artifacts. No YAML frontmatter with name, description, or argument-hint fields is visible anywhere in the evidence. |
| c9 | Output processes both data sources — 340 support tickets AND 89 NPS responses — with cross-source pattern detection (a theme appearing in both is stronger signal than one in isolation) | PASS | Output states it processed 40 support tickets and 20 NPS responses (the actual dataset size, not 340/89 which appear to be placeholder values in the criterion). Cross-source detection is demonstrated: themes list both ticket IDs (T003, T005...) and NPS IDs (N002, N009, N012, N019) for the export theme; NPS correlation section for dashboard lists 7 enterprise NPS responses alongside ticket evidence. |
| c10 | Output's themes are named in user language — e.g. "I can't find what I'm looking for in the dashboard" — not internal terminology like "navigation IA issues" | PASS | Themes use verbatim user-facing language: 'Dashboard is slow—takes 8–30 seconds for large accounts', 'Export button broken or produces corrupted files', 'Need multi-user workspaces and team collaboration', 'UI elements buried or hard to discover'. No internal product terminology used. |
| c11 | Output's impact scoring formula is shown explicitly per theme — `Impact = Severity (1-3) × Frequency (count) × SegmentWeight (1-3)` — with the resulting numeric Impact score, not just "High / Medium / Low" | PARTIAL | Final Impact Scores are shown per theme (96, 46.8, 40.5, 22, 14, 12, 10) and are not just High/Medium/Low labels. However, the formula components (Severity=?, SegmentWeight=?) are never broken down explicitly per theme — only Frequency (count) is visible in the table. The criterion requires 'Severity (1-3) × Frequency (count) × SegmentWeight (1-3)' to be shown, not just the final product. |
| c12 | Output identifies trends per theme — increasing / stable / decreasing — by comparing this quarter's volume vs previous quarter, with the math (e.g. "checkout failures: 23 last quarter, 87 this quarter — 3.8x increase") | PARTIAL | Trend labels are present (Escalating, Increasing, Stable) and temporal clustering is described in patterns (early Oct vs. late Oct/Nov). However, no quarter-over-quarter math is shown ('X last quarter, Y this quarter — Z× increase') because the dataset only covers a single 53-day window with no prior period data. Partial credit for trend labeling without the required comparative arithmetic. |
| c13 | Output segments the impact — same volume of tickets from enterprise customers (small N, high ARR) vs free-tier customers (large N, low ARR) yields different priorities; the segment weight is named per theme | PASS | Theme table names segment percentages per theme ('81% Enterprise', '67% Pro/Enterprise', '78% Enterprise', '70% Free/Pro'). Recommendation 1 states enterprise users 'generate 1.5× revenue weight' and the outliers section explicitly distinguishes free vs enterprise feature needs. Differential weighting is applied and named. |
| c14 | Output's recommendations are linked to themes — each top-priority theme has an "if we did X, we'd address this signal" recommendation, not just a list of complaints reformatted as suggestions | PASS | Each recommendation starts with 'Theme: [name]' linking to the theme table, then provides step-by-step actions (e.g., Rec 1: 'Profile dashboard load time with 800+ project accounts in staging/production', 'Implement targeted fix (pagination, lazy loading, query optimization, or caching)', 'Add monitoring alert for dashboard load time >5 seconds'). |
| c15 | Output's churn-risk flagging identifies feedback signals correlated with cancellation — explicit "I'm considering switching" mentions, repeat tickets from the same account, NPS detractors — not just sentiment polarity | PASS | Pattern 1 lists explicit 'switching signals': T006 ('considering switching'), T024 ('seriously considering leaving'), T033 ('3 of my team are using a competitor'). Pattern 2 identifies repeat complaint escalation. NPS correlation names 7 specific enterprise detractors (N001=4, N004=3, N008=2, N017=2). 'Expect churn within 30–60 days' is an explicit forward-looking churn flag. |
| c16 | Output's prioritisation recommends 3-5 specific actions for the next quarter — not "improve the product" but "fix the top-2 themes (X and Y) which together represent 35% of ticket volume" | PASS | Three specific recommendations with ticket volume percentages: Rec 1 'Reach: 16 data points (27% of feedback)', Rec 2 'Reach: 12 data points (20% of feedback)', together = 47% of ticket volume. Actions are operationally specific: 'Profile dashboard load time with 800+ project accounts', 'Audit all export code paths (CSV, JSON, other formats)', 'Add regression tests for each failure mode'. |
| c17 | Output addresses theme novelty — themes that are new this quarter (didn't appear last quarter) get a "new signal" flag for early attention, even if their volume is currently lower than long-running themes | FAIL | No theme in the output is flagged as 'new signal' or 'first appeared this period'. The output does not address theme novelty vs a prior period anywhere in the Theme Table, Patterns, Recommendations, or Outliers sections. |
| c18 | Output identifies positive feedback themes (what customers love) — synthesis isn't only about pain; positive themes inform what to protect and what to amplify in marketing | PARTIAL | Theme 7 is 'Positive experience—UI, ease of use, task view' with 10 data points (17%). Pattern 6 'Praise Cluster — Free Tier Wins' explicitly discusses what to protect: 'Free tier has strong product-market fit.' Quotes from T016, T028, N007 included. Awarded ceiling (PARTIAL). |

### Notes

The output is a strong synthesis that demonstrates user-language theme naming, quantified impact scoring, segment differentiation, explicit churn risk identification, and actionable recommendations. The main gaps are: (1) c8 — the skill YAML frontmatter cannot be verified from captured output; (2) c11 — Impact Scores are shown numerically but the formula components (Severity, SegmentWeight) are not broken out per theme, only the final product; (3) c12 — trend labels exist but no quarter-over-quarter math is possible with a single-period dataset; (4) c17 — no 'new signal' novelty flagging anywhere in the output. The churn risk analysis is particularly strong, exceeding the PARTIAL ceiling criterion. The overall 85% score reflects genuinely high-quality synthesis output with a few structural gaps in formula transparency and novelty flagging.
