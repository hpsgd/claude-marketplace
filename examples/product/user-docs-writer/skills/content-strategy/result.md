# Output: Content strategy

**Verdict:** PARTIAL
**Score:** 14/18 criteria met (78%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill uses the Diataxis framework — opens with "Define a documentation content strategy for $ARGUMENTS using the Diataxis framework" and applies Tutorial/How-to/Reference/Explanation across all six steps.
- [x] PASS: Skill requires a content inventory step before any recommendations — Step 1 "Inventory Existing Content" is mandatory first, scanning all docs before any subsequent step executes.
- [x] PASS: Skill produces a gap analysis — Step 3 has three structured tables: missing content, stale content, and orphaned content, plus a common gap patterns table.
- [x] PASS: Skill produces a prioritised content roadmap — Step 4 ranks gaps using P0/P1/P2 with explicit prioritisation criteria (user traffic, onboarding path, support ticket volume, etc.), and Step 6 synthesises into a phased roadmap.
- [x] PASS: Skill defines content standards — Step 5 has a standards table (style guide, review process, freshness policy, ownership model, templates, testing, versioning) plus a per-quadrant standards table with structure, length, and must-include elements.
- [x] PASS: Skill requires a coverage matrix — Step 2 requires a feature-by-quadrant matrix showing Yes/No/Stale for every feature-quadrant combination, plus a coverage summary by quadrant.
- [~] PARTIAL: Skill addresses content maintenance — Step 6 mandates an "Ongoing: Maintenance" section with monthly freshness review, feature-change trigger, quarterly coverage audit, and support ticket review. Substantive coverage, not a passing mention. Criterion is PARTIAL-prefixed, so capped at 0.5.
- [x] PASS: Skill has valid YAML frontmatter with `name: content-strategy`, `description`, and `argument-hint` fields, all populated.

### Output expectations

- [x] PASS: Output's content inventory step processes all existing articles — Step 1 instructs scanning ALL documentation files ("categorise every piece") with quadrant classification and a Status column (Current/Stale/Orphaned), covering the full set not a sample.
- [x] PASS: Output uses Diataxis taxonomy explicitly — framework is named in the opening sentence, and the four types are defined with purpose/orientation/user-need in a definitions table in Step 1.
- [x] PASS: Output's gap analysis identifies what's missing per product area concretely — Step 3's "Missing content" table has Feature + Missing quadrant(s) + Impact columns, requiring specific feature-level identification, not generic statements.
- [ ] FAIL: Output's coverage matrix maps content to user tasks — the matrix in Step 2 uses Feature/Area as rows, not user tasks ("export a report", "invite a teammate"). The test requires task-level rows; the skill uses feature-area rows. The two are not equivalent: a feature area may have docs but still leave specific user tasks uncovered.
- [~] PARTIAL: Output addresses the support-ticket signal — support ticket volume is a named prioritisation factor in Step 4, and support ticket review appears in the maintenance schedule. However the skill does not explicitly distinguish between "content exists but users can't find it" (findability gap) versus "content genuinely doesn't exist" (coverage gap), which the prompt scenario specifically raises.
- [x] PASS: Output's roadmap is prioritised with top items being support deflection wins or gaps blocking key user tasks — P0 is explicitly defined as "blocks user onboarding or generates frequent support tickets."
- [x] PASS: Output's content standards define what GOOD looks like per Diataxis type with actionable specifics — Per-Quadrant Standards table in Step 5 specifies structure, length, and must-include elements for each of the four quadrant types (e.g. "How-to: numbered steps, minimal explanation, 2-5 minutes to read, goal in title, prerequisites, single outcome").
- [~] PARTIAL: Output's recommendations distinguish between rewrite, retire, and create — the skill uses Stale (implies rewrite), Orphaned (implies retire), and Missing (implies create) as gap categories, but never frames these as explicit action types. A writer working from the skill could infer the right action, but it is not stated.
- [x] PASS: Output addresses content maintenance as a strategic component — Step 5 mandates a freshness policy and ownership model; Step 6's maintenance section requires monthly review, feature-change trigger, quarterly audit, and support ticket review with a cadence.
- [ ] FAIL: Output addresses the IA/findability dimension — no mention of search, navigation hierarchy, tagging, or findability anywhere in the skill. The scenario explicitly involves users being unable to find answers, making this a meaningful gap in the strategy definition.

## Notes

The skill is well-structured and strong on Diataxis application throughout. The main structural gaps are:

The coverage matrix uses feature areas as rows rather than user tasks. Feature-area coverage and task-level coverage are different things — a feature can have docs in all four quadrants and still leave the specific task "export a report" without a how-to. The test's expectation of task-level rows is deliberate and the skill doesn't meet it.

The findability gap is a real weakness. The prompt scenario describes users who "can't find answers to common questions" — this is explicitly a findability problem, not just a coverage problem. The skill has no step, output section, or rule addressing search, IA, navigation, or tagging. A content strategy for a 140-article help centre with findability complaints should address this.

The rewrite/retire/create framing is implied by the gap categories but not made explicit. Writers working from this skill would need to infer the action from the gap type.
