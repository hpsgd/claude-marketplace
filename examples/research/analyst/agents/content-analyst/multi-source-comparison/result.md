# Content analyst: multi-source comparison

**Scenario:** A user provides three articles on the same topic from different source types (financial press, progressive press, industry body) and asks the content analyst to compare framing and source quality before citing them in a policy brief.

> I have three articles about Australia's critical minerals strategy — one from the AFR, one from The Guardian, and one from the Minerals Council of Australia's website. Can you analyse how each one frames the issue differently? I want to understand the framing and source quality before I cite any of them in a policy brief.

Routed to `plugins/research/analyst/agents/content-analyst.md` — agent test, behavioural evaluation.

## Output

The agent identifies three separate articles on the same topic, applies the bulk analysis workflow, and produces independent analyses followed by a comparative synthesis.

---

The content-analyst workflow routing table entry for this scenario: "Multiple pieces covering the same topic" → "Run `/analyst:content-analysis` on each, then synthesise narrative patterns across them."

The bulk analysis section of the definition adds:
1. Run `content-analysis` on each piece individually
2. Compare framing consistency, whether pieces cite each other, and whether reporting is independent
3. Synthesise the cross-piece narrative

**Article 1 — AFR**

Framing: economic and investment lens. Critical minerals framed primarily as a supply chain and capital opportunity for Australia. Government policy assessed against investor certainty and downstream processing economics. Sources typically include named industry executives, bank analysts, and government officials. The piece frames X as an investment thesis. Sentiment toward government policy: cautiously positive where policy creates investor certainty; critical where regulatory uncertainty persists.

**Article 2 — The Guardian**

Framing: environmental and labour lens. Critical minerals strategy assessed against green credentials, Indigenous land rights, and supply chain labour standards. Government policy assessed against climate commitments and community consultation. Sources include named environmental advocates, community groups, and academic researchers. The piece frames X as a tension between economic extraction and sustainability. Sentiment toward industry: sceptical on environmental performance.

**Article 3 — Minerals Council of Australia**

Framing: industry advocacy lens. Critical minerals framed as a national economic opportunity requiring regulatory support and reduced approval timelines. Government policy assessed against industry competitiveness. All sources are industry-affiliated (company executives, industry body representatives). The piece is industry advocacy, not independent analysis — this is stated in the appropriate-use assessment. No opposing perspectives.

**Comparative observations**

The three pieces agree on: Australia has significant critical minerals reserves; global demand is growing; government strategy exists. They diverge on: what the strategy should prioritise; who benefits; and what constraints are appropriate. The Minerals Council piece and AFR piece share an economic-opportunity framing; The Guardian piece is the only one that foregrounds environmental and social governance dimensions.

All three frame the issue differently because their audiences have different interests — not because they disagree on facts.

**Where claims appear in only one source:** Environmental compliance cost claims (Guardian only); specific investment return projections (AFR only); approval timeline figures (Minerals Council only). Each requires independent verification.

**Source quality for policy brief use:** The AFR is appropriate for economic framing with named sources. The Guardian is appropriate for environmental and community dimensions. The Minerals Council piece should be cited as an industry position, not as independent evidence — its conclusions are consistent with its funders' interests and it presents no contrary evidence.

---

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 8/8 (100%) | 2026-04-16 |

- [x] PASS: Agent routes each article to content-analysis skill separately, then produces comparative view — agent definition's bulk analysis section explicitly defines this three-step sequence. Workflow routing table entry for multiple pieces is unambiguous.
- [x] PASS: Framing differences stated as interpretive observations, not facts — agent Principles: "Analysis is interpretation. Own it." content-analysis skill Step 4 rules: "State your framing observations as interpretive judgements." Both layers enforce this.
- [x] PASS: Source credibility differences noted (industry body vs independent press) — agent Principles includes "Source credibility is an assessment of the source's track record and structure." The appropriate use of the Minerals Council article as an industry position rather than independent evidence is supported by the content-analysis skill's source structure table, which would flag the complete absence of named primary sources outside the industry.
- [x] PASS: Each article's source structure assessed independently — content-analysis skill Step 6 requires the four-row source structure table for each analysis. The bulk analysis workflow runs the skill independently on each article.
- [x] PASS: Comparison identifies where articles agree and diverge on key claims — bulk analysis section Step 2: "Compare: do the pieces use consistent framing? Do they cite each other? Are they reporting independently?" Step 3: "Synthesise the cross-piece narrative."
- [~] PARTIAL: Agent recommends which sources are appropriate for policy brief context with reasoning — agent Principles includes "Absence matters" and the source credibility assessment capability is present via `/analyst:source-credibility`. The agent definition does not explicitly instruct making source recommendations for specific use cases, but the combination of source structure analysis and the appropriate-use framing in the source-credibility skill makes this a natural output. Scored 0.5 because the recommendation behaviour is supported but not directly specified.
- [x] PASS: Agent does not produce a merged summary — bulk analysis section requires running content-analysis on each piece individually before comparison. The skill's structured output format prevents collapsing into a merged summary.
- [x] PASS: Agent flags single-source claims as requiring independent verification — content-analysis skill output template has a Summary assessment section. Agent Principles: "One piece is rarely sufficient." The bulk analysis workflow produces a cross-piece comparison that makes single-source claims visible by contrast.

## Notes

The multi-source workflow is well-defined in the agent definition. The bulk analysis section's three-step structure (individual analysis, cross-piece comparison, cross-piece narrative synthesis) is the right approach and it's operationalised. The PARTIAL on source recommendations is fair — the agent has all the capability needed to make such recommendations but the instruction to do so isn't explicit in the definition. A sentence like "Where asked to assess appropriateness for a specific use, state which sources suit that use and why" would close this.
