# Deep Research

Scenario: A policy consultant needs exhaustive research on Australia's Critical Infrastructure Act 2021 sector-by-sector impact, for a submission to a government inquiry.

## Prompt

> /analyst:deep-research Impact of Australia's Security of Critical Infrastructure Act 2021 on private sector obligations — specifically what changed for the energy and data storage sectors, and what is contested or unclear.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I now have sufficient data across 6 passes. Compiling the full report.

---

## Deep research: Impact of Australia's Security of Critical Infrastructure Act 2021 on private sector obligations — energy and data storage sectors

**Date:** 2026-05-01
**Passes completed:** 6
**Sources reviewed:** 28+ (primary legislation, government factsheets, law firm analysis, industry guides, parliamentary records, regulatory vendor commentary)

---

### Domain map

**Authoritative sources**
- *Primary legislation*: Security Legislation Amendment (Critical Infrastructure) Act 2021 (SLACI); Security Legislation Amendment (Critical Infrastructure Protection) Act 2022 (SLACIP); Security of Critical Infrastructure and Other Legislation Amendment (Enhanced Response and Prevention) Act 2024 (ERP Act)
- *Regulator*: Cyber and Infrastructure Security Centre (CISC), within Department of Home Affairs — issues rules, manages the Register of Critical Infrastructure Assets, and enforces obligations
- *Operational security*: Australian Signals Directorate (ASD) — receives incident reports, provides cyber assistance for SoNS
- *Energy sector regulator*: Australian Energy Market Operator (AEMO) — developed the sector-specific Australian Energy Sector Cyber Security Framework (AESCSF)
- *Financial sector co-regulator*: Reserve Bank of Australia (RBA) — co-administers SOCI for financial sector entities
- *Parliamentary oversight*: Parliamentary Joint Committee on Intelligence and Security (PJCIS) — has conducted multiple advisory reports on the SOCI reform bills

**Key entities**
- CISC (Cyber and Infrastructure Security Centre) — rule-maker and registrar
- ASD — operational cyber response and SoNS enhanced obligations
- Home Affairs Secretary/Minister — exercises intervention and direction powers
- AEMO — energy market operator; itself a regulated entity and framework co-developer
- Law Council of Australia — primary legal profession voice on contested provisions
- Private sector industry groups — made submissions flagging cost and proportionality concerns

**Contested terrain**
- Proportionality and accountability of government intervention powers (no merits review)
- Scope of "business critical data" and "material risk" thresholds for data storage
- SoNS designation secrecy and its downstream obligations
- Boundary between responsible entity and third-party data service provider
- CIRMP "one-size-fits-all" approach across sectors of unequal maturity

**Temporal scope**
Four distinct eras: pre-2021 (narrow foreign ownership register, 4 sectors); 2021–2022 (scope expansion, government powers); 2023–2024 (CIRMP rules in force, annual reporting begins, SoNS enhanced obligations); 2025–present (ERP Act data storage rules, CISC moves from education to active audit compliance).

---

### Findings

#### 1. What the 2021 amendment actually changed

The Security Legislation Amendment (Critical Infrastructure) Act 2021 (SLACI Act), receiving Royal Assent on 2 December 2021, was the first of a two-part reform. Its core effect was **structural expansion plus emergency powers**:

- Expanded critical infrastructure sectors from **4 to 11** (subsequently 22 asset classes)
- Added new sectors including communications, data storage or processing, defence industry, education, financial services, food and grocery, healthcare, space technology, transport, and water/sewerage — alongside the original electricity, gas, water, ports
- Introduced **"government assistance measures"**: three escalating intervention mechanisms — information-gathering directions, action directions, and ASD intervention requests — that the Minister could authorize during significant cyber incidents
- Created the concept of **"Systems of National Significance" (SoNS)**: designated privately by the Minister, triggering an additional tier of enhanced obligations

The second bill — SLACIP Act, April 2022 — added the mandatory Critical Infrastructure Risk Management Program (CIRMP) obligations and formalised the SoNS enhanced cyber security obligations (ECSOs).

**[High confidence]** — confirmed across Allens, MinterEllison, Gadens, Pinsent Masons, and multiple secondary sources.

#### 2. Energy sector: what changed

Before 2021, the SOCI Act required owners of electricity networks and gas pipelines to register ownership and control details — primarily a foreign ownership transparency mechanism. The 2021–2022 reforms transformed this into a **positive obligation framework**.

