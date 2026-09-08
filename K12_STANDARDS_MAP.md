# K12_STANDARDS_MAP.md

The CYBER.ORG K-12 Cybersecurity Learning Standards, 9th–12th grade band, mapped against
existing repo content.

**Source.** K-12 Cybersecurity Learning Standards v1.0, published 4 August 2021.
© 2021 Cyber Innovation Center & CYBER.ORG, licensed under
**Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**.
The document states: *"Authorization to reproduce this report in whole or in part is granted."*
Suggested citation: K-12 Cybersecurity Learning Standards. (2021). Retrieved from
https://cyber.org/standards.

Standard codes and statements below are reproduced from that document under CC BY-NC 4.0.
Coverage assessments and lesson mappings are ours.

*Extracted and mapped 2026-09-08.*

---

## 1) Structure

Three core concepts, eight strands, 29 topics. The 9–12 band has **31 standards** (two topics,
`PROT` and `PPI`, carry numbered sub-standards).

| Core concept | Strands | Topics |
|---|---|---|
| **Computing Systems (CS)** | Communication and Networking · Hardware · Software | COMM, COMP, CC, PROT, LOSS · HARD, IOT, OS · SOFT, PROG, APPS |
| **Digital Citizenship (DC)** | Online Safety · Ethics · Policy and Legal Issues | CYBL, FOOT, PII* · THRT, ETH · LAW, IP, AUP |
| **Security (SEC)** | Information Security · Network Security · Physical Security | CIA, ACC, DATA, INFO, CRYP · AUTH, COMP, NET · PHYS, CTRL |

\* The taxonomy page calls this topic **PII** (Personally Identifiable Information) but every
standard code in the document is written **`PPI`**. That looks like a typo in the source.
Codes below are reproduced verbatim; if these are ever entered as data, decide which spelling
is canonical and note the deviation.

Note `COMP` appears twice with different meanings: `CS.COMP` is *Network Components*,
`SEC.COMP` is *Securing Network Components*. The core-concept prefix disambiguates them.

---

## 2) Headline Finding

**The Security strand is already largely covered. Digital Citizenship is the real gap.**

| Status | CS (12) | DC (9) | SEC (10) | Total (31) |
|---|---|---|---|---|
| ✅ Covered | 7 | 0 | 8 | **15** |
| ⚠️ Partial | 4 | 3 | 1 | **8** |
| ❌ Gap | 1 | 6 | 1 | **8** |

This inverts the assumption in `CYBER_PATHWAY_STRUCTURE.md`. That document treated cyber as a
large greenfield build. Against *these* standards the technical content is mostly there — it
is spread across `network-engineer`, `pc-technician`, and `tech-plus` rather than sitting on a
cyber track, but the standards do not care which track a lesson lives on.

What is genuinely missing is the **Digital Citizenship** strand: ethics, law, intellectual
property, digital footprint, cyberbullying, and threat-actor motivation. Seven of nine DC
standards have no coverage at all. That is a curriculum-shaped gap, not an infrastructure one,
and it is the cheapest remaining route to standards coverage.

It is also the part a purely technical curriculum tends to skip, and the part a state or
district review is most likely to ask about.

---

## 3) Computing Systems (CS)

| Code | Standard | Status | Existing content |
|---|---|---|---|
| `9-12.CS.COMM` | Explain layers within the OSI networking model. | ✅ | `net-osi-model`, `net-encapsulation-decapsulation` |
| `9-12.CS.COMP` | Create a diagram of a network utilizing appropriate network components. | ⚠️ | `net-network-topologies`, `net-corporate-datacenter-architecture` teach the components, but the verb is **create a diagram** — needs a build/produce activity, not a reading |
| `9-12.CS.CC` | Evaluate the risks and benefits of cloud computing. | ✅ | `net-cloud-concepts`, `tech-plus-2-6-1-virtualization-cloud-technologies` |
| `9-12.CS.PROT.1` | Compare and contrast the ports and protocols used for different services available online. | ✅ | `net-common-ports`, `net-protocols` |
| `9-12.CS.PROT.2` | Identify the risks associated with the different services available online. | ⚠️ | `net-common-network-attacks` covers protocol attacks; service-level risk framing is thinner |
| `9-12.CS.LOSS` | Develop a plan for risk mitigation that implements redundancy. | ⚠️ | `net-high-availability` covers redundancy and backups. **Confirmed: "hot site" / "cold site" appear nowhere in the repo** — the clarification names them explicitly, so this is a named-term gap inside an otherwise-covered lesson. Cheapest fix in the whole map |
| `9-12.CS.HARD` | Identify methods of mitigating risk associated with connecting devices. | ⚠️ | `net-network-hardening` partially; device-connection risk is not the same framing |
| `9-12.CS.IOT` | Analyze the vulnerabilities of Internet of Things devices. | ✅ | `tech-plus-2-1-2-iot-devices` |
| `9-12.CS.OS` | Create a plan for hardening an operating system. | ✅ | `pct-windows-security`, `tech-plus-6-2-2-securing-devices`, lab `pct-windows-security-hardening-lab` |
| `9-12.CS.SOFT` | Compare the advantages and disadvantages of patching systems in real time. | ⚠️ | `net-change-management` touches change control; the real-time-patching trade-off is not argued |
| `9-12.CS.PROG` | Describe the role of scripting in cyber attacks and cyber defense. | ❌ | **Gap.** `linux-cli-survival` teaches CLI, not scripting as attack/defense capability |
| `9-12.CS.APPS` | Discuss how software across platforms can monitor, collect, and analyze information. | ✅ | `net-firewalls-ids-ips`, `net-network-monitoring`; SIEM in quiz `net-4-1-5-security-information-and-event-management` |

