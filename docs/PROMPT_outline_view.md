# IDE Agent Prompt — Lesson Outline View + Section Micro-Checks
# Save to: docs/PROMPT_outline_view.md in repo
# Use in: VS Code with GitHub Copilot (Claude Sonnet or Opus)
# Run validate:tracks + lint after completion — do NOT commit until both pass clean

---

## Context

beattieNetTrack is an Astro 5 + React 18 + MDX + TypeScript LMS.
Read CONSTITUTION.md and CLAUDE.md before making any change.
Key rules that apply here:
- Static-first: lesson pages render at build time. All new interactivity goes in React islands (client:only).
- One change at a time. No broad refactors. Surgical diffs only.
- Never hardcode colors — use tokens from src/styles/tokens.css.
- validate:tracks must pass after every schema or content change.

---

## Feature Summary

Add an **Outline View** to lesson pages. Lessons currently render as a single long reading view.
This feature adds:
1. A view toggle in the lesson chrome (Reading | Outline)
2. An outline view that shows lessons as collapsible sections with key point bullets
3. A micro-check (2 single-select questions) per section that must pass to mark it complete
4. Shared completion state between reading view and outline view via progressStore

This feature is **additive only**. Existing lessons without the new frontmatter fields render
exactly as before — no outline toggle shown, no regressions.

---

## AUDIT FIRST — Read these files before writing a single line

Before any implementation, audit and report on:

1. `src/content/config.ts`
   - Find the lessons collection schema (z.object definition)
   - Note every existing field name and type
   - Identify where the new `sections` field will be inserted
   - Report the exact import path for zod (z)

2. `src/lib/progressStore.ts`
   - Understand the current ProgressState shape
   - Find how lab/quiz completion is currently stored (key format, data shape)
   - Identify the function signatures for reading and writing progress
   - Report whether there is an existing pattern for per-item sub-step completion

3. `src/pages/lessons/[slug].astro` (or equivalent lesson page file)
   - Find where lesson frontmatter data is destructured
   - Find where the lesson body (Content component) is rendered
   - Identify the layout wrapper and any existing chrome (breadcrumbs, XP display, etc.)
   - Note any existing React islands already on the lesson page

4. `src/components/islands/` — list all files, identify naming conventions

5. `src/styles/tokens.css` — list the CSS custom property names for:
   - Surface/card backgrounds
   - Border colors
   - Primary accent color
   - Muted text color
   - Success/green color (for completed state)

Report findings for all five audits before proceeding. Hold for confirmation.

---

## Constraints — Non-Negotiable

- `sections` field in lesson frontmatter is **optional**. Lessons without it: no outline toggle rendered, zero behavior change.
- The outline toggle is only rendered when `frontmatter.sections` exists and `sections.length > 0`.
- Completion state key format must be consistent with existing progressStore patterns. Do not invent a new storage namespace.
- `OutlineView.tsx` is a React island — `client:only="react"` directive. It receives sections data as a prop (serialized from build-time frontmatter). It does NOT query content collections at runtime.
- Reading view and outline view share the same section completion state. Passing a section's micro-check from outline view marks it done — that state is visible if the student switches to reading view.
- Micro-check: exactly 2 questions per section, single-select (4 options each), both must pass to mark section complete. No penalty for retrying — just re-present the questions on failure with feedback.
- Key points in outline view are author-defined in frontmatter. No auto-extraction from body.
- Section headings in the MDX body use `##` (h2). The outline view matches sections to body content by the `title` field in frontmatter matching the h2 text. Do not parse body MDX — the reading view renders as-is, the outline view is driven entirely by the `sections` frontmatter array.
- All styles use tokens.css custom properties. No hardcoded hex values, no Tailwind classes unless Tailwind is already confirmed in use.
- Run `npm run validate:tracks && npm run lint` after every step. Report output. Do not proceed to next step if either fails.

---

## Implementation Steps

Execute in order. Complete and validate each step before starting the next.

### Step 1 — Schema addition (src/content/config.ts)

Add these three zod types to the lessons collection schema.
Insert them just before the lessons collection definition — do not move or modify any existing types.

```typescript
const sectionCheck = z.object({
  prompt: z.string(),
  options: z.array(z.string()).length(4),
  correct: z.number().int().min(0).max(3),
});

const lessonSection = z.object({
  id: z.string(),
  title: z.string(),
  keyPoints: z.array(z.string()).min(2).max(4),
  check: z.array(sectionCheck).length(2),
});
```

Add to the lessons collection z.object:
```typescript
sections: z.array(lessonSection).optional(),
```

After adding: run `npm run validate:tracks && npm run lint`. Report output. Hold if either fails.

---

### Step 2 — progressStore extension (src/lib/progressStore.ts)

Add section completion tracking. Follow the exact pattern already used for existing completion state.

The new state needed per lesson section:
- Which sections have had their micro-check passed (boolean per section id)
- Store under a key that follows the existing naming convention (audit Step 2 determines this)

Add:
- A type/interface for section completion state (e.g. `SectionProgress: Record<string, boolean>`)
- A function `getSectionProgress(lessonSlug: string): SectionProgress`
- A function `markSectionComplete(lessonSlug: string, sectionId: string): void`
- A function `isSectionComplete(lessonSlug: string, sectionId: string): boolean`

Do not modify any existing functions or state shapes. Append only.

After adding: run `npm run lint`. Report output.

---

### Step 3 — OutlineView island (src/components/islands/OutlineView.tsx)

Create the React island. Props interface:

```typescript
interface SectionCheck {
  prompt: string;
  options: string[];
  correct: number;
}

interface LessonSection {
  id: string;
  title: string;
  keyPoints: string[];
  check: [SectionCheck, SectionCheck];
}

interface OutlineViewProps {
  lessonSlug: string;
  sections: LessonSection[];
}
```

