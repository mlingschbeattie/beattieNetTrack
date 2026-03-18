"""
extract_units_from_pdfs.py

Reads every answer-key PDF in public/resources/network-engineer/
and extracts questions + answers into UNITS dict entries ready to
paste into make_resource_pdfs.py.

Usage (run from repo root):
    python3 scripts/extract_units_from_pdfs.py

Output: scripts/extracted_units.py  — paste its contents into
        the UNITS dict in make_resource_pdfs.py
"""

import re
import sys
from pathlib import Path

try:
    from pdfminer.high_level import extract_text
except ImportError:
    print("ERROR: pdfminer.six not installed.")
    print("Run: pip install pdfminer.six --break-system-packages")
    sys.exit(1)


RESOURCES_ROOT = Path("public/resources/network-engineer")
OUTPUT_FILE = Path("scripts/extracted_units.py")


def slug_to_unit(slug):
    """'4-1-1-network-security-concepts' -> '4.1.1'"""
    parts = slug.split("-")
    # Find the numeric prefix (e.g. 4, 1, 1)
    num_parts = []
    for p in parts:
        if p.isdigit():
            num_parts.append(p)
        else:
            break
    return ".".join(num_parts)


def slug_to_title(slug):
    """'4-1-1-network-security-concepts' -> 'Network Security Concepts'"""
    parts = slug.split("-")
    # Skip leading numeric parts
    text_parts = []
    skipping_nums = True
    for p in parts:
        if skipping_nums and p.isdigit():
            continue
        skipping_nums = False
        text_parts.append(p)
    return " ".join(text_parts).title()


def extract_questions(text):
    """
    Parse PDF text into list of dicts with keys:
      num, question, answer, real_world
    """
    questions = []

    # Split on "Question N" or "Question N — Real World..."
    # The PDF uses "Question 1", "Question 2 — Real World Application", etc.
    pattern = re.compile(
        r'Question\s+(\d+)(?:\s*[—–-]\s*Real World[^\n]*)?\n',
        re.IGNORECASE
    )

    chunks = pattern.split(text)
    # chunks: [preamble, num, body, num, body, ...]

    i = 1
    while i < len(chunks) - 1:
        num = chunks[i].strip()
        body = chunks[i + 1].strip()
        i += 2

        # Check if this was a real world question (look back at original)
        is_rw = bool(re.search(
            r'Question\s+' + re.escape(num) + r'\s*[—–-]\s*Real World',
            text, re.IGNORECASE
        ))

        # Split question from answer on "Answer:" line
        answer_match = re.search(r'\nAnswer:\s*', body, re.IGNORECASE)
        if answer_match:
            question_text = body[:answer_match.start()].strip()
            answer_text = body[answer_match.end():].strip()
            # Trim answer at next Question block or end
            next_q = re.search(r'\nQuestion\s+\d+', answer_text)
            if next_q:
                answer_text = answer_text[:next_q.start()].strip()
        else:
            question_text = body.strip()
            answer_text = ""

        # Clean up whitespace artifacts from PDF extraction
        question_text = re.sub(r'\n+', '\n', question_text).strip()
        answer_text = re.sub(r'\n+', ' ', answer_text).strip()

        # Estimate lines needed based on answer length
        words = len(answer_text.split())
        if words > 80:
            lines = 7
        elif words > 50:
            lines = 6
        elif words > 30:
            lines = 5
        elif words > 20:
            lines = 4
        elif is_rw:
            lines = 6
        else:
            lines = 3

        questions.append({
            "num": num,
            "question": question_text,
            "answer": answer_text,
            "real_world": is_rw,
            "lines": lines,
        })

    return questions


def unit_to_dict_entry(unit_num, title, n10_009, n10_008, questions):
    """Render a single UNITS entry as a Python string."""
    lines = []
    lines.append(f'    "{unit_num}": {{')
    lines.append(f'        "unit": "{unit_num}",')
    lines.append(f'        "title": "{title}",')
    lines.append(f'        "n10_009": "{n10_009}",')
    lines.append(f'        "n10_008": "{n10_008}",')
    lines.append(f'        "questions": [')

    for q in questions:
        q_text = q["question"].replace('"', '\\"').replace('\n', '\\n    ')
        a_text = q["answer"].replace('"', '\\"')
        lines.append(f'            {{')
        lines.append(f'                "num": "{q["num"]}",')
        lines.append(f'                "question": "{q_text}",')
        lines.append(f'                "answer": "{a_text}",')
        if q["real_world"]:
            lines.append(f'                "real_world": True,')
        lines.append(f'                "lines": {q["lines"]}')
        lines.append(f'            }},')

    lines.append(f'        ]')
    lines.append(f'    }},')
    return "\n".join(lines)


