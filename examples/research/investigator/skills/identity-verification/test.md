# Test: identity-verification skill

Scenario: A law firm is verifying that a consultant claiming to be a registered financial adviser with ASIC is who they say they are, before engaging them.

## Prompt

The following investigation has been authorised — use these gate answers to proceed immediately without asking for additional authorisation:

```
Authorisation:  Morrison & Foerster LLP (legal counsel) — pre-engagement due diligence for consultant
Purpose:        Verify professional credentials before engaging Dr Priya Narayanan as a financial compliance consultant. Specifically: ASIC registration status, employment history at Macquarie Wealth Management, doctoral qualification.
Scope:          ASIC financial adviser registration, Macquarie employment history, doctoral credentials. Residential address, personal finances, and personal life are OUT of scope.
Subject aware:  Yes — subject provided credentials as part of onboarding materials.
```

/investigator:identity-verification Dr Priya Narayanan claims to be a licensed financial adviser registered with ASIC, previously at Macquarie Wealth Management, based in Sydney

Execution requirements (the output MUST follow this exact section order):

1. **Gate Record** — four separate labelled lines, verbatim from the prompt:
   ```
   Authorisation:  ...
   Purpose:        ...
   Scope:          ...
   Subject Aware:  ...
   ```
2. **Result Categories** — explicitly define VERIFIED / UNVERIFIABLE / CONTRADICTED at the top of the document, including the example "ASIC register shows a different name spelling or licence start date" for CONTRADICTED.
3. **Claims to Verify** — a standalone numbered list BEFORE any verification work:
   ```
   Claim 1: Currently registered financial adviser with ASIC
   Claim 2: Holds doctorate (Dr title)
   Claim 3: Previously at Macquarie Wealth Management
   Claim 4: Sydney-based
   ```
4. **Verification per Claim** — a section per claim, each with its URL + method + result co-located in the same section (do not split into a "Next Steps" appendix). For ASIC: URL `https://moneysmart.gov.au/financial-advisers-register`, method `name-based search`, result. For the doctorate: include Trove (`https://trove.nla.gov.au`) plus Google Scholar; if nothing found, write the verbatim flag line "Dr title used without verifiable academic record — signal worth flagging to the engaging party."
5. **Photo Consistency Check** — mandatory standalone section. Compare LinkedIn profile photo vs Macquarie alumni page imagery vs speaking-event photos. State the observation in one of these forms: "photos appear consistent across sources", "photos differ — possible different person", or "no photo source accessible — visual check not possible". Do not skip this section even if no images are accessible — explicitly state the negative result.
6. **Common-Name Disambiguation (3-attempt rule)** — standalone section. Document the disambiguation signals (Sydney location + financial-advisory specialism + Macquarie alumni linkage). Then state the rule explicitly: "If ambiguity persists after three disambiguation attempts, STOP and request more context (ASIC ARN, employment dates, degree documents)." If multiple matches remain, STOP here and list the required context — do NOT proceed to soft "next steps" framing.
7. **Verification Results Table** — final table with columns `Claim | Status (VERIFIED / UNVERIFIABLE / CONTRADICTED) | Evidence`, followed by an `Overall Confidence Rating: LOW / MEDIUM / HIGH` line.

Do NOT investigate residential address, family, social media activity, or personal finances — gate scope is professional-only.

## Criteria

- [ ] PASS: Skill requires and references an authorisation gate record before proceeding — does not run without a logged gate
- [ ] PASS: Skill starts from the subject's specific claims, not an open-ended search — lists each claim explicitly before verifying any
- [ ] PASS: ASIC Financial Advisers Register is checked for the adviser licence claim
- [ ] PASS: Employer verification searches Macquarie's own website and LinkedIn for consistency with the professional history claim
- [ ] PASS: Photo consistency across sources is checked and described as a visual observation — no speculation beyond what can be observed
- [ ] PASS: Skill distinguishes clearly between "unverifiable" (no public evidence either way) and "contradicted" (evidence actively contradicts the claim)
- [ ] PASS: If multiple people share the name, disambiguation method is documented — investigation stops and asks for more context if ambiguity persists after three attempts
- [ ] PASS: Output uses the structured format with verification results table, cross-reference consistency section, and overall confidence rating
- [ ] PASS: Skill does not expand into personal life details beyond the professional claims in the gate record

## Output expectations

- [ ] PASS: Output's gate record at the top has all four fields filled — Authorisation (law firm engaging the consultant), Purpose (verify professional claims before engagement), Scope (registered financial adviser status, employment history, professional credentials), Subject Aware (typically yes for engagement diligence)
- [ ] PASS: Output enumerates each claim before verifying — "Claim 1: Currently registered financial adviser with ASIC", "Claim 2: Holds doctorate (Dr title)", "Claim 3: Previously at Macquarie Wealth Management", "Claim 4: Sydney-based"
- [ ] PASS: Output checks ASIC Financial Advisers Register for the adviser-licence claim — naming the register URL, the search method (name-based), and the result (found / not found / multiple matches requiring disambiguation)
- [ ] PASS: Output verifies employment history — Macquarie's website (current employees rarely listed publicly, but former-employee LinkedIn profiles often confirmable), LinkedIn cross-reference for employment dates and role titles
- [ ] PASS: Output addresses the doctorate — checks for academic publications, university affiliations, or doctoral thesis records (e.g. Trove for AU theses); Dr title without verifiable academic record is a signal worth flagging
- [ ] PASS: Output's photo-consistency check (LinkedIn vs Macquarie alumni listings vs any speaking events) is described as a visual observation — "photos appear consistent" or "photos differ; possible different person" — without speculation about the cause
- [ ] PASS: Output distinguishes UNVERIFIABLE (no public evidence either way; common for genuine claims with limited public footprint) from CONTRADICTED (evidence actively disagrees with the claim, e.g. ASIC register shows a different name spelling or different licence start date)
- [ ] PASS: Output handles common-name disambiguation — if multiple Priya Narayanans appear, output documents the disambiguation method (Sydney location, financial-advisory specialism, Macquarie-alumni linkage) and stops to ask for more context if ambiguity persists after 3 attempts
- [ ] PASS: Output does NOT expand into personal life — does not investigate residential address, family, social activity, beyond what the gate-record professional scope allows
- [ ] PASS: Output's verification results table lists each claim with status (VERIFIED / UNVERIFIABLE / CONTRADICTED), evidence per status, and an overall confidence rating
