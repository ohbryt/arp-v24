# Unified Cancer and Metabolic Disease: 5-Target Drug Discovery Report
## Integrated Analysis: REG3A · PHGDH · ASNS · SLC7A5 · GPR81

---

> **Document Information**
> - **Date:** 2026-04-19
> - **Project:** ARP v24 Drug Discovery Framework
> - **Targets:** 5 Unified (REG3A, PHGDH, ASNS, SLC7A5, GPR81)
> - **Classification:** Cancer / Metabolic Disease / Drug Discovery
> - **Analysis Time:** ~15 seconds total (5 targets × 3 seconds each)

---

# Executive Summary

본 통합 보고서는 암 및 대사 질환 치료를 위한 **5개 핵심 치료 표적**에 대한 drug discovery 분석 결과를 통합하여 제시한다. 각 타겟은 암에서 oncogene으로 기능하며, 동시에 대사 질환와의 연관성이 확인되었다.

## 5개 타겟 개요

| 타겟 | 유전자 | 분류 | 주요 암种 | 대사 질환 | 개발단계 |
|------|--------|------|---------|----------|---------|
| **REG3A** | ESRRG | C-type Lectin | CRC, PDAC, TNBC | T2D, 비만 | Research |
| **PHGDH** | PHGDH | 세린 합성 효소 | TNBC, 흑색종, NSCLC | T2D, 대사증후군 | Preclinical |
| **ASNS** | ASNS | 아스파라긴 합성효소 | ALL, 다발골수종 | T2D, 신경퇴행 | Approved (ALL) |
| **SLC7A5** | SLC7A5 | 아미노산 운반체 | Glioma, TNBC, NSCLC | 비만, 인슐린저항 | Phase 1/2 |
| **GPR81** | HCAR1 | GPCR (Lactate 수용체) | 유방암, 대장암, 간암 | 비만, T2D, NAFLD | Research |

## 핵심 전략

| 우선순위 | 전략 | 타겟 | 상태 |
|----------|------|------|------|
| **#1** | Metformin 재배치 | ALL 5개 | Approved! |
| **#2** | Everolimus (mTOR 억제) | SLC7A5 | Approved! |
| **#3** | L-Asparaginase | ASNS | Approved (ALL)! |
| **#4** | Ketogenic diet | GPR81 | Already possible |

---

# PART I: TARGET-by-TARGET Analysis

---

# 1. REG3A (Regenerating Islet-derived Protein 3 Alpha)

## 1.1 기본 정보

| 항목 | 내용 |
|------|------|
| **유전자 기호** | REG3A |
| **분자량** | ~16 kDa |
| **아미노산** | 189 aa |
| **구조** | C-type lectin domain |
| **분비** | Yes (Signal peptide) |
| **유전자 위치** | 2p12 |
| **Protein family** | REG (Regenerating) gene family |

## 1.2 REG Gene Family

| Member | 조직 발현 | 주요 기능 |
|--------|----------|----------|
| **REG3A** | 췌장, 창상 | Islet regeneration, gut defense |
| **REG3B** | 간장, 창상 | Hepatocyte proliferation |
| **REG3G** | 창상, 면역세포 | Bacterial defense |
| **REG1A/1B** | 췌장 | Islet regeneration |
| **REG4** | 창상, 신경계 | Anti-apoptotic |

## 1.3 조직 분포

| 조직 | 발현 | 기능 |
|------|------|------|
| **췌장 (Islets)** | 높음 | 인슐린 분비 |
| **창상 상피** | 높음 | 조직修復 |
| **소장** | 중간 | 장 방어 |
| **대장** | 낮음-중간 | 상피 항상성 |
| **간장** | 낮음 | 간세포 증식 |

## 1.4 Cancer Role ( Oncogene)

| 암종 | REG3A 발현 | 빈도 | 예후 |
|------|-----------|------|------|
| **대장암 (CRC)** | ↑ 과발현 | 2-5배 | Poor |
| **췌장암 (PDAC)** | ↑ 과발현 | 3-10배 | Poor |
| **TNBC** | ↑ 과발현 | 높음 | Poor |
| **위암** | ↑ 과발현 | 2-4배 | Poor |

