# 췌장암 (Pancreatic Ductal Adenocarcinoma, PDAC) 약물 발굴 분석

**ARP v24 Pipeline - Cancer Disease Pack Expansion**  
**Date:** 2026-04-18  
**Status:** Comprehensive Target Analysis & Drug Discovery Ready

---

## Executive Summary

| 항목 | 내용 |
|------|------|
| **5-Year Survival** | 12% (최악의 주요 암종) |
| **2026 New Cases (US)** | ~66,000명 |
| **KRAS mutation** | 90% 이상 (G12D 41%, G12V 30%, G12R 15%) |
| **KRAS G12D Inhibitor** | MRTX1133 (Ph I/II 진행 중) |
| **Key Challenge** | Desmoplasia (ström 용적의 90%) + 면역억제 종양미세환경 |
| **Emerging Strategy** | Multi-antigen vaccines, CAR-T, KRAS combos |

---

## 1. PDAC 분자 아형 (Molecular Subtypes)

### 1.1 Classical (Progenitor) vs Basal-like (Squamous) - GATA6/HMGA2

| 아형 | 마커 | 특징 | 예후 | 표적 접근 |
|------|------|------|------|----------|
| **Classical** | GATA6+ | Differentiated, metabolic, pancreatic enzyme | **Better** | KRAS 억제 시 GATA6+ 선택적 |
| **Basal-like** | HMGA2+, TP63+ | Squamous, EMT, stemness, aggressive | Worse | immunotherapy 우선 |

**Reference:** Science Translational Medicine (2026) - panKRASi selects for classical-like (GATA6+) phenotype

```python
# GATA6: KRAS inhibitor response marker
classical_markers = ["GATA6", "KRT19", "KRT7", "CPA2", "ANXA4"]
basal_markers = ["HMGA2", "TP63", "S100A2", "KRT5", "KRT6A"]
```

### 1.2 PDAC 드라이버 유전자

| 유전자 | 변이 빈도 | 기능 | 표적 가능성 |
|--------|-----------|------|-------------|
| **KRAS** | 90-95% | oncogenic driver | ✅ MRTX1133 (G12D), RMC-6236 (pan-G12X) |
| **TP53** | ~70% | tumor suppressor | ❌ Difficult - intracellular |
| **SMAD4** | ~55% | TGF-β pathway | ❌ Loss of function |
| **CDKN2A** | ~95% | cell cycle | ❌ Loss of function |
| **BRCA1/2** | ~5-7% | DNA repair | ✅ PARP 억제제 (germline) |
| **RNF43** | ~10% | Wnt pathway | Investigational |

---

## 2. 핵심 표적 분석 (Priority Targets)

### 2.1 KRAS G12D - #1 Driver Target

**Why #1:** 41% of PDAC have G12D mutation - highest frequency KRAS variant

| 속성 | 내용 |
|------|------|
| **Protein** | KRAS G12D (Gly12Asp) |
| **Mutation** | G>A at codon 12, Asp instead of Gly |
| **Frequency** | 41% of PDAC, also in CRC, NSCLC |
| **Selectivity** | MRTX1133: ~1000x selectivity vs WT |
| **Mechanism** | Binds GDP-bound KRAS G12D, inhibits nucleotide exchange |
| **Clinical** | MRTX1133 Ph I/II (NCT05737706) |
| **Efficacy** | Disease control rate 87%, median PFS 8.1 months (RMC-6236) |

**MRTX1133 Key Facts:**
- Reversible KRAS G12D inhibitor
- Unlike G12C (covalent with cysteine), G12D lacks reactive cysteine → reversible design
- Phase I/II trial for G12D-mutated solid tumors
- 2026: Scientific Reports paper on liver metastasis model

**Pipeline:** MRTX1133 → RMC-6236 (pan-KRAS G12X inhibitor)

