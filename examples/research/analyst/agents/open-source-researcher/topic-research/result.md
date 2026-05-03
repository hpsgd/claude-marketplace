# Topic Research

Scenario: A user needs background research on edge computing adoption in Australian manufacturing before a client meeting.

## Prompt

> I need background research on edge computing adoption in Australian manufacturing. Specifically: how widely is it being adopted, what's driving it, and what are the main barriers? I need this for a client meeting on Friday — Standard tier is fine.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I have enough across 5-6 sources to synthesize. Writing the report now.

---

## Research: Edge Computing Adoption in Australian Manufacturing

**Date:** 2026-05-01
**Tier:** Standard
**Sources:** 6

---

### Adoption levels

No single survey directly measures what percentage of Australian manufacturers have deployed edge computing — the data is bundled under broader IIoT and "smart factory" figures. What those figures show is strong growth from a moderate base:

- Australia's industrial IoT market was valued at **USD 9.1 billion in 2025**, projected to reach USD 27.3 billion by 2034 (12.54% CAGR). Edge computing is explicitly listed alongside 5G as a key enabling layer of this growth.
- Australia's smart factory automation market hit **USD 2.2 billion in 2025**, projected to USD 4.85 billion by 2034.
- The Asia-Pacific region is forecast to be the fastest-growing edge computing market globally (~10.5% CAGR), with Australia cited as a contributor via smart-city and industrial infrastructure investment.
- From early 2026, there are reports of SMEs increasingly adopting modular, plug-and-play automation solutions — suggesting edge adoption is moving down-market, but still early-stage for smaller operators.

Mining and resources is the leading sector pulling this investment, with manufacturing a close beneficiary, particularly food & beverage, automotive components, and advanced materials.

---

### What's driving it

Five overlapping drivers come up consistently:

**1. Real-time processing demands.** Predictive maintenance and quality control require millisecond decisions that cloud round-trips can't support. Locally processed sensor data — vibration, temperature, pressure — enables anomaly detection before failures, reducing unplanned downtime.

**2. 5G infrastructure rollout.** Telcos accelerating 5G deployment have given manufacturers the underlying connectivity to deploy distributed edge architecture at scale. 5G + edge is increasingly treated as a paired infrastructure decision.

**3. Government push for sovereign manufacturing.** The Albanese government's *Future Made in Australia* budget committed a **$22.7 billion package** targeting industrial technology adoption and digital transformation. CSIRO's Future Digital Manufacturing Fund is separately investing in AI-based manufacturing tech for Australian businesses, with a specific brief to lower the IoT barrier for SMEs.

**4. Rising labour costs.** Manufacturers are using edge-enabled automation (robotic welding, vision-based QC, conveyor control) to offset wage pressures and address chronic skilled-trades shortages.

**5. Data sovereignty and latency economics.** Sending high-frequency machine data to centralised cloud is both expensive and exposes sensitive production data off-site. Keeping processing on-premises addresses both cost and security concerns, particularly relevant for defence-adjacent manufacturers.

---

### Main barriers

**Skills shortage — the most consistently cited constraint.** Australia needs an estimated **312,000 additional tech workers by 2030**. Digital skills gaps already cost large businesses **$3.1 billion per year**, a figure projected to reach $16 billion by 2030. For manufacturing specifically, edge deployments require OT/IT convergence skills (systems integration, cybersecurity, data engineering) that are scarce and expensive.

**Connectivity gaps in regional/remote locations.** Many Australian manufacturers operate outside metro areas. Consistent high-speed connectivity — a prerequisite for hybrid edge-cloud architectures — remains patchy in regional and rural sites, creating a two-speed adoption environment.

**Legacy system integration costs.** Most Australian manufacturers still run operational technology from Industry 2.0/3.0 eras. Connecting brownfield equipment to edge infrastructure is expensive and disruptive; it rarely qualifies for standard capex cycles.

**Initial capital outlay.** Edge servers, industrial-grade sensors, and supportive network infrastructure represent a significant upfront investment, particularly prohibitive for SMEs without access to financing or government co-investment programs.

**Regulatory and standards fragmentation.** Australia's regulatory frameworks evolved around older manufacturing paradigms. Interoperability between OT vendors and across edge architectures lacks standardisation, creating complexity that slows procurement and integration decisions.

**Management knowledge gaps.** Low awareness of what edge computing actually delivers — and how to build an ROI case — remains a genuine adoption barrier at the leadership level, particularly outside the mining and resources sector where use cases are better understood.

---

### Key uncertainties

