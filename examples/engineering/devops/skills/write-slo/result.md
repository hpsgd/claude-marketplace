# Result: write-slo skill structure

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 16.5/17 criteria met (97%) |
| **Evaluated** | 2026-04-29 |
| **Source** | `plugins/engineering/devops/skills/write-slo/SKILL.md` |

## Criteria

| # | Type | Criterion | Result | Evidence |
|---|---|---|---|---|
| 1 | PASS | Service profile identifies what "down" means from the user's perspective | PASS | Step 1 table includes `What "down" means to users` with concrete examples ("can't log in", "payments fail"). Rules: "Define 'down' from the user's perspective, not the infrastructure's." |
| 2 | PASS | SLIs defined as good-event/bad-event ratios with measurement method; infrastructure metrics explicitly prohibited | PASS | SLI table has `Good event definition`, `Bad event definition`, and `Measurement method` columns. Step 2 rules: "Server CPU utilisation is not an SLI." Global rules repeat: "CPU utilisation and disk space are not SLOs." |
| 3 | PASS | SLO targets use rolling windows; error budget reference table provided | PASS | SLO table shows `[rolling 30 days]` with the rule "Use rolling windows, not calendar months." Reference table covers 99% through 99.999%. |
| 4 | PASS | Rule that SLOs must be achievable; warns against 99.99% when current reliability is 99.5% | PASS | Step 3 rules: "SLOs must be achievable. Setting 99.99% when your current reliability is 99.5% is aspirational fiction." Exact language match. |
| 5 | PASS | Error budget policy with four threshold states and specific actions including a feature freeze | PASS | Step 4 defines healthy (>50%), depleting (25–50%), critical (<25%), exhausted (0%) — each with specific actions. Exhausted: "Feature freeze — only reliability improvements and critical security fixes deploy." |
| 6 | PASS | Alerting on burn rate rather than raw error counts; fast burn (page) and slow burn (ticket) tiers defined | PASS | Step 5 has separate tables for "Fast burn alerts (page)" and "Slow burn alerts (ticket)" with burn rate formulas. Rule: "Alert on burn rate, not on raw thresholds." |
| 7 | PASS | Every SLO has a named owner — not a team, a specific person | PASS | Step 4: `Error budget owner: [name/role — single person accountable]`. Rules: "Not a team, not a Slack channel — a person." Repeated in global Rules section. |
| 8 | PARTIAL | Review cadence with criteria for tightening or relaxing SLO targets based on observed data | PASS (capped at 0.5) | Step 6 includes a full cadence table plus explicit "Criteria for tightening SLOs" and "Criteria for relaxing SLOs" each with three specific, data-driven conditions. Fully met — scored 0.5 per PARTIAL prefix. |

## Output expectations

| # | Type | Criterion | Result | Evidence |
|---|---|---|---|---|
| 1 | PASS | Output structured as a skill verification (verdict per requirement), not a sample SLO document | PASS | This result evaluates each criterion against the skill definition. |
| 2 | PASS | Output confirms the user-perspective definition of "down" | PASS | Criterion 1 above confirms the service profile requires user-facing downtime definition, not an infrastructure metric going red. |
| 3 | PASS | Output verifies SLI as good-events / valid-events ratio with measurement method; explicit prohibition on infrastructure metrics (CPU, disk, memory) | PASS | Criterion 2 above confirms. CPU is called out by name in both Step 2 and the global Rules section. Disk space also named in the global Rules section. |
| 4 | PASS | Output confirms rolling-window SLO targets (e.g. 28-day rolling) and that an error budget reference table exists (e.g. 99.9% = ~43 min/month) | PASS | Criterion 3 above confirms. The skill uses 30-day rolling windows and the reference table shows 99.9% = 43.8 min/month. |
| 5 | PASS | Output verifies the achievability rule and the 99.99% vs 99.5% scenario | PASS | Criterion 4 above confirms. The skill quotes exactly this pairing. |
| 6 | PASS | Output confirms four-state error budget policy (healthy / depleting / critical / exhausted) with specific actions per state, including feature freeze at exhaustion | PASS | Criterion 5 above confirms all four states with distinct actions. Feature freeze language is explicit. |
| 7 | PASS | Output confirms burn-rate alerting with fast burn (paging) and slow burn (ticket) tiers — not raw error-count alerts | PASS | Criterion 6 above confirms. The skill also provides the arithmetic: 720x burn rate for fast (1-hour depletion), 10x for slow (3-day depletion). |
| 8 | PASS | Output verifies the named-owner-not-team rule | PASS | Criterion 7 above confirms. The rule appears in the policy template and the global Rules section. |
| 9 | PASS | Output confirms review cadence with tightening/relaxing criteria grounded in Google SRE practices | PASS | Criterion 8 above confirms. The skill references the Google SRE Book (chapters 4–5) at the top. Step 6 includes recalibration criteria with specific observable conditions. |
| 10 | PARTIAL | Output identifies any genuine gaps — e.g. no SLI cardinality budgeting, no layered service SLO dependency model, no SLO retro template | PARTIAL (0.5) | The skill leaves three real gaps: (1) no guidance on how many SLIs per service is too many; (2) no mathematical model for composing SLOs across layered service dependencies — the skill notes "your SLOs cannot be better than your worst dependency's SLO" but provides no formula or worked example; (3) no structured SLO retrospective template after budget policy actions fire. |

## Notes

The skill is production-quality and closely follows Google SRE chapters 4–5. A few observations beyond the rubric:

- The `Current reliability` field in the service profile (Step 1) directly enables the achievability rule in Step 3. Collecting that information early means the rule can be applied with data rather than intuition.
- The error budget exceptions section in Step 4 (planned maintenance counted separately, dependency failures flagged) adds practical nuance absent from most SLO templates.
- Burn rate arithmetic is explicit: 720x fast burn (30-day budget in 1 hour), 10x slow burn (30-day budget in 3 days). Engineers configuring alert tooling won't need to derive these.
- The dependency gap identified under output expectation 10 is the most consequential missing piece in practice. A service depending on three upstream services with independent 99.9% SLOs has a compounded availability ceiling of roughly 99.7%. The skill acknowledges the relationship but provides no model for working through the arithmetic.
