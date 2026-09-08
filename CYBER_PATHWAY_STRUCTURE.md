# CYBER_PATHWAY_STRUCTURE.md

Course structure for the cyber pathway, mapped to NOCTI blueprints and CompTIA Security+ SY0-701.
Covers `cybersecurity-foundations` → `cybersecurity-engineer` as one progression.

*Drafted 2026-09-08. Structure proposal — not yet implemented. No module or lesson files have been
created or moved from this document.*

---

## 0) Credential Alignment — Read This First

| Credential | Code | CIP on the blueprint | Format | Maps to track |
|---|---|---|---|---|
| NOCTI Computer Networking Fundamentals | 4514 | **11.0901** | Written 194q / 3h + Performance 2h | `network-engineer` + `pc-technician` |
| NOCTI Cybersecurity Fundamentals | 4324 | **11.1003** | Written only, 98q / 2h | `cybersecurity-foundations` |
| CompTIA Security+ | SY0-701 | — | Written | `cybersecurity-engineer` |

**The program is CIP 11.0901. Students must pass NOCTI 4514 — that is the accountability
measure, now and for the foreseeable future.** The program is formally two years: **A+ and
Net+**. Cybersecurity is a **third-year stretch** — going beyond the required scope for
students who want it, and futureproofing ahead of a planned move to CIP 11.1003 within about
two years (instructor, 2026-09-08).

That ordering drives everything below:

1. **4514 Computer Networking Fundamentals is the graded requirement.** It is a Job Ready
   assessment with a **performance component** — 2 hours, two hands-on jobs, scored separately
   from the written test. **Nothing in the repo targets it.** See §4. This is the highest
   priority item in this document, not a transitional one.
2. **The two-year core is `pc-technician` and `network-engineer`.** Those tracks carry the
   credential students are actually measured on. 4514's own competency list spans PC
   principles, addressing, routing/switching, troubleshooting, security and network design —
   all of it landing on those two tracks.
3. **Cyber is year-three enrichment.** `cybersecurity-foundations` and
   `cybersecurity-engineer` are worth building and are *not* on the critical path. Build them
   as capacity allows, ahead of the 11.1003 move.
4. **4324 becomes the destination credential only after the CIP changes.** Structuring
   `cybersecurity-foundations` against its six areas (§2) is the right shape to build toward,
   on a multi-year horizon rather than this term.

---

## 1) NOCTI Cybersecurity Fundamentals (4324) — Verbatim Blueprint

Foundational credential. Written only. 98 questions, 2 hours, 1–3 sessions.
Revision team: FL, GA, PA, SC, VA, WV. Copyright 2024, Version 01.

Six areas covered. **Weightings carry a caveat — see §1.1.**

### 1.1 Weighting caveat

The blueprint renders area names and percentages as a chart. Text extraction returns the
labels and the numbers as two separate lists, so the pairing is not machine-recoverable:

- Labels, in order: Computer Forensics · Identification, Authentication, and Authorization ·
  Security Controls · Risk and Threat Analysis Introduction · Cryptography · Cybersecurity Fundamentals
- Numbers, in order: 28% · 16% · 18% · 9% · 14% · 15%

Both orderings sum to 100%. **Confirm against page 3 of the blueprint PDF before allocating
teaching time.** The prior version of this assessment (4224) weighted: Fundamentals 23%,
Crypto 11%, Threat 16%, Controls 19%, IAA 15%, Forensics 16% — which favours the reversed
pairing, but that is inference, not evidence.

### 1.2 Competencies (verbatim, unambiguous)

**Cybersecurity Fundamentals**
- Identify different types of cybercrimes
- Communicate incident handling and the response process
- Identify risk (e.g., categorize, mitigate, accept)
- Identify basic cybersecurity terminology
- Recognize network security basics

**Cryptography**
- Identify different types of cryptography
- Distinguish between steganography and cryptography
- Describe different encryption and decryption methods

**Risk and Threat Analysis Introduction**
- Identify attackers through threat modeling
- Describe vulnerabilities in information systems and file systems
- Describe procedures necessary for finding and containing malware and viruses
- Interpret current laws and regulations to provide updates to organizational security policies

