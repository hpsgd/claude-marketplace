# Test: recon skill structure

Scenario: Checking that the recon skill enforces authorisation logging, uses passive-only methods, covers the full attack surface (DNS, ASN, technology, exposed services, credential leaks), and produces a structured output with an attack surface summary.

## Prompt

Review the recon skill definition and verify it enables thorough passive attack surface mapping while enforcing scope discipline and authorisation requirements.

## Criteria

- [ ] PASS: Skill requires authorisation reference to be logged before starting — no exceptions — and defines the legal risk of scope drift
- [ ] PASS: Skill is strictly passive — explicitly states nothing in this skill touches the target's systems
- [ ] PASS: Skill covers domain and DNS enumeration using certificate transparency (crt.sh), historical DNS data, WHOIS, and Google dorking
- [ ] PASS: Skill covers ASN and IP range mapping using BGP.he.net and RIR allocation records to find the full IP surface area
- [ ] PASS: Skill covers technology fingerprinting including job postings — identifies this as "the most underrated reconnaissance source"
- [ ] PASS: Skill covers Shodan and Censys passive data with a requirement to cite the scan timestamp of findings to avoid presenting stale data as current
- [ ] PASS: Skill covers leaked credential and breach data via HaveIBeenPwned and GitHub/paste site dorking
- [ ] PARTIAL: Skill output format includes an out-of-scope findings section for assets discovered outside the agreed scope that are noted but not investigated

## Output expectations

- [ ] PASS: Output is structured as a verification of the skill (verdict per requirement) rather than running an actual recon
- [ ] PASS: Output verifies the authorisation-reference-first rule — that no recon action is taken before a logged authorisation, with the legal-risk reasoning explicit
- [ ] PASS: Output confirms the strictly-passive scope — every method described touches third-party data sources only, never the target's systems (no port scans, no probes)
- [ ] PASS: Output verifies DNS / certificate-transparency coverage names crt.sh, Censys CT search, historical DNS (SecurityTrails / DNSDumpster), WHOIS, and Google dorking — at least three of these
- [ ] PASS: Output confirms ASN / IP range mapping uses BGP.he.net and RIR allocation records (ARIN / RIPE / APNIC / LACNIC / AFRINIC) to find the full IP surface
- [ ] PASS: Output confirms the technology fingerprinting section names job postings as a recon source and frames it as "the most underrated reconnaissance source" — not just BuiltWith / Wappalyzer
- [ ] PASS: Output verifies Shodan and Censys passive data usage requires citing the scan timestamp, with the rule that stale data must not be presented as current
- [ ] PASS: Output confirms credential / breach data coverage names HaveIBeenPwned and GitHub / paste-site dorking explicitly
- [ ] PASS: Output verifies the output format includes an out-of-scope findings section for assets discovered outside the agreed scope (noted but not investigated)
- [ ] PARTIAL: Output identifies any genuine gaps — e.g. no rule on rate-limiting passive lookups to avoid suspicion, no guidance on combining findings into an attack-surface graph, or no mention of social media / LinkedIn enumeration as a recon source
