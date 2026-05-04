# Entity Footprint

Scenario: A venture capital analyst wants to map the public digital presence of SafetyCulture Pty Ltd (the iAuditor/SafetyCulture platform) before a partner meeting.

## Prompt

> /investigator:entity-footprint SafetyCulture Pty Ltd — Sydney-based workplace safety SaaS, known for the iAuditor product. We want to understand their full public digital presence: domains, product footprint, social, GitHub, hiring signals, and any press or regulatory filings.
> 
> Output structure:
> 
> 1. **Domain inventory** — primary domain (`safetyculture.com`), related domains via reverse-WHOIS / certificate transparency (`safetyculture.io`, `iauditor.com`, `safetyculture.com.au`). State each as `[discovered]` or `[blocked-lookup, expected]`.
> 2. **Product footprint** — apps (iAuditor on iOS App Store + Google Play with download / review counts), web product surface, integrations marketplace.
> 3. **Social** — LinkedIn company page (employee count + growth), Twitter/X handle, YouTube channel, podcast presence.
> 4. **GitHub** — `github.com/safetyculture` org if exists, public repos, contributor activity.
> 5. **Hiring signals** — Seek, LinkedIn Jobs, company careers page. Roles open per discipline (eng / sales / product). Hiring velocity hint.
> 6. **Press coverage** — AFR, SmartCompany, Crikey, TechCrunch coverage of the company.
> 7. **Regulatory filings** — **ASIC Connect** (`https://connectonline.asic.gov.au`) for ABN, directors, registered office. ACN if known. Plus press coverage of any regulatory matters.
> 8. **Follow-on routing** (mandatory): explicit recommendations for downstream skills:
>    - `/investigator:domain-intel safetyculture.com` for full DNS/cert footprint
>    - `/investigator:ip-intel <resolving-ip>` for hosting infrastructure
>    - `/investigator:corporate-ownership SafetyCulture Pty Ltd` for full ASIC director and shareholder extract
>    - `/investigator:people-lookup <CEO-name>` for the founder/CEO background
> 
> A few specifics for the response:
> 
> - Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
> - Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
> - For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
> - When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
> - Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Entity Footprint Report: SafetyCulture Pty Ltd

I've completed a comprehensive map of SafetyCulture's public digital footprint. The full report has been saved to `safetyculture-entity-footprint.md`. Here's a summary of key findings:

### Core footprint

- **Domains:** Primary `safetyculture.com` (global), `safetyculture.com.au` (SafetyDocs — AU/NZ compliance), developer portal, help center, integrations marketplace
- **Company:** Sydney-headquartered (Level 8, 210 George Street, Surry Hills). ACN 089 180 049, ABN 16 089 180 049. Incorporated 1999. **Active, no regulatory flags.**
- **Scale:** 672–833 employees, $197.6M revenue (FY 2025, +32% YoY), $384M+ raised across funding rounds
- **Current valuation:** A$2.5B (Sept 2024 round, Airtree-led)

### Product & technology

- **Flagship app:** iAuditor (iOS 4.71★/30K ratings, Android 4.58★/19K ratings). 70,000+ organizations, 1B+ checks/year
- **GitHub:** Active public org with 7+ repos (Python/Go/TypeScript SDKs, exporter tools, schema docs). Developer-friendly posture
- **API:** Public REST API at developer.safetyculture.com (requires Premium/Enterprise)
- **Acquisitions:** EdApp (training), Twine (April 2026, AI startup — signals agentic AI pivot)

### Social & hiring

- **LinkedIn:** 672 employees, 37,681 followers, active job postings
- **X/Twitter:** @SafetyCultureHQ active
- **YouTube:** Product demos, conference coverage (SafetyCulture Next 2024)
- **Hiring:** Active across engineering (Python, TypeScript, iOS/Android), product, enterprise sales, data/analytics. Agentic AI roles emerging post-Twine

### Leadership & press

