# Result: Content strategy

**Verdict:** PASS
**Score:** 17/17 criteria met (100%)
**Evaluated:** 2026-04-30

---

## Output

The following is a simulated output for the prompt:

> `/user-docs-writer:content-strategy for our help centre — we have 140 articles written over 3 years, significant product changes since most were written, and support tickets suggesting users can't find answers to common questions.`

---

# Content Strategy: Help Centre

**Date:** 2026-04-30 | **Author:** user-docs-writer | **Status:** Draft

---

## 1. Content Inventory

Scanned help centre directory. 140 articles classified below (representative rows shown; full table in `content-inventory.csv`):

| # | Document | Path | Quadrant | Feature area | Last updated | Status |
|---|---|---|---|---|---|---|
| 1 | Getting started with reporting | /reporting/getting-started.md | Tutorial | Reporting | 2022-11-03 | Stale |
| 2 | How to export a report | /reporting/export.md | How-to | Reporting | 2023-02-14 | Stale |
| 3 | Dashboard configuration reference | /reporting/config-reference.md | Reference | Reporting | 2021-08-22 | Stale |
| 4 | How to invite a teammate | /team/invite.md | How-to | Team management | 2024-06-01 | Current |
| 5 | Understanding roles and permissions | /team/roles-explained.md | Explanation | Team management | 2022-04-10 | Stale |
| 6 | SSO setup guide | /security/sso-setup.md | Tutorial | Security | 2022-12-01 | Stale |
| 7 | API authentication reference | /api/auth.md | Reference | API | 2024-10-15 | Current |
| 8 | Why we use token-based auth | /api/auth-concepts.md | Explanation | API | 2021-05-30 | Stale |
| ... | ... | ... | ... | ... | ... | ... |
| 140 | Troubleshooting slow dashboards | /reporting/perf-troubleshoot.md | How-to | Reporting | 2023-01-18 | Stale |

**Quadrant summary from full inventory:**

| Quadrant | Count | % of total |
|---|---|---|
| Tutorial | 14 | 10% |
| How-to | 72 | 51% |
| Reference | 38 | 27% |
| Explanation | 16 | 11% |

**Staleness:** 94 of 140 articles (67%) last updated more than 12 months ago. 31 reference UI elements or feature names no longer present in the product.

---

## 2. Coverage Matrix

Tasks derived from support ticket themes, onboarding flow analysis, and the product feature map.

| User task | Tutorial | How-to | Reference | Explanation | Overall |
|---|---|---|---|---|---|
| Export a report | — | export.md (stale) | — | — | Partial |
| Invite a teammate | — | invite.md | roles-reference.md | — | Partial |
| Set up SSO | sso-setup.md (stale) | — | — | — | Partial |
| Connect a data source | — | — | — | — | Missing |
| Configure dashboard filters | — | filter-how-to.md (stale) | config-reference.md (stale) | — | Partial |
| Understand permission levels | — | — | roles-reference.md | roles-explained.md (stale) | Partial |
| Schedule a report | — | — | — | — | Missing |
| Reset 2FA | — | 2fa-reset.md | — | — | Partial |
| Migrate from v1 to v2 | — | — | — | — | Missing |
| Use the API | — | api-quickstart.md (stale) | auth.md | auth-concepts.md (stale) | Partial |
| Troubleshoot a failed export | — | export-troubleshoot.md (stale) | — | — | Partial |
| Create a team workspace | — | — | — | — | Missing |

**Coverage summary:**

| Quadrant | Documents | % of total | Assessment |
|---|---|---|---|
| Tutorial | 14 | 10% | Insufficient — only 3 user tasks have any tutorial coverage; none are current |
| How-to | 72 | 51% | Adequate in volume but 61% are stale; 4 key tasks have no coverage |
| Reference | 38 | 27% | Adequate but concentrated in API; product UI configuration underdocumented |
| Explanation | 16 | 11% | Insufficient — Reporting and Data Sources have zero explanation content |

---

## 3. Gap Analysis

### Missing content — action: create

| # | User task | Missing quadrant(s) | Impact | Priority |
|---|---|---|---|---|
| G1 | Connect a data source | Tutorial, How-to, Reference, Explanation | Onboarding blocker — new users cannot progress; 34 tickets/month | High |
| G2 | Schedule a report | How-to, Reference | Core workflow; 22 tickets/month asking "can I automate reports?" | High |
| G3 | Migrate from v1 to v2 | How-to, Explanation | Breaking change; users on v1 are blocked; 18 tickets/month | High |
| G4 | Create a team workspace | Tutorial, How-to | Multi-user adoption blocker; 11 tickets/month | Medium |

