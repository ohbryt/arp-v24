# Deep Research: FSP1 and NSCLC
**Date:** 2026-05-10  
**Topic:** Ferroptosis Suppressor Protein 1 (FSP1) in Non-Small Cell Lung Cancer  
**Sources:** Nature (2025), Nature Communications (2022), PNAS (2025), Cell Death & Disease (2023)

---

## Executive Summary

FSP1 (Ferroptosis Suppressor Protein 1, also known as AIFM2) is a NADH-dependent CoQ oxidoreductase that suppresses ferroptosis by reducing coenzyme Q10 (CoQ) to CoQH2, thereby preventing lipid peroxidation. In NSCLC, particularly KEAP1/STK11-altered lung adenocarcinoma (LUAD), FSP1 is a validated therapeutic target. The Nature 2025 paper demonstrates that FSP1 inhibition reduces tumor growth by up to **80% in mouse models**, with no effective FSP1 inhibitor yet in clinical trials — representing a **first-in-class opportunity**.

---

## 1. FSP1 Biology

### 1.1 Protein Function

| Property | Details |
|----------|---------|
| **Gene** | AIFM2 (Apoptosis-Inducing Factor Mitochondrial 2) |
| **Also known as** | FSP1 (Ferroptosis Suppressor Protein 1) |
| **Function** | NADH-dependent coenzyme Q oxidoreductase |
| **Mechanism** | Reduces CoQ10 → CoQH2 (antioxidant effect) |
| **Location** | Plasma membrane, mitochondria |
| **Family** | Flavoprotein oxidoreductases |

### 1.2 Ferroptosis Suppression Mechanism

```
                    FSP1
                      ↓
NADH ─────────────────→ CoQH2 (reduced CoQ)
  ↑                         ↓
  │                    Prevents lipid peroxidation
  │                         ↓
  │                    FERROPTOSIS RESISTANCE
  ↓
NAD+
```

**Without FSP1:**
- CoQ remains oxidized (CoQ)
- Lipid peroxides accumulate
- Membrane damage → ferroptosis

**With FSP1 active:**
- CoQH2 scavenges lipid peroxides
- Membrane protected
- Ferroptosis blocked

### 1.3 Relationship to GPX4

| Factor | GPX4 | FSP1 |
|--------|------|------|
| **Function** | Reduces lipid peroxides using GSH | Reduces CoQ to CoQH2 |
| **Co-factor** | GSH (glutathione) | NADH |
| **Location** | Cytosol, mitochondria | Plasma membrane |
| **Inhibition** | RSL3, ML210 | iFSP1, FSEN1, viFSP1 |
| **Relationship** | Parallel ferroptosis defense pathways |

---

## 2. FSP1 in NSCLC

### 2.1 Association with Mutations

**Key finding (Nature 2025):** FSP1 is significantly elevated in LUAD tumors with co-mutation of either STK11 or KEAP1.

| Mutation Status | FSP1 Expression | Prognosis |
|----------------|-----------------|-----------|
| KEAP1/STK11 WT | Low baseline | Better |
| STK11 mutant | Elevated | Poorer |
| KEAP1 mutant | Elevated | Poorer |
| KEAP1/STK11 mutant | Highest | Poorest |

### 2.2 KEAP1-NRF2-FSP1 Axis

```
KEAP1 mutation/inactivation
        ↓
NRF2 (NFE2L2) activation (normally suppressed by KEAP1)
        ↓
NRF2 target gene transcription
        ↓
FSP1 upregulation
        ↓
CoQ → CoQH2 (ferroptosis protection)
        ↓
Tumor cell survival, radiation resistance
```

**Note:** FSP1 is regulated by NRF2 in a **NRF2-dependent and NRF2-independent manner** depending on context.

### 2.3 STK11 (LKB1) Connection

STK11/LKB1 alterations:
- Frequently co-occur with KRAS mutations in LUAD
- Associated with PD-1 inhibitor resistance
- Promote ferroptosis protection via FSP1 upregulation
- Increase SCD1 dependence (lipid metabolism)

### 2.4 Clinical Implications

