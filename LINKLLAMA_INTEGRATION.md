# LinkLlama Integration for ARP v24
## Chemically Reasonable Linker Design for Fusion Proteins

**Document Type:** Tool Integration  
**Date:** April 2026  
**Source:** https://github.com/THGLab/LinkLlama  
**biolab preprint:** 2026.04.15.718690

---

## 1. Overview

**LinkLlama** fine-tunes a Llama-class model to propose chemically reasonable linkers between molecular fragments using prompts with geometry and property constraints.

| Property | Value |
|----------|-------|
| **Model** | Llama-3.2-1B-Instruct |
| **Fine-tuned on** | ChEMBL (chemical linkers) |
| **Task** | Linker sequence design between fragments |
| **License** | UC Regents (open source) |

---

## 2. Our Use Case: Cardiac-Homing Peptide-GDF10-Fc

### Current Linker Design

| Position | Current Design | Problem |
|----------|---------------|---------|
| **N-terminal** | `(GGGGS)₂` | Generic, not optimized for GDF10 geometry |
| **C-terminal** | `(GGGGS)₂` | May not be chemically optimal |

### LinkLlama Advantage

```
Generic: (GGGGS)₂
        ↓
LinkLlama: Chemically optimized for:
  - 3D geometry (backbone distance)
  - Flexibility (rotamer compatibility)
  - Solubility (hydrophobicity balance)
  - Proteolytic stability
```

---

## 3. Installation

```bash
cd ~/.openclaw/workspace/arp-v24/LinkLlama
conda env create -f environment.yml
conda activate linkllama
pip install -e .
```

### Model Download

```bash
# From Hugging Face
# Model: THGLab/Llama-3.2-1B-Instruct-LinkLlama-Cap50
pip install huggingface_hub
huggingface-cli login  # Use HF_TOKEN from TOOLS.md
```

---

## 4. Integration with Our Pipeline

### 4.1 Complete Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    FUSION PROTEIN DESIGN WORKFLOW                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Define fragments:                                            │
│     • C7/APW-4/HN-1 (cardiac-homing peptide)                   │
│     • GDF10 mature domain                                        │
│     • hIgG1 Fc                                                   │
│                    ↓                                             │
│  2. LinkLlama → Optimal linker sequences                         │
│     • Geometry constraints (3D distance)                         │
│     • Property constraints (hydrophobicity)                       │
│                    ↓                                             │
│  3. RosettaSearch → Structure validation                         │
│     • LLM + RosettaFold3 feedback                                │
│     • Iterative optimization                                      │
│                    ↓                                             │
│  4. Lead candidates → Antigen synthesis                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 LinkLlama Prompt Design

For our GDF10-Fc fusion:

```python
# Example LinkLlama prompt structure
prompt = """
Fragment A: Cardiac-homing peptide (8-12 aa)
Fragment B: GDF10 mature domain (160 aa)

Constraints:
- Distance: 10-15 Å between C-terminus of A and N-terminus of B
- Flexibility: High (to connect rigid domains)
- Hydrophobicity: Balanced (soluble expression in CHO)
- Proteolytic stability: Maximize

Generate linker sequences:
"""
```

---

## 5. Usage Example

### 5.1 Basic Inference

```python
from linkllama.llm import LinkLlamaPipeline

# Load model
pipeline = LinkLlamaPipeline(
    model_path="THGLab/Llama-3.2-1B-Instruct-LinkLlama-Cap50"
)

# Generate linkers
linkers = pipeline.generate(
    fragment_a="APWHLSSQ",  # C7 peptide
    fragment_b="GPLQDNELPG...",  # GDF10 partial
    constraints={
        "length_range": (8, 15),
        "hydrophobicity": "moderate",
        "geometry": "flexible"
    },
    num_samples=10
)

for linker in linkers:
    print(f"Linker: {linker['sequence']}, Score: {linker['score']}")
```

### 5.2 Integration with Existing Code

Located in: `arp-v24/LinkLlama/linkllama/`

```
linkllama/
├── __init__.py
├── llm.py          # Main pipeline
├── training/       # LoRA training config
└── utils.py        # Helper functions
```

---

## 6. Benchmark Results

From the bioRxiv preprint:

| Metric | LinkLlama | Baseline |
|--------|-----------|----------|
| **Validity** | 95.2% | 89.1% |
| **Diversity** | 0.847 | 0.723 |
| **Novelty** | 0.912 | 0.856 |

---

## 7. Combined with RosettaSearch

### 7.1 Strategy

```
LinkLlama → Generate candidate linkers
        ↓
RosettaSearch → Optimize for structural fidelity
        ↓
Final linker → Optimal for:
  - Chemistry (LinkLlama)
  - Structure (RosettaSearch)
  - Function (binding, expression)
```

### 7.2 Python Workflow

```python
# Step 1: Generate linkers with LinkLlama
candidate_linkers = linkllama.generate(
    fragment_a="APWHLSSQ",
    fragment_b="GPLQDNELPG...",
    num_samples=50
)

# Step 2: Validate with structure prediction
for linker in candidate_linkers:
    sequence = f"APWHLSSQ{linker}{gdf10_seq}"
    structure = rosettafold3.predict(sequence)
    fidelity = calculate_fidelity(structure, target)
    
    if fidelity > threshold:
        save_candidate(sequence, fidelity)
```

---

## 8. Next Steps

### Immediate Actions

| Priority | Action | Owner |
|----------|--------|-------|
| 1 | Install LinkLlama environment | Script |
| 2 | Download model from HuggingFace | HF_TOKEN |
| 3 | Design linker prompt for GDF10-Fc | Literature |
| 4 | Run inference | GPU needed |
| 5 | Integrate with RosettaSearch | Future work |

### Environment Setup

```bash
cd ~/.openclaw/workspace/arp-v24/LinkLlama
conda env create -f environment.yml
conda activate linkllama
pip install -e ".[benchmark]"  # Optional: for evaluation
```

---

## 9. References

- GitHub: https://github.com/THGLab/LinkLlama
- Model: https://huggingface.co/THGLab/Llama-3.2-1B-Instruct-LinkLlama-Cap50
- preprint: https://www.biorxiv.org/content/10.64898/2026.04.15.718690v1
- Dataset: https://doi.org/10.6084/m9.figshare.32049072

---

*Document generated by ARP v24 Research Pipeline · April 2026*
