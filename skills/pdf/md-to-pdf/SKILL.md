---
name: md-to-pdf
description: >
  Converts Markdown (.md) files to A4-formatted PDF using Playwright/Chromium.
  TRIGGER this skill when — and only when — the user's intent is to convert or export
  a Markdown (.md) file into a PDF. The source must be Markdown and the output must be PDF.
  Trigger phrases (pt-BR and EN): "converta o markdown para pdf", "gera pdf do markdown",
  "converte md para pdf", "exporta o md como pdf", "gera o pdf desse markdown",
  "convert markdown to pdf", "generate pdf from markdown", "convert this md to pdf",
  "export markdown as pdf", "md to pdf", "make a pdf from this markdown".
  DO NOT trigger for: converting HTML to PDF, exporting to Word/DOCX, viewing or rendering
  markdown, converting markdown to HTML only, or any task where the source is not a .md file
  or the output is not a PDF.
---

Convert Markdown (`.md`) files to A4-formatted PDF using Playwright/Chromium.

## What this skill does

1. Creates a temporary `.tmp/<filename>.html` next to each `.md` file
2. Uses Playwright/Chromium to render it into `pdf/<filename>.pdf`
3. Deletes the temporary HTML file and the `.tmp/` folder

Only the final **PDF** remains. The `.tmp/` folder is an implementation detail, not an output.

## Quick start

```bash
# Install dependencies (if not already installed)
pip install markdown playwright
python -m playwright install chromium

# Convert one or more files
python <skill-path>/scripts/convert.py path/to/file.md [path/to/other.md ...]
```

> Replace `<skill-path>` with the absolute path to this skill's directory.

## Folder structure after conversion

```
project/
├── notes.md
├── report.md
└── pdf/
    ├── notes.pdf
    └── report.pdf
```

The `pdf/` folder is created automatically if it does not exist.
The `.tmp/` folder is created and deleted automatically — it only exists during conversion.

## PDF output specification

| Feature | Behaviour |
|---|---|
| Generator | Playwright (`playwright.sync_api`) with bundled Chromium |
| Paper size | A4 (210 mm × 297 mm) |
| Margins | 20 mm top/sides, 25 mm bottom |
| Footer | Right-aligned "X / Y" page counter — rendered via CSS `@page @bottom-right` |
| Header | None |
| Code blocks | Background `#2d2d2d`, font 11 px, `white-space: pre-wrap` + `word-break: break-all` |
| Images | Resolved to absolute `file://` URIs so they load correctly during conversion |
| Background colours | Preserved (`print_background=True`) |
| Markdown extensions | `tables`, `fenced_code`, `toc`, `nl2br` (gracefully skips any unavailable extension) |
| Encoding | UTF-8 throughout |

## Dependencies

- Python 3.7+
- `markdown` library: `pip install markdown`
- `playwright` library + Chromium: `pip install playwright && python -m playwright install chromium`

## Bundled script

See `scripts/convert.py` — this is the main conversion script. Run it directly; no wrapper needed.
