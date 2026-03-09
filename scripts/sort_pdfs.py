#!/usr/bin/env python3
"""
sort_pdfs.py

Moves resource PDFs from new-pdfs/ into the correct subdirectory
under public/resources/<track>/.

The destination directory is derived from the filename by stripping
the trailing -guided-notes.pdf or -answer-key.pdf suffix.

Usage:
    # Default — no flags needed:
    python3 scripts/sort_pdfs.py

    # Dry run first to sanity check:
    python3 scripts/sort_pdfs.py --dry-run

    # Different track:
    python3 scripts/sort_pdfs.py --track pc-technician

    # Copy instead of move (keeps originals in new-pdfs/):
    python3 scripts/sort_pdfs.py --copy

    # Override source or destination if needed:
    python3 scripts/sort_pdfs.py --src path/to/pdfs --output-root path/to/resources

The destination directories must already exist (run make_resource_dirs.py first).
Files whose destination directory doesn't exist are flagged as warnings, not errors.
"""

import argparse
import shutil
from pathlib import Path

# ── DEFAULTS ──────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).parent.parent
DEFAULT_SRC = REPO_ROOT / "new-pdfs"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "public" / "resources"
# ─────────────────────────────────────────────────────────────────────────────

SUFFIXES = [
    "-guided-notes.pdf",
    "-answer-key.pdf",
]

def dir_from_filename(filename):
    """
    '3-1-1-network-documentation-guided-notes.pdf'
    -> '3-1-1-network-documentation'
    """
    for suffix in SUFFIXES:
        if filename.endswith(suffix):
            return filename[: -len(suffix)]
    return None

def main():
    parser = argparse.ArgumentParser(description="Sort flat resource PDFs into subdirectories")
    parser.add_argument("--src", default=None, help="Folder containing flat PDFs (default: new-pdfs/)")
    parser.add_argument("--track", default="network-engineer", help="Track name (default: network-engineer)")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without executing")
    parser.add_argument("--copy", action="store_true", help="Copy files instead of moving them")
    parser.add_argument("--output-root", default=None, help="Override output root (default: public/resources/)")
    args = parser.parse_args()

    src_dir = Path(args.src) if args.src else DEFAULT_SRC
    output_root = Path(args.output_root) if args.output_root else DEFAULT_OUTPUT_ROOT

    if not src_dir.exists():
        print(f"ERROR: Source directory not found: {src_dir}")
        return

    track_root = output_root / args.track
    action = "COPY" if args.copy else "MOVE"
    if args.dry_run:
        action = f"DRY-RUN ({action})"

    pdfs = sorted(src_dir.glob("*.pdf"))
    if not pdfs:
        print(f"No PDFs found in {src_dir}")
        return

    print(f"\nSource:  {src_dir.resolve()}")
    print(f"Track:   {args.track}")
    print(f"Dest:    {track_root.resolve()}")
    print(f"Mode:    {action}")
    print(f"Files:   {len(pdfs)}\n")

    moved = 0
    skipped = 0
    warnings = 0

    for pdf in pdfs:
        dir_name = dir_from_filename(pdf.name)

        if dir_name is None:
            print(f"  SKIP   {pdf.name}  (unrecognized suffix)")
            skipped += 1
            continue

        dest_dir = track_root / dir_name
        dest_file = dest_dir / pdf.name

        if not dest_dir.exists():
            print(f"  WARN   {pdf.name}  -> directory not found: {dest_dir.name}/")
            warnings += 1
            continue

        if dest_file.exists():
            print(f"  EXISTS {pdf.name}  (already in place, skipping)")
            skipped += 1
            continue

        print(f"  {action[:4]:4}   {pdf.name}  -> {dest_dir.name}/")

        if not args.dry_run:
            if args.copy:
                shutil.copy2(pdf, dest_file)
            else:
                shutil.move(str(pdf), dest_file)
        moved += 1

    print(f"\nDone.  Processed: {moved}  Skipped: {skipped}  Warnings: {warnings}")
    if warnings:
        print("  -> Run make_resource_dirs.py to create missing directories, then re-run.")
    if args.dry_run:
        print("  -> Dry run only -- no files were moved.")

if __name__ == "__main__":
    main()