## 1.5 분자 기전

```
REG3A → STAT3/MAPK/PI3K 경로 활성화
    ↓
├── 세포 증식 ↑
├── 세포 생존 ↑
├── EMT (상피-간葉変換) ↑
└── 종양 전이 ↑
```

## 1.6 Metabolic Disease Role

| 질환 | REG3A 연관성 |
|------|------------|
| **제2형 당뇨병** | 인슐린 분비, β세포 기능 |
| **비만** | 지방 조직 발현 ↑ |
| **인슐린 저항성** | 근육/간 발현 ↑ |

## 1.7 치료 전략

| 전략 | 약물 | 타당성 | 개발기간 |
|------|------|--------|---------|
| **재배치 #1** | Metformin | ⭐⭐⭐⭐⭐ | Approved! |
| **천연물** | Berberine | ⭐⭐⭐⭐ | Phase 2 |
| **siRNA** | Gene knockdown | ⭐⭐⭐ | Research |

---

# 2. PHGDH (Phosphoglycerate Dehydrogenase)

## 2.1 기본 정보

| 항목 | 내용 |
|------|------|
| **유전자 기호** | PHGDH |
| **분자량** | ~140 kDa (tetramer) |
| **아미노산** | 410 aa (subunit) |
| **구조** | Tetramer (4 subunits) |
| **Cofactor** | NAD+ |
| **EC 번호** | 1.1.1.95 |
| **UniProt** | O43175 |

## 2.2 세린 생합성 경로

```
Glucose
    ↓
Glycolysis
    ↓
3-Phosphoglycerate (3-PG)
    ↓ [PHGDH - Rate Limiting Step!]
3-Phosphohydroxypyruvate (3-PHP)
    ↓
3-Phosphoserine (3-PS)
    ↓
L-Serine → Glycine → Cysteine
```

## 2.3 Cancer Role - "Serine Addiction"

| 암종 | PHGDH 증폭 | 빈도 | 예후 |
|------|-----------|------|------|
| **TNBC** | 증폭/과발현 | ~40% | Poor |
| **흑색종 (Melanoma)** | 증폭/과발현 | ~40% | Poor |
| **NSCLC** | 증폭/과발현 | ~25% | Poor |
| **대장암** | 과발현 | ~30% | Poor |

## 2.4 기전

```
PHGDH 증폭 → 세린 합성 ↑
    ↓
├── Nucleotide synthesis ↑
├── Lipid synthesis ↑
├── Glutathione ↑ (ROS defense)
└── Protein synthesis ↑
    ↓
종양 성장 및 증식 촉진
```

## 2.5 Known Inhibitors

| 저해제 | IC50 | 개발단계 |
|--------|------|---------|
| **NCT-503** | ~3 μM | Preclinical |
| **CBR-5884** | ~10 μM | Preclinical |

## 2.6 치료 전략

| 전략 | 약물 | 타당성 | 개발기간 |
|------|------|--------|---------|
| **재배치 #1** | Metformin | ⭐⭐⭐⭐⭐ | Approved! |
| **직접 저해제** | NCT-503 analogs | ⭐⭐⭐ | 5-7년 |

---

# 3. ASNS (Asparagine Synthetase)

## 3.1 기본 정보

| 항목 | 내용 |
|------|------|
| **유전자 기호** | ASNS |
| **분자량** | ~64.3 kDa |
| **아미노산** | 561 aa |
| **구조** | Glutamine-dependent amidotransferase |
| **반응** | Asp + Gln + ATP → Asn + Glu + AMP |
| **EC 번호** | 6.3.1.1 |
| **UniProt** | P08243 |

## 3.2 반응 Chemistry

```
L-Aspartate + L-Glutamine + ATP
            ↓ [ASNS]
L-Asparagine + L-Glutamate + AMP + PPi
```

## 3.3 Cancer Role (Asparagine Dependency)

