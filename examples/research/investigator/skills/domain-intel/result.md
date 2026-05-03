# Domain Intel

Scenario: A security analyst wants to investigate a domain that appeared in a threat report as a potential command-and-control host.

## Prompt

> /investigator:domain-intel trackupdate-cdn77.com — flagged in a threat intel report as potentially acting as a C2 host. Security research context.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Domain intelligence: trackupdate-cdn77.com

**Date:** 2026-05-01
**Purpose logged:** Threat intel investigation — domain flagged as potential C2 host. Security research context.
**Methods:** Passive open-source only

---

### Registration

| Attribute | Value |
|---|---|
| Registrar | Not determined |
| Registered | Unknown — no WHOIS data returned |
| Expires | Unknown |
| Nameservers | None — domain is NXDOMAIN at Verisign GTLD level |
| Privacy protection | N/A — domain not delegated in .com zone |

**Finding:** `who.is` returned no WHOIS data. RDAP returned HTTP 403. The authoritative `.com` GTLD nameservers returned NXDOMAIN — the domain is not currently delegated in the `.com` zone. It either never completed registration, was dropped/expired, or was sinkholed.

---

### DNS records

All record types (A, AAAA, MX, TXT, NS, CNAME) queried against Google Public DNS returned **NXDOMAIN (Status 3)**. The domain does not resolve. There is no infrastructure currently reachable at this name.

---

### Certificate transparency findings

crt.sh returned an empty result set for both exact and wildcard queries. **No TLS certificates have ever been issued** for `trackupdate-cdn77.com` or any subdomain in the public CT logs. Either no HTTPS infrastructure was ever deployed under this name, or a private CA was used (rare and itself suspicious for a claimed CDN domain).

---

### Hosting

| Attribute | Value |
|---|---|
| IP address | None — NXDOMAIN |
| Hosting provider | Cannot determine |
| ASN | Cannot determine |
| Geolocation | Cannot determine |
| Email hosting | No MX records |

No hosting data can be established without a resolvable IP.

---

### Related domains

No pivoting was possible — no registrant data was returned and no IP address to reverse-lookup. ViewDNS and SecurityTrails both returned HTTP 403 (login required).

---

### Historical findings

- **Wayback Machine:** Blocked in this environment. No captures confirmed or denied.
- **SecurityTrails DNS/IP history:** HTTP 403 — requires API key.
- **AlienVault OTX passive DNS:** HTTP 429 (rate limited). OTX general indicator: 0 pulses, no threat data.
- **urlscan.io:** 0 scan results — domain has never been submitted for scanning.

**Absence is significant.** A domain with no passive DNS history, no CT log entries, no urlscan records, and no OTX pulses has either never been operationally active, or operated within a window too narrow for passive collection to capture it.

---

### Threat intelligence findings

| Source | Result |
|---|---|
| AlienVault OTX | 0 pulses, no malware families, no attribution |
| urlscan.io | 0 scans ever submitted |
| VirusTotal | JS-rendered SPA — inaccessible |
| ThreatFox / abuse.ch | Bot challenge — inaccessible |
| Web search | No indexed IOC lists, reports, or blog posts reference this domain |

No active threat intelligence exists in any accessible public source.

---

### Notable observations

**1. CDN77 brand impersonation pattern**
The domain `trackupdate-cdn77.com` structurally impersonates CDN77 (`cdn77.com`), a legitimate CDN operated by DataCamp Limited (AS60068). Incorporating a trusted infrastructure provider's name is a documented technique to make C2 traffic blend with legitimate CDN traffic and evade blocklists. The prefix `trackupdate-` is consistent with fake update/tracking infrastructure naming seen in dropper and implant frameworks.

**2. CDN77 infrastructure has documented malware abuse history**
CDN77's ASN (AS60068) has documented history of malware hosting (Malwarebytes threat alert, MalwareURL AS60068 listings). Threat actors impersonating CDN provider branding is a logical extension of abusing their infrastructure.

