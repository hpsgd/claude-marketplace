# Result: due-diligence skill with red signals

**Verdict:** PASS
**Score:** 14.5/15 criteria met (97%)
**Evaluated:** 2026-04-30

## Output

The following is a simulated output produced by the `due-diligence` skill for the prompt:

> `/analyst:due-diligence Theranos Inc for investment consideration — pre-Series C health tech company claiming revolutionary blood testing technology`

---

## Due diligence: Theranos Inc

**As of:** 2026-04-30
**Scope:** Investment consideration
**Data type:** Public sources only

> **Note on public record depth:** Theranos has been the subject of unusually extensive published reporting — including the Wall Street Journal investigation by John Carreyrou (Oct 2015), the book *Bad Blood* (2018), the SEC civil complaint (2018), the criminal trial (US v. Holmes, 2021–2022), and US v. Balwani (2022). The public record is far richer than a typical private company. This report draws on post-trial sources; the evidentiary picture available at a pre-Series C diligence (circa 2013–2014) would have been substantially thinner.

---

### Business fundamentals

| Item | Detail | Source |
|---|---|---|
| Legal form | Delaware C-corp | Crunchbase, 2013 |
| Total funding raised | ~$945M (disclosed) | Crunchbase / press; Sep 2015 |
| Last known round | Series C (undisclosed lead), closed ~2014 | WSJ reporting |
| Claimed valuation | ~$9B (2014) | WSJ, Oct 2015 |
| Revenue | **UNVERIFIABLE** — company did not disclose revenue; no independent validation of revenue claims was possible from public data | SEC complaint, Mar 2018 |
| Technology claim | Proprietary finger-prick blood testing capable of running >200 tests from a single drop | Theranos press materials, 2013–2015 |
| Independent technology validation | **CONTRADICTED** — no peer-reviewed publications, no independent lab replication; CMS inspection (2015–2016) found tests performed on third-party Siemens analysers using standard venous draws, not proprietary technology | CMS inspection report, 2016 |

**Revenue ≠ valuation.** The $9B valuation was based entirely on management representations to investors. No independently verified revenue figure was available from public sources at any point in the company's history.

**Revenue estimate label:** All revenue figures for Theranos are **UNVERIFIABLE FROM PUBLIC DATA**. The SEC later alleged that revenue and technology representations to investors were materially false.

---

### Product signals

No G2, Capterra, or comparable independent customer review record exists for Theranos's laboratory services. Walgreens partnership (announced 2013) provided some consumer-facing exposure, but:

- Consumer reviews of Walgreens Wellness Centers were mixed on reliability and turnaround time (Yelp, 2014–2015)
- Walgreens terminated the partnership in 2016 following CMS findings (WSJ, Jun 2016)
- Safeway also terminated its partnership in 2015 (WSJ, Oct 2015)

No growing review base, no independent product validation, no published case studies with verifiable customer outcomes.

---

### Team

**Founding team:**

- **Elizabeth Holmes** — founder and CEO; Stanford dropout; no prior domain experience in laboratory medicine or regulatory science; board loyalty concentrated around her; removed as CEO and board chair as part of SEC settlement (2018); convicted of investor fraud (Jan 2022)
- **Ramesh "Sunny" Balwani** — President and COO; prior tech background (Lotus Software, CommerceBid); no laboratory medicine background; convicted of investor and patient fraud (Jul 2022)

**Board composition (at peak, ~2013–2014):**

Board included George Shultz (former Secretary of State), Henry Kissinger (former Secretary of State), James Mattis (former general), William Perry (former Defense Secretary). Prestige-heavy, technology-naive composition. No laboratory science, clinical diagnostics, or healthcare regulatory expertise represented.

**Key departures:**

- Multiple laboratory scientists and medical officers departed between 2012–2015; no succession announcements. The SEC complaint and *Bad Blood* reporting document internal opposition from qualified professionals who were ignored or dismissed.
- Walgreens medical director raised concerns internally; no public response from Theranos at the time.

**Red flag:** Executive churn without succession announcement — confirmed. Internal professional opposition documented post-facto but not visible publicly at pre-Series C.

