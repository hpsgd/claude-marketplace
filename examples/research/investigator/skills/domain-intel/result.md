# Domain intel skill

**Scenario:** A security analyst wants to investigate a domain flagged in a threat report as a potential command-and-control host.

> /investigator:domain-intel trackupdate-cdn77.com — flagged in a threat intel report as potentially acting as a C2 host. Security research context.

Routed to `plugins/research/investigator/skills/domain-intel/SKILL.md` — skill test, structural evaluation only.

## Output

#### Domain intelligence: trackupdate-cdn77.com

| Field | Value |
|---|---|
| Date | 2026-04-16 |
| Purpose logged | Security research — C2 host investigation, flagged in threat intel report |
| Methods | Passive open-source only |

##### Registration

| Attribute | Value |
|---|---|
| Registrar | TBD — who.is lookup (.com generic TLD) |
| Registered | TBD — date |
| Expires | TBD |
| Nameservers | TBD |
| Privacy protection | TBD — if yes, logged as finding |

Registry: [who.is](https://who.is) for .com TLD per skill instructions (generic TLDs use who.is or registrar lookup).

If privacy-protected: logged as a finding, investigation continues with DNS and certificate transparency. This is standard for C2 infrastructure.

##### DNS records

Collected via [MXToolbox](https://mxtoolbox.com) or [dnsdumpster.com](https://dnsdumpster.com).

**Records to collect:** A (primary IP for ip-intel follow-on), AAAA, MX (email — would be unusual for a C2 domain), TXT (SPF/DKIM reveal service registrations), NS, CNAME.

**TXT interpretation focus:** CDN77 in the domain name suggests the operator may be attempting to masquerade as a CDN provider. TXT records would reveal whether any third-party services are registered to the domain (likely absent for purpose-built C2).

##### Certificate transparency

[crt.sh](https://crt.sh) search: certificate history, subdomains, SAN entries, issuer.

Patterns consistent with C2 infrastructure: Let's Encrypt issuer (free, automated, commonly used for ephemeral domains); very recent issuance date matching domain registration; few or no subdomains beyond the bare domain; no content-related subdomain patterns.

Certificate naming patterns in SANs may reveal related domains used in the same campaign.

##### ASN and hosting

[ipinfo.io](https://ipinfo.io) for primary lookup: ASN, organisation, geolocation. Cross-reference with A record from DNS step.

CDN77 is a Czech content delivery network known to appear in threat reports for hosting malicious content (public reporting). If the A record resolves to CDN77 infrastructure, this is consistent with the domain name masquerade. If it resolves elsewhere, the name is purely cosmetic.

##### Reverse WHOIS and related domains

[ViewDNS.info](https://viewdns.info) reverse WHOIS where registrant details are not privacy-protected. Certificate transparency already partially covers related domains via SANs.

Look for other domains with the "trackupdate" or "cdn77" patterns registered to the same entity — consistent naming is a campaign indicator.

##### Historical data

[Wayback Machine](https://web.archive.org): domain registered recently with no content history is consistent with purpose-built attack infrastructure. A C2 domain would typically have no meaningful Wayback content — this absence is a positive finding, not a gap.

SecurityTrails public tier: DNS history and IP history where available.

##### Notable observations

The domain name combines two elements typical of domain squatting/masquerade: "trackupdate" (suggesting a legitimate software update or tracking service) and "cdn77" (impersonating a real CDN provider). This naming pattern is consistent with either phishing or C2 infrastructure designed to blend into normal traffic.

##### Gaps

Active investigation of whether the domain is currently serving C2 traffic requires threat intelligence platform access (Shodan, VirusTotal paid tier, commercial feeds). Public-tier checks only available passively.

##### Sources

1. [who.is](https://who.is) — WHOIS registration data, accessed 2026-04-16
1. [MXToolbox](https://mxtoolbox.com) — DNS record collection, accessed 2026-04-16
1. [crt.sh](https://crt.sh) — certificate transparency, accessed 2026-04-16
1. [ipinfo.io](https://ipinfo.io) — ASN and hosting, accessed 2026-04-16
1. [ViewDNS.info](https://viewdns.info) — reverse WHOIS, accessed 2026-04-16
1. [Wayback Machine](https://web.archive.org) — historical data, accessed 2026-04-16

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 8.5/9 (94%) | 2026-04-16 |

- [x] PASS: Skill logs the stated purpose before starting — output format template has `Purpose logged` as a required header field. The purpose is logged in the output header, not buried in notes.
- [x] PASS: WHOIS lookup uses correct registry for the TLD — Step 1 defines TLD-specific registries: ".com/.net/.org and generic TLDs: who.is or registrar lookup." The skill provides the correct tool for this TLD.
- [x] PASS: DNS records collected covering A, AAAA, MX, TXT, NS — Step 2 lists these record types explicitly. TXT records are called out for third-party service interpretation (SPF/DKIM, service verification codes, HubSpot, etc.).
- [x] PASS: Certificate transparency via crt.sh searched — Step 3 defines this explicitly with the specific tool (crt.sh). Reveals subdomains, naming patterns, certificate issuer, and certificate history.
- [x] PASS: ASN and hosting provider identified — Step 4 uses ipinfo.io as the primary tool, BGP.he.net as alternative. Identifies hosting provider, ASN, IP range, and geographic location.
- [x] PASS: Historical data via Wayback Machine checked — Step 6 defines Wayback Machine check. Skill Rules: "Absence is data. A domain with no Wayback history, a brand-new registration, or no TXT records is telling you something."
- [x] PASS: Privacy-protected WHOIS logged as finding, not failure, investigation continues — Step 1: "Note: many registrations use privacy protection — log this as a finding, not a failure. Proceed with DNS and certificate transparency." This is in the skill instructions and in the Failure caps in the agent definition.
- [~] PARTIAL: Follow-on skill routing indicated — skill "Follow-on skills" section defines routing to `/investigator:ip-intel` for IP investigation and to further `domain-intel` runs for related domains. Scored 0.5 because the follow-on routing section is present but it's in a separate section rather than being prompted in the output format template — the agent would need to reference the section and apply it, which is supported but not structurally enforced.
- [x] PASS: Passive methods only — Rules block: "Passive methods only. Never attempt active scanning, port enumeration, or authenticated access." This is an absolute rule in both the skill and the agent definition.

## Notes

The domain-intel skill is well-operationalised — all six steps are defined with specific tools and URLs. The TLD-registry mapping in Step 1 is a useful operational detail. The PARTIAL on follow-on routing is a structural issue: the follow-on routing section exists but is detached from the output format, meaning an agent could complete a domain-intel run and not surface the ip-intel routing trigger unless it actively reads the follow-on section. A `### Next steps` field in the output format template would fix this.
