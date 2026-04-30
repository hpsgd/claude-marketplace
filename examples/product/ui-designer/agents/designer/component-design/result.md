# Result: Component design

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17/18 criteria met (94%) |
| **Evaluated** | 2026-04-30 |

---

## Output

The following simulates what the designer agent would produce for the Clearpath onboarding wizard prompt. This is a full component specification a developer or product team could act on directly.

---

## Component Spec: OnboardingWizard

### Purpose

A multi-step wizard that guides new Clearpath users through workspace setup, team invitation, integration connection, and first project creation — completing in a known, finite sequence with persistent progress visibility.

### Pre-flight: Design system audit

**Existing components inspected:** Input, Button, Avatar, Card

| Existing Component | Decision | Justification |
|---|---|---|
| `Input` | **Reuse** | Covers workspace name, logo URL, timezone select, and all email invite fields |
| `Button` | **Reuse** | Back / Next / Skip navigation; primary and secondary variants already exist |
| `Avatar` | **Reuse** | Team-member preview row after email entry — renders initials when no image |
| `Card` | **Reuse** | Template selection grid in Step 4; each template is a selectable Card |
| Step indicator / progress | **Create** | No existing primitive represents ordered, named steps with current / complete / upcoming states. A `ProgressBar` (if one exists) only shows percentage — it does not name steps or carry `aria-current="step"` semantics. A new `WizardStepIndicator` is required. |

---

### Pattern decision

**Create** `WizardShell` — orchestrates step rendering, progress tracking, and navigation state. No existing component manages multi-step form flow.

**Create** `WizardStepIndicator` — step-labelled progress component. Justification above.

**Reuse** Input, Button, Avatar, Card as specified in the audit table.

---

### Props

#### WizardShell

| Prop | Type | Default | Required | Description |
|---|---|---|---|---|
| `steps` | `WizardStep[]` | — | Yes | Ordered array of step configs (label, component, required) |
| `currentStep` | `number` | `0` | No | Controlled current step index |
| `onStepChange` | `(step: number) => void` | — | No | Callback on step navigation |
| `onComplete` | `() => void` | — | Yes | Called when all required steps are done |
| `onAbandon` | `() => void` | — | No | Called when user presses Esc or explicit exit |

#### WizardStepIndicator

| Prop | Type | Default | Required | Description |
|---|---|---|---|---|
| `steps` | `{ label: string; status: 'upcoming' \| 'current' \| 'complete' }[]` | — | Yes | Step labels and status |
| `orientation` | `'horizontal' \| 'vertical'` | `'horizontal'` | No | Layout direction |

---

### States (ALL states — no exceptions)

#### WizardShell

| State | Behaviour | Visual treatment |
|---|---|---|
| **Default** | Step rendered, inputs idle | Standard step content; Next enabled if required fields valid |
| **Hover** | Cursor over Next / Back / Skip buttons | Button shadow lifts, colour shifts per Button spec |
| **Focus** | Keyboard focus on any interactive element | 2px focus ring (offset, brand accent colour, WCAG AA) on Input, Button, Card |
| **Active** | Button being pressed | Scale 0.98, deeper shadow per Button spec |
| **Disabled** | Next button when required fields unfilled | `disabled` prop set; opacity 0.4; `cursor-not-allowed`; no pointer events |
| **Loading** | Async operation in progress (integration OAuth, form submit) | Spinner overlay on step content; Next replaced with non-interactive "Connecting…" button; `aria-busy="true"` on step region |
| **Error** | Validation failure or async error | Inline error below offending field; step does not advance; error summary at step top via `aria-live="polite"` |
| **Empty** | Step 3 (integration) before any selection | Illustrated prompt: "Choose an integration to connect" with GitHub / Jira / Slack tiles and "Skip for now" link below |

---

### Per-step breakdown

#### Step 1: Workspace setup (required — cannot skip)

**Fields:** Workspace name (Input, required), Logo URL or upload (Input, optional), Timezone (Input as select, required, default to browser-detected)

**Validation:**
- Workspace name: required, 2–64 chars, unique (async check on blur)
- Name taken → inline error: "This name is already in use. Try another."
- Timezone not selected → "Please select a timezone"

**Can skip:** No. Next disabled until name + timezone valid.

---

#### Step 2: Invite team members (optional — can skip)

**Fields:** Up to 5 email Inputs; add-another link below last filled field; Avatar row showing initials per valid entry

**Validation:**
- Valid format: RFC 5322 email pattern; validated on blur and on Next
- Max 5 emails: 6th field does not appear; counter shows "X of 5 added"
- Duplicate email: "This email has already been added"
- Malformed: "Enter a valid email address"
- Partial list (e.g. 2 of 5 filled) is valid

**Error states:** Field border shifts to error colour; error message below field; errors resolved before Next enables.

**Can skip:** Yes. "Skip for now" link below fields — solo users must not be trapped.

**Avatar preview:** Renders initials extracted from email local part immediately on valid entry (no server call).

---

