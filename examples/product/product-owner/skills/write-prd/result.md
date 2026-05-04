# Write Prd

Scenario: Testing whether the write-prd skill definition includes all required sections, RICE scoring, success metrics framework, and pre-mortem analysis.

## Prompt

> /product-owner:write-prd for a bulk user import feature that lets admins upload a CSV to add multiple team members at once.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I've written a comprehensive PRD for the bulk user import feature at `docs/prd-bulk-user-import.md`.

## What's Included

✅ **Full structure** — all 10 mandatory sections following best practices from Marty Cagan, Lenny Rachitsky, and Teresa Torres

✅ **7 detailed user stories** with ISC-compliant acceptance criteria covering:
- CSV upload and preview
- Validation with clear error reporting
- Async processing with progress tracking
- Role assignment
- Confirmation notifications
- Duplicate detection
- Invitation emails

✅ **RICE framework** (ready to calculate once you provide reach numbers)

✅ **Success metrics** — leading, lagging, and guardrail indicators to measure whether this actually delivers value

✅ **Pre-mortem** — identified value, usability, feasibility, and business viability risks with mitigations

✅ **Launch plan** — percentage rollout strategy, rollback triggers, monitoring, and communication

## Critical Unknowns (11 items flagged)

Before this PRD is actionable, you need to clarify:

1. **Strategic fit** — which company OKR does this support? (affects prioritisation)
2. **Why now** — what triggered this? Support tickets? Customer churn? Competitive pressure?
3. **Customer size distribution** — what % of your customers have 50+ users? (affects RICE reach)
4. **Evidence of demand** — do you have support tickets, user interviews, or NPS feedback requesting this?
5. **Conflict handling** — when a CSV contains an email that already exists, should you skip it, error, or update the existing user?

The PRD assumes a mid-market SaaS product with 50-200+ user organizations, but adjust if your customer profile is different.

**Next move:** Sit with product/sales to fill in the open items above, then use the user stories to hand off to design and engineering.

### Artifacts written

#### `work/docs/prd-bulk-user-import.md`

