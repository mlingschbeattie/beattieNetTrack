"""
Generate guided notes and answer key PDFs for BeattieNetTrack resources.
Unit 1.1.1 - OSI Model
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

W, H = letter

# ── STYLES ────────────────────────────────────────────────────────────────────

def make_styles():
    base = getSampleStyleSheet()

    title = ParagraphStyle(
        'DocTitle',
        parent=base['Title'],
        fontSize=16,
        textColor=colors.HexColor('#0f1829'),
        spaceAfter=4,
    )
    subtitle = ParagraphStyle(
        'Subtitle',
        parent=base['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#38bdf8'),
        spaceBefore=0,
        spaceAfter=2,
    )
    meta = ParagraphStyle(
        'Meta',
        parent=base['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#7a90b8'),
        spaceAfter=12,
    )
    instruction = ParagraphStyle(
        'Instruction',
        parent=base['Italic'],
        fontSize=9,
        textColor=colors.HexColor('#4a6180'),
        spaceAfter=16,
    )
    question_num = ParagraphStyle(
        'QuestionNum',
        parent=base['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#38bdf8'),
        fontName='Helvetica-Bold',
        spaceBefore=14,
        spaceAfter=2,
    )
    question = ParagraphStyle(
        'Question',
        parent=base['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#0f1829'),
        leading=15,
        spaceAfter=4,
    )
    answer = ParagraphStyle(
        'Answer',
        parent=base['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#166534'),  # dark green
        leading=15,
        spaceAfter=4,
        fontName='Helvetica-Oblique',
    )
    real_world_label = ParagraphStyle(
        'RWLabel',
        parent=base['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#f97316'),
        fontName='Helvetica-Bold',
        spaceBefore=14,
        spaceAfter=2,
    )
    footer = ParagraphStyle(
        'Footer',
        parent=base['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#7a90b8'),
        alignment=TA_CENTER,
    )
    wget_style = ParagraphStyle(
        'Wget',
        parent=base['Code'],
        fontSize=9,
        textColor=colors.HexColor('#22c55e'),
        backColor=colors.HexColor('#0f1829'),
        borderPadding=(6, 8, 6, 8),
        spaceAfter=8,
        spaceBefore=8,
    )

    return {
        'title': title, 'subtitle': subtitle, 'meta': meta,
        'instruction': instruction, 'question_num': question_num,
        'question': question, 'answer': answer,
        'real_world_label': real_world_label,
        'footer': footer, 'wget': wget_style,
    }


# ── QUESTIONS DATA ─────────────────────────────────────────────────────────────

QUESTIONS = [
    {
        'num': '1',
        'text': 'The OSI model divides network communication into _______ layers, '
                'from the _______ layer at the bottom to the _______ layer at the top.',
        'answer': 'Seven (7) layers — Physical at the bottom, Application at the top.',
        'rw': False,
    },
    {
        'num': '2',
        'text': 'Layer 1 devices — such as hubs, repeaters, and _______ — deal only '
                'with raw _______ and have no understanding of addresses or protocols.',
        'answer': 'Network interface cards (NICs); raw bits (electrical signals, light pulses, or radio waves).',
        'rw': False,
    },
    {
        'num': '3',
        'text': 'A switch operates at Layer _______ and uses _______ addresses to '
                'forward frames to the correct port, rather than flooding traffic '
                'to every device like a hub.',
        'answer': 'Layer 2 (Data Link); MAC addresses.',
        'rw': False,
    },
    {
        'num': '4',
        'text': 'Explain the difference between a MAC address and an IP address. '
                'Which OSI layer is each one associated with?',
        'answer': 'A MAC address is a hardware address used at Layer 2 (Data Link) '
                  'to deliver frames on a local network. An IP address is a logical '
                  'address used at Layer 3 (Network) to route packets across different '
                  'networks. MAC = local delivery; IP = internet routing.',
        'rw': False,
    },
    {
        'num': '5',
        'text': 'At Layer 4, the two main transport protocols are _______ and _______. '
                'The first provides reliable, ordered delivery; the second prioritizes '
                '_______ over reliability.',
        'answer': 'TCP (Transmission Control Protocol) and UDP (User Datagram Protocol); speed.',
        'rw': False,
    },
    {
        'num': '6',
        'text': 'Port numbers exist at Layer _______. They allow a single device with '
                'one IP address to run multiple _______ simultaneously (for example, '
                'a web server and an SSH daemon on the same machine).',
        'answer': 'Layer 4 (Transport); services (or applications).',
        'rw': False,
    },
    {
        'num': '7',
        'text': 'When a browser negotiates a TLS connection to load an HTTPS website, '
                'which OSI layer handles that encryption setup? _______',
        'answer': 'Layer 6 (Presentation).',
        'rw': False,
    },
    {
        'num': '8',
        'text': 'REAL WORLD: A user reports that they can ping 8.8.8.8 successfully '
                'but cannot load any websites in their browser. Based on the OSI model, '
                'which layer(s) would you investigate first, and what specific service '
                'is most likely the cause? Explain your reasoning in two to three sentences.',
        'answer': 'Layers 1-3 are working (ping to external IP succeeds). The problem '
                  'is at Layer 7 (Application) — specifically DNS. The computer can '
                  'reach the internet by IP but cannot resolve domain names. Check DNS '
                  'configuration with nslookup; correct or replace the DNS server address.',
        'rw': True,
    },
]

WGET_LINE = 'wget http://[SERVER]/resources/network-engineer/1.1.1-osi-model/osi-answer-key.pdf'


# ── BUILD PDFs ─────────────────────────────────────────────────────────────────

def build_guided_notes(outpath):
    S = make_styles()
    doc = SimpleDocTemplate(
        outpath, pagesize=letter,
        leftMargin=inch, rightMargin=inch,
        topMargin=0.85*inch, bottomMargin=0.85*inch,
    )
    story = []

    # Header
    story.append(Paragraph('OSI Model — Guided Notes', S['title']))
    story.append(Paragraph('Unit 1.1.1  |  CompTIA Network+ N10-009 Objective 1.1  |  N10-008 1.1', S['subtitle']))
    story.append(Paragraph('Name: ___________________________________  Date: ____________  Period: ______', S['meta']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#162035'), spaceAfter=10))
    story.append(Paragraph(
        'Complete each question using the lesson reading. '
        'Write in the blank or answer in one to two sentences.',
        S['instruction']
    ))

    # Questions
    for q in QUESTIONS:
        if q['rw']:
            story.append(Paragraph(f"Question {q['num']} — Real World Application", S['real_world_label']))
        else:
            story.append(Paragraph(f"Question {q['num']}", S['question_num']))
        story.append(Paragraph(q['text'], S['question']))
        # Answer space (3 blank lines for short answer, more for #4 and #8)
        lines = 3 if q['num'] not in ('4', '8') else 5
        for _ in range(lines):
            story.append(HRFlowable(
                width='100%', thickness=0.5,
                color=colors.HexColor('#d1d5db'),
                spaceBefore=10, spaceAfter=2,
            ))

    # Wget line
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#162035'), spaceAfter=10))
    story.append(Paragraph('Download the answer key from the class server:', S['instruction']))
    story.append(Paragraph(WGET_LINE, S['wget']))

    doc.build(story)
    print(f'  Written: {outpath}')


def build_answer_key(outpath):
    S = make_styles()
    doc = SimpleDocTemplate(
        outpath, pagesize=letter,
        leftMargin=inch, rightMargin=inch,
        topMargin=0.85*inch, bottomMargin=0.85*inch,
    )
    story = []

    # Header
    story.append(Paragraph('OSI Model — Guided Notes ANSWER KEY', S['title']))
    story.append(Paragraph('Unit 1.1.1  |  CompTIA Network+ N10-009 Objective 1.1  |  N10-008 1.1', S['subtitle']))
    story.append(Paragraph('For instructor use / distribute after students complete the notes.', S['meta']))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#162035'), spaceAfter=10))

    # Questions + answers
    for q in QUESTIONS:
        if q['rw']:
            story.append(Paragraph(f"Question {q['num']} — Real World Application", S['real_world_label']))
        else:
            story.append(Paragraph(f"Question {q['num']}", S['question_num']))
        story.append(Paragraph(q['text'], S['question']))
        story.append(Paragraph(f"Answer: {q['answer']}", S['answer']))

    doc.build(story)
    print(f'  Written: {outpath}')


# ── MAIN ───────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    import os
    out = '/tmp/beattie_output/resources/network-engineer/1.1.1-osi-model'
    os.makedirs(out, exist_ok=True)

    print('Building PDFs...')
    build_guided_notes(f'{out}/osi-guided-notes.pdf')
    build_answer_key(f'{out}/osi-answer-key.pdf')
    print('Done.')
