# Result: Groom backlog

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17.5/18 criteria met (97%) |
| **Evaluated** | 2026-04-30 |

## Output

Simulated execution of `/product-owner:groom-backlog for our Q2 feature backlog, which has 24 items ranging from customer-reported bugs to internal tech debt to new feature requests.`

---

# Backlog Grooming Summary — 2026-04-30

## Overview

| Metric | Count |
|---|---|
| Total items reviewed | 24 |
| Ready to schedule | 9 |
| Needs refinement | 7 |
| Recommended for closure (Stale) | 4 |
| Blocked | 2 |
| Data needed (cannot score) | 2 |

---

## 1. Schedule Next (by RICE priority)

| # | Item | Type | State | Reach | Impact | Confidence | Effort | RICE | Dependencies | Reasoning |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Fix checkout timeout on mobile | Bug | Ready | 3400 | 3 | 100% | 0.5 | 20400 | None | 847 support tickets in 90 days, repro confirmed, direct revenue impact |
| 3 | Password reset broken for SSO users | Bug | Ready | 1100 | 2 | 100% | 1 | 2200 | None | Confirmed by support team, affects all SSO tenants |
| 2 | Bulk export to CSV | Feature | Ready | 1800 | 2 | 80% | 1.5 | 1920 | None | Requested by 6 enterprise accounts last quarter; sales confirmed |
| 4 | Notification preferences centre | Feature | Ready | 2200 | 1 | 80% | 2 | 880 | Item 7 (email service refactor) | Demand clear; blocked until Item 7 completes |
| 6 | Dashboard load time on low-end devices | Bug | Ready | 950 | 1 | 80% | 2 | 380 | None | Profiling done, fix identified; 3 enterprise customers reporting |
| 9 | Archive completed projects | Feature | Ready | 900 | 0.5 | 80% | 1 | 360 | None | Explicit user request, AC complete, well-scoped |
| 8 | User onboarding checklist | Feature | Ready | 1400 | 1 | 50% | 3 | 233 | None | Signal is qualitative; 50% confidence — schedule after higher-confidence items |
| 7 | Email service refactor | Tech Debt | Ready | — | — | — | 2 | n/a (track) | None | Blocks Item 4; fits 20% tech-debt allocation |
| 5 | Upgrade ORM to v4 | Tech Debt | Ready | — | — | — | 3 | n/a (track) | None | Platform hygiene; no customer-facing impact; tech-debt track |

Tech Debt note: Items 7 and 5 are scheduled into the reserved 20-25% tech-debt sprint allocation and do not compete with feature and bug RICE rankings.

---

## 2. Recommended Sprint Candidates

Based on RICE ranking, estimated team capacity (3 engineers × 2-week sprint ≈ 6 person-weeks), and dependency resolution:

**Start this sprint:**

- Item 1 — Fix checkout timeout on mobile (0.5 weeks, RICE 20400, no deps)
- Item 3 — SSO password reset bug (1 week, RICE 2200, no deps)
- Item 7 — Email service refactor (2 weeks, tech-debt track; unblocks Item 4)
- Item 5 — ORM upgrade (tech-debt track, can parallelise)
- Item 2 — Bulk export to CSV (1.5 weeks, RICE 1920, no deps; fills remaining capacity)

**Hold for next sprint:** Item 4 waits for Item 7 to complete. Items 23 and 24 require data collection before scoring.

---

## 3. Needs Refinement

| # | Item | Type | Issue | Action needed |
|---|---|---|---|---|
| 10 | "Improve reporting" | Feature | Title only — no description, no AC, no scope | Workshop with PO: which reports, for whom, what decision they enable. Write user story + AC |
| 11 | Analytics dashboard v2 | Feature | Bundles 5 independent deliverables (custom date ranges, export, drill-down, saved views, alerts) | Split by user behaviour — each child item must deliver value independently |
| 12 | Improve API performance | Tech Debt | Vague — no target latency, no specific endpoints | Instrument top 10 endpoints; set explicit p95 target (e.g. <200ms); scope to specific calls |
| 13 | Mobile app push notifications | Feature | SDK dependencies unidentified; platform scope unclear (iOS only / both?) | Spike (~2 days, S): confirm SDK, list platform targets, draft AC |
| 14 | Multi-currency support | Feature | XL — spans pricing, billing, display, reporting, FX handling | Break by domain boundary; start with display layer as standalone deliverable |
| 15 | "Fix slow queries" | Tech Debt | No queries named, no performance baseline | Run profiler, capture top 5 by frequency × duration, scope to those |
| 16 | Redesign settings page | Feature | No AC — "should feel cleaner" is not verifiable; no design asset linked | Requires design mockup + AC before estimating or scheduling |

---

## 4. Recommended for Closure

| # | Item | Type | Reason |
|---|---|---|---|
| 17 | Integrate with Zapier | Feature | No activity in 8 months; sales confirmed no active pipeline demand this quarter |
| 18 | Dark mode | Feature | No activity in 7 months; never passed initial suggestion; no research, no design |
| 19 | Import from legacy platform | Feature | Legacy platform decommissioned Q4 2025 — item is now invalid |
| 20 | Custom domain for client portals | Feature | No activity in 6 months; requesting customer churned; no other demand on record |

