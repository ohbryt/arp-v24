#!/usr/bin/env python3
"""
ARP Report to Beautiful Infographic Generator
Simple script to generate HTML infographics from markdown reports.

Usage:
    python3 scripts/generate_infographic.py <markdown_file>
"""

import os
import sys
from pathlib import Path

def generate_html_template(title):
    """Generate a beautiful HTML infographic template"""
    
    html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --brand: #2563eb;
            --brand-2: #7c3aed;
            --accent: #0f766e;
            --text: #1f2937;
            --muted: #6b7280;
            --bg: #f8fafc;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Noto Sans KR', -apple-system, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
        }}
        
        .header {{
            background: linear-gradient(135deg, var(--brand), var(--brand-2));
            color: white;
            padding: 60px 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 10px;
        }}
        
        .header .subtitle {{
            font-size: 1.2rem;
            opacity: 0.9;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        
        .section {{
            margin-bottom: 50px;
        }}
        
        .section-title {{
            font-size: 1.5rem;
            color: var(--brand);
            border-left: 5px solid var(--accent);
            padding-left: 15px;
            margin-bottom: 20px;
        }}
        
        .cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}
        
        .card {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        
        .card:hover {{
            transform: translateY(-5px);
        }}
        
        .card-icon {{
            font-size: 2rem;
            margin-bottom: 15px;
        }}
        
        .card h3 {{
            color: var(--brand);
            margin-bottom: 10px;
            font-size: 1.1rem;
        }}
        
        .card p {{
            color: var(--muted);
            font-size: 0.95rem;
        }}
        
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .data-table th {{
            background: linear-gradient(135deg, var(--brand), var(--brand-2));
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 500;
        }}
        
        .data-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e5e7eb;
        }}
        
        .key-points {{
            background: linear-gradient(135deg, #e0e7ff, #c7d2fe);
            border: 2px solid var(--brand);
            border-radius: 12px;
            padding: 25px;
            margin: 20px 0;
        }}
        
        .key-points h3 {{
            color: var(--brand);
            margin-bottom: 15px;
        }}
        
        .key-points ul {{
            list-style: none;
            padding: 0;
        }}
        
        .key-points li {{
            padding: 8px 0;
            padding-left: 25px;
            position: relative;
        }}
        
        .key-points li::before {{
            content: "✓";
            position: absolute;
            left: 0;
            color: var(--accent);
            font-weight: bold;
        }}
        
        .footer {{
            background: var(--text);
            color: white;
            text-align: center;
            padding: 30px;
            margin-top: 50px;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 1.8rem; }}
            .cards {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
        <p class="subtitle">ARP Drug Discovery Research Report</p>
    </div>
    
    <div class="container">
        <div class="section">
            <h2 class="section-title">🔬 Key Findings</h2>
            <div class="key-points">
                <h3>Summary of Critical Discoveries</h3>
                <ul>
                    <li>Research finding 1 - details here</li>
                    <li>Research finding 2 - details here</li>
                    <li>Research finding 3 - details here</li>
                </ul>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">🧬 Biological Mechanisms</h2>
            <div class="cards">
                <div class="card">
                    <div class="card-icon">🧪</div>
                    <h3>Mechanism 1</h3>
                    <p>Description of the first biological mechanism.</p>
                </div>
                <div class="card">
                    <div class="card-icon">⚡</div>
                    <h3>Mechanism 2</h3>
                    <p>Description of the second mechanism.</p>
                </div>
                <div class="card">
                    <div class="card-icon">🔗</div>
                    <h3>Mechanism 3</h3>
                    <p>Description of the third mechanism.</p>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">💊 Therapeutic Opportunities</h2>
            <div class="cards">
                <div class="card">
                    <div class="card-icon">🎯</div>
                    <h3>Priority Target</h3>
                    <p>Primary therapeutic indication and development strategy.</p>
                </div>
                <div class="card">
                    <div class="card-icon">🔄</div>
                    <h3>Drug Repositioning</h3>
                    <p>Existing drugs that could be repurposed.</p>
                </div>
                <div class="card">
                    <div class="card-icon">🧪</div>
                    <h3>De Novo Design</h3>
                    <p>New molecular entities for targeted therapy.</p>
                </div>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <p>ARP v24 Drug Discovery Framework • Generated 2026-04-19</p>
        <p style="margin-top:5px; opacity:0.6;">Powered by Claude Code + Groq API</p>
    </div>
</body>
</html>'''
    
    return html


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/generate_infographic.py <markdown_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    base_name = Path(input_file).stem
    title = base_name.replace('_', ' ')
    
    html_file = f"/tmp/{base_name}_infographic.html"
    
    html = generate_html_template(title)
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ Generated: {html_file}")
    return html_file


if __name__ == '__main__':
    main()
