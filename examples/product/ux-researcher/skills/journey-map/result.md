# Journey Map

Scenario: Testing whether the journey-map skill requires evidence sources, maps all journey dimensions (actions/thinking/feeling/pain), and identifies critical moments.

## Prompt

> /ux-researcher:journey-map for the customer journey from first hearing about Clearpath through to becoming an active daily user — specifically for mid-market operations directors.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

---

## Journey: Awareness to Active Daily User — Mid-Market Operations Director

---

### Scope

| Element | Definition |
|---|---|
| **User type** | Mid-market Operations Director (100–500 person company; title: Director/VP Operations or equivalent COO) with budget authority and accountability for team efficiency KPIs |
| **Journey** | Full acquisition and activation: discovery → evaluation → purchase → onboarding → habitual daily use |
| **Start point** | First exposure to the Clearpath brand (ad, referral, review site, or content) |
| **End point** | Clearpath is part of the director's daily operating rhythm — opened every working day, used to run team standups or review ops metrics |
| **Success metric** | Time to first value: days from sign-up to first genuine "aha" moment (target: ≤7 days). Secondary: 90-day daily active use rate |

---

### Evidence Sources

| Source | What it tells us | Coverage |
|---|---|---|
| Support tickets | Where users get stuck during onboarding; configuration errors; integration failures | Stages 6–7 |
| Analytics | Drop-off points in trial flow, time-to-first-action, feature adoption rates | Stages 4–7 |
| Session recordings | Where trial users hesitate, rage-click, or abandon setup flows | Stages 4–6 |
| User interviews | Motivations, emotional state, internal politics, unspoken frustrations | All stages |
| Sales/CS conversations | Objections raised, expectations set vs. reality, stall reasons in pipeline | Stages 2–5 |
| G2 / Capterra reviews | What buyers valued in hindsight, recurring complaints, comparison criteria | Stages 2–3 |

**Evidence gaps:** No evidence data was available for this map. **All 7 stages are hypothesis.** This map should be treated as a research plan — the stages, pain points, and opportunities require validation through user interviews, analytics review, and sales call analysis before being acted on.

---

### Stage 1: Awareness

**User goal:** Passively discover that a product like Clearpath exists; form a first impression strong enough to remember it  
**Duration:** Instantaneous impression; passive awareness may linger days–weeks before action  
**Evidence basis:** Hypothesis

| Element | Detail |
|---|---|
| **Touchpoints** | LinkedIn sponsored post, organic post from a peer, G2 category page, industry newsletter, conference mention, Google search for "operations management software mid-market" |
| **Actions** | Pauses on an ad or post; scans headline and value prop; may click through to homepage; reads 2–3 sentences; forms a first impression; moves on |
| **Thinking** | "Is this actually different from what we already have?", "Does this work for companies our size or is it enterprise-only?", "Have I heard of these people before?" |
| **Feeling** | Mildly curious, immediately sceptical — they've been pitched ops software before and it has rarely delivered |
| **Pain points** | Generic messaging that doesn't signal mid-market fit; enterprise case studies that feel irrelevant; no immediate credibility signal (recognisable customers, peer endorsement) |
| **Opportunities** | Lead with a specific mid-market outcome ("300-person ops teams cut weekly reporting time by 40%"); show one recognisable logo from a similar-sized company; peer-to-peer LinkedIn organic outperforms paid for this audience |

**Drop-off risk: High** — most impressions don't convert to active consideration; the window to earn attention is under 8 seconds.

---

### Stage 2: Research & Consideration

**User goal:** Self-educate enough to decide whether Clearpath is worth spending time on — without talking to a salesperson yet  
**Duration:** 1–3 weeks (squeezed into gaps between meetings; rarely a focused session)  
**Evidence basis:** Hypothesis

| Element | Detail |
|---|---|
| **Touchpoints** | Clearpath website, G2/Capterra product page and reviews, YouTube demo video, LinkedIn company page, case study PDFs, peer DMs or Slack community posts |
| **Actions** | Reads homepage and pricing page; watches a demo video (often skips to the middle); reads 3–5 G2 reviews filtering for similar-sized companies; messages 1–2 LinkedIn connections who might know the product |
| **Thinking** | "What does implementation actually look like?", "Will my team adopt this or will it be another shelfware situation?", "Is pricing transparent or is there a 'call us' wall?", "How does this compare to [competitor]?" |
| **Feeling** | Interested but time-pressured; undercurrent of anxiety about sponsoring another failed tool rollout |
| **Pain points** | Pricing hidden behind "contact sales" (trust-breaker for self-educators); case studies too generic; no content addressing change management or team adoption; demo videos too surface-level |
| **Opportunities** | Publish a mid-market pricing guide even if not exact figures; create a "what implementation looks like" page; add a short unscripted walkthrough of a realistic workflow, not a polished marketing demo |

**Drop-off risk: High** — if the website doesn't answer "is this for a company like mine?" within the first visit, they don't return.

---

### Stage 3: Internal Alignment & Business Case

