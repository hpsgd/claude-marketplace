# Result: domain-intel skill

**Verdict:** PARTIAL
**Score:** 16.5/19 criteria met (87%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill logs the stated purpose (security research) before starting investigation — output format template has `**Purpose logged:** [stated purpose]` as a required header field.
- [x] PASS: WHOIS lookup uses the correct registry for the TLD (.com — who.is or equivalent generic TLD registry) — Step 1 defines ".com/.net/.org and generic TLDs: who.is or registrar lookup."
- [x] PASS: DNS records are fetched covering A, AAAA, MX, TXT, NS records — Step 2 lists A, AAAA, MX, TXT, NS, CNAME explicitly. TXT records are called out for SPF/DKIM and third-party service interpretation.
- [x] PASS: Certificate transparency via crt.sh is searched for subdomains and naming patterns — Step 3 defines this with crt.sh; covers subdomains, naming patterns, certificate issuer, and history.
- [x] PASS: ASN and hosting provider are identified via ipinfo.io or BGP.he.net — Step 4 names both tools explicitly. Identifies hosting provider, ASN, IP range, and geolocation.
- [x] PASS: Historical data via Wayback Machine is checked — Step 6 defines Wayback Machine check. "Historical gaps (domain registered but no Wayback content for a period) can be significant."
- [x] PASS: Privacy-protected WHOIS is logged as a finding, not a failure — Step 1: "log this as a finding, not a failure. Proceed with DNS and certificate transparency." Reinforced in Rules.
- [~] PARTIAL: Follow-on skill routing is indicated — the Follow-on skills section defines routing to `/investigator:ip-intel` for IP investigation and further `domain-intel` runs for related domains. Scored 0.5 because routing is in a standalone section, not embedded in the output format template, so it is not structurally enforced.
- [x] PASS: Passive methods only — Rules block: "Passive methods only. Never attempt active scanning, port enumeration, or authenticated access."

### Output expectations

- [x] PASS: Output logs stated purpose at top — output format template has `**Purpose logged:** [stated purpose]` as the second header field, before any lookup sections.
- [x] PASS: Output's WHOIS lookup uses a generic-TLD source for .com — Step 1 specifies who.is for .com/.net/.org and generic TLDs.
- [x] PASS: Output's DNS records cover A, AAAA, MX, TXT, NS with values and TXT interpretation — Step 2 and the DNS records output section: "Key records with interpretation — not just raw data."
- [x] PASS: Output's certificate transparency search via crt.sh returns subdomain history and naming patterns — Step 3 and "Certificate transparency findings" output section cover both.
- [~] PARTIAL: Output's ASN/hosting identification names AS number, org, and provider, flagging bulletproof/abuse-source providers — ipinfo.io and BGP.he.net are specified for ASN and provider, but the skill has no explicit instruction to flag bulletproof or common-abuse-source ASNs. The agent would need to apply this judgment without being directed to.
- [x] PASS: Output's Wayback Machine check treats registration-vs-first-content gap as a finding — Step 6 states this explicitly and the output format has a dedicated Historical findings section.
- [x] PASS: Output handles privacy-protected WHOIS as a finding and continues investigation — covered in both Step 1 and the Rules block.
- [ ] FAIL: Output queries reputation sources — VirusTotal, URLhaus, AbuseIPDB on resolving IP, AlienVault OTX — the skill does not include any reputation database step. None of these tools appear anywhere in the skill definition.
- [~] PARTIAL: Output recommends follow-on routing to `/investigator:ip-intel` and further `domain-intel` runs — Follow-on skills section covers both cases, but the output format template has no corresponding `### Next steps` section, so routing suggestions depend on the agent reading the separate section.
- [x] PASS: Output uses passive methods only — Rules block prohibits active scanning, port enumeration, and authenticated access.

## Notes

The reputation sources gap (VirusTotal, URLhaus, AbuseIPDB, AlienVault OTX) is the most significant miss for the threat-intel use case demonstrated in the prompt. A C2 investigation without reputation database checks leaves out the most actionable passive signals — whether the domain or its resolving IP already appears in threat feeds. Adding a Step 7 for reputation lookup would address this directly.

The follow-on routing PARTIAL is a structural issue rather than a substance issue: the routing logic is correct and complete, but it sits in a detached section. An agent completing a domain-intel run could overlook it. Adding a `### Next steps` field to the output format template with conditional routing prompts would fix this.

The bulletproof-hosting flag is a minor gap — the skill identifies the hosting provider correctly but doesn't direct the agent to cross-reference against known abuse-source ASN lists (e.g. AS49392 for CDN77, common bulletproof hosts). A note in Step 4 would close this.
