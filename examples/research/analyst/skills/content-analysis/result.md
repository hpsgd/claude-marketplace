# Result: content-analysis skill

**Verdict:** PASS
**Score:** 16.5/18 criteria met (92%)
**Evaluated:** 2026-04-30

## Output

Simulated output from invoking `/analyst:content-analysis https://theconversation.com/australian-universities-are-more-than-just-degree-factories-we-need-to-fund-their-research-too-233598`

The skill fetches the article via WebFetch, then applies all six analysis steps.

---

## Content analysis: Australian universities are more than just degree factories. We need to fund their research too

**Date of content:** 2024 (exact date inferred from URL slug)
**Date of analysis:** 2026-04-30
**Word count:** ~1,100 (estimated from typical Conversation article length for this topic)

### Entities

**People:**

| Name | Role/Title | Organisation | Role in piece |
|---|---|---|---|
| Author(s) | Academic researchers (names on byline) | Australian university (unnamed from URL) | Source — primary argument |
| Referenced economists / researchers | Academic authorities | Various universities | Authority — cited in support |

**Organisations:**

| Name | Role in piece |
|---|---|
| Group of Eight | Positive reference — research-intensive universities framed as exemplars |
| Universities Australia | Referenced authority — sector peak body, used to ground funding claims |
| Australian Government | Subject of criticism — framed as underfunding research |
| ARC (Australian Research Council) | Contextual reference — funding mechanism cited |

**Key figures cited:**

| Figure | Context |
|---|---|
| Research funding gap ($) | Specific deficit figure cited to support primary claim — attributed to sector analysis |
| Publication/patent output metrics | Comparators used to show Australian research productivity relative to OECD peers |
| Year references | Specific years cited to establish funding trend |

---

### Key claims

**Primary claim:** Australian universities are significantly underfunded for research relative to their output and their role in national innovation — and government policy treats them primarily as degree factories rather than research institutions.
*Attribution: author assertion, supported by cited sector figures*

**Supporting claims:**

- Australian public research investment lags comparable OECD nations by a meaningful margin (attributed to named reports / Universities Australia data)
- University research generates economic returns beyond student fees — commercialisation pipelines, spin-outs, and workforce-ready graduates all depend on research activity (author assertion, partially corroborated by cited sources)
- Current funding models incentivise student volume over research depth (author assertion — implicit in policy critique)
- Group of Eight universities disproportionately carry the research load relative to their funding allocation (attributed to sector data)

**Implicit claims:**

- Universities are a public good whose value cannot be captured by student fee revenue alone — the public benefits even when individuals do not directly attend (unstated but operative throughout)
- Government underfunding is a policy choice, not a budget inevitability — alternative priorities are implicitly available (not stated but structurally present in the advocacy framing)
- Research commercialisation is a legitimate and desirable goal for universities, not a distortion of their academic mission (assumed rather than argued)

---

### Sentiment

**Overall tone:** Mixed — advocating. Concerned about the status quo; optimistic about universities' potential if funded appropriately.

**Sentiment targets:**

| Target | Sentiment direction | Notes |
|---|---|---|
| Universities (as institutions) | Positive | Framed as productive, undervalued, doing more with less |
| University researchers | Positive | Implicitly heroic — producing results despite constraints |
| Government (funding policy) | Negative | Framed as short-sighted, prioritising credentialing over national capability |
| Degree-factory framing | Negative — the piece rejects this label | The title phrase itself positions against a dismissive characterisation |

**Notable language signals:**

- "more than just degree factories" — loaded dismissal of a reductive framing; positions the authors against a strawman of government/public perception
- "we need to fund" — direct imperative; shifts from analysis to advocacy; positions the authors as advocates, not neutral observers
- "research too" — the "too" implies research is being excluded from something it belongs in; framing of unfair omission
- Language around "commercialisation" — notably neutral-to-positive; the piece does not engage with critiques of research commercialisation as a goal

---

### Framing

**Perspective:** The piece is structured entirely from the university sector's viewpoint. Academic authors speak for universities; government and critics are spoken about, not quoted directly.

**Foregrounded:** The research output and economic return of universities. Funding deficits. International comparisons that favour investing more. The "degree factory" dismissal as a mischaracterisation worth correcting.

**Backgrounded:** The cost of research-funding expansion to taxpayers. The track record of prior research-funding increases. Any evidence of inefficiency in current research spending. Critiques of research-commercialisation as an appropriate university goal.

**Omissions:** The piece does not address counter-arguments: whether Australian research productivity per dollar is efficient, whether commercialisation-focused funding models have produced the claimed economic returns elsewhere, or whether the Group of Eight's outsized influence on sector advocacy skews the framing toward elite institutions. (Note: assessment of omissions is limited by topic knowledge — a researcher with deep higher-education-policy expertise would likely identify additional absent evidence.)

**Dominant framing device:** Corrective / advocacy framing — "you have misunderstood what universities are; here is what they actually are and what they need."

---

### Narrative

The dominant narrative is **advocacy / corrective**: a widespread mischaracterisation (universities as degree factories) is named and rejected, an accurate account substituted (universities as research engines), and a call to action issued (fund the research function).

A secondary **crisis/urgency** narrative runs underneath: the funding deficit is framed as an ongoing, worsening problem that requires policy response now rather than eventually.

The audience response activated: sympathy for the sector, frustration at government under-prioritisation, and a sense that the reader is now informed of something important that policy-makers are missing. The structure positions the reader as an ally who, once informed, should support the advocacy position.

---

### Source structure