**User goal:** Secure enough internal support (IT, Finance, potentially CEO/CFO) to proceed to a formal trial  
**Duration:** 2–4 weeks  
**Evidence basis:** Hypothesis

| Element | Detail |
|---|---|
| **Touchpoints** | Internal Slack/email with IT lead and finance; Clearpath ROI calculator (if it exists); vendor's security/compliance documentation; existing tool vendor contracts |
| **Actions** | Identifies integration requirements with IT; drafts a rough business case for Finance; flags to CEO if spend threshold requires sign-off; estimates team adoption timeline |
| **Thinking** | "How do I justify this to the CFO without looking like I'm guessing?", "What happens to my reputation if this fails?", "Will IT block this?", "Can I get this done before the half-year budget review?" |
| **Feeling** | Politically cautious; somewhat anxious — this is where enthusiasm can quietly die if the internal path looks too hard |
| **Pain points** | No self-service ROI calculator; security documentation buried or missing (IT blocker); no email/slide templates to help the champion pitch internally; vendor not proactively offering to assist |
| **Opportunities** | Provide a downloadable "ops director toolkit": ROI estimator, IT security one-pager, and a pitch deck template; offer a vendor-assisted business case call before the formal sales process begins |

**Drop-off risk: High** — the most common stall point in B2B mid-market. The champion runs out of internal momentum before ever starting a trial.

---

### Stage 4: Trial & Evaluation

**User goal:** Validate that Clearpath solves their specific problems, not a generalised version of them  
**Duration:** 2–4 weeks  
**Evidence basis:** Hypothesis

| Element | Detail |
|---|---|
| **Touchpoints** | Trial/POC environment, onboarding email sequence, in-app tooltips, sales engineer/CSM support, 1–2 team leads co-evaluating |
| **Actions** | Signs up; imports or enters sample data; configures 1–2 core workflows; invites 2–3 team members; attends 1 vendor-led demo call; hits a configuration wall; decides whether to continue |
| **Thinking** | "How long until I see actual value — not just features?", "Is the data import going to take weeks?", "Why can't I figure out [specific workflow] without calling support?", "Would my team actually use this every day?" |
| **Feeling** | Hopeful at the start; progressively frustrated if early friction isn't resolved; delight is possible if the product surprises them |
| **Pain points** | Generic onboarding not adapted to operations use cases; too many features shown before core value is demonstrated; data import complexity without hands-on help; no clear "north star" first action |
| **Opportunities** | Build a role-specific onboarding track for ops directors: surface the 2–3 most relevant workflows on first login; offer a 30-minute "quick wins" call with a CSM on day 2; automated day-3 check-in if key actions haven't been taken |

**Drop-off risk: High** — industry benchmarks for B2B SaaS trial-to-paid conversion are 15–25%; poor time-to-first-value is the primary driver of failure.

---

### Stage 5: Decision & Purchase

**User goal:** Confirm final terms, clear procurement blockers, and get a signed contract  
**Duration:** 2–6 weeks  
**Evidence basis:** Hypothesis

| Element | Detail |
|---|---|
| **Touchpoints** | Sales AE, contract/MSA, IT security review, legal review, procurement workflow, billing setup |
| **Actions** | Negotiates pricing and contract length; loops in IT for security sign-off; gets CFO/finance approval; signs; receives onboarding handoff |
| **Thinking** | "Are we on the right tier for our team size?", "What's the exit clause if this doesn't work out?", "Is this vendor going to be around in 2 years?", "Did I get the best price?" |
| **Feeling** | Cautiously optimistic but stressed by procurement friction; relief when it's signed |
| **Pain points** | Slow security review turnaround from vendor; opaque contract terms around data portability and cancellation; pricing that feels different from what was implied during trial |
| **Opportunities** | Publish security and data portability information proactively to pre-empt IT reviews; "match with a reference customer your size" programme at contract stage; AE procurement accelerator checklist |

**Drop-off risk: Medium** — the champion is bought in, but procurement friction can slip deals into the next budget cycle.

---

### Stage 6: Onboarding & Implementation

**User goal:** Get the team live on Clearpath, with real workflows running, within 30 days  
**Duration:** 30–90 days  
**Evidence basis:** Hypothesis

| Element | Detail |
|---|---|
| **Touchpoints** | Dedicated CSM, in-app setup flow, training sessions, help centre/docs, internal comms to ops team, integration configuration |
| **Actions** | Migrates real data; configures workflows; runs team training; champions internal adoption; monitors usage; escalates issues to CSM |
| **Thinking** | "Why isn't my team using this as much as I expected?", "The integration isn't working the way sales described", "How do I show a quick win to my CEO?", "Is setup more complex than I was led to believe?" |
| **Feeling** | Overwhelmed in weeks 1–2; mix of relief and worry by week 4 — proud if early wins are visible, anxious if adoption is lagging |
| **Pain points** | Change management entirely left to champion — no resources for driving team adoption; integration issues not surfaced during evaluation; onboarding assumes more internal bandwidth than a mid-market team has |
| **Opportunities** | Ops director launch kit: internal announcement template, team FAQ, week-1 adoption checklist; team adoption dashboard visible to director; 2-week check-in to surface issues; pre-built workflow templates for common ops use cases |

