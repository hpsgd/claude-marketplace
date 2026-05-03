# Multi Source Comparison

Scenario: A user provides three articles on the same topic from different source types (financial press, progressive press, industry body) and asks the content analyst to compare framing and source quality before citing them in a policy brief.

## Prompt

> I have three articles about Australia's critical minerals strategy — one from the AFR, one from The Guardian, and one from the Minerals Council of Australia's website. Can you analyse how each one frames the issue differently? I want to understand the framing and source quality before I cite any of them in a policy brief.
> 
> Here are the three articles:
> 
> ---
> 
> **ARTICLE 1 — Australian Financial Review**
> 
> **Australia's Critical Minerals Opportunity: Why We Can't Afford to Blink**
> *Australian Financial Review, March 12, 2024. By Angela Marsh, Resources Correspondent.*
> 
> Australia sits atop one of the richest deposits of critical minerals on earth — lithium, cobalt, nickel, rare earths — at precisely the moment global demand for these materials is accelerating. The energy transition is not a future event; it is happening now, and the nations that control the supply of battery minerals will define the next industrial epoch.
> 
> The federal government's Critical Minerals Strategy, released late last year, correctly identifies Australia as a potential "renewable energy superpower." What it underestimates is the pace required. China currently processes roughly 60% of the world's lithium, 65% of its cobalt, and more than 80% of its rare earths. Australia ships raw ore and imports the value-added products back. This is a structural weakness that compounding investment can correct — but only if the regulatory and infrastructure settings attract capital rather than repel it.
> 
> The economics are compelling. Benchmark Mineral Intelligence estimates that meeting 2030 electric vehicle demand alone will require $514 billion in new mine and processing capacity globally. Macquarie Bank forecasts that Australian lithium exports could grow fivefold by 2030 if processing capacity is onshored. That is not a prediction — it is a conditional: if the approvals pipeline moves.
> 
> The strategic logic extends beyond economics. Japan, South Korea, the United States, and the European Union are all scrambling to reduce exposure to Chinese supply chains. Several bilateral agreements signed in the past 18 months — including the US–Australia Critical Minerals Partnership and supply agreements with Japan under the Quad framework — reflect this. The question is whether domestic policy settings are fast enough to match the opportunity window.
> 
> Current approval timelines for new mining projects average 4.7 years. Canada's fast-track critical minerals process averages 2.1 years. For an industry where first-mover advantage determines who captures downstream processing investment, this gap is not a minor inconvenience. The government's response — a Critical Minerals List and a $2 billion facility — signals intent. It does not yet signal urgency.
> 
> ---
> 
> **ARTICLE 2 — The Guardian Australia**
> 
> **The dark side of Australia's critical minerals rush**
> *The Guardian Australia, April 3, 2024. By Sienna Okafor, Environment Correspondent.*
> 
> The language of the energy transition has become a kind of moral permission slip. Because critical minerals are essential for batteries, solar panels, and electric vehicles, the logic runs, extracting them at scale is not just commercially sound but environmentally necessary. The contradiction embedded in this argument — that we must damage ecosystems to save them — is rarely examined.
> 
> The Pilbara, the Kimberley, the Flinders Ranges, and the Northern Territory — the regions identified in government strategy documents as priority areas for critical mineral extraction — are not blank administrative canvases. They are the country of Aboriginal and Torres Strait Islander peoples, many of whom have fought for decades to achieve the native title determinations now being tested by the pace of exploration licence approvals.
> 
> Professor Megan Davis, who has spent her career at the interface of Indigenous law and resources policy, has described the current moment as "the fastest erosion of free, prior and informed consent I've seen since the mining boom of the 2000s." Community consultations that should take 12–18 months are being compressed into weeks.
> 
> The science, too, is more complicated than the government narrative allows. Processing lithium and nickel generates sulphuric acid and toxic tailings. The water footprint of lithium brine extraction in arid environments is substantial. A study published in Nature Sustainability in 2023 found that when full lifecycle emissions are included, the carbon intensity of some processing pathways rivals that of the fossil fuel technologies they are meant to replace.
> 
> Conservation groups including the Wilderness Society and the Australian Conservation Foundation have raised concerns that Strategic Assessment provisions — allowing the federal government to fast-track approvals in exchange for high-level environmental commitments — provide cover for individual project impacts that would otherwise require closer scrutiny. The Environment Protection and Biodiversity Conservation Act has not been reformed since 1999; the government's own review, completed in 2020, recommended significant changes that have not been legislated.
> 
> None of this means Australia should not develop its critical minerals sector. It means the framing of the sector as a clean-energy story, rather than a mining story with clean-energy applications, obscures costs borne by communities and ecosystems — not by the shareholders who benefit.
> 
> ---
> 
> **ARTICLE 3 — Minerals Council of Australia**
> 
> **Critical Minerals: Delivering for Australia's Future**
> *Minerals Council of Australia, January 2024 Policy Position.*
> 
> Australia's critical minerals sector is at an inflection point. The global transition to clean energy technologies has created structural demand for minerals that Australia has in abundance — lithium, cobalt, vanadium, graphite, and a suite of rare earth elements essential for the permanent magnets in wind turbines and electric vehicle motors.
> 
> The Minerals Council of Australia represents the companies investing to develop this opportunity. Our members have committed more than $38 billion in announced critical minerals projects over the next decade. These investments will create 85,000 direct jobs in regional Australia — communities that have borne the brunt of agricultural downturns and manufacturing decline and are positioned to benefit most from a well-managed resource transition.
> 
> The strategic case is clear. Australia's Five Eyes partners — the United States, United Kingdom, Canada, and New Zealand — have each identified critical mineral supply security as a national security priority. Australia's geological endowment and institutional stability make it the partner of choice for friendly-nation supply chains.
> 
> To realise this potential, government must address the regulatory bottlenecks deterring investment. Project approval timelines are too long. Royalty frameworks designed for bulk commodity exports need updating for value-added processing. Infrastructure — particularly rail, water, and power to remote deposits — requires co-investment the private sector cannot provide unilaterally.
> 
> The MCA calls for a coordinated Critical Minerals Investment Compact: a single-window approval pathway, matched infrastructure co-investment, and a sovereign processing fund to support domestic value-add. Australia's major trading partners are moving fast; the window for positioning as the world's preferred critical minerals supplier will not remain open indefinitely.
> 
> ---

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll break down the framing, evidence quality, and potential biases in each source:

