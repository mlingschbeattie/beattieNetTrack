# CONSTITUTION.md

Beattie Net Track — LMS Constitution v2  
Effective: 2026-02-23

This repository is governed by the contracts below. All changes must comply.

If a proposed change conflicts with any Constitutional Contract, the change must be rejected or revised.

---

## 0) Authority Order

1. This Constitution (`CONSTITUTION.md`)
2. Content Contracts (Astro Content Collections schemas in `src/content/config.ts`)
3. Validation Contract (`scripts/validate-tracks.mjs` and `npm run validate:tracks`)
4. Deterministic Regression Suite (Playwright + unit tests)
5. Repository source code (Astro/TS/React)

When in conflict, higher authority wins.

---

## 1) Static-First Architecture Contract

This LMS is Astro 5 with **static output**.

- Core learning content (tracks/modules/activities) must render at build time.
- No client-side router.
- No runtime fetching required to display core learning structure.
- React islands are allowed only for interaction, never for primary structure or navigation.

Any change that requires SPA behavior is prohibited.

---

## 2) Determinism Contract

The system must be reproducible and stable across machines and CI.

- No randomness without explicit seeding.
- All ordering must be explicit and stable.
- No tests that rely on timing hacks or race conditions.
- Progress-driven UI must render deterministically from persisted state (e.g., `localStorage`) without layout thrash.
- Any regression must be reproducible via the existing test commands.

If behavior is not reproducible, the change is invalid.

---

## 3) Change Scope Contract

- One feature or fix per change.
- Small, surgical diffs only.
- No broad refactors unless explicitly authorized.
- Prefer additive changes over replacements.

Scope creep is a defect.

---

## 4) Dependencies and Complexity Contract

- No new npm dependencies without explicit approval.
- No changes to `astro.config.*` or `package.json` without explicit approval.
- No new React/client-side hydration islands without explicit justification.
- No new routes unless strictly required.

Complexity must be intentional and justified.

---

## 5) Design System Contract

UI must reuse the existing layout/component system.

- Reuse existing Astro layouts (e.g., AppShell/BaseLayout/WorkspaceLayout or current equivalents).
- Reuse existing UI components (cards, sections, callouts, activity cards) before creating new ones.
- No one-off styling patterns per page.
- Prefer existing CSS architecture over introducing new CSS files.
- Avoid inline styles in components unless strictly necessary and isolated.

Consistency is enforced by reuse, not by manual styling.

---

## 6) Navigation Integrity Contract

- Do not remove or rename pages/routes without confirming no references break:
  - content references
  - tests
  - internal links
  - legacy links (when applicable)
- New activity pages must be discoverable through the track/module hierarchy (not orphan routes).
- Links must use stable canonical routes (avoid fragile file-relative patterns when a canonical route exists).

Navigation must remain stable and predictable.

---

## 7) Scroll Model Contract

Default behavior is document-only scrolling (`html/body`).

- Do not introduce nested scroll containers in workspace shells.
- Do not add global overflow locks (e.g., `100vh` + `overflow:hidden`) without explicit approval.
- Nested scrolling is allowed only for true viewport components (terminal/editor panes) and must be explicitly scoped and tested at desktop and mobile breakpoints.

Scroll regressions are functional regressions.

---

## 8) Hydration Contract

React islands must follow these rules:

- Islands exist only for interactivity.
- Islands must not change primary page structure.
- Islands must avoid CLS: reserve layout space prior to hydration.
- Islands must remain minimal and isolated.

Do not simulate SPA behavior with islands.

---

## 9) Track System Contract

The LMS is content-driven via Astro Content Collections.

- Every activity entry (labs, quizzes, activities, tours, and related activity collections) must declare:
  - `track`
  - `moduleId` (canonical metadata field)
- `moduleId` must resolve to a real modules collection entry.
- `/tracks` is the primary track hub.
- `/tracks/legacy` is archival/secondary only.

If an activity is not correctly mapped into track/module, it is invalid.

---

## 10) Validation Contract

Validation is mandatory.

- `npm run validate:tracks` must pass before build/CI is considered green.
- Validation must fail (non-zero exit) on missing or mismatched `track`/`moduleId` associations.
- Legacy `labPath` references under `/legacy/...` must resolve to real files in `public/legacy` (when present).
- Validation must run as part of CI gating.

Validation is an enforcement mechanism, not an optional check.

---

## 11) QA Gate Contract

Before a change is considered complete:

- Links and navigation verified (no orphan routes).
- Layout consistency verified against the existing design system.
- `npm run validate:tracks` passes.
- `npm run lint` passes.
- `npm run test:unit` passes.
- `npm run build` passes.
- `npm run test:visual` (Playwright) passes.
- If the change affects hydrated UI, verify no CLS regressions on `/tracks/*`.

If any gate fails, the change is not complete.

---

## 12) Performance Measurement Contract

- Lighthouse runs must use a clean Chrome profile with extensions disabled.
- Treat extension-injected audit noise as non-actionable unless reproducible in a clean profile.
- Track CLS regressions on `/tracks/*` and prioritize layout reservation for hydrated UI slots.

Performance regressions are treated as functional regressions.

---

## 13) Educational Safety and Ethics Contract

Security content must be educational and clearly labeled.

- Include ethical use warnings for offensive techniques.
- Avoid real-world exploitation instructions outside of explicit lab/workspace/CTF context.

The LMS teaches responsible defense and understanding.

---