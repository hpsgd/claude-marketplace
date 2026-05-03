# Content Analysis

Scenario: A researcher wants structured analysis of a Conversation article on Australian university research commercialisation, to understand how it frames the argument before citing it.

## Prompt

> /analyst:content-analysis of the following article:
> 
> ---
> 
> **Australian universities are more than just degree factories. We need to fund their research too.**
> 
> *Published in The Conversation, November 14, 2024. By Professor Catherine Mercer, University of Melbourne, and Dr James Hadley, Group of Eight.*
> 
> Australia spends less on research and development as a proportion of GDP than almost any comparable nation in the OECD. We rank 28th out of 38 member countries. The United States invests 3.5% of GDP in R&D; South Korea invests 4.9%; Australia manages just 1.68%.
> 
> This gap matters more than most people realise — and our universities are caught at the centre of it.
> 
> The public debate about universities tends to orbit around one axis: the cost and value of a degree. Are graduates earning enough to justify the HECS debt? Are international students taking places from domestic ones? These are real questions. But they crowd out a question that may be more consequential for Australia's economic future: what happens to the research capacity that universities generate, and whether we're doing anything useful with it?
> 
> Australia's research commercialisation rate — the share of academic research that makes its way into patents, spin-out companies, or licensed technology — sits at around 14%, compared to 32% in the United Kingdom and 44% in the United States. The Group of Eight universities alone generated more than $4.8 billion in research income last year. But the pipeline from research output to economic value remains narrow, not because the ideas aren't there, but because the funding architecture doesn't support what happens after a discovery is made.
> 
> The problem is structural. Commonwealth funding for universities is directed primarily at teaching and learning, with research grants awarded on a competitive basis through the Australian Research Council and National Health and Medical Research Council. What's largely absent is translational funding — the bridge between a research finding and a commercially viable product or service. This is the "valley of death" that kills many promising technologies before they reach market.
> 
> Universities Australia has lobbied for a dedicated translational fund for years. The previous government committed to a $150 million Trailblazer Universities program; the current government retained it but hasn't expanded it. By comparison, the UK's Innovate UK program deployed £2.5 billion in 2022–23 alone.
> 
> None of this should suggest that the purpose of a university is purely commercial. University research serves public functions that can't be captured in a commercialisation metric — advancing knowledge, training the next generation of researchers, informing public policy, contributing to cultural understanding. These are not inefficiencies to be corrected. They are the point.
> 
> But accepting this doesn't mean accepting the current funding imbalance. It's possible to value basic research and translational research simultaneously. Many of our competitor nations do. The false binary — either universities are for learning, or they're innovation engines — is a framing that has served those who prefer to spend less on both.
> 
> What would a genuine commitment look like? It would mean increasing the Research Block Grant to enable more non-competitive research time. It would mean a translational fund at meaningful scale — not $150 million spread across five years, but a sustained commitment closer to what the UK or Germany provides. And it would mean treating university research as infrastructure, not a discretionary spend that can be trimmed in a tight budget without consequence.
> 
> The consequence arrives slowly, and then all at once. Australia's competitive position in clean energy, advanced manufacturing, medical devices, and agricultural technology depends on a research pipeline that is currently underfunded at almost every stage. We're asking universities to produce ideas that can transform the economy, then declining to fund the part that transforms them.
> 
> *Professor Catherine Mercer is Pro Vice-Chancellor (Research) at the University of Melbourne. Dr James Hadley is Director of Policy at the Group of Eight. Both are members of Universities Australia's Research Policy Committee.*
> 
> ---

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll perform a structured content analysis of this opinion piece from The Conversation.

