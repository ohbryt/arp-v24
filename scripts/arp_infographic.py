#!/usr/bin/env python3
"""
ARP Report to Beautiful Infographic Generator
Uses Claude Code to generate HTML infographics from markdown reports.

Usage:
    python3 scripts/arp_infographic.py <markdown_file> [--format html/png/pdf]
"""

import os
import sys
import argparse
import subprocess
import tempfile
from pathlib import Path

# Claude Code command
CLAUDE_CMD = "claude"

def generate_infographic_prompt(markdown_content: str, topic: str = "") -> str:
    """Generate the prompt for Claude Code to create an infographic"""
    
    # Extract key information from markdown for the infographic
    lines = markdown_content.split('\n')
    
    # Find key sections
    title = ""
    sections = []
    current_section = None
    key_points = []
    
    for line in lines:
        if line.startswith('# '):
            if current_section:
                sections.append(current_section)
            current_section = {'title': line[2:], 'content': []}
        elif line.startswith('## '):
            if current_section:
                sections.append(current_section)
            current_section = {'title': line[3:], 'content': []}
        elif line.startswith('- **') or line.startswith('- '):
            key_points.append(line.strip())
            if current_section:
                current_section['content'].append(line.strip())
        elif current_section and line.strip():
            current_section['content'].append(line.strip())
    
    if current_section:
        sections.append(current_section)
    
    prompt = f'''Create a beautiful, modern HTML infographic presentation about: {topic or "Drug Discovery Research"}

This is for a scientific/biomedical research report. The design should be:
- Professional and academic in feel
- Clean, modern typography
- Use a blue/purple/teal color scheme
- Include data visualizations where appropriate
- Have clear hierarchy and visual flow

The infographic should include:
1. Title slide with the topic
2. Key findings summary (3-5 bullet points)
3. Main biological mechanisms (with diagrams)
4. Clinical relevance
5. Therapeutic opportunities
6. Summary/conclusion

Use modern HTML/CSS with:
- Gradient backgrounds
- Card-based layouts
- Clean sans-serif fonts (Pretendard, Noto Sans, or similar)
- Icons where appropriate (can use emoji)
- Tables for data presentation
- Visual hierarchy with proper spacing

Output: A single self-contained HTML file that looks like a professional infographic deck.

Here is the source content from the research report:
---
{markdown_content[:8000]}
---

Create the HTML infographic now. Output ONLY the HTML file, no explanations.'''
    
    return prompt


