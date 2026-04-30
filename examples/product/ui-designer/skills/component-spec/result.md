# Result: Component spec

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17/18 criteria met (94%) |
| **Evaluated** | 2026-04-30 |

---

## Output

Simulated output for the prompt:

> `/ui-designer:component-spec` for a file upload component that supports drag-and-drop and click-to-browse, with progress indicator and error handling for invalid file types.

---

# FileUpload Component Spec

## Design System Decision

**Decision: Create** — searched for existing upload components. Found `FileInput` (single-file, text input + browse button, no drag-and-drop, no progress indicator) and `DropZone` (drag-and-drop only, no click-to-browse, no progress). Neither covers the combined drag-and-drop + click-to-browse + progress + error flow. A new component is required.

---

## 1. Purpose and Usage Context

**What:** A file upload zone that accepts files via drag-and-drop or click-to-browse, shows upload progress, and surfaces validation errors for invalid file types or sizes.

**When to use:** When the user must upload one or more files as part of a workflow (attaching documents, importing data, uploading assets). Do NOT use for avatar/profile image uploads (use `AvatarUpload`) or for in-line rich-text attachments (use `AttachmentButton` inside `RichTextEditor`).

---

## 2. Props / API

| Prop | Type | Default | Required | Description |
|---|---|---|---|---|
| `accept` | `string` | `'*'` | No | MIME types or file extensions accepted — passed directly to the file picker. E.g. `'.pdf,.docx'`. Shown in empty-state helper text. |
| `maxSizeBytes` | `number` | `10485760` (10 MB) | No | Maximum individual file size in bytes. Shown in empty state. Error if exceeded. |
| `multiple` | `boolean` | `false` | No | Allow selecting multiple files in one operation. |
| `disabled` | `boolean` | `false` | No | Prevents all interaction. |
| `required` | `boolean` | `false` | No | Marks the field as required — exposes `aria-required` and form validation. |
| `onFilesAccepted` | `(files: File[]) => void` | — | Yes | Called with accepted files after validation passes. |
| `onFileRejected` | `(file: File, reason: 'type' \| 'size') => void` | `undefined` | No | Called for each rejected file with the rejection reason. |
| `onUploadProgress` | `(file: File, percent: number) => void` | `undefined` | No | Called as upload progresses. |
| `onUploadComplete` | `(file: File) => void` | `undefined` | No | Called when a file finishes uploading. |
| `onUploadError` | `(file: File, error: Error) => void` | `undefined` | No | Called if upload fails server-side. |
| `label` | `string` | `'Upload files'` | No | Accessible label for the drop zone region. |
| `hint` | `ReactNode` | `undefined` | No | Optional helper content rendered below the drop zone. |

---

## 3. Variants

| Variant | Visual treatment | Semantic meaning | When to use |
|---|---|---|---|
| `default` | Dashed border `color-border-default`, neutral background `color-surface-subtle` | Standard upload affordance | Most upload scenarios |
| `compact` | Reduced height, icon + text inline | Same affordance, less visual weight | When vertical space is constrained (e.g. inside a dense form) |
| `error` | Dashed border `color-border-error`, `color-surface-error-subtle` background | Validation failed | Applied automatically when a file is rejected — not set by consumers directly |

Default is `default`. When in doubt, use `default`.

---

## 4. States — Complete Coverage Table

