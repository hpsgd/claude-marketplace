# Positioning

Scenario: Testing whether the positioning skill applies the April Dunford framework, leads with competitive alternatives, and produces a complete positioning canvas before any messaging.

## Prompt

> /gtm:positioning for Clearpath Analytics — our new reporting add-on competing against native reporting in Asana and Monday.com, targeting operations directors at 50-500 person companies.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

The positioning document is saved at `docs/gtm/positioning-clearpath-analytics.md`. Here's the summary:

---

**DRAFT — requires human review**

### Key outputs

**Tagline:** Live ops reporting. No spreadsheets. No engineers.

**Tight positioning statement:**
> For operations directors drowning in spreadsheet exports from Asana and Monday.com, Clearpath Analytics is an **operations reporting tool** that automatically delivers live, cross-team dashboards to leadership — no data engineers, no manual exports, no stale decks.

**Market category:** Operations reporting for project management tools (subcategory — borrows familiarity of "reporting" while the ops qualifier signals the buyer immediately)

**Most dangerous competitors** (ranked by frequency customers actually choose them):
1. Spreadsheets — free, familiar, already in use
2. Asana/Monday.com native reporting — zero-friction because they're already paying for it
3. Doing nothing / gut feel

**Most defensible unique attribute:** Cross-tool aggregation (Asana + Monday.com in one report) — native tools are siloed by design and this is hard to replicate without a product rebuild.

---

### Before shipping this

Five open questions need answers from the team — most importantly: **does Clearpath currently aggregate Asana + Monday.com data in a single report?** If yes, lead with it everywhere. If not, it's the most important roadmap item, because it's the one thing neither native tool can match.

### Artifacts written

#### `work/docs/gtm/positioning-clearpath-analytics.md`

```
> **DRAFT — requires human review**
> Generated 2026-05-01. Attributes marked * require validation against actual product capabilities before use.

# Positioning: Clearpath Analytics

**Product:** Clearpath Analytics — reporting add-on for Asana and Monday.com
**Target:** Operations directors, 50–500 person companies
**Framework:** April Dunford — *Obviously Awesome*

---

## Step 1 — Competitive alternatives

*If Clearpath Analytics didn't exist, what would operations directors do?*

| Alternative | Type | How often chosen | Why customers pick it |
|---|---|---|---|
| Spreadsheets (Google Sheets / Excel) | Manual | High | Free, familiar, infinitely flexible — even if it means manual exports and formula debt |
| Asana native reporting | Direct | High | Already in the tool, zero setup, good enough for single-team dashboards |
| Monday.com native reporting | Direct | High | Same as above — zero friction because they're already paying for it |
| Do nothing / gut feel | Status quo | Medium | Pain isn't sharp enough yet; ops director eyeballs Slack and weekly standups instead |
| BI tools (Tableau, Power BI, Metabase, Looker Studio) | Adjacent | Low–Medium | IT/data team already has a licence; seen as "the serious" option but requires engineering time to pipe in PM data |
| Dedicated project reporting tools (Screenful, Plecto, Databox) | Direct | Low | Bought by teams already frustrated with native reporting; niche awareness |
| Hired ops analyst / coordinator | Manual | Low | Solves the symptom (someone compiles the deck) not the problem |
| In-house build via API | In-house | Low | Engineering can pull Asana/Monday APIs — sometimes done when no off-the-shelf option satisfies |

**Most dangerous competitors:** Spreadsheets and native reporting in the tool the customer already uses — not because they're good, but because switching cost feels high and the pain accumulates slowly.

---

## Step 2 — Unique attributes

*What does Clearpath Analytics have that the alternatives genuinely don't?*

| Unique attribute | Why it matters | Which alternatives lack it |
|---|---|---|
| *Cross-tool aggregation — combines Asana + Monday.com data in a single report | Teams that run both tools (common in companies that acquired or merged) get one view instead of two partial ones | All alternatives — native tools are siloed; BI tools require custom connectors; spreadsheets require double exports |
| *Ops-specific report templates (capacity utilisation, resource allocation, project velocity, cross-team throughput) | Ops directors get the metrics they actually present to leadership — not generic "task completion" charts | Asana native, Monday.com native — their templates are PM-centric; BI tools have no PM domain templates; spreadsheets require the director to build from scratch |
| *No-code report builder with zero IT dependency | Ops director builds and modifies reports without filing a ticket or waiting on engineering | BI tools (require data engineering); in-house build (requires dev); spreadsheets (require formula skill) |
| *Live sync — data updates in the source tool reflect in reports within minutes, not via manual export | Eliminates the "stale deck" problem — no manual export cycle before the Monday leadership meeting | Spreadsheets, hired analyst — both require manual pull; even native tools can lag on cross-project rollups |
| *Scheduled delivery — reports auto-sent to Slack or email on a defined schedule | Weekly ops digest lands in the inbox without anyone touching it | All manual alternatives; native tools require someone to open the tool; BI tools can schedule but require IT setup |
| *Multi-project rollup with configurable groupings | Portfolio view across all active projects and teams in a single report, grouped by department or owner | Asana native, Monday.com native — their rollups are limited to within-tool, within-workspace hierarchies |

*Attributes marked * should be confirmed against current product capabilities before use in sales or marketing materials.*

---

## Step 3 — Value mapping

*What does each unique attribute enable for the customer?*

| Unique attribute | Capability it creates | Outcome for the user | Business impact |
|---|---|---|---|
| Cross-tool aggregation | Single source of truth across PM tools | Ops director stops reconciling two exports before every leadership meeting | Recover 2–4 hours/week spent on manual data merging; eliminate reporting errors from mismatched snapshots |
| Ops-specific templates | Skip the "what should I measure?" phase | Walk into implementation and publish a useful report on day one | First value in hours not weeks; no analyst required to design the reporting framework |
| No-code report builder | Self-service report creation and modification | Ops director owns the reporting function without depending on data or engineering team | Zero IT cost for reporting changes; faster iteration as reporting needs evolve with headcount |
| Live sync | Always-current data without manual intervention | Confident data in presentations; no "this is from last Thursday" disclaimers | Reduces risk of leadership decisions based on stale data; eliminates the Friday-afternoon export scramble |
| Scheduled delivery | Automated ops digest to stakeholders | Consistent reporting rhythm without manual work each cycle | Ops director reclaims meeting prep time; stakeholders stay informed asynchronously |
| Multi-project rollup | Portfolio visibility in one view | Spot bottlenecks and imbalances across teams before they become incidents | Earlier intervention on resource crunches; credible cross-team capacity argument in headcount discussions |

---

## Step 4 — Target customer

*Who cares most about the value delivered?*

```
Target customer profile:

