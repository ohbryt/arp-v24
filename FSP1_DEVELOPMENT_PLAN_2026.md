# FSP1 Drug Development Plan: NSCLC Ferroptosis
**Date:** 2026-05-10  
**Target:** FSP1/AIFM2 (Ferroptosis Suppressor Protein 1)  
**Indication:** NSCLC (KEAP1/STK11/NFE2L2-altered lung adenocarcinoma)  
**Priority:** #1 (Highest-confidence metabolic opportunity in NSCLC)

---

## Executive Summary

FSP1 is the highest-confidence opportunity for metabolic drug discovery in NSCLC. It suppresses ferroptosis via CoQ reduction, is enriched in KEAP1/STK11-altered lung cancer, and has actionable chemical biology with multiple inhibitor chemotypes.

**Why FSP1 over alternatives:**
| Target | Issue | FSP1 Advantage |
|--------|-------|----------------|
| GPX4 | Direct inhibition → lethal | Indirect pathway, safer |
| PDK4 | Tumour-suppressive in NSCLC ❌ | Ferroptosis defense ✅ |
| Complex-I | Systemic toxicity ❌ | Tumour-selective ✅ |
| Glutamine | Metabolic plasticity ❌ | Defined axis ✅ |

---

## 1. Target Biology

### 1.1 FSP1 Mechanism

```
KEAP1 mutation/inactivation
        ↓
NRF2 activation (oxidative stress response)
        ↓
FSP1 upregulation
        ↓
CoQ → CoQH2 (CoQ reduction)
        ↓
Prevents lipid peroxidation
        ↓
Ferroptosis RESISTANCE
```

### 1.2 KEAP1/NRF2/FSP1 Axis

- **KEAP1 wild-type:** FSP1 suppressed under basal conditions
- **KEAP1 mutation:** NRF2 activation → FSP1 ↑ → ferroptosis protection
- **STK11/KEAP1 co-mutation:** Maximum FSP1 dependence

### 1.3 Connection to Our Work

| Our Target | FSP1 Connection |
|------------|----------------|
| **DGAT1** | Lipid droplet depletion → ferroptosis sensitization |
| **SLC7A11** | System Xc- → GSH → GPX4 pathway |
| **FSP1** | CoQ/FSP1 axis (alternative pathway) |

**Triple Ferroptosis Combo:**
```
DGAT1i (lipid droplets) + SLC7A11i (GSH) + FSP1i (CoQ)
= Maximum ferroptosis induction in NSCLC
```

---

## 2. Target Product Profile

### 2.1 Ideal Properties

| Property | Target |
|----------|--------|
| **Modality** | Oral small molecule |
| **IC50 (human FSP1)** | Low-nanomolar |
| **Selectivity** | ≥30-fold over redox enzymes |
| **Tumor exposure** | Above IC90 (cell-based) |
| **PK/PD** | Tumor CoQ redox shift, lipid peroxidation |
| **Safety** | No RBC, neuronal, immune-cell liability |

### 2.2 Exclusions (No-Go Criteria)

- ❌ Efficacy requiring exogenous GPX4 co-inhibition
- ❌ Activity lost when serum lipoproteins normalised
- ❌ Immune-cell toxicity narrowing combination window

---

## 3. Chemotypes (4 Parallel Tracks)

### 3.1 Inhibitor Classes

| Chemotype | Mechanism | Developability | Status |
|-----------|-----------|---------------|--------|
| **FSEN1-like** | Substrate-pocket binders | ⭐⭐⭐ Highest | Lead development |
| **viFSP1-like** | NAD(P)H-pocket binders | ⭐⭐ High | Lead development |
| **iFSP1-like** | First-gen on-target ligands | ⭐ Medium | Optimization |
| **icFSP1-like** | Condensate-forming | ⭐ Low | Mechanistic probe |

### 3.2 Recommended Priority

**FSEN1/viFSP1-like chemistry** = most developable:
- Standard medicinal chemistry optimization
- Species bridging (human + rodent)
- PK/PD modelling tractable

---

## 4. Assay Cascade

### 4.1 Biochemical

```
1. Recombinant human FSP1 enzymology (IC50)
2. Recombinant mouse FSP1 (species bridging)
3. Orthogonal binding assay
4. Selectivity panel: flavoproteins, redox enzymes
5. CYP inhibition, hERG liability
```

### 4.2 Cellular (NSCLC Panel)

**Genotype-annotated panel:**
- KEAP1-altered
- STK11-altered
- NFE2L2-altered
- EGFR-mutant
- re-genotype in-house before use

**Three essential read-outs:**
| Read-out | Method | Ferrotopsis Confirm |
|----------|--------|-------------------|
| Cell death rescue | Ferrostatin-1 or liproxstatin rescue | ✅ |
| Lipid peroxidation | BODIPY-C11 signal | ✅ |
| CoQ redox shift | LC-MS (CoQ10/CoQ10H2) | ✅ |

### 4.3 In Vivo-Early Models

Bring in earlier than usual (stronger in vivo dependence):
- 3D organoids
- Co-culture systems
- Syngeneic orthotopic models
- KRAS-driven GEMM-derived transplants

### 4.4 Stable Isotope Studies

```
^13C-glucose tracing → NADPH-generating pathways
^13C-glutamine tracing → Lipid remodelling
Oxidized phospholipid lipidomics (not Seahorse alone)
```

---

## 5. In Vivo Package (3 Tiers)

### Tier 1: Fast Efficacy
- Subcutaneous NSCLC models
- Orthotopic NSCLC models
- FSP1-high/KEAP1-STK11-altered biology