**Security Controls**
- Identify different types of attacks and applicable responses
- Apply procedural concepts necessary to configure security systems and validate security
- Understand importance of hardware and software updates and patches
- Define social engineering
- Describe an access control list

**Identification, Authentication, and Authorization**
- Identify different methods of identification, authentication, and authorization
- Describe different biometric devices
- Identify the appropriate placement of biometric devices

**Computer Forensics**
- Apply procedural concepts required to use forensic tools
- Determine the important content of event logs in forensics
- Recognize that devices are kept in the same state as they were found
- Apply procedural concepts required to discover evidence on different file systems and operating systems
- Identify the chain of custody and implement the proper handling of evidence

---

## 2) Track: `cybersecurity-foundations` → NOCTI 4324

One module per NOCTI area. Six modules replacing the single
`cfs.fundamentals.security-concepts` catch-all.

| Order | Module ID | NOCTI area | Existing content that moves here |
|---|---|---|---|
| 1 | `cfs.fundamentals` | Cybersecurity Fundamentals | `cfs-1-1-1-cia-triad`, `linux-cli-survival` |
| 2 | `cfs.risk-threat` | Risk and Threat Analysis Introduction | `cfs-1-1-2-threat-vulnerability-risk` |
| 3 | `cfs.controls` | Security Controls | `cfs-1-1-3-social-engineering` |
| 4 | `cfs.identity` | Identification, Authentication, and Authorization | — |
| 5 | `cfs.crypto` | Cryptography | — |
| 6 | `cfs.forensics` | Computer Forensics | — |

Note `cfs-1-1-3-social-engineering` moves to **Security Controls**, not to a social-engineering
module — the blueprint lists "Define social engineering" under Security Controls.

### 2.1 Proposed lessons

Existing lessons are marked ✅. Everything else is new authoring.

**`cfs.fundamentals` — Cybersecurity Fundamentals**
1. ✅ The CIA Triad — Classifying What Broke
2. Types of Cybercrime — What Gets Prosecuted and Why
3. Core Vocabulary — Asset, Threat, Actor, Control, Incident
4. Network Security Basics for Defenders
5. The Incident Response Lifecycle — Prepare, Detect, Contain, Recover, Learn
6. ✅ Linux CLI Survival Kit

**`cfs.risk-threat` — Risk and Threat Analysis Introduction**
1. ✅ Threat, Vulnerability, and Risk — The Triage Formula
2. Threat Modeling — Identifying Attackers and Their Motives
3. Vulnerabilities in Systems and File Systems
4. Malware Families — Finding and Containing an Infection
5. Laws, Regulations, and the Policies They Force

**`cfs.controls` — Security Controls**
1. Control Types — Preventive, Detective, Corrective, Compensating
2. Common Attacks and the Response Each One Demands
3. ✅ Social Engineering & Human Vectors
4. Patch and Update Management — Why Delay Is the Vulnerability
5. Access Control Lists — Reading and Writing Them
6. Configuring and Validating a Security Control

**`cfs.identity` — Identification, Authentication, and Authorization**
1. The Three Steps — Identify, Authenticate, Authorize
2. Authentication Factors and Multi-Factor Authentication
3. Biometric Devices — Types, Accuracy, and Failure Modes
4. Where Biometrics Belong — Placement and Physical Security

**`cfs.crypto` — Cryptography**
1. What Cryptography Protects — Confidentiality, Integrity, Authenticity
2. Symmetric and Asymmetric Encryption
3. Hashing and Integrity Verification
4. Steganography vs Cryptography — Hiding Existence vs Hiding Meaning

**`cfs.forensics` — Computer Forensics**
1. Forensic Tools and the Order of Operations
2. Event Logs — What Matters and Where It Lives
3. Preserving State — Why the Device Is Not Touched
4. Discovering Evidence Across File Systems and Operating Systems
5. Chain of Custody and Evidence Handling

**Totals:** 30 lessons (4 exist, 26 to author), 6 module checkpoint quizzes, 1 placement exam.

