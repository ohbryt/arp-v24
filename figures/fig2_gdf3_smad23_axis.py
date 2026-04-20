#!/usr/bin/env python3
"""
Figure 2: GDF3-SMAD2/3 Signaling Axis in Adipose Tissue Macrophages
Publication-quality molecular pathway diagram v2
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Arc
import numpy as np

# Color scheme
COLORS = {
    'AGE': '#EA580C',           # Dark orange
    'GDF3': '#7C3AED',           # Purple
    'SMAD': '#2563EB',           # Blue  
    'INFLAMMATION': '#DC2626',   # Red
    'ATM': '#DBEAFE',            # Very light blue (cell)
    'ATM_EDGE': '#3B82F6',       # Blue edge
    'CHROMATIN': '#A78BFA',      # Light purple
    'INHIBITOR': '#B91C1C',      # Dark red
    'WHITE': '#FFFFFF',
    'BLACK': '#111827',
    'GRAY': '#6B7280',
}

fig, ax = plt.subplots(1, 1, figsize=(14, 10), facecolor='white')
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.axis('off')

def draw_box(ax, x, y, w, h, text, color, text_color='white', fontsize=11, edgecolor=None, linewidth=2):
    """Draw a rounded rectangle box with text"""
    if edgecolor is None:
        edgecolor = color
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                         boxstyle='round,pad=0.1',
                         facecolor=color,
                         edgecolor=edgecolor,
                         linewidth=linewidth,
                         zorder=3)
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize,
            color=text_color, fontweight='bold', zorder=4)

def draw_arrow(ax, start, end, color='#374151', lw=2):
    """Draw an arrow between two points"""
    arr = FancyArrowPatch(start, end,
                          arrowstyle='->',
                          mutation_scale=18,
                          connectionstyle='arc3,rad=0',
                          color=color,
                          linewidth=lw,
                          zorder=2)
    ax.add_patch(arr)

def draw_inhibitor_Tbar(ax, start, end, color=COLORS['INHIBITOR']):
    """Draw a T-bar inhibition symbol"""
    ax.annotate('', xy=end, xytext=start,
                arrowprops=dict(arrowstyle='->', color=color, lw=2.5),
                zorder=4)
    # T-bar at the arrowhead
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = np.sqrt(dx**2 + dy**2)
    if length > 0:
        # Perpendicular bar
        bar_len = 0.25
        nx = -dy/length * bar_len
        ny = dx/length * bar_len
        ax.plot([end[0] - nx, end[0] + nx], [end[1] - ny, end[1] + ny], 
                color=color, linewidth=4, zorder=5)

def draw_dna_strand(ax, x, y, length=2):
    """Draw a simplified DNA strand"""
    for i in range(8):
        x_pos = x - length/2 + i * length/7
        y_offset = 0.12 * np.sin(i * np.pi / 2)
        ax.plot([x_pos, x_pos], [y - y_offset, y + y_offset], 
                color=COLORS['CHROMATIN'], linewidth=2.5, zorder=3)
    for i in range(7):
        x_pos = x - length/2 + (i + 0.5) * length/7
        ax.plot([x_pos - 0.08, x_pos + 0.08], [y - 0.1, y + 0.1], 
                color='#6366F1', linewidth=2, zorder=3)

# ========== TITLE ==========
ax.text(7, 9.6, 'Fig. 2', fontsize=12, fontweight='bold', ha='center', va='center', color=COLORS['BLACK'])
ax.text(7, 9.2, 'GDF3-SMAD2/3 Signaling Axis in Adipose Tissue Macrophages', 
        fontsize=12, fontweight='bold', ha='center', va='center', color=COLORS['BLACK'])

# ========== TOP: AGE → GDF3 Expression ==========
draw_box(ax, 7, 8.3, 1.8, 0.6, 'AGE', COLORS['AGE'], fontsize=11)

draw_arrow(ax, (7, 7.95), (7, 7.55))

draw_box(ax, 7, 7.2, 2.6, 0.6, '↑ GDF3 Expression', COLORS['GDF3'], fontsize=11)

# ========== ATM Cell Boundary ==========
cell_x, cell_y = 6.5, 4.8
cell_w, cell_h = 5.5, 3.8

cell_boundary = FancyBboxPatch((cell_x - cell_w/2, cell_y - cell_h/2), cell_w, cell_h,
                                boxstyle='round,pad=0.1',
                                facecolor=COLORS['ATM'],
                                edgecolor=COLORS['ATM_EDGE'],
                                linewidth=2.5,
                                zorder=1)
ax.add_patch(cell_boundary)
ax.text(cell_x - cell_w/2 + 0.3, cell_y + cell_h/2 - 0.3, 'ATM', fontsize=12, 
        ha='left', va='top', color=COLORS['ATM_EDGE'], fontweight='bold', zorder=4)

# ========== Inside ATM ==========

# GDF3 Receptor
draw_box(ax, 4.5, 6.0, 1.9, 0.55, 'GDF3 Receptor', COLORS['GDF3'], fontsize=10)

# Arrow from GDF3 Expression to receptor
draw_arrow(ax, (7, 6.9), (5.45, 6.25), color=COLORS['GDF3'], lw=2)

# SMAD2/3 activation
draw_box(ax, 4.5, 5.0, 1.6, 0.55, 'SMAD2/3', COLORS['SMAD'], fontsize=11)
draw_arrow(ax, (4.5, 5.7), (4.5, 5.3), color=COLORS['SMAD'], lw=2)

# H3K27me3 loss
draw_box(ax, 6.5, 5.0, 1.9, 0.55, 'H3K27me3 loss', COLORS['CHROMATIN'], fontsize=10)
draw_arrow(ax, (5.3, 5.0), (5.55, 5.0), color=COLORS['SMAD'], lw=2)

# Chromatin Remodeling label
ax.text(6.5, 4.55, 'Chromatin\nRemodeling', fontsize=8, ha='center', va='top', 
        color=COLORS['GRAY'], style='italic')

# DNA strand
draw_dna_strand(ax, 6.5, 4.3, length=1.4)
ax.text(6.5, 3.95, 'Gene Loci', fontsize=8, ha='center', va='top', color=COLORS['GRAY'])
draw_arrow(ax, (6.5, 4.7), (6.5, 4.55), color=COLORS['CHROMATIN'], lw=1.5)

# ========== Pro-inflammatory Genes (single box) ==========
draw_box(ax, 9.2, 5.0, 2.0, 1.3, '', COLORS['INFLAMMATION'], fontsize=10, edgecolor=COLORS['INFLAMMATION'])
ax.text(9.2, 5.4, 'Pro-inflammatory', fontsize=9, ha='center', va='center', 
        color='white', fontweight='bold', zorder=4)
ax.text(9.2, 5.1, 'Cytokines', fontsize=9, ha='center', va='center', 
        color='white', fontweight='bold', zorder=4)
ax.text(9.2, 4.65, 'IL-6  TNF-α  MCP-1', fontsize=8, ha='center', va='center', 
        color='white', zorder=4)

# Arrows from DNA to cytokine box
draw_arrow(ax, (7.2, 4.9), (8.2, 5.0), color=COLORS['INFLAMMATION'], lw=2)

# ========== SYSTEMIC EFFECTS ==========
draw_arrow(ax, (10.2, 4.8), (11.5, 4.0), color=COLORS['INFLAMMATION'], lw=2.5)

draw_box(ax, 12.0, 3.5, 1.8, 0.8, 'Systemic\nInflammation', COLORS['INFLAMMATION'], fontsize=10)

draw_arrow(ax, (12.0, 3.1), (12.0, 2.3), color=COLORS['INFLAMMATION'], lw=2)

draw_box(ax, 12.0, 1.8, 1.8, 0.7, 'Endotoxemia\nSusceptibility', COLORS['INFLAMMATION'], fontsize=10)

# ========== PHARMACOLOGICAL INTERVENTION ==========
# GDF3 Inhibitor - positioned to show it blocks the receptor
draw_box(ax, 2.2, 6.0, 2.0, 0.55, 'GDF3 Inhibitor', 'white', text_color=COLORS['INHIBITOR'], 
         fontsize=10, edgecolor=COLORS['INHIBITOR'], linewidth=2.5)
draw_inhibitor_Tbar(ax, (2.2, 5.7), (3.9, 6.1), color=COLORS['INHIBITOR'])

# SMAD2/3 Inhibitor - positioned to show it blocks SMAD
draw_box(ax, 2.2, 4.5, 2.0, 0.55, 'SMAD2/3 Inhibitor', 'white', text_color=COLORS['INHIBITOR'], 
         fontsize=10, edgecolor=COLORS['INHIBITOR'], linewidth=2.5)
draw_inhibitor_Tbar(ax, (2.2, 4.2), (3.7, 5.1), color=COLORS['INHIBITOR'])

# ========== LEGEND ==========
legend_x = 0.4
legend_y = 1.6

ax.text(legend_x, legend_y + 0.7, 'Legend:', fontsize=9, fontweight='bold', color=COLORS['BLACK'])

# Activation arrow
ax.annotate('', xy=(legend_x + 0.6, legend_y + 0.35), xytext=(legend_x + 0.1, legend_y + 0.35),
            arrowprops=dict(arrowstyle='->', color='black', lw=2))
ax.text(legend_x + 0.75, legend_y + 0.35, 'Activation', fontsize=8, va='center', color=COLORS['BLACK'])

# Inhibition T-bar
ax.plot([legend_x + 0.1, legend_x + 0.6], [legend_y, legend_y], color=COLORS['INHIBITOR'], lw=2.5)
ax.plot([legend_x + 0.1, legend_x + 0.6], [legend_y - 0.1, legend_y + 0.1], color=COLORS['INHIBITOR'], lw=3)
ax.text(legend_x + 0.75, legend_y, 'Inhibition', fontsize=8, va='center', color=COLORS['BLACK'])

# Color legend
legend_elements = [
    mpatches.Patch(color=COLORS['AGE'], label='AGE'),
    mpatches.Patch(color=COLORS['GDF3'], label='GDF3 / Receptor'),
    mpatches.Patch(color=COLORS['SMAD'], label='SMAD2/3'),
    mpatches.Patch(color=COLORS['CHROMATIN'], label='Chromatin State'),
    mpatches.Patch(color=COLORS['INFLAMMATION'], label='Inflammatory Output'),
]
ax.legend(handles=legend_elements, loc='lower left', fontsize=7.5, framealpha=0.95,
          bbox_to_anchor=(0.0, 0.0), ncol=1)

# ========== SAVE ==========
plt.tight_layout()
output_path = '/Users/ocm/.openclaw/workspace/arp-v24/figures/fig2_gdf3_smad23_axis.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()
print(f"Figure saved to: {output_path}")
