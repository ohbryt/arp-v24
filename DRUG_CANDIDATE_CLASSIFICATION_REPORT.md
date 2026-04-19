# Drug Candidate Classification Report Template
## ARP v24 - Comprehensive Drug Discovery Framework

---

> **Document Information**
> - **Version:** 1.0
> - **Date:** 2026-04-19
> - **Classification:** Drug Discovery / Therapeutic Development
> - **Target:** Comprehensive analysis of all drug candidate modalities

---

# 목차 (Table of Contents)

1. [개요: 약물 유형 총론](#1-개요-약물-유형-총론)
2. [Known Agonists (활성화제)](#2-known-agonists-활성화제)
3. [Known Inhibitors (억제제)](#3-known-inhibitors-억제제)
4. [Natural Compounds (천연물)](#4-natural-compounds-천연물)
5. [Small Molecules (저분자 화합물)](#5-small-molecules-저분자-화합물)
6. [Peptides (펩타이드)](#6-peptides-펩타이드)
7. [De Novo Designed Candidates](#7-de-novo-designed-candidates)
8. [Drug Repositioning Candidates](#8-drug-repositioning-candidates)
9. [Comparative Analysis Matrix](#9-comparative-analysis-matrix)
10. [ Therapeutic Ranking & Recommendations](#10-therapeutic-ranking--recommendations)

---

# 1. 개요: 약물 유형 총론 (Overview of Drug Modalities)

## 1.1 약물 개발 패러다임의 진화

현대 약물 발견은 다양한 치료적 접근법을 포함하며, 각 유형은 고유한 장단점을 가진다.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DRUG CANDIDATE MODALITIES                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────────┐ │
│  │   KNOWN    │  │   KNOWN    │  │   NOVEL     │  │   NOVEL    │ │
│  │  AGONISTS  │  │ INHIBITORS  │  │  NATURAL    │  │   SMALL    │ │
│  │            │  │            │  │ COMPOUNDS   │  │ MOLECULES  │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └────────────┘ │
│                                                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │
│  │  NOVEL     │  │  DE NOVO    │  │   DRUG      │                  │
│  │  PEPTIDES  │  │  DESIGNED   │  │REPOSITIONING│                  │
│  │            │  │ CANDIDATES  │  │ CANDIDATES  │                  │
│  └─────────────┘  └─────────────┘  └─────────────┘                  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## 1.2 약물 유형 비교표

| 유형 | 분자량 | 개발단계 | 장점 | 단점 | 투여경로 |
|------|--------|---------|------|------|---------|
| **Agonists** | ~300-500 Da | Approved/Clinical | 높은 효능, 명확한 MOA | 과활성화 위험 | 주로 경구 |
| **Inhibitors** | ~300-600 Da | Approved/Clinical | 선택적 억제, 용량 조절 용이 | 내성 가능 | 경구/주사 |
| **Natural Compounds** | ~200-1000 Da | Preclinical/Clinical | 안전성 프로파일, 다표적 | 낮은 순도, 흡수 문제 | 경구/국소 |
| **Small Molecules** | ~100-500 Da | Lead optimization | 합성 용이, ADMET 최적화 가능 | 독성 가능성 | 경구/주사 |
| **Peptides** | ~500-5000 Da | Preclinical/Clinical | 높은 선택성, 효능 | Proteolytic instability | 주사/펜 |
| **De Novo Candidates** | ~200-800 Da | Discovery | 새로운 구조, IP 가능성 | 리스크 높음 | 다양 |
| **Drug Repositioning** | ~200-600 Da | Approved drugs | 안전성 데이터 보유 | IP 제약 | 이미 승인됨 |

---

# 2. Known Agonists (활성화제)

## 2.1 정의 및 분류

**Agonist (활성화제)**는 표적 수용체에 결합하여 수용체의 고유한 생물학적 반응을 유발하는 리간드이다.

### Agonist 분류

| 분류 | 정의 | 예시 |
|------|------|------|
| **Full Agonist** | 최대 반응 유발 (100% efficacy) | GLP-1 analogs |
| **Partial Agonist** | 최대 반응 미달 (50-70% efficacy) | Aripiprazole |
| **Inverse Agonist** | 구성적 활성화 억제 | Nur77 modulators |
| **Allosteric Agonist** | 알로스테릭site 결합 | Benzodiazepines |

## 2.2 Known Agonists 예시 (疾태별)

### 표적: Nuclear Receptors

| 표적 | 약물명 | 개발단계 | 적응증 | EC50 | 비고 |
|------|--------|---------|--------|------|------|
| **ERRγ** | GSK4716 | Research | 대사 질환 | ~2 μM | Selective |
| **ERRγ** | DY131 | Research | 대사 질환 | ~0.5 μM | Potent |
| **ERRγ** | SLU-PP-332 | Preclinical | 비만, 심부전 | ~340 nM | Pan-ERR |
| **FXR** | Obeticholic acid | Approved (PBC) / Phase 3 (NASH) | PBC, NASH | ~45 nM | Semi-synthetic |
| **FXR** | GW4064 | Preclinical | NASH | ~100 nM | Non-steroidal |
| **PPARα** | Fenofibrate | Approved | 고지혈증 | ~30 μM | Fibrate |
| **PPARγ** | Pioglitazone | Approved | T2D | ~1 μM | TZD |
| **PPARδ** | GW501516 | Preclinical | 대사 증후군 | ~1 nM | Exercise mimetic |
| **GLP-1R** | Semaglutide | Approved | T2D, Obesity | ~10 pM | Peptide |
| **GDF15** | NGM386 | Phase 1 | Obesity | - | Novel |

### 표적: G-Protein Coupled Receptors (GPCRs)

| 표적 | 약물명 | 개발단계 | 적응증 | EC50 | 비고 |
|------|--------|---------|--------|------|------|
| **GLP-1R** | Exenatide | Approved | T2D | ~50 pM | GLP-1 analog |
| **GIPR** | Tirzepatide | Approved | T2D, Obesity | ~5 pM | Dual GIP/GLP-1 |
| **FGF21** | Pegbelfermin | Phase 2 | NASH | - | FGF21 analog |
| **β3-AR** | Mirabegron | Approved | Overactive bladder | ~50 nM | Bladder, BAT |

### 표적: Enzyme Receptors

| 표적 | 약물명 | 개발단계 | 적응증 | EC50 | 비고 |
|------|--------|---------|--------|------|------|
| **AMPK** | AICAR | Research | 대사 질환 | ~100 μM | AMP analog |
| **SIRT1** | Resveratrol | Research | 노화, 대사 | ~10 μM | Natural |
| **PGC-1α** | (indirect) | - | 미토콘드리아 | - | ERRγ via |

## 2.3 Agonist 개발 전략

```
Target Identification
        ↓
Lead Discovery (HTS, VLS)
        ↓
Scaffold Optimization
   ┌────┴────┐
   ↓         ↓
Full        Partial
Agonist     Agonist
   ↓         ↓
ADMET       Safety
Optimization  Profile
   ↓         ↓
Lead         Reformulation
Optimization
        ↓
Preclinical → Clinical
```

---

# 3. Known Inhibitors (억제제)

## 3.1 정의 및 분류

**Inhibitor (억제제)**는 효소 또는 수용체의活性を 억제하여 생물학적 반응을 감소시키는 화합물이다.

### Inhibitor 분류

| 분류 | 작용 기전 | 예시 |
|------|----------|------|
| **Competitive** | 기질과 결합 부위 경쟁 | Sitagliptin |
| **Non-competitive** | 알로스테릭 억제 | Allopurinol |
| **Irreversible** | 공유결합에 의한 영구적 억제 | Omeprazole |
| **Allosteric** | 알로스테릭site 결합 | Regorafenib |
| **Covalent** | 효소와 공유결합 형성 | Afatinib |

## 3.2 Known Inhibitors 예시

### 표적: Kinases

| 표적 | 약물명 | 개발단계 | 적응증 | IC50 | 비고 |
|------|--------|---------|--------|------|------|
| **LOXL2** | Simtuzumab | Phase 2 | NASH, IPF | ~50 nM | Antibody (failed) |
| **LOXL2** | (Small molecules) | Discovery | Fibrosis | TBD | Opportunity! |
| **ASK1** | Selonsertib | Phase 3 (failed) | NASH, DME | ~10 nM | - |
| **CCR2/5** | Cenicriviroc | Phase 2 | NASH | ~10 nM | Dual antagonist |
| **FGFR** | Pemigatinib | Approved | Cholangiocarcinoma | ~0.4 nM | Selective |
| **PI3Kδ** | Idelalisib | Approved | CLL | ~0.5 nM | Cancer |

### 표적: Nuclear Receptors

| 표적 | 약물명 | 개발단계 | 적응증 | IC50 | 비고 |
|------|--------|---------|--------|------|------|
| **FXR** (Antagonist) | Guggulsterone | Research | Cholestasis | ~10 μM | Natural |
| **PPARγ** (Antagonist) | T0070907 | Research | Cancer | ~10 nM | Selective |
| **LXR** (Agonist) | T0901317 | Research | Atherosclerosis | ~20 nM | Side effects |

### 표적: Metabolic Enzymes

| 표적 | 약물명 | 개발단계 | 적응증 | IC50 | 비고 |
|------|--------|---------|--------|------|------|
| **ACC** | Firsocostat | Phase 2 | NASH | ~10 nM | ACC1/2 |
| **FASN** | TVB-2640 | Phase 2 | NASH | ~100 nM | FASN |
| **SCD1** | Aramchol | Phase 3 | NASH | ~1 μM | Stearoyl-CoA |
| **DGAT2** | Pululdenser | Phase 1 | NASH | ~10 nM | - |

## 3.3 Inhibitor 개발 전략

```
Target Validation
        ↓
Assay Development (Biochemical/Cellular)
        ↓
Lead Identification (HTS/Fragment)
        ↓
Hit-to-Lead Optimization
   ├── Potency (IC50/Selectivity)
   ├── ADMET
   └── PK/PD
        ↓
Lead Optimization
        ↓
Preclinical Safety (Safety pharmacology, Tox)
        ↓
IND Filing → Clinical
```

---

# 4. Natural Compounds (천연물)

## 4.1 정의 및 특징

**Natural Compounds (천연물)**는 식물, 미생물, 동물 등의 자연계에서 유래한 생리활성 물질이다.

### 천연물의 장점

| 장점 | 설명 |
|------|------|
| **다표적 작용** | 하나의 천연물이 여러 표적에 작용 가능 |
| **안전성 프로파일** | 수천 년간 사용 历史 (한약 등) |
| **구조적 다양성** | 인공 화합물보다 복잡한 구조 |
| **효능** | 약리활성 우수 |

### 천연물의 단점

| 단점 | 설명 |
|------|------|
| **순도 문제** | 추출물은 복작한 혼합물 |
| **흡수 문제** | 생체이용률 낮음 |
| **표준화** | 배치 간 차이 |
| **특정 표적** | 정확한 작용 기전 불분명 |

## 4.2 천연물 예시 (질병별)

### 대사 질환

| 천연물 | 원천 | 표적/기전 | 효능 | 개발단계 |
|--------|------|----------|------|---------|
| **Berberine** | 황련 (Coptis chinensis) | AMPK ↑, mtDNA ↑ | HbA1c ↓ 0.7% | Phase 2/3 |
| **Resveratrol** | 포도 껍질 | SIRT1 ↑, PGC-1α ↑ | 대사 개선 | Research |
| **Curcumin** | 강황 (Curcuma longa) | NF-κB ↓, AMPK ↑ | 항염증 | Phase 2 |
| **Quercetin** | 과일/채소 | AMPK ↑, Senolytic | 노화 방지 | Research |
| **Epigallocatechin gallate** | 녹차 | AMPK ↑,脂肪分解 ↑ | 체중 ↓ | Research |
| **Silymarin** | 밀国际市场 | Antioxidant, Anti-fibrotic | 간 보호 | Approved (유럽) |
| **Ursolic acid** | 사과의 껍질 | AMPK ↑, PGC-1α ↑ | 근육 보전 | Research |
| **Oleanolic acid** | 올리브 잎 | AMPK ↑, Antioxidant | 간 보호 | Research |

### 염증/섬유화

| 천연물 | 원천 | 표적/기전 | 효능 | 개발단계 |
|--------|------|----------|------|---------|
| **Epicatechin** | 카카오, 녹차 | NRF2 ↑, Mitochondrial ↑ | 근육 보전 | Phase 2 |
| **Withaferin A** | 인도人参 | NF-κB ↓, HSC ↓ | 항섬유화 | Preclinical |
| **Salidroside** | 홍경천 | AMPK ↑, HIF-1α ↑ | 항산화 | Research |
| **Ginsenoside Rb1** | 인삼 | AMPK ↑, Glucose uptake ↑ | 대사 개선 | Research |

### 심혈관 질환

| 천연물 | 원천 | 표적/기전 | 효능 | 개발단계 |
|--------|------|----------|------|---------|
| **Danhong injection** | 당귀/단극 | 혈액순환 개선 | 허혈 보호 | Approved (중국) |
| **Salvianolic acid B** | 삼레근 | Antioxidant, Anti-platelet | 혈관 보호 | Phase 2 |
| **Notoginsenoside R1** | 삼칠 | 혈액순환 개선 | 혈관 확장 | Research |

## 4.3 천연물 기반 약물 개발

```
Natural Product Library
        ↓
Bioactivity Screening
   ├── Phenotypic screening
   └── Target-based screening
        ↓
Active Compound Identification
   ├── Bioassay-guided fractionation
   └── Dereplication
        ↓
Structure Elucidation
   ├── NMR
   ├── MS
   └── X-ray crystallography
        ↓
Lead Optimization
   ├── SAR studies
   └── ADMET improvement
        ↓
Semi-synthetic derivatives
   └── Improved potency/solubility
```

---

# 5. Small Molecules (저분자 화합물)

## 5.1 정의

**Small Molecules (저분자 화합물)**은 분자량 100-500 Da 범위의 합성 또는 천연 화합물로, 세포막을 투과하여 세포 내 표적에 도달할 수 있다.

### 저분자 화합물 특성

| 특성 | 범위 |
|------|------|
| 분자량 (MW) | 100-500 Da |
| LogP | 1-5 |
| H-bond donors | ≤5 |
| H-bond acceptors | ≤10 |
| TPSA | ≤140 Å² |

## 5.2 저분자 화합물 예시

### Synthetic FXR Agonists

| 약물명 | 구조유형 | IC50/EC50 | 개발단계 | 특징 |
|--------|---------|----------|---------|------|
| **Obeticholic acid (INT-747)** | Bile acid derivative | ~45 nM | Approved (PBC), Phase 3 (NASH) | Semi-synthetic CDCA |
| **Cilofexor (GS-9674)** | Non-steroidal | ~30 nM | Phase 2 | NASH, PSC |
| **Tropifexor (LJN452)** | Non-steroidal | ~10 nM | Phase 2 | Gut-restricted |
| **EDP-305** | Non-steroidal | ~20 nM | Phase 2 | NASH, PBC |
| **MET409** | Non-steroidal | ~5 nM | Phase 2 | Gut-restricted |
| **GW4064** | Isoxazole | ~100 nM | Preclinical | Research tool |

### Synthetic PPAR Modulators

| 약물명 | 구조유형 | 선택성 | 개발단계 | 특징 |
|--------|---------|--------|---------|------|
| **Lanifibranor** | Thiazole-dione | Pan-PPAR | Phase 3 | NASH (NATiV3) |
| **Pioglitazone** | TZD | PPARγ | Approved | T2D, NASH |
| **Elafibranor (GFT505)** | TZD | PPARα/δ | Phase 3 (failed) | NASH |
| **Seladelpar (MBX-8025)** | TZD | PPARδ | Phase 2 | PBC, NASH |

### Metabolic Enzyme Inhibitors

| 약물명 | 표적 | IC50 | 개발단계 | 적응증 |
|--------|------|------|---------|--------|
| **Firsocostat (GS-0976)** | ACC1/2 | ~10 nM | Phase 2 | NASH |
| **Aramchol (ARABIC)** | SCD1 | ~1 μM | Phase 3 | NASH |
| **TVB-2640 (FASN)** | FASN | ~100 nM | Phase 2 | NASH, Cancer |
| **Pululdenser** | DGAT2 | ~10 nM | Phase 1 | NASH |

## 5.3 저분자 약물 개발 프로세스

```
Target Identification & Validation
        ↓
Hit Generation
   ├── High-Throughput Screening (HTS)
   ├── Virtual Screening (VS)
   └── Fragment-Based Drug Design (FBDD)
        ↓
Hit-to-Lead (H2L)
   ├── SAR optimization
   ├── Lead identification
   └── Early ADMET assessment
        ↓
Lead Optimization
   ├── Potency (IC50, Ki)
   ├── Selectivity profiling
   ├── PK/PD optimization
   └── Safety assessment
        ↓
Preclinical Development
   ├── In vivo efficacy (animal models)
   ├── Safety pharmacology
   ├── Toxicology (GLP)
   └── Pharmaceutical developability
        ↓
IND/NDA Filing
```

---

# 6. Peptides (펩타이드)

## 6.1 정의 및 특징

**Peptides (펩타이드)**는 아미노산 2-50개로 구성된 짧은 사슬로서, 높은 선택성과 효능을 가진다.

### 펩타이드의 장점

| 장점 | 설명 |
|------|------|
| **높은 선택성** | 표적에 대한 특이적 결합 |
| **높은 효능** | 낮은 농도에서 효과적 |
| **생체적합성** | 천연 아미노산으로 구성 |
| **다양한 기능** |agonist, antagonist, inhibitor |

### 펩타이드의 단점

| 단점 | 설명 |
|------|------|
| **Proteolytic instability** | 체내 분해로 인한 짧은 반감기 |
| **낮은 세포 투과성** | 세포막 통과 제한 |
| **신경 glut** | 위장관 투과 어려움 |
| **제형 어려움** | 안정성 문제 |

## 6.2 펩타이드 예시

### Metabolic Disease Peptides

| 펩타이드 | 시퀀스/유형 | 표적 | 개발단계 | 특징 |
|---------|-----------|------|---------|------|
| **GLP-1 (7-37)** | 31 aa | GLP-1R | Approved (analogs) | T2D, Obesity |
| **Semaglutide** | GLP-1 analog | GLP-1R | Approved | T2D, Obesity (oral!) |
| **Tirzepatide** | Dual GIP/GLP-1 | GIPR/GLP-1R | Approved | T2D, Obesity |
| **Exenatide** | GLP-1 analog | GLP-1R | Approved | T2D |
| **Liraglutide** | GLP-1 analog | GLP-1R | Approved | T2D, Obesity |
| **Setmelanotide** | MC4R agonist | MC4R | Approved | Rare obesity |
| **Apraglutide** | GLP-2 analog | GLP-2R | Phase 2 | SBS |

### Fibrosis Peptides

| 펩타이드 | 시퀀스/유형 | 표적 | 개발단계 | 특징 |
|---------|-----------|------|---------|------|
| **BPM 31510** | Ubiquinol analog | Metabolism | Phase 1/2 | Cancer, Fibrosis |
| **Pirfenidone** | Small molecule | TGF-β ↓ | Approved | IPF |
| **NGM386** | FGF21 analog | FGFR1c | Phase 1 | NASH, Obesity |

### Novel Peptides (Research)

| 펩타이드 | 기원 | 표적 | 효능 | 개발단계 |
|---------|------|------|------|---------|
| **Catestatin** | Chromogranin A | Nicotinic receptor | 혈압 조절 | Research |
| **Humanin** | Mitochondrial | Various | 세포 보호 | Research |
| **MOTS-c** | Mitochondrial | AMPK ↑ | 대사 개선 | Research |
| **Adropin** | Energy homeostasis | GPR19 | 대사 조절 | Research |

## 6.3 펩타이드 개발 전략

```
Native Peptide or De Novo Design
        ↓
Stability Enhancement
   ├── D-amino acids
   ├── Stapled peptides
   ├── Cyclization
   └── PEGylation
        ↓
Delivery Optimization
   ├── Oral formulation (新兴)
   ├── Transdermal
   └── Subcutaneous depot
        ↓
PK/PD Optimization
   ├── Half-life extension
   └── Target selectivity
        ↓
Manufacturing Scale-up
   ├── Solid-phase synthesis
   └── Recombinant expression
        ↓
Preclinical → Clinical
```

---

# 7. De Novo Designed Candidates

## 7.1 정의

**De Novo Designed Candidates**는 전산 설계 및人工智能을 활용하여 처음부터 새로設計된 분자이다.

### 설계 전략

| 전략 | 설명 | 도구 |
|------|------|------|
| **Structure-based** | 표적 구조 기반 설계 | AutoDock, Glide |
| **Ligand-based** | 리간드 기반 설계 | Pharmacophore modeling |
| **AI-based** | 딥러닝 기반 생성 | GANs, VAEs, LLMs |
| **Fragment-based** | 프래그먼트 조합 | SAR by NMR |

## 7.2 De Novo 설계 도구

| 도구 | 방법 | 적용 |
|------|------|------|
| **AutoDock Vina** | 구조기반 VLS | Docking |
| **MolArt** | 분자 그래프 생성 | Scaffold hopping |
| **GraphN** | Graph NN 기반 | Molecular generation |
| **REINVENT 4** | RL 기반 생성 | Lead optimization |
| **Syntaurus** | VLS + generation | Multi-objective |
| **PMDM** | Property-guided | ADMET optimization |

## 7.3 De Novo 후보 예시

### AI-Designed Molecules

| 분자명 | 설계 방법 | 표적 | 효능 | 개발단계 |
|--------|---------|------|------|---------|
| **ISM001-055** | PandaPast + synthesis | DDR1 | Anti-fibrotic | Phase 1 |
| **Various** | Multi-objective RL | SARS-CoV-2 | Antiviral | Discovery |
| **Generated** | Graph NN | KRAS G12D | Anti-cancer | Discovery |

### De Novo Peptides

| 분자명 | 설계 방법 | 표적 | 효능 | 개발단계 |
|--------|---------|------|------|---------|
| **Stapled peptides** | Stapled α-helix | MCL-1, BCL-2 | Apoptosis | Clinical |
| **Macrocyclic peptides** | mRNA display | Various | High selectivity | Preclinical |
| **Designed repeat proteins** | ARMMS | TNF-α | Anti-inflammatory | Preclinical |

## 7.4 De Novo 설계 프로세스

```
Target Structure/Pharmacophore
        ↓
Design Strategy Selection
   ┌─────────┼─────────┐
   ↓         ↓         ↓
Structure  Ligand    AI/ML
Based      Based     Based
   ↓         ↓         ↓
   └─────────┼─────────┘
            ↓
Virtual Screening / Evaluation
   ├── Docking scores
   ├── ADMET prediction
   └── synthesizability
            ↓
Synthesis Planning
   └── Retrosynthetic analysis
            ↓
Synthesis & Testing
   ├── In vitro assay
   └── In vivo validation
            ↓
Iterative Optimization (loop)
```

---

# 8. Drug Repositioning Candidates

## 8.1 정의

**Drug Repositioning (약물 재배치)**는 이미 승인된 약물을 새로운 적응증에 적용하는 전략이다.

### Repositioning 전략

| 전략 | 설명 | 예시 |
|------|------|------|
| **Indication expansion** | 동일 기전의 새로운 적응증 | Sildenafil (angina → ED → PAH) |
| **Mechanism-based** | 새로운 기전 발견 | Thalidomide (sedation → leprosy → myeloma) |
| **Pathway-based** | 공유 경로 활용 | Metformin (diabetes → longevity) |
| **Phenotypic** | 표현형 기반 | Minoxidil (blood pressure → hair growth) |

## 8.2 Repositioning候蔔 예시 (대사/간 질환)

| 약물명 | 원래 적응증 | 새로운 적응증 | 기전 | 개발단계 |
|--------|-----------|------------|------|---------|
| **Metformin** | T2D | NASH, longevity | AMPK ↑, mTOR ↓ | Phase 2/3 |
| **SGLT2 inhibitors** | T2D | Heart failure, CKD, NASH | Glucose excretion | Phase 3 |
| **GLP-1 RAs** | T2D, Obesity | MASH, CVD | Weight loss, metabolic | Phase 3 |
| **Statins** | 고지혈증 | NASH | Lipid lowering, anti-inflammatory | Phase 2 |
| **Telmisartan** | Hypertension | NASH | PPARγ activation | Phase 2 |
| **Carvedilol** | Hypertension | Variceal bleeding | β-blocker + vasodilation | Approved |
| **Pentoxifylline** | Intermittent claudication | Alcoholic hepatitis | TNF-α inhibition | Research |
| **Aspirin** | Pain, CVD | CRC prevention | COX inhibition | Phase 3 |
| **Vitamin E** | Deficiency | NASH | Antioxidant | Phase 3 |
| **Obeticholic acid** | PBC | NASH | FXR activation | Phase 3 |

### 다른 질환領域의 repositioning

| 약물명 | 원래 적응증 | 새로운 적응증 | 기전 |
|--------|-----------|------------|------|
| **Baricitinib** | Rheumatoid arthritis | Alopecia areata | JAK inhibitor |
| **Rapamycin** | Transplant rejection | Longevity, anti-aging | mTOR inhibition |
| **Semaglutide** | T2D | Obesity, MASH | GLP-1R agonism |
| **Liraglutide** | T2D | Pediatric obesity | GLP-1R agonism |
| **Sildenafil** | Angina | PAH, BPH | PDE5 inhibition |

## 8.3 Drug Repositioning 방법론

```
Existing Drug Database
   ├── Approved drugs (DrugBank, ChEMBL)
   ├── Clinical candidates
   └── Failed drug candidates
           ↓
Target/Indication Mapping
   ├── Computational (signature matching)
   ├── Network-based
   └── Literature-based
           ↓
Hypothesis Generation
   ├── Shared targets
   ├── Shared pathways
   └── Phenotypic similarity
           ↓
Validation
   ├── In vitro assay
   ├── In vivo model
   └── Clinical trial (Phase 2/3)
           ↓
Regulatory Strategy
   ├── 505(b)(1) - New drug
   ├── 505(b)(2) - Known drug, new use
   └── 505(j) - Generic
```

---

# 9. Comparative Analysis Matrix

## 9.1 약물 유형 비교

| 기준 | Agonists | Inhibitors | Natural | Small Mol | Peptides | De Novo | Repositioning |
|------|----------|-----------|---------|-----------|----------|---------|---------------|
| **개발기간** | 10-15년 | 10-15년 | 15-20년 | 10-15년 | 10-12년 | 5-10년 | 3-7년 |
| **비용** | 높음 | 높음 | 중간 | 높음 | 중간-높음 | 다양 | 낮음 |
| **성공률** | ~10% | ~10% | ~5% | ~10% | ~15% | 다양 | ~25% |
| **특이성** | 중간-높음 | 중간-높음 | 낮음-중간 | 중간-높음 | 높음 | 중간 | 중간 |
| **IP 가능성** | 낮음 | 낮음 | 낮음 | 중간 | 중간 | 높음 | 낮음 |
| **생체이용률** | 중간-높음 | 중간-높음 | 낮음 | 높음 | 낮음 | 중간-높음 | 중간 |
| **표적 접근성** | Excellent | Excellent | Moderate | Excellent | Good | Excellent | Good |

## 9.2 치료 영역별 적합성

| 치료 영역 | 최적 유형 | 이유 |
|---------|----------|------|
| **대사 질환** | Agonists, Peptides | 호르몬 경로 모방 |
| **섬유화** | Inhibitors, Natural | 염증/세포增殖 억제 |
| **종양** | Inhibitors, Peptides | 세포사멸 유도, 표적 |
| **염증** | Inhibitors, Natural | 사이토카인 억제 |
| **심혈관** | Small Mol, Repositioning | 만성 투여, 비용 효율 |
| **신경퇴행** | Small Mol, Peptides | BBB 침투, 선택성 |

## 9.3 개발 리스크 비교

| 유형 | 주요 리스크 | 완화 전략 |
|------|----------|----------|
| **Agonists** | 과활성화, 내성 | partial agonist, combination |
| **Inhibitors** | 보상 경로 활성화 | 선택적 억제, combination |
| **Natural** | 품질变异, 낮은 potency | 표준화, 합성 유사체 |
| **Small Mol** | 독성, drug-drug interactions | 구조-독성 관계, DDI screening |
| **Peptides** | proteolytic instability | 안정화, 주사 제형 |
| **De Novo** | synthesizability, novelty | 계산적 평가,创新 |
| **Repositioning** | IP, dose optimization | 505(b)(2),_phase 2 trial |

---

# 10. Therapeutic Ranking & Recommendations

## 10.1 표적별 최적 치료제 유형

| 표적 | 최적 유형 | Rank 1 | Rank 2 | Rank 3 |
|------|----------|--------|--------|--------|
| **ERRγ** | Agonist | SLU-PP-332 (Pan-ERR) | GSK4716 (Selective) | DY131 |
| **FXR** | Agonist | OCA (Approved) | Cilofexor (Phase 2) | Tropifexor (Phase 2) |
| **PPARs** | Agonist | Lanifibranor (Phase 3) | Pioglitazone (Approved) | Elafibranor (Failed) |
| **GLP-1R** | Peptide | Semaglutide (Oral) | Tirzepatide (Dual) | Exenatide |
| **LOXL2** | Inhibitor | Small molecules (Opportunity!) | - | - |
| **AMPK** | Activator (indirect) | Metformin (Repositioning) | AICAR (Research) | Berberine (Natural) |
| **SGLT2** | Inhibitor | Empagliflozin (Approved) | Dapagliflozin (Approved) | Canagliflozin |
| **FGF21** | Peptide analog | Pegbelfermin (Phase 2) | - | - |

## 10.2 개발 우선순위 매트릭스

```
                    │
  높은 영향          │
      │         ┌───┴───┐\n      │         │  ★1   │\n      │         │  OCA   │\n      │         │ Lanifib│\n      │         │Semaglu │\n      │         └───────┘\n      │              │\n      │              │\n      └──────────────┴────────────────────
                    낮음      영향       높음
                            │
                      ┌─────┴─────┐\n                      │  ★3       │\n                      │ Reposition │\n                      │  Natural   │\n                      └───────────┘\n                            │
                      ┌─────┴─────┐\n                      │  ★2       │\n                      │ De Novo    │\n                      │ Small Mol  │\n                      └───────────┘\n                            │
                      낮음        │\n                           복잡성\n```

## 10.3 추천 개발 전략

### 전략 A: 기존 약물 개량 (Risk-Averse)

```
1. Repositioning candidates 확인
   └── Metformin, SGLT2i, GLP-1 RAs
   
2. Natural compounds 기반
   └── Berberine, Resveratrol, Epicatechin
   
3. Bioavailability 향상
   └── Cocrystal, formulation optimization
```

### 전략 B: 혁신적 신규 개발 (High Reward)

```
1. De Novo design (AI-assisted)
   └── REINVENT 4, fragment-based
   
2. Novel targets
   └── LOXL2 small molecules
   
3. Multi-target approach
   └── Pan-PPAR, dual agonists
```

### 전략 C: 최優先 표적 조합

| 순위 | 표적 | 약물 유형 | 권장 후보 |
|------|------|---------|---------|
| 1 | **FXR** | Small Mol | OCA, Cilofexor |
| 2 | **PPAR** | Pan agonist | Lanifibranor |
| 3 | **GLP-1R** | Peptide | Semaglutide, Tirzepatide |
| 4 | **SGLT2** | Small Mol | Empagliflozin |
| 5 | **ERRγ** | Agonist | SLU-PP-332 (Preclinical) |
| 6 | **LOXL2** | Inhibitor | (Opportunity!) |

---

## 참고 문헌 (References)

1. FDA. Novel Drug Approvals 2023-2026.
2. Deore et al. "Comprehensive Review on Drug Repositioning" (2024).
3. Blundell et al. "De novo molecular design" *Nature* (2024).
4. Tamboli et al. "Natural products in metabolic disease" *Pharmacological Research* (2023).
5. Various clinical trial data from ClinicalTrials.gov.

---

*본 템플릿 작성일: 2026-04-19*
*ARP v24 Drug Discovery Framework*
*Classification: Internal Research Use*