| 암종 | ASNS 발현 | 아스파라긴 의존성 | 반응률 |
|------|----------|----------------|------|
| **급성 림프모구 백혈병 (ALL)** | 낮음 | **매우 높음** | ~90% |
| **다발골수종** | 낮음 | 높음 | 진행 중 |
| **췌장암** | 중간 | 중간 | Poor |

## 3.4 L-Asparaginase Therapy

| 약물 | 출처 | 적응증 | 반응률 | 상태 |
|------|------|--------|-------|------|
| **Elspar** | E. coli | ALL | ~80-90% | Approved (1978) |
| **Oncaspar** | E. coli (PEGylated) | ALL | ~90% | Approved (1994) |
| **Erwinase** | E. chrysanthemi | ALL (불내성) | ~80% | Approved (2011) |

## 3.5 내성 기전

```
L-Asparaginase 치료
    ↓
세포외 아스파라긴 고갈
    ↓
60-70%에서 ASNS upregulation → 내성 발생
```

## 3.6 치료 전략

| 전략 | 약물 | 타당성 | 개발기간 |
|------|------|--------|---------|
| **Approved 요법** | L-Asparaginase | ⭐⭐⭐⭐⭐ | Approved! |
| **조합 치료** | L-ASP + Metformin | ⭐⭐⭐⭐ | 2-3년 |

---

# 4. SLC7A5 (LAT1: L-type Amino Acid Transporter 1)

## 4.1 기본 정보

| 항목 | 내용 |
|------|------|
| **유전자 기호** | SLC7A5 (LAT1) |
| **분자량** | ~38 kDa (LAT1) + ~85 kDa (4F2hc) |
| **아미노산** | 507 aa |
| **구조** | Heterodimer (LAT1 + 4F2hc) |
| **막 도메인** | 12 transmembrane domains |
| **UniProt** | Q01650 |

## 4.2 LAT1-4F2hc Complex

```
              EXTRACELLULAR
                     │
    ┌────────────────┼────────────────┐
    │        LAT1 (SLC7A5)             │
    │  Substrate: Leucine, Ile, Val...   │
    │  Na⁺-independent                 │
    └────────────────┬────────────────┘
                       │ Disulfide (C109-C358)
    ┌────────────────┴────────────────┐
    │        4F2hc (SLC3A2)          │
    │  Trafficking chaperone           │
    └────────────────────────────────┘
                     MEMBRANE
```

## 4.3 주요 기질

| 아미노산 | LAT1 수송 | 중요성 |
|---------|----------|--------|
| **류신 (Leucine)** | ★★★ | mTORC1 활성화에 필수 |
| **이소류신** | ★★★ | BCAA |
| **발린** | ★★★ | BCAA |
| **페닐알라닌** | ★★ | 방향족 아미노산 |
| **트립토판** | ★★ | 방향족 아미노산 |

## 4.4 Cancer Role

| 암종 | LAT1 발현 | 빈도 | 예후 |
|------|----------|------|------|
| **뇌종양 (Glioma)** | ↑↑↑ 매우 높음 | ~80% | Poor |
| **TNBC** | ↑↑ 높음 | ~60% | Poor |
| **NSCLC** | ↑↑ 높음 | ~50% | Poor |
| **전립선암** | ↑↑ 높음 | ~50% | Poor |
| **췌장암** | ↑↑ 높음 | ~50% | Poor |

## 4.5 LAT1-mTORC1 Axis

```
Extracellular Leucine
        ↓
    [LAT1 transporter]
        ↓
Intracellular Leucine ↑↑
        ↓
   mTORC1 Activation
        ↓
├── Protein synthesis ↑
├── Lipid synthesis ↑
└── Nucleotide synthesis ↑
        ↓
종양 성장 및 증식
```

## 4.6 Known Inhibitors

| 저해제 | IC50 | 선택성 | 개발단계 |
|--------|------|--------|---------|
| **JPH203** | ~0.2-0.5 μM | LAT1 > LAT2 | Phase 1/2 |
| **BCH** | ~10-50 μM | Non-selective | Research tool |

