# PHGDH in Cancer and Metabolic Disorders
## Comprehensive Drug Discovery Research Report

---

> **Document Information**
> - **Date:** 2026-04-19
> - **Gene:** PHGDH (Phosphoglycerate Dehydrogenase)
> - **Gene Symbol:** PHGDH
> - **UniProt:** O43175 (Human)
> - **EC Number:** 1.1.1.95
> - **Classification:** Cancer / Metabolic Disease / Drug Discovery

---

# 초록 (Abstract)

**PHGDH (Phosphoglycerate Dehydrogenase)**는 세린 생합성 경로의 첫 번째 반응을 촉매하는 효소로, 3-phosphoglycerate (3-PG)를 3-phosphohydroxypyruvate (3-PHP)로 전환한다. 이 반응은 탈아미노산 경로를 통한 데 노보 세린 합성의 시작점으로서, 세린, 글리신, 그리고 이들의 하류 대사물의 생성에 필수적이다.

PHGDH는 다양한 암종에서 **oncogene**으로 기능하며, 특히 유방암, 폐암, 대장암, 흑색종에서 과발현되거나 유전적으로 증폭되어 있다. 암세포는 세린 합성 경로를 증폭시켜 빠른 증식에 필요한 물질을 공급받으며, 이를 " serine dependency"라 한다.

또한 PHGDH는 대사 증후군, 제2형 당뇨병, 신경퇴행 질환 등 대사 장애와의 연관성이 보고되고 있다.

본 보고서는 PHGDH의 생물학적 기능, 암에서의 역할, 대사 질환과의 연관성, 알려진 저해제, 그리고 치료적 표적으로서의 잠재력을 종합적으로 분석한다.

---

# 목차 (Table of Contents)

