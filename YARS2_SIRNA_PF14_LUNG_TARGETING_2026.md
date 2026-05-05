# YARS2 siRNA + Lung Targeting Peptide (PF14) Research Framework
**ARP v24 | Updated: 2026-05-05**

---

## Executive Summary

**Hypothesis:** Mitochondrial tyrosyl-tRNA synthetase YARS2 is a valid therapeutic target in NSCLC, and PF14 peptide enables efficient lung-targeted siRNA delivery for systemic YARS2 knockdown.

**Target:** YARS2 (Tyrosyl-tRNA Synthetase 2, mitochondrial)
**Delivery:** PF14 peptide-siRNA complexes
**Indication:** NSCLC (Non-Small Cell Lung Cancer)

---

## 1. YARS2 Biology

### 1.1 Gene & Protein
| Property | Details |
|----------|---------|
| Gene Symbol | YARS2 |
| Full Name | Tyrosyl-tRNA Synthetase 2, mitochondrial |
| Location | Nuclear genome (chr12: 32,191,239-32,225,477) |
| Protein Length | 471 amino acids |
| EC Number | 6.1.1.1 |
| Subcellular | Mitochondria |
| Function | tRNA(Tyr) + L-tyrosine + ATP → L-tyrosyl-tRNA(Tyr) + AMP + PPi |

### 1.2 Normal Function
- Catalyzes tyrosine attachment to mitochondrial tRNA^Tyr
- Essential for mitochondrial protein synthesis (mtDNA-encoded proteins)
- Supports oxidative phosphorylation (OXPHOS)
- Maintains mitochondrial translation fidelity
- Pathogenic variants → MLASA syndrome (myopathy, lactic acidosis, sideroblastic anemia)

### 1.3 Cancer Relevance

#### Expression Pattern
- **Human Protein Atlas:** Low tissue specificity — detected in all tissues
- **TCGA:** Low cancer specificity — expressed across 20 cancer types
- **CRC study (2022):** mRNA significantly overexpressed in colorectal cancer vs normal tissue
- **Lung cancer:** Protein expression confirmed (HPA038721, HPA057610 antibodies)

#### Known Cancer Functions (from CRC study)
```
YARS2 knockdown in SW620 (CRC):
  ↓ tRNA^Tyr steady-state levels
  ↓ OCR (oxygen consumption rate)
  ↓ ATP synthesis
  ↑ ROS (reactive oxygen species)
  → Inhibits proliferation and migration
  → Sensitizes to 5-FU (chemotherapy)
```

#### Mechanistic Link to Ferroptosis (Hypothesis)
- Mitochondrial translation inhibition → ETC dysfunction → ROS accumulation
- ROS accumulation → lipid peroxidation → ferroptosis
- YARS2 knockdown may prime cancer cells for ferroptosis

---

## 2. Target Validation Strategy

### 2.1 Bioinformatic Analysis
| Database | Query |
|----------|-------|
| GEPIA2 | YARS2 expression in LUAD/LUSC vs normal |
| TCGA-LUAD | YARS2 survival analysis (Kaplan-Meier) |
| cBioPortal | YARS2 mutation frequency, co-occurrence |
| Human Protein Atlas | YARS2 IHC in lung cancer vs normal |
| CCLE | YARS2 mRNA in NSCLC cell lines (A549, H1299, H460, PC9) |

### 2.2 Expected Expression Pattern
Based on CRC data and cancer dependency databases:
- **YARS2 HIGH:** Cancer cells with high mitochondrial metabolism (Warburg effect in reverse)
- **YARS2 LOW/NEGATIVE:** Normal lung pneumocytes, stromal cells
- **Therapeutic window:** Cancer cells rely heavily on mitochondrial translation

### 2.3 Patient Selection Biomarkers
```
Priority 1: High YARS2 protein expression (IHC)
Priority 2: High mitochondrial activity (OCR/ATP high)
Priority 3: Low GPX4 (ferroptosis-primed tumors)
Priority 4: KRAS mutant (from Martin et al. 2026 — lineage-specific dependencies)
```

---

## 3. PF14 Peptide Delivery System

### 3.1 Background
From **Foged lab (University of Copenhagen)** — published in Scientific Reports (2019):

> "We have previously developed efficient peptide-based nucleic acid delivery vectors PF14 and NF55, where we have shown that these vectors **preferentially transfect lung tissue upon systemic administration** with the nucleic acid."

### 3.2 PF14 Characteristics
| Property | Details |
|----------|---------|
| Type | Cationic amphipathic peptide |
| Length | ~30 amino acids |
| Mechanism | Endosomal escape via proton sponge effect |
| Specificity | Lung > liver > other organs |
| Cargo | siRNA, miRNA, plasmid DNA |
| N/P Ratio | **1-4** (CRITICAL: NOT 5-10) |

### 3.3 Critical Formulation Parameters

