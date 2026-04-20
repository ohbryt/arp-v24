#!/usr/bin/env python3
"""Generate Figure 3: Inflammaging Therapeutic Pipeline"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Arrow
import numpy as np

# ── figure setup ──────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(16, 10))
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis('off')
fig.patch.set_facecolor('white')

# ── palette ────────────────────────────────────────────────────────────────────
C_PRECLINICAL = '#22C55E'
C_PHASE1      = '#3B82F6'
C_PHASE2      = '#F97316'
C_DISCOVERY   = '#8B5CF6'
C_BG          = 'white'
C_TEXT        = '#1a1a1a'
C_SUBTEXT     = '#555555'
C_ARROW       = '#aaaaaa'

# ── title ─────────────────────────────────────────────────────────────────────
ax.text(8, 9.6, 'Inflammaging Therapeutic Pipeline',
        ha='center', va='center', fontsize=20, fontweight='bold', color=C_TEXT)
ax.text(8, 9.2, 'Emerging targets across the drug development continuum',
        ha='center', va='center', fontsize=12, color=C_SUBTEXT, style='italic')

# ── phase header helper ────────────────────────────────────────────────────────
def phase_header(ax, x, y, w, label, timeline, color):
    rect = FancyBboxPatch((x, y), w, 0.7,
                          boxstyle="round,pad=0.05",
                          linewidth=1.5, edgecolor=color, facecolor=color,
                          zorder=2)
    ax.add_patch(rect)
    ax.text(x + w/2, y + 0.35, label,
           ha='center', va='center', fontsize=11, fontweight='bold', color='white')
    ax.text(x + w/2, y - 0.18, timeline,
           ha='center', va='top', fontsize=8, color=C_SUBTEXT)

# ── draw three phase columns ───────────────────────────────────────────────────
# Preclinical: x=0.5, w=4.2
# Phase 1:    x=5.5, w=4.2
# Phase 2:    x=10.5, w=5.0

phase_header(ax, 0.5,  8.4, 4.0, 'PRECLINICAL', 'Target ID & Lead Optimization · 2025–2027', C_PRECLINICAL)
phase_header(ax, 5.5,  8.4, 4.0, 'PHASE 1',     'Safety & Tolerability · 2026–2028',          C_PHASE1)
phase_header(ax, 10.5, 8.4, 4.8, 'PHASE 2',     'Efficacy & Dose-Ranging · 2027–2030',        C_PHASE2)

# Discovery banner (spans all)
phase_header(ax, 0.5, 3.4, 14.8, 'DISCOVERY', 'Target Identification & Validation', C_DISCOVERY)

# ── drug card helper ──────────────────────────────────────────────────────────
def drug_card(ax, x, y, w, h, color, title, mechanism, detail, icon_text=''):
    rect = FancyBboxPatch((x, y), w, h,
                          boxstyle="round,pad=0.12",
                          linewidth=1.2, edgecolor=color, facecolor='white',
                          zorder=3)
    ax.add_patch(rect)
    # colored left accent bar
    accent = mpatches.Rectangle((x, y), 0.18, h, facecolor=color, zorder=4)
    ax.add_patch(accent)
    # title
    ax.text(x + 0.32, y + h - 0.28, title,
            ha='left', va='top', fontsize=10.5, fontweight='bold', color=color, zorder=5)
    # mechanism
    ax.text(x + 0.32, y + h - 0.65, mechanism,
            ha='left', va='top', fontsize=8.2, color=C_TEXT, wrap=True, zorder=5,
            multialignment='left')
    # detail / status
    ax.text(x + 0.32, y + 0.18, detail,
            ha='left', va='bottom', fontsize=8.0, color=C_SUBTEXT,
            style='italic', zorder=5)
    # icon badge
    if icon_text:
        ax.text(x + w - 0.22, y + h - 0.22, icon_text,
                ha='right', va='top', fontsize=14, color=color, alpha=0.25, zorder=5)

# ── drug cards ─────────────────────────────────────────────────────────────────
# Row 1 — Preclinical
drug_card(ax,
          x=0.5, y=6.3, w=4.0, h=1.85,
          color=C_PRECLINICAL,
          title='GDF3–SMAD2/3 Inhibitors',
          mechanism='Blocks GDF3 ligand → inhibits SMAD2/3\nsignaling cascade → suppresses\nsenescence-associated inflammation',
          detail='🧬 IND filing expected: 2026–2027')

# Row 2 — Phase 1
drug_card(ax,
          x=5.5, y=6.3, w=4.0, h=1.85,
          color=C_PHASE1,
          title='NLRP3 Inhibitors (MCC940)',
          mechanism='Inhibits NLRP3 inflammasome\nassembly → blocks IL-1β / IL-18\nrelease from primed macrophages',
          detail='📍 Phase 1 · First-in-human 2026')

# Row 3 — Phase 2
drug_card(ax,
          x=10.5, y=6.3, w=4.8, h=1.85,
          color=C_PHASE2,
          title='Mitophagy Inducers — Urolithin A',
          mechanism='Activates PINK1/PARKIN mitophagy →\nclears damaged mitochondria →\nreduces ROS-inflammatory burden',
          detail='📍 Phase 2 · Nat. Aging 2025')

drug_card(ax,
          x=10.5, y=4.0, w=4.8, h=1.85,
          color=C_PHASE2,
          title='Senolytics — Dasatinib + Quercetin (D+Q)',
          mechanism='Inhibits tyrosine kinases (D) +\nflavonoid synergy (Q) →\neliminates senescent cells → reduces SASP',
          detail='📍 Phase 2 · HNSCC indication')

# Row 4 — Discovery
drug_card(ax,
          x=0.5, y=1.4, w=14.8, h=1.85,
          color=C_DISCOVERY,
          title='NAM Restoration / NAD⁺ Boosters',
          mechanism='Nicotinamide riboside / NMN supplementation → restores intracellular NAD⁺ → activates SIRT1–SIRT7 deacylases → improves mitochondrial quality control and bioenergetics',
          detail='🧪 Discovery stage · Biomarker-driven patient stratification')

# ── connecting arrows between phases ──────────────────────────────────────────
arrow_style = dict(arrowstyle='->', color=C_ARROW, lw=1.8, connectionstyle='arc3,rad=0.0')

# arrow from Preclinical to Phase1
ax.annotate('', xy=(10.5, 7.22), xytext=(5.5, 7.22), arrowprops=arrow_style)

# arrow from Phase1 to Phase2
ax.annotate('', xy=(10.5, 7.22), xytext=(9.5, 7.22), arrowprops=arrow_style)

# ── stage arrows (horizontal flow indicators) ─────────────────────────────────
for bx, label in [(2.5, '▶'), (7.5, '▶'), (12.5, '▶')]:
    ax.text(bx, 7.85, label, ha='center', va='center',
            fontsize=9, color=C_ARROW, zorder=2)

# ── timeline bar at bottom ────────────────────────────────────────────────────
tl_y = 0.45
tl_xs = [0.5, 3.0, 5.5, 8.5, 10.5, 13.0, 15.3]
tl_labels = ['2025', '2026', '2027', '2028', '2029', '2030']
tl_colors = [C_PRECLINICAL, C_PHASE1, C_PHASE2, C_PHASE2, C_PHASE2, '#cccccc']

ax.axhline(tl_y, xmin=0.031, xmax=0.969, color='#cccccc', lw=1.0, zorder=1)
for i, (xs, label, col) in enumerate(zip(tl_xs[:6], tl_labels, tl_colors)):
    circle = plt.Circle((xs, tl_y), 0.12, color=col, zorder=3)
    ax.add_patch(circle)
    ax.text(xs, tl_y - 0.32, label, ha='center', va='top', fontsize=7.5, color=C_SUBTEXT)

# ── legend ─────────────────────────────────────────────────────────────────────
legend_items = [
    mpatches.Patch(facecolor=C_PRECLINICAL, label='Preclinical'),
    mpatches.Patch(facecolor=C_PHASE1,      label='Phase 1'),
    mpatches.Patch(facecolor=C_PHASE2,      label='Phase 2'),
    mpatches.Patch(facecolor=C_DISCOVERY,   label='Discovery'),
]
ax.legend(handles=legend_items, loc='lower right',
          ncol=4, fontsize=9, framealpha=0.9,
          edgecolor='#cccccc', title='Development Stage', title_fontsize=9,
          bbox_to_anchor=(0.99, 0.01))

# ── footnote ──────────────────────────────────────────────────────────────────
ax.text(0.5, 0.12,
        'Abbreviations: GDF3 = growth differentiation factor 3; NLRP3 = NLR family pyrin domain containing 3; '
        'IL = interleukin; SASP = senescence-associated secretory phenotype; NAM = nicotinamide; '
        'NAD⁺ = nicotinamide adenine dinucleotide; HNSCC = head & neck squamous cell carcinoma; '
        'IND = investigational new drug; NMN = nicotinamide mononucleotide.',
        ha='left', va='bottom', fontsize=7, color='#888888', wrap=True)

# ── save ──────────────────────────────────────────────────────────────────────
out = '/Users/ocm/.openclaw/workspace/arp-v24/figures/fig3_therapeutic_pipeline.png'
plt.savefig(out, dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print(f'Saved → {out}')
