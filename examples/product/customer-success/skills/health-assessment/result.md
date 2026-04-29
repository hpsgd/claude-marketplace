# Output: Health assessment

**Verdict:** FAIL
**Score:** 11.5/18 criteria met (64%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill scores all 5 dimensions: Adoption (30%), Engagement (25%), Relationship (20%), Value Realisation (15%), Commercial (10%) — Step 2 defines all five with exact weights and 0–100 scoring bands
- [x] PASS: Skill calculates a composite health score using the correct weighted formula — Step 3 shows the explicit formula; not a simple average
- [x] PASS: Skill classifies accounts into health categories with defined thresholds — Step 4 defines Healthy/Neutral/At Risk/Critical with numeric bands and required response timelines
- [x] PASS: Skill requires identifying data sources for each dimension before scoring — Step 1 is mandated as the first step in a "sequential — do not skip steps" process
- [x] PASS: Skill identifies specific risk signals per account — Step 5 defines seven named churn indicators with risk levels and an override rule that can bump a Healthy composite to At Risk
- [x] PASS: Skill produces recommended interventions for at-risk accounts — Step 6 defines four typed intervention categories; each requires Owner, Timeline, Success criteria, and Escalation; Anti-patterns explicitly bans "'schedule a call' is not an intervention plan"
- [~] PARTIAL: Skill produces a portfolio summary view — Step 7 is present ("aggregate across accounts for portfolio-level insights") but provides no output template, no field list, and no guidance on what to aggregate (0.5)
- [x] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields — all three present

### Output expectations

- [ ] FAIL: Output assesses all 15 accounts — the output format template is a single-account structure with one composite, one dimension table, one risk-signal table; no per-account row mechanism across 15 accounts exists in the skill
- [ ] FAIL: Output scores each account on all 5 dimensions with per-account rows — the output format has one dimension table for one subject; a multi-account grid is not defined
- [ ] FAIL: Output computes the composite score with verifiable per-dimension math per account — follows from above; no multi-account tabular output is specified
- [ ] FAIL: Output classifies each account as Green / Yellow / Red (or ternary equivalent) with stated thresholds — the skill uses a 4-tier system (Healthy/Neutral/At Risk/Critical), not a ternary; thresholds are defined but the output format does not map to the expected Green/Yellow/Red classification
- [x] PASS: Output names the data source per dimension before scoring — Step 1 is mandated before Step 2, and "Scoring without data" is listed as an explicit anti-pattern
- [ ] FAIL: Output identifies specific risk signals per at-risk account — Step 5 defines signal types, but the output template is single-account; no mechanism for per-account signals at portfolio scale is specified
- [~] PARTIAL: Output's recommended interventions per at-risk account are specific actions tied to the failing dimension — intervention types are dimension-specific and generic "schedule a check-in" is banned; partially met because the output format is single-account and does not produce a row-per-account intervention column for a portfolio (0.5)
- [ ] FAIL: Output's portfolio summary aggregates 15 accounts with ARR at risk — Step 7 is a single sentence; no ARR field, no Red/Yellow/Green count format, no at-risk ARR total
- [ ] FAIL: Output prioritises at-risk accounts for the review with renewal dates, ARR, and interventions — not addressed in the output format
- [ ] FAIL: Output flags trends across the portfolio — no pattern-analysis step or portfolio trend prompt exists in the skill

## Notes

The skill is well-built for single-account assessment. The data-source-first sequence, weighted formula, signal override rule, and typed intervention categories with mandatory owner/timeline/success-criteria/escalation fields are all strong design choices.

The failure is structural: the prompt asks for 15 enterprise accounts in a portfolio view for a quarterly CS team review. The skill's output format is a single-account template. Step 7 gestures at portfolio mode in one sentence but provides no output template, no aggregation fields, and no ARR-at-risk rollup. A team running this skill against 15 accounts would produce 15 separate single-account reports — not the consolidated prioritised view the prompt needs.

Six of the ten output expectations fail directly because of the absent multi-account output format. Fixing the skill requires adding a portfolio output template to Step 7 with per-account rows, an ARR-at-risk aggregate, and a Red-first prioritisation list.
