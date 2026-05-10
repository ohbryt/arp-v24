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

---

## 2. Target Product Profile

| Property | Target |
|----------|--------|
| **Modality** | Oral small molecule |
| **Selectivity** | Dual ACLY + ACSS2 inhibition |
| **Distribution** | Liver-biased (strong liver, limited muscle) |
| **Target engagement** | Glucose-derived + acetate-derived acetyl-CoA |
| **PD read-out** | Anti-fibrotic signature in HSCs |

**Exclusions:** Uric acid elevation, tendon toxicity, significant muscle exposure

---

## 3. Chemistry Strategy

### Development Lead
**EVT0185-like dual chemistry** — Primary development candidate

### Backup Series
| Backup | Scaffold | Rationale |
|--------|---------|-----------|
| Liver-activated ACLY-biased | Bempedoic acid | Known liver bias |
| ACSS2 inhibitor | AD-5584/AD-8007, MTB-9655 | Distinct scaffold |

---

## 4. Preclinical Assay Cascade

### Cellular Systems
| Cell Type | Use |
|-----------|-----|
| Primary human hepatocytes | DNL, acetyl-CoA |
| iPSC-hepatocytes | Disease modeling |
| Primary human HSCs | Fibrosis |
| LX-2 | Screen only |
| Multicellular co-cultures | Physiologic context |
| Precision-cut liver slices | Full tissue |

### Key Read-outs
**Metabolic:**
- Acetyl-CoA lowering (LC-MS)
- Histone acetylation (Western blot, ChIP)
- De novo lipogenesis (^14C-incorporation)
- Fibrogenic genes (qPCR: α-SMA, COL1A1, ACTA2)

**Fibrotic:**
- α-SMA (IHC/IF) — HSC activation
- COL1A1 (qPCR, ELISA) — Collagen
- Collagen secretion (ELISA)
- Stellate-cell contractility (gel contraction)

### Isotope Flux Studies
```
^13C-glucose → acetyl-CoA, palmitate, cholesterol (glucose-derived)
^13C-acetate → acetyl-CoA, palmitate, cholesterol (acetate-derived)
Deuterated water → DNL rate
```

---

## 5. In Vivo Package

### Models (Minimum 2 Orthogonal)
| Model | Read-outs |
|-------|-----------|
| Diet-induced F2/F3 | MRI-PDFF, insulin resistance, fibrosis staging |
| Fibrotic stress model | HSC biology stressed, severe fibrosis |

### Critical PK/PD Markers
| Marker | Endpoint |
|--------|----------|
| Liver:plasma ratio | Tissue selectivity |
| Hepatic acetyl-CoA | Target engagement |
| DNL flux | Lipogenesis |
| Stellate-cell activation | α-SMA, collagen |
| Histological fibrosis | Ishak score |

### Safety (Bempedoic Acid Class)
| Monitor | Frequency |
|--------|-----------|
| Uric acid | Baseline + periodic |
| Tendon findings | Exam |
| LDL/HDL/triglycerides | Fasting |
| ALT/AST/bilirubin | Hepatic injury |

---

## 6. Clinical Development Plan

### First Human Population
**F2-F3 non-cirrhotic MASH** (NOT F4)

### Patient Selection
| Step | Method |
|------|--------|
| Non-invasive enrichment | VCTE, MRE |
| Blood tests | ELF, PRO-C3 |
| Registration intent | Biopsy confirmation |

### Phase 1b/2a (12-16 weeks)
| Biomarker | Target |
|-----------|--------|
| MRI-PDFF | ≥30% decline (de-risking sign) |
| ALT/AST | Normalization |
| apoB/LDL-C | Change from baseline |
| Fibrosis biomarkers | PRO-C3, ELF improvement |

### Pivotal Study (48-52 weeks)
- Primary: MASH resolution + no fibrosis worsening OR ≥1-stage fibrosis improvement + no worsening of steatohepatitis

### Combination (after monotherapy PoM)
- **Semaglutide** — metabolic complement
- **Resmetirom** — THRβ complement

---

## 7. Go/No-Go Criteria

### Go (quantitative gates)
- [ ] >50% DNL flux inhibition (hepatocytes)
- [ ] >50% HSC collagen/α-SMA suppression
- [ ] Fibrosis improvement in 2 in vivo models
- [ ] No hypertriglyceridemia or hepatotoxicity