## **Article 1 — AFR (Marsh)**
**Framing:** Economic opportunity + national competitiveness  
**Bias:** Market-oriented, pro-development, but from a business publication with editorial standards

**Strengths:**
- Cites specific third-party analysts (Benchmark Mineral Intelligence, Macquarie Bank)
- Quantifies the opportunity ($514B capex need) and the gap (4.7 vs 2.1 year approvals)
- Acknowledges regulatory bottlenecks as the constraint, not geology or demand
- Credible sourcing (analyst reports are traceable; bilateral agreements are public record)

**Weaknesses:**
- Treats government strategy as gospel without critical distance
- No discussion of environmental or social costs — notably absent for a major extraction story
- The comparison to Canada's timeline needs context (different regulatory scope, different environmental standards)
- Frames the issue entirely through capital velocity

**Cite as:** A reliable source on *economic framing and the investment case*, with the caveat that it doesn't address non-economic constraints.

---

## **Article 2 — Guardian (Okafor)**
**Framing:** Environmental justice + Indigenous rights  
**Bias:** Explicitly critical of extraction; pro-Indigenous, pro-conservation stance

**Strengths:**
- Centers Indigenous voices and legal concepts (free, prior and informed consent)
- Quotes a credible legal scholar (Megan Davis) with named expertise
- Raises concrete technical concerns (sulphuric acid, water footprint, lifecycle emissions)
- Flags an actual regulatory gap (EPBC Act last reformed 1999; 2020 review not legislated)
- Transparent about its critical stance

**Weaknesses:**
- The Nature Sustainability study is cited but not linked — verify the 2023 claim and what it actually found
- "Consultations compressed into weeks" is asserted without specific examples; needs documentation
- The claim that Strategic Assessment allows "cover for impacts" is argumentative without citing specific cases
- Counterpoint: this is *interpreting* environmental impact, not inventing it — but verify the specific assertions

**Cite as:** A critical perspective on *social and environmental costs*, with verification required for specific claims (the Nature Sustainability study, consultation timelines, specific consultation examples). The EPBC Act gap is factual and citable.

---

## **Article 3 — MCA**
**Framing:** Economic development + national security  
**Bias:** Direct industry advocacy — this is a policy position, not journalism

**Strengths:**
- Transparent about who is speaking (industry body)
- Employment figure (85k jobs) is based on announced projects — traceable to member companies
- $38B investment figure is likely aggregated from member announcements
- Five Eyes framing reflects actual government statements

**Weaknesses:**
- Zero acknowledgment of trade-offs or costs (environmental, Indigenous, or otherwise)
- "Communities that have borne the brunt of agricultural downturns" — this is framed as unambiguous upside, but regional employment shifts have social costs
- "Regulatory bottlenecks" assumes the current approvals timeline is wrong rather than reflecting legitimate environmental/Indigenous review
- No discussion of where processing investment actually goes (hint: often not Australia)
- The "sovereign processing fund" is a proposal, not an existing commitment

