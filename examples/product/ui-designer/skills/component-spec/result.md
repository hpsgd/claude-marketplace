# Component Spec

Scenario: Testing whether the component-spec skill definition requires all 8 interaction states, accessibility requirements, and responsive behaviour as mandatory sections.

## Prompt

> /ui-designer:component-spec for a file upload component that supports drag-and-drop and click-to-browse, with progress indicator and error handling for invalid file types.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

No existing upload components found. **Decision: Create** — no existing component covers drag-and-drop file upload with progress indication. Writing a full spec from scratch.

---

# Component Specification: `FileUpload`

## 0. Design System Decision

**Decision: Create** — searched for existing upload components, file input primitives, dropzone utilities, and progress indicators. The codebase contains no existing UI components. A full spec is required.

---

## 1. Purpose and Usage Context

**What it does:** An interactive drop zone that accepts files via drag-and-drop or click-to-browse, displays upload progress per file, and surfaces validation errors for rejected file types or size limits.

**When to use:**
- When users must attach files to a form (documents, images, CSVs, assets)
- When multi-file upload with per-file feedback is needed
- When file type or size constraints must be communicated and enforced client-side

**Do NOT use when:**
- Only a native file picker is needed with no drag-and-drop or progress (use a plain `<input type="file">` with a styled label)
- Uploading is triggered programmatically, not by user action (use the upload service directly)
- The file is never sent to a server (use `FileReader` inline without this component)

---

## 2. Props / API

| Prop | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| `accept` | `string[]` | `[]` (all types) | No | Accepted MIME types (e.g. `['image/png', 'application/pdf']`). Maps to `<input accept>`. |
| `maxSize` | `number` | `10485760` (10 MB) | No | Maximum file size in bytes per file. |
| `maxFiles` | `number` | `1` | No | Maximum number of files that can be queued simultaneously. |
| `multiple` | `boolean` | `false` | No | Allows selecting multiple files at once. Automatically `true` when `maxFiles > 1`. |
| `disabled` | `boolean` | `false` | No | Disables all interaction. |
| `onFilesAccepted` | `(files: File[]) => void` | — | Yes | Called with accepted files after client-side validation passes. Upload logic lives here. |
| `onFilesRejected` | `(rejections: FileRejection[]) => void` | `undefined` | No | Called with rejected files and their error reasons. |
| `onProgress` | `(fileId: string, percent: number) => void` | `undefined` | No | Called as upload progresses. Drive the `uploadState` prop with this. |
| `uploadState` | `Record<string, UploadEntry>` | `{}` | No | Controlled upload state keyed by a stable file ID. Each entry drives per-file progress and error display. |
| `label` | `string` | `'Upload files'` | No | Accessible label for the drop zone region. |
| `hint` | `string` | `undefined` | No | Secondary hint text shown inside the drop zone (e.g. "PNG, JPG up to 10 MB"). |
| `className` | `string` | `undefined` | No | Additional CSS classes applied to the outer container. |

**Supporting types:**

```ts
interface FileRejection {
  file: File;
  errors: Array<'file-type' | 'file-size' | 'too-many-files'>;
}

interface UploadEntry {
  status: 'pending' | 'uploading' | 'success' | 'error';
  percent: number;          // 0–100
  errorMessage?: string;    // shown when status === 'error'
  fileName: string;
}
```

**Prop design notes:**
- `uploadState` is intentionally controlled — the parent owns upload logic and progress tracking. The component is a pure presentation layer above the file transfer.
- `accept` takes MIME types (not extensions) to match the browser File API. The component derives a human-readable hint string from the array when `hint` is not provided.
- `multiple` is derived from `maxFiles` automatically; prefer setting `maxFiles` over `multiple` directly.

---

## 3. Variants

This component has no `variant` prop — it has a single visual form whose appearance changes with **state** (see Section 4), not with semantic intent.

However, two **layout modes** are available via the `layout` prop:

| Layout | Visual treatment | When to use |
|--------|-----------------|-------------|
| `'zone'` (default) | Full bordered drop area with centred icon and text | Primary upload entry points with visible affordance |
| `'compact'` | Single-line row with paperclip icon and text link | Inline within a form where vertical space is constrained |

---

## 4. States — Complete Coverage Table

### Drop Zone

| State | Visual treatment | Behaviour | Transitions to |
|-------|-----------------|-----------|---------------|
| **Default** | Dashed border (`border-dashed border-2 border-neutral-300`), neutral background, upload icon + label centred | Accepts pointer and keyboard focus | Hover, Focus, Drag-over, Disabled |
| **Hover** | Border colour → `border-primary-400`, background → `bg-primary-50` | Cursor: `pointer`, tooltip not needed | Default, Active |
| **Focus** | 2px offset focus ring (`outline-2 outline-offset-2 outline-primary-500`), same border colour as Hover | Keyboard focus indicator; `Space`/`Enter` opens file picker | Default, Active |
| **Active** | Border → `border-primary-600`, background → `bg-primary-100` | Brief visual press feedback (≤100ms) | Default |
| **Drag-over** | Border solid → `border-primary-500`, background → `bg-primary-50`, icon scales up 10%, instructional text changes to "Drop to upload" | Highlights valid drop target; if dragged file type is invalid: border → `border-error-500`, bg → `bg-error-50`, text → "File type not supported" | Default, Drag-leave, Drop |
| **Drag-over (invalid)** | Border → `border-error-400`, background → `bg-error-50`, icon red | Shows rejection reason inline; blocks drop | Default |
| **Disabled** | Reduced opacity (`opacity-50`), `cursor: not-allowed`, dashed border muted | No drag events, no click, no keyboard activation; `aria-disabled="true"` | — |
| **Loading / Uploading** | Drop zone remains visible; file list below shows per-file progress bars | Drop zone stays active so user can add more files (if `maxFiles` not reached) | Default, Error |
| **Max files reached** | Drop zone visually dimmed, pointer → `not-allowed`, tooltip "Maximum files reached" | Drag-over rejected visually; click does nothing | Clears when a file is removed |
| **Error (zone-level)** | Below the drop zone: red banner with error icon and message | Shown for systemic errors (e.g. network failure affecting all files) | Default on retry |
| **Empty** | Default state | Guides user to drag or click | Default |

### Per-File Entry (in file list below the drop zone)

| State | Visual treatment | Behaviour | Transitions to |
|-------|-----------------|-----------|---------------|
| **Pending** | File icon, name, size, spinner icon | Queued; upload not yet started | Uploading |
| **Uploading** | Progress bar fills left-to-right, percentage label, cancel `×` button | Live `aria-valuenow` on progress bar; cancel removes file | Success, Error |
| **Success** | Green check icon replaces progress bar, file name at full contrast | Non-interactive beyond remove | Removed |
| **Error (file-level)** | Red warning icon, error message below file name (e.g. "Invalid file type: .exe"), retry button | User can retry or remove | Uploading, Removed |
| **Removed** | Animate out (fade + collapse, 200ms) | File entry disappears; `onFilesRejected` not called (user-initiated) | — |

**Compound states:**
- **Uploading + drag-over**: Drop zone accepts new files while previous uploads are in progress. The zone remains active; the file list grows.
- **Max files reached + uploading**: Zone dims (not-allowed) but existing uploads continue.

---

## 5. Responsive Behaviour

| Breakpoint | Width | Layout changes | Content changes |
|-----------|-------|---------------|----------------|
| **Mobile** | < 640px (`sm`) | Drop zone is full-width; hint text is shortened; file list rows stack vertically with name above progress bar | Drag-and-drop is not the primary interaction (touch); click-to-browse is emphasised with a larger tap target; icon and text remain visible |
| **Tablet** | 640–1024px | Standard zone width (matches form column width); file list rows are single-line | All content visible |
| **Desktop** | > 1024px | As designed; max-width constrained to form column (default `max-w-2xl`) | Full label, hint, and file metadata visible |