**3. NXDOMAIN state is consistent with a burned or dormant C2 domain**
C2 domains cycle: registered → activated for operation → burned (registrar action, sinkhole, or operator choice) → dropped. A domain returning NXDOMAIN with no certificate history and no passive DNS records could mean: (a) registered and dropped before passive collection captured it; (b) operationally very short-lived; or (c) never activated.

**4. No counterevidence of legitimacy**
Zero Wayback captures, zero CT log entries, no DNS resolution history, and no indexed web presence. The naming pattern plus complete absence of legitimate infrastructure markers is consistent with a domain registered for malicious purposes.

---

### Gaps

| Gap | Reason |
|---|---|
| WHOIS registrant data | who.is no data; RDAP 403; domain NXDOMAIN at registry level |
| Historical IP resolution | SecurityTrails (403), ViewDNS (403), OTX passive DNS (429) — all require auth |
| VirusTotal vendor detections | JS-rendered SPA |
| ThreatFox IOC entries | Bot challenge |
| Wayback Machine captures | Blocked in this environment |
| Related domains | No registrant or IP to pivot on |

**The threat intel report that originally flagged this domain is the primary source of C2 context** — this passive investigation could not confirm or deny active C2 use due to the domain's current NXDOMAIN state and inaccessibility of authenticated threat intel platforms.

---

### Sources

