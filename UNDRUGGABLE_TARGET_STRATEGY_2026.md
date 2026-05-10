# Undruggable Target Strategy 2026
**Date:** 2026-05-10  
**Project:** DGAT1-SLC7A11 Synthetic Lethality for NSCLC  
**References:** Nature 2026 (PMID 42104133), JCI Studies, DGAT1_SLC7A11_SYNTHETIC_LETHALITY_2026.md

---

## Executive Summary

The paradigm of "undruggable" targets is rapidly shifting. What was once considered impossible to drug — RAS, transcription factors, tumor suppressors — is now accessible through innovative modalities: covalent allosteric inhibitors, PROTACs, synthetic lethality, and bispecific antibodies.

Our strategy centers on **DGAT1-SLC7A11 synthetic lethality** in KRAS-mutant NSCLC, a two-hit combination that simultaneously blocks lipid storage and antioxidant defense, pushing cancer cells into ferroptosis.

---

## 1. The Undruggable Paradigm Shift (Nature 2026)

### 1.1 Nature Paper: PMID 42104133

**Title:** 'Undruggable' cancer proteins meet their match

**Key Finding:** Daraxonrasib (RMC-6236), a **RAS(ON) multiselective inhibitor**, achieved **35% ORR** in RAS-mutant pancreatic cancer (NEJM 42090791).

**Paradigm Shift:**
```
OLD PARADIGM: Target GDP-bound inactive state (only GTP-bound is "ON")
NEW PARADIGM: Target active GTP-bound state using multiselective inhibitors
```

**Why This Matters for Our Strategy:**
- "Undruggable" = wrong target conformation, not wrong target
- Synthetic lethality = find the right combination partner
- DGAT1-SLC7A11 follows the same successful pattern

### 1.2 Historical Success Stories

| Target | Challenge | Solution | Outcome |
|--------|-----------|----------|---------|
| **KRAS G12C** | Covalent binding needed | Covalent allosteric (sotorasib, adagrasib) | FDA approved |
| **MDM2-p53** | Flat interaction surface | Nutlins (nutlin-3a), PROTACs | Phase III |
| **SOS1** | KRAS activator | BI-1701963 + KRAS G12C combo | Phase I/II |
| **BET proteins** | Acetyl-lysine reader | JQ1, OTX015 | Clinical trials |
| **BCL-6** | Transcription factor | PROTAC (G骨) | Preclinical |

**Common Winning Formula:**
```
1. Covalent engagement (irreversible target modification)
2. Synthetic lethality (combination with context-dependent vulnerability)
3. Allosteric modulation (target non-active site)
```

---

## 2. DGAT1-SLC7A11 Synthetic Lethality Mechanism

### 2.1 The Two-Hit Combination

```
                    DGAT1 Inhibition
                           │
         ┌─────────────────┴─────────────────┐
         │                                   │
    Lipid Droplet                         Free FFA
    Depletion                             Overflow
         │                                   │
         └───────────┬───────────────────────┘
                     │
              Mitochondrial
              ROS Burst
                     │
         ┌───────────┴───────────┐
         │                       │
    Oxidative Stress        ACSL4-mediated
         │                 lipid peroxidation
         └───────────┬───────────┘
                     │
              Ferroptosis
              (Iron-dependent
              lipid peroxidation)
```

### 2.2 Why Dual Blockade Works

**SLC7A11's Role:**
- System Xc- antiporter: imports cystine → exports glutamate
- Cystine → Glutathione synthesis → GPX4-mediated ferroptosis defense
- When SLC7A11 blocked: GSH depletes → ROS accumulates → ferroptosis

**DGAT1's Role:**
- TAG synthesis: DAG + fatty acyl-CoA → TAG
- Lipid droplets: storage of neutral lipids
- When DGAT1 blocked: free FFA accumulates → ROS burst → cell death

**The Synergy:**
```
DGAT1i alone: Cells adapt by using SLC7A11 to compensate
SLC7A11i alone: Cells use DGAT1-mediated lipid storage to survive
DGAT1i + SLC7A11i: BOTH pathways blocked = SYNTHETIC LETHAL
```

### 2.3 KRAS-Mutant NSCLC Specificity

**Why KRAS-mutant NSCLC is particularly vulnerable:**
1. KRAS mutations upregulate SLC7A11 expression (Nrf2 pathway)
2. KRAS-mutant cells depend on glutathione antioxidant defense
3. KRAS drives de novo lipogenesis (FASN, SREBP-1)
4. Lipid droplet accumulation is a known KRAS addiction

