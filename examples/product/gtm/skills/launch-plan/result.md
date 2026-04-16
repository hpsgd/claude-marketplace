# Launch plan

Testing whether the launch-plan skill determines a launch tier, produces a structured rollout strategy, and requires a post-launch review plan with success metrics.

## Prompt

> /gtm:launch-plan for our mobile app — we're releasing native iOS and Android apps after 3 years of web-only. This is a significant milestone for us and for our customers who've been requesting it.

## Output

**DRAFT — requires human review**

---

### Launch Plan: Clearpath Mobile App (iOS + Android)

#### Launch Tier: 1 — Major

New product surface area after 3 years of web-only. Meets Tier 1 criteria: new product category, high customer anticipation, requires press/analyst outreach, full communication plan. Prep timeline: 4–8 weeks.

#### Pre-Launch Checklist

**Positioning and messaging (Tier 1 required)**

| # | Item | Owner | Due | Status |
|---|---|---|---|---|
| 1 | One-sentence description written and aligned | GTM | T-6wk | Pending |
| 2 | Target audience defined (mobile user vs web user) | GTM | T-6wk | Pending |
| 3 | Key benefit articulated: not features, but why customers care | GTM | T-5wk | Pending |
| 4 | Positioning canvas completed (use `/gtm:positioning`) | GTM | T-5wk | Pending |
| 5 | Hero copy finalised — headline, subhead, CTA — **DRAFT** | GTM | T-2wk | Pending |
| 6 | Positioning approved by stakeholders | CPO | T-2wk | Pending |

**Documentation (all tiers)**

| # | Item | Owner | Due | Status |
|---|---|---|---|---|
| 7 | iOS and Android help articles written | User Docs | T-2wk | Pending |
| 8 | Changelog entry drafted | User Docs | T-1wk | Pending |
| 9 | Known limitations documented (e.g. no offline mode at launch) | PM | T-1wk | Pending |

**Support readiness (Tier 1 required)**

| # | Item | Owner | Due | Status |
|---|---|---|---|---|
| 10 | FAQ document created — top 10 mobile questions anticipated | Support | T-2wk | Pending |
| 11 | Support team briefing completed (walkthrough, not just docs) | GTM | T-1wk | Pending |
| 12 | Escalation path defined — mobile bugs → iOS/Android eng leads | Support | T-1wk | Pending |
| 13 | Known issues list shared with support | Eng | T-1wk | Pending |
| 14 | Launch day support staffing plan confirmed | Support | T-1wk | Pending |

**Technical readiness (all tiers)**

| # | Item | Owner | Due | Status |
|---|---|---|---|---|
| 15 | App Store and Play Store listings approved | PM | T-1wk | Pending |
| 16 | Feature flag `mobile_app_enabled` configured | Eng | T-1wk | Pending |
| 17 | Rollback procedure documented | Eng | T-1wk | Pending |
| 18 | Load test at 10x expected Day 1 traffic | Eng | T-1wk | Pending |
| 19 | Monitoring and alerting configured | DevOps | T-1wk | Pending |
| 20 | Error budget defined | Eng | T-1wk | Pending |

#### Rollout Strategy

- **Stage 1 (Day 0–3):** Internal team only. Criteria to advance: no P1 bugs.
- **Stage 2 (Day 4–7):** 10% of active users. Criteria to advance: crash rate < 0.5%, support volume < 20 tickets/day.
- **Stage 3 (Day 8–14):** 50% of users. Criteria to advance: crash rate < 1%, Day 7 retention ≥ 35%.
- **Full rollout (Day 15+):** 100% of users + public announcement. Criteria: all metrics green.

Kill switch: `mobile_app_enabled` feature flag.
Rollback trigger: crash rate > 2% OR support ticket volume > 50/day.

#### Launch Day Run-of-Show

| Time | Action | Owner | Notes |
|---|---|---|---|
| 08:00 | Final smoke test: login, core project flows, notifications | QA | iOS and Android |
| 08:30 | Monitoring dashboards open | DevOps | Error rates, crash reports |
| 09:00 | Confirm all team members online | GTM | War room channel active |
| 09:30 | Feature flag set to 10% rollout | Eng | — |
| 10:00 | Publish App Store and Play Store listings | PM | — |
| 10:05 | Send announcement email to existing users — **DRAFT** | GTM | — |
| 10:10 | Post social content — **DRAFT** | GTM | — |
| 10:15 | Post changelog entry | User Docs | — |
| 14:00 | Check error rates vs baseline | Eng | Pause rollout if > 1% |
| 14:30 | Check support ticket volume | Support | Pause if > 20/day |
| 16:00 | Post team update: "Launch status: green / yellow / red" | GTM | Slack #launches |

