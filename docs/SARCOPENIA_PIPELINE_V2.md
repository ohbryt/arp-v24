# Sarcopenia Pipeline: Enhanced with ARP v24 Integrations
**Date:** 2026-05-13  
**Status:** ACTIVE

---

## Overview

Sarcopenia pipeline now enhanced with:
- **StackFeat-RL** → Stable biomarker discovery via RL
- **RegFormer** → Single-cell muscle cell type annotation
- **Iterative Evaluation** → Deep candidate screening
- **Scoring Rubric** → 100-point final evaluation
- **Medmarks** → Optimal model selection

---

## Enhanced Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                  SARCOPENIA PIPELINE v2                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. LITERATURE SEARCH                                            │
│     PubMed: sarcopenia myostatin mTOR treatment                   │
│     → PMIDs, gene targets (MSTN, MTOR, FST, PDK4, GDF15, AMPK)   │
│                                                                  │
│  ▼                                                               │
│                                                                  │
│  2. STACKFEAT-RL BIOMARKER DISCOVERY                             │
│     Reinforce policy gradients for stable gene panels             │
│     → FRS (Ferroptosis Regulation Score) for muscle              │
│     → Gene stability tracking (dual-criterion)                   │
│     → STRING priors for protein interactions                     │
│                                                                  │
│  ▼                                                               │
│                                                                  │
│  3. REGFORMER CELL ANNOTATION                                    │
│     Single-cell foundation model                                 │
│     → Muscle biopsy → Cell types (myocytes, fibroblasts, etc)   │
│     → GRN reconstruction for target genes                       │
│     → TMS (TME Score) enhancement                                │
│                                                                  │
│  ▼                                                               │
│                                                                  │
│  4. ITERATIVE EVALUATION (BioDesignBench)                         │
│     5-metric deep evaluation                                      │
│     → Depth levels: SURFACE → STANDARD → COMPREHENSIVE → EXPERT   │
│     → Iterative refinement until threshold                       │
│                                                                  │
│  ▼                                                               │
│                                                                  │
│  5. BOLTZ-2 STRUCTURE PREDICTION                                 │
│     Protein structure + binding affinity                         │
│     → MSTN-Compound complexes                                    │
│     → mTOR-Compound complexes                                    │
│                                                                  │
│  ▼                                                               │
│                                                                  │
│  6. SCORING RUBRIC (100-point)                                    │
│     ├── Approach (20): Literature, hypothesis, design            │
│     ├── Orchestration (20): Tool usage, iteration, recovery      │
│     ├── Quality (30): Binding, selectivity, ADMET                │
│     └── Impact (30): Novelty, clinical, combinability             │
│                                                                  │
│  ▼                                                               │
│                                                                  │
│  7. OUTPUT: Ranked Candidates + Dossier                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## StackFeat-RL: Muscle Biomarkers

### Key Biomarkers

| Biomarker | Pathway | Stability | Evidence |
|-----------|---------|-----------|----------|
| **FRS-M (Ferroptosis Reg. Score-Muscle)** | Ferroptosis/muscle | High | RL-optimized |
| **MSTN** | Myostatin | 0.95 | Validated |
| **MTOR** | mTORC1 | 0.95 | Validated |
| **AMPK** | Energy sensing | 0.90 | Approved drug |
| **GDF15** | Appetite/muscle | 0.85 | Emerging |
| **FOXO1** | Atrophy | 0.88 | Validated |

### FRS-M Calculation

```python
from stackfeat_rl_integration import biomarker_discovery

result = biomarker_discovery(
    expression_data=muscle_rnaseq,
    labels=sarcopenia_labels,
    gene_names=gene_symbols,
    biomarker_type="muscle"
)

# Output: Stable gene panel with RL-optimized weights
print(f"FRS-M: {result['score']:.3f}")
print(f"Genes: {result['genes']}")
```

---

## RegFormer: Cell Type Annotation

### Muscle Cell Types

| Cell Type | Markers | Role |
|-----------|---------|------|
| **Myocytes** | MYH1, MYH2, ACTN1 | Muscle fibers |
| **Satellite cells** | PAX7, MYF5 | Muscle stem |
| **Fibroblasts** | COL1A1, FAP | ECM |
| **Macrophages** | CD68, CD14 | Inflammation |
| **Endothelial** | VWF, PECAM1 | Vasculature |

### RegFormer Workflow

```python
from regformer_integration import analyze_single_cell

# Cell type annotation
result = analyze_single_cell(
    "muscle_biopsy.h5ad",
    task="anno"  # annotation, embedding, grn
)

# Output: Cell type proportions for TMS
```

---

## Target Programs

### SARCO-001: Bimagrumab Derivative
- **Target:** Myostatin (MSTN)
- **Mechanism:** ActRIIB blockade
- **Evidence:** 0.95 (highest)
- **Status:** Lead optimization

### SARCO-002: Rapamycin Analogue
- **Target:** mTORC1
- **Mechanism:** mTOR inhibition
- **Evidence:** 0.95 (highest)
- **Status:** Preclinical

### SARCO-003: Senolytic Combo
- **Targets:** Senescent cells + muscle preservation
- **Mechanism:** Dasatinib + Quercetin + AMPK activator
- **Evidence:** 0.85 (emerging)
- **Status:** Discovery

---

## Medmarks Model Selection

| Task | Model | Score |
|------|-------|-------|
| **Orchestrator** | gemini_3_pro_preview | 0.89 |
| **Biomarker** | gpt_5_1 | 0.88 |
| **Design** | gpt_5_2 | 0.87 |
| **Report** | gemini_3_pro_preview | 0.89 |

---

## Timeline

| Phase | Duration | Milestone |
|-------|----------|-----------|
| **Lead Discovery** | 3 months | StackFeat-RL biomarkers |
| **Hit Validation** | 6 months | RegFormer cell types |
| **Lead Optimization** | 12 months | Iterative evaluation |
| **Preclinical** | 18 months | IND-enabling studies |

---

## Files

| File | Purpose |
|------|---------|
| `SARCOPENIA_THERAPEUTICS_DESIGN_2026.md` | Full design document |
| `stackfeat_rl_integration.py` | Biomarker discovery |
| `regformer_integration.py` | Single-cell analysis |
| `iterative_evaluation.py` | Deep evaluation |
| `scoring_rubric.py` | 100-point scoring |
| `medmarks_integration.py` | Model selection |

---

*Enhanced: 2026-05-13 | ARP v24*