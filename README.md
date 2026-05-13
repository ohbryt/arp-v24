# ARP v24 - AI-Driven Drug Discovery Pipeline

> Accelerated Research Pipeline for biomarker and drug target identification

**Version:** 2.1 | **Date:** 2026-05-13

---

## 🎯 Overview

ARP v24 is an AI-driven drug discovery platform that combines:
- Foundation models (ESM2, Boltz-2, RegFormer)
- Iterative evaluation (BioDesignBench-inspired)
- Spatial omics (MERFISH, MilliMap)
- Multi-omics integration

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/ohbryt/arp-v24.git
cd arp-v24

# Run orchestration
python3 arp_orchestrator.py "FSP1 inhibitor NSCLC" --playbook fsp1

# Test biomarkers
python3 -c "from stackfeat_rl_integration import biomarker_discovery; print('OK')"
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `arp_orchestrator.py` | Multi-agent research orchestration |
| `boltz2_client.py` | Protein structure + affinity |
| `iterative_evaluation.py` | BioDesignBench-style deep evaluation |
| `scoring_rubric.py` | 100-point evaluation |
| `stackfeat_rl_integration.py` | Stable biomarkers via RL |
| `regformer_integration.py` | Single-cell foundation model |
| `millimap_integration.py` | Spatial omics visualization |
| `medmarks_integration.py` | Medical LLM model selection |

---

## 🧬 Target Programs

| Program | Disease | Target | Stage |
|---------|---------|--------|-------|
| **FSP1** | NSCLC | Ferroptosis suppressor | Preclinical |
| **Sarcopenia** | Muscle loss | mTORC1, Myostatin | Discovery |
| **MASLD** | MASH | ACLY/ACSS2 | Preclinical |

---

## 🔬 Technology Stack

```
Multi-omics Data
    ↓
Foundation Models
├── ESM2 (protein embeddings)
├── Boltz-2 (structure + affinity)
└── RegFormer (single-cell)
    ↓
Iterative Evaluation (BioDesignBench)
    ↓
100-Point Scoring Rubric
    ↓
Reports + Evidence
```

---

## 📊 Evidence Levels

| Level | Description | Example |
|-------|-------------|---------|
| 🟢 REAL | Experimental data | TCGA, GEO |
| 🔵 VALIDATED | AI-predicted, confirmed | Boltz-2 + literature |
| 🟡 HEURISTIC | Rule-based | LASSO selection |
| 🔴 SIMULATED | In silico only | Molecular dynamics |

---

## 🌐 Spatial Analysis

**MilliMap** for spatial omics:
```python
from millimap_integration import load_spatial_data

result = load_spatial_data("merfish.h5ad")
```

Download: [milliomics.com](https://milliomics.com/millimap/docs/)

---

## 🤖 Model Selection (Medmarks)

| Task | Model | Score |
|------|-------|-------|
| Orchestrator | gemini_3_pro_preview | 0.89 |
| Biomarker | gpt_5_1 | 0.88 |
| Design | gpt_5_2 | 0.87 |

---

## 📂 Directory Structure

```
arp-v24/
├── arp_orchestrator.py       # Main
├── boltz2_client.py          # Structure
├── evidence_level.py         # Provenance
├── iterative_evaluation.py   # Evaluation
├── scoring_rubric.py         # Scoring
├── stackfeat_rl_integration.py
├── regformer_integration.py
├── millimap_integration.py
├── medmarks_integration.py
├── targets/
│   └── targets.json          # Target registry
├── configs/
│   └── pipeline.yaml         # Config
├── reports/                  # By target
├── docs/
│   └── ARCHITECTURE.md
└── schemas/
    └── output_schema.json
```

---

## 📖 Documentation

- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - System architecture
- [ARP_V24_OPERATING_STANDARDS.md](ARP_V24_OPERATING_STANDARDS.md) - Operating rules
- [ARP_BIODESIGNBENCH_UPGRADE_2026.md](ARP_BIODESIGNBENCH_UPGRADE_2026.md) - BioDesignBench integration
- [ARP_UPGRADE_V2_2026.md](ARP_UPGRADE_V2_2026.md) - Upgrade v2 details

---

## 🔗 References

| Paper | DOI/URL |
|-------|---------|
| BioDesignBench | [arXiv:2604.22892](https://arxiv.org/abs/2604.22892) |
| StackFeat-RL | [arXiv:2604.22892](https://arxiv.org/abs/2604.22892) |
| RegFormer | [GitHub/BGIResearch](https://github.com/BGIResearch/RegFormer) |
| Medmarks | [arXiv:2605.01417](https://arxiv.org/abs/2605.01417) |
| Boltz-2 | Briefings in Bioinformatics 2026 |
| PD Union | [medRxiv](https://doi.org/10.64898/2026.05.05.26352278) |

---

## 📝 License

Open source - See individual component licenses

---

**Maintainer:** 오창명 (DRCMOH)  
**Organization:** Brown Biotech AI Drug Discovery  
**GitHub:** [ohbryt/arp-v24](https://github.com/ohbryt/arp-v24)