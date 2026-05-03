# Test: domain-intel skill

Scenario: A security analyst wants to investigate a domain that appeared in a threat report as a potential command-and-control host.

## Prompt

/investigator:domain-intel trackupdate-cdn77.com — flagged in a threat intel report as potentially acting as a C2 host. Security research context.

A few specifics for the response:

- ASN/hosting section MUST name `ipinfo.io` and `BGP.he.net` as the lookup tools used (or attempted, if blocked). Even if the domain is NXDOMAIN, list the tools attempted in the Sources table.
- Reputation lookups MUST cover URLhaus and AbuseIPDB by name in addition to VirusTotal, OTX, urlscan.io, ThreatFox. List each in the Sources table with the URL attempted and the result (or "blocked / inaccessible" if not reachable).
- Wayback Machine check MUST be in its own section. If captures are not retrievable, still produce the registration-date-vs-first-archive gap analysis (e.g. "registered 2024-MM-DD, first capture not retrievable — gap unverifiable").
- Conclude with a **Follow-on Routing** section that explicitly recommends `/investigator:ip-intel <resolved-ip>` if an A record exists, AND `/investigator:domain-intel <related-domain>` for any related domains surfaced by reverse lookup or certificate transparency.

## Criteria

- [ ] PASS: Skill logs the stated purpose (security research) before starting investigation
- [ ] PASS: WHOIS lookup uses the correct registry for the TLD (.com — who.is or equivalent generic TLD registry)
- [ ] PASS: DNS records are fetched covering A, AAAA, MX, TXT, NS records — TXT records interpreted for third-party service signals
- [ ] PASS: Certificate transparency via crt.sh is searched for subdomains and naming patterns
- [ ] PASS: ASN and hosting provider are identified via ipinfo.io or BGP.he.net
- [ ] PASS: Historical data via Wayback Machine is checked — gaps in history (no content for a period after registration) are noted as findings
- [ ] PASS: Privacy-protected WHOIS is logged as a finding, not a failure — investigation continues with DNS and certificate transparency
- [ ] PARTIAL: Follow-on skill routing is indicated — if A record warrants IP investigation, `/investigator:ip-intel` is suggested; if related domains are found, further domain-intel runs are suggested
- [ ] PASS: Passive methods only — no active scanning or enumeration attempted

## Output expectations

- [ ] PASS: Output logs the stated purpose — security research / C2 host investigation per threat report — at the top before any lookup
- [ ] PASS: Output's WHOIS lookup uses a generic-TLD source (who.is, whoisxml, ICANN lookup) for trackupdate-cdn77.com — not registry-specific tools that don't apply to .com
- [ ] PASS: Output's DNS records cover A, AAAA, MX, TXT, NS — with the actual record values shown (or "no record" if absent) — and TXT records are interpreted for SPF / DKIM / DMARC / verification tokens that signal third-party services in use
- [ ] PASS: Output's certificate transparency search via crt.sh returns the subdomain history — listing seen subdomains (e.g. cdn.trackupdate-cdn77.com, api.trackupdate-cdn77.com) and naming patterns that may reveal service typology
- [ ] PASS: Output's ASN / hosting identification uses ipinfo.io, BGP.he.net, or equivalent passive lookup — naming the AS number, AS organisation, and hosting provider; flagging if hosted on bulletproof / common abuse-source providers
- [ ] PASS: Output's Wayback Machine check shows historical content — registration date vs first archived content gap is a finding (legitimate domains usually have content soon after registration; C2 domains often don't)
- [ ] PASS: Output handles privacy-protected WHOIS as a finding (typical for malicious infrastructure) — does NOT stop the investigation; continues with DNS, certificate transparency, and reputation databases
- [ ] PASS: Output queries reputation sources — VirusTotal, URLhaus, AbuseIPDB on the resolving IP, AlienVault OTX — with the lookup URLs and the result counts / verdict per source
- [ ] PASS: Output recommends follow-on routing — if the A record points to interesting infrastructure (e.g. shared IP with other known-bad domains), routes to `/investigator:ip-intel`; if related domains surface via reverse lookup, recommends additional `/investigator:domain-intel` runs
- [ ] PASS: Output uses passive methods only — no active port scans, no curl to fetch the actual domain content, no DNS bruteforce — staying strictly within passive OSINT scope
