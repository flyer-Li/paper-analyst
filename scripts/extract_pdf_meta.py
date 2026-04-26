#!/usr/bin/env python3
"""Extract structured metadata from a PDF file.

Usage: python scripts/extract_pdf_meta.py <path/to/paper.pdf>
Output: JSON to stdout

Dependencies: pypdf (pip install pypdf)
"""
import json
import sys


def extract(path: str) -> dict:
    try:
        from pypdf import PdfReader
    except ImportError:
        return {"error": "pypdf not installed. Run: pip install pypdf"}

    try:
        reader = PdfReader(path)
    except Exception as e:
        return {"error": f"Cannot open PDF: {e}"}

    meta = reader.metadata or {}
    pages = len(reader.pages)

    # Check if text is extractable (sample first 3 pages)
    sample_text = ""
    for page in reader.pages[:3]:
        sample_text += page.extract_text() or ""
    text_extractable = len(sample_text.strip()) > 100

    # Heuristic: likely scanned if pages exist but no text
    is_scanned = pages > 0 and not text_extractable

    def clean(val):
        return str(val).strip() if val else None

    return {
        "title": clean(meta.get("/Title")),
        "authors": clean(meta.get("/Author")),
        "subject": clean(meta.get("/Subject")),
        "keywords": clean(meta.get("/Keywords")),
        "creator": clean(meta.get("/Creator")),
        "pages": pages,
        "text_extractable": text_extractable,
        "is_scanned": is_scanned,
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_pdf_meta.py <file.pdf>", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(extract(sys.argv[1]), ensure_ascii=False, indent=2))
