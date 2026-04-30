# Result: write-onboarding — technical product with configuration

**Verdict:** PASS
**Score:** 14/14 criteria met (100%)
**Evaluated:** 2026-04-30

---

## Output

Simulated output of applying the write-onboarding skill to a developer CLI tool (install via npm, configure API key, connect to GitHub, run first scan) with a 10-minute time-to-first-value target.

---

**Skill invoked:** `/user-docs-writer:write-onboarding for our CLI tool that developers install via npm, configure with an API key, connect to their GitHub repo, and run their first scan. Time-to-first-value target: under 10 minutes.`

**Step 1 — Value path (internal planning output):**

| Element | Definition |
|---|---|
| **Target user** | Developer, comfortable with npm/terminal, wants to see security vulnerabilities in their repo before pushing to CI |
| **Aha moment** | Seeing the first scan results — a list of vulnerabilities (or a clean bill of health) from their actual repo |
| **Minimum steps** | 4 steps to reach aha moment: install, configure API key, connect GitHub, run first scan |
| **Time target** | Under 10 minutes from npm install to first scan results |
| **Primary drop-off risk** | API key configuration — developers may not have the key at hand or may misconfigure the env var, causing auth failures before they see the product work |

---

**Step 2 — Welcome section:**

```markdown
## Welcome to CodeGuard

You'll connect CodeGuard to your GitHub repo and see your first vulnerability scan in under 10 minutes.

Here's what we'll do:

1. Install the CLI (< 1 min)
2. Authenticate with your API key (< 2 min)
3. Connect your GitHub repo and run your first scan (< 5 min)
```

---

**Steps 3–4 — Full onboarding document produced:**

---

```markdown
# Getting Started with CodeGuard — Developer Setup

**Time to complete:** 10 minutes
**What you'll accomplish:** Your first automated vulnerability scan of a real GitHub repo, with results in your terminal.

## Welcome to CodeGuard

You'll connect CodeGuard to your GitHub repo and see your first vulnerability scan in under 10 minutes.

Here's what we'll do:

1. Install the CLI (< 1 min)
2. Authenticate with your API key (< 2 min)
3. Connect your GitHub repo and run your first scan (< 5 min)

---

## Step 1 of 4: Install the CLI

You need the CodeGuard CLI before anything else. Requires Node.js ≥ 18.

### What to do

1. Run:

   ```bash
   npm install -g @codeguard/cli
   ```

   > **Using Yarn?** `yarn global add @codeguard/cli`

2. Verify the install:

   ```bash
   codeguard --version
   ```

### You should see

```
codeguard/2.4.1 linux-x64 node-v20.11.0
```

If you see `codeguard/x.x.x`, you're ready.

### If something's not right

- **`npm: command not found`:** Node.js is not installed. Install it at [nodejs.org](https://nodejs.org) (v18+).
- **`EACCES: permission denied`:** Run with `sudo`, or fix npm global permissions: [npm docs](https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally).
- **`codeguard: command not found` after install:** Your npm global bin is not in `$PATH`. Run `npm bin -g` and add that path to your shell profile.
- **Node version error:** Run `node --version`. If below v18, upgrade via [nvm](https://github.com/nvm-sh/nvm): `nvm install 20 && nvm use 20`.

---

## Step 2 of 4: Configure your API key

CodeGuard authenticates every request with an API key tied to your account.

### What to do

1. Get your API key from [app.codeguard.io/settings/api-keys](https://app.codeguard.io/settings/api-keys).

2. Set it as an environment variable (add to your shell profile for persistence):

   ```bash
   export CODEGUARD_API_KEY=cg_live_xxxxxxxxxxxxxxxxxxxx
   ```

3. Confirm authentication:

   ```bash
   codeguard auth status
   ```

### You should see

```
✔ Authenticated as dev@yourcompany.com
  Plan: Pro · Scans remaining this month: 498