#### N/P Ratio (Charge Ratio)
**N/P = 1-4** (number of nitrogen atoms in peptide / phosphate groups in siRNA)

| N/P | Complex Charge | Typical Result |
|-----|---------------|----------------|
| 1-2 | Near neutral | Low transfection |
| 3-4 | Mildly positive | **OPTIMAL** |
| 5-10 | Too positive | Aggregation, toxicity |

#### siRNA Sequence Design
```
Target: YARS2 mRNA (NM_001165435.1)
Location: Exon 2-3 junction (conserved across variants)

siRNA #1: 5'-GCAGCAAGUUCGAGAGCAUtt-3' (targeting 546-566)
siRNA #2: 5'-GGAGCUGAUCCGCGACAUAtt-3' (targeting 1128-1148)
siRNA #3: 5'-GCUACAGCGCCGACGACGUtt-3' (targeting 756-776)

Positive control: siYARS2 #2 (most potent in CRC study)
Negative control: siCtrl (non-targeting sequence)
```

### 3.4 PF14-siRNA Complex Formation Protocol
```python
# PF14-YARS2 siRNA Complex Formation
# Based on N/P = 3 (optimal)

import numpy as np

def calculate_NP_ratio(peptide_ug, siRNA_ug, peptide_lysine_content=0.25):
    """
    PF14 ~30 AA, ~25% Lysine residues
    Peptide MW ~3500 Da
    siRNA MW ~13,000 Da (21-23 bp)
    """
    peptide_nitrogen = (peptide_ug / 3500) * 3  # ~3 Lys per peptide
    siRNA_phosphate = (siRNA_ug / 13000) * 42  # ~42 bp × 2 phosphates
    return peptide_nitrogen / siRNA_phosphate

# For N/P = 3:
# peptide_ug = 3 × (siRNA_ug / 3) × (13000/3500) ≈ 3.7 × siRNA_ug
```

---

## 4. In Vitro Validation Plan

### 4.1 Cell Lines
| Cell Line | Histology | KRAS Status | YARS2 Expected |
|-----------|-----------|-------------|----------------|
| A549 | Adenocarcinoma | G12S mut | HIGH |
| H1299 | Adenocarcinoma | WT | HIGH |
| H460 | Large cell | Q61H mut | HIGH |
| PC9 | Adenocarcinoma | delE746-A750 | MODERATE |
| BEAS-2B | Normal bronchial | WT | LOW |

### 4.2 Assay Panel
| Day | Assay | Readout |
|-----|-------|---------|
| 1 | siRNA transfection (PF14) | -- |
| 2 | qRT-PCR (YARS2 mRNA) | Knockdown efficiency |
| 3 | Cell viability (CCK-8) | Antiproliferation |
| 3 | Apoptosis (Caspase-3/7) | Cell death |
| 3 | MitoSOX + DCFDA | ROS measurement |
| 3 | Ferroptosis markers (GPX4, GSSG) | Lipid peroxidation |
| 4 | Colony formation | Long-term effect |
| 5 | Migration (Transwell) | Antimetastasis |

### 4.3 Positive Controls for Validation
- **CARS knockdown:** Known ferroptosis inducer (via cyst(e)ine depletion)
- **GPX4 knockdown:** Direct ferroptosis executioner
- **Erastin:** System Xc^- inhibitor (ferroptosis inducer)

---

## 5. In Vivo Validation Plan

### 5.1 Orthotopic NSCLC Model
```
Model: A549-luciferase or H1299-luciferase
Route: Tail vein injection or intratracheal instillation
Monitoring: IVIS bioluminescence imaging

Treatment Groups (n=8/group):
1. Vehicle (PBS)
2. siCtrl + PF14 (negative control)
3. siYARS2 #1 + PF14 (low dose)
4. siYARS2 #2 + PF14 (mid dose) ← use based on CRC study
5. siYARS2 #3 + PF14 (high dose)
6. siYARS2 #2 + PF14 + Erastin (combo)
7. siYARS2 #2 + PF14 + sulfasalazine (system Xc^- inhibitor)
```

### 5.2 Dosing Schedule
- **Dose:** 50 μg siRNA + PF14 (N/P=3) per injection
- **Volume:** 100 μL PBS
- **Route:** IV injection (systemic) OR inhalation (direct lung)
- **Schedule:** Every 3 days × 4 cycles
- **Duration:** 21 days

### 5.3 Endpoints
| Endpoint | Method |
|----------|--------|
| Tumor burden | IVIS imaging (bioluminescence) |
| Lung weight | Ex vivo measurement |
| Metastasis | Luciferase signal in distant organs |
| YARS2 knockdown | qRT-PCR of tumor tissue |
| Safety | Body weight, H&E of major organs |
| Ferroptosis markers | IHC for GPX4, 4-HNE |

---