**Supporting Evidence:**
- JCI studies show KRAS-mutant NSCLC has elevated SLC7A11
- GPX4 is essential for KRAS-driven tumor survival
- Ferroptosis induction selectively kills KRAS-mutant cells

---

## 3. Synthetic Lethal Pairs with DGAT1 in NSCLC

### 3.1 Dependency Table

| Target | Dependency | Evidence | Combination with DGAT1i |
|--------|-----------|----------|------------------------|
| **SLC7A11** | Critical | High | Primary combination |
| **GPX4** | Critical | High | Primary combination |
| **ACSL4** | Critical | High | Ferroptosis execution |
| **FSP1** | High | Medium | Alternative ferroptosis pathway |
| **LDHB** | High | Medium | STAT1-mediated SLC7A11 regulation |
| **FASN** | High | Medium | De novo lipogenesis |
| **SCD1** | High | Medium | Monounsaturated FA synthesis |
| **SREBP-1** | High | Medium | Lipid synthesis master regulator |
| **YAP/TAZ** | Medium | Medium | Hippo pathway cross-talk |
| **EGFR** | Medium | High | RTK signaling → KRAS axis |
| **NRF2** | Medium | High | Antioxidant response (regulates SLC7A11) |
| **HIF1α** | Medium | Medium | Hypoxia-induced lipid metabolism |
| **SHP2** | Exploratory | Low | KRAS upstream activator |
| **PHGDH** | Exploratory | Low | Serine → glutathione pathway |
| **BRD9** | Exploratory | Low | mSWI/SNF chromatin regulation |

### 3.2 Priority Combinations

**Tier 1 (Immediate):**
- **DGAT1i + SLC7A11i** — Direct synthetic lethality
- **DGAT1i + GPX4i** — Ferroptosis amplification

**Tier 2 (Near-term):**
- **DGAT1i + NRF2i** — Combined antioxidant blockade
- **DGAT1i + FASNi** — De novo lipogenesis + storage blockade

**Tier 3 (Exploratory):**
- **DGAT1i + EGFR TKI** — KRAS pathway inhibition
- **DGAT1i + HIF1αi** — Hypoxia metabolism

---

## 4. AI Platform Strategy

### 4.1 Current ARP v24 Capabilities

| Tool | Purpose | Status |
|------|---------|--------|
| **AlphaFold3** | Protein structure prediction | ✅ Available |
| **REINVENT** | De novo molecular generation | ✅ Available |
| **FEP+** | Free energy perturbation | 🔄 Integration pending |
| **Docking pipelines** | Virtual screening | ✅ Available |
| **TxConformal** | ML-based binding prediction | ✅ Available |
| **Boltz-2** | Structure + affinity (The Last Mile solution) | ✅ Just added |

### 4.2 Gaps to Fill

**Missing capabilities:**
1. **DepMap CRISPR screens** — Identify synthetic lethal pairs experimentally
2. **Groq API** — Rapid literature analysis for combination opportunities
3. **Scrapling** — Clinical trial tracking for combination therapies

### 4.3 Integration Plan

```python
# Ideal integration architecture
class SyntheticLethalAI:
    """
    AI-driven synthetic lethality discovery
    """
    def __init__(self):
        self.depmap = DepMapClient()      # CRISPR dependency data
        self.groq = GroqClient()          # Rapid literature
        self.scrapling = ScraplingClient() # Clinical trials
    
    def find_synthetic_lethals(self, target: str) -> List[dict]:
        """
        1. Query DepMap for genes that are lethal when knocked out
           together with target
        2. Search literature for validated pairs
        3. Track clinical trials for combinations
        """
        pass
    
    def predict_combination_affinity(self, target1: str, target2: str) -> float:
        """
        Use Boltz-2 to predict binding to both targets
        """
        pass
```

---

## 5. Validation Pipeline

### 5.1 Stage 1: In Silico (Week 1-2)

**Tasks:**
1. Run Boltz-2 on DGAT1 + SLC7A11 dual inhibitors
2. ADMET prediction for combination compounds
3. Selectivity profiling against DGAT2, MGAT1/2/3

**Deliverables:**
- List of 50 dual-target candidates
- ADMET filter: CYP3A4 IC50 > 10 μM, hERG IC50 > 30 μM
- Selectivity: DGAT2/DGAT1 > 50×

### 5.2 Stage 2: In Vitro Enzymatic (Week 3-4)

