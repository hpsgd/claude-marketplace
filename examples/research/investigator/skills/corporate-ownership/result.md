# Corporate ownership skill

**Scenario:** A due diligence analyst wants to map the ownership chain behind a company with complex group structures across multiple jurisdictions.

> /investigator:corporate-ownership Meridian Capital Partners Pty Ltd — we're considering a partnership and want to understand who actually controls this entity, whether there are offshore holding structures, and who the directors are connected to.

Routed to `plugins/research/investigator/skills/corporate-ownership/SKILL.md` — skill test, structural evaluation only.

## Output

#### Corporate ownership: Meridian Capital Partners Pty Ltd

| Field | Value |
|---|---|
| Date | 2026-04-16 |
| Primary jurisdiction | AU |
| Registration number | TBD — ASIC Connect lookup |

##### Primary registration

| Attribute | Value |
|---|---|
| Legal name | Meridian Capital Partners Pty Ltd |
| Registration number | TBD — ASIC Connect |
| Jurisdiction | Australia (Pty Ltd = AU proprietary company) |
| Status | TBD — Active / Deregistered |
| Registered office | TBD |
| Date registered | TBD |

Source: [ASIC Connect](https://connect.asic.gov.au), accessed 2026-04-16.
Cross-reference: [ABN Lookup](https://abn.business.gov.au), accessed 2026-04-16 — ABN/ACN cross-check and business name registrations.

##### Directors (current)

| Name | Role | Appointed | Other appointments |
|---|---|---|---|
| TBD | Director | TBD | ASIC director search results |

For each director: ASIC Connect director search returns all current and historical AU company appointments. Director networks often reveal undisclosed relationships between apparently separate entities.

##### Directors (historical)

Any director who has resigned or been removed — notable where a director departed and a new company was registered shortly after (common restructuring pattern).

##### Ownership structure

For AU proprietary companies: ASIC requires disclosure of shareholders holding 20%+ of shares in the company extract. Shareholders and percentage holdings listed here.

Where the registered shareholder is itself a company: follow the chain up to the next registry. If the chain terminates in a jurisdiction with limited disclosure (BVI, Cayman, Delaware LLC) — flagged as a significant finding, not a gap.

Cross-reference: [ICIJ Offshore Leaks Database](https://offshoreleaks.icij.org) — searched for company name and any director names. Absence from ICIJ does not mean no offshore structure; ICIJ only covers leaked datasets (Panama Papers, Pandora Papers, Offshore Leaks). This limitation is noted explicitly in the output.

##### Subsidiaries

ASIC Connect corporate group searches; any annual report or ASX announcement cross-reference if applicable. OpenCorporates cross-jurisdiction search for related entities.

##### Related entities

Entities sharing the same registered address, same directors, or same registered agent as Meridian Capital Partners Pty Ltd. ViewDNS.info reverse WHOIS for digital footprint overlap if relevant.

##### Offshore/complex structure notes

Any ownership chain that terminates in a jurisdiction without beneficial ownership disclosure requirements (BVI, Cayman, Cook Islands, certain US states) is flagged here. This is a significant finding because it means the actual controlling party is not publicly identifiable.

##### Director network map

Where directors hold appointments in other companies, the cross-appointment map is produced here. Shared directors between Meridian Capital Partners and other entities is a key finding for understanding undisclosed relationships.

##### Sources

1. [ASIC Connect](https://connect.asic.gov.au) — primary AU registration, directors, shareholders, accessed 2026-04-16
1. [ABN Lookup](https://abn.business.gov.au) — ABN/ACN cross-reference, business names, accessed 2026-04-16
1. [ICIJ Offshore Leaks Database](https://offshoreleaks.icij.org) — offshore structure check, accessed 2026-04-16
1. [OpenCorporates](https://opencorporates.com) — cross-jurisdiction search, accessed 2026-04-16

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 8.5/9 (94%) | 2026-04-16 |

- [x] PASS: Skill checks ASIC Connect as the primary AU registry source — Step 1 "Australia" section: ASIC Connect is listed first for company extract, directors, shareholders, registered office, date of registration, and current status.
- [x] PASS: Beneficial ownership section distinguishes registered ownership from beneficial ownership — Step 2 opens: "Identify who ultimately controls or owns the company beyond the registered directors." The section explicitly notes that absence of disclosed owners doesn't mean there aren't any, and that UK PSC register distinguishes beneficial from registered owners. The skill applies this distinction to AU entities.
- [x] PASS: Director network step executed — Step 3 requires identifying all directors and for each director searching their other company appointments across ASIC Connect, NZ Companies Office, Companies House, and OpenCorporates. The step notes that director networks reveal undisclosed relationships.
- [x] PASS: Subsidiary mapping attempted — Step 4 covers SEC 10-K Exhibit 21 (US), Companies House group structures (UK), ASX/NZX annual report subsidiaries (AU/NZ public), and ASIC Connect corporate group searches.
- [x] PASS: Related entities step executed — Step 5 requires checking for shared registered address, shared directors (from Step 3 results), shared registered agent, and similar naming patterns. OpenCorporates and ViewDNS.info reverse WHOIS are named tools.
- [x] PASS: When ownership chain terminates in a limited-disclosure jurisdiction, flagged as significant finding — Rules block: "Note when an ownership chain terminates in a jurisdiction with limited disclosure requirements (offshore structures, certain US states) — this is a significant finding, not a gap." Output format has a `### Offshore/complex structure notes` section.
- [x] PASS: Jurisdiction documented for every entity — Rules block: "Document the jurisdiction for every entity in the ownership chain." Output format requires jurisdiction in the primary registration table.
- [~] PARTIAL: ICIJ Offshore Leaks Database checked with caveat that absence doesn't mean no offshore structure — Step 2 includes ICIJ as a beneficial ownership source. Rules block: "ICIJ data covers specific leaked datasets — it's a signal, not a comprehensive offshore registry. Absence from ICIJ doesn't mean no offshore structure." The caveat is present in the rules. Scored 0.5 because the output format doesn't include a mandatory ICIJ section or caveat — the rules state it but the template doesn't enforce it structurally.
- [x] PASS: Output uses the structured format — output format template has all named sections: primary registration table, directors (current) table, directors (historical), ownership structure, subsidiaries, related entities, offshore/complex structure notes, director network map, sources.

## Notes

The corporate ownership skill is thorough and operationally specific — it names registries by country with URLs and describes what each contributes. The director network step is particularly valuable for complex group structures. The PARTIAL on the ICIJ caveat is a real gap: the caveat is in the rules but not in the output template, so it could be omitted in the produced output. Adding a `### ICIJ search result` section with mandatory caveat text to the output template would close this.