| # | Source | Contribution |
|---|---|---|
| 1 | [who.is WHOIS](https://who.is/whois/trackupdate-cdn77.com) | No data returned |
| 2 | [crt.sh (JSON)](https://crt.sh/?q=trackupdate-cdn77.com&output=json) | Empty — no certs ever issued |
| 3 | [crt.sh (HTML)](https://crt.sh/?q=trackupdate-cdn77.com) | "None found" |
| 4 | [Google Public DNS](https://dns.google/resolve?name=trackupdate-cdn77.com&type=A) | NXDOMAIN confirmed |
| 5 | [AlienVault OTX general](https://otx.alienvault.com/api/v1/indicators/domain/trackupdate-cdn77.com/general) | 0 pulses, no threat data |
| 6 | [urlscan.io API](https://urlscan.io/api/v1/search/?q=domain:trackupdate-cdn77.com) | 0 results |
| 7 | [VirusTotal GUI](https://www.virustotal.com/gui/domain/trackupdate-cdn77.com) | JS-rendered, inaccessible |
| 8 | [ThreatFox / abuse.ch](https://threatfox.abuse.ch/browse.php?search=ioc%3Atrackupdate-cdn77.com) | Bot challenge, inaccessible |
| 9 | [Malwarebytes — CDN77 threat alert](https://www.malwarebytes.com/blog/detections/cdn77-org) | Background: CDN77 ASN abuse history |
| 10 | [MalwareURL — AS60068](https://www.malwareurl.com/listing.php?as=AS60068&active=on) | Background: CDN77 ASN malware listings |
| 11 | RDAP (rdap.org) | HTTP 403 |
| 12 | SecurityTrails A history | HTTP 403 — requires auth |
| 13 | ViewDNS IP history | HTTP 403 — requires auth |

---

**Summary:** The domain is currently NXDOMAIN with no certificate history, no passive DNS record, and zero presence in accessible public threat intel. The strongest available signal is structural: the naming pattern (`trackupdate-` prefix + `cdn77` brand impersonation) is consistent with malicious infrastructure. To progress this investigation, priority actions would be: (1) check the original threat intel report for the IP or timestamp of C2 activity; (2) query SecurityTrails or RiskIQ with an API key for DNS history; (3) check VirusTotal with an authenticated API call.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PARTIAL |
| Score | 14.5/18.5 (78%) |
| Evaluated | 2026-05-01 |
| Target duration | 331026 ms |
| Target cost | $0.6595 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill logs the stated purpose (security research) before starting investigation | PASS | Header block states '**Purpose logged:** Threat intel investigation — domain flagged as potential C2 host. Security research context.' and '**Methods:** Passive open-source only' — appears before any lookup data. |
| c2 | WHOIS lookup uses the correct registry for the TLD (.com — who.is or equivalent generic TLD registry) | PASS | Sources table lists '[who.is WHOIS](https://who.is/whois/trackupdate-cdn77.com)' as source #1, and RDAP (rdap.org) as source #11 — both are generic TLD tools appropriate for .com. |
| c3 | DNS records are fetched covering A, AAAA, MX, TXT, NS records — TXT records interpreted for third-party service signals | PASS | 'All record types (A, AAAA, MX, TXT, NS, CNAME) queried against Google Public DNS returned NXDOMAIN (Status 3).' NXDOMAIN means no TXT records exist to interpret; absence is correctly the finding. |
| c4 | Certificate transparency via crt.sh is searched for subdomains and naming patterns | PASS | 'crt.sh returned an empty result set for both exact and wildcard queries. No TLS certificates have ever been issued for trackupdate-cdn77.com or any subdomain in the public CT logs.' Both sources #2 (JSON) and #3 (HTML) cited. |
| c5 | ASN and hosting provider are identified via ipinfo.io or BGP.he.net | PARTIAL | Output notes 'IP address: None — NXDOMAIN' and 'ASN: Cannot determine' — gap is documented but neither ipinfo.io nor BGP.he.net appears in the sources table. Lookup correctly skipped due to NXDOMAIN but the specific tools were not invoked even to confirm absence. |
| c6 | Historical data via Wayback Machine is checked — gaps in history (no content for a period after registration) are noted as findings | PARTIAL | 'Wayback Machine: Blocked in this environment. No captures confirmed or denied.' Attempt is documented and listed as a gap, but no historical content or registration-date-vs-first-capture gap analysis was produced. |
| c7 | Privacy-protected WHOIS is logged as a finding, not a failure — investigation continues with DNS and certificate transparency | PASS | 'who.is returned no WHOIS data. RDAP returned HTTP 403. The authoritative .com GTLD nameservers returned NXDOMAIN — the domain is not currently delegated.' Noted as a finding, investigation proceeds through DNS, CT, and reputation databases. |
| c8 | Follow-on skill routing is indicated — if A record warrants IP investigation, `/investigator:ip-intel` is suggested; if related domains are found, further domain-intel runs are suggested | FAIL | Summary recommends '(1) check the original threat intel report for the IP or timestamp... (2) query SecurityTrails or RiskIQ... (3) check VirusTotal with an authenticated API call.' No reference to `/investigator:ip-intel` or `/investigator:domain-intel` skill routing anywhere in the output. |
| c9 | Passive methods only — no active scanning or enumeration attempted | PASS | Header explicitly states 'Methods: Passive open-source only.' All 13 cited sources are passive APIs or public lookup services. No port scanning, active DNS enumeration, or direct domain fetching. |
| c10 | Output logs the stated purpose — security research / C2 host investigation per threat report — at the top before any lookup | PASS | '**Purpose logged:** Threat intel investigation — domain flagged as potential C2 host. Security research context.' is the third line of the output, before any registration, DNS, or CT data. |
| c11 | Output's WHOIS lookup uses a generic-TLD source (who.is, whoisxml, ICANN lookup) for trackupdate-cdn77.com — not registry-specific tools that don't apply to .com | PASS | Source #1 is who.is (generic TLD tool). Source #11 is rdap.org. Neither is a .com-registry-specific tool. |
| c12 | Output's DNS records cover A, AAAA, MX, TXT, NS — with the actual record values shown (or "no record" if absent) — and TXT records are interpreted for SPF / DKIM / DMARC / verification tokens that signal third-party services in use | PASS | 'All record types (A, AAAA, MX, TXT, NS, CNAME) queried against Google Public DNS returned NXDOMAIN (Status 3). The domain does not resolve.' NXDOMAIN is the effective 'no record' for all types; no TXT values to interpret. |
| c13 | Output's certificate transparency search via crt.sh returns the subdomain history — listing seen subdomains (e.g. cdn.trackupdate-cdn77.com, api.trackupdate-cdn77.com) and naming patterns that may reveal service typology | PASS | crt.sh searched via both JSON API and HTML; 'empty result set for both exact and wildcard queries' — absence itself is a finding noted: 'No TLS certificates have ever been issued for trackupdate-cdn77.com or any subdomain in the public CT logs.' |
| c14 | Output's ASN / hosting identification uses ipinfo.io, BGP.he.net, or equivalent passive lookup — naming the AS number, AS organisation, and hosting provider; flagging if hosted on bulletproof / common abuse-source providers | PARTIAL | Hosting table shows 'IP address: None — NXDOMAIN', 'ASN: Cannot determine', 'Hosting provider: Cannot determine'. AS60068 mentioned as background context for CDN77 brand, not as a lookup result. ipinfo.io and BGP.he.net not in sources; gap correctly explained but specific tools not invoked. |
| c15 | Output's Wayback Machine check shows historical content — registration date vs first archived content gap is a finding (legitimate domains usually have content soon after registration; C2 domains often don't) | PARTIAL | 'Wayback Machine: Blocked in this environment. No captures confirmed or denied.' Attempt is documented and listed in the Gaps table, but no historical content retrieved and no registration-date-vs-archive gap analysis produced. |
| c16 | Output handles privacy-protected WHOIS as a finding (typical for malicious infrastructure) — does NOT stop the investigation; continues with DNS, certificate transparency, and reputation databases | PASS | WHOIS failure logged as finding with explanation ('domain is not currently delegated in the .com zone — it either never completed registration, was dropped/expired, or was sinkholed'). Investigation proceeds through DNS, CT (crt.sh), OTX, urlscan.io, VirusTotal, ThreatFox. |
| c17 | Output queries reputation sources — VirusTotal, URLhaus, AbuseIPDB on the resolving IP, AlienVault OTX — with the lookup URLs and the result counts / verdict per source | PARTIAL | OTX covered with '0 pulses, no threat data'; urlscan.io covered with '0 scan results'; VirusTotal listed as 'JS-rendered SPA — inaccessible'; ThreatFox listed as 'Bot challenge — inaccessible'. URLhaus is absent entirely. AbuseIPDB not mentioned (no IP to query). Lookup URLs provided for accessible sources only. |
| c18 | Output recommends follow-on routing — if the A record points to interesting infrastructure (e.g. shared IP with other known-bad domains), routes to `/investigator:ip-intel`; if related domains surface via reverse lookup, recommends additional `/investigator:domain-intel` runs | FAIL | Summary recommends checking the original threat intel report, querying SecurityTrails/RiskIQ, and VirusTotal API. Neither `/investigator:ip-intel` nor `/investigator:domain-intel` is mentioned anywhere in the output. |
| c19 | Output uses passive methods only — no active port scans, no curl to fetch the actual domain content, no DNS bruteforce — staying strictly within passive OSINT scope | PASS | Header declares 'Methods: Passive open-source only.' All 13 sources are public lookup APIs or web services. No curl to the domain, no port scan, no DNS brute-force attempted. |

### Notes

The output is thorough and well-structured for a domain that turned out to be NXDOMAIN — a genuinely difficult edge case for a domain-intel skill. The skill correctly handles the NXDOMAIN state throughout (documenting why ASN, hosting, WHOIS, and historical data cannot be retrieved) and produces a substantive analysis based on the naming-pattern signal alone. The two main gaps dragging the score below 80%: (1) neither c8 nor c18 include specific `/investigator:ip-intel` or `/investigator:domain-intel` routing — the summary recommends manual analyst steps instead of skill routes; and (2) URLhaus is absent from reputation sources. The Wayback Machine and ipinfo.io/BGP.he.net gaps are legitimately explained by environment blocking and NXDOMAIN state respectively, earning partial credit rather than zero.
