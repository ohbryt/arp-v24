# Dual ACLY/ACSS2 Drug Development Plan: MASH
**Date:** 2026-05-10  
**Target:** Dual ACLY/ACSS2 (ATP Citrate Lyase / Acetyl-CoA Synthetase 2)  
**Indication:** MASH (Metabolic Dysfunction-Associated Steatohepatitis)  
**Priority:** #1 (Highest-confidence metabolic opportunity in MASH)

---

## Executive Summary

Dual ACLY/ACSS2 inhibition is the #1 priority for MASH because it attacks the acetyl-CoA economy linking steatosis to fibrosis — the exact node that current therapy underserves.

**Why dual over single:**
| Single Target | Bypass Mechanism | Dual Inhibitor |
|---------------|-----------------|----------------|
| ACLY only | ACSS2 → acetate → acetyl-CoA | **Blocks bypass** |
| ACSS2 only | ACLY → citrate → acetyl-CoA | **Blocks bypass** |

**Key Evidence:** EVT0185 (2026 Cell Metabolism) reduced steatosis, insulin resistance, and fibrosis in mouse MASH.

---

## 1. Target Biology

### 1.1 Acetyl-CoA Economy

```
Hepatocyte acetyl-CoA sources:
│
├── ACLY: citrate → acetyl-CoA (glucose-derived)
│
└── ACSS2: acetate → acetyl-CoA (dietary, gut microbiome)

Both sources feed:
├── De novo lipogenesis (DNL) → steatosis
├── HSC activation → fibrosis
└── Histone acetylation → gene regulation
```

### 1.2 Why This Node Is Underexploited

| Current MASH Drug | Mechanism | Gap |
|-------------------|-----------|-----|
| Resmetirom (THRβ) | Thyroid signaling | Steatosis only |
| Semaglutide (GLP-1) | Weight loss | Modest fibrosis |
| FGF21 analogs | Lipotoxicity | Injectable, not F4 |

**Dual ACLY/ACSS2 → addresses both steatosis AND fibrosis**

### 1.3 Connection to Our Work

| Our Target | ACLY/ACSS2 Connection |
|-----------|----------------------|
| **DGAT1** | DNL downstream → TAG synthesis |
| **FXR** | Bile acid, lipogenesis |
| **GLP-1R** | Metabolic correction |

---

## 2. Target Product Profile

### 2.1 Ideal Properties

| Property | Target |
|----------|--------|
| **Modality** | Oral small molecule |
| **Selectivity** | Dual ACLY + ACSS2 inhibition |
| **Distribution** | Liver-biased (strong liver, limited muscle) |
| **Target engagement** | Glucose-derived + acetate-derived acetyl-CoA |
| **PD read-out** | Anti-fibrotic signature in HSCs |

### 2.2 Exclusions (No-Go Criteria)

- ❌ Uric acid elevation (bempedoic acid class)
- ❌ Tendon toxicity
- ❌ Significant muscle exposure
- ❌ Insufficient anti-fibrotic signal

### 2.3 Bempedoic Acid Precedent

| Property | Evidence |
|----------|----------|
| **ACLY tractability** | FDA-approved for hyperlipidemia |
| **Liver-biased PK** | Liver-activated prodrug |
| **Safety database** | Established class safety |

---

## 3. Chemistry Strategy

### 3.1 Development Lead

**EVT0185-like dual chemistry**
- Primary development candidate
- Dual ACLY + ACSS2 inhibition in single molecule

### 3.2 Backup Series

| Backup | Scaffold | Rationale |
|--------|---------|-----------|
| **Liver-activated ACLY-biased** | Bempedoic acid | Known liver bias, ACLY-selective |
| **ACSS2 inhibitor** | AD-5584/AD-8007, MTB-9655 | Distinct ACSS2-selective |

**Backup rationale:** If exact 1:1 dual inhibition proves too narrow, backup scaffolds preserve optionality.

### 3.3 Modality Decision

| Modality | Decision | Reason |
|----------|----------|--------|
| **Small molecule** | ✅ Lead | Intracellular enzymes, chronic oral |
| Biologics | ❌ Poor fit | Not intracellular |
| RNA (GalNAc) | ❌ Partial | Misses HSC compartment |
| PROTACs | ❌ Backup only | Harder PK/manufacturability |

