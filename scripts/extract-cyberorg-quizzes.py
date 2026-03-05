#!/usr/bin/env python3
"""
extract_cyberorg_quizzes.py

Extracts quiz questions from CYBER.ORG answer key DOCX files and generates
MDX quiz files compatible with beattieNetTrack's content schema.

Usage:
    python3 extract_cyberorg_quizzes.py \
        --quizzes-dir /path/to/Quizzes \
        --output-dir /path/to/src/content/quizzes/network-engineer \
        --dry-run   # optional: preview without writing files

Output: One MDX file per quiz, named by CYBER.ORG unit number.
        e.g. 1.1.1-osi-model.mdx
"""

import argparse
import re
import sys
from pathlib import Path

try:
    from docx import Document
except ImportError:
    print("ERROR: python-docx not installed. Run: pip install python-docx --break-system-packages")
    sys.exit(1)

# ── MODULE MAPPING ─────────────────────────────────────────────────────────────
# Maps CYBER.ORG unit prefix (e.g. "1.1") to net.* moduleId
MODULE_MAP = {
    "1.1": "net.fundamentals.models-and-standards",
    "1.2": "net.fundamentals.topologies-and-types",
    "1.3": "net.fundamentals.cabling-and-connectors",
    "1.4": "net.fundamentals.addressing",
    "1.5": "net.fundamentals.ports-and-protocols",
    "1.6": "net.fundamentals.network-services",
    "1.7": "net.fundamentals.architecture",
    "1.8": "net.fundamentals.architecture",
    "2.1": "net.implementation.devices",
    "2.2": "net.implementation.routing",
    "2.3": "net.implementation.switching",
    "2.4": "net.implementation.wireless",
    "3.1": "net.operations.monitoring-and-docs",
    "3.2": "net.operations.monitoring-and-docs",
    "3.3": "net.operations.monitoring-and-docs",
    "4.1": "net.security.defense",
    "4.2": "net.security.defense",
    "4.3": "net.security.defense",
    "4.4": "net.security.defense",
    "4.5": "net.security.defense",
    "5.1": "net.troubleshooting.tools-and-methods",
    "5.2": "net.troubleshooting.tools-and-methods",
    "5.3": "net.troubleshooting.tools-and-methods",
    "5.4": "net.troubleshooting.tools-and-methods",
    "5.5": "net.troubleshooting.tools-and-methods",
}

# Order within each module (incremented as quizzes are assigned)
MODULE_ORDER_COUNTERS = {}


def slugify(text):
    """Convert title to kebab-case slug."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s]+", "-", text.strip())
    return text


def parse_key_file(filepath):
    """
    Parse a CYBER.ORG answer key DOCX file.
    Returns list of question dicts with prompt, choices, answer fields.
    """
    doc = Document(filepath)
    questions = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        # Each question block ends with "Answer: X"
        parts = re.split(r"\n\s*Answer:\s*", text)
        if len(parts) != 2:
            continue

        question_block = parts[0].strip()
        answer_letter = parts[1].strip().upper()

        lines = question_block.split("\n")
        if not lines:
            continue

        # First line is "N. Question text"
        q_text = re.sub(r"^\d+\.\s*", "", lines[0]).strip()

        # Remaining lines are choices
        choices = {}
        for line in lines[1:]:
            c_match = re.match(r"\s*([A-D])\.\s+(.+)", line.strip())
            if c_match:
                choices[c_match.group(1)] = c_match.group(2).strip()

        # Only include if we have choices and a valid answer
        if len(choices) >= 2 and answer_letter in choices:
            questions.append(
                {
                    "prompt": q_text,
                    "choices": choices,
                    "answer": answer_letter,
                }
            )

    return questions


def questions_to_mdx(unit_number, title, module_id, order, questions, track="network-engineer"):
    """Generate MDX frontmatter + body for a quiz."""
    slug = f"net-{unit_number.replace('.', '-')}-{slugify(title)}"

    # Build questions YAML block
    q_lines = []
    for i, q in enumerate(questions):
        q_lines.append(f"  - id: q{i+1}")
        q_lines.append(f"    type: single")
        # Escape any quotes in prompt
        prompt = q["prompt"].replace('"', '\\"')
        q_lines.append(f'    prompt: "{prompt}"')
        q_lines.append(f"    options:")
        for letter, text in q["choices"].items():
            text_escaped = text.replace('"', '\\"')
            q_lines.append(f'      - "{letter}. {text_escaped}"')
        correct = q["choices"][q["answer"]]
        correct_escaped = correct.replace('"', '\\"')
        q_lines.append(f'    correct: "{q["answer"]}. {correct_escaped}"')

    questions_yaml = "\n".join(q_lines)

    mdx = f"""---
