---
name: write-user-story
description: Write user stories with Gherkin acceptance criteria, edge cases, anti-requirements, and ISC-validated criteria from a feature description or PRD section.
argument-hint: "[feature description or PRD reference]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

Write user stories for $ARGUMENTS.

Follow every step below. Each story must be complete enough to hand directly to an engineer without additional conversation.

---

## Step 1: Identify the User Types

Before writing any stories, list every distinct user type involved. Do not use generic labels.

**Anti-patterns (never use these):**
- "As a user" — which user? This is always too vague.
- "As an admin" — what kind of admin? What are they trying to accomplish?
- "As the system" — systems do not have goals. Reframe as the user who benefits from the system behaviour.

**Good user types are specific about role AND context:**
- "As a team lead reviewing my direct reports' weekly submissions"
- "As a first-time visitor who arrived from a Google search"
- "As a billing admin who manages subscriptions for 50+ seats"
- "As a developer integrating our API for the first time"

For each user type, note:
- Their goal (what they are trying to accomplish overall, not just in this story)
- Their technical sophistication
- Their frequency of interaction (daily power user vs. monthly visitor)

---

## Step 2: Write One Story Per Behaviour

Each story captures exactly one user behaviour. Apply this test: if the story has "and" in the action clause, it is two stories. Split it.

### Story Format

```markdown
### US-[N]: [Short descriptive title]

**As a** [specific user type with context],
**I want** [concrete action the user takes — not what the system does],
**so that** [the value to the user — why they care, not how it works].
```

### Rules for Each Clause

**User type clause:**
- Must be a specific person from Step 1, not a generic role
- Include situational context when it matters: "a returning user who has saved items in their cart"

**Action clause:**
- Describes what the user does, not what the system does
- Bad: "I want the system to send me a notification"
- Good: "I want to receive a notification when my build fails"
- Must be a single, discrete action — no compound actions with "and"

**Value clause:**
- States the benefit to the user, not the implementation mechanism
- Bad: "so that the database is updated"
- Good: "so that I can track which items I have already reviewed"
- Must answer "why would the user care about this?"

---

## Step 3: Write Gherkin Acceptance Criteria

Every story must have acceptance criteria written in Gherkin format. Gherkin makes criteria unambiguous and directly translatable to automated tests.

```gherkin
Scenario: [Descriptive name of the scenario]
  Given [precondition — the state of the world before the action]
  When [action — what the user does]
  Then [outcome — what the user observes]
```

### Rules for Gherkin Criteria

1. **One scenario per behaviour.** If a scenario has multiple `When` steps, split it.
2. **Given sets up context, not actions.** `Given I am logged in` is context. `Given I click the login button` is an action — put actions in `When`.
3. **Then describes observable outcomes.** `Then the database is updated` is not observable to the user. `Then I see a confirmation message "Item saved"` is observable.
4. **Use concrete values, not placeholders.** `When I enter "john@example.com"` is better than `When I enter a valid email`.
5. **Include the negative case.** For every happy-path scenario, write the corresponding error scenario.

### Example

```gherkin
Scenario: Successful password reset request
  Given I am on the login page
  And I have a registered account with email "user@example.com"
  When I click "Forgot password"
  And I enter "user@example.com" in the email field
  And I click "Send reset link"
  Then I see the message "Check your email for a reset link"
  And an email is sent to "user@example.com" within 60 seconds

Scenario: Password reset with unregistered email
  Given I am on the login page
  When I click "Forgot password"
  And I enter "unknown@example.com" in the email field
  And I click "Send reset link"
  Then I see the message "Check your email for a reset link"
  And no email is sent
  # Security: same message shown to prevent email enumeration
```

---

## Step 4: Apply the ISC Splitting Test

Every acceptance criterion (Gherkin scenario) must pass all three checks:

### Independent
Can this scenario be verified without first executing another scenario? If Scenario B requires Scenario A to have run first, they are not independent — either merge them or restructure so B sets up its own preconditions in the `Given` block.

### Small
Does this scenario test exactly one behaviour? If the `Then` block asserts multiple unrelated things, split into separate scenarios. Multiple related assertions (e.g., "Then I see the item in the list And the count updates to 5") are fine if they are consequences of the same action.

### Complete
Does this scenario cover the boundary? Check:
- What happens with empty input?
- What happens with maximum-length input?
- What happens with special characters?
- What happens when the user does not have permission?
- What happens with concurrent access?

If any boundary is missing, add a scenario for it.

---

## Step 5: Document Edge Cases

For every story, enumerate edge cases explicitly. Do not leave them implicit. Common categories:

| Category | Questions to answer |
|----------|-------------------|
| **Empty state** | What does the user see when there is no data yet? First-time experience? |
| **Error handling** | What happens on network failure? Timeout? Invalid input? Server error? |
| **Permissions** | What happens if the user lacks permission? Expired session? |
| **Concurrency** | What if two users act on the same item simultaneously? |
| **Scale** | What happens with 0 items? 1 item? 1,000 items? 100,000 items? |
| **Accessibility** | Can the entire flow be completed with keyboard only? With a screen reader? |
| **Undo/recovery** | Can the user reverse the action? What is the recovery path for mistakes? |

Write a Gherkin scenario for each edge case that could affect user experience. Minor edge cases (purely cosmetic at extreme scale) can be noted without full Gherkin.

---

## Step 6: Define Anti-Requirements

List what this story deliberately does NOT cover. Anti-requirements prevent scope creep and make implicit exclusions explicit.

Format:
```markdown
**Anti-requirements:**
- This story does NOT cover bulk operations — that is a separate story (US-[N])
- This story does NOT handle the admin workflow — admin stories are in US-[N] through US-[N]
- This story does NOT include email notifications — notifications are tracked in [reference]
```

Every anti-requirement should reference where the excluded behaviour IS tracked (another story, a future initiative, or "out of scope entirely").

---

## Step 7: Story Sizing Validation

Before finalising, validate each story against these size constraints:

- **Too small**: A story that takes less than half a day is probably a task, not a story. Combine it with related work.
- **Right size**: Completable by one engineer in 1-5 days, including tests.
- **Too large**: If an engineer would need more than one week, split the story further. Apply the INVEST criteria to find the split point.

---

## Output Format

Group related stories under a feature heading. Number stories sequentially.

```markdown
# User Stories: [Feature Name]

## User Types
1. **[Type A]** — [one-line description with context]
2. **[Type B]** — [one-line description with context]

---

## [Feature Area 1]

### US-1: [Title]

**As a** [specific user type],
**I want** [action],
**so that** [value].

**Acceptance Criteria:**

\```gherkin
Scenario: [Happy path]
  Given ...
  When ...
  Then ...

Scenario: [Error case]
  Given ...
  When ...
  Then ...

Scenario: [Edge case]
  Given ...
  When ...
  Then ...
\```

**Edge Cases:**
- [Edge case not covered by Gherkin scenarios, noted for awareness]

**Anti-requirements:**
- Does NOT cover [excluded behaviour] — tracked in [reference]

**Size:** [S/M/L]

---
```

Write the output to a file if writing more than 3 stories: `docs/stories-[feature-name].md`.
