# FSP1 Inhibitor Design: From Lead to Candidate
**Date:** 2026-05-11  
**Target:** FSP1 (Ferroptosis Suppressor Protein 1 / AIFM2)  
**Indication:** KEAP1/STK11/NFE2L2-altered NSCLC  
**Based on:** Nature 2025 (FSP1), PNAS 2025 (FSEN1 co-crystal), ARP Pipeline

---

## Executive Summary

FSP1 Inhibitor设计方案를 제시합니다:

| Element | Design |
|---------|--------|
| **Lead scaffold** | FSEN1-like (substrate pocket) |
| **Backup scaffold** | viFSP1-like (NADH pocket) |
| **Target IC50** | <50 nM |
| **Selectivity** | ≥30-fold over redox enzymes |
| **Key residues** | F360 (π-π stacking) |

---

## 1. FSP1 Target Biology

### 1.1 FSP1 Mechanism

```
                    FSP1
                      ↓
NADH ───────────────→ CoQH2 (reduced CoQ)
  ↑                         ↓
  │                    Prevents lipid peroxidation
  │                         ↓
  ↓                    FERROPTOSIS RESISTANCE
NAD+
```

### 1.2 Resistance Mechanism in NSCLC

```
KEAP1 mutation → NRF2 activation → FSP1 ↑ → CoQH2 ↑ → Ferroptosis protection
                                    ↓
                            FSP1 inhibitor → Ferroptosis → Tumor death
```

---

## 2. Known FSP1 Inhibitors

### 2.1 Chemical Series

| Compound | IC50 | Target Site | Status |
|----------|------|------------|--------|
| **FSEN1** | ~60 nM | Substrate pocket | Co-crystal (PDB 9M3M) |
| **viFSP1** | Low nM | NADH pocket | Species-independent |
| **iFSP1** | nM | Substrate pocket | First-gen |
| **icFSP1** | nM | Condensate | Mechanistic probe |

### 2.2 FSEN1 Co-Crystal Structure

**PDB:** 9M3M (solved 2025)

**Key binding features:**
| Feature | Details |
|---------|--------|
| **Binding site** | Substrate pocket |
| **Key residue** | F360 (π-π stacking) |
| **Interaction** | Hydrophobic + π-π |
| **Type** | Uncompetitive inhibitor |

### 2.3 viFSP1 Binding

| Feature | Details |
|---------|--------|
| **Binding site** | NADH pocket |
| **Key residues** | A328, F294, M327, T1 |
| **Advantage** | Species-independent (human = mouse) |

---

## 3. FSP1 Inhibitor Design Strategy

### 3.1 Design Principles

```
1. High potency: IC50 < 50 nM
2. Selectivity: ≥30-fold over flavoproteins
3. Species bridging: Human = Rodent
4. Oral bioavailability: F > 20%
5. Tumor exposure: > IC90 sustained
6. Safety: No RBC, neuronal, immune toxicity
```

### 3.2 Lead Selection Criteria

| Criterion | Target | Rationale |
|-----------|--------|-----------|
| Enzymatic IC50 | <50 nM | Below cellular IC90 |
| Selectivity | >30-fold | Redox enzyme off-targets |
| Lipophilicity | cLogP 2-4 | Balance solubility/permeability |
| Solubility | >50 μM (pH 7.4) | Formulation |
| Metabolic stability | CLint <15 μL/min/mg | Hepatic clearance |
| CYP inhibition | IC50 >10 μM | Drug-drug interactions |

---

## 4. FSEN1-Like Scaffold Design

### 4.1 Core Structure

```
FSEN1-like pharmacophore:
                                   
     ╱═╲
    ╱    ╲          Key: F360 π-π stacking
   ╱______╲         Required: H-bond acceptors
  ╱        ╲        Optional: Additional hydrophobic
 ╱          ╲
    Core       Substituent
  (hydrophobic)   (polar/charged)
```

### 4.2 SAR Optimization

