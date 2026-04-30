# Result: Write integration guide

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 14 / 14 criteria met (100%) |
| **Evaluated** | 2026-04-30 |

## Output

Simulated output for the prompt: `/developer-docs-writer:write-integration-guide for connecting Clearpath to Salesforce — syncing deal status from Salesforce opportunities to Clearpath projects automatically.`

---

# Integrating Clearpath with Salesforce

By the end of this guide, you will have a working integration that automatically syncs deal status from Salesforce Opportunities to Clearpath Projects whenever an Opportunity stage changes.

## What you'll build

When a Salesforce Opportunity moves to a new stage (e.g. "Closed Won"), a webhook fires to your integration service. That service reads the new stage, maps it to a Clearpath project status, and updates the corresponding Clearpath project via the Clearpath REST API. No manual status updates required.

## Prerequisites

- [ ] Salesforce org with API access enabled — confirm at **Setup > Company Settings > My Domain**, look for "API Enabled" checkbox
- [ ] Salesforce Connected App with OAuth 2.0 — create one at **Setup > App Manager > New Connected App**; note the `client_id` and `client_secret`
- [ ] Salesforce admin profile or a profile with "Modify All Data" and "API Enabled" permissions — check at **Setup > Profiles**
- [ ] Clearpath account with Admin role — confirm at **Settings > Team > Your Role**
- [ ] Clearpath API key — generate one at **Settings > Integrations > API Keys > Create Key** (takes < 1 minute)
- [ ] Node.js >= 18.0.0 — install: `nvm install 18 && nvm use 18`
- [ ] `npm` >= 9.0.0 (bundled with Node 18)

---

## Step 1: Create the Salesforce Connected App

A Connected App gives your integration an OAuth identity to call the Salesforce API.

1. In Salesforce, go to **Setup > App Manager > New Connected App**.
2. Fill in the name (`Clearpath Sync`), contact email, and enable OAuth.
3. Add the scope `api` and `refresh_token`.
4. Set the callback URL to `https://login.salesforce.com/services/oauth2/success` for now.
5. Save and wait 2–10 minutes for propagation.

**Expected result:**

```
Connected App "Clearpath Sync" created.
Consumer Key: 3MVG9...
Consumer Secret: 1234567890ABCDEF
```

Note both values — they are your `SALESFORCE_CLIENT_ID` and `SALESFORCE_CLIENT_SECRET`.

---

## Step 2: Obtain a Salesforce access token

Exchange your credentials for a token the integration service will use on each API call.

```bash
curl -X POST https://login.salesforce.com/services/oauth2/token \
  -d "grant_type=password" \
  -d "client_id=$SALESFORCE_CLIENT_ID" \
  -d "client_secret=$SALESFORCE_CLIENT_SECRET" \
  -d "username=$SALESFORCE_USERNAME" \
  -d "password=$SALESFORCE_PASSWORD$SALESFORCE_SECURITY_TOKEN"
```

**What this does:** The `password` grant exchanges static credentials for a bearer token. `SALESFORCE_SECURITY_TOKEN` is the IP-allowlist bypass token from **Setup > My Personal Information > Reset My Security Token**.

**Expected result:**

```json
{
  "access_token": "00D5g000004xK7p!ARQAQMk_example_token",
  "instance_url": "https://yourorg.my.salesforce.com",
  "token_type": "Bearer"
}
```

Set `SALESFORCE_INSTANCE_URL` to the returned `instance_url`.

---

## Step 3: Set up the integration service

Install dependencies and configure environment variables.

```bash
mkdir clearpath-salesforce-sync && cd clearpath-salesforce-sync
npm init -y
npm install express axios dotenv
```

Create `.env`:

```bash
# Salesforce — from Setup > App Manager > Clearpath Sync
SALESFORCE_CLIENT_ID=3MVG9_your_client_id
SALESFORCE_CLIENT_SECRET=1234567890ABCDEF
SALESFORCE_USERNAME=admin@yourorg.com
SALESFORCE_PASSWORD=YourPassword
SALESFORCE_SECURITY_TOKEN=AbCdEfGhIj1234
SALESFORCE_INSTANCE_URL=https://yourorg.my.salesforce.com

# Clearpath — from Settings > Integrations > API Keys
CLEARPATH_API_KEY=cp_live_abc123xyz789
CLEARPATH_BASE_URL=https://api.clearpath.io/v1
```

**Expected result:**

```
added 3 packages in 1.8s
```

No errors. The `.env` file exists in the project root.

---

## Step 4: Write the sync handler

Create `src/sync.js`:

```js
require('dotenv').config();
const axios = require('axios');

const STAGE_TO_STATUS = {
  'Prospecting':    'backlog',
  'Qualification':  'in-progress',
  'Proposal':       'in-progress',
  'Negotiation':    'review',
  'Closed Won':     'complete',
  'Closed Lost':    'cancelled',
};

async function syncOpportunityToProject(opportunityId) {
  // 1. Fetch Opportunity from Salesforce
  const sfRes = await axios.get(
    `${process.env.SALESFORCE_INSTANCE_URL}/services/data/v59.0/sobjects/Opportunity/${opportunityId}`,
    { headers: { Authorization: `Bearer ${process.env.SF_ACCESS_TOKEN}` } }
  );
  const { Name, StageName, Clearpath_Project_ID__c } = sfRes.data;

  if (!Clearpath_Project_ID__c) {
    console.warn(`Opportunity ${opportunityId} has no linked Clearpath project — skipping`);
    return;
  }

  const newStatus = STAGE_TO_STATUS[StageName] ?? 'in-progress';

  // 2. Update Clearpath project status
  await axios.patch(
    `${process.env.CLEARPATH_BASE_URL}/projects/${Clearpath_Project_ID__c}`,
    { status: newStatus },
    { headers: { 'X-API-Key': process.env.CLEARPATH_API_KEY } }
  );

  console.log(`Synced: Opportunity "${Name}" (${StageName}) → Clearpath project ${Clearpath_Project_ID__c} (${newStatus})`);
}

module.exports = { syncOpportunityToProject };
```

**What this does:** `STAGE_TO_STATUS` maps Salesforce stage names to Clearpath status values. The custom field `Clearpath_Project_ID__c` on the Opportunity links the two records — your Salesforce admin must create this field if it doesn't exist.

**Expected result:** No output yet — this is a module. Continue to Step 5 to wire it up.

---

## Step 5: Write the webhook receiver

Create `src/server.js`:

```js
require('dotenv').config();
const express = require('express');
const { syncOpportunityToProject } = require('./sync');

const app = express();
app.use(express.json());

app.post('/webhook/salesforce', async (req, res) => {
  const { opportunityId } = req.body;
  if (!opportunityId) return res.status(400).json({ error: 'opportunityId required' });

  try {
    await syncOpportunityToProject(opportunityId);
    res.json({ ok: true });
  } catch (err) {
    console.error('Sync failed:', err.response?.data ?? err.message);
    res.status(500).json({ error: 'sync failed' });
  }
});

app.listen(3000, () => console.log('Webhook receiver listening on :3000'));
```

**Expected result:**

```
Webhook receiver listening on :3000
```

---

## Complete example

Here's the full integration in one place. Copy the two files above (`src/sync.js` and `src/server.js`) and the `.env` template, then run:

**Run it:**

```bash
node src/server.js &

# Simulate a Salesforce webhook firing for opportunity 006Qk000003xABC
curl -X POST http://localhost:3000/webhook/salesforce \
  -H "Content-Type: application/json" \
  -d '{"opportunityId": "006Qk000003xABCIAM"}'
```

**Expected result:**

```
Synced: Opportunity "Acme Corp Renewal" (Closed Won) → Clearpath project proj_9f2e1a3b (complete)
{"ok":true}
```

---

## Verifying the integration

1. In Salesforce, open a test Opportunity that has `Clearpath_Project_ID__c` populated.
2. Change the **Stage** field to `Closed Won` and save.
3. Your Salesforce Outbound Message (or Process Builder trigger) fires the webhook to your service.
4. Open the Clearpath project at **Projects > [Project Name] > Details**.
5. Confirm the **Status** field reads `complete` within 30 seconds.
6. If the status did not update, check your service logs: look for `Sync failed:` followed by an HTTP status and Clearpath API error message.

---

## Troubleshooting

### `INVALID_SESSION_ID` from Salesforce API
**Cause:** The `SF_ACCESS_TOKEN` has expired. Password-grant tokens expire after the org's session timeout (default 2 hours).
**Fix:** Re-run the token exchange in Step 2 and update `SF_ACCESS_TOKEN` in your environment. For production, implement the OAuth refresh token flow.

### `Clearpath_Project_ID__c` not found on Opportunity
**Cause:** The custom field doesn't exist in your Salesforce org.
**Fix:** Go to **Setup > Object Manager > Opportunity > Fields & Relationships > New**. Create a Text field named `Clearpath Project ID` with API name `Clearpath_Project_ID__c`. Populate it on your test Opportunity.

