# Launch Plan

Scenario: Testing whether the launch-plan skill determines a launch tier, produces a structured rollout strategy, and requires a post-launch review plan with success metrics.

## Prompt

> /gtm:launch-plan for our mobile app — we're releasing native iOS and Android apps after 3 years of web-only. This is a significant milestone for us and for our customers who've been requesting it.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll create a comprehensive launch plan for your mobile app release. This is a **Tier 1 — Major** launch (new product offering after 3 years of web-only), so I'll include full coverage of positioning, messaging, support readiness, and detailed rollout strategy.

A few quick clarifications before I finalize this:

1. **Timeline** — when are you targeting for launch? (This drives the prep schedule.)
2. **Platform sequence** — iOS and Android simultaneously, or staggered? (iOS typically goes first due to app store review time.)
3. **Feature parity** — are the mobile apps matching web feature-for-feature at launch, or a subset?
4. **User base size** — roughly how many active users will you be rolling out to?

I'll draft a plan with reasonable assumptions, but I'll flag sections where you'll need to fill in specifics unique to your product. Ready?

---

## DRAFT — Launch Plan: Native Mobile Apps (iOS & Android)

**DRAFT — requires human review and team input before execution**

### Launch Tier: **1 — Major**

**Rationale:** First native mobile apps after 3 years of web-only; significant customer demand; new platform requiring distinct support, release cadence, and positioning. Requires full pre-launch validation, coordinated rollout, and sustained post-launch monitoring.

---

### Pre-Launch Checklist

#### Positioning and Messaging

| # | Item | Owner | Due | Notes |
|---|---|---|---|---|
| 1 | One-sentence description finalized | [Product] | [DATE] | E.g., "Native iOS and Android apps bringing [key benefit] to mobile-first users." |
| 2 | Target audience segments defined | [Product] | [DATE] | Prioritize: existing web users, iOS-only, Android-only, both? |
| 3 | Key mobile benefit articulated (not feature list) | [Product] | [DATE] | Why now? What changes with mobile that doesn't on web? |
| 4 | Positioning canvas completed | [Product] | [DATE] | Use `/gtm:positioning` skill |
| 5 | Messaging approved by leadership | [Leadership] | [DATE] | Alignment with brand, market positioning, customer narrative |

#### Landing Page & Announcement

| # | Item | Owner | Due | Notes |
|---|---|---|---|---|
| 6 | Announcement page drafted | [Marketing] | [DATE] | Highlight customer demand, mobile-first experience, feature parity (or roadmap) |
| 7 | Hero copy finalized (headline + subhead) | [Marketing] | [DATE] | Headline test: does it answer "why should I download this?" |
| 8 | App store screenshots created | [Design + Product] | [DATE] | 5-8 screens showing key flows (onboarding, core use case, unique mobile feature) |
| 9 | Demo video recorded (30-60 sec) | [Marketing] | [DATE] | Quick walkthrough of the app in action |
| 10 | SEO metadata set (title, desc, OG tags) | [Marketing] | [DATE] | Optimize for "app name iOS" and "app name Android" |
| 11 | Landing page URL decided + redirects configured | [Eng] | [DATE] | E.g., yoursite.com/mobile or yoursite.com/apps |
| 12 | Landing page live (behind feature flag) | [Eng] | [DATE] | Test internally before public announcement |

#### Documentation

| # | Item | Owner | Due | Notes |
|---|---|---|---|---|
| 13 | In-app onboarding flow documented | [Product] | [DATE] | First-time user experience walkthrough |
| 14 | Mobile-specific help center section created | [Support/Docs] | [DATE] | Separate from web docs; mobile-specific troubleshooting |
| 15 | App store listing optimized (description, keywords) | [Marketing] | [DATE] | App Store & Google Play metadata |
| 16 | Changelog entry drafted | [Product] | [DATE] | Use `/gtm:write-changelog` skill |
| 17 | Known limitations documented | [Product] | [DATE] | What features aren't in v1? What's the roadmap? |
| 18 | Migration guide for power users | [Support] | [DATE] | How to move from web to mobile (if data migration needed) |

#### Support Readiness