**New energy asset classes covered** (sourced from CIRMP rules and CISC sector guidance):
- Critical electricity assets: generation above capacity thresholds, transmission networks, distribution networks, electricity market operator systems
- Critical gas assets: processing facilities, transmission pipelines (nameplate >200 TJ/day on Eastern gas market), distribution networks, **plus control rooms and any other asset required to operate a gas transmission pipeline** (a definitional expansion via SLACI)
- Critical energy market operator assets: broadened to cover both "markets" and "systems" operated by AEMO
- Critical liquid fuel assets: liquid fuel supply chain assets

**CIRMP obligations** (CIRMP Rules, commenced 17 February 2023):
- Must adopt a written CIRMP addressing at minimum: cyber/information security, personnel, supply chain, and physical security hazards
- Must identify all material risks, set out minimisation/elimination/mitigation steps
- No prescribed format, but must be board-approved
- Must comply with one of five designated cyber frameworks from 17 August 2024:
  - Essential Eight (ML1), NIST CSF, C2M2 (MIL1), AESCSF (Profile 1), AS ISO/IEC 27001
  - Or "an equivalent framework" (term undefined)
- Annual report to sector regulator within 90 days of financial year end (first due July–September 2024)

**SoNS enhanced obligations** (for entities designated by Minister):
168 entities designated as of September 2023. Enhanced obligations include: developing cyber incident response plans; running cyber exercises; conducting vulnerability assessments; providing near-real-time system information to ASD.

**Proposed 2025–2026 further uplift** (under CIRMP Rules consultation, February 2026 deadline): energy operators and electricity/gas assets are in the high-risk class facing proposed additional obligations — foreign ownership/control risk documentation, vendor-of-concern process, and cyber framework uplift to **maturity level 2** (AESCSF Profile 2 or C2M2 MIL2) by June 2028.

**[High confidence]** — confirmed by Allens, MinterEllison, Industrial Defender, Nozomi Networks, Dragos, AEMO annual report reference, Kinatico, and CISC sector search results.

#### 3. Data storage sector: what changed

The data storage or processing sector was **entirely new** under the 2021 reforms — it did not exist as a regulated sector under the original SOCI Act 2018.

**Initial 2021 framework** (SLACI Act, operationalised through SLACIP Act and CIRMP Rules 2023):
- Sector defined as entities that "provide data storage or processing services" by controlling "physical infrastructure or computing platforms": enterprise data centres, managed services data centres, colocation data centres, cloud data centres
- Responsible entities must register operational/ownership details
- Cyber incident reporting: 12 hours for significant availability impact; 72 hours for other relevant impacts
- CIRMP obligations: covering all four hazard categories
- **Notification obligation** (s.12F(3)): responsible entities must notify their third-party data storage/processing providers that they are storing or processing "business critical data" for a critical infrastructure asset

**2024 ERP Act expansion** (November 2024, in force 29 November 2024 / 29 May 2025 for CIRMP):
This was the most significant shift for the data storage sector since the original expansion. The ERP Act **deems certain data storage systems owned by responsible entities to form part of the CI asset itself** — not as a separate regulated sector, but incorporated into the primary asset's compliance obligations.

A data storage system qualifies if:
1. The responsible entity owns or operates it
2. It is connected to their critical infrastructure asset
3. It stores or processes "business critical data"
4. A hazard affecting the system creates material risk of relevant impact on the primary asset

**Business critical data** (s.5 SOCI Act) covers:
- Personal information of 20,000+ individuals
- R&D data relating to the CI asset
- "Information relating to any systems needed to operate a critical infrastructure asset"
- Operational information necessary for the asset's functioning
- Risk management and business continuity documentation

The practical effect: energy operators, for instance, must now audit whether their internally-managed data storage systems (containing operational data, network designs, encryption keys, SCADA data) fall under these expanded definitions.

**April 2025 CIRMP Rules amendment**: Formally requires CIRMP holders to include risk identification and management for qualifying data storage systems within their programs. In force 4 April 2025; CIRMP integration required from 30 May 2025.

**Hosting Certification Framework carve-out**: Providers holding a "strategic-level" hosting certification under the Hosting Certification Framework are exempt from the CIRMP requirement but must submit annual hazard impact reports within 90 days of financial year end.

**[High confidence for core framework]** — confirmed by Allens, LK Law, Pinsent Masons, Ashurst, Clayton Utz, Pentagram Advisory, Macquarie Data Centres, and Gadens.