| State | Visual treatment | Behaviour | Transitions to |
|---|---|---|---|
| **Default** | Dashed border `color-border-default` (2px, `radius-lg`), `color-surface-subtle` background, cloud-upload icon (`color-icon-secondary`), "Drag files here or click to browse" label (`color-text-secondary`), accepted types + max size below in `text-sm color-text-tertiary` | Mouse enters triggers Hover; Tab triggers Focus; click opens OS file picker | Hover, Focus |
| **Hover** | Border → `color-border-brand`, background → `color-surface-brand-subtle`, icon → `color-icon-brand`, cursor: `pointer` | Tooltip not added (label is sufficient). Hover clears when mouse leaves. | Default, DragOver |
| **Focus** | 2px solid `color-focus-ring` offset 2px (replaces dashed border); other visual treatment same as Hover | Keyboard-focusable. Enter or Space opens OS file picker. Visible in both light and dark modes. | Default, Active |
| **Active** | Background → `color-surface-brand` (20% opacity), icon scales to 1.05 (150ms ease-out), border solid `color-border-brand` | Applied during mouse-down before file picker opens; also during drag in-flight over the zone (DragOver sub-state). | Default |
| **DragOver** (sub-state of Active) | Border solid `color-border-brand` (3px), background `color-surface-brand-subtle`, icon animates downward 4px (bounce, 300ms ease), label changes to "Drop to upload" | `dragenter` triggers; `dragleave` clears. Counter guards against flickering from child `dragenter` events. | Default (on drop or dragleave) |
| **Disabled** | Border dashed `color-border-disabled`, background `color-surface-disabled`, icon `color-icon-disabled`, text `color-text-disabled`, cursor: `not-allowed` | `aria-disabled="true"`, `tabIndex={-1}`, pointer events blocked. No hover effects. | — |
| **Loading** | Drop zone replaced by file rows: filename (`text-sm font-medium`), progress bar (`color-fill-brand`, `radius-full`, animates 0% to actual %), percentage label right-aligned, cancel icon button. Zone dimensions preserved — no layout shift. | Non-interactive during upload. If `multiple=true`, each file gets its own row stacked vertically. | Default (on complete), Error (on failure) |
| **Error** | File row: filename, red X icon `color-icon-error`, message `text-sm color-text-error` e.g. "Only .pdf and .docx files are supported. You tried to upload an .xlsx file." or "File exceeds the 10 MB limit (uploaded: 14.2 MB).". Drop zone persists above error rows so user can retry without scrolling. | Error announced via `aria-live="assertive"`. File rejected without blocking form submission for already-accepted files. Dismiss button clears each error row. | Default (on dismiss or re-upload) |
| **Empty** | Same as Default — the empty state IS the default state for this component. Helper text shows accepted types and max size. | "Click to browse" acts as primary CTA. | Default |
| **Selected** | N/A — selection is not a concept for this component; files are uploaded, not selected within it. | — | — |
| **Read-only** | N/A — file upload is always interactive or disabled. | — | — |

**Compound state: DragOver + Disabled** — Disabled takes full precedence; drop zone ignores all drag events.

**Compound state: Loading + multiple files** — each file has its own progress row. New files can be dropped while others upload (unless `multiple=false`, in which case the drop zone is hidden during Loading).

---

## 5. Responsive Behaviour

| Breakpoint | Width | Layout changes | Content changes |
|---|---|---|---|
| **Mobile** | < 640px (`sm`) | Full-width drop zone, reduced height (96px vs 160px desktop), stacked within form | "Drag files here or" text hidden (drag is impractical on touch); label becomes "Tap to browse". Full zone is touch target (minimum 44px height met). |
| **Tablet** | 640–1024px (`sm`–`lg`) | Full-width, 128px height. Both drag and tap affordances shown. | "Drag files here or click to browse" — both modes mentioned. |
| **Desktop** | > 1024px (`lg`+) | Full-width, 160px height. | Full label and hint visible. |

No horizontal scrolling at any breakpoint. Progress rows scroll within the component if many files are uploading. Drop zone maintains minimum 320px width.

---

### Performance Considerations

N/A — this component does not render large datasets. File upload progress is managed via the `onUploadProgress` callback; the consumer owns server-side upload logic.

---

## 6. Accessibility Requirements

### Keyboard Navigation

| Key | Action |
|---|---|
| `Tab` | Focus moves to the drop zone |
| `Shift+Tab` | Focus moves away from the drop zone |
| `Enter` / `Space` | Opens OS file picker |
| `Escape` | Cancels an in-progress upload (focus moves to cancel button, Escape activates it) |
| `Tab` (during upload) | Cycles: drop zone → cancel button(s) per uploading file → next focusable element |

### Screen Reader

- **Role:** `role="region"` wrapping the drop zone. The upload input is `<input type="file" />` (visually hidden, accessible to assistive tech).
- **Label:** `aria-label` set from the `label` prop (default: "Upload files"). Region and input share the label via `aria-labelledby`.
- **State announcements:**
  - Drag enters zone: `aria-live="polite"` announces "Ready to drop files".
  - Upload starts: `aria-live="polite"` announces "Uploading [filename]...".
  - Upload completes: "Upload complete: [filename]".
  - File rejected: `aria-live="assertive"` announces the full error message immediately.
- **Description:** `aria-describedby` points to the hint element (accepted types, max size) so screen readers announce it on focus.
- **Disabled:** `aria-disabled="true"` on the region; hidden input also `disabled`.

### Colour and Contrast

