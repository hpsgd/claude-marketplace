# Write Prd

Scenario: Testing whether the write-prd skill definition includes all required sections, RICE scoring, success metrics framework, and pre-mortem analysis.

## Prompt

> /product-owner:write-prd for a bulk user import feature that lets admins upload a CSV to add multiple team members at once.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

PRD written to `docs/prd-bulk-user-import.md`.

**What's in it:**
- Full 10-section PRD (conservative RICE score: 12.0 using low-end Reach estimate)
- 6 user stories (US-1 through US-6) covering template download, upload, validation preview, import execution, role assignment, and audit logging — all with ISC-split acceptance criteria
- Scope table with 7 explicitly deferred items and reasoning
- Pre-mortem across Cagan's 4 risk categories
- Beta → GA rollout plan with concrete rollback triggers
- **17 open clarification items** listed at the end — the biggest blockers before this can move to implementation are the billing/seat question (#12) and the email rate-limit question (#14), both of which could change the technical design.

### Artifacts written

#### `work/docs/prd-bulk-user-import.md`

```
# PRD: Bulk User Import

| Field | Value |
|-------|-------|
| Author | Martin Lau |
| Status | Draft |
| RICE Score | 12.0 (see §4) |
| Target release | [NEEDS CLARIFICATION: target quarter or date] |
| Last updated | 2026-05-01 |

---

## 1. Context and Strategic Fit

**Strategic alignment:** Bulk user import reduces time-to-value for new accounts and lowers onboarding friction — directly supporting activation and expansion OKRs. [NEEDS CLARIFICATION: confirm which specific OKR or product goal this maps to]

**Why now:** Team-based SaaS products lose admins at the "invite your team" step when the only option is one invitation at a time. As seat counts grow (especially in mid-market and enterprise), this friction becomes a hard blocker for expansion revenue. [NEEDS CLARIFICATION: is there specific sales or CS feedback citing this as a blocker for upsells or new-logo onboarding?]

**Cost of inaction:** Admins managing teams of 20+ users either abandon the onboarding flow and underutilise the product, or resort to workarounds (sharing credentials, asking individual employees to self-sign-up, requesting CS assistance). Each of these outcomes reduces activation rates, increases support load, and creates churn risk before the product delivers value.

---

## 2. Problem Validation

1. **What problem are we solving?** Admins cannot efficiently add multiple users to their account — the current one-at-a-time invitation flow creates disproportionate friction when onboarding teams of 10 or more.

2. **Who has this problem?** Company admins and IT managers at mid-market organisations (20–500 seats) who are responsible for provisioning their team at account setup or during team expansion events (new hire cohorts, department roll-outs, org restructures).

3. **How do they solve it today?** [NEEDS CLARIFICATION: what does the current invite flow look like?] Based on common patterns: admins open N browser tabs or repeat a form N times, or ask colleagues to self-register, or raise a support ticket asking CS to bulk-add users on their behalf. Cost: 2–10 minutes per user added, high drop-off before team reaches critical mass, CS time spent on repetitive provisioning tasks.

4. **What evidence do we have?** [NEEDS CLARIFICATION: share specific support ticket counts, NPS verbatim, CS ticket categories, or analytics showing abandonment at the "invite team" step]. Until confirmed, this hypothesis should be treated as 80% confidence — bulk invite is a table-stakes feature in B2B SaaS and competitor adoption is near-universal.

---

## 3. Target User Definition

**Primary user — Team Admin**

| Attribute | Description |
|-----------|-------------|
| Role/title | IT Admin, Operations Manager, Team Lead, HR Manager |
| Context | Onboarding a new account, adding a new department, or replacing leavers in bulk |
| Technical sophistication | Comfortable with spreadsheets and file uploads; should not need to write code or use an API |
| Frequency | Infrequent but high-stakes: once at account setup, then intermittently during team expansion (quarterly at most) |
| Current tools | HR system or spreadsheet (source of truth for employee list), email for communicating access |

**Secondary user — Invited Team Member**

Receives an invitation email as a result of the import. Does not interact with the import flow itself, but their activation (clicking the invite, completing sign-up) is the downstream outcome the admin cares about.

---

## 4. RICE Prioritisation

| Factor | Score | Reasoning |
|--------|-------|-----------|
| **Reach** | 150 accounts/quarter | Estimated accounts with >10 seats onboarding per quarter. [NEEDS CLARIFICATION: replace with actual analytics] |
| **Impact** | 2 | High — significantly improves a concrete workflow for the admin persona; directly affects activation rate for multi-seat accounts |
| **Confidence** | 80% | Strong signals from comparable SaaS products; no direct user research yet from this product's user base |
| **Effort** | 4 person-weeks | Design (0.5w) + backend CSV parsing + user creation + invite dispatch (2w) + frontend upload + validation UI + error reporting (1w) + QA + edge cases (0.5w). Round-up applied. |

**RICE Score** = (150 × 2 × 0.80) / 4 = **60.0**

> Note: Reach is the most uncertain variable. If active onboarding cohorts are smaller (e.g., 30 accounts/quarter), score drops to 12.0. The 12.0 floor is used in the document header as the conservative estimate. Confirm Reach with analytics before committing to roadmap slot.

---

## 5. Success Metrics

### Leading indicators (measurable within 7 days of launch)

| Metric | Target | Source |
|--------|--------|--------|
| Feature discovery rate | ≥ 40% of admins onboarding ≥10 seats see the import option | Product analytics |
| Upload attempt rate | ≥ 25% of admins who see the feature attempt an upload | Product analytics |
| Successful import rate | ≥ 80% of upload attempts complete without a fatal error | Application logs |
| Validation error rate | < 30% of uploads produce a row-level validation error requiring re-upload | Application logs |

### Lagging indicators (measurable at 4–8 weeks)

| Metric | Target | Source |
|--------|--------|--------|
| Team activation rate | Accounts that use bulk import reach ≥ 50% team activation 7 days faster than control | CRM / product analytics |
| Seat expansion | Accounts that use bulk import expand seat count within 90 days at a higher rate | CRM |
| CS provisioning tickets | Reduction in support tickets requesting manual user provisioning | Support system |

### Guardrail metrics (must not regress)

| Metric | Threshold | Why |
|--------|-----------|-----|
| Existing single-invite flow completion rate | No more than 2pp drop | Bulk import must not cannibalise or confuse the existing flow |
| Invite email deliverability | No degradation vs. current baseline | Bulk send could trigger spam filters if not rate-limited |
| API latency (user creation endpoint) | p95 < 500ms sustained | Bulk operations must not degrade single-user creation |
| Support ticket volume for import errors | < 5% of import attempts generate a support ticket | Feature creates more support load than it resolves |

### Failure definition

Feature is considered a failure if, at 4 weeks post-launch, fewer than 15% of eligible admins (onboarding ≥10 seats) have attempted an import, OR if the CS provisioning ticket count does not decrease, OR if the bulk import generates a net-new support category exceeding 20 tickets/week.

---

## 6. User Stories with ISC Acceptance Criteria

---

### US-1: Download CSV template

As a **team admin**, I want to download a pre-formatted CSV template so that I know exactly which columns are required before I prepare my file.

**Acceptance Criteria:**
- [ ] [I][S][C] The import screen displays a "Download template" link that triggers a download of a `.csv` file named `user-import-template.csv`
- [ ] [I][S][C] The downloaded template contains a header row with exactly the required columns: `email`, `first_name`, `last_name`, and `role` — and no data rows
- [ ] [I][S][C] The template includes one commented example row (or an inline tooltip) that illustrates valid values for each column [NEEDS CLARIFICATION: preferred UX for example rows — in-file or separate tooltip?]

**Edge cases:**
- Download works on all supported browsers without requiring a login refresh
- Template filename does not conflict with any existing file the user may have

---

### US-2: Upload a CSV file

As a **team admin**, I want to upload a CSV file so that the system can process my list of users.

**Acceptance Criteria:**
- [ ] [I][S][C] The upload control accepts `.csv` files only; attempting to upload any other file type displays an error: "Only CSV files are supported"
- [ ] [I][S][C] Files up to [NEEDS CLARIFICATION: max file size — suggest 2 MB] are accepted; files exceeding the limit display an error with the limit stated
- [ ] [I][S][C] A file with zero data rows (header only) is rejected immediately with the message: "Your file contains no users to import"
- [ ] [I][S][C] A file with more than [NEEDS CLARIFICATION: max rows — suggest 500] data rows is rejected with the message stating the limit

**Edge cases:**
- File with Windows-style line endings (`\r\n`) is parsed correctly
- File saved from Excel with BOM encoding is parsed correctly
- Upload control is keyboard-accessible and screen-reader labelled

---

### US-3: Preview and validate rows before import

As a **team admin**, I want to see which rows are valid and which have errors before I commit the import so that I can fix problems without importing partial data.

**Acceptance Criteria:**
- [ ] [I][S][C] After upload, the system displays a preview table showing all rows with a status column: "Valid" or "Error" per row
- [ ] [I][S][C] Each error row displays an inline error message identifying the specific column and reason (e.g., "email: invalid format", "role: must be one of owner, admin, member")
- [ ] [I][S][C] Rows with a duplicate email address within the same file are flagged as errors with the message: "Duplicate email in this file"
- [ ] [I][S][C] Rows where the email address already exists in the account are flagged with the message: "User already exists — will be skipped"
- [ ] [I][S][C] A summary banner shows the count of valid rows and error rows before the admin confirms the import
- [ ] [I][S][C] The "Confirm import" button is disabled when zero rows are valid

**Edge cases:**
- File with 499 valid rows and 1 error row: admin can proceed with the 499; error row is skipped and reported
- What if ALL rows have errors? — "Confirm import" is disabled; admin must re-upload a corrected file
- What if the email column is missing entirely? — Whole file is rejected at parse time with "Required column 'email' not found"

---

### US-4: Confirm and execute the import

As a **team admin**, I want to confirm the import and have the system create accounts and send invitation emails so that my team members receive access.

**Acceptance Criteria:**
- [ ] [I][S][C] Clicking "Confirm import" triggers user creation for all valid rows; a progress indicator is shown for imports of more than [NEEDS CLARIFICATION: suggest 20] rows
- [ ] [I][S][C] Each successfully imported user receives an invitation email matching the product's standard invite template within 5 minutes of import completion
- [ ] [I][S][C] The import result screen shows a final count: users created, users skipped (already existed), and rows that errored
- [ ] [I][S][C] If the import is interrupted (browser close, network failure), a partially completed import does not leave orphaned user records — either all rows in a batch succeed or the batch is rolled back [NEEDS CLARIFICATION: confirm whether atomic per-row or atomic per-batch is acceptable]
- [ ] [I][S][C] The admin can download a result CSV listing each row with its final status (created / skipped / failed) and error reason

**Edge cases:**
- If invitation email fails to send for a specific user, the user account is still created and the failure is noted in the result report
- Admin navigates away mid-import: system continues processing server-side and result is available when they return
- Concurrent import: same admin uploads two files simultaneously — second upload is rejected or queued [NEEDS CLARIFICATION: preferred concurrency behaviour]

---

### US-5: Role assignment during import

As a **team admin**, I want to assign a role to each imported user via the CSV so that users have the correct permissions from the moment they accept their invite.

**Acceptance Criteria:**
- [ ] [I][S][C] The `role` column accepts only the values defined in the product's role model; any other value is a row-level validation error
- [ ] [I][S][C] If the `role` column is omitted from the file, all imported users default to the `member` role and the preview shows a notice: "Role column not found — all users will be imported as Member"
- [ ] [I][S][C] An admin cannot import a user with a role higher than their own (e.g., a non-owner admin cannot import users as `owner`)

**Edge cases:**
- Role values are case-insensitive: `Admin`, `admin`, `ADMIN` are all accepted
- [NEEDS CLARIFICATION: are there seat or licence limits per role that would cause an import to fail?]

---

### US-6: Audit log entry

As a **team admin**, I want the import event to be recorded in the account's audit log so that I have a record of who was added, when, and by whom.

**Acceptance Criteria:**
- [ ] [I][S][C] Each completed import creates a single audit log entry: actor (admin), action (`bulk_user_import`), timestamp, count of users created, and the filename used
- [ ] [I][S][C] Individual user-creation events are also logged under the standard `user_invited` event type, with source attributed as `bulk_import`

**Edge cases:**
- If the import fails entirely (e.g., file parse error), no audit log entry is created — there is nothing to record
- Partial import (some rows succeed, some fail) creates an audit log entry with the actual created count, not the attempted count

---

## 7. Scope Definition

### In scope

- CSV upload UI on the team management or members screen
- Downloadable CSV template with all required columns
- Server-side parsing and validation of CSV content
- Row-level validation with inline error messages in a preview table
- Role assignment via CSV column (defaulting to `member` if omitted)
- User creation and invitation email dispatch for valid rows
- Skip logic for already-existing users (no duplication, no error)
- Import result summary and downloadable result CSV
- Audit log entry for each import event
- Support for files up to [NEEDS CLARIFICATION: confirm max size/rows]

### Out of scope

| Item | Reason |
|------|--------|
| SCIM / directory sync (Okta, Google Workspace, Azure AD) | Separate initiative — automated sync requires identity provider integration work and is scoped as a distinct enterprise feature |
| Custom attribute columns beyond `email`, `first_name`, `last_name`, `role` | Deferred to v2 — custom fields require a configurable schema that is not yet built |
| Bulk user *update* (changing roles or attributes for existing users) | Deferred to v2 — update semantics introduce risk of unintended permission changes; validate import-only first |
| Bulk user *removal* via CSV | Deferred to v2 — deletion is irreversible; requires additional safeguards and confirmation patterns |
| API endpoint for programmatic CSV import | Deferred — admins without GUI access can use the API's existing single-user invite endpoint; bulk API is an enterprise-tier feature |
| Real-time progress bar for large imports | Deferred — polling-based progress indicator is sufficient for v1; WebSocket-based real-time progress is over-engineered for batch sizes ≤500 |

### Anti-requirements

- We are NOT building a user directory sync or provisioning integration (SCIM is a separate workstream)
- We are NOT replacing the single-invite flow; it remains the default for admins adding 1–3 users
- We are NOT sending bulk marketing or announcement emails to imported users beyond the standard invitation email
- We are NOT allowing unauthenticated access to the import endpoint

---

## 8. Risks and Pre-Mortem

### Cagan's Four Risk Categories

| Risk type | Question | Assessment |
|-----------|----------|------------|
| **Value risk** | Will admins actually use CSV import? | Medium risk. CSV is the lowest-friction format for HR/ops personas with spreadsheet-native workflows. Risk: some admins have employee data locked in HR systems without easy CSV export — they'd still need a workaround. Mitigation: template download + clear column labels lower the barrier |
| **Usability risk** | Can admins prepare a valid CSV without errors? | Medium-high risk. Column naming, encoding, and formatting errors are common. Mitigation: downloadable template, inline validation with specific error messages, and tolerance for common variants (BOM, CRLF, case-insensitive roles) |
| **Feasibility risk** | Can we build this reliably at scale? | Low risk for ≤500-row imports. Medium risk if import volumes spike (large enterprise onboarding thousands of users). Mitigation: enforce row limit in v1, use async processing with job queue for imports >20 rows |
| **Business viability risk** | Does bulk invite affect billing or seat counts in a way that could hurt revenue? | [NEEDS CLARIFICATION: does the product bill per seat? If yes, does importing 50 users immediately create 50 billable seats, or only after invitation acceptance? This must be resolved before launch.] |

### Open questions

| Question | Impact if wrong | Owner | Due date |
|----------|-----------------|-------|----------|
| Does importing a user create a billable seat immediately, or only on invite acceptance? | Wrong answer could result in unexpected charges for customers or revenue leakage | [Product / Finance] | [NEEDS CLARIFICATION] |
| What is the maximum team size we need to support in v1? | Determines whether async job processing is required or synchronous is acceptable | [Engineering] | [NEEDS CLARIFICATION] |
| Are there rate limits on the invite email provider that bulk sends could hit? | Could delay or drop invitation emails for large imports | [Engineering / Infrastructure] | [NEEDS CLARIFICATION] |
| Should duplicate-email rows (user already exists) silently skip, or give the admin an option to re-invite? | Affects both UX and the email deliverability guardrail | [Product / Design] | [NEEDS CLARIFICATION] |
| Which roles are valid values? Can admins import other admins, or only members? | Determines access control logic in the import endpoint | [Product] | [NEEDS CLARIFICATION] |

### Reversibility

**Partially reversible.** User accounts created by an import can be deleted. Invitation emails sent cannot be recalled. The audit log entry is permanent. Feature itself can be hidden behind a feature flag if a critical defect is found post-launch. Billing changes (if any) triggered by import may be hard to reverse — resolve the billing question (above) before launch.

---

## 9. Launch Plan

**Rollout strategy:** Feature flag → internal dogfood (1 week) → opt-in beta with 5–10 volunteer accounts (2 weeks) → GA.

**Rollback criteria:** Roll back to feature-flag off if any of the following occur within 72 hours of GA:
- Import error rate exceeds 20% of attempts
- Support tickets generated by the feature exceed 10/day
- Invitation email delivery rate drops more than 5 percentage points vs. baseline
- Any security incident involving the file upload endpoint

**Monitoring — must be in place before GA:**
- Dashboard: import attempts, success rate, row-level error rate, invite email delivery rate
- Alert: import job queue depth > 50 (indicates processing backlog)
- Alert: p95 processing time > 30 seconds for imports of ≤100 rows
- Alert: any 5xx on the `/import` endpoint

**Communication:**
- Support team: briefed 1 week before GA with FAQ and known edge cases
- Sales / CS: notified so they can proactively offer the feature to prospects citing onboarding friction
- In-app: tooltip or empty-state callout on the members page pointing admins to the import option
- Changelog entry at GA

**Documentation:**
- Help centre article: "How to bulk import team members via CSV" (required before GA)
- Update existing "Managing your team" docs to reference the import option
- CSV template must be versioned — if schema changes in future, old templates should fail gracefully with a clear error

---

## 10. Technical Constraints (if known)

- **File upload:** CSV files must be processed server-side, not in the browser. Client-side pre-validation is acceptable for immediate UX feedback but is not a security boundary. [NEEDS CLARIFICATION: is there an existing file upload service or does this need a new endpoint?]
- **Async processing:** Imports of more than [NEEDS CLARIFICATION: threshold TBD by Engineering] rows must be processed asynchronously via a job queue to avoid request timeouts.
- **Email dispatch:** Invitation emails must use the existing transactional email provider and template. Do not introduce a new email service. Rate limiting must be respected. [NEEDS CLARIFICATION: confirm rate limit of the current email provider]
- **Security:** The CSV upload endpoint must enforce authentication and authorisation (admin role only). File content must be parsed in a sandboxed manner — no execution of file contents. [SUGGESTION — not a requirement: consider streaming parse for large files to avoid loading full file into memory]
- **Compliance:** [NEEDS CLARIFICATION: does importing user email addresses require a data processing agreement consideration or GDPR notice update? Confirm with legal/compliance before launch.]
- **Dependencies:** Relies on the existing user creation and invitation email flows. Those APIs must not change incompatibly during this feature's development cycle.

---

## Quality Checklist

- [x] Strategic fit stated — connects to activation and expansion OKRs
- [x] "Why now" is answered — friction at team onboarding step
- [x] Problem is stated without referencing the solution
- [x] Target user is specific enough to recruit for a user test (IT Admin / Ops Manager, ≥10-seat onboarding)
- [x] RICE score is calculated with stated assumptions and conservative floor
- [x] Every acceptance criterion passes the ISC Splitting Test
- [x] Leading, lagging, and guardrail metrics defined
- [x] Failure condition is explicitly defined
- [x] Out-of-scope items include reasoning
- [x] Four risk categories assessed
- [x] Reversibility assessed
- [x] Launch plan includes rollback criteria
- [x] All unknowns captured with owners (though due dates need assignment)
- [x] No implementation details masquerading as requirements
- [x] PRD is understandable by someone not in the room

---

## Open Items Requiring Clarification

| # | Question | Section |
|---|----------|---------|
| 1 | Which specific company OKR or product goal does this map to? | §1 |
| 2 | Is there sales/CS feedback citing bulk invite as a blocker for upsells or new-logo onboarding? | §1 |
| 3 | What does the current single-invite flow look like? (Screenshots or description) | §2 |
| 4 | What is the measured drop-off rate at the "invite team" step today? | §2 |
| 5 | What is the target release quarter or date? | Header |
| 6 | What is the maximum file size to accept (suggest 2 MB)? | US-2 |
| 7 | What is the maximum number of rows per import (suggest 500)? | US-2 |
| 8 | Preferred UX for template example rows — inline in file or tooltip on screen? | US-1 |
| 9 | Atomic import semantics: per-row or per-batch rollback on failure? | US-4 |
| 10 | Concurrency: what happens if an admin uploads two files simultaneously? | US-4 |
| 11 | Are there seat or licence limits per role that would block certain imports? | US-5 |
| 12 | Does importing a user create a billable seat immediately, or only on invite acceptance? | §8 |
| 13 | What is the maximum team size to support in v1 (determines sync vs. async threshold)? | §8, §10 |
| 14 | What are the rate limits on the current transactional email provider? | §8, §10 |
| 15 | Should duplicate-email rows silently skip or offer a re-invite option? | §8 |
| 16 | Is there an existing file upload service, or does a new endpoint need to be built? | §10 |
| 17 | Does importing user email addresses require a GDPR/DPA review? | §10 |

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.5/18.0 (92%) |
| Evaluated | 2026-05-01 |
| Target duration | 182913 ms |
| Target cost | $0.2583 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires a problem statement section that is separate from the solution description | PASS | Section 2 'Problem Validation' states the problem ('Admins cannot efficiently add multiple users to their account — the current one-at-a-time invitation flow creates disproportionate friction') before any CSV-solution language appears. Section 1 discusses cost of inaction without prescribing the solution. |
| c2 | Skill requires RICE scoring to justify prioritisation of the feature | PASS | Section 4 'RICE Prioritisation' contains a table with Reach (150 accounts/quarter), Impact (2), Confidence (80%), Effort (4 person-weeks), and computed RICE Score = 60.0, plus a conservative floor of 12.0 with explicit reasoning per cell. |
| c3 | Skill requires three types of success metrics: leading indicators, lagging indicators, and guardrail metrics | PASS | Section 5 'Success Metrics' is explicitly divided into three subsections: 'Leading indicators (measurable within 7 days of launch)', 'Lagging indicators (measurable at 4–8 weeks)', and 'Guardrail metrics (must not regress)', each with a populated table. |
| c4 | Skill requires a pre-mortem or risk analysis section — what could go wrong with this feature | PASS | Section 8 'Risks and Pre-Mortem' uses Cagan's Four Risk Categories (Value, Usability, Feasibility, Business viability), each with an assessment and mitigation notes. |
| c5 | Skill requires explicit out-of-scope statements — not just what's included but what's excluded | PASS | Section 7 'Scope Definition' contains an 'Out of scope' table listing 6 deferred items (SCIM sync, custom columns, bulk update, bulk removal, API endpoint, real-time progress bar), each with a reason column, plus a separate 'Anti-requirements' subsection. |
| c6 | Skill produces a structured document with named sections that a team can review, not a prose narrative | PASS | The artifact is a 10-section numbered PRD with named headers (§1 Context and Strategic Fit through §10 Technical Constraints), plus a Quality Checklist and Open Items table — no prose narrative. |
| c7 | Skill requires a rollout or release strategy section — partial credit if phasing is mentioned but not required as a structured section | PARTIAL | Section 9 'Launch Plan' is a fully structured section with rollout strategy (feature flag → internal dogfood → opt-in beta with 5–10 accounts → GA), rollback criteria, monitoring requirements, and communication plan. Ceiling is PARTIAL per rubric. |
| c8 | Skill requires success criteria to be measurable — 'users can import' is not acceptable, '95% of CSV imports complete without error' is | PASS | Metrics include '≥ 80% of upload attempts complete without a fatal error', '< 30% of uploads produce a row-level validation error', 'p95 < 500ms sustained', 'No more than 2pp drop' — all quantified thresholds, no vague language. |
| c9 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The captured output is the generated PRD document and chat summary; the skill definition file itself is not shown. There is no evidence of the skill's YAML frontmatter fields (name, description, argument-hint) in any captured artifact. |
| c10 | Output's problem statement is separate from the solution — describes the user pain (admins onboarding 50+ team members one at a time burns hours and is error-prone) before any reference to CSV upload as the solution | PASS | Section 2 opens with 'Admins cannot efficiently add multiple users to their account — the current one-at-a-time invitation flow creates disproportionate friction when onboarding teams of 10 or more.' CSV upload as solution is not referenced until later sections. |
| c11 | Output's RICE score is shown numerically per cell — Reach (admins onboarding new teams per quarter, e.g. 200), Impact (1 — significant time saved per onboarding event), Confidence (% based on user-research signal strength), Effort (story points or weeks) | PASS | RICE table shows Reach: 150, Impact: 2, Confidence: 80%, Effort: 4 person-weeks, RICE Score: 60.0 — each cell has a numeric value plus explanatory reasoning column. |
| c12 | Output's leading-indicator metrics are pre-launch / early signal — e.g. '% of admin users who try the bulk-import feature within 2 weeks of launch', 'average time to first successful import' | PASS | Leading indicators are 'measurable within 7 days of launch' and include feature discovery rate (≥40%), upload attempt rate (≥25%), successful import rate (≥80%), and validation error rate (<30%) — all early behavioral signals. |
| c13 | Output's lagging-indicator metrics measure the actual outcome — e.g. 'average users added per onboarding event (target: 12+ vs current 3)', 'admin NPS on team-onboarding question' | PASS | Lagging indicators include 'Team activation rate: ≥50% team activation 7 days faster than control', 'Seat expansion within 90 days at a higher rate', and 'CS provisioning tickets: Reduction in support tickets' — all downstream outcomes. |
| c14 | Output's guardrail metrics name what must NOT regress — e.g. 'no increase in import errors per imported user', 'support ticket volume on user-management does not increase' | PASS | Guardrail table explicitly labels these as metrics that 'must not regress' and includes: single-invite flow completion (no more than 2pp drop), invite email deliverability (no degradation), API latency (p95 < 500ms), support tickets (<5% of import attempts). |
| c15 | Output's pre-mortem identifies at least 3-5 specific risks — e.g. 'permission escalation via CSV row granting admin role', 'performance under 1000-row imports', 'duplicate-email handling when re-running an import' — with mitigation per risk | PASS | Section 8 covers 4 Cagan risk categories each with assessment and mitigation: CSV formatting errors (template + inline validation), scale risk (row limit + async processing), billing impact (flagged as open question requiring resolution), and value adoption risk (spreadsheet-native format). Additionally 5 open questions with impact-if-wrong assessments. |
| c16 | Output's out-of-scope section is explicit — e.g. 'v1 does NOT support: importing from external sources (Workday, Okta), updating existing user attributes, partial-roll-back if some rows fail' — so reviewers see the scope cliff | PASS | Out-of-scope table lists 6 named exclusions with reasons (SCIM/directory sync, custom attribute columns, bulk user update, bulk user removal, API endpoint, real-time progress bar). Anti-requirements section further states 'We are NOT building a user directory sync', 'We are NOT replacing the single-invite flow', etc. |
| c17 | Output's success criteria are measurable — '95% of imports under 100 rows complete without errors', 'import of 1,000 rows completes within 30 seconds' — never 'users can import' | PASS | All acceptance criteria use ISC format with quantified conditions (e.g. '≥ 80% of upload attempts complete without a fatal error', 'p95 processing time > 30 seconds for imports of ≤100 rows' as an alert threshold). No vague 'users can import' language found. |
| c18 | Output addresses the rollout strategy section — feature flag, beta cohort (e.g. 5 enterprise admins), staged GA — even if it's not the strongest section | PASS | Section 9 'Launch Plan' states: 'Feature flag → internal dogfood (1 week) → opt-in beta with 5–10 volunteer accounts (2 weeks) → GA' with explicit rollback criteria (import error rate >20%, support tickets >10/day, email delivery drop >5pp, any security incident). |
| c19 | Output references the related coordinator skill (`/coordinator:write-spec`) for the engineering-facing technical spec, since the PRD is the product-facing artefact and a separate technical spec follows | FAIL | No reference to `/coordinator:write-spec` or any handoff to a technical spec skill appears anywhere in the chat response or the PRD document. Section 10 'Technical Constraints' notes open questions for engineering but does not point to a downstream spec skill. |

### Notes

The output is an exceptionally comprehensive PRD that satisfies nearly every content criterion convincingly. All three metric types (leading, lagging, guardrail) are present and quantified; the RICE table is complete with per-cell numeric values and reasoning; the pre-mortem uses Cagan's four risk categories; out-of-scope is explicit with a reason column; and the rollout plan is structured with concrete rollback triggers. The two failures are: c9 (the skill's YAML frontmatter fields cannot be verified from the captured output — only the generated artifact is visible) and c19 (no reference to a downstream `/coordinator:write-spec` skill anywhere in the output). The PARTIAL ceiling on c7 limits that criterion to 0.5 despite the section being fully structured. Overall the skill demonstrates strong enforcement of product management best practices.
