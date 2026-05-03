# Competitive Analysis

Scenario: Testing whether the competitive-analysis skill defines a competitive set with all 5 types, produces a comparison table, and identifies strategic opportunities — not just a feature comparison.

## Prompt

> /gtm:competitive-analysis for Clearpath in the project management space — we need to understand our competitive position before repositioning for the mid-market.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I have the research I need. Let me compile the full competitive analysis now.

---

> **DRAFT — requires human review**
> *Competitive intelligence must be verified by a human before use in strategy decisions or sales materials.*

---

> **Important caveat:** Clearpath does not appear in public search results as a named project management SaaS product. This analysis researches the competitive landscape thoroughly; all **[CLEARPATH DATA NEEDED]** cells must be completed by the team before this document is used in strategy or sales contexts. Everything about competitors is sourced from public data as of May 2026.

---

# Competitive Analysis: Clearpath — Project Management (Mid-Market)

*Prepared: May 1, 2026*

---

## 1. Executive Summary

The project management software market is worth ~$11B in 2026, growing at 15% CAGR, with the top five players (Microsoft, Atlassian, Asana, Monday.com, Smartsheet) holding ~60% share. The mid-market is the most contested segment in 2026: buyers are fleeing Microsoft Project Online's September 2026 retirement, legacy tools are too rigid, and "flexible" tools like Monday.com and ClickUp are winning on UX but losing on complexity and cost at scale. The clearest positioning white space for Clearpath is **control without bureaucracy** — enterprise-grade visibility and governance with mid-market setup speed — a gap every competitor claims but none fully delivers. The biggest non-obvious competitor is the spreadsheet and the status meeting: the real question buyers are asking is not "which PM tool?" but "do we actually need dedicated PM software?"

---

## 2. Competitive Landscape Map

### Direct competitors (same product category, same target customer)
| Competitor | Notes |
|---|---|
| **Asana** | Dominant mid-market PM tool; strong on reliability and structured task workflows |
| **Monday.com** | Visual, flexible work management platform; strong UI, fragmented at scale |
| **Smartsheet** | Spreadsheet-native PM; appeals to Excel-literate ops and PMO teams |
| **Wrike** | Feature-dense mid-market and enterprise tool; strong approvals and reporting |
| **ClickUp** | Feature-broadest competitor; aggressive pricing but steep complexity curve |

### Indirect competitors (different category, same problem)
| Competitor | Notes |
|---|---|
| **Notion** | Docs + databases used as ad-hoc PM by small mid-market teams; lacks scheduling and resource management |
| **Jira (Atlassian)** | Dominates software teams; bleeds into cross-functional PM in tech-heavy mid-market orgs |
| **Airtable** | Relational database / no-code app builder used for project tracking; strong in marketing and ops |

### Substitute competitors (fundamentally different approach)
| Competitor | Notes |
|---|---|
| **Excel / Google Sheets** | The baseline every salesperson actually competes against; free, familiar, no change management required |
| **Status meetings + email** | The "process" most mid-market orgs run on; cost is invisible (lost time), not a line item |
| **Hiring a PMO person** | Orgs with resource budget often hire a coordinator before buying software |

### Potential competitors (adjacent, could enter)
| Competitor | Notes |
|---|---|
| **Linear** | Loved by engineering teams; beginning to expand scope beyond software delivery |
| **Microsoft Planner / Teams** | Already in the stack for most mid-market orgs on M365; functional ceiling is rising |
| **Salesforce (Slack + project features)** | Distribution advantage if they ship coherent PM product into Slack ecosystem |

### Customer inertia
"We've always tracked this in Sheets." Switching cost perception is the most common reason mid-market orgs stall. The PM tool budget requires a champion who can quantify time lost to manual coordination — often invisible until a project fails.

---

## 3. Competitor Profiles

---

### Asana

#### What they do
Asana is a work management platform that helps teams organise, track, and manage their work. Built around projects, tasks, and portfolios, it provides structured workflow management with reporting and cross-team visibility. Its core audience is mid-market and enterprise teams running marketing, operations, product, and cross-functional programmes.

#### Target customer
- Primary segment: Mid-market and enterprise teams (marketing, ops, PMO)
- Company size: 50–5,000 employees
- Industry focus: Horizontal (strong in tech, marketing agencies, professional services)
- Buyer persona: VP of Operations, Marketing Director, PMO Lead

#### Product
- Core capabilities: Task management, project portfolios, workload management, goals, timelines (Gantt), reporting dashboards, automation rules
- Platform: Web, mobile (iOS/Android), desktop app
- Integrations: Slack, Google Workspace, Microsoft 365, Salesforce, Zoom, Jira, 200+ others
- Technical approach: Structured project hierarchy (workspace → team → project → task → subtask); rules-based automation engine; AI prioritisation features on Advanced tier

#### Pricing *(checked May 2026)*
- Model: Per seat, billed annually
- Free tier: Personal — up to 2 users, unlimited tasks/projects (basic features only)
- Starter: $10.99/user/month (annual)
- Advanced: $24.99/user/month (annual) — primary mid-market tier; includes portfolios, goals, workload, advanced automation (25,000 actions/month), SSO
- Enterprise: Custom — includes data residency, advanced security, dedicated support

#### Strengths
1. **Reliability and UX polish** — consistently top-rated on G2 for ease of use and platform stability; low support burden post-onboarding
2. **Structured hierarchy that scales** — portfolio and goals layer gives PMO visibility across dozens of simultaneous projects; rare at this price point
3. **Brand trust** — among the first PM SaaS tools mid-market buyers think of; reduces procurement friction

#### Weaknesses
1. **Advanced tier pricing is aggressive** — at $24.99/user/month, a 50-person team is $15,000/year; buyers frequently cite sticker shock relative to ClickUp and Monday.com
2. **Limited flexibility compared to ClickUp/Monday.com** — Asana's structure works against teams with non-standard workflows; boards feel rigid; no built-in docs
3. **Free plan is functionally limited** — 2-user cap makes team evaluation difficult; prospects must commit to a paid trial before assessing real-world fit

#### Positioning
- How they describe themselves: "Work smarter and move faster with Asana AI"
- Market category they claim: Work management / AI-powered work orchestration
- Key messaging themes: Cross-team visibility, connecting work to company goals, AI that surfaces what needs attention

