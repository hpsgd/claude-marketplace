# Output: content-analysis skill

**Verdict:** PASS
**Score:** 16.5/17 criteria met (97%)
**Evaluated:** 2026-04-29

## Results

### Criteria (structural — skill definition)

- [x] PASS: Skill extracts and categorises named entities — Step 1 defines a full entity extraction table covering people with role annotation (source/subject/authority), organisations, locations, dates, products/technologies, and financial figures.
- [x] PASS: Key claims section distinguishes primary, supporting, and implicit claims with attribution type — Step 2 defines exactly these three categories and requires attribution type for each (named source, anonymous source, author's assertion, established fact).
- [x] PASS: Sentiment assessed at three levels — Step 3 defines overall tone, targets of sentiment, and language signals as three named sub-assessments.
- [x] PASS: Framing analysis is present and states observations interpretively — Step 4 explicitly instructs "State your framing observations as interpretive judgements, not facts: 'The piece frames X as...' not 'The piece proves X is...'"
- [x] PASS: Narrative identification names dominant narrative structure and explains audience response — Step 5 enumerates six named narrative structures and requires explaining what audience response each activates.
- [x] PASS: Source structure table produced with four source types — Step 6 and output template define a four-row table (named primary, named secondary, anonymous, unattributed) with count and purpose columns.
- [~] PARTIAL: Omissions analysis attempted with honest caveat — Step 4 includes "Omissions" as a required field and the Rules state "Omission analysis requires topic knowledge. If you don't know enough to identify what's missing, say so." The caveat instruction is explicit. Scored 0.5: it is a stated rule rather than a structural guarantee in the output template (the template field reads "or 'insufficient topic knowledge to assess'" which is close to structural).
- [x] PASS: Output follows structured format and does not collapse into a plain summary — the output format template is a complete named-section markdown block (Entities / Claims / Sentiment / Framing / Narrative / Source Structure / Summary assessment). The Rules block reinforces this.

### Output expectations (behavioural)

- [x] PASS: Output fetches and reads the article at the specified URL — skill begins "If a URL is provided, fetch the content first" and lists `WebFetch` as an allowed tool. The definition guarantees fetching before analysis.
- [x] PASS: Entities section categorises people by role — the skill's Step 1 and output template both require name + role + source/subject/authority classification. Named organisations (Group of Eight, Universities Australia equivalents) and key figures (financial amounts, dates, statistics) are covered by the entity table.
- [x] PASS: Key claims section names primary claim (research funding deficit), supporting claims (specific funding gaps), and implicit claims (universities as public good) — Step 2 defines all three categories with attribution type, directly matching the expected content structure.
- [x] PASS: Sentiment assessed at three levels — overall tone, targets of sentiment (positive on universities, critical of government underfunding), and specific language signals — all three sub-fields are required by Step 3 and the output template.
- [x] PASS: Framing stated interpretively — the skill explicitly instructs "The piece frames X as..." construction and prohibits stating framing as established fact. The template field for Dominant framing device reinforces the interpretive stance.
- [x] PASS: Dominant narrative identified and audience response stated — Step 5 requires naming the narrative structure and explaining what audience response it activates. Crisis/urgency and advocacy structures are both in the named taxonomy.
- [x] PASS: Source structure table counts all four source types — the skill's Step 6 and output template define exactly the four-row table with count and purpose columns that the expected output calls for.
- [x] PASS: Omissions analysis attempted with honest caveat — Step 4 includes omissions as a required framing sub-field; Rules require a caveat when topic knowledge is insufficient. The output template even provides the fallback text.
- [x] PASS: Output is structured with named sections — the output format template defines Entities / Claims / Sentiment / Framing / Narrative / Source Structure / Summary assessment. Plain summary is structurally prohibited.
- [~] PARTIAL: Output addresses The Conversation as publication context — the skill has no explicit instruction to contextualise the publication type (academic-authored, advocacy-friendly, editor-reviewed but not journal-reviewed). The source structure section could surface this, and the Rules note about confidence from anonymous sources is adjacent, but the publication-context assessment is not required by the definition. Scored 0.5.

## Notes

One of the more complete skill definitions in the analyst plugin. The three-level sentiment model and named narrative taxonomy are specific enough to produce consistent output rather than ad hoc impressions.

Two minor gaps worth noting. First, the source structure table does not prompt for a confidence implication — the table exists but the skill only surfaces the "lower confidence" inference in the Rules block, not in the output template. Second, the skill has no instruction to characterise the publication venue itself (outlet type, editorial stance, peer-review model), which the output expectations treat as relevant when evaluating source credibility. Both are small; neither materially weakens the definition.