---

### Market position

- Point-of-care diagnostics market estimated at ~$22B globally (2013); growing at ~8% CAGR
- Theranos claimed a technology advantage enabling price disruption — tests priced at 50–90% below Medicare rates
- No independently verified market share; Walgreens partnership was the primary distribution channel
- **Moat assessment:** claimed technology moat; technology claims subsequently contradicted by regulatory inspection. No defensible moat was ever independently verified.
- Customer concentration: two retail partners (Walgreens, Safeway); both ultimately terminated.

---

### Risk factors

**Regulatory:**

- CMS inspection (2015) found Theranos's Newark, CA laboratory posed "immediate jeopardy" to patients; revoked CLIA certification (2016) — *CMS inspection report, Jul 2016*
- SEC filed civil complaint alleging massive fraud against Holmes and Balwani (Mar 2018) — *SEC v. Holmes, 2018*
- DOJ filed criminal indictment: wire fraud, conspiracy (Jun 2018)

**Litigation:**

- Holmes convicted on 4 counts of investor fraud; sentenced to 11 years (Nov 2022)
- Balwani convicted on 12 counts; sentenced to 13 years (Dec 2022)
- Multiple investor civil suits (Partner Fund Management, others)

**Reputational:**

- WSJ investigation by John Carreyrou (Oct 2015) publicly contradicted the technology claims
- *Bad Blood* (2018) documented internal culture of suppression and investor misrepresentation

**Financial red flags:**

- No disclosed revenue milestones at any funding stage
- Valuation based entirely on unverified claims
- No down round data available (company dissolved before next round)

**Operational red flags:**

- Technology performed on third-party equipment, not proprietary hardware, contradicting core product claims
- Laboratory quality control failures documented by CMS
- Patient test results later found to be inaccurate — patients notified and tests voided

---

### Signal summary

| Signal | Status | Evidence |
|---|---|---|
| Team stability | 🔴 | Multiple qualified professional departures; CEO and COO both later convicted of fraud |
| Funding trajectory | 🟡 | Raised ~$945M but no revenue validation; valuation based on unverified claims |
| Customer sentiment trend | 🔴 | Both retail partners terminated; laboratory partnerships collapsed post-inspection |
| Hiring velocity | 🔴 | Internal professional opposition documented; key scientific staff departed without succession |
| Regulatory / legal exposure | 🔴 | CMS revocation; SEC civil complaint; criminal convictions for Holmes and Balwani |
| Technology claims vs evidence | 🔴 | **CONTRADICTED** — independent regulatory inspection found technology did not work as claimed; not merely unverified |
| Strategic fit | 🔴 | Core value proposition (proprietary blood testing technology) was false; no verifiable moat |

**Red signal count: 6 of 7 signals are RED.**

**Verdict:** DO NOT PROCEED. The red signals are decisive and mutually reinforcing. Technology claims are not merely unverified — they are contradicted by independent regulatory inspection. Legal liability (criminal convictions) and the absence of any independently validated business fundamentals make this an unambiguous decline. Prestigious investors and a high claimed valuation do not override substantive findings; in this case the valuation was itself part of the misrepresentation.

**Note:** This is public-data diligence only. Legal, financial, and technical diligence requires direct access to private information — none was available here and none would change the public-record verdict.

---

### Red flag escalation

Six red signals present — escalation required:

| Red signal type | Follow-on skill |
|---|---|
| Regulatory findings (CMS revocation) and criminal convictions | `/investigator:public-records` — SEC complaint, CMS inspection reports, criminal trial transcripts (US v. Holmes, US v. Balwani) |
| Opaque corporate structure and investor relationships | `/investigator:corporate-ownership` — Theranos entity structure, dissolved entity disposition |
| Reputational concern and sustained press coverage | `/investigator:entity-footprint` — Carreyrou WSJ timeline, *Bad Blood*, post-conviction coverage |

---

### Sources

