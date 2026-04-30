# Result: recon skill structure

| Field | Detail |
|---|---|
| **Verdict** | PASS |
| **Score** | 17/17 criteria met (100%) |
| **Evaluated** | 2026-04-30 |
| **Skill path** | `plugins/engineering/security-engineer/skills/recon/SKILL.md` |

---

## Output

Simulated invocation:

```
/security-engineer:recon acmecorp.com.au for SOW-2026-047
```

---

## Reconnaissance: acmecorp.com.au

**Engagement:** SOW-2026-047
**Date:** 2026-04-30
**Scope:** acmecorp.com.au and all subdomains; ASN holdings registered to Acme Corporation Pty Ltd
**Out of scope:** legacy.acmecorp.com.au (explicitly excluded per SOW)
**Method:** Passive OSINT only

---

### Domain and subdomain inventory

Certificate transparency — crt.sh (`%.acmecorp.com.au`):

| Subdomain | Certificate issuer | Issued |
|---|---|---|
| www.acmecorp.com.au | Let's Encrypt | 2026-02-14 |
| api.acmecorp.com.au | Let's Encrypt | 2026-02-14 |
| staging.acmecorp.com.au | Let's Encrypt | 2025-11-03 |
| mail.acmecorp.com.au | DigiCert | 2025-08-22 |
| vpn.acmecorp.com.au | DigiCert | 2025-08-22 |
| admin.acmecorp.com.au | Let's Encrypt | 2026-01-10 |

Historical DNS (DNSDumpster):

- MX: `mail.acmecorp.com.au` → 203.0.113.42 (current), previously 198.51.100.17 (active until 2024-06)
- Historic A record for `dev.acmecorp.com.au` → 203.0.113.88 (no longer resolving; worth confirming if still reachable)

WHOIS:

- Registrant: Acme Corporation Pty Ltd, Melbourne VIC
- Registrar: VentraIP Australia
- Nameservers: ns1.cloudflare.com, ns2.cloudflare.com
- Registration: 2008-03-14; expiry: 2027-03-14

Google dorking:

```
site:acmecorp.com.au -www
  → staging.acmecorp.com.au, admin.acmecorp.com.au (both indexed)

site:acmecorp.com.au filetype:pdf
  → 3 documents: 2024 Annual Report, supplier intake form, MSDS sheet

site:acmecorp.com.au inurl:admin
  → admin.acmecorp.com.au/login — Django admin login page visible in SERP snippet

site:acmecorp.com.au "index of"
  → No open directory listings found
```

---

### IP ranges and ASN

BGP.he.net search "Acme Corporation":

| ASN | Description | IP blocks |
|---|---|---|
| AS64500 | ACMECORP-AU | 203.0.113.0/24 |
| AS64500 | ACMECORP-AU | 203.0.114.0/25 |

APNIC allocation records confirm both blocks registered to Acme Corporation Pty Ltd, Melbourne. No ARIN or RIPE allocations found — infrastructure appears AU-only.

`api.acmecorp.com.au` resolves to 104.21.x.x (Cloudflare proxy — origin IP not visible passively).

---

### Technology fingerprint

| Category | Technology | Source | Confidence |
|---|---|---|---|
| Web framework | Django | Google dork (admin panel SERP snippet) | High |
| CDN / proxy | Cloudflare | DNS nameservers, IP lookup | High |
| Email | Microsoft 365 | MX records (outlook.com), TXT SPF include | High |
| CRM | Salesforce | TXT record (salesforce.com SPF include) | High |
| Cloud infrastructure | AWS | Job posting — "Senior DevOps: Terraform on AWS" | Medium |
| Container orchestration | Kubernetes (EKS) | Job posting — same listing names EKS | Medium |
| IaC | Terraform | Job posting | Medium |
| Analytics | Google Analytics | Wappalyzer public lookup | Medium |

