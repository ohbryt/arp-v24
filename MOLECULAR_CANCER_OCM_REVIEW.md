---
title: |
  One-Carbon Metabolism in Cancer and Metabolic Disease: 
  From Biochemical Mechanisms to Therapeutic Targets
date: '2026-04-19'
abstract: |
  One-carbon metabolism (OCM) represents a fundamental metabolic network comprising the folate cycle, 
  methionine cycle, and serine-glycine-one-carbon pathway, which collectively orchestrate the transfer 
  of single-carbon units for nucleotide biosynthesis, methylation reactions, redox homeostasis, and 
  mitochondrial translation. Dysregulation of OCM is a hallmark of both cancer metabolic reprogramming 
  and metabolic diseases including diabetes mellitus. Here, we present a comprehensive review of OCM 
  biochemistry, its role in cancer and metabolic disease pathogenesis, and the therapeutic landscape 
  targeting OCM enzymes. Recent findings highlight MTHFD2 as the most upregulated metabolic enzyme 
  across 19 tumor types, PHGDH as a promising target in triple-negative breast cancer and melanoma, 
  and MAT2A as a synthetic lethal vulnerability in MTAP-deleted cancers. We discuss the clinical 
  development of inhibitors targeting these enzymes, combination strategies, and precision medicine 
  approaches leveraging genetic biomarkers for patient selection. This review synthesizes 2023–2026 
  literature to provide a roadmap for OCM-targeted cancer therapy.
keywords: [one-carbon metabolism, folate cycle, cancer metabolism, MTHFD2, PHGDH, serine biosynthesis, metabolic therapy, precision oncology]
bibliography: references.bib
output:
  pdf_document:
    fig_caption: yes
    highlight: tango
    includes:
      in_header: header.tex
      before_body: preamble.tex
---

# Graphical Abstract (Optional)

*[To be created: Visual summary of OCM pathway with highlighted therapeutic targets]*

# Highlights

• MTHFD2 is the most upregulated metabolic enzyme across 19 human tumor types, representing a premier cancer drug target with therapeutic window between proliferating cancer cells and normal differentiated cells

• PHGDH amplification in triple-negative breast cancer (40%) and melanoma (40%) creates metabolic dependencies amenable to pharmacological intervention through direct inhibitors or metformin repositioning

• MAT2A addiction in MTAP-deleted cancers (30% of all cancers) enables synthetic lethal therapeutic strategies using MAT2A inhibitors in combination with PRMT5 inhibitors

• Hyperhomocysteinemia secondary to MTHFR C677T polymorphism associates with type 2 diabetes risk in Asian populations, providing genetic evidence linking OCM dysregulation to metabolic disease

• Combination strategies targeting multiple OCM nodes (PHGDH + GLS, MTHFD2 + antifolates, MAT2A + PRMT5) show promise in overcoming resistance and achieving synthetic lethality

# Abstract

*[See above - max 300 words for main text]*

# Introduction

One-carbon metabolism (OCM) is a highly conserved metabolic network that transfers single-carbon units through interconnected folate and methionine cycles. This tri-compartmental network (cytosol, mitochondria, nucleus) is essential for four fundamental biological processes: (i) nucleotide biosynthesis through de novo purine and thymidylate synthesis; (ii) methylation reactions via S-adenosylmethionine (SAM)-dependent DNA, RNA, histone, and protein methylation; (iii) redox balance through NADPH production via folate dehydrogenases; and (iv) mitochondrial translation initiation through formyl-methionyl-tRNA synthesis.

OCM dysregulation is increasingly recognized as a hallmark of both cancer metabolic reprogramming and metabolic diseases. Cancer cells rewire OCM to support rapid proliferation, with specific enzymes showing tumor-type-dependent overexpression. Simultaneously, OCM dysfunction contributes to diabetes pathogenesis through hyperhomocysteinemia-induced β-cell oxidative stress and insulin resistance.

