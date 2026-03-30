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
    # ── TECH+ UNITS (FC0-U71) ────────────────────────────────────────────────
    # DOMAIN 2 -- Infrastructure
    "tp-2.1": {
        "unit": "tp-2.1",
        "title": "Common Computing Devices",
        "n10_009": "FC0-U71 2.1",
        "n10_008": "FC0-U71 2.1",
        "questions": [
            {
                "num": "1",
                "question": "A _______ is a full-powered computer with separate components (tower, monitor, keyboard) designed for a fixed location. A _______ integrates all components into a portable unit with a built-in screen and battery. A _______ is a portable touchscreen device, typically without a physical keyboard.",
                "answer": "Desktop; laptop; tablet.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "A _______ is a purpose-built computer that provides resources (files, print, web, database) to many client devices over a network. Servers typically have multiple _______ (processors), large amounts of _______, and enterprise-grade reliability features such as ECC memory and RAID storage.",
                "answer": "Server; CPUs (processors); RAM.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "A _______ (IoT device) is any internet-connected device that is not a traditional computer, such as a smart thermostat, IP camera, or wearable. These devices typically have _______ (limited/unlimited) processing power and often run _______ operating systems with minimal user interaction.",
                "answer": "Smart device (IoT); limited; embedded.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "A thin client is a low-powered device that relies on a _______ server to do most processing. The thin client handles _______ (input/output on the screen, keyboard/mouse) but the actual computation and storage happen on the server. This model reduces _______ and simplifies updates.",
                "answer": "Remote; input/output (display and interaction); hardware cost.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "A workstation is a high-performance desktop designed for resource-intensive tasks such as _______, _______, or _______ (name at least two). Workstations typically have ECC RAM, professional-grade _______, and may support multiple monitors.",
                "answer": "Video editing, 3D rendering, CAD/engineering design, scientific simulation; GPU (graphics card).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Match each device to its primary use case:\n    Laptop: _______\n    Tablet: _______\n    Desktop: _______\n    Server: _______",
                "answer": "Laptop: mobile productivity; Tablet: content consumption, touchscreen interaction; Desktop: stationary, upgradeable workstation; Server: providing services to multiple clients.",
                "lines": 4
            },
            {
                "num": "7",
                "question": "A _______ is a handheld computer that combines phone and computing functions, running a mobile OS such as Android or iOS. It includes sensors such as _______, _______, and _______ that traditional desktops lack, enabling location services, motion detection, and photography.",
                "answer": "Smartphone; GPS, accelerometer, camera (any three sensors).",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A small dental office is choosing between deploying thin clients connected to a central server vs. individual laptops for each workstation. List two advantages of thin clients for this scenario and two advantages of laptops, then explain which solution you would recommend and why.",
                "answer": "Thin client advantages: lower hardware cost per station; centralized management (software updates and backups happen on the server, not each device); easier to secure because patient data never sits on individual machines. Laptop advantages: work continues if the server goes down; staff can work from outside the office; each device is independently functional. Recommendation: thin clients are better for a dental office because patient records (HIPAA-protected data) should be stored centrally and never on portable devices that could be lost or stolen. Centralized backups also reduce the risk of data loss.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-2.2": {
        "unit": "tp-2.2",
        "title": "Internal Components",
        "n10_009": "FC0-U71 2.2",
        "n10_008": "FC0-U71 2.2",
        "questions": [
            {
                "num": "1",
                "question": "The _______ is the main circuit board that connects all other components. It holds the _______ socket (where the processor plugs in), RAM slots, PCIe slots, and SATA connectors. The chipset on the motherboard manages _______ between the CPU, RAM, and expansion cards.",
                "answer": "Motherboard; CPU; communication (data flow).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "RAM stands for _______ and is a _______ (volatile/non-volatile) form of memory, meaning data is lost when power is removed. The CPU uses RAM to store data _______ is currently working on. More RAM allows more programs to run _______ without performance degradation.",
                "answer": "Random Access Memory; volatile; it (the CPU); simultaneously.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "The GPU (Graphics Processing Unit) is responsible for rendering _______ on a display. It can be _______ (built into the motherboard or CPU) or _______ (a dedicated add-in card in a PCIe slot). Professional workloads like video editing and machine learning also leverage GPU _______ processing power.",
                "answer": "Images/video (graphics); integrated; discrete (dedicated); parallel.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "The PSU (Power Supply Unit) converts _______ current (from the wall outlet) to _______ current at voltages the computer components require (typically 3.3V, 5V, and 12V). A PSU is rated in _______, which is the maximum total power it can provide to all components at once.",
                "answer": "Alternating current (AC); direct current (DC); watts.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "NIC stands for _______ and provides the hardware interface between the computer and the network. Wired NICs use an _______ port (RJ-45 connector). Wireless NICs use _______ or _______ radio standards. Most modern motherboards have a NIC _______ (built in).",
                "answer": "Network Interface Card; Ethernet; Wi-Fi (802.11); Bluetooth; integrated.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "The CPU cooler sits on top of the CPU and dissipates _______ generated by the processor. It transfers heat from the IHS (Integrated Heat Spreader) to either a _______ (passive metal fin array) or an _______ (liquid loop). Thermal paste between the CPU and cooler improves _______ transfer.",
                "answer": "Heat; heatsink; all-in-one liquid cooler (AIO); thermal (heat).",
                "lines": 3
            },
            {
                "num": "7",
                "question": "PCIe (Peripheral Component Interconnect Express) slots on the motherboard allow expansion cards to be added. Common expansion cards installed in PCIe slots include: _______, _______, _______, and _______ (list at least three).",
                "answer": "Discrete GPU, dedicated NIC, sound card, RAID controller, capture card (any three).",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A video editor complains their computer is running very slowly when exporting 4K video, even though the system has a fast CPU. Upon investigation, the technician finds only 8 GB of RAM and a motherboard with an integrated GPU. Identify two specific component upgrades that would most improve export performance and explain why each helps.",
                "answer": "Upgrade 1 -- Add more RAM (to 32 GB or 64 GB): video editing software uses large amounts of RAM to hold frame buffers, preview renders, and project files. With only 8 GB, the OS is likely using the page file (slow SSD/HDD swap), which dramatically reduces performance. More RAM lets the editor work with more data in fast volatile memory. Upgrade 2 -- Add a discrete GPU: 4K video export leverages GPU hardware encoding (NVENC on NVIDIA, AMF on AMD). An integrated GPU lacks dedicated VRAM and compute units, forcing encoding onto the CPU. A dedicated GPU can accelerate encoding by 5-10x for H.264/H.265 export.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-2.3": {
        "unit": "tp-2.3",
        "title": "Storage Devices",
        "n10_009": "FC0-U71 2.3",
        "n10_008": "FC0-U71 2.3",
        "questions": [
            {
                "num": "1",
                "question": "A HDD (Hard Disk Drive) stores data on _______ platters that spin at speeds like 5,400 or 7,200 _______. A read/write _______ moves across the platters to access data. Because of these moving parts, HDDs are more susceptible to _______ damage from dropping.",
                "answer": "Magnetic; RPM (revolutions per minute); head (arm); physical (shock).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "An SSD (Solid State Drive) stores data using _______ (NAND flash) chips with no moving parts. Compared to an HDD, an SSD is _______ (faster/slower), _______ (more/less) resistant to physical shock, and _______ (more/less) expensive per gigabyte.",
                "answer": "Flash memory; faster; more resistant; more expensive.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "An M.2 NVMe SSD connects directly to the _______ bus via a slot on the motherboard, achieving speeds of _______ to _______ GB/s. A SATA SSD is limited to approximately _______ MB/s because SATA was designed for spinning hard drives.",
                "answer": "PCIe; 3 to 7+ GB/s; 550-600 MB/s.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "SATA (Serial AT Attachment) is the interface used by most _______ and 2.5-inch _______ drives. SATA III has a maximum speed of _______ Gbps (approximately 600 MB/s). The SATA cable carries _______ only; a separate power cable connects from the PSU.",
                "answer": "HDDs; SATA SSDs; 6 Gbps; data (signal).",
                "lines": 3
            },
            {
                "num": "5",
                "question": "An optical drive reads and writes data to _______ using a laser. Common formats include CD (_______ MB), DVD (_______ GB), and Blu-ray (_______ GB). Optical drives are becoming less common in modern systems because _______ and digital distribution have replaced physical media.",
                "answer": "Discs; 700 MB; 4.7 GB; 25-50 GB; USB drives (flash storage).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "RAID (Redundant Array of Independent Disks) combines multiple drives for performance or redundancy. RAID 0 (striping) _______ performance but provides _______ redundancy -- if one drive fails, all data is lost. RAID 1 (mirroring) duplicates data across _______ drives for redundancy at the cost of _______ the usable storage.",
                "answer": "Improves; no; two; half (50%).",
                "lines": 3
            },
            {
                "num": "7",
                "question": "NAS (Network Attached Storage) is a dedicated storage device connected to a network, allowing multiple _______ to access shared files. It differs from DAS (Direct Attached Storage) in that DAS connects _______ to a single computer, while NAS is accessible to anyone on the _______.",
                "answer": "Clients (users/computers); directly; network.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A school is upgrading 40 student laptops that currently use 256 GB HDDs. The budget allows for either SATA SSDs or NVMe SSDs as replacements. The primary use case is running Windows, a web browser, and Office applications. Which storage upgrade would you recommend and why? Is NVMe worth the additional cost for this scenario?",
                "answer": "Recommendation: SATA SSD is the better choice for this scenario. Reasons: Both SATA SSD and NVMe SSD are dramatically faster than spinning HDDs for the workloads described (OS boot, browser, Office) -- students would see essentially identical real-world improvement from either. SATA SSDs cost significantly less per gigabyte than NVMe. The bottleneck for these tasks is not storage throughput -- it is RAM, CPU, and network latency. NVMe drives reach their advantage during large sequential reads/writes (video editing, virtual machines, large file transfers), which these students are not doing. Saving money on storage can fund other improvements like RAM upgrades.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-2.4": {
        "unit": "tp-2.4",
        "title": "Display Types",
        "n10_009": "FC0-U71 2.4",
        "n10_008": "FC0-U71 2.4",
        "questions": [
            {
                "num": "1",
                "question": "LCD (Liquid Crystal Display) monitors use a _______ to illuminate a liquid crystal panel. LEDs are used as the backlight in most modern LCDs. The liquid crystals themselves _______ (produce/block and filter) light to create the image.",
                "answer": "Backlight; block and filter.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "OLED (Organic Light Emitting Diode) displays differ from LCDs because each pixel _______ its own light -- there is no separate backlight. This allows OLED to produce perfect _______ (true 0 luminance) by simply turning pixels off. The downside is potential _______ from prolonged static images.",
                "answer": "Emits (produces); blacks; burn-in.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Resolution is measured in _______ x _______ (horizontal x vertical). Common resolutions include 1920x1080 (_______ or Full HD), 2560x1440 (_______), and 3840x2160 (_______ or 4K UHD). Higher resolution displays show _______ detail but require more GPU power.",
                "answer": "Pixels; pixels; 1080p (FHD); 1440p (QHD); 2160p (4K); more.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Refresh rate is measured in _______ (Hz) and indicates how many times per second the display updates the image. A 60 Hz monitor updates _______ times per second. A 144 Hz gaming monitor updates _______ times per second, making fast motion appear _______ and more responsive.",
                "answer": "Hertz; 60; 144; smoother.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Response time is measured in _______ (ms) and indicates how quickly a pixel can change from one color to another. Lower response time reduces _______, a blurring effect seen behind fast-moving objects. For competitive gaming, a response time of _______ ms or less is generally preferred.",
                "answer": "Milliseconds; ghosting; 1-5 ms.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Three major display connector types are _______ (older analog standard), _______ (digital, carries audio and video, widely used), and _______ (high-speed digital, supports high refresh rates and daisy-chaining). Modern GPUs and monitors have moved away from _______ because it is an analog signal.",
                "answer": "VGA; HDMI; DisplayPort; VGA.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Brightness is measured in _______ (nits). A typical office monitor is around 250-350 nits. HDR (High Dynamic Range) content requires _______ peak brightness to show the difference between dark and bright areas. Viewing angle determines how far off-center a user can sit before _______ shifts.",
                "answer": "Nits (cd/m2); high (600+ nits); color.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A graphic designer is buying a new monitor for photo and video editing work. They are choosing between a high-refresh-rate gaming monitor (165 Hz, TN panel) and an IPS panel color-accuracy monitor (60 Hz, wide color gamut). Which should they choose and why? What is the most important spec for their use case?",
                "answer": "The IPS color-accuracy monitor is the correct choice. For photo and video editing, the most important specifications are: color accuracy (Delta E), color gamut coverage (sRGB or Adobe RGB/DCI-P3), and panel type. IPS panels offer wide viewing angles and accurate color reproduction. TN panels, while fast, have noticeably worse color accuracy and narrow viewing angles -- colors shift when viewed off-center. A graphic designer needs to be confident that the colors they see on screen match what will print or what clients will see on other devices. High refresh rate and response time are priorities for gaming, not creative work. The 60 Hz IPS is the professional choice.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-2.5": {
        "unit": "tp-2.5",
        "title": "Connectors and Cables",
        "n10_009": "FC0-U71 2.5",
        "n10_008": "FC0-U71 2.5",
        "questions": [
            {
                "num": "1",
                "question": "USB Type-A connectors are the _______ (flat rectangular) end that plugs into the _______, such as a computer tower or charger. USB Type-B is a square-ish connector used on _______ such as printers. USB Type-C is reversible and used for both _______ and _______ in modern devices.",
                "answer": "Host; data and power (charging).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "HDMI cables carry both _______ and _______ signals in a single cable. HDMI 1.4 supports up to 4K at _______ Hz. HDMI 2.0 supports 4K at _______ Hz. DisplayPort can support higher _______ rates than HDMI, making it preferred for high-refresh gaming monitors.",
                "answer": "Video and audio; 30 Hz; 60 Hz; refresh.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "A Thunderbolt 3 or 4 port uses the same physical _______ connector as USB-C but supports speeds up to _______ Gbps, can carry _______ (video output), _______ (USB protocols), and even PCIe data. Thunderbolt is identified by the _______ icon next to the port.",
                "answer": "USB-C; 40 Gbps; DisplayPort (video); USB; lightning bolt.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "RJ-45 is the connector used for _______ networking cables (Ethernet). It has _______ pins. RJ-11 is used for _______ lines and has _______ pins. A _______ cable is used to connect a computer directly to another computer without a switch.",
                "answer": "Wired (Ethernet); 8 pins; telephone (DSL/POTS); 6 pins; crossover.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "3.5mm audio jacks are color coded: _______ (lime green) is for headphones/speakers (output), _______ (pink or red) is for microphone (input), and _______ (blue) is for line-in from an external audio source. The jack carries an _______ (digital/analog) audio signal.",
                "answer": "Green; pink/red; blue; analog.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "SATA data cables are _______ (wide/narrow) L-shaped connectors carrying only _______ between the motherboard and drive. SATA power cables come from the _______ and carry 3.3V, 5V, and 12V rails. Molex connectors are an older _______ (data/power) connector used for fans and older peripherals.",
                "answer": "Narrow; data; PSU (power supply); power.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "The DB9 (DE-9) connector is a 9-pin serial port used for _______ devices such as older modems and network equipment console connections. The DB15 (DE-15) is a _______ pin VGA video connector. Both are examples of _______ -style connectors, named for their D-shaped metal shell.",
                "answer": "Legacy serial; 15; D-sub.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A student wants to connect a new 4K 144 Hz gaming monitor using a cable they found in a drawer. The cable is HDMI 1.4. They plug it in and the monitor only runs at 4K 30 Hz. Explain why this is happening, what the limitation is, and what cable they need to get the full 144 Hz at 4K.",
                "answer": "HDMI 1.4 has a maximum bandwidth of 10.2 Gbps, which is only sufficient for 4K at 30 Hz. Running 4K at 144 Hz requires approximately 48 Gbps of bandwidth. To achieve 4K 144 Hz, the student needs either: HDMI 2.1, which supports up to 48 Gbps and handles 4K 144 Hz natively, or DisplayPort 1.4, which supports 32.4 Gbps and can run 4K up to 120 Hz with Display Stream Compression (DSC). The monitor and GPU must also both support the required cable standard. The old HDMI 1.4 cable is the bottleneck -- replacing it with HDMI 2.1 or DisplayPort 1.4/2.0 will resolve the issue.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-2.6": {
        "unit": "tp-2.6",
        "title": "Peripherals",
        "n10_009": "FC0-U71 2.6",
        "n10_008": "FC0-U71 2.6",
        "questions": [
            {
                "num": "1",
                "question": "_______ are output devices that produce physical copies of digital documents. A _______ printer uses liquid ink sprayed through nozzles and is good for _______ printing. A _______ printer uses heat and a toner drum and is better for high-volume _______ printing.",
                "answer": "Printers; inkjet; color/photo; laser; document (black-and-white).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "A _______ is an input device that converts a physical document or photo into a digital image file. A _______ combines a printer, scanner, and sometimes a fax machine into one device. When a scanner is connected to a network and shared, multiple users can scan to _______.",
                "answer": "Scanner; multifunction printer (MFP/all-in-one); email/shared folders.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Keyboards and mice connect via _______ (wired USB) or _______ (2.4 GHz USB dongle or Bluetooth). A _______ keyboard has a physical USB dongle that plugs into the host computer and communicates over a proprietary 2.4 GHz signal, while a _______ keyboard pairs directly with the Bluetooth radio in the host device.",
                "answer": "Wired; wireless; wireless (RF); Bluetooth.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "A _______ is an input device that translates hand/stylus movement directly on a flat surface into cursor movement on screen, used by artists and designers. A _______ captures live video and audio and is used for video calls. A _______ is a special projector-style input surface that detects touch.",
                "answer": "Graphics tablet; webcam; interactive whiteboard (smartboard).",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Speakers and headphones are _______ devices that convert digital audio signals (passed through a DAC) into _______ sound waves. Headsets combine headphones with a _______ for two-way audio. USB audio devices include their own _______ and do not rely on the motherboard sound chip.",
                "answer": "Output; analog; microphone; DAC (digital-to-analog converter).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "KVM (Keyboard Video Mouse) switch allows _______ computers to share a single set of peripherals. The user presses a _______ to toggle control between machines. KVM switches are useful in data centers where many servers must be managed from _______ keyboard and monitor.",
                "answer": "Multiple; button (hotkey); one.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "A _______ converts digital files to 3D physical objects by depositing material layer by layer. The most common consumer type uses _______ filament (plastic) melted through a heated nozzle. A _______ scanner captures the shape of a physical object as a 3D digital model. Together these tools form part of a digital _______ workflow.",
                "answer": "3D printer; FDM (fused deposition modeling); 3D; fabrication (manufacturing).",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A small law office is replacing their aging all-in-one inkjet printer. They print about 500 pages per day in black and white, with occasional color printing for client cover sheets. They also frequently need to scan multi-page contracts. What type of printer/scanner setup would you recommend and why? Consider cost per page, speed, and document handling.",
                "answer": "Recommendation: A business-class laser multifunction printer with an automatic document feeder (ADF). Reasons: (1) Cost per page -- laser toner is far cheaper per page than inkjet ink at 500 pages/day; ink costs would be excessive. (2) Speed -- laser printers print at 30-60+ ppm; inkjets are much slower for volume. (3) ADF -- automatically feeds multi-page documents through the scanner without manual page-by-page placement, essential for scanning contracts. (4) Reliability -- laser printers are designed for high-volume use; inkjets will fail far sooner at this volume. A color laser MFP gives them occasional color at reasonable cost while keeping daily black-and-white costs low.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-2.7": {
        "unit": "tp-2.7",
        "title": "Network Devices",
        "n10_009": "FC0-U71 2.7",
        "n10_008": "FC0-U71 2.7",
        "questions": [
            {
                "num": "1",
                "question": "A _______ operates at Layer 2 (Data Link) and forwards traffic based on _______ addresses. It creates a _______ collision domain per port, isolating each connected device. This is the primary device used to connect computers within a local area network (LAN).",
                "answer": "Switch; MAC; separate.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "A _______ operates at Layer 3 (Network) and forwards traffic between different networks based on _______ addresses. The router in a home connects the local network to the _______ (Internet). It is the default _______ for devices on the LAN.",
                "answer": "Router; IP; Internet (ISP); gateway.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "A WAP (Wireless Access Point) provides _______ network connectivity by broadcasting an _______ using a radio signal. A home wireless router combines a router, switch, and _______ into one device. An enterprise may have _______ WAPs managed by a central wireless controller.",
                "answer": "Wi-Fi (wireless); SSID; WAP (wireless access point); many.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "A _______ (cable/DSL modem) converts the signal from an ISP (Internet Service Provider) into a format the local network can use. _______ modems use a coaxial cable connection. _______ modems use a telephone line. The word modem comes from _______ and _______ because it converts between analog and digital signals.",
                "answer": "Modem; cable; DSL; modulate; demodulate.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "A _______ is a network security device that monitors and controls incoming and outgoing traffic based on _______ rules. A hardware firewall is a dedicated _______ device protecting the entire network. A software firewall runs on an _______ device and protects only that machine.",
                "answer": "Firewall; policy/security; network; individual (host).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "A _______ (network hub) is a legacy Layer 1 device that broadcasts every packet to _______ ports. This creates a _______ collision domain and wastes bandwidth. Hubs have been replaced by _______ in all modern networks because switches forward traffic only to the intended recipient.",
                "answer": "Hub; all; shared (single); switches.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "PoE (Power over Ethernet) allows a _______ cable to carry both data and _______ power. This is used to power devices such as _______, _______, and _______ (list at least two) without requiring a separate power outlet at each device location.",
                "answer": "Ethernet (Cat5e/Cat6); electrical (DC); IP cameras, VoIP phones, wireless access points (any two).",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A school IT team is upgrading a computer lab with 30 student computers. They currently have one old hub connecting all machines. They notice that when multiple students download files simultaneously, everyone's connection slows to a crawl. Explain why this is happening and how replacing the hub with a managed switch would solve the problem.",
                "answer": "A hub operates at Layer 1 and broadcasts every frame out of every port. All 30 computers share one collision domain. When multiple computers transmit simultaneously, their signals collide, forcing CSMA/CD back-off retransmission, which dramatically reduces throughput. Each computer effectively divides the total bandwidth by 30. A managed switch operates at Layer 2 and maintains a MAC address table. It forwards each frame only to the correct destination port, giving each computer a dedicated collision domain. With a 1 Gbps switch, each of the 30 computers gets its own 1 Gbps link rather than sharing one. This eliminates collisions and allows simultaneous downloads at full speed.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-2.8": {
        "unit": "tp-2.8",
        "title": "Internet Connection Types",
        "n10_009": "FC0-U71 2.8",
        "n10_008": "FC0-U71 2.8",
        "questions": [
            {
                "num": "1",
                "question": "DSL (Digital Subscriber Line) delivers internet over _______ phone lines. Download speeds are typically _______ (faster/slower) than upload because consumer DSL is _______. DSL requires a _______ at the customer premises to connect to the home network.",
                "answer": "Copper telephone; faster; asymmetric (ADSL); DSL modem.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Cable internet uses _______ coaxial cable, the same infrastructure used for _______ TV. It is delivered to the home via a _______ modem. Like DSL, cable is typically asymmetric -- _______ speeds are higher than _______ speeds.",
                "answer": "Coaxial; cable; DOCSIS; download; upload.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Fiber optic internet transmits data as _______ pulses through glass or plastic strands. It offers speeds from _______ Mbps to multiple _______ and is completely immune to _______ interference. Fiber is symmetric, meaning upload and download speeds are _______.",
                "answer": "Light (photon); 100 Mbps; Gbps; electromagnetic (EMI); equal.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Satellite internet works by transmitting signals to and from a _______ in orbit. Traditional geostationary satellites sit at approximately _______ km altitude, causing high _______ (100-600 ms). Low-earth orbit (LEO) satellite services like Starlink orbit at approximately 550 km, reducing latency to _______ ms.",
                "answer": "Satellite; 35,786 km (geostationary orbit); latency; 20-40 ms.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Cellular internet (4G LTE / 5G) uses _______ towers to deliver wireless broadband. It is the primary broadband option in _______ areas without wired infrastructure. 5G mmWave frequencies offer very high speeds but have limited _______ and cannot penetrate _______ well.",
                "answer": "Cell; rural; range; walls (buildings).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "A _______ uses a cell phone data connection to share internet with nearby Wi-Fi devices. This is known as _______ or personal hotspot. The main limitation is that usage counts against the phone plan data _______ and battery life is _______ while hotspot is active.",
                "answer": "Mobile hotspot (smartphone); tethering; cap (allotment); reduced.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "WiMAX is a _______ wireless broadband standard with a range of up to _______ km under ideal conditions. It was intended to provide wireless broadband to areas without cable or DSL infrastructure. It has largely been superseded by _______ and _______ in most markets.",
                "answer": "802.16; 50 km; 4G LTE; 5G.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A family moves to a rural property 15 miles outside of any city. DSL and cable are not available. They need reliable internet for remote work (video calls, cloud file sharing) and school (video lessons, homework). Compare the two realistic options available -- satellite and cellular -- and recommend one based on their specific needs.",
                "answer": "Option 1 -- Satellite (LEO like Starlink): download 50-250 Mbps, upload 10-20 Mbps, latency 20-40 ms, monthly cost higher, requires dish hardware purchase. Suitable for video calls and streaming. Option 2 -- Cellular (4G LTE): speeds vary widely by tower proximity and carrier (5-100 Mbps), latency typically 30-50 ms, monthly data caps possible, no hardware to install. Recommendation: LEO satellite (Starlink) is better for this family because rural areas often have poor cellular coverage, and the data caps on cellular plans make heavy video call and cloud use expensive. Starlink provides consistent speeds sufficient for multiple simultaneous users and has low enough latency for video calls. The upfront hardware cost is offset by reliability.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-2.9": {
        "unit": "tp-2.9",
        "title": "Network Types",
        "n10_009": "FC0-U71 2.9",
        "n10_008": "FC0-U71 2.9",
        "questions": [
            {
                "num": "1",
                "question": "A LAN (Local Area Network) covers a _______ geographic area such as a single _______ or office. Devices on a LAN communicate at _______ speeds (typically 1 Gbps on modern wired networks). The key device connecting LAN devices is the _______.",
                "answer": "Small; home (building); high; switch.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "A WAN (Wide Area Network) spans _______ geographic areas and connects multiple LANs. The Internet is the largest example of a _______. WANs use _______ provided by ISPs (leased lines, fiber, etc.) to link distant locations. WAN links typically have _______ (higher/lower) latency than LAN.",
                "answer": "Large; WAN; infrastructure (carrier links); higher.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "A WLAN (Wireless LAN) uses _______ signals instead of physical cables to connect devices. The IEEE standard for Wi-Fi is _______. A WLAN is still a _______ -- it just uses wireless transmission within that local area. A _______ provides the wireless signal in a WLAN.",
                "answer": "Radio; 802.11; LAN; WAP (wireless access point).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "A MAN (Metropolitan Area Network) is larger than a _______ but smaller than a _______. It typically covers a _______, campus, or city district. Examples include a city-wide cable TV network or a _______ network connecting multiple university buildings.",
                "answer": "LAN; WAN; city (metropolitan area); municipal.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "A PAN (Personal Area Network) covers a very _______ range (typically _______ meters) and connects personal devices near a single individual. _______ and _______ are the most common PAN technologies. An example is a laptop connected to wireless earbuds.",
                "answer": "Short; 10; Bluetooth; NFC (near-field communication).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "A VPN (Virtual Private Network) creates an _______ tunnel over a public network (like the Internet), allowing remote users to access a _______ network as if they were physically present on it. Data inside the VPN tunnel is _______, protecting it from interception on the public network.",
                "answer": "Encrypted; private (corporate); encrypted.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "An intranet is a _______ network accessible only to authorized internal users within an organization. An extranet extends access to _______ (partners, vendors) with appropriate permissions. Neither is the same as the _______, which is a public network accessible to anyone.",
                "answer": "Private (internal); external parties; Internet.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A company has offices in Austin, TX and Boston, MA. Each office has its own LAN. Developers in both offices need to access the same internal code repository server located in Austin. Describe the network types involved and explain how a VPN could be used to give the Boston team secure access to the Austin server across the Internet.",
                "answer": "Each office has a local LAN for internal device communication. The two LANs are connected across the Internet (a WAN). The company can use a site-to-site VPN by installing VPN concentrators at each office. The concentrators establish an encrypted tunnel over the Internet between Austin and Boston. All traffic between the two LANs travels through this tunnel. The Boston developers can reach the Austin code repository server as if they were on the local Austin network, and all data in transit is encrypted. No external attacker intercepting the Internet traffic can read the contents because it appears as encrypted VPN packets. This is more secure than exposing the code repository directly to the public Internet.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-2.10": {
        "unit": "tp-2.10",
        "title": "Virtualization",
        "n10_009": "FC0-U71 2.10",
        "n10_008": "FC0-U71 2.10",
        "questions": [
            {
                "num": "1",
                "question": "Virtualization allows one physical machine (the _______) to run multiple simulated environments called _______ (VMs). A _______ is the software layer that creates and manages VMs. Examples include VMware vSphere, Microsoft Hyper-V, and _______.",
                "answer": "Host; virtual machines; hypervisor; VirtualBox (or KVM).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "A Type 1 hypervisor runs _______ on bare metal hardware, without a host OS underneath. Examples include VMware _______ and Microsoft _______. A Type 2 hypervisor runs on top of an existing _______ and is used on workstations. Examples include _______ and VirtualBox.",
                "answer": "Directly; ESXi; Hyper-V; OS; VMware Workstation.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Server consolidation uses virtualization to run many VMs on fewer _______ machines. If a company runs 20 servers at 5% CPU utilization each, they waste _______ capacity. Consolidating them onto fewer powerful physical hosts improves _______ utilization and reduces hardware, power, and _______ costs.",
                "answer": "Physical; 95%; resource; cooling.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "A VM _______ is a saved state of a VM at a point in time. If a software update or configuration change breaks the VM, the administrator can _______ to the snapshot and restore the prior state. This is a powerful feature for _______ environments where changes carry risk.",
                "answer": "Snapshot; revert (roll back); test/staging.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Containers (like _______ ) differ from VMs because they share the _______ kernel of the host OS rather than running a separate OS per instance. Containers are _______ (more/less) lightweight and start _______ (faster/slower) than VMs. They are commonly used in microservices and cloud deployments.",
                "answer": "Docker; OS (host); more; faster.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "VDI (Virtual Desktop Infrastructure) hosts users _______ on a central server. End users connect with _______ clients or thin clients. The advantage is that data and processing stay in the _______, making it secure and easy to manage. The risk is that if the server goes down, _______ users lose access.",
                "answer": "Desktop environments (operating system desktops); remote desktop; data center; all.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "VM isolation means that a _______, crash, or attack inside one VM does not _______ other VMs running on the same host (under normal conditions). Each VM has _______ virtual hardware resources. This containment is what makes virtualization valuable for running _______ or testing malware.",
                "answer": "Virus; affect; isolated; sandboxing.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A cybersecurity teacher wants students to practice using Kali Linux for penetration testing exercises. The school computers run Windows 10 and cannot be reimaged. The teacher does not want students reachable from the school network during labs. Explain how virtualization solves all three constraints and describe the specific configuration you would set up.",
                "answer": "Solution: Install VirtualBox (Type 2 hypervisor) on each Windows 10 machine. Create a Kali Linux VM inside VirtualBox on each student computer. This solves all three constraints: (1) No reimaging needed -- Kali runs inside Windows as a guest VM; the host Windows system is unaffected and students can switch between Kali and Windows. (2) Network isolation -- configure each Kali VM with a Host-Only or NAT network adapter instead of a Bridged adapter. Host-Only creates a private network visible only to the host, preventing the VM from reaching the school network or being reached by other machines on the LAN. (3) Repeatable clean state -- create a base snapshot after initial setup so students can revert after each lab.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-2.11": {
        "unit": "tp-2.11",
        "title": "Cloud Computing",
        "n10_009": "FC0-U71 2.11",
        "n10_008": "FC0-U71 2.11",
        "questions": [
            {
                "num": "1",
                "question": "Cloud computing delivers _______ resources (compute, storage, networking) over the Internet on demand. The three main service models are _______ (managed infrastructure -- VMs and storage), _______ (managed platform -- deploy apps without managing servers), and _______ (managed software -- use apps via browser).",
                "answer": "IT; IaaS (Infrastructure as a Service); PaaS (Platform as a Service); SaaS (Software as a Service).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "The four cloud deployment models are: _______ (resources owned and operated by one organization), _______ (resources provided by a vendor to the general public over the internet), _______ (two or more organizations share cloud infrastructure), and _______ (combines private + public cloud).",
                "answer": "Private; public; community; hybrid.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "_______ (the ability to grow resources up or out as demand increases) and _______ (the ability to shrink resources when demand decreases) are key cloud advantages. Combined, they allow organizations to pay only for what they _______ and avoid over-provisioning hardware that sits _______ during low usage periods.",
                "answer": "Scalability; elasticity; use; idle.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "In cloud computing, the _______ model means customers pay only for what they use -- per hour, per GB, or per API call -- instead of large upfront hardware purchases. This converts capital expenditures (CapEx) to _______ expenditures (OpEx). The cloud provider owns and maintains the _______ infrastructure.",
                "answer": "Pay-as-you-go (consumption-based); operational; physical.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "A _______ is a geographic region where a cloud provider operates multiple data centers. Within a region, there are multiple _______ (physically separate buildings) to provide _______ -- if one building loses power, the others continue. Customers choose a region to reduce _______ for their users.",
                "answer": "Region; availability zones; redundancy (high availability); latency.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "SaaS (Software as a Service) examples include _______, _______, and _______ (list three examples). In SaaS, the provider manages the _______, _______, and _______ -- the customer just uses the application. The customer does _______ manage any servers or platform.",
                "answer": "Microsoft 365, Google Workspace, Salesforce (any three); infrastructure, platform, and software; not (does not).",
                "lines": 3
            },
            {
                "num": "7",
                "question": "A CDN (Content Delivery Network) stores _______ copies of content (images, videos, web pages) at servers geographically distributed around the world called _______ _______ Points. When a user requests content, they are served from the _______ edge node, reducing latency and load on the _______ server.",
                "answer": "Cached; Points of Presence (PoPs) / edge nodes; nearest; origin.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A startup is building a mobile app. They expect low traffic for the first 6 months, but if a major influencer promotes them they could see a 50x spike overnight. They have a budget of $500/month at launch. Explain why the cloud is a better fit for this scenario than buying physical servers, and name the service model they would most likely use.",
                "answer": "Buying physical servers requires large upfront capital expenditure (CapEx) -- a small startup spending $500/month cannot fund servers capable of handling a 50x traffic spike. Physical servers also sit mostly idle during low-traffic months, wasting money. With IaaS or PaaS on a cloud provider (AWS, Azure, or GCP), the startup pays only for what they use during low-traffic months. When the influencer spike hits, auto-scaling can spin up additional compute instances within minutes to handle demand. After the spike, instances scale back down. This elasticity is impossible with owned physical hardware. Most app startups would use PaaS (like AWS Elastic Beanstalk or Google App Engine) or IaaS (EC2 / Compute Engine) depending on how much control they need over the environment.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-2.12": {
        "unit": "tp-2.12",
        "title": "Internet of Things (IoT)",
        "n10_009": "FC0-U71 2.12",
        "n10_008": "FC0-U71 2.12",
        "questions": [
            {
                "num": "1",
                "question": "IoT stands for _______ of _______. It refers to everyday physical devices -- beyond traditional computers -- that are connected to the _______ and can send or receive data. Examples include smart _______, wearable _______, and industrial _______ sensors.",
                "answer": "Internet of Things; Internet; thermostats; fitness trackers; equipment.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "IoT devices commonly communicate using low-power wireless protocols such as _______ (personal area network), _______ (short-range wireless), _______ (long-range low-power), and Wi-Fi. The choice of protocol depends on required _______, power constraints, and _______ range.",
                "answer": "Zigbee; Bluetooth (BLE); LoRa / LoRaWAN; bandwidth; communication.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "IoT devices often run _______ operating systems with minimal resources (small CPU, limited RAM). Because they are difficult to _______, many become security liabilities as vendors stop releasing _______ patches. This is known as the IoT _______ problem.",
                "answer": "Embedded; update (patch); firmware; security (attack surface).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "An IoT _______ is a hub device that collects data from local IoT sensors and aggregates or preprocesses it before sending to the cloud. This reduces _______ and allows some functions to work even without an active _______ connection. The gateway also acts as a _______ between IoT protocols and IP networking.",
                "answer": "Gateway; bandwidth; Internet; bridge (translator).",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Edge computing in IoT means processing data _______ to where it is generated rather than sending all data to a remote cloud. This reduces _______, saves _______ bandwidth, and allows faster response. A self-driving car is an example -- it cannot wait _______ ms for the cloud to decide whether to brake.",
                "answer": "Closer (at the device or local gateway); latency; network; 100+.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "The attack surface of IoT devices is large because they often have: default _______ that users never change, no _______ update mechanism, exposure on the _______ if firewalls are not configured, and minimal _______ logging for anomaly detection.",
                "answer": "Passwords; automatic patch/firmware; Internet; security.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "A _______ attack leverages thousands of compromised IoT devices (botnet) to flood a target server with traffic, overwhelming it. The 2016 _______ botnet used IoT cameras and routers with default credentials to launch massive DDoS attacks. Organizations can mitigate this by segmenting IoT devices on a separate _______ VLAN.",
                "answer": "DDoS; Mirai; isolated (dedicated).",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A hospital is planning to deploy 200 internet-connected patient monitoring sensors throughout patient rooms. The IT security team is concerned about the security risks. Identify three specific security risks introduced by these IoT devices and provide a corresponding mitigation strategy for each.",
                "answer": "Risk 1 -- Default credentials: many IoT devices ship with default admin passwords. Mitigation: change all default credentials to unique strong passwords before deployment; document them in a secure password manager. Risk 2 -- Unpatched firmware: medical IoT vendors may stop releasing firmware updates, leaving known vulnerabilities unpatched. Mitigation: establish a vendor contract requiring firmware support lifecycle; monitor CVE databases for the device models; isolate on a VLAN so an exploited device cannot reach patient records on the main network. Risk 3 -- Network exposure / lateral movement: a compromised sensor on the hospital network could be used as a pivot point to attack EMR servers. Mitigation: segment all IoT devices on an isolated VLAN with firewall rules permitting only the specific traffic needed (data upload to the monitoring server), blocking all other lateral traffic.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-2.13": {
        "unit": "tp-2.13",
        "title": "Embedded Systems",
        "n10_009": "FC0-U71 2.13",
        "n10_008": "FC0-U71 2.13",
        "questions": [
            {
                "num": "1",
                "question": "An embedded system is a _______ computing system built into a device for a specific _______ function. Unlike a general-purpose computer, an embedded system is not designed to run _______ different applications. Examples include _______, _______, and _______ (name three devices).",
                "answer": "Dedicated; purpose-built; many; microwave ovens, traffic lights, washing machines (any three).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "A microcontroller is the primary chip inside many embedded systems. It integrates a _______ (processor), _______ (program storage), _______ (working memory), and I/O interfaces all into a single _______. This makes it compact, cheap, and power-efficient for dedicated tasks.",
                "answer": "CPU; flash memory (ROM); RAM; chip (IC).",
                "lines": 3
            },
            {
                "num": "3",
                "question": "An RTOS (Real-Time Operating System) is designed to process inputs and produce outputs within a _______ deadline. Hard real-time systems must meet every deadline or the system _______. Examples include engine control units in cars and medical _______ where a missed deadline could cause harm.",
                "answer": "Guaranteed (strict); fails (malfunctions); devices (pacemakers).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Firmware is software stored in _______ (non-volatile memory, often flash or ROM) inside a hardware device. It controls the basic operation of the device at a _______ level. Unlike standard software, firmware _______ (can/cannot) usually be updated without special tools or vendor authorization, and updates carry _______ risk if interrupted.",
                "answer": "Non-volatile memory (flash/ROM); low (hardware level); can; high (bricking the device).",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Embedded systems are common in _______ (vehicles with computerized fuel and emissions control), _______ (insulin pumps, defibrillators), _______ (assembly robots, PLCs), and _______ (routers, switches). In critical systems, embedded software is subject to rigorous _______ testing before deployment.",
                "answer": "Automotive; medical devices; industrial (manufacturing); networking equipment; safety/reliability.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "The three main constraints of embedded systems that limit them compared to general-purpose computers are limited _______ (CPU speed), limited _______ (RAM and flash), and limited _______ (battery or power supply). These constraints require developers to write highly _______ code with minimal overhead.",
                "answer": "Processing (compute); memory; power; optimized (efficient).",
                "lines": 3
            },
            {
                "num": "7",
                "question": "An SoC (System on a Chip) integrates all major components of a computer -- _______, _______, and _______ controllers -- into a single silicon die. SoCs are common in _______ phones, _______ devices, and embedded systems because they reduce size, cost, and power consumption.",
                "answer": "CPU, GPU, memory; I/O; smartphones; IoT.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A car manufacturer recalls 50,000 vehicles because of a critical software bug in the embedded engine control unit (ECU) that can cause unintended acceleration. Unlike a PC software bug, the fix cannot simply be emailed to users. Explain what challenges the manufacturer faces in updating the embedded firmware and describe two methods they could use to deliver the fix.",
                "answer": "Challenges: (1) ECUs run firmware stored in non-volatile flash memory, not on a hard drive -- updating requires specialized hardware interfaces (OBD-II port, J-Tag) or a specific programming protocol. (2) A failed or interrupted firmware flash can brick the ECU (leave the car inoperable), so the update must be safe, checksummed, and reliable. (3) Not all owners bring their car to a dealer promptly. Method 1 -- Dealer OBD-II flash: customers bring the vehicle to a dealer where a technician connects a programmer to the OBD-II diagnostic port and flashes the updated firmware file -- safe, controlled environment. Method 2 -- OTA (Over-the-Air) update via cellular: if the vehicle has a telematics module with a data connection (like Tesla), the manufacturer pushes the signed firmware update wirelessly. The ECU validates the signature before applying the update, and it applies only when the vehicle is parked with the engine off to avoid interruption.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    # DOMAIN 3 -- Applications and Software
    "tp-3.1": {
        "unit": "tp-3.1",
        "title": "Operating System Types",
        "n10_009": "FC0-U71 3.1",
        "n10_008": "FC0-U71 3.1",
        "questions": [
            {
                "num": "1",
                "question": "An operating system (OS) is the software that manages a computer's _______ resources and provides services to application software. Without an OS, application programs would have to individually control every piece of _______ themselves. The OS acts as a _______ between hardware and applications.",
                "answer": "Hardware; hardware; intermediary (abstraction layer).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "A _______ OS is designed for multi-user, multi-tasking environments on shared hardware. A _______ OS (like Windows 10/11) is designed for single-user productivity on personal computers. A _______ OS (like Android/iOS) is optimized for battery life and touchscreen interaction on handheld devices.",
                "answer": "Server; desktop (workstation); mobile.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Windows is developed by _______ and holds approximately _______ % of the desktop OS market. Windows uses a _______ (graphical) interface by default. The Windows Registry is a centralized database that stores _______ settings for the OS and applications.",
                "answer": "Microsoft; ~70-75%; GUI; configuration.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "macOS is developed by _______ and runs on _______ hardware (primarily Apple Mac computers). It is built on a _______ foundation (derived from BSD Unix). This gives macOS access to a _______ terminal and Unix-compatible command-line tools.",
                "answer": "Apple; Apple; Unix/BSD; Terminal (command-line).",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Linux is an open-source OS kernel first created by _______ in 1991. A Linux _______ is a complete OS built around the Linux kernel plus additional software. Examples include Ubuntu, _______, and _______. Linux is dominant in _______ and cloud infrastructure.",
                "answer": "Linus Torvalds; distribution (distro); Fedora, Debian (any two); servers.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Chrome OS is developed by _______ and is built on the _______ kernel. It is designed primarily to run _______ and Android apps. Chrome OS is popular in _______ because devices are inexpensive and easy to manage centrally via Google Admin console.",
                "answer": "Google; Linux; web (browser); schools (K-12 education).",
                "lines": 3
            },
            {
                "num": "7",
                "question": "An embedded OS (like _______ RTOS or VxWorks) runs inside specialized hardware with no GUI. Mobile OSes include _______ (Google, open source) and _______ (Apple, closed). The key difference between mobile and desktop OSes is that mobile OSes are optimized for _______ efficiency and _______ interfaces.",
                "answer": "FreeRTOS; Android; iOS; power (battery); touch.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A school district is choosing an OS for 500 new student laptops. Options are Windows 11, Chromebook (Chrome OS), and Ubuntu Linux. The laptops will be used for web browsing, Google Classroom, and basic word processing. Budget is tight. Which OS would you recommend and why? Include at least two reasons.",
                "answer": "Chrome OS (Chromebook) is the best recommendation for this scenario. Reason 1 -- Cost: Chromebooks are significantly cheaper than Windows or MacOS devices (often $200-350 vs $600+). Reason 2 -- Management: Google Admin console allows one IT admin to manage all 500 devices centrally -- push policies, reset passwords, enforce content filters, and remotely wipe stolen devices. Reason 3 -- Use case alignment: the students only need a web browser and Google Classroom -- Chrome OS is built exactly for this workload. Reason 4 -- Security: Chrome OS auto-updates silently, sandboxes each app/tab, and verifies OS integrity on boot (Verified Boot), making it highly secure with near-zero IT maintenance. Ubuntu would require more technical management; Windows requires more expensive hardware and licenses.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-3.2": {
        "unit": "tp-3.2",
        "title": "Application Software",
        "n10_009": "FC0-U71 3.2",
        "n10_008": "FC0-U71 3.2",
        "questions": [
            {
                "num": "1",
                "question": "Application software is designed to help users perform _______ tasks, as opposed to _______ software (like the OS) which manages hardware. Common categories include _______ software (Word, Docs), _______ software (Firefox, Chrome), and _______ software (Photoshop, Premiere).",
                "answer": "Specific (productive); system; productivity (word processing); web browser; creative (multimedia).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "_______ software requires installation to a local storage device and runs using the local CPU and RAM. _______ software (SaaS) runs in a web browser and requires no local installation -- processing occurs on a _______ server. The advantage of web-based apps is accessibility from _______ device with a browser.",
                "answer": "Locally installed; web-based; remote; any.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "A _______ is a set of programs sold together, such as Microsoft 365 (Word, Excel, PowerPoint, Outlook). _______ software is provided at no charge. _______ is initially free but requires payment to unlock full features. _______ is software that has been permanently made free by its original developer.",
                "answer": "Software suite; freeware; freemium (shareware); abandonware.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "_______ source software provides users access to the source code and the freedom to use, modify, and distribute it. The Linux kernel is an example. _______ source software does not provide the source code and restricts copying and modification. Windows and macOS are examples.",
                "answer": "Open; closed (proprietary).",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Business software categories include: _______ (stores and queries structured data), _______ (tracks stock and orders), _______ (manages customer interactions), and _______ (tracks financial records). Modern businesses often rely on _______ versions of these delivered as SaaS.",
                "answer": "Database management system (DBMS); inventory management; CRM (Customer Relationship Management); accounting software; cloud.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Collaboration software allows multiple users to work together remotely. Examples include _______ (real-time document co-editing), _______ (team messaging and file sharing), and _______ (video meetings). These tools depend on _______ connectivity and typically sync changes via _______.",
                "answer": "Google Docs or Microsoft 365; Slack or Teams; Zoom or Teams; internet; cloud servers.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Vertical software is designed for a specific _______ (e.g., dental practice management, point-of-sale for retail). Horizontal software is designed for _______ industries (e.g., word processors, spreadsheets). Vertical software is often more _______ and less flexible, but better suited to the specific _______.",
                "answer": "Industry; any (general); expensive; workflow.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A small restaurant owner asks you whether they should buy desktop accounting software like QuickBooks Desktop or use a subscription-based cloud version like QuickBooks Online. They have one computer, limited IT knowledge, and need to access the financials occasionally from their phone while at the market. Which would you recommend and give three specific reasons.",
                "answer": "Recommend QuickBooks Online (cloud/SaaS). Reason 1 -- Mobile access: they can access their financials from any device with a browser -- including their phone at the market -- without VPN or special setup. Reason 2 -- No maintenance: cloud version automatically updates and backs up data on the vendor servers; no user action required. A non-technical owner should not be responsible for local backups and updates. Reason 3 -- Disaster recovery: if the one desktop computer fails or is stolen, desktop software data could be lost; cloud data is stored remotely and accessible immediately from another device. The subscription cost is offset by not needing IT support for updates and recovery.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-3.3": {
        "unit": "tp-3.3",
        "title": "Software Licenses",
        "n10_009": "FC0-U71 3.3",
        "n10_008": "FC0-U71 3.3",
        "questions": [
            {
                "num": "1",
                "question": "A software _______ is a legal agreement that grants users permission to use software under specific conditions. Without a license, using software is _______ infringement. An _______ (End User License Agreement) is the license document users must accept before installation.",
                "answer": "License; copyright; EULA.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "A _______ license allows software to be installed on one computer or used by one named user. A _______ license allows any number of users within an organization to use the software. A _______ license is tied to a specific device rather than a specific user.",
                "answer": "Per-seat (single-user); enterprise (volume); per-device.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Open source licenses allow users to freely use, modify, and often _______ software. The GPL (GNU General Public License) requires that any derivative work also be released under the _______ license -- this is called _______ licensing. The MIT license is more _______, allowing use in proprietary products.",
                "answer": "Redistribute; GPL (same open source); copyleft; permissive.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "_______ is software in the public domain -- copyright has expired or been waived -- and anyone can use it without a license. _______ software is free to distribute but may restrict modification or commercial use. _______ software is commercial software that users can try before buying, often with limited features or a time limit.",
                "answer": "Public domain; freeware; shareware (trial).",
                "lines": 3
            },
            {
                "num": "5",
                "question": "A subscription license requires periodic _______ payments to maintain access. Examples include Microsoft 365 and Adobe Creative Cloud. If the subscription _______, access to the software is typically revoked. The advantage for vendors is _______ revenue; the advantage for users is always receiving _______ updates.",
                "answer": "Recurring; expires (lapses); recurring (predictable); the latest (current).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Concurrent (floating) licenses allow a defined number of _______ simultaneous users, regardless of how many total users are licensed. If all _______ are in use, additional users must _______ until a license is released. This model is efficient for software used occasionally by many people.",
                "answer": "Maximum; seats (licenses); wait.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Software _______ is the illegal copying, distribution, or use of software beyond the terms of its license. Common violations include installing one licensed copy on _______ computers, sharing license _______ online, and using cracked software. Penalties include _______ fines and civil lawsuits.",
                "answer": "Piracy; multiple; keys; financial.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A business of 25 employees uses Microsoft Office. They currently own 5 retail boxed copies installed on several shared computers. Employees complain they cannot access Word on their own machines. The IT admin wants to fix this. Describe the most appropriate licensing model for this business and how it differs from what they currently have.",
                "answer": "The business should purchase a Microsoft 365 Business subscription (subscription/per-seat model). Currently they have 5 retail perpetual licenses tied to specific devices -- only users at those 5 machines can use Office. Microsoft 365 Business licenses each user (per-seat), so each of the 25 employees gets a named license that allows them to install Office on up to 5 of their own devices (PC, Mac, tablet, phone). Benefits: all 25 employees have access from their own devices; licenses are managed centrally in the Microsoft admin portal; the business always has the latest version; licenses can be added or removed as staff changes. This replaces the inefficient shared-device model and eliminates compliance risk from overuse.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-3.4": {
        "unit": "tp-3.4",
        "title": "Software Installation and Configuration",
        "n10_009": "FC0-U71 3.4",
        "n10_008": "FC0-U71 3.4",
        "questions": [
            {
                "num": "1",
                "question": "Software installation copies program files to the _______ drive and registers the application with the _______ (on Windows). Common installer formats on Windows include _______ (installer executables) and _______ (Microsoft Installer packages). On macOS, applications are often packaged as _______ files.",
                "answer": "Hard/SSD; Registry; .exe; .msi; .dmg (disk image).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "A package manager automates _______, _______, and _______ of software. Linux distros use package managers like _______ (Debian/Ubuntu) and _______ (Red Hat/Fedora). macOS uses _______ (third-party). Windows 11 introduced the _______ package manager.",
                "answer": "Installation, updating, removal; apt; dnf/yum; Homebrew; winget.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "A _______ installation stores all program files within the application bundle, avoiding conflicts with other software. A _______ installation installs shared components into system directories and registers them with the OS, which may cause _______ conflicts when multiple apps share the same library versions.",
                "answer": "Portable (self-contained); standard (traditional); dependency (DLL).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Software _______ are released to fix security vulnerabilities or bugs. _______ are larger releases that add major features or overhaul components. _______ updates are small, frequent patches between versions. Keeping software updated reduces the _______ of exploitation from known vulnerabilities.",
                "answer": "Patches; major (version) updates; minor (point); risk.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Driver software allows the OS to _______ with hardware devices. Without the correct driver, the OS cannot use the device. Drivers are often installed automatically via _______ or downloaded from the _______ website. An incorrect or corrupted driver can cause _______ (Blue Screen of Death) on Windows.",
                "answer": "Communicate; Windows Update; manufacturer's; BSOD.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Before installing software on a corporate device, an IT department should: verify the software is _______ through legal channels, check _______ minimum requirements, test on a _______ machine first, and ensure the software does not violate _______ security policies.",
                "answer": "Licensed; hardware/system; non-production (test); company.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Silently installing software means installing with _______ user interaction, which is useful for deploying to many machines via _______ remote management tools. Windows Group Policy and tools like _______ or Microsoft Endpoint Manager (Intune) enable _______ deployment of software across an organization.",
                "answer": "No; MDM/RMM; SCCM (System Center Configuration Manager); automated (bulk).",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A user downloads and installs a free video converter they found through a search engine. After installation their browser homepage changes, pop-up ads appear, and scans detect potentially unwanted programs (PUPs). Explain what likely happened and what steps the technician should take to clean and prevent this in the future.",
                "answer": "What happened: The installer used a bundled installation -- in addition to the video converter, additional software (a browser hijacker, adware, or PUPs) was secretly included in the installer package. The user likely clicked through the installer without reading each screen, accepting all optional bundles by default. Remediation steps: (1) Uninstall the video converter and all unknown programs installed around the same date via Programs and Features. (2) Run a PUP scan with Malwarebytes or a similar tool. (3) Reset the browser homepage, search engine, and extensions. (4) Check startup programs (Task Manager > Startup) and disable unknown entries. Prevention: only download software from official vendor websites or verified app stores; read every page of installers and choose custom install to deselect bundled extras; use a browser extension or DNS filter to block known malware domains.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-3.5": {
        "unit": "tp-3.5",
        "title": "Cloud Computing and Software",
        "n10_009": "FC0-U71 3.5",
        "n10_008": "FC0-U71 3.5",
        "questions": [
            {
                "num": "1",
                "question": "SaaS (Software as a Service) delivers applications over the _______ through a web browser. The user does not install or maintain the software -- the _______ handles all updates and infrastructure. Examples include _______, _______, and _______.",
                "answer": "Internet; provider (vendor); Google Docs, Microsoft 365 Online, Salesforce (any three).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Cloud storage services like _______, _______, and _______ let users store files on remote servers accessible from any device. Files are synchronized between devices and stored redundantly. The main risk is _______ if the account is compromised or the provider experiences an outage.",
                "answer": "OneDrive, Google Drive, Dropbox (any three); data loss / inaccessibility.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "A _______ (virtual desktop) lets a user access a full computing environment hosted in the cloud through a thin client or browser. All processing and storage happen on the _______ server. This model simplifies _______ management because the desktop is in one centralized location.",
                "answer": "Cloud desktop (VDI); remote (cloud); endpoint.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "API stands for _______ and allows different software applications to communicate with each other over a network. Cloud services expose _______ that developers use to integrate features (like payment processing, maps, or authentication) into their own applications. Today most public APIs use the _______ architectural style.",
                "answer": "Application Programming Interface; APIs; REST.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Web applications run inside a _______ and require no local installation. They use HTML, CSS, and _______ on the client side. Complex web apps may use frameworks like _______ or _______. A _______ (Progressive Web App) can be installed to the home screen of a mobile device and work offline.",
                "answer": "Browser; JavaScript; React or Angular (examples); PWA.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Cloud software updates are _______ (pushed automatically by the vendor). Users always have the _______ version without action. The downside is that businesses have _______ control over when updates occur. Enterprise cloud plans often offer _______ deployment rings to test updates before full rollout.",
                "answer": "Automatic; latest (current); less; staged.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Multi-tenancy means multiple _______ share the same underlying cloud infrastructure, with their data logically _______ from each other. This reduces cost for the vendor through economies of scale. Security concern: if the _______ is breached or misconfigured, another tenant's data could potentially be exposed.",
                "answer": "Customers (tenants); separated (isolated); isolation layer.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A company currently stores all customer data on a local file server. The IT manager wants to move to cloud storage. One employee raises a concern: 'What happens to our data if the cloud provider goes out of business or raises prices dramatically?' Explain the risk the employee is describing and two strategies to mitigate vendor lock-in.",
                "answer": "The employee is describing vendor lock-in -- the risk that once data and workflows are tied to one cloud provider, it becomes difficult and expensive to switch. If the provider raises prices, experiences an outage, or shuts down, the company has limited ability to migrate quickly. Mitigation strategy 1 -- Multi-cloud: replicate or back up data to a second cloud provider (e.g., store primary data on Azure but maintain a backup copy on AWS S3). If one provider fails, the other has the data. Migration strategy 2 -- Use open standards: store data in standard formats (CSV, PDF, JPEG) rather than proprietary formats that only work with one vendor. Ensure the application supports data export at any time, so switching providers does not require reformatting data.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-3.6": {
        "unit": "tp-3.6",
        "title": "Interfaces",
        "n10_009": "FC0-U71 3.6",
        "n10_008": "FC0-U71 3.6",
        "questions": [
            {
                "num": "1",
                "question": "A GUI (Graphical User Interface) allows users to interact with a computer using _______, _______, and _______ rather than typed commands. Users point and click with a _______ to open files and launch programs. Windows, macOS, and most mobile OSes use a GUI by default.",
                "answer": "Icons, windows, menus; mouse (pointer).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "A CLI (Command Line Interface) requires users to type _______ as text. The CLI on Windows is _______ (cmd.exe) or _______. On Linux and macOS it is the _______. The CLI is preferred by administrators for _______, as commands can be scripted and repeated across many systems.",
                "answer": "Commands; Command Prompt; PowerShell; terminal (bash/shell); automation.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "A NUI (Natural User Interface) uses _______, _______, or _______ as input rather than a mouse or keyboard. Voice assistants like _______ and _______ are examples of voice-based NUIs. Gesture-based NUIs are used in gaming (Microsoft _______) and surgical robotics.",
                "answer": "Touch, voice, gestures; Siri, Alexa (or Google Assistant); Kinect.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "A touchscreen interface accepts input directly from _______ or a _______ on the screen surface. Capacitive touchscreens detect the electrical conductivity of a human _______ and are used in smartphones. Resistive touchscreens respond to _______ and can be used with a stylus or gloved hand.",
                "answer": "Fingers; stylus; finger; pressure.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "A menu-driven interface presents users with a list of _______ to choose from. This is more accessible to _______ users but less flexible than a CLI. Examples include ATM screens, kiosk check-in systems, and _______ (basic menus found in the router or BIOS configuration screen).",
                "answer": "Options (choices); non-technical; BIOS/UEFI setup.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Accessibility features in operating systems are _______ adaptations that make computers usable for people with disabilities. Examples include _______ (reads screen content aloud for visually impaired users), _______ (enlarges text and interface elements), and _______ (allows keyboard control via an on-screen keyboard for users who cannot use a physical keyboard).",
                "answer": "Interface; screen reader (narrator); magnifier; on-screen keyboard (sticky keys / filter keys).",
                "lines": 3
            },
            {
                "num": "7",
                "question": "UI vs UX: _______ (User Interface) refers to the visual elements a user interacts with -- buttons, icons, layout, colors. _______ (User Experience) refers to the overall feeling and ease a user has while completing a task. A UI can look visually appealing but have poor _______ if it is confusing or inefficient to use.",
                "answer": "UI; UX; UX.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A government agency is deploying a self-service kiosk for citizens to register for public services. The kiosk will be used by elderly citizens, people with low digital literacy, and individuals who are visually impaired. Describe three specific interface design features you would include to make the kiosk accessible and usable for all these groups.",
                "answer": "Feature 1 -- Large text and high contrast: use minimum 18pt font and high contrast colors (e.g., black text on white background) for users with low vision or difficulty reading small text. Feature 2 -- Simplified menu-driven navigation: use large clearly labeled buttons with simple language (e.g., Register for Benefits) and a maximum of 3-4 choices per screen, avoiding jargon. This helps low-digital-literacy users complete tasks without needing technical knowledge. Feature 3 -- Screen reader / audio output: include a headphone jack and screen reader mode triggered by a physical button, so visually impaired users can hear each menu option read aloud. Also add tactile buttons or Braille labels for key actions. Feature 4 (bonus) -- Adjustable interface height or touch angle to accommodate wheelchair users.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-3.7": {
        "unit": "tp-3.7",
        "title": "Programming Languages",
        "n10_009": "FC0-U71 3.7",
        "n10_008": "FC0-U71 3.7",
        "questions": [
            {
                "num": "1",
                "question": "A programming language is a formal language used to write _______ that computers can execute. Source code is written in _______ -readable text, then converted to machine code. The two main conversion methods are _______ (converts all code at once before running) and _______ (converts and runs line by line).",
                "answer": "Instructions (programs); human; compilation; interpretation.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "_______ code (binary machine instructions) is what the CPU executes directly. _______ language uses mnemonics (like MOV, ADD) to represent machine instructions. High-level languages like Python and Java are _______ readable and must be compiled or interpreted before the CPU can run them.",
                "answer": "Machine; assembly; human.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Python is an _______ language known for readable syntax and use in data science, automation, and web development. Java is a _______ language that compiles to bytecode run on the _______ (JVM), enabling write-once run-anywhere portability. JavaScript runs primarily in _______ to make web pages interactive.",
                "answer": "Interpreted; compiled; Java Virtual Machine; browsers.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "C and C++ are _______ -level languages often used for _______ programming, game engines, and performance-critical applications. They give programmers direct access to _______ management, which increases performance but also increases the risk of _______ vulnerabilities like buffer overflows.",
                "answer": "Low (systems); systems-level; memory; security.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "SQL (Structured Query Language) is used to _______ and _______ data in relational databases. HTML (Hypertext Markup Language) defines the _______ of web pages. CSS (Cascading Style Sheets) defines the _______ (colors, fonts, layout). Neither HTML nor CSS is technically a _______ language -- they are markup/styling languages.",
                "answer": "Query; manage (create, update, delete); structure (content); appearance; programming.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "A scripting language (Python, Bash, PowerShell) is typically _______ and used for _______ tasks. A PowerShell script can automate _______ administrative tasks like creating user accounts. A Bash script on Linux can automate _______ and file operations. Scripts reduce _______ compared to doing tasks manually.",
                "answer": "Interpreted; automation; Windows; backups; time/effort.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "An IDE (Integrated Development Environment) combines a _______ editor, _______ (finds syntax errors), _______ (automates build/run), and _______ (steps through code to find logical errors) into one tool. Popular IDEs include Visual Studio Code, PyCharm, and _______.",
                "answer": "Code; linter; build tool; debugger; IntelliJ (or Eclipse).",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A student wants to build a personal website, create some scripts to automate their homework file organization, and eventually get into data analysis. They ask you which programming language they should learn first. Recommend one language, give three reasons it is the best starting point for their goals, and name one limitation.",
                "answer": "Recommendation: Python. Reason 1 -- Beginner-friendly syntax: Python reads like plain English, uses indentation instead of excessive punctuation, and has gentle error messages. It is the most commonly taught first language in universities and bootcamps. Reason 2 -- Covers three of their goals directly: Python can build web apps (Flask, Django), write automation scripts (file management, renaming, sorting), and is the dominant language in data analysis (pandas, NumPy, matplotlib). Reason 3 -- Huge community and library ecosystem: beginner stuck on any problem can find dozens of tutorials. Limitation: Python is interpreted and not the best choice for performance-critical applications or front-end web interactivity -- for the actual website UI they will also need to learn some HTML/CSS and possibly JavaScript.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-3.8": {
        "unit": "tp-3.8",
        "title": "Logic and Algorithms",
        "n10_009": "FC0-U71 3.8",
        "n10_008": "FC0-U71 3.8",
        "questions": [
            {
                "num": "1",
                "question": "An _______ is a step-by-step set of instructions for solving a problem or completing a task. Every computer program is built on _______. Key properties of a good algorithm are that it must be _______ (has a definite end), produces the _______ output for the same input, and is _______.",
                "answer": "Algorithm; algorithms; finite; correct (same); unambiguous.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "The three fundamental control structures in programming are: _______ (executes instructions one after another), _______ (chooses between paths based on a condition), and _______ (repeats a block of code while or until a condition is met).",
                "answer": "Sequence; selection (if/else); iteration (loops).",
                "lines": 3
            },
            {
                "num": "3",
                "question": "A Boolean expression evaluates to either _______ or _______. Boolean operators include _______ (both conditions must be true), _______ (at least one condition must be true), and _______ (reverses the truth value). These are the building blocks of all _______ statements in code.",
                "answer": "True; false; AND; OR; NOT; conditional (if/else).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "A _______ loop runs code a fixed number of times or over each item in a list. A _______ loop runs as long as a condition is true -- if the condition never becomes false, a _______ loop occurs. A _______ loop always runs at least once before checking the condition.",
                "answer": "For; while; infinite; do-while.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "A _______ is a named block of reusable code that performs a specific task. Functions accept _______ as input values and may _______ an output value. Using functions reduces _______ (writing the same code repeatedly) and makes programs easier to test and _______.",
                "answer": "Function (subroutine/procedure); parameters; return; redundancy (duplication); maintain.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Pseudocode is an _______ description of an algorithm using plain language rather than a specific programming language. A _______ chart visually represents the flow of an algorithm using standard symbols: rectangles for _______, diamonds for _______, and parallelograms for input/output.",
                "answer": "Informal; flowchart; processes (actions); decisions.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "A sorting algorithm arranges a list of items in a specific _______ (ascending or descending). Bubble sort repeatedly _______ adjacent items if they are in the wrong order -- it is simple but _______ for large data sets. Quick sort and merge sort are far more _______ for large datasets.",
                "answer": "Order; swaps (compares); slow (inefficient); efficient.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A student is writing a program that reads a user's grade (0-100) and prints a letter grade (A, B, C, D, or F). Write the logic in pseudocode using if/else selection statements to determine the correct letter grade. Use standard letter grade ranges (A = 90-100, B = 80-89, C = 70-79, D = 60-69, F = 0-59).",
                "answer": "INPUT grade\nIF grade >= 90 THEN\n    PRINT 'A'\nELSE IF grade >= 80 THEN\n    PRINT 'B'\nELSE IF grade >= 70 THEN\n    PRINT 'C'\nELSE IF grade >= 60 THEN\n    PRINT 'D'\nELSE\n    PRINT 'F'\nEND IF\n\nKey points: conditions are checked from highest to lowest so each threshold only needs a single comparison. If checked lowest-first, every grade >=60 would hit the D branch before reaching A/B/C.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-3.9": {
        "unit": "tp-3.9",
        "title": "Programming Concepts",
        "n10_009": "FC0-U71 3.9",
        "n10_008": "FC0-U71 3.9",
        "questions": [
            {
                "num": "1",
                "question": "A _______ stores a single value that can change during program execution. A _______ stores a value that does not change. A _______ is a named location that holds one value at a time. A _______ (like a list/array) can hold multiple values under one name.",
                "answer": "Variable; constant; variable; data structure (array/list).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Data types define what kind of data a variable holds. Common types: _______ (whole numbers), _______ (decimal numbers), _______ (text), _______ (True/False). Assigning a value of the wrong type to a variable can cause a _______ error.",
                "answer": "Integer (int); float (floating-point); string (str); boolean (bool); type (runtime).",
                "lines": 3
            },
            {
                "num": "3",
                "question": "OOP (Object-Oriented Programming) models software around _______ that combine data (_______ ) and behavior (_______). A _______ is a blueprint; an _______ is a specific object created from that blueprint. OOP supports _______ (hiding internal details) and _______ (child classes inherit from parent).",
                "answer": "Objects; attributes (properties); methods (functions); class; object (instance); encapsulation; inheritance.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "A syntax error is a violation of the _______ rules of a programming language and is caught at _______ time. A logic error is a bug where the code runs without crashing but produces the _______ output. A runtime error occurs while the program _______ and causes it to _______ unexpectedly.",
                "answer": "Grammar (syntax); compile/parse; wrong; runs; crash.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Version control (like Git) tracks _______ to source code over time. A _______ is a saved version of the codebase. _______ allows developers to create an isolated copy of the code to work on a feature without affecting the main codebase. _______ combines changes from two branches.",
                "answer": "Changes (edits); commit; branching; merging.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "An API (Application Programming Interface) defines how two software components can _______ with each other. When a weather app on your phone displays today's forecast, it is likely calling a weather service _______ to get the data. APIs use _______ requests over HTTP to send and receive _______ (typically JSON or XML format) data.",
                "answer": "Communicate; API; HTTP (GET/POST); structured.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Testing ensures software functions as expected. _______ testing checks individual functions in isolation. _______ testing checks how multiple components work together. _______ testing verifies the complete system meets requirements from the user's perspective. _______ testing ensures that new changes do not break existing functionality.",
                "answer": "Unit; integration; end-to-end (system/user acceptance); regression.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A student writes a program to calculate the area of a rectangle. They test it and it runs without errors, but the area value it prints is always wrong. Identify what type of error this is, explain why it does not show up as a crash, and describe how the student should debug it.",
                "answer": "This is a logic error -- the code is syntactically correct (no grammar violations) and does not crash (no runtime exception), but it produces incorrect output. Logic errors are the most difficult to catch because the program appears to work. Debugging approach: (1) Print intermediate values at each step to trace what the program is actually calculating. For example, print the length and width values before the calculation to verify they are being read correctly. (2) Manually work through the formula and compare to the program output -- check the formula itself (is area = length x width, or did they accidentally use length + width?). (3) Check operator precedence if complex expressions are involved. (4) Use an IDE debugger to step through the code line by line and inspect variable values at each step.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-3.10": {
        "unit": "tp-3.10",
        "title": "Web Development Concepts",
        "n10_009": "FC0-U71 3.10",
        "n10_008": "FC0-U71 3.10",
        "questions": [
            {
                "num": "1",
                "question": "HTML stands for _______ and defines the _______ (content and organization) of a web page. CSS stands for _______ and defines the _______ (colors, fonts, layout). JavaScript adds _______ to the page, making it respond to user actions without reloading.",
                "answer": "HyperText Markup Language; structure; Cascading Style Sheets; appearance (style); interactivity (behavior).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "HTTP (HyperText Transfer Protocol) is the protocol used to request and serve _______ over the web. HTTPS is the secure version that _______ traffic using TLS. HTTP uses port _______ and HTTPS uses port _______. Browsers display a _______ icon in the address bar for HTTPS sites.",
                "answer": "Web pages; encrypts; 80; 443; padlock.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "DNS (Domain Name System) translates human-readable _______ (like www.google.com) into _______ addresses that computers use to locate servers. Without DNS, users would need to type _______ addresses directly to reach websites. A DNS _______ attack replaces a legitimate IP with a fraudulent one to redirect users.",
                "answer": "Domain names; IP; IP; poisoning (spoofing).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "_______ side processing runs on the web server (PHP, Python, Node.js) and sends the finished HTML page to the client. _______ side processing runs in the user's browser (JavaScript) and modifies the page without contacting the server. Modern web apps use both: the server delivers _______ and the client updates the _______ dynamically.",
                "answer": "Server; client; initial HTML; DOM (page content).",
                "lines": 3
            },
            {
                "num": "5",
                "question": "A _______ is a pre-built set of code libraries and tools that provides a structure for building web applications. Front-end frameworks include _______ and _______. Back-end frameworks include Django (Python) and _______. Using a framework reduces _______ by providing solved solutions for common tasks.",
                "answer": "Framework; React, Angular (examples); Express (Node.js) or Flask; development time (redundancy).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "A web browser renders HTML, CSS, and JavaScript into the visual page a user sees. The _______ (Document Object Model) is a tree structure representing the page, which JavaScript can modify. Browsers use a _______ engine to interpret JavaScript (Chrome uses V8, Firefox uses _______). Developer _______ in the browser allow inspecting HTML, CSS, and network requests.",
                "answer": "DOM; JavaScript; SpiderMonkey; tools (DevTools).",
                "lines": 3
            },
            {
                "num": "7",
                "question": "A URL (Uniform Resource Locator) has several parts. In the URL https://shop.example.com/products?id=42:\n    https is the _______\n    shop.example.com is the _______\n    /products is the _______\n    ?id=42 is the _______",
                "answer": "Protocol (scheme); domain (hostname); path; query string (parameters).",
                "lines": 4
            },
            {
                "num": "8",
                "question": "REAL WORLD: A student builds a simple website and deploys it using only HTTP (not HTTPS). The site includes a login form where users submit their username and password. A cybersecurity teacher tells them this is dangerous. Explain why HTTP is dangerous for a login form compared to HTTPS, and describe what would happen if an attacker intercepted the traffic.",
                "answer": "With HTTP, all data transmitted between the browser and web server is sent in plain text -- it is not encrypted. If an attacker is on the same network (e.g., cafeteria Wi-Fi) and runs a packet capture tool like Wireshark, they can see every byte of the HTTP traffic. When a user submits the login form, the username and password are transmitted as readable text in the HTTP POST request. The attacker reads the credentials directly from the captured packet. With HTTPS (TLS), the connection is encrypted with a certificate. Even if the attacker captures the packets, all they see is encrypted ciphertext -- they cannot read the credentials without the private key. The fix is to install a TLS certificate (free options: Let's Encrypt) and configure the server to redirect all HTTP requests to HTTPS.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    # DOMAIN 4 -- Software Development Concepts
    "tp-4.1": {
        "unit": "tp-4.1",
        "title": "Software Development Life Cycle",
        "n10_009": "FC0-U71 4.1",
        "n10_008": "FC0-U71 4.1",
        "questions": [
            {
                "num": "1",
                "question": "The SDLC (Software Development Life Cycle) is a structured process for planning, creating, and maintaining software. The six main phases are: _______, _______, _______, _______, _______, and _______.",
                "answer": "Planning, requirements analysis, design, development (coding), testing, deployment (and maintenance).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "In the _______ phase, stakeholders define what the software must do. These are captured as functional requirements (what it _______ ) and non-functional requirements (how well it _______, such as performance and security). Unclear requirements at this stage lead to _______ later.",
                "answer": "Requirements analysis; does; performs; rework (costly changes).",
                "lines": 3
            },
            {
                "num": "3",
                "question": "In the _______ phase, developers write code based on the design documents. Code is typically managed in a _______ control system like Git. After coding, the _______ phase verifies the software meets requirements and finds defects before release.",
                "answer": "Development (implementation); version (source); testing (QA).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "The Waterfall model is _______ -- each phase must fully complete before the next begins. It works well when requirements are _______ and unlikely to change. The main risk is that mistakes discovered _______ in the process are very expensive to fix.",
                "answer": "Sequential (linear); stable (well-defined); late.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Agile is an iterative SDLC methodology where work is done in short cycles called _______. At the end of each cycle, a working _______ is delivered and requirements can be _______. Agile prioritizes collaboration with _______ over rigid planning.",
                "answer": "Sprints (iterations); product increment; adjusted (changed); customers (stakeholders).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "DevOps combines _______ and _______ teams to automate and integrate the build, test, and deployment pipeline. CI/CD stands for _______ and _______. With CI, every code commit triggers _______ automated tests to catch bugs immediately.",
                "answer": "Development; operations; Continuous Integration; Continuous Delivery/Deployment; automated.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Version control (source control) allows developers to track _______ over time. A _______ is a parallel line of development used to add a feature or fix a bug without disturbing the main code. After testing, the branch is _______ back into the main codebase. Git is the most widely used _______ version control system.",
                "answer": "Changes; branch; merged; distributed.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A startup uses Waterfall to build their mobile app over 18 months. At the end of development, they discover that users want a completely different onboarding flow than what was designed at the start. All the code must be rewritten. What SDLC methodology would have prevented this and why?",
                "answer": "Agile would have prevented this. In Agile, the team works in short sprints (2-4 weeks) and delivers a working increment at the end of each sprint. The onboarding flow would have been designed, coded, and shown to real users in sprint 1 or 2. User feedback would have been collected early, when changes are cheap (a few days of work). By delivering working software frequently, Agile surfaces misaligned assumptions before 18 months of work has been invested. In Waterfall, requirements are locked in up front and feedback does not happen until the final product is delivered -- making late-stage user feedback catastrophically expensive to act on. Agile's core advantage is embracing change throughout the process rather than resisting it.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-4.2": {
        "unit": "tp-4.2",
        "title": "Application Architecture",
        "n10_009": "FC0-U71 4.2",
        "n10_008": "FC0-U71 4.2",
        "questions": [
            {
                "num": "1",
                "question": "In a _______ -tier architecture, the user interface, business logic, and data are all in one application layer. In a _______ -tier architecture, the presentation and data tiers are separated. A _______ -tier (or n-tier) architecture separates presentation, application logic, and data into distinct layers on different servers.",
                "answer": "Single (1); two (2); three (3).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "The _______ tier handles what the user sees -- HTML, CSS, JavaScript in a browser. The _______ (logic) tier processes business rules and application logic (e.g., a web server running Python or Java). The _______ tier stores persistent data in a database. Each tier communicates with the tier _______ it.",
                "answer": "Presentation; application (middle/business logic); data; adjacent to (above or below).",
                "lines": 3
            },
            {
                "num": "3",
                "question": "In a _______ architecture, all functionality is packaged in one deployable unit. It is simpler to _______ initially but becomes harder to _______ as the application grows. In a _______ architecture, the application is split into small, independently deployable services that communicate over APIs.",
                "answer": "Monolithic; develop; scale/maintain; microservices.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Serverless computing means the developer writes code (called _______) without managing servers at all. The cloud provider runs the function on demand and charges per _______. It scales _______ and costs nothing when not running. Examples include AWS _______ and Azure _______.",
                "answer": "Functions; invocation (execution); automatically; Lambda; Functions.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "A _______ load balancer distributes incoming network requests across multiple backend servers to prevent any one server from being _______ and to improve availability. If one server goes down, the load balancer _______ traffic to the remaining healthy servers.",
                "answer": "Load balancer; overloaded (overwhelmed); redirects.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "A cache is a temporary storage location that holds frequently accessed data to reduce _______ to the primary data source. A CDN (Content Delivery Network) caches _______ at edge servers geographically close to users. Redis and Memcached are examples of _______ caching software used in web backends.",
                "answer": "Requests (load); static content (images, files); in-memory.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "High availability (HA) means a system is designed to minimize _______ time. It is measured as a percentage of uptime (e.g., _______ -- 'five nines' -- means 99.999% uptime, or less than _______ minutes of downtime per year). HA is achieved through _______ (no single point of failure) and failover systems.",
                "answer": "Downtime; 99.999%; 5.26 minutes; redundancy.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A retail website runs on a single web server. On Black Friday their traffic spikes 20x and the server crashes, causing 3 hours of downtime and $200,000 in lost sales. Describe two architectural changes that would prevent this outcome and explain how each helps.",
                "answer": "Change 1 -- Add a load balancer with multiple web server instances: distribute traffic across 3-5 web servers behind a load balancer. When traffic spikes 20x, the load is spread across all servers. If one fails, the others continue serving traffic. Auto-scaling groups (available in cloud providers) can automatically add new server instances when CPU/traffic thresholds are exceeded, handling unpredictable demand spikes. Change 2 -- Use a CDN (Content Delivery Network): static assets (product images, CSS, JavaScript) represent a large portion of web traffic. Moving these to a CDN means millions of requests for static files never hit the origin web server at all -- they are served from edge nodes. This dramatically reduces load on the backend during traffic spikes.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-4.3": {
        "unit": "tp-4.3",
        "title": "Testing and Quality Assurance",
        "n10_009": "FC0-U71 4.3",
        "n10_008": "FC0-U71 4.3",
        "questions": [
            {
                "num": "1",
                "question": "QA (Quality Assurance) is the process of verifying that software meets its _______ before release. A bug (defect) found in _______ is far less expensive to fix than one found in _______. The earlier a defect is found in the SDLC, the _______ it costs to fix.",
                "answer": "Requirements (specifications); testing; production; cheaper (less).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "_______ testing verifies each individual function or module works correctly in isolation. _______ testing verifies that components work correctly when combined. _______ testing verifies the complete system meets user requirements from end to end (also called acceptance testing).",
                "answer": "Unit; integration; system (end-to-end).",
                "lines": 3
            },
            {
                "num": "3",
                "question": "_______ testing is performed without knowledge of the internal code. The tester interacts with the software as a _______ would. _______ testing is performed with full knowledge of the source code. _______ (gray-box) testing is a combination of both approaches.",
                "answer": "Black-box; user; white-box; gray-box.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "_______ testing verifies the same software functions correctly across different browsers, operating systems, and hardware. _______ testing subjects the system to heavy load to find failure points. _______ testing verifies performance under expected peak conditions to ensure response times remain acceptable.",
                "answer": "Compatibility (cross-platform); stress (load); performance.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "A test case describes a specific _______, the steps to reproduce it, the _______ result, and the actual result. A bug report documents a defect including steps to _______, expected vs. actual behavior, and _______ level to help developers prioritize fixes.",
                "answer": "Scenario; expected; reproduce; severity.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "_______ testing runs automatically every time code is committed and checks that new changes do not break existing features. _______ testing involves real users testing the software in their own environment before release to validate it meets their needs. These are also called alpha and _______ testing.",
                "answer": "Regression; user acceptance testing (UAT); beta.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Security testing attempts to find _______ in the software before attackers do. _______ testing simulates attacks to find exploitable vulnerabilities. _______ analysis reviews source code for security flaws without executing it. A recently published list of the top 10 web application vulnerabilities is maintained by _______.",
                "answer": "Vulnerabilities; penetration (pen); static (SAST); OWASP.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A development team releases a new feature in their mobile banking app without running regression tests because they assumed the new code only affected the new feature. After release, customers report they can no longer log in because authentication broke. What type of testing should have caught this and describe how it works.",
                "answer": "Regression testing should have caught this before release. Regression testing re-runs the existing suite of automated test cases against the new code to verify that new changes have not broken any previously working functionality. In this case, a regression test suite covering the login/authentication flow would have automatically run after the feature code was merged. When the test run executed the login test case (enter valid credentials, expect dashboard), it would have received an unexpected error instead -- the test would fail and the CI/CD pipeline would have blocked deployment. The team would have been alerted before the code ever reached production that authentication had broken. The lesson: every code change, no matter how isolated it appears, must pass the regression suite before production deployment.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-4.4": {
        "unit": "tp-4.4",
        "title": "Version Control and Collaboration",
        "n10_009": "FC0-U71 4.4",
        "n10_008": "FC0-U71 4.4",
        "questions": [
            {
                "num": "1",
                "question": "Version control (also called source control or revision control) is a system that tracks _______ to code over time. It allows developers to _______ to any previous state, compare changes, and work _______ without overwriting each other's work.",
                "answer": "Changes (edits); revert; collaboratively.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Git is a _______ version control system, meaning every developer has a _______ copy of the full repository history. SVN is a _______ version control system, meaning there is one central server. With Git, developers can _______ without internet access and sync later.",
                "answer": "Distributed; complete (local); centralized; commit (work).",
                "lines": 3
            },
            {
                "num": "3",
                "question": "A _______ is a snapshot of the repository at a point in time. When a developer saves changes, they create a commit with a _______ describing what changed. A _______ is a pointer to a specific commit and typically named for the development stream (e.g., main, develop, feature-login).",
                "answer": "Commit; message; branch.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "A _______ request (also called a merge request) is a formal proposal to merge code from one branch into another. It triggers a _______ review where team members inspect the code before it is merged. This process catches bugs and enforces _______ standards before defects reach the main branch.",
                "answer": "Pull; code; quality (coding).",
                "lines": 3
            },
            {
                "num": "5",
                "question": "A merge conflict occurs when two developers have edited the _______ lines of the same file in different branches. Git cannot automatically decide which version is correct, so it _______ the conflict and asks the developer to _______ resolve it. Frequent small commits reduce the severity of merge _______.",
                "answer": "Same; flags (marks); manually; conflicts.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "GitHub, GitLab, and Bitbucket are _______ platforms that host Git repositories. They add features like _______ (tracks bugs and feature requests), _______ (automated testing pipelines), and team _______ (permissions, branch protection rules) on top of core Git.",
                "answer": "Cloud-based; issue tracking; CI/CD pipelines; management.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "A .gitignore file tells Git to _______ tracking specific files or directories. Common entries include _______ (compiled output), _______ (local environment configs with secrets), and _______ (IDE configuration directories). Committing secrets to a public repo is a major _______ risk.",
                "answer": "Stop (ignore); build/dist folders; .env files; .idea / .vscode; security.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A student accidentally commits their database password directly into their public GitHub repository in a config file. They realize it within 10 minutes and delete the file from the repo. Explain why deleting the file is NOT sufficient to protect the secret and what they must do to remediate the situation.",
                "answer": "Deleting the file is not sufficient because Git stores the entire history of every commit. Even after deletion, the password is still present in the commit history and anyone who cloned or browsed the repository before or after the deletion can access it via git log, git show, or by viewing earlier commits on GitHub. Additionally, automated bots scan GitHub continuously for newly pushed secrets and can capture them within seconds of a push -- the 10-minute window may have already been too late. Remediation: (1) Immediately invalidate (rotate) the compromised database password -- change it in the database right now, regardless of whether exposure is confirmed. The old credential must be treated as compromised. (2) Remove the secret from all git history using git filter-branch or the BFG Repo Cleaner tool, then force-push the cleaned history. (3) Going forward, never commit secrets -- use environment variables, .env files (added to .gitignore), or a secrets manager.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-4.5": {
        "unit": "tp-4.5",
        "title": "Databases",
        "n10_009": "FC0-U71 4.5",
        "n10_008": "FC0-U71 4.5",
        "questions": [
            {
                "num": "1",
                "question": "A database is an organized collection of _______ designed for efficient retrieval and manipulation. A _______ (DBMS) is software that manages the database -- examples include MySQL, PostgreSQL, and Microsoft SQL Server. Users interact with the DBMS using _______ (Structured Query Language).",
                "answer": "Data; DBMS (Database Management System); SQL.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "In a relational database, data is stored in _______ (rows and columns). Each row is called a _______ and each column is called a _______. A _______ key is a column whose value uniquely identifies each row. A _______ key in one table references the primary key of another table.",
                "answer": "Tables; record (row); field (column/attribute); primary; foreign.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "The four basic database operations are described by the acronym _______: _______ (add new records), _______ (retrieve data), _______ (modify existing data), and _______ (remove records).",
                "answer": "CRUD; Create; Read; Update; Delete.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "A SELECT query retrieves data from a database. Write the basic SQL syntax to retrieve all records from a table named students:\n    _______ * _______ students;\nTo retrieve only students with grade = 'A', add a _______ clause:\n    _______ * FROM students _______ grade = 'A';",
                "answer": "SELECT * FROM students; WHERE; SELECT * FROM students WHERE grade = 'A';",
                "lines": 4
            },
            {
                "num": "5",
                "question": "Database normalization reduces _______ (storing the same data in multiple places) by organizing tables so that each piece of data is stored _______ once. First normal form (1NF) requires that each column holds _______ values. Normalization improves _______ consistency and reduces the chance of update anomalies.",
                "answer": "Redundancy (duplication); only; atomic (single, indivisible); data.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "A NoSQL database stores data in formats other than tables, such as _______ (MongoDB), _______ (Redis), _______ (Apache Cassandra), or _______ (Neo4j). NoSQL databases are often preferred when data is _______ -structured, requires horizontal scaling, or schema changes frequently.",
                "answer": "Documents (JSON); key-value pairs; wide-column; graphs; unstructured (semi).",
                "lines": 3
            },
            {
                "num": "7",
                "question": "SQL Injection is a security attack where an attacker inserts malicious _______ into an input field that is then executed by the database. For example, entering ' OR '1'='1 into a login form might bypass authentication. The primary defense is using _______ statements (also called parameterized queries) which treat user input as _______ rather than executable code.",
                "answer": "SQL code; prepared; data.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A student builds a web application where users can search for products by name. The search box directly inserts the user's input into a SQL query like: SELECT * FROM products WHERE name = '[input]'. Explain the SQL injection vulnerability, show an example attack, and describe the fix.",
                "answer": "Vulnerability: the user input is concatenated directly into the SQL string without sanitization. The database executes whatever text is embedded in the query. Attack example: if the attacker enters '; DROP TABLE products;-- in the search box, the resulting SQL becomes: SELECT * FROM products WHERE name = ''; DROP TABLE products;--'. The semicolon ends the SELECT and the DROP TABLE runs as a second query, deleting all product data. Fix: use parameterized queries (prepared statements). The query becomes: SELECT * FROM products WHERE name = ? and the input value is passed separately as a parameter. The database driver treats the input as a data value -- never as executable SQL code -- so even if the attacker types DROP TABLE, it is treated as a literal search string, not a command.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-4.6": {
        "unit": "tp-4.6",
        "title": "Artificial Intelligence Concepts",
        "n10_009": "FC0-U71 4.6",
        "n10_008": "FC0-U71 4.6",
        "questions": [
            {
                "num": "1",
                "question": "AI (Artificial Intelligence) refers to computer systems designed to perform tasks that normally require human _______, such as recognizing speech, identifying images, and making decisions. _______ Learning is a subset of AI where systems learn from _______ without being explicitly programmed for each task.",
                "answer": "Intelligence; machine; data.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "In _______ learning, the training data includes labeled examples -- the model learns from input-output pairs. In _______ learning, the model finds patterns in unlabeled data with no predefined answers. _______ learning trains an agent to take actions in an environment to maximize a reward signal.",
                "answer": "Supervised; unsupervised; reinforcement.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "A _______ neural network is designed to recognize patterns in image data by scanning the image in overlapping regions. It is used in facial recognition, medical imaging, and self-driving cars. _______ neural networks (RNNs) are designed for _______ data such as text and audio because they retain context from previous inputs.",
                "answer": "Convolutional (CNN); recurrent; sequential (time-series).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "A _______ model (like GPT) predicts the next word in a sequence based on billions of parameters trained on large text datasets. These are also called _______ Models (LLMs). They can generate human-like text, translate languages, write code, and answer questions. A key limitation is that they occasionally produce confident but _______ outputs, called _______.",
                "answer": "Language; Large Language; incorrect (false); hallucinations.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "_______ AI refers to systems that excel at one specific narrow task (playing chess, recognizing faces). _______ AI (AGI) would perform any intellectual task a human can -- it does not yet exist. AI _______ refers to unintended harmful outcomes when AI systems reflect biases present in _______ data.",
                "answer": "Narrow; artificial general; bias; training.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "AI _______ is the ability to explain why an AI model made a specific decision. This is important in high-stakes domains like _______, _______, and _______ where decisions must be justifiable to affected individuals. _______ networks are often called black boxes because their decision processes are hard to interpret.",
                "answer": "Explainability (interpretability); healthcare, lending/credit, law enforcement (any two); neural.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Generative AI creates new _______ -- text, images, audio, video, or code -- based on patterns learned from training data. Tools like _______ generate images from text prompts, while _______ generates text. These tools raise ethical concerns about _______ (generating fake but realistic media) and _______.",
                "answer": "Content; DALL-E / Midjourney; ChatGPT (examples); deepfakes; copyright.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A school uses an AI tool to screen student applications and rank them. A student advocacy group finds that the model rejects more applications from students at lower-income zip codes, even when their grades are equal to students from higher-income zip codes. Explain what AI problem is occurring and recommend two steps the school should take.",
                "answer": "The problem is AI bias -- specifically training data bias. If the model was trained on historical admissions data that reflected socioeconomic inequality (e.g., the school historically admitted more students from wealthy zip codes), the model has learned to replicate that discrimination. It has encoded historical bias as a pattern to follow, not a mistake to correct. Step 1 -- Audit the model for disparate impact: analyze the model decisions disaggregated by demographic groups (income, zip code, race). If acceptance rates differ significantly for equally qualified students from different groups, the model is discriminating. Use statistical tests to quantify the disparity. Step 2 -- Mitigate bias and add human oversight: retrain the model with bias-mitigating techniques (resampling, re-weighting underrepresented groups) and exclude or carefully handle proxies for protected characteristics like zip code. Most importantly, AI should not be the final decision-maker for consequential decisions about individuals -- add mandatory human review before any rejection.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-4.7": {
        "unit": "tp-4.7",
        "title": "Emerging Technologies",
        "n10_009": "FC0-U71 4.7",
        "n10_008": "FC0-U71 4.7",
        "questions": [
            {
                "num": "1",
                "question": "Augmented Reality (AR) _______ digital content onto the real world (visible through a phone camera or AR glasses). Virtual Reality (VR) creates a fully _______ digital environment that replaces the physical world. Mixed Reality (MR) allows digital objects to interact with _______ world objects.",
                "answer": "Overlays; immersive; real.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Blockchain is a _______ -distributed ledger that records transactions across multiple nodes. Each block contains a _______ of the previous block, creating a chain that makes tampering _______ to detect. It is the underlying technology for _______ currencies like Bitcoin and Ethereum.",
                "answer": "Decentralized; cryptographic hash; easy; cryptocurrency.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Quantum computing uses _______ (quantum bits) that can exist as 0, 1, or both simultaneously (superposition). This allows quantum computers to evaluate _______ exponentially more solutions at once than classical computers. A sufficiently powerful quantum computer could break current _______ encryption (RSA/ECC), requiring _______ -resistant algorithms.",
                "answer": "Qubits; many; public-key; quantum (post-quantum).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "5G is the 5th generation cellular standard. Compared to 4G LTE, 5G offers _______ speeds, _______ latency, and supports far more _______ devices simultaneously. Use cases include smart city infrastructure, autonomous vehicles, and _______ (remote robotic surgery). 5G mmWave offers highest speeds but limited _______ penetration.",
                "answer": "Higher; lower; connected; telemedicine; building (indoor).",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Edge computing moves processing closer to where data is _______, reducing _______ and bandwidth usage. It complements rather than replaces cloud computing. Industrial IoT sensors, self-driving cars, and smart factories use edge processing because they cannot tolerate the _______ ms round-trip delay to a remote cloud server for real-time decisions.",
                "answer": "Generated; latency; 100+.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "3D printing (additive manufacturing) builds _______ objects layer by layer from a digital _______ (STL file). It enables rapid _______ (quick physical models of designs), customized medical implants, and on-demand part replacement. The two main materials are _______ (plastic filament, FDM) and _______ (photopolymer, resin).",
                "answer": "Physical; model/file; prototyping; FDM plastic; resin (SLA).",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Automation replaces repetitive human tasks with machines or software. _______ Process Automation (RPA) uses software robots to automate rule-based digital tasks like data entry. _______ automation uses physical robots for repetitive factory tasks. The societal concern is _______ displacement -- jobs replaced without equivalent new jobs being created.",
                "answer": "Robotic; industrial; workforce.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A small manufacturing company is considering adopting robotics to automate their assembly line. Currently 12 workers perform repetitive welding and packaging tasks. A manager argues the robots will pay for themselves in 3 years and improve product consistency. A workers representative argues it will harm the employees. Describe two legitimate benefits and two legitimate concerns, then suggest one way the company could balance both interests.",
                "answer": "Benefits: (1) Productivity and consistency -- robots work 24/7 without fatigue, producing more consistent output quality and higher throughput. (2) Return on investment -- after the break-even point, labor cost savings are significant and ongoing; production quality improvements reduce defect waste. Concerns: (1) Job displacement -- 12 employees lose income; in regions with few alternative jobs this causes real hardship for families. (2) Concentration of gains -- productivity gains go to owners; workers bear the cost. Balancing approach: commit to retraining employees for roles that cannot be automated (robot maintenance, quality control, programming) and offer transition support. Some companies fund retraining programs and give displaced workers first priority for new technical roles created by the automation. This is not perfect but distributes the benefit more equitably.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    # DOMAIN 5 -- Data and Database Fundamentals
    "tp-5.1": {
        "unit": "tp-5.1",
        "title": "Data Classification",
        "n10_009": "FC0-U71 5.1",
        "n10_008": "FC0-U71 5.1",
        "questions": [
            {
                "num": "1",
                "question": "Data classification is the process of organizing data into categories based on its _______ and the level of _______ required. Organizations classify data to apply _______ controls -- not all data needs the same protection, and over-protecting low-sensitivity data wastes resources.",
                "answer": "Sensitivity (value); protection; appropriate security.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Common civilian data classification levels from lowest to highest sensitivity are: _______ (available to the public), _______ (internal use only, not for external distribution), _______ (limited to authorized staff), and _______ (highest risk if disclosed, limited to need-to-know individuals).",
                "answer": "Public; internal (private); confidential; restricted (top secret / highly restricted).",
                "lines": 3
            },
            {
                "num": "3",
                "question": "PII (Personally Identifiable Information) is data that can identify a _______ individual. Examples include _______, _______, _______, and _______ (name at least four). Regulations like _______ (US healthcare) and _______ (EU privacy) require specific handling of PII.",
                "answer": "Specific; name, Social Security Number, email address, phone number, address, DOB (any four); HIPAA; GDPR.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "PHI (Protected Health Information) is a specific subset of PII relating to a person's _______ condition, treatment, or payment for care. It is protected by _______ in the United States. Organizations that handle PHI (hospitals, insurers, labs) are called _______ entities and must follow strict safeguards.",
                "answer": "Health (medical); HIPAA; covered.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "The principle of _______ requires that individuals and systems only have access to the data they need for their specific job function -- no more. A marketing employee should not have access to _______ records. A help desk technician does not need access to the company's _______ source code repository.",
                "answer": "Least privilege; financial (payroll); proprietary (development).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Data _______ marks files with their classification level so access control policies can be enforced automatically. _______ prevents sensitive data from leaving an organization via email, USB, or cloud upload by monitoring and blocking classified content. This technology is called _______ (Data Loss Prevention).",
                "answer": "Labeling (tagging); technology; DLP.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Structured data is organized in a defined format that can be easily _______ (e.g., database tables, spreadsheets). Unstructured data has no predefined format -- examples include _______, _______, and _______. Semi-structured data has some organizational properties but does not fit a relational model -- _______ and XML are examples.",
                "answer": "Searched/queried; emails, images, videos (any two); JSON.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A hospital employee accidentally emails a spreadsheet containing 500 patients social security numbers and diagnoses to an external vendor. Identify the regulatory framework violated, classify the data by type (PII/PHI), and describe two technical controls that could have prevented this from happening.",
                "answer": "Regulatory violation: HIPAA (Health Insurance Portability and Accountability Act). The data contains both PII (SSNs, which identify individuals) and PHI (diagnoses combined with identity -- patient health information). HIPAA requires covered entities to protect PHI and report breaches affecting 500 or more individuals to HHS and the media. Technical control 1 -- DLP (Data Loss Prevention): a DLP system scans outbound emails for patterns matching SSN formats and PHI keywords (e.g., ICD codes, diagnosis terms). It would automatically block the email and alert the security team before delivery. Technical control 2 -- Data classification and access controls: implement role-based access so clinical staff data exports require authorization and SSN columns are masked or removed for non-clinical workflow exports. The vendor may only need aggregate statistics, not individual identifiers.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-5.2": {
        "unit": "tp-5.2",
        "title": "File Systems and Storage",
        "n10_009": "FC0-U71 5.2",
        "n10_008": "FC0-U71 5.2",
        "questions": [
            {
                "num": "1",
                "question": "A file system organizes how data is _______, named, and accessed on a storage device. Without a file system, a drive is just a _______ series of bytes. Common Windows file systems include _______ (legacy FAT) and _______ (modern, supports large files and permissions). Linux commonly uses _______.",
                "answer": "Stored; raw (undifferentiated); FAT32 (exFAT); NTFS; ext4.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "FAT32 has a maximum single file size of _______ GB. NTFS supports files up to _______ TB theoretically. exFAT was designed for _______ drives and supports large files without the 4 GB FAT32 limit. NTFS supports features FAT32 lacks: _______ (file permissions), _______ (access logs), and file-level encryption.",
                "answer": "4 GB; 16 TB+; flash (USB/SD); permissions; auditing.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "A _______ is the directory hierarchy root from which all files are organized. On Windows, drive letters like _______ are the root for each volume. On Linux and macOS the entire filesystem has a single root called _______. Linux uses _______ as the path separator; Windows uses _______.",
                "answer": "Root; C:\\ (or D:\\); / (forward slash); /; \\ (backslash).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "A file _______ (like .txt, .docx, .exe) tells the OS what type of data the file contains and which program to open it with. Extensions are not embedded in the data -- they are just part of the _______ and can be changed. On Windows, the _______ of a file is stored in NTFS metadata, not in the extension.",
                "answer": "Extension; filename; file type (MIME type).",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Compression reduces _______ size by encoding repeated patterns more efficiently. _______ compression (ZIP, gzip) reduces size without losing data and can be restored to the original. _______ compression (JPEG, MP3) permanently discards data to achieve greater size reduction. Lossy compression is acceptable for _______ where small quality loss is imperceptible.",
                "answer": "File; lossless; lossy; multimedia (images/audio).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Encryption converts file data into _______ text that cannot be read without the _______ key. BitLocker (Windows) and FileVault (macOS) are full-disk _______ solutions that encrypt the entire drive. If the drive is lost or stolen, the data cannot be read without the _______ key or recovery code.",
                "answer": "Cipher; decryption; encryption; encryption (BitLocker).",
                "lines": 3
            },
            {
                "num": "7",
                "question": "A _______ is a file or folder shortcut (symbolic link on Linux/macOS, or shortcut .lnk on Windows) that points to another location without copying the data. Deleting the shortcut does not delete the _______ file. On Linux, a _______ link is a direct pointer (inode reference) to the same data, so deleting one does not delete the other as long as another link exists.",
                "answer": "Link (shortcut); original; hard.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A student copies a 5 GB video file from their laptop to a FAT32 USB drive and receives an error saying the file is too large even though the drive has 16 GB of free space. Explain why this error occurs and describe two ways to solve it.",
                "answer": "FAT32 has a 4 GB per single file size limitation, regardless of how much total free space exists on the drive. The 5 GB file exceeds this limit, so the copy fails. This is an architecture limitation of the FAT32 file system -- it uses a 32-bit field to store file size, which caps at 2^32 - 1 bytes (approximately 4 GB). Solution 1 -- Reformat the USB drive to exFAT: exFAT was designed for flash drives and supports files much larger than 4 GB with no practical limit. The drive should be reformatted to exFAT (Windows: right-click drive > Format > exFAT). Note: reformatting erases all data. Solution 2 -- Split the video into parts smaller than 4 GB using a video splitter tool, copy both parts to the FAT32 drive, then reassemble on the destination computer. This is a workaround that keeps the FAT32 format if the destination device requires it.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-5.3": {
        "unit": "tp-5.3",
        "title": "Data Analytics",
        "n10_009": "FC0-U71 5.3",
        "n10_008": "FC0-U71 5.3",
        "questions": [
            {
                "num": "1",
                "question": "Data analytics is the process of examining _______ to discover useful information and support decision-making. The four types of analytics in order of complexity are: _______ (what happened), _______ (why it happened), _______ (what will happen), and _______ (what should we do about it).",
                "answer": "Data (datasets); descriptive; diagnostic; predictive; prescriptive.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "The _______ is the central repository that aggregates data from multiple sources for reporting and analysis. Unlike an operational database (optimized for _______ transactions), a data warehouse is optimized for _______ analytical queries across large historical datasets.",
                "answer": "Data warehouse; fast read/write; complex (read-heavy).",
                "lines": 3
            },
            {
                "num": "3",
                "question": "ETL stands for _______, _______, and _______.  It is the process of moving data from source systems into a data warehouse. _______ pulls data from source systems. _______ cleans and reformats it into a consistent structure. _______ loads it into the destination.",
                "answer": "Extract, Transform, Load; Extract; Transform; Load.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Data _______ is the practice of examining large datasets to discover patterns, correlations, and anomalies. It uses techniques from statistics and machine learning. Business applications include _______ (flagging unusual transactions), _______ (anticipating what customers will buy), and _______ (finding patterns that predict equipment failure).",
                "answer": "Mining; fraud detection; recommendation engines; predictive maintenance.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "_______ is data that is too large, too fast, or too varied for traditional databases to handle. The three Vs of big data are: _______ (massive amounts), _______ (high speed of generation), and _______ (multiple formats and sources). Technologies like Hadoop and Apache Spark process big data across _______ of servers in parallel.",
                "answer": "Big data; volume; velocity; variety; clusters.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "A _______ is a visual representation of data designed to communicate patterns and insights clearly. Common chart types: _______ chart for comparing categories, _______ chart for parts of a whole, _______ chart for trends over time, and _______ plot for showing correlation between two variables.",
                "answer": "Data visualization; bar; pie; line; scatter.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "_______ are commonly used measures in data analysis. The _______ is the sum divided by the count. The _______ is the middle value when sorted. The _______ is the most frequently occurring value. The _______ is the difference between the maximum and minimum values.",
                "answer": "Descriptive statistics; mean (average); median; mode; range.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A school cafeteria wants to reduce food waste. The food services director collects 6 months of daily meal sales data. Describe which type of analytics they should use for each of the following goals: (a) understand which meals are most popular, (b) understand why Monday waste is 40% higher than other days, (c) predict how many portions of each meal to prepare next week.",
                "answer": "(a) Descriptive analytics -- analyze historical sales counts per meal item to see what was most purchased. Tools: aggregate counts, bar charts, ranking tables. This answers 'what happened.' (b) Diagnostic analytics -- drill into Monday data to find the why. Compare Monday menus vs. other days, check if Monday attendance is lower, examine if certain unpopular meals are scheduled Mondays. This answers 'why did it happen.' (c) Predictive analytics -- use historical demand patterns, day-of-week trends, and seasonal patterns (e.g., spike after school breaks) to build a forecast model that predicts portions needed per meal next week. This answers 'what will happen.' Tools might include a simple regression model in Excel or a machine learning model in Python.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-5.4": {
        "unit": "tp-5.4",
        "title": "Database Concepts",
        "n10_009": "FC0-U71 5.4",
        "n10_008": "FC0-U71 5.4",
        "questions": [
            {
                "num": "1",
                "question": "A relational database stores data in _______ with rows and columns. The relationship between tables is defined using _______ keys that reference _______ keys in other tables. This structure prevents data _______ and ensures that related data stays consistent.",
                "answer": "Tables; foreign; primary; duplication (redundancy).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "ACID properties ensure reliable database transactions. A = _______ (all steps complete or none do), C = _______ (data remains valid), I = _______ (transactions do not interfere with each other), D = _______ (once committed, data persists even after a crash).",
                "answer": "Atomicity; consistency; isolation; durability.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "A database _______ is a saved SQL query treated as a virtual table. It does not store data itself -- it runs the query dynamically. A database _______ is code stored in the database and executed on demand, allowing complex logic to run _______ to the data without round trips to the application server.",
                "answer": "View; stored procedure; close (server-side).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "An index in a database works like a book index -- it allows the DBMS to find records _______ without scanning every row. Creating an index on a frequently queried column speeds up _______ operations but slightly slows _______ and _______ operations because the index must be maintained when data changes.",
                "answer": "Faster; SELECT (read); INSERT; UPDATE/DELETE (write).",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Database _______ is the process of copying data to another location to protect against data loss. _______ backups copy all data each time. _______ backups copy only data changed since the last full backup. _______ backups copy only data changed since the last backup of any type. The _______ (Recovery Point Objective) defines the maximum acceptable data loss window.",
                "answer": "Backup; full; differential; incremental; RPO.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "A database _______ creates linked copies of the database on multiple servers for redundancy. A _______ replication model has one server that accepts writes and pushes changes to read-only _______. This improves _______ availability and _______ performance by distributing read queries.",
                "answer": "Replication; primary-replica (master-slave); replicas; high; read.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "NoSQL databases trade strict _______ consistency for horizontal _______ (spreading data across many servers). The CAP theorem states that a distributed system can guarantee only _______ of these three: Consistency, Availability, and Partition Tolerance. Most NoSQL systems choose _______ and Partition Tolerance (AP) over strong consistency.",
                "answer": "ACID; scalability (scaling); two (2); availability.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: An e-commerce website uses a single database server with no backup and no redundancy. One morning the server hard drive fails. The website is offline and all customer order history is gone. Describe three database infrastructure practices the company should implement to prevent this scenario from recurring.",
                "answer": "Practice 1 -- Automated scheduled backups: configure daily full backups and hourly incremental backups stored on a separate server or cloud storage (e.g., AWS S3). Test restores quarterly to verify backups are functional. With hourly incrementals, maximum data loss is 1 hour of orders. Practice 2 -- Primary-replica replication: configure a replica (read-only copy) on a second server that stays synchronized with the primary database in near real-time. If the primary drive fails, failover to the replica -- it has all committed transactions. Downtime is minutes rather than hours. Practice 3 -- RAID on the database server: configure RAID 1 (mirroring) or RAID 5/6 on the server so that even if one physical drive fails, the database continues operating on the remaining drives with no data loss. This protects against drive failure without any downtime.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-5.5": {
        "unit": "tp-5.5",
        "title": "Data Integrity and Validation",
        "n10_009": "FC0-U71 5.5",
        "n10_008": "FC0-U71 5.5",
        "questions": [
            {
                "num": "1",
                "question": "Data integrity means data is _______ (correct), _______ (complete), and _______ (not changed without authorization). Organizations achieve data integrity through _______ (enforcing data types and required fields), _______ (detecting unauthorized changes), and access controls.",
                "answer": "Accurate; complete; unaltered; validation; hashing (checksums).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Input validation ensures data entered into a system meets _______ criteria before being processed. Frontend validation in a browser gives _______ feedback but can be bypassed. Server-side validation is _______ because it is enforced in code the user cannot modify. Both should be used together.",
                "answer": "Expected (defined); immediate (user-friendly); more trustworthy (authoritative).",
                "lines": 3
            },
            {
                "num": "3",
                "question": "A _______ constraint in a database prevents NULL (empty) values in a column. A _______ constraint ensures all values in a column are different. A _______ constraint limits which values are permitted (e.g., grade must be A, B, C, D, or F). A _______ constraint enforces the relationship between two tables using keys.",
                "answer": "NOT NULL; UNIQUE; CHECK; foreign key (referential integrity).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "A checksum or _______ (hash) function produces a fixed-length value from input data. If even one _______ in the original data changes, the hash changes completely. This property allows detection of _______ during transmission or storage. Common hash functions include _______ and _______.",
                "answer": "Hash; bit; tampering (corruption); SHA-256, MD5 (note: MD5 is deprecated for security use).",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Data _______ is the process of ensuring data is formatted correctly for analysis (fixing errors, removing duplicates, standardizing formats). _______ data (incorrect, inconsistent, or incomplete records) leads to unreliable analysis results. The rule is: _______ in, _______ out.",
                "answer": "Cleaning (sanitization); dirty; garbage; garbage.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Referential integrity ensures that a foreign key value in one table must match a _______ key that _______ in the referenced table, or be NULL. If a parent record is deleted, the DBMS can _______ delete all child records (CASCADE), or _______ the deletion if child records exist (RESTRICT).",
                "answer": "Primary; exists; cascade; block.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Data _______ involves documenting data assets -- what data exists, where it is stored, who owns it, and its _______ level. Strong governance practices include _______ policies that specify how long data must be retained and when it must be _______. Retaining data longer than necessary increases _______ risk.",
                "answer": "Governance; classification (sensitivity); retention; destroyed (deleted); breach.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A student builds a web form that accepts a user's age as a text field. A malicious user enters 'abc' as their age, which crashes the database query. Another user enters -5 as their age, which the system accepts. Identify both problems and describe the server-side validation rules needed to fix them.",
                "answer": "Problem 1 -- Type validation failure: the input 'abc' is not a number, but the application passes it to the database query without checking. The fix is: validate that the input is a positive integer before processing. In server code: check that the value can be parsed as an integer (not a string or float) -- reject anything that fails type conversion with an error message. Problem 2 -- Range validation failure: -5 is a valid integer but an impossible age. The fix is: apply a range constraint -- age must be >= 0 and <= 120 (or whatever reasonable maximum). Return an error if the value is outside this range. Combined server-side rule: input must be a whole number AND be between 0 and 120. Reject any input that fails either check and return a clear user-facing error message. Never trust client-side validation alone -- browsers can be bypassed.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    # DOMAIN 6 -- Security
    "tp-6.1": {
        "unit": "tp-6.1",
        "title": "Confidentiality Concerns",
        "n10_009": "FC0-U71 6.1",
        "n10_008": "FC0-U71 6.1",
        "questions": [
            {
                "num": "1",
                "question": "The CIA triad stands for _______, _______, and _______. These are the three core principles of information security. _______ means that data can only be accessed by authorized individuals. _______ means data is accurate and has not been changed. _______ means systems and data are accessible when needed.",
                "answer": "Confidentiality, Integrity, Availability; Confidentiality; Integrity; Availability.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Confidentiality means preventing _______ access to information. Threats to confidentiality include _______ (stealing data over a network), _______ (tricking users into revealing credentials), and _______ (collecting discarded documents with sensitive info). The primary countermeasure for confidentiality is _______.",
                "answer": "Unauthorized; eavesdropping (sniffing); phishing; dumpster diving; encryption.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Encryption protects confidentiality by converting _______ text into _______ text using an algorithm and key. _______ encryption uses the same key to encrypt and decrypt. _______ encryption uses a public key to encrypt and a private key to decrypt. HTTPS uses _______ to secure web communications.",
                "answer": "Plain (clear); cipher; symmetric; asymmetric; TLS (SSL/TLS).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Access control protects confidentiality by restricting _______ to only what each user is authorized to see. _______ access control (MAC) uses security labels set by the system. _______ access control (DAC) lets the resource owner set permissions. _______ access control (RBAC) assigns permissions based on job role.",
                "answer": "Access; mandatory; discretionary; role-based.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Data classification helps protect confidentiality by labeling data so appropriate _______ controls are applied. Data labeled _______ or _______ should be accessible only to specific authorized individuals. Sensitive data should be _______ in transit (over networks) and _______ at rest (stored on drives).",
                "answer": "Security; confidential; restricted (top secret); encrypted; encrypted.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "A _______ (VPN) protects confidentiality over public networks by creating an encrypted _______ between the user and the organization. Without a VPN, data sent over public Wi-Fi can be intercepted by _______ attacks where an attacker positions themselves between sender and receiver.",
                "answer": "Virtual Private Network; tunnel; man-in-the-middle (MITM).",
                "lines": 3
            },
            {
                "num": "7",
                "question": "The _______ of least privilege states that users and systems should have only the minimum access required for their job. Applying this principle limits _______ damage if credentials are compromised. Over-permissioned accounts are a major source of _______ violations in real breaches.",
                "answer": "Principle; blast radius (damage); confidentiality.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A healthcare company stores patient records in an unencrypted database. A laptop belonging to an IT employee is stolen from a car. The laptop had a local copy of the database for testing. No patient data is encrypted at rest. Explain what confidentiality failure occurred and describe two controls that would have prevented data exposure.",
                "answer": "Confidentiality failure: sensitive data (PHI -- protected health information) was stored in plaintext on an endpoint (the laptop). When the physical device was stolen, the attacker gained immediate access to all patient records with no technical barrier. This is both a HIPAA violation and a confidentiality failure because unauthorized individuals (thieves) can now read the data. Control 1 -- Full disk encryption: enable BitLocker (Windows) or FileVault (macOS) on all endpoint devices. If the laptop had been encrypted, the thief cannot read any data without the decryption key -- the stolen hardware is useless for data access. Control 2 -- No production/PHI data on development endpoints: implement a policy prohibiting copying real patient data to local machines for testing. Use synthetic (fake but realistic) test data. Any exception requires approval, and data must be deleted when testing is complete. This eliminates the exposure vector entirely.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-6.2": {
        "unit": "tp-6.2",
        "title": "Integrity Concerns",
        "n10_009": "FC0-U71 6.1",
        "n10_008": "FC0-U71 6.1",
        "questions": [
            {
                "num": "1",
                "question": "Integrity in security means that data is _______, _______, and has not been _______ without authorization. An integrity violation occurs when data is modified by someone who was not _______ to make that change -- whether by an attacker, a system error, or accidental editing.",
                "answer": "Accurate; complete; altered (changed); authorized.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Hashing is the primary technical control for verifying integrity. A hash function produces a fixed-length _______ (digest) from input data. If even _______ bit of the data changes, the hash output changes completely. To verify integrity, compare the _______ hash to the _______ hash after transmission or storage.",
                "answer": "Hash value (fingerprint); one; received; original.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "SHA-256 (Secure Hash Algorithm 256-bit) is a widely used cryptographic hash function. It is _______ -way -- you cannot reverse the hash to recover the original input. MD5 produces a 128-bit hash but is considered _______ for security purposes because collisions can be engineered. A collision is when two _______ inputs produce the _______ hash output.",
                "answer": "One; weak (cryptographically broken); different; same.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "A digital _______ ensures both integrity and _______ of a message or document. The sender hashes the message and _______ the hash with their private key. The receiver decrypts the hash with the sender's _______ key and re-hashes the message -- if the hashes match, the message is unmodified and the sender is authenticated.",
                "answer": "Signature; authentication (non-repudiation); encrypts; public.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Threats to integrity include: _______ injection (attackers insert malicious data into a system), _______ -in-the-middle attacks (attacker modifies data during transmission), and _______ (attackers redirect users to fraudulent websites by corrupting DNS records). All three result in users receiving _______ data.",
                "answer": "SQL/code; man; DNS poisoning (cache poisoning); tampered (falsified).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "File integrity monitoring (FIM) tools alert administrators when critical system files are _______ modified. They do this by storing _______ of key files at baseline and comparing regularly. Examples include AIDE (Linux) and Tripwire. FIM is especially important on _______ and _______ servers where unauthorized changes could indicate a compromise.",
                "answer": "Unexpectedly; hashes; web; domain controller (critical infrastructure).",
                "lines": 3
            },
            {
                "num": "7",
                "question": "_______ controls like audit logs and version control help maintain and demonstrate integrity. A _______ trail records every change to data including who made it, when, and what changed. This is essential for _______ investigations and regulatory _______ (HIPAA, PCI-DSS require audit logging).",
                "answer": "Detective; audit; forensic; compliance.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A bank publishes software update files on their website so customers can download the latest mobile app. An attacker compromises the web server and replaces the legitimate installer with a malware-laced version. The file is the same size and has the same name. How would publishing a SHA-256 hash prevent customers from installing the malicious file?",
                "answer": "The bank should publish the SHA-256 hash of the legitimate installer alongside the download link (e.g., 'SHA-256: a3f9...'). Before installing, customers (or their software manager) run SHA-256 on the downloaded file. Even though the malicious version has the same filename and similar file size, its content is different from the original installer. A single-byte change causes the SHA-256 output to change completely (avalanche effect). When the customer computes the hash, it will not match the published value -- this is an immediate signal that the file has been tampered with. The customer should discard the file and alert the bank. This verification method is called hash-based integrity checking. Automated software management tools (package managers like apt, brew, or npm) do this automatically for every download, which is why supply chain attacks through package managers are difficult to execute undetected.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-6.3": {
        "unit": "tp-6.3",
        "title": "Availability Concerns",
        "n10_009": "FC0-U71 6.1",
        "n10_008": "FC0-U71 6.1",
        "questions": [
            {
                "num": "1",
                "question": "Availability in security means that systems, services, and data are _______ and _______ to authorized users when needed. An availability failure is called a _______ of Service. Causes include hardware failures, software bugs, natural disasters, and deliberate _______.",
                "answer": "Accessible; operational (functioning); denial; attacks.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "A Denial of Service (DoS) attack floods a target with _______ traffic or requests until it cannot serve legitimate users. A Distributed DoS (DDoS) attack uses thousands of _______ systems (called a _______) to amplify the attack. The compromised machines are typically infected with _______ allowing the attacker to control them remotely.",
                "answer": "Overwhelming (excessive); compromised; botnet; malware.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Availability is measured as _______ uptime. 99.9% uptime ('three nines') allows _______ hours of downtime per year. 99.999% ('five nines') allows only _______ minutes per year. Organizations choose their availability target based on the _______ of downtime (cost per hour of outage).",
                "answer": "Percentage; 8.76 hours; 5.26 minutes; business impact (cost).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "_______ eliminates single points of failure by having duplicate components so that if one fails, the other takes over. This includes redundant _______ supplies, _______ (multiple drives working together), _______ servers (secondary takes over if primary fails), and multiple _______ links to the internet.",
                "answer": "Redundancy; power; RAID; failover; network (ISP).",
                "lines": 3
            },
            {
                "num": "5",
                "question": "A _______ (BCP) is an organizational plan to maintain critical functions during and after a disaster. The _______ (DR) plan is a subset that focuses specifically on restoring IT systems. RTO (Recovery Time Objective) defines the maximum _______ the organization can tolerate. RPO (Recovery Point Objective) defines the maximum acceptable _______ loss.",
                "answer": "Business Continuity Plan; disaster recovery; downtime; data.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Load balancing distributes requests across multiple servers to prevent any one server from being _______ and to maintain availability during _______ spikes. _______ (Content Delivery Networks) cache content at geographically distributed edge nodes, reducing load on origin servers and improving availability globally.",
                "answer": "Overloaded; traffic; CDNs.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "RAID (Redundant Array of Independent Disks) protects availability of stored data. RAID _______ mirrors all data to two drives -- if one fails, data is still available. RAID _______ stripes data across three or more drives with parity, tolerating one drive failure. RAID _______ requires only raw speed but provides no fault tolerance.",
                "answer": "1; 5; 0.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A small clinic runs its patient scheduling system on a single physical server with no backup server and no offsite backups. A ransomware attack encrypts all files on the server. The clinic cannot schedule patients and cannot access existing appointment data. Identify two availability failures that made this scenario possible and describe specific controls for each.",
                "answer": "Failure 1 -- No redundancy/failover: the clinic has a single server with no standby. When it was taken offline (encrypted), there was no failover system to maintain operations. Control: implement a hot standby or cloud-based replica that can take over if the primary server is offline. Even a cold standby (a second server that can be restored from backup within a few hours) reduces downtime from days to hours. Failure 2 -- No offline or offsite backups: ransomware specifically targets and encrypts backup files on attached or network drives. A proper backup strategy uses the 3-2-1 rule: three copies of data, two different media types, one copy offsite or in immutable cloud storage (e.g., AWS S3 with object lock). An air-gapped or immutable backup cannot be encrypted by ransomware. With a clean backup from yesterday, the clinic restores the server and loses at most one day of appointment data -- not everything.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-6.4": {
        "unit": "tp-6.4",
        "title": "Privacy",
        "n10_009": "FC0-U71 6.1",
        "n10_008": "FC0-U71 6.1",
        "questions": [
            {
                "num": "1",
                "question": "Privacy is the right of individuals to control who has access to their _______ information and how it is used. In security, privacy is distinct from confidentiality: confidentiality protects data from _______ access, while privacy focuses on the individual's _______ rights over their own data.",
                "answer": "Personal; unauthorized; control.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "PII (Personally Identifiable Information) is any data that can identify a _______ person. Examples include _______, _______, _______, _______, and _______. The handling of PII is regulated by laws such as _______ (US healthcare), _______ (EU/UK), and COPPA (US children).",
                "answer": "Specific; name, SSN, email, phone, address, DOB (any four); HIPAA; GDPR.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "GDPR (General Data Protection Regulation) is a European Union law that requires organizations to obtain _______ consent before collecting personal data, allows individuals to request _______ of their data ('right to be forgotten'), and mandates that breaches be reported to authorities within _______ hours. Non-compliance fines can reach _______ % of annual global revenue.",
                "answer": "Explicit (informed); deletion; 72; 4.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Data _______ is the principle that organizations should collect only the minimum personal data necessary for a specific purpose. After that purpose is complete, the data should be _______ . Retaining personal data longer than needed increases _______ risk and regulatory exposure.",
                "answer": "Minimization; deleted (destroyed); breach.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "_______ replaces real personal data with fictional but realistic data for testing and development environments. _______ replaces part of the data with a placeholder (e.g., showing only the last 4 digits of a credit card). Both techniques reduce the risk of _______ exposure in non-production systems.",
                "answer": "Synthetic data (data masking); tokenization; PII.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "A _______ Policy explains what data an organization collects, how it is used, and with whom it is shared. It is required by GDPR, CCPA, and other privacy laws. Users must be given _______ notice before data collection. _______ (California Consumer Privacy Act) gives California residents the right to know what data is collected and to opt _______.",
                "answer": "Privacy; clear (adequate); CCPA; out.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "A data _______ is the accidental or unauthorized release of personal or sensitive information. Organizations must _______ affected individuals and in some cases regulators within a defined timeframe. Breach notification laws exist at the federal level (HIPAA) and state level (all 50 US states have breach notification laws). Costs include fines, _______ monitoring for affected individuals, and reputational damage.",
                "answer": "Breach; notify; credit.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A US high school collects student names, ages, email addresses, and behavioral incident reports in a cloud application. The vendor shares this data with third-party advertisers without the school's knowledge. Identify which federal student privacy law applies, what the violation is, and describe two steps the school should take.",
                "answer": "The applicable law is FERPA (Family Educational Rights and Privacy Act), which protects student educational records including behavioral records. Students (or parents, for minors) must consent before educational records are shared with third parties. The violation is the vendor sharing student PII and behavioral data with advertisers without FERPA-compliant consent -- this also likely violates COPPA (Children Online Privacy Protection Act) for students under 13. Step 1 -- Immediately audit the vendor contract: review the data processing agreement. If the contract does not prohibit sharing student data with third parties, it violates FERPA. The school must demand the vendor cease sharing data and delete all previously shared records. If the vendor refuses, terminate the contract. Step 2 -- Implement a vendor review process: before adopting any EdTech tool, require the vendor to sign a Student Data Privacy Agreement that explicitly prohibits secondary use of student data and requires breach notification.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-6.5": {
        "unit": "tp-6.5",
        "title": "AAA -- Authentication",
        "n10_009": "FC0-U71 6.1",
        "n10_008": "FC0-U71 6.1",
        "questions": [
            {
                "num": "1",
                "question": "AAA in security stands for _______, _______, and _______. Authentication answers: 'Who are _______?' Authorization answers: 'What are you _______ to do?' Accounting answers: 'What did you _______?'",
                "answer": "Authentication; authorization; accounting; you; allowed; do.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Authentication verifies that a user is who they claim to be. The three authentication factors are: something you _______ (password, PIN), something you _______ (smart card, security key, phone), and something you _______ (fingerprint, face, retina). Using two or more factors is called _______ -factor authentication (MFA).",
                "answer": "Know; have; are; multi.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Passwords are the most common authentication factor but also the weakest when they are _______, _______, or _______. Password best practices include: minimum _______ characters, use of upper/lower/numbers/symbols, no _______ personal info (names, dates), and no password _______ across multiple sites.",
                "answer": "Short; simple; reused; 12+ (8+); obvious; reuse.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "A _______ attack uses a list of common words and variations to crack passwords. A _______ force attack tries every possible combination. A _______ attack uses precomputed hash tables to find plaintext passwords. Account _______ after N failed attempts defeats all three approaches by limiting guesses.",
                "answer": "Dictionary; brute; rainbow table; lockout.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Multi-factor authentication (MFA) requires a second form of verification in addition to a password. Common second factors include _______ codes sent via SMS, _______ app codes (TOTP), _______ security keys (FIDO2/WebAuthn), and biometric scans. SMS-based MFA is the _______ secure option because SIM swapping attacks can intercept codes.",
                "answer": "One-time (OTP); authenticator; hardware; least.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Single Sign-On (SSO) allows users to _______ once and gain access to multiple applications without re-entering credentials. SSO relies on a trusted _______ provider (IdP) that issues authentication _______ to authorized applications. Examples include Microsoft Entra (formerly Azure AD), Google Workspace, and Okta.",
                "answer": "Log in (authenticate); identity; tokens.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Phishing attacks target authentication by tricking users into entering credentials on _______ websites that look real. Spear _______ is a targeted phishing attack aimed at a specific individual or organization. Phishing is the most common initial vector in _______ breaches. FIDO2 hardware keys are phishing-_______ because the key verifies the site domain before authenticating.",
                "answer": "Fake (fraudulent); phishing; data; resistant.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A company requires employees to use a 6-digit PIN as their only authentication factor for the internal HR system containing salary and personal data for all 500 employees. Describe two specific weaknesses of this authentication scheme and recommend a stronger implementation, explaining why each improvement helps.",
                "answer": "Weakness 1 -- Single factor (no MFA): a 6-digit PIN is a 'something you know' factor only. If an attacker learns the PIN (via shoulder surfing, keylogging, phishing, or a database breach), they gain immediate full access with no second barrier. Recommendation: add a second factor -- require an authenticator app TOTP code (e.g., Microsoft Authenticator). Even if a PIN is stolen, the attacker also needs the employee phone to complete login. This eliminates the single-point-of-failure problem. Weakness 2 -- Low entropy (10^6 = 1 million combinations): a 6-digit PIN can be brute-forced in seconds with no rate limiting. If the system does not lock accounts after failed attempts, an automated script can try all 1,000,000 combinations quickly. Recommendation: enforce account lockout after 5 failed attempts and require a minimum 12-character password with complexity requirements instead of a 6-digit PIN. This raises the brute force cost to impractical levels.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-6.6": {
        "unit": "tp-6.6",
        "title": "AAA -- Authorization",
        "n10_009": "FC0-U71 6.1",
        "n10_008": "FC0-U71 6.1",
        "questions": [
            {
                "num": "1",
                "question": "Authorization (the second A in AAA) determines what a verified user is _______ to do after they authenticate. Authentication proves _______ the user is; authorization defines _______ they can access and what _______ they can perform.",
                "answer": "Permitted (allowed); who; what; actions.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Role-Based Access Control (RBAC) assigns permissions based on _______ rather than individual identity. A nurse role has different access than a _______ role. Permissions are granted to _______, and users inherit permissions by being assigned a role. This is easier to _______ at scale than per-user permissions.",
                "answer": "Job role (function); physician/admin (any role); roles; manage.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "The principle of _______ privilege states that each user or system component should have only the _______ permissions required to perform their job -- nothing extra. This limits _______ in the event of a compromised account. If an accountant is compromised, they should not be able to access _______ source code or patient records.",
                "answer": "Least; minimum; damage; production.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Mandatory Access Control (MAC) uses _______ labels (e.g., Top Secret, Confidential) assigned by the system or administrator. Users can only access resources at or _______ their clearance level. MAC is common in _______ and government environments. Discretionary Access Control (DAC) lets the _______ owner set permissions.",
                "answer": "Sensitivity; below; military; resource.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Privilege _______ is a common attack where an attacker exploits a vulnerability to gain _______ access than authorized. Horizontal escalation means gaining access to _______ user accounts at the same level. Vertical escalation means gaining _______ (admin or root) privileges from a standard user account.",
                "answer": "Escalation; more; other; elevated.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "An Access Control List (ACL) is a list attached to a resource (file, folder, network port) that specifies which _______ or _______ are allowed or denied access. On Linux file systems, each file has _______ (read/write/execute) permissions for owner, _______, and others. On Windows, NTFS uses ACLs to control file and folder access.",
                "answer": "Users; groups; rwx; group.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Separation of duties requires that critical tasks are _______ across multiple people so no single person can complete a sensitive action alone. For example, the person who _______ a payment should not be the same person who _______ it. This is a key internal control that reduces _______ and financial fraud.",
                "answer": "Split (divided); initiates (creates); approves; insider threats.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A software company gives all engineers admin rights to the production database because it is more convenient during development. One engineer's laptop is infected with malware. The malware uses the engineer's stored database credentials to export the entire customer database containing 2 million email addresses and passwords. Explain the authorization failure and describe two specific controls that would have limited the impact.",
                "answer": "Authorization failure: violation of least privilege. Engineers were granted admin rights -- the maximum permission level -- for convenience, not necessity. Most day-to-day engineering work requires read access to specific tables, not admin rights to the entire production database. When the credentials were stolen, the attacker inherited full admin access, allowing them to export all data. Control 1 -- Least-privilege role assignment: engineers should have read-only access to specific tables needed for their work in production. Only DBAs with a demonstrated need should have admin rights, and those credentials should be stored in a secrets manager with time-limited access tokens, not saved in IDE configs or laptops. Control 2 -- Database activity monitoring (DAM) and anomaly detection: log all database queries and alert on bulk data exports. A single query selecting 2 million rows at 2am should trigger an immediate alert and optional automated block. Even if the attacker had the credentials, the bulk export would be flagged before completion.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-6.7": {
        "unit": "tp-6.7",
        "title": "AAA -- Accounting",
        "n10_009": "FC0-U71 6.1",
        "n10_008": "FC0-U71 6.1",
        "questions": [
            {
                "num": "1",
                "question": "Accounting (the third A in AAA) is the process of _______ user activity on a system. It creates a record of who _______ in, what they _______, and when they logged _______. This record is called an _______ log or audit trail.",
                "answer": "Tracking; logged; accessed/did; out; audit.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Audit logs provide _______ -- the ability to trace activity back to a specific user. This supports _______ investigations after a breach, regulatory _______ (HIPAA, PCI-DSS require logs), and detection of _______ anomalies like a user accessing files outside business hours.",
                "answer": "Accountability; forensic; compliance; suspicious.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "A SIEM (Security Information and Event Management) system _______ logs from multiple devices and applications into a central _______ for analysis and alerting. It correlates events across sources to detect _______ that no single log would reveal. Examples include Splunk, Microsoft Sentinel, and IBM QRadar.",
                "answer": "Aggregates (collects); platform (console); patterns (attacks).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Logs should be _______ to a separate server or write-once storage because an attacker who compromises the host may _______ logs to cover their tracks. _______ logging requires that logs cannot be modified once written. Time _______ ensures all logs share a consistent clock using NTP so events from multiple systems can be correlated accurately.",
                "answer": "Forwarded; delete (alter); Immutable; synchronization.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Common events that should always be logged include: _______ successes and failures (who tried to log in), _______ changes (who changed what permissions), _______ access (who read or exported sensitive files), and _______ (creating, deleting, modifying accounts). Together these events form a security baseline for detecting insider threats.",
                "answer": "Login; privilege; data; user management.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Log _______ refers to how long logs are retained before deletion. HIPAA requires audit logs to be retained for _______ years. PCI-DSS requires _______ months. Too-short retention means logs may not be available during a forensic investigation. Organizations should define a _______ policy that balances compliance, storage cost, and investigation needs.",
                "answer": "Retention; 6; 12 (1 year); log retention.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Non-repudiation means a user _______ deny having performed an action when logs prove they did. Digital _______ provide non-repudiation for electronic documents and transactions. In accounting, it is the combination of _______ (proving who acted) and _______ (proving the action was recorded) that creates non-repudiation.",
                "answer": "Cannot; signatures; authentication; logging.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A hospital systems administrator is suspected of accessing patient records for celebrities without a clinical reason. The privacy officer wants to investigate, but the access logs are only retained for 30 days and the alleged access occurred 45 days ago. The logs are gone. Identify the compliance failure, which regulation was violated, and describe two logging practices that would have allowed the investigation to proceed.",
                "answer": "Compliance failure: HIPAA requires covered entities to retain access audit logs for a minimum of 6 years (not 30 days). The hospital is in violation of HIPAA's audit control requirements (45 CFR 164.312(b)) and record retention requirements. This is not just a privacy program failure -- it carries regulatory penalty risk. Practice 1 -- HIPAA-compliant log retention policy: set the log retention period to 6 years minimum across all systems handling PHI. Storage is inexpensive -- 6 years of access logs for a mid-size hospital costs much less than a HIPAA violation fine (which can reach $1.9 million per violation category). Practice 2 -- Automated log archival to immutable cold storage: configure the SIEM and EHR system to automatically archive access logs to write-once cloud storage (e.g., AWS S3 Glacier with object lock) after 30 days. The logs are no longer hot (fast), but they remain recoverable for investigation or audit for the full retention period.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-6.8": {
        "unit": "tp-6.8",
        "title": "Non-Repudiation",
        "n10_009": "FC0-U71 6.1",
        "n10_008": "FC0-U71 6.1",
        "questions": [
            {
                "num": "1",
                "question": "Non-repudiation is the security property that ensures a party _______ deny having sent a message or performed an action after the fact. It provides _______ of origin (sender cannot deny sending) and _______ of receipt (receiver cannot deny receiving). It is achieved through a combination of _______ and _______.",
                "answer": "Cannot; proof; proof; authentication; audit logging.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Digital signatures provide non-repudiation for electronic documents. The sender uses their _______ key to sign the hash of the document. The receiver uses the sender's _______ key to verify the signature. Only the sender's private key could have produced that signature, so the sender _______ deny signing the document.",
                "answer": "Private; public; cannot.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "A Certificate Authority (CA) is a trusted third party that issues _______ certificates that bind a public key to an identity. This is part of the PKI (Public Key Infrastructure). When a CA signs a certificate, it provides non-repudiation for _______ transactions by confirming that the public key genuinely belongs to the stated _______.",
                "answer": "Digital; electronic; identity (entity).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "A digital signature is _______ from a written signature because it is cryptographically bound to the _______ of the document. If the document changes after signing, the signature becomes _______. A written signature _______ detect document tampering after the fact.",
                "answer": "Different (stronger); content; invalid; cannot.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "In legal and financial contexts, non-repudiation ensures that electronic contracts and transactions are _______ . The US E-SIGN Act and UETA give electronic signatures the same _______ weight as handwritten signatures. eSignature platforms like DocuSign use PKI-based digital signatures to provide court-admissible _______.",
                "answer": "Enforceable (legally binding); legal; non-repudiation.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Timestamping adds non-repudiation for _______ -- proving that a signature or document existed at a specific point in time. A trusted timestamping authority (TSA) signs a hash of the document along with the current _______, creating a verifiable record that the document existed in its current form at that _______.",
                "answer": "Time; timestamp; moment.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "HMAC (Hash-based Message Authentication Code) provides _______ and data _______, but not non-repudiation. This is because HMAC uses a _______ key -- both sender and receiver have the same key, so either party could have created the MAC. Non-repudiation requires _______ keys (only the sender's private key can sign).",
                "answer": "Authentication; integrity; shared (symmetric); asymmetric.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A contractor submits an invoice via email claiming they delivered 200 hours of work. The company disputes receiving the deliverables and refuses to pay. The contractor says they sent the files; the company says they never arrived. There is no digital signature on the email. Explain what non-repudiation mechanism would have resolved this dispute and describe how it works.",
                "answer": "A digitally signed email with a trusted timestamp would have resolved this. Here is how it works: (1) The contractor configures their email client with an S/MIME certificate issued by a trusted CA. (2) When they send the deliverables, their email client hashes the email body and attachments, then encrypts the hash with their private key to produce a digital signature. (3) The signed email is sent. The company receives it and their email client verifies the signature using the contractor's public key (obtained from the CA certificate). If verification passes, it proves the email came from the contractor and the content was not modified in transit. (4) A trusted timestamp from a TSA proves the signed message existed at a specific date and time. With this evidence: the contractor cannot deny sending (signature uses their private key), the company cannot deny receiving (the mail server logs and signature receipt are recorded), and the content (deliverables) cannot be disputed (any change would invalidate the signature). This is legally admissible in contract disputes.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-6.9": {
        "unit": "tp-6.9",
        "title": "Security Awareness",
        "n10_009": "FC0-U71 6.2",
        "n10_008": "FC0-U71 6.2",
        "questions": [
            {
                "num": "1",
                "question": "Security awareness training teaches employees to recognize and _______ to security threats. The most common attack vector that bypasses all technical controls is _______ engineering -- manipulating _______ rather than systems. Organizations with high security awareness have _______ breach rates than those without training.",
                "answer": "Respond; social; people; lower.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Social engineering attacks exploit human _______ (wanting to help), _______ (acting fast without thinking), _______ (following authority figures), and _______ (doing what others do). Recognizing these psychological triggers is the first step in _______ them.",
                "answer": "Helpfulness; urgency; authority; social proof; resisting.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Phishing emails often: use _______ sender addresses that look legitimate at first glance, create a sense of _______ ('act now or your account will be closed'), contain _______ to malicious websites, and request _______ or financial information. The red flag test: a legitimate organization will never ask for your password via _______.",
                "answer": "Spoofed; urgency; links (URLs); credentials; email.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Pretexting is when an attacker creates a fake _______ to manipulate a target. For example, an attacker calls IT support pretending to be a _______ and asks for a password reset. A _______ attack physically follows an authorized person through a secure door. _______ involves leaving infected USB drives where employees will find and plug them in.",
                "answer": "Scenario (story); manager/executive; tailgating (piggybacking); baiting.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Security awareness programs should include: _______ training for new employees, _______ refresher training throughout the year, _______ phishing simulations (fake phishing emails sent to employees to test their response), and _______ reporting procedures (clear instructions on how to report suspicious activity).",
                "answer": "Onboarding; recurring (periodic); simulated; clear.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "An insider _______ is a current or former employee who intentionally or accidentally causes harm. _______ insider threats are employees who deliberately steal data or sabotage systems. _______ insider threats are employees who accidentally cause breaches (clicking phishing links, misconfiguring systems). Both types are addressed partially through awareness _______.",
                "answer": "Threat; malicious; negligent; training.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Clean desk policy requires employees to clear _______ documents from their desk when not at it. Screen _______ software locks the screen after a period of inactivity. _______ filters make it difficult to read a screen from the side, preventing shoulder _______ in public spaces. These physical security measures support _______ confidentiality.",
                "answer": "Sensitive; lock (saver); Privacy; surfing; data.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: An attacker calls a bank employee and says: 'Hi, this is Mike from IT security. We had a breach last night and I need to urgently verify your credentials to protect your account. Can you give me your username and password?' The employee, panicked by the word 'breach,' complies. Identify the social engineering techniques being used and describe what the employee should have done instead.",
                "answer": "Social engineering techniques used: (1) Authority: the attacker claims to be from IT security, a trusted internal authority. Employees are conditioned to comply with IT requests. (2) Urgency/fear: mentioning a breach create panic and time pressure that bypasses rational thinking -- the employee feels they must act immediately. (3) Pretexting: the attacker constructed a plausible false scenario (post-breach credential verification) to justify the unusual request. What the employee should do: (1) Never provide credentials over the phone -- legitimate IT staff never need your password. They can reset it without you verifying it verbally. (2) Verify the caller's identity through a separate channel: hang up and call the IT help desk directly using the number from the company directory (not a number the caller provides). Ask if Mike from IT security made this call. (3) Report the attempt to the security team immediately -- this is a live attack. The goal is to identify and report, not argue with the attacker.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-6.10": {
        "unit": "tp-6.10",
        "title": "Securing Devices",
        "n10_009": "FC0-U71 6.2",
        "n10_008": "FC0-U71 6.2",
        "questions": [
            {
                "num": "1",
                "question": "Endpoint security refers to protecting _______ devices (laptops, phones, tablets, desktops) from threats. Each endpoint is a potential _______ into the network. Key endpoint controls include _______ software, _______ encryption, _______ management, and device _______ policies.",
                "answer": "End-user; entry point (attack vector); antivirus; full-disk; patch; hardening.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Full disk encryption (FDE) protects data on a device if it is lost or _______. BitLocker is the FDE solution built into Windows _______. FileVault is the FDE solution built into _______. When FDE is enabled, all data on the drive is _______ and requires an authentication step at boot to unlock.",
                "answer": "Stolen; Pro/Enterprise; macOS; encrypted.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Patch management is the process of applying _______ updates to operating systems and applications. Unpatched vulnerabilities are the leading cause of successful _______. Organizations should apply critical patches within _______ days of release. _______ testing or patch testing in a non-production environment before deploying reduces risk of breaking systems.",
                "answer": "Security; attacks (breaches); 30 (14 or 72 hours for critical); staged.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Antivirus (AV) software detects known malware using _______ -based detection (comparing files against a database of known malware signatures). Modern _______ (Endpoint Detection and Response) tools use behavior-based detection to catch _______ malware that has no known signature. Both types should generate _______ when threats are found.",
                "answer": "Signature; EDR; zero-day (novel); alerts.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "A host-based _______ (HFW) controls which network connections a device can make and accept. It blocks _______ access attempts from the network. The Windows Defender Firewall is a built-in _______ for Windows. Rules specify allowed and denied _______ (80/443 for web, 22 for SSH) and source _______.",
                "answer": "Firewall; unauthorized (inbound); HFW; ports; IP addresses.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "MDM (Mobile Device Management) allows organizations to _______ , configure, and _______ employee mobile devices. MDM can enforce _______ requirements, push _______ updates, and remotely _______ a lost or stolen device. BYOD (Bring Your Own Device) policies require MDM enrollment to access corporate resources.",
                "answer": "Enroll; monitor; password; configuration/security; wipe.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Device hardening reduces the _______ surface by removing or disabling unnecessary services, software, and features. Steps include: disable unused _______ (Bluetooth, Wi-Fi, IR), remove unneeded _______ (games, media players on servers), change default _______, and enable _______ audit logging.",
                "answer": "Attack; interfaces; software (applications); passwords; system.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A healthcare worker accidentally leaves their unencrypted company laptop at a coffee shop. The laptop contains a local cache of 300 patient appointment records including names, DOBs, and phone numbers. The laptop is not recovered. Describe the regulatory obligations the healthcare organization now has and explain what two device security controls would have prevented this from being a reportable breach.",
                "answer": "Regulatory obligations: this is a HIPAA breach. Because the PHI (protected health information) was unencrypted and on an unrecovered device, HHS must be notified. If 300+ individuals are affected, notification to HHS must occur within 60 days of year end (or 60 days of discovery if 500+ individuals). Affected patients must receive written breach notification letters. The state attorney general may also require notification under state breach notification law. Control 1 -- Full disk encryption (BitLocker): if the laptop's drive was BitLocker-encrypted with a strong recovery key managed by the organization, the thief cannot access any data without the encryption key -- even by removing the drive and connecting to another machine. HHS guidance explicitly states that encrypted lost/stolen devices are NOT reportable breaches, because the data is cryptographically protected. Control 2 -- MDM with remote wipe: enroll all laptops in an MDM solution. If the device connects to any network, the MDM can issue a remote wipe, erasing all data. This limits the exposure window and demonstrates to regulators that the organization took rapid mitigation steps.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-6.11": {
        "unit": "tp-6.11",
        "title": "Device Use Best Practices",
        "n10_009": "FC0-U71 6.2",
        "n10_008": "FC0-U71 6.2",
        "questions": [
            {
                "num": "1",
                "question": "Acceptable Use Policies (AUPs) define what employees may and may not do with company devices and networks. They are signed at _______ and set legal and disciplinary precedent for violations. Key AUP topics include: personal use of company _______, prohibited _______ and websites, handling of _______ data, and reporting obligations.",
                "answer": "Onboarding; devices; software; sensitive.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Company devices should only have _______ -approved software installed. Unauthorized software (shadow IT) may contain _______, create unpatched _______ attack surfaces, and circumvent _______ controls. Employees should not use personal _______ accounts or cloud storage to store company data.",
                "answer": "IT (approved); malware; vendor; security; email/cloud.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "USB drives are a _______ security risk. They can introduce _______ (if plugged in from an untrusted source) and exfiltrate _______ (if used to copy sensitive files). Organizations can mitigate USB risk by: disabling _______ ports in BIOS or via policy, using _______ that only allow company-issued drives, or deploying DLP to block sensitive file copies.",
                "answer": "Physical; malware; data; USB; whitelisting (device control software).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Screen _______ should lock the device after a short period of inactivity (5-15 minutes). Devices should require a _______ or biometric to unlock. When leaving a workstation even briefly, users should manually _______ the screen (Windows: Win+L, macOS: Ctrl+Cmd+Q). _______ surfing -- reading someone's screen in public -- is a real physical security threat.",
                "answer": "Lock; password/PIN; lock; shoulder.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Remote work introduces additional risks including use of _______ Wi-Fi networks, _______ routers with default passwords, and family members using company devices. Organizations should require _______ (VPN) use when working off-site and prohibit _______ sharing of company devices with family members.",
                "answer": "Public; home; VPN; device.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Software updates and patches should be applied _______ because most malware exploits _______ vulnerabilities (known flaws with available fixes). Enabling _______ updates for OS and major applications removes the human delay. _______ reboots required to complete patches should be performed promptly even if inconvenient.",
                "answer": "Promptly; known; automatic; pending.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "When a device is _______ for disposal, repurposing, or return, its data must be securely wiped. Simply _______ files does not remove them -- the data can be recovered with forensic tools. Secure deletion methods include _______ -pass overwrites, _______ (destroying the drive physically), and _______ (if the drive was fully encrypted, deleting the key renders all data unrecoverable).",
                "answer": "Decommissioned; deleting; multi; shredding/degaussing; crypto-erasure.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: An employee working from home connects their company laptop to the public Wi-Fi at a local coffee shop to finish a report. They email the report as a Word attachment to their personal Gmail because they cannot access the company file share from outside the office. Identify two security policy violations in this scenario and explain the risk each creates.",
                "answer": "Violation 1 -- Using public Wi-Fi without a VPN: public Wi-Fi is unencrypted and untrusted. An attacker on the same network can perform a man-in-the-middle attack, intercepting unencrypted traffic including email credentials, session tokens, and any unencrypted data transmitted. The AUP should require VPN use on any non-corporate network. The VPN creates an encrypted tunnel from the laptop to the company network, preventing eavesdropping. Violation 2 -- Sending company data to personal email (Gmail): corporate data sent to a personal email account is outside the company's control. Gmail is not covered by the company's DLP policies, retention rules, or security monitoring. If the employee's Gmail account is compromised (password reuse, phishing), attackers gain access to the report. Additionally, this creates a data governance problem -- the company cannot audit, retrieve, or delete data stored in personal accounts. The fix is cloud-accessible company file storage (SharePoint, OneDrive, Google Workspace) so employees can work remotely without resorting to personal email.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-6.12": {
        "unit": "tp-6.12",
        "title": "Safe Browsing Practices",
        "n10_009": "FC0-U71 6.2",
        "n10_008": "FC0-U71 6.2",
        "questions": [
            {
                "num": "1",
                "question": "HTTPS (HyperText Transfer Protocol Secure) encrypts communication between the browser and web server using _______. A _______ padlock in the browser address bar indicates an HTTPS connection. HTTPS does NOT mean the website is _______ -- it only means the _______ is encrypted. Phishing sites routinely use HTTPS.",
                "answer": "TLS (SSL/TLS); padlock; trustworthy (safe); connection.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "A browser warning 'Your connection is not private' means the site's _______ certificate is invalid, expired, or not signed by a trusted _______ Authority. Users should not click 'proceed anyway' on unfamiliar sites because HTTPS protects the _______ , not the site's _______ .",
                "answer": "SSL/TLS; certificate; transport; legitimacy (content).",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Drive-by downloads occur when visiting a _______ website causes malware to be automatically _______ without user interaction. They often exploit unpatched vulnerabilities in the _______ or _______ . Keeping both updated and enabling _______ -scripting defenses (blocking unknown JavaScript) reduces risk.",
                "answer": "Malicious (compromised); downloaded (installed); browser; plugins (extensions); no.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "URL inspection before clicking: check that the _______ domain is the expected one (attackers use similar-looking domains like paypa1.com). Look for _______ (misspellings designed to look like legitimate domains). Hover over links before clicking to see the _______ URL in the status bar. Shortened URLs (bit.ly) can _______ the real destination.",
                "answer": "Actual; typosquatting; real; hide.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Browser extensions can be a significant _______ risk. A malicious extension can read and modify _______ on pages visited, steal _______ , and bypass _______ controls. Best practice: install only extensions from _______ sources with a high number of verified reviews, and remove unused extensions.",
                "answer": "Security; content; credentials; browser; trusted (official store).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Cookies are small files websites store in the browser to remember _______ and preferences. Third-party _______ track users across websites for advertising. _______ mode (Incognito) prevents local storage of browsing history and reduces some tracking but does NOT make browsing _______ from the network or websites.",
                "answer": "Sessions (login state); cookies; private; invisible.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "An ad blocker can reduce _______ ad attacks (malicious ads that deliver malware). A DNS _______ service (like Cloudflare 1.1.1.1 with filtering or OpenDNS) blocks requests to known _______ domains before they load. A Web proxy or _______ Filter categorizes and blocks unsafe websites at the network level.",
                "answer": "Malvertising; filtering; malicious; Content.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A student clicks a link in a Discord message that says 'free Steam games.' The link opens a page that looks identical to the Steam login page, but the URL is 'stearn.io' instead of 'store.steampowered.com'. They enter their username and password. Two hours later their Steam account is emptied of $300 in items. Explain what attack occurred and list four specific warning signs the student should have caught.",
                "answer": "Attack: credential harvesting phishing via a spoofed (fake) login page. The attacker created a pixel-perfect copy of the Steam login page on a lookalike domain. When the student entered credentials, they were sent directly to the attacker. The attacker then used the credentials on the real Steam site before the student noticed. Warning sign 1 -- Suspicious source: the link came through Discord DM from someone they may not know well, offering something too good to be true ('free games'). Unsolicited offers are a primary phishing vector. Warning sign 2 -- Wrong domain: 'stearn.io' is not 'steampowered.com'. The student should have looked at the address bar before entering any credentials. The legitimate URL would be store.steampowered.com (or steampowered.com). Warning sign 3 -- No HTTPS padlock from a trusted authority/wrong certificate: the padlock may exist but the certificate would be for 'stearn.io', not Valve/Steam. Warning sign 4 -- Urgency to log in: phishing pages want you to log in quickly before you notice something is wrong. Slowing down and inspecting before entering credentials is the most effective countermeasure.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-6.13": {
        "unit": "tp-6.13",
        "title": "Password Best Practices",
        "n10_009": "FC0-U71 6.3",
        "n10_008": "FC0-U71 6.3",
        "questions": [
            {
                "num": "1",
                "question": "A strong password should be: at least _______ characters long, contain a mix of _______, _______, _______, and _______, and not include obvious personal information like _______, _______, or pet names. Length is the single most important factor -- a 16-character passphrase beats a 10-character complex password in brute force resistance.",
                "answer": "12 (or more); uppercase letters; lowercase letters; numbers; symbols; names; birthdays.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Password _______ means using the same password on multiple sites. It is extremely dangerous because if any one site is breached and your password is exposed, attackers use _______ stuffing attacks to automatically try that password on banking, email, and other accounts. The fix is to use a unique password for _______ account.",
                "answer": "Reuse; credential; every.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "A password _______ stores all your passwords in an encrypted vault, protected by a single strong _______ password. It can generate and autofill _______, unique passwords for every site. Examples include Bitwarden, 1Password, and LastPass. The browser saves them for _______ of use. This is the recommended solution to the reuse problem.",
                "answer": "Manager; master; random (strong); convenience.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Passwords should never be _______ insecurely (written on sticky notes, sent in plain text email, stored in an unencrypted text file). Never share passwords via _______ or messaging apps. If you must write a master password down as a backup, store it in a physically _______ location (safe, locked drawer -- not a monitor sticky note).",
                "answer": "Stored; email; secure.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Default passwords on devices (routers, printers, IP cameras) must be _______ immediately on setup. Many devices ship with the same default credentials (like admin/admin or admin/password) that are _______ documented online. Attackers scan for devices with _______ credentials as an automated first step. Failure to change defaults is one of the most common _______ vulnerabilities in home and small business networks.",
                "answer": "Changed; publicly; default; exploited.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Password _______ policies require users to change passwords on a regular schedule (e.g., every 90 days). NIST now recommends _______ periodic rotation unless there is evidence of compromise, because forced rotation leads to _______ password choices (e.g., Password1, Password2). Instead, NIST recommends checking passwords against known _______ lists at creation.",
                "answer": "Rotation (expiration); against; predictable; breached (compromised).",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Passwords in databases must be stored as _______ not plaintext. A _______ function converts the password to a fixed-length digest. A random value called a _______ is added before hashing to ensure two users with the same password have different stored hashes, defeating _______ table attacks.",
                "answer": "Hashes; hash; salt; rainbow.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A student uses the same password ('Gopackers88!') for their school email, Instagram, a gaming forum, and their bank. The gaming forum is breached and their email/password is posted publicly. Within 24 hours, their Instagram is taken over and their bank issues a fraud alert. Explain step by step how the attacker moved from a gaming forum breach to a bank account attempt.",
                "answer": "Step 1 -- Breach acquisition: the gaming forum database is stolen and cracked. The student's email and password hash 'Gopackers88!' is in the breach dump. The hash is cracked (or the site stored passwords in plaintext). The attacker now has: email = student@gmail.com, password = Gopackers88!. Step 2 -- Credential stuffing: the attacker runs an automated tool that takes the stolen email/password pair and tries it against hundreds of popular sites (Instagram, Facebook, Twitter, Amazon, PayPal, major banks) in rapid succession. This is credential stuffing -- the attack relies on password reuse. Step 3 -- Instagram takeover: login succeeds on Instagram. The attacker immediately changes the recovery email and phone number, locking the student out. Step 4 -- Bank attempt: the bank's fraud system flags the login attempt from an unrecognized device or IP and issues an alert, preventing the takeover. Fix: use a password manager to generate a unique random password for every account. Even if the gaming forum is breached, the attacker gains nothing usable elsewhere.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-6.14": {
        "unit": "tp-6.14",
        "title": "Encryption and Data Types",
        "n10_009": "FC0-U71 6.4",
        "n10_008": "FC0-U71 6.4",
        "questions": [
            {
                "num": "1",
                "question": "Plaintext is data that is _______ and _______ readable. Ciphertext is data that has been _______ and is not readable without the decryption key. Encryption is the process of converting _______ to _______. Decryption is the reverse. The algorithm + key combination is called a _______ .",
                "answer": "Unencrypted; human-; encrypted; plaintext; ciphertext; cipher.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Symmetric encryption uses the _______ key for both encryption and decryption. It is faster than asymmetric encryption and is used for _______ data at rest. Key examples: AES-256, 3DES. The major challenge with symmetric encryption is _______ distribution -- how do two parties share the key _______ first meeting without someone intercepting it?",
                "answer": "Same; encrypting; key; before.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Asymmetric encryption uses a mathematically linked _______ key pair. The _______ key is shared openly; the _______ key is never shared. Data encrypted with the public key can only be decrypted by the _______ key. This solves the key distribution problem. RSA and ECC are common _______ encryption algorithms.",
                "answer": "Key pair (two); public; private; private; asymmetric.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "In practice, HTTPS uses a _______ of both. Asymmetric encryption is used during the TLS _______ to exchange a one-time _______ key. Then symmetric encryption (AES) encrypts the actual _______ data because symmetric is much _______ than asymmetric for bulk data.",
                "answer": "Hybrid; handshake; session (symmetric); session; faster.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Data at _______ is data stored on a drive, database, or backup media. It should be encrypted with AES-256. Data in _______ is data actively moving across a network. It should be encrypted using TLS. Data in _______ is data actively being processed in RAM by a CPU. This is the hardest to encrypt and is a target of _______ scraping malware.",
                "answer": "Rest; transit; use; memory.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Data types relevant to security classification: _______ data is personal/identifiable information. _______ data is financial records, trade secrets, IP. _______ data has no identified source and presents lower risk. Data _______ is the process of removing identifying fields so data cannot be linked to an individual. _______ replaces sensitive fields with random tokens.",
                "answer": "Sensitive (PII/PHI); proprietary (confidential); anonymous; anonymization; tokenization.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "A common encryption misconception: password _______ is NOT encryption. Hashing is _______ -way -- you cannot recover the original password from the hash. Encryption is _______ -way -- you can recover the plaintext with the key. Passwords should be _______ with a salt. Files should be _______.",
                "answer": "Hashing; one; two (reversible); hashed; encrypted.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A company stores customer credit card numbers in their database in plaintext so customer service reps can read them when handling calls. Their database is later breached and all 50,000 card numbers are stolen. Explain what they should have stored instead of plaintext card numbers and describe how tokenization would have made the breach far less damaging.",
                "answer": "Instead of plaintext card numbers, the company should have stored tokens. Tokenization replaces each real credit card number with a randomly generated token (e.g., 4x3a-9y2b-...) that has no mathematical relationship to the original number. The real card number is stored securely in a separate, heavily protected token vault managed by a PCI-compliant tokenization provider. How this limits the breach: when the attacker steals the database, they get 50,000 random tokens -- not credit card numbers. The tokens are useless for making fraudulent purchases because they cannot be reversed to the real card numbers without access to the token vault (which was not breached). Customer service reps see the token in their system and it is sufficient to identify the customer's payment method context, but not to make charges. This is why major payment processors (Stripe, Braintree) use tokenization -- no merchant ever stores real card numbers, so merchant breaches cannot expose cards. The company also likely violated PCI-DSS by storing plaintext card numbers, which mandates encryption or tokenization of stored cardholder data.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-6.15": {
        "unit": "tp-6.15",
        "title": "Securing Small Wireless Networks",
        "n10_009": "FC0-U71 6.5",
        "n10_008": "FC0-U71 6.5",
        "questions": [
            {
                "num": "1",
                "question": "Wi-Fi networks use _______ waves to transmit data, making them accessible to anyone within range -- including attackers. Unlike wired networks, there is no _______ connection requirement. Therefore, wireless networks require strong encryption and authentication to prevent _______ access.",
                "answer": "Radio; physical; unauthorized.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "WEP (Wired Equivalent Privacy) was the original Wi-Fi encryption standard and is considered _______ -- do not use it. WPA (Wi-Fi Protected Access) improved on WEP but also has known weaknesses. WPA2 uses _______ encryption and is considered _______ secure. WPA3 is the _______ standard with stronger protections against offline dictionary attacks.",
                "answer": "Broken; AES; adequately; latest (current).",
                "lines": 3
            },
            {
                "num": "3",
                "question": "The Wi-Fi password on a home or small business router uses the _______ (Pre-Shared Key) mode of WPA2/WPA3. The PSK should be: at least _______ characters, random (not a dictionary word), and changed from the _______ password if one was preset. Enterprise networks use WPA2/WPA3 _______ mode with a RADIUS server instead of a shared key.",
                "answer": "PSK; 12+; default; Enterprise.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "The router admin console should be secured by: changing the _______ admin username and password, disabling _______ management (only allow admin access from the local network, not from the internet), and updating the router _______ regularly to patch known vulnerabilities.",
                "answer": "Default; remote; firmware.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "SSID _______ hides the network name so it does not appear in Wi-Fi scans. This provides _______ through obscurity -- not true security -- because attackers with basic tools can still detect hidden networks by monitoring _______ traffic. MAC address filtering only allows _______ MAC addresses to connect, but MAC addresses can be _______ by attackers.",
                "answer": "Hiding; security; wireless; whitelisted; spoofed.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "A guest network is a _______ Wi-Fi network that allows visitors to access the internet without accessing the _______ network where company or family devices reside. IoT devices (smart TVs, thermostats, cameras) should also be placed on an _______ VLAN or guest network because they often have poor _______ update practices and can serve as pivot points.",
                "answer": "Separate (isolated); primary; IoT; firmware.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "An evil twin attack creates a rogue wireless _______ with the same SSID as a legitimate network. Victims connect to the attacker's access point instead of the real one, allowing _______ -in-the-middle interception of all traffic. Using a _______ on any untrusted network prevents attackers from reading intercepted traffic even if connected to a rogue AP.",
                "answer": "Access point; man; VPN.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A small dental office has one wireless router for staff and patients combined. The router uses WPA2 with the password 'Dentist2018' and has never had a firmware update. A patient connects their laptop and notices the router admin page is accessible. They log in with the default admin/admin credentials. Identify four specific security failures and describe the fix for each.",
                "answer": "Failure 1 -- Shared network for staff and patients: patients should never be on the same network segment as staff computers and the practice management system containing patient PHI. Fix: set up a separate guest SSID for patient Wi-Fi that is isolated from the internal network. Failure 2 -- Weak, predictable password ('Dentist2018'): a dictionary-based password with a year suffix is trivially guessable. Fix: generate a random 16+ character WPA2-PSK and store it in a password manager. Failure 3 -- Default admin credentials (admin/admin): unchanged default credentials are the first thing any attacker tries. Fix: change the admin username and password to a strong unique credential immediately on setup. Disable remote admin access so the console is only reachable from the local wired network. Failure 4 -- No firmware updates: unpatched router firmware contains known vulnerabilities, including some that allow unauthorized remote code execution. Fix: check the manufacturer website or router admin panel for firmware updates and apply them. Enable automatic firmware updates if available.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    # DOMAIN 1 -- IT Concepts
    "tp-1.1": {
        "unit": "tp-1.1",
        "title": "Basics of Computing",
        "n10_009": "FC0-U71 1.1",
        "n10_008": "FC0-U71 1.1",
        "questions": [
            {
                "num": "1",
                "question": "A _______ is any physical component of a computer that you can touch, such as a keyboard, CPU, or hard drive. A _______ is a set of instructions that tells hardware what to do, such as an operating system or application.",
                "answer": "Hardware; software.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Every computer performs four fundamental functions: _______ (keyboard, mouse), _______ (CPU), _______ (RAM, hard drive), and _______ (monitor, speaker). The CPU coordinates all four of these functions.",
                "answer": "Input; processing; storage; output.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Analog signals are _______ (continuous/discrete) -- they can take any value within a range. Digital signals are _______ (continuous/discrete) -- they use only defined states such as 0 and 1. Computers process _______ data because transistors have two stable states: on and off.",
                "answer": "Continuous; discrete; digital.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Binary is the language computers use internally because transistors have only two states: _______ (represented as 1) and _______ (represented as 0). Each binary digit is called a _______, meaning Binary digIT.",
                "answer": "On (conducting); off (not conducting); bit.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "The CPU (Central Processing Unit) is responsible for _______ instructions. It fetches an instruction from memory, _______ it to determine what to do, and then _______ the operation. Modern CPUs perform billions of these cycles per second.",
                "answer": "Executing; decodes; executes.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "The operating system (OS) is the software that manages _______ resources (CPU, RAM, storage) and provides a platform for _______ to run. Without an OS, application software cannot communicate with the hardware.",
                "answer": "Hardware; application software (apps).",
                "lines": 3
            },
            {
                "num": "7",
                "question": "In a client-server model, the _______ device makes requests and the _______ device responds with data or services. A web browser on your laptop is an example of a _______, while the machine hosting the website is the _______.",
                "answer": "Client; server; client; server.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A student asks why their smart thermostat is considered a computer even though it does not have a screen or keyboard. Using the four functions of computing, explain how the thermostat qualifies as a computer and give one example of each function in that device.",
                "answer": "The thermostat qualifies as a computer because it performs all four functions. Input: temperature sensors read the current room temperature and the user sets a target temperature via buttons or an app. Processing: the CPU compares the current temperature to the target and decides whether to turn the heating or cooling on. Storage: the thermostat stores the schedule, settings, and historical temperature data. Output: it activates the HVAC system and displays status on a screen or app. Any device that performs all four functions -- regardless of form factor -- is a computer.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-1.2": {
        "unit": "tp-1.2",
        "title": "Binary",
        "n10_009": "FC0-U71 1.2",
        "n10_008": "FC0-U71 1.2",
        "questions": [
            {
                "num": "1",
                "question": "Binary is a base-_______ number system that uses only the digits _______ and _______. Each position in a binary number represents a power of two. The rightmost position represents 2^0 = _______, and the position immediately to its left represents 2^1 = _______.",
                "answer": "Base-2; 0 and 1; 1; 2.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Fill in the 8 bit-position values from left (most significant) to right (least significant):\n    ___ | ___ | ___ | ___ | ___ | ___ | ___ | ___",
                "answer": "128 | 64 | 32 | 16 | 8 | 4 | 2 | 1.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Convert the binary number 10110010 to decimal. Show your work by listing which bit positions are set to 1 and adding their values.",
                "answer": "Positions set to 1: 128, 32, 16, 2. Sum: 128 + 32 + 16 + 2 = 178.",
                "lines": 4
            },
            {
                "num": "4",
                "question": "Convert the decimal number 205 to binary using the subtraction method. Start at 128 and work right. Show each step.",
                "answer": "128 fits (205 - 128 = 77). 64 fits (77 - 64 = 13). 32 does not fit. 16 does not fit. 8 fits (13 - 8 = 5). 4 fits (5 - 4 = 1). 2 does not fit. 1 fits. Result: 11001101.",
                "lines": 5
            },
            {
                "num": "5",
                "question": "One byte equals _______ bits. One nibble equals _______ bits. A byte can represent values from 0 to a maximum of _______. The maximum value occurs when all 8 bits are set to _______.",
                "answer": "8 bits; 4 bits; 255; 1 (all ones: 11111111).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "The MSB stands for _______ and is the _______ (leftmost/rightmost) bit in a binary number. It has the _______ value. The LSB stands for _______ and is the _______ (leftmost/rightmost) bit, with value _______.",
                "answer": "Most Significant Bit; leftmost; highest (128 in a byte). Least Significant Bit; rightmost; 1.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Computers use binary because transistors -- the basic building blocks of processors -- have exactly _______ stable states: fully _______ (conducting, = 1) and fully _______ (not conducting, = 0). This makes binary arithmetic reliable and easy to implement in _______.",
                "answer": "Two; on; off; hardware (silicon).",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A student claims that the binary number 11111111 is the same as the decimal number 255. Another student says it must be more because there are eight 1s. Explain who is correct and why, showing the math using bit position values.",
                "answer": "The first student is correct. To convert 11111111 to decimal, add all bit position values where a 1 appears: 128 + 64 + 32 + 16 + 8 + 4 + 2 + 1 = 255. The second student is thinking of the digits as independent numbers rather than positional values. In binary, each digit represents a power of two based on its position -- not its face value. Eight 1-bits does not mean 8; it means the sum of all 8 powers of two from 2^0 through 2^7, which equals 255.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-1.3": {
        "unit": "tp-1.3",
        "title": "Hexadecimal",
        "n10_009": "FC0-U71 1.2",
        "n10_008": "FC0-U71 1.2",
        "questions": [
            {
                "num": "1",
                "question": "Hexadecimal is a base-_______ number system. It uses the digits 0 through 9 and the letters _______ through _______. The letter A represents the decimal value _______, and the letter F represents _______.",
                "answer": "16; A through F; A=10, F=15.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Convert the hexadecimal value 2F to decimal. Show your work:\n    2 is in the 16^1 position = 2 x _______ = _______\n    F (15) is in the 16^0 position = 15 x _______ = _______\n    Total = _______",
                "answer": "2 x 16 = 32; F(15) x 1 = 15; Total = 47.",
                "lines": 4
            },
            {
                "num": "3",
                "question": "To convert binary to hexadecimal, group binary digits into sets of _______ starting from the right. Convert the binary number 11010110:\n    Left group: _______ in binary = _______ in hex\n    Right group: _______ in binary = _______ in hex\n    Result: _______",
                "answer": "4 bits. Left group: 1101 = 13 = D. Right group: 0110 = 6. Result: D6 (or 0xD6).",
                "lines": 4
            },
            {
                "num": "4",
                "question": "The prefix _______ is used in programming to indicate a hexadecimal value (e.g., 0xFF). The hex value 0xFF equals _______ in decimal, which in binary is _______ -- the maximum value of one _______.",
                "answer": "0x; 255; 11111111; byte.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Hex is used for _______ addresses, which are 48-bit hardware identifiers written as six pairs of hex digits (e.g., AA:BB:CC:DD:EE:FF). Each pair represents _______ bits. Hex is also used for _______ codes in design (e.g., #FF5733).",
                "answer": "MAC; 8 bits (one byte); color (HTML/CSS).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Hex is also used for _______ addresses, where the location of data in RAM is expressed as a hex value. Programmers prefer hex over binary because it is more _______ while still mapping cleanly to binary -- every hex digit represents exactly _______ binary bits.",
                "answer": "Memory; compact (readable); 4.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Convert the decimal number 255 to hexadecimal. Show your work:\n    255 divided by 16 = _______ remainder _______\n    The remainder _______ is the rightmost hex digit = _______\n    The quotient _______ is the next digit\n    Result: _______",
                "answer": "255 / 16 = 15 remainder 15. Remainder 15 = F. Quotient 15 = F. Result: FF (or 0xFF).",
                "lines": 4
            },
            {
                "num": "8",
                "question": "REAL WORLD: A network technician reads a system log and sees a memory address listed as 0x1A4F. A new employee asks why the address is not just written in decimal. Explain why engineers use hexadecimal instead of decimal or binary for memory addresses, using at least two reasons.",
                "answer": "Reason 1 -- Compact representation of binary: each hex digit maps exactly to 4 binary bits, so 0x1A4F represents 0001 1010 0100 1111 in binary. Writing that as binary would require 16 digits; hex condenses it to 4 characters. Reason 2 -- Easier to read and transcribe than binary: humans make more errors copying long binary strings. Hex reduces cognitive load. Reason 3 -- Clean byte boundaries: since 1 byte = 8 bits = 2 hex digits, hex makes it easy to identify individual bytes in an address, which is useful when diagnosing memory and data alignment issues.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-1.4": {
        "unit": "tp-1.4",
        "title": "Octal",
        "n10_009": "FC0-U71 1.2",
        "n10_008": "FC0-U71 1.2",
        "questions": [
            {
                "num": "1",
                "question": "Octal is a base-_______ number system. It uses only the digits _______ through _______. The digits 8 and 9 do _______ (do/do not) exist in octal. Each octal digit represents exactly _______ binary bits.",
                "answer": "8; 0 through 7; do not; 3.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Convert the octal number 37 to decimal:\n    3 is in the 8^1 position = 3 x _______ = _______\n    7 is in the 8^0 position = 7 x _______ = _______\n    Total = _______",
                "answer": "3 x 8 = 24; 7 x 1 = 7; Total = 31.",
                "lines": 4
            },
            {
                "num": "3",
                "question": "To convert binary to octal, group binary digits into sets of _______ starting from the right. Convert 110101:\n    Left group: _______ = octal _______\n    Right group: _______ = octal _______\n    Result: _______",
                "answer": "3 bits. Left: 110 = 6. Right: 101 = 5. Result: 65 (octal).",
                "lines": 4
            },
            {
                "num": "4",
                "question": "In Linux, file permissions are displayed and set using octal. The permission value 755 means: owner has _______ (read/write/execute), group has _______ (read/execute only), and others have _______ (read/execute only). The octal digit 7 = binary _______ = rwx.",
                "answer": "Read/write/execute (7); read/execute (5); read/execute (5); 111.",
                "lines": 4
            },
            {
                "num": "5",
                "question": "Using octal, the chmod command sets file permissions on Linux. chmod _______ grants full permissions to owner, and read/execute only to group and others. chmod 600 means owner has _______ only, and group and others have _______ permissions.",
                "answer": "755; read/write (6 = rw-); no permissions (0 = ---).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Compare the four number systems by filling in the equivalent values for decimal 10:\n    Binary: _______\n    Octal: _______\n    Decimal: 10\n    Hexadecimal: _______",
                "answer": "Binary: 1010; Octal: 12; Decimal: 10; Hexadecimal: A.",
                "lines": 4
            },
            {
                "num": "7",
                "question": "Octal was historically used in older computing systems because early computers used _______ -bit or _______ -bit groupings where octal mapped cleanly. Today, octal is less common than hex because modern systems are byte-oriented (8-bit), and 8 bits divides more cleanly into _______ hex digits than _______ octal digits.",
                "answer": "6-bit or 12-bit; 2 hex; 3 octal (8 bits = 2.67 octal digits -- not a clean boundary).",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A student is setting permissions on a web server script in Linux and runs chmod 777 on the file. A senior admin immediately tells them to change it. Explain what chmod 777 means using octal-to-binary conversion, why it is a security risk, and what a safer permission value would be and why.",
                "answer": "chmod 777 means owner, group, and others all get binary 111 = read, write, and execute permissions. This is a security risk because any user on the system -- or any process running as any user -- can overwrite, delete, or execute the file. For a web server script, external users interacting with the web server process should generally only be able to read and execute (not write) the script. A safer value would be 755: owner gets rwx (7), group and others get r-x (5) -- they can read and run the script but cannot modify it.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-1.5": {
        "unit": "tp-1.5",
        "title": "Storage Units",
        "n10_009": "FC0-U71 1.3",
        "n10_008": "FC0-U71 1.3",
        "questions": [
            {
                "num": "1",
                "question": "The smallest unit of digital data is the _______, which holds a single binary value (0 or 1). Eight bits make one _______. A _______ stores 1,024 bytes, and a _______ stores 1,024 kilobytes.",
                "answer": "Bit; byte; kilobyte (KB); megabyte (MB).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Fill in the storage unit table:\n    1 KB = _______ bytes\n    1 MB = _______ KB\n    1 GB = _______ MB\n    1 TB = _______ GB",
                "answer": "1 KB = 1,024 bytes; 1 MB = 1,024 KB; 1 GB = 1,024 MB; 1 TB = 1,024 GB.",
                "lines": 4
            },
            {
                "num": "3",
                "question": "Hard drive manufacturers advertise storage using the _______ (decimal/binary) definition where 1 GB = 1,000,000,000 bytes. Operating systems measure storage using the _______ (decimal/binary) definition where 1 GB = 1,073,741,824 bytes. This is why a 500 GB drive appears as approximately _______ GB in Windows File Explorer.",
                "answer": "Decimal; binary; approximately 465 GB.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "A short text message is approximately 160 _______ (bits/bytes). A typical MP3 song file is around 4 to 5 _______. A 4K movie might be 50 to 100 _______. Choose the correct unit for each: bits, bytes, megabytes, gigabytes.",
                "answer": "Bytes (characters); megabytes (MB); gigabytes (GB).",
                "lines": 3
            },
            {
                "num": "5",
                "question": "_______ is the space used to run programs and store data while the computer is on (RAM). _______ is the space used to permanently save files, programs, and the OS (hard drive/SSD). The key difference is that memory is _______ (lost when power is off) while storage is _______.",
                "answer": "Memory (RAM); storage (hard drive / SSD); volatile; non-volatile (persistent).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "A file is 750 MB. A flash drive has 1 GB of free space. Will the file fit? Show your reasoning:\n    1 GB = _______ MB\n    750 MB _______ (is/is not) less than 1,024 MB\n    Conclusion: the file _______ fit on the drive.",
                "answer": "1 GB = 1,024 MB; 750 MB is less than 1,024 MB; the file will fit on the drive.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "When choosing appropriate storage units, match each description to the correct unit:\n    A single character of text: _______\n    A Word document (5 pages): _______\n    A smartphone photo: _______\n    A Blu-ray movie: _______",
                "answer": "A character: 1 byte; Word document: approximately 30-50 KB; smartphone photo: 3-8 MB; Blu-ray movie: 25-50 GB.",
                "lines": 4
            },
            {
                "num": "8",
                "question": "REAL WORLD: A student buys an external hard drive advertised as 2 TB. When they plug it in, Windows shows only 1.81 TB of usable space. The student believes they were sold a defective or undersized drive and wants to return it. Explain what is actually happening, using the decimal vs. binary definition of gigabyte, and whether the drive is defective.",
                "answer": "The drive is not defective -- this is expected behavior caused by the difference between decimal and binary storage definitions. The manufacturer defines 2 TB as 2,000,000,000,000 bytes (decimal, powers of 10). Windows measures storage in binary units where 1 TB = 1,099,511,627,776 bytes. Dividing 2,000,000,000,000 by 1,099,511,627,776 gives approximately 1.818 TB as shown by Windows. No data capacity has been lost -- it is simply a unit definition difference. The student should not return the drive.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-1.6": {
        "unit": "tp-1.6",
        "title": "Transfer Rates",
        "n10_009": "FC0-U71 1.3",
        "n10_008": "FC0-U71 1.3",
        "questions": [
            {
                "num": "1",
                "question": "Network and connection speeds are measured in _______ per second (lowercase b), while file sizes are measured in _______ (uppercase B). To convert from Mbps to MB/s, you divide by _______. A 100 Mbps internet connection transfers data at _______ MB/s.",
                "answer": "Megabits (Mbps); megabytes (MB); 8; 12.5 MB/s.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "USB 2.0 has a maximum transfer speed of _______ Mbps. USB 3.0 has a maximum of _______ Gbps. USB 3.0 is approximately _______ times faster than USB 2.0. USB 3.0 ports are typically identified by their _______ color inside the port.",
                "answer": "480 Mbps; 5 Gbps; approximately 10 times faster; blue.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Calculate how long it would take to transfer a 1 GB file over a USB 2.0 connection at a sustained 480 Mbps:\n    Convert speed to MB/s: 480 Mbps / 8 = _______ MB/s\n    1 GB = _______ MB\n    Time = 1,024 / _______ = approximately _______ seconds",
                "answer": "60 MB/s; 1,024 MB; 1,024 / 60 = approximately 17 seconds.",
                "lines": 4
            },
            {
                "num": "4",
                "question": "_______ refers to the maximum theoretical data transfer capacity of a connection, usually measured in Mbps or Gbps. _______ is the actual measured data transfer rate achieved in real conditions, which is always _______ (greater/less) than the theoretical maximum due to overhead and interference.",
                "answer": "Bandwidth; throughput; less.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "_______ is the delay between when a signal is sent and when it is received, measured in milliseconds (ms). It does not affect _______ (how much data per second) but affects how responsive a connection feels. High latency causes noticeable delays in _______ gaming, video calls, and remote desktop sessions.",
                "answer": "Latency; bandwidth (throughput); online.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "An ISP advertises an internet plan as 500 Mbps download. A user downloading a file notices the download progress bar shows around 60 MB/s. Is this accurate or is there a problem? Show the conversion:\n    500 Mbps / 8 = _______ MB/s\n    60 MB/s is _______ (above/below/at) the theoretical maximum.",
                "answer": "500 / 8 = 62.5 MB/s. 60 MB/s is slightly below the theoretical maximum -- this is normal due to protocol overhead. No problem.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Mbps stands for _______ per second. MBps stands for _______ per second. The difference is _______ times larger. Internet service providers advertise in _______ (Mbps/MBps) while download managers typically display progress in _______ (Mbps/MBps).",
                "answer": "Megabits; megabytes; 8 times; Mbps; MBps (MB/s).",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A student is downloading a 4 GB game on a home internet connection advertised at 200 Mbps. Their download client shows the download speed fluctuating between 15 MB/s and 20 MB/s, averaging about 18 MB/s. They expect much faster speeds based on the 200 Mbps advertisement. Explain why actual speed is lower and calculate the expected download time at 18 MB/s.",
                "answer": "The 200 Mbps advertisement is the maximum theoretical bandwidth. Converting: 200 Mbps / 8 = 25 MB/s theoretical maximum. Actual speeds are lower due to: network congestion at the ISP, protocol overhead (TCP headers, acknowledgments), Wi-Fi signal strength or interference if not on wired Ethernet, and server-side upload limits. 18 MB/s is approximately 72% of the theoretical max -- a reasonable real-world figure. Download time: 4 GB = 4,096 MB. 4,096 / 18 MB/s = approximately 228 seconds, or about 3.8 minutes.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-1.7": {
        "unit": "tp-1.7",
        "title": "Processing Speed",
        "n10_009": "FC0-U71 1.3",
        "n10_008": "FC0-U71 1.3",
        "questions": [
            {
                "num": "1",
                "question": "Hz stands for _______ and represents one cycle per second. GHz stands for _______ and equals _______ cycles per second. A CPU running at 3.6 GHz completes approximately _______ billion instruction cycles per second.",
                "answer": "Hertz; gigahertz; 1,000,000,000 (one billion); 3.6 billion.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Clock speed _______ (always/does not always) determine overall CPU performance. A CPU running single-threaded workloads benefits from _______ clock speed, while tasks that can be divided into parallel work benefit from more _______ even at lower clock speeds.",
                "answer": "Does not always; higher; cores.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "A multi-core CPU has multiple _______ on a single chip, each able to execute instructions _______ (sequentially/independently). A 4-core CPU can technically work on _______ different tasks at the same time, improving _______ when running multiple programs simultaneously.",
                "answer": "Cores; independently; 4; multitasking (throughput).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "CPU cache is ultra-fast memory built directly into the processor. _______ cache is the smallest and fastest, closest to the core. _______ cache is shared within a core and slightly larger. _______ cache is the largest and shared among all cores. Cache reduces how often the CPU must wait for data from _______, which is much slower.",
                "answer": "L1; L2; L3; RAM (main memory).",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Thermal throttling occurs when a CPU reaches its maximum safe _______ and automatically reduces its _______ to generate less heat. While this prevents hardware damage, it results in _______ performance. The long-term fix is to improve _______ or reapply thermal paste.",
                "answer": "Temperature; clock speed; reduced (degraded); cooling.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "A _______ is a standardized test used to measure and compare CPU, GPU, or system performance. The score allows comparisons between different hardware. However, benchmark results _______ (always/do not always) reflect real-world performance for every type of workload.",
                "answer": "Benchmark; do not always.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Hyper-Threading (Intel) and SMT (AMD) allow each physical CPU core to handle _______ threads simultaneously. A 4-core CPU with hyper-threading appears to the OS as _______ logical processors. This improves performance when the CPU has _______ work waiting than physical cores to run it.",
                "answer": "Two; 8 logical processors; more.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A student is choosing between two laptops. Laptop A has a 4-core CPU at 4.0 GHz. Laptop B has an 8-core CPU at 2.8 GHz. The student assumes Laptop A is faster because it has a higher clock speed. For which tasks would Laptop A actually perform better, and for which would Laptop B perform better? Explain your reasoning.",
                "answer": "Laptop A (4-core, 4.0 GHz) performs better on single-threaded tasks -- those that cannot be parallelized -- such as older games that rely on one CPU core, some legacy applications, and tasks where instructions must run sequentially. The higher clock speed means each individual core completes cycles faster. Laptop B (8-core, 2.8 GHz) performs better on multi-threaded workloads such as video rendering, compiling code, running multiple virtual machines, streaming while gaming, and modern games optimized for many cores. The lower clock speed is offset by having twice as many cores working in parallel. A higher GHz number alone does not make a CPU faster for all tasks.",
                "real_world": True,
                "lines": 7
            }
        ]
    },
    "tp-1.8": {
        "unit": "tp-1.8",
        "title": "Troubleshooting Methodology",
        "n10_009": "FC0-U71 1.4",
        "n10_008": "FC0-U71 1.4",
        "questions": [
            {
                "num": "1",
                "question": "The CompTIA troubleshooting methodology has _______ steps. Step 1 is _______. Step 2 is _______. Step 3 is _______. Skipping steps -- especially jumping from Step 1 directly to implementing a fix -- often results in _______ the wrong problem.",
                "answer": "7; identify the problem; establish a theory of probable cause; test the theory; solving (fixing).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "In Step 1 (identify the problem), a technician should ask _______ -ended questions (e.g., 'What happens when you turn it on?') rather than _______ questions (e.g., 'Does it turn on?'). Open questions gather _______ detail and lead to better theories in Step 2.",
                "answer": "Open; closed; more.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Step 4 is to establish a/an _______ of action to resolve the problem, including identifying potential _______ of the planned fix. This prevents a technician from solving one problem while creating another. Step 5 is to _______ the solution and then _______ full system functionality.",
                "answer": "Plan; effects (side effects); implement; verify.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Step 6 is to _______ findings, actions, and outcomes. This creates a reference for future similar issues and protects the technician legally if decisions are later questioned. Step 7 is to _______ the user -- explaining what caused the problem and how to prevent it in plain language.",
                "answer": "Document; educate.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "The distinction between a _______ (what the user reports, e.g., 'the screen is black') and a _______ (the actual technical cause, e.g., 'the GPU is unseated') is critical. Fixing a symptom without identifying the _______ will result in the problem _______.",
                "answer": "Symptom; root cause; root cause; recurring (returning).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "When testing a theory in Step 3 and the theory is _______, the technician should either establish a new theory or _______ to a higher skill level. Before escalating, the technician should document _______ steps already tried so the next technician does not repeat them.",
                "answer": "Disproved (not confirmed); escalate; all.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "When questioning a user in Step 1, a technician should ask whether any _______ were made recently -- such as software updates, new hardware, or changed settings. These changes are often the _______ of sudden failures. The technician should also reproduce the problem if possible to _______.",
                "answer": "Changes; cause (trigger); confirm the symptom (verify it themselves).",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A technician skips steps and immediately reinstalls the OS on a laptop with a reported display problem, which takes 3 hours and does not fix the issue. The actual cause was a loose display cable. Identify which troubleshooting steps were skipped, explain what the correct process would have been, and describe the cost of skipping the methodology.",
                "answer": "Skipped steps: 2 (establish theory -- no investigation of probable hardware causes), 3 (test the theory -- no attempt to test with external monitor or check the cable), and 4 (establish a plan -- no consideration of less disruptive fixes first). Correct process: identify symptom (display issue); theory = loose cable or driver issue; test = connect to external monitor. If the external works, the problem is the display panel/cable, not the OS. A 2-minute cable re-seat would have fixed it. Cost of skipping: 3 hours of unnecessary work, loss of user data (if any), user frustration, and the actual problem still unfixed.",
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