# Write Onboarding Technical

Scenario: Testing the write-onboarding skill for a developer CLI tool where activation requires installation, API key configuration, GitHub connection, and running a first scan within a 10-minute time-to-first-value target.

## Prompt

> /user-docs-writer:write-onboarding for our CLI tool that developers install via npm, configure with an API key, connect to their GitHub repo, and run their first scan. Time-to-first-value target: under 10 minutes.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

The onboarding doc is written at `docs/getting-started.md`. Here's what it covers:

**Welcome** — 3-step preview (install+auth bundled, connect repo, scan) with a 10-minute time commitment up front.

**4 steps**, each under 2 minutes:
1. Install via npm + verify
2. Add API key
3. Connect GitHub repo via OAuth
4. Run the scan

Every step has: exact commands, example inputs, a concrete "you should see" block, and 2–3 escape hatches for the most common failure modes.

**Aha moment** — real scan output showing file-level findings with severity, so users see immediately that the tool found something specific in their code (not just a "setup complete" screen).

**Internal planning** (value path, skip/abandon recovery copy for empty states and re-engagement emails) is separated into an HTML comment block at the bottom — present for the product/copy team but not rendered for end users.

### Artifacts written

#### `work/docs/getting-started.md`

```
# Getting Started with [Product] — Developer

> **Before publishing:** Replace `[Product]` (display name), `[product]` (CLI command), `[org]` (npm org), and `app.[product].com` with your real product names and URLs. Update the API key prefix (`pk_live_`) if it differs.

**Time to complete:** Under 10 minutes
**What you'll accomplish:** Run your first scan on a real GitHub repository and see your results

---

## Welcome

You signed up to find issues in your code before they ship. In the next **10 minutes**, you'll connect [Product] to a GitHub repository and see your first scan results.

Here's what we'll do:

1. **Install and authenticate** — get the CLI set up with your API key
2. **Connect your GitHub repo** — point [Product] at the code to scan
3. **Run your first scan** — and see what it finds

---

## Step 1 of 4: Install the CLI

This installs the `[product]` command globally so you can run it from any directory.

### What to do

1. Open your terminal.
2. Run:
   ```bash
   npm install -g @[org]/[product]
   ```
3. Verify the install:
   ```bash
   [product] --version
   ```

### You should see

```
[product] v1.x.x
```

### If something's not right

- **`EACCES` permission error:** Run with `sudo`, or [fix npm permissions without sudo](https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally).
- **`command not found` after install:** Your npm global bin directory isn't on your `PATH`. Run `npm bin -g` to find it, then add that path to your shell profile.

---

## Step 2 of 4: Add your API key

Your API key authenticates your CLI with [Product]. You can rotate it any time in **Settings**.

### What to do

1. Go to `app.[product].com/settings/api-keys` and copy your API key.
2. Run:
   ```bash
   [product] auth [your-api-key]
   ```
   For example:
   ```bash
   [product] auth pk_live_abc123xyz789
   ```

### You should see

```
✓ Authenticated as you@example.com
```

### If something's not right

- **`Invalid key` error:** Make sure you copied the full key — keys start with `pk_live_`. Keys from the **Test** tab won't work here; use **Live**.
- **Key not showing in Settings:** Your account may still be pending verification. Check your inbox for a confirmation email and click the link first.

---

## Step 3 of 4: Connect your GitHub repo

[Product] needs read access to your repository to scan it. You'll pick exactly which repo — nothing else is shared.

### What to do

1. Run:
   ```bash
   [product] connect github
   ```
2. Your browser opens to GitHub. Click **Authorize [Product]** to grant read access.
3. Back in your terminal, select the repository to scan:
   ```bash
   ? Which repository? (Use arrow keys)
   ❯ your-org/your-repo
     your-org/another-repo
   ```
   Pick a repo with some real code in it — the more code, the more interesting your first scan.

### You should see

```
✓ Connected to your-org/your-repo (default branch: main)
```

### If something's not right

- **Browser didn't open:** Copy the URL printed in the terminal and open it manually.
- **Repository not listed:** You may not have admin access to it. Ask a repo admin to install the [Product] GitHub App, or connect a repo you own.
- **Auth loop / page keeps refreshing:** Clear cookies for github.com and try again.

---

## Step 4 of 4: Run your first scan

Scan the repository you just connected.

### What to do

1. Run:
   ```bash
   [product] scan
   ```
   This scans the default branch. To scan a specific branch:
   ```bash
   [product] scan --branch feature/my-branch
   ```

### You should see

A progress bar, then your results:

```
Scanning your-org/your-repo (main) ...

✓ Scan complete — 142 files analysed in 38s

  3 issues found

  HIGH    src/auth/login.js:47     Hardcoded secret key
  MEDIUM  src/api/users.js:112     SQL query built with string concatenation
  LOW     src/utils/fetch.js:23    Unhandled promise rejection

