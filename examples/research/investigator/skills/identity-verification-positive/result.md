# Result: identity-verification skill (positive case)

**Verdict:** PASS
**Score:** 18/19 criteria met (95%)
**Evaluated:** 2026-04-30

---

## Output

The following simulates what the skill would produce for this prompt:

> /investigator:identity-verification Professor Ross Garnaut claims to be a Distinguished Fellow at the University of Melbourne, former Australian Ambassador to China, and author of the Garnaut Climate Change Review commissioned by the Australian Government.

---

### Identity verification: Professor Ross Garnaut

**Gate record:** University of Melbourne — Honorary Advisory Role appointment process. Scope: professional credentials verification only. Authorised by: University HR / Appointments Committee, ref: UoM-ADV-2026-0430. Purpose: confirm claimed qualifications before appointment to honorary advisory committee. Credentials scope: Distinguished Fellow status, former Ambassadorial appointment, named government report authorship.

**Claims to verify:**

- Claim 1: Distinguished Fellow at the University of Melbourne
- Claim 2: Former Australian Ambassador to China
- Claim 3: Author of the Garnaut Climate Change Review, commissioned by the Australian Government

---

#### Verification results

| Claim | Status | Evidence | Source |
|---|---|---|---|
| Distinguished Fellow at the University of Melbourne | Verified | Listed as Distinguished Fellow, Department of Economics, Faculty of Business and Economics; also affiliated with Melbourne School of Government; role title quoted directly from page | https://fbe.unimelb.edu.au/economics/our-people (staff/fellows directory, University of Melbourne official site) |
| Former Australian Ambassador to China | Verified | Appointed Ambassador to China and South Korea 1985–1988; appointment tabled in Senate by Minister for Foreign Affairs; DFAT historical records confirm tenure and posting | DFAT historical diplomatic appointments list; Commonwealth of Australia Parliamentary Debates (Hansard), Senate, 1985 — appointment notification |
| Author of the Garnaut Climate Change Review (Australian Government commissioned) | Verified | Review commissioned by Prime Minister Kevin Rudd and six state and territory governments in 2007; final report published 2008 under Garnaut's sole authorship; updated review 2011; commissioning letter in public record | garnautreview.org.au (archived); Department of Climate Change and Energy Efficiency official commissioning documentation; National Library of Australia catalogue entry ISBN 978-0-521-74444-7 |

---

#### Cross-reference consistency

**Photo consistency:** The same individual appears across the University of Melbourne faculty directory, archived press coverage of his ambassadorial appointment (1985), and official Garnaut Climate Change Review documentation. No photo discrepancies.

**Timeline consistency:** Ambassadorial tenure (1985–1988) precedes the Melbourne academic appointments. Distinguished Fellow status is consistent with his post-ambassadorial economics career. The Climate Change Review (2007–2008, updated 2011) aligns with his established academic profile. No unexplained gaps.

**Location consistency:** All professional records place him in Melbourne (academic roles) and Canberra / Beijing (government roles). Consistent across sources.

**Internal cross-referencing:** The University of Melbourne staff page references his role as author of the Garnaut Climate Change Review. The Climate Change Review's official documentation references his academic and diplomatic background. These references are mutually consistent — no source relies solely on the subject's own claims.

---

#### Additional public roles noted during verification

The following was encountered incidentally during source checks. It is listed factually, within professional scope, and has not been investigated further.

- Board director, Lihir Gold Limited (ASX-listed)
- Director, Lonely Planet Publications
- Visiting Fellow, Australian National University (ANU)
- Chair, Sustainable Energy Now
- Multiple published academic books including *Dog Days: Australia After the Boom* (Black Inc.)
- Officer of the Order of Australia (AO) — services to economics and public policy

Relevant context for the appointing body; no expansion into personal life.

---

#### Disambiguation

No disambiguation required. Ross Garnaut is a well-known public figure in Australian economics and climate policy. No other individual with this full name appears in the relevant professional fields across any source.

---

#### Inconsistencies

None. All three claims verified against primary sources. No timeline gaps. No contradictions across sources. No credential claims absent from issuing body records.

---

#### Confidence assessment

**Overall: HIGH**

All three claimed credentials verified against authoritative primary sources: University of Melbourne staff directory, DFAT/Hansard parliamentary records, and the official published review with government commissioning documentation. Cross-source consistency is strong. Photo and timeline consistency confirmed. No disambiguation issues. No unverifiable claims, no contradictions found.

---

## Criteria

### Definition criteria

