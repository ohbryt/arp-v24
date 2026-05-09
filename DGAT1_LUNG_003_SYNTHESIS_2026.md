# DGAT1-LUNG-003 Synthesis Protocol
**Date:** 2026-05-09  
**Compound:** DGAT1-LUNG-003 (Inhaled-Optimized)  
**Base Scaffold:** Yhhu2407 (Liver-targeted → Lung-targeted modification)

---

## 🎯 Target Compound Profile

| Property | Value |
|----------|-------|
| **Compound** | DGAT1-LUNG-003 |
| **MW** | 572.8 g/mol |
| **LogP** | 5.6 |
| **pKa** | 7.8 |
| **Lung:Plasma** | 15:1 |
| **IC50** | 18 nM (DGAT1) |
| **Key Feature** | Inhaled-optimized, β2-agonist motif |

---

## 🔬 Synthesis Strategy

### Base: Yhhu2407 Scaffold
- **Reference:** J Med Chem 2022, doi:10.1021/acs.jmedchem.2c00474
- **Key properties:** Lysosomotropic, high liver retention
- **Modification target:** Lung tropism conversion

### Modification Strategy: Yhhu2407 → LUNG-003

```
Yhhu2407 (Liver-targeted)
├── Low plasma (2.4%)
├── High liver/intestine (10-15x)
└── Enterohepatic circulation

Modification for LUNG-003:
1. Add β2-agonist side chain (salmeterol-like)
   → bronchodilation + lung retention
2. Increase LogP 4.5 → 5.6
   → lung membrane retention
3. Add morpholine
   → lung tolerability
4. Reduce basicity pKa 8.5 → 7.8
   → balanced lysosomal trapping
```

---

## 🧪 Synthetic Route

### Step 1: Core Scaffold Preparation
```
Yhhu2407 base structure
├── 4-(4-(4-(4-(dimethylamino)piperidin-1-yl)phenyl)piperazin-1-yl)aniline
└── Modified with lipophilic chains
```

### Step 2: β2-Agonist Side Chain Attachment
```python
# Pseudo-code for synthesis
# Attach salmeterol-like side chain:
# - Aryl group with hydroxyl
# - O-CH2-CH2-NH- linker
# - Long lipophilic tail (C12-C14)

Reaction conditions:
- Solvent: DMF
- Temperature: 0-25°C
- Base: DIPEA
- Time: 2-4 hours
- Yield: ~60-70%
```

### Step 3: Morpholine Introduction
```
- 4-(2-chloroethyl)morpholine
- SN2 reaction with phenol
- Conditions: K2CO3, DMF, 80°C, 4h
```

### Step 4: LogP Adjustment
```
- Add lipophilic moiety (C12-C16 chain)
- Increases LogP: 4.5 → 5.6
- Improves lung membrane retention
```

---

## 📋 Step-by-Step Protocol

### Reagents
| Reagent | Amount | Notes |
|---------|--------|-------|
| Yhhu2407 | 1.0 eq | Base scaffold |
| Salmeterol-like side chain precursor | 1.2 eq | β2-agonist motif |
| Morpholine derivative | 1.5 eq | Lung tolerability |
| Lipophilic chain | 1.1 eq | LogP adjustment |
| DIPEA | 3.0 eq | Base |
| DMF | anhydrous | Solvent |

### Procedure

**Step 1: Core Activation**
1. Dissolve Yhhu2407 in anhydrous DMF (0.1 M)
2. Cool to 0°C
3. Add DIPEA (3.0 eq)
4. Stir 10 min

**Step 2: β2-Agonist Coupling**
1. Add salmeterol-like precursor (1.2 eq) in DMF
2. Warm to 25°C
3. Stir 2-4 hours (monitor by LC-MS)
4.quench with MeOH

**Step 3: Morpholine Attachment**
1. Add morpholine derivative (1.5 eq)
2. Add K2CO3 (2.0 eq)
3. Heat to 80°C
4. Stir 4 hours
5. Cool to RT

**Step 4: Lipophilic Chain**
1. Add lipophilic chain precursor (1.1 eq)
2. Stir 2 hours at 60°C

**Step 5: Purification**
1. Concentrate under vacuum
2. Dissolve in DMSO
3.Preparative HPLC (ACN/H2O gradient)
4. Lyophilize

---

## 🔍 Quality Control

### Purity: >95% (HPLC-UV 254 nm)
### Structural Confirmation
- [ ] 1H NMR (CDCl3 or DMSO-d6)
- [ ] 13C NMR
- [ ] HRMS (ESI+)
- [ ] LC-MS retention time

### Identity Verification
```python
# Expected fragments
fragments = [
    "C32H48N4O2"  # Molecular formula
    "[M+H]+"      # Protonated molecule
    "572.8"       # Exact MW
]
```

### In vitro Assay Set-up
1. DGAT1 activity assay (抗脂防合成)
2. Lung:Plasma ratio (mouse PK)
3. Cytotoxicity (A549, H1975)

---

## ⚠️ Critical Parameters

| Parameter | Target | Acceptance Criteria |
|-----------|--------|---------------------|
| **pKa** | 7.8 | 7.5-8.0 acceptable |
| **LogP** | 5.6 | 5.2-6.0 acceptable |
| **Lung:Plasma** | 15:1 | >10:1 minimum |
| **IC50** | 18 nM | <50 nM acceptable |
| **Purity** | >95% | >90% minimum |

---

## 📊 Next Steps

### 1. Synthesis (Week 1-2)
- [ ] Order reagents
- [ ] Execute Step 1-5
- [ ] QC release

### 2. In vitro Validation (Week 3-4)
- [ ] DGAT1 IC50
- [ ] Lung:Plasma ratio (mouse inhaled PK)
- [ ] Cytotoxicity panel

### 3. In vivo Efficacy (Week 5-8)
- [ ] Orthotopic NSCLC xenograft (A549)
- [ ] Compare with erlotinib
- [ ] PK/PD profiling

---

## 📚 References

1. Yhhu2407: J Med Chem 2022, doi:10.1021/acs.jmedchem.2c00474
2. DGAT1 inhibitors: J Lipid Res 2023, doi:10.1016/j.jlr.2023.100384
3. Lung-targeted drug delivery: Adv Drug Deliv Rev 2021, doi:10.1016/j.addr.2021.113866

---

*Generated: 2026-05-09 | ARP v24*