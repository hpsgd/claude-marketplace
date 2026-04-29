# Test: open-source-researcher — topic research

Scenario: A user needs background research on edge computing adoption in Australian manufacturing before a client meeting.

## Prompt

I need background research on edge computing adoption in Australian manufacturing. Specifically: how widely is it being adopted, what's driving it, and what are the main barriers? I need this for a client meeting on Friday — Standard tier is fine.

## Criteria

- [ ] PASS: Agent invokes `/analyst:web-research` with Standard tier
- [ ] PASS: Every finding cites a source that has been fetched and read — no uncited assertions
- [ ] PASS: Agent prioritises AU sources (ABS, ABC News, industry associations, AFR) over US or UK equivalents for an AU-specific question
- [ ] PASS: Sources are authority-ranked — government or industry body data takes precedence over blog posts or vendor content
- [ ] PASS: Where sources conflict or evidence is thin, agent flags this explicitly rather than presenting contested findings as settled
- [ ] PASS: Agent does not hand off to business-analyst or osint-analyst — this is a general topic research request, not a company or infrastructure investigation
- [ ] PARTIAL: Agent notes gaps where authoritative data doesn't exist publicly, rather than padding with lower-quality sources to appear thorough
- [ ] PASS: Output is organised by theme, not by "here's what each source said"

## Output expectations

- [ ] PASS: Output addresses the three explicit research questions — adoption rate / how widely, drivers, barriers — each as a section, NOT collapsed into a generic "edge computing in Australian manufacturing" summary
- [ ] PASS: Output's sources are predominantly Australian — AMTIL, AMGC, ABS, AFR, IBISWorld AU, Australian government bodies (DISR), CSIRO — over US / EU sources for an AU-specific question; non-AU sources used only as comparators
- [ ] PASS: Output's authority ranking is shown — government / industry-body data first, then trade press, then vendor content (clearly flagged as vendor-influenced) — and conflicting findings between authority levels are surfaced
- [ ] PASS: Output's adoption-rate finding includes the data source, the year of measurement, and the sample base — not a single percentage without context (e.g. "AMGC 2024 industry survey of 187 manufacturers found 18% with edge deployments in production, 34% piloting")
- [ ] PASS: Output's drivers section names specific drivers with evidence — latency for OT/factory-floor automation, intermittent connectivity at remote sites (mining-adjacent manufacturing), regulatory data residency, cost of cloud egress at scale — each with at least one cited source
- [ ] PASS: Output's barriers section names specific barriers — skills gap (specialist talent shortage), upfront capex, vendor-lock-in concerns, integration with legacy OT — each with cited evidence
- [ ] PASS: Output flags conflicts or thin evidence — e.g. "AMGC reports 18% adoption; vendor-commissioned research claims 35%; the methodology differences explain the gap"
- [ ] PASS: Output uses Standard tier — moderate depth, fetched primary and secondary sources, but NOT exhaustive deep-research with all six passes; the prompt names Standard explicitly
- [ ] PASS: Output is organised by theme (adoption / drivers / barriers / examples) NOT by source ("AFR said X, ABC said Y") — the structure serves the research question
- [ ] PARTIAL: Output identifies named Australian manufacturing examples — companies that have publicly announced edge deployments (e.g. specific automotive, food processing, mining-adjacent firms) — making the abstract trend concrete