### 2.2 Content that already exists on the wrong track

Four `cybersecurity-engineer` lessons are pitched at foundations level and duplicate
4324 competencies directly. Per Constitution §14 these must **not** be copied — set
`sharedWith: ["cybersecurity-foundations"]` on the canonical file instead.

| Lesson | Canonical track | Shared into |
|---|---|---|
| `cryptography` | cybersecurity-engineer | `cfs.crypto` |
| `forensics` | cybersecurity-engineer | `cfs.forensics` |
| `exif-simulator` | cybersecurity-engineer | `cfs.forensics` |
| `auth-demo` | cybersecurity-engineer | `cfs.identity` |

This cuts the authoring load from 26 new lessons to roughly 22.

---

## 3) Track: `cybersecurity-engineer` → CompTIA Security+ SY0-701

Five modules, one per exam domain, weighted to the published exam blueprint.

*Domain names and weights below should be confirmed against the current official CompTIA
SY0-701 exam objectives document before content is authored against sub-objective numbers.*

| Order | Module ID | Domain | Exam weight |
|---|---|---|---|
| 1 | `sec.general-concepts` | 1.0 General Security Concepts | 12% |
| 2 | `sec.threats` | 2.0 Threats, Vulnerabilities, and Mitigations | 22% |
| 3 | `sec.architecture` | 3.0 Security Architecture | 18% |
| 4 | `sec.operations` | 4.0 Security Operations | 28% |
| 5 | `sec.program-management` | 5.0 Security Program Management and Oversight | 20% |

### 3.1 Where the existing 12 lessons land

All twelve were brought to the authoring standard in commit `43aed6d`. None need rewriting —
they need remapping.

| Existing lesson | Current module | Proposed module |
|---|---|---|
| `threat-modeling-basics` | sec.fundamentals.risk-and-policy | `sec.program-management` |
| `cryptography` | sec.crypto.basics | `sec.general-concepts` |
| `password-hashing` | sec.crypto.basics | `sec.general-concepts` |
| `https-demo` | sec.crypto.basics | `sec.architecture` |
| `sql-injection` | sec.network.defense-basics | `sec.threats` |
| `xss-demo` | sec.network.defense-basics | `sec.threats` |
| `web-exploitation` | sec.network.defense-basics | `sec.threats` |
| `binary-exploitation` | sec.network.defense-basics | `sec.threats` |
| `auth-demo` | sec.identity.access-management | `sec.operations` |
| `forensics` | sec.incident.response-basics | `sec.operations` |
| `exif-simulator` | sec.incident.response-basics | `sec.operations` |
| `reverse-engineering` | sec.endpoint.hardening | `sec.operations` |

Cryptography sits in Domain 1.0 in SY0-701 (crypto solutions is a General Security Concepts
objective), which is the main surprise in this remap. TLS/PKI in `https-demo` is architecture.

### 3.2 Coverage gaps by domain

Existing lessons cluster hard in Threats and Operations. The gaps:

- **1.0 General Security Concepts** — control types and categories, CIA/AAA as a framework,
  zero trust, physical security, change management. *2 of ~6 lessons exist.*
- **2.0 Threats** — threat actors and motivations, threat vectors and attack surfaces,
  vulnerability types beyond web/binary, indicators of malicious activity, mitigation techniques.
  *4 of ~8 exist, all offensive-technique focused; the actor/motivation and indicator material is absent.*
- **3.0 Security Architecture** — cloud and virtualization models, IaC, serverless, microservices,
  secure network design, data protection and classification, resilience and recovery.
  *1 of ~7 exists. Weakest domain.*
- **4.0 Security Operations** — secure baselines, hardening, asset and vulnerability management,
  alerting and monitoring, firewalls/IDS/web filtering/DNS/email security, automation, IR, log sources.
  *4 of ~12 exist. Largest domain at 28% and the thinnest relative coverage.*
- **5.0 Program Management** — governance, risk management, third-party risk, compliance,
  audits and assessments, security awareness. *1 of ~6 exists.*

**Estimated to complete the track: ~28 new lessons, 5 module checkpoints, 1 placement exam.**