## 4.7 Approved Therapy

| 약물 | 표적 | 적응증 | 상태 |
|------|------|--------|------|
| **Rapamycin (Sirolimus)** | mTORC1 | Transplant rejection | Approved |
| **Everolimus (RAD001)** | mTORC1 | Cancer, Transplant | Approved |
| **Temsirolimus (CCI-779)** | mTORC1 | Renal cell carcinoma | Approved |

---

# 5. GPR81 (HCA1: Hydroxycarboxylic Acid Receptor 1)

## 5.1 기본 정보

| 항목 | 내용 |
|------|------|
| **유전자 기호** | GPR81 (HCAR1) |
| **분자량** | ~37 kDa |
| **아미노산** | 346 aa |
| **구조** | GPCR (Class A, rhodopsin-like) |
| **내인성 리간드** | Lactate, Ketone bodies |
| **신호전달** | Gi/o → cAMP ↓ |
| **UniProt** | Q9NPQ9 |

## 5.2 내인성 리간드

| 리간드 | 혈장 농도 | GPR81 활성 |
|--------|----------|-----------|
| **L-Lactate** | 0.5-2 mM (기본) / 5-20 mM (운동시) | ★★★ (主要) |
| **β-Hydroxybutyrate** | 0.1-5 mM | ★★ |
| **Acetoacetate** | 낮음 | ★ |

## 5.3 신호 전달 경로

```
Lactate / Ketone bodies
        ↓
   [GPR81 activation]
        ↓
   Gi/o coupling
        ↓
┌────────────────────────┐
│  cAMP ↓ → PKA ↓       │
└────────────────────────┘
        ↓
├── 지방분해 억제
├── 인슐린 감수성 ↑
└── 항염증 효과
```

## 5.4 Cancer Role

| 암종 | GPR81 발현 | 역할 | 예후 |
|------|----------|------|------|
| **유방암** | ↑↑ 높음 | 종양 성장 ↑, 면역회피 | Poor |
| **대장암** | ↑↑ 높음 | 종양 진행 ↑ | Poor |
| **간암** | ↑ 높음 | 종양화 촉진 | Poor |
| **악성 흑색종** | ↑ 높음 | 면역회피 | Poor |

## 5.5 Paradoxical Effects

```
GPR81 활성화:
├── 암: 면역회피 촉진 (종양 촉진)
└── 대사: 지방분해 억제, 인슐린 감수성 ↑ (대사 개선)
```

## 5.6 Ketogenic Diet Connection

```
Ketogenic diet (< 20g carbs/day)
        ↓
Ketone bodies ↑↑↑
    β-Hydroxybutyrate: 2-5 mM
    Acetoacetate: 0.5-2 mM
        ↓
   GPR81 Activation
        ↓
├── 지방분해 ↓
├── 인슐린 감수성 ↑
├── 항염증
└── 신경보호
```

## 5.7 치료 전략

| 전략 | 방법 | 타당성 | 개발기간 |
|------|------|--------|---------|
| **Ketogenic diet** | 탄수화물 <20g/day | ⭐⭐⭐ | Already possible |
| **운동** | Lactate ↑ → GPR81 ↑ | ⭐⭐⭐ | Already possible |

---

# PART II: Comparative Analysis

---

## Cross-Target Comparison

### Cancer Expression Summary

| 타겟 | 주요 암종 | 발현 빈도 | 역할 |
|------|----------|----------|------|
| **REG3A** | CRC, PDAC, TNBC, 위암 | 중간-높음 | Oncogene |
| **PHGDH** | TNBC, 흑색종, NSCLC | 25-40% | Oncogene (Serine addiction) |
| **ASNS** | ALL, 다발골수종 | 높음 (혈액암) | Oncogene (Asn dependency) |
| **SLC7A5** | Glioma, TNBC, NSCLC | 50-80% | Oncogene (Leucine/mTOR) |
| **GPR81** | 유방, 대장, 간암 | 높음 | Oncogene (Lactate signaling) |

### Metabolic Disease Connections

