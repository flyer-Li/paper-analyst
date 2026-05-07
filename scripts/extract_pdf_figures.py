#!/usr/bin/env python3
"""Extract all images from a PDF and save to output directory.

Usage:
    python scripts/extract_pdf_figures.py <pdf_path>
    python scripts/extract_pdf_figures.py <pdf_path> --output-dir ./out
    python scripts/extract_pdf_figures.py <pdf_path> --no-clean

Output: <output_dir>/fig_p{page}_{idx}.png + <output_dir>/index.json

Dependencies: pymupdf (pip install pymupdf)
"""

from __future__ import annotations

import argparse
import json
import logging
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List

import fitz  # pymupdf

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)


def _save_page_images(
    doc: fitz.Document,
    page: fitz.Page,
    page_num: int,
    out_dir: Path,
) -> List[Dict[str, Any]]:
    """Extract and save all images from a single page.

    Args:
        doc: The fitz Document object.
        page: The fitz Page object.
        page_num: 1-based page number.
        out_dir: Output directory for saving images.

    Returns:
        List of image index entries for this page.
    """
    entries: List[Dict[str, Any]] = []
    images = page.get_images()

    for img_idx, img in enumerate(images, start=1):
        xref = img[0]
        try:
            pix_original = fitz.Pixmap(doc, xref)
            pix: fitz.Pixmap
            if pix_original.colorspace and pix_original.colorspace.n > 3:
                pix = fitz.Pixmap(fitz.csRGB, pix_original)
                # Release the original large pixmap
                del pix_original
            else:
                pix = pix_original

            name = f"fig_p{page_num}_{img_idx}.png"
            path = str(out_dir / name)
            pix.save(path)
            # Release pixmap after saving
            del pix

            entries.append({"name": name, "path": path, "page": page_num})
        except Exception as e:
            logger.warning(
                "Failed to extract image %d from page %d: %s", img_idx, page_num, e
            )
            continue

    return entries


def extract_figures(
    pdf_path: str,
    output_dir: str = "figures",
    clean: bool = True,
) -> List[Dict[str, Any]]:
    """Extract all figures from a PDF file.

    Args:
        pdf_path: Path to the input PDF file.
        output_dir: Directory to save extracted figures.
        clean: If True, delete and recreate the output directory.

    Returns:
        List of dicts with keys: name, path, page.
    """
    out_dir = Path(output_dir)

    # Validate input file
    if not Path(pdf_path).exists():
        logger.error("PDF not found: %s", pdf_path)
        sys.exit(1)

    # Handle output directory
    if out_dir.exists():
        if clean:
            logger.info("Cleaning output directory: %s", out_dir)
            shutil.rmtree(out_dir)
        else:
            logger.info("Output directory exists, appending: %s", out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    index: List[Dict[str, Any]] = []

    with fitz.open(pdf_path) as doc:
        total_pages = len(doc)
        logger.info("Processing %d pages from %s", total_pages, pdf_path)

        for page_num, page in enumerate(doc, start=1):
            logger.info("Processing page %d/%d...", page_num, total_pages)
            entries = _save_page_images(doc, page, page_num, out_dir)
            index.extend(entries)

    # Write index file
    index_path = out_dir / "index.json"
    index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False))
    logger.info("Extracted %d figures → %s", len(index), index_path)

    return index


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Extract all images from a PDF file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Example: python scripts/extract_pdf_figures.py paper.pdf --output-dir ./out",
    )
    parser.add_argument("pdf", help="Path to the input PDF file")
    parser.add_argument(
        "-o",
        "--output-dir",
        default="figures",
        help="Output directory for extracted figures (default: figures)",
    )
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Do not clean the output directory before extraction",
    )
    args = parser.parse_args()

    index = extract_figures(
        pdf_path=args.pdf,
        output_dir=args.output_dir,
        clean=not args.no_clean,
    )
    print(
        f"Extracted {len(index)} figures → {args.output_dir}/index.json",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