### Webhook fires but Clearpath returns `404 Not Found`
**Cause:** The `Clearpath_Project_ID__c` value on the Opportunity doesn't match any project in Clearpath, or the project has been deleted.
**Fix:** Verify the project ID by calling `GET /v1/projects` with your Clearpath API key and checking the list. Update the Opportunity field with the correct ID.

### Clearpath returns `429 Too Many Requests`
**Cause:** Clearpath's default rate limit is 100 requests/minute per API key. A bulk Opportunity stage update can exceed this.
**Fix:** Add exponential backoff before the `axios.patch` call. Process updates via a queue (e.g. BullMQ) rather than in-process, and delay retries by 2^attempt seconds.

### Salesforce Outbound Message shows `Pending` and never delivers
**Cause:** Your webhook URL is unreachable from Salesforce's servers (localhost won't work in production).
**Fix:** Use a tool like `ngrok http 3000` to expose your local server during development. For production, deploy to a public HTTPS endpoint and update the Outbound Message endpoint URL in **Setup > Workflow Actions > Outbound Messages**.

## Next steps

- Add HMAC signature verification to the webhook so you can confirm the request came from Salesforce — see [Outbound Message security](https://developer.salesforce.com/docs/atlas.en-us.api.meta/api/sforce_api_om_outboundmessaging_wsdl.htm)
- Handle bulk updates by publishing one message per Opportunity to a queue — see [Bull queue documentation](https://docs.bullmq.io/)
- For the underlying API reference, use `/developer-docs-writer:write-api-docs` to generate docs for the Clearpath REST endpoints
- For deeper SDK usage, see `/developer-docs-writer:write-sdk-guide` if Clearpath ships an official Node.js client

---

## Results

### Criteria

- [x] PASS: Skill requires numbered steps — met. Step 3 mandates `## Step N:` format with a template; bullet points are not offered as an alternative.
- [x] PASS: Each step includes expected output — met. Step 3's template has a mandatory `**Expected result:**` block and the rule "Every step needs expected output."
- [x] PASS: Skill requires a complete runnable end-to-end example — met. Step 4 is dedicated to this and states "This is mandatory" and "The complete example is non-negotiable."
- [x] PASS: Skill requires a troubleshooting section covering common failure modes with specific fixes — met. Step 6 requires 4+ entries (auth error, config mistake, external service unavailable, rate-limit/transient failure) with Cause/Fix structure.
- [x] PASS: Skill requires a prerequisites section before integration steps begin — met. Step 2 defines the Prerequisites checklist template with rules requiring every credential to say where to find it.
- [x] PASS: Skill requires a research step — met. Step 1 is a mandatory research phase covering codebase search, auth method, config/env vars, existing docs, and minimum viable integration scope.
- [x] PASS: Skill covers how to verify the integration is working correctly — met. Step 5 is a dedicated verification section requiring concrete test data, expected behaviour, and inspection steps, separate from per-step expected results.
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — met. All three fields present at lines 1–4.

### Output expectations

- [x] PASS: Output's prerequisites section names what the developer needs before starting — Salesforce admin access with required permissions, Clearpath admin role, OAuth credentials (client_id/client_secret) — all explicit with dashboard locations.
- [x] PASS: Output's steps are numbered (1, 2, 3...) — met. Steps 1–5 are numbered with `## Step N:` headings.
- [x] PASS: Output's steps each include expected output/visible result — met. Every step has an `**Expected result:**` block showing console output or API response.
- [x] PASS: Output's complete runnable example covers an end-to-end deal-status sync — met. The Complete example section creates an Opportunity webhook event and shows the Clearpath project updating, with run command and expected output.
- [x] PASS: Output's troubleshooting section covers at least 4 common failure modes each with symptom, cause, and specific fix — met. Five entries covering auth expiry, missing custom field, project not found, rate limiting, and unreachable webhook URL.
- [x] PASS: Output's verification section explains how the developer confirms the integration is working — met. Dedicated "Verifying the integration" section with specific test actions (change Opportunity stage, check Clearpath project status), expected timing (30 seconds), and log inspection guidance.

## Notes

The skill definition is complete and well-structured. The mandatory process (7 steps) and output format template are both present and internally consistent. One minor observation: the Output Format section at the end of the skill shows a `## Quick Start` section, but the step-by-step process doesn't include a Quick Start writing step. This is a minor inconsistency — the output template suggests a Quick Start block that the process doesn't instruct the writer to produce. It doesn't affect the rubric score but could cause the generated guide to omit this section depending on which part of the skill the model attends to.
