# BeattieNetTrack LMS — Project Review & World-Class Roadmap

**Prepared:** March 2026  
**Project:** beattieNetTrack (Astro 5 Static LMS)  
**Author:** Review + Roadmap by Claude for Beattie Tech

---

## Part 1: What You Have — An Honest Assessment

### The Foundation Is Solid and Deliberately Designed

BeattieNetTrack is not a prototype. It is a governed, constitutional LMS built on **Astro 5 with static output** — a strong architectural decision. Every page renders at build time, meaning zero client-side fetching overhead for core content. The project has 10+ Git commits of real work, a CI pipeline, a formal `CONSTITUTION.md`, a schema-enforced content system, and a validation gate. This is the kind of infrastructure discipline that most LMS side projects never reach.

---

### What Exists Today

**Tech Stack**
- Astro 5 (static output) + React 18 islands for interactive UI
- MDX content collections for all curriculum types
- Playwright visual regression testing
- TypeScript throughout, with `astro check` as the lint gate
- CodeMirror for code editor islands

**Content Architecture**
Six content collection types are schema-defined and schema-validated:

| Collection | Purpose |
|---|---|
| `tracks` | Top-level learning paths (e.g., PC Technician, Network Engineer) |
| `modules` | Chapters within a track |
| `labs` | Step-validated, interactive hands-on exercises |
| `quizzes` | Single/multi/short-answer assessments |
| `lessons` | Rich MDX content pages (study guides, references) |
| `activities` | Workspace-routed activities (iframe/terminal/code) |

Plus: `tour`, `studyGuides`, and a `legacy` compatibility layer for ported HTML content.

**Validation Pipeline**
`npm run validate:tracks` enforces that every lab, quiz, and activity declares a `track` and a `moduleId` that resolve to real entries. This runs as a pre-build gate in CI. This is critical — it means bad content **cannot ship**.

**Navigation & Progress**
The `content.ts` library builds prev/next navigation chains per module. A `TrackProgressSummary` React island reads `localStorage` to hydrate progress state client-side. The index page shows a "Continue →" smart link per track.

**Search**
A `SearchOverlay` component backed by `searchIndex.ts` provides full-text search across tracks, modules, lessons, labs, and quizzes — built at static render time.

**Legacy Compatibility**
A `legacy-compat.css` layer and `inferLegacyTrackSlug` / `mapLessonToLegacyActivity` utilities bridge old `.html`-routed content into the new track/module hierarchy. Old links under `/legacy/...` are preserved.

---

### What Is Incomplete or Rough

**Content Population Gap**
The scaffolding is excellent, but the content itself is still thin. The existing tracks (PC Technician, Network Engineer, Cybersecurity Engineer) have framework entries, but the majority of learning material is still in the legacy HTML layer — not yet migrated into the proper MDX collection structure.

**No Repeatable Curriculum Ingest Pipeline**
The most critical missing piece. There is a `scripts/ingest-assessments-from-manifest.mjs` script stub, but there is no documented, tested pipeline for: "I have new curriculum → here's how I add it without touching code." Every content author currently needs to understand MDX frontmatter schemas and Git. This is a bottleneck at scale.

**Progress Persistence is Client-Only**
`localStorage` is fine for MVP but creates real problems: progress doesn't sync across devices, can't be reset or reported on, and disappears when a user clears their browser. There is no user account layer.

**No XP/Gamification Rendering**
Labs declare `xp` values in frontmatter, but there's no visible XP tracker, leaderboard, or completion badge system rendered to the user.

**Terminal Labs Are Simulated, Not Live**
The `LabRunner` with `activity: 'terminal'` provides a simulated command-line experience. There is no live shell or container-backed execution yet.

**No Instructor/Admin Layer**
No way to add content, review student progress, or manage tracks without direct codebase access.

---

## Part 2: The Architecture of a World-Class LMS

Before the roadmap, it helps to define the target clearly. A world-class LMS built on this foundation needs three things:

1. **Repeatable content scaling** — Any curriculum author can add a full track (lessons, labs, quizzes) by following a defined process, without writing code.
2. **Durable learner progress** — Progress, XP, completions, and certificates persist and are reportable.
3. **Live, hands-on labs** — Lab environments that execute real commands in isolated, ephemeral containers — not simulations.

The current architecture (Astro static + content collections + validation gate) is the right foundation for all three. The path forward is additive, not a rewrite.

---

## Part 3: The Roadmap

### Phase 0 — Stabilize the Current Baseline *(Now → 2 weeks)*

Before building forward, lock down what exists.

**0.1 — Content Audit & Gap Map**
Run a complete audit of all three tracks: which modules are fully populated in MDX vs. still relying on the legacy layer. Produce a spreadsheet showing: Track → Module → Activity count → Legacy vs. Native.

**0.2 — Fix All Validation Warnings**
Ensure `npm run validate:tracks` passes clean with zero warnings, not just zero errors. Any `moduleId` that infers from a legacy slug should be explicitly declared.

