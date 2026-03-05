# Network Engineer Track — Module Map v1

**Status:** Approved architecture  
**Date:** 2026-03-05  
**Track slug:** `network-engineer`  
**Certification target:** CompTIA Network+ (N10-008 / N10-009)  
**Content sources:** CYBER.ORG curriculum + CompTIA objectives

---

## 1. Complete Module Map

The track expands from 8 stub modules to **14 modules** organized across all 5 CompTIA domains. Every CYBER.ORG unit and every N10-009 objective has a home. Each module targets 3–6 activities.

---

### Domain 1 — Networking Concepts (net.fundamentals.*)

#### Module 1: `net.fundamentals.models-and-standards`

| Field | Value |
|---|---|
| **Title** | Models & Standards |
| **Description** | OSI model, TCP/IP model, encapsulation, and the standards mindset. |
| **CompTIA Objectives** | N10-009 1.1 (OSI model layers) |
| **CYBER.ORG Units** | 1.1.1 OSI Model, 1.1.2 Encapsulation and Decapsulation |
| **Recommended Activities** | 4 — lesson (OSI model), lesson (encapsulation), quiz (models checkpoint), lab (packet walk exercise) |
| **Existing?** | **KEEP** as-is (order 1) |

#### Module 2: `net.fundamentals.topologies-and-types`

| Field | Value |
|---|---|
| **Title** | Topologies & Network Types |
| **Description** | Physical and logical topologies, LAN/WAN/MAN/SAN/WLAN types. |
| **CompTIA Objectives** | N10-009 1.2 (network topologies, types) |
| **CYBER.ORG Units** | 1.2.1 Network Topologies, 1.2.2 Network Types |
| **Recommended Activities** | 3 — lesson (topologies), lesson (network types), quiz (topologies checkpoint) |
| **Existing?** | **NEW** |

#### Module 3: `net.fundamentals.cabling-and-connectors`

| Field | Value |
|---|---|
| **Title** | Cabling & Connectors |
| **Description** | Copper cables, fiber-optic, connector types, and cable management. |
| **CompTIA Objectives** | N10-009 1.3 (transmission media, connectors) |
| **CYBER.ORG Units** | 1.3.1 Copper Cables, 1.3.2 Fiber-Optic Cables, 1.3.3 Connector Types, 1.3.4 Cable Management |
| **Recommended Activities** | 5 — lesson (copper & fiber), lesson (connectors), lesson (cable management), quiz (cabling checkpoint), lab (cable identification exercise) |
| **Existing?** | **NEW** |

#### Module 4: `net.fundamentals.addressing`

| Field | Value |
|---|---|
| **Title** | IP Addressing |
| **Description** | Public vs private addresses, IPv4 and IPv6, subnetting fundamentals. |
| **CompTIA Objectives** | N10-009 1.4 (IPv4 addressing, IPv6 concepts), 1.7 (public vs private) |
| **CYBER.ORG Units** | 1.4.1 Public vs Private Networks, 1.4.2 IPv4 and IPv6 |
| **Recommended Activities** | 5 — lesson (IPv4 addressing & subnetting), lesson (IPv6 fundamentals), lesson (public vs private), quiz (addressing checkpoint), lab (subnetting practice) |
| **Existing?** | **KEEP** as-is (order 4, was order 2) |

> **Note:** The existing quiz `network-fundamentals-checkpoint` is currently mapped to this module (`moduleId: net.fundamentals.addressing`). It stays here.

#### Module 5: `net.fundamentals.ports-and-protocols`

| Field | Value |
|---|---|
| **Title** | Ports & Protocols |
| **Description** | Common ports, protocol suites, TCP vs UDP, and protocol analysis. |
| **CompTIA Objectives** | N10-009 1.5 (common ports, protocol types) |
| **CYBER.ORG Units** | 1.5.1 Common Ports, 1.5.2 Protocols |
| **Recommended Activities** | 4 — lesson (common ports), lesson (TCP/UDP & protocol suites), quiz (ports checkpoint), lab (protocol identification exercise) |
| **Existing?** | **NEW** |

#### Module 6: `net.fundamentals.network-services`

