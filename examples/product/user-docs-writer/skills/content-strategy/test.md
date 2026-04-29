# Test: Content strategy

Scenario: Testing whether the content-strategy skill uses the Diataxis framework, requires a content inventory, and produces a prioritised content roadmap.

## Prompt


/user-docs-writer:content-strategy for our help centre — we have 140 articles written over 3 years, significant product changes since most were written, and support tickets suggesting users can't find answers to common questions.

## Criteria


- [ ] PASS: Skill uses the Diataxis framework — classifying content as Tutorial, How-to, Reference, or Explanation — not an ad-hoc taxonomy
- [ ] PASS: Skill requires a content inventory step before any recommendations — auditing what exists before deciding what to create
- [ ] PASS: Skill produces a gap analysis — identifying what content types are missing or underrepresented for each product area
- [ ] PASS: Skill produces a prioritised content roadmap — what to create first, with rationale based on user impact
- [ ] PASS: Skill defines content standards — what good looks like for each content type in this context
- [ ] PASS: Skill requires a coverage matrix — mapping content to user tasks to identify blind spots
- [ ] PARTIAL: Skill addresses content maintenance — how to keep existing content current as the product evolves — partial credit if this is mentioned but not required as a strategy component
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output's content inventory step processes the 140 existing articles — at minimum classifying each into one of the four Diataxis types and flagging stale articles (last reviewed > 6 months without product change) — not a sample
- [ ] PASS: Output uses the Diataxis taxonomy explicitly — Tutorial (learning-oriented), How-to (task-oriented), Reference (information-oriented), Explanation (understanding-oriented) — with the framework named, not invented categories
- [ ] PASS: Output's gap analysis identifies what's missing per product area — e.g. "Reporting has 8 How-tos but 0 Tutorials, suggesting new users have nowhere to start" — concrete, not generic "we need more content"
- [ ] PASS: Output's coverage matrix maps content to user tasks — rows are user tasks ("export a report", "invite a teammate"), columns are Diataxis types — with cells showing the article(s) that cover each, blanks revealing gaps
- [ ] PASS: Output addresses the support-ticket signal — common questions where users couldn't find answers should be cross-referenced with the inventory to identify content that exists but isn't findable, vs content that's genuinely missing
- [ ] PASS: Output's roadmap is prioritised — with the top items being either (a) high-frequency support deflection wins or (b) gaps blocking key user tasks — not arbitrary "let's update the docs"
- [ ] PASS: Output's content standards define what GOOD looks like per Diataxis type — e.g. "How-tos must have numbered steps with expected results", "Reference must be exhaustive and machine-scannable" — actionable for writers
- [ ] PASS: Output's recommendations distinguish between rewrite (article exists but is stale or wrong type), retire (no longer relevant), and create (genuine gap) — and the inventory feeds these decisions
- [ ] PASS: Output addresses content maintenance as a strategic component — review cadence (e.g. every 6 months), trigger-based update (after a product release in the same area), and content owner per article
- [ ] PARTIAL: Output addresses the IA / findability dimension — even good content fails if users can't find it; recommendations on search, navigation hierarchy, and tagging belong in the strategy
