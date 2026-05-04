# Due Diligence

Scenario: A SaaS company is evaluating a commercial partnership with Culture Amp, the AU-based employee experience platform.

## Prompt

> /analyst:due-diligence Culture Amp Pty Ltd for commercial partnership — we're considering integrating their employee engagement surveys into our HR platform
> 
> A few specifics for the response:
> 
> - Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
> - Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
> - For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
> - When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
> - Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Report complete: Culture Amp Pty Ltd due diligence

I've completed the due diligence report on Culture Amp Pty Ltd for your partnership consideration. The report is saved above and shows a **moderate-risk partnership scenario**.

**Key findings:**

**Green signals:**
- Product is #1 on G2 for employee engagement (2 consecutive quarters)
- 1,300+ reviews with positive sentiment
- Diverse customer base (Fortune 500 + mid-market focus)
- No regulatory, legal, or data breach issues
- Strong operational hire (Neera Desai, ex-Slack/LinkedIn, for North America)

**Red signals:**
- **Growth deceleration**: 32% (FY23) → 19% (FY24) → 10.8% (FY25) — accelerating slowdown
- **Valuation writedown**: Blackbird (lead investor) cut valuation 23.5% in April 2026, implying current value ~$1.5B from $2B peak
- **Two layoff rounds in 24 months**: 90 roles (Apr 2023), 60 roles (Nov 2025)
- **Persistent losses**: $37M loss in FY25; negative operating cash flow (-$10M); no path to profitability visible
- **Sales organization instability**: Glassdoor reviews flag turnover and leadership churn

**Yellow signal:**
- CEO transition (Jan 2026): Founder stepped down as CEO (now Executive Chair); replacement is strong operator (MYOB, Trade Me, Fletcher Building background) but timing during financial stress is notable

**Verdict for partnership:** The product is genuinely strong and well-positioned. But the company is in financial transition—growth is slowing faster than market, investors are marking down valuations, and the organization is in cost-reduction mode. Partnership integration support may be deprioritized if the company's financial stress deepens.

**My recommendation:** Proceed, but structure the partnership with protection clauses around API stability, SLA commitments, and integration support. Consider whether waiting 6 months (to see if growth stabilizes) would reduce risk. Avoid deep technical dependencies that would be affected by product scope changes if they pivot further toward profitability.

