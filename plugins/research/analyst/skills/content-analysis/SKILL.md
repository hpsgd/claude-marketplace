---
name: content-analysis
description: "Structured analysis of a piece of text: entity extraction, key claims, sentiment, framing, and narrative identification. Use when you need to understand not just what content says but how it says it and what it leaves out."
argument-hint: "[paste content or provide URL]"
user-invocable: true
allowed-tools: WebFetch
---

Perform structured content analysis on $ARGUMENTS.

If a URL is provided, fetch the content first. If content is pasted directly, proceed to Step 1.

## Step 1: Entity extraction

Identify and categorise all named entities in the content:

| Entity type | What to extract |
|---|---|
| People | Full names, roles/titles, organisations they're associated with |
| Organisations | Companies, institutions, government bodies, NGOs |
| Locations | Countries, cities, specific venues |
| Dates and timeframes | Specific dates, relative timeframes ("last year", "in Q3") |
| Products/technologies | Named products, platforms, systems |
| Financial figures | Any monetary amounts with their context |

For each person or organisation that appears substantively (not just mentioned in passing), note: are they a source, a subject, or a referenced authority?

## Step 2: Key claims

Extract the central claims the content makes — not summaries of sections, but the specific assertions:

- **Primary claim:** the main argument or finding
- **Supporting claims:** evidence or reasoning offered in support
- **Implicit claims:** assertions made without being explicitly stated (these are often the most significant)

For each claim, note: is it attributed to a named source, an anonymous source, the author's own assertion, or presented as established fact?

## Step 3: Sentiment analysis

Assess sentiment at three levels:

**Overall tone:** Positive / Negative / Neutral / Mixed — with a one-sentence justification.

**Targets of sentiment:** Who or what is the sentiment directed at? A piece can be positive about one subject and critical of another simultaneously.

**Language signals:** Note specific word choices that carry sentiment weight. Loaded language, euphemisms, and emotionally charged terms are explicit choices — flag them.

Do not conflate the author's sentiment with the subject's actual situation. "The company faces significant challenges" is sentiment about the company's situation; whether those challenges are real is a separate question.

## Step 4: Framing analysis

Framing is what the content foregrounds, backgrounds, and omits. It's not about accuracy — a piece can be factually correct and still frame things in a particular direction.

Assess:

**Perspective:** Whose viewpoint structures the piece? Who gets quoted, who is spoken about, and who is absent?

**Foregrounding:** What is emphasised — what appears in headlines, ledes, and summary statements?

**Backgrounding:** What is mentioned but minimised — relegated to later paragraphs, qualified, or framed as context?

**Omissions:** What relevant information, perspective, or context is absent? (This requires knowing enough about the topic to recognise what's missing.)

**Framing devices:** Note any: crisis framing, progress framing, conflict framing, human interest framing, responsibility framing. These structures shape how readers process information.

State your framing observations as interpretive judgements, not facts: "The piece frames X as..." not "The piece proves X is..."

## Step 5: Narrative identification

What story is this piece telling? Narratives are recurring story structures that activate particular audience responses:

- **Hero/villain:** someone is doing the right thing against opposition
- **Crisis/urgency:** things are bad and getting worse, action is needed now
- **Progress/innovation:** things are improving, this development is positive
- **Conflict/battle:** two sides are opposed, the reader must choose
- **Revelation/exposure:** hidden truth is being brought to light
- **Human cost:** abstract issues rendered personal through individual stories

Multiple narratives can operate simultaneously. Identifying the dominant narrative helps explain why a piece feels the way it does even when the facts are accurate.

## Step 6: Source structure

How is the piece sourced?

- **Named primary sources:** people who are on the record
- **Named secondary sources:** cited studies, reports, or prior coverage
- **Anonymous sources:** how many, how described, and for what claims?
- **No attribution:** claims asserted without any source

A piece heavily reliant on anonymous sources or unattributed assertions warrants lower confidence regardless of publication credibility.

## Rules

- Framing analysis is interpretive. Own the interpretation — don't present it as fact.
- Sentiment applies to the author's choices, not the subject's reality.
- Omission analysis requires topic knowledge. If you don't know enough to identify what's missing, say so.
- Implicit claims are often the most significant. Name them explicitly.
- One piece is rarely sufficient for conclusions about a topic. Note when analysis of additional coverage would strengthen or weaken findings.

## Output format

```markdown
## Content analysis: [Title or source]

**Date of content:** [publication date if known]
**Date of analysis:** [today]
**Word count:** [approximate]

### Entities

**People:** [name — role — source/subject/authority]
**Organisations:** [name — role in piece]
**Key figures cited:** [financial amounts, dates, statistics with context]

### Key claims

**Primary claim:** [the central assertion]
**Supporting claims:** [bulleted list with attribution type for each]
**Implicit claims:** [unstated but operative assertions]

### Sentiment

**Overall tone:** [Positive / Negative / Neutral / Mixed]
**Sentiment targets:** [who/what the tone is directed at]
**Notable language signals:** [specific word choices worth flagging]

### Framing

**Perspective:** [whose viewpoint structures the piece]
**Foregrounded:** [what is emphasised]
**Backgrounded:** [what is minimised]
**Omissions:** [what's absent — or "insufficient topic knowledge to assess"]
**Dominant framing device:** [crisis / progress / conflict / revelation / other]

### Narrative

[What story is being told, and what audience response it activates]

### Source structure

| Source type | Count | For what claims |
|---|---|---|
| Named primary | — | — |
| Named secondary | — | — |
| Anonymous | — | — |
| Unattributed | — | — |

### Summary assessment

[2-3 sentences: what this analysis tells you about the content beyond its face value]
```