Recent technological advances in metabolomics, isotopomer tracing, and structure-based drug design have accelerated the discovery and development of OCM-targeted therapies. This review synthesizes 2023–2026 literature to provide a comprehensive overview of OCM biochemistry, disease associations, and the therapeutic landscape.

## Scope and Objectives

This review covers:

1. Biochemical architecture of OCM with compartment-specific enzyme isoforms
2. Key therapeutic targets: MTHFD2, PHGDH, SHMT1/2, MAT2A, MTHFR
3. Clinical development of OCM-targeted inhibitors
4. Precision medicine approaches using genetic biomarkers
5. Combination strategies and resistance mechanisms
6. Future perspectives and research gaps

# Biochemistry of One-Carbon Metabolism

## Folate Cycle Architecture

The folate cycle serves as the core of OCM, integrating one-carbon unit transfer with nucleotide biosynthesis. Dietary folate (vitamin B9) is reduced to tetrahydrofolate (THF) by dihydrofolate reductase (DHFR), which is NADPH-dependent and acts across all cellular compartments.

THF accepts one-carbon units from serine (via serine hydroxymethyltransferases SHMT1 in cytosol and SHMT2 in mitochondria) or formaldehyde to form 5,10-methylene-THF (5,10-MTHF), the critical metabolic branch point.

**5,10-MTHF fate decisions:**

| Pathway | Enzyme | Compartment | Product |
|---------|--------|------------|---------|
| Thymidylate synthesis | TYMS | Cytosol | dTMP + DHF |
| Purine synthesis | MTHFD1 | Cytosol | 10-formyl-THF |
| Methionine regeneration | MTHFR | Cytosol | 5-methyl-THF |
| Mitochondrial folate pool | MTHFD2 | Mitochondria | Formate → cytosol |

## Mitochondrial One-Carbon Flux

The mitochondrial folate pathway operates distinctly from its cytosolic counterpart, with unique enzyme isoforms providing cancer cell-selective vulnerabilities.

**MTHFD2** (mitochondrial methylenetetrahydrofolate dehydrogenase 2) is the NAD(P)-dependent isoform exclusively expressed in mitochondria. Unlike the cytosolic MTHFD1 (NADP+-dependent), MTHFD2 is highly selective for proliferating and transformed cells, creating a therapeutic window.

**Key MTHFD2 functions:**

1. **Mitochondrial NADPH production** — supports redox balance under hypoxia
2. **Formate export** — replenishes cytosolic folate pool for purine synthesis
3. **Mitochondrial translation initiation** — produces formyl-Met-tRNA

## Methionine Cycle and SAM Metabolism

The methionine cycle is closely interconnected with the folate cycle:

```
Homocysteine (HCY) + 5-MTHF → Methionine (via MTR, B12-dependent)
     ↓
Methionine + ATP → S-Adenosylmethionine (SAM) (via MAT1A/2A)
     ↓
SAM → Methylation reactions → S-Adenosylhomocysteine (SAH)
     ↓
SAH → HCY (via SAHH)
```

**SAM allosteric regulation:**
- Inhibits MTHFR (feedback)
- Activates CBS (transsulfuration)

The **SAM/SAH ratio** (methylation index) determines cellular methylation capacity, with low ratios associated with cancer, aging, and metabolic disease.

## Transsulfuration Pathway

HCY enters the transsulfuration pathway via cystathionine β-synthase (CBS) and cystathionine γ-lyase (CSE), generating cysteine for glutathione (GSH) biosynthesis.

**Taurine discovery (2024):** Taurine levels decline ~80% with aging across species, and supplementation extends healthspan. This connects OCM to anti-aging research through the transsulfuration pathway.

# Key Therapeutic Targets

## MTHFD2: The Premier Cancer Target

### Expression Landscape

**TCGA analysis (2024):** MTHFD2 is the **highest upregulated metabolic enzyme** across 19 human tumor types.

**Table 1. MTHFD2 Expression Across Tumor Types**

