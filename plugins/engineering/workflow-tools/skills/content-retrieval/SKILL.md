---
name: content-retrieval
description: "Retrieve content from a URL using a four-tier escalation strategy: WebFetch → curl → Playwright (JS rendering) → BrightData (anti-bot bypass). Use when standard WebFetch fails or when the target URL is known to require JS rendering or bot mitigation bypass."
argument-hint: "[URL to retrieve]"
user-invocable: true
allowed-tools: WebFetch, Bash
---

Retrieve the content at $ARGUMENTS using the appropriate retrieval method.

## Tier selection

Before attempting retrieval, classify the target:

| Signal | Likely tier needed |
|---|---|
| Standard website, no login required | Tier 1 (WebFetch) |
| JavaScript-rendered SPA (React, Vue, Angular) | Tier 3 (Playwright) |
| Known anti-bot protection (Cloudflare, Datadome, PerimeterX) | Tier 4 (BrightData) |
| Previously failed WebFetch with 403/429 | Start at Tier 2 |
| News article, blog, documentation | Tier 1 first |

If classification is uncertain, start at Tier 1 and escalate on failure.

## Tier 1: WebFetch

Use the WebFetch tool. This works for the majority of public content.

**Success:** content returned with meaningful text — proceed.

**Escalate to Tier 2 if:**

- HTTP 403 Forbidden
- HTTP 429 Too Many Requests
- Content returned is empty or contains only a loading placeholder (e.g., `<div id="root"></div>` with no text)
- Response is a CAPTCHA or bot challenge page

## Tier 2: curl with browser headers

Simulate a real browser request by adding common headers.

```bash
curl -s -L \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
  -H "Accept: text/html,application/xhtml+xml,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
  -H "Accept-Language: en-AU,en;q=0.9" \
  -H "Accept-Encoding: gzip, deflate, br" \
  "[URL]"
```

**Success:** HTML returned with content — extract the relevant text and proceed.

**Escalate to Tier 3 if:**

- Response is still a bot challenge
- HTML is returned but content is empty (JavaScript-rendered)
- Site returns a redirect loop

## Tier 3: Playwright (JavaScript rendering)

For JavaScript-rendered content, use Playwright to render the page fully before extracting content.

```bash
npx playwright chromium --no-sandbox "[URL]"
```

Or via a Playwright script if more control is needed:

```javascript
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('[URL]', { waitUntil: 'networkidle' });
  const content = await page.content();
  console.log(content);
  await browser.close();
})();
```

**Prerequisites:** Playwright must be installed (`npm install playwright` or `pip install playwright && playwright install chromium`). Check first — don't assume it's available.

**Success:** fully rendered HTML returned with content — extract and proceed.

**Escalate to Tier 4 if:**

- Playwright session is immediately detected and blocked
- Site uses advanced fingerprinting that defeats headless browsers
- Tier 3 is unavailable (Playwright not installed, not appropriate in this environment)

## Tier 4: BrightData

For sites with aggressive anti-bot protection that defeats all standard approaches.

BrightData's Scraping Browser routes requests through residential proxies with full browser fingerprinting. This is a paid service — confirm it's available in the environment before attempting.

```javascript
const { chromium } = require('playwright-core');
(async () => {
  const browser = await chromium.connectOverCDP(
    'wss://brd-customer-[CUSTOMER_ID]-zone-scraping_browser:PASSWORD@brd.superproxy.io:9222'
  );
  const page = await browser.newPage();
  await page.goto('[URL]', { waitUntil: 'domcontentloaded' });
  const content = await page.content();
  console.log(content);
  await browser.close();
})();
```

Credentials are loaded from environment variables (`BRIGHTDATA_CUSTOMER_ID`, `BRIGHTDATA_PASSWORD`). Never hardcode credentials.

**If Tier 4 fails:** the content is not retrievable by automated means. Report the failure with the specific error, note what was attempted, and suggest manual retrieval or an alternative source.

## Content extraction

Once raw HTML is retrieved (any tier), extract the meaningful content:

1. Strip navigation, headers, footers, sidebars, and ads
2. Extract the main content body
3. Preserve: headings, paragraphs, lists, tables, dates, author names, publication names
4. Note: page title, URL, retrieval date and tier used

For structured data (tables, JSON-LD, microdata), extract the structure rather than the raw HTML.

## Apify filtering (optional, for high-volume tasks)

When retrieving content from a domain with a known Apify actor that produces cleaner output than raw HTML scraping, prefer the actor over raw retrieval. Check the Apify store with a targeted search before writing a custom extraction:

```
apify.com/store?search=[domain name]
```

Existing actors for common targets (LinkedIn, Amazon, social platforms) produce better-structured output than HTML parsing. Use them when available — don't build custom scrapers for already-solved problems.

## Rules

- Start at Tier 1 unless you have a strong reason to skip it.
- Escalate on failure, not preemptively.
- Never hardcode credentials. Use environment variables.
- Confirm Playwright and BrightData availability before attempting Tier 3 or 4.
- Respect `robots.txt` for Tier 1 and 2. Tiers 3 and 4 bypass these — use only when there is a legitimate purpose and the requester has confirmed compliance with the target site's terms of service.
- Log the tier used and any errors encountered in the output.

## Output format

```markdown
### Content retrieval: [URL]

**Date:** [today]
**Tier used:** [1 / 2 / 3 / 4]
**Escalation path:** [e.g., Tier 1 failed (403) → Tier 2 succeeded]

### Retrieved content

[Extracted text content with structure preserved]

### Metadata

- **Title:** —
- **Publication date:** —
- **Author:** —
- **Word count (approximate):** —

### Notes

[Any content quality issues, partial retrieval, or access limitations]
```