Company:       50–500 employees, knowledge-work business (agency, SaaS, professional
               services, or scale-up). Uses Asana and/or Monday.com as the primary
               PM tool. Has multiple teams or projects running in parallel. No
               dedicated data engineering function.

Buyer:         Operations Director (or VP Ops, Head of Ops, COO at smaller end).
               Responsible for operational efficiency, cross-team visibility, and
               reporting upwards to leadership. Owns the PM tool budget or has
               strong influence over it. Does not have a data team to call on.

Trigger:       One or more of:
               - Headcount crossed ~50 and leadership now demands a weekly ops deck
               - Just added a second team or business unit that uses a different PM tool
               - Hired a new exec who is data-driven and expects real-time visibility
               - Manual spreadsheet reporting process is breaking — taking 4+ hours per week
               - Missed a resourcing crunch that would have been visible with better reporting

Current solution: Exports from Asana or Monday.com into Google Sheets; pivot tables
               maintained by the ops director or a coordinator. Possibly supplemented
               by native dashboards for single-team views.

Must-haves:    - Connects to Asana and/or Monday.com without engineering involvement
               - Produces reports the ops director can present to the leadership team as-is
               - Setup time under one day (no months-long implementation)
               - Cross-project rollup (more than one project/team in one view)

Deal-breakers: - Requires a data warehouse or ETL pipeline (eliminates the ops director's
                 ability to self-serve)
               - Requires IT approval or procurement (slows adoption in scrappy orgs)
               - Per-seat pricing that scales to the whole company (ops director doesn't
                 want to justify cost for every employee)
               - Rebuilds functionality the PM tool already has (leadership will ask
                 "why are we paying twice?")