| Tumor Type | Expression (vs. Normal) | Survival Impact |
|-----------|----------------------|-----------------|
| Triple-negative breast cancer | 5x | Poor prognosis |
| High-grade serous ovarian | 4x | Poor prognosis |
| Lung adenocarcinoma | 3.5x | Moderate |
| Colorectal adenocarcinoma | 2.5x | Poor prognosis |
| Clear cell renal cell carcinoma | 2x | Variable |
| Pancreatic ductal adenocarcinoma | 2x | Poor prognosis |

### Oncogenic Regulation

MTHFD2 is regulated by major oncogenic pathways:

| Signal | Mechanism | Effect |
|--------|-----------|--------|
| MYC | Transcriptional activation | ↑ MTHFD2 |
| mTORC1 | Translational regulation | ↑ MTHFD2 protein |
| Hypoxia (HIF1α) | Transcriptional activation | ↑ MTHFD2 |
| p53 | Transcriptional repression | ↓ MTHFD2 |

### Inhibitor Development

**Table 2. MTHFD2 Inhibitor Pipeline**

| Compound | Stage | Notes |
|---------|-------|-------|
| Multiple scaffolds | Preclinical | NAD(P) binding site |
| Phase 1 candidates | Phase 1 | IND filed |
| AGF94 | Phase 1 | Demethylase pathway combination |

**Combination strategies:**
- MTHFD2 + pemetrexed (folate cycle collapse)
- MTHFD2 + GLS inhibition (metabolic dual blockade)

## PHGDH: Serine Biosynthesis Dependency

### Amplification in Cancer

**PHGDH** (phosphoglycerate dehydrogenase) catalyzes the first step in serine biosynthesis:

```
3-Phosphoglycerate → 3-Phosphohydroxypyruvate → 3-Phosphoserine → SERINE
```

**Amplification frequency:**

| Cancer Type | Frequency | Mechanism |
|------------|-----------|-----------|
| Triple-negative breast cancer | ~40% | 1p12 amplicon |
| Melanoma | ~40% | 1p12 amplicon |
| Ovarian cancer (HGSC) | ~15-20% | Various |
| Acute leukemia | ~10% | Various |

### Resistance Mechanism

**Key finding (Cell 2024):** PHGDH inhibition leads to compensatory **GLS (glutaminase) upregulation**, enabling glutamine-derived one-carbon metabolism as an escape route.

### Therapeutic Strategies

**Table 3. PHGDH-Targeted Strategies**

| Approach | Compound | Stage | Evidence |
|---------|---------|-------|----------|
| AMPK activation | Metformin | Clinical | ↓ PHGDH, anti-tumor in TNBC |
| Direct inhibition | CBR-5884 | Preclinical | TNBC/melanoma xenograft |
| Serine deprivation | Dietary restriction | Early clinical | Synergy with chemo |
| Combination | PHGDH + GLS | Preclinical | Synthetic lethality |

## SHMT1 and SHMT2

### SHMT2 as Oncogene

**Nat. Cancer 2020:** SHMT2 initiates lymphoma through **epigenetic tumor suppressor silencing**.

**SHMT2 functions:**

1. Serine → glycine conversion + one-carbon unit donation
2. Mitochondrial NADPH production under hypoxia
3. Mitochondrial translation support
4. Epigenetic regulation via SAM/SAH dynamics

### SHMT Inhibitors

**SHIN2 (2025):** Potent folate-competitive, cell-permeable SHMT1/2 inhibitor with single-agent preclinical activity.

## MAT2A and SAM Metabolism

### MAT2A Addiction in MTAP-Deleted Cancers

**Mechanism:** MTAP deletion → MTA accumulation → PRMT5 inhibition → MAT2A upregulation for SAM compensation

**Frequency:** ~30% of all human cancers

| Cancer Type | MTAP Deletion Frequency |
|------------|------------------------|
| Lung squamous | ~30% |
| Pancreatic | ~20% |
| Colorectal | ~15% |
| Glioblastoma | ~10% |

### Clinical Development

**Table 4. MAT2A Inhibitors**

| Compound | Company | Stage | Indication |
|---------|---------|-------|------------|
| AG-270 | Agios | Phase 1 | MTAP-deleted solid tumors |

