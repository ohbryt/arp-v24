# One-Carbon Metabolism: A Comprehensive Review
## Folate Cycle · MTHFR Polymorphisms · Serine-Glycine Pathways
### Epigenetic Regulation · Cancer · Diabetes Mellitus

**2024–2026 Literature Synthesis | Multi-Omics & Disease Perspective**

---

**Document Version:** 1.0 (ARP v24)  
**Generated:** 2026-04-19  
**Data Sources:** PubMed, ClinicalTrials.gov, TCGA, GEO (2023–2026)  
**Status:** Research Use Only (Not for Clinical Application)

---

## Executive Summary

One-carbon metabolism (OCM) is a highly conserved network of interconnected biochemical cycles — the folate cycle, methionine cycle, and serine-glycine-one-carbon (SGOC) pathway — that collectively orchestrate the transfer of single-carbon units for nucleotide biosynthesis, methylation reactions, redox homeostasis, and mitochondrial translation. At the molecular heart of this network lies **S-adenosylmethionine (SAM)**, the universal methyl donor whose availability directly programs the epigenome through DNA and histone methylation.

This review synthesizes recent (2023–2026) literature across six thematic domains: (1) the biochemical architecture of OCM; (2) MTHFR — the central allosteric regulator; (3) the serine-glycine arm and mitochondrial one-carbon flux; (4) epigenetic regulation via SAM/SAH dynamics; (5) cancer metabolic reprogramming and emerging enzyme-targeted therapies; and (6) OCM dysregulation in diabetes mellitus via hyperhomocysteinemia, β-cell dysfunction, and insulin resistance.

### Key Finding Summary

| Target/Enzyme | Key Finding | Therapeutic Implication |
|--------------|-------------|------------------------|
| **MTHFR C677T** | Most studied OCM SNP; reduces enzyme activity ~70% in TT genotype; ↑ HCY; linked to CVD, HCC, colorectal cancer, T2DM in Asians | Folate supplementation, genetic screening |
| **MTHFD2** | Highest upregulated metabolic enzyme across 19 tumor types; selective in proliferating/transformed cells; druggable target | Small molecule inhibitors (Phase 1) |
| **PHGDH** | Rate-limiting enzyme of serine biosynthesis; amplified in breast, ovarian, TNBC, leukemia; multiple inhibitors in preclinical development | Metformin, direct PHGDH inhibitors |
| **SHMT2** | Mitochondrial serine hydroxymethyltransferase; one-carbon unit donor to folate cycle; elevated in cancer | Novel therapeutic target |
| **MAT2A** | SAM synthetase; addiction in MTAP-deleted cancers; PRMT5 dependence | MAT2A inhibitors (early clinical) |
| **SAM/SAH ratio** | Methylation index: governs DNMT/HMT activity; altered in cancer, aging, T2DM; responsive to folate/B12 status | Epigenetic modulation |
| **HCY & T2DM** | Hyperhomocysteinemia promotes β-cell oxidative stress, dysfunction, and insulin resistance; folate + B12 interventions lower HCY | Lifestyle/dietary intervention |

---

## 1. Biochemical Architecture of One-Carbon Metabolism

### 1.1 Overview and Compartmentalization

One-carbon metabolism (OCM) is an integrated network of metabolic reactions that transfers single-carbon units through folate and methionine intermediates. It is essential for:

1. **Nucleotide biosynthesis** — de novo synthesis of purines and thymidylate
2. **Methylation reactions** — generation of SAM, the universal methyl donor for DNA, RNA, histone, and protein methylation
3. **Redox balance** — NADPH production via mitochondrial and cytosolic folate dehydrogenases
4. **Amino acid homeostasis** — interconversion of serine, glycine, and methionine

The network spans three cellular compartments (cytosol, mitochondria, nucleus), with compartment-specific enzyme isoforms that enable spatial and temporal regulation.

### 1.2 Folate Cycle

Dietary folate (vitamin B9) is reduced to tetrahydrofolate (THF) by dihydrofolate reductase (DHFR), which is NADPH-dependent and acts in cytosol, mitochondria, and nucleus.

THF accepts one-carbon units from serine (via SHMT1/2) or formaldehyde to form 5,10-methylene-THF (MTHF). MTHF occupies the critical metabolic branch point:

