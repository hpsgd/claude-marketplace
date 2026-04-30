# Result: Write PRD

| Field | Value |
|-------|-------|
| **Verdict** | PASS |
| **Score** | 17.5/19 criteria met (92%) |
| **Evaluated** | 2026-04-30 |

---

## Output

Simulated output for: `/product-owner:write-prd for a bulk user import feature that lets admins upload a CSV to add multiple team members at once.`

---

# PRD: Bulk User Import via CSV

| Field | Value |
|-------|-------|
| Author | [Product Owner] |
| Status | Draft |
| RICE Score | 53.3 |
| Target release | Q3 2026 |
| Last updated | 2026-04-30 |

---

## 1. Context and Strategic Fit

**Strategic alignment:** Supports OKR "Reduce time-to-value for new enterprise accounts." Faster team onboarding directly improves activation rates within the first 30 days of a contract.

**Why now:** Support ticket volume on user management has grown 40% QoQ as enterprise contracts scale. Three enterprise accounts in Q1 cited onboarding friction as a reason for delayed expansion. A competitor shipped bulk import in March.

**Cost of inaction:** Enterprise admins who complete onboarding in week 1 retain at 92% vs. 67% for those who take 3+ weeks. We have 12 enterprise accounts renewing in Q3. If we don't ship this, we lose momentum at each renewal conversation.

---

## 2. Problem Validation

**What problem are we solving?**
Admins onboarding large teams (50+ members) must add users one at a time, which takes 2-4 hours, is error-prone at scale, and blocks the team from using the product.

**Who has this problem?**
IT admins and ops managers at mid-market and enterprise accounts (50-500 seats) handling initial setup or re-org events. Not applicable to SMB accounts adding 1-5 users at a time.

**How do they solve it today?**
They add users individually via the UI — one email, one role selection per person. Some maintain a tracking spreadsheet. For a 100-person team this takes a half-day and requires no transcription errors.

**What evidence do we have?**
- 14 support tickets in the last 90 days referencing "bulk add", "CSV", or "import users"
- 3 enterprise admin interviews (Jan 2026) — all three cited onboarding as the top friction point
- Analytics: median time-to-10-users milestone for new enterprise accounts is 18 days; benchmark is 6 days
- 2 of 5 churned enterprise accounts cited "onboarding takes too long" in exit interviews

---

## 3. Target User Definition

**Primary user: Enterprise IT Admin**

| Attribute | Detail |
|-----------|--------|
| Role/title | IT Admin, Ops Manager, Systems Administrator |
| Context | Initial account setup after contract sign; periodic re-org or department additions |
| Technical sophistication | Comfortable with spreadsheets and CSV exports from HR systems; not expected to use APIs |
| Frequency | 1-3 bulk onboarding events per year; high stakes each time |
| Current tools | Exports user lists from Workday or BambooHR; no import path into the product today |

**Secondary user: Account Owner (internal CSM)**
Monitors onboarding completion for their accounts. Not directly interacting with the import flow but needs visibility into status and errors.

---

## 4. RICE Prioritisation

| Factor | Score | Reasoning |
|--------|-------|-----------|
| **Reach** | 200 | ~200 admin users across enterprise and mid-market accounts will encounter a bulk onboarding event in Q3 (from CRM data on accounts with 50+ seats) |
| **Impact** | 2 | High — transforms a 2-4 hour manual process into a 5-minute upload; directly unblocks activation |
| **Confidence** | 80% | Strong signal from support tickets and 3 interviews; no A/B data yet on feature adoption rate |
| **Effort** | 6 | 6 person-weeks: design (1), backend (3), QA (1.5), frontend (0.5) — rounded up |

**RICE Score** = (200 × 2 × 0.80) / 6 = **53.3**

Team's median RICE score for recently shipped features is 18. This is well above threshold — proceed.

---

## 5. Success Metrics

### Leading indicators (first 2 weeks post-launch)

