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
| ✅ Covered | 8 | 4 | 10 | **22** |
| ⚠️ Partial | 3 | 3 | 0 | **6** |
| ❌ Gap | 1 | 2 | 0 | **3** |

*Updated 2026-09-08. Closed `CS.LOSS`, `SEC.CIA`, `DC.AUP`, `DC.THRT`, `DC.FOOT` and `DC.PPI.1`;
corrected `SEC.ACC` (was wrongly a gap — fully covered on tech-plus), and `DC.LAW` / `DC.IP`
from gap to partial. Only three genuine gaps remain, all in the Online Safety and Software
strands. See §8.*

This inverts the assumption in `CYBER_PATHWAY_STRUCTURE.md`. That document treated cyber as a
large greenfield build. Against *these* standards the technical content is mostly there — it
is spread across `network-engineer`, `pc-technician`, and `tech-plus` rather than sitting on a
cyber track, but the standards do not care which track a lesson lives on.

What is genuinely missing is the **Digital Citizenship** strand: ethics, law, intellectual
property, digital footprint, cyberbullying, and threat-actor motivation. Six of nine DC
standards still have no coverage at all. That is a curriculum-shaped gap, not an infrastructure
one, and it is the cheapest remaining route to standards coverage.

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
| `9-12.CS.LOSS` | Develop a plan for risk mitigation that implements redundancy. | ✅ | **Closed 2026-09-08.** `net-high-availability` already covered redundancy, backups and hot/warm/cold *standby*; added a Recovery Sites section covering hot/warm/cold *sites*, offsite backups, geographic separation and plan testing, plus a matching Learn section |
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
| `9-12.DC.FOOT` | Examine the implications of both positive and negative digital footprints. | ✅ | **Closed 2026-09-08.** New lesson `cfs-1-1-5-digital-footprint` covers active vs passive footprints, permanence, and ethical, societal and career implications — including the positive case, which the standard explicitly asks for |
| `9-12.DC.PPI.1` | Explain the importance of social identity and the implications of online activity regarding private data, long-term career impacts, and the permanence of digital data. | ✅ | **Closed 2026-09-08.** `cfs-1-1-5-digital-footprint` covers digital permanence, data aggregation, hiring and admissions, and separating professional from personal identity |
| `9-12.DC.PPI.2` | Explain the individual risks of a data breach to an organization housing personal data. | ⚠️ | `tech-plus-6-1-4-privacy` partially |
| `9-12.DC.THRT` | Analyze the motives of threat actors. | ✅ | **Corrected then closed 2026-09-08.** `cfs-1-1-2-threat-vulnerability-risk` already had a Threat Actor Taxonomy (script kiddies, organised crime, APTs, insiders), so this was a partial, not a gap. Added a motive-centric section — financial, political, ideological, malice — since the standard asks students to analyse *motives*, not enumerate actor types |
| `9-12.DC.ETH` | Discuss the role that cyber ethics plays in current society. | ⚠️ | The Ethical Use sections added to the twelve `cybersecurity-engineer` lessons cover authorization, not ethics as a societal topic |
| `9-12.DC.LAW` | Compare and contrast local, state, federal, and international cyber laws and regulations for individuals and businesses. | ⚠️ | **Corrected from gap.** COPPA, GDPR, HIPAA and FERPA appear across `cfs-1-1-2`, `net-cloud-concepts`, `net-data-loss-prevention` and `net-policies-procedures`; CFAA appears in `sql-injection` and `web-exploitation`. Scattered and never *compared* across jurisdictions, which is what the standard asks |
| `9-12.DC.IP` | Debate the importance of intellectual property laws. | ⚠️ | **Corrected from gap.** `tech-plus-6-1-1-confidentiality-concerns` covers intellectual property as an asset class and `tech-plus-6-2-3-device-use-best-practices` covers copyright. The *debate* verb is unserved — see the activity-shape note below |
| `9-12.DC.AUP` | Differentiate between the various agreements that protect individuals and organizations in their digital environments. | ✅ | **Closed 2026-09-08.** Added an AUP / TOS / EULA section to `net-policies-procedures` contrasting all three on who wrote it and whose interests it protects, plus which clauses actually matter in each — the differentiation the standard asks for, which no single lesson previously did |

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
| `9-12.SEC.CIA` | Explain various interactions between the CIA Triad and the three states of data. | ✅ | **Closed 2026-09-08.** Added a Three States of Data section to `cfs-1-1-1-cia-triad` covering at rest, in transit and in use, with a 3x3 matrix of how each triad property fails in each state — which is the *interaction* the standard asks students to explain |
| `9-12.SEC.ACC` | Compare and contrast access control principles, access control modules, and the principle of least privilege. | ✅ | **Corrected 2026-09-08 — was wrongly marked a gap.** `tech-plus-6-1-6-aaa-authorization` is titled *AAA Framework — Authorization and Access Control Models* and has authored sections on RBAC vs DAC vs MAC vs ABAC and on least privilege and separation of duties. `tech-plus-6-1-5-aaa-authentication` supplies the identify/authenticate half. Fully covered, on the tech-plus track |
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

1. ✅ **Done 2026-09-08.** Hot/warm/cold *sites* added to `net-high-availability` as a Recovery
   Sites section, distinct from the hot/warm/cold *standby* material already there. Closed
   `9-12.CS.LOSS`.
2. ✅ **Done 2026-09-08.** Three States of Data section added to `cfs-1-1-1-cia-triad`, with a
   3×3 matrix of how each triad property fails at rest, in transit, and in use. Closed
   `9-12.SEC.CIA`.
3. ✅ **Done 2026-09-08.** AUP / TOS / EULA comparison added to `net-policies-procedures`,
   contrasting authorship and whose interests each protects. Closed `9-12.DC.AUP`.

Each of the three added a Learn section as well as body prose, so all three lessons went from
three authored sections to four. Coverage moved 15 → 18 for roughly the effort of one new
lesson, as estimated.

Remaining, in the same order:

4. ✅ **Corrected 2026-09-08 — not needed.** `9-12.SEC.ACC` was already fully covered by
   `tech-plus-6-1-6-aaa-authorization`. Authoring it would have duplicated existing content.
5. ✅ **Done 2026-09-08.** `9-12.DC.THRT` turned out to be a partial rather than a gap —
   `cfs-1-1-2` already had an actor taxonomy — so it was closed with a motive-centric section
   rather than a new lesson.
6. ✅ **Done 2026-09-08.** New lesson `cfs-1-1-5-digital-footprint` closed both `9-12.DC.FOOT`
   and `9-12.DC.PPI.1`, which are the same subject from two angles.

Remaining:

7. **Author `9-12.CS.PROG`** — scripting in attack and defense. Pairs naturally with the
   existing `linux-cli-survival`. The last non-DC gap.
8. **`9-12.DC.CYBL`** — cyberbullying. Needs the activity-shape decision in §7 item 2, since
   the standard asks students to *prepare a plan*.
9. **`9-12.DC.LAW` and `9-12.DC.IP`** — both partials with material scattered across tracks.
   `DC.IP` asks students to *debate*, so it hits the same activity-shape question.

**A caution learned the hard way.** Four of the original gap assessments were wrong because
coverage was judged against cyber-track lessons for cyber-shaped standards, despite §2 of this
document stating that coverage is cross-track. Before authoring anything against a standard,
grep the whole of `src/content/` for its key terms first. Two of the four would have produced
duplicate lessons.

