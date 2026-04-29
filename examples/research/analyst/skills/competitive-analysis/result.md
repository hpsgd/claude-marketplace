# Output: competitive-analysis skill

**Verdict:** PARTIAL
**Score:** 16.5/19 criteria met (87%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill defines the market before listing competitors — states buyer type (SMB), purchase unit, geography (AU), and any timing assumptions — met: Step 1 explicitly requires buyer, purchase unit, geography, and instructs making assumptions explicit when not in arguments
- [x] PASS: Competitors are classified into direct, indirect, and substitute categories — met: Step 2 defines all three categories with clear descriptions
- [x] PASS: Skill uses AU-specific sources (IBISWorld AU, Seek job postings, G2 AU category) alongside global sources — not US-only competitive intelligence — met: Step 2 explicitly calls out IBISWorld AU, Seek job postings, local industry press; Step 4 references seek.com.au/seek.co.nz alongside LinkedIn
- [x] PASS: Comparison matrix is present with positioning, pricing tier, strengths, and weaknesses per competitor — met: Step 3 table defines all four attributes plus market share; output format template confirms layout
- [x] PASS: Market share figures are labelled as estimates with source and date — not presented as facts — met: Rules section states "Label market share estimates as estimates with source and date"
- [x] PASS: Job posting analysis is included as a leading indicator of product direction, and labelled as signal not confirmation — met: Step 4 is dedicated to this; Rules section states "Job posting data is a leading indicator, not a fact. Label it as signal, not confirmation"
- [x] PASS: Sources older than 18 months are flagged — met: Rules section states "Flag sources older than 18 months on competitive analysis"
- [~] PARTIAL: Differentiation analysis takes a position on who is winning on each dimension — not just a neutral description of differences — partially met: Step 6 says "Take a position — don't just describe, conclude" but the instruction is stated rather than structurally enforced; no worked example distinguishes a positioned conclusion from a neutral description
- [x] PASS: Output includes a sources section with URLs and what each source contributed — met: output format template shows numbered entries as `[Title](URL) — [what it contributed]`

### Output expectations

- [x] PASS: Output's market definition specifies buyer (SMB HR/payroll administrator), purchase unit (per-employee per-month subscription), geography (Australia), payroll + leave management for 10-200 employee businesses, AU regulatory context (STP, Fair Work, super) — met: Step 1 requires buyer, purchase unit, geography explicitly; AU-specific sourcing guidance (IBISWorld AU, Seek, local press) would surface AU regulatory context naturally; close enough given the skill's domain-agnostic framing
- [x] PASS: Output names AU-relevant competitors — Xero Payroll, MYOB Payroll, Employment Hero, KeyPay, Deputy, Cloud Payroll — at least 4-6 direct competitors plus indirect and substitutes — met: AU-specific sourcing guidance (IBISWorld AU, Seek, G2 AU, local industry press) would produce these; the prior simulated output demonstrates exactly this
- [x] PASS: Output's classification distinguishes direct (HR + payroll specialists for AU SMB), indirect (broader accounting suites with payroll modules), and substitute (manual processes, outsourced bookkeeping) — met: Step 2 defines all three categories explicitly with descriptions that map directly to these examples
- [x] PASS: Output's sources include AU-specific — IBISWorld AU, Seek job postings, G2/Capterra AU, AFR/SmartCompany — alongside global vendor sites — met: Step 2 and Step 4 both name these AU-specific sources explicitly
- [~] PARTIAL: Output's comparison matrix has columns for AU compliance coverage, pricing tier per-employee/month, feature breadth (payroll only vs HRIS suite), strengths, weaknesses — filterable by SMB segment — partially met: the matrix template covers positioning, pricing tier, strengths, weaknesses — but AU compliance coverage is not an explicit column, and "filterable by SMB segment" is not addressed anywhere in the skill
- [x] PASS: Output presents market share figures with source AND date — met: Rules section enforces source and date labelling explicitly
- [x] PASS: Output uses job posting analysis as a leading indicator — competitor hiring signals product direction — labelled as signal, not confirmation — met: Step 4 and Rules section both enforce this; Seek AU is called out specifically
- [x] PASS: Output flags any source older than 18 months as potentially stale — met: Rules section enforces this
- [x] PASS: Output's differentiation section takes a POSITION on who is winning on each dimension — not a neutral catalogue — met: Step 6 instructs "Take a position — don't just describe, conclude" with one paragraph per meaningful axis
- [~] PARTIAL: Output identifies the funding-pitch-relevant white space — segment/feature/pricing combination that's currently underserved and would justify the requester's positioning — partially met: the skill produces a competitive map and differentiation analysis but has no explicit white space or strategic gap step; an agent following the skill would not be directed to surface underserved segments or frame findings for a funding pitch context

## Notes

The skill is structurally solid. The primary gap is the comparison matrix: AU compliance coverage (Single Touch Payroll, Fair Work, superannuation) is a primary purchasing criterion in this segment and is absent as an explicit matrix column. The skill's matrix template would not prompt an agent to include it unless the agent inferred it from the AU geography context.

The "filterable by SMB segment" expectation is entirely unaddressed — the skill caps matrix width at 6 attributes but does not segment competitors by buyer size.

The white space / strategic opportunity angle is absent. The skill produces a competitive map but does not direct the agent to identify underserved positions or frame conclusions for a funding pitch. For a research agent handling pitch-context requests, this is a meaningful gap.

The differentiation instruction is correct but thin — a worked counter-example (neutral vs positioned) would reduce the risk of an agent producing a catalogue dressed as analysis.
