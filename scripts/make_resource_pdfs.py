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
    """'1.1.1', 'OSI Model' → '1.1.1-osi-model'"""
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

    story.append(Paragraph(f"{title} — Guided Notes", S['title']))
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
            story.append(Paragraph(f"Question {num} — Real World Application", S['real_world_label']))
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
    print(f'  ✓ Guided notes: {outpath}')


def build_answer_key(outpath, unit_data):
    S = make_styles()
    unit = unit_data['unit']
    title = unit_data['title']
    questions = unit_data['questions']

    doc = SimpleDocTemplate(outpath, pagesize=letter,
        leftMargin=inch, rightMargin=inch,
        topMargin=0.85*inch, bottomMargin=0.85*inch)
    story = []

    story.append(Paragraph(f"{title} — Guided Notes ANSWER KEY", S['title']))
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
            story.append(Paragraph(f"Question {num} — Real World Application", S['real_world_label']))
        else:
            story.append(Paragraph(f"Question {num}", S['question_num']))

        q_text = q['question'].replace('\n', '<br/>')
        story.append(Paragraph(q_text, S['question']))
        story.append(Paragraph(f"Answer: {q['answer']}", S['answer']))

    doc.build(story)
    print(f'  ✓ Answer key:   {outpath}')


# ── PROCESS ONE UNIT ──────────────────────────────────────────────────────────

def process_unit(unit_data, output_root='public/resources/network-engineer'):
    unit = unit_data['unit']
    title = unit_data['title']
    slug = unit_to_slug(unit, title)
    out_dir = Path(output_root) / slug
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f'\nUnit {unit} — {title}')
    build_guided_notes(str(out_dir / f'{slug}-guided-notes.pdf'), unit_data)
    build_answer_key(str(out_dir / f'{slug}-answer-key.pdf'), unit_data)


# ── BUILT-IN UNIT DATA ─────────────────────────────────────────────────────────
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
                "answer": "Seven (7) layers — Physical at the bottom, Application at the top.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Layer 1 devices — such as hubs, repeaters, and _______ — deal only with raw _______ and have no understanding of addresses or protocols.",
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
                "answer": "Layers 1-3 are working (ping to external IP succeeds). The problem is at Layer 7 (Application) — specifically DNS. The computer can reach the internet by IP but cannot resolve domain names. Check DNS configuration with nslookup; correct or replace the DNS server address.",
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
                "question": "When data travels down the OSI model on its way out of a device, each layer adds its own _______. This process is called _______. At the destination, each layer _______ its own header in reverse — a process called _______.",
                "answer": "Header (and sometimes trailer); encapsulation; strips; decapsulation.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Match each header type to the OSI layer that adds it:\n    Port numbers and TCP/UDP info  →  Layer _______\n    Source and destination IP addresses  →  Layer _______\n    MAC addresses and CRC trailer  →  Layer _______",
                "answer": "Port numbers/TCP/UDP → Layer 4 (Transport); IP addresses → Layer 3 (Network); MAC addresses/CRC → Layer 2 (Data Link).",
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
                "answer": "TCP is reliable and connection-oriented — it guarantees delivery and retransmits lost data (e.g., web browsing, file downloads). UDP is connectionless and fast — no retransmission, used where speed matters more than perfection (e.g., Discord voice calls, live game state updates, DNS lookups).",
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
                "answer": "Normal handshake: (1) SYN from client; (2) SYN-ACK from server; (3) ACK from client — connection established. Hundreds of SYNs with no SYN-ACK = SYN flood attack. Attacker overwhelms the server with half-open connections, exhausting its connection table.",
                "real_world": True,
                "lines": 6
            }
        ]
    }
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