---

## 4) The 4514 Performance Component — Deferred

NOCTI 4514 is the credential **students must pass** under CIP 11.0901, and it includes a
2-hour **performance** assessment carrying its own score. Nothing in the repo targets it.

**Deferred by instructor decision, 2026-09-08. Do not build against the task list below.**

> ⚠️ **The tasks below are the blueprint's "Sample Job" section from the 2016 document. They
> are illustrative, not the actual jobs administered.** The instructor, who proctors this
> assessment, has confirmed the real jobs differ. An earlier draft of this document treated
> them as the specification and proposed building labs directly against them — that was wrong,
> and it is exactly the kind of confident inference from a stale public document that should
> be checked against someone who administers the thing.
>
> Before any performance-assessment work: get the current job descriptions from the
> instructor or from current NOCTI proctor materials, not from this table.

| Job | Weight | Task |
|---|---|---|
| 1 | 39% | Select and connect equipment for a simple two-workstation LAN; assign a private IPv4 Class C address and subnet; record results; verify IP connectivity |
| 2 | 61% | Name workstations; join workgroup `NOCTI`; create users; create folders; create a share; grant permissions; access-test; install a plug-and-play printer, set default, share, and print to verify |

What is still safe to take from this: the *skill areas* the performance component exercises —
private addressing and subnetting, workgroup membership, user and share creation, NTFS
permissions, printer installation and verification — are core A+ and Net+ content regardless
of how the actual jobs are worded. Those belong on `pc-technician` and `network-engineer` on
their own merits. What must not be inferred is the specific job structure, weighting, or task
sequence.

When this is picked up: get the real job descriptions first, then build `steps` labs
(`LabRunner` with exact/oneOf/regex/choice validators) against them.

---

## 5) Domain Taxonomy Must Be Fixed First

The `domains[]` frontmatter and the competency dashboard do not agree. Any structure built
on top inherits the fault. `CIS_DOMAIN_BENCHMARKS` in `src/components/teacher/ClassRoster.tsx`
is the dashboard's source of truth; content frontmatter and `scripts/tag-competency-domains.mjs`
both diverge from it.

### 5.1 Correction to an earlier draft of this section

The first version of this table was wrong in three rows, and the error is worth recording so it
is not repeated. The inventory was gathered with the pattern `domainId: [a-z0-9.]+`, which
excludes underscores and therefore silently **truncated** ids at the first underscore —
`netplus.networking_concepts` was counted as `netplus.networking`, and
`aplus2.operational_procedures` as `aplus2.operational`. Always include `_` when inventorying
these ids.

The corrected conclusion reverses part of the original claim: **the tagging script agrees with
the content.** `CIS_DOMAIN_BENCHMARKS` is the outlier.

### 5.2 Where the authority actually lives

`CIS_DOMAIN_BENCHMARKS` in `ClassRoster.tsx` is **not** the system of record. It is a static
array rendered as a read-only reference grid on the "Curriculum Domains" tab. Nothing joins it
to student progress.

The real registry is served by the external CIS API and fetched at runtime:

- `CompetencyMapView.tsx` → `GET {PUBLIC_API_URL}/api/cis/domains`
- `StudentProfile.tsx` → per-student cert/domain data from the same API
- Content `domains[]` → `src/lib/events.ts` → `POST {PUBLIC_API_URL}/api/events`

`PUBLIC_API_URL` is `https://api.beattietech.local`, and `/api/cis/domains` returns **302 to
`auth.beattietech.local`** — it is SSO-gated and cannot be read from a build session.

**Consequence: do not mass-rename content `domainId`s from this repo alone.** Whether
`netplus.networking_concepts` or `netplus.networking` is correct is decided by the server
registry, not by the local display table. Renaming to match `CIS_DOMAIN_BENCHMARKS` could break
rollups that currently work. The earlier "never rolls up" wording overstated what was verified:
the local table and the content disagree, but the actual join happens server-side against a
registry this repo cannot see.

### 5.3 Verified state

Content ids, with true counts (underscores included):

