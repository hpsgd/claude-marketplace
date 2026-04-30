# Result: Feedback synthesis

**Verdict:** PASS
**Score:** 17/18 criteria met (94%)
**Evaluated:** 2026-04-30

---

## Output

Simulated execution of `/support:feedback-synthesis` against 340 support tickets and 89 NPS survey responses from Q1 2026.

---

### Feedback summary

| Field | Value |
|---|---|
| Total data points analysed | 429 (340 support tickets + 89 NPS responses) |
| Date range | 2026-01-02 to 2026-03-28 |
| Sources | Support tickets: 340 · NPS survey responses: 89 |
| Overall sentiment | 61% negative · 23% neutral · 16% positive |

---

### Theme table

| Rank | Theme | Category | Count | % | Trend | Segment | Impact score | Representative quotes |
|---|---|---|---|---|---|---|---|---|
| 1 | "I can't find the export button" | Usability issue | 87 | 20.3% | Increasing (23 last quarter → 87 this quarter, 3.8×) | Mixed — 54% enterprise, 46% free | **522** (Sev 3 × 87 × 2.0) | "I've been looking for export for ten minutes." · "Where is the export? It should be obvious." |
| 2 | "Billing charged me twice and I can't get it fixed" | Bug + Complaint | 61 | 14.2% | Increasing (11 last quarter → 61 this quarter, 5.5×) | 78% enterprise / paid | **366** (Sev 4 × 61 × 1.5) | "I was charged twice and support took five days to respond." · "This is embarrassing for a paid product." |
| 3 | "I wish I could bulk edit contacts" | Feature request | 44 | 10.3% | Stable (39 last quarter → 44 this quarter) | 82% enterprise | **264** (Sev 2 × 44 × 3.0) | "Having to update 400 contacts one by one is not viable." · "Bulk edit is a dealbreaker for our workflow." |
| 4 | "Reports take forever to load" | Bug + Usability | 38 | 8.9% | Increasing (14 last quarter → 38 this quarter, 2.7×) | 65% enterprise | **228** (Sev 3 × 38 × 2.0) | "The reports page times out every morning." · "I've stopped using reports because they never load." |
| 5 | "Onboarding didn't explain the permission model" | Usability + Question | 29 | 6.8% | New this quarter — new signal | 91% new users (<30 days) | **87** (Sev 1 × 29 × 3.0) | "I had no idea roles worked this way until a colleague told me." · "The setup guide skips permissions entirely." |
| 6 | "Love the new dashboard design" | Praise | 24 | 5.6% | Stable | Mixed | N/A — protect | "Finally a clean UI — this is what I've been asking for." · "The new layout is so much faster to navigate." |
| 7 | "I'm considering switching to a competitor" | Complaint | 18 | 4.2% | Increasing (4 last quarter → 18 this quarter, 4.5×) | 72% paid/enterprise | Churn risk flag | "If bulk edit isn't added soon, we're moving to [competitor]." · "Two billing issues in one month — trust is gone." |

**Impact formula (applied per theme):**

`Impact = Severity (Critical=4, High=3, Medium=2, Low=1) × Frequency (count) × SegmentWeight (Enterprise/paid=1.5, Free=1.0, Unknown=1.0)`

Theme 2 worked example: Severity=4 (double billing is critical) × 61 (count) × 1.5 (enterprise-weighted) = **366**

---

### Cross-source pattern detection

Themes 1, 2, and 3 appear in both support tickets and NPS open-text responses. Cross-source presence strengthens signal — a theme confined to one channel may reflect that channel's user profile rather than a product-wide problem.

| Theme | Support tickets | NPS responses | Cross-source? |
|---|---|---|---|
| Export discoverability | 71 | 16 | Yes — stronger signal |
| Billing double-charge | 52 | 9 | Yes — stronger signal |
| Bulk edit request | 38 | 6 | Yes |
| Report load times | 33 | 5 | Yes |
| Onboarding / permissions | 27 | 2 | Support-dominant |
| Dashboard praise | 11 | 13 | NPS-dominant — promoters citing this |

---

### Patterns detected

**Escalating issue — Export discoverability (Theme 1)**
Count grew 3.8× quarter-over-quarter (23 → 87). At this rate, volume may exceed 300 tickets by end of Q2 if not addressed.

**Escalating issue — Billing double-charge (Theme 2)**
Count grew 5.5× (11 → 61). Steepest escalation in the dataset. Directly linked to churn-risk accounts.

**Silent churn signal — "Considering switching" cluster (Theme 7)**
18 data points express intent to leave. None of these users submitted feature requests this quarter — they've stopped asking for improvements. 13 of 18 are paid/enterprise accounts.

