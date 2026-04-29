# Result: open-source-researcher — topic research

**Verdict:** PARTIAL
**Score:** 12.5/17 criteria met (73.5%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Agent invokes `/analyst:web-research` with Standard tier — met: routing table maps "Background research on a topic" to "Invoke `/analyst:web-research` with the appropriate tier"; prompt explicitly names Standard tier; agent follows this path
- [~] PARTIAL: Every finding cites a source that has been fetched and read — partially met: non-negotiable states "Every finding cites a source. Every source you cite, you've fetched and read." The principle is explicit; no structural enforcement mechanism guarantees it holds under execution, but intent is clearly stated
- [x] PASS: Agent prioritises AU sources for AU-specific question — met: source authority table explicitly states "For AU/NZ topics, use ABS, Stats NZ, ABC News, RNZ as primary sources before defaulting to US/UK equivalents"
- [x] PASS: Sources are authority-ranked — met: full authority hierarchy table present; government/regulatory at top, community/opinion at bottom
- [x] PASS: Where evidence is thin or contested, agent flags explicitly — met: "Contested findings are more valuable than clean ones. Where sources conflict, the conflict is the story." and "Absence is a finding." directly address this
- [x] PASS: Agent does not hand off to business-analyst or osint-analyst for this request — met: routing table is unambiguous — "Background research on a topic" stays in-agent; company and infrastructure route out; this is a general topic request
- [~] PARTIAL: Agent notes gaps rather than padding with lower-quality sources — partially met: "Don't pad depth to seem thorough" and "Absence is a finding" are present; no explicit instruction to name the gap instead of filling with lower-quality sources, so judgement-dependent
- [x] PASS: Output organised by theme, not by source — met: "structured research" framing and the principle of organising by theme implied throughout; no instruction to list findings by source

### Output expectations

- [ ] FAIL: Output addresses three explicit research questions as distinct sections — not found: the agent definition contains no output structure instructions guaranteeing three labelled sections matching the prompt's explicit questions (adoption rate, drivers, barriers)
- [ ] FAIL: Output's sources are predominantly Australian — not found: authority table lists AU sources and says to prefer them, but does not specify AU sources must dominate output; "before defaulting to US/UK equivalents" is weaker than "predominantly AU"
- [~] PARTIAL: Output's authority ranking is shown in the output — partially met: agent applies authority ranking internally but no instruction to surface the ranking visibly in the output (e.g. labelling vendor content, flagging authority level per citation)
- [ ] FAIL: Adoption-rate finding includes data source, year, and sample base — not found: non-negotiable requires citing sources but does not require year and sample base metadata; this level of citation detail is not specified in the definition
- [ ] FAIL: Drivers section names specific drivers with evidence — not found: agent definition is domain-agnostic; no instruction to cover domain-specific drivers (latency, connectivity, data residency, egress cost); a well-run agent might produce this but the definition does not ensure it
- [ ] FAIL: Barriers section names specific barriers — not found: same gap; no domain knowledge of barriers baked in; definition would not reliably surface OT integration, capex, or skills-gap specifics
- [ ] FAIL: Output flags conflicts with methodology explanation — not found: "conflict is the story" is present, but definition does not instruct the agent to explain methodology differences when sources disagree on numbers; it would flag conflict without necessarily explaining why figures differ
- [x] PASS: Output uses Standard tier — met: routing explicitly invokes `/analyst:web-research` with tier matching the request; agent passes Standard through
- [x] PASS: Output organised by theme — met: same as Criteria item; structural research output expectation satisfied by agent definition
- [~] PARTIAL: Output identifies named Australian manufacturing examples — partially met: no instruction to include named examples; the sourcing principles might lead there but it is not guaranteed

## Notes

The agent definition is well-structured for routing, source authority, and research discipline. The core behavioural principles — cite everything you fetch, flag contested findings, don't pad — are solid and clearly stated.

The significant gap is output specification. The definition tells the agent how to research but not how to structure the output for this question type. The Output expectations criteria are materially harder to meet because they test output shape (three labelled sections, citation metadata with year and sample base, methodology notes when sources conflict), none of which are specified in the definition. A capable agent running this definition would likely produce good research, but the definition alone does not guarantee the required output structure.

The AU-priority instruction is present but could be stronger. "Use ABS before US/UK equivalents" is a preference order; "output must be predominantly AU-sourced for AU questions" is a constraint. The current wording does not prevent heavy use of non-AU sources if AU ones are thin.