| Factor | Impact |
|--------|--------|
| **KRAS mutation** | Common driver, metabolic rewiring |
| **KRAS + STK11/KEAP1** | Maximum FSP1 dependence |
| **NRF2 activation** | Oxidative stress defense, therapy resistance |

---

## 3. FSP1 Inhibitors

### 3.1 Chemical Series

| Inhibitor | Type | Key Features | IC50 | Status |
|----------|------|-------------|------|--------|
| **FSEN1** | Substrate-pocket | Most potent, uncompetitive | ~60nM | Co-crystal (PDB 9M3M) |
| **viFSP1** | NADH-pocket | Species-independent | Low nM | Preclinical |
| **iFSP1** | First-generation | π-π stacking with F360 | nM range | Probe |
| **icFSP1** | Phase separation | Condensate formation | nM range | Mechanistic probe |

### 3.2 FSEN1 (Ferroptosis Sensitizer 1)

**Most developable lead compound:**

| Property | Details |
|----------|---------|
| **Potency** | ~60 nM IC50 |
| **Type** | Uncompetitive inhibitor |
| **Binding** | Substrate-binding pocket |
| **Key interaction** | π-π stacking with F360 residue |
| **Selectivity** | Selective for FSP1 over other flavoproteins |
| **Co-crystal** | PDB 9M3M (solved 2025) |

**Binding mechanism:**
- F360 residue critical for inhibition
- π-π stacking between FSEN1 phenyl and F360
- Similar to iFSP1 predicted binding mode

### 3.3 viFSP1

| Property | Details |
|----------|---------|
| **Target site** | NADH binding pocket |
| **Key residues** | A328, F294, M327, T1 |
| **Advantage** | Species-independent (human = mouse) |
| **IC50** | Similar for human and mouse FSP1 |

### 3.4 Inhibitor Mechanism Comparison

| Inhibitor | Type | Substrate Binding | NADH Binding |
|----------|------|------------------|--------------|
| FSEN1 | Uncompetitive | ✅ (substrate pocket) | — |
| viFSP1 | Non-competitive | — | ✅ (NADH pocket) |
| iFSP1 | Non-competitive | Docked | — |

---

## 4. Key Publications

### 4.1 Nature 2025 (November 5)
**Title:** "Targeting FSP1 triggers ferroptosis in lung cancer"  
**Authors:** Wu K, Vaughan AJ, Bossowski JP, et al.  
**DOI:** 10.1038/s41586-025-09710-8

**Key findings:**
| Finding | Details |
|---------|---------|
| FSP1 knockout | 80% tumor growth reduction in mice |
| Pharmacological inhibition | Effective in multiple preclinical models |
| LUAD progression | FSP1 upregulated as tumors progress |
| Survival benefit | Prolonged survival in mouse models |
| Biomarker | FSP1 IHC + KEAP1/STK11 genotype for selection |

### 4.2 Nature Communications 2022 (April 22)
**Title:** "A targetable CoQ-FSP1 axis drives ferroptosis- and radiation-resistance in KEAP1 inactive lung cancers"  
**DOI:** 10.1038/s41467-022-29905-1

**Key findings:**
| Finding | Details |
|---------|---------|
| KEAP1 mutation | Drives FSP1 upregulation via NRF2 |
| Radiation resistance | CoQ-FSP1 axis protects against RT |
| Therapeutic angle | FSP1 inhibition + radiation = synergy |

### 4.3 PNAS 2025 (May 29)
**Title:** "Cocrystal structure reveals the mechanism of FSP1 inhibition by FSEN1"  
**DOI:** 10.1073/pnas.2505197122  
**PDB:** 9M3M

**Key findings:**
| Finding | Details |
|---------|---------|
| Binding mode | FSEN1 binds substrate pocket |
| F360 importance | Critical π-π stacking interaction |
| Mechanism | Uncompetitive inhibition |
| Drug design | Structural basis for optimization |

### 4.4 Cell Death & Disease 2023
**Title:** "FSP1 confers ferroptosis resistance in KEAP1 mutant non-small cell lung carcinoma in NRF2-dependent and -independent manner"  
**DOI:** 10.1038/s41419-023-06070-x

