# Heart Failure Disease Models for MMP11/GDF10 Therapeutic Validation

**Document Type:** Experimental Disease Models  
**Date:** April 2026  
**Targets:** MMP11 (inhibition) + GDF10 (cardiac-specific augmentation)  
**Framework:** NAMs (Cell 2026) + Traditional preclinical models

---

## 1. Disease Model Strategy Overview

### 1.1 Dual-Target Therapeutic Approach

| Target | Therapeutic | Model Requirement |
|--------|-------------|-------------------|
| **MMP11** | Selective inhibitor | Fibrosis model (pro-fibrotic phenotype) |
| **GDF10** | Cardiac-specific augmentation | Maturation/cardioprotection model |

### 1.2 Model Categories

| Category | NAMs (Human-Relevant) | Traditional (Translation) |
|----------|----------------------|--------------------------|
| **In vitro** | iPSC-CMs, Cardiac organoids | Neonatal rat cardiomyocytes |
| **Ex vivo** | Human cardiac tissue, PDOs | Rat/human explants |
| **In vivo** | Humanized mice | Mouse/rat HF models |

---

## 2. NAMs-Integrated Disease Models (Primary)

### 2.1 iPSC-Derived Cardiomyocytes (iPSC-CMs)

**Rationale:** Human-relevant, patient-specific, per FDA Modernization Act 2.0

| Model | Application | Readout |
|-------|-------------|---------|
| **Healthy donor iPSC-CMs** | Baseline GDF10 response | Maturation markers, cell size |
| **HF patient iPSC-CMs** | Disease modeling | Contractility, stress response |
| **GDF10 KO iPSC-CMs** | Loss-of-function | Accelerated aging phenotype |
| **MMP11 overexpression iPSC-CMs** | Gain-of-function | Fibrosis marker expression |

**Protocol:**
```
iPSC line → Cardiomyocyte differentiation (GiW)
                ↓
Days 7-30: Maturation (GDF10 treatment)
                ↓
Assessment: Cell size, binucleation, sarcomere organization
                ↓
Stressors: Isoproterenol (100 nM), hypoxia (1% O2)
```

**Endpoints:**
| Parameter | Method | Expected Change |
|-----------|--------|-----------------|
| Cardiomyocyte size | CellProfiler | ↑ 20-30% with GDF10 |
| Binucleation | DAPI staining | ↑ with maturation |
| Sarcomere length | α-actinin IF | ↑ (mature sarcomeres) |
| Contractility | Video microscopy | ↑ with GDF10 |
| Fibrosis markers | qPCR (COL1A1, FN1) | ↓ with MMP11i |

### 2.2 Cardiac Organoids

**3D Disease Model:** Tissue-level complexity

| Organoid Type | Disease Modeling | Treatment |
|---------------|-----------------|-----------|
| **Simple cardiac organoid** | Basic cardiac differentiation | GDF10 ± MMP11i |
| **Fibrotic cardiac organoid** | TGF-β induced fibrosis | MMP11i |
| **Vasculature-integrated** | Blood flow simulation | GDF10 |
| **Patient-derived organoids (PDOs)** | Individual patient HF | Personalized therapy |

**Fibrosis Induction Protocol:**
```
Cardiac organoids (day 30)
        ↓
TGF-β (10 ng/mL) for 72 hours
        ↓
Fibrosis assessment:
  • Collagen deposition (Sirius red)
  • α-SMA expression (IF)
  • Fibrotic gene signature (RNA-seq)
        ↓
Treatment: MMP11i ± GDF10 ± combination
```

### 2.3 Heart-on-Chip

**Physiological Model:** Functional assessment with perfusion

| Platform | Application | Readout |
|---------|-------------|---------|
| **AX-IS16 microHeart** | Contractile force | FR50, beating rate |
| **HeartDynamo** | Perfusion + function | Ejection fraction analog |
| **Empyrean** | Vascularized tissue | Perfusion rate |

**Integration with NAMs Pipeline:**
```
Heart-on-Chip (7-day perfusion)
        ↓
Drug treatment: MMP11i (1 μM) + GDF10 (100 nM)
        ↓
Serial sampling:
  • Biomarkers: NT-proBNP, CTX-I
  • Imaging: Contractility
  • Transcriptomics: Pathway activation
```

---

## 3. Traditional Preclinical Disease Models

### 3.1 Ischemic Heart Failure Models

#### Model 1: Myocardial Infarction (MI) / Ischemia-Reperfusion (IRI)