**DGAT1 Assay:**
- TLC-based or FlashPlate (see DGAT1_ACTIVITY_ASSAY_PROTOCOL_2026.md)
- Reference inhibitors: T863 (30-50 nM), A-922500 (10-30 nM)
- Z' factor ≥ 0.5, S/B ≥ 5

**SLC7A11 (System Xc-) Assay:**
- Measure [³H]cystine uptake in cells
- Inhibition by known erastin analogs
- Reference: SLC7A11-IN-1 (120 nM), sulfasalazine (45 μM)

**Combination Screen:**
- Single agent dose-response (8 concentrations)
- Combination: checkerboard or fixed-ratio
- Calculate Combination Index (CI)
  - CI < 0.8: synergism
  - CI = 0.8-1.2: additive
  - CI > 1.2: antagonism

### 5.3 Stage 3: Cell-Based (Week 5-8)

**Cell Lines:**
- A549 (KRAS G12S, wild-type p53)
- H1975 (EGFR T790M, p53 mutant)
- H460 (KRAS Q61H)
- H2122 (KRAS G12C)

**Assays:**
| Assay | Method | Readout |
|-------|--------|---------|
| Cell viability | CCK-8 or MTT | IC50 |
| Lipid droplets | BODIPY 493/503 | Fluorescence microscopy |
| Ferroptosis | C11-BODIPY 581/591 | Flow cytometry |
| GSH/GSSG | GSH/GSSG-Glo | Luminescence |
| GPX4 activity | RSL3 dose-response | Cell death |
| Apoptosis | Caspase 3/7 | RealTime-Glo |

**Key Biomarkers:**
- SLC7A11 (IHC or WB)
- GPX4 (WB)
- 4-HNE (lipid peroxidation)
- NRF2 (antioxidant response)

### 5.4 Stage 4: In Vivo (Week 9-16)

**Xenograft Model:**
```
Model: A549-Luc orthotopic NSCLC
Route: Inhaled (for LUNG-003) or IP (for systemic)
Dosing: QD × 21 days
Endpoints:
├── Tumor growth (bioluminescence)
├── Body weight
├── Lung weight
├── Metastasis (ex vivo imaging)
├── Survival
└── Biomarkers (SLC7A11, GPX4, 4-HNE in tumor)
```

**PK/PD Profiling:**
- Plasma: Cmax, AUC, half-life
- Lung tissue: concentration at 2h, 8h, 24h
- Target engagement: p-AKT, p-ERK (downstream)

---

## 6. Biomarker Strategy

### 6.1 Patient Selection Biomarkers

**HighPriority:**
- SLC7A11 high expression (IHC)
- GPX4 high expression (IHC)
- KRAS mutation (PCR/NGS)

**Exploratory:**
- NRF2 activation (mRNA signature)
- Ferroptosis signature (ACSL4, ALOX5, GCLC)

### 6.2 Response Biomarkers

| Biomarker | Method | Expected Change |
|-----------|--------|------------------|
| SLC7A11 | IHC | Decreased (target engagement) |
| GPX4 | WB | Decreased (ferroptosis) |
| GSH | Colorimetric | Decreased |
| Lipid ROS | C11-BODIPY | Increased |
| 4-HNE | IHC | Increased (oxidative damage) |

---

## 7. Timeline & Milestones

```
Week 1-2:   In silico: Boltz-2 screening, ADMET filtering
            ↓
Week 3-4:   In vitro: DGAT1 + SLC7A11 enzymatic assays
            ↓
Week 5-8:   Cell-based: Viability, ferroptosis markers
            ↓
Week 9-12:  In vivo: A549 xenograft PK/PD
            ↓
Week 13-16: In vivo: Efficacy + biomarker validation
            ↓
IND filing: Month 6 (projected)
```

---

## 8. References

1. Nature 2026, PMID 42104133 — "Undruggable" cancer proteins meet their match
2. Wang et al. 2026, J Chem Inf Model — The Last Mile Problem (Boltz-2)
3. DGAT1_SLC7A11_SYNTHETIC_LETHALITY_2026.md — Our prior analysis
4. DGAT1_ACTIVITY_ASSAY_PROTOCOL_2026.md — Enzymatic assay
5. JCI Studies — KRAS-mutant NSCLC SLC7A11 dependency

---

*Report generated: 2026-05-10 | ARP v24*
*Integration: boltz2_client.py, arp_verifier.py, arp_cli.py (boltz + verify commands)*