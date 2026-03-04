# BeattieNetTrack — AI Session Prompt Guide

**Purpose:** Copy-paste prompts for each development phase. Each prompt is self-contained — paste it, add the referenced files, and go.

---

## How to Use This Guide

1. Each section maps to one Phase from the Roadmap
2. Each prompt includes a `[PASTE]` marker — paste the file contents there
3. One session = one task. Never combine tasks.
4. After every session, run `npm run validate:tracks && npm run lint` before committing.
5. Use **Sonnet** for all generation tasks. Use **Opus** only for schema/architecture decisions (marked ⚙️).

---

---

# PHASE 0 — Stabilize the Baseline

---

## P0-A: Content Audit (Run This First)

> **What it does:** Produces a complete inventory of every track, module, and activity — native MDX vs. legacy HTML. This is the map you navigate by for all future phases.
>
> **Model:** Sonnet
>
> **Input files needed:** All files in `src/content/tracks/`, `src/content/modules/`, `src/content/labs/`, `src/content/quizzes/`, `src/content/lessons/` — paste their contents, or give the AI directory access.

```
You are working in beattieNetTrack, an Astro 5 static LMS.

CONSTITUTION rules that apply to this task:
- Read-only analysis. No file changes.
- Output must be deterministic and reproducible.

Your task: Perform a complete content audit and produce a structured report.

For every track (pc-technician, network-engineer, cybersecurity-engineer, cybersecurity-foundations, web-developer, python-developer, ai-ml), produce a table with:

| Module ID | Module Title | Activities | Native MDX Labs | Native MDX Quizzes | Native MDX Lessons | Legacy HTML | Status |
|---|---|---|---|---|---|---|---|

Status options:
- EMPTY — module stub only, no activities
- PARTIAL — has some activities but not all expected content
- LEGACY — content exists but only as legacy HTML (legacyUrl pointing to /legacy/*)
- NATIVE — fully migrated to MDX with no legacy dependency
- MIXED — some native, some legacy

Also list:
1. All legacy HTML files in public/legacy/ that do NOT yet have a corresponding MDX lesson entry
2. All lessons/ MDX files that have legacyUrl set (still depending on legacy HTML)
3. All module stubs that contain only "Starter module scaffold" or "PC Technician module stub" as body content

Here are the relevant files:

TRACKS:
[PASTE contents of all src/content/tracks/*.mdx files]

MODULES:
[PASTE contents of all src/content/modules/**/*.mdx files]

LABS:
[PASTE contents of all src/content/labs/*.mdx files]

QUIZZES (non-tech-plus):
[PASTE contents of src/content/quizzes/network-fundamentals-checkpoint.mdx and pc-tech-hardware-checkpoint.mdx]

LESSONS (frontmatter only is fine):
[PASTE frontmatter blocks from all src/content/lessons/*.mdx files]
```

---

## P0-B: Fix Validation Warnings

> **What it does:** Cleans up any `moduleId` fields that are inferred from legacy slugs so they are explicitly declared. Eliminates all validation warnings.
>
> **Model:** Sonnet
>
> **Run first:** `npm run validate:tracks` and capture its full output.

```
You are working in beattieNetTrack, an Astro 5 static LMS governed by CONSTITUTION.md.

CONSTITUTION rules that apply:
- One fix at a time (§3 Change Scope Contract)
- All changes must pass `npm run validate:tracks` (§10 Validation Contract)
- Prefer additive changes, no refactors (§3)

Here is the current output of `npm run validate:tracks`:
[PASTE full terminal output]

Here is src/content/config.ts (the schema authority):
[PASTE config.ts]

Here is scripts/validate-tracks.mjs:
[PASTE validate-tracks.mjs]

Your task: Fix every WARNING in the validation output. Do not touch errors — list those separately for human review.

For each warning, show:
1. The file that needs changing
2. The exact frontmatter change (old → new)
3. Why this resolves the warning

Output as a series of precise file edits. Do not change anything not mentioned in a warning.
```

