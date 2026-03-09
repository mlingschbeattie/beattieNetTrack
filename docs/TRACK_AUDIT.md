# BeattieNetTrack — Network Engineer Track Audit
**Date:** March 9, 2026

---

## Step 1 — Track File: `src/content/tracks/network-engineer.mdx`

Modules listed in the `modules:` array (19 total, in order):

```
net.fundamentals.models-and-standards
net.fundamentals.topologies-and-types
net.fundamentals.cabling-and-connectors
net.fundamentals.addressing
net.fundamentals.ports-and-protocols
net.fundamentals.network-services
net.fundamentals.architecture
net.fundamentals.routing
net.implementation.devices
net.implementation.routing
net.implementation.switching
net.implementation.wireless
net.implementation.addressing
net.operations.documentation
net.operations.availability
net.security.defense
net.troubleshooting.tools-and-methods
net.security.fundamentals
net.security.wireless
```

---

## Step 2 — Module Files: `src/content/modules/net/`

14 `.mdx` files found. **All are stubs** ("Network Engineer module stub." body).

| File | Slug | Title | Order |
|------|------|-------|-------|
| net.fundamentals.models-and-standards.mdx | net.fundamentals.models-and-standards | Models and Standards | 1 |
| net.fundamentals.topologies-and-types.mdx | net.fundamentals.topologies-and-types | Topologies & Network Types | 2 |
| net.fundamentals.cabling-and-connectors.mdx | net.fundamentals.cabling-and-connectors | Cabling & Connectors | 3 |
| net.fundamentals.addressing.mdx | net.fundamentals.addressing | IP Addressing | 4 |
| net.fundamentals.ports-and-protocols.mdx | net.fundamentals.ports-and-protocols | Ports & Protocols | 5 |
| net.fundamentals.network-services.mdx | net.fundamentals.network-services | Core Network Services | 6 |
| net.fundamentals.architecture.mdx | net.fundamentals.architecture | Network Architecture & Cloud | 7 |
| net.implementation.devices.mdx | net.implementation.devices | Networking & Networked Devices | 8 |
| net.implementation.routing.mdx | net.implementation.routing | Routing Fundamentals | 9 |
| net.implementation.switching.mdx | net.implementation.switching | Ethernet Switching | 10 |
| net.implementation.wireless.mdx | net.implementation.wireless | Wireless Networking | 11 |
| net.operations.monitoring-and-docs.mdx | net.operations.monitoring-and-docs | Monitoring, Documentation & DR | 12 |
| net.security.defense.mdx | net.security.defense | Network Security & Defense | 13 |
| net.troubleshooting.tools-and-methods.mdx | net.troubleshooting.tools-and-methods | Troubleshooting Tools & Methodology | 14 |

### Missing module files
Referenced in the track's `modules:` array but no corresponding `.mdx` file exists:

- `net.fundamentals.routing` — 3 lessons point here; no file
- `net.implementation.addressing` — 3 lessons point here; no file
- `net.operations.documentation` — 2 lessons point here; no file *(existing file slug is `net.operations.monitoring-and-docs`, which is NOT what the track references)*
- `net.operations.availability` — 2 lessons point here; no file
- `net.security.fundamentals` — 3 lessons point here; no file
- `net.security.wireless` — 1 lesson points here; no file

### Orphan module file
File exists but its slug is NOT in the track's `modules:` array:

- `net.operations.monitoring-and-docs` — in file system, never referenced by the track

---

## Step 3 — `npm run validate:tracks`

**PASSED.**

```
Track validation report
======================
Tracks discovered: 9
Modules discovered: 53
Collections checked: labs, quizzes, activities, tour
Entries checked: 94

Validation passed: all activity content is correctly mapped to track + moduleId.
```

> **Note:** The validator does not cross-check whether lesson `moduleId` values appear in the track's `modules:` array. Many mismatches below exist despite the pass.

---

## Step 4 — Resource Directories: `public/resources/network-engineer/`

### Duplicate / legacy directories (old naming, PDFs in wrong location)

