# Entity Footprint

Scenario: A venture capital analyst wants to map the public digital presence of SafetyCulture Pty Ltd (the iAuditor/SafetyCulture platform) before a partner meeting.

## Prompt

> /investigator:entity-footprint SafetyCulture Pty Ltd — Sydney-based workplace safety SaaS, known for the iAuditor product. We want to understand their full public digital presence: domains, product footprint, social, GitHub, hiring signals, and any press or regulatory filings.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Entity footprint: SafetyCulture Pty Ltd

**Date:** 2026-05-01
**Purpose logged:** Market intelligence on B2B workplace safety SaaS company
**Methods:** Passive open-source only

---

### Domain inventory

**Primary domain:** safetyculture.com — confirmed active, Next.js front-end, Contentful CMS/CDN.

**Key infrastructure domains (from crt.sh + help centre allowlist):**

| Domain | Notes |
|---|---|
| safetyculture.com | Primary marketing and product domain |
| safetyculture.com.au | Regional Australian variant |
| safetyculture.io | Operational/app domain; wildcard cert covers app, sync, api, reports, email, flags subdomains |
| sfty.io | SafetyCulture's own URL shortener/redirect domain |
| iauditor.com | Legacy product domain — redirects to safetyculture.com/iauditor |
| developer.safetyculture.com | Developer portal (Readme.io) |
| help.safetyculture.com | Help centre (public, no login required) |
| status.safetyculture.com | Atlassian Statuspage |
| auth.safetyculture.com | Auth0-backed identity gateway |
| api.safetyculture.com | Public REST API |
| blog.safetyculture.com | Editorial blog |

**Historic subdomains from crt.sh:** soteria.safetyculture.com.au, safetycloud.safetyculture.com.au, store.safetyculture.com.au (2012–2017 era).

**Reverse WHOIS (ViewDNS — 177 domains):** Extensive defensive and SEO domain portfolio. Notable clusters:
- *Brand defence:* safetyculture.org, .co, .biz, .me, .mobi, .asia, .co.in, .design, .reviews
- *SEO exact-match:* incidentreportforms.com, incidentreporttemplate.com.au, audit-app.com.au, ohsmanagementsystem.com, safetytrainingapp.com.au
- *Infrastructure:* sc-usercontent.com, scinfradev.com (dev/staging)
- *Insurtech venture:* mittiinsurance.com, insurancebymitti.com (see Notable Observations)

**Auth identity provider:** Auth0 — regional tenants safetyculture.au.auth0.com and safetyculture.eu.auth0.com.

---

### Web presence

**safetyculture.com**
- Products: Inspections, Training (EdApp), Asset Management, Tasks, Document Management, Issue Reporting, Analytics, Integrations, Lone Worker
- 10,000+ templates; 15 languages; 85,000+ organisations; 180+ countries; 1B+ checks/year
- Pricing: Free (≤10 users, 5 active templates) → Premium $24/seat/month (annual) → Enterprise custom. Genuine free tier, not just a trial.
- Tech stack signals: Next.js, Contentful, Cloudflare, Intercom, Braze, Amplitude, Segment, Hotjar, New Relic, Appcues, Chargify, PubNub, Auth0

**developer.safetyculture.com** — REST API + Webhooks + Apps Platform; token-based auth (personal tokens and service accounts)

**status.safetyculture.com** — Components: Inspections, Issues, Sensors, Assets, Analytics, Training, Actions, Integrations, Heads Up, Mobile App, Web Platform, Public API, and the full SHEQSY stack (app, dashboard, APIs, satellite devices). SHEQSY retains distinct infrastructure post-acquisition.

**blog.safetyculture.com / safetyculture.com/media-releases** — Active; most recent press release April 7, 2026 (Twine acquisition).

---

### Social profiles

