# TxConformal: Controlling False Discoveries in AI-Driven Therapeutic Discovery
**GitHub:** https://github.com/ying531/TxConformal
**Paper:** Ying Jin, Kexin Huang, et al. (Stanford, Google Research, Meta)

## Overview

TxConformal solves a critical problem in AI-driven drug discovery: **how to control false discoveries when selecting drug candidates for experimental validation.**

```
AI Predictions → Candidate Selection → Experimental Validation
                      ↑
              Error here = wasted resources
```

## Core Problem

AI models predict properties to prioritize drug candidates. But errors at the selection stage lead to:
- Wasted experimental resources
- False leads consuming budget
- Missed true positives

## Solution: TxConformal

Combines **conformal selection** + **balancing weights** to:
1. Start with AI model predictions
2. Adjust for distribution shifts between training and candidate pools
3. Build confidence measures for true positives
4. Control false discovery metrics

## Key Capabilities

| Task | Description |
|------|-------------|
| **FDR Control** | Select candidates ensuring desired success rate |
| **FDP Estimation** | Estimate false positives in selected subset |
| **Error Thresholds** | Set tolerable error levels |
| **Distribution Shift** | Handle ex vivo → in vivo, in silico → experimental shifts |

## Applications in Drug Discovery

1. **CRISPR perturbation screens** — gene targeting validation
2. **DNA sequence selection** — promoter/enhancer engineering
3. **Small molecules** — virtual screening hit selection
4. **Proteins** — stability/affinity prediction
5. **Clinical trials** — patient stratification

## Usage Example

```python
from txconformal import TxConformal
from txconformal.features import FeaturesProvider

# Step 1: Feature builder with calibration/test data
prov = FeaturesProvider(
    f_calib=f_cal, f_test=f_test,  # predictions
    E_calib=emb_cal, E_test=emb_test  # embeddings
)
prov.prepare()

# Step 2: TxConformal - build weights, p-values, selection
txc = TxConformal(score_name="clip", cutoff=0.5)  # Y > 0.5 = true discovery
txc.fit(prov, y_calib, print_level=-1)

# Step 3: Select with FDR control
res = txc.select(method="bh", alpha=0.1)  # BH selection for FDR < 10%

print("Selected indices:", res.idx)
print("Threshold:", res.threshold)
```

## ARP Integration

### 1. Virtual Screening Pipeline
```
PED/BioMiner predictions → TxConformal selection → Experimental validation
         ↓
    FDR < 10% 보장
```

### 2. Target Prioritization
```
AI_mechanism_analysis → Top candidates → TxConformal filtering
```

### 3. Multi-Omics Integration
```
Expression + Proteomics + Metabolomics → Consensus predictions → TxConformal
```

## Example Notebooks

| Scenario | Notebook | Content |
|----------|----------|---------|
| ADMET tasks | `general_tasks.ipynb` | FDR control, FDP estimation, min true positives |
| Protein stability | `protein_stability.ipynb` | Regression with FDR control |
| Enamine HTS | `enamine.ipynb` | Prospective screening with customization |

## Technical Details

### Feature Preparation
```python
# Default: soft block
phi = [f, f², pooled quantile bins, embeddings]
# Forces balance for principal components

# Force block
[f, pooled bins]  # When embeddings unavailable

# Backup block
[[f, pooled bins], [f]]  # Fallback options
```

### Statistical Guarantees
- **Finite-sample validity** — not asymptotic
- **Exchangeability-based** — conformal prediction theory
- **Weighted for covariate shift** — handles distribution shift

## Relevance to ARP v24

### Direct Applications
1. **SLC7A11/DGAT1/KDM4A target validation** — select best candidates for wet-lab
2. **Virtual screening hit selection** — PED embeddings + TxConformal
3. **Patient stratification** — biomarker-based selection with FDR control
4. **Clinical trial design** — endpoint selection with error control

### Integration Points
- **BioMiner** → predictions → TxConformal → validation
- **PED virtual screening** → hit list → TxConformal → experimental test
- **AtlasAI** → gene lists → TxConformal → target prioritization

## Installation

```bash
git clone https://github.com/ying531/TxConformal.git
cd TxConformal
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Reference
- GitHub: https://github.com/ying531/TxConformal
- Authors: Ying Jin*, Kexin Huang*, Nathaniel Diamant, Kerry R. Buchholz, Steven T. Rutherford, Nicholas Skelton, Tommaso Biancalani, Gabriele Scalia, Jure Leskovec, Emmanuel J. Candès
