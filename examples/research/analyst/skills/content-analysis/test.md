# Test: content-analysis skill

Scenario: A researcher wants structured analysis of a Conversation article on Australian university research commercialisation, to understand how it frames the argument before citing it.

## Prompt

/analyst:content-analysis https://theconversation.com/australian-universities-are-more-than-just-degree-factories-we-need-to-fund-their-research-too-233598

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
