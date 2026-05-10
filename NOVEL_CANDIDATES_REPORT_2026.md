# Novel Drug Candidates: Research + Business Report
**Date:** 2026-05-10  
**Based on:** FSP1 (NSCLC) + Dual ACLY/ACSS2 (MASH) Development Plans  
**Strategy:** First-in-class metabolic drugs in high-unmet-need indications

---

## Executive Summary

두 개의 혁신적 약물 후보를 제시합니다:

| Candidate | Indication | Target | Modality | Timeline | Cost | Status |
|-----------|-----------|--------|----------|----------|------|--------|
| **FSP1 Inhibitor** | NSCLC (KEAP1/STK11-altered) | Ferroptosis defense | Oral small molecule | 33-42 months | $18-35M | First-in-class |
| **Dual ACLY/ACSS2** | MASH | Acetyl-CoA economy | Oral small molecule | 30-39 months | $15-28M | First-in-class |

**Investment thesis:** Both address areas where current therapy underserves patients, both have strong preclinical validation, and both use oral small molecules with clear development paths.

---

## 1. Portfolio Overview

### 1.1 Priority Matrix

| Rank | Candidate | Indication | Unmet Need | Competitive Edge |
|------|-----------|-----------|------------|-----------------|
| **1** | **FSP1 Inhibitor** | NSCLC | No metabolism-directed drug approved | First-in-class ferroptosis |
| **2** | **Dual ACLY/ACSS2** | MASH | F4/cirrhosis untreatable | Dual bypass blockade |

### 1.2 Why These Two?

**NSCLC (FSP1):**
- No metabolic drug approved for NSCLC despite heavy research
- FSP1 has strong lung-specific validation (Nature 2025)
- Multiple chemotypes available (FSEN1, viFSP1, iFSP1, icFSP1)
- Biomarker-driven patient selection (FSP1 IHC + KEAP1/STK11 genotype)

**MASH (ACLY/ACSS2):**
- Approved drugs (resmetirom, semaglutide) only for F2-F3, not F4
- Dual inhibition blocks metabolic bypass (ACLY ↔ ACSS2)
- ACLY already clinically validated (bempedoic acid)
- Addresses both steatosis AND fibrosis

---

## 2. NSCLC: FSP1 Inhibitor

### 2.1 The Problem

| Current NSCLC Treatment | Gap |
|------------------------|-----|
| Kinase inhibitors (EGFR, ALK, ROS1) | Resistance, not all mutations |
| Chemo-immunotherapy | Limited efficacy, toxicity |
| ADCs | Not for all patients |
| **Metabolism-directed drugs** | **NONE APPROVED** |

### 2.2 FSP1 Biology

```
KEAP1 mutation
    ↓
NRF2 activation
    ↓
FSP1 upregulation
    ↓
CoQ → CoQH2 (anti-ferroptotic)
    ↓
Lipid peroxidation prevention
    ↓
Tumor survival
```

**Key insight:** KEAP1/STK11-altered NSCLC depends on FSP1 for ferroptosis defense. FSP1 inhibition = selective tumor killing.

### 2.3 Triple Ferroptosis Combo (Our Pipeline)

```
DGAT1i (our work)
    └── Lipid droplet depletion
    
SLC7A11i (our work)
    └── GSH depletion → GPX4 dysfunction
    
FSP1i (this plan)
    └── CoQ rescue blockade
    
= Maximum ferroptosis induction
```

### 2.4 Target Product Profile

| Property | Target |
|----------|--------|
| IC50 | Low-nanomolar (human FSP1) |
| Selectivity | ≥30-fold over redox enzymes |
| PK | Tumor > IC90, tumor:RBC > 1 |
| Safety | No RBC, neuronal, immune toxicity |
| PD marker | Lipid peroxidation (BODIPY-C11), CoQ redox |

### 2.5 Chemotypes

| Chemotype | Advantage | Development |
|-----------|-----------|-------------|
| **FSEN1-like** | Substrate pocket, co-crystal | ⭐ Lead |
| **viFSP1-like** | Species-independent NAD(P)H | ⭐ Lead |
| iFSP1-like | First generation | Optimization |
| icFSP1-like | Phase separation | Probe only |

### 2.6 Clinical Development

**Population:** Advanced LUAD after standard therapy
- FSP1-high IHC
- KEAP1, STK11, or NFE2L2 alterations

**Cohorts:**
1. KEAP1/STK11-altered NSCLC (monotherapy)
2. KEAP1-inactive + radiotherapy
3. + PD-(L)1 blockade (after safety)

---

## 3. MASH: Dual ACLY/ACSS2 Inhibitor

### 3.1 The Problem

| Approved Drug | Limitation |
|---------------|------------|
| Resmetirom (FDA 2024) | Not for F4/cirrhosis |
| Semaglutide (FDA 2025) | Modest fibrosis effect |
| FGF21 analogs | Injectable, not for F4 |

