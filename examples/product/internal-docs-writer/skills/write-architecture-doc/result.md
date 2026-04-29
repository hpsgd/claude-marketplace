# Output: Write architecture doc

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 16/19 criteria met (84.2%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Mermaid diagrams required for component architecture — Step 3 provides a `graph TD` Mermaid template as mandatory output. The Rules section states "Diagrams are mandatory. Use Mermaid for all diagrams so they live in version control."
- [x] PASS: Sequence diagrams required for data flows — Step 4 provides a `sequenceDiagram` Mermaid template specifically for tracing temporal interaction order. Rules state "Use Mermaid sequence diagrams — they are versionable and diffable."
- [x] PASS: Key decisions documented with rationale — Step 5 requires a Key Decisions table with Decision, Choice, Rationale, and ADR columns. Rules explicitly state "Document the rationale, not just the choice."
- [x] PASS: NFRs with specific targets — Step 6 requires an NFR table with Target, Current, and Measured by columns. The template shows concrete numeric targets (e.g., "< 200ms reads", "500 req/s peak").
- [x] PASS: Research step before writing — Step 1 is a dedicated pre-writing research phase covering codebase search, infrastructure definitions, ADR review, data flow tracing, and bounded context identification.
- [x] PASS: Bounded contexts documented — Step 5 requires a Bounded Contexts table with Owns, Communicates via, and Boundary type columns.
- [~] PARTIAL: Known limitations mentioned but not required as mandatory — the section is present and templated in Step 6's Output Format as a mandatory section. The criterion is PARTIAL-prefixed so the score caps at 0.5.
- [x] PASS: Quality checklist present — Step 7 is an explicit checklist table verifying: diagrams present, boundaries clear, decisions linked, failure modes stated, no implementation details, and freshness marker.
- [x] PASS: Valid YAML frontmatter — Frontmatter is present with `name: write-architecture-doc`, `description`, and `argument-hint: "[system, service, or area to document]"` fields.

### Output expectations

- [x] PASS: The skill's Step 3 Mermaid `graph TD` template with component arrows is mandatory. Applied to the notification system prompt, the skill would produce a component diagram showing in-app, email, push channels, queue, preferences service, and external providers with control-flow arrows — all components named in the prompt map to the template structure.
- [x] PASS: The skill's Step 4 `sequenceDiagram` template traces caller → service → queue → worker → provider with temporal ordering. The notification dispatch flow is exactly the type of critical workflow Step 4 targets.
- [x] PASS: Step 5's Bounded Contexts table requires Owns and Communicates via columns. The skill's prompt drives documenting what the notification system owns (delivery decisions, routing) vs depends on — the template structure forces this distinction.
- [ ] FAIL: The skill's Step 6 NFR template uses generic placeholders (e.g., "< 200ms reads", "500 req/s peak") rather than notification-system-specific numeric targets. The output expectations require p95 < 5s for in-app, < 60s for email/push, 50K/day throughput targets. The skill would produce a correctly structured NFR table, but the specific numeric targets in the expected output come from domain knowledge the skill does not supply — it only provides a template and instructs filling it in from research.
- [x] PASS: Step 5 requires at least the Decision, Choice, Rationale, and ADR columns. The rules state "Include decisions that were considered and rejected." Applied to the notification prompt, queue-based delivery, channel routing, and preferences design would each generate a decision row with rationale and rejected alternative — meeting the 3+ decisions criterion.
- [ ] FAIL: The skill's Known Limitations section in Step 6 is a bulleted list template with impact descriptions, but it does not require links to backlog items. The output expectation specifically requires "a link to backlog items" for each limitation — the skill template shows no such requirement.
- [x] PASS: Step 1 Research phase explicitly requires reading existing ADRs, configs, infrastructure definitions, and codebase. The rule "Do not describe aspirational architecture. Document what IS deployed" enforces citation fidelity. The research step would produce cited file paths.
- [ ] FAIL: Step 7's quality checklist verifies that every key decision references an ADR (or "to be written" with a date). However, it does not explicitly include "Mermaid diagrams render without syntax errors" as a checklist item — it says "Diagrams present" not "Diagrams render." The output expectation requires both: syntax-valid Mermaid AND ADR traceability.
- [x] PASS: Step 5's Bounded Contexts and the per-component Owns/Consumes tables in Step 3 address preferences as an owned component. The prompt explicitly names "user preference management" and the skill's component template requires documenting what each component owns, exposes, and how it fails — covering channel × event-type matrix ownership and delivery-time enforcement as natural outputs.
- [~] PARTIAL: The skill's Steps 3 and 4 annotate failure handling and latency per data-flow step, and Step 6 includes "Measured by" in the NFR table. However, there is no dedicated observability section requiring metric names (delivery rate, queue depth, provider error rate), dashboards, and alert definitions. The criterion is PARTIAL-prefixed so the score caps at 0.5.

## Notes

The Criteria section scores 8.5/9 (same as the prior evaluation). The Output expectations section scores 7.5/10 — three failures and one partial.

The primary gaps are: (1) the NFR section does not seed domain-specific targets for notification systems, relying on the executor to supply them from research; (2) the Known Limitations section omits any requirement to link limitations to backlog items; (3) the quality checklist checks diagram presence but not Mermaid syntax validity specifically.

The skill is structurally strong. The failures are cases where the expected output requires either domain-specific defaults the skill cannot reasonably embed, or explicit requirements the skill template stops just short of mandating.