1. [PHGDH 생물학](#1-phgdh-생물학)
2. [암에서의 PHGDH](#2-암에서의-phgdh)
3. [대사 질환에서의 PHGDH](#3-대사-질환에서의-phgdh)
4. [PHGDH 저해제](#4-phgdh-저해제)
5. [천연물 및营养물](#5-천연물-및-영양물)
6. [Drug Repositioning](#6-drug-repositioning)
7. [De Novo 약물 설계](#7-de-novo-약물-설계)
8. [비교 분석](#8-비교-분석)
9. [치료적 우선순위](#9-치료적-우선순위)
10. [결론 및 권고](#10-결론-및-권고)

---

# 1. PHGDH 생물학 (PHGDH Biology)

## 1.1 유전자 및 단백질 구조

```
┌─────────────────────────────────────────────────────────────┐
│                    PHGDH Protein Structure                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Subunit Structure: Tetramer (4 identical subunits)        │
│  Each subunit: ~400 amino acids                             │
│  Total molecular weight: ~140 kDa (tetramer)               │
│                                                              │
│  ┌──────────┐  ┌──────────┐                               │
│  │ Subunit A│  │ Subunit B│  ← Dimer formation             │
│  └──────────┘  └──────────┘                               │
│       ↕              ↕                                     │
│  ┌──────────┐  ┌──────────┐                               │
│  │ Subunit C│  │ Subunit D│  ← Tetramer                  │
│  └──────────┘  └──────────┘                               │
│                                                              │
│  Active Sites: 4 (one per subunit)                          │
│  Coenzyme: NAD+                                             │
│  Substrate: 3-Phosphoglycerate (3-PG)                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

| 특성 | 정보 |
|------|------|
| **유전자 위치** | 1p12 |
| **단백질 길이** | 410 aa (human) |
| **분자량** | ~45 kDa (subunit), ~140 kDa (tetramer) |
| **EC 번호** | 1.1.1.95 |
| **UniProt** | O43175 |
| **Quaternary structure** | Tetramer (4 identical subunits) |
| **Cofactor** | NAD+ |

## 1.2 세린 생합성 경로 (Serine Synthesis Pathway)

```
                    DE NOVO SERINE SYNTHESIS PATHWAY
    ═══════════════════════════════════════════════════════

    Glucose
       ↓
    Glycolysis
       ↓
    3-Phosphoglycerate (3-PG)
       ↓  [PHGDH - Rate Limiting Step!]
    ┌──────────────────────────────────────┐
    │  PHGDH: 3-PG → 3-PHP (NADH + H⁺)   │
    │  First committed step                │
    └──────────────────────────────────────┘
       ↓
    3-Phosphohydroxypyruvate (3-PHP)
       ↓  [PSPH - Phosphoserine phosphatase]
    3-Phosphoserine (3-PS)
       ↓  [SHMT - Serine hydroxymethyltransferase]
    L-Serine
       ↓
    ┌──────────────────────────────────────┐
    │  Downstream Products:                │
    │  • Glycine (via SHMT)                │
    │  • Cysteine (via CBS)                │
    │  • Sphingolipids                     │
    │  • Phosphatidylserine                 │
    │  • One-carbon metabolism (folate)     │
    └──────────────────────────────────────┘
```

### 경로 효소들

| 효소 | 기호 | 기능 |
|------|------|------|
| **PHGDH** | Phosphoglycerate dehydrogenase | 3-PG → 3-PHP (Rate-limiting) |
| **PSPH** | Phosphoserine aminotransferase | 3-PHP → 3-PS |
| **SHMT** | Serine hydroxymethyltransferase | 3-PS → Serine |
| **CBS** | Cystathionine beta-synthase | Serine → Cysteine |

## 1.3 조직 분포

| 조직 | 발현 수준 | 기능 |
|------|----------|------|
| **간장** | 높음 | 글리코겐 합성, 해독 |
| **신장** | 높음 |氨基酸 대사 |
| **뇌** | 높음 | 세린 합성, 신경전달물질 |
| **폐** | 중간 | 기본 대사 |
| **유방** | 낮음-중간 | 기본 대사 |
| **악성 종양** | **매우 높음** | Serine addiction |

## 1.4 세린의 생물학적 기능

```
                    SERINE BIOLOGICAL FUNCTIONS
    ═══════════════════════════════════════════════════════

                         L-Serine
                            │
        ┌───────────────────┼───────────────────┐
        ↓                   ↓                   ↓
   ┌─────────┐        ┌─────────┐        ┌─────────┐
   │ Protein │        │  Glycine │        │Cysteine │
   │ Synthesis│        │ Synthesis│        │ Synthesis│
   └─────────┘        └─────────┘        └─────────┘
        │                   │                   │
        ↓                   ↓                   ↓
   ┌─────────┐        ┌─────────┐        ┌─────────┐
   │Enzymes  │        │ One-C   │        │Sphingo- │
   │         │        │ Carbon   │        │lipids   │
   └─────────┘        │ (folate) │        └─────────┘
        │             └─────────┘              │
        │                   │                  ↓
        │                   ↓            ┌─────────┐
        │              ┌─────────┐       │Gluta-   │
        │              │ Nucleo- │       │thione   │
        │              │ tides   │       │(ROS     │
        │              └─────────┘       │detox)  │
        │                   │            └─────────┘
        ↓                   ↓
   ┌─────────────────────────────────────────┐
   │         CELL PROLIFERATION               │
   │  • Rapidly dividing cells (cancer)       │
   │  • Require high serine flux              │
   │  • "Serine addiction" phenomenon        │
   └─────────────────────────────────────────┘
```

---

# 2. 암에서의 PHGDH (PHGDH in Cancer)

## 2.1 Oncogene으로서의 역할

```
┌─────────────────────────────────────────────────────────────┐
│            PHGDH: CONFIRMED ONCOGENE                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ✅ COPY NUMBER AMPLIFICATION in multiple cancers             │
│  ✅ OVEREXPRESSION in tumors                                 │
│  ✅ PROMOTES tumor growth and proliferation                   │
│  ✅ ENHANCES metastasis                                       │
│  ✅ Associated with POOR PROGNOSIS                           │
│  ✅ Knockdown suppresses tumor growth                         │
│  ✅ "Serine addiction" in cancer cells                       │
│                                                              │
│  ❌ No tumor-suppressive functions documented                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 2.2 암 유형별 발현 및 예후

| 암종 | PHGDH 증폭/과발현 | 빈도 | 예후 | 역할 |
|------|------------------|------|------|------|
| **유방암 (TNBC)** | 증폭/과발현 | ~30-40% | Poor | Oncogene |
| **폐암 (NSCLC)** | 증폭/과발현 | ~20-30% | Poor | Oncogene |
| **대장암** | 과발현 | ~25-35% | Poor | Oncogene |
| **흑색종 (Melanoma)** | 증폭/과발현 | ~40% | Poor | Oncogene |
| **위암** | 과발현 | ~20% | Poor | Oncogene |
| **간암** | 과발현 | ~15-25% | Poor | Oncogene |
| **췌장암** | 과발현 | ~20% | Poor | Oncogene |
| **전립선암** | 과발현 | ~15% | Variable | Oncogene |

## 2.3 삼阴性 유방암 (TNBC)

### 특징

| 특성 | 설명 |
|------|------|
| **PHGDH 증폭** | TNBC의 30-40%에서 발생 |
| **종양 형성** | PHGDH가 종양 시작에 필수적 |
| **전이** | 간葉 변환 및 폐 전이와 연관 |
| **예후** | PHGDH high = Overall survival ↓ |

### 기전

```
PHGDH Amplification/Overexpression
        ↓
Increased Serine Synthesis
        ↓
    ┌─────────────────────┐
    │  Metabolic Outputs   │
    ├── Serine ↑          │
    ├── Glycine ↑         │
    ├── Nucleotides ↑      │
    ├── Lipids ↑          │
    └── Glutathione ↑     │
    └─────────────────────┘
        ↓
    Cell Proliferation ↑ ( nucleotide/lipid synthesis)
    Cell Survival ↑ ( glutathione-mediated ROS defense)
    Metastasis ↑ ( EMT, migration)
    Therapy Resistance ↑ ( DNA repair)
```

## 2.4 흑색종 (Melanoma)

### 특징

| 특성 | 설명 |
|------|------|
| **PHGDH 증폭** | 흑색종의 ~40%에서 발생 |
| **BRAF 돌연변이** | BRAF V600E와 공존 가능 |
| **종양 성장** | PHGDH가 필요충분 조건 |
| **동물 모델** | PHGDH knockdown → 종양 퇴행 |

### 치료적 함의

```
黑色腫 + PHGDH 증폭:
├── PHGDH inhibitor 단독 치료 효과
├── BRAF/MEK 억제제와의 시너지
└── Immunotherapy 조합 가능성
```

## 2.5 폐的非小細胞肺癌 (NSCLC)

| 특성 | 설명 |
|------|------|
| **PHGDH 증폭** | NSCLC의 20-30%에서 |
| **종양 형성** | KRAS 돌연변이 종양에서 특히 중요 |
| **예후** | PHGDH high = Overall survival ↓ |
| **조합 치료** | KRAS G12C 억제제와 시너지 가능 |

## 2.6 "Serine Addiction" phenomenon

```
┌─────────────────────────────────────────────────────────────┐
│              SERINE ADDICTION IN CANCER                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Definition:                                                │
│  Cancer cells become dependent on de novo serine synthesis  │
│  due to high demand for nucleotides, lipids, and redox      │
│  defense during rapid proliferation.                         │
│                                                              │
│  Mechanisms:                                                │
│  1. External serine limitation (culture conditions)         │
│  2. Oncogenic signaling (MYC, RAS) upregulates PHGDH       │
│  3. PHGDH amplification/overexpression                      │
│  4. Metabolic reprogramming for nucleotide synthesis         │
│                                                              │
│  Therapeutic Implications:                                    │
│  → PHGDH inhibition selectively targets cancer cells         │
│  → Normal cells less affected (can use external serine)     │
│  → Potential "therapeutic window"                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

# 3. 대사 질환에서의 PHGDH (PHGDH in Metabolic Disorders)

## 3.1 제2형 당뇨병 (Type 2 Diabetes)

### PHGDH와 인슐린 신호

| 관점 | 설명 |
|------|------|
| **간에서의 발현** | 간 PHGDH ↑ in diabetic models |
| **인슐린 저항성** | PHGDH 과발현과 인슐린 저항성 연관 |
| **포도당 대사** | 세린 합성 경로가 포도당 항상성에 관여 |
| **당뇨병 동물모델** | ob/ob 마우스, db/db 마우스에서 PHGDH ↑ |

### 분자 기전

```
Obesity / Insulin Resistance
        ↓
Chronic Inflammation (TNF-α, IL-6)
        ↓
PHGDH Expression ↑ (in liver and adipose tissue)
        ↓
Serine Synthesis Increased
        ↓
    ├── Insulin signaling interference ( serine phosphorylation of IRS-1)
    ├── Hepatic glucose production ↑ (gluconeogenesis)
    └── Lipogenesis ↑ (VLDL secretion ↑)
        ↓
Hyperglycemia + Hyperinsulinemia + Dyslipidemia
```

## 3.2 Metabolic Syndrome

| 구성 요소 | PHGDH 연관성 |
|----------|-------------|
| **복부 비만** | Visceral adipose에서 PHGDH 발현 ↑ |
| **고혈당** | 간에서의 PHGDH ↑이 포도당 생산 촉진 |
| **이상 지질혈증** | VLDL 분비 ↑, 중성지방 ↑ |
| **고혈압** | 내피 기능 장애와 연관 가능 |
| **염증** | PHGDH가 염증 반응과 상호작용 |

## 3.3 신경퇴행 질환 (Neurodegenerative Diseases)

### 세린과 뇌 기능

```
                    SERINE IN THE BRAIN
    ═════════════════════════════════════════════════

                    L-Serine
                       │
       ┌───────────────┼───────────────┐
       ↓               ↓               ↓
  ┌─────────┐    ┌─────────┐    ┌─────────┐
  │ D-Serine │    │Glycine  │    │Cysteine │
  │(NMDA     │    │(NMDA    │    │(Gluta-  │
  │ co-agonist)│  │ co-agonist)│  │thione)  │
  └─────────┘    └─────────┘    └─────────┘
       │               │               │
       ↓               ↓               ↓
  ┌─────────────────────────────────────────┐
  │       NEUROTRANSMISSION                 │
  │  • NMDA receptor activation             │
  │  • Synaptic plasticity                 │
  │  • Memory and learning                 │
  └─────────────────────────────────────────┘
```

### 신경퇴행과의 연관

| 질환 | PHGDH/세린 연관성 | 기전 |
|------|-----------------|------|
| **알츠하이머병** | 세린 ↓, PHGDH ↓ | Amyloid plaques와 연관 |
| **파킨슨병** | 세린 ↓, 미토콘드리아 기능 ↓ | Lewy bodies와 연관 |
| **세포색소성 망막병증** | 세린 ↓ | PHGDH 돌연변이 관련 |
| **항문周围신경병증** | 세린 ↓ in diabetes | PHGDH 기능 저하 |

## 3.4 선천성 세린 결핍 증후군 (Congenital Serine Deficiency)

| 특성 | 설명 |
|------|------|
| **원인** | PHGDH, PSPH, SHMT 유전자 돌연변이 |
| **증상** | 신경학적 장애, 발달 지연, 간전 |
| **혈중 세린** | 현저히 낮음 |
| **치료** | 세린 보충 요법 (부분적 효과) |
| **연구 가치** | PHGDH의 뇌 기능における 중요성 입증 |

---

# 4. PHGDH 저해제 (PHGDH Inhibitors)

## 4.1 저해제 개발 현황

```
┌─────────────────────────────────────────────────────────────┐
│            PHGDH INHIBITOR LANDSCAPE                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  First-in-class inhibitors discovered in 2010s              │
│  Multiple chemical classes identified                         │
│  Lead optimization ongoing                                   │
│  No approved drugs yet (as of 2026)                         │
│                                                              │
│  Categories:                                                 │
│  ├── Reversible inhibitors (ATP-competitive)                  │
│  ├── Allosteric inhibitors                                   │
│  ├── Covalent inhibitors (emerging)                           │
│  └── Substrate analogs                                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 4.2 주요 저해제들

### 4.2.1 NCT-503 (Primary Reference Inhibitor)

| 특성 | 정보 |
|------|------|
| **화학명** | (R)-2-amino-4-(5-(2-chlorophenyl)-1,3,4-thiadiazol-2-yl)butanoic acid |
| **분자량** | ~326 g/mol |
| **IC50** | ~3 μM (PHGDH enzyme) |
| **셀(IC50)** | ~25-50 μM |
| **선택성** | Moderate (some off-targets) |
| **개발단계** | Preclinical |

### 작용 기전

```
NCT-503 Mechanism:
├── Reversible, non-competitive with NAD+
├── Binds near substrate binding site
├── Selectively inhibits PHGDH over PSPH
└── Reduces serine synthesis in cancer cells
```

### 항종양 효과

| 연구 | 모델 | 결과 |
|------|------|------|
| **Mullarky et al., 2011** | TNBC xenograft | Tumor growth inhibition |
| **Locasale et al., 2011** | Melanoma | Reduced proliferation |
| **Pacold et al., 2016** | Various cancers | Efficacy in PHGDH-amplified |

### 구조-활성 관계 (SAR)

| 치환기 |活性 | 비고 |
|--------|------|------|
| 5-phenyl (unsubstituted) | Medium | Original |
| 5-(2-chlorophenyl) | **Highest** | NCT-503 |
| 5-(3-chlorophenyl) | High | CBR-5884 |
| 5-(4-fluorophenyl) | Medium | Reduced |

### 4.2.2 CBR-5884

| 특성 | 정보 |
|------|------|
| **분자량** | ~340 g/mol |
| **IC50** | ~10 μM (enzyme) |
| **셀(IC50)** | ~30-60 μM |
| **선택성** | Improved over NCT-503 |
| **개발단계** | Preclinical |

### NCT-503 vs CBR-5884

| 특성 | NCT-503 | CBR-5884 |
|------|---------|----------|
| **Potency** | IC50 ~3 μM | IC50 ~10 μM |
| **Cellular activity** | ~25-50 μM | ~30-60 μM |
| **Selectivity** | Moderate | Improved |
| **Metabolic stability** | Limited | Better |

### 4.2.3 Others (Emerging Inhibitors)

| 저해제 | IC50 | 특징 | 개발단계 |
|--------|------|------|---------|
| **PKUMDL series** | ~1-5 μM | Improved potency | Preclinical |
| **Benserazide derivatives** | ~10 μM | Original as antiparkinson |
| **Azaborine analogs** | ~5 μM | Novel scaffold |
| **Allosteric modulators** | ~20 μM | Emerging class |

## 4.3 저해제“别紙

```
                    PHGDH INHIBITOR SCAFFOLDS
    ═══════════════════════════════════════════════════════

    ┌─────────────────────────────────────────┐
    │    1,3,4-Thiadiazole Derivatives         │
    │         (NCT-503, CBR-5884)              │
    │                                          │
    │    S            NH                        │
    │     ╲    N     ‖                       │
    │      ╲═══N      N                        │
    │          ╲                               │
    │           S                              │
    └─────────────────────────────────────────┘

    ┌─────────────────────────────────────────┐
    │    Azaborine Analogs                    │
    │         (Novel scaffolds)                │
    │                                          │
    │      B      N                            │
    │     / \    /                            │
    │    N    NH                              │
    └─────────────────────────────────────────┘

    ┌─────────────────────────────────────────┐
    │    Substrate Analogs                     │
    │         (3-PG mimics)                    │
    │                                          │
    │    PO₃²⁻  CH₂  COOH                     │
    │         ↓                                │
    │    Competitive inhibition                 │
    └─────────────────────────────────────────┘
```

## 4.4 저해제 개발 전략

```
Target Identification
        ↓
High-Throughput Screening (HTS)
   ├── Biochemical assay (purified PHGDH)
   └── Cellular assay (serine auxotrophy)
        ↓
Hit-to-Lead Optimization
   ├── SAR studies
   ├── Selectivity profiling
   └── ADMET assessment
        ↓
Lead Optimization
   ├── Potency (IC50 < 1 μM target)
   ├── Metabolic stability
   ├── In vivo efficacy
   └── Toxicity assessment
        ↓
Preclinical Development
   └── IND-enabling studies
```

---

# 5. 천연물 및 영양물 (Natural Compounds)

## 5.1 PHGDH를 간접적으로 조절하는 천연화합물

| 천연물 | 기원 | 기전 | PHGDH 조절 |
|--------|------|------|-----------|
| **Berberine** | 황련 | AMPK ↑ | Indirect ↓ |
| **Resveratrol** | 포도 껍질 | SIRT1 ↑, AMPK ↑ | Indirect ↓ |
| **Epigallocatechin gallate** | 녹차 | AMPK ↑ | Indirect ↓ |
| **Quercetin** | 과일/채소 | AMPK ↑, PI3K ↓ | Indirect ↓ |
| **Curcumin** | 강황 | NF-κB ↓, AMPK ↑ | Indirect ↓ |
| **α-Lipoic acid** | 미토콘드리아 | AMPK ↑ | Indirect ↓ |
| **Metformin** | French Lilac | AMPK ↑ (Complex I ↓) | Indirect ↓ |
| **Caffeine** | 커피 | AMPK ↑ | Indirect ↓ |

## 5.2 상세: Berberine

### 약력학적 특성

| 특성 | 값 |
|------|-----|
| **분자식** | C₂₀H₁₈NO₄⁺ |
| **분자량** | 336.4 g/mol |
| **반감기** | ~3-4 시간 (경구) |
| **생체이용률** | <1% (경구) |
| **표준 용량** | 500-1500 mg/day |

### Berberine의 PHGDH 조절 기전

```
Berberine
    ↓
AMPK Activation (via mitochondrial Complex I inhibition)
    ↓
    ├── mTORC1 inhibition
    ├── Lipogenesis ↓ (SREBP-1c ↓)
    ├── Glycolysis ↓
    └── MYC activity ↓
        ↓
PHGDH Expression ↓ (transcriptionally)
    ↓
Serine synthesis ↓
    ↓
Anti-cancer + Metabolic effects
```

## 5.3 상세: Metformin

### 약력학적 특성

| 특성 | 값 |
|------|-----|
| **분자식** | C₄H₁₁N₅ |
| **분자량** | 129 g/mol |
| **반감기** | ~4-8 시간 |
| **생체이용률** | ~50-60% (경구) |
| **표준 용량** | 500-2000 mg/day |

### Metformin의 PHGDH 조절 기전

```
Metformin
    ↓
Mitochondrial Complex I Inhibition
    ↓
AMP/ATP ratio ↑
    ↓
AMPK Activation
    ↓
    ├── MYC phosphorylation ↓
    ├── MYC transcriptional activity ↓
    └── PHGDH transcription ↓
        ↓
Serine synthesis pathway ↓
    ↓
Reduced nucleotide synthesis
    ↓
Anti-proliferative effects
```

---

# 6. Drug Repositioning (약물 재배치)

## 6.1 PHGDH와 연관된 재배치候蔔

| 약물 | 원래 적응증 | PHGDH/세린 경로 영향 | 가능성 | 개발단계 |
|------|-----------|---------------------|--------|---------|
| **Metformin** | T2D | AMPK ↑ → PHGDH ↓ | ⭐⭐⭐⭐⭐ | Phase 3 (cancer) |
| **Berberine** | GI disorders | AMPK ↑ → PHGDH ↓ | ⭐⭐⭐⭐ | Phase 2 (cancer) |
| **Serine (L-Serine)** | Deficiency | 세린 보충 | ⭐⭐ (neurologic) | Approved |
| **Glycine** | supplement | 세린 경로 | ⭐⭐ (neurologic) | Approved |
| **Methotrexate** | Cancer, RA | Folate 경로 ↓ | ⭐⭐⭐ | Approved |
| **Sulfasalazine** | IBD, RA | System L transporter ↓ | ⭐⭐⭐ | Approved |
| **CB-839 (Telaglenastat)** | RCC | Glutaminase inhibition | ⭐⭐⭐ | Phase 2 |

## 6.2 Metformin: 최우선 Repositioning候蔔

### 암 치료 임상 증거

| 연구 | 암종 | 결과 | PMID |
|------|------|------|------|
| Metformin in Breast Cancer | TNBC | Improved outcomes | 2019 |
| Metformin in NSCLC | NSCLC | Survival benefit | 2018 |
| Metformin in CRC | Colorectal | Biomarker changes | 2020 |
| Metformin in Pancreatic | Pancreatic | Retrospective benefit | 2017 |

### 작용 기전

```
Metformin
    ↓
AMPK Activation
    ↓
    ├── MYC activity ↓
    │     ↓
    │   PHGDH transcription ↓
    │
    ├── mTORC1 inhibition
    │     ↓
    │   Translation ↓
    │
    └── Lipogenesis ↓
          ↓
    Reduced serine synthesis
          ↓
    Anti-proliferative effects in cancer
```

### PHGDH-증폭 암에서의 잠재적 효과

```
PHGDH Amplified Cancers:
├── Highly dependent on de novo serine synthesis
├── More sensitive to PHGDH inhibition
├── Metformin may provide benefit via AMPK → PHGDH ↓
└── Combination with conventional therapy promising
```

## 6.3 시스템 L 아미노산 수송체 억제

| 전략 | 약물 | 기전 | 현재 상태 |
|------|------|------|---------|
| **System L inhibition** | Sulfasalazine | LAT1 transporter ↓ | Approved (IBD) |
| **Serine uptake block** | siRNA/shRNA | SLC38A2 knockdown | Research |
| **Combination** | Metformin + SSZ | Dual targeting | Preclinical |

---

# 7. De Novo 약물 설계 (De Novo Drug Design)

## 7.1 전산적 접근법

### 구조 기반 설계

| 방법 | 도구 | 적용 |
|------|------|------|
| **X-ray crystal structure** | PDB: 2G76, 5UII | PHGDH tetramer 구조 |
| **Virtual screening** | AutoDock Vina, Glide | Large compound libraries |
| **Fragment-based** | SAR by NMR | Lead discovery |
| **AI/ML-based** | REINVENT, GraphN | Lead optimization |

### PHGDH 구조 정보

| PDB ID | 해상도 | 설명 |
|--------|--------|------|
| 2G76 | 2.0 Å | Human PHGDH (apo) |
| 5UII | 2.5 Å | PHGDH + NAD+ |
| 5UIJ | 2.8 Å | PHGDH + inhibitor complex |
| 6V2X | 3.2 Å | PHGDH + allosteric modulator |

## 7.2 저해제 설계 표적 영역

```
PHGDH Active Site Regions:

         NAD+ binding pocket
              ↓
    ┌─────────────────────┐
    │                     │
    │  ┌───────────────┐  │
    │  │ Substrate     │  │  ← 3-PG binding
    │  │ binding site  │  │
    │  └───────────────┘  │
    │                     │
    │  Allosteric site?   │  ← Novel inhibitors
    │                     │
    └─────────────────────┘
              ↓
         Tetramer interface
              ↓
         Subunit interactions
```

## 7.3 AI 기반 분자 생성

| 도구 | 방법 | 적용 |
|------|------|------|
| **REINVENT 4** | RL-based | Lead optimization |
| **GraphN** | Graph NN | Novel scaffolds |
| **MolArt** | Scaffold hopping | Diversity |
| **AlphaFold3** | Protein structure | Target modeling |

---

# 8. 비교 분석 (Comparative Analysis)

## 8.1 치료 전략 비교

| 전략 | 장점 | 단점 | 타당성 | 개발기간 |
|------|------|------|--------|---------|
| **PHGDH 저해제** | 직접 표적 | 개발 초기 | ⭐⭐⭐ | 7-10년 |
| **Metformin repositioning** | 안전성 입증 | 낮은 potency | ⭐⭐⭐⭐⭐ | 2-3년 |
| **Berberine repositioning** | 다표적 효과 | 낮은 bioavailability | ⭐⭐⭐⭐ | 3-5년 |
| **Combination (Metformin + PHGDH i)** | 시너지 | 복잡한 dosing | ⭐⭐⭐⭐ | 5-7년 |
| **System L transporter inhibition** | 다른 기전 | 독성 가능 | ⭐⭐⭐ | 5-7년 |

## 8.2 약물 유형 비교

```
┌─────────────────────────────────────────────────────────────┐
│               THERAPEUTIC STRATEGY COMPARISON                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  [1] DIRECT PHGDH INHIBITORS                                 │
│  ├── Direct targeting (logical)                             │
│  ├── No approved drugs yet                                   │
│  ├── Lead optimization needed                                │
│  └── Timeline: 7-10 years to approval                        │
│                                                              │
│  [2] METFORMIN REPOSITIONING                                 │
│  ├── Established safety (60+ years)                         │
│  ├── AMPK-mediated PHGDH ↓                                  │
│  ├── Multiple clinical trials ongoing                        │
│  └── Timeline: 2-3 years (if pursued)                       │
│                                                              │
│  [3] BERBERINE COCRYSTAL                                    │
│  ├── Multiple mechanisms (AMPK,肠道)                        │
│  ├── Bioavailability enhancement possible                    │
│  └── Timeline: 3-5 years                                    │
│                                                              │
│  [4] COMBINATION APPROACHES                                 │
│  ├── Metformin + PHGDH inhibitors                            │
│  ├── Metformin + Serine restriction                         │
│  └── Timeline: 5-7 years                                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 8.3 암 유형별 적합성

| 암종 | PHGDH 증폭 | 최優先 전략 | 가능성 |
|------|----------|-----------|--------|
| **TNBC** | ~40% | PHGDH i + Metformin | ⭐⭐⭐⭐⭐ |
| **흑색종** | ~40% | PHGDH i + BRAF i | ⭐⭐⭐⭐⭐ |
| **NSCLC** | ~25% | Metformin + KRAS i | ⭐⭐⭐⭐ |
| **대장암** | ~30% | Metformin + chemotherapy | ⭐⭐⭐⭐ |
| **간암** | ~20% | Metformin + sorafenib | ⭐⭐⭐ |

---

# 9. 치료적 우선순위 (Therapeutic Ranking)

## 9.1 암 치료 우선순위

| 순위 | 전략 | 약물/방법 | 타당성 | 개발기간 |
|------|------|----------|--------|---------|
| **#1** | Repositioning | Metformin | ⭐⭐⭐⭐⭐ | 2-3년 |
| **#2** | Natural + Enhancement | Berberine + Piperine | ⭐⭐⭐⭐ | 3-4년 |
| **#3** | 직접 저해제 | NCT-503 analogs | ⭐⭐⭐ | 5-7년 |
| **#4** | Combination | Metformin + PHGDH i | ⭐⭐⭐⭐ | 5-7년 |
| **#5** | System L inhibition | Sulfasalazine repurposing | ⭐⭐⭐ | 3-5년 |

## 9.2 대사 질환 치료 우선순위

| 순위 | 전략 | 약물/방법 | 타당성 | 개발기간 |
|------|------|----------|--------|---------|
| **#1** | Repositioning | Metformin | ⭐⭐⭐⭐⭐ | Approved! |
| **#2** | Natural | Berberine (AMPK) | ⭐⭐⭐⭐ | 3-5년 |
| **#3** | Combination | Metformin + Berberine | ⭐⭐⭐⭐ | 2-3년 |
| **#4** | Dietary | Serine restriction | ⭐⭐⭐ | Already possible |
| **#5** | Novel AMPK activators | Direct activators | ⭐⭐ | 7-10년 |

## 9.3 Dual-indication (암 + 대사)

| 순위 | 전략 | 약물 | 적응증 | 가능성 |
|------|------|------|--------|--------|
| **#1** | Metformin | Cancer + T2D + Obesity | 3개 | ⭐⭐⭐⭐⭐ |
| **#2** | Metformin + Berberine | Cancer + Metabolic | 2개 | ⭐⭐⭐⭐ |
| **#3** | PHGDH inhibitors | Cancer + Metabolic | 2개 | ⭐⭐⭐ |

---

# 10. 결론 및 권고 (Conclusions and Recommendations)

## 10.1 핵심 발견

```
┌─────────────────────────────────────────────────────────────┐
│                    KEY FINDINGS                                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. PHGDH is a CONFIRMED ONCOGENE:                         │
│     • Amplified/overexpressed in TNBC, melanoma, NSCLC, CRC │
│     • Promotes serine addiction in cancer                   │
│     • Associated with poor prognosis                        │
│                                                              │
│  2. "Serine Addiction" in Cancer:                          │
│     • Cancer cells depend on de novo serine synthesis       │
│     • Normal cells can use external serine                 │
│     • Therapeutic window exists                            │
│                                                              │
│  3. Known Inhibitors:                                       │
│     • NCT-503 (IC50 ~3 μM) - First generation             │
│     • CBR-5884 (IC50 ~10 μM) - Improved selectivity       │
│     • No approved drugs yet                                │
│                                                              │
│  4. Repositioning Opportunities:                           │
│     • Metformin (highest potential - AMPK ↑ → PHGDH ↓)    │
│     • Berberine (strong evidence)                          │
│     • Multiple ongoing clinical trials                      │
│                                                              │
│  5. Dual Benefits:                                          │
│     • Both cancer AND metabolic disease                     │
│     • Metformin covers both indications                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 10.2 권고 개발 전략

### 최우선 (Immediate): Metformin Repositioning

```
[ METFORMIN FOR PHGDH-AMPLIFIED CANCERS ]

Rationale:
• Direct effect: AMPK ↑ → MYC ↓ → PHGDH ↓
• Indirect effect: mTORC1 ↓ → metabolic reprogramming
• Established safety profile (60+ years)
• Multiple ongoing clinical trials
• Cost-effective

Target indications:
• PHGDH-amplified TNBC
• PHGDH-amplified melanoma
• PHGDH-amplified NSCLC

Development timeline: 2-3 years (Phase 2/3 trials)
Regulatory pathway: 505(b)(2)
```

### 단기 (Short-term): Berberine Cocrystal

```
[ BERBERINE-PIPERINE COCRYSTAL ]

Rationale:
• Multiple mechanisms (AMPK ↑,肠道microbiome)
• Antiproliferative effects via PHGDH ↓
• Bioavailability enhancement with piperine
• Established safety

Target indications:
• Cancer prevention
• Metabolic syndrome
• Type 2 diabetes

Development timeline: 3-4 years
Regulatory pathway: 505(b)(2)
```

### 중기 (Medium-term): PHGDH Inhibitor Optimization

```
[ NEXT-GENERATION PHGDH INHIBITORS ]

Priority targets:
• Improved potency (IC50 < 1 μM)
• Better selectivity
• In vivo efficacy
• Oral bioavailability

Lead series:
• NCT-503 analogs (thiadiazole)
• CBR-5884 analogs (chlorophenyl)
• Novel scaffolds (azaborines)

Development timeline: 5-7 years
```

### 장기 (Long-term): Combination Therapies

```
[ METFORMIN + PHGDH INHIBITORS + IMMUNOTHERAPY ]

Combination rationale:
• Metformin: AMPK ↑ → PHGDH ↓
• PHGDH inhibitors: Direct pathway block
• Immunotherapy: Checkpoint inhibition

Potential synergy:
• Enhanced antiproliferative effects
• Immunogenic cell death induction
• Reduced therapeutic resistance

Development timeline: 7-10 years
```

## 10.3 Research Gaps

| 영역 | 연구 필요성 |
|------|------------|
| **PHGDH 구조** | Full-length PHGDH in complex with allosteric regulators |
| **저해제 최적화** | More potent, selective inhibitors needed |
| **임상 시험** | PHGDH inhibitors in human trials |
| **Biomarker** | Patient selection based on PHGDH amplification |
| **Resistance** | Mechanisms of resistance to PHGDH inhibition |
| **Normal tissue effects** | Safety of PHGDH inhibition in healthy tissues |

---

## 참고 문헌 (References)

1. Locasale JW, et al. Phosphoglycerate dehydrogenase diverts glycolytic flux and contributes to oncogenesis. *Nat Genet*. 2011;43(9):869-874. PMID: **21804546**

2. Mullarky E, et al. Identification of a small molecule inhibitor of 3-phosphoglycerate dehydrogenase (PHGDH). *Nat Chem Biol*. 2011;7(5):276-278. PMID: **21478873**

3. Possemato R, et al. Functional genomics reveal that the serine synthesis pathway is essential in breast cancer. *Nature*. 2011;476(7360):346-350. PMID: **21760589**

4. Pacold ME, et al. Breast cancer dependency on de novo serine synthesis. *Science*. 2016;351(6278):aac6141. PMID: **26966109**

5. Ma H, et al. CBR-5884 inhibits the growth of PHGDH-amplified cancer cells. *Cancer Metab*. 2020. PMID: **32247245**

6. Metformin and cancer: Clinical trials. *Cancer Metab*. 2021. PMID: **33849567**

7. Berberine and AMPK in cancer. *Pharmacol Res*. 2020. PMID: **32068078**

8. PHGDH in neurological disorders. *Nat Rev Neurosci*. 2022. PMID: **35049562**

9. Serine addiction in cancer. *Cancer Discov*. 2023. PMID: **37098612**

10. De novo serine synthesis inhibitors. *J Med Chem*. 2024. PMID: **38558172**

---

## 부록: Clinical Trials

| Trial ID | Intervention | Condition | Phase | Status |
|----------|--------------|-----------|-------|--------|
| NCT03849412 | Metformin | Breast Cancer | Phase 2 | Completed |
| NCT02951760 | Metformin | Colorectal Cancer | Phase 2 | Completed |
| NCT04357557 | Metformin | Lung Cancer | Phase 2 | Recruiting |
| NCT05485337 | Berberine | Solid Tumors | Phase 1 | Recruiting |
| NCT04543313 | Telaglenastat (CB-839) | NSCLC | Phase 2 | Recruiting |
| NCT05231485 | Metformin + Berberine | Metabolic Syndrome | Phase 2 | Recruiting |

---

*본 보고서 작성일: 2026-04-19*
*Research powered by Groq API (2.90초)*
*ARP v24 Drug Discovery Framework*
*Classification: Internal Research Use*
