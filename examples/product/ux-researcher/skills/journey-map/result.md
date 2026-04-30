# Result: Journey map

**Verdict:** PASS
**Score:** 13/13 criteria met (100%)
**Evaluated:** 2026-04-30

---

## Output

Simulated output for the prompt:

> `/ux-researcher:journey-map for the customer journey from first hearing about Clearpath through to becoming an active daily user — specifically for mid-market operations directors.`

---

## Journey: Awareness to Daily Use — Mid-market Operations Director

### Scope

| Element | Definition |
|---|---|
| **User type** | Mid-market operations director (100–1,000 employees), evaluating workflow tools, typically owns operational efficiency metrics |
| **Journey** | Discovery through active daily use — full acquisition and activation arc |
| **Start point** | Operations director first encounters Clearpath (Google search result, LinkedIn ad, or peer recommendation) |
| **End point** | Uses Clearpath for portfolio reporting at least 5 days/week for 30+ consecutive days |
| **Success metric** | Time-to-first-value (target: under 14 days from signup to first completed report shared with a stakeholder) |

---

### Evidence Sources

| Source | What it tells us | Coverage |
|---|---|---|
| Sales call recordings | Initial objections, evaluation criteria, competitor comparisons | Awareness, Evaluation |
| Onboarding survey responses | Stated goals, role context, prior tool experience | Onboarding |
| Support tickets | Where users get stuck during setup and first use | Onboarding, First Use |
| Churn interview notes | Why users didn't reach daily use; what broke the journey | Evaluation, Trial |
| Product analytics | Drop-off rates per onboarding step, feature adoption, daily active use rates | Trial, Activation, Daily Use |
| Session recordings | Confusion patterns, ignored UI elements, unexpected navigation | Onboarding, First Use |

**Evidence gaps:** Awareness stage has no first-party analytics — peer-recommendation pathway is hypothesis. Delight moments post-activation are hypothesis pending NPS interview programme.

---

### Stage 1: Awareness

**User goal at this stage:** Understand whether Clearpath is worth a 30-minute demo
**Duration:** 1–5 days (passive research)
**Evidence basis:** Hypothesis (peer referral path); evidence-based (search/ad path via UTM data)

| Element | Detail |
|---|---|
| **Touchpoints** | Google search results, LinkedIn ads, peer Slack or email recommendation, G2 / Capterra review pages, Clearpath homepage |
| **Actions** | Searches "operational reporting tool mid-market", scans homepage, reads 2–3 G2 reviews, may ask a peer who mentioned it |
| **Thinking** | "Is this just another dashboard tool?" / "How long does this actually take to set up?" / "Will IT block this?" |
| **Feeling** | Sceptical, time-poor, mildly curious |
| **Pain points** | Homepage leads with features, not outcomes — directors can't quickly answer "what problem does this solve for me specifically?" |
| **Opportunities** | Lead homepage with the outcome (e.g. "Know exactly where every project stands — in one view, updated daily") before listing features |

**Drop-off risk:** High — most first visits leave without converting to a trial signup.

---

### Stage 2: Evaluation

**User goal at this stage:** Decide whether to commit time to a trial or demo
**Duration:** 3–10 days
**Evidence basis:** Evidence-based (sales call recordings, CRM deal notes)

| Element | Detail |
|---|---|
| **Touchpoints** | Demo booking page, recorded demo video, sales engineering call, pricing page, security/compliance docs |
| **Actions** | Books a demo or starts self-serve trial, asks about SSO and data residency, checks whether their ERP integrates |
| **Thinking** | "Can I justify the licence cost?" / "What's the implementation overhead?" / "How do I get buy-in from my team?" |
| **Feeling** | Cautiously optimistic but protective of their time; anxious about another failed tool rollout |
| **Pain points** | Pricing page lacks mid-market tier clarity; integration list is buried in docs; sales follow-up cadence is too aggressive |
| **Opportunities** | Surface integration compatibility check on the pricing page; add a "typical setup time for your stack" estimator |

**Drop-off risk:** High — POC outcome at the next stage is the primary fork; losing trust here ends the journey.

---

### Stage 3: Trial / POC

**User goal at this stage:** Get one real report out of Clearpath using live data
**Duration:** 7–21 days
**Evidence basis:** Evidence-based (product analytics funnel, support ticket themes)

