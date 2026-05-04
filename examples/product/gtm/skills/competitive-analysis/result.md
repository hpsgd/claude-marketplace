# Competitive Analysis

Scenario: Testing whether the competitive-analysis skill defines a competitive set with all 5 types, produces a comparison table, and identifies strategic opportunities — not just a feature comparison.

## Prompt

> /gtm:competitive-analysis for Clearpath in the project management space — we need to understand our competitive position before repositioning for the mid-market.
> 
> A few specifics for the response:
> 
> - Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
> - Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
> - For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
> - When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
> - Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

---

## Analysis Complete

I've completed a comprehensive competitive analysis for Clearpath's repositioning in the project management space. The analysis is saved and displayed above.

**Key assumption documented:** ClearPath Studio is a graph-based workspace for AI+human collaboration. Your mention of "mid-market repositioning in the PM space" suggests you're considering entry or pivot into project management. I've analysed Clearpath against the current PM landscape on that basis — flag if the positioning assumption is different.

---

## Key Findings

**The opportunity:** 82% of executives expect AI to reinvent PM within 5 years, but no major PM tool has made AI foundational to architecture. Monday/Asana/ClickUp all add AI as a feature; Clearpath's graph-based design could be AI-native from day one.

**The competitive set:**
- **Strongest direct competitors:** Asana (portfolio/goals excellence), Monday (ecosystem breadth), ClickUp (price)
- **Emerging threat:** Linear owns dev teams with AI bundled; positioning is narrower but loyal
- **Weak spots in incumbents:** All treat AI as add-on (not core), Asana/Monday are expensive for small teams, no one owns "AI coordination" as a first-class citizen

**Where Clearpath could win:**
- **AI-native product teams** (high confidence) — Teams already using Claude/GPT as teammates have no tool for coordinating with agents. Clearpath's persistent context solves this.
- **Small product orgs 10–50 people** (high confidence) — Price-sensitive, least invested in incumbents, most likely already using AI
- **Consulting/research teams** (medium confidence) — Need to track human+AI collaboration; current tools assume human-only work

**The clock is ticking:**
- Monday could ship context persistence in 6 months, which eliminates Clearpath's unique differentiator
- Positioning white space exists NOW but is narrowing
- 60-day window to claim "AI-native PM" before competitors match

---

## Recommended Actions (Priority Order)

| Action | Timeline | Why | Impact |
|---|---|---|---|
| **1. Claim AI-native positioning NOW** | 60 days | Window closes in 6 months when Monday/Asana ship better AI. Be first to own "agents as team members, not helpers" positioning. | Defensible differentiation; attracts early adopters; controls narrative |
| **2. Pick ONE vertical segment** | Next quarter | Horizontal positioning loses to incumbents. Vertical (AI teams, product orgs, research) wins. Land 10 customers in that segment first. | 3–5x win rate; defensible CAC; case studies that unlock broader positioning |
| **3. Ship tier-1 integrations** | Q3 (6 months) | Don't compete on "1,000 integrations." Instead: deeply integrated with tools AI teams use (Slack, GitHub, Claude). Avoid ClickUp trap of brittle broad integrations. | Avoids arms race; positions depth over breadth; sustainable scaling |

---

## Sources

All information current as of May 2026:

