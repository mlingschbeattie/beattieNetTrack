#!/usr/bin/env python3
"""
make_resource_dirs.py

Creates the full directory structure under
  public/resources/<track>/
for every known unit across all tracks.

Run from the repo root:
    python3 scripts/make_resource_dirs.py

Idempotent — safe to re-run. Creates directories only, no files.
Prints a summary of what was created vs already existed.
"""

import os
from pathlib import Path

# ── DIRECTORY NAMING CONVENTION ───────────────────────────────────────────────
# Unit 1.3.2, slug "fiber-optic-cables"
# → public/resources/network-engineer/1-3-2-fiber-optic-cables/

def dir_name(unit, slug):
    return f"{unit.replace('.', '-')}-{slug}"


# ── TRACK DEFINITIONS ─────────────────────────────────────────────────────────

TRACKS = {

    # ── NETWORK ENGINEER ──────────────────────────────────────────────────────
    "network-engineer": [
        # Domain 1 — Networking Concepts
        ("1.1.1", "osi-model"),
        ("1.1.2", "encapsulation-decapsulation"),
        ("1.2.1", "network-topologies"),
        ("1.2.2", "network-types"),
        ("1.3.1", "copper-cables"),
        ("1.3.2", "fiber-optic-cables"),
        ("1.3.3", "connector-types"),
        ("1.3.4", "cable-management"),
        ("1.4.1", "public-private-networks"),
        ("1.4.2", "ipv4-ipv6"),
        ("1.5.1", "common-ports"),
        ("1.5.2", "protocols"),
        ("1.6.1", "dhcp"),
        ("1.6.2", "dns"),
        ("1.6.3", "ntp"),
        ("1.7.1", "corporate-datacenter-architecture"),
        ("1.7.2", "cloud-concepts"),
        ("1.8.1", "routing-concepts"),
        ("1.8.2", "routing-protocols"),
        ("1.8.3", "wan-technologies"),
        # Domain 2 — Network Implementation
        ("2.1.1", "switching-concepts"),
        ("2.1.2", "vlans"),
        ("2.1.3", "switch-configuration"),
        ("2.2.1", "wireless-standards"),
        ("2.2.2", "wireless-security"),
        ("2.3.1", "ip-addressing-subnetting"),
        ("2.3.2", "nat-pat"),
        ("2.3.3", "ipv6-implementation"),
        ("2.4.1", "routing-protocol-configuration"),
        ("2.4.2", "router-configuration-cli"),
        ("2.5.1", "network-services-configuration"),
        # Domain 3 — Network Operations
        ("3.1.1", "network-documentation"),
        ("3.1.2", "network-monitoring-management"),
        ("3.2.1", "high-availability-redundancy"),
        ("3.2.2", "load-balancing"),
        ("3.3.1", "network-change-management"),
        ("3.3.2", "network-policies-procedures"),
        # Domain 4 — Network Security (pending authoring)
        ("4.1.1", "security-concepts"),
        ("4.1.2", "common-attacks"),
        ("4.1.3", "social-engineering"),
        ("4.2.1", "network-hardening"),
        ("4.2.2", "wireless-security-threats"),
        ("4.3.1", "firewalls-and-ids"),
        ("4.3.2", "vpn-and-remote-access-security"),
        ("4.4.1", "physical-security"),
        ("4.4.2", "data-loss-prevention"),
        # Domain 5 — Network Troubleshooting (pending authoring)
        ("5.1.1", "troubleshooting-methodology"),
        ("5.1.2", "troubleshooting-tools"),
        ("5.2.1", "troubleshooting-cables-and-physical"),
        ("5.2.2", "troubleshooting-network-connectivity"),
        ("5.2.3", "troubleshooting-performance"),
        ("5.3.1", "troubleshooting-wireless"),
        ("5.3.2", "troubleshooting-security"),
    ],

    # ── PC TECHNICIAN ─────────────────────────────────────────────────────────
    # CompTIA Tech+ / A+ Core 1 (220-1101) / A+ Core 2 (220-1102)
    "pc-technician": [
        # Hardware Components
        ("1.1.1", "hardware-components-overview"),
        ("1.1.2", "cpu-architecture"),
        ("1.1.3", "ram-memory"),
        ("1.1.4", "storage-devices"),
        ("1.1.5", "motherboards"),
        ("1.1.6", "power-supplies"),
        ("1.1.7", "display-technologies"),
        # Hardware Peripherals
        ("1.2.1", "input-devices"),
        ("1.2.2", "output-devices"),
        ("1.2.3", "connectors-and-ports"),
        # Networking Fundamentals
        ("1.3.1", "networking-basics"),
        ("1.3.2", "wireless-networking"),
        ("1.3.3", "network-troubleshooting-basics"),
        # Operating Systems — Windows
        ("2.1.1", "windows-os-overview"),
        ("2.1.2", "windows-installation"),
        ("2.1.3", "windows-configuration"),
        ("2.1.4", "windows-command-line"),
        ("2.1.5", "windows-troubleshooting"),
        # Operating Systems — Other
        ("2.2.1", "macos-overview"),
        ("2.2.2", "linux-overview"),
        ("2.2.3", "mobile-os"),
        # Security Basics
        ("3.1.1", "security-fundamentals"),
        ("3.1.2", "malware-types"),
        ("3.1.3", "security-best-practices"),
        ("3.1.4", "data-destruction-and-disposal"),
        # Troubleshooting
        ("4.1.1", "troubleshooting-methodology"),
        ("4.1.2", "troubleshooting-hardware"),
        ("4.1.3", "troubleshooting-os"),
        ("4.1.4", "troubleshooting-networks"),
        ("4.1.5", "troubleshooting-security"),
        # Professionalism
        ("5.1.1", "professionalism-and-communication"),
        ("5.1.2", "safety-and-environmental"),
    ],

    # ── CYBERSECURITY ─────────────────────────────────────────────────────────
    # CompTIA Security+ (SY0-701) / CySA+
    "cybersecurity": [
        # Fundamentals
        ("1.1.1", "security-concepts-and-cia"),
        ("1.1.2", "threat-vulnerability-risk"),
        ("1.1.3", "security-controls"),
        ("1.1.4", "cryptography-basics"),
        ("1.1.5", "pki-and-certificates"),
        # Threats and Attacks
        ("1.2.1", "malware-and-ransomware"),
        ("1.2.2", "social-engineering"),
        ("1.2.3", "network-attacks"),
        ("1.2.4", "application-attacks"),
        ("1.2.5", "threat-intelligence"),
        # Architecture and Design
        ("2.1.1", "security-architecture"),
        ("2.1.2", "network-security-design"),
        ("2.1.3", "cloud-security"),
        ("2.1.4", "virtualization-security"),
        ("2.2.1", "identity-and-access-management"),
        ("2.2.2", "authentication-protocols"),
        ("2.2.3", "authorization-and-accounting"),
        # Security Operations
        ("3.1.1", "security-monitoring"),
        ("3.1.2", "siem-and-log-analysis"),
        ("3.1.3", "incident-response"),
        ("3.1.4", "digital-forensics"),
        ("3.2.1", "vulnerability-scanning"),
        ("3.2.2", "penetration-testing-concepts"),
        # Compliance and Governance
        ("4.1.1", "compliance-frameworks"),
        ("4.1.2", "data-privacy-regulations"),
        ("4.1.3", "risk-management"),
        ("4.2.1", "security-policies"),
        ("4.2.2", "business-continuity"),
        # Ethical Hacking
        ("5.1.1", "ethical-hacking-overview"),
        ("5.1.2", "reconnaissance"),
        ("5.1.3", "scanning-and-enumeration"),
        ("5.1.4", "exploitation-basics"),
        ("5.1.5", "post-exploitation"),
        ("5.1.6", "reporting"),
    ],

}


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    # Default to running from repo root; output to public/resources/
    repo_root = Path(__file__).parent.parent
    output_root = repo_root / "public" / "resources"

    created = 0
    existed = 0

    for track, units in TRACKS.items():
        track_root = output_root / track
        for unit, slug in units:
            d = track_root / dir_name(unit, slug)
            if d.exists():
                existed += 1
            else:
                d.mkdir(parents=True, exist_ok=True)
                created += 1

    total = created + existed
    print(f"\nDone.")
    print(f"  Tracks:     {len(TRACKS)}")
    print(f"  Total dirs: {total}")
    print(f"  Created:    {created}")
    print(f"  Already existed: {existed}")
    print(f"\nOutput root: {output_root.resolve()}")


if __name__ == "__main__":
    main()