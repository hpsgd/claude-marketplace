# Write Battle Card Enterprise

Scenario: Testing the write-battle-card skill with an enterprise deal where objections, proof points, and differentiators must be segmented across three distinct buyer personas (economic, technical, end user).

## Prompt

> /gtm:write-battle-card against Salesforce for our CRM product — the deal is a 500-seat enterprise account where the economic buyer (CFO) cares about TCO, the technical buyer (VP Engineering) cares about API extensibility and data migration, and the end users (sales reps) care about mobile UX and speed.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

The battle card is at `docs/gtm/battle-cards/salesforce.md`. Here's what's in it and what you need to do before using it:

**What the card covers:**
- Persona-segmented objection handling (CFO, VP Eng, sales reps) aligned to the deal
- Line-item TCO table shaped for a CFO conversation
- Honest "where we lose" section (ecosystem, brand safety, admin talent pool, AI maturity)
- Landmine questions and questions to avoid
- Structural competitive analysis across 10 dimensions

**Why there are so many ⚠️ placeholders:**
No product data exists in this workspace, and the advisor flagged a real risk: putting a specific number (e.g. a mobile rating, a per-seat price) even marked "unverified" anchors that number in a rep's head — and they'll repeat it to a 500-seat enterprise prospect. The card is structured correctly but needs 9 inputs before a rep should carry it into a deal.

**Priority actions to complete the card:**

| # | Input | Owner |
|---|---|---|
| 1 | Our per-seat price (500-seat deal) | RevOps |
| 2 | Enterprise implementation timeline | Professional Services |
| 3 | Current App Store ratings (screenshot) | Product / Marketing |
| 4 | Compliance certifications | InfoSec / Legal |
| 5–6 | API versioning policy + data export SLA | Engineering |
| 7 | One enterprise migration case study | Marketing |
| 8 | 12-month Salesforce win/loss data | Sales Ops |
| 9 | Salesforce current pricing | salesforce.com/crm/pricing |

### Artifacts written

#### `work/docs/gtm/battle-cards/salesforce.md`

