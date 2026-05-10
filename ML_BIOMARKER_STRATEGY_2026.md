# Machine Learning Biomarker Strategy: Ferroptosis-Driven NSCLC
**Date:** 2026-05-11  
**Project:** Triple Ferroptosis Platform (FSP1 + SLC7A11 + DGAT1)  
**Indication:** KEAP1/STK11/NFE2L2-altered LUAD  
**Goal:** Nature/Cell/Science-level biomarker strategy for patient stratification and clinical development

---

## Executive Summary

Machine learning (ML) biomarkers enable precision patient selection for ferroptosis-targeted therapy in NSCLC. This strategy integrates multi-omics data (transcriptomics, proteomics, metabolomics), ferroptosis regulatory gene signatures, and tumor microenvironment (TME) profiles to develop a composite biomarker platform for:

1. **Patient stratification** — Identify FSP1-high/KEAP1-altered LUAD responders
2. **Ferroptosis competence scoring** — Predict response to ferroptosis induction
3. **TME characterization** — Predict immunotherapy combination benefit
4. **Clinical endpoint prediction** — Link biomarkers to outcomes

---

## 1. Biomarker Development Framework

### 1.1 Multi-Layer Biomarker Architecture

```
┌──────────────────────────────────────────────────────────────┐
│              Composite Biomarker Platform                     │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Layer 1: Genomic                                            │
│  ├── KEAP1 mutation (NGS)                                    │
│  ├── STK11 mutation (NGS)                                    │
│  ├── NFE2L2 mutation (NGS)                                   │
│  └── FSP1 copy number (CNA)                                 │
│                                                              │
│  Layer 2: Transcriptomic                                     │
│  ├── FSP1 mRNA expression (RNA-seq)                         │
│  ├── Ferroptosis regulator panel (24 genes)                  │
│  ├── GPX4/SLC7A11/DGAT1 signature                           │
│  └── NRF2 target gene set                                    │
│                                                              │
│  Layer 3: Proteomic                                          │
│  ├── FSP1 protein (IHC, RPPA)                               │
│  ├── Ferroptosis pathway proteins (RPPA)                    │
│  └── Phospho-protein signatures (RTK/PI3K/AKT)             │
│                                                              │
│  Layer 4: Functional                                         │
│  ├── Lipid peroxidation (BODIPY-C11, flow)                  │
│  ├── CoQ redox state (LC-MS)                                 │
│  ├── Iron levels (PCR)                                       │
│  └── ACSL4 activity (WB)                                    │
│                                                              │
│  Layer 5: TME                                                │
│  ├── Immune cell infiltration (CIBERSORTx)                  │
│  ├── PD-L1 expression (IHC)                                 │
│  ├── IFN-γ signature (RNA-seq)                               │
│  └── TMB/MSI (NGS)                                           │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 1.2 Machine Learning Pipeline

```python
# Biomarker Development Pipeline

Step 1: Data Collection
├── TCGA-LUAD (RNA-seq + clinical)
├── GEO cohorts (GSE31210, GSE19188)
├── Our SLC7A11 data (Larry report)
└── Internal ARP data

Step 2: Feature Engineering
├── Ferroptosis gene panel (24 genes)
├── NRF2 pathway genes (12 genes)
├── TME signature genes (18 genes)
└── Clinical covariates (age, sex, stage)

Step 3: ML Model Training
├── Supervised: Classification (responder/non-responder)
├── Unsupervised: Clustering (molecular subtypes)
├── Semi-supervised: Ferrostosis score prediction
└── Deep learning: Multi-omics integration