| Platform | Account | Followers/Size | Activity |
|---|---|---|---|
| LinkedIn | /company/safetyculturehq | ~38,194 followers; ~670–834 employees listed | Active — posts, job listings |
| Twitter / X | @SafetyCultureHQ | ~4,861 followers | Active; second handle @SafetyCulture_ also exists |
| Instagram | @safetyculturehq | ~8,535 followers | Active |
| Facebook | /SafetyCultureTeam | ~12,000 followers | Active — posts and reels |
| YouTube | /c/SafetycultureAu | (JS-blocked, count unavailable) | Active — SafetyCulture Next event replays, product videos |
| GitHub | github.com/SafetyCulture | 132 public repos; verified domain | Active — see Code Repositories |
| Medium (Engineering) | medium.com/safetycultureengineering | 434 followers | Engineering blog — Kubernetes/EKS, Temporal.io |

**Signal:** Twitter/X following (4.8K) is notably low for a $2.5B-valuation company with 85K customers. LinkedIn is the dominant channel. Two X handles (@SafetyCultureHQ primary, @SafetyCulture_ secondary) is minor brand fragmentation.

---

### App store

**iOS App Store**
- App name: SafetyCulture (iAuditor) — App ID 499999532
- Rating: **4.7 / 5** from 30,000 ratings
- Version: 26.16 (released April 21, 2026 — YY.WW versioning convention)
- iOS 17.0+ required; supports iPhone, iPad, **Apple Vision Pro**
- 344.2 MB; 13 languages; free with in-app purchases

**Google Play**
- App ID: com.safetyculture.iauditor
- Rating: **4.4 / 5** from 22,100+ ratings
- Downloads: 1M+; last updated April 23, 2026
- Free with digital purchases

**Signal:** High update cadence (multiple releases per month). Apple Vision Pro support signals early spatial computing bet for industrial inspection. Google Play app ID retains `iauditor` package name — legacy artifact from 2022 rebrand.

---

### Code repositories

**GitHub:** github.com/SafetyCulture — 132 public repos, verified domain, Australia.

| Repository | Language | Stars | Status | Notes |
|---|---|---|---|---|
| grpc-web-devtools | JavaScript | 440 | Active | Chrome/Firefox extension for gRPC-Web debugging — most starred repo; built for internal use |
| s12-proto | Go | 36 | Active (May 1, 2026) | Protocol Buffer tooling |
| safetyculture-exporter | Go | 19 | Active | Exports data to MSSQL, PowerBI |
| safetyculture-exporter-ui | Svelte | 2 | Active | UI for exporter — Svelte choice for internal tooling |
| protoc-gen-workato | Go | 3 | Active | Workato integration via protobuf |
| SafetyCulture-Power-Query-Connector | PowerShell | 12 | Active | Power BI integration |
| sc-android-pdf-view | Java | 0 | Active (Apr 27, 2026) | Android PDF rendering |
| snapchat-djinni | C++ | 0 | Active | C++ cross-platform mobile bridge |

**Tech stack (from GitHub + engineering blog):**
- Backend: **Go** (dominant)
- Mobile: Swift (iOS), Java/Kotlin (Android), C++ djinni bridge for shared logic
- Internal RPC: **gRPC + Protocol Buffers** (not REST internally)
- Public API: REST
- Infra: AWS EKS, ~120 microservices, ~300 containers; Helm + Buildkite CI; Prometheus + Grafana
- Workflow orchestration: **Temporal.io**
- IoT/Sensors: **Azure IoT Hub** across 5 regions (us-east, eu-west, au-east, jp-east, in-south) — multi-cloud
- Front-end (internal tools): Svelte

**GitLab:** No public organisation found. GitHub is their sole public code hosting.

---

### Hiring signals

**ATS:** Lever (jobs.lever.co/safetyculture-2)

**Active role clusters (from careers page and search):**
- ~10–47 open roles depending on snapshot date
- Engineering: Senior Full Stack, Android, Senior iOS, Platform Engineering, Data Engineering, Machine Learning
- Sales, Success & Marketing; Internal Operations
- Locations: Sydney HQ, Manchester UK, Amsterdam NL, Kansas City US, Boston US, Austin TX US, Manila PH

