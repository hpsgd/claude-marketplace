# Test: create-agent new specialist agent

Scenario: A contributor asks the create-agent skill to create a new `billing-engineer` agent for the engineering category, covering subscription billing, invoicing, payment gateway integration, and revenue recognition workflows.

## Prompt

/create-agent billing-engineer — responsible for subscription billing logic, invoicing, payment gateway integration (Stripe, PayPal), dunning management, and revenue recognition workflows. Engineering category.

Output structure:

- **Step 1 — Pre-flight reads** (show explicitly): list each Read with absolute path:
  ```
  Read: /Users/martin/Projects/turtlestack/plugins/practices/plugin-curator/templates/agent-template.md
  Read: /Users/martin/Projects/turtlestack/CLAUDE.md
  Read: /Users/martin/Projects/turtlestack/.claude-plugin/marketplace.json
  ```
- **Step 2 — Domain research** — list established billing/subscription patterns the agent should know: SaaS metrics (MRR, ARR, churn, LTV), revenue recognition (ASC 606), Stripe billing primitives (Subscriptions, Invoices, PaymentIntents, Webhooks), dunning workflows (3-7 day retry cadence), VAT/GST handling per jurisdiction.
- **Step 3 — Agent file** at `plugins/engineering/billing-engineer/agents/billing-engineer.md` with full agent template structure (frontmatter, mission, non-negotiable rules, methodology, output format, anti-patterns, related skills).
- **Step 4 — plugin.json** at `plugins/engineering/billing-engineer/.claude-plugin/plugin.json` with plugin metadata.
- **Step 5 — marketplace.json update** — show the diff adding the new entry with `source`, `description`, `category` fields:
  ```json
  {
    "name": "billing-engineer",
    "source": "./plugins/engineering/billing-engineer",
    "description": "Subscription billing, invoicing, payment gateway integration, dunning, revenue recognition.",
    "category": "engineering"
  }
  ```
- **Step 6 — README updates (THREE places)** — show the diff for each:
  1. Main agent listing (top-level table or list of agents)
  2. Engineering-category section listing
  3. Skill cross-reference (if any related skill mentions billing-adjacent agents)
- **Step 7 — Coordinator RATSI update** — show the diff to the coordinator agent's RATSI table (`plugins/leadership/coordinator/agents/coordinator.md` or equivalent) adding billing-engineer with Responsibilities/Accountabilities entries.
- **Step 8 — CTO/lead team listing update** — show the diff to the relevant lead agent (likely `plugins/leadership/cto/agents/cto.md`) adding billing-engineer to its specialist roster.
- **Step 9 — Verification** — run and SHOW THE OUTPUT of:
  ```bash
  jq . plugins/engineering/billing-engineer/.claude-plugin/plugin.json
  jq '.plugins | length' .claude-plugin/marketplace.json
  find plugins/engineering -maxdepth 1 -mindepth 1 -type d | wc -l
  grep -r "billing-engineer" plugins/ | wc -l
  grep -rn "Martin\|martin@hps" plugins/engineering/billing-engineer/ || echo "no private references found"
  ```
  Each command MUST be shown with its captured output beneath. The `jq '.plugins | length'` count MUST be reported alongside the directory count from `find ... | wc -l` and the two MUST be reconciled (e.g. "31 marketplace entries vs 31 plugin directories — match").

ALL nine steps above MUST appear as labelled headings in the output (`## Step 1 — Pre-flight reads`, `## Step 2 — Domain research`, ..., `## Step 9 — Verification`). Do NOT collapse, merge, or skip steps even if a registry entry already exists — if it exists, show its current content via `grep`/`jq` instead of writing a diff, but the heading MUST be present.

A few specifics for the response:

- Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
- Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
- For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
- When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
- Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Criteria

- [ ] PASS: Step 1 reads the agent template, CLAUDE.md, and marketplace.json before creating anything
- [ ] PASS: Step 2 performs domain research before writing — identifies established billing/payments frameworks or methodologies (e.g., Stripe billing model, revenue recognition standards, dunning flow patterns)
- [ ] PASS: All required directory structure is created: `.claude-plugin/`, `agents/`, `skills/`, and `templates/` if applicable
- [ ] PASS: Agent definition follows all mandatory sections: Core statement, Non-negotiable, Pre-Flight, Domain methodology, Output format, Failure caps, Decision checkpoints, Collaboration, Principles, What You Don't Do
- [ ] PASS: Agent uses `sonnet` model — billing-engineer is a specialist, not leadership
- [ ] PASS: marketplace.json is updated with the new plugin entry including source path, description, version, category, and tags
- [ ] PASS: All registry updates are completed — marketplace.json, README (3 places), coordinator RATSI, and relevant lead team listing
- [ ] PARTIAL: Verification step confirms JSON is valid, plugin count matches registry count, and no private references exist in the new files

## Output expectations

- [ ] PASS: Output creates the directory structure under `plugins/engineering/billing-engineer/` (engineering category from the prompt) with `.claude-plugin/plugin.json`, `agents/billing-engineer.md`, `skills/`, and `templates/` — exact paths matching the project's nested category layout
- [ ] PASS: Output's `plugin.json` contains the required metadata — name, description, version, source — and is valid JSON, not pseudo-JSON
- [ ] PASS: Output's `agents/billing-engineer.md` contains all mandatory sections: Core statement, Non-negotiable, Pre-Flight (with Step 1 reading CLAUDE.md), Domain methodology, Output format, Failure caps, Decision checkpoints, Collaboration, Principles, What You Don't Do
- [ ] PASS: Output sets the model to `sonnet` (specialist agent), not `opus`, in the agent frontmatter
- [ ] PASS: Output's domain methodology references established frameworks — Stripe billing lifecycle, subscription state machines, dunning flows, revenue recognition (ASC 606 / IFRS 15) — not invented terminology
- [ ] PASS: Output updates `marketplace.json` with the new plugin entry — name, source path (`./plugins/engineering/billing-engineer`), description, version, category (`engineering`), tags
- [ ] PASS: Output updates the README.md (in three places per the prompt — main listing, category listing, and skill cross-reference if applicable) to register the new agent
- [ ] PASS: Output updates the coordinator's RATSI table (or equivalent dispatch reference) to include the billing-engineer agent's responsibilities
- [ ] PASS: Output's verification step shows command output confirming JSON validity (`jq . marketplace.json`), the plugin count matches registry count, and no private references exist in the new files
- [ ] PARTIAL: Output's billing-engineer agent definition includes specific billing domain decision checkpoints (e.g. "before changing invoice generation logic", "before modifying retry/dunning behaviour") rather than generic checkpoints copied from another agent