| Field | Value |
|---|---|
| **Title** | Core Network Services |
| **Description** | DHCP, DNS, and NTP — how they work and how to configure them. |
| **CompTIA Objectives** | N10-009 1.6 (network services), 3.3 (IPv4/IPv6 services) |
| **CYBER.ORG Units** | 1.6.1 DHCP, 1.6.2 DNS, 1.6.3 NTP |
| **Recommended Activities** | 5 — lesson (DHCP), lesson (DNS), lesson (NTP), quiz (services checkpoint), lab (DNS/DHCP diagnostics) |
| **Existing?** | **RENAME** from `net.services.core-services` → `net.fundamentals.network-services` |

> **Rationale for rename:** DHCP/DNS/NTP align with CompTIA Domain 1 (Networking Concepts) and CYBER.ORG Unit 1.6. Moving from `services` domain to `fundamentals` domain places them where students encounter them in the certification flow. The old `services` domain segment had only this one module and is eliminated.

#### Module 7: `net.fundamentals.architecture`

| Field | Value |
|---|---|
| **Title** | Network Architecture & Cloud |
| **Description** | Corporate/datacenter architecture, cloud concepts, and modern network environments. |
| **CompTIA Objectives** | N10-009 1.7 (corporate/datacenter architecture), 1.8 (cloud concepts) |
| **CYBER.ORG Units** | 1.7.x Corporate and Datacenter Architecture, 1.8.x Cloud Concepts |
| **Recommended Activities** | 4 — lesson (corporate & datacenter design), lesson (cloud concepts: IaaS/PaaS/SaaS), quiz (architecture checkpoint), activity (network diagram exercise) |
| **Existing?** | **NEW** |

---

### Domain 2 — Network Implementation (net.implementation.*)

#### Module 8: `net.implementation.devices`

| Field | Value |
|---|---|
| **Title** | Networking & Networked Devices |
| **Description** | Routers, switches, firewalls, APs, load balancers, and IoT/ICS devices. |
| **CompTIA Objectives** | N10-009 2.1 (networking appliances, networked devices) |
| **CYBER.ORG Units** | 2.1.1 Networking Devices, 2.1.2 Networked Devices |
| **Recommended Activities** | 4 — lesson (networking appliances), lesson (networked & IoT devices), quiz (devices checkpoint), activity (device role matching exercise) |
| **Existing?** | **NEW** |

#### Module 9: `net.implementation.routing`

| Field | Value |
|---|---|
| **Title** | Routing Fundamentals |
| **Description** | Routing tables, static/dynamic routing, NAT/PAT, and bandwidth management. |
| **CompTIA Objectives** | N10-009 2.2 (routing technologies, bandwidth management) |
| **CYBER.ORG Units** | 2.2.1 Routing Tables, 2.2.2 Bandwidth Management |
| **Recommended Activities** | 5 — lesson (routing tables & static routes), lesson (dynamic routing concepts), lesson (NAT/PAT), quiz (routing checkpoint), lab (routing table analysis) |
| **Existing?** | **RENAME** from `net.routing.l3-basics` → `net.implementation.routing` |

> **Rationale:** The old domain `routing` had only one module. Folding into `implementation` aligns with CompTIA Domain 2 and makes room for bandwidth management content from CYBER.ORG 2.2.2.

#### Module 10: `net.implementation.switching`

| Field | Value |
|---|---|
| **Title** | Ethernet Switching |
| **Description** | VLANs, trunking, STP, and Layer 2 forwarding. |
| **CompTIA Objectives** | N10-009 2.3 (Ethernet switching) |
| **CYBER.ORG Units** | 2.3.x Ethernet Switching |
| **Recommended Activities** | 4 — lesson (VLANs & trunking), lesson (STP fundamentals), quiz (switching checkpoint), lab (VLAN configuration exercise) |
| **Existing?** | **RENAME** from `net.switching.l2-basics` → `net.implementation.switching` |

#### Module 11: `net.implementation.wireless`

| Field | Value |
|---|---|
| **Title** | Wireless Networking |
| **Description** | 802.11 standards, wireless security, channels, and site surveys. |
| **CompTIA Objectives** | N10-009 2.4 (wireless standards, configurations) |
| **CYBER.ORG Units** | 2.4.x Wireless Standards |
| **Recommended Activities** | 4 — lesson (802.11 standards & frequencies), lesson (wireless security & encryption), quiz (wireless checkpoint), lab (wireless site survey exercise) |
| **Existing?** | **RENAME** from `net.wireless.wlan-basics` → `net.implementation.wireless` |

