---
name: write-story-map
description: "Create a user story map — a spatial arrangement of stories along a narrative backbone. Produces a backbone of user activities, a walking skeleton, and release slices. Use when planning a new feature area, epic, or release to ensure coverage and sequence."
argument-hint: "[feature area, epic, or user workflow to map]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Create a user story map for $ARGUMENTS.

Follow every step below. The output must be a complete story map that a team can use to plan releases — not a flat backlog list.

---

## Step 1: Define the User and Their Goal

Before mapping any stories, establish the framing:

1. **Who is the user?** — specific role in a specific context, not a generic label. "A hiring manager reviewing candidates for an open role" not "a user"
2. **What is their goal?** — the end-to-end outcome they want to achieve. "Hire the best candidate for the role within 30 days" not "use the recruiting tool"
3. **Where does the journey start and end?** — the first action and the final success state. "Starts: creates a job posting. Ends: extends an offer that is accepted"
4. **What existing materials describe this workflow?** — check for PRDs, user stories, journey maps, or process documentation in the repo

Document:

| Field | Description |
|-------|-------------|
| **User** | [Specific role + context] |
| **Goal** | [End-to-end outcome] |
| **Journey start** | [First action] |
| **Journey end** | [Success state] |
| **Scope boundary** | [What is explicitly excluded from this map] |

---

## Step 2: Build the Backbone

The backbone is the sequence of high-level **activities** the user performs to achieve their goal. Activities read left-to-right as a narrative.

### Rules for Activities

- **Activities are verb phrases** — "Review Applications", "Schedule Interviews", "Make Decision" — not nouns
- **Activities are chronological or logical** — they follow the order the user naturally performs them
- **3-7 activities is typical** — fewer than 3 means you are too abstract; more than 7 means you are too granular
- **Activities are NOT features** — "Use the Dashboard" is a feature. "Monitor Progress" is an activity

### Example Backbone

```
Create Posting → Source Candidates → Review Applications → Interview → Evaluate → Hire
```

Write each activity with a one-sentence description of what the user is doing and why.

---

## Step 3: Walk the Happy Path

Under each activity, list the **tasks** that make up the minimal happy path — the simplest way to complete each activity successfully.

### Rules for Tasks

- **Tasks are concrete user actions** — "Write job description", "Post to job board", "Read resume"
- **Tasks sit under exactly one activity** — if a task spans two activities, it is too big. Split it
- **Order tasks top-to-bottom by necessity** — most essential tasks at the top, nice-to-haves lower down
- **Each task becomes a user story** — it should be small enough for one engineer to complete in 1-5 days

### Example

```
Create Posting          Source Candidates       Review Applications
├── Write description   ├── Post to job board   ├── View applicant list
├── Set requirements    ├── Share link           ├── Read resume
├── Get approval        ├── Receive referrals    ├── Score candidate
```

The happy path is the top row of tasks — the minimal set that gets the user from start to finish.

---

## Step 4: Add Detail

Below the happy path, add tasks for:

1. **Alternative paths** — other ways to accomplish the activity ("Bulk import candidates" under Source Candidates)
2. **Edge cases** — what happens when things go wrong ("Handle duplicate applications" under Review Applications)
3. **Error handling** — recovery from failures ("Reopen closed posting" under Create Posting)
4. **Supporting tasks** — necessary but not user-facing ("Sync with ATS" under Source Candidates)

Place these below the happy-path tasks, ordered by priority (most important first). Each row down is less critical than the row above.

---

## Step 5: Slice Releases

Draw horizontal lines across the map to define release boundaries. Each slice is a shippable increment.

### Slice 1: Walking Skeleton

The thinnest possible end-to-end slice that demonstrates the full flow. It must:
- Touch every activity in the backbone (at least one task per activity)
- Be deployable and usable (not a prototype — real code, real data)
- Validate the architecture (proves the system can support the full flow)

The walking skeleton is NOT an MVP. It is smaller — it proves the flow works, not that it is valuable to users.

### Slice 2: MVP

The minimum set of tasks that delivers enough value for real users to adopt. It must:
- Include the walking skeleton
- Add enough depth to each activity that users can complete their goal without workarounds
- Be the smallest thing you would put in front of a paying customer

### Slice 3+: Enhancements

