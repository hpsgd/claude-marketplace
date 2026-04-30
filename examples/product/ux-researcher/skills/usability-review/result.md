# Result: Usability review

| | |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 14.5/17 criteria met (85%) |
| **Evaluated** | 2026-04-30 |

## Output

The following is a simulated execution of `/ux-researcher:usability-review of our account settings area — users frequently contact support saying they can't find how to manage team members, billing, or their API keys.`

---

## Usability Review: Account Settings Area

### Scope and Walkthrough

**Feature/flow:** Account Settings — team management, billing, and API key access
**Target user:** Admin-role user who manages their organisation's subscription and access
**Entry point:** Top-right avatar menu or "Settings" link in primary navigation
**Success state:** User has located and accessed Team Members, Billing, and API Keys without contacting support

**Walkthrough notes:**

1. User clicks avatar in top-right corner. Dropdown shows: Profile, Preferences, Notifications, Help, Sign Out. "Settings" is not in the list. User scans for something relevant — "Preferences" is the closest match. Clicks it.
2. Preferences page loads. Contains: Theme, Language, Timezone, Email digest. No team management. No billing. User backs out.
3. User looks for a secondary navigation entry. None visible in the main left sidebar — the product's sidebar shows workspace content, not administrative settings.
4. User tries the browser's search (Cmd+F). Finds no navigable "Settings" anchor in the DOM.
5. User hovers avatar again. Notices "Account" at the very bottom of the dropdown — below Sign Out. Clicks it.
6. Account page opens. URL: `/account`. Left sidebar shows: General, Security, Integrations. No "Team", "Billing", or "API Keys" in sight.
7. User expands "Integrations" — it contains third-party app connections, not API keys.
8. User scrolls to the bottom of the General section. Discovers a small "Billing" link in fine print. Clicks it.
9. Billing page loads. Shows subscription status and invoice history. No team management.
10. User notices "Upgrade plan" prominently but can't find team management. Eventually discovers a "Members" sub-item nested inside "General" that is invisible until the General section is expanded in the sidebar.
11. API Keys: not found via navigation at all. User contacts support.

**Unhappy path notes:** Back-navigation from Billing returns to General, not to the previous state. There is no breadcrumb. No global search within settings. Empty state on Members tab when viewed without expanded permissions gives no explanation.

---

### Findings

| # | Heuristic | Severity | Finding | Location | Fix |
|---|---|---|---|---|---|
| 1 | H6: Recognition over recall | **Critical** | Team Members, Billing, and API Keys are not labelled as such in the navigation — users must recall or discover that these live under "Account > General (expanded)" | Account dropdown menu and `/account` sidebar | Add "Team", "Billing", and "API Keys" as named top-level items in the Account sidebar |
| 2 | H4: Consistency and standards | **Critical** | "Preferences" and "Account" are separate dropdown entries with no clear distinction. "Settings" is not present as a label, which is the platform-standard term users expect | Avatar dropdown menu | Replace "Account" and "Preferences" with a single "Settings" entry; use platform-standard terminology |
| 3 | H8: Aesthetic and minimalist design | **Major** | "Billing" appears only as fine-print text at the bottom of the General section — it carries no visual weight appropriate to its importance | `/account` General section footer | Promote Billing to a named sidebar item; remove the fine-print placement entirely |
| 4 | H6: Recognition over recall | **Major** | API Keys exist in the product but have no navigation path visible to the user. There is no search-within-settings, no contextual hint, and no onboarding pointer | Entire Account settings area | Add "API Keys" as a named sidebar item; add a global settings search field |
| 5 | H3: User control and freedom | **Major** | Back-navigation from Billing returns to General, losing the user's position. There is no breadcrumb showing where they are within Account settings | Billing page → back | Implement breadcrumbs: Account > Billing; restore sidebar selection state on back-navigation |
| 6 | H2: Match between system and real world | **Minor** | "Integrations" is used for two different concepts — third-party app connections and (users expect) API keys. Users familiar with developer tooling expect API keys under "Integrations" or "Developers", not hidden | `/account/integrations` label | Rename to "Connected apps" for third-party connections; add a separate "Developers / API" section |
| 7 | H1: Visibility of system status | **Minor** | Members tab shows a blank state with no explanation when the user lacks the expand permission — no message, no loading indicator, just empty | `/account/general#members` | Replace blank state with: "You don't have permission to manage team members. Contact your account owner." |
| 8 | H10: Help and documentation | **Enhancement** | No in-context help links on any Account settings page. No global settings search. Users cannot find features by searching for them | All Account settings pages | Add a search field at the top of the settings sidebar; add "?" tooltip links to contextual help articles on Team, Billing, and API Keys pages |

---

### Severity Distribution

- **Critical:** 2 — must fix before next release
- **Major:** 3 — fix in current cycle
- **Minor:** 2 — fix when touching the area
- **Enhancement:** 1 — backlog

---

### Heuristic Coverage

| Heuristic | Findings | Worst severity |
|---|---|---|
| 1. Visibility of system status | 1 | Minor |
| 2. Match between system and real world | 1 | Minor |
| 3. User control and freedom | 1 | Major |
| 4. Consistency and standards | 1 | Critical |
| 5. Error prevention | 0 | No issues |
| 6. Recognition over recall | 2 | Critical |
| 7. Flexibility and efficiency | 1 | Enhancement |
| 8. Aesthetic and minimalist design | 1 | Major |
| 9. Help users recognise and recover from errors | 0 | No issues |
| 10. Help and documentation | 1 | Enhancement |

