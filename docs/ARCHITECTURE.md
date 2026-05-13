# ARP v24 Architecture Document
**Date:** 2026-05-13  
**Version:** 2.0  
**Status:** ACTIVE

---

## Overview

ARP (Accelerated Research Pipeline) v24 is an AI-driven drug discovery platform that combines multi-omics data, foundation models, and iterative evaluation for biomarker and drug target identification.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        ARP v24 Architecture                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  INPUT LAYER                                                          │
│  ├── Multi-omics (scRNA, proteomics, metabolomics)                  │
│  ├── Literature (PubMed, patents)                                  │
│  ├── Spatial omics (MERFISH, Visium)                                │
│  └── Knowledge graphs (ImmuneKG, PrimeKG)                          │
│                                                                      │
│  ▼                                                                    │
│                                                                      │
│  CORE LAYER                                                           │
│  ├── arp_orchestrator.py (BIORESEARCHER-inspired multi-agent)       │
│  ├── boltz2_client.py (protein structure + affinity)                │
│  ├── arp_db.py (duckdb local storage)                               │
│  └── evidence_level.py (provenance tracking)                         │
│                                                                      │
│  ▼                                                                    │
│                                                                      │
│  AI/ML LAYER                                                         │
│  ├── stackfeat_rl_integration.py (stable biomarkers via RL)         │
│  ├── regformer_integration.py (single-cell foundation model)        │
│  ├── iterative_evaluation.py (BioDesignBench-style deep eval)        │
│  ├── scoring_rubric.py (100-point evaluation)                        │
│  └── medmarks_integration.py (model selection)                       │
│                                                                      │
│  ▼                                                                    │
│                                                                      │
│  SPATIAL LAYER                                                        │
│  ├── millimap_integration.py (spatial visualization)                 │
│  └── millimap (MERFISH, Xenium, Visium)                              │
│                                                                      │
│  ▼                                                                    │
│                                                                      │
│  OUTPUT LAYER                                                         │
│  ├── reports/ (target-specific reports)                              │
│  ├── targets/ (target registry)                                     │
│  └── evidence/ (experimental evidence)                               │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. arp_orchestrator.py

**Purpose:** Multi-agent research orchestration  
**Inspiration:** BIORESEARCHER (arXiv:2605.05985)  
**Playbooks:** discovery, screening, admet, synthetic_lethal, sarcopenia, cardio, masld, fsp1

```python
from arp_orchestrator import ARPOrchestrator, Playbook

orch = ARPOrchestrator()
result = orch.run("FSP1 inhibitor NSCLC", playbook=Playbook.FSP1)
```

### 2. boltz2_client.py

**Purpose:** Protein structure prediction + binding affinity  
**Based on:** Briefings in Bioinformatics 2026 (Boltz-2 benchmarking)

```python
from boltz2_client import Boltz2Client

boltz = Boltz2Client()
structure = boltz.predict_structure(smiles)
affinity = boltz.predict_affinity(protein, ligand)
```

### 3. evidence_level.py

**Purpose:** Provenance tracking and evidence classification  
**Levels:** REAL → VALIDATED → HEURISTIC → SIMULATED

```python
from evidence_level import EvidenceLevel, add_evidence_level

target = add_evidence_level(
    target,
    EvidenceLevel.VALIDATED,
    "Boltz-2 prediction",
    ["Nature 2025"]
)
```

---

## AI/ML Components

### iterative_evaluation.py

**Purpose:** BioDesignBench-inspired iterative candidate evaluation  
**Key insight:** "Evaluation depth correlates with score at ρ = 0.685"

```python
from iterative_evaluation import IterativeEvaluator, EvaluationDepth

evaluator = IterativeEvaluator(max_iterations=5)
results = evaluator.evaluate(candidates)
# Depth: SURFACE → STANDARD → COMPREHENSIVE → EXPERT
```

### scoring_rubric.py

**Purpose:** 100-point evaluation rubric  
**Categories:** Approach (20), Orchestration (20), Quality (30), Impact (30)

```python
from scoring_rubric import score_candidate

result = score_candidate(candidate)
# Grade: A+ to F
```

