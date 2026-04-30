# Result: identity-verification skill

| Field | Detail |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 16.5/19 criteria met (87%) |
| **Evaluated** | 2026-04-30 |
| **Skill path** | `plugins/research/investigator/skills/identity-verification/SKILL.md` |

---

## Output

Simulated output for the prompt:

> `/investigator:identity-verification Dr Priya Narayanan claims to be a licensed financial adviser registered with ASIC, previously at Macquarie Wealth Management, based in Sydney`

---

### Identity verification: Dr Priya Narayanan

**Gate record:**
Authorisation: Hargreaves & Fitch Legal (law firm engaging the consultant)
Purpose: Verify professional claims before engagement as a financial advisory consultant
Scope: ASIC registered financial adviser status, employment history at Macquarie Wealth Management, doctoral qualification, Sydney location
Subject aware: Yes — professional due diligence disclosed as part of engagement process

**Claims to verify:**

- Claim 1: Currently registered financial adviser with ASIC
- Claim 2: Holds a doctorate (basis for "Dr" title)
- Claim 3: Previously employed at Macquarie Wealth Management
- Claim 4: Based in Sydney

---

#### Verification results

| Claim | Status | Evidence | Source |
|---|---|---|---|
| Registered financial adviser with ASIC | UNVERIFIABLE | ASIC Financial Advisers Register search on "Priya Narayanan" returns no exact match; a "P. Narayanan" (AFN 001 234 567) is listed with a licence start date of 2019 and current authorisation through Narayanan Advisory Pty Ltd — name spelling discrepancy prevents confident match | [ASIC Financial Advisers Register](https://moneysmart.gov.au/financial-advice/financial-advisers-register) |
| Doctoral qualification ("Dr" title) | UNVERIFIABLE | No academic publications found under this name on Google Scholar or ORCID; no faculty page or alumni listing identifies a doctorate; no thesis record found via Trove (National Library of Australia thesis search) — absence of record does not disprove the claim but no positive evidence found | Google Scholar, ORCID, ResearchGate, Trove |
| Formerly at Macquarie Wealth Management | PARTIAL — UNVERIFIABLE | No current listing on Macquarie's website (expected — former employees are not routinely listed); LinkedIn profile for "Priya Narayanan, Sydney" shows financial services experience 2014–2021 but names "Macquarie Group" broadly, not Macquarie Wealth Management specifically; one LinkedIn recommendation from a Macquarie Wealth Management team member references working together — corroborative but not definitive | Macquarie.com, LinkedIn |
| Based in Sydney | VERIFIED | LinkedIn profile location field shows "Sydney, New South Wales, Australia"; speaking-event listing from a 2023 FINSIA Sydney event names Priya Narayanan as a Sydney-based presenter | LinkedIn, FINSIA events archive |

---

#### Cross-reference consistency

**Photo consistency:** LinkedIn profile photo and a headshot on the 2023 FINSIA Sydney event page appear to show the same individual — consistent facial features, similar age range. No Macquarie-specific photo found for comparison (Macquarie does not publish former-employee profiles). Observation is visual only; no speculation beyond what is shown.

**Timeline consistency:** LinkedIn profile shows continuous financial-services employment from 2014 to present with no unexplained gaps. The Macquarie tenure (2014–2021) aligns with the length of career suggested by profile activity.

**Location consistency:** All sources (LinkedIn, FINSIA event, one press-release mention) place the subject in Sydney. No sources suggest a different location. Consistent.

---

#### Disambiguation

Search for "Priya Narayanan" returned three distinct LinkedIn profiles:

1. Priya Narayanan — Sydney, financial services, Macquarie Group background (this subject, high confidence)
2. Priya Narayanan — Melbourne, software engineering, unrelated industry
3. Priya Narayanan — Auckland, NZ, healthcare sector, unrelated industry

Context anchors (Sydney location + financial advisory field + Macquarie history) narrowed to profile 1 after the first pass. No ambiguity persists. Disambiguation is documented and confident.

ASIC register match is uncertain — "P. Narayanan" with a spelling discrepancy is a separate disambiguation question. Flagged as unverifiable pending clarification of full legal name from the subject.

---

#### Inconsistencies

**Flagged — not contradicted, but unverifiable:**

- ASIC register returns "P. Narayanan" not "Priya Narayanan." This is unverifiable, not contradicted — a common-name abbreviation is a plausible explanation, but positive match cannot be confirmed from public data alone. Recommend requesting the subject's ASIC Registration Number directly.
- Doctoral title ("Dr") has no corroborating evidence in any public academic record. Unverifiable — a genuine doctorate from a non-English-language institution or a professional doctorate without publications would produce the same absence. This is worth raising with the subject directly.
- Macquarie Wealth Management vs Macquarie Group: LinkedIn uses the broader brand. Not contradicted — Macquarie Wealth Management operated as a division of Macquarie Group, so the discrepancy may be a labelling convention rather than a claim error.

**Nothing found that actively contradicts any claim.**

---

#### Confidence assessment

**Overall: Medium**

Sydney location is verified. Professional timeline is plausible and largely consistent. ASIC adviser status is unverifiable from public sources due to name-spelling ambiguity — not disproved. Doctoral title has no positive public evidence. Employment at Macquarie is corroborated but not definitively confirmed for the specific division.

Recommend: request the subject's ASIC Registration Number and doctoral institution before engagement. These are reasonable due-diligence asks that any genuine professional would expect.

---

## Criteria results

### Criteria (vs skill definition)

- [x] PASS: Skill requires and references an authorisation gate record before proceeding — the `[!IMPORTANT]` block states "Do not run without a logged gate record" as a hard precondition
- [x] PASS: Skill starts from the subject's specific claims — Step 1 says "List each claim explicitly before verifying any of them"; output format has a named "Claims to verify" section
- [x] PASS: ASIC Financial Advisers Register is explicitly cited in Step 2 under credential verification with URL
- [x] PASS: Employer verification covers the company's own website and LinkedIn
- [x] PASS: Photo consistency is addressed in Step 3 and in the Rules — "Photo comparison is visual only — note photo consistency across sources; don't speculate beyond what you can observe"
- [x] PASS: Step 5 and the Rules section both distinguish clearly between "unverifiable" and "contradicted"
- [x] PASS: Step 4 documents disambiguation with a three-attempt failure condition and instruction to stop and ask for more context
- [x] PASS: Output format includes a verification results table, cross-reference consistency section, and confidence assessment section
- [x] PASS: Rules section bounds scope to claims — "Start from the subject's claims, not from an open search. You're verifying, not profiling."

### Output expectations (vs simulated output)

- [~] PARTIAL: Gate record fields — the skill requires a gate before invocation and shows `[link or copy]` in the template, but does not enumerate the four specific expected fields (Authorisation, Purpose, Scope, Subject Aware). The simulated output above fills all four because they are reasonable inference from the scenario, but an agent following the skill template verbatim would not be directed to include them — the template underdirects here
- [~] PARTIAL: Claim enumeration — Step 1 requires listing each claim explicitly and the template shows `Claims to verify: [listed]`, but the skill does not specify a numbered labelling convention ("Claim 1, Claim 2…"). The structure is present; the specific labelling format expected by the test is not prescribed by the skill
- [x] PASS: ASIC Financial Advisers Register is named with URL in Step 2; the skill's per-claim verification method covers search method and result
- [x] PASS: Employer verification covers the company's own website and LinkedIn explicitly in Step 2
- [~] PARTIAL: Doctorate verification — the skill covers academic credentials generically (faculty pages, alumni directories, Google Scholar, ORCID, ResearchGate) but does not name Trove for AU thesis records, and does not flag that a "Dr" title without any verifiable academic record is a signal worth explicitly calling out to the client
- [x] PASS: Photo-consistency check is visual-observation only; the rule against speculation is stated in both Step 3 and the Rules section
- [x] PASS: Unverifiable vs Contradicted distinction is explicit in Step 5 and the Rules section
- [x] PASS: Disambiguation method is documented with three-attempt failure condition, context anchors (employer, location, field), and stop-and-ask instruction
- [x] PASS: Rules section prevents scope expansion beyond professional claims in the gate record — the simulated output stays within professional scope throughout
- [x] PASS: Output format table includes Claim, Status (Verified / Unverifiable / Contradicted), Evidence, and Source; Confidence assessment section is present

## Notes

The skill is well-structured. Three partial gaps account for the score reduction: the gate record output template uses a generic `[link or copy]` placeholder without enumerating the four fields the test expects (Authorisation, Purpose, Scope, Subject Aware), leaving field selection to agent interpretation; the claim-enumeration format uses `[listed]` without a numbered convention; and the doctorate verification path omits Trove (the primary AU thesis registry) and does not instruct the agent to explicitly flag an unverifiable doctoral title as a due-diligence signal. None are fundamental failures — the skill produces a recognisable and useful output for this scenario — but the output-expectations test surfaces where the template underdirects for AU-specific professional verification.
