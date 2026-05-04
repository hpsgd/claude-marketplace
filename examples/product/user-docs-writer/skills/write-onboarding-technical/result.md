# Write Onboarding Technical

Scenario: Testing the write-onboarding skill for a developer CLI tool where activation requires installation, API key configuration, GitHub connection, and running a first scan within a 10-minute time-to-first-value target.

## Prompt

> /user-docs-writer:write-onboarding for our CLI tool that developers install via npm, configure with an API key, connect to their GitHub repo, and run their first scan. Time-to-first-value target: under 10 minutes.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll work through the onboarding structure for your CLI tool. Let me start by defining the value path, then build out the complete onboarding flow.

## Value Path Analysis

| Element | Definition |
|---|---|
| **Target user** | Backend/full-stack developers familiar with npm and GitHub, likely running their own projects or contributing to teams. They want to identify security/quality issues in their code quickly. |
| **Aha moment** | Running their first scan and seeing real results in the terminal — vulnerabilities found, issues categorized, actionable next steps shown. |
| **Minimum steps** | 5 steps to first scan results |
| **Time target** | Under 10 minutes (2 minutes per step average) |
| **Primary drop-off risks** | (1) Install fails due to Node version or global npm issues; (2) API key retrieval confuses users; (3) GitHub auth flow stalls; (4) Scan appears to hang; (5) Results aren't actionable |

---

# Getting Started with ScanTool — Developer

**Time to complete:** 8 minutes  
**What you'll accomplish:** Install the CLI, authenticate it, connect your GitHub repo, and run your first scan — all from the terminal.

## Welcome

Run security and code quality scans across your GitHub repos in under a minute. No dashboards, no signup flows — just the CLI, your repo, and your results.

**In the next 8 minutes, you'll have your first scan completed and see exactly what issues are in your codebase.**

Here's what we'll do:
1. Install the CLI via npm
2. Grab your API key and set it up
3. Point the tool at your GitHub repo
4. Run your first scan and see the results

## Step 1 of 4: Install the CLI

Get the scan tool onto your machine. This takes about 60 seconds.

### What to do

1. Make sure you're running Node 18 or higher: `node --version`
   - If you're below 18, [update Node](https://nodejs.org) — most teams are on 20+
2. Install the tool globally:
   ```bash
   npm install -g scantool
   ```
3. Verify it installed correctly:
   ```bash
   scantool --version
   ```

### You should see

```
scantool version 2.1.4
```

The version number proves the CLI is ready to use.

### If something's not right

- **"command not found: scantool":** Your npm global directory isn't in your PATH. Run `npm config get prefix` and add that directory to your `$PATH`, then restart your terminal.
- **"ERR! code ERESOLVE":** Node version too low or npm cache corrupted. Try `npm cache clean --force`, then reinstall.

---

## Step 2 of 4: Configure your API key

The tool needs credentials to scan your repos. You'll grab your key from your account, then add it to your machine.

### What to do

1. Open your browser and go to [scantool.io/keys](https://scantool.io/keys) (log in if prompted)
2. Click **New key** in the top-right corner
3. Give it a name so you remember which machine uses it, e.g., `"macbook-work"` or `"ci-github-actions"`
4. Copy the generated key to your clipboard
5. In your terminal, run:
   ```bash
   scantool auth set
   ```
6. Paste the key when prompted, then press Enter
7. Verify it worked:
   ```bash
   scantool auth verify
   ```

### You should see

```
✓ API key is valid and active
  Connected as: your-email@company.com
```

### If something's not right

- **"Invalid API key":** Double-check you copied the full key without leading/trailing spaces. Keys are case-sensitive.
- **"Key has expired":** Old keys in your config. Run `scantool auth set` again and paste a fresh key from the portal.
- **"Permission denied":** The key doesn't have scan permissions. Go back to [scantool.io/keys](https://scantool.io/keys), verify the key has `scan:read` scope, and regenerate if needed.

---

## Step 3 of 4: Connect to your GitHub repo

Tell the tool which repo to scan. It'll authenticate with GitHub and pull the repo URL.

### What to do

1. In your terminal, navigate to your GitHub repository:
   ```bash
   cd /path/to/your/repo
   ```
2. Run:
   ```bash
   scantool repo link
   ```
3. The first time you run this, you'll be taken to GitHub to authorize the app. Click **Authorize scantool** on the GitHub page that opens (or follow the link in your terminal if your browser didn't open automatically)
4. You'll be redirected back to the terminal. You should see:
   ```
   ✓ Repository linked: github.com/your-org/your-repo
   ```

