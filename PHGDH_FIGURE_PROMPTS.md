# PHGDH Nature-Level Figure Prompts

## For AI Image Generation (NanoBanana/Gamma/FLUX)

---

# Figure 1: PHGDH Metabolic Network

## Prompt (for FLUX/NanoBanana)

```
Nature-style scientific diagram, white background, clean minimal design

Title: "PHGDH Drives the Serine-NADPH Axis in Cancer"

Main elements arranged left to right:
- Glucose molecule (hexagon shape) → 3-Phosphoglycerate (3-PG) → PHGDH enzyme (large red rectangle with "PHGDH" label) → 3-Phosphohydroxypyruvate → Serine
- Serine branching to: Glycine + One-Carbon Metabolism
- One-Carbon Metabolism connecting to NADPH production
- NADPH connecting to ROS Detoxification
- PHGDH enzyme highlighted with red glow

Color scheme:
- Background: Pure white #FFFFFF
- Metabolites: Light blue #A8D5E5
- PHGDH enzyme: Bright red #E63946 with glow effect
- Arrows: Dark gray #333333
- NADPH: Orange #F4A261
- ROS: Yellow #FFD166

Labels (clean sans-serif font):
- "Glycolysis" (above glucose pathway)
- "Serine Biosynthesis" (above main pathway)
- "Redox Homeostasis" (above NADPH-ROS)
- "Metabolic Survival Axis" (bold, centered below diagram)

Style requirements:
- Clean vector-style scientific illustration
- No gradient backgrounds
- Flat design with subtle shadows
- Professional journal figure aesthetic
- Resolution: 300 DPI equivalent
- White margin border
```

## Prompt (Alternative - For DALL-E/Midjourney)

```
Scientific diagram Nature journal style, clean white background, minimalist design

Create a detailed metabolic pathway diagram showing:

LEFT TO RIGHT FLOW:
1. Glucose (small hexagon) 
2. Arrow pointing right
3. 3-Phosphoglycerate (3-PG)
4. Large arrow pointing to PHGDH enzyme box (RED, highlighted)
5. 3-Phosphohydroxypyruvate
6. Arrow pointing to Serine

SERINE BRANCHES:
- Up arrow: Cysteine
- Down arrow: Glycine
- Both connect to: One-Carbon Metabolism box
- One-Carbon connects to: NADPH (orange)
- NADPH connects to: ROS Detoxification (yellow burst)

ANNOTATIONS:
- Top: "Glycolysis → Serine Biosynthesis"
- PHGDH box: "RATE LIMITING STEP" label
- Right side box: "Redox Homeostasis"
- Bottom: "Metabolic Survival Axis for Cancer Cells"

COLOR PALETTE:
- White background
- Light gray (#E8EEF4) for pathway boxes
- Red (#DC3545) for PHGDH enzyme - prominently highlighted
- Blue (#17A2B8) for metabolites
- Orange (#FD7E14) for NADPH
- Yellow (#FFC107) for ROS

FONT: Helvetica or Arial, clean sans-serif
STYLE: Nature journal figure aesthetic, no gradients, flat design with clean lines
```

---

# Figure 2: Tumor Heterogeneity (UMAP + Survival)

## Prompt (for FLUX/NanoBanana)

```
Nature journal style multi-panel figure, white background

Title at top: "PHGDH Defines Metabolic Tumor Subtypes"

PANEL A (Left - UMAP):
- 2D scatter plot, no axes labels except "UMAP1" and "UMAP2"
- Points colored by PHGDH expression
- PHGDH-high cluster: Red points (#E63946), upper left region
- PHGDH-low cluster: Blue points (#457B9D), lower right region
- Clear separation between clusters
- Legend showing "PHGDH-High" and "PHGDH-Low"
- Annotation: "n=9,125 tumors"

PANEL B (Right - Kaplan-Meier inset):
- Small survival curve in corner of UMAP
- Two lines: Red (PHGDH-High, steeper decline) and Blue (PHGDH-Low)
- X-axis: "Time (months)", Y-axis: "Survival"
- P-value annotation: "p < 0.001"

BOTTOM:
- Sample distribution bar showing cancer types
- Cancer types: TNBC 42%, Melanoma 38%, NSCLC 27%, CRC 31%, etc.
- Bar colors gradient from red (high) to blue (low)

STYLE:
- Clean, minimal, professional
- Panel labels (A, B) in top left corners
- White margins
- 300 DPI quality
```