Additional tasks that improve the experience, add alternative paths, or handle edge cases. Group them into coherent releases — each release should make a specific aspect noticeably better.

### Slice Rules

- **Every slice must touch every activity** — a release that only covers "Create Posting" is not a slice, it is a component. Users need end-to-end value
- **Walking skeleton first, always** — do not build one activity deeply before proving the full flow works
- **Each slice is independently shippable** — it must work on its own, not depend on a future slice

---

## Step 6: Validate Coverage

Before finalising, verify the map:

| Check | Question | Action if Failing |
|-------|----------|-------------------|
| **Backbone completeness** | Does the backbone cover the user's journey from start to finish? | Add missing activities |
| **No orphan stories** | Does every task sit under an activity? | Move orphans or add a missing backbone activity |
| **Walking skeleton coverage** | Does the walking skeleton include at least one task per activity? | Add missing tasks to the skeleton |
| **Story independence** | Can each task be built and delivered independently? | Split coupled tasks |
| **No hidden activities** | Are there activities the user does outside the product that affect the flow? | Add them or note them as external dependencies |
| **Edge case coverage** | Are error paths and empty states represented? | Add edge case tasks below the happy path |

---

## Rules

- **The backbone tells a story** — read the activities left-to-right as a sentence. If it does not make narrative sense, the ordering or naming is wrong.
- **Walking skeleton = thinnest possible slice that demonstrates the full flow** — not "the most important feature". It must span all activities.
- **Stories above the line are more important than stories below** — vertical position is priority. The team reads the map top-to-bottom.
- **No story exists without an activity above it** — orphan stories indicate a missing backbone activity. Find the activity or discard the story.
- **A story map is not a backlog** — it is a 2D spatial arrangement. If you flatten it into a list, you lose the narrative structure and the release slicing.
- **Do not map what you will not build** — if an activity is out of scope, exclude it from the backbone. Note it in the scope boundary.
- Reference [User Story Mapping](https://www.jpattonassociates.com/user-story-mapping/) by Jeff Patton for the definitive methodology.

---

## Output Format

```markdown
# Story Map: [Feature Area / Epic]

## User and Goal

| Field | Description |
|-------|-------------|
| **User** | [Specific role + context] |
| **Goal** | [End-to-end outcome] |
| **Journey** | [Start] → [End] |
| **Scope boundary** | [What is excluded] |

## Story Map

| | Activity 1 | Activity 2 | Activity 3 | Activity 4 | Activity 5 |
|---|---|---|---|---|---|
| **Backbone** | [Activity name] | [Activity name] | [Activity name] | [Activity name] | [Activity name] |
| **Walking Skeleton** | [Task] | [Task] | [Task] | [Task] | [Task] |
| **MVP** | [Task] | [Task] | [Task] | [Task] | [Task] |
| | [Task] | [Task] | | [Task] | |
| **Enhancement** | [Task] | [Task] | [Task] | [Task] | [Task] |
| | [Task] | | [Task] | | [Task] |
| **Future** | [Task] | [Task] | | [Task] | |

## Release Slices

### Slice 1: Walking Skeleton
- **Goal:** Prove the end-to-end flow works
- **Stories:** [list of tasks from the walking skeleton row]
- **Definition of done:** User can complete the full journey, even if manually or with minimal features

### Slice 2: MVP
- **Goal:** Deliver enough value for real adoption
- **Stories:** [list of tasks from the MVP row]
- **Definition of done:** User can complete their goal without workarounds

### Slice 3: [Enhancement theme]
- **Goal:** [What this release improves]
- **Stories:** [list of tasks]
- **Definition of done:** [Measurable improvement]

## Validation Checklist

- [ ] Backbone covers full user journey (start to finish)
- [ ] No orphan stories (every task has an activity)
- [ ] Walking skeleton touches every activity
- [ ] Each task is independently deliverable
- [ ] Edge cases and error paths are represented
- [ ] Each release slice is independently shippable
```

Write the output to a file: `docs/story-map-[feature].md`.

---

## Related Skills

- `/product-owner:write-user-story` — write detailed user stories (with Gherkin acceptance criteria) for individual tasks from the map.
- `/product-owner:groom-backlog` — prioritise the mapped stories within the backlog.
- `/coordinator:decompose-initiative` — decompose a large initiative before mapping individual features.