| Element | Detail |
|---|---|
| **Touchpoints** | Signup form, in-product onboarding checklist, integration connector UI, sales engineering call, support chat |
| **Actions** | Connects data source (ERP or spreadsheet), configures first report template, invites one team member, attempts to schedule a share |
| **Thinking** | "Is this going to be accurate?" / "I need to show this to my CFO next week — will it be ready?" |
| **Feeling** | Motivated but increasingly frustrated if the first integration fails; confidence is fragile |
| **Pain points** | Integration failures surface a generic error with no remediation path; onboarding checklist doesn't adapt to role (director vs. analyst) |
| **Opportunities** | Build a connector validator that catches auth and schema mismatches before the first sync attempt; add a role-based onboarding path |

**Drop-off risk:** Very high — a failed first integration at this stage causes abandonment in 40% of trials (product analytics, Q3 cohort).

---

### Stage 4: First Value

**User goal at this stage:** Share a Clearpath report with a stakeholder and receive positive signal
**Duration:** 1–3 days
**Evidence basis:** Evidence-based (activation event tracking, onboarding survey follow-up)

| Element | Detail |
|---|---|
| **Touchpoints** | Report share link, email notification to recipient, in-product share confirmation screen |
| **Actions** | Exports or shares report link, waits for stakeholder reaction, may loop in IT to approve email domain |
| **Thinking** | "Did this actually look professional?" / "Will they actually open it?" |
| **Feeling** | Proud if the share goes well; deflated if the link requires a login the recipient doesn't have |
| **Pain points** | Shared report requires recipient to create an account — kills the "wow moment" for a director trying to impress a CFO |
| **Opportunities** | Introduce a public/token link share option for report recipients with no account required; add a preview of what the recipient will see before sending |

**Drop-off risk:** Medium — users who reach first share convert to paid at 3× the rate of those who don't.

---

### Stage 5: Activation and Daily Use

**User goal at this stage:** Make Clearpath the default tool for weekly portfolio reporting
**Duration:** 14–30 days to habit formation
**Evidence basis:** Hypothesis (daily active use cohorts visible in analytics; qualitative reasons not yet researched)

| Element | Detail |
|---|---|
| **Touchpoints** | Weekly digest email, in-product notification centre, Slack integration (if enabled), renewal prompt |
| **Actions** | Checks Clearpath before weekly ops standup, updates project status, reviews auto-generated variance flags |
| **Thinking** | "Is this saving me time compared to the spreadsheet?" / "Should I roll this out to the other teams?" |
| **Feeling** | Satisfied when it surfaces a risk they didn't know about; frustrated if data staleness makes them look uninformed in a meeting |
| **Pain points** | Data refresh cadence (default 24h) is too slow for directors who review in real-time meetings; no alert when data goes stale |
| **Opportunities** | Add a "data freshness" indicator on every report; allow per-report refresh schedules; trigger a proactive nudge when a key metric moves outside tolerance |

**Drop-off risk:** Low once 30-day daily-use threshold is passed; medium before it.

---

### Critical Moments

| Moment | Stage | Description | Impact | Evidence |
|---|---|---|---|---|
| **Moment of truth** | Trial / POC | First successful data sync and report render | A clean first sync leads to 70%+ trial completion; failure leads to 40% abandonment | Product analytics, Q3 cohort |
| **Biggest drop-off** | Trial / POC | Integration failure with no clear fix path | 40% of trials end here; primary churn reason cited in exit surveys | Exit survey data, support ticket volume |
| **Delight opportunity** | First Value | Stakeholder opens shared report and responds positively | Directors who receive positive stakeholder feedback convert at 3× rate and expand seats | Activation tracking, sales CRM notes |

**Time to first value:** Current median is 18 days from signup to first shared report. Target is 14 days. The gap is concentrated in the Trial / POC integration stage.

---

### Journey Health

| Stage | Feeling | Drop-off risk | Top pain point | Top opportunity |
|---|---|---|---|---|
| Awareness | 😐 Sceptical | H | Homepage doesn't answer "why me?" | Outcome-led homepage copy |
| Evaluation | 🤔 Cautious | H | Integration compatibility unclear | Integration checker on pricing page |
| Trial / POC | 😤 Frustrated | Very H | Integration failure, no remediation | Connector validator before first sync |
| First Value | 😊 Proud | M | Recipient must create account to view | Token-link share for recipients |
| Activation | 😌 Satisfied | M | Data goes stale without warning | Data freshness indicator + smart alerts |

