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

| Property | Target |
|----------|--------|
| **Modality** | Oral small molecule |
| **IC50 (human FSP1)** | Low-nanomolar |
| **Selectivity** | ≥30-fold over redox enzymes |
| **Tumor exposure** | Above IC90 (cell-based) |
| **PK/PD** | Tumor CoQ redox shift, lipid peroxidation |
| **Safety** | No RBC, neuronal, immune-cell liability |

**Exclusions:** GPX4 co-inhibition required, activity lost with lipoproteins, immune toxicity

---

## 3. Chemotypes (4 Parallel Tracks)

| Chemotype | Mechanism | Developability | Status |
|-----------|-----------|---------------|--------|
| **FSEN1-like** | Substrate-pocket binders | ⭐⭐⭐ Highest | Lead development |
| **viFSP1-like** | NAD(P)H-pocket binders | ⭐⭐ High | Lead development |
| **iFSP1-like** | First-gen on-target ligands | ⭐ Medium | Optimization |
| **icFSP1-like** | Condensate-forming | ⭐ Low | Mechanistic probe |

---

## 4. Assay Cascade

### Biochemical
| Assay | Purpose |
|-------|---------|
| Recombinant human/mouse FSP1 | IC50, species bridge |
| Orthogonal binding | Confirmation |
| Flavoprotein selectivity | Safety |

### Cellular (NSCLC Panel)
| Read-out | Method | Confirm |
|----------|--------|---------|
| Cell death rescue | Ferrostatin-1/liproxstatin | ✅ Ferroptosis |
| Lipid peroxidation | BODIPY-C11 | ✅ |
| CoQ redox shift | LC-MS | ✅ |

### In Vivo-Early (Bring In Earlier)
- 3D organoids
- Syngeneic orthotopic models
- KRAS-driven GEMM transplants

### Systems Metabolism
- ^13C-glucose → NADPH pathways
- ^13C-glutamine → lipid remodelling
- Oxidized phospholipid lipidomics

---

## 5. In Vivo Package (3 Tiers)

| Tier | Models | Read-outs |
|------|--------|-----------|
| 1: Fast efficacy | SubQ + orthotopic NSCLC | TGI, PD |
| 2: Immune combo | Immune-competent | + anti-PD-(L)1, dual ICB |
| 3: RT combo | KEAP1-inactive | + radiotherapy |

### PK/PD Markers
| Marker | Sample |
|--------|--------|
| Tumor unbound exposure | LC-MS |
| Tumor:RBC ratio | LC-MS |
| Tumor CoQ redox | LC-MS |
| 4-HNE | IHC |
| Plasma oxidative stress | ELISA |

### Safety
- Haematology, ophthalmology, neurobehaviour
- Cytokine release, immune-cell viability

---

## 6. Clinical Development Plan

### First Human Population
**Advanced LUAD after standard therapy, enriched by:**
- FSP1-high IHC
- KEAP1, STK11, or NFE2L2 alterations

### Dose Selection
**Project Optimus principles** (not classical MTD)

### Expansion Cohorts
| Cohort | Population |
|--------|------------|
| 1 | Refractory KEAP1/STK11-altered NSCLC (monotherapy) |
| 2 | KEAP1-inactive NSCLC + palliative radiotherapy |
| 3 | NSCLC + PD-(L)1 blockade (post safety) |

### On-Treatment Biopsy
**Mandatory** — prove ferroptosis engagement, not just target occupancy

---

## 7. Go/No-Go Criteria

### Go (ALL must be met)
- [ ] IC50: low-nanomolar (human FSP1)
- [ ] Selectivity: ≥30-fold over redox liabilities
- [ ] Cell killing rescued by ferroptosis blockers
- [ ] Robust tumor PD signal in vivo
- [ ] TGI >50% OR additivity with radio/immuno
- [ ] No >10% body-weight loss

### No-Go
- ❌ Requires exogenous GPX4 co-inhibition
- ❌ Activity lost with lipoproteins normalized
- ❌ Immune toxicity narrows combination window

---

## 8. Modality Comparison

| Modality | Decision | Rationale |
|----------|----------|-----------|
| **Small molecule** | ✅ Primary | Intracellular enzyme, systemic metastatic, rapid PD |
| RNA therapeutic | Secondary | Delivery harder to metastases |
| PROTAC | Exploratory | Localization, oral PK harder |
| Biologic | ❌ Do not | Poor fit for intracellular redox enzyme |

---

## 9. Timeline & Cost

| Scenario | Timeline | Cost | Main Drivers |
|----------|----------|------|-------------|
| Low | 30-33 months | $15-20M | Parallel chemistry, orthotopic models |
| Medium | 33-38 months | $20-28M | Immune-competent, biopsy PD |
| High | 38-42 months | $28-35M | + Translational pack |

**Main drivers:** Parallel series, orthotopic + immune models, biopsy-grade PD

---

## 10. Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Context-rich dependence | Concordant biomarkers: FSP1 IHC + KEAP1/STK11/NFE2L2 + biopsy PD |
| Chemistry failure | Parallel scaffolds + early cross-species |
| Normal-tissue toxicity | Intermittent dosing + monotherapy PD first |

---

## 11. Competitive Landscape

| Drug | Target | Status |
|------|--------|--------|
| FSEN1 | FSP1 | Preclinical + co-crystal |
| viFSP1 | FSP1 | Preclinical |
| iFSP1 | FSP1 | Preclinical |
| icFSP1 | FSP1 | Preclinical |
| Telaglenastat | GLS1 | Phase II |
| AZD3965 | MCT1 | Phase I |

**Gap:** No FSP1 in clinical trials → **First-in-class**

---

## 12. Portfolio

| Rank | Target | Indication | Status |
|------|--------|-----------|--------|
| 1 | **FSP1** | NSCLC | First-in-class |
| 2 | **Dual ACLY/ACSS2** | MASH | First-in-class |
| 3 | DGAT1 + SLC7A11 | NSCLC | Triple ferroptosis |
| 4 | GLP-1/FXR | MASH | Dual agonist |

---

## 13. Open Questions

| Question | Implication |
|----------|-------------|
| How narrow is responsive population? | Biomarker-driven |
| Monotherapy or combo first? | Signal-seeking strategy |
| PDK4/Complex-I | Backup concepts only |

---

*Report generated: 2026-05-10 | ARP v24*