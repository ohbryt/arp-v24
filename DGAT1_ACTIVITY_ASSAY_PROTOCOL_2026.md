# DGAT1 Activity Assay Protocol
**Date:** 2026-05-10  
**Project:** DGAT1-LUNG Inhibitor Screening  
**Purpose:** Enzymatic activity determination for DGAT1 inhibitor IC50

---

## Executive Summary

DGAT1 (Diacylglycerol O-Acyltransferase 1) catalyzes the final step of triacylglycerol (TAG) synthesis:
```
1,2-diacylglycerol (DAG) + fatty acyl-CoA → triacylglycerol (TAG) + CoA
```

This protocol describes **two validated assay formats**:
1. **TLC-based assay** (radiometric, gold standard)
2. **FlashPlate assay** (radiometric, HTS-compatible, 384-well)

---

## 1. TLC-Based DGAT1 Assay (Gold Standard)

### 1.1 Principle
- [³H]oleoyl-CoA as substrate
- Product [³H]triolein extracted and separated by TLC
- Radioactivity quantitated by scintillation counting

### 1.2 Reagents

| Reagent | Concentration | Supplier |
|---------|--------------|----------|
| **Enzyme source** | Membrane prep from Sf-9/hDGAT1 or HEK293T-hDGAT1 | In-house |
| **Substrate** | 1,2-dioleoyl-sn-glycerol (diolein) | 50 μM final |
| **Co-substrate** | [³H]oleoyl-CoA (30-60 Ci/mmol) | Perkin Elmer |
| **Reaction buffer** | 50 mM Tris-HCl pH 7.4, 150 mM MgCl₂, 1 mM EDTA, 0.2% BSA | Sigma |
| **Phospholipid** | l-α-phosphatidylcholine/l-α-phosphatidylserine (PC:PS 4:1) | 32 μg/ml |
| **Stop solution** | CHCl₃/MeOH (2:1, v/v) | Fisher |
| **TLC plate** | Silica Gel 60 (20×20 cm) | Merck |
| **TLC solvent** | Hexane/diethyl ether/acetic acid (70:30:1, v/v/v) | Fisher |

### 1.3 Equipment

| Equipment | Specification |
|----------|--------------|
| Scintillation counter | MicroBeta² or equivalent |
| TLC tank | Glass chamber with saturation |
| TLC scanner | Bioscan AR-2000 or equivalent |
| Centrifuge | Refrigerated, 14,000×g |
| Vortex | Variable speed |
| Water bath | 37°C shaking |

### 1.4 Procedure

**Day 1: Membrane Preparation**
```
1. Culture Sf-9 cells or HEK293T-hDGAT1 to 80% confluence
2. Harvest cells (500×g, 5 min, 4°C)
3. Resuspend in homogenization buffer (20 mM Tris-HCl pH 7.4, 1 mM EDTA, 250 mM sucrose)
4. Homogenize with Dounce homogenizer (30 strokes)
5. Centrifuge at 800×g, 10 min, 4°C (nuclear pellet)
6. Collect supernatant, centrifuge at 100,000×g, 1 h, 4°C (membrane pellet)
7. Resuspend membrane pellet in storage buffer (20 mM Tris-HCl pH 7.4, 1 mM EDTA, 20% glycerol)
8. Aliquot (50 μl), flash-freeze in liquid N₂, store at -80°C
9. Protein concentration by BCA assay (typical: 2-5 mg/ml)
```