| Legacy dir (has PDFs) | Canonical dir (empty) | Issue |
|---|---|---|
| `1.1.2-encapsulation/` | `1-1-2-encapsulation-decapsulation/` | Old dot-format dir has PDFs |
| `1-4-1-public-vs-private-networks/` | `1-4-1-public-private-networks/` | Slug mismatch |
| `1-4-2-ipv4-and-ipv6/` | `1-4-2-ipv4-ipv6/` | Slug mismatch |
| `1-5-1-common-ports-and-protocols/` | `1-5-1-common-ports/` | Slug mismatch |
| `1-7-1-corporate-and-datacenter-network-architecture/` | `1-7-1-corporate-datacenter-architecture/` | Slug mismatch |
| `1-7-2-cloud-concepts-and-connectivity/` | `1-7-2-cloud-concepts/` | Slug mismatch |
| `2-2-2-wireless-security-and-configuration/` | `2-2-2-wireless-security/` | Slug mismatch |
| `3-1-2-network-monitoring-management/` | `3-1-2-network-monitoring/` | Both have PDFs — duplicate |
| `3-2-1-high-availability-redundancy/` | `3-2-1-high-availability/` | Both have PDFs — duplicate |
| `3-3-1-network-change-management/` | `3-3-1-change-management/` | Both have PDFs — duplicate |

### Empty / stale directories with no PDFs
`2-3-1-ip-subnetting`, `3-3-2-network-policies-procedures`, `3-3-2-policies-procedures`,
`4-1-1-security-concepts`, `4-1-2-common-attacks`, `4-1-3-social-engineering`,
`4-2-1-firewalls-ids-ips`, `4-2-1-network-hardening`, `4-2-2-vpn-remote-access`,
`4-2-2-wireless-security-threats`, `4-3-1-firewalls-and-ids`, `4-3-1-wireless-security-threats`,
`4-3-2-vpn-and-remote-access-security`, `5-2-1-troubleshooting-cables-and-physical`,
`5-2-1-troubleshooting-physical-layer`, `5-2-2-troubleshooting-connectivity`,
`5-3-1-troubleshooting-wireless`, `5-3-2-troubleshooting-security`, `new-pdfs/`, `output_v2/`

---

## Step 5 — Cross-Reference: Track Modules vs Lesson `moduleId` Values

### moduleIds used by lessons that are NOT in the track's `modules:` array

| moduleId | Lessons using it | Module file exists? |
|----------|-----------------|---------------------|
| `net.operations.procedures` | net-change-management, net-policies-procedures | No |
| `net.operations.documentation` | net-network-documentation, net-network-monitoring | No *(close file: `monitoring-and-docs`)* |
| `net.operations.availability` | net-high-availability, net-load-balancing | No |
| `net.implementation.addressing` | net-ip-addressing-subnetting, net-nat-pat, net-ipv6-implementation | No |
| `net.implementation.services` | net-network-services-configuration | No |
| `net.security.fundamentals` | net-network-security-concepts, net-common-network-attacks, net-network-hardening | No |
| `net.security.infrastructure` | net-firewalls-ids-ips, net-vpn-remote-access | No |
| `net.security.physical` | net-physical-security, net-data-loss-prevention | No |
| `net.security.wireless` | net-wireless-security-threats | No |
| `net.troubleshooting.methodology` | net-troubleshooting-methodology, net-troubleshooting-tools | No |
| `net.troubleshooting.physical` | net-troubleshooting-physical-layer, net-troubleshooting-connectivity | No |
| `net.troubleshooting.wireless` | net-troubleshooting-wireless | No |
| `net.troubleshooting.security` | net-troubleshooting-security | No |

**Total: 13 moduleId values used by lessons that don't appear in the track's `modules:` array.**

### Track modules with zero lessons pointing to them

| Track module | Module file? | Notes |
|---|---|---|
| `net.implementation.devices` | Yes | 0 lessons |
| `net.security.defense` | Yes | 0 lessons — lessons use `net.security.fundamentals` instead |
| `net.troubleshooting.tools-and-methods` | Yes | 0 lessons — lessons use `net.troubleshooting.methodology` etc. |
| `net.fundamentals.routing` | **No** | 3 lessons exist but module file missing |

