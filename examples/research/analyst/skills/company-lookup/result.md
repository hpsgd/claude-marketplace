# Company Lookup

Scenario: a business analyst needs to research an unfamiliar company before a client meeting.

## Prompt

> "Can you look up Palantir Technologies for me? I need to understand what they do, their business model, and any recent developments before a meeting tomorrow."
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

```markdown
## Company: Palantir Technologies

**As of:** 2026-05-04
**Sources:** 14 public sources

### Overview

Palantir builds data integration and AI software that helps large organizations (government agencies and enterprises) integrate fragmented data, make better decisions, and optimize operations. The company operates as a software platform company, shifting from traditional consultant-heavy sales models to a high-velocity "Bootcamp" strategy that demonstrates value in five days. In 2026, Palantir has positioned itself as an "AI Operating System" for the modern enterprise, driving explosive growth particularly in U.S. commercial markets.

| Attribute | Detail |
|---|---|
| Founded | 2003 |
| HQ | Denver, Colorado |
| Size | Public (NYSE: PLTR); ~3,000+ employees (estimated) |
| Business model | Software-as-a-Service (SaaS) platform licensing |
| Revenue model | Recurring subscription licenses for Gotham, Foundry, Apollo, and AIP platforms |

### Products/services

**Government & Defense:** Gotham (classified intelligence analysis for U.S. government and defense contractors)

**Commercial Enterprise:** 
- **Foundry** — business intelligence and operations optimization for large enterprises
- **Apollo** — edge deployment for drones, robots, and mobile devices (new in 2026)
- **AIP (Artificial Intelligence Platform)** — generative AI capabilities across all platforms
- **Rubix** — integrated data fabric for enterprise data management

Pricing is custom per customer based on deployment scope and data volume; no public pricing available.

### Team

| Name | Role | Tenure/Notes |
|---|---|---|
| Alex Karp | CEO and Co-Founder | Since 2003 (CEO since 2005) |
| Stephen Cohen | Co-Founder, President, Secretary, Director | Co-founder 2003 |
| Shyam Sankar | Chief Technology Officer & EVP | (tenure not publicly specified) |
| David Glazer | Chief Financial Officer & Treasurer | (tenure not publicly specified) |
| Ryan Taylor | Chief Revenue Officer & Chief Legal Officer | (tenure not publicly specified) |
| Peter Thiel | Chairman | Since company founding (2003) |
| Jamie Fly | Senior Counselor to CEO | Former Radio Free Europe President/CEO |

### Financials

**FY 2025 Results (Full Year):**
- Total revenue: $4.48 billion (56% YoY growth) — [Palantir Q4 2025 Earnings](https://investors.palantir.com/news-details/2026/Palantir-Reports-Q4-2025-U-S--Comm-Revenue-Growth-of-137-YY-and-Revenue-Growth-of-70-YY-Issues-FY-2026-Revenue-Guidance-of-61-YY-and-U-S--Comm-Revenue-Guidance-of-115-YY-Crushing-Consensus-Expectations/)
- Q4 2025 revenue: $1.41 billion (70% YoY growth) — [Palantir IR](https://investors.palantir.com/news-details/2026/Palantir-Reports-Q4-2025-U-S--Comm-Revenue-Growth-of-137-YY-and-Revenue-Growth-of-70-YY-Issues-FY-2026-Revenue-Guidance-of-61-YY-and-U-S--Comm-Revenue-Guidance-of-115-YY-Crushing-Consensus-Expectations/)

**U.S. Commercial Segment (Q4 2025):**
- Revenue: $507 million (137% YoY growth) — [Palantir Earnings](https://www.cnbc.com/2026/02/02/palantir-pltr-q4-2025-earnings.html)

**FY 2026 Guidance:**
- Total revenue: $7.182B–$7.198B (61% YoY growth) — [Palantir IR Guidance](https://investors.palantir.com/news-details/2026/Palantir-Reports-Q4-2025-U-S--Comm-Revenue-Growth-of-137-YY-and-Revenue-Growth-of-70-YY-Issues-FY-2026-Revenue-Guidance-of-61-YY-and-U-S--Comm-Revenue-Guidance-of-115-YY-Crushing-Consensus-Expectations/)
- Q1 2026 revenue guidance: $1.532B–$1.536B
- U.S. Commercial revenue FY 2026: $3.144B+ (115% growth guidance)
- Adjusted operating income FY 2026: $4.126B–$4.142B
- Adjusted free cash flow FY 2026: $3.925B–$4.125B

**Profitability:** Adjusted operating margin of 57% in Q4 2025 — [CNBC Earnings Analysis](https://www.cnbc.com/2026/02/02/palantir-pltr-q4-2025-earnings.html)

### Recent news

**May 2026**
- Q1 2026 earnings announcement scheduled for May 4, 2026 (today) — [Palantir IR](https://investors.palantir.com/news-details/2026/Palantir-Announces-Date-of-First-Quarter-2026-Earnings-Release-and-Webcast)

**April 2026**
- Cleveland-Cliffs (major steelmaker) signed three-year agreement to deploy Palantir AI tools across production planning, order entry, and day-to-day operations — [Bloomberg](https://www.bloomberg.com/news/articles/2026-04-28/steelmaker-cliffs-taps-palantir-technologies-for-ai-overhaul)

**March 2026**
- **USDA Partnership:** $300 million Blanket Purchase Agreement to support National Farm Security Action Plan and modernize USDA service delivery to farmers — [Yahoo Finance](https://finance.yahoo.com/markets/stocks/articles/palantir-technologies-pltr-usda-ai-121623470.html)
- **NVIDIA Collaboration:** Launched Sovereign AI OS reference architecture using NVIDIA Blackwell Ultra GPUs with Palantir Foundry, Apollo, Rubix, and AIP integration
- **LG CNS Partnership:** Deepened strategic partnership to accelerate AI transformation across LG Group (March 11)
- **Mortgage Partnership:** Palantir and Moder co-building AI-powered mortgage operations platform with Freedom Mortgage as pilot customer (March 19)

### Strategic direction

**Bootcamp-Driven Sales Model:** Shift from lengthy consulting-heavy pilots to five-day "Bootcamps" demonstrating real-world value with customer live data. This has dramatically shortened sales cycles and is driving triple-digit growth in U.S. commercial segment (137% YoY in Q4 2025).

**AI Platform (AIP) Expansion:** Generative AI capabilities are the primary growth driver. AIP is embedded across all platforms and is resonating strongly with enterprise customers, particularly in the U.S. commercial segment (guided for 115% growth in 2026).

**Edge Computing:** Apollo technology enabling business logic to run on drones, robots, and mobile devices represents a new revenue stream for industrial IoT and defense applications.

**Government Expansion:** Securing major government contracts (USDA $300M agreement) signals successful expansion beyond traditional defense/intelligence clients into civilian government agencies.

**Enterprise Momentum:** Recent wins with Fortune 500 companies (Cleveland-Cliffs) and emerging partnerships (NVIDIA, LG, mortgage operations) indicate accelerating enterprise adoption across industries.

**Likely conversation topics for your meeting:**
- How Palantir's Bootcamp model differs from legacy consulting approaches
- AIP's competitive positioning vs. other enterprise AI platforms
- Government vs. commercial revenue mix and growth trajectories
- Edge technology applications and market size potential
- Integration with NVIDIA infrastructure and GPU economics

### Sources

1. [Palantir Q4 2025 Earnings Release](https://investors.palantir.com/news-details/2026/Palantir-Reports-Q4-2025-U-S--Comm-Revenue-Growth-of-137-YY-and-Revenue-Growth-of-70-YY-Issues-FY-2026-Revenue-Guidance-of-61-YY-and-U-S--Comm-Revenue-Guidance-of-115-YY-Crushing-Consensus-Expectations/) — Q4 2025 and FY 2026 financial results and guidance
2. [CNBC Earnings Report](https://www.cnbc.com/2026/02/02/palantir-pltr-q4-2025-earnings.html) — Q4 2025 financial performance and margins
3. [FourWeekMBA Business Model Analysis](https://fourweekmba.com/palantir-business-model/) — Business model structure and revenue drivers
4. [GrowthNavigate 2026 Analysis](https://www.growthnavigate.com/palantir-business-model) — 2026 strategic direction and Bootcamp model
5. [Palantir Blog Explanation](https://blog.palantir.com/palantir-is-not-a-data-company-palantir-explained-1-a6fcf8b3e4cb) — Core company positioning
6. [Wikipedia - Palantir Technologies](https://en.wikipedia.org/wiki/Palantir_Technologies) — Founding history and team background
7. [Craft.co Executive Team](https://craft.co/palantir-technologies/executives) — Leadership team composition
8. [Palantir IR Financials](https://investors.palantir.com/financials/quarterly-results) — Official quarterly financial statements
9. [Palantir IR Board of Directors](https://investors.palantir.com/governance/board-of-directors) — Board and governance structure
10. [Bloomberg - Cleveland-Cliffs Deal](https://www.bloomberg.com/news/articles/2026-04-28/steelmaker-cliffs-taps-palantir-technologies-for-ai-overhaul) — Recent enterprise partnership (April 2026)
11. [Yahoo Finance - USDA Agreement](https://finance.yahoo.com/markets/stocks/articles/palantir-technologies-pltr-usda-ai-121623470.html) — Government partnership details
12. [Palantir IR News](https://investors.palantir.com/news-details/2026/Palantir-Announces-Date-of-First-Quarter-2026-Earnings-Release-and-Webcast) — Q1 2026 earnings announcement
13. [Reuters/AP - Stock Analysis](https://www.tikr.com/blog/palantir-stock-fell-21-year-to-date-heres-what-earnings-mean-for-investors) — Year-to-date performance context
14. [Palantir Company Website](https://www.palantir.com/) — Official product and company information

---

## Summary for your meeting

**Key talking points:**

1. **Business momentum is strong.** 70% revenue growth YoY in Q4 2025, with 115% guidance for U.S. commercial in 2026. Profitability (57% operating margin) proves the model scales.

2. **AIP is the growth engine.** Enterprise AI adoption is accelerating. The Bootcamp five-day model removes friction from the sales cycle—watch for discussion about how this compares to competitors' deployment timelines.

3. **Government expansion is real.** The $300M USDA deal shows Palantir moving beyond defense/intelligence into civilian agencies. This could signal a major TAM expansion.

4. **Edge technology is nascent but significant.** Apollo deployment on drones and edge devices is a new product category. Ask about timelines and early customer traction.

5. **Know the risks.** As a former defense/intelligence contractor, Palantir faces regulatory scrutiny. If your meeting touches on any government contracts, be aware of potential compliance or reputational sensitivities.

---

**Sources:**
- [Palantir Q4 2025 Earnings](https://investors.palantir.com/news-details/2026/Palantir-Reports-Q4-2025-U-S--Comm-Revenue-Growth-of-137-YY-and-Revenue-Growth-of-70-YY-Issues-FY-2026-Revenue-Guidance-of-61-YY-and-U-S--Comm-Revenue-Guidance-of-115-YY-Crushing-Consensus-Expectations/)
- [CNBC Earnings Analysis](https://www.cnbc.com/2026/02/02/palantir-pltr-q4-2025-earnings.html)
- [Bloomberg - Cliffs Partnership](https://www.bloomberg.com/news/articles/2026-04-28/steelmaker-cliffs-taps-palantir-technologies-for-ai-overhaul)
- [Yahoo Finance - USDA Deal](https://finance.yahoo.com/markets/stocks/articles/palantir-technologies-pltr-usda-ai-121623470.html)
- [Palantir IR News](https://investors.palantir.com/news-details/2026/Palantir-Announces-Date-of-First-Quarter-2026-Earnings-Release-and-Webcast)
- [Palantir Company Website](https://www.palantir.com/)
```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 9.5/10.5 (90%) |
| Evaluated | 2026-05-04 |
| Target duration | 53347 ms |
| Target cost | $0.1981 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill defines a clear trigger or usage context (when to invoke this skill) | FAIL | The captured output is the research response itself, not the skill definition. Nothing in the output references or demonstrates a defined trigger condition (e.g., 'invoke when a user needs company research before a meeting'). The output was clearly produced by appropriate invocation but contains no evidence of an explicit skill-level trigger statement. |
| c2 | Skill specifies what sources to check (e.g. company website, LinkedIn, Crunchbase, news) | PASS | The output checked 14 distinct sources spanning: company investor relations page (investors.palantir.com), official company website (palantir.com), company blog (blog.palantir.com), Wikipedia, financial news (CNBC, Bloomberg, Yahoo Finance), business model analysis sites (FourWeekMBA, GrowthNavigate), executive directory (Craft.co), and a stock analysis site (TIKR). This breadth across source types strongly implies the skill specifies categories of sources to consult. |
| c3 | Skill defines an output structure with named sections (not freeform) | PASS | The output uses a consistent set of named, headed sections: Overview (with structured table), Products/services, Team (with table), Financials, Recent news (chronological), Strategic direction, Sources (numbered list), and Summary for your meeting. The uniformity and consistency of the structure across a real research task implies a template-driven skill definition. |
| c4 | Output structure includes business model or 'what they do' section | PASS | The Overview section explicitly states 'Palantir builds data integration and AI software...' and includes a structured table with 'Business model: Software-as-a-Service (SaaS) platform licensing' and 'Revenue model: Recurring subscription licenses for Gotham, Foundry, Apollo, and AIP platforms'. The Products/services section further details what each platform does. |
| c5 | Output structure includes financials or funding section | PASS | Dedicated 'Financials' section present with FY2025 total revenue ($4.48B, 56% YoY), Q4 2025 revenue ($1.41B, 70% YoY), U.S. commercial Q4 2025 ($507M, 137% YoY), FY2026 guidance ($7.182B–$7.198B), and adjusted operating margin (57%). |
| c6 | Output structure includes recent news or developments section | PASS | Dedicated 'Recent news' section present with chronological entries: May 2026 (Q1 earnings date announcement), April 2026 (Cleveland-Cliffs deal), March 2026 (USDA $300M agreement, NVIDIA collaboration, LG CNS partnership, mortgage platform partnership). |
| c7 | Skill includes guidance on assessing source credibility or recency | PARTIAL | Sources are cited with titles and URLs and most are dated (2026 news articles), showing some recency awareness. However, sources like Wikipedia, FourWeekMBA Business Model Analysis, and the Palantir Blog post carry no date indicators and are not flagged for potential staleness or credibility concerns. No explicit credibility assessment or source quality commentary appears in the output. |
| c8 | Skill references collaboration with other agents (only relevant if plugin includes multiple agents) | SKIP | Criterion marked SKIP. |
| c9 | Skill instructs the model to surface controversies / reputational risks (surveillance, military contracts, regulatory actions) — relevant to a meeting if the user might be asked about them | PASS | Under 'Summary for your meeting', point 5 explicitly states: 'Know the risks. As a former defense/intelligence contractor, Palantir faces regulatory scrutiny. If your meeting touches on any government contracts, be aware of potential compliance or reputational sensitivities.' This directly surfaces the surveillance/military contract reputational risk relevant to the meeting context. |
| c10 | Output's structure has named sections — Overview, What They Do, Business Model, Financials, Recent Developments, Key People, Sources — not freeform prose | PASS | The output contains named sections covering all required topic areas: 'Overview' (exact match), 'Products/services' (covers What They Do), business model content embedded in Overview table, 'Financials' (exact match), 'Recent news' (covers Recent Developments), 'Team' (covers Key People), 'Sources' (exact match). Output is entirely section-based with tables and bullet points — no freeform prose blocks. |
| c11 | Skill flags any source >12 months old as potentially stale, with tighter thresholds for fast-moving sectors | FAIL | No staleness flags appear anywhere in the output. Sources without explicit dates — Wikipedia, 'FourWeekMBA Business Model Analysis', 'Palantir Blog Explanation', and 'Palantir IR Financials' page — are cited without any staleness warning. The output cites 14 sources without a single recency caveat, suggesting the skill does not implement staleness-flagging behaviour. |
| c12 | Skill instructs the model to surface meeting-prep angles — likely conversation topics, strategic shifts, executive statements, known sensitivities — not just facts | PASS | Within 'Strategic direction', a subsection 'Likely conversation topics for your meeting' lists five specific angles (Bootcamp model, AIP competitive positioning, government vs commercial mix, edge technology, NVIDIA integration economics). The full 'Summary for your meeting' section then provides five numbered talking points framing facts as meeting angles, including known sensitivities ('regulatory scrutiny', 'reputational sensitivities'). |

### Notes

The output is a well-structured, information-rich company brief that satisfies most of the quality criteria. It excels at output structure (clearly named sections, tables, chronological news), financial detail, recent developments, and meeting-prep framing including reputational risk surfacing. Two criteria fail: c1 (trigger definition) cannot be inferred from the output alone since no skill-level trigger is visible in the response, and c11 (staleness flagging) is absent — sources without explicit dates (Wikipedia, FourWeekMBA, Palantir Blog) are cited without recency caveats. The partial score on c7 reflects that while sources carry dates in most cases, no explicit credibility assessment or staleness guidance is demonstrated. Overall the output functions well as a pre-meeting brief despite these gaps.