#### 4. Enforcement landscape

- Civil penalty for failing to adopt/maintain CIRMP: **$275,000 per day** (1,000 penalty units at $275/unit)
- Civil penalty for failing to comply with CIRMP variation direction: **$391,250**
- Civil penalty for failure to register: $11,100 per case
- Telecommunications-specific penalties under ERP Act: up to **$2.3 million**
- CISC conducted **trial audits** in Q3/Q4 2023–24; regular compliance audit activities commenced from 2024–25
- No public enforcement actions (infringement notices, penalties) have been identified as of the research date — compliance phase is still early-stage
- CISC has stated it is shifting from "education and awareness" to actively driving compliance in 2024–25

**[Medium confidence]** — confirmed by Kinatico and AICD commentary; no CISC annual enforcement report found in public sources.

---

### Entity confidence summary

| Entity / Claim | Score | Evidence | Contradictions |
|---|---|---|---|
| SLACI Act expanded sectors from 4 to 11, Royal Assent 2 Dec 2021 | **High** | Allens, MinterEllison, Gadens, Pinsent Masons, CISC search results | None |
| CIRMP Rules commenced 17 February 2023 | **High** | MinterEllison, Industrial Defender, multiple secondary sources | None |
| Energy sector includes control rooms/operational assets of gas pipelines (expanded definition) | **High** | Allens primary analysis | None found |
| 168 SoNS entities as of September 2023 | **Medium** | Dragos, Nozomi Networks (secondary vendors); no CISC primary source confirmed directly | No contradictions but no independent primary source |
| CIRMP annual report first due July–September 2024 | **High** | MinterEllison, Kinatico, Amstelveen (CIRMP practitioner report) | None |
| ERP Act data storage systems deemed part of CI asset (4-part test) | **High** | Pinsent Masons, Ashurst, Clayton Utz, LK Law, Pentagram Advisory | None |
| Business critical data includes "information relating to any systems needed to operate a CI asset" | **High** | Pentagram Advisory (citing s.5 SOCI Act); Clayton Utz | None |
| April 2025 CIRMP Rules amendment covering data storage | **High** | LK Law (April 2025), Clayton Utz (April 2025) | None |
| 168 SoNS entities figure | **Medium** | Dragos/Nozomi (vendor secondary); no government primary source confirmed | — |
| "Equivalent framework" undefined (creating compliance ambiguity) | **Medium** | Multiple practitioner guides note flexibility; no authoritative interpretation found | Some sources treat as uncontroversial flexibility |
| No merits review for government intervention powers | **High** | PJCIS reports (cited in Allens, MinterEllison); Law Council submission referenced | Government position: safeguards in proportionality and technical feasibility requirements |
| CISC moved to active compliance auditing from 2024–25 | **Medium** | Kinatico (compliance vendor); no CISC primary source confirmed | — |
| No public enforcement actions to date | **Low** | Absence of evidence across all sources searched; could exist but not publicised | — |
| Proposed cyber uplift to ML2 by June 2028 for energy | **Medium** | Ashurst (CIRMP consultation coverage); still in consultation as of Feb 2026 | Not yet enacted — contested in consultation |

---

### Contested findings

#### A. Government intervention powers: no merits review

**Position 1 — Government and CISC**: The existing safeguards within the SOCI Act are sufficient: directions must be "reasonably necessary and proportionate" and "technically feasible." The speed of cyber incidents makes a merits review process unworkable. Government assistance powers are a last resort, with the Minister required to authorise each use.

**Position 2 — Law Council of Australia, PJCIS (both 2021 and 2022 reports)**: Merits review of government decisions to issue action directions and intervention requests is constitutionally appropriate and legally required to maintain the rule of law. Without it, entities directed to act (or to permit ASD access to their systems) have no mechanism to challenge the decision except judicial review, which is slower and narrower in scope. The PJCIS raised this in both advisory reports. Parliament declined to act on the recommendation each time.

**Status**: Unresolved. The ERP Act (2024) expanded government powers to all-hazards (beyond cyber) without adding review mechanisms. The gap between the government's position and the Law Council/PJCIS remains open.

#### B. SoNS designation: secret process, asymmetric obligations

**Position 1 — Government**: Designation of an asset as a System of National Significance may itself be sensitive information. Secrecy prevents adversaries from knowing which assets face the highest level of scrutiny. Designated entities are notified through a consultation process before final designation.