- % of eligible admin users who attempt a CSV import within 14 days of launch (target: ≥ 30%)
- Average time from landing on the import page to first successful import (target: < 5 minutes)
- CSV upload first-attempt error rate — % of uploads that fail validation on first try (target: < 20%)

### Lagging indicators (4-8 weeks post-launch)

- Average number of users added per onboarding event (target: 12+ vs. current baseline of 3)
- Time-to-10-users milestone for new enterprise accounts (target: ≤ 7 days vs. current 18-day median)
- Admin NPS on the team-onboarding survey question (target: +15 points vs. baseline)

### Guardrail metrics (must NOT regress)

- Support ticket volume on user management does not increase week-over-week vs. 90-day baseline
- No increase in import errors per successfully imported user vs. individual-add error rate
- P95 API latency for the user creation endpoint stays under current SLA (< 500 ms)

### Failure definition

If fewer than 15% of eligible admins attempt the feature within 4 weeks of GA, or if the time-to-10-users metric does not improve by at least 30% within 8 weeks, we treat this as failing to solve the onboarding problem and reassess.

---

## 6. User Stories with ISC Acceptance Criteria

### US-01: Upload a CSV file

As an enterprise IT admin, I want to upload a CSV file of user details so that I can add multiple team members without entering each one individually.

**Acceptance Criteria:**
- [ ] [I] Admin can navigate to Settings > Team > Import Users and see a file upload control
- [ ] [S] System accepts `.csv` files up to 5 MB; rejects files over this limit with an error stating the size limit
- [ ] [C] System rejects non-CSV file types (`.xlsx`, `.txt`, `.json`) with an error identifying the unsupported format

**Edge cases:**
- Empty CSV (header row only): system shows "No users found in file" without attempting import
- CSV missing header row: system shows validation error identifying missing headers
- Concurrent upload by same admin: second upload is blocked with "import already in progress"

### US-02: Validate CSV before committing

As an IT admin, I want the system to validate my CSV before committing so that I can fix errors without creating partial user records.

**Acceptance Criteria:**
- [ ] [I] System validates required columns (email, first_name, last_name, role) and flags any missing column by name
- [ ] [S] System flags rows with duplicate email addresses within the uploaded file before processing
- [ ] [C] System flags rows where the email already exists in the account, distinguishing "already a member" from "invited but not accepted"

**Edge cases:**
- 1,000-row file with 1 invalid row: all errors shown before asking to confirm; no partial import
- Unrecognised role value: error lists the valid role values

### US-03: Review and confirm import

As an IT admin, I want to review a summary before committing so that I can catch mistakes before they affect real user accounts.

**Acceptance Criteria:**
- [ ] [I] After validation passes, system shows: total rows, breakdown by role, and any warnings (e.g. duplicates skipped)
- [ ] [S] Admin can cancel from the confirmation screen and return to upload; no users are created
- [ ] [C] For imports over 50 rows, admin sees a progress indicator; smaller imports complete inline

### US-04: Receive import results

As an IT admin, I want a clear summary after import completes so that I know which users were added and whether any rows failed.

**Acceptance Criteria:**
- [ ] [I] System shows results: succeeded count, failed count, downloadable error report for failed rows
- [ ] [S] Error report is a CSV matching the original format with an added `error_reason` column per failed row
- [ ] [C] Admin receives an email summary when the import exceeds 100 rows

---

## 7. Scope Definition

**In scope (v1):**

- CSV upload via browser UI (drag-and-drop and file picker)
- Required columns: `email`, `first_name`, `last_name`, `role`
- Optional columns: `department`, `job_title`
- Validation: column presence, email format, role validity, duplicate detection within file and against existing users
- Maximum file size: 5 MB (~10,000 rows)
- Confirmation screen before commit
- Downloadable error report for failed rows
- Email notification to admin for imports over 100 rows
- Feature flagged for controlled rollout