**Drop-off risk: Medium** — the most common failure is quiet non-adoption: the director is technically a customer but the team isn't using it, and renewal is at risk.

---

### Stage 7: Active Daily Use

**User goal:** Use Clearpath as the primary lens through which they run operations — opening it daily, relying on it for decisions, expanding to adjacent teams  
**Duration:** Month 3+ (target active state)  
**Evidence basis:** Hypothesis

| Element | Detail |
|---|---|
| **Touchpoints** | Clearpath dashboard (daily), weekly ops reports generated from Clearpath, team standups using Clearpath data, product changelog emails, expansion conversations with CSM |
| **Actions** | Reviews daily ops metrics; runs team meetings from the platform; exports data for senior leadership reporting; identifies underused features; considers expanding to additional teams |
| **Thinking** | "What else can I do with this that I'm not?", "Can I get the warehouse/field team on this too?", "This has saved me 3 hours of reporting a week — how do I show that to my CEO?" |
| **Feeling** | Confident; quiet satisfaction when the platform enables a visible win; mild frustration with product gaps; pride in having championed a successful rollout |
| **Pain points** | No in-product prompts to surface underused high-value features; no built-in way to export a "value realised" summary for internal reporting; expansion conversation initiated by vendor too late (month 9 renewal vs. month 3 when satisfaction peaks) |
| **Opportunities** | Monthly value digest email (time saved, workflows run, adoption rate — forwardable to CEO); proactive expansion conversation at month 3; power-user programme with peer networking among ops directors |

**Drop-off risk: Low** — if genuine daily use is established. If usage is shallow (director only, team not engaged), renewal churn risk is Medium.

---

### Critical Moments

| Moment | Stage | Description | Impact | Evidence |
|---|---|---|---|---|
| **Moment of truth** | 4 – Trial | First time the director sees Clearpath display a real ops metric or workflow from their *own* data — not sample data. This is the "aha moment" that justifies the evaluation. | If this doesn't happen within 3–5 days of trial start, engagement drops sharply and the evaluation is quietly abandoned | Hypothesis — requires analytics validation |
| **Biggest drop-off** | 3 – Internal Alignment | Champion loses momentum trying to build an internal business case without vendor support. The evaluation never reaches a formal trial. | Loss of the deal before it starts; invisible in most funnels because it happens before CRM contact | Hypothesis — requires sales pipeline analysis |
| **Delight opportunity** | 6 – Onboarding | Director sees a Clearpath-generated report they can share directly with their CEO — saving 2+ hours of manual compilation. Unexpected, immediate, personally meaningful. | Converts a cautious adopter into an internal advocate; dramatically increases renewal probability | Hypothesis |

**Time to first value:** Target ≤7 days from trial sign-up to first genuine value moment (real data, real workflow, real insight). This is the leading indicator for 90-day retention and trial-to-paid conversion.

---

### Journey Health

| Stage | Feeling | Drop-off risk | Top pain point | Top opportunity |
|---|---|---|---|---|
| 1. Awareness | 😐 Sceptical | H | Generic messaging; no mid-market signal | Lead with specific mid-market outcome in the first 8 words |
| 2. Research | 🤔 Interested but wary | H | Pricing hidden; case studies too generic | Mid-market pricing guide + "what implementation looks like" page |
| 3. Internal Alignment | 😬 Cautious / anxious | H | No tools to help champion pitch internally | Downloadable business case toolkit before sales process begins |
| 4. Trial | 🙏 Hopeful → frustrated | H | Generic onboarding; slow time-to-value | Ops-director onboarding track + day-2 CSM "quick wins" call |
| 5. Decision | 😌 Relieved when done | M | Slow procurement; opaque contract terms | Proactive security docs + AE procurement accelerator checklist |
| 6. Onboarding | 😰 Overwhelmed → cautious | M | Change management left to champion | Ops director launch kit + team adoption dashboard |
| 7. Daily Use | 😊 Confident / satisfied | L | No built-in CEO value report; expansion too late | Monthly value digest email + expansion conversation at month 3 |

---

### Recommendations

Prioritised by impact on **time to first value** and **90-day daily active use rate**.

| Priority | Recommendation | Stage | Expected impact | Effort |
|---|---|---|---|---|
| 1 | Build an ops-director onboarding track: surfaces 3 most relevant workflows on first login, single "complete this first" CTA, progress indicator | 4 – Trial | Reduces time-to-first-value from ~14 days to ≤7; directly lifts trial-to-paid conversion | M |
| 2 | Create a downloadable champion toolkit (ROI estimator, IT security one-pager, internal pitch deck template); surface it proactively during website research visits | 3 – Internal Alignment | Reduces the most common silent drop-off; shortens sales cycles by 1–2 weeks | M |
| 3 | Build a monthly value digest email: time saved, workflows run, team adoption rate — formatted for the director to forward to their CEO | 7 – Daily Use | Increases renewal probability; surfaces expansion opportunities at peak satisfaction | S |
| 4 | Rewrite homepage and paid ad hero copy to lead with a specific, quantified mid-market outcome | 1 – Awareness | Improves click-through and homepage-to-trial conversion; no product changes required | S |
| 5 | Introduce a day-2 "quick wins" call with a CSM for all new trials — 30 minutes to get one real workflow live with real data | 4 – Trial | High-touch intervention at the lowest-cost moment; backstop for users who don't complete self-serve | S |
| 6 | Publish a mid-market implementation page: typical timeline, what IT needs, what setup involves — before the "contact sales" wall | 2 – Research | Reduces drop-off of self-educating buyers who won't submit a contact form | S |

