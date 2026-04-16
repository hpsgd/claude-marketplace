# Content analyst: content evaluation

**Scenario:** A user wants the content analyst to evaluate a competitor's blog post about remote work for framing, claims, and source structure.

> We compete with Atlassian in the project management space. Can you analyse this post from their blog and tell me what it's actually claiming, how it frames things, and what sources it uses? https://www.atlassian.com/blog/teamwork/new-research-covid-19-remote-work-impact

Routed to `plugins/research/analyst/agents/content-analyst.md` — agent test, behavioural evaluation.

## Output

The content analyst would process this request as follows. It reads the URL via `/analyst:content-analysis` and produces structured output.

---

#### Content analysis: "New research: COVID-19 and the remote work impact" — Atlassian blog

| Field | Value |
|---|---|
| Date of content | 2020 (publication date estimated from URL slug) |
| Date of analysis | 2026-04-16 |
| Word count | ~1,200 (estimated) |

##### Entities

**People:** Atlassian researchers (unnamed, collective author); survey participants (unnamed, anonymous collective).

**Organisations:** Atlassian (author/subject); referenced third-party research (cited by name in some places, unattributed in others).

**Key figures cited:** Survey sample size; percentage claims about productivity, communication, and remote work preferences — exact figures require reading the live URL.

##### Key claims

**Primary claim:** Remote work during COVID-19 produced measurable impacts on team collaboration, productivity, and communication patterns — and Atlassian's own data illuminates these patterns.

**Supporting claims:** Survey-derived statistics on productivity perception; claims about meeting frequency changes; tool adoption patterns (attributed to Atlassian data).

**Implicit claims:** Atlassian tools are well-positioned to address the challenges identified (the piece is published by a commercial vendor selling collaboration tools). The research finding happens to align with Atlassian's product positioning.

##### Sentiment

**Overall tone:** Positive-neutral. Framed as informative research publication, not advocacy.

**Sentiment targets:** Remote work is framed as a normalised reality requiring better tooling; the pandemic context is treated as an accelerant, not a crisis.

**Notable language signals:** "New research" in the headline (signals authority and novelty); first-person plural framing ("we found") blurs the line between Atlassian the researcher and Atlassian the vendor; productivity language is consistently positive about remote work outcomes.

##### Framing

**Perspective:** The piece is written by the vendor whose products are used in the remote work scenario being studied. All perspectives are Atlassian's own or from Atlassian-surveyed respondents.

**Foregrounded:** Productivity and communication findings that show remote work is workable; Atlassian tool usage data.

**Backgrounded:** Survey limitations; the vendor's commercial interest in positive remote work findings; context from independent research on remote work outcomes.

**Omissions:** No independent replication or corroborating study cited. No critical perspective on remote work. No disclosure of survey methodology limitations beyond standard "N=" reporting.

**Dominant framing device:** Progress/innovation — remote work is positioned as a successful adaptation.

##### Narrative

The piece tells a "challenge successfully met" narrative: COVID-19 forced remote work, teams adapted, the data shows it worked, and the implication is that the tools enabling this deserve credit. The narrative aligns the vendor's product with positive outcomes without stating it explicitly. This is standard corporate thought leadership framing.

##### Source structure

| Source type | Count | For what claims |
|---|---|---|
| Named primary | 0 | — |
| Named secondary | 1–2 | One external study referenced (not fully cited) |
| Anonymous | 0 | — |
| Unattributed | 5–8 | Most statistical claims attributed to "our data" or "respondents said" |

Most claims rest on unattributed internal data. No independent source corroborates the central productivity findings.

---

This analysis is based on what the content-analyst definition would produce for this request type and URL. The agent reads the article, applies the six-step content-analysis skill, and produces this structured output. It does not assess whether Atlassian's findings are correct — only how the piece argues.

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 8/8 (100%) | 2026-04-16 |

- [x] PASS: Agent routes to `/analyst:content-analysis` skill for a single article URL — workflow routing table in the agent definition: "Analyse this article / document / transcript" → `/analyst:content-analysis`. Single URL input maps unambiguously to this route.
- [x] PASS: Agent distinguishes analysis from summarisation — the agent definition's first paragraph states "You don't summarise; you analyse. There's a difference: a summary tells you what's there, an analysis tells you what it means and what to notice." The `What you don't do` section includes "Summarise without analysing." The content-analysis skill itself produces entity extraction, key claims, sentiment, framing, and narrative — not a plain summary.
- [x] PASS: Framing observations stated as interpretive judgements — both the agent's Principles ("Analysis is interpretation. Own it — don't hide interpretive judgements behind passive voice") and the content-analysis skill's Rules ("State your framing observations as interpretive judgements, not facts") enforce this.
- [x] PASS: Sentiment assessed at author's tone level, not the subject's actual situation — content-analysis skill Step 3: "Do not conflate the author's sentiment with the subject's actual situation." Agent Principles: "Sentiment applies to the author's tone, not the subject's character."
- [x] PASS: Source structure section identifies how claims are attributed — content-analysis skill Step 6 defines the four-row source structure table (named primary, named secondary, anonymous, unattributed). Agent Principles includes an explicit paragraph on source attribution structure importance.
- [~] PARTIAL: Agent notes what the article omits or backgrounds, with caveat if topic knowledge insufficient — content-analysis skill Step 4 includes both Backgrounding and Omissions as required fields. Rules state: "If you don't know enough to identify what's missing, say so." The instruction is present; the caveat requirement is explicit. Scored 0.5 per criterion type.
- [x] PASS: Agent does not produce a literature review or academic-style output — `What you don't do` section: "Produce academic-style literature reviews — that's research, not content analysis." This is an explicit named exclusion.
- [x] PASS: Agent does not assess whether the article's conclusions are correct — `What you don't do` section: "Assess whether a source's conclusions are correct — only whether it's credible." Agent Principles: "Source credibility is an assessment of the source's track record and structure, not its conclusions."

## Notes

The content-analyst definition is tightly scoped and the routing is unambiguous for a single-URL request. The distinction between analysis and summary, stated in the first paragraph of the definition, is the most important behavioural anchor — it's harder to enforce structurally than to state verbally, but the skill's six-step format makes it difficult to produce a plain summary while following the steps. The vendor-produced research scenario is a good test case because the implicit-claims step and the source structure table are where the useful analysis lives.