Run `[product] report` to export full details.
```

If your repo is clean, you'll see:

```
✓ Scan complete — 0 issues found
```

That's a result too — a clean pass is worth knowing.

### If something's not right

- **`No repository connected` error:** Run `[product] connect github` first (Step 3).
- **Scan hangs for more than 3 minutes:** Your repo may be very large. Run `[product] scan --timeout 600` to extend the limit.
- **`403 Forbidden` mid-scan:** Your GitHub token may have expired. Run `[product] connect github` again to refresh it.

---

## You're set up!

You just scanned a real repository and got your first results from [Product].

### What you just did

- Installed the [Product] CLI and authenticated your account
- Granted [Product] read-only access to a specific GitHub repository
- Ran a full scan and saw real findings (or confirmed the code is clean)

### What to explore next

| If you want to... | Go here |
|---|---|
| Scan on every pull request automatically | [CI/CD integration guide →](#) |
| Export results to share with your team | Run `[product] report --format html` or `--format json` |
| Scan a different branch or repo | Run `[product] scan --branch <name>` or `[product] connect github` |

---

*Last verified: 2026-05-01*
*Product version: v1.x.x*

---

<!--
## For the product / copy team

### Value path (internal planning reference)

| Element | Definition |
|---|---|
| **Target user** | Software developer, comfortable with npm and the terminal, has an existing GitHub repo, signed up wanting to find issues in their codebase |
| **Aha moment** | Seeing real scan results — actual findings or a clean pass — on their own code |
| **Minimum steps** | 4 steps: install → add API key → connect repo → run scan |
| **Time target** | Under 10 minutes from signup to first results |
| **Primary drop-off risk** | API key configuration (user doesn't know where to find it) and GitHub auth scope errors |

### Skip / abandon recovery copy

These are surface-level nudges for empty states and re-engagement emails. They are not part of the onboarding doc itself.

#### Skipped: API key (Step 2)

**Empty-state nudge** (shown when user runs any command without authenticating):
You haven't added your API key yet. Without it, [Product] can't run scans. [Add your key now →](https://app.[product].com/settings/api-keys)

**Re-engagement notification:**
Pick up where you left off — 3 steps to your first scan result. [Resume setup →](https://app.[product].com/onboarding)

**Resume path:** Returns to Step 2 with install already marked complete.

---

#### Skipped: GitHub connection (Step 3)

**Empty-state nudge** (shown when user runs `[product] scan` without a connected repo):
No repository connected. Connect a GitHub repo in 30 seconds and run your first scan.

```bash
[product] connect github
```

**Re-engagement notification:**
You're one step away from your first scan. Connect your GitHub repo to continue. [Resume setup →](https://app.[product].com/onboarding)

**Resume path:** Returns to Step 3 with install and auth already marked complete.

---

#### Abandoned mid-scan (Step 4)

**Empty-state nudge** (shown in dashboard after incomplete scan):
Your last scan didn't finish. Run it again — scans typically complete in under a minute.

```bash
[product] scan
```

**Re-engagement notification:**
Your scan of `your-org/your-repo` didn't complete. [Run it now →](https://app.[product].com/onboarding)

**Resume path:** Returns to Step 4 with repo already connected and ready to scan.
-->

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 13.0/14.0 (93%) |
| Evaluated | 2026-05-01 |
| Target duration | 219743 ms |
| Target cost | $0.5388 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Each step has an expected result that confirms success before moving to the next step | PASS | Every step contains a '### You should see' block: Step 1 shows '[product] v1.x.x', Step 2 shows '✓ Authenticated as you@example.com', Step 3 shows '✓ Connected to your-org/your-repo (default branch: main)', Step 4 shows the full scan output with findings. |
| c2 | Progress indicators are present — the user knows where they are in the flow (e.g., "Step 2 of 4") | PASS | All four headings use the explicit format: '## Step 1 of 4: Install the CLI', '## Step 2 of 4: Add your API key', '## Step 3 of 4: Connect your GitHub repo', '## Step 4 of 4: Run your first scan'. |
| c3 | The 10-minute time target is acknowledged and the flow is scoped to fit it | PASS | Top of doc states '**Time to complete:** Under 10 minutes'; Welcome section opens with 'In the next **10 minutes**, you'll connect [Product] to a GitHub repository and see your first scan results.' Chat response also notes 'each under 2 minutes'. |
| c4 | Error recovery is provided for the most likely failure at each step (npm install fails, API key invalid, GitHub auth fails) | PASS | Each step has an '### If something's not right' section: Step 1 covers EACCES and command-not-found; Step 2 covers 'Invalid key' and unverified account; Step 3 covers browser not opening, repo not listed, and auth loop; Step 4 covers no repo connected, scan hang, and 403 Forbidden. |
| c5 | The "first scan" is positioned as the activation moment with a clear payoff | PASS | Step 4 shows actual scan output with '3 issues found' and specific file-level findings (HIGH: src/auth/login.js:47 Hardcoded secret key, etc.). Chat response explicitly calls this the 'Aha moment — real scan output showing file-level findings with severity, so users see immediately that the tool found something specific in their code'. |
| c6 | Copy is written for developers (concise, code-first, no hand-holding on terminal basics) | PASS | Commands are given directly in fenced code blocks with minimal prose. Explanations like 'This installs the `[product]` command globally so you can run it from any directory' are single-line context, not walkthroughs. Error recovery uses terminal commands, not UI navigation descriptions. |
| c7 | The onboarding flow ends with a clear "what's next" that points to deeper usage, not just "you're done" | PASS | '## What to explore next' table with three rows: CI/CD integration (linked), exporting results with `[product] report --format html/json`, and scanning different branches/repos with specific commands. |
| c8 | Output's value path covers exactly the 4 steps from the prompt — npm install, API key configuration, GitHub connection, run first scan — fitting under the 10-minute time-to-first-value target | PASS | All four steps are present in sequence: Step 1 (npm install -g @[org]/[product]), Step 2 (API key via [product] auth), Step 3 ([product] connect github), Step 4 ([product] scan). 'Time to complete: Under 10 minutes' stated at the top. |
| c9 | Output's first-scan step is positioned as the activation moment — with the visible payoff being scan results displayed (vulnerabilities found, dependency tree, or whatever the CLI outputs) — NOT just "scan complete" | PASS | Step 4's 'You should see' block shows '3 issues found' with three specific findings including file path, line number, and severity (HIGH: src/auth/login.js:47 Hardcoded secret key; MEDIUM: src/api/users.js:112 SQL query; LOW: src/utils/fetch.js:23 Unhandled promise rejection). |
| c10 | Output's step expected results are concrete — Step 1: "after `npm install`, run `mycli --version` and you should see `v1.2.3`"; Step 2: "after setting API key, run `mycli auth status` and you should see `Authenticated as <your email>`" — every step has a verification command | PASS | Step 1: verify with `[product] --version` → '[product] v1.x.x'. Step 2: `[product] auth pk_live_abc123xyz789` → '✓ Authenticated as you@example.com'. Step 3: connect command → '✓ Connected to your-org/your-repo'. Step 4: `[product] scan` → full results block. All concrete and verifiable. |
| c11 | Output's progress indicator is shown in the docs — "Step 2 of 4: Configure your API key" or visual progress dots — so the user knows how far along they are | PASS | H2 headings use '## Step 1 of 4: Install the CLI', '## Step 2 of 4: Add your API key', '## Step 3 of 4: Connect your GitHub repo', '## Step 4 of 4: Run your first scan' throughout the document. |
| c12 | Output's error recovery covers the most likely failure per step — npm install fails (Node version mismatch, npm registry, permissions), API key invalid (typo, expired key, wrong env var), GitHub auth fails (PAT scope insufficient, network), first scan errors (no repos found, ratelimited) | PARTIAL | Step 1 covers permissions (EACCES) and PATH issues but omits Node version mismatch and npm registry failures. Step 2 covers typo/wrong key but omits expired key and wrong env var. Step 3 covers browser not opening, repo permissions, and auth loop but omits PAT scope and network failures explicitly. Step 4 covers missing repo connection, timeout, and 403 but omits rate limiting. Coverage is solid but several criterion-specified scenarios are absent. |
| c13 | Output's tone is developer-appropriate — concise, code-first, assumes terminal fluency; e.g. "run `mycli init` in your repo root" not "open your terminal application then type the following command" | PASS | Commands are given in fenced blocks with brief context. 'Open your terminal' is the only minor over-explanation (Step 1), but overall copy assumes fluency: error recovery gives commands directly ('Run npm bin -g to find it'), step instructions say 'Run:' not 'type the following into your terminal application'. |
| c14 | Output's "what's next" section points to deeper usage paths — "Set up scheduled scans in CI", "Configure custom rules", "Integrate with your CI/CD pipeline" — with linked docs, not just "explore the docs" | PARTIAL | 'What to explore next' table has three specific paths: CI/CD integration with a link ([CI/CD integration guide →](#) — but the link is a placeholder #), and two entries that provide commands rather than linked docs. No 'Configure custom rules' path. The structure is better than 'explore the docs' but links are placeholders rather than real doc URLs. |

### Notes

The output is a strong, well-structured onboarding doc that hits almost all criteria cleanly. Step-by-step progress labels, concrete 'You should see' blocks, and a realistic scan result payoff are particular strengths. The two partial scores reflect genuine gaps: error recovery misses several criterion-specified failure modes (Node version mismatch, npm registry, env var, PAT scope, network, ratelimited), and the 'what's next' section uses a placeholder link (#) rather than real documentation URLs, with only one of three paths being link-backed. These are minor omissions in an otherwise developer-appropriate, 10-minute-scoped doc.