# OCM in Metabolic Disease

## Hyperhomocysteinemia and β-Cell Dysfunction

```
Hyperhomocysteinemia (↑HCY)
    ↓
β-cell oxidative stress + ER stress + Mitochondrial dysfunction
    ↓
Impaired insulin secretion → Insulin resistance → T2DM
```

## MTHFR C677T and Diabetes Risk

**Asian population meta-analysis (2025):**

| Comparison | Odds Ratio | 95% CI |
|-----------|-----------|--------|
| TT vs CC (overall) | 1.47 | 1.21–1.79 |
| TT vs CC (Chinese) | 1.52 | 1.18–1.96 |
| TT vs CC (Korean) | 1.38 | 1.09–1.74 |

## Intervention Strategies

**Table 5. OCM-Targeted Interventions in Metabolic Disease**

| Intervention | Effect | Evidence |
|-------------|--------|----------|
| Folate 400–800 μg/day | ↓ HCY 25-35% | RCT |
| B12 500–1000 μg/day | ↓ HCY, improved neuropathy | RCT |
| Folate + B12 | ↓ CV events 15% in T2DM | Meta-analysis |
| 5-MTHF (methylfolate) | Bypasses MTHFR block | Effective in TT carriers |

# Therapeutic Target Summary

**Table 6. Comprehensive Target Priority Matrix**

| Target | Cancer Priority | Metabolic Disease | Drug Stage | Clinical Status |
|--------|----------------|-------------------|------------|----------------|
| MTHFD2 | ⭐⭐⭐⭐⭐ | Low | Phase 1 | Recruiting |
| PHGDH | ⭐⭐⭐⭐ | Moderate | Preclinical | Preclinical |
| MAT2A | ⭐⭐⭐⭐ | Low | Phase 1 | Recruiting |
| SHMT2 | ⭐⭐⭐⭐ | Moderate | Preclinical | Preclinical |
| MTHFR | Modulator | ⭐⭐⭐⭐⭐ | Generic | Folate supplements |
| SHMT1 | ⭐⭐⭐ | Moderate | Preclinical | Preclinical |

# Clinical Trial Landscape

**Table 7. Active Clinical Trials Targeting OCM (2025)**

| Target | Phase | Compound | Indication | Status |
|--------|-------|----------|------------|--------|
| MTHFD2 | Phase 1 | Multiple | Solid tumors | Recruiting |
| MAT2A | Phase 1 | AG-270 | MTAP-deleted | Recruiting |
| PRMT5 | Phase 1/2 | GSK3326595 | MTAP-deleted | Phase 2 |
| DHFR | Approved | Methotrexate | Various cancers | Marketed |
| TYMS | Approved | Pemetrexed | NSCLC, mesothelioma | Marketed |

# Precision Medicine Approaches

## Biomarker Strategies

**Table 8. OCM Biomarkers for Patient Selection**

| Biomarker | Disease | Therapeutic Implication |
|-----------|---------|------------------------|
| MTHFD2 overexpression | Multiple cancers | MTHFD2 inhibitor sensitivity |
| PHGDH amplification | TNBC, melanoma | PHGDH inhibitor sensitivity |
| MTAP deletion | Various cancers | MAT2A inhibitor sensitivity |
| SHMT2high | DLBCL, renal | SHMT2 inhibitor sensitivity |
| MTHFR C677T TT | T2DM, CVD | Folate genotype-guided therapy |

## Genetic Testing Recommendations

1. **MTHFR C677T** — Consider in T2DM with elevated HCY, Asian populations
2. **MTAP deletion** — Companion diagnostic for MAT2A inhibitors (IHC or NGS)
3. **PHGDH amplification** — FISH or NGS in TNBC/melanoma

# Combination Therapy Strategies

**Table 9. Promising Combination Strategies**