#### Traction signals
- Revenue: ~$800M ARR (FY2025, public company); growing ~10% YoY — slower than category average, suggesting market share pressure
- Team size: ~3,000 employees
- Notable customers: Deloitte, PayPal, Amazon, Spotify
- Growth trajectory: Stable; investing heavily in AI features to defend mid-market

---

### Monday.com

#### What they do
Monday.com is a visual work management platform built on configurable boards. Teams use it for project tracking, task management, CRM, service delivery, and workflow automation across marketing, HR, IT, sales, and operations. It differentiates on visual UX and flexibility — the same interface can be shaped for dozens of different team workflows without code.

#### Target customer
- Primary segment: SMB to mid-market; expanding enterprise
- Company size: 10–2,000 employees (sweet spot 50–500)
- Industry focus: Horizontal; particularly strong in marketing, creative, and IT
- Buyer persona: Team leads, department heads, IT administrators

#### Product
- Core capabilities: Configurable boards (Kanban, table, timeline, calendar, Gantt, map views), automation builder, dashboards, AI note-taker, integrations ecosystem, sub-items, docs
- Platform: Web, mobile (iOS/Android), desktop (Mac/Windows)
- Integrations: 200+ native integrations including Slack, Google Workspace, Salesforce, HubSpot, Jira, GitHub
- Technical approach: Column-type system on rows/boards; automation is event-trigger driven; multiple product lanes (Work Management, CRM, Dev, Service)

#### Pricing *(checked May 2026)*
- Model: Per seat, billed annually; minimum 3 seats
- Free: Up to 2 seats, limited to 1,000 items
- Basic: $9/seat/month (annual)
- Standard: $12/seat/month (annual) — adds timeline, Gantt, calendar, guest access, automations (250/month)
- Pro: $19/seat/month (annual) — adds time tracking, formula columns, private boards, automations (25,000/month)
- Enterprise: Custom — adds SSO, advanced security, multi-level permissions, audit log, tailored onboarding
- SMB average spend: ~$20,000/year; enterprise average: ~$133,000/year

#### Strengths
1. **Best-in-class UX and visual design** — consistently top-rated for ease of use on G2; new users are productive within hours vs. days for competitors
2. **Platform breadth without code** — a single team can run PM, CRM, and service workflows without switching tools; reduces software sprawl for mid-market ops
3. **AI depth across the platform** — AI note-taker, task suggestions, status summaries, and automation co-pilot included in Pro tier; not gated behind an add-on

#### Weaknesses
1. **Becomes expensive and complex at scale** — Pro plan at $19/user/month for 100 users is $22,800/year; SSO requires Enterprise (custom pricing), so security-conscious mid-market orgs pay a premium for standard features
2. **No native recurring tasks** — recurring tasks require automation workarounds; a basic gap that competitors cover natively
3. **Steep learning curve for non-obvious workflows** — the flexibility that makes Monday.com powerful also makes it easy to build a messy, unmaintainable board structure; teams without a dedicated admin often end up with fragmented setups

#### Positioning
- How they describe themselves: "The first AI-powered work OS"
- Market category they claim: Work OS / work management platform
- Key messaging themes: AI-powered automation, one platform for all work, enterprise-grade flexibility

#### Traction signals
- Revenue: ~$1.05B ARR (FY2025, public company); ~30% YoY growth — fastest among major PM vendors
- Team size: ~2,200 employees
- Notable customers: Canva, Coca-Cola, Hulu, WeWork, Philips
- Growth trajectory: Strong; expanding enterprise motion while defending SMB/mid-market core

---

### Smartsheet

#### What they do
Smartsheet is a collaborative work management platform built on a spreadsheet-like grid. It is designed for teams that manage structured processes — project plans, resource tracking, budget tracking, and portfolio reporting — and appeals strongly to PMO teams and operations leaders comfortable with Excel-style data models.

#### Target customer
- Primary segment: Mid-market and enterprise PMO, operations, IT
- Company size: 100–10,000 employees
- Industry focus: Horizontal; strong in construction, professional services, healthcare, government
- Buyer persona: PMO Director, VP Operations, IT Project Manager

#### Product
- Core capabilities: Grid, card, Gantt, and calendar views; automated workflows; dashboards; resource management; budget tracking; cross-sheet formulas; DataMesh; WorkApps builder
- Platform: Web, mobile (iOS/Android), desktop (Windows)
- Integrations: Microsoft 365, Google Workspace, Salesforce, Jira, Slack, ServiceNow, and 100+ others
- Technical approach: Spreadsheet grid as the data layer; formulas, cell-linking, and cross-sheet references for data integrity; automation builder for approvals and alerts

#### Pricing *(checked May 2026)*
- Model: Per user, billed annually; minimum 1 user (Pro) / 3 users (Business)
- Free tier: Discontinued in 2025; 30-day free trial only
- Pro: $9/user/month (annual) — basic features, limited automations
- Business: $19/user/month (annual, min 3 users) — full automation, reports, resource views, DataMesh
- Enterprise: Custom — advanced security, SSO, custom branding, Salesforce connector
- Advanced Work Management: Custom — resource management module for large programme offices
- Note: No free tier is a meaningful friction point vs. competitors

#### Strengths
1. **Spreadsheet familiarity eliminates onboarding resistance** — Excel-trained teams can import existing files and start immediately; G2 reviewers consistently cite "we were up and running same day"
2. **Formula power for data-heavy PMOs** — cross-sheet references, SUMIF/COUNTIF logic, and DataMesh give ops teams Excel-class analytics without leaving the tool
3. **Enterprise integration ecosystem** — native Salesforce, ServiceNow, and Microsoft connectors; appeals to IT and procurement where vendor certification matters

#### Weaknesses
1. **Dashboard customisation is severely limited** — no dynamic filtering on dashboards; what you build is static; users cannot drill down interactively (G2 complaint cited repeatedly across 2026 reviews)
2. **Complex setup for non-standard workflows** — advanced configurations and automation setups are described as "difficult to maintain over time" even by expert users; formula debugging is opaque
3. **No free tier since 2025** — removes low-friction trial path; competitors with free tiers (ClickUp, Monday.com, Asana) capture more bottom-up adoption

#### Positioning
- How they describe themselves: "The enterprise platform for modern work management"
- Market category they claim: Enterprise work management / collaborative work management
- Key messaging themes: Scalability, governance, Excel-like power with cloud collaboration