```markdown
## Content analysis: "Australian universities are more than just degree factories. We need to fund their research too."

**Date of content:** November 14, 2024
**Date of analysis:** May 2, 2026
**Word count:** ~1,200

### Entities

**People:**
- Professor Catherine Mercer — Pro Vice-Chancellor (Research), University of Melbourne — author/authority
- Dr James Hadley — Director of Policy, Group of Eight — author/authority

**Organisations:**
- University of Melbourne, Group of Eight (Go8), Universities Australia, Australian Research Council (ARC), National Health and Medical Research Council (NHMRC), Innovate UK, OECD

**Key locations:** Australia, United States, South Korea, United Kingdom, Germany

**Key figures cited:**
- 1.68% of GDP (Australia's R&D spending) vs 3.5% (US), 4.9% (South Korea)
- 28th out of 38 OECD members (Australia's R&D ranking)
- 14% commercialisation rate (Australia) vs 32% (UK), 44% (US)
- $4.8 billion in annual research income (Group of Eight universities)
- $150 million (Australian Trailblazer Universities program)
- £2.5 billion (UK Innovate UK program, 2022–23)

### Key claims

**Primary claim:** Australia's universities are underfunded for research — particularly translational research (the bridge from discovery to commercial product) — creating a structural economic disadvantage that threatens Australia's competitive position.

**Supporting claims:**
1. Australia consistently underinvests in R&D relative to comparable OECD nations — presented as established fact/statistics
2. Research commercialisation rate gap (14% vs 32-44% in competitor nations) reflects funding architecture, not lack of ideas — author assertion with statistical support
3. Commonwealth funding prioritises teaching; competitive research grants exist, but translational funding is absent — policy analysis
4. Translational funding is the missing "valley of death" bridge — metaphor/author analysis
5. Competitor nations invest substantially more in translational support (UK £2.5B vs Australia $150M) — comparative fact
6. University research serves non-commercial public goods (knowledge, training, policy advice, culture) that are valuable — value assertion
7. A false binary (learning OR innovation) serves those wanting to cut both budgets — author critique
8. Australia's future in clean energy, advanced manufacturing, medical devices, agricultural tech depends on adequate research funding — causal assertion

**Implicit claims:**
- Australia's current research competitiveness is eroding (assumed, not stated)
- Government funding decisions are driven by political preference rather than economic strategy
- The authors' institutional positions give them special knowledge of this problem
- The policy fix (more funding) is obvious; resistance is ideological or budgetary, not substantive

### Sentiment

**Overall tone:** Mixed, leaning critical. Constructive and solution-oriented about research's potential, but pointedly critical of policy choices and framing.

**Sentiment targets:**
- **Negative toward:** current funding architecture, government spending choices, the false binary framing, underfunding relative to peers
- **Positive toward:** university research capacity, research's economic and social value, what increased funding could achieve
- **Neutral/analytical:** international comparisons, statistics

**Notable language signals:**
- "Degree factories" — slightly dismissive opening, frames one way of viewing universities as reductive
- "Valley of death" — vivid, ominous metaphor for research failure
- "The consequence arrives slowly, and then all at once" — dramatic, warns of sudden competitive loss
- "We're asking universities to produce ideas that can transform the economy, then declining to fund the part that transforms them" — accusatory, rhetorical force
- "These are not inefficiencies to be corrected. They are the point." — emphatic defense against utilitarian critique
- "False binary" — characterises the either/or framing as intellectually dishonest, not just debatable
- "Discretionary spend that can be trimmed" — dismissive characterisation of how research is treated in budget cycles

### Framing

**Perspective:** The piece is anchored in the perspective of university research leaders and policy advocates. The reader views the issue through their lens — what they identify as problems, their proposed solutions, their priorities.

**Foregrounded:**
- Australia's R&D spending gap relative to OECD peers (opening)
- The gap between research generation ($4.8B) and economic commercialisation (14%)
- Translational funding as the specific missing policy tool
- International comparisons showing competitor advantage
- The "hidden" debate that the public is missing

**Backgrounded:**
- Reasons *why* other nations have higher commercialisation rates (cultural, market-structural, regulatory factors not explored)
- Arguments for current funding distribution (other national priorities, efficiency concerns)
- Potential downsides of commercialising all university research (mission drift, researcher autonomy, basic science reduction)
- Why funding hasn't increased despite years of lobbying (political will, budget constraints, competing priorities)
- Results of the existing Trailblazer program (whether it's working, why it hasn't expanded)
- Alternative funding sources (corporate R&D investment, venture capital, international partnerships)

**Omissions:**
- No government or Treasury perspective on funding rationale
- No dissenting voices on the commercialisation-first framing
- No exploration of market-based factors (why does Australia have fewer spin-outs? Is it capital availability, market size, regulatory environment?)
- No early-career researcher perspective or student perspective
- No discussion of what other sectors compete for public funding

**Dominant framing device:** **Crisis/urgency + remedy** — positions underfunding as a structural problem requiring specific policy solutions. Also uses **comparative framing** (Australia vs UK/US/Germany) to establish competitive disadvantage.

### Narrative

**Dominant narrative:** A **policy advocacy narrative** where insiders (university leaders) are trying to alert the public to an overlooked problem and propose rational solutions, but face systemic resistance. Variants: "hidden crisis" (the problem isn't visible to the public), "false choice" (we're told it's learning OR innovation, when it's really both), and **competitive jeopardy** (Australia is falling behind).

**Audience activation:**
- For academic/research audiences: validates your concerns as structural, not personal
- For policymakers: "this is about competitive position, not just institutional interests"
- For the general reader: "there's a major economic issue you haven't been hearing about"

### Source structure

| Source type | Count | Claims |
|---|---|---|
| Named primary | 2 | Authorship and implied policy expertise (positions held) |
| Named secondary | 0 | No citations to specific studies or reports |
| Anonymous | 0 | None |
| Unattributed | ~8 | OECD rankings, R&D percentages, commercialisation rates, Group of Eight income figures all presented as fact without "according to" framing |

**Source quality note:** The authors hold positions that give them institutional credibility on this topic, but the piece lacks granular sourcing. Financial figures and statistics are presented as established facts without links to underlying data. Readers cannot easily verify the specific claims. This is typical of opinion pieces in The Conversation but trades transparency for readability.

### Summary assessment

This is a well-structured policy advocacy piece authored by two people with direct institutional authority in Australian research policy. It frames research funding as a solvable structural problem and combines emotional urgency ("competitive position," "valley of death") with rational comparative analysis. However, the framing systematically omits counterarguments — why current funding distribution exists, what downsides might follow from the proposed solutions, and why commercialisation rates vary across nations. The statistics appear credible but lack specific attribution, making independent verification difficult. The piece is designed to move educated readers from awareness to support for specific policy proposals.
```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/17.0 (100%) |
| Evaluated | 2026-05-02 |
| Target duration | 44131 ms |
| Target cost | $0.0685 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill extracts and categorises named entities — people by role (source/subject/authority), organisations, key figures and dates cited | PASS | Entities section lists Professor Catherine Mercer and Dr James Hadley each tagged 'author/authority', lists 7 organisations (University of Melbourne, Group of Eight, Universities Australia, ARC, NHMRC, Innovate UK, OECD), and provides a 'Key figures cited' block with 6 specific statistics (e.g., '1.68% of GDP (Australia's R&D spending) vs 3.5% (US), 4.9% (South Korea)'). |
| c2 | Key claims section distinguishes primary claim, supporting claims, and implicit claims — with attribution type for each | PASS | Primary claim is stated. Eight supporting claims each carry an attribution type in em-dash notation (e.g., 'presented as established fact/statistics', 'author assertion with statistical support', 'comparative fact', 'value assertion', 'causal assertion'). Four implicit claims follow, also labelled (e.g., 'assumed, not stated', 'The authors' institutional positions give them special knowledge'). |
| c3 | Sentiment is assessed at three levels: overall tone, targets of sentiment, and specific language signals | PASS | Overall tone: 'Mixed, leaning critical. Constructive and solution-oriented about research's potential, but pointedly critical of policy choices.' Sentiment targets sub-section labels negative/positive/neutral targets. Notable language signals sub-section quotes and interprets 7 specific phrases (e.g., 'degree factories', 'valley of death', 'the consequence arrives slowly, and then all at once'). |
| c4 | Framing analysis is present and states observations as interpretive judgements ("the piece frames X as...") not established facts | PASS | Framing section uses consistently interpretive language: 'The piece is anchored in the perspective of university research leaders', 'The reader views the issue through their lens', 'Dominant framing device: Crisis/urgency + remedy — positions underfunding as a structural problem'. These are stated as analytical judgements, not as claims about objective reality. |
| c5 | Narrative identification names the dominant narrative structure (e.g., crisis/urgency, blame, revelation) and explains what audience response it activates | PASS | Narrative section names 'A policy advocacy narrative where insiders (university leaders) are trying to alert the public to an overlooked problem', lists three variant sub-narratives ('hidden crisis', 'false choice', 'competitive jeopardy'), and provides an Audience activation block with distinct framings for academic/research audiences, policymakers, and general readers. |
| c6 | Source structure table is produced showing count and purpose of named primary, named secondary, anonymous, and unattributed sources | PASS | A markdown table with columns Source type / Count / Claims is present, listing Named primary (2), Named secondary (0), Anonymous (0), Unattributed (~8). A Source quality note follows explaining what the unattributed sources comprise and why verification is difficult. |
| c7 | Omissions analysis is attempted, with an honest caveat if topic knowledge is insufficient to fully assess what's missing | PARTIAL | Omissions section lists six specific absences (e.g., 'No government or Treasury perspective', 'No dissenting voices on the commercialisation-first framing', 'No exploration of market-based factors', 'No early-career researcher perspective', 'No discussion of what other sectors compete for public funding'). However, no explicit caveat about the analyst's own topic-knowledge limits is included — the ceiling is PARTIAL by design. |
| c8 | Output follows the structured format — does not collapse into a plain summary of the article | PASS | Output is divided into clearly labelled sections (Entities, Key claims, Sentiment, Framing, Narrative, Source structure, Summary assessment), each with internal sub-structure. No section reads as a narrative paraphrase of the article. |
| c9 | Output fetches and reads The Conversation article at the specified URL — analysis is grounded in the actual text, not invented from the headline | PASS | No URL was provided in the prompt — the article was supplied inline. The analysis is demonstrably grounded in the actual text: it quotes specific statistics (1.68%, 14% vs 32%/44%, $4.8B, £2.5B), specific phrases ('valley of death', 'degree factories'), and cites named programs (Trailblazer, Innovate UK). Nothing is invented. |
| c10 | Output's entities section categorises people by role — authors as primary source-of-argument, named academics as authority sources, named institutions (Group of Eight, Universities Australia), key figures (research-funding $$, publication counts) and dates cited | PASS | People listed with role labels 'author/authority'; Group of Eight and Universities Australia appear in the organisations list; Key figures cited block includes $4.8 billion research income, $150 million Trailblazer, £2.5 billion Innovate UK; publication date November 14, 2024 is noted in the header. |
| c11 | Output's key claims section names the primary claim ("research funding deficit constrains commercialisation"), supporting claims (specific funding gaps cited), and implicit claims (universities are a public good worth investing in beyond teaching) | PASS | Primary claim names the structural funding gap as the constraint. Supporting claim #6 states 'University research serves non-commercial public goods (knowledge, training, policy advice, culture) that are valuable — value assertion', directly capturing the public-good claim. Specific funding gaps (14% vs 32-44%, $150M vs £2.5B) appear in supporting claims 2 and 5. |
| c12 | Output's sentiment is assessed at three levels — overall tone (concerned / advocating), targets of sentiment (positive on universities, negative on government underfunding), specific language signals ("more than degree factories", "we need to fund") | PASS | Overall tone: 'Mixed, leaning critical… pointedly critical of policy choices'. Negative targets include 'current funding architecture, government spending choices'; positive targets include 'university research capacity'. Language signals section quotes 'degree factories' and analyses 'The consequence arrives slowly, and then all at once' and 'We're asking universities to produce ideas… then declining to fund the part that transforms them'. |
| c13 | Output's framing is stated INTERPRETIVELY — "the piece frames university research as a public good rather than a private credentialing service" — not as fact about universities | PASS | All framing observations use hedging or attributive language: 'The piece is anchored in…', 'The reader views the issue through their lens', 'positions underfunding as a structural problem requiring specific policy solutions', 'uses competitive jeopardy'. None are stated as objective facts about universities. |
| c14 | Output identifies the dominant narrative — likely "advocacy / corrective" structure (you've misunderstood; here's what really matters) — and what audience response it activates (sympathy for the university sector, criticism of underfunding) | PASS | Names 'A policy advocacy narrative', with the 'hidden crisis' variant explicitly characterising the corrective move ('there's a major economic issue you haven't been hearing about'). Audience activation section specifies sympathy/validation for academic audiences and the intent to shift policymakers and general readers toward criticism of underfunding. |
| c15 | Output's source structure table counts named primary sources (the academic authors), named secondary sources (referenced research), anonymous sources (typically zero in The Conversation), and unattributed assertions | PASS | Table rows: Named primary = 2 (the authors), Named secondary = 0, Anonymous = 0, Unattributed = ~8 (OECD rankings, R&D percentages, commercialisation rates, Group of Eight income). All four expected categories are present. |
| c16 | Output's omissions analysis is attempted — what counter-evidence or counter-arguments are not addressed (e.g. critiques of research-commercialisation as a goal, evidence of inefficiency in current research spend) — with an honest caveat if topic knowledge is insufficient | PASS | Omissions includes 'No dissenting voices on the commercialisation-first framing', 'No exploration of market-based factors (cultural, market-structural, regulatory factors not explored)', 'No government or Treasury perspective on funding rationale', 'No discussion of what other sectors compete for public funding'. Coverage of counter-arguments and structural omissions is thorough. No explicit caveat about knowledge limits, but omissions listed are substantive and accurate. |
| c17 | Output is structured (Entities / Claims / Sentiment / Framing / Narrative / Source Structure / Omissions) — not a plain summary that collapses analysis into descriptive prose | PASS | Output contains distinct top-level sections: Entities, Key claims (with Primary/Supporting/Implicit sub-sections), Sentiment (with Overall tone/Targets/Language signals), Framing (Perspective/Foregrounded/Backgrounded/Omissions/Dominant framing device), Narrative (Dominant narrative/Audience activation), Source structure (table + note), Summary assessment. No collapse into narrative prose. |
| c18 | Output addresses The Conversation as a publication context — academic-authored, advocacy-friendly, peer-reviewed by editors but not journals — relevant to assessing the source structure | PARTIAL | The source quality note states 'This is typical of opinion pieces in The Conversation but trades transparency for readability.' This acknowledges The Conversation's publication norms but does not elaborate on its academic-authored model, editorial (not peer-review) process, or advocacy-friendly positioning. Minimal engagement with publication context — satisfies PARTIAL given ceiling. |

### Notes

The captured output is a high-quality, comprehensive content analysis that satisfies nearly every criterion fully. All seven major analytical sections are present and internally structured. Attribution types are provided per claim, sentiment operates at all three required levels, framing language is consistently interpretive, and the source table is complete. The two capped criteria (c7, c18) are handled partially: omissions analysis is substantive but lacks an explicit epistemic caveat, and The Conversation's publication context receives only a one-line passing mention rather than a characterisation of its academic-authored, editor-reviewed, advocacy-permitting model. No criteria are failed outright. The article was provided inline rather than via URL, so c9's fetching behaviour was not tested, but the second part of the criterion (grounded in actual text) is unambiguously satisfied.