Step 4: Validation
├── Internal: Cross-validation (5-fold)
├── External: Independent GEO cohorts
└── Functional: Orthogonal assay confirmation
```

---

## 2. Machine Learning Biomarkers

### 2.1 Ferroptosis Regulation Score (FRS)

**Purpose:** Quantify ferroptosis competence in individual tumors

**Method:** LASSO regression + random forest ensemble

**Features (24 genes):**
| Category | Genes |
|---------|-------|
| **Inhibitors** | GPX4, SLC7A11, FSP1, GCLC, GCLM, NQO1, SLC3A2 |
| **Enablers** | ACSL4, ALOX12, ALOX15, TFRC, FTH1, FTL |
| **Executors** | CHAC1, NOX1, POR, CYBB |
| **Regulators** | NFE2L2, KEAP1, STK11, TP53, MDM2 |

**Output:** Continuous FRS (0-100 scale)
```
FRS = Σ(weight_i × expression_i) + intercept
```

**Validation:**
- High FRS = ferroptosis-sensitive (low baseline defense)
- Low FRS = ferroptosis-resistant (high defense)

### 2.2 KEAP1/NRF2 Activity Score

**Purpose:** Predict NRF2-driven ferroptosis resistance

**Method:** Single-sample gene set variation analysis (ssGSEA)

**Gene sets:**
| Pathway | Genes |
|---------|-------|
| NRF2 canonical | NFE2L2, NQO1, HMOX1, GCLC, GCLM, TXNRD1, G6PD |
| Ferroptosis defense | FSP1, GPX4, SLC7A11, GSS |
| Antioxidant | SOD1, SOD2, CAT, PRDX1-6 |

**Output:** KEAP1/NRF2 activity score (continuous)

**Interpretation:**
- High NRF2 score → FSP1 upregulation → ferroptosis resistance
- Target: NRF2-high tumors for FSP1 inhibition

### 2.3 Triple Ferroptosis Combination Score (TFCS)

**Purpose:** Predict response to triple combo (DGAT1i + SLC7A11i + FSP1i)

**Method:** Gradient boosting (XGBoost) multi-classifier

**Features:**
| Feature | Weight | Source |
|---------|--------|--------|
| FSP1 expression | 0.25 | RNA-seq |
| SLC7A11 expression | 0.20 | RNA-seq |
| DGAT1 expression | 0.15 | RNA-seq |
| GPX4 expression | 0.10 | RNA-seq |
| ACSL4 expression | 0.10 | RNA-seq |
| Lipid peroxidation | 0.10 | Functional assay |
| KEAP1 status | 0.10 | NGS |

**Output:**
| Class | Description | Clinical Implication |
|-------|-------------|----------------------|
| TFCS-High | All three targets high | Best triple combo responders |
| TFCS-Intermediate | 1-2 targets high | Dual combo candidates |
| TFCS-Low | Resistance mechanisms | Avoid ferroptosis approach |

### 2.4 Tumor Microenvironment Score (TMS)

**Purpose:** Predict immunotherapy combination benefit

**Method:** CIBERSORTx + random forest

**Features:**
| Cell Type | Signature genes |
|----------|----------------|
| CD8+ T cells | CD8A, CD8B, GZMA, GZMB, PRF1 |
| CD4+ T cells | CD4, IL2, TNF, IFN-γ |
| NK cells | KLRK1, NKG7, GNLY |
| Macrophages (M1) | CD86, IL12, iNOS |
| Macrophages (M2) | CD163, CD206, ARG1 |
| Dendritic cells | CD11c, HLA-DR, DC-SIGN |
| Treg cells | FOXP3, IL2R, CTLA4 |
| Neutrophils | CD66b, ELANE, MPO |

**Output:**
| TMS Class | TME Profile | FSP1i + ICI Benefit |
|-----------|-------------|---------------------|
| Inflamed | High CD8, low Treg | High |
| Excluded | Low CD8, high Treg | Low |
| Immunosuppressed | High M2, low M1 | Medium |

### 2.5 Composite Biomarker Score (CBMS)

**Final integration score for clinical trial stratification:**

```
CBMS = (0.30 × FRS) + (0.25 × NRF2_score) + (0.25 × TMS) + (0.20 × TFCS)
```

**Stratification:**
| CBMS Range | Interpretation | Action |
|-----------|----------------|--------|
| ≥75 | Highly selected | FSP1i monotherapy |
| 50-74 | Selected | FSP1i + RT |
| 25-49 | Moderate | FSP1i + ICI |
| <25 | Unselected | Non-ferroptosis approach |

---

## 3. Machine Learning Methods

### 3.1 Supervised Learning (Patient Classification)

| Method | Task | Features | Performance Target |
|--------|------|----------|-------------------|
| **LASSO** | Feature selection | 24-gene panel | AUC ≥0.80 |
| **Random Forest** | Binary classification | 50+ features | AUC ≥0.85 |
| **XGBoost** | Multi-class | 100+ features | AUC ≥0.85 |
| **SVM** | Binary classification | Engineered features | AUC ≥0.80 |
| **Neural Network** | Multi-omics integration | Multi-layer | AUC ≥0.85 |

### 3.2 Unsupervised Learning (Subtype Discovery)

| Method | Task | Output |
|--------|------|--------|
| **k-means clustering** | Partition | 3-4 molecular subtypes |
| **Hierarchical clustering** | Dendrogram | Feature heatmaps |
| **t-SNE/UMAP** | Visualization | 2D tumor maps |
| **NMF** | Deconvolution | Metagenes |

### 3.3 Deep Learning (Multi-Omics Integration)

```python
# Multi-omics Deep Learning Architecture

