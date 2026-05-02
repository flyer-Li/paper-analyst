#!/usr/bin/env python3
"""Convert a PDF to structured Markdown using markitdown.

This script is the first step in the paper-analyst pipeline: before sending
content to an LLM for analysis, the PDF is converted to Markdown to reduce
token consumption and improve downstream parsing.

Usage:
    python scripts/pdf_to_markdown.py <pdf_path>
    python scripts/pdf_to_markdown.py <pdf_path> --output <output.md>
    python scripts/pdf_to_markdown.py <pdf_path> --output <output.md> --no-front-matter

Dependencies: markitdown (pip install 'markitdown[pdf]')
"""

from __future__ import annotations

import argparse
import sys
import textwrap
from datetime import datetime, timezone
from pathlib import Path


def _extract_pdf_page_count(pdf_path: str) -> int:
    """Best-effort page count extraction via pypdf (optional dependency)."""
    try:
        from pypdf import PdfReader

        reader = PdfReader(pdf_path)
        return len(reader.pages)
    except Exception:
        return -1


def _build_front_matter(pdf_path: str, page_count: int) -> str:
    """Generate YAML front-matter with PDF metadata."""
    lines = [
        "---",
        f'source: "{Path(pdf_path).name}"',
        f'converted_at: "{datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}"',
        "converter: markitdown",
    ]
    if page_count > 0:
        lines.append(f"pages: {page_count}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def convert_pdf_to_markdown(
    pdf_path: str,
    output_path: str | None = None,
    include_front_matter: bool = True,
) -> str:
    """Convert a PDF file to Markdown.

    Args:
        pdf_path: Path to the input PDF file.
        output_path: Optional path to write the output .md file.
            If None, the result is only returned (not written to disk).
        include_front_matter: Whether to prepend YAML front-matter.

    Returns:
        The Markdown content as a string.

    Raises:
        FileNotFoundError: If the PDF file does not exist.
        ImportError: If markitdown is not installed.
        RuntimeError: If markitdown conversion fails.
    """
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    if not path.suffix.lower() == ".pdf":
        raise ValueError(f"Expected a .pdf file, got: {path.suffix}")

    try:
        from markitdown import MarkItDown
    except ImportError:
        raise ImportError(
            "markitdown is not installed. Install it with:\n  pip install 'markitdown[pdf]'"
        )

    md = MarkItDown()
    try:
        result = md.convert(pdf_path)
    except Exception as e:
        raise RuntimeError(f"markitdown conversion failed: {e}") from e

    markdown_text = result.text_content or ""

    # Prepend front-matter if requested
    if include_front_matter:
        page_count = _extract_pdf_page_count(pdf_path)
        front_matter = _build_front_matter(pdf_path, page_count)
        markdown_text = front_matter + markdown_text

    # Write to file if output_path specified
    if output_path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(markdown_text, encoding="utf-8")

    return markdown_text


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a PDF to structured Markdown using markitdown.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              python scripts/pdf_to_markdown.py paper.pdf
              python scripts/pdf_to_markdown.py paper.pdf --output paper.md
              python scripts/pdf_to_markdown.py paper.pdf --no-front-matter
        """),
    )
    parser.add_argument("pdf", help="Path to the input PDF file")
    parser.add_argument(
        "-o",
        "--output",
        help="Output .md file path (default: same name as PDF with .md extension)",
    )
    parser.add_argument(
        "--no-front-matter",
        action="store_true",
        help="Omit YAML front-matter from the output",
    )
    args = parser.parse_args()

    # Default output path: replace .pdf with .md
    output_path = args.output
    if output_path is None:
        output_path = str(Path(args.pdf).with_suffix(".md"))

    try:
        markdown = convert_pdf_to_markdown(
            pdf_path=args.pdf,
            output_path=output_path,
            include_front_matter=not args.no_front_matter,
        )
        # Print summary to stderr so stdout is clean for piping
        line_count = len(markdown.splitlines())
        print(
            f"Converted: {args.pdf} → {output_path} ({line_count} lines)",
            file=sys.stderr,
        )
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ImportError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
