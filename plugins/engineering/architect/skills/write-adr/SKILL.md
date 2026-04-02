---
name: write-adr
description: "Write an Architecture Decision Record using the MADR template. Captures context, options considered, decision made, consequences, and confirmation criteria."
argument-hint: "[technical decision to document]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Write an Architecture Decision Record

Write an ADR for $ARGUMENTS using the MADR (Markdown Any Decision Records) format.

## When to Write an ADR

Write an ADR for decisions that:
- Affect the system's structure (service boundaries, data flow, API contracts)
- Are expensive to reverse (technology choices, database schema, authentication approach)
- Will be questioned later ("why did we do it this way?")
- Affect multiple teams or domains

**Don't write an ADR for:** trivial choices (variable names, which linter rule), decisions already covered by project conventions, or temporary decisions that will be revisited within a sprint.

## Process

### Step 1: Check for existing ADRs

```bash
find . -path '*/adr*' -name '*.md' -o -path '*/architecture-decisions*' -name '*.md' | sort
```

- Read existing ADRs to understand the numbering scheme and style
- Check if this decision supersedes or relates to an existing ADR

### Step 2: Determine the next ADR number

```bash
ls docs/adr/ 2>/dev/null | sort -n | tail -1
```

### Step 3: Write the ADR

Use the MADR template. The template is at `${CLAUDE_PLUGIN_ROOT}/templates/adr-template.md` — read it for the full structure.

**Key sections (none optional):**

#### Frontmatter
```yaml
---
status: "proposed"
date: YYYY-MM-DD
decision-makers: [who is making this decision]
consulted: [who was asked for input]
informed: [who needs to know the outcome]
---
```

#### Title
`# ADR-NNNN: {Short title — describes the problem AND solution}`

Good: "ADR-0005: Use PostgreSQL BYTEA for binary content storage"
Bad: "ADR-0005: Database decision" (too vague)
Bad: "ADR-0005: We should use PostgreSQL" (no problem stated)

#### Context and Problem Statement
2-3 sentences. What situation requires a decision? What forces are at play? Frame as a question if helpful.

**Rules:**
- State the problem, not the solution
- Include constraints (technical, business, team, timeline)
- Be specific about what triggered this decision now

#### Decision Drivers
Bulleted list of forces that influence the decision. These become the evaluation criteria for options.

#### Considered Options
At least 2 options. Always include "do nothing / status quo" if applicable.

#### Decision Outcome
- State which option was chosen
- Explain WHY in terms of the decision drivers
- Be honest about trade-offs

#### Consequences
Three categories:
- **Positive:** What improves
- **Negative:** What gets worse (every decision has downsides — if you can't name one, you haven't thought hard enough)
- **Risks:** What could go wrong, and what would trigger reconsideration

#### Confirmation
How will you know this decision is working? Specific criteria:
- A review date
- A metric to watch
- An automated test or CI check
- Conditions that would trigger revisiting

#### Pros and Cons of Options
For EACH option (including the chosen one):
- Structured as `Good, because...` / `Bad, because...` / `Neutral, because...`
- Be honest about the chosen option's downsides
- Be fair about rejected options' strengths

## Quality Checklist

Before declaring the ADR complete:

- [ ] Title describes both the problem and the solution
- [ ] Context explains WHY this decision is needed NOW
- [ ] At least 2 options considered (including status quo if applicable)
- [ ] Decision drivers are specific enough to evaluate options against
- [ ] Consequences include at least one negative (honesty check)
- [ ] Risks identify what would trigger reconsideration
- [ ] Confirmation criteria are measurable or observable
- [ ] Rejected options have fair representation (not strawmen)
- [ ] Related ADRs are linked (supersedes, builds on, relates to)

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| **Retroactive ADR** | Written after the decision to justify it | Write during the decision process, not after |
| **No alternatives** | Only the chosen option described | Always include at least one real alternative |
| **Strawman options** | Alternatives are obviously bad | Include options that were genuinely considered |
| **Missing consequences** | Only positive outcomes listed | Every decision has trade-offs. State them |
| **Too long** | 5+ pages | One page ideal, two maximum. Link to supporting docs |
| **Too vague** | "We chose X because it's better" | Better at WHAT? Against which decision drivers? |
| **Orphaned ADR** | No confirmation criteria | How will you know if this was the right call? |

## Output

Write to the project's ADR directory (check for existing location: `docs/adr/`, `docs/architecture-decisions/`, or `docs/decisions/`). If none exists, create `docs/adr/`.

File naming: `NNNN-kebab-case-title.md` (e.g., `0005-use-postgresql-bytea-for-content.md`)

After writing, update any index file if one exists.