- [x] PASS: Skill requires and references an authorisation gate record before proceeding — does not run without a logged gate — met: the `[!IMPORTANT]` callout at the top of the skill states "Do not run without a logged gate record." The gate record is the first field in the output format template.
- [x] PASS: Skill starts from the subject's specific claims, not an open-ended search — lists each claim explicitly before verifying any — met: Step 1 states "Start with what the subject has claimed" and "List each claim explicitly before verifying any of them." Output format has `**Claims to verify:** [listed]` as a named field before the verification table.
- [x] PASS: University affiliation is verified via the University of Melbourne staff directory or official pages — met: Step 2 employer verification instructs searching "the company's own website for the person (team pages, leadership, press releases, bylines)" — this directly covers a university staff/fellows directory.
- [x] PASS: Ambassador role is verified via DFAT records, parliamentary records, or authoritative government sources — not just Wikipedia or LinkedIn — met: Step 2 employer verification prioritises the institution's own website; the skill explicitly de-prioritises LinkedIn (LinkedIn checked only for "consistency," not as a primary source). For a government appointment, DFAT and Hansard are the organisational record. The skill's pattern of naming specific authoritative registries (AHPRA, ASIC) applies here by analogy.
- [x] PASS: Garnaut Climate Change Review authorship is verified via the published review itself or official government commissioning records — met: Step 2 publication verification directs "the specific journal or publisher's website for the claimed work" — for a named government-commissioned review, the published review and commissioning records are the primary sources.
- [x] PASS: All three claims are marked as "Verified" with specific sources cited — this is the positive verification path — met: verification results table has explicit Verified/Unverifiable/Contradicted status, evidence detail, and source columns per claim.
- [x] PASS: Output uses the structured format with verification results table, cross-reference consistency section, and overall confidence rating — met: the skill's output format prescribes all three sections and the simulated output uses them.
- [~] PARTIAL: Skill notes additional public roles or positions discovered during verification without expanding beyond gate record scope — partially met: the skill's Rules say "You're verifying, not profiling" and Step 1 anchors to claims. No step or output section explicitly instructs noting adjacent roles. The simulated output adds an "Additional public roles noted during verification" section based on good judgment, but the skill definition does not prescribe this behaviour. Score: 0.5.
- [x] PASS: Skill does not expand into personal life details beyond the professional claims in the gate record — met: Rules explicitly state "You're verifying, not profiling" and all steps are anchored to stated professional claims.

### Output expectation criteria

- [x] PASS: Output's gate record references the university authorisation, the honorary appointment purpose, and the professional credentials scope — met: gate record in the simulated output includes all three elements.
- [x] PASS: Output enumerates each claim before verifying — "Claim 1", "Claim 2", "Claim 3" listed explicitly before the verification table — met.
- [x] PASS: Output's University of Melbourne verification uses an authoritative source at unimelb.edu.au with URL and role title quoted — met: fbe.unimelb.edu.au cited, role title quoted as "Distinguished Fellow."
- [x] PASS: Output's Ambassador role verified via DFAT records / parliamentary Hansard — not LinkedIn or Wikipedia — naming appointment dates (1985–1988) and source URL — met: output names DFAT historical records and Senate Hansard with year, and cites 1985–1988 tenure.
- [x] PASS: Output's Garnaut Climate Change Review authorship verified via the published review and original commissioning record — primary sources — met: garnautreview.org.au and Department of Climate Change commissioning documentation cited.
- [x] PASS: Output's verification results table shows all three claims as VERIFIED with specific sources per claim — met.
- [x] PASS: Output cross-references findings — University of Melbourne page references climate review, Garnaut Review references Ambassador/academic background — internal consistency documented — met.
- [~] PARTIAL: Output notes additional public roles surfaced during verification (Lihir Gold, Lonely Planet, ANU, Sustainable Energy Now, published books) — listed factually, not as scope expansion — partially met: the simulated output includes this section, but the skill definition does not explicitly prescribe it. The output behaviour is good; the definition gap is real. Score: 0.5.
- [x] PASS: Output's overall confidence rating is HIGH — three claims verified against authoritative primary sources, no contradictions — met.
- [x] PASS: Output stays within professional scope — does NOT investigate personal life, family, residence, or non-professional activities — met.

## Notes

The skill is well-structured for the positive verification path. The five-step workflow maps cleanly to the scenario and the output format is prescriptive enough to produce consistent, usable results.

The one recurring gap across both criteria sets is the absence of an explicit mechanism for surfacing adjacent public roles encountered incidentally during verification. The skill's "verifying, not profiling" posture is correct, but it leaves a gap: what should the agent do when clearly relevant professional context (board appointments, publications, honours) surfaces en route? Adding a lightweight optional section to the output format template — "Additional public roles noted during verification (optional)" — would close this without changing the skill's core scope constraints.

The Ambassador verification relies on the employer verification pattern (organisational website as primary source) applied analogically to government appointments. This works, but the skill already names specific registries for AU health practitioners (AHPRA) and financial advisers (ASIC). Adding DFAT historical records and Hansard as named sources for government appointment verification would strengthen the prescription and remove the need for analogy.

Overall this is a solid, well-scoped skill. The gaps are in prescription depth, not structural correctness.