| Content domainId | Uses | In local benchmark table? |
|---|---|---|
| `nocti.networking` | 123 | yes |
| `netplus.networking_concepts` | 45 | no — table has `netplus.networking` |
| `aplus1.hardware` | 34 | yes |
| `techplus.security` | 31 | no — no `techplus` cert track at all |
| `nocti.hardware` | 29 | yes |
| `techplus.infrastructure` | 27 | no |
| `aplus2.os` | 27 | yes |
| `netplus.security` | 22 | yes |
| `techplus.applications` | 21 | no |
| `cyber.foundations` | 21 | no |
| `netplus.infrastructure` | 20 | yes |
| `netplus.troubleshooting` | 19 | yes |
| `techplus.concepts` | 16 | no |
| `techplus.software` | 14 | no |
| `netplus.operations` | 14 | no — table has `netplus.ops` |
| `techplus.databases` | 11 | no |
| `nocti.os` | 11 | yes |
| `aplus1.troubleshooting` | 9 | no — table has `aplus1.hardware_troubleshooting` |
| `secplus.threats` | 7 | yes |
| `secplus.architecture` | 6 | yes |
| `web.frontend` | 4 | no |
| `secplus.operations` | 3 | no — table has `secplus.ops` |
| `aplus2.operational_procedures` | 3 | no — table has `aplus2.ops` |
| `nocti.security` | 3 | no |
| `aplus2.security` | 1 | yes |

Benchmark ids with **zero** content: `aplus1.mobile`, `aplus1.networking`,
`aplus1.virtualization`, `aplus1.hardware_troubleshooting`, `aplus2.ops`,
`aplus2.software_troubleshooting`, `netplus.networking`, `netplus.ops`, `nocti.devices`,
`nocti.management`, `nocti.media`, `nocti.safety`, `nocti.tools`, `nocti.troubleshooting`,
`secplus.governance`, `secplus.implementation`, `secplus.ops`.

`CIS_DOMAIN_BENCHMARKS` also describes **SY0-601** domains (Threats / Architecture /
Implementation / Operations / Governance) while the seeds and CLAUDE.md target **SY0-701**.

Note: a `domainId: z.string` "use" appears if you grep `src/content/` naively — that is the
schema definition in `src/content/config.ts`, not content. Weights above 1.0 in a single
`domains[]` block are also **not** a defect: `events.ts` documents weight as "how strongly this
event maps to this domain", a per-domain strength rather than a share, so `0.9 + 0.8` is valid.

### 5.4 Done — internal consistency only

Three single-use ids deviated from a convention used 14–31 times elsewhere in the same modules.
Fixed, no server knowledge required:

| File | Was | Now | Evidence |
|---|---|---|---|
| `labs/tech-plus-first-program.mdx` | `techplus.software_dev` | `techplus.software` | module is `tech-plus.software-dev`; its 14 lessons all use `techplus.software` |
| `labs/tech-plus-binary-storage-bench.mdx` | `techplus.it_concepts` | `techplus.concepts` | module is `tech-plus.it-concepts`; its 16 lessons all use `techplus.concepts` |
| `labs/cfs-security-baseline-lab.mdx` | `secops.basics` | `nocti.security` | orphan with no benchmark and no other use; the parallel `pct-windows-security-hardening-lab` pairs a cert domain with a `nocti.*` domain in exactly this slot |

### 5.5 Blocked — needs the server registry

Everything below requires knowing what `/api/cis/domains` actually returns. **Get that list
first** (sign in at `https://api.beattietech.local/api/cis/domains`, or export it from the CIS
backend) and record it in this repo as the source of truth.

Then, in one pass:

1. Decide direction per id — server registry wins over both the content and the local table.
2. Reconcile `netplus.networking_concepts` / `netplus.networking`,
   `netplus.operations` / `netplus.ops`, `secplus.operations` / `secplus.ops`,
   `aplus2.operational_procedures` / `aplus2.ops`,
   `aplus1.troubleshooting` / `aplus1.hardware_troubleshooting`.