**Key findings:**
| Finding | Details |
|---------|---------|
| NRF2-dependent | Partial FSP1 regulation via NRF2 |
| NRF2-independent | FSP1 can be regulated independently |
| KEAP1 mutation | Strong association with ferroptosis resistance |

---

## 5. In Vivo Evidence

### 5.1 Nature 2025 Animal Data

| Model | Result |
|-------|--------|
| FSP1 knockout tumors | 80% growth reduction |
| Multiple preclinical models | Consistent tumor suppression |
| Survival models | Prolonged survival |
| KRAS/KEAP1/STK11 triple mutant | Profound suppression |

### 5.2 Resistance Restoration

When FSP1 is knocked out, tumor growth can be restored by:
| Factor | Effect |
|--------|--------|
| **Lipid RTAs** | Restores tumorigenesis |
| **Acsl4 loss** | Blocks ferroptosis, restores growth |

**Mechanism:** Acsl4 (ACSL4) is required for ferroptosis execution — loss blocks cell death even with FSP1 inhibition.

### 5.3 Oxidized PUFA-PLs

FSP1 knockout tumors show:
- Increased oxidized PUFA-phospholipids
- Elevated lipid peroxidation markers
- Evidence of ferroptosis engagement

---

## 6. Biomarker Strategy

### 6.1 Patient Selection Markers

| Marker | Method | Purpose |
|--------|--------|---------|
| **FSP1 IHC** | Immunohistochemistry | Tumor expression level |
| **KEAP1 mutation** | NGS | Genetic alteration |
| **STK11 mutation** | NGS | Genetic alteration |
| **NRF2 (NFE2L2) mutation** | NGS | NRF2 pathway |
| **ACSL4** | IHC or qPCR | Ferroptosis competence |

### 6.2 Concordant Biomarker Approach

**Required for clinical enrollment:**
1. FSP1-high by IHC
2. KEAP1, STK11, or NFE2L2 alteration
3. ACSL4/lipid peroxidation competence
4. Biopsy-confirmed PD signature (on-treatment)

---

## 7. Clinical Development Considerations

### 7.1 No Current Clinical Trials

| Status | Implication |
|--------|-------------|
| No FSP1 inhibitor in clinic | First-in-class opportunity |
| Preclinical only | IND-enabling studies needed |
| Multiple chemotypes | Parallel development possible |

### 7.2 Regulatory Pathway

**Potential accelerated approval based on:**
- Biomarker-defined population
- Compelling ORR/DOR in refractory NSCLC
- Ferroptosis engagement (mandatory biopsy)

### 7.3 Combination Opportunities

| Combination | Rationale |
|-------------|-----------|
| **+ Radiotherapy** | Synergy in KEAP1-inactive tumors |
| **+ PD-(L)1 blockade** | Overcome STK11-associated resistance |
| **+ Chemotherapy** | Enhanced tumor cell death |
| **+ Ferroptosis inducers** | Synergistic combinations |

---

## 8. Target Product Profile

| Property | Ideal | Acceptable |
|----------|-------|-----------|
| **Modality** | Oral small molecule | Oral or injectable |
| **IC50** | <50 nM | <100 nM |
| **Selectivity** | >30-fold over redox enzymes | >10-fold |
| **Tumor exposure** | >IC90 sustained | >IC50 |
| **PK** | Tumor:RBC >1 | Tumor:plasma >1 |
| **Safety** | No neuro/RBC/immune toxicity | Manageable toxicity |
| **PD marker** | BODIPY-C11, CoQ redox | Lipid peroxidation markers |

---

## 9. Assay Cascade

### 9.1 Biochemical

| Assay | Read-out |
|-------|----------|
| Recombinant FSP1 activity | IC50 (human + mouse) |
| Orthogonal binding | Confirmation |
| Selectivity panel | Flavo/redox enzymes |
| CYP/hERG | Drug-drug interactions |

### 9.2 Cellular

| Assay | Read-out |
|-------|----------|
| Viability (FSP1-high NSCLC) | IC50 |
| BODIPY-C11 | Lipid peroxidation |
| CoQ/CoQH2 LC-MS | Redox state |
| Ferroptosis rescue | Ferrostatin-1 confirmation |
| Organoid efficacy | 3D response |