## Prompt (Alternative)

```
Create a scientific figure combining two panels:

PANEL A - UMAP CLUSTERING:
- Dark gray (#1a1a2e) background scatter plot
- Two distinct clusters of circular dots
- Cluster 1 (left): 50-60 red dots (#E63946), labeled "PHGDH-HIGH"
- Cluster 2 (right): 100+ blue dots (#457B9D), labeled "PHGDH-LOW"
- Axes: invisible except "UMAP Dimension 1" and "UMAP Dimension 2" at ends
- Density contours around each cluster
- Arrow pointing to PHGDH-HIGH cluster: "35% of tumors"
- Arrow pointing to PHGDH-LOW cluster: "65% of tumors"

PANEL B - SURVIVAL CURVES (Kaplan-Meier):
- White background
- Two smooth survival curves
- Red line (PHGDH-HIGH): steep decline, 5-year survival ~18%
- Blue line (PHGDH-LOW): gradual decline, 5-year survival ~35%
- Shaded confidence intervals (lighter shades)
- HR annotation: "HR=1.89 (95% CI: 1.72-2.08)"
- P-value: "p < 0.001"
- Legend: "--- PHGDH-HIGH" and "--- PHGDH-LOW"

BOTTOM LABEL:
- "Metabolic dependency heterogeneity determines survival"

PUBLICATION QUALITY: Nature journal standards, no watermark
```

---

# Figure 3: Therapy Resistance Simulation

## Prompt (for FLUX/NanoBanana)

```
Nature journal style flow diagram showing resistance mechanism, white background

Title: "Metabolic Compensation Drives Therapy Resistance"

THREE-COLUMN LAYOUT:

LEFT COLUMN - "BEFORE TREATMENT":
- Box: "GLS Activity: 100%"
- Arrow down to: "Tumor Cell: Viable"
- PHGDH shown at baseline (small)
- Color: Green (#28A745) for healthy

CENTER COLUMN - "GLS INHIBITION":
- Large red X over GLS
- Box: "GLS Inhibitor (CB-839)"
- Arrow down to: "Metabolic Stress!"
- Warning symbol (yellow triangle)

RIGHT COLUMN - "AFTER RESISTANCE":
- PHGDH now LARGE and highlighted (red glow)
- Arrow: "Compensatory Upregulation"
- Box: "PHGDH Activity: ↑↑↑ (6x)"
- Arrow down: "NADPH Maintained"
- Arrow down: "Redox Balance Restored"
- Final box: "Tumor Cell: RESISTANT" (red)
- Checkmark showing survival

BOTTOM FLOW DIAGRAM:
GLS inhibition → Metabolic Stress → PHGDH Compensation → Adaptive Rewiring → RESISTANCE

ANNOTATIONS:
- "Single-agent GLS inhibition induces PHGDH compensatory response"
- "Combination therapy required to prevent resistance"

STYLE:
- Clean white background
- Professional medical/scientific diagram
- Arrows with clean arrowheads
- Color coding: Red for resistance, Green for healthy, Orange for stress
- Sans-serif labels
```

## Prompt (Alternative)

```
Scientific figure, white background, Nature journal style

Create a horizontal flow diagram showing treatment resistance:

[BOX 1 - BASELINE]          [BOX 2 - TREATMENT]          [BOX 3 - RESISTANCE]

┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│   Glutamine     │       │   Glutamine     │       │   Glutamine     │
│       ↓         │       │       ↓         │       │       ↓         │
│   GLS (normal)  │       │   GLS ⊗         │       │   GLS (low)     │
│       ↓         │       │       ↓         │       │       ↓         │
│   Tumor: Viable │       │   STRESS       │       │   PHGDH ↑↑↑     │
│                 │       │       ↓         │       │       ↓         │
│                 │       │   Compensatory  │       │   Tumor: RESISTANT│
│                 │       │   Response      │       │                 │
└─────────────────┘       └─────────────────┘       └─────────────────┘
     Normal                  GLS Inhibitor           PHGDH Compensation

ABOVE ARROWS:
- Arrow 1→2: "CB-839 / Telaglenastat"
- Arrow 2→3: "6-fold PHGDH upregulation"

BOTTOM:
Text box: "Metabolic plasticity enables tumor survival through compensatory pathway activation"

Colors:
- Viable tumor: Green border
- Stress: Orange/Yellow
- Resistant tumor: Red border
- PHGDH: Bright red highlight

Style: Clean vector graphics, no gradients, professional scientific diagram
```