#### Step 3: Connect integration (optional — can skip)

**Default / empty state:** Three selectable integration Cards (GitHub, Jira, Slack) plus "Skip for now" secondary Button link below.

**Primary path — Connect:**
1. User clicks a tile → Card enters selected state (border highlight, checkmark)
2. User clicks "Connect [Integration]" primary Button
3. OAuth flow initiates
4. Loading state: step content overlaid with spinner; button in loading state; `aria-live="polite"` announces "Connecting to GitHub"
5. OAuth stalls >10s → fallback: "This is taking longer than expected. You can wait or skip and connect later." with "Keep waiting" and "Skip for now" actions
6. OAuth error → "Couldn't connect to GitHub. Try again or skip for now."
7. OAuth success → step advances automatically

**Secondary path — Skip:**
- "Skip for now" always visible below tiles (secondary variant, not hidden)
- Skipping triggers deferred re-engagement: onboarding email Day 7 — "You haven't connected an integration yet — it takes 30 seconds"

**Can skip:** Yes.

---

#### Step 4: Create first project from template (required — cannot skip)

**Layout:** Grid of template Cards (Software sprint, Marketing campaign, Client work, Blank project). One must be selected.

**Interaction:**
- Single-select; selected Card shows border highlight and checkmark
- Project name Input appears after template selection; pre-filled with template name, editable
- Next disabled until template selected and name non-empty

**Validation:**
- Template selection required (Next disabled, not an error state — empty state guides selection)
- Project name: required, 2–64 chars

**Can skip:** No. User exits wizard with a usable first project.

---

### Responsive behaviour

| Breakpoint | Layout |
|---|---|
| **Desktop** (> 1024px) | Two-column: `WizardStepIndicator orientation="vertical"` in fixed 240px left panel; step content fluid in right panel. Next / Back right-aligned at bottom of content. |
| **Tablet** (768–1024px) | Single-column: `WizardStepIndicator orientation="horizontal"` at top, labels collapsed to current step only ("Step 2 of 4: Invite team"). Content below full-width. Next / Back full-width stacked. |
| **Mobile** (< 768px) | Out of scope per prompt — desktop and tablet only. Define in future iteration. |

**Rules applied:**
- All buttons minimum 44×44px touch target on tablet (`min-h-[44px] min-w-[44px]`)
- No horizontal scroll at any supported breakpoint
- Step indicator position differs at each breakpoint — vertical left panel vs horizontal top bar

---

### Accessibility (WCAG 2.1 AA)

| Requirement | Implementation |
|---|---|
| **Keyboard — navigation** | Tab cycles all interactive elements in current step; Shift+Tab reverses; Enter advances (Next); Esc triggers `onAbandon` |
| **Keyboard — step indicator** | Read-only; screen readers get step context from `aria-current="step"` on the active step region, not from the indicator |
| **Screen reader — step regions** | Each step: `<section role="region" aria-label="Step N: [Step Name]">`; active step `aria-current="step"` |
| **Screen reader — progress** | `WizardStepIndicator` uses `<ol>` with `<li>` per step; active: `aria-current="step"`; complete: `aria-label="[Name] — complete"` |
| **Screen reader — errors** | Error summary in `aria-live="polite"` region at step top; each field error via `aria-describedby` pointing to error message `id` |
| **Screen reader — loading** | `aria-busy="true"` on step region; `aria-live="polite"` announces "Connecting to [Integration]" |
| **Colour contrast** | Text ≥ 4.5:1; error colour 4.5:1; focus ring 3:1 against adjacent colours |
| **Focus management** | Step advance: focus moves to step `h2`. Error: focus moves to error summary. Modal close: focus returns to trigger. |
| **Reduced motion** | Spinner respects `prefers-reduced-motion`; substitutes pulsing opacity for rotation |

---

### Usage examples

```tsx
// Four-step Clearpath onboarding
<WizardShell
  steps={[
    { label: 'Workspace setup', component: <WorkspaceStep />, required: true },
    { label: 'Invite team', component: <InviteStep />, required: false },
    { label: 'Connect integration', component: <IntegrationStep />, required: false },
    { label: 'First project', component: <ProjectStep />, required: true },
  ]}
  onComplete={handleWizardComplete}
  onAbandon={handleWizardAbandon}
/>

// Controlled with external step tracking
<WizardShell
  steps={steps}
  currentStep={currentStep}
  onStepChange={setCurrentStep}
  onComplete={handleComplete}
/>

// WizardStepIndicator standalone (desktop)
<WizardStepIndicator
  orientation="vertical"
  steps={[
    { label: 'Workspace setup', status: 'complete' },
    { label: 'Invite team', status: 'current' },
    { label: 'Connect integration', status: 'upcoming' },
    { label: 'First project', status: 'upcoming' },
  ]}
/>
```

---

### Design notes