---

## P0-C ⚙️: Legacy Migration — One File at a Time

> **What it does:** Converts a single legacy HTML file to a proper native MDX lesson. Run this prompt once per legacy file.
>
> **Model:** Sonnet (Opus if the content is ambiguous about which track/module it belongs to)
>
> **Note:** After migration, the legacy HTML file stays in `public/legacy/` — do NOT delete it. Just remove the `legacyUrl` dependency from the MDX lesson.

```
You are working in beattieNetTrack, an Astro 5 static LMS governed by CONSTITUTION.md.

CONSTITUTION rules that apply:
- One file per session (§3)
- No new routes (§4)
- Navigation integrity — do not break existing links (§6)
- Track/module mapping is mandatory (§9)

Content schema authority (src/content/config.ts):
[PASTE config.ts]

Here is the legacy HTML file to migrate:
Filename: [FILENAME e.g. a-plus-hardware.html]
[PASTE full HTML file contents]

Here is the current MDX lesson file for this content (if it exists):
[PASTE src/content/lessons/[slug].mdx OR write "Does not exist yet"]

Known track/module mapping for this content:
Track: [e.g. pc-technician]
ModuleId: [e.g. pct.hardware.components-identification]
Order: [e.g. 2]

Your task:
1. Produce a complete, valid MDX lesson file for src/content/lessons/[slug].mdx
2. Extract all meaningful content from the HTML (headings, body text, lists, code blocks) and convert to clean MDX
3. Set correct frontmatter: title, description, slug, track, moduleId, order, difficulty, estMinutes, tags
4. Do NOT set legacyUrl — this is a native migration, not a wrapper
5. Replace any relative HTML links (href="a-plus-hardware.html") with canonical Astro routes (/lessons/a-plus-hardware)
6. Wrap any interactive demo content in a <Callout type="info"> noting it requires the workspace

Output: The complete MDX file contents, ready to write to disk.
```

---

---

# PHASE 1 — Curriculum Ingest Pipeline

---

## P1-A ⚙️: Design the Curriculum Manifest Schema

> **What it does:** Defines the JSON/YAML manifest format that curriculum authors will use to add new tracks. This is an architectural decision — use Opus.
>
> **Model:** Opus
>
> **This session produces:** `docs/CURRICULUM_MANIFEST_SCHEMA.md` and a sample manifest file. Do NOT write any code yet.

```
You are the architect for beattieNetTrack, an Astro 5 static LMS governed by CONSTITUTION.md.

Your task is to design a curriculum manifest schema — a JSON format that a curriculum author fills out to add a new track. The ingest script will read this manifest and generate all required MDX files.

CONSTITUTION constraints:
- Every activity (lab, quiz, activity) MUST declare track and moduleId (§9)
- No new npm dependencies (§4)
- Validation must pass after ingest (§10)
- Static-first — no runtime schema, content collections only (§1)

Current content schema (what the ingest script must generate toward):
[PASTE src/content/config.ts]

Existing ingest script for reference (assessments only, not full curriculum):
[PASTE scripts/ingest-assessments-from-manifest.mjs]

The manifest must support authoring all of these content types:
- tracks (title, description, icon, estimatedHours, level)
- modules (title, description, order within track)
- lessons (title, description, body content or reference to .md source file)
- labs (steps with validators, hints, checklist)
- quizzes (questions: single/multi/short, passThreshold)
- activities (iframe/terminal/code, labPath or labUrl)

Design requirements:
1. A curriculum author should be able to fill this out without knowing Astro or TypeScript
2. All required fields for validation must be inferrable from the manifest — authors should not need to manually specify track and moduleId on each activity (the manifest structure implies them)
3. The format must be versionable so future changes don't break existing manifests
4. Lab steps and quiz questions should be expressible without MDX syntax
5. The manifest should reference external .md files for long-form lesson body content

Produce:
1. The full manifest JSON schema with field descriptions and required/optional markers
2. A complete sample manifest for a hypothetical "Linux Fundamentals" track with 2 modules, 3 lessons, 2 labs, and 2 quizzes
3. A list of design decisions and the rationale for each
4. Any known limitations or tradeoffs in your design

Do NOT write the ingest script yet. Schema only.
```

