# Output: content-analyst — multi-source comparison

**Verdict:** PASS
**Score:** 17/17.5 criteria met (97%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Agent routes each article to content-analysis skill separately, then produces a comparative view — met. Workflow routing table explicitly states "Multiple pieces covering the same topic → Run `/analyst:content-analysis` on each, then synthesise narrative patterns across them." Bulk analysis section reinforces: run content-analysis on each piece individually, then compare.
- [x] PASS: Framing differences between the three sources are stated as interpretive observations, not facts — met. Non-negotiable section: "Framing analysis requires stating your own interpretive position. Don't present framing observations as objective fact — they're analytical judgements." Principles reinforce: "Analysis is interpretation. Own it — don't hide interpretive judgements behind passive voice."
- [x] PASS: Source credibility differences are noted (industry body vs independent press) — met. "Source credibility is an assessment of the source's track record and structure, not its conclusions." Workflow routing includes `/analyst:source-credibility` for bias questions. Principles include source attribution structure assessment.
- [x] PASS: Each article's source structure is assessed independently (named/anonymous/unattributed sources) — met. Principles explicitly call this out: "For every piece analysed, note how claims are supported: named primary sources, named secondary sources, anonymous sources, and unattributed assertions."
- [x] PASS: The comparison identifies where the three articles agree and where they diverge on key claims — met. Bulk analysis step 2 instructs: "do the pieces use consistent framing? Do they cite each other? Are they reporting independently or amplifying a single source?" Step 3: "Synthesise the cross-piece narrative — what does the pattern of coverage tell you that individual pieces don't?"
- [~] PARTIAL: Agent recommends which source(s) are most appropriate for the policy brief context, with reasoning — partially met. The agent supports interpretive judgements and source credibility assessment. However, no explicit instruction exists to produce citation-suitability recommendations for a specific downstream use case. A well-formed response would likely include this based on the prompt context, but the definition does not guarantee it.
- [x] PASS: Agent does not produce a merged summary — each article is analysed independently before comparison — met. Bulk analysis step 1 explicitly requires individual analysis before any synthesis. Core statement: "You don't summarise; you analyse." What you don't do section prohibits "Summarise without analysing."
- [x] PASS: Agent flags any claims that appear in only one source as requiring independent verification — met. Bulk analysis step 2 addresses independent vs amplified reporting. Principles: "One piece is rarely sufficient. Patterns emerge across multiple sources."

### Output expectations

- [x] PASS: Output runs content-analysis independently per article first — met. Bulk analysis workflow specifies this order explicitly.
- [x] PASS: Output's per-article analyses each cover standard dimensions at parity — met. Bulk analysis step 1 routes each piece through the same content-analysis skill, ensuring consistent dimensions. "Source attribution structure matters. For every piece analysed..." signals parity.
- [x] PASS: Output's framing comparison states differences as interpretive observations — met. Non-negotiable and Principles sections make this a hard requirement.
- [x] PASS: Output addresses source credibility differences without dismissing any — met. "Source credibility is an assessment of the source's track record and structure, not its conclusions" is inherently non-dismissive. Principles: "Framing is about what's foregrounded, not what's wrong. A framing observation isn't an accusation."
- [x] PASS: Output's source-structure comparison shows attribution patterns per article — met. Principles explicitly require per-piece source attribution assessment across named primary, named secondary, anonymous, and unattributed categories.
- [x] PASS: Output identifies where three articles agree and diverge on key claims — met. Bulk analysis steps 2 and 3 address this directly.
- [x] PASS: Output flags claims appearing in only one source as needing independent verification — met. Bulk analysis step 2 checks whether pieces report independently or amplify a single source.
- [~] PARTIAL: Output's recommendation for the policy brief context names which sources are appropriate for which kinds of claims — partially met. The agent supports the capability but has no explicit instruction to produce a source-suitability-by-claim-type breakdown for a specific downstream purpose. Scored 0.5.
- [x] PASS: Output does NOT produce a merged synthesis — met. "You don't summarise; you analyse" and the prohibition on summarising without analysing make this a hard constraint.
- [~] PARTIAL: Output recommends additional source types the policy brief should consider — partially met. The principle "One piece is rarely sufficient" nudges toward broader sourcing, but the definition contains no explicit instruction to proactively recommend additional source categories for a policy brief use case. Scored 0.5.

## Notes

The agent definition is well-suited for this scenario. The bulk analysis workflow, non-negotiable framing discipline, and source attribution principles together cover most behavioural criteria cleanly.

The consistent gap is around downstream use-case tailoring: the definition does not explicitly instruct the agent to shape its output for a specific citation purpose (e.g. "what should I cite in a policy brief for what claims"). The agent will produce strong comparative analysis, but whether it extends to citation-suitability recommendations and additional source suggestions depends on inference rather than explicit instruction. A single sentence in the bulk analysis section covering "where asked to assess appropriateness for a specific use, state which sources suit that use and why" would close this.

The content-analysis skill exists at the expected path.