- **Skip is first-class.** Steps 2 and 3 are optional. "Skip for now" is a secondary-variant Button — visible and not punishing. Hiding it would trap solo users.
- **Required steps use disabled Next, not error messages.** Before required fields are filled, Next is disabled with a tooltip "Complete required fields to continue." No angry red before the user has tried.
- **OAuth timeout is a designed state.** The 10-second fallback is in the spec because OAuth flows stall regularly. Designing only the happy path produces a broken experience on slow connections.
- **Avatar in invite step provides confidence.** Initials appear immediately on valid email entry — "I got it" without a server call.
- **Step 4 is required because empty is worthless.** A user who finishes onboarding with no project has nothing to do. The product value is the first project.

---

## Evaluation

### Criteria

- [x] PASS: Checks the existing design system first and explicitly identifies which existing components (Input, Button, Avatar, Card) can be reused versus what needs to be created — Pre-Flight Step 1 mandates finding the design system and searching for similar components before proposing anything; Step 2 requires a Reuse / Extend / Create decision per UI element with justification for any Create

- [x] PASS: Documents all 8 required component states for the wizard: Default, Hover, Focus, Active, Disabled, Loading, Error, Empty — Section 3 "States (ALL required — no exceptions)" enumerates all 8 with behaviour and visual treatment columns; "no exceptions" language is explicit

- [x] PASS: Specifies ARIA roles, labels, and keyboard navigation requirements — not deferred to a future accessibility pass — Section 5 Accessibility is a mandatory spec section covering ARIA role, label, live regions, Tab/Enter/Space/Escape, and focus management; the "Accessibility is a constraint, not a feature" opening and the Decision Checkpoint blocking removal of accessibility requirements both enforce non-deferral

- [x] PASS: Addresses the step indicator / progress component as Reuse / Extend / Create with justification — Pre-Flight Step 2 requires a Pattern Decision for every UI element; a step indicator is a UI element; Create justification is mandatory

- [x] PASS: Specifies responsive behaviour for both desktop and tablet breakpoints — Section 4 Responsive Behaviour mandates a table with Tablet (768-1024px) and Desktop (>1024px) breakpoints as required spec output

- [x] PASS: Documents the error state for each step — Error is one of the 8 mandatory states; Interaction Design Flow Mapping requires error paths covering "validation error, network error, timeout"

- [~] PARTIAL: Specifies loading states for async operations — Loading is mandatory in the 8-state table; the definition covers it at the component-state level but does not require differentiated loading treatment per async operation; an OAuth integration connection step (5-15s roundtrip) and a fast form submission would receive the same generic "spinner, not interactive" treatment unless the designer chose to go deeper unprompted

- [x] PASS: Produces output in a structured component specification format with named sections — the Output Format section provides an explicit named template: Purpose, Pattern Decision, Props, States, Responsive, Accessibility, Usage Examples, Design Notes

### Output expectations

- [x] PASS: Output addresses each of the 4 wizard steps explicitly — workspace setup, team invite, integration connection, project from template — with relevant inputs and interactions per step

- [x] PASS: Design-system reuse decisions are explicit per primitive — Input, Button, Avatar, Card all decided with justification; WizardStepIndicator identified as Create with reasoning

- [x] PASS: Progress / step-indicator decided explicitly as Create with reasoning — no existing primitive serves ordered named-step layout with `aria-current="step"` semantics

- [x] PASS: All 8 component states documented for the wizard shell — Default, Hover, Focus, Active, Disabled, Loading, Error, Empty — all present

- [x] PASS: Accessibility covers ARIA roles (`role="region"`, `aria-current="step"`), labels, and keyboard navigation (Tab, Enter to advance, Esc to abandon)

- [x] PASS: Team-invite email validation addresses valid format, max 5 emails, duplicate handling, malformed entry — with per-field error states

- [x] PASS: Integration "or skip" branch designed explicitly — primary Connect path and secondary Skip link designed; Day 7 deferred re-engagement email specified

- [x] PASS: Responsive behaviour for desktop AND tablet — single-column with horizontal indicator on tablet; two-column with vertical indicator on desktop; step indicator position specified at each breakpoint

- [x] PASS: Can-skip vs cannot-skip per step — workspace required, team invite skippable, integration optional, first project required with reasoning

- [~] PARTIAL: Loading state for integration OAuth specifically — spinner, "Connecting to GitHub…" message, and 10-second stall fallback specified; form submission loading on Steps 1 and 4 addressed at the shell level but not broken out per step

### Notes

The definition is well-suited to this scenario. The mandatory Pre-Flight audit, the non-negotiable 8-state table, and the Create-justification requirement directly address the rubric's most specific demands.

The one consistent gap is loading-state granularity. The definition mandates a Loading state but does not require per-operation loading treatment. The OAuth roundtrip is qualitatively different from a form submission — a 5-15 second wait with an external auth window needs its own messaging. The simulated output covers this because it is a reasonable design call; the definition does not mandate it.

The "can-skip vs cannot-skip" criterion is covered by inference (Disabled state + exit points + Error-prevention principle) rather than a named concept. The definition produces the right behaviour without using that vocabulary explicitly.