## 6. Combination Therapy Opportunities

### 6.1 Rationale
From CRC study: YARS2 knockdown sensitizes to 5-FU via ROS accumulation
From ferroptosis literature: ROS + system Xc^- inhibition = synthetic lethality

### 6.1 Combination Partners
| Agent | Mechanism | Expected Synergy |
|-------|-----------|------------------|
| Erastin | System Xc^- inhibitor | Ferroptosis sensitization |
| Sulfasalazine | System Xc^- inhibitor (FDA-approved) | Repurposing opportunity |
| RSL3 | GPX4 inhibitor | Direct ferroptosis |
| Sorafenib | Multi-kinase + system Xc^- | Approved drug |
| **KDM4A inhibitor** | H3K9me3 → SLC7A11 ↓ | Ferroptosis priming |
| **DGAT1 inhibitor** | Lipid ROS amplification | Ferroptosis amplification |

### 6.2 Triple Combo Hypothesis
```
PF14-siYARS2  →  Mitochondrial translation inhibition  →  ROS ↑
          +
PF14-siKDM4A  →  SLC7A11 transcription ↓  →  cystine uptake ↓  →  ferroptosis ↑
          +
PF14-siDGAT1  →  Lipid ROS amplification  →  Ferroptosis execution ↑

= Maximum ferroptosis induction via 3 distinct mechanisms
```

---

## 7. Lung Epithelial Tropism Enhancement

### 7.1 PF14 vs Other Peptides
| Peptide | Target | Lung Specificity | Reference |
|---------|--------|------------------|-----------|
| **PF14** | Lung endothelium/epithelium | HIGH | Foged 2019 |
| **NF55** | Lung endothelium/epithelium | HIGH | Foged 2019 |
| **T7** | Lung epithelium (inhaled) | MODERATE | Ressel 2024 |
| **CG* | RAGE receptor | MODERATE | Cardiovascular |

### 7.2 Inhalation Formulation
For direct lung delivery (from Frontiers 2025 review):
- Nebulized PF14-siRNA complexes
- Particle size: 1-5 μm (alveolar deposition)
- Bypasses systemic delivery barriers
- Higher local concentration in lung tumor

---

## 8. Research Timeline

```
Month 1: Bioinformatic validation + siRNA sequence design
Month 2: In vitro knockdown optimization (N/P ratio, concentration)
Month 3: In vitro assay panel (proliferation, ROS, ferroptosis markers)
Month 4: In vivo pilot study (dose escalation)
Month 5: Full in vivo efficacy study
Month 6: Combination therapy validation
```

---

## 9. Key References

1. **Foged Lab PF14:** https://www.nature.com/articles/s41598-019-56455-2
2. **CRC YARS2 Study:** https://pmc.ncbi.nlm.nih.gov/articles/PMC9518999/
3. **Human Protein Atlas:** https://www.proteinatlas.org/ENSG00000139131-YARS2/cancer
4. **Lung siRNA Delivery Review:** Frontiers Oncology 2025 (10.3389/fonc.2025.1722906)
5. **CD44-targeting LNP:** ACS Nano 2025 (siRNA delivery enhancement)
6. **KRAS SL Tissue Specificity:** bioRxiv 10.64898/2026.04.30.721990 (Martin et al.)

---

## 10. Safety Considerations

### 10.1 Off-Target Risk
- YARS2 is essential in all tissues (mitochondrial translation)
- Systemic delivery with PF14 → lung enrichment but not exclusive
- **Mitigation:** Tumor-specific promoters / ligand-targeted delivery

### 10.2 N/P Ratio Toxicity
- N/P > 5: Aggregation, hemolysis, liver toxicity
- N/P 1-4: Well tolerated, no significant toxicity
- **CRITICAL:** Maintain N/P = 1-4 throughout all experiments

### 10.3 Clinical Translation Path
1. **IND-enabling studies:** GLP tox, biodistribution (pig model)
2. **Inhalation formulation:** Dry powder or nebulized solution
3. **Companion diagnostic:** YARS2 IHC for patient selection

---

## 11. Next Steps (Immediate Actions)

- [ ] Run GEPIA2 for YARS2 survival analysis in LUAD/LUSC
- [ ] Check CCLE for YARS2 mRNA in NSCLC cell lines
- [ ] Design 3 siRNA sequences (verify specificity with BLAST)
- [ ] Synthesize PF14 peptide (or purchase from manufacturer)
- [ ] Optimize PF14:siRNA complexation (gel retardation assay)
- [ ] Test knockdown efficiency in A549 cells
- [ ] Run full in vitro assay panel
- [ ] Design in vivo study protocol

---

**Document:** `arp-v24/YARS2_SIRNA_PF14_LUNG_TARGETING_2026.md`
**Created:** 2026-05-05
**Framework:** ARP v24 Anti-Aging/Cancer Research Pipeline