3. Replace the `secplus.*` benchmarks with the SY0-701 five (§3).
4. Add benchmarks for `cyber.foundations`, `nocti.security`, `web.frontend`, and a `techplus`
   cert track with its six domains — 100+ tagged entries currently have no benchmark.
5. Add `nocti.cyber.*` benchmarks for the six 4324 areas (§1.2).
6. Align `scripts/tag-competency-domains.mjs` last, once the target ids are settled. Note that
   running it today would rewrite content ids — treat it as dormant until this is resolved.

---

## 6) Build Order

| Phase | Work | Depends on |
|---|---|---|
Ordered by what students are actually measured on.

**Tier 1 — serves the credential students must pass (CIP 11.0901 / NOCTI 4514)**

| # | Work | Depends on |
|---|---|---|
| 1 | Build the 4514 performance labs (§4), Job 2 first at 61% | nothing |
| 2 | Audit `network-engineer` + `pc-technician` coverage against the 4514 written competency list (§7) | nothing |
| 3 | Close whatever gaps that audit finds | 2 |

**Tier 2 — repo health, unblocks everything else**

| # | Work | Depends on |
|---|---|---|
| 4 | ✅ Retire the three orphan domain ids (§5.4) | done |
| 5 | Fix domain taxonomy (§5.5) | **the server registry** |
| 6 | Audit the 21 `assessment-1-x-x` pc-technician quizzes (opaque slugs, scattered modules) | nothing |

**Tier 3 — year-three cyber, build as capacity allows**

| # | Work | Depends on |
|---|---|---|
| 7 | Confirm 4324 weightings from the PDF chart (§1.1) | nothing |
| 8 | Create 6 `cfs.*` modules, migrate 4 existing lessons + 5 quizzes | 5 |
| 9 | Add `sharedWith` for the 4 cross-track lessons (§2.2) | 8 |
| 10 | Author `cfs` lessons, module by module, heaviest NOCTI weight first | 7, 8 |
| 11 | Create 5 `sec.*` SY0-701 modules, remap the existing 12 lessons | 5 |
| 12 | Author `sec` lessons, domain by domain, 4.0 first at 28% | 11 |
| 13 | Placement exams for all tracks | 3, 10, 12 |

Items 1, 2, 6 and 7 are independent of each other and of everything else.

**The critical path is Tier 1.** An earlier draft of this document put `cfs` authoring on the
critical path; that was wrong. Cyber is a third-year stretch for a two-year A+/Net+ program,
and no cyber content affects whether students pass the credential the program is accountable for.

---

## 7) NOCTI Computer Networking Fundamentals (4514) — The Credential That Counts

Job Ready credential. CIP **11.0901**. Written 194 questions / 3 hours, plus the 2-hour
performance component in §4. Copyright 2016, Version 01. Revision team: GA, NY, OK, PA.

Eleven duty areas. **Weightings carry the same chart-pairing caveat as §1.1** — the published
percentages are 11 · 10 · 6 · 5 · 6 · 10 · 7 · 12 · 10 · 12 · 11, but they cannot be paired to
their labels by text extraction. Confirm from page 3 of the blueprint.

**PC Principles** — physical and equipment safety and maintenance · storage methods · memory ·
eSATA, Bluetooth, USB · processor types and standards · client operating systems

**Network Connections** — NICs · physical and logical characteristics of connections ·
remote access · wired and wireless communications and standards

**Physical Connection Types** — cable components and uses, twisted pair and fiber ·
signal characteristics and transmission across media types

**Network Standards and Devices** — OSI model layers · TCP/IP model · IEEE and EIA/TIA
standards and common port numbers · wired network devices · wireless network devices

**Network Troubleshooting** — ping, ipconfig, tracert, netstat · maintain and troubleshoot
cabling · local and remote loopback · troubleshooting methodologies · packet capture

**Routing and Switching** — static, dynamic, default and gateway routes · WAN connection types ·
basic router operations and configuration · switch operations and configuration ·
routed vs routing protocols · collision vs broadcast domains

**Network Terminology** — protocol and architecture terminology · DHCP and DNS ·
network operating systems · network types