#### Traction signals
- Revenue: ~$1.1B ARR (FY2025, public company); growing ~17% YoY
- Team size: ~3,300 employees
- Notable customers: Pfizer, P&G, BlackRock, NASA, Cisco
- Growth trajectory: Strong enterprise motion; mid-market growth slower as ClickUp/Monday.com undercut on price and UX

---

### Wrike

#### What they do
Wrike is a collaborative work management platform targeting mid-market and enterprise teams that need structured approval workflows, real-time reporting, and resource management. It is particularly strong for marketing operations, creative production, and professional services — use cases where approval chains, proofing, and version control are critical.

#### Target customer
- Primary segment: Mid-market and enterprise; marketing ops, creative, IT, PMO
- Company size: 50–5,000 employees
- Industry focus: Marketing/creative agencies, professional services, IT departments
- Buyer persona: Marketing Operations Manager, Creative Director, IT PM

#### Product
- Core capabilities: Task management, Gantt charts, request intake forms, approval workflows, visual proofing and versioning, resource management, budget tracking, AI risk prediction, real-time reporting
- Platform: Web, mobile (iOS/Android), desktop (Mac/Windows)
- Integrations: Salesforce, Adobe Creative Cloud, Slack, Microsoft 365, Google Workspace, 400+ integrations via Wrike Integrate
- Technical approach: Hierarchical space/folder/task model; cross-tagging across folders; blueprint-based project templates; proofing layer overlaid on file attachments

#### Pricing *(checked May 2026)*
- Model: Per user, annual billing only (no monthly option at Business and above)
- Free: Up to 5 users, basic task management
- Team: $9.80/user/month (2–25 users) — unlimited projects, Gantt charts, dashboards
- Business: $24.80/user/month — adds approval workflows, request forms, resource management, project blueprints, AI risk prediction, AI Copilot (3 actions/user/month)
- Enterprise: Custom — unlimited users, SAML SSO, custom roles, advanced admin
- Pinnacle: Custom — advanced BI, locked spaces, budgeting, team performance dashboards
- Implementation budget: Expect $10,000–$30,000 in professional services for mid-market deployment on top of licence fees

#### Strengths
1. **Best-in-class approval workflows and proofing** — visual mark-up on image, video, PDF, and design files with version comparison; niche-defining for creative and agency teams; no equivalent in Asana or ClickUp at the same depth
2. **Analyst-leading project planning scores** — rated 97/100 for project planning and scheduling by SelectHub; Gantt, dependencies, and critical path analysis are genuinely deep
3. **AI included across all plans** — AI features are not a separate add-on; AI risk prediction (Business tier) flags timeline risk before it becomes a miss

#### Weaknesses
1. **Price jump from Team to Business is steep** — from $9.80 to $24.80/user/month to unlock approval workflows; a 100-person deployment at Business tier is $29,760/year before implementation costs
2. **Annual-only billing at Business tier** — no monthly option; mid-market buyers trying the product before committing face a hard cliff
3. **Implementation complexity** — multiple reviewers note 4–12% of total first-year cost goes to professional services; budget overruns are common; the product requires significant configuration before teams are productive

#### Positioning
- How they describe themselves: "The only platform purpose-built for marketing and creative teams"
- Market category they claim: Work management / marketing work management
- Key messaging themes: Approval workflows, creative operations, marketing velocity

#### Traction signals
- Revenue: Unknown — private company (acquired by Citrix, then Vista Equity Partners in 2023)
- Team size: ~1,000 employees
- Notable customers: Google, Walmart, Siemens, Ogilvy, Hootsuite
- Growth trajectory: Stable; carving a niche in marketing/creative ops while larger peers compete on breadth

---

### ClickUp

#### What they do
ClickUp is a broad productivity and project management platform that packs task management, docs, goals, whiteboards, time tracking, basic CRM, and chat into a single product. It targets teams frustrated by "too many tools" and positions itself as the single replacement for multiple SaaS subscriptions. Its pricing is aggressively below Asana and Wrike at comparable feature depth.

#### Target customer
- Primary segment: SMB to mid-market teams; particularly tech, agencies, and remote-first orgs
- Company size: 5–500 employees
- Industry focus: Horizontal; strong in software, creative agencies, consulting
- Buyer persona: Team leads, startup operators, individual contributors who drive bottom-up adoption

#### Product
- Core capabilities: Tasks with custom fields, Docs (built-in wiki), Goals, Whiteboards, Mind Maps, Dashboards, Time Tracking, Automations (100+ triggers), Forms, Chat
- Platform: Web, mobile (iOS/Android), desktop (Mac/Windows/Linux), Chrome extension
- Integrations: Slack, GitHub, GitLab, Figma, Google Drive, Zoom, Salesforce, and 1,000+ via Zapier
- Technical approach: Hierarchical workspace/space/folder/list/task model; ClickApps system lets admins enable/disable features per space; most customisable architecture in the segment

#### Pricing *(checked May 2026)*
- Model: Per user, billed annually; significant annual discount vs. monthly
- Free: Unlimited users, 100MB storage, limited features
- Unlimited: $7/user/month (annual) — unlimited storage, integrations, Gantt, dashboards, guests
- Business: $12/user/month (annual) — adds advanced automations (5,000/month), workload management, Google SSO, time tracking reports
- Enterprise: Custom — advanced permissions, SSO, unlimited custom roles, MSA, dedicated support
- AI Add-on: $9–$28/user/month (not included in base plans) — adds AI drafting, summaries, auto-subtasks; erodes pricing advantage

#### Strengths
1. **Best value-to-feature ratio in the segment** — Business at $12/user/month includes automations, time tracking, and workload that competitors charge $20–$25 for; meaningful for cost-conscious mid-market buyers
2. **Feature density as a migration accelerator** — built-in Docs eliminates Notion/Confluence for many teams; Whiteboards replace Miro for lightweight use; genuinely reduces SaaS stack for mid-market orgs
3. **Bottom-up adoption engine** — free tier with unlimited users drives individual and team adoption that converts upward; 4.7/5 on G2 from 9,500+ reviews as of 2026

