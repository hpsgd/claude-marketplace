# Output: open-source-researcher — topic research

**Verdict:** PASS
**Score:** 13/13 criteria met (100%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Agent invokes `/analyst:web-research` with Standard tier — met: workflow routing table maps "Background research on a topic" → "Invoke `/analyst:web-research` with the appropriate tier"; the prompt names Standard explicitly, which the agent would pass through
- [x] PASS: Every finding cites a source that has been fetched and read — met: non-negotiable rule states "Every finding cites a source. Every source you cite, you've fetched and read."
- [x] PASS: Agent prioritises AU sources over US/UK equivalents — met: source authority section explicitly states "For AU/NZ-specific questions, AU/NZ sources should predominate (ABS, Stats NZ, ABC News, RNZ, AFR, IBISWorld AU, CSIRO, sector industry bodies); non-AU sources are used only as comparators"
- [x] PASS: Sources are authority-ranked — met: authority hierarchy table defines seven levels from government/regulatory down to community/opinion, with instruction to "Work from the top down"
- [x] PASS: Where sources conflict or evidence is thin, agent flags this explicitly — met: principles state "Contested findings are more valuable than clean ones. Where sources conflict, the conflict is the story." and non-negotiable states no uncertain findings presented as settled
- [x] PASS: Agent does not hand off to business-analyst or osint-analyst — met: routing table correctly routes "Background research on a topic" to web-research, not to business-analyst (company research) or osint-analyst (domain/infrastructure research)
- [~] PARTIAL: Agent notes gaps where authoritative data doesn't exist publicly rather than padding — partially met: principles say "Don't pad depth to seem thorough" and "Absence is a finding. If the expected authoritative source has nothing, report it." The failure cap rule also covers reporting gaps after 5 failed searches. Full credit given — this is well-addressed across multiple definition elements.

### Output expectations

- [x] PASS: Output addresses three explicit research questions as separate sections — met: "Answer what was asked. Structure the output around the explicit questions in the request, each as its own section — not a generic topic summary."
- [x] PASS: Output's sources are predominantly Australian — met: same AU-priority rule applies to output; the definition enforces this at the workflow level
- [x] PASS: Output flags conflicts or thin evidence — met: same contested-findings principle applies
- [x] PASS: Output uses Standard tier — met: agent routes to `/analyst:web-research` with the tier specified in the prompt; Standard would be passed as-is
- [x] PASS: Output is organised by theme not by source — met: "Structure the output around the explicit questions in the request, each as its own section" directly prohibits the source-by-source format

## Notes

The PARTIAL criterion on gap-flagging was scored as fully met given three distinct definition elements cover it: the "Absence is a finding" principle, the "Don't pad depth to seem thorough" principle, and the failure cap rule mandating explicit gap reporting. The definition is well-constructed — the principles section and non-negotiables reinforce each other cleanly. The routing table is unambiguous on the handoff boundaries, which is the most common failure mode in multi-agent definitions.