Input Layer:
├── mRNA expression (2000 genes)
├── Protein expression (500 proteins)  
├── Methylation (1000 sites)
└── Mutation calls (200 genes)

Encoder:
├── Dense layers (ReLU, BatchNorm)
├── Attention mechanism
└── Latent representation (64 dims)

Output Heads:
├── Ferroptosis score (regression)
├── Survival prediction (Cox)
├── Treatment response (classification)
└── Subtype classification (softmax)
```

### 3.4 Survival Analysis

| Method | Application |
|--------|-------------|
| **Cox Proportional Hazards** | Univariate/multivariate survival |
| **Random Survival Forest** | Non-linear hazard estimation |
| **DeepSurv** | Neural network survival analysis |
| **CIndex optimization** | Model discrimination |

---

## 4. Validation Strategy

### 4.1 Internal Validation

```
Training: TCGA-LUAD (n=517)
├── 5-fold cross-validation
├── Bootstrap resampling (1000x)
└── Nested CV for hyperparameter tuning

Validation: Internal hold-out (20%)
```

### 4.2 External Validation

| Dataset | Type | Samples | Purpose |
|---------|------|---------|---------|
| GSE31210 | Microarray | 226 LUAD | Geographic validation |
| GSE19188 | Microarray | 91 NSCLC | Histotype validation |
| GSE13213 | Microarray | 150 LUAD | Independent replication |
| PRJEB23709 | RNA-seq | 80 LUAD | European cohort |
| Our internal data | RNA-seq | TBD | Functional validation |

### 4.3 Functional Validation

| Biomarker | Orthogonal Assay |
|-----------|-----------------|
| FSP1 IHC | Western blot + activity assay |
| Ferroptosis score | BODIPY-C11 flow cytometry |
| NRF2 activity | ARE-luciferase reporter |
| TME score | Multiplex IHC (mIF) |

---

## 5. Clinical Trial Integration

### 5.1 Biomarker-Driven Trial Design

```
Phase I/II Trial: FSP1 inhibitor in LUAD

Patient Selection (Screening):
├── KEAP1/STK11/NFE2L2 mutation (NGS) ✓
├── FSP1 IHC (H-score ≥200) ✓
├── CBMS ≥50 ✓
└── Ferroptosis competence (FRS ≥40) ✓

Randomization:
├── biomarker-high (CBMS ≥75) → FSP1i monotherapy
├── biomarker-intermediate (CBMS 50-74) → FSP1i + radiotherapy
└── biomarker-low (CBMS 25-49) → FSP1i + pembrolizumab

Endpoints:
├── Primary: ORR (RECIST 1.1)
├── Secondary: PFS, OS, DOR
├── Biomarker: FRS change, CoQ redox, lipid peroxidation
└── Safety: AEs, SAEs
```

### 5.2 Adaptive Design

| Phase | Adaptation | Biomarker Trigger |
|-------|------------|------------------|
| Phase I | Dose escalation | FRS ≥30% reduction |
| Phase IIa | Expand responders | CBMS ≥75 + ORR ≥30% |
| Phase IIb | Enrich population | FRS validated at 50% |
| Phase III | Companion diagnostic | CDx submission |

---

## 6. Technology Stack

### 6.1 Software

| Category | Tool | Purpose |
|----------|------|---------|
| **Language** | Python 3.9+ | Primary |
| **ML Framework** | scikit-learn, XGBoost, PyTorch | Model training |
| **Survival** | lifelines, pycox | Survival analysis |
| **Visualization** | seaborn, plotly, matplotlib | Plots |
| **Bioinformatics** | scanpy, squidpy | Single-cell |
| **TME deconvolution** | CIBERSORTx, MCP-counter | Immune profiling |

### 6.2 Infrastructure

| Component | Specification |
|-----------|---------------|
| **Compute** | Local GPU (M4 Pro) or cloud NIM |
| **Storage** | TCGA/GEO cached locally |
| **Code** | Git version control |
| **Pipeline** | Snakemake workflow |
| **Reproducibility** | Docker container |

### 6.3 Key Python Libraries

```python
# Core ML
scikit-learn==1.3.0
xgboost==2.0.0
torch==2.0.0