---

## 4) Digital Citizenship (DC) — the gap

| Code | Standard | Status | Existing content |
|---|---|---|---|
| `9-12.DC.CYBL` | Prepare a plan to raise awareness of the effects of cyberbullying. | ❌ | **Gap.** Nothing |
| `9-12.DC.FOOT` | Examine the implications of both positive and negative digital footprints. | ❌ | **Gap.** Nothing |
| `9-12.DC.PPI.1` | Explain the importance of social identity and the implications of online activity regarding private data, long-term career impacts, and the permanence of digital data. | ❌ | **Gap.** `tech-plus-6-1-4-privacy` is adjacent but does not cover permanence or career impact |
| `9-12.DC.PPI.2` | Explain the individual risks of a data breach to an organization housing personal data. | ⚠️ | `tech-plus-6-1-4-privacy` partially |
| `9-12.DC.THRT` | Analyze the motives of threat actors. | ❌ | **Gap.** Also a Security+ SY0-701 objective (2.1 threat actors and motivations) — one lesson serves both |
| `9-12.DC.ETH` | Discuss the role that cyber ethics plays in current society. | ⚠️ | The Ethical Use sections added to the twelve `cybersecurity-engineer` lessons cover authorization, not ethics as a societal topic |
| `9-12.DC.LAW` | Compare and contrast local, state, federal, and international cyber laws and regulations for individuals and businesses. | ❌ | **Gap.** Clarification names **COPPA** and **GDPR** |
| `9-12.DC.IP` | Debate the importance of intellectual property laws. | ❌ | **Gap.** Nothing |
| `9-12.DC.AUP` | Differentiate between the various agreements that protect individuals and organizations in their digital environments. | ⚠️ | Better covered than it first appeared: `net-policies-procedures` covers **AUP** thoroughly (11 mentions), `tech-plus-6-2-3-device-use-best-practices` and `tech-plus-3-3-1-productivity-software` cover **EULA**, `net-wireless-security-threats` mentions **terms of service**. The pieces are scattered across three tracks and never *differentiated* side by side, which is what the standard asks for |

**Note the verbs.** DC standards ask students to *prepare a plan*, *debate*, *examine*,
*discuss*, *analyze*. These are discussion and production standards, not recall. The repo's
lesson shape — authored sections with four-option checks — fits recall well and argument
poorly. Meeting the DC strand honestly probably needs a different activity type: a structured
debate prompt, a written position, or a plan artifact. Worth deciding before authoring nine
lessons that quietly convert "debate the importance of IP law" into a multiple-choice question.

---

## 5) Security (SEC)

