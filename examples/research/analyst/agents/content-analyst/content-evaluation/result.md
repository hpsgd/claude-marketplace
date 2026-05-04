# Content Evaluation

Scenario: A user wants the content analyst to evaluate a competitor's blog post about remote work for framing, claims, and source structure.

## Prompt

> We compete with Atlassian in the project management space. Can you analyse this post from their blog and tell me what it's actually claiming, how it frames things, and what sources it uses? https://www.atlassian.com/blog/teamwork/new-research-covid-19-remote-work-impact
> 
> A few specifics for the response:
> 
> - Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
> - Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
> - For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
> - When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
> - Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Now I'll analyse this systematically using the skill's output format.

```markdown
## Content analysis: "How to debug distributed teamwork"

**Date of content:** October 7, 2020
**Date of analysis:** May 4, 2026
**Word count:** ~1200 (estimated)

### Entities

**People:**
- Leisa Reichelt — author (Atlassian)
- No other individuals named

**Organisations:**
- Atlassian — researcher and publisher; implicit solution provider
- Paper Giant — research partner

**Locations:**
- International (no specific countries, cities, or venues identified)

**Key figures cited:**
- 43% reported increased job security concerns
- 33% of remote workers spend more time reporting progress
- 46% of women report increased goal confidence (vs. 40% of men)
- Study period: April–July 2020 (four months)
- Trigger: March 2020 pandemic shift to remote work

**Products/technologies:**
- Confluence, Trello, Miro, Mural — named as solutions

### Key claims

**Primary claim:** Remote work creates five distinct challenges and opportunities; organisations can "debug" distributed teamwork by adopting specific practices and tools.

**Supporting claims (all attributed to Atlassian/Paper Giant study):**
- Innovation drought risk from reduced spontaneous collaboration
- "Visibility paradox": workers feel productive but invisible to peers
- Women benefit disproportionately from WFH (confidence gains, leveled playing fields, appearance freedom)
- Home office resource inequality is surfacing
- Three experience factors shape outcomes: household complexity, role complexity, network quality
- Asynchronous work and outcome-focused metrics (OKRs) mitigate visibility problems
- Digital workspace tools solve visibility and coordination issues

**Implicit claims:**
- Atlassian's four-month study is methodologically sound and generalisable globally (no methodology disclosure)
- The five factors identified are comprehensive — these are THE primary issues in distributed work
- Atlassian's tool suite directly addresses the problems identified
- Remote work is a permanent shift worth systematising
- Women's positive experience is a key finding worth centring (not a footnote)

### Sentiment

**Overall tone:** Optimistic/positive with underlying urgency

The article acknowledges real problems but consistently reframes them as solvable challenges. The headline metaphor ("debug") implies problems are technical and fixable, not systemic.

**Sentiment targets:**
- **Positive toward:** Remote work potential, women's experiences, solution-oriented managers, asynchronous practices, Atlassian's tools
- **Concerned/cautious toward:** Innovation risk, job security anxiety, inequality, visibility problems
- **Neutral:** The research process itself

**Notable language signals:**
- "opportunities" (reframing challenges into solution space)
- "advantageous" (describing WFH for women positively — unusual framing for 2020)
- "leveled playing fields" (equity language)
- "drought" (crisis/loss language for innovation)
- "surfacing" (revelation — making hidden inequality visible as a positive discovery)
- "debug" (technical problem-solving metaphor — solvable, not intractable)

### Framing

**Perspective:** 
Atlassian's perspective as simultaneous researcher and solution provider. The implicit audience is managers/decision-makers who can adopt recommendations. No worker or dissenting perspectives included.

**Foregrounded:**
- The five key findings (positioned as authoritative research)
- Women's experience benefits (unusual prominence for 2020 discourse)
- Practical recommendations tied to Atlassian tools
- The opportunity/solvability angle

**Backgrounded:**
- Research methodology (sample size, geographic distribution, industry breakdown, selection bias — all absent)
- Severity thresholds (43% job anxiety — what about the 57%? Is that good?)
- The pandemic as confounding variable (is WFH the cause or is pandemic stress/uncertainty the cause?)
- Pre-pandemic baseline for comparison
- Alternative solution providers or non-tool-based approaches

**Omissions:**
- No named researchers, statisticians, or third-party methodologists
- No discussion of research limitations or confidence intervals
- No external validation or peer review
- No competing findings or alternative studies cited
- No worker voices quoted (no first-person accounts, interviews, or testimonials)
- No acknowledgment that some findings may favour Atlassian's product positioning
- No discussion of industries where findings might not apply
- No economic impact quantification (cost of innovation loss, productivity gains/losses)

**Dominant framing device:** **Progress/opportunity framing** — problems are reframed as addressable challenges with clear levers. Secondary: **revelation framing** — inequality is being discovered (not caused by WFH), positioning transparency as the solution.

### Narrative

**Dominant narrative: Progress through intelligence and tools**

- Situation: Sudden forced shift to remote work (March 2020)
- Complication: Five distinct challenges emerge
- Discovery: These challenges follow patterns; they're diagnosable
- Resolution: Adopt asynchronous practices + outcome metrics + Atlassian's visibility tools
- Implicit hero: The manager/organisation that recognises and implements these solutions

This activates: "We can engineer our way out of this problem if we're intentional and use the right tools."

**Secondary narrative: Equity revealed**

Women experience unexpected benefits → inequality was hidden, not created by WFH → WFH is actually an equaliser. This reframes WFH from "emergency adaptation" to "opportunity for fairness."

### Source structure

| Source type | Count | For what claims |
|---|---|---|
| Named primary sources | 0 | None — no respondents, researchers, or subjects named on record |
| Named secondary sources | 1 | "Atlassian and Paper Giant four-month study" (cited as single block, no granular sourcing) |
| Anonymous sources | 0 | Not applicable |
| Unattributed | 0 | Statistics are attributed to "the study," so technically attributed, but... |
| **Methodologically opaque** | N/A | No sample size, representativeness, geographic scope, industry breakdown, or methodology disclosed |

**Critical limitation:** The piece's only substantive source is Atlassian's own proprietary research. No independent verification, peer review, or external validation of findings exists in the article. The reader is asked to accept the findings on Atlassian's authority. For a 2020 piece, there are no citations to existing remote work research (pre-pandemic baselines, other studies from March–July 2020, etc.).

### Summary assessment

This is a **research-backed marketing piece** that establishes Atlassian as an authority on distributed work while promoting its tool suite as the solution set. The framing is consistently optimistic and solvable, which serves Atlassian's positioning. The decision to centre women's experiences is unusual for 2020 discourse and reframes WFH as an equity opportunity rather than a crisis — a positioning that benefits buy-in. Critically, **all claims depend entirely on Atlassian's own unreferenced study**; no external validation, methodology transparency, or comparative research is cited. For competitive analysis: Atlassian uses research credibility to establish market authority, but the source structure makes the findings impossible to independently verify or challenge.

```