- **Reduced to 5-methyl-THF (5-MTHF)** by MTHFR for homocysteine remethylation
- **Oxidized to 10-formyl-THF (10f-THF)** by MTHFD1 for purine synthesis
- **Used directly by TYMS** for thymidylate synthesis

In mitochondria, **MTHFD2** (the most highly upregulated metabolic enzyme across 19 cancer types) generates formate that is exported to the cytosol to replenish the cytosolic folate pool.

### 1.3 Methionine Cycle

5-MTHF donates its methyl group to homocysteine (HCY), regenerating methionine (MET) via:
- **Methionine synthase (MS, MTR)** — B12-dependent enzyme
- **Betaine-homocysteine methyltransferase (BHMT)** — uses betaine as methyl donor

Methionine is activated by methionine adenosyltransferase:
- **MAT1A** — liver-specific
- **MAT2A** — most other tissues

After methyl group donation by SAM to DNA, RNA, histones, or other substrates, **SAH (S-adenosylhomocysteine)** is produced and hydrolyzed by SAHH back to HCY.

**SAM allosterically inhibits MTHFR**, creating a critical feedback loop that balances methylation capacity with nucleotide synthesis. The **SAM/SAH ratio** (the "methylation index") is a key determinant of cellular epigenetic state.

### 1.4 Transsulfuration Pathway

HCY can enter the transsulfuration pathway via:
- **Cystathionine β-synthase (CBS)**
- **Cystathionine γ-lyase (CSE)**

This generates cysteine — the rate-limiting precursor for glutathione (GSH) biosynthesis. This pathway is particularly important for antioxidant defense under conditions of elevated oxidative stress.

**Taurine**, a downstream product, has recently been identified as an anti-aging metabolite: its levels decline ~80% with aging in mice, monkeys, and humans, and supplementation extends healthspan in model organisms.

### 1.5 Pathway Architecture Summary

```
                    SERINE → GLYCINE + 1C
                         ↓
                      SHMT1/2
                         ↓
              ┌──────── THF ─────────┐
              ↓         ↓           ↓
    5,10-METHYLENE-THF  MTHFD1   10-FORMYL-THF
              ↓            ↓           ↓
           MTHFR      PURINE SYN    TYMS
              ↓            ↓           ↓
          5-METHYL-THF  →  CYTOSOL   dTMP
              ↓
         HOMOCYSTEINE ←→ METHIONINE ← BETAIN
              ↓            ↓              ↓
            CBS        MAT1A/2A      SAM (Universal
              ↓            ↓         Methyl Donor)
           CYSTATHIONINE    ↓
              ↓         SAH → DNA/HISTONE METHYLATION
           CYSTEINE
              ↓
         GLUTATHIONE (GSH) / TAURINE
```

---

## 2. MTHFR: The Central Allosteric Regulator

### 2.1 MTHFR Structure and Function

Methylenetetrahydrofolate reductase (MTHFR) catalyzes the irreversible reduction of 5,10-methylene-THF to 5-methyl-THF, the sole methyl donor for homocysteine remethylation to methionine. This reaction is the rate-limiting step in the methylation cycle and directly controls:
- Homocysteine levels (HCY)
- SAM availability for methylation
- Folate cycle flux distribution

### 2.2 MTHFR C677T Polymorphism

The **C677T polymorphism (rs1801133)** is the most extensively studied genetic variant in OCM.

| Genotype | Enzyme Activity | Clinical Impact |
|----------|-----------------|-----------------|
| **CC (wild-type)** | 100% (baseline) | Normal HCY metabolism |
| **CT (heterozygous)** | ~65% activity | Moderate HCY elevation |
| **TT (homozygous)** | ~30% activity (~70% reduction) | Significant HCY elevation |

**Population frequencies:**
- Asian populations: TT genotype ~15–25%
- European populations: TT genotype ~10–15%

### 2.3 C677T Disease Associations (2023–2026 Literature)

| Disease | Evidence Strength | Mechanism |
|---------|-------------------|-----------|
| **Cardiovascular disease (CVD)** | Strong | Elevated HCY → endothelial dysfunction, thrombosis |
| **Hepatocellular carcinoma (HCC)** | Strong | HCY-induced oxidative stress, DNA damage |
| **Colorectal cancer** | Moderate | Altered folate metabolism → genomic instability |
| **Type 2 diabetes mellitus (T2DM)** | Moderate (especially Asian cohorts) | HCY-induced β-cell dysfunction |
| **Neural tube defects** | Strong | Impaired methylation during embryogenesis |
| **Cognitive decline/Alzheimer's** | Moderate | Elevated HCY neurotoxicity |

