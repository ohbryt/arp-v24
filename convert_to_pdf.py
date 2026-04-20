#!/usr/bin/env python3
"""
ARP v24 - Markdown to PDF using ReportLab (No external PDF engines needed)
"""

import os
import re
import markdown
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, ListFlowable, ListItem
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT

# Read markdown
md_file = "ONE_CARBON_METABOLISM_DEEP_REVIEW.md"
pdf_file = "ONE_CARBON_METABOLISM_DEEP_REVIEW.pdf"

with open(md_file, "r", encoding="utf-8") as f:
    md_content = f.read()

# Create PDF
doc = SimpleDocTemplate(
    pdf_file,
    pagesize=A4,
    rightMargin=1.5*cm,
    leftMargin=1.5*cm,
    topMargin=2*cm,
    bottomMargin=2*cm
)

# Styles
styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=20,
    textColor=colors.HexColor('#1a3a5c'),
    spaceAfter=20,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

subtitle_style = ParagraphStyle(
    'CustomSubtitle',
    parent=styles['Normal'],
    fontSize=12,
    textColor=colors.HexColor('#6B8CAE'),
    spaceAfter=30,
    alignment=TA_CENTER
)

h1_style = ParagraphStyle(
    'CustomH1',
    parent=styles['Heading1'],
    fontSize=16,
    textColor=colors.HexColor('#2c5f8a'),
    spaceBefore=20,
    spaceAfter=10,
    fontName='Helvetica-Bold'
)

h2_style = ParagraphStyle(
    'CustomH2',
    parent=styles['Heading2'],
    fontSize=13,
    textColor=colors.HexColor('#3a6d9c'),
    spaceBefore=15,
    spaceAfter=8,
    fontName='Helvetica-Bold'
)

h3_style = ParagraphStyle(
    'CustomH3',
    parent=styles['Heading3'],
    fontSize=11,
    textColor=colors.HexColor('#4a7fb0'),
    spaceBefore=10,
    spaceAfter=5,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['Normal'],
    fontSize=10,
    leading=14,
    textColor=colors.HexColor('#2c3e50'),
    alignment=TA_JUSTIFY,
    spaceAfter=6
)

table_style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4A6FA5')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ('TOPPADDING', (0, 0), (-1, 0), 8),
    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f8fc')),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#c5d5e5')),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
])

story = []

# Parse markdown sections
lines = md_content.split('\n')
i = 0
in_table = False
table_data = []
table_headers = []

def parse_inline(text):
    """Convert markdown inline formatting to reportlab formatting"""
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    # Code
    text = re.sub(r'`(.+?)`', r'<font face="Courier">\1</font>', text)
    return text

while i < len(lines):
    line = lines[i]
    
    # Skip horizontal rules at the start
    if line.strip() == '---' and i < 5:
        i += 1
        continue
    
    # Title
    if line.startswith('# '):
        title = line[2:].strip()
        if 'Executive Summary' in title or 'Deep Review' in title:
            story.append(Paragraph(title, title_style))
        else:
            story.append(Paragraph(title, h1_style))
        i += 1
        continue
    
    # H2
    if line.startswith('## '):
        title = line[3:].strip()
        story.append(Paragraph(title, h2_style))
        i += 1
        continue
    
    # H3
    if line.startswith('### '):
        title = line[4:].strip()
        story.append(Paragraph(title, h3_style))
        i += 1
        continue
    
    # H4
    if line.startswith('#### '):
        title = line[5:].strip()
        story.append(Paragraph(title, h3_style))
        i += 1
        continue
    
    # Table parsing
    if '|' in line and line.strip().startswith('|'):
        # Check if header row (contains ---)
        if i + 1 < len(lines) and lines[i + 1].strip().startswith('|'):
            if all(c in '-:|' for c in re.sub(r'[^|:-\s]', '', lines[i + 1])):
                # This is a header row followed by separator
                # Collect headers
                headers = [h.strip() for h in line.split('|') if h.strip()]
                i += 2  # Skip header and separator
                
                # Collect table rows
                rows = []
                while i < len(lines) and '|' in lines[i] and lines[i].strip().startswith('|'):
                    row = [c.strip() for c in lines[i].split('|') if c.strip()]
                    if row:
                        rows.append(row)
                    i += 1
                
                if headers and rows:
                    table = Table([headers] + rows, colWidths=[4*cm] * len(headers))
                    table.setStyle(table_style)
                    story.append(table)
                    story.append(Spacer(1, 10))
                continue
            else:
                # Simple table without separator
                row = [c.strip() for c in line.split('|') if c.strip()]
                if row:
                    if not in_table:
                        table_data = []
                        in_table = True
                    table_data.append(row)
                i += 1
                continue
        else:
            row = [c.strip() for c in line.split('|') if c.strip()]
            if row:
                if not in_table:
                    table_data = []
                    in_table = True
                table_data.append(row)
            i += 1
            continue
    else:
        if in_table and table_data:
            # Finish table
            if len(table_data) >= 2:
                table = Table(table_data)
                table.setStyle(table_style)
                story.append(table)
                story.append(Spacer(1, 10))
            table_data = []
            in_table = False
    
    # Empty line
    if not line.strip():
        i += 1
        continue
    
    # Bullet points
    if line.strip().startswith('- ') or line.strip().startswith('* '):
        text = line.strip()[2:]
        story.append(Paragraph(f"• {parse_inline(text)}", body_style))
        i += 1
        continue
    
    # Numbered lists
    match = re.match(r'^\d+\.\s+(.*)', line.strip())
    if match:
        text = match.group(1)
        story.append(Paragraph(f"<b>{line.strip()[0]}.</b> {parse_inline(text)}", body_style))
        i += 1
        continue
    
    # Regular paragraph
    text = line.strip()
    if text and not text.startswith('#') and len(text) > 5:
        # Check for markdown formatting
        text = parse_inline(text)
        story.append(Paragraph(text, body_style))
    
    i += 1

# Build PDF
doc.build(story)

# Check file
if os.path.exists(pdf_file):
    size = os.path.getsize(pdf_file)
    print(f"✓ PDF created: {pdf_file}")
    print(f"  Size: {size/1024:.1f} KB")
else:
    print("✗ PDF creation failed")