**Position 2 — Industry/legal commentary**: Third parties dealing with a SoNS-designated entity cannot know that enhanced obligations apply. Entities designated as SoNS cannot publicly disclose it. This creates opacity in supply chains and makes it difficult for boards and investors to assess the full regulatory burden. There is also no transparent criteria for what triggers SoNS designation.

**Status**: Contested but not formally litigated. The framework remains unchanged on this point.

#### C. "Business critical data" scope and "material risk" threshold

**Position 1 — Government/CISC**: The definition is intentionally broad to ensure responsible entities cannot simply exclude data from obligations through structural choices. "Information relating to any systems needed to operate a critical infrastructure asset" is intended to capture operational technology data, network configurations, and SCADA data that are genuinely critical to asset function.

**Position 2 — Industry practitioners (Pinsent Masons, Allens, Ashurst)**: The definition is potentially very wide — nearly any data used in operating a CI asset could qualify. The "material risk" threshold for when a data storage system is deemed part of a CI asset lacks a bright-line test, requiring case-by-case assessment. This creates compliance ambiguity during the implementation window, particularly for large organisations with complex IT estates. Allens specifically noted the data storage definitions "remain likely to capture a very broad range of services despite amendments."

**Status**: Genuinely unresolved. Regulators have not yet issued interpretive guidance on where "material risk" begins. The first compliance deadline under the expanded rules was May 2025 — enforcement experience will determine how this is interpreted in practice.

#### D. CIRMP "one-size-fits-all" approach

**Position 1 — Government**: Principles-based rules are intentionally flexible, allowing entities to adopt the most appropriate framework for their sector and maturity level. The choice of cyber framework (five options plus "equivalent") demonstrates this.

**Position 2 — Industry (reflected in Ashurst CIRMP consultation coverage, PJCIS 2022 report)**: The same framework requirements applying across sectors of vastly different capability, resourcing, and maturity — from a suburban electricity distributor to a major bank — imposes disproportionate costs on smaller or less-mature entities. PJCIS 2022 noted the "potential costs for establishing and implementing Risk Management Programs is considerable for some organisations." The proposed ML2 uplift (energy, June 2028) is described by practitioners as "non-trivial."

**Status**: Ongoing tension. The consultation on proposed CIRMP Rules amendments (open until February 2026) indicates the government is still calibrating sector-specific requirements.

#### E. Third-party cloud provider obligations: responsible entity vs. service to CI asset

**Position identified (Pinsent Masons, Allens)**: The boundary between (a) a cloud provider that is itself a "responsible entity" for a critical data storage or processing asset, and (b) a cloud provider whose services form part of a client's primary CI asset (triggering client's CIRMP but not provider's own registration), is not clearly defined. Both can apply simultaneously. A major cloud provider serving multiple CI sectors may be a responsible entity for some obligations (registration, incident reporting) while simultaneously being subject to client notification obligations under s.12F(3) for others.

**Government position (not explicitly articulated in public sources found)**: The distinctions are addressed by the definitions in the SOCI Act and accompanying rules; the Hosting Certification Framework provides a voluntary pathway for providers seeking clarity.

**Status**: Unverified as fully resolved. No definitive CISC guidance found that draws a clear line for multinational hyperscale cloud providers.

---

### Source verification

| Source | URL live | Date confirmed | Venue/type |
|---|---|---|---|
| Allens — "Full spectrum of amendments" | Yes | April 2022 | Major Australian law firm analysis |
| MinterEllison — CIRMP requirements in effect | Yes | 2023 | Major Australian law firm analysis |
| Gadens — SLACI Act 2021 analysis | Yes | December 2021 | Australian law firm analysis |
| Ashurst — CIRMP proposed changes | Yes | 2025 (consultation open to Feb 2026) | Major Australian law firm analysis |
| Pinsent Masons — 2024 amendments explained | Yes | December 2024 | International law firm (Out-Law) |
| Clayton Utz — ERP Act (April 2025) | Yes | April 2025 | Major Australian law firm analysis |
| LK Law — New SOCI Rules, data storage | Yes | April 2025 | Australian law firm analysis |
| Pentagram Advisory — business critical data | Yes | Late 2024 | Australian regulatory advisory firm |
| Macquarie Data Centres — SOCI guide | Yes | 2023 | Industry participant (data centre operator) |
| Industrial Defender — CIRMP latest | Yes | 2024 | OT security vendor (treat as medium authority) |
| Kinatico — compliance 2025 | Yes | 2025 | Compliance software vendor (treat as low-medium authority) |
| Law Council of Australia — SLACIP submission | Yes (landing page only; PDF not accessible) | 2022 | Peak legal profession body — High authority |
| CISC (cisc.gov.au) factsheets and sector pages | No (403 errors) | — | Primary regulator — would be High authority if accessible |
| Home Affairs — SLACIP Bill page | Yes (search result) | 2022 | Primary government source |
| PJCIS recommendations | Cited across multiple sources | 2021, 2022 | Parliamentary committee — High authority |
| Dragos — SOCI Act blog | Yes (search result) | 2023 | OT security vendor (Medium authority for factual claims) |
| Nozomi Networks — SOCI Act blog | Yes (search result) | 2023 | OT security vendor (Medium authority) |

