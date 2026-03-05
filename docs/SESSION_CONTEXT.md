# BeattieNetTrack — Session Context & Pipeline Reference

**Last updated:** 2026-03-05  
**Current state:** All 5 gates green, 286 pages building, 38/38 tests passing

---

## Who This Is For

Mr. L — IT teacher, Beattie Tech high school. AuDHD educator. Teaches second-year
students working toward CompTIA Network+ (N10-008 / N10-009). This document is the
handoff between AI-assisted work sessions so context doesn't have to be rebuilt
from scratch every time.

---

## Project State Summary

### Gates (must all pass before any commit)
```bash
npm run validate:tracks   # Gate 1 — content integrity
npm run lint              # Gate 2 — TypeScript / Astro check  
npm run test:unit         # Gate 3 — unit tests
npm run build             # Gate 4 — Astro build
npx playwright test       # Gate 5 — visual + browser tests
```

Current: **0 errors, 0 warnings, 38/38 tests, 286 pages**

### What's been completed
- P0: Content audit, module namespace consolidation, legacy migrations, CI baseline
- P1-A: Curriculum manifest schema designed
- Module expansion: network-engineer track 8 → 14 CompTIA-aligned modules
- 60 CYBER.ORG quizzes ingested, schema-corrected, validated
- 2 lessons authored and committed (1.1.1 OSI Model, 1.1.2 Encapsulation)
- PDF pipeline established (guided notes + answer key per unit)
- Phase 5 question engine specced: `docs/PHASE5_QUESTION_ENGINE.md`

### Active phase: P0/P1 content build-out
Building lessons unit by unit through the network-engineer track.
Next units: 1.2.1 Network Topologies, 1.2.2 Network Types

---

## Content Pipeline (How a Unit Gets Built)

### Step 1 — Opus lesson draft (2 units per call)
Use the system prompt below. Paste it first, then the unit prompt.
Output: lesson body markdown for each unit.

### Step 2 — Wire up lesson MDX
Create `src/content/lessons/net-[slug].mdx` with this frontmatter:
```yaml
---
title: "[Title]"
description: "[One line description]"
slug: net-[slug]
track: network-engineer
moduleId: [module-id]
order: [N]
difficulty: Beginner
estMinutes: 20
tags: ["network+", "[topic]", "N10-009 [obj]", "N10-008 [obj]"]
---
```
Lessons schema: title (required), track/moduleId optional but always include them,
tags array, order int. No `xp` field on lessons.

### Step 3 — Add unit data to PDF script
Open `scripts/make_resource_pdfs.py`, add a new entry to the `UNITS` dict:
```python
"1.x.x": {
    "unit": "1.x.x",
    "title": "Unit Title",
    "n10_009": "x.x",
    "n10_008": "x.x",
    "questions": [
        {
            "num": "1",
            "question": "Fill in the blank question with _______ here.",
            "answer": "The answer.",
            "lines": 3
        },
        # ... 7-8 questions total, last one has "real_world": True, "lines": 6
    ]
}
```

### Step 4 — Generate PDFs
```bash
python3 scripts/make_resource_pdfs.py --unit 1.x.x
# or regenerate all:
python3 scripts/make_resource_pdfs.py --all
```
Output goes to: `public/resources/network-engineer/[unit-slug]/`

### Step 5 — Validate and commit
```bash
npm run validate:tracks && npm run lint && npm run build
git add src/content/lessons/ public/resources/ scripts/make_resource_pdfs.py
git commit -m "feat(content): add unit X.X.X [Title] lesson and resources"
```

---

## Mr. L's Voice — Opus System Prompt

Paste this at the start of every Opus lesson-writing session, then append the unit prompt.

```
You are writing curriculum for Mr. L's high school IT class at Beattie Tech.

VOICE AND TONE:
- Direct and practical. Explain it once, move on.
- Dry humor. Absurdist references to current internet culture, gaming, memes —
  used sparingly and only when they land naturally. Never forced. Never explained.
  If you have to explain the joke, cut it.
- Gen Z references are fair game but only when they fit organically. Lampoon the
  trends affectionately, don't pander to them.
- No filler. No "great question!" energy. Respect their time.

TEACHING PHILOSOPHY:
- Real-world first. Every concept gets anchored to something a tech actually does
  or encounters in the field.
- The industry is brutal and beautiful — tech evolves constantly, lifelong learning
  isn't optional, it's the job. Say this when it fits.
- Show the evolution of the technology when relevant. Where did it come from, why
  does it work this way now, what's probably coming next.
- Introduce, resource, assign, release. Learning comes from the struggle.
- Don't baby them. They're second-year students who've built PCs and troubleshot
  Windows. Talk to them like junior techs.

STUDENTS:
- High school, second year, PC technician fundamentals complete
- Mixed experience — some have touched networking, some haven't
- They know gaming, streaming, social media infrastructure better than most adults
  — use that
- CompTIA Network+ (N10-008 / N10-009) is the target certification

WHAT NOT TO DO:
- No bullet-point walls in lesson prose
- No "in conclusion" or "in summary" wrap-ups
- No corporate training video energy
- Don't reference being an AI
- Don't use the word "crucial" or "delve"
```