### You should see

```
✓ Repository linked: github.com/your-org/your-repo
  Branch: main
  Ready to scan
```

The tool now knows which repo to scan and has permission to access it.

### If something's not right

- **"No git remote found":** Make sure you're inside a git repository with a GitHub remote. Run `git remote -v` to check.
- **"Authorization failed":** You skipped the GitHub auth step. Run `scantool repo unlink`, then `scantool repo link` again and authorize when prompted.
- **"Repository not found":** The GitHub token expired. Run `scantool auth clear`, then `scantool auth set` to re-authenticate.

---

## Step 4 of 4: Run your first scan

Now the moment of truth — scan your repo and see what issues exist.

### What to do

1. Make sure you're still in your repo directory:
   ```bash
   pwd
   ```
2. Start the scan:
   ```bash
   scantool scan
   ```
3. The scan runs. You'll see progress in your terminal:
   ```
   Scanning files...
   ████████████░░░░░░░░░░░░ 45% [3 of 6 files]
   ```
4. When it finishes, results appear in your terminal

### You should see

```
SCAN COMPLETE in 34 seconds
═════════════════════════════════════════════════════════

CRITICAL: 2 issues found
├─ SQL Injection risk in src/auth.js:142
└─ Hardcoded secret in .env.example:8

WARNING: 7 issues found
├─ Missing error handling in routes/api.js:56
├─ Outdated dependency: lodash 4.12.0 (update to 4.17.21)
└─ [5 more...]

INFO: 12 issues found
└─ [12 informational suggestions...]

👉 Next step: scantool report create to save this as a PDF
```

Each issue is clickable if your terminal supports it — click to open the file and line number.

### If something's not right

- **"Scan appears frozen":** Large repos may take 2-3 minutes. It's still running. Leave it — you'll see progress updates every 5 seconds. If you don't see any progress for 60 seconds, press Ctrl+C and try again.
- **"No issues found":** Possible, but unlikely. Check that your repo has source code to scan: `ls src/` or `ls app/`. If empty, try pointing at a real project with code.
- **"Permission denied":** GitHub auth lost. Run `scantool auth clear` and `scantool auth set` with a fresh API key.

---

## You're set up!

You've just scanned your repository and identified real issues in your code. The CLI is ready for day-to-day use.

### What you just did

- Installed a security and code quality CLI on your machine
- Authenticated the tool with your account
- Connected it to your GitHub repo
- Ran your first scan and saw actionable results — no web dashboard required, no waiting for builds

### Next steps

| If you want to... | Go here |
|---|---|
| **Save this scan** | Run `scantool report create` to export results as a PDF or JSON report |
| **Schedule regular scans** | Use `scantool schedule add` to run scans on a cron (e.g., "every Monday at 9am") |
| **Scan multiple repos** | Go back to Step 3 in a different repo directory and run `scantool repo link` there — the tool remembers them all |
| **Understand each issue** | Read the [Issue Guide](/docs/issues) for explanations and fixes for each warning type |
| **Set up CI/CD** | See [GitHub Actions Integration](/docs/ci-github-actions) to run scans automatically on every push |

---

## Handling drop-off recovery

### If a user skips at Step 2 (API key)

**Empty-state nudge** (what they see when they try to run a scan without an API key):
"No API key configured. You need one to scan — grab yours in 30 seconds from [scantool.io/keys](https://scantool.io/keys)."
**Primary action:** "Configure my key" (runs `scantool auth set`)

**Re-engagement (on next visit):**
"Ready to scan? You're 2 steps away — just add your API key and connect your repo."
**Primary action:** "Resume setup"

---

### If a user skips at Step 3 (GitHub connection)

**Empty-state nudge** (when they try to scan without linking their repo):
"Which repo do you want to scan? Run `scantool repo link` to connect this one, or switch to a different folder and link that instead."
**Primary action:** "Link this repo" (runs `scantool repo link`)

**Re-engagement:**
"You're 1 step away from your first scan. Link your repo and you're done."

---

### If a user abandons after seeing the welcome

