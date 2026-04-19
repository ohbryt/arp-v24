#!/usr/bin/env python3
"""Simple markdown to PDF converter using reportlab"""

import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

# Read markdown
with open('ONE_CARBON_METABOLISM_DEEP_REVIEW.md', 'r') as f:
    content = f.read()

pdf_file = 'ONE_CARBON_METABOLISM_DEEP_REVIEW.pdf'
doc = SimpleDocTemplate(pdf_file, pagesize=A4, 
                        rightMargin=1.5*cm, leftMargin=1.5*cm,
                        topMargin=2*cm, bottomMargin=2*cm)

styles = getSampleStyleSheet()
title_style = ParagraphStyle('T', parent=styles['Heading1'], fontSize=18, 
                             textColor=colors.HexColor('#1a3a5c'), spaceAfter=15, alignment=TA_CENTER)
h1_style = ParagraphStyle('H1', parent=styles['Heading1'], fontSize=14, 
                           textColor=colors.HexColor('#2c5f8a'), spaceBefore=15, spaceAfter=8, fontName='Helvetica-Bold')
h2_style = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=12, 
                           textColor=colors.HexColor('#3a6d9c'), spaceBefore=12, spaceAfter=6, fontName='Helvetica-Bold')
body_style = ParagraphStyle('B', parent=styles['Normal'], fontSize=9, leading=12, 
                             textColor=colors.HexColor('#2c3e50'), alignment=TA_JUSTIFY, spaceAfter=4)

table_style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4A6FA5')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
    ('TOPPADDING', (0, 0), (-1, 0), 6),
    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f5f8fc')),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#c5d5e5')),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
])

story = []
table_data = []
in_table = False

def clean(text):
    text = text.replace('**', '')
    text = text.replace('*', '')
    text = text.replace('`', '')
    return text

lines = content.split('\n')

for line in lines:
    line = line.rstrip()
    if not line.strip() or line.strip() == '---':
        if in_table and len(table_data) >= 2:
            t = Table(table_data)
            t.setStyle(table_style)
            story.append(t)
            story.append(Spacer(1, 8))
            table_data = []
            in_table = False
        continue
    
    if line.startswith('# '):
        if in_table and len(table_data) >= 2:
            t = Table(table_data)
            t.setStyle(table_style)
            story.append(t)
            story.append(Spacer(1, 8))
            table_data = []
            in_table = False
        story.append(Paragraph(clean(line[2:]).strip(), title_style))
    elif line.startswith('## '):
        if in_table and len(table_data) >= 2:
            t = Table(table_data)
            t.setStyle(table_style)
            story.append(t)
            story.append(Spacer(1, 8))
            table_data = []
            in_table = False
        story.append(Paragraph(clean(line[3:]).strip(), h1_style))
    elif line.startswith('### '):
        if in_table and len(table_data) >= 2:
            t = Table(table_data)
            t.setStyle(table_style)
            story.append(t)
            story.append(Spacer(1, 8))
            table_data = []
            in_table = False
        story.append(Paragraph(clean(line[4:]).strip(), h2_style))
    elif '|' in line and line.strip().startswith('|'):
        row = [c.strip() for c in line.split('|') if c.strip()]
        if len(row) > 1:
            if not in_table:
                table_data = []
                in_table = True
            table_data.append(row)
        else:
            if in_table and len(table_data) >= 2:
                t = Table(table_data)
                t.setStyle(table_style)
                story.append(t)
                story.append(Spacer(1, 8))
            table_data = []
            in_table = False
    else:
        if in_table and len(table_data) >= 2:
            t = Table(table_data)
            t.setStyle(table_style)
            story.append(t)
            story.append(Spacer(1, 8))
            table_data = []
            in_table = False
        
        text = line.strip()
        if text and len(text) > 3 and not text.startswith('#'):
            if text.startswith('- '):
                story.append(Paragraph('<bullet>&bull;</bullet> ' + clean(text[2:]), body_style))
            else:
                story.append(Paragraph(clean(text), body_style))

if in_table and len(table_data) >= 2:
    t = Table(table_data)
    t.setStyle(table_style)
    story.append(t)

doc.build(story)

if os.path.exists(pdf_file):
    size = os.path.getsize(pdf_file)
    print(f'PDF created: {pdf_file}')
    print(f'Size: {size/1024:.1f} KB')