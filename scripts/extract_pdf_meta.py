#!/usr/bin/env python3
"""Extract structured metadata from a PDF file.

Usage: python scripts/extract_pdf_meta.py <path/to/paper.pdf>
Output: JSON to stdout

Dependencies: pypdf (pip install pypdf)
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Union

# Minimum text length to consider a PDF as having extractable text.
# This threshold is based on typical academic paper abstracts (~100+ words).
MIN_EXTRACTABLE_TEXT_LEN: int = 100

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)


def _clean(val: Any) -> Optional[str]:
    """Clean and convert a metadata value to string.

    Args:
        val: The metadata value to clean.

    Returns:
        Cleaned string or None if value is empty/None.
    """
    if val is None:
        return None
    if not isinstance(val, str):
        logger.warning("Expected string metadata, got %s: %s", type(val).__name__, val)
        try:
            val = str(val)
        except Exception:
            return None
    val = val.strip()
    return val if val else None


def extract(path: str) -> Dict[str, Union[str, int, bool, None]]:
    """Extract metadata from a PDF file.

    Args:
        path: Path to the PDF file.

    Returns:
        Dictionary containing PDF metadata.
    """
    try:
        from pypdf import PdfReader
    except ImportError:
        logger.error("pypdf not installed. Run: pip install pypdf")
        return {"error": "pypdf not installed. Run: pip install pypdf"}

    try:
        reader = PdfReader(path)
        logger.info("Successfully opened PDF: %s", path)
    except Exception as e:
        logger.error("Cannot open PDF %s: %s", path, e)
        return {"error": f"Cannot open PDF: {e}"}

    meta = reader.metadata or {}
    pages = len(reader.pages)

    # Check if text is extractable (sample first 3 pages)
    sample_text = ""
    for i, page in enumerate(reader.pages[:3]):
        try:
            text = page.extract_text() or ""
            sample_text += text
        except Exception as e:
            logger.warning("Failed to extract text from page %d: %s", i + 1, e)

    text_extractable = len(sample_text.strip()) > MIN_EXTRACTABLE_TEXT_LEN

    # Heuristic: likely scanned if pages exist but no text
    is_scanned = pages > 0 and not text_extractable

    if is_scanned:
        logger.info("PDF appears to be scanned (no extractable text)")

    result: Dict[str, Union[str, int, bool, None]] = {
        "title": _clean(meta.get("/Title")),
        "authors": _clean(meta.get("/Author")),
        "subject": _clean(meta.get("/Subject")),
        "keywords": _clean(meta.get("/Keywords")),
        "creator": _clean(meta.get("/Creator")),
        "pages": pages,
        "text_extractable": text_extractable,
        "is_scanned": is_scanned,
    }

    logger.info(
        "Extracted metadata: %d pages, text_extractable=%s", pages, text_extractable
    )
    return result


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Extract structured metadata from a PDF file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Example: python scripts/extract_pdf_meta.py paper.pdf",
    )
    parser.add_argument("pdf", help="Path to the input PDF file")
    args = parser.parse_args()

    pdf_path = args.pdf
    if not Path(pdf_path).exists():
        print(json.dumps({"error": f"File not found: {pdf_path}"}, ensure_ascii=False))
        sys.exit(1)

    result = extract(pdf_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
