"""
Generate guided notes and answer key PDFs for BeattieNetTrack resources.
Unit 1.1.2 - Encapsulation and Decapsulation
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_CENTER

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
            fontSize=10, textColor=colors.HexColor('#0f1829'), leading=15, spaceAfter=4),
        'answer': ParagraphStyle('Answer', parent=base['Normal'],
            fontSize=10, textColor=colors.HexColor('#166534'), leading=15,
            spaceAfter=4, fontName='Helvetica-Oblique'),
        'real_world_label': ParagraphStyle('RWLabel', parent=base['Normal'],
            fontSize=10, textColor=colors.HexColor('#f97316'),
            fontName='Helvetica-Bold', spaceBefore=14, spaceAfter=2),
        'wget': ParagraphStyle('Wget', parent=base['Code'],
            fontSize=9, textColor=colors.HexColor('#22c55e'),
            backColor=colors.HexColor('#0f1829'),
            borderPadding=(6, 8, 6, 8), spaceAfter=8, spaceBefore=8),
    }

QUESTIONS = [
    {
        'num': '1',
        'text': 'When data travels down the OSI model on its way out of a device, '
                'each layer adds its own _______. This process is called _______. '
                'At the destination, each layer _______ its own header in reverse — '
                'a process called _______.',
        'answer': 'Header (and sometimes trailer); encapsulation; strips; decapsulation.',
        'rw': False, 'lines': 3,
    },
    {
        'num': '2',
        'text': 'Match each header type to the OSI layer that adds it:\n'
                '    Port numbers and TCP/UDP info  →  Layer _______\n'
                '    Source and destination IP addresses  →  Layer _______\n'
                '    MAC addresses and CRC trailer  →  Layer _______',
        'answer': 'Port numbers/TCP/UDP → Layer 4 (Transport); '
                  'IP addresses → Layer 3 (Network); '
                  'MAC addresses/CRC → Layer 2 (Data Link).',
        'rw': False, 'lines': 4,
    },
    {
        'num': '3',
        'text': 'TCP establishes a connection using a _______ handshake. '
                'The three steps are: _______ (sender initiates), '
                '_______ (receiver acknowledges), and _______ (sender confirms).',
        'answer': 'Three-way handshake; SYN; SYN-ACK; ACK.',
        'rw': False, 'lines': 3,
    },
    {
        'num': '4',
        'text': 'Explain the key difference between TCP and UDP. '
                'Give one real-world application that uses each protocol and explain why.',
        'answer': 'TCP is reliable and connection-oriented — it guarantees delivery '
                  'and retransmits lost data (e.g., web browsing, file downloads). '
                  'UDP is connectionless and fast — no retransmission, used where '
                  'speed matters more than perfection (e.g., Discord voice calls, '
                  'live game state updates, DNS lookups).',
        'rw': False, 'lines': 5,
    },
    {
        'num': '5',
        'text': 'List the purpose of three TCP flags:\n'
                '    SYN: _______\n'
                '    FIN: _______\n'
                '    RST: _______',
        'answer': 'SYN: initiates a connection; '
                  'FIN: gracefully closes a connection; '
                  'RST: immediately terminates a connection with no negotiation.',
        'rw': False, 'lines': 4,
    },
    {
        'num': '6',
        'text': 'At Layer 2, the Data Link layer wraps a packet into a _______. '
                'It adds a _______ with MAC addresses and a _______ containing '
                'a CRC value called the _______. If the CRC check fails at the '
                'receiving end, the frame is _______.',
        'answer': 'Frame; header; trailer; Frame Check Sequence (FCS); dropped silently.',
        'rw': False, 'lines': 3,
    },
    {
        'num': '7',
        'text': 'The MTU (Maximum Transmission Unit) on standard Ethernet is _______ bytes. '
                'If data exceeds this limit, it gets _______ into smaller pieces. '
                'Why can VPN tunnels cause MTU-related connectivity problems?',
        'answer': '1500 bytes; fragmented. VPN tunnels add their own encapsulation '
                  'headers on top of existing ones, reducing the available payload '
                  'space. If the resulting packet exceeds the path MTU and the '
                  'Don\'t Fragment bit is set, the packet is dropped — causing '
                  'large transfers to stall while pings still work.',
        'rw': False, 'lines': 4,
    },
    {
        'num': '8',
        'text': 'REAL WORLD: You open Wireshark on a machine and capture traffic '
                'while loading a webpage. Describe what a normal TCP connection '
                'setup looks like in the capture. What three-packet sequence would '
                'you see at the start, and what flags would each packet have? '
                'What would it mean if you saw hundreds of SYN packets but no '
                'SYN-ACK responses?',
        'answer': 'Normal setup: (1) SYN from client — initiates connection; '
                  '(2) SYN-ACK from server — acknowledges and responds; '
                  '(3) ACK from client — confirms, connection established. '
                  'Hundreds of SYN packets with no SYN-ACK responses indicate '
                  'a SYN flood attack — a denial-of-service technique where the '
                  'attacker overwhelms the server with half-open connections, '
                  'exhausting its connection table.',
        'rw': True, 'lines': 6,
    },
]

WGET_LINE = 'wget http://[SERVER]/resources/network-engineer/1.1.2-encapsulation/encapsulation-answer-key.pdf'


def build_guided_notes(outpath):
    S = make_styles()
    doc = SimpleDocTemplate(outpath, pagesize=letter,
        leftMargin=inch, rightMargin=inch,
        topMargin=0.85*inch, bottomMargin=0.85*inch)
    story = []

    story.append(Paragraph('Encapsulation &amp; Decapsulation — Guided Notes', S['title']))
    story.append(Paragraph('Unit 1.1.2  |  CompTIA Network+ N10-009 Obj. 1.1  |  N10-008 1.1', S['subtitle']))
    story.append(Paragraph('Name: ___________________________________  Date: ____________  Period: ______', S['meta']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#162035'), spaceAfter=10))
    story.append(Paragraph(
        'Complete each question using the lesson reading. '
        'Write in the blank or answer in the space provided.',
        S['instruction']))

    for q in QUESTIONS:
        if q['rw']:
            story.append(Paragraph(f"Question {q['num']} — Real World Application", S['real_world_label']))
        else:
            story.append(Paragraph(f"Question {q['num']}", S['question_num']))
        # Preserve line breaks in question text
        q_text = q['text'].replace('\n', '<br/>')
        story.append(Paragraph(q_text, S['question']))
        for _ in range(q['lines']):
            story.append(HRFlowable(width='100%', thickness=0.5,
                color=colors.HexColor('#d1d5db'), spaceBefore=10, spaceAfter=2))

    story.append(Spacer(1, 20))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#162035'), spaceAfter=10))
    story.append(Paragraph('Download the answer key from the class server:', S['instruction']))
    story.append(Paragraph(WGET_LINE, S['wget']))

    doc.build(story)
    print(f'  Written: {outpath}')


def build_answer_key(outpath):
    S = make_styles()
    doc = SimpleDocTemplate(outpath, pagesize=letter,
        leftMargin=inch, rightMargin=inch,
        topMargin=0.85*inch, bottomMargin=0.85*inch)
    story = []

    story.append(Paragraph('Encapsulation &amp; Decapsulation — Guided Notes ANSWER KEY', S['title']))
    story.append(Paragraph('Unit 1.1.2  |  CompTIA Network+ N10-009 Obj. 1.1  |  N10-008 1.1', S['subtitle']))
    story.append(Paragraph('For instructor use / distribute after students complete the notes.', S['meta']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#162035'), spaceAfter=10))

    for q in QUESTIONS:
        if q['rw']:
            story.append(Paragraph(f"Question {q['num']} — Real World Application", S['real_world_label']))
        else:
            story.append(Paragraph(f"Question {q['num']}", S['question_num']))
        q_text = q['text'].replace('\n', '<br/>')
        story.append(Paragraph(q_text, S['question']))
        story.append(Paragraph(f"Answer: {q['answer']}", S['answer']))

    doc.build(story)
    print(f'  Written: {outpath}')


if __name__ == '__main__':
    import os
    out = '/tmp/beattie_112/resources/network-engineer/1.1.2-encapsulation'
    os.makedirs(out, exist_ok=True)
    print('Building PDFs...')
    build_guided_notes(f'{out}/encapsulation-guided-notes.pdf')
    build_answer_key(f'{out}/encapsulation-answer-key.pdf')
    print('Done.')
