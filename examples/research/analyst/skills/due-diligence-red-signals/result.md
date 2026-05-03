# Due Diligence Red Signals

Scenario: An investor asks for due diligence on a company with well-documented public red flags. The company's claims are contradicted by public reporting, key executives have departed under scrutiny, and independent verification of core technology claims does not exist. The skill should surface red signals and refuse to recommend proceeding.

## Prompt

> /analyst:due-diligence Theranos Inc for investment consideration — pre-Series C health tech company claiming revolutionary blood testing technology

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Excellent research. Now I'll compile the structured report.

---

## Due diligence: Theranos Inc

**As of:** October 15, 2015 (last date before WSJ exposé; retrospective educational exercise)
**Scope:** Investment consideration
**Data type:** Public sources only

> **Note on framing:** Theranos raised Series C funding in 2006. The report is framed as a diligence exercise at the investor's point of maximum information — August/September 2015, after the HSV-1 FDA clearance announcement but before the Carreyrou exposé.

---

### Business fundamentals

**Funding history (all public):**

| Round | Date | Amount | Notable investors |
|---|---|---|---|
| Seed | June 2004 | ~$6M | Draper Fisher Jurvetson (Tim Draper) |
| Series A | February 2005 | $5.8M | Rupert Murdoch |
| Series B–C | 2006 | ~$37M | ATA Ventures and others |
| Growth | July 2010 | $45M | Crossed $1B valuation |
| Late-stage | Feb 2014 | $96.1M | Partner Fund Management ($17/share) |
| Late-stage | Oct 2014 | ~$250M | DeVos family ($100M), Walton family ($150M) |
| Late-stage | March 2015 | $348.5M | — |
| **Total raised** | | **~$1.3B** | |
| **Peak valuation** | June 2014 | **~$9–10B** | (Fortune, June 2014) |

**Revenue (publicly claimed vs. actual):**

- Claimed to investors, 2014: "$100 million in 2014, rising to $1 billion in 2015" (SEC complaint, March 2018)
- Actual 2014 revenue: just over $100,000 (SEC complaint, March 2018) — a 1,000:1 gap
- No financial statements were ever made public by Theranos; no external audit findings were published

**Headcount:** ~500 as of June 2014 (Fortune); peaked at ~800; cut 40% in October 2016

> **Private-data gap:** No audited P&L, no unit economics, no per-test margins are derivable from public sources. A real investment diligence would require access to audited financials, which Theranos refused to provide to most investors.

---

### Product signals

**What was claimed publicly:**

- Edison device runs "as many as 70+ tests" from a 25–50 microliter finger-stick sample
- Results delivered in hours vs. 2–3-day conventional lab turnaround
- Priced at or below Medicare reimbursement rates (~50–80% cheaper than Quest/LabCorp)
- Deployed in 41 Walgreens Wellness Centers (Arizona and California) as of mid-2014
- Claimed deployment on US military medevac helicopters (later confirmed false by SEC)

**Independent validation — a critical zero:**

As of October 2015, PubMed returned zero peer-reviewed publications from Theranos's own scientists validating the Edison platform. The company had operated for eleven years. Two independent academic critics had published formal commentary:

- Ioannidis, *JAMA*, February 17, 2015: Named Theranos explicitly for pursuing "stealth research" outside peer review; Theranos's legal team demanded a retraction — he declined. (*Source: JAMA, Vol. 313, Issue 7*)
- Diamandis, *Clinical Chemistry and Laboratory Medicine*, May 9, 2015: Concluded Theranos's claims were "exaggerated" and "speculative at best"; found no clinical validity data in review of 140+ Theranos patents. (*Source: CCLM, Vol. 53, Issue 7*)

**FDA regulatory status:**

- Clearances held as of October 2015: **one** — a herpes simplex virus type 1 (HSV-1) IgG test, cleared July 2, 2015. Theranos publicised this as a "major milestone." For context, this is among the simplest possible diagnostic tests; it is not the multi-panel Edison device.
- The remaining several hundred tests Theranos offered were classified as laboratory-developed tests (LDTs), exploiting an FDA enforcement discretion gap that exempted them from mandatory premarket review.

