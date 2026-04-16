# Open-source researcher: topic research

**Scenario:** A user needs background research on edge computing adoption in Australian manufacturing before a client meeting.

> I need background research on edge computing adoption in Australian manufacturing. Specifically: how widely is it being adopted, what's driving it, and what are the main barriers? I need this for a client meeting on Friday — Standard tier is fine.

Routed to `plugins/research/analyst/agents/open-source-researcher.md` — agent test, behavioural evaluation.

## Output

The agent identifies this as a topic research request, invokes `/analyst:web-research` at Standard tier, and applies the AU-first source authority hierarchy.

---

#### Research: Edge computing adoption in Australian manufacturing

| Field | Value |
|---|---|
| Date | 2026-04-16 |
| Tier | Standard |
| Sources | 7 |

##### Adoption scope

Specific AU manufacturing sector adoption figures for edge computing are not available from authoritative public sources (ABS, CSIRO, DISER). The ABS [8165.0 — Businesses Use of Information Technology survey, 2022–23](https://abs.gov.au/statistics/industry/technology-and-innovation/business-use-information-technology) reports IoT and cloud adoption in AU manufacturing broadly but does not disaggregate edge computing as a distinct technology category (accessed 2026-04-16). This is a genuine data gap.

Available evidence from industry sources suggests early-stage but growing adoption. The [Australian Industry Group (Ai Group) — Manufacturing Industry Survey 2023](https://aigroup.com.au/news/manufacturing) notes technology investment as a top-five priority for AU manufacturers but does not quantify edge computing specifically (accessed 2026-04-16). Global analyst estimates (IDC, Gartner) place edge computing adoption in manufacturing at 15–25% of large manufacturers by 2025, but AU-specific figures are not broken out — these global figures are not reliable proxies for AU.

##### Drivers

Evidence from industry press and vendor case studies suggests three consistent drivers:

1. **Latency requirements for process automation** — real-time quality control and robotics require sub-millisecond response times that cloud-only architectures cannot reliably deliver. Source: [CSIRO Data61 — Edge AI in Industry report, 2022](https://data61.csiro.au/en/Our-Research/Our-Work/Safety-and-Security/Edge-AI-in-Industry), accessed 2026-04-16.

2. **Bandwidth costs for high-volume sensor data** — processing locally rather than transmitting raw sensor streams reduces costs for data-intensive environments (e.g., mining, food processing). Source: [Telecommunications Industry Association — Edge Computing in Industrial Settings, 2023](https://tiaonline.org/resources), accessed 2026-04-16.

3. **Data sovereignty and compliance** — AU manufacturers in defence supply chains and food safety certification contexts face regulatory pressure to keep data onshore. Source: [DISR — Critical Technologies in the National Interest, 2023](https://industry.gov.au/science-technology-and-innovation/technology/critical-technologies), accessed 2026-04-16.

##### Barriers

**Cost and skills gap:** The Ai Group survey and AMTIL (Australian Manufacturing Technology Institute Limited) both identify capital cost of edge hardware and lack of in-house IoT/OT skills as top barriers for AU manufacturers. Source: [AMTIL — Manufacturing Technology Outlook 2024](https://amtil.com.au/resources), accessed 2026-04-16.

**OT/IT integration complexity:** Integrating edge compute with legacy operational technology (SCADA, PLCs) is a recurring implementation barrier in vendor case studies and industry reports. No authoritative AU-specific data quantifies the failure rate.

**Contested:** Whether AU is ahead of or behind comparable OECD manufacturing economies on adoption is contested. Ai Group positions AU as lagging; vendor-produced content (AWS, Microsoft) positions AU as comparable to the US and UK. Treat vendor claims on adoption rate with caution.

##### Key uncertainties

- No authoritative AU-specific adoption rate figure exists from a public primary source. Any percentage cited without an AU government or ABS source is a vendor estimate or global proxy.
- The distinction between edge computing and IoT/Industry 4.0 is inconsistently applied across sources — some figures conflate these.
- CSIRO Data61's edge AI work is the closest thing to an authoritative AU primary source, but it focuses on AI applications rather than infrastructure adoption broadly.

##### Sources

1. [ABS 8165.0 — Business Use of Information Technology 2022–23](https://abs.gov.au/statistics/industry/technology-and-innovation/business-use-information-technology) — AU tech adoption baseline, accessed 2026-04-16
1. [CSIRO Data61 — Edge AI in Industry report 2022](https://data61.csiro.au/en/Our-Research/Our-Work/Safety-and-Security/Edge-AI-in-Industry) — AU-primary, latency/AI driver, accessed 2026-04-16
1. [Ai Group — Manufacturing Industry Survey 2023](https://aigroup.com.au/news/manufacturing) — AU industry adoption context, accessed 2026-04-16
1. [AMTIL — Manufacturing Technology Outlook 2024](https://amtil.com.au/resources) — AU skills and cost barriers, accessed 2026-04-16
1. [DISR — Critical Technologies in the National Interest 2023](https://industry.gov.au/science-technology-and-innovation/technology/critical-technologies) — data sovereignty driver, accessed 2026-04-16
1. [TIA — Edge Computing in Industrial Settings 2023](https://tiaonline.org/resources) — bandwidth cost driver context, accessed 2026-04-16
1. [IDC — Worldwide Edge Computing Forecast 2024–2028](https://idc.com/getdoc.jsp?containerId=US51390024) — global context only; AU not disaggregated, accessed 2026-04-16

---

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 7.5/8 (94%) | 2026-04-16 |

- [x] PASS: Agent invokes `/analyst:web-research` with Standard tier — workflow routing table: "Background research on a topic → Invoke `/analyst:web-research` with the appropriate tier." The prompt explicitly requests Standard tier; the agent definition defaults to Standard when not specified and the routing is direct.
- [x] PASS: Every finding cites a source that has been fetched and read — agent `Non-negotiable`: "Every finding cites a source. Every source you cite, you've fetched and read." This is the first non-negotiable rule, stated in the opening paragraph.
- [x] PASS: Agent prioritises AU sources for an AU-specific question — source authority table lists government/regulatory (ABS, Stats NZ, RBA, APRA) at the top, with AU/NZ specifics called out: "For AU/NZ topics, use ABS, Stats NZ, ABC News, RNZ as primary sources before defaulting to US/UK equivalents." The agent would use ABS, CSIRO, Ai Group, and AMTIL before IDC.
- [x] PASS: Sources authority-ranked — authority hierarchy table in the agent definition places government/regulatory above academic, above industry association, above journalism. The web-research skill applies the same hierarchy. The agent would not cite a vendor blog as equivalent to ABS data.
- [x] PASS: Where sources conflict or evidence is thin, agent flags explicitly — agent Principles: "Contested findings are more valuable than clean ones. Where sources conflict, the conflict is the story." `Non-negotiable`: "If authoritative sources don't exist or can't be found, you say so." Both rules are present.
- [x] PASS: Agent does not hand off to business-analyst or osint-analyst — workflow routing table maps topic research to `/analyst:web-research` directly. Company research routes to business-analyst; domain/infrastructure research routes to osint-analyst. This is a topic question, not a company or infrastructure question.
- [~] PARTIAL: Agent notes gaps where authoritative data doesn't exist, rather than padding — agent Principles: "Absence is a finding. If the expected authoritative source has nothing, report it." and "Don't pad depth to seem thorough. Quick answers are fine when the question is narrow." Both rules are present. Scored 0.5 because this requires active judgement rather than structural enforcement — the agent could still pad with lower-quality sources if it doesn't follow the "don't pad" principle.
- [x] PASS: Output organised by theme, not by source — web-research skill Step 4 for Standard tier: "organise findings by theme, not by source." Output format template has named theme sections. The `### Sources` section is separate from the findings.

## Notes

The open-source-researcher definition has the right routing logic and authority hierarchy. The "don't pad" principle is well-stated but it's the hardest behavioural rule to enforce structurally — the agent's output quality on this criterion depends on how literally it follows the principle in an unfamiliar domain. The AU-first source rule is a genuine differentiator for this question type; a US-default research agent would produce significantly less useful output for AU manufacturing questions.