---

## P1-B: Build the Ingest Script

> **What it does:** Builds `scripts/ingest-curriculum.mjs` — the script that reads a manifest and generates all MDX files.
>
> **Model:** Sonnet
>
> **Prerequisite:** P1-A must be complete. Paste the approved manifest schema.

```
You are working in beattieNetTrack, an Astro 5 static LMS governed by CONSTITUTION.md.

CONSTITUTION rules that apply:
- No new npm dependencies (§4)
- validate:tracks must pass after ingest (§10)
- One feature per change (§3)
- No changes to astro.config.* or package.json except to add the new script entry (§4)

Content schema authority (what the script must generate toward):
[PASTE src/content/config.ts]

Existing ingest script for reference (assessments only):
[PASTE scripts/ingest-assessments-from-manifest.mjs]

Approved curriculum manifest schema:
[PASTE the schema from P1-A output]

Sample manifest to test against:
[PASTE the sample manifest from P1-A output]

Your task: Write scripts/ingest-curriculum.mjs that:

1. Accepts --manifest <path> argument (required) and --dry-run flag (optional)
2. Reads and validates the manifest against the schema
3. Generates in order:
   a. src/content/tracks/<track-slug>.mdx (creates or skips if exists and --no-overwrite)
   b. src/content/modules/<track-slug>/<module-id>.mdx for each module
   c. src/content/lessons/<slug>.mdx for each lesson (reads body from referenced .md file if specified)
   d. src/content/labs/<slug>.mdx for each lab
   e. src/content/quizzes/<track-slug>/<slug>.mdx for each quiz
4. Infers track and moduleId from manifest structure — never requires author to repeat them
5. On --dry-run: prints what would be created, creates nothing
6. On completion: prints a summary table (X tracks, Y modules, Z lessons, A labs, B quizzes)
7. Exits non-zero if manifest validation fails
8. Does NOT run validate:tracks itself (caller does that)

Output: The complete script file, ready to write to disk at scripts/ingest-curriculum.mjs.
Also output: The package.json scripts entry to add: "ingest:curriculum": "node scripts/ingest-curriculum.mjs"
```

---

## P1-C: Write CONTENT_AUTHORING.md

> **What it does:** Creates the documentation that a curriculum author reads to add a new track. No code knowledge required to follow it.
>
> **Model:** Sonnet

```
You are working in beattieNetTrack, an Astro 5 static LMS.

Your task: Write docs/CONTENT_AUTHORING.md — a guide for curriculum authors who want to add a new track. The audience is a subject matter expert (e.g., a network engineer) who knows their content but is not a developer.

The guide must cover:
1. Overview of the track/module/activity hierarchy with a plain-English explanation
2. Step-by-step: how to create a new track from scratch
   - Create your manifest file (link to schema)
   - Create your lesson body .md files
   - Run npm run ingest:curriculum -- --manifest path/to/manifest.json --dry-run to preview
   - Run without --dry-run to generate
   - Run npm run validate:tracks to confirm
   - Commit
3. How to add content to an existing track (new module or new activity)
4. Lab authoring reference: how to write step validators (exact, oneOf, regex) with examples
5. Quiz authoring reference: single, multi, and short-answer question formats with examples
6. Common errors from validate:tracks and how to fix them
7. What to do if you're unsure (who to ask, what not to touch)

Tone: Clear, instructional, non-condescending. Assume intelligence but not technical depth.
Format: GitHub-flavored Markdown with code blocks for examples.

Approved manifest schema for reference:
[PASTE schema from P1-A]
```

---

---

# PHASE 2 — XP, Gamification & Visible Progress

---

## P2-A: XP Accumulator Island