#### Weaknesses
1. **Complexity is its biggest retention risk** — described by multiple 2026 reviewers as "overwhelming for new users"; the breadth that attracts buyers also drives abandonment in teams without a dedicated ClickUp admin
2. **AI is a paid add-on, not included** — AI Standard ($9/user/month) or AI Max ($28/user/month) on top of base plan; a Business + AI Standard plan is $21/user/month — comparable to Asana Advanced without the reliability advantage
3. **Performance under load** — documented complaints of slow load times, especially on dashboards and large spaces; less reliable than Asana at scale

#### Positioning
- How they describe themselves: "One app to replace them all"
- Market category they claim: Productivity platform / everything app
- Key messaging themes: Replace multiple tools, best value, customisable to any workflow

#### Traction signals
- Revenue: ~$250M ARR (2025 estimates, private company)
- Team size: ~1,200 employees
- Notable customers: Unknown — private company with limited published logos
- Growth trajectory: Strong; fastest organic growth in the segment by seat count

---

### Non-obvious competitors

**Excel / Google Sheets** — The spreadsheet is the real incumbent in mid-market project management. It is free (or already paid), requires no IT approval, and every employee knows how to use it. The status quo is: one shared sheet per project, owned by whoever set it up, with colour-coded cells for status and weekly manual updates. Its weaknesses are non-obvious to the buyer: no single source of truth, no automatic dependencies, no resource visibility. Clearpath's pitch must make these costs visible — the spreadsheet never sends itself an alert when a deadline is missed.

**Microsoft Planner (via M365)** — Most mid-market organisations already pay for Microsoft 365. Planner is included. Teams are using it. It is not powerful, but it is free, already approved by IT, and does not require a procurement cycle. With Project Online retiring in September 2026 and Microsoft pushing Teams + Planner as the replacement, this is an intensifying threat for smaller mid-market buyers. Its ceiling is its limitation — no resource management, no portfolio view, no real Gantt.

---

## 4. Comparison Table

*[CLEARPATH DATA NEEDED] cells require the Clearpath team to fill in from internal product data.*

| Dimension | Clearpath | Asana (Advanced) | Monday.com (Pro) | Smartsheet (Business) | Wrike (Business) | ClickUp (Business) | Excel / Sheets |
|---|---|---|---|---|---|---|---|
| **Task management depth** | [CLEARPATH DATA NEEDED] | Deep — subtasks, dependencies, custom fields | Deep — custom columns, sub-items | Deep — cross-sheet linking, formulas | Deep — cross-tagging, blueprints | Very deep — most customisable | Basic — manual, no automation |
| **Portfolio / programme visibility** | [CLEARPATH DATA NEEDED] | Yes — Portfolios + Goals layer | Yes — via dashboards | Yes — via cross-sheet reports | Yes — reporting dashboards | Yes — via Dashboards + Goals | No — manual aggregation only |
| **Resource management** | [CLEARPATH DATA NEEDED] | Yes (Workload view) — Advanced tier | Limited — no native resource capacity | Yes (Resource views) — Business tier | Yes — full resource management | Yes — Workload view (Business) | No |
| **Approval workflows** | [CLEARPATH DATA NEEDED] | Basic — approval tasks | Basic — approval columns | Basic — approval automations | Deep — multi-stage approvals, proofing | Moderate — approval automations | No |
| **AI features** | [CLEARPATH DATA NEEDED] | Included in Advanced | Included in Pro | Not listed as core (Add-on) | Included (Business — 3 acts/user/mo) | Add-on: +$9–28/user/mo | No |
| **Setup time** | [CLEARPATH DATA NEEDED] | Medium — 1–3 days for structured rollout | Fast — 1 day for simple use, weeks for complex | Fast — Excel import same-day | Slow — 4–12% of annual cost in services | Medium — templates speed onboarding | Immediate — already in use |
| **Pricing: entry (10 users, annual)** | [CLEARPATH DATA NEEDED] | $1,319/year (Starter) | $1,440/year (Standard) | $1,080/year (Pro) | $1,176/year (Team) | $840/year (Unlimited) | $0 (already paid) |
| **Pricing: mid-market (50 users, annual)** | [CLEARPATH DATA NEEDED] | $14,994/year (Advanced) | $11,400/year (Pro) | $11,400/year (Business) | $14,880/year (Business) | $7,200/year (Business) | $0 |
| **Free tier** | [CLEARPATH DATA NEEDED] | 2 users, limited | 2 seats, 1,000 items | None (30-day trial) | 5 users, basic | Unlimited users, limited | Always free |
| **Integration depth** | [CLEARPATH DATA NEEDED] | 200+ — strong M365/Google/Salesforce | 200+ — strong across categories | 100+ — best Microsoft + Jira | 400+ — deepest library | 1,000+ (many via Zapier) | Manual (export/import) |
| **Reporting / dashboards** | [CLEARPATH DATA NEEDED] | Strong — cross-project portfolio dashboards | Strong — visual, shareable | Limited — no dynamic filtering (key weakness) | Strong — real-time, executive dashboards | Strong — custom dashboards | Manual — pivot tables |
| **Built-in docs/knowledge base** | [CLEARPATH DATA NEEDED] | No native docs | Yes (monday Docs) | No | No | Yes (ClickUp Docs) | No |
| **Mobile experience** | [CLEARPATH DATA NEEDED] | Good (iOS/Android) | Good (iOS/Android) | Moderate | Good (iOS/Android) | Good (iOS/Android) | Poor |
| **Change management burden** | [CLEARPATH DATA NEEDED] | Low–medium | Low–medium | Medium (formula complexity) | High (configuration-heavy) | High (can overwhelm teams) | None — zero change required |

---

## 5. Differentiation Analysis

*Note: "Where we win/lose" rows are directional until Clearpath's product capabilities are confirmed. All competitor-side claims are sourced.*

---

#### vs. Asana

**Where we win:**
- [CLEARPATH DATA NEEDED — fill in specific capability, speed, pricing, or workflow advantages with evidence]

**Where we lose:**
- Brand recognition: Asana is top-of-mind in mid-market PM procurement; Clearpath is not (no public presence found)
- Enterprise trust signals: Asana has Deloitte, PayPal, Spotify as logos; mid-market buyers use these as proxy validators
- Integration breadth: Asana's 200+ native integrations create stickiness; any gap in Clearpath's integration list is a deal-stopper for tech-stack buyers

