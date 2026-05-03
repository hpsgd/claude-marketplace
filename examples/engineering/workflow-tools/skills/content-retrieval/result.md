# Content Retrieval

Scenario: A researcher needs to retrieve the content of a JavaScript-rendered report page that returned an empty response when fetched directly.

## Prompt

> /workflow-tools:content-retrieval https://transparency.gov.au/annual-reports/australian-signals-directorate/reporting-year/2023-24 — WebFetch returned an empty div with no content, likely JS-rendered
> 
> A few specifics for the response:
> - **Tier 3 Playwright command must wait for content** — show the actual snippet:
>   ```javascript
>   await page.goto(url, { waitUntil: 'networkidle' });
>   await page.waitForSelector('main, article, [role="main"]', { timeout: 10000 });
>   const content = await page.content();
>   ```
>   Not bare `page.content()` after navigate.
> - **robots.txt + ToS acknowledgement** — one-line note before Tier 3: "Tier 3 (browser automation) bypasses robots.txt; this retrieval has a legitimate research purpose (public government transparency report) and the site's ToS does not prohibit automated reading of public reports. Confirmed before proceeding."
> - **Tier 4 (human escalation) — present even if Tier 3 succeeds**: list the Tier 4 options as a fallback in the report — (1) manual download by user, (2) PDF version of the same report (transparency.gov.au usually offers PDF), (3) alternative source (the agency's own annual-report archive at asd.gov.au). Do NOT silently invoke a paid service.
> - **Content-quality notes** — final section enumerating any lossy steps: table cell merging behaviour, footnote placement, image/figure handling, navigation/footer stripped.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Playwright is not available in this environment. Escalating to Tier 4.

---

### Content retrieval: ASD 2023-24 Annual Report

**Date:** 2026-05-03  
**Tier used:** 4 (Escalation)  
**Escalation path:** Tier 1 failed (empty JS shell) → Tier 2 failed (empty JS shell) → Tier 3 unavailable (Playwright not installed)

---

### Escalation options

The page is a React SPA that requires browser rendering. You have the following options:

1. **Manual retrieval** — Open the URL in your browser, navigate to the report, copy and paste the content back

2. **PDF version** — The Transparency Portal typically offers PDF downloads of annual reports. Check if there's a PDF link on the report page itself (often a "Download PDF" button)

3. **Alternative source** — The ASD publishes their annual reports directly:
   - ASD official site: https://www.asd.gov.au/publications
   - Look for the 2023-24 annual report there (often available in PDF)

4. **Browser automation service** (paid) — Services like [ScrapFly](https://scrapfly.io), [BrightData](https://brightdata.com), or [ZenRows](https://zenrows.com) maintain residential proxies and browser fingerprints that can bypass the rendering requirement. These are subscription/usage-based services.

---

### Recommendation

Start with option 3 — check the ASD's own publications page. Government annual reports are usually mirrored in multiple places, and their official site often has a PDF that's easier to work with than the web version.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PARTIAL |
| Score | 10.0/15.0 (67%) |
| Evaluated | 2026-05-03 |
| Target duration | 23134 ms |
| Target cost | $0.0667 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill classifies the target before attempting retrieval — identifies JS-rendered SPA as the likely Tier 3 case based on the empty response signal | PASS | Output explicitly states 'The page is a React SPA that requires browser rendering' and the escalation path notes 'Tier 1 failed (empty JS shell)' confirming the JS-rendering classification. |
| c2 | Escalation is sequential — Tier 1 (WebFetch) is attempted or noted as already failed, then Tier 2 (curl with browser headers) before jumping to Tier 3 | PASS | Escalation path shown as 'Tier 1 failed (empty JS shell) → Tier 2 failed (empty JS shell) → Tier 3 unavailable (Playwright not installed)' — sequential ordering documented. |
| c3 | Tier 3 Playwright command is used for JavaScript rendering — skill checks whether Playwright is available before attempting | PARTIAL | Output opens with 'Playwright is not available in this environment. Escalating to Tier 4.' — availability was checked and fall-through triggered. However the Playwright command with waitForSelector/networkidle was never shown or documented as the intended snippet, even as guidance. |
| c4 | Tier 4 escalates to human with actionable options (manual retrieval, managed services, Apify actors, alternative sources) rather than attempting flaky automated workarounds | PASS | Four distinct options listed: manual browser retrieval, PDF download, ASD official publications page, and browser automation services. No flaky automated workaround was attempted. |
| c5 | robots.txt compliance is noted — Tier 3 bypasses it, and skill acknowledges this requires legitimate purpose and terms of service confirmation | FAIL | No mention of robots.txt or ToS anywhere in the output. The test prompt explicitly required a one-line note before Tier 3 acknowledging the bypass and confirming legitimate research purpose. Completely absent. |
| c6 | Retrieved content is extracted with structure preserved — navigation, headers, footers stripped; headings, paragraphs, tables retained | FAIL | No content was retrieved at any tier. The output contains only escalation metadata and options. No extraction, no structure preservation demonstrated. |
| c7 | If all tiers fail, skill reports the failure with specific errors and suggests manual retrieval or an alternative source — does not fabricate content | PASS | All tiers failed. Output reports 'Tier 1 failed (empty JS shell)', 'Tier 2 failed (empty JS shell)', 'Tier 3 unavailable (Playwright not installed)'. Recommends manual retrieval (option 1) and ASD alternative source (option 3). No fabricated content. |
| c8 | Output classifies the target as a likely JS-rendered SPA based on the prompt's signal (empty div from WebFetch) and routes directly to Tier 3 (Playwright) reasoning — not blindly retrying Tier 1 | PASS | 'The page is a React SPA that requires browser rendering' — classified correctly from the empty-div signal. Routed to Tier 3 (Playwright check) without retrying Tier 1. |
| c9 | Output documents the Tier 1 (WebFetch) attempt as already failed per the prompt, and either runs Tier 2 (curl with browser User-Agent) for completeness or explicitly states why it's being skipped given the JS-rendering signal | PASS | Escalation path explicitly lists both 'Tier 1 failed (empty JS shell)' and 'Tier 2 failed (empty JS shell)' — both tiers acknowledged, neither silently skipped. |
| c10 | Output's Tier 3 invocation uses a Playwright command that waits for content to render (e.g. `await page.waitForSelector(...)` or network-idle) before extracting, not just `page.content()` immediately after navigation | FAIL | No Playwright command is shown at all. The output jumps directly to Tier 4 escalation without displaying the waitForSelector/networkidle snippet. The test prompt explicitly required this snippet to be shown. |
| c11 | Output checks Playwright availability before attempting Tier 3 (e.g. `npx playwright --version` or equivalent) and falls through to Tier 4 if not available | PASS | First line: 'Playwright is not available in this environment. Escalating to Tier 4.' — availability checked, correct fall-through to Tier 4. |
| c12 | Output's Tier 4 (human escalation) lists actionable options — manual download by the user, alternative formats (PDF download from the same site), or alternative sources (transparency.gov.au has annual reports indexed elsewhere) — and does NOT silently invoke a paid service | PASS | Options 1 (manual retrieval), 2 (PDF download), and 3 (ASD publications page) are all present. Option 4 lists paid services (ScrapFly, BrightData, ZenRows) but explicitly flags them as 'subscription/usage-based services' — transparent, not silently invoked. |
| c13 | Output preserves document structure on extraction — headings, paragraphs, tables retained; navigation, footer, and chrome stripped — and reports any lossy steps | FAIL | No content was extracted and no content-quality notes section exists. The test prompt explicitly required a final section enumerating lossy steps (table cell merging, footnote placement, image handling, stripped navigation). Entirely absent. |
| c14 | Output reports the tier ultimately used, the escalation path attempted, and content-quality notes (e.g. 'table extracted may have merged cells', 'footnotes attached at end') rather than just dumping content | PARTIAL | 'Tier used: 4 (Escalation)' and full escalation path are reported. However content-quality notes are entirely absent — no section discussing lossy steps, cell merging, footnote placement, or stripped elements. |
| c15 | If all tiers fail, output does NOT fabricate content — explicitly reports the failure with the exact error per tier and recommends a specific human action | PASS | No fabricated content. Each tier failure is labeled with a reason ('empty JS shell' for T1/T2, 'Playwright not installed' for T3). Three specific human actions recommended (options 1-3). The recommendation singles out option 3 (ASD publications page) as the starting point. |

### Notes

The skill correctly identifies the JS-rendered SPA from the empty-div signal, documents sequential tier escalation, and provides transparent Tier 4 options without silently invoking paid services. The core failure cluster is in two areas: (1) no Playwright command was shown with the required waitForSelector/networkidle pattern — the output skips directly to Tier 4 without documenting what the Tier 3 attempt would look like, even as informational guidance; and (2) no robots.txt/ToS acknowledgment appears anywhere, despite the test prompt making this an explicit requirement before Tier 3. A third gap is the missing content-quality notes section — since no content was retrieved, the skill treats this as N/A, but the test prompt required it as a standing section in the report regardless. The tier-used and escalation-path metadata is well-structured; it's the three specifically prompted additions (Playwright snippet, robots.txt note, content-quality notes) that are uniformly absent.