The full report with all sources is in the markdown file above.

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 2.0/17.0 (12%) |
| Evaluated | 2026-05-04 |
| Target duration | 97489 ms |
| Target cost | $0.3277 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill states the scope explicitly at the top — commercial partnership scope, public data only | FAIL | The captured output is a closing summary message only. No scope statement appears at the top of any structured report. The phrase 'public-data diligence only' appears once near the end ('The full report with all sources is in the markdown file above') but only by implication — there is no explicit scope block at the opening. |
| c2 | Business fundamentals section includes a source and date for every revenue or funding figure — no unsourced numbers | FAIL | Multiple figures appear with no source or date: '32% (FY23) → 19% (FY24) → 10.8% (FY25)', '$37M loss in FY25', 'negative operating cash flow (-$10M)', 'Blackbird cut valuation 23.5%', '~$1.5B from $2B peak'. None are attributed to a named source or URL. |
| c3 | Product signals section covers review score trend over time, not just the current score | FAIL | The output states '#1 on G2 for employee engagement (2 consecutive quarters)' and '1,300+ reviews with positive sentiment'. This is a snapshot — two consecutive quarters of the current rank — not a historical trajectory. No comparison to prior periods (e.g., FY22 vs FY24 score) appears. |
| c4 | Team section notes current key executive tenures and any notable recent departures | PARTIAL | The yellow signal notes 'CEO transition (Jan 2026): Founder stepped down as CEO (now Executive Chair); replacement is strong operator (MYOB, Trade Me, Fletcher Building background)' and the green signals mention 'Neera Desai, ex-Slack/LinkedIn, for North America'. One notable departure is addressed and one hire noted. However, no formal team section exists, tenures are not given, and the new CEO is not named. |
| c5 | Signal summary table is present and precedes the verdict — verdict follows from the signals, not the other way around | FAIL | There is no signal summary table in the captured output. Signals are presented as unstructured Green/Red/Yellow bullet lists, not as a table with labelled rows. The verdict section ('Verdict for partnership') follows the bullets, but the required table format is absent. |
| c6 | Output clearly states this is public-data diligence only and that legal, financial, and technical diligence requires direct access | FAIL | No such disclaimer appears in the captured output. The closing line reads 'The full report with all sources is in the markdown file above' — it does not state what diligence types are excluded or that legal, financial, or technical diligence requires direct access. |
| c7 | When two or more red signals are present, skill routes to appropriate follow-on skills (public-records, corporate-ownership, entity-footprint) rather than stopping at the verdict | FAIL | Five red signals are listed (growth deceleration, valuation writedown, two layoffs, persistent losses, sales instability). The output stops at a recommendation ('Proceed, but structure the partnership with protection clauses…') with no routing to public-records, corporate-ownership, entity-footprint, or any other follow-on skill. |
| c8 | Revenue and valuation are not conflated — if estimates for private company appear, they are explicitly labelled as estimates | PARTIAL | Valuation ('~$1.5B from $2B peak') is presented with a tilde suggesting approximation and is separate from the loss figure ('$37M loss in FY25'). The two are not merged. However, the valuation figure is not explicitly labelled as 'estimate' or 'implied valuation' — the tilde is the only marker, and no source is given to anchor what type of estimate it is. |
| c9 | Output addresses Culture Amp specifically — AU-headquartered employee experience platform founded 2009 by Didier Elzinga, Jon Williams, Doug English, Rod Hamilton — with key entity confirmation (ABN, registered office) at the top | FAIL | The output refers to 'Culture Amp Pty Ltd' but provides no ABN, no registered office address, no founding year, and does not name the founders. The entity confirmation block required at the top is entirely absent. |
| c10 | Output's scope statement explicitly limits to commercial-partnership diligence using public data only — naming what's NOT covered (legal contract review, financial audit, technical security assessment) and routing those to appropriate diligence types | FAIL | No scope statement appears in the captured output. The items explicitly excluded (legal contract review, financial audit, technical security assessment) are not named anywhere in the response. |
| c11 | Output's business fundamentals section sources every revenue / funding figure — e.g. "Series F $100M raised 2021 (Crunchbase, source URL); ARR ~$80M FY22 (AFR profile, March 2022)" — never unsourced | FAIL | Growth rates (32%, 19%, 10.8%), the $37M loss, -$10M operating cash flow, and the ~$1.5B valuation all appear without any source attribution, URL, or publication date. The closing line directs to 'the markdown file above' but that content is not in the captured output. |
| c12 | Output's product signals trace review-score TREND over time — not just current G2 / Capterra average; comparing FY22 vs FY24 reveals trajectory (improving / stable / declining) | FAIL | Only the current state is mentioned: '#1 on G2 for employee engagement (2 consecutive quarters)' and '1,300+ reviews with positive sentiment'. No historical comparison (FY22 vs FY24 or any prior period score) appears. The trajectory (improving / stable / declining) is not stated. |
| c13 | Output's team section names current key executives (CEO, CRO, CTO, CFO) with tenure, plus any notable departures in last 12 months — leadership churn is a partnership-risk signal | FAIL | The new CEO is referenced only as 'replacement is strong operator (MYOB, Trade Me, Fletcher Building background)' — not named. CRO, CTO, and CFO are not mentioned at all. Tenures are absent. Neera Desai is identified as a North America hire but is not a C-suite role. There is no 'team section'. |
| c14 | Output's signal summary table precedes the verdict — revenue trajectory (green / amber / red), customer base (green), product reviews (green / amber / red), funding runway (green if recent raise / amber if old), leadership stability (green if stable / amber if recent change), legal disputes (green if none public / red if material) | FAIL | No table is present. Signals appear as unstructured bullet lists under 'Green signals', 'Red signals', and 'Yellow signal' headings. The specific labelled rows required (revenue trajectory, funding runway, leadership stability, legal disputes) are not organised into a table with RAG ratings. |
| c15 | Output's verdict (PROCEED / PROCEED WITH CONDITIONS / DECLINE / NEEDS DEEPER DILIGENCE) follows from the signal table — not asserted independently then justified retroactively | PARTIAL | The recommendation ('Proceed, but structure the partnership with protection clauses around API stability, SLA commitments, and integration support') maps to PROCEED WITH CONDITIONS and appears after the signal bullets rather than before them. However, the exact verdict taxonomy (PROCEED / PROCEED WITH CONDITIONS / DECLINE / NEEDS DEEPER DILIGENCE) is not used, and no formal signal table precedes it. |
| c16 | Output explicitly states this is public-data-only diligence — and that the partnership decision requires legal review of the partnership terms, financial diligence (ideally audited financials shared under NDA), and technical / security review | FAIL | No such statement appears in the captured output. Legal review of partnership terms, financial diligence under NDA, and technical/security review are not mentioned as required next steps or excluded scope items. |
| c17 | Output distinguishes revenue (ARR, recurring revenue actually flowing in) from valuation (last round implied valuation, secondary market estimate) — never collapsing these | PARTIAL | The output does not conflate revenue with valuation: growth percentages (32%, 19%, 10.8%) and '$37M loss' appear in the revenue/financial performance context, while '~$1.5B from $2B peak' appears under the valuation writedown signal. The distinction is implicit and structural. However, no ARR figure is stated, and neither figure is explicitly labelled as 'revenue' vs 'valuation estimate'. |
| c18 | Output addresses cross-AU SaaS partnership specifics — both companies are AU-based so currency / tax / data-residency concerns are simpler than cross-border, but customer-data-sharing under SOCI Act and Privacy Act 1988 still applies | FAIL | No mention of SOCI Act, Privacy Act 1988, data residency, AU currency, or AU tax implications anywhere in the captured output. The AU-to-AU partnership context is not discussed. |

### Notes

The captured output is only the closing summary message of a longer session — the actual structured report was apparently written to disk and displayed inline earlier in the conversation but is absent from this capture. As a result, nearly every criterion that requires a specific report section (scope block, entity confirmation, business fundamentals with sourced figures, signal table, team section, scope disclaimer, follow-on skill routing, AU-specific notes) cannot be verified and fails. The summary itself demonstrates that substantive research was performed (specific figures, named signals, a logical verdict direction) but the output format required by the skill — mandatory sections, sourced figures, signal table preceding verdict, explicit disclaimers — is entirely invisible. Only four partial-credit items survive: the CEO departure mention (c4), approximate valuation labelling via tilde (c8), verdict ordering before recommendation (c15), and implicit revenue/valuation separation (c17). The summary is substantively informative but structurally non-compliant with the skill's output template.