### 9.3 In Vivo

| Assay | Read-out |
|-------|----------|
| Orthotopic NSCLC | TGI, survival |
| Syngeneic models | Immune competence |
| PDX | Human tumor response |
| Combination (RT, ICI) | Synergy studies |

---

## 10. Go/No-Go Criteria

### Go (ALL required)

- [ ] IC50 <100 nM (human FSP1)
- [ ] Selectivity >30-fold
- [ ] Cell killing rescued by ferroptosis blockers
- [ ] TGI >50% OR compelling combo additivity
- [ ] No >10% body-weight loss
- [ ] Tumor exposure >IC90

### No-Go

- ❌ Requires GPX4 co-inhibition
- ❌ Activity lost with serum lipoproteins
- ❌ Immune toxicity

---

## 11. Comparison to Other NSCLC Metabolic Targets

| Target | FSP1 | MCT1/4 | Complex I | Glutamine |
|--------|------|--------|-----------|-----------|
| **Specificity** | Lung-enriched (KEAP1) | Moderate | Broad | Broad |
| **Clinical stage** | Preclinical | Phase I | Phase I | Phase II |
| **Challenge** | Biomarker population | Redundancy | Systemic toxicity | Plasticity |
| **Modality** | Small molecule | Small molecule | Small molecule | Small molecule |

---

## 12. Files and Pipeline Integration

### 12.1 Related Files

| File | Content |
|------|---------|
| `FSP1_DEVELOPMENT_PLAN_2026.md` | Full development plan |
| `NOVEL_CANDIDATES_REPORT_2026.md` | Portfolio overview |
| `arp_orchestrator.py` | FSP1 playbook |
| `DGAT1_LUNG_COMPOUND_REPORT_2026.md` | Our NSCLC compounds |

### 12.2 Triple Ferroptosis Combo

```
DGAT1i (our compounds)
    └── Lipid droplet → PUFA accumulation
    
SLC7A11i (our work)
    └── GSH depletion → GPX4 dysfunction
    
FSP1i (this research)
    └── CoQ rescue → lipid peroxidation
    
= Maximum ferroptosis induction
```

---

## 13. Key References

1. Wu K, et al. (2025). Targeting FSP1 triggers ferroptosis in lung cancer. **Nature**. DOI: 10.1038/s41586-025-09710-8
2. Nature Communications (2022). A targetable CoQ-FSP1 axis drives ferroptosis- and radiation-resistance in KEAP1 inactive lung cancers. DOI: 10.1038/s41467-022-29905-1
3. Zhang & Megarioti (2025). Cocrystal structure reveals the mechanism of FSP1 inhibition by FSEN1. **PNAS**. DOI: 10.1073/pnas.2505197122
4. Cell Death & Disease (2023). FSP1 confers ferroptosis resistance in KEAP1 mutant NSCLC. DOI: 10.1038/s41419-023-06070-x
5. Hendricks JM, et al. (2023). Identification of structurally diverse FSP1 inhibitors. **Nature Chemical Biology**.
6. PDB 9M3M: Structure of FSP1 in complex with FSEN1.

---

## 14. Summary

**FSP1 is a validated, lung-enriched therapeutic target in KEAP1/STK11-altered NSCLC.**

| Key Point | Evidence |
|-----------|----------|
| **Target validation** | Nature 2025: 80% tumor reduction |
| **Biomarker** | KEAP1/STK11/NFE2L2 mutations + FSP1 IHC |
| **Lead compound** | FSEN1 (co-crystal, 60nM) |
| **Mechanism** | NADH → CoQ → CoQH2, prevents lipid peroxidation |
| **Combination** | Radiotherapy, immunotherapy |
| **Clinical gap** | No FSP1 inhibitor in clinical trials |

**This represents the highest-confidence first-in-class opportunity in NSCLC metabolism.**

---

*Deep research completed: 2026-05-10 | ARP v24*  
*Sources: Nature, Nature Communications, PNAS, Cell Death & Disease*