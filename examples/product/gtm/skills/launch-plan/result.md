# Result: Launch plan

**Verdict:** PASS
**Score:** 13/13 criteria met (100%)
**Evaluated:** 2026-04-30

---

## Output

> DRAFT — requires human review

## Launch Plan: Native iOS & Android Apps

### Launch Tier: 1 — Major

**Rationale:** This is a new product surface (native mobile) that follows 3 years of web-only delivery, directly answers long-standing customer requests, and carries significant brand signal. Maps unambiguously to Tier 1: "New product, major feature." 4–8 weeks prep required.

---

### Pre-Launch Checklist

#### Positioning and messaging (Tier 1 required)

| # | Item | Owner | Due | Status |
|---|---|---|---|---|
| 1 | One-sentence description written | Head of Product | T-28d | Pending |
| 2 | Target audience defined | Head of Product | T-28d | Pending |
| 3 | Key benefit articulated (not features — why customers care) | Head of Product | T-28d | Pending |
| 4 | Positioning approved by stakeholders | CPO | T-21d | Pending |
| 5 | Positioning canvas completed (`/gtm:positioning`) | GTM Lead | T-21d | Pending |

#### Landing page / announcement (Tier 1 required)

| # | Item | Owner | Due | Status |
|---|---|---|---|---|
| 6 | Announcement page drafted and reviewed | GTM Lead | T-14d | Pending |
| 7 | Hero copy finalised — headline, subhead, CTA | Copywriter | T-14d | Pending |
| 8 | App Store screenshots and demo video created | Design | T-14d | Pending |
| 9 | SEO metadata set (title, description, OG tags) | GTM Lead | T-10d | Pending |
| 10 | App Store listings copy drafted (iOS + Android separately) | Copywriter | T-14d | Pending |
| 11 | Landing page live behind preview URL | Engineering | T-7d | Pending |

#### Documentation (all tiers)

| # | Item | Owner | Due | Status |
|---|---|---|---|---|
| 12 | Mobile user documentation written (help centre) | Tech Writer | T-10d | Pending |
| 13 | Changelog entry drafted | GTM Lead | T-3d | Pending |
| 14 | Known limitations documented (e.g., features not yet on mobile) | Product | T-10d | Pending |

#### Support readiness (Tier 1 required)

| # | Item | Owner | Due | Status |
|---|---|---|---|---|
| 15 | FAQ document created — top 10 anticipated questions | Support Lead | T-14d | Pending |
| 16 | Support team briefed with walkthrough (iOS + Android) | Support Lead | T-7d | Pending |
| 17 | Escalation path defined for crash reports and App Store issues | Engineering Lead | T-7d | Pending |
| 18 | Known issues list shared with support | Product | T-3d | Pending |
| 19 | KB articles drafted for common tasks | Support Lead | T-7d | Pending |
| 20 | Support staffing plan for launch day (extended coverage) | Support Lead | T-5d | Pending |

#### Email (Tier 1 required)

| # | Item | Owner | Due | Status |
|---|---|---|---|---|
| 21 | Announcement email drafted (subject line + single CTA) | GTM Lead | T-10d | Pending |
| 22 | Email segments defined (all customers vs. mobile-request waitlist first?) | GTM Lead | T-10d | Pending |
| 23 | Email tested — rendered correctly, links working | GTM Lead | T-2d | Pending |
| 24 | Send scheduled — avoid Monday/Friday, timezone-appropriate | GTM Lead | T-2d | Pending |

#### Social media (Tier 1 required)

| # | Item | Owner | Due | Status |
|---|---|---|---|---|
| 25 | Social posts drafted per platform (LinkedIn, X, Instagram, Facebook — not a copy-paste) | GTM Lead | T-7d | Pending |
| 26 | Visual assets created — App Store badge, phone mockups, short demo GIF | Design | T-7d | Pending |
| 27 | Thread / post-launch content planned — tips, use cases, customer stories | GTM Lead | T-5d | Pending |

#### Analytics and tracking (all tiers)

| # | Item | Owner | Due | Status |
|---|---|---|---|---|
| 28 | Success metrics defined with specific numbers (see metrics table below) | Product | T-14d | Pending |
| 29 | Tracking events implemented (installs, activations, session depth, feature usage) | Engineering | T-7d | Pending |
| 30 | Mobile dashboard created (separate from web dashboard) | Data | T-7d | Pending |
| 31 | Baseline captured for web metrics to compare against | Data | T-7d | Pending |

#### Technical readiness (all tiers)

