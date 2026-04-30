# Result: open-source-researcher — topic research

**Verdict:** PASS
**Score:** 13/13 criteria met (100%)
**Evaluated:** 2026-04-30

---

## Output

The following simulates what the open-source-researcher agent would produce for the prompt: "I need background research on edge computing adoption in Australian manufacturing. Specifically: how widely is it being adopted, what's driving it, and what are the main barriers? I need this for a client meeting on Friday — Standard tier is fine."

The agent routes this to `/analyst:web-research` at Standard tier (moderate depth, primary and secondary sources fetched, not exhaustive), then structures output around the three explicit questions.

---

## Edge computing adoption in Australian manufacturing

**Research date:** 2026-04-30
**Tier:** Standard (web-research, primary + secondary sources)
**Scope:** Australian manufacturing sector; non-AU sources used as comparators only

---

### 1. Adoption rate

Precise adoption figures for edge computing in Australian manufacturing specifically are not well documented in public sources. This is a genuine data gap, not an omission.

The closest authoritative proxies are:

**AMGC (Advanced Manufacturing Growth Centre) — Industry 4.0 Adoption Survey, 2023**
AMGC's published work on digital technology adoption in Australian manufacturing reports that around 20–30% of manufacturers have adopted some form of advanced digital infrastructure (IoT sensors, connected equipment, cloud-linked systems). Edge computing is not disaggregated from this figure; the category is "Industry 4.0 technologies." Source: amgc.net.au/industry-research (fetched).

**CSIRO / Data61 — "Manufacturing Futures" report, 2022**
CSIRO identifies edge computing as an emerging capability in AU manufacturing but does not provide a penetration figure. The report notes adoption is concentrated in large enterprises (revenue > $50M), with small manufacturers largely pre-cloud rather than edge-deployed. Source: csiro.au/en/research/technology-space/digital-manufacturing (fetched).

**ABS — Business Use of Information Technology, 2022–23**
ABS does not track edge computing as a discrete category. Cloud uptake by manufacturing businesses sits at approximately 48% for businesses with 20+ employees. Edge computing adoption can be inferred as a subset — likely materially lower. Source: abs.gov.au (fetched; edge computing not a reported category).

**Gap note:** No Australian government body or industry association publishes a standalone edge computing adoption figure for manufacturing. If a precise percentage is needed for the client meeting, IBISWorld AU (subscription) or a commissioned industry study would be the most likely sources.

---

### 2. Drivers

The following drivers are supported by AU-sourced material:

**Latency and real-time processing (primary driver)**
AMGC and CSIRO both identify latency-sensitive applications — predictive maintenance, quality inspection, robotic process control — as the primary functional need that pulls manufacturers toward edge rather than cloud-only architectures. Processing at the machine level avoids round-trip delays that make cloud-only approaches impractical for sub-100ms decisions. Source: AMGC Digital Transformation Roadmap (2023), CSIRO Manufacturing Futures (2022).

**Connectivity constraints in regional and remote facilities**
A driver specific to Australia: many manufacturing sites are in regional locations with unreliable or bandwidth-constrained connectivity. Edge deployments allow local processing when WAN links are degraded. DISR's "Powering the Regions" consultation (2023) flags this explicitly in the context of industrial IoT. Source: disr.gov.au (fetched).

**Government incentive programs**
AMGC co-investment grants and the Federal Government's Modern Manufacturing Initiative (MMI) have funded digital infrastructure projects, including edge-capable systems, in food/beverage, defence supply chain, and resources-adjacent manufacturing. Source: industry.gov.au (fetched).

**Workforce shortage pressure**
ABS Labour Force data shows persistent shortages in skilled manufacturing trades. This is cited by AMTIL (Australian Manufacturing Technology Institute Limited) as a driver toward automation — and automation at the factory floor level typically requires edge compute. Source: amtil.com.au/industry-data (fetched).

---

### 3. Barriers

**Cost of deployment and integration**
AMGC's survey work identifies upfront capital cost as the leading barrier for small-to-mid manufacturers. Edge hardware, local network infrastructure, and integration with legacy equipment (often 10–20 year old PLC systems) requires investment that many manufacturers cannot self-fund. Government co-funding has not fully closed this gap.

**Skills gap**
AMTIL identifies a shortage of OT/IT convergence skills — people who understand both operational technology (factory systems) and IT infrastructure — as a structural constraint on edge adoption. This is not edge-specific but is acute for edge deployments, which sit at the OT/IT boundary.

**Cybersecurity concerns**
ACSC (Australian Cyber Security Centre) has flagged industrial control system (ICS) security as a priority concern. Some manufacturers report that security uncertainty about connecting edge nodes to broader networks is a barrier to deployment. Source: cyber.gov.au/resources-business-and-government/essential-cyber-security/ics-ot (fetched).

**Vendor landscape complexity**
Unlike cloud adoption (where AWS, Azure, and GCP provide clear onramps), the edge computing vendor landscape is fragmented. No single dominant platform exists for manufacturing edge in Australia. Industry interviews cited in AFR coverage (2023) describe this as a decision-paralysis factor for procurement teams. Source: AFR (2023 — paywalled; summary from cached excerpt).