```

**Exclusions:** Enterprise companies with a data team (they'll use Tableau/Looker). Solo PMs at sub-50 companies (native reporting is enough). Teams using Jira, Linear, or other tools (outside integration scope).

---

## Step 5 — Market category

**Recommendation: Subcategory — "Operations reporting for project management tools"**

Rationale:

- "Business intelligence" is too broad and sets the wrong expectations (requires data engineers, warehouses, complex setup).
- "Project management" is the wrong frame — Clearpath doesn't manage projects, it reports on them.
- "Reporting add-on" is accurate but undersells the ops-specific positioning.
- "Operations reporting" immediately signals the buyer (ops director) and the use case (cross-team visibility for leadership) without requiring education.

The subcategory benefits from the familiarity of "reporting" (customers know what it is) while the "operations" qualifier distinguishes it from generic BI tools and PM-native dashboards.

**Google test:** "operations reporting tool asana monday" — a buyer frustrated with native reporting and searching for an alternative would use these terms. The category passes.

---

## Step 6 — Assembled positioning

### Positioning canvas

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ COMPETITIVE ALTERNATIVES                                                     │
│ Spreadsheets (High) → Asana/Monday.com native (High) → Do nothing (Medium)  │
│ → BI tools (Low-Med) → Niche PM reporting tools (Low)                        │
├─────────────────────────────────────────────┬───────────────────────────────┤
│ UNIQUE ATTRIBUTES                           │ VALUE                         │
│ Cross-tool aggregation (Asana + Monday.com) │ 2–4 hrs/week recovered from   │
│ Ops-specific templates                      │ manual data merging           │
│ No-code report builder                      │ First useful report on day 1  │
│ Live sync (no manual export)                │ Zero IT cost for changes      │
│ Scheduled delivery                          │ Always-current leadership deck│
│ Multi-project rollup                        │ Portfolio visibility; earlier  │
│                                             │ intervention on bottlenecks   │
├─────────────────────────────────────────────┴───────────────────────────────┤
│ TARGET CUSTOMER                                                              │
│ Operations director at 50–500 person company; uses Asana and/or Monday.com;  │
│ no data team; running multiple teams or projects; spending 4+ hrs/week on    │
│ manual reporting; being asked for more visibility by a data-driven exec      │
├─────────────────────────────────────────────────────────────────────────────┤
│ MARKET CATEGORY                                                              │
│ Operations reporting for project management tools                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### Positioning statement

**Long version:**

> For operations directors at 50–500 person companies who are spending hours every week manually exporting and assembling reports from Asana or Monday.com, Clearpath Analytics is an operations reporting tool that delivers live, cross-team dashboards and automated leadership reports — without spreadsheets, data engineers, or IT involvement. Unlike native Asana or Monday.com reporting, Clearpath aggregates data across both tools, provides ops-specific templates built for capacity and resource reporting, and delivers scheduled reports to your inbox — so your leadership deck is always ready before the meeting starts.

**Tight version:**

> For operations directors drowning in spreadsheet exports from Asana and Monday.com, Clearpath Analytics is an operations reporting tool that automatically delivers live, cross-team dashboards to leadership — no data engineers, no manual exports, no stale decks.

---

### Tagline

> Live ops reporting. No spreadsheets. No engineers.

*Alternative options for testing:*
- "Your Monday morning ops deck, on autopilot."
- "Reporting your PM tools can't do."

---

### Sales narrative

> Every Monday, your ops director exports data from Asana, copies it into Monday.com's tracker, pivots it in Sheets, and still walks into the leadership meeting apologising for Thursday's numbers.
> Clearpath connects directly to both tools, rolls up every project and team into one live dashboard, and sends it to your exec team automatically — on whatever schedule you set.
> Unlike Asana or Monday.com's built-in reports, Clearpath works across both tools, updates in real time, and takes a day to set up — no IT ticket, no data engineer, no formula maintenance.

---

## Step 7 — Validation questions

| Question | Tests | Status |
|---|---|---|
| Would your best customers agree with the competitive alternatives list? | Step 1 accuracy | **Validate with 5 customer interviews** — "what did you use before / what would you use if we disappeared?" |
| Are unique attributes truly unique, or will Asana/Monday.com ship them in 6 months? | Step 2 durability | **Moderate risk** — native tools are adding reporting features. Cross-tool aggregation is the most defensible attribute; template library and ops-specific framing are easier to copy. |
| Does the value resonate in customer language? | Step 3 relevance | **Validate** — "stale decks," "manual export scramble," and "leadership meeting" language needs testing in win/loss calls |
| Would your target customer self-identify with the description? | Step 4 specificity | The trigger list is specific enough — anyone matching 2+ triggers will feel seen |
| Does "operations reporting for project management tools" help or confuse? | Step 5 clarity | **Test** — run a 5-second test with 5 ops directors: what do they think it is? |
| Could this positioning be mistaken for a competitor's? | Overall differentiation | Screenful uses similar language. The Asana+Monday.com cross-tool angle is the clearest differentiator and should appear in every touchpoint. |
| Can a new employee explain what you do after reading this? | Clarity | Yes — one pass through the sales narrative is sufficient |

---

## Open questions for the team

Before this positioning is finalised, answer:

1. **Cross-tool aggregation:** Is Clearpath currently able to pull from both Asana AND Monday.com in a single report? If not, this is the most important roadmap item — it's the hardest-to-copy differentiator.
2. **Pricing model:** Is pricing per-user or per-workspace? This affects the deal-breaker criterion and the "no per-seat sprawl" angle.
3. **Setup time:** What is the actual time-to-first-report in practice? The day-one value claim requires a real number.
4. **Integration breadth:** Are there other PM tools on the roadmap (Jira, Linear, ClickUp)? If yes, the category can expand; if no, keep the positioning tight on Asana+Monday.com.
5. **Win/loss data:** What is the most common reason you lose deals? If it's "native reporting is good enough," the positioning needs to sharpen on what ops directors can't do natively.

---

> **DRAFT — requires human review**
> All attributes marked * must be confirmed against current product capabilities. Do not use in sales materials, website copy, or paid campaigns without human review and editing.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.5/18.0 (92%) |
| Evaluated | 2026-05-01 |
| Target duration | 146463 ms |
| Target cost | $0.1815 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill follows the April Dunford positioning framework — competitive alternatives first, then unique attributes, value, target customer, market category | PASS | Artifact is explicitly structured as Step 1 — Competitive alternatives, Step 2 — Unique attributes, Step 3 — Value mapping, Step 4 — Target customer, Step 5 — Market category, with 'Framework: April Dunford — Obviously Awesome' declared in the header. |
| c2 | Skill begins with competitive alternatives as the anchor — not with product features or benefits | PASS | Step 1 is the first substantive section, opens with 'If Clearpath Analytics didn't exist, what would operations directors do?' and presents an 8-row table of alternatives before any product attributes appear. |
| c3 | Skill identifies unique attributes that only this product has relative to competitive alternatives — not general strengths | PASS | Step 2 table includes a 'Which alternatives lack it' column for every attribute — e.g. cross-tool aggregation: 'All alternatives — native tools are siloed by design; BI tools require custom connectors; spreadsheets require double exports.' |
| c4 | Skill maps unique attributes to specific value for the target customer — not generic claims like 'saves time' | PASS | Step 3 Value mapping gives quantified/specific outcomes: 'Recover 2–4 hours/week spent on manual data merging,' 'Zero IT cost for reporting changes,' 'Earlier intervention on resource crunches; credible cross-team capacity argument in headcount discussions.' |
| c5 | Skill produces a complete positioning canvas before any messaging or taglines are written | PASS | Step 6 opens with the ASCII positioning canvas covering all five elements before the positioning statement, tagline, and sales narrative appear. Steps 1–5 contain no taglines or copy. |
| c6 | Skill includes validation questions — criteria to test whether the positioning will hold up with real customers | PASS | Step 7 — Validation questions is a dedicated table with seven rows, each naming what it tests and its current status, including 'Validate with 5 customer interviews' and a '5-second test with 5 ops directors.' |
| c7 | Skill produces a sales narrative based on the positioning — partial credit if a narrative is mentioned as an output but not structured as a required section | PARTIAL | A 'Sales narrative' section is present and fully written in Step 6, structured in three paragraphs following the canvas. Ceiling is PARTIAL per test author. |
| c8 | All marketing copy output is labelled DRAFT and flagged for human review | PASS | Document opens and closes with '> **DRAFT — requires human review**'. A footer reads 'All attributes marked * must be confirmed against current product capabilities. Do not use in sales materials, website copy, or paid campaigns without human review and editing.' |
| c9 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | Neither the chat response nor the artifact file contains or references the skill definition file. There is no YAML frontmatter visible in any part of the captured output. |
| c10 | Output's competitive alternatives are listed FIRST — not features, not benefits — naming Asana native reporting, Monday.com dashboards, and the do-nothing alternative (Excel + Slack + manual rollups) | PASS | Step 1 table rows include 'Asana native reporting,' 'Monday.com native reporting,' 'Spreadsheets (Google Sheets / Excel),' and 'Do nothing / gut feel' — all listed before any product feature discussion. |
| c11 | Output's unique attributes are differentiating relative to those alternatives — not 'we have dashboards' (Asana has dashboards) but 'executive summary auto-generation that other reporting tools don't do natively' — concrete and verifiable | PASS | Attributes are framed against specific gaps: 'Cross-tool aggregation — native tools are siloed by design and this is hard to replicate without a product rebuild'; 'Ops-specific report templates — their templates are PM-centric'; 'No-code report builder — BI tools require data engineering.' |
| c12 | Output maps each unique attribute to specific customer value — e.g. 'auto-generated weekly exec summaries → operations director saves 4-6 hours/week + delivers consistent exec reporting' — not 'saves time' | PASS | Step 3 maps every attribute to quantified outcomes: cross-tool aggregation → '2–4 hrs/week recovered from manual data merging'; live sync → 'Eliminates the Friday-afternoon export scramble'; multi-project rollup → 'Earlier intervention on resource crunches; credible cross-team capacity argument in headcount discussions.' |
| c13 | Output's target customer is precise — 'operations directors at 50-500 person companies who own portfolio-level project visibility and report up to a CEO/COO' — not 'businesses that want better reporting' | PASS | Step 4 specifies: 'Buyer: Operations Director (or VP Ops, Head of Ops, COO at smaller end). Responsible for operational efficiency, cross-team visibility, and reporting upwards to leadership.' Includes specific triggers, must-haves, deal-breakers, and exclusion criteria. |
| c14 | Output's market category is named explicitly — 'executive project portfolio reporting' or 'operations intelligence for project-led teams' — not 'project management software' | PASS | Step 5 names 'Operations reporting for project management tools' with explicit rationale excluding 'Business intelligence,' 'Project management,' and 'Reporting add-on' as category names. |
| c15 | Output's positioning canvas covers all five Dunford elements — competitive alternatives, unique attributes, value, target customer, market category — in a structured layout, not prose | PASS | The ASCII canvas in Step 6 has four labeled rows: COMPETITIVE ALTERNATIVES, UNIQUE ATTRIBUTES \| VALUE (combined), TARGET CUSTOMER, MARKET CATEGORY — structured table, not prose. |
| c16 | Output's validation questions test whether real customers will recognise the positioning — e.g. 'do operations directors describe their alternative as Asana reporting, or as Excel rollups?' — concrete questions that can be answered by 5-10 customer conversations | PASS | Step 7 includes 'Validate with 5 customer interviews — what did you use before / what would you use if we disappeared?', 'run a 5-second test with 5 ops directors: what do they think it is?', and 'What is the most common reason you lose deals?' — all concrete and answerable. |
| c17 | Output's sales narrative (if produced) follows the canvas — opens with the competitive alternative pain, transitions to the unique attributes, lands on customer value, names the category — not a generic problem-solution-product structure | PASS | Sales narrative opens with 'Every Monday, your ops director exports data from Asana, copies it into Monday.com's tracker...' (competitive alternative pain), transitions to 'Clearpath connects directly to both tools...' (unique attributes), and closes with 'Unlike Asana or Monday.com's built-in reports, Clearpath works across both tools, updates in real time, and takes a day to set up — no IT ticket, no data engineer, no formula maintenance' (value vs. alternatives). |
| c18 | Output labels every customer-facing tagline / message draft — DRAFT, requires human review — not approved finals | PASS | Top and bottom of document carry '> **DRAFT — requires human review**'. Footer explicitly states 'Do not use in sales materials, website copy, or paid campaigns without human review and editing.' Tagline alternatives are presented as 'options for testing.' |
| c19 | Output addresses where the canvas may shift on pricing — analytics add-on at $15/seat positions Clearpath as a premium overlay (suggesting the buyer values exec visibility highly) which informs the pricing message and channel | FAIL | Pricing appears only as an open question: 'Is pricing per-user or per-workspace? This affects the deal-breaker criterion and the no per-seat sprawl angle.' No discussion of how a specific price point (e.g. $15/seat) would shift canvas positioning, premium overlay framing, or channel implications. |

### Notes

The output is a high-quality, structurally complete implementation of the April Dunford framework. All five positioning canvas elements are present, ordered correctly, and linked through explicit value mapping. The sales narrative properly opens with competitive alternative pain rather than product features. DRAFT labeling is thorough and consistent. The two failures are c9 (skill YAML frontmatter not visible in captured output — may exist in the skill file but cannot be verified from what was captured) and c19 (pricing's effect on canvas positioning is acknowledged as an open question but not substantively analyzed — the specific premium-overlay / channel implication was not addressed). These two gaps cost 1.5 points against an 18-point max, yielding 91.7% — a solid PASS.