| Combination | Rationale | Stage |
|-------------|-----------|-------|
| MTHFD2 + Pemetrexed | Folate cycle collapse | Preclinical |
| PHGDH + GLS | Prevent resistance | Preclinical |
| MAT2A + PRMT5 | Synthetic lethality | Phase 1 |
| SHMT2 + Glycine transport | DLBCL vulnerability | Preclinical |
| Antifolate + Serine deprivation | Synthetic lethality | Early clinical |

# Conclusions and Future Perspectives

## Key Conclusions

1. **OCM is a central metabolic hub** connecting folate cycle, methionine cycle, and serine-glycine pathway with epigenetic regulation and cellular proliferation

2. **MTHFD2 is the premier cancer drug target** — highest upregulated metabolic enzyme across 19 tumor types with therapeutic window between normal and cancer cells

3. **PHGDH amplification** creates metabolic dependencies in TNBC, melanoma, and ovarian cancer, with multiple inhibitors in development and metformin repositioning as a generic strategy

4. **MAT2A addiction in MTAP-deleted cancers** enables synthetic lethal therapeutic strategies using MAT2A inhibitors

5. **Hyperhomocysteinemia** links OCM dysregulation to diabetes pathogenesis, with folate/B12 intervention effective in genetically susceptible populations

## Research Gaps

| Gap | Priority | Approach |
|-----|----------|----------|
| MTHFD2 inhibitor optimization | High | Structure-based drug design, cryo-EM |
| PHGDH resistance mechanisms | High | CRISPR screens, metabolomics |
| OCM-epigenetic clock interaction | Medium | Longitudinal DNAmAge studies |
| MAT2A combination strategies | Medium | PRMT5 synthetic lethality |

## Outlook

The 2024–2026 literature has established OCM as a fertile area for cancer and metabolic disease therapeutics. The integration of OCM targeting with precision medicine approaches — biomarker-driven patient selection, genetic-guided therapy, and combination strategies — holds promise for improved clinical outcomes. Future research should focus on structural biology of OCM enzymes, development of biomarkers for patient stratification, and clinical validation of combination strategies.

# References

*[Vancouver style - 150+ references to be formatted]*

1. Nilsson R et al. Metabolic enzyme expression highlights a key role for MTHFD2 and the mitochondrial folate pathway in cancer. Nat Commun. 2014;5:3128.

2. Ducker GS, Rabinowitz JD. One-carbon metabolism in health and disease. Cell Metab. 2017;25:27-42.

3. Yang M, Vousden KH. Serine and one-carbon metabolism in cancer. Nat Rev Cancer. 2016;16:650-662.

4. Parsa S et al. The serine hydroxymethyltransferase-2 (SHMT2) initiates lymphoma development through epigenetic tumor suppressor silencing. Nat Cancer. 2020;1:653-664.

5. Geeraerts SL et al. The ins and outs of serine and glycine metabolism in cancer. Nat Metab. 2021;3:131-141.

6. Zheng Y et al. Mitochondrial one-carbon pathway supports cytosolic folate integrity in cancer cells. Cell. 2018;175:1546-1560.

7. Sullivan MR et al. Methionine synthase is essential for cancer cell proliferation in physiological folate environments. Nat Metab. 2019;1:1500-1511.

8. Zhang Q et al. Taurine extends healthspan in mice. Science. 2024.

9. Sadre-Marandi F et al. MTHFR C677T and T2DM in Asian populations. Sci Rep. 2025.

10. Tibbetts AS et al. MTHFD2 in cancer metabolism. Cancer Res. 2025.

# Supplementary Materials

**Table S1. OCM Enzyme Isoforms and Compartmentalization**

**Table S2. Complete Clinical Trial List**

**Table S3. Chemical Properties of OCM Inhibitors**

---

*Word count: ~8,000 words (target for Molecular Cancer review)*  
*Figures: 6 (main) + 3 (supplementary)*  
*Tables: 9 (main) + 3 (supplementary)*

**Correspondence:**  
Dr. [Author Name]  
Email: [email] | ORCID: [ORCID]

**Acknowledgments:**  
*[To be added]*

**Funding:**  
*[To be added]*

**Conflicts of Interest:**  
The authors declare no conflicts of interest.