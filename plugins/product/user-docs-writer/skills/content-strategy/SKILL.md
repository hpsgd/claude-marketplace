---
name: content-strategy
description: "Define a documentation content strategy using the Diataxis framework — map existing content, identify gaps across tutorials/how-to/reference/explanation quadrants, and plan content creation. Use when establishing or auditing a documentation practice."
argument-hint: "[product or feature area to plan content for]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Content Strategy

Define a documentation content strategy for $ARGUMENTS using the [Diataxis framework](https://diataxis.fr/). This skill inventories existing content, maps coverage across the four Diataxis quadrants, identifies gaps, and produces a prioritised content roadmap.

## Step 1: Inventory Existing Content

Scan the documentation directory and categorise every piece by Diataxis quadrant:

```markdown
### Content Inventory

| # | Document | Path | Quadrant | Feature area | Last updated | Status |
|---|---|---|---|---|---|---|
| 1 | [Title] | [path] | Tutorial / How-to / Reference / Explanation | [feature] | [date] | Current / Stale / Orphaned |
| 2 | ... | ... | ... | ... | ... | ... |
```

Use `Glob` to find documentation files (`**/*.md`, `**/docs/**`, `**/*.rst`, `**/*.mdx`) and `Grep` to identify content patterns:
- **Tutorial indicators:** "learn", "getting started", "your first", step-by-step with explanations
- **How-to indicators:** "how to", numbered steps, goal-oriented, assumes knowledge
- **Reference indicators:** API docs, configuration tables, parameter lists, schemas
- **Explanation indicators:** "why", "understanding", "concepts", architecture, design decisions

**Quadrant definitions:**

| Quadrant | Purpose | Orientation | User need |
|---|---|---|---|
| **Tutorial** | Learning-oriented | Study | "Teach me" — guided experience for beginners |
| **How-to** | Task-oriented | Work | "Show me how" — steps to achieve a specific goal |
| **Reference** | Information-oriented | Work | "Tell me the facts" — accurate, complete technical description |
| **Explanation** | Understanding-oriented | Study | "Help me understand" — context, reasoning, background |

**Output:** Complete inventory table with quadrant classification and staleness assessment.

## Step 2: Map Coverage

Create a feature-by-quadrant coverage matrix:

```markdown
### Coverage Matrix

| Feature / Area | Tutorial | How-to | Reference | Explanation | Overall |
|---|---|---|---|---|---|
| [Feature 1] | [Yes/No/Stale] | [Yes/No/Stale] | [Yes/No/Stale] | [Yes/No/Stale] | [Complete/Partial/Missing] |
| [Feature 2] | ... | ... | ... | ... | ... |
| Authentication | Yes | Yes | Stale | No | Partial |
| API integration | No | Yes | Yes | No | Partial |
| Deployment | No | No | Yes | No | Missing |

### Coverage Summary

| Quadrant | Documents | % of total | Assessment |
|---|---|---|---|
| Tutorial | [count] | [%] | [Adequate / Insufficient / Missing] |
| How-to | [count] | [%] | ... |
| Reference | [count] | [%] | ... |
| Explanation | [count] | [%] | ... |
```

**Output:** Coverage matrix showing which features have which content types, plus quadrant summary.

## Step 3: Identify Gaps

Analyse the coverage matrix for specific gap patterns:

```markdown
### Gap Analysis

#### Missing content (no documentation exists)

| # | Feature | Missing quadrant(s) | Impact | Priority |
|---|---|---|---|---|
| G1 | [Feature] | [Tutorial / How-to / Reference / Explanation] | [Who is affected and how] | [High/Medium/Low] |

#### Stale content (exists but outdated)

| # | Document | Path | Last updated | What changed since |
|---|---|---|---|---|
| G2 | [Title] | [path] | [date] | [What in the product changed that makes this stale] |

#### Orphaned content (exists but unreachable)

| # | Document | Path | Issue |
|---|---|---|---|
| G3 | [Title] | [path] | [Not linked from navigation / references removed feature / duplicate] |

#### Common gap patterns

| Pattern | Check | Found? |
|---|---|---|
| **Explanation gap** | Teams write how-to but not why — look for features with how-to but no explanation | [Yes/No] |
| **Tutorial gap** | Onboarding path has reference docs but no guided tutorial | [Yes/No] |
| **Reference gap** | APIs or config options undocumented or auto-generated but incomplete | [Yes/No] |
| **Freshness gap** | Docs not updated when features changed | [Yes/No] |
```

**Output:** Gap analysis with specific missing content, stale content, and orphaned content.

## Step 4: Prioritise Content Creation

Rank gaps by impact and sequence content creation:

```markdown
### Prioritisation Criteria

| Factor | Weight | Rationale |
|---|---|---|
| **User traffic** | High | Most-visited features need content first |
| **Onboarding path** | High | New users must succeed — tutorials and getting-started content |
| **Support ticket volume** | High | Gaps that generate support requests cost real money |
| **Feature completeness** | Medium | Features with zero docs before features with partial docs |
| **Quadrant balance** | Medium | Missing explanation docs before second how-to for same feature |
| **Staleness risk** | Low | Update stale docs during regular maintenance, not as priority |

### Prioritised Content Backlog

| Priority | Content piece | Quadrant | Feature | Effort | Owner | Deadline |
|---|---|---|---|---|---|---|
| P0 | [Title — e.g., "Getting started tutorial"] | Tutorial | Onboarding | [S/M/L] | [role] | [date] |
| P0 | [Title] | ... | ... | ... | ... | ... |
| P1 | [Title] | ... | ... | ... | ... | ... |
| P2 | [Title] | ... | ... | ... | ... | ... |
```

**P0** = blocks user onboarding or generates frequent support tickets.
**P1** = significant gap for active users.
**P2** = completeness and polish.

**Output:** Prioritised content backlog with effort estimates, owners, and deadlines.

## Step 5: Define Content Standards

Establish quality standards that apply to all documentation:

```markdown
### Content Standards

| Standard | Policy |
|---|---|
| **Style guide** | [Reference — e.g., "Follow Google Developer Documentation Style Guide" or link to internal guide] |
| **Review process** | [Who reviews — peer review, technical review, editorial review] |
| **Freshness policy** | [How often docs are reviewed — e.g., "Every 6 months or when related feature changes"] |
| **Ownership model** | [Who owns docs — feature team owns all quadrants for their feature] |
| **Templates** | [Standard templates for each quadrant — tutorial template, how-to template, etc.] |
| **Testing** | [How to verify docs — code samples tested, links checked, screenshots current] |
| **Versioning** | [How docs track product versions — versioned docs, changelog, migration guides] |

### Per-Quadrant Standards

| Quadrant | Structure | Length | Must include |
|---|---|---|---|
| **Tutorial** | Numbered steps with outcomes | 10-30 minutes to complete | Prerequisites, working example at end, next steps |
| **How-to** | Numbered steps, minimal explanation | 2-5 minutes to read | Goal in title, prerequisites, single outcome |
| **Reference** | Tables, parameter lists, schemas | Complete coverage, scannable | Every parameter, every option, every error code |
| **Explanation** | Prose with diagrams | As long as needed | Why, not how; context, not procedure |
```

If a writing style guide exists in the codebase, reference it. If `/writing-style:style-guide` has been used, align with its outputs.

**Output:** Content standards table with per-quadrant requirements.

## Step 6: Create Content Roadmap

Synthesise the prioritised backlog into a phased roadmap:

```markdown
### Content Roadmap

#### Phase 1: Foundation (Weeks 1-4)
**Goal:** Users can onboard and complete core tasks

| Content piece | Quadrant | Owner | Status |
|---|---|---|---|
| [Title] | Tutorial | [role] | [Not started / In progress / Review / Published] |
| [Title] | How-to | [role] | ... |

#### Phase 2: Completeness (Weeks 5-8)
**Goal:** All major features have reference and how-to coverage

| Content piece | Quadrant | Owner | Status |
|---|---|---|---|
| ... | ... | ... | ... |

#### Phase 3: Depth (Weeks 9-12)
**Goal:** Explanation content and advanced tutorials

| Content piece | Quadrant | Owner | Status |
|---|---|---|---|
| ... | ... | ... | ... |

#### Ongoing: Maintenance
- [ ] Monthly freshness review — check docs modified > 6 months ago
- [ ] Feature-change trigger — update docs when feature PRs merge
- [ ] Quarterly coverage audit — re-run coverage matrix
- [ ] Support ticket review — identify docs gaps from ticket themes
```

**Output:** Phased roadmap with owners, deadlines, and maintenance schedule.

## Rules

- **All four Diataxis quadrants matter.** A product with only reference docs serves experts but abandons beginners. A product with only tutorials has no depth. Cover all four quadrants for key features.
- **Gaps in explanation docs are the most common.** Teams write how-to guides and reference docs but rarely explain why things work the way they do. Always check for missing explanation content.
- **Freshness is a quality dimension.** Stale documentation is worse than no documentation because users trust it and get wrong answers. Flag stale content as a gap and establish freshness policies.
- **Don't mix quadrants in one document.** A tutorial that turns into a reference table confuses the reader. Each document serves one quadrant. Link between them instead.
- **Prioritise by user impact, not completeness.** A perfect explanation doc for a rarely-used feature is less valuable than a basic tutorial for the core onboarding flow. Traffic and support tickets drive priority.
- **Content without ownership decays.** Every piece of documentation needs an owner. Unowned docs become stale within 6 months.

## Output Format

```markdown
# Content Strategy: [Product/Feature Area]

**Date:** [date]  |  **Author:** [name]  |  **Status:** [Draft/Approved]

## 1. Content Inventory
[From Step 1 — document list with quadrant classification]

## 2. Coverage Matrix
[From Step 2 — feature × quadrant matrix]

## 3. Gap Analysis
[From Step 3 — missing, stale, and orphaned content]

## 4. Prioritised Backlog
[From Step 4 — ranked content pieces with owners]

## 5. Content Standards
[From Step 5 — style, review, freshness policies]

## 6. Roadmap
[From Step 6 — phased plan with maintenance schedule]
```

## Related Skills

- `/writing-style:style-guide` — writing standards for documentation. Define the style guide first or align content strategy with existing standards.
- `/developer-docs-writer:write-api-docs` — reference quadrant content for APIs. Use for detailed API reference documentation.
- `/user-docs-writer:write-onboarding` — tutorial quadrant content for new users. Use for guided onboarding experiences.