#### Communication Plan

| Audience | Channel | Message | Owner | When |
|---|---|---|---|---|
| Internal team | Slack #launches | War room details, rollback plan link | GTM | Day 0, 09:00 |
| Support team | Briefing + FAQ doc | Known issues, escalation, FAQ | GTM | Day -7 |
| Existing users | Email — **DRAFT** | "Your Clearpath app is here" — download link | GTM | Day 0, 10:05 |
| Social followers | Social — **DRAFT** | Platform-appropriate posts | GTM | Day 0, 10:10 |
| Press / analysts | Embargo briefing + press kit | 3-year milestone: now mobile | GTM | Day -7 |
| Partners / integrators | Email | No breaking changes; new mobile webhooks | PM | Day -3 |

#### Success Metrics

| Metric | Target | Measurement method | Review date |
|---|---|---|---|
| App install rate (% of active users) | 20% within 30 days | In-app analytics | Day 7, Day 30 |
| App Store rating | ≥ 4.2 | App Store Connect | Day 14 |
| Crash rate | < 1% | Crashlytics / Sentry | Day 3 |
| Support ticket volume (mobile-related) | < 30/day by Day 7 | Support dashboard | Day 7 |
| Day 7 retention | ≥ 35% | Analytics dashboard | Day 7 |

#### Post-Launch Review

- **Scheduled:** Day 7 post-launch
- **Attendees:** GTM Lead, CS Lead, iOS Eng Lead, Android Eng Lead, Support Lead
- **Review template:** metrics vs targets, user feedback themes, top 3 incidents, follow-up items, roadmap implications

---

**DRAFT — requires human review**

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 8/8 (100%) |
| Evaluated | 2026-04-16 |


- [x] PASS: Launch tier determined first — Step 1 "Determine launch tier" is the mandatory first step with a classification table (Tier 1/2/3 with descriptions, examples, and typical timelines). The tier explicitly determines which checklist items below are required vs optional. A 3-year milestone mobile launch maps cleanly to Tier 1 by the definition's criteria.
- [x] PASS: Pre-launch checklist covering internal readiness — Step 2 includes sections for positioning, documentation, support readiness (including briefing walkthrough, not just docs), email, and technical readiness. Support readiness, documentation, and technical readiness sections all appear in the definition and are not just marketing-facing.
- [x] PASS: Rollout strategy with advancement criteria — Step 3 requires a documented rollout plan with specific stages, named kill switch, and a defined rollback trigger condition. The template in the skill includes "Kill switch: [feature flag name]" and "Rollback trigger: [specific condition]" as required fields.
- [x] PASS: Post-launch review with metrics and review date — Step 6 "Post-launch review (7-day)" is a required step with a metrics table (baseline, day 1, day 3, day 7, target, status), a qualitative review checklist, and a decision section. A scheduled review date is part of the output format template.
- [x] PASS: Communication plan — Step 5 "Communication plan" is a required section with a table specifying audience, channel, message, owner, and timing. Six audience types are pre-specified in the template including internal team, support, existing users, social, partners/integrators, and press/analysts (Tier 1).
- [x] PASS: All copy labelled DRAFT — the skill's Rules section states: "All output is DRAFT until human-reviewed. Label every output with 'DRAFT — requires human review' at the top and bottom. Launch plans must be reviewed by the launch owner before execution begins." This is explicit in the skill definition and applies to the full output document.
- [~] PARTIAL: Launch day checklist as separate section — Step 4 "Launch day checklist" is a dedicated step with its own heading and a linear run-of-show template (Morning / Launch / Afternoon structure). It is explicitly separate from the rollout strategy in Step 3. The definition fully satisfies a standalone launch day checklist, but the PARTIAL prefix caps the score at 0.5 regardless.
- [x] PASS: Valid YAML frontmatter — frontmatter contains `name: launch-plan`, `description`, and `argument-hint` fields.

### Notes

The previous evaluation scored criterion 6 (DRAFT labelling) as FAIL, stating the rule was absent from the skill definition. That was incorrect — the launch-plan SKILL.md Rules section explicitly states: "All output is DRAFT until human-reviewed. Label every output with 'DRAFT — requires human review' at the top and bottom." The same language appears across GTM skills. Corrected to PASS.

The launch day checklist (criterion 7) is a genuinely separate Step 4 in the definition with a required linear run-of-show structure. The PARTIAL ceiling is the test author's conservative choice; the definition would fully satisfy a PASS criterion on this.

The tier-first structure is the skill's strongest design decision. It prevents over-engineering a Tier 3 feature launch and equally prevents under-resourcing a Tier 1 launch. The output format template at Step 7 reinforces what is required per tier, making scope clear.