> **What it does:** Adds a visible XP total with rank tier to the home dashboard and track pages.
>
> **Model:** Sonnet

```
You are working in beattieNetTrack, an Astro 5 static LMS governed by CONSTITUTION.md.

CONSTITUTION rules that apply:
- Islands for interactivity only, must not change primary page structure (§8)
- No CLS — reserve layout space before hydration (§8, §12)
- Reuse existing layout/component system (§5)
- No new npm dependencies (§4)
- Static-first — all learning content is already rendered (§1)

Existing progress store (localStorage):
[PASTE src/lib/progressStore.ts]

Existing island examples to match style:
[PASTE src/components/islands/TrackProgressSummary.tsx]
[PASTE src/components/islands/SidebarTrackProgress.tsx]

Existing CSS tokens:
[PASTE src/styles/tokens.css]

Current home page (index.astro):
[PASTE src/pages/index.astro]

Your task: Create src/components/islands/XpSummary.tsx

Requirements:
1. Reads xpTotal and streak from progressStore (localStorage key: beattie_progress_v1)
2. Displays: total XP, current rank tier, XP needed for next tier
3. Rank tiers:
   - 0–99 XP: Technician
   - 100–299 XP: Practitioner  
   - 300–599 XP: Specialist
   - 600–999 XP: Engineer
   - 1000+ XP: Expert
4. Shows streak count if > 0
5. Reserves layout space via min-height before hydration (no CLS)
6. Uses existing CSS tokens, no new CSS files
7. Uses client:only="react" hydration

Also show: Where to add <XpSummary client:only="react" /> in index.astro (exact insertion point).
```

---

## P2-B: Module Completion Badges

> **What it does:** Shows a completion badge on module cards when all activities in a module are done.
>
> **Model:** Sonnet

```
You are working in beattieNetTrack, an Astro 5 static LMS governed by CONSTITUTION.md.

CONSTITUTION rules that apply:
- Islands for interactivity only (§8)
- No CLS — reserve layout space (§8)
- Reuse existing components (§5)
- One feature per change (§3)

Progress store:
[PASTE src/lib/progressStore.ts]

Track detail page:
[PASTE src/pages/tracks/[slug].astro]

TrackModulesView component:
[PASTE src/components/tracks/TrackModulesView.astro]

Your task: Add module completion badge display.

When all activities in a module are completed (labs, quizzes, lessons all marked complete in progressStore), show a ✓ Complete badge on the module card.

Requirements:
1. Create src/components/islands/ModuleCompletionBadge.tsx
2. Props: moduleSlug (string), activityKeys (Array<{type: 'lab'|'quiz'|'lesson', slug: string}>)
3. Reads progressStore client-side, determines if all activities complete
4. Renders a styled "✓ Complete" badge if complete, empty placeholder if not (no CLS)
5. No new CSS files — use existing token classes

Also show: Exact change to TrackModulesView.astro to pass activityKeys and render the island per module.
```

---

## P2-C: Track Completion Certificate

> **What it does:** Adds a printable certificate page at `/certificate/[trackSlug]` that renders when a full track is complete.
>
> **Model:** Sonnet

```
You are working in beattieNetTrack, an Astro 5 static LMS governed by CONSTITUTION.md.

CONSTITUTION rules that apply:
- New route is strictly required for this feature — justified (§4)
- No CLS (§8)
- Reuse layout system (§5)
- Static-first — page is static, data hydrated client-side (§1)

Progress store:
[PASTE src/lib/progressStore.ts]

content.ts (for getTrackDetailData):
[PASTE src/lib/content.ts]

AppShell layout:
[PASTE src/layouts/AppShell.astro - or just the props interface]

CSS tokens:
[PASTE src/styles/tokens.css]

Your task: Create src/pages/certificate/[trackSlug].astro

Requirements:
1. getStaticPaths generates a route for every non-legacy track
2. Page renders statically with track title and a placeholder for learner name
3. A React island (src/components/islands/CertificateView.tsx) hydrates client-side to:
   - Check if track is 100% complete in progressStore
   - If complete: show the full certificate with completedAt date from the most recent activity
   - If not complete: show "Complete all modules to unlock this certificate" with a link back to the track
   - Read learner display name from localStorage key beattie_profile_v1.displayName (may be null — show "Learner" as fallback)
4. Certificate must be print-friendly: @media print hides nav/sidebar, shows only certificate content
5. No new npm dependencies

Output: certificate/[trackSlug].astro and CertificateView.tsx, both complete.
```

