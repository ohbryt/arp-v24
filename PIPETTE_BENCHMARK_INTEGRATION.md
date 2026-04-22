# Pipette Benchmark Integration for ARP v24
## Multi-Agent Bioinformatics for Drug Discovery

**Document Type:** Tool Integration  
**Date:** April 2026  
**Source:** https://github.com/variomeanalytics/pipette_benchmark  
**biolab preprint:** Scientific literature → executable skill graph

---

## 1. Overview

**Pipette** encodes scientific literature into an executable skill graph for multi-agent bioinformatics. It demonstrates:

| Capability | Performance |
|------------|-------------|
| **Small molecule docking** | RMSD 0.89 Å vs crystal pose |
| **Cyclic peptide design** | CP07 at -12.1 kcal/mol |
| **Clinical variant analysis** | 7/7 sensitivity, 0 FP |
| **scRNA-seq analysis** | r = 0.959-0.991 concordance |

---

## 2. Repository Structure

```
pipette_benchmark/
├── benchmark/
│   ├── DrugDesign/
│   │   ├── Imatinib/        # Small molecule docking
│   │   │   ├── scripts/
│   │   │   ├── results/
│   │   │   ├── reports/
│   │   │   └── thinking.md
│   │   └── peptides/         # Cyclic peptide design
│   │       └── ...
│   ├── clinical_variants/    # ACMG variant analysis
│   ├── clinical_variants_spikein/  # Spike-in detection
│   └── scRNA-seq/          # PBMC, Pancreas, Rice
```

---

## 3. Key Capabilities for ARP v24

### 3.1 Drug Design (Direct Relevance!)

| Task | Input | Our Use Case |
|------|-------|--------------|
| **Imatinib → ABL1 docking** | PDB 2HYY | MMP11 inhibitor docking |
| **Cyclic peptide design** | PDB 1YCR | C7/APW-4/HN-1 peptide optimization |

#### Imatinib Benchmark Results

```
Task: Redock imatinib into ABL1 kinase ATP-binding site
Result: Binding affinity -11.8 kcal/mol
RMSD: 0.89 Å vs crystal pose
Self-correction: Fixed pH 7.4 protonation
```

**Our application:**
```
MMP11 inhibitor docking
Input: PDB structure of MMP11 (AlphaFold3)
Tool: AutoDock-GPU or Smina
Target: Known MMP11 inhibitors from ChemBL
```

### 3.2 Peptide Design

```
Task: Design 10 cyclic peptides mimicking p53 hotspot triad
Input: PDB 1YCR
Result: Top candidate CP07 at -12.1 kcal/mol
Hotspot Cα RMSD: 0.95 Å vs native p53
```

**Our application:**
```
Cardiac-homing peptide optimization
Input: C7, APW-4, HN-1 sequences
Tool: LinkLlama + RosettaSearch + Pipette
Goal: Improve cardiac targeting affinity
```

---

## 4. Integration with Our Pipeline

### 4.1 Complete Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│           AR 24 DRUG DISCOVERY PIPELINE v2                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Literature Phase:                                                  │
│  • ChemBL → MMP11 inhibitors (Ki values, SMILES)                │
│  • PubMed → GDF10 mechanism                                      │
│  • Groq → Fast literature summarization                          │
│                    ↓                                               │
│  In Silico Phase:                                                  │
│  • Pipette → Docking validation (Imatinib-style)                 │
│  • LinkLlama → Linker optimization                               │
│  • RosettaSearch → Structure validation                           │
│                    ↓                                               │
│  NAMs Validation:                                                 │
│  • iPSC-CMs → GDF10 maturation                                   │
│  • Cardiac organoids → Fibrosis model                             │
│                    ↓                                               │
│  Lead Optimization:                                                │
│  • Pipette peptides → C7/APW-4/HN-1 optimization                │
│  • Self-correction → Iterative improvement                        │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 MMP11 Inhibitor Workflow

```python
# Step 1: Get compounds from ChemBL
from api.chembl import ChEMBLClient
client = ChEMBLClient()
mmp11_inhibitors = client.enrich_gene("MMP11")

# Step 2: Dock with Pipette-style approach
# (Pipette uses AutoDock-GPU internally)
# Result: Binding affinity prediction

# Step 3: Score and rank
# Criteria: Ki < 100 nM, selectivity > 50x vs MMP1/2/9
```

### 4.3 Cardiac Peptide Optimization

```python
# Step 1: Current sequences
peptides = ["APWHLSSQ", "APWHLSSQALPK", "SWKLYPSPLHKC"]

# Step 2: Run through Pipette peptide design module
# (similar to p53-MDM2 targeting)

# Step 3: Validate with RosettaSearch
# Step 4: Select best candidate
```

---

## 5. Self-Correction Capability

Pipette's key feature is **self-correction**:

| Error | Correction |
|-------|------------|
| Missing protonation | Fixed pH 7.4 |
| Wrong RMSD method | Hungarian → Kabsch SVD |
| False positive variant | Demoted to VUS |

**For our use case:**
```
MMP11 docking → Low affinity
        ↓
Check: protonation state?
        ↓
Fix: Correct pKa at active site
        ↓
Re-dock → Improved affinity
```

---

## 6. Repository Contents

### 6.1 DrugDesign/Imatinib/

| File | Description |
|------|-------------|
| `scripts/` | AutoDock-GPU docking scripts |
| `results/` | Docking poses, scores |
| `reports/` | Analysis markdown |
| `thinking.md` | Agent reasoning log |
| `provenance.json` | Full execution trace |

### 6.2 DrugDesign/peptides/

For cyclic peptide design methodology.

### 6.3 Clinical Variants

For SNP/variant interpretation pipeline.

---

## 7. How to Use

### 7.1 Study the Methodology

```bash
cd pipette_benchmark/benchmark/DrugDesign/Imatinib
cat thinking.md  # Agent's decision process
cat reports/*.md  # Final analysis
```

### 7.2 Adapt Scripts

```bash
# Copy relevant scripts
cp -r pipette_benchmark/benchmark/DrugDesign/Imatinib/scripts ./our_docking/
cd our_docking
# Modify for MMP11 targets
```

---

## 8. Comparison with Our Tools

| Tool | Strength | Integration |
|------|-----------|--------------|
| **Pipette** | Self-correcting multi-agent | Learn methodology |
| **ChemBL** | Real bioactivity data | Direct API |
| **LinkLlama** | Linker optimization | Direct use |
| **RosettaSearch** | Structure validation | Direct use |
| **Groq** | Fast literature analysis | Direct use |

---

## 9. Key Takeaways from Pipette

### 9.1 Best Practices

1. **Self-correction is essential** - Always validate and fix
2. **Provenance tracking** - Log every step
3. **Multiple validation methods** - Don't rely on single metric
4. **Literature → executable** - Encode domain knowledge in scripts

### 9.2 For Our MMP11/GDF10 Project

```
• Use Pipette-style docking for MMP11 inhibitors
• Apply peptide design for cardiac-homing optimization  
• Implement self-correction in our pipeline
• Track provenance (logs, reports, reasoning)
```

---

## 10. References

- GitHub: https://github.com/variomeanalytics/pipette_benchmark
- BioRxiv: (to be added upon publication)

---

*Document generated by ARP v24 Research Pipeline · April 2026*