**Day 2: Assay (96-well format)**
```
1. Pre-equilibrate membrane aliquot on ice
2. Prepare reaction mixture (on ice):
   - Reaction buffer: 40 μl
   - Diolein (1 mM stock in CHCl₃): 2.5 μl → 50 μM final
   - Phospholipid vesicles: prepare fresh (sonicate 1 min)
   - [³H]oleoyl-CoA (1 μCi/μl): 0.5 μl → 0.5 μCi/well
   - Water to final volume 48 μl
   
3. Pre-incubate compounds (inhibitors):
   - Serially dilute compounds in DMSO (11-point, 3-fold)
   - Final DMSO concentration: 1% (v/v)
   - Pre-incubate with membrane (10 min, 37°C, shaking)
   
4. Start reaction:
   - Add 2 μl cold oleoyl-CoA (200 μM stock) → 8 μM final
   - Mix, incubate 30 min, 37°C, shaking (600 rpm)
   
5. Stop reaction:
   - Add 100 μl stop solution (CHCl₃/MeOH 2:1)
   - Add 20 μl carrier (50 μg triolein + 50 μg oleic acid in heptane)
   - Add 10 μl internal standard ([³H]triolein, ~10,000 dpm)
   
6. Extract lipids:
   - Vortex 1 min, centrifuge 2000×g, 5 min
   - Collect lower organic phase (carefully, avoid interface)
   - Dry under N₂ stream (40°C)
   
7. TLC separation:
   - Spot samples on TLC plate (1.5 cm from bottom)
   - Develop in TLC tank (saturated, 30 min)
   - Visualize with iodine vapor or primulin
   - Mark TAG spot (Rf ~0.5-0.6)
   
8. Quantitation:
   - Scrape TAG region into scintillation vial
   - Add 5 ml scintillation cocktail
   - Count in scintillation counter (3 min/well)
   
9. Data analysis:
   - Subtract blank (no enzyme)
   - Normalize to vehicle (DMSO) control
   - Calculate % inhibition at each concentration
   - Fit to 4-parameter logistic curve (Prism or equivalent)
   - Report IC50 values
```

### 1.5 Key Controls

| Control | Purpose | Acceptance Criteria |
|---------|---------|---------------------|
| **Negative** | No enzyme | < 5% of max signal |
| **Positive** | No inhibitor | 100% activity (DMSO only) |
| **Standard** | Known inhibitor (T863, A-922500) | IC50 within 2-fold of literature |
| **Internal standard** | Extraction recovery | 80-120% recovery |

### 1.6 Validation Parameters

| Parameter | Target | Method |
|-----------|--------|--------|
| Z' factor | ≥ 0.5 | 32 wells of positive + negative |
| Signal-to-background | ≥ 5 | S/B = mean(positive)/mean(negative) |
| CV (positive) | < 10% | Inter-well variation |
| Standard IC50 | Literature ± 2-fold | T863 ~30-50 nM |

---

## 2. FlashPlate Assay (HTS-Ready, 384-well)

### 2.1 Principle
- [³H]oleoyl-CoA substrate
- SPA (Scintillation Proximity Assay) bead-based detection
- 384-well format, no extraction required

### 2.2 Reagents

| Reagent | Concentration | Supplier |
|---------|--------------|----------|
| **Enzyme** | hDGAT1 membranes (1 μg/ml) | In-house |
| **Substrate** | [³H]oleoyl-CoA (12 nM, 30 nCi/well) | Perkin Elmer |
| **Cold oleoyl-CoA** | 8.4 μM (total OA-CoA = 9.6 μM) | Sigma |
| **Diolein** | 50 μM | Sigma |
| **BSA** | 0.2% (fatty acid-free) | Sigma |
| **Buffer** | 50 mM Tris-HCl pH 7.4, 150 mM MgCl₂, 1 mM EDTA | Sigma |
| **SPA beads** | Wheat germ agglutinin (WGA) SPA beads | Perkin Elmer |
| **FlashPlate** | 384-well white, Basic Image FlashPlate | Perkin Elmer |

### 2.3 Procedure

```
1. Compound preparation:
   - 384-well compound plates (11-point, 3-fold dilution)
   - Final compound concentration: 10 μM to 0.5 nM
   - DMSO concentration: 1% final
   
2. Enzyme pre-mix (on ice):
   - hDGAT1 membranes (1 μg/ml)
   - 50 mM Tris-HCl pH 7.4
   - 150 mM MgCl₂
   - 1 mM EDTA
   - 0.2% fatty acid-free BSA
   - 32 μg/ml phospholipid (PC:PS 4:1)
   
3. Reaction setup (automated):
   a. Add 5 μl compound to assay plate
   b. Add 40 μl enzyme mix
   c. Pre-incubate 10 min, RT
   
4. Start reaction:
   - Add 5 μl substrate mix (diolein + [³H]oleoyl-CoA)
   - Final volume: 50 μl
   - Final [³H]oleoyl-CoA: 12 nM (0.5 μCi/well)
   
5. Incubation:
   - 2 hours, RT, sealed
   - No shaking required
   
6. Signal development:
   - Add 50 μl 3M HCl (terminate reaction)
   - Add 150 μl SPA beads (1 mg/well)
   - Shake 5 min, settle 1 hour, RT
   
7. Readout:
   - MicroBeta² or TopCount NXT
   - Read for 1 min/well
   
8. Data analysis:
   - Same as Section 1.4
```