---

### Domain 3 — Network Operations (net.operations.*)

#### Module 12: `net.operations.monitoring-and-docs`

| Field | Value |
|---|---|
| **Title** | Monitoring, Documentation & DR |
| **Description** | Performance monitoring, documentation standards, change management, HA, and disaster recovery. |
| **CompTIA Objectives** | N10-009 3.1 (organizational processes), 3.2 (monitoring), 3.4 (high availability/DR) |
| **CYBER.ORG Units** | 3.1.x Performance Monitoring, 3.2.x Documentation and Policies, 3.3.x High Availability and DR |
| **Recommended Activities** | 5 — lesson (network monitoring tools & baselines), lesson (documentation: diagrams, labeling, change control), lesson (HA & disaster recovery), quiz (operations checkpoint), activity (network diagram exercise) |
| **Existing?** | **RENAME** from `net.operations.documentation` → `net.operations.monitoring-and-docs` |

> **Rationale:** The old module covered only documentation. CompTIA Domain 3 bundles monitoring, documentation, and DR into one domain. Merging into one module keeps the activity count at 5 (within the 3–6 target). If content grows, this can be split in a future revision.

---

### Domain 4 — Network Security (net.security.*)

#### Module 13: `net.security.defense`

| Field | Value |
|---|---|
| **Title** | Network Security & Defense |
| **Description** | Security concepts, attack types, hardening, remote access, and physical security. |
| **CompTIA Objectives** | N10-009 4.1 (security concepts), 4.2 (attack types), 4.3 (security features), 4.5 (physical security) |
| **CYBER.ORG Units** | 4.1.2 Creating a Honeypot, 4.2.2 Phishing with SEToolkit, 4.3.x Network Hardening, 4.4.1 Remote Access Methods, 4.5.x Physical Security |
| **Recommended Activities** | 6 — lesson (security concepts & attack types), lesson (hardening & defense techniques), lesson (remote access & physical security), lab (honeypot setup), lab (network hardening exercise), quiz (security checkpoint) |
| **Existing?** | **NEW** |

> **Note:** The CYBER.ORG honeypot and SEToolkit labs are security-focused but need **Educational Safety** framing per CONSTITUTION §13. The phishing lab should be restructured as a *recognition/defense* exercise, not an attack tutorial. The honeypot lab is fine as-is (defensive technique).

---

### Domain 5 — Network Troubleshooting (net.troubleshooting.*)

#### Module 14: `net.troubleshooting.tools-and-methods`

| Field | Value |
|---|---|
| **Title** | Troubleshooting Tools & Methodology |
| **Description** | Troubleshooting methodology, CLI/GUI tools, cable testing, and performance diagnosis. |
| **CompTIA Objectives** | N10-009 5.1 (methodology), 5.2 (cable/physical), 5.3 (services issues), 5.4 (performance), 5.5 (tools) |
| **CYBER.ORG Units** | 5.3.1 Network Software Tools, 5.3.2 Command Line Tools, 5.x.x General Troubleshooting |
| **Recommended Activities** | 6 — lesson (troubleshooting methodology), lesson (CLI tools: ping, traceroute, nslookup, netstat), lesson (cable testing & physical issues), lab (terminal-basics), lab (network-terminal-basics), quiz (troubleshooting checkpoint) |
| **Existing?** | **RENAME** from `net.troubleshooting.tools` → `net.troubleshooting.tools-and-methods` |

> **Note:** Both existing labs (`terminal-basics` and `network-terminal-basics`) are currently mapped to `net.troubleshooting.tools`. They will be remapped to `net.troubleshooting.tools-and-methods`.

---

## 2. Existing Module ID Fate Map