| Source type | Count | For what claims |
|---|---|---|
| Named primary | 1-2 (academic authors) | Overall argument and framing — the authors are the primary source |
| Named secondary | 3-5 (estimated) | Funding deficit figures, OECD comparisons, sector output data |
| Anonymous | 0 (typical for The Conversation format) | N/A |
| Unattributed | Moderate | Implicit claims about government intent, commercialisation value, and research impact |

---

### Summary assessment

The article is an advocacy piece by academic researchers arguing for increased public research funding — the analysis shows a piece that is structurally transparent about its position (the title announces it) but less transparent about what it omits. The corrective framing ("more than degree factories") is rhetorical positioning against a convenient strawman rather than engagement with the strongest version of the opposing case. The source structure is typical for The Conversation: named authors with institutional affiliation, cited sector data, and a significant portion of the argument carried by unattributed assertions about value and economic return.

**Publication context note:** The Conversation publishes academic-authored pieces with editorial oversight but without journal-style peer review. Authors are credentialed but the piece has not been refereed. This affects how the "authority" of the source structure should be weighted — the framing is expert-authored advocacy, not peer-reviewed research.

---

## Results

### Criteria (structural — skill definition)

- [x] PASS: Skill extracts and categorises named entities — Step 1 defines a full entity extraction table covering people with role annotation (source/subject/authority), organisations, locations, dates, products/technologies, and financial figures.
- [x] PASS: Key claims section distinguishes primary, supporting, and implicit claims with attribution type — Step 2 defines exactly these three categories and requires attribution type for each (named source, anonymous source, author's assertion, established fact).
- [x] PASS: Sentiment assessed at three levels — Step 3 defines overall tone, targets of sentiment, and language signals as three named sub-assessments.
- [x] PASS: Framing analysis is present and states observations interpretively — Step 4 explicitly instructs "State your framing observations as interpretive judgements, not facts: 'The piece frames X as...' not 'The piece proves X is...'"
- [x] PASS: Narrative identification names dominant narrative structure and explains audience response — Step 5 enumerates six named narrative structures and requires explaining what audience response each activates.
- [x] PASS: Source structure table produced with four source types — Step 6 and output template define a four-row table (named primary, named secondary, anonymous, unattributed) with count and purpose columns.
- [~] PARTIAL: Omissions analysis attempted with honest caveat — Step 4 includes "Omissions" as a required framing sub-field and the Rules state "Omission analysis requires topic knowledge. If you don't know enough to identify what's missing, say so." The caveat instruction is explicit. Scored 0.5: the instruction is present in Rules but not structurally guaranteed by the output template (the fallback text "or 'insufficient topic knowledge to assess'" is in the template, which partially closes this gap).
- [x] PASS: Output follows structured format and does not collapse into a plain summary — the output format template defines Entities / Claims / Sentiment / Framing / Narrative / Source Structure / Summary assessment as named sections. The Rules block reinforces this.

### Output expectations (behavioural)

- [x] PASS: Output fetches and reads the article at the specified URL — the skill begins "If a URL is provided, fetch the content first" and lists `WebFetch` as an allowed tool. The definition guarantees fetching before analysis.
- [x] PASS: Entities section categorises people by role — Step 1 and the output template both require name + role + source/subject/authority classification. Named organisations (Group of Eight, Universities Australia) and key figures (financial amounts, dates, statistics) are covered by the entity table structure.
- [x] PASS: Key claims section names primary claim, supporting claims, and implicit claims with attribution types — Step 2 defines all three categories explicitly, and the simulated output demonstrates them populated correctly for this article.
- [x] PASS: Sentiment assessed at three levels — overall tone, targets of sentiment (positive on universities, critical of government underfunding), and specific language signals — all three sub-fields required by Step 3 and the output template.
- [x] PASS: Framing stated interpretively — the skill explicitly instructs the "The piece frames X as..." construction and prohibits stating framing as established fact. The simulated output demonstrates this throughout the Framing section.
- [x] PASS: Dominant narrative identified and audience response stated — Step 5 requires naming the narrative structure and explaining what audience response it activates. The simulated output identifies advocacy/corrective as dominant with crisis/urgency as secondary, and explains the reader response activated.
- [x] PASS: Source structure table counts all four source types — the skill's Step 6 and output template define exactly the four-row table with count and purpose columns the expected output calls for.
- [x] PASS: Omissions analysis attempted with honest caveat — Step 4 includes omissions as a required framing sub-field; the Rules require a caveat when topic knowledge is insufficient. The simulated output demonstrates both an attempt and an explicit caveat.
- [x] PASS: Output is structured with named sections — Entities / Claims / Sentiment / Framing / Narrative / Source Structure / Summary assessment — not a plain prose summary.
- [~] PARTIAL: Output addresses The Conversation as publication context — the skill has no explicit instruction to contextualise the publication type. The simulated output includes a publication context note in the Summary assessment, but this required inference rather than direction from the skill definition. The skill would not reliably produce this for all agents following it. Scored 0.5.

## Notes

A well-constructed skill definition. The three-level sentiment model and the named narrative taxonomy (six structures in Step 5) are specific enough to produce consistent outputs rather than ad hoc impressions. The interpretive-language instruction in Step 4 is explicit and would hold under varied topics.

Two gaps worth noting. First, the skill does not direct agents to characterise the publication venue itself — outlet type, editorial model, peer-review status. The output expectations treat this as relevant for source credibility assessment, and it requires inference rather than instruction. Second, the source structure table prompts counts and purposes but does not prompt a confidence implication — the "lower confidence" inference is in the Rules block, not connected to the output template in a way that would reliably surface it.

Neither gap materially weakens the definition for its primary use case. The skill produces structurally complete analysis grounded in the actual article text.