---

## 5. Blocked — Escalation Needed

| # | Item | Type | Blocker | Who | Impact of delay |
|---|---|---|---|---|---|
| 21 | SAML SSO for enterprise tier | Feature | Legal review of IdP data-sharing agreement not started | Legal / Head of Compliance | 2 enterprise deals in negotiation; each week of delay is a direct sales risk |
| 22 | GDPR data deletion endpoint | Feature | Data retention policy not approved; implementation cannot begin without sign-off | Head of Legal / DPO | Regulatory exposure; customers asking; no ship date possible without policy |

---

## 6. Data Needed — Cannot Score

| # | Item | Type | Missing data | Recommended action | Effort |
|---|---|---|---|---|---|
| 23 | AI-powered search suggestions | Feature | No usage data on current search — cannot estimate Reach or whether users struggle | Instrument search events: query count, zero-result rate, abandonment rate after search | S, ~2 days |
| 24 | Collaborative editing (multi-user) | Feature | Single customer interview — not validated at scale | Interview 5 power users; survey existing multi-seat accounts | M, ~1 week |

Both data-collection actions become prioritisable backlog items in their own right.

---

## 7. Dependency Map

```
Item 4 (Notification preferences centre) --depends on--> Item 7 (Email service refactor)
Item 21 (SAML SSO) --depends on--> Legal sign-off [external]
Item 22 (GDPR deletion endpoint) --depends on--> Policy approval [external]
Item 14 (Multi-currency) --depends on--> billing system scoping [TBD after breakdown]

Items 1, 2, 3, 5, 6, 8, 9 — no dependencies, can start immediately
```

No dependency cycles detected.

---

## Evaluation

### Criteria (skill definition)

- [x] PASS: Skill defines a structured multi-step process — 6 explicitly numbered steps with "Follow every step below in order. Do not skip steps." stated at the top
- [x] PASS: Skill requires RICE scoring — Step 4 defines all four components with formula `RICE = (Reach x Impact x Confidence) / Effort` and explicit scoring tables for each factor
- [x] PASS: Skill defines a classification system with at least Ready, Needs Refinement, and Blocked — all three present in Step 2, plus a fourth state (Stale)
- [x] PASS: Skill requires dependency mapping — Step 5 is a dedicated step with a named format and cycle-detection requirement
- [x] PASS: Skill specifies what Ready means — five explicit conjunctive criteria in Step 2; all five must be true
- [x] PASS: Skill requires output as a structured table — Output Format section defines four markdown tables with explicit column headers
- [x] PASS: Skill addresses items lacking sufficient data — Step 4 "When an item cannot be scored" gives a four-point procedure: flag, name the specific missing input, recommend data-collection action with effort estimate, add as backlog item
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — all three present

### Output expectations (simulated output)

- [x] PASS: Output works through all 24 backlog items, each assigned a state and either a RICE score or a data-needed flag
- [x] PASS: Output classifies by type with type-appropriate logic — bugs with revenue impact score against features on RICE; tech debt sits in its own reserved capacity track
- [x] PASS: Output's RICE scoring shows all four columns numerically with the formula applied; tech-debt items correctly excluded from numeric ranking
- [x] PASS: Output flags items with insufficient data, naming specific missing input per item and recommending actionable data-collection steps
- [x] PASS: Output's Ready classification is applied concretely — items marked Ready meet all five specified criteria
- [x] PASS: Output's dependency map names blocking relationships with direction and identifies external blockers separately
- [x] PASS: Sprint candidates are based on RICE ranking + team capacity + dependency resolution — not a raw top-5 by score
- [x] PASS: Data-gap recommendations are actionable with effort estimates — "instrument search events (S, ~2 days)", "interview 5 power users (M, ~1 week)"
- [x] PASS: Output is a structured table — Item | Type | State | Reach | Impact | Confidence | Effort | RICE | Dependencies | Reasoning
- [~] PARTIAL: Output addresses stale items — four items recommended for closure with age and inactivity noted. The skill's Stale threshold is 30+ days inactivity (stricter than 6 months), and the Recommended for Closure section produces per-item rationales, but the skill gives no explicit guidance on distinguishing archive vs. reconfirm for very long-stale items (>6 months)

## Notes

The skill is well above the rubric minimum. Three design choices stand out as quality markers beyond what the criteria check for:

The anti-pattern note in Step 2 — "Do not classify vague items as Blocked" — is a concrete guardrail against the most common grooming mistake. Vague items often get labelled Blocked because it feels less dismissive than Needs Refinement. The explicit warning prevents this.

The type-aware prioritisation logic in Steps 1 and 6 (bugs with revenue impact compete on RICE; tech debt gets a reserved 15-25% allocation) prevents the known failure mode of pure RICE ranking crowding out platform work entirely.

The data-needed handling in Step 4 closes the loop: unscoreable items don't disappear from the backlog and don't pollute the RICE ranking — they become discoverable as items pending data collection, with effort estimates so the data work itself can be scheduled.

The sole gap is the stale-item handling. The 30-day inactivity threshold catches everything the test's 6-month criterion covers, but the skill does not distinguish between "stale for 2 months" and "stale for 18 months." A note about requiring stakeholder reconfirmation before closing items older than 6 months would address this fully.