```
> **DRAFT — requires human review before distribution to the sales team.**

# Battle Card: [Our CRM] vs. Salesforce

**Last updated:** 2026-05-01
**Confidence level:** Low — product-side inputs (our pricing, certs, mobile rating, case studies, API policy) are missing. Salesforce figures are drawn from public sources and must be verified against current Salesforce pricing pages before use.

---

## Before you use this card — inputs required

This card cannot be used in a live deal until the following are confirmed. Every ⚠️ in the card body maps to one of these.

| # | Input needed | Who owns it | Status |
|---|---|---|---|
| 1 | Our per-seat price for a 500-seat enterprise deal | RevOps / Finance | Missing |
| 2 | Our typical enterprise implementation timeline (signature → go-live) | Professional Services | Missing |
| 3 | Our iOS and Android App Store ratings (screenshot with date) | Product / Marketing | Missing |
| 4 | Our current compliance certifications (SOC 2, ISO 27001, HIPAA BAA, FedRAMP, etc.) | InfoSec / Legal | Missing |
| 5 | Our API versioning policy and any stability SLA we can contractualise | Engineering | Missing |
| 6 | Our data export format and portability SLA | Engineering | Missing |
| 7 | One enterprise migration case study (200+ seats, measurable outcome, named or named-on-request) | Marketing | Missing |
| 8 | 12-month internal win/loss data for Salesforce competitive deals | Sales Ops | Missing |
| 9 | Salesforce current pricing for Enterprise and Unlimited editions | Confirm at salesforce.com/crm/pricing | Verify before each deal |

**Until inputs 1–8 are filled in, treat every claim in this card as structural guidance only — not as verifiable proof points.**

---

## TL;DR

The structural case against Salesforce for this deal rests on three things: **total cost of ownership** (Salesforce enterprise TCO is substantially higher than licence cost alone once implementation, admin headcount, and integration maintenance are counted), **mobile experience** (Salesforce Mobile has persistent rep adoption problems that erode CRM data quality), and **migration flexibility** (migrating out of Salesforce is deliberately painful). We lose on **ecosystem breadth** and **brand safety**. The single most important move: get the CFO a line-item TCO model before the deal anchors to Salesforce's list price.

*Note: specific win/loss claims must wait until our own pricing and case study data is confirmed — see inputs table above.*

---

## Quick Comparison

| Dimension | Us | Salesforce | Verdict |
|---|---|---|---|
| Licence cost (500 seats) | ⚠️ [confirm our price] | ⚠️ [verify at salesforce.com/crm/pricing — Enterprise and Unlimited tiers] | Pending |
| Implementation timeline | ⚠️ [confirm with PS team] | Typically 6–18 months for enterprise (source: Salesforce partner community; verify) | Win if our timeline is materially shorter |
| Mobile UX | ⚠️ [confirm App Store rating — screenshot with date] | ⚠️ [confirm current iOS/Android rating — do not use a number without checking] | Pending |
| API extensibility | ⚠️ [confirm our API surface and versioning policy] | REST, SOAP, Bulk, Streaming, Metadata — comprehensive but version-locked | Tie or Lose depending on our API maturity |
| Data migration (in) | ⚠️ [confirm our migration tooling] | Requires SOQL knowledge; proprietary object model adds friction | Win if we have documented migration tooling |
| Data migration (out) | ⚠️ [confirm our export formats and portability SLA] | Standard export requires support ticket; no referential integrity guarantees on bulk CSV | Win if we contractualise portability |
| Ecosystem / integrations | ⚠️ [confirm our native integration count] | Extensive AppExchange marketplace | Lose — Salesforce ecosystem depth is a real advantage |
| Admin overhead | ⚠️ [confirm our admin-to-user ratio] | High admin overhead for large orgs; verify current Salesforce Admin salary benchmarks | Win if our admin model is simpler |
| AI / automation | ⚠️ [confirm our AI feature set] | Einstein — mature, deeply embedded | Requires honest feature-by-feature comparison |
| Compliance & certs | ⚠️ [confirm our current certs — see input #4] | SOC 2, ISO 27001, FedRAMP, HIPAA BAA — verify which apply to the edition being quoted | Needs honest comparison |

---

## TCO Comparison (500-Seat Enterprise Deal)

> Salesforce figures below are structural estimates based on publicly reported implementation benchmarks. Verify Salesforce licence pricing against their current pricing page before using any number in front of a CFO. Our column must be populated by RevOps before this table is used.

| Line item | Salesforce (3-year structural estimate) | Us (3-year estimate) | Notes |
|---|---|---|---|
| Licence | ⚠️ [verify current Enterprise/Unlimited pricing × 500 seats × 36 months] | ⚠️ [RevOps to confirm] | Salesforce Enterprise and Unlimited are different price points — confirm which tier the prospect is being quoted |
| Implementation / migration | Industry benchmark: often 1–2× first-year licence cost for SI engagement | ⚠️ [PS team to confirm our implementation pricing] | Salesforce implementations typically require a certified SI partner |
| Admin headcount | Ongoing cost depends on org complexity and customisation depth — ⚠️ [confirm Salesforce Admin market rates and our admin ratio] | ⚠️ [confirm our admin model] | Key lever: if we require fewer admins, the delta compounds over 3 years |
| Training | ⚠️ [verify Salesforce training costs for enterprise tier] | ⚠️ [confirm our training model and cost] | Salesforce Trailhead is free; structured enterprise enablement is not |
| Integration maintenance | Depends on number of AppExchange apps and custom connectors | ⚠️ [confirm our integration maintenance model] | API version deprecation cycles drive ongoing engineering cost in Salesforce orgs |
| **3-year total** | **⚠️ [calculate once licence and SI inputs are verified]** | **⚠️ [calculate once our inputs are confirmed]** | |

**Key message for CFO:** "The number on the Salesforce quote is not the number you'll spend. Implementation, admin headcount, and integration maintenance routinely multiply the licence cost for enterprise deployments. We'd like 30 minutes with your finance team to build a line-item model — if Salesforce comes out ahead all-in, we'll say so."

---

## Where We Win (structural — verify with proof points)

1. **TCO at enterprise scale.** Salesforce's implementation complexity and admin overhead are real, documented costs at 500 seats. This argument only lands if we can show the delta with a specific model. ⚠️ Input #1 (our pricing) and a Salesforce quote from the prospect are both required.

2. **Sales rep adoption — mobile and speed.** If reps don't use the CRM, data quality collapses and the ROI case evaporates regardless of which platform wins the paper evaluation. ⚠️ Input #3 (our App Store rating vs. Salesforce Mobile's current rating) is required. Do not quote a rating without verifying it today — ratings change.

3. **Migration in and out.** Getting data into Salesforce requires understanding a proprietary object model. Getting data out is harder. ⚠️ Inputs #5 and #6 (our API policy and data export SLA) are required before raising this with the VP Eng.

4. **Time to value.** Salesforce enterprise implementations are long. ⚠️ Input #2 (our timeline) and Input #7 (a reference customer at comparable size) are both required before making this claim.

---

## Where We Lose (be honest)

1. **Ecosystem breadth.** Salesforce's marketplace is a genuine moat. If the VP Eng's team has deep dependencies on Salesforce-ecosystem tools, switching costs are real. *Mitigation: map which AppExchange apps they actually use. If the list is short, the ecosystem argument is theoretical for this account.*

2. **Brand safety and board optics.** For a 500-seat, multi-year decision, an established brand provides the CFO cover. This is a real objection — don't dismiss it. *Mitigation: a named enterprise reference customer in the same industry is the only credible counter.*

3. **Admin talent pool.** Salesforce has a large certified professional ecosystem, which matters if the customer wants to hire externally. *Mitigation: highlight our simpler admin model. If we require fewer dedicated admins, the talent pool constraint matters less.*

4. **AI maturity.** Einstein has a multi-year head start and deep product integration. ⚠️ Do an honest feature-by-feature comparison before AI becomes a demo differentiator.

---

## Objection Handling

### Economic Buyer (CFO / VP Finance)

| Objection | Response | Proof required |
|---|---|---|
| "Salesforce is expensive but it's a known quantity — I know what I'm budgeting." | "You know the licence cost. Implementation and admin headcount often multiply that significantly in enterprise deployments. We'd like 30 minutes with your finance team to build a side-by-side model — if Salesforce comes out ahead all-in, we'll say so." | ⚠️ Inputs #1 + completed TCO model. Do not have this conversation without a populated model. |
| "We already have other Salesforce products (Marketing Cloud, Service Cloud) — consolidating reduces our risk." | "That consolidation logic holds if the products are best-in-class. Marketing Cloud and Service Cloud are separate products with separate contracts — a CRM switch doesn't break those integrations. Let's map the actual dependencies." | ⚠️ Confirm our integration story with Marketing Cloud and Service Cloud before using this response. |
| "Switching at 500 seats mid-contract is expensive — migration, retraining, lost productivity." | "The migration and retraining cost is real and we don't minimise it. Here's what it looked like for [reference customer] — migration took [X weeks], training [Y days]. Compare that to renewing a 3-year contract with the same adoption problems you have today." | ⚠️ Input #7 (enterprise case study) required. Do not use without a real reference. |

### Technical Buyer (VP Engineering / CTO)

| Objection | Response | Proof required |
|---|---|---|
| "Salesforce has the most comprehensive API surface of any CRM." | "Breadth is not the same as stability. Salesforce API versions deprecate on a fixed cycle — your integrations require ongoing maintenance with every release. ⚠️ [Confirm our API versioning policy] — if we offer long-term stability guarantees, that's a maintenance cost argument." | ⚠️ Input #5 (API versioning policy). |
| "Our team knows Salesforce's object model — switching means retraining our engineers." | "That's a real cost. ⚠️ [Confirm our data model] — if we use standard SQL or a widely-known pattern, the retraining argument weakens. Also worth asking: how much of your eng capacity is currently spent maintaining Salesforce customisations?" | ⚠️ Requires honest comparison of our data model complexity. |
| "Data migration out of Salesforce is painful — we'd be locking into you instead." | "Fair. Here's our data portability policy: ⚠️ [confirm our export formats]. We're happy to put data portability terms in the contract." | ⚠️ Input #6. Be willing to contractualise this. |
| "Salesforce has [specific compliance cert] — do you?" | If we have it: cite the cert with documentation. If we don't: "We don't have [X] today. If that's a hard requirement, we should discuss timeline rather than pretend otherwise." | ⚠️ Input #4. Do not deflect on compliance. |

### End User (Sales Reps / Account Managers)

| Objection | Response | Proof required |
|---|---|---|
| "Our reps are used to Salesforce — they'll resist any change." | "Reps resist bad tools more than they resist change. ⚠️ [Confirm our App Store rating vs. Salesforce Mobile's current rating] — if ours is materially higher, open with the mobile demo rather than a feature comparison." | ⚠️ Input #3. |
| "Training 500 reps is a major project." | "It is. ⚠️ [Confirm our onboarding time] — if we can onboard a rep in under [X hours] vs. Salesforce's typical certification path, make that concrete. Offer a pilot cohort of 20 reps to generate internal momentum before full rollout." | ⚠️ Input #2 (implementation data includes rep onboarding time). |
| "Salesforce has a specific feature we rely on." | Name the feature. If we have it: demo it. If we don't: "That's a fair point — here's how our customers handle that workflow today, and here's what's on our roadmap." Do not claim parity you don't have. | Requires honest feature inventory. |

---

## Landmine Questions

### Ask these (expose Salesforce weaknesses)

| Question | Why it works | Expected answer and follow-up |
|---|---|---|
| "How many CRM admins do you currently have, and how much of their time is maintenance vs. strategic work?" | Exposes admin overhead and complexity cost. | "We have several admins and most of their time is on upkeep." Follow up: "What would your team do with that capacity back?" |
| "What does your mobile CRM usage look like — what percentage of reps log activities from their phone vs. desktop?" | Low mobile usage signals poor mobile UX. | "Honestly, most use it at their desk." Follow up: "What happens when they're at a customer site?" |
| "When you last did a custom data export from Salesforce, how long did it take and what format did you receive?" | Reveals data portability pain. | "It was more painful than expected." |
| "How long did your last Salesforce implementation take from signature to go-live, and what did the SI engagement cost?" | Anchors realistic TCO expectations with their own data. | If they've been through a Salesforce implementation, they will remember the cost and timeline. |
| "What's the adoption rate on the Salesforce features you're currently paying for?" | Exposes the paid-but-unused feature gap — a common Salesforce enterprise problem. | "Adoption is lower than we'd like." Follow up: "What drove the gap?" |

### Avoid these (expose our weaknesses)

| Question | Why it's dangerous | If it comes up anyway |
|---|---|---|
| "Which AppExchange apps are you currently using?" | A long list of deep AppExchange dependencies weakens our ecosystem story. | "Let's map those specifically — some will have direct equivalents, some won't. Can we get our integration team on a call to go through each one?" |
| "Are you subject to [compliance requirement]?" | Opens a conversation we may not be able to close if we lack the cert. | Be direct: "We do / don't have that certification today. Here's our roadmap / here's how other customers in your regulated segment have approached it." |
| "How important is Salesforce admin certification for your future hiring?" | Points to the talent pool argument where Salesforce wins. | "Fair concern — our model requires fewer dedicated admins. Here's how our customers staff for it." |

---

## Key Proof Points

> None of the proof points below can be used without confirmation. Do not use placeholders in front of a 500-seat enterprise prospect.

- **Customer quote:** ⚠️ Required — pull a quote from an enterprise customer (200+ seats). An SMB quote will not carry weight with this CFO. Tag it with seat count and industry.
- **Mobile benchmark:** ⚠️ Pull current iOS App Store and Google Play ratings for both Salesforce Mobile and our app. Screenshot with date. Refresh for every major deal.
- **Implementation benchmark:** ⚠️ "Customers at comparable size were live in [X weeks]" — requires a verified data point from the Professional Services team.
- **Enterprise case study:** ⚠️ Required — prior CRM, seat count, migration timeline, time-to-productivity, measurable outcome. Link to full case study if available.

---

## Competitive Intel Sources

- Salesforce pricing: verify at salesforce.com/crm/pricing before each deal (pricing changes; never quote from memory)
- Salesforce Mobile ratings: iOS App Store and Google Play — verify within 30 days of deal
- G2 and Gartner Peer Insights — "Sales Force Automation" category — useful for rep-level objection patterns and competitor review themes
- Salesforce annual report / 10-K — pricing model changes, acquisitions (MuleSoft, Tableau, Slack) affect competitive dynamics
- Internal win/loss data — ⚠️ priority action: pull last 12 months of Salesforce competitive deals from CRM and add findings to this card. Without this, the card is built on assumptions.

---

> **DRAFT — requires human review before distribution to the sales team.**

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 8.5/17.0 (50%) |
| Evaluated | 2026-05-01 |
| Target duration | 347050 ms |
| Target cost | $0.6908 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Objection handling is segmented by buyer persona (CFO, VP Eng, sales reps) not generic | PASS | The artifact has three clearly labeled subsections under 'Objection Handling': 'Economic Buyer (CFO / VP Finance)', 'Technical Buyer (VP Engineering / CTO)', and 'End User (Sales Reps / Account Managers)', each with distinct objection/response pairs. |
| c2 | Win/lose analysis is based on specific evidence (deal post-mortems, win rates, feature gaps) not generic claims | FAIL | The 'Where We Win / Where We Lose' sections are explicitly labeled 'structural — verify with proof points.' Input #8 (12-month internal win/loss data) is listed as 'Missing.' The card states: 'treat every claim in this card as structural guidance only — not as verifiable proof points.' No deal post-mortems or win-rate statistics are referenced. |
| c3 | TCO comparison includes specific line items (licence, implementation, training, ongoing admin) not just 'we're cheaper' | PASS | The TCO table contains: Licence, Implementation/migration, Admin headcount, Training, Integration maintenance, and 3-year total — all as separate rows for both Salesforce and our product. The structure satisfies the line-item requirement even though values are placeholders. |
| c4 | Technical differentiators are stated with specificity (API rate limits, migration tooling, specific integrations) | FAIL | All technical differentiators on our side are '⚠️ [confirm our API surface and versioning policy]', '⚠️ [confirm our migration tooling]', '⚠️ [confirm our data model]'. No API rate limits, no named migration tooling, no specific named integrations (Slack, MS Teams, ERPs) are present. |
| c5 | The card is concise enough for a sales rep to scan in 30 seconds | PARTIAL | The card includes a TL;DR section and a Quick Comparison table near the top which support fast scanning. However, the full document spans many pages with extensive subsections (TCO table, where-we-win/lose, three objection tables, landmine questions, proof points, intel sources), making a 30-second full scan impossible. |
| c6 | Proof points (case studies, benchmarks) are current and specific to the enterprise segment | FAIL | The 'Key Proof Points' section lists all four points as '⚠️ Required' with no actual data: enterprise customer quote is '⚠️ Required — pull a quote from an enterprise customer (200+ seats)'; mobile benchmark is '⚠️ Pull current iOS App Store and Google Play ratings'; implementation benchmark is '⚠️ requires a verified data point from the Professional Services team'. No actual proof points exist. |
| c7 | Output is labelled DRAFT and flagged for human review | PASS | The artifact opens and closes with '> **DRAFT — requires human review before distribution to the sales team.**' and the confidence level is stated as 'Low'. A 'Before you use this card — inputs required' section further reinforces the human-review requirement. |
| c8 | The card covers one competitor (Salesforce) only, not a multi-competitor overview | PASS | The entire document is titled 'Battle Card: [Our CRM] vs. Salesforce' and every section, table, and proof point references only Salesforce. No other CRMs (HubSpot, Microsoft Dynamics) are mentioned as competitors. |
| c9 | Output's objection / response pairs are SEGMENTED into three sections by buyer persona — CFO (TCO, ROI, pricing transparency), VP Engineering (API extensibility, data migration, integration ecosystem), Sales rep / end user (mobile UX, performance, adoption friction) — NOT a single mixed list | PASS | Three distinct objection tables exist: CFO section covers 'known quantity budgeting', 'consolidation', and 'switching cost' (TCO/ROI framing); VP Eng section covers API comprehensiveness, object model retraining, data portability, and compliance certs; End User section covers rep resistance, training burden, and specific feature gaps. |
| c10 | Output's TCO comparison shows specific line items per option — Salesforce licence cost (per-user-per-month at the Enterprise tier), implementation cost (typical SI engagement $X-$Y for 500 seats), training cost, ongoing admin (Salesforce admin FTE typical at this scale), 3-year total TCO; the requester's product line items in the same shape | PARTIAL | The TCO table has the correct five line-item rows in matching shape for both columns. Implementation shows 'often 1–2× first-year licence cost for SI engagement' as a structural estimate. However, no actual dollar figures are given for any line item — licence price, SI cost for 500 seats, admin FTE rates — all are '⚠️ [verify/confirm]'. The structure matches but no specific values are present. |
| c11 | Output's technical-buyer differentiators are SPECIFIC — API rate limits (e.g. our 100 calls/sec vs Salesforce's 100K daily limit), migration tooling (e.g. named import/export tool, data-mapping wizard), specific pre-built integrations (Slack, MS Teams, named ERPs) | FAIL | All technical differentiators are placeholders: '⚠️ [confirm our API surface and versioning policy]', '⚠️ [confirm our migration tooling]', '⚠️ [confirm our native integration count]'. No API rate limits are mentioned, no migration tool is named, no specific integrations (Slack, MS Teams, ERPs) are listed as ours. |
| c12 | Output's end-user differentiators are concrete — mobile app load time (e.g. '2s vs Salesforce mobile's 6s p95'), offline capability, gestures / UX patterns sales reps care about — with proof points from real benchmarks if available | FAIL | Mobile differentiators are limited to '⚠️ [confirm App Store rating — screenshot with date]' and '⚠️ [confirm our App Store rating vs. Salesforce Mobile's current rating]'. No load times, no offline capability mention, no UX patterns with data. The card notes 'Salesforce Mobile has persistent rep adoption problems' but with no concrete benchmark. |
| c13 | Output's win/loss analysis is grounded in evidence — references specific deal post-mortems, win-rate statistics, or feature-gap data — NOT generic 'we win on UX, lose on ecosystem' | FAIL | The card explicitly states 'treat every claim in this card as structural guidance only — not as verifiable proof points.' Input #8 '12-month internal win/loss data for Salesforce competitive deals' is listed as 'Missing.' Win/lose section says 'structural — verify with proof points' and makes exactly the generic claims the criterion warns against: 'Salesforce's marketplace is a genuine moat', 'we lose on ecosystem breadth'. |
| c14 | Output is concise enough that a sales rep can scan in 30 seconds — single-page, sectioned by persona, key talking points pulled to the front in bold or callout format | PARTIAL | The card has a TL;DR callout block with bolded key messages and a Quick Comparison table near the top, and is organized into persona sections. However, it is clearly multi-page with extensive tables and subsections (TCO table, 4 win sections, 4 lose sections, 3 persona objection tables, landmine questions, proof points, intel sources) — not a single-page scan in 30 seconds. |
| c15 | Output includes proof points specific to the enterprise segment — case studies of 500+ seat customers who switched FROM Salesforce or chose the requester's product over Salesforce, with named (or anonymised but specific) revenue / time-savings outcomes | FAIL | The 'Key Proof Points' section explicitly labels enterprise case study as '⚠️ Required — prior CRM, seat count, migration timeline, time-to-productivity, measurable outcome.' It asks for 'enterprise customer (200+ seats)' quote but marks it '⚠️ Required'. Input #7 'One enterprise migration case study' is listed as 'Missing'. No actual case study data exists in the card. |
| c16 | Output covers ONLY Salesforce — does not pivot into HubSpot, Microsoft Dynamics, or other CRMs; the prompt is explicit that this is one-competitor scope | PASS | The entire artifact is scoped to Salesforce. The title is '[Our CRM] vs. Salesforce', and the competitive intel sources section references only Salesforce-specific resources (salesforce.com/crm/pricing, Salesforce annual report/10-K, Salesforce Mobile ratings). No other CRM competitors are introduced. |
| c17 | Output is labelled DRAFT — explicitly flagged for sales-enablement / marketing leadership review before deployment to the rep team | PASS | File opens: '> **DRAFT — requires human review before distribution to the sales team.**' File closes with the same label. The chat response reiterates: 'Priority actions to complete the card' before any rep use. 'Before you use this card — inputs required' section lists 9 gating inputs. |
| c18 | Output addresses the multi-stakeholder DEAL DYNAMICS — what to do when the CFO, VP Eng, and rep have conflicting priorities (e.g. CFO wants cheapest, rep wants their preferred UX, VP Eng prioritises integration depth) — sequencing the message and proof points | FAIL | No section in the card addresses cross-persona conflicts or priority sequencing. Each persona is treated independently. There is no guidance on what to do when the CFO's TCO objection conflicts with the VP Eng's integration concern, or how to sequence stakeholder conversations. The TL;DR mentions different priorities but does not address how to navigate conflicts. |

### Notes

The card excels at structural scaffolding: persona segmentation, TCO line-item shape, DRAFT labeling, and single-competitor scope are all well-executed. The fundamental failure is that the card is almost entirely placeholder content — 9 of 9 'inputs required' are missing, and virtually every quantitative claim is marked ⚠️. Criteria that test structural qualities (c1, c7, c8, c9, c16, c17) pass; criteria that test specificity of content (c2, c4, c11, c12, c13, c15) all fail because the card honestly acknowledges it has no product data, win-rate statistics, API benchmarks, or case studies. The honest transparency about missing data is a quality of the card as a process artifact, but it means the deliverable cannot satisfy content-specificity criteria. The deal dynamics criterion (c18) is a structural gap — the card treats personas in isolation and never addresses how to sequence or resolve conflicting stakeholder priorities.