---

## 4. Preclinical Assay Cascade

### 4.1 Biochemical

```
1. Recombinant human ACLY enzymology (IC50)
2. Recombinant human ACSS2 enzymology (IC50)
3. Dual target-engagement assay
4. Selectivity panel (metabolic enzymes)
5. CYP inhibition, hERG liability
```

### 4.2 Cellular Systems

| Cell Type | Use |
|-----------|-----|
| **Primary human hepatocytes** | DNL, acetyl-CoA |
| **iPSC-hepatocytes** | Disease modeling |
| **Primary human HSCs** | Fibrosis |
| **LX-2** | Screen only (not primary) |
| **Multicellular co-cultures** | Physiologic context |
| **Precision-cut liver slices** | Full tissue architecture |

### 4.3 Key Read-outs

#### Metabolic (Acetyl-CoA Economy)
| Read-out | Method | Endpoint |
|----------|--------|----------|
| Acetyl-CoA lowering | LC-MS | Substrate flux |
| Histone acetylation | Western blot, ChIP | Epigenetic |
| De novo lipogenesis | ^14C-incorporation | Lipid synthesis |
| Fibrogenic genes | qPCR | α-SMA, COL1A1, ACTA2 |

#### Fibrotic
| Read-out | Method | Endpoint |
|----------|--------|----------|
| α-SMA | IHC/IF | HSC activation |
| COL1A1 | qPCR, ELISA | Collagen |
| ACTA2 | Flow cytometry | Myofibroblast |
| Collagen secretion | ELISA | Extracellular matrix |
| Stellate-cell contractility | Gel contraction | Functional readout |

### 4.4 Isotope Flux Studies

```
^13C-glucose → acetyl-CoA, palmitate, cholesterol (glucose-derived)
^13C-acetate → acetyl-CoA, palmitate, cholesterol (acetate-derived)
Deuterated water → DNL rate measurement
```

---

## 5. In Vivo Package

### 5.1 Models (Minimum 2 Orthogonal)

| Model | Read-outs |
|-------|-----------|
| **Diet-induced F2/F3** | MRI-PDFF, insulin resistance, fibrosis staging |
| **Fibrotic stress model** | HSC biology stressed, severe fibrosis |

### 5.2 Critical PK/PD Markers

| Marker | Sample | Endpoint |
|--------|--------|----------|
| **Liver:plasma ratio** | Liver + plasma | Tissue selectivity |
| **Hepatic acetyl-CoA** | Liver biopsy | Target engagement |
| **DNL flux** | Liver | Lipogenesis |
| **Stellate-cell activation** | IHC | α-SMA, collagen |
| **Histological fibrosis** | Trichrome/Masson | Ishak score |

### 5.3 Safety Package (Bempedoic Acid Class)

| Monitor | Frequency |
|--------|-----------|
| **Uric acid** | Baseline + periodic |
| **Tendon findings** | Ophthalmologic + tendon exam |
| **LDL/HDL/triglycerides** | Fasting lipids |
| **ALT/AST/bilirubin** | Hepatic injury |
| **Muscle enzymes** | CK, myoglobin |
| **Standard chronic toxicology** | 13-week + 26-week |

---

## 6. Clinical Development Plan

### 6.1 First Human Population

**MASH patients with F2-F3 fibrosis:**
- Biopsy-confirmed MASH
- NAS ≥4 with ≥1 point in each category
- Fibrosis stage F2-F3

### 6.2 Dose Selection

**Project Optimus principles:**
- Pharmacologically guided
- Not classical MTD
- Focus on optimal PD response

### 6.3 Biomarkers

| Biomarker | Use |
|-----------|-----|
| Liver fat (MRI-PDFF) | Early efficacy |
| Pro-C3 (N-terminal propeptide of type III collagen) | Fibrosis progression |
| ALT/AST | Hepatic injury |
| Fasting glucose/HbA1c | Metabolic effect |

### 6.4 Combination Potential