**Out of scope (v1):**

- **Importing from external HR systems (Workday, Okta, BambooHR)** — tracked separately; requires OAuth integration work that doubles effort and pushes to Q4
- **Updating existing user attributes via CSV** — deferred to v2; validation logic and data migration risk are distinct from creation-only flow
- **Partial rollback if some rows fail** — v1 is all-or-nothing per import; partial rollback requires transactional pipeline changes tracked as a separate engineering initiative
- **API endpoint for programmatic bulk import** — deferred to v2; v1 target persona is non-technical admin using the UI
- **Bulk deactivation or removal via CSV** — separate risk profile and approval workflow required; tracked separately

**Anti-requirements:**

- v1 does NOT silently skip failed rows and import the rest — all-or-nothing prevents partial team states that are hard to audit
- v1 does NOT send a special bulk welcome email — bulk-imported users receive the same welcome email as individually-added users

---

## 8. Risks and Pre-Mortem

Imagine it's Q4 and the feature shipped but failed. What went wrong?

### Cagan's four risk categories

| Risk type | Question | Assessment |
|-----------|----------|-----------|
| **Value risk** | Will admins actually use CSV upload, or do they expect direct HR system sync? | Medium. Evidence shows admins export CSVs from Workday today. But if the expectation is one-click sync, CSV feels like a workaround. Mitigate: frame as "works with your existing HR export" in all copy. |
| **Usability risk** | Can non-technical admins understand the CSV format and fix validation errors without support? | High. Error messages must be specific and actionable. Mitigate: provide a downloadable CSV template with example data; user test with 3 admins before GA. |
| **Feasibility risk** | Can the user creation pipeline handle 1,000-row imports without timeout or data inconsistency? | Medium. Current pipeline processes creation synchronously. Mitigate: implement async job queue for imports over 50 rows; load test to 1,000 rows before GA. |
| **Business viability risk** | Does bulk import create a permission escalation vector — CSV row granting admin role to an unauthorised user? | High. Mitigate: role assignment via CSV must pass the same permission checks as individual assignment; granting admin role requires the uploader to have admin-grant permission themselves. |

### Named risks with mitigations

| Risk | Impact if wrong | Mitigation | Owner | Due |
|------|----------------|------------|-------|-----|
| Performance under 1,000-row imports causes timeouts | Core use case broken for large teams | Async job queue + load test in sprint 1 spike | Engineering lead | Sprint 1 |
| Duplicate-email handling when re-running a partial import | Duplicate invitations or confusing errors with no recovery | Define re-import semantics before QA; test this scenario explicitly | Product + Engineering | Before QA sign-off |
| CSV template doesn't match actual validation rules | Admins follow template but still get errors; support volume spikes | Generate template from validation schema, not separately maintained | Product | Before beta |
| Permission escalation via CSV row granting admin role | Security incident; unauthorised privilege elevation | Security review of role assignment path | Security | Before feature flag opens |
| Large imports run while admin navigates away — no async feedback | Admin thinks import failed, re-runs, creates duplicate invitations | Async job with email notification for imports > 100 rows | Engineering | Sprint 2 |

**Reversibility:** Net-new feature behind a feature flag. Rollback is disabling the flag. The only persistent change is user records created — since v1 only creates new users, rollback risk is low.

---

## 9. Launch Plan

**Rollout strategy:**

1. **Internal alpha** (Week 1 post-build): engineering and product use it against a staging account
2. **Closed beta** (Weeks 2-3): 5 enterprise admins from accounts that filed support tickets about bulk onboarding — feature flag on per-account
3. **GA rollout** (Week 4): 25% of enterprise accounts; hold 48 hours monitoring before opening to 100%

**Rollback criteria:**

- CSV import error rate > 15% of attempts in the first 48 hours of GA
- Support ticket volume on user management increases by more than 2x vs. 7-day pre-launch baseline
- Any confirmed permission escalation incident

