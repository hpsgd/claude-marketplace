# Positioning

Scenario: Testing whether the positioning skill applies the April Dunford framework, leads with competitive alternatives, and produces a complete positioning canvas before any messaging.

## Prompt

> /gtm:positioning for Clearpath Analytics — our new reporting add-on competing against native reporting in Asana and Monday.com, targeting operations directors at 50-500 person companies.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll work through the April Dunford positioning framework for Clearpath Analytics. Since this is GTM work, I'm flagging this as **DRAFT — requires human review and product validation** throughout. I need to verify some product details as I work — feel free to correct assumptions about capabilities.

---

## Step 1 — Competitive Alternatives

**If Clearpath Analytics didn't exist, what would operations directors do?**

| Alternative | Type | How often chosen | Why customers pick it |
|---|---|---|---|
| Native Asana reporting | Direct competitor | High | Already embedded, no switching cost, included in their plan |
| Native Monday.com reporting | Direct competitor | High | Already embedded, part of their workflow, familiar interface |
| Excel / Google Sheets | Manual process | High | Full flexibility, own data, control over calculations and presentation |
| Tableau / Power BI | Adjacent competitor | Medium | Powerful for complex analytics, cross-tool data integration, enterprise standard |
| Hire a full-time analyst | Manual / In-house | Medium | Custom reports built exactly to spec, deep domain knowledge of workflows |
| Status quo (use basic dashboards) | Status quo | Medium | Avoids cost and switching; rely on built-in task views and KPI cards |
| Looker or similar BI platform | Adjacent competitor | Low | Enterprise-grade, but overkill and complex for operations teams |
| Custom-built internal dashboards | In-house | Low | Some orgs with engineering resources build lightweight solutions |

---

## Step 2 — Unique Attributes

**What does Clearpath have that these alternatives don't?**

*I need product validation here.* Based on "reporting add-on," I'm assuming:

| Unique attribute | Why it matters | Which alternatives lack it |
|---|---|---|
| **Operations-specific templates** (not generic BI) | Pre-built reports for ops use cases (cycle time, capacity, blockers, handoffs) — no custom SQL needed | Asana, Monday.com, Tableau, Power BI (require custom config) |
| **Instant data freshness without ETL complexity** | Real-time or near-real-time reporting directly from task tools — no pipeline setup | Tableau, Power BI, Looker, in-house solutions (all require data integration layer) |
| **Multi-workspace/org rollups** | Aggregate reporting across multiple Asana/Monday instances from one UI — *does Clearpath do this?* | Native tools (single workspace only), Excel (manual consolidation) |
| **Scheduled export & distribution** (push reports to stakeholders) | Automated weekly/daily summaries to email or Slack — not asking teams to pull data | Asana, Monday.com (require manual sharing), Excel/Sheets (manual export) |
| **Drill-down to task level** (traceability) | Click a metric → see the actual tasks/work items driving it — not just aggregate numbers | Asana/Monday dashboards (limited drill), BI tools (require custom cubes) |

**Flag for validation:** What is Clearpath's actual moat here? Which of these attributes should be prioritized as uniquely defensible? Are there others I'm missing?

---

## Step 3 — Value Mapping

**What does each unique attribute enable for the operations director?**

| Unique attribute | Capability it creates | Outcome for the user | Business impact |
|---|---|---|---|
| Operations-specific templates | Instant visibility to operations KPIs (cycle time, capacity, slippage) without custom configuration | "I have my Monday metrics in 5 minutes, not a 2-week Tableau project" | Save 40-80 hours of setup/configuration per year |
| Real-time data with no ETL | Always-current reporting without managing data pipelines or sync tools | "My reports are live; I don't discover bad data in a Friday standup" | Reduce decision lag from weekly to real-time; catch slippage earlier |
| Multi-org rollups | Consolidate reporting for ops teams managing multiple business units or customers | "One dashboard for all three account teams' capacity instead of six separate views" | 5-10 hours saved per week copying and reconciling data; faster org-wide planning |
| Scheduled exports & distribution | Stakeholders receive weekly summaries without asking them to log in and check | "Leadership has next week's forecast without me running five manual reports" | Cut status-reporting time by 70%; free up ops director for strategic work |
| Drill-down to task level | When a metric is off, immediately see the work causing it — not just a number | "That capacity spike? It's these 8 tasks blocked on design review. We can unstick them today" | Move from "report shows problem" to "report shows solution" in one click |