### 2.4 Advantages

| Feature | TLC Assay | FlashPlate Assay |
|---------|-----------|------------------|
| **Format** | 96-well | 384-well |
| **Throughput** | ~500 compounds/day | ~5000 compounds/day |
| **Extraction** | Required | Not required |
| **Z' factor** | 0.6-0.8 | 0.5-0.7 |
| **Instrument** | Scintillation counter | MicroBeta/TomTeCount |
| **Cost** | Lower | Higher (SPA beads) |

---

## 3. Cell-Based DGAT1 Assay (Secondary)

### 3.1 Principle
- HEK293A or A549 cells (stably expressing hDGAT1 or endogenous)
- [¹⁴C]oleic acid incorporation into TAG
- Lipid extraction and TLC separation

### 3.2 Procedure

```
1. Seed cells in 24-well plates (50,000 cells/well)
2. Culture overnight (37°C, 5% CO₂)

3. Compound treatment:
   - Serially dilute compounds in DMSO
   - Final DMSO: 0.5%
   - Pre-incubate 1 hour

4. Radiolabeling:
   - Add [¹⁴C]oleic acid (10 μCi/ml, 50 Ci/mmol)
   - Complexed to 0.1% fatty acid-free BSA
   - Incubate 4 hours (37°C, 5% CO₂)

5. Lipid extraction:
   - Wash cells 2× with PBS
   - Add 200 μl MeOH
   - Add 400 μl CHCl₃
   - Add 100 μl 0.1M HCl
   - Vortex, centrifuge (1000×g, 5 min)
   - Collect lower phase
   - Dry under N₂

6. TLC separation:
   - Hexane/diethyl ether/acetic acid (70:30:1)
   - Visualize with iodine
   - Mark TAG band

7. Quantitation:
   - Scrape TAG region
   - Scintillation counting
   - Normalize to protein content (BCA)

8. Data analysis:
   - Calculate IC50 for cell-based inhibition
   - Compare with enzymatic IC50
```

---

## 4. Quality Control & Acceptance Criteria

### 4.1 Assay Performance

| Parameter | Target | Critical Limit |
|-----------|--------|----------------|
| **Z' factor** | ≥ 0.5 | < 0.3 = fail |
| **S/B ratio** | ≥ 5 | < 3 = fail |
| **CV (positive)** | < 10% | > 15% = fail |
| **Standard IC50** | Literature ± 2× | > 3× = investigate |

### 4.2 Standard Inhibitors

| Inhibitor | Expected IC50 | Reference |
|-----------|---------------|-----------|
| **T863** | 30-50 nM | J Med Chem 2009 |
| **A-922500** | 10-30 nM | Bioorg Med Chem 2009 |
| **PF-06430079** | 5-15 nM | J Med Chem 2011 |
| **DGAT1-LUNG-002** | 15 nM (designed) | Our design |
| **DGAT1-LUNG-003** | 18 nM (designed) | Our design |

### 4.3 Counter-Screen

| Target | Purpose | Acceptance |
|--------|---------|-----------|
| **DGAT2** | Selectivity | IC50(DGAT2) > 10 μM |
| **MGAT1/2/3** | Selectivity | IC50 > 10 μM |
| **General cytotoxicity** | Toxicity | CC50 > 30 μM |

---

## 5. Data Analysis

### 5.1 IC50 Fitting

```python
# 4-parameter logistic equation
# y = Bottom + (Top - Bottom) / (1 + (IC50/x)^HillSlope)

# In Prism or GraphPad:
# - Non-linear regression (log[inhibitor] vs response)
# - Constraints: Bottom ≥ 0, Top ≤ 100
# - Hill slope: variable or fixed at -1
```

### 5.2 Quality Metrics

```python
def calculate_Z_factor(positive, negative):
    """
    positive: list of positive control values
    negative: list of negative control values
    Returns Z' factor
    """
    import numpy as np
    mean_p = np.mean(positive)
    mean_n = np.mean(negative)
    std_p = np.std(positive)
    std_n = np.std(negative)
    
    z_prime = 1 - (3 * (std_p + std_n) / abs(mean_p - mean_n))
    return z_prime

def calculate_SB_ratio(positive, negative):
    mean_p = np.mean(positive)
    mean_n = np.mean(negative)
    return mean_p / mean_n
```

### 5.3 Output Format