**Where it's a wash:**
- [CLEARPATH DATA NEEDED — features at parity]

**Their likely counter-positioning:**
"Clearpath is unproven — why risk your team's workflow on a product without Asana's track record? We have thousands of teams in your industry."

**Best counter-argument:**
"Asana's reliability comes with rigidity. At $24.99/user/month, you're paying for structure that slows you down. We give you [specific advantage] in [specific workflow] without the enterprise overhead."

---

#### vs. Monday.com

**Where we win:**
- [CLEARPATH DATA NEEDED]

**Where we lose:**
- UX polish: Monday.com sets the visual bar; any friction in Clearpath's interface will be noticed immediately in side-by-side demos
- Platform breadth: Monday.com's CRM, service, and dev modules mean a mid-market buyer can replace 3–4 tools; Clearpath must compete with a narrower feature set unless it matches this
- Growth and stability signals: $1B ARR and 30% growth is a powerful "we'll be here in 5 years" signal to IT procurement

**Where it's a wash:**
- [CLEARPATH DATA NEEDED]

**Their likely counter-positioning:**
"Monday.com is the future of work. Clearpath is a niche tool — you'll outgrow it."

**Best counter-argument:**
"Monday.com's flexibility is a trap — it takes weeks to set up correctly and months to maintain properly. We're purpose-built for [specific Clearpath use case] and your team will be productive in [X hours/days]."

---

#### vs. Smartsheet

**Where we win:**
- Dashboard interactivity: Smartsheet's static dashboards with no dynamic filtering is a documented weakness with real buyer frustration; if Clearpath's dashboards allow drill-down and live filtering, this is a genuine differentiator
- Free trial path: Smartsheet killed its free plan in 2025; any free trial or freemium offer from Clearpath lowers buyer friction significantly
- [CLEARPATH DATA NEEDED — other specific advantages]

**Where we lose:**
- Spreadsheet-native buyers: Teams running on Excel will import directly into Smartsheet on day one; Clearpath must earn that migration
- PMO credibility: Smartsheet is entrenched in formal programme offices; its formula and cross-sheet linking capabilities meet needs that PM tools typically cannot

**Where it's a wash:**
- [CLEARPATH DATA NEEDED]

**Their likely counter-positioning:**
"Smartsheet has enterprise PMO capabilities and proven integrations with your Microsoft and Salesforce stack. Clearpath is unverified."

**Best counter-argument:**
"Smartsheet's dashboard limitations [no dynamic filtering] mean your execs are looking at stale data. We give you [live drill-down/filtering capability] without a 45-minute setup formula every time you add a column."

---

#### vs. Wrike

**Where we win:**
- Implementation speed: Wrike's professional services overhead ($10–30K for mid-market deployments) is a known friction point; if Clearpath deploys faster with less services cost, this is a direct and quantifiable advantage
- Pricing continuity: Wrike's Team-to-Business price jump ($9.80 → $24.80) is steep; a linear pricing curve from Clearpath removes a common objection
- [CLEARPATH DATA NEEDED]

**Where we lose:**
- Approval and proofing depth: Wrike's multi-stage approval workflows and visual proofing are industry-leading for creative/marketing teams; if Clearpath doesn't match this, it loses those verticals
- Analyst scores: Wrike's 97/100 project planning rating is a useful procurement shortcut for formal RFP processes

**Where it's a wash:**
- [CLEARPATH DATA NEEDED]

**Their likely counter-positioning:**
"Wrike is purpose-built for enterprise-grade project management. Clearpath doesn't have the depth or the approval workflows we need."

**Best counter-argument:**
"Wrike's implementation costs can reach 12% of your first-year licence cost before you're live. We deploy in [X days], included in the licence, with no professional services surcharge."

---

#### vs. ClickUp

**Where we win:**
- Simplicity and reliability at scale: ClickUp's documented performance issues and overwhelming complexity are the most common churn reason; if Clearpath is more reliable and easier to govern, this is a real advantage
- AI included in base price: ClickUp charges $9–28/user/month for AI on top of base plans; if Clearpath includes AI, it closes this pricing gap significantly
- [CLEARPATH DATA NEEDED]

**Where we lose:**
- Feature breadth: ClickUp's "one app to replace them all" appeal is hard to match without matching its docs, whiteboards, CRM, and chat scope
- Price floor: ClickUp's Unlimited plan at $7/user/month for 50 users is $4,200/year — very hard to beat on cost alone
- G2 reviews volume: 9,500+ G2 reviews is a social proof signal that new entrants cannot easily close

**Where it's a wash:**
- [CLEARPATH DATA NEEDED]

**Their likely counter-positioning:**
"ClickUp does everything Clearpath does and more, at a lower price."

**Best counter-argument:**
"ClickUp's 'one app for everything' means your team gets lost in options. We're focused — your team will run their first project in [X minutes], not after a two-day configuration sprint."

---

#### vs. Excel / Google Sheets (the real incumbent)

**Where we win:**
- Automatic dependency alerts and deadline tracking
- Real-time visibility across multiple projects without manual consolidation
- Audit trail and permission control for project artefacts
- Resource utilisation across the portfolio — invisible in a spreadsheet until someone burns out or misses a deadline

**Where we lose:**
- Cost: zero vs. [CLEARPATH DATA NEEDED] per user per month
- Familiarity: no change management required; every stakeholder already knows how to open a spreadsheet
- Flexibility for one-off uses: a quick tracker in Sheets beats logging into PM software for a 2-week project

**The decisive counter-argument:**
Make the invisible cost visible. A team of 20 spending 3 hours/week on manual status updates = 60 person-hours/week = ~$6,000/month at $50/hour fully loaded. The spreadsheet is not free.

---

## 6. Strategic Opportunities

### Underserved segments