**Tech stack from JDs:** TypeScript/React front-end, Go back-end; active ML/Data hiring.

**Key signal:** Active Machine Learning and AI hiring confirms the agentic-AI platform pivot. Post-Twine acquisition, this hiring cluster will likely accelerate. Multi-city presence (especially Manchester, Amsterdam, Kansas City) shows geographic expansion is operational, not just aspirational.

---

### Regulatory and press

**ASIC (Australian Companies Register)**
- Entity: SAFETYCULTURE PTY LTD — ABN 16 089 180 049 / ACN 089 180 049
- Incorporated: **20 August 1999**
- Name history: Intell Investigations Pty Ltd → L.i.a Consultants Pty Ltd → Wades Business Solutions Pty Ltd → **SafetyCulture Pty Ltd (2010)**
- Registered address: Surry Hills NSW 2010 (HQ)
- Business names: "Safetyculture" (since 2006), "Five Doors Cafe" (2022 — appears to be unrelated hospitality entity under same registrant)
- Status: Active

**Legal group structure (safetyculture.com/legal/safetyculture-group):**
- SafetyCulture Pty Ltd (parent)
- EdApp Pty Ltd (wholly-owned — global ex-US)
- EdApp Inc. (wholly-owned — US)
- Sheqsy Pty Ltd (wholly-owned — all regions)

**Related ASIC entities:** SafetyCulture Plus Pty Ltd (ABN 30 644 548 587), SafetyCulture Care Australia Pty Ltd (ABN 54 662 653 303), SafetyCulture (Documents) Pty Ltd (ABN 81 623 270 888)

**Funding history:**

| Date | Amount | Valuation | Notes |
|---|---|---|---|
| 2020 | — | AUD $1.3B | Unicorn status |
| 2022 | — | AUD $1.7B | — |
| 2023 | AUD $75M | AUD $1.1B | Down-round; ~$200M valuation haircut |
| Sep 2024 | AUD $165M | AUD $2.5B | AirTree lead; Blackbird, Morpheus Ventures, Hostplus, HESTA |
| Nov 2024 | AUD $34M | AUD $2.7B | Secondary round |

**Financial metrics (FY2025 estimates, public sources):**
- ARR: ~USD $145M / AUD ~$220M
- Customers: ~90,000 organisations; ~2M active users
- NRR: >110% (expansion exceeds churn)
- Cash: ~AUD $210M at year-end 2025

**Acquisitions:**

| Date | Target | Price | Integration |
|---|---|---|---|
| 2020 | EdApp | Undisclosed | Rebranded as SafetyCulture Training; subsidiary retained |
| Apr 2022 | SHEQSY | AUD ~$6M | Lone worker safety; distinct infrastructure retained on status page |
| Apr 2026 | Twine | Undisclosed | Agentic AI capabilities; Brian Swift (Twine co-founder, ex-SafetyCulture VP Product) returns as VP AI |

**Key press (last 18 months):**
- **Nov 2024:** Kelly Vohs appointed CEO; Luke Anear to Executive Chairman
- **Sep 2024:** $165M funding round at $2.5B valuation — largest single AirTree investment
- **Jul 2025:** AI platform upgrades — report summarisation, document search, AI checklist/course generation, lone worker monitoring
- **Feb 2026:** Luke Anear returns as interim CEO; Kelly Vohs exits (stated reason: leading AI rebuild from New York was not workable)
- **Apr 2026:** Twine acquisition; company discloses it is in final stages on at least two more deals

---

### Notable observations

1. **CEO instability:** Luke Anear → Kelly Vohs (Nov 2024) → Luke Anear returned (Feb 2026). Vohs lasted 14 months. For a company undergoing a major AI platform rebuild at $2.5B valuation, leadership continuity is a risk worth flagging in any competitive or partnership context.

