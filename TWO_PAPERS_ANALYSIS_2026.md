# 두 논문 분석 보고서: 대사 질환과 심혈관 모델링
**Date:** 2026-05-10  
**Papers:** Nature Communications (s41467-026-72248-4), Circulation Research (T-World)

---

## Paper 1: Adipose Single Cell Epigenome/Transcriptome
**Citation:** Lee et al. 2026, Nature Communications, DOI: 10.1038/s41467-026-72248-4

### 핵심 발견

**연구 목적:**
비만이皮下지방조직(SAT)의 기능을 손상시켜 cardiometabolic disease(CMD)와 accelerated biological aging을 유발하는데, 이 استعداد를 결정하는 regulatory variants, target genes, epigenomic landscape를 규명

**주요 결과:**

| 발견 | 내용 |
|------|------|
| ** cis-eQTL 분석** | 279개 gene, 33개 cardiometabolic disease + aging trait |
| **Cell-type specificity** | 90%가 cell-type-specific, 그 중 55%가 adipocyte |
| **3D epigenome** | 81% colocalized variant가 active chromatin compartment에 mapping |
| **기존 연구와의 차이** | Bulk tissue colocalization studies에서 놓친 gene들 발견 |

### Methodology

1. **Single cell level cis-expression QTL (cis-eQTL) analysis**
2. **Colocalization 분석** with GWAS data
3. **Subcutaneous adipose tissue cell-type level epigenome analysis**

### 핵심 인사이트

```
비만 → 지방조직 기능 손상 → CMD risk + aging 가속
                    ↓
         Regulatory variants가 어떻게 작용?
                    ↓
    adipocyte에서 55% specific gene才发现
    (90% cell-type specific overall)
                    ↓
    3D chromatin (epigenome) = 질병 risk의 중심
```

### 우리 프로젝트와 연결

| 발견 | 적용 가능 분야 |
|------|---------------|
| **Adipocyte-specific genes** | DGAT1 (지방대사) — adipocyte에서 높게 발현 |
| **Cardiometabolic traits** | 심혈관 약물 개발 (SGLT2, GLP-1 등) |
| **Epigenomic regulation** | Aging/longevity 연구 (SIRT1, AMPK pathway) |
| **MASLD/NASH** | 지방간 질환과 직접 연결 |

---

## Paper 2: T-World Virtual Human Cardiomyocyte
**Citation:** Tomek et al. 2026, Circulation Research, DOI: 10.1161/CIRCRESAHA.125.328073

### 이미 분석 완료

T-World는 우리 cardio playbook에 이미 integration 완료:
- EADs, DADs, alternans, restitution simulation
- Sex-specific differences (female > male arrhythmia risk)
- Cardiotoxicity screening capability
- GitHub: https://github.com/jtmff/TWorld

### 추가 인사이트

**Sex Differences in Arrhythmia:**
```
Female cardiomyocytes:
├── Increased EAD susceptibility
├── Steeper APD restitution
└── Higher arrhythmia risk under drug-induced APD prolongation

Clinical implication: Sex-specific dosing may be needed for:
- hERG blockers (antiarrhythmics)
- Any drug prolonging QT interval
```

---

## 종합 분석: 두 논문의 연결

### 공통 주제: Precision Medicine

| Paper 1 (Adipose) | Paper 2 (Cardio) |
|-------------------|-----------------|
| Cell-type specific regulation | Cell-type specific modeling |
| Individual variability in disease risk | Individual variability in drug response |
| Epigenomic basis of disease | Mechanistic basis of arrhythmia |
| Aging acceleration | Sex differences in aging |

### drug discovery 시너지

**Paper 1 → Target Identification:**
- Adipocyte-specific regulatory genes
- Cardiometabolic disease genetic risk loci
- 3D chromatin structure as drug target

**Paper 2 → Safety Assessment:**
- Cardiotoxicity prediction before clinical trials
- Sex-specific risk assessment
- Patient-specific modeling (future)

### 우리 파이프라인 적용

```
ARP Orchestrator (BIORESEARCHER-style)
    │
    ├── discovery playbook → Paper 1 gene targets
    ├── admet playbook → Pharmacokinetics
    ├── cardio playbook → Paper 2 T-World simulation
    │
    ↓
Integration Flow:
Gene target (Paper 1)
    ↓
Compound design
    ↓
ADMET screening
    ↓
T-World cardiotoxicity (Paper 2)
    ↓
Clinical candidate
```

---

## 즉시 적용 가능 항목

### 1. DGAT1-LUNG Compounds Cardiotoxicity

DGAT1-LUNG-001~004의 cardiotoxicity를 T-World로 screening:
- hERG liability prediction
- APD prolongation risk
- Sex-specific risk (female higher)

### 2. Adipose Depot-Specific Targeting

Paper 1의 발견을 활용:
- **SAT (subcutaneous)** vs **VAT (visceral)** — drug delivery target
- Adipocyte-specific gene regulation
- obesity-induced aging mechanism

### 3. Combined Analysis for Cardiometabolic Drugs

MASLD/NASH drug development:
- Paper 1: Target identification (adipose dysfunction)
- Paper 2: Safety assessment (cardiovascular)

---

## 결론

두 논문은 모두 ** cell-type specificity**와 **individual variability**를 강조하며, 이것이 precision medicine의 핵심임.

우리 ARP pipeline:
1. **Paper 1** → Gene targets, adipocyte biology
2. **Paper 2** → Safety assessment, T-World integration

이 두 논문을 통합하면:
- 효과적인 cardiometabolic drug development
- cardiotoxicity early detection
- Sex-specific precision medicine approach

---

*Report generated: 2026-05-10 | ARP v24*
*Sources: Nature Communications (s41467-026-72248-4), Circulation Research (10.1161/CIRCRESAHA.125.328073)*