```python
kras_g12d_target = {
    "gene": "KRAS",
    "mutation": "G12D",
    "protein": "KRAS G12D",
    "frequency_in_pdpac": 0.41,
    "inhibitor": "MRTX1133",
    "clinical_trial": "NCT05737706",
    "efficacy": {
        "disease_control_rate": 0.87,
        "median_pfs_months": 8.1
    },
    "combination_potential": ["PI3K", "BRD4", "MEK", "CDK4/6"]
}
```

### 2.2 CLDN18.2 - #2 CAR-T Target

**Why #2:** Surface protein on cancer cells, minimal normal tissue expression, clinical CAR-T success

| 속성 | 내용 |
|------|------|
| **Protein** | Claudin 18 isoform 2 (CLDN18.2) |
| **Normal tissue** | Limited - gastric mucosa tight junctions only |
| **Cancer expression** | 40-60% of PDAC, also gastric/esophageal |
| **Therapy** | CAR-T (CT041, AZD6422) |
| **Efficacy** | Complete remission in PDAC patient (case report) |
| **Clinical** | Phase Ib trial (NCT04404595) |

**Clinical Data:**
- 2 metastatic PDAC patients treated with anti-CLDN18.2 CAR-T
- Both showed tumor control (1 partial response, 1 complete response)
- CRS (cytokine release syndrome) managed with tocilizumab
- TGF-β1 reduction observed → immune modulation

```python
cldn182_target = {
    "gene": "CLDN18",
    "isoform": "CLDN18.2",
    "expression_pdpc": "40-60%",
    "therapy": "CAR-T (CT041, AZD6422)",
    "trial": "NCT04404595",
    "efficacy": {
        "response_rate": "2/2 patients",
        "complete_remission": True,
        "tgf_beta_reduction": True
    },
    "key_issue": "On-target/off-tumor toxicity (gastric)"
}
```

### 2.3 FAP (Fibroblast Activation Protein) - #1 Stromal Target

**Why #3:** Desmoplasia is the major barrier - 90% of tumor mass is stroma

| 속성 | 내용 |
|------|------|
| **Protein** | Fibroblast Activation Protein (FAP) |
| **Expression** | Activated fibroblasts (CAFs), not normal |
| **Function** | ECM degradation, immunosuppression |
| **Therapy** | CAR-T, small molecule inhibitors, antibodies |
| **Challenge** | FAP+ fibroblasts can be tumor-suppressive |
| **Strategy** | Reprogram CAFs, not ablate |

**CAF (Cancer-Associated Fibroblast) Targets:**
```python
caf_targets = {
    "FAP": {
        "role": "ECM remodeling, immunosuppression",
        "strategy": "CAR-T, small molecules",
        "note": "Don't ablate - reprogram"
    },
    "CXCL12": {
        "role": "T cell exclusion",
        "strategy": "CXCR4 antagonists"
    },
    "IL-6": {
        "role": "Inflammation, resistance",
        "strategy": "Tocilizumab (IL-6R)"
    }
}
```

### 2.4 TGF-β - Fibrosis & Immunosuppression Hub

**Why #4:** Central to desmoplasia and immune evasion

| 속성 | 내용 |
|------|------|
| **Pathway** | TGF-β → Smad2/3 → Fibrosis + Immune suppression |
| **PDAC connection** | TGF-β high in PDAC stroma, promotes EMT |
| **Therapeutic** | TGF-β inhibitors, SMAD4 restoration |
| **Challenge** | TGF-β is tumor-suppressive in early stage |
| **Strategy** | Combination with immunotherapy |

```python
tgfb_target = {
    "pathway": "TGF-beta/SMAD",
    "role": [" fibrosis", "EMT", "immunosuppression"],
    "biomarker": "pSMAD2/3 nuclear localization",
    "combination": ["KRAS inhibitor", "Immunotherapy"],
    "challenge": "Dual role: tumor suppression vs promotion"
}
```

---

## 3. PDAC 치료 전략 매트릭스

### 3.1 Direct Tumor Cell Targeting