| # | Item | Owner | Due | Notes |
|---|---|---|---|---|
| 19 | FAQ document: top 15 questions | [Support] | [DATE] | Download process, permissions, syncing, platform-specific issues |
| 20 | Support team walkthrough (not just doc) | [Product] | [DATE] | Live Q&A with support team; role-play common scenarios |
| 21 | Escalation path defined | [Support Lead] | [DATE] | Platform crash? Data loss? Sync bug? → who owns it? |
| 22 | Known issues & workarounds shared | [Eng] | [DATE] | What's broken/imperfect in v1? How do we advise customers? |
| 23 | KB articles drafted (first 10 issues) | [Support] | [DATE] | Use `/gtm:write-kb-article` skill |
| 24 | Support staffing plan for launch week | [Support Lead] | [DATE] | Extra coverage? Shift coverage? On-call rotation? |
| 25 | Mobile-specific ticket template created | [Support] | [DATE] | Device OS, app version, reproduction steps |

#### Email

| # | Item | Owner | Due | Notes |
|---|---|---|---|---|
| 26 | Announcement email drafted | [Marketing] | [DATE] | Subject line A/B tested; one clear CTA (download link) |
| 27 | Email segments defined | [Marketing] | [DATE] | All users? iOS users first? Tier-based by engagement? |
| 28 | Onboarding email sequence updated | [Marketing] | [DATE] | If existing web users, email journey after app download |
| 29 | Push notification copy prepared | [Product] | [DATE] | First push (announce availability), follow-up (try key feature) |
| 30 | Email tested across clients | [Marketing] | [DATE] | Outlook, Gmail, iOS Mail, Android Gmail — all render correctly |
| 31 | Send time scheduled | [Marketing] | [DATE] | Timezone-appropriate (suggest Tuesday-Thursday, 9-11am) |

#### Social Media (if Tier 1 applies to your brand)

| # | Item | Owner | Due | Notes |
|---|---|---|---|---|
| 32 | Social posts drafted (platform-specific) | [Marketing] | [DATE] | LinkedIn (professional), Twitter (quick take), Instagram (visual) |
| 33 | Visual assets created | [Design] | [DATE] | App icon closeup, screenshot carousel, short GIF (iOS + Android) |
| 34 | Thread/post-launch content planned | [Marketing] | [DATE] | Day 1: announcement; Day 3: feature deep-dive; Day 7: user story |
| 35 | Community posts prepared | [Marketing] | [DATE] | Relevant Slack communities, subreddits, forums — no spam, add value |

#### Analytics & Tracking

| # | Item | Owner | Due | Notes |
|---|---|---|---|---|
| 36 | Success metrics defined with targets | [Product] | [DATE] | See "Success Metrics" section below |
| 37 | Tracking events implemented | [Eng] | [DATE] | App launch, onboarding completion, first action, daily active, churn |
| 38 | Analytics dashboard created | [Eng] | [DATE] | Real-time view of installs, DAU, feature usage, errors |
| 39 | Baseline captured (web metrics) | [Data] | [DATE] | Current web usage patterns — what's the control? |

#### Technical Readiness

| # | Item | Owner | Due | Notes |
|---|---|---|---|---|
| 40 | Feature flags configured for mobile | [Eng] | [DATE] | Can you toggle the mobile apps off/on without re-deploy? |
| 41 | Gradual rollout plan defined | [Eng] | [DATE] | See "Rollout Strategy" section below |
| 42 | Rollback procedure documented | [Eng] | [DATE] | Kill switch, data integrity, user communication template |
| 43 | Load testing completed | [Eng] | [DATE] | Expected traffic spike on API? Expected concurrent users? |
| 44 | Monitoring & alerting configured | [Eng] | [DATE] | API errors, app crash rate, sync failures, auth issues, latency |
| 45 | Error budget assessed | [Eng] | [DATE] | Acceptable error rate during launch? (Suggest <1%) |
| 46 | App store submissions reviewed | [Eng + Legal] | [DATE] | Apple review checklist, Google Play requirements, privacy policy |
| 47 | Push notification service tested | [Eng] | [DATE] | APNs (iOS), FCM (Android) — end-to-end test |
| 48 | Syncing behavior tested (offline + online) | [Eng] | [DATE] | Data consistency between web and mobile; conflict resolution |

