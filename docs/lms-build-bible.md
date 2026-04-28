# LMS Build Bible

> Source of truth for build order, architecture decisions, and deployment runbook.
> Read this before starting any new phase.

---

## Phase Status

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1 | Foundation | ✅ COMPLETE 2026-04-28 |
| Phase 2 | Storage | ✅ COMPLETE 2026-04-28 |
| Phase 3 | Lab Shell | ✅ COMPLETE 2026-04-28 |
| Phase 4 | First lab (04-RAID) | ✅ COMPLETE 2026-04-28 |
| Phase 5 | All 8 labs ported | ✅ COMPLETE 2026-04-28 |
| Phase 6A | CIS beacon wiring | ✅ COMPLETE 2026-04-28 |
| Phase 6B | Teacher grading | ✅ COMPLETE 2026-04-28 |
| Phase 7 | CIS Portal | 🔜 NEXT |
| Phase 8 | Translation | ⬜ QUEUED |
| Phase 9 | Polish | ⬜ QUEUED |

---

## Build Order

### Phase 1 — Foundation ✅

Core Astro + MDX + React islands stack. Static-first output, content collections wired.

### Phase 2 — Storage ✅

`localStorage`-backed progress store (`beattie_progress_v1`). XP, streaks, lesson/lab/quiz completion state.

### Phase 3 — Lab Shell ✅

`WorkspaceLayout.astro` — split-pane workspace with instruction panel, activity area, right panel (checks/hints/notes/coach tabs). `AppShell.astro` for lesson pages.

### Phase 4 — First lab (04-RAID) ✅

End-to-end lab pipeline validated: MDX frontmatter → content collection → `[slug].astro` → `LabRunner.tsx` → check/submit cycle → XP award.

### Phase 5 — All 8 labs ported ✅

All lab types functional: terminal-simulator labs (`TerminalSimulator.tsx`), code-runner labs (`CodeRunner.tsx`), drag-and-drop hardware labs (`PcAssemblyLab.tsx`), and iframe legacy labs.

Active labs in `src/content/labs/`:
- `code-basics.mdx`
- `network-terminal-basics.mdx`
- `pc-assembly.mdx`
- `pc-tech-legacy-hardware-lab.mdx`
- `terminal-basics.mdx`

---

### Phase 6 — CIS Integration ✅ COMPLETE 2026-04-28

#### 6A — CIS Beacon Wiring

**Purpose:** Report active-engagement time per CIS domain as students work in labs. Beacon fires every 30 seconds while the student is active; idle time (>3 minutes without keydown/click/scroll) is accumulated and included in the payload but no beacon is sent during idle windows.

**Files changed:**

- `src/types/lab.ts`
  - Added `DomainMapping` interface (`domainId: string`, `weight: number`)
  - Added `domains: DomainMapping[]` to `LabMeta` interface

- `src/lib/cis/beacon.ts`
  - `startBeaconSession({ domainIds, contentType, contentId, apiUrl })` — returns cleanup function
  - 30-second interval (`BEACON_INTERVAL_MS = 30_000`)
  - 3-minute idle threshold (`IDLE_THRESHOLD_MS = 3 * 60 * 1000`)
  - Idle accumulation: `idleSecondsTotal` and `idleCount` tracked, sent with each active beacon
  - `credentials: 'include'` on all fetch calls
  - Silent fail on network error — beacon loss is acceptable
  - Activity signals: `keydown`, `click`, `scroll`

- `src/components/BeaconEmitter.tsx`
  - Null-rendering React island (returns `null`)
  - Single `useEffect` on mount — calls `startBeaconSession`, returns cleanup to stop interval on unmount
  - Props: `domainIds: string[]`, `contentId: string`, `apiUrl: string`
  - Early-exit if `apiUrl` is empty or `domainIds` is empty

- `src/pages/labs/[slug].astro`
  - `<BeaconEmitter>` mounted inside the `WorkspaceLayout` branch
  - Passes lab `domains` array as `domainIds`, lab `slug` as `contentId`, `PUBLIC_API_URL` env var as `apiUrl`

- `src/content/labs/*.mdx` — `domains` arrays added to all 5 lab frontmatter files:
  - `code-basics.mdx` → `aplus2.os`
  - `network-terminal-basics.mdx` → `netplus.troubleshooting`, `nocti.networking`
  - `pc-assembly.mdx` → `aplus1.hardware`, `nocti.hardware`
  - `pc-tech-legacy-hardware-lab.mdx` → `aplus1.hardware`, `nocti.hardware`
  - `terminal-basics.mdx` → `aplus2.os`, `nocti.os`

- `src/content/config.ts`
  - `domains` field added to the labs Zod schema

- `src/env.d.ts`
  - `PUBLIC_API_URL: string` added to `ImportMetaEnv`

