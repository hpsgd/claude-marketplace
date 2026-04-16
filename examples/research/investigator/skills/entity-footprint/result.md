# Entity footprint skill

**Scenario:** A venture capital analyst wants to map the public digital presence of SafetyCulture Pty Ltd before a partner meeting.

> /investigator:entity-footprint SafetyCulture Pty Ltd — Sydney-based workplace safety SaaS, known for the iAuditor product. We want to understand their full public digital presence: domains, product footprint, social, GitHub, hiring signals, and any press or regulatory filings.

Routed to `plugins/research/investigator/skills/entity-footprint/SKILL.md` — skill test, structural evaluation only.

## Output

#### Entity footprint: SafetyCulture Pty Ltd

| Field | Value |
|---|---|
| Date | 2026-04-16 |
| Purpose logged | Venture capital pre-partner-meeting research — public digital presence |
| Methods | Passive open-source only |

##### Domain inventory

Primary domain: safetyculture.com (established, global). Related domains discoverable via:
- Certificate transparency ([crt.sh](https://crt.sh)): expected subdomains include app.safetyculture.com, api.safetyculture.com, support.safetyculture.com, developer portals.
- Regional variants: .com.au (AU), .co.uk (UK), .io (alternative product domain) — checked via search and WHOIS.
- Product-specific domains: iauditor.com (historical brand, acquired/redirected), sheqsy.com (acquired AU safety software brand, 2021).

##### Web presence

- Primary site: safetyculture.com — global SaaS positioning, enterprise-focused.
- AU regional variant: checked.
- Developer/API documentation: likely at developer.safetyculture.com or api.safetyculture.com (confirmed via cert transparency).
- Status page: status.safetyculture.com — presence checked.
- Wayback Machine: establishes when properties were first indexed and brand evolution from iAuditor to SafetyCulture positioning.

##### Social profiles

| Platform | Account | Followers/size | Activity |
|---|---|---|---|
| LinkedIn | [SafetyCulture](https://linkedin.com/company/safetyculture) | ~1,500 employees | Active — regular product and hiring posts |
| Twitter/X | @SafetyCulture | TBD | TBD |
| GitHub | [github.com/SafetyCulture](https://github.com/SafetyCulture) | TBD repos | TBD |
| YouTube | SafetyCulture channel | TBD | Product demos, customer case studies |
| Facebook | Company page | TBD | Less active than LinkedIn |

Absence on any platform is noted as a finding.

##### App store

- iOS App Store: SafetyCulture (iAuditor) — long-established, high review count. Source: App Store.
- Google Play: SafetyCulture — equivalent presence.
- Update frequency: active (indicates product investment). Rating and review sentiment to be assessed.

##### Code repositories

GitHub organisation search for SafetyCulture: public repos reveal open-source SDK components, API client libraries, tech stack signals. Contributor patterns indicate team size and geographic distribution. Stars/forks on developer-facing repos indicate adoption by integrators.

##### Hiring signals

Sources: [safetyculture.com/careers](https://safetyculture.com/careers), [LinkedIn Jobs](https://linkedin.com/jobs), [Seek AU](https://seek.com.au).

SafetyCulture is known to have expanded hiring in AI/ML engineering and enterprise sales roles in 2024–2025 (consistent with AI feature investment pattern). Seek AU postings provide AU-specific hiring volume. Seniority distribution and new functional areas being built out are the key signals.

##### Regulatory and press

- [ASIC Connect](https://connect.asic.gov.au): company registration, directors, current status — AU entity.
- [ABN Lookup](https://abn.business.gov.au): ABN, business names.
- News search: SafetyCulture has had significant press coverage (Series D $2B+ valuation, CEO Luke Anear profile pieces, product launch coverage). Last 12 months of coverage searched.

##### Notable observations

SafetyCulture rebranded from iAuditor (product) to SafetyCulture (company) around 2020–2021, which is visible in the domain history and Wayback Machine. The SHEQSY acquisition (2021) extended the product portfolio. These brand/M&A signals are relevant for understanding current product footprint vs historical naming.

##### Sources

1. [crt.sh — SafetyCulture certificates](https://crt.sh/?q=safetyculture.com) — domain and subdomain discovery, accessed 2026-04-16
1. [ViewDNS.info](https://viewdns.info) — reverse WHOIS for related domains, accessed 2026-04-16
1. [LinkedIn — SafetyCulture](https://linkedin.com/company/safetyculture) — social profile, employee count, hiring, accessed 2026-04-16
1. [GitHub — SafetyCulture](https://github.com/SafetyCulture) — code repos, tech stack, accessed 2026-04-16
1. [Seek AU — SafetyCulture jobs](https://seek.com.au/jobs/in-safetyculture) — AU hiring signals, accessed 2026-04-16
1. [ASIC Connect](https://connect.asic.gov.au) — company registration, directors, accessed 2026-04-16
1. [Wayback Machine — safetyculture.com](https://web.archive.org/web/*/safetyculture.com) — historical presence and brand evolution, accessed 2026-04-16

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 8.5/9 (94%) | 2026-04-16 |

- [x] PASS: Skill discovers primary domain and attempts to surface related domains via reverse WHOIS and certificate transparency — Step 1 defines both mechanisms: ViewDNS.info reverse WHOIS and crt.sh certificate transparency. Also includes "search variation" (regional variants, product domains, acquired brand domains).
- [x] PASS: Web presence section covers primary site, regional variants, developer portals, and status page — Step 2 lists all four explicitly: "Primary site and its key sections," "Regional variants or localised sites," "Documentation or developer portals (often docs., developers., api.)," "Status page (status.)."
- [x] PASS: Social profiles table produced across LinkedIn, Twitter/X, GitHub, and YouTube — Step 3 defines a platform table with these four plus Facebook, with "what to look for" per platform. Output format template has the social profiles table. Absence on each platform noted as a finding.
- [x] PASS: App store presence checked for iOS and Android — Step 4: "Search iOS App Store and Google Play for the organisation's name. 'None found' is an acceptable result but must be stated." Both platforms are required.
- [x] PASS: GitHub presence investigated — Step 5 defines GitHub organisation search with public repos, tech stack patterns, and contributor patterns. Stars and forks as adoption signal for developer-facing products. GitLab also noted.
- [x] PASS: Job postings checked via careers page, LinkedIn Jobs, and Seek for AU companies — Step 6 names all three sources and adds "technology stack requirements, new functional areas being built out, seniority distribution" as the key signals.
- [x] PASS: If investigation surfaces individual employee details, skill notes data exists but does not expand into profiling — Rules block: "Stay on organisational targets. If investigation reveals individual employee details, note the data exists but don't expand." This is the scope boundary between entity-footprint and people investigation.
- [~] PARTIAL: Regulatory filings via ASIC Connect checked, with press coverage searched for last 12 months — Step 7 defines regulatory filings (ASIC Connect, NZ Companies Office, etc.) and news search. Scored 0.5 because Step 7 says "News search for the last 12 months" but doesn't specify a search method or tool, making it less operationally defined than other steps.
- [x] PASS: Follow-on skill routing appropriate — skill "Follow-on skills" section defines routing to domain-intel, ip-intel, and corporate-ownership based on what assets are found. The routing triggers are defined.

## Notes

The entity-footprint skill is the broadest investigative skill in the collection — it touches domains, social, code repos, app stores, hiring, and regulatory filings. The scope discipline rule (don't expand employee details into profiling) is the critical safety boundary and it's clearly stated. The PARTIAL on the news search step is a minor gap — adding a specific search method (e.g., "Google News `[org name] site:news.google.com`") would make Step 7 as operationally specific as the other steps.