**Touch targets:** The entire drop zone is the tap target on mobile (minimum 44px height; default zone min-height is 120px). The remove `×` button on each file row is minimum 44×44px.

**Note on drag-and-drop on mobile:** Drag-and-drop is supported on modern iOS/Android but unreliable on older devices. Click-to-browse is always the primary interaction path. Do not hide the "click to browse" affordance at any breakpoint.

**Performance:** N/A — file lists are bounded by `maxFiles` (default 1). No virtualisation required. If `maxFiles` exceeds 50, consider a table layout with virtualisation.

---

## 6. Accessibility Requirements

### Keyboard Navigation

| Key | Action |
|-----|--------|
| `Tab` | Moves focus into the drop zone (single tab stop); subsequent `Tab` moves to the first file entry's remove/retry button |
| `Shift+Tab` | Reverse focus movement |
| `Enter` / `Space` | Opens the native file picker (when drop zone is focused) |
| `Escape` | Closes the file picker if open; no effect on the drop zone itself |
| `Tab` (within file list) | Moves between Cancel / Retry / Remove buttons per file entry |
| `Enter` / `Space` (on file action button) | Activates cancel, retry, or remove |

**Focus management:**
- On file added: focus remains on the drop zone (user may want to add more files)
- On file removed via keyboard: focus moves to the previous file's remove button, or back to the drop zone if the list is now empty
- The drop zone is a single `div[role="button"]` with `tabIndex={0}` — it is one tab stop, not a collection

### Screen Reader

- **Role:** Drop zone uses `role="button"` with `aria-label` derived from the `label` prop (e.g. `aria-label="Upload files"`)
- **Instructions:** An `aria-describedby` element (visually hidden) reads: "Press Enter or Space to browse files. Accepted types: PNG, PDF. Maximum size: 10 MB."
- **Drag-over state:** `aria-live="polite"` region announces "File type accepted — drop to upload" or "File type not supported" during drag-over
- **Upload progress:** Each progress bar uses `role="progressbar"`, `aria-valuenow={percent}`, `aria-valuemin={0}`, `aria-valuemax={100}`, `aria-label="{fileName} upload progress"`
- **Status changes:** An `aria-live="polite"` region announces: "Upload complete: {fileName}" on success; "{fileName} failed: {errorMessage}" on error
- **Error messages:** File-level errors are associated with their file entry via `aria-describedby`. Zone-level errors use `role="alert"` for immediate announcement.

### Colour and Contrast

- All text: minimum 4.5:1 against background in default, hover, and drag-over states
- Progress bar fill colour against its track: minimum 3:1
- Error red (`error-500`) and success green (`success-600`) must meet 3:1 against icon backgrounds
- Drag-over state colour changes are always accompanied by a text change ("Drop to upload") — colour is not the sole indicator

### Focus Management

- Drop zone focus ring: 2px solid, 2px offset, `outline-primary-500` in light mode / `outline-primary-400` in dark mode
- Focus ring must not be clipped by overflow: the container must not have `overflow: hidden` without accounting for the offset
- No focus trap — the component is inline, not a modal

---

## 7. Dark Mode

- [ ] Drop zone border: `border-neutral-600` dark / `border-neutral-300` light (semantic token `--color-border-default`)
- [ ] Drop zone background: `bg-neutral-900` dark / `bg-white` light
- [ ] Drag-over fill: `bg-primary-900` dark / `bg-primary-50` light
- [ ] Error fill: `bg-error-950` dark / `bg-error-50` light
- [ ] Progress bar track: `bg-neutral-700` dark / `bg-neutral-200` light
- [ ] Progress bar fill: `bg-primary-400` dark / `bg-primary-600` light (re-check contrast against track in dark mode — target 3:1)
- [ ] Success icon: `text-success-400` dark / `text-success-600` light
- [ ] Shadows: none used; elevation communicated via border, not box-shadow
- [ ] All values use semantic design tokens, not hardcoded hex

---

## 8. Animation and Motion