**Customer reviews:** No G2/Capterra profile existed for a B2B product. Consumer experience via Walgreens locations was not publicly aggregated; however, Glassdoor reviews of Theranos as an employer described it as operating "like a religious sect," with extreme NDA enforcement, alleged instruction to post positive reviews, and a company that "throws lawyers at anyone who they consider a threat." (*Source: BuzzFeed, Glassdoor reviews, 2015–2016*)

---

### Team

**Elizabeth Holmes — Founder & CEO:**

- Enrolled Stanford Chemical Engineering 2002; dropped out sophomore year (2003) at age 19 to found Theranos
- No degree in medicine, biology, clinical laboratory science, or diagnostics
- One Stanford professor (Phyllis Gardner, MD) reportedly rejected her original idea on scientific grounds; Gardner has publicly stated the idea would not work

**Ramesh "Sunny" Balwani — President & COO (joined 2009):**

- Background: B2B e-commerce (CommerceBid.com, sold 1999 for ~$228M); earlier sales roles at Lotus and Microsoft
- No biological sciences, medical device, or FDA regulatory background
- Personal relationship with Holmes — predating his employment at Theranos — was not disclosed to investors (later cited in criminal indictment and SEC complaint)

**Board composition (public record, October 2015):**

The full board consisted of George Shultz, Henry Kissinger, William Perry, Sam Nunn, Bill Frist (the only active medical professional), James Mattis, Gary Roughead, Dick Kovacevich, Riley Bechtel, and William Foege. Average age: ~80. No clinical laboratory specialists. No FDA regulatory experts. No diagnostics industry executives.

Fortune's own analysis (October 15, 2015, the day before the WSJ exposé) noted: board designed for political access and reputational signalling, not technical governance.

**Key scientific departure (Ian Gibbons):**

Ian Gibbons, Theranos's Chief Scientist, hired 2005, died May 23, 2013. His widow stated publicly that he had pressed Holmes on scientific accuracy, believed he was being asked to misrepresent the state of the technology, and faced an impending deposition in a patent dispute at the time of his death. The loss of the company's most senior scientist — with no public announcement about succession — was visible in public obituaries.

**Notable:** No specialist life sciences or diagnostics executives joined at any stage. Hiring was primarily Silicon Valley technologists.

---

### Market position

**Market size:** US clinical laboratory testing market approximately $60–70B annually (2013–2014). Quest Diagnostics revenue ~$7.1B (2013); LabCorp ~$5.7B (2012). Both incumbents growing in low single digits. (*Source: Quest Q3 2014 earnings release; LabCorp/G2 Intelligence analysis*)

**Theranos's claimed moat:**

1. Proprietary technology (Edison device) — unprecedented accuracy from micro-samples
2. Price: 50–80% cheaper than incumbents, priced at Medicare reimbursement rates
3. Distribution: embedded in Walgreens retail network
4. Speed: results in hours

**Moat assessment (public-data basis):**

- Technology moat: *unverifiable and later debunked* — no independent validation; company later confirmed to have been running most tests on commercial Siemens analyzers with diluted samples
- Price moat: *real but derivative* — depends entirely on the technology claims being true
- Distribution moat: *real* — Walgreens partnership was genuine; 41 locations operational
- Speed moat: *plausible* — centralized lab turnaround times do average 2–3 days

**Competitive comparison:** Even Theranos's most aggressive projection ($1B revenue in 2015) would have represented ~1.5% of the market — plausible penetration trajectory if the technology worked. The incumbents' competitive response (replication of a lower-cost point-of-care platform) would have been significant given their R&D budgets.

**No specialist VC investment:** No major life sciences VC (OrbiMed, Third Rock, NEA Healthcare, Versant) invested at any stage. These firms conduct technical diligence including clinical validation data review. Their systematic absence from the cap table is a signal the technology had not survived expert scrutiny.

