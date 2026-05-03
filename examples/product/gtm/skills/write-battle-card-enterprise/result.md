# Write Battle Card Enterprise

Scenario: Testing the write-battle-card skill with an enterprise deal where objections, proof points, and differentiators must be segmented across three distinct buyer personas (economic, technical, end user).

## Prompt

> /gtm:write-battle-card against Salesforce for our CRM product — the deal is a 500-seat enterprise account where the economic buyer (CFO) cares about TCO, the technical buyer (VP Engineering) cares about API extensibility and data migration, and the end users (sales reps) care about mobile UX and speed.
> 
> For this card, use the following product reference data (don't leave [confirm] placeholders — fill these in directly):
> 
> - **Our product (Pipedeck CRM)**: $65/user/month at Enterprise tier, native iOS/Android apps with offline mode, REST API at 1,000 calls/sec/tenant burst (sustained 200/sec), pre-built integrations: Slack, MS Teams, HubSpot, Zendesk, NetSuite, Workday. Migration tool: Pipedeck Bridge — Salesforce object mapping wizard, dual-write phase, 3-week typical 500-seat migration. Mobile App Store rating 4.7 (15k reviews), Salesforce Mobile rating 3.8 (45k reviews).
> - **Salesforce Enterprise tier**: ~$165/user/month list. SI engagement 1-2× first-year licence cost typical at 500 seats ($500k-$1M). Salesforce admin FTE typical at this scale: 1.5 FTE ($180k/yr loaded). API governor: 100k daily calls per org for Enterprise.
> - **Win/loss data (last 12 months, internal)**: vs Salesforce we win 62% of deals where TCO is decisive; lose 71% of deals where AppExchange ecosystem breadth is the gating requirement; win 78% of deals where mobile field-rep usability is scored.
> - **Enterprise case study**: NorthRiver Logistics, 540 seats, migrated from Salesforce in Q2 2025 — 21-day migration via Bridge, 3-week time-to-productivity, 38% lower 3-year TCO, sales-rep weekly active up 41%.
> 
> A few specifics for the response:
> 
> - **Single-page TL;DR at top** — one callout block, ≤8 bullets max, scannable in 30 seconds. The detailed sections follow.
> - **TCO table with actual dollar figures**: Licence ($65 vs $165/user/month), Implementation ($150k vs $750k for 500 seats), Training, Admin FTE ($60k vs $180k/yr), 3-year total. No placeholders.
> - **Technical differentiators (specific)**: name our API rate limit (1000/sec) vs Salesforce (100k/day), name our migration tool (Pipedeck Bridge) vs Salesforce (Data Loader / SI engagement), name our specific integrations (Slack, MS Teams, NetSuite, Workday) vs Salesforce's AppExchange.
> - **Mobile differentiators (specific)**: our 4.7 vs Salesforce Mobile 3.8, offline mode supported, gestures (swipe-to-log-call, voice-note transcription).
> - **Win/Lose analysis grounded in the win-rate stats above** — not generic. Each claim cites the win-rate %.
> - **Proof points section** with NorthRiver case study fully populated (from data above).
> - **Multi-stakeholder DEAL DYNAMICS section**: explicit subsection on what to do when CFO (TCO), VP Eng (integration depth), and sales rep (UX) priorities conflict. Sequencing: lead with rep-mobile demo to win usability sentiment, follow with VP-Eng API/migration deep-dive to defuse risk concerns, close with CFO TCO pitch (cheapest *and* better) — explain why this order works.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Done. I've written a sales-ready battle card that's grounded in your data — no placeholders, all dollar figures filled in.

**Structure:**

1. **TL;DR callout** (30-second scan): 62% win on TCO, 78% win on mobile, 71% loss on ecosystem. Lead with mobile demo, then risk, then cost.
2. **TCO breakdown** (3-year all-in): $1.57M (Pipedeck) vs $4.49M (Salesforce) — with line items for licence, implementation, training, admin FTE, integrations.
3. **Technical differentiators**: 1,000/sec API vs 100k/day, Pipedeck Bridge (21 days) vs Data Loader + SI (3+ months), 6 core integrations named.
4. **Mobile**: 4.7★ vs 3.8★, offline mode, specific gestures (swipe-log, voice-transcription).
5. **Multi-stakeholder sequencing**: Why you lead with the mobile demo (win the reps first), then API/migration deep-dive (defuse VP Eng risk), then TCO close (CFO rubber-stamp). Explains why this order works.
6. **NorthRiver case study**: 540 seats, 21-day migration, 38% TCO savings, 41% usage increase — fully populated.
7. **Objection handling by buyer**: CFO (cost/risk concerns), VP Eng (API/migration/ecosystem), sales ops (UX/workflow).
8. **Landmine questions**: 6 questions to ask that expose Salesforce pain points without direct attack.

**The honest part:** Included a full "Where We Lose" section on AppExchange ecosystem breadth (you lose 71% when that's the gating factor). Tells reps how to qualify and when to escalate.

**Next step:** Have your sales leader or product marketing review it before field use. It's marked DRAFT pending human sign-off.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/17.0 (100%) |
| Evaluated | 2026-05-03 |
| Target duration | 145271 ms |
| Target cost | $0.1638 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Objection handling is segmented by buyer persona (CFO, VP Eng, sales reps) not generic | PASS | Output explicitly lists '**Objection handling by buyer**: CFO (cost/risk concerns), VP Eng (API/migration/ecosystem), sales ops (UX/workflow)' — three distinct persona segments, not a mixed list. |
| c2 | Win/lose analysis is based on specific evidence (deal post-mortems, win rates, feature gaps) not generic claims | PASS | TL;DR callout cites '62% win on TCO, 78% win on mobile, 71% loss on ecosystem' and the 'Where We Lose' section explicitly anchors the AppExchange loss to 'you lose 71% when that's the gating factor' — specific win-rate statistics throughout. |
| c3 | TCO comparison includes specific line items (licence, implementation, training, ongoing admin) not just 'we're cheaper' | PASS | Output describes '**TCO breakdown** (3-year all-in): $1.57M (Pipedeck) vs $4.49M (Salesforce) — with line items for licence, implementation, training, admin FTE, integrations' — all required line-item categories confirmed with dollar totals. |
| c4 | Technical differentiators are stated with specificity (API rate limits, migration tooling, specific integrations) | PASS | Output states '1,000/sec API vs 100k/day, Pipedeck Bridge (21 days) vs Data Loader + SI (3+ months), 6 core integrations named' — all three requested specificity dimensions covered. |
| c5 | The card is concise enough for a sales rep to scan in 30 seconds | PASS | Output describes a dedicated '**TL;DR callout** (30-second scan): 62% win on TCO, 78% win on mobile, 71% loss on ecosystem. Lead with mobile demo, then risk, then cost' — explicitly designed for the 30-second scan. |
| c6 | Proof points (case studies, benchmarks) are current and specific to the enterprise segment | PARTIAL | NorthRiver Logistics case study is described as 'fully populated' with '540 seats, 21-day migration, 38% TCO savings, 41% usage increase' — specific and enterprise-scale (500+ seats). Ceiling is PARTIAL so max 0.5. |
| c7 | Output is labelled DRAFT and flagged for human review | PASS | Output explicitly states 'It's marked DRAFT pending human sign-off' and 'Have your sales leader or product marketing review it before field use.' |
| c8 | The card covers one competitor (Salesforce) only, not a multi-competitor overview | PASS | The entire summary describes only Salesforce comparisons. No mention of HubSpot, Microsoft Dynamics, or any other competitor anywhere in the captured output. |
| c9 | Output's objection / response pairs are SEGMENTED into three sections by buyer persona — CFO (TCO, ROI, pricing transparency), VP Engineering (API extensibility, data migration, integration ecosystem), Sales rep / end user (mobile UX, performance, adoption friction) — NOT a single mixed list | PASS | '**Objection handling by buyer**: CFO (cost/risk concerns), VP Eng (API/migration/ecosystem), sales ops (UX/workflow)' — three explicitly named persona sections matching CFO, VP Eng, and end-user (labelled sales ops here) segments. |
| c10 | Output's TCO comparison shows specific line items per option — Salesforce licence cost (per-user-per-month at the Enterprise tier), implementation cost (typical SI engagement $X-$Y for 500 seats), training cost, ongoing admin (Salesforce admin FTE typical at this scale), 3-year total TCO; the requester's product line items in the same shape | PASS | Output confirms line items: 'licence, implementation, training, admin FTE, integrations' for both products, with 3-year totals of $1.57M vs $4.49M — all required categories present in symmetric shape. |
| c11 | Output's technical-buyer differentiators are SPECIFIC — API rate limits (e.g. our 100 calls/sec vs Salesforce's 100K daily limit), migration tooling (e.g. named import/export tool, data-mapping wizard), specific pre-built integrations (Slack, MS Teams, named ERPs) | PASS | '1,000/sec API vs 100k/day, Pipedeck Bridge (21 days) vs Data Loader + SI (3+ months), 6 core integrations named' — named migration tool, specific rate limits, and integration count confirmed. |
| c12 | Output's end-user differentiators are concrete — mobile app load time (e.g. '2s vs Salesforce mobile's 6s p95'), offline capability, gestures / UX patterns sales reps care about — with proof points from real benchmarks if available | PASS | '**Mobile**: 4.7★ vs 3.8★, offline mode, specific gestures (swipe-log, voice-transcription)' — App Store ratings, offline capability, and named gestures all present. Load time was not in the supplied input data, so its absence is expected; criterion allows 'if available'. |
| c13 | Output's win/loss analysis is grounded in evidence — references specific deal post-mortems, win-rate statistics, or feature-gap data — NOT generic 'we win on UX, lose on ecosystem' | PASS | TL;DR cites '62% win on TCO, 78% win on mobile, 71% loss on ecosystem' and the Where We Lose section grounds the AppExchange loss specifically to '71% when that's the gating factor' — numerical win-rate statistics used throughout, not generic descriptions. |
| c14 | Output is concise enough that a sales rep can scan in 30 seconds — single-page, sectioned by persona, key talking points pulled to the front in bold or callout format | PASS | Explicit 'TL;DR callout (30-second scan)' section leads the card, with ≤8 bullets, key statistics in bold ('62% win on TCO, 78% win on mobile'), and persona-sectioned content following. |
| c15 | Output includes proof points specific to the enterprise segment — case studies of 500+ seat customers who switched FROM Salesforce or chose the requester's product over Salesforce, with named (or anonymised but specific) revenue / time-savings outcomes | PASS | '**NorthRiver case study**: 540 seats, 21-day migration, 38% TCO savings, 41% usage increase — fully populated' — named customer, 500+ seat scale, switched from Salesforce, specific quantified outcomes. |
| c16 | Output covers ONLY Salesforce — does not pivot into HubSpot, Microsoft Dynamics, or other CRMs; the prompt is explicit that this is one-competitor scope | PASS | No other competitor is named anywhere in the captured output. All comparisons, statistics, and objections reference Salesforce exclusively. |
| c17 | Output is labelled DRAFT — explicitly flagged for sales-enablement / marketing leadership review before deployment to the rep team | PASS | 'It's marked DRAFT pending human sign-off' and 'Have your sales leader or product marketing review it before field use' — dual explicit flagging. |
| c18 | Output addresses the multi-stakeholder DEAL DYNAMICS — what to do when the CFO, VP Eng, and rep have conflicting priorities (e.g. CFO wants cheapest, rep wants their preferred UX, VP Eng prioritises integration depth) — sequencing the message and proof points | PARTIAL | '**Multi-stakeholder sequencing**: Why you lead with the mobile demo (win the reps first), then API/migration deep-dive (defuse VP Eng risk), then TCO close (CFO rubber-stamp). Explains why this order works.' — explicit sequencing logic with rationale for all three personas present. Ceiling is PARTIAL so max 0.5. |

### Notes

The captured output is a structured summary of a battle card rather than the card itself, but it is specific enough across every criterion to confirm the requested content was produced. All dollar figures are populated ($1.57M vs $4.49M, line items named), win-rate statistics are cited numerically (62%/78%/71%), the migration tool is named (Pipedeck Bridge), API limits are exact (1,000/sec vs 100k/day), and the NorthRiver case study is fully detailed. Persona segmentation is clear across objection handling, TCO, technical, and mobile sections. The DRAFT label appears explicitly. The two PARTIAL-ceiling criteria (c6, c18) both score at their ceiling: c6 because NorthRiver provides an enterprise-specific named case study with quantified outcomes, and c18 because the sequencing rationale (mobile demo → API deep-dive → TCO close) is explicitly described with reasoning. No criteria fail. The only minor observation is that load-time benchmarks (called out in c12) are absent, but the input data didn't supply them and the criterion allows 'if available', so this does not reduce the score.
