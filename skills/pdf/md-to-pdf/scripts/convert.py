#!/usr/bin/env python3
"""Convert Markdown files to A4-formatted PDF via Playwright/Chromium. HTML is a temporary intermediate step and is deleted after each PDF is generated."""

import sys
import os
import re
from pathlib import Path

try:
    import markdown
except ImportError:
    print("ERROR: 'markdown' library not installed. Run: pip install markdown")
    sys.exit(1)

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("ERROR: 'playwright' not installed. Run: pip install playwright && python -m playwright install chromium")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Image path resolution
# ---------------------------------------------------------------------------

def resolve_image_paths(html_content: str, base_dir: Path) -> str:
    """Replace relative src= paths with absolute file:// URIs so the browser can load them."""
    def to_absolute(match):
        path = match.group(1)
        if re.match(r'^(https?://|file://|data:|#|//)', path):
            return match.group(0)
        abs_path = (base_dir / path).resolve()
        if abs_path.exists():
            return f'src="{abs_path.as_uri()}"'
        return match.group(0)

    return re.sub(r'src="([^"]*)"', to_absolute, html_content)


# ---------------------------------------------------------------------------
# HTML template
# ---------------------------------------------------------------------------

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
@page {{
  size: A4;
  margin: 20mm 20mm 25mm 20mm;
}}

@page {{
  @bottom-right {{
    content: counter(page) " / " counter(pages);
    font-family: Arial, sans-serif;
    font-size: 10pt;
    font-weight: normal;
    color: #000;
  }}
}}

@media print {{
  header, .no-print {{
    display: none !important;
  }}
}}

body {{
  font-family: Arial, Helvetica, sans-serif;
  font-size: 12pt;
  line-height: 1.6;
  color: #000;
  background: #fff;
  max-width: 170mm;
  margin: 0 auto;
  padding: 10mm 0;
}}

img {{
  max-width: 100%;
  height: auto;
  display: block;
}}

pre {{
  background: #2d2d2d;
  color: #f8f8f2;
  font-family: "Courier New", Courier, monospace;
  font-size: 11px;
  padding: 14px 16px;
  border-radius: 4px;
  white-space: pre-wrap;
  word-wrap: break-word;
  word-break: break-all;
  overflow-wrap: break-word;
  page-break-inside: avoid;
  margin: 12px 0;
}}

code {{
  background: #2d2d2d;
  color: #f8f8f2;
  font-family: "Courier New", Courier, monospace;
  font-size: 11px;
  padding: 2px 5px;
  border-radius: 3px;
}}

pre code {{
  background: transparent;
  padding: 0;
  font-size: inherit;
}}

h1, h2, h3, h4, h5, h6 {{
  page-break-after: avoid;
  margin-top: 1em;
  margin-bottom: 0.4em;
}}

table {{
  border-collapse: collapse;
  width: 100%;
  max-width: 100%;
  margin: 12px 0;
  page-break-inside: avoid;
}}

th, td {{
  border: 1px solid #ccc;
  padding: 6px 10px;
  text-align: left;
}}

th {{
  background: #f0f0f0;
  font-weight: bold;
}}

blockquote {{
  border-left: 4px solid #ccc;
  margin: 12px 0;
  padding: 4px 16px;
  color: #444;
}}

hr {{
  border: none;
  border-top: 1px solid #ddd;
  margin: 16px 0;
}}
</style>
</head>
<body>
{content}
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Conversion functions
# ---------------------------------------------------------------------------

def md_to_html(md_path: str) -> str:
    """Convert a Markdown file to HTML; returns the path of the created HTML file."""
    md_file = Path(md_path).resolve()
    if not md_file.exists():
        raise FileNotFoundError(f"Markdown file not found: {md_path}")

    html_dir = md_file.parent / ".tmp"
    html_dir.mkdir(parents=True, exist_ok=True)
    html_file = html_dir / (md_file.stem + ".html")

    with open(md_file, encoding="utf-8") as f:
        md_text = f.read()

    # Remove <br> tags at end of lines so nl2br doesn't double them into blank lines
    md_text = re.sub(r'[ \t]*<br\s*/?>[ \t]*\n', '\n', md_text, flags=re.IGNORECASE)

    for ext_set in (
        ["tables", "fenced_code", "toc", "nl2br"],
        ["tables", "fenced_code"],
        [],
    ):
        try:
            html_body = markdown.markdown(md_text, extensions=ext_set)
            break
        except Exception:
            continue
    else:
        html_body = markdown.markdown(md_text)

    full_html = HTML_TEMPLATE.format(title=md_file.stem, content=html_body)
    full_html = resolve_image_paths(full_html, md_file.parent)

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"  [HTML] {html_file}")
    return str(html_file)


def html_to_pdf(html_path: str) -> str:
    """Convert an HTML file to PDF using Playwright/Chromium; returns PDF path."""
    html_file = Path(html_path).resolve()
    if not html_file.exists():
        raise FileNotFoundError(f"HTML file not found: {html_path}")

    pdf_dir = html_file.parent.parent / "pdf"
    pdf_dir.mkdir(parents=True, exist_ok=True)
    pdf_file = pdf_dir / (html_file.stem + ".pdf")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(html_file.as_uri(), wait_until="networkidle")
        page.pdf(
            path=str(pdf_file),
            format="A4",
            print_background=True,
            display_header_footer=False,
            margin={
                "top": "20mm",
                "bottom": "25mm",
                "left": "20mm",
                "right": "20mm",
            },
        )
        browser.close()

    print(f"  [PDF]  {pdf_file}")
    return str(pdf_file)


# ---------------------------------------------------------------------------
# Cleanup
# ---------------------------------------------------------------------------

def cleanup_html(html_path: str) -> None:
    """Delete the temporary HTML file and its folder if empty afterwards."""
    html_file = Path(html_path)
    try:
        html_file.unlink()
    except OSError:
        pass
    try:
        html_file.parent.rmdir()  # Only succeeds if empty — safe to always attempt
        print(f"  [CLEAN] {html_file.parent}")
    except OSError:
        pass


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print("Usage: convert.py <file1.md> [file2.md ...]")
        print("\nConverts each .md file to:")
        print("  pdf/<name>.pdf  — A4-formatted PDF generated by Playwright/Chromium")
        print("\nThe html/ folder is created temporarily and deleted after each PDF is generated.")
        sys.exit(0)

    errors = []
    for md_path in args:
        print(f"\nConverting: {md_path}")
        html_path = None
        try:
            html_path = md_to_html(md_path)
            html_to_pdf(html_path)
        except Exception as exc:
            print(f"  ERROR: {exc}")
            errors.append((md_path, str(exc)))
        finally:
            if html_path:
                cleanup_html(html_path)

    print()
    if errors:
        print(f"Finished with {len(errors)} error(s):")
        for path, msg in errors:
            print(f"  {path}: {msg}")
        sys.exit(1)
    else:
        print("All files converted successfully.")


if __name__ == "__main__":
    main()