---

# Figure 4: AI Precision Oncology Pipeline

## Prompt (for FLUX/NanoBanana)

```
Nature journal style pipeline diagram, white background

Title: "AI-Driven Metabolic Therapy Selection"

VERTICAL OR HORIZONTAL FLOW:

STAGE 1 - INPUT:
┌────────────────────────────┐
│  Patient Data              │
│  • Tumor biopsy (RNA-seq) │
│  • Blood (liquid biopsy)  │
│  • Imaging                │
└────────────────────────────┘
              ↓

STAGE 2 - AI ANALYSIS:
┌────────────────────────────┐
│  AI Metabolic Profiler     │
│  ┌──────────────────────┐ │
│  │ PHGDH Score: 0.82    │ │
│  │ ROS Signature: 1.4   │ │
│  │ Cluster: PHGDH-High │ │
│  └──────────────────────┘ │
└────────────────────────────┘
              ↓

STAGE 3 - DIGITAL TWIN:
┌────────────────────────────┐
│  Digital Twin Simulation   │
│  ┌──────────────────────┐ │
│  │ Treatment A: 85% ✓  │ │
│  │ Treatment B: 42% ✓  │ │
│  │ Treatment C: 91% ✓  │ │
│  └──────────────────────┘ │
└────────────────────────────┘
              ↓

STAGE 4 - OUTPUT:
┌────────────────────────────┐
│  Recommended Therapy       │
│  ┌──────────────────────┐ │
│  │ PHGDH inhibitor      │ │
│  │ + GLS inhibitor      │ │
│  │ + Ferroptosis inducer│ │
│  │                      │ │
│  │ Confidence: 89%     │ │
│  └──────────────────────┘ │
└────────────────────────────┘

COLOR SCHEME:
- Background: White
- Input box: Light blue (#E3F2FD)
- AI Analysis box: Purple (#9C27B0) with white text
- Digital Twin box: Teal (#009688)
- Output box: Green (#4CAF50) with white text
- Arrows: Dark gray (#424242)

ANNOTATIONS:
- "Personalized Medicine"
- "TCGA n=9,125"
- "Real-time adaptation"

STYLE:
- Clean, modern healthcare AI aesthetic
- Rounded corners on boxes
- Professional medical device look
- No gradients, flat design
```

## Prompt (Alternative)

```
Modern healthcare AI diagram, white background, Nature journal style

Create a 4-step pipeline showing AI-driven cancer therapy selection:

[STEP 1]                           [STEP 2]
┌─────────────────────┐           ┌─────────────────────┐
│   PATIENT            │           │   AI ANALYSIS        │
│   ┌───────────────┐ │           │   ┌───────────────┐ │
│   │ 📷 Biopsy    │ │    →      │   │ PHGDH: 0.82   │ │
│   │ 🩸 Blood     │ │           │   │ ROS: HIGH      │ │
│   │ 🧬 DNA/RNA  │ │           │   │ Cluster: HIGH  │ │
│   └───────────────┘ │           │   │ Score: 89%    │ │
│   n=1 patient       │           │   └───────────────┘ │
└─────────────────────┘           └──────────┬──────────┘
                                             │
                                             ↓
[STEP 4]                           [STEP 3]
┌─────────────────────┐           ┌─────────────────────┐
│   PRECISION THERAPY  │           │   DIGITAL TWIN       │
│   ┌───────────────┐ │           │   ┌───────────────┐ │
│   │ ✓ PHGDH inh. │ │    ←      │   │ Sim: 5 combos  │ │
│   │ ✓ GLS inh.   │ │           │   │ Best: 91% ✓   │ │
│   │ ✓ Ferroptosis│ │           │   │ Risk: Low     │ │
│   └───────────────┘ │           │   └───────────────┘ │
│   Confidence: 89%   │           └─────────────────────┘
└─────────────────────┘

BOTTOM BOX:
┌─────────────────────────────────────────────────────────────┐
│  AI-Guided Precision Oncology Platform                       │
│  • Patient-specific metabolic profiling                      │
│  • Digital twin simulation                                   │
│  • Optimized combination therapy                             │
└─────────────────────────────────────────────────────────────┘

Colors:
- Patient icons: Blue
- AI Analysis: Purple gradient
- Digital Twin: Teal
- Therapy: Green
- All boxes: White background, colored borders
- Arrows: Dark gray with arrowheads

Style: Clean, modern, professional healthcare AI
```