**0.3 — Close the Legacy Migration**
Systematically convert legacy `.html` lessons to proper MDX `lessons` entries with full `track` and `moduleId` frontmatter. The `lesson-link-updates-diff.md` already started this — finish it.

**0.4 — CI Green at All Gates**
Ensure `npm run test:ci` (validate + lint + unit + build + visual) passes on every commit. No exceptions. The CONSTITUTION already mandates this; enforce it in GitHub Actions with branch protection.

---

### Phase 1 — The Content Ingest Pipeline *(2–6 weeks)*

**This is the highest-leverage investment.** Without it, scaling content requires developers. With it, a curriculum author with a folder of Markdown files can ship a new track.

**1.1 — Define the Curriculum Manifest Schema**

Create a documented `curriculum-manifest.json` (or YAML) format that a content author fills out to define a new track. Example structure:

```json
{
  "track": {
    "id": "cloud-practitioner",
    "title": "AWS Cloud Practitioner",
    "description": "...",
    "estimatedHours": 40,
    "order": 4
  },
  "modules": [
    {
      "id": "cloud-foundations",
      "title": "Cloud Foundations",
      "order": 1,
      "activities": [
        { "type": "lesson", "file": "01-what-is-cloud.md", "order": 1 },
        { "type": "lab",    "file": "lab-s3-basics.md",   "order": 2 },
        { "type": "quiz",   "file": "quiz-foundations.md", "order": 3 }
      ]
    }
  ]
}
```

**1.2 — Build the Ingest Script**

Extend `scripts/ingest-assessments-from-manifest.mjs` into a full `scripts/ingest-curriculum.mjs` that:

- Reads a manifest + a folder of source `.md` files
- Generates all required MDX files with correct frontmatter
- Places files into the correct `src/content/` subdirectories
- Runs `validate:tracks` automatically after ingest
- Reports a summary: X lessons created, Y labs created, Z quizzes created

**1.3 — Define the Lab Authoring Format**

Labs are the most complex content type (they have `steps`, `validators`, `hints`). Create a simplified authoring template — a single `.md` file with a YAML block that the ingest script converts to the full lab MDX schema. The author only specifies what matters for pedagogy, not the technical collection plumbing.

**1.4 — Document the Workflow**

Write a `CONTENT_AUTHORING.md` that explains the complete process: write files → fill in manifest → run `npm run ingest:curriculum -- --manifest path/to/manifest.json` → validate → commit. No Astro knowledge required.

---

### Phase 2 — XP, Gamification & Visible Progress *(6–10 weeks)*

The schema already declares `xp` per lab. Build the UX around it.

**2.1 — XP Accumulator Island**

React island that reads all completed labs from `localStorage`, sums XP, and displays a running total with a progress bar toward the next "rank" (e.g., 0–100 XP = Technician → 101–300 = Practitioner → etc.).

**2.2 — Module Completion Badges**

When all activities in a module are completed, display a badge on the module card. Store earned badges in `localStorage` keyed by `moduleId`. Show them on the track overview page.

**2.3 — Track Completion Certificate**

When a full track is completed (all modules done), render a printable certificate page at `/certificate/[trackSlug]` that displays the learner's name (from a simple local profile), the track title, and completion date. No backend required — fully static with client-side data.

**2.4 — Study Streak Tracker**

Display a streak counter (consecutive days with at least one completed activity) on the home dashboard. Uses `localStorage` with date-stamped completions.

---

### Phase 3 — Durable Progress & User Accounts *(10–18 weeks)*

This is the transition from a single-device tool to a true multi-session LMS.

**3.1 — Supabase Backend**

You are already connected to Supabase. Introduce an optional Supabase auth + progress persistence layer:

- User table: `id`, `email`, `display_name`, `created_at`
- Progress table: `user_id`, `activity_type`, `activity_slug`, `completed_at`, `xp_earned`
- Badge table: `user_id`, `badge_id`, `earned_at`

Keep the `localStorage` path as a fallback for anonymous/guest users. Authenticated users get synced progress.

**3.2 — Preserve the Static-First Contract**

This is critical. The Astro CONSTITUTION prohibits runtime fetching for core content. The auth/progress layer must be **additive**, loaded only in React islands after hydration. The static pages stay static.

**3.3 — Progress Dashboard Page**

Add a `/dashboard` page that shows: overall XP, track completion percentages, earned badges, and a "continue where you left off" smart link. Data is fetched in a `client:only` React island from Supabase.

**3.4 — Instructor View (Read-Only)**

An instructor-facing page at `/admin/progress` (auth-gated) that shows aggregate completion rates by track and module. No student PII exposed — aggregate only.

---

### Phase 4 — Live Lab Environments *(18–30 weeks)*

This is the most technically complex phase and what separates a great LMS from an excellent one.

**4.1 — WebTerminal with Real Shell**