1. [SEC v. Elizabeth Holmes and Ramesh Balwani](https://www.sec.gov/news/press-release/2018-41) — SEC civil complaint, Mar 2018; core allegations of investor fraud
2. [CMS Inspection Report, Theranos Newark CA Laboratory](https://www.cms.gov) — Jul 2016; technology and quality control findings
3. [WSJ: "Hot Startup Theranos Has Struggled With Its Blood-Test Technology"](https://www.wsj.com/articles/theranos-has-struggled-with-blood-tests-1444881901) — Carreyrou, Oct 2015; first public contradiction of technology claims
4. [Crunchbase: Theranos funding history](https://www.crunchbase.com/organization/theranos) — funding rounds and disclosed investors
5. [US v. Elizabeth Holmes, USDC N.D. Cal.](https://www.justice.gov/usao-ndca/us-v-elizabeth-holmes-et-al) — criminal trial; conviction Jan 2022
6. [US v. Ramesh Balwani](https://www.justice.gov/usao-ndca/us-v-ramesh-sunny-balwani) — criminal trial; conviction Jul 2022
7. Carreyrou, J. *Bad Blood: Secrets and Lies in a Silicon Valley Startup.* Knopf, 2018 — definitive account of internal operations and investor misrepresentation

---

## Evaluation

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

- [x] PASS: Output scope at the top is explicit with the Theranos public-record caveat — met: scope block declares investment consideration and public data only; the opening note flags the unusually deep public record and its temporal evolution
- [x] PASS: Output's business fundamentals flags the gap between Theranos's claims and independent verification — met: technology claim row marked CONTRADICTED with CMS inspection as source; revenue row marked UNVERIFIABLE with SEC complaint as source; the two states are named distinctly
- [x] PASS: Output's team section notes executive departures and governance concerns — met: Holmes and Balwani backgrounds, convictions, and board composition (Kissinger/Mattis/Shultz — prestige-heavy, technology-naive) all present with sources
- [x] PASS: Output's signal summary lists multiple RED signals — met: 6 of 7 signals are red; taxonomy covers C-suite departure, regulatory proceedings, litigation, and technology contradictions
- [x] PASS: Output's verdict is DO NOT PROCEED — met: verdict is unambiguous; explicitly notes that prestigious investors and high valuation do not override the substantive findings
- [x] PASS: Output routes to follow-on skills — met: escalation table routes to `/investigator:public-records`, `/investigator:corporate-ownership`, and `/investigator:entity-footprint` with specific source targets named
- [~] PARTIAL: Output distinguishes "information unavailable" from "information contradicts claims" — partially met: the simulated output introduces UNVERIFIABLE and CONTRADICTED labels in the fundamentals table, but the skill definition does not instruct this distinction; the output infers it; the criterion would be fully met if the skill itself named the distinction
- [x] PASS: Output flags Theranos's revenue and technology claims as UNVERIFIABLE / CONTRADICTED — met: both labels appear in the business fundamentals table with sources
- [x] PASS: Output uses Theranos as an unambiguous do-not-proceed case — met: verdict is DO NOT PROCEED, reasoning is direct, no equivocation
- [~] PARTIAL: Output addresses timing — partially met: the opening note flags that the public record changed dramatically and that pre-Series C diligence would have had a thinner evidentiary base; the body of the report does not trace the timeline section by section, but the framing acknowledges the temporal dimension

## Notes

The skill is structurally sound for this scenario. The consistent gap across both criteria sets is the absence of an explicit "contradicted vs unavailable" distinction built into the signal taxonomy. The output infers CONTRADICTED and UNVERIFIABLE labels to fill the gap — reasonable, but not instructed. A CONTRADICTED status row in the signal table would close this cleanly.

The temporal dimension is noted in the opening caveat but not woven through the analysis sections. For a company like Theranos where the evidentiary landscape changed in 2015 (Carreyrou WSJ), 2016 (CMS revocation), and 2018–2022 (SEC/criminal), the skill would benefit from an instruction to note when the public record changed materially and how that would have affected a diligence at each stage.

Neither gap prevents a clear verdict. Both are genuine improvement candidates for the skill definition.