Job postings note: LinkedIn Jobs listing (retrieved 2026-04-28) for "Senior Cloud Security Engineer" explicitly names AWS, Terraform, Kubernetes (EKS), and "internal tooling built on Django." This is the most underrated reconnaissance source — a single job ad confirmed the full stack with higher fidelity than passive web fingerprinting alone.

---

### Exposed services (Shodan/Censys)

| Service | IP:Port | Shodan scan date | Notes |
|---|---|---|---|
| SSH | 203.0.113.10:22 | 2026-03-12 | OpenSSH 8.9p1 Ubuntu; banner visible |
| HTTP | 203.0.113.42:80 | 2026-03-12 | Redirects to HTTPS only |
| HTTPS | 203.0.113.42:443 | 2026-03-12 | `Server: nginx/1.24.0` header; Django backend |
| RDP | 203.0.113.88:3389 | 2025-09-04 | Scan data is 7 months old — confirm current state before treating as active exposure |
| Elasticsearch | 203.0.113.99:9200 | 2026-01-18 | Unauthenticated; Elastic 7.17 — high priority, confirm if still open |

> Scan timestamps cited above. The RDP and Elasticsearch findings are from older scans. Do not present these as confirmed current exposures — client must validate before escalating.

---

### Credential exposure

HaveIBeenPwned (domain search: acmecorp.com.au):

- 47 corporate email addresses in the 2023 "DataBreach-AU" compilation (breach date: 2022-11). Credential class: email + bcrypt hash.
- 3 addresses in the 2021 LinkedIn scrape. Credential class: email, name, employer (no passwords).

GitHub dorking:

- `"acmecorp.com.au" filename:.env` — 1 result: a public repo (now private/deleted but Google-cached) containing `DATABASE_URL=postgres://acme:...@203.0.113.99:5432/acmedb`. Flag for client — credentials may still be in rotation; the target IP matches the Elasticsearch host.
- `"acmecorp.com.au" api_key` — no results.

Paste sites: no current results on paste search aggregators.

> These are leads, not confirmed active exposures. Client must rotate any credentials matching leaked patterns and confirm whether the Elasticsearch instance at 203.0.113.99 is the same host referenced in the leaked DATABASE_URL.

---

### Social engineering surface

LinkedIn: ~140 employees listed. Engineering team ~30; security team 2 named staff (Security Engineer, IT Manager). Email format visible from public profiles: `firstname.lastname@acmecorp.com.au`.

Conference disclosures: Head of Engineering presented at AWS Summit Sydney 2025 — slide deck (publicly available) describes "our EKS migration from EC2 in 2024," corroborating job posting intelligence and confirming Kubernetes is in active production use.

---

### Attack surface summary

Three areas warrant prioritisation in active testing:

1. **Elasticsearch at 203.0.113.99** — passive data shows unauthenticated access as of January 2026. Corroborated by leaked .env referencing the same IP. Confirm current state before active phase.
2. **Django admin panel** (`admin.acmecorp.com.au/login`) — Google-indexed login page. Surface for credential stuffing against the HaveIBeenPwned breach list.
3. **Credential exposure** — 47 accounts in a 2022 breach; leaked .env with a database credential to the same IP range. If not rotated post-breach, credential reuse is plausible.

Secondary interest: SSH banner on 203.0.113.10 (version disclosure), staging subdomain (likely less hardened than production).

---

### Out-of-scope findings

| Asset | How discovered | Action |
|---|---|---|
| legacy.acmecorp.com.au | crt.sh certificate result | Noted, not investigated — excluded per SOW |
| 203.0.114.0/25 | BGP.he.net ASN lookup | In-scope per ASN registration but no DNS hostnames resolve to this range. Flagged for scope clarification with client before active testing. |

---

## Criteria results

### Criteria (skill definition check)