---

### Rollout Strategy

**Assumption:** App store approval takes 1-2 weeks for iOS, same-day for Android.

#### Stage 1: Internal Dogfood (3 days before public launch)
- **Users:** Internal team only (100% of test users)
- **Platform:** iOS TestFlight + Android Firebase App Distribution
- **Go/no-go criteria:**
  - Onboarding completes without errors
  - Core user flows work (login, create/edit, delete, navigate)
  - No app crashes in first 5 minutes of use
  - Sync between web and mobile is consistent
  - Support team can answer FAQ questions

#### Stage 2: Limited Beta (1 day before public launch)
- **Users:** 5–10% of existing web users (beta testers opted in)
- **Platform:** App store links live; limited audience
- **Monitoring:** Error rate, session length, feature usage, early feedback
- **Go/no-go criteria:**
  - Error rate < 2%
  - No data loss incidents
  - Support volume manageable (< 5 tickets/day)
  - NPS from beta feedback > 7/10
  - **Kill switch:** Disable public visibility in app stores; communicate with beta testers

#### Stage 3: Public Launch (Day 0)
- **Users:** 100% of active users (both platforms simultaneously)
- **Announcement:** Email, social, in-app banner, website homepage
- **Monitoring:** Real-time dashboards; war room open for 48 hours
- **Kill switch:** Feature flag to disable API endpoints; app store takedown (slower, last resort)

