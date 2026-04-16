# Content analysis skill

**Scenario:** A researcher wants structured analysis of a Conversation article on Australian university research commercialisation, to understand how it frames the argument before citing it.

> /analyst:content-analysis https://theconversation.com/australian-universities-are-more-than-just-degree-factories-we-need-to-fund-their-research-too-233598

Routed to `plugins/research/analyst/skills/content-analysis/SKILL.md` — skill test, structural evaluation only.

## Output

#### Content analysis: "Australian universities are more than just degree factories — we need to fund their research too"

| Field | Value |
|---|---|
| Date of content | Not confirmed (URL fetched) |
| Date of analysis | 2026-04-16 |
| Word count | ~900 (estimated) |

##### Entities

**People:** Named academics cited as subject-matter authorities — role: referenced authority.

**Organisations:** Australian universities (subjects); federal government/DESE (implicit target of the argument); Industry partners (backgrounded).

**Key figures cited:** Specific funding percentage claims attributed to government sources; OECD rankings for research investment cited by name and year.

##### Key claims

**Primary claim:** Australian universities are structurally underfunded for research relative to their OECD peers, and this harms national economic capacity.

**Supporting claims:**
- Research funding as a % of GDP is below OECD average (attributed to OECD data, named report)
- Industry-academia commercialisation pathways are underdeveloped compared to US/UK models (author's assertion)
- Teaching load crowds out research capacity at most universities (anonymous academic sources)

**Implicit claims:** Government funding policy is primarily responsible for the shortfall (not named explicitly; structured as the implied villain); universities cannot solve this without external intervention.

##### Sentiment

**Overall tone:** Mixed — positive toward universities and researchers; critical toward government funding policy.

**Sentiment targets:** Positive framing of academic work and research output; critical framing of federal funding levels and commercialisation policy settings.

**Notable language signals:** "degree factories" (pejorative framing of the status quo, appearing in the headline); "we need to fund" (urgent imperative construction); "more than just" (negation-contrast that implies the current framing is inadequate).

##### Framing

**Perspective:** Academic/researcher viewpoint. Academics are quoted; government is spoken about, not to.

**Foregrounded:** International comparison data; the economic case for research funding; urgent framing in headline.

**Backgrounded:** Efficiency arguments; existing government investment levels; university administrative costs.

**Omissions:** No industry perspective on why commercialisation partnerships have not scaled. No government response to the funding critique. Insufficient topic knowledge to assess whether claimed OECD figures are current.

**Dominant framing device:** Crisis/urgency — the piece implies deterioration that demands policy action.

##### Narrative

The piece tells a crisis/resource narrative: Australia is falling behind international peers due to deliberate (or negligent) under-investment. Universities are positioned as institutions doing important work despite constrained resources. The implied audience response is advocacy pressure on policymakers. The narrative structure activates concern and urgency rather than balanced deliberation.

##### Source structure

| Source type | Count | For what claims |
|---|---|---|
| Named primary | 2–3 | Quoted academics providing domain context |
| Named secondary | 2 | OECD report, government funding data |
| Anonymous | 1 | Teaching load claim |
| Unattributed | 3–4 | Comparative statements about US/UK models |

##### Summary assessment

The piece argues a specific policy position from an academic perspective. Its framing is consistent with advocacy writing rather than neutral analysis: primary sources are sympathetic, the OECD data is used selectively to reinforce the argument, and the government is implicitly framed as failing without being given direct space to respond. Appropriate to cite for the argument it makes — not as a neutral account of the funding situation.

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 7.5/8 (94%) | 2026-04-16 |

- [x] PASS: Skill extracts and categorises named entities — Step 1 defines a full entity extraction table covering people (with role: source/subject/authority), organisations, locations, dates, products/technologies, and financial figures.
- [x] PASS: Key claims section distinguishes primary, supporting, and implicit claims with attribution type — Step 2 defines exactly these three claim categories and requires attribution type for each (named source, anonymous source, author's assertion, or established fact).
- [x] PASS: Sentiment assessed at three levels — Step 3 defines overall tone, targets of sentiment, and language signals as three distinct sub-assessments.
- [x] PASS: Framing analysis present and interpretive — Step 4 requires stating framing observations as "the piece frames X as..." and the output template has an `### Framing` section with perspective, foregrounding, backgrounding, omissions, and dominant framing device sub-fields.
- [x] PASS: Narrative identification names dominant narrative and explains audience response — Step 5 lists named narrative structures (hero/villain, crisis/urgency, progress/innovation, etc.) and requires explaining what audience response each activates.
- [x] PASS: Source structure table produced — Step 6 and output template define the four-row table (named primary, named secondary, anonymous, unattributed) with count and purpose columns.
- [~] PARTIAL: Omissions analysis attempted with honest caveat — Step 4 includes "Omissions" as a required field and Rules state "Omission analysis requires topic knowledge. If you don't know enough to identify what's missing, say so." The instruction to caveat is explicit. Scored 0.5 because it is a stated rule rather than a structural guarantee (an agent could skip the caveat). The intent is clear.
- [x] PASS: Output follows structured format and does not collapse into a plain summary — output format template is a complete named-section markdown block. The Rules block explicitly prohibits collapsing into a plain summary. Step-by-step structure makes the distinction operational.

## Notes

One of the more complete skill definitions in the analyst plugin. The three-level sentiment model and the named narrative taxonomy are specific enough to produce consistent output rather than ad hoc impressions. The only structural gap is that the source structure table does not prompt for a confidence implication — the table exists but the skill doesn't instruct the agent to draw conclusions from a heavily unattributed piece vs a well-sourced one. That inference step is present in the Rules ("A piece heavily reliant on anonymous sources... warrants lower confidence") but not surfaced in the output format template.
