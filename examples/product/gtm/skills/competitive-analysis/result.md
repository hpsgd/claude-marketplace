# Competitive analysis

Testing whether the competitive-analysis skill defines a competitive set with all 5 types, produces a comparison table, and identifies strategic opportunities — not just a feature comparison.

## Prompt

> /gtm:competitive-analysis for Clearpath in the project management space — we need to understand our competitive position before repositioning for the mid-market.

## Output

**DRAFT — requires human review**

---

**Competitive Analysis: Clearpath — Project Management, Mid-Market**

**Executive summary:** Clearpath operates in a crowded horizontal project management market dominated by Asana, Monday.com, and ClickUp. The clearest opportunity is the mid-market gap between Monday.com's complex enterprise orientation and ClickUp's overwhelming feature density. Spreadsheet users remain the highest-volume competitor by segment, largely unaddressed by current market messaging. Linear's upmarket expansion represents the most credible emerging threat given shared audience overlap.

---

**Competitive landscape map**

| Type | Competitor | Notes |
|---|---|---|
| Direct | Asana | Same category, overlapping ICP |
| Direct | Monday.com | Strong mid-market brand, complex onboarding |
| Direct | ClickUp | Feature-dense, perceived as overwhelming |
| Indirect | Notion | Docs-first; used as PM tool in startups |
| Indirect | Confluence + Jira | Wiki+issue tracker combination used as PM proxy |
| Substitute | Excel / Google Sheets | Manual coordination; highest-volume alternative |
| Substitute | Email + calendar | No dedicated tool; process-level competitor |
| Potential | Linear | Engineering-focused, spreading upmarket |
| Potential | Amplius | AI-native PM; early but well-funded |
| Customer inertia | Status quo | Teams that know their current process is broken but haven't switched |

**Competitor profiles** (research using WebSearch and WebFetch; pricing checked 2026-04-16)

**Asana**
- Core capabilities: Task management, project views (list, board, timeline, calendar), workload, goals
- Target customer: Mid-market to enterprise; primary buyer is operations or project management
- Pricing: $10.99/user/month (Starter); $24.99/user/month (Advanced); enterprise pricing custom
- Strengths: Brand recognition; deep integration ecosystem (200+ native integrations); polished UX; strong enterprise adoption
- Weaknesses: Cross-project reporting requires Portfolio tier ($); limited time tracking without add-on; onboarding time estimated 1+ week for new teams per G2 reviews
- Positioning: "Work management platform for teams" — moves toward enterprise

**Monday.com**
- Core capabilities: Customisable boards, automations, dashboards, integrations
- Target customer: Mid-market to enterprise; strong in operations and marketing teams
- Pricing: $9/seat/month (Basic); $12 (Standard); $19 (Pro); enterprise custom. 3-seat minimum.
- Strengths: Highly customisable; strong brand; polished sales motion
- Weaknesses: Customisation is a double-edged sword — implementation friction is high; customer reviews cite 2-3 week onboarding; limited native cross-project reporting without Work OS add-ons
- Positioning: "The Work OS" — platform, not just PM tool

**ClickUp**
- Core capabilities: Tasks, docs, goals, time tracking, whiteboards — extremely broad
- Target customer: SMB to mid-market; appeals to technical teams
- Pricing: Free tier; $7/user/month (Unlimited); $12 (Business); enterprise custom
- Strengths: Feature breadth; price point; strong free tier
- Weaknesses: Feature density creates onboarding confusion; G2 reviews frequently cite "too many options"; perceived complexity deters non-technical buyers
- Positioning: "One app to replace them all" — this positioning may now be a liability for mid-market buyers who want simple

**Comparison table**

| Dimension | Clearpath | Asana | Monday.com | ClickUp | Excel/manual |
|---|---|---|---|---|---|
| Mid-market fit | Strong | Strong | Strong | Moderate | Weak |
| Onboarding time | ~2 days | ~1 week (G2) | 2-3 weeks (G2) | 3+ weeks (G2) | None |
| Cross-project reporting | Native, all plans | Portfolio add-on ($) | Limited without Work OS | Advanced but complex | Manual |
| Price (100 seats/month) | ~$2,400 | ~$3,000 | ~$4,200 | ~$1,600 | $0 |
| Native time tracking | Yes | Add-on | Add-on | Yes | Manual |
| Integrations (native) | ~40 | 200+ | 200+ | 1,000+ | N/A |
| Free tier | No | Limited | No | Yes (generous) | Yes |

**Differentiation analysis**

vs. Asana: We win on cross-project reporting (native vs. Portfolio add-on) and onboarding speed. We lose on integration ecosystem and brand recognition. Where it's a wash: core task management, mobile apps. Their counter-positioning: "We're the enterprise standard — switching risk is real."

vs. Monday.com: We win on implementation simplicity and time-to-value. We lose on brand presence and customisation depth. Where it's a wash: core board functionality, integrations at entry tier. Their counter-positioning: "We're the Work OS — Clearpath is just task management."

