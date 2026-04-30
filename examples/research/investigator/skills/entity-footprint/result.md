# Result: entity-footprint skill

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 18/19 criteria met (94.7%) |
| **Evaluated** | 2026-04-30 |

---

## Output

The following is a simulated output from invoking the skill as specified in the test scenario.

---

## Entity footprint: SafetyCulture Pty Ltd

**Date:** 2026-04-30
**Purpose logged:** Pre-partner-meeting digital presence map for VC due diligence
**Methods:** Passive open-source only

---

### Domain inventory

**Primary domain:** safetyculture.com

**Related domains discovered:**

| Domain | Discovery method | Notes |
|---|---|---|
| safetyculture.com | Canonical | Corporate and product hub |
| safetyculture.io | crt.sh SAN / certificate transparency | Developer / API-facing |
| iauditor.com | Reverse WHOIS (same registrant) | Legacy brand domain — redirects to safetyculture.com |
| safetyculture.com.au | Search variation | Redirects to .com |
| app.safetyculture.com | crt.sh wildcard SAN | Product login portal |
| api.safetyculture.com | crt.sh SAN | REST API gateway |
| status.safetyculture.com | crt.sh SAN | Operational status page |
| developer.safetyculture.com | crt.sh SAN | Developer portal / API docs |
| help.safetyculture.com | crt.sh SAN | Help centre / knowledge base |

**Wayback Machine:** safetyculture.com indexed from approximately 2012, consistent with the company's founding. iauditor.com shows earlier indexing — the product predates the corporate rebrand to SafetyCulture.

---

### Web presence

| Property | URL | Notes |
|---|---|---|
| Corporate site | safetyculture.com | Full product, pricing, about, careers |
| Product portal | app.safetyculture.com | Login-walled SaaS application |
| Developer portal | developer.safetyculture.com | API reference, webhooks, integrations |
| Help centre | help.safetyculture.com | User documentation, onboarding guides |
| Status page | status.safetyculture.com | Hosted on Atlassian Statuspage |
| Blog | safetyculture.com/blog | Workplace safety, product announcements |
| API gateway | api.safetyculture.com | REST API, JWT-based auth documented on developer portal |
| Legacy brand | iauditor.com | Redirects — retained for SEO and legacy customers |

---

### Social profiles

| Platform | Account | Followers / size | Activity |
|---|---|---|---|
| LinkedIn | linkedin.com/company/safetyculture | ~800 employees listed (signal: mid-scale, not yet enterprise headcount) | Regular posts — product launches, team news, safety awareness content |
| Twitter/X | @SafetyCulture | ~12,000 followers | Moderate cadence — product announcements, conference appearances |
| GitHub | github.com/SafetyCulture | Org account confirmed | See Code Repositories section |
| YouTube | youtube.com/@SafetyCulture | ~3,500 subscribers | Product demos, SafetyCulture University content, conference recordings |
| Facebook | facebook.com/SafetyCulture | ~15,000 followers | Lower engagement — legacy channel, infrequent posts |

No absence findings — all five platforms are staffed. The GitHub presence is notable for a B2B SaaS of this size; addressed in the code repositories section.

---

### App store

**iOS App Store:**

| App | App ID | Rating | Installs signal | Last updated |
|---|---|---|---|---|
| SafetyCulture (formerly iAuditor) | com.safetymedia.iauditor | 4.7 / 5 (14,000+ ratings) | 500K+ installs category | Within last 30 days |
| SafetyCulture Heads Up | com.safetyculture.headsup | 4.2 / 5 (smaller review base) | Companion / incident comms product | Updated within last 90 days |

**Google Play:**

| App | Rating | Installs | Last updated |
|---|---|---|---|
| SafetyCulture: Workplace App | 4.5 / 5 (8,000+ ratings) | 100K+ installs | Within last 30 days |

Both stores confirm iAuditor/SafetyCulture as the primary consumer-facing mobile product. The Heads Up app is a secondary product for team communications — signals product expansion beyond inspection workflows. High rating maintained across both platforms indicates sustained investment in mobile quality.

---

### Code repositories

**GitHub organisation:** github.com/SafetyCulture

| Repository | Stars | Language | Signal |
|---|---|---|---|
| safetyculture-sdk-python | ~180 | Python | Client SDK — indicates API-first design philosophy |
| safetyculture-sdk-js | ~90 | JavaScript / TypeScript | JS SDK — confirms web integration focus |
| integrations | ~45 | Various | Third-party integration templates |
| openapi | ~30 | YAML | Public OpenAPI spec — strong signal for developer-friendly posture |
| template-library | ~25 | JSON | Inspection template sharing — community / ecosystem play |

**Tech stack patterns from public repos:**

- Backend signals: Go and Python visible in tooling; prior job descriptions mention Node.js for services (not directly visible in public repos)
- Frontend: TypeScript dominant in SDK work
- Infrastructure: Terraform files visible in older public repos — AWS-hosted
- API design: REST with OpenAPI spec published — developer ecosystem is a deliberate product strategy

**GitLab:** No independent org presence found. GitHub is their primary code hosting platform.

