# Test: entity-footprint skill

Scenario: A venture capital analyst wants to map the public digital presence of SafetyCulture Pty Ltd (the iAuditor/SafetyCulture platform) before a partner meeting.

## Prompt

/investigator:entity-footprint SafetyCulture Pty Ltd — Sydney-based workplace safety SaaS, known for the iAuditor product. We want to understand their full public digital presence: domains, product footprint, social, GitHub, hiring signals, and any press or regulatory filings.

Output structure:

1. **Domain inventory** — primary domain (`safetyculture.com`), related domains via reverse-WHOIS / certificate transparency (`safetyculture.io`, `iauditor.com`, `safetyculture.com.au`). State each as `[discovered]` or `[blocked-lookup, expected]`.
2. **Product footprint** — apps (iAuditor on iOS App Store + Google Play with download / review counts), web product surface, integrations marketplace.
3. **Social** — LinkedIn company page (employee count + growth), Twitter/X handle, YouTube channel, podcast presence.
4. **GitHub** — `github.com/safetyculture` org if exists, public repos, contributor activity.
5. **Hiring signals** — Seek, LinkedIn Jobs, company careers page. Roles open per discipline (eng / sales / product). Hiring velocity hint.
6. **Press coverage** — AFR, SmartCompany, Crikey, TechCrunch coverage of the company.
7. **Regulatory filings** — **ASIC Connect** (`https://connectonline.asic.gov.au`) for ABN, directors, registered office. ACN if known. Plus press coverage of any regulatory matters.
8. **Follow-on routing** (mandatory): explicit recommendations for downstream skills:
   - `/investigator:domain-intel safetyculture.com` for full DNS/cert footprint
   - `/investigator:ip-intel <resolving-ip>` for hosting infrastructure
   - `/investigator:corporate-ownership SafetyCulture Pty Ltd` for full ASIC director and shareholder extract
   - `/investigator:people-lookup <CEO-name>` for the founder/CEO background

A few specifics for the response:

- Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
- Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
- For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
- When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
- Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Criteria

- [ ] PASS: Skill discovers the primary domain and attempts to surface related domains via reverse WHOIS and certificate transparency
- [ ] PASS: Web presence section covers primary site, regional variants, developer or documentation portals, and status page if found
- [ ] PASS: Social profiles table is produced across LinkedIn, Twitter/X, GitHub, and YouTube — absence on any platform is noted as a finding
- [ ] PASS: App store presence is checked for both iOS and Android — "none found" is an acceptable result but must be stated
- [ ] PASS: GitHub presence is investigated — public repos, tech stack patterns, and contributor activity are noted
- [ ] PASS: Job postings are checked via company careers page, LinkedIn, and Seek for AU companies — hiring signals are interpreted for growth direction and tech stack
- [ ] PASS: If investigation surfaces individual employee details, skill notes the data exists but does not expand into profiling individuals
- [ ] PARTIAL: Regulatory filings via ASIC Connect are checked, with press coverage searched for the last 12 months
- [ ] PASS: Follow-on skill routing is appropriate — domain-intel, ip-intel, or corporate-ownership suggested where relevant assets are found

## Output expectations

- [ ] PASS: Output's primary domain identification confirms safetyculture.com (the corporate domain) and any related — safetyculture.io, iauditor.com (legacy / brand-specific), regional variants — discovered via reverse-WHOIS and certificate transparency
- [ ] PASS: Output's web-presence section covers — corporate site (safetyculture.com), product portal (app.safetyculture.com), developer portal (developer.safetyculture.com if exists), status page (status.safetyculture.com), help centre, blog
- [ ] PASS: Output's social profiles table covers LinkedIn (with employee count signal), Twitter/X, GitHub (org name), YouTube — with absence on any platform stated explicitly as a finding rather than silently skipped
- [ ] PASS: Output's app store presence checks both iOS App Store and Google Play — iAuditor app ID, install count tier, average rating, last updated — confirming the consumer-facing mobile footprint
- [ ] PASS: Output's GitHub investigation lists public repos — open source projects, SDKs, code samples — and tech stack patterns (languages, frameworks evident from repo activity)
- [ ] PASS: Output's hiring signals come from at least 3 sources — careers page on safetyculture.com, LinkedIn job posts, Seek (since they're AU-headquartered) — with the tech-stack and team-build inferences stated as signals not certainty
- [ ] PASS: Output addresses individual-employee scope — if employee names surface (founder profiles, key engineers in GitHub commits, executive team page) the names are noted but NOT expanded into individual profiling, per the entity-not-person scope of the skill
- [ ] PASS: Output's regulatory filings use ASIC Connect — confirming SafetyCulture Pty Ltd entity details, directors, recent filings (annual returns, charges), and registered office — with sources cited
- [ ] PASS: Output's press coverage section covers the last 12 months — funding announcements, executive moves, product launches — with sources from AFR, AusBiz, SmartCompany, TechCrunch
- [ ] PARTIAL: Output's follow-on routing suggests — `/investigator:domain-intel` for any suspicious-looking related domain, `/investigator:corporate-ownership` for the entity structure if the partner-meeting context warrants ownership clarity