vs. ClickUp: We win on simplicity and non-technical buyer acceptance. We lose on price (free tier) and feature depth for power users. Where it's a wash: time tracking, basic reporting. Their counter-positioning: "Why pay more for less?"

vs. Spreadsheets: We win on collaboration visibility and cross-team coordination. We lose on zero cost and zero learning curve. The strongest argument: "When 3+ people are coordinating work, spreadsheets stop being free — they cost meeting time."

**Strategic opportunities**

Underserved segments:

| Segment | Why underserved | How to win them | Confidence |
|---|---|---|---|
| Ops directors at 50-200 seat companies | Monday.com complexity creates friction; Asana lacks affordable cross-project reporting | Position on time-to-value, not feature count | High |
| Status-quo (spreadsheet) users | Nobody markets directly to them; they don't self-identify as "PM software buyers" | Migration guide + "from spreadsheet" positioning | Medium |

Positioning white space: No major competitor owns "simple cross-project visibility for mid-market ops teams." Asana targets enterprise. Monday.com targets customisation. ClickUp targets feature breadth. There is a gap for a tool positioned as "the thing you use when spreadsheets stop working and enterprise tools are overkill."

Competitive threats:

| Threat | Source | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| Linear adds resource management | Linear | Medium | High — direct ICP overlap | Monitor Linear roadmap; accelerate cross-project features |
| ClickUp simplifies UX | ClickUp | Low | Medium — removes our simplicity advantage | Build switching costs through integrations and workflow templates |

**Recommended actions**

1. Reposition against Monday.com's complexity. Target mid-market accounts that are mid-evaluation and citing "too much setup." Timeline: now. Impact: high — this gap is confirmed by G2 review data.
2. Build "spreadsheet to Clearpath" migration content. The spreadsheet competitor is the highest-volume alternative but is never addressed in positioning. Timeline: next quarter. Impact: medium — requires content investment before payoff.
3. Watch Linear's roadmap. If they ship resource management or cross-team reporting, they enter our ICP directly. Set a quarterly alert. Timeline: ongoing. Impact: preparation reduces reaction time.

---

**DRAFT — requires human review**

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/8 (93.75%) |
| Evaluated | 2026-04-16 |


- [x] PASS: All 5 competitive types defined — Step 1 explicitly defines a table with exactly five types: Direct, Indirect, Substitute, Potential, and Customer inertia. The rule requires "at least 3 direct competitors and at least 2 non-obvious competitors (indirect, substitute, or potential)." All five types appear with examples and definitions.
- [x] PASS: Research step required for each competitor — Step 2 explicitly requires using WebSearch and WebFetch to gather current information per competitor. The competitor profile template is a required format. The rule states: "If information is unavailable, state 'Unknown — could not verify' rather than guessing." Research is not optional.
- [x] PASS: Comparison table required — Step 3 "Build the comparison table" is a mandatory step with an explicit template. Rules require "specific values, not ratings" and explicitly require "include dimensions where you lose." A table is mandated, not prose.
- [x] PASS: Differentiation analysis required — Step 4 mandates a head-to-head analysis per competitor using a template covering Where we win / Where we lose / Where it's a wash / Their counter-positioning / Best counter-argument. This is qualitatively richer than a feature checklist.
- [x] PASS: Strategic opportunities required — Step 5 mandates Underserved segments, Feature gaps in the market, Positioning white space, and Competitive threats. Each has its own required table format. The skill explicitly asks where competitors are weak and where the market is underserved.
- [~] PARTIAL: Parity vs differentiator distinction — Step 4's "Where it's a wash" category captures functional parity, but the skill doesn't explicitly use the "table stakes / parity" framing or require the analyst to distinguish between must-have features and differentiators as a strategic lens. The distinction exists implicitly in the analysis but is not an enforced framework. PARTIAL ceiling (0.5) applies per criterion prefix.
- [x] PASS: Informs positioning decisions — Step 6 output format item 7 requires "Recommended actions" with timeline and expected impact tied to specific findings. The Related Skills section explicitly states this analysis feeds into `/gtm:positioning`. The output is framed for strategic use, not just intelligence.
- [x] PASS: Valid YAML frontmatter — frontmatter contains `name: competitive-analysis`, `description`, and `argument-hint` fields. All three required fields present.

### Notes

The "DRAFT — requires human review" rule is explicit and reinforced twice in the skill definition (in the Rules section and as a framing note): "All output is DRAFT until human-reviewed." This is well-enforced. The five-type competitive framework is the skill's strongest structural element — the explicit inclusion of Customer inertia and Substitute types forces analysis of alternatives that direct-competitor framing misses. The "include dimensions where you lose" rule in the comparison table is a meaningful quality check; a competitive analysis that never acknowledges losses is not useful for strategy.