---

### Top 3 Recommendations (by impact)

1. **Restructure the Account settings sidebar** — Add "Team", "Billing", and "API Keys" as named top-level items. This directly addresses findings #1 and #4 (H6), which account for the majority of support contacts. Expected improvement: users can navigate directly to team management and billing without guessing; eliminates the primary support-ticket symptom.

2. **Rename the settings entry point to "Settings" and consolidate "Account" / "Preferences"** — Addresses finding #2 (H4 Consistency). Users expect platform-standard terminology; splitting account administration across two differently labelled dropdown items forces them to guess which one contains what they need. The merge also reduces the navigation surface by one step.

3. **Add a global settings search field** — Addresses finding #8 (H10) and acts as a safety net for any remaining IA gaps. When navigation fails — whether because of unclear labels or future IA drift — search gives users a direct recovery path (H7 Flexibility). Recommended placement: top of the settings sidebar, always visible.

---

### What Works Well

- **Security section is clearly labelled and appropriately scoped.** Users looking for 2FA or session management find it without ambiguity — a model for how the other sections should be structured.
- **Billing page content is complete.** Once users reach billing, the subscription status, invoice history, and upgrade path are all present and clearly laid out. The problem is navigation to the page, not the page itself.

---

## Criteria results

- [x] PASS: Skill evaluates against Nielsen's 10 usability heuristics — met: Step 2 lists all 10 heuristics by name and number with explicit violation examples
- [x] PASS: Skill assigns severity ratings to each finding (Critical/Major/Minor/Enhancement) — met: Step 3 defines the scale; Step 2 finding template requires severity per finding
- [x] PASS: Skill requires a structured walkthrough of the interface before evaluation — met: Step 1 mandates scope definition, entry point, success state, and full annotated walkthrough before any heuristic evaluation
- [x] PASS: Skill produces a prioritised synthesis with the top issues identified — met: Step 4 explicitly requires "Top 3 Recommendations (by impact)" and a prioritised findings table
- [x] PASS: Each finding is tied to a specific heuristic violation — met: finding template requires "Heuristic: [number and name]" and rules state "every finding must map to a specific heuristic"
- [~] PARTIAL: Skill distinguishes between blocking and non-blocking issues — partially met: severity scale implicitly covers this (Critical = "cannot complete the task", Enhancement = "not blocked") but the skill never uses "blocking" / "non-blocking" terminology explicitly
- [x] PASS: Skill includes recommendations for each finding — met: finding template requires "Recommendation: [specific fix]" and rules explicitly ban vague feedback
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — met: all three fields present in frontmatter

## Output expectations results

- [x] PASS: Output evaluates the account settings area against Nielsen's 10 heuristics by name — met: heuristic coverage table names all 10; findings cite heuristics by number and name
- [x] PASS: Output's structured walkthrough traces the actual user paths from the prompt — met: walkthrough steps trace finding team members, billing, and API keys; unhappy paths noted
- [x] PASS: Output's findings each have a severity rating AND a heuristic violation cited AND a specific location — met: all eight findings carry all three fields
- [~] PARTIAL: Output's findings address the prompt's specific symptom (support contacts) — partially met: H6 and H4 violations are surfaced as Critical; however the skill gives no explicit instruction to cross-reference support-ticket signals against findings; the symptom-to-heuristic connection depends on agent inference
- [x] PASS: Output's prioritised synthesis names the top 3-5 issues — met: Top 3 Recommendations section names three issues with reasoning that addresses the support-ticket signal
- [x] PASS: Output's recommendations are concrete per finding — met: each recommendation names specific UI changes (add "Team" as named sidebar item; rename "Account" to "Settings"; add search field at top of settings sidebar)
- [x] PASS: Output distinguishes blocking from non-blocking — met: Critical findings = task failure (users contact support unable to complete task); Enhancement = user not blocked; distinction is functional through severity
- [ ] FAIL: Output addresses information architecture explicitly — not met: the simulated output includes navigation restructuring suggestions, but the skill itself has no instruction to evaluate IA as a category; this gap persists in the definition even when the output partially compensates through agent inference
- [~] PARTIAL: Output addresses search/find-as-fallback — partially met: H7 and H10 are in the heuristics table; simulated output surfaces global settings search as recommendation #3; however the skill provides no explicit instruction to consider find-as-fallback as a recovery mechanism for navigation failure

## Notes

The skill is structurally strong. The four-step mandatory process (scope, walkthrough, evaluate, synthesise) is well-sequenced. The finding template is complete. The rules section actively prevents common quality failures — vague feedback, missing locations, manufactured findings.

The main gap is information architecture. The skill identifies heuristic violations at the interaction level but does not direct the agent to step back and assess whether the navigation structure itself is the root problem. For the test prompt — users unable to find team, billing, and API keys — the root cause is IA (wrong labels, wrong grouping, wrong hierarchy), not individual interaction defects. The skill would surface H6 and H4 violations via the heuristics table, but there is no explicit prompt to produce sitemap or navigation restructuring recommendations. The simulated output compensates through agent inference, but a weaker execution would miss it.

The blocking/non-blocking distinction through severity is functional but less explicit than it could be for teams triaging findings by task-criticality. Adding "Affected user task: [job-to-be-done]" to the finding template would also strengthen traceability to product decisions.