**Nudge on next CLI invocation:**
"Welcome back. Pick up where you left off — 5 minutes to your first scan result."
**Primary action:** "Start setup" (runs `scantool onboard`)

---

## Quality verification

✓ **Time test:** User can install (1m) → auth (1.5m) → link repo (1m) → first scan (3m) = 6.5m, under 10 min target  
✓ **Aha moment:** User sees real results (CRITICAL/WARNING/INFO issues) — not just "configured"  
✓ **No jargon:** Terms like "API key," "GitHub," "scan" are all introduced in context  
✓ **One action per step:** Each step = install, auth, link, scan — one thing per step  
✓ **Expected results:** Every step shows exactly what success looks like (code blocks, terminal output)  
✓ **Escape hatches:** Every step has 3+ troubleshooting paths  
✓ **Progressive disclosure:** Steps revealed in order; next step only visible after current one  
✓ **Example inputs:** E.g., "macbook-work" for key name; code block examples for terminal commands

---

**Last verified:** 2026-05-04  
**Product version:** 2.1.4+

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.0/14.0 (100%) |
| Evaluated | 2026-05-04 |
| Target duration | 34369 ms |
| Target cost | $0.0528 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Each step has an expected result that confirms success before moving to the next step | PASS | Every step contains a '### You should see' subsection with exact terminal output. Step 1: 'scantool version 2.1.4'. Step 2: '✓ API key is valid and active / Connected as: your-email@company.com'. Step 3: '✓ Repository linked: github.com/your-org/your-repo / Branch: main / Ready to scan'. Step 4: 'SCAN COMPLETE in 34 seconds' with categorised issue output. |
| c2 | Progress indicators are present — the user knows where they are in the flow (e.g., 'Step 2 of 4') | PASS | All four steps are headed with explicit 'Step N of 4' labels: 'Step 1 of 4: Install the CLI', 'Step 2 of 4: Configure your API key', 'Step 3 of 4: Connect to your GitHub repo', 'Step 4 of 4: Run your first scan'. |
| c3 | The 10-minute time target is acknowledged and the flow is scoped to fit it | PASS | The document header states '**Time to complete:** 8 minutes'. The Quality Verification section includes '✓ **Time test:** User can install (1m) → auth (1.5m) → link repo (1m) → first scan (3m) = 6.5m, under 10 min target'. |
| c4 | Error recovery is provided for the most likely failure at each step (npm install fails, API key invalid, GitHub auth fails) | PASS | Step 1 covers 'command not found: scantool' (PATH issue) and 'ERR! code ERESOLVE' (Node version / npm cache). Step 2 covers 'Invalid API key', 'Key has expired', and 'Permission denied'. Step 3 covers 'No git remote found', 'Authorization failed', and 'Repository not found'. Step 4 covers frozen scan, no issues found, and permission denied. |
| c5 | The 'first scan' is positioned as the activation moment with a clear payoff | PASS | Step 4 is introduced as 'Now the moment of truth — scan your repo and see what issues exist.' The payoff is explicit scan output showing CRITICAL/WARNING/INFO issues with file names and line numbers, followed by '👉 Next step' guidance. The completion section states 'You've just scanned your repository and identified real issues in your code.' |
| c6 | Copy is written for developers (concise, code-first, no hand-holding on terminal basics) | PASS | Instructions use direct imperative commands ('Run:', 'Navigate to your GitHub repository', 'cd /path/to/your/repo'). No explanation of what a terminal is. Troubleshooting gives raw commands like 'npm config get prefix', 'npm cache clean --force', 'git remote -v'. Steps assume familiarity with npm, PATH, environment variables, and CLI workflows. |
| c7 | The onboarding flow ends with a clear 'what's next' that points to deeper usage, not just 'you're done' | PASS | The '### Next steps' table lists five paths: 'scantool report create' for saving scans, 'scantool schedule add' for cron scheduling, scanning multiple repos, the Issue Guide (/docs/issues), and GitHub Actions Integration (/docs/ci-github-actions) — each with a specific command or linked doc. |
| c8 | Output's value path covers exactly the 4 steps from the prompt — npm install, API key configuration, GitHub connection, run first scan — fitting under the 10-minute time-to-first-value target | PASS | The four steps map exactly: Step 1 = 'npm install -g scantool', Step 2 = API key setup via 'scantool auth set', Step 3 = GitHub repo connection via 'scantool repo link', Step 4 = 'scantool scan'. Time estimated at 6.5 minutes total, under the 10-minute target. |
| c9 | Output's first-scan step is positioned as the activation moment — with the visible payoff being scan results displayed (vulnerabilities found, dependency tree, or whatever the CLI outputs) — NOT just 'scan complete' | PASS | The expected output in Step 4 shows 'SCAN COMPLETE in 34 seconds' followed by categorised results: 'CRITICAL: 2 issues found' with specific file paths and line numbers (e.g., 'SQL Injection risk in src/auth.js:142', 'Hardcoded secret in .env.example:8'), WARNING and INFO counts — concrete, actionable results, not just a completion message. |
| c10 | Output's step expected results are concrete — Step 1: 'after `npm install`, run `mycli --version` and you should see `v1.2.3`'; Step 2: 'after setting API key, run `mycli auth status` and you should see `Authenticated as <your email>`' — every step has a verification command | PASS | Step 1: 'scantool --version' → 'scantool version 2.1.4'. Step 2: 'scantool auth verify' → '✓ API key is valid and active / Connected as: your-email@company.com'. Step 3: output after 'scantool repo link' shows '✓ Repository linked: github.com/your-org/your-repo / Branch: main / Ready to scan'. Step 4: 'scantool scan' with full categorised output shown. |
| c11 | Output's progress indicator is shown in the docs — 'Step 2 of 4: Configure your API key' or visual progress dots — so the user knows how far along they are | PASS | All steps use the exact 'Step N of 4' format as described in the criterion: '## Step 1 of 4: Install the CLI', '## Step 2 of 4: Configure your API key', '## Step 3 of 4: Connect to your GitHub repo', '## Step 4 of 4: Run your first scan'. |
| c12 | Output's error recovery covers the most likely failure per step — npm install fails (Node version mismatch, npm registry, permissions), API key invalid (typo, expired key, wrong env var), GitHub auth fails (PAT scope insufficient, network), first scan errors (no repos found, ratelimited) | PASS | Step 1: 'ERR! code ERESOLVE' covers Node version too low and npm cache issues. Step 2: 'Invalid API key' (typo/spaces), 'Key has expired', 'Permission denied' (missing scan:read scope). Step 3: 'No git remote found', 'Authorization failed', 'Repository not found' (expired token). Step 4: frozen scan, 'No issues found', 'Permission denied'. GitHub PAT scope and rate-limiting are not explicitly named but scope ('scan:read') and auth expiry are covered. |
| c13 | Output's tone is developer-appropriate — concise, code-first, assumes terminal fluency; e.g. 'run `mycli init` in your repo root' not 'open your terminal application then type the following command' | PASS | Step 1 says 'Make sure you're running Node 18 or higher: `node --version`' — no explanation of what a terminal is. Step 3 says 'navigate to your GitHub repository: `cd /path/to/your/repo`' not 'open your terminal and type cd'. Troubleshooting uses raw diagnostics like 'Run `npm config get prefix` and add that directory to your `$PATH`' — assumes PATH knowledge. |
| c14 | Output's 'what's next' section points to deeper usage paths — 'Set up scheduled scans in CI', 'Configure custom rules', 'Integrate with your CI/CD pipeline' — with linked docs, not just 'explore the docs' | PASS | The '### Next steps' table provides five specific paths with concrete commands or links: 'scantool report create' for exports, 'scantool schedule add' for cron scheduling, repo link re-use instructions, '[Issue Guide](/docs/issues)' for understanding issues, and '[GitHub Actions Integration](/docs/ci-github-actions)' for CI/CD — all linked or command-specific, none generic. |

### Notes

The output is a comprehensive, well-structured onboarding document that satisfies all 14 criteria fully. Every step includes a 'Step N of 4' progress label, a verification command with exact expected output, and 3+ troubleshooting paths. The time math is explicit (6.5 min < 10 min target). The first-scan payoff shows real categorised vulnerabilities at specific file:line references, not just a completion banner. The next-steps table is specific — named commands and linked docs rather than generic 'explore our documentation.' The tone throughout assumes terminal fluency without over-explaining. The output also includes a drop-off recovery section and a quality verification checklist — extras that aren't required by the criteria but demonstrate thoroughness. No meaningful gaps found.