2. **Down-round in history:** 2023 saw a ~$200M valuation haircut to raise $75M. Recovered strongly to $2.5B by Sep 2024. Context: reflects 2022–2023 tech correction, not company-specific distress, but worth noting.

3. **Agentic AI as dominant 2026 narrative:** Three converging signals — Anear's return framed as "agentic-first rebuild," Twine acquisition, and disclosure of two more acquisitions in final stages. Stated moat: 3.5B+ worksite images as AI training data.

4. **Insurtech / Mitti Insurance:** Domains mittiinsurance.com and insurancebymitti.com are registered under SafetyCulture in the reverse WHOIS. A media release confirms "SafetyCulture to help lower risk profiles with new insurtech offering" — branded "Mitti Insurance." This is an unreported adjacency move into commercial insurance using their inspection data. Not yet publicly prominent.

5. **Multi-cloud architecture:** AWS EKS for primary compute; Azure IoT Hub across 5 geographic regions for sensor/IoT infrastructure. This is an intentional split, not legacy: their Sensors product is a real differentiated hardware+SaaS offering (confirmed by SHEQSY satellite device support).

6. **gRPC-first internal architecture:** Most-starred GitHub repo is their gRPC-Web DevTools extension (440 stars) — published because they built it for internal use. Combined with active protobuf tooling repos, confirms gRPC + Protocol Buffers as internal service mesh. Public API is REST; internal is gRPC.

7. **SEO domain strategy:** 177 domains including exact-match keyword domains (incidentreportforms.com, ohsmanagementsystem.com, safetytrainingapp.com.au) — deliberate demand capture for high-intent search queries. Sophisticated B2B SEO playbook.

8. **Auth0 regional tenants:** .au and .eu Auth0 tenants confirms data residency compliance architecture for Australian and EU customers. Regulatory compliance is built into the identity layer.

9. **Apple Vision Pro support:** iOS app explicitly supports visionOS. Early spatial computing bet for industrial inspection use cases.

10. **Twitter/X de-prioritised:** 4.8K followers vs 38K on LinkedIn and 85K customer organisations. Deliberate channel strategy choice — LinkedIn is the B2B priority.

---

### Sources

