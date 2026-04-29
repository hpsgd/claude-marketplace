# Output: content-retrieval skill

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 15/15 criteria met (100%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Skill classifies the target before attempting retrieval — tier-selection table maps JS-rendered SPA to Tier 3; Tier 1 escalation conditions cover the empty-div signal from the prompt
- [x] PASS: Escalation is sequential — Tier 2 explicitly documents when to skip to Tier 3 (confirmed JS rendering), preserving the numbered 1→2→3→4 escalation model
- [x] PASS: Tier 3 Playwright command used for JS rendering with availability check — script present with `waitUntil: 'networkidle'`; Prerequisites state "Check first — don't assume it's available"
- [x] PASS: Tier 4 escalates to human with actionable options — manual retrieval, managed scraping services (flagged as paid), Apify actors, and alternative sources all listed; no flaky automated fallbacks
- [x] PASS: robots.txt compliance noted — Rules section states Tier 1 and 2 respect it; Tier 3 and 4 bypass it and require legitimate purpose with terms-of-service confirmation
- [x] PASS: Content extraction strips nav/header/footer/sidebars/ads and preserves headings, paragraphs, lists, tables
- [x] PASS: Failure reporting without fabrication — Tier 4 requires reporting what was attempted, why it failed, and human-resolvable options; Rules section requires logging tier and errors

### Output expectations

- [x] PASS: Tier selection table maps JS-rendered SPA to Tier 3; the empty-div prompt signal matches the Tier 1 escalation condition, so the skill would classify as Tier 3 and document Tier 1 as already failed
- [x] PASS: Tier 2 skip logic is explicit — "Skip Tier 2 when the cause is confirmed JS rendering (empty container, framework markers)" — skill would skip Tier 2 and document the reason
- [x] PASS: Tier 3 script uses `waitUntil: 'networkidle'` before extracting — rendering is complete before `page.content()` is called
- [x] PASS: Playwright availability check is explicit in Prerequisites and in the Rules section; Tier 3 escalation conditions include "Playwright not installed, not appropriate in this environment"
- [x] PASS: Tier 4 names managed services as paid with usage-based pricing; the cost decision is delegated to the human; no silent automated invocation of paid services
- [x] PASS: Extraction section preserves document structure and strips chrome; output format template includes Notes field for content quality issues and lossy steps
- [x] PASS: Output format template includes Tier used, Escalation path, and Notes fields for content quality observations
- [x] PASS: Tier 4 requires exact error reporting per tier and human-action options; no fabrication path exists in the skill definition

## Notes

The skill is well-constructed. The Tier 2 skip logic for confirmed JS rendering is a meaningful addition — it avoids a pointless curl round-trip when the signal is unambiguous, which was a gap in the previous version. The paid-service flag in Tier 4 is present and adequate: services are named with explicit cost framing and the decision is left to the human. The Playwright script uses `waitUntil: 'networkidle'` which correctly covers the rendering wait before extraction. The domain-specificity criterion from the prior evaluation was removed in the updated test.md, which aligns the rubric with what a generic skill is designed to do.
