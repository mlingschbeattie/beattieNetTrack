# CLAUDE.md — beattieNetTrack Session Brief
# Auto-read by Claude Code at session start. Source of truth for all decisions.

---

## Project Purpose

beattieNetTrack is a purpose-built LMS for IT/cybersecurity certification education.
Students: high school, mixed experience levels (zero to advanced).
Goal: move students from zero → employable along a coherent cert-mapped learning path.
Stack: Astro + MDX + TypeScript + React islands. Read CONSTITUTION.md before any change.

---

## Behavioral Rules

- **Ask before destructive or irreversible changes.** Everything else: proceed and summarize.
- Run `npm run validate:tracks && npm run lint` after every content or schema change. Report output.
- One change at a time. No broad refactors unless explicitly requested.
- Never hardcode colors — use tokens from `src/styles/tokens.css`.
- Never create orphan content — every activity needs a `track` and `moduleId` that resolve to real entries.

---

## CRITICAL: Use Actual Repo Slugs

The slugs below are the ones that EXIST IN THE REPO. Do not invent new slugs or use
the planning names from earlier sessions. If a slug below says "create", it does not
exist yet and must be created before any content references it.

## Complete Track Registry

| Slug (actual) | Name | Cert target | Status | Notes |
|---|---|---|---|---|
| `tech-plus` | Technology Plus | CompTIA Tech+ FC0-U71 | **CREATE — Phase A now** | 59 lesson guides ready |
| `pc-technician` | CompTIA A+ | 220-1101 + 220-1102 | Exists, building | TestOut source |
| `network-engineer` | Network+ | N10-009 | Exists, Phase 0 active | CYBER.ORG course 239 |
| `python-developer` | Python Fundamentals | PCEP | Exists | CYBER.ORG course 60 |
| `cybersecurity-foundations` | Cybersecurity 1 | CyberPatriot / intro | Exists | CYBER.ORG course 243 |
| `cybersecurity-engineer` | Security+ | SY0-701 | Exists | CYBER.ORG 368 + 100 merged |
| `web-developer` | Web Dev Fundamentals | HTML/CSS/JS | Exists | Author from scratch |
| `ai-ml` | AI & Machine Learning | none / awareness | Exists | Bonus track |
| `linux` | Linux | Linux+ / LPIC-1 | **CREATE when ready** | CYBER.ORG course 357 |
| `cyber-literacy` | Cyber Literacy | none / awareness | **CREATE — stretch** | CYBER.ORG course 359 |
| `legacy` | Legacy (archive) | — | Exists, read-only | Do not modify |
| `legacy-grouped` | Legacy Grouped (archive) | — | Exists, read-only | Do not modify |

**Do not invent new slugs. Do not use planning names like `network-plus`, `a-plus`,
`coding-fundamentals`, `cybersec-1`, `linux-intro`, `linux-deep-dive`, `web-dev`.
Those were planning names. The repo uses the slugs in the table above.**

---

## Current Build Focus: tech-plus

**Exam:** CompTIA Tech+ FC0-U71 v2.0
**Source:** 59 lesson guide PDFs — confirmed from CYBER.ORG live, all gaps resolved
**Location in repo:** `public/resources/pc-technician/` (30 PDFs already there) +
lesson guides added this session
**Audit doc:** `TECHPLUS_TRACK_AUDIT.md`

### tech-plus module structure (6 modules — one per exam domain)

| Module ID | Domain | Exam weight | Lessons |
|---|---|---|---|
| `tech-plus.it-concepts` | 1.0 IT Concepts and Terminology | 13% | 8 |
| `tech-plus.infrastructure` | 2.0 Infrastructure | 24% | 13 |
| `tech-plus.applications` | 3.0 Applications and Software | 18% | 10 |
| `tech-plus.software-dev` | 4.0 Software Development Concepts | 13% | 7 |
| `tech-plus.databases` | 5.0 Data and Database Fundamentals | 13% | 5 |
| `tech-plus.security` | 6.0 Security | 19% | 16 |
| **Total** | | **100%** | **59** |

### Domain 6 complete lesson list (all 16 confirmed from CYBER.ORG API)
6.1.1 Confidentiality Concerns · 6.1.2 Integrity Concerns · 6.1.3 Availability Concerns ·
6.1.4 Privacy · 6.1.5 AAA Authentication · 6.1.6 AAA Authorization · 6.1.7 AAA Accounting ·
6.1.8 Non-Repudiation · 6.2.1 Security Awareness · 6.2.2 Securing Devices ·
6.2.3 Device Use Best Practices · 6.2.4 Safe Browsing Practices · 6.3.1 Password Best Practices ·
6.4.1 Plain Text vs Cipher Text · 6.4.2 Data Types · 6.5.1 Securing Small Wireless Networks

*Note: 6.5.1 PDF has a typo in filename ("Secruing") — do not carry typo into slug.*

### Phase A — Execute now
1. Read `src/content/config.ts` — understand lesson/module schema before writing anything
2. Read one existing module file to understand the pattern
3. Create `src/content/tracks/tech-plus.mdx`
4. Create all 6 module files in `src/content/modules/`
5. Run `npm run validate:tracks` — must pass clean before any lessons
6. Commit: `content(tech-plus): add track and 6 module definitions`