```
# PRD: Bulk User Import via CSV

| Field | Value |
|-------|-------|
| Author | [NEEDS CLARIFICATION: Product Owner name] |
| Status | Draft |
| RICE Score | [Calculated below] |
| Target release | [NEEDS CLARIFICATION: Q target or specific date] |
| Last updated | 2026-05-04 |

---

## 1. Context and Strategic Fit

### Strategic Alignment

[NEEDS CLARIFICATION: Which company OKR does this support?]

**Assumed context:** This feature supports improved onboarding velocity and reduced friction for new customers. For SaaS products, team setup is a critical activation step — reducing time-to-productive-team improves initial retention and expansion.

### Why Now

[NEEDS CLARIFICATION: What triggered this feature request now?]

**Possible drivers** (confirm which apply):
- Support volume: are admins requesting bulk import functionality in tickets?
- Churn signal: are customers citing manual user addition as a friction point?
- Competitive pressure: are competitors offering this?
- New customer segment: did we just start selling to enterprises that require bulk onboarding?
- API maturity: do we have the foundation to build this securely?

### Cost of Inaction

Without bulk import:
- Admins manually invite users one-by-one → slower onboarding for large teams
- [NEEDS CLARIFICATION: Quantify the impact — e.g., "enterprises add 50-100 users per month, each taking 2 mins to add manually = 100-200 minutes per customer"]
- Manual process is error-prone → support burden from incorrectly added users
- Competitive disadvantage if competitors offer this for similar products

---

## 2. Problem Validation

### The Core Problem (One Sentence)

Admins of large teams spend excessive time manually adding users one-at-a-time instead of bulk onboarding entire teams at once.

### Who Has This Problem?

**Primary:** Mid-market to enterprise organization admins (50-2,000+ team members) onboarding new departments or locations.

[NEEDS CLARIFICATION: Validate this is the right segment]
- Are most of your customers in this size range?
- Do smaller orgs care about bulk import, or is this a "nice-to-have" for them?

**Secondary:** IT/HR administrators from companies with structured hiring waves or known upcoming team additions.

### How They Solve It Today

**Current state:**
- Admins use the "Add User" button repeatedly, filling in email, name, role, permissions for each user
- Estimated time per user: 1-2 minutes (enter email, select role, click confirm)
- For a 100-person import: 100-200 minutes (1.5-3 hours)
- Error handling: if a user already exists or email is invalid, admin notices mid-process or after and must correct individually

**Workarounds:**
- [NEEDS CLARIFICATION: Do they use the API directly? Do they script additions? Do they ask support for help?]
- Some may ask support to add users for them (cost to support, delays for customer)
- Some may manually build user list in spreadsheet, then spend hours importing

### Evidence

[NEEDS CLARIFICATION: Provide one or more of:]
- Support tickets referencing bulk import, user mention volume (last 3 months)
- Customer interviews: "I wish I could..." quotes from admins at target accounts
- Churn analysis: did any customers leave citing onboarding friction?
- NPS feedback or feature requests from customer advisory board
- Competitive analysis: which competitors offer this?

**Current evidence status:** Hypothesis — no direct validation provided yet. Recommend user interviews with 3-5 admins at target customer segment before final greenlight.

---

## 3. Target User Definition

### Primary User: Organization Admin

**Role/Title:**
- Called "Admin," "Owner," "Account Admin," or "Organization Manager" depending on company
- Responsible for user management, permissions, and team structure
- May also handle compliance and security settings

**Context:**
- **When:** Onboarding a new team, opening a new office, onboarding a whole department at once
- **Where:** Their admin dashboard or management interface
- **Frequency:** [NEEDS CLARIFICATION: Is this a one-time event per customer or recurring? Do they do this quarterly, annually, or only once?]
  - Hypothesis: Quarterly (new hires), or during restructures

**Technical Sophistication:**
- Can use Excel/Google Sheets comfortably
- May not know REST APIs or command-line tools
- Expects a web UI or simple file upload, not code
- Comfortable with the concept of CSV but may not have written one

**Current Tools in Workflow:**
- HR system (Workday, BambooHR, Guidepoint): source of truth for employee data
- Email/SSO system (Azure AD, Okta, Google Workspace): existing directory
- Spreadsheet tool (Excel, Google Sheets): staging area for manual work
- [NEEDS CLARIFICATION: Does the product already integrate with any of these? Should this feature integrate?]

### Secondary User: IT/Support

- Uses this feature to help customers during onboarding calls
- Validates CSV before upload (catching malformed data)
- Monitors for errors and troubleshoots failed imports

---

## 4. RICE Prioritisation

| Factor | Score | Reasoning |
|--------|-------|-----------|
| **Reach** | [NEEDS CLARIFICATION] | How many organizations/users will this affect per quarter? <br> **Assumption:** If 30% of customer base is "medium+" (50+ users) and 50% of those do at least one bulk import per year, that's roughly _N_ customers/quarter. Provide actual number from CRM. |
| **Impact** | **2 (High)** | Reduces onboarding friction for a key activation moment. Time saved: 1-3 hours per customer per import. Not transformative for the product experience overall, but materially speeds up a critical path. |
| **Confidence** | **50%** | Educated guess that bulk import matters to mid-market customers, but no validated evidence yet. No user interviews or support ticket volume data provided. |
| **Effort** | **3-4 weeks** | Engineering: 2 weeks (upload, parse, validation, async processing). Design/QA: 1 week. Docs: 0.5 weeks. Assumes [NEEDS CLARIFICATION: existing user management API/DB structure]. |

**RICE Score** = (Reach × 2 × 0.5) / 3.5 = **[Reach] × 0.29**

[NEEDS CLARIFICATION: Provide actual reach number.]

**Example:** If 15 customers per quarter would use this feature, score = 4.3 (moderate-high priority). If 5 customers/quarter, score = 1.4 (lower priority, consider deferring).

**Comparison:** [NEEDS CLARIFICATION: How does this score against other initiatives in the current roadmap?]

---

## 5. Success Metrics

### Leading Indicators (measure within week 1 of launch)

- **Feature discovery rate:** % of admin users who discover the CSV import option in the first week (target: >40%)
- **Activation rate:** % of discovered users who actually attempt an import (target: >30%)
- **Error rate:** % of imports that fail or produce validation errors (target: <10%)
- **Time-to-completion:** Average time from "click upload" to "users created" (target: <5 minutes for 50-person import)

### Lagging Indicators (measure after 4-8 weeks)

- **Adoption rate:** % of eligible customers (50+ users) who complete at least one bulk import (target: >25%)
- **Frequency:** Average imports per customer per month (target: 0.3-0.5, i.e., bulk imports happen regularly, not just once)
- **Onboarding completion rate:** Do accounts with bulk import complete their first deployment/workflow faster than those using manual add? (target: +15% faster to first action)
- **Onboarding retention:** 30-day retention for customers who use bulk import vs. manual import (target: +10 percentage points)
- **Support ticket volume:** Are bulk imports generating more support tickets than manual adds? (target: no increase or net decrease if bulk reduces manual overhead)

### Guardrail Metrics (must not regress)

- **Existing user management features:** Manual "Add User" button usage must not drop (indicates we're not replacing, just adding)
- **Permission/role assignment:** Errors in permission assignment (target: no regression)
- **API latency:** User management API response time (target: <200ms p99)
- **Data integrity:** No duplicate users created, no orphaned invitations (target: zero incidents)

### Failure Definition

Kill decision triggered if:
- **Adoption:** <10% of eligible customers use bulk import after 8 weeks
- **Reliability:** >20% of imports fail or produce errors
- **Support burden:** Support tickets related to bulk import exceed 10/week without ability to self-service
- **Data issues:** Any incident of bulk import creating duplicate users or corrupting team structure

---

## 6. User Stories with ISC Acceptance Criteria

### US-1: Admin uploads CSV file with user list

As an **organization admin**, I want to **upload a CSV file containing a list of users** so that **I can import multiple team members at once instead of adding them one-by-one**.

**Acceptance Criteria:**

- [ ] **[I]** Admin can access "Bulk Import" option from the user management page
- [ ] **[S]** Click "Upload CSV" opens a file picker that accepts `.csv` files only
- [ ] **[S]** File size limit is enforced (target: 10 MB max) with clear error message if exceeded
- [ ] **[S]** After selecting file, admin sees a preview of parsed data (first 5 rows) before confirming import

**Edge Cases:**

- Admin uploads a non-CSV file (e.g., `.xlsx`, `.txt`) → error message: "Please upload a CSV file"
- Admin uploads a 50 MB file → error: "File exceeds 10 MB limit"
- Admin closes browser during file upload → upload is cancelled, no partial data created
- Admin selects file but doesn't confirm → no import occurs; data is discarded

---

### US-2: CSV is validated and errors are shown clearly

As an **admin**, I want to **see validation errors before the import runs** so that **I can fix the data and retry instead of discovering errors after import**.

**Acceptance Criteria:**

- [ ] **[I]** CSV header row is validated against required columns: `email`, `first_name`, `last_name`, `role`
- [ ] **[S]** If required column is missing, admin sees: "Missing required column: [column_name]. Required columns: email, first_name, last_name, role"
- [ ] **[S]** Each row is validated: email format, name length (min 1 char), role exists in system
- [ ] **[S]** Validation runs before import starts; errors are shown in a list with row numbers and specific issues
- [ ] **[S]** Admin can download a report of errors (CSV) for offline fixing

**Edge Cases:**

- Email column contains invalid format: "john@" → error: "Row 5: Invalid email format"
- Name field is empty → error: "Row 12: first_name is required"
- Role field contains a role that doesn't exist in the system → error: "Row 3: 'SuperUser' is not a valid role. Valid roles: Admin, Member, Guest"
- CSV has duplicate emails across rows → warning: "Row 5 and Row 12 contain the same email address"
- Email already exists as active user → [NEEDS CLARIFICATION: Skip, error, or update? Define conflict handling]

---

### US-3: Import creates users asynchronously with progress tracking

As an **admin**, I want to **see progress as users are created** so that **I know the import is working and how long it will take**.

**Acceptance Criteria:**

- [ ] **[I]** After validation passes, import runs asynchronously (doesn't lock up the UI)
- [ ] **[S]** Admin is redirected to an import status page showing: "Importing 50 users... (12 complete, 38 pending)"
- [ ] **[S]** Status updates in real-time (or refreshes every 5 seconds if not WebSocket)
- [ ] **[S]** Progress bar shows percentage complete
- [ ] **[S]** Estimated time remaining is shown (e.g., "~2 minutes remaining")
- [ ] **[S]** If import completes, admin sees: "Successfully imported 50 users" with option to view newly created users

**Edge Cases:**

- Admin closes status page mid-import → import continues in background; admin can navigate back to check status anytime
- Network disconnects mid-import → import continues; next page reload shows current progress
- Import partially succeeds (30 created, 10 failed) → admin sees results with list of failures and reasons

---

### US-4: Users are created with correct role and permissions

As an **admin**, I want to **assign a role to each imported user** so that **permissions are set correctly on creation instead of requiring manual adjustment**.

**Acceptance Criteria:**

- [ ] **[I]** CSV supports a `role` column with values: `admin`, `member`, `guest`
- [ ] **[S]** If `role` column is omitted, default role is `member` (with clear warning before import)
- [ ] **[S]** Each user is created with the specified role and associated permissions
- [ ] **[S]** Users created via bulk import have the same permissions as users added manually with the same role

**Edge Cases:**

- Admin specifies `role: admin` for 20 users → all 20 receive admin permissions (consider warning if adding many admins?)
- Admin leaves `role` column blank on some rows → [NEEDS CLARIFICATION: apply default, or error?]

---

### US-5: Admin receives confirmation email/notification of import results

As an **admin**, I want to **receive a summary of the import** so that **I have a record of who was added and whether there were any issues**.

**Acceptance Criteria:**

- [ ] **[I]** After import completes, admin receives email with subject: "Bulk User Import Complete"
- [ ] **[S]** Email includes: total users added, list of new users (name, email, role), any failures with reasons
- [ ] **[S]** Email is sent to the admin who initiated the import
- [ ] **[S]** Import summary is also available in the dashboard under "Import History" for 90 days

**Edge Cases:**

- Import has failures → email includes section "Failed to Import (5)" with detailed reasons per row
- Admin email is no longer valid → [NEEDS CLARIFICATION: where does notification go?]

---

### US-6: Duplicate detection prevents accidental re-imports

As an **admin**, I want to **know if a user already exists** so that **I don't accidentally create duplicates**.

**Acceptance Criteria:**

- [ ] **[I]** Before import, system checks each email against existing active users in the organization
- [ ] **[S]** If email already exists, admin sees warning: "User john@example.com already exists in your organization"
- [ ] **[S]** Admin can choose to: skip this user, update existing user, or continue anyway
- [ ] **[S]** [NEEDS CLARIFICATION: Should bulk import support UPSERT (create or update) or only create?]

**Edge Cases:**

- Admin is re-importing the same CSV twice → second import detects all users exist and prompts "All users already exist. Continue to add duplicate invite?"
- One CSV row has a duplicate email within the same file → caught in validation (US-2)

---

### US-7: Imported users receive activation invitations

As an **imported user**, I want to **receive an invitation email** so that **I can set up my account and join the team**.

**Acceptance Criteria:**

- [ ] **[I]** Each newly created user receives an invitation email at their provided email address
- [ ] **[S]** Invitation includes: sign-up link, sender (the admin who added them), organization name
- [ ] **[S]** Link is valid for 7 days; after 7 days, admin can re-send or resend in bulk
- [ ] **[S]** Invitation email uses existing invitation template (no special bulk-import-specific email)

**Edge Cases:**

- User doesn't receive email → admin can re-send from user management page
- Email bounces → [NEEDS CLARIFICATION: Mark user inactive, notify admin, or retry?]

---

## 7. Scope Definition

### In Scope

- CSV file upload via web UI
- Validation of required columns: `email`, `first_name`, `last_name`, `role`
- Basic data validation: email format, field presence, role existence
- Async import processing with real-time progress tracking
- Duplicate detection and conflict handling (skip existing users)
- Bulk invitation emails to newly created users
- Import history and results dashboard (view past imports, download reports)
- Support for roles: `admin`, `member`, `guest` (or [NEEDS CLARIFICATION: confirm role list])
- File size limit: 10 MB max (500-1000 users per import)

### Out of Scope

- **SSO/Directory Sync (deferred to v2):** Automatic sync from Azure AD, Okta, Google Workspace. Valuable but adds significant complexity; bulk import alone solves immediate need for manual control.
- **Custom field import:** Importing custom fields or profile data beyond name/email/role. Scope limited to core user creation fields.
- **Scheduled/recurring imports:** Repeating bulk imports on a schedule. One-time manual uploads solve the primary use case; recurring imports may require deeper directory integration.
- **API-based bulk import:** Programmatic CSV upload via API. Start with UI; API can follow if demand is high.
- **Bulk import from other platforms:** Migration from Slack, Monday.com, etc. Out of scope — focus on own CSV format.
- **Role assignment workflows:** Complex permission matrices or conditional role assignment based on department. Stick to direct role specification in CSV.

**Reasoning:** Phased approach: V1 solves the immediate problem (admins can upload 50-100 users at once). V2 can add integrations, scheduling, and API support if adoption is strong.

### Anti-Requirements

- We are NOT building a full employee directory importer (that's directory sync, separate feature)
- We are NOT auto-assigning roles based on hierarchies or departments (manual specification is intentional)
- We are NOT providing a UI to edit rows in-place before import (users should fix CSV offline and re-upload)
- We are NOT supporting password import (users must set via activation email)

---

## 8. Risks and Pre-Mortem

### Value Risk: Will admins actually want this?

**Assessment:**

| Question | Evidence For | Evidence Against | Confidence |
|---|---|---|---|
| Do customers have large teams? | [NEEDS CLARIFICATION: How many customers have 50+ users?] | If most are <20 users, bulk import benefits few | 50% |
| Is manual add a real pain point? | [NEEDS CLARIFICATION: Support tickets, NPS feedback] | Could be low-priority complaint | 50% |
| Is this the right solution? | CSV is familiar, low-barrier | Might prefer SSO sync; CSV is outdated | 60% |

**Hypothesis:** Moderate value risk. Bulk import helps *some* customers meaningfully, but may not be a must-have for core audience. **Mitigation:** User interviews with 3-5 target admins before finalizing design.

### Usability Risk: Can admins figure out how to use it?

**Assessment:**
- CSV format is well-understood; low learning curve
- UI should be self-explanatory if following existing patterns
- Main risk: error messages are confusing, admins don't know why import failed
- Secondary risk: data validation is too strict or too lenient

**Mitigation:**
- Error messages must be specific and actionable (not "invalid data")
- Provide a sample CSV template for download
- Add help text on the upload page: "Ensure your CSV has columns: email, first_name, last_name, role"

### Feasibility Risk: Can we build this with current tech/team/timeline?

**Assessment:**

[NEEDS CLARIFICATION: Fill in technical details]

**Assumed feasibility:** 3-4 weeks is realistic if:
- User management API/DB already exists (not starting from scratch)
- Async job queue exists (can't block UI during 1000+ user creation)
- Email system already has invitation templates
- CSV parsing library available in your stack (Python: `csv`, Node: `csv-parse`, etc.)

**Technical concerns:**
- Rate limiting: Creating 1000 users rapidly may hit rate limits or overload DB. Need to batch and throttle.
- Transaction handling: Partial failures (50 created, 50 failed) must be handled cleanly — can't leave orphaned data.
- File upload security: Validate MIME type, scan for malicious content, enforce size limits.

### Business Viability Risk: Does this work for the business?

**Assessment:**

- **Pricing impact:** [NEEDS CLARIFICATION: Does bulk import affect pricing? (e.g., per-user seat costs)] Clarify if this creates new revenue or cost.
- **Compliance/Legal:** Does bulk import raise data privacy concerns? (e.g., importing PII, storing CSVs) Confirm GDPR/privacy compliance.
- **Support cost:** Will bulk import generate support volume? Mitigation: robust validation and error messages reduce support burden.

**Open Questions:**

| Question | Impact if wrong | Owner | Due date |
|---|---|---|---|
| How many customers per quarter would use this? | If <5, RICE score is too low to prioritize | [NEEDS CLARIFICATION: PM/Sales] | Before greenlight |
| Should we support UPSERT (create or update)? | If users expect update capability, skip will frustrate | [NEEDS CLARIFICATION: Product/Eng] | During design phase |
| Does bulk import need SSO integration eventually? | If yes, architecture now to avoid later rework | [NEEDS CLARIFICATION: Eng Lead] | Before development |
| What is max CSV size we'll support? | If we set too low (100 users), customers frustrated; too high (10k), performance risk | [NEEDS CLARIFICATION: Tech Lead] | Before development |
| Do we charge per import or per user added? | Affects pricing and billing logic | [NEEDS CLARIFICATION: Finance] | Before launch |

### Reversibility Assessment

**High reversibility** (feature flag, easy rollback):
- Can ship behind feature flag (admin can enable/disable)
- Can remove CSV upload UI without breaking existing user creation
- Users are created via existing API; no breaking changes to data model
- **Decision confidence:** Can greenlight with lower certainty than irreversible work

**Irreversible or hard to reverse:**
- If we change the user creation API signature to accept bulk data, that's hard to undo
- If we add a new column to users table permanently, harder to remove later
- [NEEDS CLARIFICATION: Are we aware of any hard-to-reverse decisions in this feature?]

---

## 9. Launch Plan

### Rollout Strategy

**Recommended: Percentage Rollout with Beta Group**

1. **Week 1 (Internal Testing):** Ship behind feature flag to internal team + 1-2 partner customers. Test with real CSVs, find data edge cases.
2. **Week 2 (Beta Group):** Open to 10% of mid-market customers (those with 50+ users). Monitor adoption, support volume, errors.
3. **Week 3 (Gradual Rollout):** Expand to 50% of eligible customers. Watch guardrail metrics.
4. **Week 4 (GA):** Enable for all customers. Monitor for 1 week post-launch.

[NEEDS CLARIFICATION: Adjust timeline based on engineering capacity and launch window]

### Rollback Criteria

Trigger immediate rollback if:
- Import error rate exceeds 20% (e.g., >20% of rows fail across any import)
- Support tickets exceed 10 related to bulk import in a single day
- Data integrity issue detected (duplicate users, orphaned data, permission corruption)
- File upload causes API latency to exceed 500ms p99
- Any security issue discovered (e.g., CSV injection, unauthorized access)

**Rollback process:** Feature flag disabled → bulk import UI hidden. Existing imports stay as-is; no data rollback.

### Monitoring

Before launch, set up dashboards/alerts for:

- **Import volume:** Imports per day, files processed, total users created
- **Error metrics:** % of imports with >0 errors, most common error types
- **Performance:** CSV parsing time, user creation latency (p50, p95, p99)
- **Reliability:** Import success rate, file upload failure rate, job queue health
- **Support:** Bulk import tickets, reopens, resolution time
- **Data quality:** Duplicate user detection, permission misassignments, orphaned invitations

### Communication Plan

**Before launch:**
- Announce feature in product roadmap update (if public)
- Email to [NEEDS CLARIFICATION: eligible customer segment] with feature overview
- Write help article: "How to bulk import users with CSV"

**At launch:**
- In-app notification or banner: "New: Import multiple users at once with CSV"
- Help article linked from UI
- Changelog entry

**Post-launch:**
- If adoption is strong: case study or customer highlight
- If adoption is weak: investigate why (survey, interviews)

### Documentation to Create

- **Help article:** "Bulk Import Users via CSV" (how-to guide with screenshots)
- **CSV template:** Download-able example file with header row
- **Troubleshooting:** Common errors and how to fix them
- **API docs:** [If API-based import added in v2]
- **Admin guide:** Update user management docs to reference bulk import

---

## 10. Technical Constraints

### Dependencies

- **User management API:** Must support creating users in batch (or this feature relies on repeated single-user creation calls; clarify if that's acceptable for performance)
- **Email system:** Existing invitation templates and bulk email dispatch
- **Async job queue:** For processing imports without blocking UI (e.g., Bull, Celery, AWS SQS)
- **Database:** User table with `email` (unique index), `first_name`, `last_name`, `role` columns

[NEEDS CLARIFICATION: Do these systems exist? Any limitations or gotchas?]

### Performance Requirements

- **CSV parsing:** <5 seconds for 1000-row CSV (client-side parsing before upload)
- **Validation:** <10 seconds for 1000 rows (server-side)
- **User creation:** Aim for >10 users/second (100 users created in <10 seconds)
- **Progress updates:** Real-time or every 5 seconds (latency-acceptable for progress bar)

### Compliance & Security

- **Data privacy:** No sensitive data (passwords, SSNs) accepted in CSV; invite-based activation only
- **File upload security:**
  - Validate MIME type (must be `text/csv`)
  - Enforce max file size (10 MB)
  - Scan for malicious content (CSV injection, embedded code)
  - Do not store raw CSVs long-term; delete after processing
- **Audit logging:** Log who imported which CSV and results (for compliance/troubleshooting)
- **Rate limiting:** Prevent spam imports (e.g., max 10 imports/day per user)

### Data Requirements

- CSV must have: `email`, `first_name`, `last_name`, `role`
- Optional columns: [NEEDS CLARIFICATION: departments, manager, start_date, etc.?]
- Data assumed clean (no validation that values make business sense, only technical validation)

---

## Summary: Open Items Requiring Clarification

| # | Item | Priority | Owner | Due |
|---|---|---|---|---|
| 1 | Strategic OKR alignment — which goal does this serve? | High | Product Lead | Before greenlight |
| 2 | Why now? What triggered this request? (support tickets, customer churn, competitive pressure) | High | Product Lead | Before greenlight |
| 3 | Customer segment size — how many customers have 50+ users? | High | Sales/CS | Before RICE calculation |
| 4 | Adoption metrics — actual evidence of bulk import demand (tickets, interviews, NPS feedback) | High | Product/CS | Before design |
| 5 | Conflict handling — if email already exists, should we skip, error, or offer UPSERT? | High | Product/Eng | During design |
| 6 | Max file size and user import limits (current 10 MB = ~500-1000 users; confirm this is right) | Medium | Eng | Before development |
| 7 | Does user management API/async job queue already exist in current system? | Medium | Eng Lead | Before estimation |
| 8 | Optional CSV columns beyond email/name/role — departments, manager, custom fields? | Medium | Product | During design |
| 9 | Email bounce handling — what happens if invited user's email bounces? | Medium | Product | Before launch |
| 10 | Pricing impact — does bulk import affect per-user costs or support SKU? | Medium | Finance | Before launch |
| 11 | SSO/directory sync timeline — do customers expect this eventually? Does architecture need to account for it? | Low | Eng | Before development |

---

## Next Steps

1. **Validation (this week):** Conduct 3-5 user interviews with target admins (50+ user organizations) to confirm problem and desired solution
2. **Clarification meeting:** Review open items above with product, engineering, and design leads
3. **Design phase:** Once problem validated, design CSV format, error UX, and import flow
4. **Spec review:** Revisit this PRD with learnings from interviews; update assumptions
5. **Greenlight:** After 3 amigos review (PM + Eng + QA), proceed to implementation


```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.5/18.0 (92%) |
| Evaluated | 2026-05-04 |
| Target duration | 97104 ms |
| Target cost | $0.1447 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires a problem statement section that is separate from the solution description | PASS | Section 2 'Problem Validation' opens with 'The Core Problem (One Sentence): Admins of large teams spend excessive time manually adding users one-at-a-time...' and describes current-state pain before any CSV solution is mentioned. The solution (CSV upload) appears first in Section 7 Scope. |
| c2 | Skill requires RICE scoring to justify prioritisation of the feature | PASS | Section 4 'RICE Prioritisation' contains a table with Reach (flagged for clarification), Impact (2 – High), Confidence (50%), Effort (3-4 weeks), and provides the formula 'RICE Score = (Reach × 2 × 0.5) / 3.5' with an example calculation. |
| c3 | Skill requires three types of success metrics: leading indicators, lagging indicators, and guardrail metrics | PASS | Section 5 'Success Metrics' has three explicitly named subsections: 'Leading Indicators (measure within week 1 of launch)', 'Lagging Indicators (measure after 4-8 weeks)', and 'Guardrail Metrics (must not regress)'. |
| c4 | Skill requires a pre-mortem or risk analysis section — what could go wrong with this feature | PASS | Section 8 'Risks and Pre-Mortem' covers four risk categories: Value Risk, Usability Risk, Feasibility Risk, and Business Viability Risk, each with assessment and mitigations. |
| c5 | Skill requires explicit out-of-scope statements — not just what's included but what's excluded | PASS | Section 7 has an 'Out of Scope' subsection listing six explicit exclusions (SSO/Directory Sync, custom field import, scheduled imports, API-based import, cross-platform import, complex role workflows) plus an 'Anti-Requirements' subsection with four more. |
| c6 | Skill produces a structured document with named sections that a team can review, not a prose narrative | PASS | The PRD has 10 numbered sections (Context and Strategic Fit, Problem Validation, Target User Definition, RICE Prioritisation, Success Metrics, User Stories with ISC Acceptance Criteria, Scope Definition, Risks and Pre-Mortem, Launch Plan, Technical Constraints) with tables, checklists, and subsections throughout. |
| c7 | Skill requires a rollout or release strategy section — partial credit if phasing is mentioned but not required as a structured section | PARTIAL | Section 9 'Launch Plan' contains a 'Rollout Strategy' subsection with a 4-week phased plan (internal testing → 10% beta → 50% gradual → GA), plus rollback criteria, monitoring dashboards, communication plan, and documentation list. Ceiling caps this at 0.5. |
| c8 | Skill requires success criteria to be measurable — "users can import" is not acceptable, "95% of CSV imports complete without error" is | PASS | Metrics include specific targets: 'Feature discovery rate: >40%', 'Error rate: <10%', 'Time-to-completion: <5 minutes for 50-person import', 'Adoption rate: >25%', '30-day retention: +10 percentage points', 'API latency: <200ms p99'. |
| c9 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The captured output (chat response and PRD document) does not include the skill definition file. The PRD itself uses a markdown table for metadata (Author, Status, RICE Score, etc.) rather than YAML frontmatter. The skill's own definition file with name/description/argument-hint fields is not surfaced in the output. |
| c10 | Output's problem statement is separate from the solution — describes the user pain (admins onboarding 50+ team members one at a time burns hours and is error-prone) before any reference to CSV upload as the solution | PASS | Section 2 states 'Admins of large teams spend excessive time manually adding users one-at-a-time' and quantifies pain ('For a 100-person import: 100-200 minutes'). CSV as solution does not appear until Section 7 Scope Definition. |
| c11 | Output's RICE score is shown numerically per cell — Reach (admins onboarding new teams per quarter, e.g. 200), Impact (1 — significant time saved per onboarding event), Confidence (% based on user-research signal strength), Effort (story points or weeks) | PASS | RICE table shows Impact: 2 (High), Confidence: 50%, Effort: 3-4 weeks. Reach is marked '[NEEDS CLARIFICATION]' with explanation and an example calculation ('If 15 customers per quarter, score = 4.3'). Three of four cells are numeric; Reach is correctly flagged as requiring input data not provided in the prompt. |
| c12 | Output's leading-indicator metrics are pre-launch / early signal — e.g. "% of admin users who try the bulk-import feature within 2 weeks of launch", "average time to first successful import" | PASS | Leading indicators include 'Feature discovery rate: % of admin users who discover the CSV import option in the first week (target: >40%)', 'Activation rate: % of discovered users who actually attempt an import (target: >30%)', and 'Time-to-completion: Average time from upload to users created (target: <5 minutes)'. |
| c13 | Output's lagging-indicator metrics measure the actual outcome — e.g. "average users added per onboarding event (target: 12+ vs current 3)", "admin NPS on team-onboarding question" | PASS | Lagging indicators include 'Adoption rate: % of eligible customers (50+ users) who complete at least one bulk import (target: >25%)', 'Onboarding completion rate: +15% faster to first action', '30-day retention: +10 percentage points vs manual import', and 'Support ticket volume' comparison. |
| c14 | Output's guardrail metrics name what must NOT regress — e.g. "no increase in import errors per imported user", "support ticket volume on user-management does not increase" | PASS | Guardrail Metrics section explicitly states: 'Manual Add User button usage must not drop', 'Permission/role assignment errors: no regression', 'API latency: <200ms p99', 'Data integrity: no duplicate users created, no orphaned invitations (target: zero incidents)'. |
| c15 | Output's pre-mortem identifies at least 3-5 specific risks — e.g. "permission escalation via CSV row granting admin role", "performance under 1000-row imports", "duplicate-email handling when re-running an import" — with mitigation per risk | PASS | Section 8 identifies: (1) Value Risk with user-interview mitigation, (2) Usability Risk with actionable error messages and CSV template mitigations, (3) Feasibility Risk with specific technical concerns (rate limiting, transaction handling, CSV injection, file upload security) and mitigations, (4) Business Viability Risk with open-questions table. More than 5 specific risks named. |
| c16 | Output's out-of-scope section is explicit — e.g. "v1 does NOT support: importing from external sources (Workday, Okta), updating existing user attributes, partial-roll-back if some rows fail" — so reviewers see the scope cliff | PASS | 'Out of Scope' lists SSO/Directory Sync ('deferred to v2'), custom field import, scheduled/recurring imports, API-based bulk import, bulk import from other platforms, role assignment workflows — each with a reasoning note. Anti-Requirements adds four more explicit exclusions including 'NOT building a full employee directory importer'. |
| c17 | Output's success criteria are measurable — "95% of imports under 100 rows complete without errors", "import of 1,000 rows completes within 30 seconds" — never "users can import" | PASS | Every metric has a numeric target: discovery >40%, activation >30%, error rate <10%, time-to-completion <5 minutes, adoption >25%, retention +10pp, API latency <200ms p99. Kill criteria are also numeric: <10% adoption after 8 weeks, >20% import failure rate, >10 support tickets/week. |
| c18 | Output addresses the rollout strategy section — feature flag, beta cohort (e.g. 5 enterprise admins), staged GA — even if it's not the strongest section | PASS | Section 9 'Rollout Strategy' explicitly covers: Week 1 'ship behind feature flag to internal team + 1-2 partner customers', Week 2 '10% of mid-market customers (those with 50+ users)' as beta, Week 3 '50% of eligible customers', Week 4 'GA'. Feature flag also referenced in Reversibility Assessment ('Can ship behind feature flag'). |
| c19 | Output references the related coordinator skill (`/coordinator:write-spec`) for the engineering-facing technical spec, since the PRD is the product-facing artefact and a separate technical spec follows | FAIL | Neither the chat response nor the PRD document contains any reference to '/coordinator:write-spec' or any coordinator skill for the engineering spec. The 'Next Steps' section mentions 'Spec review' and '3 amigos review' but does not point to or invoke a downstream technical spec skill. |

### Notes

The output is a comprehensive, well-structured PRD that satisfies nearly all substantive criteria. It correctly separates problem from solution, provides RICE scoring with numerical values and a clear formula, includes all three metric types with specific targets, covers pre-mortem with multiple risk categories and mitigations, and has an explicit out-of-scope section. The rollout plan is thorough (feature flag, beta cohort, staged GA). Two criteria failed: c9 (skill YAML frontmatter) cannot be verified from the captured output since the skill definition file is not surfaced, and c19 (reference to `/coordinator:write-spec`) is simply absent from both the chat response and the artifact. The RICE Reach field is appropriately flagged as needing clarification rather than being invented, which is the right behavior given the prompt provided no reach data.
