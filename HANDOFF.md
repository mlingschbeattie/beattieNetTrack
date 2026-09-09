# beattieNetTrack — Session Handoff

*Updated 2026-09-09. Paste this into a new thread to continue.*

---

## Read these first

`CLAUDE.md` (session brief, track registry, build phases) · `VOICE_AND_TONE.md` (lesson
voice standard) · `CONSTITUTION.md` · `src/content/config.ts` (schema authority) ·
`scripts/validate-tracks.mjs`.

---

## Where the repo is

- Branch: **`master`**, clean.
- **`gitea` and `origin` are both in sync.** Gitea
  (`git.beattietech.local/mbeattie/newnettrack`) is what the LMS deploys from; origin is
  GitHub. Both were brought current on 2026-09-09.
- ⚠️ **`lms.beattietech.local` may still be serving a stale build.** It served one for the
  whole 09-08 session and has not been confirmed redeployed since. **A redeploy and a
  spot-check in production is the single most useful next action.**

### Branch state

- `claude/compassionate-cohen-94996e` — merged into master 09-09 (tech-plus 6.1.7), worktree
  removed, branch deleted.
- `claude/suspicious-kilby` — stale April branch, deleted 09-09; its tech-plus track and
  module definitions were already on master.
- `fix/*` and `refactor/lesson-two-modes` — all merged into master, kept as history.

---

## Content state

Measured 2026-09-09 against the compliance definition below.

| Track | Lessons (compliant) | Quizzes | Labs |
|---|---|---|---|
| tech-plus | **59 / 59** | 58 | 6 |
| pc-technician | **18 / 18** | 39 | 6 |
| network-engineer | **51 / 51** | 61 | 4 |
| cybersecurity-engineer | **12 / 12** | 6 | **0** |
| cybersecurity-foundations | 5 / 6 | 6 | 1 |
| web-developer | 0 / 4 | 0 | 1 |
| python-developer | 0 / 0 | 0 | 0 |
| ai-ml | 0 / 0 | 0 | 0 |

"Compliant" = authored `sections[]` **and** `<Callout>` **and** `## Key Terms`.

**tech-plus is complete at 59/59** — the full FC0-U71 lesson set, Domain 6 contiguous 1–16.

### Counting caveat — utility pages live in the lessons collection

A naive count reports network-engineer as 51/56 and foundations as 5/11. The extra files are
**navigation/utility pages misfiled into `src/content/lessons/`**, not lessons:

- network-engineer: `cheat-sheets` · `download` · `resources` · `review-game` · `study-guides`
- cybersecurity-foundations: `about-class` · `general-skills` · `index` · `learning-tracks` · `tour`

They have no `sections`, no callout, no Key Terms **by design**. Don't "fix" them — either
leave them or move them out of the lessons collection deliberately. The real remaining gap in
foundations is a single lesson: **`intro-to-cybersecurity.mdx`, missing only `## Key Terms`.**

---

## The standard every lesson is held to

1. Authored `sections[]` — 2–4 `keyPoints`, **exactly 2** `check` questions, **exactly 4**
   options each, `correct` 0–3. Schema-enforced; violating it fails content sync.
2. **Two callouts.** `exam` for what CompTIA actually tests. `warn` for the failure that
   *misleads* — the response that makes things worse, not just the wrong answer. That
   second one is where most of the teaching value sits.
3. `## Key Terms` — terms only, `·` separated, no definitions.

Questions test **mechanism, not vocabulary**. Good examples to match the register:
why account lockout barely dents credential stuffing (the password is already correct);
why a link light plus an IP address can still mean the wrong VLAN; why raising AP transmit
power makes coverage worse.

Free text **only** where the literal string is the skill (a binary conversion, a broadcast
address, a closure note). Everything conceptual uses the `choice` validator with a
`rationale`, so a wrong pick teaches.

---

## Suggested next work, in order

1. **Redeploy and verify in production.** Everything below is unverified live.
2. **Labs and quizzes for cybersecurity-engineer.** Its 12 lessons are now fully compliant,
   but it has **6 quizzes for 12 lessons and zero labs** — the widest remaining gap. The
   working legacy interactive demos (sql-injection, xss-demo, cryptography, forensics,
   binary-exploitation, reverse-engineering) are lab material waiting to be wrapped.
3. **`intro-to-cybersecurity.mdx`** — add `## Key Terms`. Small; closes foundations.
4. **A checkpoint quiz for tech-plus 6.1.7 AAA accounting.** Quiz order 7 in
   `tech-plus.security` is deliberately vacant; the lesson shipped without one.
