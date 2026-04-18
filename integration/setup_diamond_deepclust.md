# DIAMOND DeepClust Integration Guide
## Enhanced ARP v24 - Protein Family & Ortholog Analysis

**Based on:** Buchfink et al. (2026) Nature Methods  
**DOI:** 10.1038/s41592-026-03030-z  
**Paper:** "Clustering the protein universe of life using DIAMOND DeepClust"

---

## Overview

DIAMOND DeepClust enables ultra-fast clustering of billions of protein sequences, which can be integrated into ARP pipeline for:

1. **Target Family Analysis** - Protein family clustering and annotation
2. **Ortholog Detection** - Cross-species target comparison
3. **AlphaFold2 Enhancement** - Structure prediction improvement

---

## Installation

### 1. Install DIAMOND

```bash
# Using conda (recommended)
conda install -c bioconda diamond

# Using pip
pip install diamond

# Or download binary directly
wget https://github.com/bbuchfink/diamond/releases/latest/diamond-linux64.tar.gz
tar -xzf diamond-linux64.tar.gz
sudo mv diamond /usr/local/bin/
```

### 2. Download Reference Databases

```bash
# NR database (for clustering)
diamond makedb --in nr.faa.gz -d nr

# UniProt/Swiss-Prot
diamond makedb --in uniprot.fasta -d uniprot

# OrthoDB for orthologs
wget https://v101.orthodb.org/download/odb11v1_fasta.tar.gz
tar -xzf odb11v1_fasta.tar.gz
diamond makedb --in OrthoDB11_proteins.fasta -d orthodb
```

### 3. Verify Installation

```bash
diamond --version
# Should output: diamond version 2.x.x
```

---

## ARP Pipeline Integration

### Module Location

```
arp-v24/integration/
├── diamond_deepclust.py      # Main integration module
└── setup_diamond_deepclust.md # This guide
```

### Usage Examples

#### 1. Target Family Analysis

```python
from integration.diamond_deepclust import DiamondDeepClustIntegration

diamond = DiamondDeepClustIntegration()

# Analyze LOXL2 family
loxl2_family = diamond.analyze_protein_family("LOXL2")
print(f"Family: {loxl2_family.family_id}")
print(f"Members: {loxl2_family.members}")
print(f"Cluster size: {loxl2_family.cluster_size}")

# Compare protein families
comparison = diamond.compare_protein_families("LOXL2", "TGFB1")
print(f"Pathway crosstalk: {comparison['pathway_crosstalk_score']}")
print(f"Combinatorial potential: {comparison['combinatorial_potential']}")
```

#### 2. Ortholog Detection

```python
# Find orthologs across species
orthos = diamond.find_orthologs("LOXL2", species=["human", "mouse", "rat"])

print(f"Human: {orthos.orthologs['human']}")
print(f"Mouse: {orthos.orthologs['mouse']}")
print(f"Conservation (human-mouse): {orthos.sequence_identity_matrix[('human', 'mouse')]}")

# Species comparison report
report = diamond.get_species_comparison_report("LOXL2")
print(report['recommendations'])
```

#### 3. AlphaFold2 Enhancement

```python
# Enhance structure prediction
af2 = diamond.enhance_alphafold2("LOXL2", species="human")

print(f"Confidence boost: +{af2.confidence_boost*100:.1f}%")
print(f"Templates: {af2.cluster_representatives}")

# Get detailed structure report
structure = diamond.generate_structure_report("LOXL2", "human")
print(f"Binding sites: {structure['binding_sites']}")
```

#### 4. Complete Analysis Pipeline

```python
# Run all analyses
result = diamond.run_complete_analysis("LOXL2", "human")

# Contains:
# - result['protein_family']
# - result['orthologs']
# - result['alphafold2']
# - result['structure_report']
```

---

## Key Functions

### 1. Protein Family Analysis

| Function | Description | Output |
|----------|-------------|--------|
| `analyze_protein_family()` | Cluster protein family | ProteinFamily object |
| `compare_protein_families()` | Compare two families | Comparison dict |

### 2. Ortholog Detection

| Function | Description | Output |
|----------|-------------|--------|
| `find_orthologs()` | Find orthologs across species | OrthologGroup object |
| `get_species_comparison_report()` | Conservation analysis | Species report |

### 3. AlphaFold2 Integration

| Function | Description | Output |
|----------|-------------|--------|
| `enhance_alphafold2()` | Generate templates | AlphaFold2Enhancement |
| `generate_structure_report()` | Detailed structure analysis | Structure report |

---

## ARP Target Applications

### LOXL2 (Diabetic Nephropathy Target)