Component behavior:

**Section list:** Renders all sections as collapsible accordion items.
- Each section shows: section number (01, 02...), title, completion status dot + label, chevron
- Status labels: "Done" (check passed), "In progress" (expanded, check not passed), "Not started" (collapsed, not visited)
- Clicking the header toggles open/closed
- Multiple sections can be open simultaneously

**Expanded section shows:**
- 3–4 key point bullets (checkmark icon + text)
- If section complete: a green "Check passed" chip (no action)
- If section not complete: a "Take quick check" chip that opens the micro-check inline

**Micro-check inline (inside expanded section, below key points):**
- Shows one question at a time (Q1 first, then Q2 on correct answer)
- 4 option buttons, single select
- On correct: brief success feedback, advance to Q2 (or complete if Q2)
- On incorrect: brief error feedback ("Not quite — try again"), reset that question, do NOT advance
- On both correct: call `markSectionComplete(lessonSlug, section.id)`, flip chip to "Check passed"
- No score tracking, no XP from micro-check (XP comes from lesson completion as a whole)

**State management:**
- On mount: call `getSectionProgress(lessonSlug)` to restore any previously passed sections
- Sections already passed on mount show "Check passed" immediately, no re-check required

**Styling:**
- Use CSS custom properties from tokens.css only
- Follow the visual language from BNT_UI_DESIGN_SPEC.md if accessible
- Section container: card with border, subtle background on header
- Completed section header: success-tinted left border or dot
- Chevron rotates 180deg when open (CSS transition)
- Option buttons: full-width, border, hover state, selected state with accent color
- Correct answer feedback: green tint
- Incorrect answer feedback: warm/orange tint, no red (this is low-stakes)

After creating: run `npm run lint`. Report output.

---

### Step 4 — Lesson page chrome (src/pages/lessons/[slug].astro)

Add the view toggle and wire OutlineView into the lesson page.

**Toggle bar** (rendered between lesson header and lesson body):
- Only render if `entry.data.sections && entry.data.sections.length > 0`
- Two buttons: "Reading" and "Outline" (icons: align-left, list)
- Toggle state is local UI state — does NOT need to persist across page loads
- Default view: Reading

**View switching:**
- Reading view: existing Content component render, unchanged
- Outline view: `<OutlineView client:only="react" lessonSlug={entry.data.slug} sections={entry.data.sections} />`
- Simple show/hide via a wrapping div — do not unmount/remount OutlineView on toggle (preserves state)
- Toggle uses a small inline script or Astro's client-side approach — confirm with audit findings

**Progress display:**
- Add a section progress indicator in the toggle bar: "X of Y sections complete"
- This reads from the same progressStore state via a separate small island or computed from OutlineView's own state passed upward — use whichever pattern is simpler given the existing architecture

Do not modify: lesson body rendering, layout wrapper, breadcrumbs, XP display, or any other existing chrome. Surgical addition only.

After changes: run `npm run validate:tracks && npm run lint`. Report output. Hold before committing.

---

## Validation Gate (before any commit)

All of the following must be true:

- [ ] `npm run validate:tracks` exits 0, reports 0 errors
- [ ] `npm run lint` (astro check) exits 0, reports 0 errors, 0 warnings
- [ ] A lesson WITH `sections` frontmatter: outline toggle renders, sections collapse/expand, micro-check functions, completion state persists on page reload
- [ ] A lesson WITHOUT `sections` frontmatter: renders identically to pre-feature — no toggle, no regressions
- [ ] TypeScript: no `any` types introduced, all props typed explicitly
- [ ] No hardcoded colors anywhere in new files

Report results for each checkpoint. If any fail, fix and re-run before flagging complete.

---

## Example Frontmatter for Manual Testing

Use this on one existing lesson to test the full flow end-to-end.
Do not create a new lesson file — add `sections` to an existing one.

```yaml
sections:
  - id: why-layers-exist
    title: "Why layers exist"
    keyPoints:
      - "Each layer has one job — isolation makes troubleshooting possible"
      - "Layers build on each other, they do not replace each other"
      - "When something breaks, you can pin the failure to a specific layer"
    check:
      - prompt: "A switch operates at which OSI layer?"
        options:
          - "Layer 1 — Physical"
          - "Layer 2 — Data Link"
          - "Layer 3 — Network"
          - "Layer 7 — Application"
        correct: 1
      - prompt: "What is the primary benefit of the OSI model's layered design?"
        options:
          - "It makes networks faster"
          - "It isolates problems to a specific layer"
          - "It reduces the number of cables needed"
          - "It replaces TCP/IP"
        correct: 1
  - id: lower-layers
    title: "The lower layers (1–3)"
    keyPoints:
      - "L1: raw bits only — hubs, cables, NICs, no addressing"
      - "L2: MAC addresses let switches deliver frames locally"
      - "L3: IP addresses let routers move packets across networks"
    check:
      - prompt: "Which device operates at Layer 2 and uses MAC addresses to forward traffic?"
        options:
          - "Hub"
          - "Router"
          - "Switch"
          - "Firewall"
        correct: 2
      - prompt: "What type of address does a router use to make forwarding decisions?"
        options:
          - "MAC address"
          - "IP address"
          - "Port number"
          - "Serial number"
        correct: 1
```

---

## What NOT to Do

- Do not auto-generate key points from lesson body text
- Do not add a third view mode or any feature not described above
- Do not modify existing quiz or lab completion logic
- Do not change any existing lesson page behavior for lessons without sections
- Do not introduce new npm packages without flagging and getting confirmation first
- Do not commit until the validation gate above is fully green