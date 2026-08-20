# Neurodivergent UX Contract Backlog

Status: Draft for execution
Owner: Product + LMS engineering
Source of truth: CONSTITUTION.md section 16
Last updated: 2026-06-01

## Goal

Implement the Neurodivergent UX Contract across student-facing LMS flows with measurable outcomes:
- Lower decision load on first view
- Faster resume after interruption
- Clear next action on every page
- Reduced sensory overload by default

## Guardrails

All backlog work must comply with:
- Static-first architecture contract
- Determinism contract
- Change scope contract
- Dependencies and complexity contract
- QA gate contract

Implications:
- No new npm dependencies without approval
- No broad refactor in one PR
- No new routes unless required
- All student UX changes must pass validate, lint, unit, build, visual checks

## Scope

In scope:
- Student-facing pages and shells
- Dashboard, tracks, lessons, workspace, quizzes, labs, tours
- Shared layout components and islands that affect attention, context, and re-entry

Out of scope for this program:
- Instructor analytics feature expansion
- Supabase sync architecture changes
- AI coach feature implementation

## Current Findings Summary

High-impact gaps identified:
- Continue Learning entry point is not implemented
- Workspace exposes multiple competing support systems at once
- Decorative motion and random animation run in default shell
- Navigation/status density is high on attention-critical screens
- Quiz feedback can become visually dense after submission

## Backlog Structure

Priority labels:
- P0: Must ship first
- P1: Ship after P0 stabilizes
- P2: Polish and sustainment

Sizing labels:
- S: 1 to 2 days
- M: 3 to 5 days
- L: 1 to 2 weeks

## P0 Backlog (Foundation)

### NUX-001 Implement Continue Learning (P0, M)
Why:
- Re-entry is a core contract promise.

Scope:
- Implement Continue Learning island behavior and rendering.
- Show one primary resume action and one secondary option.
- Include last activity context and deterministic next step.

Primary files:
- src/components/islands/ContinueLearning.tsx
- src/pages/index.astro
- src/lib/progressStore.ts

Acceptance criteria:
- Dashboard always has exactly one obvious primary next action.
- If progress exists, resume card appears with last known location.
- If no progress exists, start path appears with clear first step.
- Works with localStorage-only mode and no runtime fetch dependency.

### NUX-002 Calm Defaults in App Shell (P0, M)
Why:
- Default sensory load must be low and interruption-safe.

Scope:
- Disable non-essential animated background by default.
- Keep visual clarity without random or decorative motion.
- Add an optional persistent preference for enhanced visuals if retained.

Primary files:
- src/layouts/AppShell.astro
- src/styles/global.css

Acceptance criteria:
- No decorative animation runs by default on student pages.
- Any optional animation is opt-in and persisted.
- No regressions in layout or CLS.

### NUX-003 Single Support Model for Workspace (P0, L)
Why:
- Current workspace has competing controls, tabs, drawers, and panel states.

Scope:
- Choose one support model for student workflow.
- Keep support surfaces progressive and collapsed by default.
- Remove duplicate result surfaces and duplicate progress messaging.

Primary files:
- src/layouts/WorkspaceLayout.astro
- src/components/islands/RightPanel.tsx
- src/components/workspace/BottomBar.astro
- src/lib/panelStore.ts

Acceptance criteria:
- Student workspace initial state presents one dominant task action.
- Secondary tools are hidden until explicitly opened.
- Checks, hints, and notes remain available without competing with primary task flow.
- Disabled placeholder controls are removed from primary flow.

### NUX-004 Route-Aware Navigation Density (P0, M)
Why:
- Persistent nav complexity is too high for attention-critical views.

Scope:
- Define route-level density rules.
- Keep richer nav on dashboard and track pages.
- Minimize persistent nav/status artifacts in workspace contexts.

Primary files:
- src/components/Navbar.astro
- src/components/Sidebar.astro
- src/layouts/AppShell.astro

Acceptance criteria:
- Workspace routes show minimal persistent navigation chrome.
- Learner always has where-am-I and what-next cues.
- No loss of discoverability for essential navigation paths.

## P1 Backlog (Flow and Feedback)

### NUX-005 Quiz Feedback Rhythm Cleanup (P1, M)
Why:
- Current results reveal can feel dense and abrupt.

Scope:
- Keep one question at a time.
- Stage feedback in calmer sequence.
- Ensure explanation language is direct and low ambiguity.

Primary files:
- src/components/QuizRunner.tsx
- src/styles/global.css