5. **`assessment-1-x-x` quizzes on pc-technician** — 21 quizzes with opaque slugs and
   module assignments that look scattered (`assessment-1-2-5` sits in
   `fundamentals.computing-basics` despite being in the 1-2 hardware group). Never audited;
   may duplicate the 12 properly-named ones.
6. **Duplicate quiz `order` warnings** from `validate:tracks` — three, all on
   network-engineer: `net.fundamentals.addressing` (order 1) and
   `net.implementation.switching` (orders 1 and 2). Where two activities tie on order, a
   tiebreak silently decides sequence. *(The `pct.hardware.components-identification`
   warning noted on 09-08 is gone.)*
7. **web-developer** — 4 lessons, none compliant. Phase E, not urgent.
8. **⚠️ ar / fa / uk translations in `src/i18n/strings.ts` are Claude-drafted and
   unreviewed.** Flagged in the file header. Mr. Beattie's students are the only fluent
   speakers available and are the intended reviewers — this is deliberate, not an oversight.

---

## Bug patterns that recur here — check these first

**Lessons invisible because `order` is missing.** `src/lib/content.ts:215` skips any lesson
without a numeric `order`. Hit three times: 5 misfiled utility pages on network-engineer,
**11 of 12 cybersecurity-engineer lessons**, then the body of `cfs-1-1-2`. If a track looks
emptier than its files suggest, check `order` before anything else.

**Lessons and quizzes share one order namespace per module.** `src/lib/content.ts`
interleaves them by order, lesson before quiz. Inserting a lesson mid-module means shifting
**both** the following lessons and their quizzes — this is what the 6.1.7 merge had to do.

**Static assets shadowing Astro routes.** `public/labs/*` was served at `/labs/<slug>`,
shadowing `/labs/[slug]` and leaving two labs with no workspace, no Submit, no XP. Fixed by
moving to `public/lab-frames/`. **Never put a directory under `public/` that collides with a
route.**

**MDX imports need a blank line after them.** An ESM import glued to the following markdown
500s the whole lesson with an MDXError. Cost nine broken lessons that looked perfect on disk.

**Verify against a production build, not the dev server.** Dev adds ~70 KB of
`data-astro-source-*` attributes, and its Vite dep cache goes stale after import-graph
changes (throws `Cannot read properties of null (reading 'useState')`). Pattern used all
session:

```bash
npm run build
PORT=4399 HOST=127.0.0.1 node ./dist/server/entry.mjs &
curl -s http://127.0.0.1:4399/lessons/<slug>
```

**Check rendered output, not file contents.** Multiple times the files were perfect and the
pages were broken. Grep for `data-testid` or `component-url`, not CSS class names — class
names match the inlined stylesheet and produce false positives.

---

## Gates — run after every content or schema change

```bash
npm run validate:tracks && npm run lint && npm run test:unit
```

Baseline confirmed 2026-09-09: validate passes, **3 duplicate-order warnings only** ·
11 tracks, 72 modules, 352 entries · lint **0 errors, 0 warnings, 7 hints** · **14/14 tests**.

---

## Architecture worth knowing

- **Lessons have two modes: Learn and Read.** Guided was retired — it was 968 lines of
  text-to-speech carousel that received the check questions and never rendered them.
  Read-aloud survived as a control in Read mode.
- **A lesson with no authored sections shows Read only.** It used to fabricate a Learn quiz
  asking "This lesson is titled X — True/False". That fallback is gone; don't reintroduce it.
- **Four lab shapes, all frontmatter-authorable**: `steps` (LabRunner, validators
  `exact`/`oneOf`/`regex`/`choice`), `code` (CodeRunner + a `codeExercises.ts` entry, keyed
  on lab slug), `iframe` (LabFrame — the fragile one), and native React sims (PcAssemblyLab).
  **Prefer `steps`.** Both broken labs found on 09-08 were hand-written iframe labs.
- **`tokens.css` is the single source of colour truth.** Light is a full token redefinition
  under `html[data-theme='light']`. Never hardcode a colour or add a per-component
  `[data-theme='light']` override — that pattern is what made light mode unusable.
- Accessibility panel lives in the top nav (motion, text size, calm mode, collapse long
  lists, readable spacing, underline links), persisted to `beattie_a11y_v1`, applied
  pre-paint.
- Contrast was verified at **0 WCAG AA failures in both themes** on every page touched.
  Keep that bar.

---

## Working style that fitted this project

Mr. Beattie wants the actual problem found, not the symptom patched. Several times the
reported issue ("PC sim is broken", "no way to submit") turned out to be a different and
larger fault underneath — a routing collision, a stale deploy. **Investigate before
building.** Say plainly when something was your own error.