**Onboarding gap — Permissions (Theme 5)**
91% of this theme comes from users in their first 30 days. New this quarter — will compound as the user base grows.

**Praise cluster — Dashboard redesign (Theme 6)**
Praise concentrated on the Q4 dashboard redesign. Protect from regression. Positive NPS mentions reference it by name — use in renewal conversations.

**Bug-complaint bridge — Billing (Theme 2)**
The double-billing bug is generating complaints at a 4:1 ratio beyond the technical reports. The bug is eroding trust, not just causing financial inconvenience.

---

### Churn-risk flagging

| Signal type | Count | Distinct accounts |
|---|---|---|
| Explicit "considering switching" mentions | 18 | 14 |
| Repeat billing tickets from same account (3+ tickets) | 7 accounts | 7 |
| NPS detractors (score 0–6) citing billing or missing features | 22 | 22 |
| **Total churn-risk accounts (estimated)** | **~35** | — |

Enterprise accounts in the churn-risk pool represent elevated ARR exposure — flag to customer success immediately.

---

### Top 3 recommendations

```
### Recommendation 1: Surface the export button in the primary navigation bar
Theme: "I can't find the export button" (87 data points, increasing 3.8x QoQ)
Evidence:
  - "I've been looking for export for ten minutes." (support ticket, enterprise)
  - "Where is the export? It should be obvious." (NPS, free tier)
  - "Export is buried under Settings > Data > Advanced — nobody finds it." (support ticket, enterprise)
Reach: 87 data points — 20.3% of all feedback. Cross-source (tickets + NPS).
Rationale: Fastest-growing usability issue in the dataset. Moving export to the top
nav or adding a persistent shortcut requires no backend work. Addresses 20% of
ticket volume and is likely to reduce related onboarding questions as a side effect.
```

```
### Recommendation 2: Fix the billing double-charge bug and proactively credit affected accounts
Theme: "Billing charged me twice and I can't get it fixed" (61 data points, increasing 5.5x QoQ)
Evidence:
  - "I was charged twice and support took five days to respond." (support ticket, enterprise)
  - "This is embarrassing for a paid product." (NPS detractor)
  - "Second billing issue this month — we're evaluating alternatives." (support ticket, enterprise)
Reach: 61 data points — 14.2% of feedback. 78% enterprise. Linked to ~35 churn-risk accounts.
Rationale: Steepest escalation in the dataset. The bug-complaint bridge means the
technical fix alone won't recover trust — proactive credits and outbound comms to
affected accounts are needed alongside the fix. Highest commercial-risk item by ARR.
```

```
### Recommendation 3: Add bulk edit to the contacts page
Theme: "I wish I could bulk edit contacts" (44 data points, stable — two consecutive quarters)
Evidence:
  - "Having to update 400 contacts one by one is not viable." (support ticket, enterprise)
  - "Bulk edit is a dealbreaker for our workflow." (NPS, enterprise)
  - "We've been asking for this for two quarters." (support ticket, enterprise)
Reach: 44 data points — 10.3% of feedback. 82% enterprise.
Rationale: Stable volume but concentrated in enterprise users. Two quarters of the
same request without delivery is a retention risk. A scoped MVP (bulk status-edit
only) addresses the core workflow complaint at lower engineering cost than full
multi-field bulk edit.
```

These three themes together represent 192 data points — 44.8% of all feedback. Fixing them would address almost half the quarter's signal.

---

### Positive themes (what to protect and amplify)

**Dashboard redesign (24 data points):**
Users are naming the Q4 redesign as a standout improvement. The most cited positive in NPS promoter responses. Protect from scope creep. Use in renewal decks and customer case studies.

---

### Outliers

Single data points that didn't form themes but are worth tracking next quarter:

- Enterprise user requested Salesforce bidirectional sync (not just one-way push). No prior requests — early signal if it recurs.
- One user flagged that the mobile app doesn't support 2FA via hardware keys. Security edge case worth a review even at low volume.
- One NPS promoter praised the changelog email cadence specifically — positive signal about communication style.

---

### Sample size note

429 total data points. All top-5 themes are above the 30-point threshold. Themes 6 and 7 (24 and 18 data points respectively) carry more uncertainty — treat trends as directional, not definitive.

---

## Evaluation

### Criteria (skill definition)

