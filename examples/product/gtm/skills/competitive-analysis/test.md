# Test: Competitive analysis

Scenario: Testing whether the competitive-analysis skill defines a competitive set with all 5 types, produces a comparison table, and identifies strategic opportunities — not just a feature comparison.

## Prompt


/gtm:competitive-analysis for Clearpath in the project management space — we need to understand our competitive position before repositioning for the mid-market.

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
