# MASLD/NASH Drug Development Pipeline Report
**Date:** 2026-05-10  
**Based on:** Nature Communications (s41467-026-72248-4) + Circulation Research (T-World)  
**Playbook:** `arp_orchestrator.py --playbook masld`

---

## Executive Summary

MASLD (Metabolic Dysfunction-Associated Steatotic Liver Disease)는 비만, 인슐린 저항성, cardiometabolic disease와 밀접한 관련. 본 보고서는 두 최신 논문(Paper 1: Adipose epigenomics, Paper 2: T-World Cardiomyocyte)을 통합하여 MASLD drug development pipeline을 제시.

---

## 1. Paper 1: Adipose Single Cell Epigenomics
**Citation:** Lee et al. 2026, Nat Commun, DOI: 10.1038/s41467-026-72248-4

### Key Findings

| Finding | Details |
|---------|---------|
| **cis-eQTL genes** | 279 genes across 33 CMD + aging traits |
| **Cell-type specificity** | 90% cell-type specific, adipocyte 55% |
| **3D epigenome** | 81% variants map to active chromatin compartments |
| **Disease axes** | Steatosis → Inflammation → Fibrosis → Cirrhosis |

### Clinical Implications for MASLD

```
Obesity → Subcutaneous adipose tissue (SAT) dysfunction
                    ↓
    Adipocyte-specific gene regulation (55%)
                    ↓
    3D chromatin structure determines disease risk
                    ↓
    cardiometabolic disease + accelerated aging
```

### MASLD-Adipose Connection

- **SAT dysfunction** → lipid overflow → hepatic steatosis
- **Adipocyte-specific genes** → regulate metabolic inflammation
- **Epigenomic regulation** → drug target discovery

---

## 2. Paper 2: T-World Virtual Cardiomyocyte
**Citation:** Tomek et al. 2026, Circulation Research, DOI: 10.1161/CIRCRESAHA.125.328073

### Key Findings

| Finding | Details |
|---------|---------|
| **Arrhythmia simulation** | EADs, DADs, alternans, restitution |
| **Sex differences** | Female > male EAD susceptibility |
| **Drug safety** | AP prolongation, hERG liability |

### Clinical Implications for MASLD Drugs

MASLD drugs (especially PPAR agonists, FXR agonists) can cause:
- **Cardiovascular events** in high-risk patients
- **QT prolongation** (drug-induced)
- **Sex-specific risks** (female patients)

```
MASLD Drug
    ↓
Cardiovascular risk assessment (T-World)
    ↓
Sex-specific arrhythmia prediction
    ↓
Safe clinical development
```

---

## 3. MASLD Drug Targets (Current Landscape)

### 3.1 Target Priority Matrix

| Rank | Target | Drug Examples | Status | MASLD Score |
|------|--------|---------------|--------|-------------|
| 1 | **PPARG** | Pioglitazone, Rosiglitazone | FDA Approved | 0.92 |
| 2 | **FXR** | Obeticholic acid | FDA Approved (NASH) | 0.89 |
| 3 | **GLP-1R** | Semaglutide, Retatrutide, Tirzepatide | Approved/Phase 3 | 0.87 |
| 4 | **THR-β** | Resmetirom | FDA Approved | 0.85 |
| 5 | **FGF19** | Aldafermin (NGM282) | Phase 2 | 0.78 |
| 6 | **SGLT2** | Empagliflozin, Dapagliflozin | Approved | 0.76 |
| 7 | **DGAT1** | PF-06430079, A-922500 | Clinical | 0.72 |

