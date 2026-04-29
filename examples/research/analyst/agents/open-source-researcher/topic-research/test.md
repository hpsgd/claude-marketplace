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
- [ ] PASS: Output flags conflicts or thin evidence where sources disagree
- [ ] PASS: Output uses Standard tier — moderate depth, fetched primary and secondary sources, but NOT exhaustive deep-research with all six passes; the prompt names Standard explicitly
- [ ] PASS: Output is organised by theme (adoption / drivers / barriers / examples) NOT by source ("AFR said X, ABC said Y") — the structure serves the research question
