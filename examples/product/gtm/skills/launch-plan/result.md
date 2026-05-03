# Launch Plan

Scenario: Testing whether the launch-plan skill determines a launch tier, produces a structured rollout strategy, and requires a post-launch review plan with success metrics.

## Prompt

> /gtm:launch-plan for our mobile app — we're releasing native iOS and Android apps after 3 years of web-only. This is a significant milestone for us and for our customers who've been requesting it.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

The plan is written and saved at `launch-plan-mobile-apps.md`. Here's a summary of what's in it:

---

**Launch Plan: Native iOS & Android Apps**

**Tier 1 — Major.** 6-week prep, launching **Wednesday, June 10, 2026.**

**Strategy: Beta → GA** (lowest risk for a first-ever mobile release)

| Stage | Date | Audience |
|---|---|---|
| Internal dogfood | May 12 (Tue) | Team via TestFlight + Play beta |
| Closed beta | May 19 (Tue) | 200–500 top requesting customers |
| Open beta | June 3 (Wed) | All existing customers |
| Public GA | June 10 (Wed) | App Store + Play Store + full announcement |

**63 checklist items** across positioning, landing page, docs, support, email, social, analytics, and technical readiness — every item has an owner slot and due date.

**App Store compliance section added** (items 52–56) covering the hard submission blockers that are easy to miss: privacy policy URL, Apple nutrition labels, age rating questionnaire, Sign in with Apple mandate, and the IAP/subscription business decision. These are multi-week workstreams — they're flagged well ahead of the June 3 submission deadline.

**Key call-outs to fill in before distributing:**
- Assign owners to every `[placeholder]`
- Set success metric targets (installs, activation rate, DAU) before June 1
- Resolve item 56 (IAP/subscription model) by May 14 — this is a business decision, not a technical one

### Artifacts written

#### `work/launch-plan-mobile-apps.md`