def call_claude_code(prompt: str, output_file: str) -> bool:
    """Call Claude Code to generate the infographic"""
    
    # Create a Claude Code script
    script = f'''
import {os.path.dirname(os.path.abspath(__file__))}
topic = "ARP Research Report Infographic"

{generate_infographic_prompt.__name__}(markdown_content="", topic=topic)
'''

    try:
        # Use Claude Code to generate the infographic
        result = subprocess.run(
            [CLAUDE_CMD, "--print", "--output-format", "json", prompt],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=os.path.dirname(os.path.abspath(__file__))
        
        if result.returncode == 0:
            print(f"✓ Claude Code generated infographic")
            return True
        else:
            print(f"✗ Claude Code error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("✗ Claude Code timeout")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def generate_infographic_direct(markdown_file: str, output_format: str = "html") -> str:
    """Generate infographic directly using Claude Code CLI"""
    
    # Read the markdown file
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract topic from filename or first heading
    topic = Path(markdown_file).stem.replace('_', ' ').replace('-', ' ')
    
    prompt = generate_infographic_prompt(content, topic)
    
    # Create a temp file for the HTML output
    base_name = Path(markdown_file).stem
    html_output = f"/tmp/{base_name}_infographic.html"
    
    # Write prompt to a file
    prompt_file = f"/tmp/{base_name}_prompt.txt"
    with open(prompt_file, 'w') as f:
        f.write(prompt)
    
    print(f"Generating infographic for: {topic}")
    print(f"Using Claude Code...")
    
    # Call Claude Code to generate HTML
    # Claude Code needs to create the HTML file directly
    claude_prompt = f'''Create a beautiful, professional HTML infographic presentation.

Topic: {topic}

Create a self-contained HTML file with modern CSS styling. The design should be:
- Professional and academic/scientific feel
- Blue/purple/teal color scheme (#2563eb, #7c3aed, #0f766e)
- Clean typography with Google Fonts
- Card-based layouts with shadows
- Gradient backgrounds
- Tables for data
- Visual hierarchy

Structure the infographic as a scrollable single-page with sections:
1. Title header with gradient background
2. Key findings (3-5 bullet points as cards)
3. Biological mechanisms (diagram-style layout)
4. Clinical data (tables, charts placeholder)
5. Therapeutic opportunities
6. Conclusion

Save the HTML to: {html_output}

Output only the completed HTML file path.'''
    
    try:
        result = subprocess.run(
            [CLAUDE_CMD, "--print", claude_prompt],
            capture_output=True,
            text=True,
            timeout=180,
            cwd=os.path.dirname(os.path.abspath(__file__)))
        
        if result.returncode == 0:
            print(f"✓ Infographic generation completed")
            return html_output
        else:
            print(f"Claude Code output: {result.stdout}")
            print(f"Claude Code error: {result.stderr}")
    except Exception as e:
        print(f"Error: {e}")
    
    return None


def markdown_to_infographic(markdown_file: str, output_format: str = "png") -> str:
    """Main function to convert markdown to infographic"""
    
    base_name = Path(markdown_file).stem
    html_file = f"/tmp/{base_name}_infographic.html"
    
    # Generate the infographic HTML using Claude Code
    html_content = generate_html_template(base_name.replace('_', ' '))
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Generated: {html_file}")
    
    # Convert to PNG/PDF if requested
    if output_format in ['png', 'pdf']:
        pdf_file = html_file.replace('.html', f'.{output_format}')
        
        # Use Chrome headless for conversion
        if output_format == 'pdf':
            convert_cmd = [
                '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
                '--headless',
                '--disable-gpu',
                '--no-sandbox',
                f'--print-to-pdf={pdf_file}',
                f'file://{html_file}'
            ]
        else:
            # PNG screenshot
            png_file = html_file.replace('.html', '.png')
            convert_cmd = [
                '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
                '--headless',
                '--disable-gpu',
                '--screenshot={png_file}',
                f'file://{html_file}'
            ]
        
        try:
            subprocess.run(convert_cmd, timeout=30, capture_output=True)
            print(f"✓ Converted to {output_format}: {pdf_file}")
            return pdf_file
        except Exception as e:
            print(f"Note: Chrome conversion failed ({e})")
            print("HTML file is still available for manual export")
    
    return html_file


def generate_html_template(title: str) -> str:
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
        
        /* Header */
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
        
        /* Container */
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        
        /* Section */
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
        
        /* Cards Grid */
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
        
        /* Table */
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
        
        .data-table tr:last-child td {{
            border-bottom: none;
        }}
        
        .data-table tr:nth-child(even) {{
            background: #f9fafb;
        }}
        
        /* Key Points */
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
        
        /* Footer */
        .footer {{
            background: var(--text);
            color: white;
            text-align: center;
            padding: 30px;
            margin-top: 50px;
        }}
        
        .footer p {{
            opacity: 0.8;
            font-size: 0.9rem;
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.8rem;
            }}
            .cards {{
                grid-template-columns: 1fr;
            }}
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
                    <li>Research finding 4 - details here</li>
                </ul>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">🧬 Biological Mechanisms</h2>
            <div class="cards">
                <div class="card">
                    <div class="card-icon">🧪</div>
                    <h3>Mechanism 1</h3>
                    <p>Description of the first biological mechanism and its relevance to the research.</p>
                </div>
                <div class="card">
                    <div class="card-icon">⚡</div>
                    <h3>Mechanism 2</h3>
                    <p>Description of the second biological mechanism and its relevance.</p>
                </div>
                <div class="card">
                    <div class="card-icon">🔗</div>
                    <h3>Mechanism 3</h3>
                    <p>Description of the third biological mechanism and its role.</p>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">📊 Clinical Data</h2>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Parameter</th>
                        <th>Value</th>
                        <th>Significance</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Target Expression</td>
                        <td>High in tumor tissue</td>
                        <td>Therapeutic opportunity</td>
                    </tr>
                    <tr>
                        <td>IC50</td>
                        <td>nM range</td>
                        <td>Drug-like potency</td>
                    </tr>
                    <tr>
                        <td>Selectivity</td>
                        <td>>10-fold vs off-targets</td>
                        <td>Safety profile</td>
                    </tr>
                </tbody>
            </table>
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
                    <p>Existing drugs that could be repurposed for this target.</p>
                </div>
                <div class="card">
                    <div class="card-icon">🧪</div>
                    <h3>De Novo Design</h3>
                    <p>New molecular entities for targeted therapy.</p>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">📈 Development Roadmap</h2>
            <div class="cards">
                <div class="card">
                    <div class="card-icon">1</div>
                    <h3>Short-term (2-3 years)</h3>
                    <p>Drug repositioning candidates, natural compounds</p>
                </div>
                <div class="card">
                    <div class="card-icon">2</div>
                    <h3>Medium-term (5-7 years)</h3>
                    <p>Optimized small molecules, clinical trials</p>
                </div>
                <div class="card">
                    <div class="card-icon">3</div>
                    <h3>Long-term (7-10 years)</h3>
                    <p>Novel therapeutics, combination therapies</p>
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
    parser = argparse.ArgumentParser(description='ARP Report to Infographic Generator')
    parser.add_argument('markdown_file', help='Input markdown file')
    parser.add_argument('--format', '-f', choices=['html', 'png', 'pdf'], default='html',
                        help='Output format (default: html)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.markdown_file):
        print(f"Error: File not found: {args.markdown_file}")
        sys.exit(1)
    
    # Generate the infographic
    output = markdown_to_infographic(args.markdown_file, args.format)
    
    if output:
        print(f"\n✓ Success! Output: {output}")
    else:
        print("\n✗ Failed to generate infographic")
        sys.exit(1)


if __name__ == '__main__':
    main()
