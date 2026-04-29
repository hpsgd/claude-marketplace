# Test: due-diligence skill

Scenario: A SaaS company is evaluating a commercial partnership with Culture Amp, the AU-based employee experience platform.

## Prompt

/analyst:due-diligence Culture Amp Pty Ltd for commercial partnership — we're considering integrating their employee engagement surveys into our HR platform

## Criteria

- [ ] PASS: Skill states the scope explicitly at the top — commercial partnership scope, public data only
- [ ] PASS: Business fundamentals section includes a source and date for every revenue or funding figure — no unsourced numbers
- [ ] PASS: Product signals section covers review score trend over time, not just the current score
- [ ] PASS: Team section notes current key executive tenures and any notable recent departures
- [ ] PASS: Signal summary table is present and precedes the verdict — verdict follows from the signals, not the other way around
- [ ] PASS: Output clearly states this is public-data diligence only and that legal, financial, and technical diligence requires direct access
- [ ] PARTIAL: When two or more red signals are present, skill routes to appropriate follow-on skills (public-records, corporate-ownership, entity-footprint) rather than stopping at the verdict
- [ ] PASS: Revenue and valuation are not conflated — if estimates for private company appear, they are explicitly labelled as estimates

## Output expectations

- [ ] PASS: Output addresses Culture Amp specifically — AU-headquartered employee experience platform founded 2009 by Didier Elzinga, Jon Williams, Doug English, Rod Hamilton — with key entity confirmation (ABN, registered office) at the top
- [ ] PASS: Output's scope statement explicitly limits to commercial-partnership diligence using public data only — naming what's NOT covered (legal contract review, financial audit, technical security assessment) and routing those to appropriate diligence types
- [ ] PASS: Output's business fundamentals section sources every revenue / funding figure — e.g. "Series F $100M raised 2021 (Crunchbase, source URL); ARR ~$80M FY22 (AFR profile, March 2022)" — never unsourced
- [ ] PASS: Output's product signals trace review-score TREND over time — not just current G2 / Capterra average; comparing FY22 vs FY24 reveals trajectory (improving / stable / declining)
- [ ] PASS: Output's team section names current key executives (CEO, CRO, CTO, CFO) with tenure, plus any notable departures in last 12 months — leadership churn is a partnership-risk signal
- [ ] PASS: Output's signal summary table precedes the verdict — revenue trajectory (green / amber / red), customer base (green), product reviews (green / amber / red), funding runway (green if recent raise / amber if old), leadership stability (green if stable / amber if recent change), legal disputes (green if none public / red if material)
- [ ] PASS: Output's verdict (PROCEED / PROCEED WITH CONDITIONS / DECLINE / NEEDS DEEPER DILIGENCE) follows from the signal table — not asserted independently then justified retroactively
- [ ] PASS: Output explicitly states this is public-data-only diligence — and that the partnership decision requires legal review of the partnership terms, financial diligence (ideally audited financials shared under NDA), and technical / security review
- [ ] PASS: Output distinguishes revenue (ARR, recurring revenue actually flowing in) from valuation (last round implied valuation, secondary market estimate) — never collapsing these
- [ ] PARTIAL: Output addresses cross-AU SaaS partnership specifics — both companies are AU-based so currency / tax / data-residency concerns are simpler than cross-border, but customer-data-sharing under SOCI Act and Privacy Act 1988 still applies