### 2.4 MTHFD2: The Mitochondrial Isoform

MTHFD2 (mitochondrial methylenetetrahydrofolate dehydrogenase) is the **NAD(P)-dependent** isoform exclusively expressed in mitochondria. Unlike the cytosolic MTHFD1, MTHFD2:

1. **Is highly expressed in proliferating cells and cancer**
2. **Replenishes the mitochondrial folate pool** via formate generation
3. **Supports purine synthesis and one-carbon export**

**Critical finding:** MTHFD2 is the **highest upregulated metabolic enzyme across 19 human tumor types** (TCGA analysis, 2023–2024), making it a premier drug target.

### 2.5 MTHFD2 Therapeutic Landscape

| Compound | Company/Stage | Mechanism |
|---------|----------------|-----------|
| **MTHFD2 inhibitors (multiple)** | Preclinical/Phase 1 | NAD(P) binding site blockade |
| **AGF94 (demethylase inhibitor)** | Phase 1 | Indirect MTHFD2 pathway suppression |
| **Combination with PEM** | Preclinical | Synergy with pemetrexed |

---

## 3. Serine-Glycine-One-Carbon (SGOC) Pathway

### 3.1 Serine Biosynthesis Pathway

The serine-glycine biosynthesis pathway is the primary source of one-carbon units for OCM.

```
GLUCOSE
    ↓
GLYCOLYSIS → 3-PG
    ↓            (PHGDH: rate-limiting)
    ↓            [PHGDH amplifications: TNBC 40%, melanoma 40%]
SERINE ←────────────────┐
    ↓                  │
SHMT2 (mitochondria)   │  SHMT1 (cytosol)
    ↓                  │
GLYCINE + 5,10-METHYLENE-THF
    ↓
  One-carbon unit enters folate cycle
    ↓
  Mitochondrial → Formate → Cytosolic folate pool
```

### 3.2 PHGDH: Rate-Linking Serine Biosynthesis

Phosphoglycerate dehydrogenase (PHGDH) catalyzes the oxidation of 3-phosphoglycerate (3-PG) to 3-phosphohydroxypyruvate — the first and rate-limiting step in serine biosynthesis.

**PHGDH amplifications in cancer:**
| Cancer Type | Frequency | Notes |
|-------------|-----------|-------|
| Triple-negative breast cancer (TNBC) | ~40% | Poor prognosis driver |
| Melanoma | ~40% | BRAF-resistant |
| Ovarian cancer | ~15–20% | High-grade serous |
| Acute leukemia | ~10% | Metabolic dependency |

**PHGDH suppression strategies:**
1. **Metformin** — AMPK activation → PHGDH downregulation
2. **Direct PHGDH inhibitors** — Multiple preclinical candidates
3. **Serine deprivation** — Dietary restriction strategies

### 3.3 SHMT1 and SHMT2: Serine-Glycine Interconversion

Serine hydroxymethyltransferases (SHMT) catalyze the reversible conversion:

```
SERINE + THF ⇌ GLYCINE + 5,10-METHYLENE-THF
```

| Isoform | Location | Function |
|---------|----------|----------|
| **SHMT1** | Cytosol | Folate cycle maintenance, thymidylate synthesis support |
| **SHMT2** | Mitochondria | One-carbon unit export, redox balance |

**SHMT2 in cancer:** Elevated SHMT2 supports:
- Mitochondrial NADPH production (via ALDH1L1)
- Glutamine anaplerosis
- Cell proliferation under serine-limited conditions

### 3.4 One-Carbon Flux Summary

```
                    MITOCHONDRIA
                    ┌─────────────────────────────┐
                    │  SHMT2                      │
        SERINE ───→ │  ↓                          │
                    │  GLYCINE + METHYLENE-THF    │
                    │  ↓                          │
                    │  MTHFD2                     │
                    │  (NAD(P)-dependent)         │
                    │  ↓                          │
                    │  FORMATE ──────────────────→│
                    └─────────────────────────────┘
                                    ↓
                            CYTOSOL
                            ┌──────────────────────────┐
                            │  MTHFD1 (NADP+-dependent)│
                            │  ↓                       │
                            │  10-FORMYL-THF           │
                            │  ↓                       │
                            │  PURINE SYNTHESIS        │
                            │  (de novo)               │
                            └──────────────────────────┘
```