Replace the simulated `LabRunner` terminal with a WebSocket-connected terminal (xterm.js) backed by ephemeral containers (Docker via a Fly.io or Railway microservice). Each lab session spins a container, connects the terminal, and tears down on completion.

**4.2 — Lab Environment Definitions**

Define lab environments as Docker images. A lab's MDX frontmatter declares which image to use:

```yaml
environment: ubuntu-network-tools
```

The `ubuntu-network-tools` image is a published Docker image in your registry with tools pre-installed (nmap, Wireshark, etc.).

**4.3 — Auto-Graded Steps**

Connect the existing `steps[].validator` schema in labs to real command output. When a step uses `validator.type: regex`, the terminal output after a command is tested against the regex server-side, and success/failure is returned to the client.

**4.4 — Lab Session Management**

Build a lightweight session API (Supabase Edge Functions work well here): create session → get WebSocket URL → heartbeat → teardown. Sessions time out after inactivity to manage cost.

---

### Phase 5 — Content Scale & AI Assist *(Ongoing)*

**5.1 — AI-Assisted Lab Generation**

Build a script that takes a topic description (e.g., "subnetting practice — CIDR notation") and uses the Anthropic API to generate a complete lab MDX file in the correct schema. A curriculum author reviews and approves before ingest. This dramatically accelerates content creation.

**5A — Instructor Batch Question Generation**

Instructor-facing UI for generating CompTIA Network+ practice questions on demand. Each generated question is scenario-based ("A technician notices…"), includes per-distractor explanations, maps to a specific N10-009 objective, and passes automated schema validation before surfacing in an instructor review queue (approve / edit / reject). Approved questions enter a permanent Supabase bank and are available in quizzes and exam simulation mode. The API key never touches the browser — all Anthropic calls go through a Supabase Edge Function. Target: 50+ approved questions across all five N10-009 domains; exam simulation at 90 questions / 90 minutes mirroring the real exam's domain weighting. Full spec: `docs/PHASE5_QUESTION_ENGINE.md`.

**5B — Adaptive Student Mode** *(requires 5A complete)*

After a student finishes a lesson, the system generates a single fresh challenge question grounded in that lesson's content and serves it in real time — no instructor in the loop. The lesson MDX is injected directly into the generation prompt, so the model summarizes facts it was just given rather than recalling from training (dramatically reducing hallucination risk). Every generated question passes four automated validation gates (schema, content safety, grounding check, duplicate check) before the student sees it; any failure silently falls back to a random approved question from the 5A bank. Questions are low-stakes and formative — no grade impact, 5 XP on correct answer, skip always available. Students can flag bad questions; three flags auto-retire a question. An instructor dashboard exposes generation quality metrics (gate pass rate, per-lesson correct/incorrect rate, flag queue) and closes the feedback loop: a lesson with poor adaptive question performance signals that the lesson content itself needs work. Full spec: `docs/PHASE5_QUESTION_ENGINE.md § Phase 5B`.

**5C — Instructor Adaptive Dashboard**

Visibility layer for 5B: generation quality metrics, per-lesson correct/incorrect rates on adaptive questions, student flag queue, and the ability to promote a high-quality adaptive question into the approved 5A bank. The feedback loop this creates — student performance on adaptive questions → lesson quality signal → instructor improves lesson → better generated questions — is the mechanism that makes the system self-improving over time.

**5.5 — Per-Student Difficulty Adaptation** *(future, schema-ready)*

Track correct/incorrect rates per student per module. Above 80% correct → next adaptive question generates at higher difficulty. Below 40% → lower difficulty and flag for instructor. The `adaptive_questions` table is already designed to accumulate this data; the adaptation logic is intentionally deferred until enough sessions exist to provide a reliable signal.

**5.2 — Content Versioning**

As tracks get updated, version them (`v1`, `v2` etc.) so learners mid-track don't get broken experiences. The ingest script handles version stamping.

---

## Part 4: The Immediate Priority List

If you were to start tomorrow, in this order:

1. **Run the content audit** — know exactly what content exists vs. what's still legacy HTML. This is 2 hours of work that informs everything else.
2. **Build the ingest pipeline** — this is the unlock that lets content scale without developers.
3. **Finish the legacy migration** — eliminate the legacy layer entirely. It's technical debt that will complicate every future phase.
4. **Ship XP + badges** — visible progress mechanics are what turn learners from visitors into students.
5. **Wire in Supabase auth** — you're already connected. Persistent progress is the step from "cool demo" to "real product."

---

## Summary: Where You Stand

The project is architecturally well ahead of most LMS builds at this stage. The CONSTITUTION, the validation pipeline, and the content collection schema are the kinds of decisions that most projects have to painfully retrofit later — you made them early, correctly.

The gaps are not architectural. They are content volume and operational tooling: getting curriculum into the system at scale without needing a developer on every import, and building the progress mechanics that make learners want to come back.

The path from here to world-class is a series of additive layers on top of a foundation that is already sound.