| # | Item | Owner | Due | Status |
|---|---|---|---|---|
| 32 | App Store listings submitted and approved (iOS review typically 24–72h) | Engineering | T-5d | Pending |
| 33 | Feature flags configured for any staged rollout via phased release (App Store supports this) | Engineering | T-5d | Pending |
| 34 | Gradual rollout plan defined — App Store phased release % schedule | Engineering | T-5d | Pending |
| 35 | Rollback procedure documented — expedited hotfix process, App Store revert path | Engineering Lead | T-7d | Pending |
| 36 | Load testing completed — expect spike from 3 years of pent-up demand | Engineering | T-7d | Pending |
| 37 | Monitoring and alerting configured for crash rate, API errors, auth flows | Engineering | T-5d | Pending |
| 38 | Error budget assessed — acceptable crash-free session rate for launch | Engineering Lead | T-7d | Pending |

---

### Rollout Strategy

**Strategy: Phased release (App Store) + Beta → GA**

Risk is medium-high — 3 years of pent-up demand means real traffic on day one. App Store phased release limits exposure while the team monitors stability.

```
Rollout plan for iOS & Android Apps:

- T-14d: Internal team dogfood (TestFlight / internal track)
- T-7d: Beta group — customers who requested mobile (invite via email)
- T-0 (Launch Day): App Store phased release begins at 10% of new downloads
- T+2d: Advance to 25% if crash-free rate > 99.5% and support tickets < 15/day
- T+5d: Advance to 50% if metrics stable
- T+7d: 100% — full public availability + public announcement

Kill switch: App Store phased release pause (immediate — no deploy required)
Rollback trigger: crash-free session rate drops below 99%, or support tickets exceed 30/day
```

**Note:** iOS App Store phased releases cannot be feature-flagged out of the app — if a critical bug surfaces, the rollback path is pausing the phased release and issuing an expedited hotfix submission. Engineering must have a hotfix pipeline ready to submit within 4 hours.

---

### Launch Day Run-of-Show

| Time | Action | Owner | Notes |
|---|---|---|---|
| 07:00 | Confirm App Store listings are live and correct (iOS + Android) | Engineering Lead | Check both stores, both regions |
| 07:15 | Smoke test on iOS and Android: install, login, core flows | QA Lead | At least 3 devices per platform |
| 07:30 | Open monitoring dashboard | Engineering | Crash rate, API error rate, auth errors |
| 07:45 | Open war room channel | GTM Lead | #launch-mobile-apps in Teams |
| 07:50 | Confirm all team members online | Engineering Lead | Engineering, Support, GTM |
| 08:00 | Set App Store phased release to 10% | Engineering | iOS App Store Connect |
| 08:05 | Publish landing page (remove preview lock) | Engineering | Confirm URL resolves |
| 08:10 | Send announcement email | GTM Lead | Confirm delivery via ESP |
| 08:15 | Post social — LinkedIn | GTM Lead | Check post renders correctly |
| 08:20 | Post social — X / Instagram / Facebook | GTM Lead | Platform-appropriate copy |
| 08:25 | Publish changelog entry | GTM Lead | — |
| 08:30 | Update in-app banner on web app | Engineering | "Now available on iOS and Android" |
| 09:00 | First status check — error rate vs baseline | Engineering Lead | Post to war room: green/yellow/red |
| 10:00 | Check support ticket volume | Support Lead | Is it within the expected range? |
| 11:00 | Read early user feedback — App Store reviews, social, support | GTM Lead | Capture verbatim positives and issues |
| 12:00 | Midday team sync — 15 minutes | Engineering Lead | Go/pause/rollback decision point |
| 14:00 | Second metrics check | Data | Installs, activations, session depth |
| 16:00 | First social follow-up post | GTM Lead | Tip or use case, not another announcement |
| 17:00 | End-of-day status report | Engineering Lead | Post to #launch-mobile-apps |
| EOD | Decide: advance to 25% tomorrow? | Engineering Lead | Gate: crash-free rate + support volume |

---

### Communication Plan