**Unmet needs:** Cirrhosis (F4), fibrosis reversal, durable enrichment

### 3.2 Acetyl-CoA Economy

```
Hepatocyte acetyl-CoA sources:
│
├── ACLY: citrate → acetyl-CoA (glucose-derived)
│
└── ACSS2: acetate → acetyl-CoA (dietary, microbiome)

Both sources feed:
├── De novo lipogenesis → steatosis
├── HSC activation → fibrosis
└── Histone acetylation → gene regulation
```

### 3.3 Why Dual Over Single?

| Single Target | Bypass | Dual Inhibitor |
|---------------|--------|----------------|
| ACLY only | ACSS2 → acetate → acetyl-CoA | **Blocks bypass** |
| ACSS2 only | ACLY → citrate → acetyl-CoA | **Blocks bypass** |

### 3.4 Target Product Profile

| Property | Target |
|----------|--------|
| Modality | Oral small molecule |
| Selectivity | Dual ACLY + ACSS2 |
| Distribution | Liver-biased (low muscle) |
| PK | Liver:plasma >10:1 |
| Safety | No uric acid/tendon issues |

### 3.5 Clinical Development

**Population:** F2-F3 non-cirrhotic MASH (NOT F4)

**Phase 1b/2a (12-16 weeks):**
| Biomarker | Target |
|-----------|--------|
| MRI-PDFF | ≥30% decline |
| ALT/AST | Normalization |
| Fibrosis markers | PRO-C3, ELF improvement |

**Pivotal (48-52 weeks):**
- Primary: MASH resolution + no fibrosis worsening OR ≥1-stage fibrosis improvement

---

## 4. Research Plan

### 4.1 Assay Cascade

#### NSCLC FSP1
| Layer | Assay | Read-out |
|-------|-------|----------|
| Biochemistry | Recombinant human/mouse FSP1 | IC50, selectivity |
| Cell PD | BODIPY-C11, CoQ LC-MS | Ferroptosis markers |
| Efficacy | FSP1-high NSCLC panel, organoids | Viability |
| Metabolism | ^13C-glucose, ^13C-glutamine | Lipid remodelling |
| In vivo | Orthotopic, syngeneic, PDX | TGI, PD |
| PK/PD | Tumor:RBC, 4-HNE | Exposure/response |
| Safety | Neuro, immune-cell viability | Oxidative stress |

#### MASH ACLY/ACSS2
| Layer | Assay | Read-out |
|-------|-------|----------|
| Biochemistry | Dual ACLY/ACSS2 enzymology | IC50, residence time |
| Cell PD | Acetyl-CoA, ^13C flux | DNL suppression |
| Efficacy | Hepatocytes, HSCs, co-culture | Collagen, contractility |
| Metabolism | ^13C-glucose/acetate | Palmitate, cholesterol |
| In vivo | 2 MASH models | MRI-PDFF, fibrosis |
| PK/PD | Liver:plasma, acetyl-CoA | Target engagement |
| Safety | Uric acid, tendon, lipids | Bempedoic acid class |

### 4.2 Go/No-Go Criteria

#### NSCLC FSP1
**Go:**
- [ ] IC50 <100nM (human FSP1)
- [ ] Selectivity >30-fold
- [ ] Cell killing rescued by ferroptosis blockers
- [ ] TGI >50% OR combo additivity
- [ ] No >10% body-weight loss

**No-Go:**
- ❌ Requires GPX4 co-inhibition
- ❌ Activity lost with lipoproteins
- ❌ Immune toxicity

#### MASH ACLY/ACSS2
**Go:**
- [ ] >50% DNL flux inhibition
- [ ] >50% HSC collagen/α-SMA suppression
- [ ] Fibrosis improvement in 2 models
- [ ] No hypertriglyceridemia/hepatotoxicity

**No-Go:**
- ❌ Lipid lowering without anti-fibrotic
- ❌ Acetate bypass intact
- ❌ Safety worse than approved MASH drugs

---

## 5. Timeline & Budget

### 5.1 NSCLC FSP1

| Phase | Duration | Cost |
|-------|----------|------|
| Lead discovery | 12-18 months | $8-15M |
| IND-enabling | 12-18 months | $10-20M |
| Phase I | 12-18 months | $15-25M |
| **Total** | **33-42 months** | **$18-35M** |

### 5.2 MASH ACLY/ACSS2

| Phase | Duration | Cost |
|-------|----------|------|
| Lead discovery | 10-14 months | $6-12M |
| IND-enabling | 12-16 months | $8-16M |
| Phase I | 12-14 months | $10-18M |
| **Total** | **30-39 months** | **$15-28M** |

### 5.3 Parallel Execution

Both programs can run in parallel:
- **NSCLC FSP1:** Heavier PD-enabling translational work early
- **MASH ACLY/ACSS2:** Heavier chronic safety + biomarker work

### 5.4 If Only One Program