---

---

# PHASE 3 — Durable Progress & Supabase

---

## P3-A ⚙️: Design the Supabase Data Model

> **What it does:** Defines the database schema for user accounts, progress, and badges.
>
> **Model:** Opus

```
You are the architect for beattieNetTrack, an Astro 5 static LMS governed by CONSTITUTION.md.

Your task: Design the Supabase PostgreSQL schema for durable progress persistence.

CONSTITUTION constraints:
- Static-first architecture must be preserved — Supabase is additive only (§1)
- localStorage fallback must continue to work for anonymous users (§2 Determinism)
- No new npm dependencies without approval (§4)
- This is a design task only — no code

Current client-side progress model (localStorage):
[PASTE src/lib/progressStore.ts]

Current content model summary:
- 7 tracks, each with 5 modules
- Activities: labs, quizzes, lessons
- Each lab has xp value
- Quizzes have passThreshold and bestScore
- Streak tracking (consecutive active days)

Design requirements:
1. User table: support both authenticated users and anonymous (guest) users
2. Progress table: mirror the structure of ProgressState from progressStore.ts so sync is straightforward
3. Badge table: earned badges with earnedAt timestamp
4. Leaderboard view (future): XP by user, filterable by track
5. Row Level Security: users can only read/write their own progress
6. Schema must be additive to the existing codebase — no breaking changes to localStorage shape

Produce:
1. Full SQL CREATE TABLE statements with RLS policies
2. A sync strategy: how localStorage progress gets merged with Supabase on first login
3. Supabase Edge Function stubs needed (if any)
4. A list of what stays in localStorage vs. what moves to Supabase
5. Known risks or tradeoffs
```

---

## P3-B: Supabase Auth Integration (Anonymous → Authenticated)

> **What it does:** Adds optional Supabase auth. Anonymous users continue using localStorage. Signing in syncs progress to the database.
>
> **Model:** Sonnet
>
> **Prerequisite:** P3-A approved schema must be applied to your Supabase project first.

```
You are working in beattieNetTrack, an Astro 5 static LMS governed by CONSTITUTION.md.

CONSTITUTION rules that apply:
- Static-first — auth is additive only, no SSR (§1)
- Islands for interactivity only (§8)
- No new npm dependencies without approval — @supabase/supabase-js is approved for this task (§4)
- One feature: auth sign-in/sign-out island only. Progress sync is a separate task. (§3)

Approved Supabase schema from P3-A:
[PASTE approved schema]

Existing progress store:
[PASTE src/lib/progressStore.ts]

AppShell layout (for where to add auth UI):
[PASTE src/layouts/AppShell.astro]

Your task: Add Supabase authentication as an optional layer.

1. Create src/lib/supabaseClient.ts — initializes the Supabase client from environment variables SUPABASE_URL and SUPABASE_ANON_KEY
2. Create src/components/islands/AuthButton.tsx — a React island that:
   - Shows "Sign In" if not authenticated (opens Supabase magic link email flow)
   - Shows user email + "Sign Out" if authenticated
   - Does NOT sync progress yet (that is the next task)
   - Uses client:only="react"
3. Show where to add <AuthButton client:only="react" /> in AppShell.astro
4. Show the .env.example entries needed

Do not implement progress sync in this task.
```

---

---

# PHASE 1 — Coach Client (Stub → Real)

*(The CoachClient stub already exists at src/lib/coach/CoachClient.ts. This phase activates it.)*

---

## COACH-A: Wire the Anthropic API into CoachClient