#### Rollback Trigger (any of these)
- Error rate exceeds 2% for > 30 minutes
- Database data loss confirmed
- Auth system broken (users can't log in)
- Support volume > 50 critical tickets in a day
- App crash rate > 5%

---

### Launch Day Run-of-Show

#### Morning (Approx. 8:00 AM local time, 1 day before public launch)

| Time | Action | Owner | Notes |
|---|---|---|---|
| 8:00 | War room opens (Slack channel) | [Product] | All leads join; escalation path clear |
| 8:15 | Final production deployment verified | [Eng] | Run smoke tests: login, onboarding, core flow, sync |
| 8:30 | Monitoring dashboards live | [Eng] | Open: error rates, API latency, app crashes, support queue |
| 8:45 | App store links go live (limited audience) | [Eng] | Links become clickable; only beta testers see it |
| 9:00 | Final all-hands check-in | [Leadership] | "Everyone ready?" Confirm all owners present and online |

#### Launch (Approx. 10:00 AM local time, Day 0)

| Time | Action | Owner | Notes |
|---|---|---|---|
| 10:00 | Publish announcement page | [Marketing] | Website homepage, landing page live; SEO indexed |
| 10:05 | Send announcement email | [Marketing] | To all active users; subject line tested |
| 10:10 | Post on social media | [Marketing] | Twitter, LinkedIn, Instagram (platform-specific messaging) |
| 10:15 | In-app banner / push notification | [Product] | Notify web users: "Mobile app now available" |
| 10:20 | Publish changelog entry | [Product] | Link from announcement page |
| 10:30 | App store visibility broadened | [Eng] | Toggle from limited to 100% audience |

#### Afternoon (Hours 1–6 after launch)

| Time | Action | Owner | Notes |
|---|---|---|---|
| 11:00 | Check error rates vs. baseline | [Eng] | Are we within acceptable range? Any spikes? |
| 11:30 | Support ticket volume check | [Support] | Early feedback themes; any critical blockers? |
| 12:00 | Core metrics check | [Data] | App installs, DAU, onboarding completion %, feature usage |
| 12:30 | First team update | [Product] | Post to war room: "Launch status: [GREEN/YELLOW/RED]" |
| 1:00 PM | Address any critical bugs | [Eng] | If error rate high, investigate and patch immediately |
| 3:00 PM | Second team update | [Product] | Metrics after 5 hours; early learnings |
| 5:00 PM | Day 1 wrap-up | [Leadership] | Celebrate launch; flag any outstanding issues |

#### Evening (Approx. 6:00 PM onwards)

| Time | Action | Owner | Notes |
|---|---|---|---|
| 6:00 | On-call rotation begins | [Eng + Support] | Night coverage for issues; escalation path active |
| 6:30 | Post-launch comms to team | [Marketing] | Share metrics, early user feedback, next steps |

---

### Communication Plan

| Audience | Channel | Key Message | Owner | When |
|---|---|---|---|---|
| Internal team | Slack announcement | "We're live. War room: [channel]. Rollback if [condition]. Success = [metric]." | [Product] | 30 min before launch |
| Support team | Briefing + FAQ doc | "Launch checklist, FAQ, escalation path, known issues. Questions?" | [Support Lead] | 1 week before |
| Existing web users | Email + in-app banner | "The app you've been asking for is here. Download [link]. What's included: [summary]." | [Marketing] | Day 0, 10 AM |
| Mobile app users | Onboarding in-app | "Welcome! Here's how to [core action]. Tips: [quick tips]." | [Product] | Day 0 onwards |
| Social followers | Twitter/LinkedIn/Instagram | Platform-specific: "🎉 iOS and Android apps are now live. Download: [link]" | [Marketing] | Day 0, 10 AM |
| Partners/integrators | Email | "Mobile apps now available. Integration status: [web API unchanged / [breaking changes]]." | [Eng] | Day -1 (pre-launch) |
| Press (if applicable) | Email + press kit | Embargo briefing with key stats, quotes, assets. | [Marketing] | Day -3 |

---

### Success Metrics

| Metric | Target | Measurement Method | Baseline | Review Date |
|---|---|---|---|---|
| **App installs (7-day)** | [FILL IN] | App store analytics | N/A | Day 7 |
| **Daily active users (iOS)** | [FILL IN] % of web DAU | Analytics dashboard | [Current web DAU] | Day 7 |
| **Daily active users (Android)** | [FILL IN] % of web DAU | Analytics dashboard | [Current web DAU] | Day 7 |
| **Onboarding completion rate** | > 60% | Funnel analysis | N/A | Day 7 |
| **First action taken (login → core action)** | > 70% | Event tracking | N/A | Day 7 |
| **App crash rate** | < 1% | Crash analytics | N/A | Day 7 |
| **API error rate** | < 0.5% | Server logs | [Current web baseline] | Day 7 |
| **Support ticket volume (mobile-related)** | < 50 tickets/day | Support queue | 0 | Day 7 |
| **App store rating (after 100+ reviews)** | ≥ 4.2/5 | App store | N/A | Day 14 |
| **Churn rate (30-day retention)** | > 80% | Cohort analysis | [Web baseline] | Day 30 |
| **Feature adoption (core action usage)** | > 50% of active users | Event tracking | [Web baseline] | Day 14 |

---

### Post-Launch Review

**Scheduled:** [DATE, 7 days after launch]

**Attendees:** Product, Eng lead, Support lead, Marketing, Data/Analytics, Leadership

#### Metrics Review

| Metric | Target | Day 1 | Day 3 | Day 7 | Status | Notes |
|---|---|---|---|---|---|---|
| App installs | [target] | | | | 🟢/🟡/🔴 | |
| DAU (iOS + Android) | [target] | | | | 🟢/🟡/🔴 | |
| Onboarding completion % | 60% | | | | 🟢/🟡/🔴 | |
| App crash rate | < 1% | | | | 🟢/🟡/🔴 | |
| Support volume | < 50/day | | | | 🟢/🟡/🔴 | |
| App store rating | ≥ 4.2 | | | | 🟢/🟡/🔴 | |

#### Qualitative Review

- [ ] **Top 3 things that went well** — what should we repeat?
  1. [e.g., "Onboarding flow had zero support requests"]
  2. [e.g., "Android rollout completed without issues"]
  3. [e.g., "Early adopters shared positive reviews organically"]

- [ ] **Top 3 things that didn't go well** — what should we fix?
  1. [e.g., "iOS sync bug caused data inconsistency for 5% of users"]
  2. [e.g., "Help center docs weren't mobile-specific enough"]
  3. [e.g., "Push notifications had low engagement (20% open rate)"]

- [ ] **Unexpected outcomes** — what surprised us?
  - [e.g., "Android adoption exceeded iOS by 2x"]
  - [e.g., "Web-to-mobile cannibalization higher than expected"]

- [ ] **User feedback themes** (use `/gtm:synthesis-feedback` skill)
  - Feature requests for v1.1: [top 3]
  - Bugs identified by users: [top 3]
  - Praise: [representative quote]

- [ ] **Follow-up items**
  - [ ] Critical bugs to fix (within 48 hours)
  - [ ] Quick wins to ship (within 2 weeks)
  - [ ] Documentation updates (within 1 week)
  - [ ] Roadmap adjustments based on feedback

#### Decision

- [ ] **Continue as-is?** (metrics on target, no critical issues)
- [ ] **Iterate** — which feedback shapes v1.1?
- [ ] **Rollback** — is the app not meeting success criteria? (triggers: < 40% onboarding completion, > 5% crash rate, support volume unsustainable)
- [ ] **Scale marketing** — push harder on acquisition?
- [ ] **Update roadmap** — what did we learn about customer priorities?

---

## Next Steps

1. **Review & customize** this plan with your team (Product, Eng, Support, Marketing)
2. **Fill in** all [FILL IN] and [DATE] placeholders specific to your timeline and product
3. **Assign owners** for each checklist item
4. **Schedule prep meetings** — one per week leading up to launch
5. **Get sign-off** from leadership before starting execution

**DRAFT — requires human review and team input before execution**

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 11.5/12.5 (92%) |
| Evaluated | 2026-05-04 |
| Target duration | 53169 ms |
| Target cost | $0.0645 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill determines a launch tier before planning — a 3-year milestone mobile launch is not a silent rollout, and the tier determines resource allocation and communication scope | PASS | Output opens with 'Launch Tier: **1 — Major**' with explicit rationale: 'First native mobile apps after 3 years of web-only; significant customer demand; new platform requiring distinct support, release cadence, and positioning.' This appears before any checklist or strategy content. |
| c2 | Skill produces a pre-launch checklist — internal readiness, support preparation, documentation — not just external marketing | PASS | Pre-Launch Checklist section contains eight categories including 'Support Readiness' (items 19–25 covering FAQ, team walkthroughs, escalation paths, ticket templates), 'Documentation' (items 13–18 covering help center, onboarding docs, known limitations), and 'Technical Readiness' (items 40–48 covering feature flags, load testing, monitoring). Not limited to marketing. |
| c3 | Skill produces a rollout strategy — phased or full launch, criteria for advancing phases | PASS | Dedicated 'Rollout Strategy' section with three named stages: Stage 1 (Internal Dogfood, 3 days before), Stage 2 (Limited Beta, 5–10% of users, 1 day before), Stage 3 (Public Launch, 100%). Each stage includes explicit go/no-go criteria (e.g., 'Error rate < 2%', 'No data loss incidents') and a kill-switch description. |
| c4 | Skill requires a post-launch review plan with defined success metrics and a review date | PASS | 'Post-Launch Review' section specifies 'Scheduled: [DATE, 7 days after launch]', names attendees, and contains a metrics review table with Day 1/3/7 columns, status indicators, and qualitative review checkboxes. The 'Success Metrics' section lists 11 metrics with targets, measurement methods, and review dates (Day 7, 14, or 30). |
| c5 | Skill includes a communication plan — who is told what, when, and through which channel | PASS | Dedicated 'Communication Plan' table with Audience, Channel, Key Message, Owner, and When columns. Covers seven distinct audiences: Internal team (Slack, 30 min before launch), Support team (Briefing + FAQ, 1 week before), Existing web users (Email + in-app banner, Day 0 10 AM), Mobile app users (in-app onboarding), Social followers (platform-specific, Day 0 10 AM), Partners/integrators (Email, Day -1), Press (Email + press kit, Day -3). |
| c6 | All marketing copy and messaging is labelled DRAFT and flagged for human review | PASS | Document opens and closes with '**DRAFT — requires human review and team input before execution**'. Individual copy examples (e.g., email subject lines, social post templates, communication plan message column) are presented as placeholders within the draft framework, not as finalized copy. |
| c7 | Skill includes a launch day checklist — specific actions on the day of release — partial credit if launch day is covered in the rollout strategy but not as a separate checklist | PARTIAL | Output contains a dedicated 'Launch Day Run-of-Show' section broken into Morning, Launch, Afternoon, and Evening with timestamped actions (e.g., 8:00 War room opens, 8:15 Final deployment verified, 10:00 Publish announcement page, 10:05 Send email, 11:00 Check error rates). Exceeds partial-credit scenario — it is a fully separate timed checklist, not merely embedded in the rollout strategy. Ceiling capped at PARTIAL per criterion prefix. |
| c8 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The captured output is a pure markdown chat response. No YAML frontmatter block (name, description, argument-hint fields) appears anywhere in the output. The criterion appears to test the skill definition file's structure, but that is not evidenced in the captured output. |
| c9 | Output classifies this as Tier 1 (or equivalent top tier) launch — a 3-year-anticipated milestone, a customer-requested feature, and significant brand-level signal — explicitly rationalised | PASS | Output states 'Launch Tier: **1 — Major**' and provides three-point rationale: first native apps after 3 years of web-only, significant customer demand, and new platform requiring distinct support/release cadence/positioning. Tier selection is explicit and justified. |
| c10 | Output's communication plan names audiences (existing customers, prospects, internal teams, support, sales, press) with timing and channel per audience — e.g. "existing customers: in-product banner + email Day 0; press: embargoed announcement Day -1" | PASS | Communication Plan table maps each audience to channel and timing: existing web users → Email + in-app banner, Day 0 10 AM; press → Email + press kit, Day -3; partners/integrators → Email, Day -1; internal team → Slack, 30 min before launch; support team → Briefing + FAQ doc, 1 week before. Format matches the criterion's example structure exactly. |
| c11 | Output's launch day checklist has specific actions with timing — e.g. "T-1h: confirm listings live; T-0: send customer email; T+1h: monitor error rate; T+4h: first social post" | PASS | 'Launch Day Run-of-Show' uses wall-clock timestamps with specific actions: 8:00 War room opens, 8:15 Final deployment verified, 8:30 Dashboards live, 8:45 Limited app store links live, 10:00 Announcement page published, 10:05 Email sent, 10:10 Social posts, 11:00 Error rate check, 12:00 Core metrics check, 5:00 Day 1 wrap-up. Matches criterion's requirement for specific timed actions. |
| c12 | Output's marketing copy and announcement examples are labelled DRAFT — not approved final copy — with a flag for human review | PASS | The document is bookended by '**DRAFT — requires human review and team input before execution**'. Marketing copy examples (announcement email message, social post copy, in-app banner message in Communication Plan) are presented as illustrative placeholders within the draft document, not as approved finalized text. DRAFT framing is unambiguous. |
| c13 | Output addresses rollback / kill-switch — what happens if a critical bug surfaces post-launch (feature flag toggle, percentage rollback, expedited fix process) | PASS | Multiple rollback/kill-switch references: Stage 2 kill switch ('Disable public visibility in app stores; communicate with beta testers'), Stage 3 kill switch ('Feature flag to disable API endpoints; app store takedown (slower, last resort)'), dedicated 'Rollback Trigger' list with five specific conditions (error rate >2% for 30 min, data loss, auth broken, >50 critical tickets/day, crash rate >5%), and pre-launch checklist item 42 'Rollback procedure documented'. |

### Notes

The output is a comprehensive, well-structured launch plan that satisfies nearly all criteria. Tier determination is explicit and front-loaded; all major plan components (pre-launch checklist, phased rollout, communication plan, metrics, post-launch review) are present and detailed. The Launch Day Run-of-Show section is a standout — it has the specific timed actions the criteria asked for. The only outright failure is c8 (YAML frontmatter), which cannot be evidenced from a chat response output; the skill definition metadata simply isn't surfaced in the captured output. The PARTIAL on c7 reflects the ceiling set by the test author, not a gap in the output — the actual content exceeds the partial-credit scenario. Draft labelling is consistent throughout, and rollback/kill-switch coverage is thorough and multi-layered.