**Key findings for competitive context:**

This is clean positioning work. Atlassian publishes their own research to establish expertise, frames remote work as solvable (not intractable), and ties every solution back to their products. They foreground women's experiences — unusual for 2020, strategic for equity framing. But the entire evidentiary basis is internal, unverified, and unreviewed. You can't fact-check their claims from this article because no external sources exist. If you wanted to challenge this positioning, you'd need third-party research on the same cohort during the same period, or methodological critiques of their study design (which they haven't disclosed).

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.5/17.0 (97%) |
| Evaluated | 2026-05-04 |
| Target duration | 49215 ms |
| Target cost | $0.0810 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent routes to `/analyst:content-analysis` skill for a single article URL | PARTIAL | The agent says 'Now I'll analyse this systematically using the skill's output format' — acknowledging the skill exists and following its structure — but no explicit Skill tool invocation is visible in the captured output. The format match is strong evidence the skill informed the output, but routing cannot be confirmed. |
| c2 | Agent distinguishes analysis from summarisation — produces entity extraction, key claims, sentiment, framing, and narrative sections rather than a plain summary | PASS | Output contains distinct headed sections: Entities, Key Claims, Sentiment, Framing, Narrative, and Source Structure — none of which is a plain summary. Each section performs a different analytical operation on the article. |
| c3 | Framing observations are stated as interpretive judgements, not facts ("the piece frames X as..." not "X is...") | PASS | Framing section uses interpretive language throughout: 'The headline metaphor ("debug") implies problems are technical and fixable', 'reframes WFH from "emergency adaptation" to "opportunity for fairness"', 'Dominant framing device: Progress/opportunity framing — problems are reframed…'. No objective-fact assertions. |
| c4 | Sentiment is assessed at the author's tone level, not the subject's actual situation | PASS | 'Overall tone: Optimistic/positive with underlying urgency' and 'Sentiment targets: Positive toward: Remote work potential…Concerned/cautious toward: Innovation risk…' — all directed at the author's choices, not at whether remote work is actually good or bad. |
| c5 | Source structure section identifies how claims are attributed (named sources, anonymous, unattributed) | PASS | Source Structure table lists: Named primary sources (0), Named secondary sources (1 — Atlassian/Paper Giant study), Anonymous sources (0), Unattributed (0), and Methodologically opaque — with explicit counts and descriptions of what each covers. |
| c6 | Agent notes what the article omits or backgrounds, with a caveat if topic knowledge is insufficient to fully assess omissions | PARTIAL | Omissions section identifies: missing methodology, no pre-pandemic baseline, pandemic as confounding variable, no external validation, no worker voices, no industry breakdown — all substantive. However, no caveat is offered acknowledging limits of the agent's topic knowledge to fully assess what might be missing. Ceiling is PARTIAL; giving full ceiling credit since omissions coverage is strong. |
| c7 | Agent does not produce a literature review or academic-style output — output is analytical, not encyclopedic | PASS | Output contains no citations to external remote-work research, no literature review section, and no encyclopedic coverage of the topic. Stays entirely focused on this one article's argument structure. |
| c8 | Agent does not assess whether the article's conclusions are correct, only how it argues | PASS | Summary Assessment says 'This is a research-backed marketing piece that establishes Atlassian as an authority…' — a structural observation. No claim is made about whether remote work actually creates the five challenges or whether the WFH equity finding is true. |
| c9 | Output is structured per the content-analysis format — sections for Entities, Key Claims, Sentiment, Framing, Narrative, Source Structure — not a plain summary | PASS | All six required sections present by name: Entities, Key Claims, Sentiment, Framing, Narrative, Source Structure — in that sequence, each with appropriate sub-structure. |
| c10 | Output's Entities section extracts people (by role: source / subject / authority), organisations, key statistics and dates referenced in the article — with the article URL fetched and read | PASS | Entities section identifies Leisa Reichelt as 'author (Atlassian)', organisations (Atlassian as 'researcher and publisher; implicit solution provider', Paper Giant as 'research partner'), key statistics (43%, 33%, 46%, 40%), dates (April–July 2020, March 2020), and products. Statistics match article content, confirming the URL was fetched. |
| c11 | Output's Key Claims section distinguishes the primary claim from supporting claims and implicit claims, with attribution per claim — "primary claim: remote work reduced productivity; attribution: anonymous internal Atlassian survey" | PASS | Key Claims section has three explicit sub-categories: 'Primary claim' (remote work creates five distinct challenges…), 'Supporting claims (all attributed to Atlassian/Paper Giant study)' with a bulleted list, and 'Implicit claims' for unstated assumptions. Attribution is provided at the group level for supporting claims. |
| c12 | Output's framing observations are clearly stated as INTERPRETIVE — e.g. "the piece frames remote work as a productivity question rather than a wellbeing or culture question" — not asserted as fact | PASS | 'Dominant framing device: Progress/opportunity framing — problems are reframed as addressable challenges with clear levers.' 'This reframes WFH from "emergency adaptation" to "opportunity for fairness."' All framing claims use hedged, interpretive constructions. |
| c13 | Output's sentiment assessment evaluates the AUTHOR's tone and target — "tone is mildly positive on hybrid models, mildly negative on fully remote" — not the actual reality of remote work | PASS | Sentiment section explicitly structures findings around 'Overall tone' (author's register: 'Optimistic/positive with underlying urgency') and 'Sentiment targets' (what the author is positive/negative/neutral toward). No claims about whether remote work is actually good or bad. |
| c14 | Output's source structure analyses how claims are attributed — count of named primary sources (e.g. 2 named Atlassian executives), named secondary sources, anonymous citations, unattributed assertions | PASS | Table gives explicit counts: Named primary sources = 0, Named secondary sources = 1 (the Atlassian/Paper Giant study), Anonymous sources = 0, Unattributed = 0, with annotations on what each category covers. The critical limitation paragraph expands on the methodological opacity. |
| c15 | Output identifies the dominant narrative structure — e.g. "transformation narrative" or "research-reveals narrative" — and what audience response it activates | PASS | 'Dominant narrative: Progress through intelligence and tools' with the full arc (Situation → Complication → Discovery → Resolution → Implicit hero). 'This activates: "We can engineer our way out of this problem if we're intentional and use the right tools."' Secondary narrative also named and described. |
| c16 | Output flags omissions where the article backgrounds or skips relevant context — e.g. "no mention of selection bias in the Atlassian-internal survey" — with a caveat if topic knowledge is insufficient to fully assess | PASS | Omissions subsection lists nine specific gaps: no named researchers, no methodology disclosure, no confidence intervals, no external validation, no worker voices, no industry breakdown, no economic quantification, no competing findings, and no acknowledgment of product-positioning alignment. Comprehensive coverage; the 'if insufficient' caveat condition is arguably not triggered by this well-documented topic. |
| c17 | Output is analytical NOT encyclopedic — does NOT include a literature review on remote work; stays focused on this article's argument structure | PASS | No external studies cited, no broad remote-work literature canvassed. Every observation references the Atlassian article specifically. The Source Structure's 'Critical limitation' paragraph notes the absence of external citations as a finding about the article, not as grounds to supply them. |
| c18 | Output flags the competitive context — Atlassian is a competitor in PM space, so framing of remote work productivity may align with their commercial interest in collaboration tooling — relevant for the requester's competitive intel use case | PARTIAL | Summary Assessment calls it 'a research-backed marketing piece that establishes Atlassian as an authority on distributed work while promoting its tool suite.' The 'Key findings for competitive context' closing paragraph explicitly addresses competitive intel: 'Atlassian publishes their own research to establish expertise, frames remote work as solvable, and ties every solution back to their products.' Commercial interest in collaboration tooling is flagged, though not explicitly linked to the PM-space competitive dynamic vs. the requester's company. Ceiling is PARTIAL; full ceiling awarded. |

### Notes

Exceptionally strong output. The agent produced a comprehensive, properly structured content analysis covering all six required sections with appropriate sub-structure. Framing is consistently interpretive rather than factual, sentiment targets the author rather than the subject, and source attribution is quantified. The dominant narrative is named and the audience activation is stated explicitly. The only meaningful gaps are: (1) no explicit Skill tool invocation is visible — the agent references 'the skill's output format' but routing cannot be confirmed from captured output alone; (2) the omissions section, while thorough, omits the 'topic knowledge caveat' that the criterion specifies for c6; (3) for c18, the commercial-interest flag is present but doesn't explicitly connect Atlassian's PM-competitor status to the framing choices. The 'Key findings for competitive context' closing section is a nice addition that goes slightly beyond the template — useful for the requester but not required.
