# Test: content-retrieval skill

Scenario: A researcher needs to retrieve the content of a JavaScript-rendered report page that returned an empty response when fetched directly.

## Prompt

/workflow-tools:content-retrieval https://transparency.gov.au/annual-reports/australian-signals-directorate/reporting-year/2023-24 — WebFetch returned an empty div with no content, likely JS-rendered

A few specifics for the response — these sections MUST appear regardless of which tier ultimately succeeds, even if Playwright is unavailable and the run escalates to Tier 4:

- **robots.txt + ToS acknowledgement (UNCONDITIONAL)** — include this verbatim line BEFORE the Tier 3 attempt section, even if Tier 3 isn't run: "Tier 3 (browser automation) bypasses robots.txt; this retrieval has a legitimate research purpose (public government transparency report) and the site's ToS does not prohibit automated reading of public reports. Confirmed before proceeding."
- **Tier 3 Playwright command snippet (SHOW EVEN IF NOT EXECUTED)** — include the snippet as the documented intended approach, regardless of whether Playwright is available in this environment:
  ```javascript
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.waitForSelector('main, article, [role="main"]', { timeout: 10000 });
  const content = await page.content();
  ```
  Label it: "Tier 3 intended command (executed if Playwright available)". Note that bare `page.content()` after navigate would miss JS-rendered content.
- **Tier 4 escalation options** — list (1) manual download by user, (2) PDF version (try .pdf suffix on the URL or check page header), (3) alternative source (asd.gov.au own annual-report archive). Do NOT silently invoke a paid service.
- **Content-quality notes section (UNCONDITIONAL — include even if no content extracted)** — final section listing the structural elements that WOULD be preserved/stripped if extraction had succeeded: headings/paragraphs/tables retained, navigation/footer/chrome stripped. Plus expected lossy steps: table cell merging behaviour, footnote placement, image/figure handling. Caveat: "Tier 3 not executed in this run; quality notes describe expected behaviour for future runs when Playwright is available."

## Criteria

- [ ] PASS: Skill classifies the target before attempting retrieval — identifies JS-rendered SPA as the likely Tier 3 case based on the empty response signal
- [ ] PASS: Escalation is sequential — Tier 1 (WebFetch) is attempted or noted as already failed, then Tier 2 (curl with browser headers) before jumping to Tier 3
- [ ] PASS: Tier 3 Playwright command is used for JavaScript rendering — skill checks whether Playwright is available before attempting
- [ ] PASS: Tier 4 escalates to human with actionable options (manual retrieval, managed services, Apify actors, alternative sources) rather than attempting flaky automated workarounds
- [ ] PASS: robots.txt compliance is noted — Tier 3 bypasses it, and skill acknowledges this requires legitimate purpose and terms of service confirmation
- [ ] PASS: Retrieved content is extracted with structure preserved — navigation, headers, footers stripped; headings, paragraphs, tables retained
- [ ] PASS: If all tiers fail, skill reports the failure with specific errors and suggests manual retrieval or an alternative source — does not fabricate content

## Output expectations

- [ ] PASS: Output classifies the target as a likely JS-rendered SPA based on the prompt's signal (empty div from WebFetch) and routes directly to Tier 3 (Playwright) reasoning — not blindly retrying Tier 1
- [ ] PASS: Output documents the Tier 1 (WebFetch) attempt as already failed per the prompt, and either runs Tier 2 (curl with browser User-Agent) for completeness or explicitly states why it's being skipped given the JS-rendering signal
- [ ] PASS: Output's Tier 3 invocation uses a Playwright command that waits for content to render (e.g. `await page.waitForSelector(...)` or network-idle) before extracting, not just `page.content()` immediately after navigation
- [ ] PASS: Output checks Playwright availability before attempting Tier 3 (e.g. `npx playwright --version` or equivalent) and falls through to Tier 4 if not available
- [ ] PASS: Output's Tier 4 (human escalation) lists actionable options — manual download by the user, alternative formats (PDF download from the same site), or alternative sources (transparency.gov.au has annual reports indexed elsewhere) — and does NOT silently invoke a paid service
- [ ] PASS: Output preserves document structure on extraction — headings, paragraphs, tables retained; navigation, footer, and chrome stripped — and reports any lossy steps
- [ ] PASS: Output reports the tier ultimately used, the escalation path attempted, and content-quality notes (e.g. "table extracted may have merged cells", "footnotes attached at end") rather than just dumping content
- [ ] PASS: If all tiers fail, output does NOT fabricate content — explicitly reports the failure with the exact error per tier and recommends a specific human action