```

### If something's not right

- **`401 Unauthorized`:** The key is wrong or expired. Copy it fresh from the dashboard — don't add quotes or trailing spaces.
- **`CODEGUARD_API_KEY is not set`:** The env var isn't in scope. Run `echo $CODEGUARD_API_KEY` to check. If empty, re-export or add it to `~/.zshrc` / `~/.bashrc` and run `source ~/.zshrc`.
- **`403 Forbidden`:** Your key exists but your plan has no scans remaining. Check your dashboard.

---

## Step 3 of 4: Connect your GitHub repo

Link your GitHub account so CodeGuard can clone and analyse your repositories.

### What to do

1. Run:

   ```bash
   codeguard github connect
   ```

2. A browser window opens to GitHub's OAuth flow. Authorise the **CodeGuard** app when prompted.

3. Return to your terminal. When prompted, enter the repo to scan, e.g., `myorg/my-repo`:

   ```bash
   ? Which repository? myorg/my-repo
   ```

### You should see

```
✔ Connected to GitHub as @yourhandle
✔ Repository myorg/my-repo linked
```

### If something's not right

- **Browser doesn't open:** Copy the URL from the terminal output and paste it into your browser manually.
- **`insufficient_scope` error on GitHub:** Your personal access token (if using PAT instead of OAuth) needs the `repo` scope. Regenerate it at GitHub → Settings → Developer settings → Personal access tokens.
- **`Repository not found`:** Confirm the repo name is `org/repo` format and that your GitHub account has read access.
- **Firewall/proxy blocking OAuth redirect:** Contact your network team or use a PAT instead: `codeguard github connect --token ghp_xxxx`.

---

## Step 4 of 4: Run your first scan

This is where CodeGuard earns its place. You'll see exactly what vulnerabilities exist in your repo right now.

### What to do

1. Run:

   ```bash
   codeguard scan myorg/my-repo
   ```

2. Wait for the scan to complete — typically 30–90 seconds for a mid-sized repo.

### You should see

```
Scanning myorg/my-repo (main)...

  Analysing 1,247 files · 38 dependencies

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SCAN RESULTS — myorg/my-repo
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Critical   2   lodash prototype pollution (CVE-2019-10744)
                 minimist RCE (CVE-2021-44906)
  High       5
  Medium    12
  Low        3

  Full report: https://app.codeguard.io/scans/abc123
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

If your repo has no issues: you'll see `✔ No vulnerabilities found`.

### If something's not right

- **`No repositories found`:** Confirm you ran Step 3 successfully. Run `codeguard github status` to check.
- **`Rate limited`:** GitHub is throttling clone requests. Wait 60 seconds and retry.
- **Scan hangs past 3 minutes:** Press `Ctrl+C`, then run `codeguard scan myorg/my-repo --verbose` to see where it stalls.
- **`0 files analysed`:** Your `.codeguardignore` may be excluding everything. Run `codeguard scan myorg/my-repo --show-config` to inspect.

---

## You're set up!

You just ran CodeGuard's full analysis pipeline against a real repo and have actual vulnerability data in front of you.

### What you just did