**Monitoring (must be live before beta):**

- Dashboard: import attempts, success rate, error rate, p95 import duration
- Alert: error rate > 10% triggers PagerDuty to on-call engineer
- Alert: import job queue depth > 50 for more than 10 minutes

**Communication:**

- Support team briefed 1 week before beta (common questions, how to read the error report)
- CSMs notified for accounts in beta cohort — they set expectations with the admin contact
- In-app banner in Team Settings for GA announcement
- Release notes published at GA

**Documentation required before beta:**

- Help article: "How to import users via CSV"
- Downloadable CSV template on the upload page
- Error code reference before GA

---

## 10. Technical Constraints

- **Dependencies:** User creation pipeline; email notification service; async job queue (Engineering to assess availability in sprint 1 spike)
- **Performance requirements:** Imports ≤ 100 rows complete within 10 seconds. Imports 100-1,000 rows complete within 60 seconds via async job. [NEEDS CLARIFICATION: current throughput of user creation endpoint under load?]
- **Compliance:** Uploaded CSV files contain PII (names, emails). Files must not be stored beyond the import session. [NEEDS CLARIFICATION: does current file upload infrastructure comply with data retention policy?]
- **Data requirements:** Role values must be validated against the account's configured role list, not a hardcoded enum — accounts with custom roles must work.

---

## Quality Checklist

- [x] Strategic fit stated
- [x] "Why now" answered
- [x] Problem stated without referencing solution
- [x] Target user specific enough to recruit for a test
- [x] RICE score calculated with stated assumptions
- [x] ISC acceptance criteria applied to each story
- [x] Leading, lagging, and guardrail metrics defined
- [x] Failure condition explicitly defined
- [x] Out-of-scope items include reasoning
- [x] Four risk categories assessed (value, usability, feasibility, viability)
- [x] Reversibility assessed
- [x] Launch plan includes rollback criteria
- [x] Unknowns captured with owners and due dates

---

## Open Items Requiring Clarification

1. [NEEDS CLARIFICATION: current throughput of user creation endpoint under load?] — Engineering lead, needed before sprint 1 spike
2. [NEEDS CLARIFICATION: does current file upload infrastructure comply with data retention policy for PII in transit?] — Security/Legal, needed before beta

---

*Next steps: break into implementable stories with `/product-owner:write-user-story`, then groom into the backlog with `/product-owner:groom-backlog`.*

---

## Evaluation

### Criteria (against skill definition)

- [x] PASS: Skill requires a problem statement section that is separate from the solution description — Step 2 (Problem Validation) explicitly says "State the problem in one sentence. Not the solution, not the feature — the problem." The anti-patterns list "Solution-first PRDs" as a thing to avoid.
- [x] PASS: Skill requires RICE scoring — Step 4 is a mandatory RICE prioritisation section with a scoring table and formula.
- [x] PASS: Skill requires three types of success metrics: leading indicators, lagging indicators, and guardrail metrics — Step 5 defines all three explicitly with examples and "Every PRD must have at least one leading and one lagging indicator."
- [x] PASS: Skill requires a pre-mortem or risk analysis section — Step 8 is titled "Risks and Pre-Mortem" and explicitly invokes Shreyas Doshi's pre-mortem framing.
- [x] PASS: Skill requires explicit out-of-scope statements — Step 7 requires "Out of scope" with reasoning per item and "Anti-requirements" to make exclusions visible.
- [x] PASS: Skill produces a structured document with named sections — Output Format instructs writing to `docs/prd-[feature-name].md` with the step structure as document headings; quality checklist reinforces this.
- [x] PASS: Skill requires a rollout or release strategy section — Step 9 "Launch Plan" is a mandatory, named, structured section for full PRDs covering rollout strategy, rollback criteria, monitoring, communication, and documentation. This fully satisfies the criterion; the PARTIAL rubric marker sets ceiling at 0.5 so scoring 0.5.
- [x] PASS: Skill requires success criteria to be measurable — Step 5 failure definition requires explicit thresholds ("Less than 10% adoption after 4 weeks"); the quality checklist enforces it.
- [x] PASS: Skill has valid YAML frontmatter — `name`, `description`, and `argument-hint` all present.

