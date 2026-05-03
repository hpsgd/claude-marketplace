# Test: write-battle-card — enterprise deal with multiple buyer personas

Scenario: Testing the write-battle-card skill with an enterprise deal where objections, proof points, and differentiators must be segmented across three distinct buyer personas (economic, technical, end user).

## Prompt

/gtm:write-battle-card against Salesforce for our CRM product — the deal is a 500-seat enterprise account where the economic buyer (CFO) cares about TCO, the technical buyer (VP Engineering) cares about API extensibility and data migration, and the end users (sales reps) care about mobile UX and speed.

For this card, use the following product reference data (don't leave [confirm] placeholders — fill these in directly):

- **Our product (Pipedeck CRM)**: $65/user/month at Enterprise tier, native iOS/Android apps with offline mode, REST API at 1,000 calls/sec/tenant burst (sustained 200/sec), pre-built integrations: Slack, MS Teams, HubSpot, Zendesk, NetSuite, Workday. Migration tool: Pipedeck Bridge — Salesforce object mapping wizard, dual-write phase, 3-week typical 500-seat migration. Mobile App Store rating 4.7 (15k reviews), Salesforce Mobile rating 3.8 (45k reviews).
- **Salesforce Enterprise tier**: ~$165/user/month list. SI engagement 1-2× first-year licence cost typical at 500 seats ($500k-$1M). Salesforce admin FTE typical at this scale: 1.5 FTE ($180k/yr loaded). API governor: 100k daily calls per org for Enterprise.
- **Win/loss data (last 12 months, internal)**: vs Salesforce we win 62% of deals where TCO is decisive; lose 71% of deals where AppExchange ecosystem breadth is the gating requirement; win 78% of deals where mobile field-rep usability is scored.
- **Enterprise case study**: NorthRiver Logistics, 540 seats, migrated from Salesforce in Q2 2025 — 21-day migration via Bridge, 3-week time-to-productivity, 38% lower 3-year TCO, sales-rep weekly active up 41%.

A few specifics for the response:

- **Single-page TL;DR at top** — one callout block, ≤8 bullets max, scannable in 30 seconds. The detailed sections follow.
- **TCO table with actual dollar figures**: Licence ($65 vs $165/user/month), Implementation ($150k vs $750k for 500 seats), Training, Admin FTE ($60k vs $180k/yr), 3-year total. No placeholders.
- **Technical differentiators (specific)**: name our API rate limit (1000/sec) vs Salesforce (100k/day), name our migration tool (Pipedeck Bridge) vs Salesforce (Data Loader / SI engagement), name our specific integrations (Slack, MS Teams, NetSuite, Workday) vs Salesforce's AppExchange.
- **Mobile differentiators (specific)**: our 4.7 vs Salesforce Mobile 3.8, offline mode supported, gestures (swipe-to-log-call, voice-note transcription).
- **Win/Lose analysis grounded in the win-rate stats above** — not generic. Each claim cites the win-rate %.
- **Proof points section** with NorthRiver case study fully populated (from data above).
- **Multi-stakeholder DEAL DYNAMICS section**: explicit subsection on what to do when CFO (TCO), VP Eng (integration depth), and sales rep (UX) priorities conflict. Sequencing: lead with rep-mobile demo to win usability sentiment, follow with VP-Eng API/migration deep-dive to defuse risk concerns, close with CFO TCO pitch (cheapest *and* better) — explain why this order works.

## Criteria

- [ ] PASS: Objection handling is segmented by buyer persona (CFO, VP Eng, sales reps) not generic
- [ ] PASS: Win/lose analysis is based on specific evidence (deal post-mortems, win rates, feature gaps) not generic claims
- [ ] PASS: TCO comparison includes specific line items (licence, implementation, training, ongoing admin) not just "we're cheaper"
- [ ] PASS: Technical differentiators are stated with specificity (API rate limits, migration tooling, specific integrations)
- [ ] PASS: The card is concise enough for a sales rep to scan in 30 seconds
- [ ] PARTIAL: Proof points (case studies, benchmarks) are current and specific to the enterprise segment
- [ ] PASS: Output is labelled DRAFT and flagged for human review
- [ ] PASS: The card covers one competitor (Salesforce) only, not a multi-competitor overview

## Output expectations

- [ ] PASS: Output's objection / response pairs are SEGMENTED into three sections by buyer persona — CFO (TCO, ROI, pricing transparency), VP Engineering (API extensibility, data migration, integration ecosystem), Sales rep / end user (mobile UX, performance, adoption friction) — NOT a single mixed list
- [ ] PASS: Output's TCO comparison shows specific line items per option — Salesforce licence cost (per-user-per-month at the Enterprise tier), implementation cost (typical SI engagement $X-$Y for 500 seats), training cost, ongoing admin (Salesforce admin FTE typical at this scale), 3-year total TCO; the requester's product line items in the same shape
- [ ] PASS: Output's technical-buyer differentiators are SPECIFIC — API rate limits (e.g. our 100 calls/sec vs Salesforce's 100K daily limit), migration tooling (e.g. named import/export tool, data-mapping wizard), specific pre-built integrations (Slack, MS Teams, named ERPs)
- [ ] PASS: Output's end-user differentiators are concrete — mobile app load time (e.g. "2s vs Salesforce mobile's 6s p95"), offline capability, gestures / UX patterns sales reps care about — with proof points from real benchmarks if available
- [ ] PASS: Output's win/loss analysis is grounded in evidence — references specific deal post-mortems, win-rate statistics, or feature-gap data — NOT generic "we win on UX, lose on ecosystem"
- [ ] PASS: Output is concise enough that a sales rep can scan in 30 seconds — single-page, sectioned by persona, key talking points pulled to the front in bold or callout format
- [ ] PASS: Output includes proof points specific to the enterprise segment — case studies of 500+ seat customers who switched FROM Salesforce or chose the requester's product over Salesforce, with named (or anonymised but specific) revenue / time-savings outcomes
- [ ] PASS: Output covers ONLY Salesforce — does not pivot into HubSpot, Microsoft Dynamics, or other CRMs; the prompt is explicit that this is one-competitor scope
- [ ] PASS: Output is labelled DRAFT — explicitly flagged for sales-enablement / marketing leadership review before deployment to the rep team
- [ ] PARTIAL: Output addresses the multi-stakeholder DEAL DYNAMICS — what to do when the CFO, VP Eng, and rep have conflicting priorities (e.g. CFO wants cheapest, rep wants their preferred UX, VP Eng prioritises integration depth) — sequencing the message and proof points
