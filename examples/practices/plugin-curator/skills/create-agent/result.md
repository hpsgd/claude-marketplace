# Create Agent

Scenario: A contributor asks the create-agent skill to create a new `billing-engineer` agent for the engineering category, covering subscription billing, invoicing, payment gateway integration, and revenue recognition workflows.

## Prompt

> /create-agent billing-engineer — responsible for subscription billing logic, invoicing, payment gateway integration (Stripe, PayPal), dunning management, and revenue recognition workflows. Engineering category.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Created: billing-engineer

The billing-engineer agent plugin has been successfully created and verified. This agent specializes in subscription billing logic, payment gateway integration, invoicing, dunning management, and revenue recognition workflows.

### Files Created/Present
- ✅ `plugins/engineering/billing-engineer/.claude-plugin/plugin.json`
- ✅ `plugins/engineering/billing-engineer/agents/billing-engineer.md`
- ✅ `plugins/engineering/billing-engineer/skills/` (ready for future skills)
- ✅ `plugins/engineering/billing-engineer/templates/` (ready for future templates)

### Registry Updates
- ✅ **marketplace.json:** Entry present with correct metadata
- ✅ **README.md:** Install command, detailed agent section, and JSON install block
- ✅ **CTO agent:** billing-engineer listed in team coordination table
- ✅ **plugin.json:** Repository URL corrected from placeholder