- `.env` / `.env.example`
  - `PUBLIC_API_URL=https://api.beattietech.local`

#### 6B — Teacher Grading

**Purpose:** Allow authenticated teachers to view student lab answers and submit a numeric score (0–100) per student, which triggers the CIS grade event on the API.

**Files changed:**

- `src/components/GradeEntry.tsx`
  - On mount: fetches `GET /api/lms/labs/:labId/answers` with `credentials: 'include'`
  - Renders per-student score input (number, 0–100) + "Grade" button
  - On submit: `POST /api/lms/labs/:labId/grade` with `{ studentId, score }`
  - Per-student states: `idle` | `saving` | `saved` | `error`
  - `saved` → success badge; `error` → error badge
  - Loading and fetch-error states render separate card UI

- `src/pages/labs/[slug]/grade.astro`
  - Server-rendered, teacher-gated page
  - Reads `Remote-Groups` header to verify teacher role
  - Redirects non-teachers
  - Mounts `GradeEntry` client island

#### Lab completion events

- `src/components/LabRunner.tsx`
  - In the `allDone` branch, fires `lms.lab_completed` custom event with full CIS payload:
    ```
    { domains, contentType: 'lab', contentId, score, maxScore }
    ```

#### Known gaps

- **iframe labs** (`pc-assembly`, `pc-tech-legacy-hardware-lab`) have no client-side completion signal. The beacon covers active engagement time. Teacher grade submission via the grading endpoint (`/grade`) triggers the CIS event for these labs.

---

### Phase 7 — CIS Portal 🔜 NEXT

New application: `cis.beattietech.local` (port 4328).

**Student view:**
- Readiness overview per cert track
- Per-domain breakdown showing time-on-content vs. competency thresholds
- Recommendations for weak domains

**Teacher view:**
- Cohort heat map — domain coverage by student
- Student drill-down
- Score override

---

### Phase 8 — Translation ⬜ (previously Phase 7)

- LibreTranslate integration
- ES / UK / AR language support
- RTL layout for Arabic
- Bilingual answer persistence

---

### Phase 9 — Polish ⬜ (previously Phase 8)

- Mobile tab view
- Print stylesheet

---

## Deployment

### Stack

| Component | Value |
|-----------|-------|
| Runtime | Node 20 (Alpine slim, non-root `astro` user) |
| Server | Astro standalone (`output: 'server'`, `@astrojs/node`) |
| Port | 4321 |
| Container | `beattie-lms` |
| Docker network | `beattie` (external: true) |

### Docker network — IMPORTANT

The compose network **must** be `beattie`, not `beattie-net`.  
Using `beattie-net` caused a deployment failure on 2026-04-28.

Current `docker-compose.yml`:
```yaml
networks:
  beattie:
    external: true
```

Create the network on the rack server if it does not exist:
```bash
docker network create beattie
```

### CI/CD

Gitea Actions CI workflow is **disabled**.  
`.gitea/workflows/ci.yml` contains `on: []` because the rack server runner cannot reach `github.com` to pull `actions/checkout`.

**Manual deploy process — run in order:**

1. `pnpm lint` — must pass
2. `pnpm build` — must pass (includes `validate:tracks` prebuild)
3. Push to Gitea master:
   ```bash
   git push gitea master
   ```
4. On the rack server:
   ```bash
   cd /opt/beattie/lms
   git pull
   docker compose up -d --build
   ```

### Credential caching

Run once on the rack server to avoid repeated credential prompts:
```bash
git config credential.helper store
```

### Environment variables

| Variable | Value |
|----------|-------|
| `PUBLIC_API_URL` | `https://api.beattietech.local` |
| `HOST` | `0.0.0.0` (set in Dockerfile) |
| `PORT` | `4321` (set in Dockerfile) |

---

## Architecture Notes

### Content collections

All content lives in `src/content/`. Schema authority: `src/content/config.ts`.  
Run `npm run validate:tracks` to verify all activities map to a real `track` + `moduleId`.

### Progress storage

Key: `beattie_progress_v1` in `localStorage`.  
Progress updates broadcast via `window.dispatchEvent(new CustomEvent('progress-updated'))`.  
Islands subscribe in `useEffect` and clean up the listener on unmount.

### SSR dynamic routes

All `[slug].astro` pages resolve content by `Astro.params.slug` at request time.  
`getStaticPaths()` is present for type safety only — it is ignored in `output: 'server'` mode (expected, non-blocking warning).

### CIS beacon flow

```
Student opens lab
  → BeaconEmitter mounts (useEffect)
    → startBeaconSession() starts 30s interval
      → every 30s: check last activity timestamp
        → active: POST /api/cis/beacon with domainIds + idleSecondsTotal
        → idle (>3 min): accumulate idle time, skip POST
  → student leaves / tab closes
    → useEffect cleanup → clearInterval + removeEventListeners
```