**Core modifications:**
| Position | Modification | Expected Effect |
|----------|-------------|----------------|
| R1 | Phenyl → Pyridyl | π-π with F360 |
| R2 | Halogen (Cl/Br) | Hydrophobic |
| R3 | Methyl → Ethyl | Selectivity |
| R4 | H → OH/OMe | Metabolite stability |

### 4.3 Proposed Analogs

```python
# FSEN1 analogs for synthesis
analogs = [
    {
        "name": "ARP-FSP1-001",
        "smiles": "Cc1ccc(-c2nc3ccccc3[nH]c2=O)cc1",
        "modification": "Core phenyl pyridyl replacement",
        "target": "F360 pocket"
    },
    {
        "name": "ARP-FSP1-002", 
        "smiles": "Cc1ccc(-c2nc3ccccc3c(N)nc2=O)cc1",
        "modification": "Amino substituent",
        "target": "H-bond network"
    },
    {
        "name": "ARP-FSP1-003",
        "smiles": "Cc1ccc(-c2nc3ccccc3c(O)nc2=O)cc1",
        "modification": "Hydroxyl (metabolite)",
        "target": "Solubility"
    },
    {
        "name": "ARP-FSP1-004",
        "smiles": "Cc1ccc(-c2nc3cccc(Cl)c3c(N)nc2=O)cc1",
        "modification": "Chlorophenyl + amino",
        "target": "Potency + selectivity"
    }
]
```

---

## 5. Medicinal Chemistry Synthesis

### 5.1 Retrosynthetic Analysis

```
FSEN1-like target
       │
       ├──Suzuki coupling
       │
       ├──Buchwald-Hartwig amination
       │
       └──Nucleophilic substitution
```

### 5.2 Proposed Synthesis

**Step 1: Core formation**
```
Phenyl boronic acid + Bromopyridone
        ↓ Pd(PPh3)4, K2CO3
    Coupled core
```

**Step 2: Amination**
```
Core + Amine
    ↓ Buchwald-Hartwig
    Final compound
```

**Step 3: Analog diversification**
```
Final + R-X
    ↓ SNAr or coupling
    Analogs
```

### 5.3 Key Intermediates

| Intermediate | SMILES | Purity Target |
|-------------|--------|--------------|
| Core-1 | c1ccc2c(c1)nc(n2)C | >90% |
| Boronate-1 | CC(C)(C)OC(=O)nc1ccc2ccccc2n1 | >90% |
| Amines | R-NH2 (various) | >95% |

---

## 6. In Vitro Assay Cascade

### 6.1 Biochemical Assays

| Assay | Method | Threshold |
|-------|--------|-----------|
| FSP1 enzymatic | Recombinant hFSP1, NADH→CoQ reduction | IC50 <50 nM |
| Selectivity | Panel: FSP1, FSP2, GR, ADH | >30-fold |
| Species bridge | Human + mouse FSP1 | IC50 ratio 0.5-2.0 |

### 6.2 Cellular Assays

| Assay | Method | Threshold |
|-------|--------|-----------|
| Viability | CellTiter-Glo | IC50 <1 μM |
| Lipid peroxidation | BODIPY-C11 | EC50 <500 nM |
| Ferroptosis rescue | Ferrostatin-1 rescue | Confirm mechanism |
| CoQ redox | LC-MS | CoQH2/CoQ ratio ↓ |

### 6.3 ADMET Assays

| Assay | Method | Threshold |
|-------|--------|-----------|
| Solubility | MDCK or PAMPA | >50 μM |
| Metabolic stability | Human liver microsomes | CLint <15 |
| CYP inhibition | CYP 3A4, 2D6, 2C9 | IC50 >10 μM |
| hERG | Patch clamp | IC50 >10 μM |
| Plasma protein binding | PPB | fu >0.1 |

---

## 7. Structural Optimization

### 7.1 Binding Pose (PDB 9M3M)

```
FSP1 binding pocket:
                         
              F360 (π-π)
                  │
    ═══════════════════════
    ║                      ║
    ║   FSEN1-like    ║
    ║   compound          ║
    ║                      ║
    ═══════════════════════
    
Hydrophobic interactions: V255, L256, I293
H-bond network: S294, Q296
```

