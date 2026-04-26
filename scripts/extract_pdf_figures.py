#!/usr/bin/env python3
"""
Extract all images from a PDF and save to figures/ directory.
Usage: python extract_pdf_figures.py <pdf_path>
Output: figures/fig_p{page}_{idx}.png + figures/index.json
"""
import sys
import json
from pathlib import Path

import fitz  # pymupdf


def extract_figures(pdf_path: str) -> None:
    out_dir = Path("figures")
    out_dir.mkdir(exist_ok=True)

    doc = fitz.open(pdf_path)
    index = []

    for page_num, page in enumerate(doc, start=1):
        for img_idx, img in enumerate(page.get_images(), start=1):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.colorspace and pix.colorspace.n > 3:
                pix = fitz.Pixmap(fitz.csRGB, pix)
            name = f"fig_p{page_num}_{img_idx}.png"
            path = str(out_dir / name)
            pix.save(path)
            index.append({"name": name, "path": path, "page": page_num})

    (out_dir / "index.json").write_text(json.dumps(index, indent=2, ensure_ascii=False))
    print(f"Extracted {len(index)} figures → figures/index.json")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_pdf_figures.py <pdf_path>")
        sys.exit(1)
    extract_figures(sys.argv[1])
