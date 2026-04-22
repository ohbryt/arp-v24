# MUSDTA - Multimodal Drug-Target Affinity Prediction

## Paper Info

| Field | Value |
|-------|-------|
| **PMID** | 42001823 |
| **DOI** | 10.1016/j.compbiolchem.2026.109053 |
| **Title** | A drug-target affinity prediction model integrating multimodal feature fusion and structural modeling |
| **Authors** | Yinan Xu et al. |
| **Journal** | Computational Biology and Chemistry |
| **Year** | 2026 |
| **Free article** | ✅ |
| **GitHub** | https://github.com/xu1nan/MUSDTA |

---

## Abstract

Deep learning model for drug-target binding affinity (DTA) prediction.

### Model Architecture

```
Drug Representation:
├── SMILES sequences → ChemBERTa (semantic features)
└── Graph Neural Networks (topological information)

Protein Representation:
├── ESM-2 pretrained model (sequence semantics)
├── Geometric Vector Perceptron (3D structural dependencies)
└── Graph Transformer (spatial geometry)

Fusion Module:
├── Multi-head attention mechanism
└── Gated feature fusion module
```

### Performance (State-of-the-art on 4 benchmarks)

| Dataset | Metrics |
|---------|---------|
| Davis | Best MSE, CI, rm2 |
| KIBA | Best MSE, CI, rm2 |
| PDBbind | Strong generalization |
| BindingDB | Strong ranking |

---

## Key Features

1. **Multimodal fusion** - Combines sequence + structure + graph features
2. **ESM-2 protein embeddings** - Pre-trained protein language model
3. **ChemBERTa drug embeddings** - Chemical language model
4. **3D structure modeling** - GVP + Graph Transformer for spatial geometry
5. **Interpretable** - Attention-based feature importance

---

## ARP v24 Integration Points

| Component | Integration |
|-----------|-------------|
| **DTA prediction** | Use MUSDTA for binding affinity scoring |
| **Protein embeddings** | ESM-2 for target representation |
| **Drug embeddings** | ChemBERTa for compound representation |
| **Benchmark comparison** | Validate against Davis, KIBA, PDBbind |
| **Open source** | https://github.com/xu1nan/MUSDTA |

---

## Why This Matters for ARP

Current ARP pipeline uses molecular docking for binding affinity. MUSDTA provides:
- **Faster screening** - ML-based vs docking
- **Higher accuracy** - Benchmarked against SOTA
- **Multimodal learning** - Captures drug-target interactions comprehensively

---

## Keywords

Drug discovery; Drug-target binding affinity; Multimodal Feature Fusion
