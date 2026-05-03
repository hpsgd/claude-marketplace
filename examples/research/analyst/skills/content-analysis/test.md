# Test: content-analysis skill

Scenario: A researcher wants structured analysis of a Conversation article on Australian university research commercialisation, to understand how it frames the argument before citing it.

## Prompt

/analyst:content-analysis of the following article:

---

**Australian universities are more than just degree factories. We need to fund their research too.**

*Published in The Conversation, November 14, 2024. By Professor Catherine Mercer, University of Melbourne, and Dr James Hadley, Group of Eight.*

Australia spends less on research and development as a proportion of GDP than almost any comparable nation in the OECD. We rank 28th out of 38 member countries. The United States invests 3.5% of GDP in R&D; South Korea invests 4.9%; Australia manages just 1.68%.

This gap matters more than most people realise — and our universities are caught at the centre of it.

The public debate about universities tends to orbit around one axis: the cost and value of a degree. Are graduates earning enough to justify the HECS debt? Are international students taking places from domestic ones? These are real questions. But they crowd out a question that may be more consequential for Australia's economic future: what happens to the research capacity that universities generate, and whether we're doing anything useful with it?

Australia's research commercialisation rate — the share of academic research that makes its way into patents, spin-out companies, or licensed technology — sits at around 14%, compared to 32% in the United Kingdom and 44% in the United States. The Group of Eight universities alone generated more than $4.8 billion in research income last year. But the pipeline from research output to economic value remains narrow, not because the ideas aren't there, but because the funding architecture doesn't support what happens after a discovery is made.

The problem is structural. Commonwealth funding for universities is directed primarily at teaching and learning, with research grants awarded on a competitive basis through the Australian Research Council and National Health and Medical Research Council. What's largely absent is translational funding — the bridge between a research finding and a commercially viable product or service. This is the "valley of death" that kills many promising technologies before they reach market.

Universities Australia has lobbied for a dedicated translational fund for years. The previous government committed to a $150 million Trailblazer Universities program; the current government retained it but hasn't expanded it. By comparison, the UK's Innovate UK program deployed £2.5 billion in 2022–23 alone.

None of this should suggest that the purpose of a university is purely commercial. University research serves public functions that can't be captured in a commercialisation metric — advancing knowledge, training the next generation of researchers, informing public policy, contributing to cultural understanding. These are not inefficiencies to be corrected. They are the point.

But accepting this doesn't mean accepting the current funding imbalance. It's possible to value basic research and translational research simultaneously. Many of our competitor nations do. The false binary — either universities are for learning, or they're innovation engines — is a framing that has served those who prefer to spend less on both.

What would a genuine commitment look like? It would mean increasing the Research Block Grant to enable more non-competitive research time. It would mean a translational fund at meaningful scale — not $150 million spread across five years, but a sustained commitment closer to what the UK or Germany provides. And it would mean treating university research as infrastructure, not a discretionary spend that can be trimmed in a tight budget without consequence.

The consequence arrives slowly, and then all at once. Australia's competitive position in clean energy, advanced manufacturing, medical devices, and agricultural technology depends on a research pipeline that is currently underfunded at almost every stage. We're asking universities to produce ideas that can transform the economy, then declining to fund the part that transforms them.

*Professor Catherine Mercer is Pro Vice-Chancellor (Research) at the University of Melbourne. Dr James Hadley is Director of Policy at the Group of Eight. Both are members of Universities Australia's Research Policy Committee.*

---

## Criteria

- [ ] PASS: Skill extracts and categorises named entities — people by role (source/subject/authority), organisations, key figures and dates cited
- [ ] PASS: Key claims section distinguishes primary claim, supporting claims, and implicit claims — with attribution type for each
- [ ] PASS: Sentiment is assessed at three levels: overall tone, targets of sentiment, and specific language signals
- [ ] PASS: Framing analysis is present and states observations as interpretive judgements ("the piece frames X as...") not established facts
- [ ] PASS: Narrative identification names the dominant narrative structure (e.g., crisis/urgency, blame, revelation) and explains what audience response it activates
- [ ] PASS: Source structure table is produced showing count and purpose of named primary, named secondary, anonymous, and unattributed sources
- [ ] PARTIAL: Omissions analysis is attempted, with an honest caveat if topic knowledge is insufficient to fully assess what's missing
- [ ] PASS: Output follows the structured format — does not collapse into a plain summary of the article

## Output expectations

- [ ] PASS: Output fetches and reads The Conversation article at the specified URL — analysis is grounded in the actual text, not invented from the headline
- [ ] PASS: Output's entities section categorises people by role — authors as primary source-of-argument, named academics as authority sources, named institutions (Group of Eight, Universities Australia), key figures (research-funding $$, publication counts) and dates cited
- [ ] PASS: Output's key claims section names the primary claim ("research funding deficit constrains commercialisation"), supporting claims (specific funding gaps cited), and implicit claims (universities are a public good worth investing in beyond teaching)
- [ ] PASS: Output's sentiment is assessed at three levels — overall tone (concerned / advocating), targets of sentiment (positive on universities, negative on government underfunding), specific language signals ("more than degree factories", "we need to fund")
- [ ] PASS: Output's framing is stated INTERPRETIVELY — "the piece frames university research as a public good rather than a private credentialing service" — not as fact about universities
- [ ] PASS: Output identifies the dominant narrative — likely "advocacy / corrective" structure (you've misunderstood; here's what really matters) — and what audience response it activates (sympathy for the university sector, criticism of underfunding)
- [ ] PASS: Output's source structure table counts named primary sources (the academic authors), named secondary sources (referenced research), anonymous sources (typically zero in The Conversation), and unattributed assertions
- [ ] PASS: Output's omissions analysis is attempted — what counter-evidence or counter-arguments are not addressed (e.g. critiques of research-commercialisation as a goal, evidence of inefficiency in current research spend) — with an honest caveat if topic knowledge is insufficient
- [ ] PASS: Output is structured (Entities / Claims / Sentiment / Framing / Narrative / Source Structure / Omissions) — not a plain summary that collapses analysis into descriptive prose
- [ ] PARTIAL: Output addresses The Conversation as a publication context — academic-authored, advocacy-friendly, peer-reviewed by editors but not journals — relevant to assessing the source structure