### Unit prompt template (append after system prompt)
```
UNIT [X.X.X] — [Title]
CompTIA N10-009 / N10-008 Objective: [X.X]
Module: [module-id]

Key concepts from source material: [comma-separated list from CYBER.ORG guided notes]

---

UNIT [X.X.X] — [Title]  
CompTIA N10-009 / N10-008 Objective: [X.X]
Module: [module-id]

Key concepts from source material: [comma-separated list]

---

Write the lesson body for EACH unit. Label them clearly:
## LESSON X.X.X and ## LESSON X.X.X

Same format, length, and voice as the OSI Model and Encapsulation lessons.
Markdown only, no MDX components.
```

**Batching rule:** 2 units per Opus call maximum. Quality drifts on the third.

---

## Reference Lessons (voice benchmarks)

- `src/content/lessons/net-osi-model.mdx` — Unit 1.1.1, the template
- `src/content/lessons/net-encapsulation-decapsulation.mdx` — Unit 1.1.2

Key voice markers from these lessons:
- Opens with a real-world scenario the student has lived ("You buy a GPU online...")
- One paragraph per major concept, no sub-bullets
- Analogies that respect student intelligence ("UDP is a guy yelling information
  out of a car window")
- Closes with field relevance, not a summary

---

## Module Map (network-engineer track)

| Module ID | Title | CompTIA Domain |
|---|---|---|
| net.fundamentals.models-and-standards | Models & Standards | 1.1 |
| net.fundamentals.topologies-and-types | Topologies & Types | 1.2 |
| net.fundamentals.cabling-and-connectors | Cabling & Connectors | 1.3 |
| net.fundamentals.addressing | Addressing | 1.4 |
| net.fundamentals.ports-and-protocols | Ports & Protocols | 1.5 |
| net.fundamentals.network-services | Network Services | 1.6 |
| net.fundamentals.architecture | Architecture | 1.7/1.8 |
| net.implementation.devices | Devices | 2.1 |
| net.implementation.routing | Routing | 2.2 |
| net.implementation.switching | Switching | 2.3 |
| net.implementation.wireless | Wireless | 2.4 |
| net.operations.monitoring-and-docs | Monitoring & Docs | 3.x |
| net.security.defense | Security & Defense | 4.x |
| net.troubleshooting.tools-and-methods | Troubleshooting | 5.x |

---

## Key Files

| File | Purpose |
|---|---|
| `CONSTITUTION.md` | Rules. Read before any change. |
| `src/content/config.ts` | Schema authority for all collections |
| `src/lib/progressStore.ts` | XP / completion state (localStorage) |
| `src/lib/content.ts` | Content query functions |
| `scripts/make_resource_pdfs.py` | Generates guided notes + answer key PDFs |
| `scripts/extract-cyberorg-quizzes.py` | Ingests CYBER.ORG quiz DOCX files |
| `docs/PHASE5_QUESTION_ENGINE.md` | AI question generation engine spec |

---

## Known Schema Rules (learned the hard way)

- Quiz `passThreshold`: integer 1–100 (not float — `70` not `0.7`)
- Quiz `correctIndex`: zero-based integer (not `correct: "B. text"`)
- Lesson `tags`: array of strings, always include CompTIA objective
- Lab `order: 99` is a bad pattern — causes nav collisions; use real order values
- `<` in MDX prose must be `&lt;` or it breaks the build
- Run `validate:tracks` before every commit — it's fast and catches orphaned content

---

## Roadmap Phases

| Phase | Status | Description |
|---|---|---|
| P0 | ✅ Complete | Stabilize baseline, fix validation, migrate legacy HTML |
| P1 | 🔄 Active | Curriculum build-out — lessons, guided notes, PDFs |
| P2 | Upcoming | XP ranks, badges, certificates |
| P3 | Upcoming | Supabase — durable progress, cross-device sync |
| P4 | Future | Live Docker lab environments |
| P5 | Future | AI question generation engine (see PHASE5_QUESTION_ENGINE.md) |

---

## How to Start a New Session

1. Paste this document into context (or reference it by path)
2. State current objective: "We're building units 1.2.1 and 1.2.2"
3. If writing lessons: paste Opus system prompt + unit prompt, run call, paste output
4. If fixing bugs: paste error output, reference relevant schema rules above
5. Always end session with full gate run and commit