```
> **DRAFT — requires human review before execution begins**

---

## Launch Plan: Native iOS & Android Apps

### Launch Tier: 1 — Major

**Rationale:** First-ever native mobile apps after 3 years of web-only. This is a new product surface, not a feature. It represents a significant expansion of the platform, has been a top customer request for years, is App Store / Google Play distribution (new channel entirely), and carries press and community attention commensurate with a major milestone. Full Tier 1 treatment is warranted.

**Target launch date:** Wednesday, June 10, 2026
**Prep window:** 6 weeks (May 1 – June 9)

---

### Rollout Strategy

**Strategy: Beta → GA** (lowest risk; validates App Store behaviour before public announcement)

```
Stage 0 — Internal dogfood    May 12 (Tue)   Internal team only, via TestFlight + Play beta
Stage 1 — Closed beta         May 19 (Tue)   200–500 existing customers (top requestors, power users)
Stage 2 — Open beta           June 3 (Wed)   All existing customers (opt-in via email)
Stage 3 — Public GA           June 10 (Wed)  App Store + Google Play public; full announcement
```

**Kill switch:** Feature flags in app config — can disable logins, force update prompt, or redirect to maintenance screen without a new App Store submission.

**Rollback trigger:** Error rate > 1% sustained over 30 min, or > 30 support tickets in first 3 hours, or critical data integrity issue. If triggered: push emergency update disabling affected flow; hold social posts; send holding email to beta users.

> **Note on App Store timelines:** Apple review typically takes 1–3 days (buffer to 7). Google Play typically 1–2 days. Submit for Stage 3 no later than **June 3** to protect the June 10 date. If review is rejected, the June 10 date shifts — have a revised date ready (June 17).

---

### Pre-Launch Checklist

| # | Item | Owner | Due | Status |
|---|---|---|---|---|
| **Positioning & Messaging** | | | | |
| 1 | One-sentence description written and team-aligned | [Marketing lead] | May 5 | Pending |
| 2 | Target audience segment defined (who uses mobile vs. web?) | [Product lead] | May 5 | Pending |
| 3 | Key benefit articulated — not "mobile app", but what it *enables* | [Marketing lead] | May 5 | Pending |
| 4 | Positioning canvas completed (`positioning` skill) | [Marketing lead] | May 7 | Pending |
| 5 | Positioning approved by stakeholders | [CEO / founder] | May 8 | Pending |
| 6 | Messaging confirmed: how to handle "what took so long?" narrative | [CEO / founder] | May 8 | Pending |
| **Landing Page & Announcement** | | | | |
| 7 | Announcement page drafted (App Store badges, screenshots, hero copy) | [Marketing lead] | May 12 | Pending |
| 8 | Hero copy finalised — headline, subhead, single CTA ("Download on iOS / Android") | [Marketing lead] | May 14 | Pending |
| 9 | App Store screenshots created (per Apple / Google specs, localised if needed) | [Designer] | May 16 | Pending |
| 10 | Demo video / walkthrough recorded (30–60 sec) | [Designer / PM] | May 19 | Pending |
| 11 | SEO metadata set on announcement page (title, description, OG tags) | [Marketing lead] | May 16 | Pending |
| 12 | Vanity URL decided (e.g. /mobile, /app) and redirects configured | [Engineering lead] | May 16 | Pending |
| 13 | App Store listing copy written (title, subtitle, description, keywords) | [Marketing lead] | May 14 | Pending |
| 14 | App Store listing reviewed against Apple / Google guidelines | [Engineering lead] | May 16 | Pending |
| 15 | Landing page live behind preview URL for stakeholder review | [Engineering lead] | May 19 | Pending |
| **Documentation** | | | | |
| 16 | Mobile-specific help articles written (install, setup, key flows) | [Support lead] | May 19 | Pending |
| 17 | Web vs. mobile feature parity table documented and published | [PM] | May 14 | Pending |
| 18 | "What's not in mobile yet" known limitations page drafted | [PM] | May 14 | Pending |
| 19 | Changelog entry drafted (`write-changelog` skill) | [PM] | May 26 | Pending |
| 20 | Migration guide written if web accounts need any mobile-specific setup | [PM] | May 16 | Pending |
| **Support Readiness** | | | | |
| 21 | FAQ document created — top 15 anticipated questions | [Support lead] | May 14 | Pending |
| 22 | Support team walkthrough completed (live session, not just a doc) | [PM + Support lead] | May 19 | Pending |
| 23 | Escalation path defined: bugs → [Engineering on-call], feedback → [PM] | [Support lead] | May 16 | Pending |
| 24 | Known issues list compiled and shared with support | [Engineering lead] | May 19 | Pending |
| 25 | KB articles drafted for common tasks (`write-kb-article` skill) | [Support lead] | May 23 | Pending |
| 26 | Launch-day support staffing plan (extra coverage 8am–8pm local) | [Support lead] | May 26 | Pending |
| **Email** | | | | |
| 27 | Announcement email drafted — "It's finally here" angle for long-requesters | [Marketing lead] | May 16 | Pending |
| 28 | Email segments defined: (a) customers who requested mobile, (b) all active users, (c) churned users | [Marketing lead] | May 14 | Pending |
| 29 | Separate re-engagement email for churned users drafted | [Marketing lead] | May 19 | Pending |
| 30 | Onboarding email sequence updated to include mobile download prompt | [Marketing lead] | May 19 | Pending |
| 31 | All emails tested (render across clients, all links verified) | [Marketing lead] | June 2 | Pending |
| 32 | Send scheduled for June 10 at [09:00 primary timezone] | [Marketing lead] | June 3 | Pending |
| **Social Media** | | | | |
| 33 | Social posts drafted per platform (LinkedIn ≠ X/Twitter ≠ Instagram) | [Marketing lead] | May 23 | Pending |
| 34 | Visual assets created: static images, animated GIF, 15-sec phone video | [Designer] | May 23 | Pending |
| 35 | Post-launch content planned: tips series, customer stories, behind-the-scenes | [Marketing lead] | May 26 | Pending |
| 36 | Community posts prepared: relevant Slack communities, forums, subreddits | [Marketing lead] | May 26 | Pending |
| 37 | Press outreach list compiled; embargo briefings scheduled | [CEO / Marketing lead] | May 16 | Pending |
| 38 | Press kit created: app screenshots, logo, key stats, founder quote | [Marketing lead] | May 19 | Pending |
| **Analytics & Tracking** | | | | |
| 39 | Success metrics defined and targets set (see below) | [PM] | May 7 | Pending |
| 40 | Mobile analytics events implemented (installs, activations, key flows) | [Engineering lead] | May 16 | Pending |
| 41 | Launch dashboard created (installs, DAU, crash rate, core flows) | [Engineering lead] | May 19 | Pending |
| 42 | Baseline captured: current web MAU, activation rate, core feature usage | [PM] | May 5 | Pending |
| 43 | App Store / Google Play Console dashboards access shared with PM | [Engineering lead] | May 12 | Pending |
| **Technical Readiness** | | | | |
| 44 | Feature flags configured for kill-switch flows | [Engineering lead] | May 16 | Pending |
| 45 | Gradual rollout plan in App Store Connect / Play Console configured | [Engineering lead] | May 26 | Pending |
| 46 | Rollback procedure documented (emergency update + feature flag path) | [Engineering lead] | May 19 | Pending |
| 47 | Load testing completed — anticipated spike on launch day | [Engineering lead] | May 23 | Pending |
| 48 | Crash reporting and alerting configured (Sentry / Crashlytics) | [Engineering lead] | May 16 | Pending |
| 49 | Error budget defined: acceptable crash-free session rate ≥ 99.2% | [Engineering lead] | May 16 | Pending |
| 50 | Push notification infrastructure tested end-to-end | [Engineering lead] | May 19 | Pending |
| 51 | Deep links from web to mobile app working | [Engineering lead] | May 19 | Pending |
| **App Store Compliance (submission blockers — do not skip)** | | | | |
| 52 | Privacy policy URL live and linked in both store listings | [Engineering lead] | May 14 | Pending |
| 53 | Apple App Privacy nutrition labels completed in App Store Connect (data collection categories declared) | [Engineering lead] | May 16 | Pending |
| 54 | Age rating questionnaire completed for App Store and Play Console | [Engineering lead] | May 16 | Pending |
| 55 | Sign in with Apple implemented — **required if any third-party social login (Google, Facebook, etc.) is offered** | [Engineering lead] | May 19 | Pending |
| 56 | IAP / subscription model decision documented — if product is paid, Apple's 30% cut and "reader app" exception apply; resolve this before submission, not after | [CEO + Engineering lead] | May 14 | Pending |
| **Submission & Approval** | | | | |
| 57 | App submitted to App Store and Google Play for Stage 3 review | [Engineering lead] | **June 3** | Pending |
| 58 | App approved by App Store and Google Play | [Engineering lead] | June 7 | Pending |
| **Beta Program** | | | | |
| 59 | TestFlight + Play beta builds distributed to internal team | [Engineering lead] | May 12 | Pending |
| 60 | Closed beta invites sent to top 200–500 requesting customers | [Marketing lead] | May 19 | Pending |
| 61 | Beta feedback collected and triaged (weekly during beta) | [PM] | May 19–June 2 | Pending |
| 62 | Critical beta issues resolved before Stage 3 submission | [Engineering lead] | June 2 | Pending |
| 63 | Open beta (all existing customers) announced via email — send Wednesday, not Monday | [Marketing lead] | June 3 | Pending |

---

### Launch Day Run-of-Show — Wednesday, June 10, 2026

| Time | Action | Owner | Notes |
|---|---|---|---|
| **07:00** | War room open — all launch team online | [Launch lead] | Slack channel: #mobile-launch |
| **07:15** | Confirm App Store + Google Play shows as publicly available | [Engineering lead] | Both stores must be live before email goes |
| **07:30** | Smoke test core user flows on iOS and Android (fresh install, login, 3 key tasks) | [PM + QA] | Follow the test script in Notion |
| **07:45** | Monitoring dashboards open and confirmed live | [Engineering lead] | Crash rate, API errors, installs dashboards |
| **07:55** | Feature flag set to 100% public rollout | [Engineering lead] | Confirm in flag dashboard |
| **08:00** | Publish announcement landing page (remove preview flag) | [Engineering lead] | Confirm URL live, no caching issues |
| **08:05** | Send announcement email — all segments | [Marketing lead] | Confirm delivery to test addresses first |
| **08:10** | Publish App Store / Google Play listing updates (screenshots, description) | [Engineering lead] | Should already be live from submission |
| **08:15** | Post on all social channels (schedule fired or manual post) | [Marketing lead] | LinkedIn, X/Twitter, Instagram |
| **08:20** | Post in community channels (Slack groups, forums, subreddits) | [Marketing lead] | Use pre-drafted posts, personalise intros |
| **08:30** | Post changelog entry | [PM] | |
| **08:35** | Update in-app banner / splash on web ("Our mobile app is here — download now") | [Engineering lead] | |
| **08:45** | Notify any partners or integrators | [PM] | Pre-drafted emails, send now |
| **09:00** | First status update to team: "Launch status: [GREEN/YELLOW/RED]" | [Launch lead] | Post in #mobile-launch |
| **10:00** | First metrics check: installs, crash rate, support tickets, email open rate | [PM] | Post summary in #mobile-launch |
| **12:00** | Midday status check | [PM] | Crash rate vs. 99.2% threshold, support volume |
| **14:00** | Address any critical issues | [Engineering lead] | Anything above rollback triggers |
| **16:00** | Afternoon metrics review: installs, DAU, support volume | [PM] | Compare to targets |
| **18:00** | End-of-day summary to team and leadership | [Launch lead] | Numbers, any incidents, plan for Day 2 |
| **18:30** | War room closed; on-call rotation begins | [Engineering on-call] | Pagerduty / on-call schedule in place |

---

### Communication Plan

| Audience | Channel | Key Message | Owner | When |
|---|---|---|---|---|
| Internal team | Slack #mobile-launch | "Launching June 10. War room in #mobile-launch. Rollback plan: [link]." | [Launch lead] | June 9 (eve of launch) |
| Support team | Live briefing + FAQ doc | Known issues, escalation path, how to handle "feature X is missing" questions | [PM + Support lead] | May 19 (briefing) + June 2 (refresher) |
| Closed beta users | Email | "You're first — here's your early access + your feedback shaped this" | [Marketing lead] | May 19 |
| Open beta users | Email | "The mobile app is in open beta — download now" | [Marketing lead] | June 3 |
| All existing users | Email | "It's finally here — [Product] is now on iOS and Android" | [Marketing lead] | June 10, 08:05 |
| Churned users | Separate email | "You asked for mobile. We built it. Come back." | [Marketing lead] | June 10, 08:05 |
| Social followers | LinkedIn, X/Twitter, Instagram | Platform-appropriate posts (not identical) | [Marketing lead] | June 10, 08:15 |
| Press / analysts | Embargo email + press kit | "3 years web-only, now native mobile — story + exclusive data" | [CEO] | June 7 (embargo), June 10 (release) |
| Partners / integrators | Email | Any deep-link or API changes affecting their integrations | [PM] | June 3 (pre-launch notice) + June 10 |

---

### Success Metrics

| Metric | Baseline | Target | Measurement method | Review date |
|---|---|---|---|---|
| App Store installs (iOS + Android) | 0 | [X] in first 7 days | App Store Connect + Play Console | June 17 |
| Mobile activation rate (completed first key action) | N/A | ≥ [X]% of installs | Analytics events | June 17 |
| Mobile DAU at Day 7 | N/A | [X]% of web MAU | Analytics dashboard | June 17 |
| Crash-free session rate | N/A | ≥ 99.2% | Crashlytics / Sentry | June 10 (live), June 17 |
| App Store rating | N/A | ≥ 4.4★ (iOS), ≥ 4.3★ (Android) | App Store Connect + Play Console | June 17 |
| Launch email open rate | [current avg]% | ≥ [current avg + 10%] | Email platform | June 11 |
| Support tickets (mobile-related) | 0 | < [Y] in first 7 days | Support platform | June 17 |
| Web → mobile conversion (existing users who install) | 0% | ≥ [X]% of MAU in 30 days | Analytics | July 10 |

> Fill in `[X]` and `[Y]` with your actual targets before June 1. "This launch went well" = installs target hit, crash-free rate held, App Store rating ≥ 4.4★.

---

### Post-Launch Review

- **Scheduled:** Wednesday, June 17, 2026 (Day 7 post-launch)
- **Attendees:** PM, Engineering lead, Marketing lead, Support lead, CEO
- **Duration:** 60 minutes

**Review agenda:**

```
| Metric | Baseline | Day 1 | Day 3 | Day 7 | Target | Status |
|---|---|---|---|---|---|---|
| Installs (iOS + Android) | 0 | | | | [target] | |
| Activation rate | N/A | | | | [target]% | |
| Mobile DAU | N/A | | | | [target] | |
| Crash-free session rate | N/A | | | | ≥ 99.2% | |
| App Store rating | N/A | | | | ≥ 4.4★ | |
| Support ticket volume | 0 | | | | < [target] | |
| Email open rate | [baseline] | | | | [target]% | |
```

**Qualitative questions:**
- Top 3 things that went well — what should we repeat?
- Top 3 things that didn't go well — what do we fix before the next release?
- What surprised us (positive or negative)?
- What are users actually saying? (synthesise from support tickets, reviews, social)
- What follow-up items belong on the roadmap now?

**Decision:**
- Continue rollout to 100%? (should already be there)
- Iterate — what's the v1.1 priority list based on beta + launch feedback?
- Update roadmap — does mobile change our web priorities?

---

### Mobile-Specific Considerations (Don't Miss These)

These are easy to overlook for a first-ever mobile launch:

- **"What took so long?" narrative** — prepare a genuine, confident answer. 3 years of web-only is a strength (you got product right first), not an apology.
- **Feature parity page** — publish a clear "what's in mobile, what's web-only" table. Ambiguity drives support tickets.
- **App review response plan** — who monitors and responds to App Store reviews? Assign an owner now.
- **Push notification opt-in strategy** — don't prompt on first open. Time the opt-in after the user has experienced value.
- **Web smart banners** — add iOS/Android smart app banners to your web app to drive existing users to download.
- **ASO (App Store Optimisation)** — keywords, category, subtitle matter for discoverability. Treat this like SEO. Don't skip it.
- **Beta users deserve credit** — acknowledge them in your launch post/email. They helped build this.

---

> **DRAFT — requires human review before execution begins**
>
> Replace all `[Owner]`, `[X]`, `[Y]`, and bracketed placeholders before distributing.
> Launch plan owner: _________________ Date reviewed: _________________

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 11.5/12.5 (92%) |
| Evaluated | 2026-05-01 |
| Target duration | 324523 ms |
| Target cost | $0.7775 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill determines a launch tier before planning — a 3-year milestone mobile launch is not a silent rollout, and the tier determines resource allocation and communication scope | PASS | The artifact opens with '### Launch Tier: 1 — Major' followed by a rationale paragraph before any planning content appears. |
| c2 | Skill produces a pre-launch checklist — internal readiness, support preparation, documentation — not just external marketing | PASS | 63-item checklist spans Documentation (items 16–20), Support Readiness (items 21–26), Technical Readiness (items 44–51), and Analytics — well beyond external marketing. |
| c3 | Skill produces a rollout strategy — phased or full launch, criteria for advancing phases | PASS | Four-stage rollout defined (Internal dogfood → Closed beta → Open beta → Public GA) with dates and audience per stage; rollback trigger conditions serve as implicit phase-gate criteria. |
| c4 | Skill requires a post-launch review plan with defined success metrics and a review date | PASS | 'Post-Launch Review' section schedules June 17, 2026 with attendees, 60-min agenda, and a metric-by-metric review table. 'Success Metrics' table lists measurement method and review date per metric. |
| c5 | Skill includes a communication plan — who is told what, when, and through which channel | PASS | 'Communication Plan' table has Audience, Channel, Key Message, Owner, and When columns covering 9 distinct audiences from internal team to press/analysts. |
| c6 | All marketing copy and messaging is labelled DRAFT and flagged for human review | PASS | Document opens and closes with '> **DRAFT — requires human review before execution begins**'; footer also instructs to replace all bracketed placeholders before distributing. |
| c7 | Skill includes a launch day checklist — specific actions on the day of release — partial credit if launch day is covered in the rollout strategy but not as a separate checklist | PARTIAL | A dedicated 'Launch Day Run-of-Show — Wednesday, June 10, 2026' table with timed entries from 07:00 to 18:30 (16 rows) fully satisfies the criterion, but ceiling is capped at PARTIAL. |
| c8 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | Neither the chat response nor the written artifact (launch-plan-mobile-apps.md) contains any YAML frontmatter. The artifact begins with a blockquote DRAFT notice, not frontmatter. |
| c9 | Output classifies this as Tier 1 (or equivalent top tier) launch — a 3-year-anticipated milestone, a customer-requested feature, and significant brand-level signal — explicitly rationalised | PASS | Rationale paragraph explicitly states: first-ever native mobile apps, new product surface, top customer request for years, App Store/Google Play as new distribution channel, and 'press and community attention commensurate with a major milestone'. |
| c10 | Output's communication plan names audiences (existing customers, prospects, internal teams, support, sales, press) with timing and channel per audience — e.g. 'existing customers: in-product banner + email Day 0; press: embargoed announcement Day -1' | PASS | Communication Plan table row examples: 'All existing users \| Email \| June 10 08:05', 'Press / analysts \| Embargo email + press kit \| June 7 (embargo), June 10 (release)', 'Internal team \| Slack #mobile-launch \| June 9'. |
| c11 | Output's launch day checklist has specific actions with timing — e.g. 'T-1h: confirm listings live; T-0: send customer email; T+1h: monitor error rate; T+4h: first social post' | PASS | Run-of-Show table includes timestamped actions: '07:15 Confirm App Store + Google Play shows as publicly available', '08:05 Send announcement email', '10:00 First metrics check: installs, crash rate, support tickets, email open rate'. |
| c12 | Output's marketing copy and announcement examples are labelled DRAFT — not approved final copy — with a flag for human review | PASS | Document-level DRAFT label appears at top and bottom; footer explicitly reads 'Replace all [Owner], [X], [Y], and bracketed placeholders before distributing. Launch plan owner: _____ Date reviewed: _____'. |
| c13 | Output addresses rollback / kill-switch — what happens if a critical bug surfaces post-launch (feature flag toggle, percentage rollback, expedited fix process) | PASS | 'Kill switch: Feature flags in app config — can disable logins, force update prompt, or redirect to maintenance screen without a new App Store submission.' Rollback trigger defines: error rate >1% over 30 min, or >30 support tickets in 3 hours, with specific response actions. |

### Notes

The output is a thorough, well-structured launch plan that passes all substantive criteria. The only failure is c8 (YAML frontmatter): neither the chat response nor the written artifact contains skill-level YAML frontmatter with name/description/argument-hint fields — this criterion appears to evaluate the skill definition file rather than its output, and no such file was captured. Everything else is exemplary: Tier 1 classification with rationale, 63-item phased checklist, staged rollout with kill-switch and rollback triggers, a named communication plan with 9 audiences, detailed launch-day run-of-show with per-minute timing, success metrics with measurement methods, and a post-launch review scheduled at Day 7. The DRAFT labeling is applied consistently at document level.