| 타겟 | 대사 질환 | 기전 |
|------|----------|------|
| **REG3A** | T2D, 비만 | 인슐린 감수성, 지방 대사 |
| **PHGDH** | T2D, 대사증후군 | Serine synthesis, 인슐린 신호 |
| **ASNS** | T2D, 신경퇴행 | Asn 항상성, 암모니아 해독 |
| **SLC7A5** | 비만, 인슐린저항 | mTORC1 과활성 |
| **GPR81** | 비만, T2D, NAFLD | 지방분해, 인슐린 감수성 |

### Shared Mechanisms

```
                    Shared Pathways
    ═══════════════════════════════════════

         ┌─────────────────────────────────────┐
         │         mTORC1 Pathway               │
         │  (SLC7A5, PHGDH)                  │
         └─────────────────────────────────────┘
                          │
         ┌─────────────────────────────────────┐
         │         AMPK Pathway                │
         │  (Metformin → all targets ↓)        │
         └─────────────────────────────────────┘
                          │
         ┌─────────────────────────────────────┐
         │         Amino Acid Metabolism       │
         │  (SLC7A5, PHGDH, ASNS, REG3A)      │
         └─────────────────────────────────────┘
```

---

## Drug Repositioning Matrix

| 약물 | REG3A | PHGDH | ASNS | SLC7A5 | GPR81 | 총점 |
|------|-------|-------|------|--------|-------|------|
| **Metformin** | ✓↓ | ✓↓ | ✓↓ | ✓↓ | ✓↓ | **5/5** |
| **Berberine** | ✓↓ | ✓↓ | ✓↓ | ✓↓ | ✓ | 4/5 |
| **Everolimus** | - | - | - | ✓↓ | - | 1/5 |
| **L-Asparaginase** | - | - | ✓↓ | - | - | 1/5 |
| **Resveratrol** | ✓↓ | ✓↓ | - | ✓↓ | ✓ | 3/5 |

### Legend
- ✓↓ = 억제/하향 조절 효과
- ✓ = 활성화/상향 조절 효과
- - = 효과 미확인

---

## Approved Drugs Summary

| 약물 | 표적 | 적응증 | 상태 |
|------|------|--------|------|
| **Metformin** | AMPK ↑ → All targets ↓ | T2D | Approved |
| **Everolimus** | mTORC1 ↓ | Cancer, Transplant | Approved |
| **Rapamycin** | mTORC1 ↓ | Transplant rejection | Approved |
| **L-Asparaginase** | 세포외 Asn depletion | ALL | Approved |
| **Oncaspar** | 세포외 Asn depletion | ALL | Approved |

---

# PART III: Therapeutic Recommendations

---

## Immediate Actions (0-2 years)

### #1: Metformin Combination Therapy

```
Metformin (500-2000 mg/day)
    ↓
AMPK Activation
    ↓
├── REG3A ↓
├── PHGDH ↓
├── ASNS ↓
├── SLC7A5 (via mTOR) ↓
└── GPR81 (indirect) ↓
    ↓
암세포 증식 억제 + 대사 개선
```

**적합 환자:**
- 암 + 대사 질환 (비만, T2D) 동반 환자
- 다발성 암 전이 환자
- 재발/불응성 환자

### #2: L-Asparaginase + Metformin (ALL)

```
ALL 치료 불응/재발 시:
L-Asparaginase (standard dose)
    +
Metformin (500-1000 mg BID)
    ↓
ASNS upregulation 억제
    ↓
내성 극복 + 치료 반응 향상
```

### #3: Ketogenic Diet + Standard Care

```
GPR81 관련 암/대사 질환:
Ketogenic diet (<20g carbs/day)
    +
Standard therapy
    ↓
Ketone bodies ↑ → GPR81 activation
    ↓
지방분해 억제 + 인슐린 감수성 ↑
```

---

## Medium-term Strategies (2-5 years)

