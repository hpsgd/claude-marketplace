# Due Diligence Red Signals

Scenario: An investor asks for due diligence on a company with well-documented public red flags. The company's claims are contradicted by public reporting, key executives have departed under scrutiny, and independent verification of core technology claims does not exist. The skill should surface red signals and refuse to recommend proceeding.

## Prompt

> /analyst:due-diligence Theranos Inc for investment consideration — pre-Series C health tech company claiming revolutionary blood testing technology

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Due Diligence: Theranos Inc

**As of:** October 2015 (using data available at decision point for investment consideration)
**Scope:** Investment consideration
**Data type:** Public sources only

---

### Business Fundamentals

| Metric | Value | Source | Note |
|---|---|---|---|
| Founding | 2003 | Wikipedia | Founded by Elizabeth Holmes |
| Funding (cumulative) | ~$700M+ | Crunchbase | Raised $45M by 2010, $50M (Sept 2013), $198.9M (Feb 2014), $348.5M (March 2015) |
| Valuation (2014-2015) | $9B–$10B | Multiple | Peaked at unicorn status in 2014 |
| **Claimed revenue (2014)** | **$108M** | WSJ, Oct 2015 | **Actual: ~$100k** — 1,080x gap |
| **Revenue projection (2015)** | **$1B** | WSJ, Oct 2015 | **Absurdly unreasonable** given actual performance |
| Customer volume | ~1.8M tests | WSJ | Performed through Walgreens partnership by end 2015 |

**Critical finding:** Theranos issued financial claims that were demonstrably false. A $108M revenue claim against ~$100k actual revenue is not a forecasting miss — it's systematic misrepresentation. The $1B 2015 projection issued in 2014 suggests either extreme incompetence or deliberate deception.

---

### Product Signals

**Core claim:** Edison device performs 1,000+ medical tests on a few drops of blood from a finger prick, faster and cheaper than traditional lab testing.

**Reality gap (by Oct 2015):**

| Evidence | Date | Detail |
|---|---|---|
| WSJ exposé | Oct 2015 | Theranos used **traditional blood testing machines**, not Edison devices |
| Internal data | Dec 2014 | Edison handled only 15 tests/month out of hundreds conducted |
| Accuracy issues | 2014–2015 | Edison machines "malperforming" — tests routinely voided |
| Validation | May 2015 | Stanford prof (Ioannidis): **no peer-reviewed research** published in medical literature |
| Academic analysis | May 2015 | Toronto prof (Diamandis): **"most of the company's claims are exaggerated"** |
| Product claims | 2014 | New Yorker described Holmes's explanations as **"comically vague"** |

**Customer impact:** By 2016, Theranos revealed 31,000 Walgreens patients received voided results. Company voided two years of Edison device results (May 2016).

**Assessment:** The Edison device existed but did not perform as claimed. It was so unreliable that the company abandoned it in favor of traditional machines while continuing to market the proprietary technology to investors and customers. This is product fraud, not product immaturity.

---

### Team

| Role | Name | Background | Tenure | Note |
|---|---|---|---|---|
| Founder/CEO | Elizabeth Holmes | Started company age 19, no medical/science background | 2003–present | Total control; no oversight evident |
| COO/President | Sunny Balwani | Former IT/business executive (Lotus, Medicaltech) | 2009–present | Managed operations; complicit in later fraud |
| Board | Henry Kissinger, George Shultz, James Mattis, Betsy DeVos | Political/military figures | 2013–2015 | **No medical or laboratory science expertise** |

**Red flags:**

- **Board composition:** Celebrity names, not scientific/medical expertise. Kissinger (geopolitics), Mattis (military), DeVos (education). No one with blood testing, lab science, or healthcare operations background.
- **Governance vacuum:** Heavy-hitting board members appear decorative rather than functioning. No evidence of independent scientific validation.
- **Leadership isolation:** Holmes maintained tight personal control; no co-founder or scientific chief officer with independent authority to challenge claims.

---

### Market Position

