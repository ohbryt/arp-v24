#!/usr/bin/env python3
"""
Fig. 5 — NAMs in Adipose Tissue Homeostasis
Publication-quality 3-panel scientific figure
Gonzalez-Hurtado et al. 2025, Nature Aging
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Ellipse
import numpy as np
from matplotlib.lines import Line2D

# ── Colours ───────────────────────────────────────────────────────────────────
C_ADIP   = '#F5D98B'
C_ADIP_O = '#8B6914'
C_NAM    = '#00B5AD'
C_NAM_LT = '#B2E8E5'
C_NERVE  = '#CC2222'
C_NERVE_D= '#882222'
C_IL10   = '#7CB342'
C_FIB    = '#689F38'
C_M1     = '#FF6B4A'
C_M2     = '#80CBC4'
C_MAST   = '#FF69B4'
C_EOS    = '#FFA07A'
C_TC     = '#9575CD'
C_RED    = '#D32F2F'
C_WHITE  = 'white'

# ── Figure setup ───────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(18, 10))
fig.patch.set_facecolor(C_WHITE)
ax.set_facecolor(C_WHITE)
ax.set_xlim(0, 18); ax.set_ylim(0, 10); ax.axis('off')

# ── Panel headers ─────────────────────────────────────────────────────────────
for x, label in [(2.5,'A'), (8.5,'B'), (14.5,'C')]:
    ax.text(x, 9.7, label, fontsize=22, fontweight='bold', ha='center', va='top')
titles = ['Young Adipose Tissue', 'Aged Adipose Tissue', 'NAM Functions & Age-Related Decline']
for x, t in zip([2.5, 8.5, 14.5], titles):
    ax.text(x, 9.3, t, fontsize=13, fontweight='bold', ha='center', va='top', color='#333')

# ── Helpers ────────────────────────────────────────────────────────────────────
def adipocyte(cx, cy, r, a=1.0):
    ax.add_patch(Ellipse((cx,cy), r*2, r*1.7, facecolor=C_ADIP, edgecolor=C_ADIP_O, lw=1.2, alpha=a))
    ax.add_patch(Ellipse((cx,cy), r*0.85, r*0.65, facecolor='#FFF9C4', edgecolor='#F9A825', lw=0.5, alpha=a*0.7))

def nam(cx, cy, r, dim=False, dash=False):
    fc  = '#4DD0C5' if not dim else '#90D4D0'
    ec  = C_NAM if not dim else '#5DB5B0'
    lw  = 2.0 if not dim else 1.0
    ls  = 'solid' if not dash else (0,(4,3))
    ax.add_patch(Ellipse((cx,cy), r*2.4, r*2.0, facecolor=fc, edgecolor=ec, lw=lw, ls=ls, alpha=0.85 if not dim else 0.45))
    if not dim and not dash:
        ax.add_patch(Ellipse((cx-r*0.2,cy+r*0.1), r*0.7, r*0.5, facecolor='#00695C', ec='none', alpha=0.55))
        for ang, ln in [(200,r*1.4),(160,r*1.1),(240,r*1.0),(110,r*0.9),(290,r*0.8),(70,r*0.6)]:
            r_=np.radians(ang); ax.plot([cx,cx+np.cos(r_)*ln],[cy,cy+np.sin(r_)*ln], color=ec, lw=1.6, alpha=0.75, zorder=7)

def mast(cx, cy, r):
    ax.add_patch(Circle((cx,cy), r, facecolor=C_MAST, edgecolor='#C2185B', lw=0.8, alpha=0.85))
    ax.scatter(cx, cy, s=6, color='#880E4F', zorder=5)

def eos(cx, cy, r):
    ax.add_patch(Circle((cx,cy), r, facecolor=C_EOS, edgecolor='#BF360C', lw=0.8, alpha=0.85))

def tc(cx, cy, r):
    ax.add_patch(Circle((cx,cy), r, facecolor=C_TC, edgecolor='#4527A0', lw=0.8, alpha=0.85))

def m1(cx, cy, r):
    ax.add_patch(Ellipse((cx,cy), r*2.2, r*2.0, facecolor=C_M1, edgecolor='#BF360C', lw=1.0, alpha=0.85))
    ax.add_patch(Ellipse((cx,cy), r*0.8, r*0.5, facecolor='#D32F2F', ec='none', alpha=0.5))

def m2(cx, cy, r):
    ax.add_patch(Ellipse((cx,cy), r*2.2, r*2.0, facecolor=C_M2, edgecolor='#00796B', lw=1.0, alpha=0.85))

def fibrosis(cx, cy, w, h, a=0.45):
    ax.add_patch(Ellipse((cx,cy), w, h, facecolor=C_FIB, ec='none', alpha=a))

def nerve(pts, col=C_NERVE, lw=1.5, al=1.0):
    xs,ys=zip(*pts); ax.plot(xs,ys,color=col,lw=lw,alpha=al,zorder=2)

def cytokine(cx, cy, lbl, col=C_IL10):
    ax.scatter(cx,cy,s=28,color=col,zorder=8,alpha=0.9)
    ax.text(cx+0.1,cy+0.07,lbl,fontsize=6,color='#33691E',zorder=9)

def scalebar(x0, x1, y, lbl):
    ax.plot([x0,x1],[y,y],color='black',lw=1.5)
    ax.text((x0+x1)/2, y-0.22, lbl, fontsize=8, ha='center')

# ════════════════════════════════════════════════════════════════════════════════
# PANEL A — Young
# ════════════════════════════════════════════════════════════════════════════════
np.random.seed(42)
for x,y,r in [(1.4,5.5,.75),(2.6,5.5,.72),(3.8,5.5,.78),(1.0,4.0,.80),(2.2,4.0,.73),
              (3.4,4.0,.76),(4.6,4.0,.70),(1.4,2.5,.77),(2.6,2.5,.74),(3.8,2.5,.71),
              (1.0,1.0,.75),(2.2,1.0,.78),(3.4,1.0,.72),(4.6,1.0,.69),(5.0,5.5,.68),
              (4.1,2.5,.73),(5.0,2.5,.65),(4.1,1.0,.70)]:
    adipocyte(x,y,r)

nerve([(2.5,0.5),(2.4,1.5),(2.6,2.5),(2.4,3.5),(2.5,4.5),(2.4,5.5),(2.6,6.5)])
nerve([(3.5,0.5),(3.6,1.5),(3.4,2.5),(3.6,3.5),(3.5,4.5),(3.4,5.5)])
nerve([(1.8,1.5),(1.9,2.5),(1.7,3.5),(1.9,4.5)], col='#FF4444', lw=1.2)
nerve([(4.2,2.5),(4.3,3.5),(4.1,4.5),(4.3,5.5)], col='#FF4444', lw=1.2)

nam(2.4,5.5,.28); nam(3.5,3.5,.26); nam(1.9,2.5,.27); nam(2.6,1.5,.26)

mast(1.2,3.2,.18); mast(4.4,2.8,.17)
eos(2.9,3.3,.18); eos(3.9,1.5,.17)
tc(1.7,5.8,.17); tc(4.7,3.5,.16)
m2(0.8,2.2,.20)

cytokine(2.8,6.2,'IL-10'); cytokine(2.0,4.2,'TGF-β'); cytokine(3.3,2.8,'IL-10')

ax.annotate('',xy=(1.4,5.5),xytext=(3.1,5.7),arrowprops=dict(arrowstyle='->',color=C_IL10,lw=2.0))
ax.text(2.2,5.9,'Lipolysis\nregulation',fontsize=7.5,color='#33691E',ha='center',fontweight='bold')

scalebar(0.7,2.2,0.5,'50 μm')

# ════════════════════════════════════════════════════════════════════════════════
# PANEL B — Aged
# ════════════════════════════════════════════════════════════════════════════════
rng = np.random.default_rng(43)
for x,y,r in [(6.8,5.5,.62),(7.9,5.5,.58),(9.0,5.5,.60),(6.4,4.0,.65),(7.6,4.0,.58),
              (8.8,4.0,.55),(10.0,4.0,.52),(6.8,2.5,.60),(8.0,2.5,.57),(9.2,2.5,.54),
              (6.4,1.0,.62),(7.6,1.0,.58),(8.8,1.0,.55),(10.0,1.0,.50),(10.2,5.5,.50)]:
    adipocyte(x,y,r,a=0.88)

for i in range(5):
    fibrosis(6.5+i*0.9+rng.random()*0.3, 3.0+rng.random()*1.5,
             0.6+rng.random()*0.4, 0.15+rng.random()*0.1, a=0.45)
for i in range(4):
    fibrosis(7.0+i*0.8+rng.random()*0.2, 0.9+rng.random()*0.8,
             0.5+rng.random()*0.3, 0.12, a=0.40)

nerve([(7.5,0.5),(7.6,1.5),(7.4,2.5),(7.6,3.5),(7.5,4.5),(7.6,5.5),(7.4,6.5)],
      col=C_NERVE_D, lw=1.0, al=0.45)
nerve([(8.5,0.5),(8.4,1.5),(8.6,2.5),(8.4,3.5),(8.5,4.5)],
      col=C_NERVE_D, lw=0.8, al=0.35)

nam(7.6,5.5,.26,dim=True,dash=True); nam(8.5,3.5,.24,dim=True,dash=True)
ax.text(7.6,5.0,'↓NAMs',fontsize=7,color='#00695C',ha='center',fontweight='bold',alpha=0.7)
ax.text(8.5,3.0,'↓NAMs',fontsize=7,color='#00695C',ha='center',fontweight='bold',alpha=0.7)

for x,y,_ in [(6.9,4.8,.22),(7.2,2.2,.21),(9.3,5.0,.23),(8.5,2.0,.22),
              (10.1,2.8,.20),(6.5,1.3,.21)]:
    m1(x,y,0.21)

mast(7.5,4.2,.17); mast(9.5,2.5,.18); mast(6.7,3.2,.16)

ax.annotate('',xy=(9.5,6.2),xytext=(9.5,5.5),arrowprops=dict(arrowstyle='->',color=C_RED,lw=2.5))
ax.annotate('',xy=(8.0,3.3),xytext=(8.0,2.5),arrowprops=dict(arrowstyle='->',color=C_RED,lw=2.0))
ax.text(10.8,5.8,'Unrestrained\nlipolysis',fontsize=8,color=C_RED,ha='left',fontweight='bold')
cytokine(8.1,3.9,'IL-10',col='#A5D6A7')
ax.text(8.5,3.6,'(low)',fontsize=6,color='#33691E',alpha=0.6)

scalebar(5.8,7.3,0.5,'50 μm')

# ════════════════════════════════════════════════════════════════════════════════
# PANEL C — NAM Functions & Cascade
# ════════════════════════════════════════════════════════════════════════════════
nam(14.5,6.0,.38)
ax.text(14.5,6.75,'NAM',fontsize=10,fontweight='bold',color=C_NAM,ha='center')

funcs = [
    ('Lipolysis\nControl',         14.5, 7.7,  C_IL10,  -90,  '#33691E'),
    ('Inflammation\nRestraint\n(IL-10, TGF-β)', 16.3, 5.2, C_IL10, 20, '#33691E'),
    ('Tissue Repair\n& Remodeling',12.7, 5.2, '#9C27B0', -20, '#4A148C'),
]
for lbl,tx,ty,col,ang,tc in funcs:
    ax.annotate('',xy=(tx,ty),xytext=(14.5,6.38),
               arrowprops=dict(arrowstyle='->',color=col,lw=2.5,connectionstyle='arc3,rad=0.15'))
    ax.text(tx,ty,lbl,fontsize=8,color=tc,ha='center',va='center',fontweight='bold',
            bbox=dict(facecolor='white',edgecolor=col,boxstyle='round,pad=0.3',alpha=0.9))

steps  = ['NAM\ndepletion','Loss of\nlipolysis\ncontrol','Unrestrained\ninflammation','Adipose\nfibrosis']
cols2  = [C_NAM, C_RED, C_M1, C_FIB]
xs_c   = [11.2, 12.8, 14.4, 16.0]
y_c    = 2.8
ax.text(13.6,y_c+1.05,'Age-related NAM decline',fontsize=10,fontweight='bold',color='#333',ha='center')

for i,(step,col,x) in enumerate(zip(steps,cols2,xs_c)):
    rect = FancyBboxPatch((x-0.7,y_c-0.55),1.4,1.1,
                          boxstyle='round,pad=0.08',facecolor=col,edgecolor='black',lw=1.5,alpha=0.85,zorder=6)
    ax.add_patch(rect)
    ax.text(x,y_c,step,fontsize=7.5,color='white',ha='center',va='center',fontweight='bold',zorder=7)
    if i < 3:
        ax.annotate('',xy=(xs_c[i+1]-0.72,y_c),xytext=(x+0.72,y_c),
                    arrowprops=dict(arrowstyle='->',color='#444',lw=2.0))

# Reference
ax.text(13.6,0.7,'Gonzalez-Hurtado et al. 2025, Nature Aging',fontsize=9,style='italic',color='#555',ha='center')

# Legend
legend_elements = [
    mpatches.Patch(facecolor=C_ADIP,edgecolor=C_ADIP_O,label='Adipocyte'),
    mpatches.Patch(facecolor=C_NAM,edgecolor=C_NAM,label='NAM (nerve-associated macrophage)'),
    mpatches.Patch(facecolor=C_M1,edgecolor='#BF360C',label='M1 pro-inflammatory macrophage'),
    mpatches.Patch(facecolor=C_M2,edgecolor='#00796B',label='M2 anti-inflammatory macrophage'),
    mpatches.Patch(facecolor=C_FIB,edgecolor='none',label='Fibrosis (collagen)'),
    Line2D([0],[0],color=C_NERVE,linewidth=2,label='Nerve fiber'),
    Line2D([0],[0],marker='o',color='w',markerfacecolor=C_MAST,markersize=8,label='Mast cell'),
    Line2D([0],[0],marker='o',color='w',markerfacecolor=C_EOS,markersize=8,label='Eosinophil'),
    Line2D([0],[0],marker='o',color='w',markerfacecolor=C_TC,markersize=8,label='T cell'),
    Line2D([0],[0],marker='o',color='w',markerfacecolor=C_IL10,markersize=8,label='IL-10/TGF-β'),
]
leg = ax.legend(handles=legend_elements,loc='lower right',fontsize=7.5,
                frameon=True,framealpha=0.92,edgecolor='#AAA',ncol=2,
                title='Color Key',title_fontsize=8)
leg.get_frame().set_linewidth(0.8)

ax.text(0.3,9.9,'Fig. 5',fontsize=18,fontweight='bold',color='#222')

# Panel dividers
for xp in [5.5, 11.5]:
    ax.plot([xp,xp],[0.3,9.0],color='#CCC',lw=1.0,ls='--',alpha=0.6)

plt.tight_layout(pad=0.5)
out = '/Users/ocm/.openclaw/workspace/arp-v24/figures/fig5_nams_adipose.png'
plt.savefig(out, dpi=300, bbox_inches='tight', facecolor=C_WHITE)
print(f'Done → {out}')
plt.close()