Acceptance criteria:
- Feedback sequence does not overload with simultaneous signals.
- Correctness, explanation, and next action are visually ordered.
- Retake and submit states remain deterministic and persistent.

### NUX-006 Context Integrity Pattern (P1, S)
Why:
- Users must always know location, state change, and next step.

Scope:
- Standardize compact page-level context header pattern.
- Apply to lessons, labs, quiz, and workspace pages.

Primary files:
- src/pages/lessons/[slug].astro
- src/pages/labs/[slug].astro
- src/pages/quizzes/[slug].astro
- src/pages/workspace/[type]/[slug].astro

Acceptance criteria:
- Each page explicitly shows: location, current state, immediate next action.
- Language is concrete and non-metaphorical.

### NUX-007 Interruption Recovery Hardening (P1, M)
Why:
- Recovery from interruptions is a contract requirement.

Scope:
- Audit and normalize persisted state keys and restore behavior.
- Ensure resume context is available from dashboard and page-level views.

Primary files:
- src/lib/progressStore.ts
- src/lib/checksStore.ts
- src/components/islands/RightPanel.tsx
- src/components/QuizRunner.tsx

Acceptance criteria:
- Reload or return restores place and action context in all core activity types.
- Resume never depends on in-memory state only.

## P2 Backlog (Governance and Sustainment)

### NUX-008 Neurodivergent UX QA Checklist (P2, S)
Why:
- Contract compliance must be reviewable and repeatable.

Scope:
- Add a PR checklist section for section 16 compliance.
- Add reviewer prompts for decision-count and sensory-load checks.

Primary files:
- .github/pull_request_template.md or equivalent
- docs/NEURODIVERGENT_UX_BACKLOG.md

Acceptance criteria:
- Every student-facing UX PR includes explicit contract checks.

### NUX-009 Contract Regression Tests (P2, M)
Why:
- Prevent drift after initial improvements.

Scope:
- Add Playwright tests for calm defaults and resume behavior.
- Add assertions for default collapsed support surfaces.

Primary files:
- tests/*.spec.ts
- playwright.config.ts

Acceptance criteria:
- Test suite fails on regressions to core contract behaviors.

### NUX-010 UX Language Standardization (P2, S)
Why:
- Contract requires concrete, direct language.

Scope:
- Inventory student-facing labels and status text.
- Replace ambiguous wording and novelty labels.

Primary files:
- src/components/**/*.astro
- src/components/**/*.tsx
- src/pages/**/*.astro
- VOICE_AND_TONE.md

Acceptance criteria:
- Primary actions and statuses use plain, direct wording.
- No placeholder or vague labels in student primary flow.

## Cross-Cutting Considerations

### Accessibility
- Keyboard-first flow for all primary actions
- Focus management for overlays, drawers, and tab changes
- Clear status announcements for dynamic updates

### Performance
- No CLS regression on /tracks and workspace routes
- No unnecessary hydration for static content
- Preserve static-first build behavior

### Determinism
- No random state-driven UX behavior in default mode
- Explicit ordering for cards, modules, and actions
- Persistent preference keys are stable and versioned

### Safety and Ethics
- Keep educational framing and low-ambiguity language in cyber content contexts
- Do not introduce manipulative streak patterns or urgency patterns

## Rollout Plan

### Wave 1 (2 weeks)
- NUX-001
- NUX-002

Exit criteria:
- Continue Learning works end-to-end
- Calm default shell is in place
- QA gates green

### Wave 2 (2 to 3 weeks)
- NUX-003
- NUX-004
- NUX-005

Exit criteria:
- Workspace has one support model
- Nav density tuned by route context
- Quiz feedback rhythm simplified
- QA gates green

### Wave 3 (1 to 2 weeks)
- NUX-006
- NUX-007
- NUX-008
- NUX-009
- NUX-010

Exit criteria:
- Context and interruption recovery are consistent
- Regression protections are active
- PR checklist enforcement in place

## Tracking Template

Use this template for each backlog item in WORKLOG:

- ID:
- Status: OPEN | WIP | DONE | DEFERRED
- Priority: P0 | P1 | P2
- Owner:
- Scope summary:
- Acceptance criteria:
- Dependencies:
- Test evidence:
- Risks and rollback:

## Suggested First Execution Slice

Start with this minimal high-value slice:
- NUX-001 first-pass implementation
- NUX-002 remove decorative default motion
- NUX-003 design decision document selecting one workspace support model

This yields visible learner impact quickly while keeping scope controlled.
