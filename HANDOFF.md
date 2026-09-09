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
| cybersecurity-engineer | **12 / 12** | 6 (one checkpoint per module — complete) | **0** |
| cybersecurity-foundations | **5 / 5** | 6 | 1 |
| web-developer | 0 / 4 | 0 | 1 |
| python-developer | 0 / 0 | 0 | 0 |
| ai-ml | 0 / 0 | 0 | 0 |

"Compliant" = authored `sections[]` **and** `<Callout>` **and** `## Key Terms`.

**tech-plus is complete at 59 lessons and 59 quizzes** — the full FC0-U71 set, Domain 6
contiguous 1–16 on both sides.

**cybersecurity-engineer's quiz count is not a gap.** It uses one checkpoint quiz per module,
all six modules covered, each at order 10 so it lands after that module's lessons. Six
quizzes for twelve lessons is the design, not a shortfall. Its real gap is **labs: zero**.

### Counting caveat — utility pages live in the lessons collection

A naive count reports network-engineer as 51/56 and foundations as 5/11. The extra files are
**navigation/utility pages misfiled into `src/content/lessons/`**, not lessons:

- network-engineer: `cheat-sheets` · `download` · `resources` · `review-game` · `study-guides`
- cybersecurity-foundations: `about-class` · `general-skills` · `index` · `learning-tracks` · `tour`

They have no `sections`, no callout, no Key Terms **by design**, and **no `order`** — which is
exactly why `content.ts` skips them and they never render as lessons. Don't "fix" them; either
leave them or move them out of the lessons collection deliberately.

The sixth foundations file, `intro-to-cybersecurity.mdx`, is **`draft: true` and explicitly
superseded by `cfs-1-1-1-cia-triad`**. It does not need Key Terms. **cybersecurity-foundations
is complete at 5/5.**

⚠️ **Latent defect in that draft file.** It sits at order 1 in
`cfs.fundamentals.security-concepts`, colliding with the real `cfs-1-1-1-cia-triad`, and its
`sections[]` are **OSI networking sections** ("Why layers exist", "The lower layers (1-3)")
copy-pasted from a networking lesson — they have nothing to do with its own CIA-triad body.
`draft: true` is the only thing keeping this off the site. If anyone ever clears that flag it
will ship broken. Either delete the file or fix the sections; don't just un-draft it.

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
2. **⚠️ Decide what to do with the 20 `assessment-*` stubs on pc-technician.** See the audit
   below — this is a live student-facing quality problem and it needs Mr. Beattie's call.
3. **Labs for cybersecurity-engineer.** Twelve compliant lessons, six checkpoint quizzes,
   and **zero labs** — the widest genuine content gap in the repo. The working legacy
   interactive demos (sql-injection, xss-demo, cryptography, forensics, binary-exploitation,
   reverse-engineering) are lab material waiting to be wrapped. Prefer the `steps` lab shape.
4. **web-developer** — 4 lessons, none compliant. Phase E, not urgent.
5. **⚠️ ar / fa / uk translations in `src/i18n/strings.ts` are Claude-drafted and
   unreviewed.** Flagged in the file header. Mr. Beattie's students are the only fluent
   speakers available and are the intended reviewers — this is deliberate, not an oversight.

### Closed on 2026-09-09

- **tech-plus 6.1.7 AAA accounting** — lesson merged from a stray worktree branch, and its
  checkpoint quiz authored. Track closed at 59/59 lessons and quizzes.
- **All three duplicate quiz `order` warnings** on network-engineer. `validate:tracks` now
  passes with **zero warnings**.
- **cybersecurity-foundations** — was never incomplete; the apparent gap was a draft file
  plus five nav pages.

---

## Audit: the 20 `assessment-*` quizzes on pc-technician

Done 2026-09-09. The handoff had these as "never audited; may duplicate." The finding is worse
than duplication.

**Every one of the 20 is a single-question stub.** Each `assessment-1-x-x.mdx` carries no
inline questions — it points at `public/quizzes/pc-technician/assessment-1.x.x.json` via
`quizJsonPath`, and every one of those JSON files contains **exactly one** placeholder question
with a one-line explanation. Example, the whole of `assessment-1.2.5`:

> "What is a key IoT security concern?" → Weak default credentials.

They are generated by `scripts/ingest-assessments-from-manifest.mjs` from
`scripts/assessment-manifest.techplus.json`, and **the placeholder questions live in the
manifest itself** — the script only renders what it is given. Each entry names a
`sourceQuestionDocx` and `sourceAnswerDocx` (e.g. `Assessment 1.1.1 Basics of Computing.docx`).
**There are zero .docx files anywhere in the repo.** The real question banks were never
ingested; these are scaffolding left behind waiting for source documents.

Three further facts:

- **They duplicate properly-authored quizzes, with strictly worse content.** `assessment-1.1.1
  Basics of Computing` (1 question) against `pct-computing-basics` (9). `assessment-1.2.1
  Internal Hardware Components` (1) against `pct-components-identification` (10).
  `assessment-1.4.5 Customer Support Workflow` (1) against `pct-customer-professionalism` (10).
  The pattern holds across most of the set.
- **Their metadata is Tech+, their track is pc-technician.** Every file says "Auto-generated
  assessment quiz from Tech+ manifest" and is tagged `tech+`, while carrying `aplus1.hardware`
  / `aplus2.os` domain weights on the `pc-technician` track.
- **The manifest's `moduleId` is `pct.foundations` for all of them**, but the generated files
  carry varied real module ids. Someone hand-reassigned modules after generation, which is why
  the assignments looked scattered — `assessment-1-2-5` landing in
  `pct.fundamentals.computing-basics` is a leftover of that pass, not a mapping decision.

They sit at orders 101–120, so they trail their modules and collide with nothing. That is the
only good news: **they are student-visible activities that award XP for one trivial question.**

**Options, for Mr. Beattie to choose:**
1. Hide them (`draft: true`) until the real `.docx` banks are ingested — reversible, removes
   them from students now, keeps the scaffolding.
2. Delete the 20 `.mdx` and 20 `.json` — the topics are already covered better by the `pct-*`
   quizzes. The manifest and ingest script would stay for a future real ingest.
3. Ingest the real questions — needs the 40 `.docx` files, which are not in the repo.

Do **not** quietly leave them live on the assumption they are harmless.

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

Baseline confirmed 2026-09-09: validate passes with **zero warnings** ·
11 tracks, 72 modules, 353 entries · lint **0 errors, 0 warnings, 7 hints** · **14/14 tests**.

The duplicate-order warnings are gone — treat any new one as a regression, not as noise.

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