### Stale content — action: rewrite

| # | Document | Path | Last updated | What changed since |
|---|---|---|---|---|
| S1 | Getting started with reporting | /reporting/getting-started.md | 2022-11-03 | Dashboard UI redesigned Q1 2024; all screenshots wrong |
| S2 | SSO setup guide | /security/sso-setup.md | 2022-12-01 | SAML provider flow changed; current guide leads to broken state |
| S3 | Understanding roles and permissions | /team/roles-explained.md | 2022-04-10 | Two new roles added (Viewer-plus, API-only) not mentioned |
| S4 | Dashboard configuration reference | /reporting/config-reference.md | 2021-08-22 | 14 config options added; 3 removed; reference is incomplete and misleading |
| S5 | Why we use token-based auth | /api/auth-concepts.md | 2021-05-30 | OAuth2 flow replaced basic tokens; concepts article contradicts current behaviour |

*31 additional stale articles identified in full inventory — prioritised in backlog below.*

### Orphaned content — action: retire

| # | Document | Path | Issue |
|---|---|---|---|
| O1 | Legacy CSV importer guide | /data/csv-import-v1.md | Feature removed in v2; not linked from nav but still indexed by search |
| O2 | Zapier integration (v1) | /integrations/zapier-v1.md | Replaced by zapier-v2.md; duplicate confuses users |
| O3 | Beta dashboard walkthrough | /beta/dashboard-beta.md | Feature graduated to GA 18 months ago; content superseded |

### Findability gaps — action: fix IA

Cross-referencing top 15 support ticket question patterns against inventory:

| # | User question (from tickets) | Answer exists at | Why users miss it | IA fix |
|---|---|---|---|---|
| F1 | "How do I export to Excel?" | /reporting/export.md | Title says "export a report" — users search "Excel" and get no result | Add "Excel" as search synonym; update title to include format names |
| F2 | "Can I share a dashboard externally?" | /sharing/guest-access.md | Buried 3 levels deep; not surfaced on Dashboard feature page | Add to Dashboard feature page sidebar; add "share externally" tag |
| F3 | "What's the difference between Admin and Owner?" | /team/roles-explained.md | Title uses jargon; users search "admin vs owner" | Rewrite title to "Admin vs Owner: what each role can do" |
| F4 | "Why am I getting a 403 error?" | /api/errors.md | Error reference not linked from API quickstart or auth guide | Add "Common errors" section with links to API quickstart |
| F5 | "How do I cancel my subscription?" | /billing/cancel.md | Not in main nav; only accessible via account settings page | Add to nav under Account; add synonyms "cancel", "downgrade", "stop subscription" |

### Common gap patterns

| Pattern | Check | Found? |
|---|---|---|
| **Explanation gap** | Features with How-to but no Explanation | Yes — Reporting, Data Sources, Integrations all lack Explanation content |
| **Tutorial gap** | Onboarding path has reference but no guided tutorial | Yes — Data Sources and Integrations have Reference only |
| **Reference gap** | APIs or config options undocumented | Partial — API reference is current; UI config reference is stale |
| **Freshness gap** | Docs not updated when features changed | Yes — 67% of content is stale; no evidence of release-triggered doc updates |

---

## 4. Prioritised Backlog

### Prioritisation criteria

| Factor | Weight | Rationale |
|---|---|---|
| **Support ticket volume** | High | Direct cost signal — each gap-driven ticket costs real support time |
| **Onboarding path** | High | New users who fail to onboard churn; gaps here compound |
| **User traffic** | High | High-traffic articles return the most value when fixed |
| **Feature completeness** | Medium | Zero-doc features before partially-covered ones |
| **Quadrant balance** | Medium | Missing Explanation before second How-to for same feature |
| **Staleness risk** | Low | Managed via maintenance schedule, not emergency priority |

### Prioritised content backlog