| 표적 | 치료법 | 임상 단계 | 우선순위 |
|------|--------|----------|----------|
| **KRAS G12D** | MRTX1133 (小分子) | Ph I/II | ⭐⭐⭐⭐⭐ |
| **KRAS G12X (pan)** | RMC-6236 | Ph I | ⭐⭐⭐⭐ |
| **CLDN18.2** | CT041 CAR-T | Ph Ib | ⭐⭐⭐⭐ |
| **KRAS vaccine** | 6-mutant pooled peptide | Ph I | ⭐⭐⭐ |
| **EGFR** | Erlotinib (approved) | Approved | ⭐⭐ |
| **MEK** | Trametinib + KRAS combo | Preclinical | ⭐⭐⭐ |
| **PI3K** | Pictilisib + MRTX1133 | Preclinical | ⭐⭐⭐ |

### 3.2 Stromal/Immune Modulation

| 표적 | 치료법 | 임상 단계 | 우선순위 |
|------|--------|----------|----------|
| **FAP** | CAR-T, antibodies | Preclinical | ⭐⭐⭐⭐ |
| **CXCL12/CXCR4** | AMD3100, BL-8040 | Ph II | ⭐⭐⭐ |
| **IL-6/IL-6R** | Tocilizumab | Repurposed | ⭐⭐⭐ |
| **TGF-β** | Fresolumab, LY3200882 | Ph II | ⭐⭐⭐ |
| **PD-1/PD-L1** | Pembrolizumab | Approved (MSI-H) | ⭐⭐⭐ |
| **CD40** | Selicrelumab + chemo | Ph I | ⭐⭐ |

### 3.3 DNA Repair / Synthetic Lethality

| 표적 | 치료법 | 환자 선택 | 우선순위 |
|------|--------|----------|----------|
| **BRCA1/2** | Olaparib (approved) | Germline BRCA | ⭐⭐⭐⭐ |
| **PARP** | Rucaparib, Niraparib | HRD+ | ⭐⭐⭐ |
| **ATM** | AZD0156 | Preclinical | ⭐⭐ |
| **CHK1/2** | Prexasertib | Preclinical | ⭐⭐ |

---

## 4. MRTX1133 + 조합 전략

### 4.1 MRTX1133 Resistance Mechanisms

| 저항 기전 | 빈도 |克服 전략 |
|-----------|------|----------|
| **RTK activation (HER2, MET)** | Common | RTK combination |
| **PI3K/AKT activation** | Common | PI3K inhibitor |
| **KRAS amplification** | Rare | Dose escalation |
| **Histological transformation** | Observed | Basal-like → Classical 전환 |

### 4.2 Optimal Combinations

| Combination | Rationale | Stage | Priority |
|-------------|-----------|-------|----------|
| **MRTX1133 + PI3K/BRD4** | Overcome resistance, reduce desmoplasia | Preclinical (2025) | ⭐⭐⭐⭐⭐ |
| **MRTX1133 + MEK** | Dual MAPK suppression | Ph I | ⭐⭐⭐⭐ |
| **MRTX1133 + CD40** | Immune activation | Preclinical | ⭐⭐⭐⭐ |
| **MRTX1133 + PD-1** | Checkpoint unblock | Preclinical | ⭐⭐⭐⭐ |
| **MRTX1133 + IL-6R** | Reduce inflammation | Rationale | ⭐⭐⭐ |

**Key Paper:** "Dual Inhibition of KRAS G12D and PI3K/BRD4 signaling overcomes therapeutic resistance in pancreatic cancer" (ScienceDirect, Dec 2025)
- MDP5: Novel BRD4 + PI3K dual inhibitor
- MRTX1133 + MDP5: Synergistic in vivo

---

## 5. 천연화합물 PDAC 접근

### 5.1 PDAC의 천연화합물 표적

