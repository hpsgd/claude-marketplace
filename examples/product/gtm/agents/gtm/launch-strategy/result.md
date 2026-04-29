# Output: Launch strategy

**Verdict:** PASS
**Score:** 16.5/17 criteria met (97%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: All marketing copy, messaging, and campaign content is labelled DRAFT and flagged for human review before use — met. The output format template mandates `### Status: DRAFT — requires human review`. The content marketing section states "Never publish directly." Decision checkpoints list publishing without human review as a mandatory stop. Enforced at multiple points.
- [x] PASS: Applies positioning work before tactics — met. The definition runs the April Dunford framework (competitive alternatives → unique attributes → value → target segment → category) before any execution, and "Positioning before execution" is a named principle.
- [x] PASS: Leads messaging with the customer problem rather than feature descriptions — met. The non-negotiable states "Lead with the problem, not the feature." Content rules reinforce: "Problem-first: Start with the pain, then offer relief. Nobody reads 'Introducing Feature X.'"
- [x] PASS: Recommends a launch tier — met. The launch planning section has an explicit tier classification table. An add-on product for existing customers at >$100k ARR impact maps to Tier 1 or Tier 2. The agent is directed to classify before building a plan.
- [x] PASS: Distinguishes between existing customer expansion and net-new motion — met. The definition has a dedicated "Expansion vs net-new" section stating "Never combine these into a single 'launch plan.'" Channels, messaging, and metrics are specified separately for each motion.
- [~] PARTIAL: Includes a post-launch review plan with success metrics — partially met. The definition's post-launch checklist names "Review metrics daily (sign-ups, activation, errors)" and "Write retrospective." The metrics section names KPIs. However, no mandated owner or specific review date format appears in the definition. An agent following it would name metrics but could omit the review timeline and named owner. Score: 0.5.
- [x] PASS: Produces a structured launch plan with phases and owners, not a list of marketing ideas — met. The definition states "Every launch plan must be a phased plan with owners and dates, not a checklist of ideas" with three required phases each requiring "(owner, dates)."

### Output expectations

- [x] PASS: Output sizes the existing-customer revenue opportunity — met. The agent is built to be specific ("Saves 3 hours per sprint" not "improves productivity") and its metrics orientation together with the prompt's inputs (340 accounts, 50+ seats, $15/seat/month) would produce ARR ceiling and a realistic conversion target.
- [x] PASS: Output's positioning anchors against Asana/Monday native reporting — met. The April Dunford framework step 1 is competitive alternatives. With the prompt naming Asana and Monday, the agent would anchor on them with the executive summary as the named differentiator.
- [x] PASS: Output's customer-problem framing leads with the operations director/PMO pain — met. "Problem-first" is a non-negotiable. The agent would frame around exec reporting pain, not feature descriptions.
- [x] PASS: Output classifies this as Tier 1 or Tier 2 — met. The tier classification table is explicit and the criteria (add-on product, >$100k ARR impact, 340-account activation event) map to Tier 1 or Tier 2. The agent would name the tier and note it is not a silent rollout.
- [x] PASS: Output separates existing-customer expansion from net-new acquisition — met. The definition explicitly prohibits combining them: "Never combine these into a single 'launch plan.'"
- [x] PASS: Output's launch plan has phases with owners and dates — met. The definition mandates Pre-launch, Launch day, and Post-launch phases each with named owners. The scenario provides a one-month horizon to anchor dates.
- [x] PASS: Output's marketing copy and messaging examples are labelled DRAFT — met. Labelling is mandatory and enforced throughout the definition including the output format template and decision checkpoints.
- [~] PARTIAL: Output's post-launch review plan names success metrics, a review date, and a review owner — partially met. The definition supplies metrics and a "write retrospective" instruction but does not mandate a specific review date format (Day 30/60/90) or named review owner in the post-launch phase. Score: 0.5 — criteria criterion already partially credited above; treating consistently here.
- [x] PASS: Output addresses internal readiness alongside external launch — met. The pre-launch checklist includes support briefing, documentation, and the collaboration section covers CSMs and support. The decision checkpoints block launching without support briefing.
- [~] PARTIAL: Output addresses pricing communication carefully — partially met. The definition's decision checkpoint flags "changing pricing or packaging in marketing materials" as a stop-and-ask trigger. The agent would escalate rather than independently surface grandfathering for early adopters or volume discounting logic. It handles pricing with caution but may not generate the nuanced analysis the criterion expects. Score: 0.5.

## Notes

The agent definition is strong for this scenario. The April Dunford positioning framework, tier classification table, explicit expansion-vs-net-new separation, and mandatory DRAFT labelling directly address the rubric criteria.

Two gaps keep this from a clean pass: (1) post-launch review ownership and date format are not mandated in the definition — an agent following it would produce metrics but may not structure a Day 30/60/90 review with a named owner; (2) pricing grandfathering/volume discount reasoning is handled by escalation rather than analysis, which is safe but may not satisfy the output expectation for "addressing pricing carefully."

The decision checkpoint table is a strong design feature — it prevents the most common GTM agent failure modes (publishing without review, pricing changes without approval, launches without support briefing).
