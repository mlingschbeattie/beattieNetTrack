#!/usr/bin/env python3
"""
make_resource_pdfs.py

Generate guided notes and answer key PDFs for BeattieNetTrack.
One script, any unit. Reads from a JSON data file or inline dict.

Usage:
    python3 make_resource_pdfs.py --unit 1.1.1
    python3 make_resource_pdfs.py --unit 1.1.2 --data path/to/questions.json
    python3 make_resource_pdfs.py --all --data-dir scripts/resource-data/

Output goes to: public/resources/network-engineer/<unit-slug>/
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
except ImportError:
    print("ERROR: reportlab not installed. Run: pip install reportlab --break-system-packages")
    sys.exit(1)


# ── STYLE FACTORY ─────────────────────────────────────────────────────────────

def make_styles():
    base = getSampleStyleSheet()
    return {
        'title': ParagraphStyle('DocTitle', parent=base['Title'],
            fontSize=16, textColor=colors.HexColor('#0f1829'), spaceAfter=4),
        'subtitle': ParagraphStyle('Subtitle', parent=base['Normal'],
            fontSize=10, textColor=colors.HexColor('#38bdf8'), spaceAfter=2),
        'meta': ParagraphStyle('Meta', parent=base['Normal'],
            fontSize=9, textColor=colors.HexColor('#7a90b8'), spaceAfter=12),
        'instruction': ParagraphStyle('Instruction', parent=base['Italic'],
            fontSize=9, textColor=colors.HexColor('#4a6180'), spaceAfter=16),
        'question_num': ParagraphStyle('QuestionNum', parent=base['Normal'],
            fontSize=10, textColor=colors.HexColor('#38bdf8'),
            fontName='Helvetica-Bold', spaceBefore=14, spaceAfter=2),
        'question': ParagraphStyle('Question', parent=base['Normal'],
            fontSize=10, textColor=colors.HexColor('#0f1829'),
            leading=15, spaceAfter=4),
        'answer': ParagraphStyle('Answer', parent=base['Normal'],
            fontSize=10, textColor=colors.HexColor('#166534'),
            leading=15, spaceAfter=4, fontName='Helvetica-Oblique'),
        'real_world_label': ParagraphStyle('RWLabel', parent=base['Normal'],
            fontSize=10, textColor=colors.HexColor('#f97316'),
            fontName='Helvetica-Bold', spaceBefore=14, spaceAfter=2),
        'wget': ParagraphStyle('Wget', parent=base['Code'],
            fontSize=9, textColor=colors.HexColor('#22c55e'),
            backColor=colors.HexColor('#0f1829'),
            borderPadding=(6, 8, 6, 8), spaceAfter=8, spaceBefore=8),
    }


# ── SLUG HELPER ───────────────────────────────────────────────────────────────

def unit_to_slug(unit_number, title):
    """'1.1.1', 'OSI Model' -> '1.1.1-osi-model'"""
    t = title.lower()
    t = re.sub(r'[^a-z0-9\s-]', '', t)
    t = re.sub(r'\s+', '-', t.strip())
    return f"{unit_number.replace('.', '-')}-{t}"


# ── PDF BUILDERS ──────────────────────────────────────────────────────────────

def build_guided_notes(outpath, unit_data):
    S = make_styles()
    unit = unit_data['unit']
    title = unit_data['title']
    questions = unit_data['questions']
    server_path = unit_data.get(
        'server_path',
        f"http://[SERVER]/resources/network-engineer/{unit_to_slug(unit, title)}/{unit_to_slug(unit, title)}-answer-key.pdf"
    )

    doc = SimpleDocTemplate(outpath, pagesize=letter,
        leftMargin=inch, rightMargin=inch,
        topMargin=0.85*inch, bottomMargin=0.85*inch)
    story = []

    story.append(Paragraph(f"{title} -- Guided Notes", S['title']))
    story.append(Paragraph(
        f"Unit {unit}  |  CompTIA Network+ N10-009 Obj. {unit_data.get('n10_009', '')}  |  N10-008 {unit_data.get('n10_008', '')}",
        S['subtitle']))
    story.append(Paragraph(
        'Name: ___________________________________  Date: ____________  Period: ______',
        S['meta']))
    story.append(HRFlowable(width='100%', thickness=1,
        color=colors.HexColor('#162035'), spaceAfter=10))
    story.append(Paragraph(
        'Complete each question using the lesson reading. '
        'Write in the blank or answer in the space provided.',
        S['instruction']))

    for q in questions:
        is_rw = q.get('real_world', False)
        num = q['num']
        if is_rw:
            story.append(Paragraph(f"Question {num} -- Real World Application", S['real_world_label']))
        else:
            story.append(Paragraph(f"Question {num}", S['question_num']))

        q_text = q['question'].replace('\n', '<br/>')
        story.append(Paragraph(q_text, S['question']))

        lines = q.get('lines', 3)
        for _ in range(lines):
            story.append(HRFlowable(width='100%', thickness=0.5,
                color=colors.HexColor('#d1d5db'), spaceBefore=10, spaceAfter=2))

    story.append(Spacer(1, 20))
    story.append(HRFlowable(width='100%', thickness=1,
        color=colors.HexColor('#162035'), spaceAfter=10))
    story.append(Paragraph('Download the answer key from the class server:', S['instruction']))
    story.append(Paragraph(f'wget {server_path}', S['wget']))

    doc.build(story)
    print(f'  OK Guided notes: {outpath}')


def build_answer_key(outpath, unit_data):
    S = make_styles()
    unit = unit_data['unit']
    title = unit_data['title']
    questions = unit_data['questions']

    doc = SimpleDocTemplate(outpath, pagesize=letter,
        leftMargin=inch, rightMargin=inch,
        topMargin=0.85*inch, bottomMargin=0.85*inch)
    story = []

    story.append(Paragraph(f"{title} -- Guided Notes ANSWER KEY", S['title']))
    story.append(Paragraph(
        f"Unit {unit}  |  CompTIA Network+ N10-009 Obj. {unit_data.get('n10_009', '')}  |  N10-008 {unit_data.get('n10_008', '')}",
        S['subtitle']))
    story.append(Paragraph(
        'For instructor use / distribute after students complete the notes.',
        S['meta']))
    story.append(HRFlowable(width='100%', thickness=1,
        color=colors.HexColor('#162035'), spaceAfter=10))

    for q in questions:
        is_rw = q.get('real_world', False)
        num = q['num']
        if is_rw:
            story.append(Paragraph(f"Question {num} -- Real World Application", S['real_world_label']))
        else:
            story.append(Paragraph(f"Question {num}", S['question_num']))

        q_text = q['question'].replace('\n', '<br/>')
        story.append(Paragraph(q_text, S['question']))
        story.append(Paragraph(f"Answer: {q['answer']}", S['answer']))

    doc.build(story)
    print(f'  OK Answer key:   {outpath}')


# ── PROCESS ONE UNIT ──────────────────────────────────────────────────────────

def process_unit(unit_data, output_root='public/resources/network-engineer'):
    unit = unit_data['unit']
    title = unit_data['title']
    slug = unit_to_slug(unit, title)
    out_dir = Path(output_root) / slug
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f'\nUnit {unit} -- {title}')
    build_guided_notes(str(out_dir / f'{slug}-guided-notes.pdf'), unit_data)
    build_answer_key(str(out_dir / f'{slug}-answer-key.pdf'), unit_data)


# ── BUILT-IN UNIT DATA ────────────────────────────────────────────────────────
# Add new units here as lessons are approved.
# Each unit can also live in scripts/resource-data/<unit>.json

UNITS = {
    "1.1.1": {
        "unit": "1.1.1",
        "title": "OSI Model",
        "n10_009": "1.1",
        "n10_008": "1.1",
        "questions": [
            {
                "num": "1",
                "question": "The OSI model divides network communication into _______ layers, from the _______ layer at the bottom to the _______ layer at the top.",
                "answer": "Seven (7) layers -- Physical at the bottom, Application at the top.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Layer 1 devices -- such as hubs, repeaters, and _______ -- deal only with raw _______ and have no understanding of addresses or protocols.",
                "answer": "Network interface cards (NICs); raw bits (electrical signals, light pulses, or radio waves).",
                "lines": 3
            },
            {
                "num": "3",
                "question": "A switch operates at Layer _______ and uses _______ addresses to forward frames to the correct port, rather than flooding traffic to every device like a hub.",
                "answer": "Layer 2 (Data Link); MAC addresses.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Explain the difference between a MAC address and an IP address. Which OSI layer is each one associated with?",
                "answer": "A MAC address is a hardware address used at Layer 2 (Data Link) to deliver frames on a local network. An IP address is a logical address used at Layer 3 (Network) to route packets across different networks. MAC = local delivery; IP = internet routing.",
                "lines": 5
            },
            {
                "num": "5",
                "question": "At Layer 4, the two main transport protocols are _______ and _______. The first provides reliable, ordered delivery; the second prioritizes _______ over reliability.",
                "answer": "TCP (Transmission Control Protocol) and UDP (User Datagram Protocol); speed.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Port numbers exist at Layer _______. They allow a single device with one IP address to run multiple _______ simultaneously (for example, a web server and an SSH daemon on the same machine).",
                "answer": "Layer 4 (Transport); services (or applications).",
                "lines": 3
            },
            {
                "num": "7",
                "question": "When a browser negotiates a TLS connection to load an HTTPS website, which OSI layer handles that encryption setup? _______",
                "answer": "Layer 6 (Presentation).",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A user reports that they can ping 8.8.8.8 successfully but cannot load any websites in their browser. Based on the OSI model, which layer(s) would you investigate first, and what specific service is most likely the cause? Explain your reasoning in two to three sentences.",
                "answer": "Layers 1-3 are working (ping to external IP succeeds). The problem is at Layer 7 (Application) -- specifically DNS. The computer can reach the internet by IP but cannot resolve domain names. Check DNS configuration with nslookup; correct or replace the DNS server address.",
                "real_world": True,
                "lines": 6
            }
        ]
    },
    "1.1.2": {
        "unit": "1.1.2",
        "title": "Encapsulation and Decapsulation",
        "n10_009": "1.1",
        "n10_008": "1.1",
        "questions": [
            {
                "num": "1",
                "question": "When data travels down the OSI model on its way out of a device, each layer adds its own _______. This process is called _______. At the destination, each layer _______ its own header in reverse -- a process called _______.",
                "answer": "Header (and sometimes trailer); encapsulation; strips; decapsulation.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Match each header type to the OSI layer that adds it:\n    Port numbers and TCP/UDP info  ->  Layer _______\n    Source and destination IP addresses  ->  Layer _______\n    MAC addresses and CRC trailer  ->  Layer _______",
                "answer": "Port numbers/TCP/UDP -> Layer 4 (Transport); IP addresses -> Layer 3 (Network); MAC addresses/CRC -> Layer 2 (Data Link).",
                "lines": 4
            },
            {
                "num": "3",
                "question": "TCP establishes a connection using a _______ handshake. The three steps are: _______ (sender initiates), _______ (receiver acknowledges), and _______ (sender confirms).",
                "answer": "Three-way handshake; SYN; SYN-ACK; ACK.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Explain the key difference between TCP and UDP. Give one real-world application that uses each protocol and explain why.",
                "answer": "TCP is reliable and connection-oriented -- it guarantees delivery and retransmits lost data (e.g., web browsing, file downloads). UDP is connectionless and fast -- no retransmission, used where speed matters more than perfection (e.g., Discord voice calls, live game state updates, DNS lookups).",
                "lines": 5
            },
            {
                "num": "5",
                "question": "List the purpose of three TCP flags:\n    SYN: _______\n    FIN: _______\n    RST: _______",
                "answer": "SYN: initiates a connection; FIN: gracefully closes a connection; RST: immediately terminates a connection with no negotiation.",
                "lines": 4
            },
            {
                "num": "6",
                "question": "At Layer 2, the Data Link layer wraps a packet into a _______. It adds a _______ with MAC addresses and a _______ containing a CRC value called the _______. If the CRC check fails at the receiving end, the frame is _______.",
                "answer": "Frame; header; trailer; Frame Check Sequence (FCS); dropped silently.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "The MTU on standard Ethernet is _______ bytes. If data exceeds this limit, it gets _______. Why can VPN tunnels cause MTU-related connectivity problems?",
                "answer": "1500 bytes; fragmented. VPN tunnels add their own encapsulation headers on top of existing ones, reducing available payload space. If the resulting packet exceeds the path MTU and the Don't Fragment bit is set, the packet is dropped.",
                "lines": 4
            },
            {
                "num": "8",
                "question": "REAL WORLD: You open Wireshark and capture traffic while loading a webpage. Describe the normal TCP three-way handshake as it appears in the capture. What would it mean if you saw hundreds of SYN packets but no SYN-ACK responses?",
                "answer": "Normal handshake: (1) SYN from client; (2) SYN-ACK from server; (3) ACK from client -- connection established. Hundreds of SYNs with no SYN-ACK = SYN flood attack. Attacker overwhelms the server with half-open connections, exhausting its connection table.",
                "real_world": True,
                "lines": 6
            }
        ]
    },
    "2.3.1": {
        "unit": "2.3.1",
        "title": "IP Addressing and Subnetting",
        "n10_009": "2.3",
        "n10_008": "2.3",
        "questions": [
            {
                "num": "1",
                "question": "An IPv4 address is a _______ -bit number divided into four _______ -bit sections called octets. Each octet is written in _______ notation, with values ranging from 0 to _______.",
                "answer": "32-bit; 8-bit; dotted-decimal; 255.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Convert the decimal number 172 to binary using the bit-position table (128, 64, 32, 16, 8, 4, 2, 1). Show your work step by step.",
                "answer": "128 fits (172 - 128 = 44). 64 doesn't fit. 32 fits (44 - 32 = 12). 16 doesn't fit. 8 fits (12 - 8 = 4). 4 fits (4 - 4 = 0). 2 and 1 don't fit. Result: 10101100.",
                "lines": 5
            },
            {
                "num": "3",
                "question": "A subnet mask of 255.255.255.0 written in CIDR notation is _______. The mask tells a device which portion of an IP address is the _______ address and which portion identifies the _______.",
                "answer": "/24; network; host.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "For the network 192.168.10.0/24, identify: the network address _______, the broadcast address _______, the number of usable host addresses _______, and the valid host range _______.",
                "answer": "Network: 192.168.10.0; Broadcast: 192.168.10.255; Usable hosts: 254; Valid range: 192.168.10.1 to 192.168.10.254.",
                "lines": 4
            },
            {
                "num": "5",
                "question": "A /26 subnet mask borrows _______ bits from the host portion of a /24. Each /26 subnet provides _______ usable host addresses. How many /26 subnets can be created from a single /24 network?",
                "answer": "2 bits; 62 usable hosts; 4 subnets (because 2^2 = 4).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "VLSM stands for _______. Unlike fixed-length subnetting, VLSM allows a network engineer to assign _______ -sized subnets to different segments, which prevents _______ of IP address space.",
                "answer": "Variable Length Subnet Masking; different (variable); waste.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Explain the difference between a network address and a broadcast address. Why can neither be assigned to a host? What happens if a packet is sent to the broadcast address?",
                "answer": "The network address (all host bits = 0) identifies the subnet itself; the broadcast address (all host bits = 1) represents all hosts on that subnet. Neither can be assigned to a host because they serve as reserved identifiers. A packet sent to the broadcast address is delivered to every device on that subnet.",
                "lines": 5
            },
            {
                "num": "8",
                "question": "REAL WORLD: A network admin needs to allocate subnets for four departments: Engineering (50 hosts), Sales (25 hosts), HR (10 hosts), and a WAN link (2 hosts). Using VLSM starting from 10.0.0.0/24, identify the correct subnet size (/prefix) for each department and explain why you chose it.",
                "answer": "Engineering: /26 (62 usable -- smallest mask that fits 50). Sales: /27 (30 usable -- fits 25). HR: /28 (14 usable -- fits 10). WAN link: /30 (2 usable -- exact fit for point-to-point). VLSM assigns the tightest mask that accommodates each group, conserving address space.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "2.3.2": {
        "unit": "2.3.2",
        "title": "NAT and PAT",
        "n10_009": "2.3",
        "n10_008": "2.3",
        "questions": [
            {
                "num": "1",
                "question": "NAT stands for _______. It was developed to extend the life of IPv4 by allowing _______ of devices to share a single _______ IP address, delaying the exhaustion of the public address pool.",
                "answer": "Network Address Translation; many (an entire network); public.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "The three private (non-routable) IPv4 address ranges are _______, _______, and _______. Packets with these source addresses are _______ by internet backbone routers.",
                "answer": "10.0.0.0/8; 172.16.0.0/12; 192.168.0.0/16; dropped (not forwarded).",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Static NAT creates a _______ -to- _______ permanent mapping between a private address and a public address. This is typically used for devices that must be _______ from the internet, such as web servers or mail servers.",
                "answer": "One-to-one; permanent; reachable (accessible).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "PAT (Port Address Translation) is also called NAT _______. It allows thousands of devices to share a _______ public IP address by using unique _______ numbers to track each session in the NAT translation table.",
                "answer": "Overload; single; port.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "In NAT terminology, the _______ interface faces the private network, while the _______ interface faces the public internet. When a packet leaves the private network, NAT replaces the _______ address with the router's public IP.",
                "answer": "Inside (or inside local); outside (or inside global); source (private).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Describe one advantage and one disadvantage of NAT. How does NAT affect end-to-end connectivity, and why is this a problem for certain protocols or applications?",
                "answer": "Advantage: conserves public IPv4 addresses; also provides a degree of security by hiding internal addressing. Disadvantage: breaks end-to-end connectivity -- devices behind NAT cannot be directly addressed from outside, which complicates peer-to-peer applications, VoIP, and some VPN protocols that embed IP addresses in the payload.",
                "lines": 5
            },
            {
                "num": "7",
                "question": "Dynamic NAT maps private addresses to a _______ of public addresses. Unlike PAT, each active session uses a _______ public IP. If the pool is exhausted, new connections are _______ until a public address becomes available.",
                "answer": "Pool; dedicated (unique); dropped (queued/refused).",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A user reports they can access the internet normally, but a colleague trying to connect to the user's PC from outside the office cannot reach it. The office uses PAT on a single public IP. Explain why this happens and describe two solutions that would allow inbound connections.",
                "answer": "PAT only tracks outbound sessions -- unsolicited inbound connections have no NAT table entry, so the router drops them. Solutions: (1) Port forwarding -- configure a static mapping from a specific public port to the internal IP:port of the target PC; (2) Static NAT -- assign the PC a dedicated public IP. A VPN where the colleague initiates the tunnel outbound is a third option.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "2.3.3": {
        "unit": "2.3.3",
        "title": "IPv6 Implementation",
        "n10_009": "2.3",
        "n10_008": "2.3",
        "questions": [
            {
                "num": "1",
                "question": "IPv6 uses _______ -bit addresses, compared to IPv4's 32-bit addresses. Written in hexadecimal, an IPv6 address has _______ groups of four hex digits separated by colons. The total number of possible IPv6 addresses is approximately 3.4 x 10^38 (340 undecillion).",
                "answer": "128-bit; 8 groups; approximately 3.4 x 10^38 (340 undecillion).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Two rules for abbreviating IPv6 addresses: (1) Leading _______ in any group may be omitted. (2) One consecutive run of all-zero groups may be replaced with _______. This compression can only be used _______ per address.",
                "answer": "Zeros (leading zeros); :: (double colon); once.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "IPv6 eliminates the need for NAT because every device can receive a globally unique _______ address. This restores the internet's original design principle of _______ connectivity.",
                "answer": "Global unicast; end-to-end.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Match each IPv6 address type to its description:\n    Global Unicast  ->  _______\n    Link-Local      ->  _______\n    Multicast       ->  _______\n    Loopback        ->  _______",
                "answer": "Global Unicast: publicly routable, starts with 2000::/3. Link-Local: valid only on the local segment, starts with FE80::/10, auto-configured. Multicast: one-to-many delivery, starts with FF00::/8. Loopback: ::1/128, equivalent to 127.0.0.1.",
                "lines": 5
            },
            {
                "num": "5",
                "question": "SLAAC stands for _______. It allows IPv6 hosts to configure their own _______ automatically using the network prefix advertised by a router, combined with the host's _______ or a random value -- without needing a DHCP server.",
                "answer": "Stateless Address Autoconfiguration; global unicast address; EUI-64 (MAC address).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "IPv6 replaces ARP with _______. It uses _______ messages to discover the link-layer address of a neighbor. This is part of the _______ Discovery Protocol (NDP).",
                "answer": "Neighbor Discovery; Neighbor Solicitation and Neighbor Advertisement; Neighbor.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "During the transition from IPv4 to IPv6, what is a dual-stack configuration? What is tunneling in the context of IPv6 transition, and name one common tunneling mechanism.",
                "answer": "Dual-stack: a device runs both IPv4 and IPv6 simultaneously, using whichever is supported by the destination. Tunneling: IPv6 packets are encapsulated inside IPv4 packets to traverse IPv4-only networks. Common mechanisms include 6to4, Teredo, and ISATAP.",
                "lines": 5
            },
            {
                "num": "8",
                "question": "REAL WORLD: A technician pings a server and receives a reply from FE80::1. What does this tell the technician about the current state of connectivity? What would need to be true for the server to be reachable from the public internet over IPv6?",
                "answer": "FE80:: is a link-local address -- the reply confirms Layer 3 IPv6 connectivity on the local segment only. Link-local addresses are not routable beyond the local link. For the server to be reachable from the public internet, it needs a global unicast address (2000::/3 range), and the upstream router must advertise the correct prefix and have IPv6 routing configured.",
                "real_world": True,
                "lines": 6
            }
        ]
    },
    "2.4.1": {
        "unit": "2.4.1",
        "title": "Routing Protocol Configuration",
        "n10_009": "2.4",
        "n10_008": "2.4",
        "questions": [
            {
                "num": "1",
                "question": "A _______ route is manually configured by an administrator and does not update automatically when the network changes. A _______ route is learned automatically through a routing protocol. The _______ route is used when no more specific match exists in the routing table.",
                "answer": "Static route; dynamic route; default route (0.0.0.0/0).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Distance-vector routing protocols share their _______ table with directly connected neighbors at regular intervals. The two classic distance-vector protocols are _______ (used in small networks) and _______ (used in large enterprise networks).",
                "answer": "Routing table; RIP (Routing Information Protocol); EIGRP (Enhanced Interior Gateway Routing Protocol).",
                "lines": 3
            },
            {
                "num": "3",
                "question": "OSPF is a _______ -state routing protocol. Instead of sharing routing tables, routers share _______ advertisements (LSAs) to build a complete map of the network called the _______. Each router then independently calculates the best path using Dijkstra's algorithm.",
                "answer": "Link-state; Link State Advertisements; LSDB (Link State Database).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Administrative distance (AD) is used when a router learns about the same network from _______ sources. The route with the _______ AD value is preferred. List the AD values for: directly connected (___), static route (___), OSPF (___), RIP (___).",
                "answer": "Multiple (different) routing sources; lowest AD; Connected = 0; Static = 1; OSPF = 110; RIP = 120.",
                "lines": 4
            },
            {
                "num": "5",
                "question": "BGP (Border Gateway Protocol) is the routing protocol that runs the _______. It is classified as an _______ gateway protocol because it routes between different autonomous systems. Unlike OSPF or EIGRP, BGP makes routing decisions based primarily on _______.",
                "answer": "Internet (public internet backbone); Exterior (EGP); path attributes and policy (not just metric/cost).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Route redistribution allows a router to take routes learned from one protocol (e.g., OSPF) and advertise them into another (e.g., EIGRP). Why might this be necessary, and what is one risk of misconfigured redistribution?",
                "answer": "Redistribution is needed when two different routing protocols must share route information -- for example, when two companies with different protocols merge networks. A misconfigured redistribution can cause routing loops, where a route learned from one protocol is redistributed back into the original protocol with a different metric.",
                "lines": 5
            },
            {
                "num": "7",
                "question": "In OSPF, routers within the same _______ exchange LSAs directly. Area 0 is called the _______ area and all other areas must connect to it. This hierarchical design reduces the size of the _______ on each router.",
                "answer": "Area; backbone; LSDB (link state database).",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A network engineer notices that traffic between two sites is taking an unexpected path -- traveling through a slower WAN link instead of a faster fiber connection. Both paths are learned via OSPF. What OSPF value would the engineer adjust to prefer the faster link, and how does OSPF calculate this value by default?",
                "answer": "The engineer adjusts the OSPF cost on the interface. By default, OSPF calculates cost as reference bandwidth divided by interface bandwidth (default reference = 100 Mbps). A gigabit interface and a 100 Mbps interface both get cost 1 -- which is why the reference bandwidth is often manually set higher. To prefer the fiber link, lower its cost or raise the cost on the slower WAN interface.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "2.4.2": {
        "unit": "2.4.2",
        "title": "Router Configuration CLI",
        "n10_009": "2.4",
        "n10_008": "2.4",
        "questions": [
            {
                "num": "1",
                "question": "Cisco IOS has three primary privilege levels used in day-to-day work: _______ mode (read-only, prompt ends in >), _______ mode (full access, prompt ends in #), and _______ mode (used to make configuration changes, prompt shows router(config)#).",
                "answer": "User EXEC mode; Privileged EXEC mode; Global Configuration mode.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "To assign an IP address to a router interface, a technician enters interface configuration mode with _______, then types _______ followed by the IP address and subnet mask, then enables the interface with _______.",
                "answer": "interface [type/number] (e.g., interface GigabitEthernet0/0); ip address [address] [mask]; no shutdown.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "The command _______ displays the current routing table in Cisco IOS. The letter codes at the start of each route indicate how it was learned: C = _______, S = _______, O = _______.",
                "answer": "show ip route; C = Connected; S = Static; O = OSPF.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Running configuration is stored in _______. Startup configuration is stored in _______. If a router reboots without saving, changes made since the last save are _______. The command to save is _______.",
                "answer": "RAM (running-config); NVRAM (startup-config); lost; copy running-config startup-config (or write memory).",
                "lines": 4
            },
            {
                "num": "5",
                "question": "To configure a static default route on a Cisco router that sends all unmatched traffic to a next-hop address of 10.0.0.1, a technician would type: _______",
                "answer": "ip route 0.0.0.0 0.0.0.0 10.0.0.1",
                "lines": 3
            },
            {
                "num": "6",
                "question": "The _______ command displays active interfaces, their IP addresses, and their status. An interface showing administratively down means it was disabled with the _______ command. An interface showing down/down indicates a _______ problem.",
                "answer": "show ip interface brief; shutdown; physical (Layer 1) problem.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Describe the purpose of the enable secret command versus the enable password command. Which takes precedence when both are configured, and why is one more secure than the other?",
                "answer": "Both set the password for entering privileged EXEC mode. enable secret takes precedence when both are configured. enable secret is more secure because it stores the password as an MD5 hash; enable password stores it in plaintext, visible in show running-config output.",
                "lines": 5
            },
            {
                "num": "8",
                "question": "REAL WORLD: A technician configures a new router interface with an IP address and types no shutdown, but show ip interface brief still shows the interface as down/down. List three physical-layer causes the technician should investigate and explain what command output would help diagnose each one.",
                "answer": "1) Bad or missing cable -- check show interfaces for input/output errors and line protocol. 2) Speed/duplex mismatch -- check show interfaces for late collisions or excessive errors. 3) Wrong cable type or SFP module mismatch -- physical inspection and show interfaces for transceiver info. Down/down means the physical signal is not present.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "2.5.1": {
        "unit": "2.5.1",
        "title": "Network Services Configuration",
        "n10_009": "2.5",
        "n10_008": "2.5",
        "questions": [
            {
                "num": "1",
                "question": "A DHCP server automatically assigns _______, _______, _______, and _______ to clients on a network. Without DHCP, these values would need to be configured _______ on every device.",
                "answer": "IP address; subnet mask; default gateway; DNS server address; manually (statically).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "The four steps of the DHCP process in order are: _______, _______, _______, _______. The memory aid for this sequence is _______.",
                "answer": "Discover, Offer, Request, Acknowledge (DORA). Memory aid: DORA.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "A DHCP scope defines the _______ of addresses available for assignment. An exclusion range removes specific addresses from the pool (typically used for _______). A DHCP reservation assigns the _______ IP address to a device based on its MAC address.",
                "answer": "Range (pool); servers, printers, and other devices needing static IPs; same (fixed/permanent).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "When a client on one subnet needs to obtain a DHCP address from a server on a different subnet, a _______ agent must be configured on the router interface. This agent forwards DHCP _______ packets across subnet boundaries since these packets cannot normally cross a router.",
                "answer": "DHCP relay agent (ip helper-address); broadcast.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "DNS resolves _______ names (like www.example.com) to _______ addresses. A DNS _______ record maps a hostname to an IPv4 address. A _______ record maps a hostname to an IPv6 address. A _______ record maps an IP address back to a hostname.",
                "answer": "Domain (human-readable); IP; A record; AAAA record; PTR record (reverse lookup).",
                "lines": 4
            },
            {
                "num": "6",
                "question": "NTP (Network Time Protocol) synchronizes _______ across network devices. Accurate time is critical for _______, _______, and _______. NTP uses a hierarchy of servers called _______ levels, with atomic clocks at stratum _______.",
                "answer": "Clocks (system time); log correlation, security certificates/authentication, and Kerberos/AD; stratum; 0.",
                "lines": 4
            },
            {
                "num": "7",
                "question": "Explain the difference between a DHCP lease and a DHCP reservation. When would you use each, and what happens when a DHCP lease expires if the client is still connected?",
                "answer": "A lease is a temporary assignment from the address pool -- any available address is assigned for a set duration (e.g., 8 days). A reservation permanently assigns a specific IP to a specific MAC address, used for printers, servers, and cameras. When a lease expires on an active client, the client attempts to renew with a DHCP Request; if the server responds with an Acknowledge, the lease is extended.",
                "lines": 6
            },
            {
                "num": "8",
                "question": "REAL WORLD: Users on a network segment report that some devices receive IP addresses in the expected range (192.168.10.x) but others receive addresses in the 169.254.x.x range. Explain what 169.254.x.x addresses indicate, list three possible causes, and describe the first diagnostic command you would run.",
                "answer": "169.254.x.x is an APIPA (Automatic Private IP Addressing) address -- the client could not reach a DHCP server and self-assigned a link-local address. Possible causes: (1) DHCP scope is exhausted; (2) DHCP server is down or unreachable; (3) DHCP relay agent is misconfigured or missing. First command: ipconfig /all on an affected client to confirm no DHCP server is listed, then check scope statistics for lease exhaustion.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    # ── PC TECHNICIAN UNITS ───────────────────────────────────────────────────
    "1.1": {
        "unit": "1.1",
        "title": "Safety and ESD",
        "n10_009": "Core 1 5.1",
        "n10_008": "",
        "questions": [
            {
                "num": "1",
                "question": "ESD stands for _______. It refers to the sudden discharge of static electricity between objects with different _______. Human hands can build up thousands of volts of static electricity -- often with no physical sensation -- yet even as little as _______ volts can permanently damage a sensitive electronic component.",
                "answer": "Electrostatic Discharge; electrical potential (charge); 10-30 volts.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "An ESD wrist strap protects components by keeping the technician at the same _______ as the hardware being worked on. The strap contains a _______ -ohm resistor in series, which prevents the wrist strap from becoming a _______ hazard if the technician contacts live voltage.",
                "answer": "Electrical potential (charge/ground); 1 megaohm (1,000,000); shock (electrocution).",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Antistatic bags protect components during storage and transport. A component should be placed _______ the bag, not _______ it. The outside surface of an antistatic bag can actually _______ static charge and cause ESD damage.",
                "answer": "Inside; on top of (on the outside of); accumulate (hold / concentrate).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Three types of equipment that contain _______ voltages and should NEVER be opened by a PC technician are: _______, _______, and _______. Even when unplugged, these devices can retain a lethal charge.",
                "answer": "High voltages; power supply units (PSU); CRT monitors; laser printers. (Any three of these.)",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Before handling internal components, a technician should remove _______ (such as rings and bracelets) because these can bridge electrical contacts and cause _______. Working on a hard _______ floor (rather than carpet) also reduces static buildup.",
                "answer": "Jewelry (metal jewelry); short circuits (and ESD damage); hard (non-carpeted).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Walking across carpet can generate up to _______ volts of static electricity due to _______. When you then touch a metal object or component, the charge discharges instantly. The safest working surface for PC repair is a/an _______ mat, which dissipates charge slowly and safely.",
                "answer": "35,000 volts (thousands of volts); friction (triboelectric effect); antistatic (ESD).",
                "lines": 3
            },
            {
                "num": "7",
                "question": "A latent ESD failure is one that does not cause _______ failure at the time of the discharge. Instead, the component continues to work but with _______ reliability, and may fail days, weeks, or months later. This makes latent ESD damage especially dangerous because the cause is _______.",
                "answer": "Immediate (instant); degraded (reduced); hard to trace (difficult to identify).",
                "lines": 4
            },
            {
                "num": "8",
                "question": "REAL WORLD: A student technician is upgrading RAM on a desktop. The workbench is carpeted. They remove the RAM from a static bag by setting the bag on the desk and placing the module on top of the bag while they prepare the system. Identify all the ESD safety mistakes in this scenario and explain how each one should be corrected.",
                "answer": "Mistake 1 -- Carpeted surface: carpet generates static. Use an antistatic mat or work on a hard floor. Mistake 2 -- No wrist strap: technician is not grounded. Attach an ESD wrist strap to the wrist and clip to the case chassis. Mistake 3 -- Module placed on top of the static bag: the outside of the bag can accumulate charge. Store the module inside the bag. Mistake 4 -- Not touching the case before starting: should touch an unpainted metal part of the case to equalize charge before handling components.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "1.2": {
        "unit": "1.2",
        "title": "Computing Basics",
        "n10_009": "Core 1 1.1",
        "n10_008": "",
        "questions": [
            {
                "num": "1",
                "question": "Every computer performs four basic functions: _______ (keyboard, mouse), _______ (CPU), _______ (RAM, hard drive), and _______ (monitor, printer). The _______ (CPU) is considered the brain of the computer because it coordinates all four functions.",
                "answer": "Input; processing; storage; output; CPU (Central Processing Unit).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "The CPU's fetch-decode-execute cycle has three steps: it _______ an instruction from memory, _______ the instruction to determine what operation to perform, and then _______ the operation. The speed at which this cycle repeats is measured in _______, with modern CPUs reaching billions of cycles per second (gigahertz).",
                "answer": "Fetches; decodes; executes; clock speed (Hz / GHz).",
                "lines": 3
            },
            {
                "num": "3",
                "question": "A modern CPU has multiple _______, each capable of executing instructions independently. Hyper-threading (Intel) and SMT (AMD) allow each core to handle two _______ simultaneously. A 6-core CPU with hyper-threading appears to the operating system as _______ logical processors.",
                "answer": "Cores; threads; 12 logical processors.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "CPU cache is ultra-fast memory built directly into the processor. _______ cache is the smallest and fastest, holding recently used data for the specific core. _______ cache is slightly larger and shared within a core. _______ cache is the largest and is shared across all cores. Cache reduces the need to access _______, which is much slower.",
                "answer": "L1 cache; L2 cache; L3 cache; RAM (main memory).",
                "lines": 4
            },
            {
                "num": "5",
                "question": "RAM (Random Access Memory) is described as _______ memory because its contents are lost when power is removed. A typical modern desktop uses _______ RAM. The data currently in RAM represents the programs and files that are _______ open and in use.",
                "answer": "Volatile; DDR4 or DDR5; currently (actively).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "When the system runs low on RAM, the OS uses a _______ file (also called virtual memory) on the hard drive as overflow space. This is stored as _______ on Windows. Because hard drive access is much slower than RAM, heavy use of virtual memory results in noticeable system _______.",
                "answer": "Page file; pagefile.sys; slowdown (sluggishness / poor performance).",
                "lines": 3
            },
            {
                "num": "7",
                "question": "A traditional mechanical hard drive (HDD) has typical sequential read speeds of _______ MB/s, while a modern NVMe SSD can reach _______ MB/s or higher. The PSU provides three main DC voltage rails: _______ V (for CPU and GPU), _______ V, and _______ V.",
                "answer": "80-160 MB/s (HDD); 3000-7000 MB/s (NVMe); +12V; +5V; +3.3V.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A user has a 3-year-old desktop with 8 GB of RAM and a mechanical hard drive. They recently upgraded to Windows 11 and opened their usual applications -- a browser with 20 tabs, a video editor, and a spreadsheet. The system is now extremely slow. Using the concepts of RAM, virtual memory, and storage performance, explain what is most likely happening and what upgrade would have the greatest impact on performance.",
                "answer": "With 8 GB of RAM and 20 browser tabs plus a video editor and spreadsheet, the system is exceeding available RAM and is heavily using the page file on the mechanical hard drive. HDD random-access speeds (less than 150 MB/s) are far slower than RAM, causing severe performance degradation whenever virtual memory is used. The single most impactful upgrade would be replacing the HDD with an SSD, which reduces page file latency dramatically. A secondary upgrade would be adding more RAM (16 GB or 32 GB) to reduce page file usage entirely.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "1.3": {
        "unit": "1.3",
        "title": "Number Systems",
        "n10_009": "Core 1 (foundational)",
        "n10_008": "",
        "questions": [
            {
                "num": "1",
                "question": "Binary is a base-_______ number system using only the digits _______ and _______. Each position represents a power of two. Fill in the missing position values from left to right:\n    128  |  ___  |  ___  |  16  |  ___  |  4  |  ___  |  1",
                "answer": "Base-2; 0 and 1. Position values: 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Convert the decimal number 157 to binary. Use the subtraction method: start at the highest position (128), subtract if it fits, and record a 1; otherwise record a 0. Show your work step by step.",
                "answer": "128 fits (157 - 128 = 29). 64 does not fit (29 < 64). 32 does not fit (29 < 32). 16 fits (29 - 16 = 13). 8 fits (13 - 8 = 5). 4 fits (5 - 4 = 1). 2 does not fit (1 < 2). 1 fits (1 - 1 = 0). Result: 10011101.",
                "lines": 5
            },
            {
                "num": "3",
                "question": "Hexadecimal is a base-_______ number system. It uses the digits 0-9 and the letters _______. The letter A = _______, B = _______, C = _______, D = _______, E = _______, F = _______.",
                "answer": "Base-16; A through F. A=10, B=11, C=12, D=13, E=14, F=15.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "To convert binary to hexadecimal, group the binary digits into sets of _______. For example, convert 11001010 to hex:\n    1100 = _______   |   1010 = _______\n    Result in hex: _______",
                "answer": "Groups of 4 (nibbles). 1100 = 12 = C; 1010 = 10 = A. Result: CA (or 0xCA).",
                "lines": 4
            },
            {
                "num": "5",
                "question": "The hexadecimal value 0xFF equals _______ in decimal. In binary, this is _______ (all eight bits set to 1). This is the maximum value that can be stored in _______ byte of memory.",
                "answer": "255; 11111111; one (1).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Data transfer speeds are measured in _______ (bits per second). Storage sizes are measured in _______ (bytes). Since 1 byte = _______ bits, a 1 Gbps (gigabit per second) connection transfers data at _______ MB/s (megabytes per second).",
                "answer": "Megabits or gigabits (Mbps / Gbps); megabytes or gigabytes (MB / GB); 8 bits; 125 MB/s.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "The prefix _______ (e.g., 0xFF) indicates a hexadecimal value. The APIPA address range _______._______.x.x is assigned to a device when it cannot reach a DHCP server. A MAC address is a 48-bit address written as _______ hexadecimal pairs (e.g., AA:BB:CC:DD:EE:FF).",
                "answer": "0x; 169.254; six (6) hexadecimal pairs.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A network technician reads a MAC address filter log and sees the entry: 00:1A:2B:3C:4D:5E. Convert the last octet (5E) from hexadecimal to binary and then to decimal. Explain why hex is used for MAC addresses instead of binary or decimal.",
                "answer": "5E in hex: 5 = 0101, E = 1110, so 5E = 01011110 in binary. 01011110 in decimal: 64+16+8+4+2 = 94. Hex is used for MAC addresses because it is compact (12 hex characters vs. 48 binary digits) and human-readable. Binary is too long to work with; decimal doesn't divide cleanly across 4-bit groups. Each hex digit maps perfectly to exactly 4 binary bits, making encoding and reading addresses efficient.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "2.1": {
        "unit": "2.1",
        "title": "Hardware Components Identification",
        "n10_009": "Core 1 3.4",
        "n10_008": "",
        "questions": [
            {
                "num": "1",
                "question": "LGA (Land Grid Array) sockets have _______ on the motherboard socket itself, while the CPU has flat _______. PGA (Pin Grid Array) sockets have pins on the _______ and the socket has _______. Intel uses _______ sockets; AMD traditionally used _______ sockets (though AM5 is LGA).",
                "answer": "Pins; contact pads; CPU; holes. Intel = LGA; AMD traditionally = PGA (AM4 and earlier).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "On a motherboard, a PCIe x16 slot is _______ than a PCIe x1 slot. An x16 slot is used primarily for _______. A PCIe x1 slot is used for smaller cards such as _______ and _______. A graphics card designed for an x16 slot will/will not fit in an x1 slot.",
                "answer": "Longer; discrete graphics cards (GPUs); sound cards; network cards (any expansion cards). Will NOT fit -- the x16 card is physically longer.",
                "lines": 4
            },
            {
                "num": "3",
                "question": "An M.2 slot on a motherboard is a small _______ -shaped connector on the board surface. It accepts an M.2 SSD that mounts flat against the board and is secured with a single _______. A SATA port, by contrast, is an _______ -shaped connector used with a cable to connect 2.5-inch and 3.5-inch drives.",
                "answer": "Rectangular (edge); screw; L-shaped (right-angle / small rectangular).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "The 24-pin ATX connector supplies _______ from the power supply to the motherboard. The small headers at the front edge of the motherboard connect to _______ panel cables. These cables control the _______ button, _______ LED, and _______ LED.",
                "answer": "Main power (voltage and current); front panel; power; HDD activity; reset.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "SO-DIMM (Small Outline DIMM) RAM modules are used in _______ and are physically _______ than full-size DIMMs used in desktops. A standard desktop DIMM is approximately _______ mm long, while a SO-DIMM is approximately _______ mm long.",
                "answer": "Laptops (and small form factor systems); shorter; 133 mm; 67 mm.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "A system with _______ graphics uses a GPU built into the CPU or motherboard chipset. Display output ports in this case are located on the _______. A _______ GPU is a separate add-in card. When a discrete GPU is installed, display cables should be connected to the _______, not the motherboard.",
                "answer": "Integrated; motherboard (rear I/O panel); discrete; GPU (graphics card).",
                "lines": 3
            },
            {
                "num": "7",
                "question": "High-end discrete GPUs require supplemental power from the PSU via _______ connectors (6-pin or 8-pin PCIe power connectors). These connectors supply the _______ V rail directly to the GPU. If these connectors are not plugged in, the system may _______ or the GPU may not be detected.",
                "answer": "PCIe power (auxiliary power); +12V; fail to POST (not power on / produce no display).",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A student opens a used desktop tower to identify its components before upgrading it. They see a short rectangular connector on the surface of the motherboard, a long connector on the motherboard near a large fan, two different-length slots on the motherboard, and a cable going to the drive labeled SATA. Identify each component and explain the function of two of them in detail.",
                "answer": "Short rectangular connector on the board surface = M.2 slot (for M.2 NVMe or SATA SSDs). Long connector on the motherboard near a large fan = CPU socket (holds the processor). Two different-length motherboard slots = PCIe x16 (for GPU) and PCIe x1 (for expansion cards). Cable labeled SATA = SATA data cable connecting to a hard drive or optical drive. The M.2 slot connects directly to the PCIe bus, bypassing SATA entirely for NVMe speeds. The PCIe x16 slot receives the GPU and feeds it +12V power plus data bandwidth.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "2.2": {
        "unit": "2.2",
        "title": "Motherboards and Architecture",
        "n10_009": "Core 1 3.5",
        "n10_008": "",
        "questions": [
            {
                "num": "1",
                "question": "Match each motherboard form factor to its dimensions:\n    ATX:        _______ mm x _______ mm\n    Micro-ATX:  _______ mm x _______ mm\n    Mini-ITX:   _______ mm x _______ mm\nA smaller motherboard will/will not fit in a larger ATX case.",
                "answer": "ATX: 305 x 244 mm. Micro-ATX: 244 x 244 mm. Mini-ITX: 170 x 170 mm. A smaller motherboard WILL fit in a larger ATX case (using fewer standoffs).",
                "lines": 4
            },
            {
                "num": "2",
                "question": "Socket LGA 1700 is compatible with Intel _______ through _______ generation Core processors. Socket AM4 is compatible with AMD Ryzen _______ through _______ series. A CPU from one socket family _______ (will/will not) fit a motherboard with a different socket.",
                "answer": "12th through 14th generation (Alder Lake, Raptor Lake). AM4 = Ryzen 1000 through 5000 series. Will NOT -- socket incompatibility is physical.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "DDR4 and DDR5 RAM modules are physically _______ with each other. A DDR5 stick _______ (will/will not) physically fit in a DDR4 slot because the _______ (alignment notch) is in a different position. You must match the RAM generation to the _______ specification.",
                "answer": "Incompatible; will NOT; key notch; motherboard's.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "By default, RAM operates at its base _______ (e.g., 4800 MHz for DDR5-4800), not its advertised rated speed. To enable the rated speed, you must enable _______ (Intel) or _______ (AMD) in the UEFI settings. Without this, faster RAM sticks run slower than their marketed specification.",
                "answer": "JEDEC speed; XMP (Extreme Memory Profile); EXPO (Extended Profiles for Overclocking).",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Modern motherboards use _______ firmware instead of the legacy BIOS. UEFI supports the _______ partition table, which allows drives larger than _______ TB and up to 128 primary partitions. Legacy BIOS uses _______ which limits drives to 2 TB.",
                "answer": "UEFI; GPT (GUID Partition Table); 2 TB; MBR (Master Boot Record).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Secure Boot is a UEFI feature that checks the _______ signature of the OS bootloader before allowing it to run. Its purpose is to prevent _______ (malware that infects the boot process) from loading. Secure Boot must be enabled for Windows _______ installation.",
                "answer": "Digital (cryptographic) signature; bootkits / rootkits; 11.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "The CMOS battery (typically a _______ coin cell) powers a small chip that stores the BIOS/UEFI settings when the system is unplugged. If this battery dies, the system will _______ its BIOS settings and reset the _______. Clearing the CMOS (by removing the battery or using the CLRTC jumper) resets all BIOS settings to _______.",
                "answer": "CR2032; lose; date and time; factory defaults.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A customer bought a motherboard (LGA 1700, DDR5 slots) and plans to install a 13th Gen Intel Core i7, two sticks of DDR5-6000 RAM, and a 4 TB NVMe SSD. They want to run Windows 11. List every UEFI setting they should verify before and after installing Windows 11, and explain what could go wrong if each setting is wrong.",
                "answer": "1) XMP/EXPO -- must be enabled for DDR5-6000 (without it, RAM runs at DDR5-4800 JEDEC default, wasting performance). 2) Secure Boot -- must be enabled for Windows 11 (disabled = install blocked or system flags unsupported). 3) Boot order -- set NVMe as primary boot device (wrong order = boots wrong drive or fails to boot). 4) UEFI mode -- must not be in Legacy/CSM mode (CSM mode uses MBR, which cannot address drives larger than 2 TB). 5) TPM 2.0 -- must be enabled (required for Windows 11; without it installation wizard blocks the install).",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "2.3": {
        "unit": "2.3",
        "title": "Storage Devices",
        "n10_009": "Core 1 3.4",
        "n10_008": "",
        "questions": [
            {
                "num": "1",
                "question": "A 5400 RPM HDD is typically used in _______ drives due to lower heat and power consumption. A 7200 RPM HDD provides _______ performance and is common in _______ storage applications. S.M.A.R.T. stands for _______ and is a built-in system that monitors _______ health and predicts potential failure.",
                "answer": "Laptop (mobile); better read/write; desktop; Self-Monitoring, Analysis, and Reporting Technology; drive.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "A _______ sound coming from a hard drive (HDD) is a symptom of mechanical failure -- a read/write head is likely contacting the _______. The correct immediate response is to _______ all important data before the drive fails completely.",
                "answer": "Clicking (grinding); platters (disk surface); back up (copy / save).",
                "lines": 3
            },
            {
                "num": "3",
                "question": "SATA III has a maximum transfer speed of approximately _______ MB/s. An NVMe SSD using PCIe 4.0 can reach speeds of up to _______ MB/s. This means NVMe is roughly _______ times faster than the fastest SATA SSD for sequential reads.",
                "answer": "550 MB/s (SATA III); 7000 MB/s (PCIe 4.0 NVMe); approximately 12-13 times faster.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "An M.2 SSD with the designation 2280 is _______ mm wide and _______ mm long. The M.2 form factor connects directly to the motherboard using an _______ slot, eliminating the need for a _______ cable. M.2 drives can use either the SATA or _______ protocol depending on the type.",
                "answer": "22 mm wide; 80 mm long; M.2; SATA data cable; NVMe.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "RAID 0 stripes data across _______ or more drives for improved _______. It provides _______ (does/does not) redundancy. RAID 1 mirrors data across _______ drives, providing _______ redundancy. If one drive fails in RAID 1, the data is _______ from the mirror.",
                "answer": "Two; performance (speed); does NOT provide redundancy. RAID 1: two drives; full (complete); recovered.",
                "lines": 4
            },
            {
                "num": "6",
                "question": "RAID 5 requires a minimum of _______ drives and distributes _______ data across all drives. If one drive fails, data can be reconstructed using the _______ information. RAID 5 provides both performance and redundancy but _______ (can/cannot) survive a two-drive failure.",
                "answer": "Three (3); parity; parity; cannot survive a two-drive failure.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "FAT32 has a maximum individual file size of _______ GB. This means you _______ (can/cannot) store a 30 GB video file on a FAT32-formatted drive. NTFS and exFAT do not have this limitation. GPT partition style is required when the drive is larger than _______ TB and supports up to _______ primary partitions.",
                "answer": "4 GB; cannot; 2 TB; 128 primary partitions.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A small business owner asks you to set up storage for a file server that needs to survive a single drive failure, maximize storage efficiency, and hold files larger than 4 GB. They have four identical 4 TB drives available. Recommend a RAID level, explain your reasoning, calculate the usable storage, and specify the required file system.",
                "answer": "Recommend RAID 5. It uses three or more drives, distributes parity across all drives, survives one drive failure, and provides better storage efficiency than RAID 1. With four 4 TB drives in RAID 5: usable storage = (4 - 1) x 4 TB = 12 TB (one drive worth used for parity). RAID 1 would yield only 8 TB usable (50% efficiency vs. 75% for RAID 5). File system: NTFS -- required for files over 4 GB (FAT32 4 GB limit) and for Windows file server permissions. Note: RAID is not a backup -- a separate offsite backup should still be maintained.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "2.4": {
        "unit": "2.4",
        "title": "Power and Cooling",
        "n10_009": "Core 1 3.5",
        "n10_008": "",
        "questions": [
            {
                "num": "1",
                "question": "The ATX PSU provides three main DC voltage rails. The _______ V rail powers the CPU and GPU and is the most heavily loaded rail. The _______ V rail powers older drives and some motherboard logic. The _______ V rail powers RAM and low-voltage logic. The wattage rating of the PSU represents its maximum _______ output.",
                "answer": "+12V; +5V; +3.3V; continuous (sustained) power.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "The 80 PLUS certification rates PSU _______. An 80 PLUS Gold PSU achieves approximately _______ % efficiency at 50% load, meaning _______ % of the power drawn from the wall is wasted as heat. A more efficient PSU produces less _______ and reduces electricity costs.",
                "answer": "Efficiency (energy efficiency); 90%; 10%; heat.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "When selecting a PSU wattage, technicians add up the TDP of all components and add _______ to _______ % as a headroom buffer. This prevents the PSU from running near _______ % capacity, which reduces efficiency and component lifespan. A system with a 300W total TDP should use a PSU rated at least _______ W.",
                "answer": "20% to 30%; 100%; 360-390W (300W + 20-30%).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "The EPS _______ -pin connector (sometimes called the CPU power connector) delivers +12V power directly to the _______ voltage regulator module on the motherboard. Without this connector plugged in, high-end CPUs may _______ POST or operate at reduced power.",
                "answer": "8-pin; CPU (motherboard VRM); fail to.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Thermal paste (also called thermal compound) is applied between the CPU and heatsink to fill _______ air gaps in the metal surfaces. It improves _______ transfer from the CPU to the heatsink. The recommended application amount is approximately _______ -sized -- too much can _______ onto the motherboard and cause shorts.",
                "answer": "Microscopic (tiny); heat; pea-sized; spill (spread).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "An AIO (All-In-One) liquid cooler is a _______ cooling system. It consists of a _______ block that mounts on the CPU, connected by tubes to a _______ where heat is dissipated. AIO coolers generally provide _______ thermal performance than air coolers for high-TDP processors, but require more _______ mounting space.",
                "answer": "Closed-loop; pump and cold plate (water block); radiator; better (superior); case (radiator).",
                "lines": 4
            },
            {
                "num": "7",
                "question": "Case fans are labeled with a direction indicator. The _______ side of the fan is the exhaust side. For optimal airflow, intake fans should be mounted at the _______ and front, while exhaust fans go at the _______ and top. A system with more _______ fans than exhaust fans creates positive pressure, which reduces dust buildup.",
                "answer": "Label (sticker) side; bottom; rear; intake.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A student builds a PC and notices that after 10 minutes of gaming, the system stutters, frame rates drop sharply, and then performance returns to normal after a minute. No BSOD occurs. Explain the most likely cause, identify the technical term for this behavior, and describe two corrective actions the technician should take.",
                "answer": "The most likely cause is thermal throttling. When the CPU or GPU reaches its maximum safe operating temperature, it reduces its clock speed to lower heat production -- this causes the performance drop. After a minute of reduced load, temperatures drop and performance recovers. Technical term: thermal throttling (also called dynamic thermal management). Corrective actions: (1) Verify thermal paste is applied correctly -- reapply if the CPU temperature exceeds 90-95 degrees C under load. (2) Check case airflow -- add intake fans, clear cable obstructions, and ensure the exhaust path is unblocked. Also verify the CPU cooler is properly seated with even contact pressure.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "2.5": {
        "unit": "2.5",
        "title": "Build Compatibility",
        "n10_009": "Core 1 3.5",
        "n10_008": "",
        "questions": [
            {
                "num": "1",
                "question": "The most critical compatibility check in any PC build is the CPU _______. A CPU with socket LGA 1700 _______ (will/will not) fit a motherboard with socket AM4. There is _______ physical adapter or workaround that allows a CPU to be used with an incompatible socket.",
                "answer": "Socket; will NOT; no.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "DDR4 and DDR5 RAM are physically _______ with each other because the _______ (alignment notch) is in a different position on each generation. Installing a DDR5 stick into a DDR4 slot is _______ without forcing it, which prevents accidental damage. Always verify the motherboard's _______ specification before purchasing RAM.",
                "answer": "Incompatible; key notch; impossible (physically blocked); memory (RAM).",
                "lines": 3
            },
            {
                "num": "3",
                "question": "GPU physical compatibility requires that the GPU _______ length fits within the case's maximum GPU clearance. A 340mm GPU _______ (will/will not) fit in a case with 310mm GPU clearance. Before buying, check the case _______ for maximum GPU length in millimeters.",
                "answer": "Card; will NOT; specifications (specs / manual).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "PSU wattage should cover the system's total power requirement plus a _______ % to _______ % headroom buffer. A system with a CPU TDP of 125W, GPU TDP of 200W, drives and fans totaling 50W has an estimated total TDP of _______ W. The recommended minimum PSU for this system would be _______ W.",
                "answer": "20%; 30%; 375W total TDP; 450-490W PSU (375W x 1.2 to 1.3).",
                "lines": 3
            },
            {
                "num": "5",
                "question": "A PCIe x16 graphics card _______ (will/will not) fit into a PCIe x1 slot because the x16 card is physically _______ than the x1 slot. However, a PCIe x1 card _______ (will/will not) fit into an x16 slot and will operate at x1 bandwidth. PCIe slots are designed to be electrically _______ compatible.",
                "answer": "Will NOT; longer; will (yes); backward (and forward).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "An ATX power supply _______ (will/will not) fit in a case designed for SFX form factor. ATX PSUs measure approximately _______ mm long, while SFX PSUs are significantly _______. When building a small form factor (SFF) system, always verify that the PSU form factor matches the _______ specifications.",
                "answer": "Will NOT; 140-160mm; shorter (smaller); case.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Before installing a new CPU on an existing motherboard, a technician should consult the manufacturer's _______ to verify the CPU is supported. When a new CPU generation requires a BIOS update for compatibility, the technician must update the BIOS _______ (before/after) installing the new CPU, using a/an _______ CPU that the board already supports.",
                "answer": "CPU support list (QVL); before; compatible (already-supported / older).",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A customer brings in a PC build they assembled at home. It will not POST. They have a 13th Gen Intel Core i9 in an LGA 1700 motherboard, 2 x 16 GB DDR5-5600 RAM, and a 4 TB NVMe SSD. The motherboard is an older model manufactured before 13th Gen CPUs were released. List the compatibility checks you would perform in order and explain what you expect to find.",
                "answer": "Step 1 -- Check CPU compatibility list on the manufacturer website for this exact motherboard model. Older LGA 1700 boards support 12th Gen natively; 13th Gen support requires a BIOS update. Step 2 -- Check BIOS version. If the current BIOS is too old to support 13th Gen, the board will not POST. A BIOS update using a 12th Gen CPU would be needed first. Step 3 -- Verify DDR5 slot compatibility -- confirm the board supports DDR5 (not DDR4). Step 4 -- Verify M.2 slot supports NVMe PCIe 4.0 or 5.0 for the SSD. Step 5 -- Check PSU wattage for a Core i9 + high-end SSD (minimum 650W recommended). Most likely cause: BIOS too old to recognize 13th Gen CPU.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "3.1": {
        "unit": "3.1",
        "title": "Windows Basics",
        "n10_009": "Core 2 1.1",
        "n10_008": "",
        "questions": [
            {
                "num": "1",
                "question": "List three features that are available in Windows _______ but NOT in Windows Home:\n    1. _______ (full-disk encryption)\n    2. _______ (join a company domain)\n    3. _______ (remote into the PC from another device)",
                "answer": "Windows Pro. 1. BitLocker; 2. Domain join (Active Directory); 3. Remote Desktop Protocol (RDP) host.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Task Manager can be opened by pressing _______. The _______ tab in Task Manager shows programs that launch automatically at Windows startup and allows you to _______ or _______ each one. Disabling unnecessary startup programs can improve _______ time.",
                "answer": "Ctrl+Shift+Esc (or Ctrl+Alt+Del, then Task Manager); Startup; enable; disable; boot.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "_______ Manager is the Windows tool that displays all installed hardware devices and their driver status. A yellow exclamation mark indicates a _______ error. A red X means the device is _______. You can access this tool by right-clicking _______ and selecting it from the menu.",
                "answer": "Device; driver (hardware); disabled (not functioning); This PC (or Start, or Computer Management).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "_______ Management is the Windows built-in tool for creating, deleting, formatting, and assigning drive letters to partitions. To open it, press Windows+R and type _______ or right-click the Start button. A volume showing as _______ means it has no file system and cannot store data.",
                "answer": "Disk; diskmgmt.msc; unallocated (RAW).",
                "lines": 3
            },
            {
                "num": "5",
                "question": "_______ Viewer is the Windows tool that records system, application, and security events. To find the cause of a crash, a technician would look in the _______ log under Windows Logs. Each log entry includes a _______ level (Information, Warning, Error, Critical) and a _______ code.",
                "answer": "Event; System (or Application); severity; event ID.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "UAC stands for _______. When a program attempts to make changes to the system, Windows displays a/an _______ prompt asking for confirmation or admin credentials. UAC is designed to prevent _______ from making unauthorized changes without the user's knowledge. UAC can be configured through _______ settings.",
                "answer": "User Account Control; elevation; malware (unauthorized programs); User Account Control (Control Panel / Security settings).",
                "lines": 3
            },
            {
                "num": "7",
                "question": "The System Configuration utility is launched by pressing Windows+R and typing _______. It is primarily used to change _______ options and control which services and programs start with Windows. The command _______ opens the Services management console, where background services can be started, stopped, or set to automatic or manual startup.",
                "answer": "msconfig; startup (boot); services.msc.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A user calls to say their computer is running very slowly since they installed a free PDF converter yesterday. Task Manager shows a process called pdf-helper.exe using 40% CPU at all times. Describe the step-by-step process you would use -- using the Windows tools covered in this unit -- to investigate and resolve the issue.",
                "answer": "Step 1 -- Open Task Manager (Ctrl+Shift+Esc) and confirm pdf-helper.exe CPU usage. Note the file location by right-clicking and selecting Open File Location. Step 2 -- Check Task Manager Startup tab for any pdf-helper entries and disable them. Step 3 -- Open Device Manager to check for unexpected hardware or driver changes from the installation. Step 4 -- Open Event Viewer > Windows Logs > Application to look for error events associated with the PDF converter around the install time. Step 5 -- Uninstall the PDF converter via Settings > Apps. Step 6 -- Run Windows Defender scan to check for bundled malware. Monitor Task Manager after removal to confirm CPU usage drops.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "3.2": {
        "unit": "3.2",
        "title": "Windows Security",
        "n10_009": "Core 2 2.2",
        "n10_008": "",
        "questions": [
            {
                "num": "1",
                "question": "Windows _______ is the built-in antivirus and antimalware solution included with Windows 10 and 11. It provides _______ -time protection by scanning files as they are opened or downloaded. When a third-party antivirus is installed, Windows Defender automatically _______.",
                "answer": "Defender (Windows Defender Antivirus); real; disables itself (turns off).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Windows _______ is a host-based firewall that blocks _______ connections by default. It maintains separate profiles for _______, _______, and _______ networks. Outbound connections are _______ by default, meaning programs can send data out without a firewall rule.",
                "answer": "Firewall; inbound (unsolicited inbound); Domain; Private; Public; allowed.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "BitLocker encrypts the entire _______ drive to protect data if the device is lost or stolen. It requires a _______ chip on the motherboard to store the encryption key securely. If the TPM fails or the drive is moved to a different computer, a _______ key (a 48-digit numeric code) is required to unlock the drive.",
                "answer": "System (OS / hard); TPM (Trusted Platform Module); recovery.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Windows _______ delivers security patches and bug fixes to the operating system. Delaying or disabling updates leaves the system vulnerable to _______ that target known vulnerabilities. Zero-day vulnerabilities are exploits that exist before a _______ is available.",
                "answer": "Update; exploits (malware / attacks); patch.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "UAC has four configurable levels. At the highest level, Windows notifies about _______ system changes. At the default level, Windows notifies only when _______ make changes. At a lower level, UAC notifies only when apps try to install software. Disabling UAC entirely removes all _______ before system changes.",
                "answer": "All; apps (programs); prompts (elevation prompts).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Safe Mode loads Windows with _______ drivers and services, making it useful for diagnosing and removing malware. Safe Mode with _______ allows internet access for downloading tools. Safe Mode can be accessed by holding _______ while clicking Restart, or by pressing F8 during older system boot sequences.",
                "answer": "Minimal (basic); Networking; Shift.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Match each malware type to its description:\n    Ransomware: _______\n    Adware: _______\n    Trojan: _______\n    Rootkit: _______",
                "answer": "Ransomware: encrypts files and demands payment for decryption. Adware: displays unwanted pop-up or injected ads. Trojan: disguises itself as legitimate software to gain access. Rootkit: hides itself and other malware deep in the OS, often at the kernel level.",
                "lines": 5
            },
            {
                "num": "8",
                "question": "REAL WORLD: A user reports that all their document files now have a .locked extension and cannot be opened. A message on the desktop demands payment in cryptocurrency to restore the files. Describe what type of attack this is, explain why restoring from a backup is the safest response, and list two preventive measures that could have prevented this attack.",
                "answer": "This is a ransomware attack. The malware encrypted the user's files using asymmetric encryption -- decrypting without the attacker's key is computationally infeasible. Paying the ransom does not guarantee key delivery. The safest response is to isolate the machine (disconnect from network), wipe the drive, reinstall Windows, and restore files from an offline or cloud backup taken before the infection. Prevention 1: maintain a 3-2-1 backup (3 copies, 2 media types, 1 offsite or offline) so files can be restored without paying. Prevention 2: keep Windows Update current -- most ransomware exploits known vulnerabilities that have existing patches.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "3.3": {
        "unit": "3.3",
        "title": "OS Installation and Recovery",
        "n10_009": "Core 2 1.3",
        "n10_008": "",
        "questions": [
            {
                "num": "1",
                "question": "A _______ install completely wipes the existing drive and installs a fresh copy of Windows, removing all user data and applications. An _______ install preserves the user's files, settings, and installed applications while replacing the OS files. An upgrade is only available from a _______ (older/newer) version of Windows.",
                "answer": "Clean; upgrade (in-place upgrade); supported older.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "_______ is a free tool used to create a bootable USB drive from a Windows ISO file. After downloading the Windows ISO from Microsoft, you point Rufus to the _______ file, select the USB drive, choose the _______ partition scheme (required for UEFI + Windows 11), and click Start.",
                "answer": "Rufus; ISO; GPT.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "To boot from a USB drive, the technician must change the _______ order in UEFI settings so the USB device is listed _______ the hard drive. UEFI settings are accessed by pressing a key such as _______, _______, or _______ immediately when the system powers on (varies by manufacturer).",
                "answer": "Boot; before (above); Del, F2, or F12 (common keys).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Windows 11 requires UEFI boot with _______ disabled (no legacy CSM mode) and a _______ partition table on the drive. It also requires _______ version 2.0 and _______ (a firmware security feature). These requirements exist to improve _______ compared to older Windows versions.",
                "answer": "CSM (legacy mode); GPT; TPM; Secure Boot; security.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Windows Recovery Environment (WinRE) provides repair tools when Windows fails to start. It can be accessed by pressing _______ + Restart in Windows Settings, holding _______ while clicking Restart, or by Windows automatically offering it after _______ consecutive failed boot attempts.",
                "answer": "Shift (Start > Power, hold Shift, click Restart); Shift; two (2) or three (3).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "System Restore returns the OS to a previous _______ point, undoing recent driver or software changes, while preserving _______. Reset This PC re-installs Windows and gives the user the option to _______ or _______ personal files. Reset This PC is more thorough and is closer to a _______ install.",
                "answer": "Restore point; personal files (documents and data); keep; remove; clean.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "After a clean Windows installation, the recommended driver installation order is: _______ drivers first, then _______ drivers, then GPU drivers, then peripheral drivers. The chipset drivers must go first because they enable the CPU, PCIe lanes, and USB controllers that _______ drivers depend on.",
                "answer": "Chipset; motherboard (audio, LAN, etc.); other.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A customer brings in a laptop running Windows 10 with a failed SSD. You replace the SSD with a new NVMe drive and attempt a clean Windows 11 install from USB. The installer says the PC does not meet the requirements. List the most likely causes in order of probability and describe the UEFI settings you would check to resolve each one.",
                "answer": "Most likely causes in order: 1) TPM 2.0 is disabled in UEFI -- check Security settings for TPM/fTPM and enable it. 2) Secure Boot is disabled -- check Boot settings and enable Secure Boot (also requires CSM to be off). 3) CSM (Legacy mode) is enabled -- disable CSM/legacy mode so UEFI-only mode is active; required for GPT and Secure Boot. 4) Drive is MBR-formatted -- new NVMe should default to GPT, but verify the installer uses GPT partitioning. 5) CPU does not meet Windows 11 requirements (check Microsoft compatibility list -- minimum 8th Gen Intel or Ryzen 2000). Resolution: enable TPM, enable Secure Boot, disable CSM, confirm GPT partition scheme in installer.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "4.1": {
        "unit": "4.1",
        "title": "Troubleshooting Methodology",
        "n10_009": "Core 2 5.1",
        "n10_008": "",
        "questions": [
            {
                "num": "1",
                "question": "The CompTIA troubleshooting methodology has _______ steps. Step 1 is _______ the problem. Step 2 is _______ a theory of probable cause. When gathering information in Step 1, open-ended questions (e.g., 'What were you doing when this happened?') are preferred over closed questions because they _______.",
                "answer": "Seven (7); identify; establish; provide more detail / gather more information.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Step 3 is _______ the theory. If the theory is confirmed, proceed to Step 4. If the theory is _______, establish a new theory or escalate. Step 4 is establishing a/an _______ of action to resolve the problem and identifying the potential effects of the fix.",
                "answer": "Test; not confirmed (disproven); plan.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Step 5 is _______ the solution or escalating as necessary, then _______ full system functionality and -- if applicable -- implementing preventive measures. Step 6 is _______ findings, actions, and outcomes, which creates a reference for future repairs and protects the technician legally.",
                "answer": "Implementing; verifying; documenting.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Step 7 is the final step: _______ the user. This includes explaining what caused the problem in non-technical terms, showing the user how to prevent the issue in the future, and confirming _______ with the resolution. This step is often skipped by junior technicians but is important for _______ and professional reputation.",
                "answer": "Educate; satisfaction; customer satisfaction (client relationship).",
                "lines": 3
            },
            {
                "num": "5",
                "question": "The distinction between a _______ and a _______ is critical in troubleshooting. The first is what the user observes or reports (e.g., 'the screen is black'). The second is the underlying technical reason (e.g., 'the GPU is not seated'). Treating a symptom without finding the _______ will result in the problem recurring.",
                "answer": "Symptom; cause (root cause); root cause.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Escalation means passing the problem to a _______ skill level or different team when it is beyond the current technician's ability to resolve. Before escalating, the technician should document what has already been _______ and what the _______ confirmed or ruled out through testing.",
                "answer": "Higher; tried (tested); tests (theory).",
                "lines": 3
            },
            {
                "num": "7",
                "question": "When should a technician consider whether a _______ change occurred recently? If a user says 'it just stopped working,' a technician should ask about any _______, _______, or _______ changes in the recent past, as these are the most common causes of sudden failures.",
                "answer": "Configuration; software updates; hardware changes; settings changes (any combination of recent changes).",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A user calls and says, 'My computer doesn't work.' Using the seven-step troubleshooting methodology, describe the exact questions you would ask in Step 1 and how those questions lead to a testable theory in Step 2. Demonstrate the difference between asking open-ended and closed questions.",
                "answer": "Step 1 -- Identify the problem. Open-ended questions: 'What happens when you turn it on?', 'What were you doing when it stopped working?', 'Has anything changed recently -- updates, new hardware, dropped it?' These gather narrative detail. Closed questions (less useful in Step 1): 'Is it on?' -- yes/no only, provides minimal information. Step 2 -- Based on answers, form a theory. If the user says 'the screen is black but the fans spin,' the theory shifts from will not turn on to a display or POST failure. If the user says 'it happened after a Windows update,' the theory is software-related. Open-ended questions produce a richer symptom description, leading to a more targeted, testable theory.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "4.2": {
        "unit": "4.2",
        "title": "Troubleshooting Hardware",
        "n10_009": "Core 2 5.2",
        "n10_008": "",
        "questions": [
            {
                "num": "1",
                "question": "POST stands for _______. It runs every time a computer _______ and tests the CPU, RAM, storage, and other hardware before loading the OS. If POST fails, the system will _______ with an error code, beep code, or stop code displayed on screen.",
                "answer": "Power-On Self-Test; powers on (boots); halt (stop).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Beep codes are audio signals the motherboard emits when a POST failure occurs before video output is available. The meaning of beep codes varies by _______ manufacturer. One long beep followed by two short beeps on many systems indicates a _______ failure. To interpret a beep code, you should consult the motherboard's _______.",
                "answer": "BIOS (motherboard); video (GPU / display); documentation (manual).",
                "lines": 3
            },
            {
                "num": "3",
                "question": "When a system powers on but shows no display, the first two things to check are: (1) the _______ cable is firmly connected to the correct port (the _______ rather than the motherboard if a discrete GPU is installed), and (2) the _______ is fully seated in its PCIe slot. These steps resolve the majority of no-display issues.",
                "answer": "Monitor (display); GPU (graphics card); GPU (graphics card).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "A _______ sound coming from a hard drive is a serious symptom indicating mechanical failure -- the read/write heads are likely making contact with the _______. The correct response is to _______ immediately before attempting any further diagnosis. Running a drive that is clicking risks permanent _______ loss.",
                "answer": "Clicking (grinding); platters (disk surface); back up all data; data.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Failing RAM typically causes _______ (random errors causing Windows to crash with a blue screen) and random restarts. RAM failure can also prevent POST entirely. To isolate failing RAM, a technician should test _______ stick at a time and run a tool such as _______.",
                "answer": "BSODs (Blue Screens of Death); one; MemTest86.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "_______ are visual display errors such as random pixels, color blocks, or flickering -- they indicate the GPU may be overheating or failing. When the CPU reaches its maximum safe temperature, it reduces its clock speed in a process called _______ _______. If the CPU temperature limit is exceeded, the system will perform a _______ shutdown to prevent damage.",
                "answer": "GPU artifacts (visual artifacts); thermal throttling; emergency (protective) shutdown.",
                "lines": 4
            },
            {
                "num": "7",
                "question": "Visually inspecting a motherboard for _______ capacitors (bulging or leaking tops) is a reliable sign that the board needs to be replaced. A system that will not power on at all -- no fans, no LEDs, nothing -- should first have the technician check the _______ switch on the back of the PSU, which is sometimes accidentally switched to the _______ position.",
                "answer": "Bulging (swollen / failed); rear power (PSU on/off); off (0).",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A user drops off a desktop that was working fine but now powers on, the CPU fan spins, and the keyboard lights flash -- but there is no video output at all and no beep codes. Describe your complete diagnostic process in the correct order, including what you would check, test, or swap at each step.",
                "answer": "Step 1 -- Check the monitor and cable. Test with a known-good monitor and cable connected to the GPU output port (not motherboard). Step 2 -- Reseat the GPU in the PCIe x16 slot and confirm PCIe power connectors are attached. Step 3 -- If still no video, remove the GPU and test with integrated graphics (if CPU has it) connected to the motherboard display port. Step 4 -- Reseat RAM sticks. Try one stick at a time in slot A2 (typically the recommended single-stick slot). Step 5 -- Listen for beep codes -- if a speaker is not connected, connect one to the front panel header. Step 6 -- Clear CMOS by removing the battery for 30 seconds to reset BIOS to defaults. Step 7 -- If none of the above work, suspect a failed CPU, motherboard, or PSU and begin component swap testing.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "4.3": {
        "unit": "4.3",
        "title": "Troubleshooting Software",
        "n10_009": "Core 2 5.3",
        "n10_008": "",
        "questions": [
            {
                "num": "1",
                "question": "Safe Mode starts Windows with only _______ drivers and services loaded. This is useful for diagnosing software issues because malware and problematic drivers are _______ to load. Safe Mode with Networking adds _______ support. Safe Mode is accessed by holding _______ while clicking Restart.",
                "answer": "Minimal (essential); unable (prevented); network; Shift.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "A BCD error message ('Boot Configuration Data file is missing or contains errors') means the Windows _______ store is damaged. The command _______ is run from WinRE Command Prompt to rebuild it. The WinRE command bootrec _______ repairs the master boot record, and bootrec _______ repairs the boot sector.",
                "answer": "Boot configuration data (BCD); bootrec /rebuildbcd; /fixmbr; /fixboot.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Startup Repair is a WinRE tool that automatically scans for and fixes common problems preventing Windows from _______. It is located under Troubleshoot > _______ Options in WinRE. Startup Repair can fix issues such as missing system files, boot manager errors, and _______ configuration.",
                "answer": "Starting (booting); Advanced; BCD (boot).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "When Windows crashes with a BSOD, it writes a mini crash report called a _______ file to the folder _______. These files can be analyzed with tools such as WinDbg or _______ to identify the driver or component that caused the crash. The analysis typically shows a _______ name linked to the failure.",
                "answer": "Minidump; C:\\Windows\\Minidump; BlueScreenView (or WinDbg Preview); driver or module.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "BSOD stop codes are displayed in _______ format. A stop code of 0x0000007E means SYSTEM THREAD EXCEPTION NOT _______. A stop code of 0x000000EF means _______ Process Died. When researching a stop code, the technician should record the _______ hexadecimal value and search the Microsoft documentation for it.",
                "answer": "Hexadecimal; HANDLED; Critical; full.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "When diagnosing slow Windows performance, the three columns to examine in Task Manager's Processes tab are _______, _______, and _______. A process using 100% of any column is the _______ and should be investigated. Disk at 100% on an HDD system often indicates the OS is using the _______ heavily.",
                "answer": "CPU; Memory; Disk; bottleneck; page file (virtual memory).",
                "lines": 3
            },
            {
                "num": "7",
                "question": "If a device stops working after a Windows Update installs a new driver, a technician can use _______ Manager to roll back the driver. Right-clicking the device and selecting _______ opens the properties dialog, where the _______ Driver button returns to the previously working version.",
                "answer": "Device; Properties; Roll Back.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A user reports that Windows boots to the login screen, they enter their password, and then the desktop loads briefly before logging them out automatically and showing a 'temporary profile' notification. They have noticed this for the last two days. Identify the problem, explain what is causing it, and describe the complete repair procedure.",
                "answer": "The problem is a corrupted user profile. When Windows cannot load the primary user profile (profile hive is locked or corrupted), it falls back to a temporary profile that is discarded on logout -- all changes are lost. Cause: often a result of a crash or improper shutdown during a Windows Update that was writing to the registry hive. Repair: Step 1 -- Log in as a different administrator account (or use Safe Mode). Step 2 -- Open Registry Editor (regedit) and navigate to HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\ProfileList. Step 3 -- Find the entry for the affected user profile (it may have a .bak extension on the SID key). Rename the .bak entry to remove .bak, and if two entries exist for the same SID, delete the non-.bak one. Step 4 -- Reboot and log in normally -- Windows will reload the original profile. Step 5 -- Back up the fixed profile and document the repair.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "5.1": {
        "unit": "5.1",
        "title": "Customer Professionalism",
        "n10_009": "Core 2 4.1",
        "n10_008": "",
        "questions": [
            {
                "num": "1",
                "question": "Active listening means giving the customer your full _______ and not interrupting them. After they finish speaking, a technician should _______ back what they said to confirm understanding (e.g., 'So what I'm hearing is...'). This technique is called _______ and reduces misunderstandings and repeat calls.",
                "answer": "Attention; repeat (paraphrase); reflective listening (paraphrasing / active feedback).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Open-ended questions cannot be answered with yes or no and _______ more information from the customer (e.g., 'Can you describe what happens when you turn it on?'). Closed questions _______ the answer to yes or no (e.g., 'Does it turn on?'). Open-ended questions should be used primarily at the _______ of the troubleshooting conversation.",
                "answer": "Gather (elicit); limit; beginning.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Before beginning any repair, a professional technician should set _______ by communicating the estimated _______ of the repair and its likely _______ to the customer. If unexpected complications arise during the repair, the technician should _______ the customer before proceeding rather than surprising them later.",
                "answer": "Expectations; timeline (duration); cost (price); notify (contact).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "When explaining a technical issue to a non-technical customer, a good technician avoids _______ (technical language and acronyms the customer does not understand) and uses _______ instead. For example, instead of saying 'the HDD is experiencing read/write head actuator failure,' say '_______'.",
                "answer": "Jargon; plain language (analogies); something like: 'the part that reads your files is broken and we need to replace the drive.'",
                "lines": 4
            },
            {
                "num": "5",
                "question": "When repairing a customer's device, a technician must respect the customer's _______ by only accessing files, folders, and data that are _______ to the repair. Accessing personal photos, documents, or accounts that are not related to the technical problem is _______ and could violate _______ laws.",
                "answer": "Privacy; necessary (relevant); unethical (unprofessional); privacy.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Escalation is the process of transferring a problem to a _______ -level technician or specialist when the issue is beyond the current technician's _______ or _______. Before escalating, the technician should document what has been _______ and share that information with the next technician to avoid repeating steps.",
                "answer": "Higher; skill level; authority; tested (tried).",
                "lines": 3
            },
            {
                "num": "7",
                "question": "After completing a repair, the technician should document all _______ performed, all _______ replaced or installed, and the _______ to the problem. Following up with the customer after service -- for example, calling the next day to confirm everything is working -- builds _______ and reduces call-backs.",
                "answer": "Work (steps); parts (components); solution (root cause and fix); trust (customer satisfaction).",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: You arrive to repair a business client's computer. The client is agitated and says, 'This is the third time this has happened -- your company always does a bad job.' You believe the recurring issue is caused by something the client is doing. Describe how you would handle this situation professionally, using the communication techniques from this unit.",
                "answer": "Step 1 -- Remain calm. Do not become defensive or argue. Let the client express their frustration without interruption. Step 2 -- Use active listening and reflective listening: 'I hear that this has been very frustrating, and I want to make sure we resolve it correctly this time.' Step 3 -- Ask open-ended questions to understand the full history: 'Can you walk me through what happens each time this occurs? Is there a pattern in when it starts?' Step 4 -- Avoid blame or defensiveness about previous visits -- document what you find. Step 5 -- Set clear expectations: 'I will diagnose the root cause today and explain exactly what is causing the recurring issue before I leave.' Step 6 -- If the client is causing the issue, explain it plainly without jargon: 'It looks like the issue may be connected to how the software updates are being handled -- I can show you a quick step that will prevent this.' Step 7 -- Follow up the next day to confirm resolution.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
}


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Generate BeattieNetTrack resource PDFs')
    parser.add_argument('--unit', help='Unit number to process (e.g. 1.1.1)')
    parser.add_argument('--all', action='store_true', help='Process all built-in units')
    parser.add_argument('--data', help='Path to JSON file with unit data')
    parser.add_argument('--data-dir', help='Directory of JSON files to process in batch')
    parser.add_argument('--output-root', default='public/resources/network-engineer',
        help='Output root directory (default: public/resources/network-engineer)')
    args = parser.parse_args()

    units_to_process = []

    if args.data:
        with open(args.data) as f:
            units_to_process.append(json.load(f))
    elif args.data_dir:
        for jf in sorted(Path(args.data_dir).glob('*.json')):
            with open(jf) as f:
                units_to_process.append(json.load(f))
    elif args.all:
        units_to_process = list(UNITS.values())
    elif args.unit:
        if args.unit not in UNITS:
            print(f"ERROR: Unit {args.unit} not found in built-in data.")
            print(f"Available: {', '.join(UNITS.keys())}")
            sys.exit(1)
        units_to_process.append(UNITS[args.unit])
    else:
        parser.print_help()
        sys.exit(0)

    for unit_data in units_to_process:
        process_unit(unit_data, output_root=args.output_root)

    print(f'\nDone. {len(units_to_process)} unit(s) processed.')


if __name__ == '__main__':
    main()