title: "{title}"
slug: "{slug}"
track: {track}
moduleId: {module_id}
order: {order}
difficulty: Beginner
xp: 20
passThreshold: 0.7
tags: ["network+", "cyberorg"]
questions:
{questions_yaml}
---

Quiz covering {title} — CYBER.ORG unit {unit_number}.
"""
    return slug, mdx


def process_quizzes_dir(quizzes_dir, output_dir, dry_run=False):
    """Process all answer key files in the quizzes directory."""
    quizzes_path = Path(quizzes_dir)
    output_path = Path(output_dir)

    # Find all key files
    key_files = sorted(quizzes_path.glob("*- key -*.docx"))

    if not key_files:
        print(f"ERROR: No key files found in {quizzes_dir}")
        sys.exit(1)

    print(f"Found {len(key_files)} answer key files\n")

    results = []
    errors = []

    for key_file in key_files:
        # Parse filename: "1.1.1 - key - OSI Model.docx"
        name = key_file.stem  # "1.1.1 - key - OSI Model"
        parts = name.split(" - key - ")
        if len(parts) != 2:
            errors.append(f"SKIP: unexpected filename format: {key_file.name}")
            continue

        unit_number = parts[0].strip()   # "1.1.1"
        title = parts[1].strip()          # "OSI Model"

        # Get module ID from unit prefix
        unit_prefix = ".".join(unit_number.split(".")[:2])  # "1.1"
        module_id = MODULE_MAP.get(unit_prefix)

        if not module_id:
            errors.append(f"SKIP: no module mapping for unit {unit_number} ({title})")
            continue

        # Assign order within module
        if module_id not in MODULE_ORDER_COUNTERS:
            MODULE_ORDER_COUNTERS[module_id] = 1
        order = MODULE_ORDER_COUNTERS[module_id]
        MODULE_ORDER_COUNTERS[module_id] += 1

        # Parse questions
        try:
            questions = parse_key_file(key_file)
        except Exception as e:
            errors.append(f"ERROR parsing {key_file.name}: {e}")
            continue

        if not questions:
            errors.append(f"SKIP: no questions extracted from {key_file.name}")
            continue

        # Generate MDX
        slug, mdx_content = questions_to_mdx(unit_number, title, module_id, order, questions)
        output_file = output_path / f"{slug}.mdx"

        results.append({
            "unit": unit_number,
            "title": title,
            "module": module_id,
            "order": order,
            "questions": len(questions),
            "slug": slug,
            "output": output_file,
            "content": mdx_content,
        })

    # Report
    print(f"{'DRY RUN — ' if dry_run else ''}Results:")
    print(f"  Processed: {len(results)} quizzes")
    print(f"  Skipped/errors: {len(errors)}\n")

    # Show by module
    current_module = None
    for r in results:
        if r["module"] != current_module:
            current_module = r["module"]
            print(f"\n  [{current_module}]")
        print(f"    {r['unit']:8} {r['title']:<45} {r['questions']} questions → {r['slug']}.mdx")

    if errors:
        print("\nErrors/Skips:")
        for e in errors:
            print(f"  {e}")

    if not dry_run:
        output_path.mkdir(parents=True, exist_ok=True)
        written = 0
        for r in results:
            r["output"].write_text(r["content"], encoding="utf-8")
            written += 1
        print(f"\nWrote {written} MDX files to {output_path}")
    else:
        print(f"\nDry run complete. Run without --dry-run to write files.")

    return results, errors


def main():
    parser = argparse.ArgumentParser(description="Extract CYBER.ORG quizzes to MDX")
    parser.add_argument("--quizzes-dir", required=True, help="Path to CYBER.ORG Quizzes folder")
    parser.add_argument("--output-dir", required=True, help="Output directory for MDX files")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")
    args = parser.parse_args()

    process_quizzes_dir(args.quizzes_dir, args.output_dir, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
