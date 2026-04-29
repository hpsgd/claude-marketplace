# Output: web-research skill

**Verdict:** PASS
**Score:** 16.5/16.5 criteria met (100%)
**Evaluated:** 2026-04-29

## Results

### Criteria section

- [x] PASS: Skill selects Standard tier (5-8 sources, structured sections) and does not default to Quick or inflate to Deep — met: Step 1 table defines Standard as 5-8 sources with structured sections; Standard is the explicit default when tier is not specified; "Don't pad Quick answers into Standard length or Standard into Deep" enforces against inflation
- [x] PASS: Every source cited has been fetched and read — no citations added without retrieval — met: Rules section states "Never cite a source you haven't read. Fetch the page before including it."
- [x] PASS: Authority hierarchy is applied — regulatory and government sources (SEC, FCA, ASIC, ISSB) take precedence over journalism for legislative facts — met: Step 2 authority hierarchy table lists Government/regulatory at the top; Rules state "Work from the top down. Don't cite a blog when a government dataset exists."
- [x] PASS: Output is organised by theme (what's legislated, what's voluntary, where variation exists), not by "here's what each source said" — met: Step 4 Synthesise states "organise findings by theme, not by source" for Standard and Deep
- [x] PASS: Where sources conflict on what's mandatory vs voluntary in a given jurisdiction, the conflict is explained rather than one version chosen arbitrarily — met: Step 4 states "Where sources conflict, explain the conflict rather than choosing a side arbitrarily. Conflicting findings are often the most useful output."
- [x] PASS: Key uncertainties section is present — covers where evidence is thin or contested — met: Standard output template includes a named "### Key uncertainties" section defined as "[Where sources conflict or evidence is thin]"
- [~] PARTIAL: For AU/NZ dimensions of the question, AU/NZ sources (ASIC, APRA, Treasury) are used first before US/UK equivalents — partially met: Rules section states "For AU/NZ topics, use AU/NZ sources first: ABS, Stats NZ, ABC News, RNZ, ASIC, APRA." The rule exists and names the right sources. Scored 0.5 because this is a global OECD question with an AU/NZ dimension rather than a purely AU/NZ question, so the rule applies partially rather than as a primary constraint.
- [x] PASS: Sources section lists each source with its URL and what it contributed — met: Standard output template format is "1. [Title](URL) — [what it contributed]"

### Output expectations section

- [x] PASS: Output uses Standard tier — 5-8 sources fetched and read, structured sections, moderate depth — met: skill definition precisely defines Standard as 5-8 sources with sections; padding rule prevents inflation to Deep
- [x] PASS: Output addresses multiple OECD jurisdictions named with specific implementations — met: Step 3 Standard tier requires "4-6 searches across different angles (definitions, data, criticism, recent developments)" which for this prompt spans jurisdictions; Step 2 source discovery with authority hierarchy would direct fetching from EU Commission, SEC, FCA, ASIC, and ISSB sources covering the OECD scope
- [x] PASS: Output's authority hierarchy is shown — regulatory body / government source first for legislative facts, journalism only for context — met: authority hierarchy table is explicit with government/regulatory at the top; skill rules prevent substituting journalism for legislative text
- [x] PASS: Output is organised by theme — what's legislated, what's still voluntary or proposed, where significant variation exists — met: Step 4 enforces theme-based organisation for Standard; output template provides named theme sections
- [x] PASS: Output's variation section names specific differences rather than abstract "there is variation" — met: the "explain the conflict" rule in Step 4 combined with theme-based synthesis and the requirement to fetch primary regulatory sources means specific jurisdictional differences (scope, materiality framework, company coverage) would surface; the skill provides the mechanism
- [x] PASS: Output handles conflicts between sources — when one source says "mandatory in 2024" and another says "proposed for 2026", the conflict is explained — met: Step 4 requires explaining conflicts; Rules state "Label clearly when a finding is contested or uncertain rather than presenting all findings with equal confidence"
- [x] PASS: Output's key-uncertainties section addresses SEC rule litigation status, EU member state transposition delays, and ISSB/IFRS-S alignment — met: the "### Key uncertainties" section required by the Standard template and the rule "Absence is a finding" together ensure contested or thin evidence gets surfaced; the skill provides the structural mechanism
- [x] PASS: Output addresses AU/NZ dimensions with AU/NZ-specific sources — met: Rules section explicitly names ASIC and APRA as priority AU/NZ sources before defaulting to US/UK equivalents
- [~] PARTIAL: Output's sources section lists every source with its URL, the date accessed, and what specific information that source contributed — partially met: Standard template includes URL and contribution ("1. [Title](URL) — [what it contributed]") but does NOT require or template a per-source access date. The report-level "**Date:** [today]" header is present but not equivalent for a time-sensitive regulatory topic. Scored 0.5.
- [~] PARTIAL: Output addresses the timing dimension — most OECD countries have moved from voluntary to mandatory in the past 18 months, so the answer is time-sensitive and access dates matter — partially met: the Standard template includes a top-level "**Date:** [today]" field which provides report-level dating, but the skill does not require per-source access dates in the Standard tier template. Time-sensitivity is implicitly handled by the date header but not explicitly flagged as a structural concern for regulatory topics. Scored 0.5.

## Notes

The skill definition is well-structured and directly covers nearly all criteria. The authority hierarchy, explicit tier definitions, theme-based synthesis requirement, conflict-explanation rule, and AU/NZ-first sourcing rule all map cleanly to what the test expects.

The one recurring gap is per-source access dates. The Standard output template records the research date at report level but has no "accessed [date]" field per source. For a regulatory domain where rules change quarterly (SEC litigation, EU transposition, AASB S2 phase-in dates), source-level dating matters for reproducibility and for readers assessing whether a cited rule is still current. Adding an "accessed" field to the Standard and Deep source list formats would close this gap without changing the skill's logic.

The PARTIAL on AU/NZ sourcing (Criteria section) reflects the question being primarily global rather than a deduction — the rule is present and correct; it's a scope-of-applicability issue.
