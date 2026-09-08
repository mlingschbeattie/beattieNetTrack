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

**The program is CIP 11.0901 today and is moving to CIP 11.1003 within two years**
(instructor decision, 2026-09-08). 11.0901 is stamped on the *networking* blueprint (4514);
11.1003 is stamped on the *cybersecurity* blueprint (4324).

That decision settles the target and sets the sequencing:

1. **4324 Cybersecurity Fundamentals is the destination credential.** Building
   `cybersecurity-foundations` against its six areas (§2) is the right long-term investment
   and should proceed now — it takes more than two years of authoring to fill anyway.
2. **4514 remains the live credential during the transition window.** It is a Job Ready
   assessment with a **performance component** (2 hours, 2 hands-on jobs) that nothing in
   the repo targets. See §4. This is time-boxed work with a closing window, not permanent
   infrastructure — scope it accordingly.
3. **Cyber content is assessed under both codes.** 4514 carries a Security duty area of its
   own, so foundations content earns its keep before the CIP change lands, not only after.

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

## 4) The 4514 Performance Component — Currently Unserved

NOCTI 4514 is the credential aligned to CIP 11.0901 and includes a 2-hour **performance**
assessment worth its own score. Nothing in the repo targets it.

| Job | Weight | Task |
|---|---|---|
| 1 | 39% | Select and connect equipment for a simple two-workstation LAN; assign a private IPv4 Class C address and subnet; record results; verify IP connectivity |
| 2 | 61% | Name workstations; join workgroup `NOCTI`; create users; create folders; create a share; grant permissions; access-test; install a plug-and-play printer, set default, share, and print to verify |

Both map cleanly to the existing `steps` lab shape (`LabRunner` with exact/oneOf/regex/choice
validators), which the handoff notes is the preferred and most reliable lab type.

Proposed: two labs on `network-engineer`, mirroring the job structure and weighting.

With the CIP moving to 11.1003 (§0), this work has a closing window — it serves students
sitting 4514 between now and the change, then stops mattering for credentialing. Two `steps`
labs is the right size for it. Do not build performance-assessment infrastructure beyond that;
the hands-on skills themselves (addressing, shares, permissions, printers) stay valuable on
`pc-technician` regardless of which credential is current.

---

## 5) Domain Taxonomy Must Be Fixed First

The `domains[]` frontmatter and the competency dashboard do not agree. Any structure built
on top inherits the fault. `CIS_DOMAIN_BENCHMARKS` in `src/components/teacher/ClassRoster.tsx`
is the dashboard's source of truth; content frontmatter and `scripts/tag-competency-domains.mjs`
both diverge from it.

| Benchmark ID (dashboard) | Content frontmatter uses | Tagging script emits | Status |
|---|---|---|---|
| `secplus.ops` | `secplus.operations` | `secplus.operations` | **never rolls up** |
| `netplus.ops` | `netplus.operations` | — | **never rolls up** |
| `netplus.networking` | `netplus.networking` | `netplus.networking_concepts` | script wrong |
| `aplus2.ops` | `aplus2.operational` | `aplus2.operational_procedures` | **all three differ** |
| `aplus1.hardware_troubleshooting` | `aplus1.troubleshooting` | `aplus1.troubleshooting` | **never rolls up** |
| `secplus.implementation` | — | — | benchmark unused |
| `secplus.governance` | — | — | benchmark unused |
| — | `cyber.foundations` (21 uses) | yes | **no benchmark exists** |
| — | `techplus.*` (100+ uses) | yes | **no benchmark, no cert track** |
| — | `nocti.security` (2 uses) | yes | **no benchmark exists** |
| — | `secops.basics` (1 use) | — | orphan, likely a typo |

Additionally, `CIS_DOMAIN_BENCHMARKS` describes **SY0-601** domains (Threats / Architecture /
Implementation / Operations / Governance). The seeds and CLAUDE.md target **SY0-701**, whose
five domains are listed in §3. The benchmark table needs replacing, not patching.

Recommended order of work:

1. Replace the `secplus.*` benchmarks with the SY0-701 five.
2. Add `nocti.cyber.*` benchmarks for the six 4324 areas.
3. Add a `techplus` cert track and its six domains.
4. Reconcile the `.ops` / `.operations` and `aplus1.troubleshooting` id mismatches in one pass
   across benchmarks, content frontmatter, and the tagging script.
5. Retire `secops.basics`.

---

## 6) Build Order

| Phase | Work | Depends on |
|---|---|---|
| 1 | Fix domain taxonomy (§5) | nothing |
| 2 | Confirm 4324 weightings from the PDF chart (§1.1) | nothing |
| 3 | Create 6 `cfs.*` modules, migrate 4 existing lessons + 5 quizzes | 1 |
| 4 | Add `sharedWith` for the 4 cross-track lessons (§2.2) | 3 |
| 5 | Author `cfs` lessons, module by module, heaviest NOCTI weight first | 2, 3 |
| 6 | Build the two 4514 performance labs (§4) — closing window, time-box it | 1 |
| 7 | Create 5 `sec.*` SY0-701 modules, remap the existing 12 lessons | 1 |
| 8 | Author `sec` lessons, domain by domain, 4.0 first at 28% | 7 |
| 9 | Placement exams for both tracks | 5, 8 |

Phases 1, 2 and 6 are independent of each other and of the authoring work.

With 11.1003 confirmed as the destination, phase 5 (`cfs` authoring against the 4324
competencies) is the critical path — it is the largest body of work and the credential it
serves is the one the program is moving to.

---

## 7) Open Questions

1. ~~**CIP alignment.**~~ **Resolved 2026-09-08** — the program moves to CIP 11.1003 within
   two years, making NOCTI 4324 the destination credential. 4514 stays live until then; see §0.
2. **4324 weightings.** Which pairing is correct in §1.1?
3. **Module ID convention.** Existing modules mix two and three segments
   (`sec.crypto.basics` vs proposed `sec.threats`). CLAUDE.md specifies
   `{track-slug}.{domain-or-topic}`. Confirm the two-segment form for the new modules.
4. **Migration vs additive.** §2 and §3.1 move existing lessons between modules. Module IDs
   are referenced by progress tracking — confirm whether completion state is keyed on
   `lesson_slug` alone (Constitution §14 says it is) before moving anything.
5. **Source material.** `public/resources/` has nothing for either cyber track. The NOCTI
   blueprints give the competency spine but no teaching content. Confirm whether CYBER.ORG
   243/368/100 material is available to draw facts from.

---

## Sources

- NOCTI Cybersecurity Fundamentals (4324), Foundational Credential Blueprint, 2024 v01 —
  https://nocti.org/wp-content/uploads/Blueprints/FoundCyberFund4324.pdf
- NOCTI Computer Networking Fundamentals (4514), Job Ready Credential Blueprint, 2016 v01 —
  https://www.nocti.org/wp-content/uploads/Blueprints/JRComNtwkgFund4514.pdf
- CompTIA Security+ SY0-701 domain weights — confirm against the current official exam
  objectives PDF before authoring to sub-objective numbers.