### Tier 2: Immune-Combination
- Immune-competent models
- Anti-PD-(L)1 combination
- Dual ICB combination

### Tier 3: Radiotherapy Combination
- KEAP1-inactive + radiotherapy
- CoQ-FSP1 axis for radiation resistance

### PK/PD Markers
| Marker | Sample | Read-out |
|--------|--------|----------|
| Tumor unbound exposure | Tumor | LC-MS |
| Tumor:RBC ratio | Blood | LC-MS |
| Tumor CoQ redox state | Tumor | LC-MS |
| 4-HNE immunostaining | Tumor | IHC |
| Plasma oxidative stress | Plasma | ELISA |

### Safety Package
- Haematology (CBC)
- Ophthalmology (fundoscopy)
- Neurobehaviour ( Irwin test)
- Cytokine release (ELISA)
- Immune-cell viability (flow cytometry)

---

## 6. Clinical Development Plan

### 6.1 First Human Population

**Advanced LUAD after standard therapy, enriched by:**
- FSP1-high IHC
- KEAP1, STK11, or NFE2L2 alterations

### 6.2 Dose Selection

**Project Optimus principles** (not classical MTD):
- Dose optimization over dose maximization
- Pharmacologically guided endocrinology

### 6.3 Expansion Cohorts

| Cohort | Population | Regimen |
|--------|------------|---------|
| 1 | Refractory KEAP1/STK11-altered NSCLC | FSP1i monotherapy |
| 2 | KEAP1-inactive NSCLC | FSP1i + palliative radiotherapy |
| 3 | NSCLC (post monotherapy safety) | FSP1i + PD-(L)1 blockade |

### 6.4 On-Treatment Biopsy

**Mandatory** — success depends on proving ferroptosis engagement, not just target occupancy.

---

## 7. Go/No-Go Criteria

### Go Criteria (ALL must be met)

- [ ] Enzyme IC50: low-nanomolar range (human FSP1)
- [ ] Biochemical selectivity: ≥30-fold over redox liabilities
- [ ] Cell killing rescued by ferroptosis blockers (FSP1-high NSCLC)
- [ ] Robust tumor PD signal in vivo
- [ ] Monotherapy TGI >50% OR compelling additivity with radio/immuno
- [ ] No >10% body-weight loss

### No-Go Criteria

- ❌ Efficacy depends only on exogenous GPX4 co-inhibition
- ❌ Activity disappears when serum lipoproteins normalized
- ❌ Immune-cell toxicity narrows combination window

---

## 8. Timeline & Cost (Estimate)

| Phase | Duration | Cost (USD) |
|-------|----------|------------|
| Lead discovery | 12-18 months | $8-15M |
| IND-enabling | 12-18 months | $10-20M |
| Phase I | 12-18 months | $15-25M |
| **Total to Phase I** | **33-42 months** | **$18-35M** |

---

## 9. Competitive Landscape

| Drug | Target | Company | Status |
|------|--------|---------|--------|
| iFSP1 | FSP1 | Academic | Preclinical |
| icFSP1 | FSP1 | Academic | Preclinical |
| viFSP1 | FSP1 | Academic | Preclinical |
| FSEN1 | FSP1 | Academic | Preclinical + co-crystal |
| Telaglenastat | GLS1 | Calithera | Phase II (NSCLC) |
| DRP-104 | GLS1 | Drill | Phase I/II |
| AZD3965 | MCT1 | AstraZeneca | Phase I |

**Gap:** No FSP1 inhibitor in clinical trials → First-in-class opportunity

---

## 10. Connection to Our Pipeline

### 10.1 Playbook Integration

```bash
# Run FSP1 playbook
python3 arp_orchestrator.py "FSP1 NSCLC ferroptosis" --playbook fsp1
```

### 10.2 Triple Ferroptosis Combination

```
┌──────────────────────────────────────────────────────────────┐
│              Triple Ferroptosis Induction (NSCLC)            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  DGAT1i (our DGAT1-LUNG series)                            │
│  └── Lipid droplet depletion → PUFA accumulation            │
│                                                              │
│  SLC7A11i (our work)                                        │
│  └── GSH depletion → GPX4 dysfunction                      │
│                                                              │
│  FSP1i (NEW: this plan)                                     │
│  └── CoQ rescue blockade → Lipid peroxidation               │
│                                                              │
│  = Maximum ferroptosis without normal cell toxicity         │
└──────────────────────────────────────────────────────────────┘
```

### 10.3 MASLD/FSP1 Synergy

| Indication | Target | Combination |
|-----------|--------|-------------|
| NSCLC | FSP1i | + Radiotherapy/Immunotherapy |
| MASLD | ACLY/ACSS2i | + Resmetirom/GLP-1 |

---

## 11. Key References

1. Nature 2025: FSP1 genetic/pharmacological disruption in lung tumors
2. Nature Communications: KEAP1-NRF2-CoQ-FSP1 axis, radiation resistance
3. FSEN1 co-crystal structure
4. iFSP1, icFSP1, viFSP1 chemical biology

---

## 12. Files

| File | Purpose |
|------|---------|
| `arp_orchestrator.py` | FSP1 playbook added |
| `FSP1_DEVELOPMENT_PLAN_2026.md` | This document |
| `DGAT1_LUNG_COMPOUND_REPORT_2026.md` | Our NSCLC compounds |
| `TWO_PAPERS_ANALYSIS_2026.md` | Paper 1 + Paper 2 |

---

*Report generated: 2026-05-10 | ARP v24*
*Playbooks: discovery, screening, admet, synthetic_lethal, sarcopenia, cardio, masld, fsp1*