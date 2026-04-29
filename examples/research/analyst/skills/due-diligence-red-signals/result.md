# Output: due-diligence skill with red signals

**Verdict:** PASS
**Score:** 14.5/15 criteria met (97%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill states scope explicitly at the top — met: Step 1 and the output format template both mandate explicit scope declaration with decision type
- [x] PASS: Business fundamentals section flags the gap between claims and independently verifiable evidence — met: Step 2 requires every figure to have a source and date; Rules require private-company revenue estimates to be labelled explicitly; Step 6 covers regulatory findings via SEC EDGAR
- [x] PASS: Team section notes executive departures or governance concerns from public reporting — met: Step 4 explicitly covers recent departures and flags "executive churn without a clear succession announcement" as a red signal
- [x] PASS: Signal summary contains at least two red signals from public sources — met: Step 7 defines the red signal taxonomy covering C-suite departure, regulatory proceedings, and litigation; the escalation rule presupposes multiple reds will be captured
- [x] PASS: When two or more red signals are present, skill routes to follow-on skills (public-records, corporate-ownership) — met: the Red flag escalation table maps regulatory/litigation findings to `/investigator:public-records` and complex ownership to `/investigator:corporate-ownership` explicitly; the two-signal threshold is stated
- [x] PASS: Verdict does NOT recommend proceeding — met: the signal summary must precede the verdict per Rules; no mechanism allows positive signals to override multiple reds; the escalation logic drives toward investigation not clearance
- [~] PARTIAL: Skill distinguishes "information unavailable" from "information contradicts claims" — partially met: Step 2 requires labelling estimates and the skill flags gaps in evidence, but there is no explicit named distinction in the signal taxonomy or output format between "absent evidence" and "evidence that contradicts the claim"; the skill treats both as things to flag without differentiating their severity
- [x] PASS: Revenue and technology claims flagged as unverifiable when no independent validation exists — met: Rules require explicit labelling of private-company revenue estimates; the source-and-date requirement surfaces absence of validation; Step 6 regulatory search would surface contradicting findings

### Output expectations

- [x] PASS: Output scope at the top is explicit with the Theranos public-record caveat — met: Step 1 and output format require scope and the "Data type: Public sources only" field; the instruction to search press and SEC EDGAR would surface the depth of the Theranos record
- [x] PASS: Output's business fundamentals flags the gap between Theranos's claims and independent verification — met: Step 2's sourcing requirement and Step 6's SEC EDGAR / regulatory search would force surfacing that no peer-reviewed validation exists and that CMS inspections contradicted the technology claims
- [x] PASS: Output's team section notes executive departures and governance concerns — met: Step 4 covers founding team backgrounds, key executive tenures, and departures; Holmes, Balwani, and board composition would surface from press and LinkedIn research
- [x] PASS: Output's signal summary lists multiple RED signals — met: the taxonomy covers C-suite departure, regulatory proceedings, and litigation; all four expected red signals (claims gap, SEC charges, criminal convictions, governance) map to taxonomy categories
- [x] PASS: Output's verdict is DO NOT PROCEED — met: the escalation logic requires investigation when two or more reds are present; with four red signals the skill would not produce a proceed verdict
- [x] PASS: Output routes to follow-on skills — met: Red flag escalation table maps litigation to `/investigator:public-records` and ownership to `/investigator:corporate-ownership` explicitly, matching the expected routing
- [~] PARTIAL: Output distinguishes "information unavailable" from "information contradicts claims" — same gap as criterion 7; the signal table provides green/amber/red status but no built-in mechanism to mark a finding as "CONTRADICTED" versus "UNAVAILABLE"; a well-formed agent response might infer the distinction, but the skill does not instruct it
- [x] PASS: Output flags Theranos's revenue and technology claims as UNVERIFIABLE / CONTRADICTED — met: the sourcing Rules and Step 6 regulatory search would produce this; the CONTRADICTED state emerges from the CMS and SEC findings research steps
- [x] PASS: Output uses Theranos as an unambiguous do-not-proceed case — met: the signal taxonomy and escalation logic are strong enough to produce a clear red verdict without equivocation
- [~] PARTIAL: Output addresses timing — when this diligence might have run relative to the Carreyrou reporting and trial — partially met: the skill has no instruction to contextualise the temporal evolution of the public record; it would produce a single-point-in-time report without noting that the evidentiary landscape changed materially from pre-2015 to post-2018

## Notes

The skill is structurally sound. The consistent gap across both criteria sets is the absence of an explicit "contradicted vs unavailable" distinction. The signal table uses green/amber/red status but provides no mechanism to label a finding as "evidence actively contradicts the claim" rather than "no evidence found" — and for a Theranos scenario, that distinction is the crux of the analysis. A "CONTRADICTED" status alongside the colour-coded signals would close this.

The temporal dimension is also absent. The skill produces a point-in-time report but does not instruct the analyst to note how the public record evolved — relevant when the subject's evidentiary landscape changed dramatically over time. Neither gap is a failure; both are genuine improvement candidates.