- All text meets 4.5:1 (normal text) and 3:1 (large text / icons) in both light and dark mode.
- Error state uses `color-icon-error` icon AND error text — not colour alone.
- Progress bar `color-fill-brand` against `color-fill-track` meets 3:1.
- Focus ring `color-focus-ring` meets 3:1 against all adjacent surfaces.

### Focus Management

- On mount: no automatic focus (standard form field behaviour).
- On file picker close (cancelled): focus returns to the drop zone.
- On file picker close (files selected): focus returns to the drop zone; upload begins.
- On error dismiss: focus returns to the drop zone.
- Focus not trapped — this is not a modal.
- Focus ring visible in both light and dark mode.

---

## 7. Dark Mode

- [x] All colours use semantic tokens — no hardcoded hex values in this spec.
- [x] Contrast ratios verified for dark mode (error text, progress bar, drop zone border re-checked).
- [x] No images or illustrations — not applicable.
- [x] No shadows — elevation handled by border only.
- [x] Dashed border `color-border-default` visible against `color-surface-subtle` in dark mode.

---

## 8. Animation and Motion

| Animation | Element | Duration | Easing | Reduced-motion fallback |
|---|---|---|---|---|
| Border colour change (Default → Hover / DragOver) | Drop zone border | 150ms | `ease-out` | Instant colour change |
| Background colour change (Default → Hover / DragOver) | Drop zone background | 150ms | `ease-out` | Instant |
| Icon downward nudge (DragOver) | Upload icon | 300ms | `ease-in-out` bounce | Static — icon does not move |
| Progress bar fill | Progress bar | Continuous, tied to real upload % | Linear | No change — tracks real progress |
| Progress bar row entry | Progress bar row | 200ms slide-down + fade-in | `ease-out` | Instant appearance |
| Success / error state transition | Progress bar → result row | 200ms cross-fade | `ease-out` | Instant swap |

All transitions respect `prefers-reduced-motion: reduce`. Maximum micro-interaction duration is 300ms.

---

## 9. Usage Examples

```tsx
// Basic single-file upload
<FileUpload
  accept=".pdf,.docx"
  maxSizeBytes={5 * 1024 * 1024}
  label="Upload contract"
  onFilesAccepted={(files) => uploadToServer(files[0])}
  onUploadProgress={(file, pct) => setProgress(pct)}
  onUploadComplete={(file) => toast.success(`${file.name} uploaded`)}
/>

// Multiple files with rejection handling
<FileUpload
  accept="image/*"
  multiple
  maxSizeBytes={10 * 1024 * 1024}
  onFilesAccepted={(files) => Promise.all(files.map(uploadToServer))}
  onFileRejected={(file, reason) =>
    reason === 'type'
      ? showError(`${file.name} is not an image`)
      : showError(`${file.name} exceeds 10 MB`)
  }
  onUploadError={(file, err) => toast.error(`Failed to upload ${file.name}`)}
/>

// Disabled (uploads locked during processing)
<FileUpload
  accept=".csv"
  disabled
  label="Upload data (unavailable during processing)"
  onFilesAccepted={() => {}}
/>
```

---

## 10. Do / Don't

| Do | Don't |
|---|---|
| Show accepted file types and max size in the empty state | Rely on the OS picker to enforce type restrictions — validate on receipt too |
| Use `aria-live="polite"` for progress, `aria-live="assertive"` for errors | Use `assertive` for progress updates — it will interrupt the user mid-sentence |
| Keep the drop zone visible while files upload (stack progress rows below) | Replace the drop zone with progress rows — both must be visible when `multiple=true` |
| Use `onFileRejected` to show specific, actionable error messages naming accepted types | Show a generic "invalid file" message |
| Preserve component dimensions during Loading | Let layout jump when progress rows appear |
| Test the click-to-browse path with keyboard only | Assume drag-and-drop is the only path that needs accessibility testing |

---

## Related Skills

- `/ui-designer:design-review` — review the implemented component against this spec.
- `/ui-designer:accessibility-audit` — audit the component for WCAG compliance after implementation.

---

## Evaluation

### Criteria (skill definition)