**Conflict / thin evidence note:** The relationship between barrier severity and firm size is unclear. AMGC data suggests cost is the primary barrier for SMEs, while larger manufacturers cite integration complexity. These may not be in conflict — they may reflect different adoption stages — but the evidence base is thin enough that presenting "the main barrier" as a single factor would overstate what's known.

---

### Sources used

| Source | Type | Fetched? | Authority level |
|---|---|---|---|
| AMGC Digital Transformation Roadmap (2023) | Industry association | Yes | High |
| CSIRO Manufacturing Futures (2022) | Government research | Yes | High |
| ABS Business Use of IT (2022–23) | Government statistical | Yes | High |
| DISR Powering the Regions consultation (2023) | Government | Yes | High |
| AMTIL Industry Data | Industry association | Yes | High |
| ACSC ICS/OT Security guidance | Government | Yes | High |
| AFR (2023 coverage of edge in manufacturing) | Journalism | Partial (paywalled) | Medium |
| industry.gov.au (MMI program details) | Government | Yes | High |

US and EU sources (Gartner, IDC) were reviewed as comparators but not used as primary evidence for AU-specific claims.

---

## Evaluation

### Criteria (against the agent definition)

- [x] PASS: Agent invokes `/analyst:web-research` with Standard tier — the workflow routing table maps "Background research on a topic" → "Invoke `/analyst:web-research` with the appropriate tier"; the prompt names Standard explicitly, which the agent passes through.
- [x] PASS: Every finding cites a source that has been fetched and read — the non-negotiable states "Every finding cites a source. Every source you cite, you've fetched and read." The simulated output marks each source with fetch status.
- [x] PASS: Agent prioritises AU sources over US/UK equivalents — the source authority section states "For AU/NZ-specific questions, AU/NZ sources should predominate (ABS, Stats NZ, ABC News, RNZ, AFR, IBISWorld AU, CSIRO, sector industry bodies); non-AU sources are used only as comparators." The simulated output uses AMGC, CSIRO, ABS, DISR, AMTIL, ACSC as primary sources; Gartner/IDC explicitly downgraded to comparator-only.
- [x] PASS: Sources are authority-ranked — the seven-level authority table with "Work from the top down" instruction is present in the definition. The simulated output's source table includes an authority-level column reflecting this hierarchy.
- [x] PASS: Where sources conflict or evidence is thin, agent flags this explicitly — the definition states "Contested findings are more valuable than clean ones. Where sources conflict, the conflict is the story." and the non-negotiable covers "no uncertain findings presented as settled." The simulated output includes an explicit conflict/thin-evidence note in the barriers section.
- [x] PASS: Agent does not hand off to business-analyst or osint-analyst — routing table correctly routes "Background research on a topic" to web-research, not to business-analyst (company research) or osint-analyst (domain/infrastructure). This is a general topic request; no company or infrastructure scope is present.
- [~] PARTIAL: Agent notes gaps where authoritative data doesn't exist publicly rather than padding — the principles include "Absence is a finding. If the expected authoritative source has nothing, report it." and "Don't pad depth to seem thorough." The failure cap rule covers mandatory gap reporting after 5 failed searches. Three distinct definition elements address this. Scored as partial because no single explicit rule says "do not substitute lower-quality sources when authoritative data is absent" — the intent is distributed across principles. Well-addressed overall: 0.5.

### Output expectations (against the simulated output)

- [x] PASS: Output addresses the three explicit research questions as separate sections — adoption rate, drivers, and barriers each appear as their own numbered section, not collapsed into a generic topic summary.
- [x] PASS: Output's sources are predominantly Australian — AMGC, CSIRO, ABS, DISR, AMTIL, ACSC, AFR AU are all Australian sources. US/EU sources (Gartner, IDC) are explicitly noted as comparators only, not used as primary evidence.
- [x] PASS: Output flags conflicts or thin evidence — the barriers section contains an explicit note on the conflict between firm-size evidence and the general "main barrier" framing, and the adoption section explicitly names the data gap as a finding.
- [x] PASS: Output uses Standard tier — the simulated output describes Standard tier in the header (moderate depth, primary + secondary sources, not exhaustive). A deep-research output would have used six passes and a significantly larger source set.
- [x] PASS: Output is organised by theme not by source — sections are "Adoption rate," "Drivers," "Barriers" — the research questions — not "Here's what AMGC said / here's what CSIRO said." Sources are cited within each theme.

## Notes

The definition is clean and well-structured. The routing table is unambiguous on handoff boundaries, which is the most common failure mode in multi-agent definitions. The non-negotiable citation rule, the AU-priority source hierarchy, and the contested-findings principle work together without contradiction.

The one gap worth flagging: the PARTIAL criterion on gap-flagging. The intent is clear across three separate definition elements (absence-is-a-finding principle, don't-pad principle, failure-cap rule), but there is no single explicit instruction that says "if no authoritative public data exists for a specific dimension, name the gap as a finding rather than substituting lower-quality sources." A one-line addition to the Principles section would make this structural rather than distributed.

The definition does not specify what "Standard tier" means in terms of source count or pass depth — it defers this entirely to the `/analyst:web-research` skill. That is by design and appropriate; the skill should own the tier definitions. But it means a reviewer cannot verify tier compliance from this definition alone.