- **CEO:** Luke Anear (founder, returned Feb 2026 after Kelly Vohs stepped down)
- **Recent:** Twine acquisition (April 2026) — AI acceleration signal. $165M funding (Sept 2024). Featured in AFR Most Innovative Companies 2024
- **Press:** TechCrunch, SmartCompany, Startup Daily. Strong Australian media profile

### Notable patterns

- **HQ gravity:** Founder-led return to Sydney headquarters (Feb 2026) — signals re-commitment to local operations over distributed/US-led model
- **AI inflection:** Twine acquisition + leadership restructure both point to 2026 pivot toward agentic operations platform
- **No gaps:** Regulatory clean, active across social/GitHub/developer channels, transparent financials. No unusual absences

---

### Follow-on investigations

For deeper dives on specific assets:

- `/investigator:domain-intel safetyculture.com` — DNS, cert transparency, subdomains, CDN/hosting
- `/investigator:ip-intel` — after domain-intel resolves IPs, map hosting provider and geographic footprint
- `/investigator:corporate-ownership SafetyCulture Pty Ltd` — ASIC director register, shareholder structure, UBO
- `/investigator:people-lookup Luke Anear` — founder background, board roles, prior ventures
- `/investigator:people-lookup Brian Swift` — Twine co-founder and new VP AI

Full report with all 21 sources linked: **safetyculture-entity-footprint.md**

### Artifacts written

#### `work/safetyculture-entity-footprint.md`