| Audience | Channel | Message | Owner | When |
|---|---|---|---|---|
| Internal team | Teams (#launch-mobile-apps) | "Launching iOS and Android today. War room: #launch-mobile-apps. Rollback plan: [link]." | Engineering Lead | T-0 morning (07:45) |
| Support team | Teams briefing + shared doc | FAQ, known issues, escalation paths, crash reporting procedure | Support Lead | T-7d (briefing) + T-1d (reminder) |
| Existing customers (mobile-request waitlist) | Email | "You asked for it — iOS and Android are here." — [CTA: Download] | GTM Lead | T-0 08:10 |
| All existing customers | Email | Announcement with download links and what's available on mobile | GTM Lead | T+2d (after stability confirmed) |
| Social followers | LinkedIn, X, Instagram, Facebook | Platform-appropriate launch posts | GTM Lead | T-0 08:15 |
| Press / analysts | Email embargo | Briefing deck, screenshots, key quotes — embargo lifted at 08:00 T-0 | GTM Lead | T-1d (embargo briefing) |
| Partners / integrators | Email | No breaking API changes; mobile-specific webhooks available; doc link | Engineering Lead | T-3d |

---

### Success Metrics

| Metric | Target | Measurement method | Review date |
|---|---|---|---|
| iOS installs (Day 7) | 15% of active web users | App Store Connect | T+7d |
| Android installs (Day 7) | 10% of active web users | Google Play Console | T+7d |
| Mobile activation rate (first session > 5 min) | > 60% of installs | Mobile analytics dashboard | T+7d |
| Crash-free session rate | > 99.5% | Crashlytics / Sentry | Daily T+1 through T+7 |
| Support tickets (mobile-related) | < 20/day by Day 3 | Support platform | T+3d, T+7d |
| App Store rating | > 4.0 by Day 7 | App Store Connect | T+7d |
| Email open rate (announcement) | > 35% | ESP dashboard | T+1d |

---

### Post-Launch Review

- **Scheduled:** T+7d (Wednesday 6 May — confirm with launch owner)
- **Attendees:** Head of Product, Engineering Lead, GTM Lead, Support Lead, Data Lead
- **Review template:** metrics vs targets (table above), user feedback themes, incidents and near-misses, App Store review sentiment, next 30-day mobile roadmap priorities

---

> DRAFT — requires human review

---

## Evaluation

### Criteria

- [x] PASS: Skill determines a launch tier before planning — Step 1 is an explicit tier classification table (Tier 1/2/3) that gates checklist scope. A 3-year milestone mobile launch maps unambiguously to Tier 1.
- [x] PASS: Skill produces a pre-launch checklist — Step 2 covers internal readiness (technical readiness section), support preparation, and documentation across all tiers.
- [x] PASS: Skill produces a rollout strategy — Step 3 provides five named strategies with risk levels and a documented plan template including kill switch and rollback trigger fields.
- [x] PASS: Skill requires a post-launch review plan with defined success metrics and a review date — Step 6 is a 7-day review with a metrics table structure, and Step 7 mandates a scheduled date in every output.
- [x] PASS: Skill includes a communication plan — Step 5 maps six audiences (internal team, support, existing users, social, partners, press/analysts) to channel, timing, and message.
- [x] PASS: All marketing copy and messaging is labelled DRAFT — Rules section states "All output is DRAFT until human-reviewed. Label every output with 'DRAFT — requires human review' at the top and bottom."
- [x] PASS: Skill includes a launch day checklist as its own step (Step 4), structured as a sequential run-of-show with morning/launch/afternoon blocks.
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields at lines 1–7.

### Output expectations

- [x] PASS: Output classifies this as Tier 1 with explicit rationale — rationale names the three factors (new surface, 3-year wait, customer-requested) and maps to the Tier 1 definition.
- [x] PASS: Output's communication plan names distinct audiences with channel, timing, and message — existing customers split into waitlist (Day 0) and full list (Day +2), press has embargo, internal team has war room channel.
- [x] PASS: Output's launch day checklist has specific actions with clock times — T-relative wall-clock times from 07:00 to EOD, each row has owner and notes.
- [x] PASS: Output's marketing copy and announcement examples are labelled DRAFT — top and bottom DRAFT banners present per the Rules requirement.
- [x] PASS: Output addresses rollback/kill-switch — rollback trigger defined in rollout strategy (crash-free rate < 99% or tickets > 30/day), and the note explicitly describes the App Store phased release pause path and hotfix pipeline requirement.

## Notes

The skill is a well-structured generic launch framework. All structural criteria are met cleanly.

The simulated output adds mobile-specific detail the skill itself doesn't mandate (App Store phased release mechanics, TestFlight, Crashlytics, platform-split install targets). The skill is intentionally platform-agnostic, so those additions come from applying the framework to the scenario rather than from explicit skill instructions. This is appropriate — the skill's generic structure produces the right output shape; the scenario fills the specifics.

One minor observation: the skill's launch day run-of-show uses time blocks (morning/launch/afternoon) rather than explicit wall-clock times. The output format template shows `[HH:MM]` placeholders, which is close enough that a practitioner would naturally produce timestamped actions. The criterion passes because the structure is present and clock times are the natural interpretation of the format.
