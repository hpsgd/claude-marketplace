# Output: ip-intel skill

**Verdict:** PARTIAL
**Score:** 17.5/20 criteria met (87.5%)
**Evaluated:** 2026-04-29

## Results

### Criteria section

- [x] PASS: Skill logs the stated purpose (security investigation) before starting — output format template includes `**Purpose logged:** [stated purpose]` as the first metadata field before any lookup data
- [x] PASS: Primary ownership lookup uses ipinfo.io for ASN, organisation, and geolocation — Step 1 explicitly names ipinfo.io as the primary source
- [x] PASS: The appropriate regional internet registry is queried — RIPE NCC for European IP — Step 1 includes the full RIR table mapping Europe/Middle East/Central Asia to RIPE NCC
- [x] PASS: Reverse DNS PTR record is looked up and interpreted — Step 2 directs MXToolbox reverse lookup and lists naming conventions to interpret (operator scheme, hosting provider patterns, geographic naming)
- [x] PASS: Reputation checked across VirusTotal, AbuseIPDB, and Shodan — Step 3 names all three explicitly with links
- [x] PASS: Shodan data labelled as historical — Step 3 states "Shodan data may be stale. It's a historical record of what was observed, not necessarily current state."
- [x] PASS: Cloud/hosting provider attribution caveat noted — Rules section states "attribution to the provider doesn't identify the actual customer"
- [x] PASS: Clean reputation not equated with benign — Rules section states "A clean reputation score doesn't mean the IP is benign. It means it hasn't been reported. State this distinction clearly."
- [~] PARTIAL: Related infrastructure investigated — other domains and ASN patterns — partially met: Step 4 covers ViewDNS.info reverse IP and ASN pattern checking, but no passive DNS aggregators (SecurityTrails, RiskIQ/PassiveTotal) are named; the ASN pattern check lacks a specified tool
- [x] PASS: Passive methods only — Rules section and skill description both prohibit port scanning, banner grabbing, and service interaction

### Output expectations section

- [x] PASS: Output logs stated purpose at top before any lookup — output template has `**Purpose logged:** [stated purpose]` in the header block before ownership data
- [x] PASS: Output's primary lookup uses ipinfo.io for ASN, organisation, geolocation — Step 1 directs ipinfo.io as primary
- [x] PASS: Output queries RIPE NCC for European IP range — RIR table in Step 1 maps Europe to RIPE NCC with URL; definition drives agent to the correct registry
- [x] PASS: PTR lookup performed and result interpreted — Step 2 covers this with naming-scheme interpretation examples
- [x] PASS: Reputation checked across at least 3 sources with specific URLs — Step 3 names VirusTotal, AbuseIPDB, Shodan with links; output template includes `[Date of last scan]` field for Shodan
- [x] PASS: Shodan data labelled as HISTORICAL — Step 3 note addresses staleness explicitly; output template Shodan row includes `[Date of last scan]`
- [~] PARTIAL: Output addresses 185.220.101.47 as a known Tor exit node — partially met: the skill is generic and has no Tor-specific awareness; the PTR interpretation guidance lists hosting patterns but not anonymisation infrastructure (Tor exits, VPN providers); a well-formed execution might surface it via reputation data but the definition does not direct the agent to look for this pattern
- [x] PASS: Output explicitly states clean reputation does not mean benign — Rules section instructs "State this distinction clearly" and gives the exact framing ("hasn't been reported")
- [ ] FAIL: Output investigates related infrastructure via SecurityTrails and RiskIQ — not met: Step 4 uses only ViewDNS.info for reverse IP; SecurityTrails and RiskIQ/PassiveTotal are not mentioned anywhere in the skill definition
- [x] PASS: Passive methods only — no active scanning — Rules section explicitly prohibits port scans, banner grabbing, service interaction; Shodan passive-use note reinforces this

## Notes

The skill covers the core passive-OSINT workflow well. The primary gap is passive DNS depth: ViewDNS.info is a starting point but SecurityTrails and RiskIQ/PassiveTotal are the standard tools for passive DNS enumeration in security investigations and are absent from the definition.

The Tor exit node gap is a fairness observation rather than a structural flaw — the skill is generic by design. That said, "anonymisation infrastructure" (Tor exits, VPN providers) is common enough in firewall investigation scenarios that adding it to the PTR interpretation examples would be a meaningful improvement.

The purpose-logging requirement is met by template structure rather than an explicit "log purpose before proceeding" instruction. That's close enough given the template field position.