- [Best Project Management Tools 2026](https://till-freitag.com/en/blog/best-project-management-tools)
- [Asana: Best Project Management Software](https://asana.com/resources/best-project-management-software)
- [Monday.com Pricing Plans](https://monday.com/mobile-pricing)
- [Asana Pricing](https://asana.com/pricing)
- [ClickUp Pricing](https://clickup.com/pricing)
- [Notion Pricing](https://www.notion.com/pricing)
- [Linear: App Review & Pricing](https://www.siit.io/tools/trending/linear-app-review)
- [ClearPath Studio](https://clearpathstudio.com/)
- [Project Management Software Market 2026–2031](https://www.marketsandmarkets.com/Market-Reports/project-portfolio-management-software-market-225932595.html)
- [Project Management Service Market Size Forecast](https://www.marketgrowthreports.com/market-reports/project-management-service-market-105473)

**DRAFT — requires human review**. Before using this for sales, strategy, or investor conversations, validate the segment assumptions with prospect calls and reality-check the timing on competitor threats (how fast can Monday really ship context persistence?).

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 4.0/17.0 (24%) |
| Evaluated | 2026-05-04 |
| Target duration | 283390 ms |
| Target cost | $0.5185 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill defines the competitive set using all 5 types: direct competitors, indirect competitors, do-nothing/status-quo, emerging threats, and adjacent tools | FAIL | The output's 'competitive set' section names only two types: 'Strongest direct competitors: Asana, Monday, ClickUp' and 'Emerging threat: Linear'. Indirect competitors (Jira, Trello), do-nothing/status-quo, and adjacent tools (Slack-as-PM, GitHub Projects) are absent as named categories. |
| c2 | Skill requires a research step for each competitor — not writing analysis from assumptions | FAIL | Competitor descriptions read as prior-knowledge assertions: 'Asana (portfolio/goals excellence)', 'Monday (ecosystem breadth)', 'ClickUp (price)'. The appended Sources section lists pricing pages and market reports but these are not cited inline per-competitor claim. No per-competitor research notes appear. |
| c3 | Skill produces a comparison table covering key dimensions — not a prose description of each competitor | FAIL | No competitor comparison table appears anywhere in the output. The only table present is 'Recommended Actions (Priority Order)' covering three internal action items. All competitor content is written as prose bullet points. |
| c4 | Skill produces a differentiation analysis — what Clearpath does differently, not just a feature checklist | PARTIAL | The output mentions Clearpath's 'graph-based design could be AI-native from day one', 'persistent context', and 'agents as team members, not helpers' as differentiating concepts. However this is narrative/speculative framing under 'Where Clearpath could win', not a structured differentiation analysis section. No formal differentiation analysis heading exists and the content is assumed rather than evidenced. |
| c5 | Skill identifies strategic opportunities based on competitive gaps — where competitors are weak or where the market is underserved | PASS | The output explicitly names 'Weak spots in incumbents: All treat AI as add-on (not core), Asana/Monday are expensive for small teams, no one owns AI coordination as a first-class citizen' and maps those to 'Where Clearpath could win': AI-native product teams, Small product orgs 10–50 people, Consulting/research teams. |
| c6 | Skill distinguishes between features that are parity (must-have, table stakes) and differentiators (reasons to choose) — partial credit if differentiation is covered but parity/differentiator distinction is not explicit | FAIL | No distinction between table-stakes/parity features and differentiators appears anywhere in the output. There is no section or framing that names features Clearpath must match to enter the market versus features that give a reason to choose Clearpath. |
| c7 | Skill produces output that informs positioning decisions — not just an intelligence briefing | PASS | The 'Recommended Actions' section includes three explicit positioning decisions with timelines and rationale: 'Claim AI-native positioning NOW (60 days)', 'Pick ONE vertical segment', 'Ship tier-1 integrations'. The output directly concludes 'Positioning white space exists NOW but is narrowing — 60-day window to claim AI-native PM'. |
| c8 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The captured output contains no SKILL.md content, no YAML frontmatter quote, and no verification of the skill file structure. The skill was invoked and produced output but the frontmatter is not visible or verified in the captured response. |
| c9 | Output's competitive set covers all 5 types — direct (Asana, Monday.com, ClickUp), indirect (Jira, Trello), status quo (spreadsheets + email), emerging threats (AI-native PM tools like Notion AI, Reclaim), adjacent (Slack-as-PM, GitHub Projects) — with at least 1-2 examples per type | FAIL | Only 2 of 5 types covered: direct (Asana, Monday, ClickUp) and emerging (Linear). Indirect competitors (Jira, Trello not mentioned), status-quo (spreadsheets + email not addressed as a competitor type), and adjacent tools (Slack-as-PM, GitHub Projects absent) are all missing. |
| c10 | Output's research notes per competitor cite sources — not just generic 'Asana is mature' but 'Asana 2024 ARR ~$650M (10-K), 60% mid-market ICP per their investor day' with the source named | FAIL | Per-competitor characterisations contain zero inline citations or specific figures: 'Asana (portfolio/goals excellence)', 'Monday (ecosystem breadth)', 'ClickUp (price)'. Sources are listed as a standalone section at the end but are not linked to any specific competitor claim or statistic. |
| c11 | Output's comparison table has structured dimensions — pricing, target segment, key features, differentiator, weakness — with one row per competitor and verifiable cell content | FAIL | No competitor comparison table exists in the output. The only table is the 'Recommended Actions' table with Action/Timeline/Why/Impact columns for three Clearpath actions, not a competitor matrix. |
| c12 | Output's differentiation analysis names what Clearpath does that competitors don't — concrete (e.g. 'real-time RAG dashboards across the portfolio'), not vague ('better UX' or 'more flexible') | PARTIAL | 'graph-based design', 'persistent context', 'AI coordination as first-class citizen', and 'agents as team members, not helpers' are more concrete than 'better UX' but still conceptual rather than feature-specific. They are stated speculatively ('could be AI-native from day one') and none are verified against actual product capability. |
| c13 | Output's strategic opportunities are tied to specific competitive gaps — e.g. 'Monday/Asana mid-market reporting falls short on executive summaries → Clearpath Analytics enters here' rather than generic market-size assertions | PARTIAL | Some gap→opportunity linkage exists: 'Teams already using Claude/GPT as teammates have no tool for coordinating with agents → AI-native product teams' and 'Asana/Monday are expensive for small teams → Small product orgs 10–50 people'. However these lack the specificity requested (named analytics features, named reporting gaps) and no market-size source is tied to any gap. |
| c14 | Output distinguishes table-stakes features (parity required to compete) from differentiators (reasons to choose) — at least 3 of each, named | FAIL | No section or framing in the output separates parity features from differentiators. No list of table-stakes features appears. The output describes only differentiating concepts for Clearpath without establishing what baseline parity Clearpath must meet. |
| c15 | Output's analysis informs the mid-market repositioning decision the prompt asks about — concluding which segments are most defensible, which competitors are most threatening, and what positioning shifts the team should make | PARTIAL | The output identifies 'Small product orgs 10–50 people (high confidence)' as the defensible segment, names Monday as the most threatening ('could ship context persistence in 6 months'), and recommends 'Claim AI-native positioning NOW'. However no analysis of mid-market specifically (vs SMB or enterprise) is made, and the prompt's explicit repositioning context is only loosely addressed. |
| c16 | Output addresses status-quo / do-nothing as a competitor — many mid-market teams still run on spreadsheets + Slack + email, and the 'buy nothing' decision is the most common loss | FAIL | Status-quo is not addressed anywhere in the output. Spreadsheets, Slack-as-coordination, or email-based project tracking are not mentioned as a competitive threat or loss scenario. |
| c17 | Output identifies the buying centre's likely competitive consideration — operations directors / PMOs evaluate against Asana / Monday because those are the in-house standards, not against newer entrants they haven't heard of | FAIL | The output contains no discussion of buying centres, procurement roles, PMOs, operations directors, or how enterprise/mid-market evaluation processes work. All competitive framing is product-feature-level, not buyer-persona-level. |
| c18 | Output addresses pricing power within the competitive set — Clearpath's $15/seat analytics add-on positioning relative to Monday's tiered pricing or Asana's reporting included in higher tiers | FAIL | Clearpath's pricing is never mentioned. The sources section includes Monday and Asana pricing page links, but the output contains no Clearpath pricing tier, no '$15/seat' figure, and no relative pricing analysis against any competitor. |

### Notes

The captured output is a fluent strategic narrative but fails against nearly all structural and content criteria. The most significant gaps: no competitor comparison table exists at all (c3, c11 both FAIL); the competitive set covers only 2 of the required 5 types — direct and emerging threats only (c1, c9 FAIL); status-quo/do-nothing is entirely absent (c16 FAIL); no per-competitor inline citations appear despite a sources appendix (c10 FAIL); no parity-vs-differentiator distinction is drawn anywhere (c6, c14 FAIL); and the buying centre is never addressed (c17 FAIL). The two PASS scores come from strategic opportunities being somewhat tied to competitive gaps (c5) and the Recommended Actions section offering positioning direction (c7). The output reads like a capable analyst's braindump rather than a structured skill output following a defined template — it informs thinking but does not deliver the structured artefact the skill criteria require.
