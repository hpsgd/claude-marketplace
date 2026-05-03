# Content Evaluation

Scenario: A user wants the content analyst to evaluate a competitor's blog post about remote work for framing, claims, and source structure.

## Prompt

> We compete with Atlassian in the project management space. Can you analyse this post from their blog and tell me what it's actually claiming, how it frames things, and what sources it uses? https://www.atlassian.com/blog/teamwork/new-research-covid-19-remote-work-impact

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Now let me write up the full structured analysis.

---

## Content analysis: "How to Debug Distributed Teamwork, as Suggested by New Research"

**Date of content:** October 7, 2020
**Date of analysis:** 2026-05-01
**Word count:** ~1,200 (estimated from fetch summary)

---

### Entities

**People:**
- Leisa Reichelt — author, Atlassian (Head of Research & Insights) — narrator/authority
- Tiffany Philippou — quoted commentator — secondary source/colour

**Organisations:**
- Atlassian — publisher, implicit beneficiary of all recommendations
- Microsoft (Teams), Slack, Google (Docs), Miro, Mural, Trello, Confluence, Karmabot — tools mentioned in recommendations

**Key figures cited:**
- 43% of workers became more concerned about job security/career
- 33% of remote workers spending more time reporting progress than before
- 46% of women vs. 40% of men reported increased confidence in ability to achieve

---

### Key claims

**Primary claim:** COVID-era distributed work creates four specific problems — innovation risk, invisible work, gendered experience gaps, and home-environment inequality — and teams can "debug" these with the right practices and tools.

**Supporting claims:**
- Remote work reduces spontaneous collaboration and diverse perspective exposure *(attributed to unnamed study participants)*
- Workers feel "out of sight, out of mind" regarding career progression *(anonymous quote)*
- Women gained confidence advantages in video-call formats vs. office environments *(attributed to the proprietary report)*
- Home environment (space, wifi) amplifies pre-existing inequality *(Tiffany Philippou quote)*
- Visibility anxiety is measurable: 43% more job-security concern, 33% more time spent on progress reporting *(proprietary report — no independent verification)*

**Implicit claims:**
- The "new research" is credible and independent (it is not — it is Atlassian-commissioned proprietary research)
- The four problems identified are the salient ones (others — e.g. manager quality, company culture — are absent)
- Atlassian's products (Confluence, Trello) are natural, obvious solutions to the problems surfaced
- Distributed work is the permanent direction of travel; the question is only how to do it well

---

### Sentiment

**Overall tone:** Cautiously optimistic — Mixed, leaning Positive

The piece acknowledges real pain points but consistently pivots toward solvability. Problems are framed as bugs to "debug," not structural failures.

**Sentiment targets:**
- Remote work: sympathetic — challenges are real but fixable
- Atlassian tools: positively foregrounded as remedies
- Office-centric work: implicitly critiqued (gender inequality, lack of flexibility)
- Workers experiencing hardship: empathetic, humanised through quotes