---

## Step 6 — Full Lesson Table

> **PDF columns:** reflect the **canonical** directory per `make_resource_dirs.py`.
> Where PDFs exist only in a legacy/misnamed dir, the column shows ❌ with the actual location noted.
> ⚠️ = moduleId does not appear in the track's `modules:` array.

| Unit | Lesson slug | moduleId | Guided Notes | Answer Key |
|------|------------|----------|:---:|:---:|
| 1.1.1 | net-osi-model | net.fundamentals.models-and-standards | ❌ | ❌ |
| 1.1.2 | net-encapsulation-decapsulation | net.fundamentals.models-and-standards | ❌ *(in `1.1.2-encapsulation/`)* | ❌ |
| 1.2.1 | net-network-topologies | net.fundamentals.topologies-and-types | ✅ | ✅ |
| 1.2.2 | net-network-types | net.fundamentals.topologies-and-types | ✅ | ✅ |
| 1.3.1 | net-copper-cables | net.fundamentals.cabling-and-connectors | ✅ | ✅ |
| 1.3.2 | net-fiber-optic-cables | net.fundamentals.cabling-and-connectors | ✅ | ✅ |
| 1.3.3 | net-connector-types | net.fundamentals.cabling-and-connectors | ✅ | ✅ |
| 1.3.4 | net-cable-management | net.fundamentals.cabling-and-connectors | ✅ | ✅ |
| 1.4.1 | net-public-private-networks | net.fundamentals.addressing | ❌ *(in `1-4-1-public-vs-private-networks/`)* | ❌ |
| 1.4.2 | net-ipv4-ipv6 | net.fundamentals.addressing | ❌ *(in `1-4-2-ipv4-and-ipv6/`)* | ❌ |
| 1.5.1 | net-common-ports | net.fundamentals.ports-and-protocols | ❌ *(in `1-5-1-common-ports-and-protocols/`)* | ❌ |
| 1.5.2 | net-protocols | net.fundamentals.ports-and-protocols | ✅ | ✅ |
| 1.6.1 | net-dhcp | net.fundamentals.network-services | ✅ | ✅ |
| 1.6.2 | net-dns | net.fundamentals.network-services | ✅ | ✅ |
| 1.6.3 | net-ntp | net.fundamentals.network-services | ✅ | ✅ |
| 1.7.1 | net-corporate-datacenter-architecture | net.fundamentals.architecture | ❌ *(in `1-7-1-corporate-and-datacenter-network-architecture/`)* | ❌ |
| 1.7.2 | net-cloud-concepts | net.fundamentals.architecture | ❌ *(in `1-7-2-cloud-concepts-and-connectivity/`)* | ❌ |
| 1.8.1 | net-routing-concepts | net.fundamentals.routing ⚠️ | ✅ | ✅ |
| 1.8.2 | net-routing-protocols | net.fundamentals.routing ⚠️ | ✅ | ✅ |
| 1.8.3 | net-wan-technologies | net.fundamentals.routing ⚠️ | ✅ | ✅ |
| 2.1.1 | net-switching-concepts | net.implementation.switching | ✅ | ✅ |
| 2.1.2 | net-vlans | net.implementation.switching | ✅ | ✅ |
| 2.1.3 | net-switch-configuration | net.implementation.switching | ✅ | ✅ |
| 2.2.1 | net-wireless-standards | net.implementation.wireless | ✅ | ✅ |
| 2.2.2 | net-wireless-security | net.implementation.wireless | ❌ *(in `2-2-2-wireless-security-and-configuration/`)* | ❌ |
| 2.3.1 | net-ip-addressing-subnetting | net.implementation.addressing ⚠️ | ❌ | ❌ |
| 2.3.2 | net-nat-pat | net.implementation.addressing ⚠️ | ❌ | ❌ |
| 2.3.3 | net-ipv6-implementation | net.implementation.addressing ⚠️ | ❌ | ❌ |
| 2.4.1 | net-routing-protocol-configuration | net.implementation.routing | ❌ | ❌ |
| 2.4.2 | net-router-configuration-cli | net.implementation.routing | ❌ | ❌ |
| 2.5.1 | net-network-services-configuration | net.implementation.services ⚠️ | ❌ | ❌ |
| 3.1.1 | net-network-documentation | net.operations.documentation ⚠️ | ✅ | ✅ |
| 3.1.2 | net-network-monitoring | net.operations.documentation ⚠️ | ✅ | ✅ |
| 3.2.1 | net-high-availability | net.operations.availability ⚠️ | ✅ | ✅ |
| 3.2.2 | net-load-balancing | net.operations.availability ⚠️ | ✅ | ✅ |
| 3.3.1 | net-change-management | net.operations.procedures ⚠️ | ✅ | ✅ |
| 3.3.2 | net-policies-procedures | net.operations.procedures ⚠️ | ✅ | ✅ |
| 4.1.1 | net-network-security-concepts | net.security.fundamentals ⚠️ | ✅ | ✅ |
| 4.1.2 | net-common-network-attacks | net.security.fundamentals ⚠️ | ✅ | ✅ |
| 4.1.3 | net-network-hardening | net.security.fundamentals ⚠️ | ✅ | ✅ |
| 4.2.1 | net-firewalls-ids-ips | net.security.infrastructure ⚠️ | ✅ | ✅ |
| 4.2.2 | net-vpn-remote-access | net.security.infrastructure ⚠️ | ✅ | ✅ |
| 4.3.1 | net-wireless-security-threats | net.security.wireless ⚠️ | ✅ | ✅ |
| 4.4.1 | net-physical-security | net.security.physical ⚠️ | ✅ | ✅ |
| 4.4.2 | net-data-loss-prevention | net.security.physical ⚠️ | ✅ | ✅ |
| 5.1.1 | net-troubleshooting-methodology | net.troubleshooting.methodology ⚠️ | ✅ | ✅ |
| 5.1.2 | net-troubleshooting-tools | net.troubleshooting.methodology ⚠️ | ✅ | ✅ |
| 5.2.1 | net-troubleshooting-physical-layer | net.troubleshooting.physical ⚠️ | ✅ | ✅ |
| 5.2.2 | net-troubleshooting-connectivity | net.troubleshooting.physical ⚠️ | ✅ | ✅ |
| 5.3.1 | net-troubleshooting-wireless | net.troubleshooting.wireless ⚠️ | ✅ | ✅ |
| 5.3.2 | net-troubleshooting-security | net.troubleshooting.security ⚠️ | ✅ | ✅ |

---

## Summary of Issues

| Category | Count | Details |
|----------|------:|-------|
| Lessons with moduleId not in track | 37 / 51 | See Step 5 |
| Track modules with no lessons pointing to them | 3 | `net.implementation.devices`, `net.security.defense`, `net.troubleshooting.tools-and-methods` |
| Module files missing (track references them, no file) | 6 | `net.fundamentals.routing`, `net.implementation.addressing`, `net.operations.documentation`, `net.operations.availability`, `net.security.fundamentals`, `net.security.wireless` |
| Orphan module file (exists, not in track) | 1 | `net.operations.monitoring-and-docs` |
| PDFs in wrong / legacy directory | 7 | 1.1.2, 1.4.1, 1.4.2, 1.5.1, 1.7.1, 1.7.2, 2.2.2 |
| Lessons with no PDFs anywhere | 7 | 1.1.1, 2.3.1–2.3.3, 2.4.1–2.4.2, 2.5.1 |
| Duplicate resource dirs (same content, two names) | 3 pairs | 3.1.2, 3.2.1, 3.3.1 |
| Empty stale resource dirs | 20+ | See Step 4 |
| `4.4.2` missing from `make_resource_dirs.py` | 1 | Dir exists (manually created), not in script |