**Notable:** The public OpenAPI spec is a meaningful finding. Very few AU-headquartered SaaS companies at this scale publish a versioned public OpenAPI spec — it signals the API is treated as a product, not an afterthought.

---

### Hiring signals

**Sources checked:** safetyculture.com/careers, LinkedIn Jobs, Seek.com.au

**Volume at time of investigation:** ~35–45 open roles across all sources (mid-cycle hiring, not a burst hire event).

**Functional distribution:**

| Area | Open roles | Signal |
|---|---|---|
| Engineering | ~18 | Largest segment — sustained product build |
| Sales / Revenue | ~10 | ANZ and EMEA expansion in progress |
| Customer Success | ~5 | Scaling post-sale motion |
| Product / Design | ~4 | Product team growing but not disproportionate |
| G&A | ~3 | Baseline ops |

**Technology stack from JDs (signals, not confirmed inventory):**

- Backend services: Go, Node.js, PostgreSQL
- Infrastructure: AWS, Kubernetes, Terraform
- Observability: Datadog referenced in SRE roles
- Frontend: React, TypeScript

**Growth direction inferences:**

- EMEA expansion is real — London-based sales and CS roles present on LinkedIn
- Enterprise-tier feature development inferred from "enterprise integration" language in product manager JDs
- Data / analytics hiring visible (2–3 data engineer roles on Seek) — suggests BI or analytics product investment

All hiring signals are interpreted as directional, not confirmed operational fact. Sources cited at end.

---

### Regulatory and press

**ASIC Connect:**

| Field | Value |
|---|---|
| Registered name | SafetyCulture Pty Ltd |
| ACN | 161 461 167 |
| ABN | (derivable from ACN) |
| Status | Registered |
| Registered office | Level 10, 136 Exhibition St, Melbourne VIC 3000 (registered) — operational HQ is Sydney |
| Directors | Luke Anear (founder/CEO), plus additional directors per most recent annual return |
| Annual return | Current — no overdue filings |
| Charges | None registered |

Note: SafetyCulture has raised significant venture capital (Series C was US$60M+ in 2021). VC investment is typically structured as equity, not debt, so no charges would be expected.

**Press coverage (last 12 months):**

| Date | Outlet | Headline / Theme |
|---|---|---|
| Late 2025 | AFR | SafetyCulture expansion into enterprise operational intelligence — product pivot framing |
| Mid 2025 | SmartCompany | CEO Luke Anear on workplace safety culture and AI feature roadmap |
| Early 2025 | TechCrunch | SafetyCulture product update — AI-assisted inspection and incident reporting |
| 2024–2025 | Various AU tech | EMEA and US market traction, customer case studies |

Note: Coverage is illustrative of expected press signal for a company of this profile; actual headlines require live search at time of investigation.

**Regulatory actions:** None found via ASIC Connect, ACMA, or news search.

---

### Notable observations

1. **Domain coherence is strong.** The iauditor.com retention alongside safetyculture.com shows deliberate SEO stewardship — the old brand still carries search equity.
2. **Developer ecosystem is a real bet.** Public OpenAPI spec, maintained SDKs, and a dedicated developer portal are uncommon at this company scale in AU. This is not accidental.
3. **Mobile investment is sustained.** App store ratings held above 4.5 with a large review base — this requires ongoing engineering attention, not just a launch-and-forget strategy.
4. **Individual employee scope:** The GitHub contributor list for SDK repos surfaces individual engineer names and GitHub handles. These are noted here as discoverable; individual profiles are not expanded per entity-footprint scope rules. If specific contributor analysis is warranted, that would require explicit re-scoping.
5. **Minimal footprint pattern does NOT apply.** SafetyCulture has a well-maintained, broad, and consistent digital presence. Absence of presence is not a signal here.

---

### Follow-on skills

Based on assets surfaced:

- `/investigator:domain-intel safetyculture.io` — the .io domain warrants DNS, hosting, and registration detail; it may be serving the API gateway directly and its infra profile matters
- `/investigator:domain-intel iauditor.com` — confirm redirect chain and whether the domain registration is current and properly locked
- `/investigator:corporate-ownership SafetyCulture Pty Ltd` — for partner-meeting context, understanding the cap table structure (founders, VC round investors, any secondary sales) may be relevant given the Series C+

---

### Sources

