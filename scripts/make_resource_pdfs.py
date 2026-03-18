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