**Cite as:** The *industry's economic case*, with the clear caveat that this is advocacy literature with vested interests. Use specific numbers (jobs, investment) with that framing. Do not cite it for claims about environmental or social impacts.

---

## **For your policy brief:**

**Strong citations:**
- AFR for *market-based opportunity framing and approval timeline gaps* (verifiable)
- MCA for *industry investment commitments and jobs projections* (traceable to members, but framed as industry position)
- Guardian's reporting on *EPBC Act regulatory gaps* and *Indigenous consultation concerns* (but verify specific consultation examples)

**Red flags to avoid:**
- Don't cite MCA on environmental or social impacts (naked conflict of interest)
- Don't cite AFR's implicit assumption that approvals should be faster (that's assumption, not reporting)
- Don't cite Guardian's processing emissions claim without verifying the Nature Sustainability study

**Recommend:** Get the actual Nature Sustainability paper before citing Guardian's claim about lifecycle emissions. And if you cite approval timelines, do a quick check on whether the 4.7-year AFR figure is current — regulatory timelines shift.

The pattern is clear: each source has a legitimate framing, but together they're telling you there's a real tension between *opportunity speed* (AFR/MCA framing) and *environmental/social review adequacy* (Guardian framing). Your brief's job is naming that tension, not pretending one framing is right.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.5/17.5 (94%) |
| Evaluated | 2026-05-02 |
| Target duration | 26304 ms |
| Target cost | $0.0235 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent routes each article to content-analysis skill separately, then produces a comparative view | PASS | Output contains three clearly separated per-article sections (Article 1 — AFR, Article 2 — Guardian, Article 3 — MCA) each with independent analysis, followed by a distinct 'For your policy brief' comparative section. |
| c2 | Framing differences between the three sources are stated as interpretive observations, not facts | PASS | Each article is given a labelled 'Framing:' line — 'Economic opportunity + national competitiveness', 'Environmental justice + Indigenous rights', 'Economic development + national security' — clearly tagged as interpretive characterisations. The closing paragraph explicitly says 'each source has a legitimate framing.' |
| c3 | Source credibility differences are noted (industry body vs independent press) | PASS | MCA is labelled 'Direct industry advocacy — this is a policy position, not journalism'; AFR is described as a 'business publication with editorial standards'; Guardian is characterised as having an 'Explicitly critical' stance. Credibility distinctions are drawn for all three. |
| c4 | Each article's source structure is assessed independently (named/anonymous/unattributed sources) | PASS | AFR: 'Cites specific third-party analysts (Benchmark Mineral Intelligence, Macquarie Bank)'; Guardian: 'Quotes a credible legal scholar (Megan Davis)' but 'asserted without specific examples'; MCA: 'Employment figure (85k jobs) is based on announced projects — traceable to member companies'. Attribution patterns assessed independently for each. |
| c5 | The comparison identifies where the three articles agree and where they diverge on key claims | PASS | Comparative section states 'there's a real tension between opportunity speed (AFR/MCA framing) and environmental/social review adequacy (Guardian framing)'. Implicit agreement on Australia's strategic minerals endowment noted across all three; divergence on environmental/social costs is explicitly surfaced. |
| c6 | Agent recommends which source(s) are most appropriate for the policy brief context, with reasoning | PARTIAL | 'Strong citations' section maps each source to specific claim types with reasoning — AFR for 'market-based opportunity framing and approval timeline gaps (verifiable)', MCA for 'industry investment commitments and jobs projections (framed as industry position)', Guardian for 'EPBC Act regulatory gaps and Indigenous consultation concerns'. |
| c7 | Agent does not produce a merged summary — each article is analysed independently before comparison | PASS | Three separate labelled article sections precede the comparative section. The closing line states 'Your brief's job is naming that tension, not pretending one framing is right' — explicitly refusing to collapse perspectives. |
| c8 | Agent flags any claims that appear in only one source as requiring independent verification | PASS | 'Get the actual Nature Sustainability paper before citing Guardian's claim about lifecycle emissions'; 'do a quick check on whether the 4.7-year AFR figure is current'; Guardian's 'consultations compressed into weeks is asserted without specific examples; needs documentation'. |
| c9 | Output runs content-analysis independently per article first — three separate analyses for AFR, The Guardian, MCA — before any comparative view | PASS | Article 1 (AFR), Article 2 (Guardian), Article 3 (MCA) sections each appear fully before the 'For your policy brief' comparative section. Structure is unambiguously sequential: three independent analyses, then comparison. |
| c10 | Output's per-article analyses each cover the standard dimensions — entities, key claims, sentiment, framing, narrative, source structure — at parity, not deeper analysis on one article | PASS | All three articles receive the same structural template: Framing, Bias, Strengths (with key claims and sourcing), Weaknesses, and Cite-as guidance. Length and depth are comparable across all three, confirming parity. |
| c11 | Output's framing comparison states differences as interpretive observations — 'AFR frames as economic opportunity / national competitiveness; The Guardian frames as environmental / Indigenous land rights tension; MCA frames as industrial development / employment story' — clearly tagged as interpretation | PASS | AFR: 'Framing: Economic opportunity + national competitiveness'; Guardian: 'Framing: Environmental justice + Indigenous rights'; MCA: 'Framing: Economic development + national security'. All labelled as 'Framing:' lines, clearly interpretive rather than factual claims about the articles. |
| c12 | Output addresses source credibility differences — MCA is an industry advocacy body (advocacy bias toward industry positions), AFR is financial press (economic-frame bias), The Guardian is progressive-leaning (political-frame bias) — without dismissing any | PASS | MCA: 'Direct industry advocacy — this is a policy position, not journalism' but acknowledged as transparent. AFR: 'Market-oriented, pro-development, but from a business publication with editorial standards'. Guardian: 'Explicitly critical of extraction; pro-Indigenous, pro-conservation stance' but 'Transparent about its critical stance'. None dismissed — all given a 'Cite as' recommendation. |
| c13 | Output's source-structure comparison shows attribution patterns per article — e.g. MCA cites named industry executives + own commissioned research, The Guardian cites independent academics + Indigenous-community sources, AFR cites government officials + corporate executives | PASS | AFR: third-party analysts (BMI, Macquarie), bilateral agreements as public record. Guardian: named academic (Megan Davis), peer-reviewed journal (Nature Sustainability), conservation groups. MCA: member-company investment announcements, Five Eyes government statements. Attribution patterns mapped per article. |
| c14 | Output identifies where the three articles AGREE (likely on the basic economic/strategic premise) and where they DIVERGE (impact assessment, Indigenous rights, environmental cost) on key claims | PASS | Comparative section: 'tension between opportunity speed (AFR/MCA framing) and environmental/social review adequacy (Guardian framing)'. Guardian is noted as acknowledging the economic case ('None of this means Australia should not develop its critical minerals sector'), implying shared premise but divergent assessment of costs. |
| c15 | Output flags claims appearing in only one source — e.g. 'MCA claims X jobs; not corroborated in AFR or The Guardian; would need independent verification before citing in policy brief' | PASS | MCA's 85k jobs figure flagged as 'traceable to member companies' (not independently corroborated). Guardian's Nature Sustainability claim flagged: 'verify the 2023 claim and what it actually found'. AFR's 4.7-year approval timeline flagged for currency check. All are single-source claims that are explicitly called out for verification. |
| c16 | Output's recommendation for the policy brief context names which sources are appropriate for which kinds of claims — MCA for industry positions (cited as industry view, not as fact), The Guardian / academic-cited material for civil society perspective, AFR for market-impact claims | PASS | 'AFR for market-based opportunity framing and approval timeline gaps (verifiable)'; 'MCA for industry investment commitments and jobs projections (traceable to members, but framed as industry position)'; 'Guardian's reporting on EPBC Act regulatory gaps and Indigenous consultation concerns'. Explicit source-to-claim-type mapping with caveats. |
| c17 | Output does NOT produce a merged synthesis ('the truth is...') — comparison preserves the perspectives without collapsing them | PASS | Final line: 'Your brief's job is naming that tension, not pretending one framing is right.' The output preserves three distinct framings throughout and never asserts one as more accurate than others. |
| c18 | Output recommends additional source types the policy brief should consider beyond these three — academic peer-reviewed journals, Senate inquiry submissions, Indigenous-community direct sources — for a balanced citation set | FAIL | Output recommends verifying the Nature Sustainability paper (verifying an existing citation, not recommending a new source category) and checking the 4.7-year figure. No recommendation is made to consult Senate inquiry submissions, direct Indigenous-community sources, or other source categories beyond the three provided. |

### Notes

The output is a high-quality, well-structured analysis that meets nearly all criteria. It maintains consistent analytical parity across all three articles, clearly labels framing as interpretation, maps sources to appropriate citation contexts, and explicitly avoids synthesising a merged 'truth'. The main gap is c18: the output focuses on verifying existing claims rather than recommending additional source categories (Senate submissions, peer-reviewed journals, Indigenous community sources) that would round out a policy brief's citation set. This is the only substantive omission. C6 was capped at PARTIAL by the test author and is satisfied at that level.
