# Output: content-retrieval skill

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 14/18 criteria met (78%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Skill classifies the target before attempting retrieval — met. The tier-selection table maps "JavaScript-rendered SPA (React, Vue, Angular)" to Tier 3. Tier 1 escalation conditions cover "Content returned is empty or contains only a loading placeholder" which matches the scenario signal exactly.
- [x] PASS: Escalation is sequential — met. Each tier section defines explicit failure conditions before escalation triggers. The Rules section reinforces "Start at Tier 1 unless you have a strong reason to skip it. Escalate on failure, not preemptively."
- [x] PASS: Tier 3 Playwright command with availability check — met. Tier 3 includes both a `npx playwright chromium` command and a full JavaScript script. Prerequisites explicitly state "Check first — don't assume it's available."
- [x] PASS: Tier 4 escalates to human with actionable options — met. Four options listed: manual retrieval, managed scraping services (ScrapFly, BrightData, ZenRows), Apify actors, alternative sources. The section explicitly prohibits flaky open-source workarounds and defers the cost decision to the human.
- [x] PASS: robots.txt compliance noted for Tier 3 — met. The Rules section states Tier 1 and 2 respect robots.txt; Tiers 3 and 4 bypass it and require legitimate purpose with terms-of-service confirmation.
- [x] PASS: Content extraction strips noise and preserves structure — met. The Content extraction section lists what to strip (navigation, headers, footers, sidebars, ads) and what to preserve (headings, paragraphs, lists, tables, dates, author names, publication names).
- [~] PARTIAL: Output includes tier used, escalation path, and content quality notes — partially met. The output format template specifies `**Tier used:**`, `**Escalation path:**`, and a `### Notes` section for content quality issues. Scored as PARTIAL per criterion type.
- [x] PASS: Failure reporting is honest with no fabricated content — met. Tier 4 requires reporting what was attempted, why it failed, and presenting human-resolvable options. The rules say "Log the tier used and any errors encountered in the output."

### Output expectations

- [x] PASS: Output classifies the target as a likely JS-rendered SPA and routes to Tier 3 reasoning — met. The tier-selection table maps JS-rendered SPA to Tier 3. The Tier 1 escalation conditions cover the empty div signal, so the skill would correctly identify and classify the case.
- [~] PARTIAL: Output documents the Tier 1 attempt as already failed and either runs Tier 2 or explains skipping it — partially met. The skill says "Start at Tier 1 unless you have a strong reason to skip it" and lacks an explicit rule for skipping Tier 2 when the JS-rendering cause is already known. The skill may run Tier 2 for completeness, but does not instruct when to skip it given a confirmed JS-rendering signal.
- [~] PARTIAL: Output's Tier 3 invocation waits for content to render before extracting — partially met. The full Playwright script uses `waitUntil: 'networkidle'`, which handles rendering correctly. However, the simpler `npx playwright chromium` command at the top of Tier 3 provides no explicit wait mechanism. A developer following the short-form command would not wait for JS rendering.
- [x] PASS: Output checks Playwright availability before attempting Tier 3 — met. Prerequisites state "Check first — don't assume it's available." The Rules section also says "Confirm Playwright availability before attempting Tier 3."
- [x] PASS: Tier 4 lists actionable options and does not silently invoke a paid service — met. Managed services are flagged explicitly as paid with usage-based pricing. The decision is delegated to the human. No automated invocation of paid services.
- [x] PASS: Output preserves document structure on extraction and reports lossy steps — met. Content extraction section specifies what to strip and what to preserve. The Notes section in the output template covers content quality issues and partial retrieval.
- [ ] FAIL: Output addresses the transparency.gov.au domain context explicitly — not met. The skill is generic and contains no domain-specific guidance. It would not reference Australian government transparency reports, public disclosure context, or the specific site's structure. The output would be generic retrieval commentary.
- [x] PASS: Output reports the tier used, escalation path, and content-quality notes — met. The output format template includes `**Tier used:**`, `**Escalation path:**`, and a `### Notes` section.
- [x] PASS: If all tiers fail, output does not fabricate content — met. Tier 4 requires explicit reporting of what was attempted and why it failed, with human-resolvable options presented. No path produces or suggests fabricated content.
- [~] PARTIAL: Output checks for an alternative format before committing to scraping JS-rendered HTML — partially met. The skill mentions alternative formats (PDF, RSS feed) in the Tier 4 options, but only after Tiers 1–3 have been attempted. There is no instruction to check for a PDF or data API equivalent before starting the JS scraping attempt.

## Notes

The previous result.md only scored the `## Criteria` section and ignored the `## Output expectations` section entirely. This re-evaluation covers both.

The skill is structurally sound. The gap that drops this to PARTIAL is the domain-specificity criterion: a skill that is deliberately generic will not address context like "Australian government transparency report, public disclosure" explicitly. That is a design trade-off, not a defect, but it does fail the criterion as written.

Two weaker spots worth noting. First, the short-form Playwright command (`npx playwright chromium "[URL]"`) does not include a wait mechanism. A developer using that path would get whatever the page emits at navigation time, not the fully-rendered content. The full script path handles this correctly with `waitUntil: 'networkidle'`. The short form should either be removed or annotated with a `--wait-for-selector` or equivalent flag. Second, the alternative-format check happens only at Tier 4. For government transparency sites that routinely publish PDFs alongside HTML pages, checking for a PDF link or a `?format=pdf` variant before starting Playwright would save work and produce cleaner output. The skill does not instruct this as a preliminary step.

The BrightData citation in Tier 4 is correctly handled — it is a human decision with explicit cost acknowledgment, not an automated code path.
