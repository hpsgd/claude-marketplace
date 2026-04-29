# Result: Write QBR

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 16 / 18 criteria met (89%) |
| **Evaluated** | 2026-04-29 |
| **Skill source** | `plugins/product/customer-success/skills/write-qbr/SKILL.md` |

## Results

### Criteria

- [x] PASS: Skill requires a data gathering step before writing — met. Step 1 explicitly gates all writing behind collecting health score, usage metrics, support history, prior QBR goals, commercial context, and relationship signals. The rule "do not fabricate metrics" enforces the gate.

- [x] PASS: Skill documents value delivered in customer outcome terms — met. Step 2 value narrative instructs translating raw metrics into business language. The worked example ("Your team resolved 40% more support tickets" vs "Automation workflow usage increased 40%") is concrete. Rules state: "Tie metrics to their goals, not ours."

- [x] PASS: Skill includes a forward-looking section — met. Step 3 has "Strategic recommendations" for next quarter. Step 4 template includes a "Recommendations for Next Quarter" section with a Goals table carrying metric, target, owner, and timeline columns.

- [x] PASS: Skill identifies risks and open issues — met. Step 3 has a Risks table with severity, evidence, and recommended action columns. Rules state: "Hiding problems from the customer destroys trust. Acknowledging them with a remediation plan builds it."

- [x] PASS: Skill produces a structured QBR document with distinct sections — met. Step 4 template includes Executive Summary, Value Delivered This Quarter, Challenges and Lessons Learned, Health Overview, Recommendations for Next Quarter, and Appendix. All four required section types are present.

- [~] PARTIAL: Skill includes expansion or growth conversation guidance conditioned on account health — fully met within the PARTIAL cap. Step 3 includes an Expansion Opportunities table, and the rules explicitly state: "Do not propose expansion to unhealthy accounts. If the customer is At Risk or Critical, the QBR should focus on stabilisation, not upselling." Score: 0.5.

- [x] PASS: Skill requires next steps with owners and dates — met. The Goals table in Step 4 template has Owner and Timeline columns. Strategic Recommendations must each be "Owned" and "Time-bound" per the rules. The rules also state: "Track commitments both ways."

- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — met. Lines 1–7 contain `name: write-qbr`, `description: "Prepare a Quarterly Business Review..."`, and `argument-hint: "[customer name or account to prepare QBR for]"`.

### Output expectations

- [x] PASS: Output's data gathering step lists specific data sources for Landermere — met. Step 1 covers all six dimensions (health score, usage metrics, support history, prior-QBR goals, commercial context including ARR and renewal date, relationship signals) that apply directly to the Landermere scenario.

- [x] PASS: Output's value-delivered section uses customer-outcome language — met. The worked example in Step 2 ("Your team resolved 40% more support tickets this quarter" vs "Automation workflow usage increased 40%") establishes this standard explicitly.

- [x] PASS: Output's value section quantifies outcomes with before/after metrics — met. Rules in Step 2 state: "Quantify everything. 'Your team saved approximately 120 hours this quarter' not 'Your team saved a lot of time.'" Before/after framing is enforced by the quantity rule.

- [x] PASS: Output's forward-looking section sets at least 2-3 specific measurable goals — met. Step 4 template Goals table requires metric, target, owner, and timeline per goal. Step 3 requires 3-5 strategic recommendations, each specific and time-bound.

- [x] PASS: Output's risks/issues section is honest about deteriorating signals — met. Risks table captures underutilised features, support patterns, relationship gaps, and renewal concerns with severity and evidence. Rules reinforce honesty.

- [x] PASS: Output's structure follows the named sections — met. Value Delivered, Health Overview, Challenges (mapping to Risks), Recommendations for Next Quarter are all named sections in the Step 4 template.

- [x] PASS: Output's expansion/growth guidance is conditional on health — met. Rules are explicit: "Do not propose expansion to unhealthy accounts." The conditioning is enforced in the rules section, not just implied.

- [x] PASS: Output's next steps each have an owner and a date, at least 3 — met. Goals table has Owner and Timeline columns. Strategic Recommendations requires 3-5 items, each owned and time-bound. Rules reinforce: "Track commitments both ways."

- [ ] FAIL: Output's deck outline is structured for a meeting (10-15 slides) with talking points per slide — not met. The skill produces a markdown document with sections, not a slide deck outline. No mention of slide count, no per-slide talking points. The prompt explicitly asked for "the QBR deck outline and talking points for the meeting" — the skill's output format does not match this presentation-layer requirement.

- [~] PARTIAL: Output addresses 18-month tenure context — partially met. The skill captures tenure as part of commercial context in Step 1, and the Expansion Opportunities table may reflect tenure signals. However, the skill has no explicit guidance on year-2 value-articulation (past the first-year wow factor, emphasising depth of use and ROI realisation rather than feature adoption). Score: 0.5.

## Notes

The skill's core structure is solid — data-gathering gate, customer-outcome framing, honest risk handling, and health-conditioned expansion are all implemented well. The gap that matters most for this prompt is the output format: the user asked for a deck outline with talking points per slide, and the skill produces a markdown document. A well-formed QBR skill for a CS context should offer both a full document and a presentation-ready outline. That is a meaningful absence, not a minor gap.

The 18-month tenure gap is softer — the skill would produce a competent QBR for Landermere, but it misses the nuance that year-2 customers need value articulated differently than year-1 customers. Adding a tenure-stage consideration to Step 1 (e.g., "note whether this is a first, second, or third QBR and adjust value framing accordingly") would close this.