**Network Architecture** — physical and logical topologies · LAN, MAN, PAN, WLAN, WAN topologies

**Network Addressing** — IP network addressing · classful vs classless · MAC addressing ·
binary, hexadecimal and decimal conversion · creating subnets from a network address

**Security** — organizational and acceptable use policies · device security procedures ·
defense in depth · network security attacks and breaches · viruses, worms and malware ·
firewalls including NAT · general cryptography concepts

**Network Planning and Design** — analysis and planning concepts · logical vs physical design ·
power protection, backups and UPS · thin clients · installing and troubleshooting physical and
wireless networks to spec · access methods · virtualization

### 7.1 Two observations

**PC Principles is a networking-assessment duty area.** Hardware, storage, memory, processors
and client OS all sit inside 4514. `pc-technician` content therefore serves this credential
directly — the two tracks are not separable for 4514 purposes.

**The Security duty area is served by existing `network-engineer` content**, which already
covers defense in depth, common attacks, hardening, firewalls and wireless security. Cyber-track
work is not required to satisfy it.

---

## 8) Source Material While CYBER.ORG Is Unavailable

`public/resources/` holds nothing for either cyber track, and the CYBER.ORG account is pending
a reset. The NOCTI and CompTIA blueprints give the competency spine but no teaching content.

Per VOICE_AND_TONE.md, external material is a source of **facts, topic coverage, and objective
mapping only** — never prose. Everything is rewritten in the beattieNetTrack voice. That
sidesteps most licensing friction, but attribution for structure and figures is still good
practice, and worth getting right in a school setting.

**Unambiguously free — US government works, public domain, no licence conditions.** These are
the strongest option and map directly onto 4324's competency areas:

- **NIST SP 800-61** (incident handling) → 4324 "Communicate incident handling and the response process"
- **NIST SP 800-86** (forensics into IR) → the entire Computer Forensics area, including order of volatility and chain of custody
- **NIST SP 800-63** (digital identity) → Identification, Authentication, and Authorization
- **NIST SP 800-30 / 800-37** (risk) → Risk and Threat Analysis Introduction
- **NIST CSF 2.0** → a clean framing for Security Controls
- **CISA** advisories, Secure by Design material, and free training → current, concrete examples

**Open courseware — usable, but check the licence per item.** MIT OpenCourseWare and Harvard's
CS50 both publish under Creative Commons variants that are typically **BY-NC-SA**: attribution
required, non-commercial only, and derivatives must be shared under the same terms. Classroom
use is squarely non-commercial, but the share-alike condition matters if material is ever
redistributed beyond the school. Confirm the licence on each specific course page rather than
assuming it applies across the institution.

**picoCTF (Carnegie Mellon).** The primer and picoGym are built for exactly this audience and
are an excellent fit for the offensive-technique lessons already on `cybersecurity-engineer`.
Best used as **linked practice** rather than ingested content — point students at picoGym
challenges from a lesson, so no licensing question arises and the challenges stay maintained
upstream. Confirm terms before copying any challenge text into the repo.

### 8.1 Decision — NIST and CISA (instructor, 2026-09-08)

**Cyber content is sourced from NIST and CISA.** Public domain, authoritative, no licence
conditions, and maps cleanly onto the 4324 areas. picoCTF is used as *linked* hands-on
practice rather than ingested content. MIT/Harvard OCW is structural reference only.
Reconcile against CYBER.ORG once that account is restored, rather than waiting on it.

### 8.2 "NIST framework" means two different things — don't conflate them

This matters for how CYBER.ORG and NIST relate, and the answer is that they are complementary
rather than duplicative:

**The NICE Framework (NIST SP 800-181r1)** is a workforce *taxonomy* — categories, work roles,
and Knowledge/Skill statements. Education programs align *to* it. It is a mapping and labelling
layer that says which job a course prepares a student for. It supplies **no teaching content**.

**NIST CSF 2.0 and the SP 800-series** are an organizational risk framework and technical
guidance respectively. This is subject matter — the actual substance a lesson teaches.