---

### Gap analysis

| Gap | Category | Access route |
|---|---|---|
| CISC primary factsheets and sector guidance (cisc.gov.au returned 403 for all PDF and sector pages) | Not yet public / Access restriction | Direct access to cisc.gov.au; may require non-automated browser with cookies accepted |
| CISC annual compliance report — aggregate data on how many entities have registered, submitted CIRMPs, reported incidents | Not yet public | CISC annual reports (if published); possible via Freedom of Information request to Department of Home Affairs |
| ASD threat reports citing SOCI-covered entities — incident volumes, sector breakdown | Not yet public (classified or withheld) | ASD Annual Cyber Threat Report (partially public); classified detail behind government access |
| Full text of Law Council of Australia's SLACIP Bill submission (specific contested provisions) | Paywall / PDF not crawlable | Download from lawcouncil.au directly |
| Enforcement actions under SOCI Act (any penalty notices, infringement notices issued) | Not yet public | CISC/Home Affairs media releases; Federal Court registry if any civil proceedings commenced |
| SoNS designation list — which entities are designated | Genuinely unknown (secrecy by design) | Not publicly disclosed; only accessible to designated entities and government |
| CIRMP Rules consultation submissions (February 2026) — industry positions on proposed ML2 uplift | Not yet public (consultation period open) | Home Affairs website post-consultation; submissions may be published |
| Interpretive guidance on "material risk" threshold for data storage system inclusion | Not yet public | CISC has not issued binding guidance as of research date; expected as audit experience accumulates |
| Enforcement interpretation of "equivalent framework" (s.8 CIRMP Rules) | Not yet public / Requires primary research | CISC guidance; test cases through audit process |
| Hyperscaler-specific compliance positions (AWS, Azure, Google Cloud AU) | Not yet public / Primary research needed | Industry submissions; direct disclosure by providers; regulatory correspondence |

---

### Sources

