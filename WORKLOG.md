# BeattieNetTrack — Work Log
# Updated as issues are identified and resolved.
# Format: [STATUS] [TYPE] Description — Notes

## STATUS KEY
# OPEN     — identified, not yet started
# WIP      — actively being worked
# DONE     — resolved and committed
# DEFERRED — intentionally postponed (phase dependency noted)
# WONTFIX  — decided not to address

## TYPE KEY
# BUG      — something broken
# FEAT     — new feature or enhancement
# CONTENT  — lesson/quiz/PDF content work
# CLEANUP  — housekeeping, organization
# DEBT     — technical debt to address later

---

## OPEN ITEMS

### FEAT — Quiz ELI5 Explanations
**Logged:** 2026-03-25
**Priority:** High
**Description:** After a student submits a quiz, incorrect answers should display a plain-language
"Here's why" explanation of why the correct answer is right and why the chosen answer is wrong.
**Implementation plan:**
1. Add optional `explanation` field to quiz schema in `src/content/config.ts`
   - Field is optional — existing quizzes without it degrade gracefully
   - Format: plain string, 2-4 sentences written for a high school student
2. Update `src/components/islands/QuizRunner.tsx` to display explanations on results screen
   - Only show for incorrect answers
   - Style as a distinct callout (e.g., light blue background, "Here's why:" label)
3. Update all future quiz-writing prompts to include `explanation` per question
4. Backfill explanations into existing quizzes (lower priority — do new ones first)
**Dependencies:** Schema change must happen before any new quizzes are authored with explanations
**Note:** Phase 5 AI question engine also auto-generates explanations — this is the manual
precursor. Keep format compatible.

---

### FEAT — Lesson Coverage Guarantee
**Logged:** 2026-03-25
**Priority:** High
**Description:** Every lesson must explicitly cover all topics tested in its corresponding quiz.
Currently quizzes and lessons are authored independently — gaps are possible.
**Implementation plan:**
1. Add quiz topic checklist to every lesson-writing prompt going forward
2. For existing lessons where quiz was written after: spot-check coverage and flag gaps
3. Consider adding a "Learning Objectives" section to lesson frontmatter listing key topics
   — this becomes the source of truth for both lesson content and quiz questions
**Affected tracks:** Tech+ (quizzes written before lessons — must sync), future tracks

---

### CLEANUP — Misplaced PCT Quizzes in Tech+ Directory
**Logged:** 2026-03-25
**Priority:** Medium
**Description:** `src/content/quizzes/tech-plus/` contains 20 files (assessment-1-1-1.mdx through
assessment-1-4-5.mdx) that are PC Technician quizzes, not Tech+ quizzes. They reference
`pct.*` moduleIds and were placed here incorrectly during an earlier session.
**Fix:** Move all 20 files to `src/content/quizzes/pc-technician/` and verify validate passes.
**Note:** These do not currently cause build failures because the pct moduleIds are valid.
Low urgency but creates confusion when auditing quiz coverage.

---

### BUG — Route Conflict Warning: /labs/code-basics
**Logged:** 2026-03-25
**Priority:** Low
**Description:** Build output shows:
  `[WARN] Could not render /labs/code-basics from route /labs/[slug] as it conflicts
  with higher priority route /labs/code-basics`
Both `src/pages/labs/code-basics.astro` (static) and `src/pages/labs/[slug].astro` (dynamic)
match the `/labs/code-basics` URL. The static route wins, which is probably correct behavior,
but the warning should be eliminated.
**Fix:** Remove `src/pages/labs/code-basics.astro` if `[slug].astro` handles it correctly,
or add code-basics to an exclusion list in the dynamic route.
**Note:** Pre-existing issue, not introduced recently. Does not affect functionality.

---

### CONTENT — Tech+ Quizzes Need Explanation Fields
**Logged:** 2026-03-25
**Priority:** Medium (after schema change above)
**Description:** All 58 Tech+ quizzes being authored currently have no `explanation` field.
Once the schema supports it and QuizRunner displays it, these need to be backfilled.
**Approach:** Re-run quiz generation with explanation field included rather than editing
58 files by hand.

---

### CONTENT — Tech+ Lessons Not Yet Written
**Logged:** 2026-03-25
**Priority:** High — next major content phase
**Description:** Tech+ has 58 lessons ingested (Phase B complete) and quizzes being authored,
but lesson content quality and quiz coverage alignment needs verification.
**Phase C tasks per audit:**
- Verify 1.2.1 Binary covers decimal notation
- Verify 6.1.7 content on CYBER.ORG (missing lesson)
- Full coverage audit: every quiz topic must appear in its lesson
**After Phase C:** Author PDF units for all 58 Tech+ lessons