- Installed and authenticated the CodeGuard CLI
- Linked your GitHub account
- Ran a dependency and code scan that surfaced real vulnerabilities (or confirmed you're clean)

### What to explore next

| If you want to... | Go here |
|---|---|
| Block PRs that introduce new vulnerabilities | [CI/CD integration guide](https://docs.codeguard.io/ci) — GitHub Actions, CircleCI, and GitLab CI |
| Write custom rules for your stack | [Custom rules](https://docs.codeguard.io/rules) |
| Scan on every push automatically | [Scheduled scans](https://docs.codeguard.io/scheduled) |

---

## If you abandoned during setup

**Left at Step 2 (API key)?**

Empty state nudge (shown in dashboard): "CodeGuard isn't connected yet — add your API key in one command to start scanning."
Action: **Copy setup command**

Re-engagement (next login): "Pick up where you left off — 2 steps to your first scan."
Action: **Resume setup**

Resume path: Returns to Step 2 with API key field pre-focused.

---

**Left at Step 3 (GitHub connect)?**

Empty state nudge (shown on repo selector): "No repos connected. Link your GitHub account to scan your code in under 2 minutes."
Action: **Connect GitHub**

Re-engagement: "One step left — connect GitHub to run your first scan."
Action: **Connect now**

Resume path: Returns to GitHub OAuth flow directly.

---

Last verified: 2026-04-30
Product version: 2.4.1
```

---

**Quality checklist (from SKILL.md Step 6):**

| Check | Result |
|---|---|
| Time test | 4 steps, each under 2 min = ~8 min total. Fits 10-minute target. Pass |
| Aha moment reached | Step 4 ends with real scan output — specific CVEs and severity counts — not just a "configured" state. Pass |
| No jargon | `EACCES`, `PAT`, `OAuth scope` explained inline. Acceptable for developer audience. Pass |
| One action per step | Each step has a single primary outcome. Pass |
| Expected results present | Every step has a "You should see" section with exact terminal output. Pass |
| Escape hatches | Every step has multiple "If something's not right" entries covering the most likely failures. Pass |
| Progressive disclosure | Welcome shows 3 high-level steps; details reveal per step. Pass |
| Example inputs provided | `myorg/my-repo`, `cg_live_xxxx`, `dev@yourcompany.com` used throughout. Pass |

---

## Criteria

- [x] PASS: Each step has an expected result that confirms success before moving to the next step — met: Step 3 template mandates a "### You should see" section; simulated output includes exact terminal output for every step including verification commands
- [x] PASS: Progress indicators are present — met: output format uses "## Step N of [N]:" heading pattern throughout; simulated output shows "Step 1 of 4", "Step 2 of 4", etc.
- [x] PASS: The 10-minute time target is acknowledged and the flow is scoped to fit it — met: value path table includes "Time target" row; output header states "Time to complete: 10 minutes"; quality checklist includes time test; each step capped under 2 minutes
- [x] PASS: Error recovery is provided for the most likely failure at each step — met: Step 3 template includes a mandatory "### If something's not right" section; simulated output covers npm install fails, API key invalid, GitHub auth fails, and scan errors
- [x] PASS: The "first scan" is positioned as the activation moment with a clear payoff — met: Step 4 is the final onboarding step and ends with visible scan results including specific CVE names and severity counts
- [x] PASS: Copy is written for developers (concise, code-first, no hand-holding on terminal basics) — met: Step 1 instructs matching register to target user from the value path; simulated output skips terminal basics, leads with code blocks, uses `codeguard --version` verification rather than prose descriptions
- [x] PASS: The onboarding flow ends with a clear "what's next" that points to deeper usage — met: Step 4 mandates a "### What to explore next" table with links; simulated output points to CI/CD integration, custom rules, and scheduled scans with specific doc URLs

## Output expectations

- [x] PASS: Output's value path covers exactly the 4 steps from the prompt fitting under the 10-minute target — met: value path table identifies install, API key config, GitHub connection, and first scan; time target row states "under 10 minutes"; quality checklist time test confirms fit
- [x] PASS: Output's first-scan step is positioned as the activation moment with visible payoff — met: simulated output shows scan results with specific CVE names (CVE-2019-10744, CVE-2021-44906) and severity counts (Critical 2, High 5, Medium 12, Low 3); the result is scan data from the user's actual repo, not a "scan complete" message
- [x] PASS: Output's step expected results are concrete with verification commands — met: every step in simulated output has a "You should see" block with exact terminal output; Step 1 uses `codeguard --version`, Step 2 uses `codeguard auth status`, Steps 3 and 4 show full terminal output including auth confirmation and scan results
- [x] PASS: Output's progress indicator is shown in the docs — met: "Step N of 4:" pattern appears at every step heading in the simulated output
- [x] PASS: Output's error recovery covers the most likely failure per step — met: Step 1 covers Node version, EACCES, PATH, and version errors; Step 2 covers 401, missing env var, 403; Step 3 covers browser, PAT scope, repo not found, firewall; Step 4 covers no repos, rate limit, hang, and zero files analysed
- [x] PASS: Output's tone is developer-appropriate — met: simulated output leads with `npm install -g` without explaining what a terminal is; uses `codeguard auth status` as a verification command; error recovery references shell profile and npm global bin directly
- [x] PASS: Output's "what's next" section points to deeper usage paths with linked docs — met: simulated output points to CI/CD integration (GitHub Actions, CircleCI, GitLab CI), custom rules, and scheduled scans with explicit doc URLs

## Notes

The skill's structural mechanisms work well for this scenario. The value path table, per-step "You should see" template, mandatory escape hatches, and quality checklist combine to produce output that meets every criterion in the rubric.

One gap worth noting: the skill is audience-neutral in its writing guidance. It instructs the writer to "match the register to the target user from Step 1" but provides no developer-specific writing conventions (lead with code blocks, skip terminal basics, use verification commands over prose). The simulated output gets this right through writer judgment, not skill instruction. A developer-specific variant of the step template would make this reliable rather than incidental.