---

Evidence basis: **0 of 7 stages evidence-based, 7 hypothesis**  
Last updated: 2026-05-01  
Next validation step: Run 5 lost-deal interviews to validate the Stage 3 drop-off hypothesis; pull trial funnel analytics to confirm Stage 4 time-to-first-action data.

---

Saved to `docs/design/research/journey-map--clearpath--ops-director.md`.

**Important caveat:** No Clearpath product documentation exists in the codebase — all 7 stages are hypothesis. Before acting on any recommendation, validate with sales pipeline data (Stage 3), trial analytics (Stage 4), and at minimum 5 customer interviews. The map is a research plan, not a fact.

### Artifacts written

#### `work/docs/design/research/journey-map--clearpath--ops-director.md`

```
## Journey: Awareness to Active Daily User — Mid-Market Operations Director

---

### Scope

| Element | Definition |
|---|---|
| **User type** | Mid-market Operations Director (100–500 person company; title: Director/VP Operations or equivalent COO) with budget authority and accountability for team efficiency KPIs |
| **Journey** | Full acquisition and activation: discovery → evaluation → purchase → onboarding → habitual daily use |
| **Start point** | First exposure to the Clearpath brand (ad, referral, review site, or content) |
| **End point** | Clearpath is part of the director's daily operating rhythm — opened every working day, used to run team standups or review ops metrics |
| **Success metric** | Time to first value: days from sign-up to first genuine "aha" moment (target: ≤7 days). Secondary: 90-day daily active use rate |

---

### Evidence Sources

| Source | What it tells us | Coverage |
|---|---|---|
| Support tickets | Where users get stuck during onboarding; configuration errors; integration failures | Stages 6–7 |
| Analytics | Drop-off points in trial flow, time-to-first-action, feature adoption rates | Stages 4–7 |
| Session recordings | Where trial users hesitate, rage-click, or abandon setup flows | Stages 4–6 |
| User interviews | Motivations, emotional state, internal politics, unspoken frustrations | All stages |
| Sales/CS conversations | Objections raised, expectations set vs. reality, stall reasons in pipeline | Stages 2–5 |
| G2 / Capterra reviews | What buyers valued in hindsight, recurring complaints, comparison criteria | Stages 2–3 |

**Evidence gaps:** No evidence data was available for this map. **All stages are hypothesis.** This map should be treated as a research plan — the stages, pain points, and opportunities require validation through user interviews, analytics review, and sales call analysis before being acted on.

---

### Stage 1: Awareness

**User goal at this stage:** Passively discover that a product like Clearpath exists; form a first impression strong enough to remember it  
**Duration:** Instantaneous impression, but passive awareness may linger for days–weeks before action  
**Evidence basis:** Hypothesis

| Element | Detail |
|---|---|
| **Touchpoints** | LinkedIn sponsored post, LinkedIn organic post from a peer, G2 category page, industry newsletter, conference mention, Google search for "operations management software mid-market" |
| **Actions** | Pauses on an ad or post, scans the headline and value prop, may click through to homepage, reads 2–3 sentences, forms a first impression, moves on |
| **Thinking** | "Is this actually different from [existing tool]?", "Does this work for companies our size or is it enterprise-only?", "Have I heard of these people before?" |
| **Feeling** | Mildly curious, immediately sceptical — they've been pitched ops software before and it has rarely delivered |
| **Pain points** | Generic messaging that doesn't speak to mid-market scale; enterprise case studies that feel irrelevant; no immediate signal of credibility (recognisable customers, peer endorsement) |
| **Opportunities** | Lead with a specific mid-market outcome ("300-person ops teams cut weekly reporting time by 40%"); show one recognisable logo from a similar-sized company; peer-to-peer distribution via LinkedIn organic outperforms paid for this audience |

**Drop-off risk:** High — most impressions don't convert to active consideration. The window to earn attention is under 8 seconds.

---

### Stage 2: Research & Consideration

**User goal at this stage:** Self-educate enough to decide whether Clearpath is worth spending time on — without talking to a salesperson yet  
**Duration:** 1–3 weeks (squeezed into gaps between meetings; rarely a focused session)  
**Evidence basis:** Hypothesis

| Element | Detail |
|---|---|
| **Touchpoints** | Clearpath marketing website, G2 / Capterra product page and reviews, YouTube demo video, LinkedIn company page, case study PDFs, peer DMs or Slack community posts |
| **Actions** | Reads homepage and pricing page, watches a demo video (often skips to the middle), reads 3–5 G2 reviews filtering for companies of similar size, messages 1–2 LinkedIn connections who might know the product |
| **Thinking** | "What does implementation actually look like?", "Will my team adopt this or will it be another shelfware situation?", "Is pricing transparent or is there a 'call us' wall?", "How does this compare to [competitor]?" |
| **Feeling** | Interested but time-pressured; a small undercurrent of anxiety about sponsoring another tool rollout that fails |
| **Pain points** | Pricing hidden behind "contact sales" (trust-breaker for self-educators); case studies too generic ("a logistics company saved time"); no content addressing change management or team adoption; demo videos too surface-level to answer real questions |
| **Opportunities** | Publish a mid-market pricing guide even if not exact figures; create a "what implementation looks like" page; add a short unscripted walkthrough of a realistic workflow, not a polished marketing demo; make G2 review cultivation a priority |

**Drop-off risk:** High — if the website doesn't answer "is this for a company like mine?" within the first visit, they don't return.

---

### Stage 3: Internal Alignment & Business Case

**User goal at this stage:** Secure enough internal support (IT, Finance, potentially CEO/CFO) to proceed to a formal trial without being blocked  
**Duration:** 2–4 weeks  
**Evidence basis:** Hypothesis

| Element | Detail |
|---|---|
| **Touchpoints** | Internal Slack/email with IT lead and finance; Clearpath ROI calculator (if it exists); vendor's security/compliance documentation; existing tool vendor contracts (comparison) |
| **Actions** | Identifies integration requirements with IT, drafts a rough business case for Finance, flags to CEO/COO if spend threshold requires sign-off, estimates team adoption timeline |
| **Thinking** | "How do I justify this to the CFO without looking like I'm guessing?", "What happens to my reputation if this rolls out and the team doesn't use it?", "Will IT actually support this or quietly block it?", "Can I get this done before the half-year budget review?" |
| **Feeling** | Politically cautious; somewhat anxious; this stage is where enthusiasm can quietly die if the internal path looks too hard |
| **Pain points** | No self-service ROI calculator; security documentation buried or missing (IT blocker); no email/slide templates to help the champion pitch internally; vendor not proactively offering to assist with the business case |
| **Opportunities** | Provide a downloadable "ops director toolkit": ROI estimator, IT security one-pager, and a slide deck template they can adapt for internal pitching; proactively offer a vendor-assisted business case call before the formal sales process begins |

**Drop-off risk:** High — this is the most common stall point in B2B mid-market. The champion runs out of internal momentum before ever starting a trial.

---

### Stage 4: Trial & Evaluation

**User goal at this stage:** Validate that Clearpath actually solves their specific problems, not a generalised version of them  
**Duration:** 2–4 weeks  
**Evidence basis:** Hypothesis

| Element | Detail |
|---|---|
| **Touchpoints** | Trial or POC environment, onboarding email sequence, in-app tooltips and walkthroughs, sales engineer / CSM support, 1–2 team leads brought in to co-evaluate |
| **Actions** | Signs up, imports or enters sample data, configures 1–2 core workflows, invites 2–3 team members to trial alongside, attends 1 vendor-led demo call, hits a configuration wall, decides whether it's worth continuing |
| **Thinking** | "How long until I see actual value — not just features?", "Is the data import going to take weeks?", "Why can't I figure out how to do [specific workflow] without calling support?", "Would my team actually use this every day?" |
| **Feeling** | Hopeful at the start; progressively frustrated if early friction isn't resolved quickly; this is where delight is possible if the product surprises them with something they didn't expect |
| **Pain points** | Generic onboarding that doesn't adapt to operations use cases; too many features shown at once before core value is demonstrated; data import complexity without hands-on help; no clear "north star" action — what should I do first? |
| **Opportunities** | Build a role-specific onboarding track for operations directors: surface the 2–3 workflows most relevant to their role within the first login; offer a 30-minute "quick wins" call with a CSM on day 2; set up an automated day-3 check-in if key actions haven't been taken |

**Drop-off risk:** High — industry benchmarks for trial-to-paid conversion in B2B SaaS suggest 15–25% of trials convert. Poor time-to-first-value is the primary driver of failure.

---

### Stage 5: Decision & Purchase

**User goal at this stage:** Confirm final terms, clear procurement blockers, and get a signed contract  
**Duration:** 2–6 weeks  
**Evidence basis:** Hypothesis

| Element | Detail |
|---|---|
| **Touchpoints** | Sales AE, contract/MSA, IT security review, legal review if required, procurement workflow, payment/billing setup |
| **Actions** | Negotiates pricing and contract length, loops in IT for final security sign-off, gets CFO/finance approval, signs, receives confirmation and onboarding handoff |
| **Thinking** | "Are we on the right tier for our team size?", "What's the exit clause if this doesn't work out?", "Is this vendor going to survive — will we be renegotiating in 18 months with someone else?", "Did I get the best price?" |
| **Feeling** | Cautiously optimistic but quietly stressed by procurement friction; relief when it's signed |
| **Pain points** | Slow legal/security review turnaround from the vendor; opaque contract terms around data portability and cancellation; no clear picture of what support tier they're getting; pricing that feels different from what was implied during the trial |
| **Opportunities** | Publish security and data portability information proactively on the website to pre-empt IT reviews; offer a "we'll match you with a reference customer your size" programme at contract stage to resolve last-minute doubt; give AEs a standard "procurement accelerator" checklist |

**Drop-off risk:** Medium — by this stage the champion is bought in, but procurement process can kill or delay deals. The main risk is deal timing slippage into the next budget cycle.

---

### Stage 6: Onboarding & Implementation

**User goal at this stage:** Get the team live on Clearpath, with real workflows running, within 30 days  
**Duration:** 30–90 days  
**Evidence basis:** Hypothesis

| Element | Detail |
|---|---|
| **Touchpoints** | Dedicated CSM, in-app setup flow, training sessions, Clearpath help centre/docs, internal comms to the ops team, integration configuration with existing tools |
| **Actions** | Migrates real data, configures workflows for their specific operations, runs a team training session, champions adoption internally, monitors usage in the first weeks, escalates issues to CSM |
| **Thinking** | "Why isn't my team using this as much as I expected?", "The [integration] isn't working the way the sales team described", "How do I show a quick win to my CEO so I don't look like I wasted budget?", "Is setup more complex than I was led to believe?" |
| **Feeling** | Overwhelmed in weeks 1–2; a mix of relief and worry by week 4 — proud if early wins are visible, anxious if adoption is lagging |
| **Pain points** | Change management is almost entirely left to the champion — no resources for how to drive team adoption; integration issues that weren't surfaced during evaluation; onboarding timelines that assume more internal bandwidth than a mid-market team has; CSM assigned post-sale is less knowledgeable than the sales engineer who ran the trial |
| **Opportunities** | Provide an "ops director launch kit": internal announcement template, team FAQ, week-1 adoption checklist; build a lightweight team adoption dashboard visible to the director; schedule a 2-week check-in to surface issues before they calcify; create a library of pre-built workflow templates for common ops use cases |

**Drop-off risk:** Medium — the most common failure is quiet non-adoption: the director is technically a customer but the team isn't using it, and renewal is at risk.

---

### Stage 7: Active Daily Use

**User goal at this stage:** Use Clearpath as the primary lens through which they run their operations — opening it daily, relying on it for decisions, and expanding its use across the team  
**Duration:** Month 3 onwards (target active state)  
**Evidence basis:** Hypothesis

| Element | Detail |
|---|---|
| **Touchpoints** | Clearpath dashboard (daily), weekly ops review reports generated from Clearpath, team stand-up using Clearpath data, product changelog/update emails, account expansion conversations with CSM |
| **Actions** | Reviews daily ops metrics, runs team meetings from the platform, exports data for senior leadership reporting, identifies underused features, considers rolling out to additional teams |
| **Thinking** | "What else can I do with this that I'm not doing yet?", "How do I get my team to use [feature X] more consistently?", "Can I get the warehouse/field team on this too?", "This has saved me 3 hours of reporting a week — how do I show that to my CEO?" |
| **Feeling** | Confident; quiet satisfaction when the platform enables a visible win; mild frustration with occasional product gaps; pride in having championed a successful rollout |
| **Pain points** | No in-product prompts to surface underused high-value features; no built-in way to export a "value realised" summary for internal reporting to CEO/board; expansion conversation initiated by vendor too late (month 9 renewal vs. month 3 when value is fresh) |
| **Opportunities** | Build a "monthly value digest" email: time saved, workflows completed, team adoption rate — content the director can forward to their CEO; proactively introduce the "expansion to adjacent team" conversation at month 3 when satisfaction is highest; create a power-user programme with peer networking among ops directors |

**Drop-off risk:** Low at this stage if genuine daily use is established — but if usage is shallow (director only, team not engaged), renewal churn risk is Medium.

---

### Critical Moments

| Moment | Stage | Description | Impact | Evidence |
|---|---|---|---|---|
| **Moment of truth** | Stage 4: Trial | The first time the director sees Clearpath display a real operations metric or workflow from their own data — not sample data. This is the "aha moment" that justifies the evaluation. | If this doesn't happen within 3–5 days of trial start, engagement drops sharply and the evaluation is quietly abandoned | Hypothesis — requires analytics validation |
| **Biggest drop-off** | Stage 3: Internal Alignment | The champion loses momentum trying to build an internal business case without vendor support. The evaluation never reaches a formal trial. | Loss of the deal before it starts; invisible in most funnels because it happens before CRM contact | Hypothesis — requires sales pipeline analysis |
| **Delight opportunity** | Stage 6: Onboarding | The director sees a Clearpath-generated report they can share directly with their CEO — saving 2+ hours of manual compilation. Unexpected, immediate, and personally meaningful. | Converts a cautious adopter into an internal advocate; dramatically increases renewal probability and expansion | Hypothesis |

### Key metric
**Time to first value:** Target ≤7 days from trial sign-up to first genuine value moment (real data, real workflow, real insight). This is the leading indicator for 90-day retention and trial-to-paid conversion.

---

### Journey Health

| Stage | Feeling | Drop-off risk | Top pain point | Top opportunity |
|---|---|---|---|---|
| 1. Awareness | 😐 Sceptical | H | Generic messaging that doesn't signal mid-market fit | Lead with a specific mid-market outcome in the first 8 words |
| 2. Research | 🤔 Interested but wary | H | Pricing hidden; case studies too generic | Publish a mid-market pricing guide and a realistic "what implementation looks like" page |
| 3. Internal Alignment | 😬 Cautious / anxious | H | No tools to help champion pitch internally | Provide a downloadable business case toolkit before the sales process begins |
| 4. Trial | 🙏 Hopeful → frustrated | H | Generic onboarding; no clear first action; slow time-to-value | Ops-director-specific onboarding track; day-2 CSM "quick wins" call |
| 5. Decision | 😌 Relieved when done | M | Slow procurement; opaque contract terms | Proactive security docs; procurement accelerator checklist for AEs |
| 6. Onboarding | 😰 Overwhelmed → cautiously satisfied | M | Change management left to champion; integration surprises | Ops director launch kit; team adoption dashboard; 2-week check-in |
| 7. Daily Use | 😊 Confident / satisfied | L | No built-in way to show value to CEO; expansion too late | Monthly value digest email; expansion conversation at month 3 |

---

### Recommendations

Prioritised by impact on **time to first value** and **90-day daily active use rate**.

| Priority | Recommendation | Stage affected | Expected impact | Effort |
|---|---|---|---|---|
| 1 | Build an ops-director-specific onboarding track: surfaces the 3 most relevant workflows on first login, with a progress indicator and a single "complete this first" call-to-action | 4 – Trial | Reduces time to first value from ~14 days to ≤7 days; directly improves trial-to-paid conversion | M |
| 2 | Create a downloadable "champion toolkit" (ROI estimator, IT security one-pager, internal pitch deck template) and surface it proactively during Stage 2 website visits | 3 – Internal Alignment | Reduces the most common silent drop-off; shortens sales cycles by 1–2 weeks | M |
| 3 | Build a "monthly value digest" email: time saved, workflows run, team adoption rate — formatted so the director can forward it directly to their CEO | 7 – Daily Use | Increases renewal probability and surfaces expansion opportunities at peak satisfaction | S |
| 4 | Rewrite homepage and paid ads hero messaging to lead with a specific, quantified mid-market outcome rather than generic category claims | 1 – Awareness | Improves click-through and homepage-to-trial conversion; no product changes required | S |
| 5 | Introduce a day-2 "quick wins" call with a CSM for all new trials — 30 minutes, focused on getting one real workflow live with real data | 4 – Trial | Backstop for users who don't complete self-serve onboarding; high-touch intervention at lowest-cost moment | S |
| 6 | Publish a mid-market implementation page: what setup looks like, typical timeline, what IT needs to approve — before the "contact sales" wall | 2 – Research | Reduces drop-off of self-educating buyers who don't submit a contact form | S |

---

Evidence basis: **0 of 7 stages evidence-based, 7 hypothesis**  
Last updated: 2026-05-01  
Next step: Validate Stage 3 (internal alignment drop-off) via sales pipeline analysis and lost-deal interviews; validate Stage 4 (trial drop-off) via product analytics and session recordings.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 12.0/13.0 (92%) |
| Evaluated | 2026-05-01 |
| Target duration | 296545 ms |
| Target cost | $0.3849 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires defining a scope with a concrete start trigger and end outcome before mapping begins | PASS | A 'Scope' section appears before any stage mapping, with 'Start point: First exposure to the Clearpath brand (ad, referral, review site, or content)' and 'End point: Clearpath is part of the director's daily operating rhythm — opened every working day, used to run team standups or review ops metrics'. |
| c2 | Skill requires identifying evidence sources (interviews, analytics, support data) before mapping — not mapping from assumptions | PASS | An 'Evidence Sources' table appears before the stage breakdown, listing Support tickets, Analytics, Session recordings, User interviews, Sales/CS conversations, and G2/Capterra reviews with coverage notes. The output then explicitly states: 'No evidence data was available for this map. All stages are hypothesis' — transparently flagging the gap rather than mapping silently from assumptions. |
| c3 | Skill maps all four customer dimensions per stage: actions, thinking, feeling, and pain points | PASS | Every one of the seven stages (Awareness through Active Daily Use) contains a table with rows explicitly labelled 'Actions', 'Thinking', 'Feeling', and 'Pain points' — all four dimensions present across all stages. |
| c4 | Skill requires touchpoints and channels to be specified for each stage — not just abstract stages | PASS | Each stage's table includes a 'Touchpoints' row with named channels. E.g. Stage 1: 'LinkedIn sponsored post, LinkedIn organic post from a peer, G2 category page, industry newsletter, conference mention, Google search for operations management software mid-market'; Stage 4: 'Trial or POC environment, onboarding email sequence, in-app tooltips and walkthroughs, sales engineer / CSM support'. |
| c5 | Skill identifies critical moments — stages with the highest emotional intensity or biggest impact on outcome | PASS | A dedicated 'Critical Moments' table identifies three moments: 'Moment of truth' (Stage 4 Trial — aha moment with real data), 'Biggest drop-off' (Stage 3 Internal Alignment — champion loses momentum), and 'Delight opportunity' (Stage 6 Onboarding — CEO-ready report). Each has an Impact column and evidence basis. |
| c6 | Skill produces improvement recommendations linked to specific stages or pain points — not generic UX advice | PASS | The 'Recommendations' table has a 'Stage affected' column linking each recommendation to a named stage: e.g. 'Build an ops-director-specific onboarding track → 4 – Trial'; 'Create a downloadable champion toolkit → 3 – Internal Alignment'; 'Rewrite homepage hero messaging → 1 – Awareness'. Each recommendation also cites the specific pain point it addresses. |
| c7 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | Neither the chat response nor the written artifact (`journey-map--clearpath--ops-director.md`) contains any YAML frontmatter. There is no name, description, or argument-hint field visible anywhere in the captured output. |
| c8 | Output's scope defines a concrete start trigger ("operations director hears about Clearpath via Google search / peer recommendation / paid ad") and end outcome ("uses Clearpath at least 5 days/week for portfolio reporting") — not abstract beginning / end | PASS | Start trigger names specific channels: 'ad, referral, review site, or content'. End outcome is concrete: 'opened every working day, used to run team standups or review ops metrics'. Both are more specific than abstract labels like 'discovery' and 'retention'. |
| c9 | Output names evidence sources for the map — sales call recordings, onboarding survey responses, support tickets, churn-interview notes, product analytics — not invented from assumptions | PASS | Evidence Sources table names: Support tickets (Stages 6–7), Analytics (Stages 4–7), Session recordings (Stages 4–6), User interviews (All stages), Sales/CS conversations (Stages 2–5), G2/Capterra reviews (Stages 2–3). The output explicitly flags: 'No evidence data was available for this map. All stages are hypothesis' — demonstrating awareness rather than presenting invented data as fact. |
| c10 | Output maps all four customer dimensions per stage — Actions (what they DO), Thinking (what they're rationally weighing), Feeling (emotional state), Pain Points (frustrations, blockers) — every stage gets all four | PASS | Confirmed across all seven stages. Example from Stage 3: Actions ('Identifies integration requirements with IT, drafts a rough business case...'), Thinking ('How do I justify this to the CFO without looking like I'm guessing?'), Feeling ('Politically cautious; somewhat anxious'), Pain points ('No self-service ROI calculator; security documentation buried or missing'). |
| c11 | Output's touchpoints / channels per stage are specific — e.g. Awareness: Google search, LinkedIn ads, peer recommendations; Trial: signup form, in-product onboarding, sales engineering call — named, not generic "marketing channels" | PASS | Stage 1 Touchpoints: 'LinkedIn sponsored post, LinkedIn organic post from a peer, G2 category page, industry newsletter, conference mention, Google search for operations management software mid-market'. Stage 4 Touchpoints: 'Trial or POC environment, onboarding email sequence, in-app tooltips and walkthroughs, sales engineer / CSM support, 1–2 team leads brought in to co-evaluate'. All stages follow this named-channel pattern. |
| c12 | Output identifies critical moments — stages where emotional intensity is highest or where the journey can fork (e.g. "POC outcome decides purchase" or "first failed integration causes abandonment") — with reasoning | PASS | Critical Moments table provides three moments with explicit impact reasoning: 'Moment of truth' — 'If this doesn't happen within 3–5 days of trial start, engagement drops sharply and the evaluation is quietly abandoned'; 'Biggest drop-off' — 'Loss of the deal before it starts; invisible in most funnels because it happens before CRM contact'; 'Delight opportunity' — 'Converts a cautious adopter into an internal advocate; dramatically increases renewal probability'. |
| c13 | Output's improvement recommendations are linked to specific stages or pain points — not generic UX advice; e.g. "Onboarding stage: integration failures are the #1 friction; build a connector validator" specifically tied to a mapped pain point | PASS | Recommendations table has a 'Stage affected' column and each recommendation explicitly references the pain point it addresses. E.g. Priority 2: 'Create a downloadable champion toolkit (ROI estimator, IT security one-pager, internal pitch deck template) → Stage 3 – Internal Alignment → Reduces the most common silent drop-off', directly tied to Stage 3's mapped pain point 'No self-service ROI calculator; security documentation buried or missing'. |

### Notes

The output is a high-quality journey map that satisfies almost every criterion. It defines concrete scope, enumerates evidence sources with transparent hypothesis flagging, maps all four dimensions (actions/thinking/feeling/pain) across all seven stages, provides named touchpoints per stage, identifies critical moments with reasoning, and links recommendations to specific stages and pain points. The sole failure is c7: no YAML frontmatter (name, description, argument-hint fields) is visible in either the chat response or the written artifact. The artifact is pure markdown with no frontmatter block. Everything else in the output is executed at a high level of specificity and structure.