---

## Step 4 — Target Customer

**Who cares most about this value?**

```
Target customer profile:

Company: 
- Size: 50–500 employees
- Growth stage: Post-PMF, scaling operations (Series A–B typical)
- PM tool maturity: Heavy Asana or Monday.com user (core to workflow, not optional)
- Operational complexity: Multiple teams / projects / geographic locations; some handoff bottlenecks
- Pain trigger: Operating with stale dashboards and manual reporting; visibility lags decision-making

Buyer:
- Title: Operations Director / Director of Program Management / Head of Ops
- Responsibilities: Cross-team capacity planning, project delivery visibility, stakeholder reporting, process optimization
- Current behaviour: Spending 8-12 hours/week on manual reporting, using native dashboards as starting point
- Budget: $3–15K/year discretionary ops budget (tools, contractors, admin time)

Trigger for buying:
- "We just hired 5 more teams and our Excel-based forecasting broke down"
- "Leadership asks the same three questions every Monday; I spend Friday prepping answers"
- "By the time I see a problem in the dashboard, it's already missed our deadline"
- "We bought Monday/Asana 18 months ago and we're still using basic views"

Current solution:
- Native Asana/Monday dashboards (insufficient for cross-project visibility)
- Weekly manual rollups in Excel/Sheets (slow, error-prone)
- Email status updates compiled by hand (8-12 hours/week)
- Monthly business reviews that are 50% "pull together last month's data"

Must-haves:
- ✓ Works with their existing PM tool (non-negotiable)
- ✓ Gives true visibility across multiple projects/teams without 4-week setup
- ✓ Runs in real-time (not yesterday's data)
- ✓ Reduces manual reporting time immediately (not someday)
- ✓ Accessible to non-technical users (ops directors, not data engineers)

Deal-breakers:
- Requires custom SQL or data engineering work
- Only works with one team's data (doesn't solve rollup problem)
- Slower than opening native dashboard ("why would I use this?")
- Requires weekly manual data refresh
- Expensive relative to 10-20 hours/month saved
```

---

## Step 5 — Market Category

**What frame makes your value obvious?**

Three options:

| Option | Why to choose | Positioning consequence |
|---|---|---|
| **"Operations reporting platform"** | Establishes you as purpose-built for ops (not a generic BI tool). Sets context for template-first thinking. | Customers immediately understand: "This is for my use case." Default to this. |
| **"Work management analytics"** (subcategory) | Emphasizes you're analytics *within* PM tools, not a separate system. | Customers might confuse you with native tools. Less differentiation. |
| **"Real-time operations intelligence"** (new category) | Emphasizes real-time + intelligence. Educates market on what's missing from current tools. | Expensive to educate; risky if you're the only player. Only if you have major market momentum. |

**Recommendation: Use existing category "Operations reporting platform."** It's clear, searchable, defensible.

---

## Step 6 — Assemble the Positioning

### Positioning Statement

```
For operations directors at scaling teams who spend 10+ hours weekly on manual reporting and stakeholder updates,
Clearpath Analytics is an operations reporting platform
that delivers real-time, multi-team capacity and project health visibility in minutes, not weeks.
Unlike native Asana/Monday dashboards that require custom configuration and limit visibility to one workspace,
Clearpath delivers pre-built operations templates with drill-down traceability — so you see slippage and move fast before it compounds.
```

**Tighter version:**

```
For operations directors drowning in manual reporting,
Clearpath Analytics replaces weekly spreadsheet summaries with real-time, pre-built operations dashboards that roll up across teams and projects.
```

### Tagline

**"Operations visibility. Real-time. Built-in templates."** (7 words)

Or: **"Real-time ops reporting. Built for scaled teams."** (7 words)

Or: **"Multi-team visibility without the manual work."** (6 words) ← I'd recommend this one — it's specific to the problem (manual work) and the outcome (multi-team visibility).

### Sales Narrative (3-sentence version)