---

### Risk factors

**Regulatory:**
- FDA inspection of Newark facility, August 25 – September 16, 2015: FDA Form 483 issued with documented violations including use of an unapproved Class II device (the "Nanotainer") reclassified to Class I to avoid clearance requirements; validation failures; quality audit failures. (This inspection was completed just weeks before the October 2015 WSJ article; the 483 was a public document.)
- Only one FDA clearance obtained after eleven years of operation
- LDT exemption strategy was legally precarious — FDA had communicated directly to Holmes that the devices required clearance

**Reputational:**
- Two peer-reviewed papers explicitly questioning Theranos's claims published in February and May 2015
- Company's legal response to academic criticism (demanding Ioannidis retract his JAMA paper) publicly reported
- Glassdoor reviews described extreme NDA enforcement, litigation culture, and suspected astroturfing

**Financial:**
- Revenue figures disclosed to investors were approximately 1,000× actual revenue (established post-collapse, but the refusal to share audited financials was itself a visible red flag)
- No public revenue milestones announced between rounds
- Partnership structure unusual: Walgreens was simultaneously a $40M creditor and primary distribution partner — creating incentive to suppress scrutiny

**Team/operational:**
- Founder and COO combined had zero clinical laboratory, medical device, or FDA regulatory experience
- Chief Scientist died in 2013 with no public succession announcement
- Board structurally incapable of evaluating technical claims

**Litigation (post-October 2015, for completeness):**
- Partner Fund Management lawsuit (October 2016): alleged "lies, material misstatements and omissions" covering $96.1M investment
- Walgreens lawsuit (November 2016): sought $140M; settled ~$30M
- SEC civil charges (March 2018): Holmes settled; Balwani did not
- Criminal convictions: Holmes (January 2022, 11 years 3 months); Balwani (July 2022, 12 years 11 months)

---

### Signal summary

| Signal | Status | Evidence |
|---|---|---|
| Team stability | 🔴 | Founder (no domain expertise), COO (no domain expertise), Chief Scientist died 2013 with no succession; board structurally unable to evaluate claims |
| Funding trajectory | 🟡 | Rounds increasing in size (green) but investor base entirely non-specialist; no life sciences VC at any stage (red) |
| Customer sentiment / product validation | 🔴 | Zero peer-reviewed publications after 11 years; two independent academic papers questioning claims (Feb & May 2015); one FDA clearance for a trivial test |
| Regulatory / legal exposure | 🔴 | FDA Form 483 issued September 2015; FDA had told Holmes devices required clearance; LDT exemption legally precarious; no clearances for core product |
| Revenue / financial transparency | 🔴 | No audited financials shared with investors or public; no disclosed revenue milestones between rounds; actual revenue ~$100K vs claimed ~$100M |
| Hiring velocity / expertise | 🔴 | No diagnostics executives hired at any seniority; Silicon Valley technology hiring with no clinical laboratory depth |
| Competitive moat | 🟡 | Distribution moat (Walgreens) real; technology moat entirely unverified and structurally unverifiable by investors |

**Verdict:** Do not invest. The technology moat — the entire basis of Theranos's valuation premium over incumbents — was unverifiable by design, with two peer-reviewed scientific critics in print, zero independent validation, and a regulatory posture specifically structured to avoid the scrutiny that would have resolved the question. Seven of the seven signal categories show red or qualified yellow, all of which were derivable from public sources by August 2015.

**Red flag escalation triggered (≥2 red signals):**

| Red signal type | Follow-on recommended |
|---|---|
| Regulatory and FDA findings | `/investigator:public-records` — full FDA 483 record, CMS inspection history, any state lab proceedings |
| Reputational concern + litigation culture | `/investigator:entity-footprint` — press timeline, legal filings, Glassdoor pattern analysis |
| Technology moat unverifiable | `/analyst:competitive-analysis` — LabCorp and Quest capabilities, whether incumbents could replicate claims if true |