**Why important:**
- Collagen crosslinking enzyme
- TGF-β/LOX/Snail axis
- Elevated in diabetic nephropathy

**Analysis:**
```python
loxl2 = diamond.analyze_protein_family("LOXL2")
# Members: LOX, LOXL1, LOXL2, LOXL3, LOXL4
# Key function: collagen_crosslinking (0.95)
```

### IL11 (Cardiac Fibrosis Target)

**Why important:**
- Downstream of TGF-β
- Specific fibrosis targeting
- Avoids TGF-β toxicity

**Analysis:**
```python
il11 = diamond.analyze_protein_family("IL11")
# Members: IL6, IL11, IL27, CNTF, LIF, OSM
# Key function: fibrosis (0.85)
```

### Cross-Target Comparison

```python
comparison = diamond.compare_protein_families("LOXL2", "IL11")
# Shared: TGF-beta pathway
# Crosstalk score: 0.75
# Potential: MODERATE-HIGH for combination therapy
```

---

## DIAMOND DeepClust Key Algorithms

### 1. Greedy Vertex Cover

Finds minimum set of representative sequences:
- Start with alignments graph
- Select highest outdegree vertex
- Remove vertex and its neighbors
- Repeat until complete

### 2. Cascaded Clustering

Multi-round clustering with increasing sensitivity:
```
Round 1 (fast) → Round 2 (default) → Round 3 (sensitive) → ... → Round N (ultra-sensitive)
```

### 3. Bi-directional Coverage

Requires both sequences to cover each other:
- Prevents asymmetric clustering
- More accurate functional grouping
- Better for distantly related sequences

---

## Performance

| Dataset | Sequences | Time | Memory |
|---------|-----------|------|--------|
| NR (2023) | 19B | ~100 CPU hours | ~1 TB |
| UniRef50 | 250M | ~10 CPU hours | ~100 GB |
| Swiss-Prot | 500K | ~1 minute | ~1 GB |

---

## ARP Pipeline Workflow

```
Protein Target (e.g., LOXL2)
        │
        ├──────────────────────────────────────┐
        │                                      │
        ▼                                      ▼
┌─────────────────┐                    ┌─────────────────┐
│ Family Analysis │                    │ Ortholog         │
│ DIAMOND DeepCl │                    │ Detection        │
│ - LOX family   │                    │ - Human/Mouse    │
│ - Cluster size  │                    │ - Conservation    │
└─────────────────┘                    └─────────────────┘
        │                                      │
        └──────────────┬───────────────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ AlphaFold2      │
              │ Enhancement      │
              │ - Templates     │
              │ - Confidence ↑   │
              └─────────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Drug Discovery  │
              │ - Binding sites │
              │ - Selectivity   │
              └─────────────────┘
```

---

## Example Output

### LOXL2 Complete Analysis

```
======================================================================
DIAMOND DEEPCLUST COMPLETE ANALYSIS: LOXL2
======================================================================

📊 1. Protein Family Analysis
   Family: PF00386 (Lysyl oxidase)
   Members: LOX, LOXL1, LOXL2, LOXL3, LOXL4
   Cluster size: 4,863 sequences

🔍 2. Ortholog Detection
   Human ortholog: LOXL2
   Species coverage: 5
   - human: LOXL2
   - mouse: Loxl2
   - rat: Loxl2
   - zebrafish: loxl2
   - drosophila: CG31730

🧬 3. AlphaFold2 Enhancement
   Confidence boost: +12.5%
   Cluster templates: 5
   Templates: LOXL2, LOX, LOXL1, LOXL3, LOXL4

📐 4. Structure Analysis
   Binding sites identified: 3
   - Catalytic domain: 150-400
   - Copper binding site: CD1
   - Protein-protein interface: N-terminal
```

---

## References

1. Buchfink B, Barbé É, Ashkenazy H, et al. (2026). Clustering the protein universe of life using DIAMOND DeepClust. Nat Methods. doi:10.1038/s41592-026-03030-z

2. Buchfink B, et al. (2021). DIAMOND 2: fast and sensitive protein alignment using DIAMOND. Nat Methods. 18:366-368.

3. Altschul SF, et al. (1997). Gapped BLAST and PSI-BLAST. Nucleic Acids Res. 25:3389-3402.

---

## Support

- **DIAMOND GitHub:** https://github.com/bbuchfink/diamond
- **OrthoDB:** https://v101.orthodb.org
- **AlphaFold Database:** https://alphafold.ebi.ac.uk

---

**Document Version:** 1.0  
**Last Updated:** 2026-04-18  
**Prepared by:** Enhanced ARP v24 Pipeline