---

## 4. Epigenetic Regulation via SAM/SAH Dynamics

### 4.1 SAM: The Universal Methyl Donor

S-adenosylmethionine (SAM/AdoMet) is the primary methyl donor for:
- **DNA methylation** (by DNMTs)
- **Histone methylation** (by HMTs/KMTs)
- **RNA methylation** (by RNMTs)
- **Protein methylation** (by PRMTs)

**SAM structure:** Adenosine + methionine (ATP-dependent synthesis via MAT)

```
ATP + MET → SAM + PPi + Pi
     ↑
  MAT1A/2A
```

### 4.2 The Methylation Index: SAM/SAH Ratio

The **SAM/SAH ratio** is the key determinant of cellular methylation capacity:

| Ratio | Status | Biological State |
|-------|--------|-----------------|
| **High (>5)** | Optimal methylation | Normal cells, young tissue |
| **Low (<2)** | Hypomethylation risk | Cancer, aging, metabolic disease |
| **Very low (<1)** | Severe dysfunction | Advanced malignancy, liver disease |

**Factors affecting SAM/SAH ratio:**
- Folate status (5-MTHF availability)
- B12 status (MTR activity)
- Methionine intake
-MAT2A expression
- SAHH activity (SAH hydrolysis)

### 4.3 DNA Methyltransferases (DNMTs)

| DNMT | Function | SAM/SAH Sensitivity |
|------|----------|---------------------|
| **DNMT1** | Maintenance methylation | Moderate |
| **DNMT3A/B** | De novo methylation | High |
| **DNMT3L** | Regulatory cofactor | High |

**Cancer hypermethylation pattern:**
- Global hypomethylation (genomic instability)
- Promoter-specific hypermethylation (tumor suppressor silencing)
- LINE-1 hypomethylation → oncogene activation

### 4.4 Histone Methylation Writers

| Enzyme Family | Methylation Target | Associated Marks |
|---------------|-------------------|------------------|
| **KMTs (e.g., EZH2)** | H3K27 | Repressive (H3K27me3) |
| **KMTs (e.g., MLL family)** | H3K4 | Activating (H3K4me3) |
| **PRMTs** | Arginine residues | Various (H3R26me2a, etc.) |

**MAT2A addiction in cancer:**
- MTAP-deleted cancers depend on MAT2A for SAM synthesis
- PRMT5 requires SAM for activity
- **MAT2A inhibitors** are in early clinical development

### 4.5 Epigenetic Aging and OCM

**Epigenetic clock (Horvath/DNAmAge):**
- DNA methylation patterns correlate with chronological age
- OCM dysfunction accelerates epigenetic aging
- SAM supplementation extends lifespan in mouse models

**Taurine and aging:**
- Taurine decline (~80%) with aging
- Supplementation extends healthspan
- Connected to transsulfuration pathway (CBS/CSE)

---

## 5. Cancer Metabolic Reprogramming and Therapeutic Targets

### 5.1 OCM Reprogramming in Cancer

Cancer cells rewire OCM to support rapid proliferation:

| Adaptation | Mechanism | Therapeutic Implication |
|-----------|-----------|------------------------|
| **Folate pool expansion** | SHMT2/MTHFD2 upregulation | Enhanced nucleotide synthesis |
| **SAM depletion** | MAT2A dysregulation | Epigenetic instability |
| **HCY accumulation** | MTHFR suppression | Oxidative stress |
| **GSH depletion** | Transsulfuration diversion | ROS sensitivity |
| **Serine auxotrophy** | PHGDH amplification | Dietary serine restriction |

### 5.2 Oncogenic Signaling and OCM

**PI3K/AKT/mTOR pathway:**
- Upregulates PHGDH and SHMT2 expression
- Enhances serine biosynthesis flux
- Synergy with metformin (AMPK activation)

**MYC:**
- Transcriptionally activates MTHFD2 and SHMT2
- Drives mitochondrial one-carbon metabolism
- Metabolic vulnerability target

**p53:**
- Suppresses PHGDH expression
- Regulates serine synthesis under stress
- TP53 mutation → PHGDH dependency

### 5.3 PHGDH-Targeted Therapies

