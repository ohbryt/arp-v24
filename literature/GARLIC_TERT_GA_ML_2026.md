# Garlic-Derived Ligands for hTERT - Genetic Algorithm + ML Pipeline

## Paper Info

| Field | Value |
|-------|-------|
| **PMID** | 42013033 |
| **Title** | Genetic algorithm-guided design of garlic-derived ligands targeting TEN domain of telomerase reverse transcriptase |
| **Authors** | Hassen Elmir et al. |
| **Journal** | Comput Methods Biomech Biomed Engin |
| **Year** | 2026 |
| **Target** | hTERT (human telomerase reverse transcriptase) |

---

## Abstract

Human telomerase reverse transcriptase (hTERT) is a key target for anticancer drug discovery. This study developed a computational pipeline:

### Pipeline Architecture
```
1. Garlic phytochemicals → Initial chemical space
2. Genetic Algorithm (GA) iterative evolution
   - Mutation + fragment expansion
3. Multi-parameter fitness function:
   - Lipinski, Veber, Ghose drug-likeness rules
   - QED (quantitative estimate of drug-likeness)
   - H-bond donor/acceptor balance
   - Aromatic ring constraints
4. RandomForest classifier → pre-screen telomerase activity
5. Molecular docking (CB-Dock2)
6. ADMET evaluation (SwissADME)
```

### Results
| Metric | Value |
|--------|-------|
| Generated ligands | 125 |
| Passed drug-likeness + activity | 14 |
| Best binding affinity | -10.5 kcal/mol |
| ADMET violations | Top compound excluded |

---

## Key Novelty

1. **GA + ML integration** - RandomForest pre-screening before docking
2. **Garlic-derived natural products** - Novel scaffold discovery
3. **Multi-parameter optimization** - Drug-likeness + activity combined

---

## Connection to ARP

- **Natural compound pipeline**: Garlic phytochemicals workflow
- **Genetic algorithm**: BOAT integration reference
- **TERT targeting**: Cancer therapeutic target
- **ADMET filtering**: SwissADME-style evaluation

---

## Keywords

Genetic algorithm; TEN domain; activity classification; cancer drug discovery; garlic-derived ligands; machine learning; telomerase reverse transcriptase
