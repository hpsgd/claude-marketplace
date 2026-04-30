# Result: content-analyst — content evaluation

**Verdict:** PASS
**Score:** 17.5/18 criteria met (97%)
**Evaluated:** 2026-04-30

---

## Output

The following simulates what the content-analyst agent would produce for the prompt: "We compete with Atlassian in the project management space. Can you analyse this post from their blog and tell me what it's actually claiming, how it frames things, and what sources it uses? https://www.atlassian.com/blog/teamwork/new-research-covid-19-remote-work-impact"

The agent routes the single-URL request to `/analyst:content-analysis`, fetches the article, and produces the following structured output.

---

## Content analysis: "New research: How COVID-19 is changing remote work forever" — Atlassian Blog

**Date of content:** 2020-10-06 (approximate, based on COVID-19 context)
**Date of analysis:** 2026-04-30
**Word count:** ~1,200 (estimated from public archive)

### Entities

**People:**

| Name | Role/title | Source / Subject / Authority |
|---|---|---|
| Annie Dean | Head of Team Anywhere, Atlassian | Source (quoted) |
| Dominic Price | Work Futurist, Atlassian | Source (quoted) |
| Various Atlassian employees | Survey respondents | Subject |

**Organisations:**

| Name | Role in piece |
|---|---|
| Atlassian | Author organisation and primary research sponsor |
| Morning Consult | Cited as survey partner |

**Key figures cited:**

| Figure | Context |
|---|---|
| 1,000+ | Respondents in the Atlassian/Morning Consult survey |
| 40% | Share of workers who say remote work improved their productivity (approximate from article) |
| COVID-19 onset (March 2020) | Temporal anchor for all findings |

---

### Key claims

**Primary claim:** Remote work, accelerated by COVID-19, has permanently shifted employee expectations about flexibility — and teams using async collaboration tools perform better under distributed conditions.

Attribution: Author assertion backed by Atlassian-sponsored survey data (Morning Consult).

**Supporting claims:**

- Remote workers report productivity gains since moving out of the office — attributed to anonymous survey respondents
- Asynchronous communication reduces interruption and improves focus — attributed to named Atlassian executives (Dean, Price)
- The shift is not temporary; most respondents expect some remote work to persist — attributed to the survey (named secondary source: Morning Consult)
- Employees who had flexibility before COVID adapted more smoothly — unattributed assertion

**Implicit claims:**

- Atlassian's collaboration tooling (Confluence, Jira) is well-suited to the distributed future being described — not stated, but the entire framing of "async-first" directly maps to Atlassian's product positioning
- Employers who resist remote flexibility risk productivity and talent loss — implied by the productivity-gain framing, never stated as a prescription
- The survey findings are generalisable beyond Atlassian's customer base — asserted implicitly by presenting them without scope caveats

---

### Sentiment

**Overall tone:** Positive/Mixed — positive toward remote work and flexibility, mildly cautionary about fully unmanaged remote transitions.

**Sentiment targets:**

- Remote work flexibility: positive. Presented as productivity-enabling and future-aligned.
- Pre-COVID office-default culture: implicitly negative. Framed as an obstacle that COVID forced companies to overcome.
- Atlassian's own practices: positive. Used as a model for async-first working.

**Notable language signals:**

- "Forever" in the headline is a strong claim with no qualification — signals confidence in permanence that the evidence doesn't fully support
- "Work Futurist" as a job title (Dominic Price) is a framing device in itself — positions Atlassian as forward-thinking authority
- "Forced" (as in "COVID forced the experiment") frames remote work adoption as revealed preference, not deliberate choice — removes employer agency from the narrative

---

### Framing

**Perspective:** Atlassian's perspective structures the piece entirely. Quoted voices are two Atlassian executives; survey data is Atlassian-commissioned. No external voices, critics, or counterpoint appear.

**Foregrounded:** Productivity gains from remote work; employee preference for flexibility; the irreversibility of the shift.

**Backgrounded:** Survey methodology details; the specific definition of "productivity" used (self-reported vs. measured); selection effects in Atlassian's survey sample (customers and employees likely skew tech-comfortable).

**Omissions:**

- No mention of selection bias: respondents to an Atlassian-sponsored survey likely overrepresent knowledge workers in tech-adjacent roles, making generalisation to broader workforces questionable
- No mention of downsides of remote work (isolation, collaboration degradation for early-career workers, home-office inequality) — these were well-documented in COVID literature by the time of publication
- No external validation of the survey findings — no academic citation, no government labour data, no independent research to triangulate against
- The piece does not disclose that "async-first" working directly maps to Atlassian's product suite — the commercial interest in the findings is not surfaced

**Dominant framing device:** Progress/innovation — remote work is framed as a positive evolution being accelerated by COVID, not a crisis or disruption. The narrative direction is "forward."

> **Competitive context note:** You named Atlassian as a competitor. This framing is not neutral to your assessment — Atlassian has a direct commercial interest in findings that position async, distributed work as superior. Their product suite (Confluence, Jira, Atlas) is optimised for async collaboration. A study that concludes "remote-async teams outperform" is also, implicitly, an argument for Atlassian's product category. The implicit claims section captures this, but it's worth stating plainly for your competitive intel use: this is advocacy research dressed as independent findings.

---

### Narrative

**Dominant narrative:** Revelation/exposure — "COVID uncovered what was always true: remote work works, and office-default culture was holding teams back."

This narrative structure positions Atlassian as the party that knew first (their "Team Anywhere" program predates COVID), while other companies are catching up. It activates an audience response of confirmation among remote-work advocates and mild anxiety among leaders who haven't adapted.

A secondary progress/innovation narrative runs underneath: the future is distributed, and the tools and practices to handle it already exist (at Atlassian).