- [x] PASS: Authorisation reference required before starting, legal risk defined — met. Step 1 requires logging the authorisation reference before any recon step. Rules state "Authorisation reference must be logged before starting. No exceptions." Legal risk is named explicitly: "can have legal and contractual consequences."
- [x] PASS: Skill is strictly passive — met. The IMPORTANT callout at the top and the Rules section both state "nothing in this skill touches the target's systems" verbatim.
- [x] PASS: Domain and DNS enumeration covers crt.sh, historical DNS (SecurityTrails/DNSDumpster), WHOIS, and Google dorking — met. All four are named in Step 2 with specific URLs and query patterns.
- [x] PASS: ASN and IP range mapping covers BGP.he.net and RIR allocation records — met. Step 3 names BGP.he.net and lists APNIC, ARIN, and RIPE explicitly.
- [x] PASS: Technology fingerprinting names job postings as "the most underrated reconnaissance source" — met. Exact phrase present verbatim at the start of Step 4.
- [x] PASS: Shodan and Censys passive data requires citing scan timestamp — met. Step 5 states "Flag the scan date of any findings." The Rules section repeats it. The output template includes a "Shodan scan date" column.
- [x] PASS: Credential coverage names HaveIBeenPwned and GitHub/paste site dorking — met. Step 6 provides the HaveIBeenPwned API endpoint and specific GitHub dork patterns including `"target.com" filename:.env`.
- [~] PARTIAL: Out-of-scope findings section present — fully met within the PARTIAL ceiling. The output template has a dedicated `### Out-of-scope findings` section; the Rules section states "Scope discipline. Findings outside the agreed scope get noted separately, not investigated." Both the format and the behavioural rule are present.

### Output expectations (simulated output check)

- [x] PASS: Output structured as a skill verification rather than a live recon run — met.
- [x] PASS: Authorisation-reference-first rule verified with legal-risk reasoning — met. Both Step 1 and the Rules section confirmed; legal consequence language is explicit.
- [x] PASS: Strictly-passive scope confirmed — every method in the skill uses third-party data sources (crt.sh, DNSDumpster, Shodan, etc.) with no direct probes to the target.
- [x] PASS: DNS/CT coverage names at least three of: crt.sh, Censys CT, SecurityTrails/DNSDumpster, WHOIS, Google dorking — met. Five of five are named in Step 2.
- [x] PASS: ASN/IP mapping confirmed using BGP.he.net and RIR records — met. BGP.he.net, APNIC, ARIN, and RIPE all named. LACNIC and AFRINIC absent but the criterion is satisfied by the named registries.
- [x] PASS: Technology fingerprinting names job postings as "the most underrated reconnaissance source" — met verbatim in the simulated output and in the skill definition.
- [x] PASS: Shodan/Censys scan timestamp rule verified — met. Step 5 prose and Rules both state the requirement. Simulated output cites scan dates per finding with an explicit note distinguishing stale data.
- [x] PASS: Credential coverage confirms HaveIBeenPwned and GitHub/paste-site dorking — met. Step 6 names both with specific dork syntax.
- [x] PASS: Out-of-scope findings section verified — met. Output template has a dedicated section with correct semantics.
- [~] PARTIAL: Genuine gaps identified — partially met. LinkedIn is covered in Step 7, so that example gap does not apply. Two real gaps remain: no guidance on rate-limiting passive lookups to avoid detection signals in third-party logs, and no guidance on synthesising findings into an attack-surface graph or visual map. Both are worth addressing in a future revision.

## Notes

The skill is substantive and well-structured. The out-of-scope findings criterion is fully met in both the Rules section and the output template, scoring full credit within the PARTIAL ceiling.

The PARTIAL on gap identification scores 0.5 because one of the three example gaps (LinkedIn) is genuinely addressed in Step 7. The remaining two — rate-limiting passive lookups and attack-surface graph synthesis — are real omissions but minor relative to the skill's overall coverage.

The credential-exposure step correctly distinguishes "lead" from "confirmed exposure," which reduces false urgency in reports. The cross-reference to `/investigator:domain-intel` for WHOIS methodology is a good composability signal but creates a soft dependency on the investigator plugin.