| Segment | Why underserved | How to win them | Confidence |
|---|---|---|---|
| **Microsoft Project Online refugees** | Project Online retires September 2026; Microsoft's replacement (Planner + Teams) has a low feature ceiling; displaced PMO teams need a structured migration path fast | Offer a "Project Online migration in 30 days" programme with templates and import tooling; position as the modern upgrade, not a step down | High — deadline-driven urgency |
| **Mid-market ops teams in professional services** | Most PM tools target tech or marketing; professional services (consulting, architecture, law) need client-facing project tracking, milestone billing tie-ins, and external stakeholder access | Build a professional services workflow template with client portal features and billing milestone tracking | Medium |
| **Teams stuck between Trello and enterprise tools** | Trello is too simple at 50+ people; Jira and Wrike are too complex; the gap between $5/user casual tools and $25/user enterprise tools is real and underserved | Position Clearpath as "the PM tool for teams that have outgrown Trello and don't need Jira" | High — this is the stated mid-market gap |
| **Orgs replacing stale spreadsheet-based PMOs** | Finance, HR, and operations departments still running shared Google Sheets for project tracking; want structure without the PM software learning curve | Lead with "your team knows it in a day" and offer Sheets import + migration playbooks | Medium |

---

### Feature gaps in the market

| Gap | Who needs it | Which competitors could fill it | Priority |
|---|---|---|---|
| **Dynamic dashboard filtering** | PMO leads and execs who need to drill into live project data without rebuilding reports | Smartsheet (their specific weakness) | High |
| **Transparent pricing at scale** | Mid-market IT and procurement — total cost is unpredictable across most platforms (add-ons, implementation, enterprise gates) | All — none do this well | High |
| **Fast self-serve onboarding** | Small PMO teams without a dedicated admin who need to go live in hours, not days | Wrike and ClickUp both struggle here | High |
| **Client-facing project portals** | Professional services and agencies sharing project status with clients | No major PM tool does this natively without add-ons | Medium |
| **AI included, not add-on** | Any team that wants AI benefits without surprise invoices | ClickUp (charges extra), Wrike (limited quota) | Medium |

---

### Positioning white space

**Price point gap:** There is a gap between ClickUp's $7/user "feature-dense but chaotic" positioning and Asana's $24.99/user "reliable but rigid and expensive" positioning. Monday.com's Pro at $19/user is in this range but optimised for visual flexibility, not governance. A product that delivers **structured mid-market PM with enterprise-grade reporting at $12–16/user/month** with no implementation tax sits in real white space.

**Approach gap:** Every major competitor claims "easy to set up" but delivers complexity at scale. There is white space for a PM tool that is genuinely opinionated — one that enforces a workflow model that works for mid-market programmes without requiring a dedicated admin to maintain it.

**Audience gap:** Microsoft Project Online refugees are a time-limited, high-intent segment in 2026. No competitor is running a dedicated migration campaign. First mover in this segment with a credible migration offer captures high-LTV PMO buyers in a narrow window.

---

### Competitive threats

| Threat | Source | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| Monday.com price compression | Monday.com — running aggressive mid-market promotions; $19 Pro tier is already competitive | High | High | Compete on setup speed and governance depth, not price |
| ClickUp adds reliability / performance fixes | ClickUp — well-resourced, actively addressing performance issues | Medium | High | Build reliability reputation before ClickUp closes the gap |
| Microsoft Planner ceiling rises | Microsoft — regularly releasing Planner features within M365 licence already paid | High | Medium | Focus on buyers where M365 Planner is "not enough but already installed" — show the ceiling clearly |
| Asana drops Advanced pricing | Asana — under revenue growth pressure, may lower pricing to defend mid-market | Low | High | Ensure differentiation is not purely price-based |
| Wrike improves self-serve onboarding | Wrike (Vista Equity) — private equity owner incentivised to reduce services dependency | Medium | Medium | Own the "fast onboarding" narrative aggressively with proof points before they close the gap |

---

## 7. Recommended Actions

### 1. Launch a "Project Online Migration" programme immediately

**What:** Build a structured migration offer targeting teams displaced by Microsoft Project Online's September 2026 retirement. Package this as a named programme with import tooling, templates replicating common Project Online structures, and a "live in 30 days" SLA.

**Why:** Project Online retirement is a deadline-driven displacement event affecting thousands of mid-market PMO teams. No major competitor is running a dedicated capture programme. The window is narrow — September 2026 — and buyers are actively searching right now.

**Timeline:** Now — this window closes by September 2026.

**Expected impact:** High-intent PMO buyer acquisition with long LTV; establishes Clearpath as the credible upgrade path from legacy Microsoft tooling.

---

### 2. Make pricing legible and all-in at mid-market scale

**What:** Publish a clear, all-inclusive price per user for a 50-person mid-market team. Include AI, onboarding, and standard support in the published price. Do not gate SSO or reporting behind a custom-pricing tier unless there is a compelling reason.

**Why:** Every major competitor (Asana, Wrike, ClickUp with AI) has unpredictable total cost of ownership at mid-market scale. This is a documented frustration in buyer reviews across G2 and Capterra. Legible pricing is itself a differentiator — IT and finance buyers at mid-market companies do not have the procurement bandwidth for complex enterprise negotiations.

**Timeline:** Next quarter — before new sales motion is built around the mid-market repositioning.

**Expected impact:** Reduced sales cycle friction; opens deals where procurement rejected opaque vendors; differentiates in RFP processes where competitors cannot publish comparable numbers.

---

### 3. Build a "day-one value" story with a measurable onboarding benchmark

**What:** Define and test a specific, verifiable claim about how fast a new team is productive in Clearpath — e.g., "first project tracked in under 20 minutes with no training." Instrument the product to measure time-to-first-project. Use real customers to validate the number and publish it.

**Why:** ClickUp and Wrike's biggest weaknesses are complexity and implementation overhead. Asana's free plan caps at 2 users. The mid-market sweet spot is buyers who want to try before they commit and be productive without a consultant. A specific, verifiable onboarding benchmark beats any marketing claim and is a direct weapon against ClickUp's complexity reputation and Wrike's implementation cost story.

**Timeline:** Next quarter — instrument, measure, and validate with 5–10 early mid-market customers.

**Expected impact:** Reduces buyer risk perception; accelerates free-trial-to-paid conversion; gives sales a concrete differentiator with evidence.

---

> **DRAFT — requires human review**
> *All competitor pricing and feature data reflects publicly available information as of May 1, 2026. Clearpath-specific cells marked [CLEARPATH DATA NEEDED] must be completed by the internal team before this analysis is used in sales or strategy contexts. Verify competitor pricing at source before any outbound use — pricing changes frequently.*

---