| Model | Method | HF Induction | Suitability |
|-------|--------|--------------|-------------|
| **Permanent LAD ligation** | Permanent coronary occlusion | Large infarct, severe HF | High mortality |
| **IRI (30/60 min ischemia)** | Temporary occlusion + reperfusion | Moderate HF | Better survival |
| **Closed-chest IRI** | Interventional occlusion | Adjustable infarct | Most physiological |

**MI/IRI Protocol:**
```
C57BL/6 mice (8-12 weeks)
        ↓
LAD ligation (permanent or 45 min IRI)
        ↓
4 weeks post-MI:
  • Echocardiography (EF% assessment)
  • Randomization to treatment
        ↓
Treatment Groups:
  • Vehicle (control)
  • MMP11 inhibitor (10 mg/kg, oral, bid)
  • rGDF10-Fc (2.5 mg/kg, SC, qd)
  • Combination (MMP11i + rGDF10-Fc)
        ↓
8 weeks treatment → Endpoint assessment
```

**Endpoints:**
| Category | Parameters |
|----------|-------------|
| **Echocardiography** | EF%, FS%, LVEDD, LVESD, LV mass |
| **Histology** | Fibrosis area (Masson's trichrome), infarct size |
| **Molecular** | BNP, ANP, collagen I/III, MMPs, TIMPs |
| **Hemodynamics** | LV pressure-volume analysis |

#### Model 2: Transverse Aortic Constriction (TAC)

**Pressure Overload HF Model:**

| Feature | Details |
|---------|---------|
| **Method** | Surgical constriction of transverse aorta |
| **Pressure gradient** | 50-70 mmHg (moderate TAC) |
| **Timecourse** | 4-8 weeks to HF |
| **Phenotype** | Concentric hypertrophy → failure |

**TAC Protocol:**
```
C57BL/6 mice (8-10 weeks)
        ↓
TAC surgery (27G constriction)
        ↓
1 week: Pressure overload assessment
        ↓
4 weeks post-TAC (established HF):
  • Randomization
  • Treatment (same groups as MI)
        ↓
8 weeks treatment → Endpoint
```

**Why TAC for GDF10?**
- TAC causes pathological remodeling → similar to HFpEF
- MMP11 upregulation in pressure overload
- GDF10 protective effect on cardiomyocyte maturation

### 3.2 Non-Ischemic HF Models

#### Model 3: Doxorubicin (DOX)-Induced Cardiotoxicity

| Feature | Details |
|---------|---------|
| **Mechanism** | Topoisomerase II inhibition, ROS |
| **Model** | Acute cardiotoxicity (single dose) or chronic (repeated low dose) |
| **Phenotype** | Cardiomyocyte death, fibrosis, dysfunction |
| **Relevance** | Chemotherapy-induced HF |

**DOX Protocol:**
```
C57BL/6 mice (10-12 weeks)
        ↓
DOX injection (5 mg/kg, IP, weekly × 4)
        ↓
1 week after last dose: Cardiac dysfunction
        ↓
Treatment: MMP11i ± GDF10 (regeneration potential)
```

#### Model 4: Spontaneous Hypertensive Heart Failure (SHHF) Mice

| Feature | Details |
|---------|---------|
| **Model** | Genetic hypertension → HF |
| **Strain** | SHHF/Mcc (SBP > 180 mmHg) |
| **Timecourse** | 6 months: hypertrophy, 12 months: failure |
| **Advantage** | Natural disease progression |

**Use Case:** Long-term chronic HF study for AAV9-GDF10

#### Model 5: High-Fat Diet + TAC (Metabolic HF)

| Feature | Details |
|---------|---------|
| **Mechanism** | Obesity + pressure overload |
| **Model** | HFD (16 weeks) + TAC |
| **Phenotype** | HFpEF-like (preserved EF, diastolic dysfunction) |
| **Relevance** | Clinical HFpEF population |

---

## 4. Genetic Disease Models

### 4.1 GDF10 Loss-of-Function Models

| Model | Design | Application |
|-------|--------|-------------|
| **Gdf10 KO mice** | Global knockout | GDF10 mechanism validation |
| **Cardiac-specific Gdf10 KO** | cTnT-Cre × Gdf10 flox | Cardiac-specific loss |
| **Gdf10 conditional KO** | Tamoxifen-inducible | Temporal deletion |

**Expected Phenotype:**
- Decreased cardiomyocyte maturation
- Increased fibrosis post-MI
- Exacerbated HF phenotype

### 4.2 MMP11 Gain-of-Function Models

| Model | Design | Application |
|-------|--------|-------------|
| **Mmp11 TG mice** | Cardiac-specific overexpression (αMHC-Mmp11) | Pro-fibrotic phenotype |
| **Mmp11 KO mice** | Global knockout | MMP11 mechanism validation |

**Expected Phenotype:**
- Spontaneous cardiac fibrosis (TG)
- Decreased fibrosis (KO)

### 4.3 Double Mutant Model

| Model | Design | Application |
|-------|--------|-------------|
| **Mmp11 TG × Gdf10 KO** | Combined manipulation | Synergistic effects |
| **Mmp11 KO × GDF10 OE** | Therapeutic mimic | Protective effects |

---

## 5. Model Selection Matrix

### 5.1 Research Objective → Model Mapping

| Objective | Recommended Model(s) | Rationale |
|-----------|---------------------|-----------|
| **GDF10 maturation effect** | iPSC-CMs, TAC | Maturation + stress response |
| **MMP11 pro-fibrotic role** | TAC, MI/IRI | Established fibrosis |
| **Combination therapy** | MI/IRI + TAC | Compare settings |
| **Cardiac-specific delivery** | AAV9-GDF10 in MI | In vivo validation |
| **Long-term safety** | SHHF mice | Chronic dosing |
| **Human translation** | PDOs, human tissue | NAMs validation |

### 5.2 Timeline Mapping

```
Phase 1 (Months 1-6):
  In vitro: iPSC-CMs, cardiac organoids
        ↓
Phase 2 (Months 4-12):
  Ex vivo: Human cardiac tissue
  In vivo: TAC + MI/IRI (mouse)
        ↓
Phase 3 (Months 8-18):
  In vivo: SHHF (chronic), DOX (regeneration)
  GLP toxicology: Rabbit, non-human primate
```

---

## 6. Biomarker Translation (Model → Human)

| Murine Biomarker | Human Equivalent | Correlation |
|------------------|------------------|-------------|
| **NT-proBNP** | NT-proBNP | Direct |
| **Cardiac fibrosis (%)** | Cardiac MRI T1 mapping | Direct |
| **EF%** | Echocardiography EF% | Direct |
| **α-SMA expression** | Circulating fibroblasts | Indirect |
| **CTX-I (collagen turnover)** | CTX-I (serum) | Direct |
| **GDF10 (plasma)** | GDF10 (plasma) | Direct |

---

## 7. Recommended Primary Disease Model Portfolio

### 7.1 Minimum Viable Set

| Model | Purpose | Priority |
|-------|---------|----------|
| **iPSC-CMs (GDF10 response)** | NAMs human validation | HIGH |
| **TAC (fibrosis)** | MMP11i + GDF10 efficacy | HIGH |
| **MI/IRI (ischemic HF)** | Clinical translation | HIGH |
| **Human cardiac tissue** | Ex vivo validation | MEDIUM |

### 7.2 Extended Set (Full Characterization)

| Model | Purpose | Priority |
|-------|---------|----------|
| **Gdf10 KO mice** | Mechanism | MEDIUM |
| **Mmp11 TG mice** | Target validation | MEDIUM |
| **SHHF mice** | Chronic HF | LOW |
| **DOX model** | Regeneration | LOW |
| **PDOs** | Personalized medicine | MEDIUM |

---

## 8. Regulatory Considerations

### 8.1 FDA Modernization Act 2.0/3.0 Compliance

| Requirement | NAMs Contribution | Traditional Data |
|-------------|-------------------|------------------|
| **Efficacy** | iPSC/organoid + heart-on-chip | Reduced animal data |
| **Safety** | iPSC-CMs cardiotoxicity panel | Minimal GLP |
| **Pharmacology** | Human-relevant PK/PD | Species comparison |

### 8.2 IND-Enabling Studies

| Study | Species | NAMs Alternative |
|-------|---------|------------------|
| **14-day dose-range** | Rat | iPSC-CMs (high-dose) |
| **28-day toxicology** | Rat + dog | Organoid + in silico |
| **Safety pharmacology** | hERG, CIPA | iPSC-CMs + AI prediction |

---

## 9. Conclusion

### 9.1 Disease Model Strategy

| Target | Primary Model | Key Readout |
|--------|---------------|-------------|
| **MMP11 inhibition** | TAC, MI/IRI | Fibrosis reduction |
| **GDF10 augmentation** | iPSC-CMs, TAC | Maturation + function |
| **Combination** | MI/IRI + TAC | Synergistic efficacy |

### 9.2 NAMs-First Approach

> Per FDA Modernization Act 2.0: Start with human-relevant NAMs (iPSC-CMs, organoids) before traditional animal models

### 9.3 Translational Path

```
iPSC-CMs (NAMs)
        ↓
TAC/MI mouse model (mechanistic)
        ↓
SHHF/rabbit (chronic GLP toxicology)
        ↓
Human trials (NAMs-validated endpoints)
```

---

*Document generated by ARP v24 Research Pipeline · April 2026*
