#!/usr/bin/env python3
"""
ARP v24 - MMP11/GDF10 Combined Report to Kami-Style HTML/PDF
"""

import markdown
import os

# Read combined markdown
md_file = "MMP11_GDF10_COMBINED_2026.md"
html_file = "MMP11_GDF10_COMBINED_2026.html"

with open(md_file, "r", encoding="utf-8") as f:
    md_content = f.read()

# Convert markdown to HTML
html_body = markdown.markdown(
    md_content,
    extensions=[
        'tables',
        'fenced_code',
        'codehilite',
        'nl2br',
        'sane_lists'
    ]
)

# Kami-style HTML template
html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>MMP11 and GDF10 in Heart Failure - Drug Discovery Pipeline</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Newsreader:wght@400;500&family=Inter:wght@400;500;600&display=swap');

  @page {
    size: A4;
    margin: 20mm 22mm 22mm 22mm;
    background: #f5f4ed;
  }
  @page:first { background: #f5f4ed; }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --parchment: #f5f4ed;
    --ivory: #faf9f5;
    --near-black: #141413;
    --dark-warm: #3d3d3a;
    --charcoal: #4d4c48;
    --olive: #5e5d59;
    --stone: #87867f;
    --brand: #1B365D;
    --border: #e8e6dc;
    --tag-bg: #E4ECF5;
    --table-header: #4A6FA5;
    --table-alt: #f5f8fc;
  }

  body {
    background: var(--parchment);
    color: var(--near-black);
    font-family: "Newsreader", Georgia, serif;
    font-size: 10.5pt;
    line-height: 1.55;
  }

  /* Cover */
  .cover {
    min-height: 260mm;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 50mm 20mm;
    background: var(--parchment);
    break-after: page;
  }
  .cover-eyebrow {
    font-family: "Inter", sans-serif;
    font-size: 10pt;
    color: var(--brand);
    letter-spacing: 2pt;
    text-transform: uppercase;
    font-weight: 500;
    margin-bottom: 18pt;
  }
  .cover-title {
    font-size: 32pt;
    font-weight: 500;
    color: var(--near-black);
    line-height: 1.15;
    letter-spacing: -0.5pt;
    margin-bottom: 20pt;
  }
  .cover-subtitle {
    font-family: "Inter", sans-serif;
    font-size: 14pt;
    color: var(--olive);
    line-height: 1.5;
    max-width: 85%;
    margin-bottom: 40pt;
  }
  .cover-meta {
    font-family: "Inter", sans-serif;
    font-size: 9pt;
    color: var(--stone);
    border-top: 1px solid var(--border);
    padding-top: 15pt;
    margin-top: auto;
  }

  /* Content */
  .content {
    background: var(--ivory);
    padding: 30mm 25mm;
    max-width: 100%;
  }

  /* Headings */
  h1 {
    font-size: 20pt;
    font-weight: 500;
    color: var(--brand);
    margin: 35pt 0 15pt 0;
    border-bottom: 2px solid var(--border);
    padding-bottom: 8pt;
  }
  h1:first-of-type { margin-top: 0; }

  h2 {
    font-size: 15pt;
    font-weight: 500;
    color: var(--dark-warm);
    margin: 25pt 0 12pt 0;
  }

  h3 {
    font-size: 12pt;
    font-weight: 500;
    color: var(--charcoal);
    margin: 18pt 0 8pt 0;
  }

  h4 {
    font-size: 10.5pt;
    font-weight: 600;
    color: var(--charcoal);
    margin: 12pt 0 6pt 0;
  }

  /* Paragraphs */
  p {
    margin: 0 0 10pt 0;
    text-align: justify;
  }

  /* Lists */
  ul, ol {
    margin: 8pt 0 10pt 0;
    padding-left: 20pt;
  }
  li {
    margin: 4pt 0;
    line-height: 1.5;
  }

  /* Tables */
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 15pt 0;
    font-size: 9.5pt;
  }
  th {
    background: var(--table-header);
    color: white;
    font-family: "Inter", sans-serif;
    font-weight: 500;
    font-size: 8.5pt;
    text-transform: uppercase;
    letter-spacing: 0.5pt;
    padding: 8pt 10pt;
    text-align: left;
    border: none;
  }
  td {
    padding: 7pt 10pt;
    border-bottom: 1px solid var(--border);
    vertical-align: top;
  }
  tr:nth-child(even) td { background: var(--table-alt); }
  tr:last-child td { border-bottom: none; }

  /* Code */
  code {
    font-family: "JetBrains Mono", Consolas, monospace;
    font-size: 8.5pt;
    background: #f0ede6;
    padding: 1pt 4pt;
    border-radius: 3pt;
  }
  pre {
    background: #f0ede6;
    padding: 12pt;
    border-radius: 5pt;
    overflow-x: auto;
    margin: 12pt 0;
    font-size: 8pt;
    line-height: 1.4;
  }
  pre code {
    background: none;
    padding: 0;
  }

  /* Blockquotes */
  blockquote {
    border-left: 3px solid var(--brand);
    padding: 8pt 15pt;
    margin: 15pt 0;
    background: var(--tag-bg);
    font-style: italic;
    color: var(--dark-warm);
  }

  /* Bold/Italic */
  strong { font-weight: 600; color: var(--dark-warm); }
  em { font-style: italic; }

  /* Horizontal Rule */
  hr {
    border: none;
    border-top: 1px solid var(--border);
    margin: 25pt 0;
  }

  /* Page breaks */
  .page-break { break-after: page; }

  /* Small caps label */
  .label {
    font-family: "Inter", sans-serif;
    font-size: 8pt;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1pt;
    color: var(--stone);
  }

  @media print {
    body { background: var(--parchment); }
    .content { padding: 0; }
    .page-break { break-after: page; }
  }
</style>
</head>
<body>

<div class="content">
''' + html_body + '''
</div>

</body>
</html>'''

with open(html_file, "w", encoding="utf-8") as f:
    f.write(html_template)

size = os.path.getsize(html_file)
print(f"✓ HTML created: {html_file}")
print(f"  Size: {size/1024:.1f} KB")
print(f"  → Open in browser and Print to PDF")
