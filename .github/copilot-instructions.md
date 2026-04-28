---
name: BeattieNetTrack Ruleset
description: Astro 5 LMS cybersecurity labs per CONSTITUTION.md
applyTo: "**/*.{astro,mdx,js,ts,jsx,tsx,Dockerfile}"
globs: ["src/content/**","src/components/**"]
---

# BeattieNetTrack Copilot Ruleset

**Read first:** `#file CONSTITUTION.md` (authority), `#file src/content/config.ts` (schema), `#file PROMPT_GUIDE-10.md` (phases).

**ALWAYS enforce:**
- Static‑first: No SSR/SPA, islands only (no CLS).
- Content: Every lab/quiz/lesson → track/moduleId (validate: `npm run validatetracks`).
- Security: OWASP, no secrets/eval, helmet/JWT.
- Docker: Alpine, non‑root, multi‑stage.
- XP: Per frontmatter, localStorage `beattieprogressv1`.
- Output: Git diff, JSON `{success:true, data:...}`.

**Node/Astro:**
- Node 20, `npm ci`, `npm run test:ci`.
- MDX collections: Explicit `order`, `track`, `moduleId`.
- Islands: `client:load`, reserve layout.

**NEVER:** New deps/routes without `#file CONSTITUTION.md` approval, duplicate content, break determinism.

**Phases:** `#file BeattieNetTrack_LMS_Roadmap-4.md` → Phase 0 audit first.

Test: "Per rules, add tech‑plus track stub."
