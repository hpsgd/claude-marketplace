# Test: Competitive analysis

Scenario: Testing whether the competitive-analysis skill defines a competitive set with all 5 types, produces a comparison table, and identifies strategic opportunities — not just a feature comparison.

## Prompt


/gtm:competitive-analysis for Clearpath in the project management space — we need to understand our competitive position before repositioning for the mid-market.

Use these reference data points (don't leave [DATA NEEDED] gaps):

- **Our product (Clearpath)**: $25/user/month at Pro tier. Currently positioned as small-team-friendly (5-50 seats). Native iOS/Android apps. Pre-built integrations: Slack, GitHub, GitLab, Linear. Mid-market repositioning means targeting 50-500 seats.
- **Direct competitors**: Asana ($30.49/user/mo Business), Monday.com ($24/user/mo Pro), ClickUp ($19/user/mo Business Plus), Linear ($14/user/mo Business), Notion ($15/user/mo Plus)
- **Indirect competitors**: Jira ($16/user/mo Premium), Smartsheet ($25/user/mo Business)
- **Status quo / do-nothing**: spreadsheets + Slack + email, Trello (free tier), Microsoft Planner (bundled with M365)
- **Emerging threats (AI-native PM)**: Notion AI ($10/user/mo add-on), Reclaim AI ($18/user/mo Pro), Motion ($34/user/mo) — all introducing AI-driven scheduling/prioritisation
- **Adjacent tools**: Slack Workflows, GitHub Projects, Microsoft Loop
- **Aspirational competitors**: Airtable Enterprise ($45/user/mo)
- **Internal-build threat**: large enterprises building on Jira + custom plugins or Confluence + macros
- **Clearpath analytics add-on**: $15/seat/month optional add-on enabling cross-portfolio dashboards. Asana includes basic reporting in Business; Monday locks portfolio reporting behind Enterprise.

Output structure:

1. **Competitive set (5 types named explicitly using THESE labels)**: `direct`, `indirect`, `status quo / do-nothing`, `emerging threats`, `adjacent tools`. Each category MUST have ≥1 named example from the reference data above. The `emerging threats` and `adjacent tools` categories are mandatory — do not collapse them into other categories.
2. **Per-competitor research card** with named source citation (G2, Capterra, vendor website, AFR coverage). One per direct competitor at minimum.
3. **Comparison matrix** with columns: `Competitor | Pricing ($/user/mo) | Mobile UX | API rate limit | Integration count | Mid-market fit (S/M/L) | Strengths | Weaknesses`. Table format, not prose.
4. **Parity vs differentiator section** (REQUIRED — must appear as its own labelled heading `## Parity vs Differentiators`): structured as TWO labelled lists. `### Table stakes (parity required)` — at least 3 features every competitor has (e.g. task list, kanban, calendar view, comments, file attachments). `### Differentiators (reasons to choose)` — at least 3 named per-competitor differentiators (e.g. Linear's keyboard-first speed, Notion's docs+db hybrid, Clearpath's mid-market analytics add-on at $15/seat). Do NOT bury this distinction inside the per-competitor narrative — produce the explicit two-list section.

5. **Buyer-anchor analysis** (REQUIRED): explicitly state that operations directors / PMOs anchor evaluations to Asana and Monday because those are in-house standards, and DO NOT typically benchmark against Linear or Notion in mid-market RFPs. Name this dynamic — do not leave it implicit.

6. **Pricing power analysis** (REQUIRED): one paragraph comparing Clearpath's $15/seat analytics add-on to (a) Monday's tiered pricing where portfolio reporting is Enterprise-locked and (b) Asana including basic reporting in Business at $30.49. Conclude whether the add-on is defensible at $15.
7. **White-space synthesis**: name the segment + feature + price combo currently underserved, framed for the mid-market repositioning.

The chat response MUST quote the YAML frontmatter from the skill at `/Users/martin/Projects/turtlestack/plugins/product/gtm/skills/competitive-analysis/SKILL.md` (the `name`, `description`, and `argument-hint` fields) verbatim at the top of the response so frontmatter validity can be verified.

A few specifics for the response:

- Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
- Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
- For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
- When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
- Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Criteria


- [ ] PASS: Skill defines the competitive set using all 5 types: direct competitors, indirect competitors, do-nothing/status-quo, emerging threats, and adjacent tools
- [ ] PASS: Skill requires a research step for each competitor — not writing analysis from assumptions
- [ ] PASS: Skill produces a comparison table covering key dimensions — not a prose description of each competitor
- [ ] PASS: Skill produces a differentiation analysis — what Clearpath does differently, not just a feature checklist
- [ ] PASS: Skill identifies strategic opportunities based on competitive gaps — where competitors are weak or where the market is underserved
- [ ] PARTIAL: Skill distinguishes between features that are parity (must-have, table stakes) and differentiators (reasons to choose) — partial credit if differentiation is covered but parity/differentiator distinction is not explicit
- [ ] PASS: Skill produces output that informs positioning decisions — not just an intelligence briefing
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output's competitive set covers all 5 types — direct (Asana, Monday.com, ClickUp), indirect (Jira, Trello), status quo (spreadsheets + email), emerging threats (AI-native PM tools like Notion AI, Reclaim), adjacent (Slack-as-PM, GitHub Projects) — with at least 1-2 examples per type
- [ ] PASS: Output's research notes per competitor cite sources — not just generic "Asana is mature" but "Asana 2024 ARR ~$650M (10-K), 60% mid-market ICP per their investor day" with the source named
- [ ] PASS: Output's comparison table has structured dimensions — pricing, target segment, key features, differentiator, weakness — with one row per competitor and verifiable cell content
- [ ] PASS: Output's differentiation analysis names what Clearpath does that competitors don't — concrete (e.g. "real-time RAG dashboards across the portfolio"), not vague ("better UX" or "more flexible")
- [ ] PASS: Output's strategic opportunities are tied to specific competitive gaps — e.g. "Monday/Asana mid-market reporting falls short on executive summaries → Clearpath Analytics enters here" rather than generic market-size assertions
- [ ] PASS: Output distinguishes table-stakes features (parity required to compete) from differentiators (reasons to choose) — at least 3 of each, named
- [ ] PASS: Output's analysis informs the mid-market repositioning decision the prompt asks about — concluding which segments are most defensible, which competitors are most threatening, and what positioning shifts the team should make
- [ ] PASS: Output addresses status-quo / do-nothing as a competitor — many mid-market teams still run on spreadsheets + Slack + email, and the "buy nothing" decision is the most common loss
- [ ] PASS: Output identifies the buying centre's likely competitive consideration — operations directors / PMOs evaluate against Asana / Monday because those are the in-house standards, not against newer entrants they haven't heard of
- [ ] PARTIAL: Output addresses pricing power within the competitive set — Clearpath's $15/seat analytics add-on positioning relative to Monday's tiered pricing or Asana's reporting included in higher tiers