| Current Module ID | Action | New Module ID | Rationale |
|---|---|---|---|
| `net.fundamentals.models-and-standards` | **KEEP** | *(unchanged)* | Perfect fit for CompTIA 1.1 + CYBER.ORG 1.1.x |
| `net.fundamentals.addressing` | **KEEP** | *(unchanged)* | Perfect fit for CompTIA 1.4 + CYBER.ORG 1.4.x |
| `net.switching.l2-basics` | **RENAME** | `net.implementation.switching` | Aligns domain with CompTIA Domain 2; eliminates orphan `switching` domain |
| `net.routing.l3-basics` | **RENAME** | `net.implementation.routing` | Aligns domain with CompTIA Domain 2; merges bandwidth management |
| `net.wireless.wlan-basics` | **RENAME** | `net.implementation.wireless` | Aligns domain with CompTIA Domain 2; eliminates orphan `wireless` domain |
| `net.services.core-services` | **RENAME** | `net.fundamentals.network-services` | Moves to Domain 1 (where DHCP/DNS/NTP live in CompTIA + CYBER.ORG) |
| `net.troubleshooting.tools` | **RENAME** | `net.troubleshooting.tools-and-methods` | Broadens scope to include methodology (CompTIA 5.1) and physical troubleshooting |
| `net.operations.documentation` | **RENAME** | `net.operations.monitoring-and-docs` | Absorbs monitoring + HA/DR content from CompTIA Domain 3 |

**No modules are SPLIT or MERGED** (beyond the documentation → monitoring-and-docs broadening). All 8 existing stubs are preserved or renamed — none are deleted.

### Activity Remapping Required

| Activity | Current moduleId | New moduleId |
|---|---|---|
| `terminal-basics` (lab) | `net.troubleshooting.tools` | `net.troubleshooting.tools-and-methods` |
| `network-terminal-basics` (lab) | `net.troubleshooting.tools` | `net.troubleshooting.tools-and-methods` |
| `network-fundamentals-checkpoint` (quiz) | `net.fundamentals.addressing` | `net.fundamentals.addressing` *(no change)* |

### Legacy Module Note

`network-legacy` (in `src/content/modules/network/`) has `moduleId: network-legacy` which does **not** follow the `net.*.*` pattern. This module is excluded from the active track module list and should remain as-is for archival purposes per CONSTITUTION §6.

---

## 3. Scope Conflicts & Gap Analysis

### Gaps: CompTIA objectives without clear CYBER.ORG mapping

| CompTIA Objective | Module Assigned | Gap |
|---|---|---|
| N10-009 1.3 (Transmission media) | `net.fundamentals.cabling-and-connectors` | CYBER.ORG has 1.3.1–1.3.4 ✓ — **no gap** |
| N10-009 1.7 (Corporate/datacenter arch.) | `net.fundamentals.architecture` | CYBER.ORG 1.7.x is "implied" — **no structured quiz/lesson source**. Must author from CompTIA objectives directly. |
| N10-009 1.8 (Cloud concepts) | `net.fundamentals.architecture` | CYBER.ORG 1.8.x is "implied" — **same gap as 1.7**. |
| N10-009 2.1 (Networking appliances) | `net.implementation.devices` | CYBER.ORG 2.1.1–2.1.2 ✓ — **partial gap** (CYBER.ORG covers device types but not all CompTIA sub-objectives like load balancers) |
| N10-009 2.3 (Ethernet switching) | `net.implementation.switching` | CYBER.ORG 2.3.x is "implied" — **no structured content source**. Author from CompTIA. |
| N10-009 2.4 (Wireless standards) | `net.implementation.wireless` | CYBER.ORG 2.4.x is "implied" — **partial gap**. May need supplemental content. |
| N10-009 3.1–3.4 (Operations) | `net.operations.monitoring-and-docs` | CYBER.ORG 3.x are all "implied" — **largest gap**. Entire operations domain needs authoring from CompTIA objectives. |
| N10-009 4.3 (Security features) | `net.security.defense` | CYBER.ORG has labs (4.1.2, 4.2.2, 4.4.1) but no theory lessons for 4.3/4.5. **Lesson content must be authored.** |
| N10-009 5.1 (Methodology) | `net.troubleshooting.tools-and-methods` | CYBER.ORG 5.3.x covers tools but not the step-by-step methodology. **Must author methodology lesson.** |
| N10-009 5.2, 5.4 (Cable/performance) | `net.troubleshooting.tools-and-methods` | **No CYBER.ORG source.** Must author from CompTIA objectives. |

### Conflicts resolved