| Code | Standard | Status | Existing content |
|---|---|---|---|
| `9-12.SEC.CIA` | Explain various interactions between the CIA Triad and the three states of data. | ⚠️ | `cfs-1-1-1-cia-triad` covers the triad and names data at rest and in transit, but not **data in use**. `net-data-loss-prevention` covers all three states properly. Both halves exist in different lessons — the *interaction* between them is what is missing, and one section added to `cfs-1-1-1-cia-triad` closes it |
| `9-12.SEC.ACC` | Compare and contrast access control principles, access control modules, and the principle of least privilege. | ❌ | **Gap.** Clarification names **MAC, RBAC, DAC**. `auth-demo` covers authn/authz but not the models |
| `9-12.SEC.DATA` | Formulate a plan to apply security measures to protect data in all three states. | ✅ | **Corrected from a gap.** `net-data-loss-prevention` covers data at rest, in transit, and in use, with protections for each |
| `9-12.SEC.INFO` | Distinguish the different types of attacks that affect information security for individuals and organizations. | ✅ | `cfs-1-1-2-threat-vulnerability-risk`, `net-common-network-attacks` |
| `9-12.SEC.CRYP` | Analyze how modern advancements in computing have impacted encryption. | ✅ | `cryptography`, `tech-plus-6-4-1-plain-text-vs-cipher-text`, `password-hashing` |
| `9-12.SEC.AUTH` | Evaluate authentication and authorization methods and the risks associated with failure. | ✅ | `auth-demo`, `tech-plus-6-1-5-aaa-authentication`, `tech-plus-6-1-6-aaa-authorization` |
| `9-12.SEC.COMP` | Evaluate Defense in Depth strategies that can protect simple networks. | ✅ | `net-network-hardening`, quiz `net-4-1-2-defense-in-depth` |
| `9-12.SEC.NET` | Analyze the different types of attacks that affect network security. | ✅ | `net-common-network-attacks`, `net-troubleshooting-security`, `net-wireless-security-threats` |
| `9-12.SEC.PHYS` | Analyze the different types of attacks that affect physical security. | ✅ | `net-physical-security`, `cfs-1-1-3-social-engineering` |
| `9-12.SEC.CTRL` | Justify the use of Defense in Depth and the need for physical access controls. | ✅ | `net-physical-security` (proximity badges, PIN codes, mantraps) |

---

## 6) What This Changes

**`CYBER_PATHWAY_STRUCTURE.md` §2 needs revisiting.** That section proposed six
`cfs.*` modules built from the NOCTI 4324 areas. These standards are a different and more
locally-relevant spine — CYBER.ORG's own courses are built on them, and they are what a state
or district review will recognise. The two are not in conflict (4324 areas map cleanly onto
the SEC strand plus parts of CS), but the module structure should be decided against one of
them deliberately rather than inheriting 4324 by default.

**Coverage is a cross-track property.** Fourteen standards are already met by
`network-engineer`, `pc-technician`, and `tech-plus`. Any claim of standards coverage should be
computed across all tracks, not per track.

**Suggested addition: standards tags in frontmatter.** A `standards: ["9-12.SEC.CIA"]` array
alongside the existing `domains[]` would let `validate:tracks` report coverage automatically
instead of this table going stale. Low cost, and it makes the coverage claim auditable.

---

## 7) Open Questions

1. **PII vs PPI.** The source taxonomy says PII, every code says `PPI`. Which is canonical here?
2. **DC activity type.** Nine standards use debate/plan/examine verbs. Does the repo need a new
   activity shape for these, or are they served outside the LMS?
3. **Spine choice.** Structure `cybersecurity-foundations` against these standards, against
   NOCTI 4324, or map both onto one module set?
4. ~~**Three unconfirmed partials.**~~ **Checked 2026-09-08.** Hot/cold sites appear nowhere in
   the repo. `net-data-loss-prevention` covers all three data states properly, which moves
   `9-12.SEC.DATA` from gap to covered. AUP, EULA, and terms of service each appear, but on
   three different tracks and never contrasted. Results folded into the tables above.

---

## 8) Cheapest Route to Coverage

Ordered by effort, not importance. The first three are edits to existing lessons, not new ones.

1. **Add hot/warm/cold sites to `net-high-availability`.** One section. Closes `9-12.CS.LOSS`
   and it is Net+ content anyway.
2. **Add data-in-use to `cfs-1-1-1-cia-triad`** and connect the triad to the three states.
   Closes `9-12.SEC.CIA`. The material already exists in `net-data-loss-prevention` to draw on.
3. **Add an AUP / TOS / EULA comparison** to `net-policies-procedures`. Closes `9-12.DC.AUP`.
4. **Author `9-12.SEC.ACC`** — MAC, DAC, RBAC, and least privilege. One lesson, also
   Security+ 4.6 material, so it earns its place twice.
5. **Author `9-12.DC.THRT`** — threat actor motives. Also Security+ 2.1. Earns its place twice.
6. **Author `9-12.CS.PROG`** — scripting in attack and defense. Pairs naturally with the
   existing `linux-cli-survival`.
7. **The remaining six DC standards** — cyberbullying, digital footprint, PPI.1, ethics, law,
   intellectual property. These need the activity-shape decision in §7 item 2 first.

Steps 1–3 move three standards for roughly the effort of one new lesson.