| Interaction | Animation | Duration | Easing |
|-------------|-----------|----------|--------|
| Drag-over enter | Border colour + background crossfade | 120ms | `ease-out` |
| Drag-over leave | Crossfade back to default | 80ms | `ease-in` |
| Drop zone hover | Border + background crossfade | 100ms | `ease-out` |
| File entry appear | Fade-in + height expand from 0 | 200ms | `ease-out` |
| File entry remove | Fade-out + height collapse to 0 | 200ms | `ease-in` |
| Progress bar fill | Width transition | continuous, no easing override | linear |
| Upload success (check icon) | Scale from 0.5 → 1 | 150ms | `ease-out` |

All animations must be wrapped in a `prefers-reduced-motion` check:

```css
@media (prefers-reduced-motion: reduce) {
  /* Replace transitions with instant state changes */
  .file-upload-* { transition: none; }
}
```

In JavaScript/React: use `window.matchMedia('(prefers-reduced-motion: reduce)')` to conditionally skip `framer-motion` or CSS transition classes.

Maximum duration: 200ms for micro-interactions. No animation exceeds 300ms.

---

## 9. Usage Examples

```tsx
// Basic single-file upload
<FileUpload
  accept={['image/png', 'image/jpeg']}
  maxSize={5 * 1024 * 1024}
  hint="PNG or JPG up to 5 MB"
  onFilesAccepted={(files) => uploadFile(files[0])}
/>
```

```tsx
// Multi-file with controlled progress state
const [uploadState, setUploadState] = useState<Record<string, UploadEntry>>({});

<FileUpload
  accept={['application/pdf', 'text/csv']}
  maxFiles={5}
  maxSize={10 * 1024 * 1024}
  hint="PDF or CSV, up to 5 files, 10 MB each"
  uploadState={uploadState}
  onFilesAccepted={(files) => {
    files.forEach((file) => {
      const id = crypto.randomUUID();
      setUploadState((s) => ({
        ...s,
        [id]: { status: 'pending', percent: 0, fileName: file.name },
      }));
      startUpload(file, id, (percent) =>
        setUploadState((s) => ({
          ...s,
          [id]: { ...s[id], status: 'uploading', percent },
        }))
      );
    });
  }}
  onFilesRejected={(rejections) => {
    rejections.forEach(({ file, errors }) =>
      toast.error(`${file.name}: ${errors.join(', ')}`)
    );
  }}
/>
```

```tsx
// Compact layout, disabled during form submission
<FileUpload
  layout="compact"
  accept={['image/*']}
  disabled={isSubmitting}
  label="Attach an image"
  onFilesAccepted={(files) => setAttachment(files[0])}
/>
```

---

## 10. Do / Don't

| Do | Don't |
|----|-------|
| Show accepted file types and size limits in the `hint` prop | Hide constraints until the user triggers a rejection error |
| Keep `onFilesAccepted` responsible for upload logic; keep this component as presentation | Put XHR/fetch calls inside the component |
| Use `uploadState` to drive progress — derive it from your upload service | Rely on internal component state for upload status |
| Show a per-file error message with a specific reason ("File type not supported: `.exe`") | Show a generic "Upload failed" without context |
| Allow the user to remove any file at any stage (pending, uploading, success, error) | Lock the file list during upload |
| Announce progress and completion to screen readers via `aria-live` | Skip live region updates for assistive technology users |
| Use `layout="compact"` in space-constrained inline contexts | Force the full zone layout into a narrow sidebar or table cell |
| Test drag-and-drop with keyboard-only (use `Tab` + `Enter` to open picker) | Assume drag-and-drop is the only path for all users |
| Validate file type by MIME type, not file extension | Use extension-only validation — it is easily spoofed |

---

