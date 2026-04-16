# Test: domain-intel skill

Scenario: A security analyst wants to investigate a domain that appeared in a threat report as a potential command-and-control host.

## Prompt

/investigator:domain-intel trackupdate-cdn77.com — flagged in a threat intel report as potentially acting as a C2 host. Security research context.

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