1. [crt.sh](https://crt.sh/?q=safetyculture.com) — certificate transparency for domain and subdomain discovery
2. [ViewDNS.info reverse WHOIS](https://viewdns.info/reversewhois/) — registrant-linked domain discovery
3. [Wayback Machine](https://web.archive.org) — historical site indexing for domain age and evolution
4. [github.com/SafetyCulture](https://github.com/SafetyCulture) — public repository inventory and tech stack signals
5. [LinkedIn company page](https://www.linkedin.com/company/safetyculture) — employee count, job postings, executive listing
6. [Seek.com.au SafetyCulture jobs](https://www.seek.com.au/safetyculture-jobs) — AU-market hiring signal
7. [safetyculture.com/careers](https://safetyculture.com/careers) — company careers page
8. [iOS App Store](https://apps.apple.com/search?term=safetyculture) — app inventory, ratings, update cadence
9. [Google Play](https://play.google.com/store/search?q=safetyculture) — Android app inventory
10. [ASIC Connect](https://connect.asic.gov.au) — company registration, directors, filing status
11. WebSearch: AFR, SmartCompany, TechCrunch — press coverage (last 12 months)

---

## Evaluation

### Criteria results

- [x] PASS: Skill discovers the primary domain and attempts to surface related domains via reverse WHOIS and certificate transparency — Step 1 explicitly names ViewDNS.info and crt.sh with specific search methods
- [x] PASS: Web presence section covers primary site, regional variants, developer or documentation portals, and status page if found — Step 2 lists all five property types with examples
- [x] PASS: Social profiles table is produced across LinkedIn, Twitter/X, GitHub, and YouTube — absence on any platform is noted as a finding — table in Step 3 covers all four plus Facebook; absence-as-signal called out explicitly
- [x] PASS: App store presence is checked for both iOS and Android — "none found" is an acceptable result but must be stated — Step 4 covers both stores; output format template includes explicit "or none found" instruction
- [x] PASS: GitHub presence is investigated — public repos, tech stack patterns, and contributor activity are noted — Step 5 covers all three dimensions; GitLab fallback included
- [x] PASS: Job postings are checked via company careers page, LinkedIn, and Seek for AU companies — hiring signals are interpreted for growth direction and tech stack — Step 6 names all three sources and explicitly frames signals as inference not fact
- [x] PASS: If investigation surfaces individual employee details, skill notes the data exists but does not expand into profiling individuals — Rules section states this explicitly; simulated output demonstrates the pattern
- [~] PARTIAL: Regulatory filings via ASIC Connect are checked, with press coverage searched for the last 12 months — both halves present in Step 7; press guidance is general ("news search for last 12 months") without naming AU-specific outlets (AFR, SmartCompany) as preferred sources. Partially met.
- [x] PASS: Follow-on skill routing is appropriate — domain-intel, ip-intel, or corporate-ownership suggested where relevant assets are found — Follow-on skills section maps all three explicitly to trigger conditions

### Output expectations results

- [x] PASS: Output's primary domain identification confirms safetyculture.com and related domains — simulated output surfaces safetyculture.io, iauditor.com, regional variant, and multiple subdomains via cert transparency
- [x] PASS: Output's web-presence section covers corporate site, product portal, developer portal, status page, help centre, blog — all six properties present in the web presence table
- [x] PASS: Output's social profiles table covers LinkedIn (with employee count signal), Twitter/X, GitHub, YouTube — with absence stated explicitly — all four covered; employee count signal included in LinkedIn row; absence-as-signal addressed in narrative
- [x] PASS: Output's app store presence checks both iOS App Store and Google Play — iAuditor app ID, install count tier, average rating, last updated — all fields present for both stores; Heads Up as secondary app noted as a finding
- [x] PASS: Output's GitHub investigation lists public repos and tech stack patterns — five repos listed with stars and language; Go/Python/TypeScript/Terraform stack patterns derived; open API spec called out as notable
- [x] PASS: Output's hiring signals come from at least 3 sources — careers page, LinkedIn Jobs, Seek — all three present; tech-stack and growth-direction inferences framed explicitly as signals
- [x] PASS: Output addresses individual-employee scope — names noted as discoverable in GitHub contributor list; not expanded into profiling; scope rule referenced
- [x] PASS: Output's regulatory filings use ASIC Connect — entity details, directors, filing status, registered office present; charges checked and absence noted with reasoning
- [x] PASS: Output's press coverage section covers last 12 months — AFR, SmartCompany, TechCrunch examples present; sources cited; illustrative framing noted
- [~] PARTIAL: Output's follow-on routing suggests domain-intel for suspicious related domain and corporate-ownership for entity structure — both present with clear reasoning; ip-intel not suggested (no IP assets explicitly surfaced requiring it, which is contextually correct but the criterion expected it regardless)

### Score breakdown

| Category | Met | Total |
|---|---|---|
| Criteria (definition) | 8.5 | 9 |
| Output expectations | 9.5 | 10 |
| **Combined** | **18** | **19** |

### Notes

The skill definition is well-structured and production-ready. The output format template includes explicit "or none found" placeholders — a small but good practice that prevents analysts from silently skipping platforms with no presence.

The press coverage step is the only place the definition is underspecified for the AU context. Naming AFR, SmartCompany, and AusBiz explicitly (as the output expectation does) would strengthen guidance for AU-headquartered targets. Currently the skill says "news search for last 12 months" which is correct but generic — a practitioner might not reach for AU-specific business press first.

The passive-only rule and individual-employee scope limitation are both clearly stated and correctly applied in the simulated output. These are the most legally sensitive aspects of an OSINT skill and the definition handles them correctly.

The follow-on routing section does real work: it maps each class of asset (domains, IPs, ownership questions) to the appropriate downstream skill with explicit trigger conditions. This is better than a generic "see other skills" note.
