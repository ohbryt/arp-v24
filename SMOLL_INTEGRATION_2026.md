# SMolLM Integration: Small Language Model for Molecule Generation

**Date:** 2026-05-12  
**Source:** Jindal & Ju 2026, arXiv:2605.06322  
**GitHub:** https://github.com/akhljndl/smollm  
**HuggingFace:** akhljndl/smollm

---

## Overview

SMolLM is a 53K-parameter weight-shared transformer trained on ZINC-250K for SMILES generation.

| Feature | Value |
|---------|-------|
| **Parameters** | 53K (ultra-lightweight) |
| **Training data** | ZINC-250K (250K molecules) |
| **Architecture** | Weight-shared transformer |
| **Output** | Valid SMILES strings |

---

## ARP Pipeline Integration

### Molecular Design Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    ARP Molecular Design                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  SMolLM (SMILES generation)                                   │
│  └── 53K params → Fast generation                            │
│      ↓                                                        │
│  Boltz-2 (structure prediction)                              │
│  └── Validate 3D structure                                   │
│      ↓                                                        │
│  LinkLlama (linker optimization)                              │
│  └── Design protein linkers                                   │
│      ↓                                                        │
│  Final compound candidates                                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Why SMolLM?

| Aspect | SMolLM | Other LLMs |
|--------|--------|------------|
| **Size** | 53K params | 7B+ params |
| **Speed** | ~8h training | Days/weeks |
| **Local run** | ✅ Mac/ laptop | ❌ GPU required |
| **Purpose** | Molecule-specific | General |

---

## Installation

```bash
# Clone SMolLM
git clone https://github.com/akhljndl/smollm
cd smollm

# Install dependencies
uv sync

# macOS: install rdkit first
conda install -c conda-forge rdkit

# Train (if needed)
uv run python train.py --config ws-53k --seed 42

# Evaluate
uv run python eval.py --checkpoint checkpoints/ws-53k-s42.pt --n 10000
```

---

## Usage in ARP Pipeline

### Python API

```python
from smolm_integration import SMolLMGenerator

# Initialize
generator = SMolLMGenerator()

# Generate molecules
smiles_list = generator.generate(num=10)

# Generate with property targeting
ferroptosis_molecules = generator.generate_diverse(
    target_property="ferroptosis",
    num=20
)
```

### Integration with Boltz-2

```python
from smolm_integration import SMolLMGenerator
from boltz2_client import Boltz2Client

# Generate candidates
generator = SMolLMGenerator()
smiles_list = generator.generate(num=20)

# Validate with Boltz-2
boltz = Boltz2Client()
valid_candidates = []

for smi in smiles_list:
    structure = boltz.predict_structure(smi)
    if structure.score > 0.8:
        valid_candidates.append(smi)

print(f"Valid candidates: {len(valid_candidates)}/{len(smiles_list)}")
```

---

## Performance Metrics

| Metric | Description |
|--------|-------------|
| **Validity** | % of generated SMILES that are chemically valid |
| **Uniqueness** | % of unique structures |
| **Novelty** | % not in training set |
| **IntDiv** | Internal diversity |
| **FCD** | Fréchet ChemNet Distance |

---

## ARP Files Updated

| File | Content |
|------|---------|
| `smolm_integration.py` | SMolLM wrapper class |
| `SMOLL_INTEGRATION_2026.md` | This documentation |

---

## Key Findings from SMolLM Paper

1. **Weight sharing** enables 53K params instead of full model
2. **ZINC-250K** provides good chemical diversity
3. **Negative result:** DPO (Direct Preference Optimization) hurt validity
4. **Distillation:** 206K → 53K teacher-student works

---

## Next Steps

1. Clone and install SMolLM locally
2. Test generation with ferroptosis-relevant prompts
3. Integrate with Boltz-2 for structure validation
4. Compare with existing LinkLlama approach

---

*Generated: 2026-05-12 | ARP v24*  
*Integration: SMolLM 53K transformer for SMILES generation*