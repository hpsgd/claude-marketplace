---
name: create-skill
description: "Create a new skill following the standard template. Handles SKILL.md creation, README update, and parent agent cross-reference."
argument-hint: "[skill name, parent agent, and brief description]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Create a new skill for $ARGUMENTS.

## Process (sequential — do not skip steps)

### Step 1: Read the template and conventions

```
Read(file_path="${CLAUDE_PLUGIN_ROOT}/templates/skill-template.md")
Read(file_path="CLAUDE.md")
```

The template defines the MANDATORY structure. Every field is required unless explicitly marked optional.

### Step 2: Identify the parent agent

1. Determine which agent owns this skill
2. Read the parent agent's definition:
   ```bash
   find plugins -path "*/{agent-name}/agents/*.md"
   ```
3. Understand the agent's domain, methodology, and existing skills
4. Check for existing skills under the agent to avoid duplication:
   ```bash
   find plugins -path "*/{agent-name}/skills/*/SKILL.md"
   ```

### Step 3: Research the domain

Before writing, understand what the skill should cover:

1. **Read the parent agent's methodology** — the skill should implement a specific slice of the agent's process
2. **Check sibling skills** — what do adjacent skills cover? Where are the boundaries?
3. **Identify the skill's unique contribution** — what does this skill do that the parent agent's general methodology doesn't cover in enough depth?

### Step 4: Create the directory

```bash
mkdir -p plugins/{category}/{agent}/skills/{skill-name}
```

Skill names are `kebab-case`, matching the directory name.

### Step 5: Write the SKILL.md

Follow the template structure. Every section is mandatory:

**Frontmatter (all fields required):**

```yaml
---
name: {kebab-case — matches directory}
description: "{What it produces — when to use it. Specific enough for auto-invocation}"
argument-hint: "[{what the user provides}]"
user-invocable: true
allowed-tools: {minimal set — principle of least access}
---
```

**Frontmatter rules:**
- `description` is CRITICAL — Claude may only read this to decide whether to invoke. Must include (1) what it produces, (2) when to use it
- `allowed-tools`: only include tools the skill actually needs. Read-only skills: `Read, Glob, Grep`. Skills that create files: add `Write, Edit`. Skills that run commands: add `Bash`
- `argument-hint`: wrapped in `[brackets]`, specific enough to guide the user
- `paths` (optional): add if the skill should auto-trigger on specific file patterns

**Body structure:**

| Section | Required | Purpose |
|---|---|---|
| Opening paragraph | Yes | What this skill does for `$ARGUMENTS`. Reference related skills |
| Sequential steps | Yes | Numbered, mandatory, blocking. Each produces a verifiable output |
| Rules / Anti-patterns | Yes | Specific imperatives ("Always X", "Never Y because Z") |
| Output format | Yes | Exact markdown template with all fields defined |

**Quality targets:**
- 100–500 lines
- Self-contained — works without reading the parent agent
- Sequential mandatory steps (not suggestions)
- Each step produces a verifiable output
- Generic examples only (no private references)
- External tools linked on first mention

### Step 6: Verify self-containment

Read the skill as if you've never seen the parent agent. Can you execute it?

| Check | Pass criteria |
|---|---|
| **Understandable** | A reader can understand what to do without the parent agent |
| **Executable** | Steps are specific enough to follow |
| **Complete** | No "see the agent for details" references |
| **Bounded** | Clear scope — doesn't try to be the whole agent |

### Step 7: Update README

Add the skill to the parent agent's row in the agent table in `README.md`.

### Step 8: Verify

Run the audit criteria mentally:

- [ ] 100–500 lines
- [ ] Description specific enough for auto-invocation
- [ ] Self-contained
- [ ] Sequential mandatory steps
- [ ] Verifiable step outputs
- [ ] Rules with anti-patterns
- [ ] Structured output format
- [ ] Cross-references related skills
- [ ] Generic examples only
- [ ] External tools linked
- [ ] Argument hint present
- [ ] Frontmatter description precise

## Anti-Patterns (NEVER do these)

- **Stub skills** — creating a 9-line placeholder with just frontmatter and a one-line instruction. Either write the full skill or don't create it
- **Agent duplication** — copying the parent agent's methodology verbatim. Skills zoom in on a specific process, not repeat the whole agent
- **"See the agent" references** — skills must be self-contained. "Follow the process defined in the agent" defeats the purpose
- **Vague descriptions** — "Helps with testing" matches everything and triggers on nothing. "Write E2E acceptance tests in Playwright for a user story" matches precisely
- **Kitchen sink tools** — listing every tool in `allowed-tools`. Read-only skills don't need Write, Edit, or Bash
- **Suggestions instead of steps** — "You might want to consider..." is not a step. "Identify all external API calls and verify each has a timeout configured" is a step

## Output Format

The output is the skill directory and file itself:

```
plugins/{category}/{agent}/skills/{skill-name}/SKILL.md
```

After creation, report:

```markdown
## Created: {skill-name} ({parent-agent})

- **Path:** `plugins/{category}/{agent}/skills/{skill-name}/SKILL.md`
- **Lines:** {count}
- **Description:** {frontmatter description}
- **Self-contained:** {yes/no}
- **README updated:** {yes/no}
- **Quality score:** {X}/12 criteria met
```
