---
name: service-blueprint
description: "Create a service blueprint -- mapping both the customer-facing journey and the backstage organisational processes that support it. Extends journey mapping with employee actions, support systems, and physical evidence. Use when analysing end-to-end service delivery or identifying backstage bottlenecks."
argument-hint: "[service or customer journey to blueprint]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Service Blueprint

Create a service blueprint for $ARGUMENTS. A service blueprint extends a journey map by adding everything that happens behind the scenes — employee actions, support systems, and handoffs that the customer never sees but that determine whether the experience works.

Reference: [NNGroup Service Blueprints](https://www.nngroup.com/articles/service-blueprints-definition/)

## Step 1: Define scope (mandatory)

```markdown
### Blueprint scope

| Element | Detail |
|---|---|
| **Service** | [specific service being blueprinted] |
| **Journey** | [which customer journey — start to end] |
| **Start point** | [concrete trigger — e.g. "customer submits support ticket"] |
| **End point** | [concrete outcome — e.g. "issue resolved and customer confirms"] |
| **Customer type** | [who is the customer in this journey] |
| **Success metric** | [how you measure this service works — resolution time, NPS, completion rate] |
```

**Rules for scope:**
- One service, one blueprint. "Our entire product experience" is not a scope — "new customer onboarding from signup to first value" is
- Start and end must be concrete events with a clear trigger and outcome
- If a journey map exists from `/ux-researcher:journey-map`, use it as the frontstage foundation

**Output:** Scope definition table.

## Step 2: Map customer actions (mandatory)

Map every action the customer takes from start to end:

```markdown
### Customer actions (top lane)

| Step | Customer action | Touchpoint | Channel |
|---|---|---|---|
| 1 | [what the customer does] | [what they interact with] | [web, app, email, phone, in-person] |
| 2 | [next action] | [touchpoint] | [channel] |
| ... | ... | ... | ... |
```

**Rules for customer actions:**
- These are ONLY things the customer does or sees. If the customer doesn't do it or see it, it belongs in a later lane
- Include wait times as explicit steps — "Customer waits for response (avg 4h)" is a real step
- Every touchpoint must specify the channel — "email" and "in-app notification" serve different purposes

**Output:** Complete customer action lane.

## Step 3: Map frontstage employee actions (mandatory)

Map what employees do that the customer CAN see:

```markdown
### Frontstage employee actions

| Step | Corresponding customer action | Employee action | Role | Touchpoint |
|---|---|---|---|---|
| 1 | [customer step] | [what the employee does visibly] | [role — support agent, CS manager, sales] | [email, call, chat, in-person] |
| 2 | [customer step] | [employee action] | [role] | [touchpoint] |
```

**Rules for frontstage:**
- Frontstage means the customer is aware of it. The support agent replying to a ticket is frontstage. The support agent looking up the customer's history is backstage
- Every customer action should have a corresponding frontstage response (even if automated). If a customer action has no response, that's a gap
- Specify the role, not the person — roles are replaceable, people are not

**Output:** Frontstage employee action lane aligned to customer actions.

## Step 4: Draw the line of visibility (mandatory)

```markdown
### Line of visibility

───────────────────── LINE OF VISIBILITY ─────────────────────
Everything above: the customer sees it
Everything below: the customer does NOT see it

**Visibility audit:**
| Customer action | What customer sees | What customer does NOT see |
|---|---|---|
| [action] | [frontstage response] | [backstage work that makes it possible] |
| [action] | [visible response] | [hidden process] |
```

**Rules for the line of visibility:**
- The line of visibility is the most important concept in the blueprint. It separates the experience (above) from the operations (below)
- Anything that crosses the line (backstage work that becomes visible) is a moment of truth — handle with care
- If the customer can see internal process leaking through (e.g. "your ticket has been escalated to tier 2"), that's a visibility breach. Decide if it's intentional or accidental

**Output:** Line of visibility with visibility audit table.

## Step 5: Map backstage employee actions (mandatory)

Map what employees do that the customer CANNOT see:

```markdown
### Backstage employee actions

| Step | Triggered by | Employee action | Role | System/tool used | Duration |
|---|---|---|---|---|---|
| 1 | [customer or frontstage action] | [what happens behind the scenes] | [role] | [internal tool] | [how long] |
| 2 | [trigger] | [backstage action] | [role] | [tool] | [duration] |
```

**Rules for backstage:**
- Every backstage action must be triggered by something — a customer action, a frontstage action, or another backstage action. No orphaned steps
- Include handoffs between people/teams as explicit steps — handoffs are where services break
- Duration matters — a "quick review" that takes 3 days is a bottleneck, not a quick review

**Output:** Backstage employee action lane with triggers and durations.

## Step 6: Map support processes (mandatory)

Map the internal systems, tools, and infrastructure that enable the service:

```markdown
### Support processes (bottom lane)

| Backstage action | Support system | Type | Owner | SLA/availability |
|---|---|---|---|---|
| [backstage step] | [system that enables it] | [CRM, database, API, queue, manual process] | [team] | [uptime, response time] |
| [backstage step] | [system] | [type] | [owner] | [SLA] |
```

**Rules for support processes:**
- If a backstage action relies on a system, that system belongs here. If the system goes down, the service fails
- "Manual process" is a valid support process — and often the most fragile. Flag it
- Identify single points of failure — systems or people where there is no backup

**Output:** Support process lane linked to backstage actions.

## Step 7: Identify failure points (mandatory)

```markdown
### Failure points

| # | Location | Failure mode | Impact on customer | Frequency | Root cause | Current mitigation |
|---|---|---|---|---|---|---|
| F1 | [lane and step] | [what goes wrong] | [what the customer experiences] | [daily/weekly/rare] | [why it fails] | [what's in place today — or "none"] |
| F2 | [location] | [failure] | [customer impact] | [frequency] | [cause] | [mitigation] |
```

**Focus areas for failure points:**
- **Handoffs between people** — information lost, delays, miscommunication
- **Handoffs between systems** — data sync failures, API timeouts, format mismatches
- **Line of visibility crossings** — internal errors leaking to customers
- **Manual processes** — human error, inconsistency, capacity bottlenecks
- **Wait times** — any step where the customer waits more than expected

**Output:** Failure point table with root causes and current mitigations.

## Step 8: Recommend improvements (mandatory)

```markdown
### Recommendations (prioritised by customer impact)

| Priority | Failure point | Recommendation | Impact | Effort | Owner |
|---|---|---|---|---|---|
| 1 | [F#] | [specific improvement] | [how it improves the customer experience] | [S/M/L] | [team] |
| 2 | [F#] | [improvement] | [impact] | [effort] | [team] |
| 3 | [F#] | [improvement] | [impact] | [effort] | [team] |
```

**Rules for recommendations:**
- Prioritise by customer impact, not ease of implementation
- "Automate X" is only a recommendation if you specify what to automate and how
- Quick wins (high impact, low effort) go first, but don't ignore systemic issues

**Output:** Prioritised recommendation table.

## Rules

- **The line of visibility is the key insight.** It separates what the customer sees from what they don't. Everything interesting happens at or near this line.
- **Every customer action must have a corresponding backstage process.** If there's no backstage support, who's handling it? Either someone is and you haven't mapped them, or no one is and that's a failure point.
- **Failure points at handoffs are the most common.** When work passes from one person to another, or one system to another, information is lost and delays accumulate. Look at handoffs first.
- **Wait times are steps, not gaps.** A customer waiting 48 hours for a response is experiencing the service. Map it, measure it, improve it.
- **Manual processes are fragile.** Every manual step is a reliability risk. Don't assume manual means simple — it often means inconsistent.
- **Don't blueprint what doesn't exist.** Map the current state first. Aspirational blueprints are roadmaps, not blueprints.

## Output Format

```markdown
# Service Blueprint: [service name]

## Scope
[From Step 1]

## Customer Actions
[Lane from Step 2]

## Frontstage Employee Actions
[Lane from Step 3]

───────────────────── LINE OF VISIBILITY ─────────────────────

## Backstage Employee Actions
[Lane from Step 5]

## Support Processes
[Lane from Step 6]

## Failure Points
[Table from Step 7]

## Recommendations
[Prioritised table from Step 8]

---
Service: [name]
Journey: [start → end]
Failure points identified: [N]
Last updated: [date]
```

## Related Skills

- `/ux-researcher:journey-map` — the customer-facing layer of the blueprint. If a journey map exists, use it as the foundation and add the backstage lanes.
- `/ux-researcher:usability-review` — for deep-diving into specific frontstage touchpoints that the blueprint identifies as high-friction.

Use the service blueprint template (`templates/service-blueprint.md`) for output structure.
