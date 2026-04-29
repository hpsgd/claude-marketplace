# Output: Write battle card

**Verdict:** PARTIAL
**Score:** 14/17 criteria met (82%)
**Evaluated:** 2026-04-29

## Results

### Criteria (skill definition — 7.5/8)

- [x] PASS: Research step required — Step 1 mandates checking existing analysis, competitor profile, recent changes, and win/loss data before writing. The rule "Every claim on the battle card must have a source" reinforces this as a hard gate, not a suggestion.
- [x] PASS: Win/loss analysis required — Step 2 "Identify win/lose dynamics" is a dedicated required step with a structured table. Step 1 explicitly requires searching "deal retrospectives, CRM notes, or customer feedback that mentions this competitor." The rules state "Include where we lose. A battle card that claims we win everywhere is not credible."
- [x] PASS: At least 4 objection/response pairs — Step 3 states "Build at least 4 objection-response pairs. Prioritise by frequency." The structured format (objection, why they say it, response, proof point) is required per pair.
- [x] PASS: Landmine questions — Step 4 "Create landmine questions" is a dedicated required step covering questions to ask (expose competitor weaknesses) and questions to avoid (expose our own weaknesses), with structured tables.
- [x] PASS: Single page, scannable — description calls it "one-page sales reference" and "scannable in under 30 seconds." Rules state "If a rep can't scan the card and find what they need in 30 seconds, the card is too long. Prefer tables and bullets over paragraphs."
- [x] PASS: All messaging labelled DRAFT — Rules explicitly state "Label every output with 'DRAFT — requires human review' at the top and bottom." Both the rule and the template header enforce this.
- [~] PARTIAL: Buyer type/deal stage segmentation — Step 3 includes explicit buyer persona segmentation (Economic buyer/CFO, Technical buyer/VP Eng, End user) and the template carries through. The segmentation is conditional on enterprise deals, which is honest — but the criteria expects segmented responses or deal-stage differentiation regardless. The skill handles this as optional rather than required, so partial credit.
- [x] PASS: Valid YAML frontmatter — frontmatter contains `name: write-battle-card`, `description`, and `argument-hint` fields, all populated with appropriate values.

### Output expectations (simulated output — 6.5/9)

- [~] PARTIAL: Research notes on Monday.com are sourced — pricing cited from public pages, G2 mentioned. However, no win/loss data, no mention of Monday's CRM expansion, no recent positioning shifts, no product gap specifics. The research reads like it was synthesised from general knowledge rather than sourced intelligence.
- [~] PARTIAL: Win/loss analysis identifies WHY Clearpath loses to Monday late in deals — the output has a quick comparison and TL;DR but does not explain the late-stage dynamic specifically: why Monday appears late, what decision context triggers it, what objections arise at that stage vs earlier. The scenario specifically calls this out and the output doesn't address it directly.
- [x] PASS: At least 4 objection/response pairs — 5 pairs shown, each with objection, response, and proof point.
- [x] PASS: Landmine questions surface Monday weaknesses — 3 questions with explanations of what they reveal. Questions target cross-team reporting, onboarding timelines, and admin dependency — all genuine Monday weaknesses.
- [x] PASS: Fits single page — tables and bullets throughout, no narrative paragraphs. Scannable in under 60 seconds.
- [x] PASS: Competitive truth is honest — explicitly shows where Monday wins (integrations: 200+ vs 40, brand recognition: established vs growing). Not a one-sided card.
- [x] PASS: All messaging labelled DRAFT — appears at top and bottom of the output.
- [x] PASS: Tone is calm and confident — not defensive, not bashing. Responses redirect to Clearpath strengths rather than attacking Monday directly.
- [~] PARTIAL: Responses include proof points — some proof points are vague placeholders ("Customer case study: [link]", "G2 reviews on implementation time"). The pricing comparison is specific and credible. The case study link is not real. A sales-ready card would need real links and real quotes. Partial credit because the structure is right but the substance is placeholder.
- [ ] FAIL: Output addresses different buyer types — no segmentation by IT decision-maker, Operations leader, or End-user team lead. All objections are flat. The skill's own template includes buyer persona tables but the simulated output doesn't use them.

## Notes

The skill definition is strong. The output exposes a gap between the skill's stated requirements and what a model actually produces. The skill mandates buyer persona segmentation for enterprise deals and provides a template for it, but the simulated output flattens everything into a single objection table.

The research step is the other structural weakness in the output. The skill correctly requires sourced intelligence before writing, but the output's sources are public pages checked on a single day. No CRM data, no win/loss retrospectives, no recent positioning intel (Monday's CRM push is a meaningful competitive development that goes unmentioned). The skill cannot force an agent to have access to internal data, but the output should at minimum flag where internal data was unavailable rather than proceeding as if generic sources are sufficient.

The "questions to avoid" section in Step 4 is the most practically useful element most battle card templates omit. It survives into the output and is stronger for it.