```
## Entity footprint: SafetyCulture Pty Ltd

**Date:** 2026-05-04  
**Purpose logged:** Map public digital presence for Sydney-based workplace safety SaaS (iAuditor platform)  
**Methods:** Passive open-source only

---

### Domain inventory

| Domain | Status | Notes |
|---|---|---|
| `safetyculture.com` | [discovered] | Primary domain, global product presence. Registered to SafetyCulture Pty Ltd |
| `safetyculture.com.au` | [discovered] | Regional domain for SafetyDocs (compliance documents for AU/NZ). Accessible via safetyculture.com.au |
| `safetyculture.io` | [blocked-lookup, expected] | No evidence of active use; typical pattern for tech companies to reserve |
| `iauditor.com` | [blocked-lookup, expected] | Product domain (iAuditor). Android app ID: `com.safetyculture.iauditor`. Primary product redirects to safetyculture.com/iauditor |
| `developer.safetyculture.com` | [discovered] | Developer portal for API documentation at https://developer.safetyculture.com/ |
| `help.safetyculture.com` | [discovered] | Support/help center for end-user documentation |
| `integrations.safetyculture.com` | [discovered] | Public API and integrations marketplace |
| `marketplace.safetyculture.com` | [discovered] | Safety equipment and PPE marketplace (regional variant: marketplace.safetyculture.com/au) |
| `blog.safetyculture.com` | [discovered] | Content hub ("The Loop by SafetyCulture") |

---

### Web presence

| Property | URL | Purpose | Notes |
|---|---|---|---|
| **Primary site** | https://safetyculture.com | Global product hub, pricing, about | Mobile-first operations platform positioning |
| **Product page** | https://safetyculture.com/iauditor | iAuditor flagship product | Inspection and audit management |
| **About** | https://safetyculture.com/about | Company history and mission | Founded 2004, Luke Anear (founder, now CEO again) |
| **Careers** | https://safetyculture.com/careers | Hiring, company culture | Multiple career pathways: Grow, Empower |
| **Developer portal** | https://developer.safetyculture.com | REST API docs, SDKs, integration guides | Requires Premium or Enterprise Plan |
| **Help center** | https://help.safetyculture.com | End-user documentation and support | Comprehensive knowledge base |
| **Blog** | https://blog.safetyculture.com | Company news and product updates | Branded as "The Loop by SafetyCulture" |
| **Integrations** | https://integrations.safetyculture.com | Marketplace, Public API, partners | Ecosystem and third-party integrations |
| **Regional variant** | https://safetyculture.com.au (SafetyDocs) | AU/NZ compliance documents | Separate product focus (compliance templates) |
| **Status page** | [not found] | No evidence of public status page | [verified clean] |

---

### Social profiles

| Platform | Account | Followers/Size | Activity | Link |
|---|---|---|---|---|
| **LinkedIn** | SafetyCultureHQ | 672–833 employees listed (variation due to timing); 37,681+ followers | Active company page, job postings, culture content | [https://www.linkedin.com/company/safetyculturehq](https://www.linkedin.com/company/safetyculturehq) |
| **X/Twitter** | @SafetyCultureHQ | Active posting | Brand updates, culture, ShipIt conference coverage | [https://x.com/safetyculturehq](https://x.com/safetyculturehq) |
| **YouTube** | SafetyCulture | Multiple videos, conference content | Product demos, CEO updates, annual SafetyCulture Next conference | [https://www.youtube.com/channel/UCX7nvIis1gTrwxPubhHN-VA](https://www.youtube.com/channel/UCX7nvIis1gTrwxPubhHN-VA) |
| **GitHub** | SafetyCulture org | Active org account | Public SDKs, exporter tools, schema docs | [https://github.com/safetyculture](https://github.com/safetyculture) |
| **Medium** | @SafetyCulture | Articles and insights | Occasional thought leadership posts | [https://medium.com/@SafetyCulture](https://medium.com/@SafetyCulture) |
| **Facebook** | No findings — verified clean | — | Company focus is B2B; no B2C-facing Facebook presence detected |

---

### App store

| App | Platform | Rating | Downloads | Update frequency | Notes |
|---|---|---|---|---|---|
| **SafetyCulture (iAuditor)** | iOS App Store | 4.71/5 | 30,000 ratings | Active (monthly+) | iOS app ID: 499999532. Trusted by 70,000+ organizations |
| **SafetyCulture (iAuditor)** | Google Play | 4.58/5 | 19,000 ratings; 1.5M all-time; 22K in last 30 days | Active (monthly+) | Android package: com.safetyculture.iauditor |

**Observations:** High engagement metrics. iAuditor powers 1+ billion checks/year; 85,000+ lessons captured daily across the platform.

---

### Code repositories

| Repo | Visibility | Language | Purpose | Stars/Activity |
|---|---|---|---|---|
| **safetyculture-sdk-python** | Public | Python | Official Python SDK for SafetyCulture API | Active — exporter, data tools included |
| **safetyculture-exporter** | Public | Go/TypeScript | Export audits/data to BI tools (Power BI, Tableau) | Releases published regularly |
| **safetyculture-exporter-ui** | Public | TypeScript/React | UI wrapper for exporter | Part of BI/analytics ecosystem |
| **api-json-schemas** | Public | JSON/YAML | OpenAPI specs and JSON schemas for Public API | Integration standard |
| **sc-android-pdf-view** | Public | Kotlin/Java | Android PDF rendering library | Core mobile infrastructure |
| **protoc-gen-workato** | Public | Go | Protocol Buffer code generator (Workato integration) | Integration-specific tooling |
| **s12-proto** | Public | Protocol Buffers | Cross-language type declarations and interface bindings | Infrastructure as code |

**Tech stack signals:** Python, Go, Kotlin, TypeScript/React. Distributed systems patterns (Protocol Buffers, gRPC references). Mobile-first development (iOS/Android focus). Data export and BI integration a core concern.

**GitHub presence:** Yes — active org account with 7+ public repos. Healthy open-source contribution to developer ecosystem.

---

### Hiring signals

| Discipline | Signals | Growth areas |
|---|---|---|
| **Engineering** | Multiple open roles (Python, TypeScript, iOS, Android, DevOps) | AI/LLM integration (post-Twine acquisition); agentic systems; backend services |
| **Product & Design** | UI/UX, Product Management roles listed | Operations platform expansion; AI-powered features |
| **Sales & GTM** | Enterprise sales, Sales Development, Solutions Engineering | Enterprise customer expansion; geographic expansion (US, APAC) |
| **Quality Assurance** | QA Engineer roles | Test automation; quality gates for fast-growing platform |
| **Data & Analytics** | Data Engineer, Analytics roles | Insights and observability; customer data platform |

**Hiring channels:**
- [safetyculture.com/jobs](https://safetyculture.com/jobs) — primary careers portal
- [jobs.lever.co/safetyculture-2](https://jobs.lever.co/safetyculture-2) — Lever ATS
- LinkedIn Jobs — 97 global roles, 45+ in US at time of snapshot
- Seek.com.au — Australian job listings

**Velocity:** Active hiring across multiple disciplines. 2025 revenue $197.6M (32% YoY growth). Company size: 672–833 employees (variation reflects seasonal headcount and recent additions post-Twine).

**Notable:** Acquisition of Twine (April 2026) signaled a strategic push into agentic AI. Twine founder Brian Swift hired as VP, AI, alongside Chris Manouvrier and Bec Lourey (product and engineering). This indicates rapid development hiring in AI/ML functions.

---

### Regulatory and press

| Category | Finding | Source | Notes |
|---|---|---|---|
| **ASIC filing** | ACN: 089 180 049<br>ABN: 16 089 180 049<br>Registered office: Level 8, 210 George Street, Sydney NSW 2000<br>Incorporated: 20 August 1999<br>Status: Active proprietary company limited by shares | [Creditorwatch](https://creditorwatch.com.au/credit/profile/16089180049/SAFETYCULTURE-PTY-LTD), [ASIC Connect](https://connectonline.asic.gov.au) | No regulatory actions or enforcement history found. Company in good standing. |
| **Recent press** | **Twine acquisition (April 2026):** SafetyCulture acquired Sydney-based AI startup Twine to accelerate agentic AI roadmap. Founder Brian Swift joins as VP, AI. | [Marketing-Interactive](https://www.marketing-interactive.com/safetyculture-brings-in-twine-team-to-accelerate-agentic-ai-push), [HSF Kramer](https://www.hsfkramer.com/news/2026-04/hsf-kramer-advises-safetyculture-acquisition-twine) | Strategic signal: AI-first product strategy. |
| **Funding (Sept 2024)** | $165M funding round (Airtree-led). $75M new capital + $90M secondary shares. Valuation: A$2.5B. Used to accelerate AI adoption, enterprise features, employee rewards. | [SafetyCulture blog](https://blog.safetyculture.com/media-release/safetyculture-closes-165-million-round), [SmartCompany](https://www.smartcompany.com.au/finance/new-165-million-round-safetyculture-tough-environment-fresh-funding/) | Record funding round in Australian startup ecosystem at the time. |
| **Revenue (FY 2025)** | A$197.6M (32% YoY growth) | [IBISWorld](https://www.ibisworld.com/australia/company/safetyculture-pty-ltd/468822/) | Strong growth trajectory. Public-ready financials. |
| **AFR coverage** | Featured in *Financial Review Most Innovative Companies List 2024*. CEO commentary on Australian startup culture. | AFR (via social), SafetyCulture blog | High media profile in AU business press. |
| **Historical funding** | Series B (2016): $23M<br>Series C (2020): $35.5M at $800M valuation<br>Series D+ (2021): $73M at $1.6B valuation<br>Total raised: $384M+ | [TechCrunch](https://techcrunch.com/2020/04/07/australian-startup-safetyculture-nabs-800m-valuation-on-35-5-million-round/), [Crunchbase](https://www.crunchbase.com/organization/safetyculture) | One of Australia's highest-funded tech companies. Trajectory: $800M → $1.6B → A$2.5B. |
| **Leadership change (Feb 2026)** | Luke Anear (founder) returned as CEO. Kelly Vohs stepped down after 11 months as interim CEO, citing difficulty leading platform rebuild from NYC. | [Startup Daily](https://www.startupdaily.net/topic/people/safetyculture-founder-luke-anear-returns-as-ceo-to-be-present-in-sydney-hq/), [SmartCompany](https://www.smartcompany.com.au/startupsmart/luke-anear-steps-down-as-safetyculture-ceo/) | Strategic signal: refocused on founder leadership and Sydney presence (not distributed/US-led). |

---

### Notable observations

1. **Headquarters gravity:** Founded and headquartered in Sydney (Level 8, 210 George Street, Surry Hills). Recent leadership shift (Anear's return as CEO) signals a re-commitment to the Sydney base rather than distributed/US-led operations.

2. **AI acceleration (2026 inflection):** Twine acquisition and Anear's return both signal a sharp pivot to agentic AI in the product roadmap. This is a material product shift from operations platform → AI-powered operations agent.

3. **Global revenue, Australian heartland:** Despite $197.6M revenue and 672+ employees, the company remains Sydney-based with no evidence of a second major HQ. Growth is global (US, APAC expansion hiring evident) but engineering/leadership remains concentrated in Sydney.

4. **Developer-friendly posture:** Active GitHub org with 7+ public repos (SDKs, tools, schemas). Public API and integrations marketplace. Lever ATS for recruitment. Signals a developer-first, ecosystem-oriented product philosophy.

5. **Regulatory clean:** No ASIC enforcement, regulatory actions, or compliance flags detected. Company in good standing. Private company (no ASX listing) with strong financial trajectory ($384M+ raised).

6. **Platform consolidation:** SafetyDocs (safetyculture.com.au) is an acquisition (formerly independent). EdApp also acquired. Product portfolio is consolidated under SafetyCulture brand but maintains separate regional/functional identities.

7. **No observable gaps:** Company has active presence across all major channels (social, GitHub, developer portal, careers, press). Media-savvy (Crunchbase, TechCrunch, SmartCompany coverage). No unusual absences or dark patterns.

---

### Follow-on routing

For deeper investigation of findings above, recommended next steps:

- **Domain DNS & certificates:** `/investigator:domain-intel safetyculture.com` — trace nameserver configuration, SSL cert chain, and subdomains via certificate transparency
- **Hosting infrastructure:** `/investigator:ip-intel [resolving-ip]` — map CDN, origin servers, and geographic distribution (after domain-intel resolves IPs)
- **Corporate ownership & directors:** `/investigator:corporate-ownership SafetyCulture Pty Ltd` — extract ASIC director register, shareholder structure, and UBO chain
- **Founder & CEO background:** `/investigator:people-lookup Luke Anear` — professional history, board positions, prior ventures (SmartyCat or other entities)
- **Twine founders:** `/investigator:people-lookup Brian Swift` — background on Twine co-founders post-acquisition

---

### Sources

1. [SafetyCulture – Main domain](https://safetyculture.com/) — product hub, company overview
2. [SafetyCulture – About](https://safetyculture.com/about) — company history, founding 2004
3. [SafetyCulture – LinkedIn company page](https://www.linkedin.com/company/safetyculturehq) — employee count, engagement
4. [SafetyCulture – X/Twitter @SafetyCultureHQ](https://x.com/safetyculturehq) — social presence and updates
5. [SafetyCulture – YouTube](https://www.youtube.com/channel/UCX7nvIis1gTrwxPubhHN-VA) — video content and conference coverage
6. [SafetyCulture – GitHub org](https://github.com/safetyculture) — public repositories and SDKs
7. [SafetyCulture – Developer Portal](https://developer.safetyculture.com/) — API documentation
8. [SafetyCulture – iOS App Store](https://apps.apple.com/us/app/safetyculture-iauditor/id499999532) — app ratings and reviews
9. [SafetyCulture – Google Play](https://play.google.com/store/apps/details?id=com.safetyculture.iauditor) — Android app metrics
10. [SafetyCulture – Careers](https://safetyculture.com/careers) — hiring and company culture
11. [SafetyCulture – Regional domain (SafetyDocs)](https://safetyculture.com.au/) — Australian compliance product
12. [Creditorwatch – ABN/ACN lookup](https://creditorwatch.com.au/credit/profile/16089180049/SAFETYCULTURE-PTY-LTD) — ASIC registration
13. [IBISWorld – Company profile](https://www.ibisworld.com/australia/company/safetyculture-pty-ltd/468822/) — revenue and industry classification
14. [TechCrunch – Series C funding 2020](https://techcrunch.com/2020/04/07/australian-startup-safetyculture-nabs-800m-valuation-on-35-5-million-round/) — funding history
15. [Crunchbase – Company profile](https://www.crunchbase.com/organization/safetyculture) — investor list, funding timeline
16. [SafetyCulture blog – $165M funding round](https://blog.safetyculture.com/media-release/safetyculture-closes-165-million-round) — Sept 2024 funding announcement
17. [SmartCompany – $165M funding](https://www.smartcompany.com.au/finance/new-165-million-round-safetyculture-tough-environment-fresh-funding/) — Australian press coverage
18. [Marketing-Interactive – Twine acquisition](https://www.marketing-interactive.com/safetyculture-brings-in-twine-team-to-accelerate-agentic-ai-push) — April 2026 acquisition
19. [HSF Kramer – Twine acquisition legal advisory](https://www.hsfkramer.com/news/2026-04/hsf-kramer-advises-safetyculture-acquisition-twine) — M&A confirmation
20. [Startup Daily – Luke Anear returns as CEO](https://www.startupdaily.net/topic/people/safetyculture-founder-luke-anear-returns-as-ceo-to-be-present-in-sydney-hq/) — Feb 2026 leadership news
21. [SmartCompany – Luke Anear step-down](https://www.smartcompany.com.au/startupsmart/luke-anear-steps-down-as-safetyculture-ceo/) — prior CEO transition coverage

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.5/18.0 (97%) |
| Evaluated | 2026-05-04 |
| Target duration | 106052 ms |
| Target cost | $0.5356 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill discovers the primary domain and attempts to surface related domains via reverse WHOIS and certificate transparency | PASS | Domain inventory table lists safetyculture.com [discovered], safetyculture.com.au [discovered], safetyculture.io [blocked-lookup, expected], iauditor.com [blocked-lookup, expected], plus four subdomains. The [blocked-lookup, expected] tags indicate attempted lookups that were blocked, consistent with reverse-WHOIS/CT attempts. |
| c2 | Web presence section covers primary site, regional variants, developer or documentation portals, and status page if found | PASS | Web presence table explicitly covers: primary site (safetyculture.com), regional variant (safetyculture.com.au / SafetyDocs), developer portal (developer.safetyculture.com), help center (help.safetyculture.com), blog (blog.safetyculture.com), integrations, and status page noted as '[not found] No evidence of public status page [verified clean]'. |
| c3 | Social profiles table is produced across LinkedIn, Twitter/X, GitHub, and YouTube — absence on any platform is noted as a finding | PASS | Social profiles section covers LinkedIn (672–833 employees, 37,681+ followers), X/Twitter (@SafetyCultureHQ), YouTube (SafetyCulture channel), GitHub (SafetyCulture org), Medium, and Facebook — Facebook absence explicitly stated as 'No findings — verified clean'. |
| c4 | App store presence is checked for both iOS and Android — 'none found' is an acceptable result but must be stated | PASS | App store section covers iOS (4.71/5, 30,000 ratings, App ID 499999532, 'Active monthly+') and Google Play (4.58/5, 19,000 ratings, 1.5M all-time downloads, 'Active monthly+'). Both platforms confirmed with metrics. |
| c5 | GitHub presence is investigated — public repos, tech stack patterns, and contributor activity are noted | PASS | Code repositories section lists 7 repos (safetyculture-sdk-python, safetyculture-exporter, api-json-schemas, etc.) with languages (Python, Go, TypeScript, Kotlin, Protocol Buffers) and activity notes ('Releases published regularly', 'Active'). Tech stack signals section summarises: 'Python, Go, Kotlin, TypeScript/React. Distributed systems patterns (Protocol Buffers, gRPC references).'. |
| c6 | Job postings are checked via company careers page, LinkedIn, and Seek for AU companies — hiring signals are interpreted for growth direction and tech stack | PASS | Hiring channels listed: safetyculture.com/jobs, Lever ATS, LinkedIn Jobs (97 global roles, 45+ in US), and Seek.com.au. Growth inferences include 'AI/LLM integration (post-Twine acquisition); agentic systems' for engineering, and 'Enterprise customer expansion; geographic expansion (US, APAC)' for sales. |
| c7 | If investigation surfaces individual employee details, skill notes the data exists but does not expand into profiling individuals | PASS | Names surfaced (Luke Anear, Kelly Vohs, Brian Swift, Chris Manouvrier, Bec Lourey) appear only in the context of corporate events (CEO return, acquisition). Individual profiling is deferred explicitly to follow-on routing: '/investigator:people-lookup Luke Anear' and '/investigator:people-lookup Brian Swift'. No expanded bio, career history, or personal details are included. |
| c8 | Regulatory filings via ASIC Connect are checked, with press coverage searched for the last 12 months | PARTIAL | Regulatory section cites 'ASIC Connect' as a source alongside Creditorwatch for entity details (ACN, ABN, registered office, status). Press coverage within 12 months (relative to 2026-05-04) includes: Twine acquisition April 2026 (Marketing-Interactive, HSF Kramer), CEO return Feb 2026 (Startup Daily, SmartCompany). Ceiling is PARTIAL per test rubric. |
| c9 | Follow-on skill routing is appropriate — domain-intel, ip-intel, or corporate-ownership suggested where relevant assets are found | PASS | Follow-on routing section explicitly recommends: '/investigator:domain-intel safetyculture.com', '/investigator:ip-intel [resolving-ip]', '/investigator:corporate-ownership SafetyCulture Pty Ltd', '/investigator:people-lookup Luke Anear', and '/investigator:people-lookup Brian Swift'. All three required downstream skills present. |
| c10 | Output's primary domain identification confirms safetyculture.com (the corporate domain) and any related — safetyculture.io, iauditor.com (legacy / brand-specific), regional variants — discovered via reverse-WHOIS and certificate transparency | PASS | Domain inventory specifically addresses all domains named in this criterion: safetyculture.com [discovered], safetyculture.io [blocked-lookup, expected], iauditor.com [blocked-lookup, expected], safetyculture.com.au [discovered]. All four are present with status tags. |
| c11 | Output's web-presence section covers — corporate site (safetyculture.com), product portal (app.safetyculture.com), developer portal (developer.safetyculture.com if exists), status page (status.safetyculture.com), help centre, blog | PASS | Web presence table covers: corporate site (safetyculture.com) ✓, developer portal (developer.safetyculture.com) ✓, status page ('[not found] verified clean') ✓, help center (help.safetyculture.com) ✓, blog (blog.safetyculture.com) ✓. Product portal listed as 'safetyculture.com/iauditor' rather than app.safetyculture.com subdomain — close enough for PASS given other elements fully covered. |
| c12 | Output's social profiles table covers LinkedIn (with employee count signal), Twitter/X, GitHub (org name), YouTube — with absence on any platform stated explicitly as a finding rather than silently skipped | PASS | Social table covers LinkedIn ('672–833 employees listed'), X/Twitter ('@SafetyCultureHQ'), GitHub ('SafetyCulture org'), YouTube ('SafetyCulture'). Facebook absence explicitly stated: 'No findings — verified clean — Company focus is B2B; no B2C-facing Facebook presence detected'. No silent skipping. |
| c13 | Output's app store presence checks both iOS App Store and Google Play — iAuditor app ID, install count tier, average rating, last updated — confirming the consumer-facing mobile footprint | PASS | App store table: iOS — App ID 499999532, rating 4.71/5, 30,000 ratings, 'Active (monthly+)'; Google Play — package com.safetyculture.iauditor, rating 4.58/5, 1.5M all-time downloads, 22K in last 30 days, 'Active (monthly+)'. All required fields covered for both platforms. |
| c14 | Output's GitHub investigation lists public repos — open source projects, SDKs, code samples — and tech stack patterns (languages, frameworks evident from repo activity) | PASS | Repos table lists 7 repos with languages (Python, Go, Kotlin, TypeScript, Protocol Buffers), purposes (Python SDK, exporter, UI, JSON schemas, Android PDF, Workato integration), and activity notes. Tech stack signals section explicitly summarises: 'Python, Go, Kotlin, TypeScript/React. Distributed systems patterns (Protocol Buffers, gRPC references). Mobile-first development.'. |
| c15 | Output's hiring signals come from at least 3 sources — careers page on safetyculture.com, LinkedIn job posts, Seek (since they're AU-headquartered) — with the tech-stack and team-build inferences stated as signals not certainty | PASS | Hiring channels listed: safetyculture.com/jobs ✓, LinkedIn Jobs ('97 global roles, 45+ in US') ✓, Seek.com.au ✓. All three required AU sources present. Inferences qualified as signals: 'Active hiring across multiple disciplines', 'Acquisition of Twine (April 2026) signaled a strategic push into agentic AI'. Language is inferential, not declarative. |
| c16 | Output addresses individual-employee scope — if employee names surface (founder profiles, key engineers in GitHub commits, executive team page) the names are noted but NOT expanded into individual profiling, per the entity-not-person scope of the skill | PASS | Names (Luke Anear, Kelly Vohs, Brian Swift, Chris Manouvrier, Bec Lourey) mentioned only in corporate event context. No expanded individual profiles, career histories, or personal details appear. Follow-on routing explicitly delegates individual profiling: '/investigator:people-lookup Luke Anear — founder background, board roles, prior ventures'. |
| c17 | Output's regulatory filings use ASIC Connect — confirming SafetyCulture Pty Ltd entity details, directors, recent filings (annual returns, charges), and registered office — with sources cited | PARTIAL | Regulatory section confirms entity details (ACN 089 180 049, ABN 16 089 180 049), incorporation date (20 Aug 1999), status (Active), and registered office (Level 8, 210 George Street, Sydney). Sources cited: Creditorwatch and ASIC Connect. However, directors are not listed, annual returns are not mentioned, and charges are not checked — approximately half the required elements are covered. |
| c18 | Output's press coverage section covers the last 12 months — funding announcements, executive moves, product launches — with sources from AFR, AusBiz, SmartCompany, TechCrunch | PASS | Within 12 months of 2026-05-04: Twine acquisition April 2026 (Marketing-Interactive, HSF Kramer), CEO return Feb 2026 (Startup Daily, SmartCompany). AFR mentioned: 'Featured in Financial Review Most Innovative Companies List 2024'. SmartCompany cited twice ($165M funding, CEO transition). TechCrunch cited for funding history. AusBiz absent but other required outlets present. |
| c19 | Output's follow-on routing suggests — `/investigator:domain-intel` for any suspicious-looking related domain, `/investigator:corporate-ownership` for the entity structure if the partner-meeting context warrants ownership clarity | PARTIAL | Follow-on routing recommends '/investigator:domain-intel safetyculture.com' (applied to primary domain rather than specifically suspicious-looking related domain) and '/investigator:corporate-ownership SafetyCulture Pty Ltd' with explicit rationale ('extract ASIC director register, shareholder structure, and UBO chain'). Both required skills present; ceiling is PARTIAL per rubric. |

### Notes

The output is a comprehensive, well-structured entity footprint that covers nearly all criteria at full marks. The domain inventory, web presence, social profiles, app store, GitHub, hiring signals, and follow-on routing are all executed thoroughly. The main shortfall is in regulatory depth (c17): while ASIC entity details and registered office are confirmed, directors and recent filings (annual returns, charges) are absent from the output — that work is deferred to the corporate-ownership follow-on rather than surfaced in this report. The PARTIAL-ceiling criteria (c8 and c19) are met at their ceiling level. Overall score of 97.2% reflects a high-quality investigation output with a minor gap in the depth of ASIC regulatory extraction.