**Notable language signals:**
- **"Debug"** in the title — frames distributed teamwork as a software problem (solvable, technical, Atlassian's domain)
- **"Innovation drought"** — crisis language that creates urgency without citing a measured phenomenon
- **"Insulating effects"** — neutral/clinical language softens the negative finding
- **"Unexpected advantages"** for women — frames an equity finding as a pleasant surprise rather than an indictment of office culture

---

### Framing

**Perspective:** The piece is structured entirely from the employer/team-leader viewpoint. Workers are subjects of study, not co-authors of solutions. The frame is "what should organisations do" not "what do workers want."

**Foregrounded:**
- Atlassian's proprietary research as the authoritative source
- Four discrete, manageable problem buckets
- Specific tool recommendations (Confluence, Trello, Slack, OKRs)
- Gender gains as a reason to preserve remote flexibility

**Backgrounded:**
- Who commissioned and conducted the research, and its methodology
- Whether the findings are generalisable beyond the study cohort
- The possibility that the problems have structural causes tools can't fix
- Competing tools or approaches not in the Atlassian/partner ecosystem

**Omissions:**
- No mention of management quality, psychological safety, or organisational culture as variables — factors that can't be sold
- No acknowledgement that Atlassian has a direct commercial interest in promoting distributed work (they are a distributed-first company selling collaboration software)
- No independent corroboration of the statistics; no link to methodology
- The "full report" is available for download — gated content, likely requiring an email address (a lead generation mechanism)

**Dominant framing device:** **Progress/solution framing** layered over a thin **crisis frame**. The crisis (COVID disrupted work) creates the opening; the progress frame (here's how to fix it) delivers the product message.

---

### Narrative

The piece tells a **revelation + hero** story: "The chaos of COVID has exposed hidden dynamics in how teams work — and now that we can see them, we know how to fix them." Atlassian's research plays the role of the lamp that lights the dark, and its tools play the role of the remedy. The reader — a team lead or manager anxious about distributed work — is positioned as a capable problem-solver who just needs the right framework. This activates a sense of agency and competence, and makes the product recommendations feel earned rather than pushed.

---

### Source structure

| Source type | Count | For what claims |
|---|---|---|
| Named primary | 0 | — |
| Named secondary | 1 | Tiffany Philippou (inequality colour quote — no institutional affiliation given) |
| Anonymous | 2 | Worker experience quotes (innovation, visibility) |
| Proprietary/unverified | 1 | Atlassian-commissioned report — all headline statistics |
| Unattributed | 3+ | General assertions about remote work behaviour |

---

### Summary assessment

The post is a polished example of **research-led content marketing**: Atlassian commissions a study, uses it to define the problem space in terms that favour their product suite, then recommends their own tools as solutions — all under the credibility halo of "new research." The framing device of "debugging" is strategically chosen to position distributed teamwork as a solvable engineering problem in Atlassian's domain, while the gender-equity finding gives the piece a social dimension that makes sharing it feel values-aligned rather than promotional. For competitive purposes, the key takeaway is that Atlassian is actively shaping the narrative around what distributed work problems *are* — which means they're also shaping what solutions look credible.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/17.0 (94%) |
| Evaluated | 2026-05-01 |
| Target duration | 76219 ms |
| Target cost | $0.1326 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent routes to `/analyst:content-analysis` skill for a single article URL | FAIL | The captured output begins 'Now let me write up the full structured analysis.' — no skill invocation is shown. The output matches what the skill would produce, but there is no evidence the agent routed through `/analyst:content-analysis`. |
| c2 | Agent distinguishes analysis from summarisation — produces entity extraction, key claims, sentiment, framing, and narrative sections rather than a plain summary | PASS | Output contains discrete headed sections: Entities, Key Claims (with primary/supporting/implicit subdivisions), Sentiment, Framing (with foregrounded/backgrounded/omissions), Narrative, and Source Structure table — clearly analytical, not a plain summary. |
| c3 | Framing observations are stated as interpretive judgements, not facts ("the piece frames X as..." not "X is...") | PASS | Framing section uses: 'The piece is structured entirely from...', 'frames distributed teamwork as a software problem', 'frames an equity finding as a pleasant surprise rather than an indictment'. All interpretive constructions. |
| c4 | Sentiment is assessed at the author's tone level, not the subject's actual situation | PASS | 'Overall tone: Cautiously optimistic — Mixed, leaning Positive. The piece acknowledges real pain points but consistently pivots toward solvability.' Evaluated as the author's rhetorical stance, not the objective condition of remote workers. |
| c5 | Source structure section identifies how claims are attributed (named sources, anonymous, unattributed) | PASS | Source structure table lists: Named primary (0), Named secondary (1 — Tiffany Philippou), Anonymous (2), Proprietary/unverified (1 — Atlassian-commissioned report), Unattributed (3+), with 'for what claims' column. |
| c6 | Agent notes what the article omits or backgrounds, with a caveat if topic knowledge is insufficient to fully assess omissions | PARTIAL | Omissions are noted in detail under 'Backgrounded' and 'Omissions' subsections (management quality, commercial interest, methodology gaps, gated lead-gen). However, no caveat about topic knowledge limitations is included. Ceiling is PARTIAL. |
| c7 | Agent does not produce a literature review or academic-style output — output is analytical, not encyclopedic | PASS | Output contains no literature review, no citations to external remote-work research, no academic framing. It is tightly scoped to this single article's argument structure. |
| c8 | Agent does not assess whether the article's conclusions are correct, only how it argues | PASS | Summary assessment: 'The post is a polished example of research-led content marketing' — this describes argumentative structure and rhetorical strategy, not the truth value of the remote-work claims. No statement verifying or refuting the 43%/33% statistics. |
| c9 | Output is structured per the content-analysis format — sections for Entities, Key Claims, Sentiment, Framing, Narrative, Source Structure — not a plain summary | PASS | All six required sections present with their canonical headings: Entities, Key Claims, Sentiment, Framing, Narrative, Source Structure. |
| c10 | Output's Entities section extracts people (by role: source / subject / authority), organisations, key statistics and dates referenced in the article — with the article URL fetched and read | PASS | Entities section lists: People with roles (Leisa Reichelt — author/authority; Tiffany Philippou — secondary source/colour), Organisations (Atlassian, Microsoft, Slack, Google, Miro, Mural, Trello, Confluence, Karmabot), Key figures cited (43%, 33%, 46%). Date of content: October 7, 2020 confirms URL was fetched. |
| c11 | Output's Key Claims section distinguishes the primary claim from supporting claims and implicit claims, with attribution per claim — "primary claim: remote work reduced productivity; attribution: anonymous internal Atlassian survey" | PASS | Primary claim stated with attribution ('COVID-era distributed work creates four specific problems...'), Supporting claims each carry attribution in italics ('attributed to unnamed study participants', 'anonymous quote', 'attributed to the proprietary report'), Implicit claims section listed separately. |
| c12 | Output's framing observations are clearly stated as INTERPRETIVE — e.g. "the piece frames remote work as a productivity question rather than a wellbeing or culture question" — not asserted as fact | PASS | 'The piece is structured entirely from the employer/team-leader viewpoint', 'frames distributed teamwork as a software problem (solvable, technical, Atlassian's domain)', 'frames an equity finding as a pleasant surprise rather than an indictment of office culture' — all interpretive constructions. |
| c13 | Output's sentiment assessment evaluates the AUTHOR's tone and target — "tone is mildly positive on hybrid models, mildly negative on fully remote" — not the actual reality of remote work | PASS | 'Overall tone: Cautiously optimistic — Mixed, leaning Positive' with 'Sentiment targets' breaking down author tone toward remote work, Atlassian tools, office-centric work, and workers. 'Notable language signals' analyses word choice as authorial choices. |
| c14 | Output's source structure analyses how claims are attributed — count of named primary sources (e.g. 2 named Atlassian executives), named secondary sources, anonymous citations, unattributed assertions | PASS | Table provides: Named primary: 0, Named secondary: 1 (Tiffany Philippou), Anonymous: 2, Proprietary/unverified: 1 (Atlassian-commissioned report — all headline statistics), Unattributed: 3+ (general assertions about remote work behaviour). |
| c15 | Output identifies the dominant narrative structure — e.g. "transformation narrative" or "research-reveals narrative" — and what audience response it activates | PASS | 'The piece tells a revelation + hero story: The chaos of COVID has exposed hidden dynamics... Atlassian's research plays the role of the lamp that lights the dark... This activates a sense of agency and competence, and makes the product recommendations feel earned rather than pushed.' |
| c16 | Output flags omissions where the article backgrounds or skips relevant context — e.g. "no mention of selection bias in the Atlassian-internal survey" — with a caveat if topic knowledge is insufficient to fully assess | PASS | Omissions section: 'No mention of management quality, psychological safety, or organisational culture as variables — factors that can't be sold', 'No acknowledgement that Atlassian has a direct commercial interest', 'No independent corroboration of the statistics; no link to methodology'. Caveat is conditional; agent's omissions are specific and well-grounded, not requiring a knowledge-limitation caveat. |
| c17 | Output is analytical NOT encyclopedic — does NOT include a literature review on remote work; stays focused on this article's argument structure | PASS | No external literature cited. All analysis is scoped to this article: its language signals, source table, narrative structure, framing devices. Word count and date metadata confirm article-focused analysis. |
| c18 | Output flags the competitive context — Atlassian is a competitor in PM space, so framing of remote work productivity may align with their commercial interest in collaboration tooling — relevant for the requester's competitive intel use case | PARTIAL | Omissions: 'No acknowledgement that Atlassian has a direct commercial interest in promoting distributed work (they are a distributed-first company selling collaboration software)'. Summary: 'Atlassian commissions a study, uses it to define the problem space in terms that favour their product suite'. Commercial interest noted, but not explicitly framed as competitive intelligence context for the requester. Ceiling is PARTIAL. |

### Notes

The output is a high-quality content analysis that satisfies virtually every structural and interpretive criterion. It correctly produces all required sections (Entities, Key Claims, Sentiment, Framing, Narrative, Source Structure), uses interpretive language throughout the framing observations, evaluates author tone rather than subject reality, and identifies the dominant narrative structure and its audience activation mechanism. The only hard failure is c1: no evidence the agent routed through the `/analyst:content-analysis` skill — it appears to have produced the output directly. The two PARTIAL scores (c6, c18) reflect ceiling caps set by the test author: omissions are noted well but lack the knowledge-caveat hedge, and commercial interest is flagged but not explicitly connected to the requester's competitive intel framing.