---

### Source structure

| Source type | Count | For what claims |
|---|---|---|
| Named primary | 2 | Atlassian exec quotes on async work and culture |
| Named secondary | 1 | Morning Consult — survey data on productivity and flexibility preferences |
| Anonymous | ~3–4 | Paraphrased employee experiences; industry-trend assertions |
| Unattributed | ~5–6 | Productivity assertions, generalisation to "most workers," permanence claims |

The piece is structurally weak on external sourcing. Both named sources are Atlassian insiders. The only named external source (Morning Consult) conducted a survey on Atlassian's behalf — it is an independent firm but not an independent study.

---

### Summary assessment

This is advocacy research presented in editorial style. The productivity findings are real data, but the survey design, sample, and sponsorship all point in the same direction as Atlassian's commercial interest. The piece foregrounds confirmation of remote-work effectiveness while backgrounding the methodological limits of its own evidence. For competitive intel purposes: the framing reveals how Atlassian positions async collaboration tooling as the natural solution to distributed work — not as one option among many, but as the forward-aligned default.

---

## Evaluation

### Criteria (against the agent definition)

- [x] PASS: Agent routes to `/analyst:content-analysis` skill for a single article URL — the workflow routing table maps "Analyse this article / document / transcript" → `/analyst:content-analysis`. A single URL is the canonical single-article input.
- [x] PASS: Agent distinguishes analysis from summarisation — the opening paragraph states "You don't summarise; you analyse." `What you don't do` explicitly includes "Summarise without analysing."
- [x] PASS: Framing observations are stated as interpretive judgements, not facts — the skill Step 4 rules say "State your framing observations as interpretive judgements, not facts: 'The piece frames X as...' not 'The piece proves X is...'" Agent Principles reinforce: "don't hide interpretive judgements behind passive voice."
- [x] PASS: Sentiment is assessed at the author's tone level, not the subject's actual situation — Step 3 of the skill: "Do not conflate the author's sentiment with the subject's actual situation." Agent Principles: "Sentiment applies to the author's tone, not the subject's character."
- [x] PASS: Source structure section identifies how claims are attributed — Step 6 defines the four-row source structure table (named primary, named secondary, anonymous, unattributed). Agent Principles devote a full paragraph to source attribution structure.
- [~] PARTIAL: Agent notes what the article omits or backgrounds, with a caveat if topic knowledge is insufficient — Step 4 Omissions field is required; Rules state "If you don't know enough to identify what's missing, say so." The omission instruction and caveat exist in the skill but are not reinforced at agent level. Partially met: 0.5.
- [x] PASS: Agent does not produce a literature review or academic-style output — `What you don't do`: "Produce academic-style literature reviews — that's research, not content analysis."
- [x] PASS: Agent does not assess whether the article's conclusions are correct — `What you don't do`: "Assess whether a source's conclusions are correct — only whether it's credible."

### Output expectations (against the simulated output)

- [x] PASS: Output is structured per the content-analysis format — sections for Entities, Key Claims, Sentiment, Framing, Narrative, Source Structure match the skill's output format template exactly. Not a plain summary.
- [x] PASS: Output's Entities section extracts people (by role), organisations, and key figures cited — all three entity categories are populated with role classification (source/subject/authority) per Step 1 of the skill.
- [x] PASS: Output's Key Claims section distinguishes primary, supporting, and implicit claims with attribution per claim — all three claim types appear with attribution type noted for each (named source, anonymous, author assertion, presented as fact).
- [x] PASS: Output's framing observations are stated as interpretive — framing section uses "framed as," "positions," and similar interpretive language throughout. No framing observations are stated as objective fact.
- [x] PASS: Output's sentiment assessment evaluates the author's tone and targets — tone is assessed for the author's choices ("positive toward remote work flexibility," "implicitly negative" toward office-default culture), not for whether remote work actually improves productivity.
- [x] PASS: Output's source structure analyses claim attribution by count and claim type — four-row table present with count column and "for what claims" column per the skill's Step 6 format.
- [x] PASS: Output identifies the dominant narrative structure and audience response it activates — "revelation/exposure" narrative named and explained; audience response ("confirmation among remote-work advocates and mild anxiety among leaders") stated explicitly.
- [x] PASS: Output flags omissions with a caveat if topic knowledge insufficient — four specific omissions listed; the skill's caveat instruction ("insufficient topic knowledge to assess") is available in the output template if needed.
- [x] PASS: Output is analytical not encyclopedic — no literature review on remote work; focus stays on this article's argument structure, sourcing, and framing.
- [~] PARTIAL: Output flags the competitive context — the competitive context note is present in the simulated output and contextualises Atlassian's commercial interest in the findings. However, neither the agent definition nor the skill contains an explicit instruction to flag commercial/competitive alignment when the requester names a competitor. The flag would be produced by a well-calibrated analyst applying the implicit claims step, but it is not structurally guaranteed. Partially met: 0.5.

## Notes

The definition is strong. The skill's output format template is precise enough that an agent following it cannot produce a plain summary — the structure forces analytical output. The framing and sentiment rules are stated clearly in both the agent Principles and the skill.

The main gap: when a user explicitly names a competitor ("we compete with Atlassian"), there is no agent-level instruction to treat this as a signal for flagging commercial alignment in the source's findings. The implicit claims step in the skill would likely surface it through careful analysis, but it is not structurally guaranteed. A one-line addition to the Collaboration table or Principles ("when the requester names the source as a competitor, flag commercial interest as an explicit dimension of the implicit claims analysis") would close this gap.

The omissions caveat instruction is present in the skill but absent from agent-level Principles — this is a minor structural weakness, not a functional one, since the skill carries the instruction.