| Combination | Rationale |
|------------|----------|
| **+ Resmetirom** | Different mechanisms, additive |
| **+ Semaglutide** | Metabolic + metabolic |
| **+ FGF21 analog** | Broad effects |

---

## 7. Go/No-Go Criteria

### Go Criteria

- [ ] Dual IC50: low-nanomolar (human ACLY + ACSS2)
- [ ] Liver:plasma ratio >10:1
- [ ] Significant acetyl-CoA lowering in vivo
- [ ] Anti-fibrotic signal (α-SMA, collagen ↓)
- [ ] Histological fibrosis improvement ≥1 stage
- [ ] Acceptable safety (no uric acid/tendon issues)

### No-Go Criteria

- ❌ Significant muscle exposure
- ❌ Uric acid elevation requiring xanthine oxidase inhibition
- ❌ Tendon toxicity
- ❌ Single-mechanism bypass confirmed

---

## 8. Timeline & Cost (Estimate)

| Phase | Duration | Cost (USD) |
|-------|----------|------------|
| Lead discovery | 10-14 months | $6-12M |
| IND-enabling | 12-16 months | $8-16M |
| Phase I | 12-14 months | $10-18M |
| **Total to Phase I** | **30-39 months** | **$15-28M** |

---

## 9. Competitive Landscape

| Drug | Target | Company | Status |
|------|--------|---------|--------|
| **EVT0185** | Dual ACLY/ACSS2 | N/A | Preclinical (2026 data) |
| Bempedoic acid | ACLY | Esperion | Approved (LDL) |
| AD-5584/AD-8007 | ACSS2 | N/A | Preclinical |
| MTB-9655 | ACSS2 | N/A | Preclinical |
| Resmetirom | THRβ | Madrigal | FDA Approved |
| Semaglutide | GLP-1 | Novo Nordisk | FDA Approved |
| Lanifibranor | PPARα/δ/γ | Inventiva | Phase 3 |
| Pegozafermin | FGF21 | N/A | Phase 3 |
| Efruxifermin | FGF21 | N/A | Phase 3 |

**Gap:** No dual ACLY/ACSS2 in clinical trials → **First-in-class opportunity**

---

## 10. Connection to Our Pipeline

### 10.1 Playbook Integration

```bash
# Run MASLD playbook (updated with ACLY/ACSS2)
python3 arp_orchestrator.py "MASH ACLY ACSS2 dual inhibitor" --playbook masld
```

### 10.2 Our MASLD Playbook Targets

| Target | Included |
|--------|----------|
| **Dual ACLY/ACSS2** | NEW #1 priority |
| FXR | ✅ |
| GLP-1R | ✅ |
| THRβ | ✅ |
| FGF19 | ✅ |
| SGLT2 | ✅ |
| DGAT1 | ✅ |

### 10.3 MASH Combination Strategy

```
Early MASH (Steatosis):
├── Dual ACLY/ACSS2 (NEW)
├── DGAT1 inhibitor (our work)
└── SGLT2 inhibitor

Late MASH (Fibrosis):
├── FXR agonist
├── FGF19 analog
└── Anti-TGFβ
```

---

## 11. References

1. Cell Metabolism 2026: EVT0185 dual ACLY/ACSS2 in MASH
2. Cell Metabolism 2026: ACSS2 compensatory activation after ACLY inhibition
3. FDA: Bempedoic acid approval (ACLY tractability)
4. AD-5584/AD-8007, MTB-9655 chemical biology

---

## 12. Files

| File | Purpose |
|------|---------|
| `arp_orchestrator.py` | MASLD playbook |
| `MASLD_PIPELINE_REPORT_2026.md` | MASLD pipeline overview |
| `FSP1_DEVELOPMENT_PLAN_2026.md` | FSP1 (NSCLC) |
| `DGAT1_LUNG_COMPOUND_REPORT_2026.md` | Our NSCLC compounds |

---

*Report generated: 2026-05-10 | ARP v24*
*Targets: FSP1 (NSCLC), Dual ACLY/ACSS2 (MASH), DGAT1, GLP-1R*
*Playbooks: discovery, screening, admet, synthetic_lethal, sarcopenia, cardio, masld, fsp1*