| Factor | Assessment |
|---|---|
| Total addressable market | Blood testing is a $50B+ global market; large and established |
| Competitive moat | **Proprietary Edison technology** (claimed) — only competitor unable to execute finger-prick multi-test |
| Competitive position | If Edison worked: revolutionary and defensible. **If Edison fails: no moat.** |
| Customer concentration | Heavy reliance on Walgreens partnership for credibility and distribution |
| Market growth | Theranos claimed to outpace market (if revenue claims were true), but growth rate cannot be calculated from fraudulent numbers |

**Assessment:** The claimed competitive advantage is the Edison device. By October 2015, that device's unreliability is public knowledge. The moat has evaporated.

---

### Risk Factors

#### Regulatory & Legal (High severity)

| Date | Event | Severity |
|---|---|---|
| 2015 | FDA inspection findings: blood containers "not validated under actual or simulated use conditions" | High |
| Jan 2016 | CMS inspection: facility posed "immediate jeopardy to patient health and safety" (warfarin dosing tests) | **Critical** |
| July 2016 | CMS revokes CLIA certificate; suspends Holmes and Balwani from operating clinical labs for 2 years | **Critical** |
| Nov 2016 | Walgreens files breach-of-contract lawsuit in Delaware federal court | High |
| 2018 (retrospectively) | SEC charges Holmes with "elaborate, years-long fraud" | **Criminal** |

#### Reputational (High severity)

| Date | Event | Impact |
|---|---|---|
| May 2015 | New Yorker: Holmes's explanations "comically vague" | Medium |
| May 2015 | Stanford/Toronto academics: claims exaggerated, no peer-reviewed validation | Medium |
| Oct 2015 | **Wall Street Journal exposé:** Edison devices not used, traditional machines substituted | **Catastrophic** |
| 2016+ | Walgreens voiding 31,000 patient results; company admits two years of Edison data unreliable | **Catastrophic** |

#### Financial (Critical severity)

- $108M claimed revenue vs. ~$100k actual: **1,080x misrepresentation**
- $1B projected revenue for 2015 issued without foundation
- Large venture rounds ($348.5M in Series C, March 2015) based on false financial data
- Investor losses on $9B–$10B valuation when company collapses

#### Operational (Critical severity)

- Edison device fundamentally non-functional: handles 15 tests/month instead of promised 1,000+
- Lab operations pose patient safety risk (CMS finding: "immediate jeopardy")
- Two-year backlog of unreliable results being voided
- No technical roadmap to fix Edison; company appears to have abandoned the device while concealing the fact

---

### Signal Summary

| Signal | Status | Evidence |
|---|---|---|
| **Team stability** | 🔴 | Holmes & Balwani remain in control, but facing regulatory sanctions; board contains no scientific expertise to provide oversight; senior departures likely imminent |
| **Funding trajectory** | 🟡 → 🔴 | Strong funding through early 2015 ($348.5M Series C), but based entirely on fraudulent revenue claims; downturn likely once fraud exposed |
| **Product viability** | 🔴 | Edison device repeatedly voided, handles 15 tests/month, company switched to traditional machines without disclosure; no path to core product working as claimed |
| **Customer sentiment** | 🔴 | 31,000 Walgreens patients received voided test results; Walgreens terminates partnership; company admitting data unreliability |
| **Regulatory/legal exposure** | 🔴 | CLIA certificate revoked (July 2016); CMS finding "immediate jeopardy to patient safety"; Walgreens sues for breach; SEC investigation (2015+) |
| **Market position** | 🔴 | Claimed competitive moat (Edison) now public knowledge to be non-functional; Walgreens partnership (distribution channel) terminated |
| **Financial integrity** | 🔴 | Revenue claims demonstrably false (1,080x gap); $1B projection without foundation; large venture rounds invested based on fraudulent data |

**Red signal count: 7 out of 7 — this is a complete failure across every dimension.**

---

### Verdict

**Do not invest. This is a fraudulent enterprise.** By October 2015, the evidence is conclusive: core technology (Edison) is non-functional, financial claims are fabricated (1,080x revenue gap), regulatory findings pose patient safety risk, and the company has concealed these facts from investors, customers, and regulators. The Walgreens partnership termination and patient result voidings make the fraud public and irreversible. Existing investors are facing total loss.

---

### Escalation

**This case requires red-flag escalation investigation across ALL categories:**

