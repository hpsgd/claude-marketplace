---
name: launch-plan
description: Create a launch plan checklist for a product or feature release.
argument-hint: "[product or feature being launched]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Create a launch plan for $ARGUMENTS using the mandatory process below.

## Step 1 — Determine launch tier

Not every launch is the same. Classify first:

| Tier | Description | Examples | Typical timeline |
|---|---|---|---|
| **Tier 1 — Major** | New product, major feature, pricing change, rebrand | New product launch, v2.0, new pricing model | 4-8 weeks prep |
| **Tier 2 — Standard** | Significant feature, integration, meaningful improvement | New integration, workflow overhaul, new API | 2-4 weeks prep |
| **Tier 3 — Minor** | Small feature, improvement, quality of life | UI improvements, minor new feature, performance boost | 1-2 weeks prep |

The tier determines which checklist items are required vs. optional below.

## Step 2 — Pre-launch checklist

Complete these items before announcing anything. Items marked with tier numbers are required for that tier and above.

### Positioning and messaging (Tier 1, 2)

- [ ] **One-sentence description** written — can anyone on the team say what this is in one sentence?
- [ ] **Target audience defined** — who is this for, specifically? Name the segment.
- [ ] **Key benefit articulated** — not what it does, but why someone should care
- [ ] **Positioning approved** by stakeholders
- [ ] If Tier 1: **Positioning canvas completed** (use the `positioning` skill)

### Landing page / announcement (Tier 1, 2)

- [ ] **Announcement page** drafted and reviewed
- [ ] **Hero copy** finalised — headline, subhead, CTA
- [ ] **Screenshots / demo** created showing the feature in action
- [ ] **SEO metadata** set (title, description, OG tags)
- [ ] **URL** decided and redirects configured
- [ ] If Tier 1: **Landing page** live behind feature flag or preview URL

### Documentation (All tiers)

- [ ] **User documentation** written or updated (help center, guides)
- [ ] **API documentation** updated if applicable (use the `write-api-docs` skill)
- [ ] **Changelog entry** drafted (use the `write-changelog` skill)
- [ ] **Migration guide** written if there are breaking changes
- [ ] **Known limitations** documented — what doesn't it do (yet)?

### Support readiness (Tier 1, 2)

- [ ] **FAQ document** created — anticipate the top 10 questions
- [ ] **Support team briefed** — walkthrough completed, not just a doc
- [ ] **Escalation path defined** — who handles bugs? Who handles feedback?
- [ ] **Known issues list** shared with support — what's not perfect yet?
- [ ] **KB articles drafted** for common tasks (use the `write-kb-article` skill)
- [ ] If Tier 1: **Support staffing plan** for launch day (extra coverage?)

### Email (Tier 1, 2)

- [ ] **Announcement email** drafted — clear subject line, one CTA
- [ ] **Email segments defined** — who gets it? Everyone or targeted?
- [ ] **Onboarding email sequence** updated if the new feature changes the getting-started flow
- [ ] **Email tested** — send to yourself, check rendering, check links
- [ ] **Send time scheduled** — timezone-appropriate, avoid Mondays and Fridays

### Social media (Tier 1)

- [ ] **Social posts drafted** — platform-appropriate (not the same post everywhere)
- [ ] **Visual assets created** — images, GIFs, short video
- [ ] **Thread / post-launch content planned** — tips, use cases, customer stories
- [ ] **Community posts prepared** — relevant forums, Slack communities, subreddits

### Analytics and tracking (All tiers)

- [ ] **Success metrics defined** — what does "this launch went well" look like? Be specific with numbers.
- [ ] **Tracking events implemented** — feature usage, conversion, engagement
- [ ] **Dashboard created or updated** — can you see launch metrics in real-time?
- [ ] **Baseline captured** — what are the current numbers so you can measure change?

### Technical readiness (All tiers)

- [ ] **Feature flags configured** — can you toggle this off without a deploy?
- [ ] **Gradual rollout plan defined** — what percentage of users at each stage?
- [ ] **Rollback procedure documented** — if something goes wrong, how fast can you revert?
- [ ] **Load testing completed** if expecting traffic spike
- [ ] **Monitoring and alerting** configured for the new feature
- [ ] **Error budget assessed** — what's the acceptable error rate during launch?

## Step 3 — Rollout strategy

Choose and document the rollout approach:

| Strategy | When to use | Risk level |
|---|---|---|
| **Big bang** | Low-risk features, marketing-driven launches needing a moment | Medium |
| **Percentage rollout** | Any feature where you want to validate before full release | Low |
| **Cohort-based** | When you want feedback from specific user types first | Low |
| **Beta → GA** | Complex features needing extended validation | Lowest |
| **Dark launch** | Backend changes — enable for monitoring, no user announcement | Lowest |

Document the specific plan:

```
Rollout plan for [feature]:
- Day 0: Enable for internal team (dogfood)
- Day 1-3: 5% of users (monitor error rates, support volume)
- Day 4-7: 25% of users (watch for performance impact)
- Day 8: 100% of users (public announcement)

Kill switch: [feature flag name]
Rollback trigger: [specific condition — e.g., "error rate exceeds 1%" or "support tickets exceed 20/day"]
```

## Step 4 — Launch day checklist

A linear sequence — do these in order:

```
#### Morning (before announcement)
- [ ] Final deployment to production verified
- [ ] Smoke test core user flows: [list them]
- [ ] Monitoring dashboards open: [links]
- [ ] War room / communication channel open: [channel]
- [ ] Feature flag set to target rollout percentage
- [ ] All team members online and available: [list who]

#### Launch (go time)
- [ ] Publish announcement page / landing page
- [ ] Send announcement email
- [ ] Post on social channels
- [ ] Post changelog entry
- [ ] Update in-app messaging / banners if applicable
- [ ] Notify partners / integrators if applicable

#### Afternoon (first hours monitoring)
- [ ] Check error rates vs. baseline — are they within acceptable range?
- [ ] Check support ticket volume — any spike?
- [ ] Check core metrics — signups, activation, feature usage
- [ ] Read initial user feedback — social, support, community
- [ ] Address any critical bugs immediately
- [ ] Post first update to the team: "Launch status: [green/yellow/red]"
```

## Step 5 — Communication plan

Prepare messages for different audiences:

| Audience | Channel | When | Message |
|---|---|---|---|
| Internal team | Slack / email | Pre-launch (morning) | "Launching [feature] today. War room: [channel]. Rollback plan: [link]." |
| Support team | Briefing + doc | Pre-launch (1 week) | FAQ, known issues, escalation paths |
| Existing users | Email | Launch time | Announcement with clear CTA |
| Social followers | Social media | Launch time | Platform-appropriate announcement |
| Partners / integrators | Email | Pre-launch (if breaking changes) | Technical changes, migration guide, timeline |
| Press / analysts | Email | Pre-launch (if Tier 1) | Embargo briefing, press kit |

## Step 6 — Post-launch review (7-day)

Schedule a review at day 7. Assess:

### Metrics review

```
| Metric | Baseline | Day 1 | Day 3 | Day 7 | Target | Status |
|---|---|---|---|---|---|---|
| Feature adoption (% of active users) | 0% | | | | [target]% | |
| Error rate | [baseline]% | | | | < [target]% | |
| Support ticket volume (feature-related) | 0 | | | | < [target] | |
| Conversion impact | [baseline] | | | | [target] | |
| NPS / satisfaction | [baseline] | | | | [target] | |
```

### Qualitative review

- [ ] **Top 3 things that went well** — what should we repeat?
- [ ] **Top 3 things that didn't go well** — what should we fix?
- [ ] **Unexpected outcomes** — what surprised us?
- [ ] **User feedback themes** — what are people actually saying? (use the `feedback-synthesis` skill)
- [ ] **Follow-up items** — bugs to fix, quick wins to ship, docs to improve

### Decision

Based on the 7-day review:
- [ ] **Continue rollout** to 100% if not already there?
- [ ] **Iterate** — what changes based on feedback?
- [ ] **Rollback** — is this not working and should we revert?
- [ ] **Update roadmap** — what did we learn that changes our plans?

## Step 7 — Deliver the launch plan

Output the complete plan as a document with:
1. Launch tier and rationale
2. Pre-launch checklist (only include items relevant to the tier)
3. Rollout strategy with specific dates
4. Launch day run-of-show with times
5. Communication plan
6. Success metrics with targets
7. Post-launch review template with scheduled date

## Rules

- Every checklist item must have an owner. "Somebody should do this" means nobody will.
- Be specific about dates. "Before launch" is not a date. "By Monday April 7" is.
- Not every launch needs every item. A Tier 3 launch with a full Tier 1 checklist will never ship. Scope the plan to the launch size.
- The launch day checklist is a sequential run-of-show, not a grab bag. Order matters.
- If the feature can't be feature-flagged, say so — and adjust the rollout strategy to account for the higher risk.
- Always define what "success" looks like in numbers before launching. If you can't measure it, you can't evaluate it.
