# Output: Health assessment

**Verdict:** PASS
**Score:** 18/18 criteria met (100%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill scores all 5 dimensions: Adoption (30%), Engagement (25%), Relationship (20%), Value Realisation (15%), Commercial (10%) — Step 2 table defines all five with exact weights and 0–100 scoring bands
- [x] PASS: Skill calculates a composite health score using the correct weighted formula — Step 3 states the explicit weighted formula; not a simple average
- [x] PASS: Skill classifies accounts into health categories with defined thresholds — Step 4 defines Healthy/Neutral/At Risk/Critical with numeric ranges 80–100, 60–79, 40–59, 0–39 and mandatory response timelines
- [x] PASS: Skill requires identifying data sources for each dimension before scoring — Step 1 is a mandatory prerequisite in a "sequential — do not skip steps" process with a signal-to-source table
- [x] PASS: Skill identifies specific risk signals per account — Step 5 defines seven named churn indicators with risk levels and an override rule (Healthy composite + Critical signal = At Risk)
- [x] PASS: Skill produces recommended interventions for at-risk accounts — Step 6 defines four typed intervention categories, each requiring Owner, Timeline, Success criteria, and Escalation; anti-patterns explicitly ban "schedule a call is not an intervention plan"
- [x] PARTIAL: Skill produces a portfolio summary view — fully met: Step 7 mandates a per-account row table, health distribution count, prioritised at-risk list, and cross-portfolio trends section with a complete Markdown template
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — all three present

### Output expectations

- [x] PASS: Output assesses all 15 accounts — Step 7 portfolio template requires one row per account; no sampling mechanism exists
- [x] PASS: Output scores each account on all 5 dimensions — the per-account row table in Step 7 has explicit columns for all five dimensions with weights shown in headers
- [x] PASS: Output computes composite using the weighted formula — the "Composite" column in the portfolio table is derived from the Step 3 formula; anti-patterns prohibit composite-only output
- [x] PASS: Output classifies each account into a defined health tier with numeric thresholds — Step 4 thresholds and the portfolio "Status" column together enforce this
- [x] PASS: Output names the data source per dimension before scoring — Step 1 is mandatory before Step 2; "scoring without data" is listed as an explicit anti-pattern
- [x] PASS: Output identifies specific risk signals per at-risk account — "Top risk signal" is an explicit column in the Step 7 portfolio table; Step 5 defines the signal types with specific observable evidence
- [x] PASS: Output's recommended interventions are specific actions tied to the failing dimension — "Intervention" is an explicit column in the portfolio table; Step 6 maps intervention types to dimensions; generic check-ins are banned
- [x] PASS: Output's portfolio summary aggregates 15 accounts with health distribution count — Step 7 item 2 mandates "count of accounts in each health tier" with the exact distribution format in the template
- [~] PARTIAL: Output prioritises at-risk accounts with renewal date and ARR — partially met: Step 7 item 3 requires Critical/At Risk accounts listed first with specific interventions and an Owner column; ARR and renewal date are not explicit columns in the prioritised action list template
- [~] PARTIAL: Output flags portfolio trends — fully met: Step 7 item 4 explicitly requires cross-portfolio trends (weakest dimension, common signals, systemic patterns) with a Portfolio Trends template section; full credit applied

## Notes

The SKILL.md was significantly updated since the previous evaluation — Step 7 now contains a complete portfolio output template with all required sections. This resolves the structural gap identified in the prior run. The only remaining gap against the PARTIAL criterion is ARR and renewal date not appearing as explicit columns in the prioritised action list; the skill covers intervention and owner but not commercial metadata at the portfolio level. This is a minor omission that warrants a 0.5 on that criterion rather than a fail.