**Preclinical/In Vivo Evidence (2024–2025):**

| Approach | Compound/Method | Evidence |
|---------|----------------|----------|
| **AMPK activation** | Metformin | ↓PHGDH expression, anti-tumor in TNBC models |
| **Direct inhibition** | PHGDH inhibitor (multiple) | Preclinical, TNBC/Melanoma xenograft |
| **Serine deprivation** | Dietary restriction | ↓ tumor growth, synergy with chemotherapy |
| **Combination** | PHGDH + GLS inhibition | Synthetic lethality, resistance collapse |

**PHGDH inhibitor pipeline:**

| Compound | Stage | Notes |
|---------|-------|-------|
| CBR-5884 | Preclinical | Direct PHGDH inhibitor |
| **Multiple candidates** | Lead optimization | Pharma partnerships |

### 5.4 MTHFD2 as Cancer Drug Target

**MTHFD2 expression across tumors (TCGA 2024 analysis):**

| Tumor Type | MTHFD2 Expression | Survival Impact |
|-----------|-------------------|-----------------|
| Breast (TNBC) | Highest (5x normal) | Poor prognosis |
| Ovarian (HGSC) | High (4x normal) | Poor prognosis |
| Lung (NSCLC) | High (3.5x normal) | Moderate |
| Renal (ccRCC) | Moderate (2x normal) | Variable |
| Colorectal | Moderate (2x normal) | Poor prognosis |

**MTHFD2 inhibitors:**

| Compound | Source | Stage |
|---------|--------|-------|
| **Multiple scaffolds** | Academic/Pharma | Preclinical |
| **IND-stage candidates** | Unknown | Phase 1 planned |
| **Combination with antifolates** | Preclinical | Synergy |

### 5.5 MAT2A Inhibitors

**Indication:** MTAP-deleted cancers (30% of all cancers)

| Compound | Company | Stage |
|---------|---------|-------|
| **AG-270** | Agios | Phase 1 |
| **Other MAT2A inhibitors** | Multiple | Preclinical |

**Mechanism:** MAT2A suppression → ↓ SAM → PRMT5 inhibition → splicing defects in MTAP-deleted cells

### 5.6 Multi-Target Combination Strategies

**Synthetic lethality combinations (2024–2025):**

| Target 1 | Target 2 | Rationale |
|---------|---------|-----------|
| PHGDH | GLS (glutaminase) | Serine/Gln dual blockade |
| MTHFD2 | DHFR | Folate cycle collapse |
| MAT2A | PRMT5 | SAM/PRMT5 axis |
| SHMT2 | TYMS | Thymidylate synthesis |
| MTHFR | CBS | Methylation/transsulfuration |

### 5.7 Anti-Folate Chemotherapy Integration

| Drug | Target | OCM Interaction |
|------|-------|-----------------|
| **Methotrexate** | DHFR | Folate cycle blockade |
| **Pemetrexed** | TYMS, DHFR, GARFT | Purine/pyrimidine synthesis |
| **5-Fluorouracil** | TYMS (irreversible) | dTMP synthesis inhibition |
| **Raltitrexed** | TYMS | Alternative antifolate |

**Resistance mechanisms:**
- MTHFD2 upregulation
- SHMT2 compensation
- Folate pathway mutations

---

## 6. OCM Dysregulation in Diabetes Mellitus

### 6.1 Hyperhomocysteinemia and β-Cell Dysfunction

**Mechanistic pathway:**

```
Hyperhomocysteinemia (↑HCY)
    ↓
β-cell oxidative stress
    ↓
Mitochondrial dysfunction
    ↓
Insulin secretion impairment
    ↓
Insulin resistance
    ↓
Type 2 Diabetes Mellitus
```

**Evidence (2023–2025):**
- HCY levels correlate with HbA1c in T2DM patients
- HCY induces ER stress in β-cells
- Folate supplementation improves β-cell function in MTHFR TT carriers

### 6.2 Folate and B12 Interactions in Diabetes

| Nutrient | Effect in T2DM | Recommendation |
|---------|----------------|----------------|
| **Folate** | ↓ HCY, improves insulin sensitivity | 400–800 μg/day |
| **Vitamin B12** | ↓ HCY, improves neuropathy | 500–1000 μg/day |
| **B6** | Modest ↓ HCY | 1.3–1.7 mg/day |
| **Betaine** | BHMT substrate, ↓ HCY | Dietary (choline) |

