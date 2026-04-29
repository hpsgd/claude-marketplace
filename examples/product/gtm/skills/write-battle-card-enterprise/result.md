# Output: write-battle-card — enterprise deal with multiple buyer personas

**Verdict:** PARTIAL
**Score:** 15.5/18 criteria met (86.1%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Objection handling is segmented by buyer persona (CFO, VP Eng, sales reps) not generic — Step 3 includes an explicit "For enterprise deals with multiple buyer personas" block defining three named segments: Economic buyer (CFO/VP Finance), Technical buyer (VP Eng/CTO), and End user. Step 5's template requires all three as separate objection tables for enterprise deals.

- [x] PASS: Win/lose analysis is based on specific evidence not generic claims — Step 2 rules state: "Be specific. 'Better UX' is not a win. 'Onboarding takes 5 minutes vs. their 2-hour setup' is a win." Also: "Quantify where possible. Numbers beat adjectives." The global sourcing rule enforces: "Every claim must have a source. If you cannot verify it, mark it as 'Unverified — needs confirmation'."

- [x] PASS: TCO comparison includes specific line items (licence, implementation, training, ongoing admin) not just "we're cheaper" — Step 3 states: "When the competitor is an established platform (Salesforce, HubSpot, etc.), include a TCO breakdown with specific line items: licence cost per seat, implementation/migration cost, training, ongoing admin overhead, and integration maintenance." Five named line items required.

- [~] PARTIAL: Technical differentiators are stated with specificity (API rate limits, migration tooling, specific integrations) — The general rules in Step 2 require specificity and quantification across all dimensions. However, the skill has no targeted instruction requiring the technical buyer section to address API rate limits, migration tooling depth, or SDK/webhook specifics by name. The "be specific" rule is the only lever — partially met.

- [x] PASS: The card is concise enough for a sales rep to scan in 30 seconds — Rules section states: "If a rep can't scan the card and find what they need in 30 seconds, the card is too long. Prefer tables and bullets over paragraphs." Explicitly required.

- [~] PARTIAL: Proof points (case studies, benchmarks) are current and specific to the enterprise segment — Step 5 states: "Proof points must match the deal segment. An SMB case study doesn't carry weight in an enterprise deal. Tag each proof point with the segment it applies to." Currency is addressed in Rules: "Proof points must be current." Both aspects explicitly covered. PARTIAL-prefixed criterion — scored 0.5.

- [x] PASS: Output is labelled DRAFT and flagged for human review — Rules section states: "All output is DRAFT until human-reviewed. Label every output with 'DRAFT — requires human review' at the top and bottom." Explicit and required.

- [x] PASS: The card covers one competitor (Salesforce) only, not a multi-competitor overview — Rules section states: "One competitor per card. Do not combine multiple competitors into a single card. Each card is a focused reference for a specific competitive deal." Explicit.

### Output expectations

- [x] PASS: Output's objection / response pairs are segmented into three sections by buyer persona — the skill template in Step 5 explicitly defines three separate persona-segmented objection tables (Economic Buyer / Technical Buyer / End User), with column headers Objection, Response, Proof. The enterprise routing logic in Step 3 instructs the agent to use this structure for multi-persona deals.

- [~] PARTIAL: Output's TCO comparison shows specific line items per option — Step 3 names five line items (licence, implementation/migration, training, ongoing admin, integration maintenance) and requires them for established platforms like Salesforce. However, the skill does not instruct the agent to show both sides (our product vs. Salesforce) in a parallel two-column shape, nor does it require a 3-year total rollup or per-seat breakdowns at a specific seat count. The requirement is structurally present but not shaped to the depth this criterion demands.

- [~] PARTIAL: Output's technical-buyer differentiators are specific — API rate limits, migration tooling, specific pre-built integrations named — the skill requires specificity and quantification generally, and includes an integration row in the Quick Comparison table. But it never instructs the agent to address API rate limits, migration tooling by name, or specific integration partners (Slack, MS Teams, named ERPs) for the technical buyer section. The general rule is the only lever; specific categories for this persona are absent.

- [ ] FAIL: Output's end-user differentiators are concrete — mobile app load time, offline capability, UX patterns with benchmarks — the skill has no specific instruction to address mobile UX, load time metrics, offline capability, or gesture-based UX patterns for the end-user section. The "be specific" general rule applies, but mobile-specific differentiators for the sales rep persona are not called out anywhere in the definition.

- [~] PARTIAL: Output's win/loss analysis is grounded in evidence — references deal post-mortems, win-rate statistics, or feature-gap data — Step 1 instructs: "Search for deal retrospectives, CRM notes, or customer feedback that mentions this competitor." Step 2 requires evidence for each win/lose cell. The mechanism exists, but the skill does not require specific evidence types (post-mortems, win-rate %) to be cited; it relies on whatever is found during research. Partially met.

- [x] PASS: Output is concise enough for a sales rep to scan in 30 seconds — explicitly required in Rules: "If a rep can't scan the card and find what they need in 30 seconds, the card is too long. Prefer tables and bullets over paragraphs." The template enforces tables and bullets throughout.

- [~] PARTIAL: Output includes proof points specific to the enterprise segment — case studies of 500+ seat customers with named or anonymised revenue/time-savings outcomes — Step 5 requires segment-tagged proof points: "Proof points must match the deal segment. An SMB case study doesn't carry weight in an enterprise deal." However, the skill does not require the agent to actively seek or flag absence of enterprise-specific case studies involving large seat counts, or to require named outcomes (revenue, time-savings). The segment-tagging instruction is present; the specificity depth required by this criterion is not.

- [x] PASS: Output covers only Salesforce — the one-competitor rule is explicit: "One competitor per card. Do not combine multiple competitors into a single card."

- [x] PASS: Output is labelled DRAFT — Rules section requires "DRAFT — requires human review" at the top and bottom. Explicit.

- [~] PARTIAL: Output addresses multi-stakeholder deal dynamics — what to do when CFO, VP Eng, and rep have conflicting priorities — the skill structures each persona's objections separately but includes no instruction about sequencing across personas, resolving conflicting priorities, or coaching on message ordering when stakeholder interests diverge. The segmentation exists; the deal-dynamics guidance does not. PARTIAL-prefixed criterion — scored 0.5.

## Notes

The skill handles the structural requirements of the enterprise scenario well. Persona-segmented objections, TCO line items, DRAFT labelling, and the one-competitor rule are all explicit. A well-formed agent following this skill would produce a card meeting those criteria reliably.

The gaps cluster in output depth rather than output structure. The skill's "be specific" general rule is doing heavy lifting in places where targeted instructions per persona would produce more consistent results. The technical buyer section has no explicit requirements for API rate limits or migration tooling. The end-user section has no explicit requirements for mobile metrics. Win/loss evidence is required but not typed (no requirement to surface post-mortem data or win-rate statistics specifically). The multi-stakeholder deal-dynamics gap is the largest structural absence — the skill segments personas but does not coach on how to sequence or reconcile conflicting buyer signals.