| 천연화합물 | 표적 | 기전 | Evidence |
|-----------|------|------|----------|
| **Berberine** | KRAS, PI3K, AMPK | KRAS signaling ↓, AMPK ↑ | Preclinical |
| **Curcumin** | NF-κB, STAT3, COX-2 | Inflammation ↓, apoptosis ↑ | Preclinical |
| **Resveratrol** | SIRT1, p53 | Tumor suppression ↑ | Preclinical |
| **Quercetin** | PI3K/AKT, mTOR | Autophagy ↑, Growth ↓ | Preclinical |
| **Genistein** | EGFR, HER2 | RTK signaling ↓ | Phase I |
| **Epigallocatechin gallate (EGCG)** | EGFR, PI3K | Proliferation ↓ | Preclinical |

### 5.2 PDAC 천연화합물 조합 설계

```python
pdac_natural_combo = {
    "name": "PDAC-Protect-NX",
    "anchor": {
        "compound": "Berberine",
        "dose": "500-1500mg/day",
        "mechanism": ["KRAS signaling ↓", "AMPK ↑", "PI3K/AKT ↓"],
        "bioavailability": "5% - needs enhancement"
    },
    "synergists": [
        {
            "compound": "EGCG (Epigallocatechin gallate)",
            "dose": "400-800mg/day",
            "mechanism": ["EGFR ↓", "PI3K ↓", "ROS ↓"]
        },
        {
            "compound": "Curcumin",
            "dose": "500-1000mg/day",
            "mechanism": ["NF-κB ↓", "STAT3 ↓", "COX-2 ↓"],
            "bioavailability": "15% - needs piperine"
        },
        {
            "compound": "Quercetin",
            "dose": "500-1000mg/day",
            "mechanism": ["PI3K/AKT ↓", "Autophagy ↑", "Immune modulation"]
        }
    ],
    "enhancement": {
        "berberine": "Nicotinamide cocrystal",
        "curcumin": "Piperine 5mg"
    },
    "expected_benefits": [
        "KRAS pathway suppression (adjuvant to MRTX1133)",
        "Reduced desmoplasia",
        "Immune modulation",
        "Chemoprevention"
    ]
}
```

---

## 6. CAR-T & Immunotherapy 접근

### 6.1 PDAC CAR-T 현황

| 표적 | CAR-T | 임상 | 반응률 | 주요 이슈 |
|------|-------|------|--------|----------|
| **CLDN18.2** | CT041 | Ph Ib | **CR in PDAC** | On-target/off-tumor |
| **CLDN18.2** | AZD6422 | Preclinical | Promising | Armored CAR |
| **Mesothelin** | Several | Ph I/II | Limited | On-target/off-tumor |
| **HER2** | Various | Ph I | Partial | Limited |
| **MUC1** | Various | Preclinical | - | Early |
| **FAP** | Various | Preclinical | - | Stromal targeting |

### 6.2 CAR-T + Stromal Combination

```
CAR-T (CLDN18.2) + Stromal Reprogramming
         │
         ├─ FAP targeting (CAFs) → T cell penetration ↑
         ├─ CXCR4 antagonist → T cell recruitment ↑
         └─ TGF-β inhibitor → Immune activation ↑

Rationale: Desmoplasia is #1 barrier to CAR-T in PDAC
```

---

## 7. 표적 조합 매트릭스

### 7.1 PDAC Multi-Target Strategy

```
                    ┌─────────────────────────────────────┐
                    │         PDAC MULTI-TARGET          │
                    └─────────────────────────────────────┘
                                      │
          ┌────────────────────────────┼────────────────────────────┐
          │                            │                            │
          ▼                            ▼                            ▼
   ┌─────────────┐            ┌──────────────┐              ┌─────────────┐
   │  TUMOR CELL │            │    STROMA    │              │ IMMUNE TME  │
   └─────────────┘            └──────────────┘              └─────────────┘
          │                            │                            │
   KRAS G12D (MRTX1133)        FAP (CAR-T/inhib)          PD-1/PD-L1
   CLDN18.2 (CAR-T)            CXCL12/CXCR4                 CD40 agonist
   EGFR (Erlotinib)            IL-6 (Tocilizumab)           TGF-β inhibitor
   PI3K (combination)          ECM remodeling              IL-2/IL-15
```