---

### CONTENT — Tech+ PDFs Not Yet Generated
**Logged:** 2026-03-25
**Priority:** Medium (after quizzes complete)
**Description:** 0 PDF directories exist for Tech+ track. Need to add 58 UNITS entries to
`make_resource_pdfs.py` and generate guided notes + answer keys.
**Output directory:** `public/resources/tech-plus/`
**Approach:** Same pipeline as Network Engineer and PC Technician. Use Sonnet prompt.

---

### DEFERRED — Supabase Integration (Phase 3)
**Logged:** 2026-03-25
**Priority:** High (when ready)
**Description:** Replace localStorage-only progress with Supabase database. Students lose
progress when switching devices or clearing browser history.
**Dependencies:** Requires stable multi-track LMS first. Target: after 3 tracks complete.
**Spec:** See `docs/LMS_MASTER_PLAN.md` and `PHASE5_ADAPTIVE_ENGINE.md`
**Key files:** `src/lib/coachClient.ts` (stub, do not touch until Phase 3)

---

### DEFERRED — Phase 4: Live Lab Environments
**Logged:** 2026-03-25
**Priority:** Future
**Description:** Replace simulated terminal labs with real Docker containers. Students run
actual commands against real systems.
**Dependencies:** Phase 3 (Supabase) must be complete first.

---

### DEFERRED — Phase 5: AI Question Generation Engine
**Logged:** 2026-03-25
**Priority:** Future
**Description:** Use Anthropic API to generate novel CompTIA practice questions on demand.
Instructor reviews and approves before going live.
**Dependencies:** Phase 3 complete, app fully stable.
**Spec:** `PHASE5_QUESTION_ENGINE.md`
**Key files:** `src/lib/coachClient.ts` (stub already wired)

---

## DONE ITEMS

### DONE — Network Engineer Track Complete
**Resolved:** 2026-03-25
**Description:** All 44 lessons, 60 quizzes, 51 PDF directories. Build passes clean.

### DONE — PC Technician Track Complete
**Resolved:** 2026-03-25
**Description:** All 15 lessons, 15 quizzes, 15 PDF directories. Build passes clean.

### DONE — Tech+ Lessons Ingested (Phase B)
**Resolved:** 2026-03-25
**Description:** 58 lessons across 6 domains ingested. Build passes clean.

### DONE — Empty Module Stubs Fixed
**Resolved:** 2026-03-25
**Description:** `net.security.infrastructure.mdx` and `net.security.wireless.mdx` were empty
(no frontmatter), causing build failure. Both repaired with correct stub content.

### DONE — Misplaced Module Stubs Removed from lessons/
**Resolved:** 2026-03-25
**Description:** Several `pct.*` and `net.*` dot-notation module stub files were incorrectly
placed in `src/content/lessons/`. All moved to correct `src/content/modules/` locations.

### DONE — make_resource_pdfs.py UNITS Dict Backfilled
**Resolved:** 2026-03-25
**Description:** Script now contains all 9 Network Engineer units (1.1.1-2.5.1) and all 15
PC Technician units. Script is authoritative source for regenerating any unit on demand.

---

## DECISIONS LOG
# Architectural and content decisions made — recorded to avoid re-debating them.

### DECISION — Lessons authored before quizzes going forward
**Date:** 2026-03-25
**Decision:** Standard workflow is lesson → quiz → PDF. Tech+ was an exception (lessons ingested
from CYBER.ORG source, quizzes authored after). For all future original tracks, lesson is
written first, quiz is authored against lesson content.

### DECISION — Quiz explanations: manual first, AI later
**Date:** 2026-03-25
**Decision:** Implement `explanation` field in quiz schema manually for near-term.
Phase 5 AI engine will auto-generate explanations at scale. Keep format compatible.

### DECISION — RAID is not a backup (content standard)
**Date:** 2026-03-25
**Decision:** Every lesson and quiz that covers RAID must explicitly state "RAID is not a backup."
This is a critical misconception that costs people data.

### DECISION — Use Sonnet for content generation, Opus for architecture
**Date:** 2026-03-25
**Decision:** Claude Sonnet for all content generation (lessons, quizzes, PDFs) — structured
output, clear templates, fast. Claude Opus for complex reasoning tasks: architecture decisions,
debugging strange validation errors, designing new features, writing prompts.