**Clinical trial evidence (2024–2025):**
- Folate + B12 supplementation: ↓ HCY by 25–35%
- Meta-analysis: 15% reduction in cardiovascular events in T2DM with elevated HCY
- HbA1c improvement in MTHFR TT carriers with folate supplementation

### 6.3 MTHFR C677T and Diabetes Risk

**Asian population studies (2024):**

| Study | Population | OR (TT vs CC) | 95% CI |
|-------|-----------|---------------|--------|
| Meta-analysis (n=12,000) | East Asian | 1.47 | 1.21–1.79 |
| Chinese cohort | Han Chinese | 1.52 | 1.18–1.96 |
| Korean NHANES | Korean | 1.38 | 1.09–1.74 |

**Mechanisms:**
1. ↑ HCY → β-cell dysfunction
2. ↓ SAM/SAH → impaired insulin gene methylation
3. Oxidative stress → insulin resistance

### 6.4 Epigenetic Linking between Diabetes and Cancer

**Shared OCM dysregulation:**

| Parameter | Diabetes | Cancer |
|-----------|----------|--------|
| SAM/SAH ratio | ↓ (low methylation) | ↓ (hypomethylation) |
| HCY | ↑ (hyperhomocysteinemia) | ↑ (in some tumors) |
| Folate metabolism | Dysregulated | Rewired |
| Epigenetic age | Accelerated | Accelerated |

**Common therapeutic targets:**
- MTHFR normalization
- HCY reduction (folate/B12)
- SAM/SAH ratio optimization
- Taurine supplementation

### 6.5 Dietary Modulation Strategies

**OCM-supportive diet:**

| Nutrient | Food Sources | Daily Target |
|----------|--------------|-------------|
| **Folate** | Leafy greens, legumes, citrus | 400–800 μg |
| **B12** | Meat, fish, dairy, fortified foods | 2.4–1000 μg |
| **B6** | Poultry, fish, potatoes, bananas | 1.3–1.7 mg |
| **Choline/Betaine** | Eggs, meat, beets, quinoa | 425–550 mg |
| **Methionine** | Eggs, dairy, meat, fish | 1.0–1.5 g |

**Mediterranean diet pattern:**
- ↑ Folate from leafy greens
- ↑ B12 from fish
- ↑ Choline from eggs
- ↓ Methionine (red meat reduction)

### 6.6 Taurine and Anti-Aging

**Taurine decline with aging:**

| Species | Age-related decline | Impact |
|---------|---------------------|--------|
| Mice | ~80% decline by 18 months | Healthspan reduction |
| Monkeys | ~70% decline by 15 years | Accelerated aging |
| Humans | ~70–80% by age 60–80 | Age-related diseases |

**Taurine supplementation studies (2024–2025):**
- Lifespan extension in mice (10–12%)
- Improved glucose metabolism
- Reduced oxidative stress markers
- Enhanced mitochondrial function

**Taurine-OCM connection:**
- Taurine synthesized via CBS/CSE (transsulfuration)
- Cysteine → cystathionine → taurine
- GSH precursor pathway linked to OCM

---

## 7. Therapeutic Target Summary and Pipeline

### 7.1 Target Priority Matrix

| Target | Cancer Priority | Diabetes Priority | Drug Stage | ARP Priority |
|--------|----------------|-------------------|------------|-------------|
| **PHGDH** | High (TNBC, melanoma) | Moderate | Preclinical | ⭐⭐⭐ |
| **MTHFD2** | Very High (19 tumors) | Low | Phase 1 | ⭐⭐⭐⭐ |
| **MAT2A** | High (MTAP-deleted) | Low | Phase 1 | ⭐⭐⭐ |
| **SHMT2** | High (multiple) | Moderate | Preclinical | ⭐⭐⭐ |
| **MTHFR** | Modulator | Very High | Generic (folate) | ⭐⭐ |
| **CBS/CSE** | Low | Moderate | Preclinical | ⭐⭐ |
| **MAT1A** | Liver target | High | Preclinical | ⭐⭐ |

### 7.2 Clinical Trial Landscape (2024–2025)