### 7.2 Novel Target Ranking

| 순위 | 표적 | 카테고리 | 점수 | 근거 |
|------|------|----------|------|------|
| **1** | KRAS G12D | Oncogenic driver | 9.5/10 | 41% PDAC, MRTX1133 임상 |
| **2** | CLDN18.2 | CAR-T target | 8.5/10 | CR 보고, Ph Ib 진행 |
| **3** | FAP | Stromal | 8.0/10 | Desmoplasia 해결 |
| **4** | PI3K/BRD4 | Resistance | 8.0/10 | MRTX1133 조합增效 |
| **5** | TGF-β | Fibrosis hub | 7.5/10 | Desmoplasia 핵심 |
| **6** | IL-6/IL-6R | Inflammation | 7.5/10 | CRS 관리, 면역조절 |
| **7** | CXCR4 | Metastasis | 7.0/10 | T cell recruitment |
| **8** | BRCA/PARP | DNA repair | 7.0/10 | 5-7% 환자, approved |
| **9** | GATA6 | Subtype marker | 6.5/10 | Classical PDAC predictor |
| **10** | MEK | KRAS pathway | 6.5/10 | Combination therapy |

---

## 8. 임상 개발 로드맵

### 8.1 PDAC 치료 라인별 접근

| 라인 | 현재 표준치료 | 혁신적 접근 |
|------|--------------|-------------|
| **1차** | Gemcitabine + Nab-paclitaxel | + MRTX1133 (G12D+) / + KRAS vaccine |
| **2차** | FOLFIRINOX | + Immunotherapy / + CAR-T |
| **BRCA+** | Platinum + Olaparib | PARP 억제제 유지 |
| **G12D+** | Targeted | MRTX1133 ± PI3K/BRD4 |
| ** refractory** | Trial | Multi-antigen vaccine + CPI |

### 8.2 Phase I/II Trial Candidates

| 표적 조합 | 치료제 | 예상 환자 |imeline |
|-----------|--------|----------|---------|
| KRAS G12D + PI3K | MRTX1133 + Gedatolisib | G12D+ PDAC | 2026-2027 |
| Multi-KRAS vaccine + CPI | 6-mutant KRAS + Nivo/Ipi | Resected PDAC | Ph I 완료 |
| CLDN18.2 CAR-T + CXCR4 | CT041 + AMD3100 | CLDN18.2+ PDAC | 2026 |
| FAP CAR-T + KRAS | Anti-FAP + MRTX1133 | All PDAC | Preclinical |

---

## 9. ARP Pipeline 적용

### 9.1 PDAC Disease Pack용 표적

```python
pdac_targets = {
    # Oncogenic drivers
    "KRAS_G12D": {
        "gene": "KRAS",
        "mutation": "G12D",
        "frequency": 0.41,
        "druggability": "small_molecule",
        "drug": "MRTX1133",
        "pipeline": "Mirati/BeiGene",
        "score": 9.5
    },
    "KRAS_G12X": {
        "gene": "KRAS",
        "mutation": "G12V, G12R, etc.",
        "frequency": 0.45,
        "druggability": "small_molecule",
        "drug": "RMC-6236",
        "pipeline": "Revolution Medicines",
        "score": 8.5
    },
    
    # CAR-T targets
    "CLDN18.2": {
        "gene": "CLDN18",
        "isoform": "CLDN18.2",
        "frequency": 0.50,
        "druggability": "CAR-T",
        "drug": "CT041",
        "pipeline": "Coherent Bioscience",
        "score": 8.5
    },
    
    # Stromal
    "FAP": {
        "gene": "FAP",
        "frequency": 0.90,  # CAFs
        "druggability": "CAR-T/antibody",
        "challenge": "CAF reprogram vs ablate",
        "score": 8.0
    },
    "TGFB1": {
        "gene": "TGFB1",
        "frequency": "high in TME",
        "druggability": "small_molecule/antibody",
        "drug": "Fresolumab",
        "score": 7.5
    }
}
```

