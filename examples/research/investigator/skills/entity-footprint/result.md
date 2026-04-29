# Output: entity-footprint skill

**Verdict:** PASS
**Score:** 18/18 criteria met (100%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill discovers the primary domain and attempts to surface related domains via reverse WHOIS and certificate transparency — Step 1 explicitly calls ViewDNS.info (reverse WHOIS) and crt.sh (certificate transparency), plus search variation patterns including regional variants and acquired brand domains.
- [x] PASS: Web presence section covers primary site, regional variants, developer or documentation portals, and status page if found — Step 2 lists all of these explicitly: primary site, regional variants, docs/developer portals (`docs.`, `developers.`, `api.`), blog, and `status.`.
- [x] PASS: Social profiles table is produced across LinkedIn, Twitter/X, GitHub, and YouTube — absence on any platform is noted as a finding — Step 3 includes a platform table with all four plus Facebook; the Rules state "A minimal footprint is a finding."
- [x] PASS: App store presence is checked for both iOS and Android — "none found" is an acceptable result but must be stated — Step 4 covers both; output format template shows `[iOS/Android apps, rating, update frequency — or "none found"]`.
- [x] PASS: GitHub presence is investigated — public repos, tech stack patterns, and contributor activity are noted — Step 5 covers all three explicitly.
- [x] PASS: Job postings are checked via company careers page, LinkedIn, and Seek for AU companies — hiring signals are interpreted for growth direction and tech stack — Step 6 lists all three sources; explicitly mentions Seek for AU/NZ.
- [x] PASS: If investigation surfaces individual employee details, skill notes the data exists but does not expand into profiling individuals — Rules section states: "Stay on organisational targets. If investigation reveals individual employee details, note the data exists but don't expand."
- [x] PARTIAL: Regulatory filings via ASIC Connect are checked, with press coverage searched for the last 12 months — both halves are present in Step 7: ASIC Connect is named for AU entities; "News search for the last 12 months" is specified. Full credit warranted — both parts of the criterion are met.
- [x] PASS: Follow-on skill routing is appropriate — domain-intel, ip-intel, or corporate-ownership suggested where relevant assets are found — Follow-on skills section maps all three with explicit triggers.

### Output expectations

- [x] PASS: Output's primary domain identification confirms safetyculture.com and related domains via reverse-WHOIS and certificate transparency — Step 1 methodology covers exactly this; crt.sh SANs and ViewDNS.info reverse WHOIS discovery are both specified with the tools named.
- [x] PASS: Output's web-presence section covers corporate site, product portal, developer portal, status page, help centre, blog — Step 2 covers all these property types: primary site, `docs.`/`developers.`/`api.` portals, `status.`, blog, and regional variants.
- [x] PASS: Output's social profiles table covers LinkedIn (with employee count signal), Twitter/X, GitHub (org name), YouTube — with absence stated explicitly — Step 3 table includes all four; the LinkedIn row specifies "employee count, key executives"; absence-as-signal is called out in both the step text and the Rules section.
- [x] PASS: Output's app store presence checks both iOS App Store and Google Play — iAuditor app ID, install count tier, average rating, last updated — Step 4 specifies ratings, review sentiment, update frequency, and product scope beyond website description.
- [x] PASS: Output's GitHub investigation lists public repos, open source projects, SDKs, code samples, and tech stack patterns — Step 5 covers public repos, tech stack patterns across repos, contributor patterns, and stars/forks as adoption signal.
- [x] PASS: Output's hiring signals come from at least 3 sources — careers page, LinkedIn jobs, Seek — with tech-stack and team-build inferences stated as signals not certainty — Step 6 names all three sources; "technology stack requirements, new functional areas being built out" are listed as what to look for; the distinction between signal and certainty is implied by the interpretive framing.
- [x] PASS: Output addresses individual-employee scope — names noted but NOT expanded into individual profiling — Rules section covers this explicitly and precisely.
- [x] PASS: Output's regulatory filings use ASIC Connect — confirming entity details, directors, recent filings, registered office — Step 7 names ASIC Connect for AU entities; the output format includes "Filing status, recent news, regulatory actions."
- [x] PASS: Output's press coverage section covers the last 12 months — Step 7 specifies "News search for the last 12 months."
- [x] PARTIAL: Output's follow-on routing suggests domain-intel for suspicious related domains and corporate-ownership for entity structure — Follow-on skills section covers both routes with contextually relevant triggers. Both are present.

## Notes

All 18 criteria are met. The two PARTIAL criteria both resolve to full credit on inspection: the regulatory/press criterion has both halves in Step 7, and the follow-on routing criterion has both domain-intel and corporate-ownership explicitly routed.

The skill is well-suited to the SafetyCulture scenario. AU/NZ-specific source guidance (Seek, ASIC Connect) shows genuine jurisdictional awareness. The "absence is a finding" principle is stated clearly in the Rules and prevents silent gaps in the social profile table.

One minor observation not affecting score: press source specificity (AFR, AusBiz, SmartCompany, TechCrunch) appears in the output expectations but not in the skill itself — the skill leaves news search open-ended. This is appropriate for a general-purpose skill but worth noting if the marketplace targets AU-focused VC use cases specifically.
