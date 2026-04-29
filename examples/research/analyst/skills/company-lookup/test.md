# Test: company-lookup skill

Scenario: a business analyst needs to research an unfamiliar company before a client meeting.

## Prompt

"Can you look up Palantir Technologies for me? I need to understand what they do, their business model, and any recent developments before a meeting tomorrow."

## Criteria

- [ ] PASS: Skill defines a clear trigger or usage context (when to invoke this skill)
- [ ] PASS: Skill specifies what sources to check (e.g. company website, LinkedIn, Crunchbase, news)
- [ ] PASS: Skill defines an output structure with named sections (not freeform)
- [ ] PASS: Output structure includes business model or "what they do" section
- [ ] PASS: Output structure includes financials or funding section
- [ ] PASS: Output structure includes recent news or developments section
- [ ] PARTIAL: Skill includes guidance on assessing source credibility or recency
- [ ] SKIP: Skill references collaboration with other agents (only relevant if plugin includes multiple agents)

## Output expectations

- [ ] PASS: Output covers Palantir Technologies specifically — including the named entity (NYSE: PLTR, headquartered Denver CO, founded 2003 by Karp / Lonsdale / Cohen / Thiel) — not generic placeholders
- [ ] PASS: Output's "What they do" section names the two main product lines (Gotham for government / defence, Foundry for commercial) and the AIP layer for AI applications — with a 1-2 sentence explanation of the customer problem each solves
- [ ] PASS: Output's business model section explains revenue mix — government vs commercial split (currently still skewing government but commercial growing), contract structures (multi-year, large-deal-driven), and the recent push into AI-enabled software
- [ ] PASS: Output's financials section includes recent quarterly revenue (last reported quarter), YoY growth, profitability status (recently profitable), and market cap — with the source date stamped (e.g. "Q4 2024, source: investor presentation")
- [ ] PASS: Output's recent news / developments covers the last 6-12 months — major contracts, product launches (e.g. AIP), executive moves, partnerships, controversies — relevant to a meeting-prep context
- [ ] PASS: Output cites specific sources per claim — palantir.com, SEC 10-K filings, recent earnings releases, named news outlets — not "based on public sources"
- [ ] PASS: Output addresses the controversies — Palantir's history with surveillance / immigration / military contracts is a known reputation factor; relevant to a meeting if the user might raise it
- [ ] PASS: Output's structure has named sections — Overview, What They Do, Business Model, Financials, Recent Developments, Key People, Sources — not freeform prose
- [ ] PASS: Output flags any source that's >12 months old as potentially stale — Palantir moves fast and recent quarters matter
- [ ] PARTIAL: Output addresses meeting-prep angles — likely conversation topics (commercial vs government strategy, AIP positioning, Karp's public statements) rather than just facts