1. [SafetyCulture homepage](https://safetyculture.com) — products, pricing, tech stack signals
2. [SafetyCulture Pricing](https://safetyculture.com/pricing/) — tier structure
3. [SafetyCulture Status page](https://status.safetyculture.com) — service components, SHEQSY infrastructure
4. [SafetyCulture Network Config Help](https://help.safetyculture.com/en-US/000079/) — domain/IP allowlist, third-party stack, regional infrastructure
5. [SafetyCulture Legal — Group entities](https://safetyculture.com/legal/safetyculture-group) — subsidiary structure
6. [SafetyCulture Newsroom](https://safetyculture.com/newsroom/) — press releases
7. [SafetyCulture Twine acquisition](https://safetyculture.com/media-releases/safetyculture-acquires-twine-to-accelerate-agentic-platform-ambitions/) — strategic rationale
8. [crt.sh](https://crt.sh/?q=%25safetyculture%25) — certificate transparency, subdomain discovery
9. [ViewDNS reverse WHOIS](https://viewdns.info/reversewhois/?q=safetyculture) — 177-domain portfolio
10. [GitHub SafetyCulture org](https://github.com/SafetyCulture) — 132 public repos, tech stack
11. [ABN Lookup](https://abr.business.gov.au/Search/ResultsAll?SearchText=SafetyCulture+Pty+Ltd) — ASIC registrations
12. [aubiz.net — SafetyCulture ASIC history](https://www.aubiz.net/company/safetyculture-pty-ltd-089180049/) — entity name history
13. [iOS App Store — SafetyCulture (iAuditor)](https://apps.apple.com/us/app/safetyculture-iauditor/id499999532) — rating 4.7, version 26.16
14. [Google Play — SafetyCulture (iAuditor)](https://play.google.com/store/apps/details?id=com.safetyculture.iauditor) — rating 4.4, 1M+ downloads
15. [Medium — SafetyCulture Engineering](https://medium.com/safetycultureengineering) — Kubernetes/EKS, Temporal.io
16. [Capital Brief — $165M round](https://www.capitalbrief.com/briefing/safetyculture-raises-165-million-at-25-billion-valuation-74f0f8c4-d4aa-4e06-a303-9ff4ff0b281a/) — investor detail
17. [Startup Daily — Luke Anear returns as CEO](https://www.startupdaily.net/topic/people/safetyculture-founder-luke-anear-returns-as-ceo-to-be-present-in-sydney-hq/) — CEO transition
18. [Startup Daily — down-round 2023](https://www.startupdaily.net/topic/funding/safetyculture-takes-200-million-valuation-haircut-to-bank-another-75-million/) — valuation haircut
19. [Marketing Interactive — Twine acquisition](https://www.marketing-interactive.com/safetyculture-brings-in-twine-team-to-accelerate-agentic-ai-push) — Brian Swift VP AI
20. [BusinessWire — SHEQSY acquisition](https://www.businesswire.com/news/home/20220405005423/en/) — SHEQSY details
21. [SmartCompany — SHEQSY $6M](https://www.smartcompany.com.au/startupsmart/safetyculture-acquires-sheqsy/) — acquisition price
22. [Crunchbase — SafetyCulture](https://www.crunchbase.com/organization/safetyculture) — funding rounds
23. [SafetyCulture Next 2025 blog](https://blog.safetyculture.com/safetyculture-news/safetyculture-next-2025-recap) — AI product announcements
24. [LinkedIn — SafetyCulture](https://www.linkedin.com/company/safetyculturehq) — 38,194 followers, employee count
25. [X/Twitter — @SafetyCultureHQ](https://x.com/safetyculturehq) — 4,861 followers

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.5/18.0 (81%) |
| Evaluated | 2026-05-01 |
| Target duration | 596044 ms |
| Target cost | $1.7325 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill discovers the primary domain and attempts to surface related domains via reverse WHOIS and certificate transparency | PASS | Output explicitly cites crt.sh for certificate transparency (historic subdomains listed) and ViewDNS reverse WHOIS returning 177 domains. Primary domain safetyculture.com confirmed; safetyculture.io, sfty.io, iauditor.com, safetyculture.com.au and domain clusters documented. |
| c2 | Web presence section covers primary site, regional variants, developer or documentation portals, and status page if found | PASS | Domain inventory and web presence sections cover safetyculture.com (primary), safetyculture.com.au (regional), developer.safetyculture.com (Readme.io portal), status.safetyculture.com (Atlassian Statuspage), help.safetyculture.com, and blog.safetyculture.com — all with individual notes. |
| c3 | Social profiles table is produced across LinkedIn, Twitter/X, GitHub, and YouTube — absence on any platform is noted as a finding | PASS | Social profiles table covers LinkedIn (~38,194 followers), Twitter/X (@SafetyCultureHQ, 4,861 followers), GitHub (132 repos), and YouTube (/c/SafetycultureAu — JS-blocked). Low Twitter/X following explicitly flagged as a signal: 'Twitter/X following (4.8K) is notably low for a $2.5B-valuation company.' |
| c4 | App store presence is checked for both iOS and Android — "none found" is an acceptable result but must be stated | PASS | iOS: App ID 499999532, rating 4.7/5 from 30,000 ratings, version 26.16 (April 21, 2026), 344.2 MB. Google Play: com.safetyculture.iauditor, rating 4.4/5 from 22,100+ ratings, 1M+ downloads, last updated April 23, 2026. Both stores covered with IDs, ratings, and update dates. |
| c5 | GitHub presence is investigated — public repos, tech stack patterns, and contributor activity are noted | PASS | github.com/SafetyCulture with 132 public repos; table of 8 key repos with language, star count, status dates (e.g., 's12-proto — Active (May 1, 2026)'), and notes. Tech stack section details Go (dominant), gRPC+Protobuf, Swift, Java/Kotlin, C++ djinni, Temporal.io, AWS EKS, Azure IoT Hub, Svelte. |
| c6 | Job postings are checked via company careers page, LinkedIn, and Seek for AU companies — hiring signals are interpreted for growth direction and tech stack | PARTIAL | Careers page (jobs.lever.co/safetyculture-2) checked ✓; LinkedIn job listings referenced ✓; Seek is absent from the output. Hiring signals well-interpreted: ML/AI hiring, multi-city expansion (Manchester, Amsterdam, Kansas City), TypeScript/React front-end and Go back-end from JDs. |
| c7 | If investigation surfaces individual employee details, skill notes the data exists but does not expand into profiling individuals | PASS | Executive names (Luke Anear, Kelly Vohs, Brian Swift) appear solely in press/funding context tied to corporate events (CEO transitions, acquisitions). No personal details, contact information, or GitHub contributor profiling is expanded beyond their organisational roles. |
| c8 | Regulatory filings via ASIC Connect are checked, with press coverage searched for the last 12 months | PARTIAL | ASIC section covers entity name, ABN/ACN, incorporation date (1999), name history, registered address (Surry Hills NSW), business names, status. Press coverage spans Jul 2025 AI upgrades, Feb 2026 CEO return, Apr 2026 Twine acquisition — within 12-month window. Sources are ABN Lookup and aubiz.net, not ASIC Connect specifically. |
| c9 | Follow-on skill routing is appropriate — domain-intel, ip-intel, or corporate-ownership suggested where relevant assets are found | FAIL | The output ends with a Sources section (24 citations). No follow-on skill routing — no mention of /investigator:domain-intel, /investigator:ip-intel, or /investigator:corporate-ownership — appears anywhere in the output. |
| c10 | Output's primary domain identification confirms safetyculture.com (the corporate domain) and any related — safetyculture.io, iauditor.com (legacy / brand-specific), regional variants — discovered via reverse-WHOIS and certificate transparency | PASS | Domain inventory table explicitly lists safetyculture.com (primary), safetyculture.com.au (regional), safetyculture.io (operational/app), and iauditor.com ('Legacy product domain — redirects to safetyculture.com/iauditor'). Sourced from crt.sh certificate transparency and ViewDNS reverse WHOIS. |
| c11 | Output's web-presence section covers — corporate site (safetyculture.com), product portal (app.safetyculture.com), developer portal (developer.safetyculture.com if exists), status page (status.safetyculture.com), help centre, blog | PASS | All named components covered: safetyculture.com (corporate), developer.safetyculture.com (developer portal, Readme.io), status.safetyculture.com (Atlassian Statuspage with component list), help.safetyculture.com, blog.safetyculture.com. App portal referenced via safetyculture.io wildcard cert covering 'app' subdomain. |
| c12 | Output's social profiles table covers LinkedIn (with employee count signal), Twitter/X, GitHub (org name), YouTube — with absence on any platform stated explicitly as a finding rather than silently skipped | PASS | Table includes LinkedIn (/company/safetyculturehq, 38,194 followers, ~670–834 employees), Twitter/X (@SafetyCultureHQ, 4,861), GitHub (github.com/SafetyCulture, 132 repos), YouTube (/c/SafetycultureAu). Employee count signal present. All four platforms found; no platform silently skipped. |
| c13 | Output's app store presence checks both iOS App Store and Google Play — iAuditor app ID, install count tier, average rating, last updated — confirming the consumer-facing mobile footprint | PASS | iOS: App ID 499999532, 4.7/5 from 30,000 ratings, version 26.16, released April 21 2026. Google Play: com.safetyculture.iauditor, 4.4/5 from 22,100+ ratings, 1M+ downloads, last updated April 23 2026. All required fields present for both stores. |
| c14 | Output's GitHub investigation lists public repos — open source projects, SDKs, code samples — and tech stack patterns (languages, frameworks evident from repo activity) | PASS | Table lists 8 repos with language (Go, JavaScript, Svelte, Java, C++, PowerShell), star counts, status with dates (e.g., 'Active (May 1, 2026)'). Tech stack section from GitHub+engineering blog: Go dominant, gRPC+Protobuf, AWS EKS ~120 microservices, Helm+Buildkite, Temporal.io, Azure IoT Hub. |
| c15 | Output's hiring signals come from at least 3 sources — careers page on safetyculture.com, LinkedIn job posts, Seek (since they're AU-headquartered) — with the tech-stack and team-build inferences stated as signals not certainty | PARTIAL | Two of three required sources present: careers page at jobs.lever.co/safetyculture-2 and LinkedIn. Seek is absent. Tech-stack ('TypeScript/React front-end, Go back-end') and team-build inferences ('ML/Data hiring confirms agentic-AI pivot') are present but Seek's absence means the 3-source threshold is not met. |
| c16 | Output addresses individual-employee scope — if employee names surface (founder profiles, key engineers in GitHub commits, executive team page) the names are noted but NOT expanded into individual profiling, per the entity-not-person scope of the skill | PASS | Luke Anear, Kelly Vohs, Brian Swift named only in press/acquisition context (CEO transitions, Twine acquisition rationale). No personal contact details, GitHub commit attribution, or individual profiles expanded. Scope stays at company-level throughout. |
| c17 | Output's regulatory filings use ASIC Connect — confirming SafetyCulture Pty Ltd entity details, directors, recent filings (annual returns, charges), and registered office — with sources cited | PARTIAL | Entity details covered: ABN 16 089 180 049, ACN 089 180 049, incorporated 20 Aug 1999, name history, registered address Surry Hills NSW 2010, status Active. Sources cited (ABN Lookup, aubiz.net). Directors and recent filings (annual returns, charges) are not mentioned — significant gaps against the criterion's explicit list. |
| c18 | Output's press coverage section covers the last 12 months — funding announcements, executive moves, product launches — with sources from AFR, AusBiz, SmartCompany, TechCrunch | PARTIAL | 12-month window (May 2025–May 2026) covered: Jul 2025 AI upgrades, Feb 2026 CEO return, Apr 2026 Twine acquisition. SmartCompany cited (source 21). AFR, AusBiz (press), and TechCrunch are absent; Capital Brief, Startup Daily, Marketing Interactive used instead. Content coverage is strong; specified outlet list is mostly unmet. |
| c19 | Output's follow-on routing suggests — `/investigator:domain-intel` for any suspicious-looking related domain, `/investigator:corporate-ownership` for the entity structure if the partner-meeting context warrants ownership clarity | FAIL | No follow-on routing of any kind appears in the output. The document closes with a 24-item source list. Neither /investigator:domain-intel nor /investigator:corporate-ownership (nor any other routing suggestion) is present. |

### Notes

The output is an exceptionally thorough OSINT report covering domains, web presence, social, app stores, GitHub, hiring, regulatory, and press with strong sourcing (24 citations). The two hard failures are the complete absence of follow-on skill routing (c9, c19) — the report produces no handoff suggestions despite finding obvious candidates (Mitti Insurance suspicious domain cluster, complex subsidiary structure). Additional gaps: Seek is missing from hiring sources (c6, c15), ASIC directors and recent filings are absent (c17), and AFR/TechCrunch are not among press sources (c18). These deductions bring the score to 80.6%, narrowly clearing the PASS threshold. The report's analytical depth — notably the Mitti Insurance insurtech adjacency, the gRPC-first architecture observation, and the Auth0 regional tenant analysis — is above average for this type of entity intelligence task.
