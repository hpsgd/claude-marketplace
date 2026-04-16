# Content strategy

Testing whether the content-strategy skill uses the Diataxis framework, requires a content inventory, and produces a prioritised content roadmap.

## Prompt

> /user-docs-writer:content-strategy for our help centre — we have 140 articles written over 3 years, significant product changes since most were written, and support tickets suggesting users can't find answers to common questions.

## Output

**Content Strategy: Clearpath Help Centre**

**Step 1 — Inventory (140 articles):**

| # | Document | Path | Quadrant | Feature area | Last updated | Status |
|---|---|---|---|---|---|---|
| 1 | Getting started with time tracking | /docs/time/start.md | Tutorial | Time tracking | 2023-01-12 | Stale |
| 2 | How to read utilisation reports | /docs/reports/utilisation.md | How-to | Reporting | 2022-08-04 | Stale |
| ... | ... | ... | ... | ... | ... | ... |

Summary: 8 Tutorial (6%), 61 How-to (44%), 42 Reference (30%), 29 Explanation (20%). 14 orphaned articles with no clear quadrant.

**Step 2 — Coverage matrix:**

| Feature | Tutorial | How-to | Reference | Explanation |
|---|---|---|---|---|
| Time tracking | No | Yes | Stale | No |
| Reporting | No | Partial | Stale | Yes |
| Integrations | No | Yes | No | No |
| Admin settings | No | Yes | Yes | No |

**Step 3 — Gap analysis:**

Missing content: Tutorials are nearly absent (6%). All admin and integration areas lack explanation docs. Reference docs for time tracking and reporting are stale.

Stale content: 14 reference articles flagged as outdated by product changes.

Orphaned: 14 articles with no inbound links or navigation entry.

Common patterns: Tutorial gap (onboarding path has no guided walkthrough), Freshness gap (major feature changes not reflected).

**Step 4 — Prioritised backlog:**

| Priority | Content piece | Quadrant | Feature | Effort | Owner |
|---|---|---|---|---|---|
| P0 | Getting started tutorial | Tutorial | Onboarding | M | Docs lead |
| P0 | Utilisation reports how-to | How-to | Reporting | S | Docs lead |
| P1 | Integration reference | Reference | Integrations | L | Docs lead |

**Step 5 — Content standards:**

| Quadrant | Structure | Length | Must include |
|---|---|---|---|
| Tutorial | Numbered steps with outcomes | 10-30 min | Prerequisites, working example, next steps |
| How-to | Numbered steps, minimal explanation | 2-5 min | Goal in title, single outcome |
| Reference | Tables, parameter lists | Complete | Every option, every error code |
| Explanation | Prose with diagrams | As needed | Why, not how |

**Step 6 — Roadmap:**

Phase 1 (Weeks 1-4): Foundation — onboarding tutorial, top 3 stale how-tos.
Phase 2 (Weeks 5-8): Completeness — reference docs for integrations and admin.
Phase 3 (Weeks 9-12): Depth — explanation articles for complex features.

Ongoing maintenance: monthly freshness review, feature-change trigger, quarterly coverage audit, support ticket review.

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/8 criteria met (94%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Diataxis framework applied — the skill opens with "Define a documentation content strategy for $ARGUMENTS using the Diataxis framework." All six steps classify content as Tutorial, How-to, Reference, or Explanation throughout. The inventory table, coverage matrix, gap analysis, and content standards all use Diataxis quadrants as the mandatory taxonomy. The quadrant definitions are explicitly stated in Step 1.
- [x] PASS: Content inventory before recommendations — Step 1 "Inventory Existing Content" is mandatory and uses Glob/Grep to find and classify all existing documentation. The output format requires a complete inventory table before any Step 2-6 content executes.
- [x] PASS: Gap analysis required — Step 3 "Identify Gaps" is a required step with dedicated table structures for missing content, stale content, and orphaned content, all structured by feature area and quadrant. Common gap patterns (explanation gap, tutorial gap, reference gap, freshness gap) are explicitly required checks.
- [x] PASS: Prioritised content roadmap — Step 4 "Prioritise Content Creation" produces a ranked backlog (P0/P1/P2) with rationale. The prioritisation criteria table includes weights (High/Medium/Low) and rationale for user traffic, onboarding path, support ticket volume, feature completeness, quadrant balance, and staleness risk. Step 6 synthesises this into a phased roadmap.
- [x] PASS: Content standards per type — Step 5 "Define Content Standards" is a required step with a per-quadrant standards table covering structure, length, and must-include elements for Tutorial, How-to, Reference, and Explanation.
- [x] PASS: Coverage matrix required — Step 2 "Map Coverage" explicitly requires a feature-by-quadrant matrix. The output format template shows exactly how it must be structured, including a Coverage Summary table with quadrant counts and percentages.
- [~] PARTIAL: Content maintenance — Step 6's roadmap includes an "Ongoing: Maintenance" section requiring monthly freshness review, feature-change trigger, quarterly coverage audit, and support ticket review. This is a required component of the roadmap output. Maximum score is 0.5 per PARTIAL ceiling — criterion is PARTIAL-prefixed regardless of how fully the definition meets it.
- [x] PASS: Valid YAML frontmatter — contains `name: content-strategy`, `description`, and `argument-hint` fields.

### Notes

This skill is well-structured and closely matches the test criteria. The Diataxis framework is applied consistently across all six steps rather than just mentioned in the introduction. Every step produces a required output artifact.

The content maintenance criterion is PARTIAL-ceilinged by the test author. The definition actually fully requires a maintenance schedule as part of Step 6's output — monthly reviews, feature-change triggers, and ownership are all mandated. The ceiling is the test author's constraint.

The prioritisation rationale (Step 4) is notably specific: user traffic, onboarding path, support ticket volume, feature completeness, quadrant balance, and staleness risk are listed with relative weights. This is more useful than most content strategy approaches that just say "prioritise by impact."