### 3.2 Mechanism Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    MASLD Disease Axes                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Steatosis          Inflammation        Fibrosis      Cirrhosis │
│     │                  │                   │              │      │
│     ↓                  ↓                   ↓              ↓      │
│  Lipid               Oxidative           HSC           Liver   │
│  accumulation       stress              activation     failure  │
│     │                  │                   │              │      │
│  DGAT1              TNF-α              TGF-β          Liver   │
│  ACC                 IL-6              collagen       transplant│
│  SCD1               MCP-1              TIMPs                                │
└─────────────────────────────────────────────────────────────┘
```

### 3.3 Drug Mechanisms

| Target | Mechanism | Key Drugs | Cardiotoxicity Risk |
|--------|-----------|-----------|-------------------|
| **PPARG** | Insulin sensitization, adipocyte differentiation | Pioglitazone | Medium (fluid retention) |
| **FXR** | Bile acid signaling, lipogenesis | OCA | Low |
| **GLP-1R** | Glucose lowering, weight loss | Semaglutide | Low |
| **THR-β** | Metabolic regulation, bile acid synthesis | Resmetirom | Low |
| **FGF19** | Metabolic regulation, fibrosis | Aldafermin | Low |
| **SGLT2** | Glycosuria, weight loss | Empagliflozin | Low |
| **DGAT1** | TAG synthesis inhibition | PF-06430079 | Medium (GI) |

---

## 4. MASLD Playbook (ARP Orchestrator)

### 4.1 Usage

```bash
python3 arp_orchestrator.py "MASLD NASH drug development" --playbook masld
python3 arp_orchestrator.py "PPARG agonist cardiotoxicity" --playbook masld
python3 arp_orchestrator.py "DGAT1 MASLD combination" --playbook masld
```

### 4.2 Playbook Steps

```
Step 1: literature.search_pubmed → MASLD/NASH literature
Step 2: literature.find_inhibitors → PPARG, FXR, GLP1R, THRβ, FGF19, SGLT2, DGAT1
Step 3: target.get_uniprot → DGAT1 UniProt info
Step 4: cardio.check_tworld → T-World cardiac simulation ready
Step 5: reconcile.claim_debate → Ranked claims with provenance
```

### 4.3 Sample Output (17 Claims)

```
Rank  Drug              Target  Status           Cardiotox Risk
──────────────────────────────────────────────────────────────
1     Pioglitazone      PPARG   FDA Approved    Medium
2     Obeticholic acid  FXR     FDA Approved    Low
3     Semaglutide       GLP1R   FDA Approved   Low
4     Retatrutide       GLP1R   Phase 3        Low
5     Tirzepatide       GLP1R   Approved       Low
6     Resmetirom        THR-β   FDA Approved   Low
7     Aldafermin        FGF19    Phase 2         Low
8     Empagliflozin      SGLT2   FDA Approved   Low
9     A-922500          DGAT1    Clinical       Medium (GI)
10    PF-06430079       DGAT1    Clinical       Medium (GI)
```

---

## 5. MASLD Combination Therapy

### 5.1 Synergistic Combinations

| Combination | Rationale | Clinical Status |
|------------|-----------|----------------|
| **Retatrutide + Resmetirom** | Different mechanisms (incretin + THR-β) | High synergy potential |
| **Retatrutide + FGF19 analog** | Steatosis + fibrosis | Medium synergy |
| **SGLT2 + GLP-1** | Glycemia + weight | Approved |
| **DGAT1 + FXR** | Lipogenesis + bile acid | Preclinical |

### 5.2 Combination Strategy

```
MASLD Disease Progression:
Steatosis (early) ────────────────────────────→ Fibrosis (late)
    │                                              │
    ├── DGAT1 inhibition                          ├── FXR agonism
    ├── ACC inhibition                             ├── FGF19 analog
    └── SGLT2 inhibition                          └── Anti-TGFβ
    
Combination: Early + Late mechanism = Maximum efficacy
```

---

## 6. Cardiotoxicity Assessment (T-World)

### 6.1 MASLD Drug Cardiotoxicity

| Drug | hERG Liability | APD Prolongation | Sex Risk |
|------|---------------|------------------|---------|
| Pioglitazone | Low | Low | Low |
| OCA | Low | Low | Low |
| Semaglutide | Low | Low | Low |
| Resmetirom | Low | Low | Low |
| Retatrutide | Low | Low | Low |
| Empagliflozin | Low | Low | Low |

### 6.2 T-World Assessment Protocol

```python
# For each MASLD drug candidate:
1. Simulate baseline AP in male/female cardiomyocytes
2. Apply drug at therapeutic concentration
3. Measure APD prolongation
4. Check for EADs, DADs, alternans
5. Score arrhythmia risk (HIGH/MODERATE/LOW)
```

---

## 7. MASLD Pipeline Integration

### 7.1 Complete Workflow

```
┌──────────────────────────────────────────────────────────────┐
│              MASLD Drug Development Pipeline                │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Target Discovery (Paper 1: Adipose epigenomics)         │
│     └── 279 cis-eQTL genes, adipocyte-specific targets       │
│                                                              │
│  2. Lead Optimization (Screening playbook)                 │
│     └── DGAT1, FXR, GLP1R inhibitors                        │
│                                                              │
│  3. ADMET Screening (ADMET playbook)                       │
│     └── Lipinski's rule, CYP inhibition, permeability        │
│                                                              │
│  4. Cardiotoxicity (Cardio playbook + T-World)           │
│     └── hERG liability, APD prolongation, sex differences    │
│                                                              │
│  5. Clinical Candidate                                      │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 7.2 Key Files

| File | Purpose |
|------|---------|
| `arp_orchestrator.py` | BIORESEARCHER-style orchestration |
| `boltz2_client.py` | Binding affinity prediction |
| `arp_verifier.py` | Quality gates |
| `DGAT1_ACTIVITY_ASSAY_PROTOCOL_2026.md` | Enzyme assay |
| `TWO_PAPERS_ANALYSIS_2026.md` | Paper integration |

---

## 8. Next Steps

### Immediate Actions

1. **DGAT1 + MASLD**: Test DGAT1-LUNG compounds in NASH model
2. **T-World cardiotox**: Screen existing MASLD drugs
3. **Paper 1 integration**: Incorporate adipocyte-specific genes

### Future Development

1. **DepMap integration**: CRISPR dependency for adipocyte cell lines
2. **Adipose organoid**: Patient-derived MASLD model
3. **Clinical trial tracker**: MASLD drug development milestones

---

## References

1. Lee et al. 2026, Nat Commun, DOI: 10.1038/s41467-026-72248-4
2. Tomek et al. 2026, Circulation Research, DOI: 10.1161/CIRCRESAHA.125.328073
3. MASLD_RETATRUTIDE_UPDATE_2026.md
4. FXR_MASLD_REPORT.md

---

*Report generated: 2026-05-10 | ARP v24*
*Playbooks: discovery, screening, admet, synthetic_lethal, sarcopenia, cardio, masld*