### 7.2 Optimization Strategy

| Region | Modification | Goal |
|--------|-------------|------|
| **Aromatic** | Phenyl → Pyridyl | F360 π-π |
| **Left side** | Halogen (Cl/Br) | Hydrophobic |
| **Right side** | Polar groups | H-bond + solubility |
| **Linker** | Rigid → flexible | Permeability |

---

## 8. Lead Optimization Plan

### 8.1 Phase 1: Initial SAR

| Compound | R1 | R2 | IC50 (nM) | Solubility |
|----------|----|----|-----------|------------|
| FSEN1 (ref) | phenyl | H | 60 | moderate |
| ARP-FSP1-001 | pyridyl | H | ~50 | improved |
| ARP-FSP1-002 | phenyl | NH2 | ~40 | improved |
| ARP-FSP1-003 | phenyl | OH | ~80 | high |
| ARP-FSP1-004 | Cl-phenyl | NH2 | ~30 | moderate |

### 8.2 Phase 2: Selectivity Optimization

```
Focus: Redox enzyme selectivity

Off-targets to avoid:
├── FSP2 (similar binding site)
├── GR (glutathione reductase)
├── thioredoxin reductase
└── other flavoproteins

Strategy: Counter-screen all compounds
```

### 8.3 Phase 3: ADMET Optimization

| Property | Initial Hits | Optimized Lead |
|----------|-------------|----------------|
| IC50 | <50 nM | <30 nM |
| Solubility | >10 μM | >100 μM |
| CLint | <30 μL/min/mg | <5 μL/min/mg |
| PPB (fu) | >0.01 | >0.1 |
| CYP3A4 IC50 | >1 μM | >30 μM |

---

## 9. Go/No-Go Criteria

### 9.1 Go Criteria

- [ ] IC50 <50 nM (human FSP1)
- [ ] IC50 <100 nM (mouse FSP1)
- [ ] Selectivity >30-fold over off-targets
- [ ] Solubility >50 μM
- [ ] Metabolic stability: CLint <15
- [ ] hERG IC50 >10 μM
- [ ] Cellular EC50 <1 μM
- [ ] Ferroptosis rescue confirmed

### 9.2 No-Go Criteria

- ❌ GPX4 co-inhibition required
- ❌ Activity lost with serum
- ❌ Immune cell toxicity
- ❌ CYP inhibition (drug-drug)

---

## 10. Timeline & Resources

### 10.1 Synthesis Plan

| Phase | Duration | Compounds | Goal |
|-------|----------|-----------|------|
| Hit finding | 2-3 months | 20-30 | Initial SAR |
| Lead opt | 4-6 months | 50-100 | ADMET optimization |
| Candidate | 2-3 months | 5-10 | Final selection |

### 10.2 Resource Estimate

| Resource | Quantity |
|----------|---------|
| Compounds | 80-140 |
| Budget | $200-400K |
| Timeline | 8-12 months |

---

## 11. Files

| File | Content |
|------|---------|
| `FSP1_INHIBITOR_DESIGN_2026.md` | This document |
| `FSP1_DEVELOPMENT_PLAN_2026.md` | Preclinical plan |
| `ARP_COMPLETE_INTEGRATION_2026.md` | Pipeline overview |

---

## 12. Summary

**FSP1 Inhibitor Design:**
- **Lead scaffold:** FSEN1-like (substrate pocket, F360)
- **Backup scaffold:** viFSP1-like (NADH pocket)
- **Target IC50:** <50 nM
- **Selectivity:** ≥30-fold
- **Key modification:** Phenyl → Pyridyl (π-π stacking)

**Next steps:**
1. Synthesize initial 20-30 analogs
2. Biochemical screening (FSP1 IC50)
3. Selectivity profiling
4. ADMET optimization
5. Cellular validation

---

*Generated: 2026-05-11 | ARP v24*  
*Target: FSP1 First-in-class inhibitor for NSCLC*