- [x] PASS: Skill requires all 8 interaction states — Section 4 lists Default, Hover, Focus, Active, Disabled, Loading, Error, and Empty explicitly in the coverage table, plus Selected and Read-only. Rules beneath mandate Hover, Focus, Active, and Disabled with "No exceptions."
- [x] PASS: Skill requires ARIA roles, labels, and keyboard navigation as mandatory — Section 6 opens with "Every component must meet WCAG 2.1 AA" and contains named sub-sections for keyboard navigation, screen reader (role, label, state announcements, description), colour and contrast, and focus management. None are marked optional.
- [x] PASS: Skill requires a design system decision (Reuse / Extend / Create) with justification before specifying the component — Section 0 is labelled "MANDATORY — before writing the spec" and requires a stated decision plus justification. A Reuse decision terminates the spec immediately.
- [x] PASS: Skill requires responsive behaviour specification at multiple breakpoints — Section 5 mandates a breakpoint table covering Mobile (< 640px), Tablet (640–1024px), and Desktop (> 1024px) with explicit touch target minimums and no-horizontal-scroll rules.
- [x] PASS: Skill requires a properties/variants table — Section 2 requires a full props table with type, default, required, and description. Section 3 requires a separate variants table with visual treatment, semantic meaning, and when-to-use.
- [x] PASS: Skill requires animation and transition specifications where state changes occur — Section 8 mandates what animates, duration, easing function, `prefers-reduced-motion` handling, and entry/exit animations. Maximum duration limits are prescribed (300ms micro-interactions, 500ms page transitions).
- [~] PARTIAL: Skill requires token references — Section 7 (Dark Mode) explicitly requires semantic tokens for colour. Spacing and typography tokens are never mentioned. Colour tokens are mandated; spacing and typography are not.
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint — lines 1–7 contain all three fields with correct values.

### Output expectations (simulated output)

- [x] PASS: Design-system decision made up front with reasoning — Create, citing that `FileInput` lacks drag-and-drop/progress and `DropZone` lacks click-to-browse/progress. Both gaps are specific.
- [x] PASS: All 8 interaction states documented — Default (drop zone, helper text), Hover (brand border/background), Focus (focus ring, Enter/Space opens picker), Active/DragOver (drag-over sub-state with icon animation), Disabled (aria-disabled, no events), Loading (per-file progress rows, layout preserved), Error (named error messages, zone persists), Empty (same as Default, explained).
- [x] PASS: ARIA/keyboard spec covers `role="region"`, keyboard activation (Enter/Space), and `aria-live` announcements for upload start, completion, and error.
- [x] PASS: Both drag-and-drop AND click-to-browse documented — separate affordances described in states and responsive tables; mobile label changes to "Tap to browse" acknowledging touch.
- [x] PASS: Invalid-file-type error handling specified — error message names accepted types and the rejected extension; file rejected without blocking form.
- [x] PASS: File-size error handling specified — max size shown in empty state; error message shows the specific uploaded size alongside the limit.
- [x] PASS: Progress indicator animated with explicit transitions — entry via slide-down + fade-in (200ms), fill tracks real %, cross-fade to success/error state (200ms), reduced-motion fallbacks for each.
- [x] PASS: Responsive behaviour describes desktop AND mobile — desktop: 160px full-width zone, drag + click; mobile: 96px, drag text hidden, "Tap to browse", 44px touch target maintained.
- [x] PASS: Properties/variants table documents configurable aspects — `accept`, `maxSizeBytes`, `multiple`, `required`, `onFileRejected`, and custom error callbacks are all present.
- [~] PARTIAL: Token references by name — colour tokens named throughout (`color-border-default`, `color-surface-subtle`, `color-fill-brand`, `radius-lg`, etc.). Spacing values are expressed in pixels (96px, 160px, 4px, 44px) rather than spacing tokens. Typography uses Tailwind utility classes (`text-sm`, `font-medium`) rather than token names. Partial: colours and radii are tokenised; spacing and typography are not.

### Notes

The skill is structurally strong. Section 0's mandatory decision gate before any spec content is the most important feature — it prevents spec proliferation by requiring a documented codebase search before work begins. The sample justification in that section directly anticipates a file-upload scenario, which means this test case is precisely what the skill was designed to handle.

The one consistent gap is token reference scope. The dark-mode checklist mandates colour tokens but the skill never mentions spacing or typography tokens. For a drag-and-drop upload zone with a progress bar and error typography, those missing token categories are not trivial. Adding explicit guidance to Section 2 (Props) or Section 4 (States) to reference spacing and typography tokens by name would close this gap.

The `allowed-tools: Read, Glob, Grep` constraint is appropriate — the skill needs to search the codebase before deciding Reuse/Extend/Create and should not have Write access.

The `Related Skills` footer connecting to `/ui-designer:design-review` and `/ui-designer:accessibility-audit` situates the spec step inside a broader verification workflow, which is good practice.