**Sources:**
- [G2 — Smartsheet Reviews 2026](https://www.g2.com/products/smartsheet/reviews)
- [G2 — ClickUp Reviews 2026](https://www.g2.com/products/clickup/reviews)
- [Asana Pricing](https://asana.com/pricing)
- [Smartsheet Pricing](https://www.smartsheet.com/pricing)
- [monday.com Pricing](https://monday.com/pricing)
- [Wrike Review 2026 — SelectHub](https://www.selecthub.com/p/project-management-software/wrike/)
- [Smartsheet vs Asana vs monday.com — UC Today 2026](https://www.uctoday.com/project-management/monday-com-vs-asana-vs-smartsheet-which-ai-strategy-will-win-enterprise-in-2026/)
- [Asana vs monday.com 2026 — Tech.co](https://tech.co/project-management-software/asana-vs-monday)
- [ClickUp Pricing 2026 — Tech.co](https://tech.co/project-management-software/clickup-pricing)
- [Microsoft Project Online retirement — UC Today](https://www.uctoday.com/project-management/the-great-microsoft-project-migration-and-why-the-april-2026-deadline-changes-everything/)
- [Wrike Pricing 2026 — SaaSworthy](https://www.saasworthy.com/blog/wrike-pricing-plans)
- [Project Management Market Report — Mordor Intelligence](https://www.mordorintelligence.com/industry-reports/project-management-software-systems-market)
- [Best PM Software 2026 — Workzone](https://www.workzone.com/blog/best-project-management-software-2026/)
- [Smartsheet Review 2026 — SmartSuite](https://www.smartsuite.com/blog/smartsheet-review)
- [monday.com Review 2026 — G2](https://learn.g2.com/monday-review)

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.5/17.0 (91%) |
| Evaluated | 2026-05-01 |
| Target duration | 342661 ms |
| Target cost | $0.8981 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill defines the competitive set using all 5 types: direct competitors, indirect competitors, do-nothing/status-quo, emerging threats, and adjacent tools | PASS | Section 2 'Competitive Landscape Map' explicitly structures into: Direct (Asana, Monday.com, Smartsheet, Wrike, ClickUp), Indirect (Notion, Jira, Airtable), Substitute/status-quo (Excel/Google Sheets, Status meetings + email, Hiring a PMO person), Potential/emerging (Linear, Microsoft Planner/Teams, Salesforce). All 5 conceptual types are represented, even if labeled slightly differently. |
| c2 | Skill requires a research step for each competitor — not writing analysis from assumptions | PASS | Output opens with 'I have the research I need' and closes with 15 sourced URLs (G2, pricing pages, SelectHub, Tech.co, SaaSworthy). Pricing data is noted as 'checked May 2026', revenue figures cite 'FY2025, public company', and specific claims like Wrike's '97/100 project planning rating' are attributed to SelectHub. |
| c3 | Skill produces a comparison table covering key dimensions — not a prose description of each competitor | PASS | Section 4 'Comparison Table' is a structured matrix with 14 dimensions (task management depth, portfolio visibility, resource management, approval workflows, AI features, setup time, pricing at two scales, free tier, integration depth, reporting/dashboards, built-in docs, mobile experience, change management burden) and one column per competitor including Excel/Sheets. |
| c4 | Skill produces a differentiation analysis — what Clearpath does differently, not just a feature checklist | PASS | Section 5 'Differentiation Analysis' has a structured win/lose/wash/counter-positioning/counter-argument format for each of 6 competitor matchups. It goes beyond feature lists — e.g., vs. Wrike: 'Implementation speed: Wrike's professional services overhead ($10–30K for mid-market deployments) is a known friction point'; vs. Smartsheet: 'Dashboard interactivity: Smartsheet's static dashboards with no dynamic filtering is a documented weakness.' [CLEARPATH DATA NEEDED] placeholders are correctly used where Clearpath's actual capabilities are unknown. |
| c5 | Skill identifies strategic opportunities based on competitive gaps — where competitors are weak or where the market is underserved | PASS | Section 6 has four subsections: Underserved segments (4 named segments tied to specific competitor gaps), Feature gaps in the market (5 gaps mapped to specific competitor weaknesses like Smartsheet's static dashboards), Positioning white space (price gap between $7 ClickUp and $24.99 Asana), and Competitive threats (5 threats with likelihood/impact ratings). |
| c6 | Skill distinguishes between features that are parity (must-have, table stakes) and differentiators (reasons to choose) — partial credit if differentiation is covered but parity/differentiator distinction is not explicit | PARTIAL | The differentiation analysis covers win/lose/wash per competitor and the comparison table maps feature coverage, but neither section explicitly labels features as 'table stakes' vs. 'differentiators.' The concept is implicitly present (e.g., 'Where it's a wash' implies parity) but never named or listed as such. |
| c7 | Skill produces output that informs positioning decisions — not just an intelligence briefing | PASS | Section 7 'Recommended Actions' gives 3 concrete positioning actions: (1) Launch a 'Project Online Migration' programme with timeline and expected impact; (2) make pricing legible and all-in; (3) build a day-one value story with a measurable onboarding benchmark. Section 6 'Positioning white space' explicitly identifies the $12–16/user/month gap and the 'control without bureaucracy' positioning territory. |
| c8 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The captured output is the skill's execution result — a markdown competitive analysis. No YAML frontmatter is visible anywhere in the output. The skill definition file cannot be verified from the captured output alone. |
| c9 | Output's competitive set covers all 5 types — direct (Asana, Monday.com, ClickUp), indirect (Jira, Trello), status quo (spreadsheets + email), emerging threats (AI-native PM tools like Notion AI, Reclaim), adjacent (Slack-as-PM, GitHub Projects) — with at least 1-2 examples per type | PASS | All 5 types have 1+ examples: Direct — Asana, Monday.com, ClickUp, Smartsheet, Wrike ✓; Indirect — Jira, Notion, Airtable ✓ (Trello absent but adequate substitutes); Status quo — Excel/Google Sheets, Status meetings + email ✓; Emerging — Linear, Microsoft Planner, Salesforce ✓ (not Notion AI/Reclaim specifically, but the type is covered); Adjacent — Microsoft Planner via Teams, Salesforce Slack-as-PM ✓ (GitHub Projects absent). The criterion's 1-2 examples per type threshold is met for all categories. |
| c10 | Output's research notes per competitor cite sources — not just generic 'Asana is mature' but 'Asana 2024 ARR ~$650M (10-K), 60% mid-market ICP per their investor day' with the source named | PASS | Revenue figures specify filing period and public/private status ('~$800M ARR (FY2025, public company)' for Asana; '~$1.05B ARR (FY2025, public company)' for Monday.com). Specific claims are sourced: Wrike's '97/100 project planning' attributed to SelectHub. Pricing noted 'checked May 2026' with 15 URLs in the sources section covering G2, pricing pages, Tech.co, and industry reports. |
| c11 | Output's comparison table has structured dimensions — pricing, target segment, key features, differentiator, weakness — with one row per competitor and verifiable cell content | PASS | Section 4 table has 7 competitor columns and 14 dimension rows. Cells contain specific, verifiable content: e.g., 'Pricing: mid-market (50 users)' shows '$14,994/year (Advanced)' for Asana, '$7,200/year (Business)' for ClickUp, '$0' for Excel. Feature descriptions are concrete rather than generic ('No — manual aggregation only' for Excel portfolio visibility). Clearpath column uses [CLEARPATH DATA NEEDED] appropriately. |
| c12 | Output's differentiation analysis names what Clearpath does that competitors don't — concrete (e.g. 'real-time RAG dashboards across the portfolio'), not vague ('better UX' or 'more flexible') | PARTIAL | The 'Where we win' sections are largely [CLEARPATH DATA NEEDED] placeholders. Where conditional claims are made they are specific (e.g., 'if Clearpath's dashboards allow drill-down and live filtering, this is a genuine differentiator' vs. Smartsheet; 'if Clearpath deploys faster with less services cost' vs. Wrike) but remain hypothetical rather than concrete named capabilities. The output correctly flags this as a gap requiring the team to fill in product data. |
| c13 | Output's strategic opportunities are tied to specific competitive gaps — e.g. 'Monday/Asana mid-market reporting falls short on executive summaries → Clearpath Analytics enters here' rather than generic market-size assertions | PASS | Feature gaps table explicitly ties each gap to specific competitor weaknesses: 'Dynamic dashboard filtering → Smartsheet (their specific weakness)'; 'Fast self-serve onboarding → Wrike and ClickUp both struggle here'. The Microsoft Project Online refugee segment is tied to a concrete deadline ('September 2026 retirement') not a generic market-size claim. Positioning white space cites specific price points ($7 ClickUp vs. $24.99 Asana) rather than abstract assertions. |
| c14 | Output distinguishes table-stakes features (parity required to compete) from differentiators (reasons to choose) — at least 3 of each, named | FAIL | No section of the output explicitly labels features as 'table stakes' or 'must-have parity features' with a named list. The 'Where it's a wash' rows in the differentiation analysis use [CLEARPATH DATA NEEDED] placeholders. The closest approximation is the implicit framing in the comparison table but no named categorisation of parity vs. differentiator features appears anywhere in the output. |
| c15 | Output's analysis informs the mid-market repositioning decision the prompt asks about — concluding which segments are most defensible, which competitors are most threatening, and what positioning shifts the team should make | PASS | Section 6 rates segment confidence ('High' for Project Online refugees, 'High' for Trello-to-enterprise gap, 'Medium' for others). Section 6 competitive threats rank Monday.com and Microsoft Planner as 'High' likelihood threats. Section 7 translates analysis into 3 specific positioning shifts with timelines and expected impact. Executive Summary identifies 'control without bureaucracy' as the positioning white space. |
| c16 | Output addresses status-quo / do-nothing as a competitor — many mid-market teams still run on spreadsheets + Slack + email, and the 'buy nothing' decision is the most common loss | PASS | The 'Substitute competitors' section explicitly names Excel/Google Sheets, 'Status meetings + email', and 'Hiring a PMO person.' The vs. Excel section has a dedicated full analysis including the counter-argument: 'Make the invisible cost visible. A team of 20 spending 3 hours/week on manual status updates = 60 person-hours/week = ~$6,000/month.' The Executive Summary also flags 'the spreadsheet and the status meeting' as the real question buyers are asking. |
| c17 | Output identifies the buying centre's likely competitive consideration — operations directors / PMOs evaluate against Asana / Monday because those are the in-house standards, not against newer entrants they haven't heard of | PASS | vs. Asana 'Where we lose' states: 'Brand recognition: Asana is top-of-mind in mid-market PM procurement; Clearpath is not (no public presence found)' and 'Enterprise trust signals: Asana has Deloitte, PayPal, Spotify as logos; mid-market buyers use these as proxy validators.' Asana strengths section notes 'reduces procurement friction.' This directly identifies that the buying centre benchmarks against Asana/Monday as the in-house standard, and that Clearpath is not yet in that consideration set. |
| c18 | Output addresses pricing power within the competitive set — Clearpath's $15/seat analytics add-on positioning relative to Monday's tiered pricing or Asana's reporting included in higher tiers | PARTIAL | The output includes a detailed pricing comparison across competitors at two scales (10 users and 50 users) and identifies the price gap between ClickUp ($7) and Asana ($24.99). Positioning white space names '$12–16/user/month' as the defensible price point. However, Clearpath's column is [CLEARPATH DATA NEEDED] throughout, so no specific analytics add-on pricing or Clearpath's pricing power is addressed. The competitor pricing analysis is complete; Clearpath's relative positioning is not. |

### Notes

The output is a high-quality competitive analysis that correctly handles the core challenge: Clearpath is not a publicly known SaaS product, so all Clearpath-specific cells are correctly marked [CLEARPATH DATA NEEDED] rather than fabricated. The skill excels at structuring competitor research (all 5 competitive types covered), producing a verifiable comparison table, identifying specific competitive gaps, and generating actionable positioning recommendations tied to those gaps. The two clear failures are: (1) no evidence of YAML frontmatter in the skill definition (c8, cannot verify from output); (2) no explicit table-stakes vs. differentiators categorisation (c14) — the output has win/lose/wash framing but never names 3+ features as 'parity required' vs. '3+ reasons to choose.' The differentiation analysis (c12) scores only partial because all 'Where we win' cells are placeholders — this is arguably the right behavior given an unknown product, but the criterion requires concrete named capabilities. The strongest sections are strategic opportunities (c13), status-quo competitor treatment (c16), and the recommended actions section that directly addresses the mid-market repositioning prompt.