*Related: `/ui-designer:design-review` to audit an implementation against this spec. `/ui-designer:accessibility-audit` for WCAG compliance after implementation.*

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/17.0 (94%) |
| Evaluated | 2026-05-01 |
| Target duration | 132692 ms |
| Target cost | $0.1763 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires all 8 interaction states: Default, Hover, Focus, Active, Disabled, Loading, Error, Empty | PASS | Section 4 'States — Complete Coverage Table' explicitly lists all 8 states as named rows: Default, Hover, Focus, Active, Disabled, 'Loading / Uploading', 'Error (zone-level)', and Empty — each with visual treatment, behaviour, and transitions. |
| c2 | Skill requires ARIA roles, labels, and keyboard navigation as mandatory — not optional or deferred | PASS | Section 6 'Accessibility Requirements' is a full mandatory section with a Keyboard Navigation table, Screen Reader sub-section specifying role, aria-label, aria-describedby, aria-live, role='progressbar', and aria-valuenow — none marked optional or deferred. |
| c3 | Skill requires a design system decision (Reuse / Extend / Create) with justification before specifying the component | PASS | Section 0 'Design System Decision' opens the spec with 'Decision: Create — searched for existing upload components, file input primitives, dropzone utilities, and progress indicators. The codebase contains no existing UI components.' This precedes all other sections. |
| c4 | Skill requires responsive behaviour specification — the component must be described at multiple breakpoints | PASS | Section 5 'Responsive Behaviour' has a breakpoint table covering Mobile (< 640px), Tablet (640–1024px), and Desktop (> 1024px), each with layout changes and content changes columns. |
| c5 | Skill requires a properties/variants table documenting all configurable aspects of the component | PASS | Section 2 'Props / API' provides a full table with Prop, Type, Default, Required, and Description columns covering 11 props. Section 3 'Variants' documents the layout prop with a table of layout modes. |
| c6 | Skill requires animation and transition specifications where state changes occur (e.g. drag-over highlight, upload progress) | PASS | Section 8 'Animation and Motion' has a table with 7 named interactions (drag-over enter/leave, hover, file appear/remove, progress bar fill, success icon), each specifying duration and easing. Includes prefers-reduced-motion CSS and JS handling. |
| c7 | Skill requires token references for colours, spacing, and typography — partial credit if tokens are mentioned but not required to be referenced by name | PARTIAL | Section 7 'Dark Mode' mentions '--color-border-default' by name once and states 'All values use semantic design tokens, not hardcoded hex', but uses Tailwind utility classes (bg-neutral-900, border-neutral-600) rather than formal token names (spacing-md, radius-lg) consistently throughout the spec. |
| c8 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The captured output is entirely a chat response (the spec document). No YAML frontmatter block with name, description, or argument-hint fields appears anywhere in the captured output. |
| c9 | Output's design-system decision (Reuse / Extend / Create) is made up front with reasoning — likely Create because file-upload with drag-and-drop has no existing primitive, or Extend if there's a base Input/Box to build from | PASS | Section 0 states 'Decision: Create' up front with reasoning: 'The codebase contains no existing UI components.' Also noted in the opening line: 'No existing upload components found. Decision: Create — no existing component covers drag-and-drop file upload with progress indication.' |
| c10 | Output documents all 8 interaction states for the file upload — Default (drop zone visible), Hover (hover over the zone), Focus (keyboard focus on the click-to-browse), Active (currently dragging file over), Disabled (uploads not currently allowed), Loading (upload in progress with progress bar), Error (invalid file type / size), Empty (no files added yet) | PASS | Section 4 Drop Zone table rows explicitly named: Default, Hover, Focus, Active, 'Drag-over' (active drag state), Disabled, 'Loading / Uploading', 'Error (zone-level)', and Empty — all with visual treatment, behaviour, and transition descriptions. |
| c11 | Output's ARIA / keyboard spec covers — `role="region"` with `aria-label="File upload"`, the drop zone is keyboard-activatable (Enter/Space triggers file picker), live region announces "Uploading X.pdf..." and completion / error | PASS | Section 6 Screen Reader: role='button' with aria-label from label prop (note: uses role='button' not role='region', but aria-label is present); Keyboard Navigation: 'Enter / Space \| Opens the native file picker'; aria-live='polite' announces status changes including 'Upload complete: {fileName}' and '{fileName} failed: {errorMessage}'. |
| c12 | Output addresses drag-and-drop AND click-to-browse — drag accepts files dropped over the zone, click-to-browse opens the OS file picker; both lead to the same upload flow | PASS | Drag-and-drop covered in Section 4 Drag-over states. Click-to-browse covered in Section 6 Keyboard ('Enter / Space \| Opens the native file picker') and Section 5 Responsive ('click-to-browse is emphasised with a larger tap target' on mobile). Do/Don't: 'Do not hide the click to browse affordance at any breakpoint.' |
| c13 | Output specifies invalid-file-type error handling — visible error message stating which file types ARE accepted (e.g. "Only .pdf and .docx files are supported. The file you tried to upload is .xlsx"), file rejection without form interruption | PASS | Section 4 'Drag-over (invalid)': 'border → error-400, bg → error-50, icon red'; Per-File Entry Error state: 'error message below file name (e.g. "Invalid file type: .exe")'; FileRejection interface includes 'file-type' error; Do/Don't: 'Show per-file error message with specific reason ("File type not supported: .exe")' |
| c14 | Output specifies file-size error handling — max size threshold visible in the empty state, error if exceeded with the specific file size shown | PASS | Section 2: maxSize prop ('Maximum file size in bytes per file'). FileRejection errors include 'file-size'. Section 9 examples: 'hint="PNG or JPG up to 5 MB"'. Do/Don't: 'Show accepted file types and size limits in the hint prop'. FileRejection error codes cover file-size rejection. |
| c15 | Output's progress indicator is animated with explicit transition — appears on upload start, updates with progress %, transitions to success or error state | PASS | Section 8: 'Progress bar fill \| Width transition \| continuous, no easing override \| linear'. Section 4 Per-File: Pending → Uploading ('Progress bar fills left-to-right, percentage label') → Success ('Green check icon replaces progress bar, scale from 0.5→1, 150ms ease-out') or Error state. |
| c16 | Output's responsive behaviour describes the component at desktop (full-width drop zone) AND mobile (smaller drop zone, single-column, tap-to-browse takes priority over drag since drag is awkward on touch) | PASS | Section 5: Mobile '< 640px — Drop zone is full-width; Drag-and-drop is not the primary interaction (touch); click-to-browse is emphasised with a larger tap target'; Desktop '> 1024px — max-width constrained to form column (default max-w-2xl)'. Also: 'Drag-and-drop is supported on modern iOS/Android but unreliable on older devices. Click-to-browse is always the primary interaction path.' |
| c17 | Output's properties / variants table documents configurable aspects — accepted file types, max size, multiple-files vs single-file, optional vs required, custom error messages | PASS | Section 2 Props table covers: accept (MIME types), maxSize (bytes), maxFiles (1 default, drives multiple), multiple (boolean), onFilesRejected (custom error callback), each with Required column. Section 3 Variants covers layout='zone'/'compact'. |
| c18 | Output references design tokens by name — `color-border-default`, `spacing-md`, `radius-lg` — for every visual property, not just hex codes | PARTIAL | Section 7 references '--color-border-default' by name and states 'All values use semantic design tokens, not hardcoded hex'. However, the spec predominantly uses Tailwind utility class names (border-neutral-300, bg-primary-50, outline-primary-500) rather than formal design token names like spacing-md or radius-lg across visual property specifications. |

### Notes

The captured output is an exceptionally thorough component specification covering all 8 interaction states, comprehensive ARIA/keyboard accessibility, responsive breakpoints, animation specs, and controlled-state API design. The main deductions are: c8 fails because no YAML frontmatter is visible in the chat response output (the skill definition file itself was not captured); c7 and c18 score at PARTIAL ceiling because token references default to Tailwind utility classes rather than formal design token names throughout. One notable discrepancy in c11: the spec uses role='button' instead of role='region' for the drop zone, which is arguably semantically correct but diverges from the criterion's explicit mention of role='region'. The spec scores PASS overall at 94.1% due to its thoroughness across all structural requirements.