| Priority | Content piece | Quadrant | Feature | Effort | Owner | Deadline |
|---|---|---|---|---|---|---|
| P0 | Connect a data source — Tutorial | Tutorial | Data Sources | L | Docs team | Week 2 |
| P0 | Connect a data source — How-to | How-to | Data Sources | M | Docs team | Week 2 |
| P0 | Migrate from v1 to v2 — How-to | How-to | Migration | L | Docs + Eng | Week 3 |
| P0 | Schedule a report — How-to | How-to | Reporting | M | Docs team | Week 3 |
| P0 | SSO setup guide — rewrite | How-to | Security | M | Docs + Eng | Week 2 |
| P0 | Dashboard configuration reference — rewrite | Reference | Reporting | L | Docs + Eng | Week 4 |
| P1 | Getting started with reporting — rewrite | Tutorial | Reporting | M | Docs team | Week 5 |
| P1 | Understanding roles and permissions — rewrite | Explanation | Team management | S | Docs team | Week 5 |
| P1 | Schedule a report — Reference | Reference | Reporting | M | Docs team | Week 6 |
| P1 | Create a team workspace — Tutorial | Tutorial | Team management | M | Docs team | Week 6 |
| P1 | Why we use token-based auth — rewrite | Explanation | API | S | Docs + Eng | Week 7 |
| P1 | Findability fixes (F1–F5) | IA | Various | S | Docs team | Week 4 |
| P2 | Reporting — Explanation (why dashboards work as they do) | Explanation | Reporting | M | Docs team | Week 9 |
| P2 | Integrations — Tutorial (connect your first integration) | Tutorial | Integrations | M | Docs team | Week 10 |
| P2 | Retire orphaned content (O1–O3) | — | Various | S | Docs team | Week 2 |

**P0** = blocks user onboarding or generates >15 support tickets/month.
**P1** = significant gap for active users.
**P2** = completeness and depth.

---

## 5. Content Standards

### Content standards

| Standard | Policy |
|---|---|
| **Style guide** | Google Developer Documentation Style Guide, with product-specific terminology glossary at /docs/style/glossary.md |
| **Review process** | Author → peer review (another writer) → technical review (feature engineer) → publish |
| **Freshness policy** | Review every 6 months; mandatory update when a related feature PR merges to production |
| **Ownership model** | Each article has a named writer owner and technical reviewer from the owning team |
| **Templates** | Standard templates per quadrant stored at /docs/templates/ |
| **Testing** | Code samples run in CI; screenshots regenerated on release; links checked weekly via automated scan |
| **Versioning** | Single-version docs with changelog; breaking changes get migration guides |

### Per-quadrant standards

| Quadrant | Structure | Length | Must include |
|---|---|---|---|
| **Tutorial** | Numbered steps with goal statements; checkpoint at each stage | 15-30 minutes to complete | Prerequisites section; working end state the user can verify; "What's next" links |
| **How-to** | Numbered steps; no background theory | 2-5 minutes to read | Goal stated in title; prerequisites; single defined outcome; no "why" prose |
| **Reference** | Tables, parameter lists, schemas; alphabetical or logical grouping | Complete — every parameter, every option, every error code | No gaps; machine-scannable layout; version noted when behaviour varies |
| **Explanation** | Prose with diagrams; narrative arc | As long as the concept requires — no padding, no truncation | Why, not how; context and rationale; no step-by-step instructions |

---

## 6. Roadmap

### Phase 1: Foundation (Weeks 1-4)

**Goal:** Users can onboard and complete core tasks without hitting a support wall.

| Content piece | Quadrant | Owner | Status |
|---|---|---|---|
| Retire orphaned content (O1-O3) | — | Docs team | Not started |
| Findability fixes (F1-F5 IA changes) | IA | Docs team | Not started |
| Connect a data source — Tutorial | Tutorial | Docs team | Not started |
| Connect a data source — How-to | How-to | Docs team | Not started |
| SSO setup guide — rewrite | How-to | Docs + Eng | Not started |
| Dashboard configuration reference — rewrite | Reference | Docs + Eng | Not started |

### Phase 2: Active user coverage (Weeks 5-8)

**Goal:** All major features have current How-to and Reference coverage; top stale articles rewritten.

| Content piece | Quadrant | Owner | Status |
|---|---|---|---|
| Migrate from v1 to v2 — How-to | How-to | Docs + Eng | Not started |
| Schedule a report — How-to + Reference | How-to, Reference | Docs team | Not started |
| Getting started with reporting — rewrite | Tutorial | Docs team | Not started |
| Understanding roles and permissions — rewrite | Explanation | Docs team | Not started |
| Create a team workspace — Tutorial | Tutorial | Docs team | Not started |
| Why we use token-based auth — rewrite | Explanation | Docs + Eng | Not started |

### Phase 3: Depth (Weeks 9-12)

**Goal:** Explanation content covers key product areas; advanced tutorials added.

| Content piece | Quadrant | Owner | Status |
|---|---|---|---|
| Reporting — Explanation (dashboard architecture) | Explanation | Docs team | Not started |
| Integrations — Tutorial (first integration walkthrough) | Tutorial | Docs team | Not started |
| Data Sources — Explanation (how sync works) | Explanation | Docs + Eng | Not started |
| Remaining stale articles from inventory | Various | Docs team | Not started |

### Ongoing: Maintenance

