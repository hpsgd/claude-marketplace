# Output: recon skill structure

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17.5/18 criteria met (97%) |
| **Evaluated** | 2026-04-29 |
| **Source** | `plugins/engineering/security-engineer/skills/recon/SKILL.md` |

## Results

### Criteria

- [x] PASS: Skill requires authorisation reference to be logged before starting — no exceptions — and defines the legal risk of scope drift — met: Step 1 states "legal and contractual consequences" for scope drift; Rules state "Authorisation reference must be logged before starting. No exceptions."
- [x] PASS: Skill is strictly passive — explicitly states nothing in this skill touches the target's systems — met: IMPORTANT callout and Rules both use the explicit phrase "nothing in this skill touches the target's systems."
- [x] PASS: Skill covers domain and DNS enumeration using certificate transparency (crt.sh), historical DNS data, WHOIS, and Google dorking — met: Step 2 names crt.sh, SecurityTrails/DNSDumpster for historical DNS, WHOIS, and four specific Google dork patterns.
- [x] PASS: Skill covers ASN and IP range mapping using BGP.he.net and RIR allocation records to find the full IP surface area — met: Step 3 names BGP.he.net, APNIC, ARIN, and RIPE explicitly.
- [x] PASS: Skill covers technology fingerprinting including job postings — identifies this as "the most underrated reconnaissance source" — met: Step 4 opens with the exact phrase verbatim.
- [x] PASS: Skill covers Shodan and Censys passive data with a requirement to cite the scan timestamp of findings to avoid presenting stale data as current — met: Step 5 requires flagging the scan date; the Rules section reinforces it; the output template includes a "Shodan scan date" column.
- [x] PASS: Skill covers leaked credential and breach data via HaveIBeenPwned and GitHub/paste site dorking — met: Step 6 provides the HaveIBeenPwned API endpoint and specific GitHub dork patterns including `"target.com" filename:.env`.
- [x] PARTIAL: Skill output format includes an out-of-scope findings section for assets discovered outside the agreed scope that are noted but not investigated — fully met: output template has a dedicated `### Out-of-scope findings` section with the note "noted but not investigated"; Rules reinforce it. Scores as full credit within the PARTIAL ceiling.

### Output expectations

- [x] PASS: Output is structured as a verification of the skill (verdict per requirement) rather than running an actual recon — met.
- [x] PASS: Output verifies the authorisation-reference-first rule — that no recon action is taken before a logged authorisation, with the legal-risk reasoning explicit — met: Step 1 and Rules both cover this; legal/contractual risk language is explicit.
- [x] PASS: Output confirms the strictly-passive scope — every method described touches third-party data sources only, never the target's systems (no port scans, no probes) — met: two locations in the skill state this unambiguously.
- [x] PASS: Output verifies DNS / certificate-transparency coverage names crt.sh, Censys CT search, historical DNS (SecurityTrails / DNSDumpster), WHOIS, and Google dorking — at least three of these — met: five of five named in Step 2 (crt.sh, SecurityTrails, DNSDumpster, WHOIS, Google dorking).
- [x] PASS: Output confirms ASN / IP range mapping uses BGP.he.net and RIR allocation records (ARIN / RIPE / APNIC / LACNIC / AFRINIC) to find the full IP surface — met: BGP.he.net, ARIN, RIPE, APNIC named; LACNIC and AFRINIC absent but the major registries are covered and the criterion is satisfied.
- [x] PASS: Output confirms the technology fingerprinting section names job postings as a recon source and frames it as "the most underrated reconnaissance source" — not just BuiltWith / Wappalyzer — met verbatim.
- [x] PASS: Output verifies Shodan and Censys passive data usage requires citing the scan timestamp, with the rule that stale data must not be presented as current — met in Step 5 prose and the Rules section.
- [x] PASS: Output confirms credential / breach data coverage names HaveIBeenPwned and GitHub / paste-site dorking explicitly — met: Step 6 names both with specifics including dork syntax.
- [x] PASS: Output verifies the output format includes an out-of-scope findings section for assets discovered outside the agreed scope (noted but not investigated) — met: output template has a dedicated section.
- [~] PARTIAL: Output identifies any genuine gaps — e.g. no rule on rate-limiting passive lookups to avoid suspicion, no guidance on combining findings into an attack-surface graph, or no mention of social media / LinkedIn enumeration as a recon source — partially met: LinkedIn IS covered in Step 7 (social engineering surface), so that example gap does not apply. The skill has no rate-limiting guidance and no attack-surface graph synthesis guidance — two real gaps remain unaddressed.

## Notes

The skill is substantive and well-structured. The out-of-scope findings criterion is fully met in both the Rules and output template, so it scores full credit despite being typed PARTIAL in the rubric.

The PARTIAL on gap identification scores 0.5 because one of the three example gaps (LinkedIn) is genuinely addressed in Step 7. The other two — rate-limiting passive lookups to avoid detection and guidance on synthesising findings into an attack-surface graph — are real omissions worth noting for a future revision.

LACNIC and AFRINIC are absent from the ASN section, but the criterion is satisfied by the three named RIRs covering the main geographies.

The skill's credential-exposure step correctly distinguishes "lead" from "confirmed exposure," reducing false urgency in reports. The cross-reference to `/investigator:domain-intel` for WHOIS is a good composability pattern but creates a soft dependency on that plugin.