---

**Note:** This is public-data diligence only. Legal, financial, and technical diligence requires direct access to private information — audited financials, laboratory validation data, cap table details, and board minutes — none of which Theranos disclosed to most investors, and the systematic refusal to disclose them was itself the most actionable red flag available.

---

### Sources

1. [SEC press release and complaint, March 14, 2018](https://www.sec.gov/newsroom/press-releases/2018-41) — Revenue figures (actual vs. claimed), regulatory timeline
2. [FDA Form 483, Theranos Newark CA, September 16, 2015](https://www.fda.gov/files/about%20fda/published/Theranos--Inc.--Newark--CA-483-Issued-09-16-2015.pdf) — Specific inspection violations
3. [Fortune cover profile, June 12, 2014](https://fortune.com/2014/06/12/theranos-blood-holmes/) — Headcount, product claims, absence of peer review noted without comment
4. [Fortune board analysis, October 15, 2015](https://fortune.com/2015/10/15/theranos-board-leadership/) — Board composition and expertise gaps
5. [Ioannidis, "Stealth Research," JAMA, February 17, 2015](https://jamanetwork.com/journals/jama/fullarticle/2110977) — First peer-reviewed academic challenge; Theranos's legal response
6. [Diamandis, "Theranos phenomenon: promises and fallacies," CCLM, May 9, 2015](https://pubmed.ncbi.nlm.nih.gov/26030792/) — Patent review finding no clinical validity data; technical critique
7. [Walgreens/Theranos partnership press release, September 9, 2013](https://www.businesswire.com/news/home/20130909005578/en/Theranos-Selects-Walgreens-as-a-Long-Term-Partner-Through-Which-to-Offer-Its-New-Clinical-Laboratory-Service) — Partnership structure and $40M loan
8. [Theranos CLIA waiver / HSV-1 clearance press release, July 16, 2015](https://www.businesswire.com/news/home/20150716005630/en/Theranos-Receives-CLIA-Waiver-Paving-the-Way-for-Greater-Accessibility-of-Health-Information-at-the-Time-and-Place-It-Matters) — Scope of the single FDA clearance
9. [Dark Daily on Clapper/Carreyrou, July 2019](https://www.darkdaily.com/2019/07/15/skeptical-missouri-pathologist-played-a-key-role-in-wall-street-journal-reporter-john-carreyrous-expose-of-medical-lab-test-company-theranos/) — Expert scepticism pathway from clinical community to WSJ
10. [QZ — how Safeway and Walgreens fell for Theranos](https://qz.com/2074304/how-safeway-and-walgreens-fell-for-the-theranos-pipe-dream) — Safeway partnership economics and structure
11. [Quest Diagnostics Q3 2014 earnings](https://newsroom.questdiagnostics.com/2014-10-23-Quest-Diagnostics-Reports-Third-Quarter-2014-Financial-Results) — Market size and incumbent revenue benchmarks
12. [BuzzFeed — seven biggest lies](https://www.buzzfeednews.com/article/stephaniemlee/theranos-elizabeth-holmes-sec-charges) — Claims vs. actuals, consolidated
13. [CBS News — Ian Gibbons widow](https://www.cbsnews.com/news/theranos-scientist-widow-elizabeth-holmes/) — Chief Scientist departure signal
14. [Crunchbase News — investors and board](https://news.crunchbase.com/health-wellness-biotech/theranos-elizabeth-holmes-trial-investors-board/) — Cap table composition and absence of specialist VCs
15. [MIT Sloan — four red flags](https://mitsloan.mit.edu/ideas-made-to-matter/4-red-flags-signaled-theranos-downfall) — Academic analysis of publicly visible warning signals

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.5/17.0 (97%) |
| Evaluated | 2026-05-01 |
| Target duration | 593747 ms |
| Target cost | $1.9532 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill states scope explicitly at the top — investment consideration, public data only | PASS | Report header states '**Scope:** Investment consideration' and '**Data type:** Public sources only' on lines 3–4 of the report. |
| c2 | Business fundamentals section flags the gap between claims and independently verifiable evidence | PASS | 'Revenue (publicly claimed vs. actual)' subsection shows claimed $100M vs actual ~$100K — a '1,000:1 gap' — sourced to the SEC complaint. The 'Private-data gap' note explicitly states no audited financials were derivable. |
| c3 | Team section notes executive departures or governance concerns from public reporting | PASS | Ian Gibbons death noted as a visible departure signal with no succession announcement. Board described as 'structurally incapable of evaluating technical claims' with average age ~80 and no clinical laboratory specialists. Balwani's undisclosed personal relationship cited from criminal indictment. |
| c4 | Signal summary contains at least two red signals from public sources | PASS | Signal summary table lists five 🔴 signals: Team stability, Customer sentiment/product validation, Regulatory/legal exposure, Revenue/financial transparency, and Hiring velocity/expertise — all with cited public sources. |
| c5 | When two or more red signals are present, skill routes to follow-on skills (public-records, corporate-ownership) | PASS | 'Red flag escalation triggered (≥2 red signals)' section explicitly routes to `/investigator:public-records` and `/investigator:entity-footprint` (plus `/analyst:competitive-analysis`). Public-records routing is present; entity-footprint serves as the entity/legal-structure follow-on. |
| c6 | Verdict does NOT recommend proceeding — red signals override positive indicators | PASS | Verdict states: 'Do not invest. The technology moat — the entire basis of Theranos's valuation premium — was unverifiable by design… Seven of the seven signal categories show red or qualified yellow.' Positive indicators (Walgreens distribution moat, funding trajectory) are noted but explicitly do not override the verdict. |
| c7 | The skill distinguishes between 'information unavailable' and 'information contradicts claims' in the signal assessment | PARTIAL | The 'Private-data gap' note distinguishes data simply unavailable ('No audited P&L…are derivable from public sources') from contradicted claims ('Technology moat: unverifiable and later debunked'). The distinction is present but informal — not consistently labeled across the signal summary table. |
| c8 | Revenue and technology claims are flagged as unverifiable from public data when no independent validation exists | PASS | 'Independent validation — a critical zero': 'PubMed returned zero peer-reviewed publications from Theranos's own scientists validating the Edison platform.' Technology moat labeled 'unverifiable and later debunked.' Revenue gap established from SEC complaint. |
| c9 | Output's scope at the top is explicit — investment-consideration diligence, public data only, with the caveat that Theranos has been the subject of extensive published reporting (WSJ Carreyrou, books, court cases) so the public record is unusually deep | PASS | Scope and data-type fields are explicit. The framing note references 'before the Carreyrou exposé' and litigation section covers post-2015 court outcomes. Fifteen cited sources include SEC complaint, FDA Form 483, criminal convictions, and multiple investigative outlets, demonstrating the unusually deep public record in practice. |
| c10 | Output's business fundamentals section flags the gap between Theranos's claims (revolutionary blood testing from finger-prick) and the independent verification record (no peer-reviewed validation, regulatory inspections finding the technology did not work as claimed) | PASS | 'Independent validation — a critical zero' subsection cites Ioannidis (JAMA 2015) and Diamandis (CCLM 2015) as explicit peer-reviewed challenges. FDA 483 violations listed. Market position notes company 'confirmed to have been running most tests on commercial Siemens analyzers with diluted samples.' |
| c11 | Output's team section notes the executive departures and governance concerns — board composition (high-profile but technology-naive members like Kissinger / Mattis / Shultz), CEO/founder removal, COO Sunny Balwani charged | PASS | Board section explicitly names Kissinger, Mattis, Shultz, Perry, Nunn with 'average age: ~80. No clinical laboratory specialists.' Balwani's 'criminal indictment' is cited in the team section. Holmes and Balwani convictions noted in litigation section. |
| c12 | Output's signal summary lists multiple RED signals — gap between claims and evidence (red), legal action (red — SEC charges and criminal trial), executive criminal liability (red — Holmes and Balwani both convicted), governance concerns (red — board lacked technical expertise) | PASS | Signal summary table shows five 🔴 rows. Regulatory/legal exposure 🔴 cites 'FDA Form 483 issued September 2015.' Revenue/financial transparency 🔴 notes the 1,000× gap. Team stability 🔴 notes 'Founder (no domain expertise), COO (no domain expertise)…board structurally unable to evaluate claims.' |
| c13 | Output's verdict is DO NOT PROCEED (or DECLINE) — red signals are decisive; positive signals (high valuation, prestigious investors) do NOT override the substantive concerns | PASS | Verdict: 'Do not invest.' The funding trajectory is rated 🟡 with explicit note that 'investor base entirely non-specialist; no life sciences VC at any stage (red).' Positive Walgreens distribution moat is rated 🟡 but does not influence the final verdict. |
| c14 | Output routes to follow-on skills — `/investigator:public-records` for court filings (the SEC complaint, criminal trial transcripts), `/investigator:corporate-ownership` for the entity structure / disposition | PARTIAL | Routes to `/investigator:public-records` (FDA 483 record, CMS inspection history) — present. Routes to `/investigator:entity-footprint` for press timeline and legal filings — NOT `/investigator:corporate-ownership` for entity structure/disposition. One of two required specific skill routes is missing. |
| c15 | Output distinguishes 'information unavailable' (e.g. private investor return data) from 'information contradicts claims' (e.g. WSJ reporting and lab inspection results contradict the technology claims) — both are findings but they're qualitatively different | PASS | 'Private-data gap' box explicitly marks things unavailable: 'No audited P&L…are derivable from public sources. A real investment diligence would require access to audited financials.' Technology claims are separately characterized as 'unverifiable and later debunked' and revenue as a '1,000:1 gap' — contradicted, not merely missing. |
| c16 | Output flags Theranos's revenue and technology claims as CONTRADICTED state (not just unverified) — and notes that the independent verification that DID happen contradicted the claims | PASS | Technology moat labeled 'unverifiable and later debunked — no independent validation; company later confirmed to have been running most tests on commercial Siemens analyzers.' Revenue actual (~$100K) explicitly contradicts claimed (~$100M) per SEC complaint. Both are framed as contradicted, not merely unknown. |
| c17 | Output uses Theranos as a case where 'do not proceed' is unambiguous — the skill demonstrates it can recognise a clear red verdict, not equivocate | PASS | Verdict section states: 'Do not invest' followed by 'Seven of the seven signal categories show red or qualified yellow.' No hedging language, no 'consider with caveats' framing. The red flag escalation table further reinforces the decisiveness. |
| c18 | Output addresses the timing — when this diligence might have run (pre-Carreyrou-WSJ, post-WSJ, post-trial); the public record changed dramatically over time and that affects the diligence trajectory | PARTIAL | Framing note anchors the report 'As of October 15, 2015… before the Carreyrou exposé' and explicitly frames it as 'investor's point of maximum information.' Litigation section is labeled 'post-October 2015, for completeness.' However, the output does not discuss how the diligence trajectory would differ or escalate post-WSJ or post-trial — the timing context is acknowledged but not developed into a trajectory analysis. |

### Notes

The output is an exceptionally thorough due-diligence report that earns near-perfect scores. It explicitly scopes the exercise, surfaces the 1,000× revenue gap, details the board's technical incapacity, and delivers an unambiguous 'Do not invest' verdict. The distinction between unavailable and contradicted information is present throughout, though informal. The only material gap is in the follow-on skill routing: `/investigator:corporate-ownership` was not invoked — the output substituted `/investigator:entity-footprint` — resulting in a PARTIAL for c14. The timing section (c18) acknowledges the pre-Carreyrou framing but does not develop how the diligence trajectory would change post-WSJ or post-conviction, capping it at PARTIAL per the ceiling. All other criteria are fully satisfied.
