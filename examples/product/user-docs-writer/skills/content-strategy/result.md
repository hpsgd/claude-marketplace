# Output: Content strategy

**Verdict:** PARTIAL
**Score:** 17.5/18 criteria met (97%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill uses the Diataxis framework — opens with "Define a documentation content strategy for $ARGUMENTS using the Diataxis framework" and applies Tutorial/How-to/Reference/Explanation across all six steps.
- [x] PASS: Skill requires a content inventory step before any recommendations — Step 1 "Inventory Existing Content" is mandatory first, scanning all docs before any subsequent step executes.
- [x] PASS: Skill produces a gap analysis — Step 3 has four structured tables: missing content (create), stale content (rewrite), orphaned content (retire), and findability gaps (fix IA), plus a common gap patterns table.
- [x] PASS: Skill produces a prioritised content roadmap — Step 4 ranks gaps using P0/P1/P2 with explicit prioritisation criteria (user traffic, onboarding path, support ticket volume, etc.), and Step 6 synthesises into a phased roadmap.
- [x] PASS: Skill defines content standards — Step 5 has a standards table (style guide, review process, freshness policy, ownership model, templates, testing, versioning) plus a per-quadrant standards table with structure, length, and must-include elements.
- [x] PASS: Skill requires a coverage matrix — Step 2 explicitly specifies user tasks as rows (not feature areas), with worked examples ("export a report", "invite a teammate"), plus a quadrant summary table.
- [~] PARTIAL: Skill addresses content maintenance — Step 6 mandates an "Ongoing: Maintenance" section with monthly freshness review, feature-change trigger, quarterly coverage audit, and support ticket review. Substantive coverage, not a passing mention. Criterion is PARTIAL-prefixed, so capped at 0.5.
- [x] PASS: Skill has valid YAML frontmatter with `name: content-strategy`, `description`, and `argument-hint` fields, all populated.

### Output expectations

- [x] PASS: Output's content inventory step processes all existing articles — Step 1 instructs scanning ALL documentation files ("categorise every piece") with quadrant classification and a Status column (Current/Stale/Orphaned), covering the full set not a sample.
- [x] PASS: Output uses Diataxis taxonomy explicitly — framework is named in the opening sentence, and the four types are defined with purpose/orientation/user-need in a definitions table in Step 1.
- [x] PASS: Output's gap analysis identifies what's missing per product area concretely — Step 3's "Missing content" table has User task + Missing quadrant(s) + Impact + Priority columns, requiring specific task-level identification.
- [x] PASS: Output's coverage matrix maps content to user tasks — Step 2 explicitly uses user tasks as rows with concrete examples ("export a report", "invite a teammate", "Set up SSO"), not feature-area rows.
- [x] PASS: Output addresses the support-ticket signal — Step 3's "Findability gaps" section explicitly cross-references recurring support questions against the inventory, and distinguishes between "content exists but users can't find it" (findability gap, fix IA) versus "no doc" (coverage gap, create).
- [x] PASS: Output's roadmap is prioritised — P0 is explicitly defined as "blocks user onboarding or generates frequent support tickets."
- [x] PASS: Output's content standards define what GOOD looks like per Diataxis type — Per-Quadrant Standards table in Step 5 specifies structure, length, and must-include elements for each type (e.g. "How-to: numbered steps, minimal explanation, 2-5 minutes to read, goal in title, prerequisites, single outcome").
- [x] PASS: Output's recommendations distinguish between rewrite, retire, and create — Step 3 makes the action mapping explicit: "Missing → create", "Stale → rewrite", "Orphaned → retire", "Findability → fix IA". No inference required.
- [x] PASS: Output addresses content maintenance as a strategic component — Step 5 mandates a freshness policy and ownership model; Step 6's maintenance section requires monthly review, feature-change trigger, quarterly audit, and support ticket review.
- [x] PASS: Output addresses the IA/findability dimension — Step 3 has a dedicated "Findability gaps" table requiring cross-reference of support questions vs inventory, with columns for why users miss content and the specific IA fix (search, navigation, tagging). The Rules section reinforces: "Findability is part of the strategy."

## Notes

The skill has been substantially strengthened since the previous evaluation. All three previous failures have been resolved: the coverage matrix now explicitly uses user tasks as rows with worked examples; the findability dimension has its own gap category in Step 3 with a dedicated table; and the rewrite/retire/create/fix-IA action mapping is now stated explicitly rather than implied.

The only criterion not fully met is the PARTIAL-prefixed maintenance criterion, which by definition cannot score above 0.5 regardless of how well the skill addresses it — and the skill addresses it well.