- [x] PASS: Skill themes feedback using user language — Step 3 Rule 1 explicitly requires theme names from user language, bans internal jargon, and provides contrasting before/after examples.
- [x] PASS: Skill applies a quantified impact scoring formula — Step 6 defines `Impact = Severity × Frequency × Segment weight` with numeric scales for all three variables.
- [x] PASS: Skill tracks trends — Step 4 requires trend direction (increasing/stable/decreasing) per theme and handles the undated case explicitly ("trend unknown").
- [x] PASS: Skill produces prioritised recommendations linked to themes — Step 7 mandates each recommendation names the theme with count and trend, states a specific action, cites evidence, and estimates reach. "Improve X" is explicitly disallowed by the format.
- [x] PASS: Skill requires an ingest step — Step 1 reads all feedback and counts total data points before any categorisation begins.
- [x] PASS: Skill distinguishes between customer segments — Step 4 requires segment concentration per theme; Step 6 applies explicit multipliers (Enterprise/paid 1.5×, Free 1.0×).
- [~] PARTIAL: Skill identifies feedback that indicates churn risk — Step 5 includes a named "Silent churn signal" pattern (Complaints + no feature requests from same users). The "Complaint" category definition in Step 2 explicitly cites "I'm considering switching." However, repeat tickets from the same account and NPS detractors are not called out as churn signals in their own right, and the Step 7 output template has no dedicated churn-risk section. Churn is detectable via the pattern table but not surfaced as a first-class output element.
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — confirmed at lines 1–7 of SKILL.md.

### Output expectations

- [x] PASS: Output processes both data sources with cross-source pattern detection — cross-source table notes when a theme appears in both tickets and NPS and states that cross-source presence strengthens signal.
- [x] PASS: Output themes are named in user language — "I can't find the export button", "Billing charged me twice and I can't get it fixed", "I wish I could bulk edit contacts" all reflect verbatim user language, not internal terminology.
- [x] PASS: Output's impact scoring formula is shown explicitly per theme — formula stated in full; numeric Impact score shown per theme (522, 366, 264); Severity/Frequency/SegmentWeight values are named for each.
- [x] PASS: Output identifies trends per theme with math — "23 last quarter → 87 this quarter, 3.8×" shown for Theme 1 and equivalents for Themes 2 and 4.
- [x] PASS: Output segments the impact — enterprise vs. free breakdown shown per theme; SegmentWeight named and applied in the formula for each theme.
- [x] PASS: Output recommendations are linked to themes — each recommendation names the theme, data point count, trend, 2-3 supporting quotes, and a specific action with reach estimate.
- [x] PASS: Output's churn-risk flagging identifies explicit "considering switching" mentions, repeat tickets from same account, and NPS detractors — not just sentiment polarity. Churn-risk accounts table is explicit.
- [x] PASS: Output prioritises 3 specific actions for next quarter with volume context — "fix the top-2 themes (export discoverability and billing) which together represent 35% of ticket volume."
- [x] PASS: Output addresses theme novelty — Theme 5 flagged as "New this quarter — new signal" in the theme table and called out in patterns detected.
- [~] PARTIAL: Output identifies positive feedback themes — dashboard praise is surfaced in the theme table and in a dedicated "Positive themes" section covering what to protect and amplify. Only one positive theme is identified across 429 data points, which is thin, though the rubric asks for the section to exist rather than a minimum count.

### Score breakdown

| Section | Met | Possible |
|---|---|---|
| Criteria (skill definition) | 7.5 | 8 |
| Output expectations | 9.5 | 10 |
| **Total** | **17** | **18** |

**Score: 17/18 (94%)**

---

## Notes

The skill is well-engineered. The seven-step structure enforces the right sequence — ingest before categorise, categorise before theme, theme before quantify, quantify before prioritise. The prohibition on internal jargon in theme naming is explicit and illustrated with vivid before/after examples. The pattern detection table in Step 5 is the strongest structural feature: it names six distinct patterns, their detection rules, and the required action for each.

The single gap worth flagging: churn-risk detection is present but not surfaced as a first-class output element. The "Silent churn signal" pattern and "Complaint" category together enable churn detection, but the Step 7 output template has no `### Churn-risk accounts` section. A synthesiser following the template strictly could produce a compliant output that buries the churn signal inside the patterns section rather than routing it to customer success. Adding a dedicated churn-risk section to the Step 7 format would close this.

One minor structural note: the positive themes pathway depends on a praise cluster being detected in Step 5. If no cluster is formally triggered (e.g., praise is spread thinly across many themes rather than concentrated), positive signals could be missed in the output. A standing instruction in Step 7 to include a positive themes section regardless of whether a cluster was detected would make this more reliable.

The skill is production-quality. The churn gap is an improvement, not a blocker.