### No-Go
- ❌ Lipid lowering without anti-fibrotic signal
- ❌ Acetate bypass intact at tolerable doses
- ❌ Chronic safety worse than approved MASH benchmarks

---

## 8. Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Acetyl-CoA rerouting | Isotope tracing from start; select high-DNL F2/F3 |
| Chronic safety | Liver-biased exposure; sufficient dose, not maximal |
| Anti-fibrotic lag | HSC-focused assays; early combo with THRβ/GLP-1 |

---

## 9. Updated Portfolio

| Rank | Target | Indication | Status |
|------|--------|-----------|--------|
| 1 | **FSP1** | NSCLC (KEAP1/STK11) | First-in-class |
| 2 | **Dual ACLY/ACSS2** | MASH | First-in-class |
| 3 | DGAT1 + SLC7A11 | NSCLC | Triple ferroptosis |
| 4 | GLP-1/FXR | MASH | Dual agonist |

---

## 10. Modality Comparison

| Programme | Small Molecule | RNA | PROTAC | Biologic |
|-----------|:-------------:|:---:|:------:|:--------:|
| **NSCLC FSP1** | ✅ Primary | Secondary | Exploratory | ❌ Do not |
| **MASH ACLY/ACSS2** | ✅ Primary | Secondary | Exploratory | ❌ Do not |

**NSCLC FSP1 small molecule rationale:**
- Intracellular enzyme
- Systemic metastatic disease
- Rapid PD iteration needed
- iFSP1, icFSP1, viFSP1, FSEN1 chemotypes available

**MASH small molecule rationale:**
- Chronic oral therapy
- Dual-enzyme control
- EVT0185 lead, bempedoic acid precedent

---


## 11. Assay Cascade Summary

| Layer | NSCLC FSP1 | MASH ACLY/ACSS2 |
|-------|-----------|----------------|
| **Biochemistry** | Recombinant human/mouse FSP1, flavoprotein selectivity | Dual ACLY/ACSS2 enzymology, residence time |
| **Mechanistic cell PD** | BODIPY-C11, 4-HNE, CoQ/CoQH2 LC-MS, ferroptosis blocker rescue | Acetyl-CoA, H3K27ac/H3K9ac, ^13C-glucose/acetate flux |
| **Cell efficacy** | FSP1-high NSCLC panel, organoids | Hepatocytes, HSCs, co-culture |
| **Systems metabolism** | OCR/ECAR, isotope tracing | DNL tracer, glucose/acetate routing |
| **In vivo** | Orthotopic/syngeneic/PDX, RT+ICI combos | 2 MASH models, MRI-PDFF, fibrosis biomarkers |
| **PK/PD** | Tumor unbound, tumor:RBC, serial PD biopsy | Liver:plasma, liver acetyl-CoA suppression |
| **Safety** | Hematology, neuro, immune-cell fitness | Uric acid, tendon, lipids, DILI |

---


## 12. Timeline & Cost (Indicative)

### NSCLC FSP1
| Scenario | Timeline | Cost | Drivers |
|----------|----------|------|---------|
| Low | 30-33 months | $15-20M | Parallel chemistry, orthotopic models |
| Medium | 33-38 months | $20-28M | Immune-competent models, biopsy PD |
| High | 38-42 months | $28-35M | + Comprehensive translational pack |


### MASH ACLY/ACSS2
| Scenario | Timeline | Cost | Drivers |
|----------|----------|------|---------|
| Low | 27-31 months | $12-18M | Chronic tox, isotope flux |
| Medium | 30-36 months | $15-24M | + Precision-cut liver slices |
| High | 36-39 months | $24-28M | + Biomarker method development |


---


## 13. If Only One Programme

| Programme | Rationale |
|-----------|-----------|
| **MASH ACLY/ACSS2** | Safer bet: ACLY clinically validated (bempedoic acid) |
| **NSCLC FSP1** | Higher upside, higher variance |


---

## 14. Open Questions

| Programme | Main Question |
|-----------|---------------|
| **NSCLC FSP1** | How narrow is clinically responsive biomarker population? Monotherapy vs combo? |
| **MASH ACLY/ACSS2** | Anti-fibrotic effect in humans without tolerability penalty? |

**Backup concepts:**
- PDK4 → back-up MASH/insulin resistance concept
- Complex-I/Metformin → NSCLC comparator pathway

---

*Report generated: 2026-05-10 | ARP v24*