- **No reliable survey data** exists on the specific percentage of Australian manufacturers running edge computing today. Market projections (IMARC, MarketsAndMarkets) are commercial forecasts and should be treated as directional, not precise.
- The ASPI *Breaking Down Barriers to Industry 4.0 in the North* report (2023) likely contains relevant government-commissioned data, but it was inaccessible during this research — worth pulling directly if specific policy context is needed for the client meeting.
- Edge computing statistics are frequently bundled with IIoT and smart manufacturing figures. It is difficult to isolate edge-specific spend or deployment counts from broader digital transformation data.
- Adoption among SMEs is reported as "growing" but quantitative evidence is thin. CSIRO's active work on lowering IoT barriers suggests the SME problem is recognised but unsolved.

---

### Sources

1. [Australia Industrial IoT Market 2034 — IMARC Group](https://www.imarcgroup.com/australia-industrial-iot-market) — market sizing, growth drivers, barriers, government initiatives
2. [Future Digital Manufacturing Fund — CSIRO](https://www.csiro.au/en/work-with-us/industries/manufacturing/future-digital-manufacturing-fund) — sovereign manufacturing push, SME IoT barrier reduction
3. [Australia Industrial IoT: Smart Manufacturing Adoption & Edge Computing Integration — vocal.media/futurism](https://vocal.media/futurism/australia-industrial-io-t-market-smart-manufacturing-adoption-predictive-maintenance-solutions-and-edge-computing-integration) — market figures, 5G/edge pairing, skills shortage data
4. [Breaking Down Barriers to Industry 4.0 in the North — ASPI](https://www.aspi.org.au/report/breaking-down-barriers-industry-40-north) — regulatory and structural barriers (inaccessible during research; recommend direct access)
5. [Edge Computing Automation Driving Manufacturing Revolution — EIT](https://www.eit.edu.au/edge-computing-and-automation-smart-manufacturing/) — Australian manufacturing use cases and drivers
6. [Industrial Edge Computing: Accelerating Industry 4.0 — STL Partners](https://stlpartners.com/articles/edge-computing/industrial-edge/) — interoperability and OT/IT convergence challenges

---

The short version for your meeting: adoption is growing solidly from a mid-maturity base, led by mining and larger manufacturers, with SMEs just starting to move. The $22.7B government package and 5G rollout are the clearest near-term accelerants. Skills and legacy integration are the biggest real-world brakes — not a lack of appetite.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PARTIAL |
| Score | 8.5/12.5 (68%) |
| Evaluated | 2026-05-01 |
| Target duration | 110563 ms |
| Target cost | $0.3732 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent invokes `/analyst:web-research` with Standard tier | FAIL | The captured output begins with 'I have enough across 5-6 sources to synthesize. Writing the report now.' — no invocation of `/analyst:web-research` is shown. The report header includes 'Tier: Standard' but this appears to be self-labelling within the output, not evidence of skill invocation. |
| c2 | Every finding cites a source that has been fetched and read — no uncited assertions | PARTIAL | A sources section lists 6 URLs with descriptions, providing post-hoc coverage of most claims. However, several specific assertions lack inline citation: 'From early 2026, there are reports of SMEs increasingly adopting modular, plug-and-play automation solutions'; '$22.7 billion package'; 'Asia-Pacific region is forecast to be the fastest-growing edge computing market (~10.5% CAGR)'. Statistics like 312,000 tech workers and $3.1B are attributed to vocal.media implicitly but not with inline markers. |
| c3 | Agent prioritises AU sources (ABS, ABC News, industry associations, AFR) over US or UK equivalents for an AU-specific question | FAIL | None of the criterion's preferred AU sources (ABS, ABC News, AFR, AMTIL, industry associations) appear. Of 6 sources: IMARC Group is a global commercial research firm; vocal.media is a user-generated content platform; STL Partners is a UK telecom research firm. CSIRO and ASPI are Australian, but ASPI was inaccessible and yielded no data. EIT (eit.edu.au) is Australian but is an educational institution, not an industry body or press outlet. |
| c4 | Sources are authority-ranked — government or industry body data takes precedence over blog posts or vendor content | PARTIAL | Government data (CSIRO Future Digital Manufacturing Fund) and the ASPI report are cited, and government initiatives ($22.7B package) are treated as primary. However, key statistics — skills shortage (312,000 workers, $3.1B per year, $16B by 2030) — are sourced from vocal.media (user-generated content) without any qualification of its relative authority. No explicit authority-ranking logic is stated in the output. |
| c5 | Where sources conflict or evidence is thin, agent flags this explicitly rather than presenting contested findings as settled | PASS | A dedicated 'Key uncertainties' section explicitly states: 'No reliable survey data exists on the specific percentage of Australian manufacturers running edge computing today. Market projections (IMARC, MarketsAndMarkets) are commercial forecasts and should be treated as directional, not precise.' It also flags the inaccessible ASPI report, bundling of edge stats with IIoT figures, and thin quantitative evidence on SME adoption. |
| c6 | Agent does not hand off to business-analyst or osint-analyst — this is a general topic research request, not a company or infrastructure investigation | PASS | The entire output is a self-contained research report. No handoff or delegation to business-analyst or osint-analyst is mentioned anywhere in the captured output. |
| c7 | Agent notes gaps where authoritative data doesn't exist publicly, rather than padding with lower-quality sources to appear thorough | PARTIAL | The 'Key uncertainties' section explicitly acknowledges gaps: no reliable survey data on adoption %, edge statistics bundled with broader IIoT, and thin quantitative evidence on SMEs. However, the agent also cites vocal.media (user-generated platform) for key quantitative statistics, which is lower-quality padding rather than acknowledging the gap in authoritative data for those figures. |
| c8 | Output is organised by theme, not by 'here's what each source said' | PASS | Output uses thematic headers: 'Adoption levels', 'What's driving it', 'Main barriers', 'Key uncertainties', followed by a separate 'Sources' list. No section presents findings by source ('Source 1 said X, Source 2 said Y'). |
| c9 | Output addresses the three explicit research questions — adoption rate / how widely, drivers, barriers — each as a section, NOT collapsed into a generic 'edge computing in Australian manufacturing' summary | PASS | Three separate sections directly map to the three research questions: 'Adoption levels' covers how widely adopted; 'What's driving it' covers drivers (five itemised sub-points); 'Main barriers' covers barriers (six itemised sub-points). Not collapsed into a generic summary. |
| c10 | Output's sources are predominantly Australian — AMTIL, AMGC, ABS, AFR, IBISWorld AU, Australian government bodies (DISR), CSIRO — over US / EU sources for an AU-specific question; non-AU sources used only as comparators | FAIL | Of 6 sources: CSIRO (AU), ASPI (AU, but inaccessible/no real data), EIT/eit.edu.au (AU educational) are Australian. IMARC Group (global commercial), vocal.media (global UGC), STL Partners (UK firm) are non-AU. None of the criterion's named AU sources (AMTIL, AMGC, ABS, AFR, IBISWorld AU, DISR) appear. With ASPI yielding no usable data, effectively 2 real AU sources out of 6 — not predominantly Australian. |
| c11 | Output flags conflicts or thin evidence where sources disagree | PASS | The 'Key uncertainties' section flags four distinct areas of thin evidence: no survey-level adoption data; market forecasts should be treated as directional; edge stats bundled with IIoT making isolation difficult; SME adoption reported as 'growing' but 'quantitative evidence is thin.' The closing caveat 'CSIRO's active work on lowering IoT barriers suggests the SME problem is recognised but unsolved' also signals contested/unresolved state. |
| c12 | Output uses Standard tier — moderate depth, fetched primary and secondary sources, but NOT exhaustive deep-research with all six passes; the prompt names Standard explicitly | PASS | Report header explicitly states 'Tier: Standard' and 'Sources: 6'. The depth is moderate — three themed sections with supporting data points, a short uncertainties section, and 6 listed sources. No claim of exhaustive multi-pass research. Consistent with Standard tier scope. |
| c13 | Output is organised by theme (adoption / drivers / barriers / examples) NOT by source ('AFR said X, ABC said Y') — the structure serves the research question | PASS | Structure: 'Adoption levels' / 'What's driving it' (with 5 sub-themes) / 'Main barriers' (with 6 sub-themes) / 'Key uncertainties' / 'Sources'. Sources are listed separately at the end, not interwoven as 'Source X said Y'. Structure directly serves the three research questions posed in the prompt. |

### Notes

The output produces a well-structured, thematically organised research report that directly addresses all three research questions and includes a commendable 'Key uncertainties' section flagging thin evidence. However, it fails on two of the most important criteria for an AU-specific research task: it does not invoke the `/analyst:web-research` skill (c1), and its sources are not predominantly Australian (c3, c10) — relying on IMARC (global commercial), vocal.media (user-generated content), and STL Partners (UK) rather than ABS, AFR, AMTIL, AMGC, or IBISWorld AU. Using vocal.media as a source for major quantitative claims (skills shortage figures) also undercuts the authority-ranking criterion (c4). The output's structural quality and uncertainty flagging are strong, but the sourcing strategy is the core weakness for an AU-market research task.
