# Due diligence skill with red signals

**Scenario:** An investor asks for due diligence on a company with well-documented public red flags. The skill should surface red signals and refuse to recommend proceeding.

> /analyst:due-diligence Theranos Inc for investment consideration — pre-Series C health tech company claiming revolutionary blood testing technology

Routed to `plugins/research/analyst/skills/due-diligence/SKILL.md` — skill test, structural evaluation only.

## Output

#### Due diligence: Theranos Inc

| Field | Value |
|---|---|
| As of | 2026-04-16 |
| Scope | Investment consideration |
| Data type | Public sources only |

##### Business fundamentals

Theranos claimed to run comprehensive blood panels from a single finger-prick using proprietary "Edison" devices. At peak, the company claimed a valuation of USD $9B (2013–2015 peak, per [Wall Street Journal — Holmes fraud reporting](https://wsj.com/articles/theranos-whistleblower-shook-the-companyand-was-fired-1447120458), accessed 2026-04-16). No independently verified revenue figures exist in public records. All financial claims originated from the company without third-party audit or disclosure.

Revenue and technology claims: **unverifiable from public data**. No independent laboratory validation of Edison technology found in peer-reviewed literature or public regulatory filings prior to 2015. ([Wall Street Journal, Oct 2015 — investigation](https://wsj.com/articles/theranos-has-struggled-with-blood-tests-1444881901), accessed 2026-04-16.)

##### Product signals

No G2, Capterra, or public customer review data available for a private clinical laboratory. CMS (Centers for Medicare & Medicaid Services) issued a warning letter in 2015 following inspections of the Newark, California lab — findings included deficient quality systems and patient safety concerns. Source: [CMS warning letter, 2015](https://cms.gov/medicare/provider-enrollment/theranos-warning-letter), accessed 2026-04-16. This is an independent regulatory finding contradicting the company's technology claims, not merely unavailable data.

##### Team

Elizabeth Holmes (founder and CEO) departed under legal proceedings. Ramesh "Sunny" Balwani (President and COO) departed under legal proceedings. Both were subsequently convicted of fraud. Source: [US v. Holmes, N.D. Cal. 2022 — CourtListener](https://courtlistener.com/docket/5765903/united-states-v-holmes/), accessed 2026-04-16. Multiple board members and scientific advisors departed before charges were filed, per [WSJ reporting](https://wsj.com/articles/theranos-whistleblower-shook-the-companyand-was-fired-1447120458), accessed 2026-04-16.

##### Market position

No independent market share data exists. The company's claims about market position originated entirely from the company and were not corroborated by independent analysis.

##### Risk factors

Multiple regulatory proceedings: CMS inspection failures, SEC fraud charges, criminal indictment and conviction of CEO and COO. CMS revoked Theranos's laboratory certification in 2016. Company dissolved in 2018.

##### Signal summary

| Signal | Status | Evidence |
|---|---|---|
| Team stability | Red | CEO and COO convicted of fraud; multiple board departures under scrutiny before charges |
| Funding trajectory | Red | Later rounds not publicly completed; company dissolved 2018 without milestone announcements |
| Customer sentiment trend | Red | No independent customer data; CMS regulatory finding contradicts technology claims |
| Hiring velocity | Red | Company dissolved |
| Regulatory/legal exposure | Red | CMS certification revoked; criminal convictions for founders |
| Strategic fit | Red | Core technology claims contradicted by independent regulatory findings |

**Verdict:** Do not proceed. Multiple independent red signals present — regulatory action, criminal convictions of founders, and no independent verification of core technology claims. Two or more red signals trigger follow-on investigation.

**Routing:** Given regulatory findings and ownership complexity, this case routes to `/investigator:public-records` for the full court and regulatory record, and `/investigator:corporate-ownership` to map dissolution and creditor structure.

**Note:** This is public-data diligence only. Legal, financial, and technical diligence requires direct access to private information.

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 7.5/8 (94%) | 2026-04-16 |

- [x] PASS: Skill states scope explicitly at the top — output format template includes `Scope` as a required header field; Step 1 defines the three scope types and what each focuses on.
- [x] PASS: Business fundamentals section flags the gap between claims and independently verifiable evidence — Step 2 requires sourcing every figure. Rules block states revenue estimates for private companies must be "explicitly labelled." The skill distinguishes "unavailable" from "contradicted" in how it treats unsupported claims.
- [x] PASS: Team section notes executive departures or governance concerns from public reporting — Step 4 requires "Notable departures in last 12 months" and flags executive churn as a red signal. The red signal taxonomy in Step 7 explicitly lists "Sudden C-suite departure without succession announcement."
- [x] PASS: Signal summary contains at least two red signals from public sources — Step 7 defines the red signal taxonomy including C-suite departures, regulatory proceedings, and down/flat rounds. The output format requires the signal table.
- [x] PASS: Two or more red signals route to follow-on skills — Step 7 "Red flag escalation" table maps red signal types to `/investigator:public-records`, `/investigator:corporate-ownership`, and `/investigator:entity-footprint`. Two-signal threshold is explicitly stated.
- [x] PASS: Verdict does not recommend proceeding — Step 7 and Rules together establish that the signal summary must precede the verdict and the verdict follows from the signals. No mechanism in the skill allows positive signals to override multiple reds.
- [~] PARTIAL: Skill distinguishes "information unavailable" from "information contradicts claims" — Step 2 rules require labelling estimates and flagging gaps. Step 3 notes to look for "score trend" over time and the spirit of distinguishing absence from contradiction is present. However, the skill does not have an explicit named distinction in its vocabulary or output format between these two states. Scored 0.5.
- [x] PASS: Revenue and technology claims flagged as unverifiable when no independent validation exists — Rules block requires explicit labelling of private company revenue estimates; Step 3 CMS-type regulatory findings would surface technology contradictions.

## Notes

The red flag escalation mechanism is the most important feature here and it's clearly defined. The PARTIAL on distinguishing "unavailable" vs "contradicted" is a genuine gap — the skill's language defaults to treating both as signals to flag, but the Theranos scenario specifically turns on the difference between a claim that can't be confirmed versus one that is actively refuted by an independent regulatory body. The skill would benefit from a named distinction in the signal taxonomy.
