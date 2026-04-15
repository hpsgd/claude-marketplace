---
name: deep-research
description: "Multi-pass exhaustive investigation of a topic with entity scoring, source triangulation, and explicit gap analysis. Use when web-research Deep tier isn't sufficient — typically for unfamiliar domains, contested topics, or high-stakes decisions requiring the strongest possible evidence base."
argument-hint: "[research question or topic]"
user-invocable: true
allowed-tools: WebSearch, WebFetch
---

Conduct a multi-pass deep investigation into $ARGUMENTS.

This skill goes further than `/analyst:web-research` Deep tier. It runs multiple structured passes, scores entities by confidence, triangulates claims across source types, and produces an explicit gap analysis. Use it when you genuinely need the most thorough public-data investigation possible — not as a default.

## Pass 1: Domain mapping

Before searching for facts, map the domain itself.

1. **Authoritative sources:** who produces primary data in this domain? (government agencies, regulatory bodies, standards organisations, research institutions)
2. **Key entities:** what organisations, people, and publications are central to this topic?
3. **Contested terrain:** what aspects of this topic are genuinely disputed vs what is settled?
4. **Temporal scope:** what time range is relevant? Are there distinct eras in how this topic has evolved?

Spend time here. Domain mapping produces a search strategy. Without it, you're searching blind.

## Pass 2: Primary source sweep

Systematic sweep of authoritative and primary sources identified in Pass 1.

For each source:

- Fetch the most relevant primary documents (reports, filings, published data)
- Extract key claims with verbatim quotes where significant
- Note methodology: how was this data collected, and what are its known limitations?

Do not rely on summaries of primary sources. Fetch and read the source.

## Pass 3: Secondary source sweep

News coverage, analyst commentary, expert opinion, academic literature.

Search across source types independently — don't let one source type dominate:

- Journalism: Reuters, AP, major regional (ABC News AU, RNZ, BBC, FT, AFR)
- Academic: Google Scholar, arXiv, SSRN, PubMed depending on domain
- Industry: IBISWorld AU, Gartner, IDC
- Community: relevant forums, practitioner communities (treat as low-authority signal, not evidence)

## Pass 4: Entity scoring

For each significant entity (person, organisation, claim, dataset) encountered across Passes 2 and 3, assign a confidence score:

| Score | Criteria |
|---|---|
| **High** | Confirmed by 2+ independent primary sources; no contradicting evidence |
| **Medium** | Confirmed by 1 primary source or 2+ secondary sources; minor inconsistencies |
| **Low** | Single secondary source only; or primary source with known methodology limitations |
| **Contested** | Multiple credible sources actively disagree |
| **Unverified** | Asserted but no independent confirmation found |

This scoring step is the key difference from a standard deep research pass. Surface contested and unverified findings explicitly — they're often more important than the high-confidence ones.

## Pass 5: URL and source verification

For every source cited:

- Verify the URL is live and resolves to the claimed content
- Confirm the publication date — AI training data, cached pages, and archive links can surface outdated versions
- For academic papers: check the publication venue (peer-reviewed journal vs preprint server vs conference proceedings vs blog post)
- For statistics: trace back to the original data collection, not just a reference to it

A cited source that can't be verified gets downgraded to Unverified regardless of how it was described.

## Pass 6: Gap analysis

What is genuinely unknown after exhausting public sources?

Gaps fall into categories:

- **Not yet public:** data exists but isn't released (e.g., regulatory filings not yet processed)
- **Behind paywall:** exists but requires paid access (note the source and access route)
- **Requires primary research:** only obtainable through surveys, interviews, or direct access
- **Genuinely unknown:** no credible source has this data; it may not exist

Be specific about which category each gap falls into. "Information not available" without categorisation is unhelpful.

## Rules

- Primary sources over summaries. Always.
- Entity scoring is mandatory. Don't skip it to get to the output faster — it's the point.
- URL verification is mandatory. A dead link is not a source.
- Contested findings get their own section. Don't bury disagreement in footnotes.
- Gap analysis is a deliverable, not an afterthought. A thorough gap analysis tells the reader what to investigate next and how.

## Output format

```markdown
## Deep research: [Topic]

**Date:** [today]
**Passes completed:** 6
**Sources reviewed:** [count]

### Domain map

[Authoritative sources, key entities, contested terrain, temporal scope]

### Findings

#### [Theme 1]

[Findings with entity scores and inline citations]

#### [Theme 2]

[Findings with entity scores and inline citations]

### Entity confidence summary

| Entity / Claim | Score | Evidence | Contradictions |
|---|---|---|---|
| [claim] | High / Medium / Low / Contested / Unverified | [sources] | [if any] |

### Contested findings

[Where credible sources actively disagree — present each position with its evidence]

### Source verification

| Source | URL live | Date confirmed | Venue/type |
|---|---|---|---|
| [source] | Yes / No | [date] | [peer-reviewed / preprint / news / etc.] |

### Gap analysis

| Gap | Category | Access route |
|---|---|---|
| [what's unknown] | Not yet public / Paywall / Primary research needed / Unknown | [if applicable] |

### Sources

1. [Title](URL) — [authority level] — [entity score contribution]
```