1. [Allens — The full spectrum of amendments to the Security of Critical Infrastructure regime](https://www.allens.com.au/insights-news/insights/2022/04/The-full-spectrum-of-amendments-to-the-Security-of-Critical-Infrastructure-regime/) — Law firm primary analysis — High authority
2. [MinterEllison — SOCI risk management program requirements now in effect](https://www.minterellison.com/articles/soci-risk-management-program-requirements-now-in-effect) — Law firm primary analysis — High authority
3. [MinterEllison — SOCI Round 2: law reform now enacted](https://www.minterellison.com/articles/soci-round-2-law-reform-now-enacted) — Law firm analysis — High authority
4. [Gadens — Security Legislation Amendment (Critical Infrastructure) Act 2021](https://www.gadens.com/legal-insights/security-legislation-amendment-critical-infrastructure-act-2021/) — Law firm analysis — High authority
5. [Ashurst — SOCI Act consultation: proposed CIRMP Rule changes](https://www.ashurst.com/en/insights/soci-act-consultation-what-the-proposed-changes-to-the-cirmp-rules-might-mean-for-you/) — Law firm analysis — High authority
6. [Ashurst — Changes to the SOCI Act are on the horizon](https://www.ashurst.com/en/insights/changes-to-the-soci-act-are-on-the-horizon/) — Law firm analysis — High authority
7. [Pinsent Masons — Australia's latest SOCI Act amendments explained](https://www.pinsentmasons.com/out-law/analysis/security-critical-infrastructure-act-amendments-explained) — Law firm (Out-Law) — High authority
8. [Clayton Utz — Enhancing response and prevention powers, critical infrastructure assets](https://www.claytonutz.com/insights/2025/april/enhancing-response-and-prevention-powers-in-relation-to-critical-infrastructure-assets) — Law firm analysis — High authority
9. [LK Law — New SOCI Rules Go Live: data storage systems and telco assets](https://www.lk.law/2025/04/new-soci-rules-go-live-changes-for-data-storage-systems-and-telco-assets/) — Law firm analysis — High authority
10. [Pentagram Advisory — SOCI Act Update: Managing Business Critical Data](https://pentagramadvisory.com.au/latest-amendments-to-the-security-of-critical-infrastructure-act-2018-a-major-shift-impacting-critical-infrastructure-owners-and-operators/) — Regulatory advisory — Medium-high authority
11. [Macquarie Data Centres — The SOCI Act Deadline is Here (2023)](https://www.macquariedatacentres.com/blog/soci-act-guide/) — Industry participant — Medium authority
12. [Industrial Defender — The Latest with Australia's SOCI Act and CIRMP](https://www.industrialdefender.com/blog/australia-soci-cirmp) — OT security vendor — Medium authority
13. [Kinatico — A Renewed Focus for the SOCI Act in the 2025 Financial Year](https://kinatico.com/a-renewed-focus-for-the-soci-act-in-the-2025-financial-year/) — Compliance vendor — Low-medium authority
14. [CISC — Security of Critical Infrastructure Act 2018](https://www.cisc.gov.au/legislation-regulation-and-compliance/soci-act-2018) — Primary regulator (site returned 403 during research) — High authority when accessible
15. [Home Affairs — SLACIP Bill 2022](https://www.homeaffairs.gov.au/reports-and-publications/submissions-and-discussion-papers/slacip-bill-2022) — Primary government source — High authority
16. [Law Council of Australia — Submission on SLACIP Bill 2022](https://lawcouncil.au/resources/submissions/review-of-the-security-legislation-amendment-critical-infrastructure-protection-bill-2022) — Peak legal body — High authority
17. [Dragos — SOCI Act: Strengthening Australia's Critical Infrastructure Security](https://www.dragos.com/blog/soci-act-strengthening-australias-critical-infrastructure-security) — OT security vendor — Medium authority
18. [Nozomi Networks — What Is Australia's Security of Critical Infrastructure Act?](https://www.nozominetworks.com/blog/australian-security-of-critical-infrastructure-soci-act) — OT security vendor — Medium authority
19. [Holding Redlich — Security of Critical Infrastructure Act: the past, present and future](https://www.holdingredlich.com/security-of-critical-infrastructure-act-the-past-present-and-future) — Law firm — High authority
20. [UpGuard — SOCI Act Explained: Compliance Rules & Requirements](https://www.upguard.com/blog/soci-act-2018) — Cybersecurity vendor — Low-medium authority
21. [Fivecast — The SOCI Act: Key Compliance Dates in 2024](https://www.fivecast.com/blog/the-soci-act-key-compliance-dates-in-2024/) — Security vendor — Low-medium authority
22. [AICD — New cyber security and privacy regulation](https://www.aicd.com.au/risk-management/framework/cyber-security/new-cyber-security-and-privacy-regulation.html) — Director body — Medium authority
23. [Dentons — Operationalising SOCI Act compliance for grid-scale BESS projects](https://www.dentons.com/en/insights/alerts/2025/september/25/operationalising-soci-act-compliance-for-grid-scale-bess-projects) — Law firm (403 at access time) — High authority when accessible

## Evaluation

| Field | Value |
|---|---|
| Verdict | PARTIAL |
| Score | 14.0/18.0 (78%) |
| Evaluated | 2026-05-01 |
| Target duration | 423755 ms |
| Target cost | $1.2890 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill completes all six passes — domain mapping, primary source sweep, secondary source sweep, entity scoring, URL verification, and gap analysis | PASS | Output states 'Passes completed: 6' and contains distinct sections for all six: Domain map, Findings (source sweeps), Entity confidence summary table, Contested findings, Source verification table, and Gap analysis table. |
| c2 | Domain mapping identifies the authoritative sources (DISR, ACSC, parliamentary committee reports) before beginning evidence collection | PASS | Domain map lists CISC (within Department of Home Affairs), ASD (functional successor to ACSC for cyber), and PJCIS ('Parliamentary oversight: Parliamentary Joint Committee on Intelligence and Security (PJCIS)') before findings begin. DISR is absent but is not the primary SOCI regulator. |
| c3 | Primary sources are fetched and read directly — not cited via summaries or secondary references | FAIL | Source verification table shows CISC factsheets returned 403 errors ('No (403 errors)') and Law Council PDF was 'not accessible'. The Act itself has no Federal Register URL in the source list. The report explicitly draws on law firm secondary analyses (Allens, MinterEllison, Gadens, Pinsent Masons) for all substantive claims, e.g. '[High confidence] — confirmed across Allens, MinterEllison, Gadens, Pinsent Masons.' |
| c4 | Entity confidence scoring is applied to all significant claims — High/Medium/Low/Contested/Unverified | PASS | Findings sections include inline tags like '[High confidence]' and '[Medium confidence]'. An 'Entity confidence summary' table lists 14 specific claims each rated High/Medium/Low with evidence and contradiction columns. |
| c5 | Contested findings get their own section and present each position with its evidence — not buried in footnotes | PASS | Dedicated 'Contested findings' section contains five named subsections (A–E) each presenting 'Position 1' and 'Position 2' with supporting evidence and a 'Status' line. E.g. section A presents government position vs. Law Council/PJCIS position on merits review. |
| c6 | URL verification step confirms each cited source is live and the date is confirmed | PASS | 'Source verification' table has columns 'URL live \| Date confirmed \| Venue/type' with explicit Yes/No entries for each source. CISC returns 403 (flagged as No), Law Council PDF inaccessible — both anomalies are noted, confirming verification was actually performed. |
| c7 | Gap analysis categorises each gap (not yet public / paywall / primary research needed / genuinely unknown) — not just 'information unavailable' | PASS | Gap analysis table has a 'Category' column with labels matching the criterion: 'Not yet public / Access restriction', 'Not yet public', 'Paywall / PDF not crawlable', 'Genuinely unknown (secrecy by design)', and 'Not yet public / Primary research needed'. |
| c8 | Secondary source sweep draws on multiple source types independently — journalism, academic, industry — without one type dominating | PARTIAL | Sources include law firms (Allens, MinterEllison, Gadens, Ashurst, Pinsent Masons, Clayton Utz, LK Law, Holding Redlich, Dentons), OT security vendors (Dragos, Nozomi, Industrial Defender), compliance vendors (Kinatico, Pentagram), industry participant (Macquarie Data Centres), and director body (AICD). However, law firm analyses dominate; no journalism or academic sources appear. |
| c9 | Sources section includes authority level and entity score contribution per source | PARTIAL | Numbered sources list explicitly labels authority per entry, e.g. 'Law firm primary analysis — High authority', 'OT security vendor — Medium authority', 'Compliance vendor — Low-medium authority'. However, 'entity score contribution per source' (i.e. which confidence-scored claims each source supported) is not mapped in the sources list — it appears only in the entity confidence table per claim, not per source. |
| c10 | Output addresses Australia's Security of Critical Infrastructure Act 2021 specifically — covering the 2018 original Act and the 2021 amendments (SOCI Act amendments), not just generic 'critical infrastructure law' | PASS | Report explicitly names and distinguishes the 2018 original SOCI Act (4 sectors, foreign ownership register), the SLACI Act 2021 (11 sectors, emergency powers), SLACIP Act 2022 (CIRMP), and ERP Act 2024, including Royal Assent date '2 December 2021'. |
| c11 | Output's sector coverage explicitly addresses BOTH energy AND data storage / processing — separately, with sector-specific obligations (e.g. positive security obligation, mandatory cyber incident reporting) per sector | PASS | Separate sections: 'Energy sector: what changed' details CIRMP obligations, asset classes, cyber framework requirements (Essential Eight ML1 etc.), SoNS enhanced obligations, and proposed ML2 uplift. 'Data storage sector: what changed' details new sector creation, s.12F(3) notification obligation, ERP Act 4-part test, business critical data definition, and April 2025 CIRMP Rules amendment. |
| c12 | Output's domain-mapping step names authoritative AU sources — Department of Home Affairs (CISC, formerly DCO), ACSC, Parliamentary Joint Committee on Intelligence and Security (PJCIS) reports, Federal Register of Legislation, sector-specific regulators (AER for energy, OAIC for data) — before evidence collection | PARTIAL | Domain map names CISC (within Home Affairs) ✓, ASD (ACSC successor) ✓, PJCIS ✓, AEMO (energy) ✓. Missing: AER (Australian Energy Regulator), OAIC (for data), and Federal Register of Legislation not mentioned as a source to consult. |
| c13 | Output's primary sources are fetched and read — the Act itself (federal register URL), the Risk Management Program rules, sector-specific guidance documents, parliamentary committee reports — not cited via summaries | FAIL | No Federal Register URL for the Act appears in the source list. CISC sector guidance pages returned 403 errors ('No (403 errors)'). PJCIS recommendations are noted as 'Cited across multiple sources' (secondary). The CIRMP Rules are cited via law firm analyses (MinterEllison, Allens), not via a direct Government source URL. Specific section numbers (s.5, s.12F(3)) appear to derive from law firm annotations, not direct Act reads. |
| c14 | Output's entity confidence per significant claim uses High / Medium / Low / Contested / Unverified — e.g. 'Mandatory cyber incident reporting within 12 hours: HIGH (legislated in s30BC); Industry's compliance cost claims: CONTESTED (varies widely by source)' | PARTIAL | Entity confidence table and inline tags consistently use High/Medium/Low. 'Contested' does not appear as a confidence rating in the table — contested claims are handled in a separate section rather than tagged inline as 'CONTESTED'. 'Unverified' is also absent as a label; the nearest is 'Low' for the no-enforcement-actions claim. |
| c15 | Output's contested findings get their own section — presenting industry's view (high cost, low net benefit) alongside government's view (national security imperative) with evidence per position, not buried as footnotes | PASS | Five-subsection 'Contested findings' section (A–E) explicitly labels 'Position 1 — Government' and 'Position 2 — Industry/legal commentary' for each dispute, with named sources and a 'Status' summary. E.g. section D cites PJCIS 2022 on cost burden alongside government's principles-based flexibility argument. |
| c16 | Output's URL verification confirms each cited source is live — checking publication date, version (e.g. specific compilation of the Act), and that the link still resolves | PASS | Source verification table checks URL live (Yes/No) and date confirmed for all 17 sources. CISC returns 403 (flagged), Law Council PDF inaccessible (flagged). Date column populated for each accessible source. Version-level checking (specific Act compilation) is not present, but liveness and date checks are performed. |
| c17 | Output's gap analysis classifies each gap — 'not yet public' (regulations under development), 'paywall' (industry analyst reports), 'primary research needed' (operational impact data is held by individual entities), 'genuinely unknown' (long-term effectiveness) | PASS | Gap analysis table uses explicit category labels: 'Not yet public / Access restriction', 'Not yet public', 'Paywall / PDF not crawlable', 'Not yet public / Primary research needed', 'Not yet public / Requires primary research', and 'Genuinely unknown (secrecy by design)' for the SoNS designation list. |
| c18 | Output's sources section includes per-source authority level (government legislation = high authority, parliamentary committee = high, industry submission = medium with conflict-of-interest noted, news = medium with date sensitivity) and what each source contributed | PARTIAL | Numbered sources list includes authority level per entry (e.g. 'Major Australian law firm analysis — High authority', 'Compliance software vendor (treat as low-medium authority)'). OT security vendors noted as 'treat as medium authority'. However, 'what each source contributed' (i.e. which claims it supported) is not stated per source in the sources section — that mapping exists only in the entity confidence table per claim. |
| c19 | Output addresses what would be needed for a strong inquiry submission — primary regulatory text + parliamentary record + a balanced selection of industry submissions — the requester is preparing one, so the deep-research output should map to that artifact | PARTIAL | The gap analysis identifies missing primary regulatory text (CISC factsheets, CIRMP consultation submissions), missing parliamentary record detail (Law Council PDF inaccessible), and notes industry submissions are not yet public. However, the output does not explicitly frame its findings in terms of what a submission drafter would need — no section maps evidence to submission structure or flags which gaps are submission-critical vs. background. |

### Notes

The output is a substantively strong deep-research product covering the SOCI Act regime in detail, with correct sector separation, a genuine contested-findings section, categorised gap analysis, and per-source authority labelling. Its main weakness is reliance on law firm secondary analyses throughout: CISC primary pages returned 403 errors, the Act was never fetched from the Federal Register, and PJCIS reports were cited only through secondary summaries — causing both c3 and c13 to fail. Entity confidence uses only High/Medium/Low (not Contested/Unverified as distinct tiers), and the source list maps authority but not contribution per source. The secondary sweep is dominated by law firm analysis with no journalism or academic sources. These gaps collectively hold the score just below the PASS threshold at 77.8%.