```
Sentence 1 (Problem): "You're managing capacity across three teams and Asana dashboards only show one at a time. 
Your Friday is consumed rolling up spreadsheets for Monday's leadership standup."

Sentence 2 (What we do): "Clearpath gives you live, consolidated visibility across all your teams — pre-built for operations metrics 
like cycle time, capacity, and slippage. No SQL, no pipeline setup. It works because it's built for operations, not generic analytics."

Sentence 3 (Why us): "Native tools aren't built for this scale of coordination. BI tools take weeks to set up. 
Clearpath works in your existing PM tool and your stakeholders see the dashboards by end of week."
```

---

### Positioning Canvas

```
┌──────────────────────────────────────────────────────────────┐
│ COMPETITIVE ALTERNATIVES                                      │
│ • Native Asana/Monday dashboards (high)                        │
│ • Manual Excel/Sheets rollups (high)                           │
│ • Tableau / Power BI (medium)                                  │
│ • Hire a full-time analyst (medium)                            │
│ • Status quo: basic task views (medium)                        │
├──────────────────────────────────────────────────────────────┤
│ UNIQUE ATTRIBUTES         │ VALUE DELIVERED                   │
│ ────────────────────────  │ ──────────────────────────────   │
│ • Ops-specific templates  │ Save 40–80 hrs setup/config      │
│ • Real-time, no ETL       │ Real-time decisions, catch drift │
│ • Multi-org rollups       │ 5–10 hrs/week saved              │
│ • Scheduled distribution  │ 70% less manual reporting time   │
│ • Drill-down to tasks     │ From problem reporting to action │
├──────────────────────────────────────────────────────────────┤
│ TARGET CUSTOMER                                                │
│ Ops Director, 50–500 person scaling company, using            │
│ Asana/Monday heavily. Spending 8-12 hrs/week on manual        │
│ reporting. Needs multi-team visibility, not just dashboards.  │
├──────────────────────────────────────────────────────────────┤
│ MARKET CATEGORY: Operations reporting platform                │
└──────────────────────────────────────────────────────────────┘
```

---

## Step 7 — Validation Questions

| Question | Answer | If "no," fix |
|---|---|---|
| Would your best customers agree with the competitive alternatives list? | **Need to confirm** — Have you talked to ops directors about what they actually use today? | Interview 3-5 customers on their current workflow |
| Are your unique attributes truly unique, or will competitors match them in 6 months? | **Need to confirm** — Asana/Monday move fast. How defensible is real-time + ops templates? | Clarify what takes competitors 12+ months to build |
| Does the value resonate with target customers in their own words? | **Need to confirm** — Do ops directors say "I need real-time" or do they say "I waste Friday on reports"? | Validate with customer interviews — use their language |
| Would your target customer self-identify with this description? | **Likely yes** — "Ops director at 50–500 person company" is specific enough | Narrow further if early conversations show a tighter niche |
| Does "operations reporting platform" help or confuse? | **Likely helps** — It's clear and searchable | Test with actual ops directors in a discovery call |
| Could this be mistaken for a competitor's positioning? | **Risk: Yes** — Native tools may claim "real-time operations visibility." Need stronger differentiation. | Emphasize multi-workspace rollup or pre-built templates as primary differentiator |
| Can a new employee explain what you do after reading this? | **Likely yes** — Positioning is concrete | Test with sales team; adjust jargon if needed |

---

## Questions for You

Before you use this positioning, I need to validate:

1. **Product capabilities**: I assumed real-time data, multi-workspace rollups, drill-down traceability, and scheduled exports. Are these accurate? What's the actual feature set?

2. **Competitive moat**: Asana and Monday.com are shipping reporting faster than ever. What will still be defensible 18 months from now? (Template library? Integrations? Speed?)

3. **Customer validation**: Have you talked to ops directors about their pain? Does "I waste 10 hours/week on manual reporting" match what they're telling you?

4. **Pricing sensitivity**: Is $3–15K/year the right budget range for this buyer, or should we target higher (enterprise) or lower (SMB)?

5. **Go-to-market**: Will you sell to operations directors directly, or through Asana/Monday partner channels?

Positioning is only useful if it's grounded in real customer problems and defensible product strengths. Once you confirm product details and customer validation, this positioning can be hardened and used in your marketing and sales materials.

---