CISA states that its own courses are aligned to NICE work roles, and CYBER.ORG is CISA-funded,
so a CYBER.ORG "NIST alignment" claim is very likely a **NICE** mapping. That is a statement
about which work roles the curriculum targets — not a claim that the courses reproduce SP 800
guidance.

**Unverified:** CYBER.ORG's standards page returns HTTP 403 to automated fetches and no
explicit alignment statement surfaced in search. Treat the NICE inference as probable, not
confirmed, and check `cyber.org/standards` in a browser when convenient.

**So there is no duplication.** Drawing facts from SP 800-86 for a forensics lesson is a
different activity from tagging that lesson to a NICE work role. Both are worth doing, and
NICE work-role tags would slot naturally alongside the existing `domains[]` frontmatter as a
future addition.

### 8.3 Mapping the 4324 areas to specific NIST sources

| 4324 area | Primary NIST/CISA source |
|---|---|
| Cybersecurity Fundamentals | NIST CSF 2.0 (Govern/Identify/Protect/Detect/Respond/Recover); SP 800-61 for the IR process |
| Cryptography | SP 800-175B (using cryptographic standards); FIPS 197 (AES), FIPS 180-4 (SHA), FIPS 186 (signatures) |
| Risk and Threat Analysis Introduction | SP 800-30 (risk assessment), SP 800-37 (RMF), SP 800-83 (malware incident prevention) |
| Security Controls | SP 800-53r5 (control catalogue and families), CSF 2.0 Protect function |
| Identification, Authentication, and Authorization | SP 800-63-3 suite (identity, authenticators, federation), SP 800-162 (ABAC) |
| Computer Forensics | SP 800-86 (forensics into incident response) — order of volatility, imaging, chain of custody |

SP 800-53r5 is a control *catalogue*, not a lesson — mine it for the control families and
representative examples rather than trying to teach it. SP 800-63 is written for federal
identity systems; take the factor model and authenticator assurance concepts, leave the
federal assurance-level machinery.

---


## 9) Open Questions

1. ~~**CIP alignment.**~~ **Resolved 2026-09-08** — CIP 11.0901 now, moving to 11.1003 in about
   two years. Students must pass NOCTI 4514; cyber is a third-year stretch. See §0.
2. ~~**Source material.**~~ **Resolved 2026-09-08** — NIST and CISA, per §8.1. picoCTF as linked
   practice. Reconcile with CYBER.ORG when that account is restored.
3. ~~**Migration vs additive.**~~ **Resolved 2026-09-08** — progress is keyed on `lessonSlug`
   in `src/lib/progressStore.ts`, not on `moduleId`, so moving a lesson between modules
   preserves completion state. Constitution §14 is accurate. Safe to migrate.
4. ~~**NOCTI performance jobs.**~~ **Withdrawn 2026-09-08** — the sample jobs in the 2016
   blueprint are not the jobs administered. Performance work deferred; see §4.
5. **4324 weightings.** Which pairing is correct in §1.1? Needs a look at page 3 of the PDF.
6. **Module ID convention.** Existing modules mix two and three segments
   (`sec.crypto.basics` vs proposed `sec.threats`). CLAUDE.md specifies
   `{track-slug}.{domain-or-topic}`. Confirm the two-segment form for the new modules.
7. **Domain registry.** Blocked on the SSO-gated `/api/cis/domains`; see §5.5. New `cfs.*`
   modules can proceed meanwhile by using the established `cyber.foundations` id.
8. **CYBER.ORG standards alignment.** NICE is the probable mapping but is unconfirmed; see §8.2.

---

## Sources

- NOCTI Cybersecurity Fundamentals (4324), Foundational Credential Blueprint, 2024 v01 —
  https://nocti.org/wp-content/uploads/Blueprints/FoundCyberFund4324.pdf
- NOCTI Computer Networking Fundamentals (4514), Job Ready Credential Blueprint, 2016 v01 —
  https://www.nocti.org/wp-content/uploads/Blueprints/JRComNtwkgFund4514.pdf
- CompTIA Security+ SY0-701 domain weights — confirm against the current official exam
  objectives PDF before authoring to sub-objective numbers.