### Quality Metrics
- **Lines:** 206 (within 150-300 range)
- **Sections:** 23 (Pre-Flight, Payment Processing, Dunning, Revenue Recognition, Webhooks, Reconciliation, Evidence, Failure Caps, Decision Checkpoints, Collaboration, Principles, What You Don't Do)
- **Model:** Sonnet (appropriate for specialist implementation agent)
- **Tools:** Read, Write, Edit, Bash, Glob, Grep (appropriate for billing implementation)

### Agent Audit Score
- [x] 150–300 lines ✓ (206 lines)
- [x] Core statement explains ownership ✓
- [x] Non-negotiable rules are specific ✓ (idempotency, revenue recognition, logging)
- [x] Pre-Flight reads conventions and patterns ✓
- [x] Domain methodology has mandatory steps ✓ (5 major sections: idempotency, dunning, revenue recognition, invoicing, webhooks, reconciliation)
- [x] Structured output format defined ✓
- [x] Failure caps defined ✓
- [x] Decision checkpoints defined ✓ (5 triggers)
- [x] Collaboration table present ✓ (6 roles)
- [x] Principles are opinionated and domain-specific ✓ (7 principles)
- [x] "What You Don't Do" names who owns each excluded thing ✓
- [x] No private/internal references ✓
- [x] External tools linked (Stripe, PayPal, ASC 606, IFRS 15) ✓
- [x] Correct model (sonnet) ✓
- [x] Description precise for auto-invocation ✓

### Verification
- JSON valid: ✅
- Plugin count matches registry: ✅ (39 plugins in registry)
- No private references: ✅
- Repository URL corrected: ✅

The billing-engineer agent is ready to use. It provides expert guidance on payment processing, subscription management, revenue recognition, and financial compliance. Invoke with `billing-engineer:billing-engineer` for payment workflow implementation, invoicing systems, or dunning strategy design.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.5/17.0 (85%) |
| Evaluated | 2026-05-03 |
| Target duration | 64522 ms |
| Target cost | $0.1668 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 reads the agent template, CLAUDE.md, and marketplace.json before creating anything | FAIL | The captured output is a final summary report. There is no mention anywhere of reading the agent template, CLAUDE.md, or marketplace.json as a pre-creation step. The output jumps directly to listing created files and audit results. |
| c2 | Step 2 performs domain research before writing — identifies established billing/payments frameworks or methodologies (e.g., Stripe billing model, revenue recognition standards, dunning flow patterns) | PARTIAL | No explicit research step is described. However, the audit checklist entry 'External tools linked (Stripe, PayPal, ASC 606, IFRS 15) ✓' shows established frameworks were identified and incorporated, and the domain methodology includes Dunning, Revenue Recognition, and Webhooks sections — indirect evidence that domain research occurred. The process step itself is not shown. |
| c3 | All required directory structure is created: `.claude-plugin/`, `agents/`, `skills/`, and `templates/` if applicable | PASS | All four paths are explicitly listed: 'plugins/engineering/billing-engineer/.claude-plugin/plugin.json', 'plugins/engineering/billing-engineer/agents/billing-engineer.md', 'plugins/engineering/billing-engineer/skills/ (ready for future skills)', and 'plugins/engineering/billing-engineer/templates/ (ready for future templates)'. |
| c4 | Agent definition follows all mandatory sections: Core statement, Non-negotiable, Pre-Flight, Domain methodology, Output format, Failure caps, Decision checkpoints, Collaboration, Principles, What You Don't Do | PASS | The audit checklist explicitly confirms each mandatory section: 'Core statement explains ownership ✓', 'Non-negotiable rules are specific ✓', 'Pre-Flight reads conventions and patterns ✓', 'Domain methodology has mandatory steps ✓', 'Structured output format defined ✓', 'Failure caps defined ✓', 'Decision checkpoints defined ✓', 'Collaboration table present ✓', 'Principles are opinionated and domain-specific ✓', 'What You Don't Do names who owns each excluded thing ✓'. |
| c5 | Agent uses `sonnet` model — billing-engineer is a specialist, not leadership | PASS | 'Model: Sonnet (appropriate for specialist implementation agent)' and audit checklist '[x] Correct model (sonnet) ✓'. |
| c6 | marketplace.json is updated with the new plugin entry including source path, description, version, category, and tags | PASS | '✅ marketplace.json: Entry present with correct metadata' and verification shows 'Plugin count matches registry: ✅ (39 plugins in registry)'. Audit entry '[x] Description precise for auto-invocation ✓' also implies the description field is populated. |
| c7 | All registry updates are completed — marketplace.json, README (3 places), coordinator RATSI, and relevant lead team listing | PASS | Output confirms: '✅ marketplace.json: Entry present with correct metadata', '✅ README.md: Install command, detailed agent section, and JSON install block' (three places), '✅ CTO agent: billing-engineer listed in team coordination table'. No explicit mention of engineering-lead team listing, but coordinator and three README locations are covered. |
| c8 | Verification step confirms JSON is valid, plugin count matches registry count, and no private references exist in the new files | PARTIAL | Verification section states: 'JSON valid: ✅', 'Plugin count matches registry: ✅ (39 plugins in registry)', 'No private references: ✅'. All three items confirmed, though as status icons rather than command output. |
| c9 | Output creates the directory structure under `plugins/engineering/billing-engineer/` (engineering category from the prompt) with `.claude-plugin/plugin.json`, `agents/billing-engineer.md`, `skills/`, and `templates/` — exact paths matching the project's nested category layout | PASS | All four exact paths are listed under 'plugins/engineering/billing-engineer/' matching the engineering category: '.claude-plugin/plugin.json', 'agents/billing-engineer.md', 'skills/', and 'templates/'. |
| c10 | Output's `plugin.json` contains the required metadata — name, description, version, source — and is valid JSON, not pseudo-JSON | PASS | 'JSON valid: ✅' in verification, and 'plugin.json: Repository URL corrected from placeholder' indicates the file was inspected and its content corrected, confirming real JSON was written with actual field values. |
| c11 | Output's `agents/billing-engineer.md` contains all mandatory sections: Core statement, Non-negotiable, Pre-Flight (with Step 1 reading CLAUDE.md), Domain methodology, Output format, Failure caps, Decision checkpoints, Collaboration, Principles, What You Don't Do | PASS | Agent Audit Score checklist explicitly confirms every mandatory section present, including 'Pre-Flight reads conventions and patterns ✓', 'Failure caps defined ✓', 'Decision checkpoints defined ✓ (5 triggers)', 'Collaboration table present ✓ (6 roles)', 'Principles are opinionated and domain-specific ✓ (7 principles)', and 'What You Don't Do names who owns each excluded thing ✓'. |
| c12 | Output sets the model to `sonnet` (specialist agent), not `opus`, in the agent frontmatter | PASS | Quality Metrics section: 'Model: Sonnet (appropriate for specialist implementation agent)' and audit '[x] Correct model (sonnet) ✓'. |
| c13 | Output's domain methodology references established frameworks — Stripe billing lifecycle, subscription state machines, dunning flows, revenue recognition (ASC 606 / IFRS 15) — not invented terminology | PASS | Audit checklist confirms 'External tools linked (Stripe, PayPal, ASC 606, IFRS 15) ✓', and domain methodology sections include 'Payment Processing, Dunning, Revenue Recognition' — all established billing frameworks, not invented terminology. |
| c14 | Output updates `marketplace.json` with the new plugin entry — name, source path (`./plugins/engineering/billing-engineer`), description, version, category (`engineering`), tags | PASS | '✅ marketplace.json: Entry present with correct metadata' with plugin count verification. The path under 'plugins/engineering/billing-engineer/' matches the required source path. Specific field values not shown verbatim but claimed to be correct and valid per JSON validity check. |
| c15 | Output updates the README.md (in three places per the prompt — main listing, category listing, and skill cross-reference if applicable) to register the new agent | PASS | '✅ README.md: Install command, detailed agent section, and JSON install block' — three named locations explicitly confirmed. |
| c16 | Output updates the coordinator's RATSI table (or equivalent dispatch reference) to include the billing-engineer agent's responsibilities | PASS | '✅ CTO agent: billing-engineer listed in team coordination table' confirms the coordinator's dispatch reference was updated. |
| c17 | Output's verification step shows command output confirming JSON validity (`jq . marketplace.json`), the plugin count matches registry count, and no private references exist in the new files | FAIL | The verification section shows status checkmarks ('JSON valid: ✅', 'Plugin count matches registry: ✅', 'No private references: ✅') but no actual command output is shown — no `jq` output, no grep results, no terminal commands. The criterion specifically requires 'command output'. |
| c18 | Output's billing-engineer agent definition includes specific billing domain decision checkpoints (e.g. 'before changing invoice generation logic', 'before modifying retry/dunning behaviour') rather than generic checkpoints copied from another agent | PARTIAL | Audit checklist states 'Decision checkpoints defined ✓ (5 triggers)' but does not enumerate what those triggers are. The captured output provides no text from the agent file itself, so specific billing-domain wording cannot be verified. Existence is confirmed but domain specificity is unverifiable. |

### Notes

The captured output is a well-structured final summary report rather than a full execution transcript, which means process-oriented criteria (c1: reading templates before starting; c17: showing actual command output) cannot be verified and fail for lack of evidence. The agent creation itself appears high-quality: all directory paths are correct, all mandatory sections are claimed present, established billing frameworks (Stripe, ASC 606, IFRS 15, dunning) are referenced, the sonnet model is used, and all four registry locations are updated. The two PARTIAL results (c2, c18) reflect that domain framework usage is inferred from results rather than shown explicitly, and decision checkpoint content cannot be inspected. The main gap is the absence of raw command output in the verification step — checkmarks confirm outcomes but do not satisfy the `jq` / grep evidence requirement in c17.