### 9.2 DIAMOND DeepClust 적용

```python
# PDAC specific protein families
pdac_protein_families = {
    "KRAS_family": {
        "members": ["HRAS", "KRAS", "NRAS"],
        "significance": "Oncogenic signaling hubs",
        "cluster_size": "~15,000"
    },
    "Claudin_family": {
        "members": ["CLDN1", "CLDN3", "CLDN4", "CLDN18", "CLDN18.2"],
        "significance": "Tight junction proteins, CAR-T targets"
    },
    "FAP_family": {
        "members": ["FAP", "DPP4"],
        "significance": "Fibroblast activation, stromal targeting"
    }
}
```

---

## 10. 결론 및 권고

### 10.1 핵심 인사이트

1. **KRAS G12D가 PDAC 치료의 핵심**
   - 41% 빈도, MRTX1133 임상 진행 중
   - 2026년 RMC-6236 (pan-KRAS G12X) Ph I data乐观

2. **Desmoplasia 해결이 관건**
   - 섬유증 조직이 약물 침투 차단
   - FAP, TGF-β, IL-6 동시 표적화 필요

3. **CAR-T는 CLDN18.2에서 성공 사례**
   - Complete remission 보고
   - Stromal combination 필수

4. **천연화합물은 보조적 역할**
   - KRAS pathway 억제 보조
   - Chemoprevention 가능
   - 생체이용률 문제 해결 필요

### 10.2 ARP Pipeline 우선순위

| 우선순위 | 활동 | 예상 결과 |
|----------|------|-----------|
| **P0** | KRAS G12D 가상 스크리닝 | 후보 화합물 10-20개 |
| **P1** | MRTX1133 조합 전략 분석 | 최적 조합 确定 |
| **P2** | 천연화합물 PDAC 활성 예측 | Berberine, EGCG 등 |
| **P3** | CLDN18.2 CAR-T 설계 지원 | 결합 친화성 예측 |

### 10.3 Shortcut to Value

```
Immediate (Today):
└── Generate PDAC target list (this analysis)
    └── Update cancer disease pack with PDAC subtypes

This Week:
└── Run virtual screening for KRAS G12D candidates
└── Analyze MRTX1133 analog space

This Month:
└── Validate top 5 candidates with ADMET
└── Design combination strategies
```

---

## References

1. Buchfink et al. (2026). DIAMOND DeepClust. Nat Methods. doi:10.1038/s41592-026-03030-z
2. Science Translational Medicine (2026). panKRASi selects classical-like phenotype. doi:10.1126/scitranslmed.adt5511
3. NCI Cancer Currents (2023). MRTX1133 Targets KRAS G12D. 
4. Scientific Reports (2026). Antimetastatic effects of MRTX1133. doi:10.1038/s41598-025-34204-y
5. JCI (2025). KRAS: Achilles' heel of pancreas cancer. doi:10.1172/JCI191939
6. Cancer Biology & Medicine (2025). Drugging KRAS in pancreatic cancer.
7. PMC12528555 (2025). Emerging therapeutic advancements in pancreatic cancer.
8. Clinical Cancer Research (2024). AZD6422 CAR-T preclinical.
9. Advanced Healthcare Materials (2025). CLDN18.2 CAR-sEVs.
10. Frontiers in Oncology (2024). KRAS G12D targeted therapies.
11. Journal of Hematology & Oncology (2023). CT041 CAR T cell therapy.
12. ScienceDirect (2025). Dual Inhibition of KRAS G12D and PI3K/BRD4.

---

**Document Version:** 1.0  
**Created:** 2026-04-18  
**Author:** ARP v24 Pipeline