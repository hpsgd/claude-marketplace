# Component design

A product team needs a multi-step onboarding wizard designed for their B2B SaaS product. The designer agent is asked to produce a component specification.

## Prompt

> We need to design a multi-step onboarding wizard for Clearpath, our B2B project management tool. New users need to:
> 1. Set up their workspace (name, logo, timezone)
> 2. Invite team members (up to 5 emails)
> 3. Connect their first integration (GitHub, Jira, or Slack — or skip)
> 4. Create their first project from a template
>
> We have a design system with existing Input, Button, Avatar, and Card components. The wizard should work on desktop and tablet. Can you design this?

## Output

**Pre-flight: Design System Audit**

| Component | Decision | Justification |
|---|---|---|
| Input | Reuse | Standard text and email inputs cover all form fields |
| Button | Reuse | Primary/secondary variants cover all CTA needs |
| Avatar | Reuse | Used in team invite row to show added members |
| Card | Extend | Existing card lacks full-bleed step layout — extend with `variant="wizard-step"` |
| Step indicator | Create | No existing progress indicator component. New `WizardProgress` required. |

---

### Component Spec: OnboardingWizard

#### Purpose
A multi-step wizard that guides new Clearpath users through workspace setup, team invitation, integration connection, and first project creation.

#### Pattern Decision
Extend (Card) + Create (WizardProgress)

#### Props

| Prop | Type | Default | Required | Description |
|---|---|---|---|---|
| `steps` | `Step[]` | — | Yes | Step definitions |
| `onComplete` | `() => void` | — | Yes | Called on final step completion |
| `onSkip` | `(stepId: string) => void` | — | No | Called when optional step is skipped |
| `initialStep` | `number` | `0` | No | Step index to start on |

#### States

| State | Trigger | Visual |
|---|---|---|
| Default | Initial render | Step 1 active, steps 2-4 inactive |
| Hover | Mouse over interactive element | Pointer cursor, subtle shadow on CTA |
| Focus | Keyboard navigation | 2px focus ring using `color.focus.ring` token |
| Active | Button being pressed | Pressed visual on Button component |
| Disabled | Next button before required fields complete | Button disabled variant, `aria-disabled="true"` |
| Loading | Form submission or integration connection | Button shows spinner, fields disabled, `aria-busy="true"` on form |
| Error | Validation failure or API error | Inline error below affected field, `role="alert"` |
| Empty | Step with no pre-filled content | Helper text and placeholder shown |

#### Responsive

| Breakpoint | Layout |
|---|---|
| Desktop (>1024px) | Wizard in centred modal, max-width 640px, horizontal step indicator |
| Tablet (768-1024px) | Full-width modal, horizontal step indicator, reduced padding |
| Mobile | Out of scope for v1 — document as excluded |

#### Accessibility

| Requirement | Implementation |
|---|---|
| Keyboard | Tab navigates fields, Enter submits current step, Escape focuses Back button |
| Screen reader | `role="main"` on wizard, `aria-label="Clearpath onboarding"`, `aria-current="step"` on active step |
| Live regions | `aria-live="polite"` announces step transitions; `aria-live="assertive"` for validation errors |
| Focus management | Focus moves to first field of new step on step transition |
| Colour contrast | Meets 4.5:1 for all text per design tokens |

#### Per-step error states
- Step 1: Workspace name already taken → "This name is already taken. Try adding your company name."
- Step 2: Invalid email → inline error per field: "Enter a valid email address"
- Step 3: Integration auth failure → error banner: "Couldn't connect to [service]. Check your credentials and try again."
- Step 4: Template load failure → "Couldn't load templates. Try refreshing."

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/8 criteria met (94%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Design system checked first — the agent's Pre-Flight Step 1 requires finding the design system and checking existing components before proposing anything new. Step 2 mandates a Reuse/Extend/Create decision for every UI element, with justification required for Create. This is a mandatory pre-flight, not a suggestion.
- [x] PASS: All 8 states documented — the Component Specification section "States (ALL required — no exceptions)" lists exactly the 8 states: Default, Hover, Focus, Active, Disabled, Loading, Error, Empty. The definition states "If a state doesn't apply, state explicitly: 'Hover: N/A — this is a static display component.'" No states can be omitted without documentation.
- [x] PASS: ARIA roles, labels, keyboard navigation — the Accessibility section of the component spec template is mandatory and includes Keyboard, Screen reader, Colour contrast, Focus management, and Reduced motion rows. The definition's non-negotiables state: "Accessibility is a constraint, not a feature." The Decision Checkpoints list "Removing an accessibility requirement to simplify implementation" as a STOP trigger.
- [x] PASS: Step indicator as Reuse/Extend/Create — the Pre-Flight Step 2 pattern decision applies to every UI element. A step indicator/progress component is a UI element that requires an explicit Reuse/Extend/Create decision with justification. No exception for new components.
- [x] PASS: Responsive behaviour at desktop and tablet — the Responsive Behaviour section of the component spec template is mandatory with a table covering Mobile, Tablet, and Desktop breakpoints. The agent definition requires all breakpoints to be addressed.
- [x] PASS: Error state per step — the Component Specification requires the Error state to be documented in the States table. The Interaction Design section also requires "Error paths — what happens when things go wrong?" Per-step error states follow from applying these requirements to a multi-step form.
- [~] PARTIAL: Loading states for async operations — the States table requires a Loading state entry: "Awaiting data/action | Skeleton or spinner, not interactive." The definition requires the Loading state to be documented but does not require breaking it down per async operation (workspace submit vs integration connect vs template load). Criterion prefix is PARTIAL — maximum 0.5 points.
- [x] PASS: Structured component spec format — the Output Format section specifies named sections: Purpose, Pattern Decision, Props, States, Responsive, Accessibility, Usage Examples, Design Notes. Prose descriptions without this structure do not satisfy the format requirement.

### Notes

The loading states criterion scores PARTIAL per its prefix. The agent definition requires a Loading state in the states table, which covers the general case. It does not require per-async-operation loading state breakdown. A multi-step wizard with three distinct async operations (workspace create, integration OAuth, template fetch) could benefit from per-step loading states in the definition, but this is not currently required.

The Pre-Flight structure is the agent's strongest feature. Reuse/Extend/Create with mandatory justification for Create prevents unnecessary component proliferation. The Decision Checkpoints add enforcement: "Creating a new component when a similar one exists" is an explicit STOP trigger.