| Choice | Rationale |
|--------|-----------|
| **MASH** | Safer bet: ACLY clinically validated (bempedoic acid precedent) |
| **NSCLC FSP1** | Higher upside, higher variance |

---

## 6. Business Case

### 6.1 Market Opportunity

| Indication | Market Size | Growth Driver |
|-----------|-------------|---------------|
| NSCLC | $40B+ by 2030 | New targets, combinations |
| MASH | $35B+ by 2030 | Approved therapies, F4 gap |

### 6.2 Competitive Position

| Program | Advantage | Risk |
|---------|-----------|------|
| FSP1 | First-in-class, no approved metabolism drug in NSCLC | Biomarker population size |
| ACLY/ACSS2 | Dual blockade, addresses both steatosis + fibrosis | Chronic tolerability |

### 6.3 IP Strategy

| Program | Protection |
|---------|-----------|
| FSP1 | New chemical entities, biomarkers (FSP1 IHC + genotype) |
| ACLY/ACSS2 | Dual inhibitors, fixed-dose combinations |

### 6.4 Partnership Potential

| Stage | Partnership Type |
|-------|-----------------|
| Lead optimization | Co-development with pharma |
| IND-enabling | Licensing or acquisition |
| Phase II | Regional partnerships |

---

## 7. Risk Mitigation

### 7.1 NSCLC FSP1

| Risk | Mitigation |
|------|------------|
| Narrow population | Concordant biomarkers (FSP1 IHC + KEAP1/STK11) |
| Chemistry failure | Parallel scaffolds (FSEN1, viFSP1, iFSP1) |
| Toxicity | Intermittent dosing, monotherapy PD first |

### 7.2 MASH ACLY/ACSS2

| Risk | Mitigation |
|------|------------|
| Bypass rerouting | Isotope tracing from start |
| Chronic safety | Liver-biased exposure, sufficient dose |
| Fibrosis lag | HSC-focused assays, early combo planning |

---

## 8. Integration with Our Pipeline

### 8.1 ARP Orchestrator Playbooks

```bash
# Available playbooks
python3 arp_orchestrator.py "FSP1 NSCLC" --playbook fsp1
python3 arp_orchestrator.py "MASH ACLY ACSS2" --playbook masld
```

### 8.2 Complete Portfolio

| Rank | Target | Indication | Source |
|------|--------|-----------|--------|
| 1 | **FSP1** | NSCLC | This report |
| 2 | **Dual ACLY/ACSS2** | MASH | This report |
| 3 | DGAT1 + SLC7A11 | NSCLC | Existing work |
| 4 | GLP-1/FXR | MASH | Existing work |
| 5 | DGAT1-LUNG-003 | NSCLC | Synthesized |

### 8.3 Triple Ferroptosis Combo (NSCLC)

```
DGAT1i + SLC7A11i + FSP1i
= Maximum ferroptosis without normal cell toxicity
```

### 8.4 MASH Combination Strategy

```
Early (Steatosis): ACLY/ACSS2 dual + DGAT1i
Late (Fibrosis): FXR agonist + FGF19 analog + Anti-TGFβ
```

---

## 9. Immediate Actions

### 9.1 NSCLC FSP1
1. Literature search for FSEN1/viFSP1 lead compounds
2. Establish KEAP1/STK11-altered NSCLC panel
3. Set up BODIPY-C11 and CoQ redox assays
4. Plan orthotopic/syngeneic models

### 9.2 MASH ACLY/ACSS2
1. Literature search for EVT0185 and backup scaffolds
2. Establish primary hepatocyte and HSC assays
3. Set up ^13C-glucose/acetate flux studies
4. Plan MASH mouse models (2 orthogonal)

---

## 10. Files

| File | Content |
|------|---------|
| `NOVEL_CANDIDATES_REPORT_2026.md` | This document |
| `FSP1_DEVELOPMENT_PLAN_2026.md` | NSCLC detailed plan |
| `ACLY_ACSS2_DEVELOPMENT_PLAN_2026.md` | MASH detailed plan |
| `arp_orchestrator.py` | 8 playbooks |
| `DGAT1_LUNG_COMPOUND_REPORT_2026.md` | Our NSCLC compounds |

---

## 11. Conclusion

두 후보 모두 **first-in-class** 기전으로, 현재 치료법이 만족시키지 못하는 환자에게 새로운 치료 옵션을 제공합니다.

**NSCLC FSP1:** KEAP1/STK11-altered lung cancer에서 ferroptosis를 유도하는 혁신적 접근

**MASH ACLY/ACSS2:** Steatosis와 fibrosis를 동시에 해결하는 dual blockade

두 프로그램을 병행하면:
- Risk diversification (두 개의 독립적 적응증)
- 플랫폼 활용 ( Assay cascade 공통점)
- 파트너십 기회 확대

---

*Report generated: 2026-05-10 | ARP v24*  
*GitHub: github.com/ohbryt/arp-v24 (yars2-sirna-pf14-2026 branch)*