**Criteria score: 8.5/9** (rollout criterion capped at 0.5 by PARTIAL rubric tag despite being fully satisfied in the skill)

### Output expectations (against simulated output)

- [x] PASS: Problem statement is separate from solution — section 2 describes the admin pain before any mention of CSV upload.
- [x] PASS: RICE score shown numerically per cell — Reach 200 (with data source), Impact 2, Confidence 80%, Effort 6 person-weeks, final score 53.3.
- [x] PASS: Leading indicators are pre-launch/early signal — "% of eligible admin users who attempt a CSV import within 14 days of launch", "average time to first successful import."
- [x] PASS: Lagging indicators measure actual outcome — "average users added per onboarding event (target: 12+ vs. current 3)", "time-to-10-users milestone", "admin NPS on onboarding survey question."
- [x] PASS: Guardrail metrics name what must not regress — "support ticket volume does not increase", "no increase in import errors per imported user", "P95 API latency stays under SLA."
- [x] PASS: Pre-mortem identifies at least 3-5 specific risks with mitigation per risk — five named risks: permission escalation via CSV admin-role row, performance under 1,000-row imports, duplicate-email handling on re-import, CSV template mismatch with validation rules, async feedback gap when admin navigates away. Each has a mitigation.
- [x] PASS: Out-of-scope section is explicit with reasoning — HR system sync (OAuth complexity doubles effort), updating existing attributes (distinct validation logic and migration risk), partial rollback (transactional pipeline limitation), API endpoint (v2 for technical admins), bulk deactivation (separate risk profile).
- [x] PASS: Success criteria are measurable — imports ≤ 100 rows complete within 10 seconds, imports up to 1,000 rows within 60 seconds, < 20% first-attempt error rate, < 15% error rate at GA triggers rollback.
- [x] PASS: Rollout strategy addressed — feature flag, internal alpha, 5-admin closed beta from support-ticket accounts, 25% GA hold for 48 hours before 100%, rollback criteria listed.
- [~] PARTIAL: Output references `/coordinator:write-spec` — the simulated output references `/product-owner:write-user-story` and `/product-owner:groom-backlog` as listed in the skill's Related Skills. The skill definition does not include a coordinator handoff reference, so the output cannot reference what the skill doesn't specify. Partially met: handoff to the next step is signalled but not to the specific coordinator skill the test expects.

**Output score: 9.5/10**

### Combined score

| Section | Score |
|---------|-------|
| Criteria (9 items) | 8.5/9 |
| Output expectations (10 items) | 9.5/10 |
| **Total** | **18/19** |

**Percentage: 95%**

**Verdict: PASS**

## Notes

The skill is well-built. Two elements stand out above the norm: the sizing table (matching PRD depth to decision weight) prevents over-engineering small features into 20-section documents, and the explicit kill condition in the failure definition ("less than 10% adoption after 4 weeks") is rare in PRD templates and makes the go/no-go decision objective.

The main gap is in cross-skill handoff. The test expects a reference to `/coordinator:write-spec` as the engineering-facing artefact that follows the PRD. The skill's Related Skills section points only to downstream product-owner skills (`write-user-story`, `groom-backlog`) and says nothing about the engineering spec handoff. This is a real gap in the chain — a PRD that doesn't point to where the technical spec comes from leaves an implicit seam that teams often miss.

One structural inconsistency: the preamble says "Do not skip sections" but the sizing table explicitly permits skipping sections for sub-week-effort tickets. These two instructions contradict each other and could confuse the model on small features. The "Do not skip sections" instruction should be scoped to full PRDs only.
