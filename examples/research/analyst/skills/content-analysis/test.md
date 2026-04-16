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