### stackfeat_rl_integration.py

**Purpose:** Stable biomarker discovery via RL  
**Source:** arXiv:2604.22892 (StackFeat-RL)

```python
from stackfeat_rl_integration import biomarker_discovery

result = biomarker_discovery(X, y, gene_names, "ferroptosis")
```

### regformer_integration.py

**Purpose:** Single-cell foundation model  
**Source:** BGIResearch/RegFormer

```python
from regformer_integration import analyze_single_cell

result = analyze_single_cell("data.h5ad", task="emb")
```

### medmarks_integration.py

**Purpose:** Medical LLM model selection  
**Source:** arXiv:2605.01417 (Medmarks)

```python
from medmarks_integration import get_recommendations

recs = get_recommendations()
# orchestrator: gemini_3_pro_preview
# biomarker: gpt_5_1
```

---

## Target Programs

### FSP1 (NSCLC Ferroptosis)
- **Target:** FSP1 (AIFM2), Ferroptosis Suppressor Protein 1
- **Indication:** KEAP1/STK11/NFE2L2-altered NSCLC
- **Approach:** Triple ferroptosis (FSP1 + SLC7A11 + DGAT1)
- **Stage:** Preclinical

### Sarcopenia (Muscle Loss)
- **Targets:** mTORC1, Myostatin, AMPK, GDF15/GFRAL
- **Indication:** Age-related muscle loss
- **Approach:** Senolytic + muscle preservation combo
- **Stage:** Discovery

### MASLD (Metabolic)
- **Targets:** ACLY/ACSS2, GLP-1, FXR, PPAR
- **Indication:** MASH F2-F3
- **Approach:** Dual acetyl-CoA inhibition
- **Stage:** Preclinical

---

## Directory Structure

```
arp-v24/
├── arp/                          # Core source (planned)
├── arp_orchestrator.py           # Main orchestrator
├── boltz2_client.py              # Structure prediction
├── evidence_level.py            # Provenance
├── iterative_evaluation.py      # Deep evaluation
├── scoring_rubric.py            # 100-point scoring
├── stackfeat_rl_integration.py  # Biomarker RL
├── regformer_integration.py      # Single-cell
├── millimap_integration.py       # Spatial
├── medmarks_integration.py       # Model selection
├── targets/                      # Target registry
│   └── targets.json
├── configs/                     # Configuration
│   └── pipeline.yaml
├── reports/                     # Reports by target
├── evidence/                    # Raw evidence
├── schemas/                     # JSON schemas
│   └── output_schema.json
├── .github/workflows/           # CI/CD
│   └── ci.yml
└── docs/                       # Documentation
    └── ARCHITECTURE.md (this)
```

---

## Branch Strategy

| Branch | Purpose | Status |
|--------|---------|--------|
| `main` | Stable, production | Protected |
| `exp/sirna-pf14-2026` | Current experiment | Active |
| `feat/*` | New features | Development |
| `fix/*` | Bug fixes | As needed |

---

## Operating Standards

See `ARP_V24_OPERATING_STANDARDS.md` for:
- Branch naming convention
- File naming rules
- Config separation (target_id vs experiment_id)
- Commit message format

---

## Key References

| Paper | Source | Integration |
|-------|--------|-------------|
| BioDesignBench | arXiv:2604.22892 | iterative_evaluation.py |
| StackFeat-RL | arXiv:2604.22892 | stackfeat_rl_integration.py |
| RegFormer | GitHub/BGI | regformer_integration.py |
| MilliMap | milliomics.com | millimap_integration.py |
| Medmarks | arXiv:2605.01417 | medmarks_integration.py |
| PD Union | medRxiv 2026 | stage_policies.py |
| Boltz-2 | Briefings in Bioinformatics 2026 | boltz2_client.py |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-04-26 | Initial (sarcopenia pipeline) |
| 2.0 | 2026-05-12 | BioDesignBench integration |
| 2.1 | 2026-05-13 | 4 new integrations + docs |

---

*Generated: 2026-05-13 | ARP v24*  
*Architecture document v2.0*