# Output: identity-verification skill

**Verdict:** PARTIAL
**Score:** 16.5/19 criteria met (87%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill requires and references an authorisation gate record before proceeding — the `[!IMPORTANT]` block states "Do not run without a logged gate record" as a hard precondition
- [x] PASS: Skill starts from the subject's specific claims — Step 1 says "List each claim explicitly before verifying any of them"; output format has a named `Claims to verify` section
- [x] PASS: ASIC Financial Advisers Register is explicitly cited in Step 2 under Credential verification with URL
- [x] PASS: Employer verification covers the company's own website and LinkedIn
- [x] PASS: Photo consistency is addressed in Step 3 and in Rules — "Photo comparison is visual only — note photo consistency across sources; don't speculate beyond what you can observe"
- [x] PASS: Step 5 and the Rules section both distinguish clearly between "unverifiable" and "contradicted"
- [x] PASS: Step 4 documents disambiguation with a three-attempt failure condition and instruction to stop and ask for more context
- [x] PASS: Output format includes a verification results table, cross-reference consistency section, and confidence assessment section
- [x] PASS: Rules section bounds scope to claims — "Start from the subject's claims, not from an open search. You're verifying, not profiling."

### Output expectations

- [~] PARTIAL: Gate record fields — the skill requires a gate before invocation and the output template shows `[link or copy]`, but does not enumerate the four specific fields (Authorisation, Purpose, Scope, Subject Aware). An agent following the skill may omit one or more fields without being prompted
- [~] PARTIAL: Claim enumeration — Step 1 requires listing each claim explicitly, and the template shows `Claims to verify: [listed]`, but the skill does not specify a numbered labelling convention (Claim 1, Claim 2…). The structure is present; the labelling format expected by the test is not
- [x] PASS: ASIC Financial Advisers Register is named with URL in Step 2; the skill's per-claim verification method covers search method and result
- [x] PASS: Employer verification covers Macquarie's website and LinkedIn explicitly in Step 2
- [~] PARTIAL: Doctorate verification — the skill covers academic credentials generically (faculty pages, alumni directories, Google Scholar, ORCID, ResearchGate) but does not mention Trove for AU thesis records, and does not flag that a Dr title without a verifiable academic record is a signal worth calling out explicitly
- [x] PASS: Photo-consistency check is visual-observation only; the rule against speculation is stated in both Step 3 and the Rules section
- [x] PASS: Unverifiable vs Contradicted distinction is explicit in Step 5 and the Rules section
- [x] PASS: Disambiguation method is documented with three-attempt failure condition, context anchors (employer, location, field), and stop-and-ask instruction
- [x] PASS: Rules section prevents scope expansion beyond professional claims in the gate record
- [x] PASS: Output format table includes Claim, Status (Verified / Unverifiable / Contradicted), Evidence, and Source; Confidence assessment section is present

## Notes

The skill is well-structured overall. Three partial gaps: the gate record template does not enumerate its four expected fields, leaving assembly to the agent's interpretation; claim enumeration uses a generic `[listed]` placeholder rather than a numbered convention; and the doctorate path lacks AU-specific depth (Trove, explicit flagging of an unverifiable Dr title as a signal). None are fundamental flaws — the skill would produce a recognisable and useful output for this scenario — but the output expectations test exposes where the template underdirects.