> **What it does:** Replaces the stub CoachClient with a real implementation that calls the Anthropic API from a Supabase Edge Function (keeps the API key server-side).
>
> **Model:** Sonnet
>
> **Prerequisite:** Supabase is connected and Edge Functions are enabled.

```
You are working in beattieNetTrack, an Astro 5 static LMS governed by CONSTITUTION.md.

CONSTITUTION rules that apply:
- Islands for interactivity only (§8)
- No new npm dependencies in the Astro project without approval (§4)
- Static-first — coach is an island, never affects static build (§1)
- Educational safety — coach responses must reinforce learning, not give direct answers (§13)

Current CoachClient stub:
[PASTE src/lib/coach/CoachClient.ts]

Current contextSnapshot:
[PASTE src/lib/contextSnapshot.ts]

Your task: Replace the stub with a real implementation via Supabase Edge Function.

1. Write supabase/functions/coach/index.ts — an Edge Function that:
   - Accepts POST with { message: string, context: ContextSnapshot }
   - Calls Anthropic claude-sonnet-4-6 with a system prompt that:
     * Establishes the coach as a Socratic tutor — asks leading questions rather than giving answers
     * Is aware of the current track, module, and activity from context
     * Enforces educational safety: no direct exam answers, no cheating assistance
   - Returns { content: string }
   - Reads ANTHROPIC_API_KEY from Supabase secrets

2. Update src/lib/coach/CoachClient.ts to call the Edge Function instead of returning the stub
   - Keep the same interface (sendMessage input/output types unchanged)
   - Add error handling with a user-friendly fallback message

Output: The Edge Function file and the updated CoachClient.ts.
```

---

---

# Reusable Debug Prompts

---

## DEBUG-VALIDATE: Fix a Failing Validate Run

```
You are working in beattieNetTrack, an Astro 5 static LMS governed by CONSTITUTION.md.

Here is the failing output of `npm run validate:tracks`:
[PASTE full output]

Here is scripts/validate-tracks.mjs:
[PASTE validate-tracks.mjs]

Here is src/content/config.ts:
[PASTE config.ts]

The failing files:
[PASTE contents of any flagged MDX files]

Your task: Identify the exact cause of each failure and produce the minimal fix for each affected file. Show old → new for each frontmatter field that changes. Do not change anything not directly causing a failure.
```

---

## DEBUG-BUILD: Fix a Failing Astro Build

```
You are working in beattieNetTrack, an Astro 5 static LMS governed by CONSTITUTION.md.

Here is the failing output of `npm run build`:
[PASTE full terminal output including the error]

Relevant source files (paste whichever are referenced in the error):
[PASTE files]

Your task: Identify the root cause and produce the minimal fix. One change only. Do not refactor surrounding code.
```

---

## DEBUG-TEST: Fix a Failing Playwright Test

```
You are working in beattieNetTrack, an Astro 5 static LMS governed by CONSTITUTION.md.

Here is the failing test output:
[PASTE playwright output]

Here is the failing test file:
[PASTE tests/[name].spec.ts]

Relevant source files:
[PASTE any component or page files referenced by the test]

Your task: Determine if this is (a) a test that needs updating because the feature changed intentionally, or (b) a regression in the source code.

If (a): Show the minimal test update.
If (b): Show the minimal source fix. Do not update tests to hide regressions.
```

---

---

# Session Hygiene Checklist

Run this after every AI session before committing:

```bash
npm run validate:tracks    # Must exit 0
npm run lint               # Must exit 0 (astro check)
npm run test:unit          # Must exit 0
npm run build              # Must succeed
```

Only run Playwright if you changed a component that affects visual layout:
```bash
npm run test:visual
```

If visual snapshots need updating (intentional layout change only):
```bash
npm run test:visual:update
```

**Commit message format:**
```
feat(phase): short description of what changed

- Specific file 1: what changed
- Specific file 2: what changed

Resolves: [roadmap item reference]
```