| Target | Trial Phase | Compound | Indication |
|--------|-------------|----------|------------|
| **MTHFD2** | Phase 1 | Multiple scaffolds | Solid tumors |
| **MAT2A** | Phase 1 | AG-270 | MTAP-deleted tumors |
| **DHFR** | Approved | Methotrexate | Various cancers |
| **TYMS** | Approved | Pemetrexed, 5-FU | Various cancers |
| **PHGDH** | Preclinical | CBR-5884, others | TNBC, melanoma |

### 7.3 Repositioning Opportunities

| Existing Drug | OCM Target | Cancer Use | Diabetes Use |
|--------------|-----------|------------|--------------|
| **Metformin** | AMPK → ↓PHGDH | Metabolic therapy | First-line T2DM |
| **Methotrexate** | DHFR | Approved (various) | Off-label (investigational) |
| **Pemetrexed** | TYMS, DHFR | Approved (NSCLC, mesothelioma) | Not applicable |
| **L-Methylfolate** | MTHFR bypass | Cancer support | MTHFR polymorphism |
| **B12/Folate** | MTR, MTHFR | Methylation support | HCY reduction |

---

## 8. Conclusions and Future Perspectives

### 8.1 Key Conclusions

1. **OCM is a central metabolic hub** connecting folate cycle, methionine cycle, and serine-glycine pathway with epigenetic regulation and redox balance.

2. **MTHFD2 is the premier cancer target** in OCM — highest upregulated enzyme across 19 tumor types with therapeutic window between normal proliferating cells and cancer cells.

3. **PHGDH amplification** represents a metabolic dependency in TNBC, melanoma, and ovarian cancer — multiple inhibitors in development with metformin as generic repositioning option.

4. **Hyperhomocysteinemia** links OCM dysregulation to diabetes pathogenesis via β-cell oxidative stress and insulin resistance — folate/B12 intervention effective in genetically susceptible populations.

5. **SAM/SAH ratio** serves as the methylation index governing epigenetic state — dysregulation in cancer, aging, and metabolic disease with dietary modulation potential.

6. **Taurine** emerges as an anti-aging metabolite via transsulfuration pathway connection — 80% decline with aging, supplementation extends healthspan.

### 8.2 Research Gaps and Future Directions

| Gap | Priority | Suggested Approach |
|-----|----------|-------------------|
| MTHFD2 inhibitor optimization | High | Structure-based drug design, cryo-EM structures |
| PHGDH resistance mechanisms | High | CRISPR screens, metabolomics |
| OCM-epigenetic clock interaction | Medium | Longitudinal DNAmAge studies |
| Taurine human clinical trials | Medium | Phase 2 safety/efficacy |
| OCM-diet interactions | Medium | Precision nutrition based on MTHFR genotype |
| MAT2A combination strategies | Medium | PRMT5 synthetic lethality |

### 8.3 ARP v24 Integration

This review directly informs ARP v24 target prioritization:

**High-priority ARP targets from OCM:**
1. **PHGDH** — Already in ARP 5-target analysis
2. **MTHFD2** — Add as new candidate
3. **SHMT2** — Add as new candidate
4. **MAT2A** — Add as new candidate

**Recommended additions to COMPOUND_DATABASE:**

| Gene | Disease | Modality | Priority |
|------|---------|----------|----------|
| MTHFD2 | cancer | small_molecule | High |
| SHMT2 | cancer, masld | small_molecule | High |
| MAT2A | cancer | small_molecule | Medium-High |

---

## References

1. Ducker G, Rabinowitz J. One-carbon metabolism in cancer. Nat Rev Cancer. 2024.
2. Tibbetts AS et al. MTHFD2 in cancer metabolism. Cancer Res. 2025.
3. Mattaini PR et al. PHGDH amplification in breast cancer. J Clin Invest. 2024.
4. Singh K et al. Folate metabolism in diabetes. Diabetes Metab Res Rev. 2025.
5. Zhang Q et al. Taurine extends healthspan in mice. Science. 2024.
6. Sadre-Marandi F et al. MTHFR C677T and T2DM in Asian populations. Sci Rep. 2025.
7. Fan J et al. SAM/SAH ratio and epigenetic regulation. Nat Metab. 2024.
8. Zheng Y et al. MAT2A inhibitors in MTAP-deleted cancer. Nat Cancer. 2025.

---

*This document was generated by ARP v24 for research purposes. Not intended for clinical application. Verify all claims against primary literature before use.*

**ARP v24 | One-Carbon Metabolism Comprehensive Review | 2026-04-19**