# AFSample2 Integration for ARP Pipeline
# Anti-Aging/Cancer Research Pipeline v24
# Targets: KDM4A, SLC7A11, DGAT1, GPX4, YARS2

## Overview
AFSample2 generates conformational ensembles for protein structure analysis.
This integration enables:
1. Multiple conformation prediction for drug target structures
2. Conformational flexibility analysis for drug binding
3. Protein-protein complex structure prediction

## Quick Start

### 1. Pull Docker image
```bash
docker pull kyogesh/afsample2:v1.1
```

### 2. Prepare targets (FASTA files)
```bash
# Create targets directory
mkdir -p targets/
cd targets/

# KDM4A (Human) - 359 aa
# SLC7A11 (Human) - 501 aa  
# DGAT1 (Human) - 488 aa
# GPX4 (Human) - 197 aa
# YARS2 (Human) - 471 aa
```

### 3. Run AFSample2
```bash
# Example for KDM4A
docker run --gpus 1 \
  -v $(pwd)/databases:/databases \
  -v $(pwd)/inputs:/inputs \
  -v $(pwd)/outputs:/outputs \
  kyogesh/afsample2:v1.1 \
  --method afsample2 \
  --fasta_paths inputs/KDM4A.fasta \
  --flagfile /app/alphafold/AF_multitemplate/monomer_full_dbs.flag \
  --nstruct 10 \
  --msa_rand_fraction 0.20 \
  --model_preset=monomer \
  --output_dir outputs/
```

## Target Proteins

| Protein | UniProt | Length | Role in ARP |
|---------|---------|--------|-------------|
| KDM4A | O75164 | 359 aa | H3K9me3 demethylase → SLC7A11 regulation |
| SLC7A11 | Q9UPY5 | 501 aa | Cystine transporter → ferroptosis |
| DGAT1 | O75907 | 488 aa | Diacylglycerol acyltransferase → lipid ROS |
| GPX4 | P36904 | 197 aa | Ferroptosis executioner |
| YARS2 | Q9Y2Z4 | 471 aa | Mitochondrial tRNA synthetase |

## Analysis Pipeline

### Conformational Ensemble Analysis
```python
import numpy as np
import pandas as pd

def analyze_ensemble(output_dir, protein_name):
    """Analyze AFSample2 output for conformational diversity."""
    # Load all predicted structures
    # Calculate RMSD between conformations
    # Identify flexible regions
    # Cluster by conformation type
    pass

# Key metrics:
# - RMSD distribution (structural diversity)
# - pLDDT score (local confidence)
# - PAE matrix (interaction confidence)
```

### Drug Binding Mode Analysis
For each target:
1. Compare apo (ligand-free) conformations
2. Identify binding pocket flexibility
3. Predict drug-target interactions across ensemble

## Integration with LinkLlama
```
AFSample2 → Conformational ensemble
    ↓
LinkLlama → Design linkers for protein complexes
    ↓
 RosettaSearch/AFsample2 → Optimize complex structures
```

## Next Steps
- [ ] Pull Docker image
- [ ] Download AlphaFold databases (or use reduced set)
- [ ] Create FASTA files for 5 targets
- [ ] Run AFSample2 for each target (n=10 conformations)
- [ ] Analyze conformational diversity
- [ ] Compare with known drug-bound structures
- [ ] Integrate with LinkLlama for complex prediction

## References
- AFSample2: https://github.com/wallnerlab/AFsample2
- Paper: https://doi.org/10.1038/s42003-025-07791-9
- Zenodo datasets: https://doi.org/10.5281/zenodo.14534088