### Recommendations

| Priority | Recommendation | Stage affected | Expected impact on time-to-first-value | Effort |
|---|---|---|---|---|
| 1 | Build a connector validator that checks auth and schema compatibility before the first sync attempt, with plain-language remediation steps | Trial / POC | Reduce integration failure rate by ~50%; close 4-day gap to 14-day target | M |
| 2 | Introduce a public token-link share option so report recipients can view without creating an account | First Value | Increase stakeholder share conversion; improve director-to-paid conversion rate | S |
| 3 | Add a data freshness indicator on every report and a configurable stale-data alert | Activation | Reduce churn from staleness complaints; support expansion conversations | S |
| 4 | Rewrite homepage hero with an outcome-led headline targeted at operations directors | Awareness | Lift trial signup rate from organic search (currently 2.1% CTR) | S |
| 5 | Add an integration compatibility checker to the pricing page | Evaluation | Reduce sales-call length; qualify leads earlier | M |

---

Evidence basis: 4 of 5 stages evidence-based, 1 hypothesis (Activation qualitative reasons).
Last updated: 2026-04-30

---

## Criteria results

- [x] PASS: Skill requires defining a scope with a concrete start trigger and end outcome before mapping begins — Step 1 mandates start/end points as "concrete events, not states" with explicit scope table
- [x] PASS: Skill requires identifying evidence sources before mapping — Step 2 is a mandatory evidence-gathering step before stage mapping, with explicit rules about labelling hypothesis stages
- [x] PASS: Skill maps all four customer dimensions per stage: actions, thinking, feeling, and pain points — Step 3 stage table includes Actions, Thinking, Feeling, and Pain points as required fields
- [x] PASS: Skill requires touchpoints and channels to be specified for each stage — Touchpoints row is mandatory in each Stage table in Step 3
- [x] PASS: Skill identifies critical moments — Step 4 is a mandatory "Identify critical moments" step with Moment of truth, Biggest drop-off, and Delight opportunity fields
- [x] PASS: Skill produces improvement recommendations linked to specific stages — Step 5 recommendations table includes "Stage affected" column; rules require specific opportunities not generic advice
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — frontmatter present with all three fields

### Output expectations

- [x] PASS: Output's scope defines a concrete start trigger ("first encounters Clearpath via Google search, LinkedIn ad, or peer recommendation") and end outcome ("uses Clearpath for portfolio reporting at least 5 days/week for 30+ consecutive days") — not abstract beginning / end
- [x] PASS: Output names evidence sources — sales call recordings, onboarding survey responses, support tickets, churn interview notes, product analytics, session recordings — with coverage column and evidence gaps flagged
- [x] PASS: Output maps all four customer dimensions per stage — Actions, Thinking, Feeling, and Pain points present for all five stages
- [x] PASS: Output's touchpoints / channels per stage are specific — Awareness: Google search, LinkedIn ads, peer Slack/email, G2/Capterra, homepage; Trial: signup form, in-product onboarding checklist, integration connector UI, sales engineering call, support chat; named throughout
- [x] PASS: Output identifies critical moments with reasoning — Moment of truth (first sync), Biggest drop-off (integration failure, 40% abandonment, cited evidence), Delight opportunity (stakeholder share, 3× conversion rate) — each with impact and evidence
- [x] PASS: Output's improvement recommendations are linked to specific stages — every recommendation row names the stage; e.g. "Trial / POC: connector validator for integration failures" tied directly to the mapped pain point

## Notes

The skill structure enforces good research discipline through mandatory steps and explicit labelling rules for hypothesis stages. The evidence-based / hypothesis distinction is well-designed — it stops the map from presenting invented pain points as fact. The rules section is strong: "Opportunities must be specific" and "Pain points without evidence are opinions" are load-bearing constraints that would catch low-quality outputs. One minor gap: the skill doesn't specify a minimum or maximum number of stages, which leaves the 4–7 range as guidance rather than a hard constraint. For most journeys this is fine; for very long journeys it may produce sprawl.