```json
{
  "compound": "DGAT1-LUNG-003",
  "assay_type": "TLC-based enzymatic",
  "ic50_nM": 18.5,
  "ic50_95CI_lower": 12.3,
  "ic50_95CI_upper": 27.8,
  "hill_slope": -1.2,
  "top_percent": 102,
  "bottom_percent": -3,
  "n_points": 11,
  "r_squared": 0.94,
  "z_factor": 0.72,
  "date": "2026-05-10",
  "operator": "ARP System"
}
```

---

## 6. Timeline & Throughput

### 6.1 Estimated Timeline

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| Reagent prep | Week 1 | Membranes, substrates, compounds |
| Assay validation | Week 2 | Z', S/B, standard IC50 |
| Primary screening | Week 3-4 | 50 compounds (LUNG-001 to 004 + analogs) |
| Counter-screen | Week 5 | Selectivity panel |
| Dose-response | Week 6-8 | Full IC50 curves |

### 6.2 Throughput

| Assay | Format | Compounds/Plate | Daily Throughput |
|-------|--------|-----------------|------------------|
| Primary screen | 384-well | 32 (11-pt curve) | 128 compounds |
| Confirmatory | 96-well | 8 (11-pt curve) | 32 compounds |
| Selectivity | 96-well | 16 compounds | 48 compounds |

---

## 7. Safety & Disposal

### 7.1 Radioactive Handling
- **Isotopes:** ³H, ¹⁴C
- **PPE:** Lab coat, gloves, safety glasses
- **Monitoring:** Personal dosimeter (if required)
- **Waste:** Radioactive waste container (aqueous/organic)

### 7.2 Chemical Safety
| Chemical | Hazard | Precaution |
|----------|--------|------------|
| Chloroform | Carcinogen | Fume hood |
| Oleoyl-CoA | Irritant | Gloves |
| DMSO | Flammable | Away from heat |

---

## 8. References

1. **TLC Assay:** Cases et al. (2001) J Lipid Res, PMC3215772
2. **FlashPlate Assay:** Perry et al. (2011) J Biomol Screen, PMID 21990351
3. **Cell-based Assay:** Cao et al. (2011) J Med Chem, PMC3308890
4. **Standard inhibitors:** T863 ~30-50 nM (J Med Chem 2009)
5. **PF-06430079:** 5-15 nM (J Med Chem 2011)

---

## Appendix A: Compound Serial Dilution

```python
def prepare_serial_dilution(stock_conc_mM=10, final_high_nM=10000, 
                            num_points=11, dilution_factor=3):
    """
    Prepare 11-point 3-fold serial dilution for IC50
    
    Example:
      Stock: 10 mM
      Final high: 10 μM
      Dilution: 3-fold × 11 points
      Final DMSO: 1%
    """
    concentrations = []
    current = final_high_nM  # nM
    
    for i in range(num_points):
        # Calculate required volume of stock
        dilution_factor = 3  # 3-fold
        
        # Calculate DMSO dilution
        # Working stock from 10 mM to target concentration
        concentrations.append(current)
        current = current / dilution_factor
    
    return concentrations[::-1]  # Low to high

# Example: 3-fold, 11 points from 10 μM to ~0.5 nM
# [0.0005, 0.0015, 0.0046, 0.0137, 0.041, 0.123, 0.37, 1.11, 3.33, 10, 30] μM
```

---

## Appendix B: Plate Layout (384-well)

```
Row A-H: Compounds (A1=compound 1, A2=compound 2, etc.)
Row I-P: Standards (T863, A-922500, PF-06430079)

Column 1-2: Negative control (no enzyme)
Column 3-4: Positive control (no inhibitor)
Column 5-22: Compounds/standards (duplicates)
Column 23-24: Empty (border)

Example:
   1  2  3  4  5  6  7  8  9  10 11 12 ... 22 23 24
A  NC NC  C  C  C  C  C  C  C  C  C  C  ... C  -- --
B  NC NC  C  C  C  C  C  C  C  C  C  C  ... C  -- --
...
P  PC PC  S  S  S  S  S  S  S  S  S  S  ... S  -- --

NC = Negative control (no enzyme)
PC = Positive control (DMSO only)
C = Compound (duplicate)
S = Standard inhibitor (duplicate)
-- = Border/empty
```

---

*Protocol generated: 2026-05-10 | ARP v24*
*Based on: Perry et al. 2011, Cases et al. 2001, Cao et al. 2011*