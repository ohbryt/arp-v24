# GPS: Gene Expression Profile Predictor on Chemical Structures
**Date:** 2026-05-14  
**Source:** Cell 189, 2556-2572 (April 30, 2026)  
**Authors:** Xing, Tan, Leshchiner et al.  
**Lab:** Bin-Chen Lab (Michigan State), Octad  
**DOI:** https://doi.org/10.1016/j.cell.2026.02.016  
**GitHub:** https://github.com/Bin-Chen-Lab/GPS

---

## Executive Summary

| Feature | Details |
|---------|---------|
| **Core Innovation** | Predict gene expression from chemical structures |
| **Approach** | Transcriptomic reversal (restore healthy phenotype) |
| **Scale** | ZINC + Enamine HTS libraries (millions of compounds) |
| **Validation** | HCC (2 series, in vivo), IPF (1 repurposing + 1 novel) |
| **Open Source** | Apache 2.0, Docker available |

---

## GPS Architecture

### Three Core Components

| Component | Function |
|-----------|----------|
| **RCL (Robust Collaborative Learning)** | Training with custom drug/cell data |
| **GPS4Drugs** | Predict gene expression from SMILES |
| **MolSearch** | MCTS-based multi-objective optimization |

### Pipeline

```
Chemical Structure (SMILES)
    ↓
GPS (deep learning model)
    ↓
Predicted transcriptomic signature
    ↓
Score vs disease signature (reverse disease genes)
    ↓
MCTS optimization
    ↓
Lead compounds
```

---

## Key Results

### Hepatocellular Carcinoma (HCC)
- 2 unique compound series identified
- Favorable cellular selectivity
- In vivo efficacy validated

### Idiopathic Pulmonary Fibrosis (IPF)
- 1 repurposing candidate
- 1 novel anti-fibrotic compound
- Multi-cell targeting (scRNA-seq)

---

## Technical Features

| Feature | Details |
|---------|---------|
| **Training Data** | LINCS phase I (18,746 compounds, 978 landmark genes) |
| **Predictable Genes** | 307 out of 978 landmark genes |
| **Noise Handling** | RCL (Robust Collaborative Learning) |
| **Optimization** | Monte Carlo Tree Search (MCTS) |
| **Analysis** | SGAR (Structure-Gene-Activity Relationship) |

---

## ARP Pipeline Integration

| Use Case | GPS Application |
|----------|-----------------|
| **FSP1 NSCLC** | Predict transcriptomic reversal of ferroptosis genes |
| **Sarcopenia** | Muscle regeneration signature reversal |
| **MASLD** | Metabolic gene expression restoration |
| **IPF** | Already validated in Cell 2026 |
| **HCC** | Already validated in Cell 2026 |

---

## Web Resources

| Resource | URL |
|----------|-----|
| **GPS GitHub** | https://github.com/Bin-Chen-Lab/GPS |
| **Screening Portal** | http://apps.octad.org/GPS/ |
| **Repurposing Portal** | http://octad.org/ |
| **Docker (GPS4Drugs)** | binchengroup/gpsimage |
| **Docker (MolSearch)** | binchengroup/molsearch |

---

## Disease Signatures

### Ferroptosis Target (ARP)
```
Up genes: TFRC, IREB2, FTL, FTH1 (iron metabolism)
Down genes: GPX4, SLC7A11, FSP1 (ferroptosis suppressors)
```

### IPF Target (Validated)
```
Up genes: COL1A1, COL3A1, ACTA2, FN1, MMP2 (fibrosis)
Down genes: SFTPC, SFTPA1, SFTPD (surfactant)
```

### HCC Target (Validated)
```
Up genes: AFP, GPC3, HGF, VEGFA, ANPT2 (oncofetal)
Down genes: ALB, ApoE, CYP3A4 (liver function)
```

---

## Comparison: GPS vs Traditional

| Approach | GPS Advantage |
|----------|---------------|
| **Docking-based** | No need for known protein target |
| **ML on screening data** | Works on unprofiled compounds |
| **Traditional transcriptomics** | Predicts from structure alone |

---

*Cell 2026 | Bin-Chen Lab | Apache 2.0*