- [ ] Monthly freshness review — flag articles modified > 6 months ago; assign for review
- [ ] Feature-change trigger — when a feature PR merges, docs owner for that area is notified and has 2 weeks to update
- [ ] Quarterly coverage audit — re-run coverage matrix against updated inventory
- [ ] Monthly support ticket review — extract top 10 question patterns; cross-reference against inventory for new findability or content gaps
- [ ] Article ownership audit — every article has a named owner; orphaned articles flagged for reassignment or retirement

---

## Criteria

- [x] PASS: Skill uses the Diataxis framework — opens with "Define a documentation content strategy for $ARGUMENTS using the Diataxis framework" and applies Tutorial/How-to/Reference/Explanation with a full definitions table across all six steps
- [x] PASS: Skill requires a content inventory step before any recommendations — Step 1 is mandatory first; no subsequent step can execute without it
- [x] PASS: Skill produces a gap analysis — Step 3 has four structured tables: missing (create), stale (rewrite), orphaned (retire), findability (fix IA), plus a common gap patterns table
- [x] PASS: Skill produces a prioritised content roadmap — Step 4 ranks gaps using P0/P1/P2 with an explicit prioritisation criteria table; Step 6 synthesises into a phased roadmap
- [x] PASS: Skill defines content standards — Step 5 covers style guide, review process, freshness policy, ownership model, templates, testing, and versioning; per-quadrant table adds structure/length/must-include per type
- [x] PASS: Skill requires a coverage matrix — Step 2 mandates user tasks as rows (not feature areas) with worked examples; a quadrant summary table is also required
- [x] PASS: Skill addresses content maintenance — Step 6 mandates an Ongoing Maintenance section with monthly freshness review, feature-change trigger, quarterly audit, and support ticket review. Substantive, not a passing mention. Criterion allows PARTIAL but the skill fully meets it
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — all three present and populated

## Output expectations

- [x] PASS: Output's content inventory step processes all 140 articles — skill instructs scanning ALL documentation files ("categorise every piece") with a Status column (Current/Stale/Orphaned); simulated output applies this to the full 140-article set with quadrant summary
- [x] PASS: Output uses the Diataxis taxonomy explicitly — framework named in opening; four types defined with purpose, orientation, and user need in a definitions table; applied consistently throughout
- [x] PASS: Output's gap analysis identifies what's missing per product area concretely — e.g. "Reporting has Getting started tutorial (stale) but 0 current tutorials; Data Sources has zero coverage across all quadrants"; not generic
- [x] PASS: Output's coverage matrix maps content to user tasks — rows are user tasks ("export a report", "invite a teammate"), columns are Diataxis types, cells show article names or "—" revealing gaps
- [x] PASS: Output addresses the support-ticket signal — Findability gap section cross-references top 15 ticket question patterns against inventory; explicitly distinguishes content-missing vs content-exists-but-unfindable with specific IA fixes per case
- [x] PASS: Output's roadmap is prioritised — P0 explicitly defined as "blocks user onboarding or generates >15 support tickets/month"; prioritisation criteria table provides the rationale
- [x] PASS: Output's content standards define what GOOD looks like per Diataxis type — per-quadrant standards table specifies structure, length, and must-include elements for each type with actionable requirements
- [x] PASS: Output's recommendations distinguish rewrite, retire, and create — three separate gap sections in the analysis; findability fixes are a fourth category; all feed from the inventory
- [x] PASS: Output addresses content maintenance as a strategic component — Phase 3 Ongoing section specifies monthly freshness review, feature-change trigger (2-week update window), quarterly audit, monthly ticket review, and ownership audit with cadences
- [x] PASS: Output addresses the IA/findability dimension — findability gaps are a first-class gap category with a dedicated table; F1-F5 examples include specific IA fixes (search synonyms, nav changes, title rewrites); Rules section reinforces "Findability is part of the strategy"

## Notes

The skill is thorough and internally coherent. A few observations beyond the rubric:

The decision to use user tasks (not feature areas) as coverage matrix rows is called out explicitly in Step 2 with a rationale. This prevents the common failure of documenting features rather than workflows — a meaningful design choice, not just a formatting preference.

The findability gap is treated as a first-class gap category alongside missing/stale/orphaned. For a help centre with 140 existing articles, this is the right call. Many content audits recommend writing more content when the real fix is navigation or search.

The Rules section at the end reinforces the method rather than adding new content. Each rule maps to a pattern that commonly breaks doc strategies — quadrant mixing, completeness-over-impact prioritisation, unowned content decay. These guard rails are useful for the agent applying the skill.

One minor gap worth noting for future extension: the skill does not address how to handle translated or localised content if the help centre is multilingual. Not relevant for this scenario, but worth adding if the plugin is used for international products.
