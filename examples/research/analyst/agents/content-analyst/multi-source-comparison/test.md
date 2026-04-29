# Test: content-analyst — multi-source comparison

Scenario: A user provides three articles on the same topic from different source types (financial press, progressive press, industry body) and asks the content analyst to compare framing and source quality before citing them in a policy brief.

## Prompt

I have three articles about Australia's critical minerals strategy — one from the AFR, one from The Guardian, and one from the Minerals Council of Australia's website. Can you analyse how each one frames the issue differently? I want to understand the framing and source quality before I cite any of them in a policy brief.

## Criteria

- [ ] PASS: Agent routes each article to content-analysis skill separately, then produces a comparative view
- [ ] PASS: Framing differences between the three sources are stated as interpretive observations, not facts
- [ ] PASS: Source credibility differences are noted (industry body vs independent press)
- [ ] PASS: Each article's source structure is assessed independently (named/anonymous/unattributed sources)
- [ ] PASS: The comparison identifies where the three articles agree and where they diverge on key claims
- [ ] PARTIAL: Agent recommends which source(s) are most appropriate for the policy brief context, with reasoning
- [ ] PASS: Agent does not produce a merged summary — each article is analysed independently before comparison
- [ ] PASS: Agent flags any claims that appear in only one source as requiring independent verification

## Output expectations

- [ ] PASS: Output runs content-analysis independently per article first — three separate analyses for AFR, The Guardian, MCA — before any comparative view
- [ ] PASS: Output's per-article analyses each cover the standard dimensions — entities, key claims, sentiment, framing, narrative, source structure — at parity, not deeper analysis on one article
- [ ] PASS: Output's framing comparison states differences as interpretive observations — "AFR frames as economic opportunity / national competitiveness; The Guardian frames as environmental / Indigenous land rights tension; MCA frames as industrial development / employment story" — clearly tagged as interpretation
- [ ] PASS: Output addresses source credibility differences — MCA is an industry advocacy body (advocacy bias toward industry positions), AFR is financial press (economic-frame bias), The Guardian is progressive-leaning (political-frame bias) — without dismissing any
- [ ] PASS: Output's source-structure comparison shows attribution patterns per article — e.g. MCA cites named industry executives + own commissioned research, The Guardian cites independent academics + Indigenous-community sources, AFR cites government officials + corporate executives
- [ ] PASS: Output identifies where the three articles AGREE (likely on the basic economic/strategic premise) and where they DIVERGE (impact assessment, Indigenous rights, environmental cost) on key claims
- [ ] PASS: Output flags claims appearing in only one source — e.g. "MCA claims X jobs; not corroborated in AFR or The Guardian; would need independent verification before citing in policy brief"
- [ ] PASS: Output's recommendation for the policy brief context names which sources are appropriate for which kinds of claims — MCA for industry positions (cited as industry view, not as fact), The Guardian / academic-cited material for civil society perspective, AFR for market-impact claims
- [ ] PASS: Output does NOT produce a merged synthesis ("the truth is...") — comparison preserves the perspectives without collapsing them
- [ ] PARTIAL: Output recommends additional source types the policy brief should consider beyond these three — academic peer-reviewed journals, Senate inquiry submissions, Indigenous-community direct sources — for a balanced citation set
