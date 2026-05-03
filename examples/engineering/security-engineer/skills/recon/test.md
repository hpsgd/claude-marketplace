# Test: recon skill structure

Scenario: Checking that the recon skill enforces authorisation logging, uses passive-only methods, covers the full attack surface (DNS, ASN, technology, exposed services, credential leaks), and produces a structured output with an attack surface summary.

## Prompt

Review the recon skill definition and verify it enables thorough passive attack surface mapping while enforcing scope discipline and authorisation requirements.

Read the skill at `/Users/martin/Projects/turtlestack/plugins/engineering/security-engineer/skills/recon/SKILL.md` and verify each item by name. Quote skill text where present:

- **Authorisation reference logged before starting** — no exceptions. The skill defines the legal risk of scope drift (unauthorised recon = potential CFAA / Computer Misuse Act violation).
- **Strictly passive** — every method touches third-party data sources only, never the target's systems. No port scans, no probes.
- **Domain / DNS enumeration sources (5)**: crt.sh (certificate transparency), Censys CT search, historical DNS (SecurityTrails / DNSDumpster), WHOIS, Google dorking. At least three named.
- **ASN / IP range mapping**: BGP.he.net AND RIR allocation records (ARIN, RIPE, APNIC, LACNIC, AFRINIC) named.
- **Technology fingerprinting includes job postings** as a recon source — explicitly framed as "the most underrated reconnaissance source".
- **Shodan and Censys** for passive infrastructure data, with the rule that **scan timestamps must be cited** to avoid presenting stale data as current.
- **Credential / breach data**: HaveIBeenPwned AND GitHub / paste-site dorking.
- **Out-of-scope findings section** in the output template — assets discovered outside agreed scope are noted but not investigated.
- **Identified gaps**: any of — no rule on rate-limiting passive lookups to avoid suspicion, no guidance on combining findings into an attack-surface graph, no mention of social media / LinkedIn enumeration as a recon source.

Confirm or flag each by name.

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