def guess_objectives(unit_num):
    """Best-guess N10-009 and N10-008 objective from unit number."""
    major = unit_num.split(".")[0]
    mapping = {
        "1": ("1.1", "1.1"),
        "2": ("2.1", "2.1"),
        "3": ("3.1", "3.1"),
        "4": ("4.1", "4.1"),
        "5": ("5.1", "5.1"),
    }
    # More specific mappings
    specific = {
        "1.1": ("1.1", "1.1"),
        "1.2": ("1.2", "1.2"),
        "1.3": ("1.3", "1.3"),
        "1.4": ("1.4", "1.4"),
        "1.5": ("1.5", "1.5"),
        "1.6": ("1.6", "1.6"),
        "1.7": ("1.7", "1.7"),
        "1.8": ("1.8", "1.8"),
        "2.1": ("2.1", "2.1"),
        "2.2": ("2.2", "2.2"),
        "2.3": ("2.3", "2.3"),
        "3.1": ("3.1", "3.1"),
        "3.2": ("3.2", "3.2"),
        "3.3": ("3.3", "3.3"),
        "4.1": ("4.1", "4.1"),
        "4.2": ("4.2", "4.2"),
        "4.3": ("4.3", "4.3"),
        "4.4": ("4.4", "4.4"),
        "5.1": ("5.1", "5.1"),
        "5.2": ("5.2", "5.2"),
        "5.3": ("5.3", "5.3"),
    }
    prefix = ".".join(unit_num.split(".")[:2])
    return specific.get(prefix, mapping.get(major, ("1.1", "1.1")))


def main():
    if not RESOURCES_ROOT.exists():
        print(f"ERROR: {RESOURCES_ROOT} not found. Run from repo root.")
        sys.exit(1)

    unit_dirs = sorted(RESOURCES_ROOT.iterdir())
    entries = []
    skipped = []

    for d in unit_dirs:
        if not d.is_dir():
            continue

        slug = d.name
        unit_num = slug_to_unit(slug)
        if not unit_num or unit_num in ("1.1.1", "1.1.2"):
            # Skip — already in script or can't parse
            print(f"  SKIP {slug} (already in UNITS or no unit number)")
            continue

        # Find answer key PDF
        ak_pdfs = list(d.glob("*answer-key*.pdf"))
        if not ak_pdfs:
            print(f"  SKIP {slug} — no answer-key PDF found")
            skipped.append(slug)
            continue

        ak_pdf = ak_pdfs[0]
        print(f"  Reading {ak_pdf.name} ...")

        try:
            text = extract_text(str(ak_pdf))
        except Exception as e:
            print(f"    ERROR reading PDF: {e}")
            skipped.append(slug)
            continue

        questions = extract_questions(text)
        if not questions:
            print(f"    WARNING: no questions extracted from {ak_pdf.name}")
            skipped.append(slug)
            continue

        print(f"    Extracted {len(questions)} questions")

        title = slug_to_title(slug)
        n10_009, n10_008 = guess_objectives(unit_num)
        entry = unit_to_dict_entry(unit_num, title, n10_009, n10_008, questions)
        entries.append(entry)

    # Write output
    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        f.write("# ── EXTRACTED UNITS ─────────────────────────────────────────────────\n")
        f.write("# Paste these entries INSIDE the UNITS dict in make_resource_pdfs.py\n")
        f.write("# Review titles, objective codes, and question formatting before use.\n")
        f.write("# ─────────────────────────────────────────────────────────────────────\n\n")
        f.write("\n".join(entries))
        f.write("\n")

    print(f"\nDone. {len(entries)} units extracted → {OUTPUT_FILE}")
    if skipped:
        print(f"Skipped ({len(skipped)}): {', '.join(skipped)}")
    print("\nNext: review scripts/extracted_units.py, then paste into UNITS dict.")


if __name__ == "__main__":
    main()