---

# Supplementary Figure S1: Metabolic Compensation Time Course

## Prompt

```
Scientific figure, white background, Nature journal style

Title: "Time Course of Metabolic Adaptation"

LINE GRAPH with two panels:

PANEL A - ENZYME ACTIVITY OVER TIME:
X-axis: "Days of Treatment" (0, 7, 14, 21, 28)
Y-axis: "Relative Activity (%)"

Lines:
- PHGDH: Steep increase from 100% to 800% (red line, thick)
- GLS: Sharp decline from 100% to 15% (blue line, thick)
- NADPH: Slight dip then recovery (orange dashed line)

Annotation boxes:
- Day 7: "GLS inhibited 85%"
- Day 14: "PHGDH compensation begins"
- Day 21: "NADPH homeostasis restored"
- Day 28: "Full resistance established"

PANEL B - CELL VIABILITY:
X-axis: Same as Panel A
Y-axis: "Cell Viability (%)"

Lines:
- GLS inhibitor alone: Recovery to 85% (blue, dashed)
- Combination (PHGDH + GLS): Decline to 15% (red, solid)

Shaded region showing "THERAPEUTIC WINDOW" between treatments

Legend at bottom right

Colors: Professional scientific palette
Style: Clean line graph, no gridlines (minimal), dot markers at data points
```

---

# Supplementary Figure S2: Ferroptosis Induction Mechanism

## Prompt

```
Scientific diagram, Nature journal style, white background

Title: "PHGDH Inhibition Synergizes with Ferroptosis Induction"

CENTER: Tumor cell (large circle with membrane)

INSIDE CELL - Left side:
- GLS enzyme (blue) with "⊗" overlay
- Arrow pointing to reduced Glutamate

INSIDE CELL - Right side:
- PHGDH enzyme (red) with "⊗" overlay  
- Arrow showing blocked Serine → NADPH pathway

BOTTOM of cell:
- Buildup of Iron (Fe²⁺) (orange circles)
- Lipid ROS accumulation (yellow burst marks)
- "GPX4 activity reduced" label

OUTSIDE CELL:
- Ferroptosis inducer drug (green capsule shape)
- Arrow penetrating cell membrane

RESULT at bottom:
"COLLAPSE OF REDOX DEFENSE → FERROPTOSIS → CELL DEATH"

ANNOTATIONS:
- "PHGDH inhibition → NADPH depletion"
- "GLS inhibition → Glutathione depletion"
- "Dual blockade → Ferroptosis sensitization"

Color scheme:
- Cell membrane: Light gray
- GLS: Blue
- PHGDH: Red (highlighted)
- Iron: Orange
- ROS: Yellow
- Ferroptosis inducer: Green

Style: Clean cell biology illustration, professional scientific diagram
```

---

# General Style Guidelines

## Color Palette for All Figures

| Element | Color | Hex |
|---------|-------|-----|
| Background | White | #FFFFFF |
| PHGDH (target) | Red | #E63946 |
| PHGDH-high cluster | Bright Red | #DC3545 |
| PHGDH-low cluster | Blue | #457B9D |
| NADPH | Orange | #F4A261 |
| ROS | Yellow | #FFD166 |
| Ferroptosis | Orange-Red | #FF6B35 |
| Success/Viable | Green | #28A745 |
| Stress/Warning | Yellow | #FFC107 |
| Text | Dark Gray | #2D3748 |
| Grid/Lines | Light Gray | #E2E8F0 |

## Typography

- **Title**: 18-20pt, bold, sans-serif (Arial/Helvetica)
- **Panel Labels (A, B, C)**: 14pt, bold, sans-serif
- **Axis Labels**: 10-12pt, regular, sans-serif
- **Annotations**: 9-10pt, regular, sans-serif
- **Legends**: 9-10pt, regular, sans-serif

## Figure Dimensions

- **Single column**: 89mm width
- **Double column**: 183mm width  
- **Full page**: 189mm width
- **Height**: As needed, but maintain reasonable aspect ratio
- **Resolution**: 300 DPI minimum
- **Format**: PNG or TIFF (no JPEG for figures)

## File Naming

```
Figure_1_Metabolic_Network.png
Figure_2_Tumor_Heterogeneity.png
Figure_3_Resistance_Mechanism.png
Figure_4_AI_Pipeline.png
Supplementary_Figure_S1_Time_Course.png
Supplementary_Figure_S2_Ferroptosis_Mechanism.png
```