| Potential Conflict | Resolution |
|---|---|
| CYBER.ORG 1.6 (DHCP/DNS/NTP) vs CompTIA 3.3 (IPv4/IPv6 services) | Both map to `net.fundamentals.network-services`. CompTIA 3.3 covers these services from an operations angle; the lesson will cover both theory (Domain 1) and operational troubleshooting (Domain 3). |
| CYBER.ORG 4.2.2 (Phishing with SEToolkit) — offensive tool | Restructured as a *phishing recognition and defense* exercise per CONSTITUTION §13 (Educational Safety). The lab teaches recognition, not attack execution. |
| `terminal-basics` lab — generic, not network-specific | Kept in troubleshooting module. It teaches foundational CLI skills (`pwd`, `ls`, `cd`) that are prerequisite to network CLI tools. Listed as the first lab before the network-specific `network-terminal-basics`. |

### N10-008 vs N10-009 compatibility

The module map targets N10-009 objectives as the primary structure. N10-008 differences are minor:
- N10-008 objective numbering differs but topics overlap ~90%.
- The map covers all major N10-008 topics. No separate modules needed.
- If a lesson references an objective number, it should note both: "N10-009 1.4 / N10-008 1.4".

---

## 4. Ordered Module List (Track `modules` Array)

This is the canonical order for the track file's `modules` array and module `order` values:

| Order | Module ID | Domain | Title |
|---|---|---|---|
| 1 | `net.fundamentals.models-and-standards` | Concepts | Models & Standards |
| 2 | `net.fundamentals.topologies-and-types` | Concepts | Topologies & Network Types |
| 3 | `net.fundamentals.cabling-and-connectors` | Concepts | Cabling & Connectors |
| 4 | `net.fundamentals.addressing` | Concepts | IP Addressing |
| 5 | `net.fundamentals.ports-and-protocols` | Concepts | Ports & Protocols |
| 6 | `net.fundamentals.network-services` | Concepts | Core Network Services |
| 7 | `net.fundamentals.architecture` | Concepts | Network Architecture & Cloud |
| 8 | `net.implementation.devices` | Implementation | Networking & Networked Devices |
| 9 | `net.implementation.routing` | Implementation | Routing Fundamentals |
| 10 | `net.implementation.switching` | Implementation | Ethernet Switching |
| 11 | `net.implementation.wireless` | Implementation | Wireless Networking |
| 12 | `net.operations.monitoring-and-docs` | Operations | Monitoring, Documentation & DR |
| 13 | `net.security.defense` | Security | Network Security & Defense |
| 14 | `net.troubleshooting.tools-and-methods` | Troubleshooting | Troubleshooting Tools & Methodology |

**Total: 14 modules, 63 planned activities (avg 4.5 per module)**

---

## 5. Activity Count Summary

| Domain | Modules | Total Activities | Avg per Module |
|---|---|---|---|
| Concepts (1.x) | 7 | 32 | 4.6 |
| Implementation (2.x) | 4 | 17 | 4.3 |
| Operations (3.x) | 1 | 5 | 5.0 |
| Security (4.x) | 1 | 6 | 6.0 |
| Troubleshooting (5.x) | 1 | 6 | 6.0 |
| **Total** | **14** | **66** | **4.7** |

> The Concepts domain is intentionally the largest (7 modules) because it carries the most CYBER.ORG structured content and the highest CompTIA exam weight for N10-009 (23%).

---

## 6. Implementation Notes for P1-B (Ingest)

When the curriculum manifest is authored for this track:

1. **Renames require two steps:** Create new module file → update `moduleId` on all activities → delete old module file. The ingest script (P1-B) handles creation; renames of existing stubs are a manual migration step.

2. **Track MDX update needed:** The `modules` array in `network-engineer.mdx` must be updated to the 14-module list from §4.

3. **Sections auto-generation:** Per the manifest schema (P1-A, decision D10), sections are generated from modules. Each module becomes one section with its activities listed in order.

4. **estimatedHours update:** Track `estimatedHours` should increase from 8 to ~20 given the expanded content.

5. **CYBER.ORG quizzes with DOCX sources:** Where CYBER.ORG provides assessment DOCX files (like the tech-plus assessments), those should be ingested through `ingest-assessments-from-manifest.mjs` first, then referenced from the curriculum manifest via `quizJsonPath` on the quiz entries.