**DRAFT — requires human review and product validation**

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/18.0 (89%) |
| Evaluated | 2026-05-04 |
| Target duration | 47583 ms |
| Target cost | $0.0579 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill follows the April Dunford positioning framework — competitive alternatives first, then unique attributes, value, target customer, market category | PASS | Output is structured as Steps 1–6 explicitly: Step 1 Competitive Alternatives → Step 2 Unique Attributes → Step 3 Value Mapping → Step 4 Target Customer → Step 5 Market Category → Step 6 Assemble the Positioning. The sequence is identical to the Dunford framework. |
| c2 | Skill begins with competitive alternatives as the anchor — not with product features or benefits | PASS | Step 1 opens with 'If Clearpath Analytics didn't exist, what would operations directors do?' — the Dunford anchor question — before any features are described. The first table lists eight alternatives with type, frequency, and customer rationale. |
| c3 | Skill identifies unique attributes that only this product has relative to competitive alternatives — not general strengths | PASS | Step 2 table includes a 'Which alternatives lack it' column for every attribute. E.g. 'Multi-workspace/org rollups' is paired with 'Native tools (single workspace only), Excel (manual consolidation)' — each attribute is explicitly tied to what specific alternatives cannot do. |
| c4 | Skill maps unique attributes to specific value for the target customer — not generic claims like 'saves time' | PASS | Step 3 gives quantified, specific outcomes: 'Save 40–80 hours of setup/configuration per year', 'Cut status-reporting time by 70%', '5–10 hours saved per week copying and reconciling data', 'Move from report shows problem to report shows solution in one click' — none are generic. |
| c5 | Skill produces a complete positioning canvas before any messaging or taglines are written | FAIL | The positioning canvas (ASCII table covering all five Dunford elements) appears at the END of Step 6, after the Positioning Statement, three Tagline options, and the Sales Narrative have all been written. The criterion requires the canvas before messaging; the output reverses the order. |
| c6 | Skill includes validation questions — criteria to test whether the positioning will hold up with real customers | PASS | Step 7 'Validation Questions' is a structured table with seven rows including 'Would your best customers agree with the competitive alternatives list?', 'Does the value resonate with target customers in their own words? Do ops directors say I need real-time or do they say I waste Friday on reports?' — all actionable and testable. |
| c7 | Skill produces a sales narrative based on the positioning — partial credit if a narrative is mentioned as an output but not structured as a required section | PARTIAL | Output includes 'Sales Narrative (3-sentence version)' as a labelled section within Step 6 with three explicitly labelled sentences (Problem, What we do, Why us). A narrative is fully produced, but ceiling is capped at PARTIAL per the test rubric. |
| c8 | All marketing copy output is labelled DRAFT and flagged for human review | PASS | Output opens with 'DRAFT — requires human review and product validation' and closes with the identical label. The opening paragraph also states 'I'm flagging this as DRAFT — requires human review and product validation throughout.' All messaging sits within this framing. |
| c9 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The captured output is a chat response only. No YAML frontmatter (name, description, argument-hint) appears anywhere in the output. The skill definition file is not visible in the captured output, so this criterion cannot be verified. |
| c10 | Output's competitive alternatives are listed FIRST — not features, not benefits — naming Asana native reporting, Monday.com dashboards, and the do-nothing alternative (Excel + Slack + manual rollups) | PASS | Step 1 table lists 'Native Asana reporting', 'Native Monday.com reporting', and 'Excel / Google Sheets' among eight alternatives — all appearing before any features or benefits. Slack is not mentioned explicitly but Excel/manual rollups and 'Status quo' cover the do-nothing alternative. |
| c11 | Output's unique attributes are differentiating relative to those alternatives — not 'we have dashboards' (Asana has dashboards) but 'executive summary auto-generation that other reporting tools don't do natively' — concrete and verifiable | PASS | Attributes like 'Multi-workspace/org rollups', 'Instant data freshness without ETL complexity', and 'Scheduled export & distribution' are each paired with which competitors lack them. The attributes are specific capabilities, not 'we have dashboards' equivalents. |
| c12 | Output maps each unique attribute to specific customer value — e.g. 'auto-generated weekly exec summaries → operations director saves 4-6 hours/week + delivers consistent exec reporting' — not 'saves time' | PASS | Step 3 gives concrete mappings: 'Scheduled distribution → Cut status-reporting time by 70%; free up ops director for strategic work'; 'Multi-org rollups → 5–10 hours saved per week copying and reconciling data; faster org-wide planning'. All are specific and quantified. |
| c13 | Output's target customer is precise — 'operations directors at 50-500 person companies who own portfolio-level project visibility and report up to a CEO/COO' — not 'businesses that want better reporting' | PASS | Step 4 specifies: 'Operations Director / Director of Program Management / Head of Ops', '50–500 employees', 'Post-PMF, scaling operations (Series A–B typical)', 'Heavy Asana or Monday.com user', 'Spending 8-12 hours/week on manual reporting', '$3–15K/year discretionary ops budget'. Not a generic persona. |
| c14 | Output's market category is named explicitly — 'executive project portfolio reporting' or 'operations intelligence for project-led teams' — not 'project management software' | PASS | Step 5 explicitly names the category as 'Operations reporting platform' and recommends it with 'Use existing category Operations reporting platform.' The canvas footer also reads 'MARKET CATEGORY: Operations reporting platform'. Not 'project management software'. |
| c15 | Output's positioning canvas covers all five Dunford elements — competitive alternatives, unique attributes, value, target customer, market category — in a structured layout, not prose | PASS | The ASCII canvas includes labelled sections: 'COMPETITIVE ALTERNATIVES' (5 bullet items), 'UNIQUE ATTRIBUTES' and 'VALUE DELIVERED' (two-column table), 'TARGET CUSTOMER' (prose description), and 'MARKET CATEGORY: Operations reporting platform'. All five elements present in a structured visual layout. |
| c16 | Output's validation questions test whether real customers will recognise the positioning — e.g. 'do operations directors describe their alternative as Asana reporting, or as Excel rollups?' — concrete questions that can be answered by 5-10 customer conversations | PASS | Step 7 includes 'Have you talked to ops directors about what they actually use today?' and 'Do ops directors say I need real-time or do they say I waste Friday on reports?' — both questions are resolvable via a small number of customer conversations, matching the criterion's intent. |
| c17 | Output's sales narrative (if produced) follows the canvas — opens with the competitive alternative pain, transitions to the unique attributes, lands on customer value, names the category — not a generic problem-solution-product structure | PASS | Sentence 1 opens with Asana dashboard limitation and manual Friday rollups (competitive alternative pain). Sentence 2 transitions to 'pre-built for operations metrics like cycle time, capacity, and slippage. No SQL, no pipeline setup. Built for operations, not generic analytics' (unique attributes + implicit category). Sentence 3 lands on value by contrasting native tools and BI setup time. Structure follows the canvas. |
| c18 | Output labels every customer-facing tagline / message draft — DRAFT, requires human review — not approved finals | PASS | The document opens and closes with 'DRAFT — requires human review and product validation'. Taglines are presented as options with 'I'd recommend this one' framing rather than as approved finals. No messaging is presented as production-ready. |
| c19 | Output addresses where the canvas may shift on pricing — analytics add-on at $15/seat positions Clearpath as a premium overlay (suggesting the buyer values exec visibility highly) which informs the pricing message and channel | PARTIAL | The output references '$3–15K/year discretionary ops budget' in the target customer section and validation question 4 asks 'Is $3–15K/year the right budget range for this buyer, or should we target higher (enterprise) or lower (SMB)?' It raises the pricing question but does not analyze how pricing tier (e.g. $15/seat as premium overlay) affects the positioning message or channel strategy. Partial coverage only. |

### Notes

The output is a strong application of the April Dunford framework — the five-step build-up through competitive alternatives, unique attributes, value mapping, target customer, and market category is well-executed and thorough. The main structural failure is c5: the positioning canvas appears after the messaging and taglines in Step 6, inverting the required order. c9 cannot be evaluated from the chat output alone (no skill definition file is visible). The sales narrative, validation questions, and DRAFT labelling all meet their criteria well. Unique attributes are meaningfully differentiated from Asana/Monday capabilities and mapped to quantified customer outcomes rather than generic claims. The target customer profile and market category are both specific and defensible. The pricing criterion (c19) gets partial credit — budget range is mentioned but the positioning implications of premium-tier pricing are not analysed.
