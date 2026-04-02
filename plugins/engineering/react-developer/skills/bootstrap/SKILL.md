---
name: bootstrap
description: "Bootstrap React/Next.js conventions into the architecture documentation. Appends frontend-specific sections to docs/architecture/CLAUDE.md. Idempotent — merges missing sections into existing files without overwriting."
argument-hint: "[project name]"
user-invocable: false
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Bootstrap React/Next.js Conventions

Bootstrap React/Next.js development conventions for **$ARGUMENTS**.

This skill does NOT create its own domain directory. It appends React-specific sections to `docs/architecture/CLAUDE.md`.

## Process

### Step 1: Verify architecture domain exists

```bash
mkdir -p docs/architecture
```

If `docs/architecture/CLAUDE.md` does not exist, stop and report that the architect bootstrap should run first.

### Step 2: Append React conventions to `docs/architecture/CLAUDE.md`

Check if `docs/architecture/CLAUDE.md` already contains a "React/Next.js Conventions" section. If not, append the following:

```markdown

<!-- Added by react-developer bootstrap v0.1.0 -->
## React/Next.js Conventions

### TypeScript

- **Strict mode enabled** — `"strict": true` in `tsconfig.json`
- No `any` — use `unknown` and narrow, or define proper types
- Prefer `interface` for object shapes, `type` for unions and intersections
- Export types alongside components: co-locate types in the same file

### Styling

- **Tailwind CSS** for all styling — no CSS modules or styled-components
- Use `cn()` utility (clsx + tailwind-merge) for conditional classes
- Design tokens via Tailwind config (`tailwind.config.ts`)
- Responsive: mobile-first (`sm:`, `md:`, `lg:` breakpoints)

### Component Patterns

- Server Components by default (Next.js App Router)
- `"use client"` only when the component needs interactivity or browser APIs
- Co-locate components with their tests: `Button.tsx` + `Button.test.tsx`
- Props interfaces named `{Component}Props`
- Prefer composition over prop drilling — use React Context sparingly

### Testing

- **Vitest** for unit and component tests
- **React Testing Library** for component testing — test behaviour, not implementation
- Test file naming: `{Component}.test.tsx`
- Use `screen.getByRole()` queries — avoid `getByTestId` unless necessary
- Coverage enforced via SonarCloud (project-specific threshold)

### Project Structure

```
src/
├── app/                 # Next.js App Router (pages, layouts, routes)
├── components/
│   ├── ui/              # Reusable primitives (Button, Input, Card)
│   └── features/        # Feature-specific composed components
├── lib/                 # Shared utilities, API clients, hooks
├── types/               # Shared TypeScript types
└── styles/              # Global styles, Tailwind config
```

### Deployment

- **Vercel** for hosting with preview deployments on every PR
- Environment variables managed in Vercel dashboard
- Production deploy on merge to main (or release tag)

### React/Next.js Tooling

| Tool | Purpose |
|------|---------|
| [Vercel](https://vercel.com) | Frontend hosting with preview deploys |
| [SonarCloud](https://sonarcloud.io) | TypeScript code quality and coverage gate |
| [GitHub Actions](https://docs.github.com/en/actions) | `vitest` in CI on every PR |

### Available React Skills

| Skill | Purpose |
|-------|---------|
| `/react-developer:component-from-spec` | Create a React component from a design spec |
| `/react-developer:performance-audit` | Audit frontend performance |
```

### Step 3: Return manifest

After creating/merging all files, output a summary:

```
## React Developer Bootstrap Complete

### Files updated
- `docs/architecture/CLAUDE.md` — appended React/Next.js Conventions section

### Files merged
- (list any existing files where sections were appended)

### Next steps
- Configure Tailwind CSS and `cn()` utility
- Set up Vitest with React Testing Library
- Use `/react-developer:component-from-spec` for new components
- Use `/react-developer:performance-audit` for performance reviews
```