### Phase B — Lessons (domain by domain, validate + commit after each)
Ingest order: Domain 2 (highest weight) → Domain 6 → Domain 3 → Domain 1 → Domain 4 → Domain 5

### Lesson frontmatter minimum
```yaml
---
title: "Basics of Computing"
slug: tech-plus-1-1-1-basics-of-computing
track: tech-plus
moduleId: tech-plus.it-concepts
order: 1
objective: "FC0-U71 1.1"
xp: 15
source: cyber-org
---
```

---

## Module ID Conventions

Format: `{track-slug}.{domain-or-topic}` — lowercase, hyphens only, no underscores.

Examples from existing repo:
- `net.fundamentals` — network-engineer track fundamentals module
- `pct.hardware` — pc-technician track hardware module
- `sec.threats` — cybersecurity-engineer track threats module
- `py.core-syntax` — python-developer track

New tracks follow same pattern:
- `tech-plus.infrastructure` — tech-plus Domain 2
- `linux.intro` — linux track intro module
- `linux.deep-dive` — linux track advanced module

---

## Existing Module Inventory (do not duplicate)

### network-engineer track (net/ folder — 20 modules)
net.fundamentals · net.implementation · net.operations · net.security · net.troubleshooting
(+ submodules within each — read src/content/modules/net/ before adding anything)

### pc-technician track (pct/ folder — 10 modules + pc-tech/ — 3 modules)
pct.customer · pct.fundamentals · pct.hardware · pct.os · pct.troubleshooting (+ submodules)

### python-developer track (py/ folder — 5 modules)
### cybersecurity-foundations + cybersecurity-engineer (sec/ folder — 8 modules)
### web-developer track (web/ folder — 6 modules)
### ai-ml track (ai/ folder — 5 modules)

---

## Build Phase Order

| Phase | Track | Prerequisite | Status |
|---|---|---|---|
| 0 | `network-engineer` | none | Active |
| A | `tech-plus` | 59 PDFs confirmed | **Execute now** |
| B | `pc-technician` | TestOut export | Blocked — waiting |
| C | `cybersecurity-foundations` + `python-developer` | Phase A stable | Queued |
| D | `cybersecurity-engineer` + `linux` | Phase C stable | Queued |
| E | `cyber-literacy` + `web-developer` | Phase D stable | Queued |
| F | Competency placement exams — all tracks | Each track complete | Last |

---

## CYBER.ORG Course → Track Mapping

| CYBER.ORG Course | Canvas ID | Repo track slug |
|---|---|---|
| Technology Plus | 371 | `tech-plus` |
| Networking | 239 | `network-engineer` |
| Cybersecurity 1 | 243 | `cybersecurity-foundations` |
| Cybersecurity 2 | 368 | `cybersecurity-engineer` (merged) |
| Cybersecurity 701 | 100 | `cybersecurity-engineer` (merged) |
| Intro to Linux | 357 | `linux` |
| Coding Fundamentals (Python only) | 60 | `python-developer` |
| Cyber Literacy | 359 | `cyber-literacy` |

A+ source is CompTIA TestOut — not CYBER.ORG. Track slug: `pc-technician`.

---

## Competency Placement Exams

One per track. Suggested, never required. Quiz type `placement` in frontmatter.
Show domain-breakdown results so students see weak areas, not just pass/fail.
Author after all lessons for that track are ingested — Phase F.

---

## XP Scale

| Activity | XP |
|---|---|
| Lesson (reading) | 15 |
| Quiz (pass) | 35 |
| Lab (complete) | 50 |
| Placement exam (pass) | 75 |
| Module complete (bonus) | 25 |
| Track complete (bonus) | 200 |

---

## Files to Read Before Any Work Session

| File | Why |
|---|---|
| `CONSTITUTION.md` | The law. Read before any change. |
| `src/content/config.ts` | Schema authority. All field definitions. |
| `src/lib/content.ts` | Content API. Pages query through here. |
| `scripts/validate-tracks.mjs` | Understand every check it runs. |
| `src/content/tracks/` | Check before adding a new track. |
| `src/content/modules/` | Every moduleId must resolve here. |

---

## Do Not Touch

- `src/lib/coachClient.ts` — Phase 5 AI stub, leave alone
- `public/legacy/` — read-only archive, one-file-at-a-time migration only
- `.github/workflows/ci.yml` — do not modify
- Any Supabase schema files — Phase 3 not started
- `legacy` and `legacy-grouped` tracks — archive, read-only

---

## Commit Message Format

```
content(tech-plus): add track and 6 module definitions
content(tech-plus): ingest Domain 2 infrastructure — 13 lessons
fix(tech-plus): correct moduleId in lesson 2.4.1
feat(schema): add placement quiz type to config
```

---

*Last updated: post-audit reconciliation — actual repo slugs confirmed*
*Validation: passing clean · 9 tracks · 63 modules · 109 entries*
*Tech+ PDFs: 59 confirmed from CYBER.ORG · all 26 objectives covered*
