# Test: content-retrieval skill

Scenario: A researcher needs to retrieve the content of a JavaScript-rendered report page that returned an empty response when fetched directly.

## Prompt

/workflow-tools:content-retrieval https://transparency.gov.au/annual-reports/australian-signals-directorate/reporting-year/2023-24 — WebFetch returned an empty div with no content, likely JS-rendered

## Criteria

- [ ] PASS: Skill classifies the target before attempting retrieval — identifies JS-rendered SPA as the likely Tier 3 case based on the empty response signal
- [ ] PASS: Escalation is sequential — Tier 1 (WebFetch) is attempted or noted as already failed, then Tier 2 (curl with browser headers) before jumping to Tier 3
- [ ] PASS: Tier 3 Playwright command is used for JavaScript rendering — skill checks whether Playwright is available before attempting
- [ ] PASS: Tier 4 escalates to human with actionable options (manual retrieval, managed services, Apify actors, alternative sources) rather than attempting flaky automated workarounds
- [ ] PASS: robots.txt compliance is noted — Tier 3 bypasses it, and skill acknowledges this requires legitimate purpose and terms of service confirmation
- [ ] PASS: Retrieved content is extracted with structure preserved — navigation, headers, footers stripped; headings, paragraphs, tables retained
- [ ] PARTIAL: Output includes the tier used, escalation path taken, and any content quality issues or partial retrieval notes
- [ ] PASS: If all tiers fail, skill reports the failure with specific errors and suggests manual retrieval or an alternative source — does not fabricate content