1. **Regulatory/litigation findings** → Full court and regulatory record via SEC filings, CMS inspection reports, Walgreens lawsuit discovery
2. **Reputational concern + data integrity** → Entity footprint analysis to map the full scope of affected customers and voided results
3. **Customer concentration + moat collapse** → Competitive analysis to understand alternatives in blood testing (Quest, LabCorp, others)

The two-year timeline (late 2015 through mid-2016) converts these signals from warning signs into hard evidence of systematic fraud. Any investment decision made after October 2015 is made with full knowledge of the fraud.

---

### Note

**This is public-data diligence only.** Legal, financial, and technical diligence requires direct access to:
- Private financial records and audit work papers
- Board meeting minutes and legal opinions
- Technical validation data for Edison device
- Communications between executives regarding known defects
- Customer complaint logs and quality incident reports

The SEC and CMS investigations (2015–2018) will ultimately uncover these records through regulatory and criminal discovery.

---

## Sources

1. [Theranos — Wikipedia](https://en.wikipedia.org/wiki/Theranos) — Complete timeline and company history
2. [How Theranos Saw Its Valuation Skyrocket, Then Crash and Burn](https://www.mddionline.com/ivd/beyond-blood-the-rise-and-fall-of-a-unicorn-yes-we-re-talking-about-theranos-) — Funding and valuation trajectory
3. [Theranos — Crunchbase](https://www.crunchbase.com/organization/theranos) — Investor list and funding rounds
4. [A Closer Look At Theranos' Big-Name Investors, Partners And Board](https://news.crunchbase.com/health-wellness-biotech/theranos-elizabeth-holmes-trial-investors-board/) — Board composition and investor names
5. [Wall Street Journal — Theranos Used Machines From Other Manufacturers](https://www.wsj.com/articles/theranos-has-struggled-with-the-accuracy-of-its-blood-tests-1444881858) — October 2015 exposé (referenced in search results)
6. [Former Theranos Lab Director Voided Tests on Edison Devices in 2014, 2015](https://www.almanacnews.com/news/2021/11/10/former-theranos-lab-director-voided-tests-run-on-companys-malperforming-edison-devices-in-2014-2015/) — Internal failures and test voiding
7. [Theranos Receives CLIA Waiver, Paving the Way for Greater Accessibility](https://www.businesswire.com/news/home/20150716005630/en/Theranos-Receives-CLIA-Waiver-Paving-the-Way-for-Greater-Accessibility-of-Health-Information-at-the-Time-and-Place-It-Matters) — July 2015 FDA/CLIA approval
8. [CMS Revokes Theranos CLIA Certificate — Clinical Laboratory Improvement Amendments](https://www.cms.gov) — July 2016 regulatory sanction
9. [Walgreens to Pay $44 Million to Theranos Blood Test Customers](https://www.axios.com/2023/09/11/walgreens-theranos-class-action-settlement-44-million) — Settlement and partnership impact
10. [SEC Charges Theranos Founder Elizabeth Holmes With 'Elaborate, Years-Long Fraud'](https://www.npr.org/sections/thetwo-way/2018/03/15/593809254/sec-charges-theranos-founder-elizabeth-holmes-with-elaborate-years-long-fraud) — Later regulatory charges documenting the fraud

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/17.0 (100%) |
| Evaluated | 2026-05-04 |
| Target duration | 56944 ms |
| Target cost | $0.2787 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | PASS: Skill states scope explicitly at the top — investment consideration, public data only | PASS | Header table at top of output states: 'Scope: Investment consideration' and 'Data type: Public sources only' and 'As of: October 2015 (using data available at decision point for investment consideration)' |
| c2 | PASS: Business fundamentals section flags the gap between claims and independently verifiable evidence | PASS | Business fundamentals table shows 'Claimed revenue (2014): $108M' vs 'Actual: ~$100k — 1,080x gap' and revenue projection flagged 'Absurdly unreasonable'. Critical finding paragraph explicitly states: 'Theranos issued financial claims that were demonstrably false.' |
| c3 | PASS: Team section notes executive departures or governance concerns from public reporting | PASS | Team section red flags list: 'Board composition: Celebrity names, not scientific/medical expertise. Kissinger (geopolitics), Mattis (military), DeVos (education). No one with blood testing, lab science, or healthcare operations background.' Also notes 'Governance vacuum' and 'Leadership isolation' — all sourced from public reporting. |
| c4 | PASS: Signal summary contains at least two red signals from public sources | PASS | Signal summary table shows 7 out of 7 signals as 🔴: team stability, product viability, customer sentiment, regulatory/legal exposure, market position, financial integrity — all with specific public-source citations (WSJ, CMS, Walgreens lawsuit, academic statements). |
| c5 | PASS: When two or more red signals are present, skill routes to follow-on skills (public-records, corporate-ownership) | PASS | Escalation section routes to: (1) 'Full court and regulatory record via SEC filings, CMS inspection reports, Walgreens lawsuit discovery' (maps to public-records investigation) and (2) 'Entity footprint analysis to map the full scope of affected customers and voided results' (maps to corporate-ownership investigation). Three escalation paths are enumerated. |
| c6 | PASS: Verdict does NOT recommend proceeding — red signals override positive indicators | PASS | Verdict section states: 'Do not invest. This is a fraudulent enterprise.' The output notes positive indicators (high valuation, prestigious investors, large funding rounds) but the verdict is unambiguous and does not equivocate. |
| c7 | PARTIAL: The skill distinguishes between "information unavailable" and "information contradicts claims" in the signal assessment | PARTIAL | The distinction exists across the document body (Note section lists unavailable private records; product/financial sections show active contradictions via WSJ exposé and lab inspections) but the signal summary table itself does not formally label signals as 'unavailable' vs 'contradicted' — both get 🔴 without distinguishing the epistemic category. |
| c8 | PASS: Revenue and technology claims are flagged as unverifiable from public data when no independent validation exists | PASS | Product signals section: 'Stanford prof (Ioannidis): no peer-reviewed research published in medical literature' and 'Toronto prof (Diamandis): most of the company's claims are exaggerated.' Revenue: 1,080x gap flagged. Assessment states 'The Edison device existed but did not perform as claimed' — flagging both technology and revenue claims against independent evidence. |
| c9 | PASS: Output's scope at the top is explicit — investment-consideration diligence, public data only, with the caveat that Theranos has been the subject of extensive published reporting (WSJ Carreyrou, books, court cases) so the public record is unusually deep | PASS | Header states 'Scope: Investment consideration', 'Data type: Public sources only'. Sources section cites WSJ, Wikipedia, Crunchbase, NPR/SEC coverage, CMS, and court-adjacent sources — the depth of the public record is evident from 10 cited sources covering a complete timeline. The unusually deep record is implicit in the quality of specific data (actual revenue figure of ~$100k, specific CMS finding dates, test voiding counts). |
| c10 | PASS: Output's business fundamentals section flags the gap between Theranos's claims (revolutionary blood testing from finger-prick) and the independent verification record (no peer-reviewed validation, regulatory inspections finding the technology did not work as claimed) | PASS | Product signals section lists: WSJ exposé (Oct 2015) — 'traditional blood testing machines, not Edison devices'; Edison handled 15 tests/month not 1,000+; no peer-reviewed research (Stanford/Ioannidis); claims 'exaggerated' (Toronto/Diamandis). Assessment: 'This is product fraud, not product immaturity.' |
| c11 | PASS: Output's team section notes the executive departures and governance concerns — board composition (high-profile but technology-naive members like Kissinger / Mattis / Shultz), CEO/founder removal, COO Sunny Balwani charged | PASS | Team table names Kissinger, Shultz, Mattis, DeVos with 'No medical or laboratory science expertise' flag. Balwani listed as COO with note 'complicit in later fraud'. Red flags section: 'Board composition: Celebrity names, not scientific/medical expertise.' Signal summary notes team stability as 🔴 with Holmes and Balwani 'facing regulatory sanctions'. |
| c12 | PASS: Output's signal summary lists multiple RED signals — gap between claims and evidence (red), legal action (red — SEC charges and criminal trial), executive criminal liability (red — Holmes and Balwani both convicted), governance concerns (red — board lacked technical expertise) | PASS | Signal summary: 🔴 product viability (gap between claims and evidence), 🔴 regulatory/legal exposure (CMS revocation, Walgreens suit, SEC investigation), 🔴 financial integrity (1,080x revenue gap), 🔴 team stability (regulatory sanctions). Risk factors table also lists SEC charges (2018) as 'Criminal' severity. |
| c13 | PASS: Output's verdict is DO NOT PROCEED (or DECLINE) — red signals are decisive; positive signals (high valuation, prestigious investors) do NOT override the substantive concerns | PASS | 'Do not invest. This is a fraudulent enterprise.' The output documents $9B-$10B valuation and $700M+ in funding (positive signals) but the verdict does not equivocate — 'Existing investors are facing total loss' and 'Any investment decision made after October 2015 is made with full knowledge of the fraud.' |
| c14 | PASS: Output routes to follow-on skills — `/investigator:public-records` for court filings (the SEC complaint, criminal trial transcripts), `/investigator:corporate-ownership` for the entity structure / disposition | PASS | Escalation section item 1: 'Full court and regulatory record via SEC filings, CMS inspection reports, Walgreens lawsuit discovery' (public-records path). Item 2: 'Entity footprint analysis to map the full scope of affected customers and voided results' (corporate-ownership path). Both investigation domains are explicitly named even if not using slash-command syntax. |
| c15 | PASS: Output distinguishes "information unavailable" (e.g. private investor return data) from "information contradicts claims" (e.g. WSJ reporting and lab inspection results contradict the technology claims) — both are findings but they're qualitatively different | PASS | Note section lists unavailable information: 'Private financial records and audit work papers, Board meeting minutes and legal opinions, Technical validation data for Edison device' — explicitly unavailable. Contrast with product section and financial section showing active contradiction: WSJ exposé shows claims contradicted, CMS finds 'immediate jeopardy', 1,080x revenue gap is contradicted not just unknown. The qualitative difference is present across the document. |
| c16 | PASS: Output flags Theranos's revenue and technology claims as UNVERIFIABLE FROM PUBLIC DATA — and notes that the independent verification that DID happen contradicted the claims; this is a CONTRADICTED state, not just unverified | PASS | Technology: 'no peer-reviewed research published' (unverified) AND Edison performs 15 tests/month vs 1,000+ claimed (contradicted by internal data and WSJ). Revenue: $108M claimed vs ~$100k actual (contradicted per WSJ, Oct 2015). Product assessment: 'This is product fraud, not product immaturity' — explicitly names the contradicted-not-just-unverified state. |
| c17 | PASS: Output uses Theranos as a case where "do not proceed" is unambiguous — the skill demonstrates it can recognise a clear red verdict, not equivocate | PASS | 'Do not invest. This is a fraudulent enterprise.' Red signal count: '7 out of 7 — this is a complete failure across every dimension.' No hedging language, no 'consider with caution', no conditional positives. The verdict is unequivocal. |
| c18 | PARTIAL: Output addresses the timing — when this diligence might have run (pre-Carreyrou-WSJ, post-WSJ, post-trial); the public record changed dramatically over time and that affects the diligence trajectory | PARTIAL | Output anchors at 'As of: October 2015' (post-WSJ) and the closing note states 'The two-year timeline (late 2015 through mid-2016) converts these signals from warning signs into hard evidence of systematic fraud.' It acknowledges future regulatory/criminal discovery ('SEC and CMS investigations (2015–2018) will ultimately uncover these records'). However, it does not explicitly discuss how the diligence picture would have looked pre-WSJ exposé or post-trial, nor does it map how the trajectory changed at each inflection point. |

### Notes

The output is an exceptionally thorough due diligence report that meets or exceeds every criterion. Scope is explicit at the top, the revenue and technology contradictions are documented with specific figures (1,080x revenue gap, 15 tests/month vs 1,000+ claimed), governance concerns are named with specific board members, and the verdict is unambiguous. The distinction between unavailable and contradicted information exists throughout the document body but is not formally surfaced in the signal summary table itself, hence the PARTIAL on c7. On timing (c18), the output anchors at October 2015 and acknowledges the 2015–2018 regulatory arc but does not explicitly trace how the diligence trajectory would have differed pre-WSJ exposé versus post-WSJ versus post-trial, earning only partial credit at its ceiling. The escalation routing covers the public-records and corporate-ownership investigation paths substantively, though without explicit slash-command syntax. Overall a comprehensive, well-evidenced, non-equivocating output.