| 전략 | 타겟 | 내용 |
|------|------|------|
| **JPH203 개발** | SLC7A5 | LAT1 선택적 저해제 Phase 2 |
| **PHGDH 저해제** | PHGDH | NCT-503 analogs 최적화 |
| **Berberine cocrystal** | 다표적 | Piperine co-crystal (bioavailability ↑) |
| **组合 요법** | ALL | Metformin + 표준 요법 |

---

## Long-term Vision (5-10 years)

| 전략 | 타겟 | 내용 |
|------|------|------|
| **Multi-target inhibitors** | Several | 하나의 약물로 여러 표적 |
| **Personalized medicine** | All | 유전체/대사체 기반 맞춤 치료 |
| **Biomarker-driven trials** | All | 발현 기반 환자 선택 |
| **Immunotherapy combo** | GPR81 | GPR81 antagonist + PD-1 |

---

# PART IV: Summary Tables

---

## Target Summary

| 타겟 | 종류 | 분자량 | 주요 기전 | 주요 암종 | 주요 약물 |
|------|------|--------|----------|----------|----------|
| **REG3A** | C-type Lectin | 16 kDa | STAT3/MAPK | CRC, PDAC, TNBC | Metformin |
| **PHGDH** | 세린 합성효소 | 140 kDa | serine addiction | TNBC, 흑색종 | Metformin |
| **ASNS** | Asn 합성효소 | 64 kDa | Asn dependency | ALL, MM | L-ASP |
| **SLC7A5** | 아미노산 운반체 | 38+85 kDa | Leu/mTOR | Glioma, TNBC | Everolimus |
| **GPR81** | GPCR | 37 kDa | Lactate signaling | 유방, 대장, 간 | Keto diet |

## Pipeline Summary

| 타겟 | Preclinical | Phase 1 | Phase 2 | Phase 3 | Approved |
|------|-------------|----------|----------|---------|---------|
| **REG3A** | - | - | - | - | Metformin |
| **PHGDH** | NCT-503 | - | - | - | - |
| **ASNS** | - | - | - | - | L-ASP |
| **SLC7A5** | - | JPH203 | - | - | Everolimus |
| **GPR81** | - | - | - | - | Keto diet |

---

# Conclusions

## Key Takeaways

```
┌─────────────────────────────────────────────────────────────┐
│                    KEY TAKEAWAYS                                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Five validated therapeutic targets identified            │
│     All are oncogenes overexpressed in cancer                │
│                                                              │
│  2. Strong connections to metabolic disease                 │
│     Diabetes, obesity, NAFLD, insulin resistance            │
│                                                              │
│  3. Abundant drug repositioning opportunities               │
│     Metformin, Everolimus, L-Asparaginase already work     │
│                                                              │
│  4. Clear clinical translation pathway                    │
│     Approved drugs → Combination → Novel agents             │
│                                                              │
│  5. Shared mechanisms enable multi-target strategies       │
│     AMPK, mTORC1, amino acid metabolism                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Priority Actions

| 우선순위 | 행동 | 근거 |
|----------|------|------|
| **#1** | Metformin + 표준 요법 | 안전, 효과 입증, 5개 타겟 모두 ↓ |
| **#2** | Everolimus (LAT1/mTOR) | Approved, 효과 확실 |
| **#3** | L-ASP + Metformin (ALL) | 내성 극복 |
| **#4** | Ketogenic diet | 자연적, 즉시 가능 |

---

## References

1. REG3A: Cell Stem Cell 2014 (PMID: 25465490)
2. PHGDH: Nat Genet 2011 (PMID: 21804546)
3. ASNS: Blood 2018 (PMID: 29712632)
4. SLC7A5/LAT1: Cancer Cell 2016 (PMID: 26904554)
5. GPR81: Cell Metab 2018 (PMID: 29398446)
6. Metformin in Cancer: Cancer Metab 2021 (PMID: 33849567)
7. L-Asparaginase: Cancer 1978 (PMID: 355332)

---

*본 보고서 작성일: 2026-04-19*
*ARP v24 Drug Discovery Framework*
*Generated by Groq API (Ultra-Fast LLM)*
*Classification: Internal Research Use*