# Bioinformatics
scanpy==1.9.0
squidpy==1.2.0
lifelines==0.27.0

# Visualization
matplotlib==3.8.0
seaborn==0.12.0
plotly==5.15.0

# Pipeline
snakemake==7.25.0
```

---

## 7. Integration with ARP Pipeline

### 7.1 ARP Orchestrator Integration

```bash
# ML biomarker playbook
python3 arp_orchestrator.py "ferroptosis ML biomarker LUAD" --playbook discovery
```

### 7.2 Triple Ferroptosis Platform

```
┌──────────────────────────────────────────────────────────────┐
│              Triple Ferroptosis Platform                      │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Target Layer                                                 │
│  ├── FSP1 inhibitor (CoQ axis)                               │
│  ├── SLC7A11 inhibitor (GSH/GPX4 axis)                       │
│  └── DGAT1 inhibitor (lipid droplet axis)                    │
│                                                              │
│  Biomarker Layer                                              │
│  ├── Ferroptosis Regulation Score (FRS)                      │
│  ├── KEAP1/NRF2 Activity Score                               │
│  ├── Triple Combo Score (TFCS)                               │
│  ├── Tumor Microenvironment Score (TMS)                      │
│  └── Composite Biomarker Score (CBMS)                        │
│                                                              │
│  Clinical Layer                                               │
│  ├── Patient stratification (CBMS-based)                      │
│  ├── Combination selection (RT, ICI, Chemo)                  │
│  └── Endpoint prediction (ML survival model)                   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 8. Timeline & Milestones

| Quarter | Milestone | Deliverable |
|---------|-----------|-------------|
| Q2 2026 | Data collection + preprocessing | Multi-omics dataset |
| Q3 2026 | Feature engineering + ML training | FRS, NRF2, TMS models |
| Q4 2026 | Model validation + optimization | Validated CBMS |
| Q1 2027 | Clinical integration planning | Trial design document |
| Q2 2027 | Companion diagnostic development | CDx prototype |

---

## 9. Expected Outcomes

| Outcome | Target | Validation |
|---------|--------|------------|
| Ferroptosis score | AUC ≥0.80 | External cohort |
| Patient stratification | HR ≥2.0 for high vs low | Cox regression |
| Combination prediction | AUC ≥0.75 | Prospective |
| CDx submission | 510(k) or PMA | Regulatory |

---

## 10. Files

| File | Content |
|------|---------|
| `ML_BIOMARKER_STRATEGY_2026.md` | This document |
| `FSP1_DEVELOPMENT_PLAN_2026.md` | FSP1 preclinical plan |
| `SLC7A11 bioinformatics report` | Larry's LUAD data (existing) |
| `arp_orchestrator.py` | ML biomarker playbook |

---

## 11. References

1. TCGA Research Network (2014). Nature 513:559-563
2. Liu et al. (2023). Machine learning revealed ferroptosis features in LUAD. Bioinformatics.
3. Stockwell et al. (2022). Ferroptosis: A regulated cell death. Cell 181:1078-1090
4. Wu et al. (2025). Targeting FSP1 triggers ferroptosis in lung cancer. Nature.
5. Heng et al. (2023). Ferroptosis in cancer therapy. Nat Rev Cancer.

---

*ML Biomarker Strategy: 2026-05-11 | ARP v24*
*Author: Brown Biotech AI Drug Discovery*
*Integration: FSP1 + SLC7A11 + DGAT1 Triple Ferroptosis Platform*